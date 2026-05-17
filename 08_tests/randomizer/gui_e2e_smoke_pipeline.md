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

Current sanitized status:

- Ogerpon asset blocker: resolved after syncing DPE PR #2 and UPR-FVX PR #77.
- Updated Pool Asset Report baseline after local DPE+CFRU rebuild: 1186 accepted after guard, 6 excluded total, 1 no-usable-learnset exclusion, 5 invalid/missing front battle sprite pointer exclusions and 5 invalid/missing normal palette pointer exclusions.
- Ogerpon internal slots 1422..1429 now have movesLearntCount 20, learnsetPointerValid true, frontSpritePointerValid true and palettePointerValid true.
- Ogerpon status: accepted.
- Learnset runtime pointer blocker: resolved after syncing UPR-FVX PR #76 plus CFRU/DPE learnset table/repoint fixes.
- GUI-0 passed after UPR-FVX PR #68: GUI opened yes and the correct CFRU/DPE Gen9 ROM loaded yes.
- GUI-1 passed with Wild Standard/Fallback only: randomization completed yes and output ROM created yes.
- GUI-2 passed: output ROM booted locally in BizHawk yes.
- GUI-3 passed: first wild encounter reached yes, with first encounter species recorded as Avalugg Lv2.
- PokemonCount 1439, PokedexCount 1290 and generation counts include 4-9 yes.
- Private paths, logs, hashes and screenshots remain omitted.

### GUI-0: Load Only

- Open the UPR-FVX GUI locally.
- Load the private custom ROM.
- Do not randomize and do not save an output ROM in this stage.
- Result status: passed locally after the null-Species dropdown fix in UPR-FVX PR #68.

### GUI-1: Wild Standard/Fallback Only

- Start from a fresh GUI session or reset options to a known empty/minimal state.
- Enable only Standard/Fallback Wild Encounter randomization.
- Leave all other option groups disabled.
- Generate one local randomized output ROM.
- Result status: passed locally; Wild Standard/Fallback only randomization completed and created an output ROM.

### GUI-2: Boot Output ROM

- Boot the locally generated output ROM in the local emulator.
- Do not document emulator paths, ROM paths, screenshots or full logs.
- Result status: passed locally in BizHawk.

### GUI-3: First Wild Encounter

- Reach the first wild encounter locally.
- Record only whether an encounter was reached.
- Do not document species names, screenshots, save states or route/location details unless a later sanitized scope explicitly asks for them.
- Result status: passed locally; first encounter species was Avalugg Lv2.

### GUI-4+: Later Option Groups

- Add further option groups only after GUI-0 through GUI-3 are clean.
- Each new group should be added in a separate local smoke so failures stay attributable.
- Do not treat any later group as P1-promoted by this pipeline.
- Recommended first GUI-4 candidates: Trainer-Core or Learnsets. Do not jump directly to full randomization.
- With Ogerpon accepted in the updated Pool Asset Report, rerun the local GUI E2E path on the new pins before broadening option groups.

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
Randomization: not yet / yes / no
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

This pipeline is a local GUI E2E compatibility smoke plan only. The GUI-0 sync pins the already-merged UPR-FVX PR #68, and the GUI-1 through GUI-3 pass records sanitized local Output-ROM, BizHawk boot and first-encounter evidence for Wild Standard/Fallback only. It does not make new UPR-FVX code changes in the workspace and does not promote any new feature to P1-supported.

The GUI-1 through GUI-3 pass does not imply support for Trainer Names/Class Names, Learnsets, Items/Moves/Abilities, Special Wild systems or full randomization.
