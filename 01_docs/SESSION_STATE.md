# Session update - Wild encounters ROM smoke harness sync

- New branch: `randomizer/wild-encounters-rom-smoke-harness-sync`.
- UPR-FVX PR #65 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins verified merged UPR-FVX commit `f224862c91aed8e7a75fe843f5088cadea734da4`.
- Evidence scope: ROM-facing Wild Encounter smoke harness prepared in UPR-FVX; default no-ROM execution skips cleanly.
- The real local ROM smoke has not been executed in this workspace sync.
- Status remains below P1-supported; no private ROM path, hash, log, output ROM, Randomizer run, ROM evidence result or P1 promotion was added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No new UPR-FVX code change in this workspace sync.
- Note: the requested SHA `c7a07a4643a570b2e27de059804f1a249616aaf0` was not reachable in the UPR-FVX fork; GitHub reports PR #65 merge commit `f224862c91aed8e7a75fe843f5088cadea734da4`.

# Session update - Wild encounters reload equality evidence sync

- New branch: `randomizer/wild-encounters-p1-track`.
- UPR-FVX PR #64 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `d49837fea305157a2fe94f3f57d09cedc8ab25f8`.
- Evidence scope: ROM-free synthetic Writer/Reload Equality evidence for Wild Encounters in `WildCatchLevelDecisionTest`; a reloadable fake `RomHandler` deep-copies `setEncounters(...)` data and reloads fresh `getEncounters(...)` copies.
- Covered invariants: Area metadata, Slot-Anzahlen, Levelbereiche, allowed Species pool and high Species IDs above `1000` remain reload-equal.
- Status remains below P1-supported; no real Gen3 ROM byte writer proof, output ROM, Randomizer run, ROM-Smoke or P1 promotion was added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No new UPR-FVX code change in this workspace sync.

# Session update - Items first test slice sync

- New branch: `docs/sync-items-first-slice`.
- UPR-FVX PR #63 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `d88a0cdb8c11473d2a3448028e937422eaf38679`.
- Evidence scope: third ROM-free Items/Moves/Abilities slice for Items; synthetic `ItemDecisionTest` verifies `ItemRandomizer.randomizeFieldItems()` for Non-TM Field Items keeps choices inside the non-bad allowed Item pool, excludes bad/key-style Items, keeps output non-empty, preserves Field-Item count and allows high Item IDs `1001..1003`.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Moves first test slice sync

- New branch: `docs/sync-moves-first-slice`.
- UPR-FVX PR #62 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `a5b1b63b134149bd88e62af27a9b45332f617d9e`.
- Evidence scope: second ROM-free Items/Moves/Abilities slice for Moves; synthetic `TMTutorMoveDecisionTest` verifies `TMTutorMoveRandomizer.randomizeTMMoves()` keeps TM choices inside the allowed Move pool, excludes HM/game-breaking/levelup-banned/illegal Moves, preserves the Field-Move-TM slot, keeps output count stable and allows high Move IDs `1001..1003`.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Items/Moves/Abilities first test slice sync

- New branch: `docs/sync-items-moves-abilities-first-slice`.
- UPR-FVX PR #61 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `c365b96399ed36881ed637edce0721c059c442d1`.
- Evidence scope: first ROM-free Items/Moves/Abilities slice for Abilities; synthetic `SpeciesAbilityDecisionTest` verifies `SpeciesAbilityRandomizer` keeps Ability choices inside the allowed pool, rejects banned Ability candidates, produces non-empty two-Ability output and keeps high Species ID `1025` in the path.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Learnsets evolution moves test slice sync

- New branch: `docs/sync-learnsets-evolution-moves-slice`.
- UPR-FVX PR #60 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `c40fbbd796db5b43a3bc53e547dc890a853cef20`.
- Evidence scope: fourth ROM-free `LearnsetDecisionTest` slice for Learnsets; synthetic Evolution Moves for All data verifies exactly one Level-0 Evolution-Move slot is added while existing Level-1/later level slots, Move pool and high Species ID `1025` path remain stable.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Learnsets starting moves test slice sync

- New branch: `docs/sync-learnsets-starting-moves-slice`.
- UPR-FVX PR #59 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `0d217db45086d8d03b4eb606ae2621633396d768`.
- Evidence scope: third ROM-free `LearnsetDecisionTest` slice for Learnsets; synthetic Guaranteed Starting Moves data verifies expected Level-1 slots are added while the later level slot, Move pool and high Species ID `1025` path remain stable.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Learnsets option test slice sync

- New branch: `docs/sync-learnsets-option-slice`.
- UPR-FVX PR #58 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `6ed75f5b1e5b8b354e2db694c880407c8e0a10dd`.
- Evidence scope: second ROM-free `LearnsetDecisionTest` slice for Learnsets; synthetic `orderDamagingMovesByDamage()` data verifies damaging Moves are sorted by damage while Evolution-/Non-Damaging-Slots, Level-/Slot-Anzahl, Move pool and high Species ID `1025` remain stable.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Learnsets first test slice sync

- New branch: `docs/sync-learnsets-first-test-slice`.
- UPR-FVX PR #57 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `56cae7eb0c2ddc626dc31c4802d3f696a42959bf`.
- Evidence scope: first ROM-free `LearnsetDecisionTest` slice for Learnsets; synthetic `randomizeMovesLearnt()` data verifies non-empty Learnsets, preserved Level-/Slot-Anzahl, allowed Move-pool selection and high Species ID `1025`.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Wild encounters option test slice sync

- New branch: `docs/sync-wild-encounters-option-slice`.
- UPR-FVX PR #56 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `b3b9a8ab5e8726f4b4d2d4e23efa733cce7287ac`.
- Evidence scope: third ROM-free `WildCatchLevelDecisionTest` slice for Wild Encounters; synthetic `BlockWildLegendaries` coverage verifies legendary Species stay out of the replacement pool while Slot-/Level-/Area structure remains stable.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Wild encounters multi-area test slice sync

- New branch: `docs/sync-wild-encounters-multi-area-slice`.
- UPR-FVX PR #55 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `8f88e25d458996b560189ba23d3216ee0c775f14`.
- Evidence scope: second ROM-free `WildCatchLevelDecisionTest` slice for Wild Encounters; synthetic multi-area data verifies that different Areas, Slot-Anzahlen, Levelbereiche, encounter types, rates and map/location metadata stay structurally stable.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Wild encounters first test slice sync

- New branch: `docs/sync-wild-encounters-first-slice`.
- UPR-FVX PR #54 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `8d67f8686e16b3a9d3e77da5789a06889a645e5f`.
- Evidence scope: first ROM-free `WildCatchLevelDecisionTest` slice for Wild Encounters; synthetic encounters verify preserved Slot-/Level-/Area structure, non-empty encounter areas, allowed Species selection and high-numbered Species IDs above `1000`.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Trainer Class Names encoded length fix sync

- New branch: `docs/sync-trainer-class-names-encoded-length-fix`.
- UPR-FVX PR #53 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `955c852cf07f155a046b18865a39e6912a6ee09c`.
- Fix scope: Trainer Class Names max-length filtering now uses encoded/internal length through `romHandler.internalStringLength(...)` instead of Java `changeTo.length()`.
- Evidence scope: focused ROM-free `TrainerNameRandomizerTest` coverage for class names inside limit, exactly at limit, over limit and Java length != internal length.
- Status remains `tested-non-rom`, not P1-supported; no ROM-facing Writer/Reload, real Terminator/Padding proof, decoded reload equality or Text-Encoding safety claim is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Trainer Names text length unit evidence

- New branch: `docs/trainer-names-text-length-unit-evidence`.
- UPR-FVX PR #52 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `7357b244e01ef2c7790b858d50c19c31ac72e955`.
- Added evidence document `08_tests/randomizer/031_trainer_names_text_length_unit_evidence.md`.
- Evidence scope: ROM-free `TrainerNameRandomizerTest` extension for Trainer Names/Class Names text-length risks: ASCII inside limit, exactly at encoded/internal limit, over encoded/internal limit, Java length != internal length, escaped-token-style divergence and Class-Names `changeTo.length()` risk exposure.
- Status remains `tested-non-rom`, not P1-supported; no ROM-facing Writer/Reload, real Terminator/Padding proof, decoded reload equality or Text-Encoding safety claim is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload fix, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Trainer Names text harness design

- New branch: `analysis/trainer-names-text-harness-design`.
- Added read-only design `08_tests/randomizer/030_trainer_names_text_harness_design.md` for a future ROM-free Trainer Names/Class Names harness.
- Decision: later implementation should be a focused UPR-FVX unit-test scope, with a fake `RomHandler` whose `internalStringLength(...)` can differ from Java length; workspace-only/manual plan, local helper and separate diagnosis harness are less suitable for the first ROM-free step.
- The design keeps byte truncation, terminator/padding and decoded reload equality as a separate synthetic byte-model layer or later ROM-facing evidence, not as proven support.
- Status remains `tested-non-rom`, not P1-supported; no Text-Encoding safety claim is made and `changeTo.length()` remains an open class-name risk.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, hash, secret, token or `.env` file was read, copied, changed or documented.
- No implementation, UPR-FVX code change, Writer-/Reload fix, external download, smoke run, build or P1 promotion was performed.

# Session update - Trainer Names text evidence harness plan

- New branch: `analysis/trainer-names-text-evidence-harness-plan`.
- Added read-only plan `08_tests/randomizer/029_trainer_names_text_evidence_harness_plan.md` for Trainer Names/Class Names only.
- The plan derives minimal later cases from 027/028: ASCII inside limit, ASCII exactly at limit, encoded over-limit rejection, Gen3 escaped/control-token length divergence, terminator/padding checks and decoded reload equality.
- Status remains `tested-non-rom`, not P1-supported; the plan makes no Text-Encoding safety claim and keeps `changeTo.length()` as an open class-name risk.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, hash, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change, Writer-/Reload fix, Text-Encoding implementation, smoke run, build or P1 promotion was performed.

# Session update - Trainer writer/reload/text field review

- New branch: `analysis/trainer-writer-reload-text-field-review`.
- Added read-only review `08_tests/randomizer/028_trainer_writer_reload_text_field_review.md`.
- Identified Trainer writer/reload fields in the Gen3 `loadTrainers()` / `saveTrainers()` path: team flags, Trainer name text, battle mode byte, party size, Pokemon data pointer, per-Pokemon species, level, IV/strength, held item and moves, plus Mossdeep Steven as a special separate team writer.
- Identified Trainer text checks for later evidence: Gen3 `translateString(...)`, `internalStringLength(...)`, `writeFixedLengthString(...)`, `TrainerNameLength`, `TrainerClassNameLength`, terminator/padding behavior and decoded reload equality.
- Open risk remains: Trainer class-name max filtering contains a Java `changeTo.length()` check, so later evidence must prove encoded/internal byte length safety before any Text P1 promotion.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, hash, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change, Writer-/Reload fix, Text-Encoding implementation, smoke run, build or P1 promotion was performed.

# Session update - Trainer ROM/Reload/Text evidence plan

- New branch: `analysis/trainer-rom-reload-text-evidence-plan`.
- Added a read-only plan for later Trainer ROM-/Reload-/Text-Encoding evidence: `08_tests/randomizer/027_trainer_rom_reload_text_evidence_plan.md`.
- The plan records current Trainer suboptions `FVX-FOE-005` through `FVX-FOE-014` as applicable `tested-non-rom`, not P1-supported, based on recent synthetic harness follow-ups.
- Missing evidence is kept separate: later ROM-/Reload evidence, Trainer text-encoding proof, and the `changeTo.length()` length-measurement risk each need their own proof before any promotion.
- No Roadmap status promotion is made: no ROM, save, emulator state, output ROM, log, build artifact, Randomizer JAR, tool binary, private path, hash, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code, Writer-/Reload fix, Text-Encoding implementation, Randomizer run or P1 promotion was performed.

# Session update - Diagnose 181

- New branch: `test/upr-fvx-cfru-dpe-trainer-names-followup`.
- UPR-FVX PR #51 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `d20eb1367c62a4f14c8778bc61ad6904ea76a6d6`.
- Original UPR-FVX test commit: `f49f5aa9 test: cover trainer name decisions`.
- Follow-up 181 records the Non-ROM `TrainerNameRandomizerTest` harness for `FVX-FOE-013` Trainer Names/Class Names.
- Covered decisions: `canChangeTrainerText=false`, Trainer Names singles-/doubles-pools, repeated-name translation, `MAX_LENGTH`, `MAX_LENGTH_WITH_CLASS`, Trainer Class Name pools through `getDoublesTrainerClasses()` and fixed class-name length.
- Statuswirkung: `FVX-FOE-013` moves to `tested-non-rom`, not P1-supported.
- Checks from PR #51 are recorded as `git diff --check`, focused `:random:test --tests '*TrainerNameRandomizer*'` and broader `:random:test --tests '*Trainer*'`, all successful.
- No Gen3 Writer/Reload, ROM-Smoke, text-encoding proof, output-ROM generation, Randomizer run, `changeTo.length()` fix or P1-promotion was performed.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, secret, token or `.env` file was committed.

# Session update - Diagnose 180B

- New branch: `test/upr-fvx-cfru-dpe-battle-style-followup`.
- UPR-FVX PR #50 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `5e2d351966ce4a96d02cdb6ca676b39bde7a9505`.
- Original UPR-FVX test commit: `99f46cce7464750ea5cdc4055b1e9168e59bc1a0`.
- Follow-up 180B records the Non-ROM `TrainerBattleStyleTest` harness for `FVX-FOE-011` Battle Style.
- Statuswirkung: `FVX-FOE-011` moves to `tested-non-rom`, not P1-supported.
- Checks from PR #50 are recorded as `git diff --check`, focused `:random:test --tests '*TrainerBattleStyle*'`, broader `:random:test --tests '*Trainer*'` and full `:random:test`, all successful.
- No Writer/Reload, ROM-Smoke, output-ROM generation, Randomizer run, Trainer Names/Class Names/Text work or P1-promotion was performed.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, secret, token or `.env` file was committed.

# Session update - Diagnose 179B

- New branch: `test/upr-fvx-cfru-dpe-trainer-special-rules-followup`.
- UPR-FVX PR #49 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `bc46fdc49741643d8f09dd302b67b5b2d35d24c5`.
- Original UPR-FVX test commit: `6489dd1e61d1bcb35345ae006032b884527e0a97`.
- Follow-up 179B records the Non-ROM `TrainerSpecialRulesTest` harness for Trainer Special Rules.
- Statuswirkung: `FVX-FOE-010`, `FVX-FOE-012` and `FVX-FOE-014` move to `tested-non-rom`, not P1-supported.
- `FVX-FOE-011` Battle Style and `FVX-FOE-013` Trainer Names/Class Names/Text remain separate and unpromoted.
- Checks from PR #49 are recorded as focused `:random:test --tests com.uprfvx.random.randomizers.TrainerSpecialRulesTest`, broader `:random:test --tests '*Trainer*'` and full `:random:test`, all `BUILD SUCCESSFUL`.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was committed.

# Session update - Diagnose 178B

- New branch: `test/upr-fvx-cfru-dpe-trainer-additional-pokemon-followup`.
- UPR-FVX PR #48 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `32ab7d969e5439d38e5781670c9a68e0ea418d0a`.
- Original UPR-FVX test commit: `cdc09eaee12c44a7f3ba5ca24a091ce4da2ef8ac`.
- Follow-up 178B records the Non-ROM `TrainerAdditionalPokemonTest` harness for Additional Pokemon on Boss, Important and Regular Trainers.
- Guard/Fix: `TrainerPokemonRandomizer` clones additional Pokemon only from original slots with non-null Species; trainers without a safe template are skipped, while max party size 6 and multi-battle limit 3 are covered.
- Statuswirkung: `FVX-FOE-005`, `FVX-FOE-006` and `FVX-FOE-007` move to `tested-non-rom`, not P1-supported.
- Checks from PR #48 are recorded as focused `:random:test --tests com.uprfvx.random.randomizers.TrainerAdditionalPokemonTest`, broader `:random:test --tests '*Trainer*'` and full `:random:test`, all `BUILD SUCCESSFUL`.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was committed.

# Session update - Diagnose 177B

- New branch: `test/upr-fvx-cfru-dpe-trainer-type-diversity-followup`.
- UPR-FVX PR #47 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `ea5269706eb7d04eb0b305f88e8fa20bfb21f92a`.
- Original UPR-FVX test commit: `60f6664e556cc750801ad1d47ba970ded8d6af85`.
- Follow-up 177B records the Non-ROM `TrainerTypeDiversityGuardTest` harness for Trainer Type Diversity / Type Themes.
- Statuswirkung: `FVX-FOE-009` moves to `tested-non-rom`, not P1-supported.
- Checks from PR #47 are recorded as focused `:random:test --tests com.uprfvx.random.randomizers.TrainerTypeDiversityGuardTest`, broader `:random:test --tests '*Trainer*'` and full `:random:test`, all `BUILD SUCCESSFUL`.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was committed.

# Session update - Diagnose 176B

- New branch: `test/upr-fvx-cfru-dpe-wild-catch-level-followup`.
- UPR-FVX PR #46 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `c86221d758bece06b216b1f4fb23dd8e4a6c8ec0`.
- Original UPR-FVX test commit: `8665eb4f070567fd908327b272c7f1da5abdef68`.
- Follow-up 176B records the Non-ROM `WildCatchLevelDecisionTest` harness for Wild catch/level decision paths.
- Statuswirkung: `FVX-WILD-007`, `FVX-WILD-010` and `FVX-WILD-012` move to `tested-non-rom`, not P1-supported.
- Checks from PR #46 are recorded as focused `:random:test --tests com.uprfvx.random.randomizers.WildCatchLevelDecisionTest`, broader `:random:test --tests '*Wild*'` and full `:random:test`, all `BUILD SUCCESSFUL`.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was committed.

# Session update - Diagnose 175B

- New branch: `test/upr-fvx-cfru-dpe-movedata-write-followup`.
- UPR-FVX PR #45 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `1be6f51779906af017f6177f264e41f8c7902d8e`.
- Original UPR-FVX test commit: `60996b166113d40f4ff848d8063e98661415a599`.
- Follow-up 175B records the Non-ROM `Gen3MoveDataWriterTest` and `MoveUpdateDecisionTest` harnesses for MoveData writer/updater decisions.
- Statuswirkung: `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` and `FVX-MOVE-006` move to `tested-non-rom`, not P1-supported.
- `FVX-MOVE-005` Move Names/Text remains out of scope.
- Checks from PR #45 are recorded as focused `:romio:test --tests '*Move*'`, focused `:random:test --tests '*Move*'`, full `:romio:test` and full `:random:test`, all `BUILD SUCCESSFUL`; the known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was committed.

# Session update - Diagnose 174B

- New branch: `test/upr-fvx-cfru-dpe-make-evolutions-easier-followup`.
- UPR-FVX PR #44 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `85b282112322f8991dd11b14cc98d6dd68fd3fd4`.
- Original UPR-FVX test commit: `a0fc6515b60ad3032a8d94c554bbc3021e10a33f`.
- Follow-up 174B records the Non-ROM `EvolutionMakeEasierDecisionTest` harness for `FVX-TRAIT-025A` Make Evolutions Easier Condense-/Level-/Decision logic.
- Test-/Seam-Entscheidung: small package-private helper in `AbstractRomHandler`; synthetic `Species` / `Evolution` chains; intermediate/final level caps, non-level `estimatedEvoLvl` capping and `highestEvoLvl` behavior are covered.
- Statuswirkung: `FVX-TRAIT-025A` moves to `tested-non-rom`; `FVX-TRAIT-025B` remains a separate Gen3 Happiness-byte patch / writer-like scope; `FVX-TRAIT-026` remains helper-only with no standalone support claim.
- Checks from 174A are recorded as `./gradlew --offline :romio:test --tests '*Evolution*'` and `./gradlew --offline :romio:test`, both `BUILD SUCCESSFUL`; the known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 173

- New branch: `test/upr-fvx-cfru-dpe-evolution-make-easier-scope-plan`.
- PR #221 / Follow-up 172B was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `3b33412e80d1cb2d97725ad7a7dd01529aa56919`.
- Diagnose 173 plans `FVX-TRAIT-025` Make Evolutions Easier as a split scope.
- Result: `make-easier-plan-ready`.
- `025A` is ROM-free Condense-/Level-/Decision logic around `AbstractRomHandler.condenseLevelEvolutions(...)`, synthetic Species/Evolution chains, `extraInfo`, `estimatedEvoLvl` and `highestEvoLvl`.
- `025B` is the separate Gen3 Happiness-byte patch / writer-like scope around `Gen3RomHandler.makeEvolutionsEasier(...)` and `Gen3Constants.friendshipValueForEvoLocator`.
- `FVX-TRAIT-026` remains a helper flag for `024/025`, with no standalone support claim.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 172B

- New branch: `test/upr-fvx-cfru-dpe-evolution-method-decisions-followup`.
- UPR-FVX PR #43 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `3b33412e80d1cb2d97725ad7a7dd01529aa56919`.
- Original UPR-FVX test commit: `4b049ee82cf8716cb2fc17d0b6244020cddd22e4`.
- Follow-up 172B records the Non-ROM `EvolutionMethodDecisionTest` harness for `FVX-TRAIT-024` Change Impossible Evolutions and `FVX-TRAIT-027` Remove Time-Based Evolutions.
- Test-/Seam-Entscheidung: small package-private decision seams in `Gen3RomHandler` and `AbstractRomHandler`; synthetic `Species` / `Evolution` objects; no ROM file, Gen3 writer, reload, ROM-Smoke or Randomizer run.
- Statuswirkung: `FVX-TRAIT-024` and `FVX-TRAIT-027` move from `decision-review-ready` to `tested-non-rom`, not P1-supported.
- `FVX-TRAIT-025` remains split into condense-level logic and Gen3 happiness-byte patch risk; `FVX-TRAIT-026` remains a helper flag for `024/025`.
- Checks from 172A are recorded as `./gradlew --offline :romio:test --tests '*Evolution*'` and `./gradlew --offline :romio:test`, both `BUILD SUCCESSFUL`; the known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 171

- New branch: `test/upr-fvx-cfru-dpe-evolution-methods-decision-review`.
- PR #219 / Diagnose 170 was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- Diagnose 171 reviews the Evolution method decision paths for `FVX-TRAIT-024` Change Impossible Evolutions and `FVX-TRAIT-027` Remove Time-Based Evolutions.
- Result: `decision-review-ready`.
- Finding for `024`: Gen3 `removeImpossibleEvolutions(...)` maps FRLG happiness/beauty, Trade and Trade-Item branches to deterministic Stone or Level methods, with `extraInfo` carrying standard Item IDs or levels and `useEstimatedLevels` affecting Level targets only.
- Finding for `027`: `removeTimeBasedEvolutions()` maps `LEVEL_DUSK` to Dusk Stone, paired day/night time evolutions to Sun/Moon Stone, and unpaired time evolutions to `EvolutionType.timeless()` while preserving `extraInfo`.
- Recommended next minimal scope is a small ROM-free UPR-FVX `:romio:test` decision harness for `024/027`; writer/reload and ROM-Smoke remain separate.
- `FVX-TRAIT-025` remains split into condense-level logic and Gen3 happiness-byte patch risk; `FVX-TRAIT-026` remains a helper flag for `024/025`.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 170

