# GUI-4A Wild/Trainer Ogerpon Pass

## Scope

This records sanitized local GUI-4A evidence after the Ogerpon asset fix and the merged UPR-FVX PR #78 sync.

Codex did not read, copy, change or generate ROM files. The GUI run, output creation, emulator boot, wild encounter check and trainer battle check were local user evidence only.

## Pins

- UPR-FVX PR #78: merged.
- Workspace `02_external/upr-fvx` pin: `18e184b2c22451c74b4ba46bd7203c579d3bc9e7`.

## Sanitized Evidence

- Correct CFRU/DPE Gen9 ROM loaded: yes.
- `isRomHack=true`.
- PokemonCount: 1439.
- PokedexCount: 1290.
- Generations 1-9 present: yes.
- GUI randomization completed: yes.
- Options used: Wild Standard/Fallback plus Trainer Pokemon core.
- Trainer Names/Class Names enabled: no.
- Learnsets enabled: no.
- Items/Moves/Abilities enabled: no.
- Special-Wild systems enabled: no.
- Output ROM created locally: yes.
- Emulator boot: yes.
- Wild encounters checked: yes.
- Trainer battle checked: yes.
- Missing sprites observed: no.
- Move-less Pokemon observed: no.
- Ogerpon appears in Trainer output/log: yes.
- Ogerpon pool eligibility after asset fix: yes.

## Known Remaining Guards

- Bad Egg: no usable learnset.
- Warrior, Exeggcute, Cubone, Koffing and Mime Jr.: invalid/missing front battle sprite/palette.

## Boundary

- CFRU Day/Night Wild, Swarms and other Special-Wild systems remain out-of-scope for the current normal walkthrough goal.
- This does not promote any new P1 status.
- Private paths, ROM hashes, file hashes, full logs, screenshots, saves, emulator states, output ROMs, secrets, tokens and `.env` data are omitted.
