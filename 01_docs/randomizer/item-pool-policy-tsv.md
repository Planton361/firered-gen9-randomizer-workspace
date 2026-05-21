# CFRU/DPE Item Pool Policy Review TSV

Status: review-only Markdown/TSV analysis from local CFRU/DPE source constants and current UPR-FVX item-pool policy. No ROMs were read, copied, generated, or tested. No builds were run. No CFRU/DPE table values or UPR-FVX code were changed.

The optional external TSV file was not created because `04_data/reference/items/` does not exist in this workspace.

## Scope And Limits

This is not a final ROM candidate dump. It maps local source constants from `02_external/CFRU-expansion/include/constants/items.h` and source metadata from `src/Tables/item_tables.c` against the current FVX policy classes:

- `Gen3RomHandler.loadItems()` reads final ROM `ItemData`, then applies FVX `allowed`, `bad`, and `tm` flags.
- Normal Field non-TM, Shop random filler, and Pickup random pools use `allowed` or `nonBad`, apply `ItemMechanicPredicates`, and remove `Item::isTM`.
- `CfruDpeItemPoolPolicy` hard-bans fossils from normal pools and marks Shards, Relic/high-value valuables, Apricorns, Memories, Plates, Drives, Nectars, and covered form-change items as bad when Ban Bad Items is on.
- `ItemMechanicPredicates` gates Mega, Z-Crystal, and Dynamax/GMax items by the existing include settings.

Where exact final ROM item names or standard IDs are required, this table uses `REVIEW` or `UNKNOWN`. Range rows are used where adjacent constants share one policy and expanding every individual row would not add review value.

## Policy Values

- `ALLOW`: expected to remain candidate-eligible in normal pools when loaded as allowed/non-bad.
- `BAN`: expected to be excluded by current policy when Ban Bad Items is on, or hard-banned before pool construction.
- `MECHANIC_SETTING`: controlled by Include Mega Items, Include Z-Crystal Items, or Include Dynamax/GMax Items.
- `REVIEW`: local source exists, but current source-to-ROM/name/policy confidence is not strong enough for an allow/ban claim.
- `OUT_OF_SCOPE`: source item is not part of normal Field/Shop/Pickup policy or was not found locally.
- `UNKNOWN`: local evidence is insufficient.

## Review TSV

