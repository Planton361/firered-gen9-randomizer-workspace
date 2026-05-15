# Diagnose 155: In-Game Trades active-row candidates

## Scope

This is a read-only In-Game Trades active-row candidate diagnosis for the tested CFRU/DPE Gen9-BPRE scope.

Only local source and documentation inspection was used. No ROM, save, emulator state, build, Randomizer JAR, log, output ROM, external download, write smoke, Species write, text randomization, code change or private artifact was accessed or prepared.

## Result

Classification: blocked.

Valid active In-Game Trade rows are not read-only confirmed. The current UPR-FVX BPRE ROM-entry model exposes a 60-byte Gen3 trade table with `TradeTableSize=3` and `TradesUnused=[]`, so all three modeled rows are treated as active by the handler. However, the only available candidate evidence from Diagnose 152 shows those same three rows failing active-row validation:

| Metric | Value |
| --- | --- |
| `tradeScanSuccessful` | `false` |
| `tradeCount` | `3` |
| `tradesUnusedCount` | `0` |
| `requestedSpeciesTotal` | `3` |
| `requestedSpeciesNullCount` | `3` |
| `invalidTradeSpecies` | `6` |
| `placeholderTradeSpecies` | `6` |
| `tradeTextTerminatorIssues` | `6` |

This blocks a Species-Write-Smoke. It also does not yet prove `unsupported-dummy`, because read-only source/documentation inspection cannot distinguish wrong locator, changed CFRU/DPE row shape, disabled/dummy rows, or script-replaced trades without additional explicitly scoped candidate structure evidence.

## UPR-FVX row model

UPR-FVX Gen3 In-Game Trades are located from ROM-entry metadata:

- `TradeTableOffset`
- `TradeTableSize`
- `TradesUnused`

For the BPRE profile, the model provides `TradeTableSize=3` and `TradesUnused=[]`. The exact offset value is not repeated in this protocol to keep the handoff free of raw locator details; it remains available in the local UPR-FVX `gen3_offsets.ini` source.

`Gen3RomHandler.getInGameTrades()` and `setInGameTrades(...)` use fixed 60-byte rows. The relevant Species and skip fields are:

| Field | Model |
| --- | --- |
| Row size | `60` bytes |
| Active row selection | all rows from `0..TradeTableSize-1` except indexes listed in `TradesUnused` |
| Offered/Given Species | word field read through `pokesInternal[...]` |
| Requested Species | word field read through `pokesInternal[...]` |
| Nickname | fixed-length write field of `12` bytes |
| OT name | fixed-length write field of `11` bytes |
| Held item | word field converted through Gen3 item ID mapping |

The writer dereferences both Species objects. A null `requestedSpecies` is therefore not safe in the current Gen3 writer path even though the shared `InGameTrade` model allows null requested species.

## Active-row validation criteria

A row can be promoted to `candidate-confirmed` only if all of these are true for at least one non-unused row:

- `requestedSpecies` is not null.
- `offeredSpecies` / `givenSpecies` is valid in the expected CFRU/DPE SpeciesSet.
- `requestedSpecies` is valid in the expected CFRU/DPE SpeciesSet.
- No Species field classifies as invalid, unloaded, fallback or placeholder/dummy.
- The row index is not listed in `TradesUnused`.
- No additional content-based dummy/disabled-row marker is present.
- The first write plan would not require Nickname/OT randomization or other fixed-length text changes.

The current three modeled active rows fail these criteria because requested species are null and all six Species fields were previously classified as invalid placeholders.

## Classification decision

| Outcome | Decision | Reason |
| --- | --- | --- |
| `candidate-confirmed` | no | No valid active row satisfies non-null requested Species plus valid offered/requested Species. |
| `blocked` | yes | The source model is understood, but active-row candidate validity is not proven. |
| `unsupported-dummy` | no | Dummy/unsupported is plausible, but not read-only proven from source/docs plus Diagnose 152 metrics alone. |
| `unknown` | no | The blocker is specific: the modeled active rows exist structurally but fail Species validity. |

## Implications

- Do not prepare or run an In-Game Trades Species-Write-Smoke.
- Do not randomize Nickname/OT text, IVs or Trade Held Items.
- Do not infer support from `TradeTableSize=3` alone; `TradesUnused=[]` only says the UPR-FVX model does not skip rows by index.
- A future unblock requires one of: corrected locator evidence, confirmed active non-dummy row evidence, explicit dummy-row skip policy, defensive null-requested-species handling, or an explicit unsupported-scope decision.

## Recommendation

Keep In-Game Trades blocked. The next useful step is a read-only decision block that either obtains explicit candidate-structure evidence for active trade rows or records In-Game Trades as unsupported/dummy for the tracked CFRU/DPE Gen9-BPRE scope. No Species write or text-scope work should start before that decision.
