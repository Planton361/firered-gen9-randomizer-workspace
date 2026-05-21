# CFRU/DPE Item Policy Ban Audit

Status: documentation-only audit from current UPR-FVX code, local workspace docs, ROM-free tests, and UPR-FVX git history. No ROMs were read, copied, generated, or tested. No builds were run. No UPR-FVX, CFRU, or DPE code was changed.

## 1. Executive Summary

The current CFRU/DPE Item-Pool policy bans or excludes items through four different mechanisms:

- Hard bans during `Gen3RomHandler.loadItems()`: legacy Gen3 banned items, HMs, fallback/invalid CFRU/DPE names, fossils, and review-gap system items such as `Light Stone`, `Dark Stone`, `Sun Flute`, `Moon Flute`, `Rusted Sword`, `Rusted Shield`, `Odd Keystone`, `Bottle Cap`, and `Gold Bottle Cap`.
- Ban-Bad-only bans: items stay loaded but are excluded from normal Field/Shop/Pickup candidate pools when the matching Ban Bad Items option is active. This covers Shards, high-value/relic valuables, Apricorns/Aprikokos, Plates, Drives, Silvally Memories, Nectars, Gracidea, DNA Splicers, Reveal Glass, Prison Bottle, N-Solarizer/N-Lunarizer, Reins of Unity, and selected legendary orbs.
- Mechanic-setting gates: Mega Stones/accessories, Z-Crystals/accessories, and Dynamax/GMax items are excluded unless their existing Include setting is enabled.
- Pool-local filters: normal Field non-TM, Shop random filler, and Pickup pools remove `Item::isTM`; TM field slots remain separate.

Anton-confirmed policy decisions in the current code include: no TMs/HMs in normal pools; fossils banned; Shards and high-value/relic valuables banned when Ban Bad Items is active; Apricorns banned when Ban Bad Items is active; Mega/Z/Dynamax-GMax controlled by Include settings; and the review-gap hard bans for Light/Dark Stone, Sun/Moon Flute, Rusted Sword/Shield, Odd Keystone, Bottle Cap, and Gold Bottle Cap.

Codex-derived policy is strongest around broad form-change grouping. Plates, Drives, Memories, Nectars, DNA Splicers, Reveal Glass, Prison Bottle, N-Solarizer/N-Lunarizer, Reins of Unity, and legendary orbs are treated as Ban-Bad form/system items. That is technically consistent with the current category predicates, but it is the main area where a useful item could have been over-banned from normal rewards.

Potentially too aggressive current bans are: Bottle Caps, Odd Keystone, Sun/Moon Flute, Apricorns, Shards, Rusted Sword/Shield, Gracidea/form-change items, Light/Dark Stone, and high-value valuables. These are not code bugs by themselves; they are design decisions that may need Anton review if a later gameplay policy wants them as rewards.

## 2. Ban Source Per Category

