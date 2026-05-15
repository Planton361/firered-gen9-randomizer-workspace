# Diagnose 134 - Shop Balance Prices Reload Smoke

## Scope

- Feature: FVX-ITEM-009 Balance Shop Prices.
- Tested mode: Shop-only `Settings.ShopItemsMod = UNCHANGED` with `balanceShopPrices=true`.
- Explicitly disabled: `addCheapRareCandiesToShops`, `guaranteeEvolutionItems`, `guaranteeXItems`, `banBadRandomShopItems`, `banRegularShopItems`, `banOPShopItems`.
- Out of scope: Shop Random, Shop Shuffle, Cheap Rare Candies, Bans, Guarantees, Field Items, Pickup, Held Items, Ban combinations, and Evolution+X combination.
- Candidate source: local CFRU/DPE Gen9-BPRE candidate released for this block; no private path, ROM name, hash, pointer, offset, raw byte, or script data is documented.

## Baseline

- Diagnose 133 planned FVX-ITEM-009 as a separate Shop-only price / Cheap Rare Candy subscope.
- Balance Shop Prices is expected to write only price fields through `getShopPrices()` / `setShopPrices(...)`.
- `ShopItemsMod.UNCHANGED` was selected to avoid Shop-list randomization.
- Cheap Rare Candies remain a later separate smoke because they grow Shop item lists and also set the Rare Candy price.

## Smoke result

PASS.

`FVX-ITEM-009` is documented as GUI-compatible only for Balance Shop Prices in the tested Shop-only scope.

- Save, log, output ROM creation, and reload succeeded.
- Price table was readable, touched, and reload-stable.
- `balancedPriceWrites=132` and `priceReloadMismatches=0`.
- Shop count, Shop item total, terminator model, skipped Shops, and foreign item scopes stayed stable.
- Cheap Rare Candies were not tested and are not promoted.

## Shop structure / reload finding

| Metric | Before | After | Reload |
| --- | ---: | ---: | ---: |
| shopCount | 23 | 23 | 23 |
| shopItemsTotal | 157 | 157 | 157 |

Additional reload metrics:

- `terminatorModelStableAfter=true`
- `terminatorModelStableReload=true`
- `shopLengthMismatchesAfter=0`
- `shopLengthMismatchesReload=0`
- `shopItemReloadMismatches=0`

## Price finding

| Metric | Value |
| --- | ---: |
| priceTableReadable | true |
| priceTableTouched | true |
| priceEntriesBefore | 1779 |
| priceEntriesAfter | 1779 |
| priceEntriesReload | 1779 |
| balancedPriceWrites | 132 |
| priceReloadMismatches | 0 |

Cheap Rare Candies were not tested in this block:

- `cheapRareCandyWrites=0`
- `cheapRareCandyReloadPresent=not_tested`

## Preserve / skip finding

- `skippedShopItemMismatchesAfter=0`
- `skippedShopItemMismatchesReload=0`
- Shop item lists stayed unchanged with `ShopItemsMod.UNCHANGED`.
- Skipped Shops stayed preserve-only for this price-only smoke.

## Safety / write-quality metrics

- `candidateFilesChecked=4`
- `candidateLoaded=true`
- `smokeExecuted=true`
- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- `reloadSuccessful=true`
- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `heldItemScopeChanged=false`
- `exceptionClass=none`
- `stacktrace=none`

## Risks / blockers

No blocker for the tested Balance Shop Prices subscope.

Remaining risks:

- Cheap Rare Candies are not tested and remain separate because they change Shop-list lengths and Rare Candy price.
- Balance Prices + Cheap Rare Candies combination is not tested.
- Ban combinations and Evolution+X combination remain optional separate follow-ups and are not implied by this smoke.

## Status decision

- FVX-ITEM-009 Balance Shop Prices: GUI-compatible in the tested Shop-only scope.
- FVX-ITEM-009 Cheap Rare Candies: still write-modeled / untested.
- FVX-ITEM-009 Balance Prices + Cheap Rare Candies combination: not tested.

## Next minimal step

Run a Shop-only Cheap Rare Candies write/reload smoke only if the same safety rules and sanitized candidate handling are preserved.
