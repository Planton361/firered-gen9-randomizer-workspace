# CFRU/DPE Tracker Extension Design

Status: design only. No Tracker core code, CFRU/DPE source, ROM, save, build, emulator state, screenshot, raw log, hash or private path is part of this document.

## Executive summary

Stock Ironmon Tracker and NatDexExtension `dev_new` are useful references, but neither is a drop-in adapter for the CFRU/DPE/Gen9 ROM target. The safe implementation path is a separate external Tracker extension, for example `CFRUDPEExtension.lua`, plus a source-derived profile/manifest. The extension should load CFRU/DPE addresses, counts, sizes, offsets and data mappings without forking Tracker core.

The v1 target should be narrow: make the Tracker load the right CFRU/DPE species, move, ability and item names, then prove player party and active enemy battle data. Static trainer-party data should remain informational only, because CFRU builds trainer and wild parties at runtime through CFRU logic and randomizer output.

## Source-backed constraints

| Area | Source | Finding | Design impact |
| --- | --- | --- | --- |
| Extension loading | `02_external/Ironmon-Tracker/ironmon_tracker/CustomCode.lua` | `loadExtension` loads an external Lua extension, `enableExtension` runs `startup`, and `unload` is available for cleanup. | Implement as an external extension, not a Tracker-core fork. |
| Safe early hook | `CustomCode.beforeGameDataLoad` | Hook is explicitly intended for additions to `GameSettings.RomVersions` and custom game address JSON setup. | Use this hook to install a minimal `GameSettings.initialize` wrapper or register a CFRU/DPE profile before normal data load. |
| Runtime hooks | `CustomCode.afterProgramDataUpdate`, `afterBattleDataUpdate` | Hooks run every 30 frames after most memory or battle data is read. | Use only for lightweight post-read correction/validation; avoid per-frame heavy logic. |
| JSON address loading | `TrackerAPI.loadGameSettingsFromJson`, `TrackerAPI.loadTrackerOverridesFromJson`; `GameSettings.importAddressesFromJson`, `importTrackerOverridesFromJson` | Tracker already supports custom game address JSON and hard-coded value/address override JSON. | Prefer manifest-backed address and override loading before overriding core functions. |
| Party reads | `Program.updatePokemonTeams`, `Program.readNewPokemon` | Tracker reads `GameSettings.pstats` and `GameSettings.estats`, then decodes vanilla Gen 3 Pokemon structures. | v1 must validate CFRU `struct Pokemon` compatibility and add overrides for CFRU/DPE fields if needed. |
| Static trainer reads | `Program.readTrainerGameData` | Tracker reads `gTrainers` with vanilla-style trainer header and four legacy party layouts. | Do not treat static trainer party as final truth for CFRU/DPE randomizer runs. Prefer live `gEnemyParty`/`gBattleMons` for active enemies. |
| NatDex pattern | `02_external/NatDexExtension/NatDexExtension.lua` | NatDexExtension wraps `GameSettings.initialize`, detects via a NatDex-specific mon-count marker, updates addresses from fixed metadata slots, then extends data/resources. | Reuse the pattern, not the detection marker or CyanSMP64-specific address layout. |
| CFRU/DPE counts | DPE/CFRU headers | Species, moves, abilities and items are expanded beyond stock Gen 3. | Manifest must carry source-derived counts and IDs; stock Tracker data tables are insufficient. |
| CFRU/DPE runtime construction | `build_pokemon.c`, `wild_encounter.c` | Trainer and wild enemies are constructed into `gEnemyParty`; CFRU adds hidden ability, Gigantamax and Tera fields. | Live party/battle memory is the first fidelity target; static tables are secondary context. |

## Recommended architecture

Use a two-artifact extension:

- `CFRUDPEExtension.lua`: small external Tracker extension that manages lifecycle hooks, profile selection, data loading, cleanup and optional lightweight runtime correction.
- CFRU/DPE profile manifest files: generated or curated JSON/Lua data from source, containing addresses, sizes, offsets, counts and name/ID mappings.

