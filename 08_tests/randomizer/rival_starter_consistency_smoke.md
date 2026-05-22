# Rival Starter Consistency Smoke Plan

Status: documentation-only plan. No ROM run by Codex. No builds, code changes, raw logs, private paths, screenshots, saves, emulator states, output ROMs or P1 promotion.

## Scope

This plan defines a small local smoke for Rival starter consistency on the current UPR-FVX CFRU/DPE Gen9 BPRE compatibility line.

The smoke checks that:

- the Oak-Lab Rival receives the expected counter-starter after starter randomization,
- `Rival Carries Starter Through Game` preserves or corrects the Rival starter slot after Foe Pokemon randomization,
- the Route 22 Rival starter matches the Oak-Lab Rival starter for the sampled player starter,
- non-starter Rival Pokemon remain eligible for Foe Pokemon randomization,
- runtime-source TrainerData evidence is sufficient to interpret Rival/Trainer Pokemon observations without committing private artifacts.

This is not an all-starter-choice matrix, a full Rival playthrough, a global trainer sweep or a P1 promotion.

## Existing Evidence

Current documentation already has enough structure for this smoke plan:

| Topic | Existing evidence | What it supports |
|---|---|---|
| Oak-Lab Rival counter-slot | `08_tests/randomizer/192_starter_rival_sync_pass.md` | Oak-Lab first Rival counter-slot mapping and randomized counter-starter behavior for a sampled starter path. |
| Rival Counter-Starter / Rival Carry | `08_tests/randomizer/207_rival_counter_starter_and_combined_visual_smoke.md` | PR #117 corrected Rival starter behavior after Foe Pokemon randomization and kept Rival runtime-source rows participating in the carry/correction path. |
| Oak-Lab plus Route 22 consistency | `08_tests/randomizer/208_combined_trainer_visual_runtime_smoke.md` | Player Charmander -> Oak-Lab Rival Squirtle and Route 22 Rival Squirtle; Route 22 non-starter Pokemon randomized separately. |
| Oak-Lab Rival independence | `08_tests/randomizer/212_gen_limit_special_form_item_smoke.md` | Oak-Lab Rival counter-starter is preserved independently of `Rival Carries Starter Through Game`. |
| Trainer Runtime | `08_tests/randomizer/202_trainer_runtime_source_diagnostics_sync.md`, `203_runtime_source_trainer_randomization_smoke.md`, `204_runtime_source_trainer_randomization_smoke.md` | Runtime-source diagnostics and targeted runtime-source Trainer Pokemon evidence exist; broader loaded-mismatch, invalid and out-of-range rows remain caveated. |
| Trainer Pokemon status | `08_tests/randomizer/fvx_feature_test_status_matrix.tsv`, `01_docs/randomizer/fvx-feature-decision-matrix.md` | `FVX-FOE-001` and `FVX-FOE-012` are caveated targeted smoke/evidence areas, not full support claims. |

Conclusion: the existing log/evidence structure is sufficient for a focused Rival starter consistency smoke, provided the result is recorded only as sanitized observations and does not claim full coverage.

## Tested Settings

Use a local private-ROM run only outside Codex. Keep generated settings and outputs in ignored local directories.

Minimal intended settings:

| Setting area | Required state | Reason |
|---|---|---|
| Starter Pokemon | Random completely or equivalent randomized starter mode | Needed to verify randomized counter-starter behavior instead of vanilla-only behavior. |
| Foe Pokemon / Trainer Pokemon | Randomized | Needed because the regression involved Foe Pokemon randomization interacting with Rival starter slots. |
| Rival Carries Starter Through Game | Enabled | Main feature under smoke for later Rival starter consistency. |
| Trainer Class Sprite Sync | Enabled only if Trainer Class Names are randomized | Keeps class label / classId / trainerPic consistency from contaminating visual interpretation. |
| Randomize Trainer Names | Optional | Personal-name-only; not needed for starter consistency. |
| Randomize Trainer Class Names | Optional; if enabled, also enable Trainer Class Sprite Sync | Avoids legacy textlabel-only mismatch. |
| Random Intro Mon | Optional | Can be left on when using the current compat pin; not part of Rival starter PASS/FAIL. |
| Special Wild / Day-Night / Swarms | Off | Keeps unrelated runtime wild systems out of scope. |
| Item, Palette, Misc, TypeEffectiveness variants | Off unless already part of a stable visual profile | Avoids turning this into a broad interaction run. |

