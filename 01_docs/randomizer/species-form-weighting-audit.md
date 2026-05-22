# Species Form Weighting Audit

Branch: `analysis/species-form-weighting-audit`

Scope: documentation-only audit of whether form-heavy Pokemon families, especially Unown, can be overrepresented in current UPR-FVX species pools. This review covers Wild, Trainer, Starter, Static Pokemon, and Rival starter carry behavior. No ROMs, builds, table edits, or code changes were used.

## Executive Summary

Unown overrepresentation is theoretically possible in any pool that samples from a `SpeciesSet` containing multiple Unown form entries. `SpeciesSet.getRandomSpecies(...)` samples a flat `ArrayList` of eligible `Species` entries and does not collapse by `baseForme`, `baseNumber`, or family. If 28 Unown letter forms are eligible as distinct `Species` identities, the Unown family has 28 tickets.

The current code review confirms the flat per-`Species` sampling behavior, but it does not confirm that the current CFRU/DPE FireRed candidate pools actually contain Unown letters as distinct eligible `Species` entries. Some upstream handlers model Unown as cosmetic form counts instead of separate Pokemon objects. This audit intentionally did not load ROM metadata, so actual Unown count in the target candidate pools remains an evidence gap.

Affected features are Wild Pokemon, Trainer Pokemon, Starters, and Static Pokemon whenever their alternate-form settings and special-form filters allow non-cosmetic form entries into the candidate pool. Rival starter carry does not draw from an independent species pool; it inherits whatever the Starter randomizer selected and then carries or evolves that starter through rival battles.

## Codepath Analysis

| Feature | Pool source | Form inclusion flag | Final draw | Base-species dedupe? | Risk |
| --- | --- | --- | --- | --- | --- |
| Wild Pokemon | `WildEncounterRandomizer.randomizeEncounters(...)` builds `allowed` from `rSpecService.getSpecies(noLegendaries, allowAltFormes, false)`, then removes wild bans, player-banned forms, ability-dependent forms when abilities are unchanged, irregular forms when banned, premature evolutions, and unusable extended BPRE assets. | `settings.isAllowWildAltFormes()` | `SpeciesSet.getRandomSpecies(random)` or `SpeciesSet.getRandomSimilarStrengthSpecies(...)` from filtered `SpeciesSet`s. Catch Em All tracking removes picked `Species` entries, not whole form families. | No. `SpeciesSet` samples individual `Species` entries. | High if form-heavy non-cosmetic families survive filtering. Type/theme and Catch Em All logic do not neutralize family size. |
| Trainer Pokemon | `TrainerPokemonRandomizer.randomizeTrainerPokes(...)` builds `cachedAll` from `rSpecService.getSpecies(noLegendaries, includeFormes, false)`, optionally intersects local families, then removes trainer bans, ability-dependent forms, irregular forms, unusable BPRE assets, and type-theme-invalid entries. | `settings.isAllowTrainerAlternateFormes()` | `pickTrainerPokeReplacement(...)` draws with `getRandomSpecies(random)` or `getRandomSimilarStrengthSpecies(...)`. Type-themed picking also builds type weights from pool sizes. | No. Type weights and final picks count surviving form entries individually. | High for trainer replacement pools if many forms survive; type weighting can also inherit form-entry frequency. |
| Starters | `StarterRandomizer.getAvailableSet(...)` uses `rSpecService.getNonLegendaries(true)` or `rSpecService.getAll(true)` when alt forms are enabled, then removes ability-dependent forms when abilities are unchanged, irregular forms when banned, cosmetic replacements, and `isActuallyCosmetic` entries. Extra starter filters can apply for custom, basic, dual-type, BST, and type modes. | `settings.isAllowStarterAltFormes()` | `chooseStartersBasic(...)`, `chooseStartersOfTypes(...)`, and `chooseUniqueTypeStarters(...)` draw with `SpeciesSet.getRandomSpecies(...)`. | No. | Medium to high if a form-heavy family passes starter-specific filters. The starter trio then determines Rival starter carry input. |
| Static Pokemon | `StaticPokemonRandomizer` uses `rSpecService.getLegendaries(allowAltFormes)`, `getNonLegendaries(allowAltFormes)`, or `getAll(true)` with cosmetic replacements filtered, then removes static bans, player-banned forms, ability-dependent forms, irregular forms, and mode-specific restricted lists. | `settings.isAllowStaticAltFormes()` | Static replacement paths draw with `getRandomSpecies(random)`, `getRandomSimilarStrengthSpecies(...)`, restricted-pool `getRandomSpecies(random)`, or Mega-specific helper pools. | No general dedupe. | Medium to high for random/similar/restricted pools if form-heavy families are eligible. Swap-legendaries mode depends heavily on legendary/nonlegendary split. |
| Rival starter carry | `TrainerPokemonRandomizer.makeRivalCarryStarter()` and `rivalCarriesStarterUpdate(...)` read the existing `romHandler.getStarters()` list. The rival starter slot is index `1`, then later battles carry or evolve that selected starter. | Inherited from Starter selection, not a separate flag. | No new species-pool draw for the carried starter; evolution selection follows legal evolution logic from the selected starter. | Not applicable in carry step. Starter selection itself has no base-species dedupe. | No independent weighting risk beyond Starter randomization. If Starter picked a form-heavy family member, Rival carry preserves that result. |

