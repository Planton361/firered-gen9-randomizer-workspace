# Item Pool UNKNOWN Candidate Review

Status: documentation-only review from the local sanitized `combined_item_summary.tsv` under `.local/item-pool-analysis/`. No raw logs, ROMs, output ROMs, saves, screenshots, builds, private paths, hashes, or table values were read or documented. No UPR-FVX code or workspace tooling was changed.

## Scope

The current 1000-run combined item summary contains 259 item rows. Of those, 113 rows still have `policy_guess=UNKNOWN` from the analyzer. `UNKNOWN` means the analyzer did not match a known allow/suspicious heuristic; it does not mean the item is unsafe, and it does not prove a randomizer policy bug.

This review groups those UNKNOWN rows into Anton-review buckets. It is intentionally not a new UPR-FVX policy. Any ban, allow, or toggle decision still needs Anton confirmation before code changes.

Reference context:

- `01_docs/randomizer/item-policy-ban-audit.md`: current hard bans, Ban-Bad-only bans, mechanic-setting gates, and likely over-broad categories.
- `01_docs/randomizer/item-pool-policy-tsv.md`: local CFRU/DPE source table review and current policy caveats.
- `.local/item-pool-analysis/combined_item_summary.tsv`: sanitized local 1000-run item summary, used only as aggregate evidence.

## Review Buckets

| Bucket | Meaning | Policy implication |
| --- | --- | --- |
| `ALLOW_HELD_BATTLE` | Looks like a normal held battle item or held utility item. | Likely okay to allow unless Anton wants reward-pool balance restrictions. |
| `ALLOW_EVOLUTION` | Looks like an evolution item or evolution-held item. | Likely okay because evolution items are currently allowed, but rare/custom evolutions can still need balance review. |
| `ALLOW_UTILITY` | Looks like normal player utility, healing, or status support. | Likely okay to allow. |
| `REVIEW_BALANCE_POWER` | Useful but power-affecting item. | Not "bad", but Anton should decide if normal Field/Shop/Pickup pools should include it. |
| `REVIEW_ECONOMY` | Money gain, sell value, or reward economy item. | Anton should decide if it belongs in normal pools or an economy/OP filter. |
| `REVIEW_STORY_SYSTEM` | Key/story/system-like item or special unlock. | Needs source/script context before allowing. |
| `BAN_RECOMMENDED` | Strong candidate for exclusion from normal random reward pools. | Recommendation only; no new policy without Anton decision. |

## Highlighted Findings

| Item | Observed total | Suggested bucket | Why it matters | Recommendation |
| --- | ---: | --- | --- | --- |
| `A-Potion` | 48 | `REVIEW_BALANCE_POWER` | Local CFRU source maps this name to `ITEM_ABILITY_CAPSULE`, a party-use ability modifier with high price. | Decide whether ability modifiers are allowed normal rewards or need OP/balance filtering. |
| `A-Patch` | 50 | `REVIEW_BALANCE_POWER` | Local CFRU source maps this name to `ITEM_ABILITY_PATCH`, a stronger hidden-ability modifier. | Same as `A-Potion`; likely stronger balance concern. |
| `Lucky Egg` | 34 | `REVIEW_BALANCE_POWER` | Held EXP multiplier; useful but can heavily affect progression pace. | Consider optional OP/balance filtering, not Ban-Bad by default. |
| `Exp. Share` | 75 | `REVIEW_BALANCE_POWER` | CFRU source lists it as a key-item style field toggle, while item type review also shows held-item context; gameplay impact is large. | Needs Anton decision; do not silently treat as ordinary utility. |
| `Amulet Coin` | 44 | `REVIEW_ECONOMY` | Held double-prize item; affects money economy. | Consider economy/OP review bucket. |
| `Luck Incense` | 130 | `REVIEW_ECONOMY` | Incense variant of prize-money boost. | Same as `Amulet Coin`. |
| `Gimmi Coin` | 89 | `ALLOW_EVOLUTION` with caveat | Local CFRU table marks `ITEM_GIMMIGHOUL_COIN` as `ITEM_TYPE_EVOLUTION_ITEM`. | Likely allow if evolution items stay allowed; review because it is also coin/currency-themed. |
| `Silver Wing` | 70 | `BAN_RECOMMENDED` | Local CFRU source marks it as key-item pocket and importance `1`. | Recommend excluding from normal pools unless a scripted use is intentionally wanted. |
| `Rainbow Wing` | 57 | `BAN_RECOMMENDED` | Same key-item/story-unlock pattern as `Silver Wing`. | Recommend excluding from normal pools unless intentionally used. |
| `Sacred Ash` | 46 | `REVIEW_BALANCE_POWER` | Local CFRU `gItemsByType` maps it to revive type; it is powerful but not story/system by itself. | Review as powerful healing, not as invalid. |