| Category / Item family | Current outcome | Ban source | Anton decision? | Codex-derived? | Reason | Review priority |
| --- | --- | --- | --- | --- | --- | --- |
| invalid/placeholder/fallback names | Excluded from normal pools | HARD_BANNED | no direct Anton item-by-item decision | no | `Gen3RomHandler.loadItems()` marks CFRU/DPE fallback names disallowed/bad. | Low |
| legacy Gen3 key/progression unique items | Excluded if covered by Gen3 unique range | LEGACY_FVX_BAD / HARD_BANNED | no | no | `Gen3Constants.bannedItems` covers Gen3 unique/key-style item range. | Medium |
| HMs | Excluded | HARD_BANNED | ANTON_CONFIRMED | no | HMs are globally banned by `Gen3Constants.bannedItems`. | Low |
| TMs from normal pools | Excluded from normal Field/Shop/Pickup; still allowed in TM slots | HARD_BANNED pool-local filter | ANTON_CONFIRMED | no | Vanilla and expanded CFRU/DPE TMs are marked `Item::isTM`; normal pools remove TMs. | Low |
| fossils | Excluded even without Ban Bad | HARD_BANNED | ANTON_CONFIRMED | partly | `CfruDpeItemPoolPolicy.isFossilItem()` feeds `isBannedFromNormalItemPools()`. | Low |
| shards/exchange items | Excluded only when Ban Bad Items is active | BAN_BAD_ONLY | ANTON_CONFIRMED | no | Anton update after Green Shard smoke; `isShardExchangeItem()`. | Medium |
| relic/high-value valuables | Excluded only when Ban Bad Items is active | BAN_BAD_ONLY | ANTON_CONFIRMED | partly | Anton update after Relic Crown smoke; includes Big Nugget, Balm Mushroom, Pearl String, Comet Shard, Rare Bone. | Medium |
| apricorns/aprikokos | Excluded only when Ban Bad Items is active | BAN_BAD_ONLY | ANTON_CONFIRMED | partly | Anton smoke found Apricorns unwanted without Apricorn-ball mechanic scope. | Medium |
| memories / `* Mem.` | Excluded only when Ban Bad Items is active | BAN_BAD_ONLY | ANTON_CONFIRMED for smoke examples | partly | Form-change policy catches Silvally Memory full and abbreviated names. | Medium |
| plates | Excluded only when Ban Bad Items is active | BAN_BAD_ONLY | REVIEW | CODEX_DERIVED | Broad form-change policy catches Arceus Plates. | Medium |
| drives | Excluded only when Ban Bad Items is active | BAN_BAD_ONLY | REVIEW | CODEX_DERIVED | Broad form-change policy catches Genesect Drives. | Medium |
| nectars | Excluded only when Ban Bad Items is active | BAN_BAD_ONLY | REVIEW | CODEX_DERIVED | Broad form-change policy catches Oricorio Nectars. | Medium |
| Gracidea | Excluded only when Ban Bad Items is active | BAN_BAD_ONLY | ANTON_CONFIRMED | partly | Current `CfruDpeItemCategories` treats Gracidea as nectar/form-change. | Medium |
| Light Stone / Dark Stone | Excluded even without Ban Bad | HARD_BANNED | ANTON_CONFIRMED | no | Review-gap hard-ban from Anton decisions. | Low |
| Sun Flute / Moon Flute | Excluded even without Ban Bad | HARD_BANNED | ANTON_CONFIRMED | no | Review-gap hard-ban from Anton decisions. | Medium |
| Red/Blue/Black/White/Yellow Flute | Not explicitly banned by current CFRU/DPE policy | REVIEW | no current confirmation found | no | `CfruDpeItemPoolPolicy` only lists Sun/Moon Flute; old flutes may pass unless legacy flags mark them bad in final data. | High |
| Rusted Sword / Rusted Shield | Excluded even without Ban Bad | HARD_BANNED | ANTON_CONFIRMED | no | Review-gap hard-ban from Anton decisions. | Medium |
| Odd Keystone | Excluded even without Ban Bad | HARD_BANNED | ANTON_CONFIRMED | no | Review-gap hard-ban from Anton decisions. | Medium |
| Bottle Cap / Gold Bottle Cap | Excluded even without Ban Bad | HARD_BANNED | ANTON_CONFIRMED | no | Review-gap hard-ban from Anton decisions. | High |
| Shiny Charm / Oval Charm | Not explicitly banned by current CFRU/DPE policy | REVIEW | no current confirmation found | no | Present in local constants, but not in review-gap or form-change predicates. | High |
| Magma Stone | Not explicitly banned by current CFRU/DPE policy | REVIEW | no current confirmation found | no | Present in local constants, but not in review-gap or form-change predicates. | High |
| Mega Stones/accessories | Mechanic-setting-gated | MECHANIC_SETTING | ANTON_CONFIRMED | no | `ItemMechanicPredicates.isItemAllowed()` excludes unless Include Mega Items is on. | Low |
| Z-Crystals/accessories | Mechanic-setting-gated | MECHANIC_SETTING | ANTON_CONFIRMED | no | Z names/source IDs are excluded unless Include Z-Crystal Items is on. | Low |
| Dynamax/GMax items | Mechanic-setting-gated | MECHANIC_SETTING | ANTON_CONFIRMED | no | Dynamax/GMax items are excluded unless Include Dynamax/GMax Items is on. | Low |
| legacy FVX bad items: mail, many berries, contest scarves, Shoal/Shards | Excluded when Ban Bad Items is active | LEGACY_FVX_BAD | inherited | no | `Gen3Constants.getBadItems()` applies old Gen3 bad-item flags. | Medium |

