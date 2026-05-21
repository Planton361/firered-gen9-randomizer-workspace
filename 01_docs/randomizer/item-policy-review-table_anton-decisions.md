# Item Policy Review Table

Stand: 2026-05-21

Scope: documentation-only review table for CFRU/DPE + UPR-FVX item-pool policy. No ROMs were read,
copied, generated or tested. No builds were run. No UPR-FVX, CFRU or DPE code was changed. No table
values were changed.

External references to review manually later, without downloading into this repository:

- PokeAPI item endpoint, item-category, item-pocket and item-attribute.
- Pokemon Showdown `data/items.ts`.
- Bulbapedia item pages as manual review source only.

## 1. Executive Summary

Codex is only proposing policy defaults here. Item rewards affect difficulty, economy, progression,
mechanic exposure and player experience, so Anton should make the final decisions before any code
change. This table is meant to turn those decisions into explicit review rows.

Anton needs to decide:

- Which categories should be part of `Ban Bad Items`.
- Which categories belong in normal Field, Shop and Pickup pools.
- Which categories should be gated by existing mechanic settings or new toggles.
- Which categories should be held-item-only or excluded from Trainer Held pools.
- Which review-only categories should be mapped from local CFRU/DPE source before implementation.

Likely clear defaults: invalid/placeholders, key/progression items, HMs, normal TMs, mail and
contest/deco-only items should not enter normal item pools. Healing, status recovery, basic balls
and ordinary utility items are likely safe to allow. Mega/Z/Dynamax-GMax should stay behind existing
mechanic include settings.

Review-needed categories: Plates, Drives, Memories, Nectars, other form-change items, Fossils,
Shards/Mushrooms/exchange items, Rare Candy/Vitamins, Master Ball, money items and battle-only held
items in Field/Shop/Pickup pools.

Anton review decisions were applied on 2026-05-21 based on Anton's item-pool policy preference. The
`Anton Decision` and `Anton Notes` columns now record the desired default behavior for categories and
representative items; implementation remains a later code scope.

## 2. Decision Model

Columns:

- `Item / Category`: category name or representative item.
- `Codex Category`: proposed taxonomy from the item-pool categorization audit.
- `Codex Recommendation`: short default proposal before Anton review.
- `Field Pool`: normal Field Item random pool recommendation.
- `Shop Pool`: randomized supported/special shop filler recommendation.
- `Pickup Pool`: Pickup randomization pool recommendation.
- `Trainer Held Pool`: Trainer Held Item pool recommendation.
- `BanBad Default`: whether `Ban Bad Items` should ban this by default.
- `Optional Toggle`: existing or possible future toggle that should control the category.
- `Risk`: main compatibility, progression, economy or design risk.
- `Reason`: why Codex recommends the row.
- `Anton Decision`: intentionally blank for final decision.
- `Anton Notes`: intentionally blank for review notes.

Hard facts behind the table:

- FVX `Ban Bad Items` currently means `Item.isBad == false`, not a full policy model.
- Field/Shop normal pools remove `Item.isTM`; Pickup removes TMs only when TMs cannot be held or
  are reusable.
- Trainer Held Items use separate held-item lists and sensible-item logic.
- `ItemMechanicPredicates` actively filters Mega/Z/Dynamax-GMax by settings.
- Plates, Drives, Memories and Nectars are classified by `CfruDpeItemCategories` but do not have
  active user-facing pool policy today.

## 3. Policy Values

- `ALLOW`: include by default in that pool.
- `BAN`: exclude by default.
- `OPTIONAL`: allow only if a policy/toggle explicitly includes it.
- `MECHANIC_SETTING`: controlled by Mega/Z/Dynamax-GMax include settings or a future matching setting.
- `HELD_ONLY`: valid only for Trainer Held Item policy, not generic reward pools.
- `REVIEW`: do not implement until Anton decides or source mapping is stronger.
- `OUT_OF_SCOPE`: not a target for current item-pool policy.

## 4. Category Table

