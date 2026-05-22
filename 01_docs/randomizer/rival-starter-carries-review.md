# Rival Starter Carries Review

Stand: 2026-05-22

Scope: documentation-only review for the current UPR-FVX Rival Counter-Starter / Rival Carries
Starter behavior in the FireRed Gen9 CFRU/DPE workspace. Codex did not read, copy, create, modify or
test ROMs, output ROMs, saves, emulator states, screenshots, private paths, hashes, secrets, tokens or
`.env` data. No UPR-FVX, CFRU or DPE code was changed. No builds were run. No P1 promotion is made.

## Ergebnis

No code fix appears necessary from this documentation-only read. The current code has explicit paths
for:

- Oak-Lab Rival counter-starter correction after starter randomization and after Trainer Pokemon
  randomization.
- `Rival Carries Starter Through Game` for tagged Rival/Friend rows across later encounters.
- FRLG runtime-source Rival trainer rows with known `RIVALx-y` tags.
- Foe Pokemon randomization preserving tagged Rival/Friend starter slots when carry-through is enabled.

The remaining gap is evidence, not an obvious code defect: existing local ingame evidence covers the
sampled Charmander -> Squirtle path for Oak-Lab and Route 22, but it is not an all-starter-choice
matrix, not a later-Rival sweep and not a full playthrough.

## Codepfade

### Starter write and Oak-Lab raw trainer sync

- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/StarterRandomizer.java`
  calls `romHandler.setStarters(...)` after selecting randomized starters.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
  `setStarters(...)` writes starter script bytes and then calls
  `writeFrlgOakLabRivalRawTrainerParties(...)`.
- `writeFrlgOakLabRivalRawTrainerParties(...)` maps player starter slot `0/1/2` to rival counter
  starter slot `1/2/0` and writes the first raw trainer Pokemon species for the three Oak-Lab Rival
  trainer IDs.
- `findFrlgOakLabRivalTrainerIdsByPlayerStarterSlot(...)` discovers the FRLG Oak-Lab tutorial
  trainerbattle commands near `StarterPokemon` and corrects the script-order mismatch:
  script order is rival Squirtle, rival Charmander, rival Bulbasaur; UPR-FVX player slots are
  Charmander, Squirtle, Bulbasaur.
- Extended BPRE writes use internal SpeciesSet identity through `getStarterInternalSpeciesId(...)` and
  `getTrainerPokemonInternalSpeciesId(...)`, not plain NatDex numbers.

### Trainer randomization ordering

- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`
  `maybeRandomizeTrainerPokemon()` is the critical orchestration point.
- If `Rival Carries Starter Through Game` is enabled, it calls
  `trainerPokeRandomizer.makeRivalCarryStarter()` before Trainer Pokemon randomization.
- It then runs `trainerPokeRandomizer.randomizeTrainerPokes()` when Trainer Pokemon is randomized or
  additional Pokemon are added.
- If carry-through is enabled and Trainer Pokemon changed, it reapplies
  `makeRivalCarryStarter()` after randomization.
- Independently, for Gen3, it reapplies `makeFirstRivalCarryStarter()` whenever starters changed or
  Trainer Pokemon changed. This is the Oak-Lab counter-starter preservation path and is not gated on
  `Rival Carries Starter Through Game`.

### Rival carry implementation

- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java`
  `makeRivalCarryStarter()` updates all tagged `RIVAL` rows with starter offset `1` and all tagged
  `FRIEND` rows with starter offset `2`.
- `makeFirstRivalCarryStarter()` limits the generic tag update to encounter `1`, then for FRLG calls
  `syncFrlgOpeningRivalTrainerIds(...)` to correct Oak-Lab rows by trainer ID as well as by tag.
- `rivalCarriesStarterUpdate(...)` computes the starter for each variant with
  `(variant + pokemonOffset) % 3`, then applies level-based evolutions for later encounters.
- During Trainer Pokemon randomization, tagged Rival/Friend starters are protected by the
  `skipStarter` path when carry-through is enabled. Non-starter Pokemon on Rival teams remain eligible
  for normal Foe Pokemon randomization by design.

### Runtime-source Rival rows

- `Gen3RomHandler` has known FRLG runtime-source Rival tags for trainer IDs:
  `0x148/0x146/0x147` through `0x2E5/0x2E3/0x2E4`, covering `RIVAL1` through `RIVAL9`.
- `loadTrainers()` loads normal trainer rows, applies FRLG tags, then calls
  `loadFrlgRuntimeTrainerSourceRows(...)`.
- `findFrlgRuntimeTrainerDataRowsToLoad(...)` uses runtime trainerbattle source discovery plus the
  `UNLOADED_VALID_PARTIES` audit classification to pull valid runtime rows into the trainer model.
- Loaded runtime rows receive either the known Rival/Brock tag or generic `RUNTIME-SOURCE`, and
  `saveFrlgRuntimeTrainerSourceRows(...)` writes valid runtime-source rows back.

## Bestehende Tests / Evidence

### ROM-free tests

- `GameRandomizerStarterRivalSyncTest`
  - Confirms `maybeRandomizeTrainerPokemon()` reapplies `makeFirstRivalCarryStarter()` after Trainer
    Pokemon randomization.
  - Confirms Oak-Lab counter-starter reapply is not conditional on `Rival Carries Starter Through Game`
    being disabled.
  - Confirms carry-through uses `makeRivalCarryStarter()` before and after Trainer Pokemon
    randomization.
- `TrainerSpecialRulesTest`
  - Covers synthetic carry-through across early and later Rival teams.
  - Covers vanilla counter-starter behavior when starters are unchanged.
  - Covers first-Rival-only sync.
  - Covers randomized counter-slot behavior.
  - Covers Foe randomization with carry OFF restoring only Oak-Lab counter-starter.
  - Covers Foe randomization with carry ON restoring Oak-Lab and later Rival counter-starter.
  - Covers untagged FRLG Oak-Lab rows via trainer ID.
  - Covers runtime-source Rival rows tagged from known runtime-source IDs.
- `TrainerRandomizersTest`
  - Has parameterized ROM-handler tests for tagged Rival/Friend carry behavior with randomized Trainer
    Pokemon and with randomized starters.
- `Gen3OakLabRivalScriptTest`
  - Covers Oak-Lab trainerbattle command extraction and script-order remapping.
  - Covers known runtime-source Rival tags.
  - Covers runtime-source row validation/audit behavior.
  - Checks reference Oak-Lab script semantics and that local CFRU source does not own an alternate
    Oak-Lab script file.
- `Gen3OakLabRivalRuntimeSourceRomTest`
  - Contains opt-in private-ROM diagnostics only. It is intentionally skipped unless local private ROM
    properties/env vars are supplied. Codex did not run it.

### Dokumentierte lokale Evidence

- `08_tests/randomizer/192_starter_rival_sync_pass.md`
  - Earlier Oak-Lab randomized starter/counter-slot smoke passed for one sampled path.
  - Marked `Rival Carries Starter Through Game` as separate at that time.
- `08_tests/randomizer/207_rival_counter_starter_and_combined_visual_smoke.md`
  - PR #117 evidence: sampled Player Charmander -> Rival Squirtle.
  - Intro Mon Species `0` regression fixed in the same combined profile.
  - Caveat: targeted visual smoke only.
- `08_tests/randomizer/208_combined_trainer_visual_runtime_smoke.md`
  - Player Charmander -> Oak-Lab Rival Squirtle and Route 22 Rival Squirtle.
  - Route 22 non-starter Pokemon was randomized, supporting the intended behavior that only the Rival
    starter slot is protected/corrected.
  - Route 22 Rival sprite consistency also passed in the sampled run.
- `08_tests/randomizer/212_gen_limit_special_form_item_smoke.md`
  - Reports Oak-Lab Rival counter-starter is preserved independently of
    `Rival Carries Starter Through Game`.
- `08_tests/randomizer/fvx_feature_test_status_matrix.tsv`
  - `FVX-FOE-012` is `PASS_TARGETED_INGAME_SMOKE` with explicit caveats: no all-starter-choice matrix,
    no full playthrough and no P1 promotion.

## Smoke-Plan-Abdeckung

The requested file `08_tests/randomizer/rival_starter_consistency_smoke.md` is not present in this
checkout. Therefore that exact smoke plan cannot currently be treated as covering any cases.

Nearest existing evidence files cover the requested cases as follows:

| Case | Current coverage | Gap |
| --- | --- | --- |
| Oak-Lab Rival | Covered by ROM-free tests and targeted local evidence 192/207/208/212. | Only sampled ingame paths, no all-starter matrix. |
| Route-22 Rival | Covered by targeted local evidence 208 for Player Charmander -> Route 22 Rival Squirtle. | Only one starter-choice path. |
| Later Rival trainers | ROM-free synthetic and tag/runtime-source tests cover the carry logic through later `RIVALx-y` rows. | No documented local ingame later-Rival sweep beyond Route 22. |
| Trainer Pokemon Randomization ON | Covered by ROM-free tests and evidence 208, including randomized Route 22 non-starter Pokemon. | Targeted only. |
| Trainer Pokemon Randomization OFF | ROM-free tests cover starter/carry behavior without Trainer Pokemon randomization. | No dedicated current local ingame OFF smoke documented under the requested plan name. |
| Counter-starter logic | Covered by code, ROM-free tests and sampled local evidence. | All three player-starter choices are not locally smoke-documented on the current final pin. |

## Offene Risiken

- The exact requested smoke plan file is missing, so future handoff readers may not find a single
  Rival-starter checklist under that name.
- Current ingame evidence is targeted: it confirms Charmander -> Squirtle for Oak-Lab and Route 22, not
  all three player-starter choices.
- Later Rival carry behavior is well covered by ROM-free tests, but no current sanitized local ingame
  evidence proves later encounters beyond Route 22.
- Runtime-source logic intentionally skips invalid, out-of-range, empty-party or loaded-mismatch rows.
  That is correct for safety, but any future suspected vanilla-looking Rival battle still needs
  targeted sanitized evidence.
- Class/sprite sync evidence is adjacent but separate. It supports visual consistency, not party
  species correctness by itself.

## Lokale Ingame-Smokes, die Anton noch machen muss

Run these locally only with private ROMs and document only sanitized observations.

1. Oak-Lab + Route 22, Trainer Pokemon Randomization ON, carry-through ON:
   - Choose player starter slot 0, then confirm Oak-Lab Rival has slot 1 counter-starter.
   - Confirm Route 22 Rival starter is the same carried/counter starter.
   - Confirm any Route 22 non-starter Pokemon may be randomized.
2. Repeat the same ON/carry-through ON smoke for player starter slot 1:
   - Expected Rival starter is slot 2.
3. Repeat the same ON/carry-through ON smoke for player starter slot 2:
   - Expected Rival starter is slot 0.
4. Trainer Pokemon Randomization ON, carry-through OFF:
   - Confirm Oak-Lab Rival still has the counter-starter.
   - Confirm Route 22/later Rival starter is not being forced by the carry-through option.
5. Trainer Pokemon Randomization OFF, starters randomized, carry-through OFF:
   - Confirm Oak-Lab Rival still receives the randomized counter-slot starter.
6. Trainer Pokemon Randomization OFF, starters randomized, carry-through ON:
   - Confirm Route 22 and at least one later Rival appearance carry the expected starter family.
7. Later Rival spot check:
   - After Route 22, sample at least one later Rival trainer and record only whether the expected
     starter family appears in the protected starter slot/family path.

Do not document ROM paths, output paths, hashes, full logs, screenshots, saves, emulator states,
private paths, secrets, tokens or `.env` content.

## Code-Fix-Bewertung

No code fix appears necessary from the current read-only review. The implementation already separates
two concerns correctly:

- Oak-Lab counter-starter preservation is always reapplied after Gen3 starter or Trainer Pokemon
  mutations.
- `Rival Carries Starter Through Game` remains the wider later-Rival carry behavior and protects the
  Rival starter slot while allowing non-starter Rival Pokemon to remain randomized.

Recommended next action is documentation/evidence only: either add the missing
`08_tests/randomizer/rival_starter_consistency_smoke.md` in a separately scoped docs PR, or keep this
review as the handoff checklist for Anton's remaining local smokes. No P1 promotion.
