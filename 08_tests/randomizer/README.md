# Current update

- `212_gen_limit_special_form_item_smoke.md` records sanitized local Gen-Limit / Special-Form / Mechanic-Item smoke evidence.
- Workspace branch `randomizer/sync-gen-limit-special-form-item-smoke` pins `02_external/upr-fvx` to merged UPR-FVX compat commit `765d8ec0ab298bbaab4aa9f8f31b93c7259a47e5`, including the fix chain through PR #150.
- Gen Limit / Special Form / Mechanic Item Exclusions status is `PASS_TARGETED_LOG_VISUAL_SMOKE_WITH_CAVEATS`.
- Sanitized local evidence: Gen-Limit 1-9 infrastructure works; Gen1-only and Gen1-6 log smokes looked correct; Gen7/8/9 Intro Mon no longer crashes and supports valid visual-table candidates; Mega/GMax/Regional/Irregular/Special-form filtering works in latest local checks; Evolutionary Relatives remain an explicit cross-gen-family override; Regional forms are not pulled in by Evolutionary Relatives unless Regional Forms across Gen Limit is enabled.
- Additional evidence: Trainer Class Sprite Sync is GUI-exposed and should be enabled when Trainer Class Names are randomized; Oak-Lab Rival counter-starter is preserved independently of Rival Carries Starter Through Game; mechanic item filtering uses source-backed CFRU/DPE categories for Mega/Z/Dynamax-GMax items; no current Pokemon special-form filtering issue was observed after latest checks.
- Caveat: targeted local smoke only; no full playthrough; Plates/Drives/Memories/Nectars are categorized but have no separate user-facing policies yet; Static Script/Gift/NPC item sources remain caveated if outside randomizer item replacement pools; custom/future form encodings outside documented CFRU/DPE identity blocks remain audit-required.
- No ROM run by Codex and no P1 promotion is added.

# Current update

- `210_misc_tweaks_behavior_smoke.md` records sanitized local Misc Tweaks behavior-smoke evidence after the merged UPR-FVX Misc fixes.
- Workspace branch `randomizer/sync-misc-tweaks-behavior-smoke` pins `02_external/upr-fvx` to merged UPR-FVX PR #127 commit `155fac0b33474f6ed5b3fbaed7dd9bf24b4e1315`, including PR #125 Running Shoes tweaks, PR #126 Catching Tutorial species mapping and PR #127 Fast Egg Hatching missing-`BreedingInfo` guard.
- Misc Tweaks status is `PASS_TARGETED_BEHAVIOR_SMOKE_WITH_CAVEATS`.
- Sanitized local evidence: Fastest Text pass, Randomize PC Potion pass, Run Without Running Shoes pass, Running Shoes Indoors pass, Randomize Catching Tutorial pass with no question-mark sprite/name, Fast Egg Hatching crash-free randomization/output-load and Ban Lucky Egg likely pass / no issue observed.
- Reusable TMs and Forgettable HMs are CFRU-provided for the stable profile and should not be duplicated by UPR-FVX.
- Caveat: targeted behavior smoke only; no full playthrough, no full hatch-cycle proof, no dedicated stronger Ban Lucky Egg proof and no P1 promotion.
- No ROM run by Codex and no P1 promotion is added.

# Current update

- `211_type_effectiveness_battle_smoke.md` records sanitized local Type Effectiveness battle-smoke evidence.
- Type Effectiveness status is `PASS_TARGETED_BATTLE_SMOKE_WITH_CAVEATS`.
- Sanitized local evidence: Type Effectiveness was tested in battle, effectiveness behavior looked appropriate and no battle crashes were reported.
- Caveat: targeted battle smoke only, not a full type-chart matchup matrix, not a full playthrough and not a P1 promotion.
- No ROM run by Codex and no P1 promotion is added.

# Current update

- `209_graphics_palettes_visual_smoke.md` records sanitized local Graphics/Palettes visual/audit smoke evidence.
- Workspace branch `randomizer/sync-graphics-palettes-visual-smoke` pins `02_external/upr-fvx` to merged UPR-FVX PR #124 commit `0eb815418470fa1ac000695b95d09cb084338dca`, including PR #123 palette output writes and PR #124 expanded trainer logging fallback.
- Graphics/Palettes visual/audit smoke status is local targeted pass with caveats.
- Sanitized evidence: `Pokemon Palettes: Randomized/Changed`; CFRU-DPE palette copy save `normalPaletteWriteAttempts=841`; Palette Audit `sampledCount=21`, `normalChangedCount=21`, `shinyChangedCount=0`, `unchangedCount=0`; sampled Charmander/Squirtle/Caterpie/Pikachu/Blissey normal palettes changed from base; changed palettes visually observed.
- Final run had no `Error during logging`.
- Caveat: targeted visual/audit smoke only, not full-playthrough coverage, broad species/form coverage, shiny behavior proof or P1 promotion.
- No ROM run by Codex and no P1 promotion is added.

# Current update

- Local ignored manual input `05_builds/randomizer-smoke/settings/manual/graphics_palettes_smoke.rnqs` is prepared for a future isolated Graphics/Palettes visual smoke.
- It reuses the generated `risk_graphics_palettes_visual` settings-profile artifact; no RNQS fields were guessed or byte-patched.
- Intended Feature-ID scope: `FVX-GFX-001` through `FVX-GFX-004`.
- Excluded: Wild, Foe, Items, Misc, TypeEffectiveness/type chaos, Custom Player Graphics and Character-to-Replace.
- No evidence file is updated, no ROM run by Codex occurred and no P1 promotion is added.

# Current update

- Workspace branch `randomizer/sync-wild-encounter-output-audit` pins `02_external/upr-fvx` to merged UPR-FVX PR #118 commit `ed692d07bfc81405706f2b94fda06639426e6a75`.
- Wild Encounter Base-vs-Output Audit is available for Gen3/FRLG/CFRU-DPE.
- The audit is diagnostic-only and does not change writer or randomizer behavior.
- Scope: modeled Gen3 base `WildPokemon` table path. CFRU/DPE special/runtime wild sources remain follow-up if audit and ingame observations diverge.
- No ROM run by Codex and no P1 promotion is added.

# Current update

- `208_combined_trainer_visual_runtime_smoke.md` records sanitized local combined trainer visual runtime smoke evidence.
- Combined trainer visual runtime smoke status is `PASS_WITH_CAVEATS`.
- Intro Mon was visibly randomized.
- Player starter was Charmander; Oak-Lab Rival starter was Squirtle; Route 22 Rival starter was Squirtle.
- Route 22 Rival sprite was randomized and consistent with the Oak-Lab Rival sprite.
- Route 22 Rival non-starter Pokemon observed: Silvally Lv9.
- Interpretation: Rival Carries Starter Through Game protects/corrects the Rival starter slot only; non-starter Rival Pokemon remain eligible for Foe Pokemon randomization.
- Viridian Forest trainer sprites were randomized.
- No crash/freeze/garbled sprite was observed.
- No ROM run by Codex and no P1 promotion is added.

# Current update

- `207_rival_counter_starter_and_combined_visual_smoke.md` records sanitized local evidence for merged UPR-FVX PR #117.
- Workspace branch `randomizer/sync-rival-counter-starter-and-visual-smoke` pins `02_external/upr-fvx` to merge commit `5983011752273e00c402e25cc1ae1a9baca110f1`.
- Rival Carries Starter Through Game is locally smoke-confirmed for the sampled counter path: Player Charmander -> Rival Squirtle.
- Combined visual profile smoke passed for the targeted checks.
- Intro Mon Species `0` regression is fixed in the sampled profile; visible Intro Mon was Blissey.
- Trainer Class Sprite Sync remains visually okay from prior checks: Viridian Forest trainers get per-trainer randomized classes/sprites and Rival keeps a consistent class/sprite across appearances.
- Caveat: targeted visual smoke only, not full-playthrough coverage or P1 promotion.
- No ROM run by Codex and no P1 promotion is added.

# Current update

- `206_trainer_class_sprite_sync.md` records the workspace sync for final merged UPR-FVX PR #116.
- Workspace branch `randomizer/sync-trainer-class-sprite-sync-final` pins `02_external/upr-fvx` to merge commit `36dd431d059bc69eb1bee3311200e28c872c6cc9`.
- `MODE-TRAINER-CLASS-SPRITE-SYNC` is locally smoke-confirmed for targeted visual consistency.
- `Randomize Trainer Names` remains separate and changes no `classId`/`pic`.
- Without the mode, `Randomize Trainer Class Names` remains legacy/textlabel-only.
- With the mode, Sprite Sync follows the Trainer Class Names assignment and syncs class label / classId / visible `trainerPic`.
- Regular trainers use per-trainer class/sprite assignments. Rival/Friend rows use grouped class/sprite consistency. Runtime-source rows are included where eligible.
- Sanitized local evidence: Viridian Forest Bug Catcher classes randomize per trainer, Rival keeps the first randomized sprite across later appearances, other sampled trainers appeared aligned, and no garbled sprite/crash was reported.
- Caveat: targeted visual smoke only, not full-playthrough coverage.
- No ROM run by Codex and no P1 promotion is added.

# Current update

- `205_intro_mon_visual_source_fix_smoke.md` records sanitized local smoke evidence for merged UPR-FVX PR #109.
- Workspace branch `randomizer/sync-intro-mon-visual-source-fix` pins `02_external/upr-fvx` to merged UPR-FVX PR #109 commit `a9bb4a5f201c5078ec02fe1f2f8417695448afe9`.
- PR #109 fixes the CFRU/DPE Gen9 BPRE Intro Mon visual mismatch by syncing the Nidoran female `PokemonFrontImages` and `PokemonNormalPalettes` entries to the selected intro species' asset pointers when Intro Mon is randomized.
- Previous sanitized finding: known FRLG Intro sources changed from Nidoran female to Hitmontop, but the visible ingame Oak intro sprite stayed Nidoran female.
- Local smoke after PR #109 observed the visible Oak intro sprite changed away from Nidoran female, with no crash, freeze or garbled sprite.
- Status impact: `FVX-GEN-003` / Intro Mon visual mismatch is locally fixed for the targeted smoke.
- Caveat: targeted ingame smoke only, not full-playthrough coverage. No ROM run by Codex and no P1 promotion is added.

# Current update

- Workspace branch `randomizer/sync-intro-mon-visual-source-diagnostics` pins `02_external/upr-fvx` to merged UPR-FVX PR #107 commit `a7e098a5158d824b1ddec62a286f2a6ffafce8e4`.
- PR #107 adds an opt-in Intro Mon Visual-Source diagnostic for known FRLG Intro Mon literals/pointers and optional Base-ROM vs randomized Output-ROM comparison.
- `No Random Intro Mon` is documented as the negative GUI option; `randomizeIntroMon=true` is the active Randomize Intro Mon path.
- `MODE-INTRO-RANDOM` sets true; `MODE-NO-RANDOM-INTRO` and `FVX-GEN-003` set false.
- This is diagnosis-only: no visible Intro Mon fix, no ROM run by Codex and no P1 promotion are added.
- Sanitized future evidence should include only candidate source names, offsets, raw/decoded species, `changedFromBase` yes/no and observed visible Intro Mon label.

# Current update

- `204_runtime_source_trainer_randomization_smoke.md` records expanded sanitized local evidence for merged UPR-FVX PR #105.
- Workspace branch `randomizer/sync-runtime-source-trainer-randomization-smoke` keeps `02_external/upr-fvx` pinned to PR #106 commit `5bb1d853f132095922be2aceef55af2878192b85`.
- PR #105 makes generic `RUNTIME-SOURCE` trainers randomizer-eligible as regular trainers while preserving known Rival 2/Brock special tags; this smoke evidence remains compatible with PR #106 post-audit tooling.
- Local targeted audit for Viridian Forest trainer IDs `531/532` showed randomized loaded/raw parties with `loadedRawPartyComparison=match`.
- Ingame smoke observed the formerly vanilla Metapod/Caterpie Viridian Forest trainer showing Eiscue.
- Randomized output audit reported `trainer runtime source audit mode=unloaded-valid-parties` with `total=0`.
- Additional sanitized examples: Rival 2 trainer IDs `329/330/331` show randomized parties; Brock trainer ID `414` shows `[Drifloon Lv12, Growlithe Lv14]`.
- Loaded-mismatch, invalid-pointer, empty-party, out-of-range rows and full playthrough coverage remain follow-up scope. No ROM run by Codex and no P1 promotion is added.

# Current update

- Workspace branch `randomizer/sync-runtime-trainer-post-audit` pins `02_external/upr-fvx` to merged UPR-FVX PR #106 commit `5bb1d853f132095922be2aceef55af2878192b85`.
- PR #106 adds the opt-in Pre/Post Runtime-Trainer-Audit for local comparison of a private Base-ROM and private randomized Output-ROM.
- The report is audit-only and helps check valid script-referenced runtime trainer rows for changed-from-base state, loaded/raw output comparison and warning markers.
- This sync adds no new Writer, Sync or Randomizer behavior, and no ROM run by Codex.
- Local users should compare their Base-ROM and randomized Output-ROM locally and post only sanitized trainer IDs, party summaries, classifications, warning markers and pass/fail observations.
- No P1 promotion is added.

# Current update

- `203_runtime_source_trainer_randomization_smoke.md` records sanitized local evidence for merged UPR-FVX PR #105.
- Workspace branch `randomizer/sync-runtime-source-trainer-randomization` pins `02_external/upr-fvx` to merge commit `c0d8e33f3547020c6fd2fe5baffbc80ec93f9197`.
- PR #105 makes generic `RUNTIME-SOURCE` trainers randomizer-eligible as regular trainers while preserving known Rival 2/Brock special tags.
- Local targeted audit for Viridian Forest trainer IDs `531/532` showed randomized loaded/raw parties with `loadedRawPartyComparison=match`.
- Ingame smoke observed the formerly vanilla Metapod/Caterpie Viridian Forest trainer showing Eiscue.
- Loaded-mismatch, invalid-pointer, empty-party and out-of-range rows remain diagnosis/follow-up scope. No ROM run by Codex and no P1 promotion is added.

# Current update

- Workspace branch `randomizer/sync-strict-runtime-trainer-source-sync` pins `02_external/upr-fvx` to merged UPR-FVX PR #104 commit `6dcda7e499cd3e22319c447c7d7df9ddbd67de60`.
- PR #104 adds strict auto-sync for valid FRLG/CFRU-DPE `trainerbattle` runtime-source TrainerData rows classified as `VALID_RUNTIME_NOT_LOADED`.
- Trainer/Foe remains CLI-log-clean; local private-ROM audit plus ingame smoke is still required before stronger support claims.
- Viridian Forest trainer IDs `531/532` should be covered by strict sync if the local audit still classifies them as `VALID_RUNTIME_NOT_LOADED`.
- Loaded-mismatch, invalid-pointer, empty-party and out-of-range audit rows remain diagnosis/follow-up scope.
- No ROM run, output ROM, private path, full log or P1 promotion is added.

# Current update

- Workspace branch `randomizer/sync-runtime-trainer-party-fix` pins `02_external/upr-fvx` to merged UPR-FVX PR #102 commit `eabbcd7eccb1703f98000f85669d969f516e1247`.
- PR #102 fixes the confirmed CFRU/DPE FireRed runtime Trainer Pokemon mismatch for Rival 2 trainer IDs `329/330/331` and Brock trainer ID `414`.
- The fix loads and saves validated raw FRLG `trainerbattle` runtime-source `TrainerData` rows outside the normal loaded trainer count, so those rows are no longer only visible through diagnostics.
- Foe Trainer remains CLI-log-clean; ingame smoke remains required before stronger support claims.
- Additional vanilla-looking trainers should only be added after targeted redacted runtime-source evidence.
- No ROM run, output ROM, private path, full log or P1 promotion is added.

# Current update

- `202_trainer_runtime_source_diagnostics_sync.md` records the workspace sync for merged UPR-FVX PR #100.
- Workspace pin: `02_external/upr-fvx` now points to merge commit `87bba797620dd2043f02c11c67f7b752a7238a00`.
- PR #100 adds No-ROM/synthetic trainerbattle runtime-source diagnostics for FRLG script trainer IDs, `TrainerData` rows, party pointers and first raw party species.
- The opt-in runtime-source report remains local-only and must not be run by Codex with a ROM.
- Foe Trainer is CLI-log-clean from exact coverage, but ingame status remains partial/caveated until local sanitized runtime-source evidence confirms affected battles use the logged/written `TrainerData` source.
- No ROM run, output ROM, private path, full log or P1 promotion is added.

# Current update

