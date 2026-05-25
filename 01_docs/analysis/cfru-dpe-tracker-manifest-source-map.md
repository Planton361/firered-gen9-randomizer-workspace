# CFRU/DPE Tracker Manifest Source Map

Status: documentation-only source analysis. No ROMs, builds, saves, emulator states, raw logs, hashes, private paths or generated build artifacts were used.

## Executive summary

The Tracker extension can safely commit some manifest data directly from CFRU/DPE source:

- species, move and ability counts from DPE/CFRU constant headers;
- most enum ID mappings from `SPECIES_*`, `MOVE_*`, `ABILITY_*` and `ITEM_*` headers;
- many struct fields and offsets from CFRU `pokemon.h`, `battle.h` and `global.h`;
- ROM pointer-slot locations that are declared in source, as metadata locations only.

The extension should not commit local target addresses from a private build. Runtime addresses for party, battle mons, trainer tables, save blocks and repointed data tables must come from a source-symbol map, a public CFRU-owned metadata table, or local ignored override JSON.

The safest v1 plan is therefore split:

1. Commit source-derived counts, mappings and layout documentation.
2. Keep `game-addresses.json` and any local target-address override ignored/local.
3. Add a later generator or CFRU metadata table so the extension can discover real runtime/table addresses without private build data.

## Source-derived counts

| Field | Source | Value | Manifest action |
| --- | --- | ---: | --- |
| Species count | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`: `SPECIES_PECHARUNT 0x59F`, `NUM_SPECIES (SPECIES_PECHARUNT + 1)` | 1440 | Commit-safe as source-derived count, with ID 0 handling documented. |
| Move count | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/moves.h`: `MOVE_PSYCHICNOISE 0x3DF`, `MOVES_COUNT (MOVE_PSYCHICNOISE + 1)` | 992 | Commit-safe as source-derived count. |
| Ability count | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/abilities.h`: `ABILITY_PASTELVEIL 0xFE`; CFRU constants define `ABILITIES_COUNT (ABILITY_PASTELVEIL + 1)` | 255 | Commit-safe as source-derived count. |
| DPE item count | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/items.h`: `ITEM_PORTABLE_PC 0x307`, then free/shiny slots through `ITEMS_COUNT` | 799 | Commit-safe as a DPE source count, but not yet a final Tracker item count. |
| CFRU constants item count | `02_external/CFRU-expansion/include/constants/items.h`: `ITEM_PORTABLE_PC 0x307`, then three free slots through `ITEMS_COUNT` | 779 | Commit-safe as CFRU constants count, but conflicts with DPE item header count and needs reconciliation. |

Item count is the first manifest risk. The DPE header exposes additional shiny-space constants after `ITEM_PORTABLE_PC`, while the CFRU constants header only exposes three free-space slots. A generator should report both values until the actual build's item data table source of truth is confirmed.

## Layout findings

