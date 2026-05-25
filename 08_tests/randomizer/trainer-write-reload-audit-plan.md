# UPR-FVX Trainer Write/Reload Audit Plan

## Goal

Separate the remaining Route-22 Rival / Trainer Better-Movesets symptoms into three layers:

1. Final UPR-FVX in-memory `TrainerPokemon` state after Trainer Pokemon randomization, Rival carryover reapply, and Trainer Better Movesets.
2. Gen3/CFRU-DPE trainer data as written to and reloaded from the output ROM.
3. CFRU runtime `gBattleMons` construction observed by the Tracker extension.

No ROMs, saves, screenshots, raw logs, hashes, private paths, or generated builds belong in the repository.

## New Source-Backed Diagnostic Coverage

UPR-FVX now extends the existing FRLG runtime trainer-source diagnostics:

- `Gen3RomHandler.FrlgRawTrainerPokemonDiagnostics` includes raw custom move words when the trainer party has custom moves.
- Post-randomization runtime-source audit rows include raw move lists in `outputRawParty` formatting.
- The audit warns when raw output trainer data has `MOVE_NONE` in slot 0 while later slots contain real moves.
- The audit warns when a Route-22 protected Rival starter slot does not match the final Oak-Lab opening Rival starter raw Species.

This is diagnostic-only. It does not change Trainer randomization, Better Movesets, writer normalization, CFRU runtime, or Tracker code.

## ROM-Free Regression Checks

The synthetic `Gen3OakLabRivalScriptTest` additions prove that:

- raw trainer diagnostics decode custom move slots,
- `[-/Move/Move/Move]` raw rows are flagged,
- Route-22 protected starter mismatch is flagged at the raw trainer-source layer.

These tests do not prove a private output ROM was generated from the current jar/settings. They prove the audit can identify the relevant failures when they exist in raw trainer data.

## Local Private-ROM Audit

Use only local private ROM paths and keep generated reports out of commits.

Suggested command shape from `02_external/upr-fvx`:

```sh
./gradlew :romio:test --tests '*Gen3OakLabRivalRuntimeSourceRomTest.trainerRuntimeSourcePostRandomizationAuditReportOptIn*' \
  -Duprfvx.trainerRuntimeSourceBaseRom=<private-base-rom> \
  -Duprfvx.trainerRuntimeSourceRandomizedRom=<private-output-rom>
```

The `romio:test` Gradle task forwards these two `-D` properties into the forked test JVM. If the test is still
reported as `SKIPPED`, inspect the local Gradle test XML/HTML first to confirm whether the test executor received both
properties before interpreting missing report files as audit logic failure.

Inspect the local report under UPR-FVX `build/reports/diagnostics/`.
The test also prints a sanitized line with the relative report path, for example:

```text
[UPRFVX-DIAG] reportPath=build/reports/diagnostics/trainer-runtime-source-post-randomization-audit-report.txt
```

The post-randomization audit prints a sanitized summary and any core warnings to the test output. If the report cannot be written, the test fails with the relative target path.
If a configured ROM crashes during load, the test should fail without printing the private path and identify the role:
`Configured base ROM could not be loaded during <phase>: <ExceptionClass>` or
`Configured randomized ROM could not be loaded during <phase>: <ExceptionClass>`.
Current sanitized load phases include detection, setup, item table load, pokemon data load, evolution load, move table
load, pokemon palette load, trainer load, ability table load, and evolution-level estimate.

Interpretation:

- If `outputRawParty` already shows `moves=[0, ...]`, the failure is in output-ROM trainer data or stale output ROM generation, not CFRU runtime.
- If the report warns `route22 protected starter differs`, the output ROM raw Route-22 starter slot is wrong.
- If raw output parties are compact and Route-22 protected slots match, but `gBattleMons` still shows broken moves/starters, investigate CFRU runtime trainer construction or confirm the smoke used a fresh output ROM and save context.
- If the audit does not show the target Trainer IDs, inspect whether the battle uses a trainer source row outside the loaded/runtime-source set.

## Minimal Manual Smoke

1. Build or run the local randomizer from the current UPR-FVX branch.
2. Generate a fresh private output ROM from the same settings profile.
3. Start from a clean local test context, not a stale save state.
4. Run the post-randomization runtime-source audit above.
5. Then use CFRUDPEExtension `gBattleMons` only as the runtime layer check.

Record only sanitized findings: trainer ID if known, party slot, Species name, Level, move names, and whether the row is the protected Rival starter slot.

## Current Boundary

This audit answers whether the bad row is visible in raw UPR-FVX-written trainer data. It does not directly prove final in-memory state during a full private randomizer run unless paired with a local run/report from the same generated output ROM.
