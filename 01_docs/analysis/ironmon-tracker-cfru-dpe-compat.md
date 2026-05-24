# Ironmon Tracker CFRU/DPE Compatibility

Date: 2026-05-25
Branch: `analysis/ironmon-tracker-cfru-dpe-compat`
Scope: source-backed compatibility assessment only. No ROMs, saves, builds, emulator states, screenshots, raw logs, patches, or tool binaries were read or committed.

## Executive Summary

The stock Ironmon Tracker is built around per-game address profiles plus Gen 3 FireRed/Ruby/Sapphire/Emerald data layouts. It supports BizHawk and mGBA, and its FireRed path reads core runtime memory such as party Pokemon, battle Pokemon, move tables, base stats, trainer data, and save blocks.

Our CFRU/DPE/Gen9 target is not expected to be drop-in compatible with stock Tracker data reading. The largest risks are not emulator support; they are data-layout and table-model differences:

- CFRU uses a direct expanded `struct Pokemon` layout in source, while the Tracker reads encrypted Gen 3 Pokemon substructures.
- CFRU/DPE expands species through `SPECIES_PECHARUNT 0x59F` and `NUM_SPECIES (SPECIES_PECHARUNT + 1)`, while the Tracker's standard Pokemon data list is much smaller.
- CFRU/DPE uses expanded moves through `MOVE_PSYCHICNOISE 0x3DF` and `MOVES_COUNT (MOVE_PSYCHICNOISE + 1)`.
- CFRU/DPE item IDs extend through `ITEM_FREE_SPACE3 0x30A` / `ITEMS_COUNT`.
- CFRU repoints core tables such as `gBattleMoves`, `gLevelUpLearnsets`, and `gTrainers`; stock Tracker FireRed JSON points at vanilla addresses.
- NatDexExtension is useful as an extension pattern, but it is CyanSMP64 NatDex-specific and should not be treated as a drop-in CFRU/DPE extension.

The current `FLAG_SMART_TRAINER_AI` work should not materially affect Tracker memory compatibility. It changes trainer AI flags used by CFRU battle AI, not Pokemon structs, move tables, species IDs, item IDs, save layout, or battle memory addresses.

## Sources Checked

| Source | What was checked | Relevant finding |
| --- | --- | --- |
| `besteon/Ironmon-Tracker` `main` | README and Lua source fetched read-only to `/tmp` via GitHub raw URLs | Tracker is Lua for BizHawk/mGBA and supports FR/LG/R/S/E; source uses JSON address profiles and Gen 3 memory readers. |
| `CyanSMP64/NatDexExtension` `main` | README and `NatDexExtension.lua` fetched read-only to `/tmp` | Extension supports NatDex ROM hacks by adding data/resources and overriding addresses; hardcoded NatDex detection/address values make it CyanSMP64-specific. |
| `02_external/CFRU-expansion` | `include/pokemon.h`, `include/battle.h`, `src/config.h`, `docs/cfru_feature_matrix.md`, `offsets.ini` | CFRU source defines expanded Pokemon/BattleMove/BaseStats/Trainer structs and repointed tables. |
| `02_external/Dynamic-Pokemon-Expansion-Gen-9` | species, pokedex, item, move, base stat and species-map sources | DPE source provides Gen9 species/dex tables and expanded counts. |
| Workspace docs | Smart-AI source-port and patch verification docs | AI flag changes are behavior-side only and not table-layout changes. |

External source URLs used read-only:

- `https://github.com/besteon/Ironmon-Tracker`
- `https://raw.githubusercontent.com/besteon/Ironmon-Tracker/main/Ironmon-Tracker.lua`
- `https://raw.githubusercontent.com/besteon/Ironmon-Tracker/main/ironmon_tracker/GameSettings.lua`
- `https://raw.githubusercontent.com/besteon/Ironmon-Tracker/main/ironmon_tracker/Memory.lua`
- `https://raw.githubusercontent.com/besteon/Ironmon-Tracker/main/ironmon_tracker/Program.lua`
- `https://raw.githubusercontent.com/besteon/Ironmon-Tracker/main/ironmon_tracker/PokemonData.lua`
- `https://raw.githubusercontent.com/besteon/Ironmon-Tracker/main/ironmon_tracker/MoveData.lua`
- `https://raw.githubusercontent.com/besteon/Ironmon-Tracker/main/ironmon_tracker/GameAddresses/Pokemon%20FireRed%20v1.0.json`
- `https://github.com/CyanSMP64/NatDexExtension`
- `https://raw.githubusercontent.com/CyanSMP64/NatDexExtension/main/NatDexExtension.lua`

