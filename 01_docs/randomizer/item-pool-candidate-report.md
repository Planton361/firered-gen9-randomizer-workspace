# UPR-FVX CFRU/DPE Item Pool Candidate Report

Status: documentation-only analysis from current UPR-FVX code and local CFRU/DPE source context. No ROMs were read, copied, built, or tested.

## 1. Executive Summary

This report covers the item candidate pools that can feed normal Field, Shop, and Pickup randomization after the current CFRU/DPE item-policy fixes. It also documents adjacent held-item pools so their behavior is not confused with normal item spots.

What can be read from code with high confidence:

- `Gen3RomHandler.loadItems()` loads final ROM `ItemData` through the `romEntry` `ItemData`, `ItemEntrySize`, and `ItemCount` values, then applies FVX allowed/bad/TM flags.
- Normal Field non-TM, Shop random filler, and Pickup random pools are all based on `romHandler.getAllowedItems()` or `romHandler.getNonBadItems()`, then filtered by `ItemMechanicPredicates`, then stripped of `Item::isTM`.
- Field TM slots remain a separate path and can still receive TMs, including expanded CFRU/DPE TM items.
- Fossils are hard-banned from normal item pools. Shards, Relic/high-value valuables, Memories, Apricorns, Plates, Drives, Nectars, and other form-change items are Ban-Bad filtered.
- Mega, Z-Crystal, and Dynamax/GMax items are controlled by their include settings, not by the Ban-Bad toggle alone.

What remains unproven without final ROM `ItemData`:

- The exact complete list of item names loaded by FVX for a specific built ROM.
- Whether every local CFRU source constant maps to the same decoded final ROM name and standard FVX item ID.
- Static script/gift/NPC items that are not routed through Field/Shop/Pickup randomizer APIs.
- Any custom localized name or future item whose final ROM name is not covered by the current name/category predicates.

## 2. Pool Trace

| Pool | Codepath | Source | Ban-Bad Filter | Mechanic Filter | TM/HM Filter | Caveat |
| --- | --- | --- | --- | --- | --- | --- |
| Field non-TM random pool | `ItemRandomizer.randomizeFieldItems()` -> `randomizeNonTMFieldItems()` | `romHandler.getNonBadItems()` when `banBadRandomFieldItems`; otherwise `getAllowedItems()` | Yes when option is enabled | Yes via `filterAllowedMechanicItems()` | Removes `Item::isTM`; HMs are blocked earlier by `Gen3Constants.bannedItems` | Only applies to Field Item API slots; script/gift/NPC rewards are out of scope. |
| Field TM slots | `randomizeFieldItems()` -> `randomizeTMFieldItems()` | Current TM field slots plus `romHandler.getItems()` TM candidates | Not the normal non-TM Ban-Bad path | No normal item-pool mechanic policy | Requires `Item::isTM`; preserves TM-slot semantics | TMs appearing here are expected if the original slot was a TM slot. |
| Shop random filler | `ItemRandomizer.randomizeShopItems()` -> `setupPossible()` | `getNonBadItems()` when `banBadRandomShopItems`; otherwise `getAllowedItems()` | Yes when option is enabled | Yes via `filterAllowedMechanicItemSet()` | Removes `Item::isTM`; HMs are blocked earlier | Optional `Ban Regular Shop Items` and `Ban OP Shop Items` remove extra subsets. Guaranteed items are a separate path. |
| Shop shuffle | `ItemRandomizer.shuffleShopItems()` | Existing special-shop contents | No new candidate pool | No new candidate pool | No new candidate pool | Can preserve/shuffle whatever was already in the shop data. Do not treat as proof that the random filler allowed an item. |
| Pickup random pool | `ItemRandomizer.randomizePickupItems()` | `getNonBadItems()` when `banBadRandomPickupItems`; otherwise `getAllowedItems()` | Yes when option is enabled | Yes via `filterAllowedMechanicItems()` | Removes `Item::isTM`; HMs are blocked earlier | Replaces pickup table rows loaded through the FVX pickup API, not arbitrary script items. |
| Trainer held items | `TrainerPokemonRandomizer.randomizeTrainerHeldItems()` | `getAllHeldItems()` or `getSensibleHeldItemsFor()` with fallback | Trainer held settings, not Field/Shop/Pickup Ban-Bad | Yes in current tests and randomizer path | Separate held-item logic | Policy intentionally allows many held battle items that would be odd as overworld rewards. |
| Encounter held items | `EncounterHeldItemRandomizer.randomizeWildHeldItems()` | `getNonBadItems()` or `getAllowedItems()` based on wild held Ban-Bad | Yes when wild held Ban-Bad is enabled | Yes | Removes null/fallback names, TMs, and Poke Balls | Separate from Field/Shop/Pickup; Poke Balls are allowed in normal pools but blocked here. |
| Static Script/Gift/NPC item sources | Out of scope for this pool report | Scripts, events, NPC/gift logic | Unknown | Unknown | Unknown | Needs separate source/script trace. A leaked item here may not imply a Field/Shop/Pickup pool bug. |

