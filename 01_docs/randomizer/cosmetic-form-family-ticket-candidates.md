# Cosmetic Form Family Ticket Candidates

Status: documentation-only review. No ROMs, no builds, no UPR-FVX code changes.

## Executive Summary

Unown is already handled separately by the targeted UPR-FVX family-ticket fix. The next best candidates are the families whose source-level form entries are numerous and whose known differences are cosmetic or nearly cosmetic:

- `Vivillon`: strongest follow-up candidate. The local DPE source exposes 20 Vivillon pattern entries, and the sampled DPE stats/type/ability data is identical across the checked pattern forms.
- `Alcremie`: good candidate for normal sweet/decoration forms only. The local source exposes 7 normal Alcremie sweet forms and one separate GMax entry; GMax must stay mechanic-gated.
- `Minior`: review candidate, not a simple whole-family candidate. The seven core colors appear color-only relative to each other, but `Minior Shield` has different battle stats from core forms.

Do not globally deduplicate forms. UPR-FVX currently treats eligible `SpeciesSet` entries as flat tickets, but many forms intentionally differ by region, type, stats, ability, item mechanics, battle transformation, fusion, or special-form gates. A broad base-species dedupe would incorrectly change Regional Forms, Mega/GMax handling, and gameplay-relevant form families.

Explicit non-candidates for a cosmetic family ticket are Regional Forms, Mega/GMax forms, Rotom, Arceus, Silvally, Deoxys, Giratina, Kyurem, Necrozma, Calyrex, Darmanitan, Meloetta, Aegislash, Zygarde, Genesect, Ogerpon, and Oricorio unless Anton later approves a separate feature-specific design.

## Evidence Scope

Reviewed sources:

- UPR-FVX species model and pool behavior:
  - `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Species.java`
  - `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/SpeciesSet.java`
  - `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/services/RestrictedSpeciesService.java`
  - `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/services/SpecialFormPredicates.java`
- Local DPE/CFRU source metadata:
  - `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`
  - `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c`
  - `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Species_To_Pokdex_Table.c`
  - `02_external/CFRU-expansion/include/`
  - `02_external/CFRU-expansion/src/`

This review does not prove final ROM-loaded candidate counts. It only identifies source-level family size and gameplay relevance so Anton can decide whether another narrow family-ticket fix is worth implementing.

## Candidate Table

| Family | Source-level form count | Form type | Gameplay relevance | Candidate for family-ticket? | Recommendation |
| --- | ---: | --- | --- | --- | --- |
| Vivillon | 20 | Pattern forms | Checked DPE pattern entries share stats, typing, and abilities; pattern is cosmetic in normal gameplay. | `COSMETIC_GOOD_CANDIDATE` | Best next candidate if Anton approves `fix/species-family-ticket-cosmetic-forms`. |
| Alcremie | 7 normal sweet forms; 8 including GMax | Sweet/decoration forms plus GMax | Normal sweet forms share checked stats, typing, and abilities; GMax is a separate mechanic form. | `COSMETIC_GOOD_CANDIDATE` for normal forms; `MECHANIC_GATED` for GMax | Candidate only for normal sweet forms. Exclude GMax from any family ticket. |
| Minior | 8 | Shield plus 7 core colors | Core colors are likely cosmetic relative to each other, but Shield and Core have different stat profiles. | `MOSTLY_COSMETIC_REVIEW` | Do not group all 8 blindly. Consider a core-color-only ticket only after Anton approves that split. |
| Rotom | 6 | Appliance forms | Appliance forms alter typing and form role. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No change without a separate Rotom-specific decision. |
| Arceus | 18 | Type/plate forms | Type identity and item/form mechanics are central. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Silvally | 18 | Type/memory forms | Type identity and item/form mechanics are central. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Deoxys | 4 | Stat forms | Forms have different battle roles and stat profiles. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Giratina | 2 | Altered/Origin | Origin form is item/form-mechanic relevant and is already restricted for player Pokemon contexts. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Kyurem | 3 | Base/Black/White fusion forms | Fusion forms have different battle identity. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Necrozma | 4 | Base/fusion/Ultra forms | Fusion and Ultra forms are mechanic and battle relevant. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` / `MECHANIC_GATED` | No family ticket. |
| Calyrex | 3 | Base/Ice Rider/Shadow Rider | Rider forms are fused, typed, and stat-relevant. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Darmanitan | 4 including Zen and Galarian forms | Zen, regional, regional Zen | Zen is ability-dependent; Galarian forms are regional/type-distinct. | `MECHANIC_GATED` / `REGIONAL_DO_NOT_GROUP` | No broad grouping. Keep current ability-dependent and regional handling. |
| Meloetta | 2 | Aria/Pirouette | Form change affects typing and battle behavior. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Aegislash | 2 | Shield/Blade | Battle stance is ability-dependent and stat-relevant. | `MECHANIC_GATED` | No family ticket. |
| Zygarde | 5 | Cell/Core/10 percent/50 percent/Complete | Form progression and battle identity are not cosmetic. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Regional Forms | Variable | Regional variants and regional branches | Intended as distinct species candidates with typing, stats, movepool, and generation semantics. | `REGIONAL_DO_NOT_GROUP` | No global regional dedupe. |
| Mega/GMax | Variable | Battle mechanic forms | Already tied to special-form filters and mechanic settings. | `MECHANIC_GATED` | Do not family-ticket; rely on existing gates. |
| Cap/Event Pikachu and costume-like Pikachu | About 16 non-GMax costume/cap/event forms plus GMax | Event/costume/irregular and GMax | Existing source-backed irregular Pikachu and GMax gates are more important than cosmetic grouping. | `MECHANIC_GATED` | Do not include in the next cosmetic ticket pass; count only if leakage is suspected. |
| Furfrou | 10 | Trim forms | Likely cosmetic trims, but not part of the first requested focus and final pool exposure is unproven. | `MOSTLY_COSMETIC_REVIEW` | Secondary candidate after Vivillon/Alcremie if Anton wants a broader cosmetic pass. |
| Flabebe/Floette/Florges | 5 / 6 / 5 | Flower color forms; Floette also has Eternal Flower | Flower colors look cosmetic, but Eternal Flower is special. | `MOSTLY_COSMETIC_REVIEW` | Review separately; do not group Eternal Flower with color forms. |
| Deerling/Sawsbuck | 4 / 4 | Season forms | Mostly visual in mainline context, but season semantics may be intentional. | `MOSTLY_COSMETIC_REVIEW` | Low priority; count first. |
| Pumpkaboo/Gourgeist | 4 / 4 | Size forms | Size can affect stats and battle identity. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Oricorio | 4 | Style forms | Styles alter typing. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Genesect | 5 | Drive forms | Drive/item forms affect move typing and form identity. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` | No family ticket. |
| Ogerpon | 8 | Mask and transformed forms | Mask, type, and transformation mechanics are central. | `GAMEPLAY_RELEVANT_DO_NOT_GROUP` / `MECHANIC_GATED` | No family ticket. |

