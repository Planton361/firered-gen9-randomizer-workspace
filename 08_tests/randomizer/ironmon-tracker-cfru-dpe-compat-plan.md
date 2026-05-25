# Ironmon Tracker CFRU/DPE Compatibility Smoke Plan

Status: local manual plan only. Do not commit ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths or tool binaries.

## Purpose

Validate whether stock Ironmon Tracker, NatDexExtension `dev_new`, or a future CFRU/DPE-specific extension can read a CFRU/DPE/Gen9 FireRed-based ROM plausibly.

The source map in `01_docs/analysis/tracker-memory-api-map.md` predicts that stock Tracker/NatDexExtension will not be sufficient without CFRU/DPE-specific address and data metadata.

## Safety boundaries

- Use local ROMs and emulator state only outside committed artifacts.
- Record only sanitized pass/fail notes.
- Do not document ROM paths, ROM hashes, private directories, screenshots, raw logs, save data or emulator states.
- Do not force Tracker memory writes as part of compatibility smoke.
- BizHawk remains a local tool; no BizHawk binaries or source are added to the repo.

## Smoke matrix

| Case | Setup | What to check | Expected current result |
| --- | --- | --- | --- |
| Stock Tracker | Load the CFRU/DPE/Gen9 ROM with Ironmon Tracker only. | Whether Tracker recognizes the game; whether player species, level, current HP, moves and ability display plausibly. | Likely unsupported or partially wrong if vanilla FireRed address JSON is applied to repointed CFRU/DPE tables. |
| Stock Tracker battle read | Enter a simple trainer/wild battle locally. | Active player/enemy Pokemon, battle HP, status, types and enemy move display. | Requires validation; stock offsets may miss CFRU/DPE expanded fields. |
| NatDexExtension dev_new | Enable the local NatDexExtension source in Tracker. | Whether the extension detects the ROM as NatDex and runs its address/data updates. | Expected not to activate unless `Memory.read32(0x08000170) == 1258`; do not force it on without a separate source-backed experiment. |
| NatDexExtension data sanity | If it activates naturally, inspect species/move/ability names for DPE Gen9 examples. | Gen9 species, moves, abilities, items and forms should match CFRU/DPE source IDs. | Likely mismatch unless the ROM uses CyanSMP64 NatDex metadata and ID maps. |
| Future CFRU/DPE extension | Load a purpose-built CFRU/DPE extension or custom address JSON. | Player party, enemy party, active battle Pokemon, species names, moves, abilities, held items, bag items and trainer data. | Target path. Requires generated CFRU/DPE metadata first. |

## Pass criteria for a future CFRU/DPE extension

- Player party species/name/level/current HP/max HP/moves/PP/held item are plausible for all occupied slots.
- Ability display handles ability 1, ability 2 and hidden ability cases.
- Active battle reads show correct player and opponent species, HP, status and dynamic types.
- Move names/types/power/accuracy/PP match CFRU/DPE source data for sampled Gen1, mid-dex and Gen9 moves.
- Item names/categories match DPE item IDs for sampled bag and held items.
- Trainer lookup identifies the active trainer and does not claim static party details that runtime randomizer/CFRU build logic can invalidate.

## Recommended next implementation step

Do not patch stock Tracker first. Build a small source-derived data/address manifest for CFRU/DPE, then prototype a minimal Tracker extension that loads those values through `TrackerAPI.loadGameSettingsFromJson`, `TrackerAPI.loadTrackerOverridesFromJson`, or NatDexExtension-style overrides.

The first prototype should target read-only display correctness for party, active battle, move names and abilities. Trainer-party fidelity and full item categorization can follow after the basic memory map is proven.

## CFRU/DPE extension design follow-up

Use `01_docs/analysis/cfru-dpe-tracker-extension-design.md` as the implementation concept for the future adapter.

Minimal extension smoke should use an external `CFRUDPEExtension.lua` plus source-derived manifests, not a Tracker-core fork. v1 should start with manual profile activation, load CFRU/DPE counts/addresses/sizes/offsets and name mappings, then prove:

- player party display from live party memory;
- active wild enemy display from live enemy/battle memory;
- active trainer enemy display from live enemy/battle memory;
- species, move, ability and item names for sampled stock and Gen9 IDs.

Static trainer-party data should remain caveated. CFRU and the randomizer can construct or alter actual trainer Pokemon at runtime, so live `gEnemyParty`/`gBattleMons` data is the first source of truth for battle display.

## Skeleton extension smoke

Workspace skeleton path: `03_tools/tracker-extensions/CFRUDPEExtension/`.

For local Tracker-only smoke, install the skeleton outside Git-managed Tracker sources:

1. Copy `CFRUDPEExtension.lua` into the Ironmon Tracker custom extension folder.
2. Copy the `data/` folder as `CFRUDPEExtension/data/` next to that extension file.
3. Enable `CFRUDPEExtension` in the Tracker UI.

Expected skeleton-only result:

- Tracker lists and enables the extension.
- The extension logs that the manual CFRU/DPE profile is prepared.
- No Tracker core file, NatDexExtension file, ROM, save, emulator state, build, raw log, screenshot, hash or private path is changed or committed.
- Without real `game-addresses.json` and `tracker-overrides.json`, no CFRU/DPE data correctness should be claimed.

Next local manifest smoke requires filled, local non-example files:

- `CFRUDPEExtension/data/game-addresses.json`
- `CFRUDPEExtension/data/tracker-overrides.json`

Those files should be produced from source-derived values and sanitized local validation. Do not commit private paths, ROM hashes, runtime logs, saves or emulator states.

## Manifest source-map follow-up

Use `01_docs/analysis/cfru-dpe-tracker-manifest-source-map.md` before filling local manifests.

Safe committed data starts with source-derived counts, enum mappings and layout candidates. Runtime/table target addresses for `gPlayerParty`, `gEnemyParty`, `gBattleMons`, `gBattleMoves`, `gBaseStats`, names, items, trainers, TM/HM moves and saveblock data should stay in local ignored JSON until they are available from a public symbol source or CFRU/DPE metadata table.

## Lua source-inventory follow-up

Use `01_docs/analysis/tracker-lua-source-inventory.md` before implementing the next extension or generator step.

The recommended order is source-data first, then layouts, then local ignored address overrides, then extension smoke. Local CFRU/DPE `offsets.ini` files may help seed table/name addresses for local smoke, but they are ignored/generated artifacts and should not be committed or copied wholesale. They also do not appear to solve all live party, battle RAM, SaveBlock or bag addresses by themselves.