## 3. Candidate Categories Still Allowed

These categories can still appear in normal Field/Shop/Pickup pools when the item is present in final ROM `ItemData`, `Item.isAllowed()` is true, Ban-Bad is on, and no optional shop-only filter removes it.

| Category | Field | Shop | Pickup | Trainer Held | Warum erlaubt | Risiko |
| --- | --- | --- | --- | --- | --- | --- |
| Healing/status items | ALLOW | ALLOW | ALLOW | Usually possible if held pool includes them | No CFRU/DPE policy predicate bans `Potion`, `Super Potion`, `Full Restore`, `Antidote`, etc. Local CFRU `gItemsByType` marks them as healing/status types. | Exact item list depends on final `ItemData` and legacy `badItems`. |
| Ordinary utility | ALLOW | ALLOW | ALLOW | Usually possible if held pool includes them | `Escape Rope`, `Repel`, and similar utility items are not newly banned. | Some key/progression-looking utility items may be blocked by `Gen3Constants.bannedItems`; verify final item identity before treating as leak. |
| Balls including Master Ball | ALLOW | ALLOW | ALLOW | Encounter-held blocks Poke Balls; trainer held is separate | `CfruDpeItemPoolPolicy.isPokeBallItem()` deliberately keeps balls reward-eligible and exempts them from the CFRU encounter-held hard ban during load. | `Ban OP Shop Items` removes vanilla ball range from shop filler if enabled through `Gen3Constants.opShopItems`; Field/Pickup do not use that shop-only option. |
| Rare Candy / PP Up / Vitamins | ALLOW | ALLOW, unless optional OP-shop filter removes specific items | ALLOW | Usually possible if held pool includes them | Anton policy keeps `rare_candy_vitamin` allowed. Tests explicitly keep `Rare Candy`, `PP Up`, and `HP Up` unbanned by the new policy. | `Rare Candy` is in `Gen3Constants.opShopItems`, so Shop with `Ban OP Shop Items` can remove it. |
| X Items / battle consumables | ALLOW | ALLOW | ALLOW | Usually possible if held pool includes them | `X Defend` is explicitly covered as allowed by policy tests; shops can also guarantee X items through a separate guaranteed path. | Guaranteed shop path is mechanic-filtered but not the same as random filler Ban-Bad filtering. |
| Held battle items, including Eviolite/Gems | ALLOW | ALLOW | ALLOW | ALLOW | Tests keep `Leftovers`, `Eviolite`, and `Fire Gem` allowed; local CFRU `gItemsByType` classifies these as held/gem categories, not mechanic exclusions. | Design caveat: these may be legal rewards but still balance-heavy. |
| Evolution items | ALLOW | ALLOW | ALLOW | Possible if held pool includes them | Local CFRU `gItemsByType` marks stones and modern evolution items as `ITEM_TYPE_EVOLUTION_STONE` or `ITEM_TYPE_EVOLUTION_ITEM`; current policy does not ban them. | Shop guarantee evolution option can inject them separately. |
| Lower-value sell/utility items | ALLOW for non-high-value subset | ALLOW, unless optional OP-shop filter removes vanilla money items | ALLOW | Usually possible if held pool includes them | Policy bans high-value/relic valuables but leaves normal money-ish items such as `Nugget` allowed; test coverage explicitly keeps `Nugget` allowed. | `Gen3Constants.opShopItems` can remove `Tiny Mushroom` through `Nugget` from shop filler when `Ban OP Shop Items` is enabled. Other sellables need final ROM review. |
| Useful berries | ALLOW | ALLOW | ALLOW | ALLOW when held pool includes them | `isAllowedWhenBanBadItems()` clears legacy bad flags for useful berries such as Oran and Lum. | Low-value berries may remain legacy bad; see unknown row. |
| Unknown/custom items | REVIEW | REVIEW | REVIEW | REVIEW | Unknown items are not automatically added to new allow or ban categories. If final `ItemData` loads them as allowed and non-bad, and no predicate matches, they can pass. | This is the largest remaining category-leak risk for custom/localized/future items. Fallback names like `item #...` are usually marked disallowed/bad during load. |

