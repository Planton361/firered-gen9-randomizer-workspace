# CFRU/DPE + UPR-FVX Item Pool Categorization Audit

Stand: 2026-05-21

Scope: documentation-only audit for item-pool categorization and future policy decisions. No ROMs
were read, copied, generated or tested. No builds were run. No UPR-FVX, CFRU or DPE code was
changed. No table values were changed.

External references to review later, without downloading into this repository:

- PokeAPI item endpoints: item, item-category, item-pocket, item-attribute.
- Pokemon Showdown `data/items.ts`.
- Bulbapedia item pages as manual cross-check only.

## 1. Executive Summary

The goal of item categorization is to make Item Randomization predictable across CFRU/DPE and
UPR-FVX pools. "Allowed", "bad", "TM", "mechanic item" and "held item" are separate dimensions.
A future policy should say which categories are eligible for Field, Shop, Pickup and Trainer Held
Item pools, instead of relying on one coarse flag.

`Ban Bad Items` is not enough today because it only switches Field, Shop and Pickup from
`getAllowedItems()` to `getNonBadItems()`. That removes items marked `Item.isBad`, but it does not
encode all balance, progression, mechanic, form-change or engine-table risks. Mega/Z/Dynamax-GMax
items already have separate include settings, while Plates, Drives, Memories and Nectars are
recognized but not actively blocked by a user-facing policy.

Three problem classes should stay separate:

- Technically bad: placeholders, invalid names, key/progression items, HMs or engine/system items
  that should not enter generic random pools.
- Player low-value: mail, contest-only/deco-only items, weak berries or exchange-only items that
  are valid data but poor rewards.
- Mechanic-dependent: Mega Stones, Z-Crystals, Dynamax/GMax items and form-change items whose value
  depends on enabled battle mechanics and species/form support.

TM51+ classification was handled as a separate fix scope. This audit assumes expanded TMs should be
treated as `tm_item` policy-wise, but does not implement or verify code behavior.

## 2. Current FVX Item Categories

Hard facts from UPR-FVX:

- `Item.isAllowed`: boolean on `Item`; `AbstractRomHandler.getAllowedItems()` returns loaded items
  where this is true. `Gen3RomHandler.loadItems()` clears it for Gen3 banned items, HMs, CFRU/DPE
  fallback names and CFRU/DPE encounter-held banned rows.
- `Item.isBad`: boolean on `Item`; `AbstractRomHandler.getNonBadItems()` filters allowed items by
  `!isBad`. Gen3 bad lists include mail, many low-value berries, Pokemon-specific held items,
  contest scarves, and FRLG shoal/shard rows.
- `Item.isTM`: boolean on `Item`; Field/Shop/Pickup code uses it to keep TM items out of normal
  item pools. The current local UPR-FVX code also has a CFRU/DPE source-backed helper for expanded
  TM51-TM120 classification.
- `CfruDpeItemCategories`: source-backed classifier for Mega, Z, Dynamax/GMax, Plates, Drives,
  Memories and Nectar/Form-change items. It pairs CFRU/DPE source ranges with item names where
  expanded source IDs enter FVX's unique-offset namespace.
- `ItemMechanicPredicates`: active filter layer. By default it excludes Mega Stones/accessories,
  Z-Crystals/accessories and Dynamax/GMax items unless the matching include setting is enabled.
  Plates, Drives, Memories and Nectars are categorized but not filtered today.

Pool differences:

- Field Random: splits current slots into TM and non-TM stacks. Non-TM replacements use
  allowed/non-bad items, mechanic filters and `removeIf(Item::isTM)`.
- Field Shuffle: shuffles existing TM and non-TM stacks separately. It does not build a new item
  policy pool.
- Shop Random: supported/special shop filler uses allowed/non-bad items, mechanic filters, removes
  TMs, and optionally removes regular-shop or overpowered-shop lists. Guarantees can add evolution
  items and X items.
- Shop Shuffle: shuffles existing supported/special shop contents only.
- Pickup Random: starts from allowed/non-bad items and mechanic filters. It removes TMs only when
  the handler says TMs cannot be held or TMs are reusable. Gen3 defaults remove TMs, but the policy
  should be explicit.
