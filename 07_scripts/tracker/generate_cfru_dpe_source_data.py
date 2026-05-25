#!/usr/bin/env python3
"""Generate CFRU/DPE Tracker source-data from source headers only."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFINE_RE = re.compile(r"^\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)\s+(.+?)\s*$")
ENUM_START_RE = re.compile(r"^\s*enum(?:\s+[A-Za-z_][A-Za-z0-9_]*)?(?:\s*\{)?\s*$")
ENUM_BRACE_RE = re.compile(r"^\s*\{\s*$")
ENUM_END_RE = re.compile(r"^\s*\}\s*;")
ENUM_ENTRY_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)(?:\s*=\s*(.+?))?\s*,?\s*$")
IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
INT_RE = re.compile(r"^(?:0[xX][0-9A-Fa-f]+|\d+)$")
ADD_RE = re.compile(r"^(.+?)\s*\+\s*(.+?)$")
SUB_RE = re.compile(r"^(.+?)\s*-\s*(.+?)$")


@dataclass(frozen=True)
class HeaderSpec:
    key: str
    prefix: str
    count_name: str
    dpe_path: Path
    cfru_compare_path: Path | None = None


def strip_comments(line: str) -> str:
    return line.split("//", 1)[0].strip()


def strip_outer_parens(value: str) -> str:
    value = value.strip()
    while value.startswith("(") and value.endswith(")"):
        depth = 0
        wraps = True
        for index, char in enumerate(value):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0 and index != len(value) - 1:
                    wraps = False
                    break
        if not wraps:
            break
        value = value[1:-1].strip()
    return value


def parse_int(value: str) -> int | None:
    value = strip_outer_parens(value)
    if not INT_RE.match(value):
        return None
    return int(value, 0)


def eval_expr(expr: str, symbols: dict[str, int], seen: set[str] | None = None) -> int | None:
    expr = strip_outer_parens(expr.strip())
    if not expr:
        return None

    parsed_int = parse_int(expr)
    if parsed_int is not None:
        return parsed_int

    if seen is None:
        seen = set()

    if IDENT_RE.match(expr):
        if expr in seen:
            return None
        if expr in symbols:
            return symbols[expr]
        return None

    for pattern, op in ((ADD_RE, lambda a, b: a + b), (SUB_RE, lambda a, b: a - b)):
        match = pattern.match(expr)
        if not match:
            continue
        left = eval_expr(match.group(1), symbols, set(seen))
        right = eval_expr(match.group(2), symbols, set(seen))
        if left is None or right is None:
            return None
        return op(left, right)

    return None


def parse_header(path: Path) -> tuple[dict[str, int], dict[str, str], dict[str, int], list[str]]:
    raw_defines: list[tuple[str, str]] = []
    symbols: dict[str, int] = {}
    source_exprs: dict[str, str] = {}
    order: dict[str, int] = {}
    warnings: list[str] = []
    in_enum = False
    pending_enum_brace = False
    next_enum_value: int | None = None
    order_index = 0

    for line_number, original_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = strip_comments(original_line)
        if not line:
            continue

        if pending_enum_brace:
            if ENUM_BRACE_RE.match(line):
                pending_enum_brace = False
                in_enum = True
                next_enum_value = 0
                continue
            pending_enum_brace = False

        if in_enum:
            if ENUM_END_RE.match(line):
                in_enum = False
                next_enum_value = None
                continue
            match = ENUM_ENTRY_RE.match(line)
            if not match:
                continue
            name, expr = match.groups()
            if expr is not None:
                value = eval_expr(expr, symbols)
                if value is None:
                    warnings.append(f"{path}:{line_number}: unresolved enum expression for {name}: {expr}")
                    next_enum_value = None
                    continue
            elif next_enum_value is not None:
                value = next_enum_value
            else:
                value = 0
            symbols[name] = value
            source_exprs[name] = expr.strip() if expr is not None else str(value)
            order[name] = order_index
            order_index += 1
            next_enum_value = value + 1
            continue

        if ENUM_START_RE.match(line):
            if "{" in line:
                in_enum = True
                next_enum_value = 0
            else:
                pending_enum_brace = True
            continue

        match = DEFINE_RE.match(line)
        if not match:
            continue
        name, expr = match.groups()
        expr = expr.strip()
        if "(" in name:
            continue
        raw_defines.append((name, expr))

    pending = list(raw_defines)
    while pending:
        progressed = False
        still_pending: list[tuple[str, str]] = []
        for name, expr in pending:
            value = eval_expr(expr, symbols)
            if value is None:
                still_pending.append((name, expr))
                continue
            symbols[name] = value
            source_exprs[name] = expr
            order[name] = order_index
            order_index += 1
            progressed = True
        if not progressed:
            for name, expr in still_pending:
                source_exprs.setdefault(name, expr)
            break
        pending = still_pending

    return symbols, source_exprs, order, warnings


def normalize_name(constant: str, prefix: str) -> str:
    base = constant
    if base.startswith(prefix):
        base = base[len(prefix) :]
    parts = [part for part in base.split("_") if part]
    normalized = []
    for part in parts:
        if len(part) == 1:
            normalized.append(part)
        elif part.isdigit():
            normalized.append(part)
        else:
            normalized.append(part[:1].upper() + part[1:].lower())
    return " ".join(normalized) if normalized else constant


def build_mapping(
    key: str,
    prefix: str,
    symbols: dict[str, int],
    source_exprs: dict[str, str],
    order: dict[str, int],
    count_value: int | None,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    by_id: dict[int, list[str]] = {}
    for name, value in symbols.items():
        if not name.startswith(prefix):
            continue
        if name.endswith("_NAME_LENGTH"):
            continue
        if count_value is not None and (value < 0 or value >= count_value):
            continue
        by_id.setdefault(value, []).append(name)

    rows: list[dict[str, object]] = []
    alias_groups = 0
    alias_constants = 0
    for value in sorted(by_id):
        constants = sorted(by_id[value], key=lambda name: order.get(name, 10**9))
        canonical = constants[0]
        aliases = [name for name in constants if name != canonical]
        if aliases:
            alias_groups += 1
            alias_constants += len(aliases)
        row: dict[str, object] = {
            "id": value,
            "constant": canonical,
            "name": normalize_name(canonical, prefix),
        }
        if aliases:
            row["aliases"] = aliases
        if canonical in source_exprs:
            row["sourceExpression"] = source_exprs[canonical]
        rows.append(row)

    stats = {
        "mappedValues": len(rows),
        "aliasGroups": alias_groups,
        "aliasConstants": alias_constants,
        "maxMappedId": rows[-1]["id"] if rows else None,
    }
    return rows, stats


def count_details(
    count_name: str,
    symbols: dict[str, int],
    source_exprs: dict[str, str],
    mapping: list[dict[str, object]],
    stats: dict[str, object],
) -> dict[str, object]:
    value = symbols.get(count_name)
    last_constant = None
    last_id = None
    if mapping:
        last_row = mapping[-1]
        last_constant = last_row["constant"]
        last_id = last_row["id"]
    value = symbols.get(count_name)
    source_expression = source_exprs.get(count_name)
    if value is None and last_id is not None:
        value = int(last_id) + 1
        source_expression = "max mapped ID + 1 fallback"
    return {
        "value": value,
        "sourceExpression": source_expression,
        "lastMappedConstant": last_constant,
        "lastMappedId": last_id,
        **stats,
    }


def warning_for_aliases(key: str, mapping: Iterable[dict[str, object]]) -> dict[str, object] | None:
    groups = []
    for row in mapping:
        aliases = row.get("aliases")
        if aliases:
            groups.append(
                {
                    "id": row["id"],
                    "constant": row["constant"],
                    "aliases": aliases,
                }
            )
    if not groups:
        return None
    return {
        "type": "aliases",
        "section": key,
        "message": f"{key} contains duplicate ID aliases; canonical constants are deterministic fallbacks.",
        "count": len(groups),
        "groups": groups,
    }


def generate(source_root: Path) -> dict[str, object]:
    dpe_root = source_root / "02_external" / "Dynamic-Pokemon-Expansion-Gen-9"
    cfru_root = source_root / "02_external" / "CFRU-expansion"
    specs = [
        HeaderSpec("species", "SPECIES_", "NUM_SPECIES", dpe_root / "include" / "species.h"),
        HeaderSpec("moves", "MOVE_", "MOVES_COUNT", dpe_root / "include" / "moves.h"),
        HeaderSpec("abilities", "ABILITY_", "ABILITIES_COUNT", dpe_root / "include" / "abilities.h"),
        HeaderSpec(
            "items",
            "ITEM_",
            "ITEMS_COUNT",
            dpe_root / "include" / "items.h",
            cfru_root / "include" / "constants" / "items.h",
        ),
    ]

    counts: dict[str, object] = {}
    sections: dict[str, list[dict[str, object]]] = {}
    warnings: list[object] = []
    sources: list[str] = []

    for spec in specs:
        if not spec.dpe_path.is_file():
            raise FileNotFoundError(spec.dpe_path)
        symbols, source_exprs, order, parse_warnings = parse_header(spec.dpe_path)
        sources.append(str(spec.dpe_path.relative_to(source_root)))
        warnings.extend({"type": "parse", "section": spec.key, "message": item} for item in parse_warnings)

        count_value = symbols.get(spec.count_name)
        if count_value is None:
            prefixed_values = [
                value
                for name, value in symbols.items()
                if name.startswith(spec.prefix) and not name.endswith("_NAME_LENGTH")
            ]
            count_value = max(prefixed_values) + 1 if prefixed_values else None
        mapping, stats = build_mapping(spec.key, spec.prefix, symbols, source_exprs, order, count_value)
        sections[spec.key] = mapping
        counts[spec.key] = count_details(spec.count_name, symbols, source_exprs, mapping, stats)

        alias_warning = warning_for_aliases(spec.key, mapping)
        if alias_warning is not None:
            warnings.append(alias_warning)

        if spec.cfru_compare_path is not None and spec.cfru_compare_path.is_file():
            compare_symbols, compare_exprs, _compare_order, compare_warnings = parse_header(spec.cfru_compare_path)
            sources.append(str(spec.cfru_compare_path.relative_to(source_root)))
            warnings.extend(
                {"type": "parse", "section": f"{spec.key}-cfru-compare", "message": item}
                for item in compare_warnings
            )
            cfru_count = compare_symbols.get(spec.count_name)
            dpe_count = count_value
            if cfru_count is not None:
                counts[spec.key]["cfruConstantsValue"] = cfru_count
                counts[spec.key]["cfruSourceExpression"] = compare_exprs.get(spec.count_name)
            if dpe_count is not None and cfru_count is not None and dpe_count != cfru_count:
                warnings.append(
                    {
                        "type": "count-conflict",
                        "section": spec.key,
                        "message": "DPE and CFRU item count defines differ; do not infer final Tracker item table size yet.",
                        "dpeValue": dpe_count,
                        "cfruConstantsValue": cfru_count,
                    }
                )

    return {
        "metadata": {
            "schema": "cfru-dpe-tracker-source-data-v1",
            "status": "source-derived",
            "generatedBy": "07_scripts/tracker/generate_cfru_dpe_source_data.py",
            "sourceRoot": ".",
            "sources": sorted(dict.fromkeys(sources)),
            "addressPolicy": "No ROM, build, offsets.ini, runtime, private path or local address data is included.",
            "namePolicy": "Names are normalized fallback display names derived from macro constants.",
        },
        "counts": counts,
        "species": sections["species"],
        "moves": sections["moves"],
        "abilities": sections["abilities"],
        "items": sections["items"],
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate CFRU/DPE Tracker source-data.json from source headers only."
    )
    parser.add_argument(
        "--source-root",
        default=".",
        help="Workspace root containing 02_external/ and 03_tools/. Defaults to the current directory.",
    )
    parser.add_argument(
        "--output",
        default="03_tools/tracker-extensions/CFRUDPEExtension/data/source-data.json",
        help="Output JSON path. Defaults to CFRUDPEExtension/data/source-data.json under --source-root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_root = Path(args.source_root).resolve()
    output = Path(args.output)
    if not output.is_absolute():
        output = source_root / output

    data = generate(source_root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
