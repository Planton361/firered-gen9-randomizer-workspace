# Roadmap update - Gen Limit / Special Form / Mechanic Item smoke

- UPR-FVX compat commit `765d8ec0ab298bbaab4aa9f8f31b93c7259a47e5` is merged and the workspace submodule is pinned to it.
- The pin includes the Gen-Limit 1-9, pool filtering, Gen7/8/9 Intro Mon visual candidates, Special-Form filtering/settings/GUI, regional/evolution-relative separation, Trainer Class Sprite Sync GUI exposure, Oak-Lab Rival counter-starter preservation and source-backed CFRU/DPE mechanic item category work through PR #150.
- Evidence 212 records targeted local Gen Limit / Special Form / Mechanic Item smoke.
- Gen Limit / Special Form / Mechanic Item Exclusions move to `PASS_TARGETED_LOG_VISUAL_SMOKE_WITH_CAVEATS`.
- Local checks report no current Pokemon special-form filtering issue; Regional forms are not pulled in by Evolutionary Relatives unless Regional Forms across Gen Limit is enabled; mechanic item filtering now uses source-backed CFRU/DPE categories for Mega/Z/Dynamax-GMax items.
- Caveats remain: targeted local smoke only, no full playthrough, Plates/Drives/Memories/Nectars have no separate user-facing policies yet, Static Script/Gift/NPC item sources remain caveated when outside replacement pools, and custom/future form encodings outside documented CFRU/DPE identity blocks remain audit-required.
- No Full-Playthrough or P1 promotion follows from this smoke.

# Roadmap update - Misc Tweaks behavior smoke

- UPR-FVX PR #125, PR #126 and PR #127 are merged and the workspace submodule is pinned to `155fac0b33474f6ed5b3fbaed7dd9bf24b4e1315`.
- PR #125 covers CFRU/DPE BPRE Running Shoes misc-tweak behavior, PR #126 covers CFRU/DPE BPRE Catching Tutorial species mapping and PR #127 covers Fast Egg Hatching missing-`BreedingInfo` handling.
- Evidence 210 records targeted local Misc Tweaks behavior smoke.
- Misc Tweaks move from behavior-smoke-open to `PASS_TARGETED_BEHAVIOR_SMOKE_WITH_CAVEATS`.
- Fast Egg Hatching remains caveated as crash-free randomization/output-load evidence, not full hatch-cycle proof; Ban Lucky Egg is likely pass / no issue observed; Reusable TMs and Forgettable HMs are CFRU-provided and should not be duplicated by the UPR-FVX stable profile.
- No Full-Playthrough or P1 promotion follows from this smoke.

# Roadmap update - Type Effectiveness battle smoke

- Evidence 211 records targeted local Type Effectiveness battle smoke.
- Type Effectiveness moves to `PASS_TARGETED_BATTLE_SMOKE_WITH_CAVEATS`.
- Local evidence: Type Effectiveness was tested in battle, effectiveness behavior looked appropriate and no battle crashes were reported.
- Caveat: targeted battle smoke only, no full type-chart matchup matrix, no Full-Playthrough and no P1 promotion.

# Roadmap update - Graphics/Palettes visual smoke

- UPR-FVX PR #124 is merged and the workspace submodule is pinned to `0eb815418470fa1ac000695b95d09cb084338dca`.
- The pin includes PR #123's Gen3/CFRU-DPE palette output write fix and PR #124's expanded trainer logging fallback.
- Added sanitized evidence file `08_tests/randomizer/209_graphics_palettes_visual_smoke.md`.
- Sanitized local evidence confirms `Pokemon Palettes: Randomized/Changed`, `normalPaletteWriteAttempts=841`, Palette Audit `sampledCount=21`, `normalChangedCount=21`, `shinyChangedCount=0`, `unchangedCount=0`, sampled normal palettes changed from base, visible palette changes observed, and no final `Error during logging`.
- Graphics/Palettes moves from prepared-only to targeted visual/audit smoke passed with caveats. Shiny behavior remains separately caveated by the sampled audit.
- No ROM run by Codex, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Graphics/Palettes smoke settings prep

- Local ignored manual smoke input `05_builds/randomizer-smoke/settings/manual/graphics_palettes_smoke.rnqs` is prepared from the generated `risk_graphics_palettes_visual` profile.
- Scope stays isolated to `FVX-GFX-001` through `FVX-GFX-004`; no Wild, Foe, Items, Misc, TypeEffectiveness/type chaos or manual Custom Player Graphics scope is mixed in.
- This is preparation only: no ROM run by Codex, no evidence update and no P1 promotion.

# Roadmap update - Wild encounter output audit sync

- UPR-FVX PR #118 is merged and the workspace submodule is pinned to `ed692d07bfc81405706f2b94fda06639426e6a75`.
- The pinned change adds an opt-in Wild Encounter Base-vs-Output Audit for Gen3/FRLG/CFRU-DPE.
- The audit is diagnostic-only: it compares modeled Gen3 base `WildPokemon` table slots from Base-ROM and Output-ROM and reports changed slots plus summary counts, but it does not change writer or randomizer behavior.
- CFRU/DPE special/runtime wild sources remain follow-up if audit evidence and ingame observations diverge.
- No ROM run by Codex, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Combined trainer visual runtime smoke

- Added sanitized evidence file `08_tests/randomizer/208_combined_trainer_visual_runtime_smoke.md`.
- Combined trainer visual runtime smoke is `PASS_WITH_CAVEATS`.
- Sanitized local evidence confirms Intro Mon visibly randomized, Player Charmander -> Oak-Lab Rival Squirtle and Route-22 Rival Squirtle, Route 22 Rival sprite consistent with Oak-Lab Rival sprite, Viridian Forest trainer sprites randomized and no crash/freeze/garbled sprite observed.
- Route 22 Rival non-starter Pokemon observed: Silvally Lv9. Interpretation: Rival Carries Starter Through Game protects/corrects the Rival starter slot only; non-starter Rival Pokemon remain eligible for Foe Pokemon randomization.
- This strengthens targeted visual/runtime confidence for the combined trainer profile, but remains below full-playthrough coverage and below P1 promotion.
- No ROM run by Codex, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Rival counter starter and combined visual smoke

- UPR-FVX PR #117 is merged and the workspace submodule is pinned to `5983011752273e00c402e25cc1ae1a9baca110f1`.
- The pinned fix preserves/corrects `Rival Carries Starter Through Game` after Foe Pokemon randomization and prevents invalid Intro Mon species `0` writes in the extended CFRU/DPE BPRE pool.
- Sanitized local evidence confirms the combined visual Rival test is fixed, Intro Mon was visibly Blissey, Player Charmander -> Rival Squirtle, and no crash/freeze/garbled sprite was reported.
- Trainer Class Sprite Sync remains visually okay from prior checks: Viridian Forest trainers get per-trainer randomized classes/sprites and Rival keeps consistent class/sprite across appearances.
- Caveat: targeted visual smoke only, not full-playthrough coverage, all-starter-choice proof, broad route/category proof or P1 promotion.
- No ROM run by Codex, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Trainer Class Sprite Sync final smoke

- UPR-FVX PR #116 is merged and the workspace submodule is pinned to `36dd431d059bc69eb1bee3311200e28c872c6cc9`.
- The pinned feature finalizes opt-in `MODE-TRAINER-CLASS-SPRITE-SYNC` for Gen 3 Trainer Class Sprite Sync.
- `Randomize Trainer Names` remains separate and changes only personal names.
- `Randomize Trainer Class Names` remains legacy/textlabel-only unless Sprite Sync is enabled.
- With Sprite Sync enabled, class label, `trainerClass` and visible `trainerPic` follow the Trainer Class Names assignment. Regular trainers use per-trainer assignments; Rival/Friend rows share one grouped class/sprite identity; eligible runtime-source rows participate in the sync.
- Sanitized local evidence confirms Viridian Forest Bug Catcher classes randomize per trainer, Rival keeps the first randomized sprite across later appearances, other sampled trainers appeared aligned, and no garbled sprite/crash was reported.
- Caveat: targeted visual smoke only, not full-playthrough coverage, broad route/category proof or P1 promotion.
- No ROM run by Codex, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Trainer Class Sprite Sync

- UPR-FVX PR #111 is merged and the workspace submodule is pinned to `4805a5a930bc97203199816222465c76de2f2150`.
- The pinned feature adds opt-in `MODE-TRAINER-CLASS-SPRITE-SYNC` for Gen 3 Trainer Class Sprite Sync.
- `Randomize Trainer Names` remains separate and changes only personal names.
- `Randomize Trainer Class Names` remains legacy/textlabel-only unless Sprite Sync is enabled.
- With Sprite Sync enabled, `trainerClass` and visible `trainerPic` follow the Trainer Class Names old-class-ID to target-class-ID mapping. The goal is class label / classId / pic consistency, not Regular-only remapping.
- Sanitized pre-merge evidence showed a regular trainer battle started, the visible sprite changed, and class/sprite sync markers appeared in the log. Further local smoke is still required on the merged pin.
- No ROM run by Codex, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Intro Mon visual source fix smoke