- Workspace branch `randomizer/sync-settings-profile-variant-overlays` pins `02_external/upr-fvx` to merged UPR-FVX PR #99 commit `4c8e7394a230e6e8471977036be268c80883ac0b`.
- PR #99 extends the No-ROM `settings-profile` helper with exact `MODE-*` overlays for Foe Pokemon modes, Wild replacement/location modes, TypeEffectiveness modes and Intro Mon toggles.
- `cli_profile_matrix.coverage.example.tsv` now includes disabled opt-in exact variant rows for Foe mode, Wild location, TypeEffectiveness and Intro random/no-random coverage.
- Unsupported Gen-Limit-1-9 mode rows are documented as disabled expected-fail rows because the current Settings format cannot represent Gen 8/9 restrictions or GMax exclusion.
- No ROM run, output ROM, private path, full log or P1 promotion is added.

- `201_exact_coverage_batches_03_18.md` records the sanitized exact-coverage Batch 03 through 18 CLI log-smoke/helper results.
- Batches 03 through 17 processed 165 generator-capable exact/cumulative/mode profiles across TM/Tutor, Wild, Foe, General/Traits, Starters/Statics/Trades, Moves, Graphics/Palettes, Misc, Types, cumulative coverage and exact mode overlays.
- All Batch 03 through 17 PASS profiles had 0 bad markers and 0 warnings; Batch 18 confirmed 4 Gen-Limit `MODE-*` overlays fail as expected because they are unsupported by the current Settings format.
- Updated `fvx_feature_test_status_matrix.tsv` for the affected generator-capable rows while preserving caveats for Graphics/Palettes, sensible Trainer Held Items, Intro Mon visual confirmation, Special-Wild, static placeholders and manual/unsupported rows.
- No ROM paths, hashes, full logs, output paths or P1 promotion are documented.

# Current update

- `200_exact_coverage_batch_02_items.md` records the sanitized exact-coverage Batch 02 CLI log-smoke result for Item Feature IDs.
- 13 exact Item single/variant profiles were processed with dry-run disabled.
- All 13 profiles passed with 0 bad markers and 0 warnings.
- Updated `fvx_feature_test_status_matrix.tsv` only for `FVX-ITEM-001` through `FVX-ITEM-010`.
- The updated rows remain below P1: log-pass evidence still needs local boot/play or item-specific ingame smoke.
- No ROM paths, hashes, full logs, output paths or P1 promotion are documented.

# Current update

- `199_exact_coverage_batch_01.md` records the sanitized exact-coverage Batch 01 CLI log-smoke result.
- 19 exact single/variant profiles were processed with dry-run disabled.
- All 19 profiles passed with 0 bad markers and 0 warnings.
- Updated `fvx_feature_test_status_matrix.tsv` only for the requested Feature IDs: `FVX-TRAIT-017`, selected Starter/Static variants and selected Foe variants.
- The updated rows remain below P1: log-pass evidence still needs local boot/play or feature-specific ingame smoke.
- No ROM paths, hashes, full logs, output paths or P1 promotion are documented.

# Current update

- `198_cli_profile_matrix_coverage_run.md` records the sanitized coverage-generated `.rnqs` CLI profile matrix result.
- 14 coverage profiles were processed with dry-run disabled.
- PASS profiles and UNEXPECTED_PASS profiles all reported 0 bad markers and 0 warnings.
- Unexpected passes remain caveated: Sensible Trainer Held Items, Graphics/Palettes, Misc Tweaks and Special-Wild.
- `fvx_feature_test_status_matrix.tsv` is updated only where the executed coverage profile exactly enabled the Feature ID through the profile/feature overlay set.
- No ROM paths, hashes, full logs, output paths or P1 promotion are documented.

# Current update

- `fvx_profile_coverage_plan.md` audits the generated settings profiles against all 130 FVX Feature IDs.
- `cli_profile_matrix.coverage.example.tsv` adds an opt-in coverage manifest with single, variant, tab, cumulative and risk-interaction profile IDs.
- `generate_settings_profiles_from_matrix.sh` now accepts an optional `feature_overlays` TSV column and can generate profiles via explicit `--enable` Feature IDs instead of only built-in UPR-FVX profile IDs.
- The audit identifies features that were previously only covered by related broad profiles, including missing `Random Every Level`, several Starter/Static variants, Foe variants and Item mode variants.
- This is No-ROM coverage planning only: no ROM run, output ROM, private path, full log or P1 promotion is added.

# Current update

- `197_cli_profile_matrix_generated_run.md` records the sanitized generated `.rnqs` CLI profile matrix result.
- 14 profiles were processed; every profile produced CLI log smoke pass or unexpected pass.
- Bad markers and warnings were 0 for all profiles.
- Unexpected passes are now caveated instead of treated as stable: Sensible Trainer Held Items, Graphics/Palettes, Misc Tweaks and Special-Wild.
- `fvx_feature_test_status_matrix.tsv` is updated to reflect log-pass evidence while keeping ingame/manual smoke requirements and no P1 promotion.

# Current update

- `196_settings_profile_generator_sync.md` documents the synced UPR-FVX Settings Profile Generator from PR #98.
- `generate_settings_profiles_from_matrix.sh` derives `.rnqs` files from a local base settings file and the profile matrix manifest by calling `UPR-FVX.jar settings-profile`.
- The generator path is No-ROM only: it accepts no ROM argument, runs no randomization and creates no output ROM.
- The profile matrix can now move from saved GUI-exported profiles to generated profiles under ignored local directories.
- Real ROM CLI matrix runs remain local-only user work and no P1 promotion is made.

# Current update

- `195_fvx_feature_test_status_matrix.md` documents the machine-readable per-feature status matrix.
- `fvx_feature_test_status_matrix.tsv` tracks all 130 dashboard Feature IDs with profile mapping, log status, ingame status, caveats, blockers, evidence anchors and next steps.
- The dashboard remains the human overview; the TSV is the CLI-profile-matrix worklist.
- This historical matrix-update block recorded the sanitized knowledge at the time; later updates now supersede Graphics/Palettes and Misc Tweaks with targeted smoke caveats, while Trainer Class Names remains legacy/textlabel-only without Sync, Trainer held Sensible Items remains expected-fail, Special-Wild remains out-of-scope and no P1 promotion is made.
- No ROMs, logs, output ROMs, private paths or P1 promotion are added.

# Current update

- `194_cli_profile_matrix_pipeline.md` documents the second CLI smoke stage: a profile matrix runner for multiple saved FVX settings profiles.
- `cli_profile_matrix.example.tsv` lists the current roadmap profile IDs from `00_baseline` through `11_special_wild`.
- `run_cli_profile_matrix.sh` executes enabled manifest rows through `cli_log_smoke_pipeline.sh` and writes a sanitized aggregate table with `profile_id | result | bad markers | warnings | next action`.
- `generate_cli_smoke_profiles.sh` creates only a manifest scaffold. It does not byte-patch or generate `.rnqs` settings because FVX settings are versioned Base64 plus CRC/checksum state.
- Real matrix runs remain local-only with private ROM/settings paths under ignored output directories. Codex may only use dry-run or artificial fixtures.
- No P1 promotion is made.

# Current update

- `193_cli_log_smoke_pipeline.md` documents the local-only UPR-FVX CLI log smoke pipeline.
- `07_scripts/randomizer/cli_log_smoke_pipeline.sh` wraps `UPR-FVX.jar cli` for opt-in local runs, requests detailed logging with `-l` and writes a sanitized summary report.
- The helper supports `--dry-run` for repo checks without reading a ROM or creating an output ROM.
- CLI smoke evidence must stay sanitized: no ROM paths, output paths, hashes, full logs, screenshots, saves, emulator states, secrets, tokens or `.env` data.
- This is pipeline/tooling evidence only and does not promote P1.

# Current update

- `192_starter_rival_sync_pass.md` records the sanitized Starter/Rival sync smoke after syncing UPR-FVX PR #97.
- Workspace pin: `02_external/upr-fvx` now points to merge commit `51d52a03235664154549105003dadfb45c76d0d0`.
- Root cause: Oak-Lab Rival uses raw `TrainerData` party rows outside the normal loaded trainer list; PR #97 corrects the slot projection to `[328, 326, 327]`.
- Evidence: starter slots Groudon, Fearow and Mudbray; player chose Groudon; expected Rival Fearow; observed Rival Fearow.
- Starter Pokemon passed for the Oak-Lab first Rival smoke.
- No vanilla fallback, same-starter bug, crash or softlock was observed.
- Stable Visual Profile can now optionally include Starter Pokemon for local sampling.
- `Rival Carries Starter Through Game` remains separate and not tested by this smoke.
- No P1 promotion is made.

# Current update

- `191_stable_visual_profile_smoke.md` records the sanitized Stable Visual Profile smoke after the merged GUI Working Settings Matrix baseline.
- Stable Visual Profile ON: Wild Standard/Fallback, Trainer Pokemon core, Pokemon Movesets -> Random completely, Trainer Movesets, Trainer Names, Field Items basic, Pokemon Abilities, TM/HM Compatibility, TM Moves, Move Tutor Moves, Move Tutor Compatibility, Shop Items, Pickup Items, In-Game Trades, Static Pokemon, Type Effectiveness, Pokemon Base Statistics and Move Data Power/Accuracy/PP/Type/Names.
- Stable Visual Profile OFF: Starter Pokemon, Trainer Class Names, Evolution Randomization and Special-Wild/Day-Night/Swarms.
- Evidence: randomization completed, output ROM booted, a short run was played, wild encounters worked and a trainer battle worked.
- Items/shops/moves/abilities showed no blockers during the short run; evolutions unchanged remain expected.
- No missing sprites, move-less Pokemon, crash, freeze or softlock were observed in this short smoke.
- Known exclusions remain: Starter/Rival sync, Trainer Class Names visual mismatch and Special-Wild out-of-scope.
- No P1 promotion is made.

# Current update

- `190_gui_working_settings_matrix.md` records the sanitized GUI Working Settings Matrix after syncing UPR-FVX PR #88 and PR #89.
- Workspace pin: `02_external/upr-fvx` now points to merge commit `f3a6d04ff6db8d48468800194e0baffbafb7505c`.
- Evidence: Wild Standard/Fallback, Trainer Pokemon core, Pokemon Movesets -> Random completely, Trainer Movesets, Trainer Names, Field Items basic, Pokemon Abilities, TM/HM Compatibility, TM Moves, Move Tutor Moves, Move Tutor Compatibility, Shop Items, Pickup Items, In-Game Trades, Static Pokemon, Type Effectiveness, Pokemon Base Statistics and Move Data Power/Accuracy/PP/Type/Names are recorded as passed in sanitized local evidence.
- In-Game Trades no longer show `NEW GIVEN = ?` after PR #89.
- Evolutions unchanged are preserved and swarms remain disabled by CFRU `SWARM_CHANCE=0`.
- Caveats: Trainer Class Names is textlabel remapping only and should stay off for visual consistency; Starter rival first-battle sync remains unresolved; Special-Wild remains out-of-scope; Shop Items evidence covers supported/special shops; Static null placeholders remain null; Base Stats ability-name log display may appear truncated while ingame names are correct.
- No P1 promotion is made.

# Current update

- `190_trainer_names_class_names_pass.md` records the sanitized Trainer Names/Class Names GUI-smoke after syncing UPR-FVX PR #83, PR #85 and PR #86.
- Workspace pin: `02_external/upr-fvx` now points to merge commit `f86315e7528ba3257df03b80c0c75ccc69ef574b`.
- Evidence: Trainer Names are visibly changed in the Trainer Pokemon log.
- Evidence: Trainer Class Names no longer collapse to `Director` or `[PKMN] BREEDER`.
- Trainer Class Names pass as global class-label remapping: the same original class gets the same new class label.
- Per-trainer class assignment is not part of this option and remains a separate possible future feature.
- Evolutions remain correct, including Squirtle -> Wartortle Lv16.
- Wild Standard/Fallback, Trainer Pokemon core and Pokemon Movesets -> Random completely remain stable; swarms remain disabled.
- Missing sprites observed: no. Move-less Pokemon observed: no. No P1 promotion is made.

# Current update

- `189_cfru_dpe_evolution_row_stride_fix.md` records the sanitized Evolution Report evidence after syncing UPR-FVX PR #82.
- Workspace pin: `02_external/upr-fvx` now points to merge commit `485f0b899c84470f3fab82317331a671ec023ac1`.
- Evidence: CFRU/DPE uses `EVOS_PER_MON=16`; PR #82 uses `evolutionSlotsPerSpecies=16` and `evolutionRowSize=0x80` for CFRU/DPE Gen9 evolution rows.
- Input ROM starter chains correct and new Output ROM starter chains correct in sanitized local report evidence.
- Correct starter chain baseline: Bulbasaur -> Ivysaur Lv16, Ivysaur -> Venusaur Lv32, Charmander -> Charmeleon Lv16, Charmeleon -> Charizard Lv36, Squirtle -> Wartortle Lv16 and Wartortle -> Blastoise Lv36.
- Sanitized ingame smoke evidence: Squirtle evolved at Lv16 in a new FVX output.
- Previous bad/Test13-style outputs are stale and must not be used. Next recommended option block is a separate Trainer Names/Class Names or first Items/Moves/Abilities slice. No P1 promotion is made.

# Current update

- `188_gui4b_learnsets_no_swarms_pass.md` records the sanitized GUI-4B pass after syncing UPR-FVX PR #79, UPR-FVX PR #80 and CFRU PR #5.
- Workspace pins now include UPR-FVX `226bcacc4f66cee5689caa128d5e35ef4acc001d` and CFRU `c4c90373fe7f24acd5dcfa3a8fbdd5cb573bfe29`.
- Evidence: correct CFRU/DPE Gen9 ROM loaded with `isRomHack=true`, PokemonCount 1439, PokedexCount 1290 and generations 1-9 present; Wild Standard/Fallback plus Trainer Pokemon core plus Pokemon Movesets -> Random completely passed.
- Output ROM was created locally, emulator boot succeeded, wild encounters and a trainer battle were checked, missing sprites were not observed and move-less Pokemon were not observed.
- Learnset empty-moveset crash was not reproduced. CFRU `SWARM_CHANCE=0` was confirmed; Route 1 no-swarm rebuild did not observe Swarm-Frigibax and an example Route 1 encounter was Urshifu Lv3 displayed correctly.
- Ogerpon remains valid and pool-eligible. Remaining guarded invalid palette candidates are known warnings and not blockers. Day/Night/Special-Wild remain out-of-scope. No P1 promotion is made.

# Current update

- `187_gui4a_wild_trainer_ogerpon_pass.md` records the sanitized GUI-4A pass after syncing UPR-FVX PR #78.
- Workspace pin: `02_external/upr-fvx` now points to merge commit `18e184b2c22451c74b4ba46bd7203c579d3bc9e7`.
- Evidence: correct CFRU/DPE Gen9 ROM loaded with `isRomHack=true`, PokemonCount 1439, PokedexCount 1290 and generations 1-9 present; Wild Standard/Fallback plus Trainer Pokemon core randomization completed; output ROM was created locally; emulator boot, wild encounter check and trainer battle check passed.
- Missing sprites observed: no. Move-less Pokemon observed: no.
- Ogerpon appears in Trainer output/log and is pool-eligible after the Learnset/Sprite/Palette fixes.
- Day/Night Wild, Swarms and other Special-Wild systems remain out-of-scope. Remaining invalid asset candidates are known and guarded. No P1 promotion is made.

# Current update

- `186_ogerpon_asset_fix_sync.md` records the sanitized Pool Asset Report evidence after syncing DPE PR #2 and UPR-FVX PR #77.
- Workspace pins now include DPE `3d0ac870fadc91e55f6ff19c0f7aae3cac2014a1` and UPR-FVX `d6415d59a8b94b4d6d4c1e424a73c0f426993d03`.
- Evidence: accepted count after guard improved to 1186, excluded count is 6, no usable learnset exclusions remain at 1, invalid/missing front battle sprite pointer exclusions dropped to 5, and invalid/missing normal palette pointer exclusions dropped to 5.
- Ogerpon internal slots 1422..1429 now report movesLearntCount 20, learnsetPointerValid true, frontSpritePointerValid true and palettePointerValid true.
- Ogerpon status: accepted. No P1 promotion is made.

# Current update

- `185_cfru_dpe_learnset_runtime_fixes_sync.md` records the sanitized Pool Asset Report evidence after syncing UPR-FVX PR #76, CFRU PR #3, CFRU PR #2 and DPE PR #1.
- Workspace pins now include UPR-FVX `808cbe823772187ec3ecc13e484a87eb449aaac5`, CFRU `1c99ca5abeeb577f8214247e523e62575443bb81` and DPE `0a1ca7811fd00f981dad19d7476b92513fe62cdc`.
- Evidence: accepted count after guard improved to 1185, excluded count is 7, no usable learnset exclusions dropped to 1, and Ogerpon now reports movesLearntCount 20 with learnsetPointerValid true.
- Remaining blocker: Ogerpon is still excluded because of invalid/missing front battle sprite pointer. No P1 promotion is made.

