# Pokemon Data Gen9 Inventory

Date: 2026-05-29

Branch: `analysis/pokemon-data-gen9-inventory`

Scope: source-backed inventory only. No CFRU, DPE, UPR-FVX, submodule pin, ROM, save, emulator state, build artifact, tool binary, raw log, screenshot, hash, private path, token, secret or `.env` data was changed.

## Method

- Read the workspace handoff docs first: `README.md`, `AGENTS.md`, `01_docs/PROJECT_BRIEF.md`, `01_docs/SESSION_STATE.md`, `01_docs/NEXT_STEPS.md`, and `01_docs/references/tool-manifest.md`.
- Used `rg --files` and targeted `rg` searches in:
  - `02_external/CFRU-expansion`
  - `02_external/Dynamic-Pokemon-Expansion-Gen-9`
- Checked external references read-only:
  - Pokemon Showdown data directory: <https://github.com/smogon/pokemon-showdown/tree/master/data>
  - pokeemerald-expansion Pokemon data directory: <https://github.com/rh-hideout/pokeemerald-expansion/tree/master/src/data/pokemon>
  - CFRU upstream family reference: <https://github.com/Skeli789/Complete-Fire-Red-Upgrade>
  - Shiny-Miner GitHub account/fork family reference: <https://github.com/Shiny-Miner>
  - Shiny-Miner DPE Gen 9 reference: <https://github.com/Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9>

## Current High-Level Finding

The local CFRU/DPE source already carries Gen9-era species and move markers through `SPECIES_PECHARUNT` and `MOVE_PSYCHICNOISE`.

- CFRU `include/constants/species.h` and DPE `include/species.h` define `SPECIES_IRON_BOULDER`, `SPECIES_IRON_CROWN`, `SPECIES_TERAPAGOS`, `SPECIES_TERAPAGOS_TERASTAL`, `SPECIES_TERAPAGOS_STELLAR`, and `SPECIES_PECHARUNT`; `NUM_SPECIES` is based on `SPECIES_PECHARUNT + 1`.
- CFRU `include/constants/moves.h` and DPE `include/moves.h` define late Gen9 moves including `MOVE_TERASTARSTORM`, `MOVE_MALIGNANTCHAIN`, `MOVE_THUNDERCLAP`, and `MOVE_PSYCHICNOISE`; `MOVES_COUNT` is based on `MOVE_PSYCHICNOISE + 1`.
- CFRU `src/Tables/level_up_learnsets.c` and DPE `src/Learnsets.c` both include Gen9 learnset blocks for starters, paradox Pokemon, box legends, Ogerpon, Hydrapple, Terapagos, and Pecharunt.
- Ability constants are less complete than species/moves. CFRU still sizes ability tables with `ABILITIES_COUNT (ABILITY_PASTELVEIL + 1)`, while several Gen9 ability names in CFRU/DPE are aliases to older effect IDs, for example `ABILITY_ORICHALCUMPULSE ABILITY_DROUGHT`, `ABILITY_HADRONENGINE ABILITY_ELECTRICSURGE`, and `ABILITY_POISONPUPPETEER ABILITY_PLUS`. That means Gen9-named assignments can exist without true Gen9-native ability behavior.

## Data Areas

