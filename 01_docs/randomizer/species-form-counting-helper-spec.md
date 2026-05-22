# Species/Form Candidate-Counting Helper Specification

Status: documentation-only specification. No code changes, no ROM reads, no builds, no randomizer behavior changes.

## 1. Executive Summary

The current UPR-FVX species randomization path samples flat from eligible `SpeciesSet` entries. The prior audits show that form-heavy families such as Unown, Vivillon, Arceus, Silvally, Minior, Alcremie, and Rotom can have many source-level form entries. They do not yet prove the final loaded, post-filter candidate counts used by Wild Pokemon, Trainer Pokemon, Starters, or Static Pokemon.

A counting helper is needed to bridge that gap. It should aggregate already-loaded candidate pools by base family and emit sanitized summaries only. It can prove how many species tickets each family contributes to a specific feature/preset pool, whether form families appear with Alt-Forms OFF, which families dominate the top form-heavy rows, and whether a later fix is justified by evidence.

Without a ROM-loaded candidate pool, the helper cannot prove final UPR-FVX runtime counts. Source tables can show that many forms exist, and ROM-free unit tests can prove helper grouping logic, but only a local post-load diagnostic can prove the actual post-filter species tickets for Anton's CFRU/DPE target. The output must never include ROM paths, hashes, raw logs, saves, screenshots, output ROM names, or private local paths.

## 2. Helper Goal

The helper should summarize candidate pools after the same filtering stage that the randomizer will sample from. It should not change sampling behavior.

Required aggregates:

- Feature/preset label.
- Total species tickets in the sampled pool.
- Base-family count.
- Top form-heavy families.
- Per-family ticket count.
- Whether forms appear despite Alt-Forms OFF.
- Candidate source path as a safe internal label, not a filesystem path.
- Filters/settings summary.
- Sanitized output only.

The preferred input is an already-created `SpeciesSet` or equivalent post-filter collection. For ROM-free tests, synthetic `Species` objects can validate grouping and TSV formatting. For real evidence, a later local diagnostic may run after ROM load, but it must output only aggregate rows.

## 3. Possible Implementation Locations

| Location | What it proves | Strengths | Limits | Recommendation |
| --- | --- | --- | --- | --- |
| UPR-FVX ROM-free unit/integration test helper | Grouping logic, TSV schema, risk classification on synthetic `SpeciesSet` data | CI-safe, no ROM needed, easy to test edge cases like Unown 28 tickets | Does not prove Anton's final loaded candidate counts | Use first to validate helper behavior |
| Local CLI/diagnostic mode after ROM-load with sanitized output | Actual post-filter candidate counts for Anton's local ROM/settings | Best evidence for Alt-Forms OFF leakage and family share | Local-only, must guard all output, must not be committed with private data | Use as evidence producer if Anton approves |
| Workspace-side parser/analyzer from randomizer logs | Counts only if logs already contain complete candidate summaries | Avoids UPR-FVX code changes if logging is already sufficient | Current logs are unlikely to include every post-filter candidate pool and base-family grouping | Fallback only |
| Documentation-only manual checklist | Review discipline and acceptance criteria | No code and no ROM required | Cannot produce proof | Keep as review gate, not as evidence |

## 4. Data Model

Minimum TSV columns:

```text
feature	settings_profile_label	total_tickets	base_family	base_species_number_if_safe	family_ticket_count	forms_seen_count	alt_forms_setting	is_regional_family	is_cosmetic_or_form_family	risk_level	recommendation
```

Column semantics:

