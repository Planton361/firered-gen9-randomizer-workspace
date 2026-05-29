# Pokemon data generator dry-run smoke

Date: 2026-05-29
Branch: `analysis/pokemon-data-generator-dry-run-plan`
Result: `PASS_DRY_RUN_GATE_BLOCKED_BY_REVIEWED_POLICY`

## Scope

This smoke covers the read-only Pokemon Showdown-to-CFRU/DPE data dry-run helper and the reviewed alias-table gate.

No CFRU/DPE Pokemon data tables, UPR-FVX code, submodule pins, Pokemon Showdown data copies, ROMs, saves, emulator states, builds, tool binaries, screenshots, raw reports, hashes, private paths, tokens, secrets, or `.env` data are included.

## Commands

- `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`
- `python3 07_scripts/data_audit/showdown_mapping_audit.py --showdown-data-dir <external-pokemon-showdown-data-dir> --limit 50`
- `python3 -m py_compile 07_scripts/data_audit/pokemon_data_dry_run.py`
- `python3 07_scripts/data_audit/pokemon_data_dry_run.py --showdown-data-dir <external-pokemon-showdown-data-dir> --limit 8`

## Observed result

The dry-run helper completed successfully and remained read-only.

Sanitized input counts:

- Showdown `pokedex.ts`: 1517 top-level keys.
- Showdown `learnsets.ts`: 1288 top-level keys.
- Showdown `moves.ts`: 954 top-level keys.
- Showdown `abilities.ts`: 318 top-level keys.
- DPE `Base_Stats.c`: 1412 species table entries.
- DPE `Learnsets.c`: 1408 level-up pointer table entries.
- CFRU `level_up_learnsets.c`: 1412 level-up pointer table entries.
- DPE `Egg_Moves.c`: 437 egg-move species blocks.
- DPE TM compatibility text files: 128.
- DPE tutor compatibility text files: 152.

Mapping gate:

- Species: `0` Showdown uncategorized, `0` local uncategorized, blocked by `29` Species `open-risk/open-risk` entries.
- Moves: `0` Showdown uncategorized, `0` local uncategorized, blocked by `13` `open-risk/lgpe-partner-move` and `1` `open-risk/missing-engine-move`.
- Abilities: `0` Showdown uncategorized, `0` local uncategorized, blocked by `13` `behavior-risk/alias-plus-hook`, `5` `behavior-risk/behavior-risk`, `3` `behavior-risk/name-mismatch`, and `8` `open-risk/missing-local`.

Data-block result:

- Base Stats: blocked by Species open-risk.
- Ability Assignments: blocked by Species open-risk and Ability behavior/open risks.
- Level-up Learnsets: blocked by Species open-risk and Move open-risk.
- Egg Moves: blocked by Species open-risk and Move open-risk.
- TM Compatibility: blocked by Species open-risk and Move open-risk.
- Tutor Compatibility: blocked by Species open-risk and Move open-risk.

## Caveats

This is a dry-run gate smoke, not a data update. `BLOCKED_BY_REVIEWED_POLICY` is the expected safe result until the listed open-risk and behavior-risk entries are resolved or explicitly excluded.

No raw report was committed. No Pokemon Showdown data was copied into the repo.