| Data area | Source-backed paths | Data format | Owner | Classification | Risk | Build impact |
| --- | --- | --- | --- | --- | --- | --- |
| Level-up learnsets | DPE `src/Learnsets.c`; CFRU `src/Tables/level_up_learnsets.c` | `struct LevelUpMove { u16 move; u8 level; }`, per-species `static const` arrays with `LEVEL_UP_MOVE(level, move)` and `LEVEL_UP_END`, plus `gLevelUpLearnsets[...]` pointer table | Both DPE and CFRU | Pokemon data with engine-facing pointer table | Medium-high. The data is duplicated across DPE and CFRU, and form names can differ; Ogerpon form naming is one concrete sync risk. Move/species ID drift can break table lookup. | DPE learnsets are gated by `EXPAND_LEARNSETS`; CFRU has its own active table. Any real update needs a coordinated rebuild and a generated diff between the two copies. |
| Pokemon ability assignments | DPE `src/Base_Stats.c`; DPE `include/base_stats.h` | `struct BaseStats` fields `.ability1`, `.ability2`, `.hiddenAbility` using `ABILITY_*` constants | DPE | Pokemon data | Medium-high. Assignment edits affect wild/trainer ability generation, randomizer expectations, and hidden ability behavior. Gen9 alias constants can make a name look current while the battle effect remains older. | DPE rebuild and downstream CFRU/DPE ROM integration. If constants change, CFRU and DPE must remain ID-compatible. |
| Base stats | DPE `src/Base_Stats.c`; DPE `include/base_stats.h` | `const struct BaseStats gBaseStats[]` with HP/Atk/Def/Speed/SpAtk/SpDef, types, catch rate, EXP yield, EV yields, held items, gender, egg cycles/groups, friendship, growth rate, abilities and `noFlip` | DPE | Pokemon data | Medium-high. Stats, typing, catch rate, EXP yield, held item and egg data are broad runtime inputs and can affect randomizer assumptions. | DPE rebuild. Large data edits should be staged separately from learnsets/TM data. |
| TM/HM compatibility | DPE `src/TM_Tutor_Tables.c`; DPE `src/tm_compatibility/*.txt`; CFRU `src/item.c`; CFRU `include/new/item.h`; CFRU `config.h` | DPE has `gTMHMMoves[NUM_TMSHMS]` and 128 text compatibility files, one TM/HM header plus species names. CFRU reads generated bitsets through `gTMHMLearnsets`; `TM_HM_T` size changes with `NUM_TMSHMS`. | DPE data consumed by CFRU engine paths | Pokemon data plus engine bitset layout | High. TM order/count and bitset width are brittle. Compatibility text lists must match constants, species names and generated table order. | DPE table generation/rebuild plus CFRU runtime bitset reads. Count changes must be avoided unless the whole table path is audited. |
| Tutor compatibility | DPE `src/TM_Tutor_Tables.c`; DPE `src/tutor_compatibility/*.txt`; CFRU `include/constants/tutors.h`; CFRU `src/item.c`; CFRU `src/learn_move.c`; CFRU `config.h` | DPE has `gMoveTutorMoves[NUM_MOVE_TUTOR_MOVES]` and 152 text compatibility files. CFRU uses expanded tutor bitsets through `gTutorLearnsets` and scans `NUM_MOVE_TUTORS` in move-reminder/tutor paths. | DPE data consumed by CFRU engine paths | Pokemon data plus engine/menu/reminder data | High. Tutor count/order is especially sensitive; local source shows `NUM_MOVE_TUTORS 152` while tutor-related total constants also exist, so a count/order audit is required before edits. | DPE and CFRU rebuild. Tutor list/count edits should be last, after move IDs and compatibility generation are frozen. |
| Egg moves | DPE `src/Egg_Moves.c` | Flat `const u16 gEggMoves[]`; species markers use `SPECIES_* + EGG_MOVES_SPECIES_OFFSET`; list ends with `EGG_MOVES_TERMINATOR 0xFFFF` | DPE | Pokemon data | Medium. Data is compact and less structurally broad than TM/Tutor, but species marker/order mistakes can corrupt multiple lists. | DPE rebuild. Safer after species and move IDs are frozen. |
| Move data | CFRU `src/Tables/battle_moves.c`; CFRU `strings/attack_name_table.string`; CFRU `strings/attack_description_table.string`; CFRU `include/constants/moves.h`; DPE `include/moves.h` | CFRU `const struct BattleMove gBattleMoves[]` with move parameters/effects/flags; parallel string and constant tables; DPE mirrors move IDs for Pokemon data references | CFRU primary, DPE ID mirror | Engine data and battle data | High. True move behavior can require effect constants, battle scripts, flags, animations and text. ID/order drift would break learnsets and compatibility tables. | CFRU rebuild, and DPE rebuild only if constants used by DPE data change. Prefer no ID reorder. |
| Ability data | CFRU `include/constants/abilities.h`; CFRU `strings/ability_name_table.string`; CFRU `strings/ability_descriptions.string`; CFRU `assembly/data/ability_tables.json`; CFRU `src/ability_battle_effects.c`; CFRU `src/ability_util.c`; CFRU `include/new/ability_tables.h`; DPE `include/abilities.h` | CFRU constants, names/descriptions, JSON table metadata and battle/effect code; DPE mirrors constants for `Base_Stats.c` assignments | CFRU primary, DPE ID mirror | Engine data and Pokemon assignment dependency | Very high. Adding true Gen9 ability behavior is not just data: it can require new IDs, table sizes, battle hooks, utility checks, text and DPE assignment sync. Current aliases should be treated as compatibility shims, not evidence of full Gen9 ability effects. | CFRU rebuild and DPE rebuild if constants/assignments change. Do this only after a dedicated ability design/audit. |