## Tracker Variants

| Variant | Source-backed behavior | Fit for CFRU/DPE/Gen9 |
| --- | --- | --- |
| Ironmon Tracker standard | README says the tracker is Lua for BizHawk v2.8+ or mGBA v0.10.0+ and supports FR/LG/R/S/E. `GameSettings.importAddressesFromJson()` loads per-ROM JSON addresses. | Good emulator baseline, but not enough for expanded CFRU/DPE data without custom address/data support. |
| NatDexExtension | `NatDexExtension.lua` defines itself as Nat. Dex ROM-hack support, checks a hardcoded `monCountAddress = 0x08000170`, expects count `1210`, adds Pokemon/move/type/resources, and overrides game settings. | Useful template for extension mechanics. Not drop-in because detection, table addresses, species/resources and counts are CyanSMP64 NatDex-specific. |
| BizHawk | `Memory.lua` uses BizHawk `memory.read_u8`, `memory.read_u16_le`, `memory.read_u32_le` with domain handling. | Best first local test target because Tracker UI is graphical on BizHawk and already target-aligned for the project. |
| mGBA | `Memory.lua` uses `emu:read8` and composes 16/32-bit reads; README notes mGBA Lua has limited drawing, so tracker is text-based there. | Secondary compatibility test. Use after BizHawk because display limitations make smoke evidence harder to interpret. |

## What The Tracker Reads

| Data | Tracker source | Read model | CFRU/DPE compatibility concern |
| --- | --- | --- | --- |
| Game address profile | `GameSettings.lua`, FireRed JSON | Reads ROM header version, loads `GameAddresses/Pokemon FireRed v1.0.json`, assigns `GameSettings.gBaseStats`, `gBattleMoves`, `gTrainers`, `pstats`, `estats`, etc. | CFRU repoints many tables. Stock FireRed JSON points at vanilla addresses such as `gBaseStats 0x8254784`, `gBattleMoves 0x8250C04`, `gTrainers 0x823EAC8`. |
| Player/enemy party | `Program.updatePokemonTeams()`, `Program.readNewPokemon()` | Iterates party slots with `sizeofPokemonStruct = 0x64`; reads encrypted Gen 3 substructures at offset `0x20`, using personality/OTID XOR and substructure permutation. | CFRU source has direct fields in `struct Pokemon`: `species`, `item`, `experience`, `moves`, EVs, IVs, `hiddenAbility`, `gigantamax`, `teraType`, stats. This does not match encrypted vanilla read logic. |
| Battle memory | `Battle.lua`, `Program.getPokemonTypes()` | Reads `gBattleMons`, `sizeofBattlePokemon = 0x58`, battle results, current moves, battler indexes and type bytes. | CFRU `struct BattlePokemon` still has recognizable offsets such as species `0x00`, moves `0x0C`, types `0x21/0x22`, and total through `otId 0x54`; actual runtime addresses still need smoke verification. |
| Base stats | `PokemonData.buildData()` | Reads `gBaseStats + id * 0x1C`; offsets include base stats `0x0`, types `0x6`, exp yield `0x9`, friendship `0x12`, abilities `0x16`. | CFRU `struct BaseStats` fields run through hidden ability at `0x1A`; the 0x1C stride may remain compatible after padding, but hidden ability and extension-specific offset changes need target-specific verification. |
| Moves | `MoveData.buildData()`, `MoveData.readMoveInfoFromMemory()` | Reads `gBattleMoves + moveId * 0xC`; packs power/type/accuracy/PP from a dword at offset `0x1`, and move category from flags offset `0x8`. | CFRU `struct BattleMove` is 12 bytes and source fields match effect/power/type/accuracy/PP/flags/split, so stride is promising. Address and move count/resource list still need CFRU/DPE-specific extension support. |
| Abilities | `PokemonData.buildData()`, `AbilityData.buildData()` | Reads two 1-byte abilities from BaseStats offset `0x16`; Tracker list is static unless extension adds data. | CFRU/DPE has `ABILITIES_COUNT (ABILITY_PASTELVEIL + 1)`, 1-byte IDs up to `0xFE`, and `hiddenAbility` in BaseStats. Tracker standard two-ability model misses hidden ability and renamed/mapped Gen9 ability semantics. |
| Items | Party/trainer readers plus Tracker static item data | Held items are read as 16-bit IDs; trainer items are read from trainer struct offsets. | CFRU/DPE items extend through `ITEM_FREE_SPACE3 0x30A`. Stock Tracker item names/categories will be incomplete for Gen9/Mega/Z/Dynamax/Tera/custom items. |
| Trainer data | `Program.readTrainerGameData()` | Reads `gTrainers + trainerId * 0x28`; offsets: `partyFlags 0x00`, class `0x01`, items `0x10`, double `0x18`, `aiFlags 0x1C`, size `0x20`, party pointer `0x24`; trainer party struct sizes are vanilla-oriented. | CFRU `struct Trainer` still matches 0x28 top-level offsets. But CFRU `TrainerMonItemCustomMoves` is expanded with ability, nature, IV spread, EV spread, and tera type, so Tracker's custom item/moves party parsing is not compatible with fully expanded parties. |
| Learned moves | `PokemonData.getLearnedMoves()` | Reads `gLevelUpLearnsets` pointer table, 2-byte `LEVEL_UP_MOVE` entries, move ID bits 0..8 and level bits 9..15. | DPE learnsets are `const struct LevelUpMove* const gLevelUpLearnsets[NUM_SPECIES]`; CFRU `struct LevelUpMove` is packed `u16 move; u8 level`, i.e. 3-byte source entries, not vanilla packed 2-byte entries. This is a likely incompatibility for learned move display. |