- Trainer Held Items: separate held-item lists and sensible-item logic. Field/Shop/Pickup `Ban Bad`
  toggles do not control this pool.

## 3. Local CFRU/DPE Item Sources

| Quelle | Enthaelt | Relevanz | direkt von FVX geschrieben? | Risiko |
| --- | --- | --- | --- | --- |
| `include/constants/items.h` | Item constants such as `ITEM_MASTER_BALL`, `ITEM_HM01_CUT`, `ITEM_TM51`, `ITEM_TM120`, modern key/form/mechanic items, berries and held items. | Source identity for CFRU/DPE items; useful for category blocks and source-backed predicates. | No. FVX writes final ROM tables, not this source file. | Source constants can differ from FVX static IDs; unknown IDs use FVX unique-offset mapping. |
| `src/Tables/item_tables.c` | Item data rows, names, pockets, use types, pickup lists, Fling, consumable effects and `gItemsByType`. | Main CFRU item metadata source before build; confirms TM pocket/name patterns and engine-side semantics. | No source write. FVX loads/writes the final ROM `ItemData` and placement tables. | Source table values do not prove final ROM pointers without local build/ROM verification. |
| `gItemsByType` | Engine item type table used by helpers such as healing, status recovery, shard and ability/level modifier checks. | Good future source for richer policy categories. | No traced direct FVX write. | Randomizer pools may expose items whose runtime behavior depends on this table. |
| `gFlingTable` | Fling power/effect table for held items. | Relevant for Trainer Held Item and battle-item policy. | No. | Held-item usefulness and risk can depend on Fling behavior outside FVX policy. |
| `gConsumableItemEffects` | CFRU consumable item effect table. | Relevant for consumable trainer-held and Pickup categorization. | No. | FVX sensible-item logic does not fully model every CFRU consumable effect. |
| `sPickupCommonItems` | CFRU common Pickup source list and probability rows. | Source context for the final Pickup table. | FVX writes final ROM Pickup entries through `setPickupItems()`, not source. | Pointer/locator must be verified against the final ROM for stronger claims. |
| `sPickupRareItems` | CFRU rare Pickup source list. | Same as common Pickup. | Same as above. | Same as above. |
| TM/HM item definitions | TM01-TM120 and HM01-HM08 item constants; TM entries use TM Case pocket and mystery bytes. | Distinguishes item placement from TM move/compatibility tables. | FVX ItemRandomizer does not write source definitions. | Item identity, TM move list and compatibility are separate compatibility surfaces. |
| DPE `gTMHMMoves` context | Final TM/HM move list source in DPE/CFRU setup. | Determines what a TM teaches, not whether the item should enter a generic item pool. | Written by TM/HM move randomizer, not ItemRandomizer. | TM item policy must not be confused with TM move/compatibility support. |

## 4. Proposed Item Taxonomy