| Category | Codex Recommendation | Field | Shop | Pickup | Trainer Held | BanBad Default | Optional Toggle | Risk | Reason | Anton Decision | Anton Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `invalid_placeholder` | BAN | BAN | BAN | BAN | BAN | BAN | none | Invalid item or useless reward | Placeholder/fallback rows can be unsafe or unreadable. | BAN | Anton: ban invalid/placeholder items from all randomizer pools. |
| `key_progression` | BAN | BAN | BAN | BAN | BAN | BAN | none | Progression/script break | Key items, rods, bike and story items should remain controlled. | BAN | Anton: remove key/progression items from normal pools; progression should stay controlled. |
| `hm_field_move` | BAN normal pools | BAN | BAN | BAN | BAN | BAN | none | Field-move progression break | HMs are field progression and already globally banned by Gen3 constants. | BAN | Anton: ban HMs/field-move items from random pools because HMs should be obtained through normal progression. |
| `tm_item` | BAN normal pools, separate TM pool | BAN | BAN | BAN | BAN | REVIEW | future Allow Pickup TMs only if desired | TM availability/compatibility confusion | TM slots and TM/HM move compatibility are separate systems. | BAN | Anton: ban TMs from normal item pools; use a separate TM pool/slot handling. |
| `mechanic_mega` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | REVIEW | Include Mega Items | Mechanic-dependent reward | Existing setting already controls Mega items. | MECHANIC_SETTING | Anton: ban unless the corresponding Mega item option/mechanic is enabled. |
| `mechanic_z` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | REVIEW | Include Z-Crystal Items | Mechanic-dependent reward | Existing setting already controls Z items. | MECHANIC_SETTING | Anton: ban unless the corresponding Z item option/mechanic is enabled. |
| `mechanic_dynamax_gmax` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | REVIEW | Include Dynamax/GMax Items | Mechanic-dependent reward | Existing setting already controls Dynamax/GMax items. | MECHANIC_SETTING | Anton: ban unless the corresponding Dynamax/GMax item option/mechanic is enabled. |
| `form_change_plate` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | future Form-Change Items | Species/form dependency | Categorized but no current active pool policy. | BAN | Anton: treat as Ban Bad Items/default ban because it rarely has useful effect. |
| `form_change_drive` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | future Form-Change Items | Species/form dependency | Genesect-specific value depends on form support. | BAN | Anton: treat as Ban Bad Items/default ban because it rarely has useful effect. |
| `form_change_memory` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | future Form-Change Items | Species/form dependency | Silvally-specific value depends on form support. | BAN | Anton: treat as Ban Bad Items/default ban because it rarely has useful effect. |
| `form_change_nectar` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | future Form-Change Items | Species/form dependency | Nectars/form items may be useful or useless depending support. | BAN | Anton: treat as Ban Bad Items/default ban because it rarely has useful effect. |
| `form_change_other` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | future Form-Change Items | Script/mechanic dependency | Gracidea, DNA Splicers and similar items need explicit policy. | BAN | Anton: treat form-change/system items as Ban Bad Items/default ban unless separately reviewed. |
| `mail` | BAN by BanBad | BAN | BAN | BAN | BAN | BAN | none | Low-value reward | Gen3 already treats mail as bad; poor randomizer reward. | BAN | Anton: ban via Ban Bad Items. |
| `contest_deco_low_value` | BAN by BanBad | BAN | BAN | BAN | BAN | BAN | future Low-Value Items if desired | Low-value or unused feature | Contest/deco-only rewards are valid data but weak rewards here. | BAN | Anton: ban low-value contest/deco-only items via Ban Bad Items. |
| `berry_useful` | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | none | Low | Useful berries are safe rewards and trainer-held candidates. | ALLOW | Anton: allow useful berries. |
| `berry_low_value` | OPTIONAL or BanBad | OPTIONAL | OPTIONAL | OPTIONAL | REVIEW | BAN | future Low-Value Items | Low reward quality | Valid but can dilute rewards. | BAN | Anton: ban low-value berries via Ban Bad Items. |
| `medicine_healing` | ALLOW | ALLOW | ALLOW | ALLOW | BAN | ALLOW | none | Low | Good player reward; not a trainer held item. | ALLOW | Anton: allow healing medicine. |
| `status_healing` | ALLOW | ALLOW | ALLOW | ALLOW | OPTIONAL | ALLOW | none | Low | Generally useful; some berries overlap held-item logic. | ALLOW | Anton: allow status healing. |
| `poke_ball` | ALLOW basic, Master Ball optional | ALLOW | ALLOW | ALLOW | BAN | ALLOW | Overpowered Items for Master Ball | Economy/capture power | Basic balls are useful; Master Ball needs separate decision. | ALLOW | Anton: allow Poké Balls, including Master Ball. |
| `battle_item_consumable` | ALLOW player pools, optional held | ALLOW | ALLOW | ALLOW | OPTIONAL | ALLOW | future Battle Items | Difficulty/economy | X items are valid rewards but can affect balance. | ALLOW | Anton: allow battle consumables. |
| `held_battle_item` | HELD_ONLY by default | OPTIONAL | OPTIONAL | OPTIONAL | ALLOW | ALLOW | future Held Items in Rewards | Battle balance | Strong held items are best governed by held-item policy. | ALLOW | Anton: allow held battle items. |
| `evolution_item` | ALLOW, shop guarantee candidate | ALLOW | ALLOW | OPTIONAL | BAN | ALLOW | Guarantee Evolution Items | Progression balance | Useful rewards; existing shop guarantee option can handle availability. | ALLOW | Anton: allow evolution items. |
| `fossil` | REVIEW | OPTIONAL | OPTIONAL | REVIEW | BAN | REVIEW | future Fossil Items | Revival/source dependency | Useful only if fossil revival/content path is supported. | BAN | Anton: ban fossils because they should be obtained through normal progression. |
| `money_sell_item` | OPTIONAL economy item | ALLOW | OPTIONAL | OPTIONAL | BAN | ALLOW | Overpowered/Economy Items | Economy spike | Not bad, but strong economy rewards should be explicit. | ALLOW | Anton: allow normal sell/economy items like Nuggets; exclude only completely overpowered cases separately. |
| `rare_candy_vitamin` | OPTIONAL power item | ALLOW | OPTIONAL | OPTIONAL | BAN | ALLOW | Overpowered Items | Level/stat power | Powerful but valid; should not be confused with bad/invalid. | ALLOW | Anton: allow Rare Candy/Vitamin-style power items. |
| `shard_exchange_item` | REVIEW or BanBad in FRLG | OPTIONAL | OPTIONAL | OPTIONAL | BAN | BAN | future Exchange Items | May do nothing | FRLG bad list already marks shards as bad because they may lack use. | ALLOW | Anton: allow shard/exchange items. |
| `ordinary_utility` | ALLOW | ALLOW | ALLOW | ALLOW | BAN | ALLOW | none | Low | Safe player utility such as Escape Rope and Repel. | ALLOW | Anton: allow ordinary utility items. |
| `unknown_needs_review` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | none | Unknown behavior | Future/custom CFRU rows should not be silently allowed. | REVIEW | Anton: handle unknown items separately because their behavior is unclear. |