| Column | Meaning |
| --- | --- |
| `feature` | One of `wild`, `trainer`, `starter`, `static`, or `rival_starter_carry_inherited`. |
| `settings_profile_label` | Sanitized label such as `gen1_9_alt_off_special_off`; never a local file path. |
| `total_tickets` | Count of eligible `Species` entries in the final candidate pool. |
| `base_family` | Safe family label used for aggregation, for example `Unown` or `Vivillon`. |
| `base_species_number_if_safe` | National Dex/base species number if safe and non-private; otherwise blank or `UNKNOWN`. |
| `family_ticket_count` | Number of sampled species tickets belonging to the base family. |
| `forms_seen_count` | Number of distinct form/species identities seen for that family in the pool. |
| `alt_forms_setting` | `ON`, `OFF`, or `UNKNOWN` for the feature/preset under audit. |
| `is_regional_family` | `true` for regional or regional-branch families, otherwise `false`. |
| `is_cosmetic_or_form_family` | `true`, `false`, or `review` based on source-backed family classification. |
| `risk_level` | `NONE`, `LOW`, `MEDIUM`, `HIGH`, or `CONFIRMED`. |
| `recommendation` | Short action label such as `keep_flat`, `count_more`, `unown_ticket`, `selected_family_ticket`, or `no_global_dedupe`. |

Optional TSV columns for a later helper:

- `special_forms_setting`
- `candidate_source_path`
- `filter_stage`
- `filters_summary`
- `family_share`
- `forms_seen_label`
- `notes`

The optional `candidate_source_path` must be an internal code-stage label such as `StarterRandomizer.available_after_filters`, not a filesystem path.

## 5. Target Families

The helper should always report the known form-heavy families even when their count is zero. This makes Alt-Forms OFF/ON comparisons explicit.

| Family | Source-level count from prior audit | Why it is tracked | Default recommendation |
| --- | ---: | --- | --- |
| Unown | 28 | Highest confirmed source-level form count; most likely cosmetic overrepresentation risk | Count first; if confirmed, consider Unown-only or selected family ticket |
| Vivillon | 20 | Many pattern forms; likely form-family weighting risk | Count first; do not fix without post-filter evidence |
| Arceus | 18 | Many type forms; functional/policy-sensitive | Count first; avoid automatic cosmetic dedupe |
| Silvally | 18 | Many type forms; functional/policy-sensitive | Count first; avoid automatic cosmetic dedupe |
| Minior | 8 | Multiple source-level forms/colors | Count first; classify before fix |
| Alcremie | 8 | Multiple source-level forms in local audit | Count first; classify before fix |
| Rotom | 6 | Functional appliance forms | Count first; avoid automatic cosmetic dedupe |
| Regional Forms | variable | Intentional separate identity in many randomizer policies | Do not globally dedupe |
| Mega/GMax | variable | Should normally be gated by Special Forms settings | Verify filters; do not bundle with regular forms |
| Furfrou | 10 | Many trim forms in source-level audit | Count if present; likely selected-family candidate only after evidence |
| Ogerpon | 8 | Multiple mask forms; functional/policy-sensitive | Count first; avoid automatic cosmetic dedupe |
| Zygarde | 5 | Form/state family | Count first; classify before fix |
| Genesect | 5 | Drive forms may be gated or functional | Count first; classify before fix |
| Flabebe/Floette/Florges | 5-6 | Color families can add multiple tickets | Count first; selected-family review only |
| Deerling/Sawsbuck | 4 | Seasonal forms | Count first; selected-family review only |
| Pumpkaboo/Gourgeist | 4 | Size forms can differ mechanically | Count first; avoid blanket dedupe |
| Oricorio | 4 | Style/type forms | Count first; avoid automatic cosmetic dedupe |
| Deoxys | 4 | Functional stat forms | Count first; avoid automatic cosmetic dedupe |

## 6. Feature Scope

