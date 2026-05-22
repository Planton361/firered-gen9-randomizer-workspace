# Randomizer Pool Weighting Review

Status: documentation-only review of current UPR-FVX code and existing sanitized reports. No ROMs, output ROMs, saves, screenshots, builds, raw logs, private paths, hashes, secrets, or CFRU/DPE table values were read or documented. No UPR-FVX code was changed.

## Executive Summary

- Pokemon randomization currently selects from `SpeciesSet` candidate pools. `SpeciesSet.getRandomSpecies(Random)` builds a flat cache from the set and chooses one entry by `random.nextInt(randomCache.size())`.
- Forms that survive `RestrictedSpeciesService`, special-form filters, and feature-specific bans are therefore separate candidate entries. There is no observed base-species dedupe or species-family bucket before the final pick.
- Unown or any other many-form species can be overrepresented if those forms are modeled as distinct `Species` entries and are allowed by the current settings. This review found no Unown-specific weighting exception outside a Catch Em All wild-encounter comment.
- Regional Forms are also separate `Species` entries when allowed. That appears intentional from the current Gen-limit / regional-form option design, but it still means separate tickets in flat form-enabled pools.
- Items in Field non-TM, Shop random filler, Pickup, Encounter held items, and non-sensible Trainer held fallback are selected flat per eligible item. Shop random filler and Field `RANDOM_EVEN` use shuffled refill stacks, which gives even cycling over individual items, not category buckets.
- Berries, Gems, held battle items, evolution items, Balls, and other large item families can be overrepresented at the family/category level because each surviving item is an individual ticket. Current filters decide eligibility, not family-level weighting.
- Exception: `Gen3RomHandler.getSensibleHeldItemsFor(...)` can intentionally insert duplicate item IDs for move/species synergy. Trainer sensible held items are therefore list-weighted by heuristic candidates, not purely unique-item flat.

## Pokemon Pool Weighting

