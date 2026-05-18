# Exact Coverage Batches 03-13

## Scope

This evidence records sanitized local exact-coverage CLI log-smoke results for batches 03 through 13.

Codex did not run a ROM smoke. The local run details remain private and only the sanitized aggregate result is recorded here.

## Common Sanitized Summary

- Dry run: no.
- ROM path/hash/full log documented: no.
- Output paths documented: no.
- P1 promotion: no.
- Bad markers: 0 for all batches.
- Warnings: 0 for all batches.

## Batch Results

| Batch | Area | Profiles processed | Sanitized result | Notes |
|---:|---|---:|---|---|
| 03 | TM/Tutor | 15 | PASS | `FVX-TM-001` through `FVX-TM-015` passed CLI log-smoke. |
| 04 | Wild | 12 | PASS | `FVX-WILD-001` through `FVX-WILD-012` passed CLI log-smoke. Special-Wild remains separate. |
| 05 | Foe | 16 | PASS | `FVX-FOE-001` through `FVX-FOE-014` plus held-items risk profiles passed CLI log-smoke. Sensible held items remains caveated because of previous NPE history. |
| 06 | General + Traits | 30 | PASS | `FVX-GEN-001`, `FVX-GEN-002` and `FVX-TRAIT-001` through `FVX-TRAIT-028` passed CLI log-smoke. |
| 07 | Starters/Statics/Trades | 23 | PASS | `FVX-SST-002` through `FVX-SST-015` passed CLI log-smoke. `FVX-SST-001` Custom Starters remains manual/unsupported. |
| 08 | Moves | 10 | PASS | `FVX-MOVE-001` through `FVX-MOVE-005` and `FVX-MOVE-007` through `FVX-MOVE-011` passed CLI log-smoke. `FVX-MOVE-006` remains by-design out-of-scope for CFRU/DPE Gen9. |
| 09 | Graphics/Palettes | 9 | PASS_WITH_CAVEAT | `FVX-GFX-001` through `FVX-GFX-004` passed CLI log-smoke and still need visual smoke. `FVX-GFX-005` and `FVX-GFX-006` remain manual/unsupported. |
| 10 | Misc | 17 | PASS | `FVX-MISC-001` through `FVX-MISC-012` passed CLI log-smoke and still need behavior-specific ingame/manual smoke. |
| 11 | General | 2 | PASS | `FVX-GEN-001` and `FVX-GEN-002` passed CLI log-smoke. `FVX-GEN-003` and `FVX-GEN-004` were not covered in this batch. |
| 12 | Types | 5 | PASS_WITH_CAVEAT | `FVX-TYPE-001`, `FVX-TYPE-002` and `FVX-TYPE-003` passed CLI log-smoke. Exact Random/Keep/Inverse variants remain a generator-overlay gap if unsupported. |
| 13 | Cumulative | 10 | PASS | Baseline through `08_types_full` passed CLI log-smoke. |

## Matrix Impact

- Generator-capable rows covered by batches 03 through 13 are updated with CLI log-smoke evidence only.
- `ingame_status` still requires local boot/play, visual smoke, behavior smoke or manual follow-up depending on the feature.
- Manual/unsupported rows remain manual or out-of-scope.
- No P1 promotion follows from these log-smoke results.

No ROMs, output ROMs, full logs, private paths, hashes, screenshots, saves, emulator states, secrets, tokens or `.env` values are documented.
