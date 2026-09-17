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
import showdown_coherent_forms as coherent

REFERENCE = Path(__file__).with_name("showdown_pilot_reference.json")
CATEGORIES = ("SAFE_DATA_DIFF", "NO_DIFF", "SHARED_TABLE_CONFLICT", "FORM_MAPPING_BLOCK",
              "MOVE_BEHAVIOR_BLOCK", "ABILITY_BEHAVIOR_BLOCK", "NO_L1_PATH", "UNBOUND_POINTER")
FOCUS = ("Pikachu", "Pichu", "Rotom", "Zygarde", "Necrozma", "Magearna", "Zacian", "Zamazenta", "Sandshrew", "Dialga", "Zarude")


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
    if "ownership_sha256" in reference:
        require(digest(coherent.OWNERSHIP) == reference["ownership_sha256"], "Reviewed ownership policy differs from lock")
        require(digest(data.parent / "sim/dex-species.ts") == reference["dex_species_sha256"], "Modified source inheritance implementation")


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
        return "SHARED_TABLE_CONFLICT", "different coherent expectations; no approved split", None
    if any(r["move_blockers"] for r in records):
        return "MOVE_BEHAVIOR_BLOCK", "unresolved/blocked move in a consumer", None
    if uncovered or not records or any(r["form_blocker"] for r in records):
        return "FORM_MAPPING_BLOCK", "unmapped consumer or no justified coherent dataset", None
    require(len(expectations) == 1, "Missing consensus")
    target = next(iter(expectations))
    invariant = move_invariant(target, values)
    if invariant["problems"]:
        return "MOVE_BEHAVIOR_BLOCK", ",".join(invariant["problems"]), None
    if current == target:
        return "NO_DIFF", "exact ordered consensus", target
    if Counter(current) == Counter(target):
        return "MOVE_BEHAVIOR_BLOCK", "unapproved order-only change", None
    return "SAFE_DATA_DIFF", "one coherent generation per consumer; reviewed ownership; L1 and bounds valid", target