## 5. Example Item Table

| Item | Codex Category | Codex Recommendation | Field | Shop | Pickup | Trainer Held | BanBad | Reason | Anton Decision | Anton Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Potion | `medicine_healing` | ALLOW | ALLOW | ALLOW | ALLOW | BAN | ALLOW | Basic healing reward. | ALLOW | Anton: healing item allowed. |
| Super Potion | `medicine_healing` | ALLOW | ALLOW | ALLOW | ALLOW | BAN | ALLOW | Basic healing reward. | ALLOW | Anton: healing item allowed. |
| Full Restore | `medicine_healing` | ALLOW | ALLOW | ALLOW | ALLOW | BAN | ALLOW | Strong but valid healing reward. | ALLOW | Anton: healing item allowed. |
| Antidote | `status_healing` | ALLOW | ALLOW | ALLOW | ALLOW | BAN | ALLOW | Basic status recovery. | ALLOW | Anton: status healing allowed. |
| Escape Rope | `ordinary_utility` | ALLOW | ALLOW | ALLOW | ALLOW | BAN | ALLOW | Safe utility reward. | ALLOW | Anton: ordinary utility allowed. |
| Repel | `ordinary_utility` | ALLOW | ALLOW | ALLOW | ALLOW | BAN | ALLOW | Safe utility reward. | ALLOW | Anton: ordinary utility allowed. |
| Poke Ball | `poke_ball` | ALLOW | ALLOW | ALLOW | ALLOW | BAN | ALLOW | Basic capture reward. | ALLOW | Anton: Poké Ball allowed. |
| Ultra Ball | `poke_ball` | ALLOW | ALLOW | ALLOW | ALLOW | BAN | ALLOW | Strong but normal capture reward. | ALLOW | Anton: Poké Ball allowed. |
| Master Ball | `poke_ball` | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | BAN | ALLOW | Overpowered capture reward, not invalid. | ALLOW | Anton: Master Ball allowed. |
| Rare Candy | `rare_candy_vitamin` | OPTIONAL | ALLOW | OPTIONAL | OPTIONAL | BAN | ALLOW | Powerful level reward; OP/economy decision. | ALLOW | Anton: Rare Candy allowed. |
| Nugget | `money_sell_item` | OPTIONAL | ALLOW | OPTIONAL | OPTIONAL | BAN | ALLOW | Economy reward; current OP shop list handles shop ban. | ALLOW | Anton: normal sell/economy item allowed. |
| Big Nugget | `money_sell_item` | OPTIONAL | ALLOW | OPTIONAL | OPTIONAL | BAN | ALLOW | Strong economy reward if present. | ALLOW | Anton: sell/economy item allowed unless later classified as completely overpowered. |
| Bicycle | `key_progression` | BAN | BAN | BAN | BAN | BAN | BAN | Key/progression item. | BAN | Anton: key/progression item banned from random pools. |
| Old Rod | `key_progression` | BAN | BAN | BAN | BAN | BAN | BAN | Key/progression item. | BAN | Anton: key/progression item banned from random pools. |
| Good Rod | `key_progression` | BAN | BAN | BAN | BAN | BAN | BAN | Key/progression item. | BAN | Anton: key/progression item banned from random pools. |
| HM01 | `hm_field_move` | BAN | BAN | BAN | BAN | BAN | BAN | Field-move progression item. | BAN | Anton: HM/field-move item banned; should be obtained through normal progression. |
| TM51 | `tm_item` | BAN normal pools | BAN | BAN | BAN | BAN | REVIEW | Expanded TM item; TM pool only. | BAN | Anton: TM banned from normal pools; separate TM pool/slot handling. |
| Leftovers | `held_battle_item` | HELD_ONLY | OPTIONAL | OPTIONAL | OPTIONAL | ALLOW | ALLOW | Strong held item; valid trainer-held candidate. | ALLOW | Anton: held battle item allowed. |
| Choice Band | `held_battle_item` | HELD_ONLY | OPTIONAL | OPTIONAL | OPTIONAL | ALLOW | ALLOW | Strong held item; battle balance risk. | ALLOW | Anton: held battle item allowed. |
| Life Orb | `held_battle_item` | HELD_ONLY | OPTIONAL | OPTIONAL | OPTIONAL | ALLOW | ALLOW | Strong modern held item if present; review source ID. | ALLOW | Anton: held battle item allowed. |
| Oran Berry | `berry_useful` | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | Useful berry and held item. | ALLOW | Anton: useful berry allowed. |
| Chesto Berry | `berry_useful` | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | Useful status berry. | ALLOW | Anton: useful berry allowed. |
| Lum Berry | `berry_useful` | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | Useful status berry. | ALLOW | Anton: useful berry allowed. |
| Mail | `mail` | BAN | BAN | BAN | BAN | BAN | BAN | Low-value; Gen3 bad item range. | BAN | Anton: mail banned via Ban Bad Items. |
| Blue Shard | `shard_exchange_item` | REVIEW | OPTIONAL | OPTIONAL | OPTIONAL | BAN | BAN | FRLG may have no useful exchange path. | ALLOW | Anton: shard/exchange item allowed. |
| Tiny Mushroom | `money_sell_item` | OPTIONAL | ALLOW | OPTIONAL | OPTIONAL | BAN | ALLOW | Economy/exchange item; current OP shop list covers shop ban. | ALLOW | Anton: economy/exchange item allowed. |
| Fossil | `fossil` | REVIEW | OPTIONAL | OPTIONAL | REVIEW | BAN | REVIEW | Depends on fossil revival support and desired reward pacing. | BAN | Anton: fossil banned; should be obtained through normal progression. |
| Fire Stone | `evolution_item` | ALLOW | ALLOW | ALLOW | OPTIONAL | BAN | ALLOW | Useful evolution item; shop guarantee candidate. | ALLOW | Anton: evolution item allowed. |
| Linking Cord or equivalent | `evolution_item` | REVIEW | REVIEW | REVIEW | REVIEW | BAN | REVIEW | Not confirmed in local source by this audit; verify local item name/ID first. | ALLOW | Anton: evolution item allowed if present/verified locally. |
| Mega Stone | `mechanic_mega` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | REVIEW | Existing Include Mega Items setting should govern. | MECHANIC_SETTING | Anton: ban unless Mega items/mechanic is enabled. |
| Z-Crystal | `mechanic_z` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | REVIEW | Existing Include Z-Crystal Items setting should govern. | MECHANIC_SETTING | Anton: ban unless Z items/mechanic is enabled. |
| Dynamax Band | `mechanic_dynamax_gmax` | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | MECHANIC_SETTING | REVIEW | Existing Include Dynamax/GMax setting should govern. | MECHANIC_SETTING | Anton: ban unless Dynamax/GMax items/mechanic is enabled. |
| Plate | `form_change_plate` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | Categorized but no active pool policy. | BAN | Anton: ban via Ban Bad Items/default because it rarely has useful effect. |
| Drive | `form_change_drive` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | Species/form dependent. | BAN | Anton: ban via Ban Bad Items/default because it rarely has useful effect. |
| Memory | `form_change_memory` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | Species/form dependent. | BAN | Anton: ban via Ban Bad Items/default because it rarely has useful effect. |
| Nectar | `form_change_nectar` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | Form-change dependent. | BAN | Anton: ban via Ban Bad Items/default because it rarely has useful effect. |
| Gracidea | `form_change_other` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | Form-change item; needs explicit policy. | BAN | Anton: form-change item banned via Ban Bad Items/default. |
| DNA Splicers | `form_change_other` | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | REVIEW | Form-change/system item; needs explicit policy. | BAN | Anton: form-change/system item banned via Ban Bad Items/default. |
| Placeholder / ???? item | `invalid_placeholder` | BAN | BAN | BAN | BAN | BAN | BAN | Invalid or useless item row. | BAN | Anton: invalid/placeholder item banned. |
| Key Item example | `key_progression` | BAN | BAN | BAN | BAN | BAN | BAN | Script/progression risk. | BAN | Anton: key/progression item banned from random pools. |