## Grouped UNKNOWN Rows

### ALLOW_HELD_BATTLE

These look like normal held battle items, held utility items, type boosters, weather/terrain extenders, or species-held items. They should not be banned just because the analyzer did not recognize them.

| Item | Observed total | Notes |
| --- | ---: | --- |
| `Air Balloon` | 86 | Held battle utility. |
| `Assault Vest` | 50 | Held battle item. |
| `Big Root` | 44 | Held drain-effect item. |
| `Binding Band` | 45 | Held battle item. |
| `Black Belt` | 60 | Type-boosting held item. |
| `Black Sludge` | 96 | Held item; poison-specific healing/damage. |
| `BlackGlasses` | 37 | Type-boosting held item. |
| `Blunder Pol.` | 82 | Abbreviated Blunder Policy; held battle item. |
| `BrightPowder` | 62 | Held evasion item; balance-sensitive but normal held category. |
| `Cell Battery` | 55 | Held consumable. |
| `Charcoal` | 59 | Type-boosting held item. |
| `Choice Scarf` | 55 | Strong held battle item. |
| `Choice Specs` | 81 | Strong held battle item. |
| `Cleanse Tag` | 96 | Held encounter-rate utility. |
| `Covert Cloak` | 83 | Held battle item. |
| `Damp Rock` | 87 | Weather extender. |
| `Destiny Knot` | 66 | Held utility/battle item. |
| `Dragon Fang` | 65 | Type-boosting held item. |
| `Eject Button` | 56 | Held battle item. |
| `Eject Pack` | 87 | Held battle item. |
| `Elect. Seed` | 80 | Terrain seed. |
| `Focus Band` | 74 | Held battle item. |
| `Focus Sash` | 92 | Strong held battle item. |
| `Full Incense` | 47 | Incense held item. |
| `Grassy Seed` | 59 | Terrain seed. |
| `Grip Claw` | 61 | Held battle item. |
| `Heat Rock` | 67 | Weather extender. |
| `HeavyDBoots` | 28 | Abbreviated Heavy-Duty Boots; held battle item. |
| `Lagging Tail` | 59 | Held battle item. |
| `Lax Incense` | 37 | Incense/evasion held item. |
| `Leek` | 107 | Species-held item; already treated as allowed in policy tests. |
| `Light Clay` | 20 | Screen-duration held item. |
| `Loaded Dice` | 42 | Held battle item. |
| `Lucky Punch` | 87 | Species-held item; already treated as allowed in policy tests. |
| `LuminousMoss` | 59 | Held consumable. |
| `Macho Brace` | 71 | Held EV/training item. |
| `Magnet` | 101 | Type-boosting held item. |
| `Mental Herb` | 107 | Held consumable. |
| `Metal Powder` | 68 | Species-held item; already treated as allowed in policy tests. |
| `Metronome` | 94 | Held battle item. |
| `Misty Seed` | 56 | Terrain seed. |
| `Muscle Band` | 38 | Held battle item. |
| `Mystic Water` | 80 | Type-boosting held item. |
| `Nevermeltice` | 33 | Type-boosting held item. |
| `Odd Incense` | 59 | Incense held item. |
| `Poison Barb` | 78 | Type-boosting held item. |
| `Power Anklet` | 63 | EV held item. |
| `Power Band` | 31 | EV held item. |
| `Power Belt` | 68 | EV held item. |
| `Power Bracer` | 102 | EV held item. |
| `Power Herb` | 66 | Held consumable. |
| `Power Lens` | 57 | EV held item. |
| `Power Weight` | 41 | EV held item. |
| `Protec Pads` | 58 | Abbreviated Protective Pads; held battle item. |
| `Psychic Seed` | 55 | Terrain seed. |
| `Punch Glove` | 55 | Abbreviated Punching Glove; held battle item. |
| `Pure Incense` | 97 | Incense held item. |
| `Quick Claw` | 59 | Held battle item. |
| `Quick Powder` | 47 | Species-held item. |
| `Ring Target` | 38 | Held battle item. |
| `Rock Incense` | 106 | Incense held item. |
| `Rocky Helmet` | 55 | Held battle item. |
| `Room Service` | 57 | Held battle item. |
| `Rose Incense` | 36 | Incense held item. |
| `Scope Lens` | 76 | Held battle item. |
| `Sea Incense` | 107 | Incense held item. |
| `Sharp Beak` | 76 | Type-boosting held item. |
| `Shed Shell` | 90 | Held battle item. |
| `Shell Bell` | 82 | Held battle item. |
| `Silk Scarf` | 27 | Type-boosting held item. |
| `SilverPowder` | 92 | Type-boosting held item. |
| `Smooth Rock` | 56 | Weather extender. |
| `Soft Sand` | 87 | Type-boosting held item. |
| `Soothe Bell` | 49 | Held utility/evolution helper. |
| `Soul Dew` | 75 | Species/legendary held item; allowed by current policy override. |
| `Sticky Barb` | 58 | Held battle item. |
| `Terrain Ext.` | 84 | Terrain Extender. |
| `Thick Club` | 74 | Species-held item; already treated as allowed in policy tests. |
| `Ut. Umbrella` | 109 | Abbreviated Utility Umbrella; held battle item. |
| `Wave Incense` | 70 | Incense held item. |
| `Weakness Pol.` | 58 | Abbreviated Weakness Policy; held battle item. |
| `White Herb` | 48 | Held consumable. |
| `Wise Glasses` | 65 | Held battle item. |
| `Zoom Lens` | 106 | Held battle item. |