## 3. Explicitly Banned Groups

| Group | Current code behavior | Evidence |
| --- | --- | --- |
| invalid/placeholder | Fallback names are set `allowed=false` and `bad=true`. | `Gen3RomHandler.loadItems()` and `readItemNameOrFallback()` path. |
| key/progression | Legacy Gen3 unique/key range is banned; custom CFRU/DPE key-like items are only covered where explicit predicates/ranges exist. | `Gen3Constants.bannedItems`; `CfruDpeItemPoolPolicy` review-gap set. |
| HMs | Banned globally. | `Gen3Constants.setupBannedItems()` adds `hm01..hm08`. |
| TMs from normal pools | Removed from normal Field non-TM, Shop random filler, and Pickup pools. | `ItemRandomizer.randomizeNonTMFieldItems()`, `setupPossible()`, `randomizePickupItems()`. |
| fossils | Hard-banned from normal pools, independent of Ban Bad. | `CfruDpeItemPoolPolicy.isBannedFromNormalItemPools()`; `CfruDpeItemPoolPolicyTest.fossilsAreBannedFromNormalItemPools`. |
| shards/exchange items | Ban-Bad-only. | `isShardExchangeItem()`; tests cover Red/Blue/Yellow/Green Shard. |
| relic/high-value valuables | Ban-Bad-only. | `isHighValueValuableItem()`; tests cover Relic Crown/Statue/Band/Gold/Vase/Copper/Silver, Big Nugget, Balm Mushroom, Pearl String, Comet Shard, Rare Bone. |
| apricorns | Ban-Bad-only. | `isApricornItem()`; tests cover full, abbreviated, and Aprikoko variants. |
| memories | Ban-Bad-only. | `CfruDpeItemCategories.isSilvallyMemory()`; tests cover `Flying Mem.`, `Flying Memory`, and `Fire Mem.`. |
| plates | Ban-Bad-only. | `isArceusPlate()`. |
| drives | Ban-Bad-only. | `isGenesectDrive()`. |
| nectars | Ban-Bad-only. | `isNectarOrFormChangeItem()`. |
| Gracidea | Ban-Bad-only. | `ITEM_GRACIDEA` source ID and name are in nectar/form-change category. |
| Light Stone / Dark Stone | Hard-banned from normal pools. | Review-gap hard-ban set and tests. |
| Sun Flute / Moon Flute | Hard-banned from normal pools. | Review-gap hard-ban set and tests. |
| Red/Blue/Black/White/Yellow Flute | Not explicitly banned by the current CFRU/DPE policy. | `CfruDpeItemPoolPolicy` does not list these names/IDs; analyzer flags `flute` heuristically only. |
| Rusted Sword / Rusted Shield | Hard-banned from normal pools. | Review-gap hard-ban set and tests. |
| Odd Keystone | Hard-banned from normal pools. | Review-gap hard-ban set and tests. |
| Bottle Cap / Gold Bottle Cap | Hard-banned from normal pools. | Review-gap hard-ban set and tests. |
| Shiny Charm / Oval Charm | Not explicitly banned by the current CFRU/DPE policy. | Local constants exist; no matching current predicate found. |
| Magma Stone | Not explicitly banned by the current CFRU/DPE policy. | Local constant exists; no matching current predicate found. |
| Mega Stones when Include Mega OFF | Mechanic-setting blocked. | `ItemMechanicPredicatesTest.megaStonesAndAccessoriesAreMegaMechanicItems`. |
| Z-Crystals when Include Z OFF | Mechanic-setting blocked. | `ItemMechanicPredicatesTest.zCrystalsAndAccessoriesAreZMechanicItems`. |
| Dynamax/GMax when Include Dynamax/GMax OFF | Mechanic-setting blocked. | `ItemMechanicPredicatesTest.dynamaxAndGigantamaxItemsUseTheirOwnMechanicCategory`. |