| Manifest area | Source | Source-backed finding | Risk / validation needed |
| --- | --- | --- | --- |
| `struct Pokemon` | `02_external/CFRU-expansion/include/pokemon.h` | CFRU uses a direct expanded party layout with visible growth/attack/condition/misc fields, `teraType`, `gigantamax` and `hiddenAbility`; it is not safe to assume vanilla encrypted Gen3 party substruct behavior. | Exact byte offsets after bitfields should be generated from compiler metadata or a CFRU metadata table before final Tracker overrides. |
| `struct BoxPokemon` | `pokemon.h` | Box data keeps personality/OT/nickname/header fields, then `teraType` and unencrypted substructs. | Tracker box support should be a later target; v1 should focus on live party and battle data. |
| `struct BattlePokemon` | `pokemon.h` | Source comments define battle-mon offsets; fields include species at 0x00, moves at 0x0C, ability at 0x20, types at 0x21/0x22, HP at 0x28, item at 0x2E and OT ID at 0x54. | Size is source-inferable as 0x58, but final manifest should prefer generated/validated size. |
| `struct BattleMove` | `pokemon.h` | 12-byte move struct: effect, power, type, accuracy, PP, chance, target, priority, flags, z-move power, split, z-move effect. | Commit-safe as a source-derived layout candidate. |
| `struct BaseStats` | `pokemon.h`, `DPE/include/base_stats.h` | Source comments place stats/types/items/abilities; hidden ability is at offset 0x1A. | Natural C alignment likely makes the row 0x1C bytes, matching Tracker stock size, but final manifest should validate. |
| Trainer structs | `02_external/CFRU-expansion/include/battle.h` | `struct Trainer` retains source-commented offsets through party pointer at 0x24 and likely size 0x28; expanded custom trainer mon includes ability, nature, IV spread, EV spread and Tera type. | Stock Tracker's custom trainer mon size is insufficient for CFRU expanded custom parties; static trainer-party display needs dedicated support. |
| Bag pockets | `02_external/CFRU-expansion/include/global.h` | Source defines pocket counts such as `BAG_ITEMS_COUNT 42`, `BAG_KEYITEMS_COUNT 30`, `BAG_POKEBALLS_COUNT 13`, `BAG_TMHM_COUNT 58`, `BAG_BERRIES_COUNT 43`. | SaveBlock pointer and exact runtime base remain address-dependent. |

## Address and table classification

| Manifest field | Source-backed clue | Classification | Manifest action |
| --- | --- | --- | --- |
| `gPlayerParty` | `BPRE.ld` declares `gPlayerParty = 0x2024284`; `pokemon.h` declares `extern struct Pokemon gPlayerParty[PARTY_SIZE]`. | Profile-specific symbol value. | Do not bake into public example as a final address; use local override or generated metadata. |
| `gEnemyParty` | `BPRE.ld` declares `gEnemyParty = 0x202402C`; `pokemon.h` declares `extern struct Pokemon gEnemyParty[PARTY_SIZE]`. | Profile-specific symbol value. | Local override or metadata table. |
| `gBattleMons` | `BPRE.ld` declares `gBattleMons = 0x2023BE4`; `battle.h` declares `extern struct BattlePokemon gBattleMons[MAX_BATTLERS_COUNT]`. | Profile-specific symbol value. | Local override or metadata table. |
| `gBattleMoves` | CFRU `repointall` declares pointer slot `080001CC`. | Source-backed pointer slot, not the final table address. | Commit pointer-slot metadata only; extension must dereference or generator must resolve. |
| `gSpeciesNames` | DPE `repointall` and CFRU `rom_locs.h` reference pointer slot `08000144`. | Source-backed pointer slot. | Commit pointer-slot metadata only. |
| `gBaseStats` / `gSpeciesInfo` | DPE `repointall` and CFRU `rom_locs.h` reference pointer slot `080001BC`; `BPRE.ld` also lists a legacy-style symbol. | Source-backed pointer slot plus possible linker symbol. | Prefer pointer-slot/metadata model; do not assume a private build target address. |
| `gMoveNames` | CFRU `repointall` declares pointer slot `0804EF84`. | Source-backed pointer slot. | Commit pointer-slot metadata only. |
| `gAbilityNames` | CFRU `repointall` declares pointer slot `080001C0`. | Source-backed pointer slot. | Commit pointer-slot metadata only. |
| `gItems` / item data | CFRU `rom_locs.h` uses pointer slot `080001C8`; CFRU `repointall` lists `gItemData 0809A8D8`. | Mixed source metadata; exact table target still profile/build dependent. | Resolve with generator/metadata before final address JSON. |
| `gTrainers` | CFRU `repoints` references `gTrainers 0800FC00`; NatDexExtension expects its own metadata pointer. | Source-backed repoint anchor, not proven compatible with NatDex metadata. | Local override or CFRU metadata table. |
| `sTMHMMoves` | User-facing Tracker needs it; local NatDexExtension has a NatDex-specific pointer slot. | Not fully proven for this CFRU/DPE profile from current source scan. | Treat as local override/metadata-needed. |
| SaveBlock / bag | `global.h` defines `struct SaveBlock1`, and `BPRE.ld` declares `gSaveBlock1`/`gSaveBlock2` pointer variables. | Runtime pointer-dependent. | Do not commit resolved local saveblock addresses; use runtime pointer read/metadata. |