## CFRU/DPE Compatibility Risks

| Area | Source-backed CFRU/DPE evidence | Risk |
| --- | --- | --- |
| Species count and IDs | CFRU/DPE define `SPECIES_PECHARUNT 0x59F` and `NUM_SPECIES (SPECIES_PECHARUNT + 1)`. DPE defines `NATIONAL_DEX_PECHARUNT 1025`, `FINAL_DEX_ENTRY`, and `NATIONAL_DEX_COUNT FINAL_DEX_ENTRY + 1`. | Stock Tracker Pokemon data/resources will not cover CFRU/DPE species/forms/GMax/Tera forms. Species names, icons, type resources and dex mappings need a custom extension. |
| Pokemon party struct | CFRU `struct Pokemon` has direct `species`, `item`, `experience`, `moves`, EVs, stats, `teraType`, `gigantamax`, `hiddenAbility`. Tracker assumes encrypted vanilla Gen 3 substructures. | High. Player/enemy team reads can be wrong even if the 0x64 stride remains plausible. |
| Battle Pokemon struct | CFRU `struct BattlePokemon` has species, moves, IV bits, types, stat stages, ability, PP, HP, item, nickname, experience, personality, status and OT ID through 0x58. | Medium. Some battle reads may remain compatible, but address/profile and type/ability semantics must be tested. |
| Move count and IDs | CFRU `MOVE_PSYCHICNOISE 0x3DF`; `MOVES_COUNT (MOVE_PSYCHICNOISE + 1)`. | High for names/resources. Move struct stride likely remains 0xC, but Tracker move list and resources need Gen9 extension. |
| Move data struct | CFRU `struct BattleMove` has 12 bytes: effect, power, type, accuracy, PP, secondary chance, target, priority, flags, z move power, split, z move effect. Tracker reads 12-byte records and category from flags byte. | Medium. Basic power/type/accuracy/PP may be recoverable if address is correct; categories and Z/Max metadata need custom handling. |
| Abilities | CFRU `ABILITIES_COUNT (ABILITY_PASTELVEIL + 1)` with one-byte ability IDs; BaseStats has ability1, ability2, hiddenAbility. | Medium-high. Standard Tracker can read two ability bytes but not hidden ability and not updated Gen9 names/resources without extension. |
| Items | CFRU `ITEMS_COUNT (ITEM_FREE_SPACE3 + 1)`, with IDs through `0x30A`. | Medium-high. Held item IDs are 16-bit and readable, but names/categories/resources are incomplete in stock Tracker. |
| Trainer tables | CFRU `EXPAND_TRAINERS` is enabled; feature matrix says `repoints` repoints `gTrainers`; `offsets.ini` lists a repointed `gTrainers` address. | Medium-high. Top-level trainer struct still resembles Tracker expectations, but address and expanded custom party rows need support. |
| Level-up learnsets | CFRU source uses packed `struct LevelUpMove { u16 move; u8 level; }`, while Tracker reads vanilla 2-byte packed `LEVEL_UP_MOVE`. | High for learned move display and move-history inference if it uses level-up data. |
| Repointed tables | CFRU feature matrix says `repoints` covers `gLevelUpLearnsets`, `gTrainers`, trainer class names, experience, item/type tables; `repointall` covers `gBattleMoves`, move names, abilities, item data, movement tables. | High. A custom Tracker profile must derive addresses from the built ROM/symbol map or stable CFRU pointer slots, not vanilla JSON. |
| NatDexExtension fit | NatDexExtension hardcodes NatDex detection count `1210`, FireRed NatDex addresses such as `gBattleMoves 0x082635cc` and `gBaseStats 0x0826a5fc`, and adds its own data/resources. | Not drop-in. Use only as a pattern for a CFRU/DPE-specific extension. |

