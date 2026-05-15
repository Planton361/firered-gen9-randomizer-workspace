# Diagnose 131 - Shop Guarantee Evolution Items Reload Smoke

## Scope

- Feature: FVX-ITEM-008 Guarantee Evolution Items.
- Tested mode: Shop-only `Settings.ShopItemsMod = RANDOM` with `guaranteeEvolutionItems=true`.
- Explicitly disabled: `guaranteeXItems`, `banBadRandomShopItems`, `banRegularShopItems`, `banOPShopItems`, `balanceShopPrices`, `addCheapRareCandiesToShops`.
- Out of scope: Field Items, Pickup, Held Items, Ban combinations, prices, Cheap Rare Candies, Guarantee X Items.
- Candidate source: local CFRU/DPE Gen9-BPRE candidate released for this block; no private path, ROM name, hash, pointer, offset, raw byte, or script data is documented.

## Baseline

- FVX-ITEM-005 Shop Shuffle is GUI-compatible in the tested Shop-only scope.
- FVX-ITEM-006 Shop Random is GUI-compatible in the tested Shop-only scope.
- FVX-ITEM-007 single Ban Bad, Ban Regular, and Ban OP scopes are reload-stable individually; Ban combinations remain untested.
- Diagnose 130 established that Guarantee flags apply only with `ShopItemsMod.RANDOM`.
- Guarantee placement replaces existing Shop slots; Shop lists are not lengthened.
- Placement is restricted to Special Shops / MainGame Special Shops.
- `SkipShops` remain preserve-only.

## Smoke result

PASS.

`FVX-ITEM-008` is documented as GUI-compatible only for Guarantee Evolution Items in the tested Shop-only Random scope.

- Save, log, output ROM creation, and reload succeeded.
- Shop count, Shop lengths, terminator model, skipped Shops, prices, and foreign item scopes stayed stable.
- All expected Evolution guarantee items were present after write and after reload.
- Guarantee X Items remain untested and are not promoted.
- FVX-ITEM-009 prices / Cheap Rare Candies remain out of scope and are not promoted.

## Shop structure / reload finding

| Metric | Before | After | Reload |
| --- | ---: | ---: | ---: |
| shopCount | 23 | 23 | 23 |
| mainGameShopCount | 3 | 3 | 3 |
| skippedShopCount | 20 | 20 | 20 |
| specialShopCount | 3 | 3 | 3 |
| shopItemsTotal | 157 | 157 | 157 |
| minShopLength | 2 | 2 | 2 |
| maxShopLength | 9 | 9 | 9 |

Additional reload metrics:

- `terminatorModelStableAfter=true`
- `terminatorModelStableReload=true`
- `shopLengthMismatchesAfter=0`
- `shopLengthMismatchesReload=0`
- `shopItemReloadMismatches=0`
- `specialShopPolicyMismatches=0`

## Preserve / skip finding

- `skippedShopItemMismatchesAfter=0`
- `skippedShopItemMismatchesReload=0`
- `skipShopsPreserved=true`
- Skipped Shops stayed preserve-only.
- Special Shop policy stayed stable across write and reload.

## Guarantee Evolution finding

| Metric | Value |
| --- | ---: |
| guaranteePlacementShopCount | 2 |
| guaranteedEvolutionItemsExpected | 6 |
| guaranteedEvolutionItemsPresent | 6 |
| guaranteedEvolutionItemsMissing | 0 |
| guaranteedEvolutionItemsReloadPresent | 6 |
| guaranteedEvolutionItemsReloadMissing | 0 |

Guarantee X Items were not tested in this block:

- `guaranteedXItemsPresent=not_tested`
- `guaranteedXItemsMissing=not_tested`

## Safety / write-quality metrics

- `candidateFilesChecked=4`
- `candidateLoaded=true`
- `smokeExecuted=true`
- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- `reloadSuccessful=true`
- `invalidShopItemWrites=0`
- `unloadedShopItemWrites=0`
- `fallbackShopItemWrites=0`
- `placeholderShopItemWrites=0`
- `priceTableTouched=false`
- `priceReloadMismatches=0`
- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `heldItemScopeChanged=false`
- `exceptionClass=none`
- `stacktrace=none`

## Risks / blockers

- Guarantee X Items remain untested and must stay separate.
- FVX-ITEM-008 is not promoted for combined Evolution+X guarantees yet.
- FVX-ITEM-007 Ban combinations remain optional later coverage and are not implied by this smoke.
- FVX-ITEM-009 price balancing and Cheap Rare Candies remain separate writer scopes.
- The result depends on the observed replacement-without-length-growth model; future changes that lengthen Shop lists require separate repointing and terminator checks.

## Status decision

- FVX-ITEM-008 Guarantee Evolution Items: GUI-compatible in the tested Shop-only Random scope.
- FVX-ITEM-008 Guarantee X Items: still write-modeled / untested.
- FVX-ITEM-008 combined Guarantee Evolution + X: not tested.
- FVX-ITEM-009: not promoted.

## Next minimal step

Run a Shop-only Guarantee X Items write/reload smoke only if the same safety rules and sanitized candidate handling are preserved.
