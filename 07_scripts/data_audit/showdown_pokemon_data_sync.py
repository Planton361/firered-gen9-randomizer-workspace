#!/usr/bin/env python3
"""Fail-closed Pokemon Showdown -> local CFRU/DPE data sync helper.

The pinned closure planner audits all generations together before any write.
Shared tables, incomplete forms and behavior-risk aliases fail closed.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
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
LEARNSET_DECL_RE = re.compile(r"static const struct LevelUpMove (s[A-Za-z0-9_]+)\[\] = \{")
POINTER_RE = re.compile(r"\[(SPECIES_[A-Z0-9_]+|[0-9]+)\]\s*=\s*(s[A-Za-z0-9_]+)")


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


def coherent_level_moves(move_sources: dict[str, list[str]]) -> tuple[int | None, list[tuple[int, str]]]:
    """Choose one generation for the entire literal dataset, never per move."""
    selected: list[tuple[int, int, str]] = []
    parsed = []
    for order, (move_key, sources) in enumerate(move_sources.items()):
        for source in sources:
            match = re.fullmatch(r"(\d+)L(\d+)", source)
            if match:
                if not 1 <= int(match.group(1)) <= 9:
                    raise ValueError("Level-up source outside Gen1-9: " + source)
                parsed.append((int(match.group(1)), int(match.group(2)), order, move_key))
            elif re.match(r"\d+L", source):
                raise ValueError("Unparsed level-up source: " + source)
    generation = max((row[0] for row in parsed), default=None)
    selected = list({(level, order, move) for gen, level, order, move in parsed if gen == generation})
    selected.sort(key=lambda item: (item[0], item[1], item[2]))
    return generation, [(level, move_key) for level, _, move_key in selected]


def latest_level_moves(move_sources: dict[str, list[str]]) -> tuple[list[tuple[int, str]], list[str]]:
    # Retain the legacy call shape, not its superseded per-move union semantics.
    return coherent_level_moves(move_sources)[1], []


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
        if entry.get("showdown_pattern"):
            by_showdown[f"{entry.get('kind')}:*"].append(entry)
        for local_key in entry.get("local_keys", []):
            by_local[f"{entry.get('kind')}:{norm(str(local_key))}"].append(entry)
    return by_showdown, by_local


def matching_entries(kind, key, index):
    entries = list(index.get(f"{kind}:{key}", []))
    entries.extend(entry for entry in index.get(f"{kind}:*", [])
                   if re.fullmatch(str(entry["showdown_pattern"]), key))
    return entries


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
    entries = matching_entries("species", key, by_showdown)
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
    entries = matching_entries("abilities", ability_key, by_showdown)
    if any(ignored_entry(entry) for entry in entries):
        return None, "ability-ignored"
    if any(blocked_entry(entry) for entry in entries):
        return None, "ability-blocked-alias"
    if ability_key in dpe_abilities:
        return dpe_abilities[ability_key], None
    candidates = set()
    for entry in entries:
        if entry.get("status") == "alias":
            for local_key in entry.get("local_keys", []):
                normalized = norm(str(local_key))
                if normalized in dpe_abilities:
                    candidates.add(dpe_abilities[normalized])
    if len(candidates) == 1:
        return candidates.pop(), None
    if candidates:
        return None, "ability-ambiguous"
    return None, "ability-unmapped"


def resolve_move(
    move_key: str,
    dpe_moves: dict[str, str],
    cfru_moves: dict[str, str],
    by_showdown: dict[str, list[dict[str, object]]],
) -> tuple[tuple[str, str] | None, str | None]:
    entries = matching_entries("moves", move_key, by_showdown)
    if any(blocked_entry(entry) for entry in entries):
        return None, "move-open-risk"
    if any(ignored_entry(entry) for entry in entries):
        return None, "move-ignore"
    if move_key in dpe_moves and move_key in cfru_moves:
        return (dpe_moves[move_key], cfru_moves[move_key]), None
    candidates = set()
    for entry in entries:
        if entry.get("status") != "alias":
            continue
        for local_key in entry.get("local_keys", []):
            normalized = norm(str(local_key))
            if normalized in dpe_moves and normalized in cfru_moves:
                candidates.add((dpe_moves[normalized], cfru_moves[normalized]))
    if len(candidates) == 1:
        return candidates.pop(), None
    if candidates:
        return None, "move-ambiguous"
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
            if blocker:
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
    # Retain line positions while ignoring commented-out declarations/pointers.
    source = re.sub(r"/\*.*?\*/|//[^\n]*", lambda m: "\n" * m[0].count("\n"),
                    "".join(lines), flags=re.S)
    pointers: dict[str, str] = {}
    blocks: dict[str, tuple[int, int]] = {}
    current_name: str | None = None
    start = 0
    for idx, line in enumerate(source.splitlines(keepends=True)):
        pointer = POINTER_RE.search(line)
        if pointer:
            key = norm(pointer.group(1).removeprefix("SPECIES_"))
            if key in pointers:
                raise ValueError("Duplicate learnset pointer: " + key)
            pointers[key] = pointer.group(2)
        decl = LEARNSET_DECL_RE.match(line)
        if decl:
            if current_name is not None or decl.group(1) in blocks:
                raise ValueError("Overlapping/duplicate learnset: " + decl.group(1))
            current_name = decl.group(1)
            start = idx
        if current_name is not None and "};" in line:
            blocks[current_name] = (start, idx + 1)
            current_name = None
    if current_name is not None:
        raise ValueError("Unterminated learnset: " + current_name)
    if set(pointers.values()) - blocks.keys():
        raise ValueError("Unparsed active learnsets: " + str(sorted(set(pointers.values()) - blocks.keys())))
    return pointers, blocks, lines


def format_learnset_block(name: str, moves: list[tuple[int, str]], cfru: bool) -> list[str]:
    end = "\tLEVEL_UP_END,\n" if cfru else "\tLEVEL_UP_END\n"
    lines = [f"static const struct LevelUpMove {name}[] = {{\n"]
    for level, move in moves:
        lines.append(f"\tLEVEL_UP_MOVE({level:2d}, {move}),\n")
    lines.append(end)
    lines.append("};\n")
    return lines


def update_learnsets_file(path: Path, updates: dict[str, list[tuple[int, str]]], cfru: bool,
                         *, approved_tables: set[str] | None = None) -> int:
    if approved_tables is None:
        raise ValueError("A full pinned shared-table audit is required before writing")
    pointers, blocks, lines = parse_learnset_blocks(path)
    changed = 0
    replacements: list[tuple[int, int, list[str]]] = []
    grouped = {}
    for local_key, moves in updates.items():
        name = pointers.get(norm(local_key.removeprefix("SPECIES_")))
        if name not in blocks or name not in approved_tables:
            raise ValueError("Unapproved or missing target: " + local_key)
        expected = tuple(moves)
        if not expected:
            raise ValueError("Refusing empty learnset: " + name)
        levels = [level for level, _ in expected]
        if (len(expected) > 50 or levels != sorted(levels) or levels[0] > 1
                or any(not 0 <= level <= 100 for level in levels)
                or any(move == "MOVE_NONE" or not re.fullmatch(r"MOVE_[A-Z0-9_]+", move) for _, move in expected)):
            raise ValueError("Invalid bounds or low-level move path: " + name)
        if name in grouped and grouped[name] != expected:
            raise ValueError("Conflicting shared table: " + name)
        grouped[name] = expected
    for name, moves in grouped.items():
        start, end = blocks[name]
        new_block = format_learnset_block(name, moves, cfru)
        # Preserve the original terminator/closing-line suffix, including the
        # legacy inline END}; form. Only move rows are approved for replacement.
        original = "".join(lines[start:end])
        terminator = re.search(r"(?m)^[\t ]*LEVEL_UP_END\b[\s\S]*", original)
        if terminator is None:
            raise ValueError("Missing standalone terminator: " + name)
        new_block = new_block[:-2] + [terminator.group()]
        if original != "".join(new_block):
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
    from showdown_pinned_closure import main as pinned_main
    return pinned_main()


if __name__ == "__main__":
    raise SystemExit(main())
