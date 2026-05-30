# DPE Base Stats full source sync smoke

Date: 2026-05-30
Branch: `analysis/dpe-base-stats-full-source-sync`
Result: `PASS_READ_ONLY_NO_FULL_REPLACE_RECOMMENDED`

## Scope

This smoke documents a read-only audit for whether local DPE `src/Base_Stats.c` can be fully or mostly replaced from another current Gen9-compatible source.

No DPE/CFRU/UPR-FVX source file, submodule pin, Pokemon Showdown checkout, external repository, ROM, save, build artifact, tool binary, screenshot, raw report, hash, private path, token, secret, or `.env` data was changed.

## Sources checked

- Local DPE `src/Base_Stats.c`, `include/base_stats.h`, `include/species.h`, `include/abilities.h`, and `include/types.h`.
- Planton DPE `origin/master` merge commit `34f88ab9fb2d23db715297016f00d1c5e30b064d`.
- Shiny-Miner DPE Gen9 `master` commit `5906aa4d4904e41393fd9184a16951c961e96263`.
- Skeli789 DPE `master` commit `cdfc053a56326a13dc5311b24488445e17536b7e`.
- pokeemerald-expansion Pokemon data as shape/reference only.
- Pokemon Showdown `data/pokedex.ts` as reference only.

## Sanitized findings

- Local DPE and Planton DPE `origin/master` are compatible and have no audited-file tree diff. This confirms the accepted local source line; it does not provide a new replacement.
- Shiny-Miner DPE Gen9 uses the same DPE struct/header shape but is behind local accepted data. A full replace from it would remove local accepted Ogerpon Terastal rows and tranche-1 fields.
- Skeli789 DPE is not Gen9-compatible for this purpose; it ends before the local Gen9 tail.
- pokeemerald-expansion and Pokemon Showdown are useful references but not drop-in C table sources.

## Decision

Full replace: no.

Partial/field-based updates: yes, but only through the reviewed alias table and fail-closed dry-diff workflow. Ability fields remain blocked by local alias/behavior risk until separately accepted or fixed.

## Checks

- `git status --short`.
- `git diff --stat`.
- `git diff --check`.

## Caveats

No local build, ROM boot, BizHawk validation, Ironmon Tracker validation, full playthrough, or P1 promotion is claimed.
