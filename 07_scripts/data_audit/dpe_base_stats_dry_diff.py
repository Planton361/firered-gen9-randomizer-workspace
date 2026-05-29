#!/usr/bin/env python3
"""Read-only dry diff for DPE Base_Stats.c against Pokemon Showdown pokedex.ts.

The helper writes nothing and emits only a compact sanitized summary. It uses
the reviewed alias table to fail closed on Species open-risk entries and keeps
Ability assignment differences separate from non-Ability base-stat candidates.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import showdown_mapping_audit as mapping


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_ALIAS_FILE = SCRIPT_DIR / "showdown_aliases.json"
DEFAULT_DPE_BASE_STATS = REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c"

SPECIES_BLOCK_RE = re.compile(r"^\s*\[(SPECIES_[A-Z0-9_]+)\]\s*=")
FIELD_RE = re.compile(r"^\s*\.(?P<field>[A-Za-z0-9_]+)\s*=\s*(?P<value>[^,]+),")
TS_KEY_RE = mapping.TS_KEY_RE

STAT_FIELDS = {
    "hp": "baseHP",
    "atk": "baseAttack",
    "def": "baseDefense",
    "spa": "baseSpAttack",
    "spd": "baseSpDefense",
    "spe": "baseSpeed",
}

TYPE_MAP = {
    "normal": "TYPE_NORMAL",
    "fighting": "TYPE_FIGHTING",
    "flying": "TYPE_FLYING",
    "poison": "TYPE_POISON",
    "ground": "TYPE_GROUND",
    "rock": "TYPE_ROCK",
    "bug": "TYPE_BUG",
    "ghost": "TYPE_GHOST",
    "steel": "TYPE_STEEL",
    "fire": "TYPE_FIRE",
    "water": "TYPE_WATER",
    "grass": "TYPE_GRASS",
    "electric": "TYPE_ELECTRIC",
    "psychic": "TYPE_PSYCHIC",
    "ice": "TYPE_ICE",
    "dragon": "TYPE_DRAGON",
    "dark": "TYPE_DARK",
    "fairy": "TYPE_FAIRY",
    "stellar": "TYPE_STELLAR",
}

EGG_GROUP_MAP = {
    "monster": "EGG_GROUP_MONSTER",
    "water1": "EGG_GROUP_WATER_1",
    "water2": "EGG_GROUP_WATER_2",
    "water3": "EGG_GROUP_WATER_3",
    "bug": "EGG_GROUP_BUG",
    "flying": "EGG_GROUP_FLYING",
    "field": "EGG_GROUP_FIELD",
    "fairy": "EGG_GROUP_FAIRY",
    "humanlike": "EGG_GROUP_HUMAN_LIKE",
    "mineral": "EGG_GROUP_MINERAL",
    "amorphous": "EGG_GROUP_AMORPHOUS",
    "ditto": "EGG_GROUP_DITTO",
    "dragon": "EGG_GROUP_DRAGON",
    "undiscovered": "EGG_GROUP_UNDISCOVERED",
    "none": "EGG_GROUP_NONE",
}

SHOWDOWN_ONLY_FIELDS = (
    "catchRate",
    "expYield",
    "evYield",
    "growthRate",
)


@dataclass(frozen=True)
class SpeciesRef:
    key: str
    local_key: str
    name: str
    fields: dict[str, object]
    ability_keys: tuple[str, ...]


@dataclass(frozen=True)
class DiffExample:
    species: str
    local_key: str
    fields: tuple[str, ...]
    detail: str


def norm(value: str) -> str:
    return mapping.normalize(value)


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] in "'\"" and value[-1] == value[0]:
        return value[1:-1]
    return value


def parse_ts_blocks(path: Path) -> dict[str, str]:
    blocks: dict[str, str] = {}
    in_export = False
    depth = 0
    current_key: str | None = None
    current_lines: list[str] = []
    current_depth = 0

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not in_export:
                if "export const" in line and "{" in line:
                    in_export = True
                    depth += line.count("{") - line.count("}")
                continue

            if current_key is None and depth == 1:
                match = TS_KEY_RE.match(line)
                if match:
                    current_key = norm(match.group("key"))
                    current_lines = [line]
                    current_depth = line.count("{") - line.count("}")
                    depth += line.count("{") - line.count("}")
                    if current_depth <= 0:
                        blocks[current_key] = "".join(current_lines)
                        current_key = None
                    continue

            if current_key is not None:
                current_lines.append(line)
                current_depth += line.count("{") - line.count("}")
                depth += line.count("{") - line.count("}")
                if current_depth <= 0:
                    blocks[current_key] = "".join(current_lines)
                    current_key = None
                continue

            depth += line.count("{") - line.count("}")
            if in_export and depth <= 0:
                break

    return blocks


def parse_showdown_pokedex(path: Path) -> dict[str, dict[str, object]]:
    parsed: dict[str, dict[str, object]] = {}
    for key, block in parse_ts_blocks(path).items():
        fields: dict[str, object] = {}

        name_match = re.search(r'\bname:\s*"([^"]+)"', block)
        fields["name"] = name_match.group(1) if name_match else key

        stats_match = re.search(
            r"baseStats:\s*\{\s*hp:\s*(\d+),\s*atk:\s*(\d+),\s*def:\s*(\d+),\s*spa:\s*(\d+),\s*spd:\s*(\d+),\s*spe:\s*(\d+)\s*\}",
            block,
        )
        if stats_match:
            fields["baseStats"] = {
                stat: int(value)
                for stat, value in zip(("hp", "atk", "def", "spa", "spd", "spe"), stats_match.groups(), strict=True)
            }

        types_match = re.search(r"types:\s*\[([^\]]+)\]", block)
        if types_match:
            types = [strip_quotes(part.strip()) for part in types_match.group(1).split(",")]
            fields["types"] = tuple(TYPE_MAP.get(norm(type_name), f"TYPE_{norm(type_name).upper()}") for type_name in types)

        gender_match = re.search(r"gender:\s*\"([MFN])\"", block)
        ratio_match = re.search(r"genderRatio:\s*\{\s*M:\s*([0-9.]+),\s*F:\s*([0-9.]+)\s*\}", block)
        if gender_match:
            fields["genderRatio"] = {"M": "MON_MALE", "F": "MON_FEMALE", "N": "MON_GENDERLESS"}[gender_match.group(1)]
        elif ratio_match:
            female_percent = float(ratio_match.group(2)) * 100
            if female_percent.is_integer():
                fields["genderRatio"] = f"PERCENT_FEMALE({int(female_percent)})"
            else:
                fields["genderRatio"] = f"PERCENT_FEMALE({female_percent:g})"

        egg_match = re.search(r"eggGroups:\s*\[([^\]]+)\]", block)
        if egg_match:
            groups = [strip_quotes(part.strip()) for part in egg_match.group(1).split(",")]
            if len(groups) == 1:
                groups.append(groups[0])
            fields["eggGroups"] = tuple(EGG_GROUP_MAP.get(norm(group), f"EGG_GROUP_{norm(group).upper()}") for group in groups[:2])

        abilities_match = re.search(r"abilities:\s*\{([^}]+)\}", block)
        ability_values: dict[str, str] = {}
        ability_keys: list[str] = []
        if abilities_match:
            for label, ability in re.findall(r"([0-9H]):\s*\"([^\"]+)\"", abilities_match.group(1)):
                normalized = norm(ability)
                ability_values[label] = normalized
                ability_keys.append(normalized)
            fields["abilities"] = ability_values
        fields["abilityKeys"] = tuple(ability_keys)
        parsed[key] = fields
    return parsed


def parse_dpe_base_stats(path: Path) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    current_key: str | None = None
    current_fields: dict[str, str] = {}

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            match = SPECIES_BLOCK_RE.match(line)
            if match:
                if current_key is not None:
                    entries[current_key] = current_fields
                current_key = norm(match.group(1).removeprefix("SPECIES_"))
                current_fields = {}
                continue
            if current_key is None:
                continue
            if line.strip() == "},":
                entries[current_key] = current_fields
                current_key = None
                current_fields = {}
                continue
            field_match = FIELD_RE.match(line)
            if field_match:
                current_fields[field_match.group("field")] = field_match.group("value").strip()

    return entries


def alias_raw_entries(alias_file: Path) -> list[dict[str, object]]:
    with alias_file.open("r", encoding="utf-8") as handle:
        return list(json.load(handle).get("entries", []))


def alias_maps(alias_file: Path) -> tuple[dict[str, str], set[str], set[str], set[str]]:
    raw_entries = alias_raw_entries(alias_file)
    showdown_to_local: dict[str, str] = {}
    species_open_risk: set[str] = set()
    species_ignored: set[str] = set()
    ability_blockers: set[str] = set()

    for entry in raw_entries:
        kind = entry.get("kind")
        status = entry.get("status")
        category = entry.get("category")
        blocked = status in {"open-risk", "behavior-risk"} or entry.get("generator_policy") == "blocked"

        if kind == "species":
            showdown_key = entry.get("showdown_key")
            local_keys = [norm(str(key)) for key in entry.get("local_keys", [])]
            if blocked:
                if showdown_key:
                    species_open_risk.add(norm(str(showdown_key)))
                species_open_risk.update(local_keys)
            elif status == "ignore":
                if showdown_key:
                    species_ignored.add(norm(str(showdown_key)))
                species_ignored.update(local_keys)
            elif status == "alias" and showdown_key and local_keys:
                showdown_to_local[norm(str(showdown_key))] = local_keys[0]
        elif kind == "abilities" and blocked:
            if entry.get("showdown_key"):
                ability_blockers.add(norm(str(entry["showdown_key"])))
            ability_blockers.update(norm(str(key)) for key in entry.get("local_keys", []))

    return showdown_to_local, species_open_risk, species_ignored, ability_blockers


def local_constant_key(value: str, prefix: str) -> str:
    value = value.strip()
    if value.startswith(prefix):
        value = value[len(prefix):]
    return norm(value)


def compare_species(ref: SpeciesRef, local: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
    non_ability_fields: list[str] = []
    ability_fields: list[str] = []
    details: list[str] = []

    base_stats = ref.fields.get("baseStats")
    if isinstance(base_stats, dict):
        for show_field, local_field in STAT_FIELDS.items():
            expected = base_stats[show_field]
            actual = local.get(local_field)
            if actual is not None and str(expected) != actual:
                non_ability_fields.append(local_field)
                details.append(f"{local_field}: DPE {actual} vs ref {expected}")

    types = ref.fields.get("types")
    if isinstance(types, tuple) and types:
        expected_type1 = types[0]
        expected_type2 = types[1] if len(types) > 1 else types[0]
        for field, expected in (("type1", expected_type1), ("type2", expected_type2)):
            actual = local.get(field)
            if actual is not None and actual != expected:
                non_ability_fields.append(field)
                details.append(f"{field}: DPE {actual} vs ref {expected}")

    gender = ref.fields.get("genderRatio")
    if isinstance(gender, str):
        actual = local.get("genderRatio")
        if actual is not None and actual != gender:
            non_ability_fields.append("genderRatio")
            details.append(f"genderRatio: DPE {actual} vs ref {gender}")

    egg_groups = ref.fields.get("eggGroups")
    if isinstance(egg_groups, tuple) and len(egg_groups) >= 2:
        for field, expected in (("eggGroup1", egg_groups[0]), ("eggGroup2", egg_groups[1])):
            actual = local.get(field)
            if actual is not None and actual != expected:
                non_ability_fields.append(field)
                details.append(f"{field}: DPE {actual} vs ref {expected}")

    abilities = ref.fields.get("abilities")
    if isinstance(abilities, dict):
        expected = {
            "ability1": abilities.get("0"),
            "ability2": abilities.get("1", abilities.get("0")),
            "hiddenAbility": abilities.get("H"),
        }
        for field, expected_key in expected.items():
            if not expected_key:
                continue
            actual = local.get(field)
            if actual is not None and local_constant_key(actual, "ABILITY_") != expected_key:
                ability_fields.append(field)

    return non_ability_fields, ability_fields, details


def build_refs(showdown_data_dir: Path, alias_file: Path) -> tuple[dict[str, SpeciesRef], int, int]:
    showdown_to_local, species_open_risk, species_ignored, _ = alias_maps(alias_file)
    pokedex = parse_showdown_pokedex(showdown_data_dir / "pokedex.ts")
    refs: dict[str, SpeciesRef] = {}
    skipped_open_risk = 0
    skipped_ignored = 0

    for showdown_key, fields in pokedex.items():
        local_key = showdown_to_local.get(showdown_key, showdown_key)
        if showdown_key in species_open_risk or local_key in species_open_risk:
            skipped_open_risk += 1
            continue
        if showdown_key in species_ignored or local_key in species_ignored:
            skipped_ignored += 1
            continue
        if local_key == showdown_key or showdown_key in showdown_to_local:
            refs[showdown_key] = SpeciesRef(
                key=showdown_key,
                local_key=local_key,
                name=str(fields.get("name", showdown_key)),
                fields=fields,
                ability_keys=tuple(fields.get("abilityKeys", ())),
            )

    return refs, skipped_open_risk, skipped_ignored


def run_dry_diff(showdown_data_dir: Path, alias_file: Path, limit: int) -> dict[str, object]:
    if not (showdown_data_dir / "pokedex.ts").is_file():
        raise FileNotFoundError("missing Showdown pokedex.ts")

    _, _, _, ability_blockers = alias_maps(alias_file)
    refs, skipped_open_risk, skipped_ignored = build_refs(showdown_data_dir, alias_file)
    local_entries = parse_dpe_base_stats(DEFAULT_DPE_BASE_STATS)

    tested = 0
    missing_local = 0
    skipped_ability = 0
    safe_candidate_total = 0
    safe_candidates: list[str] = []
    examples: list[DiffExample] = []
    non_ability_field_counts: Counter[str] = Counter()
    ability_field_counts: Counter[str] = Counter()
    unavailable_counts = {field: len(refs) for field in SHOWDOWN_ONLY_FIELDS}

    for ref in refs.values():
        local = local_entries.get(ref.local_key)
        if local is None:
            missing_local += 1
            continue
        tested += 1

        ability_blocked = any(ability in ability_blockers for ability in ref.ability_keys)
        if ability_blocked:
            skipped_ability += 1

        non_ability_fields, ability_fields, details = compare_species(ref, local)
        non_ability_field_counts.update(non_ability_fields)
        ability_field_counts.update(ability_fields)

        if non_ability_fields and not ability_blocked:
            safe_candidate_total += 1
            if len(safe_candidates) < 25:
                safe_candidates.append(f"{ref.name} ({ref.local_key})")
            if len(examples) < limit:
                examples.append(
                    DiffExample(
                        species=ref.name,
                        local_key=ref.local_key,
                        fields=tuple(non_ability_fields),
                        detail="; ".join(details[:4]),
                    )
                )

    return {
        "tested": tested,
        "skipped_open_risk": skipped_open_risk,
        "skipped_ignored": skipped_ignored,
        "skipped_ability": skipped_ability,
        "missing_local": missing_local,
        "safe_candidate_total": safe_candidate_total,
        "safe_candidates": safe_candidates,
        "examples": examples,
        "non_ability_field_counts": non_ability_field_counts,
        "ability_field_counts": ability_field_counts,
        "unavailable_counts": unavailable_counts,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--showdown-data-dir", type=Path, required=True)
    parser.add_argument("--alias-file", type=Path, default=DEFAULT_ALIAS_FILE)
    parser.add_argument("--limit", type=int, default=10)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = run_dry_diff(args.showdown_data_dir, args.alias_file, args.limit)

    print("# DPE Base Stats Safe Dry Diff")
    print("")
    print("mode: read-only")
    print("reference: external Pokemon Showdown pokedex.ts")
    print("writes: none")
    print("")
    print("## Summary")
    print(f"- tested_species: {result['tested']}")
    print(f"- skipped_species_open_risk: {result['skipped_open_risk']}")
    print(f"- skipped_species_reviewed_ignore: {result['skipped_ignored']}")
    print(f"- skipped_ability_blocker: {result['skipped_ability']}")
    print(f"- missing_local_entries_after_alias: {result['missing_local']}")
    print(f"- safe_candidate_species_with_non_ability_diffs: {result['safe_candidate_total']}")

    print("\n## Frequent non-Ability field differences")
    for field, count in result["non_ability_field_counts"].most_common(12):
        print(f"- {field}: {count}")
    if not result["non_ability_field_counts"]:
        print("- none")

    print("\n## Ability assignment differences")
    for field, count in result["ability_field_counts"].most_common(8):
        print(f"- {field}: {count}")
    if not result["ability_field_counts"]:
        print("- none")
    print("- interpretation: Ability differences are analysis-only and not update candidates while Ability blockers remain.")

    print("\n## Reference fields unavailable from Showdown pokedex.ts")
    for field, count in result["unavailable_counts"].items():
        print(f"- {field}: unavailable for {count} mapped non-open-risk refs")

    print("\n## Safe candidate sample")
    for item in result["safe_candidates"][:10]:
        print(f"- {item}")
    if not result["safe_candidates"]:
        print("- none")

    print("\n## Example diffs")
    for example in result["examples"]:
        print(f"- {example.species} ({example.local_key}): {', '.join(example.fields)} | {example.detail}")
    if not result["examples"]:
        print("- none")

    print("\n## Result")
    print("- dry_diff_result: PASS_READ_ONLY_WITH_BLOCKERS")
    print("- write_recommendation: no writes; review sanitized diff candidates first")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