Core evidence:

- `SpeciesSet` extends `HashSet<Species>` and `getRandomSpecies(Random, boolean)` caches `new ArrayList<>(this)` and chooses `random.nextInt(randomCache.size())`.
- `Species.equals(...)` and `hashCode()` use `speciesSetIdentityNumber`, so separate form identities can be separate set members.
- `Species.getBaseNumber()` and `baseForme` exist, but the reviewed draw paths do not use them to build base-species buckets before sampling.
- `RestrictedSpeciesService.getSpecies(noLegendaries, allowAltFormes, allowCosmeticFormes)` controls inclusion and removes cosmetic replacements only when requested. It does not rebalance families after filtering.

## Unown-Specific Check

Unown forms can be represented in different ways depending on handler data:

- If Unown letters are separate `Species` objects with distinct `speciesSetIdentityNumber` values in `getSpeciesSetInclFormes()`, each eligible letter is one flat ticket in `SpeciesSet`.
- If Unown is modeled as one base `Species` with cosmetic form numbers, the randomizer may choose the base species once and later write a random cosmetic form number. That path does not multiply species-pool tickets.
- Existing upstream constants show both patterns are possible in the codebase. For example, Gen 4 constants define Unown as 28 cosmetic forms, while `PokemonImageGetter` notes that graphical formes such as Unown and Arceus often do not get separate Pokemon objects. This is informative but not proof for the CFRU/DPE FireRed target.

No Unown-specific family weighting or dedupe was found in the reviewed Wild, Trainer, Starter, Static, or Rival carry paths. A Wild Catch Em All comment mentions an "Unown clause" for banned species/theme behavior, but that logic does not collapse Unown forms into one draw ticket.

Settings and filters required for Unown-form overrepresentation:

- The feature must randomize the relevant pool.
- The feature-specific alt-form flag must allow forms: `allowWildAltFormes`, `allowTrainerAlternateFormes`, `allowStarterAltFormes`, or `allowStaticAltFormes`.
- Gen restrictions and special-form options must allow the entries into `RestrictedSpeciesService`.
- The entries must not be removed as cosmetic replacements, actually cosmetic forms, irregular special forms, ability-dependent forms, player-banned forms, pool-specific bans, unusable extended BPRE assets, or starter/statics mode filters.
- For starters, additional basic/evolution/BST/type filters can remove entries even if the species service allowed them.

Conclusion for Unown: the code supports overrepresentation if Unown letters are distinct eligible `Species` entries, but this audit does not confirm that condition for the current CFRU/DPE pools.

## Other Form-Heavy Species

| Family or group | Potential behavior | Risk note |
| --- | --- | --- |
| Alcremie | Can be overrepresented if sweets/cream forms are separate non-cosmetic `Species` entries and alt forms are enabled. | Needs candidate-count audit. If modeled as cosmetic-only, risk is reduced. |
| Minior | Meteor/core/color forms can create multiple entries if represented as separate `Species`. | Ability or form-change semantics may make some forms unsuitable; current flat sampler would still count surviving entries individually. |
| Vivillon | Pattern forms can multiply tickets if represented as separate non-cosmetic entries. | Likely a candidate for family-level review if the target data exposes patterns as species identities. |
| Rotom | Functional appliance forms are usually gameplay-relevant and may be intentionally separate. | Do not dedupe automatically without deciding whether each form should remain a distinct encounter candidate. |
| Arceus | Plate forms may be cosmetic or item/form-change driven depending metadata. | No broad dedupe recommended; no-legendaries and special-form filters may already gate this. |
| Silvally | Memory forms may be item/form-change driven. | Same caveat as Arceus; candidate inclusion must be source-backed before changing weighting. |
| Regional Forms | Regional forms and regional branch evolutions are explicitly classified in `Species`. | Do not globally dedupe. Regional forms are often intentionally separate species candidates with distinct typing/evolution behavior. |
| Mega and GMax | `SpecialFormPredicates` can exclude Mega/GMax by default unless settings allow them. | If enabled and eligible, each surviving form is an individual ticket. Many pools also have additional bans or asset checks. |
| Castform, Darmanitan-Z, Aegislash-B, Wishiwashi-S | `RestrictedSpeciesService.getAbilityDependentFormes()` is removed in reviewed pools when abilities are not randomized. | If abilities are randomized and other filters allow them, surviving entries still sample flat. |
| Irregular special forms | `Species.isIrregularSpecialForm()` and `settings.isBanIrregularAltFormes()` control exclusion in reviewed randomizers. | If allowed by settings, entries still count individually. |

## Existing Test Evidence