- New branch: `test/upr-fvx-cfru-dpe-evolution-methods-scope-plan`.
- PR #218 / Follow-up 169B was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- Diagnose 170 plans the separate Evolution methods/improvement slices `FVX-TRAIT-024` through `FVX-TRAIT-027`.
- Result: `methods-plan-ready`.
- Finding: `GameRandomizer.maybeApplyEvolutionImprovements()` dispatches `024`, `025` and `027` through `RomHandler` improvement methods, while `026` is an estimated-level helper flag for `024/025`.
- `FVX-TRAIT-024` and `FVX-TRAIT-027` need method-mapping decision evidence before any writer/reload scope; `FVX-TRAIT-025` splits into ROM-free condense-level logic and Gen3 happiness-byte patch risk; `FVX-TRAIT-026` should not be promoted standalone.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 169B

- New branch: `test/upr-fvx-cfru-dpe-evolution-filter-non-rom-harness-followup`.
- UPR-FVX PR #42 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- Original UPR-FVX test commit: `e71a126c test: cover evolution filter options`.
- Follow-up 169B records the Non-ROM `EvolutionFilterOptionsTest` harness for `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023`.
- Statuswirkung: these slices move from `harness-plan-ready` to `tested-non-rom`, but not to P1-supported because there was no ROM-Smoke, Gen3 writer test, reload or output-ROM scope.
- 169A checks are recorded as `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.EvolutionFilterOptionsTest` and `./gradlew --offline :random:test`, both `BUILD SUCCESSFUL`.
- `FVX-TRAIT-024` through `FVX-TRAIT-027` remain separate not-started Evolution-improvement/method slices.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 168

- New branch: `test/upr-fvx-cfru-dpe-evolution-filter-harness-plan`.
- PR #216 / Diagnose 167 was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 168 plans a Non-ROM harness for Evolution filter slices `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023`.
- Result: `harness-plan-ready`.
- Finding: the target slices are all in `EvolutionRandomizer` Species-carrier/filter logic and can be tested with synthetic `Species` / `Evolution` data plus a small `RomHandler` proxy/fake, likely in `EvolutionRandomizerTest` or a new `EvolutionFilterRandomizerTest`.
- No production-code seam is expected; no ROM-Smoke, Randomizer run, build, testcode, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 167

- New branch: `test/upr-fvx-cfru-dpe-evolution-suboptions-consolidation`.
- PR #215 / Diagnose 166 was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 167 consolidates Evolution suboptions `FVX-TRAIT-016` through `FVX-TRAIT-027`.
- Result: `evolution-scope-consolidated`.
- Consolidated status: `FVX-TRAIT-016` remains P1-supported; `FVX-TRAIT-018` and `FVX-TRAIT-019` are `diagnosis-ready`; `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023` remain plan-only Species-Carrier filters; `FVX-TRAIT-024` through `FVX-TRAIT-027` remain not-started Evolution-improvement/method slices outside the narrow Species-Carrier.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 166

- New branch: `test/upr-fvx-cfru-dpe-evolution-same-typing-diagnostics`.
- PR #214 / Diagnose 165 was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 166 reclassifies `FVX-TRAIT-019` Evolution Same Typing read-only as `diagnosis-ready`.
- Finding: the original 070 Same-Typing blocker (`saveSuccessful=false`, no Output/Reload, `NullPointerException`) is superseded by Diagnose 079/080. The current `EvolutionRandomizer` Same-Typing filter uses `hasUsableSharedType(...)` and guards candidate null/unsupported Primary Type before `candidate.hasSharedType(reference)`.
- Diagnose 080 confirms Save/Log/Output/Reload true, `writeReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` and `stacktrace=none` for the narrow Same-Typing scope.
- No immediate UPR-FVX fixblock is recommended for this narrow Same-Typing scope; next minimal work is status reconciliation or, if extra evidence is requested, a read-only code-review / Non-ROM harness plan.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 165

- New branch: `test/upr-fvx-cfru-dpe-evolution-similar-strength-diagnostics`.
- PR #213 / Diagnose 164 was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 165 reclassifies `FVX-TRAIT-018` Evolution Similar Strength read-only as `diagnosis-ready`.
- Finding: the original 070 blocker (`writeReloadEvolutionMismatches=24` plus `Bad Egg=true`) is superseded by Diagnose 081/082. The normalized reload comparison in 082 confirms Save/Log/Output/Reload true, `normalizedWriteReloadEvolutionMismatches=0`, `rawWithFormeWriteReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` and `stacktrace=none`.
- No immediate UPR-FVX fixblock is recommended for this narrow Similar-Strength scope; next minimal work is status reconciliation or, if extra evidence is requested, a read-only code-review / Non-ROM harness plan.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 164

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-final-classification`.
- UPR-FVX submodule remains pinned at `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 164 closes In-Game Trades in the tested CFRU/DPE Gen9-BPRE scope as `guarded/preserve-only, not supported`.
- Rationale: no valid active In-Game Trade rows are confirmed; `P1-supported`, `candidate-confirmed` and hard `unsupported-dummy` are not justified by the current evidence.
- Achieved evidence remains valuable: mutation guard, writer-preserve guard, non-ROM `TradeRandomizerTest`, and ROM-free `Gen3InGameTradeWriterTest`.
- No ROM-Smoke, Species-Write-Smoke, Randomizer run, build, code change, text/Nickname/OT, IV or Trade Held Item randomization was performed or authorized.

# Session update - FVX dashboard XLSX export script

- New branch: `docs/fvx-dashboard-xlsx-export-script`.
- Added `07_scripts/randomizer/export_fvx_progress_dashboard_xlsx.py`, a Python standard-library exporter for selected Markdown tables from `01_docs/randomizer/fvx-progress-dashboard.md`.
- Exported sheets include Summary, Gesamtfortschritt, GUI-Feature-Gruppen, Vollstaendige Feature-Liste, Offene Blocker, Naechste Arbeitspakete, Zuletzt PRs Diagnosen and Carrier-tested nicht global.
- The exporter refuses to write if the complete feature list is shortened from 130 data rows.
- No external dependency, dependency installation, ROM/save/build/tool-binary/private path/hash/secret/`.env` access, UPR-FVX code change or generated dashboard workbook commit is required.

# Session update - Diagnose 163B

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-writer-preserve-followup`.
- UPR-FVX PR #41 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 163B records the ROM-free Gen3 In-Game Trades writer-preserve test follow-up. The pinned `Gen3InGameTradeWriterTest` uses synthetic `InGameTrade` rows and synthetic bytes to verify unsafe/null-request rows are skipped before byte writes and preserved unchanged.
- UPR-FVX PR #41 implementation-side checks are recorded as `./gradlew --offline :romio:test` and focused `./gradlew --offline :romio:test --tests com.uprfvx.romio.romhandlers.Gen3InGameTradeWriterTest`, both with `BUILD SUCCESSFUL`.
- The known existing report failure line for `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` remains documented as a risk/assumption.
- In-Game Trades remain `blocked-pending-evidence`; no ROM-Smoke, Species-Write-Smoke, valid-active-row promotion, text, Nickname/OT, IV or Trade Held Item randomization is authorized.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 162

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-writer-preserve-test-plan`.
- PR #206 / Follow-up 161B was verified as merged before this block.
- UPR-FVX submodule remains pinned at `1eaee2873cd69682335223f817b124bf36d004f2`.
- Diagnose 162 plans a ROM-free Gen3 In-Game Trades writer-preserve test. Result: `writer-test-plan-ready`.
- Read-only finding: `Gen3RomHandler.setInGameTrades(...)` checks `canWriteInGameTrade(...)` before nickname, Species, IV, OT ID, held-item, OT-name and requested-Species byte writes, so unsafe rows are preserve/skipped before row mutation.
- A later test should add only a narrow `:romio:test` seam around the Gen3 row-write decision or eligibility helper; direct construction of a ROM-backed handler is not recommended.
- In-Game Trades remain `blocked-pending-evidence`; no code, build, Randomizer run, ROM-Smoke, Species-Write-Smoke, text, Nickname/OT, IV or Trade Held Item scope was performed.

# Session update - Diagnose 161B

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-non-rom-harness-followup`.
- UPR-FVX PR #40 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `1eaee2873cd69682335223f817b124bf36d004f2`.
- Diagnose 161B records the non-ROM In-Game Trades `TradeRandomizerTest` harness follow-up. The harness uses synthetic `InGameTrade` rows and a minimal `RomHandler` proxy/fake to cover null-request and placeholder/unsafe Species skips, all-skipped no `setInGameTrades(...)`, `isChangesMade=false`, skip counters and `hasSkippedTrades()`.
- UPR-FVX PR #40 implementation-side check is recorded as `./gradlew --offline :random:test` with `BUILD SUCCESSFUL`.
- In-Game Trades remain `blocked-pending-evidence`; no Gen3 writer test, ROM-Smoke, Species-Write-Smoke, text, Nickname/OT, IV or Trade Held Item randomization is authorized.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 160

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-non-rom-harness-plan`.
- PR #204 / Diagnose 159 was verified as merged before this block.
- UPR-FVX submodule remains pinned at `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Diagnose 160 plans a small non-ROM harness for the In-Game Trades guard. Result: `harness-plan-ready`.
- Recommended first scope: `TradeRandomizer` unit tests with synthetic `InGameTrade` rows and a fake/test `RomHandler`, proving null-request and unsafe Species rows skip before mutation, all-skipped input avoids `setInGameTrades(...)`, and skip counters stay observable.
- Optional Gen3 writer preserve coverage is useful only if it can be done without ROM bytes, broad refactor or generated artifacts.
- In-Game Trades remain `blocked-pending-evidence`; no Species-Write-Smoke, ROM smoke, build, Randomizer run, code change, submodule change, text, Nickname/OT, IV or Trade Held Item scope was performed.

# Session update - Diagnose 159

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-guard-code-review`.
- PR #203 / Follow-up 158B was verified as merged before this block.
- UPR-FVX submodule remains pinned at `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Diagnose 159 reviews `TradeRandomizer.java` and `Gen3RomHandler.java` read-only against the Diagnose 156 Preserve/Skip policy.
- Result: `review-pass-with-risks`. Unsafe In-Game Trade rows are skipped before mutation and preserved/skipped before Gen3 byte writes; no text, Nickname/OT, IV or Trade Held Item path was expanded.
- In-Game Trades remain `blocked-pending-evidence`; Species-Write-Smoke remains blocked. A later non-ROM harness is useful before any ROM-facing smoke is considered.
- No code, build, Randomizer run, ROM/save/output/log access, submodule change or external download was performed.

# Session update - Diagnose 158B

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-null-request-guard-followup`.
- UPR-FVX PR #39 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Diagnose 158B records the In-Game Trades Null-/Invalid-Species guard follow-up: `TradeRandomizer.java` skips unsafe rows before mutation and `Gen3RomHandler.java` preserves/skips unsafe rows before byte writes.
- In-Game Trades remain `blocked-pending-evidence`; no Species-Write-Smoke, text randomization, Nickname/OT randomization, IV randomization or Trade Held Item randomization is authorized by this follow-up.
- 158A Gradle context is recorded as an assumption/risk: `./gradlew --offline :romio:test :random:test` reported `BUILD SUCCESSFUL`, while an existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` failure line remained in the romio report.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 157

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-null-request-guard-plan`.
- PR #201 / Diagnose 156 is contained in `main` before this block.
- Diagnose 157 documents a read-only defensive Null-Requested-Species Skip/Guard plan for In-Game Trades.
- Result: In-Game Trades remain `blocked-pending-evidence`; the later minimal fix would skip/preserve rows with `requestedSpecies == null` or invalid/placeholder Species before mutation/write and report skipped/preserved rows clearly.
- No code, build, Randomizer run, Species-Write-Smoke, text randomization, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 156

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-preserve-skip-policy`.
- PR #200 / Diagnose 155 is contained in `main` before this block.
- Diagnose 156 defines the In-Game Trades Preserve/Skip policy from Diagnoses 152, 154 and 155.
- Result: `blocked-pending-evidence`. All modeled In-Game Trade rows stay preserve-only; no Species-Write-Smoke, Trade Held Item, IV, Nickname/OT or other In-Game Trade write work is allowed.
- `unsupported-dummy` remains plausible but unproven without additional read-only candidate-structure evidence; no code, build, Randomizer run, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 155

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-active-row-candidates`.
- Diagnose 155 performs the requested read-only In-Game Trades active-row candidate check from UPR-FVX `TradeTableOffset`, `TradeTableSize`, `TradesUnused` and the 60-byte Gen3 row model.
- Result: blocked. The BPRE model exposes three non-unused rows, but Diagnose 152 evidence still has `requestedSpeciesNullCount=3`, `invalidTradeSpecies=6` and `placeholderTradeSpecies=6`, so no valid active row is confirmed.
- `unsupported-dummy` remains plausible but unproven; no Species-Write-Smoke, text randomization, build, Randomizer run, ROM/save/output/log access or code change was performed.

