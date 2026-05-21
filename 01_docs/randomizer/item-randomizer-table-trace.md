# UPR-FVX Item Randomizer Table Trace

Stand: 2026-05-21

Scope: documentation-only trace of the tables and pools that UPR-FVX uses for Item Randomization
against the local CFRU/DPE workspace sources. No ROMs were read, copied, generated or tested. No
builds were executed. No UPR-FVX, CFRU or DPE code was changed.

## Executive Summary

UPR-FVX does not use one single item pool for all item features. Field items, shop items, pickup
items and trainer held items all start from ROM-loaded `ItemData` or fixed held-item lists, but each
feature applies different rules before writing.

Hard facts from the code:

- `Gen3RomHandler.loadItems()` loads final ROM item data through the `romEntry` key `ItemData`,
  whose value is populated from `readPointer(Gen3Constants.itemDataPointer)`.
- `getAllowedItems()` means `Item.isAllowed() == true`; `getNonBadItems()` additionally requires
  `!Item.isBad()`.
- `Ban Bad Items` switches Field/Shop/Pickup randomization from `getAllowedItems()` to
  `getNonBadItems()`. It does not create a separate CFRU source-table policy.
- Field-item randomization preserves TM-vs-non-TM slot class. Existing TM slots receive TMs;
  non-TM field spots do not receive TMs.
- Shop randomization removes TMs from the randomized shop filler pool. Shop shuffle only shuffles
  existing items among supported/special shops.
- Pickup randomization can include TMs only when `romHandler.canTMsBeHeld()` is true and
  `romHandler.isTMsReusable()` is false. The Gen3 default handler reports reusable TMs and
  non-holdable TMs, so the local CFRU stable profile should not get TMs through Pickup unless those
  handler assumptions change.
- Trainer held items do not use the Field/Shop/Pickup pool. They use fixed Gen3 held-item lists or
  sensible-item candidates, then pass through the same mechanic-item exclusion predicate.

Main policy finding: the current separation is mostly clean for Field and Shop item randomization,
but Pickup's conditional TM allowance is a real policy point. If future local settings make TMs
holdable and non-reusable, Pickup can legally select TMs.

## 1. Final ROM Table Loaded For ItemData

`Gen3RomHandler.addPointerBlock2ToRomEntry()` stores:

- `romEntry.putIntValue("ItemData", readPointer(Gen3Constants.itemDataPointer))`
- `romEntry.putIntValue("MoveData", readPointer(Gen3Constants.moveDataPointer))`

`Gen3RomHandler.loadItems()` then reads:

- item table start from `romEntry.getIntValue("ItemData")`
- item struct size from `romEntry.getIntValue("ItemEntrySize")`
- configured item count from `romEntry.getIntValue("ItemCount")`
- CFRU/DPE expanded fallback limit from `getItemLoadInternalLimit(...)`

The loaded `Item` model is then annotated:

- `allowed=false` for `Gen3Constants.bannedItems` and CFRU/DPE fallback names.
- `bad=true` for CFRU/DPE fallback names, CFRU/DPE encounter-held banned rows and
  `Gen3Constants.getBadItems(getROMType())`.
- `tm=true` for `ItemIDs.tm01` through `ItemIDs.tm01 + Gen3Constants.tmCount`.

Interpretation: FVX consumes the final built ROM's item table, not CFRU source files directly. CFRU
source files such as `include/constants/items.h` and `src/Tables/item_tables.c` define what the build
puts into ROM; FVX follows the resulting `ItemData` pointer.

Open verification: exact local final ROM `ItemData -> gItemData` symbol identity remains
`unclear / verify locally`, because no ROM or build artifact was inspected in this task.

## 2. Pools Built By FVX

