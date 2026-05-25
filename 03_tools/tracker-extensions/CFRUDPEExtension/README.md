# CFRU/DPE Gen9 Tracker Extension

This directory contains the workspace-owned Ironmon Tracker extension for a future CFRU/DPE/Gen9 profile.

The extension is intentionally minimal:

- no Tracker-core fork;
- no NatDexExtension dependency or modification;
- no ROM, save, emulator state, build, screenshot, raw log, hash or private path data;
- no real local runtime/table addresses in committed JSON.

## Files

| Path | Purpose |
| --- | --- |
| `CFRUDPEExtension.lua` | External Tracker extension. It prepares a manual CFRU/DPE profile, loads only real non-example local manifests if present, and owns a read-only `gBattleMons` diagnostic reader. |
| `data/source-data.example.json` | Human-readable example shape for source-derived data. |
| `data/source-data.json` | Committed generated source-derived counts and ID mappings from CFRU/DPE headers. The extension reads this file and logs current counts. |
| `data/game-addresses.example.json` | Example only. Copy locally to `game-addresses.local.json` after filling safe local address values. |
| `data/tracker-overrides.example.json` | Example only. Copy locally to `tracker-overrides.local.json` after filling safe local override values. |

Local-only files:

- `data/game-addresses.local.json`
- `data/tracker-overrides.local.json`

These local files are ignored by Git and must not contain committed ROM/runtime/build addresses, private paths, logs, hashes, saves or emulator-state data.

## Generate source data

Run from the workspace root:

```sh
python3 07_scripts/tracker/generate_cfru_dpe_source_data.py
```

The generator reads only source headers:

- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/moves.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/abilities.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/items.h`
- CFRU item constants only for the DPE-vs-CFRU item-count warning.

It writes:

```sh
03_tools/tracker-extensions/CFRUDPEExtension/data/source-data.json
```

Optional output path:

```sh
python3 07_scripts/tracker/generate_cfru_dpe_source_data.py --output /tmp/source-data.json
```

## Current data boundary

`source-data.json` contains only source-derived metadata:

- counts;
- ID mappings;
- fallback display names derived from macro constants;
- alias/duplicate warnings;
- the DPE-vs-CFRU item-count conflict warning.

It does not contain:

- ROM addresses;
- runtime addresses;
- values from `offsets.ini`;
- private build symbols;
- `game-addresses.json` or `tracker-overrides.json` local values.

## Local Tracker smoke

For local extension-load smoke, copy this extension outside Git-managed Tracker sources:

1. Copy `CFRUDPEExtension.lua` directly into the Ironmon Tracker extension folder, for example `Lua/extensions/CFRUDPEExtension.lua`.
2. Copy this `data/` folder next to it, for example `Lua/extensions/data/`.
3. Enable `CFRUDPEExtension` in Tracker.

Expected loader-only result:

- the extension loads and unloads without Tracker-core edits;
- `source-data.json` is read and counts are logged, currently species `1440`, moves `992`, abilities `255`, items `799`;
- missing `game-addresses.local.json` / `tracker-overrides.local.json` are reported as missing, not as failures;
- if local files are present, the extension calls `TrackerAPI.loadGameSettingsFromJson` and `TrackerAPI.loadTrackerOverridesFromJson` with those explicit paths and logs each return status.

Without local non-example `.local.json` manifests, the extension can only prove load/unload and source-data availability. It cannot yet prove live party, battle or trainer data correctness.

Manifest path resolution is relative to the folder containing the loaded `CFRUDPEExtension.lua` file. If that cannot be detected, the extension falls back to `FileManager.getExtensionsFolderPath()`. In both cases, manifest files are expected under `data/` directly below the extension folder.

## Active battle reader smoke

The extension includes a read-only CFRU/DPE `gBattleMons` diagnostic reader. It does not patch Tracker core, does not override `TrackerAPI.getActiveBattlePokemon`, does not inject into stock team screens, and does not write emulator memory.

Required local manifest key:

- `Addresses.gBattleMons` in `data/game-addresses.local.json`

Optional local manifest key:

- `Addresses.gBattlersCount`, used only to avoid reading stale rows before at least two battlers are active

When `gBattleMons` is available, the extension reads the left player and left opponent `BattlePokemon` rows using the source-backed row size `0x58`. The v1 fields are species, level, current HP, max HP, four moves, PP, ability, and held item. Species, move, ability, and item IDs are mapped through committed `data/source-data.json`.

Expected local status messages:

- `active-battle=missing gBattleMons` when the local address manifest does not provide the key;
- `active-battle=memory reader unavailable` if Tracker has not exposed its read API yet;
- `active-battle=waiting battlers=0` or similar when optional `gBattlersCount` says no battle is active;
- `active-battle=idle/no valid rows` during no-battle or battle-transition states;
- `active-battle=loaded rows=...` when one or both left-side rows look plausible;
- `active-battle=snapshot P:... | E:...` when the formatted battle snapshot changes.

The snapshot includes player/enemy species, level, HP/max HP, and four move slots with current PP where available. Snapshot logging is change-based, so repeated identical frames should not spam the Tracker console.

This is a diagnostic/helper state only. Read data is stored in `extension.state.activeBattleMons`, exposed through `extension.getActiveBattleMons()`, and formatted by `extension.formatActiveBattleMons()` for later extension-owned UI work.

### Local active battle debug smoke

Install/update these files in the local Tracker extension layout:

1. Copy `CFRUDPEExtension.lua` to `Lua/extensions/CFRUDPEExtension.lua`.
2. Copy committed `data/source-data.json` to `Lua/extensions/data/source-data.json`.
3. Provide local ignored `Lua/extensions/data/game-addresses.local.json` with `Addresses.gBattleMons`.
4. Keep local ignored `Lua/extensions/data/tracker-overrides.local.json` beside it if testing other layout overrides.
5. Optional: include `Addresses.gBattlersCount` to reduce transition/no-battle noise.

Expected sanitized debug output in battle is shaped like:

```text
active-battle=loaded rows=2
active-battle=snapshot P:<species> L<level> HP <hp>/<max> moves[...] | E:<species> L<level> HP <hp>/<max> moves[...]
```

Do not copy real address values, local JSON contents, ROM paths, raw logs, screenshots, hashes, saves, emulator states, or private paths into committed files.

## Local address manifests

Start from the example files only for private local smoke:

```sh
cp data/game-addresses.example.json data/game-addresses.local.json
cp data/tracker-overrides.example.json data/tracker-overrides.local.json
```

Then replace TODOs locally from safe source metadata or sanitized local validation. Do not commit these `.local.json` files.

### Generate local game addresses from offsets.ini

For local smoke, a generated CFRU/DPE `offsets.ini` can seed the ignored address manifest:

```sh
python3 07_scripts/tracker/generate_cfru_dpe_game_addresses_local.py --offsets path/to/offsets.ini
```

If CFRU and DPE produced separate local symbol files, repeat `--offsets` and the generator will merge recognized symbols:

```sh
python3 07_scripts/tracker/generate_cfru_dpe_game_addresses_local.py --offsets path/to/cfru-offsets.ini --offsets path/to/dpe-offsets.ini
```

Default output:

```sh
03_tools/tracker-extensions/CFRUDPEExtension/data/game-addresses.local.json
```

The generated file is local-only and ignored by Git. It may include table/name symbols such as `gBattleMoves`, `gMoveNames`, `gAbilityNames`, `gTrainers`, `gLevelUpLearnsets`, `gTrainerClassNames`, `gTypeNames`, `gBaseStats`, `gSpeciesInfo`, `gSpeciesNames`, and `sTMHMMoves` when present in the input. Missing live RAM symbols such as `gPlayerParty`, `gEnemyParty`, `gBattleMons`, SaveBlock, or bag-pocket symbols remain warnings and must be solved before claiming party, battle, or bag correctness.

### Generate local tracker overrides

For local layout smoke, generate the ignored override manifest from source-backed CFRU/DPE layout candidates:

```sh
python3 07_scripts/tracker/generate_cfru_dpe_tracker_overrides_local.py
```

Default output:

```sh
03_tools/tracker-extensions/CFRUDPEExtension/data/tracker-overrides.local.json
```

The generated override file contains only layout values for recognized Tracker sections: `Program`, `PokemonData`, and `MoveData`. It includes candidates for `BattleMove`, `BattlePokemon`, `BaseStats`, and Trainer header sizes/offsets. It intentionally does not emit ROM/RAM addresses, `offsets.ini` values, party `struct Pokemon` overrides, final bag SaveBlock addresses, or expanded CFRU TrainerMon support.

Before relying on it in Tracker, locally verify that `TrackerAPI.loadTrackerOverridesFromJson` updates the effective nested `*.Addresses` fields consumed by the read paths.
