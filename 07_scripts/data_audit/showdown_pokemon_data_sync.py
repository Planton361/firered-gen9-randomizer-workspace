#!/usr/bin/env python3
"""Fail-closed Pokemon Showdown -> local CFRU/DPE data sync helper.

This helper is intended for controlled generation-by-generation data commits.
It reads an external Pokemon Showdown data checkout and local CFRU/DPE tables.
It writes only when --write is passed.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import showdown_mapping_audit as mapping
import dpe_base_stats_dry_diff as base_dry


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
ALIAS_FILE = SCRIPT_DIR / "showdown_aliases.json"

DPE_ROOT = REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9"
CFRU_ROOT = REPO_ROOT / "02_external/CFRU-expansion"

DPE_BASE_STATS = DPE_ROOT / "src/Base_Stats.c"
DPE_LEARNSETS = DPE_ROOT / "src/Learnsets.c"
CFRU_LEARNSETS = CFRU_ROOT / "src/Tables/level_up_learnsets.c"

GEN_RANGES = {
    1: (1, 151),
    2: (152, 251),
    3: (252, 386),
    4: (387, 493),
    5: (494, 649),
    6: (650, 721),
    7: (722, 809),
    8: (810, 905),
    9: (906, 9999),
}

BASE_STAT_FIELDS = {
    "hp": "baseHP",
    "atk": "baseAttack",
    "def": "baseDefense",
    "spa": "baseSpAttack",
    "spd": "baseSpDefense",
    "spe": "baseSpeed",
}

ABILITY_FIELDS = {
    "0": "ability1",
    "1": "ability2",
    "H": "hiddenAbility",
}

FIELD_RE = re.compile(r"^(\s*\.(?P<field>[A-Za-z0-9_]+)\s*=\s*)(?P<value>[^,]+)(,.*)$")
SPECIES_BLOCK_RE = re.compile(r"^(\s*)\[(SPECIES_[A-Z0-9_]+)\]\s*=")
LEARNSET_DECL_RE = re.compile(r"static const struct LevelUpMove (s[A-Za-z0-9_]+LevelUpLearnset)\[\] = \{")
POINTER_RE = re.compile(r"\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*(s[A-Za-z0-9_]+LevelUpLearnset)")


@dataclass
class SpeciesPlan:
    showdown_key: str
    dpe_key: str
    cfru_key: str
    dpe_constant: str
    cfru_constant: str
    num: int


def norm(value: str) -> str:
    return mapping.normalize(value)


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] in "'\"" and value[-1] == value[0]:
        return value[1:-1]
    return value


def parse_ts_blocks(path: Path) -> dict[str, str]:
    return base_dry.parse_ts_blocks(path)


def parse_pokedex(path: Path) -> dict[str, dict[str, object]]:
    parsed = base_dry.parse_showdown_pokedex(path)
    for key, block in parse_ts_blocks(path).items():
        num_match = re.search(r"\bnum:\s*(-?\d+)", block)
        parsed.setdefault(key, {})["num"] = int(num_match.group(1)) if num_match else 0
        nonstandard_match = re.search(r'\bisNonstandard:\s*"([^"]+)"', block)
        if nonstandard_match:
            parsed[key]["isNonstandard"] = nonstandard_match.group(1)
        if "genderRatio" not in parsed[key] and "gender:" not in block:
            parsed[key]["genderRatio"] = "PERCENT_FEMALE(50)"
    return parsed


def parse_learnsets(path: Path) -> dict[str, dict[str, list[str]]]:
    result: dict[str, dict[str, list[str]]] = {}
    for key, block in parse_ts_blocks(path).items():
        learn_match = re.search(r"learnset:\s*\{(?P<body>.*?)\n\s*\}", block, re.S)
        if not learn_match:
            continue
        moves: dict[str, list[str]] = {}
        for move, raw_sources in re.findall(r"([A-Za-z0-9_]+):\s*\[([^\]]+)\]", learn_match.group("body")):
            sources = re.findall(r'"([^"]+)"', raw_sources)
            moves[norm(move)] = sources
        result[key] = moves
    return result


def latest_level_moves(move_sources: dict[str, list[str]]) -> tuple[list[tuple[int, str]], list[str]]:
    selected: list[tuple[int, int, str]] = []
    non_level: list[str] = []
    for order, (move_key, sources) in enumerate(move_sources.items()):
        level_sources: list[tuple[int, int]] = []
        for source in sources:
            match = re.fullmatch(r"(\d+)L(\d+)", source)
            if match:
                level_sources.append((int(match.group(1)), int(match.group(2))))
        if not level_sources:
            continue
        latest_gen = max(gen for gen, _ in level_sources)
        latest_levels = sorted({level for gen, level in level_sources if gen == latest_gen})
        if not latest_levels:
            non_level.append(move_key)
        for level in latest_levels:
            selected.append((level, order, move_key))
    selected.sort(key=lambda item: (item[0], item[1], item[2]))
    return [(level, move_key) for level, _, move_key in selected], non_level


def raw_alias_entries() -> list[dict[str, object]]:
    with ALIAS_FILE.open("r", encoding="utf-8") as handle:
        return list(json.load(handle).get("entries", []))


def alias_indexes() -> tuple[dict[str, list[dict[str, object]]], dict[str, list[dict[str, object]]]]:
    by_showdown: dict[str, list[dict[str, object]]] = defaultdict(list)
    by_local: dict[str, list[dict[str, object]]] = defaultdict(list)
    for entry in raw_alias_entries():
        showdown_key = entry.get("showdown_key")
        if showdown_key:
            by_showdown[f"{entry.get('kind')}:{norm(str(showdown_key))}"].append(entry)
        for local_key in entry.get("local_keys", []):
            by_local[f"{entry.get('kind')}:{norm(str(local_key))}"].append(entry)
    return by_showdown, by_local


def blocked_entry(entry: dict[str, object]) -> bool:
    return entry.get("status") in {"open-risk", "behavior-risk"} or entry.get("generator_policy") == "blocked"


def ignored_entry(entry: dict[str, object]) -> bool:
    return entry.get("status") == "ignore"


def constants_by_kind(kind: str) -> dict[str, dict[str, str]]:
    grouped: dict[str, dict[str, str]] = {"DPE": {}, "CFRU": {}}
    for constant in mapping.parse_constants(kind):
        grouped[constant.source][constant.normalized] = constant.name
    return grouped


def constants_set(kind: str) -> dict[str, set[str]]:
    grouped = constants_by_kind(kind)
    return {source: set(values.values()) for source, values in grouped.items()}


def resolve_species(
    key: str,
    pokedex_entry: dict[str, object],
    dpe_species: dict[str, str],
    cfru_species: dict[str, str],
    by_showdown: dict[str, list[dict[str, object]]],
) -> tuple[SpeciesPlan | None, str | None]:
    num = int(pokedex_entry.get("num") or 0)
    entries = by_showdown.get(f"species:{key}", [])
    if any(blocked_entry(entry) for entry in entries):
        return None, "species-open-risk"
    if any(ignored_entry(entry) for entry in entries):
        return None, "species-ignore"

    candidates: list[tuple[str, str]] = []
    if key in dpe_species and key in cfru_species:
        candidates.append((key, key))
    for entry in entries:
        if entry.get("status") != "alias":
            continue
        dpe_candidates: set[str] = set()
        cfru_candidates: set[str] = set()
        for local_key in entry.get("local_keys", []):
            normalized = norm(str(local_key))
            if normalized in dpe_species:
                dpe_candidates.add(normalized)
            if normalized in cfru_species:
                cfru_candidates.add(normalized)
        for local_constant in entry.get("local_constants", []):
            normalized = norm(str(local_constant).removeprefix("SPECIES_"))
            if normalized in dpe_species:
                dpe_candidates.add(normalized)
            if normalized in cfru_species:
                cfru_candidates.add(normalized)
        for dpe_key in dpe_candidates:
            for cfru_key in cfru_candidates:
                candidates.append((dpe_key, cfru_key))

    candidates = sorted(set(candidates))
    if not candidates:
        return None, "species-unmapped"
    if len(candidates) > 1:
        return None, "species-ambiguous"
    dpe_key, cfru_key = candidates[0]
    return SpeciesPlan(key, dpe_key, cfru_key, dpe_species[dpe_key], cfru_species[cfru_key], num), None


def resolve_ability(
    ability_key: str,
    dpe_abilities: dict[str, str],
    by_showdown: dict[str, list[dict[str, object]]],
) -> tuple[str | None, str | None]:
    entries = by_showdown.get(f"abilities:{ability_key}", [])
    if ability_key in dpe_abilities:
        if any(blocked_entry(entry) for entry in entries):
            return dpe_abilities[ability_key], "ability-blocked-name"
        return dpe_abilities[ability_key], None
    for entry in entries:
        if blocked_entry(entry):
            return None, "ability-blocked-alias"
        if ignored_entry(entry):
            return None, "ability-ignored"
        if entry.get("status") == "alias":
            for local_key in entry.get("local_keys", []):
                normalized = norm(str(local_key))
                if normalized in dpe_abilities:
                    return dpe_abilities[normalized], None
    return None, "ability-unmapped"


def resolve_move(
    move_key: str,
    dpe_moves: dict[str, str],
    cfru_moves: dict[str, str],
    by_showdown: dict[str, list[dict[str, object]]],
) -> tuple[tuple[str, str] | None, str | None]:
    entries = by_showdown.get(f"moves:{move_key}", [])
    if any(blocked_entry(entry) for entry in entries):
        return None, "move-open-risk"
    if any(ignored_entry(entry) for entry in entries):
        return None, "move-ignore"
    if move_key in dpe_moves and move_key in cfru_moves:
        return (dpe_moves[move_key], cfru_moves[move_key]), None
    for entry in entries:
        if entry.get("status") != "alias":
            continue
        for local_key in entry.get("local_keys", []):
            normalized = norm(str(local_key))
            if normalized in dpe_moves and normalized in cfru_moves:
                return (dpe_moves[normalized], cfru_moves[normalized]), None
    return None, "move-unmapped"


def target_fields(
    pokedex_entry: dict[str, object],
    dpe_abilities: dict[str, str],
    by_showdown: dict[str, list[dict[str, object]]],
) -> tuple[dict[str, str], list[str]]:
    fields: dict[str, str] = {}
    blockers: list[str] = []

    base_stats = pokedex_entry.get("baseStats")
    if isinstance(base_stats, dict):
        for source_field, local_field in BASE_STAT_FIELDS.items():
            if source_field in base_stats:
                fields[local_field] = str(base_stats[source_field])

    types = pokedex_entry.get("types")
    if isinstance(types, tuple) and types:
        fields["type1"] = str(types[0])
        fields["type2"] = str(types[1] if len(types) > 1 else types[0])

    gender = pokedex_entry.get("genderRatio")
    if isinstance(gender, str):
        fields["genderRatio"] = gender

    egg_groups = pokedex_entry.get("eggGroups")
    if isinstance(egg_groups, tuple) and egg_groups:
        fields["eggGroup1"] = str(egg_groups[0])
        fields["eggGroup2"] = str(egg_groups[1] if len(egg_groups) > 1 else egg_groups[0])

    abilities = pokedex_entry.get("abilities")
    if isinstance(abilities, dict):
        for label, field in ABILITY_FIELDS.items():
            ability_key = abilities.get(label)
            if ability_key is None:
                fields[field] = "ABILITY_NONE"
                continue
            local_ability, blocker = resolve_ability(str(ability_key), dpe_abilities, by_showdown)
            if blocker == "ability-blocked-name":
                blockers.append(f"{field}:{ability_key}:{blocker}")
                if local_ability:
                    fields[field] = local_ability
            elif blocker:
                blockers.append(f"{field}:{ability_key}:{blocker}")
            else:
                fields[field] = str(local_ability)

    return fields, blockers


def parse_base_blocks(path: Path) -> dict[str, tuple[int, int, list[str]]]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    blocks: dict[str, tuple[int, int, list[str]]] = {}
    current_key: str | None = None
    start = 0
    for idx, line in enumerate(lines):
        match = SPECIES_BLOCK_RE.match(line)
        if match:
            current_key = norm(match.group(2).removeprefix("SPECIES_"))
            start = idx
            continue
        if current_key is not None and line.strip() == "},":
            blocks[current_key] = (start, idx + 1, lines[start : idx + 1])
            current_key = None
    return blocks


def update_base_stats_file(path: Path, updates: dict[str, dict[str, str]]) -> int:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    blocks = parse_base_blocks(path)
    changed = 0
    for local_key, fields in updates.items():
        block = blocks.get(local_key)
        if not block:
            continue
        start, end, block_lines = block
        new_block: list[str] = []
        for line in block_lines:
            match = FIELD_RE.match(line)
            if match and match.group("field") in fields:
                new_line = f"{match.group(1)}{fields[match.group('field')]}{match.group(4)}\n"
                if new_line != line:
                    changed += 1
                new_block.append(new_line)
            else:
                new_block.append(line)
        lines[start:end] = new_block
    if changed:
        path.write_text("".join(lines), encoding="utf-8")
    return changed


def parse_learnset_blocks(path: Path) -> tuple[dict[str, str], dict[str, tuple[int, int]], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    pointers: dict[str, str] = {}
    blocks: dict[str, tuple[int, int]] = {}
    current_name: str | None = None
    start = 0
    for idx, line in enumerate(lines):
        pointer = POINTER_RE.search(line)
        if pointer:
            pointers[norm(pointer.group(1).removeprefix("SPECIES_"))] = pointer.group(2)
        decl = LEARNSET_DECL_RE.match(line)
        if decl:
            current_name = decl.group(1)
            start = idx
            continue
        if current_name is not None and line.strip() == "};":
            blocks[current_name] = (start, idx + 1)
            current_name = None
    return pointers, blocks, lines


def format_learnset_block(name: str, moves: list[tuple[int, str]], cfru: bool) -> list[str]:
    end = "\tLEVEL_UP_END,\n" if cfru else "\tLEVEL_UP_END\n"
    lines = [f"static const struct LevelUpMove {name}[] = {{\n"]
    for level, move in moves:
        lines.append(f"\tLEVEL_UP_MOVE({level:2d}, {move}),\n")
    lines.append(end)
    lines.append("};\n")
    return lines


def update_learnsets_file(path: Path, updates: dict[str, list[tuple[int, str]]], cfru: bool) -> int:
    pointers, blocks, lines = parse_learnset_blocks(path)
    changed = 0
    replacements: list[tuple[int, int, list[str]]] = []
    for local_key, moves in updates.items():
        name = pointers.get(local_key)
        if not name or name not in blocks:
            continue
        start, end = blocks[name]
        new_block = format_learnset_block(name, moves, cfru)
        if lines[start:end] != new_block:
            changed += 1
            replacements.append((start, end, new_block))
    for start, end, new_block in sorted(replacements, reverse=True):
        lines[start:end] = new_block
    if changed:
        path.write_text("".join(lines), encoding="utf-8")
    return changed


def generation_species(pokedex: dict[str, dict[str, object]], generation: int) -> dict[str, dict[str, object]]:
    lo, hi = GEN_RANGES[generation]
    return {
        key: value
        for key, value in pokedex.items()
        if lo <= int(value.get("num") or 0) <= hi
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--showdown-data-dir", required=True)
    parser.add_argument("--generation", type=int, choices=range(1, 10), required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    showdown_dir = Path(args.showdown_data_dir)
    pokedex = parse_pokedex(showdown_dir / "pokedex.ts")
    learnsets = parse_learnsets(showdown_dir / "learnsets.ts")
    by_showdown, _ = alias_indexes()

    species_constants = constants_by_kind("species")
    move_constants = constants_by_kind("moves")
    ability_constants = constants_by_kind("abilities")

    selected = generation_species(pokedex, args.generation)
    plans: list[SpeciesPlan] = []
    blockers: Counter[str] = Counter()
    blocked_samples: dict[str, list[str]] = defaultdict(list)
    base_updates: dict[str, dict[str, str]] = {}
    dpe_learnset_updates: dict[str, list[tuple[int, str]]] = {}
    cfru_learnset_updates: dict[str, list[tuple[int, str]]] = {}

    dpe_current = base_dry.parse_dpe_base_stats(DPE_BASE_STATS)

    for showdown_key, entry in sorted(selected.items(), key=lambda item: (int(item[1].get("num") or 0), item[0])):
        plan, species_blocker = resolve_species(
            showdown_key,
            entry,
            species_constants["DPE"],
            species_constants["CFRU"],
            by_showdown,
        )
        if species_blocker:
            blockers[species_blocker] += 1
            blocked_samples[species_blocker].append(showdown_key)
            continue
        assert plan is not None
        plans.append(plan)

        fields, ability_blockers = target_fields(entry, ability_constants["DPE"], by_showdown)
        for blocker in ability_blockers:
            blockers["ability-blocked"] += 1
            blocked_samples["ability-blocked"].append(f"{showdown_key}:{blocker}")
            field = blocker.split(":", 1)[0]
            fields.pop(field, None)

        current = dpe_current.get(plan.dpe_key, {})
        changed_fields = {field: value for field, value in fields.items() if current.get(field) != value}
        if changed_fields:
            base_updates[plan.dpe_key] = changed_fields

        move_sources = learnsets.get(showdown_key)
        if not move_sources:
            blockers["learnset-missing-showdown"] += 1
            blocked_samples["learnset-missing-showdown"].append(showdown_key)
            continue
        level_moves, _ = latest_level_moves(move_sources)
        dpe_moves: list[tuple[int, str]] = []
        cfru_moves: list[tuple[int, str]] = []
        learnset_blocked = False
        for level, move_key in level_moves:
            resolved, move_blocker = resolve_move(move_key, move_constants["DPE"], move_constants["CFRU"], by_showdown)
            if move_blocker or resolved is None:
                blockers["learnset-move-blocked"] += 1
                blocked_samples["learnset-move-blocked"].append(f"{showdown_key}:{move_key}:{move_blocker}")
                learnset_blocked = True
                break
            dpe_move, cfru_move = resolved
            dpe_moves.append((level, dpe_move))
            cfru_moves.append((level, cfru_move))
        if learnset_blocked:
            continue
        dpe_learnset_updates[plan.dpe_constant] = dpe_moves
        cfru_learnset_updates[plan.cfru_constant] = cfru_moves

    print(f"generation: {args.generation}")
    print(f"showdown_species_in_generation: {len(selected)}")
    print(f"mapped_species: {len(plans)}")
    print(f"base_species_with_changes: {len(base_updates)}")
    print(f"base_field_changes: {sum(len(fields) for fields in base_updates.values())}")
    print(f"learnset_species_ready: {len(dpe_learnset_updates)}")
    print("blockers:")
    for key, value in sorted(blockers.items()):
        print(f"- {key}: {value}")
        for sample in blocked_samples[key][:10]:
            print(f"  - {sample}")
        if len(blocked_samples[key]) > 10:
            print(f"  - ... {len(blocked_samples[key]) - 10} more")

    if args.write:
        base_changed = update_base_stats_file(DPE_BASE_STATS, base_updates)
        dpe_learnsets_changed = update_learnsets_file(DPE_LEARNSETS, dpe_learnset_updates, cfru=False)
        cfru_learnsets_changed = update_learnsets_file(CFRU_LEARNSETS, cfru_learnset_updates, cfru=True)
        print("writes:")
        print(f"- dpe_base_field_lines_changed: {base_changed}")
        print(f"- dpe_learnset_blocks_changed: {dpe_learnsets_changed}")
        print(f"- cfru_learnset_blocks_changed: {cfru_learnsets_changed}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
