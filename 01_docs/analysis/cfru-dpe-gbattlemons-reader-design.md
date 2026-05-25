# CFRU/DPE gBattleMons Reader Design

Status: design-only analysis. No Tracker core fork, no code changes, no ROMs, no saves, no emulator states, no builds, no raw logs, no private paths, and no real local addresses.

## Executive summary

A minimal CFRU/DPE active-battle reader should be implemented as an extension-owned read path over `gBattleMons`, not as a first attempt to make stock `TrackerAPI.getActiveBattlePokemon` work.

Source-backed reason: stock `TrackerAPI.getActiveBattlePokemon` returns objects from `Tracker.getPokemon`, which reads `Program.GameData.PlayerTeam` / `EnemyTeam`. Those teams are populated by `Program.updatePokemonTeams` through `Program.readNewPokemon`, and that reader decodes vanilla encrypted Gen III party data. CFRU `struct Pokemon` is a different expanded direct layout, so the party path remains a separate problem.

`gBattleMons` is a better v1 target because CFRU declares `struct BattlePokemon` with source-commented offsets for active battle fields. A read-only extension path can read active battlers directly from `GameSettings.gBattleMons`, use source-derived `BattlePokemon` size `0x58`, map IDs through committed `source-data.json`, and expose a small extension status/diagnostic surface without writing emulator memory or modifying Tracker core files.

## Source-backed Tracker constraints

| Tracker source | Behavior | Design implication |
| --- | --- | --- |
| `TrackerAPI.getPlayerPokemon` / `getEnemyPokemon` | Wrap `Tracker.getPokemon`, optionally using `Battle.Combatants` when `Battle.inActiveBattle()` is true. | These APIs still require stock team tables to be populated correctly. |
| `TrackerAPI.getActiveBattlePokemon` | Returns empty unless `Battle.inActiveBattle()` is true, then returns player/enemy party objects through `TrackerAPI.getPlayerPokemon` / `getEnemyPokemon`. | It is not a direct `gBattleMons` API. A CFRU extension should not depend on it for the first active-battle smoke. |
| `Tracker.getPokemon` | Reads from `Program.GameData.PlayerTeam` or `Program.GameData.EnemyTeam`. | Direct active battle data cannot appear here unless the extension populates/overrides those team tables. |
| `Program.updatePokemonTeams` | Iterates six slots from `GameSettings.pstats` / `estats`, then calls `Program.readNewPokemon`. | Requires `gPlayerParty` / `gEnemyParty` and a CFRU-aware party reader before full integration. |
| `Program.readNewPokemon` | XOR-decodes vanilla encrypted/reordered Pokemon substructures. | Not suitable for CFRU `struct Pokemon` without a separate port/replacement. |
| `Program.getPokemonTypes` | Reads types from `GameSettings.gBattleMons` using `sizeofBattlePokemon`, `offsetBattlePokemonTypes`, and doubles partner offset. | Confirms Tracker already has a direct battle-mon read concept, but only for dynamic types. |
| `Battle.updateBattleStatus` | Requires `gBattlersCount`, first species at `gBattleMons`, `gBattleOutcome`, `gBattleMainFunc`, and a valid opposing Pokemon from stock enemy team. | A standalone extension reader should not require stock `Battle.inActiveBattle()` for initial smoke; it can use its own lighter validity checks. |
| `Battle.updateViewSlots` | Reads `gBattlerPartyIndexes` to map battlers back to party slots. | Useful for labels/party-slot mapping, but not required to read `gBattleMons` rows themselves. |
| `CustomCode.afterProgramDataUpdate` / `afterBattleDataUpdate` | Extension hooks run after periodic Tracker memory updates. | Safe place for a read-only smoke reader and status refresh. Avoid frame-by-frame hooks for v1. |

## CFRU BattlePokemon layout