The extension should follow this lifecycle:

| Hook | Responsibility |
| --- | --- |
| `beforeGameDataLoad` | Capture `GameSettings.initialize`; register or select a CFRU/DPE profile; arrange custom address/override JSON loading before the stock unsupported-game failure path. |
| `startup` | Check Tracker compatibility, resolve extension data paths, detect or confirm the CFRU/DPE profile, load mappings/resources, then rebuild Pokemon/move/ability data as needed. |
| `unload` | Restore wrapped functions, remove extension-owned overrides where possible, clear extension state and request Tracker restart if mutable global data tables were patched. |
| `afterProgramDataUpdate` | Optional v1.5+ validation/correction after party reads, limited to low-cost checks. |
| `afterBattleDataUpdate` | Optional v1.5+ battle-only correction for enemy battle data, dynamic types, active enemy fields or CFRU-only fields. |

Avoid a Tracker-core fork in v1. If a stock function must be wrapped, keep the override local to the extension, store the original function, and restore it in `unload`, matching the NatDexExtension cleanup pattern.

## v1 scope

v1 should do the smallest useful read-only compatibility layer:

- Manual profile activation first, with robust detection as an optional follow-up once a source-backed CFRU/DPE marker is identified.
- Load a CFRU/DPE GameSettings/address manifest and Tracker override manifest.
- Load or patch species, move, ability and item names/IDs for CFRU/DPE/Gen9.
- Rebuild Pokemon and move data from CFRU/DPE `gBaseStats` and `gBattleMoves` where the Tracker supports it.
- Prove player party display from `gPlayerParty`.
- Prove enemy display from live `gEnemyParty` and active `gBattleMons`.
- Treat wild enemies and trainer enemies as live runtime data first.
- Keep static trainer data limited to trainer identity, class/name and optional source context until runtime/randomizer fidelity is proven.

Out of scope for v1:

- Tracker-core refactor.
- BizHawk source submodule or bundled emulator/tool binaries.
- ROM patching, ROM hash detection, save parsing or committed local runtime artifacts.
- Full bag/item categorization beyond minimal item names and held-item sanity.
- Claiming static trainer-party tables as final battle truth.
- Writing to emulator memory.

## Manifest design

A CFRU/DPE profile manifest should be explicit enough that the extension can be public and reproducible without private ROM paths or runtime logs.

Suggested top-level sections:

```json
{
  "profile": {
    "id": "cfru-dpe-gen9",
    "displayName": "CFRU/DPE Gen9 FireRed",
    "activation": "manual-first",
    "engine": "firered-cfru-dpe"
  },
  "markers": {
    "mode": "manual-or-source-marker",
    "notes": "No ROM hash or private path detection."
  },
  "counts": {
    "species": "source-derived",
    "moves": "source-derived",
    "abilities": "source-derived",
    "items": "source-derived"
  },
  "addresses": {
    "gPlayerParty": "runtime pointer/address",
    "gEnemyParty": "runtime pointer/address",
    "gBattleMons": "runtime pointer/address",
    "gBaseStats": "table pointer/address",
    "gBattleMoves": "table pointer/address",
    "gSpeciesNames": "table pointer/address",
    "gMoveNames": "table pointer/address",
    "gAbilityNames": "table pointer/address",
    "gItems": "table pointer/address",
    "gTrainers": "table pointer/address"
  },
  "sizes": {
    "Pokemon": "source-derived",
    "BattlePokemon": "source-derived",
    "BattleMove": "source-derived",
    "BaseStats": "source-derived",
    "Trainer": "source-derived",
    "TrainerMon": "source-derived"
  },
  "offsets": {
    "Pokemon": {},
    "BattlePokemon": {},
    "BattleMove": {},
    "BaseStats": {},
    "Trainer": {},
    "Bag": {}
  },
  "mappings": {
    "species": "id-to-name/source-id map",
    "moves": "id-to-name/source-id map",
    "abilities": "id-to-name/source-id map",
    "items": "id-to-name/source-id map",
    "types": "type-id map"
  }
}
```