### ALLOW_EVOLUTION

These look like standard evolution items or evolution-held items. The existing policy intentionally allows normal evolution items, but individual high-impact items can still be balance-reviewed.

| Item | Observed total | Notes |
| --- | ---: | --- |
| `Auspicious-A` | 68 | Auspicious Armor; local CFRU table marks as evolution item. |
| `DeepSeaScale` | 48 | Evolution-held item. |
| `DeepSeaTooth` | 66 | Evolution-held item. |
| `Dragon Scale` | 61 | Evolution item. |
| `Gimmi Coin` | 89 | Local CFRU table marks `ITEM_GIMMIGHOUL_COIN` as evolution item; review currency semantics. |
| `King's Rock` | 87 | Evolution-held item and battle held item. |
| `Leaders Crest` | 127 | Local CFRU table marks as evolution item. |
| `Malicious-A` | 55 | Malicious Armor; local CFRU table marks as evolution item. |
| `Metal Alloy` | 55 | Evolution item. |
| `Metal Coat` | 79 | Evolution-held item. |
| `Peat Block` | 115 | Evolution item. |
| `Syrupy Apple` | 84 | Evolution item. |
| `Upgrade` | 47 | Evolution item. |

### ALLOW_UTILITY

These look like normal utility, healing, or status-support items. They should generally be allowed unless Anton wants a separate low-value filter.

