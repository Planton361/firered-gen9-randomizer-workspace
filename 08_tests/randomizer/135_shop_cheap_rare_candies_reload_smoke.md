# Diagnose 135 - Shop Cheap Rare Candies Reload Smoke

## Scope

- Feature: FVX-ITEM-009 Cheap Rare Candies.
- Tested mode: Shop-only `Settings.ShopItemsMod = UNCHANGED` with `addCheapRareCandiesToShops=true`.
- Explicitly disabled: `balanceShopPrices`, `guaranteeEvolutionItems`, `guaranteeXItems`, `banBadRandomShopItems`, `banRegularShopItems`, `banOPShopItems`.
- Out of scope: Shop Random, Shop Shuffle, Balance Shop Prices combination, Bans, Guarantees, Field Items, Pickup, Held Items.
- Candidate source: local CFRU/DPE Gen9-BPRE candidate released for this block; no private path, ROM name, hash, pointer, offset, raw byte, or script data is documented.

## Baseline

- Diagnose 123 confirmed the local Shop candidate structure.
- Diagnose 133 planned Cheap Rare Candies as separate from Balance Shop Prices.
- Diagnose 134 passed Balance Shop Prices only.
- Cheap Rare Candies is expected to change Shop lists and touch the Rare Candy price.
- SkipShops are measured in this smoke, not assumed preserve-only.

## Smoke result

PASS.

FVX-ITEM-009 is documented as GUI-compatible only for Cheap Rare Candies in the tested Shop-only scope. Save, log, output and reload succeeded. Shop item total grew by 23 entries and reload stayed stable. Rare Candy writes persisted after reload. Rare Candy price was touched and reload-stable. Field Items, Pickup and Held Items stayed unchanged. Balance Prices + Cheap Rare Candies combination is not promoted.

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

Skipped Shop Rare Candy writes are observed for this option because Cheap Rare Candies adds to Shop lists instead of preserving SkipShops. This is not treated as a preserve-policy failure for Diagnose 135.

## Price finding

- `priceTableReadable=true`
- `priceTableTouched=true`
- `priceEntriesBefore=1779`
- `priceEntriesAfter=1779`
- `priceEntriesReload=1779`
- `rareCandyPriceTouched=true`
- `rareCandyPriceReloadStable=true`
- `priceReloadMismatches=0`

The price table was touched as expected because Rare Candy is made cheap. Price entry count and reload comparison stayed stable.

## Scope safety

- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `heldItemScopeChanged=false`
- No Shop Random or Shop Shuffle option was enabled.
- No Ban, Guarantee, or Balance Shop Prices option was enabled.
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
| rareCandyPriceTouched | true |
| rareCandyPriceReloadStable | true |
| priceTableReadable | true |
| priceTableTouched | true |
| priceEntriesBefore | 1779 |
| priceEntriesAfter | 1779 |
| priceEntriesReload | 1779 |
| priceReloadMismatches | 0 |
| skippedShopRareCandyWrites | 20 |
| fieldItemScopeChanged | false |
| pickupScopeChanged | false |
| heldItemScopeChanged | false |
| exceptionClass | none |
| stacktrace | none |

## Risks / blockers

- Balance Prices + Cheap Rare Candies combination remains untested and must not be inferred from the two individual FVX-ITEM-009 smokes.
- SkipShop preservation is not a valid success criterion for Cheap Rare Candies because the option writes Rare Candy entries into skipped shops in this observed flow.
- No Ban combinations or Evolution+X combination coverage is implied by this smoke.

## Decision

- Promote FVX-ITEM-009 only for Cheap Rare Candies in the tested Shop-only `ShopItemsMod.UNCHANGED + addCheapRareCandiesToShops=true` scope.
- Keep Balance Prices + Cheap Rare Candies combination open.

## Next minimal step

Decide whether Balance Prices + Cheap Rare Candies combination coverage is needed or close the Shop Items scope.