The manifest should be split if needed:

- `game-addresses.json`: values compatible with `TrackerAPI.loadGameSettingsFromJson`.
- `tracker-overrides.json`: values compatible with `TrackerAPI.loadTrackerOverridesFromJson`.
- `data/*.lua` or `data/*.json`: generated source-derived names and ID maps.

## Source-derived data

These can be generated from CFRU/DPE source without reading a ROM:

| Data | Source-backed basis | Notes |
| --- | --- | --- |
| Species IDs/count | DPE/CFRU `include/species.h` / constants headers | Must include Gen9 IDs and any special/filler IDs. |
| Move IDs/count | DPE/CFRU `include/moves.h`; CFRU `gBattleMoves` table | Tracker move table must cover expanded move IDs. |
| Ability IDs/count | DPE/CFRU `include/abilities.h`; CFRU ability name table declarations | Hidden ability requires source support beyond stock two-ability display. |
| Item IDs/count | DPE/CFRU `include/items.h`, CFRU item tables and item accessors | CFRU and DPE item count definitions should be reconciled before public v1. |
| Species names | DPE string table and CFRU symbol declarations | Needed before Gen9 species display can be trusted. |
| Move data | CFRU `src/Tables/battle_moves.c` and `struct BattleMove` | Tracker already reads power/type/accuracy/PP/category if offsets and sizes are correct. |
| Base stats and abilities | DPE/CFRU `BaseStats` source and struct definitions | Must include ability1, ability2 and hiddenAbility. |
| Trainer struct metadata | CFRU `include/battle.h`, `src/Tables/trainer_data.c` | Static data is not final battle truth but still useful for names/classes. |
| Runtime struct layouts | CFRU `include/pokemon.h`, `include/battle.h` | Needed for party, battle, Tera, hidden ability and Gigantamax fields. |
| Repointed table anchors | CFRU/DPE `repointall`, `rom_locs.h`, source symbol declarations | Useful for manifest generation; exact runtime pointers still need local validation. |

## Runtime data

These must be read from emulator memory during a local test session:

| Runtime data | Why needed |
| --- | --- |
| `gPlayerParty` / Tracker `pstats` | Player party slots, levels, HP, moves, PP, item and ability display. |
| `gEnemyParty` / Tracker `estats` | Wild and trainer enemy party as actually constructed by CFRU/randomizer runtime logic. |
| `gBattleMons` | Active battle HP/status/types/stat stages and battle-side fields. |
| `gTrainerBattleOpponent_A` / optional B | Active trainer identity and class/name lookup. |
| `gBattleTypeFlags` and battle outcome/state | Distinguish wild, trainer, double and special battle contexts. |
| SaveBlock bag pockets | Later item/bag support; not required for first party/battle v1. |
| CFRU-only Pokemon fields | Hidden ability, Tera type and Gigantamax state require validation against CFRU struct layout. |

Static `gTrainers` should not be used as the final source for active enemy team display in the Randomizer target. CFRU builds trainer parties into `gEnemyParty`, and difficulty/config/randomizer logic can alter level, moves, held item, ability, IV/EV spread, PP or other fields before battle.

## Tracker API and hook use

Recommended v1 hook use:

- `beforeGameDataLoad`: install a minimal GameSettings initialization wrapper and/or prepare custom profile JSON paths.
- `startup`: load source-derived data/mappings and apply address/override manifests.
- `unload`: restore original functions and require refresh/restart if global data tables were changed.
- `afterProgramDataUpdate`: optional sanity checks after Tracker party reads; avoid expensive work.
- `afterBattleDataUpdate`: optional battle-only correction for active enemy display after stock battle memory update.

Recommended v1 API use:

