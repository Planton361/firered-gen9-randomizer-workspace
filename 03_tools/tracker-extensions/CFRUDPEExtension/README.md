# CFRU/DPE Gen9 Tracker Extension

This directory contains the workspace-owned Ironmon Tracker extension skeleton for a future CFRU/DPE/Gen9 profile.

The extension is intentionally minimal:

- no Tracker-core fork;
- no NatDexExtension dependency or modification;
- no ROM, save, emulator state, build, screenshot, raw log, hash or private path data;
- no real local runtime/table addresses in committed JSON.

## Files

| Path | Purpose |
| --- | --- |
| `CFRUDPEExtension.lua` | External Tracker extension skeleton. It prepares a manual CFRU/DPE profile and loads only real non-example local manifests if present. |
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

1. Copy `CFRUDPEExtension.lua` into the Ironmon Tracker custom extension folder.
2. Copy this `data/` folder next to it as `CFRUDPEExtension/data/`.
3. Enable `CFRUDPEExtension` in Tracker.

Expected loader-only result:

- the extension loads and unloads without Tracker-core edits;
- `source-data.json` is read and counts are logged, currently species `1440`, moves `992`, abilities `255`, items `799`;
- missing `game-addresses.local.json` / `tracker-overrides.local.json` are reported as missing, not as failures;
- if local files are present, the extension calls `TrackerAPI.loadGameSettingsFromJson` and `TrackerAPI.loadTrackerOverridesFromJson` with those explicit paths and logs each return status.

Without local non-example `.local.json` manifests, the extension can only prove load/unload and source-data availability. It cannot yet prove live party, battle or trainer data correctness.

## Local address manifests

Start from the example files only for private local smoke:

```sh
cp data/game-addresses.example.json data/game-addresses.local.json
cp data/tracker-overrides.example.json data/tracker-overrides.local.json
```

Then replace TODOs locally from safe source metadata or sanitized local validation. Do not commit these `.local.json` files.