| Feature | Codepfad | Kandidatenbasis | Formbehandlung | Risiko | Empfehlung |
| --- | --- | --- | --- | --- | --- |
| Shared species pick | `SpeciesSet.getRandomSpecies(...)` | `SpeciesSet` entries after caller filters | Flat per `Species` object in the set; no base-species bucket | Any multi-form species gains more tickets when forms are included | Treat as current baseline; design a separate weighting option before changing behavior. |
| Wild Pokemon | `WildEncounterRandomizer.randomizeEncounters()` -> `rSpecService.getSpecies(...)` -> `pickReplacement(...)` | Allowed species/forms minus wild bans, asset guard, local/type/evo filters | `allowWildAltFormes` controls inclusion; cosmetic replacements excluded through service call; later pick is flat | Form-heavy species can be overrepresented inside each filtered area/type/BST pool | Audit form-heavy species counts before changing; consider base-species-first only for specific form families. |
| Trainer Pokemon | `TrainerPokemonRandomizer.randomizeTrainerPokes()` -> `cachedAll` / `cachedByType` -> `pickTrainerPokeReplacement(...)` | Allowed species/forms minus trainer bans, local/type/diversity/evo filters | `allowTrainerAlternateFormes` controls inclusion; banned/irregular/ability-dependent forms removed; final pick flat unless similar-strength narrows first | Flat forms affect normal, local, type-themed, distributed, and type-weighted pools; type weighting also counts form entries by type | Keep eligibility filters; if changing weighting, preserve trainer type/diversity behavior explicitly. |
| Starters | `StarterRandomizer.randomizeStarters()` -> `getAvailableSet(...)` -> `chooseStartersBasic(...)` / type-triangle helpers | Allowed starter species/forms minus custom starters, legendary, dual-type, basic/tri-stage/BST filters | `allowStarterAltFormes` includes alt forms; cosmetic and actually-cosmetic forms removed; final pick flat from `SpeciesSet` | Starter pool can favor multi-form species when starter alt forms are enabled | Review starter-specific toggle separately; do not silently collapse Regional Forms. |
| Static Pokemon | `StaticPokemonRandomizer.randomizeStaticPokemon()` | Legendary/nonlegendary/UB/all pools from `RestrictedSpeciesService` plus static bans and restricted pools | `allowStaticAltFormes` includes forms; cosmetic replacements filtered in form-enabled paths; final pick flat or similar-strength flat within narrowed pool | Static replacement can favor multi-form species; restricted static pools may reduce this locally | Include in future species-form audit, but no immediate code fix from docs-only evidence. |
| Rival Counter-Starter / Rival carries starter | `GameRandomizer` around starter/trainer flow; `TrainerPokemonRandomizer.makeRivalCarryStarter()`, `makeFirstRivalCarryStarter()` | Already selected starter trio from `romHandler.getStarters()` | Does not draw a new global pool during carry/counter sync; it chooses starter offsets and evolutions | Weighting is inherited from Starter selection, not introduced by Rival carry logic | Document as inherited risk only. A Rival-specific weighting fix does not appear needed. |
| Gen Limit 1-9 | `RestrictedSpeciesService.setRestrictions(...)`, `SpecialFormPredicates.isAllowedByGeneration(...)` | Species/forms passing generation and special-form options | Eligibility filter only; no weighting or dedupe | Regional override can include regional branches by base-family generation, but still as separate form entries | Keep as eligibility logic; do not treat Gen Limit as weighting control. |
| Special / Regional / Mega / GMax / Irregular filters | `SpecialFormPredicates`, `RestrictedSpeciesService`, feature-specific `getIrregularFormes()` bans | Full species incl. formes, filtered by settings | Mega/GMax/Irregular are filtered by options; Regional Forms have explicit generation semantics | Filters can remove categories, but surviving categories are still flat tickets | Future weighting design should reuse these filters before sampling. |
| Unown specifically | No Unown-specific picker found; wild code has a Catch Em All comment mentioning Unown/banned species | Whatever Unown entries are present in `getSpeciesSetInclFormes()` and pass filters | No observed base-species collapse for Unown forms | If Unown letters are separate `Species` entries and allowed, Unown can be overrepresented | Add `analysis/species-form-weighting-audit` to count form-heavy candidates from sanitized metadata before any fix. |
| Rotom / Arceus / Silvally / Alcremie / Minior / similar | General alternate-form paths above | Distinct `Species` entries where modeled and allowed | No family/category bucket observed | Any large allowed form family can be overrepresented; some forms may be excluded as cosmetic, irregular, ability-dependent, or asset-unsafe | Classify by exact loaded form metadata in a follow-up audit; keep Regional Forms separate by default unless Anton decides otherwise. |

Answers from code:

- Current selection is by `Species` entry, not by base species.
- `Species.getBaseNumber()` / `getBaseForme()` exist and are used for evolution/family logic, bans, and some load checks, but not as a general random sampling bucket.
- No category/family-level species sampling layer was found for Wild, Trainer, Starter, Static, or Rival starter carry.
- Similar-strength modes first narrow a `SpeciesSet` by BST window, then still choose flat inside that narrowed set.

## Item Pool Weighting

