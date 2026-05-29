# Tool Manifest Update - 2026-05-29 - DPE Base Stats Gen9 tranche 1 plan

- Workspace branch: `analysis/dpe-base-stats-gen9-tranche-1-plan`.
- Analysis file: `01_docs/analysis/dpe-base-stats-gen9-tranche-1-plan.md`.
- Smoke file: `08_tests/randomizer/dpe-base-stats-gen9-tranche-1-plan.md`.
- Scope: documentation-only planning for the first real DPE `Base_Stats.c` update tranche from the read-only dry-diff.
- Helper used read-only: `07_scripts/data_audit/dpe_base_stats_dry_diff.py`.
- Recommended tranche 1 candidates: Sneasel-Hisui, Sneasler, Ursaluna, Toedscool, Toedscruel, Primarina, Brionne, Sylveon, Magnezone, and Crobat.
- Local smoke commands: dry-diff helper against the external Pokemon Showdown `data/` directory with `--limit 25`; `python3 -m py_compile 07_scripts/data_audit/dpe_base_stats_dry_diff.py`.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - DPE Base Stats Gen9 safe dry diff

- Workspace branch: `analysis/dpe-base-stats-gen9-safe-dry-diff`.
- Added read-only helper: `07_scripts/data_audit/dpe_base_stats_dry_diff.py`.
- Analysis file: `01_docs/analysis/dpe-base-stats-gen9-safe-dry-diff.md`.
- Smoke file: `08_tests/randomizer/dpe-base-stats-gen9-safe-dry-diff.md`.
- Scope: sanitized DPE Base Stats dry-diff against external Pokemon Showdown `pokedex.ts`.
- Helper inputs: external Pokemon Showdown `data/` directory, `07_scripts/data_audit/showdown_aliases.json`, `07_scripts/data_audit/showdown_mapping_audit.py`, and local DPE `src/Base_Stats.c` read-only.
- Dry-diff status: `PASS_READ_ONLY_WITH_BLOCKERS`; `1317` tested Species, `29` Species `open-risk` skipped, `167` reviewed Species ignores skipped, `65` Ability-blocked Species skipped from safe candidate promotion, `4` missing local entries after alias/ignore handling, and `225` safe candidate Species with non-Ability field diffs.
- Local smoke commands: `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`; `python3 07_scripts/data_audit/pokemon_data_dry_run.py --showdown-data-dir <external-pokemon-showdown-data-dir>`; `python3 -m py_compile 07_scripts/data_audit/dpe_base_stats_dry_diff.py`; dry-diff helper against the external Pokemon Showdown `data/` directory with `--limit 10`.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon data generator dry-run plan

- Workspace branch: `analysis/pokemon-data-generator-dry-run-plan`.
- Added read-only helper: `07_scripts/data_audit/pokemon_data_dry_run.py`.
- Analysis file: `01_docs/analysis/pokemon-data-generator-dry-run-plan.md`.
- Smoke file: `08_tests/randomizer/pokemon-data-generator-dry-run-plan.md`.
- Scope: fail-closed dry-run planning for future Pokemon Showdown-to-CFRU/DPE data generator work.
- Helper inputs: external Pokemon Showdown `data/` directory, `07_scripts/data_audit/showdown_aliases.json`, local constants through `showdown_mapping_audit.py`, and local DPE/CFRU table-shape files.
- Dry-run status: `BLOCKED_BY_REVIEWED_POLICY`; uncategorized Species/Move/Ability key counts are 0, while reviewed Species `open-risk`, Move `open-risk`, and Ability `behavior-risk` / `open-risk` entries block all planned data blocks.
- Local smoke commands: `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`; full comparison against an external Pokemon Showdown `data/` directory with `--limit 50`; `python3 -m py_compile 07_scripts/data_audit/pokemon_data_dry_run.py`; dry-run helper against the external Pokemon Showdown `data/` directory.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon data species alias table final

- Workspace branch: `analysis/pokemon-data-species-alias-table-final`.
- Alias table: `07_scripts/data_audit/showdown_aliases.json`.
- Analysis file updated: `01_docs/analysis/pokemon-data-reviewed-alias-table.md`.
- Smoke file updated: `08_tests/randomizer/pokemon-data-reviewed-alias-table.md`.
- Scope: Species-only final classification of remaining Pokemon Showdown-to-CFRU/DPE unresolved Species/Form keys.
- Added explicit local-shortform, GMax/Giga, cosmetic-form, fan-ignore, local-extra, and blocking open-risk Species entries.
- Alias table status: 471 entries total; external Species buckets now classify 319 Showdown-only Species keys and 221 local-only Species keys with 0 still uncategorized.
- Local smoke commands: `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`; full comparison against an external Pokemon Showdown `data/` directory with `--limit 50`; `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py`.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon data ability risk table final

- Workspace branch: `analysis/pokemon-data-ability-risk-table-final`.
- Alias table: `07_scripts/data_audit/showdown_aliases.json`.
- Analysis file updated: `01_docs/analysis/pokemon-data-reviewed-alias-table.md`.
- Smoke file updated: `08_tests/randomizer/pokemon-data-reviewed-alias-table.md`.
- Scope: Ability-only final classification of remaining Pokemon Showdown-to-CFRU/DPE unresolved Ability keys.
- Added explicit legacy `intentionally-merged` entries, blocking `behavior-risk` / `alias-plus-hook` / `name-mismatch` entries, `open-risk` missing-local entries, Showdown Future/CAP non-project ignores, and sentinel-only `noability` handling.
- Alias table status: 239 entries total; external Ability buckets now classify 36 Showdown-only Ability keys and 8 local-only Ability keys with 0 still uncategorized.
- Local smoke commands: `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`; full comparison against an external Pokemon Showdown `data/` directory with `--limit 50`; `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py`.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon data ability risk table

- Workspace branch: `analysis/pokemon-data-ability-risk-table`.
- Alias table: `07_scripts/data_audit/showdown_aliases.json`.
- Analysis file updated: `01_docs/analysis/pokemon-data-reviewed-alias-table.md`.
- Smoke file updated: `08_tests/randomizer/pokemon-data-reviewed-alias-table.md`.
- Scope: Ability-only encoding of the source-backed CFRU/DPE Ability behavior-risk audit into the reviewed Pokemon Showdown-to-CFRU/DPE alias/ignore table.
- Added blocking Ability risk classifications for alias-plus-hook behavior, unresolved behavior risk, missing local support, and name mismatch; added explicit non-blocking legacy merges and local-only ignores.
- Alias table status: 215 entries total; Ability categories include `alias-plus-hook` 12, `behavior-risk` 4, `name-mismatch` 1, `missing-local` 7, `intentionally-merged` 2, and `local-only` 5.
- Local smoke commands: `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`; full comparison against an external Pokemon Showdown `data/` directory with `--limit 50`; `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py`.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon ability behavior risk audit

- Workspace branch: `analysis/pokemon-ability-behavior-risk-audit`.
- Analysis file: `01_docs/analysis/pokemon-ability-behavior-risk-audit.md`.
- Smoke file: `08_tests/randomizer/pokemon-ability-behavior-risk-audit.md`.
- Scope: read-only source audit of CFRU/DPE Ability constants, alias defines, display strings, DPE Base Stats assignments, and CFRU battle behavior hooks for Gen9/newer Ability names.
- Source search covered CFRU `include/constants/abilities.h`, `strings/ability_name_table.string`, `strings/ability_descriptions.string`, `assembly/data/ability_tables.json`, `src/ability_battle_effects.c`, `src/ability_util.c`, `include/new/ability_tables.h`, and additional behavior-hook files found by `rg`; DPE `include/abilities.h` and `src/Base_Stats.c`.
- Status impact: Ability behavior policy now has source-backed categories for alias-plus-hook behavior, partial alias behavior, alias-only risk, display/definition risk, and missing local support.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon data alias table move final

- Workspace branch: `analysis/pokemon-data-alias-table-move-final`.
- Alias table: `07_scripts/data_audit/showdown_aliases.json`.
- Analysis file updated: `01_docs/analysis/pokemon-data-reviewed-alias-table.md`.
- Smoke file updated: `08_tests/randomizer/pokemon-data-reviewed-alias-table.md`.
- Scope: Move-only final classification of remaining Pokemon Showdown-to-CFRU/DPE unresolved Move keys.
- Added `open-risk` entries for Ally Switch and Let's Go partner moves, plus explicit ignores for CAP/Future Showdown moves and local helper/project constants.
- Alias table status: 191 entries total; Move unresolved audit buckets now classify 104 Showdown-only Move keys and 143 local-only Move keys with 0 still uncategorized.
- Local smoke commands: `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`; full comparison against an external Pokemon Showdown `data/` directory with `--limit 50`; `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py`.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon data alias table move splits

- Workspace branch: `analysis/pokemon-data-alias-table-move-splits`.
- Alias table: `07_scripts/data_audit/showdown_aliases.json`.
- Analysis file updated: `01_docs/analysis/pokemon-data-reviewed-alias-table.md`.
- Smoke file updated: `08_tests/randomizer/pokemon-data-reviewed-alias-table.md`.
- Scope: Move-only expansion of the reviewed Pokemon Showdown-to-CFRU/DPE alias/ignore table.
- Added explicit reviewed Z-Move, Max Move, and G-Max Move physical-special split aliases with local `P`/`S` constants.
- Alias table status: 169 entries total; Move `split-move` 69.
- Local smoke commands: `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`; full comparison against an external Pokemon Showdown `data/` directory with `--limit 50`; `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py`.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon data alias table batch 2

- Workspace branch: `analysis/pokemon-data-alias-table-batch-2`.
- Alias table: `07_scripts/data_audit/showdown_aliases.json`.
- Analysis file updated: `01_docs/analysis/pokemon-data-reviewed-alias-table.md`.
- Smoke file updated: `08_tests/randomizer/pokemon-data-reviewed-alias-table.md`.
- Scope: Species-only expansion of the reviewed Pokemon Showdown-to-CFRU/DPE alias/ignore table.
- Added explicit reviewed aliases for regional/local shortforms using Alola `A`, Galar `G`, Hisui `H`, and Paldea `P`, plus the remaining reviewed GMax/Giga Species aliases.
- Alias table status: 107 entries total; Species `gmax-giga` 32 and Species `local-shortform` 55.
- Local smoke commands: `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`; full comparison against an external Pokemon Showdown `data/` directory with `--limit 50`; `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py`.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon data reviewed alias table

- Workspace branch: `analysis/pokemon-data-reviewed-alias-table`.
- Analysis file: `01_docs/analysis/pokemon-data-reviewed-alias-table.md`.
- Smoke file: `08_tests/randomizer/pokemon-data-reviewed-alias-table.md`.
- Alias table: `07_scripts/data_audit/showdown_aliases.json`.
- Updated helper: `07_scripts/data_audit/showdown_mapping_audit.py`.
- Tool purpose update: the read-only Pokemon Showdown mapping audit now loads a reviewed alias/ignore table, reports category counts, and classifies unresolved Showdown/local Species, Move and Ability keys while keeping still-uncategorized keys visible.
- Initial alias coverage: Ogerpon Terastal form aliases, GMax/Giga Species examples, regional/local shortform examples, Z/Max/GMax physical-special Move split aliases, Hidden Power typed-variant ignore pattern, `visegrip` to `vicegrip`, and Ability aliases as explicit behavior risks.
- Local smoke commands: `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`; full comparison against an external Pokemon Showdown `data/` directory with `--limit 50`; `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py`.
- Boundary: no Pokemon Showdown data is vendored; no raw reports, CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon data Showdown mapping audit

- Workspace branch: `analysis/pokemon-data-showdown-mapping-audit`.
- Analysis file: `01_docs/analysis/pokemon-data-showdown-mapping-audit.md`.
- Smoke file: `08_tests/randomizer/pokemon-data-showdown-mapping-audit.md`.
- Added read-only helper: `07_scripts/data_audit/showdown_mapping_audit.py`.
- Tool purpose: parse local CFRU/DPE Species, Move and Ability constants; report CFRU-vs-DPE drift; report Ability alias defines; optionally compare normalized keys against an external Pokemon Showdown `data/` directory containing `pokedex.ts`, `moves.ts`, and `abilities.ts`.
- Local-only smoke command: `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`.
- Local-only status: helper ran successfully without Showdown input; Species Ogerpon form-name drift, Ability `0x4D` drift and Ability aliases are documented; Moves showed no local CFRU/DPE constant-name drift.
- Boundary: no Pokemon Showdown data is vendored; no CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - Pokemon data Gen9 inventory

- Workspace branch: `analysis/pokemon-data-gen9-inventory`.
- Analysis file: `01_docs/analysis/pokemon-data-gen9-inventory.md`.
- Scope: documentation-only inventory of CFRU/DPE Pokemon data table ownership, format, risk and update sequencing.
- Local source references: CFRU `src/Tables/level_up_learnsets.c`, `src/Tables/battle_moves.c`, `src/item.c`, `src/learn_move.c`, `include/constants/species.h`, `include/constants/moves.h`, `include/constants/abilities.h`, `include/constants/tutors.h`, and related strings/JSON table metadata; DPE `src/Learnsets.c`, `src/Base_Stats.c`, `src/TM_Tutor_Tables.c`, `src/Egg_Moves.c`, `include/species.h`, `include/moves.h`, `include/abilities.h`, `include/base_stats.h`, `src/tm_compatibility/*.txt`, and `src/tutor_compatibility/*.txt`.
- External read-only references checked: Pokemon Showdown data directory, pokeemerald-expansion Pokemon data directory, Shiny-Miner fork/account references, Skeli789 CFRU upstream family reference, and Shiny-Miner DPE Gen 9.
- Status impact: establishes Pokemon Showdown as the preferred machine-readable audit input, pokeemerald-expansion as the GBA-shape comparison reference, and CFRU/DPE upstreams as the format/engine references.
- Boundary: no CFRU, DPE, UPR-FVX, submodule pin, external download, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - CFRU Randomizer baseline config local smoke

- Workspace branch: `feature/cfru-randomizer-baseline-config`.
- Evidence file: `08_tests/randomizer/cfru-randomizer-baseline-config.md`.
- Scope: sanitized local build / mGBA smoke result for the existing CFRU Randomizer Baseline Config candidate.
- Status impact: `PASS_TARGETED_LOCAL_BUILD_BOOT_SETTINGS_SMOKE_WITH_CAVEATS`.
- Local reported evidence: CFRU commit `53273184bab06f91cdc3ad6e0e5af4a8ba41591a` was synchronized into the local Mac build workspace, a local clean rebuild completed, `wav2agb` / `mid2agb` were resolved through local `local-bin` wrappers, the local ROM candidate booted in mGBA, and the new/adjusted in-game settings worked.
- Smoke matrix: Build/Boot pass, Options/Settings pass, Nuzlocke Toggle pass, Wild Prebattle Toggle pass; Oak Tutorial removed, Poison Overworld Faint, SwSh Catch-Level-Malus off, Old/Flat EXP, and Intro Controls Guide skipped remain inconclusive pending separate sanitized evidence.
- Boundary: documentation-only update; no CFRU code, UPR-FVX, DPE, submodule pin, full-playthrough, BizHawk, Ironmon Tracker or P1 support claim is included.
- Safety: no ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, ROM hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-29 - CFRU Randomizer baseline config

