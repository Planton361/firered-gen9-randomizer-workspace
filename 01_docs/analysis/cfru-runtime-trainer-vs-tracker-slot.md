# CFRU Runtime Trainer vs Tracker Slot

Status: source-backed analysis plus minimal Tracker-extension diagnostic hardening. No ROMs, saves, builds, raw logs, hashes, private paths, local addresses, `.local.json` files, UPR-FVX behavior, or CFRU/DPE code were changed.

## Problem

The private UPR-FVX write/reload audit is now clean:

- `warnings=none`
- `outputValidRuntimeNotLoadedCount=0`
- `outputLoadedRuntimeMismatchCount=0`

That makes the raw output-ROM trainer rows unlikely to be the remaining source of Route-22/Rival smoke confusion. The remaining split is:

1. CFRU runtime trainer construction may alter the final party or battle rows after the ROM data is read.
2. `CFRUDPEExtension` may be reading live battle context too weakly, especially party slot and trainer context.

## Source-backed CFRU findings

| Area | Source | Finding | Impact |
| --- | --- | --- | --- |
| Trainer construction entry | `02_external/CFRU-expansion/src/build_pokemon.c` `BuildTrainerPartySetup` / `CreateNPCTrainerParty` | Trainer battles build `gEnemyParty` from `gTrainerBattleOpponent_A` and, for two-opponent battles, second trainer data. | The runtime party is a constructed layer after raw trainer rows. A clean UPR-FVX reload audit does not prove `gEnemyParty`/`gBattleMons` identity without live context. |
| Custom moves | `02_external/CFRU-expansion/include/new/build_pokemon_2.h` `SET_MOVES` | CFRU copies four custom moves directly from `structure[i].moves[j]` into `party[i].moves[j]` and computes PP per slot. | If raw custom moves contained a leading `MOVE_NONE`, CFRU would preserve it. The clean UPR-FVX audit argues against raw output rows as the current cause, but this remains the source-backed runtime behavior. |
| Randomizer custom-move gate | `02_external/CFRU-expansion/src/build_pokemon.c` `CreateNPCTrainerParty` | `setCustomMoves` can be false when the Pokemon randomizer flag is active and battle-facility/temp-disable exceptions do not apply. | In that mode CFRU creates the Pokemon and lets generated/default moves stand instead of applying ROM custom moves. That can make live moves differ from raw trainer custom moves by design. |
| Difficulty/runtime effects | `02_external/CFRU-expansion/src/build_pokemon.c` `CreateNPCTrainerParty` | Level scaling, randomizer evolution, IV/EV/Friendship/PP logic, and tera/type adjustments can run after species creation depending on flags/difficulty. | Runtime `gBattleMons` can legitimately diverge from raw trainer rows in level/stats/PP/context, even when UPR-FVX wrote the trainer rows correctly. |
| BattlePokemon layout | `02_external/CFRU-expansion/include/pokemon.h` `struct BattlePokemon` | `species` is at `0x00`, `moves[4]` at `0x0C`, `pp[4]` at `0x24`, `hp` at `0x28`, `level` at `0x2A`, `maxHP` at `0x2C`, `item` at `0x2E`, `status1` at `0x4C`, `status2` at `0x50`, `otId` at `0x54`; total row size is `0x58`. | The extension's `gBattleMons` move offsets/order are source-backed and likely not the cause of leading empty move slots. |
| Battle globals | `02_external/CFRU-expansion/BPRE.ld`, `include/battle.h`, `include/new/ram_locs_battle.h` | `gBattleTypeFlags` is `u32`; `gBattleMons` is the battle row array; `gBattlerPartyIndexes` is declared as `u16[MAX_BATTLERS_COUNT]`; `gTrainerBattleOpponent_A` is `u16` at the vanilla trainer-battle work area. | The previous extension reader treated party indexes as bytes. That explains unreliable `partySlot` display and must be fixed before interpreting Route-22 slot evidence. |
| Multi/two-opponent slots | `02_external/CFRU-expansion/src/multi.c` `MultiInitPokemonOrder` | In multi/two-opponent battles, opponent-left starts at party index `0` and opponent-right at `3`; partner starts at `3`. | Slot interpretation depends on battle type and battler position. A single opponent Route-22 smoke should focus opponent-left, but double/two-opponent context needs `gBattleTypeFlags`. |

## Extension findings

`CFRUDPEExtension.lua` already used the source-backed `BattlePokemon` row size `0x58` and move offset `0x0C`. The main reader issue was `gBattlerPartyIndexes`: CFRU declares it as `u16[MAX_BATTLERS_COUNT]`, but the previous extension code read one byte at `address + battlerIndex`.

The minimal extension-side hardening in this block:

- reads `gBattlerPartyIndexes` as `u16` at `address + battlerIndex * 2`;
- displays `partySlot[...]` only for plausible slots `0..5`;
- keeps `partySlot[-]` when the key is absent, unreadable, or out of range;
- optionally reads `gBattleTypeFlags` as `u32`;
- optionally reads `gTrainerBattleOpponent_A/B` as `u16`;
- formats snapshots with `ctx[flags=... trainerA=... trainerB=...]` and opponent-left `trainer[...]`.

## Current likelihood

Tracker party-slot confusion is more likely than CFRU runtime corruption for the `partySlot` part, because the extension had a concrete width/indexing bug against a source-backed `u16[]` declaration.

Leading empty move slots are not explained by the same bug. The `BattlePokemon.moves[4]` offsets are source-backed and match the extension reader. With the UPR-FVX write/reload audit clean, remaining explanations are:

- stale local smoke artifact or old installed extension/JAR/output context;
- CFRU runtime intentionally not applying raw custom moves when `setCustomMoves` is false under randomizer flags;
- a live battle transition/window where `gBattleMons` is partially initialized or stale;
- a different CFRU runtime path mutating moves after party construction.

## Next minimal test

Run a sanitized local Tracker smoke with local ignored addresses for:

- `Addresses.gBattleMons`
- `Addresses.gBattlerPartyIndexes`
- `Addresses.gBattleTypeFlags`
- `Addresses.gTrainerBattleOpponent_A`
- optionally `Addresses.gTrainerBattleOpponent_B`

Then classify each Route-22 observation by:

- `ctx.flags`
- `trainerA` / `trainerB`
- opponent-left `partySlot`
- opponent-left Species/Level/Moves
- whether the battle is a stable loaded state, not transition/idle.

If `partySlot[1]` in weak Route 22 still shows the wrong Rival starter while UPR-FVX raw audit remains clean, investigate CFRU runtime construction. If only `partySlot[0]` differs, that is expected because the weak Route-22 nonstarter slot is randomizable.

## Non-goals

- No UPR-FVX Randomizer fix in this block.
- No CFRU/DPE code change.
- No stock Tracker-core fork or NatDexExtension change.
- No committed local addresses, manifests, ROMs, saves, builds, raw logs, screenshots, hashes, or private paths.