# Current update

- `184_gui_e2e_wild_smoke_pass.md` records the first sanitized GUI E2E Wild smoke pass on UPR-FVX pin `04bdd8b2f2769bedb1bf6c6ff8fcdecbbf84e29c`.
- Evidence: correct CFRU/DPE Gen9 ROM loaded yes, PokemonCount 1439, PokedexCount 1290, generation counts include 4-9 yes, Wild Standard/Fallback only randomization completed yes, output ROM created yes, BizHawk boot yes, first wild encounter reached yes, first encounter species Avalugg Lv2, private paths/logs/hashes/screenshots omitted yes.
- Statuswirkung: GUI-0 through GUI-3 passed for the minimal Wild Standard/Fallback route. No new P1 promotion; Wild Standard/Fallback was already P1-supported.
- Next GUI step: GUI-4 with one option group at a time, preferably Trainer-Core or Learnsets, not full randomization.

# Current update

- UPR-FVX PR #68 is merged and `02_external/upr-fvx` now pins `04bdd8b2f2769bedb1bf6c6ff8fcdecbbf84e29c`.
- The GUI-0 blocker in `RandomizerGUI.populateDropdowns()` is fixed by filtering null Species out of GUI dropdown Species lists.
- Sanitized local GUI-0 result: GUI opened yes, custom ROM loaded yes, randomization not yet, output ROM not yet, private paths/logs/hashes/screenshots omitted yes.
- Statuswirkung: GUI-0 passed for Custom ROM load; GUI-1 Wild Standard/Fallback only is next. No Output-ROM evidence and no P1 promotion.

# Current update

- `gui_e2e_smoke_pipeline.md` defines the fastest local GUI E2E smoke order for the private custom ROM: GUI load only, then Wild Standard/Fallback only, then local emulator boot, then first wild encounter. It also defines the sanitized yes/no feedback format and keeps Trainer Names/Class Names, Learnsets, Items/Moves/Abilities and Special Wild systems disabled initially. No ROM/GUI/emulator smoke was run and no P1 promotion was made.

# Current update

- UPR-FVX PR #67 is merged and `02_external/upr-fvx` now pins verified merge commit `9bde3d4e2f983bfb96875c5fe9697f87763d8665`.
- Trainer Names/Class Names now have an opt-in ROM-facing smoke harness in `Gen3TrainerTextRomSmokeTest`; default no-ROM execution skips cleanly with Tests 1, Skipped 1, Failures 0, Errors 0.
- Statuswirkung: harness prepared only; no private local ROM smoke is documented, no ROM path/hash/full log/output ROM is documented, byte-exact Terminator/Padding inspection is not directly proven and no P1 promotion was performed.
- Note: the expected SHA `a5a8887e0dac0bdbe4bfe87bfdc2e7a27fb79b75` was not the actual PR #67 merge commit; PR #67 resolves to merge commit `9bde3d4e2f983bfb96875c5fe9697f87763d8665`.

# Current update

- `183_wild_encounters_p1_decision.md` records the separate P1 decision for Wild Encounters.
- Statuswirkung: Standard/Fallback Wild Encounters are now `P1-supported` for the documented writer/reload scope in the tested private target context.
- Scope boundary: CFRU Day/Night Wild, Swarms, Roamers, DexNav, Raids, Wild Double Battles and other special Wild systems remain separate and non-promoted.
- No new ROM execution, UPR-FVX code change, submodule pin change, ROM path/hash/full log or output ROM was added.

# Current update

- UPR-FVX PR #66 is merged and `02_external/upr-fvx` now pins `f4d0cbbe3143cab4b963d2444b8354d97fa96403`.
- PR #66 fixes the Gen3 Evolution load blocker that stopped the opt-in Wild Encounter ROM smoke before the Wild Encounter writer/reload portion.
- `182_wild_encounters_rom_smoke_evidence.md` records sanitized local ROM-facing evidence: `Gen3WildEncounterRomSmokeTest` passed with Tests 1, Failures 0, Errors 0, Skipped 0.
- Statuswirkung: Wild Encounters is a P1 candidate, not P1-promoted; promotion requires a separate short decision/evaluation.
- No ROM path, hash, full log or output ROM is documented.

# Current update

- UPR-FVX PR #65 is merged and `02_external/upr-fvx` now pins verified merge commit `f224862c91aed8e7a75fe843f5088cadea734da4`.
- Wild Encounters now have an opt-in ROM-facing smoke harness in `Gen3WildEncounterRomSmokeTest`; default no-ROM execution skips cleanly.
- Statuswirkung: harness prepared only; no private local ROM smoke was executed, no ROM path/hash/log/output ROM is documented and no P1 promotion was performed.
- Note: the requested SHA `c7a07a4643a570b2e27de059804f1a249616aaf0` was not reachable in the UPR-FVX fork; PR #65 resolves to merge commit `f224862c91aed8e7a75fe843f5088cadea734da4`.

# Current update

- UPR-FVX PR #64 is merged and `02_external/upr-fvx` now pins `d49837fea305157a2fe94f3f57d09cedc8ab25f8`.
- Wild Encounters now have ROM-free synthetic Writer/Reload Equality evidence in `WildCatchLevelDecisionTest`: a reloadable fake `RomHandler` deep-copies `setEncounters(...)` data and reloads fresh `getEncounters(...)` copies.
- Statuswirkung: Writer/Reload Equality evidence only at synthetic ROM-free level; no real Gen3 byte writer proof, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #63 is merged and `02_external/upr-fvx` now pins `d88a0cdb8c11473d2a3448028e937422eaf38679`.
- Items/Moves/Abilities now have a third ROM-free Slice in `ItemDecisionTest`: `ItemRandomizer.randomizeFieldItems()` for Non-TM Field Items covers the non-bad allowed Item pool, bad/key-style exclusions, non-empty output, stable Field-Item count and high Item IDs `1001..1003`.
- Statuswirkung: ROM-free evidence only; no ROM-facing Reload evidence, Writer/Reload smoke, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #62 is merged and `02_external/upr-fvx` now pins `a5b1b63b134149bd88e62af27a9b45332f617d9e`.
- Items/Moves/Abilities now have a second ROM-free Slice in `TMTutorMoveDecisionTest`: `TMTutorMoveRandomizer.randomizeTMMoves()` covers allowed Move pool, exclusion of HM/game-breaking/levelup-banned/illegal Moves, preserved Field-Move-TM slot, stable output count and high Move IDs `1001..1003`.
- Statuswirkung: ROM-free evidence only; no ROM-facing Reload evidence, Writer/Reload smoke, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #61 is merged and `02_external/upr-fvx` now pins `c365b96399ed36881ed637edce0721c059c442d1`.
- Items/Moves/Abilities now have a first ROM-free Ability-Test-Slice in `SpeciesAbilityDecisionTest`: `SpeciesAbilityRandomizer` covers allowed Ability pool, banned Ability exclusion, non-empty two-Ability output and Species-ID-`1025` path.
- Statuswirkung: ROM-free evidence only; no ROM-facing Reload evidence, Writer/Reload smoke, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #60 is merged and `02_external/upr-fvx` now pins `c40fbbd796db5b43a3bc53e547dc890a853cef20`.
- Learnsets now have a fourth ROM-free Test-Slice in `LearnsetDecisionTest`: Evolution Moves for All adds exactly one Level-0 Evolution-Move slot, preserves existing Level-1/later level slots and Move pool, and keeps Species ID `1025` in the path.
- Statuswirkung: ROM-free evidence only; no ROM-facing Reload evidence, Writer/Reload smoke, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #59 is merged and `02_external/upr-fvx` now pins `0d217db45086d8d03b4eb606ae2621633396d768`.
- Learnsets now have a third ROM-free Test-Slice in `LearnsetDecisionTest`: Guaranteed Starting Moves adds the expected Level-1 slots, preserves the later level slot and Move pool, and keeps Species ID `1025` in the path.
- Statuswirkung: ROM-free evidence only; no ROM-facing Reload evidence, Writer/Reload smoke, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #58 is merged and `02_external/upr-fvx` now pins `6ed75f5b1e5b8b354e2db694c880407c8e0a10dd`.
- Learnsets now have a second ROM-free Option-Test-Slice in `LearnsetDecisionTest`: `orderDamagingMovesByDamage()` sorts damaging Moves by damage, leaves Evolution-/Non-Damaging-Slots unchanged, preserves Level-/Slot-Anzahl and Move pool, and keeps Species ID `1025` in the path.
- Statuswirkung: ROM-free evidence only; no ROM-facing Reload evidence, Writer/Reload smoke, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #57 is merged and `02_external/upr-fvx` now pins `56cae7eb0c2ddc626dc31c4802d3f696a42959bf`.
- Learnsets now have a first ROM-free Unit-Test-Slice in `LearnsetDecisionTest`: `randomizeMovesLearnt()` keeps Learnsets non-empty, preserves Level-/Slot-Anzahl, selects from the allowed Move pool and processes high Species ID `1025`.
- Statuswirkung: ROM-free evidence only; no ROM-facing Reload evidence, Writer/Reload smoke, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #56 is merged and `02_external/upr-fvx` now pins `b3b9a8ab5e8726f4b4d2d4e23efa733cce7287ac`.
- Wild Encounters now have a third ROM-free Option-Test-Slice in `WildCatchLevelDecisionTest`: `BlockWildLegendaries` is checked synthetically so legendary Species stay out of the replacement pool while Slot-/Level-/Area structure remains stable.
- Statuswirkung: ROM-free evidence only; no ROM-facing Reload evidence, Writer/Reload smoke, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #55 is merged and `02_external/upr-fvx` now pins `8f88e25d458996b560189ba23d3216ee0c775f14`.
- Wild Encounters now have a second ROM-free Multi-Area-/Multi-Slot Unit-Test-Slice in `WildCatchLevelDecisionTest`: unterschiedliche Areas, Slot-Anzahlen und Levelbereiche bleiben strukturell stabil; selected Species stay in the allowed pool including high IDs above `1000`.
- Statuswirkung: ROM-free evidence only; no ROM-facing Reload evidence, Writer/Reload smoke, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #54 is merged and `02_external/upr-fvx` now pins `8d67f8686e16b3a9d3e77da5789a06889a645e5f`.
- Wild Encounters now have a first ROM-free Unit-Test-Slice in `WildCatchLevelDecisionTest`: Slot-/Level-/Area structure remains preserved, encounter areas stay non-empty, and selected Species stay in the allowed pool including high IDs above `1000`.
- Statuswirkung: ROM-free evidence only; no ROM-facing Reload evidence, Writer/Reload smoke, output ROM, Randomizer run or P1 promotion was performed.

# Current update

- UPR-FVX PR #53 is merged and `02_external/upr-fvx` now pins `955c852cf07f155a046b18865a39e6912a6ee09c`.
- Trainer Class Names Length Check now uses internal/encoded length instead of Java `changeTo.length()`; the focused ROM-free `TrainerNameRandomizerTest` passed in PR #53.
- Statuswirkung: Trainer Names/Class Names remains `tested-non-rom`, not P1-supported; no ROM-facing Reload evidence, Terminator/Padding proof, decoded reload equality or P1 promotion was performed.

# Current update

- `031_trainer_names_text_length_unit_evidence.md`: records merged UPR-FVX PR #52 and pins `02_external/upr-fvx` to `7357b244e01ef2c7790b858d50c19c31ac72e955`.
- The pinned ROM-free `TrainerNameRandomizerTest` extension covers Trainer Names/Class Names text-length risks with synthetic encoded/internal length data: ASCII inside limit, exactly at limit, over limit, Java length != internal length, escaped-token-style length divergence and the Class-Names `changeTo.length()` risk.
- Statuswirkung: Trainer Names/Class Names remains `tested-non-rom`, not P1-supported; no ROM-facing Writer/Reload, Terminator/Padding proof, decoded reload equality, Text-Encoding safety claim or P1 promotion was performed.

# Current update

- `027_trainer_rom_reload_text_evidence_plan.md`: read-only plan for later Trainer ROM-/Reload-/Text-Encoding evidence. It keeps current Trainer suboptions at `tested-non-rom`, separates missing ROM/reload proof from text-encoding and `changeTo.length()` risks, and defines criteria for any later narrowly scoped P1 promotion.

# Current update

- `181_trainer_names_followup.md`: records merged UPR-FVX PR #51 and pins `02_external/upr-fvx` to `d20eb1367c62a4f14c8778bc61ad6904ea76a6d6`.
- The pinned `TrainerNameRandomizerTest` covers `FVX-FOE-013` Trainer Names/Class Names with synthetic Non-ROM data: `canChangeTrainerText=false`, singles-/doubles-pool selection, repeated-name translation, `MAX_LENGTH`, `MAX_LENGTH_WITH_CLASS`, Class-Name pools and fixed class-name length.
- Statuswirkung: Trainer Names/Class Names is now `tested-non-rom`, not P1-supported; no Gen3 Writer-/Reload-ROM evidence, ROM-Smoke, text-encoding proof, output-ROM or Randomizer run was performed.

# Previous update

- `180_trainer_battle_style_followup.md`: records merged UPR-FVX PR #50 and pins `02_external/upr-fvx` to `5e2d351966ce4a96d02cdb6ca676b39bde7a9505`.
- The pinned `TrainerBattleStyleTest` covers `FVX-FOE-011` with synthetic Non-ROM Trainer data: `UNCHANGED`, `SINGLE_STYLE`, deterministic `RANDOM` and too-few-Pokemon skips.
- Statuswirkung: Battle Style is now `tested-non-rom`, not P1-supported; no ROM-Smoke, Trainer Writer-/Reload-ROM evidence, Trainer Names/Class Names/Text work, output-ROM or Randomizer run was performed.

# Previous update

- `179_trainer_special_rules_followup.md`: records merged UPR-FVX PR #49 and pins `02_external/upr-fvx` to `bc46fdc49741643d8f09dd302b67b5b2d35d24c5`.
- The pinned `TrainerSpecialRulesTest` covers `FVX-FOE-010`, `FVX-FOE-012` and `FVX-FOE-014` with synthetic Non-ROM Trainer, Party, Species and Evolution data.
- Statuswirkung: Trainer Special Rules for League Unique, Rival Carries Starter and Trainers Evolve Their Pokemon + Level Modifier are now `tested-non-rom`, not P1-supported; `FVX-FOE-011` Battle Style and `FVX-FOE-013` Trainer Names/Class Names/Text remain separate; no ROM-Smoke, Trainer Writer-/Reload-ROM evidence, output-ROM or Randomizer run was performed.

# Current update

- `178_trainer_additional_pokemon_followup.md`: records merged UPR-FVX PR #48 and pins `02_external/upr-fvx` to `32ab7d969e5439d38e5781670c9a68e0ea418d0a`.
- The pinned `TrainerAdditionalPokemonTest` covers `FVX-FOE-005`, `FVX-FOE-006` and `FVX-FOE-007` with synthetic Non-ROM Trainer/Party/Species data, including safe-template cloning, max party size 6 and multi-battle limit 3.
- Statuswirkung: Trainer Additional Pokemon for Boss, Important and Regular Trainers is now `tested-non-rom`, not P1-supported; no ROM-Smoke, Trainer Writer-/Reload-ROM evidence, Trainer Names/Class Names/Text work, output-ROM or Randomizer run was performed.

# Current update

- `177_trainer_type_diversity_followup.md`: records merged UPR-FVX PR #47 and pins `02_external/upr-fvx` to `ea5269706eb7d04eb0b305f88e8fa20bfb21f92a`.
- The pinned `TrainerTypeDiversityGuardTest` covers `FVX-FOE-009` Force Diverse Types / Type Themes with synthetic Non-ROM Trainer and Species data, including the old null Primary/Secondary Type guard path.
- Statuswirkung: `FVX-FOE-009` is now `tested-non-rom`, not P1-supported; no ROM-Smoke, Writer-/Reload-ROM evidence, Trainer Names/Class Names/Text work, output-ROM or Randomizer run was performed.

# Current update

- `176_wild_catch_level_followup.md`: records merged UPR-FVX PR #46 and pins `02_external/upr-fvx` to `c86221d758bece06b216b1f4fb23dd8e4a6c8ec0`.
- The pinned `WildCatchLevelDecisionTest` covers `FVX-WILD-007` Set Minimum Catch Rate, `FVX-WILD-010` Catch Em All Mode and `FVX-WILD-012` Balance Low Level Encounters + Level Modifier with synthetic Non-ROM data.
- Statuswirkung: `FVX-WILD-007`, `FVX-WILD-010` and `FVX-WILD-012` are now `tested-non-rom`, not P1-supported; no ROM-Smoke, Writer-/Reload-ROM evidence, output-ROM or Randomizer run was performed.