## Categories

`COSMETIC_GOOD_CANDIDATE`: Source entries are numerous, share one base family, and appear visual-only or near visual-only after checking local source data. These are reasonable candidates for a narrow allowlist family-ticket model after Anton approval.

`MOSTLY_COSMETIC_REVIEW`: The family may contain cosmetic subsets, but the whole family is mixed, final candidate exposure is unproven, or the split needs explicit design. Minior is the clearest example because core colors and Shield should not automatically be one ticket.

`GAMEPLAY_RELEVANT_DO_NOT_GROUP`: Forms differ by type, stats, ability behavior, item/fusion mechanics, battle role, or legendary/form-change semantics. These should remain flat Species tickets unless a later feature-specific design says otherwise.

`MECHANIC_GATED`: Forms are already controlled or should be controlled by existing special-form, Mega/GMax, irregular, ability-dependent, or player-pokemon restriction logic. A cosmetic family-ticket pass should not bypass those gates.

`REGIONAL_DO_NOT_GROUP`: Regional Forms and regional branches are intentionally separate randomizer candidates. They should not be deduplicated by a cosmetic form policy.

`UNKNOWN_NEEDS_COUNT_EVIDENCE`: Source entries are visible, but final ROM-loaded and post-filter `SpeciesSet` exposure remains unproven. These families should be counted before implementation.

## Recommendation

Do not implement global form dedupe. Keep the Unown fix targeted and extend the model only with an explicit allowlist if Anton approves a follow-up.

Recommended first follow-up scope for `fix/species-family-ticket-cosmetic-forms`:

- Include `Vivillon` pattern forms.
- Include normal `Alcremie` sweet forms.
- Exclude Alcremie GMax.
- Leave `Minior` out unless Anton explicitly approves a core-color-only design that keeps Shield separate.

Do not change Regional Forms. Do not change Rotom, Arceus, or Silvally without a separate design decision. Do not change Mega/GMax, ability-dependent, fusion, type-changing, or stat-changing families as part of this cosmetic pass.

If implemented later, tests should prove that the allowlisted cosmetic family counts as one ticket against normal species, the selected family item resolves only to allowed forms from the filtered pool, and all non-allowlisted families remain flat Species tickets.

## Next Step

Anton should decide whether the next implementation package, `fix/species-family-ticket-cosmetic-forms`, should include only Vivillon plus normal Alcremie, or also a Minior core-color-only design; no code fix should start before that decision.
