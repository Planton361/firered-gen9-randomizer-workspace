# Exact Coverage Batches 03-18

## Scope

This evidence records sanitized local exact-coverage CLI log-smoke results for batches 03 through 18.

Codex did not run a ROM smoke. The local run details remain private and only the sanitized aggregate result is recorded here.

## Common Sanitized Summary

- Dry run: no for batches 03 through 17.
- Batch 18 was a no-ROM helper validation for unsupported generator overlays.
- ROM path/hash/full log documented: no.
- Output paths documented: no.
- P1 promotion: no.
- Bad markers: 0 for all PASS batches.
- Warnings: 0 for all PASS batches.

## Batch Results

| Batch | Area | Profiles processed | Sanitized result | Notes |
|---:|---|---:|---|---|
| 03 | TM/Tutor | 15 | PASS | `single_fvx_tm_001` through `single_fvx_tm_015` passed CLI log-smoke. |
| 04 | Wild | 12 | PASS | `single_fvx_wild_001` through `single_fvx_wild_012` passed CLI log-smoke. Special-Wild remains separate. |
| 05 | Foe | 16 | PASS_WITH_CAVEAT | `variant_foe_held_items_basic`, `risk_foe_held_items_sensible` and `single_fvx_foe_001` through `single_fvx_foe_014` passed CLI log-smoke. Sensible held items remains caveated because of previous NPE history. |
| 06 | General + Traits | 30 | PASS | `single_fvx_gen_001`, `single_fvx_gen_002` and `single_fvx_trait_001` through `single_fvx_trait_028` passed CLI log-smoke. |
| 07 | Starters/Statics/Trades | 23 | PASS_WITH_CAVEAT | Starter/static variants and `single_fvx_sst_002` through `single_fvx_sst_015` passed CLI log-smoke. `FVX-SST-001` Custom Starters remains manual/unsupported. |
| 08 | Moves | 10 | PASS | `single_fvx_move_001` through `single_fvx_move_005` and `single_fvx_move_007` through `single_fvx_move_011` passed CLI log-smoke. `FVX-MOVE-006` remains by-design off/out-of-scope for CFRU/DPE Gen9. |
| 09 | Graphics/Palettes | 9 | PASS_WITH_CAVEAT | Palette variants, graphics/palettes risk profile and `single_fvx_gfx_001` through `single_fvx_gfx_004` passed CLI log-smoke. These rows still need visual smoke. `FVX-GFX-005` and `FVX-GFX-006` remain manual/unsupported. |
| 10 | Misc | 17 | PASS_WITH_CAVEAT | Misc groups and `single_fvx_misc_001` through `single_fvx_misc_012` passed CLI log-smoke. These rows still need behavior-specific ingame/manual smoke. |
| 11 | General | 2 | PASS | `single_fvx_gen_001` and `single_fvx_gen_002` passed CLI log-smoke. `FVX-GEN-003` and `FVX-GEN-004` were not covered in this batch. |
| 12 | Types | 5 | PASS_WITH_CAVEAT | `variant_type_effectiveness_random_balanced`, `risk_type_effectiveness_chaos` and `single_fvx_type_001` through `single_fvx_type_003` passed CLI log-smoke. TypeEffectiveness remains a gameplay-disruptive mode family that needs focused ingame validation before stronger support claims. |
| 13 | Cumulative | 10 | PASS | `00_baseline` through `08_types_full` passed CLI log-smoke. |
| 14 | Foe mode variants | 5 | PASS | `variant_foe_mode_random`, `variant_foe_mode_even_distribution`, `variant_foe_mode_main_playthrough`, `variant_foe_mode_type_themed` and `variant_foe_mode_keep_themed` passed CLI log-smoke. |
| 15 | Wild location variants | 5 | PASS | `variant_wild_location_encounter_set`, `variant_wild_location_map`, `variant_wild_location_named_location`, `variant_wild_location_game` and `variant_wild_location_catch_em_all` passed CLI log-smoke. |
| 16 | TypeEffectiveness exact variants | 5 | PASS_WITH_CAVEAT | `variant_type_effectiveness_random`, `variant_type_effectiveness_random_balanced`, `variant_type_effectiveness_keep_identities`, `variant_type_effectiveness_inverse` and `risk_type_effectiveness_chaos` passed CLI log-smoke. TypeEffectiveness remains gameplay-disruptive and needs focused ingame validation. |
| 17 | Intro Mon | 1 | PASS_WITH_CAVEAT | `variant_intro_random` passed CLI log-smoke. Ingame sprite mismatch and visual confirmation remain open. |
| 18 | Gen-Limit unsupported | 4 | EXPECTED_FAIL | `MODE-GEN-LIMIT-1-9`, `MODE-GEN-LIMIT-1-9-NO-RELATIVES`, `MODE-GEN-LIMIT-1-9-NO-MEGAS` and `MODE-GEN-LIMIT-1-9-NO-GMAX` failed as expected with exit code 1. Status: `EXPECTED_FAIL` / `UNSUPPORTED_BY_SETTINGS_FORMAT`. |

## Matrix Impact

- Generator-capable rows covered by batches 03 through 18 are updated with CLI log-smoke evidence only.
- `ingame_status` still requires local boot/play, visual smoke, behavior smoke or manual follow-up depending on the feature.
- Graphics/Palettes, sensible Trainer Held Items, TypeEffectiveness exact variants and Intro Mon remain caveated.
- Gen-Limit-1-9 `MODE-*` overlays remain unsupported by the current Settings format and are not promoted.
- Manual/unsupported rows remain manual or out-of-scope.
- No P1 promotion follows from these log-smoke results.

No ROMs, output ROMs, full logs, private paths, hashes, screenshots, saves, emulator states, secrets, tokens or `.env` values are documented.
