# Diagnose 154: In-Game Trades table-model diagnostics

## Scope

This is a read-only source/documentation diagnostic for the In-Game Trades locator/table model in the tested CFRU/DPE Gen9-BPRE scope.

No code is changed. No build, Randomizer run, ROM access, save access, output ROM, write smoke, text randomization or external download is performed.

## Result

Status: blocked.

Valid active In-Game Trade rows were not read-only confirmed in this diagnostic. The source model is clear, but the candidate evidence from Diagnose 152 remains blocked: `tradeScanSuccessful=false`, `tradeCount=3`, `requestedSpeciesNullCount=3`, `invalidTradeSpecies=6`, and `placeholderTradeSpecies=6`.

Therefore a later Species-Write-Smoke remains blocked until a locator/table-model diagnostic confirms valid active rows or explicitly classifies the current rows as unsupported/dummy/preserve-only.

## UPR-FVX Gen3/FireRed locator

UPR-FVX localizes Gen3 In-Game Trades through the Gen3 ROM-entry metadata:

- `TradeTableOffset`
- `TradeTableSize`
- `TradesUnused`

The Gen3 handler reads these values in `Gen3RomHandler.getInGameTrades()` and writes through the same metadata in `Gen3RomHandler.setInGameTrades(...)`.

For FireRed/BPRE profiles, the metadata lives in `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`. The exact numeric locator values are intentionally not repeated here because this protocol avoids documenting private or raw locator details in the diagnostic handoff.

## Expected table and row model

`Gen3RomHandler` expects a fixed-size table:

- table count from `TradeTableSize`
- skip list from `TradesUnused`
- row length: 60 bytes
- nickname field at row start, read as a variable-length internal string and written as a fixed-length string of length 12
- given species at the species word field, read via `pokesInternal[...]`
- six IV byte fields
- OT ID word field
- held item word field, converted with `Gen3Constants.itemIDToStandard(...)` on read and `itemIDToInternal(...)` on write
- OT name field, read as a variable-length internal string and written as a fixed-length string of length 11
- requested species word field, read via `pokesInternal[...]`

The writer then emits species through `pokedexToInternal[trade.getGivenSpecies().getNumber()]` and `pokedexToInternal[trade.getRequestedSpecies().getNumber()]`.

## Why Diagnose 152 was blocked

Diagnose 152 loaded the local BPRE candidate read-only and applied the current Gen3 BPRE table model. The model produced three rows, but every inspected species field classified as null/invalid/placeholder rather than a valid loaded species.

Key blocker metrics from Diagnose 152:

| Metric | Value |
| --- | --- |
| `tradeScanSuccessful` | `false` |
| `tradeCount` | `3` |
| `requestedSpeciesNullCount` | `3` |
| `invalidTradeSpecies` | `6` |
| `placeholderTradeSpecies` | `6` |
| `tradeTextTerminatorIssues` | `6` |

This does not prove that In-Game Trades are absent. It proves only that the current vanilla-style Gen3 BPRE table model did not safely identify valid active trade rows in the tested CFRU/DPE Gen9-BPRE candidate.

## Null requested-species risk

`InGameTrade.requestedSpecies` is nullable in the shared model. The Gen3 writer is not defensive for requested species: it dereferences `trade.getRequestedSpecies().getNumber()` when writing.

That makes the Diagnose 152 result a hard blocker for any write smoke. Active null requested-species rows must be either absent, skipped/preserved by policy, or guarded by an explicit fix before writes are allowed.

## Interpretation

The current evidence supports these possibilities:

- the BPRE trade-table locator is stale for the CFRU/DPE candidate;
- the candidate uses a different row shape than vanilla Gen3 60-byte trade rows;
- the rows are dummy/disabled rows not represented by `TradesUnused`;
- In-Game Trades are disabled or script-replaced in the candidate;
- a defensive null-requested-species policy is required before any writer path.

This diagnostic does not choose a fix because no code change or ROM-level locator investigation is in scope.

## Minimum criteria before Species-Write-Smoke

A later species-only write/reload smoke is allowed only if all of the following are documented first:

- `tradeScanSuccessful=true`
- `validActiveTradeRows > 0`
- `requestedSpeciesNullCount=0` for active rows, or null-request rows are explicitly preserve/skip
- `invalidTradeSpecies=0` for active rows
- `unloadedTradeSpecies=0` for active rows
- `placeholderTradeSpecies=0` for active rows unless classified as skipped dummy rows
- `TradesUnused` or equivalent dummy-row policy is stable
- nickname and OT fields are classified but not modified
- IV and held-item fields are readable but not modified in the species-only smoke
- Starter, Static/Gift, Trainer, Wild, Held Items and Item scopes remain unchanged

## Recommendation

Keep In-Game Trades blocked for write smokes. The next useful block is a read-only locator/table-model diagnostic with explicit permission to inspect the local candidate structure at the table-model level, still without writes, saves, text randomization, builds or Randomizer runs.

If that future diagnostic cannot confirm valid active rows, the scope should move toward either a ROM-entry/locator correction plan, a dummy-row skip plan, a defensive null-requested-species plan, or an unsupported-scope decision.
