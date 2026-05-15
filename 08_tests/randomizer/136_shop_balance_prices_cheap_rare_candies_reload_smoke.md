# Diagnose 136 - Shop Balance Prices + Cheap Rare Candies Reload Smoke

## Scope

- Feature: FVX-ITEM-009 Balance Shop Prices + Cheap Rare Candies combination.
- Tested mode: Shop-only `Settings.ShopItemsMod = UNCHANGED` with `balanceShopPrices=true` and `addCheapRareCandiesToShops=true`.
- Explicitly disabled: `guaranteeEvolutionItems`, `guaranteeXItems`, `banBadRandomShopItems`, `banRegularShopItems`, `banOPShopItems`.
- Out of scope: Shop Random, Shop Shuffle, Bans, Guarantees, Field Items, Pickup, Held Items.
- Candidate source: local CFRU/DPE Gen9-BPRE candidate released for this block; no private path, ROM name, hash, pointer, offset, raw byte, or script data is documented.

## Baseline

- Diagnose 123 confirmed the local Shop candidate structure.
- Diagnose 133 planned FVX-ITEM-009 as separate price and Cheap Rare Candy subscopes, with the combination only after stable individual smokes.
- Diagnose 134 passed Balance Shop Prices only.
- Diagnose 135 passed Cheap Rare Candies only.
- This block tests the explicit combination and does not imply Ban, Guarantee, Shop Random, or Shop Shuffle coverage.

## Smoke result

PASS.

FVX-ITEM-009 is documented as GUI-compatible for Balance Shop Prices, Cheap Rare Candies, and their tested Shop-only combination. Save, log, output and reload succeeded. Shop item total grew by 23 entries and reload stayed stable. Rare Candy writes persisted after reload. Price table writes, including balanced prices and Rare Candy price, were reload-stable. Field Items, Pickup and Held Items stayed unchanged.

## Shop structure / reload finding

| Metric | Before | After | Reload |
| --- | ---: | ---: | ---: |
| shopCount | 23 | 23 | 23 |
| shopItemsTotal | 157 | 180 | 180 |
| terminatorModelStable | n/a | true | true |
| shopLengthMismatches | n/a | 0 | 0 |

Additional reload metrics:

- `shopItemsTotalDeltaAfter=23`
- `shopItemsTotalDeltaReload=23`
- `shopItemReloadMismatches=0`

## Rare Candy finding

- `rareCandyWrites=23`
- `rareCandyReloadPresent=true`
- `skippedShopRareCandyWrites=20`

Skipped Shop Rare Candy writes are observed for this option because Cheap Rare Candies adds to Shop lists instead of preserving SkipShops. This remains expected for the Cheap Rare Candies path and is not treated as a preserve-policy failure.

## Price finding

- `priceTableReadable=true`
- `priceTableTouched=true`
- `priceEntriesBefore=1779`
- `priceEntriesAfter=1779`
- `priceEntriesReload=1779`
- `balancedPriceWrites=132`
- `rareCandyPriceTouched=true`
- `rareCandyPriceReloadStable=true`
- `priceReloadMismatches=0`

The combination touched the price table as expected. Balanced price writes were present, Rare Candy price was touched, and the reloaded price table matched the written state.

## Scope safety

- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `heldItemScopeChanged=false`
- No Shop Random or Shop Shuffle option was enabled.
- No Ban or Guarantee option was enabled.
- No code, submodule, build output, ROM, save, emulator state, log, output ROM, Randomizer JAR, tool binary, private path, hash, pointer, offset, raw byte, script data, secret, token, or `.env` content is documented or committed.

## Metrics

| Metric | Value |
| --- | --- |
| candidateFilesChecked | 4 |
| candidateLoaded | true |
| smokeExecuted | true |
| saveSuccessful | true |
| logSuccessful | true |
| outputRomExists | true |
| logNonEmpty | true |
| reloadSuccessful | true |
| shopCountBefore | 23 |
| shopCountAfter | 23 |
| shopCountReload | 23 |
| shopItemsTotalBefore | 157 |
| shopItemsTotalAfter | 180 |
| shopItemsTotalReload | 180 |
| shopItemsTotalDeltaAfter | 23 |
| shopItemsTotalDeltaReload | 23 |
| terminatorModelStableAfter | true |
| terminatorModelStableReload | true |
| shopLengthMismatchesAfter | 0 |
| shopLengthMismatchesReload | 0 |
| shopItemReloadMismatches | 0 |
| rareCandyWrites | 23 |
| rareCandyReloadPresent | true |
| skippedShopRareCandyWrites | 20 |
| priceTableReadable | true |
| priceTableTouched | true |
| priceEntriesBefore | 1779 |
| priceEntriesAfter | 1779 |
| priceEntriesReload | 1779 |
| balancedPriceWrites | 132 |
| rareCandyPriceTouched | true |
| rareCandyPriceReloadStable | true |
| priceReloadMismatches | 0 |
| fieldItemScopeChanged | false |
| pickupScopeChanged | false |
| heldItemScopeChanged | false |
| exceptionClass | none |
| stacktrace | none |

## Shop scope closure decision

The tested CFRU/DPE Gen9-BPRE Shop Items scope is closed for the individually tested GUI-compatible paths:

- FVX-ITEM-005 Shop Items Shuffle.
- FVX-ITEM-006 Shop Items Random.
- FVX-ITEM-007 Shop Item Bans for Ban Bad, Ban Regular, and Ban OP individually.
- FVX-ITEM-008 Guarantee Evolution Items and Guarantee X Items individually.
- FVX-ITEM-009 Balance Shop Prices, Cheap Rare Candies, and their tested combination.

Not implied by this closure:

- Ban combinations.
- Guarantee Evolution + X combination.
- Any Field Items, Pickup, Held Items, TM/HM/Tutor/Learnset, Encounter, Trainer, Starter, Wild, Evolution, Text/Menu, Palette/Graphics, MoveData/MoveNames, or TypeChart work.

## Risks / blockers

No blocker remains for the tested Shop Items scope.

Residual limits:

- Ban combinations remain optional future regression coverage, not required for closing the tested Shop scope.
- Guarantee Evolution + X combination remains optional future regression coverage, not required for closing the tested Shop scope.
- Cheap Rare Candies intentionally writes Rare Candy entries into skipped shops in the observed flow.

## Decision

- Promote FVX-ITEM-009 for Balance Prices + Cheap Rare Candies in the tested Shop-only `ShopItemsMod.UNCHANGED` combination scope.
- Mark Shop Items scope as closed for the tested CFRU/DPE Gen9-BPRE GUI-compatible paths.

## Next minimal step

Prepare the next major scope: Held Items diagnostics plan.
