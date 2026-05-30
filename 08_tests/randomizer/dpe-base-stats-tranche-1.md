# DPE Base Stats tranche 1 smoke

Date: 2026-05-29
Workspace branch: `data/dpe-base-stats-tranche-1`
DPE branch: `data/dpe-base-stats-tranche-1`
DPE commit: `1c8d53870e38d7019c681a68a17c9425a3490611`
Result: `PASS_SOURCE_DIFF_CHECKED_WITH_DRY_DIFF_REDUCTION`

## Scope

This smoke covers the first narrow DPE `Base_Stats.c` tranche from the merged plan.

Only DPE `src/Base_Stats.c` was changed. No CFRU, UPR-FVX, other DPE files, ROMs, saves, builds, tool binaries, screenshots, raw reports, hashes, private paths, tokens, secrets, or `.env` data are included.

## Changed fields

- Crobat: `eggGroup2` `EGG_GROUP_FIELD` -> `EGG_GROUP_FLYING`.
- Magnezone: `eggGroup1/eggGroup2` `EGG_GROUP_MONSTER` -> `EGG_GROUP_MINERAL`.
- Sylveon: `eggGroup1/eggGroup2` `EGG_GROUP_FAIRY` -> `EGG_GROUP_FIELD`.
- Brionne: `eggGroup1` `EGG_GROUP_MONSTER` -> `EGG_GROUP_WATER_1`; `eggGroup2` `EGG_GROUP_WATER_1` -> `EGG_GROUP_FIELD`.
- Primarina: `genderRatio` `PERCENT_FEMALE(50)` -> `PERCENT_FEMALE(12.5)`.
- Ursaluna: `type1/type2` `TYPE_NORMAL` / `TYPE_GROUND` -> `TYPE_GROUND` / `TYPE_NORMAL`.
- Sneasel-Hisui: `type1/type2` `TYPE_POISON` / `TYPE_FIGHTING` -> `TYPE_FIGHTING` / `TYPE_POISON`.
- Sneasler: `type1/type2` `TYPE_POISON` / `TYPE_FIGHTING` -> `TYPE_FIGHTING` / `TYPE_POISON`.
- Toedscool: `eggGroup1/eggGroup2` `EGG_GROUP_GRASS` -> `EGG_GROUP_FIELD`.
- Toedscruel: `eggGroup1/eggGroup2` `EGG_GROUP_GRASS` -> `EGG_GROUP_FIELD`.

## Explicit non-scope

No Ability fields, Catch Rate, EXP Yield, EV Yield, Growth Rate, held items, base stats, moves, learnsets, egg moves outside `Base_Stats.c` egg-group fields, TM/Tutor compatibility, CFRU code, UPR-FVX code, or submodule changes outside the DPE pin were changed.

## Checks

- DPE `git status --short`.
- DPE `git diff --stat`.
- DPE `git diff --check`.
- Workspace `git status --short`.
- Workspace `git diff --stat`.
- Workspace `git diff --check`.
- `python3 07_scripts/data_audit/dpe_base_stats_dry_diff.py --showdown-data-dir <external-pokemon-showdown-data-dir> --limit 25`.

Dry-diff summary after the tranche:

- Safe candidate Species with non-Ability field diffs changed from `225` to `215`.
- Frequent field counts dropped as expected for the tranche fields: `eggGroup1` `39` -> `34`, `eggGroup2` `41` -> `35`, `type1` `8` -> `5`, `type2` `17` -> `14`, `genderRatio` `103` -> `102`.

## Caveats

This is source/diff checked only. No local DPE/CFRU rebuild, ROM boot, emulator smoke, BizHawk validation, Ironmon Tracker validation, full playthrough, or P1 promotion is claimed.