# Current update

- Diagnose 175B records merged UPR-FVX PR #45 for the Non-ROM `Gen3MoveDataWriterTest` and `MoveUpdateDecisionTest` harnesses and pins `02_external/upr-fvx` to `1be6f51779906af017f6177f264e41f8c7902d8e`. `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` and `FVX-MOVE-006` are now `tested-non-rom`; `FVX-MOVE-005` Move Names/Text remains out of scope and no P1-promotion is made.

# Current update

- Diagnose 174B records merged UPR-FVX PR #44 for the Non-ROM `EvolutionMakeEasierDecisionTest` harness and pins `02_external/upr-fvx` to `85b282112322f8991dd11b14cc98d6dd68fd3fd4`. `FVX-TRAIT-025A` is now `tested-non-rom` for Condense-/Level-/Decision logic; `FVX-TRAIT-025B` remains a separate Gen3 Happiness-byte patch / writer-like scope, and `FVX-TRAIT-026` remains helper-only with no standalone support claim.

# Current update

- Diagnose 173 plans `FVX-TRAIT-025` Make Evolutions Easier as a split scope. Result: `make-easier-plan-ready`; 025A is ROM-free Condense-/Level-/Decision logic, while 025B is a separate Gen3 Happiness-byte patch / writer-like scope. `FVX-TRAIT-026` remains helper-only for `024/025`, with no standalone support claim. No testcode, ROM-Smoke, Randomizer run, build, code change or submodule change was performed.

# Current update

- Diagnose 172B records merged UPR-FVX PR #43 for the Non-ROM `EvolutionMethodDecisionTest` harness and pins `02_external/upr-fvx` to `3b33412e80d1cb2d97725ad7a7dd01529aa56919`. `FVX-TRAIT-024` and `FVX-TRAIT-027` are now `tested-non-rom`; this is not a P1-supported promotion because no Writer-/Reload-Evidenz, ROM-Smoke, Gen3 writer, output-ROM or Randomizer run was performed. `025` stays split and `026` remains a helper flag.

# Current update

- Diagnose 171 reviews Evolution method decision paths for `FVX-TRAIT-024` and `FVX-TRAIT-027`. Result: `decision-review-ready`; Change Impossible Evolutions and Remove Time-Based Evolutions have concrete ROM-free mapping assertions for a later small `:romio:test`, while `025` stays split and `026` remains a helper flag. No testcode, ROM-Smoke, Randomizer run, build, code change or submodule change was performed.

# Current update

- Diagnose 170 plans the separate Evolution methods/improvement slices `FVX-TRAIT-024` through `FVX-TRAIT-027`. Result: `methods-plan-ready`; `024/027` need method-mapping decision evidence before any writer/reload scope, `025` splits into ROM-free condense logic and Gen3 happiness-byte patch risk, and `026` remains a helper flag for `024/025`. No testcode, ROM-Smoke, Randomizer run, build, code change or submodule change was performed.

# Current update

- Diagnose 169B records merged UPR-FVX PR #42 for the Non-ROM `EvolutionFilterOptionsTest` harness and pins `02_external/upr-fvx` to `587e857088cac4fba41c6559d3a6f6e2a7aad71f`. `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023` are now `tested-non-rom`; this is not a P1-supported promotion because no ROM-Smoke, Gen3 writer, reload or `FVX-TRAIT-024..027` scope was performed.

# Current update

- Diagnose 168 plans a Non-ROM harness for Evolution filter slices `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023`. Result: `harness-plan-ready`; all five slices are ROM-free testable with synthetic `Species`/`Evolution` data and a small `RomHandler` proxy/fake, with no expected production-code seam. No testcode, ROM-Smoke, Randomizer run, build or code change was performed.

# Current update

- Diagnose 167 consolidates Evolution suboptions `FVX-TRAIT-016` through `FVX-TRAIT-027`. Result: `evolution-scope-consolidated`; `016` remains P1-supported, `018/019` are `diagnosis-ready`, `017/020-023` stay plan-only, and `024-027` stay separate not-started Evolution-improvement/method slices. No ROM-Smoke, Randomizer run, build or code change was performed.

# Current update

- Diagnose 166 reclassifies `FVX-TRAIT-019` Evolution Same Typing read-only. Result: `diagnosis-ready`; 070's NullPointerException blocker is superseded by 079/080 same-typing null-primary-type guard evidence, so no immediate UPR-FVX fix block is recommended. No ROM-Smoke, Randomizer run, build or code change was performed.

# Current update

- Diagnose 165 reclassifies `FVX-TRAIT-018` Evolution Similar Strength read-only. Result: `diagnosis-ready`; 070's mismatch blocker is superseded by 081/082 normalized reload evidence, so no immediate UPR-FVX fix block is recommended. No ROM-Smoke, Randomizer run, build or code change was performed.

# Current update

- Diagnose 164 closes In-Game Trades for the tested CFRU/DPE Gen9-BPRE scope as `guarded/preserve-only, not supported`. Guards and non-ROM tests are documented, but no valid active rows are confirmed; Species-Write-Smoke, ROM-Smoke, valid-active-row promotion, and text/Nickname/OT/IV/Held-Item scopes remain blocked.

# Current update

- Diagnose 163B records merged UPR-FVX PR #41 for the ROM-free Gen3 In-Game Trades writer-preserve test and pins `02_external/upr-fvx` to `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`. The test covers unsafe/null-request writer preserve decisions with synthetic `InGameTrade` rows and bytes; Species-Write-Smoke, ROM-Smoke, valid-active-row promotion, and text/Nickname/OT/IV/Held-Item scopes remain blocked.

# Current update

- Diagnose 162 plans a small ROM-free Gen3 In-Game Trades writer-preserve test. Result: `writer-test-plan-ready`; the recommended later scope is a `:romio:test` unit test with a narrow Gen3 row-write decision seam proving unsafe/null-request rows skip before byte writes. Species-Write-Smoke, ROM-Smoke, Gen3 writer implementation, and text/Nickname/OT/IV/Held-Item scopes remain blocked.

# Current update

- Diagnose 161B records merged UPR-FVX PR #40 for the non-ROM `TradeRandomizerTest` In-Game Trades guard harness and pins `02_external/upr-fvx` to `1eaee2873cd69682335223f817b124bf36d004f2`. The harness covers null-request and placeholder/unsafe Species skips, all-skipped no `setInGameTrades(...)`, `isChangesMade=false`, and skip counters; Species-Write-Smoke, ROM-Smoke and Gen3 writer testing remain blocked.

# Current update

- Diagnose 160 plans a small non-ROM In-Game Trades guard harness. Result: `harness-plan-ready`; the recommended first scope is a `TradeRandomizer` unit test with synthetic `InGameTrade` rows and a fake/test `RomHandler`, while Species-Write-Smoke and all text/Nickname/OT/IV/Held-Item scopes remain blocked.

# Current update

- Diagnose 159 reviews the merged UPR-FVX In-Game Trades guard code read-only. Result: `review-pass-with-risks`; unsafe rows skip before mutation and preserve before Gen3 byte writes, but Species-Write-Smoke stays blocked and a later non-ROM harness is recommended.

# Current update

- Diagnose 158B records merged UPR-FVX PR #39 for the In-Game Trades null/invalid Species guard and pins `02_external/upr-fvx` to `a86315e8d82e0854e0fd59549f50e2c49f523c40`. In-Game Trades remain `blocked-pending-evidence`; Species-Write-Smoke, text, Nickname/OT, IV and Trade Held Item scopes stay blocked.

# Current update

- Diagnose 157 documents a read-only defensive null-request guard plan for In-Game Trades. Result: still `blocked-pending-evidence`; a later fix would skip/preserve null-request or invalid/placeholder Species rows before mutation/write and must not include Species-Write-Smoke, text, IV or Trade Held Item writes.

# Current update

- Diagnose 156 defines the In-Game Trades Preserve/Skip policy. Result: `blocked-pending-evidence`; all modeled trade rows remain preserve-only, no Species-Write-Smoke or Nickname/OT randomization is allowed, and `unsupported-dummy` remains plausible but unproven.

# Current update

- Diagnose 155 checks In-Game Trades active-row candidates from UPR-FVX `TradeTableOffset`, `TradeTableSize`, `TradesUnused` and the documented 60-byte Gen3 row model. Result: blocked; no valid active row is confirmed and `unsupported-dummy` is not proven strongly enough for a final unsupported decision.

# Current update

- Diagnose 154 documents the In-Game Trades locator/table-model from source and prior diagnostics. Result: blocked; valid active trade rows are still not read-only confirmed, so Species-Write-Smoke remains disallowed.

# Current update

- Diagnose 153 adds the In-Game Trades table-model blocker plan. It explains why Diagnose 152 does not permit a species-only smoke yet and requires a read-only locator/table-model diagnostic before any In-Game Trade write work.

# Current update

- Diagnose 152 records a read-only In-Game Trades candidate diagnostic. Result: blocked/preflight because the current Gen3 BPRE trade-table model does not classify valid active trade Species fields for the CFRU/DPE Gen9-BPRE candidate; no write/reload smoke is recommended yet.

# Current update

- Diagnose 151 plans In-Game Trades as the next open CFRU/DPE Gen9-BPRE Randomizer scope. The plan splits trade species, held items, IVs and fixed-length nickname/OT fields into separate follow-up diagnostics and keeps Standard Wild, Special Wild, Starters, Statics, Trainer Pokemon, Held Items and Text/Menu work out of scope.

# Latest - Diagnose 150

- `150_special_wild_triggerability.md`: Read-only Special Wild triggerability analysis; marks Day/Night as dormant in the tracked state, Swarms/Roamers/Wild Double/gWildDataSwitch as runtime-state driven, DexNav as partial/future, and Raids as future parser/write scope.

# Latest - Diagnose 149

- `149_coverage_reconciliation.md`: Coverage/roadmap reconciliation after Held Items closure and Wild Encounters plan; identifies special Wild Encounter systems, not Standard Wild retest, as the next genuinely open major scope.

# Latest - Diagnose 148

- `148_wild_encounters_scope_diagnostics_plan.md`: Wild Encounters scope diagnostics plan; starts a new Wild Pokemon/Encounter scope after Held Items closure and requires read-only candidate diagnostics before any write/reload smoke.

# Latest - Diagnose 147

- `147_starter_held_items_ban_bad_reload_smoke.md`: Starter Held Items + Ban Bad Write/Reload-Smoke; PASS with non-bad pool writes, reload stability and Wild/Trainer/Field/Pickup/Shop isolation. Tested Held Items scope is closed.

# Latest - Diagnose 146

- `146_starter_held_items_reload_smoke.md`: Starter Held Items Write/Reload-Smoke without Ban Bad; PASS with one shared Gen3/FRLG Starter Held Item slot, reload stability and Wild/Trainer/Field/Pickup/Shop isolation.

# Latest - Diagnose 145

- `145_trainer_held_items_regular_filtered_reload_smoke.md`: Regular Trainer Held Items filtered Write/Reload-Smoke; PASS with Consumable Only, Sensible Items and Highest Level Only in the narrow Regular-Trainer scope.

# Latest - Diagnose 144

- `144_trainer_held_items_filters_scope_plan.md`: Trainer Held Items filter scope plan; separates Consumable Only, Sensible Items and Highest Level Only after Boss/Important/Regular no-filter smokes passed.

# Latest - Diagnose 143

- `143_trainer_held_items_regular_reload_smoke.md`: Regular Trainer Held Items Write/Reload-Smoke; PASS with reload-stable `TrainerPokemon.heldItem`, class preserve-policy and Wild/Starter/Field/Pickup/Shop isolation.

# Latest - Diagnose 142

- `142_trainer_held_items_important_reload_smoke.md`: Important Trainer Held Items Write/Reload-Smoke; PASS with reload-stable `TrainerPokemon.heldItem`, class preserve-policy and Wild/Starter/Field/Pickup/Shop isolation.

# Latest - Diagnose 141

- `141_trainer_held_items_boss_reload_smoke.md`: Boss Trainer Held Items Write/Reload-Smoke; PASS with reload-stable `TrainerPokemon.heldItem`, class preserve-policy and Wild/Starter/Field/Pickup/Shop isolation.

# Latest - Diagnose 140

- `140_wild_held_items_ban_bad_reload_smoke.md`: Wild/Encounter Held Items + Ban Bad Write/Reload-Smoke; PASS with reload-stable Species/BaseStats held items, non-bad pool enforcement and Trainer/Starter/Field/Pickup/Shop isolation.

# Latest - Diagnose 139

- `139_wild_held_items_reload_smoke.md`: Wild/Encounter Held Items Write/Reload-Smoke without Ban Bad; PASS with reload-stable Species/BaseStats held items and Trainer/Starter/Field/Pickup/Shop isolation.

# Latest - Diagnose 138

- `138_held_items_scope_diagnostics.md`: PASS for read-only CFRU/DPE Held Items candidate diagnostics; Wild/Encounter, Trainer and Starter paths are readable, with no Field/Pickup/Shop scope changes.

# Latest - Diagnose 137

- `137_held_items_scope_diagnostics_plan.md`: Read-only plan for CFRU/DPE Gen9-BPRE Held Items scope diagnostics after the tested Shop Items scope closed.

# Latest - Diagnose 136

- `136_shop_balance_prices_cheap_rare_candies_reload_smoke.md`: PASS for Shop-only FVX-ITEM-009 Balance Shop Prices + Cheap Rare Candies combination; Shop Items scope closed for tested CFRU/DPE Gen9-BPRE GUI-compatible paths.

# 2026-05-15 - Diagnose 135 Shop Cheap Rare Candies Reload Smoke

- Added `08_tests/randomizer/135_shop_cheap_rare_candies_reload_smoke.md`.
- Result: PASS for FVX-ITEM-009 Cheap Rare Candies with `ShopItemsMod.UNCHANGED`.
- Shop item total grew from 157 to 180 and reload stayed stable; `rareCandyWrites=23`, `skippedShopRareCandyWrites=20`, `shopItemReloadMismatches=0`.
- Rare Candy price write was reload-stable; Balance Prices + Cheap Rare Candies combination remains out of scope.

# 2026-05-15 - Diagnose 134 Shop Balance Prices Reload Smoke

- Added `08_tests/randomizer/134_shop_balance_prices_reload_smoke.md`.
- Result: PASS for FVX-ITEM-009 Balance Shop Prices with `ShopItemsMod.UNCHANGED`.
- `balancedPriceWrites=132`, `priceTableTouched=true`, `priceReloadMismatches=0`; Shop lists, skipped Shops, Field Items, Pickup, and Held Items stayed stable.
- Cheap Rare Candies remain out of scope and unpromoted.

# 2026-05-15 - Diagnose 133 Shop Prices / Cheap Rare Candies Scope Plan

- Neues Protokoll: `133_shop_prices_cheap_rare_candies_scope_plan.md`.
- `FVX-ITEM-009` ist als separater Shop-only Preis-/Rare-Candy-Subscope geplant.
- Balance Shop Prices schreibt unabhaengig von `ShopItemsMod` ueber `getShopPrices()`/`setShopPrices()`; erster Smoke soll preis-only mit `ShopItemsMod.UNCHANGED` laufen.
- Cheap Rare Candies erweitert Shoplisten um Rare Candies und setzt den Rare-Candy-Preis; dieser Pfad bleibt ein zweiter separater Smoke.

# 2026-05-15 - Diagnose 132 Shop Guarantee X Items Reload Smoke

- Added `08_tests/randomizer/132_shop_guarantee_x_items_reload_smoke.md`.
- Result: PASS for FVX-ITEM-008 Guarantee X Items with Shop Random only.
- All 7 expected X Items were present after write and reload; Shop counts, lengths, terminators, skipped Shops, prices, Field Items, Pickup, and Held Items stayed stable.
- Evolution+X combination, FVX-ITEM-007 Ban combinations, and FVX-ITEM-009 prices/Cheap Rare Candies remain out of scope.

# 2026-05-15 - Diagnose 131 Shop Guarantee Evolution Items Reload Smoke

- Added `08_tests/randomizer/131_shop_guarantee_evolution_items_reload_smoke.md`.
- Result: PASS for FVX-ITEM-008 Guarantee Evolution Items with Shop Random only.
- All 6 expected Evolution guarantee items were present after write and reload; Shop counts, lengths, terminators, skipped Shops, prices, Field Items, Pickup, and Held Items stayed stable.
- Guarantee X Items, combined guarantees, FVX-ITEM-007 Ban combinations, and FVX-ITEM-009 prices/Cheap Rare Candies remain out of scope.

