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

- GUI Working Settings Matrix is recorded after syncing UPR-FVX PR #88 and PR #89.
- UPR-FVX pin: `f3a6d04ff6db8d48468800194e0baffbafb7505c`.
- Working settings passed: Wild Standard/Fallback, Trainer Pokemon core, Pokemon Movesets -> Random completely, Trainer Movesets, Trainer Names, Field Items basic, Pokemon Abilities, TM/HM Compatibility, TM Moves, Move Tutor Moves, Move Tutor Compatibility, Shop Items, Pickup Items, In-Game Trades, Static Pokemon, Type Effectiveness, Pokemon Base Statistics and Move Data Power/Accuracy/PP/Type/Names.
- In-Game Trades passed after PR #89 with no `NEW GIVEN = ?` observed in sanitized evidence.
- Evolutions unchanged are preserved and swarms remain disabled by CFRU `SWARM_CHANCE=0`.
- Trainer Class Names is class-text remapping only: class id and sprite remain unchanged, so sprite/class visual mismatch is expected. Recommend off for the stable visual profile.
- Starter Pokemon remains caveated: player starter choices randomize, but rival first-battle sync is unresolved/blocked.
- Special-Wild remains out-of-scope. Shop Items evidence covers supported/special shops, Pickup Items are log-confirmed, Static null placeholders remain null and Base Stats ability-name log display may appear truncated while ingame names are correct.
- Trainer Names/Class Names GUI-smoke is recorded after syncing UPR-FVX PR #83, PR #85 and PR #86.
- UPR-FVX pin: `f86315e7528ba3257df03b80c0c75ccc69ef574b`.
- Trainer Names are visibly changed in the Trainer Pokemon log.
- Trainer Class Names no longer collapse to `Director` or `[PKMN] BREEDER`.
- Trainer Class Names pass as global class-label remapping: the same original class gets the same new class label.
- Per-trainer class assignment is not part of this option and remains a separate possible future feature.
- Evolutions remain correct, including Squirtle -> Wartortle Lv16.
- Wild Standard/Fallback, Trainer Pokemon core and Pokemon Movesets -> Random completely remain stable; swarms remain disabled.
- Missing sprites observed: no. Move-less Pokemon observed: no.
- Evolution row-stride fix is synced after UPR-FVX PR #82.
- UPR-FVX pin: `485f0b899c84470f3fab82317331a671ec023ac1`.
- CFRU/DPE uses `EVOS_PER_MON=16`; the UPR-FVX evolution report/read/write path now uses `evolutionSlotsPerSpecies=16` and `evolutionRowSize=0x80`.
- Sanitized local Evolution Report evidence after PR #82 shows the private input ROM starter chains correct and a newly generated output preserving starter evolutions.
- Correct starter chain baseline: Bulbasaur -> Ivysaur Lv16, Ivysaur -> Venusaur Lv32, Charmander -> Charmeleon Lv16, Charmeleon -> Charizard Lv36, Squirtle -> Wartortle Lv16 and Wartortle -> Blastoise Lv36.
- Sanitized ingame smoke evidence after PR #82: Squirtle evolved at Lv16 in a new FVX output.
- Previous bad/Test13-style outputs are stale and must not be used for current validation.
- Next recommended option block: Trainer Names/Class Names or a first Items/Moves/Abilities slice, with Special-Wild systems still disabled.
- GUI-4B passed with Wild Standard/Fallback plus Trainer Pokemon core plus Pokemon Movesets -> Random completely after syncing UPR-FVX PR #79, UPR-FVX PR #80 and CFRU PR #5.
- UPR-FVX pin: `226bcacc4f66cee5689caa128d5e35ef4acc001d`.
- CFRU pin: `c4c90373fe7f24acd5dcfa3a8fbdd5cb573bfe29`.
- Correct CFRU/DPE Gen9 ROM loaded with `isRomHack=true`, PokemonCount 1439, PokedexCount 1290 and generations 1-9 present.
- Output ROM was created locally, emulator boot succeeded, wild encounters were checked and a trainer battle was checked.
- Missing sprites observed: no. Move-less Pokemon observed: no.
- `SpeciesMovesetRandomizer` empty-moveset `IndexOutOfBoundsException` was not reproduced.
- CFRU `SWARM_CHANCE=0` was confirmed; Route 1 no-swarm rebuild did not observe Swarm-Frigibax and an example Route 1 encounter was Urshifu Lv3 displayed correctly.
- Ogerpon remains valid and pool-eligible. Remaining guarded invalid palette candidates are known warnings and not blockers.
- GUI-4A passed with Wild Standard/Fallback plus Trainer Pokemon core after syncing UPR-FVX PR #78.
- Correct CFRU/DPE Gen9 ROM loaded with `isRomHack=true`, PokemonCount 1439, PokedexCount 1290 and generations 1-9 present.
- GUI randomization completed, output ROM was created locally, emulator boot succeeded, wild encounters were checked and a trainer battle was checked.
- Missing sprites observed: no. Move-less Pokemon observed: no.
- Ogerpon appears in Trainer output/log and is pool-eligible after the Ogerpon Learnset/Sprite/Palette fixes.
- CFRU Day/Night Wild, Swarms and other Special-Wild systems remain out-of-scope for the current normal walkthrough goal.
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
- GUI-4A result: Wild Standard/Fallback plus Trainer Pokemon core passed in sanitized local evidence.
- GUI-4B result: Learnsets passed when layered on the now-passed Wild Standard/Fallback plus Trainer Pokemon core path, with CFRU swarms neutralized by `SWARM_CHANCE=0`.
- GUI-4C result: Trainer Names/Class Names passed as global class-label remapping on the current stable path.
- GUI Working Settings Matrix result: broad local settings matrix passed after fixes through UPR-FVX PR #89, with the caveats documented above.
- Recommended next candidate: isolate Starter Pokemon/rival starter sync, or repeat the stable visual profile with Trainer Class Names, Starters and Special-Wild disabled.
- Keep Special-Wild disabled unless explicitly selected as a separate diagnostic smoke.

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

