# Diagnose 153: In-Game Trades table-model blocker plan

## Scope

This is a read-only blocker plan for the CFRU/DPE Gen9-BPRE In-Game Trades locator and table model. It explains why Diagnose 152 does not permit a species-only write/reload smoke yet.

No code is changed. No build, Randomizer run, ROM write, save, output ROM or artifact access is performed.

## Starting point

Diagnose 152 loaded a local BPRE candidate read-only but classified the current UPR-FVX Gen3 BPRE trade-table model as blocked/preflight:

- `tradeScanSuccessful=false`
- `tradeCount=3`
- `requestedSpeciesNullCount=3`
- `invalidTradeSpecies=6`
- `placeholderTradeSpecies=6`
- fixed-length text fields were field-readable but terminator classification was not stable

Therefore no In-Game Trade species-only smoke is safe yet.

## Blocker assessment

The blocker is table-model/locator safety, not Randomizer option wiring. UPR-FVX has an In-Game Trades GUI path and a Gen3 reader/writer, but the current BPRE ROM-entry trade locator does not classify valid active CFRU/DPE Gen9-BPRE trade rows in the candidate.

A write smoke would call `setInGameTrades(...)` on rows whose Species fields are not proven valid. That is unsafe because the Gen3 writer writes both given and requested species through dereferenced Species objects and internal ID mapping.

## Relevant code paths

- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`
  - `maybeRandomizeInGameTrades()` calls the trade randomizer for `RANDOMIZE_GIVEN` and `RANDOMIZE_GIVEN_AND_REQUESTED`.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/Settings.java`
  - `InGameTradesMod`: `UNCHANGED`, `RANDOMIZE_GIVEN`, `RANDOMIZE_GIVEN_AND_REQUESTED`.
  - Subflags: nicknames, OTs, IVs and items.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TradeRandomizer.java`
  - `randomizeIngameTrades()` always randomizes given species when trade randomization is enabled.
  - Requested species are randomized only for the requested+given mode, except same-species trades are preserved to the new given species.
  - Nickname/OT/IV/item fields are optional subfeatures but share the same final `setInGameTrades(...)` write.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
  - `getInGameTrades()` reads `TradeTableOffset`, `TradeTableSize`, `TradesUnused` from the ROM entry.
  - It assumes 60-byte entries and reads nickname, given species, six IV bytes, OT ID, held item, OT name and requested species at fixed positions.
  - `setInGameTrades(...)` writes fixed-length nickname/OT fields, IV bytes, held item and both species fields.
- `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`
  - Provides the Gen3 BPRE trade table locator and count values.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/InGameTrade.java`
  - `requestedSpecies` is nullable in the shared model, but the Gen3 writer does not defend against null requested species.

## Answers to blocker questions

1. Trade table offset and count come from the Gen3 ROM entry via `TradeTableOffset`, `TradeTableSize` and `TradesUnused`.
2. The current BPRE ROM entry is not proven valid for the CFRU/DPE Gen9-BPRE candidate because the read-only diagnostic did not find valid active trade Species fields.
3. The three rows classify as placeholder/invalid Species because the active-row model reads zero/null-like Species values from the expected Species positions.
4. The rows may be wrong-location data, disabled/dummy rows, or a changed CFRU/DPE table shape; Diagnose 152 cannot prove they are real active trades.
5. `TradesUnused` is interpreted as a sorted list of entry indexes to skip while iterating the fixed-size table; it is not a content-based dummy-row detector.
6. CFRU/DPE may keep vanilla table metadata, relocate the table, disable trades, or replace behavior via scripts; this must be checked read-only before any write plan.
7. `requestedSpecies` is nullable in the UPR-FVX model, but the Gen3 writer dereferences it when writing, so active null rows must be skipped/preserved or guarded before writes.
8. The likely fix category must be determined by diagnostics: ROM-entry/locator correction, dummy-row classification, nullable requested-species guard, or unsupported status.
9. A write smoke requires valid active rows, no invalid active Species, and a clear skip policy for null requested Species.
10. Nickname and OT fields stay out of the first fix/smoke; they are only classified read-only until fixed-length string safety is separately proven.

## Hypotheses to test read-only next

- The BPRE `TradeTableOffset` no longer points at the active CFRU/DPE trade table.
- The table exists but the entry shape differs from vanilla Gen3 60-byte trades.
- The rows are dummy/disabled rows and need content-based skip classification in addition to `TradesUnused`.
- CFRU/DPE uses scripts or a custom system instead of vanilla In-Game Trade table data.
- `requestedSpecies=null` must be preserve/skip behavior for Gen3 or guarded before any writer path.

## Recommended next diagnostic block

Run an In-Game Trades locator/table-model read-only diagnostic. It should:

- compare ROM-entry table assumptions against candidate-read field plausibility without documenting private offsets or raw bytes;
- classify whether active trade rows exist at all;
- determine whether rows are vanilla 60-byte entries, dummy rows, relocated rows or unsupported;
- verify `TradesUnused` and any additional dummy-row policy;
- confirm requested-species null handling requirements;
- keep Nickname/OT text fields read-only and unmodified;
- recommend either a ROM-entry/locator fix plan, dummy-row skip plan, defensive null-request plan, or unsupported-scope decision.

## Minimum criteria before a later species smoke

- `tradeScanSuccessful=true`
- `validActiveTradeRows > 0`
- `requestedSpeciesNullCount=0` for active rows, or active null-request rows are explicitly preserve/skip
- `invalidTradeSpecies=0` for active rows
- `unloadedTradeSpecies=0` for active rows
- `placeholderTradeSpecies=0` for active rows unless explicitly classified as skipped dummy rows
- `tradeNicknameFieldsReadable=true`
- `tradeOtFieldsReadable=true`
- text fields classified but not modified
- `starterScopeChanged=false`
- `staticGiftScopeChanged=false`
- `trainerScopeChanged=false`
- `heldItemScopeChanged=false`
- `wildScopeChanged=false`
- `itemScopesChanged=false`

## Risks and blockers

- Writing with the current model can dereference null requested species.
- Species writes can target invalid internal IDs if the locator is wrong.
- Fixed-length Nickname/OT fields can be corrupted if text work is mixed into locator or species smoke work.
- A dummy-row skip policy based only on `TradesUnused` may be insufficient for CFRU/DPE.
- If CFRU/DPE disables or script-replaces In-Game Trades, UPR-FVX may need to mark the scope unsupported rather than write vanilla tables.

## Decision

Do not run an In-Game Trades species-only write/reload smoke yet. The next block must be read-only locator/table-model diagnostics.
