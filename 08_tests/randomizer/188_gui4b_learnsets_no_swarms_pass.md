# GUI-4B Learnsets No-Swarms Pass

## Scope

This records sanitized local GUI-4B evidence after syncing the merged UPR-FVX learnset guard, the Route 1 special-wild diagnosis and the CFRU no-swarms config fix.

Codex did not read, copy, change or generate ROM files. The GUI run, output creation, emulator boot, wild encounter check, Route 1 check and trainer battle check were local user evidence only.

## Pins

- UPR-FVX PR #79: merged.
- UPR-FVX PR #80: merged.
- CFRU PR #5: merged.
- Workspace `02_external/upr-fvx` pin: `226bcacc4f66cee5689caa128d5e35ef4acc001d`.
- Workspace `02_external/CFRU-expansion` pin: `c4c90373fe7f24acd5dcfa3a8fbdd5cb573bfe29`.

## Sanitized Evidence

- Correct CFRU/DPE Gen9 ROM loaded: yes.
- `isRomHack=true`.
- PokemonCount: 1439.
- PokedexCount: 1290.
- Generations 1-9 present: yes.
- GUI randomization completed: yes.
- Options used: Wild Standard/Fallback, Trainer Pokemon core and Pokemon Movesets -> Random completely.
- Trainer Names/Class Names enabled: no.
- Items/Moves/Abilities enabled: no.
- TM/HM/Tutor enabled: no.
- Special-Wild systems enabled: no.
- Output ROM created locally: yes.
- Emulator boot: yes.
- Wild encounters checked: yes.
- Trainer battle checked: yes.
- Missing sprites observed: no.
- Move-less Pokemon observed: no.
- `SpeciesMovesetRandomizer` `IndexOutOfBoundsException` reproduced: no.
- CFRU `SWARM_CHANCE=0` confirmed: yes.
- Route 1 checked after no-swarm rebuild: yes.
- Swarm-Frigibax observed after no-swarm rebuild: no.
- Example Route 1 encounter after fix: Urshifu Lv3, displayed correctly.
- Ogerpon remains valid and pool-eligible: yes.

## Known Remaining Guards

- Remaining console warnings for guarded invalid palette candidates are known and not blockers for this scope.
- Bad Egg and other guarded invalid/special candidates remain protected by existing randomizer guards.

## Boundary

- CFRU Day/Night Wild and other Special-Wild systems remain out-of-scope for the current normal walkthrough goal.
- Swarms are neutralized for normal randomized walkthroughs by `SWARM_CHANCE=0`; this does not promote Swarms as a randomized Special-Wild feature.
- This does not promote any new P1 status.
- Private paths, ROM hashes, file hashes, full logs, screenshots, saves, emulator states, output ROMs, secrets, tokens and `.env` data are omitted.