## NatDexExtension As Template

NatDexExtension is useful for these implementation ideas:

- Extension startup can detect a supported ROM and abort otherwise.
- Extension can append Pokemon/move/type/resources and then rebuild `PokemonData`, `MoveData`, and `AbilityData`.
- Extension can override `GameSettings` table addresses and `PokemonData` offsets.
- Extension can ship additional icon/type resources outside the main Tracker.

It is not a direct solution for this project:

- The ROM detection reads a hardcoded `monCountAddress = 0x08000170` and expects `1210`.
- It hardcodes CyanSMP64 NatDex FireRed/Emerald addresses, not CFRU/DPE addresses.
- It ships CyanSMP64 NatDex data/resources and randomizer profile folders.
- It does not solve CFRU's direct party `struct Pokemon` layout or CFRU trainer custom party extensions by itself.

## AI And Moveset Change Impact

`FLAG_SMART_TRAINER_AI` is not expected to change Tracker compatibility by itself:

- It changes CFRU battle AI flag selection in `GetAIFlags`.
- It does not alter `struct Pokemon`, `struct BattlePokemon`, `struct BattleMove`, `struct Trainer`, species IDs, move IDs, item IDs, or table addresses.
- Tracker may read `trainer.aiFlags` from trainer data, but the runtime flag hook does not rewrite the trainer table; it changes battle-time AI flags.

Other randomizer changes can affect Tracker display:

- New or randomized move IDs beyond the Tracker's data list require extended `MoveData`.
- Trainer custom party rows using CFRU's extended `TrainerMonItemCustomMoves` require a custom parser.
- Species/form IDs beyond stock Tracker/NatDexExtension lists require CFRU/DPE Pokemon data/resources.
- Item IDs beyond the stock item list require item name/category support.

## Compatibility Direction

Recommended approach:

1. Do not try to force stock Ironmon Tracker to read the CFRU/DPE ROM as vanilla FireRed.
2. Use BizHawk + standard Tracker as the first local smoke only to identify what fails cleanly.
3. Treat NatDexExtension as an implementation template, not a dependency.
4. Build a future CFRU/DPE extension or address profile that handles:
   - CFRU/DPE species count, names, forms, dex mapping, and icons.
   - CFRU/DPE move count, names, power/type/accuracy/PP/category, and resources.
   - CFRU direct party Pokemon layout.
   - CFRU/DPE BaseStats hidden ability and Gen9 ability list.
   - CFRU/DPE item IDs and names/categories.
   - CFRU repointed table addresses from a reliable build artifact or pointer table.
   - CFRU trainer custom party row layouts.

## Open Questions

- Can the built CFRU/DPE ROM expose stable pointer slots for all needed Tracker addresses, or does the extension need generated symbol/address metadata from the build?
- Does the current built ROM preserve Tracker-readable `gBattleMons` offsets in all battle modes used by Ironmon?
- Which Tracker screens depend on encrypted party data versus battle data, and can a CFRU extension override only the party reader cleanly?
- Is the level-up learnset display required for our first Tracker compatibility target, or can it be deferred?
- How much Gen9 icon/type/move/item resource coverage is required for a useful v1: text-only correctness first, or visual Tracker parity?