## 6. Clear Proposals

Codex has a strong default recommendation for these categories:

- `invalid_placeholder` -> `BAN`.
- key/progression/script items -> `BAN`.
- HMs / field-move progression items -> `BAN` from normal pools.
- TMs -> `BAN` from normal Field/Shop/Pickup pools; keep a separate TM pool for TM slots.
- mail / contest / deco-only -> `BAN` by `BanBad Default`.
- healing, status recovery, basic balls and ordinary utility -> `ALLOW`.
- Mega/Z/Dynamax/GMax -> `MECHANIC_SETTING`.

## 7. Review Decisions

Anton's decisions have been applied in the `Anton Decision` and `Anton Notes` columns. The originally review-needed areas were:

- Plates: ban, allow, or future form-change toggle.
- Drives: ban, allow, or future form-change toggle.
- Memories: ban, allow, or future form-change toggle.
- Nectars: ban, allow, or future form-change toggle.
- Fossils: whether revival support makes them normal rewards.
- Shards, Mushrooms and exchange items: whether low value means `BanBad` or optional economy item.
- Rare Candy and Vitamins: whether they are normal rewards, OP-only, or toggle-gated.
- Master Ball: whether it is allowed outside special settings.
- Money items: whether Field/Pickup may include them and whether Shop should ban them.
- Form-change items such as Gracidea and DNA Splicers.
- Battle-only held items in Field/Shop/Pickup pools: allow as rewards or restrict to Trainer Held.

