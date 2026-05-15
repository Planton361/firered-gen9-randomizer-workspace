# Diagnose 157: In-Game Trades null-request guard plan

## Scope

This is a read-only plan for a later defensive null-requested-species skip/guard in the CFRU/DPE Gen9-BPRE In-Game Trades path.

No code is changed. No ROM, save, emulator state, build, Randomizer run, Randomizer JAR, log, output ROM, external download, Species-Write-Smoke, text randomization or feature-scope work is performed.

## Current status

Plan result: defensive guard plan documented; In-Game Trades remain `blocked-pending-evidence`.

The plan does not reopen In-Game Trades and does not authorize a Species-Write-Smoke. It only defines the minimum shape a later code-fix branch would need if In-Game Trades are kept as a guarded preserve/skip scope rather than fully unsupported.

## Evidence basis

Diagnose 152:

- `tradeScanSuccessful=false`
- `tradeCount=3`
- `requestedSpeciesNullCount=3`
- `invalidTradeSpecies=6`
- `placeholderTradeSpecies=6`
- fixed-length text fields were readable but not safe for randomization

Diagnose 154:

- Gen3 In-Game Trades are read from `TradeTableOffset`, `TradeTableSize` and `TradesUnused`.
- The Gen3 table model uses fixed 60-byte rows.
- `setInGameTrades(...)` currently dereferences both offered/given Species and requested Species when writing.

Diagnose 155:

- UPR-FVX BPRE metadata models three non-unused 60-byte rows.
- No valid active trade row is confirmed.
- `unsupported-dummy` is plausible but not proven.

Diagnose 156:

- Current documented status is `blocked-pending-evidence`.
- Preserve/Skip policy writes no modeled trade rows.
- Dummy/placeholder/null-request structures remain unchanged.

## Guard intent

A later defensive fix should make unsafe rows no-op / preserve-only rows:

- Trade rows with `requestedSpecies == null` must not be written.
- Trade rows with null offered/given Species must not be written.
- Trade rows with invalid, unloaded, fallback or placeholder Species must not be written.
- Skipped rows must preserve existing row bytes; no fixed-length text, IV, held-item or Species fields should be rewritten.
- Text, Nickname, OT, IV and Trade Held Item randomization must stay disabled for the first guard fix.
- Status/log output must make skipped/preserved rows explicit enough that a run cannot be mistaken for full In-Game Trades compatibility.

## Minimal future code-fix candidates

Expected affected files for a later implementation branch:

1. `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TradeRandomizer.java`
   - Add a pre-mutation eligibility check for each `InGameTrade`.
   - Skip rows before changing given Species, requested Species, nickname, OT, IVs or held item.
   - Count skipped/preserved rows by reason: null requested Species, null given Species, invalid/placeholder Species.
   - Set changes-made status only when at least one eligible row is actually changed.

2. `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
   - Add a defensive writer guard in `setInGameTrades(...)` for Gen3 rows whose Species fields are null or not safely mappable.
   - For guarded rows, continue without writing any bytes for that table entry so the raw row remains preserved.
   - Keep `TradesUnused` behavior unchanged; this guard is an additional content-safety guard, not a replacement for the ROM-entry skip list.

3. `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/InGameTrade.java`
   - Optional only if a later branch needs explicit row status such as `preserveOnly`, `skipReason` or original table index.
   - Do not add this unless simple local guards are insufficient.

4. `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/log/RandomizationLogger.java`
   - Optional but likely needed for clear status.
   - Log or summarize skipped/preserved In-Game Trade rows so the user can distinguish guarded no-op behavior from successful row randomization.

5. `02_external/upr-fvx/random/src/main/resources/com/uprfvx/random/gui/Bundle.properties`
   - Optional only if new localized log/status strings are added.

The narrowest first implementation should try to stay in `TradeRandomizer.java` and `Gen3RomHandler.java`, adding logger/resource changes only if skipped-row status cannot be reported clearly through existing log paths.

## Non-goals for the later fix

- Do not correct `TradeTableOffset`, `TradeTableSize` or row shape in the same branch.
- Do not implement text/Nickname/OT randomization.
- Do not implement IV randomization.
- Do not implement Trade Held Item randomization.
- Do not promote In-Game Trades to GUI-compatible.
- Do not touch Static/Gift, Starters, Trainers, Wild, Held Items, Field Items, Pickup, Shops, Text/Menu repointing, or other feature scopes.

## Later fix stop criteria

A later code-fix branch must stop before implementation or smoke if any of these are true:

- The branch would need ROM bytes, private paths, hashes, output ROMs, saves, logs, builds or tool binaries in committed docs.
- The fix requires changing multiple feature scopes.
- The fix requires text, Nickname, OT, IV or Trade Held Item writes.
- The fix cannot preserve skipped row bytes.
- The fix cannot distinguish changed rows from skipped/preserved rows in status/logging.
- The implementation would silently mark changes made when every modeled row is skipped.
- The implementation needs a locator or row-shape correction instead of a null-request guard.

## Later fix exit criteria

A later implementation can be considered ready for a guarded write/reload diagnostic only if all of these are true:

- The code compiles.
- Rows with `requestedSpecies == null` are skipped before mutation and before write.
- Rows with null/invalid/placeholder offered/given or requested Species are skipped before mutation and before write.
- Skipped rows preserve every row byte by avoiding writer calls for that entry.
- `skippedNullRequestedTradeRows` is reported or otherwise visible.
- `skippedInvalidTradeSpeciesRows` / `skippedPlaceholderTradeSpeciesRows` are reported or otherwise visible.
- `changedTradeRows=0` is possible and must not be logged as GUI-compatible randomization.
- Text/Nickname/OT/IV/Held Item writes remain disabled in the first diagnostic.
- No Starter, Static/Gift, Trainer, Wild, Held Items or Item scopes change.

## Recommended next step

Keep In-Game Trades closed as `blocked-pending-evidence`. If implementation is desired later, open a separate `compat/...` branch for a defensive null-request guard only. The first implementation branch should prove skip/preserve behavior and explicit status reporting before any Species randomization smoke is considered.
