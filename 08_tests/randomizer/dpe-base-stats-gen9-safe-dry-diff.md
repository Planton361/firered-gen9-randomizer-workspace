# DPE Base Stats Gen9 safe dry diff smoke

Date: 2026-05-29
Branch: `analysis/dpe-base-stats-gen9-safe-dry-diff`
Result: `PASS_READ_ONLY_WITH_BLOCKERS`

## Scope

This smoke covers the read-only DPE Base Stats dry-diff helper against external Pokemon Showdown `pokedex.ts`.

No CFRU/DPE data table, UPR-FVX code, submodule pin, Pokemon Showdown data copy, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret, or `.env` data is included.

## Commands

- `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`
- `python3 07_scripts/data_audit/pokemon_data_dry_run.py --showdown-data-dir <external-pokemon-showdown-data-dir>`
- `python3 -m py_compile 07_scripts/data_audit/dpe_base_stats_dry_diff.py`
- `python3 07_scripts/data_audit/dpe_base_stats_dry_diff.py --showdown-data-dir <external-pokemon-showdown-data-dir> --limit 10`

## Observed result

The helper completed successfully and remained read-only.

Sanitized dry-diff counts:

- Tested Species: `1317`.
- Skipped Species `open-risk`: `29`.
- Skipped reviewed Species ignores: `167`.
- Skipped from safe candidate promotion by Ability blockers: `65`.
- Missing local entries after alias/ignore handling: `4`.
- Safe candidate Species with non-Ability field diffs: `225`.

Top non-Ability field differences:

- `genderRatio`: `103`.
- `baseAttack`: `67`.
- `baseSpAttack`: `60`.
- `baseDefense`: `52`.
- `baseSpDefense`: `49`.
- `baseSpeed`: `48`.
- `eggGroup2`: `41`.
- `eggGroup1`: `39`.
- `baseHP`: `23`.
- `type2`: `17`.
- `type1`: `8`.

Ability assignment differences were reported but not promoted:

- `ability2`: `711`.
- `hiddenAbility`: `106`.
- `ability1`: `101`.

Pokemon Showdown `pokedex.ts` did not provide Catch Rate, EXP Yield, EV Yield, or Growth Rate for this pass.

## Caveats

This smoke confirms a sanitized dry-diff path only. It is not a generated update, not a DPE/CFRU data-table change, not a build, not a ROM smoke, and not P1 promotion.
