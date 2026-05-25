#!/usr/bin/env python3
"""Generate ignored CFRU/DPE Tracker address overrides from a local offsets.ini."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


COMMENT_RE = re.compile(r"\s*(?://|#|;).*$")
SYMBOL_RE = re.compile(r"^\.?([A-Za-z_][A-Za-z0-9_]*)$")
ADDRESS_RE = re.compile(r"^(?:0[xX])?[0-9A-Fa-f]{6,8}$")

REQUESTED_SYMBOLS = [
    "gBattleMoves",
    "gMoveNames",
    "gAbilityNames",
    "gTrainers",
    "gLevelUpLearnsets",
    "gTrainerClassNames",
    "gTypeNames",
    "gBaseStats",
    "gSpeciesInfo",
    "gSpeciesNames",
    "sTMHMMoves",
]

OPTIONAL_TRACKER_SYMBOLS = [
    "gBattleTypeFlags",
    "gBattleOutcome",
    "gPlayerPartyCount",
    "gTrainerBattleOpponent_A",
    "gTrainerBattleOpponent_B",
]

LIVE_SYMBOLS = [
    "gPlayerParty",
    "gEnemyParty",
    "gBattleMons",
]

SAVE_BLOCK_MARKERS = [
    "gSaveBlock1",
    "gSaveBlock2",
    "gSaveBlock1Ptr",
    "gSaveBlock2Ptr",
]

BAG_MARKERS = [
    "gBagPockets",
    "BagPocket",
    "BagPockets",
]

TRACKER_ADDRESS_ALIASES = {
    "gPlayerParty": "pstats",
    "gEnemyParty": "estats",
}


def strip_comment(line: str) -> str:
    return COMMENT_RE.sub("", line).strip()


def normalize_symbol(token: str) -> str | None:
    match = SYMBOL_RE.match(token.strip())
    if match is None:
        return None
    return match.group(1)


def parse_address(token: str) -> int | None:
    token = token.strip().rstrip(",")
    if not ADDRESS_RE.match(token):
        return None
    if token.lower().startswith("0x"):
        return int(token, 16)
    return int(token, 16)


def format_address(value: int) -> str:
    return f"0x{value:08X}"


def parse_symbol_line(line: str) -> tuple[str, int] | None:
    line = strip_comment(line)
    if not line or line.startswith("["):
        return None

    if ":" in line:
        left, right = line.split(":", 1)
        symbol = normalize_symbol(left)
        address = parse_address(right.strip().split()[0]) if right.strip() else None
        if symbol is not None and address is not None:
            return symbol, address

    if "=" in line:
        left, right = line.split("=", 1)
        symbol = normalize_symbol(left)
        address = parse_address(right.strip().split()[0]) if right.strip() else None
        if symbol is not None and address is not None:
            return symbol, address

    tokens = line.replace(",", " ").split()
    if len(tokens) < 2:
        return None

    first_symbol = normalize_symbol(tokens[0])
    second_address = parse_address(tokens[1])
    if first_symbol is not None and second_address is not None:
        return first_symbol, second_address

    first_address = parse_address(tokens[0])
    second_symbol = normalize_symbol(tokens[1])
    if first_address is not None and second_symbol is not None:
        return second_symbol, first_address

    return None


def parse_offsets(path: Path) -> dict[str, int]:
    symbols: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parsed = parse_symbol_line(line)
        if parsed is None:
            continue
        symbol, address = parsed
        symbols[symbol] = address
    return symbols


def warning(message: str, symbol: str | None = None) -> dict[str, str]:
    data = {"type": "missing-symbol", "message": message}
    if symbol is not None:
        data["symbol"] = symbol
    return data


def build_manifest(symbols: dict[str, int], input_count: int) -> dict[str, object]:
    extracted: dict[str, str] = {}
    addresses: dict[str, str] = {}
    warnings: list[dict[str, str]] = []

    for symbol in REQUESTED_SYMBOLS + OPTIONAL_TRACKER_SYMBOLS + LIVE_SYMBOLS:
        if symbol not in symbols:
            continue
        value = format_address(symbols[symbol])
        extracted[symbol] = value
        addresses[symbol] = value
        alias = TRACKER_ADDRESS_ALIASES.get(symbol)
        if alias is not None:
            addresses[alias] = value

    for symbol in REQUESTED_SYMBOLS:
        if symbol not in symbols:
            warnings.append(warning("Requested table/name symbol was not present in offsets.ini.", symbol))

    for symbol in LIVE_SYMBOLS:
        if symbol not in symbols:
            warnings.append(warning("Live party/battle RAM symbol was not present in offsets.ini.", symbol))

    if not any(symbol in symbols for symbol in SAVE_BLOCK_MARKERS):
        warnings.append(
            {
                "type": "missing-saveblock-symbols",
                "message": "No SaveBlock symbols were found; bag/save data addresses still need local runtime metadata.",
            }
        )

    if not any(symbol in symbols for symbol in BAG_MARKERS):
        warnings.append(
            {
                "type": "missing-bag-symbols",
                "message": "No bag-pocket symbols were found; bag support still needs local runtime metadata.",
            }
        )

    return {
        "CFRUDPEManifest": {
            "schema": "cfru-dpe-tracker-game-addresses-local-v1",
            "status": "local-generated-do-not-commit",
            "generatedBy": "07_scripts/tracker/generate_cfru_dpe_game_addresses_local.py",
            "source": {
                "kind": "offsets.ini",
                "pathPolicy": "Input path intentionally omitted from generated JSON.",
                "inputCount": input_count,
            },
            "addressPolicy": (
                "Local target addresses only. This file is ignored and must not be committed."
            ),
            "recognizedSymbols": sorted(extracted.keys()),
            "warnings": warnings,
        },
        "GameInfo": {
            "GameCode": 1112560197,
            "VersionColor": "FireRed",
            "Language": "English",
            "VersionName": "CFRU/DPE Gen9 FireRed Local",
            "VersionGroup": 2,
            "GameName": "CFRU/DPE Gen9 FireRed Local",
            "GameNumber": 3,
        },
        "Addresses": addresses,
        "AbilityAddresses": {},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate ignored CFRU/DPE game-addresses.local.json from a local offsets.ini. "
            "The generated file contains local addresses and must not be committed."
        )
    )
    parser.add_argument(
        "--offsets",
        action="append",
        required=True,
        help=(
            "Path to a local CFRU/DPE offsets.ini file. May be repeated for split CFRU and DPE "
            "symbol files. Paths are not written to the output JSON."
        ),
    )
    parser.add_argument(
        "--output",
        default="03_tools/tracker-extensions/CFRUDPEExtension/data/game-addresses.local.json",
        help="Output JSON path. Defaults to the ignored CFRUDPEExtension data/game-addresses.local.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    offsets_paths = [Path(path) for path in args.offsets]
    for offsets in offsets_paths:
        if not offsets.is_file():
            raise FileNotFoundError(offsets)

    output = Path(args.output)
    symbols: dict[str, int] = {}
    for offsets in offsets_paths:
        symbols.update(parse_offsets(offsets))
    manifest = build_manifest(symbols, len(offsets_paths))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    recognized = manifest["CFRUDPEManifest"]["recognizedSymbols"]
    warnings = manifest["CFRUDPEManifest"]["warnings"]
    print(f"Wrote local game-addresses manifest with {len(recognized)} recognized symbols.")
    print(f"Warnings: {len(warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