| Item | Observed total | Notes |
| --- | ---: | --- |
| `Fluffy Tail` | 67 | Battle escape utility. |
| `Lava Cookie` | 87 | Food/status recovery. |
| `Paralyz Heal` | 79 | Status recovery. |
| `Poke Doll` | 74 | Battle escape utility. |
| `Safe Guard` | 68 | Ambiguous log spelling; likely Safeguard-style utility. Review exact source name only if it becomes a concern. |

### REVIEW_BALANCE_POWER

These are useful and probably valid data, but they affect progression, abilities, revival, or battle power enough that Anton should decide whether normal Field/Shop/Pickup pools should include them.

| Item | Observed total | Notes |
| --- | ---: | --- |
| `A-Potion` | 48 | Local CFRU source maps to `ITEM_ABILITY_CAPSULE`; party-use ability modifier. |
| `A-Patch` | 50 | Local CFRU source maps to `ITEM_ABILITY_PATCH`; stronger hidden-ability modifier. |
| `Exp. Share` | 75 | Local CFRU item data uses key-item pocket/field use; high progression impact. |
| `Lucky Egg` | 34 | Held EXP multiplier; high progression impact. |
| `Sacred Ash` | 46 | Local CFRU `gItemsByType` maps to revive type; very strong healing/revive reward. |

### REVIEW_ECONOMY

These affect money gain or are sell-value rewards. They are not automatically bad, but they may belong behind an economy/OP review instead of ordinary item pools.

| Item | Observed total | Notes |
| --- | ---: | --- |
| `Amulet Coin` | 44 | Held double-prize effect. |
| `Luck Incense` | 130 | Prize-money incense; same economy concern as Amulet Coin. |
| `Star Piece` | 17 | Sellable money item; lower frequency but economy-relevant. |
| `Stardust` | 82 | Sellable money item. |

### REVIEW_STORY_SYSTEM

These look like story/key/system-like items but are not automatically a ban recommendation from this document. They need source/script context or Anton decision.

| Item | Observed total | Notes |
| --- | ---: | --- |
| `Exp. Share` | 75 | Also listed under balance because CFRU source treats it as key-item pocket field toggle. |
| `Safe Guard` | 68 | Name is ambiguous in the log; review exact local source if it is not normal utility. |

### BAN_RECOMMENDED

These are strong candidates for exclusion from normal Field/Shop/Pickup pools because local CFRU source identifies them as key-item pocket story/unlock items. This is still only a recommendation; no new policy is implied here.

| Item | Observed total | Notes |
| --- | ---: | --- |
| `Rainbow Wing` | 57 | Local CFRU source: key-item pocket, importance `1`, likely legendary/story unlock. |
| `Silver Wing` | 70 | Local CFRU source: key-item pocket, importance `1`, likely legendary/story unlock. |

## Suggested Review Order

1. Decide story/system exclusions first: `Rainbow Wing`, `Silver Wing`, and possibly `Exp. Share` if the key-item field-toggle behavior should not enter normal pools.
2. Decide balance-power items next: `A-Potion`, `A-Patch`, `Lucky Egg`, `Exp. Share`, and `Sacred Ash`.
3. Decide economy items: `Amulet Coin`, `Luck Incense`, `Star Piece`, and `Stardust`.
4. Treat the large `ALLOW_HELD_BATTLE` and `ALLOW_EVOLUTION` groups as likely okay unless Anton wants a separate reward-balance pass.

## Caveats

- This review is based on the current sanitized combined summary and local CFRU source context, not final ROM `ItemData` loaded by Codex.
- Some item names are abbreviated in logs, so exact source identity should be verified locally before a code policy change.
- Static Script/Gift/NPC sources remain out of scope; this review only concerns observed Shop/Pickup summary candidates.
- No P1/support promotion follows from this document.
