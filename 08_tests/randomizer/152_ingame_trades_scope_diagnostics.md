# Diagnose 152: In-Game Trades scope diagnostics

## Scope

This is a read-only CFRU/DPE Gen9-BPRE In-Game Trades candidate diagnostic. It does not write, save, build, run the Randomizer, create an output ROM, or touch code.

The diagnostic stays limited to In-Game Trade table readability and field safety. Static/Gift Pokemon, Starters, Trainer Pokemon, Wild Pokemon, Held Items outside trade fields, Field Items, Pickup Items, Shop Items and Text/Menu work remain out of scope.

## Result

Status: blocked / preflight.

A local BPRE candidate source was available and could be loaded read-only. The current UPR-FVX Gen3 In-Game Trade table model did not produce a safe active trade structure for the candidate: the expected active trade entries were readable as bytes, but the Species fields classified as null/invalid placeholders and requested species were null in every inspected entry. Fixed-length text fields were readable as fixed-size fields, but terminator classification was not stable enough for a write smoke.

No In-Game Trade feature is promoted by this diagnostic. Do not run a species-only write/reload smoke until the trade locator/table model is reconciled for CFRU/DPE Gen9-BPRE.

## Trade table finding

- Candidate source: loaded read-only; private path, file name, hash, offsets and raw bytes are intentionally not documented.
- Candidate file scan stayed local and read-only.
- The current Gen3 UPR-FVX trade-table model expects three active entries and no `TradesUnused` entries for the BPRE profile.
- The inspected active entries did not classify as valid trade records because Species fields resolved to null/invalid placeholder values.
- `TradesUnused` is classifiable from the ROM-entry model, but preserve-only behavior cannot be proven until a valid active table is located.

## Species finding

- Given Species fields were readable as fields, but not valid as loaded Species IDs under the current model.
- Requested Species fields were readable as fields, but every inspected requested species classified as null.
- This is a blocker for the Gen3 writer path because `setInGameTrades(...)` writes requested species through a dereferenced Species object.
- CFRU/DPE Gen9 SpeciesSet/internal identity safety remains unproven for In-Game Trades.

## Held-item finding

- Trade held-item fields were readable.
- All inspected trade held-item fields were empty/non-held-item values.
- No invalid or unloaded trade item values were observed in the inspected fields.
- Trade held-item write safety remains unproven until the trade table locator is fixed or confirmed.

## Text and IV finding

- Nickname fixed-length fields were readable with the expected field length.
- OT fixed-length fields were readable with the expected field length.
- Terminator/padding classification was not stable in the inspected entries, matching the broader table-locator blocker.
- IV fields were readable and no out-of-range IV values were observed.
- Nickname/OT randomization remains a later separate fixed-length text scope and must not be combined with the first species smoke.

## Metrics

| Metric | Value |
| --- | --- |
| `candidateFilesChecked` | `2` |
| `candidateLoaded` | `true` |
| `tradeScanSuccessful` | `false` |
| `tradeCount` | `3` |
| `tradesUnusedCount` | `0` |
| `givenSpeciesTotal` | `3` |
| `requestedSpeciesTotal` | `3` |
| `requestedSpeciesNullCount` | `3` |
| `invalidTradeSpecies` | `6` |
| `unloadedTradeSpecies` | `0` |
| `fallbackTradeSpecies` | `0` |
| `placeholderTradeSpecies` | `6` |
| `tradeHeldItemsTotal` | `3` |
| `tradeHeldItemsNonZero` | `0` |
| `invalidTradeItems` | `0` |
| `unloadedTradeItems` | `0` |
| `fallbackTradeItems` | `0` |
| `placeholderTradeItems` | `0` |
| `tradeNicknameFieldsReadable` | `true` |
| `tradeNicknameFieldLength` | `12` |
| `tradeOtFieldsReadable` | `true` |
| `tradeOtFieldLength` | `11` |
| `tradeTextTerminatorIssues` | `6` |
| `tradeIvFieldsReadable` | `true` |
| `tradeIvOutOfRangeCount` | `0` |
| `starterScopeChanged` | `false` |
| `staticGiftScopeChanged` | `false` |
| `trainerScopeChanged` | `false` |
| `heldItemScopeChanged` | `false` |
| `wildScopeChanged` | `false` |
| `itemScopesChanged` | `false` |
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

## Risks and blockers

- Current Gen3 BPRE trade locator/model does not identify valid active CFRU/DPE Gen9-BPRE trade records.
- Requested species nullability blocks the existing Gen3 writer path.
- Species-ID mapping for trade rows is unproven and must not be assumed from earlier Starter/Static/Trainer species work.
- Fixed-length nickname/OT text safety is not ready for randomization.
- A write/reload smoke would risk writing invalid species or corrupting fixed-length trade text if run before locator reconciliation.

## Recommendation

Do not run the Given/Requested species-only write/reload smoke yet. Next minimal step should be a narrow In-Game Trades locator/table-model blocker plan that reconciles the CFRU/DPE Gen9-BPRE trade table location and active-entry model read-only, without text randomization and without any write/save step.