| Pool | Codepath | Source | Contains TMs/HMs? | Contains Key Items? | Contains Mechanic Items? | Ban-Bad-Filter? | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Field Items: Shuffle | `GameRandomizer.maybeRandomizeFieldItems()` -> `ItemRandomizer.randomizeFieldItems()` | Existing `romHandler.getFieldItems()` slots from map item offsets | Preserves existing TM slots only; non-TM slots stay non-TM | Existing non-randomized key items are excluded if not exposed by `isFieldItemRandomizerApiSlot()` | Shuffle does not create new mechanic items, but can preserve existing exposed items | No | TMs and non-TMs are shuffled in separate stacks. |
| Field Items: Random / Random Even, TM slots | `randomizeTMFieldItems()` | `romHandler.getRequiredFieldTMs()`, `romHandler.getItems()`, original TM field slots | Yes, only in original TM slots | No direct key-item pool | If a mechanic item is also flagged TM, no extra mechanic filter is applied on this TM path | No | Required field TMs are forced first; filler TMs are unique. |
| Field Items: Random / Random Even, non-TM slots | `randomizeNonTMFieldItems()` | `getAllowedItems()` or `getNonBadItems()` from final `ItemData` | No; `possible.removeIf(Item::isTM)` | Normally no, because key/unique Gen3 items are `allowed=false` | Mega/Z/Dynamax-GMax filtered unless include settings are enabled | Yes, via `getNonBadItems()` when enabled | May avoid duplicate no-sell Mega Stones when shop prices are not balanced. |
| Shop Items: Shuffle | `ItemRandomizer.shuffleShopItems()` | Existing `romHandler.getShops()` special-shop item lists | Existing TMs remain possible if already in supported special shops | Existing shop content only | Existing shop content only | No | Only shops with `Shop.isSpecialShop()` are shuffled; skipped shops are not touched. |
| Shop Items: Random | `randomizeShopItems()`, `setupPossible()` | `getAllowedItems()` or `getNonBadItems()` from final `ItemData` | No; `possible.removeIf(Item::isTM)` | Normally no, because not allowed | Mega/Z/Dynamax-GMax filtered unless include settings are enabled | Yes, via `getNonBadItems()` when enabled | Optional regular-shop and overpowered-shop removals are separate filters. |
| Guaranteed Shop Items | `setupGuaranteed()` | `romHandler.getEvolutionItems()`, `romHandler.getXItems()` | No, unless a configured guaranteed item were a TM; not observed in Gen3 constants | No | Mega/Z/Dynamax-GMax filtered unless include settings are enabled | No direct bad filter | Guarantees are placed into supported special shops. |
| Pickup Items | `ItemRandomizer.randomizePickupItems()` | `getAllowedItems()` or `getNonBadItems()` from final `ItemData` | Conditional: TMs removed only if TMs cannot be held or are reusable | Normally no, because not allowed | Mega/Z/Dynamax-GMax filtered unless include settings are enabled | Yes, via `getNonBadItems()` when enabled | Preserves existing Pickup probability slots from `getPickupItems()`. |
| Trainer Held Items | `TrainerPokemonRandomizer.randomizeTrainerHeldItems()` -> `randomizeHeldItem()` | `romHandler.getAllHeldItems()` or `getAllConsumableHeldItems()` | No evidence that Gen3 fixed held-item lists include TMs/HMs | No | Mega/Z/Dynamax-GMax filtered unless include settings are enabled | No `Ban Bad Items` setting here | Existing Z-Crystals are preserved; Mega Stones are preserved when Mega swap owns them. |
| Sensible Trainer Held Items | `romHandler.getSensibleHeldItemsFor(...)` with fallback to all/consumable held items | Gen3 fixed lists plus move/species context | No evidence that sensible lists include TMs/HMs | No | Mega/Z/Dynamax-GMax filtered on sensible and fallback pools | No `Ban Bad Items` setting here | Missing movepools fall back instead of NPE. |
| Required / Progression Items | `romHandler.getRequiredFieldTMs()` only in field TM path | Static FVX Gen3 required-TM lists | Yes, TMs only | Not general key/progression items | Not a general mechanic pool | No | General required key items are not a visible item-randomizer pool in this code slice. |
| TM/HM Items | `Item.isTM()` flag in `loadItems()` and field/pickup logic | Final `ItemData` plus FVX static TM ID range | TMs flagged; HMs are globally banned by Gen3 constants | HMs are excluded through `bannedItems` | Mechanic TM classification not separately modeled | Not inherently bad | Expanded CFRU TM item IDs beyond the FVX static TM range need source/pointer verification before stronger claims. |

## 3. How `Ban Bad Items` Works

Code definition:

- `AbstractRomHandler.getAllowedItems()` returns all loaded non-null items where `item.isAllowed()`.
- `AbstractRomHandler.getNonBadItems()` returns `getAllowedItems()` filtered by `!item.isBad()`.
- Field, Shop and Pickup use `getNonBadItems()` only when their respective setting is enabled:
  `isBanBadRandomFieldItems()`, `isBanBadRandomShopItems()`, `isBanBadRandomPickupItems()`.

Bad item source in Gen3:

- `Gen3Constants.getBadItems(romType)` marks vanilla bad items such as mail, many berries,
  Pokemon-specific held items, contest scarves and FRLG-specific shoal/shard items as `bad=true`.
- CFRU/DPE fallback item names are marked `allowed=false` and `bad=true`.
- For CFRU/DPE Gen9 species mode, `cfruDpeEncounterHeldItemBannedItems` marks balls, mail,
  TM01-TM50, HM01-HM08 and modern special/system/form item ranges as disallowed/bad for encounter
  held-item loading.

Separate filters:

- Bad filter: `item.isBad()`.
- Banned/required/key exclusion: mostly `item.isAllowed() == false`, via `bannedItems` and fallback
  item handling.
- Overpowered shop filter: `romHandler.getOPShopItems()`, currently Rare Candy, money items,
  Lucky Egg and similar Gen3 constants.
- Regular shop filter: `romHandler.getRegularShopItems()`, from global regular-shop constants.
- Mechanic filter: `ItemMechanicPredicates.isItemAllowed(...)`.

TMs/HMs:

- HMs are globally banned in `Gen3Constants.bannedItems`.
- TMs are not automatically "bad" for all item pools. Field/Shop random pools remove TMs explicitly.
- Pickup removes TMs only when TMs cannot be held or are reusable.

Policy interpretation: `Ban Bad Items` is useful but coarse. It is not equivalent to "ban every
balance-sensitive or CFRU-mechanic-sensitive item".

## 4. Mechanic Item Filtering

Mechanic filtering is shared by `Randomizer.filterAllowedMechanicItems()` and
`filterAllowedMechanicItemSet()`. These build `ItemMechanicExclusionOptions` from:

- `Settings.isIncludeMegaItems()`
- `Settings.isIncludeZCrystalItems()`
- `Settings.isIncludeDynamaxGmaxItems()`

`ItemMechanicPredicates.isItemAllowed(...)` actively excludes these categories by default:

- `MEGA_STONE`
- `MEGA_ACCESSORY`
- `Z_CRYSTAL`
- `Z_ACCESSORY`
- `DYNAMAX_GIGANTAMAX`

`CfruDpeItemCategories` recognizes both canonical FVX IDs and source-backed CFRU/DPE names/ranges
for known mechanic items. It also classifies passive/source-backed categories:

- `ARCEUS_PLATE`
- `GENESECT_DRIVE`
- `SILVALLY_MEMORY`
- `NECTAR_FORM_CHANGE`

Important caveat: Plates, Drives, Memories and Nectars/Form-change items are categorized but are not
actively rejected by `ItemMechanicPredicates.isItemAllowed(...)` today. There is no separate
user-facing policy for those categories in the traced code.

| Category | Active Filtered? | User Policy? | Evidence |
| --- | --- | --- | --- |
| Mega Stones | Yes, unless Include Mega Items | Yes, global include setting | `ItemMechanicPredicatesTest`, `ItemDecisionTest` |
| Mega accessories | Yes, unless Include Mega Items | Yes, global include setting | `ItemMechanicPredicatesTest` |
| Z-Crystals | Yes, unless Include Z-Crystal Items | Yes, global include setting | `ItemMechanicPredicatesTest`, `ItemDecisionTest` |
| Z accessories | Yes, unless Include Z-Crystal Items | Yes, global include setting | `ItemMechanicPredicatesTest` |
| Dynamax/GMax items | Yes, unless Include Dynamax/GMax Items | Yes, global include setting | `ItemMechanicPredicatesTest`, `ItemDecisionTest` |
| Plates | No, categorized only | No | `passiveSourceBackedCategoriesAreClassifiedWithoutChangingMechanicFilters()` |
| Drives | No, categorized only | No | same test |
| Memories | No, categorized only | No | same test |
| Nectars / form-change items | No, categorized only | No | same test |