## 8. Anton Decision Summary

Anton's current default policy is:

- Ban invalid/placeholders, key/progression items, HMs/field-move items and TMs from normal pools.
- Keep TMs in a separate TM pool / TM-slot path.
- Gate Mega, Z and Dynamax/GMax items behind their corresponding mechanic settings.
- Treat Plates, Drives, Memories, Nectars and other form-change/system items as Ban Bad Items/default ban.
- Ban mail, contest/deco-only and low-value berries through Ban Bad Items.
- Allow useful berries, medicine, status healing, Poké Balls including Master Ball, battle consumables,
  held battle items, evolution items, sell/economy items, Rare Candy/Vitamins, shard/exchange items and
  ordinary utility items.
- Ban fossils because they should be obtained through normal progression.
- Keep `unknown_needs_review` separate until local behavior is understood.

## 9. Implementation After Review


No implementation is included here. A later code task would likely touch:

- `Gen3RomHandler.loadItems()` or a new source-backed item classifier to annotate richer categories.
- `CfruDpeItemCategories` for additional CFRU/DPE source-backed blocks.
- `ItemMechanicPredicates` or a new `ItemPoolPolicy` helper for pool-specific decisions.
- `ItemRandomizer` for Field, Shop and Pickup filters.
- `TrainerPokemonRandomizer` for a separate Trainer Held Item policy.
- Settings, GUI and settings-profile generation if Anton approves new toggles.

Required later tests:

- ROM-free category classifier tests for representative local source IDs/names.
- Field/Shop/Pickup pool tests for each category and each toggle.
- Trainer Held Item policy tests, including consumable-only and sensible-items modes.
- Regression tests for no TMs/HMs in normal pools and separate TM field-slot behavior.
- A generated TSV/manual audit path for `unknown_needs_review` items before they are allowed.
