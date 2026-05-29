# DPE Base Stats Gen9 tranche 1 plan

Date: 2026-05-29
Branch: `analysis/dpe-base-stats-gen9-tranche-1-plan`
Scope: planning only; no DPE/CFRU table edits.

## Purpose

This plan selects a small first real DPE `Base_Stats.c` update tranche from the read-only dry-diff helper.

The goal is to make the later data PR easy to review: only clear non-Ability fields, no broad stat rebalance, no open-risk forms, and no generated raw report in the repository.

## Inputs

- Dry-diff helper: `07_scripts/data_audit/dpe_base_stats_dry_diff.py`.
- Reference input: external Pokemon Showdown `data/pokedex.ts`.
- Alias/risk input: `07_scripts/data_audit/showdown_aliases.json`.
- Local table inspected read-only: DPE `src/Base_Stats.c`.

Sanitized dry-diff context:

- Tested Species: `1317`.
- Species `open-risk` skipped by helper: `29`.
- Reviewed Species ignores skipped by helper: `167`.
- Species blocked from safe promotion by Ability blockers: `65`.
- Safe candidate Species with non-Ability field diffs: `225`.

## Selection criteria

Include only candidates that meet all of these:

- Species is not `open-risk`.
- Species is not a reviewed ignore.
- Candidate does not require Ability assignment changes.
- Candidate uses only non-Ability fields available from Showdown `pokedex.ts`.
- Candidate is small enough to review by hand.
- Candidate is not an obvious local stat buff or local custom type/balance policy.

Prefer:

- Gen7-Gen9 or later-form fixes.
- Clear type-order, gender-ratio, or egg-group corrections.
- Field changes with no dependency on moves, learnsets, TM/Tutor, Catch Rate, EXP Yield, EV Yield, or Growth Rate.

## Excluded fields

Do not include these in tranche 1:

- `ability1`, `ability2`, `hiddenAbility`.
- Catch Rate.
- Base EXP / EXP Yield.
- EV Yield.
- Growth Rate.
- Move data.
- Level-up learnsets.
- Egg moves outside `Base_Stats.c` egg-group fields.
- TM/HM compatibility.
- Tutor compatibility.
- Base stat changes that look like local balance buffs unless separately source-reviewed as Gen9 corrections.

## Excluded Species/Form groups

Tranche 1 excludes:

- All Species `open-risk` groups from the reviewed alias table: Alcremie cream/sweet forms, Basculin/Basculegion form semantics, Battle Bond Greninja, Pumpkaboo/Gourgeist sizes, Ogerpon mask-vs-form naming, Sinistea/Polteageist antique/chipped naming, Rockruff Dusk, and Tatsugiri form color/name semantics.
- Reviewed ignore groups: CAP/Fan/Pokestar/Totem/non-project keys, local sentinels/helpers, and cosmetic-only forms without a dedicated policy.
- Ability-blocked Species for Ability assignment purposes.
- Cosmetic Pikachu costume/cap entries in this first data PR, even where the dry diff shows egg-group or type differences.
- Gender-only representation diffs where local `PERCENT_FEMALE(100)` is equivalent to `MON_FEMALE`, or local `PERCENT_FEMALE(0)` is equivalent to `MON_MALE`.
- Egg-group order-only churn where both groups are already present and only order differs.
- Local custom/balance-looking type additions such as canonicalizing Psyduck, Meganium, or Samurott typing without a separate project policy.
- Early Kanto stat differences such as Butterfree, Beedrill, Pidgeot, Raticate, Fearow, Raichu, Sandslash, and similar local-looking buffs.

## Candidate tranche

Recommended tranche 1: 10 Species.

