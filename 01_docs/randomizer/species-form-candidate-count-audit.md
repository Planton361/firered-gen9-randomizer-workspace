# Species Form Candidate Count Audit

Branch: `analysis/species-form-candidate-count-audit`

Scope: documentation-only candidate-count audit for form-heavy Pokemon families in UPR-FVX species pools. Focus is Wild, Trainer, Starter and Static Pokemon with Alt-Forms ON/OFF. This audit used local source files only; no ROMs, builds, raw logs, private paths, saves, screenshots or output ROMs were read or produced.

## Executive Summary

The local DPE/CFRU sources make form-heavy overrepresentation plausible, and for several families the source-level ticket counts are countable. DPE `include/species.h`, `src/Base_Stats.c`, and `src/Species_To_Pokdex_Table.c` define separate entries for Unown letters, Vivillon patterns, Arceus type forms, Silvally type forms, Minior colors, Alcremie sweets/forms and other families. If the final ROM exposes those entries through UPR-FVX `Gen3RomHandler` as distinct `Species` objects, each surviving entry is one flat `SpeciesSet` ticket.

Unown is **locally source-confirmed as 28 DPE species/form entries**: `SPECIES_UNOWN` plus `SPECIES_UNOWN_B` through `SPECIES_UNOWN_QUESTION`, with matching Base Stats and Species-to-Pokedex mappings. It is **not fully ROM-pool-confirmed** because this audit did not load the final ROM or inspect an actual `romHandler.getSpeciesSetInclFormes()` result. In practical terms, Unown overrepresentation is likely for CFRU/DPE builds that include these DPE internal species IDs and do not filter them before randomization.

The affected features are Wild Pokemon, Trainer Pokemon, Starters and Static Pokemon. Rival starter carry has no independent species candidate pool; it inherits whatever the Starter randomizer selected.

One important Gen3/CFRU-DPE caveat: `Gen3RomHandler.getSpeciesInclFormes()` currently returns the same `speciesList` as `getSpecies()`, and `getAltFormes()` returns an empty `SpeciesSet`. For this handler, many DPE form entries are therefore not separated by UPR-FVX's generic alt-form model. Alt-Forms OFF may not remove source-defined DPE form entries if they are loaded as ordinary internal species.

## Candidate-Counting Method

What can be counted safely without ROM:

- Source-defined Species IDs in `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`.
- Presence of matching source entries in DPE `src/Base_Stats.c`.
- Shared National Dex mappings in DPE `src/Species_To_Pokdex_Table.c`, for example all Unown letters mapping to `NATIONAL_DEX_UNOWN`.
- UPR-FVX source behavior: `SpeciesSet.getRandomSpecies(...)` is flat per `Species`; `Species.equals(...)` and `hashCode()` use `speciesSetIdentityNumber`; Gen3/CFRU-DPE species loading uses internal species identities for extended BPRE.
- UPR-FVX filter structure: `RestrictedSpeciesService`, `SpecialFormPredicates`, and feature-specific bans in Wild, Trainer, Starter and Static randomizers.

What remains unproven without final ROM/SpeciesSet load:

- The exact `PokemonCount` and final `PokemonStats` table entries in the built ROM.
- The exact `speciesList` and `SpeciesSet` content produced by `Gen3RomHandler.loadSpeciesStats()` for the current private target ROM.
- Whether any local build step, ROM entry, name table, or final pointer state omits a source-defined form entry.
- Final per-feature candidate counts after all runtime filters, BST/type/local/static restrictions, no-legendary settings and asset checks.

Sources used:

- UPR-FVX: `Species.java`, `SpeciesSet.java`, `RestrictedSpeciesService.java`, `WildEncounterRandomizer.java`, `TrainerPokemonRandomizer.java`, `StarterRandomizer.java`, `StaticPokemonRandomizer.java`, and relevant tests around special-form predicates/settings.
- DPE: `include/species.h`, `src/Base_Stats.c`, `src/Species_To_Pokdex_Table.c`, sprite/palette table references where helpful.
- CFRU: `src/wild_encounter.c`, `src/config.h`, follower/experience tables where they corroborate species/form presence.

Hypothetical settings profiles considered:

- Alt-Forms OFF: for Gen3/CFRU-DPE this may still include DPE form entries because `getAltFormes()` is empty and `getSpeciesInclFormes()` returns the same `speciesList` source as `getSpecies()`.
- Alt-Forms ON: same source list, but feature-specific code may apply cosmetic or actually-cosmetic filters if metadata exists.
- Gen Limit 1-9: permits all documented generations and regional generation ranges; no generation-only exclusion for Unown/Vivillon/Minior/Alcremie if they are within allowed generations.
- Special Forms OFF: `SpecialFormPredicates` excludes Mega, GMax and irregular special forms, but does not automatically exclude all DPE source-defined variants such as Unown letters, Vivillon patterns, Minior colors, Rotom appliances, Arceus plates or Silvally memories.
- Special Forms ON: Mega/GMax/irregular entries can additionally survive if other feature filters allow them.

