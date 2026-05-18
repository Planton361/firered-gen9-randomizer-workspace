# FVX Feature Test Status Matrix

## Purpose

`fvx_feature_test_status_matrix.tsv` is the machine-readable working list for every FVX feature ID currently listed in the dashboard's `## Vollstaendige Feature-Liste`.

The dashboard remains the human overview. The TSV is the per-feature execution ledger that can later be joined to the CLI profile matrix and updated one feature at a time.

## Status Model

`test_mode` values:

- `single`: tested as a focused single feature.
- `tab_full`: tested as part of a full GUI tab/profile block.
- `cumulative`: tested only as part of a broader cumulative profile.
- `risk_interaction`: passed or failed with an important interaction caveat.
- `manual_only`: not suitable for automated CLI-only evidence.

`log_status` values:

- `NOT_STARTED`: no current log evidence.
- `PLAN_READY`: scope is planned but not log-smoked.
- `TESTED_NON_ROM`: ROM-free test or harness evidence only.
- `PASS_LOG`: local log smoke passed in sanitized evidence.
- `PASS_LOG_WITH_CAVEAT`: local log smoke passed, but the row has a known caveat.
- `FAIL`: unexpected current failure.
- `EXPECTED_FAIL`: known blocked/risky profile until fixed.
- `OUT_OF_SCOPE`: deliberately excluded from the current matrix.

`ingame_status` values:

- `NOT_STARTED`: no ingame evidence.
- `NEEDS_INGAME_SMOKE`: log-level evidence exists, but a local play/visual check is still needed.
- `PASS_INGAME_SMOKE`: a sanitized local ingame smoke exists for this feature path.
- `MANUAL_ONLY`: evidence requires manual local inspection.
- `OUT_OF_SCOPE`: excluded from current smoke scope.

## CLI Profile Link

The `test_profile_id` column maps each feature to the profile IDs in `cli_profile_matrix.example.tsv`.

Current profile IDs:

- `00_baseline`
- `01_traits_full`
- `02_starters_statics_trades_full`
- `03_moves_movesets_full`
- `04_foe_base`
- `04_foe_held_items_basic`
- `05_wild_full`
- `06_tm_tutor_full`
- `07_items_full`
- `08_types_full`
- `09_graphics_palettes`
- `10_misc_tweaks`

`11_special_wild` remains out-of-scope in the current feature list because the dashboard tracks Standard/Fallback Wild features, not CFRU Day/Night/Special-Wild systems as supported FVX feature IDs.

## Current Caveats Captured

- Pokemon Traits tab is marked log-passed, including Evolutions and subsettings.
- Hard Evolution combinations are marked with constraint/fallback caveats.
- Starters, Statics and Trades are marked log-passed; Oak-Lab Rival sync has ingame smoke for `FVX-SST-002`.
- Static null placeholder entries remain null.
- Starter Held Items are marked log-passed.
- In-Game Trades Species/Nickname-visible path is marked log-passed; no `NEW GIVEN = ?` is recorded in the sanitized evidence.
- Moves and Movesets are marked log-passed.
- `Update Moves to Generation` is `OUT_OF_SCOPE` by design for the CFRU/DPE Gen9 basis.
- Foe base is marked log-passed.
- Trainer Class Names remains textlabel-only.
- Trainer Held Items basic is log-passed, but Sensible Items remains blocked/expected-fail because of the `getSensibleHeldItemsFor` NPE interaction.
- Trainer `Don't Use Legendaries` carries an expanded-pool caveat on the Trainer Pokemon base row.
- Special-Wild remains out-of-scope.
- Palettes/Graphics remain expected-fail or P2/out-of-scope.
- Misc Tweaks remain not started.
- No P1 promotion is made by this matrix.

## Updating Rows

When a new local run is reported:

1. Identify the profile ID and affected feature IDs.
2. Update only the affected TSV rows.
3. Use `PASS_LOG` only when the sanitized CLI/log report passed with no blocking markers.
4. Use `PASS_LOG_WITH_CAVEAT` when the log passed but the feature has a known scoped limitation.
5. Move `ingame_status` to `PASS_INGAME_SMOKE` only when the user reports sanitized local ingame evidence for that specific path.
6. Keep `known_caveat`, `blocker`, `evidence` and `next_step` concise and free of private data.

Do not put these into the TSV:

- ROM paths.
- Output ROM paths.
- ROM hashes or file hashes.
- Full logs or stack traces.
- Screenshots.
- Save files or emulator states.
- Private local paths.
- Secrets, tokens or `.env` values.

## Validation

Expected invariants:

- 130 feature rows after the header.
- No duplicate `feature_id` values.
- Every `Feature-ID` in `fvx-progress-dashboard.md` appears in the TSV.
- The dashboard's full feature list must not be shortened or replaced by this TSV.