- UPR-FVX PR #109 is merged and the workspace submodule is pinned to `a9bb4a5f201c5078ec02fe1f2f8417695448afe9`.
- The pinned fix syncs the confirmed CFRU/DPE Gen9 BPRE Intro Mon visual source by updating the Nidoran female `PokemonFrontImages` and `PokemonNormalPalettes` entries to the selected intro species' asset pointers during Intro Mon randomization.
- Sanitized local smoke confirms the visible Oak intro sprite changed away from Nidoran female and no crash, freeze or garbled sprite was observed.
- `FVX-GEN-003` / Intro Mon visual mismatch is now locally fixed for the targeted smoke, but this remains below P1 and below full-playthrough coverage.
- No ROM run by Codex, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Intro Mon visual source diagnostics

- UPR-FVX PR #107 is merged and the workspace submodule is pinned to `a7e098a5158d824b1ddec62a286f2a6ffafce8e4`.
- The pinned diagnostics now include an opt-in Intro Mon Visual-Source report for known FRLG Intro Mon literals/pointers and optional Base-ROM vs randomized Output-ROM comparison.
- Setting semantics are explicit for future profile work: `No Random Intro Mon` is the negative GUI option, `randomizeIntroMon=true` is the active Randomize Intro Mon path, `MODE-INTRO-RANDOM` sets true, and `MODE-NO-RANDOM-INTRO` / `FVX-GEN-003` set false.
- This does not fix the visible Intro Mon mismatch and does not prove ingame visuals; it only provides local sanitized evidence to identify whether the known vanilla-style sources changed.
- No ROM run by Codex, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Runtime source trainer randomization smoke evidence refresh

- UPR-FVX PR #105 is merged and its smoke evidence is documented while the workspace submodule remains pinned to PR #106 commit `5bb1d853f132095922be2aceef55af2878192b85`.
- Generic `RUNTIME-SOURCE` trainers are treated as regular trainers for randomizer eligibility while known special runtime tags remain special.
- Local sanitized evidence confirms Viridian Forest trainer IDs `531/532` load randomized parties, raw parties match loaded parties, and the observed battle shows randomized Eiscue.
- The randomized output audit reports `unloaded-valid-parties total=0`, equivalent to no focused valid-runtime-not-loaded rows left in that audit mode.
- Additional sanitized observations show Rival 2 trainer IDs `329/330/331` randomized and Brock trainer ID `414` randomized to `[Drifloon Lv12, Growlithe Lv14]`.
- This confirms the targeted runtime-source Trainer Pokemon path, but does not promote broader Trainer/Foe P1 support.
- Loaded-mismatch, invalid audit classifications, out-of-range rows and full playthrough coverage remain separate follow-up lanes.
- No ROM run by Codex, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Runtime trainer post-randomization audit

- UPR-FVX PR #106 is merged and the workspace submodule is pinned to `5bb1d853f132095922be2aceef55af2878192b85`.
- The pinned diagnostics now include an opt-in Pre/Post Runtime-Trainer-Audit for comparing a local Base-ROM with a randomized Output-ROM.
- The audit helps verify whether valid script-referenced runtime trainer rows changed from base, are loaded in the output model and match the output raw party.
- This is an audit-only roadmap step: no new writer, sync or randomizer behavior, no ROM run by Codex and no P1 promotion.
- Next Foe Trainer work should use sanitized local two-ROM audit evidence before opening any follow-up for unchanged, loaded-mismatch or still-not-loaded runtime rows.

# Roadmap update - Runtime source trainer randomization smoke

- UPR-FVX PR #105 is merged and the workspace submodule is pinned to `c0d8e33f3547020c6fd2fe5baffbc80ec93f9197`.
- Generic `RUNTIME-SOURCE` trainers are now treated as regular trainers for randomizer eligibility while known special runtime tags remain special.
- Local sanitized evidence confirms Viridian Forest trainer IDs `531/532` load randomized parties, raw parties match loaded parties, and the observed battle shows randomized Eiscue.
- This upgrades the targeted runtime-source Trainer Pokemon path from strict-sync-pinned to locally smoke-confirmed for `531/532`, but does not promote broader Trainer/Foe P1 support.
- Loaded-mismatch and invalid audit classifications remain separate follow-up lanes.
- No ROM run by Codex, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Strict runtime trainer source sync

- UPR-FVX PR #104 is merged and the workspace submodule is pinned to `6dcda7e499cd3e22319c447c7d7df9ddbd67de60`.
- The pinned trainer path now strictly syncs valid audit candidates classified as `VALID_RUNTIME_NOT_LOADED` into the trainer model/writer path instead of relying on a narrow known-ID list.
- Trainer/Foe remains below P1: CLI-log-clean plus strict sync pinned is not a private-ROM audit or ingame smoke pass.
- Viridian Forest trainer IDs `531/532` should be covered when the local audit still reports them as valid runtime-not-loaded rows.
- Loaded-mismatch and invalid audit classifications remain separate follow-up lanes.
- No ROM run, output ROM, workspace-side UPR-FVX/CFRU/DPE code change or P1 promotion is part of this workspace sync.

# Roadmap update - Runtime trainer source audit

- UPR-FVX PR #103 is merged and the workspace submodule is pinned to `14c1c8c0c6960f1b4a0cf0246a1117628ca1f3cc`.
- The pinned runtime-source diagnostics now include an opt-in global Trainer Runtime Source Audit with modes `all`, `unloaded-valid-parties`, `loaded-mismatch` and `invalid`.
- The audit classifies deduped script-referenced trainer IDs and highlights valid raw runtime parties that are not loaded into the normal trainer model.
- This is an audit-only roadmap step: no automatic sync/write behavior, no SaveTrainers expansion, no ROM run and no P1 promotion.
- Next Foe Trainer work for additional vanilla-looking battles must start from sanitized local audit evidence, then a separate focused UPR-FVX fix PR if a valid runtime row should be synced.

# Roadmap update - Diagnose 179B

- UPR-FVX PR #49 is merged and the workspace submodule is pinned to `bc46fdc49741643d8f09dd302b67b5b2d35d24c5`.
- The pinned `TrainerSpecialRulesTest` provides Non-ROM `:random:test` coverage for League Unique, Rival Carries Starter and Trainers Evolve Their Pokemon + Level Modifier.
- Roadmap status for `FVX-FOE-010`, `FVX-FOE-012` and `FVX-FOE-014` is now `tested-non-rom`; this remains below P1-supported because no ROM-/Reload-Evidenz, ROM-Smoke, Trainer Names/Class Names/Text work, Battle Style work, output-ROM or Randomizer run was executed.
- Keep `FVX-FOE-011` Battle Style and `FVX-FOE-013` Trainer Names/Class Names/Text as separate out-of-scope lanes.

# Roadmap update - Diagnose 178B

- UPR-FVX PR #48 is merged and the workspace submodule is pinned to `32ab7d969e5439d38e5781670c9a68e0ea418d0a`.
- The pinned `TrainerAdditionalPokemonTest` provides Non-ROM `:random:test` coverage for Additional Pokemon on Boss, Important and Regular Trainers.
- Roadmap status for `FVX-FOE-005`, `FVX-FOE-006` and `FVX-FOE-007` is now `tested-non-rom`; this remains below P1-supported because no ROM-/Reload-Evidenz, ROM-Smoke, Trainer Names/Class Names/Text work, output-ROM or Randomizer run was executed.
- A later P1 promotion needs a separately authorized ROM-/Reload-Smoke or equivalent writer/reload evidence.

# Roadmap update - Diagnose 177B

- UPR-FVX PR #47 is merged and the workspace submodule is pinned to `ea5269706eb7d04eb0b305f88e8fa20bfb21f92a`.
- The pinned `TrainerTypeDiversityGuardTest` provides Non-ROM `:random:test` coverage for Trainer Type Diversity / Type Themes null Primary/Secondary Type guard decisions.
- Roadmap status for `FVX-FOE-009` is now `tested-non-rom`; this remains below P1-supported because no ROM-/Reload-Evidenz, ROM-Smoke, Trainer Names/Class Names/Text work, output-ROM or Randomizer run was executed.
- A later P1 promotion needs a separately authorized ROM-/Reload-Smoke or equivalent writer/reload evidence.

# Roadmap update - Diagnose 176B

- UPR-FVX PR #46 is merged and the workspace submodule is pinned to `c86221d758bece06b216b1f4fb23dd8e4a6c8ec0`.
- The pinned `WildCatchLevelDecisionTest` provides Non-ROM `:random:test` coverage for Wild Set Minimum Catch Rate, Catch Em All and Balance Low Level Encounters + Level Modifier decisions.
- Roadmap status for `FVX-WILD-007`, `FVX-WILD-010` and `FVX-WILD-012` is now `tested-non-rom`; this remains below P1-supported because no ROM-/Reload-Evidenz, ROM-Smoke, output-ROM or Randomizer run was executed.
- A later P1 promotion needs a separately authorized ROM-/Reload-Smoke or equivalent writer/reload evidence.

