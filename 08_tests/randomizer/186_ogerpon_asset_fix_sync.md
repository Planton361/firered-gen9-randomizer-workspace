# Ogerpon Asset Fix Sync

## Scope

This document records sanitized local Pool Asset Report evidence after syncing the merged DPE Ogerpon asset fix and the merged UPR-FVX Ogerpon sprite/palette diagnosis into the workspace.

Codex did not read, copy, modify or generate ROM files. The local DPE+CFRU rebuild and report execution were performed outside this workspace sync, and only sanitized aggregate evidence is recorded here.

## Synced Fixes

- DPE PR #2: maps Ogerpon Terastal/Internal slots 1426..1429 to existing base/mask Ogerpon Battle/UI assets.
- UPR-FVX PR #77: adds sanitized Ogerpon front sprite and palette diagnostics to the opt-in Pool Asset Report.

## Workspace Pins

- `02_external/Dynamic-Pokemon-Expansion-Gen-9`: `3d0ac870fadc91e55f6ff19c0f7aae3cac2014a1`.
- `02_external/upr-fvx`: `d6415d59a8b94b4d6d4c1e424a73c0f426993d03`.

## Sanitized Evidence

- PokemonCount: 1439.
- PokedexCount: 1290.
- candidate count before guard: 1192.
- accepted count after guard: 1186.
- excluded count: 6.
- excluded no usable learnset: 1.
- excluded invalid/missing front battle sprite pointer: 5.
- excluded invalid/missing normal palette pointer: 5.
- Ogerpon internal 1422..1429:
  - movesLearntCount: 20.
  - learnsetPointerValid: true.
  - frontSpritePointerValid: true.
  - palettePointerValid: true.
- Ogerpon status: accepted.
- Remaining invalid candidates:
  - Bad Egg: no usable learnset.
  - Warrior, Exeggcute, Cubone, Koffing and Mime Jr.: invalid/missing front battle sprite pointer.
- Private paths, hashes, full logs and screenshots are omitted.

## Effect

The Ogerpon asset blocker is resolved for the sanitized local report. Ogerpon now has valid learnset, front sprite and normal palette evidence across internal slots 1422..1429 and is accepted by the guard.

The remaining exclusions are outside Ogerpon and remain separate follow-up candidates.

## Boundary

No P1 status changes are made by this sync. This is evidence for the asset-guard/report baseline and the next local GUI retest only.