CFRU declares `struct BattlePokemon` in `02_external/CFRU-expansion/include/pokemon.h`. The active battle rows are exposed as `gBattleMons[MAX_BATTLERS_COUNT]`, with `MAX_BATTLERS_COUNT` defined as `4`.

| Field | Offset | Size | v1 use |
| --- | ---: | ---: | --- |
| `species` | `0x00` | `u16` | Required; primary validity and display ID. |
| `attack` / `defense` / `speed` / `spAttack` / `spDefense` | `0x02..0x0A` | `u16` each | Optional v1; useful later for stats. |
| `moves[4]` | `0x0C` | four `u16` | Required; active move display. |
| IV bitfields / `isEgg` / `altAbility` | `0x14..0x17` | bitfields | Caveated; do not decode in v1 unless validated. |
| `type3` | `0x18` | `u8` | Optional/caveated; useful for Roost/extra type effects later. |
| `statStages` | `0x19` | seven `s8` | Optional v1; source-backed for later battle details. |
| `ability` | `0x20` | `u8` | Required/caveated; maps directly to ability ID, but hidden ability provenance is not derived from this alone. |
| `type1` / `type2` | `0x21` / `0x22` | `u8` | Required for active type display. |
| `pp[4]` | `0x24` | four `u8` | Required for move PP display. |
| `hp` | `0x28` | `u16` | Required. |
| `level` | `0x2A` | `u8` | Required. |
| `friendship` | `0x2B` | `u8` | Optional/caveated. |
| `maxHP` | `0x2C` | `u16` | Required. |
| `item` | `0x2E` | `u16` | Useful v1; item names are still source-data/item-policy caveated. |
| `nickname` | `0x30` | `POKEMON_NAME_LENGTH + 1` | Optional; decoding game text is separate. |
| `ppBonuses` | `0x3B` | `u8` | Optional. |
| `experience` | `0x44` | `u32` | Optional. |
| `personality` | `0x48` | `u32` | Useful for identity/shiny later. |
| `status1` / `status2` | `0x4C` / `0x50` | `u32` each | Optional v1; useful later for status display. |
| `otId` | `0x54` | `u32` | Optional. |

Natural row size from the final `u32 otId` field is `0x58`.

## Required anchors

| Anchor | Source concept | v1 requirement |
| --- | --- | --- |
| `gBattleMons` | Base address of `struct BattlePokemon gBattleMons[MAX_BATTLERS_COUNT]`. | Required. Without it, no active battle reader exists. |
| `gBattlersCount` | Current battler count. | Strongly recommended for row count and validity. Without it, v1 can attempt rows `0..3` and filter by species/hp, but that is weaker. |
| `gBattleTypeFlags` | Battle type flags. | Optional for first read; useful to label trainer/wild/double/raid cases later. |
| `gBattleOutcome` | Battle result state. | Optional for first read; useful to suppress stale rows after battle. |
| `gBattlerPartyIndexes` | Battler to party slot mapping. | Optional for v1 display; required if data will later sync into party slots. |
| `gBattleMainFunc` | Tracker stock battle-ready timing. | Not required for extension-owned diagnostic display; required only if trying to align with stock `Battle.inActiveBattle()`. |

If local `offsets.ini` does not expose `gBattleMons`, the next implementation should stop and require another local symbol source or a public CFRU/DPE metadata table. Real address values must stay in ignored local manifests and out of committed docs.

## Recommended reader strategy

Implement an extension-owned active-battle reader with three layers:

1. **Manifest validation:** after loading local manifests, check whether `GameSettings.gBattleMons` exists and whether source-data counts are loaded. Also check `gBattlersCount` if present.
2. **Direct row read:** for each battler index, compute `gBattleMons + index * 0x58`, read source-backed fields, and reject invalid rows where species is zero, species exceeds source-data species count, max HP is zero, or level is outside a sane byte range.
3. **Extension-owned output:** store the result in `extension.state.activeBattleMons` and print/log a compact sanitized status such as row count and species/move IDs. Do not write emulator memory and do not mutate Tracker core data in v1.