Trainer Names has a sanitized local GUI-smoke pass but remains below P1-supported. Trainer Class Names is class-text remapping only and should stay disabled in a stable visual profile unless the sprite/class-id mismatch is acceptable. Special Wild systems remain outside the Standard/Fallback Wild Encounter scope.

## Sanitized Result Format

Use this exact structure for local handoff notes:

```text
GUI opened: yes/no
Custom ROM loaded: yes/no
Randomization: not yet / yes / no
Options used: Wild Standard/Fallback only / Wild Standard/Fallback + Trainer Pokemon core / other narrow block
Output ROM created: yes/no
Emulator boot: yes/no
First wild encounter reached: yes/no
Trainer battle checked: yes/no/not in scope
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

This pipeline is a local GUI E2E compatibility smoke plan only. The GUI-0 sync pins the already-merged UPR-FVX PR #68, the GUI-1 through GUI-3 pass records sanitized local Output-ROM, BizHawk boot and first-encounter evidence for Wild Standard/Fallback only, and GUI-4A records sanitized Wild Standard/Fallback plus Trainer Pokemon core evidence after the Ogerpon asset fix. It does not make new UPR-FVX code changes in the workspace and does not promote any new feature to P1-supported.

The GUI-4B pass does not imply support for Special Wild systems or full randomization. GUI-4C records Trainer Names/Class Names only as a sanitized GUI-smoke pass, not as P1 support. The GUI Working Settings Matrix records broad local evidence after PR #89, still without P1 promotion. CFRU Day/Night Wild and other Special-Wild systems remain outside the current normal walkthrough scope. Swarms are neutralized for normal randomized walkthroughs by `SWARM_CHANCE=0`, not promoted as a randomized Special-Wild feature.

The evolution row-stride sync documents a corrected CFRU/DPE evolution table path and sanitized report evidence only. It does not promote Evolution randomization settings or any new GUI option group to P1-supported.
