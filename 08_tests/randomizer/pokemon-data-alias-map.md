# Pokemon Data Alias Map Policy - Sanitized Full-Audit Summary

Date: 2026-05-29

Branch: `analysis/pokemon-data-alias-map`

Result: `PASS_SANITIZED_POLICY_SUMMARY_WITH_CAVEATS`

## Scope

This records a sanitized summary of the local full mapping audit against an external Pokemon Showdown `data/` directory and the resulting alias-/ignore-policy categories.

No Pokemon Showdown source files, raw audit reports, CFRU/DPE Pokemon data tables, UPR-FVX code, submodule pins, ROMs, saves, emulator states, builds, tool binaries, screenshots, hashes, private paths, tokens, secrets or `.env` data are committed.

## Summary Counts

- Species: Showdown-without-local `319`; local-without-Showdown `221`.
- Moves: Showdown-without-local `104`; local-without-Showdown `143`.
- Abilities: Showdown-without-local `36`; local-without-Showdown `8`.
- Local Ability alias define rows across CFRU/DPE headers: `67`.

## Policy Outcome

- Species unresolved rows are mostly form-name aliases, local shortforms, GMax/Giga names, CAP/fan content, local placeholders/extras, and a smaller true-risk set around form semantics.
- Move unresolved rows are mostly Z-Move and Max/GMax physical/special splits, Hidden Power typed variants, spelling aliases, ignored fan/mode content, local helper moves, and a smaller true-risk set around real moves without local constants.
- Ability unresolved rows are the highest-risk group because many local Gen9 names are aliases to older effects; name coverage must not be treated as behavior coverage.

## Caveats

- This is not a raw report and should not be used as a machine-readable import source.
- This does not change or validate CFRU/DPE Pokemon data tables.
- This does not claim move behavior correctness, ability behavior correctness, generated learnsets, TM/Tutor compatibility, local build success, BizHawk/Tracker behavior, full-playthrough coverage or P1 support.
