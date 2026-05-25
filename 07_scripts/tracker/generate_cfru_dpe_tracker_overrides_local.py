#!/usr/bin/env python3
"""Generate ignored CFRU/DPE Tracker layout overrides from source-backed candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_OUTPUT = "03_tools/tracker-extensions/CFRUDPEExtension/data/tracker-overrides.local.json"

PROGRAM_ADDRESSES = {
    "offsetBattlePokemonTypes": 0x21,
    "offsetBattlePokemonStatStages": 0x19,
    "offsetBattleMoves": 0x01,
    "offsetBattleMoveFlags": 0x08,
    "offsetTrainerClass": 0x01,
    "offsetTrainerGender": 0x02,
    "offsetTrainerPic": 0x03,
    "offsetTrainerName": 0x04,
    "offsetTrainerItems": 0x10,
    "offsetTrainerDoubleBattle": 0x18,
    "offsetTrainerFlagsAI": 0x1C,
    "offsetTrainerPartySize": 0x20,
    "offsetTrainerPartyPtr": 0x24,
    "sizeofBaseStatsPokemon": 0x1C,
    "sizeofBattlePokemon": 0x58,
    "sizeofBattleMove": 0x0C,
    "sizeofTrainer": 0x28,
    "sizeofTrainerName": 0x0C,
    "sizeofTrainerItem": 0x02,
}

POKEMON_DATA_ADDRESSES = {
    "offsetBaseStats": 0x00,
    "offsetTypes": 0x06,
    "offsetCatchRate": 0x08,
    "offsetExpYield": 0x09,
    "offsetBaseFriendship": 0x12,
    "offsetAbilities": 0x16,
    "sizeofAbilityInBytes": 0x01,
}

MOVE_DATA_ADDRESSES = {
    "offsetMovePower": 0,
    "offsetMoveType": 8,
    "offsetMoveAccuracy": 16,
    "offsetMovePP": 24,
    "offsetMoveFlagsCategory": 6,
    "sizeofMovePower": 8,
    "sizeofMoveType": 8,
    "sizeofMoveAccuracy": 8,
    "sizeofMovePP": 8,
    "sizeofMoveFlagsCategory": 2,
}

SOURCE_DERIVED_CANDIDATES = {
    "BattleMove": {
        "sizeofBattleMove": "0x0C",
        "offsetBattleMoves": "0x01",
        "offsetBattleMoveFlags": "0x08",
        "offsetMovePowerByte": "0x01",
        "offsetMoveTypeByte": "0x02",
        "offsetMoveAccuracyByte": "0x03",
        "offsetMovePPByte": "0x04",
        "offsetMoveSplitByte": "0x0A",
    },
    "BattlePokemon": {
        "sizeofBattlePokemon": "0x58",
        "offsetBattlePokemonTypes": "0x21",
        "offsetBattlePokemonStatStages": "0x19",
    },
    "BaseStats": {
        "sizeofBaseStatsPokemon": "0x1C",
        "offsetBaseStats": "0x00",
        "offsetTypes": "0x06",
        "offsetCatchRate": "0x08",
        "offsetExpYield": "0x09",
        "offsetBaseFriendship": "0x12",
        "offsetAbilities": "0x16",
        "offsetHiddenAbility": "0x1A",
    },
    "Trainer": {
        "sizeofTrainer": "0x28",
        "offsetTrainerClass": "0x01",
        "offsetTrainerGender": "0x02",
        "offsetTrainerPic": "0x03",
        "offsetTrainerName": "0x04",
        "offsetTrainerItems": "0x10",
        "offsetTrainerDoubleBattle": "0x18",
        "offsetTrainerFlagsAI": "0x1C",
        "offsetTrainerPartySize": "0x20",
        "offsetTrainerPartyPtr": "0x24",
    },
    "Bag": {
        "sizeofItemSlot": "0x04",
        "bagItemsCount": 42,
        "bagKeyItemsCount": 30,
        "bagPokeBallsCount": 13,
        "bagTmHmCount": 58,
        "bagBerriesCount": 43,
    },
}


def build_manifest() -> dict[str, object]:
    return {
        "CFRUDPEManifest": {
            "schema": "cfru-dpe-tracker-overrides-local-v1",
            "status": "local-generated-do-not-commit",
            "generatedBy": "07_scripts/tracker/generate_cfru_dpe_tracker_overrides_local.py",
            "sourceDerivedFrom": [
                "01_docs/analysis/cfru-dpe-tracker-layout-overrides.md",
                "02_external/Ironmon-Tracker/ironmon_tracker/GameSettings.lua",
                "02_external/Ironmon-Tracker/ironmon_tracker/TrackerAPI.lua",
                "02_external/Ironmon-Tracker/ironmon_tracker/Program.lua",
                "02_external/Ironmon-Tracker/ironmon_tracker/data/PokemonData.lua",
                "02_external/Ironmon-Tracker/ironmon_tracker/data/MoveData.lua",
                "02_external/CFRU-expansion/include/pokemon.h",
                "02_external/CFRU-expansion/include/battle.h",
                "02_external/CFRU-expansion/include/global.h",
            ],
            "notAddressData": True,
            "addressPolicy": "Layout values only. No ROM, RAM, runtime, build, offsets.ini or private path data.",
            "effectiveOverrideSections": ["Program", "PokemonData", "MoveData"],
            "loaderCaveat": (
                "TrackerAPI.loadTrackerOverridesFromJson accepts Program/PokemonData/MoveData sections, "
                "but local smoke must verify whether imported keys update the nested *.Addresses tables "
                "used by Tracker read paths."
            ),
            "sourceDerivedCandidates": SOURCE_DERIVED_CANDIDATES,
            "notEmittedAsEffectiveOverrides": {
                "offsetMoveSplitByte": (
                    "CFRU split byte is source-backed, but stock Tracker category reading uses "
                    "MoveData.Addresses.offsetMoveFlagsCategory against a flags byte."
                ),
                "sizeofItemSlot": (
                    "Bag slot size is source-backed, but bag support uses GameSettings saveblock "
                    "pocket fields rather than a recognized tracker-overrides section."
                ),
                "bagPocketCounts": (
                    "Pocket counts are source-backed, but SaveBlock/runtime addresses remain local metadata."
                ),
                "expandedTrainerMonItemCustomMovesSize": (
                    "CFRU expanded custom trainer rows exceed stock Tracker static trainer-party assumptions."
                ),
                "structPokemonPartyOffsets": (
                    "CFRU party Pokemon layout is not safely handled by stock vanilla encrypted "
                    "Program.readNewPokemon offsets."
                ),
            },
            "warnings": [
                "This file is ignored and local-only.",
                "No real ROM/runtime/build addresses are included.",
                "Do not claim live party, battle, trainer-party or bag correctness from layout overrides alone.",
                "Validate Tracker override loader behavior before relying on these values in Tracker.",
            ],
        },
        "Program": {
            "Addresses": PROGRAM_ADDRESSES,
            "Values": {},
        },
        "PokemonData": {
            "Addresses": POKEMON_DATA_ADDRESSES,
            "Values": {},
        },
        "MoveData": {
            "Addresses": MOVE_DATA_ADDRESSES,
            "Values": {},
        },
        "AbilityData": {
            "Addresses": {},
            "Values": {},
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate ignored CFRU/DPE tracker-overrides.local.json with source-backed layout "
            "candidates only. No ROM/runtime addresses are emitted."
        )
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Output JSON path. Defaults to {DEFAULT_OUTPUT}.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_manifest(), indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print("Wrote local tracker-overrides manifest with Program, PokemonData and MoveData layout candidates.")
    print("Warnings: validate Tracker override loader behavior before relying on these values.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
