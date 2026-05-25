# Tracker Lua Source Inventory

Status: documentation-only source inventory. No Tracker implementation, generator, ROM, build, save, emulator state, screenshot, raw log, hash, private path or true public manifest address was added.

## Executive summary

The current workspace already has enough source material to design the next CFRU/DPE/Gen9 Ironmon Tracker extension step:

- Tracker API and extension lifecycle sources define how an external Lua extension can load and unload.
- CFRU/DPE headers define source-derived counts, IDs and many struct/layout candidates.
- CFRU/DPE tables define move data, base stats, trainer data, trainer classes, item categories and learnsets.
- Repoint/source-symbol files define pointer-slot and repoint metadata, but not all final runtime target addresses.
- Local `offsets.ini` files exist under CFRU/DPE source folders, but they are ignored/generated local artifacts and must not be committed or copied wholesale into docs.

The safest next step remains a generator for source-derived names/counts/layout candidates first. Address loading should stay local override until a public metadata table or safe symbol source exists.

## Inventory table

| Source | Type | Data it can provide | Commit safety | Extension use | v1 priority | Risks / open questions |
| --- | --- | --- | --- | --- | --- | --- |
| `02_external/Ironmon-Tracker/ironmon_tracker/TrackerAPI.lua` | Extension API source | Extension-facing reads for player/enemy Pokemon, active battle Pokemon, move/ability/item/trainer info, and `loadGameSettingsFromJson` / `loadTrackerOverridesFromJson`. | Yes, source reference only. | Direct Lua API seam. | High | API loads address/override JSON, but correctness still depends on CFRU/DPE manifests. |
| `02_external/Ironmon-Tracker/ironmon_tracker/CustomCode.lua` | Extension lifecycle source | `loadExtension`, `enableExtension`, `startup`, `unload`, `beforeGameDataLoad`, `afterProgramDataUpdate`, `afterBattleDataUpdate`. | Yes. | Direct external extension hook model. | High | Per-frame hooks must stay lightweight. |
| `02_external/Ironmon-Tracker/ironmon_tracker/Memory.lua` | Memory API source | BizHawk/mGBA read helpers and write helpers. | Yes. | Read-only runtime validation and later extension reads. | High | Extension should not use write helpers. |
| `02_external/Ironmon-Tracker/ironmon_tracker/GameSettings.lua` | Tracker settings source | ROM address JSON import, tracker override import, stock ROM detection, address fields. | Yes. | JSON manifest compatibility target. | High | Stock FireRed JSON can be wrong for repointed CFRU/DPE tables. |
| `02_external/Ironmon-Tracker/ironmon_tracker/Program.lua` | Tracker core read model | Party reads, battle reads, trainer reads, bag/TM/HM reads and expected offset names. | Yes, source reference only. | Generator target for fields/offsets; analysis seam before wrapping anything. | High | Stock `readNewPokemon` assumes vanilla-like Pokemon decoding. |
| `02_external/Ironmon-Tracker/ironmon_tracker/data/PokemonData.lua` | Tracker static data source | Stock Pokemon table and data build model. | Yes. | Data-shape reference for generated source-data. | Medium | Static stock table cannot cover DPE Gen9 by itself. |
| `02_external/Ironmon-Tracker/ironmon_tracker/data/MoveData.lua` | Tracker static/runtime data source | Move build model and `readMoveInfoFromMemory`. | Yes. | Data-shape reference and runtime table reader reference. | High | Requires correct `gBattleMoves`, size and move count. |
| `02_external/Ironmon-Tracker/ironmon_tracker/data/AbilityData.lua` | Tracker static data source | Ability data model. | Yes. | Generated ability table target. | Medium | Stock model does not solve hidden ability selection. |
| `02_external/Ironmon-Tracker/ironmon_tracker/data/TrainerData.lua` | Tracker static trainer source | Stock route/trainer metadata and `Program.readTrainerGameData` usage. | Yes. | Best-effort trainer identity reference. | Low/medium | Static trainer party must not be treated as final battle truth for CFRU/randomizer. |
| `02_external/NatDexExtension/NatDexExtension.lua` | Extension pattern source | GameSettings wrapper, NatDex detection, data injection, metadata pointer reads for `gBattleMons`, parties, `gBattleMoves`, `gBaseStats`, `gTrainers`, `sTMHMMoves`. | Yes, source reference only. | Pattern for lifecycle, wrapping and metadata-driven updates. | High as reference | NatDex marker and metadata slots are CyanSMP64-specific; not drop-in for CFRU/DPE. |
| `03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua` | Workspace extension skeleton | Name/version/hooks, manual profile prep, real `game-addresses.json` and `tracker-overrides.json` loading. | Yes. | Current implementation baseline. | High | Skeleton does not load example JSON or provide data correctness yet. |
| `03_tools/tracker-extensions/CFRUDPEExtension/data/*.example.json` | Example JSON manifests | Desired schema shape, TODO address fields, source-derived count/layout candidates, pointer-slot policy. | Yes, example-only. | Manifest schema/prototype. | High | Must not be confused with ready-to-load real manifests. |
| DPE `include/species.h` and CFRU `include/constants/species.h` | ID/count headers | `SPECIES_*` IDs and `NUM_SPECIES`; current source-derived count is 1440. | Yes. | Generator input for species ID mapping. | High | Display names still need a name source or table pointer. |
| DPE/CFRU `moves.h` | ID/count headers | `MOVE_*` IDs and `MOVES_COUNT`; current source-derived count is 992. | Yes. | Generator input for move IDs. | High | Move display also needs names and `gBattleMoves` table data. |
| DPE/CFRU `abilities.h` | ID/count headers | `ABILITY_*` IDs and `ABILITIES_COUNT`; current source-derived count is 255. | Yes. | Generator input for ability IDs/names. | High | Hidden ability runtime selection needs Pokemon/BaseStats support. |
| DPE/CFRU `items.h` / `include/constants/items.h` | ID/count headers | `ITEM_*` IDs and `ITEMS_COUNT` candidates. | Yes. | Generator input for item IDs. | Medium | DPE item count 799 vs CFRU constants 779 must be reconciled before final item map. |
| `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c` | Source table | `gBaseStats[]`, species stats, types, items and abilities through Gen9. | Yes. | Generator input for Pokemon base data. | High | Needs exact row layout and source count alignment. |
| `02_external/CFRU-expansion/src/Tables/battle_moves.c` | Source table | `gBattleMoves[]`, move effect/power/type/accuracy/PP/split-related data. | Yes. | Generator input or runtime table validation source. | High | CFRU semantics exceed vanilla move fields. |
| `02_external/CFRU-expansion/src/Tables/trainer_data.c` and `trainer_parties.h` | Source tables | `gTrainers[]`, trainer names/classes, party pointers and party layouts. | Yes. | Trainer identity and optional static party context. | Medium | Runtime `gEnemyParty` remains first truth for randomized battles. |
| `02_external/CFRU-expansion/src/Tables/item_tables.c` | Source table | `gItemsByType`, fling table, graphics table, item categorization by `ITEMS_COUNT`. | Yes. | Later item category/name enrichment. | Medium | Item name source and DPE/CFRU count mismatch remain open. |
| `02_external/CFRU-expansion/src/Tables/level_up_learnsets.c` and DPE `src/Learnsets.c` | Source tables | `gLevelUpLearnsets` and species learnset mappings. | Yes. | Optional move learning / Tracker move context. | Low for v1 | Not required for first party/battle display. |
| CFRU `include/pokemon.h` | Struct/layout header | `struct Pokemon`, `BoxPokemon`, `BattlePokemon`, `BaseStats`, `BattleMove`, party externs. | Yes. | Struct size/offset generator input. | High | Bitfields/padding should be validated by metadata or compiler-derived checks. |
| CFRU `include/battle.h` | Struct/layout header | `struct Trainer`, TrainerMon variants, `gBattleMoves`, `gBattleMons`. | Yes. | Trainer and battle layout generator input. | High | Expanded custom TrainerMon rows differ from stock Tracker assumptions. |
| CFRU `include/global.h` | Save/Bag/Party layout header | Bag pocket counts, `struct SaveBlock1`, SaveBlock pointer extern. | Yes. | Bag/saveblock manifest design input. | Medium | SaveBlock target addresses are runtime pointer-dependent. |
| CFRU `include/data2.h`, `include/new/rom_locs.h` | Symbol/table declarations | Externs for `gSpeciesNames`, `gMoveNames`, `gAbilityNames`, `gTypeNames`; pointer-slot macros for `gItems`, `gSpeciesNames`, `gBaseStats`. | Yes. | Name table and pointer-slot metadata source. | High | Pointer slots are not final target addresses unless dereferenced. |
| CFRU/DPE `repointall` / `repoints` | Source repoint config | Pointers/repoint anchors for `gBattleMoves`, `gMoveNames`, `gAbilityNames`, `gSpeciesNames`, `gBaseStats`, `gLevelUpLearnsets`, `gTrainers`, `gTrainerClassNames`, `gTypeNames`. | Yes. | Generator metadata input for pointer slots/repoint anchors. | High | Some entries are anchors or pointer slots, not final runtime/table addresses. |
| CFRU/DPE `BPRE.ld` | Linker script source | RAM and ROM symbol declarations for selected vanilla/profile symbols. | Yes. | Symbol-source input and cross-check. | Medium | Linker values can be profile-specific and should not be overgeneralized. |
| CFRU/DPE `scripts/insert.py`, `scripts/build.py`, `scripts/make.py` | Build/insert scripts | How repoints, symbol tables, `generatedrepoints`, `offsets.ini` and `special_inserts` are produced/used. | Yes as source scripts. | Generator design input only. | Medium | Running these would create build artifacts; this block did not run them. |
| CFRU/DPE `special_inserts.asm` | Insert script source | Manual `.org` hooks and inserted code/table references. | Yes as source. | Analysis/cross-check for inserted symbol use. | Low/medium | Not a convenient manifest source by itself. |
| CFRU/DPE `offsets.ini` | Local ignored generated artifact | Symbol-to-address entries for useful symbols such as `gBattleMoves`, `gMoveNames`, `gAbilityNames`, `gTrainers`, `gLevelUpLearnsets`, `gTrainerClassNames`, `gTypeNames`, DPE `gBaseStats`, `gSpeciesNames`. | Local only; do not commit or copy wholesale. | Local override / symbol sanity check. | Medium for local smoke | Generated/ignored; may reflect local build/source state and not public truth. |
| CFRU/DPE `generatedrepoints` | Local ignored generated artifact | Generated repoint occurrences for symbols such as CFRU `gMoveNames`, `gAbilityNames`, `gItemData`, `gBattleMoves`, and DPE `gSpeciesNames`, `gBaseStats`, `gTMHMLearnsets`. | Local only; do not commit or copy wholesale. | Analysis hint for repoint coverage. | Low/medium | Generated/ignored; useful for diagnosis, not manifest publication. |