Git history confirms the policy was introduced incrementally through UPR-FVX commits `5c868c57` (expanded TM classification), `10a02f77` (central CFRU/DPE item-pool policy), `16d42d1b` (Mega name coverage), `a26cbb47` (economy/exchange junk), `d7ffd86b` (Memories/Apricorns/Fossils/Shards/high-value coverage), `f8d99453` (Z-Crystal name variants), and `b51478b1` (review-gap hard bans).

## 4. Potentially Too Aggressive Bans

| Item / Category | Warum gebannt | Warum eventuell sinnvoll | Empfehlung |
| --- | --- | --- | --- |
| Bottle Cap / Gold Bottle Cap | Anton review-gap hard ban. | Could be useful if the hack has IV-changing or late-game reward semantics. | RECONSIDER |
| Odd Keystone | Anton review-gap hard ban. | Could be a Spiritomb-related reward or encounter key depending custom script design. | NEEDS_INGAME_CONTEXT |
| Sun/Moon Flute | Anton review-gap hard ban. | Could matter if Alola legendary/form content is intentionally reachable. | NEEDS_INGAME_CONTEXT |
| Red/Blue/Black/White/Yellow Flute | Not currently explicitly banned by code; analyzer marks flute-like names suspicious. | Old flutes may be harmless reusable utility rather than progression blockers. | RECONSIDER |
| Shiny Charm / Oval Charm | Not currently explicitly banned by code. | If they appear, they may be powerful meta-progression items rather than useless junk. | NEEDS_INGAME_CONTEXT |
| Magma Stone | Not currently explicitly banned by code. | Could be story-only, but local context alone does not prove how the hack uses it. | NEEDS_INGAME_CONTEXT |
| Apricorns | Ban-Bad-only. | Could be meaningful if Apricorn Ball crafting or exchange NPCs are implemented. | MAKE_OPTIONAL_LATER |
| Shards | Ban-Bad-only. | Could be useful if tutor/exchange NPCs are present. | MAKE_OPTIONAL_LATER |
| Rusted Sword / Rusted Shield | Anton review-gap hard ban. | Could be legitimate held/form items if Zacian/Zamazenta mechanics are supported. | MAKE_OPTIONAL_LATER |
| Gracidea | Ban-Bad-only form-change item. | Could be legitimate if Shaymin form handling is supported and desired. | MAKE_OPTIONAL_LATER |
| Light Stone / Dark Stone | Anton review-gap hard ban. | Could be used as story/form unlocks, but random rewards could break progression or be useless. | KEEP_BANNED |
| high-value valuables | Ban-Bad-only. | They can be valid economy rewards, but Relic/Big Nugget class items can distort money balance. | MAKE_OPTIONAL_LATER |
| Plates/Drives/Memories/Nectars/form-change items | Ban-Bad-only broad form-change policy. | Some are held battle modifiers or form unlocks that can be meaningful for specific species. | MAKE_OPTIONAL_LATER |
| evolution items, excluding story/form/key-like items | Generally allowed. | This is intentionally not over-banned; only fossil/story/form-like subsets are blocked. | KEEP_BANNED only for the story/form subset |

