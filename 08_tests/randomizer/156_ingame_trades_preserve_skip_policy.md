# Diagnose 156: In-Game Trades preserve/skip policy

## Scope

This is a read-only documentation decision for the CFRU/DPE Gen9-BPRE In-Game Trades preserve/skip policy.

No code is changed. No ROM, save, emulator state, build, Randomizer run, Randomizer JAR, log, output ROM, external download, Species-Write-Smoke, text randomization or feature-scope work is performed.

## Decision

Diagnosis result: `blocked-pending-evidence`.

The current evidence is strong enough to forbid all In-Game Trade writes, but not strong enough to classify the scope as final `unsupported-dummy`.

`unsupported-dummy` remains plausible because the modeled rows behave like dummy/placeholder rows under the current UPR-FVX BPRE table model. However, Diagnose 152, 154 and 155 do not prove whether the rows are truly disabled/dummy data, wrong-location data, a changed CFRU/DPE row shape, or script-replaced trades. Therefore the safer documentation status is `blocked-pending-evidence`.

## Evidence summary

Diagnose 152 loaded the local BPRE candidate read-only and applied the current UPR-FVX Gen3 In-Game Trades model:

| Metric | Value |
| --- | --- |
| `tradeScanSuccessful` | `false` |
| `tradeCount` | `3` |
| `requestedSpeciesNullCount` | `3` |
| `invalidTradeSpecies` | `6` |
| `placeholderTradeSpecies` | `6` |

Diagnose 154 confirmed the source model:

- UPR-FVX Gen3 reads In-Game Trades through `TradeTableOffset`, `TradeTableSize` and `TradesUnused`.
- The Gen3 handler uses fixed 60-byte rows.
- `setInGameTrades(...)` writes both offered/given Species and requested Species through dereferenced Species objects.
- Null requested Species is therefore unsafe in the current Gen3 writer path.

Diagnose 155 confirmed the active-row candidate result:

- UPR-FVX BPRE metadata models three non-unused 60-byte rows.
- `TradesUnused=[]`, so the model itself does not skip any of the three rows.
- No valid active trade row is confirmed.
- `unsupported-dummy` is plausible but not read-only proven from the documented evidence.

## Preserve/Skip Policy

Effective policy for the tracked CFRU/DPE Gen9-BPRE scope:

- Preserve every modeled In-Game Trade row exactly as-is.
- Skip all In-Game Trade write paths.
- Do not run or prepare a Species-Write-Smoke.
- Do not randomize requested Species.
- Do not randomize offered/given Species.
- Do not randomize Trade Held Items.
- Do not randomize IVs.
- Do not randomize Nickname or OT text.
- Leave dummy/placeholder/null-request structures unchanged.
- Treat `TradesUnused=[]` as insufficient for write permission; it only means the current ROM-entry model has no index-based skip list.
- Treat null/invalid/placeholder Species rows as preserve-only until a later block proves a valid active-row model or implements a defensive skip/guard.
- Plan any future code fix separately, defensively and narrowly; this diagnosis does not authorize implementation.

## Reopen criteria

In-Game Trades may be reopened only if a later read-only or explicitly scoped implementation block documents one of these exit paths:

1. Valid active-row evidence:
   - `tradeScanSuccessful=true`
   - `validActiveTradeRows > 0`
   - active `requestedSpeciesNullCount=0`
   - active `invalidTradeSpecies=0`
   - active `placeholderTradeSpecies=0`
   - active offered/given and requested Species map to the expected CFRU/DPE SpeciesSet
   - Nickname/OT fields remain out of the first Species smoke

2. Corrected locator or row-shape evidence:
   - the current BPRE `TradeTableOffset` / `TradeTableSize` / 60-byte model is replaced by read-only evidence for the actual active trade structure
   - any replacement model avoids private path, hash, raw offset and raw byte disclosure in workspace docs
   - active Species fields validate before any write plan

3. Explicit unsupported/dummy decision:
   - the modeled rows are proven to be disabled, dummy, placeholder or script-replaced for the tracked scope
   - the documented behavior becomes preserve-only / no-op for In-Game Trades
   - no GUI-compatible In-Game Trade subfeature is promoted

4. Defensive null-requested-species plan:
   - a separate code-fix plan defines how Gen3 writes skip or guard null requested Species without mutating dummy rows
   - the plan includes reload criteria and cross-scope isolation
   - Species, text, item and IV work remain split into separate follow-up smokes

## Status matrix

| Classification | Decision | Reason |
| --- | --- | --- |
| `unsupported-dummy` | no | Plausible, but not proven without additional candidate-structure evidence. |
| `blocked-pending-evidence` | yes | Current rows fail Species validity, but the underlying cause remains unresolved. |
| Species-Write-Smoke | no | Requested Species are null in all modeled rows and Species fields classify as invalid placeholders. |
| Nickname/OT text scope | no | Text fields must not be mixed into locator, dummy-row or Species safety work. |

## Recommendation

Keep In-Game Trades closed as `blocked-pending-evidence`. Move to another Randomizer scope unless the next block is explicitly limited to read-only candidate-structure evidence or a separate defensive skip/guard plan. No In-Game Trade writes are allowed from the current evidence.