- Workspace branch: `feature/cfru-randomizer-baseline-config`.
- CFRU branch: `feature/cfru-randomizer-baseline-config`.
- CFRU base commit: `74310deeb62c7f73ba6c7b11f921418617a9a740`.
- Workspace submodule `02_external/CFRU-expansion` now pins CFRU baseline commit `53273184bab06f91cdc3ad6e0e5af4a8ba41591a`.
- Scope: narrow CFRU Randomizer-/Ironmon-near baseline config plus source-backed option-menu flag toggles.
- Compile-time config: `TUTORIAL_BATTLES` disabled, `POISON_1_HP_SURVIVAL` disabled, `SWSH_CATCHING_DIFFICULTY_MODIFIER` disabled, `OLD_EXP_SPLIT` enabled, `FLAT_EXP_FORMULA` enabled, and `SKIP_INTRO_CONTROLS_GUIDE` enabled.
- `IgnoreWildPokemon` remains enabled because source search shows it compiles the prebattle feature and runtime generation remains gated by `FLAG_ENABLE_WILD_PMN_PREBATTLE_SCREEN`.
- Runtime toggles: Page 3 `Nuzlocke = Off/On` clears/sets only `FLAG_NUZLOCKE`; Page 3 `Wild Prebattle = Off/On` clears/sets only `FLAG_ENABLE_WILD_PMN_PREBATTLE_SCREEN`.
- `FLAG_WILD_POKEMON_PREBATTLE_SCREEN` remains transient encounter/window state and is not menu-owned.
- Evidence file: `08_tests/randomizer/cfru-randomizer-baseline-config.md`.
- Checks: CFRU `diff --check` passed; `arm-none-eabi-gcc -fsyntax-only src/option_menu.c` passed; workspace `diff --check` passed.
- Boundary: no UPR-FVX, DPE, Trainer AI, Trainer Level Scaling, Hard Cap, Difficulty logic, Wild Encounter Tables, Randomizer code, ROM build, emulator boot, full-playthrough, BizHawk, Ironmon Tracker or P1 support claim is included.
- Safety: no ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, ROM hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-28 - Trainer AI Policy v3 local smoke

- Workspace branch: `experiment/trainer-ai-policy-v3`.
- Evidence file: `08_tests/randomizer/trainer-ai-policy-v3.md`.
- Scope: sanitized local mGBA smoke result for the existing CFRU Trainer-AI-Policy v3 experiment.
- Status impact: `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`.
- Local reported evidence: CFRU Trainer-AI-Policy v3 built locally, the local ROM candidate booted in mGBA, `Trainer AI` option values were selectable and appeared to save, the Rival Smokescreen / move-choice smoke passed with caveats, and `Smart` / `Hard` / `Expert` appeared distinguishable.
- Interpretation: `Smart` appeared to activate Full Smart Move-AI; `Hard` appeared to add stronger fair reactions without obvious hidden-knowledge behavior; `Expert` appeared to be the strongest plausible advanced profile.
- Boundary: documentation-only update; no CFRU code, UPR-FVX, DPE, submodule pin, full-playthrough, BizHawk, Ironmon Tracker, statistical AI-quality or P1 support claim is included.
- Safety: no ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, ROM hash, private path, token, secret or `.env` data is included.

# Tool Manifest Update - 2026-05-28 - Trainer AI Policy v3 experiment

- Workspace branch: `experiment/trainer-ai-policy-v3`.
- CFRU branch: `experiment/trainer-ai-policy-v3`.
- CFRU base commit: `caaf81b2582d5af0905281aab88658ac145b43eb`.
- Workspace submodule `02_external/CFRU-expansion` now pins CFRU experiment commit `74310deeb62c7f73ba6c7b11f921418617a9a740`.
- Scope: narrow Trainer-AI policy update in CFRU. `Smart`, `Hard`, and `Expert` trainer AI profiles receive full smart move AI for trainer battles through `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`.
- Policy split: `Smart` is move-AI-only; `Hard` adds fair anti-cheese / Protect-Fake-Out retarget behavior without switch prediction, shift-switching, bench/prediction behavior or type-resist berry hidden knowledge; `Expert` keeps the advanced Expert AI gates.
- Additional CFRU file rationale: `src/damage_calc.c` was changed because the requested `rg` search found the existing Expert type-resist berry knowledge gate there, and the policy requires `Smart`/`Hard` to avoid hidden berry knowledge.
- Status impact: implementation is ready for targeted local mGBA A/B smoke, documented in `08_tests/randomizer/trainer-ai-policy-v3.md`.
- Boundary: no `VAR_GAME_DIFFICULTY` broad effects, trainer level scaling, IV/EV/friendship/PP logic, bag/move restrictions, wild/raid/DexNav/ability-capsule logic, `AI_TRY_TO_KILL_RATE`, UPR-FVX or DPE changes are included.
- Safety: no ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, ROM hash, private path, token, secret, `.env` data, UPR-FVX/DPE change, full-playthrough claim or P1 promotion is included.

# Tool Manifest Update - 2026-05-28 - Trainer AI Smokescreen behavior analysis

- Workspace branch: `analysis/trainer-ai-smokescreen-behavior`.
- Added source-backed analysis file `01_docs/analysis/trainer-ai-smokescreen-behavior.md`.
- Scope: documentation-only review of current CFRU Trainer AI profile plumbing, Smart Trainer AI v2 behavior, Accuracy-down scoring, and NatDex/Ironmon Smart-AI reference semantics.
- Sanitized local observation documented: Rival trainer battle with an opposing Pokemon that had `Tackle` + `Smokescreen`; `Smokescreen` was repeatedly selected until player Accuracy reached minimum.
- Status impact: behavior is classified as plausible but suspicious pending local mGBA A/B smoke across Trainer AI `Auto`, `Vanilla`, `Normal`, `Hard`, `Expert`, and `Smart`.
- Safety: no CFRU, DPE, UPR-FVX or Tracker code change; no ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret, `.env` data, external repo change or submodule repin is included.

# Tool Manifest Update - 2026-05-28 - MacBook rebuild success

- Workspace branch: `docs/macbook-rebuild-success`.
- Workspace submodule `02_external/upr-fvx` is confirmed at commit `1a597a667129b50284dd88afb231372b5bd01d7f` on the local compat branch.
- UPR-FVX local build command confirmed: `./gradlew clean :random:jar`.
- UPR-FVX GUI starts locally with Java 25.
- Local GBA toolchain confirmed present: devkitPro/devkitARM, `arm-none-eabi-gcc` 15.2.0, `gbafix`, `grit`, and GNU Make 4.4.1.
- Local audio conversion wrappers confirmed present: Wine wrappers for `wav2agb.exe` and `mid2agb.exe`.
- Local DPE and CFRU rebuilds completed successfully.
- Final local CFRU+DPE Gen9 ROM candidate loads in UPR-FVX and boots in mGBA.
- Status impact: the MacBook workspace is rebuilt to a usable local UPR-FVX + CFRU/DPE + mGBA smoke baseline; BizHawk and Ironmon Tracker remain open.
- Safety: no ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, ROM hash, private path, token, secret, `.env` data, external repo change or submodule repin is included in this workspace update.

# Tool Manifest Update - 2026-05-25 - Tracker source references

- Workspace branch: `setup/tracker-source-references`.
- Added read-only source submodule reference `02_external/Ironmon-Tracker` on branch `main` at commit `c450ecaee2d8131a2789bb656e3be792a93712fb`.
- Added read-only source submodule reference `02_external/NatDexExtension` on branch `dev_new` at commit `a94b8844800308248bb5090b6c36c8b2d7e5d7b9`.
- Central Tracker API analysis source: `02_external/Ironmon-Tracker/ironmon_tracker/TrackerAPI.lua`, corresponding to the project shorthand `IronmonTrackerAPI.lua`.
- BizHawk remains a local tool target only. No BizHawk source submodule, release zip, AppImage, build output or binary is added to the repo.
- Safety: no ROMs, saves, emulator states, builds, tool binaries, screenshots, raw logs, hashes, private paths, secrets, tokens or `.env` data were read or documented.

# Tool Manifest Update - 2026-05-24 - CFRU Smart Trainer AI v2 utility-spam reduction

- CFRU fork base branch: `fix/cfru-smart-trainer-ai-v2-reduce-utility-spam`.
- Workspace submodule `02_external/CFRU-expansion` now pins CFRU commit `992d3dc6a8db33b3c633dd4d504c40fb6efe37d1`.
- Scope: reduces the project-local `FLAG_SMART_TRAINER_AI` trainer-only `GetAIFlags` hook from `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE` to `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`.
- Status impact: v2 keeps Normal Difficulty and tests a more conservative CFRU-native Smart Trainer AI path after v1 local smoke showed utility/Accuracy-drop spam.
- Boundary: no `VAR_GAME_DIFFICULTY`, wild/raid AI, trainer IV/EV/friendship/PP, level-scaling, bag/move restriction, battle-rule, Option Menu, Settings NPC, DPE or UPR-FVX code change was included.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented and no build artifact committed.

# Tool Manifest Update - 2026-05-24 - CFRU Smart Trainer AI smoke confirmation

- CFRU fork base branch: `feature/cfru-smart-trainer-ai-smoke-script`.
- Workspace submodule `02_external/CFRU-expansion` now pins CFRU commit `b0b750faa66700dfb923b76e6302291ca248193e`.
- Scope: adds a visible Pallet smoke confirmation after `FLAG_SMART_TRAINER_AI` activation: `Smart Trainer AI enabled.`
- Status impact: local testers can visually confirm the flag-on smoke path before entering sampled trainer battles.
- Boundary: this is not final player UX. No Settings NPC, Option Menu, toggle, randomizer-profile wiring, `VAR_GAME_DIFFICULTY`, Battle AI, trainer-build, level-scaling, wild/raid AI, bag/move restriction, battle-rule, Expert anti-cheese, shift-switch, DPE or UPR-FVX code change was included.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented and no build artifact committed.

# Tool Manifest Update - 2026-05-24 - CFRU Smart Trainer AI smoke activation

- CFRU fork base branch: `feature/cfru-smart-trainer-ai-smoke-script`.
- Workspace submodule `02_external/CFRU-expansion` now pins CFRU commit `8f909da1abef6adabbfccf8767544924d114b287`.
- Scope: adds a local smoke activation line to `EventScript_Pallet_FatGuy` in `assembly/overworld_scripts/Pallet_town.s`, setting `0xA0E` for `FLAG_SMART_TRAINER_AI`.
- Status impact: local testers can run Normal Difficulty with the flag off by not triggering the Pallet test script, or flag on by triggering the existing Pallet test script once before sampled trainer battles.
- Boundary: this is not final player UX. No Settings NPC, Option Menu, randomizer-profile wiring, `VAR_GAME_DIFFICULTY`, trainer-build, level-scaling, wild/raid AI, bag/move restriction, battle-rule, Expert anti-cheese, shift-switch, DPE or UPR-FVX code change was included.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented and no build artifact committed.

# Tool Manifest Update - 2026-05-24 - CFRU Smart Trainer AI runtime flag

- CFRU fork base branch: `feature/cfru-smart-trainer-ai-mode`.
- Workspace submodule `02_external/CFRU-expansion` now pins CFRU commit `eb1f3bff3fef83b46999e0513a7598b6bde601b8`.
- Scope: adds project-local runtime flag `FLAG_SMART_TRAINER_AI 0xA0E` and a trainer-only `GetAIFlags` hook that ORs trainer AI flags with `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`.
- Status impact: v1 Smart Trainer AI only is source-available for scripts or later integration wiring; no UI, NPC, option-menu or randomizer-profile toggle is included.
- Boundary: `VAR_GAME_DIFFICULTY` remains unchanged; no trainer IV/EV/friendship/PP, level-scaling, wild/raid AI, bag/move restriction, battle-rule, Expert anti-cheese or shift-switch logic was added.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented and no DPE or UPR-FVX code change.

# Tool Manifest Update - 2026-05-20 - Gen Limit Special Form Mechanic Item final smoke

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #150: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/150>.
- UPR-FVX PR #151: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/151>.
- UPR-FVX PR #152: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/152>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX compat commit `8349daf5ce005f0defc5674cbc3a3468f009218c`.
- Scope: final merged Gen-Limit 1-9, species pool restriction, Gen7/8/9 Intro Mon visual-candidate, Special-Form filtering/settings/GUI, regional/evolution-relative separation, Trainer Class Sprite Sync GUI, Oak-Lab Rival counter-starter, source-backed CFRU/DPE mechanic item category fixes and Trainer Held Items / Sensible Items NPE guards through PR #152.
- Workspace evidence file: `08_tests/randomizer/212_gen_limit_special_form_item_smoke.md`.
- Status impact: `PASS_TARGETED_LOG_VISUAL_SMOKE_WITH_CAVEATS`; local sanitized evidence reports Gen-Limit 1-9 infrastructure pass, Gen1-only and Gen1-6 log-smoke correctness, Gen7/8/9 Intro Mon crash-free valid visual-table candidates, Special-form filtering pass in latest checks, Trainer Class Sprite Sync GUI exposure, Oak-Lab Rival counter-starter preservation, source-backed Mega/Z/Dynamax-GMax item filtering, Trainer Held Items / Sensible Items running without the earlier missing-pool or missing-movepool NPEs and no current crash in the latest GUI smoke.
- Boundary: targeted local smoke only; no full playthrough, no full held-item distribution audit, no P1 promotion, no separate user-facing policies yet for Plates/Drives/Memories/Nectars, Static Script/Gift/NPC item source caveat remains when outside replacement pools, and custom/future form encodings outside documented CFRU/DPE identity blocks remain audit-required.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-20 - Type Effectiveness battle smoke