## 5. Allowed Groups That Intentionally Stay Allowed

These groups remain allowed by current policy unless a separate optional shop-only filter removes them:

- Healing/status items: `Potion`, `Super Potion`, `Full Restore`, `Antidote`, PP recovery, and similar medicines.
- Balls including `Master Ball`: current Anton policy keeps balls reward-eligible.
- `Rare Candy`, `PP Up`, and Vitamins: allowed; `Rare Candy` can still be removed from shop filler by optional OP-shop filtering.
- X Items and battle consumables: `X Defend` is test-covered as allowed.
- Held battle items: `Leftovers`, `Choice Band`, `Life Orb`, and similar held items are not banned by the new CFRU/DPE policy.
- Gems and `Eviolite`: explicitly test-covered as allowed.
- Modern held/battle items: examples such as `Wide Lens`, `Throat Spray`, `Clear Amulet`, and `Punching Glove` are intended to stay allowed unless Anton changes policy.
- Normal utility items: `Escape Rope`, Repels, and similar non-progression utility are allowed.
- Evolution items: stones and normal evolution items stay allowed; story/form/key-like exceptions are handled separately.
- Lower-value sell items: `Nugget`, `Pearl`, `Tiny Mushroom`, and `Big Mushroom` are not part of the high-value valuable ban, though shop OP filtering can remove some shop candidates.

## 6. Analyzer Heuristic Review

The batch analyzer in `07_scripts/randomizer/item_pool_batch_analyzer.py` is intentionally heuristic. It is useful for finding suspicious log entries, but it is not the exact UPR-FVX policy engine.

Likely false positives or overflags:

- `Blk Augurite` can be flagged as a Mega Stone because `is_mega_stone_name()` treats most names ending in `ite` as suspicious. That suffix rule is too broad.
- `Flame Orb`, `Toxic Orb`, and `Adrenal Orb` can be flagged by the generic `orb` marker, even though Orb-style held battle items may be valid allowed rewards.
- `Red Card` can be flagged by the generic `card` marker, but it is a normal held battle item in modern games.
- `Hard Stone` can be flagged by the generic `stone` marker, but it is a regular held type-boosting item.
- `Absorb Bulb` is not clearly covered by the allow whitelist; it should likely be treated like other held battle items rather than suspicious.

Likely false negatives or weak catches:

- `Charzardite X/Y` should be suspicious when Include Mega Items is off, but the analyzer known-name set covers canonical `Charizardite X/Y` spelling, not the misspelled `Charzardite` variant. The broad `ite` suffix also does not catch `...itex` / `...itey` misspellings reliably.
- Any localized/custom form or system item outside the current exact-name set can remain `UNKNOWN` instead of suspicious.
- Old flutes and charm-like items are heuristic-only. The analyzer may flag them, but current UPR-FVX policy does not explicitly ban every such item.

Recommended analyzer-only follow-up, if chosen later:

- Replace the broad `endswith("ite")` Mega heuristic with a stricter known-name list plus specific known localized variants.
- Add explicit allow-list entries for common held/battle items: `Flame Orb`, `Toxic Orb`, `Absorb Bulb`, `Adrenal Orb`, `Red Card`, and `Hard Stone`.
- Add known misspellings/log variants only where they have been observed, such as `Charzardite X/Y`.
- Keep analyzer output labelled as `policy_guess`, not authoritative ban proof.

## 7. Next Decision

Recommended next step: Anton review of the potentially too aggressive bans before another UPR-FVX policy change.

Smallest review packet: decide whether `Bottle Cap`/`Gold Bottle Cap`, `Odd Keystone`, old flutes, Apricorns, Shards, high-value valuables, and form-change items should stay banned, become optional later, or be allowed in normal Field/Shop/Pickup pools. After that decision, a separate small analyzer-heuristic PR can reduce false positives without changing randomizer behavior.
