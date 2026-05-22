# Item Family Ticket Weighting Design

Status: documentation-only design for a minimal UPR-FVX item weighting model. No ROMs, output ROMs, saves, screenshots, builds, raw logs, private paths, hashes, secrets, or table values were read or documented. No UPR-FVX, CFRU, or DPE code was changed.

## Executive Summary

Anton does not want full category-first sampling with configurable category percentages. That would turn item randomization into a policy-heavy reward-distribution system and would require decisions for healing, balls, evolution items, held items, money items, power items, and many edge categories.

The smaller model is family-ticket weighting: keep the current flat item pool for normal items, but collapse a few large same-purpose variant families into one ticket each. The first target families are Berries and Gems:

- all allowed Berries in the already-filtered pool count as one `BERRY_FAMILY_TICKET`;
- all allowed Gems in the already-filtered pool count as one `GEM_FAMILY_TICKET`;
- every other allowed item remains one item ticket.

This directly addresses the main overrepresentation concern without changing the rest of the randomizer distribution as much as category-first sampling would. The likely first affected pools are Field non-TM items, Shop random filler, and Pickup. Encounter held items are compatible but should be reviewed separately. Trainer held items should stay out of the first pass because sensible held-item logic intentionally uses list weighting for move/species synergy.

## Target Model

Input is the already-filtered candidate pool for a specific randomizer path:

- Ban Bad Items has already selected `getNonBadItems()` instead of `getAllowedItems()` where applicable.
- Mechanic settings have already filtered Mega, Z-Crystal, and Dynamax/GMax items through `filterAllowedMechanicItems(...)`.
- TM/HM and pool-local filters have already run where they currently run.
- Shop-only filters such as Ban Regular Shop Items, Ban OP Shop Items, and guaranteed item removal have already run.

Transformation:

1. Split the candidate pool into `berries`, `gems`, and `otherItems`.
2. Remove every allowed Berry from the top-level ticket pool and insert exactly one `BERRY_FAMILY_TICKET` if `berries` is not empty.
3. Remove every allowed Gem from the top-level ticket pool and insert exactly one `GEM_FAMILY_TICKET` if `gems` is not empty.
4. Keep all `otherItems` as individual item tickets.

Draw:

- Normal item ticket -> return that item directly.
- `BERRY_FAMILY_TICKET` -> choose one item uniformly from the already-filtered `berries` list.
- `GEM_FAMILY_TICKET` -> choose one item uniformly from the already-filtered `gems` list.

The family draw must not re-add banned or mechanic-filtered items. The family contents are exactly the items that survived the existing pool filters.

## Pool-Specific Analysis

| Pool | Current flat behavior | Family-ticket applicability | Risks | Recommendation |
| --- | --- | --- | --- | --- |
| Field non-TM items | `randomizeNonTMFieldItems()` builds `possible` from allowed/non-bad items, mechanic-filters it, removes TMs, then uses either `possible.get(random.nextInt(size))` or a shuffled refill stack. | Strong fit. Berries/Gems are normal reward-family variants and currently each surviving item is one ticket. | `RANDOM_EVEN` must cycle over top-level tickets, not individual Berries/Gems; unique no-sell Mega-stone removal must happen after ticket resolution if still relevant. | First implementation target with ROM-free tests for `RANDOM` and `RANDOM_EVEN`. |
| Shop random filler | `setupPossible()` filters allowed/non-bad items, mechanic items, TMs, regular-shop and OP-shop removals, then `setupNewItems()` uses a shuffled refill stack over individual items. | Strong fit for filler items after guarantees are removed. | Guaranteed evolution/X items must not be collapsed; placement shuffles should receive resolved concrete items, not ticket objects, unless the ticket model is internal-only. | First implementation target, after Field, preserving guarantee handling. |
| Pickup | `randomizePickupItems()` filters allowed/non-bad items, mechanic items, removes TMs, then chooses a flat item for each pickup row while copying original probability slots. | Strong fit. It reduces Berry/Gem row dominance without changing pickup probability tiers. | Runtime pickup probabilities still come from copied table slots; family-ticket only changes which item occupies a row. | First implementation target with explicit probability-slot preservation test. |
| Encounter held items | `EncounterHeldItemRandomizer` filters allowed/non-bad/mechanic items, removes unsafe held items, then flat-picks for guaranteed/common/rare/dark-grass slots. | Technically compatible, especially because Berries/Gems are held-item-like families. | This pool has extra slot-type probabilities and common/rare duplication avoidance; it is gameplay-facing differently from reward pools. | Review after Field/Shop/Pickup. Do not include in first fix unless Anton explicitly wants it. |
| Trainer held items | `randomizeHeldItem()` picks from sensible held lists or held-item fallback lists; Gen3 sensible held items can intentionally add duplicate items for move/species synergy. | Possible only for fallback all-held pools, not sensible lists. | Collapsing Berries/Gems can fight intentional sensible-item weighting and unique-held retries. | Exclude from first design. Treat as separate held-item policy if ever requested. |

## Family Definition

