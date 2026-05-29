# Pokemon Data Showdown Mapping Audit - Local-Only Smoke

Date: 2026-05-29

Branch: `analysis/pokemon-data-showdown-mapping-audit`

Result: `PASS_LOCAL_ONLY_AUDIT_HELPER_SMOKE_WITH_CAVEATS`

## Scope

This is a sanitized local-only smoke for `07_scripts/data_audit/showdown_mapping_audit.py`.

No Pokemon Showdown checkout was supplied. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data was read into the report or changed.

## Command

```sh
python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20
```

## Observed Summary

- Species: CFRU `1415`, DPE `1415`, local-only drift limited to Ogerpon Terastal form names.
- Moves: CFRU `993`, DPE `993`, no CFRU-vs-DPE local constant drift found.
- Abilities: CFRU `289`, DPE `288`, with CFRU-only `EVAPORATE` / `LINGERINGAROMA`, DPE-only `UNUSED`, and same value `0x4D` named differently.
- Ability aliases: `67` total alias define rows across the two local headers.

## Caveats

- This smoke proves only that the helper parses local constants and reports local CFRU/DPE drift.
- It does not prove Pokemon Showdown coverage because no external Showdown `data/` directory was supplied.
- It does not validate Pokemon data correctness, move behavior, ability behavior, generated learnsets, TM/Tutor compatibility, local build success, BizHawk/Tracker behavior, full-playthrough coverage or P1 support.