## `offsets.ini` assessment

Two local `offsets.ini` files are present:

- `02_external/CFRU-expansion/offsets.ini`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/offsets.ini`

Both are ignored by their submodule `.gitignore` files and are not tracked source. They are therefore useful local diagnostics, not commit-safe source data.

Relevant symbol types found in the local files:

- CFRU: `gAbilityNames`, `gBattleMoves`, `gItemsByType`, `gLevelUpLearnsets`, `gMoveNames`, `gTrainerClassNames`, `gTrainers`, `gTrainersWithEvsSpreads`, `gTypeNames`.
- DPE: `gBaseStats`, `gSpeciesNames`.

Not found in the checked symbol-name search:

- `gPlayerParty`
- `gEnemyParty`
- `gBattleMons`
- `gSaveBlock` / `SaveBlock`
- `sTMHMMoves`

Interpretation:

- `offsets.ini` can help local smoke produce temporary `game-addresses.json` values for table pointers and names.
- It does not currently appear sufficient by itself for live party/battle RAM addresses or SaveBlock/bag support.
- The file should not be committed, copied wholesale into docs, or treated as final public truth.

## Name-source notes

The inventory found source declarations and pointer slots for names:

- `gSpeciesNames` through DPE `repointall` and CFRU `include/new/rom_locs.h` / `include/data2.h`.
- `gMoveNames`, `gAbilityNames`, `gTypeNames` through CFRU `include/data2.h`, `repointall`, `repoints`, and runtime references.
- `gTrainerClassNames` in `src/Tables/trainer_data.c`.

The scan did not identify a simple committed C array for all species names equivalent to `gSpeciesNames[]` in the same way `Base_Stats.c` defines `gBaseStats[]`. A generator may need to derive species display names from source constants, DPE text assets, pointer-table extraction from safe public build metadata, or a curated source-data table.

## Recommended build order

1. **Generator input inventory lock-in**
   - Treat this document and `cfru-dpe-tracker-manifest-source-map.md` as the source boundary.
   - Do not add true local addresses yet.

2. **Source-derived data generator**
   - Parse species, move, ability and item constants.
   - Emit counts and ID mappings into a source-data format.
   - Report DPE/CFRU item-count mismatch explicitly.

3. **Layout candidate generator**
   - Parse or curate struct offsets for `BattleMove`, `BattlePokemon`, `BaseStats`, `Trainer` and TrainerMon variants.
   - Keep `struct Pokemon` party layout caveated until compiler/metadata validation exists.

4. **Manual local address override**
   - Use ignored local `game-addresses.json` / `tracker-overrides.json`.
   - Local `offsets.ini` may seed table pointers for smoke, but missing party/battle RAM symbols still need another source.

5. **Extension v1**
   - Use current `CFRUDPEExtension.lua` skeleton.
   - Load real local non-example manifests.
   - Prove player party, enemy party and active battle data before static trainer-party claims.

6. **Public metadata path**
   - Prefer a CFRU/DPE metadata table or safe symbol artifact later.
   - This should replace ad hoc local `offsets.ini` dependency for public users.

## Risks and assumptions

- `offsets.ini` and `generatedrepoints` are useful but local/generated/ignored; they are not public source-of-truth inputs.
- DPE/CFRU item count disagreement remains unresolved.
- Species names need a stronger source-derived path than just ID constants.
- Live party and battle RAM addresses are not fully solved by the currently found local `offsets.ini` symbols.
- Static trainer tables are useful for identity/context but not final randomized battle truth.
- No code implementation should start by modifying Tracker core; use the external extension and manifests first.
