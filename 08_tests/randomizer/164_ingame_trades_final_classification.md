# Diagnose 164: In-Game Trades final classification

## Scope

This is a documentation-only decision for the tested CFRU/DPE Gen9-BPRE In-Game Trades scope.

No code is changed. No build, Randomizer run, ROM-Smoke, Species-Write-Smoke, ROM file, save, emulator state, output ROM, log, Randomizer JAR, tool binary, private path, hash, secret, token or `.env` file is touched.

## Final classification

Classification: `guarded/preserve-only, not supported`.

In-Game Trades are closed for the current tested scope as a preserve-only guarded path. UPR-FVX now defensively avoids mutating or writing unsafe modeled trade rows, but the feature is not supported for randomization because no valid active trade row has been confirmed and no ROM-facing Species write evidence exists.

## Evidence basis

Diagnose 152 found the current modeled trade rows blocked before any write:

| Metric | Value |
| --- | --- |
| `tradeScanSuccessful` | `false` |
| `tradeCount` | `3` |
| `requestedSpeciesNullCount` | `3` |
| `invalidTradeSpecies` | `6` |
| `placeholderTradeSpecies` | `6` |

Diagnoses 154 and 155 confirmed that UPR-FVX models the BPRE In-Game Trades as three non-unused 60-byte Gen3 rows, but did not confirm any valid active row. Diagnose 156 established the Preserve/Skip policy. Diagnoses 158B, 161B and 163B then documented the merged guard and non-ROM test evidence.

## Why not P1-supported

This scope is not `P1-supported` because there is no save/log/output/reload or equivalent ROM-facing compatibility evidence for In-Game Trade randomization.

No ROM-Smoke, Species-Write-Smoke, text/Nickname/OT, IV or Trade Held Item smoke has been run or authorized. The current evidence proves defensive skip/preserve behavior for unsafe rows, not functional randomization of active trades.

## Why not candidate-confirmed

This scope is not `candidate-confirmed` because no modeled row satisfies the active-row criteria:

- requested Species must be non-null
- given/offered and requested Species must map to valid loaded Species in the expected SpeciesSet
- Species fields must not be invalid, unloaded, fallback or placeholder
- the row must not be unused or content-dummy
- the first write plan must not require text/Nickname/OT randomization

The available candidate metrics still have `requestedSpeciesNullCount=3`, `invalidTradeSpecies=6` and `placeholderTradeSpecies=6`.

## Why not hard unsupported-dummy

This scope is also not classified as hard `unsupported-dummy`.

Dummy/unsupported remains plausible because the modeled rows behave like placeholder rows. However, the documented evidence does not prove whether the cause is truly disabled dummy data, script-replaced trades, a stale locator, or a changed CFRU/DPE row shape. Without that proof, the correct final classification is not a hard unsupported/dummy assertion.

## Why guarded/preserve-only fits

`guarded/preserve-only, not supported` is the narrowest accurate closure:

- unsafe rows are guarded before mutation
- unsafe Gen3 rows are guarded before byte writes
- skipped rows are preserved rather than rewritten
- the GUI feature is not promoted as compatible
- future work has explicit reopen criteria instead of implicit write permission

This classification closes the current In-Game Trades lane without pretending that the feature works and without overclaiming that the candidate definitively uses unsupported dummy data.

## What was achieved

Implemented and documented in the pinned UPR-FVX submodule:

- Mutation guard in `TradeRandomizer`: rows with null requested Species or unsafe/placeholder Species skip before mutation.
- Writer preserve guard in `Gen3RomHandler`: unsafe rows skip before Gen3 byte writes.
- Non-ROM `TradeRandomizerTest`: covers null-request and placeholder/unsafe Species skips, all-skipped no writer call, `isChangesMade=false` and skip status.
- ROM-free `Gen3InGameTradeWriterTest`: covers writer preserve decisions with synthetic `InGameTrade` rows and synthetic bytes.

## Reopen criteria

In-Game Trades may be reopened only with a separate explicitly scoped block that documents at least one of these:

1. Valid active trade rows are confirmed read-only:
   - `tradeScanSuccessful=true`
   - `validActiveTradeRows > 0`
   - active requested Species are non-null
   - active Species fields are valid and non-placeholder

2. Corrected locator or row-shape evidence:
   - the active CFRU/DPE trade structure is documented without private paths, hashes, raw offsets or raw bytes
   - the corrected model validates active Species fields before any write plan

3. Explicit unsupported/dummy proof:
   - the modeled rows are proven disabled, dummy, placeholder or script-replaced for the tracked scope
   - no GUI-compatible In-Game Trade subfeature is promoted

4. Separately authorized ROM-facing smoke scope:
   - explicitly allows ROM-Smoke or Species-Write-Smoke
   - keeps text/Nickname/OT, IV and Trade Held Item writes separate unless specifically authorized
   - includes cross-scope isolation and preserve metrics

## Final status

In-Game Trades are closed for the tested CFRU/DPE Gen9-BPRE scope as `guarded/preserve-only, not supported`.

No Species-Write-Smoke, ROM-Smoke, Randomizer run, text/Nickname/OT, IV or Trade Held Item randomization is authorized by this decision.