- Workspace evidence file: `08_tests/randomizer/211_type_effectiveness_battle_smoke.md`.
- Scope: sanitized local Type Effectiveness battle smoke.
- Status impact: `PASS_TARGETED_BATTLE_SMOKE_WITH_CAVEATS`; local evidence reports Type Effectiveness tested in battle, effectiveness behavior looked appropriate and no battle crashes were reported.
- Boundary: targeted battle smoke only; no full type-chart matchup matrix, no full playthrough and no P1 promotion.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-20 - Misc Tweaks behavior smoke

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #125: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/125>.
- UPR-FVX PR #126: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/126>.
- UPR-FVX PR #127: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/127>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #127 commit `155fac0b33474f6ed5b3fbaed7dd9bf24b4e1315`.
- Scope: PR #125 fixes CFRU/DPE BPRE Running Shoes Misc Tweaks, PR #126 maps CFRU/DPE Catching Tutorial species through the valid internal species identity and PR #127 skips expanded-pool Species entries without `BreedingInfo` during Fast Egg Hatching.
- Workspace evidence file: `08_tests/randomizer/210_misc_tweaks_behavior_smoke.md`.
- Status impact: `PASS_TARGETED_BEHAVIOR_SMOKE_WITH_CAVEATS`; local sanitized evidence reports Fastest Text pass, Randomize PC Potion pass, Run Without Running Shoes pass, Running Shoes Indoors pass, Randomize Catching Tutorial pass with no question-mark sprite/name, Fast Egg Hatching crash-free randomization/output-load and Ban Lucky Egg likely pass / no issue observed.
- Boundary: targeted behavior smoke only; no full playthrough, no full hatch-cycle proof, no dedicated stronger Ban Lucky Egg proof and no P1 promotion. Reusable TMs and Forgettable HMs are CFRU-provided for the stable profile and should not be duplicated by UPR-FVX.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-20 - Graphics Palettes visual smoke

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #123: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/123>.
- UPR-FVX PR #124: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/124>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #124 commit `0eb815418470fa1ac000695b95d09cb084338dca`.
- Scope: PR #123 writes Gen3/CFRU-DPE palette randomization output; PR #124 guards expanded trainer logging bounds/fallbacks.
- Workspace evidence file: `08_tests/randomizer/209_graphics_palettes_visual_smoke.md`.
- Status impact: targeted local Graphics/Palettes visual/audit smoke passes with caveats: `Pokemon Palettes: Randomized/Changed`, `normalPaletteWriteAttempts=841`, Palette Audit `sampledCount=21`, `normalChangedCount=21`, `shinyChangedCount=0`, `unchangedCount=0`, sampled normal palettes changed from base and visible palette changes were observed. Final run had no `Error during logging`.
- Boundary: targeted smoke only, not full-playthrough coverage, broad species/form coverage, shiny behavior proof or P1 promotion.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Wild encounter output audit

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #118: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/118>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #118 commit `ed692d07bfc81405706f2b94fda06639426e6a75`.
- Scope: PR #118 adds opt-in Wild Encounter Base-vs-Output Audit tooling for Gen3/FRLG/CFRU-DPE.
- Status impact: diagnostic-only report for the modeled Gen3 base `WildPokemon` table path; no writer/randomizer behavior change and no P1 promotion.
- Follow-up boundary: CFRU/DPE special/runtime wild sources remain separate if audit results and ingame observations diverge.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Combined trainer visual runtime smoke

- Workspace evidence file: `08_tests/randomizer/208_combined_trainer_visual_runtime_smoke.md`.
- Scope: sanitized local combined trainer visual runtime smoke on the current UPR-FVX PR #117 workspace pin.
- Status impact: `PASS_WITH_CAVEATS`; Intro Mon visibly randomized; Player Charmander -> Oak-Lab Rival Squirtle and Route 22 Rival Squirtle; Route 22 Rival sprite consistent with Oak-Lab Rival sprite; Viridian Forest trainer sprites randomized; no crash/freeze observed.
- Caveat: targeted visual/runtime smoke only. Route 22 Rival non-starter Pokemon Silvally Lv9 is documented as a randomized non-starter, while the Rival starter slot stayed Squirtle.
- Boundary: targeted smoke only, not full-playthrough coverage, all-starter-choice proof or P1 promotion.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Rival counter starter and combined visual smoke

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #117: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/117>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #117 commit `5983011752273e00c402e25cc1ae1a9baca110f1`.
- Scope: PR #117 preserves/corrects Rival Carries Starter Through Game after Foe Pokemon randomization and prevents invalid Intro Mon species `0` writes in the extended CFRU/DPE BPRE pool.
- Status impact: targeted local visual smoke confirms the combined visual Rival test fixed, visible Blissey Intro Mon, Player Charmander -> Rival Squirtle, prior Trainer Class Sprite Sync visual checks still okay, and no reported crash/freeze/garbled sprite.
- Boundary: targeted smoke only, not full-playthrough coverage, all-starter-choice proof or P1 promotion.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Trainer Class Sprite Sync final smoke

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #116: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/116>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #116 commit `36dd431d059bc69eb1bee3311200e28c872c6cc9`.
- Scope: PR #116 finalizes opt-in `MODE-TRAINER-CLASS-SPRITE-SYNC` for Gen 3 Trainer Class Sprite Sync after per-trainer assignment and Rival/Friend grouped-consistency follow-ups.
- Semantics: `Randomize Trainer Names` changes only trainer personal names; `Randomize Trainer Class Names` remains legacy/textlabel-only without Sprite Sync; with Sprite Sync, class label, `trainerClass` and visible `trainerPic` follow the class assignment.
- Status impact: targeted local visual smoke confirms regular per-trainer class/sprite assignments, Rival/Friend grouped class/sprite consistency, eligible runtime-source sync participation, and no reported garbled sprite/crash.
- Boundary: targeted smoke only, not full-playthrough coverage or P1 promotion.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Trainer Class Sprite Sync

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #111: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/111>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #111 commit `4805a5a930bc97203199816222465c76de2f2150`.
- Scope: PR #111 adds opt-in `MODE-TRAINER-CLASS-SPRITE-SYNC` for Gen 3 Trainer Class Sprite Sync.
- Semantics: `Randomize Trainer Names` changes only trainer personal names; `Randomize Trainer Class Names` remains legacy/textlabel-only without Sprite Sync; with Sprite Sync, `trainerClass` and visible `trainerPic` follow the Trainer Class Names target class mapping.
- Status impact: class label / classId / pic consistency is available as an opt-in feature. Sanitized evidence so far confirms a regular trainer battle started, visible sprite changed and class/sprite sync markers appeared, but final local smoke on the merged pin remains required.
- Boundary: no ROM execution by Codex and no P1 promotion.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Intro Mon visual source fix smoke

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #109: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/109>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #109 commit `a9bb4a5f201c5078ec02fe1f2f8417695448afe9`.
- Scope: PR #109 syncs the confirmed CFRU/DPE Gen9 BPRE Intro Mon visual source by updating the Nidoran female `PokemonFrontImages` and `PokemonNormalPalettes` entries to the selected intro species' asset pointers during Intro Mon randomization.
- Status impact: local sanitized evidence confirms the visible Oak intro sprite changed away from Nidoran female, with no crash, freeze or garbled sprite observed.
- Boundary: targeted ingame smoke only; no full-playthrough claim and no P1 promotion.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Intro Mon visual source diagnostics sync

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #107: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/107>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #107 commit `a7e098a5158d824b1ddec62a286f2a6ffafce8e4`.
- Scope: PR #107 adds an opt-in Intro Mon Visual-Source diagnostic for known FRLG Intro Mon literals/pointers and optional Base-ROM vs randomized Output-ROM comparison.
- Status impact: `No Random Intro Mon` is documented as the negative GUI option; `randomizeIntroMon=true` is the active Randomize Intro Mon path; `MODE-INTRO-RANDOM` sets true; `MODE-NO-RANDOM-INTRO` and `FVX-GEN-003` set false.
- Boundary: diagnosis-only; no visible Intro Mon fix, writer change, ROM execution by Codex or P1 promotion.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Runtime source trainer randomization smoke evidence refresh

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #105: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/105>.
- Workspace submodule `02_external/upr-fvx` remains pinned to merged UPR-FVX PR #106 commit `5bb1d853f132095922be2aceef55af2878192b85`.
- Scope: this update documents PR #105 smoke evidence for generic `RUNTIME-SOURCE` trainer randomizer eligibility while keeping the PR #106 post-audit tooling pin.
- Status impact: local sanitized evidence confirms Viridian Forest trainer IDs `531/532` are loaded, randomized, saved and observed in-game; the randomized output audit reports `unloaded-valid-parties total=0`; Rival 2 `329/330/331` and Brock `414` also show randomized parties in sanitized observations.
- Follow-up scope: loaded-mismatch, invalid-pointer, empty-party, out-of-range rows and full playthrough coverage remain diagnostic/follow-up work.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Runtime trainer post-randomization audit sync

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #106: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/106>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #106 commit `5bb1d853f132095922be2aceef55af2878192b85`.
- Scope: PR #106 adds an opt-in Pre/Post Runtime-Trainer-Audit that compares a private base ROM against a private randomized output ROM.
- Status impact: local users can check valid script-referenced runtime trainer rows for base/output raw party differences, loaded output party, output classification, changed-from-base state, loaded/raw comparison and warning markers.
- Boundary: audit-only; no new writer, auto-sync or randomizer behavior.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Runtime source trainer randomization smoke

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #105: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/105>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #105 commit `c0d8e33f3547020c6fd2fe5baffbc80ec93f9197`.
- Scope: PR #105 makes generic `RUNTIME-SOURCE` trainers randomizer-eligible as regular trainers while preserving known Rival 2/Brock special tags.
- Status impact: local sanitized evidence confirms Viridian Forest trainer IDs `531/532` are loaded, randomized, saved and observed in-game for the targeted Trainer Pokemon path.
- Follow-up scope: loaded-mismatch, invalid-pointer, empty-party and out-of-range audit rows remain diagnostic/follow-up work.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Strict runtime trainer source sync

- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #104: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/104>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #104 commit `6dcda7e499cd3e22319c447c7d7df9ddbd67de60`.
- Scope: PR #104 implements strict sync for FRLG/CFRU-DPE `trainerbattle` runtime-source TrainerData rows classified as `VALID_RUNTIME_NOT_LOADED`, deduped by trainer ID and constrained to valid in-bounds rows with readable parties.
- Status impact: Trainer/Foe remains CLI-log-clean with strict sync pinned, but local private-ROM audit plus ingame smoke is still required; Viridian Forest trainer IDs `531/532` should be covered if they remain `VALID_RUNTIME_NOT_LOADED`.
- Follow-up scope: loaded-mismatch, invalid-pointer, empty-party and out-of-range audit rows remain diagnostic/follow-up work.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Runtime trainer source audit sync

- Workspace branch: `randomizer/sync-runtime-trainer-source-audit`.
- UPR-FVX PR #103: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/103>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #103 commit `14c1c8c0c6960f1b4a0cf0246a1117628ca1f3cc`.
- Scope: PR #103 adds an opt-in global FRLG trainer runtime-source audit to the existing trainer runtime-source diagnostics.
- Audit enablement: system property `uprfvx.trainerRuntimeSourceAudit` or env `UPRFVX_TRAINER_RUNTIME_SOURCE_AUDIT`.
- Audit modes: `all`, `unloaded-valid-parties`, `loaded-mismatch` and `invalid`.
- Status impact: the audit can classify script-referenced trainer IDs as runtime-not-loaded, loaded/runtime match, loaded/runtime mismatch, invalid pointer, empty party, out-of-range or likely false positive. This is audit-only and does not add any automatic sync/write behavior.
- Follow-up rule: additional trainer runtime-source fixes must wait for sanitized local audit evidence proving specific valid in-game runtime rows.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-19 - Runtime trainer party fix sync

- Workspace branch: `randomizer/sync-runtime-trainer-party-fix`.
- UPR-FVX PR #102: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/102>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #102 commit `eabbcd7eccb1703f98000f85669d969f516e1247`.
- Scope: PR #102 fixes the confirmed CFRU/DPE FireRed Trainer Pokemon runtime-source mismatch for Rival 2 trainer IDs `329/330/331` and Brock trainer ID `414` by loading and saving validated raw FRLG `trainerbattle` runtime-source `TrainerData` rows outside the normal loaded trainer count.
- Status impact: Foe Trainer remains CLI-log-clean from exact coverage; Rival 2 and Brock now have a pinned runtime-source party fix, but local ingame smoke remains required before stronger support claims.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - Trainer runtime source diagnostics sync

- Workspace branch: `randomizer/sync-trainer-runtime-source-diagnostics`.
- UPR-FVX PR #100: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/100>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #100 commit `87bba797620dd2043f02c11c67f7b752a7238a00`.
- Scope: PR #100 adds No-ROM/synthetic trainerbattle runtime-source diagnostics for mapping FRLG script trainer IDs to `TrainerData` rows, party pointers and first raw party species.
- The existing opt-in local runtime-source report can now include trainerbattle runtime-source rows; it remains local-only and ROM-reading only when explicitly configured by the user.
- Status impact: Foe Trainer remains CLI-log-clean from exact coverage, but ingame status is partial/caveated until local sanitized evidence confirms affected battles use the same runtime `TrainerData` source that UPR-FVX logs and writes.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - Settings profile variant overlays sync

- Workspace branch: `randomizer/sync-settings-profile-variant-overlays`.
- UPR-FVX PR #99: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/99>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #99 commit `4c8e7394a230e6e8471977036be268c80883ac0b`.
- Scope: PR #99 extends the No-ROM `settings-profile` helper with exact `MODE-*` overlays for Foe Pokemon modes, Wild replacement/location modes, TypeEffectiveness modes and Intro Mon toggles.
- Updated the workspace generator/matrix docs so `feature_overlays` can contain either Feature IDs such as `FVX-FOE-001` or exact mode overlay IDs such as `MODE-FOE-RANDOM`.
- Updated `08_tests/randomizer/cli_profile_matrix.coverage.example.tsv` with disabled opt-in rows for Foe mode, Wild location, TypeEffectiveness and Intro random/no-random variants.
- Documented exact Gen-Limit-1-9 variants as unsupported because current UPR-FVX Settings cannot encode Gen 8/9 restrictions or GMax exclusion.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no workspace-side UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - Exact coverage batches 03-18

- Workspace branch: `randomizer/sync-exact-coverage-batches-03-18`.
- Added `08_tests/randomizer/201_exact_coverage_batches_03_18.md`.
- Sanitized local exact-coverage Batch 03 through 18 CLI log-smoke/helper results: Batches 03 through 17 processed 165 generator-capable exact/cumulative/mode profiles with all PASS profiles at bad markers 0 and warnings 0; Batch 18 confirmed 4 Gen-Limit `MODE-*` overlays fail as expected.
- Updated `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` for affected generator-capable Feature IDs across TM/Tutor, Wild, Foe, General/Traits, Starters/Statics/Trades, Moves, Graphics/Palettes, Misc, Types, cumulative coverage and exact Foe/Wild/Type/Intro mode overlays.
- Updated `01_docs/randomizer/fvx-progress-dashboard.md` conservatively for the Batch 03-18 snapshot/package/diagnosis status without shortening the full Feature-ID list.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - Exact coverage batch 02 items

- Workspace branch: `randomizer/sync-exact-coverage-batch-02-items`.
- Added `08_tests/randomizer/200_exact_coverage_batch_02_items.md`.
- Sanitized local exact-coverage Batch 02 Item CLI log-smoke result: dry-run disabled, 13 profiles processed, all profiles PASS, bad markers 0 and warnings 0.
- Updated `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` only for `FVX-ITEM-001` through `FVX-ITEM-010`.
- Updated `01_docs/randomizer/fvx-progress-dashboard.md` conservatively for the Batch 02 Items snapshot/diagnosis status without shortening the full Feature-ID list.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - Exact coverage batch 01

- Workspace branch: `randomizer/sync-exact-coverage-batch-01`.
- Added `08_tests/randomizer/199_exact_coverage_batch_01.md`.
- Sanitized local exact-coverage Batch 01 CLI log-smoke result: dry-run disabled, 19 profiles processed, all profiles PASS, bad markers 0 and warnings 0.
- Updated `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` only for `FVX-TRAIT-017`, `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-009`, `FVX-SST-010`, `FVX-SST-012`, `FVX-FOE-005`, `FVX-FOE-006`, `FVX-FOE-007`, `FVX-FOE-009` and `FVX-FOE-011`.
- Updated `01_docs/randomizer/fvx-progress-dashboard.md` conservatively for the Batch 01 snapshot/diagnosis status without shortening the full Feature-ID list.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - Coverage CLI profile matrix pass