## Feature Matrix

| Feature | Alt-Forms setting | Candidate source | Countability without ROM | Risk |
| --- | --- | --- | --- | --- |
| Wild Pokemon | `settings.isAllowWildAltFormes()` | `rSpecService.getSpecies(noLegendaries, allowAltFormes, false)`, then wild bans, player-form bans, ability-dependent bans, irregular bans, premature-evolution and asset filters. | Source family sizes are countable. Final Wild pool is not countable without ROM because `PokemonCount`, bans, asset availability and encounter-mode filters are runtime-loaded. | High for ordinary random/similar-strength Wild replacement if DPE forms survive as species entries. |
| Trainer Pokemon | `settings.isAllowTrainerAlternateFormes()` | `rSpecService.getSpecies(noLegendaries, includeFormes, false)`, then trainer bans, ability-dependent bans, irregular bans, local/type/diversity filters and asset checks. | Source family sizes are countable. Final Trainer pool is not fully countable without ROM because local-Pokemon, type-theme and trainer-mode filters narrow candidates dynamically. | High if forms survive; type weighting can also inherit form-entry counts. |
| Starters | `settings.isAllowStarterAltFormes()` | `rSpecService.getNonLegendaries(true)` or `getAll(true)` when alt forms are enabled; otherwise `getNonLegendaries(false)` or `getAll(false)`. Starter filters remove ability-dependent, irregular, cosmetic and actually-cosmetic entries when metadata exists. | Source family sizes are countable. Final starter candidates need ROM-loaded metadata and starter-mode settings for exact counts. | Medium to high. No-legendary/basic/BST/type filters can remove many entries, but form-heavy nonlegendary families can still multiply tickets. |
| Static Pokemon | `settings.isAllowStaticAltFormes()` | `rSpecService.getLegendaries(allowAltFormes)`, `getNonLegendaries(allowAltFormes)` or `getAll(true)` depending static mode, plus static bans, player-form bans, ability-dependent bans, irregular bans and restricted pools. | Source family sizes are countable. Final static candidates depend on static mode, legendary split and per-static restrictions. | Medium to high; Arceus/Silvally are often affected by legendary/no-legendary settings, while nonlegendary form families can still multiply. |
| Rival starter carry | Inherited from Starter selection. | `TrainerPokemonRandomizer.makeRivalCarryStarter()` uses `romHandler.getStarters()` and the rival starter slot, then carries/evolves that selected starter. | No independent candidate count. Countability is the Starter pool question. | No separate risk beyond Starter randomization. |

## Form-Family Count Table

Counts below are source-level DPE Species ID counts from `include/species.h`, corroborated where relevant by `Base_Stats.c` and `Species_To_Pokdex_Table.c`. "Approx eligible form tickets" means potential flat tickets before final ROM load and per-feature filters.