## 4. Candidate Categories Now Blocked

| Category | Block reason | Codepath / Predicate | Tests |
| --- | --- | --- | --- |
| TMs/HMs from normal pools | Normal Field/Shop/Pickup remove `Item::isTM`; HMs are in `Gen3Constants.bannedItems`. | `ItemRandomizer.randomizeNonTMFieldItems()`, `setupPossible()`, `randomizePickupItems()`; `Gen3RomHandler.loadItems()` marks vanilla and CFRU/DPE expanded TMs. | `ItemDecisionTest.nonTmFieldItemPoolExcludesExpandedCfruDpeTechnicalMachines`, `shopRandomFillerExcludesExpandedCfruDpeTechnicalMachines`, `pickupPoolExcludesExpandedCfruDpeTechnicalMachinesByDefault`. |
| Mega when Include Mega Items OFF | Mechanic setting excludes Mega stones/accessories. | `ItemMechanicPredicates.isItemAllowed()` and `CfruDpeItemCategories.isMegaMechanicItem()`. | `ItemMechanicPredicatesTest.megaStonesAndAccessoriesAreMegaMechanicItems`; `ItemDecisionTest.mechanicItemsAreExcludedFromFieldShopPickupAndHeldPoolsByDefault`. |
| Z-Crystals when Include Z-Crystal Items OFF | Mechanic setting excludes Z items. | `ItemMechanicPredicates.isItemAllowed()` and `CfruDpeItemCategories.isZMechanicItem()`. | `ItemMechanicPredicatesTest.zCrystalsAndAccessoriesAreZMechanicItems`, `signatureZCrystalNamesAreRecognizedWhenIdsAreNotCanonical`. |
| Dynamax/GMax when Include Dynamax/GMax OFF | Mechanic setting excludes Dynamax/GMax items. | `ItemMechanicPredicates.isItemAllowed()` and explicit `ItemMechanicCategory.DYNAMAX_GIGANTAMAX`. | `ItemMechanicPredicatesTest.dynamaxAndGigantamaxItemsUseTheirOwnMechanicCategory`. |
| Fossils | Hard-banned from normal item pools by setting allowed false and bad true during load. | `Gen3RomHandler.applyCfruDpeItemPoolPolicy()` -> `CfruDpeItemPoolPolicy.isBannedFromNormalItemPools()`. | `CfruDpeItemPoolPolicyTest.fossilsAreBannedFromNormalItemPools`. |
| Shards/exchange junk | Ban-Bad marks them bad. | `CfruDpeItemPoolPolicy.isBadWhenBanBadItems()` -> `isShardExchangeItem()`. | `CfruDpeItemPoolPolicyTest.shardsAreBadOnlyWhenBanBadItemsIsEnabled`. |
| Relic/high-value valuables | Ban-Bad marks them bad. | `isHighValueValuableItem()`. | `CfruDpeItemPoolPolicyTest.highValueValuablesAreBadOnlyWhenBanBadItemsIsEnabled`. |
| Memories | Ban-Bad marks form-change items bad. | `isFormChangeItem()` -> `CfruDpeItemCategories.isSilvallyMemory()`. | `CfruDpeItemPoolPolicyTest.formChangeItemsAreBadOnlyWhenBanBadItemsIsEnabled`; `ItemMechanicPredicatesTest.passiveSourceBackedCategoriesAreClassifiedWithoutChangingMechanicFilters`. |
| Apricorns | Ban-Bad marks Apricorn/Aprikoko variants bad. | `isApricornItem()`. | `CfruDpeItemPoolPolicyTest.apricornsAreBadOnlyWhenBanBadItemsIsEnabled`. |
| Plates/Drives/Nectars/form-change items | Ban-Bad marks form-change categories bad. | `isFormChangeItem()` -> Arceus Plate, Genesect Drive, Nectar/form-change predicates. | `CfruDpeItemPoolPolicyTest.formChangeItemsAreBadOnlyWhenBanBadItemsIsEnabled`. |
| Invalid/placeholders/key/progression | Partially blocked through legacy banned items, fallback handling, and CFRU encounter-held banned set. | `Gen3Constants.bannedItems`; `Gen3RomHandler.readItemNameOrFallback()` and fallback bad marking. | No complete source-to-ROM proof for every custom key/progression item in this report. |