- Workspace branch: `randomizer/sync-coverage-profile-matrix-pass`.
- Added `08_tests/randomizer/198_cli_profile_matrix_coverage_run.md`.
- Sanitized local coverage-generated `.rnqs` CLI profile matrix result: dry-run disabled, 14 profiles processed, all PASS/UNEXPECTED_PASS profiles had 0 bad markers and 0 warnings.
- PASS profiles: `00_baseline`, `01_traits_full`, `02_starters_statics_trades_full`, `03_moves_movesets_full`, `04_foe_base`, `04_foe_held_items_basic`, `05_wild_full`, `06_tm_tutor_full`, `07_items_full` and `08_types_full`.
- UNEXPECTED_PASS profiles remain caveated: `04_foe_held_items_sensible_expected_fail`, `09_graphics_palettes`, `10_misc_tweaks` and `11_special_wild`.
- Updated `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` and `01_docs/randomizer/fvx-progress-dashboard.md` conservatively, only crediting 198 evidence where the executed profile exactly enabled the Feature ID.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - FVX profile coverage audit

- Workspace branch: `randomizer/profile-coverage-audit`.
- Added `08_tests/randomizer/fvx_profile_coverage_plan.md`.
- Added `08_tests/randomizer/cli_profile_matrix.coverage.example.tsv`.
- Extended `07_scripts/randomizer/generate_settings_profiles_from_matrix.sh` with an optional TSV `feature_overlays` column. Rows with this column call `UPR-FVX.jar settings-profile --enable <FEATURE_ID>` for each comma-separated Feature ID instead of only `--profile <profile_id>`.
- Updated `07_scripts/randomizer/run_cli_profile_matrix.sh` so the runner tolerates the optional generator-only column and continues to consume generated `settings_file` paths.
- The coverage audit keeps all 130 Feature IDs trackable across single, variant, tab, cumulative and risk-interaction profile layers.
- Current generator gap: exact TypeEffectiveness Random, Keep-Identities and Inverse modes are documented as disabled placeholders until UPR-FVX exposes exact overlays; `FVX-TYPE-001` currently maps to Random-Balanced.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - Generated CLI profile matrix results

- Workspace branch: `randomizer/sync-cli-profile-matrix-results`.
- Added `08_tests/randomizer/197_cli_profile_matrix_generated_run.md`.
- Sanitized local generated `.rnqs` CLI profile matrix result: 14 profiles processed, all profiles produced CLI log smoke pass or unexpected pass, bad markers 0 for all profiles and warnings 0 for all profiles.
- Unexpected-pass profiles: `04_foe_held_items_sensible_expected_fail`, `09_graphics_palettes`, `10_misc_tweaks` and `11_special_wild`.
- Updated `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` and `01_docs/randomizer/fvx-progress-dashboard.md` to record log-pass evidence and caveats without removing Feature IDs or shortening the dashboard full list.
- Safety: no ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - Settings profile generator sync

- Workspace branch: `randomizer/sync-settings-profile-generator`.
- UPR-FVX PR #98: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/98>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #98 commit `81fa4cf35af48bce19996e4581f1e4a688ebfa3b`.
- Scope: PR #98 adds the No-ROM `settings-profile` helper that reads a base `.rnqs`, applies feature/profile overlays through FVX `Settings` APIs and writes generated `.rnqs` files.
- Added `07_scripts/randomizer/generate_settings_profiles_from_matrix.sh` to call the UPR-FVX helper once per enabled profile in a TSV manifest.
- Added `08_tests/randomizer/196_settings_profile_generator_sync.md` and updated CLI profile matrix docs.
- Default UPR-FVX jar path remains `02_external/upr-fvx/random/build/libs/UPR-FVX.jar`.
- Safety: Codex verified only No-ROM build/help paths and generated no output ROM. No ROM/save/output/log artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX code change in this workspace PR and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - FVX feature test status matrix

- Workspace branch: `randomizer/fvx-feature-test-status-matrix`.
- Base verified: current `main` includes merged Workspace PR #268 at `1c2ca82c7cc96191c6ab57f198956542e95e44d6`.
- Added `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` with all 130 Feature IDs from the dashboard full feature list.
- Added `08_tests/randomizer/195_fvx_feature_test_status_matrix.md` documenting the status model, CLI profile mapping, update rules and privacy boundary.
- Scope: machine-readable status/worklist only. The dashboard remains the human overview and its full feature list is unchanged.
- Historical caveats captured at this matrix-update point: hard Evolution combinations can fallback under constraints, Trainer Class Names is textlabel-only, trainer held Sensible Items is expected-fail due to `getSensibleHeldItemsFor` NPE and Special-Wild is out-of-scope. Later updates supersede Palettes/Graphics and Misc Tweaks with targeted smoke caveats.
- Safety: no ROM/save/output/log/build artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - CLI profile matrix pipeline

- Workspace branch: `randomizer/settings-profile-matrix-pipeline`.
- Base verified: current `main` includes merged Workspace PR #267 at `204184e4d5aab834fa2a3725fa76f341995cd042`.
- Added `07_scripts/randomizer/run_cli_profile_matrix.sh` for TSV-driven multi-profile CLI smoke orchestration.
- Added `07_scripts/randomizer/generate_cli_smoke_profiles.sh` as a manifest scaffold generator. It does not create or modify FVX `.rnqs` settings files.
- Added `08_tests/randomizer/194_cli_profile_matrix_pipeline.md` and `08_tests/randomizer/cli_profile_matrix.example.tsv`.
- Updated `07_scripts/randomizer/cli_log_smoke_pipeline.sh` so per-profile sanitized reports include warning marker counts and snippets.
- Technical decision: FVX settings files are versioned Base64 plus CRC/checksum state, so this workspace PR avoids shell/Python byte-patching. Current matrix execution uses saved local settings profiles; automatic profile derivation should be a later UPR-FVX helper/CLI subcommand or Java helper using FVX `Settings` APIs.
- Safety: Codex used dry-run only, no ROM/save/output/log/build artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - CLI log smoke pipeline

- Workspace branch: `randomizer/cli-log-smoke-pipeline`.
- Added `07_scripts/randomizer/cli_log_smoke_pipeline.sh` as a local opt-in wrapper around `UPR-FVX.jar cli`.
- Added `08_tests/randomizer/193_cli_log_smoke_pipeline.md` with usage, pass criteria, dry-run behavior and sanitized handoff rules.
- Default jar path: `02_external/upr-fvx/random/build/libs/UPR-FVX.jar`.
- The helper forwards local private ROM/settings/output paths to UPR-FVX only when the user runs it explicitly; Codex did not run it with a ROM.
- The helper requests UPR-FVX detailed logging with `-l`, then writes a sanitized summary report with CLI exit status, success marker, output/log creation and blocked marker counts.
- Scope boundary: Stable Visual Profile plus optional Starter Pokemon remains the current local smoke target; Trainer Class Names is textlabel-only, Special-Wild is out-of-scope and `Rival Carries Starter Through Game` remains separate.
- Safety: no ROM/save/output/log/build artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - Starter/Rival sync pass

- Workspace branch: `randomizer/sync-starter-rival-sync-pass`.
- UPR-FVX PR #97: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/97>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #97 commit `51d52a03235664154549105003dadfb45c76d0d0`.
- Scope: PR #97 fixes the FireRed/CFRU-DPE Oak-Lab Rival slot mapping after PR #96 identified the raw `TrainerData` party rows as the real runtime source.
- Root cause: the Oak-Lab Rival uses raw trainer party rows outside the normal loaded trainer list; PR #96 wrote the correct source but projected the starter slots incorrectly. PR #97 maps the candidate trainer IDs as `[328, 326, 327]` and keeps the FRLG counter rule: player slot 0 -> starter slot 1, player slot 1 -> starter slot 2 and player slot 2 -> starter slot 0.
- Sanitized local smoke evidence: randomized starter slots were Groudon, Fearow and Mudbray; the player chose Groudon; the expected Rival counter-slot was Fearow; the observed Rival was Fearow.
- Result: Starter Pokemon passed for the Oak-Lab first Rival smoke. No vanilla fallback, same-starter bug, crash or softlock was observed in the sanitized evidence.
- Stable Visual Profile can now optionally include Starter Pokemon for local sampling. `Rival Carries Starter Through Game` remains a separate, not-tested full-rival path.
- Safety: no ROM/save/output/log/build artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change in this workspace sync and no P1 promotion.

# Tool Manifest Update - 2026-05-18 - GUI working settings matrix

- Workspace branch: `randomizer/sync-gui-settings-matrix-pass`.
- UPR-FVX PR #88: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/88>.
- UPR-FVX PR #89: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/89>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #89 commit `f3a6d04ff6db8d48468800194e0baffbafb7505c`, including PR #88.
- Scope: PR #88 documents Trainer Class Names as class-text remapping with unchanged trainer class id/sprite behavior; PR #89 fixes CFRU/DPE Extended-BPRE In-Game Trades species writes to use internal SpeciesSet identity.
- Sanitized local evidence records the current GUI Working Settings Matrix after UPR-FVX fixes through PR #89.
- Passed settings: Wild Standard/Fallback, Trainer Pokemon core, Pokemon Movesets -> Random completely, Trainer Movesets, Trainer Names, Field Items basic, Pokemon Abilities, TM/HM Compatibility, TM Moves, Move Tutor Moves, Move Tutor Compatibility, Shop Items, Pickup Items, In-Game Trades, Static Pokemon, Type Effectiveness, Pokemon Base Statistics and Move Data Power/Accuracy/PP/Type/Names.
- Evolutions unchanged are preserved, including the corrected CFRU/DPE row-stride path; swarms remain disabled through CFRU `SWARM_CHANCE=0`.
- Caveats: Trainer Class Names is textlabel remapping only and can mismatch the trainer sprite/class id, so it is recommended off for the stable visual profile; Starter Pokemon still has unresolved rival first-battle sync; Special-Wild remains out-of-scope; supported/special shops are confirmed; Static null placeholders remain null; Base Stats ability-name log display can appear truncated while ingame names are correct.
- Safety: no ROM/save/output/log/build artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change in this workspace sync and no P1 promotion.

# Tool Manifest Update - 2026-05-17 - Trainer Names/Class Names GUI smoke

- Workspace branch: `randomizer/sync-trainer-names-class-names-pass`.
- UPR-FVX PR #83: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/83>.
- UPR-FVX PR #85: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/85>.
- UPR-FVX PR #86: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/86>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #86 commit `f86315e7528ba3257df03b80c0c75ccc69ef574b`, including PR #83 and PR #85.
- Scope: PR #83 refreshed stale Gen3 trainer `fullDisplayName` values after Trainer Names/Class Names changes; PR #85 changed Trainer Class Names to shuffle existing class labels; PR #86 fixed the Gen3 loaded trainer class id used by the display-name refresh path.
- Sanitized local GUI-smoke evidence: Trainer Names and Trainer Class Names were enabled with the stable Wild Standard/Fallback, Trainer Pokemon core and Pokemon Movesets -> Random completely path.
- Trainer Names are visibly changed in the Trainer Pokemon log.
- Trainer Class Names no longer collapse to `Director` or `[PKMN] BREEDER`.
- Trainer Class Names pass as global class-label remapping; per-trainer class assignment remains a separate possible future feature.
- Evolutions remain correct in the tested path, including Squirtle -> Wartortle Lv16.
- Wild Standard/Fallback, Trainer Pokemon core and Pokemon Movesets -> Random completely remain stable; swarms remain disabled.
- Missing sprites were not observed and move-less Pokemon were not observed.
- Safety: no ROM/save/output/log/build artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change in this workspace sync and no P1 promotion.

# Tool Manifest Update - 2026-05-17 - CFRU/DPE evolution row stride fix

- Workspace branch: `randomizer/sync-cfru-dpe-evolution-row-stride-fix`.
- UPR-FVX PR #82: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/82>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #82 commit `485f0b899c84470f3fab82317331a671ec023ac1`.
- Scope: PR #82 fixes the Gen3/CFRU-DPE evolution table row-stride path. CFRU/DPE uses `EVOS_PER_MON=16`, so CFRU/DPE evolution rows are now read/written/reported with `evolutionSlotsPerSpecies=16` and `evolutionRowSize=0x80`.
- Root cause: the old UPR-FVX evolution read/write/report path used vanilla 5-slot rows (`0x28` bytes), which made the report read the private input ROM incorrectly and could corrupt output evolutions.
- Sanitized local report evidence after PR #82: Input ROM starter chains correct and new Output ROM starter chains correct.
- Starter chain evidence: Bulbasaur -> Ivysaur Lv16, Ivysaur -> Venusaur Lv32, Charmander -> Charmeleon Lv16, Charmeleon -> Charizard Lv36, Squirtle -> Wartortle Lv16 and Wartortle -> Blastoise Lv36.
- Sanitized ingame smoke evidence after PR #82: Squirtle evolved at Lv16 in a new FVX output.
- Previous bad/Test13-style outputs were produced by the old writer path and are stale; they must not be reused as current evidence.
- Recommended next isolated option block: Trainer Names/Class Names or a first Items/Moves/Abilities slice, keeping Special-Wild systems off.
- Safety: no ROM/save/output/log/build artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change in this workspace sync and no P1 promotion.

# Tool Manifest Update - 2026-05-17 - GUI-4B no-swarms pass

- Workspace branch: `randomizer/sync-gui4b-no-swarms-pass`.
- UPR-FVX PR #79: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/79>.
- UPR-FVX PR #80: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/80>.
- CFRU PR #5: <https://github.com/Planton361/CFRU-expansion/pull/5>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #80 commit `226bcacc4f66cee5689caa128d5e35ef4acc001d`, including PR #79's empty-learnset guard.
- Workspace submodule `02_external/CFRU-expansion` now pins merged CFRU PR #5 commit `c4c90373fe7f24acd5dcfa3a8fbdd5cb573bfe29`, with `SWARM_CHANCE=0` for normal FVX-randomized runs.
- Sanitized local GUI-4B evidence: correct CFRU/DPE Gen9 ROM loaded with `isRomHack=true`, PokemonCount 1439, PokedexCount 1290 and generations 1-9 present.
- Options used: Wild Standard/Fallback, Trainer Pokemon core and Pokemon Movesets -> Random completely. Trainer Names/Class Names, Items/Moves/Abilities, TM/HM/Tutor and Special-Wild systems were not enabled.
- Result: output ROM was created locally, emulator boot succeeded, wild encounters and a trainer battle were checked, missing sprites were not observed and move-less Pokemon were not observed.
- The `SpeciesMovesetRandomizer` empty-moveset `IndexOutOfBoundsException` was not reproduced; Ogerpon remains valid and pool-eligible.
- Route 1 no-swarm rebuild check did not observe Swarm-Frigibax; example post-fix Route 1 encounter was Urshifu Lv3 displayed correctly.
- Remaining guarded invalid palette candidates are known warnings and not blockers for this GUI-4B scope.
- CFRU Day/Night Wild and other Special-Wild systems remain outside the current normal walkthrough scope.
- Safety: no ROM/save/output/log/build artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change in this workspace sync and no P1 promotion.

