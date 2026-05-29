# Pokemon data generator dry-run plan

Date: 2026-05-29
Branch: `analysis/pokemon-data-generator-dry-run-plan`
Scope: read-only dry-run/audit planning only.

## Purpose

This plan defines a fail-closed dry-run path for comparing external Pokemon Showdown data against local CFRU/DPE table shapes and the reviewed alias table.

The dry run does not write CFRU/DPE data tables, does not vendor Pokemon Showdown data, and does not commit raw comparison reports.

## Helper

Added `07_scripts/data_audit/pokemon_data_dry_run.py`.

Inputs:

- External Pokemon Showdown `data/` directory containing `pokedex.ts`, `learnsets.ts`, `moves.ts`, and `abilities.ts`.
- Reviewed alias table: `07_scripts/data_audit/showdown_aliases.json`.
- Existing local constants parsed through `07_scripts/data_audit/showdown_mapping_audit.py`.
- Existing local DPE/CFRU table files for count/shape checks only.

The helper is read-only. It prints a compact status summary and exits successfully when the dry-run gate runs, even if the result is blocked by reviewed policy.

Fail-closed blockers:

- Any uncategorized Showdown-only or local-only key.
- Any alias table entry with `status = open-risk`.
- Any alias table entry with `status = behavior-risk`.
- Any alias table entry with `generator_policy = blocked`.

## Dry-run result

Against the local external Pokemon Showdown checkout, the dry run reported:

- Species mapping gate: `0` Showdown uncategorized, `0` local uncategorized, `29` `open-risk/open-risk` blockers.
- Move mapping gate: `0` Showdown uncategorized, `0` local uncategorized, `13` `open-risk/lgpe-partner-move` blockers and `1` `open-risk/missing-engine-move` blocker.
- Ability mapping gate: `0` Showdown uncategorized, `0` local uncategorized, `13` `behavior-risk/alias-plus-hook`, `5` `behavior-risk/behavior-risk`, `3` `behavior-risk/name-mismatch`, and `8` `open-risk/missing-local` blockers.
- Overall result: `BLOCKED_BY_REVIEWED_POLICY`.

This is the intended result. The reviewed alias table now classifies unresolved names, but true data generation remains blocked until the open behavior/form risks are accepted, fixed, or explicitly excluded.

## Data blocks

| Block | Needed inputs | Blocking categories | Expected dry-run output | Risk | First real implementation PR |
| --- | --- | --- | --- | --- | --- |
| Base Stats | Showdown `pokedex.ts`; DPE `Base_Stats.c`; local species constants; reviewed alias table | Species `open-risk/open-risk` | Sanitized per-species base-stat diff plan; no C writes | Medium-high: form semantics, typing/stat fields, catch/EXP/held-item fields, and broad table churn | Base stats for non-blocked species only, with generated diff summary and DPE rebuild smoke |
| Ability Assignments | Showdown `pokedex.ts`; Showdown `abilities.ts`; DPE `Base_Stats.c`; local ability constants; reviewed alias table | Species `open-risk`; Ability `behavior-risk`, `name-mismatch`, `alias-plus-hook`, and `missing-local` | Sanitized ability-assignment diff plan; no DPE writes | High: Gen9-looking local Ability names can alias older CFRU behavior | Ability assignments only after blocked Ability behavior risks are accepted, fixed, or explicitly excluded |
| Level-up Learnsets | Showdown `learnsets.ts`; DPE `Learnsets.c`; CFRU `level_up_learnsets.c`; local species/move constants; reviewed alias table | Species `open-risk`; Move `open-risk` | Sanitized learnset diff plan for DPE/CFRU sync; no table writes | Medium-high: duplicated DPE/CFRU tables and move behavior gaps | Narrow non-blocked learnset tranche with CFRU/DPE parity check |
| Egg Moves | Showdown `learnsets.ts`; DPE `Egg_Moves.c`; local species/move constants; reviewed alias table | Species `open-risk`; Move `open-risk` | Sanitized egg-move diff plan; no DPE writes | Medium: compact marker format can corrupt adjacent species if generated incorrectly | Egg moves after species and move blockers are accepted or excluded |
| TM Compatibility | Showdown `learnsets.ts`; DPE `TM_Tutor_Tables.c`; DPE `tm_compatibility/*.txt`; local TM/move order; reviewed alias table | Species `open-risk`; Move `open-risk` | Sanitized TM compatibility diff plan; no compatibility writes | High: TM order/count and generated bitsets are brittle | TM compatibility only after move IDs and TM order are frozen |
| Tutor Compatibility | Showdown `learnsets.ts`; DPE `TM_Tutor_Tables.c`; DPE `tutor_compatibility/*.txt`; local tutor/move order; reviewed alias table | Species `open-risk`; Move `open-risk` | Sanitized tutor compatibility diff plan; no compatibility writes | High: tutor count/order and reminder/menu bitsets are the most brittle path | Tutor compatibility last, after TM compatibility and move behavior decisions |

## Policy

The first real generator should produce only sanitized diff summaries by default. It must require a separate explicit implementation PR before writing any CFRU/DPE data table.

Recommended behavior:

- Run mapping gate first.
- Refuse to generate write patches if any required kind has uncategorized keys.
- Refuse to generate write patches for any block whose required kinds contain `open-risk`, `behavior-risk`, or `generator_policy = blocked`.
- Allow block-specific dry diff summaries for non-blocked subsets only if the subset explicitly excludes blocked species/moves/abilities and documents the exclusion.
- Keep raw Showdown data and raw full reports outside the repo.

## Handoff

Next useful step: decide the first narrow implementation tranche. The safest first real PR is a base-stats-only dry diff for non-blocked species/forms, still with no table writes until the sanitized diff is reviewed.
