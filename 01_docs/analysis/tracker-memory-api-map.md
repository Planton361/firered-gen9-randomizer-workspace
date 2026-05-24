# Ironmon Tracker Memory/API Map for CFRU/DPE

Status: source-backed analysis only. No ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths or binaries were read or documented.

## Executive summary

Stock Ironmon Tracker is built around vanilla Gen 3 memory layouts plus JSON-provided address tables. It reads live data through `Memory.lua`, resolves the active ROM in `GameSettings.lua`, then uses `Program.lua` and static data tables for Pokemon, moves, abilities, items and trainers. `TrackerAPI.lua` exposes that data to extensions.

NatDexExtension `dev_new` is a useful reference, but it is not a generic CFRU/DPE/Gen9 adapter. It activates only when `Memory.read32(0x08000170) == 1258`, then expects a NatDex-specific pointer/metadata table at fixed ROM addresses such as `0x080001bc`, `0x080001cc`, `0x08000228`, `0x0800027c`, `0x08000314` and `0x080004xx`.

CFRU/DPE breaks the stock assumptions in several independent ways: Gen9 species and move counts, expanded item IDs, expanded ability IDs, hidden ability handling, extra Pokemon fields such as Tera type and Gigantamax, expanded battle move fields, and richer trainer-party data for custom moves/items/IVs/EVs/nature/ability/Tera type. A small CFRU/DPE-specific Tracker extension is the safer path than forcing NatDexExtension on.

## Tracker read pipeline

| Area | Source-backed file/function | Tracker assumption | CFRU/DPE risk |
| --- | --- | --- | --- |
| Emulator memory access | `02_external/Ironmon-Tracker/ironmon_tracker/Memory.lua`, `Memory.initialize` | BizHawk uses memory domains; mGBA uses `emu:read*`. Tracker has write helpers but notes it should not write unless necessary. | API is usable, but all higher-level reads depend on correct addresses and layouts. |
| ROM detection | `GameSettings.lua`, `RomHeaders`, `RomVersions`, `GameSettings.initialize`, `getRomAddressesFilePath` | Reads ROM header software version at `0x080000BC` and loads a vanilla JSON from `ironmon_tracker/GameAddresses/`; otherwise reports unsupported. | A CFRU/DPE ROM can be unsupported, or worse, look like FireRed while tables are repointed, causing vanilla JSON reads to point at wrong data. |
| Party/enemy Pokemon | `Program.updatePokemonTeams`, `Program.readNewPokemon` | Player/enemy party pointers are `GameSettings.pstats`/`estats`; each slot advances by `sizeofPokemonStruct` default `0x64`; Pokemon data follows vanilla Gen III encrypted substructures. | CFRU/DPE has extra fields and direct struct use; vanilla-compatible first fields may not be enough for hidden abilities, Tera, Gigantamax or future form data. |
| Ability on Pokemon | `Program.readNewPokemon`; `PokemonData.getAbilityId` | Reads one ability selector bit from misc data and maps only ability slot 0/1. | CFRU/DPE has explicit hidden ability support in base stats and party data. |
| Battle Pokemon | `Program.getPokemonTypes`; `TrackerAPI.getActiveBattlePokemon` | Reads battle mon types from `GameSettings.gBattleMons + offsetBattlePokemonTypes`; default `sizeofBattlePokemon` is `0x58`. | CFRU battle structs include modern battle features; offsets must be verified from CFRU symbols, not assumed from stock. |
| Move data | `MoveData.buildData`, `MoveData.readMoveInfoFromMemory` | Static move table length drives reads; default battle move size is `0xC`; packed power/type/accuracy/PP plus optional split flag. | CFRU battle move struct is 12 bytes but includes `z_move_power`, `split`, and `z_move_effect`; DPE Gen9 has move IDs through `MOVE_PSYCHICNOISE`. Static Tracker move data ends before Gen9 unless extended. |
| Ability data | `AbilityData.buildData`, `AbilityData.isValid`, `AbilityData.getTotal` | Ability list is static and `buildData` intentionally does not read memory. | DPE abilities run through `ABILITY_PASTELVEIL 0xFE`; stock ability IDs/names are incomplete. |
| Pokemon data | `PokemonData.buildData`, `getTotal`, `getNatDexCompatible` | Static `PokemonData.Pokemon` length controls supported species; NatDex fallback assumes base total 411 and the NatDex extension. | DPE `NUM_SPECIES` is `SPECIES_PECHARUNT + 1`, not stock 411 and not NatDexExtension's `1258` marker model. |
| Items/bag | `TrackerAPI.getBagItems`, `Program.updateBagItems`, `Resources.Game.ItemNames` | Reads bag pockets from SaveBlock addresses and classifies only known item IDs/categories. | DPE item IDs reach `ITEMS_COUNT (ITEM_SHINY_SPACE20 + 1)` and include Gen4+ / Gen9 mechanic items, so names and categories need CFRU/DPE data. |
| Trainer data | `Program.readTrainerGameData`, `TrainerData.lua` | `struct Trainer` is `0x28`; trainer party flags are stock 0..3; static trainer mappings are FRLG/RSE oriented. | CFRU keeps trainer header offsets compatible but extends `TrainerMonItemCustomMoves` with ability, nature, IV spread, EV spread and Tera type, and runtime build logic can alter levels/species/EVs/friendship/PP. |