## 5. CFRU Tables Relevant To Item Randomization

| CFRU Source Table | Doku-Aussage | Wird direkt von FVX geschrieben? | Wird indirekt ueber finale ROM-Tabelle genutzt? | Risiko |
| --- | --- | --- | --- | --- |
| `include/constants/items.h` | CFRU docs say item indices are defined here and unused names should not be deleted. | No | Yes, compiled item IDs/names become final ROM `ItemData` and source IDs used by predicates. | Expanded IDs can differ from FVX's static TM range; verify local final item identity before stronger claims. |
| `src/Tables/item_tables.c` | CFRU docs list pickup, Fling, consumable effects and item type/sort tables here. | Not as source. FVX writes final ROM data only. | Partly: final Pickup table is located and written; item names/data are loaded through `ItemData`. | Static source tables such as `gFlingTable` and `gItemsByType` are not updated when FVX swaps item placements. |
| `gItemsByType` | CFRU docs tie it to item type sorting/classification. | No | No direct traced FVX read/write. | Random placement of items can expose item-type behavior the randomizer does not reason about. |
| `gFlingTable` | CFRU docs say unused item names should be removed here; table defines Fling behavior. | No | No direct traced FVX read/write. | If randomization surfaces unusual held items, battle behavior depends on this table, not on FVX pool policy. |
| `gConsumableItemEffects` | Listed in local CFRU `item_tables.c` table-to-edit header. | No | No direct traced FVX read/write. | Consumable semantics are engine-side; FVX sensible-item logic is only a pool heuristic. |
| `sPickupCommonItems` | CFRU docs: modify Pickup common items in `src/Tables/item_tables.c`; do not add new entries. | FVX writes the final ROM pickup item entries via `setPickupItems()`, not source. | Yes, via `getPickupItems()` table locator and metadata fallback. | Pointer/metadata locator must uniquely resolve the final table. |
| `sPickupRareItems` | Same as common pickup items. | Same as above. | Same as above. | Same as above. |
| TM Move Table / `gTMHMMoves` | CFRU docs: pointer at `0x125A8C`; DPE users modify `src/TM_Tutor_Tables.c`. | TM randomizer writes final TM move table, not ItemRandomizer. | ItemRandomizer only sees TM item flags; TM move identity comes from separate TM code path. | Item placement and TM move compatibility are separate concerns. |
| TM Compatibility Table / `gTMHMLearnsets` | CFRU docs: pointer at `0x43C68`, 16 bytes per species for local 120+8 setup. | TM compatibility randomizer writes final compatibility table, not ItemRandomizer. | No direct item-pool effect except required-TM field caveat. | Compatibility correctness does not prove item placement safety. |

## 6. Trace Per GUI Option