| Family | Approx eligible form tickets | Base species tickets | Feature exposure | Risk | Recommendation |
| --- | ---: | ---: | --- | --- | --- |
| Unown | 28 source entries: base plus B-Z, exclamation and question. | 1 National Dex family. | Wild, Trainer, Starter, Static if nonlegendary forms survive. CFRU wild code also has Unown letter runtime handling for Tanoby Ruins, but that is separate from UPR-FVX species-pool sampling. | High and likely if loaded as distinct species entries. | Prioritize for candidate-count helper. If confirmed in final pools, consider Unown-only family ticket first. |
| Vivillon | 20 source entries: base/Fancy plus 18 pattern entries. | 1 National Dex family. | Wild, Trainer, Starter, Static if forms survive. | High; pattern forms are a classic cosmetic-style family. | Candidate-count helper should report family count; selected family-ticket design may be better than base-species-global dedupe. |
| Arceus | 18 source entries: base plus 17 typed forms. | 1 National Dex family. | Mainly Static and any pool allowing legendaries; Wild/Trainer/Starter only if no-legendary settings allow. | Medium to high, but legendary and item/form-change semantics make automatic dedupe risky. | Count and document; do not fix before policy decision. |
| Silvally | 18 source entries: base plus 17 typed forms. | 1 National Dex family. | Wild, Trainer, Starter, Static depending legendary classification and filters. | Medium to high; typed Memory forms can multiply tickets. | Count and document; policy needed because forms are gameplay-relevant. |
| Minior | 8 source entries: Shield plus 7 core colors. | 1 National Dex family. | Wild, Trainer, Starter, Static if forms survive. | Medium to high; color/core forms may be cosmetic-style but ability/form-change behavior matters. | Candidate-count helper should report; selected family-ticket candidate if confirmed. |
| Alcremie | 8 source entries: Strawberry, Berry, Clover, Flower, Love, Ribbon, Star and GMax. | 1 National Dex family. | Non-GMax forms can affect Wild/Trainer/Starter/Static; GMax depends on special-form settings. | Medium to high; normal Alcremie forms can multiply even with GMax excluded. | Count separately as normal forms vs GMax. Consider selected family ticket only after evidence. |
| Rotom | 6 source entries: base plus Heat/Wash/Frost/Fan/Mow. | 1 National Dex family. | Wild, Trainer, Starter, Static if forms survive. | Medium; appliance forms are functional and type-distinct. | Do not auto-dedupe; count and decide intentionally. |
| Furfrou | 10 source entries: base plus trims. | 1 National Dex family. | Wild, Trainer, Starter, Static if forms survive. | Medium to high if trims are loaded as ordinary species. | Add to selected-family review if Unown/Vivillon issue is confirmed. |
| Pikachu costume/cap/GMax | 17 source entries by simple family-name count, including base, irregular variants and GMax. | 1 National Dex family. | Many variants should be excluded by irregular/GMax filters when those options are off. | Medium; special-form filters already cover the known CFRU/DPE irregular Pikachu range and GMax. | Keep current filters; count only to verify no unexpected leakage. |
| Ogerpon | 8 source entries including mask and Terastal variants. | 1 National Dex family. | Gen9 pools if target data and filters allow. | Medium; forms are gameplay-significant and very new. | Count, but do not dedupe without explicit design. |
| Zygarde | 5 source entries: base, Cell, Core, 10%, Complete. | 1 National Dex family. | Mostly legendary-enabled pools. | Medium; Cell/Core may be inappropriate candidates depending metadata. | Candidate-count helper should flag but not auto-fix. |
| Genesect | 5 source entries: base plus drive forms. | 1 National Dex family. | Legendary/mythical-enabled pools. | Medium; drive forms are item/form-change related. | Count and leave policy-gated. |
| Flabebe/Floette/Florges | 5 to 6 entries per family name, depending Eternal Floette. | 1 National Dex family per species line member. | Wild, Trainer, Starter, Static if forms survive. | Medium; flower colors are cosmetic-style. | Selected family-ticket review candidate, not global dedupe. |
| Deerling/Sawsbuck | 4 entries each. | 1 National Dex family per species. | Wild, Trainer, Starter, Static if forms survive. | Medium; seasonal forms may be cosmetic-style. | Count only; lower priority than Unown/Vivillon. |
| Pumpkaboo/Gourgeist | 4 entries each. | 1 National Dex family per species. | Wild, Trainer, Starter, Static if forms survive. | Medium; sizes affect stats in some games. | Do not treat as cosmetic automatically. |
| Oricorio | 4 source entries. | 1 National Dex family. | Wild, Trainer, Starter, Static if forms survive. | Medium; type-distinct forms. | Do not auto-dedupe. |
| Deoxys | 4 source entries. | 1 National Dex family. | Static/legendary-enabled pools mostly. | Medium, but Gen3 handler has legacy hardcoded Deoxys stats behavior and comments that no alt formes are modeled generically. | Count only; separate from Unown-style cosmetic concern. |
| Regional Forms | Source ranges include Alolan, Galarian, Hisuian and Paldean forms plus regional branch evolutions. UPR-FVX range predicates classify known CFRU/DPE regional identities. | Distinct regional species/forms by design. | All four pools if Gen restrictions and regional policy allow. | Intentional distinctness, not a "too many forms" bug by itself. | Do not pauschal dedupe. Keep regional semantics explicit. |
| Mega/GMax | 48 Mega/Primal-name entries and 34 GMax-name entries counted from DPE `species.h`. UPR-FVX range predicates classify Mega and GMax identity blocks. | Distinct mechanic forms. | Only when special-form options allow; often further banned or unsuitable by pool. | Low when Special Forms OFF; high only if explicitly enabled and expected. | Keep source-backed filters. Do not solve with family weighting. |

## Unown Deep Dive

Local source evidence:

- DPE `include/species.h` defines 28 Unown species IDs: `SPECIES_UNOWN`, `SPECIES_UNOWN_B` through `SPECIES_UNOWN_Z`, `SPECIES_UNOWN_EXCLAMATION` and `SPECIES_UNOWN_QUESTION`.
- DPE `src/Base_Stats.c` has a separate Base Stats entry for each of those Unown IDs.
- DPE `src/Species_To_Pokdex_Table.c` maps all 28 entries to `NATIONAL_DEX_UNOWN`, meaning they are separate source species entries sharing one Pokedex family.
- CFRU `src/wild_encounter.c` contains separate runtime logic for choosing an Unown letter in Tanoby Ruins when the wild species is `SPECIES_UNOWN`; that runtime letter selection is not the same as UPR-FVX candidate-pool sampling.