# Session update - Diagnose 154

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-table-model-diagnostics`.
- Diagnose 154 documents the UPR-FVX Gen3/FireRed In-Game Trades locator/table model using read-only source and documentation inspection.
- Result: blocked. The model expects ROM-entry `TradeTableOffset`, `TradeTableSize`, `TradesUnused` and 60-byte rows, but Diagnose 152 remains unresolved with null/invalid/placeholder Species fields.
- No code changes, no build, no Randomizer run, no ROM/save/output access, no write smoke and no text randomization were performed.

# Session update - Diagnose 153

- New branch: `analysis/upr-fvx-cfru-dpe-ingame-trades-table-model-blocker-plan`.
- PR #197 was merged; `main` was fast-forwarded before planning.
- Diagnose 153 documents the In-Game Trades locator/table-model blocker: `TradeTableOffset`, `TradeTableSize` and `TradesUnused` come from the Gen3 ROM entry, while `setInGameTrades(...)` dereferences requested Species and therefore is unsafe after Diagnose 152 null/invalid Species results.
- No code changes, no build, no Randomizer run, no write/save, no ROM/artifact access and no `02_external/**` edits were made.

# Session update - Diagnose 152

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-scope-diagnostics`.
- PR #196 was merged; `main` was fast-forwarded before the diagnostic.
- Read-only In-Game Trades candidate diagnostic completed as blocked/preflight. The candidate loaded, but the current UPR-FVX Gen3 BPRE trade-table model produced null/invalid Species fields and unstable fixed-length text terminator classification.
- No code changes, no build, no Randomizer run, no write/save, no output ROM and no private paths, ROM names, hashes, offsets or raw bytes were documented.

# Session update - Diagnose 151

- New branch: `analysis/upr-fvx-cfru-dpe-ingame-trades-scope-plan`.
- PR #195 was merged; `main` was fast-forwarded before planning.
- Diagnose 151 adds the In-Game Trades diagnostics scope plan as the next genuinely open GUI scope after Standard Wild, Special Wild documentation, item scopes and Held Items.
- Codepath finding: `GameRandomizer.maybeRandomizeInGameTrades()` dispatches to `TradeRandomizer.randomizeIngameTrades()`, which mutates `InGameTrade` records and writes through `RomHandler.setInGameTrades(...)`; Gen3 uses fixed-size trade table entries with Species, IV, held-item, nickname and OT fields.
- No code changes, no build, no Randomizer run, no ROM/artifact access and no `02_external/**` edits were made.

# 2026-05-15 - Diagnose 150

- Current branch documents CFRU/DPE Special Wild triggerability read-only.
- Result: no Special Wild system currently requires immediate UPR-FVX randomization for the tracked compatibility state.
- Day/Night headers exist but are sentinel-only/dormant; Swarms, Roamers, Wild Double and `gWildDataSwitch` are runtime-state driven; DexNav is partial/future; Raids need a separate future parser/write scope if required.
- Standard Wild remains P0-supported and was not retested.

# 2026-05-15 - Diagnose 149

- Current branch reconciles Randomizer feature coverage after Held Items closure and the merged Wild Encounters plan.
- Assessment: Standard Wild/Surfing/Fishing/Rock Smash P0 is already covered; do not spend the next block retesting Standard Wild.
- Genuinely open major scope: CFRU Day/Night and special Wild Encounter systems such as Swarms, Roamers, DexNav, Raids and Altering Cave/Tanoby-style cases.
- No code, build, Randomizer run, ROM access or tool-manifest change was made.

# 2026-05-15 - Diagnose 148

- Current branch plans Wild Encounters/Wild Pokemon Randomization as the next separate CFRU/DPE Gen9-BPRE scope after Held Items closure.
- Scope is explicitly separate from Wild Held Items, Trainer Pokemon, Starters, Static/Gift Pokemon, Field Items, Pickup and Shops.
- Code findings: Gen3 `getEncounters`/`setEncounters` use fixed EncounterArea/Encounter slot tables for Walking, Surfing, Rock Smash/Interact and Fishing, with CFRU/DPE extended BPRE species writes using SpeciesSet identity.
- No feature is promoted in this plan; next step is read-only Wild Encounters candidate diagnostics.

# 2026-05-15 - Diagnose 147

- Current branch records Starter Held Items + Ban Bad Write/Reload-Smoke.
- Smoke result: PASS; save/log/output/reload succeeded and `starterHeldItemReloadMismatches=0`.
- Ban Bad result: `badStarterHeldItemWrites=0`, `heldItemPoolAllowedSize=212`, `heldItemPoolNonBadSize=161`, `badStarterHeldItemPoolExcluded=51`.
- Safety metrics: invalid/unloaded/fallback/placeholder writes all `0`; Wild, Trainer, Field, Pickup and Shop scopes stayed unchanged.
- The tested Held Items scope is closed.

# 2026-05-15 - Diagnose 146

- Current branch records Starter Held Items Write/Reload-Smoke without Ban Bad.
- Smoke result: PASS; save/log/output/reload succeeded and `starterHeldItemReloadMismatches=0`.
- Starter model result: one shared Gen3/FRLG Starter Held Item slot changed from empty to non-empty and reloaded stably.
- Safety metrics: bad/TM/invalid/unloaded/fallback/placeholder Starter-Held-Item writes all `0`; Wild, Trainer, Field, Pickup and Shop scopes stayed unchanged.
- Starter Ban Bad remains the only open Starter Held Items sub-scope.

# 2026-05-15 - Diagnose 145

- Current branch records Regular Trainer Held Items filtered Write/Reload-Smoke.
- Smoke result: PASS; save/log/output/reload succeeded and `regularTrainerHeldItemReloadMismatches=0`.
- Filter result: `highestLevelHeldItemWrites=697`, `consumableHeldItemWrites=697`, `sensibleHeldItemWrites=697`, with `nonConsumableHeldItemWrites=0` and `nonSensibleHeldItemWrites=0`.
- Preserve result: Boss, Important and `shouldNotGetBuffs` Trainer Held Items stayed unchanged; Wild, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Next minimal scope is Starter Held Items unless Boss/Important filter combinations are explicitly required.

# 2026-05-15 - Diagnose 144

- Current branch plans Trainer Held Item filters as a separate sub-scope after Boss, Important and Regular no-filter smokes passed.
- Code findings: `Consumable Only`, `Sensible Items` and `Highest Level Only` are separate Trainer Held Item settings; no separate Trainer Held Item Ban Bad flag was found.
- Recommended next smoke: Regular Trainers only with the combined filter set, or split filters if narrower isolation is preferred.
- Starter Held Items remain unpromoted and should follow after the filter coverage decision.

# 2026-05-15 - Diagnose 143

- Current branch records Regular Trainer Held Items Write/Reload-Smoke.
- Smoke result: PASS; `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `regularTrainerHeldItemReloadMismatches=0`.
- Preserve result: Boss, Important and `shouldNotGetBuffs` Trainer Held Items stayed unchanged with mismatch counters all `0`.
- Safety metrics: invalid/unloaded/fallback/placeholder Trainer-Held-Item writes all `0`; Wild, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Trainer Held Items are now covered for Boss, Important and Regular Trainers in the tested no-filter scopes; filters and Starter Held Items remain open.

# 2026-05-15 - Diagnose 142

- Current branch records Important Trainer Held Items Write/Reload-Smoke.
- Smoke result: PASS; `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `importantTrainerHeldItemReloadMismatches=0`.
- Preserve result: Boss, Regular and `shouldNotGetBuffs` Trainer Held Items stayed unchanged with mismatch counters all `0`.
- Safety metrics: invalid/unloaded/fallback/placeholder Trainer-Held-Item writes all `0`; Wild, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Trainer Held Items are now covered for Boss and Important Trainers in the tested scopes; Regular, filters and Starter Held Items remain open.

# 2026-05-15 - Diagnose 141

- Current branch records Boss Trainer Held Items Write/Reload-Smoke.
- Smoke result: PASS; `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `bossTrainerHeldItemReloadMismatches=0`.
- Preserve result: Important, Regular and `shouldNotGetBuffs` Trainer Held Items stayed unchanged with mismatch counters all `0`.
- Safety metrics: invalid/unloaded/fallback/placeholder Trainer-Held-Item writes all `0`; Wild, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Trainer Held Items are now covered only for Boss Trainers in the tested scope; Important, Regular, filters and Starter Held Items remain open.

# 2026-05-15 - Diagnose 140

- Current branch records Wild/Encounter Held Items + Ban Bad Write/Reload-Smoke.
- Smoke result: PASS; `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `wildHeldItemReloadMismatches=0`.
- Ban Bad result: `badWildHeldItemWrites=0`, `wildHeldItemsBadBefore/After/Reload=174/0/0`, `badWildHeldItemPoolCandidates=51`, `badWildHeldItemPoolExcluded=51`.
- Safety metrics: invalid/unloaded/fallback/placeholder Wild-Held-Item writes all `0`; Trainer, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Wild/Encounter Held Items are now covered with and without Ban Bad in the tested scope; Trainer Held Items and Starter Held Items remain open.

# 2026-05-15 - Diagnose 139

- Current branch records Wild/Encounter Held Items Write/Reload-Smoke without Ban Bad.
- Smoke result: PASS; `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `wildHeldItemReloadMismatches=0`.
- Wild held item slots stayed stable at `5656/5656/5656`; non-zero slots changed as expected `526/312/312`.
- Safety metrics: invalid/unloaded/fallback/placeholder Wild-Held-Item writes all `0`; Trainer, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Wild/Encounter Held Items without Ban Bad are GUI-compatible in the tested scope; Ban Bad, Trainer Held Items and Starter Held Items remain open.

# 2026-05-15 - Diagnose 138

- Current branch records read-only CFRU/DPE Gen9-BPRE Held Items candidate diagnostics.
- Result: PASS for read-only structure; `candidateLoaded=true`, `heldItemScanSuccessful=true`, Wild/Encounter, Trainer and Starter held-item paths are readable.
- Key metrics: `wildHeldItemsTotal=5656`, `wildHeldItemsNonZero=526`, `trainerHeldItemsTotal=1754`, `trainerHeldItemsNonZero=87`, `starterHeldItemsTotal=1`, `starterHeldItemsNonZero=0`.
- Safety metrics: invalid/unloaded held item IDs `0`, fallback held items `109`, placeholder held items `130`, `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `shopScopeChanged=false`.
- No feature promotion; next minimal block is Wild/Encounter Held Items smoke without Ban Bad.

# 2026-05-15 - Diagnose 137

- Current branch plans Held Items as the next separate CFRU/DPE Gen9-BPRE Randomizer scope after closed Shop Items.
- Scope split: Wild/Encounter Held Items, Trainer Held Items, and Starter Held Items if the candidate exposes a stable starter-held-item path.
- Read-only codepath finding: Wild/Encounter writes Species/BaseStats held-item fields, Trainer writes `TrainerPokemon.heldItem`, and Starter uses `getStarterHeldItems()` / `setStarterHeldItems(...)`.
- No smoke, no code changes, no ROM/artifact access, no submodule pin change, and no Held-Item feature promotion in this block.

# 2026-05-15 - Diagnose 136

- Current branch records Shop-only FVX-ITEM-009 Balance Prices + Cheap Rare Candies Write/Reload-Smoke.
- Smoke result: PASS with `ShopItemsMod.UNCHANGED`, `balanceShopPrices=true`, `addCheapRareCandiesToShops=true`.
- Shop-list result: `shopItemsTotal=157/180/180`, deltas `+23/+23`, `rareCandyWrites=23`, `skippedShopRareCandyWrites=20`, `shopItemReloadMismatches=0`.
- Price result: `balancedPriceWrites=132`, `rareCandyPriceTouched=true`, `rareCandyPriceReloadStable=true`, `priceReloadMismatches=0`.
- Shop Items scope is closed for the tested CFRU/DPE Gen9-BPRE GUI-compatible paths; Held Items diagnostics plan is the next major scope.

# Session update - 2026-05-15 - Diagnose 135

- Current branch records Shop-only FVX-ITEM-009 Cheap Rare Candies Write/Reload-Smoke.
- Smoke result: PASS with `ShopItemsMod.UNCHANGED`, `addCheapRareCandiesToShops=true`, `balanceShopPrices=false`.
- Shop-list result: `shopItemsTotal=157/180/180`, deltas `+23/+23`, `rareCandyWrites=23`, `skippedShopRareCandyWrites=20`, `shopItemReloadMismatches=0`.
- Price result: `rareCandyPriceTouched=true`, `rareCandyPriceReloadStable=true`, `priceReloadMismatches=0`.
- FVX-ITEM-009 is now individually covered for Balance Shop Prices and Cheap Rare Candies; their combination remains untested.

# Session update - 2026-05-15 - Diagnose 134

- Current branch records Shop-only FVX-ITEM-009 Balance Shop Prices Write/Reload-Smoke.
- Smoke result: PASS with `ShopItemsMod.UNCHANGED`, `balanceShopPrices=true`, `addCheapRareCandiesToShops=false`.
- Price result: `priceTableTouched=true`, `balancedPriceWrites=132`, `priceReloadMismatches=0`, price entry counts stay `1779`.
- Shop-list result: `shopCount=23`, `shopItemsTotal=157`, `shopItemReloadMismatches=0`, skipped Shop mismatches 0.
- FVX-ITEM-009 is promoted only for Balance Shop Prices; Cheap Rare Candies remain open.

# Session update - 2026-05-15 - Diagnose 133

- Current branch plans `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies` as a separate Shop-only subscope.
- Read-only codepath finding: Balance Shop Prices runs after the `ShopItemsMod` switch and can write prices independently of Shop item shuffle/random.
- Cheap Rare Candies appends one Rare Candy to each Shop via `setShops(...)` and sets the Rare-Candy price via `setShopPrices(...)`, so it combines Shop-list growth with price writes.
- Recommended order: Balance Shop Prices smoke first, Cheap Rare Candies smoke second, combination only after both individual smokes are reload-stable.
- FVX-ITEM-005..008 stay GUI-compatible only in their documented individual scopes; FVX-ITEM-009 remains Write modelliert until smoke.

# Session update - 2026-05-15 - Diagnose 132

- Current branch records Shop-only FVX-ITEM-008 Guarantee X Items Write/Reload-Smoke.
- Smoke result: PASS; `guaranteedXItemsExpected=7`, `guaranteedXItemsPresent=7`, `guaranteedXItemsReloadPresent=7`, missing counts stay 0.
- Stable metrics: `shopCount=23`, `mainGameShopCount=3`, `skippedShopCount=20`, `specialShopCount=3`, `shopItemsTotal=157`, `minShopLength=2`, `maxShopLength=9`, reload mismatches 0.
- Foreign scopes stayed false: `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`; prices stayed untouched.
- FVX-ITEM-008 now has separate GUI-compatible evidence for Guarantee Evolution Items and Guarantee X Items; the Evolution+X combination and FVX-ITEM-009 remain open.

# Session update - 2026-05-15 - Diagnose 131

- Current branch records Shop-only FVX-ITEM-008 Guarantee Evolution Items Write/Reload-Smoke.
- Smoke result: PASS; `guaranteedEvolutionItemsExpected=6`, `guaranteedEvolutionItemsPresent=6`, `guaranteedEvolutionItemsReloadPresent=6`, missing counts stay 0.
- Stable metrics: `shopCount=23`, `mainGameShopCount=3`, `skippedShopCount=20`, `specialShopCount=3`, `shopItemsTotal=157`, `minShopLength=2`, `maxShopLength=9`, reload mismatches 0.
- Foreign scopes stayed false: `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`; prices stayed untouched.
- FVX-ITEM-008 is promoted only for Guarantee Evolution Items in the tested Shop-only Random scope; Guarantee X Items and FVX-ITEM-009 remain open.

# 2026-05-15 - Shop Guarantee Items Scope Plan

- Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-shop-guarantee-items-scope-plan`.
- Diagnose 130 plant `FVX-ITEM-008 Guarantee Evolution/X Items` als separaten Shop-only Subscope.
- Read-only Befund: Guarantee Evolution/X wirkt nur bei `ShopItemsMod.RANDOM` ueber `setupGuaranteed()` und `placeNewItems(...)`.
- Placement zielt auf Special Shops; Guaranteed Items werden fuer MainGame-Special-Shops reserviert, SkipShops bleiben preserve-only.
- `FVX-ITEM-005`, `FVX-ITEM-006` und die einzeln getesteten `FVX-ITEM-007` Ban-Flags bleiben GUI-kompatibel; `FVX-ITEM-008` bleibt bis Smoke `Write modelliert`, `FVX-ITEM-009` bleibt offen.

# 2026-05-15 - Shop Items Random + Ban OP Smoke

- Arbeitsbranch: `test/upr-fvx-cfru-dpe-shop-items-random-ban-op-reload-smoke`.
- Diagnose 129 dokumentiert den Shop-only `FVX-ITEM-007` Subscope `ShopItemsMod.RANDOM + banOPShopItems=true`.
- Smoke bestanden: `opShopSetClassifiable=true`, Save, Log, Output und Reload erfolgreich; `shopItemReloadMismatches=0`, `opShopItemBannedWrites=0`, Skip-Shops und Preise unveraendert.
- `FVX-ITEM-007` ist fuer Ban Bad, Ban Regular und Ban OP einzeln belegt; Ban-Kombinationen, `FVX-ITEM-008` und `FVX-ITEM-009` bleiben offen.

# 2026-05-15 - Shop Items Random + Ban Regular Smoke

- Arbeitsbranch: `test/upr-fvx-cfru-dpe-shop-items-random-ban-regular-reload-smoke`.
- Diagnose 128 dokumentiert den Shop-only `FVX-ITEM-007` Subscope `ShopItemsMod.RANDOM + banRegularShopItems=true`.
- Smoke bestanden: `regularShopSetClassifiable=true`, Save, Log, Output und Reload erfolgreich; `shopItemReloadMismatches=0`, `regularShopItemBannedWrites=0`, Skip-Shops und Preise unveraendert.
- `FVX-ITEM-007` ist fuer Ban Bad und Ban Regular einzeln belegt; OP-Ban, `FVX-ITEM-008` und `FVX-ITEM-009` bleiben offen.

# 2026-05-15 - Shop Items Random + Ban Bad Smoke

- Arbeitsbranch: `test/upr-fvx-cfru-dpe-shop-items-random-ban-bad-reload-smoke`.
- Diagnose 127 dokumentiert den Shop-only `FVX-ITEM-007` Subscope `ShopItemsMod.RANDOM + banBadRandomShopItems=true`.
- Smoke bestanden: Save, Log, Output und Reload erfolgreich; `shopItemReloadMismatches=0`, `badShopItemWrites=0`, Skip-Shops und Preise unveraendert.
- `FVX-ITEM-005` und `FVX-ITEM-006` bleiben im getesteten Shop-only Scope GUI-kompatibel.
- `FVX-ITEM-007` ist nur fuer Ban Bad hochgestuft; Regular-Ban, OP-Ban, `FVX-ITEM-008` und `FVX-ITEM-009` bleiben offen.

# Session State Update - 2026-05-15 - Shop Item Bans scope plan

- Branch: `analysis/upr-fvx-cfru-dpe-shop-item-bans-scope-plan`.
- Workspace PR #170 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/126_shop_item_bans_scope_plan.md`.
- Read-only UPR-FVX analysis confirms `FVX-ITEM-007 Shop Item Bans` as a Shop-only sub-scope after `FVX-ITEM-006`.
- The Ban flags affect `ItemRandomizer.randomizeShopItems()` through `setupPossible()` and therefore require `ShopItemsMod.RANDOM`; they do not affect `ShopItemsMod.SHUFFLE` or `UNCHANGED`.
- Baseline from Diagnose 125 remains the pool anchor: `allowedShopItemPoolSize=536`, `nonBadShopItemPoolSize=485`, with `badShopItemsBefore/After/Reload=36` treated as existing inventory, not a Ban result.
- Recommended first executable smoke: Shop Random + Ban Bad only, with `banBadRandomShopItems=true` and Regular/OP/Guarantee/Price/Rare-Candy options disabled.
- `FVX-ITEM-005` and `FVX-ITEM-006` remain `GUI-kompatibel` in their tested Shop-only scopes. `FVX-ITEM-007` remains `Write modelliert`; `FVX-ITEM-008..009`, Field Items, Pickup and Held Items are not upgraded.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run, no ROM/log/output artefacts and no private artefact documentation.

# Session State Update - 2026-05-15 - Shop Items Random reload smoke

- Branch: `test/upr-fvx-cfru-dpe-shop-items-random-reload-smoke`.
- Workspace PR #169 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/125_shop_items_random_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Shop-only `FVX-ITEM-006 Shop Items Random` Write/Reload-Smoke.
- Sanitized result: `candidateFilesChecked=3`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`.
- Shop reload stayed stable: `shopCountBefore=23`, `shopCountAfter=23`, `shopCountReload=23`, `shopItemsTotalBefore=157`, `shopItemsTotalAfter=157`, `shopItemsTotalReload=157`, `shopItemReloadMismatches=0`, `shopLengthMismatchesAfter=0`, `shopLengthMismatchesReload=0`.
- Preserve/scope result: `skippedShopItemMismatchesAfter=0`, `skippedShopItemMismatchesReload=0`, `specialShopPolicyMismatches=0`, `priceTableTouched=false`, `priceReloadMismatches=0`, `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`.
- Pool result: active no-ban/no-TM Shop Random pool `allowedShopItemPoolSize=536`; comparison non-bad pool `nonBadShopItemPoolSize=485`; invalid/unloaded/fallback/placeholder writes all `0`.
- `FVX-ITEM-006 Shop Items Random` is now `GUI-kompatibel` in the tested Shop-only scope. `FVX-ITEM-007..009`, Field Items, Pickup and Held Items are not upgraded by this block.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Shop Items Shuffle reload smoke

- Branch: `test/upr-fvx-cfru-dpe-shop-items-shuffle-reload-smoke`.
- Workspace PR #168 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/124_shop_items_shuffle_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Shop-only `FVX-ITEM-005 Shop Items Shuffle` Write/Reload-Smoke.
- Sanitized result: `candidateFilesChecked=3`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`.
- Shop reload stayed stable: `shopCountBefore=23`, `shopCountAfter=23`, `shopCountReload=23`, `shopItemsTotalBefore=157`, `shopItemsTotalAfter=157`, `shopItemsTotalReload=157`, `shopItemReloadMismatches=0`, `shopLengthMismatchesAfter=0`, `shopLengthMismatchesReload=0`.
- Preserve/scope result: `skippedShopItemMismatchesAfter=0`, `skippedShopItemMismatchesReload=0`, `specialShopPolicyMismatches=0`, `priceTableTouched=false`, `priceReloadMismatches=0`, `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`.
- `FVX-ITEM-005 Shop Items Shuffle` is now `GUI-kompatibel` in the tested Shop-only scope. `FVX-ITEM-006..009`, Field Items, Pickup and Held Items are not upgraded by this block.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Shop Items candidate diagnostics

- Branch: `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-candidate`.
- Workspace PR #167 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/123_shop_items_scope_diagnostics_candidate.md`.
- An explicitly approved local CFRU/DPE Gen9-BPRE candidate source was used read-only for Shop diagnostics only; no private paths, ROM names, hashes, pointers, offsets, raw bytes or script data are documented.
- Sanitized result: `candidateFilesChecked=3`, `candidateLoaded=true`, `shopScanSuccessful=true`, `shopCount=23`, `mainGameShopCount=3`, `skippedShopCount=20`, `specialShopCount=3`, `emptyShopCount=0`, `shopItemsTotal=157`, `minShopLength=2`, `maxShopLength=9`.
- Structure/safety result: `terminatorModelStable=true`, `shopLengthMismatch=0`, `invalidShopItemIds=0`, `unloadedShopItemIds=0`, `fallbackShopItems=0`, `placeholderShopItems=0`, `badShopItems=36`, `tmShopItems=6`.
- Scope result: `shopPointerModelObserved=true`, `dataRewriterOrRepointingRisk=true`, `skipShopsPreserved=true`, `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`, `priceTableTouched=false`, `priceTableReadable=true`, `exceptionClass=none`, `stacktrace=none`.
- `FVX-ITEM-005..009` are not upgraded. Diagnose 123 only clears the prerequisite for a Shop-only Shuffle smoke. No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer write/save and no committed artefacts.

# Session State Update - 2026-05-15 - Shop Items scope diagnostics preflight

- Branch: `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics`.
- Workspace PR #166 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/122_shop_items_scope_diagnostics.md`.
- No explicitly approved local CFRU/DPE Gen9-BPRE candidate source was provided for this block; no private search was expanded and no ROM was touched.
- Result is blocked/preflight: `candidateFilesChecked=0`, `candidateLoaded=false`, `shopScanSuccessful=false`; Shop counts, lengths, terminator stability and item-safety counters remain `not_available`.
- Read-only codepath review keeps `shopPointerModelObserved=true` and `dataRewriterOrRepointingRisk=true` because Gen3 Shops use `ShopPointerOffsets`, `MainGameShops`, `SkipShops`, `Shop` and `DataRewriter<Shop>` in `Gen3RomHandler.setShops(...)`.
- `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`, `priceTableTouched=false`. No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer write/save and no private artefact documentation.

# Session State Update - 2026-05-15 - Shop Items scope diagnostics plan

- Branch: `analysis/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-plan`.
- Workspace PR #165 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/121_shop_items_scope_diagnostics_plan.md`.
- Shops are confirmed as the next separate CFRU/DPE Gen9-BPRE Item writer scope after Field Items and Pickup.
- Feature IDs stay separated: `FVX-ITEM-005` Shop Items Shuffle, `FVX-ITEM-006` Shop Items Random, `FVX-ITEM-007` Shop Item Bans, `FVX-ITEM-008` Guarantee Evolution/X Items and `FVX-ITEM-009` Balance Shop Prices / Cheap Rare Candies.
- Read-only UPR-FVX analysis identifies `Settings.ShopItemsMod`, `GameRandomizer.maybeRandomizeShops()`, `ItemRandomizer.shuffleShopItems()`, `randomizeShopItems()`, `addCheapRareCandiesToShops()`, `RomHandler.getShops()`/`setShops(...)`, `getShopPrices()`/`setShopPrices(...)`, `Gen3RomHandler` and `Shop` as the relevant paths.
- `Gen3RomHandler.setShops(...)` uses `DataRewriter<Shop>` and can repoint terminated Shop item lists, so later diagnostics must measure pointers, terminators, lengths, skipped/special/main-game policy and price writes separately.
- No Field Items, Pickup or Held Items are upgraded by this plan. No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run and no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items Random Ban Bad reload smoke

- Branch: `test/upr-fvx-cfru-dpe-pickup-items-random-ban-bad-reload-smoke`.
- Workspace PR #164 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/120_pickup_items_random_ban_bad_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Pickup-only `FVX-ITEM-010 Pickup Items Random` smoke with `banBadRandomPickupItems=true`.
- Sanitized result: `candidateFilesChecked=101`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`.
- Pickup reload stayed stable: `pickupItemsTotalBefore=16`, `pickupItemsTotalAfter=16`, `pickupItemsTotalReload=16`, `pickupItemReloadMismatches=0`, `pickupTableLengthMismatches=0`, `pickupProbabilityMismatches=0`, `pickupReloadLocatorRegression=false`.
- Ban-Bad result: `badPickupItemWrites=0`, `pickupBadItemPoolCandidates=51`, `pickupBadItemPoolExcluded=51`, `pickupPoolNonBadSize=485`.
- `FVX-ITEM-010 Pickup Items Random / Ban Bad Items` is now `GUI-kompatibel` in the tested Pickup-only scope. Field Items, Shops and Held Items remain separate scopes and are not upgraded by this block.
- No code changes, no `02_external/**` changes, no submodule pin change, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items Ban Bad scope plan

- Branch: `analysis/upr-fvx-cfru-dpe-pickup-items-ban-bad-scope-plan`.
- UPR-FVX PR #38 and Workspace PR #163 were verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/119_pickup_items_ban_bad_scope_plan.md`.
- Read-only UPR-FVX analysis confirms `banBadRandomPickupItems=true` only switches the Pickup candidate pool from `getAllowedItems()` to `getNonBadItems()` inside `ItemRandomizer.randomizePickupItems()`.
- Baseline from 115/118 remains valid: Pickup table count `16`, entry size `4`, probability slots `10`, allowed pool `536`, non-bad pool `485`, bad pool candidates `51`, TMs allowed for Pickup because `canTMsBeHeld=true` and `isTMsReusable=false`.
- Recommendation: run a direct Pickup-only Random Ban-Bad reload smoke next; no code fix is planned before that smoke.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run, no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items reload locator fix

- Branch: `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- Workspace PR #162 was verified as merged before branch creation.
- UPR-FVX fix commit: `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- UPR-FVX PR #38 opened: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/38>.
- Workspace now pins `02_external/upr-fvx` to `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/118_pickup_items_reload_locator_fix.md`.
- Fix is limited to `Gen3RomHandler` Pickup table localization: classic `PickupTableStartLocator` remains first path; CFRU/DPE Gen9-BPRE gets a metadata fallback that ignores randomized item-ID words and requires exactly one table candidate.
- Sanitized Pickup-only Random smoke with `banBadRandomPickupItems=false` passed: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `pickupLocatorSuccessful=true`, `pickupItemsTotalReload=16`, `pickupItemReloadMismatches=0`, `pickupLocatorMode=stable-metadata`, `pickupContentLocatorUsed=false`, `pickupReloadLocatorRegression=false`.
- `FVX-ITEM-010 Pickup Items Random` is GUI-compatible only for `banBadRandomPickupItems=false`; Pickup Ban Bad remains separate.
- No Field Items, Shops, Held Items, TM/HM/Tutor/Learnset, Scriptparser, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution or Text/Menu work was done.

# Session State Update - 2026-05-15 - Pickup Items reload locator blocker plan

- Branch: `analysis/upr-fvx-cfru-dpe-pickup-items-reload-locator-blocker-plan`.
- Workspace PR #161 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- New protocol: `08_tests/randomizer/117_pickup_items_reload_locator_blocker_plan.md`.
- Read-only UPR-FVX analysis narrows the Pickup Random reload blocker to table localization, not to the direct item write: `getPickupItems()` finds `PickupTableStartLocator` by content pattern and caches the offset only within the handler instance; `setPickupItems(...)` then changes the item ID words that are part of that pattern.
- This explains Diagnose 116: same-handler `pickupItemsTotalAfter=16`, but fresh reload has no cache and reports `pickupLocatorSuccessful=false` / `pickupItemsTotalReload=0`.
- Recommended next branch: `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- Pickup Ban Bad remains blocked until Pickup Random without Ban Bad is reload-stable.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run, no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items Random reload smoke blocked

- Branch: `test/upr-fvx-cfru-dpe-pickup-items-random-reload-smoke`.
- Workspace PR #160 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- New protocol: `08_tests/randomizer/116_pickup_items_random_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Pickup-only `FVX-ITEM-010 Pickup Items Random` smoke with `banBadRandomPickupItems=false`.
- Sanitized result: `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`.
- Blocker: after write, fresh reload cannot locate the Pickup table: `pickupLocatorSuccessful=false`, `pickupItemsTotalReload=0`, `pickupItemReloadMismatches=16`, `pickupTableLengthMismatches=1`, `pickupProbabilityMismatches=16`.
- Direct write-scope safety remained clean: `pickupItemsTotalBefore=16`, `pickupItemsTotalAfter=16`, `invalidPickupItemWrites=0`, `unloadedPickupItemWrites=0`, `fallbackPickupItemWrites=0`, `placeholderPickupItemWrites=0`, `fieldItemScopeChanged=false`, `shopItemScopeChanged=false`, `heldItemScopeChanged=false`.
- `FVX-ITEM-010` remains `Write modelliert` / reload-blocked. Pickup Ban Bad remains untested.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items scope diagnostics

- Branch: `test/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics`.
- Workspace PR #159 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- New protocol: `08_tests/randomizer/115_pickup_items_scope_diagnostics.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was scanned read-only for Pickup Items only.
- Sanitized result: `candidateFilesChecked=97`, `candidateLoaded=true`, `pickupScanSuccessful=true`, `pickupLocatorSuccessful=true`, `pickupItemsTotal=16`, `pickupExpectedCount=16`, `pickupEntrySize=4`, `pickupProbabilitySlots=10`, `pickupProbabilityModelStable=true`, `pickupTableLengthMismatch=0`, `pickupLocatorCandidateCount=1`.
- Item safety result: `pickupInvalidItemIds=0`, `pickupUnloadedItemIds=0`, `pickupFallbackItems=0`, `pickupPlaceholderItems=0`, `pickupBadItems=7`, `pickupTmItems=1`.
- Pool result: `pickupPoolAllowedSize=536`, `pickupPoolNonBadSize=485`, `pickupBadItemPoolCandidates=51`, `pickupBadItemPoolExcluded=51`, `pickupTmPoolPolicy=tms allowed`, `canTMsBeHeld=true`, `isTMsReusable=false`.
- Recommendation: run a Pickup-only Random write/reload smoke without Ban Bad first; keep Ban Bad separate afterwards.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer write/save, no Output-ROM committed, no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items diagnostics scope plan

- Branch: `analysis/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics-plan`.
- Workspace PR #158 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- New protocol: `08_tests/randomizer/114_pickup_items_scope_diagnostics_plan.md`.
- Pickup was split as the next separate Item writer scope after Field Items.
- Read-only UPR-FVX analysis identifies the active paths: `Settings.PickupItemsMod`, `GameRandomizer.maybeRandomizePickupItems()`, `ItemRandomizer.randomizePickupItems()`, `Gen3RomHandler.getPickupItems()` and `setPickupItems(...)`, plus `PickupItem.PROBABILITY_SLOTS=10`.
- Plan result: do a Pickup-only read-only candidate diagnostic before any write smoke, because `PickupTableStartLocator`, `PickupItemCount`, table length, Common/Rare/probability semantics and Item-ID pool safety must be confirmed for CFRU/DPE Gen9-BPRE.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run, no ROM/output/log/private artefact documentation.

# Session State Update - 2026-05-15 - Field Items Random Even Ban Bad reload smoke

- Branch: `test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke`.
- Workspace PR #157 was verified as merged before branch creation.
- UPR-FVX pin confirmed: `02_external/upr-fvx` at `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- New protocol: `08_tests/randomizer/113_field_items_random_even_ban_bad_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-003 Field Items Random even distribution` smoke with `banBadRandomFieldItems=true`.
- Sanitized result: `candidateFilesChecked=9`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`.
- Field-Items scope stayed stable: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`, visible/hidden mismatches `0`, TM/Non-TM slot mismatches `0`, `requiredFieldTMMissingAfter=0`.
- Ban-Bad result: `badFieldItemWrites=0`, `badFieldItemPoolCandidates=47`, `badFieldItemPoolExcluded=47`, `nonBadFieldItemPoolSize=485`.
- Random-Even result: `randomEvenQueueUsed=true`, `randomEvenTmDistributionStable=true`, `randomEvenNonTmDistributionStable=true`, `nonBadFieldItemQueueRefills=0`.
- `FVX-ITEM-004` is now `GUI-kompatibel` for Field Items Random and Random Even. Shops, Pickup and Held Items remain separate scopes and are not upgraded.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Field Items API TM-slot scope fix

- UPR-FVX fix commit: `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- UPR-FVX PR #37 opened: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/37>.
- New protocol: `08_tests/randomizer/108_field_items_api_tm_slot_scope_fix.md`.
- Fix is limited to Gen3RomHandler Field-Items get/set: CFRU/DPE Field-TM slots are exposed through the Field-Items API while TMs are not made globally allowed.
- `./gradlew :random:classes` passed in UPR-FVX.
- No fachlicher ROM Write-/Reload-Smoke ran in this block; `FVX-ITEM-002` remains `Write modelliert` until a separate sanitized reload smoke passes.
- Workspace now pins `02_external/upr-fvx` to `328e4441c2981d37aba9e2707a6f27f779b026e2`.

# Session State Update - 2026-05-15 - Field Items Random API TM-slot scope plan

- New protocol: `08_tests/randomizer/107_field_items_random_api_tm_slot_scope_plan.md`.
- Read-only UPR-FVX analysis confirms the active `FVX-ITEM-002` blocker is not the PR #36 TM-filler pool anymore: raw Field-Item diagnostics see `tmFieldItemSlots=28`, while `Gen3RomHandler.getFieldItems()` exposes `0` TM slots because the Field-Items API only includes slots whose current item is `isAllowed()`.
- TMs are loaded and classified as TMs, but the existing allowed-slot API scope filters them before `ItemRandomizer.randomizeTMFieldItems(...)`.
- `FVX-ITEM-001` remains `GUI-kompatibel`; `FVX-ITEM-002` remains `Write modelliert` until a CFRU/DPE-gated API TM-slot scope fix and reload smoke pass; `FVX-ITEM-003` and `FVX-ITEM-004` remain `Write modelliert`.

# Session State Update - 2026-05-15 - Field Items Random TM-pool reload smoke blocked

- Branch: `test/upr-fvx-cfru-dpe-field-items-random-tm-pool-reload-smoke`.
- UPR-FVX PR #36 and Workspace PR #150 were verified as merged before branch creation.
- Workspace pin confirmed: `02_external/upr-fvx` at `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd`.
- New protocol: `08_tests/randomizer/106_field_items_random_tm_pool_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-002 Field Items Random` smoke with `banBadRandomFieldItems=false`.
- Result remains blocked before output/reload: `saveSuccessful=false`, `outputRomExists=false`, `reloadSuccessful=false`, `exceptionClass=com.uprfvx.random.exceptions.RandomizationException`.
- The PR #36 pool deficit is no longer the active blocker: `randomTmUniquePoolSize=50`, `randomTmFillerAvailable=26`, `randomTmPoolDeficit=0`.
- New blocker: API TM-slot scope mismatch. Raw diagnostics established `tmFieldItemSlots=28`, but the Randomizer API path sees `randomTmNeededSlots=0` / `randomTmCurrentSlots=0`, so Required Field TMs (`24`) exceed visible TM slots.
- `FVX-ITEM-002` remains `Write modelliert`; no GUI-compatible upgrade.

# Session State Update - 2026-05-15 - Field Items Random TM-pool fix

- Branch: `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix`.
- Workspace PR #149 was verified as merged before branch creation.
- UPR-FVX fix commit: `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd`.
- UPR-FVX PR #36 opened: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/36>.
- New protocol: `08_tests/randomizer/105_field_items_random_tm_pool_fix.md`.
- Fix is limited to `ItemRandomizer.randomizeTMFieldItems(...)`: Required Field TMs stay mandatory, the filler pool is deduplicated from loaded TM items plus current Field-TM slots, and pool deficits now fail with a clear `RandomizationException`.
- No ROM Write-/Reload-Smoke was executed in this block; `FVX-ITEM-002` is not upgraded until a separate sanitized Field-Items-only reload smoke passes.
- Workspace now pins `02_external/upr-fvx` to `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd`.
- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Scriptparser, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution or Text/Menu work was done.

# Session State Update - 2026-05-15 - Field Items Random TM-pool blocker plan

- Branch: `analysis/upr-fvx-cfru-dpe-field-items-random-tm-pool-blocker-plan`.
- Workspace PR #148 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/104_field_items_random_tm_pool_blocker_plan.md`.
- Read-only analysis confirms the likely blocker for `FVX-ITEM-002 Field Items Random`: `ItemRandomizer.randomizeTMFieldItems(...)` requires the generated unique TM set size to exactly match the current TM Field Item slot count and throws `RandomizationException` otherwise.
- Relevant data: `tmFieldItemSlots=28`, `requiredFieldTMsTotal=24`, `requiredFieldTMPresent=24`, `requiredFieldTMMissing=0`; Diagnose 103 failed before output/reload but preserve counters stayed stable.
- `FVX-ITEM-001` remains `GUI-kompatibel`; `FVX-ITEM-002`, `FVX-ITEM-003`, and `FVX-ITEM-004` remain `Write modelliert`.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run, no private artefact documentation.

# Session State Update - 2026-05-15 - Field Items Random reload smoke blocked

- Branch: `test/upr-fvx-cfru-dpe-field-items-random-reload-smoke`.
- Workspace PR #147 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/103_field_items_random_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=false`.
- Sanitized result: `candidateFilesChecked=9`, `candidateLoaded=true`, `smokeExecuted=true`, but `saveSuccessful=false`, `outputRomExists=false`, `reloadSuccessful=false`, `exceptionClass=com.uprfvx.random.exceptions.RandomizationException`, `stacktrace=com.uprfvx.random.exceptions.RandomizationException`.
- Field-Items scope remained stable until abort: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `requiredFieldTMMissingAfter=0`, `disallowedFieldItemWrites=0`, `scriptPatternExpansion=0`, `badFieldItemWrites=0`.
- `FVX-ITEM-001` remains `GUI-kompatibel` for the narrow Shuffle scope; `FVX-ITEM-002` remains `Write modelliert` and blocked by the Random TM-pool path; `FVX-ITEM-003` and `FVX-ITEM-004` remain `Write modelliert`.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Field Items allowed-slot reload smoke

- Branch: `test/upr-fvx-cfru-dpe-field-items-allowed-slot-reload-smoke`.
- Workspace PR #146 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/102_field_items_allowed_slot_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-001 Field Items Shuffle` Write-/Reload-Smoke.
- Sanitized result: `candidateFilesChecked=94`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`, `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`, visible/hidden reload mismatches `0`, TM/Non-TM slot mismatches `0`, `requiredFieldTMMissingAfter=0`, `disallowedFieldItemWrites=0`, `scriptPatternExpansion=0`, `exceptionClass=none`, `stacktrace=none`.
- `FVX-ITEM-001` is now `GUI-kompatibel` for the tested narrow Shuffle scope.
- `FVX-ITEM-002`, `FVX-ITEM-003` and `FVX-ITEM-004` remain `Write modelliert` pending separate Random / Random Even / Ban Bad Items smokes.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-14 - Field Items allowed-slot guard decision

- Branch: `compat/upr-fvx-cfru-dpe-field-items-allowed-slot-write-guard`.
- Workspace PR #145 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/101_field_items_allowed_slot_write_guard.md`.
- UPR-FVX remains pinned to `2697511da9a97df4c29c00dfda8b40e556020489`; no UPR-FVX code change or submodule pin change was needed.
- Guard decision: existing `Gen3RomHandler.getFieldItems()` / `setFieldItems(...)` already restricts writes to allowed Field-Item slots and preserves disallowed/progression/key/system/pattern-unmatched slots.
- No Write-/Reload-Smoke ran in this block because no local CFRU/DPE Gen9-BPRE candidate was explicitly approved for this write block.
- `FVX-ITEM-001..004` remain `Write modelliert` pending a separate Field-Items-only Write-/Reload-Smoke, preferably starting with `FVX-ITEM-001 Field Items Shuffle`.
- No code changes, no `02_external/**` changes, no Randomizer write/save, no build, no output ROM, no private artefact documentation.

# Session State Update - 2026-05-14 - Field Items candidate diagnostics

- Branch: `test/upr-fvx-cfru-dpe-field-items-scope-diagnostics-candidate`.
- Workspace PR #144 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/100_field_items_scope_diagnostics_candidate.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was scanned read-only for Field Items only.
- Sanitized result: `candidateFilesChecked=94`, `candidateLoaded=true`, `fieldItemScanSuccessful=true`, `fieldItemsTotal=339`, `visibleFieldItemSlots=168`, `hiddenFieldItemSlots=171`, `allowedFieldItemSlots=280`, `disallowedFieldItemSlots=59`, `tmFieldItemSlots=28`, `nonTmFieldItemSlots=311`, `requiredFieldTMMissing=0`, `invalidFieldItemIds=0`, `unloadedFieldItemIds=0`, `scriptPatternUnmatchedItemBalls=10`, `exceptionClass=none`, `stacktrace=none`.
- No code changes, no `02_external/**` changes, no Randomizer write/save, no build, no output ROM, no private artefact documentation.
- `FVX-ITEM-001..004` remain `Write modelliert`; next recommended block is a guarded Field-Items write/smoke branch.

# Session State Update - 2026-05-14 - Field Items diagnostics blocked

- Branch: `test/upr-fvx-cfru-dpe-field-items-scope-diagnostics`.
- Workspace PR #143 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/099_field_items_scope_diagnostics.md`.
- Field-Items-only diagnostics did not run because no explicitly approved local CFRU/DPE Gen9-BPRE candidate was provided in this block.
- Sanitized preflight: `candidateFilesChecked=0`, `candidateLoaded=false`, `fieldItemScanSuccessful=false`, `exceptionClass=none`, `stacktrace=none`.
- No code changes, no `02_external/**` changes, no Randomizer write/save, no build, no output ROM, no ROM/private artefact documentation.
- `FVX-ITEM-001..004` remain `Write modelliert`.
- Planned next block when a candidate is explicitly approved: `test/upr-fvx-cfru-dpe-field-items-scope-diagnostics-candidate`.

# Session State Update - 2026-05-14 - Field Items diagnostics scope plan

- Branch: `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`.
- New protocol: `08_tests/randomizer/098_field_items_scope_diagnostics_plan.md`.
- Field Items were split from the combined Field Items / Shops / Pickup planning track as the first dedicated item-writer diagnostic scope.
- Scope remains read-only: no code changes, no `02_external/**` changes, no Randomizer run, no build, no ROM or private artefact documentation.
- Planned next block: `test/upr-fvx-cfru-dpe-field-items-scope-diagnostics` for an aggregated Field-Items-only diagnostic run.

## 2026-05-14 - CFRU/DPE Field Items / Shops / Pickup Scope Plan

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/097_field_items_shops_pickup_scope_plan.md` erstellt.
- UPR-FVX bleibt auf `2697511da9a97df4c29c00dfda8b40e556020489` gepinnt.
- Palette Diagnose 096 bleibt blockiert abgeschlossen; `FVX-GFX-001..004` bleiben `Write modelliert`.
- Field Items, Shops und Pickup wurden gegen `GameRandomizer`, `Settings`, `ItemRandomizer`, `Gen3RomHandler`, `RomHandler`, `Shop`, `PickupItem`, `Item` und GUI-Texte read-only getrennt.
- Ergebnis: kein gemeinsamer Fixblock. Field Items sind Map-/Script-/Hidden-Item-Offset-Writer, Pickup ist ein begrenzter Table-Writer, Shops sind Terminator-/DataRewriter-/Repointing- und Preis-Scope.
- Gemeinsame Item-Pool-/Bad-/Banned-Policy ist noetig, aber die Write-/Reload-Risiken muessen getrennt bleiben.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build, kein Randomizer-Lauf und kein ROM-/Artefaktzugriff.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`: Field Items zuerst read-only planen/diagnostizieren; Shops und Pickup separat halten.

## 2026-05-14 - Post-Merge Sync nach blockiertem Palette Normal Single-owner Reload-Smoke

Workspace-Branch: `docs/post-merge-palette-normal-smoke-blocked-sync`

Post-Merge-Stand:

- UPR-FVX PR #35 ist gemerged.
- Workspace PR #139 ist gemerged.
- Workspace PR #140 ist gemerged.
- Workspace pinnt `02_external/upr-fvx` weiter auf `2697511da9a97df4c29c00dfda8b40e556020489`.
- Diagnose 096 ist auf `main` verfuegbar und als blockierter Reload-Smoke abgeschlossen.

Diagnose 096 bleibt blockiert:

- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- `candidateSpeciesTotal=0`
- kein fachlicher Palette-Write-/Reload-Smoke
- keine Hochstufung fuer `FVX-GFX-001`

Feature-Status:

- `FVX-GFX-001` bleibt `Write modelliert`: Guard-Fix vorhanden, Reload-Smoke blockiert bis ein UPR-FVX-ladbarer CFRU/DPE Gen9-BPRE-Kandidat mit `candidateSpeciesTotal=1439` verfuegbar ist.
- `FVX-GFX-002` bleibt `Write modelliert`.
- `FVX-GFX-003` bleibt `Write modelliert`.
- `FVX-GFX-004` bleibt `Write modelliert`.

Naechster empfohlener P1-Block:

- `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan`

Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build, kein Randomizer-Lauf und kein ROM-/Artefaktzugriff.

## 2026-05-14 - Palette Normal Single-owner Reload-Smoke blockiert

Arbeitsbranch: `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`

Diagnose 096 wurde als sanitisiert blockierter Reload-Smoke dokumentiert. Der lokale Preflight fand 94 BPRE-Kandidaten, aber keinen UPR-FVX-ladbaren CFRU/DPE-Gen9-BPRE-Zielkandidaten mit `candidateSpeciesTotal=1439`.

Aggregierte Zähler:

- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- `exceptionClass=none`
- `stacktrace=none`

Es wurde kein fachlicher Palette-Write-/Reload-Smoke ausgeführt. `FVX-GFX-001` wird nicht hochgestuft; `FVX-GFX-001..004` bleiben im Palette-Bereich konservativ bewertet. UPR-FVX bleibt auf `2697511da9a97df4c29c00dfda8b40e556020489` gepinnt.

# Session State

# Session State Update - 2026-05-15 - Field Items Random Ban Bad reload smoke

- New protocol: `08_tests/randomizer/112_field_items_random_ban_bad_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=true` on UPR-FVX `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Save/log/output/reload succeeded with `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, and `fieldItemReloadMismatches=0`.
- Required Field TMs remained complete, TM/Non-TM slot mismatches stayed `0`, `badFieldItemWrites=0`, and no Shop/Pickup/Held-Item scope change was observed.
- The smoke measured `badFieldItemPoolCandidates=47` and `badFieldItemPoolExcluded=47`, not the 75er baseline expected by Diagnose 111; therefore `FVX-ITEM-004` is only tested for `FieldItemsMod.RANDOM`, not fully GUI-compatible.
- Recommended next block: `test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke`.


# Session State Update - 2026-05-15 - Field Items Ban Bad scope plan

- New protocol: `08_tests/randomizer/111_field_items_ban_bad_scope_plan.md`.
- Read-only UPR-FVX analysis confirms `banBadRandomFieldItems` affects only `ItemRandomizer.randomizeNonTMFieldItems(...)`: it switches the Non-TM pool from `getAllowedItems()` to `getNonBadItems()` and removes TMs afterward.
- `randomizeTMFieldItems(...)` does not read `banBadRandomFieldItems`; Required Field TMs remain a separate TM-pool requirement.
- Diagnose 100 provides the key Ban-Bad baseline: `badFieldItems=75`, `badItemBanCandidates=75`, `badItemBanRemovalsNeeded=75`.
- Recommended first smoke: `test/upr-fvx-cfru-dpe-field-items-random-ban-bad-reload-smoke` for `FVX-ITEM-002 Field Items Random` with `banBadRandomFieldItems=true`; Random Even + Ban Bad stays separate afterward.
- `FVX-ITEM-004` remains `Write modelliert`; no code change, no Randomizer run, no build, no `02_external/**` change and no private artifact documentation.

# Session State Update - 2026-05-15 - Field Items Random Even reload smoke

- New protocol: `08_tests/randomizer/110_field_items_random_even_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-003 Field Items Random even distribution` Write-/Reload-Smoke with `banBadRandomFieldItems=false` on UPR-FVX `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Save/log/output/reload succeeded. Field Items remained stable: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`.
- API TM-slot scope remains stable: `apiTmFieldItemSlots=28`, `rawTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`, `tmGloballyAllowedChanged=false`.
- Random-Even TM pool is stable: `randomTmNeededSlots=28`, `randomTmCurrentSlots=28`, `randomTmRequiredTotal=24`, `randomTmFillerNeeded=4`, `randomTmFillerAvailable=26`, `randomTmPoolDeficit=0`, `randomTmResultUniqueSize=28`.
- Preserve counters stayed stable: `disallowedFieldItemWrites=0`, `invalidFieldItemWrites=0`, `unloadedFieldItemWrites=0`, `fallbackFieldItemWrites=0`, `placeholderFieldItemWrites=0`, `scriptPatternExpansion=0`.
- `FVX-ITEM-003` is now `GUI-kompatibel` only for the narrow Field-Items Random-Even scope with `banBadRandomFieldItems=false`; `FVX-ITEM-004` Ban Bad Items remains `Write modelliert`.

# Session State Update - 2026-05-15 - Field Items API TM-slot reload smoke

- New protocol: `08_tests/randomizer/109_field_items_api_tm_slot_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=false` on UPR-FVX `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Save/log/output/reload succeeded. Field Items remained stable: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`.
- API TM-slot scope is confirmed: `apiTmFieldItemSlots=28`, `rawTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`, `tmGloballyAllowedChanged=false`.
- Random-TM pool is stable: `randomTmNeededSlots=28`, `randomTmCurrentSlots=28`, `randomTmRequiredTotal=24`, `randomTmFillerNeeded=4`, `randomTmFillerAvailable=26`, `randomTmPoolDeficit=0`, `randomTmResultUniqueSize=28`.
- Preserve counters stayed stable: `disallowedFieldItemWrites=0`, `invalidFieldItemWrites=0`, `unloadedFieldItemWrites=0`, `fallbackFieldItemWrites=0`, `placeholderFieldItemWrites=0`, `scriptPatternExpansion=0`.
- `FVX-ITEM-002` is now `GUI-kompatibel` only for the narrow Field-Items Random scope with `banBadRandomFieldItems=false`; `FVX-ITEM-003` Random Even and `FVX-ITEM-004` Ban Bad Items remain `Write modelliert`.

## 2026-05-14 - CFRU/DPE Palette Normal Single-owner Write Guard Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`

UPR-FVX-Pin: `2697511da9a97df4c29c00dfda8b40e556020489`

Aktueller Stand:

- UPR-FVX-Fix erstellt: `2697511da9a97df4c29c00dfda8b40e556020489`.
- UPR-FVX PR #35 geoeffnet: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/35`.
- Neues Diagnose-/Fixprotokoll `08_tests/randomizer/095_palette_normal_single_owner_write_guard_fix_diagnostics.md` erstellt.
- `Gen3RomHandler.savePokemonPalettes()` nutzt im CFRU/DPE-Gen9-BPRE-Gate nun einen Normal-only-Single-owner-Guard.
- Shiny-, Shared-, Missing-, Invalid-, Decode-failed-, Cross-kind-shared- und unsichere Forme-Faelle werden nicht an `rewriteCompressedPalette()` / `DataRewriter` uebergeben.
- Vanilla-/Nicht-CFRU-Palette-Pfade bleiben unveraendert.
- UPR-FVX Checks: `git diff --check` sauber, `./gradlew clean :random:jar` erfolgreich.
- `./gradlew test` beendet mit Gradle-Status 0, meldet aber bestehende Failures in `PlayerCharacterGraphicsTest` und `Gen1CmpTest`.
- Kein ROM-/Reload-Smoke wurde in diesem Block ausgefuehrt; `FVX-GFX-001` bleibt bis zu einem separaten Reload-Smoke `Write modelliert`.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit.

Naechster sinnvoller Schritt:

- `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`: den Normal-only-Single-owner-Palette-Guard mit einem sanitisierten Reload-Smoke fachlich bestaetigen. Erwartet: `normalPaletteWriteCandidates=385`, `normalPaletteWriteAttempts <= 385`, `normalPaletteReloadMismatches=0`, ausgeschlossene Kategorien mit `WriteAttempts=0`, `exceptionClass=none`, `stacktrace=none`.

## 2026-05-14 - CFRU/DPE Palette Single-owner Normal-only Fix-Scope Plan

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-palette-single-owner-normal-only-fix-scope-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/094_palette_single_owner_normal_only_fix_scope_plan.md` erstellt.
- Diagnose 093 bleibt die Datenbasis: `candidateWritablePalettes=385`, `candidateWritableNormalPalettes=385`, `candidateWritableShinyPalettes=0`, `skipPaletteEntries=2493`, `crossKindSharedPalettePointers=1809`.
- Planergebnis: ein spaeterer Fix-/Smoke-Scope ist reviewbar, aber nur fuer Normal-Paletten, die single-owner, dekomprimierbar, gueltig, nicht shared, nicht missing, nicht invalid, nicht decode-failed und nicht cross-kind shared sind.
- Shiny-, Shared-, Invalid-, Missing-, Decode-failed- und unsichere Forme-/Expanded-Mapping-Faelle bleiben preserve-only.
- Der bestehende komprimierte Palette-Writer laeuft ueber `rewriteCompressedPalette()`/`DataRewriter`; ein echter Write-Smoke muss Repointing entweder bewusst zulassen und nachweisen oder den Fix zurueckstellen.
- Fuer den ersten spaeteren Smoke ist nur `FVX-GFX-001 Pokemon Palettes Random` als Normal-only-Farbtraeger geeignet.
- `FVX-GFX-002 Follow Types` bleibt ein separater spaeterer Normal-only-Smoke ohne TypeChart-/Species-Type-Scope.
- `FVX-GFX-003 Follow Evolutions` und `FVX-GFX-004 Shiny From Normal` bleiben ausserhalb des ersten Fix-Smokes.
- `FVX-GFX-001..004` bleiben aktuell `Write modelliert`.
- Keine Codeaenderung, kein Build, kein Randomizer-Lauf, kein ROM-Zugriff, keine Submodule-Pin-Aenderung.

Naechster sinnvoller Schritt:

- `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`: engen UPR-FVX-Writer-Gate-Fix fuer sichere Normal-Palette-Single-owner-Kandidaten vorbereiten und mit sanitisiertem Reload-Smoke dokumentieren.

## 2026-05-14 - CFRU/DPE Palette Pointer / Compression Diagnostics Run

Workspace-Branch: `test/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neuer sanitiserter Diagnosebericht `08_tests/randomizer/093_palette_pointer_compression_diagnostics.md` erstellt.
- Der lokale Diagnose-Harness blieb ignored unter `05_builds/**` und wurde nicht committed.
- Der Lauf blieb read-only: keine Palette-Randomization, kein Writer-Fix, kein Repointing, kein Build, keine Output-ROM.
- Kandidaten-Preflight: `candidateFilesChecked=94`, `candidateLoaded=true`, `palettePointerScanSuccessful=true`, `candidateSpeciesTotal=1439`, `exceptionClass=none`, `stacktrace=none`.
- Pointer-/Compression-Ergebnis: `candidateWritablePalettes=385`, `candidateWritableNormalPalettes=385`, `candidateWritableShinyPalettes=0`.
- Skip-/Preserve-Scope: `skipPaletteEntries=2493`, `skippedSharedPalettes=329`, `skippedInvalidPalettes=592`, `skippedMissingPalettes=38`, `skippedDecodeFailedPalettes=625`.
- Risikobefund: `crossKindSharedPalettePointers=1809`, `sharedPointerGroups=775`, `largestSharedPointerGroupSize=156`, `singleOwnerBothNormalAndShinySpecies=0`.
- Ergebnis: ein spaeterer enger Fix-/Smoke-Scope ist nur normal-palette-only, single-owner/decompressible realistisch; Shiny und alle shared/invalid/missing/decode-failed Paletten bleiben preserve-only.
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`.
- Keine privaten Pfade, ROM-Namen, Hashes, Raw Pointer, Offsets, Logs oder Output-ROM-Pfade dokumentiert.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-palette-single-owner-normal-only-fix-scope-plan`: read-only planen, ob ein normal-palette-only Single-owner/decompressible Fix-/Smoke-Scope reviewbar eng genug ist. Shiny, shared, invalid, missing und decode-failed Paletten preserve-only lassen.

## 2026-05-14 - CFRU/DPE Palette Pointer / Compression Diagnostics Plan

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/092_palette_pointer_compression_diagnostics_plan.md` erstellt.
- Der Plan konkretisiert die von Diagnose 091 geforderte Palette-Pointer-/Compression-Diagnose.
- Relevante Codepfade: `Gen3RomHandler` mit `PokemonNormalPalettes`, `PokemonShinyPalettes`, `loadPokemonPalettes()`, `savePokemonPalettes()`, `rewriteCompressedPalette(...)`, `pokedexToInternal[...]`, `AbstractGBRomHandler.DataRewriter`, `GameRandomizer`, `Settings.PokemonPalettesMod` und `Gen3to5PaletteRandomizer`.
- Die spaetere Diagnose soll Normal-/Shiny-Palette-Pointer aggregiert klassifizieren: dekomprimierbar, nicht dekomprimierbar, single-owner, shared, missing/null, invalid/out-of-ROM, duplicate und candidateWritable.
- Raw Pointer, Offsets, ROM-Namen, Hashes, lokale Pfade, Logauszuege und Output-ROMs duerfen nicht dokumentiert werden.
- Policy: shared, missing, invalid und decode-failed Paletten bleiben preserve-only; nur dekomprimierbare single-owner Kandidaten kommen fuer einen spaeteren engen Fix-/Smoke-Scope in Frage.
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build, kein Randomizer-Lauf und kein ROM-/Artefaktzugriff.

Naechster sinnvoller Schritt:

- `test/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics`: nur bei expliziter lokaler Freigabe einen sanitisierten read-only Diagnose-Lauf fuer Palette-Pointer, Compression, Owner-Counts und sichere Kandidaten ausfuehren. Kein Palette-Fix, kein Repointing.

## 2026-05-14 - CFRU/DPE Palette Randomization Preserve/Repoint Plan

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/091_palette_randomization_preserve_repoint_plan.md` erstellt.
- Der Plan trennt bestehende Palette-Safety/Skip-Unchanged-Save von echter geaenderter `PokemonPalettesMod.RANDOM`-Randomization.
- Relevante Codepfade: `GameRandomizer.maybeRandomizePokemonPalettes()`, `Settings.PokemonPalettesMod`, `RandomizerGUI`, `Gen3to5PaletteRandomizer`, `Gen3RomHandler.loadPokemonPalettes()`, `savePokemonPalettes()`, `rewriteCompressedPalette()` und `AbstractGBRomHandler.DataRewriter`.
- Ergebnis: echte Palette-Randomization ist fuer CFRU/DPE ein komprimierter Repointing-/Shared-Pointer-Writer und noch nicht direkt fixbar.
- Belegte Safety bleibt: missing/invalid Paletten defensiv laden/skippen und unveraenderte Paletten beim Save nicht neu schreiben.
- Offene Risiken: compressed decode, FreeSpace/Repointing, Single-Pointer-Annahme, Shared-Palette-Pointer, fehlende/invalid Slots, Forme-/Alt-Species-Zuordnung und `pokedexToInternal`-Grafikpfad.
- Empfehlung: vor jedem Fix eine read-only Palette-Pointer-/Compression-Diagnose fuer dekomprimierbare, single-owner, shared, missing und invalid Normal-/Shiny-Paletten.
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build, kein Randomizer-Lauf und kein ROM-/Artefaktzugriff.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics-plan`: read-only Diagnoseplan fuer Palette-Pointer-Eigentum, Dekomprimierbarkeit, Shared-Pointer, missing/invalid Slots und moegliche spaetere single-owner Write-Grenzen.

## 2026-05-14 - Post-Merge-Doku-Sync nach blockiertem Move Names Retry

Workspace-Branch: `docs/post-merge-move-names-retry-blocked-sync`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Workspace PR #133 ist gemerged.
- Diagnose 090 ist als blockierter Retry abgeschlossen.
- `candidateFilesChecked=94`.
- `candidatePreflightSuccessful=false`.
- Es gab keinen fachlichen Name-only fixed-length Reload-Smoke, weil kein explizit freigegebener CFRU/DPE Gen9-BPRE-Kandidat mit `moves.total=992` und `991:PsychicNoise` verfuegbar war.
- `FVX-MOVE-005` wird nicht hochgestuft und bleibt `Write modelliert`.
- `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` und `FVX-MOVE-006` bleiben GUI-kompatibel.
- UPR-FVX PR #34 ist weiterhin als gemerged dokumentiert; der Workspace-Pin bleibt `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build und kein Randomizer-Lauf.

Naechster sinnvoller Schritt:

- P1-Arbeit auf `analysis/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint-plan` verschieben. `FVX-MOVE-005` bleibt wartend, bis ein explizit freigegebener 992-/`991:PsychicNoise`-Kandidat verfuegbar ist.

## 2026-05-14 - CFRU/DPE Move Names fixed-length Reload-Smoke Retry

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke-retry`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/090_move_names_fixed_length_reload_smoke_retry.md` erstellt.
- Ziel war ein erneuter enger Candidate-Preflight fuer `FVX-MOVE-005` Randomize Move Names im bestehenden Gen3 fixed-length `MoveNames`-Pfad.
- Das lokale Preflight pruefte freigegebene private/ignored Kandidaten, ohne private Pfade, ROM-Namen, Hashes, Logauszuege oder Output-ROMs zu dokumentieren.
- Ergebnis: `candidateFilesChecked=94`, `candidatePreflightSuccessful=false`, `candidateMovesTotal=not available`, `candidateHighestMove=not available`.
- Der fachliche Name-only Reload-Smoke wurde nicht ausgefuehrt, weil kein Kandidat die Mindestkriterien `moves.total=992` und `991:PsychicNoise` erfuellte.
- `saveSuccessful`, `logSuccessful`, Output-, Reload-, Name-Length-, Terminator-/Padding-, Description-Pointer- und Name-Reload-Zaehler bleiben daher nicht fachlich ausgewertet.
- Keine Move Descriptions, keine Pointer-/Repointing- oder Text/Menu-Umsetzung, keine MoveData-Byte-Writer-Aenderung.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build und kein Randomizer-Smoke nach blockiertem Preflight.
- `FVX-MOVE-005` wird nicht hochgestuft und bleibt `Write modelliert`; `FVX-MOVE-001/002/003/004/006` bleiben GUI-kompatibel.

Naechster sinnvoller Schritt:

- `FVX-MOVE-005` vorerst konservativ halten. Den Name-only fixed-length Smoke nur erneut starten, wenn ein lokal freigegebener CFRU/DPE Gen9-BPRE-Kandidat vorab eindeutig `moves.total=992` und `991:PsychicNoise` meldet; ansonsten keinen Smoke ausfuehren.

## 2026-05-14 - CFRU/DPE Move Names fixed-length Reload-Smoke

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/089_move_names_fixed_length_reload_smoke.md` erstellt.
- Ziel war ein enger Name-only Reload-Smoke fuer `FVX-MOVE-005` Randomize Move Names im bestehenden Gen3 fixed-length `MoveNames`-Pfad.
- Ein lokaler, nicht committeter Harness unter ignored `05_builds/**` wurde erstellt.
- Der fachliche Smoke konnte nicht ausgewertet werden, weil lokal kein freigegebener CFRU/DPE Gen9-BPRE-Kandidat mit `moves.total=992` und hoechstem Move `991:PsychicNoise` gefunden wurde.
- Ein automatisch gefundener erster Kandidat war kein CFRU/DPE-Gen9-Stand und wurde verworfen; danach fand die stumme Kandidatensuche keinen passenden 992-Move-Kandidaten.
- `saveSuccessful`, `logSuccessful`, Reload-, Name-Length-, Terminator-/Padding-, Description-Pointer- und Name-Reload-Zaehler bleiben daher nicht fachlich ausgewertet.
- Keine Move Descriptions, keine Pointer-/Repointing- oder Text/Menu-Umsetzung, keine MoveData-Byte-Writer-Aenderung.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build.
- `FVX-MOVE-005` wird nicht hochgestuft und bleibt `Write modelliert`; `FVX-MOVE-001/002/003/004/006` bleiben GUI-kompatibel.

Naechster sinnvoller Schritt:

- Den gleichen Name-only fixed-length Smoke erneut ausfuehren, sobald ein freigegebener lokaler CFRU/DPE Gen9-BPRE-ROM-Kandidat fuer den Smoke eindeutig verfuegbar ist. Scope unveraendert eng halten: keine Move Descriptions, kein Pointer-/Repointing, keine Text/Menu-Umsetzung.

## 2026-05-14 - CFRU/DPE Move Names / Descriptions Text/Menu-Scope Plan

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-move-names-text-menu-scope-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neuer read-only Planbericht `08_tests/randomizer/088_move_names_text_menu_scope_plan.md` erstellt.
- `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` und `FVX-MOVE-006` bleiben GUI-kompatibel.
- `FVX-MOVE-005` Randomize Move Names / Move Descriptions bleibt getrennt vom MoveData-Byte-Writer-Scope `+0..+11`.
- UPR-FVX-Codepfad: GUI/Settings aktivieren `randomizeMoveNames`, `GameRandomizer` ruft `MoveNameRandomizer.randomizeMoveNames()` auf, und `Gen3RomHandler.saveMoves()` schreibt `Move.name` ueber `writeFixedLengthString(...)` in die fixed-length Move-Namen-Tabelle.
- Fuer Gen3/CFRU/DPE ist der direkte Name-Writer kein Pointer-/Repointing-Pfad, sondern ein in-place fixed-length Textpfad mit `MoveNameLength` und sichtbarer `getMaxMoveNameLength() = 12`.
- Move Descriptions werden durch `FVX-MOVE-005` nicht als eigener Randomizer-Pfad geschrieben; sichtbare `MoveDescriptions`-Nutzung gehoert zu getrennten TM-/Item-Textpfaden.
- Planentscheidung: enger Name-only Reload-Smoke ist realistisch; Move Descriptions / Text/Menu-Repointing bleibt vorerst zurueckgestellt, bis ein eigener Description-/Pointer-Befund vorliegt.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Randomizer-Lauf, kein Build und kein ROM-/Artefaktzugriff.

Naechster sinnvoller Schritt:

- Separater Smoke-Branch `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke`: nur `FVX-MOVE-005` Name-only pruefen, Move-Descriptions nicht schreiben, keine Pointer-/Repointing- oder Text/Menu-Umsetzung.

## 2026-05-14 - CFRU/DPE MoveData Fairy-Type-Byte Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- UPR-FVX PR #34 ist gemerged.
- Workspace PR #129 ist gemerged.
- Diagnose 087 ist abgeschlossen und auf `main`.
- UPR-FVX-Fix `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3` erstellt.
- Der Fix bleibt auf `Gen3RomHandler` und das MoveData-Type-Byte `+2` begrenzt.
- Im sicheren CFRU/DPE-Gen9-BPRE-Gate liest `typeFromMoveData(...)` raw `0x17` als `Type.FAIRY`.
- Im selben Gate schreibt `moveDataTypeToByte(...)` `Type.FAIRY` als raw `0x17`.
- Vanilla-, Jambo- und andere Gen3-Pfade bleiben beim bestehenden Mapping.
- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/087_move_data_fairy_type_byte_fix_diagnostics.md` erstellt.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadMoveDataMismatches=0`, `moves.total=992`, hoechster Move `991:PsychicNoise`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`, `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`, `exceptionClass=none` und `stacktrace=none`.
- `typeByteMismatches=54` bleibt als Legacy-Mapping-Vergleich gegen `Gen3Constants.typeToByte(...)` sichtbar und ist in diesem Fix-Smoke kein CFRU/DPE-Reload-Fehler.
- `FVX-MOVE-004` Randomize Move Types ist damit GUI-kompatibel.
- `FVX-MOVE-005` Move Names/Descriptions bleibt ausserhalb dieses Scopes.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit.
- Keine TypeChart-/TypeEffectiveness-, Species-Type-, Stellar-/Typenmodell-, Name-, Description-, Palette-, Item-, Field-/Shop-/Pickup-, Trainer-, Wild-, Evolution-, Text/Menu-, Graphics-, TM/HM-, Tutor-, Egg- oder Learnset-Write-Aenderung.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`; private Pfade, ROM-Namen, Hashes, Logs und Output-ROMs wurden nicht dokumentiert.

Naechster sinnvoller Schritt:

- Separater Planungsbranch `analysis/upr-fvx-cfru-dpe-move-names-text-menu-scope-plan`: nur entscheiden und modellieren, ob `FVX-MOVE-005` Move Names / Move Descriptions als eigener Text/Menu-Scope machbar ist oder vorerst zurueckgestellt bleibt. Keine Umsetzung in diesem Sync-Block.

## 2026-05-14 - CFRU/DPE MoveData Types Reload-Smoke

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke`

UPR-FVX-Pin: `bb5ee11978e38839979e654ff1c14ba60a0cde93`

Aktueller Stand:

- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/086_move_data_types_reload_smoke.md` erstellt.
- Der Smoke blieb eng auf `FVX-MOVE-004` Randomize Move Types und das MoveData-Type-Byte `+2` begrenzt.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `moves.total=992`, hoechster Move `991:PsychicNoise`, `exceptionClass=none` und `stacktrace=none`.
- Der Smoke ist fachlich blockiert: `writeReloadMoveDataMismatches=54`, `typeReloadMismatches=54`, `expectedFairyMoves=54`, `fairyReloadMismatches=54` und `cfruDpeTypeByteMismatches=54`.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` blieben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
- Einordnung: Die aktuelle Gen3-MoveData-Type-Mappingfunktion schreibt `FAIRY` im MoveData-Pfad faktisch als Fallback `0x00`; fuer den getesteten CFRU/DPE Gen9-BPRE-Stand muss `FAIRY` im sicheren MoveData-Gate als raw `0x17` geschrieben werden.
- Dies ist kein TypeChart-/TypeEffectiveness-/Species-Type-Write-Befund.
- `FVX-MOVE-004` bleibt `Write modelliert`; `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003` und `FVX-MOVE-006` bleiben GUI-kompatibel.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`; private Pfade, ROM-Namen, Hashes, Logs und Output-ROMs wurden nicht dokumentiert.
- Keine Aenderung an `02_external/upr-fvx`; der Submodule-Pin bleibt `bb5ee11978e38839979e654ff1c14ba60a0cde93`.
- Keine TypeChart-/TypeEffectiveness-, Species-Type-, Name-, Description-, Palette-, Item-, Field-/Shop-/Pickup-, Trainer-, Wild-, Evolution-, Text/Menu-, Graphics-, TM/HM-, Tutor-, Egg- oder Learnset-Write-Aenderung.

Naechster sinnvoller Schritt:

- Enger UPR-FVX-Fixbranch `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`: im sicheren CFRU/DPE-Gen9-BPRE-MoveData-Writer-Gate `FAIRY` fuer Byte `+2 type` als raw `0x17` schreiben; Vanilla/Jambo/andere Gen3-Pfade sowie TypeChart/TypeEffectiveness/Species-Type-Write unveraendert lassen.

## 2026-05-14 - CFRU/DPE MoveData Power/Accuracy/PP Reload-Smoke

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke`

UPR-FVX-Pin: `bb5ee11978e38839979e654ff1c14ba60a0cde93`

Aktueller Stand:

- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/085_move_data_power_accuracy_pp_reload_smoke.md` erstellt.
- Der Smoke blieb eng auf MoveData Power / Accuracy / PP begrenzt.
- Aktiviert wurden nur `FVX-MOVE-001` Randomize Move Power, `FVX-MOVE-002` Randomize Move Accuracy und `FVX-MOVE-003` Randomize Move PP.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadMoveDataMismatches=0`, `moves.total=992`, hoechster Move `991:PsychicNoise`, `powerReloadMismatches=0`, `accuracyReloadMismatches=0`, `ppReloadMismatches=0`, `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`, `exceptionClass=none` und `stacktrace=none`.
- Rohbytes fuer `+1 power`, `+3 accuracy` und `+4 pp` reloadeten stabil: `powerByteMismatches=0`, `accuracyByteMismatches=0`, `ppByteMismatches=0`.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` blieben bytegleich.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`; private Pfade, ROM-Namen, Hashes, Logs und Output-ROMs wurden nicht dokumentiert.
- Keine Aenderung an `02_external/upr-fvx`; der Submodule-Pin bleibt `bb5ee11978e38839979e654ff1c14ba60a0cde93`.
- Keine Type-, Name-, Description-, Palette-, Item-, Field-/Shop-/Pickup-, TypeChart-/TypeEffectiveness-, Trainer-, Wild-, Evolution-, Text/Menu-, Graphics-, TM/HM-, Tutor-, Egg- oder Learnset-Write-Aenderung.

Naechster sinnvoller Schritt:

- Separater Folgebranch fuer `FVX-MOVE-004` Randomize Move Types. `FVX-MOVE-005` Move Names/Descriptions bleibt out of scope.

## 2026-05-14 - CFRU/DPE MoveData Write Preserve Reload-Smoke

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-data-write-preserve-reload-smoke`

UPR-FVX-Pin: `bb5ee11978e38839979e654ff1c14ba60a0cde93`

Aktueller Stand:

- Workspace PR #125 ist gemerged; Diagnose 084 ist abgeschlossen.
- UPR-FVX PR #33 und Workspace PR #124 sind gemerged; der Workspace bleibt auf `02_external/upr-fvx` Commit `bb5ee11978e38839979e654ff1c14ba60a0cde93` gepinnt.
- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/084_move_data_write_preserve_reload_smoke.md` erstellt.
- Der Smoke blieb eng auf MoveData / Update Moves und Preserve-Verhalten begrenzt.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadMoveDataMismatches=0`, `moves.total=992`, hoechster Move `991:PsychicNoise`, `categorySplitMismatches=0`, `categoryReloadMismatches=0`, `preserveByteMismatchesUnchangedMoves=0`, `exceptionClass=none` und `stacktrace=none`.
- Der Harness erzwang genau eine Category-Aenderung, weil `Update Moves` in diesem Stand keine Category-Aenderung erzeugte; damit wurde der CFRU/DPE-`BattleMove.split`-Write bei Byte `+10` konkret geprueft.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` blieben fuer unveraenderte Moves bytegleich.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`; private Pfade, ROM-Namen, Hashes, Logs und Output-ROMs wurden nicht dokumentiert.
- Keine Aenderung an `02_external/upr-fvx`; der Submodule-Pin bleibt `bb5ee11978e38839979e654ff1c14ba60a0cde93`.
- Keine Palette-, Item-, Field-/Shop-/Pickup-, TypeChart-/TypeEffectiveness-, Trainer-, Wild-, Evolution-, Text/Menu-, Graphics-, TM/HM-, Tutor-, Egg- oder Learnset-Write-Aenderung.

Naechster sinnvoller Schritt:

- Separater Folgebranch `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke` fuer GUI-nahe Reload-Smokes von `FVX-MOVE-001` Randomize Move Power, `FVX-MOVE-002` Randomize Move Accuracy und `FVX-MOVE-003` Randomize Move PP. `FVX-MOVE-004` Randomize Move Types danach separat halten; `FVX-MOVE-005` Move Names/Descriptions bleibt out of scope.

## 2026-05-14 - CFRU/DPE MoveData Write Preserve Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-move-data-write-preserve`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-move-data-write-preserve`

Aktueller Stand:

- UPR-FVX PR #33 und Workspace PR #124 sind gemerged.
- UPR-FVX-Fix `bb5ee11978e38839979e654ff1c14ba60a0cde93` erstellt.
- Der Fix bleibt auf `Gen3RomHandler.saveMoves()` begrenzt.
- Klassische MoveData-Felder werden weiter geschrieben: `+0 effect`, `+1 power`, `+2 type`, `+3 accuracy`, `+4 pp`.
- Im bestehenden CFRU/DPE-Gen9-BPRE-Gate wird zusaetzlich `BattleMove.split` bei Byte `+10` geschrieben: `PHYSICAL -> 0`, `SPECIAL -> 1`, `STATUS -> 2`.
- Nicht modellierte Bytes `+5 secondaryEffectChance`, `+6 target`, `+7 priority`, `+8 flags`, `+9 z_move_power` und `+11 z_move_effect` bleiben bytegleich erhalten.
- `./gradlew clean :random:jar` war erfolgreich.
- `./gradlew test` endete mit `BUILD SUCCESSFUL`, meldete aber bestehende Failures ausserhalb des MoveData-Scopes in `PlayerCharacterGraphicsTest` und `Gen1CmpTest`.
- Der lokale Randomizer-/ROM-Reload-Smoke wurde separat in Diagnose 084 ausgefuehrt und bestaetigt.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit und dokumentiert Diagnose 083.
- Keine Palette-, Item-, Field-/Shop-/Pickup-, TypeChart-/TypeEffectiveness-, Trainer-, Wild-, Evolution-, Text/Menu-, Graphics-, TM/HM-, Tutor-, Egg- oder Learnset-Write-Aenderung.

Naechster sinnvoller Schritt:

- Fix- und Reload-Smoke-PRs sind gemerged. Naechster MoveData-Schritt ist ein separater Power/Accuracy/PP-Reload-Smoke; Move Types und Move Names bleiben getrennt.

## 2026-05-14 - CFRU/DPE Evolution Similar Strength Normalized Reload Diagnostics

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-evolution-similar-strength-normalized-reload`

Aktueller Stand:

- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/082_evolution_similar_strength_normalized_reload_diagnostics.md` erstellt.
- Es wurde nur `FVX-TRAIT-018` Evolutions Similar Strength im Carrier `FVX-TRAIT-016` Evolution-Species-Writer lokal ausgefuehrt.
- Der Reload-Vergleich wurde auf persistierte Gen3-Evolution-Felder normalisiert: Evolution-Type, ExtraInfo mit Item-ID-Normalisierung und Ziel-Species per interner `SpeciesSet`-Identitaet.
- `Evolution.forme` wurde nicht als Mismatch-Kriterium gewertet.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `normalizedWriteReloadEvolutionMismatches=0`, `rawWithFormeWriteReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- `Bad Egg=true` bleibt nach 055 als bestehender Evolution-Log-/Sonder-Species-Marker klassifiziert, weil der normalisierte Reload stabil ist und der Mismatch-Zaehler `0` bleibt.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.
- `FVX-TRAIT-019`, Wild, Trainer, TypeChart, MoveData, Palette, Items, Text/Menu, Graphics und Evolution-Methoden-Writer blieben ausgeschlossen.

Naechster sinnvoller Schritt:

- PR fuer Diagnose 082 reviewen und mergen. Danach Evolution-Methoden-Writer und weitere Evolution-Suboptionen getrennt planen; fuer `FVX-TRAIT-018` ist in diesem engen Similar-Strength-Scope kein Fixbranch erforderlich.

## 2026-05-14 - CFRU/DPE Evolution Similar Strength Mismatch Diagnostics

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-evolution-similar-strength-mismatch-diagnostics`

Aktueller Stand:

- Neues read-only Code-/Protokollanalyse-Protokoll `08_tests/randomizer/081_p1_evolution_similar_strength_mismatch_diagnostics.md` erstellt.
- 081 untersucht den verbliebenen 070-Blocker `FVX-TRAIT-018` Evolutions Similar Strength im Carrier `FVX-TRAIT-016` Evolution-Species-Writer.
- Relevante Codepfade sind `EvolutionRandomizer.randomizeEvolutionsInner()`, `findPossibleReplacements(...)`, `prepareNewEvolution(...)`, `SpeciesSet.getRandomSimilarStrengthSpecies(...)`, `Gen3RomHandler.loadEvolutions()`, `writeEvolutions()` und `Evolution.toString()/equals(...)`.
- Wahrscheinlichste Einordnung: `writeReloadEvolutionMismatches=24` aus 070 ist eher ein zu breiter Diagnosevergleich auf nicht persistierte Forme-/Zusatzfelder als ein harter Evolution-Species-Write-Fehler.
- `prepareNewEvolution(...)` setzt `Evolution.forme`, aber der Gen3-Evolution-Write-/Reload-Pfad persistiert dieses Feld nicht; 026 definiert den Reload-Erfolg ueber persistierte Evolution-Felder und Ziel-Species per interner `SpeciesSet`-Identitaet.
- `Bad Egg=true` korreliert nicht zwingend mit den 070-Mismatches: 026 und 080 zeigen `Bad Egg` im Evolution-Scope bei `0` Reload-Mismatches.
- Der Same-Typing-Fix aus 080 bleibt getrennt; `FVX-TRAIT-018` nutzt den BST-/Similar-Strength-Pfad und nicht den Same-Typing-`hasSharedType(...)`-Guard.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater, eng freigegebener Diagnose-Smoke fuer `FVX-TRAIT-018` mit normalisiertem Reload-Vergleich auf persistierte Gen3-Evolution-Felder und interne Ziel-Species-Identitaet. `Evolution.forme` nicht als Mismatch-Kriterium werten; `Bad Egg` nach 055 separat klassifizieren.

## 2026-05-14 - CFRU/DPE Evolution Same Typing Null-Type Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`

Aktueller Stand:

- UPR-FVX-Fix `74d88a7ab1d306e1e09ccabb851dffd7f6922b66` erstellt.
- Der Fix bleibt auf `EvolutionRandomizer` begrenzt und behandelt Species mit `primaryType == null` defensiv im Evolutions-Same-Typing-Filter.
- `FVX-TRAIT-019` Evolutions Same Typing wurde lokal sanitisiert ausgefuehrt: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- `Bad Egg=true` bleibt nach 055 als bestehender Evolution-Log-/Sonder-Species-Marker klassifiziert, weil Save/Log/Output/Reload stabil sind und der Reload-Mismatch-Zaehler `0` ist.
- `FVX-TRAIT-018` Evolutions Similar Strength wurde nur getrennt als Regression ausgefuehrt und bleibt nicht mit dem Same-Typing-Fix vermischt.
- Neues Diagnoseprotokoll `08_tests/randomizer/080_evolution_same_typing_nulltype_fix_diagnostics.md` erstellt.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit und aktualisiert README, Session, Next Steps, Roadmap, Feature-Coverage und Tool-Manifest.
- Keine Wild-, Trainer-, TypeChart-, MoveData-, Palette-, Item-, Text/Menu-, Graphics- oder Evolution-Methoden-Writer-Aenderung.

Naechster sinnvoller Schritt:

- UPR-FVX-PR und Workspace-PR reviewen und mergen. Danach verbleibende Evolution-Suboptionen weiter getrennt behandeln, insbesondere Evolution-Methoden-Writer und weitere Poolfilter.

## 2026-05-14 - CFRU/DPE Evolution Same Typing Code Diagnosis

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-evolution-same-typing-blocker-diagnostics`

Aktueller Stand:

- Neues read-only Codeanalyse-Protokoll `08_tests/randomizer/079_p1_evolution_same_typing_code_diagnosis.md` erstellt.
- 079 untersucht konkret den 070-Blocker `FVX-TRAIT-019` Evolutions Same Typing im Carrier `FVX-TRAIT-016` Evolution-Species-Writer.
- Relevante Codepfade sind `GameRandomizer.maybeRandomizeEvolutions()`, `EvolutionRandomizer.randomizeEvolutions()`, `findPossibleReplacements(...)`, `SpeciesSet.filter(...)`, `Species.hasSharedType(...)` und der Gen3 Base-Stats-Type-Read-Scope.
- Wahrscheinlich konkrete Ursache: Der Same-Typing-Filter ruft `to.hasSharedType(...)` auf. Wenn ein Kandidat aus dem Evolution-Replacement-Pool `primaryType == null` hat, dereferenziert `Species.hasSharedType(...)` diesen Null-Type und wirft eine `NullPointerException`.
- Der allgemeine Evolution-Species-Carrier bleibt abgegrenzt: `FVX-TRAIT-016` ist belegt, aber Same Typing nutzt einen zusaetzlichen Species-Type-Filter vor der Zielauswahl.
- `FVX-TRAIT-018` Evolutions Similar Strength bleibt getrennt, weil es nicht denselben `hasSharedType(...)`-Pfad nutzt und in 070 stattdessen Save/Reload mit `writeReloadEvolutionMismatches=24` und `Bad Egg=true` erreichte.
- Ein lokaler Diagnose-Lauf ist fuer die Fixplanung nicht zwingend noetig; ein spaeterer Fix-Smoke fuer `FVX-TRAIT-019` bleibt erforderlich.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Eng gegateten UPR-FVX-Fixbranch fuer `EvolutionRandomizer` Same-Typing-/Null-Primary-Type-Scope vorbereiten. `FVX-TRAIT-018` separat halten und nicht durch denselben Fix als supported hochstufen.

## 2026-05-14 - CFRU/DPE Trainer Type Diversity Null-Type Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`

Aktueller Stand:

- UPR-FVX-Fix `d89fc64e3b0223b03a65466422847dc7df30d03c` erstellt.
- Der Fix bleibt auf `TrainerPokemonRandomizer` begrenzt und behandelt Species mit `primaryType == null` defensiv im Force-Diverse-Types-/`usedTypes`-Pfad.
- Null-Primary-Type-Species werden im erweiterten BPRE-Hack nicht mehr als valide Type-Diversity-/Type-Themes-Replacements genutzt; `EnumSet<Type>` erhaelt keine `null`-Eintraege.
- Bestehende BST-zero-, all-zero-Ability- und Placeholder-/Special-Species-Grenzen bleiben unveraendert.
- `FVX-FOE-009` Trainer Type Diversity / Type Themes wurde lokal sanitisiert ausgefuehrt: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTrainerPokemonMismatches=0`, `filterViolations=0`, `Bad Egg=false`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- Trainer Similar Strength unter `FVX-FOE-001` wurde als Regression lokal sanitisiert ausgefuehrt und bleibt mit Save/Log/Output/Reload true sowie `writeReloadTrainerPokemonMismatches=0` stabil.
- Neues Diagnoseprotokoll `08_tests/randomizer/078_trainer_type_diversity_nulltype_fix_diagnostics.md` erstellt.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit und aktualisiert README, Session, Next Steps, Roadmap, Feature-Coverage und Tool-Manifest.
- Keine Wild-, Evolution-, TypeChart-, MoveData-, Palette-, Item-, Text/Menu-, Graphics-, Trainer-Level-, Additional-Pokemon-, Better-Movesets-, Battle-Style- oder Trainer-Names/Class-Names-Aenderung.

Naechster sinnvoller Schritt:

- UPR-FVX-PR und Workspace-PR reviewen und mergen. Danach die verbleibenden 070-Evolution-Blocker `FVX-TRAIT-018` und `FVX-TRAIT-019` getrennt fortsetzen.

## 2026-05-14 - CFRU/DPE Trainer Type Diversity Code Diagnosis

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-trainer-type-diversity-code-diagnosis`

Aktueller Stand:

- Neues read-only Codeanalyse-Protokoll `08_tests/randomizer/077_p1_trainer_type_diversity_code_diagnosis.md` erstellt.
- 077 untersucht konkret den 070/076-Blocker `FVX-FOE-009` Trainer Type Diversity / Type Themes im Carrier `FVX-FOE-001` Trainer Pokemon.
- Relevante Codepfade sind `GameRandomizer.maybeRandomizeTrainerPokemon()`, `TrainerPokemonRandomizer.randomizeTrainerPokes()`, `pickTrainerPokeReplacement(...)` und `updateUsedTypes(...)`.
- Wahrscheinlich konkrete Ursache: Der Force-Diverse-Types-Pfad schreibt `sp.getPrimaryType(false)` in ein `EnumSet<Type>`. Wenn eine Replacement-Species `primaryType == null` hat, wirft `EnumSet.add(null)` eine `NullPointerException`.
- Der Trainer-Species-Pool filtert im erweiterten BPRE-Hack bereits `BST == 0` und all-zero Ability Species, aber keinen Null-Primary-Type-/unsupported-Type-Scope.
- Trainer Similar Strength ist abgegrenzt: Der stabile 070-Slice nutzt `getRandomSimilarStrengthSpecies(...)`, aktiviert aber nicht den Force-Diverse-Types-/`usedTypes`-Pfad.
- Ein lokaler Diagnose-Lauf ist fuer die Fixplanung nicht zwingend noetig; optional waere er nur fuer sanitisierten Stacktrace-/Null-Primary-Type-Zaehler-Beleg.
- Empfohlen ist ein eng gegateter UPR-FVX-Fixbranch fuer Trainer-Type-Diversity-Null-Type-Scope in `TrainerPokemonRandomizer`, ohne Wild, Evolution, TypeChart, MoveData, Palette, Items, Text/Menu, Graphics oder Level-Modifier.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Fixbranch fuer defensiven Trainer-Type-Diversity-Null-Type-Scope vorbereiten. Danach nur `FVX-FOE-009` und optional Trainer Similar Strength als Regression lokal sanitisiert pruefen.

## 2026-05-14 - CFRU/DPE Trainer Type Diversity Blocker Diagnostics Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-trainer-type-diversity-blocker-diagnostics`

Aktueller Stand:

- Neues read-only Diagnoseplan-Protokoll `08_tests/randomizer/076_p1_trainer_type_diversity_blocker_diagnostics_plan.md` erstellt.
- 076 fokussiert nur den verbliebenen 070-Blocker `FVX-FOE-009` Trainer Type Diversity / Type Themes im Carrier `FVX-FOE-001` Trainer Pokemon.
- Der Befund aus 070 bleibt als echter Save-Blocker klassifiziert: `saveSuccessful=false`, kein Output/Reload, `NullPointerException` und `filterViolations=112` nur bis Abbruch.
- Trainer Similar Strength unter `FVX-FOE-001` bleibt bewusst getrennt, weil dieser Slice in 070 mit Save/Log/Output/Reload true und `writeReloadTrainerPokemonMismatches=0` stabil war.
- Pruefspuren sind Trainer-Type-Diversity-Auswahl gegen Null-Type-, Placeholder-, BST-zero- oder unsupported-Type-Species, Trainer-Pool-Scope, Team-Type-Constraints und fehlende Skip-/Scope-Regeln im Type-Diversity-/Type-Themes-Pfad.
- Spaetere Diagnosemetriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater read-only Code-/Protokollanalysebranch fuer `FVX-FOE-009`, der Trainer-Randomizer- und Type-Diversity-Codepfade identifiziert und den Unterschied zum stabilen Trainer Similar Strength Slice klaert. Kein Fixbranch ohne klare Ursache.

## 2026-05-14 - CFRU/DPE Wild Filter Carrier Nullslot Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`

Aktueller Stand:

- UPR-FVX-Fix `acaada514d04b1d306581ce872d2d77fe1b4c5b3` erstellt.
- Der Fix bleibt auf `WildEncounterRandomizer` begrenzt und behandelt `Encounter`-Slots mit `species == null` defensiv vor der Mapping-/InfoMap-Auswahl.
- Null/unaufloesbare Wild-Encounter-Slots werden nicht als `zoneMap`-/InfoMap-Anker genutzt; sie erhalten ein Replacement aus bestehenden `remaining`-/`allowed`-Pools, mit vorhandener Theme-Grenze und Area-Bans.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary wurden einzeln lokal sanitisiert ausgefuehrt.
- Beide Slices melden `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadWildPokemonMismatches=0`, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`.
- `FVX-WILD-004` meldet `filterViolations=0`; fuer `FVX-WILD-011` wurde kein eigener Filterverletzungszaehler behauptet.
- Die lokalen Fix-Smokes beobachteten `nullSlotsBefore=0` und `nullSlotsAfter=0`; der Fix bleibt trotzdem auf den in 074 identifizierten defensiven Null-/unaufloesbar-Scope begrenzt.
- Neues Diagnoseprotokoll `08_tests/randomizer/075_wild_filter_carrier_nullslot_fix_diagnostics.md` erstellt.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit und aktualisiert README, Session, Next Steps, Roadmap, Feature-Coverage und Tool-Manifest.
- Keine TypeChart-, MoveData-, Palette-, Item-, Encounter-Held-Item-, custom-Day/Night-Wild-, Catch-Em-All-, Minimum-Catch-Rate-, Level-Modifier-, Text/Menu- oder Graphics-Aenderung.

Naechster sinnvoller Schritt:

- UPR-FVX-PR und Workspace-PR reviewen und mergen. Danach die restlichen 070-Blocker getrennt fortsetzen: `FVX-FOE-009` Trainer Type Diversity sowie `FVX-TRAIT-018/019` Evolution-Slices.

## 2026-05-14 - CFRU/DPE Wild Filter Carrier Code Diagnosis

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-code-diagnosis`

Aktueller Stand:

- Neues read-only Codeanalyse-Protokoll `08_tests/randomizer/074_p1_wild_filter_carrier_code_diagnosis.md` erstellt.
- 074 untersucht konkret die 070-Wild-Blocker `FVX-WILD-011` und `FVX-WILD-004` im gemeinsamen `FVX-WILD-001` Standard/Fallback-Wild-Carrier.
- Beide Slices nutzen `wildPokemonZoneMod=GAME` und laufen daher durch `WildEncounterRandomizer.InnerRandomizer.game1to1Encounters()` mit `useMapping=true`.
- Wahrscheinlich konkrete Ursache: `setupAreaInfoMap()` baut seine Infos aus `EncounterArea.getSpeciesInArea()`, dieses nutzt `SpeciesSet`, und `SpeciesSet.add(...)` ignoriert `null`; ein nicht aufloesbarer/null Encounter-Slot bleibt aber in `randomizeArea()` erhalten und trifft danach `setupAllowedForReplacementUsingInfoMap()`, das `IllegalStateException("Info was null for encounter's species!")` wirft.
- Damit treffen `FVX-WILD-011` und `FVX-WILD-004` wahrscheinlich denselben InfoMap-/Nullslot-Pfad, bevor Similar-Strength-BST- oder Keep-Primary-Type-Filter fachlich greifen.
- Ein lokaler Diagnose-Lauf ist fuer die Fixplanung nicht zwingend noetig; optional waere er nur fuer sanitisierten Area-/Slot- oder Exception-Message-Beleg.
- Empfohlen ist ein eng gegateter Fixbranch fuer Wild-Mapping-/Nullslot-Scope, ohne TypeChart, MoveData, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level Modifier, Text/Menu oder Graphics.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- PR fuer 074 reviewen und mergen; danach Fixbranch fuer defensiven Wild-Filter-Carrier-/Nullslot-Scope vorbereiten oder optional einen separat freigegebenen lokalen Diagnosebranch fuer sanitisierten Exception-/Area-Beleg starten.

## 2026-05-14 - CFRU/DPE Wild Filter Carrier Diagnostics Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-diagnostics`

Aktueller Stand:

- Neues read-only Diagnose-/Harness-Planprotokoll `08_tests/randomizer/073_p1_wild_filter_carrier_diagnostics_plan.md` erstellt.
- 073 fokussiert nur `FVX-WILD-011` Wild Similar Strength, `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary und den gemeinsamen `FVX-WILD-001` Standard/Fallback-Wild-Carrier.
- Ausgangsbefunde aus 070 bleiben: beide Wild-Slices sind echte Save-Blocker mit `saveSuccessful=false`, keinem Output/Reload und `IllegalStateException`; `FVX-WILD-004` hatte `filterViolations=0` nur bis Abbruch.
- 073 plant zuerst read-only Code-/Protokollanalyse, um Carrier-Scope von Similar-Strength- und Type-Restriction-Filter-Scope zu trennen.
- Falls vorhandene Dokumente und Codepfade nicht ausreichen, soll eine spaetere lokale Diagnose nur als separater Freigabeschritt erfolgen.
- Hypothesen zu Wild-Nullslot-/Placeholder-Eintraegen, Area-/Encounter-Slot-Scope, leeren oder ungueltigen BST-/Species-Pools, Species-Type-Filtern und strengeren Suboption-Grenzen sind dokumentiert.
- Spaetere Metriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- PR fuer 073 reviewen und mergen; danach read-only Code-/Protokollanalyse fuer den Wild-Filter-Carrier oder, falls nicht ausreichend, ein separat freigegebener lokaler Diagnosebranch.

## 2026-05-14 - CFRU/DPE Wild 070 Blockers Diagnostics Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-070-blockers-diagnostics`

Aktueller Stand:

- Neues read-only Diagnoseplan-Protokoll `08_tests/randomizer/072_p1_wild_070_blockers_diagnostics_plan.md` erstellt.
- 072 plant die gemeinsame Folge-Diagnose fuer `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary.
- Beide Slices bleiben echte Save-Blocker im `FVX-WILD-001` Standard/Fallback-Wild-Carrier: kein Output/Reload und `IllegalStateException`.
- `FVX-WILD-011` wird als BST-/Species-Pool-Filter-Scope plus Wild-Nullslot-/Placeholder-Scope eingeordnet.
- `FVX-WILD-004` wird als Species-Type-Filter-Scope plus Wild-Nullslot-/Placeholder-Scope eingeordnet; `filterViolations=0` aus 070 bleibt nur ein Vor-Abbruch-Befund.
- Gemeinsame Hypothesen sind dokumentiert: Nullslot-/Placeholder-Wild-Entries, Area-/Encounter-Slot-Scope, leere/ungueltige Pools, Placeholder-/Special-/unsupported-Type-Species und strengere Suboption-Vorauswahl trotz P1-supported `FVX-WILD-001` Carrier.
- Spaetere Diagnosemetriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- TypeChart/TypeEffectiveness, MoveData Write, Palette, Items/Field/Shops/Pickup, Encounter Held Items, custom Day/Night-Wild, Catch Em All / Minimum Catch Rate, Level Modifier und Text/Menu/Graphics bleiben ausgeschlossen.
- Keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater read-only Diagnose-/Harness-Plan oder freigegebene read-only Diagnose fuer den Wild-Filter-Carrier; kein Fixbranch ohne klare Ursache.

## 2026-05-14 - CFRU/DPE 070 Blocked Slices Follow-up Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-070-blocked-slices-followup-plan`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/071_p1_070_blocked_slices_followup_plan.md` erstellt.
- 071 plant die Folgeanalyse fuer die in 070 blockierten Similar Strength / Same Type / Type Themes Slices, ohne Codeaenderung, Fix oder Randomizer-Laeufe.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary werden gemeinsam als Wild-Carrier-/Placeholder-Scope modelliert, weil beide `FVX-WILD-001` Carrier und `IllegalStateException` teilen.
- `FVX-FOE-009` Trainer Type Diversity / Type Themes bleibt ein eigener Trainer-Type-Diversity-/Null-Type-Scope.
- `FVX-TRAIT-018` Evolutions Similar Strength bleibt ein eigener Evolution-Reload-/Bad-Egg-Scope; `Bad Egg` kann dort nicht als reine 055-Log-Hygiene freigegeben werden, solange `writeReloadEvolutionMismatches` ungleich `0` ist.
- `FVX-TRAIT-019` Evolutions Same Typing bleibt ein eigener Evolution-Same-Typing-/Null-Scope.
- Spaetere Diagnosemetriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- TypeChart/TypeEffectiveness, MoveData Write, Palette, Items/Field/Shops/Pickup, Graphics/Sprites, Text/Menu, Level Modifier und Evolution-Methoden-Writer bleiben ausgeschlossen.
- Keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater read-only Diagnoseplan oder Diagnosebranch fuer Wild Similar Strength + Wild Type Restrictions, ohne offene Writer und ohne Fixarbeit.

## 2026-05-14 - CFRU/DPE Similar Strength / Same Type Regression-Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/070_p1_similar_strength_same_type_regression_smoke_results.md` erstellt.
- Die in 069 geplanten Similar-Strength-/Same-Type-/Type-Theme-/Type-Restriction-Slices wurden einzeln lokal ausgefuehrt und sanitisiert dokumentiert.
- Trainer Similar Strength unter `FVX-FOE-001` ist im Trainer-Species-Carrier-Smoke stabil: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTrainerPokemonMismatches=0`, `Bad Egg=false`, `<unknown>=false`, `stacktrace=none`.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary blockieren beim Save mit `IllegalStateException`; kein Output/Reload.
- `FVX-FOE-009` Trainer Type Diversity / Type Themes blockiert beim Save mit `NullPointerException`; kein Output/Reload.
- `FVX-TRAIT-018` Evolutions Similar Strength speichert und reloadet, meldet aber `writeReloadEvolutionMismatches=24` und `Bad Egg=true`; der Marker wird wegen der Mismatches nicht als unkritischer 055-Marker freigegeben.
- `FVX-TRAIT-019` Evolutions Same Typing blockiert beim Save mit `NullPointerException`; kein Output/Reload.
- TypeChart/TypeEffectiveness, MoveData Write, Field Items/Shops/Pickup, Encounter Held Items, Palette/Graphics, Text/Menu, Level-Modifier, Evolution-Methoden-Writer, Starter Held Items, Race Mode / Intro Mon, Better Movesets, Trainer Additional Pokemon, Battle Style, Trainer Names/Class Names, Catch Em All, Minimum Catch Rate, Wild held items und custom Day/Night-Wild blieben ausgeschlossen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.
- Lokale ROM-, Log-, Output-ROM-, Build- und Diagnoseartefakte blieben ignored und werden nicht committed oder dokumentiert.

Naechster sinnvoller Schritt:

- Read-only Diagnoseplan fuer die blockierten 070-Slices: Wild Similar Strength/Type Restrictions gegen Wild-Nullslot-/Placeholder-Scope, `FVX-FOE-009` gegen Trainer-Type-Diversity-/Null-Type-Scope und `FVX-TRAIT-018/019` gegen Evolution-Reload-Mismatches, `Bad Egg` und Null-Evolution-Scope.

## 2026-05-14 - CFRU/DPE Similar Strength / Same Type Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/069_p1_similar_strength_same_type_regression_smoke.md` erstellt.
- 069 plant spaetere Regression-Smokes fuer BST-/Type-basierte Poolfilter: Similar Strength, Same Type / Same Typing, Type Themes und Type Restrictions.
- Geplante Slices: `FVX-WILD-011` Wild Similar Strength, `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary, Trainer Similar Strength konservativ als Suboption unter `FVX-FOE-001`, `FVX-FOE-009` Trainer Type Diversity / Type Themes, `FVX-TRAIT-018` Evolutions Similar Strength und `FVX-TRAIT-019` Evolutions Same Typing.
- Geeignete Carrier sind `FVX-WILD-001` Standard/Fallback Wild, `FVX-FOE-001` Trainer Pokemon und `FVX-TRAIT-016` Evolution Randomization.
- 069 nutzt Species-Pools, BaseStats/BST und Species-Type-Felder aus belegten Datenpfaden; Same Type / Type Themes beweisen keinen TypeChart- oder TypeEffectiveness-Support.
- Starter-Type/BST aus 065 und `FVX-SST-012` Static Similar Strength bleiben nur Referenz-/Vergleichsbelege, nicht primaerer Scope.
- TypeChart/TypeEffectiveness, MoveData Write, Field Items/Shops/Pickup, Encounter Held Items, Palette/Graphics, Text/Menu, Level-Modifier, Evolution-Methoden-Writer, Starter Held Items, Race Mode / Intro Mon, Better Movesets, Trainer Additional Pokemon, Battle Style, Trainer Names/Class Names, Catch Em All, Minimum Catch Rate, Wild held items und custom Day/Night-Wild bleiben ausgeschlossen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`: die in 069 geplanten Wild-, Trainer- und Evolution-Slices einzeln lokal ausfuehren und sanitisiert dokumentieren, weiter ohne offene Writer.

## 2026-05-14 - CFRU/DPE TypeEffectiveness Follow-up Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/068_type_effectiveness_followup_smoke_results.md` erstellt.
- Die in 067 geplanten TypeEffectiveness-Folgesmokes wurden einzeln lokal ausgefuehrt und sanitisiert dokumentiert: `FVX-TYPE-001` Balanced, Keep Type Identities und Inverse, `FVX-TYPE-002` Add Random Immunities sowie `FVX-TYPE-003` Update Type Effectiveness.
- Alle fuenf Slices melden `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTypeChartMismatches=0` und `stacktrace=none`.
- Foresight- und Endtable-Terminatoren blieben in allen Slices erhalten.
- Unsupported/Stellar wurde in keinem Slice eingefuehrt oder still normalisiert.
- `Bad Egg=false` und `<unknown>=false` in allen Slice-Logs.
- Balanced erzeugte Fairy-Rohtriplets und reloadete sie als raw `0x17`; Keep Type Identities, Inverse, Add Random Immunities und Update Type Effectiveness erzeugten keine Fairy-Rohtriplets und kein Fehlmapping.
- `FVX-TYPE-002` Add Random Immunities wurde getrennt als eigener Risikopunkt getestet.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.
- Lokale ROM-, Log-, Output-ROM-, Build- und Diagnoseartefakte blieben ignored und werden nicht committed.

Naechster sinnvoller Schritt:

- PR fuer `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes` reviewen und mergen; danach zu `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke` zurueckkehren oder einen offenen Writer separat freigeben.

## 2026-05-14 - CFRU/DPE TypeEffectiveness Follow-up Smoke Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/067_type_effectiveness_followup_smoke_plan.md` erstellt.
- Der gemergte TypeChart-Fix aus Diagnose 066 bleibt Referenz: TypeEffectiveness-only Random war Save/Log/Output/Reload-stabil, `writeReloadTypeChartMismatches=0`, Fairy reloadete als raw `0x17`, unsupported/Stellar wurde nicht eingefuehrt oder still normalisiert und Terminatoren blieben erhalten.
- 067 stellt klar, dass der Random-Smoke aus 066 die Einzelpruefung weiterer TypeEffectiveness-GUI-Modi nicht ersetzt.
- Geplante spaetere Slices: `FVX-TYPE-001` Balanced, `FVX-TYPE-001` Keep Type Identities, `FVX-TYPE-001` Inverse, `FVX-TYPE-002` Add Random Immunities und `FVX-TYPE-003` Update Type Effectiveness.
- `FVX-TYPE-002` Add Random Immunities bleibt als eigener Risikopunkt getrennt geplant.
- Gemeinsame spaetere Erfolgskriterien dokumentiert: Save/Log/Output/Reload true, `writeReloadTypeChartMismatches=0`, Fairy raw `0x17`, unsupported/Stellar nicht eingefuehrt oder normalisiert, Foresight-/Endtable-Terminatoren erhalten, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`.
- MoveData, Palette-Randomization, Items/Field Items/Shops/Pickup, Graphics/Sprites, Text/Menu und Species-Type-Write bleiben ausgeschlossen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Spaeterer Test-/Diagnosebranch fuer die geplanten TypeEffectiveness-Folgesmokes, der die Slices einzeln ausfuehrt und sanitisiert dokumentiert, oder Rueckkehr zu `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`.

## 2026-05-14 - CFRU/DPE TypeChart Preserve Effectiveness Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`

Aktueller Stand:

- UPR-FVX-Fix `36707e0190d3d9fa587550dfc5631fcaa9abd6b1` erstellt.
- Der Fix trennt TypeChart-raw-Type-Mapping von `gBaseStats`-Type-Mapping: Fairy `0x17` wird im CFRU/DPE-TypeChart gelesen und geschrieben, waehrend Stellar/raw `0x18` unsupported bleibt.
- Unsupported raw TypeChart-Triplets werden preserve-/skip-only behandelt und nicht still auf Normal, Fairy oder null normalisiert.
- Foresight-Block und Endtable-Terminator bleiben erhalten; die CFRU/DPE-Kapazitaetspruefung nutzt den vorhandenen TypeChart-Bereich.
- Neues Diagnoseprotokoll `08_tests/randomizer/066_type_chart_preserve_effectiveness_fix_diagnostics.md` erstellt.
- TypeEffectiveness-only Smoke: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTypeChartMismatches=0`, `fairyNonNeutralReload=13`, `rawFairyEntriesReload=13`, `unsupportedRawEntriesPreserved=true`, Terminatoren erhalten und `stacktrace=none`.
- `Bad Egg=false` und `<unknown>=false` im TypeEffectiveness-only Log.
- Keine Species-Type-Write-Aenderung aus 051, kein STELLAR-Enum, keine MoveData-, Palette-, Item-, Graphics- oder Text/Menu-Aenderung.
- Workspace dokumentiert den neuen UPR-FVX-Submodule-Pin; lokale Diagnoseartefakte bleiben ignored und werden nicht committed.

Naechster sinnvoller Schritt:

- PRs fuer UPR-FVX-Fix und Workspace-Submodule-/Diagnoseupdate pruefen; danach optional einzelne TypeEffectiveness-Folgesmokes fuer Balanced, Keep Identities, Inverse/Add Immunities und Update Type Effectiveness planen.

## 2026-05-14 - CFRU/DPE Starters Suboptions Regression-Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/065_p1_starters_suboptions_regression_smoke_results.md` erstellt.
- Die lokal ausgefuehrten 063-Slices wurden sanitisiert dokumentiert: Baseline `FVX-SST-002`, `FVX-SST-003` basic with 2 evolutions, `FVX-SST-004` any basic, `FVX-SST-005` type restrictions, `FVX-SST-006` no legendaries und `FVX-SST-009` BST min/max.
- Alle sechs Slices melden Save/Log/Reload true, `Starter-Mismatches=0`, `Filterverletzungen=0` und `stacktrace=none`.
- `Bad Egg=false` und `<unknown>=false` in allen Slice-Logs.
- Starter Held Items `FVX-SST-007`/`FVX-SST-008`, MoveData Write, Field Items/Shops/Pickup, Palette-Randomization, TypeChart und Text/Menu/Graphics blieben aus.
- `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` wurden konservativ als getestet im Starter-Species-Writer-Smoke dokumentiert, nicht als globale Vollabdeckung fuer Wild-/Trainer-/Evolution-Kombinationen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe im Dokumentationsblock, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`: BST-/Type-basierte Pooling-Suboptionen pruefen, ohne TypeChart oder MoveData-Write zu aktivieren.

## 2026-05-14 - CFRU/DPE Global Species Pool Regression-Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/064_p1_global_species_pool_regression_smoke_results.md` erstellt.
- Die lokal ausgefuehrten 062-Slices wurden sanitisiert dokumentiert: Baseline Carrier, `FVX-GEN-001` Generation Limits, `FVX-GEN-001` related Pokemon und `FVX-GEN-002` No Premature Evolutions.
- Alle vier Slices melden Save/Log/Reload true, `Starter-Mismatches=0` und `stacktrace=none`.
- `Bad Egg` und `<unknown>` traten in den Slice-Logs nicht auf.
- Aktiv war nur `FVX-SST-002` als Starter-Species-Carrier plus jeweiliger Poolfilter.
- Held Items, MoveData-Write, Palette-Randomization, TypeChart, Evolution-Methoden-Fixes und Intro/Race Mode blieben aus.
- `FVX-GEN-001` und `FVX-GEN-002` wurden konservativ als getestet im Starter-Carrier-Smoke dokumentiert, nicht als globale Vollabdeckung fuer Wild-/Trainer-/Evolution-Kombinationen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe im Dokumentationsblock, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`: die in 063 geplanten Starter-Suboptions-Slices lokal ausfuehren, weiter ohne Starter Held Items und ohne offene Writer.

## 2026-05-14 - CFRU/DPE Starters Suboptions Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/063_p1_starters_suboptions_regression_smoke.md` erstellt.
- Starter-Suboptionen aus Diagnose 061/062 ueber den belegten Starter-Species-Writer geplant.
- `FVX-SST-002` bleibt nur belegter Basis-/Carrier-Pfad.
- Geplante Slices dokumentiert: `FVX-SST-003`/`FVX-SST-004` Basic-/Evolution-Filter, `FVX-SST-005` Type Restrictions, `FVX-SST-006` Legendary Filter und `FVX-SST-009` BST-Min/Max separat.
- Starter Held Items `FVX-SST-007`/`FVX-SST-008`, Field Items/Shops/Pickup, Encounter Held Items, MoveData Write, Palette/Graphics, TypeChart, Text/Menu, Level Modifier und Evolution-Methoden-Writer bleiben ausgeschlossen.
- Erwartete spaetere Metriken, Artefaktregeln und Stop-Regeln dokumentiert; keine Hochstufung der Starter-Suboptionen auf P1-supported ohne separaten spaeteren Lauf.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`: BST-/Type-basierte Pooling-Suboptionen planen, ohne TypeChart oder MoveData-Write zu aktivieren.

## 2026-05-14 - CFRU/DPE Global Species Pool Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/062_p1_global_species_pool_regression_smoke.md` erstellt.
- Erster konkreter Regression-Smoke aus Diagnose 061 fuer Global Species Pools / Generation Limits geplant.
- Primaere Feature-IDs festgelegt: `FVX-GEN-001` Limit Pokemon und `FVX-GEN-002` No Premature Evolutions.
- Generation Limits und related-Pokemon-Scope werden unter `FVX-GEN-001` gefuehrt, weil keine separaten Feature-IDs existieren.
- `FVX-GEN-003` No Random Intro Mon und `FVX-GEN-004` Race Mode sind ausdruecklich nicht Teil dieses Smokes.
- Minimaler Carrier fuer spaetere Laeufe ist ein einzelner P1-stabiler Species-Writer, bevorzugt `FVX-SST-002`; optionaler Wild-Vergleich gegen `FVX-WILD-001` bleibt separat.
- Spaetere Smoke-Slices, erlaubte Settings, ausgeschlossene offene Writer, erwartete Metriken, Artefaktregeln und Stop-Regeln dokumentiert.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`: Starter-Poolfilter wie random basic/two evolutions, Type Restrictions, No Legendaries und BST-Min/Max getrennt von Starter-Held-Items planen.

## 2026-05-13 - CFRU/DPE P1 Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/061_p1_regression_smoke_plan.md` erstellt.
- Priorisierte Smoke-Gruppen aus Diagnose 060 und der FVX Feature-Coverage-Matrix abgeleitet.
- Feature-Coverage mit `130` Feature-/Suboption-Zeilen eingebunden; spaetere Smokes sollen Feature-IDs referenzieren.
- Smoke-Gruppen festgelegt: Global Species Pools / Generation Limits, Similar Strength / Same Type Pooling, Evolutions-Suboptionen ohne offene Method-/Item-/Move-Writer, Starters, Movesets/TM/Tutor/Egg, Trainer Level Modifier separat und Wild Level Modifier separat.
- Offene Writer explizit als Nicht-Smoke-Fixbereiche markiert: MoveData Write, Field Items/Shops/Pickup, Palette Randomization, TypeChart, Graphics/Sprites und Text/Menu.
- Allgemeine spaetere Metriken definiert: Save/Log/Output/Reload, relevanter Mismatch-Zaehler `0`, `stacktrace=none`, keine verbotenen Artefakte und Marker nur nach 055 klassifizieren.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke`: erster spaeterer Regression-Smoke fuer `Limit Pokemon`, Generation Limits und related Pokemon, strikt ohne offene Writer.

## 2026-05-13 - CFRU/DPE GUI-Suboptions-Regressionsmatrix

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-gui-suboptions-regression-matrix`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md` erstellt.
- Konkrete FVX-GUI-Hauptoptionen und Suboptionen wurden gegen den aktuellen CFRU/DPE-P1-Supportstand eingeordnet.
- Statusklassen festgelegt: `P1-supported`, `wahrscheinlich supported, aber nicht einzeln getestet`, `modelliert, Fix offen`, `open-not-diagnosed` und `out of scope`.
- Direkt belegte Datenpfade wurden von nur wahrscheinlich stabilen Suboptionen, modellierten offenen Writern und ungetesteten GUI-Kombinationen getrennt.
- Similar Strength, Same Type / Prefer Same Type, Follow Evolutions, Level Modifier, Force Change, Change Impossible Evolutions und Make Evolutions Easier wurden konservativ nach Datenpfad- und Writer-Risiko eingeordnet.
- Diagnose 055 bleibt Log-Hygiene-Grenze, 056 MoveData-Grenze, 057 Field-/Shop-/Pickup-Grenze, 058 Palette-/Graphics-Grenze und 059 TypeChart-Grenze.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan`: read-only Smoke-/Regression-Plan fuer priorisierte Suboptionen erstellen, bevor mehrere offene Writer in einem Fixbranch vermischt werden.

## 2026-05-13 - CFRU/DPE Type-Chart-Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/059_p1_type_chart_model.md` erstellt.
- Pokemon-Type-Read/Write aus Diagnose 051 wurde strikt von Type-Chart-/Effectiveness-Randomization getrennt.
- Klar dokumentiert: 051 beweist `gBaseStats`-Type-Read/Write inklusive Fairy `0x17` und `typeIdMismatches=0`, aber keinen Type-Chart-Support.
- Fairy `0x17` in Species-Daten wurde von Fairy-Effectiveness-Eintraegen in der TypeTable getrennt.
- Stellar `0x18` bleibt unsupported/preserve-only und darf nicht stillschweigend in Random-Pools oder TypeChart-Writes eingefuehrt werden.
- `TypeEffectivenessRandomizer`, `getTypeTable()`/`setTypeTable()`, `TypeEffectivenessOffset`, Foresight-/End-Table-Terminatoren und `nonNeutralEffectivenessCount` wurden als eigener Hochrisiko-Writer klassifiziert.
- Preserve-/Skip-Policy und Reload-/Diagnosekriterien fuer spaetere TypeChart-Fixbranches festgelegt.
- Diagnose 058 bleibt Palette-Grenze, 057 Item-/Field-/Shop-/Pickup-Grenze, 056 MoveData-Grenze und 055 Log-Hygiene-Grenze.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-gui-suboptions-regression-matrix`: GUI-Suboptionen nach den read-only Modellen 055-059 regressionsorientiert konsolidieren.

## 2026-05-13 - CFRU/DPE Palette-Randomization-Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/058_p1_palette_randomization_model.md` erstellt.
- Bestehende Palette-Safety wurde strikt von echter geaenderter Palette-Randomization getrennt.
- Safety-Stand eingeordnet: defensiver `loadPokemonPalettes()` fuer missing/invalid Slots und Skip-Unchanged-`savePokemonPalettes()` fuer unveraenderte CFRU/DPE-Pokemon-Paletten.
- Klar dokumentiert: `PokemonPalettesMod.RANDOM` und `Gen3to5PaletteRandomizer` sind echte Writer-Pfade und nicht durch die Safety-Diagnosen als P1-supported belegt.
- `savePokemonPalettes()`, `rewriteCompressedPalette()` und der komprimierte `DataRewriter`-Repointing-Pfad wurden als offene Hochrisiko-Writer klassifiziert.
- Shared/missing Palette-Pointer-Risiken dokumentiert, inklusive `SPECIES_CUBONE_A`-/`gMonPaletteTable[1038]`-Nullslot, DPE-Gap-Slots `[252]..[276]` und `gFrontSprite252Pal`/`gBackShinySprite252Pal`.
- Preserve-/Skip-Policy und Reload-/Diagnosekriterien fuer spaetere Palette-Fixbranches festgelegt.
- Graphics/Sprites bleiben ein eigenes P2-Modell; keine Vermischung mit Pokemon-Palette-Randomization.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`: Type-Chart- und moderne Type-Interaktion getrennt von Pokemon-Type-Read/Write modellieren.

## 2026-05-13 - CFRU/DPE Field Items / Shops / Pickup Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-field-items-shops-pickup-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md` erstellt.
- Field Items, Shops, Pickup und allgemeine Item-Randomization wurden strikt von Encounter Held Items aus Diagnose 054 getrennt.
- Item-Scope-Stand aus 053/054 eingeordnet: klassischer FVX-FRLG-`ItemCount=374`, CFRU-naher Scope bis `778`/`779`, DPE-Header-Scope bis ca. `799`, getesteter 054-Scope `item.count=778`.
- Field-Item-Risiken dokumentiert: Map-/Script-Kontext, required field TMs, moderne TM/HM-Items, Key-/System-/Placeholder-Items und eigener Reload-Nachweis.
- Shop-Randomization-Risiken dokumentiert: `ShopPointerOffsets`, Special-/Main-Game-Shop-Scope, Shopgroessen, Preise, Guaranteed Items und Text/Menu-Grenze.
- Pickup-Risiken dokumentiert: klassischer `PickupTableStartLocator`/`PickupItemCount`, CFRU `sPickupCommonItems`/`sPickupRareItems`, Probability-Slots und moderne Item-Pools.
- Preserve-/Skip-Policy und Reload-/Diagnosekriterien fuer spaetere Fixbranches festgelegt.
- Diagnose 055 bleibt Log-Hygiene-Grenze; Diagnose 056 bleibt Move-Data-Write-Grenze.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`: Vorhandene Palette-Safety von echter Palette-/Graphics-Randomization trennen und Write-/Repointing-Risiken modellieren.

## 2026-05-13 - CFRU/DPE Move-Data-Write-Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/056_p1_move_data_write_model.md` erstellt.
- Der aktuelle Move-Data-Read-Stand wurde aus vorhandenen Diagnosen eingeordnet: `moves.total=992`, hoechster geladener Move `991:PsychicNoise`, Category-Verteilung aus Diagnose 034.
- Das CFRU/DPE-`BattleMove`-Layout wurde als 12-Byte-Entry mit `split` bei Byte `+10` dokumentiert.
- Der aktuelle Gen3-`saveMoves()`-Pfad wurde read-only klassifiziert: Move-Namen und die ersten fuenf MoveData-Bytes werden geschrieben; `secondaryEffectChance`, `target`, `priority`, `flags`, `z_move_power`, `split` und `z_move_effect` bleiben nicht als Writer modelliert.
- Preserve-Policy und Reload-Kriterien fuer einen spaeteren Move-Data-Write-Fix wurden festgelegt.
- Diagnose 055 bleibt die Grenze: Log-Hygiene/Fallback-Marker sind getrennt von echten MoveData-Writer-/Scope-Risiken.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-field-items-shops-pickup-model`: Field Items, Shops, Pickup und allgemeine Item-Randomization getrennt von Encounter Held Items modellieren.

## 2026-05-13 - CFRU/DPE Type Log / Placeholder Hygiene

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-type-log-placeholder-hygiene`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/055_type_log_placeholder_hygiene.md` erstellt.
- `Bad Egg`, `<unknown>`, Unknown-Type-/Unknown-Ability-/Unknown-Item-Marker und Placeholder-/Null-Species wurden strikt aus bestehenden Protokollen und read-only `rg`-Befunden klassifiziert.
- Die Marker aus 051/052/054 blockieren den dokumentierten P1-Support nicht, solange Save/Log/Output/Reload stabil bleiben und die jeweiligen Mismatch-Zaehler `0` sind.
- Echte Blocker bleiben getrennt: Null-Species-/BST-zero-/all-zero-Ability-Species sind nur dann Blocker, wenn ein konkreter Randomizer-Pfad abbricht, falsch schreibt oder falsch reloadet.
- Log-Hygiene wurde getrennt von Type-Chart-, Ability-Name-, Item-Name-, Species-Scope- und Fix-Themen dokumentiert.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`: Move-Data-Write fuer `moves.total=992`, `BattleMove.split` und CFRU/DPE-Felder read-only modellieren.

## 2026-05-13 - CFRU/DPE Encounter Held Items Scope-and-Write Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`

Aktueller Stand:

- Workspace PR #91 als gemerged geprueft.
- UPR-FVX-Fix `5c7170b654b09e1fc27ced6857dd50a8e4711f08` erstellt.
- CFRU/DPE-gegateter Item-Scope implementiert: DPE-Oberregion bis `798` wird nur bei plausiblen Itemnamen genutzt, sonst konservativer Scope bis `778`.
- Itemnamen-Fallbacks bleiben sichtbar als `item #<id>` und werden nicht als Random-Pick zugelassen.
- Moderne Bad-/Banned-Filter fuer Encounter Held Items ergaenzt: TMs/HMs, Mail, Balls, Free-/Placeholder-/Shiny-Space, Booster Energy, Tera Orb, Portable PC und modellierte Form-/Mega-/Z-/Plate-/Mask-/Utility-Items.
- Encounter Held Items in `gBaseStats` bei `item1/item2` (`0x0C`/`0x0E`) werden read/write/reload-stabil behandelt; moderne bestehende IDs werden preserved statt zu `0` zu kollabieren.
- Neues Diagnoseprotokoll `08_tests/randomizer/054_encounter_held_items_scope_write_diagnostics.md` erstellt.
- Encounter Held Items-only, Encounter Held Items + Base Stats, + Abilities und + Types liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true` und `writeReloadEncounterHeldItemMismatches=0`.
- Keine Field-Items-, Shops-, Pickup-, Move-Data-, Tutor-, Egg-Move-, Palette/Graphics-, Type-Chart- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs einen der offenen Matrixbereiche modellieren: Move-Data-Write, Field Items/Shops/Pickup, Palette/Graphics, Type-Chart oder Placeholder-/Bad-Egg-Log-Hygiene.

## 2026-05-13 - CFRU/DPE Item-/Bad-Item-/Encounter-Held-Item Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-item-data-and-bad-item-model`

Aktueller Stand:

- Workspace PR #90 und UPR-FVX PR #27 als gemerged geprueft.
- Neues read-only Analyseprotokoll `08_tests/randomizer/053_p1_item_data_and_bad_item_model.md` erstellt.
- CFRU/DPE Itemgrenzen eingeordnet: CFRU-naher Scope bis `ITEM_FREE_SPACE3=778` / `ITEMS_COUNT=779`, DPE-Header-Scope bis `ITEM_SHINY_SPACE20 + 1` / ca. `799`.
- FVX-Risiko dokumentiert: klassischer FireRed `ItemCount=374`, `itemIDToStandard(...)`-Fallback ueber `UNIQUE_OFFSET` und unvollstaendige moderne Itemnamen-/Bad-Item-Abdeckung.
- Encounter Held Items liegen in `gBaseStats` als `u16 item1/item2` bei Offsets `0x0C/0x0E`; Felder sind eng fixbar, aber nicht sicher ohne erweiterten Item-Scope und moderne Bad-/Key-Item-Filter.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.

Naechster sinnvoller Schritt:

- Fixbranch `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`: CFRU/DPE-gated ItemCount-/Itemnamen-Scope, moderne Bad-/Banned-Item-Filter und Encounter-Held-Item-Read/Write/Reload diagnostisch absichern.

## 2026-05-13 - CFRU/DPE Abilities + Hidden Ability Scope-and-Write Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-abilities-hidden-ability-scope-and-write`

Aktueller Stand:

- Workspace PR #89 und UPR-FVX PR #26 als gemerged geprueft.
- UPR-FVX-Fix `639c7e61adbeffea2e29b1d0dafdba8a02a83f89` erstellt.
- CFRU/DPE-gegatetes Ability-Modell implementiert: Ability1/2 bleiben bei BaseStats-Offsets `0x16/0x17`, Hidden Ability wird bei Offset `0x1A` gelesen/geschrieben.
- CFRU/DPE meldet `abilitiesPerSpecies=3` und `highestAbilityIndex=254` / `0xFE`.
- Ability-Namen werden bis `0xFE` geladen; fehlende moderne Namen fallen sichtbar auf `ability #<id>` zurueck.
- `SpeciesAbilityRandomizer` skippt Placeholder-/Null-Species, `BST == 0`, all-zero-Ability-Species und invalid Ability-IDs defensiv.
- Neues Diagnoseprotokoll `08_tests/randomizer/052_abilities_hidden_ability_scope_write_diagnostics.md` erstellt.
- Ability1/2-only, Hidden Ability-only, Ability1/2 + Hidden Ability und Base Stats + Types + Abilities liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `writeReloadAbilityMismatches=0` und `writeReloadHiddenAbilityMismatches=0`.
- Keine Encounter-Held-Item-, Move-Data-Write-, Tutor-, Egg-Move-, Palette/Graphics-, Type-Chart- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Item-/Bad-Item-Modell fuer Encounter Held Items starten oder vorher Placeholder-/Unknown-Type-/Bad-Egg-Log-Hygiene separat einordnen.

## 2026-05-13 - CFRU/DPE Base Stats + Types Scope-and-Write Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write`

Aktueller Stand:

- Workspace PR #88 als gemerged geprueft.
- UPR-FVX-Fix `20f16d07ab4ea62e5cd3f27ef09a6d5b036d2392` erstellt.
- CFRU/DPE-gegatetes BaseStats-Type-Mapping implementiert: raw `0x17` wird als `Type.FAIRY` gelesen und `Type.FAIRY` als `0x17` geschrieben.
- CFRU/DPE-TypeTable-Pool enthaelt Fairy, aber kein Stellar; Stellar-/unsupported Primary-Type-Species werden im Type-Randomizer defensiv uebersprungen.
- Neues Diagnoseprotokoll `08_tests/randomizer/051_base_stats_types_scope_write_diagnostics.md` erstellt.
- Base Stats-only, Types-only und Base Stats + Types liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `writeReloadBaseStatsMismatches=0` und `typeIdMismatches=0`.
- Keine Hidden-Ability-, Encounter-Held-Item-, Move-Data-Write-, Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Hidden Abilities separat fixen oder vorher Item-/Bad-Item-Modell fuer Encounter Held Items starten.

## 2026-05-13 - CFRU/DPE Base Stats, Types, Abilities Model

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model`

Aktueller Stand:

- UPR-FVX PR #25 und Workspace PR #87 als gemerged geprueft.
- Neues read-only Protokoll `08_tests/randomizer/050_p1_base_stats_types_abilities_model.md` erstellt.
- `gBaseStats` fuer den getesteten CFRU/DPE Gen9-BPRE-Stand modelliert: Pointer-Ort `0x080001BC`, Entry-Size `0x1C`, internes Species-Indexing bis `SPECIES_PECHARUNT=0x59F` / `NUM_SPECIES=1440`.
- CFRU BaseStats-Felder eingeordnet: Stats, `type1/type2`, `item1/item2`, `ability1/ability2` und `hiddenAbility` bei Offset `0x1A`.
- FVX-Risiken dokumentiert: Gen3-Type-Mapping liest/schreibt Fairy aktuell nicht korrekt, Stellar ist nicht im FVX-Type-Enum, Hidden Ability wird nicht gelesen/geschrieben, Ability-Count ist `77` statt CFRU `255`, Encounter Held Items haengen am erweiterten Itemmodell.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein ROM-/Build-/Log-Artefakt.

Naechster sinnvoller Schritt:

- `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write` als kleinen ersten Fixbranch planen.
- Hidden Abilities und Encounter Held Items getrennt behandeln; Encounter Held Items erst nach Item-/Bad-Item-Modell.

## 2026-05-13 - CFRU/DPE Learnset GUI Flow Safety Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`

Aktueller Stand:

- UPR-FVX-Fix `086d2a9177df7624a0e7ca1876b210a200d7aa98` erstellt.
- Logger-Nullsafety, Learnset-Repointing-Multiwrite-Safety, Trainer-Movesets-Key-Fallbacks sowie TM/HM-/Tutor-Level-Up-Sanity defensiv stabilisiert.
- Neues Protokoll `08_tests/randomizer/049_p1_learnset_gui_flow_safety_fix_diagnostics.md` erstellt.
- Sieben GameRandomizer-nahe Movesets/Learnsets-Laeufe diagnostiziert: Movesets-only, Trainer-Movesets, Reorder-Damaging, TM/HM-Sanity, Tutor-Sanity, gekoppelte Egg Moves und TM/HM+Tutor-Sanity.
- Alle Laeufe liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true` und `writeReloadLearnsetMismatches=0`.
- Reorder-Damaging nutzt zwei freie Learnset-Blob-Bloecke innerhalb `0x1219A48-0x1600000`; der zweite Write blockiert nicht mehr an einem statischen FreeSpace-Start.
- Keine Move-Data-Write-, Tutor-Text/Menu-, Special-Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.
- Danach Move-Data-Write, Items/Shops/Field, Palette/Graphics und Special-Tutor/Text/Menu separat modellieren.

## 2026-05-13 - CFRU/DPE Learnset GUI Combination Diagnostics

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-learnset-gui-combinations`

Aktueller Stand:

- UPR-FVX PR #24 und Workspace PR #85 als gemerged geprueft.
- Neues Protokoll `08_tests/randomizer/048_p1_learnset_gui_combinations.md` erstellt.
- GameRandomizer-nahe Movesets/Learnsets-Laeufe diagnostiziert; keine Codeaenderung und keine `02_external/**`-Aenderung.
- Erster Learnset-Repointing-Write bleibt stabil: `plannedBlobBytes=30099`, `writtenBlobBytes=31771`, `pointertableEntriesUpdated=1413`, `writeReloadLearnsetMismatches=0`.
- Movesets-only, Movesets+TM/HM ohne Level-Up-Sanity, Movesets+Tutor ohne Level-Up-Sanity und gekoppelte Egg Moves speichern/reloaden stabil.
- Voller GUI-P1-Support bleibt blockiert durch Logger-Fehler, Trainer-Movesets-Kombinationen, Reorder-Damaging-Moves sowie TM/HM-/Tutor-Level-Up-Sanity.

Naechster sinnvoller Schritt:

- Fixbranch `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety` starten.
- Ziele: multi-write-sicheren Learnset-Repointing-Pfad, interne Species-ID-Key-Fallbacks fuer Sanity/Trainer-Movesets und Logger-Nullpfad beheben.


## 2026-05-13 - CFRU/DPE Learnset-Write Repointing Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`

Aktueller Stand:

- UPR-FVX-Fix `77de517da880bebb6ed690ca6e170e5bd10b9cad` erstellt.
- `setMovesLearnt()` schreibt fuer den eng gegateten CFRU/DPE Gen9-BPRE-Pfad neue Level-Up-Learnset-Blobs in die validierte FreeSpace-Region `0x1219A48-0x1600000`.
- Die bestehende `gLevelUpLearnsets`-Pointertable bei `0x25D7B4` bleibt erhalten und wird pro interner Species-ID aktualisiert.
- Diagnose 046 bestaetigt `plannedBlobBytes=17418`, `writtenBlobBytes=11547`, `uniqueBlobCount=416`, `pointertableEntriesUpdated=1413` und `writeReloadLearnsetMismatches=0`.
- Save, Reload, Output-ROM und nichtleerer Log waren im lokalen Diagnoseharness erfolgreich; lokale Artefakte blieben ignored unter `05_builds/**`.
- Keine Move-Data-Write-, Tutor-Text-, Special-Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs einen GUI-/Settings-Kombinationssmoke fuer Pokemon Movesets/Learnsets planen.
- Danach `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.


## 2026-05-13 - FVX GUI Options Compatibility Matrix

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-fvx-gui-options-matrix`

Aktueller Stand:

- Matrixprotokoll `08_tests/randomizer/047_fvx_gui_options_compatibility_matrix.md` erstellt.
- P1-supported Bereiche aus vorhandenen Diagnosen zusammengefuehrt: Standard/Fallback-Wild, Starters, Static/Gift, Trainer Species, Trainer Movesets, Trainer Held Items, Evolutions, Move-Data-Read, TM/HM 128-Slot, normale Tutor-Tabellen und direkte Egg Moves.
- Teilunterstuetzte Bereiche markiert: bounded Learnset-Write, Palette-Safety und Move-Data-Read ohne Write.
- Offene Hochrisiko-Writer priorisiert: Full Learnset Repointing, Base Stats/Types/Abilities, Move-Data-Write, Items/Shops/Field/Pickup und Palette/Graphics-Randomization.
- Keine Codeaenderung, keine `02_external/**`-Aenderung und keine ROM-/Build-/Tool-Artefakte.

Naechster sinnvoller Schritt:

- Wenn Phase 2 FreeSpace-Nachweis positiv ist, `compat/upr-fvx-cfru-dpe-learnset-write-repointing` fortsetzen.
- Andernfalls zuerst `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #80 ist gemerged.
- UPR-FVX PR #23 und Workspace PR #81 sind gemerged.
- UPR-FVX-Stand im Workspace: `5c7170b654b09e1fc27ced6857dd50a8e4711f08`.
- TM/HM-only ist im getesteten CFRU/DPE-128-Slot-Scope P1-supported.
- Tutor-only ist im getesteten CFRU/DPE-152-Slot-Scope P1-supported.
- Egg-Move direct scope ist P1-supported.
- Learnset-Write bounded in-place ist implementiert und diagnostisch stabil fuer strikt validierte same-size Writes.
- Full Learnset-Write-Repointing ist im direkten `setMovesLearnt()`-Scope implementiert und diagnostisch stabil.
- Pokemon Movesets/Learnsets sind im getesteten GUI-/Settings-nahen Flow P1-supported.
- Encounter Held Items sind im getesteten CFRU/DPE-`gBaseStats`-Scope P1-supported.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`

## Aktueller Arbeitsblock

CFRU/DPE Palette-Randomization-Modell.

## Ziel

Read-only modellieren, wie bestehende Palette-Safety von echter geaenderter Palette-/Graphics-Randomization zu trennen ist.

## In diesem Arbeitsblock geprueft / geaendert

- Workspace-Branch `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model` genutzt; nicht auf `main` gearbeitet.
- Pflichtdokumente und Diagnosen 047/055/056/057 sowie vorhandene Palette-Safety-Protokolle gelesen.
- Read-only `rg`-Suche nach Palette-, `PokemonPalettesMod.RANDOM`-, `Gen3to5PaletteRandomizer`-, `savePokemonPalettes()`-, `rewriteCompressedPalette()`-, compressed-, repoint-, sprite- und graphics-Markern ausgefuehrt.
- Neues Protokoll erstellt: `08_tests/randomizer/058_p1_palette_randomization_model.md`.
- `08_tests/randomizer/README.md`, `SESSION_STATE.md`, `NEXT_STEPS.md` und Roadmap aktualisiert.
- Tool-Manifest nicht geaendert, weil kein Tool-/Repo-/Commit-/Submodule-Stand geaendert wurde.

## Ergebnis

- Palette-Safety ist nur fuer defensive Loads, missing/invalid Slots und unveraenderte Palette-Saves belegt.
- Echte geaenderte Palette-Randomization ueber `PokemonPalettesMod.RANDOM` / `Gen3to5PaletteRandomizer` bleibt open / not diagnosed.
- `savePokemonPalettes()` faellt bei geaenderten Paletten in compressed Write-/Repointing-Semantik.
- Shared/missing Palette-Pointer, Dex-/Pokedex-Mapping und FreeSpace/Repointing bleiben eigene Risiken.
- Graphics/Sprites bleiben ein separates P2-Modell.

## Noch nicht gestartet

- Special-Tutor-Modell/Fix
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Vollstaendige Nullslot-`<unknown>`-Analyse ausserhalb der bereits dokumentierten Klassifikation
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen.

Lokale Diagnose-Artefakte blieben ignored unter `05_builds/**` und wurden nicht committed.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

UPR-FVX und andere `02_external/**`-Repos blieben in diesem Analyseblock unangetastet.

Keine Type-Chart-, Ability-Name-, Item-Name-, Move-Data-Write-, Tutor-Text/Menu-, Special-Tutor-, Egg-Move-, Graphics/Sprite- oder Text/Menu-Ausweitung.

Keine MCP-Configs mit Secrets angelegt.

## Naechste Pruefung

Lokal im Workspace nach den Dokumentationsaenderungen pruefen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

## Naechster empfohlener Branch

Nach Merge dieses Analyseblocks: `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`. Graphics/Sprites, Special Tutors, Tutor-Text/Menu-Rewrites und spaetere Palette- oder Field-Items-/Shops-/Pickup-Fixes bleiben eigene Folgebranches.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-learnset-repointing-model

- UPR-FVX PR #23 und Workspace PR #81 als gemerged geprueft.
- CFRU/DPE Learnset-Repointing-Modell read-only dokumentiert.
- `gLevelUpLearnsets` Pointer-Ort `0x03EA7C` zeigt auf die aktive Pointertable bei `0x25D7B4`.
- Quellenanalyse: `1408` Pointertable-Zuweisungen, `1104` eindeutige Learnset-Ziele, `148` Shared-Zielgruppen.
- Kein statisch freier Append-Bereich belastbar belegt; spaeterer Fix muss FreeSpace im konkreten ROM nachweisen.
- Kein Fix, keine Aenderung an `02_external/**`, kein Repointing.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-learnset-write-bounded

- Workspace PR #80 als gemerged geprueft.
- UPR-FVX-Fix `dd9d80c16936a99bac1d7ef777b43baa7c2f029d` erstellt.
- `setMovesLearnt()` erhaelt einen eng gegateten CFRU/DPE bounded in-place Write-Pfad fuer `gLevelUpLearnsets`.
- Kein Repointing: Growth wird diagnostiziert und uebersprungen.
- Diagnose 044 bestaetigt Save/Log/Output/Reload und `writeReloadLearnsetMismatches=0`.
- Writer akzeptiert im Test `boundedWrites=1` und skippt `1412` unsafe Pointer; voller Learnset-Write braucht ein separates Repointing-Modell.
- Keine Move-Data-Write-, Tutor-Text-, Special-Tutor- oder Egg-Move-Ausweitung.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-egg-move-model

- UPR-FVX PR #21 und Workspace PR #77 als gemerged geprueft.
- CFRU/DPE Egg-Move-Modell read-only dokumentiert.
- `gEggMoves` als `u16`-Stream mit Species-Marker `species + 20000` und Terminator `0xFFFF` eingeordnet.
- DPE `repointall` zeigt `gEggMoves 08045C50`; FVX nutzt aktuell noch `EggMoves=0x25EF0C` aus dem FireRed-RomEntry.
- DPE-Egg-Move-Stream enthaelt Gen8-/PLA-/Paldea-Species und Move-IDs bis `MOVE_TIDYUP` ID `967`.
- Aktuelle FVX-Risiken: Pokédex-ID-Mapping statt interner Species-ID, globale Move-Ban-Arrays mit Laenge `827`, Egg-Move-Randomization an Learnset-Write gekoppelt.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility

- Workspace PR #76 als gemerged geprueft.
- UPR-FVX-Fix `4ce93754de390e9177efd2541c02edba0afbb0c4` erstellt.
- CFRU/DPE-Tutor-Pfad eng ueber `useCfruDpeGen9SpeciesCount` gegatet.
- `gMoveTutorMoves` als `u16[152]` ueber `0x8120BE4` gelesen/geschrieben.
- `gTutorLearnsets` als 19-Byte-/152-Bit-Compatibility pro Species ueber `0x8120C30` gelesen/geschrieben.
- Diagnose 040 bestaetigt Tutor moves-only, Compatibility-only und Tutor moves + Compatibility mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Special-Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder Tutor-Text-Rewrite-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tutor-model

- UPR-FVX PR #20 und Workspace PR #75 als gemerged geprueft.
- CFRU/DPE Tutor-/Special-Tutor-Modell read-only dokumentiert.
- `gMoveTutorMoves` als `u16[152]` ueber Pointer-Location `0x8120BE4` eingeordnet.
- `gTutorLearnsets` als 152-Bit-/19-Byte-Compatibility pro Species ueber Pointer-Location `0x8120C30` eingeordnet.
- Special Tutors als Sonderlogik ausserhalb der normalen Tabelle dokumentiert.
- FVX nutzt aktuell weiterhin klassischen FireRed-Tutor-Scope `15`; Tutor-only bleibt nicht P1-supported.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tm-hm-128-slot

- Workspace PR #74 als gemerged geprueft.
- UPR-FVX-Fix `58379ffd3146fcd6bb0eb416647cdf9b752cfc0e` erstellt.
- CFRU/DPE-128-Slot-TM/HM-Pfad eng ueber `useCfruDpeGen9SpeciesCount` gegatet.
- `gTMHMMoves` als `u16[128]` ueber `0x8125A8C` gelesen/geschrieben; TMs `0..119`, HMs `120..127`.
- `gTMHMLearnsets` als 16-Byte-/128-Bit-Compatibility pro Species ueber `0x8043C68` gelesen/geschrieben.
- Diagnose 038 bestaetigt TM moves-only, Compatibility-only und TM moves + Compatibility mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder TM51..TM120-Item-Text-/Palette-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model

- UPR-FVX PR #19 und Workspace PR #73 als gemerged geprueft.
- CFRU/DPE-128-Slot-TM/HM-Modell read-only dokumentiert.
- `gTMHMMoves` ist `u16[128]` ueber Pointer `0x8125A8C`; TMs `1..120`, HMs `121..128`.
- `gTMHMLearnsets` ist 128-Bit-/16-Byte-Compatibility pro Species ueber Pointer `0x8043C68`.
- FVX-`50+8`-Pfad bleibt P1-supported, bildet aber das 128-Slot-Modell nicht ab.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety

- Workspace PR #72 als gemerged geprueft.
- UPR-FVX-Fix `32e43ac03a5762542773213a13be4e0389f1deae` erstellt.
- TM-Move-Randomization fuer CFRU/DPE gegen Move-IDs oberhalb der alten FVX-Sicherheitslisten abgesichert.
- TM/HM-Compatibility fuer CFRU/DPE gegen Placeholder-Species und `null`-Typen abgesichert.
- Diagnose 036 bestaetigt TM moves + Compatibility, Compatibility-only und TM moves-only mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder 128-Slot-TM/HM-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-only

- UPR-FVX PR #18 und Workspace PR #71 als gemerged geprueft.
- TM/HM-only Diagnose auf UPR-FVX `c71fd75e67f5a839560bbf5de7c6f17317a64bd1` ausgefuehrt.
- FVX erkennt nur klassisches `50+8`-TM/HM-Modell.
- TM-Move-Randomization blockiert an altem Move-Ban-Array-Limit.
- TM/HM-Compatibility-only blockiert separat an Null-Type-Species.
- Neues Protokoll erstellt: `08_tests/randomizer/035_p1_tm_hm_only.md`.
- Kein Fix, keine Randomizer-Codeaenderung, keine committed ROM-/Build-Artefakte.

## 2026-05-13 - CFRU/DPE Egg-Move scope/write fix

- Active branch: `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write`.
- UPR-FVX fix commit: `18168b78b973a4c39f34053ac58f21279a26d8d2`.
- Implemented a gated CFRU/DPE `gEggMoves` reader/writer through pointer location `0x45C50` while preserving the classic `u16` stream, `species + 20000` markers, and `0xFFFF` sentinel.
- Preserved internal `SpeciesSet` identity for Egg-Move keys and guarded high move-ID flag-array access in `SpeciesMovesetRandomizer`.
- Added diagnosis `08_tests/randomizer/042_egg_moves_scope_and_write_fix_diagnostics.md`.
- Direct Egg-Move harness result: `moves.total=992`, highest loaded move `991:PsychicNoise`, target pointer `0x09A0E94C`, species entries `436 -> 436 -> 436`, highest species `1412`, highest move after/reload `991`, `writeReloadEggMoveMismatches=0`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`.
- No Learnset-Write, Move-Data-Write, Tutor-Text, Special-Tutor, or `setMovesLearnt()` expansion was included.

## 2026-05-13 - CFRU/DPE Learnset-Write-Modell

- Active branch: `analysis/upr-fvx-cfru-dpe-p1-learnset-write-model`.
- UPR-FVX PR #22 und Workspace PR #79 als gemerged geprueft.
- `gLevelUpLearnsets` Write-Modell read-only dokumentiert; keine Aenderung an `02_external/**`.
- Neues Protokoll: `08_tests/randomizer/043_p1_learnset_write_model.md`.
- Befund: Pointer-Ort `0x03EA7C` / `0x0803EA7C`, interne Species-ID-Pointertabelle, Eintraege `u16 move + u8 level`, Sentinel `{0, 0xFF}`, `MAX_LEARNABLE_MOVES=50`, Species bis `SPECIES_PECHARUNT=0x59F`, Moves bis `MOVE_PSYCHICNOISE=0x3DF`.
- Empfehlung: Folgefix nur eng gegatet und zunaechst bounded in-place; Repointing separat modellieren.