| GUI Option | Settings Field | Randomizer Method | Pool Used | Writer Method | Caveat |
| --- | --- | --- | --- | --- | --- |
| Field Items: Shuffle | `fieldItemsMod == SHUFFLE` | `ItemRandomizer.randomizeFieldItems()` | Existing field items split into TM and non-TM stacks | `Gen3RomHandler.setFieldItems()` | Preserves slot TM class; no bad/mechanic filtering because no new pool is built. |
| Field Items: Random | `fieldItemsMod == RANDOM` | `randomizeTMFieldItems()`, `randomizeNonTMFieldItems()` | TM slots: required/filler TMs; non-TM slots: allowed/non-bad item pool | `setFieldItems()` | Required TM forcing is separate from normal item pool. |
| Field Items: Random Even | `fieldItemsMod == RANDOM_EVEN` | Same as Random, even-distribution branch | Same as Random | `setFieldItems()` | Evenness applies to non-TM filler cycling, not to TM slots. |
| Field Items: Ban Bad Items | `banBadRandomFieldItems` | `randomizeNonTMFieldItems()` | `getNonBadItems()` instead of `getAllowedItems()` | `setFieldItems()` | Does not affect TM-slot required/filler path. |
| Shop Items: Shuffle | `shopItemsMod == SHUFFLE` | `shuffleShopItems()` | Existing supported/special shop items | `Gen3RomHandler.setShops()` | Skipped shops are not touched; existing TMs/mechanic items can remain if already in supported shop content. |
| Shop Items: Random | `shopItemsMod == RANDOM` | `randomizeShopItems()` | `setupPossible()` plus `setupGuaranteed()` | `setShops()` | Only supported/special shops are randomized. |
| Shop Items: Ban Bad Items | `banBadRandomShopItems` | `setupPossible()` | `getNonBadItems()` instead of `getAllowedItems()` | `setShops()` | Guaranteed items are not bad-filtered directly, but are mechanic-filtered. |
| Shop Items: Ban Regular Shop Items | `banRegularShopItems` | `setupPossible()` | Removes `romHandler.getRegularShopItems()` | `setShops()` | Applies only to random filler pool. |
| Shop Items: Ban Overpowered Shop Items | `banOPShopItems` | `setupPossible()` | Removes `romHandler.getOPShopItems()` | `setShops()` | Static OP list, not CFRU economy-aware. |
| Shop Items: Guarantee Evolution Items | `guaranteeEvolutionItems` | `setupGuaranteed()` | Adds `romHandler.getEvolutionItems()` | `setShops()` | Gen3 static evolution item set; not a full Gen9 evolution-item audit. |
| Shop Items: Guarantee X Items | `guaranteeXItems` | `setupGuaranteed()` | Adds `romHandler.getXItems()` | `setShops()` | Places into supported/special shops only. |
| Pickup Items: Random | `pickupItemsMod == RANDOM` | `randomizePickupItems()` | Allowed/non-bad item pool after mechanic filter; conditional TM removal | `Gen3RomHandler.setPickupItems()` | Probability slots are preserved; source table locator must be unique. |
| Pickup Items: Ban Bad Items | `banBadRandomPickupItems` | `randomizePickupItems()` | `getNonBadItems()` instead of `getAllowedItems()` | `setPickupItems()` | TMs can still be possible if holdable and not reusable. |
| Trainer Held Items | Any of `randomizeHeldItemsForBoss/Important/RegularTrainerPokemon` | `TrainerPokemonRandomizer.randomizeTrainerHeldItems()` | `getAllHeldItems()` or `getAllConsumableHeldItems()` after mechanic filter | Trainer save path through trainer party writer | Not controlled by Field/Shop/Pickup Ban Bad toggles. |
| Sensible Items | `sensibleItemsOnlyForTrainers` | `randomizeHeldItem()` -> `getSensibleHeldItemsFor(...)` | Sensible candidates; fallback to all/consumable held items if empty | Trainer save path | NPE class fixed; distribution is not fully audited. |

## 7. Preliminary Policy Assessment

### normalItemPool vs tmHmItemPool

There is a clean practical split for Field and Shop:

- Field randomization separates TM slots from non-TM slots before randomizing.
- Field non-TM items remove `Item::isTM`.
- Shop randomization removes `Item::isTM` from the filler pool.
- HMs are disallowed globally through Gen3 banned items.

Pickup is intentionally different:

- Pickup starts from the same allowed/non-bad item source as Field/Shop.
- It removes TMs only when the handler says TMs cannot be held or are reusable.
- Therefore a future configuration with holdable, non-reusable TMs can place TMs into Pickup.

Trainer held items are a third model:

- They use fixed held-item sets and sensible-item logic, not normal field/shop item pools.

### Can normal item spots get TMs/HMs?

- Field non-TM spots: no, by slot preservation and `removeIf(Item::isTM)`.
- Field TM spots: yes, but only because they are TM slots.
- Shop random filler: no, because TMs are removed.
- Shop shuffle: existing special-shop TMs could move among supported shop slots if present.
- Pickup: yes only if TMs are holdable and not reusable; otherwise no.
- HMs: no normal pool evidence; Gen3 constants ban HM01-HM08.

Policy recommendation: mark Pickup TM eligibility as `NEEDS_POLICY_DECISION`. It is test-covered as
current behavior, but the desired CFRU/DPE profile policy should be explicit.

### Is `Ban Bad Items` sufficient?

No. It is sufficient for the static bad-item flag, but not for all policy categories. It does not
cover every balance-sensitive item, all form-change items, all item-type behavior, or every
script/gift/NPC source. Mechanic filtering covers Mega/Z/Dynamax-GMax by default, but Plates,
Drives, Memories and Nectars/Form-change items are only classified.

