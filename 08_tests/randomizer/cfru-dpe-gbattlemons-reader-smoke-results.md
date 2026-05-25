# CFRU/DPE gBattleMons Reader Smoke Results

Status: targeted local smoke pass with caveats. This file records sanitized observations only.

## Testziel

Validate that the workspace-owned `CFRUDPEExtension` can load its source data and local manifests in an installed Ironmon Tracker setup, then read plausible active-battle rows from CFRU/DPE `gBattleMons` into extension-owned state.

This smoke checks the v1 diagnostic path only:

- no Tracker-core fork;
- no NatDexExtension modification;
- no memory writes;
- no stock Tracker team-screen integration;
- no committed ROM, save, emulator state, build, screenshot, raw log, hash, private path, `offsets.ini`, local JSON, or real address data.

## Voraussetzungen

- `CFRUDPEExtension.lua` was installed in the local Ironmon Tracker extension setup.
- `data/source-data.json` was present beside the installed extension data folder.
- Local ignored `game-addresses.local.json` was present and loaded.
- Local ignored `tracker-overrides.local.json` was present and loaded.
- The smoke used sanitized pass/fail observation only; local address values and raw logs are intentionally not documented.

## Sanitized Beobachtungen

- The extension loaded in the installed Ironmon Tracker.
- `source-data.json` loaded with:
  - species `1440`
  - moves `992`
  - abilities `255`
  - items `799`
- `game-addresses.local.json` loaded.
- `tracker-overrides.local.json` loaded.
- The active-battle reader produced plausible rows in local battle smoke:
  - player-left: `Charmander`
  - opponent-left: `Rattata`
  - opponent-left: `Pidgey`
- `active-battle=no valid rows` was observed outside a valid battle state or during battle-state transitions. This is acceptable for v1 because the reader is diagnostic-only and does not yet have a full battle-state gate.
- Stock Tracker UI remained unchanged, as expected. v1 stores results in `extension.state.activeBattleMons` and does not inject into stock Tracker screens.

## Pass/Fail-Bewertung

Result: `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`.

Pass criteria met:

- Extension load path works in a real installed Tracker setup.
- Committed source-data is found and decoded.
- Local ignored manifests can be loaded without committing local values.
- `gBattleMons` reader can produce plausible active-battle species rows.
- No evidence from this sanitized smoke suggests memory writes, Tracker-core edits, or NatDexExtension edits.

Not proven:

- Full `BattlePokemon` field correctness for HP, PP, ability, held item, and all move slots across many species.
- Double battle indexing.
- Party synchronization.
- Stock Tracker UI integration.
- Player party, enemy party, bag, SaveBlock, trainer lookup, static trainer-party, or item display correctness.
- Behavior across battle start/end frames beyond the accepted `no valid rows` transition status.

## Bekannte Grenzen

- `active-battle=no valid rows` can appear during non-battle or transition states.
- v1 reads only player-left and opponent-left rows.
- v1 does not use `gBattlerPartyIndexes`, `gBattlerPositions`, battle side helpers, or full battle-state detection.
- v1 does not patch `Program.readNewPokemon` or `TrackerAPI.getActiveBattlePokemon`.
- Real local manifest values remain private/ignored and are not public source of truth.

## Nächster Schritt

Keep the current reader as a diagnostic baseline, then choose one small follow-up:

- add a safer battle-state gate using sanitized local symbol presence, if available;
- expose `extension.state.activeBattleMons` through an extension-owned debug panel/status view;
- broaden sanitized smoke to verify HP, PP, move names, ability, and held item in sampled wild and trainer battles;
- only after that, design a stock-UI integration path without modifying Tracker core.