# Tool Manifest Update - 2026-05-17 - GUI-4A Ogerpon Wild/Trainer pass

- Workspace branch: `randomizer/sync-gui4a-ogerpon-wild-trainer-pass`.
- UPR-FVX PR #78: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/78>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #78 commit `18e184b2c22451c74b4ba46bd7203c579d3bc9e7`.
- Sanitized local GUI-4A evidence: correct CFRU/DPE Gen9 ROM loaded with `isRomHack=true`, PokemonCount 1439, PokedexCount 1290 and generations 1-9 present.
- Options used: Wild Standard/Fallback plus Trainer Pokemon core. Trainer Names/Class Names, Learnsets, Items/Moves/Abilities and Special-Wild systems were not enabled.
- Result: GUI randomization completed, output ROM was created locally, emulator boot succeeded, wild encounters were checked and a trainer battle was checked.
- Observed blockers: no missing sprites and no move-less Pokemon were observed in the local smoke.
- Ogerpon appears in Trainer output/log and is pool-eligible after the Learnset/Sprite/Palette asset fixes.
- Remaining known guarded exclusions: Bad Egg for no usable learnset; Warrior, Exeggcute, Cubone, Koffing and Mime Jr. for invalid/missing front battle sprite/palette.
- CFRU Day/Night Wild, Swarms and other Special-Wild systems remain outside the current normal walkthrough scope.
- Safety: no ROM/save/output/log/build artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change in this workspace sync and no P1 promotion.

# Tool Manifest Update - 2026-05-17 - Ogerpon asset fix sync

- Workspace branch: `randomizer/sync-ogerpon-asset-fix`.
- DPE PR #2: <https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/pull/2>.
- UPR-FVX PR #77: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/77>.
- Workspace submodule `02_external/Dynamic-Pokemon-Expansion-Gen-9` now pins merged DPE PR #2 commit `3d0ac870fadc91e55f6ff19c0f7aae3cac2014a1`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX PR #77 commit `d6415d59a8b94b4d6d4c1e424a73c0f426993d03`.
- Sanitized local Pool Asset Report evidence after local DPE+CFRU rebuild: PokemonCount 1439, PokedexCount 1290, candidate count before guard 1192, accepted count after guard 1186, excluded count 6, excluded no usable learnset 1, invalid/missing front battle sprite pointer 5 and invalid/missing normal palette pointer 5.
- Ogerpon internal slots 1422..1429 report movesLearntCount 20, learnsetPointerValid true, frontSpritePointerValid true and palettePointerValid true; Ogerpon status is accepted.
- Remaining invalid candidates in the sanitized report: Bad Egg has no usable learnset; Warrior, Exeggcute, Cubone, Koffing and Mime Jr. still have invalid/missing front battle sprite pointers.
- Safety: no ROM/save/output/log/build artifact committed, no private path/ROM hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change in this workspace sync and no P1 promotion.

# Tool Manifest Update - 2026-05-17 - CFRU/DPE learnset runtime fixes sync

- Workspace branch: `randomizer/sync-cfru-dpe-learnset-runtime-fixes`.
- UPR-FVX PR #76: `fix: read cfru runtime learnset pointer`.
- CFRU PR #3: `fix: generate learnset runtime repoint`.
- CFRU PR #2: gLevelUpLearnsets runtime repoint plus Ogerpon internal mappings.
- DPE PR #1: Ogerpon Terastal learnset mappings.
- Workspace submodule `02_external/upr-fvx` now pins `808cbe823772187ec3ecc13e484a87eb449aaac5`.
- Workspace submodule `02_external/CFRU-expansion` now pins `1c99ca5abeeb577f8214247e523e62575443bb81`.
- Workspace submodule `02_external/Dynamic-Pokemon-Expansion-Gen-9` now pins `0a1ca7811fd00f981dad19d7476b92513fe62cdc`.
- Sanitized local Pool Asset Report evidence after local rebuild: PokemonCount 1439, PokedexCount 1290, maxInternalSpeciesId 1439, accepted count after guard 1185, excluded count 7, excluded no usable learnset 1, invalid/missing front battle sprite pointer 6, invalid/missing normal palette pointer 6, cfruRuntimeLearnsetPointerOffset `0x1167134`, chosenLearnsetTableBase `0x1167134`, Ogerpon movesLearntCount 20 and Ogerpon learnsetPointerValid true.
- Effect: the learnset runtime pointer blocker is resolved; Ogerpon now has moves/learnset and remains excluded only because of invalid/missing front battle sprite pointer.
- Safety: no ROM/save/output/log/build artifact committed, no private path/hash/full log/screenshot documented, no UPR-FVX/CFRU/DPE code change in this workspace sync and no P1 promotion.

# Tool Manifest Update - 2026-05-16 - GUI load null species fix

- Workspace branch: `randomizer/gui-load-null-species-fix-sync`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #68: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/68>.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `04bdd8b2f2769bedb1bf6c6ff8fcdecbbf84e29c`.
- Previous workspace pin was `9bde3d4e2f983bfb96875c5fe9697f87763d8665`.
- Scope: fixes the GUI-0 ROM-load blocker where `RandomizerGUI.populateDropdowns()` could dereference a null Species in sparse Custom-ROM mappings.
- Fix summary: null Species are filtered out before GUI dropdown names are built, so null Species are not selectable dropdown entries.
- Sanitized local GUI-0 evidence after PR #68: GUI opened yes, custom ROM loaded yes, randomization not yet, output ROM not yet, private paths/logs/hashes/screenshots omitted yes.
- Safety: no ROM/save/output/log/build artifact committed, no private path/hash/full log/screenshot documented, no UPR-FVX code change in this workspace sync beyond pinning the merged PR, no Output-ROM evidence and no P1 promotion.

# Tool Manifest Update - 2026-05-16 - Trainer text ROM smoke harness

- Workspace branch: `randomizer/trainer-text-rom-smoke-harness-sync`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #67: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/67>.
- Original UPR-FVX test commit: `7b03bcae test: add trainer names rom smoke harness`.
- Workspace submodule `02_external/upr-fvx` now pins verified merged UPR-FVX commit `9bde3d4e2f983bfb96875c5fe9697f87763d8665`.
- Previous workspace pin was `f4d0cbbe3143cab4b963d2444b8354d97fa96403`.
- Scope: opt-in ROM-facing Gen3 Trainer Names/Class Names smoke harness in `Gen3TrainerTextRomSmokeTest`; default no-ROM run skips cleanly.
- Checks recorded from UPR-FVX PR #67: `git diff --check`, `git diff --cached --check`, `./gradlew :romio:test --tests '*Trainer*Smoke*'` and `./gradlew :random:test --tests '*TrainerNameRandomizerDecisions*'`, successful with the no-ROM smoke skipped.
- Evidence status: harness prepared only; no documented local ROM-smoke pass, no byte-exact Terminator/Padding inspection proof and no P1 promotion.
- Safety: no Workspace code changes beyond documentation and submodule pin, no new UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no private ROM path/hash/full log/output ROM documented and no Original-Upstream PR.
- Note: the expected SHA `a5a8887e0dac0bdbe4bfe87bfdc2e7a27fb79b75` was not the actual PR #67 merge commit; GitHub reports `9bde3d4e2f983bfb96875c5fe9697f87763d8665`.

# Tool Manifest Update - 2026-05-16 - Wild encounters P1 decision

- Workspace branch: `randomizer/wild-encounters-p1-decision`.
- UPR-FVX pin remains `f4d0cbbe3143cab4b963d2444b8354d97fa96403`.
- Decision: Standard/Fallback Wild Encounters are now `P1-supported` for the documented writer/reload scope in the tested private target context.
- Evidence basis: ROM-free Wild Encounter decision/option slices, ROM-free synthetic Writer/Reload Equality, opt-in ROM-facing smoke harness and sanitized local `Gen3WildEncounterRomSmokeTest` pass after PR #66.
- Scope boundary: CFRU Day/Night Wild, Swarms, Roamers, DexNav, Raids, Wild Double Battles and other special Wild systems remain separate/non-promoted scopes.
- Safety: no UPR-FVX code change, no submodule pin change, no new ROM execution, no ROM/save/output/log/build artifact committed, and no private ROM path/hash/full log/output ROM documented.

# Tool Manifest Update - 2026-05-16 - Wild encounters ROM smoke evidence

- Workspace branch: `randomizer/wild-encounters-rom-smoke-evidence-sync`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #66: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/66>.
- Original UPR-FVX fix commit: `75f95d15 fix: handle gen3 wild smoke evolution load blocker`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `f4d0cbbe3143cab4b963d2444b8354d97fa96403`.
- Previous workspace pin was `f224862c91aed8e7a75fe843f5088cadea734da4`.
- Scope: PR #66 fixes the Gen3 Evolution load blocker in `loadEvolutions()` so the opt-in Wild Encounter ROM smoke can reach the Wild Encounter writer/reload path.
- Sanitized local evidence after PR #66: `Gen3WildEncounterRomSmokeTest` passed with Tests 1, Failures 0, Errors 0, Skipped 0.
- Status: Wild Encounters is a P1 candidate; no P1 promotion is made in this sync.
- Safety: no Workspace code changes beyond documentation and submodule pin, no new UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no private ROM path/hash/full log/output ROM documented and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Wild encounters ROM smoke harness

- Workspace branch: `randomizer/wild-encounters-rom-smoke-harness-sync`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #65: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/65>.
- Original UPR-FVX test commit: `41e35eec test: add wild encounters rom smoke harness`.
- Workspace submodule `02_external/upr-fvx` now pins verified merged UPR-FVX commit `f224862c91aed8e7a75fe843f5088cadea734da4`.
- Previous workspace pin was `d49837fea305157a2fe94f3f57d09cedc8ab25f8`.
- Scope: opt-in ROM-facing Wild Encounter smoke harness in `Gen3WildEncounterRomSmokeTest`; default no-ROM run skips cleanly.
- Checks recorded from UPR-FVX PR #65: `git diff --check`, `git diff --cached --check`, `./gradlew :romio:test --tests '*Gen3WildEncounterRomSmokeTest*'`, `./gradlew :romio:test --tests '*Wild*'` and `./gradlew :random:test --tests '*Wild*'`, successful with the no-ROM smoke skipped.
- Safety: no Workspace code changes beyond documentation and submodule pin, no new UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no private ROM path/hash/log/output ROM documented, no local ROM-smoke result, no P1-promotion and no Original-Upstream PR.
- Note: the requested SHA `c7a07a4643a570b2e27de059804f1a249616aaf0` was not reachable in the UPR-FVX fork; GitHub reports PR #65 merge commit `f224862c91aed8e7a75fe843f5088cadea734da4`.

# Tool Manifest Update - 2026-05-16 - Wild encounters reload equality evidence

- Workspace branch: `randomizer/wild-encounters-p1-track`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #64: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/64>.
- Original UPR-FVX test commit: `0a0ec0b2 test: add wild encounters reload equality evidence`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `d49837fea305157a2fe94f3f57d09cedc8ab25f8`.
- Previous workspace pin was `d88a0cdb8c11473d2a3448028e937422eaf38679`.
- Scope: ROM-free synthetic Wild Encounter Writer/Reload Equality evidence in `WildCatchLevelDecisionTest`; a reloadable fake `RomHandler` deep-copies `setEncounters(...)` data and reloads fresh `getEncounters(...)` copies.
- Checks recorded from UPR-FVX PR #64: `git diff --check`, `git diff --cached --check`, `./gradlew :random:test --tests '*WildCatchLevelDecisionTest*'` and `./gradlew :random:test --tests '*Wild*'`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no new UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no real Gen3 byte writer proof, no output ROM, no Randomizer run, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Items first test slice

- Workspace branch: `docs/sync-items-first-slice`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #63: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/63>.
- Original UPR-FVX test commit: `86067eaa test: add items first slice`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `d88a0cdb8c11473d2a3448028e937422eaf38679`.
- Previous workspace pin was `a5b1b63b134149bd88e62af27a9b45332f617d9e`.
- Scope: third ROM-free Items/Moves/Abilities test slice in `ItemDecisionTest`; synthetic `ItemRandomizer.randomizeFieldItems()` coverage for Non-TM Field Items verifies non-bad allowed Item pool bounds, bad/key-style Item exclusion, non-empty output, stable Field-Item count and high Item IDs `1001..1003`.
- Checks recorded from UPR-FVX PR #63: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests '*ItemDecisionTest*'`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Moves first test slice

- Workspace branch: `docs/sync-moves-first-slice`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #62: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/62>.
- Original UPR-FVX test commit: `d6912e31 test: add moves first slice`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `a5b1b63b134149bd88e62af27a9b45332f617d9e`.
- Previous workspace pin was `c365b96399ed36881ed637edce0721c059c442d1`.
- Scope: second ROM-free Items/Moves/Abilities test slice in `TMTutorMoveDecisionTest`; synthetic `TMTutorMoveRandomizer.randomizeTMMoves()` coverage verifies allowed Move pool bounds, HM/game-breaking/levelup-banned/illegal Move exclusion, preserved Field-Move-TM slot, stable output count and high Move IDs `1001..1003`.
- Checks recorded from UPR-FVX PR #62: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests '*TMTutorMoveDecisionTest*'`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Items/Moves/Abilities first test slice

- Workspace branch: `docs/sync-items-moves-abilities-first-slice`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #61: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/61>.
- Original UPR-FVX test commit: `952d0a66 test: add items moves abilities first slice`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `c365b96399ed36881ed637edce0721c059c442d1`.
- Previous workspace pin was `c40fbbd796db5b43a3bc53e547dc890a853cef20`.
- Scope: first ROM-free Items/Moves/Abilities test slice in `SpeciesAbilityDecisionTest`; synthetic `SpeciesAbilityRandomizer` coverage verifies allowed Ability pool bounds, banned Ability rejection, non-empty two-Ability output and high Species ID `1025` path.
- Checks recorded from UPR-FVX PR #61: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests '*SpeciesAbilityDecisionTest*'`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Learnsets evolution moves test slice

- Workspace branch: `docs/sync-learnsets-evolution-moves-slice`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #60: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/60>.
- Original UPR-FVX test commit: `d98e3f8c test: cover learnsets evolution moves option`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `c40fbbd796db5b43a3bc53e547dc890a853cef20`.
- Previous workspace pin was `0d217db45086d8d03b4eb606ae2621633396d768`.
- Scope: fourth ROM-free Learnsets test slice in `LearnsetDecisionTest`; synthetic Evolution Moves for All coverage verifies exactly one Level-0 Evolution-Move slot is added while existing Level-1/later level slots, Move pool and high Species ID `1025` path remain stable.
- Checks recorded from UPR-FVX PR #60: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests '*Learn*'`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Learnsets starting moves test slice