```tsv
local_constant	local_id_or_value	local_name_guess	category_guess	field_ban_bad_on	shop_ban_bad_on	pickup_ban_bad_on	trainer_held_policy	mechanic_setting_dependency	reason	evidence_source	confidence	anton_review_needed
ITEM_NONE	0	None	invalid_placeholder	BAN	BAN	BAN	BAN	none	Null/no-item sentinel, not a reward candidate.	items.h; Gen3RomHandler fallback/allowed model	High	no
ITEM_MASTER_BALL	1	Master Ball	poke_ball	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Poke Ball policy keeps balls reward-eligible; optional shop OP filter can remove shop filler separately.	items.h; CfruDpeItemPoolPolicyTest.pokeBallsAreRecognizedAsAllowedRewardItems	High	yes
ITEM_ULTRA_BALL..ITEM_PREMIER_BALL	2..12	Ultra Ball..Premier Ball	poke_ball	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Poke Ball names/range are allowed reward items; encounter-held pool blocks Poke Balls separately.	items.h; CfruDpeItemPoolPolicy.isPokeBallItem	High	no
ITEM_POTION..ITEM_MOOMOO_MILK	13..29	healing/status medicines	medicine_healing	ALLOW	ALLOW	ALLOW	REVIEW	none	Healing/status items are not newly banned and are typed as healing/status in local CFRU item tables.	items.h; item_tables.c gItemsByType; CfruDpeItemPoolPolicyTest.clearlyAllowedPolicyItemsAreNotNewlyBanned	High	no
ITEM_ENERGY_POWDER..ITEM_REVIVAL_HERB	30..33	herbal healing medicines	medicine_healing	ALLOW	ALLOW	ALLOW	REVIEW	none	Healing category; not covered by CFRU/DPE bad policy.	items.h; item_tables.c gItemsByType	Medium	no
ITEM_ETHER..ITEM_MAX_ELIXIR	34..37	PP recovery	status_healing	ALLOW	ALLOW	ALLOW	REVIEW	none	PP recovery is useful utility, not a current bad/mechanic category.	items.h; item_tables.c gItemsByType	Medium	no
ITEM_BLUE_FLUTE..ITEM_WHITE_FLUTE	39..43	flutes	ordinary_utility	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Utility/story-adjacent item class; not currently classified by CFRU/DPE policy.	items.h; item_tables.c gItemsByType ITEM_TYPE_FLUTE	Medium	yes
ITEM_SHOAL_SALT..ITEM_SHOAL_SHELL	46..47	Shoal items	contest_deco_low_value	BAN	BAN	BAN	OUT_OF_SCOPE	none	FRLG bad list bans shoal/shard range as low-value/no-use in this context.	items.h; Gen3Constants.setupBadItemsFRLG	High	no
ITEM_RED_SHARD..ITEM_GREEN_SHARD	48..51	Red/Blue/Yellow/Green Shard	shard_exchange_item	BAN	BAN	BAN	OUT_OF_SCOPE	none	Current policy marks Shards bad when Ban Bad Items is on.	items.h; CfruDpeItemPoolPolicy.isShardExchangeItem; policy tests	High	no
ITEM_HP_UP..ITEM_PP_MAX	63..71	vitamins / Rare Candy / PP Up	rare_candy_vitamin	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Anton policy keeps these allowed; Rare Candy can still be removed by optional shop OP filter.	items.h; item_tables.c gItemsByType; policy tests	High	yes
ITEM_DYNAMAX_CANDY	72	Dynamax Candy	mechanic_dynamax_gmax	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	Include Dynamax/GMax Items	Dynamax/GMax category is excluded unless matching include setting is on.	items.h; CfruDpeItemCategories; ItemMechanicPredicatesTest	High	no
ITEM_GUARD_SPEC..ITEM_POKE_DOLL	73..80	X/battle consumables	battle_item_consumable	ALLOW	ALLOW	ALLOW	REVIEW	none	X items and battle consumables are not banned by current policy; X Defend is test-covered as allowed.	items.h; item_tables.c gItemsByType; CfruDpeItemPoolPolicyTest	High	no
ITEM_FLUFFY_TAIL	81	Fluffy Tail	battle_item_consumable	ALLOW	ALLOW	ALLOW	REVIEW	none	Battle escape item; not currently a bad/mechanic category.	items.h; item_tables.c	Medium	no
ITEM_SUPER_REPEL..ITEM_REPEL	83..86	repels / Escape Rope	ordinary_utility	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Ordinary utility item; Escape Rope is test-covered as allowed.	items.h; item_tables.c gItemsByType; policy tests	High	no
ITEM_LINK_CABLE..ITEM_ICE_STONE	87..102	evolution stones/items	evolution_item	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Evolution items are intentionally allowed; shop guarantee path may handle availability separately.	items.h; item_tables.c gItemsByType	Medium	yes
ITEM_TINY_MUSHROOM..ITEM_BIG_MUSHROOM	103..104	Mushrooms	money_sell_item	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Not part of current high-value ban; optional shop OP list can remove shop filler.	items.h; Gen3Constants.opShopItems	Medium	yes
ITEM_BALM_MUSHROOM	105	Balm Mushroom	high_value_money_sell_item	BAN	BAN	BAN	OUT_OF_SCOPE	none	Current high-value valuable predicate marks it bad under Ban Bad Items.	items.h; CfruDpeItemPoolPolicy.isHighValueValuableItem; policy tests	High	no
ITEM_PEARL..ITEM_NUGGET	106..110	Pearl..Nugget	money_sell_item	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Lower-value sell items remain allowed by policy; optional shop OP list can remove shop filler.	items.h; Gen3Constants.opShopItems; Nugget allowed test	High	yes
ITEM_HEART_SCALE	111	Heart Scale	ordinary_utility	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Local CFRU classifies it as sellable; current policy does not ban it.	items.h; item_tables.c gItemsByType	Medium	yes
ITEM_RARE_BONE..ITEM_BIG_NUGGET	112..115	Rare Bone / Pearl String / Comet Shard / Big Nugget	high_value_money_sell_item	BAN	BAN	BAN	OUT_OF_SCOPE	none	Current high-value valuable predicate marks these bad under Ban Bad Items.	items.h; CfruDpeItemPoolPolicy.isHighValueValuableItem; policy tests	High	no
ITEM_HONEY	116	Honey	ordinary_utility	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Field-use utility item; not currently classified as bad.	items.h; item_tables.c gItemsByType	Medium	yes
ITEM_PRETTY_WING	117	Pretty Wing	money_sell_item	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Sellable/low-value item not explicitly in current high-value list.	items.h; item_tables.c gItemsByType	Medium	yes
ITEM_ORANGE_MAIL..ITEM_RETRO_MAIL	121..132	Mail	mail	BAN	BAN	BAN	BAN	none	Legacy Gen3 bad list marks mail bad; weak/no-use random reward.	items.h; Gen3Constants.setupBadItemsRSE	High	no
ITEM_CHERI_BERRY..ITEM_SITRUS_BERRY	133..142	useful berries	berry_useful	ALLOW	ALLOW	ALLOW	ALLOW	none	Policy explicitly clears legacy bad for useful berries.	items.h; CfruDpeItemPoolPolicy.USEFUL_BERRY_IDS; tests	High	no
ITEM_FIGY_BERRY..ITEM_ENIGMA_BERRY_OLD	143..175	low/conditional berries	berry_low_value	BAN	BAN	BAN	REVIEW	none	Legacy Gen3 bad ranges mark many lower-value/contest/flavor berries bad.	items.h; Gen3Constants.setupBadItemsRSE	Medium	yes
ITEM_BRIGHT_POWDER..ITEM_LEEK	179..225	legacy held battle / species held items	held_battle_item	ALLOW	ALLOW	ALLOW	ALLOW	none	Held battle items are not newly banned; some legacy species-specific held items are explicitly allowed when Ban Bad is on.	items.h; CfruDpeItemPoolPolicy.HELD_BATTLE_ITEM_IDS_ALLOWED_BY_POLICY	Medium	yes
ITEM_STRAWBERRY_SWEET..ITEM_STAR_SWEET	226..232	Alcremie sweets	evolution_item	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Local CFRU type table treats these as evolution items; current policy does not ban them.	items.h; item_tables.c gItemsByType	Medium	yes
ITEM_SWEET_APPLE..ITEM_GALARICA_WREATH	233..238	modern evolution items	evolution_item	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Evolution-item class remains allowed by policy.	items.h; item_tables.c gItemsByType	Medium	yes
ITEM_CHERISH_BALL..ITEM_PARK_BALL	239..253	modern/special balls	poke_ball	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Local source ball range; current name predicate covers common balls but not every modern name, so final name behavior should be reviewed.	items.h; item_tables.c item data rows	Medium	yes
ITEM_RED_SCARF..ITEM_YELLOW_SCARF	254..258	contest scarves	contest_deco_low_value	BAN	BAN	BAN	OUT_OF_SCOPE	none	Legacy Gen3 bad list marks contest scarves bad.	items.h; Gen3Constants.setupBadItemsRSE	High	no
ITEM_MACH_BIKE..ITEM_DEVON_SCOPE	259..288	key/progression and fossils	key_progression	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Mixed range: bikes/rods/tickets/story items should be blocked, fossils are hard-banned; review exact final IDs/names if any leak appears.	items.h; Gen3Constants unique/key item mapping; fossil policy	Medium	yes
ITEM_TM01..ITEM_TM50	0x121..0x152	TM01..TM50	tm_item	BAN	BAN	BAN	OUT_OF_SCOPE	none	Normal Field/Shop/Pickup remove Item::isTM; TM field slots remain separate.	items.h; Gen3RomHandler.loadItems; ItemRandomizer; ItemDecisionTest	High	no
ITEM_HM01_CUT..ITEM_HM08_ROCK_CLIMB	0x153..0x15A	HM01..HM08	hm_field_move	BAN	BAN	BAN	BAN	none	HMs are globally banned through Gen3 constants and should not enter normal pools.	items.h; Gen3Constants.bannedItems	High	no
ITEM_TM51..ITEM_TM120	376..0x1BD	expanded TM51..TM120	tm_item	BAN	BAN	BAN	OUT_OF_SCOPE	none	CFRU/DPE expanded TM classification marks source-block TM names as TMs; normal pools remove them.	items.h; CfruDpeItemCategories.isCfruDpeExpandedTechnicalMachineItem; ItemDecisionTest	High	no
ITEM_DYNAMAX_BAND	347	Dynamax Band	mechanic_dynamax_gmax	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	Include Dynamax/GMax Items	Mechanic setting controls Dynamax/GMax item availability.	items.h; ItemMechanicPredicatesTest	High	no
ITEM_GOLD_TEETH..ITEM_X_SP_DEF	348..375	FRLG/CFRU key/system items	key_progression	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Mixed key/progression/system range; many map to Gen3 unique IDs, but final source-to-ROM identity should be verified if seen.	items.h; Gen3Constants.itemIDToStandardMap	Medium	yes
ITEM_OCCA_BERRY..ITEM_MARANGA_BERRY	0x1BE..0x1D5	modern berries	berry_useful	ALLOW	ALLOW	ALLOW	ALLOW	none	Modern battle berries are valid held/useful items; not in current bad policy.	items.h; item_tables.c gFlingTable; gItemsByType berry context	Medium	yes
ITEM_OVAL_CHARM..ITEM_MAGMA_STONE	0x1D6..0x1DA	Charms / legendary key items	key_progression	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Local source identifies key/system-like items; current CFRU/DPE pool policy does not explicitly classify every one.	items.h	Medium	yes
ITEM_LIGHT_STONE	0x1DB	Light Stone	legendary_form_key_system	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Found locally, but not explicitly covered by current form-change predicate; treat as review-required potential leak if final ItemData loads it allowed.	items.h; rg source check; CfruDpeItemCategories name sets	Medium	yes
ITEM_DARK_STONE	0x1DC	Dark Stone	legendary_form_key_system	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Found locally, but not explicitly covered by current form-change predicate; treat as review-required potential leak if final ItemData loads it allowed.	items.h; rg source check; CfruDpeItemCategories name sets	Medium	yes
ITEM_SUN_FLUTE..ITEM_MOON_FLUTE	0x1DD..0x1DE	Sun/Moon Flute	legendary_form_key_system	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Story/system items; not explicitly covered by current policy.	items.h	Medium	yes
ITEM_GRACIDEA	0x1DF	Gracidea	legendary_form_key_system	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Found locally; current predicate does not list Gracidea by name, so do not claim it is blocked without final evidence.	items.h; CfruDpeItemCategories.NECTAR_FORM_CHANGE_NAMES	Medium	yes
ITEM_DNA_SPLICERS	0x1E0	DNA Splicers	legendary_form_key_system	BAN	BAN	BAN	OUT_OF_SCOPE	none	Name-based form-change predicate marks DNA Splicers bad when Ban Bad Items is on.	items.h; CfruDpeItemCategories.NECTAR_FORM_CHANGE_NAMES; CfruDpeItemPoolPolicyTest	High	no
ITEM_REVEAL_GLASS	0x1E1	Reveal Glass	legendary_form_key_system	BAN	BAN	BAN	OUT_OF_SCOPE	none	Name/ID-backed form-change predicate marks it bad when Ban Bad Items is on.	items.h; CfruDpeItemCategories; policy tests	High	no
ITEM_PRISON_BOTTLE	0x1E2	Prison Bottle	legendary_form_key_system	BAN	BAN	BAN	OUT_OF_SCOPE	none	Name-based form-change predicate marks it bad when Ban Bad Items is on if decoded name matches.	items.h; CfruDpeItemCategories.NECTAR_FORM_CHANGE_NAMES	Medium	no
ITEM_N_SOLARIZER..ITEM_N_LUNARIZER	0x1E3..0x1E4	N-Solarizer / N-Lunarizer	legendary_form_key_system	BAN	BAN	BAN	OUT_OF_SCOPE	none	Name-based form-change predicate marks these bad when Ban Bad Items is on if decoded names match.	items.h; CfruDpeItemCategories.NECTAR_FORM_CHANGE_NAMES	Medium	no
ITEM_RUSTED_SWORD..ITEM_RUSTED_SHIELD	0x1E5..0x1E6	Rusted Sword/Shield	held_battle_item	REVIEW	REVIEW	REVIEW	ALLOW	none	Legendary held items are typed as held items locally but are form/species dependent; no current ban predicate.	items.h; item_tables.c gItemsByType	Medium	yes
ITEM_ADAMANT_ORB..ITEM_GRISEOUS_ORB	0x1E7..0x1E9	legendary orbs	legendary_form_key_system	BAN	BAN	BAN	REVIEW	none	Current form-change names include Adamant/Lustrous/Griseous Orb, so Ban Bad filters them.	items.h; CfruDpeItemCategories.NECTAR_FORM_CHANGE_NAMES	High	no
ITEM_FIST_PLATE..ITEM_PIXIE_PLATE	0x1EA..0x1FA	Arceus Plates	form_change_plate	BAN	BAN	BAN	REVIEW	none	Current form-change policy marks Plates bad when Ban Bad Items is on.	items.h; item_tables.c gItemsByType ITEM_TYPE_PLATE; policy tests	High	no
ITEM_FIGHTING_MEMORY..ITEM_FAIRY_MEMORY	0x1FB..0x20B	Silvally Memories / * Mem. variants	form_change_memory	BAN	BAN	BAN	REVIEW	none	Current name/ID predicates cover full Memory and abbreviated Mem. variants.	items.h; CfruDpeItemCategories.SILVALLY_MEMORY_NAMES; policy tests	High	no
ITEM_BURN_DRIVE..ITEM_CHILL_DRIVE	0x20C..0x20F	Genesect Drives	form_change_drive	BAN	BAN	BAN	REVIEW	none	Current form-change policy marks Drives bad when Ban Bad Items is on.	items.h; item_tables.c gItemsByType ITEM_TYPE_DRIVE; policy tests	High	no
ITEM_RED_NECTAR..ITEM_PURPLE_NECTAR	0x210..0x213	Nectars	form_change_nectar	BAN	BAN	BAN	REVIEW	none	Current form-change policy marks Nectars bad when Ban Bad Items is on.	items.h; item_tables.c gItemsByType ITEM_TYPE_NECTAR; policy tests	High	no
ITEM_ULTRANECROZIUM_Z	0x214	Ultranecrozium Z	mechanic_z	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	Include Z-Crystal Items	Mechanic predicate treats it as Z-related and gates it by Include Z.	items.h; CfruDpeItemCategories; ItemMechanicPredicatesTest	High	no
ITEM_VENUSAURITE..ITEM_DIANCITE	0x215..0x243	Mega Stones	mechanic_mega	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	Include Mega Items	Mechanic predicate gates Mega Stones by Include Mega Items; localized/name variants are tested for key leak cases.	items.h; item_tables.c ITEM_TYPE_MEGA_STONE; ItemMechanicPredicatesTest	High	no
ITEM_NORMALIUM_Z..ITEM_TAPUNIUM_Z	0x244..0x265	Z-Crystals	mechanic_z	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	Include Z-Crystal Items	Mechanic predicate gates all local source Z-Crystal range by Include Z when decoded name matches.	items.h enum; item_tables.c ITEM_TYPE_Z_CRYSTAL; ItemMechanicPredicatesTest	High	no
ITEM_BLACK_APRICORN..ITEM_YELLOW_APRICORN	0x266..0x26C	Apricorns / Aprikokos	apricorn	BAN	BAN	BAN	OUT_OF_SCOPE	none	Current policy marks Apricorn/Aprikoko variants bad when Ban Bad Items is on.	items.h; CfruDpeItemPoolPolicy.isApricornItem; policy tests	High	no
ITEM_RELIC_COPPER..ITEM_RELIC_CROWN	0x26D..0x273	Relic valuables	high_value_money_sell_item	BAN	BAN	BAN	OUT_OF_SCOPE	none	Current policy marks Relic valuables bad when Ban Bad Items is on.	items.h; item_tables.c ITEM_TYPE_RELIC; policy tests	High	no
ITEM_SKULL_FOSSIL..ITEM_FOSSILIZED_DINO	0x274..0x27D	Fossils	fossil	BAN	BAN	BAN	BAN	none	Current policy hard-bans fossils from normal item pools.	items.h; CfruDpeItemPoolPolicy.isBannedFromNormalItemPools; policy tests	High	no
ITEM_ODD_KEYSTONE	0x27E	Odd Keystone	money_sell_item	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Local table marks it sellable; story/form context unclear for random rewards.	items.h; item_tables.c gItemsByType ITEM_TYPE_SELLABLE	Medium	yes
ITEM_BOTTLE_CAP..ITEM_GOLD_BOTTLE_CAP	0x27F..0x280	Bottle Caps	rare_candy_vitamin	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Local table treats caps as sellable/modern reward context; current policy does not ban them.	items.h; item_tables.c gItemsByType	Low	yes
ITEM_WISHING_PIECE	0x281	Wishing Piece	mechanic_dynamax_gmax	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	MECHANIC_SETTING	Include Dynamax/GMax Items	Mechanic predicate gates Wishing Piece as Dynamax/GMax-related.	items.h; CfruDpeItemCategories; ItemMechanicPredicatesTest	High	no
ITEM_POWER_BRACER..ITEM_POWER_WEIGHT	0x282..0x287	Power EV held items	held_battle_item	ALLOW	ALLOW	ALLOW	ALLOW	none	Typed as stat-boost held items; current policy does not ban them.	items.h; item_tables.c gItemsByType	Medium	yes
ITEM_LUCK_INCENSE..ITEM_WAVE_INCENSE	0x288..0x28E	Incense held items	held_battle_item	ALLOW	ALLOW	ALLOW	ALLOW	none	Typed as incense/held item; current policy does not ban them.	items.h; item_tables.c gItemsByType	Medium	yes
ITEM_NORMAL_GEM..ITEM_FAIRY_GEM	0x28F..0x2A0	Gems	held_battle_item	ALLOW	ALLOW	ALLOW	ALLOW	none	Gems are allowed by current policy; Fire Gem is explicitly test-covered.	items.h; item_tables.c gItemsByType ITEM_TYPE_GEM; policy tests	High	no
ITEM_WIDE_LENS..ITEM_THROAT_SPRAY	0x2A1..0x2D7	modern held battle items	held_battle_item	ALLOW	ALLOW	ALLOW	ALLOW	none	Current policy does not ban these; balance review may still be desired for normal reward pools.	items.h; item_tables.c gItemsByType held items	Medium	yes
ITEM_ABILITY_CAPSULE..ITEM_ABILITY_PATCH	0x2D8..0x2D9	ability modifiers	rare_candy_vitamin	REVIEW	REVIEW	REVIEW	OUT_OF_SCOPE	none	Powerful modifier items; not currently banned, but final policy/balance should be reviewed.	items.h; item_tables.c gItemsByType ability modifier	Medium	yes
ITEM_AUSPICIOUS_ARMOR..ITEM_SYRUPY_APPLE	0x2DA..0x2E1	modern evolution items	evolution_item	ALLOW	ALLOW	ALLOW	OUT_OF_SCOPE	none	Local type table marks these as evolution items; current policy allows evolution items.	items.h; item_tables.c gItemsByType	Medium	yes
ITEM_CLEAR_AMULET..ITEM_PUNCHING_GLOVE	0x2E2..0x2E5	modern held battle items	held_battle_item	ALLOW	ALLOW	ALLOW	ALLOW	none	Current policy does not ban these if final ItemData loads them normally.	items.h; item_tables.c likely held item rows	Low	yes
ITEM_REINS_OF_UNITY	0x2E6	Reins of Unity	legendary_form_key_system	BAN	BAN	BAN	REVIEW	none	Current form-change predicate includes Reins of Unity name variants.	items.h; CfruDpeItemCategories.NECTAR_FORM_CHANGE_NAMES	Medium	no
ITEM_BOOSTER_ENERGY..ITEM_PORTABLE_PC	0x2E7..0x307	modern system/free-space block	key_progression	BAN	BAN	BAN	BAN	none	CFRU/DPE encounter-held banned set hard-disallows this source block during load; includes Tera Orb and Portable PC.	items.h; Gen3Constants.cfruDpeEncounterHeldItemBannedItems	High	no
ITEM_FREE_SPACE1..ITEM_FREE_SPACE3	0x308..0x30A	free space / reserved	invalid_placeholder	BAN	BAN	BAN	BAN	none	CFRU/DPE free-space range is disallowed/bad by load policy.	items.h; Gen3Constants.cfruDpeFreeSpace1..cfruDpeShinySpace20	High	no
ITEM_ZYGARDE_CUBE	not found locally	Zygarde Cube	legendary_form_key_system	OUT_OF_SCOPE	OUT_OF_SCOPE	OUT_OF_SCOPE	OUT_OF_SCOPE	none	Requested review item was not found in local CFRU items.h; generic FVX name predicate would ban if a decoded item has this name.	rg items.h; CfruDpeItemCategories.NECTAR_FORM_CHANGE_NAMES	Medium	yes
ITEM_RED_CHAIN	not found locally	Red Chain	legendary_form_key_system	OUT_OF_SCOPE	OUT_OF_SCOPE	OUT_OF_SCOPE	OUT_OF_SCOPE	none	Requested review item was not found in local CFRU items.h and is not covered by current name predicates.	rg items.h; CfruDpeItemCategories name sets	Medium	yes
custom/localized future item	UNKNOWN	custom item	unknown_needs_review	REVIEW	REVIEW	REVIEW	REVIEW	none	Unknown items are not silently added to new ban or allow categories; final ItemData decides loaded name/status.	CfruDpeItemPoolPolicyTest.unknownItemsAreNotSilentlyAddedToNewBanOrAllowCategories	High	yes
```