| Kategorie | Definition | Examples / source hints |
| --- | --- | --- |
| `invalid_placeholder` | Empty, unused, fallback, "????" or do-not-use rows. | CFRU fallback names, unused Gen3 unique items. |
| `key_progression` | Key items, story items, rods, bike, parcels, flutes, tickets, required script items. | `ITEM_BICYCLE`, `ITEM_OLD_ROD`, key item pocket rows. |
| `hm_field_move` | HMs and field-move progression machines. | `ITEM_HM01_CUT` through HM08. |
| `tm_item` | TM items, including expanded CFRU/DPE TM51-TM120. | `ITEM_TM51`, TM Case pocket. |
| `mechanic_mega` | Mega Stones and Mega accessories. | `CfruDpeItemCategories` Mega categories. |
| `mechanic_z` | Z-Crystals and Z accessories. | Z-Crystal/Z accessory categories. |
| `mechanic_dynamax_gmax` | Dynamax/GMax system items and related consumables. | Dynamax Band, Wishing Piece, Max Mushrooms. |
| `form_change_plate` | Arceus Plates. | Plate names/categories. |
| `form_change_drive` | Genesect Drives. | Drive names/categories. |
| `form_change_memory` | Silvally Memories. | Memory names/categories. |
| `form_change_nectar` | Nectars and broader form-change items. | Nectars, Gracidea, DNA Splicers, Reveal Glass. |
| `mail` | Mail items. | Gen3 bad item range `mail1..mail12`. |
| `contest_deco_low_value` | Contest scarves, deco-only or contest-only rewards. | Contest scarves, decorations if present. |
| `berry_useful` | Berries with direct battle/status/HP/PP utility. | Oran, Chesto, Lum, Sitrus, Leppa. |
| `berry_low_value` | Berries with weak, flavor, contest or low-impact use in this hack context. | Many Gen3 flavor/contest berries. |
| `medicine_healing` | HP/revive restoration. | Potion, Full Restore, Revive. |
| `status_healing` | Status recovery. | Antidote, Full Heal, Chesto Berry when modeled as berry. |
| `poke_ball` | Capture balls. | Poke Ball, Great Ball, Master Ball. |
| `battle_item_consumable` | X items, Dire Hit and temporary battle boosters. | X Attack, Dire Hit. |
| `held_battle_item` | Non-consumable or strategic held items. | Leftovers, Choice Band, Quick Claw. |
| `evolution_item` | Evolution stones/items. | Fire Stone, Sun Stone, King's Rock where used. |
| `fossil` | Fossil revival items. | Dome Fossil, Helix Fossil. |
| `money_sell_item` | Valuable sell-only or economy-sensitive items. | Nugget, Big Nugget, Pearl. |
| `rare_candy_vitamin` | Level/stat modifier items. | Rare Candy, PP Up, vitamins, Bottle Cap. |
| `shard_exchange_item` | Exchange/currency fragments. | Blue Shard, other shards. |
| `ordinary_utility` | Valid utility items that are not progression-critical. | Escape Rope, Repel, Heart Scale if non-critical. |
| `unknown_needs_review` | Valid-looking rows without confident category. | Future/custom CFRU rows, unreviewed modern items. |

## 5. Pool Policy Table

Values: `ALLOW`, `BAN`, `OPTIONAL`, `MECHANIC_SETTING`, `REVIEW`.

| Kategorie | Field Pool | Shop Pool | Pickup Pool | Trainer Held Pool | Ban Bad Default | Overpowered Optional | Grund |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `invalid_placeholder` | BAN | BAN | BAN | BAN | BAN | BAN | Not useful and can be unsafe. |
| `key_progression` | BAN | BAN | BAN | BAN | BAN | BAN | Can break progression or script assumptions. |
| `hm_field_move` | BAN | BAN | BAN | BAN | BAN | BAN | Field progression and HM behavior should stay controlled. |
| `tm_item` | BAN | BAN | BAN | BAN | REVIEW | OPTIONAL | Normal pools should not contain TMs; TM slots and TM systems are separate. |
| `mechanic_mega` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | REVIEW | OPTIONAL | Existing include setting should govern this. |
| `mechanic_z` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | REVIEW | OPTIONAL | Existing include setting should govern this. |
| `mechanic_dynamax_gmax` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | REVIEW | OPTIONAL | Existing include setting should govern this. |
| `form_change_plate` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | OPTIONAL | Recognized but no current user policy. |
| `form_change_drive` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | OPTIONAL | Species/form dependent. |
| `form_change_memory` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | OPTIONAL | Species/form dependent. |
| `form_change_nectar` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | OPTIONAL | Can be harmless or mechanic-critical depending form support. |
| `mail` | BAN | BAN | BAN | BAN | BAN | BAN | Low-value and already bad in Gen3 constants. |
| `contest_deco_low_value` | BAN | BAN | BAN | BAN | BAN | BAN | Valid data but poor reward in this scope. |
| `berry_useful` | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | Useful and low risk. |
| `berry_low_value` | OPTIONAL | OPTIONAL | OPTIONAL | REVIEW | BAN | BAN | Valid but weak or context-dependent. |
| `medicine_healing` | ALLOW | ALLOW | ALLOW | BAN | ALLOW | OPTIONAL | Good player rewards; not generally trainer held items. |
| `status_healing` | ALLOW | ALLOW | ALLOW | OPTIONAL | ALLOW | ALLOW | Generally safe; some berries overlap held policy. |
| `poke_ball` | ALLOW | ALLOW | ALLOW | BAN | ALLOW | OPTIONAL | Useful player rewards; Master Ball needs OP handling. |
| `battle_item_consumable` | ALLOW | ALLOW | ALLOW | OPTIONAL | ALLOW | OPTIONAL | Useful but can affect difficulty/economy. |
| `held_battle_item` | ALLOW | OPTIONAL | OPTIONAL | ALLOW | ALLOW | OPTIONAL | Strong items should be trainer-held aware. |
| `evolution_item` | ALLOW | ALLOW | OPTIONAL | BAN | ALLOW | OPTIONAL | Usually useful; shops may guarantee them. |
| `fossil` | OPTIONAL | OPTIONAL | REVIEW | BAN | REVIEW | OPTIONAL | Useful only if revival/source support exists. |
| `money_sell_item` | ALLOW | OPTIONAL | OPTIONAL | BAN | ALLOW | OPTIONAL | Reward value, not invalid; OP shop toggle should control economy. |
| `rare_candy_vitamin` | ALLOW | OPTIONAL | OPTIONAL | BAN | ALLOW | OPTIONAL | Powerful but not bad; should be OP/economy policy. |
| `shard_exchange_item` | OPTIONAL | OPTIONAL | OPTIONAL | BAN | BAN | BAN | FRLG marks shards bad because they may do nothing. |
| `ordinary_utility` | ALLOW | ALLOW | ALLOW | BAN | ALLOW | ALLOW | Safe utility reward. |
| `unknown_needs_review` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | Do not silently classify future/custom items. |

