#!/usr/bin/env python3
"""Sanitized local coverage auditor for UPR-FVX CFRU/DPE randomizer runs.

The tool can build expected Pokemon/item/TM-HM indexes from local source
constants, parse local randomizer logs, run local batches for Anton, and compare
expected vs observed summaries. Codex must not run batch mode with ROMs.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUTPUT_DIR = Path(".local/randomizer-coverage")
LOG_SUFFIXES = {".log", ".txt"}

SPECIES_FIELDS = [
    "canonical_key", "source_constant", "display_name_guess", "dex_number_or_source_id",
    "form_family", "generation_guess", "expected_source", "observed_count_total",
    "observed_sections", "observed_runs_seen", "coverage_status", "reason", "confidence",
]
ITEM_FIELDS = [
    "canonical_key", "source_constant", "display_name_guess", "item_id_or_source_id",
    "item_family", "item_category_guess", "is_tm", "is_hm", "expected_source",
    "observed_count_total", "observed_sections", "observed_runs_seen", "coverage_status",
    "reason", "confidence",
]
OBSERVED_FIELDS = [
    "canonical_key", "display_name", "observed_count_total", "observed_sections",
    "observed_runs_seen", "source_logs_seen", "confidence",
]

DEFINE_RE = re.compile(
    r"^\s*#define\s+(?P<constant>[A-Z][A-Z0-9_]+)\s+(?P<value>0x[0-9A-Fa-f]+|\d+)\b"
)
SECTION_RE = re.compile(r"^\(\s*(?P<title>.+?)\s+\{[A-Z0-9]+}\s*\)\s*$")
STARTER_RE = re.compile(r"^Set starter\s+\d+\s+to\s+(?P<species>.+?)(?:,\s+holding\s+(?P<item>.+))?$")
WILD_RE = re.compile(r"^(?P<species>.+?)\s+Lv(?:s)?\d+(?:-\d+)?$")
TRAINER_SPECIES_RE = re.compile(r"(?P<species>.+?)(?:@(?P<item>.+?))?\s+Lv\d+\b")
STATIC_RE = re.compile(r"=>\s*(?P<species>.+)$")
TM_HM_RE = re.compile(r"\b(?P<label>(?:TM|HM)\d{1,3})(?:[_ -][A-Za-z][A-Za-z0-9' .-]*)?")


@dataclass(frozen=True)
class ConstantRecord:
    constant: str
    value: int
    source: str


@dataclass(frozen=True)
class ObservedOccurrence:
    run_id: str
    section: str
    display_name: str
    source_log: str


def load_item_pool_batch_analyzer():
    module_path = SCRIPT_DIR / "item_pool_batch_analyzer.py"
    spec = importlib.util.spec_from_file_location("item_pool_batch_analyzer", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not import item_pool_batch_analyzer.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(spec.name, module)
    spec.loader.exec_module(module)
    return module


item_analyzer = load_item_pool_batch_analyzer()


def canonicalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def display_from_constant(constant: str, prefix: str) -> str:
    raw = constant.removeprefix(prefix)
    if re.fullmatch(r"TM\d{2,3}", raw) or re.fullmatch(r"HM\d{2,3}(?:_[A-Z0-9]+)?", raw):
        parts = raw.split("_", 1)
        return parts[0] if len(parts) == 1 else parts[0] + " " + title_from_parts(parts[1])
    return title_from_parts(raw)


def title_from_parts(raw: str) -> str:
    special = {
        "NIDORAN_F": "Nidoran F",
        "NIDORAN_M": "Nidoran M",
        "MR_MIME": "Mr Mime",
        "HO_OH": "Ho-Oh",
        "PORYGON_Z": "Porygon-Z",
        "TYPE_NULL": "Type Null",
        "JANGMO_O": "Jangmo-o",
        "HAKAMO_O": "Hakamo-o",
        "KOMMO_O": "Kommo-o",
    }
    if raw in special:
        return special[raw]
    return " ".join(part.capitalize() for part in raw.split("_") if part)


def parse_int(value: str) -> int:
    return int(value, 16) if value.lower().startswith("0x") else int(value)


def parse_constants(paths: Sequence[Path], prefix: str) -> list[ConstantRecord]:
    records: list[ConstantRecord] = []
    seen: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        rel_source = safe_relative(path)
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = DEFINE_RE.match(line)
            if not match:
                continue
            constant = match.group("constant")
            if not constant.startswith(prefix) or constant in seen:
                continue
            seen.add(constant)
            records.append(ConstantRecord(constant, parse_int(match.group("value")), rel_source))
    return records


def safe_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT.resolve()))
    except ValueError:
        return path.name


def build_expected(output_dir: Path, source_root: Path = REPO_ROOT) -> dict[str, list[dict[str, str]]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    dpe = source_root / "02_external" / "Dynamic-Pokemon-Expansion-Gen-9" / "include"
    cfru = source_root / "02_external" / "CFRU-expansion" / "include" / "constants"

    species_constants = parse_constants([dpe / "species.h", cfru / "species.h"], "SPECIES_")
    item_constants = parse_constants([dpe / "items.h", cfru / "items.h"], "ITEM_")

    species_rows = [species_expected_row(record) for record in species_constants if not skip_expected_constant(record.constant)]
    item_rows = [item_expected_row(record) for record in item_constants if not skip_expected_constant(record.constant)]
    tm_hm_rows = [row for row in item_rows if row["is_tm"] == "yes" or row["is_hm"] == "yes"]

    write_tsv(output_dir / "species_expected.tsv", species_rows, SPECIES_FIELDS)
    write_tsv(output_dir / "items_expected.tsv", item_rows, ITEM_FIELDS)
    write_tsv(output_dir / "tms_hms_expected.tsv", tm_hm_rows, ITEM_FIELDS)
    return {
        "species_expected.tsv": species_rows,
        "items_expected.tsv": item_rows,
        "tms_hms_expected.tsv": tm_hm_rows,
    }


def skip_expected_constant(constant: str) -> bool:
    suffix = constant.rsplit("_", 1)[-1]
    return suffix in {"NONE", "COUNT", "TOTAL", "END"} or constant.endswith("_COUNT")


def species_expected_row(record: ConstantRecord) -> dict[str, str]:
    display = display_from_constant(record.constant, "SPECIES_")
    return {
        "canonical_key": canonicalize(display),
        "source_constant": record.constant,
        "display_name_guess": display,
        "dex_number_or_source_id": str(record.value),
        "form_family": species_form_family(record.constant, display),
        "generation_guess": generation_guess(record.value),
        "expected_source": record.source,
        "observed_count_total": "0",
        "observed_sections": "",
        "observed_runs_seen": "0",
        "coverage_status": "UNKNOWN_REVIEW",
        "reason": "expected from source constants; final ROM-loaded presence not proven",
        "confidence": "Medium",
    }


def item_expected_row(record: ConstantRecord) -> dict[str, str]:
    display = display_from_constant(record.constant, "ITEM_")
    is_tm = bool(re.match(r"ITEM_TM\d{2,3}$", record.constant))
    is_hm = bool(re.match(r"ITEM_HM\d{2,3}(?:_|$)", record.constant))
    category = item_category_guess(record.constant, display)
    return {
        "canonical_key": canonicalize(display),
        "source_constant": record.constant,
        "display_name_guess": display,
        "item_id_or_source_id": str(record.value),
        "item_family": item_family_guess(record.constant, display),
        "item_category_guess": category,
        "is_tm": yes_no(is_tm),
        "is_hm": yes_no(is_hm),
        "expected_source": record.source,
        "observed_count_total": "0",
        "observed_sections": "",
        "observed_runs_seen": "0",
        "coverage_status": "UNKNOWN_REVIEW",
        "reason": "expected from source constants; final ROM-loaded presence not proven",
        "confidence": "Medium",
    }


def species_form_family(constant: str, display: str) -> str:
    name = normalize_name(display)
    families = ["unown", "vivillon", "alcremie", "minior", "rotom", "arceus", "silvally", "deoxys"]
    for family in families:
        if name.startswith(family):
            return family.capitalize()
    if any(token in constant for token in ("ALOLAN", "GALARIAN", "HISUIAN", "PALDEAN")):
        return "Regional Forms"
    if "MEGA" in constant or "GIGA" in constant:
        return "Mega/GMax"
    return ""


def generation_guess(source_id: int) -> str:
    ranges = [(151, "1"), (251, "2"), (386, "3"), (493, "4"), (649, "5"), (721, "6"), (809, "7"),
              (905, "8"), (1200, "9")]
    for max_id, generation in ranges:
        if source_id <= max_id:
            return generation
    return "UNKNOWN"


def item_family_guess(constant: str, display: str) -> str:
    norm = normalize_name(display)
    if re.match(r"ITEM_TM\d{2,3}$", constant):
        return "TM"
    if re.match(r"ITEM_HM\d{2,3}", constant):
        return "HM"
    if norm.endswith("berry"):
        return "Berry"
    if norm.endswith("gem"):
        return "Gem"
    if norm.endswith("ball"):
        return "Ball"
    if norm.endswith("plate"):
        return "Plate"
    if norm.endswith("memory") or norm.endswith("mem"):
        return "Memory"
    if norm.endswith("drive"):
        return "Drive"
    if norm.endswith("nectar"):
        return "Nectar"
    return ""


def item_category_guess(constant: str, display: str) -> str:
    if re.match(r"ITEM_TM\d{2,3}$", constant):
        return "tm"
    if re.match(r"ITEM_HM\d{2,3}", constant):
        return "hm"
    policy = item_analyzer.classify_item(display)
    if policy.policy_guess == "BAN":
        return "banned_or_bad_policy_guess"
    if policy.policy_guess == "MECHANIC_SETTING":
        return "mechanic_gated"
    if policy.policy_guess == "ALLOW":
        return "normal_reward_candidate"
    return "unknown_review"


def parse_logs(logs_dir: Path, output_dir: Path, delete_raw: bool = False) -> dict[str, list[dict[str, str]]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    log_files = discover_log_files(logs_dir)
    if not log_files:
        raise ValueError(f"no .log/.txt files found under {sanitize_path_for_error(logs_dir)}")

    species_occurrences: list[ObservedOccurrence] = []
    item_occurrences: list[ObservedOccurrence] = []
    tm_hm_occurrences: list[ObservedOccurrence] = []

    for log_file in log_files:
        text = log_file.read_text(encoding="utf-8-sig", errors="replace")
        run_id = log_file.stem
        source_log = log_file.name
        parsed_items = item_analyzer.parse_log_text(text, run_id=run_id, path=log_file)
        for occurrence in parsed_items.shop_items:
            item_occurrences.append(ObservedOccurrence(run_id, "shop", occurrence.item, source_log))
            add_tm_hm_if_needed(tm_hm_occurrences, run_id, "shop", occurrence.item, source_log)
        for occurrence in parsed_items.pickup_items:
            item_occurrences.append(ObservedOccurrence(run_id, "pickup", occurrence.item, source_log))
            add_tm_hm_if_needed(tm_hm_occurrences, run_id, "pickup", occurrence.item, source_log)

        parsed = parse_species_and_misc_log_text(text, run_id, source_log)
        species_occurrences.extend(parsed["species"])
        item_occurrences.extend(parsed["items"])
        tm_hm_occurrences.extend(parsed["tms_hms"])

    outputs = {
        "species_observed.tsv": aggregate_occurrences(species_occurrences),
        "items_observed.tsv": aggregate_occurrences(item_occurrences),
        "tms_hms_observed.tsv": aggregate_occurrences(tm_hm_occurrences),
    }
    write_tsv(output_dir / "species_observed.tsv", outputs["species_observed.tsv"], OBSERVED_FIELDS)
    write_tsv(output_dir / "items_observed.tsv", outputs["items_observed.tsv"], OBSERVED_FIELDS)
    write_tsv(output_dir / "tms_hms_observed.tsv", outputs["tms_hms_observed.tsv"], OBSERVED_FIELDS)

    if delete_raw:
        cleanup_files(log_files, logs_dir, allowed_suffixes=LOG_SUFFIXES)
    return outputs


def discover_log_files(logs_dir: Path) -> list[Path]:
    if not logs_dir.is_dir():
        raise ValueError(f"logs directory does not exist: {sanitize_path_for_error(logs_dir)}")
    return sorted(path for path in logs_dir.rglob("*") if path.is_file() and path.suffix.lower() in LOG_SUFFIXES)


def parse_species_and_misc_log_text(text: str, run_id: str, source_log: str) -> dict[str, list[ObservedOccurrence]]:
    species: list[ObservedOccurrence] = []
    items: list[ObservedOccurrence] = []
    tms_hms: list[ObservedOccurrence] = []
    section = ""

    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("\ufeff")
        match = SECTION_RE.match(line)
        if match:
            section = classify_section(match.group("title"))
            continue
        if not line or line.startswith("="):
            continue

        if section == "starter":
            starter_match = STARTER_RE.match(line)
            if starter_match:
                species.append(ObservedOccurrence(run_id, "starter", clean_species_name(starter_match.group("species")), source_log))
                if starter_match.group("item"):
                    item = clean_item_text(starter_match.group("item"))
                    items.append(ObservedOccurrence(run_id, "starter_held_item", item, source_log))
                    add_tm_hm_if_needed(tms_hms, run_id, "starter_held_item", item, source_log)
        elif section == "static":
            static_match = STATIC_RE.search(line)
            if static_match:
                species.append(ObservedOccurrence(run_id, "static", clean_species_name(static_match.group("species")), source_log))
        elif section == "wild":
            wild_match = WILD_RE.match(line)
            if wild_match and not line.lower().startswith("area #"):
                species.append(ObservedOccurrence(run_id, "wild", clean_species_name(wild_match.group("species")), source_log))
        elif section == "trainer":
            if " - " not in line:
                continue
            party_text = line.split(" - ", 1)[1]
            for party_entry in party_text.split(","):
                trainer_match = TRAINER_SPECIES_RE.search(party_entry.strip())
                if not trainer_match:
                    continue
                species.append(ObservedOccurrence(run_id, "trainer", clean_species_name(trainer_match.group("species")), source_log))
                if trainer_match.group("item"):
                    item = clean_item_text(trainer_match.group("item"))
                    items.append(ObservedOccurrence(run_id, "trainer_held_item", item, source_log))
                    add_tm_hm_if_needed(tms_hms, run_id, "trainer_held_item", item, source_log)
        elif section == "field_item":
            item = parse_field_item_line(line)
            if item:
                items.append(ObservedOccurrence(run_id, "field", item, source_log))
                add_tm_hm_if_needed(tms_hms, run_id, "field", item, source_log)
        elif section == "tm_hm":
            for label in parse_tm_hm_line(line):
                tms_hms.append(ObservedOccurrence(run_id, "tm_hm", label, source_log))

    return {"species": species, "items": items, "tms_hms": tms_hms}


def classify_section(title: str) -> str:
    lower = title.lower()
    if "starter" in lower:
        return "starter"
    if "static" in lower:
        return "static"
    if "wild" in lower:
        return "wild"
    if "trainer pokemon" in lower:
        return "trainer"
    if "field item" in lower:
        return "field_item"
    if "tm" in lower or "hm" in lower:
        return "tm_hm"
    return ""


def clean_species_name(value: str) -> str:
    cleaned = value.strip()
    cleaned = re.sub(r"\([^)]*\)$", "", cleaned).strip()
    cleaned = re.sub(r"\s+Lv(?:s)?\d+(?:-\d+)?$", "", cleaned).strip()
    cleaned = cleaned.split("@", 1)[0].strip()
    return cleaned


def clean_item_text(value: str) -> str:
    return value.strip().strip(",")


def parse_field_item_line(line: str) -> str:
    if "=>" in line:
        return clean_item_text(line.rsplit("=>", 1)[1])
    if line.startswith("- "):
        return clean_item_text(line[2:])
    return ""


def parse_tm_hm_line(line: str) -> list[str]:
    return [match.group("label").upper() for match in TM_HM_RE.finditer(line)]


def add_tm_hm_if_needed(occurrences: list[ObservedOccurrence], run_id: str, section: str, item: str, source_log: str) -> None:
    labels = parse_tm_hm_line(item)
    for label in labels:
        occurrences.append(ObservedOccurrence(run_id, section, label, source_log))


def aggregate_occurrences(occurrences: Sequence[ObservedOccurrence]) -> list[dict[str, str]]:
    grouped: dict[str, list[ObservedOccurrence]] = defaultdict(list)
    display_by_key: dict[str, str] = {}
    for occurrence in occurrences:
        if not occurrence.display_name:
            continue
        key = canonicalize(occurrence.display_name)
        grouped[key].append(occurrence)
        display_by_key.setdefault(key, occurrence.display_name)

    rows: list[dict[str, str]] = []
    for key in sorted(grouped):
        values = grouped[key]
        rows.append({
            "canonical_key": key,
            "display_name": display_by_key[key],
            "observed_count_total": str(len(values)),
            "observed_sections": ";".join(sorted({value.section for value in values})),
            "observed_runs_seen": str(len({value.run_id for value in values})),
            "source_logs_seen": str(len({value.source_log for value in values})),
            "confidence": observed_confidence(display_by_key[key]),
        })
    return rows


def observed_confidence(display_name: str) -> str:
    norm = display_name.lower()
    if "unknown" in norm or "????" in norm or norm.startswith("item #"):
        return "Low"
    return "Medium"


def compare(expected_path: Path, observed_path: Path, output_path: Path, fields: list[str],
            loaded_manifest: Path | None = None) -> list[dict[str, str]]:
    expected_rows = read_tsv(expected_path)
    observed_rows = read_tsv(observed_path) if observed_path.exists() else []
    observed_by_key = {row["canonical_key"]: row for row in observed_rows}
    loaded_keys = load_manifest_keys(loaded_manifest)

    coverage_rows: list[dict[str, str]] = []
    for expected in expected_rows:
        observed = observed_by_key.get(expected["canonical_key"])
        row = dict(expected)
        if observed:
            row["observed_count_total"] = observed["observed_count_total"]
            row["observed_sections"] = observed["observed_sections"]
            row["observed_runs_seen"] = observed["observed_runs_seen"]
            row["coverage_status"] = "EXPECTED_AND_OBSERVED"
            row["reason"] = "expected source constant was observed in parsed randomizer logs"
            row["confidence"] = merge_confidence(row.get("confidence", ""), observed.get("confidence", ""))
        elif loaded_keys is not None and expected["canonical_key"] not in loaded_keys:
            row["coverage_status"] = "EXPECTED_NOT_LOADED"
            row["reason"] = "expected source constant absent from supplied loaded manifest"
            row["confidence"] = "High"
        elif loaded_keys is not None:
            row["coverage_status"] = "LOADED_NOT_OBSERVED"
            row["reason"] = "loaded manifest contains expected row but batch logs did not observe it"
            row["confidence"] = "Medium"
        else:
            row["coverage_status"] = "EXPECTED_NOT_OBSERVED"
            row["reason"] = "not seen in parsed batch logs; random runs do not prove non-reachability without loaded manifest"
            row["confidence"] = "Medium"
        coverage_rows.append(row)

    expected_keys = {row["canonical_key"] for row in expected_rows}
    for key, observed in sorted(observed_by_key.items()):
        if key in expected_keys:
            continue
        coverage_rows.append(observed_not_expected_row(observed, fields))

    write_tsv(output_path, coverage_rows, fields)
    return coverage_rows


def observed_not_expected_row(observed: dict[str, str], fields: list[str]) -> dict[str, str]:
    row = {field: "" for field in fields}
    row["canonical_key"] = observed["canonical_key"]
    if "display_name_guess" in row:
        row["display_name_guess"] = observed["display_name"]
    row["observed_count_total"] = observed["observed_count_total"]
    row["observed_sections"] = observed["observed_sections"]
    row["observed_runs_seen"] = observed["observed_runs_seen"]
    row["coverage_status"] = "OBSERVED_NOT_EXPECTED"
    row["reason"] = "observed in sanitized logs but not found in source-derived expected index"
    row["confidence"] = "Low" if observed.get("confidence") == "Low" else "Medium"
    return row


def load_manifest_keys(path: Path | None) -> set[str] | None:
    if path is None:
        return None
    return {row["canonical_key"] for row in read_tsv(path)}


def merge_confidence(left: str, right: str) -> str:
    if "Low" in {left, right}:
        return "Low"
    if "High" in {left, right}:
        return "High"
    return "Medium"


def compare_all(output_dir: Path, loaded_manifest_dir: Path | None = None) -> dict[str, list[dict[str, str]]]:
    loaded_species = loaded_manifest_dir / "species_loaded.tsv" if loaded_manifest_dir else None
    loaded_items = loaded_manifest_dir / "items_loaded.tsv" if loaded_manifest_dir else None
    loaded_tms = loaded_manifest_dir / "tms_hms_loaded.tsv" if loaded_manifest_dir else None

    outputs = {
        "species_coverage.tsv": compare(
            output_dir / "species_expected.tsv", output_dir / "species_observed.tsv",
            output_dir / "species_coverage.tsv", SPECIES_FIELDS, loaded_species if loaded_species and loaded_species.exists() else None,
        ),
        "items_coverage.tsv": compare(
            output_dir / "items_expected.tsv", output_dir / "items_observed.tsv",
            output_dir / "items_coverage.tsv", ITEM_FIELDS, loaded_items if loaded_items and loaded_items.exists() else None,
        ),
        "tm_hm_coverage.tsv": compare(
            output_dir / "tms_hms_expected.tsv", output_dir / "tms_hms_observed.tsv",
            output_dir / "tm_hm_coverage.tsv", ITEM_FIELDS, loaded_tms if loaded_tms and loaded_tms.exists() else None,
        ),
    }
    write_summary(output_dir / "coverage_summary.md", outputs, loaded_manifest_dir is not None)
    suspicious = suspicious_or_missing_rows(outputs)
    write_tsv(output_dir / "suspicious_or_missing.tsv", suspicious,
              ["scope", "canonical_key", "display_name_guess", "coverage_status", "reason", "confidence"])
    return outputs


def suspicious_or_missing_rows(outputs: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows = []
    for filename, coverage_rows in outputs.items():
        scope = filename.removesuffix("_coverage.tsv").replace("tm_hm", "tms_hms")
        for row in coverage_rows:
            if row["coverage_status"] in {"OBSERVED_NOT_EXPECTED", "EXPECTED_NOT_LOADED", "LOADED_NOT_OBSERVED"}:
                rows.append({
                    "scope": scope,
                    "canonical_key": row["canonical_key"],
                    "display_name_guess": row.get("display_name_guess", ""),
                    "coverage_status": row["coverage_status"],
                    "reason": row["reason"],
                    "confidence": row["confidence"],
                })
            elif row["coverage_status"] == "EXPECTED_NOT_OBSERVED" and row["confidence"] == "Low":
                rows.append({
                    "scope": scope,
                    "canonical_key": row["canonical_key"],
                    "display_name_guess": row.get("display_name_guess", ""),
                    "coverage_status": row["coverage_status"],
                    "reason": row["reason"],
                    "confidence": row["confidence"],
                })
    return rows


def write_summary(path: Path, outputs: dict[str, list[dict[str, str]]], loaded_manifest_available: bool) -> None:
    lines = [
        "# Randomizer Coverage Audit Summary",
        "",
        "## Sanitized Scope",
        "",
        "- ROM paths documented: no",
        "- Output ROM paths documented: no",
        "- Raw logs included: no",
        "- Hashes included: no",
        "- Private paths included: no",
        "",
        "## Interpretation",
        "",
        "- `EXPECTED_AND_OBSERVED` means a source-derived expected row appeared in parsed log sections.",
        "- `EXPECTED_NOT_OBSERVED` is not a hard failure; random runs do not prove non-reachability.",
        "- `OBSERVED_NOT_EXPECTED` is a review candidate because a log label did not match the source-derived index.",
    ]
    if loaded_manifest_available:
        lines.append("- Loaded-manifest statuses were enabled for supplied manifest files.")
    else:
        lines.append("- No loaded manifest was supplied, so `EXPECTED_NOT_LOADED` was not assigned.")
    lines.extend(["", "## Counts", ""])
    for filename, rows in outputs.items():
        counts: dict[str, int] = defaultdict(int)
        for row in rows:
            counts[row["coverage_status"]] += 1
        lines.append(f"### {filename}")
        for status in sorted(counts):
            lines.append(f"- {status}: {counts[status]}")
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def batch_run(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir)
    ensure_local_output_dir(output_dir)
    raw_logs_dir = output_dir / "raw-logs"
    raw_roms_dir = output_dir / "output-roms"
    raw_logs_dir.mkdir(parents=True, exist_ok=True)
    raw_roms_dir.mkdir(parents=True, exist_ok=True)

    jar = Path(args.jar)
    input_rom = Path(args.input_rom)
    settings_file = Path(args.settings_file)
    if not jar.is_file():
        raise ValueError("UPR-FVX jar not found")
    if not input_rom.is_file():
        raise ValueError("input ROM path does not exist")
    if not settings_file.is_file():
        raise ValueError("settings/profile path does not exist")

    raw_logs: list[Path] = []
    output_roms: list[Path] = []
    for index in range(1, args.runs + 1):
        seed = seed_for_run(args.seed_strategy, args.seed_base, index)
        run_id = f"run_{index:04d}"
        output_rom = raw_roms_dir / f"{run_id}.gba"
        stdout_log = raw_logs_dir / f"{run_id}.stdout.log"
        detail_log = Path(str(output_rom) + ".log")
        command = [
            "java", "-jar", str(jar), "cli",
            "-i", str(input_rom),
            "-o", str(output_rom),
            "-s", str(settings_file),
            "-z", str(seed),
            "-l",
        ]
        with stdout_log.open("w", encoding="utf-8") as stdout_handle:
            completed = subprocess.run(command, stdout=stdout_handle, stderr=subprocess.STDOUT, check=False)
        raw_logs.append(stdout_log)
        output_roms.append(output_rom)
        if detail_log.exists():
            target_log = raw_logs_dir / f"{run_id}.log"
            shutil.move(str(detail_log), target_log)
            raw_logs.append(target_log)
        if completed.returncode != 0:
            raise RuntimeError(f"UPR-FVX CLI failed for {run_id}; raw local outputs were kept for review")

    parse_logs(raw_logs_dir, output_dir, delete_raw=False)
    if not args.keep_raw:
        cleanup_files(raw_logs, raw_logs_dir, allowed_suffixes=LOG_SUFFIXES)
        cleanup_files(output_roms, raw_roms_dir, allowed_suffixes={".gba", ".gb", ".gbc", ".nds", ".cxi"})


def seed_for_run(strategy: str, seed_base: int, run_index: int) -> int:
    if strategy == "sequential":
        return seed_base + run_index - 1
    if strategy == "fixed":
        return seed_base
    raise ValueError(f"unsupported seed strategy: {strategy}")


def cleanup_files(paths: Iterable[Path], base_dir: Path, allowed_suffixes: set[str]) -> None:
    safe_base = resolve_inside_workspace(base_dir)
    if not safe_base.parts or ".local" not in safe_base.parts:
        raise ValueError("refusing cleanup outside .local")
    for path in paths:
        safe_path = resolve_inside_workspace(path)
        if not is_relative_to(safe_path, safe_base):
            raise ValueError(f"refusing cleanup outside target directory: {sanitize_path_for_error(path)}")
        if safe_path.suffix.lower() not in allowed_suffixes:
            raise ValueError(f"refusing cleanup of unsupported file type: {safe_path.name}")
    for path in paths:
        Path(path).unlink(missing_ok=True)


def ensure_local_output_dir(output_dir: Path) -> None:
    resolved = (Path.cwd() / output_dir).resolve() if not output_dir.is_absolute() else output_dir.resolve()
    local_root = (Path.cwd() / ".local").resolve()
    if not is_relative_to(resolved, local_root):
        raise ValueError("output directory must be inside .local/")


def resolve_inside_workspace(path: Path) -> Path:
    workspace = Path.cwd().resolve()
    resolved = (workspace / path).resolve() if not path.is_absolute() else path.resolve()
    if not is_relative_to(resolved, workspace):
        raise ValueError(f"path outside workspace: {sanitize_path_for_error(path)}")
    return resolved


def sanitize_path_for_error(path: Path) -> str:
    value = str(path)
    value = re.sub(r"/[^ \t\n]+", "<path>", value)
    value = re.sub(r"[A-Za-z]:\\[^ \t\n]+", "<path>", value)
    return value


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def cmd_build_expected(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    ensure_local_output_dir(output_dir)
    build_expected(output_dir, Path(args.source_root))
    print(f"Wrote source-derived expected TSVs to {output_dir}")
    return 0


def cmd_parse_logs(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    ensure_local_output_dir(output_dir)
    parse_logs(Path(args.logs_dir), output_dir, delete_raw=args.delete_raw)
    print(f"Wrote sanitized observed TSVs to {output_dir}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    ensure_local_output_dir(output_dir)
    loaded_dir = Path(args.loaded_manifest_dir) if args.loaded_manifest_dir else None
    compare_all(output_dir, loaded_dir)
    print(f"Wrote coverage TSVs and summary to {output_dir}")
    return 0


def cmd_batch_run(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    ensure_local_output_dir(output_dir)
    batch_run(args)
    print(f"Wrote sanitized batch-run observed TSVs to {output_dir}")
    return 0


def cmd_all(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    ensure_local_output_dir(output_dir)
    build_expected(output_dir, Path(args.source_root))
    batch_run(args)
    compare_all(output_dir, None)
    print(f"Wrote full sanitized coverage audit to {output_dir}")
    return 0


def add_common_output(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory under .local/.")


def add_batch_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--jar", required=True, help="Path to local UPR-FVX.jar.")
    parser.add_argument("--input-rom", required=True, help="Private input ROM path. Never written to summaries.")
    parser.add_argument("--settings-file", required=True, help="Private settings/profile path. Never written to summaries.")
    parser.add_argument("--runs", type=int, required=True, help="Number of randomizer runs.")
    parser.add_argument("--seed-base", type=int, default=1)
    parser.add_argument("--seed-strategy", choices=["sequential", "fixed"], default="sequential")
    parser.add_argument("--keep-raw", action="store_true", help="Keep raw logs and output ROMs under .local/.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build sanitized UPR-FVX CFRU/DPE coverage audit summaries.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    expected = subparsers.add_parser("build-expected", help="Build source-derived expected TSVs without ROMs.")
    add_common_output(expected)
    expected.add_argument("--source-root", default=str(REPO_ROOT), help="Workspace/source root.")
    expected.set_defaults(func=cmd_build_expected)

    parse = subparsers.add_parser("parse-logs", help="Parse existing local randomizer logs.")
    add_common_output(parse)
    parse.add_argument("--logs-dir", default=str(DEFAULT_OUTPUT_DIR / "raw-logs"))
    parse.add_argument("--delete-raw", action="store_true", help="Delete parsed raw logs after successful analysis.")
    parse.set_defaults(func=cmd_parse_logs)

    batch = subparsers.add_parser("batch-run", help="Run local UPR-FVX CLI batches, parse logs, and clean outputs.")
    add_common_output(batch)
    add_batch_args(batch)
    batch.set_defaults(func=cmd_batch_run)

    compare_parser = subparsers.add_parser("compare", help="Compare expected and observed TSVs.")
    add_common_output(compare_parser)
    compare_parser.add_argument("--loaded-manifest-dir", help="Optional future sanitized loaded-manifest TSV directory.")
    compare_parser.set_defaults(func=cmd_compare)

    all_parser = subparsers.add_parser("all", help="Run build-expected, batch-run, parse, and compare.")
    add_common_output(all_parser)
    add_batch_args(all_parser)
    all_parser.add_argument("--source-root", default=str(REPO_ROOT), help="Workspace/source root.")
    all_parser.set_defaults(func=cmd_all)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "runs", 1) < 1:
        parser.error("--runs must be >= 1")
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