## Notes For Review

- The current code-derived policy is stricter than older review docs for several form-change categories: Plates, Drives, Memories, Nectars, DNA Splicers, Reveal Glass, Prison Bottle, N-Solarizer, N-Lunarizer, Reins of Unity, and Adamant/Lustrous/Griseous Orbs are now expected to be Ban-Bad filtered when their decoded names match the current predicates.
- `ITEM_LIGHT_STONE`, `ITEM_DARK_STONE`, and `ITEM_GRACIDEA` are local source constants but are not explicitly covered by the current form-change name sets. They should be treated as review-required potential leaks if Anton observes them in normal pools.
- `ITEM_ZYGARDE_CUBE` and `ITEM_RED_CHAIN` were not found in the local CFRU `items.h`. `Zygarde Cube` is covered by a generic name predicate if such a final item exists; `Red Chain` is not covered by the current name predicates.
- `ALLOW` does not mean "good design"; it means the current policy likely permits the row in normal Field/Shop/Pickup pools when the final ROM loads it as allowed/non-bad. Balance-heavy allowed rows, especially Master Ball, Rare Candy, Bottle Caps, held battle items, and modern berries, still need Anton review.
- Shop-only optional filters are not fully represented in the Field/Shop/Pickup columns. For example `Ban OP Shop Items` can remove Rare Candy and vanilla money/ball ranges from shop filler even when Field/Pickup would still allow them.

## Next Minimal Action

Review the rows marked `anton_review_needed=yes` and decide whether any should become explicit future code-policy bans. The smallest follow-up code scope would be only the currently uncovered local form/story constants if Anton confirms they should be banned: `ITEM_LIGHT_STONE`, `ITEM_DARK_STONE`, and `ITEM_GRACIDEA`.
