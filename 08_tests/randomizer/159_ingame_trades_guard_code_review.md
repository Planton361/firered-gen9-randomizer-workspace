# Diagnose 159: In-Game Trades guard code review

## Scope

This is a read-only code review of the merged UPR-FVX In-Game Trades Null-/Invalid-Species guard against the Preserve/Skip policy from Diagnose 156.

No code is changed. No build, Randomizer run, ROM smoke, save, emulator state, output ROM, log, Randomizer JAR, tool binary, private path, hash, secret, token or `.env` file is touched.

## Preconditions

- Workspace PR #203 / Follow-up 158B is merged into `main`.
- Workspace branch: `test/upr-fvx-cfru-dpe-ingame-trades-guard-code-review`.
- UPR-FVX submodule pin: `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- UPR-FVX PR #39 is merged on base branch `compat/firered-gen9-cfru-dpe`.

## Reviewed files

- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TradeRandomizer.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

## Review result

Classification: `review-pass-with-risks`.

The guard satisfies the narrow preserve/skip intent for unsafe modeled rows:

- rows with `requestedSpecies == null` are skipped before mutation
- rows with null/placeholder/unsafe offered/given or requested Species are skipped before mutation
- Gen3 writer skips unsafe rows before any byte write for the row
- text, Nickname/OT, IV and held-item paths are not expanded by the guard
- Species-Write-Smoke remains blocked

The result is not `review-pass` because the review is still static only and leaves non-ROM harness coverage, visible skip reporting, valid-active-row proof and reader/mapping edge cases open.

## Pre-mutation guard

`TradeRandomizer.randomizeIngameTrades()` loads the trade list and then checks each `InGameTrade` before the first mutation:

- `trade == null` increments `skippedUnsafeSpeciesTrades` and continues
- `trade.getRequestedSpecies() == null` increments `skippedNullRequestedSpeciesTrades` and continues
- unsafe given/requested Species fail `isSafeTradeSpecies(...)` and continue

The first mutating statement for the row is `trade.setGivenSpecies(given)`, and it occurs only after these checks. Requested Species, nickname, OT, IV and held-item mutations also occur after the same guard.

The Species predicate rejects:

- null Species
- Species number `<= 0`
- null Species names
- names equal to `Bad Egg`
- names equal to `?`
- names containing `unused`
- Species not present in `romHandler.getSpeciesSetInclFormes()`

The method calls `romHandler.setInGameTrades(trades)` only if at least one eligible row was actually changed. If every modeled row is skipped, `changesMade=false` and no writer call is made.

## Writer preserve/skip guard

`Gen3RomHandler.setInGameTrades(...)` keeps the existing `TradeTableOffset`, `TradeTableSize`, `TradesUnused` and 60-byte row iteration model.

For non-unused rows, the writer now retrieves the modeled `InGameTrade` and immediately checks `canWriteInGameTrade(trade)`. If the check fails, it continues before:

- nickname fixed-length write
- offered/given Species write
- IV writes
- OT ID write
- held item write
- OT name fixed-length write
- requested Species write

That ordering preserves the existing row bytes for unsafe rows because no field write is reached.

The writer Species predicate rejects:

- null Species
- Species number `<= 0`
- Species number outside `pokedexToInternal`
- null Species names
- placeholder names (`Bad Egg`, `?`, `unused`)
- mappings whose internal Species value is `<= 0`
- mappings outside `pokesInternal`
- mappings where `pokesInternal[internalSpecies] == null`

This is conservative for CFRU/DPE Gen9-BPRE. Rows that cannot be proven safely writable through the current writer mapping are preserved rather than rewritten.

## Preserve/Skip policy comparison

Diagnosis 156 required all modeled null/invalid/placeholder rows to remain preserve-only until valid active rows or a defensive skip/guard exists.

The merged guard meets that policy for unsafe rows:

- unsafe rows are not mutated in `TradeRandomizer`
- unsafe rows are not written in `Gen3RomHandler`
- dummy/placeholder/null-request rows can remain byte-stable through skip/preserve behavior
- `TradesUnused=[]` remains only an index-skip input, not write permission

The guard does not reopen In-Game Trades. It reduces unsafe-write risk but does not prove that valid active Trade rows exist.

## Text, Nickname/OT, IV and held-item paths

No new text, Nickname/OT, IV or Trade Held Item randomization is introduced.

Existing optional mutation blocks remain present for eligible rows:

- `randomNickname` can set `trade.setNickname(...)`
- the fallback nickname sanity branch can set the nickname to the new given Species name
- `randomOT` can set OT name and OT ID
- `randomStats` can rewrite IVs
- `randomItem` can rewrite the held item

For unsafe rows, all of these blocks are bypassed by the pre-mutation guard. For any future valid active rows, these paths remain out of scope for compatibility promotion and must not be enabled by a Species-only diagnostic.

## Remaining risks

- Static review only: no non-ROM harness proves the skip counters, `changesMade=false`, or writer skip behavior with synthetic trades.
- Skip counters are available through getters but are not shown in the normal user log/status path reviewed here.
- `getInGameTrades()` still indexes `pokesInternal[readWord(...)]` directly; an out-of-range raw Species ID would still be a reader risk outside the writer guard.
- The writer guard uses current `pokedexToInternal` mapping and is intentionally conservative; extended CFRU/DPE Species rows may be preserved instead of written until a separate active-row and mapping proof exists.
- Existing optional Nickname/OT, IV and held-item blocks remain reachable for eligible rows if those settings are enabled, so later diagnostics must keep them disabled unless separately scoped.
- No valid active-row evidence exists; `blocked-pending-evidence` remains the correct coverage state.

## Later non-ROM harness recommendation

A later harness is useful and can be kept small without ROM access:

- instantiate or mock a `TradeRandomizer` with synthetic unsafe `InGameTrade` rows
- verify `requestedSpecies == null` rows increment skip counters and do not call `setInGameTrades(...)`
- verify invalid/placeholder Species rows increment unsafe skip counters
- verify an all-skipped run leaves `changesMade=false`
- unit-test a small Gen3 writer seam only if it can be done without ROM bytes or broad refactor

Do not run a ROM Species-Write-Smoke from this review. A harness should remain non-ROM and should not touch text, Nickname/OT, IV or held-item behavior beyond proving unsafe rows bypass those paths.

## Status

In-Game Trades remain `blocked-pending-evidence`.

No Given Species, Requested Species, Trade Held Item, IV, Nickname/OT or text subfeature is promoted. Species-Write-Smoke remains blocked until valid active rows are separately proven and explicitly authorized.