| Candidate | Local key | Planned fields | Current DPE | Showdown reference | Rationale | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| Sneasel-Hisui | `sneaselh` | `type1`, `type2` | `TYPE_POISON`, `TYPE_FIGHTING` | `TYPE_FIGHTING`, `TYPE_POISON` | Hisui form type order normalization; same type pair, later-form focused. | Low: mostly display/order, not damage chart behavior. |
| Sneasler | `sneasler` | `type1`, `type2` | `TYPE_POISON`, `TYPE_FIGHTING` | `TYPE_FIGHTING`, `TYPE_POISON` | Evolution of Hisui Sneasel; same clear type-order issue. | Low: mostly display/order. |
| Ursaluna | `ursaluna` | `type1`, `type2` | `TYPE_NORMAL`, `TYPE_GROUND` | `TYPE_GROUND`, `TYPE_NORMAL` | Later-form type order normalization. | Low: mostly display/order. |
| Toedscool | `toedscool` | `eggGroup1`, `eggGroup2` | `EGG_GROUP_GRASS`, `EGG_GROUP_GRASS` | `EGG_GROUP_FIELD`, `EGG_GROUP_FIELD` | Gen9 Species with clear egg-group mismatch. | Medium-low: breeding compatibility changes. |
| Toedscruel | `toedscruel` | `eggGroup1`, `eggGroup2` | `EGG_GROUP_GRASS`, `EGG_GROUP_GRASS` | `EGG_GROUP_FIELD`, `EGG_GROUP_FIELD` | Gen9 evolution with same clear egg-group mismatch. | Medium-low: breeding compatibility changes. |
| Primarina | `primarina` | `genderRatio` | `PERCENT_FEMALE(50)` | `PERCENT_FEMALE(12.5)` | Starter-line gender ratio correction; not a representation-only diff. | Medium-low: affects gender generation. |
| Brionne | `brionne` | `eggGroup1`, `eggGroup2` | `EGG_GROUP_MONSTER`, `EGG_GROUP_WATER_1` | `EGG_GROUP_WATER_1`, `EGG_GROUP_FIELD` | Clear middle-evolution egg-group mismatch. | Medium-low: breeding compatibility changes. |
| Sylveon | `sylveon` | `eggGroup1`, `eggGroup2` | `EGG_GROUP_FAIRY`, `EGG_GROUP_FAIRY` | `EGG_GROUP_FIELD`, `EGG_GROUP_FIELD` | Clear Eeveelution egg-group mismatch. | Medium-low: breeding compatibility changes. |
| Magnezone | `magnezone` | `eggGroup1`, `eggGroup2` | `EGG_GROUP_MONSTER`, `EGG_GROUP_MONSTER` | `EGG_GROUP_MINERAL`, `EGG_GROUP_MINERAL` | Clear species-family egg-group mismatch. | Medium-low: breeding compatibility changes. |
| Crobat | `crobat` | `eggGroup2` | `EGG_GROUP_FIELD` | `EGG_GROUP_FLYING` | Clear second egg-group mismatch, no stat/balance implication. | Low-medium: older Species, but field is narrow. |

## Later PR structure

Recommended real data PR:

1. Create a DPE-only branch for `Base_Stats.c` tranche 1.
2. Make exactly the 10 Species edits above, grouped in local table order.
3. Do not touch Ability fields, stats, Catch Rate, EXP Yield, EV Yield, Growth Rate, moves, learnsets, TM/Tutor compatibility, CFRU, UPR-FVX, or submodule pins.
4. Run DPE/CFRU syntax or build checks if locally available.
5. Add a sanitized smoke note that the PR is table-only and not a ROM/full-playthrough claim.

Suggested later DPE commit:

- `data: update dpe base stats tranche 1`

Suggested later workspace commit, if pin/docs are updated:

- `docs: pin dpe base stats tranche 1`

## Risks

- Egg-group edits can change breeding compatibility. This is intended for the selected candidates but should be reviewed explicitly.
- Type order edits should be low-risk but may affect display order or any code that reads `type1` preferentially.
- Gender-ratio edits affect generated gender distribution and should not be mixed with representation-only cleanups.
- This plan relies on Pokemon Showdown `pokedex.ts` for fields it actually exposes; unavailable fields remain excluded.
- No raw report was committed, so reviewers should rerun the dry-diff helper when preparing the real data PR.

## Handoff

Proceed to a later DPE data PR only after accepting this tranche. Keep the first implementation narrow: the 10 listed candidates, non-Ability fields only, no opportunistic cleanup.
