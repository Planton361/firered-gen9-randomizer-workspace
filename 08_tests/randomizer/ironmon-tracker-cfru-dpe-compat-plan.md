# Ironmon Tracker CFRU/DPE Local Compatibility Smoke Plan

Date: 2026-05-25
Branch: `analysis/ironmon-tracker-cfru-dpe-compat`
Scope: local plan only. Do not commit ROMs, output ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, secrets, tokens, or `.env` data.

## Goal

Determine how far the current Ironmon Tracker and NatDexExtension can read a local CFRU/DPE/Gen9 FireRed build, and identify the smallest extension/address-profile work needed for useful Tracker compatibility.

## Preconditions

- Use a local ignored ROM/output ROM only.
- Use a local ignored Tracker install or release folder; do not commit it.
- Prefer BizHawk for first smoke because the Tracker README documents full graphical support there. mGBA can be a secondary text-window smoke.
- Keep all notes sanitized: pass/fail summaries only, no full logs, screenshots, file paths, ROM hashes, or private data.

## Smoke Matrix

| Case | Setup | Expected observation | Pass/fail signal |
| --- | --- | --- | --- |
| Standard Tracker only | Load local CFRU/DPE/Gen9 ROM in BizHawk, then load Ironmon Tracker Lua without NatDexExtension. | Tracker may identify FireRed by header, but vanilla addresses/data are likely wrong or incomplete. | PASS only if current player Pokemon, moves, stats, and enemy data are plausible. FAIL if species/moves/items show as unknown, wrong, or unstable. |
| Standard Tracker + NatDexExtension | Enable NatDexExtension with the same local ROM. | Extension may not detect the ROM because it expects CyanSMP64 NatDex count/address values. | PASS only if extension activates and improves species/move/resource display. Expected result is likely FAIL/BLOCKED for drop-in use. |
| Battle-only observation | Enter a simple wild battle and a trainer battle. | Battle memory may be closer to Tracker expectations than party memory. | Record whether active enemy species, enemy moves used, HP/status/types and current player mon look plausible. |
| Smart Trainer AI flag off/on | On Normal Difficulty, compare without and with local `FLAG_SMART_TRAINER_AI` smoke activation. | Tracker reading should not change except for observed enemy move choices during battle. | PASS if Tracker data display is stable across flag off/on; AI behavior differences are separate from compatibility. |
| Custom-extension future baseline | After a future CFRU/DPE extension exists, repeat with custom addresses and data resources. | Species, moves, abilities, items, party and battle data should become plausible. | PASS only with source-backed address/data mapping and sanitized local observations. |

## Data To Check In Game

| Data | Local check | Notes |
| --- | --- | --- |
| Player lead species | Compare Tracker species/name/icon with in-game summary. | Important because CFRU direct party struct likely differs from Tracker vanilla encrypted read logic. |
| Player moves and PP | Compare four moves and PP with in-game summary. | Move IDs beyond stock Tracker need Gen9 move data. |
| Player stats | Compare HP/Attack/Defense/Speed/Sp. Atk/Sp. Def with in-game summary. | Stat offsets may still be plausible even if species/moves fail. |
| Ability | Compare ability text with in-game summary. | Hidden ability and Gen9 ability mapping need attention. |
| Held item | Compare held item ID/name/category with in-game summary. | Expanded CFRU/DPE item IDs likely require item data extension. |
| Wild enemy | Enter one wild battle and compare active enemy species, HP/status/types and used moves. | Avoid documenting encounter table dumps or raw addresses. |
| Trainer enemy | Enter one trainer battle and compare active enemy species, move use, and trainer metadata if visible. | Trainer table address and custom party layout are likely risk areas. |
| Level-up move display | If Tracker shows learned moves, compare a small sample against in-game/source expectations. | CFRU `struct LevelUpMove` is 3 bytes, while Tracker assumes vanilla packed 2 bytes. |

## Recommended Smallest Next Step

Run a local BizHawk smoke with standard Ironmon Tracker only, then with NatDexExtension enabled, and record sanitized pass/fail notes. Do not build a custom extension before confirming which parts fail in practice.

If standard/NatDex smoke fails as expected, the next implementation step should be a documentation-only design for a CFRU/DPE Tracker extension that first targets:

1. address profile / table pointers,
2. CFRU party Pokemon reader,
3. species/move/ability/item text data,
4. battle data verification,
5. trainer custom party parser.

## Safety Rules

- Do not commit Tracker release folders, generated files, ROMs, saves, states, screenshots, builds, logs, hashes, private paths, or tool binaries.
- Do not apply BPS/IPS/UPS patches in this repo.
- Do not clone new external repos without explicit approval.
- Keep `FLAG_SMART_TRAINER_AI` testing separate from Tracker compatibility: it is an AI behavior switch, not a memory-layout change.
