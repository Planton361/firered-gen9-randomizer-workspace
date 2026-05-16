# GUI E2E Smoke Pipeline

## Scope

This document defines the fastest local GUI end-to-end smoke for the private custom ROM with the pinned UPR-FVX workspace state.

Codex does not run this smoke. The GUI, ROM loading, randomized output creation, emulator boot and first encounter check are local-only user steps.

The goal is quick GUI compatibility evidence:

1. Load the private custom ROM in the UPR-FVX GUI.
2. Randomize only the smallest currently supported option slice.
3. Produce a local randomized ROM.
4. Boot the randomized ROM locally.
5. Record only sanitized yes/no results.

## Fastest Order

### GUI-0: Load Only

- Open the UPR-FVX GUI locally.
- Load the private custom ROM.
- Do not randomize and do not save an output ROM in this stage.
- Result target: prove the GUI accepts and identifies the custom ROM without documenting private details.

### GUI-1: Wild Standard/Fallback Only

- Start from a fresh GUI session or reset options to a known empty/minimal state.
- Enable only Standard/Fallback Wild Encounter randomization.
- Leave all other option groups disabled.
- Generate one local randomized output ROM.
- Result target: prove the smallest P1-supported GUI path can write an output ROM.

### GUI-2: Boot Output ROM

- Boot the locally generated output ROM in the local emulator.
- Do not document emulator paths, ROM paths, screenshots or full logs.
- Result target: prove the generated ROM starts locally.

### GUI-3: First Wild Encounter

- Reach the first wild encounter locally.
- Record only whether an encounter was reached.
- Do not document species names, screenshots, save states or route/location details unless a later sanitized scope explicitly asks for them.
- Result target: prove the minimal Wild Standard/Fallback GUI output reaches gameplay evidence.

### GUI-4+: Later Option Groups

- Add further option groups only after GUI-0 through GUI-3 are clean.
- Each new group should be added in a separate local smoke so failures stay attributable.
- Do not treat any later group as P1-promoted by this pipeline.

## Initially Disabled

Do not enable these groups in GUI-1:

- Trainer Names/Class Names.
- Learnsets.
- Items/Moves/Abilities.
- Special Wild systems.
- Day/Night Wild.
- Swarms.
- Roamers.
- DexNav.
- Raids.
- Wild Double Battles.

Trainer Names/Class Names currently has only a ROM-facing smoke harness prepared and remains below P1-supported. Learnsets and Items/Moves/Abilities have ROM-free evidence slices only for this pipeline decision. Special Wild systems remain outside the Standard/Fallback Wild Encounter scope.

## Sanitized Result Format

Use this exact structure for local handoff notes:

```text
GUI opened: yes/no
Custom ROM loaded: yes/no
Options used: Wild Standard/Fallback only
Output ROM created: yes/no
Emulator boot: yes/no
First wild encounter reached: yes/no
Error summary: sanitized, no paths/logs/hashes
```

Allowed error summaries:

- Short plain-language failure category.
- GUI stage where the failure happened.
- Whether retrying with the same minimal option set reproduced the failure.

Do not include:

- ROM paths.
- Output ROM paths.
- ROM hashes or file hashes.
- Full logs or stack traces.
- Screenshots with private paths.
- Save files, emulator states or build artifacts.
- Tokens, secrets or `.env` data.

## Evidence Boundary

This pipeline is a local GUI E2E compatibility smoke plan only. It does not add ROM evidence by itself, does not update the UPR-FVX submodule pin, does not change UPR-FVX code and does not promote any new feature to P1-supported.
