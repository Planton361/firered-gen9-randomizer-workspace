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

1. Copy `CFRUDPEExtension.lua` directly into the Ironmon Tracker extension folder, for example `Lua/extensions/CFRUDPEExtension.lua`.
2. Copy the `data/` folder next to that extension file, for example `Lua/extensions/data/`.
3. Enable `CFRUDPEExtension` in the Tracker UI.

Expected skeleton-only result:

- Tracker lists and enables the extension.
- The extension logs that the manual CFRU/DPE profile is prepared.
- No Tracker core file, NatDexExtension file, ROM, save, emulator state, build, raw log, screenshot, hash or private path is changed or committed.
- Without real `game-addresses.json` and `tracker-overrides.json`, no CFRU/DPE data correctness should be claimed.

Next local manifest smoke requires filled, local non-example files:

- `data/game-addresses.local.json`
- `data/tracker-overrides.local.json`

Those files should be produced from source-derived values and sanitized local validation. Do not commit private paths, ROM hashes, runtime logs, saves or emulator states.

## Manifest source-map follow-up

Use `01_docs/analysis/cfru-dpe-tracker-manifest-source-map.md` before filling local manifests.

Safe committed data starts with source-derived counts, enum mappings and layout candidates. Runtime/table target addresses for `gPlayerParty`, `gEnemyParty`, `gBattleMons`, `gBattleMoves`, `gBaseStats`, names, items, trainers, TM/HM moves and saveblock data should stay in local ignored JSON until they are available from a public symbol source or CFRU/DPE metadata table.

## Lua source-inventory follow-up

Use `01_docs/analysis/tracker-lua-source-inventory.md` before implementing the next extension or generator step.

The recommended order is source-data first, then layouts, then local ignored address overrides, then extension smoke. Local CFRU/DPE `offsets.ini` files may help seed table/name addresses for local smoke, but they are ignored/generated artifacts and should not be committed or copied wholesale. They also do not appear to solve all live party, battle RAM, SaveBlock or bag addresses by themselves.

## Source-data generator

Use `07_scripts/tracker/generate_cfru_dpe_source_data.py` to regenerate `03_tools/tracker-extensions/CFRUDPEExtension/data/source-data.json` from source headers.

This generated JSON is safe for committed source-data smoke because it contains only counts, ID mappings, macro-derived fallback names and warnings. It still does not make the extension live-data-capable. Real local `game-addresses.json` and `tracker-overrides.json` remain separate ignored smoke inputs until a public metadata or symbol path exists.

## Layout override follow-up

Use `01_docs/analysis/cfru-dpe-tracker-layout-overrides.md` before filling or generating `tracker-overrides.json`.

Safe layout candidates exist for `BattleMove`, `BattlePokemon`, `BaseStats`, `Trainer`, simple TrainerMon rows, bag `ItemSlot`, and bag pocket counts. These are offsets/sizes only, not ROM/RAM addresses.

Do not assume stock party reads are fixed by layout overrides alone. CFRU `struct Pokemon` differs from vanilla encrypted Gen 3 party data, while Ironmon Tracker's `Program.readNewPokemon` decodes vanilla encrypted/reordered substructs. A real party/battle smoke should validate either a CFRU-aware reader or source-backed metadata path.

Before relying on `TrackerAPI.loadTrackerOverridesFromJson`, verify locally that override JSON updates the nested fields consumed by Tracker read paths, such as `Program.Addresses.*`, `PokemonData.Addresses.*`, and `MoveData.Addresses.*`. Record only sanitized pass/fail notes.

## Manifest loader smoke

The minimal loader smoke uses committed `source-data.json` plus optional ignored local manifests:

- committed `CFRUDPEExtension/data/source-data.json` should load and report counts;
- missing `game-addresses.local.json` and `tracker-overrides.local.json` should be reported as missing, not as extension failure;
- if local `.local.json` files exist, the extension should call TrackerAPI's explicit-path JSON loaders and log each return status.