| Feature | Candidate pool to count | Notes |
| --- | --- | --- |
| Wild Pokemon | Post-filter replacement pool after `RestrictedSpeciesService`, wild bans, special-form filters, type/BST/location constraints where applicable | Count each final pool stage that can feed `getRandomSpecies` or `getRandomSimilarStrengthSpecies`. |
| Trainer Pokemon | Post-filter pool used for normal, type-aware, local, and diversity-aware trainer replacements | Type-specific pools should report both the type pool and the all-species fallback when used. |
| Starters | Available starter pool after starter restrictions, ability-dependent exclusions, irregular/cosmetic exclusions, and mode-specific filters | This is the direct source for starter family ticket risk. |
| Static Pokemon | Mode-specific static pool after legendary/non-legendary/restricted filters, static bans, and special-form gates | Report separate rows for unrestricted, legend-preserving, non-legendary, and restricted-pool modes if present. |
| Rival starter carry | No independent candidate pool | Document as inherited from the starter choice. Count starter pool evidence, not a separate Rival pool. |

## 7. Sanitized Run Plan

If final evidence requires ROM load, Anton should run the helper locally and share only sanitized summary output.

Suggested local flow:

1. Run the helper/diagnostic locally with the private ROM and selected settings profile.
2. Write only aggregate TSV summaries to an ignored local output path.
3. Review the TSV before sharing or committing it.
4. Remove any ROM path, output ROM name, save reference, screenshot reference, full log line, hash, seed, username, or local directory.
5. Share or commit only the sanitized aggregate TSV/report if a later work package explicitly asks for it.

Suggested profile matrix:

| Profile label | Required settings summary |
| --- | --- |
| `gen1_9_alt_off_special_off` | Gen Limit 1-9, Alt-Forms OFF, Special Forms OFF/default |
| `gen1_9_alt_on_special_off` | Gen Limit 1-9, Alt-Forms ON, Special Forms OFF/default |
| `gen1_9_alt_off_special_on` | Gen Limit 1-9, Alt-Forms OFF, Special Forms allowed |
| `gen1_9_alt_on_special_on` | Gen Limit 1-9, Alt-Forms ON, Special Forms allowed |

For each profile, count Wild Pokemon, Trainer Pokemon, Starters, and Static Pokemon. Rival starter carry should be a short note pointing to the starter rows.

## 8. Decision Logic

A code fix becomes justified only after count evidence shows that flat per-entry sampling creates a real target-pool skew.

Evidence thresholds:

- `family_ticket_count > 1` for Unown in a target feature pool.
- A family share that is materially higher than a base-family-neutral expectation, especially if the same family would otherwise be one base species.
- Alt-Forms OFF still shows multiple DPE form entries for the same base family.
- Repeated sanitized samples or logs match the count-based expectation.

Count evidence is stronger than random samples because it measures the actual ticket pool before RNG. Samples are useful as confirmation, not as the primary proof.

Regional Forms require a separate policy decision. Multiple regional tickets are not automatically a bug because regional forms are often intended to be independent randomizer candidates. Functional forms such as Rotom, Arceus, Silvally, Ogerpon, Pumpkaboo, Gourgeist, Oricorio, Deoxys, and Genesect should not be deduplicated without an explicit design decision.

## 9. Fix Options After Evidence

| Option | Benefits | Drawbacks | Compatibility risk | Recommendation |
| --- | --- | --- | --- | --- |
| Keep flat | Preserves current UPR-FVX behavior and seed semantics | Leaves confirmed form-family skew in place | Lowest | Keep until count evidence justifies a change |
| Unown-only family ticket | Minimal targeted fix for the highest-risk cosmetic family | Does not address other form-heavy families | Low to medium | First fix candidate if only Unown is confirmed |
| Selected form-family tickets | Handles multiple confirmed cosmetic-like families | Needs source-backed family allowlist and careful policy review | Medium | Use only after counts identify repeated skew |
| Base-species-first then form | General solution for all forms | Broad behavior change; may collapse intentional regional/functional forms | High | Not recommended as a blanket change |
| Optional toggle | Lets users choose current flat behavior or family-balanced forms | Adds UI/profile/testing complexity | Medium to high | Later only, after evidence and Anton decision |

Recommendation: no code fix without counting evidence. If Unown is confirmed with many tickets in post-filter pools, start with an Unown-only or selected form-family ticket design. Do not globally deduplicate Regional Forms.
