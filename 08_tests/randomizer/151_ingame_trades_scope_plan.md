# Diagnose 151: In-Game Trades scope diagnostics plan

## Scope

This is a read-only planning protocol for CFRU/DPE Gen9-BPRE In-Game Trades as a new, separate Randomizer scope. It does not run the Randomizer, does not build, does not access ROMs or artifacts, and does not change code.

The scope is intentionally separate from Standard Wild, Special Wild, Starters, Static/Gift Pokemon, Trainer Pokemon, Held Items, Field Items, Pickup Items and Shop Items. Trade held items are considered only as fields inside the trade table.

## Context

- Standard Wild remains P0-supported.
- Special Wild systems are documented as dormant, runtime-only or future scope in Diagnose 150.
- Field, Pickup, Shop and Held Item scopes are closed in the tested CFRU/DPE Gen9-BPRE scope.
- Starters, Statics, Trainer and Evolution Species write paths were handled in earlier diagnostics.
- In-Game Trades remain a genuinely open GUI scope and need their own candidate diagnostic before any write smoke.

## Relevant code paths

- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`
  - `maybeRandomizeInGameTrades()` dispatches only when `Settings.InGameTradesMod` is not `UNCHANGED`.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/Settings.java`
  - `Settings.InGameTradesMod`: `UNCHANGED`, `RANDOMIZE_GIVEN`, `RANDOMIZE_GIVEN_AND_REQUESTED`.
  - Additional flags: `randomizeInGameTradesNicknames`, `randomizeInGameTradesOTs`, `randomizeInGameTradesIVs`, `randomizeInGameTradesItems`.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TradeRandomizer.java`
  - `randomizeIngameTrades()` mutates the in-memory `InGameTrade` list and calls `romHandler.setInGameTrades(trades)`.
  - Given species are always randomized when the trade mode is active.
  - Requested species are randomized only for `RANDOMIZE_GIVEN_AND_REQUESTED`; if the original requested species equals the original given species, the request is preserved to the new given species.
  - Nickname and OT randomization use custom-name pools filtered by handler-reported maximum internal string length.
  - IVs use six fields and Gen3 uses 0-31 values.
  - Held items use `romHandler.getAllowedItems()`.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/InGameTrade.java`
  - Data model: `requestedSpecies`, `givenSpecies`, `nickname`, `otName`, `otId`, `ivs`, `heldItem`.
  - `requestedSpecies` can be null in the model, but Gen3 write path should be diagnosed before assuming null-safe writes.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/RomHandler.java`
  - API: `getInGameTrades()` and `setInGameTrades(...)`.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
  - Gen3 trade table reader/writer for this target family.
  - Uses `TradeTableOffset`, `TradeTableSize`, `TradesUnused`, 60-byte entries and fixed field offsets.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/gui/RandomizerGUI.java`
  - GUI maps In-Game Trade radio buttons and suboptions to `Settings`.
- `02_external/upr-fvx/random/src/main/resources/com/uprfvx/random/gui/Bundle.properties`
  - GUI labels and tooltips for In-Game Trades.

## Expected data structure

Gen3 In-Game Trades are modeled as a table of fixed-size trade entries. The relevant UPR-FVX Gen3 handler fields are:

- trade table locator: `TradeTableOffset` and `TradeTableSize` from ROM entries.
- skip/preserve list: `TradesUnused`.
- entry size: 60 bytes in the Gen3 handler.
- nickname: fixed-length string field, written with length 12.
- given species: word field read through `pokesInternal[...]`; written through `pokedexToInternal[species.getNumber()]`.
- IVs: six byte fields.
- OT ID: word field.
- held item: word field with Gen3 standard/internal item-ID conversion.
- OT name: fixed-length string field, written with length 11.
- requested species: word field read through `pokesInternal[...]`; written through `pokedexToInternal[species.getNumber()]`.

## Scope assessment