| Pool | Codepfad | Kandidatenbasis | Gewichtung | Risiko | Empfehlung |
| --- | --- | --- | --- | --- | --- |
| Field non-TM items | `ItemRandomizer.randomizeFieldItems()` -> `randomizeNonTMFieldItems()` | `getNonBadItems()` or `getAllowedItems()`, then mechanic filter, then remove `Item::isTM` | `RANDOM`: flat `possible.get(random.nextInt(size))`; `RANDOM_EVEN`: shuffled refill cycle over individual items | Berries/held/evolution/utility families with many entries can dominate category-level distribution | Consider category-first sampling for a later feature, especially Field rewards. |
| TM field slots | `randomizeTMFieldItems()` | Required field TMs plus unique TM fillers from item lists/current slots | Shuffled unique TM filler list, then sublist | Not a Berry/held-item issue; TM slots intentionally stay TM slots | Keep separate from normal item-weighting design. |
| Shop random filler | `randomizeShopItems()` -> `setupPossible()` -> `setupNewItems()` | `getNonBadItems()` or `getAllowedItems()`, mechanic filter, remove TMs, optional regular/OP shop bans, guaranteed items removed from filler | Shuffled refill stack over individual eligible filler items | Large item families recur across shop slots/runs; guaranteed evolution/X items are separate injection | Category-first shop filler is a viable later feature, but must preserve guarantees. |
| Shop shuffle | `shuffleShopItems()` | Existing special-shop contents only | `Collections.shuffle` of existing items | Does not prove random filler candidate eligibility; any pre-existing family skew is preserved | Document separately; do not use shuffle observations as filler-pool proof. |
| Pickup | `randomizePickupItems()` | `getNonBadItems()` or `getAllowedItems()`, mechanic filter, remove TMs | Flat `possibleItems.get(random.nextInt(size))` per pickup table row; existing probability slots are copied | Large families can fill many pickup rows; gameplay probability also depends on copied pickup slot probabilities | Category-first sampling may help, but design must respect pickup table probability tiers. |
| Trainer held items | `TrainerPokemonRandomizer.randomizeHeldItem()` | `getSensibleHeldItemsFor(...)`, fallback `getAllConsumableHeldItems()` / `getAllHeldItems()` | Final pick is `toChooseFrom.get(random.nextInt(size))`; sensible candidate lists may contain intentional duplicates | Sensible mode can weight Liechi/Petaya/type boosters/species items by heuristics; all-held fallback is flat per item | Do not collapse until held-item design decides whether heuristic duplicates are desired. |
| Encounter held items | `EncounterHeldItemRandomizer.randomizeWildHeldItems()` | `getNonBadItems()` or `getAllowedItems()`, mechanic filter, remove null/fallback names, TMs, Poke Balls | Flat item pick for guaranteed/common/rare/dark-grass slots; slot presence probabilities are separate | Berries/held items can be common because every surviving item is a ticket | If category-first is added, decide separately for encounter-held pools. |

Answers from code:

- Normal item pools do not have category buckets today.
- OP, sensible, Ban-Bad, mechanic, TM, Poke Ball, regular-shop, and guaranteed-item filters run before the relevant draw, except Shop shuffle, which has no new candidate draw.
- `CfruDpeItemPoolPolicy` recognizes useful berries and some held battle items as allowed under Ban-Bad; this controls eligibility only.
- Trainer sensible held item generation is the one reviewed item path where duplicate list entries can deliberately change probability.

## Observed Batch Evidence

Existing sanitized item reports fit the flat-pool interpretation:

- `item-pool-unknown-review.md` describes a sanitized 1000-run combined item summary with 259 item rows and 113 `UNKNOWN` analyzer rows. It shows many held battle, held utility, evolution, economy, and utility items appearing as aggregate rows.
- Several highlighted rows have high observed totals for held/evolution/economy-style items, e.g. `Luck Incense`, `Leaders Crest`, and `Peat Block`. This is consistent with broad flat eligible pools, though it is not statistical proof by itself.
- `item-pool-candidate-report.md` already documents that Field non-TM, Shop random filler, and Pickup share the same broad allowed/non-bad candidate source before final filters.
- No raw logs or ROM-specific paths were used here, and the existing reports explicitly warn that analyzer summaries are heuristic, not authoritative randomizer policy.

## Design Options