- Workspace branch: `docs/sync-learnsets-starting-moves-slice`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #59: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/59>.
- Original UPR-FVX test commit: `948d8526 test: cover learnsets starting or evolution option`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `0d217db45086d8d03b4eb606ae2621633396d768`.
- Previous workspace pin was `6ed75f5b1e5b8b354e2db694c880407c8e0a10dd`.
- Scope: third ROM-free Learnsets test slice in `LearnsetDecisionTest`; synthetic Guaranteed Starting Moves coverage verifies expected Level-1 slots are added while the later level slot, Move pool and high Species ID `1025` path remain stable.
- Checks recorded from UPR-FVX PR #59: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests '*Learn*'`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Learnsets option test slice

- Workspace branch: `docs/sync-learnsets-option-slice`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #58: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/58>.
- Original UPR-FVX test commit: `96b6fc0f test: cover learnsets option behavior`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `6ed75f5b1e5b8b354e2db694c880407c8e0a10dd`.
- Previous workspace pin was `56cae7eb0c2ddc626dc31c4802d3f696a42959bf`.
- Scope: second ROM-free Learnsets option-test slice in `LearnsetDecisionTest`; synthetic `orderDamagingMovesByDamage()` coverage verifies damaging Moves are sorted by damage while Evolution-/Non-Damaging-Slots, Level-/Slot-Anzahl, Move pool and high Species ID `1025` remain stable.
- Checks recorded from UPR-FVX PR #58: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests '*Learn*'`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Learnsets first test slice

- Workspace branch: `docs/sync-learnsets-first-test-slice`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #57: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/57>.
- Original UPR-FVX test commit: `747c4821 test: add learnsets first slice`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `56cae7eb0c2ddc626dc31c4802d3f696a42959bf`.
- Previous workspace pin was `b3b9a8ab5e8726f4b4d2d4e23efa733cce7287ac`.
- Scope: first ROM-free Learnsets unit-test slice in `LearnsetDecisionTest`; synthetic `randomizeMovesLearnt()` coverage verifies non-empty Learnsets, preserved Level-/Slot-Anzahl, allowed Move-pool selection and high Species ID `1025`.
- Checks recorded from UPR-FVX PR #57: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests '*Learn*'`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Wild encounters option test slice

- Workspace branch: `docs/sync-wild-encounters-option-slice`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #56: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/56>.
- Original UPR-FVX test commit: `75c8b1a1 test: cover wild encounters option behavior`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `b3b9a8ab5e8726f4b4d2d4e23efa733cce7287ac`.
- Previous workspace pin was `8f88e25d458996b560189ba23d3216ee0c775f14`.
- Scope: third ROM-free Wild Encounter unit-test slice in `WildCatchLevelDecisionTest`; synthetic `BlockWildLegendaries` coverage verifies legendary Species stay out of the replacement pool while Slot-/Level-/Area structure remains stable and high-numbered Species IDs above `1000` remain usable.
- Checks recorded from UPR-FVX PR #56: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests com.uprfvx.random.randomizers.WildCatchLevelDecisionTest`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Wild encounters multi-area test slice

- Workspace branch: `docs/sync-wild-encounters-multi-area-slice`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #55: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/55>.
- Original UPR-FVX test commit: `52da522e test: cover wild encounters multi area structure`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `8f88e25d458996b560189ba23d3216ee0c775f14`.
- Previous workspace pin was `8d67f8686e16b3a9d3e77da5789a06889a645e5f`.
- Scope: second ROM-free Wild Encounter unit-test slice in `WildCatchLevelDecisionTest`; synthetic multi-area data covers different encounter areas, encounter types, slot counts, rates, map/location metadata and level ranges while preserving structure and allowing high-numbered Species IDs above `1000`.
- Checks recorded from UPR-FVX PR #55: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests com.uprfvx.random.randomizers.WildCatchLevelDecisionTest`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Wild encounters first test slice

- Workspace branch: `docs/sync-wild-encounters-first-slice`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #54: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/54>.
- Original UPR-FVX test commit: `20213ee6 test: add wild encounters first slice`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `8d67f8686e16b3a9d3e77da5789a06889a645e5f`.
- Previous workspace pin was `955c852cf07f155a046b18865a39e6912a6ee09c`.
- Scope: first ROM-free Wild Encounter unit-test slice in `WildCatchLevelDecisionTest`; synthetic encounters cover preserved Slot-/Level-/Area structure, non-empty encounter areas, allowed Species selection and high-numbered Species IDs above `1000`.
- Checks recorded from UPR-FVX PR #54: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests com.uprfvx.random.randomizers.WildCatchLevelDecisionTest`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Trainer class names encoded length fix

- Workspace branch: `docs/sync-trainer-class-names-encoded-length-fix`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #53: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/53>.
- Original UPR-FVX fix commit: `ceeec131 fix: use encoded length for trainer class names`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `955c852cf07f155a046b18865a39e6912a6ee09c`.
- Previous workspace pin was `7357b244e01ef2c7790b858d50c19c31ac72e955`.
- Scope: narrow `TrainerNameRandomizer.randomizeTrainerClassNames()` max-length check now uses `romHandler.internalStringLength(...)` instead of Java `changeTo.length()`, plus ROM-free `TrainerNameRandomizerTest` coverage.
- Checks recorded from UPR-FVX PR #53: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests '*TrainerNameRandomizer*'`, successful.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX code changes in this workspace sync, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no Terminator/Padding proof, no decoded reload equality, no Text-Encoding safety claim, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Trainer names text length unit evidence

- Workspace branch: `docs/trainer-names-text-length-unit-evidence`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #52: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/52>.
- Original UPR-FVX test commit: `230f667f test: cover trainer names text length risks`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `7357b244e01ef2c7790b858d50c19c31ac72e955`.
- Previous workspace pin was `d20eb1367c62a4f14c8778bc61ad6904ea76a6d6`.
- Scope: ROM-free `TrainerNameRandomizerTest` extension; synthetic RomHandler data covers Trainer Names/Class Names text-length risks including ASCII inside limit, exactly at encoded/internal limit, over encoded/internal limit, Java length != internal length, escaped-token-style divergence and Class-Names `changeTo.length()` risk exposure.
- Checks recorded from UPR-FVX PR #52: `git diff --check`, `git diff --cached --check` and `./gradlew :random:test --tests '*TrainerNameRandomizer*'`, successful after local Gradle cache access was allowed.
- Safety: no Workspace code changes beyond documentation and submodule pin, no UPR-FVX production code changes in this block, no ROM/save/output/log/build artifacts committed, no ROM-facing Writer/Reload evidence, no Terminator/Padding proof, no decoded reload equality, no Text-Encoding safety claim, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Trainer names follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-trainer-names-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #51: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/51>.
- Original UPR-FVX test commit: `f49f5aa9 test: cover trainer name decisions`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `d20eb1367c62a4f14c8778bc61ad6904ea76a6d6`.
- Previous workspace pin was `5e2d351966ce4a96d02cdb6ca676b39bde7a9505`.
- Scope: Non-ROM `TrainerNameRandomizerTest`; synthetic RomHandler data covers `FVX-FOE-013` Trainer Names/Class Names decisions.
- Checks recorded from UPR-FVX PR #51: `git diff --check`, `./gradlew --offline :random:test --tests '*TrainerNameRandomizer*'` and `./gradlew --offline :random:test --tests '*Trainer*'`, all successful.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no Gen3 Writer-/Reload-ROM test, no ROM-Smoke, no text-encoding implementation, no `changeTo.length()` fix, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Trainer battle style follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-battle-style-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #50: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/50>.
- Original UPR-FVX test commit: `99f46cce7464750ea5cdc4055b1e9168e59bc1a0`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `5e2d351966ce4a96d02cdb6ca676b39bde7a9505`.
- Previous workspace pin was `bc46fdc49741643d8f09dd302b67b5b2d35d24c5`.
- Scope: Non-ROM `TrainerBattleStyleTest`; synthetic Trainer data covers `FVX-FOE-011` Battle Style decisions.
- Checks recorded from UPR-FVX PR #50: `git diff --check`, `./gradlew --offline :random:test --tests '*TrainerBattleStyle*'`, `./gradlew --offline :random:test --tests '*Trainer*'` and `./gradlew --offline :random:test`, all successful.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no Trainer Names/Class Names/Text scope, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Trainer special rules follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-trainer-special-rules-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #49: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/49>.
- Original UPR-FVX test commit: `6489dd1e61d1bcb35345ae006032b884527e0a97`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `bc46fdc49741643d8f09dd302b67b5b2d35d24c5`.
- Previous workspace pin was `32ab7d969e5439d38e5781670c9a68e0ea418d0a`.
- Scope: Non-ROM `TrainerSpecialRulesTest`; synthetic Trainer, Party, Species and Evolution data cover `FVX-FOE-010`, `FVX-FOE-012` and `FVX-FOE-014`.
- Checks recorded from UPR-FVX PR #49: `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.TrainerSpecialRulesTest`, `./gradlew --offline :random:test --tests '*Trainer*'` and `./gradlew --offline :random:test`, all `BUILD SUCCESSFUL`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no Battle Style scope, no Trainer Names/Class Names/Text scope, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Trainer additional pokemon follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-trainer-additional-pokemon-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #48: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/48>.
- Original UPR-FVX test commit: `cdc09eaee12c44a7f3ba5ca24a091ce4da2ef8ac`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `32ab7d969e5439d38e5781670c9a68e0ea418d0a`.
- Previous workspace pin was `ea5269706eb7d04eb0b305f88e8fa20bfb21f92a`.
- Scope: Non-ROM `TrainerAdditionalPokemonTest`; synthetic Trainer, Party and Species data cover `FVX-FOE-005`, `FVX-FOE-006` and `FVX-FOE-007`.
- Guard/Fix: `TrainerPokemonRandomizer` clones additional Pokemon only from original slots with non-null Species; trainers without a safe template are skipped, and max party size 6 plus multi-battle limit 3 are covered.
- Checks recorded from UPR-FVX PR #48: `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.TrainerAdditionalPokemonTest`, `./gradlew --offline :random:test --tests '*Trainer*'` and `./gradlew --offline :random:test`, all `BUILD SUCCESSFUL`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no Trainer Names/Class Names/Text scope, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Trainer type diversity follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-trainer-type-diversity-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #47: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/47>.
- Original UPR-FVX test commit: `60f6664e556cc750801ad1d47ba970ded8d6af85`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `ea5269706eb7d04eb0b305f88e8fa20bfb21f92a`.
- Previous workspace pin was `c86221d758bece06b216b1f4fb23dd8e4a6c8ec0`.
- Scope: Non-ROM `TrainerTypeDiversityGuardTest`; synthetic `Species`, `Trainer` and `TrainerPokemon` data cover `FVX-FOE-009` Force Diverse Types / Type Themes null Primary/Secondary Type guard behavior.
- Checks recorded from UPR-FVX PR #47: `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.TrainerTypeDiversityGuardTest`, `./gradlew --offline :random:test --tests '*Trainer*'` and `./gradlew --offline :random:test`, all `BUILD SUCCESSFUL`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no Trainer Names/Class Names/Text scope, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Wild catch level follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-wild-catch-level-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #46: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/46>.
- Original UPR-FVX test commit: `8665eb4f070567fd908327b272c7f1da5abdef68`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `c86221d758bece06b216b1f4fb23dd8e4a6c8ec0`.
- Previous workspace pin was `1be6f51779906af017f6177f264e41f8c7902d8e`.
- Scope: Non-ROM `WildCatchLevelDecisionTest`; synthetic `Species`, `Encounter` and `EncounterArea` data cover `FVX-WILD-007`, `FVX-WILD-010` and `FVX-WILD-012`.
- Checks recorded from UPR-FVX PR #46: `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.WildCatchLevelDecisionTest`, `./gradlew --offline :random:test --tests '*Wild*'` and `./gradlew --offline :random:test`, all `BUILD SUCCESSFUL`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - MoveData write follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-movedata-write-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #45: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/45>.
- Original UPR-FVX test commit: `60996b166113d40f4ff848d8063e98661415a599`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `1be6f51779906af017f6177f264e41f8c7902d8e`.
- Previous workspace pin was `85b282112322f8991dd11b14cc98d6dd68fd3fd4`.
- Scope: Non-ROM `Gen3MoveDataWriterTest` and `MoveUpdateDecisionTest`; synthetic MoveData bytes and synthetic `Move` data cover `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` and `FVX-MOVE-006`.
- Checks recorded from UPR-FVX PR #45: focused `./gradlew --offline :romio:test --tests '*Move*'`, focused `./gradlew --offline :random:test --tests '*Move*'`, full `./gradlew --offline :romio:test` and full `./gradlew --offline :random:test`, all `BUILD SUCCESSFUL`; known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no Move Names/Text scope, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - Evolution make easier follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-make-evolutions-easier-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #44: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/44>.
- Original UPR-FVX test commit: `a0fc6515b60ad3032a8d94c554bbc3021e10a33f`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `85b282112322f8991dd11b14cc98d6dd68fd3fd4`.
- Previous workspace pin was `3b33412e80d1cb2d97725ad7a7dd01529aa56919`.
- Scope: Non-ROM `EvolutionMakeEasierDecisionTest` only; synthetic `Species` / `Evolution` chains and a small package-private helper in `AbstractRomHandler` cover `FVX-TRAIT-025A`.
- Checks recorded from UPR-FVX PR #44: `./gradlew --offline :romio:test --tests '*Evolution*'` and `./gradlew --offline :romio:test`, both `BUILD SUCCESSFUL`; known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts, no Gen3 Happiness-byte patch, no writer/reload, no ROM-Smoke, no Randomizer run, no `FVX-TRAIT-025B` scope, no `FVX-TRAIT-026` standalone support claim, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - Evolution method decision harness follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-evolution-method-decisions-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #43: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/43>.
- Original UPR-FVX test commit: `4b049ee82cf8716cb2fc17d0b6244020cddd22e4`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `3b33412e80d1cb2d97725ad7a7dd01529aa56919`.
- Previous workspace pin was `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- Scope: Non-ROM `EvolutionMethodDecisionTest` only; synthetic `Species` / `Evolution` data and small package-private decision seams in `Gen3RomHandler` and `AbstractRomHandler` cover `FVX-TRAIT-024` and `FVX-TRAIT-027`.
- Checks recorded from UPR-FVX PR #43: `./gradlew --offline :romio:test --tests '*Evolution*'` and `./gradlew --offline :romio:test`, both `BUILD SUCCESSFUL`; known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts, no Gen3 writer, no reload, no ROM-Smoke, no Randomizer run, no `FVX-TRAIT-025/026` scope except `useEstimatedLevels` as `024` decision input, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - Evolution filter non-ROM harness follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-evolution-filter-non-rom-harness-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #42: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/42>.
- Original UPR-FVX test commit: `e71a126c test: cover evolution filter options`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- Previous workspace pin was `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Scope: Non-ROM `EvolutionFilterOptionsTest` only; synthetic `Species` / `Evolution` data and a minimal `RomHandler` proxy/fake cover `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023`.
- Checks recorded from UPR-FVX PR #42: `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.EvolutionFilterOptionsTest` and `./gradlew --offline :random:test`, both `BUILD SUCCESSFUL`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts, no ROM-Smoke, no Gen3 writer, no reload, no `FVX-TRAIT-024..027` scope, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - In-Game Trades writer preserve follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-ingame-trades-writer-preserve-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #41: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/41>.
- Original UPR-FVX test commit: `b71bd2ec test: cover ingame trade writer preserve guard`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Previous workspace pin was `1eaee2873cd69682335223f817b124bf36d004f2`.
- Scope: ROM-free `Gen3InGameTradeWriterTest` only; synthetic `InGameTrade` rows and synthetic bytes cover unsafe/null-request writer preserve decisions through a narrow package-private `Gen3RomHandler` seam.
- Checks recorded from UPR-FVX PR #41: `./gradlew --offline :romio:test` and focused `./gradlew --offline :romio:test --tests com.uprfvx.romio.romhandlers.Gen3InGameTradeWriterTest`, both `BUILD SUCCESSFUL`; known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts, no ROM-Smoke, no Species-Write-Smoke, no valid-active-row promotion, no text, Nickname/OT, IV or Trade Held Item randomization, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - In-Game Trades non-ROM harness follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-ingame-trades-non-rom-harness-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #40: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/40>.
- Original UPR-FVX test commit: `8b7d0846 test: cover ingame trade skip guard`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `1eaee2873cd69682335223f817b124bf36d004f2`.
- Previous workspace pin was `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Scope: non-ROM `TradeRandomizerTest` harness only; synthetic `InGameTrade` rows and a minimal `RomHandler` proxy/fake cover null-request and placeholder/unsafe Species skips, all-skipped no `setInGameTrades(...)`, `isChangesMade=false`, skip counters and `hasSkippedTrades()`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts, no Gen3 writer test, no ROM-Smoke, no Species-Write-Smoke, no text, Nickname/OT, IV or Trade Held Item randomization, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - In-Game Trades null-request guard follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-ingame-trades-null-request-guard-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #39: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/39>.
- Original UPR-FVX fix commit: `1d3062d1 fix: skip unsafe ingame trade rows`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Previous workspace pin was `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- Scope: In-Game Trades defensive null/invalid Species guard only; `TradeRandomizer.java` skips unsafe rows before mutation and `Gen3RomHandler.java` preserves/skips unsafe rows before byte writes.
- Safety: no Workspace code changes, no ROM/save/output/log/build artifacts, no text randomization, no Nickname/OT, IV or Trade Held Item randomization, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - Pickup reload locator fix

