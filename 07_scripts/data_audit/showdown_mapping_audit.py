#!/usr/bin/env python3
"""Read-only mapping audit for Pokemon Showdown data vs local CFRU/DPE constants.

The script does not download data and does not modify CFRU/DPE tables. Point
`--showdown-data-dir` at an external Pokemon Showdown `data/` checkout when a
full comparison is needed; without it, the script reports local constants,
cross-source drift, and ability aliases.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_ALIAS_FILE = SCRIPT_DIR / "showdown_aliases.json"

LOCAL_HEADERS = {
    "species": [
        REPO_ROOT / "02_external/CFRU-expansion/include/constants/species.h",
        REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h",
    ],
    "moves": [
        REPO_ROOT / "02_external/CFRU-expansion/include/constants/moves.h",
        REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9/include/moves.h",
    ],
    "abilities": [
        REPO_ROOT / "02_external/CFRU-expansion/include/constants/abilities.h",
        REPO_ROOT / "02_external/Dynamic-Pokemon-Expansion-Gen-9/include/abilities.h",
    ],
}

SHOWDOWN_FILES = {
    "species": "pokedex.ts",
    "moves": "moves.ts",
    "abilities": "abilities.ts",
}

PREFIXES = {
    "species": "SPECIES_",
    "moves": "MOVE_",
    "abilities": "ABILITY_",
}

DEFINE_RE = re.compile(
    r"^\s*#define\s+(?P<name>[A-Z][A-Z0-9_]+)\s+(?P<value>0x[0-9A-Fa-f]+|\d+|[A-Z][A-Z0-9_]+)\b"
)
TS_KEY_RE = re.compile(r"^\s*(?P<quote>['\"]?)(?P<key>[A-Za-z0-9_]+)(?P=quote)\s*:\s*\{")


@dataclass(frozen=True)
class Constant:
    source: str
    name: str
    value: str
    normalized: str
    path: str
    line: int
    is_alias: bool


@dataclass(frozen=True)
class AliasEntry:
    kind: str
    category: str
    status: str
    showdown_key: str | None
    showdown_pattern: str | None
    local_keys: tuple[str, ...]
    note: str


@dataclass(frozen=True)
class AliasIndex:
    entries: tuple[AliasEntry, ...]
    by_showdown: dict[str, list[AliasEntry]]
    by_local: dict[str, list[AliasEntry]]
    patterns: tuple[tuple[re.Pattern[str], AliasEntry], ...]


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def load_aliases(path: Path | None) -> AliasIndex:
    if path is None or not path.is_file():
        return AliasIndex((), {}, {}, ())

    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)

    entries: list[AliasEntry] = []
    by_showdown: dict[str, list[AliasEntry]] = defaultdict(list)
    by_local: dict[str, list[AliasEntry]] = defaultdict(list)
    patterns: list[tuple[re.Pattern[str], AliasEntry]] = []

    for raw_entry in raw.get("entries", []):
        showdown_key = raw_entry.get("showdown_key")
        showdown_pattern = raw_entry.get("showdown_pattern")
        entry = AliasEntry(
            kind=raw_entry["kind"],
            category=raw_entry["category"],
            status=raw_entry["status"],
            showdown_key=normalize(showdown_key) if showdown_key else None,
            showdown_pattern=showdown_pattern,
            local_keys=tuple(normalize(key) for key in raw_entry.get("local_keys", [])),
            note=raw_entry.get("note", ""),
        )
        entries.append(entry)
        if entry.showdown_key:
            by_showdown[entry.showdown_key].append(entry)
        for local_key in entry.local_keys:
            by_local[local_key].append(entry)
        if entry.showdown_pattern:
            patterns.append((re.compile(entry.showdown_pattern), entry))

    return AliasIndex(tuple(entries), dict(by_showdown), dict(by_local), tuple(patterns))


def local_name_to_key(kind: str, name: str) -> str:
    prefix = PREFIXES[kind]
    if name.startswith(prefix):
        name = name[len(prefix):]
    return normalize(name)


def parse_constants(kind: str) -> list[Constant]:
    constants: list[Constant] = []
    for path in LOCAL_HEADERS[kind]:
        source = "CFRU" if "CFRU-expansion" in str(path) else "DPE"
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                match = DEFINE_RE.match(line)
                if not match:
                    continue
                name = match.group("name")
                if not name.startswith(PREFIXES[kind]):
                    continue
                value = match.group("value")
                is_alias = value.startswith(PREFIXES[kind])
                constants.append(
                    Constant(
                        source=source,
                        name=name,
                        value=value,
                        normalized=local_name_to_key(kind, name),
                        path=str(path.relative_to(REPO_ROOT)),
                        line=line_no,
                        is_alias=is_alias,
                    )
                )
    return constants


def parse_showdown_keys(data_dir: Path, kind: str) -> set[str]:
    path = data_dir / SHOWDOWN_FILES[kind]
    if not path.is_file():
        raise FileNotFoundError(f"missing Showdown file for {kind}: {path}")

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
                match = TS_KEY_RE.match(line)
                if match:
                    keys.add(normalize(match.group("key")))

            depth += line.count("{") - line.count("}")
            if in_export and depth <= 0:
                break
    return keys


def group_by_name(constants: list[Constant]) -> dict[str, list[Constant]]:
    grouped: dict[str, list[Constant]] = defaultdict(list)
    for constant in constants:
        grouped[constant.normalized].append(constant)
    return grouped


def source_name_set(constants: list[Constant], source: str) -> set[str]:
    return {constant.normalized for constant in constants if constant.source == source}


def value_name_map(constants: list[Constant], source: str) -> dict[str, set[str]]:
    grouped: dict[str, set[str]] = defaultdict(set)
    for constant in constants:
        if constant.source == source:
            grouped[constant.value].add(constant.name)
    return grouped


def print_limited(title: str, values: list[str], limit: int) -> None:
    print(f"\n### {title}")
    print(f"count: {len(values)}")
    for value in values[:limit]:
        print(f"- {value}")
    if len(values) > limit:
        print(f"- ... {len(values) - limit} more")


def print_alias_summary(alias_index: AliasIndex, limit: int) -> None:
    print("\n## reviewed alias table")
    print(f"- entries: {len(alias_index.entries)}")
    if not alias_index.entries:
        return

    grouped: dict[str, int] = defaultdict(int)
    samples: list[str] = []
    for entry in alias_index.entries:
        grouped[f"{entry.kind}/{entry.status}/{entry.category}"] += 1
        source = entry.showdown_key or entry.showdown_pattern or "<no-showdown-key>"
        target = ",".join(entry.local_keys) if entry.local_keys else "<no-local-key>"
        samples.append(f"{entry.kind} {source} -> {target} [{entry.status}/{entry.category}]")

    print_limited("Alias table categories", [f"{key}: {value}" for key, value in sorted(grouped.items())], limit)
    print_limited("Alias table samples", samples, limit)


def matching_aliases(kind: str, key: str, alias_index: AliasIndex, side: str) -> list[AliasEntry]:
    if side == "showdown":
        matches = list(alias_index.by_showdown.get(key, []))
        matches.extend(entry for pattern, entry in alias_index.patterns if pattern.fullmatch(key))
    elif side == "local":
        matches = list(alias_index.by_local.get(key, []))
    else:
        raise ValueError(f"unknown alias side: {side}")
    return [entry for entry in matches if entry.kind == kind]


def report_alias_classification(
    title: str,
    kind: str,
    keys: list[str],
    alias_index: AliasIndex,
    side: str,
    limit: int,
) -> None:
    if not alias_index.entries:
        return

    category_counts: dict[str, int] = defaultdict(int)
    classified: list[str] = []
    unclassified: list[str] = []
    for key in keys:
        aliases = matching_aliases(kind, key, alias_index, side)
        if aliases:
            labels = sorted({f"{entry.status}/{entry.category}" for entry in aliases})
            for label in labels:
                category_counts[label] += 1
            classified.append(f"{key}: {', '.join(labels)}")
        else:
            unclassified.append(key)

    print_limited(f"{title} reviewed classifications", [f"{k}: {v}" for k, v in sorted(category_counts.items())], limit)
    print_limited(f"{title} classified examples", classified, limit)
    print_limited(f"{title} still uncategorized", unclassified, limit)


def report_local(kind: str, constants: list[Constant], limit: int) -> None:
    cfru = [constant for constant in constants if constant.source == "CFRU"]
    dpe = [constant for constant in constants if constant.source == "DPE"]
    aliases = [constant for constant in constants if constant.is_alias]
    print(f"\n## {kind}")
    print(f"- CFRU constants: {len(cfru)}")
    print(f"- DPE constants: {len(dpe)}")
    print(f"- alias constants: {len(aliases)}")

    cfru_names = source_name_set(constants, "CFRU")
    dpe_names = source_name_set(constants, "DPE")
    print_limited("Only in CFRU", sorted(cfru_names - dpe_names), limit)
    print_limited("Only in DPE", sorted(dpe_names - cfru_names), limit)

    cfru_values = value_name_map(constants, "CFRU")
    dpe_values = value_name_map(constants, "DPE")
    renamed_same_value: list[str] = []
    for value in sorted(set(cfru_values) & set(dpe_values)):
        if cfru_values[value] != dpe_values[value]:
            renamed_same_value.append(
                f"{value}: CFRU={','.join(sorted(cfru_values[value]))} DPE={','.join(sorted(dpe_values[value]))}"
            )
    print_limited("Same numeric/alias value with different names", renamed_same_value, limit)

    if kind == "abilities":
        alias_lines = [
            f"{constant.source} {constant.name} -> {constant.value} ({constant.path}:{constant.line})"
            for constant in aliases
        ]
        print_limited("Ability aliases", alias_lines, limit)


def report_showdown(
    kind: str,
    constants: list[Constant],
    showdown_keys: set[str],
    alias_index: AliasIndex,
    limit: int,
) -> None:
    local_keys = set(group_by_name(constants))
    unresolved_showdown = sorted(showdown_keys - local_keys)
    local_without_showdown = sorted(local_keys - showdown_keys)
    print_limited(f"Showdown {kind} keys without local normalized constant", unresolved_showdown, limit)
    report_alias_classification(
        f"Showdown {kind} keys without local normalized constant",
        kind,
        unresolved_showdown,
        alias_index,
        "showdown",
        limit,
    )
    print_limited(f"Local {kind} constants without Showdown normalized key", local_without_showdown, limit)
    report_alias_classification(
        f"Local {kind} constants without Showdown normalized key",
        kind,
        local_without_showdown,
        alias_index,
        "local",
        limit,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--showdown-data-dir",
        type=Path,
        help="External Pokemon Showdown data directory containing pokedex.ts, moves.ts and abilities.ts.",
    )
    parser.add_argument(
        "--alias-file",
        type=Path,
        default=DEFAULT_ALIAS_FILE,
        help="Reviewed alias/ignore table JSON. Defaults to 07_scripts/data_audit/showdown_aliases.json.",
    )
    parser.add_argument("--limit", type=int, default=40, help="Max entries per report section.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    print("# Pokemon Showdown Mapping Audit")
    print("")
    print("mode: read-only")
    print("local repo: current workspace")
    if args.showdown_data_dir:
        print("showdown input: external data directory")
    else:
        print("showdown input: not provided; local-only audit")
    alias_index = load_aliases(args.alias_file)
    if alias_index.entries:
        try:
            alias_label = str(args.alias_file.resolve().relative_to(REPO_ROOT))
        except ValueError:
            alias_label = "external alias file"
    else:
        alias_label = "not loaded"
    print(f"alias input: {alias_label}")
    print_alias_summary(alias_index, args.limit)

    for kind in ("species", "moves", "abilities"):
        constants = parse_constants(kind)
        report_local(kind, constants, args.limit)
        if args.showdown_data_dir:
            report_showdown(kind, constants, parse_showdown_keys(args.showdown_data_dir, kind), alias_index, args.limit)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