# 2026-05-15 - Diagnose 130 Shop Guarantee Items Scope Plan

- Neues Protokoll: `130_shop_guarantee_items_scope_plan.md`.
- Ergebnis: `FVX-ITEM-008 Guarantee Evolution/X Items` ist als separater Shop-only Subscope nach `FVX-ITEM-007` geplant.
- Guarantee-Flags wirken nur im `ShopItemsMod.RANDOM`-Pfad; Shuffle und Unchanged liefern keinen Guarantee-Nachweis.
- Empfohlen: zuerst Guarantee Evolution Items Smoke, danach Guarantee X Items Smoke; Preise, Cheap Rare Candies, Field Items, Pickup und Held Items bleiben aus Scope.

# 2026-05-15 - Diagnose 129 Shop Items Random + Ban OP Reload Smoke

- Neues Protokoll: `129_shop_items_random_ban_op_reload_smoke.md`.
- Ergebnis: `ShopItemsMod.RANDOM + banOPShopItems=true` besteht den Shop-only Write/Reload-Smoke.
- `opShopSetClassifiable=true`, `opShopItemBannedWrites=0`; Counts, Terminatoren, Laengen, Skip-Shops, Preise und Fremdscopes bleiben stabil.
- `FVX-ITEM-007` ist nun fuer Ban Bad, Ban Regular und Ban OP jeweils einzeln GUI-kompatibel; Ban-Kombinationen bleiben separat ausstehend.

# 2026-05-15 - Diagnose 128 Shop Items Random + Ban Regular Reload Smoke

- Neues Protokoll: `128_shop_items_random_ban_regular_reload_smoke.md`.
- Ergebnis: `ShopItemsMod.RANDOM + banRegularShopItems=true` besteht den Shop-only Write/Reload-Smoke.
- `regularShopSetClassifiable=true`, `regularShopItemBannedWrites=0`; Counts, Terminatoren, Laengen, Skip-Shops, Preise und Fremdscopes bleiben stabil.
- `FVX-ITEM-007` ist nun fuer Ban Bad und Ban Regular einzeln GUI-kompatibel; OP-Ban bleibt separat ausstehend.

# 2026-05-15 - Diagnose 127 Shop Items Random + Ban Bad Reload Smoke

- Neues Protokoll: `127_shop_items_random_ban_bad_reload_smoke.md`.
- Ergebnis: `ShopItemsMod.RANDOM + banBadRandomShopItems=true` besteht den Shop-only Write/Reload-Smoke.
- `badShopItemWrites=0`; Counts, Terminatoren, Laengen, Skip-Shops, Preise und Fremdscopes bleiben stabil.
- `FVX-ITEM-007` ist nur fuer den Ban-Bad-Subscope GUI-kompatibel; Regular- und OP-Bans bleiben separat ausstehend.

# Randomizer Testprotokolle

- 126 - `126_shop_item_bans_scope_plan.md`: Read-only plan for `FVX-ITEM-007 Shop Item Bans`. Confirms Shop bans only affect `ItemRandomizer.randomizeShopItems()` under `ShopItemsMod.RANDOM`, splits `banBadRandomShopItems`, `banRegularShopItems` and `banOPShopItems`, keeps Guarantee Evolution/X Items, prices, Cheap Rare Candies, Field Items, Pickup and Held Items out of scope, and recommends Shop Random + Ban Bad as the first ban smoke.

- 125 - `125_shop_items_random_reload_smoke.md`: Shop-only `FVX-ITEM-006 Shop Items Random` Write/Reload-Smoke without Shop Bans, Guarantee, prices or Cheap Rare Candies. `candidateFilesChecked=3`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`; Shop counts, lengths, terminators, skipped shops, special policy, prices and Field/Pickup/Held scopes stayed stable, `shopItemReloadMismatches=0`, `allowedShopItemPoolSize=536`, `nonBadShopItemPoolSize=485`. `FVX-ITEM-006` is GUI-compatible in the tested Shop-only Random scope; `FVX-ITEM-007..009` remain separate.

- 124 - `124_shop_items_shuffle_reload_smoke.md`: Shop-only `FVX-ITEM-005 Shop Items Shuffle` Write/Reload-Smoke. `candidateFilesChecked=3`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`; Shop counts, lengths, terminators, skipped shops, special policy, prices and Field/Pickup/Held scopes stayed stable, `shopItemReloadMismatches=0`. `FVX-ITEM-005` is GUI-compatible in the tested Shop-only Shuffle scope; `FVX-ITEM-006..009` remain separate.

- 123 - `123_shop_items_scope_diagnostics_candidate.md`: Sanitized read-only Shop-only candidate diagnostics. `candidateFilesChecked=3`, `candidateLoaded=true`, `shopScanSuccessful=true`, `shopCount=23`, `mainGameShopCount=3`, `skippedShopCount=20`, `specialShopCount=3`, `shopItemsTotal=157`, `terminatorModelStable=true`, `shopLengthMismatch=0`, invalid/unloaded/fallback/placeholder Shop items `0`; recommends a Shop Shuffle smoke next.


- 122 - `122_shop_items_scope_diagnostics.md`: Blocked/Preflight fuer die read-only CFRU/DPE Shop-Items-Kandidatendiagnose. Keine explizit freigegebene lokale Kandidatenquelle im Block, daher `candidateFilesChecked=0`, `candidateLoaded=false`, `shopScanSuccessful=false`; Codepfadmodell mit `ShopPointerOffsets`, `MainGameShops`, `SkipShops`, `Shop` und `DataRewriter<Shop>` bleibt dokumentiert.


- 121 - `121_shop_items_scope_diagnostics_plan.md`: Read-only Plan fuer den CFRU/DPE Shop-Items-Scope. Bestaetigt `FVX-ITEM-005..009` als separates Shop-Paket nach Field Items und Pickup, dokumentiert `ShopItemsMod`, `ItemRandomizer`, `Gen3RomHandler.getShops()`/`setShops(...)`, `DataRewriter`, terminierte Shoplisten, MainGame/Skip/Special Shops, Preislogik, Risiken, Preserve-/Skip-Policy, spaetere Metriken und empfohlene Diagnose-Reihenfolge.


## Latest
- `118_pickup_items_reload_locator_fix.md` dokumentiert den engen UPR-FVX-Fix fuer den Pickup-Reload-Locator und den erfolgreichen Pickup-only Random-Smoke mit `banBadRandomPickupItems=false`.
- Ergebnis: Save/Log/Output/Reload true, `pickupItemsTotalReload=16`, `pickupItemReloadMismatches=0`; Pickup Ban Bad bleibt separat.
- `117_pickup_items_reload_locator_blocker_plan.md` dokumentiert read-only den Pickup-Reload-Locator-Blocker nach `PickupItemsMod.RANDOM`.
- Ergebnis: Der bestehende `PickupTableStartLocator` ist inhaltsbasiert und wird durch den Random-Write veraendert; empfohlen ist ein enger reloadstabiler Locator-Fix vor Pickup Ban Bad.

- `112_field_items_random_ban_bad_reload_smoke.md` dokumentiert den Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke mit `banBadRandomFieldItems=true`.
- Ergebnis: Save/Log/Output/Reload erfolgreich, Field-Item Reload-Mismatches `0`, Required Field TMs erhalten, `badFieldItemWrites=0`, keine Shop-/Pickup-/Held-Item-Scope-Aenderung.
- Einschraenkung: Der Lauf misst `badFieldItemPoolCandidates=47` statt der in Diagnose 111 erwarteten 75er-Baseline; `FVX-ITEM-004` ist damit fuer `FieldItemsMod.RANDOM` getestet, aber Random Even + Ban Bad bleibt separat.

Dieses Verzeichnis enthaelt die dauerhaften Markdown-Protokolle fuer UPR-FVX/CFRU-DPE-Randomizer-Analysen und Smokes. Lokale ROM-, Build-, Log- und Tool-Artefakte bleiben unter `05_builds/**` oder `03_tools/releases/**` und werden nicht committed.

## Nummerierung und Latest

Neue Randomizer-Smoke-Protokolle sollen ab jetzt eine laufende Nummer bekommen:

```text
001_<kurzer-zweck>.md
002_<kurzer-zweck>.md
003_<kurzer-zweck>.md
```

Bestehende unnummerierte Protokolle bleiben vorerst unveraendert, damit alte Verweise stabil bleiben. Fuer sie gilt die Nummer in der Tabelle unten als Ordnungsindex.

Lokale Smoke-Artefakte sollen passend dazu unter nummerierten Ordnern abgelegt werden:

```text
05_builds/randomizer-smoke/001_<kurzer-zweck>/
05_builds/randomizer-smoke/002_<kurzer-zweck>/
05_builds/randomizer-smoke/003_<kurzer-zweck>/
```

Der neueste bestaetigte Stand wird in Markdown ueber die Spalte `Latest` markiert. Ein `latest`-Symlink ist nicht erforderlich.

## Wichtige Protokolle

