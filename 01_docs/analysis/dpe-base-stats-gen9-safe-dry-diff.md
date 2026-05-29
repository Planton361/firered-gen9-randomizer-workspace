# DPE Base Stats Gen9 safe dry diff

Date: 2026-05-29
Branch: `analysis/dpe-base-stats-gen9-safe-dry-diff`
Scope: read-only dry-diff only.

## Purpose

This pass adds a sanitized dry-diff path for comparing local DPE `src/Base_Stats.c` against an external Pokemon Showdown `data/pokedex.ts` checkout.

The helper does not write DPE/CFRU tables, does not copy Pokemon Showdown data into the repo, and does not commit raw diff reports.

## Helper

Added `07_scripts/data_audit/dpe_base_stats_dry_diff.py`.

Inputs:

- External Pokemon Showdown `data/` directory containing `pokedex.ts`.
- Reviewed alias table: `07_scripts/data_audit/showdown_aliases.json`.
- Existing normalization and TypeScript block parsing helpers from `07_scripts/data_audit/showdown_mapping_audit.py`.
- Local DPE `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c`, read-only.

The helper compares only mapped, non-ignored, non-open-risk Species. Ability assignment differences are reported separately and are not treated as safe update candidates while Ability blockers remain.

Fail-closed policy:

- Species `open-risk` entries are skipped.
- Reviewed Species `ignore` entries are skipped.
- Ability `behavior-risk`, `open-risk`, and `generator_policy = blocked` entries block the Species from safe candidate promotion.
- Uncategorized keys remain blocked by the upstream mapping/dry-run gate and are not solved here.
- Move risks do not enter this Base Stats helper.

## Dry-diff result

Sanitized local run against external Showdown `pokedex.ts`:

- Tested Species: `1317`.
- Skipped Species `open-risk`: `29`.
- Skipped reviewed Species ignores: `167`.
- Skipped from safe candidate promotion by Ability blockers: `65`.
- Missing local entries after alias/ignore handling: `4`.
- Safe candidate Species with non-Ability field diffs: `225`.
- Result: `PASS_READ_ONLY_WITH_BLOCKERS`.

Most frequent non-Ability field differences:

- `genderRatio`: `103`.
- `baseAttack`: `67`.
- `baseSpAttack`: `60`.
- `baseDefense`: `52`.
- `baseSpDefense`: `49`.
- `baseSpeed`: `48`.
- `eggGroup2`: `41`.
- `eggGroup1`: `39`.
- `baseHP`: `23`.
- `type2`: `17`.
- `type1`: `8`.

Ability assignment differences are intentionally analysis-only:

- `ability2`: `711`.
- `hiddenAbility`: `106`.
- `ability1`: `101`.

## Unavailable fields

Pokemon Showdown `pokedex.ts` did not provide the following DPE Base Stats fields in this source pass:

- Catch Rate.
- Base EXP / EXP Yield.
- EV Yield.
- Growth Rate.

Those fields need a secondary source before a real DPE update PR. They were not inferred and were not proposed as updates.

## Safe candidate sample

The first sanitized non-Ability diff candidates from the dry run:

- Butterfree.
- Butterfree-Gmax.
- Beedrill.
- Pidgeot.
- Raticate.
- Raticate-Alola.
- Fearow.
- Arbok.
- Pikachu-Cosplay.
- Pikachu-Rock-Star.

These are candidates for review, not generated table edits.

## Example diffs

Ten compact examples from the sanitized helper output:

- Butterfree: `baseSpAttack` DPE `100` vs ref `90`; `baseSpeed` DPE `90` vs ref `70`.
- Butterfree-Gmax: `baseAttack` DPE `40` vs ref `45`; `baseDefense` DPE `90` vs ref `50`; `baseSpAttack` DPE `140` vs ref `90`; `baseSpDefense` DPE `90` vs ref `80`.
- Beedrill: `baseAttack` DPE `110` vs ref `90`; `baseSpDefense` DPE `90` vs ref `80`.
- Pidgeot: `baseAttack` DPE `90` vs ref `80`; `baseSpAttack` DPE `90` vs ref `70`.
- Raticate: `baseAttack` DPE `100` vs ref `81`.
- Raticate-Alola: `baseAttack` DPE `90` vs ref `71`.
- Fearow: `baseAttack` DPE `120` vs ref `90`; `baseSpeed` DPE `110` vs ref `100`.
- Arbok: `baseHP` DPE `70` vs ref `60`; `type2` DPE `TYPE_DARK` vs ref `TYPE_POISON`.
- Pikachu-Cosplay: gender representation/field difference plus egg-group differences.
- Pikachu-Rock-Star: `type2` difference plus gender representation/field and egg-group differences.

## Risks and caveats

- This is a dry diff, not a DPE data update.
- Gender-only examples can include representation differences such as local `PERCENT_FEMALE(100)` versus Showdown female-only notation.
- Ability differences are intentionally excluded from update candidates until the Ability behavior-risk table is resolved or explicitly scoped out.
- Catch Rate, EXP Yield, EV Yield, and Growth Rate need a separate trusted source before any generated update.
- No full raw report is committed.
- No CFRU/DPE data table, UPR-FVX code, submodule pin, Pokemon Showdown source, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret, or `.env` data is included.

## Handoff

Recommended first real data PR: a narrow DPE Base Stats update tranche for reviewed non-open-risk Species and non-Ability fields only, with Catch Rate / EXP Yield / EV Yield / Growth Rate excluded until a secondary source is chosen.