- Workspace branch: `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- UPR-FVX fork branch: `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- UPR-FVX PR #38: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/38>.
- Workspace submodule `02_external/upr-fvx` now pins `a2373888ad17145f270ebf6ff17303af41aa86eb` for the Pickup table reload locator fix.
- Previous pin was `328e4441c2981d37aba9e2707a6f27f779b026e2`.

# Tool Manifest Update - 2026-05-15 - UPR-FVX Field Items API TM-slot fix

- `02_external/upr-fvx` pinned to Planton361/universal-pokemon-randomizer-fvx commit `328e4441c2981d37aba9e2707a6f27f779b026e2` on branch `compat/upr-fvx-cfru-dpe-field-items-api-tm-slot-scope-fix`.
- UPR-FVX PR #37 opened against `compat/firered-gen9-cfru-dpe`: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/37>.
- Scope: CFRU/DPE Field-Items API TM-slot exposure only; no original-upstream PR.

# Tool Manifest Update - 2026-05-15 - Field Items Random TM-pool fix pin

Dieser Stand dokumentiert den Arbeitsblock `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix`. UPR-FVX wurde im Planton361-Fork-Submodule eng im Field-Items-Random-TM-Pool geaendert; kein ROM-/Randomizer-Reload-Smoke wurde in diesem Block ausgefuehrt. Tool-Binaries, Release-Assets, Secrets und private Pfade wurden nicht dokumentiert.

| Komponente | Rolle | Remote | Lokaler Pfad | Branch | Commit/Pin | Aenderung | Notiz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix` | `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd` | ja, nur in diesem Branch | Field-Items-Random-TM-Pool-Fix fuer `FVX-ITEM-002`; Required TMs bleiben Pflicht, Filler-Pool dedupliziert; Reload-Smoke noch offen |

# Tool Manifest

Dieses Manifest dokumentiert Tools, Repos, Forks, Versionen, Pfade und Sicherheitsstatus.

## Sicherheitsstatus

Dieser Stand dokumentiert den Arbeitsblock `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`. UPR-FVX wurde im Planton361-Fork-Submodule gezielt geaendert und gebaut; kein ROM-/Randomizer-Reload-Smoke wurde ausgefuehrt. Tool-Binaries, Release-Assets, Secrets und private Pfade wurden nicht dokumentiert.

Linux/CachyOS ist die primaere lokale Umgebung. Windows-Toolchain-Befunde bleiben historischer Referenzstand und duerfen nicht als Linux-Ist-Stand verwendet werden.

Der aktuelle Arbeitsblock pinnt den Workspace auf den UPR-FVX-Normal-Palette-Single-owner-Write-Guard-Fix-Commit fuer CFRU/DPE.

| Tool/Repo | Zweck | Upstream | Fork/Origin | Lokaler Pfad | Branch | Commit | Codex darf ändern | Status |
|---|---|---|---|---|---|---|---|---|
| Workspace Repo | Source of Truth | n/a | git@github.com:Planton361/firered-gen9-randomizer-workspace.git | Workspace-Root | `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write` | offen | ja, nur Branches | aktiv |
| Git | Versionierung | n/a | n/a | `/usr/bin/git` | n/a | n/a | nein | gefunden: 2.54.0 |
| GitHub CLI (`gh`) | PRs und GitHub-Checks automatisieren | https://cli.github.com/ | n/a | `/usr/bin/gh` | n/a | n/a | nein | gefunden: 2.92.0; Auth via Keyring aktiv |
| POSIX Shell | Terminal-Standard | n/a | n/a | `/bin/fish` laut `$SHELL` | n/a | n/a | nein | primär |
| PowerShell 7 (`pwsh`) | optionale Script-Ausführung für bestehende Checks | https://github.com/PowerShell/PowerShell | n/a | nicht im PATH gefunden | n/a | n/a | nein | fehlt/optional |
| Java | Laufzeit fuer UPR FVX | https://adoptium.net/ oder Distribution-Paket | n/a | `/usr/bin/java` | n/a | n/a | nein | gefunden: OpenJDK 26.0.1; UPR-FVX-Anforderung spaeter verifizieren |
| `make` | Build-Orchestrierung fuer spaetere Toolchain-Schritte | n/a | n/a | `/usr/bin/make` | n/a | n/a | nein | gefunden: GNU Make 4.4.1 |
| devkitPro/devkitARM | GBA Build Toolchain | devkitPro | n/a | Linux-Pfad offen | n/a | n/a | nein | nicht nachgewiesen; Installation nur in separatem Block |
| `arm-none-eabi-gcc` | GBA Cross-Compiler | ARM GNU Toolchain/devkitARM | n/a | nicht im PATH gefunden | n/a | n/a | nein | fehlt; ueber devkitPro/devkitARM priorisiert klaeren |
| `agbcc` | optionale GBA/pret-kompatible Compiler-Komponente | pret/devkitARM-Kontext | n/a | nicht im PATH gefunden | n/a | n/a | nein | fehlt/optional; nur bei Buildpfad-Bedarf klaeren |
| Codex CLI | primärer Coding Agent | OpenAI | n/a | offen | n/a | n/a | nur nach Branch-Freigabe | primärer Worker fuer erlaubte Arbeitsbranches |
| ChatGPT QA | Analyse, Review und Handoff | OpenAI | n/a | n/a | n/a | n/a | nein | Steuerungs-/QA-Ebene |
| JetBrains Toolbox | JetBrains IDE-Verwaltung | JetBrains | n/a | User-Installation; privater Pfad nicht dokumentiert | n/a | n/a | nein | gefunden: Toolbox 3.4.3.81140 |
| IntelliJ IDEA | optionale lokale IDE-Navigation | JetBrains | n/a | Toolbox-verwaltete User-Installation; privater Pfad nicht dokumentiert | n/a | Build `IU-262.4852.50` | nein | gefunden: IntelliJ IDEA 2026.2 EAP; Mindestversion 2025.2 erfuellt |
| JetBrains MCP Server | optionale IDE-MCP-Integration fuer read-only Codebase-Analyse | JetBrains, gebuendelt in IntelliJ-basierten IDEs | n/a | gebuendeltes IntelliJ-Plugin `com.intellij.mcpServer`; Installationspfad nicht dokumentiert | n/a | Plugin-Version `262.4852.50` | nein | verfuegbar; fuer Codex nur read-only und optional freigegeben |
| `.aiignore` | Agent-Kontextschutz | n/a | n/a | `.aiignore` | n/a | n/a | ja | ergänzt fuer ROM-/Build-/Tool-Binary-/Secret-Pfade |
| GitHub PR Template | PR-Checkliste | GitHub | n/a | `.github/pull_request_template.md` | n/a | n/a | ja | ergänzt |
| MCP allgemein | optionale Tool-Integration | abhängig vom Server | n/a | keine aktive Config committed | n/a | n/a | nur nach Manifest-Eintrag | optional, nicht Default |
| UPR FVX | Randomizer | https://github.com/upr-fvx/universal-pokemon-randomizer-fvx | offen | `02_external/upr-fvx` oder lokales JAR unter `03_tools/releases/upr-fvx/` | offen | offen | nur nach Freigabe | read-only geprüft; spaeter Release/JAR oder Source-Clone entscheiden |
| CFRU-expansion | FireRed Gen9/CFRU-Basis | https://github.com/Shiny-Miner/CFRU-expansion | offen | `02_external/CFRU-expansion` | offen | offen | nur nach Freigabe | Hauptbasis-Kandidat; nicht geklont |
| DPE Gen9 | Pokémon Expansion | https://github.com/Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9 | offen | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | offen | offen | nur nach Freigabe | Hauptbasis-Kandidat; nicht geklont |
| Skeli789 CFRU | Upstream CFRU-Referenz | https://github.com/Skeli789/Complete-Fire-Red-Upgrade | n/a | `02_external/Complete-Fire-Red-Upgrade` | offen | offen | nein, Referenz zuerst | read-only geprüft; nicht geklont |
| Skeli789 DPE | Upstream DPE-Referenz | https://github.com/Skeli789/Dynamic-Pokemon-Expansion | n/a | `02_external/Dynamic-Pokemon-Expansion` | offen | offen | nein, Referenz zuerst | read-only geprüft; nicht geklont |
| CyanSMP64 NatDexExtension | IronMON/NatDex-Referenz | https://github.com/CyanSMP64/NatDexExtension | offen | `02_external/NatDexExtension` | `dev_new` | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | nein, read-only Referenz | read-only Source-Submodule; Analysevorlage, keine Drop-in-Annahme fuer CFRU/DPE |
| pret/pokefirered | FireRed Decomp-Referenz | https://github.com/pret/pokefirered | n/a | `02_external/pokefirered` | offen | offen | nein, Referenz zuerst | read-only geprüft; nicht geklont |
| Hex Maniac Advance | ROM-Analyse | offen | n/a | `03_tools/releases` | n/a | n/a | nein | Quelle offen; Tool-Binary nicht committen |
| BizHawk | Emulator | https://github.com/TASEmulators/BizHawk | n/a | `03_tools/releases` oder lokale User-Installation | n/a | n/a | nein | lokales Toolziel; kein Source-Submodule, keine Release-Zips/AppImages/Binaries committen |
| Ironmon Tracker | Tracker | https://github.com/besteon/Ironmon-Tracker | offen | `02_external/Ironmon-Tracker` | `main` | `c450ecaee2d8131a2789bb656e3be792a93712fb` | nein, read-only Referenz | read-only Source-Submodule; zentrale API-Quelle `ironmon_tracker/TrackerAPI.lua` |

## Lokale Submodule-Pins 2026-05-14

Arbeitsblock: `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write` | `2697511da9a97df4c29c00dfda8b40e556020489` | ja, nur in diesem Branch | Normal-Palette-Single-owner-Write-Guard fuer CFRU/DPE; Shiny/shared/invalid/missing/decode-failed/cross-kind Faelle werden nicht an den Palette-Rewriter uebergeben; Reload-Smoke noch offen |
| CFRU-expansion Fork | CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `02_external/CFRU-expansion` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | nein in diesem Block | read-only, unveraendert |
| DPE Gen9 Fork | DPE/Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | nein in diesem Block | read-only, unveraendert |
| CyanSMP64 UPR-ZX NatDex | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `02_external/references/cyansmp64-upr-zx-natdex` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | nein | read-only Referenz |
| CyanSMP64 FireRed NatDex | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `02_external/references/cyansmp64-pokefirered-natdex` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | nein | read-only Referenz |
| UPR-FVX upstream | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `02_external/references/upr-fvx-upstream` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | nein | read-only Referenz |
| Ajarmar UPR-ZX | UPR-ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `02_external/references/upr-zx-ajarmar` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | nein | read-only Referenz |
| pret FireRed | Vanilla-BPRE-Decomp | `https://github.com/pret/pokefirered.git` | `02_external/references/pret-pokefirered` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | nein | read-only Referenz |

Arbeitsblock: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte` | `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3` | ja, nur in diesem Branch | MoveData-Fairy-Type-Byte-Fix fuer CFRU/DPE; `Type.FAIRY` wird im sicheren MoveData-Gate als raw `0x17` gelesen/geschrieben; `FVX-MOVE-004` reloadet mit `writeReloadMoveDataMismatches=0`; kein TypeChart/TypeEffectiveness/Species-Type-Write |
| CFRU-expansion Fork | CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `02_external/CFRU-expansion` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | nein in diesem Block | read-only, unveraendert |
| DPE Gen9 Fork | DPE/Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | nein in diesem Block | read-only, unveraendert |
| CyanSMP64 UPR-ZX NatDex | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `02_external/references/cyansmp64-upr-zx-natdex` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | nein | read-only Referenz |
| CyanSMP64 FireRed NatDex | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `02_external/references/cyansmp64-pokefirered-natdex` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | nein | read-only Referenz |
| UPR-FVX upstream | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `02_external/references/upr-fvx-upstream` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | nein | read-only Referenz |
| Ajarmar UPR-ZX | UPR-ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `02_external/references/upr-zx-ajarmar` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | nein | read-only Referenz |
| pret FireRed | Vanilla-BPRE-Decomp | `https://github.com/pret/pokefirered.git` | `02_external/references/pret-pokefirered` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | nein | read-only Referenz |

Arbeitsblock: `compat/upr-fvx-cfru-dpe-move-data-write-preserve`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-move-data-write-preserve` | `bb5ee11978e38839979e654ff1c14ba60a0cde93` | ja, nur in diesem Branch | MoveData-Write-Preserve-Fix fuer CFRU/DPE; klassische MoveData-Bytes `+0..+4` bleiben geschrieben, `BattleMove.split` wird im CFRU/DPE-Gate bei `+10` geschrieben, Preserve-Bytes bleiben unangetastet; Reload-Smoke noch offen |
| CFRU-expansion Fork | CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `02_external/CFRU-expansion` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | nein in diesem Block | read-only, unveraendert |
| DPE Gen9 Fork | DPE/Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | nein in diesem Block | read-only, unveraendert |
| CyanSMP64 UPR-ZX NatDex | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `02_external/references/cyansmp64-upr-zx-natdex` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | nein | read-only Referenz |
| CyanSMP64 FireRed NatDex | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `02_external/references/cyansmp64-pokefirered-natdex` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | nein | read-only Referenz |
| UPR-FVX upstream | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `02_external/references/upr-fvx-upstream` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | nein | read-only Referenz |
| Ajarmar UPR-ZX | UPR-ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `02_external/references/upr-zx-ajarmar` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | nein | read-only Referenz |
| pret FireRed | Vanilla-BPRE-Decomp | `https://github.com/pret/pokefirered.git` | `02_external/references/pret-pokefirered` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | nein | read-only Referenz |