# Roadmap update - Diagnose 175B

- UPR-FVX PR #45 is merged and the workspace submodule is pinned to `1be6f51779906af017f6177f264e41f8c7902d8e`.
- The pinned `Gen3MoveDataWriterTest` provides Non-ROM `:romio:test` writer-decision coverage for MoveData Power, Accuracy, PP and Type bytes.
- The pinned `MoveUpdateDecisionTest` provides Non-ROM `:random:test` apply-decision coverage for `Update Moves to Generation`.
- Roadmap status for `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` and `FVX-MOVE-006` is now `tested-non-rom`; this remains below P1-supported because no ROM-/Reload-Evidenz, ROM-Smoke, output-ROM or Randomizer run was executed.
- Keep `FVX-MOVE-005` Move Names/Text as a separate out-of-scope Text/Menu lane.

# Roadmap update - Diagnose 174B

- UPR-FVX PR #44 is merged and the workspace submodule is pinned to `85b282112322f8991dd11b14cc98d6dd68fd3fd4`.
- The pinned `EvolutionMakeEasierDecisionTest` provides Non-ROM `:romio:test` decision coverage for `FVX-TRAIT-025A`.
- Roadmap status for `025A` is now `tested-non-rom`; this remains below P1-supported because no Writer-/Reload-Evidenz, ROM-Smoke, output-ROM or Randomizer run was executed.
- Keep `FVX-TRAIT-025B` as a separate Gen3 Happiness-byte patch / writer-like scope.
- Keep `FVX-TRAIT-026` helper-only for `024/025`, not a standalone feature promotion.

# Roadmap update - Diagnose 173

- `FVX-TRAIT-025` Make Evolutions Easier is now `make-easier-plan-ready`.
- Split future work into 025A ROM-free Condense-/Level-/Decision harness and 025B Gen3 Happiness-byte patch / writer-like scope.
- Recommended next implementation, if approved, is only 025A as a small Non-ROM UPR-FVX `:romio:test` with synthetic Species/Evolution chains.
- Keep 025B, Writer-/Reload-Evidenz, ROM-Smoke, output-ROM and Randomizer runs separate and unauthorized.
- `FVX-TRAIT-026` remains helper-only for `024/025`, not a standalone feature promotion.

# Roadmap update - Diagnose 172B

- UPR-FVX PR #43 is merged and the workspace submodule is pinned to `3b33412e80d1cb2d97725ad7a7dd01529aa56919`.
- The pinned `EvolutionMethodDecisionTest` provides Non-ROM `:romio:test` decision coverage for `FVX-TRAIT-024` and `FVX-TRAIT-027`.
- Roadmap status for those slices is now `tested-non-rom`; this remains below P1-supported because no Writer-/Reload-Evidenz, ROM-Smoke, output-ROM or Randomizer run was executed.
- Keep `FVX-TRAIT-025` split into condense-level logic and Gen3 happiness-byte patch risk; keep `FVX-TRAIT-026` helper-only.

# Roadmap update - Diagnose 171

- `FVX-TRAIT-024` and `FVX-TRAIT-027` are now `decision-review-ready`.
- Recommended next implementation, if approved, is a small ROM-free UPR-FVX `:romio:test` decision harness for Change Impossible Evolutions and Remove Time-Based Evolutions.
- Keep the harness at mapping-decision level: synthetic `Species` / `Evolution` objects, no ROM file, no Gen3 writer, no reload, no Randomizer run and no output-ROM.
- `FVX-TRAIT-025` remains a separate split plan and `FVX-TRAIT-026` remains a helper flag for `024/025`.

# Roadmap update - Diagnose 170

- Evolution methods/improvement slices `FVX-TRAIT-024` through `FVX-TRAIT-027` now have a `methods-plan-ready` path.
- `FVX-TRAIT-024` and `FVX-TRAIT-027` should be reviewed as method-mapping decision scopes before any writer/reload work.
- `FVX-TRAIT-025` should be split into ROM-free condense-level evidence and separate Gen3 happiness-byte patch risk.
- `FVX-TRAIT-026` stays a helper flag for `024/025`, not a standalone feature promotion.
- No ROM-Smoke, Randomizer run, build, code change or submodule change is recommended by this planning block.

# Roadmap update - Diagnose 169B

- UPR-FVX PR #42 is merged and the workspace submodule is pinned to `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- The pinned `EvolutionFilterOptionsTest` provides Non-ROM `:random:test` coverage for `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023`.
- Roadmap status for those slices is now `tested-non-rom`; this remains below P1-supported because no ROM-Smoke, Gen3 writer, reload or output-ROM scope was executed.
- Keep `FVX-TRAIT-024` through `FVX-TRAIT-027` separate as `methods-plan-ready` Evolution-improvement/method work.

# Roadmap update - Diagnose 168

- Evolution filter slices `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023` now have a concrete `harness-plan-ready` path.
- Recommended next implementation, if approved, is a small UPR-FVX `:random:test` Non-ROM harness using synthetic `Species` / `Evolution` data and a `RomHandler` proxy/fake.
- No ROM-Smoke, Gen3 writer test, Randomizer run or production-code seam is recommended by this planning block.
- Keep `FVX-TRAIT-024` through `FVX-TRAIT-027` separate as Evolution-improvement/method work.

# Roadmap update - Diagnose 167

- Evolution suboptions `FVX-TRAIT-016` through `FVX-TRAIT-027` are consolidated.
- `FVX-TRAIT-016` remains P1-supported; `FVX-TRAIT-018` and `FVX-TRAIT-019` are `diagnosis-ready` and no longer active 070 blockers.
- `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023` stay plan-only Species-Carrier filter work; `FVX-TRAIT-024` through `FVX-TRAIT-027` stay separate not-started Evolution-improvement/method work.
- Next minimal Evolution path is a read-only Non-ROM harness plan for the remaining Species-Carrier filters, not a fixbranch or ROM-Smoke.

# Roadmap update - Diagnose 166

- Evolution Same Typing (`FVX-TRAIT-019`) is reclassified read-only as `diagnosis-ready` for the narrow `FVX-TRAIT-016` Evolution-Species-Carrier scope.
- The historical 070 NullPointerException blocker is superseded by Diagnose 079/080 evidence: `EvolutionRandomizer` guards null/unsupported Primary Type candidates before `hasSharedType(...)`, and Same Typing has Save/Log/Output/Reload true with `writeReloadEvolutionMismatches=0`.
- No immediate UPR-FVX fix block is recommended; if additional confidence is requested, plan read-only code review or a small Non-ROM harness before any new ROM-facing smoke.
- Keep Evolution-Methoden-Writer and other Evolution suboptions separate.

# Roadmap update - Diagnose 165

- Evolution Similar Strength (`FVX-TRAIT-018`) is reclassified read-only as `diagnosis-ready` for the narrow `FVX-TRAIT-016` Evolution-Species-Carrier scope.
- The historical 070 mismatch blocker is superseded by Diagnose 081/082 normalized reload evidence: Save/Log/Output/Reload true and `normalizedWriteReloadEvolutionMismatches=0`.
- No immediate UPR-FVX fix block is recommended; if additional confidence is requested, plan read-only code review or a small Non-ROM harness before any new ROM-facing smoke.
- Keep Evolution-Methoden-Writer and other Evolution suboptions separate.

# Roadmap update - Diagnose 164

- In-Game Trades are closed for the tested CFRU/DPE Gen9-BPRE scope as `guarded/preserve-only, not supported`.
- The roadmap should not schedule further In-Game Trade work unless new evidence meets the documented reopen criteria.
- Guard evidence remains pinned through UPR-FVX PR #39, PR #40 and PR #41, but no valid active rows are proven and Species-Write-Smoke remains unauthorized.
- Next roadmap work should move to a different Randomizer feature lane.

# Roadmap update - Diagnose 163B

- UPR-FVX PR #41 is merged and the workspace submodule is pinned to `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- The In-Game Trades ROM-free Gen3 writer-preserve test is now present in the pinned UPR-FVX submodule and covers unsafe/null-request row skip-before-byte-write behavior with synthetic `InGameTrade` rows and bytes.
- Roadmap classification remains `blocked-pending-evidence`; valid active rows are still unproven and Species-Write-Smoke remains unauthorized.
- Next roadmap step is either a guarded/preserve-only closure decision or additional read-only active-row evidence.

# Roadmap update - Diagnose 162

- In-Game Trades now have a ready ROM-free Gen3 writer-preserve test plan after the non-ROM `TradeRandomizer` harness follow-up.
- Recommended next implementation, only if explicitly scoped, is a UPR-FVX test-only branch for `Gen3RomHandler` unsafe-row preserve behavior using a narrow row-write decision seam and synthetic bytes.
- Roadmap classification remains `blocked-pending-evidence`; valid active rows are still unproven and Species-Write-Smoke remains unauthorized.
- If the writer test requires ROM fixtures, reflection-heavy private state setup or broad handler refactor, leave the scope blocked/preserve-only.