## Tracker API surface

`TrackerAPI.lua` is the central extension-facing API source. It exposes:

- Pokemon reads: `getPlayerPokemon`, `getEnemyPokemon`, `getActiveBattlePokemon`, `getPokemonInfo`.
- Battle reads: `inActiveBattle`, `getBattleOutcome`, `getPokemonTypes`.
- Ability/move/item reads: `getAbilityIdOfPokemon`, `getMoveInfo`, `getAbilityInfo`, `getBagItems`, `getItemName`, `getMoveIdFromTMHMNumber`.
- Trainer reads: `getOpponentTrainerId`, `getTrainerGameData`, `getTrainerInfo`, `getTrainersOnRoute`, `hasDefeatedTrainer`.
- Extension hooks: `loadGameSettingsFromJson` and `loadTrackerOverridesFromJson`.

This means a CFRU/DPE compatibility layer should prefer the supported API/override seams before patching Tracker internals directly. The main missing piece is correct data and address/layout metadata.

## NatDexExtension hooks

| Hook | Source-backed behavior | Compatibility implication |
| --- | --- | --- |
| Detection | `NatDexExtension.lua`, `checkIfNatDexROM`: `Memory.read32(0x08000170) == 1258`. | Our CFRU/DPE/Gen9 source does not prove this marker exists; DPE species count is based on `SPECIES_PECHARUNT + 1`, so stock NatDexExtension should not be assumed active. |
| Startup | `startup` and `overrideGameSettingsInitialize` keep `isNatDex=false` and return if detection fails. | If detection fails, NatDexExtension does not update Tracker addresses or data. |
| Core overrides | `overrideCoreTrackerFunctions` replaces Dex mapping, randomizer settings path, PokemonRevo data, ability/stat/move tracking helpers. | These overrides are NatDex-specific and include hard-coded ID mapping. |
| Data injection | `addNewPokemonData`, `addNewMoves`, `addNewAbilities` append NatDex tables after stock data. | This is not DPE data. It appends if stock slots 412/355/78 are absent, which is not a CFRU/DPE source-backed mapping. |
| Address metadata | `updateProgramAddresses` reads many offsets/sizes from fixed `0x080003ec` / `0x080004xx` metadata addresses. | CFRU/DPE would need to provide the same metadata table or a different extension must load equivalent values. |
| Runtime symbols | `updateGameSettings` reads `gBattleMons`, `gPlayerParty`, `gEnemyParty`, `gBattleMoves`, `gBaseStats`, `gLevelUpLearnsets`, `gTrainers`, `sTMHMMoves` from fixed ROM metadata addresses. | These symbol pointers are exactly what CFRU/DPE needs, but their NatDexExtension addresses are not proven for this ROM. |

## CFRU/DPE source facts

