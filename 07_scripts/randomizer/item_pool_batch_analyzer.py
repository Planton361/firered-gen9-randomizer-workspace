#!/usr/bin/env python3
"""Analyze UPR-FVX Shop/Pickup item logs without keeping raw logs.

The parser consumes already generated Randomizer logs. The optional batch-run
mode only wraps the existing UPR-FVX CLI for local user execution; Codex must
not run it with ROMs.
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_OUTPUT_DIR = Path(".local/item-pool-analysis")
LOG_SUFFIXES = {".log", ".txt"}

SECTION_RE = re.compile(r"^\(\s*(?P<title>.+?)\s+\{[A-Z0-9]+}\s*\)\s*$")
PICKUP_LEVEL_RE = re.compile(r"^Level\s+(\d+\s*-\s*\d+|\d+)\s*$", re.IGNORECASE)
PICKUP_PERCENT_RE = re.compile(r"^(?P<percent>\d+)%:\s*(?P<items>.+)$")


@dataclass(frozen=True)
class ShopItemOccurrence:
    run_id: str
    item: str
    shop: str


@dataclass(frozen=True)
class PickupItemOccurrence:
    run_id: str
    item: str
    level_range: str
    percentage: str


@dataclass(frozen=True)
class ParsedLog:
    run_id: str
    path: Path | None
    shop_items: tuple[ShopItemOccurrence, ...]
    pickup_items: tuple[PickupItemOccurrence, ...]


@dataclass(frozen=True)
class PolicyGuess:
    policy_guess: str
    suspicious: bool
    reason: str
    suggested_action: str


def normalize_item_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def clean_item_name(name: str) -> str:
    return name.strip().lstrip("\ufeff").strip()


def parse_log_text(text: str, run_id: str, path: Path | None = None) -> ParsedLog:
    shop_items: list[ShopItemOccurrence] = []
    pickup_items: list[PickupItemOccurrence] = []

    section: str | None = None
    in_special_shops = False
    current_shop: str | None = None
    current_level_range: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("\ufeff")
        section_match = SECTION_RE.match(line)
        if section_match:
            title = section_match.group("title").strip().lower()
            if title == "shop items":
                section = "shop"
                in_special_shops = False
                current_shop = None
            elif title == "pickup items":
                section = "pickup"
                current_level_range = None
            else:
                section = None
            continue

        if section == "shop":
            if not line or line.startswith("="):
                continue
            if line == "--Special Shops:--":
                in_special_shops = True
                current_shop = None
                continue
            if not in_special_shops:
                continue
            if line.startswith("- "):
                if current_shop:
                    item = clean_item_name(line[2:])
                    if item:
                        shop_items.append(ShopItemOccurrence(run_id, item, current_shop))
                continue
            if not line.startswith("--"):
                current_shop = line
            continue

        if section == "pickup":
            if not line or line.startswith("="):
                continue
            level_match = PICKUP_LEVEL_RE.match(line)
            if level_match:
                current_level_range = " ".join(line.split())
                continue
            percent_match = PICKUP_PERCENT_RE.match(line)
            if percent_match and current_level_range:
                percentage = f"{percent_match.group('percent')}%"
                for item in split_item_list(percent_match.group("items")):
                    pickup_items.append(PickupItemOccurrence(run_id, item, current_level_range, percentage))

    return ParsedLog(run_id, path, tuple(shop_items), tuple(pickup_items))


def split_item_list(text: str) -> list[str]:
    return [clean_item_name(part) for part in text.split(",") if clean_item_name(part)]


def discover_log_files(logs_dir: Path) -> list[Path]:
    if not logs_dir.is_dir():
        raise ValueError(f"logs directory does not exist: {logs_dir}")
    return sorted(path for path in logs_dir.rglob("*") if path.is_file() and path.suffix.lower() in LOG_SUFFIXES)


def parse_log_file(path: Path) -> ParsedLog:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return parse_log_text(text, run_id=path.stem, path=path)


def classify_item(item: str) -> PolicyGuess:
    norm = normalize_item_name(item)

    suspicious_exact = {
        "lightstone": ("BAN", "Light Stone is banned by Anton review."),
        "darkstone": ("BAN", "Dark Stone is banned by Anton review."),
        "gracidea": ("BAN", "Gracidea is a form-change item and Ban-Bad filtered."),
        "rustedsword": ("BAN", "Rusted Sword is a form/species system item."),
        "rustedshield": ("BAN", "Rusted Shield is a form/species system item."),
        "oddkeystone": ("BAN", "Odd Keystone is banned by Anton review."),
        "bottlecap": ("BAN", "Bottle Cap is banned from normal pools by Anton review."),
        "goldbottlecap": ("BAN", "Gold Bottle Cap is banned from normal pools by Anton review."),
        "sunflute": ("BAN", "Sun Flute is a story/system item."),
        "moonflute": ("BAN", "Moon Flute is a story/system item."),
        "dnasplicers": ("BAN", "DNA Splicers is a form/system item."),
        "revealglass": ("BAN", "Reveal Glass is a form/system item."),
        "prisonbottle": ("BAN", "Prison Bottle is a form/system item."),
        "zygardecube": ("BAN", "Zygarde Cube is a form/system item."),
        "nsolarizer": ("BAN", "N-Solarizer is a form/system item."),
        "nlunarizer": ("BAN", "N-Lunarizer is a form/system item."),
        "reinsunity": ("BAN", "Reins of Unity is a form/system item."),
        "reinsofunity": ("BAN", "Reins of Unity is a form/system item."),
    }
    if norm in suspicious_exact:
        policy, reason = suspicious_exact[norm]
        return PolicyGuess(policy, True, reason, "verify source section; keep excluded from normal pools")

    if re.fullmatch(r"(tm|hm)\d{1,3}.*", norm):
        return PolicyGuess("BAN", True, "TM/HM appeared in a normal item-pool log section.", "check slot type")
    if "fossil" in norm or norm == "oldamber":
        return PolicyGuess("BAN", True, "Fossil items are hard-banned from normal pools.", "confirm source is not static gift/script")
    if norm.endswith("shard"):
        return PolicyGuess("BAN", True, "Shard/exchange items are Ban-Bad filtered.", "confirm Ban Bad Items was enabled")
    if norm.startswith("relic"):
        return PolicyGuess("BAN", True, "Relic/high-value valuables are Ban-Bad filtered.", "confirm policy fix is present")
    if norm in {"bignugget", "balmmushroom", "pearlstring", "cometshard", "rarebone"}:
        return PolicyGuess("BAN", True, "High-value sell item should be Ban-Bad filtered.", "confirm policy fix is present")
    if "apricorn" in norm or "aprikoko" in norm:
        return PolicyGuess("BAN", True, "Apricorn/Aprikoko items are Ban-Bad filtered.", "confirm decoded item name")
    if norm.endswith("memory") or norm.endswith("mem"):
        return PolicyGuess("BAN", True, "Silvally Memory/form-change item should be Ban-Bad filtered.", "add name variant if needed")
    if norm.endswith("plate"):
        return PolicyGuess("BAN", True, "Plate/form-change item should be Ban-Bad filtered.", "confirm decoded item name")
    if norm.endswith("drive"):
        return PolicyGuess("BAN", True, "Drive/form-change item should be Ban-Bad filtered.", "confirm decoded item name")
    if norm.endswith("nectar"):
        return PolicyGuess("BAN", True, "Nectar/form-change item should be Ban-Bad filtered.", "confirm decoded item name")
    if is_z_crystal_name(norm):
        return PolicyGuess("MECHANIC_SETTING", True, "Z-Crystal should require Include Z-Crystal Items.", "check include setting")
    if is_mega_stone_name(norm):
        return PolicyGuess("MECHANIC_SETTING", True, "Mega Stone should require Include Mega Items.", "check include setting")
    if norm in {"dynamaxband", "dynamaxcandy", "wishingpiece", "wishingstar", "maxmushrooms", "maxhoney"}:
        return PolicyGuess("MECHANIC_SETTING", True, "Dynamax/GMax item should require Include Dynamax/GMax Items.", "check include setting")
    if "????" in item or "#" in item or norm.startswith("item") and any(ch.isdigit() for ch in norm):
        return PolicyGuess("REVIEW", True, "Fallback/unknown-looking item name.", "verify final ItemData")

    if is_allowed_reward_name(norm):
        return PolicyGuess("ALLOW", False, "Allowed by current Anton policy heuristic.", "none")

    if looks_system_or_form_related(norm):
        return PolicyGuess("REVIEW", True, "Name looks system/form/story-related but is not explicitly classified.", "review and add policy if confirmed")

    return PolicyGuess("UNKNOWN", False, "No suspicious heuristic matched.", "review only if observed unexpectedly")


def is_z_crystal_name(norm: str) -> bool:
    z_names = {
        "normaliumz", "firiumz", "wateriumz", "electriumz", "grassiumz", "iciumz", "fightiniumz",
        "poisoniumz", "groundiumz", "flyiniumz", "psychiumz", "buginiumz", "rockiumz", "ghostiumz",
        "dragoniumz", "darkiniumz", "steeliumz", "fairiumz", "pikaniumz", "pikashuniumz",
        "aloraichiumz", "alorichiumz", "araichuniumz", "eeviumz", "mewniumz", "snorliumz",
        "decidiumz", "inciniumz", "primariumz", "tapuniumz", "marshadiumz", "kommoniumz",
        "lycaniumz", "mimikiumz", "solganiumz", "lunaliumz", "ultranecroziumz", "necroziumz",
    }
    return norm in z_names or norm.endswith("iumz") or "zcrystal" in norm


def is_mega_stone_name(norm: str) -> bool:
    if norm == "eviolite":
        return False
    known = {
        "venusaurite", "charizarditex", "charizarditey", "blastoisinite", "blastoisnite",
        "blastoisenite", "blastoiseite", "beedrillite", "pidgeotite", "alakazite", "slowbronite",
        "gengarite", "kangaskhanite", "pinsirite", "gyaradosite", "aerodactylite", "mewtwonitex",
        "mewtwonitey", "ampharosite", "scizorite", "heracronite", "houndoominite", "tyranitarite",
        "sceptilite", "blazikenite", "swampertite", "gardevoirite", "sablenite", "mawilite",
        "aggronite", "medichamite", "manectite", "sharpedonite", "cameruptite", "altarianite",
        "banettite", "absolite", "glalitite", "salamencite", "metagrossite", "latiasite",
        "latiosite", "lucarionite", "abomasite", "galladite", "audinite", "diancite",
    }
    return norm in known or norm.endswith("ite") and norm not in {"eviolite"}


def is_allowed_reward_name(norm: str) -> bool:
    if norm.endswith("ball"):
        return True
    if norm.endswith("berry"):
        return True
    if norm.endswith("gem"):
        return True
    if norm in {
        "potion", "superpotion", "hyperpotion", "maxpotion", "fullrestore", "antidote", "parlyzheal",
        "awakening", "burnheal", "iceheal", "fullheal", "revive", "maxrevive", "freshwater",
        "sodapop", "lemonade", "moomoomilk", "energypowder", "energyroot", "healpowder",
        "revivalherb", "ether", "maxether", "elixir", "maxelixir", "berryjuice",
        "rarecandy", "ppup", "ppmax", "hpup", "protein", "iron", "carbos", "calcium", "zinc",
        "escaperope", "repel", "superrepel", "maxrepel", "honey", "heartscale",
        "xattack", "xdefend", "xdefense", "xspeed", "xaccuracy", "xspatk", "xspdef", "direhit",
        "guardspec", "floatstone", "twistedspoon", "spelltag", "expertbelt", "icyrock",
        "miracleseed", "clearamulet", "widelens", "throatspray", "punchingglove", "leftovers",
        "choiceband", "lifeorb", "eviolite",
        "firestone", "waterstone", "thunderstone", "leafstone", "moonstone", "sunstone",
        "shinystone", "duskstone", "dawnstone", "icestone", "linkcable", "linkingcord",
        "nugget", "pearl", "bigpearl", "tinymushroom", "bigmushroom",
    }:
        return True
    return False


def looks_system_or_form_related(norm: str) -> bool:
    markers = ("key", "card", "ticket", "charm", "orb", "flute", "stone", "chain", "cube", "gear", "catalog")
    return any(marker in norm for marker in markers)


def aggregate(parsed_logs: Sequence[ParsedLog]) -> dict[str, list[dict[str, str]]]:
    shop_by_item: dict[str, list[ShopItemOccurrence]] = defaultdict(list)
    pickup_by_item: dict[str, list[PickupItemOccurrence]] = defaultdict(list)
    for parsed in parsed_logs:
        for occurrence in parsed.shop_items:
            shop_by_item[occurrence.item].append(occurrence)
        for occurrence in parsed.pickup_items:
            pickup_by_item[occurrence.item].append(occurrence)

    shop_rows = []
    for item, occurrences in sorted(shop_by_item.items(), key=lambda pair: normalize_item_name(pair[0])):
        policy = classify_item(item)
        shops = sorted({occ.shop for occ in occurrences})
        runs = sorted({occ.run_id for occ in occurrences})
        shop_rows.append({
            "item": item,
            "count": str(len(occurrences)),
            "runs_seen": str(len(runs)),
            "shops_seen": str(len(shops)),
            "example_shop": shops[0] if shops else "",
            "policy_guess": policy.policy_guess,
            "suspicious": yes_no(policy.suspicious),
            "reason": policy.reason,
        })

    pickup_rows = []
    for item, occurrences in sorted(pickup_by_item.items(), key=lambda pair: normalize_item_name(pair[0])):
        policy = classify_item(item)
        level_ranges = sorted({occ.level_range for occ in occurrences})
        percentages = sorted({occ.percentage for occ in occurrences}, key=percentage_sort_key)
        runs = sorted({occ.run_id for occ in occurrences})
        pickup_rows.append({
            "item": item,
            "count": str(len(occurrences)),
            "runs_seen": str(len(runs)),
            "level_ranges_seen": "; ".join(level_ranges),
            "percentages_seen": "; ".join(percentages),
            "policy_guess": policy.policy_guess,
            "suspicious": yes_no(policy.suspicious),
            "reason": policy.reason,
        })

    combined_rows = []
    all_items = sorted(set(shop_by_item) | set(pickup_by_item), key=normalize_item_name)
    for item in all_items:
        policy = classify_item(item)
        shop_count = len(shop_by_item.get(item, []))
        pickup_count = len(pickup_by_item.get(item, []))
        first_seen_section = "shop" if shop_count else "pickup"
        combined_rows.append({
            "item": item,
            "shop_count": str(shop_count),
            "pickup_count": str(pickup_count),
            "total_count": str(shop_count + pickup_count),
            "first_seen_section": first_seen_section,
            "policy_guess": policy.policy_guess,
            "suspicious": yes_no(policy.suspicious),
            "reason": policy.reason,
        })

    suspicious_rows = []
    for row in combined_rows:
        if row["suspicious"] != "yes":
            continue
        item = row["item"]
        policy = classify_item(item)
        sections = []
        if int(row["shop_count"]) > 0:
            sections.append(("shop", row["shop_count"]))
        if int(row["pickup_count"]) > 0:
            sections.append(("pickup", row["pickup_count"]))
        for section, count in sections:
            suspicious_rows.append({
                "item": item,
                "section": section,
                "count": count,
                "policy_guess": policy.policy_guess,
                "reason": policy.reason,
                "suggested_action": policy.suggested_action,
            })

    return {
        "shop_items_summary.tsv": shop_rows,
        "pickup_items_summary.tsv": pickup_rows,
        "combined_item_summary.tsv": combined_rows,
        "suspicious_items.tsv": suspicious_rows,
    }


def percentage_sort_key(value: str) -> int:
    return -int(value.rstrip("%"))


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def write_outputs(parsed_logs: Sequence[ParsedLog], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    summaries = aggregate(parsed_logs)
    for filename, rows in summaries.items():
        write_tsv(output_dir / filename, rows)
    write_run_summary(output_dir / "run_summary.md", parsed_logs, summaries)


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames_by_file = {
        "shop_items_summary.tsv": [
            "item", "count", "runs_seen", "shops_seen", "example_shop", "policy_guess", "suspicious", "reason",
        ],
        "pickup_items_summary.tsv": [
            "item", "count", "runs_seen", "level_ranges_seen", "percentages_seen", "policy_guess",
            "suspicious", "reason",
        ],
        "combined_item_summary.tsv": [
            "item", "shop_count", "pickup_count", "total_count", "first_seen_section", "policy_guess",
            "suspicious", "reason",
        ],
        "suspicious_items.tsv": [
            "item", "section", "count", "policy_guess", "reason", "suggested_action",
        ],
    }
    fieldnames = fieldnames_by_file[path.name]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_run_summary(path: Path, parsed_logs: Sequence[ParsedLog], summaries: dict[str, list[dict[str, str]]]) -> None:
    shop_count = sum(len(log.shop_items) for log in parsed_logs)
    pickup_count = sum(len(log.pickup_items) for log in parsed_logs)
    suspicious_count = len(summaries["suspicious_items.tsv"])
    unique_items = len(summaries["combined_item_summary.tsv"])
    lines = [
        "# Item Pool Batch Analysis Summary",
        "",
        "## Sanitized Summary",
        "",
        f"- Runs/logs parsed: {len(parsed_logs)}",
        f"- Shop item occurrences: {shop_count}",
        f"- Pickup item occurrences: {pickup_count}",
        f"- Unique items observed: {unique_items}",
        f"- Suspicious item-section rows: {suspicious_count}",
        "- ROM paths documented: no",
        "- Output ROM paths documented: no",
        "- Raw logs included: no",
        "- Hashes included: no",
        "",
        "## Notes",
        "",
        "- `policy_guess` is heuristic and review-oriented; it is not final ROM proof.",
        "- Static Script/Gift/NPC sources are outside this parser unless they appear in these log sections.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_only(args: argparse.Namespace) -> int:
    logs_dir = Path(args.logs_dir)
    output_dir = Path(args.output_dir)
    ensure_output_dir_is_local(output_dir)
    log_files = discover_log_files(logs_dir)
    if not log_files:
        raise ValueError(f"no .log/.txt files found under {logs_dir}")
    parsed_logs = [parse_log_file(path) for path in log_files]
    write_outputs(parsed_logs, output_dir)
    if args.delete_raw_logs:
        cleanup_raw_logs(log_files, logs_dir, Path.cwd())
    print(f"Wrote sanitized summaries for {len(parsed_logs)} logs to {output_dir}")
    return 0


def batch_run(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    ensure_output_dir_is_local(output_dir)
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    jar = Path(args.jar)
    input_rom = Path(args.input_rom)
    settings_file = Path(args.settings_file)
    if not jar.is_file():
        raise ValueError("UPR-FVX jar not found. Build it locally outside this script if needed.")
    if not input_rom.is_file():
        raise ValueError("input ROM path does not exist")
    if not settings_file.is_file():
        raise ValueError("settings/profile path does not exist")

    parsed_logs: list[ParsedLog] = []
    raw_logs: list[Path] = []
    output_roms: list[Path] = []

    for run_index in range(1, args.runs + 1):
        seed = seed_for_run(args.seed_strategy, args.seed_base, run_index)
        run_id = f"run_{run_index:04d}"
        output_rom = raw_dir / f"{run_id}.gba"
        stdout_log = raw_dir / f"{run_id}.stdout.log"
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
            raw_logs.append(detail_log)
        if completed.returncode != 0:
            raise RuntimeError(f"UPR-FVX CLI failed for {run_id}; raw logs remain under ignored local output dir")
        if not detail_log.exists():
            raise RuntimeError(f"UPR-FVX detailed log missing for {run_id}; raw logs remain under ignored local output dir")
        parsed_logs.append(parse_log_file(detail_log))

    write_outputs(parsed_logs, output_dir)
    if not args.keep_raw_logs:
        cleanup_raw_logs(raw_logs, raw_dir, Path.cwd())
        cleanup_output_roms(output_roms, raw_dir, Path.cwd())
    print(f"Wrote sanitized summaries for {len(parsed_logs)} batch runs to {output_dir}")
    return 0


def seed_for_run(strategy: str, seed_base: int, run_index: int) -> int:
    if strategy == "sequential":
        return seed_base + run_index - 1
    if strategy == "fixed":
        return seed_base
    raise ValueError(f"unsupported seed strategy: {strategy}")


def cleanup_raw_logs(log_files: Iterable[Path], logs_dir: Path, workspace: Path) -> None:
    safe_dir = resolve_within_workspace(logs_dir, workspace)
    if safe_dir == workspace.resolve():
        raise ValueError("refusing to delete logs from workspace root")
    for log_file in log_files:
        safe_file = resolve_within_workspace(log_file, workspace)
        if not is_relative_to(safe_file, safe_dir):
            raise ValueError(f"refusing to delete file outside logs directory: {log_file}")
        if safe_file.suffix.lower() not in LOG_SUFFIXES:
            raise ValueError(f"refusing to delete non-log file: {log_file}")
    for log_file in log_files:
        Path(log_file).unlink(missing_ok=True)


def cleanup_output_roms(output_roms: Iterable[Path], raw_dir: Path, workspace: Path) -> None:
    safe_dir = resolve_within_workspace(raw_dir, workspace)
    for output_rom in output_roms:
        safe_file = resolve_within_workspace(output_rom, workspace)
        if not is_relative_to(safe_file, safe_dir):
            raise ValueError(f"refusing to delete output outside raw directory: {output_rom}")
        if safe_file.suffix.lower() not in {".gba", ".gb", ".gbc", ".nds", ".cxi"}:
            raise ValueError(f"refusing to delete non-ROM output path: {output_rom}")
    for output_rom in output_roms:
        Path(output_rom).unlink(missing_ok=True)


def resolve_within_workspace(path: Path, workspace: Path) -> Path:
    resolved_workspace = workspace.resolve()
    resolved_path = path.resolve()
    if not is_relative_to(resolved_path, resolved_workspace):
        raise ValueError(f"path is outside workspace: {path}")
    return resolved_path


def ensure_output_dir_is_local(output_dir: Path) -> None:
    workspace = Path.cwd().resolve()
    resolved = output_dir.resolve()
    if not is_relative_to(resolved, workspace / ".local"):
        raise ValueError("output directory must be inside .local/")


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze UPR-FVX Shop/Pickup item logs.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    parse_parser = subparsers.add_parser("parse-only", help="Parse existing local Randomizer logs.")
    parse_parser.add_argument("--logs-dir", required=True, help="Directory containing local .log/.txt Randomizer logs.")
    parse_parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Local ignored output directory.")
    parse_parser.add_argument("--delete-raw-logs", action="store_true",
                              help="Delete parsed raw logs after successful summary generation.")
    parse_parser.set_defaults(func=parse_only)

    batch_parser = subparsers.add_parser("batch-run", help="Run UPR-FVX CLI locally, then parse and clean outputs.")
    batch_parser.add_argument("--jar", required=True, help="Path to local UPR-FVX.jar.")
    batch_parser.add_argument("--input-rom", required=True, help="Private input ROM path. Never written to summaries.")
    batch_parser.add_argument("--settings-file", required=True, help="Settings/profile path.")
    batch_parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Local ignored output directory.")
    batch_parser.add_argument("--runs", type=int, required=True, help="Number of randomization runs.")
    batch_parser.add_argument("--seed-strategy", choices=["sequential", "fixed"], default="sequential")
    batch_parser.add_argument("--seed-base", type=int, default=1)
    batch_parser.add_argument("--keep-raw-logs", action="store_true",
                              help="Keep raw logs and output ROMs under .local/ instead of deleting them.")
    batch_parser.set_defaults(func=batch_run)
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
