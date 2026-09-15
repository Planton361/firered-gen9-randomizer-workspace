#!/usr/bin/env python3
"""Pinned, source-only whole-pilot planner. Default operation never writes tables."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import showdown_pokemon_data_sync as sync

REFERENCE = Path(__file__).with_name("showdown_pilot_reference.json")
CATEGORIES = ("SAFE_DATA_DIFF", "BLOCKED_SHARED_TABLE_CONFLICT", "BLOCKED_FORM_MAPPING",
              "BLOCKED_MOVE_BEHAVIOR", "BLOCKED_ABILITY_BEHAVIOR", "ENGINE_LIMITATION", "NO_DIFF")
FOCUS = ("Pikachu", "Rotom", "Necrozma", "Zacian", "Zamazenta", "Sandshrew", "Dialga")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_reference(data, reference):
    require(git(data, "rev-parse", "HEAD") == reference["revision"], "Wrong Showdown reference commit")
    for filename, expected in reference["sha256"].items():
        require(digest(data / filename) == expected, "Modified reference file: " + filename)
    require(digest(sync.ALIAS_FILE) == reference["aliases_sha256"], "Alias configuration differs from reference lock")


def uncomment(text):
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)


def read_tables(path):
    pointers, blocks, lines = sync.parse_learnset_blocks(path)
    tables = {}
    for name, (start, end) in blocks.items():
        text = uncomment("".join(lines[start:end]))
        body = text[text.index("{") + 1:text.rindex("}")]
        pairs = tuple((int(level), move) for level, move in re.findall(
            r"LEVEL_UP_MOVE\(\s*(\d+),\s*(MOVE_\w+)\)", body))
        rest = re.sub(r"LEVEL_UP_MOVE\(\s*\d+,\s*MOVE_\w+\)\s*,", "", body).strip()
        require(rest in ("LEVEL_UP_END", "LEVEL_UP_END,"), "Unparsed or missing terminator: " + name)
        require(body.strip().endswith(("LEVEL_UP_END", "LEVEL_UP_END,")), "Nonterminal END: " + name)
        tables[name] = pairs
    return pointers, tables


def constant_values(kind, source):
    definitions = {c.name: c.value for c in sync.mapping.parse_constants(kind) if c.source == source}
    def resolve(name, seen):
        require(name not in seen, "Cyclic constant " + name)
        raw = definitions.get(name)
        require(raw is not None, "Unknown constant " + name)
        return int(raw, 0) if not raw.startswith(sync.mapping.PREFIXES[kind]) else resolve(raw, seen | {name})
    return {name: resolve(name, set()) for name in definitions}


def move_invariant(pairs, values):
    levels = [level for level, _ in pairs]
    problems = []
    if not pairs:
        problems.append("empty")
    if len(pairs) > 50:
        problems.append("exceeds-MAX_LEARNABLE_MOVES-50")
    if levels != sorted(levels) or any(not 0 <= level <= 100 for level in levels):
        problems.append("invalid-level-order-or-range")
    if any(not 0 < values.get(move, 0) <= 65535 for _, move in pairs):
        problems.append("invalid-or-zero-move-id")
    # Mirror the engine's initial-moveset prefix scan, not an arbitrary filter.
    eligible = []
    for level, move in pairs:
        if level > 1:
            break
        eligible.append(move)
    if not eligible and pairs:
        problems.append("no-level-1-path")
    return {"status": "PASS_L1_STRUCTURAL" if not problems else "FAIL_LOW_LEVEL_PATH",
            "problems": problems, "row_count": len(pairs),
            "first_move_level": levels[0] if levels else None,
            "level1_initial_last4": eligible[-4:]}


def classify_table(current, records, uncovered, values):
    """All mapped expectations (including explicit empty forms) are considered."""
    expectations = {r["expected"] for r in records if r["expected"] is not None}
    if len(expectations) > 1:
        return "BLOCKED_SHARED_TABLE_CONFLICT", "different literal ordered expectations", None
    if any(r["move_blockers"] for r in records):
        return "BLOCKED_MOVE_BEHAVIOR", "unresolved/blocked move in a consumer", None
    if uncovered or not records or any(r["form_blocker"] for r in records):
        return "BLOCKED_FORM_MAPPING", "unmapped consumer or missing/empty literal learnset; no inherited fallback", None
    require(len(expectations) == 1, "Missing consensus")
    target = next(iter(expectations))
    invariant = move_invariant(target, values)
    if invariant["problems"]:
        return "BLOCKED_MOVE_BEHAVIOR", ",".join(invariant["problems"]), None
    if current == target:
        return "NO_DIFF", "exact ordered consensus", target
    if Counter(current) == Counter(target):
        return "BLOCKED_MOVE_BEHAVIOR", "order-only change can alter initial last-four moves", None
    return "SAFE_DATA_DIFF", "unambiguous literal data; all consumers covered; L1 and bounds valid", target


def build_inventory(data, reference):
    dex = sync.parse_pokedex(data / "pokedex.ts")
    learnsets = sync.parse_learnsets(data / "learnsets.ts")
    aliases, _ = sync.alias_indexes()
    species = sync.constants_by_kind("species")
    moves = sync.constants_by_kind("moves")
    abilities = sync.constants_by_kind("abilities")
    values = constant_values("moves", "CFRU")
    pointers, tables = read_tables(sync.CFRU_LEARNSETS)
    # Numeric aliases must not hide two source designators writing the same row.
    species_values = constant_values("species", "CFRU")
    seen_ids = {}
    for key, table in pointers.items():
        value = int(key) if key.isdigit() else species_values[species["CFRU"][key]]
        require(value not in seen_ids, f"Duplicate numeric pointer ID {value}: {key}/{seen_ids.get(value)}")
        seen_ids[value] = key
    current_base = sync.base_dry.parse_dpe_base_stats(sync.DPE_BASE_STATS)
    buckets = {category: [] for category in CATEGORIES}
    by_table, by_local_base = defaultdict(list), defaultdict(list)
    all_plans = {}
    mapped = 0
    selected = {k: v for k, v in dex.items() if 1 <= int(v.get("num") or 0) <= 1025}
    # A new numbered species beyond the approved Gen9 boundary is not silently included.
    for key, entry in sorted(dex.items()):
        if int(entry.get("num") or 0) > 1025:
            buckets["BLOCKED_FORM_MAPPING"].append({"kind": "species", "source": key, "reason": "outside Gen1-9 NatDex boundary"})
    for key, entry in sorted(selected.items()):
        plan, blocker = sync.resolve_species(key, entry, species["DPE"], species["CFRU"], aliases)
        if blocker:
            buckets["BLOCKED_FORM_MAPPING"].append({"kind": "species", "source": key, "reason": blocker})
            continue
        mapped += 1
        fields, blocked = sync.target_fields(entry, abilities["DPE"], aliases)
        missing = set(reference["policy"]["base_fields"]) - set(fields) - {b.split(":")[0] for b in blocked}
        if missing or plan.dpe_key not in current_base:
            buckets["BLOCKED_FORM_MAPPING"].append({"kind": "base", "source": key, "reason": "missing base row/fields", "fields": sorted(missing)})
            fields = {}
        for problem in blocked:
            field, ability, reason = problem.split(":")
            fields.pop(field, None)
            buckets["BLOCKED_ABILITY_BEHAVIOR"].append({"kind": "ability-slot", "source": key,
                "local": plan.dpe_key, "field": field, "ability": ability, "reason": reason,
                "current": current_base.get(plan.dpe_key, {}).get(field)})
        by_local_base[plan.dpe_key].append((key, fields))
        table = pointers.get(plan.cfru_key)
        record = {"source": key, "local": plan.cfru_key, "expected": None,
                  "move_blockers": [], "form_blocker": None}
        raw = learnsets.get(key)
        if raw is None:
            record["form_blocker"] = "missing literal learnset"
        else:
            selected_moves, _ = sync.latest_level_moves(raw)
            expected = []
            for level, move in selected_moves:
                resolved, reason = sync.resolve_move(move, moves["DPE"], moves["CFRU"], aliases)
                if reason or resolved is None:
                    record["move_blockers"].append(f"{move}:{reason}")
                else:
                    expected.append((level, resolved[1]))
            if not record["move_blockers"]:
                record["expected"] = tuple(expected)
            if not selected_moves:
                record["form_blocker"] = "no literal level-up sources; empty is not an inheritance rule"
        all_plans[key] = record
        if table not in tables:
            buckets["BLOCKED_FORM_MAPPING"].append({"kind": "learnset-mapping", "source": key,
                "local": plan.cfru_key, "reason": "missing local pointer/table"})
        else:
            by_table[table].append(record)

    # Coalesce base rows/fields too: do not let the last source form win.
    for local, records in sorted(by_local_base.items()):
        if any(not fields for _, fields in records):
            continue  # Already inventoried as incomplete; not a NO_DIFF claim.
        changes, conflicts = {}, {}
        for field in reference["policy"]["base_fields"]:
            expected = {fields[field] for _, fields in records if field in fields}
            if len(expected) > 1:
                conflicts[field] = sorted(expected)
            elif expected and len([1 for _, fields in records if field in fields]) == len(records):
                value = next(iter(expected))
                if current_base[local].get(field) != value:
                    changes[field] = {"current": current_base[local].get(field), "reference": value}
        row = {"kind": "base", "local": local, "sources": sorted(k for k, _ in records)}
        if conflicts:
            buckets["BLOCKED_SHARED_TABLE_CONFLICT"].append({**row, "conflicts": conflicts})
        elif changes:
            buckets["SAFE_DATA_DIFF"].append({**row, "changes": changes})
        else:
            buckets["NO_DIFF"].append({**row, "scope": "all comparable approved fields; blocked ability slots excluded"})

    targets, invariants, table_status = {}, [], {}
    for name, current in sorted(tables.items()):
        consumers = sorted(k for k, target in pointers.items() if target == name)
        records = by_table[name]
        uncovered = sorted(set(consumers) - {r["local"] for r in records})
        if name == "sEmptyMoveset":
            category, reason, target = "ENGINE_LIMITATION", "intentional NONE/EGG/reserved sentinel, not an encounter species", None
        else:
            category, reason, target = classify_table(current, records, uncovered, values)
        row = {"kind": "learnset", "table": name, "consumers": consumers,
               "sources": [{"source": r["source"], "rows": len(r["expected"]) if r["expected"] is not None else None,
                            "form_blocker": r["form_blocker"], "move_blockers": r["move_blockers"]} for r in records],
               "reason": reason, "uncovered_consumers": uncovered, "current_rows": len(current)}
        if target is not None:
            row["reference_rows"] = len(target)
        if category == "SAFE_DATA_DIFF":
            row["removed"] = list((Counter(current) - Counter(target)).elements())
            row["added"] = list((Counter(target) - Counter(current)).elements())
            targets[name] = target
        buckets[category].append(row)
        table_status[name] = category
        invariant = move_invariant(current, values)
        expected = {r["expected"] for r in records if r["expected"] is not None}
        # Source legality is not inferred for unresolved forms, even if rows are nonempty.
        legal = target is not None and all(pair in target for pair in current if pair[0] <= 1)
        invariants.append({"table": name, "consumers": consumers, **invariant,
            "legal_reference_status": "PASS_EXISTING_L1_ROWS_LEGAL" if legal and not invariant["problems"] else
                                      "FAIL_NO_L1_MOVE" if not invariant["level1_initial_last4"] else "BLOCKED_REFERENCE_LEGALITY",
            "classification": category, "reference_expectation_variants": len(expected)})

    focus = {}
    for name in FOCUS:
        table = "s" + name + "LevelUpLearnset"
        record = all_plans[name.lower()]
        target = record["expected"]
        focus[name] = {"table": table, "classification": table_status[table], "current": tables[table],
            "literal_base_reference": target, "exact_base_match": tables[table] == target,
            "note": "Literal base expectation is evidence only; all shared consumers must agree before writing"}
    engine = [
        ("Commander/Hospitality/Embody Aspect", "missing existing engine mechanics; blocked assignments retained"),
        ("Palafin/Terapagos", "existing partial/alias display and form semantics are not Gen9 behavior clearance"),
        ("DPE learnsets", "EXPAND_LEARNSETS disabled; dormant DPE tables are not a synchronization target"),
    ]
    buckets["ENGINE_LIMITATION"].extend({"kind": "policy", "subject": key, "reason": reason} for key, reason in engine)
    for rows in buckets.values():
        rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    inventory = {"schema_version": 1, "reference": reference,
        "inputs_sha256": {"CFRU_learnsets": digest(sync.CFRU_LEARNSETS), "DPE_base": digest(sync.DPE_BASE_STATS)},
        "helper_sha256": {name: digest(sync.SCRIPT_DIR / name) for name in
                          ("showdown_pokemon_data_sync.py", "showdown_pinned_closure.py",
                           "showdown_mapping_audit.py", "dpe_base_stats_dry_diff.py")},
        "summary": {"selected_showdown_records": len(selected), "mapped_records": mapped,
            "active_pointer_bindings": len(pointers), "active_tables_including_sentinel": len(tables),
            "unbound_species_ids": [{"id": number, "constants": sorted(name for name, value in species_values.items() if value == number)}
                                    for number in sorted(set(range(max(seen_ids) + 1)) - seen_ids.keys())],
            "counts": {category: len(buckets[category]) for category in CATEGORIES},
            "counts_by_kind": {category: dict(sorted(Counter(row["kind"] for row in buckets[category]).items())) for category in CATEGORIES},
            "low_level_status": dict(sorted(Counter(row["status"] for row in invariants).items())),
            "low_level_legality": dict(sorted(Counter(row["legal_reference_status"] for row in invariants).items()))},
        "inventories": buckets, "low_level_invariants": invariants, "focused_families": focus}
    return inventory, targets


def verify_component_inputs(reference):
    # Lock every read dependency except the active learnsets under audit.
    for root, component, files in (
        (sync.DPE_ROOT, "DPE", ["src/Base_Stats.c", "include/species.h", "include/moves.h", "include/abilities.h", "src/defines.h"]),
        (sync.CFRU_ROOT, "CFRU", ["include/constants/species.h", "include/constants/moves.h", "include/constants/abilities.h", "include/new/learn_move.h", "src/learn_move.c", "src/config.h"]),
    ):
        pin = reference["canonical_pins"][component]
        for file in files:
            require(git(root, "hash-object", file) == git(root, "rev-parse", pin + ":" + file),
                    component + " input differs from canonical pilot: " + file)
    require("#define MAX_LEARNABLE_MOVES 50" in (sync.CFRU_ROOT / "include/new/learn_move.h").read_text(), "Re-audit stack bound")
    require(not re.search(r"^\s*#define\s+EXPAND_LEARNSETS\b", uncomment((sync.DPE_ROOT / "src/defines.h").read_text()), re.M), "DPE active learnset policy changed")
    require(re.search(r"^\s*#define\s+EXPAND_MOVESETS\b", uncomment((sync.CFRU_ROOT / "src/config.h").read_text()), re.M), "CFRU learnsets are not active")


def write_cfru(inventory, targets, reference):
    root = sync.CFRU_ROOT
    require(git(root, "rev-parse", "--absolute-git-dir") != git(root, "rev-parse", "--path-format=absolute", "--git-common-dir"),
            "Writes require an isolated linked worktree")
    require(git(root, "branch", "--show-current") not in ("", "main", "master"), "Writes require an isolated candidate branch")
    require(git(root, "rev-parse", "HEAD") == reference["canonical_pins"]["CFRU"], "First write must start at canonical CFRU pin, not #46")
    require(not git(root, "diff", "--name-only", "HEAD", "--", "src", "include", "assembly"), "Source worktree is not clean")
    require(not any(r["kind"] == "base" for r in inventory["inventories"]["SAFE_DATA_DIFF"]), "Separate bounded DPE candidate required; no implicit multi-component write")
    pointers, _ = read_tables(sync.CFRU_LEARNSETS)
    updates = {key: list(targets[table]) for key, table in pointers.items() if table in targets}
    return sync.update_learnsets_file(sync.CFRU_LEARNSETS, updates, cfru=True, approved_tables=set(targets))


def serialize_inventory(inventory, jsonl=False):
    if not jsonl:
        return json.dumps(inventory, indent=2, sort_keys=True) + "\n"
    # One record per line makes full before/after inventories diffable without
    # vendoring upstream TS or expanding each simple row over dozens of lines.
    metadata = {k: v for k, v in inventory.items() if k not in
                ("inventories", "low_level_invariants", "focused_families")}
    rows = [{"record": "metadata", **metadata}]
    for category in CATEGORIES:
        rows.extend({"record": "inventory", "classification": category, **row}
                    for row in inventory["inventories"][category])
    rows.extend({"record": "low_level_invariant", **row} for row in inventory["low_level_invariants"])
    rows.extend({"record": "focused_family", "family": family, **row}
                for family, row in sorted(inventory["focused_families"].items()))
    return "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)


def verify_candidate(data, reference):
    """Replay on a disposable source-text fixture; never overwrite component input."""
    candidate = sync.CFRU_LEARNSETS
    before = subprocess.check_output(["git", "-C", str(sync.CFRU_ROOT), "show",
        reference["canonical_pins"]["CFRU"] + ":src/Tables/level_up_learnsets.c"], text=True)
    try:
        with tempfile.TemporaryDirectory(prefix="showdown-source-replay-") as tmp:
            source = Path(tmp) / "level_up_learnsets.c"
            source.write_text(before)
            sync.CFRU_LEARNSETS = source
            inventory, targets = build_inventory(data, reference)
            pointers, _ = read_tables(source)
            updates = {key: list(targets[table]) for key, table in pointers.items() if table in targets}
            sync.update_learnsets_file(source, updates, True, approved_tables=set(targets))
            require(source.read_bytes() == candidate.read_bytes(), "Candidate is not the exact replay of canonical safe updates")
            print(f"PASS: exact whole-file replay of {len(targets)} safe tables; every other byte identical to canonical")
    finally:
        sync.CFRU_LEARNSETS = candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--showdown-data-dir", type=Path, required=True)
    parser.add_argument("--generation", type=int, choices=range(1, 10), help="Legacy dry-run selector; inventory still audits ALL generations for collisions")
    parser.add_argument("--cfru-learnsets", type=Path, help="Read-only alternate source .c file for baseline comparison; never allowed with --write")
    parser.add_argument("--write", action="store_true", help="Write only globally approved CFRU learnsets from a clean canonical candidate")
    parser.add_argument("--verify-candidate", action="store_true", help="Replay on disposable source text and compare every byte of the candidate")
    parser.add_argument("--inventory", type=Path, help="Write deterministic source-only audit JSON, not tables")
    args = parser.parse_args()
    reference = json.loads(REFERENCE.read_text())
    try:
        require(not (args.verify_candidate and (args.write or args.cfru_learnsets)), "Candidate replay cannot be combined with writes or alternate sources")
        if args.cfru_learnsets:
            require(not args.write, "Alternate learnset source is read-only")
            require(args.cfru_learnsets.name == "level_up_learnsets.c", "Expected active learnset source filename")
            sync.CFRU_LEARNSETS = args.cfru_learnsets
        verify_reference(args.showdown_data_dir, reference)
        verify_component_inputs(reference)
        inventory, targets = build_inventory(args.showdown_data_dir, reference)
        if args.verify_candidate:
            verify_candidate(args.showdown_data_dir, reference)
        if args.write:
            require(args.generation is None, "Partial-generation writes forbidden: shared tables cross generations")
            changed = write_cfru(inventory, targets, reference)
            post, _ = build_inventory(args.showdown_data_dir, reference)
            require(not post["inventories"]["SAFE_DATA_DIFF"], "Post-write SAFE_DATA_DIFF remains; candidate must stop")
            print(f"CFRU tables written: {changed}; post-write SAFE_DATA_DIFF: 0")
            inventory = post
        if args.inventory:
            args.inventory.write_text(serialize_inventory(inventory, args.inventory.suffix == ".jsonl"))
        print(json.dumps(inventory["summary"], indent=2, sort_keys=True))
        return 0
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(2, "FAIL CLOSED: " + str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