Arbeitsblock: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix` | `74d88a7ab1d306e1e09ccabb851dffd7f6922b66` | ja, nur in diesem Branch | Evolution-Same-Typing-Null-Type-Fix fuer CFRU/DPE; `FVX-TRAIT-019` im `FVX-TRAIT-016` Carrier mit Save/Log/Output/Reload und `writeReloadEvolutionMismatches=0` bestaetigt |
| CFRU-expansion Fork | CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `02_external/CFRU-expansion` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | nein in diesem Block | read-only analysiert |
| DPE Gen9 Fork | DPE/Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | nein in diesem Block | read-only analysiert |
| CyanSMP64 UPR-ZX NatDex | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `02_external/references/cyansmp64-upr-zx-natdex` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | nein | read-only Referenz |
| CyanSMP64 FireRed NatDex | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `02_external/references/cyansmp64-pokefirered-natdex` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | nein | read-only Referenz |
| UPR-FVX upstream | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `02_external/references/upr-fvx-upstream` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | nein | read-only Referenz |
| Ajarmar UPR-ZX | UPR-ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `02_external/references/upr-zx-ajarmar` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | nein | read-only Referenz |
| pret FireRed | Vanilla-BPRE-Decomp | `https://github.com/pret/pokefirered.git` | `02_external/references/pret-pokefirered` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | nein | read-only Referenz |

## Lokale Submodule-Pins 2026-05-13

Arbeitsblock: `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write` | `5c7170b654b09e1fc27ced6857dd50a8e4711f08` | ja, nur in diesem Branch | Encounter-Held-Items-Scope-and-Write-Fix fuer CFRU/DPE; basiert auf Abilities-Hidden-Ability-Scope-and-Write-Fix `639c7e61` |
| CFRU-expansion Fork | CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `02_external/CFRU-expansion` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | nein in diesem Block | read-only analysiert |
| DPE Gen9 Fork | DPE/Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | nein in diesem Block | read-only analysiert |
| CyanSMP64 UPR-ZX NatDex | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `02_external/references/cyansmp64-upr-zx-natdex` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | nein | read-only Referenz |
| CyanSMP64 FireRed NatDex | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `02_external/references/cyansmp64-pokefirered-natdex` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | nein | read-only Referenz |
| UPR-FVX upstream | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `02_external/references/upr-fvx-upstream` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | nein | read-only Referenz |
| Ajarmar UPR-ZX | UPR-ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `02_external/references/upr-zx-ajarmar` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | nein | read-only Referenz |
| pret FireRed | Vanilla-BPRE-Decomp | `https://github.com/pret/pokefirered.git` | `02_external/references/pret-pokefirered` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | nein | read-only Referenz |

## Workspace-Zielstruktur fuer Integration

| Pfad | Zweck | Git-Regel |
|---|---|---|
| `02_external/` | spaetere lokale Clone-Ziele fuer UPR FVX, CFRU/DPE und Referenzen | Clone-Inhalte nicht vendorisieren; Branch/Commit im Manifest pinnen |
| `03_tools/` | Tool-Dokumentation | committen |
| `03_tools/releases/` | UPR-FVX-JARs, BizHawk, Hex Maniac, Tool-Releases | lokal/ignored, nicht committen |
| `04_private_roms/` | private FireRed-ROM-Basis und lokale ROM-Arbeitskopien | lokal/ignored, nicht in ChatGPT hochladen |
| `05_builds/` | CFRU/DPE-Build-Ausgaben, gepatchte GBA, lokale Logs | lokal/ignored, nicht committen |
| `08_tests/` | Smoke-Test-Protokolle ohne ROM-Inhalte | committen |

## Randomizer-Smoke-Artefaktkonvention

Arbeitsblock: `maintenance/randomizer-smoke-artifact-cleanup`.

| Pfad | Zweck | Git-Regel |
|---|---|---|
| `08_tests/randomizer/README.md` | Index, Nummerierung und Latest-Markierung fuer Randomizer-Smoke-Protokolle | committen |
| `08_tests/randomizer/NNN_<kurzer-zweck>.md` | neue dauerhafte Randomizer-Smoke-Protokolle | committen |
| `05_builds/randomizer-smoke/NNN_<kurzer-zweck>/` | lokale ROM-/Log-/Output-Artefakte passend zum Protokoll | lokal/ignored, nicht committen |

Bestehende unnummerierte Protokolle unter `08_tests/randomizer/` bleiben vorerst unveraendert und werden ueber die README-Tabelle eingeordnet. Der neueste bestaetigte Stand wird in Markdown als `Latest` markiert; ein lokaler `latest`-Symlink ist nicht erforderlich.

## UPR-FVX Source Build

| Thema | Stand |
|---|---|
| Lokaler Pfad | `02_external/upr-fvx` |
| Einbindung | Git-Submodule auf `Planton361/universal-pokemon-randomizer-fvx` |
| Upstream | `upr-fvx/universal-pokemon-randomizer-fvx` |
| Arbeitsbranch | `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write` |
| Gepinnter Workspace-Stand | `2697511da9a97df4c29c00dfda8b40e556020489` auf `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`; enthaelt den CFRU/DPE-Normal-Palette-Single-owner-Write-Guard-Fix auf Basis der bisherigen MoveData-Fairy-Type-Byte-Fixkette |
| Buildsystem | Gradle Wrapper |
| Java | JDK 25 |
| JAR-Build | `./gradlew :random:jar` |
| GUI-Start | `./gradlew :random:launch` oder `java -jar random/build/libs/UPR-FVX.jar` |
| ROM-freie Tests | `./gradlew test` |
| ROM-Tests | `./gradlew :romio:testROMs`, `./gradlew :random:testROMs`; nur separat freigegeben |


## Linux/CachyOS-Inventur

Arbeitsblock: `setup/linux-toolchain-inventory`.

| Prüfpunkt | Status | Nachweisstand | Nächster Schritt |
|---|---|---|---|
| Git | gefunden | `/usr/bin/git`; Git 2.54.0 | keine Aktion |
| GitHub CLI (`gh`) | gefunden, Auth aktiv | `/usr/bin/gh`; gh 2.92.0; Auth-Refresh auf `setup/linux-gh-auth-refresh` erfolgreich | keine Aktion |
| Shell | gefunden | `$SHELL` ist `/bin/fish` | POSIX-kompatible Projektbefehle weiter bevorzugen |
| Java | gefunden | `/usr/bin/java`; OpenJDK 26.0.1 | UPR-FVX-Anforderung spaeter gegen konkrete Version pruefen |
| `make` | gefunden | `/usr/bin/make`; GNU Make 4.4.1 | keine Aktion |
| devkitPro/devkitARM | offen | nicht installiert oder nicht nachgewiesen; keine Installation durchgefuehrt | separaten Toolchain-Setup-Block planen |
| `arm-none-eabi-gcc` | fehlt | nicht im PATH gefunden | spaeter devkitPro/devkitARM oder ARM-Toolchain klaeren |
| `agbcc` | fehlt/optional | nicht im PATH gefunden | nur bei konkretem pret-/Build-Bedarf klaeren |
| `pwsh` | fehlt/optional | nicht im PATH gefunden | PowerShell-Checks unter Linux nur nutzen, wenn `pwsh` separat bereitgestellt wird |

## Linux/CachyOS GitHub-Auth-Refresh

Arbeitsblock: `setup/linux-gh-auth-refresh`.

- GitHub CLI und Git-Auth sind auf Linux/CachyOS wieder funktionsfähig.
- `gh` ist fuer Account `Planton361` authentifiziert; der Token-Wert wurde nicht übernommen.
- `git fetch origin` ist erfolgreich und bestätigt Remote-Zugriff auf `origin`.
- GitHub CLI und Git können fuer Push und PR-Erstellung genutzt werden.

## Linux/CachyOS GBA-Toolchain-Plan

Arbeitsblock: `setup/linux-gba-toolchain-plan`.

Planungsdokument: `01_docs/setup/linux-gba-toolchain-plan.md`.

| Thema | Stand | Naechster Schritt |
|---|---|---|
| devkitPro/devkitARM | primaere Richtung vorbereiten, aber nicht installieren | Installation/Check nur in separatem Arbeitsblock |
| `arm-none-eabi-gcc` | fehlt im PATH; soll im Kontext der Ziel-Toolchain geloest werden | pruefen, ob devkitARM oder Fallback-Paket genutzt werden soll |
| `agbcc` | fehlt/optional | erst bei konkretem pret-/Build-Bedarf bewerten |
| Build-Schritte | weiterhin gesperrt | erst nach Repo-Pinning, Toolchain-Freigabe und ROM-/Build-Freigabe |
| Externe Repos | weiterhin nicht geklont | erst nach separater Clone-/Fork-Entscheidung |

## Workspace Build and Randomizer Integration

Arbeitsblock: `planning/workspace-build-randomizer-integration`.

Planungsdokument: `01_docs/setup/workspace-build-randomizer-integration-plan.md`.

| Thema | Stand | Naechster Schritt |
|---|---|---|
| Private FireRed-ROM | bleibt nur lokal in `04_private_roms/`; keine ROM in Git/ChatGPT | separater `rom/fire-red-private-hash-check`-Block |
| devkitPro/devkitARM | Ziel-Toolchain fuer spaeteres Bauen | `setup/devkitpro-toolchain-install-check` nach Freigabe |
| CFRU/DPE Gen9 | Shiny-Miner-Forks bleiben Hauptkandidaten | Branch/Commit pinnen, bevor Clone/Fork/Build erfolgt |
| UPR FVX | Haupt-Randomizer-Kandidat | Release/JAR oder Source-Clone entscheiden; Java-Anforderung pruefen |
| `03_tools/releases/` | lokaler Ort fuer JARs/Tool-Binaries | ignored, nicht committen |
| `05_builds/` | lokaler Ort fuer Build-Ergebnisse | ignored, nicht committen |
| `08_tests/` | Testprotokolle ohne ROM-Inhalte | spaetere Smoke-Tests dokumentieren |

## Nicht-mutierende Linux-Prüfbefehle

```sh
command -v git && git --version
command -v gh && gh --version
gh auth status
printf '%s\n' "$SHELL"
command -v java && java -version
command -v make && make --version
command -v arm-none-eabi-gcc && arm-none-eabi-gcc --version
command -v agbcc || true
command -v pwsh && pwsh -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'
```

## Historischer Windows-Stand

Die folgenden Befunde stammen aus der Windows-Inventur vor dem OS-Wechsel und dürfen nicht als Linux-Ist-Stand verwendet werden:

| Tool | Historischer Windows-Befund |
|---|---|
| Git | Git 2.54.0 unter `c:\\devkitPro\\msys2\\usr\\bin\\git.exe` |
| GitHub CLI (`gh`) | 2.92.0, authentifiziert, aber nicht im damaligen PowerShell-PATH |
| PowerShell | Windows PowerShell 5.1.26100.8328 |
| PowerShell 7 (`pwsh`) | 7.6.1 |
| Java | Temurin OpenJDK 25.0.3+9 LTS |
| `make` | GNU Make 4.4.1 unter devkitPro/MSYS2 |
| `arm-none-eabi-gcc` | nicht im damaligen PATH gefunden |
| `agbcc` | optional; nicht im damaligen PATH gefunden |

## Nicht committen

- ROMs
- Saves
- Emulator States
- Builds
- Tool-Binaries
- private `.env`-Dateien
- Secrets
- lokale absolute private Pfade

## Naechste Manifest-Aufgabe

Naechster empfohlener Branch nach Review/Merge von `planning/workspace-build-randomizer-integration`: `setup/devkitpro-toolchain-install-check`.

Ziel: devkitPro/devkitARM installieren oder den freigegebenen Installationsweg ausführen und rein read-only pruefen. Keine Builds und keine ROM-Zugriffe.

Vor dem ersten Clone pro externer Quelle weiterhin festlegen:

- ob nur gelesen, geklont oder geforkt wird
- welcher Branch relevant ist
- welcher Commit-Hash gepinnt wird
- ob Codex Änderungen durchführen darf

## 2026-05-13 - UPR-FVX Egg-Move scope/write pin

- Workspace branch: `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write`.
- UPR-FVX branch: `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write`.
- UPR-FVX commit: `18168b78b973a4c39f34053ac58f21279a26d8d2`.
- Scope: gated CFRU/DPE Gen9 BPRE `gEggMoves` reader/writer plus high move-ID safety in Egg-Move randomization.

## 2026-05-13 - UPR-FVX Learnset-Write bounded pin

- Workspace branch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`.
- UPR-FVX branch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`.
- UPR-FVX commit: `77de517da880bebb6ed690ca6e170e5bd10b9cad`.
- Scope: gated CFRU/DPE Gen9 BPRE `setMovesLearnt()` full repointing writer for `gLevelUpLearnsets`; no Move-Data-Write, no Tutor text/menu rewrite, no Special Tutors, no Egg-Move expansion.

## 2026-05-13 - UPR-FVX Encounter Held Items scope/write pin

- Workspace branch: `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`.
- UPR-FVX branch: `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`.
- UPR-FVX commit: `5c7170b654b09e1fc27ced6857dd50a8e4711f08`.
- Scope: gated CFRU/DPE Gen9 BPRE Item-Scope, modern Bad-/Banned-Item filters, and `gBaseStats` Encounter Held Item read/write/reload for `item1`/`item2`.

## 2026-05-13 - UPR-FVX Learnset GUI flow safety pin

- Workspace branch: `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`.
- UPR-FVX branch: `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`.
- UPR-FVX commit: `086d2a9177df7624a0e7ca1876b210a200d7aa98`.
- Scope: gated CFRU/DPE Gen9 BPRE Learnset GUI flow safety: Logger null-safety, repeated `setMovesLearnt()` FreeSpace allocation, Trainer-Movesets missing-map fallback and TM/HM-/Tutor-Level-Up-Sanity fallback; no Move-Data-Write, Tutor text/menu rewrite, Special Tutors, Egg-Move expansion, Palette/Graphics or Text/Menu paths.


## 2026-05-13 - UPR-FVX Learnset-Write repointing pin

- Workspace branch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`.
- UPR-FVX branch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`.
- UPR-FVX commit: `77de517da880bebb6ed690ca6e170e5bd10b9cad`.
- Scope: gated CFRU/DPE Gen9 BPRE `setMovesLearnt()` full repointing writer for `gLevelUpLearnsets`; writes new blobs into validated FreeSpace, updates the existing pointertable by internal SpeciesSet ID, and leaves Move-Data-Write, Tutor text/menu rewrites, Special Tutors and Egg Moves out of scope.