UPR-FVX load/filter interpretation:

- `Gen3RomHandler.loadSpeciesStats()` creates one `Species` per internal species index and, for extended BPRE, assigns `speciesSetIdentityNumber` to that internal index.
- `constructPokemonList()` includes every non-null, non-unused internal species entry for ROM hacks.
- `getSpeciesInclFormes()` returns `speciesList`; `getAltFormes()` returns an empty set for Gen3.
- `RestrictedSpeciesService` therefore cannot remove these DPE form entries through the generic `altFormes` set unless they are absent from the loaded ROM or removed by another predicate.
- `SpecialFormPredicates` does not have an Unown-specific exclusion. Special Forms OFF removes Mega, GMax and irregular entries, not Unown letters.

Are Unown forms removed by standard filters?

- Not by generic alt-form OFF, based on the current Gen3 handler source.
- Not by Special Forms OFF.
- Not by ability-dependent filters.
- Possibly by pool-specific bans, no-legendary is irrelevant because Unown is nonlegendary, asset guards, final ROM omission, or future metadata not visible from source-only review.

Feature pools where Unown could appear:

- Wild: yes, if candidate pool includes Unown entries and wild bans/asset checks do not remove them.
- Trainer: yes, if trainer bans/asset checks do not remove them.
- Starters: yes, unless starter filters such as basic/BST/type/custom settings remove them. Unown is nonlegendary and source-defined as multiple entries.
- Static: yes for random/similar static modes if allowed and not banned.
- Rival starter carry: only if Starter selection first picked an Unown entry.

Concrete evidence still needed:

- A sanitized count dump from a local final-ROM load of `romHandler.getSpeciesSet()` / `getSpeciesSetInclFormes()`, grouped by National Dex number or base family.
- Per-feature post-filter counts for Wild, Trainer, Starter and Static with Alt-Forms OFF/ON and Special Forms OFF/ON labels.
- For Unown specifically: `family=Unown`, `loaded_entries`, `post_filter_entries`, `removed_by_reason`, and a yes/no marker for whether entries are distinct `speciesSetIdentityNumber` values.

## Design Options If Confirmed

| Option | Advantages | Disadvantages | Compatibility risk | Recommendation |
| --- | --- | --- | --- | --- |
| Keep flat | Preserves current UPR-FVX behavior and treats every loaded internal species identity transparently. | Confirmed form-heavy families remain overrepresented. | Lowest. | Acceptable if Anton wants legacy DPE form behavior. |
| Unown-only family ticket | Minimal targeted correction for the strongest source-confirmed risk. | Special-case policy; does not help Vivillon or other cosmetic-style families. | Low to medium. | Best first fix if only Unown is confirmed and unwanted. |
| Selected form-family ticket | Groups explicitly approved families such as Unown, Vivillon, Furfrou or flower/color families while leaving Regional, Rotom, Arceus, Silvally and other functional forms separate. | Requires a maintained source-backed family list and tests. | Medium. | Best broader design if candidate counts show multiple cosmetic-style families skewing pools. |
| Base-species-first then form | Removes all form-count weighting by design. | Too broad; collapses Regional Forms and functional/type-distinct forms unless many exemptions are added. | High. | Not recommended as a blanket CFRU/DPE change. |
| Optional setting/toggle | Lets users choose legacy flat behavior or family-neutral behavior. | Adds GUI/RNQS/profile/test surface and reproducibility branches. | Medium to high. | Consider later only after the target policy is clear. |

## Recommendation

Do not implement a code fix from this audit alone. The source-level evidence is strong enough to say Unown and several other families are plausible or likely overrepresented if loaded into the final UPR-FVX species pool, but the final candidate counts still need one sanitized final-ROM SpeciesSet count.

If Unown is confirmed with many post-filter tickets, evaluate an Unown-only family ticket first. If Vivillon/Furfrou/Alcremie/Minior-style families are also confirmed and considered undesirable, move to a selected form-family ticket design. Do not globally deduplicate Regional Forms; UPR-FVX already treats them as source-backed regional identities and current compatibility docs preserve their intentional distinctness.

No P1 promotion follows from this audit.

## Next Minimal Step

Design a ROM-free counting helper spec for later implementation: a small, testable reporting helper that accepts an already-loaded `SpeciesSet` and prints sanitized aggregate counts grouped by National Dex number/base family for Wild, Trainer, Starter and Static post-filter pools. The helper should not open ROMs itself, should not log raw paths or hashes, and should report only aggregate fields such as `feature`, `settings_label`, `pool_size`, `family`, `entry_count`, `distinct_identity_count`, and `filter_stage`.