| Data | Source-backed fact | Tracker impact |
| --- | --- | --- |
| Species count | `Dynamic-Pokemon-Expansion-Gen-9/include/species.h`: `SPECIES_PECHARUNT 0x59F`, `NUM_SPECIES (SPECIES_PECHARUNT + 1)`. | Stock 411 and NatDexExtension marker `1258` are not enough for DPE Gen9. |
| Moves count | `Dynamic-Pokemon-Expansion-Gen-9/include/moves.h`: `MOVE_PSYCHICNOISE 0x3DF`, `MOVES_COUNT (MOVE_PSYCHICNOISE + 1)`. | Stock move table through Gen3 is incomplete; NatDexExtension move list is not proven to match DPE IDs. |
| Abilities | `Dynamic-Pokemon-Expansion-Gen-9/include/abilities.h`: abilities extend through `ABILITY_PASTELVEIL 0xFE`; Gen9 ability aliases follow. | Stock ability table through Gen3 is incomplete; ability names and tracking need DPE mapping. |
| Items | `Dynamic-Pokemon-Expansion-Gen-9/include/items.h`: items include modern mechanic items through `ITEM_PORTABLE_PC 0x307`; `ITEMS_COUNT` follows free/shiny slots. | Stock Tracker item names/categories are incomplete and can mislabel bag/held items. |
| Base stats | CFRU and DPE `struct BaseStats` include `ability1`, `ability2`, and `hiddenAbility`. | Tracker's one-bit ability selector cannot represent hidden ability without extra handling. |
| Pokemon struct | `CFRU-expansion/include/pokemon.h`: `BoxPokemon` and `Pokemon` include `teraType`; misc substruct includes `gigantamax` and `hiddenAbility`. | Stock `0x64` vanilla decode misses meaningful CFRU/DPE fields even when species/moves parse. |
| Battle moves | `CFRU-expansion/include/pokemon.h`: `struct BattleMove` includes effect, power, type, accuracy, PP, secondary chance, target, priority, flags, `z_move_power`, `split`, `z_move_effect`. | Size is still 12 bytes, but semantics exceed vanilla packed move data. Tracker needs confirmed offsets and expanded move names. |
| Trainer parties | `CFRU-expansion/include/battle.h`: `TrainerMonItemCustomMoves` includes ability, nature, IV spread, EV spread, held item, moves, and Tera type. | Stock trainer reader only decodes legacy default/custom move and held item layouts; it will miss custom spreads and Tera data. |
| Runtime trainer build | `CFRU-expansion/src/build_pokemon.c`: trainer build can set custom moves, held items, ability/nature, EV/IV spreads, Tera type, level scaling, and difficulty-specific EV/friendship behavior. | Reading static `gTrainers` is not enough to know final in-battle trainer Pokemon under all config/runtime modes. |
| Battle type/ability refresh | `CFRU-expansion/src/mid_battle_evo.c` reads types from `gSpeciesInfo` and ability through `GetAbilityBySpecies`; `util.c` exposes `GetHiddenAbility`. | A Tracker extension must align with CFRU's active species/ability tables, not just stock `gBaseStats` names. |

## Broken assumptions

1. Stock ROM selection is too narrow. `GameSettings.getRomAddressesFilePath` resolves only known vanilla ROM header versions to bundled JSON. CFRU/DPE needs explicit address/layout metadata.
2. Static resource tables are too small. `PokemonData`, `MoveData`, `AbilityData`, item names and trainer maps are stock/NatDex-oriented, not DPE Gen9.
3. Ability decoding is incomplete. Tracker maps one bit to ability 1/2; CFRU/DPE has hidden abilities in base stats and Pokemon data.
4. Trainer reads are static and partial. CFRU's runtime build path can alter levels, species, EVs, IVs, ability, nature, PP, friendship and Tera fields depending on flags/config/difficulty.
5. NatDexExtension is marker- and layout-specific. It is valuable as a pattern for extensions, but its `1258` detection, pointer table and ID maps are CyanSMP64/NatDex-specific.

## Minimal adaptation strategy

Preferred path: create a small CFRU/DPE Tracker extension rather than modifying Tracker core or forcing NatDexExtension.

Minimum extension responsibilities:

- Detect the CFRU/DPE ROM through a project-local, non-private marker or a user-selected profile. Do not document ROM hashes or private paths.
- Load CFRU/DPE address metadata for `gPlayerParty`, `gEnemyParty`, `gBattleMons`, `gBattleMoves`, `gBaseStats` / `gSpeciesInfo`, `gLevelUpLearnsets`, `gTrainers`, `sTMHMMoves`, bag pockets and save blocks.
- Override or populate `PokemonData`, `MoveData`, `AbilityData`, item names/categories and Dex mappings from DPE source-derived tables.
- Add hidden ability and CFRU/DPE form-field awareness for player/enemy party reads.
- Treat static trainer-party reads as best-effort only unless runtime build outcomes are validated in battle.

Fallback path: use stock Tracker only in a limited diagnostic mode for vanilla-compatible fields after local smoke validation. Do not rely on it for Gen9 names, hidden abilities, modern moves/items or trainer teams.

Riskier path: adapt NatDexExtension. This would require replacing its detection, metadata addresses, ID maps and data tables with CFRU/DPE-specific equivalents. It is source-backed as a pattern, not as a drop-in layer.

## Open questions

- Does the built CFRU/DPE ROM expose a stable symbol/metadata table that an extension can read without private paths?
- Which source should own generated Tracker data: DPE headers/tables directly, a build map/symbol artifact, or a curated JSON checked into workspace docs/tools?
- How much runtime trainer accuracy is required? Static `gTrainers` may be sufficient for route/trainer identity, but not for final battle Pokemon under randomizer and CFRU runtime options.
- Should hidden ability, Tera type, Gigantamax and other modern fields be visible in the Tracker UI immediately, or only parsed for correctness first?
