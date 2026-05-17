# 190 - Trainer Names/Class Names Pass

## Scope

Sync merged UPR-FVX PR #83, PR #85 and PR #86 and record sanitized local GUI-smoke evidence for Trainer Names and Trainer Class Names.

Codex did not read, copy, change or generate ROMs.

## Synced Pin

- UPR-FVX PR #83: `test: diagnose cfru dpe trainer names unchanged`.
- UPR-FVX PR #85: `fix: shuffle existing trainer class names`.
- UPR-FVX PR #86: `test: diagnose cfru dpe trainer class source mismatch`.
- Workspace submodule `02_external/upr-fvx`: `f86315e7528ba3257df03b80c0c75ccc69ef574b`.

## Sanitized Evidence

- Trainer Names + Trainer Class Names GUI-smoke run locally: yes.
- Trainer Names visibly changed in the Trainer Pokemon log: yes.
- Trainer Class Names collapse to `Director`: no.
- Trainer Class Names collapse to `[PKMN] BREEDER`: no.
- Trainer Class Names behave as global class-label remapping: yes.
- Same original class receives the same new class label: yes.
- Per-trainer class assignment tested or supported by this option: no.
- Evolutions remain correct: yes.
- Squirtle -> Wartortle Lv16: yes.
- Wild Standard/Fallback remains stable: yes.
- Trainer Pokemon core remains stable: yes.
- Pokemon Movesets -> Random completely remains stable: yes.
- Swarms remain disabled: yes.
- Missing sprites observed: no.
- Move-less Pokemon observed: no.

## Interpretation

- Trainer Names passed for the current GUI-smoke path.
- Trainer Class Names passed as class-label remapping.
- PR #83 fixed stale Trainer Pokemon log names after trainer text changes.
- PR #85 replaced weak Custom-Class-pool behavior with existing-class label shuffling.
- PR #86 fixed the Gen3 loaded trainer class id used by the `fullDisplayName` refresh path.
- Per-trainer class assignment is a separate possible future feature, not part of the current option.

## Next Recommended Option Block

- Keep Special-Wild systems disabled.
- Keep swarms disabled.
- Choose one separate first Items/Moves/Abilities slice.
- Keep reporting sanitized yes/no evidence only.

## Safety Boundary

- No ROM paths.
- No output ROM paths.
- No hashes.
- No screenshots.
- No full logs.
- No saves or emulator states.
- No secrets, tokens or `.env` details.
- No P1 promotion.