Preferred sampled paths:

| Path | Minimum expectation |
|---|---|
| One sampled player starter | Oak-Lab Rival and Route 22 Rival starter both match the expected counter-starter for that starter slot. |
| Optional all-starter-choice matrix | Repeat for all three player starter slots if a stronger follow-up is explicitly requested. |
| Optional later Rival appearances | Sample later Rival appearances only as a separate extension after the Oak-Lab and Route 22 checks pass. |

## Expected Log And Ingame Observations

Record only sanitized summaries. Do not commit or paste full logs.

Expected log/audit summary:

- Randomization completes without crash, fatal exception or bad marker.
- Starter slots are identifiable in sanitized form, enough to derive the expected Rival counter-starter.
- Rival rows remain tagged or treated as Rival/carry-eligible where applicable.
- If runtime-source diagnostics are enabled, only sanitized trainer IDs, classifications and loaded/raw comparison summaries are recorded.
- No private ROM path, output path, hash, full log, screenshot, save, emulator state, secret, token or `.env` value is recorded.

Expected ingame observations:

- The selected player starter is recorded as a species label only.
- The Oak-Lab Rival starter is the expected counter-starter for the selected starter slot.
- The Route 22 Rival starter matches the Oak-Lab Rival starter for that sampled path.
- Any Route 22 Rival non-starter Pokemon may differ from vanilla and may be randomized; this is expected and is not a starter-carry failure.
- The Rival visual/class sprite should not be used as starter proof, but if Trainer Class Sprite Sync is in scope it should remain visually coherent.
- No crash, freeze, softlock or garbled Rival/trainer sprite is observed in the sampled path.

## PASS Criteria

Mark this smoke as `PASS_WITH_CAVEATS` only if all required observations are true for the sampled path:

- Local run completes through Oak-Lab Rival and Route 22 Rival without crash, freeze or softlock.
- Player starter label and expected Rival counter-starter can be stated without private artifacts.
- Oak-Lab Rival starter equals the expected counter-starter.
- Route 22 Rival starter equals the same expected counter-starter.
- Non-starter Rival Pokemon randomization, if observed, is documented separately from the starter slot.
- Evidence is sanitized and limited to high-level species/trainer labels, settings labels and pass/fail observations.
- No P1 promotion is made.

## FAIL Criteria

Mark this smoke as `FAIL` or `BLOCKED` if any of the following occur:

- Oak-Lab Rival receives the player starter, a vanilla fallback inconsistent with the randomized counter-slot, or an unexpected species.
- Route 22 Rival starter differs from the Oak-Lab Rival starter for the same sampled path.
- Rival starter slot appears overwritten by generic Foe Pokemon randomization.
- The run crashes, freezes, softlocks or shows garbled Rival/trainer visuals on the sampled path.
- Runtime-source diagnostics show the sampled Rival battle uses a source outside the documented Rival/carry correction path.
- The only available evidence is a full raw log or private artifact that cannot be sanitized.

Use `BLOCKED` instead of `FAIL` when the run cannot be interpreted because sanitized evidence is insufficient.

## Known Caveats

- Existing evidence covers targeted paths, not all starter choices.
- Current strongest sampled path is Player Charmander -> Oak-Lab Rival Squirtle -> Route 22 Rival Squirtle.
- Non-starter Rival Pokemon remain eligible for Foe Pokemon randomization by design.
- Runtime-source Trainer Pokemon support is targeted-smoke-confirmed for specific rows, not a global trainer proof.
- Loaded-mismatch, invalid-pointer, empty-party, out-of-range rows and full playthrough coverage remain follow-up scope.
- Trainer Class Names without Trainer Class Sprite Sync can visually mismatch labels and sprites; this is not a Rival starter bug.
- This smoke must not promote `FVX-FOE-012` or broader Trainer Pokemon support to P1.

## Handoff

Next local evidence, if requested, should add a short sanitized result section to this file or a follow-up file with:

- settings labels used,
- player starter label,
- expected Rival counter-starter label,
- observed Oak-Lab Rival starter label,
- observed Route 22 Rival starter label,
- whether non-starter Rival Pokemon were randomized,
- pass/fail result and caveats.

Keep ROMs, builds, output ROMs, saves, emulator states, screenshots, hashes, full logs, private paths, secrets, tokens and `.env` content out of committed documentation.