The extension resolves `data/` relative to the actual loaded `CFRUDPEExtension.lua` file first, then falls back to Tracker's `FileManager.getExtensionsFolderPath()`. This supports a Tracker install that is outside the workspace, with `CFRUDPEExtension.lua` directly in `Lua/extensions/` and manifests in `Lua/extensions/data/`.

This smoke still proves only extension load/unload, source-data availability and manifest-loader wiring. Live party, battle, trainer and bag correctness require a separate local address smoke after safe local manifests exist.

## Local address generator smoke

Use `07_scripts/tracker/generate_cfru_dpe_game_addresses_local.py` only with a local generated `offsets.ini` artifact. The script writes the ignored `03_tools/tracker-extensions/CFRUDPEExtension/data/game-addresses.local.json` by default and does not write the input path into the JSON.

Minimal local steps:

1. Run `python3 07_scripts/tracker/generate_cfru_dpe_game_addresses_local.py --offsets path/to/offsets.ini`.
2. If CFRU and DPE produced separate local symbol files, repeat `--offsets` in the same command to merge them into one local manifest.
3. Verify `game-addresses.local.json` remains unstaged and ignored.
4. Copy the generated local file into the installed Tracker extension `Lua/extensions/data/` folder only for local smoke.
5. Start Tracker and confirm the extension reports `game-addresses.local=loaded` or a clear loader status.

Expected first result: table/name symbols may load when present in `offsets.ini`, but missing `gPlayerParty`, `gEnemyParty`, `gBattleMons`, SaveBlock, or bag-pocket warnings mean live party, battle, and bag correctness is not proven yet.

## Local tracker-overrides generator smoke

Use `07_scripts/tracker/generate_cfru_dpe_tracker_overrides_local.py` to create the ignored local layout manifest:

```sh
python3 07_scripts/tracker/generate_cfru_dpe_tracker_overrides_local.py
```

Expected output is `03_tools/tracker-extensions/CFRUDPEExtension/data/tracker-overrides.local.json`, which must remain ignored and unstaged.

The generated file includes only source-backed layout candidates for recognized Tracker override sections:

- `Program`: BattlePokemon, BattleMove, BaseStats row size, and Trainer header offsets/sizes.
- `PokemonData`: BaseStats core byte offsets and ability byte size.
- `MoveData`: bit offsets/sizes used when Tracker reads power/type/accuracy/PP/category from `gBattleMoves`.

Do not treat this as a complete compatibility proof. It does not solve CFRU party `struct Pokemon` decoding, SaveBlock/bag runtime addresses, expanded TrainerMon variants, hidden ability UI behavior, or whether the Tracker override loader updates the nested `*.Addresses` tables used by read paths. Validate loader behavior locally and record only sanitized pass/fail notes.

## Live RAM anchor follow-up

Use `01_docs/analysis/cfru-dpe-tracker-live-ram-anchors.md` before treating the loader smoke as live-data capable.

The local smoke where `source-data`, `game-addresses.local`, and `tracker-overrides.local` all loaded but Player/Starter and Wild battle data were still missing is consistent with two unresolved layers:

- the local address manifest may still lack live RAM anchors consumed by stock Tracker paths, especially `pstats`/`gPlayerParty`, `estats`/`gEnemyParty`, `gBattleMons`, `gBattlersCount`, `gBattleMainFunc`, and `gBattlerPartyIndexes`;
- stock `Program.readNewPokemon` decodes vanilla encrypted Gen 3 party data, while CFRU `struct Pokemon` is a direct expanded source layout.

Next local smoke should not copy or document real addresses. It should only report sanitized presence/absence of required symbol keys and whether an extension-side CFRU/DPE reader can produce plausible active battle data. The recommended v1 smoke target is a custom `gBattleMons` active-battle reader before full party, bag, or SaveBlock support.
