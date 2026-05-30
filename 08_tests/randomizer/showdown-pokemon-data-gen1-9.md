# Pokemon Showdown Pokemon Data Gen1-9 Sync

Status: `PASS_LOCAL_BUILD_BOOT_SMOKE_WITH_REVIEWED_BLOCKERS`

Branch:

- Workspace: `data/showdown-pokemon-data-gen1-9`
- DPE: `data/showdown-pokemon-data-gen1-9`
- CFRU: `data/showdown-pokemon-data-gen1-9`

Pinned commits:

- DPE: `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`
- CFRU: `8c2d69b48aee8923098912ee06c188d3db93d231`

## Scope

Synced Pokemon Showdown Gen1-9 data into local DPE/CFRU tables through a fail-closed helper:

- DPE `src/Base_Stats.c`
- DPE `src/Learnsets.c`
- CFRU `src/Tables/level_up_learnsets.c`

Allowed DPE Base Stats fields were limited to:

- `baseHP`, `baseAttack`, `baseDefense`, `baseSpAttack`, `baseSpDefense`, `baseSpeed`
- `type1`, `type2`
- `genderRatio`
- `eggGroup1`, `eggGroup2`
- `ability1`, `ability2`, `hiddenAbility`

Fields intentionally not updated from Showdown:

- Catch Rate
- EXP Yield / Base EXP
- EV Yield
- Growth Rate
- Held items
- Egg cycles / friendship / safari flee / body color / no flip
- Egg moves
- TM/HM compatibility
- Tutor compatibility
- Move behavior or Ability behavior

## Helper

Added `07_scripts/data_audit/showdown_pokemon_data_sync.py`.

The helper reads an external Pokemon Showdown `data/` checkout, local CFRU/DPE constants, and `07_scripts/data_audit/showdown_aliases.json`. It writes only when `--write` is passed.

Fail-closed behavior:

- Species `open-risk` and reviewed ignores are not updated.
- Move `open-risk` / ignored mappings block that species learnset.
- Ability `behavior-risk`, `open-risk`, `name-mismatch`, or blocked generator policy prevents that Ability slot from being updated.
- Unmapped or ambiguous Species do not get updated.
- Ogerpon Terastal aliases are resolved source-backed across DPE/CFRU's different local names for the same IDs.

No Pokemon Showdown data files or raw reports are committed.

## Results

Final post-write dry-runs for all generations reported `base_species_with_changes: 0` and `base_field_changes: 0`.

| Gen | Showdown Species | Mapped Species | Ready Learnsets | Blocking Notes |
| --- | ---: | ---: | ---: | --- |
| 1 | 238 | 227 | 197 | Missing Showdown form learnsets, Ally Switch move risk, reviewed ignores |
| 2 | 116 | 113 | 107 | Missing Mega-form learnsets, reviewed ignores |
| 3 | 167 | 162 | 136 | 1 Ability blocker, missing Mega/form learnsets, Ally Switch move risk |
| 4 | 147 | 141 | 110 | 1 Ability blocker, missing form learnsets, Ally Switch move risk |
| 5 | 189 | 179 | 163 | 1 Ability blocker, Basculin open-risk forms, missing form learnsets |
| 6 | 105 | 86 | 79 | Pumpkaboo/Gourgeist/Greninja form risks, missing form learnsets |
| 7 | 136 | 119 | 95 | 1 Ability blocker, Rockruff Dusk form risk, missing form learnsets |
| 8 | 135 | 130 | 102 | 8 Ability blockers, Sinistea/Polteageist/Alcremie/Basculegion form risks |
| 9 | 147 | 136 | 120 | 32 Ability blockers, Tatsugiri/Ogerpon mask form risks, missing form learnsets |

Aggregate learnset validation:

- Ready learnsets checked: `1109`
- DPE/CFRU expected-output drift among ready learnsets: `0`

Data commits:

- DPE Gen1-9 commits: `916aa1a`, `c23fcf7`, `aa0fe9f`, `8d6f268`, `325610d`, `5835c17`, `5ab0dd5`, `b193aee`, `22ffa27`
- CFRU Gen1-8 learnset commits: `27d78a69`, `2b517691`, `b102c2d1`, `79da5db0`, `2d2756a2`, `f1c63b89`, `21887ce4`, `e9fac6db`
- CFRU learnset syntax repair commit: `8c2d69b`
- Gen9 produced no CFRU learnset diff.

## Local Build / Boot Smoke

Sanitized local smoke after the CFRU learnset syntax repair:

| Check | Result |
| --- | --- |
| DPE build | Pass |
| CFRU build on new DPE ROM | Pass |
| mGBA boot | Pass |
| No crash before first gameplay | Pass |
| CFRU learnset syntax repair included | Pass |

This is a targeted local build/boot smoke only. It does not include ROM paths, saves, emulator states, screenshots, raw logs, hashes, private paths, full-playthrough coverage, BizHawk validation, Ironmon Tracker validation, or P1 support promotion.

## Checks

Passed:

- `python3 -m py_compile 07_scripts/data_audit/showdown_pokemon_data_sync.py`
- `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`
- Per-generation helper dry-runs after writes, Gen1-9
- Aggregate DPE/CFRU learnset expected-output drift check
- DPE `git diff --check`
- CFRU `git diff --check`
- Workspace `git diff --check`
- Local DPE build
- Local CFRU build on the new DPE ROM
- Local mGBA boot
- Local no-crash-before-first-gameplay smoke

Not run:

- BizHawk validation
- Ironmon Tracker validation
- Full playthrough

## Risks And Blockers

Remaining blockers are intentional and visible:

- Ability behavior risk remains the main Gen9 blocker. Several newer Ability names exist locally but alias to older effects or source-backed partial hooks.
- Ally Switch and Let's Go-style moves remain Move behavior risks and do not promote learnsets.
- Open-risk form families remain blocked: Alcremie, Basculin/Basculegion, Pumpkaboo/Gourgeist sizes, Sinistea/Polteageist antique/chipped naming, Rockruff Dusk, Tatsugiri forms, and Ogerpon mask-vs-form rows.
- GMax/Mega/cosmetic forms often lack separate Showdown level-up learnset blocks and are not forced.

## Handoff

Recommended local smoke path:

1. Rebuild DPE/CFRU from the pinned DPE and CFRU commits.
2. Boot a local ROM candidate and check Pokemon data table loading around representative Gen1, Gen5, Gen8, and Gen9 species.
3. Spot-check Ability assignment behavior only as display/data presence unless the relevant Ability has source-backed behavior coverage.
4. Spot-check level-up learnsets for a few changed species in DPE and CFRU.
5. Keep the result scoped as targeted build/boot/data smoke unless broader gameplay evidence is collected.

Do not claim P1 support, full-playthrough coverage, BizHawk compatibility, or Ironmon Tracker compatibility from this data sync alone.