| Option | Vorteile | Nachteile | Randomizer-Kompatibilitaetsrisiko | Implementierungsaufwand | Empfehlung |
| --- | --- | --- | --- | --- | --- |
| Keep flat pool | Matches current FVX behavior; simple and reproducible; minimal regression risk | Form-heavy species and large item families get more aggregate weight | Low | None | Accept only if Anton wants current behavior documented rather than changed. |
| Category-first item sampling | Reduces Berry/Gem/Held/Evolution/Ball family dominance; easier to tune reward feel | Requires stable category taxonomy and per-pool policy decisions; can make rare categories too common | Medium, especially Shop guarantees and Pickup tiers | Medium | Best candidate for a later item design PR after Anton chooses categories. |
| Family-capped species/form sampling | Limits extreme form-heavy species without fully changing species identity | Needs definition of family cap and exceptions; can be opaque to users | Medium | Medium | Useful for Unown/cosmetic-heavy families, but needs candidate counts first. |
| Base-species-first then form sampling | Gives each base species one ticket, then chooses an allowed form inside that base | Collapses intentional form distinction unless exceptions exist; Regional Forms may feel underrepresented | Medium-high if applied globally | Medium-high | Good for cosmetic/form-heavy families, not recommended globally without toggles/exceptions. |
| Optional toggles later | Preserves legacy flat behavior while allowing balanced pools | More settings, UI/docs/test matrix complexity | Low-medium if default remains flat | Medium-high | Prefer for any behavior change after analysis. |

## Recommendation

No immediate code fix is justified from this documentation-only review.

For Pokemon, the current behavior should be documented as flat per eligible `Species` entry. A follow-up audit should count candidate families/forms from sanitized metadata and identify which families actually create skew. If Anton wants a behavior change, prefer base-species-first or family-capped sampling for selected form-heavy species such as Unown-like cosmetic families. Keep Regional Forms separate by default unless Anton explicitly decides that regional variants should share one base-species ticket.

For Items, category-first sampling is worth designing as a later feature for Field, Shop random filler, and Pickup. It should not be mixed into this review and should preserve existing Ban-Bad, mechanic, TM, shop guarantee, OP-shop, and pickup probability-slot semantics. Trainer sensible held items need a separate decision because their duplicate heuristic candidates appear intentional.

## Existing Tests / Evidence

- `SpeciesSetTest` covers `SpeciesSet.getRandomSpecies(...)` behavior at the set level, but there is no ROM-free test proving base-species-neutral form weighting because the current implementation is not base-species-neutral.
- `SpecialFormPredicatesTest` and `RestrictedSpeciesServiceGenLimitExclusionsTest` cover Mega/GMax/Irregular/Regional/Gen-limit eligibility. They do not test distribution fairness.
- `WildEncounterRandomizerTest`, `TrainerRandomizersTest`, `StaticPokemonRandomizerTest`, and related tests cover form inclusion/exclusion and randomizer invariants, not category/family weighting.
- `GameRandomizerStarterRivalSyncTest` and `TrainerRandomizersTest` cover Rival starter/counter-starter flow. They show Rival carry uses the starter trio rather than a fresh global species pool.
- `ItemDecisionTest`, `CfruDpeItemPoolPolicyTest`, and `Gen3SensibleHeldItemsTest` cover item eligibility, mechanic exclusions, TM exclusions, Ban-Bad behavior, and sensible held-item NPE/sanity cases. They do not test category-level distribution.
- Existing sanitized item analyzer reports provide aggregate evidence that many held/evolution/utility items appear, but they do not prove exact probabilities.

## Open Risks

- Final ROM `ItemData`, exact localized item names, and final species/form metadata were not loaded by this review.
- `SpeciesSet` iteration order comes from `HashSet`; the random pick is flat over cache entries, but ordering should not be interpreted as stable documentation.
- Some form families may be removed by cosmetic, irregular, ability-dependent, or asset-guard filters before sampling; this report describes weighting after eligibility, not exact final candidate counts.
- Item category labels such as Berry, Gem, held battle, utility, evolution, and economy are design buckets for review, not current code buckets.
- Existing batch evidence is sanitized and aggregate-only; it supports the flat-pool hypothesis but is not a formal statistical test.

## Next Work-Packages

1. `analysis/species-form-weighting-audit` - Count allowed species/form tickets per feature/settings profile and identify concrete overrepresented form families.
2. `analysis/item-category-weighting-design` - Define item category taxonomy, per-pool defaults, and compatibility constraints for Field/Shop/Pickup.
3. `fix/item-category-first-sampling` - Only if Anton decides to implement category-first item sampling after design review.
