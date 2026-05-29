# DPE Base Stats Gen9 tranche 1 plan smoke

Date: 2026-05-29
Branch: `analysis/dpe-base-stats-gen9-tranche-1-plan`
Result: `PASS_PLANNING_ONLY_WITH_BLOCKERS`

## Scope

This smoke covers the documentation-only selection of a first DPE `Base_Stats.c` update tranche from the read-only dry-diff.

No DPE/CFRU table, UPR-FVX code, submodule pin, Pokemon Showdown source, raw report, ROM, save, build, tool binary, screenshot, hash, private path, token, secret, or `.env` data is included.

## Commands

- `python3 07_scripts/data_audit/dpe_base_stats_dry_diff.py --showdown-data-dir <external-pokemon-showdown-data-dir> --limit 25`
- `python3 -m py_compile 07_scripts/data_audit/dpe_base_stats_dry_diff.py`

## Observed result

The dry-diff helper completed successfully and remained read-only.

Sanitized dry-diff counts used for planning:

- Tested Species: `1317`.
- Species `open-risk` skipped: `29`.
- Reviewed Species ignores skipped: `167`.
- Ability-blocked Species skipped from safe candidate promotion: `65`.
- Missing local entries after alias/ignore handling: `4`.
- Safe candidate Species with non-Ability field diffs: `225`.

Recommended tranche 1 candidates:

- Sneasel-Hisui.
- Sneasler.
- Ursaluna.
- Toedscool.
- Toedscruel.
- Primarina.
- Brionne.
- Sylveon.
- Magnezone.
- Crobat.

## Caveats

This is a plan only. The later real data PR must not expand beyond the listed candidates without another review pass.