In-Game Trades should be treated as a separate CFRU/DPE Gen9-BPRE Randomizer scope because they combine species writes, item writes, IV writes and fixed-length text writes in one table. The first diagnostic must be read-only and must establish whether the local candidate trade table is readable, how many rows are active after `TradesUnused`, and whether all fields map safely to loaded Species and Items.

No feature is promoted by this plan. The current state remains `planned / needs candidate diagnostic`.

## Risk assessment

- Species-ID mapping: Gen3 write path uses `pokedexToInternal[trade.getGivenSpecies().getNumber()]` and the same for requested species. CFRU/DPE Gen9 species must be verified for correct SpeciesSet/internal identity behavior before write smoke.
- Requested species nullability: the model allows null for some generations, while the Gen3 writer dereferences requested species; the candidate diagnostic must confirm Gen3 entries are non-null or document a blocker.
- Fixed-length strings: nickname and OT writes use fixed-length fields. Text randomization must not be combined with species smoke until length, terminator and reload behavior are proven.
- Item-ID mapping: trade held item writes use allowed-item pool plus Gen3 internal item conversion; invalid, unloaded, fallback and placeholder item writes need separate metrics.
- IV fields: six byte fields are expected; range and reload behavior should be diagnosed separately from species writes.
- Table length and unused rows: `TradeTableSize` and `TradesUnused` must be preserved; unused entries must not be mutated.
- Foreign scopes: Starter, Static/Gift, Trainer, Wild, Held Items and Item scopes must remain unchanged in later smokes.

## Preserve / skip policy

- Preserve all entries listed in `TradesUnused`.
- Preserve table count and active-row ordering.
- Preserve text fields in the first species-only smoke unless the text subfeature is explicitly under test.
- Preserve held items in the first species-only smoke unless the held-item subfeature is explicitly under test.
- Preserve IVs in the first species-only smoke unless the IV subfeature is explicitly under test.
- Treat Trade Held Items as trade-table fields, not as Wild/Trainer/Starter Held Items.

## Recommended diagnostic and smoke order

1. In-Game Trades read-only candidate diagnostic.
2. Given/Requested species-only write/reload smoke.
3. Held item-only write/reload smoke, if the read-only diagnostic confirms item-field safety.
4. Nickname/OT text smoke only as a separate fixed-length-string diagnostic and only after length/terminator policy is clear.
5. IV/random extras smoke separately after species/item/text are stable.

## Future diagnostic and smoke metrics

- `candidateLoaded`
- `tradeScanSuccessful`
- `tradeCount`
- `tradeTableEntrySize`
- `tradesUnusedCount`
- `requestedSpeciesTotal`
- `givenSpeciesTotal`
- `nullRequestedSpecies`
- `invalidTradeSpecies`
- `unloadedTradeSpecies`
- `fallbackTradeSpecies`
- `placeholderTradeSpecies`
- `tradeHeldItemsTotal`
- `invalidTradeItems`
- `unloadedTradeItems`
- `fallbackTradeItems`
- `placeholderTradeItems`
- `tradeNicknameFieldsReadable`
- `tradeOtFieldsReadable`
- `tradeIvFieldsReadable`
- `tradeNicknameMaxLength`
- `tradeOtMaxLength`
- `tradeIvFieldCount`
- `tradeSpeciesReloadMismatches`
- `tradeItemReloadMismatches`
- `tradeTextReloadMismatches`
- `tradeIvReloadMismatches`
- `starterScopeChanged=false`
- `staticGiftScopeChanged=false`
- `trainerScopeChanged=false`
- `heldItemScopeChanged=false`
- `wildScopeChanged=false`
- `itemScopesChanged=false`
- `exceptionClass`
- `stacktrace`

## Next minimal step

Run a read-only In-Game Trades candidate diagnostic that loads the candidate source, calls only the read path, records sanitized table and field metrics, and does not write or save anything.