The initial index interpretation can follow the CFRU/Gen III position convention documented in `include/constants/battle.h`:

- `0`: player left
- `1`: opponent left
- `2`: player right
- `3`: opponent right

For single battles, v1 only needs indices `0` and `1`. Doubles can be read opportunistically when `gBattlersCount == 4`, but should remain caveated until local smoke validates partner order.

## Tracker integration without core fork

`TrackerAPI` is not enough for this v1 because its active-battle API still returns stock party objects. The extension should initially expose its own data surface:

- `extension.state.activeBattleMons`
- a helper such as `extension.getActiveBattleMons()` in the extension table
- a compact console/status message during `afterProgramDataUpdate` or `afterBattleDataUpdate`

Avoid wrapping or replacing `Program.readNewPokemon`, `Tracker.getPokemon`, `TrackerAPI.getActiveBattlePokemon`, or stock screens in this block. Those are later integration steps with higher blast radius.

If a visible UI is needed after the diagnostic smoke, prefer an extension-owned lightweight status panel or log/status text first. Feeding data into stock `Program.GameData.PlayerTeam` / `EnemyTeam` should wait until a CFRU-aware `struct Pokemon` party reader exists, because stock Tracker screens assume `Program.DefaultPokemon` fields and Battle/Tracker bookkeeping.

## v1 scope

Minimum useful v1 fields:

| Display goal | Fields |
| --- | --- |
| Player active summary | index `0`, species ID/name, level, HP/max HP, item ID/name if available. |
| Player active moves | index `0`, four move IDs/names, current PP. |
| Enemy active summary | index `1`, species ID/name, level, HP/max HP, ability ID/name, item ID/name if available. |
| Enemy active moves | index `1`, four move IDs/names, current PP. |
| Doubles smoke | indices `2` and `3` only when `gBattlersCount == 4`; caveated until validated. |

Keep these out of v1:

- full party display through `gPlayerParty` / `gEnemyParty`;
- SaveBlock and bag data;
- static trainer-party truth;
- hidden ability provenance;
- Tera/Gigantamax display;
- transformed/illusion handling;
- status icon parity with stock Tracker;
- stock screen replacement.

## Smoke plan

The next implementation smoke should be local-only and sanitized:

1. Extension loads committed `source-data.json`.
2. Local `game-addresses.local.json` is present and contains `gBattleMons`; optionally `gBattlersCount`.
3. Enter a known battle locally.
4. Extension reports player-left and opponent-left active rows with plausible species, level, HP, and move IDs.
5. Confirm no emulator memory writes and no Tracker-core file changes.
6. Record only pass/fail and high-level behavior. Do not commit ROMs, saves, emulator states, raw logs, screenshots, hashes, private paths, `offsets.ini`, or real local addresses.

## Risks and assumptions

- `gBattleMons` can contain stale rows outside battle; v1 needs at least species/maxHP/level validity checks, and `gBattleOutcome` or `gBattlersCount` improves reliability.
- `gBattlersCount` is strongly recommended. Without it, reading four rows is a diagnostic fallback, not a robust battle detector.
- Ability and item names depend on source-data/item mapping quality; current item count conflict remains caveated.
- Active battle rows do not replace full party truth. They are a live in-battle snapshot and may reflect transformations, temporary type changes, held item removal, status changes, and runtime move/PP changes.
- Injecting results into stock Tracker team tables too early could confuse route tracking, damage tracking, ability tracking, and screens that assume vanilla `Program.DefaultPokemon` semantics.

## Recommendation

For the next implementation branch, build a read-only extension diagnostic reader over `gBattleMons` and expose extension-owned active battle state. Treat it as the first live-data smoke, not as full Tracker compatibility. Only after that passes should the project decide whether to integrate with stock Tracker screens or keep a dedicated CFRU/DPE extension panel.