| Family | Detection source | Confidence | Caveats |
| --- | --- | --- | --- |
| Berries | Best: source-backed item type metadata such as local CFRU/DPE `gItemsByType` `ITEM_TYPE_BERRY` if made available to UPR-FVX. Conservative fallback: canonical UPR/FVX Berry ID ranges such as `cheriBerry..rowapBerry` plus modern additions `roseliBerry..marangaBerry`, paired with exact known names. | High if source-backed type is available; Medium with ID/name fallback. | Do not catch `Berry Juice`, `Berry Sweet`, `Berry Pots`, `Berry Pouch`, or Let's Go silver/golden berry variants unless Anton explicitly wants them in the family. Name-only `endsWith("Berry")` is risky for custom/localized rows. |
| Gems | Best: source-backed item type metadata such as `ITEM_TYPE_GEM`. Conservative fallback: canonical type Gem IDs `fireGem..normalGem` plus `fairyGem`, paired with exact type-gem names. | High for source-backed type or canonical IDs; Medium with names. | Avoid broad `*Gem` matching because non-type gems or valuables can exist, e.g. `Star Gem` style constants. Only type-boosting Gems should be in `GEM_FAMILY_TICKET`. |

Current code notes:

- `Item` has only `allowed`, `bad`, `tm`, and mechanic categories; it has no general item-type enum.
- `CfruDpeItemCategories` currently classifies mechanic/form-change families, not Berries or Gems.
- `CfruDpeItemPoolPolicy` has `USEFUL_BERRY_IDS` for Ban-Bad overrides and tests keep `Fire Gem` allowed, but these are not full family classifiers.
- A future implementation should add explicit Berry/Gem predicates or item-family metadata instead of deriving families ad hoc in each randomizer method.

## Not Bundled For Now

- Balls: capture strength and shop OP filtering are separate balance questions; Master Ball policy should not be hidden inside a family ticket.
- Evolution Items: availability affects progression and team planning; shop guarantees also handle them separately.
- Held Battle Items generally: too broad and power-diverse; Trainer held pools already have their own logic.
- Healing: core reward category with clear item-to-item progression; collapsing it would materially change reward pacing.
- X Items: battle consumables are valid but balance-sensitive; no clear overlarge variant-family problem comparable to Berries/Gems.
- Money Items: economy impact needs explicit policy, not family dedupe.
- Plates, Memories, Drives, Nectars, and related form-change items: current policy already bans or gates them through Ban-Bad/mechanic logic; do not add another weighting layer first.
- TMs: normal Field/Shop/Pickup pools remove TMs; Field TM slots are intentionally separate and should stay separate.

## RNG / Reproducibility

This model changes seed results, but it remains deterministic for a fixed seed, candidate order, and implementation. It should be treated as a behavioral randomization change, not a bug fix.

Implementation guidance:

- Build family tickets from a stable ordered list after current filters. Prefer list order that already exists in the caller, or sort by `Item.getId()` if converting from a `Set`.
- Resolve a family ticket with the same `Random` instance by choosing uniformly from that family list.
- For `RANDOM`, a draw consumes one top-level ticket draw, plus a second draw only if the ticket is a family ticket. That is deterministic but will shift later RNG values compared with current flat selection.
- For Field `RANDOM_EVEN`, the refill stack should contain top-level tickets. If a family ticket is popped multiple cycles, each pop resolves to a fresh random member of the family.
- For Shop random filler, the shuffled refill stack should also contain top-level tickets. `newItems` should hold resolved concrete items before `placeNewItems(...)` shuffles and places them.
- For Pickup, copy the original pickup probability slots exactly as today; family-ticket sampling only changes the selected item for that row.
- If a family has only one allowed item, using a family ticket is equivalent in top-level probability but consumes a nested RNG draw. Prefer the `> 1 allowed item` option below to reduce unnecessary seed churn.

## Implementation Options

| Option | Pros | Cons | Recommendation |
| --- | --- | --- | --- |
| Internal always-on for CFRU/DPE item pools | No new UI/settings complexity; fixes the observed family-ticket issue directly for the target hack profile. | Changes legacy seed behavior without an opt-out; needs clear documentation. | Reasonable if Anton wants this as the new CFRU/DPE workspace default. |
| Option/toggle later | Preserves legacy flat behavior and allows comparison. | Adds Settings, GUI, profile, and test-matrix work for a small feature. | Defer unless Anton wants user-facing control. |
| Only Field+Shop+Pickup | Targets normal reward pools and avoids held-item policy complexity. | Encounter-held Berries/Gems remain flat. | Preferred first scope. |
| Include Encounter held items too | Consistent across wild held item rewards. | More gameplay semantics and duplicate/common/rare behavior to verify. | Optional second scope after normal pools. |
| Family tickets only when family has more than 1 allowed item | Avoids extra RNG consumption and no-op tickets for singleton families. | Slightly more branching in helper code. | Recommended. |

## Recommendation

Implement nothing yet without Anton approval.

If Anton approves, start with Field non-TM, Shop random filler, and Pickup only. Apply family tickets after all existing filters and before the final selection/refill-stack step. `RANDOM_EVEN` is compatible if the shuffled refill stack contains top-level tickets, not individual family members. Shop is compatible if tickets are resolved before concrete items are placed into shops. Pickup is compatible if probability tiers remain copied exactly as today.

Required tests for a later code PR:

- ROM-free family classifier tests for canonical Berry and Gem IDs/names, including negative cases such as `Berry Juice`, `Berry Sweet`, `Berry Pouch`, and non-type `Star Gem`-style names.
- Field `RANDOM` test proving many Berries collapse to one top-level ticket while unrelated items keep one ticket each.
- Field `RANDOM_EVEN` test proving refill cycles operate over top-level tickets and family members are resolved inside the family.
- Shop filler test proving guaranteed items are not family-ticketed and placement receives concrete items.
- Pickup test proving probability slots are preserved while family-ticket selection resolves to concrete items.
- Regression tests that TMs, mechanic-gated items, banned form-change items, and Ban-Bad removals still happen before family-ticket construction.

## Follow-Up Work Package

If Anton approves the design:

- `fix/item-family-ticket-sampling`