def build_inventory(data, reference):
    dex = sync.parse_pokedex(data / "pokedex.ts")
    learnsets = sync.parse_learnsets(data / "learnsets.ts")
    forms = coherent.metadata(data / "pokedex.ts")
    aliases, _ = sync.alias_indexes()
    species = sync.constants_by_kind("species")
    moves = sync.constants_by_kind("moves")
    abilities = sync.constants_by_kind("abilities")
    values = constant_values("moves", "CFRU")
    pointers, tables = read_tables(sync.CFRU_LEARNSETS)
    canonical = subprocess.check_output(["git", "-C", str(sync.CFRU_ROOT), "show",
        reference["canonical_pins"]["CFRU"] + ":src/Tables/level_up_learnsets.c"], text=True)
    baseline_pointers, baseline_tables = read_tables(coherent.TextSource(canonical))
    desired_pointers = dict(baseline_pointers)
    ownership = json.loads(coherent.OWNERSHIP.read_text())
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
    def learnset_record(key, local, policy="existing reviewed species alias or exact ID"):
        record = {"source": key, "local": local, "expected": None,
                  "move_blockers": [], "form_blocker": None, "mapping_policy": policy,
                  "selection": None, "profile": "LEARNSET_DATA_ONLY; battle/form mechanics not certified"}
        try:
            selection = coherent.select(key, learnsets, forms)
            record["selection"] = coherent.provenance(selection)
            expected = []
            for level, move in selection["moves"]:
                resolved, reason = sync.resolve_move(move, moves["DPE"], moves["CFRU"], aliases)
                if reason or resolved is None:
                    record["move_blockers"].append(f"{move}:{reason}")
                else:
                    expected.append((level, resolved[1]))
            if not record["move_blockers"]:
                base_table = baseline_pointers.get(local, "sZarudeLevelUpLearnset" if local == "zarudedada" else "")
                record["expected"] = coherent.preserve_ties(expected, baseline_tables.get(base_table, ()))
        except ValueError as error:
            record["form_blocker"] = str(error)
        return record
    mapped = 0
    selected = {k: v for k, v in dex.items() if 1 <= int(v.get("num") or 0) <= 1025}
    # A new numbered species beyond the approved Gen9 boundary is not silently included.
    for key, entry in sorted(dex.items()):
        if int(entry.get("num") or 0) > 1025:
            buckets["FORM_MAPPING_BLOCK"].append({"kind": "species", "source": key, "reason": "outside Gen1-9 NatDex boundary", "profile": "EXCLUDE_SOURCE_ONLY_SPECIES"})
    for key, entry in sorted(selected.items()):
        plan, blocker = sync.resolve_species(key, entry, species["DPE"], species["CFRU"], aliases)
        if blocker:
            local_review = any(key == group["source"] or key in group.get("equivalent_sources", []) for group in ownership["groups"])
            buckets["FORM_MAPPING_BLOCK"].append({"kind": "species", "source": key, "reason": blocker,
                "profile": "LEARNSET_ONLY_REVIEWED_OWNERSHIP; general base/ability import remains blocked" if local_review else "EXCLUDE_FROM_SUPPORTED_SOURCE_FORM_PROFILE",
                "reviewed_alias_entries": sync.matching_entries("species", key, aliases)})
            continue
        mapped += 1
        fields, blocked = sync.target_fields(entry, abilities["DPE"], aliases)
        missing = set(reference["policy"]["base_fields"]) - set(fields) - {b.split(":")[0] for b in blocked}
        if missing or plan.dpe_key not in current_base:
            buckets["FORM_MAPPING_BLOCK"].append({"kind": "base", "source": key, "reason": "missing base row/fields", "fields": sorted(missing), "profile": "EXCLUDE_UNRESOLVED_BASE_ROW"})
            fields = {}
        for problem in blocked:
            field, ability, reason = problem.split(":")
            fields.pop(field, None)
            buckets["ABILITY_BEHAVIOR_BLOCK"].append({"kind": "ability-slot", "source": key,
                "local": plan.dpe_key, "field": field, "ability": ability, "reason": reason,
                "current": current_base.get(plan.dpe_key, {}).get(field)})
        by_local_base[plan.dpe_key].append((key, fields))
        table = baseline_pointers.get(plan.cfru_key)
        record = learnset_record(key, plan.cfru_key)
        all_plans[key] = record
        if table in baseline_tables:
            by_table[table].append(record)

    # Narrow learnset-only local representation policy. Never overrides the
    # existing Base Stats/ability alias blocks or automatically accepts a prefix.
    dpe_pointers = {sync.norm(key.removeprefix("SPECIES_")): table for key, table in
                    sync.POINTER_RE.findall(uncomment(sync.DPE_LEARNSETS.read_text()))}
    covered = {r["local"] for records in by_table.values() for r in records}
    for group in ownership["groups"]:
        source = coherent.select(group["source"], learnsets, forms)
        for other in group.get("equivalent_sources", []):
            equivalent = coherent.select(other, learnsets, forms)
            require((source["generation"], source["moves"]) == (equivalent["generation"], equivalent["moves"]),
                    "Reviewed source equivalence no longer holds: " + other)
        for local in group["locals"]:
            require(local not in covered, "Ownership policy overlaps existing resolved consumer: " + local)
            require(baseline_pointers.get(local) == group["table"], "CFRU ownership drift: " + local)
            require(dpe_pointers.get(local) == group.get("dpe_table", group["table"]), "DPE ownership drift: " + local)
            record = learnset_record(group["source"], local, "showdown_learnset_ownership.json: reviewed canonical CFRU pointer ownership; DPE target=" + str(group.get("dpe_table", group["table"])))
            record["profile"] = group.get("profile", record["profile"])
            by_table[group["table"]].append(record)
            covered.add(local)

    bindings = {}
    for split in ownership["splits"]:
        require(split["to"] not in baseline_tables, "Split would overwrite an existing table")
        selected_records = [r for r in by_table[split["from"]] if r["local"] in split["locals"]]
        require({r["local"] for r in selected_records} == set(split["locals"]), "Incomplete split mapping")
        require(all(r["selection"] and r["selection"]["generation"] == split["generation"] and
                    r["expected"] and not r["move_blockers"] and not r["form_blocker"] for r in selected_records), "Blocked split consumer")
        require(len({r["expected"] for r in selected_records}) == 1, "Conflicting split expectations")
        for local in split["locals"]:
            require(baseline_pointers.get(local) == split["from"], "Split pointer ownership changed")
            bindings[local] = desired_pointers[local] = split["to"]
        by_table[split["from"]] = [r for r in by_table[split["from"]] if r not in selected_records]
        by_table[split["to"]] = selected_records

    for binding in ownership["bindings"]:
        local = binding["local"]
        require(local not in baseline_pointers and dpe_pointers.get(local) == binding["table"], "New binding lacks pinned DPE ownership")
        require(species_values[species["CFRU"][local]] == binding["species_id"], "Existing species ID changed")
        own = coherent.select(binding["source"], learnsets, forms)
        base = coherent.select(binding["equal_source"], learnsets, forms)
        require((own["generation"], own["moves"]) == (base["generation"], base["moves"]) and own["generation"] == binding["generation"], "New binding datasets differ")
        by_table[binding["table"]].append(learnset_record(binding["source"], local, binding["evidence"]))
        bindings[local] = desired_pointers[local] = binding["table"]

    require(not (tables.keys() - baseline_tables.keys() - {s["to"] for s in ownership["splits"]}),
            "Unapproved additional active table")
    require(not (pointers.keys() - desired_pointers.keys()), "Unapproved additional pointer designator")
    for local, table in baseline_pointers.items():
        require(pointers.get(local) in {table, bindings.get(local, table)}, "Unapproved or missing existing pointer: " + local)

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
            buckets["SHARED_TABLE_CONFLICT"].append({**row, "conflicts": conflicts, "profile": "BLOCK_ALL_CONFLICTING_WRITES"})
        elif changes:
            buckets["SAFE_DATA_DIFF"].append({**row, "changes": changes})
        else:
            buckets["NO_DIFF"].append({**row, "scope": "all comparable approved fields; blocked ability slots excluded"})

    targets, invariants, table_status = {}, [], {}
    for name in sorted(set(baseline_tables) | {s["to"] for s in ownership["splits"]}):
        current = tables.get(name, ())
        consumers = sorted(k for k, target in desired_pointers.items() if target == name)
        records = by_table[name]
        uncovered = sorted(set(consumers) - {r["local"] for r in records})
        if name == "sEmptyMoveset":
            category, reason, target = "NO_DIFF", "intentional NONE/EGG/reserved sentinel; EXCLUDE_FROM_RANDOM_SELECTION", None
        else:
            category, reason, target = classify_table(current, records, uncovered, values)
        row = {"kind": "learnset", "table": name, "consumers": consumers,
               "sources": [{"source": r["source"], "local": r["local"], "selection": r["selection"],
                            "mapping_policy": r["mapping_policy"], "profile": r["profile"],
                            "rows": len(r["expected"]) if r["expected"] is not None else None,
                            "form_blocker": r["form_blocker"], "move_blockers": r["move_blockers"]} for r in records],
               "reason": reason, "uncovered_consumers": uncovered, "current_rows": len(current),
               "profile": "EXCLUDE_UNRESOLVED_LOCAL_FORM" if uncovered else "DATA_SCOPE_ONLY"}
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
        if name in tables:
            invariants.append({"table": name, "consumers": sorted(k for k, t in pointers.items() if t == name),
            "planned_consumers": consumers, **invariant,
            "legal_reference_status": "PASS_EXISTING_L1_ROWS_LEGAL" if legal and not invariant["problems"] else
                                      "FAIL_NO_L1_MOVE" if not invariant["level1_initial_last4"] else "BLOCKED_REFERENCE_LEGALITY",
            "classification": category, "reference_expectation_variants": len(expected)})
        if name in tables and name != "sEmptyMoveset" and not invariant["level1_initial_last4"]:
            buckets["NO_L1_PATH"].append({"kind": "learnset", "table": name, "consumers": consumers,
                "current_rows": len(current), "selected_reference_has_L1": bool(target and target[0][0] <= 1),
                "reason": "current source lacks L1 path"})

    for local, table in sorted(bindings.items()):
        if pointers.get(local) != table:
            buckets["SAFE_DATA_DIFF"].append({"kind": "learnset-pointer", "local": local,
                "current": pointers.get(local), "reference": table, "reason": "explicit reviewed existing-ID ownership"})
    holes = [{"id": number, "constants": sorted(name for name, value in species_values.items() if value == number)}
             for number in sorted(set(range(max(seen_ids) + 1)) - seen_ids.keys())]
    buckets["UNBOUND_POINTER"].extend({"kind": "learnset-pointer", **hole} for hole in holes)

    focus = {}
    for name in FOCUS:
        table = "s" + name + "LevelUpLearnset"
        record = all_plans[name.lower()]
        target = record["expected"]
        focus[name] = {"table": table, "classification": table_status[table], "current": tables[table],
            "coherent_base_reference": target, "selection": record["selection"], "exact_base_match": tables[table] == target,
            "note": "Coherent content; existing same-level ordering preserved; explicit splits separately inventoried"}
    for rows in buckets.values():
        rows.sort(key=lambda row: json.dumps(row, sort_keys=True))
    inventory = {"schema_version": 2, "reference": reference, "layout_plan": bindings,
        "inputs_sha256": {"CFRU_learnsets": digest(sync.CFRU_LEARNSETS), "DPE_base": digest(sync.DPE_BASE_STATS)},
        "helper_sha256": {name: digest(sync.SCRIPT_DIR / name) for name in
                          ("showdown_pokemon_data_sync.py", "showdown_pinned_closure.py", "showdown_coherent_forms.py",
                           "showdown_mapping_audit.py", "dpe_base_stats_dry_diff.py")},
        "summary": {"selected_showdown_records": len(selected), "mapped_records": mapped,
            "active_pointer_bindings": len(pointers), "active_tables_including_sentinel": len(tables),
            "unbound_species_ids": holes,
            "counts": {category: len(buckets[category]) for category in CATEGORIES},
            "counts_by_kind": {category: dict(sorted(Counter(row["kind"] for row in buckets[category]).items())) for category in CATEGORIES},
            "low_level_status": dict(sorted(Counter(row["status"] for row in invariants).items())),
            "low_level_legality": dict(sorted(Counter(row["legal_reference_status"] for row in invariants).items()))},
        "inventories": buckets, "low_level_invariants": invariants, "focused_families": focus,
        "engine_limitations": ["Missing ability/move behaviors remain blocked; no engine implementation.",
            "Palafin/Terapagos/Ogerpon and other transformed forms are not certified battle mechanics.",
            "DPE EXPAND_LEARNSETS disabled; no DPE writes.", "Reserved/sentinel and explicit custom forms require supported-profile exclusions."],
        "consumer_provenance": [{"local": local, "current_target": pointers.get(local), "planned_target": table,
            "showdown_revision": reference["revision"],
            "selected_source_generations": sorted({r["selection"]["generation"] for r in by_table[table]
                if r["local"] == local and r["selection"]}),
            "unresolved_generation_reason": None if any(r["local"] == local and r["selection"] for r in by_table[table]) else
                "NOT_APPLICABLE_RESERVED_SENTINEL" if table == "sEmptyMoveset" else "UNKNOWN_UNSUPPORTED_LOCAL_FORM",
            "records": [{k: v for k, v in r.items() if k != "expected"} for r in by_table[table] if r["local"] == local],
            "disposition": "EXCLUDE_RESERVED_SENTINEL" if table == "sEmptyMoveset" else
                           "EXCLUDE_UNRESOLVED_FORM" if not any(r["local"] == local for r in by_table[table]) else table_status[table]}
            for local, table in sorted(desired_pointers.items())]}
    return inventory, targets