ROM-free tests exist around special-form predicates, settings serialization, trainer special rules, and helper behavior, but this audit did not find a direct distribution test asserting base-species-neutral sampling for Wild, Trainer, Starter, or Static pools.

That is consistent with the implementation: current tests validate whether forms are allowed or filtered, not whether a family with many surviving form entries has the same probability as a family with one entry.

## Sampling And Test Proposal

Use two layers of evidence before any code fix.

1. ROM-free mechanics test

Create a synthetic `SpeciesSet` containing one normal species plus a form family with many distinct `speciesSetIdentityNumber` values and shared base form metadata. Draw repeatedly from `getRandomSpecies(...)` with deterministic seeds or inspect the constructed pool. Expected result under current code: the multi-form family receives one ticket per `Species` entry. This proves mechanics without loading ROMs.

2. Sanitized candidate-count audit

Anton can run a local, sanitized audit against the target setup without publishing ROM paths, raw logs, hashes, saves, screenshots, or output ROMs. Prefer candidate counting over only counting random outcomes.

Recommended sanitized fields:

- `feature`: Wild, Trainer, Starter, Static.
- `settings_profile`: compact label only, especially alt-form ON/OFF and special-form options.
- `pool_size`: total eligible `Species` entries after all filters.
- `distinct_base_count`: count after grouping by `getBaseNumber()` or stable base-form identity.
- `family_name`: Unown, Alcremie, Minior, Vivillon, Rotom, Arceus, Silvally, Regional Forms, Mega/GMax, other high-count families.
- `family_entry_count`: number of eligible entries for that family.
- `expected_flat_probability`: `family_entry_count / pool_size`.
- `expected_base_neutral_probability`: `1 / distinct_base_count`, where applicable.
- `observed_family_count` and `observed_form_count`: only for optional sampled runs.

Recommended run shape:

- First pass: deterministic candidate-count dump for each feature and alt-form setting. This is the strongest evidence and may need no random runs.
- Second pass: 500 to 1000 sanitized seeds only if distribution evidence is still useful after candidate counts.
- For Wild and Trainer, collect both family-level counts and individual-form counts because type/local/similar-strength filters can narrow pools after the global candidate set.
- For Starters and Static, record the final candidate list for each mode being evaluated, because starter-specific and static-specific filters can dominate the result.

Unown-specific metric:

- Compare Unown family probability as `eligible_unown_entries / eligible_pool_size` against a base-species-neutral model where Unown contributes one family ticket.
- If observed picks match the flat expectation, the code behavior is confirmed for the active target pool.
- If Unown appears as only one eligible entry plus cosmetic form numbers, the suspected overrepresentation is not present for that pool.

## Design Options

| Option | Advantages | Disadvantages | Randomizer compatibility risk | Implementation effort | Recommendation |
| --- | --- | --- | --- | --- | --- |
| Keep flat species/form pool | Matches current UPR-FVX behavior; every eligible `Species` identity is transparent and easy to reason about. | Form-heavy families can be overrepresented when forms are distinct entries. | Lowest because behavior is unchanged. | None. | Acceptable until candidate counts confirm an unwanted skew. |
| Unown-only family ticket | Minimal correction for the suspected worst case if Unown is confirmed as many eligible entries. | Special-case logic can be surprising and may not help other form-heavy families. | Low to medium; only one family changes probability. | Low. | Good first fix candidate only if Unown overrepresentation is confirmed. |
| Selected form-family ticket model | Groups only agreed families such as Unown, Alcremie, Minior, or Vivillon while leaving gameplay-significant forms separate. | Requires a maintained family list and clear policy. | Medium; selected families change odds while Regional/functional forms stay compatible. | Medium. | Best design direction if multiple cosmetic-style families are confirmed skewed. |
| Base-species-first then form | Cleanly neutralizes all form-count weighting. | Too broad; would collapse Regional Forms, functional forms, Mega/GMax, and other intentionally distinct candidates unless heavily exempted. | High. Could change expected randomizer semantics across many features. | Medium to high. | Not recommended as a blanket change. |
| Optional toggle | Lets users choose legacy flat behavior or family-neutral behavior. | Adds UI/profile/test surface and can fragment reproducibility expectations. | Medium; compatibility depends on default. | Medium to high. | Consider only after the desired policy is proven and Anton wants user-facing control. |

## Recommendation

Do not implement a code fix from this audit alone. The code confirms a real flat-sampling mechanism, but current Unown overrepresentation is not confirmed without target candidate counts.

Next step should be a sanitized candidate-count audit for Wild, Trainer, Starter, and Static pools with alt forms ON/OFF. If Unown is confirmed to appear as many eligible distinct entries and Anton considers that undesirable, design the smallest correction first: either an Unown-only family ticket or a selected form-family ticket model. Do not globally deduplicate Regional Forms; they are intentionally distinct in CFRU/DPE-aware behavior and may differ in typing, evolution, and asset support.

No P1 promotion is implied by this audit.