## External Reference Assessment

Pokemon Showdown is the best machine-readable current-data reference for Gen1-9 species, learnsets, moves and abilities. Its `data` directory exposes `pokedex.ts`, `learnsets.ts`, `moves.ts`, and `abilities.ts`, making it suitable as an input to a converter or audit report. It should not be copied directly into CFRU/DPE because naming, form IDs, ability aliases, move effects and GBA table shapes do not match one-to-one.

pokeemerald-expansion is the best GBA-source comparison point. Its Pokemon data directory includes modernized `level_up_learnsets`, `species_info`, `all_learnables.json`, `egg_moves.h`, and related data files. It is useful for C data-shape comparison, compatibility matrix ideas and sanity checks, but it is not the active engine in this workspace.

The upstream CFRU/DPE family remains the format/engine reference for local edits. Shiny-Miner's DPE Gen9 repository describes itself as a tool to expand Pokemon in FireRed alongside CFRU, so it is the closest format sibling for DPE table layout. For CFRU, the public Shiny-Miner account is a useful fork-family reference point, while Skeli789 CFRU remains the canonical public upstream engine reference for battle, table and hook behavior. These are reference points, not drop-in data sources.

## Recommended Update Path

1. Freeze constants and mappings first: species IDs, form names, move IDs, ability IDs, `NUM_SPECIES`, `MOVES_COUNT`, `NUM_TMSHMS`, and `NUM_MOVE_TUTORS`.
2. Generate a read-only mapping/diff report from Pokemon Showdown to local CFRU/DPE constants, including unresolved names and form aliases.
3. Update DPE `Base_Stats.c` and Pokemon ability assignments before learnsets, while avoiding new ability IDs unless a CFRU ability-behavior branch exists.
4. Update CFRU move data only for moves that already have safe IDs/effects, or split true new-effect moves into a dedicated CFRU engine branch.
5. Update level-up learnsets in one primary source and mechanically verify the CFRU/DPE copies do not drift.
6. Update egg moves after species/move mapping is stable.
7. Update TM/HM compatibility after move IDs and TM order are frozen.
8. Update tutor compatibility last because tutor move count/order, move reminder behavior and expanded bitsets are the most brittle data path.
9. After each tranche, run source checks and a sanitized local build/smoke handoff without documenting ROM paths, hashes, raw logs or private local details.

## Risks And Assumptions

- CFRU and DPE duplicate several Pokemon-facing tables; source-backed updates need a sync check, not manual confidence.
- Gen9 species/move constants being present does not prove all Gen9 mechanics are implemented.
- Ability aliases are the biggest semantic trap: a Gen9 ability name can resolve to an older CFRU ability effect.
- TM/Tutor count/order changes can break bitset layout and menu/reminder logic.
- Form naming differences, especially Ogerpon form labels, need an explicit mapping table before any generated update.
- UPR-FVX may depend on local table shape, species IDs, move IDs and DPE/CFRU naming conventions; data changes should be reviewed against the randomizer after source build checks.

## Handoff Prompt

Continue from `analysis/pokemon-data-gen9-inventory`. Build a read-only converter/audit plan that maps Pokemon Showdown `pokedex.ts`, `learnsets.ts`, `moves.ts`, and `abilities.ts` names to local CFRU/DPE constants, reports unresolved species/forms/moves/abilities, and compares against DPE `Base_Stats.c`, DPE `Learnsets.c`, DPE egg/TM/tutor compatibility files, and CFRU `battle_moves.c`. Do not change data tables until the mapping report is reviewed.