## 5. Concrete Local Item Name Audit

This is a reviewable sample from local CFRU item constants/tables plus current FVX predicates. It is not an exhaustive final ROM candidate dump.

| Item constant/name | Category guess | Field BanBad ON | Shop BanBad ON | Pickup BanBad ON | Reason | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| `ITEM_POTION` / Potion | healing | ALLOW | ALLOW | ALLOW | Policy tests keep Potion allowed; local `gItemsByType` marks potion type. | High |
| `ITEM_SUPER_POTION` / Super Potion | healing | ALLOW | ALLOW | ALLOW | Explicit allowed policy test. | High |
| `ITEM_FULL_RESTORE` / Full Restore | healing/status | ALLOW | ALLOW | ALLOW | Explicit allowed policy test. | High |
| `ITEM_ANTIDOTE` / Antidote | status healing | ALLOW | ALLOW | ALLOW | Explicit allowed policy test. | High |
| `ITEM_ESCAPE_ROPE` / Escape Rope | ordinary utility | ALLOW | ALLOW | ALLOW | Explicit allowed policy test; not a key/progression item in current FVX policy. | High |
| `ITEM_REPEL` / Repel | ordinary utility | ALLOW | ALLOW | ALLOW | Local CFRU item type is repel; no current FVX ban predicate. | Medium |
| `ITEM_POKE_BALL` / Poke Ball | Poke Ball | ALLOW | ALLOW | ALLOW | Poke Ball policy predicate treats balls as allowed reward items. | High |
| `ITEM_ULTRA_BALL` / Ultra Ball | Poke Ball | ALLOW | ALLOW | ALLOW | Explicit allowed policy test. | High |
| `ITEM_MASTER_BALL` / Master Ball | Poke Ball / powerful reward | ALLOW | ALLOW unless optional shop OP filter removes ball range | ALLOW | Explicit allowed policy test; `Gen3Constants.opShopItems` can remove ball range only when Shop `Ban OP Shop Items` is enabled. | High |
| `ITEM_RARE_CANDY` / Rare Candy | rare candy/vitamin | ALLOW | ALLOW unless optional shop OP filter removes it | ALLOW | Explicit allowed policy test; also in optional OP shop set. | High |
| `ITEM_PP_UP` / PP Up | rare candy/vitamin | ALLOW | ALLOW | ALLOW | Explicit allowed policy test. | High |
| `ITEM_HP_UP` / HP Up | vitamin | ALLOW | ALLOW | ALLOW | Explicit allowed policy test. | High |
| `ITEM_X_DEFEND` / X Defend | battle item | ALLOW | ALLOW | ALLOW | Explicit allowed policy test. | High |
| `ITEM_LEFTOVERS` / Leftovers | held battle item | ALLOW | ALLOW | ALLOW | Explicit allowed policy test; local type is held item. | High |
| `ITEM_EVIOLITE` / Eviolite | held battle item | ALLOW | ALLOW | ALLOW | Explicit allowed policy test; local type is held item. | High |
| `ITEM_FIRE_GEM` / Fire Gem | gem / held consumable | ALLOW | ALLOW | ALLOW | Explicit allowed policy test; local type is gem. | High |
| `ITEM_FIRE_STONE` / Fire Stone | evolution item | ALLOW | ALLOW | ALLOW | Local type is evolution stone; no current ban predicate. | Medium |
| `ITEM_NUGGET` / Nugget | lower-value sell item | ALLOW | ALLOW unless optional shop OP filter removes money range | ALLOW | Explicit allowed policy test; high-value ban does not include Nugget. | High |
| `ITEM_BIG_NUGGET` / Big Nugget | high-value valuable | BLOCK | BLOCK | BLOCK | `isHighValueValuableItem()` marks bad under Ban-Bad. | High |
| `ITEM_BALM_MUSHROOM` / Balm Mushroom | high-value valuable | BLOCK | BLOCK | BLOCK | High-value valuable predicate. | High |
| `ITEM_PEARL_STRING` / Pearl String | high-value valuable | BLOCK | BLOCK | BLOCK | High-value valuable predicate. | High |
| `ITEM_COMET_SHARD` / Comet Shard | high-value valuable | BLOCK | BLOCK | BLOCK | High-value valuable predicate. | High |
| `ITEM_RARE_BONE` / Rare Bone | high-value valuable | BLOCK | BLOCK | BLOCK | High-value valuable predicate. | High |
| `ITEM_GREEN_SHARD` / Green Shard | shard/exchange junk | BLOCK | BLOCK | BLOCK | Shard predicate marks bad under Ban-Bad. | High |
| `ITEM_FOSSILIZED_FISH` / Fish Fossil | fossil | BLOCK | BLOCK | BLOCK | Fossil predicate hard-bans normal pools. | High |
| `ITEM_FLYING_MEMORY` / Flying Mem. | Silvally Memory | BLOCK | BLOCK | BLOCK | Form-change predicate; name variants covered. | High |
| `ITEM_RED_APRICORN` / Red Apricorn/Aprikoko | Apricorn | BLOCK | BLOCK | BLOCK | Apricorn predicate marks bad under Ban-Bad. | High |
| `ITEM_FLAME_PLATE` / Flame Plate | Plate/form-change | BLOCK | BLOCK | BLOCK | Form-change predicate. | High |
| `ITEM_BURN_DRIVE` / Burn Drive | Drive/form-change | BLOCK | BLOCK | BLOCK | Form-change predicate. | High |
| `ITEM_RED_NECTAR` / Red Nectar | Nectar/form-change | BLOCK | BLOCK | BLOCK | Form-change predicate. | High |
| `ITEM_BLASTOISINITE` / Blastoiseite | Mega stone | BLOCK when Include Mega OFF; ALLOW when ON | Same | Same | Mechanic filter, independent of Ban-Bad. | High |
| `ITEM_ALORAICHIUM_Z` / Alorichium Z | Z-Crystal | BLOCK when Include Z OFF; ALLOW when ON | Same | Same | Mechanic filter; localized/name variants covered by tests. | High |
| `ITEM_NORMALIUM_Z` / Normalium Z | Z-Crystal | BLOCK when Include Z OFF; ALLOW when ON | Same | Same | Mechanic filter. | High |
| `ITEM_DYNAMAX_BAND` / Dynamax Band | Dynamax/GMax | BLOCK when Include Dynamax/GMax OFF; ALLOW when ON | Same | Same | Mechanic filter. | High |
| `ITEM_TM51` / TM51 | TM | BLOCK from normal pools | BLOCK from random filler | BLOCK | `Item.isTM` and expanded TM classification remove it from normal pools. | High |
| `ITEM_HM01_CUT` / HM01 | HM/field move | BLOCK | BLOCK | BLOCK | HMs are in `Gen3Constants.bannedItems`. | High |
| `ITEM_BICYCLE` / Bicycle or similar key item | key/progression | UNKNOWN / likely blocked if in Gen3 unique banned range | UNKNOWN | UNKNOWN | Legacy banned range covers Gen3 unique/key items, but custom final IDs/names require final ROM verification. | Medium |
| Fallback `item #...` | invalid/fallback | BLOCK | BLOCK | BLOCK | `Gen3RomHandler` marks CFRU/DPE fallback item names disallowed and bad. | High |
| Custom future localized item | unknown_needs_review | UNKNOWN | UNKNOWN | UNKNOWN | Unknown items are not silently added to new ban/allow categories. Final `ItemData` decides name/allowed/bad status. | Low |