## Commit-safe manifest fields

These can be generated into committed source-data examples or generated data once formatting is finalized:

- counts for species, moves and abilities;
- both DPE and CFRU item-count candidates, with a reconciliation status;
- enum-to-ID mappings from constants headers;
- source file references for name-table generation;
- `BattleMove` field offsets and size candidate;
- `BattlePokemon`, `BaseStats`, `Trainer` and TrainerMon layout candidates, marked as source-derived and ABI-validation-required where bitfields or padding are involved;
- pointer-slot metadata for source-declared repointed tables, clearly separated from final target addresses.

## Local override only

These must stay out of committed examples unless they come from a public source metadata table rather than a private build/runtime session:

- target addresses for `gPlayerParty`, `gEnemyParty`, `gBattleMons`, `gBattleMoves`, `gBaseStats`, `gSpeciesNames`, `gMoveNames`, `gAbilityNames`, `gItems`, `gTrainers`, `gTrainerClassNames` and `sTMHMMoves`;
- pointer values read from emulator memory or a local ROM;
- saveblock target addresses;
- local ROM markers, hashes, paths, screenshots, raw logs or generated map files from private builds.

## Long-term metadata table recommendation

The extension would be more robust if CFRU/DPE exposed a small public metadata table for Tracker-like tooling. It should provide:

- profile/schema version and engine marker;
- counts for species, moves, abilities, items and trainers;
- target addresses or pointer slots for party, battle, move, species, item, ability, trainer and TM/HM tables;
- struct sizes and offsets for Pokemon, BattlePokemon, BattleMove, BaseStats, Trainer and TrainerMon variants;
- bag/saveblock pointer model;
- optional display-name table pointers or generated mapping version.

This avoids teaching every Tracker extension to infer linker, repoint and runtime pointer behavior differently.

## Generator strategy

### v1: source-derived data only

Create a generator that reads CFRU/DPE headers and emits committed source-data:

- parse `SPECIES_*`, `MOVE_*`, `ABILITY_*`, `ITEM_*` constants;
- parse counts from `NUM_SPECIES`, `MOVES_COUNT`, `ABILITIES_COUNT` and item `ITEMS_COUNT`;
- report DPE/CFRU item count mismatch instead of hiding it;
- parse or curate display names from source tables only;
- emit no runtime target addresses.

### v1 local address JSON

Keep local, ignored `game-addresses.json` and `tracker-overrides.json` for smoke work. These files can use local symbols or runtime validation, but should not be committed unless all values are source-public and sanitized.

### v2: source-symbol generator

If a public map/symbol artifact exists, generate `game-addresses.json` from that artifact and validate it against source structs. The committed repo should still contain only example manifests unless the symbol artifact is itself safe and public.

### v3: CFRU metadata table

Add a CFRU-owned metadata table later. The Tracker extension can then read one stable marker/pointer and populate addresses and offsets from the ROM itself, similar in spirit to NatDexExtension's metadata approach but specific to this CFRU/DPE/Gen9 profile.

## Open questions

- Whether the final Tracker-facing base-stat table should be named `gBaseStats`, `gSpeciesInfo`, or both in the manifest schema.
- Which item count is authoritative for the final local build: DPE's 799 item IDs or CFRU constants' 779 item IDs.
- Exact compiler-derived sizes for expanded `struct Pokemon`, `struct BoxPokemon`, `struct BaseStats` and expanded TrainerMon variants.
- Whether `sTMHMMoves` has a stable source-declared pointer slot in the current CFRU/DPE profile or needs a new metadata entry.
- Whether static trainer-party display should be delayed until live party/battle reads are correct, because CFRU and randomizer logic can alter actual battle Pokemon at runtime.