## 6. First Concrete Policy Recommendation

Recommended conservative policy:

- Normal Field, Shop and Pickup pools should contain no TMs/HMs. TM Field slots and TM/HM move
  randomization remain separate.
- Pickup TMs should stay banned unless a future explicit toggle allows them.
- Key, progression, script and system items should be banned by default.
- Mail and contest/deco-only items should be treated as default bad.
- Mega, Z and Dynamax/GMax items should continue to follow existing include settings.
- Plates, Drives, Memories and Nectars/Form-change items should be `REVIEW` by default until a
  project policy decides whether to ban or setting-gate them.
- Rare Candy, Master Ball, Nuggets, Big Nuggets, vitamins and similar strong/economy items should
  be overpowered/economy optional, not automatically "bad".
- Evolution items should remain allowed and can be guaranteed in shops where the existing option
  supports that.
- Trainer Held Items need a separate held-item policy. They should not blindly inherit Field/Shop
  reward policy.

## 7. Example Classification

| Item example | Proposed category | Field | Shop | Pickup | Trainer Held | Note |
| --- | --- | --- | --- | --- | --- | --- |
| Potion | `medicine_healing` | ALLOW | ALLOW | ALLOW | BAN | Player reward, not a held item. |
| Full Restore | `medicine_healing` | ALLOW | ALLOW | ALLOW | BAN | Strong but valid. |
| Poke Ball | `poke_ball` | ALLOW | ALLOW | ALLOW | BAN | Normal capture reward. |
| Master Ball | `poke_ball` | OPTIONAL | OPTIONAL | OPTIONAL | BAN | Treat as overpowered optional, not bad. |
| Rare Candy | `rare_candy_vitamin` | ALLOW | OPTIONAL | OPTIONAL | BAN | Strong progression item; OP/economy toggle candidate. |
| Nugget | `money_sell_item` | ALLOW | OPTIONAL | OPTIONAL | BAN | Economy-sensitive, not invalid. |
| Escape Rope | `ordinary_utility` | ALLOW | ALLOW | ALLOW | BAN | Safe utility. |
| Bicycle | `key_progression` | BAN | BAN | BAN | BAN | Key/progression item. |
| Old Rod | `key_progression` | BAN | BAN | BAN | BAN | Key/progression item. |
| HM01 | `hm_field_move` | BAN | BAN | BAN | BAN | Field-move progression. |
| TM51 | `tm_item` | BAN | BAN | BAN | BAN | Allowed only in TM-specific paths. |
| Leftovers | `held_battle_item` | ALLOW | OPTIONAL | OPTIONAL | ALLOW | Strong held item; valid trainer-held candidate. |
| Choice Band | `held_battle_item` | ALLOW | OPTIONAL | OPTIONAL | ALLOW | Strong held item. |
| Oran Berry | `berry_useful` | ALLOW | ALLOW | ALLOW | ALLOW | Useful low-risk berry. |
| Chesto Berry | `berry_useful` | ALLOW | ALLOW | ALLOW | ALLOW | Useful status berry. |
| Mail | `mail` | BAN | BAN | BAN | BAN | Default bad/low-value. |
| Blue Shard | `shard_exchange_item` | OPTIONAL | OPTIONAL | OPTIONAL | BAN | FRLG bad list treats shards as doing nothing. |
| Fossil | `fossil` | OPTIONAL | OPTIONAL | REVIEW | BAN | Needs revival/source support confidence. |
| Fire Stone | `evolution_item` | ALLOW | ALLOW | OPTIONAL | BAN | Useful and shop guarantee candidate. |
| Mega Stone | `mechanic_mega` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | Existing include setting should control. |
| Z-Crystal | `mechanic_z` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | Existing include setting should control. |
| Dynamax Band | `mechanic_dynamax_gmax` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | System/mechanic item. |
| Plate | `form_change_plate` | REVIEW | REVIEW | REVIEW | REVIEW | Categorized, no active policy today. |
| Drive | `form_change_drive` | REVIEW | REVIEW | REVIEW | REVIEW | Genesect-specific. |
| Memory | `form_change_memory` | REVIEW | REVIEW | REVIEW | REVIEW | Silvally-specific. |
| Nectar | `form_change_nectar` | REVIEW | REVIEW | REVIEW | REVIEW | Form-change dependent. |
| Gracidea | `form_change_nectar` | REVIEW | REVIEW | REVIEW | REVIEW | Form-change dependent even if not a nectar. |
| DNA Splicers | `form_change_nectar` | REVIEW | REVIEW | REVIEW | REVIEW | Form-change/system item. |
| Placeholder / ???? item | `invalid_placeholder` | BAN | BAN | BAN | BAN | Unsafe or useless. |
| Key item example | `key_progression` | BAN | BAN | BAN | BAN | Script/progression risk. |