## 6. Gaps / Possible Remaining Leaks

- Localized or abbreviated names not covered by `CfruDpeItemCategories` or `CfruDpeItemPoolPolicy` can still pass if final `ItemData` loads them as allowed and non-bad.
- Key Item pocket items are not generically classified from CFRU `gItemsByType` by FVX; current blocking relies on legacy banned ranges, fallback handling, and explicit policy predicates.
- Custom story/form items outside known Plate/Drive/Memory/Nectar/form-change names need concrete evidence before adding new bans.
- Low-value exchange/sell items remain partly policy-dependent. High-value valuables and relics are blocked, but ordinary sellables such as Nugget remain allowed by Anton policy.
- Static script/gift/NPC sources remain outside this candidate-pool report. If Anton sees a blocked item from a scripted source, the normal Field/Shop/Pickup pool may still be correct.
- Final item names are only known after loading the built ROM `ItemData`; local CFRU source constants are useful evidence but not a substitute for final source-to-ROM pointer verification.
- Shop shuffle and shop guarantees can explain observations that do not match the random filler pool.

## 7. Next Action

Generate a review-only TSV from local `items.h`, `item_tables.c`, and the current FVX predicates that lists each known local item constant with predicted category, normal-pool outcome, evidence source, and confidence. Keep it documentation/generated-artifact only until Anton reviews new suspicious rows.