Useful future policy categories, without changing code in this PR:

- `normal item pool`
- `tm/hm item pool`
- `pickup eligible`
- `shop eligible`
- `trainer held eligible`
- `progression / field-move required`
- `mechanic key item`
- `form-change item`
- `battle-only held item`
- `sell/economy sensitive`
- `engine-table-sensitive`, for items whose behavior depends on `gFlingTable`, `gItemsByType` or
  custom use effects

## 8. Recommendations

| Area | Recommendation | Reason |
| --- | --- | --- |
| Field Items | `KEEP_WITH_CAVEATS` | TM/non-TM split is clear; required-TM forcing and ingame smoke remain caveats. |
| Shop Items | `KEEP_WITH_CAVEATS` | Random filler pool removes TMs and supports bans/guarantees; only supported/special shops are touched. |
| Pickup Items | `NEEDS_POLICY_DECISION` | Current behavior can include TMs when holdable and not reusable; local profile likely removes them, but policy should be explicit. |
| Ban Bad Items | `NEEDS_POLICY_DECISION` | Static bad filter is coarse and not equivalent to a full CFRU/DPE item policy. |
| Mechanic Items: Mega/Z/Dynamax-GMax | `KEEP_WITH_CAVEATS` | Source-backed active filters exist and are tested. |
| Plates/Drives/Memories/Nectars | `NEEDS_POLICY_DECISION` | Categorized but not actively filtered. |
| CFRU Pickup Table Pointer | `NEEDS_SOURCE_POINTER_VERIFICATION` | FVX has locator and metadata fallback; final local build was not inspected. |
| `gFlingTable`, `gItemsByType`, custom use effects | `OUT_OF_SCOPE` for this PR | FVX does not directly write these tables in item randomization. |
| Trainer Held Items / Sensible Items | `KEEP_WITH_CAVEATS` | NPE/path fixes exist; no full distribution audit. |
| Static Script/Gift/NPC Item Sources | `NEEDS_SOURCE_POINTER_VERIFICATION` | Not traced as part of normal ItemRandomizer pools. |

## Evidence Read

- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/ItemRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/Randomizer.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractRomHandler.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Item.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/services/ItemMechanicPredicates.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/services/CfruDpeItemCategories.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/services/ItemMechanicExclusionOptions.java`
- `02_external/upr-fvx/random/src/test/java/com/uprfvx/random/randomizers/ItemDecisionTest.java`
- `02_external/upr-fvx/random/src/test/java/com/uprfvx/random/randomizers/ItemRandomizerTest.java`
- `02_external/upr-fvx/romio/src/test/java/com/uprfvx/romio/services/ItemMechanicPredicatesTest.java`
- `02_external/upr-fvx/romio/src/test/java/com/uprfvx/romio/romhandlers/RomHandlerFieldItemTest.java`
- `02_external/upr-fvx/romio/src/test/java/com/uprfvx/romio/romhandlers/RomHandlerPickupItemTest.java`
- `02_external/CFRU-expansion/include/constants/items.h`
- `02_external/CFRU-expansion/src/Tables/item_tables.c`
- `02_external/CFRU-expansion/src/item.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/TM_Tutor_Tables.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/tm_compatibility/`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/tutor_compatibility/`
- `01_docs/randomizer/fvx-compat-implementation-report.md`
- `01_docs/randomizer/fvx-feature-decision-matrix.md`
- `01_docs/randomizer/cfru-doc-alignment-code-quality-review.md`
- `08_tests/randomizer/fvx_feature_test_status_matrix.tsv`

## Open Risks / Assumptions

- No final ROM pointer or symbol table was inspected; source-to-final-ROM identity remains caveated.
- No build was run, so CFRU/DPE compile-time item table generation was not revalidated.
- No ingame item behavior was tested.
- Static script/gift/NPC item sources remain outside the traced normal ItemRandomizer pool.
- Expanded CFRU/DPE TM item IDs and FVX's static TM flag range should be verified before relying on
  expanded TM placement semantics.
- Plates, Drives, Memories and Nectars/Form-change items need an explicit policy decision if they
  should be excluded from normal item pools.