| Nr. | Datei | Zweck | Status | Lokaler Artefaktordner | Latest |
|---:|---|---|---|---|---|
| 001 | `upr-fvx-source-integration.md` | UPR-FVX-Source-Integration und Sicherheitsgrenzen | dokumentiert | keiner | nein |
| 002 | `upr-fvx-source-build-smoke-test.md` | lokaler UPR-FVX-Source-Build-Smoke | bestaetigt | keiner | nein |
| 003 | `upr-fvx-cfru-dpe-load-smoke-test.md` | CFRU/DPE-ROM in UPR-FVX laden | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 004 | `upr-fvx-cfru-dpe-randomize-smoke-test.md` | minimal randomisieren und speichern | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 005 | `route-1-fallback-wild-randomizer-check.md` | Route-1-Fallback-Wilddaten fuer FVX pruefen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 006 | `upr-fvx-cfru-dpe-species-pool-analysis.md` | Species-Pool read-only analysieren | dokumentiert | keiner | nein |
| 007 | `upr-fvx-cfru-dpe-species-diagnostics-run.md` | CFRU/DPE-Species-Diagnose mit `PokemonCount=823` | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 008 | `upr-fvx-gen4plus-wild-pool-diagnostics.md` | Gen4+-Wild-Pool-Engpass diagnostizieren | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 009 | `upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics.md` | Wild-Write ueber interne Species-Identitaet diagnostizieren | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 010 | `upr-fvx-cfru-dpe-p0-post-merge-smoke.md` | PR #3/#4/#5 Post-Merge-Smoke | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 011 | `upr-fvx-cfru-dpe-p1-starter-write-diagnostics.md` | Starter-Schreibpfad diagnostizieren | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 012 | `upr-fvx-cfru-dpe-starter-internal-species-write-diagnostics.md` | Starter-Fix diagnostisch bestaetigen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 013 | `upr-fvx-cfru-dpe-p1-static-gift-write-diagnostics.md` | Static/Gift-Read-/Write-Scope vor Gen9-Coverage | teilweise, wieder aufnehmen | `05_builds/randomizer-smoke/` historisch | nein |
| 014 | `upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics.md` | `PokemonCount`-Kappung bei DPE/CFRU einordnen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 015 | `upr-fvx-cfru-dpe-gen9-species-count-diagnostics.md` | Gen9-SpeciesCount-Unblocker diagnostizieren | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 016 | `upr-fvx-cfru-dpe-defensive-palette-loading-diagnostics.md` | defensives Palette-Load/-Save-Verhalten pruefen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 017 | `upr-fvx-cfru-dpe-lazy-trainer-movesets-diagnostics.md` | Lazy-Trainer-Movesets-Unblocker pruefen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 018 | `upr-fvx-cfru-dpe-skip-unchanged-palette-save-diagnostics.md` | unveraenderte CFRU/DPE-Paletten beim Save ueberspringen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 019 | `upr-fvx-cfru-dpe-gen9-wild-post-merge-smoke.md` | Gen9 Standard-/Fallback-Wild post-merge smoke | bestaetigt: `saveSuccessful=true`, Gen7/8/9 im Wild-Log | `05_builds/randomizer-smoke/` historisch, lokal bereinigt | nein |
| 020 | `upr-fvx-cfru-dpe-wild-banned-special-species-diagnostics.md` | CFRU/DPE-Special-Species-Wild-Ban diagnostisch bestaetigen | bestaetigt: `Bad Egg=0`, `<unknown>=0`, Gen7/8/9 im Wild-Log | `05_builds/randomizer-smoke/` historisch, lokal bereinigt | nein |
| 021 | `021_p1_static_gift_species_only.md` | Static/Gift Species-only Diagnose auf Gen9-Wild-sauberem Stand | blockiert: Gen1-Gen9-Pool vorhanden, Pick erreicht Gen7/8/9, Save bricht an Null-Static-Scope ab | `05_builds/randomizer-smoke/021_p1_static_gift_species_only/` lokal/ignored | nein |
| 022 | `022_static_gift_scope_write_diagnostics.md` | Static/Gift-Scope und interner Species-Write fuer CFRU/DPE | bestaetigt: `saveSuccessful=true`, nichtleerer Static/Gift-Log, Gen7/8/9-Picks, `writeReloadMismatches=0` | `05_builds/randomizer-smoke/022_static_gift_scope_write/` lokal/ignored | nein |
| 023 | `023_p1_trainer_species_only.md` | Trainer-Species-only Diagnose mit Gen1-Gen9-Pool | blockiert: Trainer-Pool Gen1-Gen9 vorhanden, aber `randomizeTrainerPokes()` haengt in `getRandomAbilitySlot()` auf Zero-Ability-Sonder-Species | `05_builds/randomizer-smoke/023_p1_trainer_species_only/` lokal/ignored | nein |
| 024 | `024_trainer_scope_write_diagnostics.md` | Trainer-Scope und interner Species-Write fuer CFRU/DPE | bestaetigt: `saveSuccessful=true`, nichtleerer Trainer-Log, Gen7/8/9-Picks, `writeReloadMismatches=0` | `05_builds/randomizer-smoke/024_trainer_scope_write/` lokal/ignored | nein |
| 025 | `025_p1_evolutions_species_only.md` | Evolution-Species-only Diagnose mit Gen1-Gen9-Pool | blockiert: Evolution-Pool Gen1-Gen9 vorhanden, Save erzeugt Output-ROM, aber Log-Fehler und `writeReloadMismatches=146` | `05_builds/randomizer-smoke/025_p1_evolutions_species_only/` lokal/ignored | nein |
| 026 | `026_evolutions_scope_write_diagnostics.md` | Evolution-Scope und interner Species-Write fuer CFRU/DPE | bestaetigt: `saveSuccessful=true`, `logSuccessful=true`, Gen7/8/9-Picks, `writeReloadMismatches=0` | `05_builds/randomizer-smoke/026_evolutions_scope_write/` lokal/ignored | nein |
| 027 | `027_p1_trainer_held_items_only.md` | Trainer Held Items-only Diagnose | blockiert: Trainer-Held-Item-Pool vorhanden, aber `randomizeTrainerHeldItems()` scheitert in `getMovesLearnt()` bei `0x25e49c`; kein Save/Log/Reload | `05_builds/randomizer-smoke/027_p1_trainer_held_items_only/` lokal/ignored | nein |
| 028 | `028_trainer_held_items_lazy_movesets_diagnostics.md` | Trainer Held Items lazy Moveset-/Learnset-Load | bestaetigt: `saveSuccessful=true`, nichtleerer Trainer-Log, `after/reload.heldItemEntries=481`, `writeReloadMismatches=0` | `05_builds/randomizer-smoke/028_trainer_held_items_lazy_movesets/` lokal/ignored | nein |
| 029 | `029_p1_trainer_movesets_only.md` | Trainer Movesets-only Diagnose | blockiert: Trainer-Load stabil, aber `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel()` scheitert in `getMovesLearnt()` bei `0x25e49c`; kein Save/Log/Reload | `05_builds/randomizer-smoke/029_p1_trainer_movesets_only/` lokal/ignored | nein |
| 030 | `030_p1_learnsets_model.md` | CFRU/DPE-Level-Up-Learnset-Modell fuer `gLevelUpLearnsets` | dokumentiert: FVX liest CFRU/DPE-Learnsets mit alten Gen3-/Jambo-Annahmen; `0x25e49c` ist `PokemonMovesets + SPECIES_ZYGARDE*4`; minimaler Folgepfad ist ein gegateter CFRU/DPE-Learnset-Reader | keiner | nein |
| 031 | `031_trainer_movesets_learnsets_fix_diagnostics.md` | Trainer Movesets Learnsets-Fix Diagnose | bestaetigt: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleerer Trainer-Log, `after/reload.movesetEntries=417`, `writeReloadMismatches=0` | `05_builds/randomizer-smoke/031_trainer_movesets_learnsets_fix/` lokal/ignored | nein |
| 032 | `032_p1_trainer_movesets_combinations.md` | Trainer Movesets Kombinationsdiagnosen | bestaetigt: Movesets-only, Movesets+Species, Movesets+Held Items normal und Movesets+sensible Held Items jeweils mit `saveSuccessful=true`, `logSuccessful=true`, `writeReloadMoveMismatches=0` | `05_builds/randomizer-smoke/032_p1_trainer_movesets_combinations/` lokal/ignored | nein |
| 033 | `033_p1_move_data_model.md` | CFRU/DPE Gen8/9-Move-Datenmodell | dokumentiert: FVX laedt aktuell `moves.total=559`, CFRU/DPE definiert `MOVES_COUNT=992`; TM/HM-, Tutor- und Egg-Move-Pfade brauchen getrennte gegatete Modelle | keiner | nein |
| 034 | `034_move_data_reader_fix_diagnostics.md` | CFRU/DPE Move-Data-Reader-Fix Diagnose | bestaetigt: `moves.total=992`, hoechster Move `PsychicNoise`, Trainer-Moveset-Kombinationen mit `saveSuccessful=true`, `logSuccessful=true`, `writeReloadMoveMismatches=0` | `05_builds/randomizer-smoke/034_move_data_reader_fix_diagnostics/` lokal/ignored | nein |
| 035 | `035_p1_tm_hm_only.md` | TM/HM-only Diagnose | blockiert: FVX erkennt nur `50+8`, TM-Move-Randomization scheitert an altem Move-Ban-Array-Limit `827`, Compatibility-only scheitert an Null-Type-Species; kein Save/Output/Reload | `05_builds/randomizer-smoke/035_p1_tm_hm_only/` lokal/ignored | nein |
| 036 | `036_tm_hm_scope_and_safety_fix_diagnostics.md` | TM/HM Scope-and-Safety-Fix Diagnose | bestaetigt im klassischen `50+8`-Scope: TM moves + Compatibility, Compatibility-only und TM moves-only jeweils mit `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleerem Log und `writeReloadMismatches=0` | `05_builds/randomizer-smoke/036_tm_hm_scope_and_safety_fix/` lokal/ignored | nein |
| 037 | `037_p1_tm_hm_128_slot_model.md` | CFRU/DPE TM/HM-128-Slot-Modell | dokumentiert: aktives `gTMHMMoves` ist `u16[128]` ueber Pointer `0x8125A8C`, TMs `1..120`, HMs `121..128`, Compatibility `16` Bytes pro Species ueber `0x8043C68`; kein Fix | keiner | nein |
| 038 | `038_tm_hm_128_slot_fix_diagnostics.md` | CFRU/DPE TM/HM-128-Slot-Fix Diagnose | bestaetigt: `tmCount=120`, `hmCount=8`, 128 Slots, 129 Compatibility-Flags, HM-Slots unveraendert, alle drei TM/HM-Laeufe mit `saveSuccessful=true`, `logSuccessful=true` und `writeReloadMismatches=0` | `05_builds/randomizer-smoke/038_tm_hm_128_slot_fix/` lokal/ignored | nein |
| 039 | `039_p1_tutor_model.md` | CFRU/DPE Tutor-/Special-Tutor-Modell | dokumentiert: normale Tutor-Tabelle `gMoveTutorMoves` mit `152` `u16`-Eintraegen ueber Pointer-Location `0x8120BE4`, `gTutorLearnsets` ueber `0x8120C30`, Special Tutors separat; kein Fix | keiner | nein |
| 040 | `040_tutor_scope_and_compatibility_fix_diagnostics.md` | CFRU/DPE Tutor-Scope-and-Compatibility-Fix Diagnose | bestaetigt: `tutorMoveCount=152`, `gMoveTutorMoves` ueber `0x8120BE4`, `gTutorLearnsets` mit 19-Byte-Stride ueber `0x8120C30`, alle drei Tutor-Laeufe mit Save/Log/Reload und `writeReloadMismatches=0` | `05_builds/randomizer-smoke/040_tutor_scope_and_compatibility_fix/` lokal/ignored | nein |
| 041 | `041_p1_egg_move_model.md` | CFRU/DPE Egg-Move-Modell | dokumentiert: Streamformat `u16`, Species-Marker `species + 20000`, Terminator `0xFFFF`; DPE-Stream enthaelt Gen8/9-Species und Move-IDs bis `967`, aber FVX nutzt noch falschen Tabellenort/Pokedex-Mapping und hat hohe-Move-ID-Risiken | keiner | nein |
| 042 | `042_egg_moves_scope_and_write_fix_diagnostics.md` | CFRU/DPE Egg-Move-Scope-and-Write-Fix Diagnose | bestaetigt: `gEggMoves` ueber `0x45C50`, interne SpeciesSet-Keys, Gen8/9-Species und Gen9-Moves bleiben erhalten, `writeReloadEggMoveMismatches=0` | `05_builds/randomizer-smoke/042_egg_moves_scope_and_write_fix/` lokal/ignored | nein |
| 043 | `043_p1_learnset_write_model.md` | CFRU/DPE Learnset-Write-Modell | dokumentiert: `gLevelUpLearnsets` ueber `0x03EA7C`, interne Species-ID-Pointertabelle, `u16 move + u8 level`, Sentinel `{0, 0xFF}`; Folgefix nur bounded in-place ohne Repointing | keiner | nein |
| 044 | `044_learnset_write_bounded_fix_diagnostics.md` | CFRU/DPE Learnset-Write bounded in-place Fix Diagnose | teilweise bestaetigt: eng gegateter Writer speichert/reloadet sichere same-size Learnsets mit `writeReloadLearnsetMismatches=0`, aber die getestete ROM liefert nur `boundedWrites=1` und `skippedInvalidPointer=1412`; voller Learnset-Write braucht Repointing-Modell | `05_builds/randomizer-smoke/044_learnset_write_bounded_fix/` lokal/ignored | nein |
| 045 | `045_p1_learnset_repointing_model.md` | CFRU/DPE Learnset-Repointing-Modell | dokumentiert: Pointertable bleibt ueber `0x03EA7C -> 0x25D7B4`, Quellen zeigen `1408` Zuweisungen, `1104` eindeutige Ziele, `148` Shared-Gruppen und keinen belastbar reservierten freien Append-Bereich; Folgefix muss freie ROM-Fläche nachweisen | keiner | nein |
| 046 | `046_learnset_write_repointing_diagnostics.md` | CFRU/DPE Learnset-Write Repointing-Fix Diagnose | bestaetigt: Full `setMovesLearnt()`-Repointing schreibt neue Blobs in `0x1219A48-0x1600000`, aktualisiert `1413` Pointertable-Eintraege und reloadet mit `writeReloadLearnsetMismatches=0` | `05_builds/randomizer-smoke/046_learnset_write_repointing/` lokal/ignored | nein |
| 047 | `047_fvx_gui_options_compatibility_matrix.md` | FVX-GUI-Options-Kompatibilitaetsmatrix | dokumentiert: P1-supported, teilunterstuetzte, offene und blockierte FVX-GUI-Optionsbereiche fuer den getesteten CFRU/DPE Gen9-BPRE-Stand | keiner | nein |
| 048 | `048_p1_learnset_gui_combinations.md` | CFRU/DPE Learnset GUI-Kombinationsdiagnose | teilweise bestaetigt: erster Repointing-Write im GameRandomizer-Flow reloadet mit `writeReloadLearnsetMismatches=0`, aber Logger, Trainer-Movesets, Reorder-Damaging und Level-Up-Sanity-Kombinationen blockieren | `05_builds/randomizer-smoke/048_p1_learnset_gui_combinations/` lokal/ignored | nein |
| 049 | `049_p1_learnset_gui_flow_safety_fix_diagnostics.md` | CFRU/DPE Learnset GUI-Flow-Safety-Fix Diagnose | bestaetigt: Movesets-only, Trainer-Movesets, Reorder-Damaging, TM/HM-Sanity, Tutor-Sanity, gekoppelte Egg Moves und TM/HM+Tutor-Sanity jeweils mit Save/Log/Output/Reload und `writeReloadLearnsetMismatches=0` | `05_builds/randomizer-smoke/049_gui_flow_safety/` lokal/ignored | nein |
| 050 | `050_p1_base_stats_types_abilities_model.md` | CFRU/DPE Base Stats, Types, Abilities und Encounter Held Items Modell | dokumentiert: `gBaseStats` ueber `0x080001BC`, Entry-Size `0x1C`, interne Species-ID bis `0x59F`, Fairy/Hidden-Ability/Ability-Count/Item-Count-Risiken fuer Folgefixes | keiner | nein |
| 051 | `051_base_stats_types_scope_write_diagnostics.md` | CFRU/DPE Base Stats + Types Scope-and-Write-Fix Diagnose | bestaetigt: Base Stats-only, Types-only und Base Stats + Types mit Save/Log/Output/Reload, `writeReloadBaseStatsMismatches=0`, `typeIdMismatches=0`, Fairy `0x17` gelesen/geschrieben, Stellar preserve/skip | `05_builds/randomizer-smoke/051_base_stats_types_scope_write/` lokal/ignored | nein |
| 052 | `052_abilities_hidden_ability_scope_write_diagnostics.md` | CFRU/DPE Ability1/2 + Hidden Ability Scope-and-Write-Fix Diagnose | bestaetigt: Ability1/2-only, Hidden Ability-only, Ability1/2 + Hidden Ability und Base Stats + Types + Abilities mit Save/Log/Output/Reload, `abilitiesPerSpecies=3`, `highestAbilityIndex=254`, `writeReloadAbilityMismatches=0` und `writeReloadHiddenAbilityMismatches=0` | `05_builds/randomizer-smoke/052_abilities_hidden_ability_scope_write/` lokal/ignored | nein |
| 053 | `053_p1_item_data_and_bad_item_model.md` | CFRU/DPE Item-ID-, Itemnamen-, Bad-/Key-Item- und Encounter-Held-Item-Modell | dokumentiert: CFRU/DPE Itemgrenzen `779`/ca. `799`, klassischer FVX-`ItemCount=374`, moderne Bad-/Key-Item-Risiken und Encounter-Held-Item-Felder `item1/item2` bei `0x0C`/`0x0E`; Encounter Held Items brauchen separaten Fix | keiner, read-only Analyse | nein |
| 054 | `054_encounter_held_items_scope_write_diagnostics.md` | CFRU/DPE Encounter Held Items Scope-and-Write-Fix Diagnose | bestaetigt: Item-Scope bis `778`, moderne Bad-/Banned-Filter, Encounter Held Items-only sowie Kombinationen mit Base Stats, Abilities und Types mit Save/Log/Output/Reload und `writeReloadEncounterHeldItemMismatches=0` | `05_builds/randomizer-smoke/054_encounter_held_items_scope_write/` lokal/ignored | nein |
| 055 | `055_type_log_placeholder_hygiene.md` | CFRU/DPE Type-/Trait-Log-, Placeholder- und Unknown-Marker-Klassifikation | dokumentiert: `Bad Egg`, `<unknown>`, Unknown-Type-/Ability-/Item-Fallbacks und Null-/BST-zero-/all-zero-Ability-Species aus vorhandenen Protokollen klassifiziert; keine neuen Randomizer-Laeufe, kein Fix | keiner, read-only Analyse | nein |
| 056 | `056_p1_move_data_write_model.md` | CFRU/DPE Move-Data-Write-Modell | dokumentiert: `moves.total=992`, `991:PsychicNoise`, `BattleMove.split`-/Category-Semantik, aktuelle `saveMoves()`-Teilfeld-Write-Annahme, Preserve-Policy und Reload-Kriterien fuer spaeteren Fix; kein Fix | keiner, read-only Analyse | nein |
| 057 | `057_p1_field_items_shops_pickup_model.md` | CFRU/DPE Field-Items-/Shops-/Pickup-Item-Modell | dokumentiert: Grenze zu Encounter Held Items, Item-Scope aus 053/054, Field-/Shop-/Pickup-Risiken, allgemeine Bad-/Banned-Item-Risiken, Preserve-/Skip-Policy und Reload-Kriterien fuer spaetere Fixbranches; kein Fix | keiner, read-only Analyse | nein |
| 058 | `058_p1_palette_randomization_model.md` | CFRU/DPE Palette-Randomization-Modell | dokumentiert: Palette-Safety/Skip-Unchanged-Save, Grenze zu echter Palette-Randomization, `PokemonPalettesMod.RANDOM`, `Gen3to5PaletteRandomizer`, `savePokemonPalettes()`, compressed/shared/repointing risks, Graphics-Abgrenzung, Preserve-/Skip-Policy und Reload-Kriterien; kein Fix | keiner, read-only Analyse | nein |
| 059 | `059_p1_type_chart_model.md` | CFRU/DPE Type-Chart-Modell | dokumentiert: Grenze zu Pokemon-Type-Read/Write aus 051, Fairy-vs-TypeChart-Grenze, Stellar-/unsupported-Type-Grenze, Type-Effectiveness-Table-Risiken, Preserve-/Skip-Policy und Reload-Kriterien; kein Fix | keiner, read-only Analyse | nein |
| 060 | `060_p1_gui_suboptions_regression_matrix.md` | CFRU/DPE GUI-Suboptions-Regressionsmatrix | dokumentiert: konkrete FVX-GUI-Hauptoptionen und Suboptionen nach Statusklassen, belegten Datenpfaden, wahrscheinlich stabilen Suboptionen, modellierten offenen Writern und ungetesteten GUI-Kombinationen; kein Fix | keiner, read-only Analyse | nein |
| 061 | `061_p1_regression_smoke_plan.md` | CFRU/DPE P1 Regression-Smoke-Plan | dokumentiert: priorisierte Smoke-Gruppen mit Feature-IDs, spaetere Metriken, Reihenfolge, Stop-Regeln und explizite Nicht-Smoke-Fixbereiche fuer offene Writer; keine Testausfuehrung | keiner, read-only Analyse | nein |
| 062 | `062_p1_global_species_pool_regression_smoke.md` | CFRU/DPE P1 Global Species Pool Regression-Smoke-Plan | dokumentiert: erster geplanter Smoke fuer `FVX-GEN-001` Limit Pokemon inklusive Generation Limits / related Pokemon und `FVX-GEN-002` No Premature Evolutions gegen einen einzelnen stabilen Species-Carrier; keine Testausfuehrung | keiner, read-only Analyse | nein |
| 063 | `063_p1_starters_suboptions_regression_smoke.md` | CFRU/DPE P1 Starters Suboptions Regression-Smoke-Plan | dokumentiert: Starter-Suboptionen `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` ueber den belegten `FVX-SST-002`-Carrier; Starter Held Items und offene Writer ausgeschlossen; keine Testausfuehrung | keiner, read-only Analyse | nein |
| 064 | `064_p1_global_species_pool_regression_smoke_results.md` | CFRU/DPE P1 Global Species Pool Regression-Smoke-Ergebnisse | bestaetigt sanitisiert: Baseline Carrier, `FVX-GEN-001` Generation Limits, `FVX-GEN-001` related Pokemon und `FVX-GEN-002` No Premature Evolutions im `FVX-SST-002`-Starter-Carrier-Smoke mit Save/Log/Reload true, `Starter-Mismatches=0` und `stacktrace=none`; keine offenen Writer | lokal/ignored, nicht dokumentiert | nein |
| 065 | `065_p1_starters_suboptions_regression_smoke_results.md` | CFRU/DPE P1 Starters Suboptions Regression-Smoke-Ergebnisse | bestaetigt sanitisiert: `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` im Starter-Species-Writer-Smoke mit Save/Log/Reload true, `Starter-Mismatches=0`, `Filterverletzungen=0` und `stacktrace=none`; Starter Held Items und offene Writer bleiben separat | lokal/ignored, nicht dokumentiert | nein |
| 066 | `066_type_chart_preserve_effectiveness_fix_diagnostics.md` | CFRU/DPE TypeChart Preserve Effectiveness Fix Diagnose | bestaetigt: TypeEffectiveness-only mit Save/Log/Output/Reload true, `writeReloadTypeChartMismatches=0`, Fairy-Reload als raw `0x17`, unsupported/Stellar nicht eingefuehrt oder normalisiert, Foresight-/Endtable-Terminatoren erhalten | lokal/ignored, nicht dokumentiert | nein |
| 067 | `067_type_effectiveness_followup_smoke_plan.md` | CFRU/DPE TypeEffectiveness-Folgesmoke-Plan | dokumentiert: einzelne spaetere Slices fuer `FVX-TYPE-001` Balanced, Keep Type Identities und Inverse, `FVX-TYPE-002` Add Random Immunities sowie `FVX-TYPE-003` Update Type Effectiveness; keine Ausfuehrung | keiner, read-only Analyse | nein |
| 068 | `068_type_effectiveness_followup_smoke_results.md` | CFRU/DPE TypeEffectiveness-Folgesmoke-Ergebnisse | bestaetigt sanitisiert: Balanced, Keep Type Identities, Inverse, Add Random Immunities und Update Type Effectiveness jeweils mit Save/Log/Output/Reload true, `writeReloadTypeChartMismatches=0`, erhaltenen Terminatoren, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none` | lokal/ignored, nicht dokumentiert | nein |
| 069 | `069_p1_similar_strength_same_type_regression_smoke.md` | CFRU/DPE P1 Similar Strength / Same Type Regression-Smoke-Plan | dokumentiert: spaetere Wild-, Trainer- und Evolution-Slices fuer Similar Strength, Same Type, Type Themes und Type Restrictions ueber belegte Species-/BST-/Type-Datenpfade; keine Ausfuehrung | keiner, read-only Analyse | nein |
| 070 | `070_p1_similar_strength_same_type_regression_smoke_results.md` | CFRU/DPE P1 Similar Strength / Same Type Regression-Smoke-Ergebnisse | gemischt: Trainer Similar Strength unter `FVX-FOE-001` bestaetigt mit Save/Log/Output/Reload true und `writeReloadTrainerPokemonMismatches=0`; Wild Similar Strength, Wild Type Restrictions, `FVX-FOE-009` und Evolutions Same Typing blockieren beim Save; Evolutions Similar Strength reloadet mit `writeReloadEvolutionMismatches=24` und `Bad Egg=true` | lokal/ignored, nicht dokumentiert | nein |
| 071 | `071_p1_070_blocked_slices_followup_plan.md` | CFRU/DPE P1 070 Blocked Slices Follow-up Plan | dokumentiert: read-only Folgeanalyse-Plan fuer blockierte 070-Slices, getrennt nach Wild-Carrier-/Placeholder-Scope, Trainer-Type-Diversity, Evolution-Reload-/Bad-Egg-Scope und Evolution-Same-Typing-/Null-Scope; keine Ausfuehrung | keiner, read-only Analyse | nein |
| 072 | `072_p1_wild_070_blockers_diagnostics_plan.md` | CFRU/DPE P1 Wild 070 Blockers Diagnostics Plan | dokumentiert: read-only Diagnoseplan fuer `FVX-WILD-011` und `FVX-WILD-004` im `FVX-WILD-001` Standard/Fallback-Wild-Carrier, getrennt nach BST-/Species-Pool-Filter, Species-Type-Filter und Wild-Nullslot-/Placeholder-Scope; keine Ausfuehrung | keiner, read-only Analyse | nein |
| 073 | `073_p1_wild_filter_carrier_diagnostics_plan.md` | CFRU/DPE P1 Wild Filter Carrier Diagnostics Plan | dokumentiert: read-only Diagnose-/Harness-Plan fuer den Wild-Filter-Carrier aus 072; trennt Carrier-Scope, Area-/Encounter-Slot-Scope, BST-/Species-Pool-Filter und Species-Type-Filter; keine Ausfuehrung | keiner, read-only Analyse | nein |
| 074 | `074_p1_wild_filter_carrier_code_diagnosis.md` | CFRU/DPE P1 Wild Filter Carrier Code Diagnosis | dokumentiert: read-only Codeanalyse fuer `FVX-WILD-011` und `FVX-WILD-004`; wahrscheinliche Ursache ist ein `GAME`-Mapping-/InfoMap-Nullslot-Pfad vor BST-/Type-Filterauswahl; keine Ausfuehrung | keiner, read-only Analyse | nein |
| 075 | `075_wild_filter_carrier_nullslot_fix_diagnostics.md` | CFRU/DPE Wild Filter Carrier Nullslot Fix Diagnostics | bestaetigt: UPR-FVX-Fix fuer WildEncounterRandomizer Mapping-/InfoMap-Nullslot-Scope; `FVX-WILD-011` und `FVX-WILD-004` jeweils mit Save/Log/Output/Reload true, `writeReloadWildPokemonMismatches=0`, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none` | lokal/ignored, nicht dokumentiert | nein |
| 076 | `076_p1_trainer_type_diversity_blocker_diagnostics_plan.md` | CFRU/DPE P1 Trainer Type Diversity Blocker Diagnostics Plan | dokumentiert: read-only Diagnoseplan fuer den 070-Blocker `FVX-FOE-009` Trainer Type Diversity / Type Themes; klassifiziert `NullPointerException`, fehlenden Output/Reload und `filterViolations=112` als Vor-Abbruch-Befund; keine Ausfuehrung | keiner, read-only Analyse | nein |
| 077 | `077_p1_trainer_type_diversity_code_diagnosis.md` | CFRU/DPE P1 Trainer Type Diversity Code Diagnosis | dokumentiert: read-only Codeanalyse fuer `FVX-FOE-009`; wahrscheinlich konkrete Ursache ist `EnumSet.add(null)` im Force-Diverse-Types-/`updateUsedTypes(...)`-Pfad, weil Trainer-Pools Null-Primary-Type-Species nicht ausschliessen; keine Ausfuehrung | keiner, read-only Analyse | nein |
| 078 | `078_trainer_type_diversity_nulltype_fix_diagnostics.md` | CFRU/DPE Trainer Type Diversity Null-Type Fix Diagnostics | bestaetigt: UPR-FVX-Fix fuer `TrainerPokemonRandomizer` Null-Primary-Type-Scope; `FVX-FOE-009` und Trainer Similar Strength Regression mit Save/Log/Output/Reload true, `writeReloadTrainerPokemonMismatches=0`, `filterViolations=0` fuer Type Diversity, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none` | lokal/ignored, nicht dokumentiert | nein |
| 079 | `079_p1_evolution_same_typing_code_diagnosis.md` | CFRU/DPE P1 Evolution Same Typing Code Diagnosis | dokumentiert: read-only Codeanalyse fuer `FVX-TRAIT-019`; wahrscheinlich konkrete Ursache ist `to.hasSharedType(...)` im Same-Typing-Filter mit Null-Primary-Type-Kandidaten aus dem Evolution-Replacement-Pool; keine Ausfuehrung | keiner, read-only Analyse | nein |
| 080 | `080_evolution_same_typing_nulltype_fix_diagnostics.md` | CFRU/DPE Evolution Same Typing Null-Type Fix Diagnostics | bestaetigt: UPR-FVX-Fix fuer `EvolutionRandomizer` Same-Typing-Null-Primary-Type-Scope; `FVX-TRAIT-019` mit Save/Log/Output/Reload true, `writeReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`; `FVX-TRAIT-018` nur als getrennte Regression | lokal/ignored, nicht dokumentiert | nein |
| 081 | `081_p1_evolution_similar_strength_mismatch_diagnostics.md` | CFRU/DPE P1 Evolution Similar Strength Mismatch Diagnostics | dokumentiert: read-only Code-/Protokollanalyse fuer `FVX-TRAIT-018`; wahrscheinlich ist der 070-Mismatch-Zaehler durch einen zu breiten Vergleich auf nicht persistierte Forme-/Zusatzfelder entstanden; empfiehlt getrennten normalisierten Diagnose-Smoke vor jedem Fix | keiner, read-only Analyse | nein |
| 082 | `082_evolution_similar_strength_normalized_reload_diagnostics.md` | CFRU/DPE Evolution Similar Strength Normalized Reload Diagnostics | bestaetigt: `FVX-TRAIT-018` mit Save/Log/Output/Reload true, `normalizedWriteReloadEvolutionMismatches=0`, `rawWithFormeWriteReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`; `Bad Egg=true` nach 055 klassifiziert | lokal/ignored, nicht dokumentiert | nein |
| 165 | `165_evolution_similar_strength_diagnostics.md` | CFRU/DPE Evolution Similar Strength Diagnostics | read-only Neueinordnung: `diagnosis-ready`; `FVX-TRAIT-018` ist durch 081/082 nicht mehr aktiver Fixblocker, naechster minimaler Pfad ist Statuspflege oder optionaler Non-ROM-Harness-/Code-Review-Plan statt Fixbranch | keiner, read-only Analyse | nein |
| 166 | `166_evolution_same_typing_diagnostics.md` | CFRU/DPE Evolution Same Typing Diagnostics | read-only Neueinordnung: `diagnosis-ready`; `FVX-TRAIT-019` ist durch 079/080 nicht mehr aktiver Fixblocker, naechster minimaler Pfad ist Statuspflege oder optionaler Non-ROM-Harness-/Code-Review-Plan statt Fixbranch | keiner, read-only Analyse | nein |
| 167 | `167_evolution_suboptions_consolidation.md` | CFRU/DPE Evolution Suboptions Consolidation | read-only Konsolidierung: `evolution-scope-consolidated`; `FVX-TRAIT-016` bleibt P1-supported, `018/019` sind `diagnosis-ready`, `017/020-023` plan-only und `024-027` separate nicht begonnene Improvement-/Methoden-Slices | keiner, read-only Analyse | nein |
| 168 | `168_evolution_filter_harness_plan.md` | CFRU/DPE Evolution Filter Harness Plan | read-only Plan: `harness-plan-ready`; `FVX-TRAIT-017` und `020-023` sind ROM-frei mit synthetischen Species/Evolution-Daten und kleinem `RomHandler`-Proxy/Fake testbar, ohne erwarteten Produktivcode-Seam | keiner, read-only Analyse | nein |
| 169 | `169_evolution_filter_non_rom_harness_followup.md` | CFRU/DPE Evolution Filter Non-ROM Harness Follow-up | UPR-FVX PR #42 gepinnt: `EvolutionFilterOptionsTest` deckt `FVX-TRAIT-017` und `020-023` ROM-frei ab; Status `tested-non-rom`, keine P1-Freigabe ohne ROM-Smoke/Reload | keiner, Submodule-Gitlink und Doku | nein |
| 170 | `170_evolution_methods_scope_plan.md` | CFRU/DPE Evolution Methods Scope Plan | read-only Plan: `methods-plan-ready`; `FVX-TRAIT-024` bis `027` bleiben separate Methoden-/Improvement-Slices mit Method-Mapping-, ExtraInfo-, Level-, Time- und Writer-/Reload-Risiken | keiner, read-only Analyse | nein |
| 171 | `171_evolution_methods_decision_review.md` | CFRU/DPE Evolution Methods Decision Review | read-only Review: `decision-review-ready`; `FVX-TRAIT-024` und `027` haben konkrete ROM-freie Method-Mapping-Assertions fuer einen spaeteren kleinen `:romio:test`, waehrend `025` split und `026` Helper-Flag bleiben | keiner, read-only Analyse | nein |
| 172 | `172_evolution_method_decision_harness_followup.md` | CFRU/DPE Evolution Method Decision Harness Follow-up | UPR-FVX PR #43 gepinnt: `EvolutionMethodDecisionTest` deckt `FVX-TRAIT-024` und `027` ROM-frei ab; Status `tested-non-rom`, keine P1-Freigabe ohne Writer-/Reload- oder ROM-Smoke-Evidenz | keiner, Submodule-Gitlink und Doku | nein |
| 173 | `173_evolution_make_easier_scope_plan.md` | CFRU/DPE Evolution Make Evolutions Easier Scope Plan | read-only Plan: `make-easier-plan-ready`; `FVX-TRAIT-025` wird in 025A Condense-/Level-Decision und 025B Gen3-Happiness-Byte-Patch getrennt, `026` bleibt Helper-Flag | keiner, read-only Analyse | ja |
| 083 | `083_move_data_write_preserve_diagnostics.md` | CFRU/DPE MoveData Write Preserve Diagnostics | UPR-FVX-Fix implementiert: klassische MoveData-Bytes `+0..+4` bleiben geschrieben, CFRU/DPE `BattleMove.split` wird im Gate bei `+10` geschrieben, nicht modellierte Bytes bleiben erhalten; Reload-Smoke separat in 084 | keiner | nein |
| 084 | `084_move_data_write_preserve_reload_smoke.md` | CFRU/DPE MoveData Write Preserve Reload-Smoke | bestaetigt: Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `moves.total=992`, `991:PsychicNoise`, category/split reload stabil und Preserve-Bytes fuer unveraenderte Moves bytegleich | lokal/ignored, nicht dokumentiert | nein |
| 085 | `085_move_data_power_accuracy_pp_reload_smoke.md` | CFRU/DPE MoveData Power/Accuracy/PP Reload-Smoke | bestaetigt: Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `powerReloadMismatches=0`, `accuracyReloadMismatches=0`, `ppReloadMismatches=0`, rohe `+1/+3/+4` Bytes stabil und Preserve-Bytes bytegleich | lokal/ignored, nicht dokumentiert | nein |
| 086 | `086_move_data_types_reload_smoke.md` | CFRU/DPE MoveData Types Reload-Smoke | blockiert: Save/Log/Output/Reload true und Preserve-Bytes stabil, aber `writeReloadMoveDataMismatches=54` durch Fairy-Type-Byte-Mismatches im MoveData-`+2 type`-Writer | lokal/ignored, nicht dokumentiert | nein |
| 087 | `087_move_data_fairy_type_byte_fix_diagnostics.md` | CFRU/DPE MoveData Fairy-Type-Byte Fix Diagnostics | bestaetigt: UPR-FVX `fad56f60`, Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0` und Preserve-Bytes bytegleich | lokal/ignored, nicht dokumentiert | nein |
| 088 | `088_move_names_text_menu_scope_plan.md` | CFRU/DPE Move Names / Descriptions Text/Menu-Scope Plan | dokumentiert: `FVX-MOVE-005` ist vom MoveData-Byte-Writer getrennt; Name-only fixed-length Smoke ist realistisch, Move Descriptions / Text/Menu-Repointing vorerst zurueckstellen | keiner, read-only Analyse | nein |
| 089 | `089_move_names_fixed_length_reload_smoke.md` | CFRU/DPE Move Names fixed-length Reload-Smoke | blockiert: lokaler Harness erstellt, aber kein freigegebener lokaler CFRU/DPE Gen9-BPRE-Kandidat mit `moves.total=992` und `991:PsychicNoise` gefunden; `FVX-MOVE-005` bleibt `Write modelliert` | lokal/ignored, nicht dokumentiert | nein |
| 090 | `090_move_names_fixed_length_reload_smoke_retry.md` | CFRU/DPE Move Names fixed-length Reload-Smoke Retry | blockiert: Candidate-Preflight pruefte 94 lokale freigegebene private/ignored Kandidaten, fand aber keinen Stand mit `moves.total=992` und `991:PsychicNoise`; fachlicher Smoke nicht ausgefuehrt; `FVX-MOVE-005` bleibt `Write modelliert` | lokal/ignored, nicht dokumentiert | nein |
| 175 | `175_movedata_write_followup.md` | MoveData Write Follow-up | UPR-FVX PR #45 gemerged und Submodule auf `1be6f517` gepinnt; `Gen3MoveDataWriterTest` und `MoveUpdateDecisionTest` belegen `FVX-MOVE-001/002/003/004/006` ROM-frei als `tested-non-rom`; `FVX-MOVE-005` bleibt Move Names/Text out of scope | keiner | nein |
| 176 | `176_wild_catch_level_followup.md` | Wild Catch/Level Follow-up | UPR-FVX PR #46 gemerged und Submodule auf `c86221d7` gepinnt; `WildCatchLevelDecisionTest` belegt `FVX-WILD-007/010/012` ROM-frei als `tested-non-rom`; keine P1-Freigabe ohne ROM-/Reload-Evidenz | keiner | nein |
| 177 | `177_trainer_type_diversity_followup.md` | Trainer Type Diversity Follow-up | UPR-FVX PR #47 gemerged und Submodule auf `ea526970` gepinnt; `TrainerTypeDiversityGuardTest` belegt `FVX-FOE-009` ROM-frei als `tested-non-rom`; keine P1-Freigabe ohne ROM-/Reload-Evidenz | keiner | nein |
| 178 | `178_trainer_additional_pokemon_followup.md` | Trainer Additional Pokemon Follow-up | UPR-FVX PR #48 gemerged und Submodule auf `32ab7d96` gepinnt; `TrainerAdditionalPokemonTest` belegt `FVX-FOE-005/006/007` ROM-frei als `tested-non-rom`; keine P1-Freigabe ohne ROM-/Reload-Evidenz | keiner | nein |
| 179 | `179_trainer_special_rules_followup.md` | Trainer Special Rules Follow-up | UPR-FVX PR #49 gemerged und Submodule auf `bc46fdc4` gepinnt; `TrainerSpecialRulesTest` belegt `FVX-FOE-010/012/014` ROM-frei als `tested-non-rom`; `FVX-FOE-011/013` bleiben separat; keine P1-Freigabe ohne ROM-/Reload-Evidenz | keiner | nein |
| 180 | `180_trainer_battle_style_followup.md` | Trainer Battle Style Follow-up | UPR-FVX PR #50 gemerged und Submodule auf `5e2d3519` gepinnt; `TrainerBattleStyleTest` belegt `FVX-FOE-011` ROM-frei als `tested-non-rom`; keine P1-Freigabe ohne ROM-/Reload-Evidenz | keiner | nein |
| 091 | `091_palette_randomization_preserve_repoint_plan.md` | CFRU/DPE Palette Randomization Preserve/Repoint Plan | dokumentiert: echte Palette-Randomization ist ein komprimierter Repointing-/Shared-Pointer-Writer; direkter Fix noch nicht eng genug, zuerst read-only Pointer-/Compression-Diagnose noetig; `FVX-GFX-001..004` bleiben `Write modelliert` | keiner, read-only Analyse | nein |
| 092 | `092_palette_pointer_compression_diagnostics_plan.md` | CFRU/DPE Palette Pointer / Compression Diagnostics Plan | dokumentiert: spaetere Diagnose soll Normal-/Shiny-Palette-Pointer, Dekomprimierbarkeit, Single-Owner/Shared, missing/invalid und sichere Kandidaten aggregiert klassifizieren; kein Fix, kein Repointing | keiner, read-only Analyse | nein |
| 093 | `093_palette_pointer_compression_diagnostics.md` | CFRU/DPE Palette Pointer / Compression Diagnostics | bestaetigt sanitisiert: `candidateLoaded=true`, `palettePointerScanSuccessful=true`, `candidateWritablePalettes=385`, `candidateWritableNormalPalettes=385`, `candidateWritableShinyPalettes=0`; shared/invalid/missing/decode-failed bleiben preserve-only | lokal/ignored, nicht dokumentiert | nein |
| 094 | `094_palette_single_owner_normal_only_fix_scope_plan.md` | CFRU/DPE Palette Single-owner Normal-only Fix-Scope Plan | geplant: spaeterer Scope nur Normal-Paletten, single-owner, dekomprimierbar, gueltig, non-shared, non-cross-kind; Shiny/shared/invalid/missing/decode-failed preserve-only | keiner | nein |
| 095 | `095_palette_normal_single_owner_write_guard_fix_diagnostics.md` | CFRU/DPE Palette Normal Single-owner Write Guard Fix Diagnostics | UPR-FVX-Fix implementiert: Normal-only-Guard fuer sichere single-owner/decode-success/non-shared Paletten; kein Reload-Smoke in diesem Block, `FVX-GFX-001..004` bleiben `Write modelliert` | Build-Artefakte lokal/ignored, nicht dokumentiert | ja |

## Aktuell bestaetigter Stand

Latest ist Nr. 095: CFRU/DPE Palette Normal Single-owner Write Guard Fix Diagnostics.

Kernaussagen:

- UPR-FVX `2697511da9a97df4c29c00dfda8b40e556020489` implementiert zusaetzlich den engen CFRU/DPE Normal-Palette-Single-owner-Write-Guard.
- `Randomize Move Power`, `Randomize Move Accuracy` und `Randomize Move PP` bleiben durch Diagnose 085 mit `writeReloadMoveDataMismatches=0` belegt.
- `Randomize Move Types` reloadet in Diagnose 087 mit `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true` und `writeReloadMoveDataMismatches=0`.
- `moves.total=992` und `991:PsychicNoise` bleiben nach Reload stabil.
- Fairy im MoveData-`+2 type`-Byte reloadet stabil: `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`.
- Nicht modellierte Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` bleiben bytegleich erhalten.
- `Update Moves` und Category-/Split-Reload bleiben durch Diagnose 084 belegt.
- Diagnose 088 trennt `FVX-MOVE-005` vom MoveData-Byte-Writer und empfiehlt einen Name-only fixed-length Smoke.
- Diagnose 089 konnte diesen Smoke noch nicht fachlich auswerten, weil lokal kein freigegebener CFRU/DPE Gen9-BPRE-Kandidat mit `moves.total=992` und `991:PsychicNoise` gefunden wurde.
- Diagnose 090 wiederholte den Candidate-Preflight sanitisiert: `candidateFilesChecked=94`, `candidatePreflightSuccessful=false`, `candidateMovesTotal=not available`, `candidateHighestMove=not available`; der fachliche Smoke wurde erneut nicht ausgefuehrt.
- `FVX-MOVE-005` bleibt `Write modelliert`; Move Descriptions / Text/Menu-Repointing bleibt zurueckgestellt.
- Diagnose 091 bestaetigt fuer echte Palette-Randomization: `PokemonPalettesMod.RANDOM` faellt in einen komprimierten `rewriteCompressedPalette()`-/`DataRewriter`-Repointing-Pfad; shared/missing/invalid Pointer und Forme-/Mapping-Fragen muessen vor einem Fix read-only inventarisiert werden.
- Diagnose 092 plant diese Inventarisierung als separaten sanitisierten Diagnose-Lauf: Normal-/Shiny-Palette-Pointer, Decode-Failures, Single-Owner/Shared, missing/invalid und `candidateWritablePalettes` werden nur aggregiert dokumentiert.
- Diagnose 093 fuehrt diese Inventarisierung read-only aus: `candidateLoaded=true`, `palettePointerScanSuccessful=true`, `candidateWritablePalettes=385`, aber `candidateWritableShinyPalettes=0`; ein spaeterer Fix darf nur normal-palette-only single-owner/decompressible Kandidaten betrachten.
- Diagnose 095 implementiert den Guard-Fix, fuehrt aber keinen ROM-/Reload-Smoke aus; `FVX-GFX-001` bleibt bis zum separaten Reload-Smoke `Write modelliert`.
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`; Custom Player Graphics bleibt separat.

## Lokale Artefaktpflege

Der Ordner `05_builds/randomizer-smoke/` ist nur fuer lokale, ignored Smoke-Outputs gedacht. Alte lokale `.gba`- und `.log`-Artefakte duerfen entfernt werden, wenn sie eindeutig zu dokumentierten Smoke-Laeufen gehoeren und keine Markdown-Protokolle betroffen sind.

Wenn ein Artefakt nicht eindeutig Smoke-Output ist, bleibt es lokal liegen und wird im jeweiligen Protokoll oder in der Session-Dokumentation als `manuell pruefen` markiert.

## Offene Themen

- Gen8/9-Move-Datenmodell-Fix
- Learnsets/Movesets
- TM/Tutor/Egg-Move-Pfade
- TM/Tutor/Abilities
- CFRU Day/Night

- `096_palette_normal_single_owner_reload_smoke.md` - Sanitisiert blockierter Reload-Smoke für `FVX-GFX-001` Normal-only Single-owner Palette-Write-Guard; kein UPR-FVX-ladbarer `candidateSpeciesTotal=1439` Zielkandidat verfügbar, daher keine Feature-Hochstufung.
| 097 | `097_field_items_shops_pickup_scope_plan.md` | CFRU/DPE Field Items / Shops / Pickup Scope Plan | geplant: Field Items, Shops und Pickup muessen getrennt behandelt werden; Field Items zuerst, Pickup und Shops separat; gemeinsame Item-Pool-/Bad-Item-Policy noetig, aber kein gemeinsamer Fixblock | keiner, read-only Analyse | nein |

- 098 - `098_field_items_scope_diagnostics_plan.md`: Read-only CFRU/DPE Field-Items-only diagnostics plan. Splits visible Itemballs, Hidden Items/Signposts, TM/Non-TM slots, Required Field TMs and item safety policy away from Shops/Pickup.

- 099 - `099_field_items_scope_diagnostics.md`: Sanitized blocked Field-Items-only diagnostics block. PR #143 was merged, but no explicitly approved local CFRU/DPE Gen9-BPRE candidate was provided; `candidateFilesChecked=0`, `candidateLoaded=false`, no fachlicher Field-Item scan, `FVX-ITEM-001..004` remain `Write modelliert`.

- 100 - `100_field_items_scope_diagnostics_candidate.md`: Sanitized read-only Field-Items-only candidate diagnostics. `candidateLoaded=true`, `fieldItemScanSuccessful=true`, `fieldItemsTotal=339`, visible `168`, hidden `171`, allowed `280`, disallowed `59`, TM slots `28`, Non-TM slots `311`, `requiredFieldTMMissing=0`, invalid/unloaded `0`; recommends guarded Field-Items write/smoke.

- 101 - `101_field_items_allowed_slot_write_guard.md`: Field-Items-only Guard-Entscheidung. Bestehender Gen3 `getFieldItems()` / `setFieldItems(...)`-Pfad schreibt nur allowed Slots; kein UPR-FVX-Codefix, kein Write-/Reload-Smoke ohne explizite Kandidatenfreigabe; `FVX-ITEM-001..004` bleiben `Write modelliert`.

- 102 - `102_field_items_allowed_slot_reload_smoke.md`: Sanitized Field-Items-only `FVX-ITEM-001 Field Items Shuffle` Write-/Reload-Smoke. Save/log/output/reload true, `fieldItemsTotalBefore/After/Reload=339`, Field-Item reload mismatches `0`, visible/hidden mismatches `0`, TM/Non-TM slot mismatches `0`, required TMs preserved, disallowed writes `0`; `FVX-ITEM-001` now `GUI-kompatibel` for the narrow Shuffle scope.

- 103 - `103_field_items_random_reload_smoke.md`: Sanitized Field-Items-only `FVX-ITEM-002 Field Items Random` smoke with `banBadRandomFieldItems=false`. Candidate loaded and Field-Items scope stayed `339`, but save failed with `RandomizationException`; no output/reload, no Feature-Hochstufung. Next: Random TM-pool blocker plan.

- 104 - `104_field_items_random_tm_pool_blocker_plan.md`: Read-only Plan fuer den `FVX-ITEM-002` Random-TM-Pool-Blocker. Ursache liegt wahrscheinlich in `ItemRandomizer.randomizeTMFieldItems(...)`: benoetigte TM-Field-Slots `28`, Required Field TMs `24`, Unique-TM-Pool muss exakt passen; naechster Schritt ist ein enger TM-Pool-Fixbranch.

- 105 - `105_field_items_random_tm_pool_fix.md`: UPR-FVX-Fix fuer den `FVX-ITEM-002 Field Items Random` TM-Pool vorbereitet. Required Field TMs bleiben Pflicht, Filler-TMs werden dedupliziert aus geladenen TMs plus aktuellen Field-TM-Slots gebaut; kein fachlicher ROM-Reload-Smoke in diesem Block, daher keine Feature-Hochstufung.

- 106 - `106_field_items_random_tm_pool_reload_smoke.md`: Sanitized Field-Items-only `FVX-ITEM-002 Field Items Random` reload smoke after UPR-FVX PR #36. Candidate loaded, but save still blocks before output/reload. Pool deficit is cleared (`randomTmPoolDeficit=0`); active blocker is API TM-slot scope mismatch (`randomTmNeededSlots=0` vs raw `tmFieldItemSlots=28`).

- 107 - `107_field_items_random_api_tm_slot_scope_plan.md`: Read-only plan for the `FVX-ITEM-002` API TM-slot blocker. Raw diagnostics find `tmFieldItemSlots=28`, but `Gen3RomHandler.getFieldItems()` exposes `0` TM slots because the Field-Items API filters on `Item::isAllowed`; next fix should be CFRU/DPE-gated and must not make TMs globally allowed.

- 108 - `108_field_items_api_tm_slot_scope_fix.md`: UPR-FVX PR #37 prepares the CFRU/DPE Field-Items API TM-slot fix. `Gen3RomHandler.getFieldItems()` / `setFieldItems(...)` expose Field-TM slots in the CFRU/DPE gate without making TMs globally allowed; compile passed, reload smoke remains separate.

- 109 - `109_field_items_api_tm_slot_reload_smoke.md`: Sanitized Field-Items-only `FVX-ITEM-002 Field Items Random` reload smoke after UPR-FVX PR #37. Save/log/output/reload true, Field-Item reload mismatches `0`, API/raw TM-slot alignment `28/28`, Required Field TMs preserved, no global TM allowed change; `FVX-ITEM-002` is now `GUI-kompatibel` only for `banBadRandomFieldItems=false`.

- 110 - `110_field_items_random_even_reload_smoke.md`: Sanitized Field-Items-only `FVX-ITEM-003 Field Items Random even distribution` reload smoke. Save/log/output/reload true, Field-Item reload mismatches `0`, API/raw TM-slot alignment `28/28`, Required Field TMs preserved, no global TM allowed change; `FVX-ITEM-003` is now `GUI-kompatibel` only for `banBadRandomFieldItems=false`.

- 111 - `111_field_items_ban_bad_scope_plan.md`: Read-only plan for `FVX-ITEM-004 Field Items Ban Bad Items`. Confirms Ban Bad affects only the Non-TM Field-Items pool via `getNonBadItems()`, keeps TM/Required-TM handling separate, and recommends first smoke as `FieldItemsMod.RANDOM` with `banBadRandomFieldItems=true`.

- 112 - `112_field_items_random_ban_bad_reload_smoke.md`: Sanitized Field-Items-only `FVX-ITEM-002 Field Items Random` smoke with `banBadRandomFieldItems=true`. Save/log/output/reload true, Field-Item reload mismatches `0`, Required Field TMs preserved, `badFieldItemWrites=0`; `FVX-ITEM-004` is tested for `FieldItemsMod.RANDOM`, while Random Even + Ban Bad remains separate.

- 113 - `113_field_items_random_even_ban_bad_reload_smoke.md`: Sanitized Field-Items-only `FVX-ITEM-003 Field Items Random even distribution` smoke with `banBadRandomFieldItems=true`. Save/log/output/reload true, Field-Item reload mismatches `0`, Required Field TMs preserved, `badFieldItemWrites=0`, Random-Even queue/distribution stable; `FVX-ITEM-004` is now GUI-compatible for Field Items Random and Random Even only.

- 114 - `114_pickup_items_scope_diagnostics_plan.md`: Read-only plan for the CFRU/DPE Pickup Items scope. Identifies `FVX-ITEM-010` as a separate table/locator/probability writer, recommends a Pickup-only candidate diagnostic before any write smoke, and keeps Field Items, Shops and Held Items separate.

- 115 - `115_pickup_items_scope_diagnostics.md`: Sanitized read-only Pickup-only candidate diagnostics. Locator/count/entry-size/probability model stable (`pickupLocatorSuccessful=true`, `pickupItemsTotal=16`, `pickupEntrySize=4`, `pickupProbabilityModelStable=true`), no invalid/unloaded/fallback/placeholder Pickup IDs; recommends Pickup Random without Ban Bad before a separate Ban-Bad smoke.

- 117 - `117_pickup_items_reload_locator_blocker_plan.md`: Read-only Plan fuer den Pickup-Reload-Locator-Blocker nach `PickupItemsMod.RANDOM`. Diagnose 116 spricht fuer einen inhaltsbasierten `PickupTableStartLocator`, der nach Random-Write nicht mehr passt; empfiehlt einen engen reloadstabilen Pickup-Table-Locator-Fix vor Pickup Ban Bad.

- 116 - `116_pickup_items_random_reload_smoke.md`: Sanitized Pickup-only `FVX-ITEM-010 Pickup Items Random` smoke with `banBadRandomPickupItems=false`. Save/log/output/reopen true, but blocked because fresh reload cannot locate the Pickup table after random write (`pickupLocatorSuccessful=false`, `pickupItemsTotalReload=0`, reload mismatches `16`); no feature upgrade.

- 118 - `118_pickup_items_reload_locator_fix.md`: UPR-FVX-Fix fuer reloadstabile Pickup-Table-Lokalisierung im CFRU/DPE Gen9-BPRE-Gate; Pickup-only Random-Smoke mit `banBadRandomPickupItems=false` reloadet stabil mit `pickupItemReloadMismatches=0`; Pickup Ban Bad bleibt separat.

- 119 - `119_pickup_items_ban_bad_scope_plan.md`: Read-only plan for `FVX-ITEM-010 Pickup Items Random` with `banBadRandomPickupItems=true`. Confirms Ban Bad only swaps the Pickup candidate pool from allowed to non-bad allowed items; recommends a direct Pickup-only Ban-Bad reload smoke next, with Field Items, Shops and Held Items kept separate.

- 120 - `120_pickup_items_random_ban_bad_reload_smoke.md`: Sanitized Pickup-only `FVX-ITEM-010 Pickup Items Random` smoke with `banBadRandomPickupItems=true`. Save/log/output/reload true, Pickup reload mismatches `0`, bad Pickup writes `0`, bad pool candidates/excluded `51`, non-bad pool `485`; `FVX-ITEM-010` is now GUI-compatible for the tested Pickup-only Random scope with and without Ban Bad.
