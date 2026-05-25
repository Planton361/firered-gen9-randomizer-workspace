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
| `data/source-data.json` | Generated source-derived counts and ID mappings from CFRU/DPE headers. |
| `data/game-addresses.example.json` | Example only. Copy locally to `game-addresses.json` after filling safe address values. |
| `data/tracker-overrides.example.json` | Example only. Copy locally to `tracker-overrides.json` after filling safe override values. |

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

Without local non-example `game-addresses.json` and `tracker-overrides.json`, the extension can only prove load/unload and source-data availability. It cannot yet prove live party, battle or trainer data correctness.