# Roadmap update - Diagnose 161B

- UPR-FVX PR #40 is merged and the workspace submodule is pinned to `1eaee2873cd69682335223f817b124bf36d004f2`.
- The In-Game Trades non-ROM `TradeRandomizer` harness is now present in the pinned UPR-FVX submodule and covers null-request, placeholder/unsafe Species, all-skipped no-writeback, `changesMade=false`, and skip-status behavior.
- Roadmap classification remains `blocked-pending-evidence`; valid active rows are still unproven and Species-Write-Smoke remains unauthorized.
- Next roadmap step is either a read-only writer-preserve-test plan or leaving In-Game Trades guarded/preserve-only until further evidence is explicitly requested.

# Roadmap update - Diagnose 160

- In-Game Trades have a ready non-ROM harness plan after the guard code review.
- Recommended next implementation, only if explicitly scoped, is a UPR-FVX test-only branch for `TradeRandomizer` with synthetic unsafe `InGameTrade` rows and a fake/test `RomHandler`.
- Roadmap classification remains `blocked-pending-evidence`; valid active rows are still unproven and Species-Write-Smoke remains unauthorized.
- Writer preserve testing is a secondary target only if it stays ROM-free and small.

# Roadmap update - Diagnose 159

- In-Game Trades guard code review is complete as `review-pass-with-risks`.
- The UPR-FVX guard satisfies the narrow Preserve/Skip policy for unsafe rows: skip before mutation and preserve/skip before Gen3 byte writes.
- Roadmap classification remains `blocked-pending-evidence`; valid active rows are still unproven and Species-Write-Smoke remains unauthorized.
- Next roadmap step is a small non-ROM harness if implementation evidence is needed, or further read-only active-row/locator evidence.

# Roadmap update - Diagnose 158B

- UPR-FVX PR #39 is merged and the workspace submodule is pinned to `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- The In-Game Trades defensive null/invalid Species guard is now implemented upstream in the fork: `TradeRandomizer.java` skips unsafe rows before mutation and `Gen3RomHandler.java` preserves/skips unsafe rows before byte writes.
- Roadmap classification remains `blocked-pending-evidence`; the guard reduces unsafe-write risk but does not prove valid active rows or authorize Species-Write-Smoke.
- Next roadmap step is targeted read-only/code-review or an explicitly allowed non-ROM guard test/harness.

# Roadmap update - Diagnose 157

- In-Game Trades defensive null-request guard is planned read-only, not implemented.
- Current classification remains `blocked-pending-evidence`.
- A future `compat/...` branch may add a narrow skip/preserve guard for null requested Species and invalid/placeholder Species rows, with explicit status reporting and no Species-Write-Smoke, text, IV or Trade Held Item writes.

# Roadmap update - Diagnose 156

- In-Game Trades move from active-row candidate blocker to explicit Preserve/Skip policy.
- Current classification: `blocked-pending-evidence`; no trade row writes, Species-Write-Smoke, Trade Held Item, IV or Nickname/OT randomization are allowed.
- Future reopening requires valid active-row evidence, corrected locator/row-shape evidence, explicit unsupported/dummy proof, or a separate defensive null-requested-species skip/guard plan.

# Roadmap update - Diagnose 155

- Keep the In-Game Trades blocker lane active after active-row candidate diagnosis.
- Current classification: blocked, not candidate-confirmed and not yet unsupported-dummy.
- Required next evidence: explicit valid active rows, corrected locator/row-shape evidence, content-based dummy skip policy, defensive null-requested-species plan, or final unsupported/dummy decision.

# Roadmap update - Diagnose 154

- Preserve the In-Game Trades blocker lane before any write smoke.
- Required next evidence: valid active trade rows or explicit unsupported/dummy-row classification.
- Text/Menu work remains out of scope.

# Roadmap update - Diagnose 153

- Insert an In-Game Trades locator/table-model diagnostic before any species-only smoke.
- Possible follow-up outcomes: ROM-entry/locator correction plan, dummy-row skip plan, defensive null-request plan, or unsupported-scope decision.
- Text fields, Trade Held Items and IV extras remain later subscopes.

# Roadmap update - Diagnose 152

- Pause In-Game Trade write smokes.
- Add a narrow read-only locator/table-model blocker plan before testing Given/Requested species writes.
- Keep Trade Held Items, Nickname/OT text and IV extras as later subscopes after valid active trade rows are confirmed.

# Roadmap update - Diagnose 151

- Add In-Game Trades as the recommended next Randomizer scope after Special Wild triggerability analysis.
- Recommended sequence: read-only trade candidate diagnostic, species-only smoke, held-item-only smoke, fixed-length nickname/OT text smoke, IV/extras smoke.
- Keep Text/Menu repointing, Static/Gift, Starter, Trainer, Wild and Held Item scopes separate.

# 2026-05-15 - Special Wild roadmap update

- Diagnose 150 closes the immediate Special Wild triggerability question for the current tracked state.
- No active Special Wild writer scope is recommended now.
- Roadmap can move to the next major Randomizer feature unless explicit product goals require Day/Night, Swarm, Raid, DexNav or Wild Double support.

# 2026-05-15 - Roadmap reconciliation

- Diagnose 149 reconciles completed Randomizer scopes against remaining major gaps.
- Held Items are closed; Standard Wild P0 should not be retested as the next major scope.
- Next recommended roadmap item is CFRU Day/Night and special Wild Encounter systems read-only planning/diagnostics.

# 2026-05-15 - Wild Encounters roadmap start

- Wild Encounters/Wild Pokemon Randomization becomes the next major Randomizer feature scope in Diagnose 148.
- The first step is read-only candidate diagnostics for Gen3 encounter tables and CFRU/DPE Gen9 SpeciesSet mapping.
- No Wild Encounter feature is promoted until diagnostics and later write/reload smokes pass.

# 2026-05-15 - Held Items roadmap closure

- Starter Held Items + Ban Bad passed in Diagnose 147.
- Held Items coverage now includes Wild, Wild Ban Bad, Trainer Boss/Important/Regular, Regular Trainer filters, Starter no-Ban-Bad and Starter Ban Bad in separate tested scopes.
- Next roadmap step is the next major Randomizer feature scope.

# 2026-05-15 - Held Items roadmap starter update

- Starter Held Items without Ban Bad passed in Diagnose 146.
- Held Items coverage now includes Wild, Wild Ban Bad, Trainer Boss/Important/Regular, Regular Trainer filters and Starter no-Ban-Bad in separate tested scopes.
- Next recommended Held Items step is Starter Ban Bad smoke.

# 2026-05-15 - Held Items roadmap filtered update

- Regular Trainer Held Item combined filters passed in Diagnose 145.
- Trainer Held Items are covered for Boss/Important/Regular no-filter scopes and Regular combined-filter scope.
- Next recommended major scope is Starter Held Items unless Boss/Important filter combinations are required.

# 2026-05-15 - Held Items roadmap filter update

- Trainer Held Item filter coverage is planned in Diagnose 144 after Boss/Important/Regular no-filter success.
- Recommended next step is a Regular-only combined filter smoke, with split filter smokes only if needed.
- Starter Held Items remain the next major Held Items scope after the filter decision.

# 2026-05-15 - Held Items roadmap update

- Regular Trainer Held Items are now GUI-compatible in the tested CFRU/DPE Gen9-BPRE no-filter scope after Diagnose 143.
- Boss, Important and Regular Trainer Held Items are covered separately without Consumable/Sensible/Highest-Level filters.
- Trainer pool filters and Starter Held Items remain follow-up scopes.

# 2026-05-15 - Held Items roadmap update

- Important Trainer Held Items are now GUI-compatible in the tested CFRU/DPE Gen9-BPRE scope after Diagnose 142.
- Boss Trainer Held Items remain covered separately; Regular Trainer Held Items, Trainer pool filters and Starter Held Items remain follow-up scopes.
- Wild/Encounter Held Items remain covered with and without Ban Bad.

# 2026-05-15 - Held Items roadmap update

- Boss Trainer Held Items are now GUI-compatible in the tested CFRU/DPE Gen9-BPRE scope after Diagnose 141.
- Important Trainer Held Items, Regular Trainer Held Items, Trainer pool filters and Starter Held Items remain separate follow-up scopes.
- Wild/Encounter Held Items remain covered with and without Ban Bad.

# 2026-05-15 - Held Items roadmap update

- Wild/Encounter Held Items + Ban Bad are now GUI-compatible in the tested CFRU/DPE Gen9-BPRE scope after Diagnose 140.
- Wild/Encounter Held Items are covered both without Ban Bad and with Ban Bad.
- Trainer Held Items and Starter Held Items remain separate follow-up scopes.

# 2026-05-15 - Held Items roadmap update

- Wild/Encounter Held Items without Ban Bad are now GUI-compatible in the tested CFRU/DPE Gen9-BPRE scope after Diagnose 139.
- Ban Bad, Trainer Held Items and Starter Held Items remain separate follow-up scopes.
- Field Items, Pickup and Shops remain closed/separate and unchanged by this block.

