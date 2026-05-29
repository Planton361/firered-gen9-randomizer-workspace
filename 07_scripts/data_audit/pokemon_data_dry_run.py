#!/usr/bin/env python3
"""Read-only dry-run gate for Pokemon Showdown-to-CFRU/DPE data updates.

This helper does not download data, write reports, or edit CFRU/DPE tables. It
checks whether the reviewed alias table is safe enough for a future generator
pass and reports per-data-block blockers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import showdown_mapping_audit as mapping


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_ALIAS_FILE = SCRIPT_DIR / "showdown_aliases.json"

SHOWDOWN_REQUIRED_FILES = {
    "pokedex": "pokedex.ts",
    "learnsets": "learnsets.ts",
    "moves": "moves.ts",
    "abilities": "abilities.ts",
}

LOCAL_INPUTS = {
    "base_stats": REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c",
    "dpe_learnsets": REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Learnsets.c",
    "cfru_learnsets": REPO_ROOT / "02_external/CFRU-expansion/src/Tables/level_up_learnsets.c",
    "egg_moves": REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Egg_Moves.c",
    "tm_tutor_tables": REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9/src/TM_Tutor_Tables.c",
    "tm_compatibility_dir": REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9/src/tm_compatibility",
    "tutor_compatibility_dir": REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9/src/tutor_compatibility",
}

DATA_BLOCKS = {
    "Base Stats": {
        "requires": ("species",),
        "inputs": ("Showdown pokedex.ts", "DPE Base_Stats.c", "local species constants", "reviewed alias table"),
        "output": "sanitized per-species base-stat diff plan; no C table writes",
        "risk": "Medium-high: form semantics, typing/stat fields, catch/EXP/held-item fields, and table-wide churn.",
        "first_pr": "Base stats for non-blocked species only, with generated diff summary and DPE rebuild smoke.",
    },
    "Ability Assignments": {
        "requires": ("species", "abilities"),
        "inputs": ("Showdown pokedex.ts", "Showdown abilities.ts", "DPE Base_Stats.c", "local ability constants", "reviewed alias table"),
        "output": "sanitized ability-assignment diff plan; no DPE writes",
        "risk": "High: local Gen9-looking Ability names can alias old CFRU behavior.",
        "first_pr": "Ability assignments only after blocked Ability behavior risks are accepted, fixed, or explicitly excluded.",
    },
    "Level-up Learnsets": {
        "requires": ("species", "moves"),
        "inputs": ("Showdown learnsets.ts", "DPE Learnsets.c", "CFRU level_up_learnsets.c", "local species/move constants", "reviewed alias table"),
        "output": "sanitized learnset diff plan for DPE/CFRU sync; no table writes",
        "risk": "Medium-high: duplicated DPE/CFRU tables and move behavior gaps.",
        "first_pr": "A narrow non-blocked learnset tranche with CFRU/DPE parity check.",
    },
    "Egg Moves": {
        "requires": ("species", "moves"),
        "inputs": ("Showdown learnsets.ts", "DPE Egg_Moves.c", "local species/move constants", "reviewed alias table"),
        "output": "sanitized egg-move diff plan; no DPE writes",
        "risk": "Medium: compact marker format can corrupt adjacent species if generated incorrectly.",
        "first_pr": "Egg moves after species and move blockers are accepted or excluded.",
    },
    "TM Compatibility": {
        "requires": ("species", "moves"),
        "inputs": ("Showdown learnsets.ts", "DPE TM_Tutor_Tables.c", "DPE tm_compatibility/*.txt", "local TM/move order", "reviewed alias table"),
        "output": "sanitized TM compatibility diff plan; no compatibility file writes",
        "risk": "High: TM order/count and generated bitsets are brittle.",
        "first_pr": "TM compatibility only after move IDs and TM order are frozen.",
    },
    "Tutor Compatibility": {
        "requires": ("species", "moves"),
        "inputs": ("Showdown learnsets.ts", "DPE TM_Tutor_Tables.c", "DPE tutor_compatibility/*.txt", "local tutor/move order", "reviewed alias table"),
        "output": "sanitized tutor compatibility diff plan; no compatibility file writes",
        "risk": "High: tutor count/order and reminder/menu bitsets are the most brittle path.",
        "first_pr": "Tutor compatibility last, after TM compatibility and move behavior decisions.",
    },
}

SPECIES_ENTRY_RE = re.compile(r"^\s*\[SPECIES_[A-Z0-9_]+\]\s*=")
LEARNSET_TABLE_RE = re.compile(r"^\s*\[SPECIES_[A-Z0-9_]+\]\s*=\s*s[A-Za-z0-9_]+LevelUpLearnset")
EGG_MOVES_RE = re.compile(r"\begg_moves\(")
MOVE_ARRAY_ITEM_RE = re.compile(r"^\s*MOVE_[A-Z0-9_]+,")


@dataclass(frozen=True)
class KindGate:
    showdown_uncategorized: int
    local_uncategorized: int
    blockers: dict[str, int]
    blocker_samples: tuple[str, ...]

    @property
    def blocked(self) -> bool:
        return self.showdown_uncategorized > 0 or self.local_uncategorized > 0 or bool(self.blockers)


def normalize_kind(raw_kind: str) -> str:
    return "abilities" if raw_kind == "abilities" else raw_kind


def top_level_ts_keys(data_dir: Path, file_name: str) -> set[str]:
    path = data_dir / file_name
    if not path.is_file():
        raise FileNotFoundError(f"missing Showdown input: {file_name}")

    keys: set[str] = set()
    in_export = False
    depth = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not in_export:
                if "export const" in line and "{" in line:
                    in_export = True
                    depth += line.count("{") - line.count("}")
                continue
            if depth == 1:
                match = mapping.TS_KEY_RE.match(line)
                if match:
                    keys.add(mapping.normalize(match.group("key")))
            depth += line.count("{") - line.count("}")
            if in_export and depth <= 0:
                break
    return keys


def alias_raw_entries(alias_file: Path) -> list[dict[str, object]]:
    with alias_file.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return list(data.get("entries", []))


def raw_entry_kind(raw_entry: dict[str, object]) -> str:
    return str(raw_entry.get("kind", ""))


def is_blocking_entry(raw_entry: dict[str, object]) -> bool:
    return (
        raw_entry.get("status") in {"open-risk", "behavior-risk"}
        or raw_entry.get("generator_policy") == "blocked"
    )


def blocking_aliases_by_kind(raw_entries: list[dict[str, object]], limit: int) -> dict[str, tuple[dict[str, int], tuple[str, ...]]]:
    grouped_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    grouped_samples: dict[str, list[str]] = defaultdict(list)

    for raw_entry in raw_entries:
        if not is_blocking_entry(raw_entry):
            continue
        kind = raw_entry_kind(raw_entry)
        label = f"{raw_entry.get('status')}/{raw_entry.get('category')}"
        grouped_counts[kind][label] += 1
        if len(grouped_samples[kind]) < limit:
            key = raw_entry.get("showdown_key") or ",".join(str(k) for k in raw_entry.get("local_keys", []))
            grouped_samples[kind].append(f"{key}: {label}")

    return {
        kind: (dict(counts), tuple(grouped_samples.get(kind, ())))
        for kind, counts in grouped_counts.items()
    }


def uncategorized_counts(kind: str, showdown_keys: set[str], alias_index: mapping.AliasIndex) -> tuple[int, int]:
    constants = mapping.parse_constants(kind)
    local_keys = set(mapping.group_by_name(constants))
    showdown_missing = sorted(showdown_keys - local_keys)
    local_missing = sorted(local_keys - showdown_keys)

    showdown_uncategorized = sum(
        1 for key in showdown_missing if not mapping.matching_aliases(kind, key, alias_index, "showdown")
    )
    local_uncategorized = sum(
        1 for key in local_missing if not mapping.matching_aliases(kind, key, alias_index, "local")
    )
    return showdown_uncategorized, local_uncategorized


def build_kind_gates(data_dir: Path, alias_file: Path, limit: int) -> dict[str, KindGate]:
    alias_index = mapping.load_aliases(alias_file)
    raw_entries = alias_raw_entries(alias_file)
    blockers = blocking_aliases_by_kind(raw_entries, limit)

    kind_to_file = {
        "species": SHOWDOWN_REQUIRED_FILES["pokedex"],
        "moves": SHOWDOWN_REQUIRED_FILES["moves"],
        "abilities": SHOWDOWN_REQUIRED_FILES["abilities"],
    }
    gates: dict[str, KindGate] = {}
    for kind, file_name in kind_to_file.items():
        showdown_keys = top_level_ts_keys(data_dir, file_name)
        showdown_uncategorized, local_uncategorized = uncategorized_counts(kind, showdown_keys, alias_index)
        counts, samples = blockers.get(kind, ({}, ()))
        gates[kind] = KindGate(
            showdown_uncategorized=showdown_uncategorized,
            local_uncategorized=local_uncategorized,
            blockers=counts,
            blocker_samples=samples,
        )
    return gates


def count_lines(path: Path, regex: re.Pattern[str]) -> int:
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if regex.search(line):
                count += 1
    return count


def count_txt_files(path: Path) -> int:
    return sum(1 for child in path.glob("*.txt") if child.is_file())


def collect_input_counts(data_dir: Path) -> dict[str, int]:
    return {
        "showdown_pokedex_keys": len(top_level_ts_keys(data_dir, SHOWDOWN_REQUIRED_FILES["pokedex"])),
        "showdown_learnsets_keys": len(top_level_ts_keys(data_dir, SHOWDOWN_REQUIRED_FILES["learnsets"])),
        "showdown_moves_keys": len(top_level_ts_keys(data_dir, SHOWDOWN_REQUIRED_FILES["moves"])),
        "showdown_abilities_keys": len(top_level_ts_keys(data_dir, SHOWDOWN_REQUIRED_FILES["abilities"])),
        "dpe_base_stats_entries": count_lines(LOCAL_INPUTS["base_stats"], SPECIES_ENTRY_RE),
        "dpe_levelup_table_entries": count_lines(LOCAL_INPUTS["dpe_learnsets"], LEARNSET_TABLE_RE),
        "cfru_levelup_table_entries": count_lines(LOCAL_INPUTS["cfru_learnsets"], LEARNSET_TABLE_RE),
        "dpe_egg_move_species_blocks": count_lines(LOCAL_INPUTS["egg_moves"], EGG_MOVES_RE),
        "dpe_tm_tutor_move_array_items": count_lines(LOCAL_INPUTS["tm_tutor_tables"], MOVE_ARRAY_ITEM_RE),
        "dpe_tm_compatibility_files": count_txt_files(LOCAL_INPUTS["tm_compatibility_dir"]),
        "dpe_tutor_compatibility_files": count_txt_files(LOCAL_INPUTS["tutor_compatibility_dir"]),
    }


def block_status(required_kinds: tuple[str, ...], gates: dict[str, KindGate]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    for kind in required_kinds:
        gate = gates[kind]
        if gate.showdown_uncategorized:
            reasons.append(f"{kind} showdown uncategorized={gate.showdown_uncategorized}")
        if gate.local_uncategorized:
            reasons.append(f"{kind} local uncategorized={gate.local_uncategorized}")
        for label, count in sorted(gate.blockers.items()):
            reasons.append(f"{kind} {label}={count}")
    return ("BLOCKED" if reasons else "READY_FOR_DRY_DIFF"), reasons


def print_counts(title: str, values: dict[str, int]) -> None:
    print(f"\n## {title}")
    for key in sorted(values):
        print(f"- {key}: {values[key]}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--showdown-data-dir",
        type=Path,
        required=True,
        help="External Pokemon Showdown data directory containing pokedex.ts, learnsets.ts, moves.ts, and abilities.ts.",
    )
    parser.add_argument(
        "--alias-file",
        type=Path,
        default=DEFAULT_ALIAS_FILE,
        help="Reviewed alias/ignore table JSON. Defaults to 07_scripts/data_audit/showdown_aliases.json.",
    )
    parser.add_argument("--limit", type=int, default=20, help="Max blocker samples per kind.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    print("# Pokemon Data Generator Dry Run")
    print("")
    print("mode: read-only")
    print("showdown input: external data directory")
    print("writes: none")

    for file_name in SHOWDOWN_REQUIRED_FILES.values():
        if not (args.showdown_data_dir / file_name).is_file():
            raise FileNotFoundError(f"missing Showdown input: {file_name}")
    if not args.alias_file.is_file():
        raise FileNotFoundError(f"missing alias file: {args.alias_file}")

    raw_entries = alias_raw_entries(args.alias_file)
    print(f"alias entries: {len(raw_entries)}")

    print_counts("Input counts", collect_input_counts(args.showdown_data_dir))
    gates = build_kind_gates(args.showdown_data_dir, args.alias_file, args.limit)

    print("\n## Mapping gate")
    for kind in ("species", "moves", "abilities"):
        gate = gates[kind]
        print(f"- {kind}: showdown_uncategorized={gate.showdown_uncategorized}, local_uncategorized={gate.local_uncategorized}")
        if gate.blockers:
            labels = ", ".join(f"{label}={count}" for label, count in sorted(gate.blockers.items()))
            print(f"  blockers: {labels}")
        else:
            print("  blockers: none")
        for sample in gate.blocker_samples:
            print(f"  sample: {sample}")

    print("\n## Data blocks")
    any_blocked = False
    for name, block in DATA_BLOCKS.items():
        status, reasons = block_status(block["requires"], gates)
        any_blocked = any_blocked or status == "BLOCKED"
        print(f"\n### {name}")
        print(f"- status: {status}")
        print(f"- required inputs: {', '.join(block['inputs'])}")
        print(f"- expected output: {block['output']}")
        print(f"- risk: {block['risk']}")
        print(f"- first implementation PR: {block['first_pr']}")
        if reasons:
            print("- blocking categories:")
            for reason in reasons:
                print(f"  - {reason}")
        else:
            print("- blocking categories: none")

    print("\n## Result")
    if any_blocked:
        print("- dry_run_result: BLOCKED_BY_REVIEWED_POLICY")
        print("- interpretation: fail-closed gate works; no data-table generator should write output yet.")
    else:
        print("- dry_run_result: READY_FOR_SANITIZED_DIFF_GENERATION")
        print("- interpretation: no policy blockers were found for the configured blocks.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
