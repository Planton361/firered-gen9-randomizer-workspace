# Diagnose 132 - Shop Guarantee X Items Reload Smoke

## Scope

- Feature: FVX-ITEM-008 Guarantee X Items.
- Tested mode: Shop-only `Settings.ShopItemsMod = RANDOM` with `guaranteeXItems=true`.
- Explicitly disabled: `guaranteeEvolutionItems`, `banBadRandomShopItems`, `banRegularShopItems`, `banOPShopItems`, `balanceShopPrices`, `addCheapRareCandiesToShops`.
- Out of scope: Field Items, Pickup, Held Items, Ban combinations, prices, Cheap Rare Candies, Guarantee Evolution Items, and the Evolution+X combination.
- Candidate source: local CFRU/DPE Gen9-BPRE candidate released for this block; no private path, ROM name, hash, pointer, offset, raw byte, or script data is documented.

## Baseline

- FVX-ITEM-005 Shop Shuffle is GUI-compatible in the tested Shop-only scope.
- FVX-ITEM-006 Shop Random is GUI-compatible in the tested Shop-only scope.
- FVX-ITEM-007 single Ban Bad, Ban Regular, and Ban OP scopes are reload-stable individually; Ban combinations remain untested.
- FVX-ITEM-008 Guarantee Evolution Items is reload-stable in its tested Shop-only scope.
- Diagnose 130 established that Guarantee flags apply only with `ShopItemsMod.RANDOM`.
- Guarantee placement replaces existing Shop slots; Shop lists are not lengthened.
- Placement is restricted to Special Shops / MainGame Special Shops.
- `SkipShops` remain preserve-only.

## Smoke result

PASS.

`FVX-ITEM-008` is documented as GUI-compatible for Guarantee X Items in the tested Shop-only Random scope.

- Save, log, output ROM creation, and reload succeeded.
- Shop count, Shop lengths, terminator model, skipped Shops, prices, and foreign item scopes stayed stable.
- All expected X Items were present after write and after reload.
- Guarantee Evolution Items were not tested in this block.
- FVX-ITEM-008 is not automatically promoted for the combined Evolution+X configuration.
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

## Guarantee X finding

| Metric | Value |
| --- | ---: |
| guaranteePlacementShopCount | 3 |
| guaranteedXItemsExpected | 7 |
| guaranteedXItemsPresent | 7 |
| guaranteedXItemsMissing | 0 |
| guaranteedXItemsReloadPresent | 7 |
| guaranteedXItemsReloadMissing | 0 |

Guarantee Evolution Items were not tested in this block:

- `guaranteedEvolutionItemsPresent=not_tested`
- `guaranteedEvolutionItemsMissing=not_tested`

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

- The Evolution+X combination remains untested and is not implied by the two individual passes.
- FVX-ITEM-007 Ban combinations remain optional later coverage and are not implied by this smoke.
- FVX-ITEM-009 price balancing and Cheap Rare Candies remain separate writer scopes.
- The result depends on the observed replacement-without-length-growth model; future changes that lengthen Shop lists require separate repointing and terminator checks.

## Status decision

- FVX-ITEM-008 Guarantee Evolution Items: GUI-compatible in its tested Shop-only Random scope.
- FVX-ITEM-008 Guarantee X Items: GUI-compatible in the tested Shop-only Random scope.
- FVX-ITEM-008 combined Guarantee Evolution + X: not tested.
- FVX-ITEM-009: not promoted.

## Next minimal step

Decide whether FVX-ITEM-008 needs Evolution+X combination coverage or move to the separate FVX-ITEM-009 prices / Cheap Rare Candies scope plan.