# 2026-05-15 - Held Items roadmap update

- Held Items read-only candidate diagnostics are complete in Diagnose 138.
- Follow-up order remains split: Wild/Encounter first, Trainer second, Starter third; Ban Bad remains separate.
- Fallback/placeholder held-item inventory is a tracked smoke-safety risk.

# 2026-05-15 - Held Items roadmap update

- Held Items becomes the next Item-related package after Field Items, Pickup and the closed tested Shop Items scope.
- The package is planned as separate Wild/Encounter, Trainer and optional Starter subscopes.
- First follow-up is read-only candidate diagnostics, not a write smoke.

# 2026-05-15 - Shop Items roadmap update

- Shop Items package is closed for the tested CFRU/DPE Gen9-BPRE GUI-compatible scope after Diagnose 136.
- FVX-ITEM-009 now covers Balance Shop Prices, Cheap Rare Candies, and their tested combination.
- Remaining Shop-related combinations, if desired, are optional regression follow-ups rather than blockers for moving to Held Items.

# 2026-05-15 - Roadmap note: Shop Cheap Rare Candies

- Completed Shop-only FVX-ITEM-009 Cheap Rare Candies reload smoke.
- Promote only the tested Cheap Rare Candies subscope to GUI-compatible alongside Balance Shop Prices.
- Decide next whether Balance Prices + Cheap Rare Candies combination coverage is needed or close the Shop Items scope.

# 2026-05-15 - Roadmap note: Shop Balance Prices

- Completed Shop-only FVX-ITEM-009 Balance Shop Prices reload smoke.
- Promote only the tested Balance Shop Prices subscope to GUI-compatible.
- Keep Cheap Rare Candies as the next separate Shop-only FVX-ITEM-009 smoke.

# 2026-05-15 - Roadmap note: Shop Prices / Cheap Rare Candies

- Planned FVX-ITEM-009 as the next separate Shop-only subscope after individual Shop Guarantee smokes.
- Run Balance Shop Prices before Cheap Rare Candies because price-only writes are narrower than Shop-list growth plus price writes.
- Keep Evolution+X combination and Ban combinations optional separate follow-ups.

# 2026-05-15 - Roadmap note: Shop Guarantee X Items

- Completed Shop-only FVX-ITEM-008 Guarantee X Items reload smoke.
- Promote only the tested Guarantee X Items subscope to GUI-compatible alongside the prior Guarantee Evolution Items subscope.
- Decide next between Evolution+X combination coverage and the separate FVX-ITEM-009 price/Cheap Rare Candy scope plan.

# 2026-05-15 - Roadmap note: Shop Guarantee Evolution Items

- Completed Shop-only FVX-ITEM-008 Guarantee Evolution Items reload smoke.
- Promote only the tested Guarantee Evolution Items subscope to GUI-compatible.
- Keep Guarantee X Items as the next Shop-only FVX-ITEM-008 candidate; keep FVX-ITEM-009 as a later separate price/Cheap Rare Candy scope.

# 2026-05-15 - Shop Guarantee Items Roadmap Update

- Diagnose 130 plant `FVX-ITEM-008 Guarantee Evolution/X Items` als naechsten Shop-only Subscope.
- Erste empfohlene Ausfuehrung: Guarantee Evolution Items Smoke, danach Guarantee X Items Smoke, Kombination nur nach stabilen Einzel-Smokes.
- Keine Hochstufung fuer Ban-Kombinationen, Shop-Preise, Cheap Rare Candies, Field Items, Pickup oder Held Items.

# 2026-05-15 - Shop Item Bans Ban OP Roadmap Update

- Diagnose 129 stuft den Ban-OP-Subscope von `FVX-ITEM-007` hoch: Shop Random mit `banOPShopItems=true` ist im getesteten Shop-only Scope GUI-kompatibel.
- Ban Bad und Ban Regular bleiben aus Diagnose 127/128 belegt; keine Hochstufung fuer Ban-Kombinationen, Guarantee Evolution/X Items, Shop-Preise oder Cheap Rare Candies.
- Naechster minimaler Roadmap-Schritt: Entscheidung Ban-Kombinationen vs. `FVX-ITEM-008`.

# 2026-05-15 - Shop Item Bans Ban Regular Roadmap Update

- Diagnose 128 stuft den Ban-Regular-Subscope von `FVX-ITEM-007` hoch: Shop Random mit `banRegularShopItems=true` ist im getesteten Shop-only Scope GUI-kompatibel.
- Ban Bad bleibt aus Diagnose 127 belegt; keine Hochstufung fuer OP-Ban, Ban-Kombinationen, Guarantee Evolution/X Items, Shop-Preise oder Cheap Rare Candies.
- Naechster minimaler Roadmap-Schritt: separater Ban-OP-Block.

# 2026-05-15 - Shop Item Bans Roadmap Update

- Diagnose 127 stuft nur den Ban-Bad-Subscope von `FVX-ITEM-007` hoch: Shop Random mit `banBadRandomShopItems=true` ist im getesteten Shop-only Scope GUI-kompatibel.
- Keine Hochstufung fuer Regular-Ban, OP-Ban, Guarantee Evolution/X Items, Shop-Preise oder Cheap Rare Candies.
- Naechster minimaler Roadmap-Schritt: separater Ban-Regular-Block.

# FVX Feature Roadmap Update - 2026-05-15 - Shop Item Bans scope plan

- `FVX-ITEM-007 Shop Item Bans` is now planned as the next Shop-only sub-scope after Shop Random.
- First executable step should be Shop Random + Ban Bad because its pool delta is directly measurable from Diagnose 125 (`536` allowed/no-TM vs `485` non-bad/no-TM).
- Ban Regular and Ban OP should follow as separate smokes only after their banned sets are measured clearly.
- `FVX-ITEM-008..009` remain separate Shop sub-scopes; Field Items, Pickup and Held Items are unchanged.

# FVX Feature Roadmap Update - 2026-05-15 - Shop Items Random reload smoke

- `FVX-ITEM-006 Shop Items Random` is now GUI-compatible in the tested Shop-only CFRU/DPE Gen9-BPRE scope.
- The next roadmap step is a narrow `FVX-ITEM-007 Shop Item Bans` scope plan or smoke split.
- `FVX-ITEM-008..009` remain separate Shop sub-scopes; Field Items, Pickup and Held Items are unchanged.

# FVX Feature Roadmap Update - 2026-05-15 - Shop Items Shuffle reload smoke

- `FVX-ITEM-005 Shop Items Shuffle` is now GUI-compatible in the tested Shop-only CFRU/DPE Gen9-BPRE scope.
- The next roadmap step is a narrow `FVX-ITEM-006 Shop Items Random` Write/Reload-Smoke.
- `FVX-ITEM-007..009` remain separate Shop sub-scopes; Field Items, Pickup and Held Items are unchanged.

# FVX Feature Roadmap Update - 2026-05-15 - Shop Items candidate diagnostics

- Shop Items advance from blocked preflight to a stable read-only candidate diagnostic.
- The next roadmap step is a narrow `FVX-ITEM-005 Shop Items Shuffle` Write/Reload-Smoke.
- `FVX-ITEM-005..009` remain `Write modelliert` until Shop-only smokes pass; Diagnose 123 does not upgrade GUI compatibility.

# FVX Feature Roadmap Update - 2026-05-15 - Shop Items diagnostics preflight

- Shop Items remain the active next Item package, but Diagnose 122 blocks before a candidate scan because no explicitly approved local CFRU/DPE Gen9-BPRE candidate source was provided.
- The next roadmap step is a read-only Shop candidate diagnostic with an approved source, not a Shop Shuffle smoke.
- `FVX-ITEM-005..009` stay `Write modelliert`; Field Items, Pickup and Held Items stay separate and unchanged.

# FVX Feature Roadmap Update - 2026-05-15 - Shop Items scope diagnostics plan

- Shop Items are now the next planned Item package after completed Field Items and Pickup scopes.
- `FVX-ITEM-005..009` are kept together as a Shop package but split by diagnostic order: Shuffle, Random, Bans, Guarantee Evolution/X Items, then Balance Prices/Cheap Rare Candies.
- The package remains `Write modelliert`; no Shop writer compatibility is claimed before read-only candidate diagnostics and Shop-only reload smokes.
- Field Items, Pickup and Held Items are explicitly not promoted by the Shop plan.

# FVX Feature Roadmap Update - 2026-05-15 - Pickup complete, Shops next

- Pickup Random is reload-stable and GUI-compatible with and without Ban Bad in the tested Pickup-only scope.
- Field Items and Pickup are now split from the remaining Item writer work.
- Next recommended Item writer scope: Shops-only read-only diagnostics plan.
- Keep Shop work separate from Field Items, Pickup and Held Items.

# FVX Feature Roadmap Update - 2026-05-15 - Pickup Ban Bad next