def verify_component_inputs(reference):
    # Lock every read dependency except the active learnsets under audit.
    for root, component, files in (
        (sync.DPE_ROOT, "DPE", ["src/Base_Stats.c", "src/Learnsets.c", "include/species.h", "include/moves.h", "include/abilities.h", "src/defines.h"]),
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
    after = coherent.render(sync.CFRU_LEARNSETS.read_text(), targets, inventory["layout_plan"], sync.constants_by_kind("species")["CFRU"])
    sync.CFRU_LEARNSETS.write_text(after)
    return len(targets)


def serialize_inventory(inventory, jsonl=False):
    if not jsonl:
        return json.dumps(inventory, indent=2, sort_keys=True) + "\n"
    # One record per line makes full before/after inventories diffable without
    # vendoring upstream TS or expanding each simple row over dozens of lines.
    metadata = {k: v for k, v in inventory.items() if k not in
                ("inventories", "low_level_invariants", "focused_families", "consumer_provenance")}
    rows = [{"record": "metadata", **metadata}]
    for category in CATEGORIES:
        rows.extend({"record": "inventory", "classification": category, **row}
                    for row in inventory["inventories"][category])
    rows.extend({"record": "low_level_invariant", **row} for row in inventory["low_level_invariants"])
    rows.extend({"record": "consumer_provenance", **row} for row in inventory.get("consumer_provenance", []))
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
            replay = coherent.render(before, targets, inventory["layout_plan"], sync.constants_by_kind("species")["CFRU"])
            require(replay.encode() == candidate.read_bytes(), "Candidate is not the exact replay of canonical safe updates and explicit bindings")
            print(f"PASS: exact whole-file replay of {len(targets)} safe tables and {len(inventory['layout_plan'])} explicit bindings; every other byte identical to canonical")
    finally:
        sync.CFRU_LEARNSETS = candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--showdown-data-dir", type=Path, required=True)
    parser.add_argument("--generation", type=int, choices=range(1, 10), help="Legacy dry-run selector; inventory still audits ALL generations for collisions")
    parser.add_argument("--cfru-learnsets", type=Path, help="Read-only alternate source .c file for baseline comparison; never allowed with --write")
    parser.add_argument("--canonical-baseline", action="store_true", help="Read-only inventory of canonical Git source, without switching or modifying a checkout")
    parser.add_argument("--write", action="store_true", help="Write only globally approved CFRU learnsets from a clean canonical candidate")
    parser.add_argument("--verify-candidate", action="store_true", help="Replay on disposable source text and compare every byte of the candidate")
    parser.add_argument("--inventory", type=Path, help="Write deterministic source-only audit JSON, not tables")
    args = parser.parse_args()
    reference = json.loads(REFERENCE.read_text())
    try:
        require(not (args.canonical_baseline and (args.write or args.verify_candidate or args.cfru_learnsets)), "Canonical baseline mode is read-only and exclusive")
        require(not (args.verify_candidate and (args.write or args.cfru_learnsets)), "Candidate replay cannot be combined with writes or alternate sources")
        if args.cfru_learnsets:
            require(not args.write, "Alternate learnset source is read-only")
            require(args.cfru_learnsets.name == "level_up_learnsets.c", "Expected active learnset source filename")
            sync.CFRU_LEARNSETS = args.cfru_learnsets
        verify_reference(args.showdown_data_dir, reference)
        verify_component_inputs(reference)
        if args.canonical_baseline:
            sync.CFRU_LEARNSETS = coherent.TextSource(subprocess.check_output(["git", "-C", str(sync.CFRU_ROOT), "show",
                reference["canonical_pins"]["CFRU"] + ":src/Tables/level_up_learnsets.c"], text=True))
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