## 8. Later Code Impact

No implementation is proposed in this PR. If the taxonomy is accepted, later code could change:

- `Gen3RomHandler.loadItems()`: annotate loaded items with richer source-backed categories after
  reading final `ItemData`.
- `CfruDpeItemCategories`: add passive categories for more CFRU/DPE source blocks, keeping
  source-range plus name checks for unique-offset IDs.
- `ItemMechanicPredicates` or a new `ItemPoolPolicy` helper: separate active randomizer pool policy
  from mechanic-only predicates.
- `ItemRandomizer`: replace ad hoc `isAllowed`/`isBad`/`isTM` filtering with pool-specific policy
  decisions for Field, Shop and Pickup.
- `TrainerPokemonRandomizer`: use a held-item-specific policy instead of generic reward-item policy.
- Settings/GUI/profile generation: possible toggles include "Allow Pickup TMs", "Allow Form-Change
  Items", "Ban Low-Value Items", "Ban Economy Items" and "Held Item Policy".

Tests to add later:

- ROM-free taxonomy classifier tests for representative CFRU/DPE source IDs and item names.
- Field/Shop/Pickup pool policy tests for every category.
- Trainer-held policy tests for held-only, consumable-only and sensible-item modes.
- Regression tests ensuring TM/HM items remain excluded from normal pools and TM slots still use
  TM-specific pools.
- Optional generated TSV/audit test that flags unknown items as `unknown_needs_review` instead of
  silently allowing them.

## 9. Next Minimal Action

Next step: review this taxonomy as a project policy document before any code change. The review
should decide only whether each proposed category and pool action is correct. After that, a separate
documentation-only or tooling-only task can generate a local item-category TSV from CFRU/DPE source
metadata for manual review.