- Pickup Random without Ban Bad is reload-stable after UPR-FVX PR #38 and Diagnose 118.
- Pickup Ban Bad is the next narrow Item sub-scope; it should be tested directly before Shops or Held Items.
- Recommended branch: `test/upr-fvx-cfru-dpe-pickup-items-random-ban-bad-reload-smoke`.
- Preserve separation from Field Items, Shops, Encounter Held Items, Trainer Held Items and Starter Held Items.

# Roadmap Note - 2026-05-15 - Pickup reload locator fix

- Diagnose 118 closes the Pickup Random reload-locator blocker for `banBadRandomPickupItems=false`.
- UPR-FVX PR #38 keeps the fix scoped to Pickup table localization and leaves pool policy unchanged.
- Next Pickup sub-scope is Ban Bad planning/smoke; Shops and Held Items remain separate.

# Roadmap Note - 2026-05-15 - Pickup reload locator blocker

- Diagnose 117 keeps Pickup as the active separated Item-writer track after Field Items.
- Next recommended implementation branch is `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- The intended fix stays below Pickup pool policy: make the Pickup table locator reload-stable after `PickupItemsMod.RANDOM` changes item IDs.
- Pickup Ban Bad, Shops and Held Items remain blocked/separate until Pickup Random without Ban Bad reloads stably.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random Ban Bad reload smoke

- Diagnose 112 confirms the Field-Items Random Ban-Bad carrier: `FVX-ITEM-002` with `banBadRandomFieldItems=true` has a successful CFRU/DPE Field-Items-only reload smoke.
- `FVX-ITEM-004` can be treated as tested for `FieldItemsMod.RANDOM`, but not fully GUI-compatible until Random Even + Ban Bad passes separately.
- Keep Shops, Pickup and Held Items separate from Field Items Ban Bad.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Ban Bad scope plan

- Diagnose 111 plans `FVX-ITEM-004 Field Items Ban Bad Items` as a Field-Items Non-TM pool-filter validation.
- First smoke should use `FVX-ITEM-002 Field Items Random` with `banBadRandomFieldItems=true`; Random Even + Ban Bad should follow separately.
- Keep Shops, Pickup and Held Items separate from Field Items Ban Bad.
- Next step is `test/upr-fvx-cfru-dpe-field-items-random-ban-bad-reload-smoke`.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random Even reload smoke

- Diagnose 110 confirms `FVX-ITEM-003 Field Items Random even distribution` with a successful CFRU/DPE Field-Items-only reload smoke.
- `FVX-ITEM-003` can move to `GUI-kompatibel` only for the narrow Field-Items Random-Even scope with `banBadRandomFieldItems=false`.
- Keep `FVX-ITEM-004` Ban Bad Items as a separate follow-up block.
- Next step is `analysis/upr-fvx-cfru-dpe-field-items-ban-bad-scope-plan`; do not fold Shops or Pickup into that work.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items API TM-slot reload smoke

- Diagnose 109 confirms the UPR-FVX PR #37 Field-Items API TM-slot fix with a successful `FVX-ITEM-002 Field Items Random` reload smoke.
- `FVX-ITEM-002` can move to `GUI-kompatibel` only for the narrow Field-Items Random scope with `banBadRandomFieldItems=false`.
- Keep `FVX-ITEM-003` Random Even and `FVX-ITEM-004` Ban Bad Items as separate follow-up blocks.
- Next step is `test/upr-fvx-cfru-dpe-field-items-random-even-reload-smoke`; do not fold Shops or Pickup into that work.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items API TM-slot fix prepared

- UPR-FVX PR #37 prepares the narrow `FVX-ITEM-002` API TM-slot scope fix.
- The fix stays in Gen3RomHandler Field-Items get/set and exposes CFRU/DPE Field-TM slots without making TMs globally allowed.
- Next step is a separate sanitized reload smoke before any `FVX-ITEM-002` GUI-compatible upgrade.
- Keep `FVX-ITEM-003` Random Even and `FVX-ITEM-004` Ban Bad Items separate.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items API TM-slot scope plan

- Diagnose 107 explains the post-PR-36 `FVX-ITEM-002` blocker: raw diagnostics find `28` TM Field-Item slots, but `getFieldItems()` exposes none because the API filters on `Item::isAllowed`.
- Next fix should stay in the CFRU/DPE Field-Items API TM-slot scope and must not make TMs globally allowed.
- Keep `FVX-ITEM-002` below GUI-compatible until a narrow API-scope fix and reload smoke pass.
- Keep `FVX-ITEM-003` Random Even and `FVX-ITEM-004` Ban Bad Items separate.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random API TM-slot blocker

- Diagnose 106 shows UPR-FVX PR #36 removes the original Unique-TM-Filler pool deficit for `FVX-ITEM-002`.
- The remaining blocker is an API TM-slot scope mismatch: raw Field-Item diagnostics found `tmFieldItemSlots=28`, but `ItemRandomizer.randomizeTMFieldItems(...)` receives `0` TM slots through `getFieldItems()`.
- Keep `FVX-ITEM-002` below GUI-compatible until the API TM-slot scope is understood and a later smoke passes.
- Do not proceed to `FVX-ITEM-003` or `FVX-ITEM-004` before `FVX-ITEM-002` reloads successfully.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random TM-pool fix prepared

- UPR-FVX PR #36 prepares the narrow `FVX-ITEM-002 Field Items Random` TM-pool fix.
- The fix is limited to the TM Field Items randomization pool and does not expand Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even or Ban Bad Items.
- `FVX-ITEM-002` should only be upgraded after a separate sanitized reload smoke confirms `randomTmPoolDeficit=0`, `fieldItemReloadMismatches=0`, and `requiredFieldTMMissingAfter=0`.
- Do not proceed to `FVX-ITEM-003` or `FVX-ITEM-004` before this `FVX-ITEM-002` reload smoke passes.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random TM-pool blocker planned

- Diagnose 104 narrows `FVX-ITEM-002 Field Items Random` to a TM-pool / Required-TM algorithm blocker.
- Next fix should stay inside Field Items Random TM-pool handling and avoid Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even and Ban Bad Items.
- Do not proceed to `FVX-ITEM-003` or `FVX-ITEM-004` until `FVX-ITEM-002` has a successful reload smoke.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random blocked

- Field Items Random has a blocked smoke in Diagnose 103: candidate loaded, but save fails with `RandomizationException` before output/reload.
- Keep `FVX-ITEM-002` as `Write modelliert` until the Random TM-pool blocker is planned and fixed.
- Do not proceed to Random Even or Ban Bad Items until the Random carrier is stable.
- Do not fold Shops or Pickup into the Field Items Random blocker work.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Shuffle complete

- Field Items Shuffle has a successful allowed-slot Write-/Reload-Smoke in Diagnose 102.
- `FVX-ITEM-001` can be treated as `GUI-kompatibel` for the narrow Shuffle scope.
- Continue Field Items in separate slices: Random first, Random Even second, Ban Bad Items third.
- Do not fold Shops or Pickup into the Field Items Random follow-up.

# FVX Feature Roadmap Update - 2026-05-14 - Field Items allowed-slot guard

- Field Items remain the first active Item-writer track after Palette.
- Diagnose 101 records that the existing Gen3 Field-Items writer already guards writes to allowed slots.
- No UPR-FVX code change is planned until a Write-/Reload-Smoke proves a concrete mismatch.
- Next minimal validation block: `test/upr-fvx-cfru-dpe-field-items-allowed-slot-reload-smoke` for `FVX-ITEM-001 Field Items Shuffle` only.
- Shops and Pickup stay separate and must not be folded into the first Field-Items smoke.

# FVX Feature Roadmap

Diese Datei ist die feature-orientierte Roadmap fuer Universal Pokemon Randomizer FVX. Sie verdichtet `01_docs/randomizer/fvx-feature-coverage.md` auf planbare Arbeitspakete.

Die detaillierte Status- und Feature-ID-Matrix bleibt in:

```text
01_docs/randomizer/fvx-feature-coverage.md
```

## Gesamtstand aus Feature-Matrix

| Status | Anzahl |
|---|---:|
| Nicht begonnen | 36 |
| Plan erstellt | 28 |
| Read modelliert | 0 |
| Write modelliert | 13 |
| Getestet | 13 |
| GUI-kompatibel | 40 |
| In Arbeit | 0 |
| **Gesamt** | **130** |

## Feature-Pakete

| Paket | Feature-Zeilen | Leitstatus | Ziel |
|---|---:|---|---|
| General Options | 4 | Gemischt | `FVX-GEN-001/002` sind im Starter-Carrier-Smoke getestet; Race Mode und Intro-Mon separat pruefen |
| Pokemon Traits | 28 | Gemischt | Base Stats, Types, Abilities, Evolutions, EXP Curves und Suboptionen systematisch absichern; Evolution-Scope ist konsolidiert: `016` P1-supported, `018/019` diagnosis-ready, `017/020-023` tested-non-rom, `024-027` methods-plan-ready |
| Starters, Statics & Trades | 15 | Gemischt | Starter-Filter sind im Starter-Species-Writer-Smoke getestet; Starter-Held-Items, Trades und Level-Subpfade ergaenzen |
| Moves & Movesets | 11 | Gemischt | Learnset-/Moveset-GUI halten; MoveData `Update Moves`, Power/Accuracy/PP und Move Types haben zusaetzliche Non-ROM Writer-/Updater-Testabdeckung; Move Names ist als Name-only Smoke planbar, aber Diagnosen 089/090 sind mangels lokalem 992-Move-Kandidaten mit `991:PsychicNoise` blockiert; Move Descriptions / Text/Menu-Repointing bleibt getrennt |
| Foe Pokemon | 14 | Gemischt | Trainer-Species/-Movesets/-Held-Items halten; Trainer Similar Strength halten; `FVX-FOE-012` Rival Carries Starter ist nach PR #117 targeted-smoke-confirmed fuer Player Charmander -> Rival Squirtle, aber ohne P1-Promotion; `FVX-FOE-005/006/007` sind nach 178B `tested-non-rom`; `FVX-FOE-009` ist nach 177B `tested-non-rom`; `FVX-FOE-010/014` sind nach 179B `tested-non-rom`; ROM-/Reload-/Full-Playthrough-Evidenz bleibt separat |
| Wild Pokemon | 12 | Gemischt | Standard/Fallback-Wild halten; Similar Strength und Type Restrictions sind nach Diagnose 075 im `FVX-WILD-001` Carrier wieder stabil |
| TM/HMs & Tutors | 15 | Gemischt | TM/Tutor-Tabellen halten; Preserve-/Filter-/Follow-Evolution-Suboptionen testen |
| Items | 10 | Write modelliert | Field Items, Shops und Pickup als getrennte Writer implementieren/testen |
| Types | 3 | PASS_TARGETED_BATTLE_SMOKE_WITH_CAVEATS | Evidence 211 bestaetigt targeted Type-Effectiveness-Battle-Smoke ohne Battle-Crash; keine vollstaendige Type-Matchup-Matrix, kein Full-Playthrough und keine P1-Promotion |
| Graphics | 6 | Gemischt | PR #123/#124 plus Evidence 209 bestaetigen targeted Graphics/Palettes visual/audit smoke fuer sampled Normal-Paletten; Shiny bleibt caveated (`shinyChangedCount=0`), kein Full-Playthrough und keine P1-Promotion; Custom Player Graphics separat modellieren |
| Misc Tweaks | 12 | PASS_TARGETED_BEHAVIOR_SMOKE_WITH_CAVEATS | Evidence 210 bestaetigt targeted Misc-Tweaks-Behavior-Smoke; Fast Egg Hatching nur crash-free/output-load, Ban Lucky Egg likely pass, Reusable TMs/Forgettable HMs CFRU-provided und nicht doppelt im UPR-FVX stable profile |
| GUI-Suboptions-Regressionsmatrix | n/a | Erledigt | vorhandene Diagnose 060 als technische Regressionssicht nutzen |
| Regression-Smoke-Plan | n/a | In Arbeit | konkrete Smoke-/Regression-Laeufe aus Feature-IDs ableiten und sanitisiert dokumentieren |

## Priorisierte Roadmap ab jetzt

### P0 - Coverage und Smoke-Plan

| Reihenfolge | Branch | Ziel | Status |
|---|---|---|---|
| P0.1 | `docs/fvx-feature-coverage-matrix` | FVX-GUI-Features als Requirements-/Coverage-Matrix dokumentieren | In Arbeit |
| P0.2 | `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan` | Smoke-/Regression-Plan fuer priorisierte GUI-Suboptionen erstellen, ohne neue Randomizer-Laeufe im Planblock | Erledigt |
| P0.3 | `test/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke` | Global-Species-Pool-Smoke fuer `FVX-GEN-001/002` im Starter-Carrier-Scope sanitisiert dokumentieren | Erledigt |
| P0.4 | `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke` | Starter-Suboptions-Smoke fuer `FVX-SST-003/004/005/006/009` sanitisiert dokumentieren | Erledigt |
| P0.5 | `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke` | Similar-Strength-/Same-Type-/Type-Restrictions-Smoke sanitisiert dokumentieren | Review/Test |

### P1 - Offene Writer mit vorhandenen Modellen

| Reihenfolge | Branch | Paket | Ziel |
|---|---|---|---|
| P1.1 | `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness` + `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes` | Types | erledigt: TypeEffectiveness Random, Balanced, Keep Type Identities, Inverse, Add Immunities und Update Type Effectiveness mit Reload-/Terminator-/Preserve-Kriterien abgesichert |
| P1.2 | `compat/upr-fvx-cfru-dpe-move-data-write-preserve` + `test/upr-fvx-cfru-dpe-move-data-write-preserve-reload-smoke` | Moves & Movesets | erledigt: UPR-FVX PR #33, Workspace PR #124 und Workspace PR #125 sind gemerged; Diagnose 084 bestaetigt `Update Moves` mit `writeReloadMoveDataMismatches=0`, stabilem category/split-Reload und bytegleich erhaltenen Preserve-Bytes |
| P1.2a | `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke` | Moves & Movesets | erledigt: Diagnose 085 bestaetigt `FVX-MOVE-001/002/003` mit `writeReloadMoveDataMismatches=0`, stabilen `+1/+3/+4` Bytes und bytegleich erhaltenen Preserve-Bytes |
| P1.2b | `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke` | Moves & Movesets | blockiert: Diagnose 086 zeigt Save/Log/Output/Reload true und Preserve-Bytes stabil, aber `writeReloadMoveDataMismatches=54` durch Fairy-Type-Byte-Mismatches im MoveData-`+2 type`-Writer |
| P1.2c | `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte` | Moves & Movesets | erledigt und gemerged: UPR-FVX PR #34, Workspace PR #129 und Diagnose 087 bestaetigen `FVX-MOVE-004` mit `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0` und bytegleich erhaltenen Preserve-Bytes |
| P1.2d | `analysis/upr-fvx-cfru-dpe-move-names-text-menu-scope-plan` | Moves & Movesets | erledigt: Diagnose 088 klassifiziert `FVX-MOVE-005` als getrennten Text/Menu-Scope; Name-only fixed-length Smoke ist realistisch, Move Descriptions / Text/Menu-Repointing bleibt zurueckgestellt |
| P1.2e | `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke` | Moves & Movesets | blockiert: Diagnose 089 fand keinen freigegebenen lokalen CFRU/DPE Gen9-BPRE-Kandidaten mit `moves.total=992` und `991:PsychicNoise`; `FVX-MOVE-005` bleibt `Write modelliert` |
| P1.2f | `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke-retry` | Moves & Movesets | abgeschlossen/blockiert: Workspace PR #133 ist gemerged; Diagnose 090 wiederholte den Candidate-Preflight sanitisiert, `candidateFilesChecked=94`, `candidatePreflightSuccessful=false`; kein fachlicher Name-only Smoke, keine Feature-Hochstufung |
| P1.3 | `analysis/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint-plan` | Graphics | erledigt: Diagnose 091 trennt Safety von echter Palette-Randomization und empfiehlt vor Fix eine read-only Pointer-/Compression-Diagnose |
| P1.3a | `analysis/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics-plan` | Graphics | erledigt: Diagnose 092 plant Normal-/Shiny-Palette-Pointer read-only nach dekomprimierbar, single-owner, shared, missing und invalid zu klassifizieren |
| P1.3b | `test/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics` | Graphics | erledigt: Diagnose 093 klassifiziert Pointer/Compression; `candidateWritablePalettes=385`, davon `385` Normal und `0` Shiny |
| P1.3c | `analysis/upr-fvx-cfru-dpe-palette-single-owner-normal-only-fix-scope-plan` | Graphics | erledigt: Diagnose 094 plant den spaeteren Scope nur fuer Normal-Paletten, single-owner, dekomprimierbar, gueltig, non-shared und non-cross-kind; Shiny/shared/invalid/missing/decode-failed preserve-only |
| P1.3d | `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write` | Graphics | erledigt/abgeloest durch PR #123/#124 Stand: Palette-Output-Writes und Logging-Fallback im aktuellen FVX-Pin enthalten |
| P1.3e | `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke` | Graphics | Evidence 209: targeted visual/audit smoke passed with caveats; sampled Normal-Paletten changed from base and visually changed, aber kein P1, kein Full-Playthrough, Shiny sample unchanged |
| P1.3f | `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint` | Graphics | wartet: breitere Shared-/Shiny-/Repoint-Policy nur mit separater shiny-/species-/forme-fokussierter Evidence planen |
| P1.4 | `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write` | Items | Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern |

### P2 - Suboptionen der bereits GUI-kompatiblen Pakete

| Paket | Ziel |
|---|---|
| Pokemon Traits | Follow Evolutions, Force Dual Types, Ability-Ban-/Allow-Filter, EXP Curves testen; Evolution-Suboptionen nach 170 getrennt halten: `017/020-023` tested-non-rom, `024-027` methods-plan-ready |
| Starters, Statics & Trades | Starter-Held-Items und In-Game-Trades absichern; Starter-Type-/Legendary-/BST-Filter ausserhalb des Starter-Species-Writer-Smokes nur separat hochstufen |
| Foe Pokemon | Battle Style und Trainer Names/Class Names separat absichern; Rival Carries Starter `FVX-FOE-012` nach PR #117 als targeted-smoke-confirmed ohne P1-Promotion fuehren; Additional Pokemon `FVX-FOE-005/006/007` nach 178B, Force Diverse Types / `FVX-FOE-009` nach 177B und Trainer Special Rules `FVX-FOE-010/014` nach 179B als `tested-non-rom` fuehren und P1 nur mit separater ROM-/Reload-Evidenz pruefen |
| Wild Pokemon | Evolution Restrictions, Catch Rate, Catch-em-all und Level-Balance absichern; Wild Similar Strength und Type Restrictions aus 075 im `FVX-WILD-001` Carrier halten |
| TM/HMs & Tutors | Keep Field Moves, No Game-Breaking, Good-Damaging-%, Follow-Evolutions und Full-HM-Kompatibilitaet absichern |

### P3 - Noch nicht begonnene Sonderbereiche

| Paket | Ziel |
|---|---|
| General Options | Limit Pokemon und No Premature Evolutions ausserhalb des Starter-Carrier-Smokes weiter pruefen; No Random Intro Mon und Race Mode separat inventarisieren |
| Misc Tweaks | Evidence 210 halten; nur bei Regression oder fuer Full-Hatch-/Ban-Lucky-Egg-/nicht beobachtete Detailpfade separat nachtesten |
| Custom Player Graphics | getrennt von Pokemon-Palette-Randomization modellieren |
| In-Game Trades Text/Items/IVs | Spezies-, Text-, Item- und IV-Writer getrennt pruefen |

## Roadmap-Regel

- Neue Einzeltests referenzieren mindestens eine `FVX-*` Feature-ID aus der Matrix.
- Die Feature-Matrix ist fuer Vollstaendigkeit und Zaehlregel massgeblich.
- Diese Roadmap ist fuer Reihenfolge und Arbeitsbranch-Zuschnitt massgeblich.
- `roadmap-status.md` bleibt die allgemeine Projekt-Roadmap und sollte nur grobe Statuswechsel aufnehmen.
- Keine ROMs, Saves, Builds, Tool-Binaries, private Pfade oder Secrets in Roadmap-Dateien aufnehmen.

## 2026-05-14 - Palette Follow-up nach Diagnose 096

Diagnose 096 blockiert den `FVX-GFX-001` Normal-only Single-owner Reload-Smoke mangels UPR-FVX-ladbarem `candidateSpeciesTotal=1439` Kandidaten. Der nächste Palette-Schritt ist kein Scope-Ausbau, sondern ein Retry desselben engen Smoke-Scope nach expliziter Kandidatenfreigabe.

Nicht in den Retry aufnehmen: Shiny-Palette-Writes, Shared-Palette-Writes, Graphics/Sprites, TypeChart/TypeEffectiveness, Species-Type-Write, Evolution-Writer, Items, Trainer/Wild, Text/Menu, MoveData oder MoveNames.

## 2026-05-14 - P1-Reihenfolge nach blockiertem Palette-Smoke

Nach Diagnose 096 bleibt Palette konservativ: `FVX-GFX-001` hat einen Guard-Fix, aber keinen erfolgreichen Reload-Smoke; `FVX-GFX-001..004` bleiben `Write modelliert`. Ein Palette-Retry wird erst mit explizit freigegebenem UPR-FVX-ladbarem `candidateSpeciesTotal=1439` Kandidaten sinnvoll.

Der naechste empfohlene P1-Block ist deshalb kein Palette-Scope-Ausbau, sondern `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan` als read-only Planung fuer Field Items, Shops und Pickup.

## 2026-05-14 - Item-P1-Aufteilung nach Diagnose 097

Field Items, Shops und Pickup bleiben im Items-Paket, werden aber nicht als gemeinsamer Fixbranch empfohlen. Reihenfolge: Field Items zuerst, danach Pickup, Shops zuletzt wegen Terminator-/DataRewriter-/Repointing- und Preisrisiken. Gemeinsame Item-Pool-Bans bleiben Querschnitt, aber jeder Writer braucht eigene Reload-Kriterien.

## 2026-05-14 - Field Items diagnostics scope

- Field Items are split into their own first item-writer diagnostic branch: `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`.
- Follow-up should diagnose only Field Items before any fix: visible Itemballs, Hidden Items/Signposts, TM-vs-Non-TM slots, Required Field TMs, progression-sensitive items, bad items, modern item IDs and invalid/unloaded item IDs.
- Shops and Pickup stay separate; no shared fix block is recommended until each writer has its own sanitized diagnostics.

## 2026-05-14 - Field Items diagnostics candidate needed

- Field-Items-only diagnostics from protocol 099 are blocked until an explicitly approved local CFRU/DPE Gen9-BPRE candidate is available.
- No Field-Item fix should start before the aggregated diagnostics from 098 can report visible Itemballs, Hidden Items/Signposts, TM/Non-TM slots, Required Field TMs, bad items, modern item IDs and invalid/unloaded item IDs.
- Shops and Pickup remain separate follow-up tracks.

## 2026-05-14 - Field Items candidate diagnostics

- Field-Items-only diagnostics now have sanitized candidate data: `fieldItemsTotal=339`, visible `168`, hidden `171`, allowed `280`, disallowed `59`, TM slots `28`, Non-TM slots `311`, and `requiredFieldTMMissing=0`.
- The next reviewable scope is a guarded Field-Items write/smoke for allowed slots only; disallowed, progression-sensitive, key/system and script-pattern-unmatched slots stay preserve-only.
- Shops and Pickup remain separate follow-up tracks.

## 2026-05-15 - Field Items completion in tested scope

Diagnosen 102, 109, 110, 112 und 113 schliessen `FVX-ITEM-001..004` fuer Field Items im getesteten engen CFRU/DPE Gen9-BPRE-Scope ab:

- Shuffle, Random und Random Even reloaden stabil.
- Ban Bad ist fuer Random und Random Even bestaetigt.
- Field-Item-Gesamtzahl bleibt `339`, Reload-Mismatches bleiben `0`, Required Field TMs bleiben vollstaendig.
- CFRU/DPE Field-TM-Slots bleiben im API-Scope sichtbar, ohne TMs global allowed zu setzen.

Naechste Item-Reihenfolge:

1. Pickup Items separat read-only planen und diagnostizieren.
2. Shops separat planen, weil Terminatoren, Shoplisten-Laengen, Preise und Repointing ein eigener Scope sind.
3. Held Items bleiben getrennt von Field Items / Shops / Pickup.

## 2026-05-15 - Pickup Items diagnostics scope planned

Pickup folgt nach Field Items als separater Item-Writer-Scope:

- `FVX-ITEM-010` bleibt `Write modelliert`, bis eine Pickup-only Kandidatendiagnose und danach eigene Reload-Smokes vorliegen.
- Der Gen3-Pfad nutzt `PickupTableStartLocator`, `PickupItemCount`, `PickupItem.PROBABILITY_SLOTS=10` und schreibt nur Item-ID-Felder.
- CFRU/DPE-Risiken: falscher Locator, abweichende Common/Rare-Struktur, Probability-Semantik, moderne/fallback/bad Items und TM-Holdability-/Reusable-Policy.
- Reihenfolge: read-only Diagnose, Random ohne Ban Bad, Random mit Ban Bad.
- Shops bleiben wegen Terminator-/Repointing-/Preis-Scope separat.

## 2026-05-15 - Pickup Items candidate diagnostics completed

Pickup read-only diagnostics are complete for the next Item writer slice:

- `FVX-ITEM-010` remains `Write modelliert` until a dedicated Write-/Reload-Smoke passes.
- Diagnose 115 establishes `pickupLocatorSuccessful=true`, `pickupItemsTotal=16`, `pickupExpectedCount=16`, `pickupEntrySize=4`, `pickupProbabilitySlots=10` and `pickupProbabilityModelStable=true`.
- Invalid/unloaded/fallback/placeholder Pickup IDs were not found in the current table.
- Ban Bad remains a separate follow-up because `pickupBadItemPoolCandidates=51` and `pickupBadItemPoolExcluded=51` must be validated through the Pickup poolfilter.
- Reihenfolge: Pickup Random ohne Ban Bad, danach Pickup Random mit Ban Bad.

## 2026-05-15 - Pickup Items Random reload blocker

Pickup Random reached save/log/output but is not reload-stable:

- `FVX-ITEM-010` remains `Write modelliert`.
- Diagnose 116 shows `pickupItemsTotalBefore=16` and `pickupItemsTotalAfter=16`, but fresh reload reports `pickupLocatorSuccessful=false` and `pickupItemsTotalReload=0`.
- The likely narrow issue is the content-based `PickupTableStartLocator` no longer matching after item IDs are randomized.
- Next step: read-only locator-blocker plan before any codefix or Ban-Bad smoke.