- `TrackerAPI.loadGameSettingsFromJson` for GameSettings addresses.
- `TrackerAPI.loadTrackerOverridesFromJson` for Tracker offsets/sizes.
- `TrackerAPI.getPlayerPokemon`, `getEnemyPokemon`, `getActiveBattlePokemon` for validation during local smoke.
- `TrackerAPI.getPokemonInfo`, `getMoveInfo`, `getAbilityInfo`, `getItemName` for data-table sanity checks.

Avoid memory writes. `Memory.lua` supports writes, but also states that the Tracker should not write to memory unless absolutely necessary. This extension should stay read-only.

## Detection strategy

Use manual profile activation for v1. This avoids false positives and avoids depending on a private ROM hash or a NatDex-specific metadata layout.

Robust detection can be added later if source-backed markers are introduced or identified, for example:

- a project-local metadata table embedded in the ROM by build/source config;
- a source-derived count/pointer marker that is stable for this CFRU/DPE profile;
- a Tracker extension setting that selects the CFRU/DPE profile explicitly.

Do not reuse NatDexExtension's `Memory.read32(0x08000170) == 1258` marker unless the CFRU/DPE build is proven to expose the same marker semantics.

## Test matrix

| Phase | Setup | Checks | Pass condition |
| --- | --- | --- | --- |
| Load/unload | Enable `CFRUDPEExtension.lua`, then disable it. | Extension starts, applies profile, unloads without persistent broken state. | No Tracker-core edits; cleanup restores wrapped functions. |
| Manual profile | Select CFRU/DPE profile explicitly. | GameSettings shows supported CFRU/DPE profile instead of unsupported stock game. | Profile loads without ROM path/hash logging. |
| Species data | Sample Gen1, mid-dex and Gen9 species. | IDs, names, base stats, types and abilities. | Values match CFRU/DPE source-derived manifest. |
| Move data | Sample stock, expanded and Gen9 moves. | Name, type, power, accuracy, PP and category. | Values match CFRU `gBattleMoves` and mappings. |
| Ability data | Sample ability1, ability2 and hidden ability cases. | Ability ID/name resolution. | Hidden ability does not collapse into stock ability 1/2 only. |
| Item data | Sample held items and bag items later. | Item ID/name/category where supported. | Names are plausible; bag categorization can remain caveated in v1. |
| Player party | Local party with multiple occupied slots. | Species, level, HP, moves, PP, held item, ability. | Tracker display matches observed in-game state from sanitized manual check. |
| Wild enemy | Enter a wild battle. | Enemy species, HP, moves, ability and dynamic battle data. | Live `gEnemyParty`/`gBattleMons` display is plausible. |
| Trainer enemy | Enter a trainer battle. | Active enemy data and trainer identity. | Live enemy display is plausible; static trainer party is not overclaimed. |
| CFRU-only fields | Sample hidden ability, Tera or Gigantamax if available. | Extension does not misreport or crash on expanded fields. | Unsupported fields are either correct or explicitly hidden/caveated. |

## Risks and assumptions

- This design assumes the Tracker's extension API is stable enough to load custom address JSON and data overrides without a core fork.
- NatDexExtension is only a pattern. Its detection marker and metadata layout are CyanSMP64/NatDex-specific until proven otherwise.
- CFRU/DPE source gives counts and layouts, but exact runtime addresses still require a source-derived manifest and local sanitized validation.
- Static trainer tables are not enough for the Randomizer target because CFRU/runtime logic constructs actual battle Pokemon.
- Hidden ability, Tera and Gigantamax may require a small extension-side read correction if stock `Program.readNewPokemon` cannot represent them.
- Item support is likely a v1.5/v2 topic because item IDs, item names, pockets and categories need separate reconciliation.
- Public extension packaging must avoid ROMs, saves, emulator states, private paths, logs, screenshots, hashes and bundled tool binaries.

## Recommended next step

Create a source-derived CFRU/DPE manifest prototype, then implement the smallest external `CFRUDPEExtension.lua` that manually loads that profile and proves player party plus active enemy battle display. Keep BizHawk local and do not fork Tracker core unless the extension API proves insufficient.
