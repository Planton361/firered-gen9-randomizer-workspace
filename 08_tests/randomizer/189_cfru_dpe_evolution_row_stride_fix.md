# 189 - CFRU/DPE Evolution Row Stride Fix

## Scope

Sync merged UPR-FVX PR #82 and record sanitized Evolution Report evidence for the CFRU/DPE Gen9 evolution table row stride.

Codex did not read, copy, change or generate ROMs.

## Synced Pin

- UPR-FVX PR #82: `fix: use cfru dpe evolution row stride`.
- Workspace submodule `02_external/upr-fvx`: `485f0b899c84470f3fab82317331a671ec023ac1`.

## Finding

- CFRU/DPE uses `EVOS_PER_MON=16`.
- Old UPR-FVX evolution read/write/report logic used the vanilla 5-slot row stride.
- Vanilla row stride: `5 * 8 = 0x28`.
- CFRU/DPE row stride: `16 * 8 = 0x80`.
- The old report could read the private input ROM incorrectly even when the ROM evolved correctly ingame.
- The old writer path could corrupt output evolutions; previous bad/Test13-style outputs are stale and must not be reused.

## Sanitized Evidence

- PR #82 uses `evolutionSlotsPerSpecies=16` and `evolutionRowSize=0x80` for CFRU/DPE Gen9.
- Local report after PR #82: Input ROM starter chains correct.
- Local report after PR #82: new Output ROM starter chains correct.
- Ingame smoke after PR #82: Squirtle evolved at Lv16 in a new FVX output.

Starter chain baseline:

- Bulbasaur -> Ivysaur Lv16.
- Ivysaur -> Venusaur Lv32.
- Charmander -> Charmeleon Lv16.
- Charmeleon -> Charizard Lv36.
- Squirtle -> Wartortle Lv16.
- Wartortle -> Blastoise Lv36.

## Next Recommended Option Block

- Keep Special-Wild systems disabled.
- Choose one separate narrow scope, preferably Trainer Names/Class Names or a first Items/Moves/Abilities slice.
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
