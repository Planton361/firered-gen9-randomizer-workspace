# CFRU/DPE Learnset Runtime Fixes Sync

## Scope

This document records sanitized local Pool Asset Report evidence after syncing the merged UPR-FVX, CFRU and DPE learnset runtime fixes into the workspace.

Codex did not read, copy, modify or generate ROM files. The local rebuild and report execution were performed outside this workspace sync, and only sanitized aggregate evidence is recorded here.

## Synced Fixes

- UPR-FVX PR #76: reads the CFRU runtime learnset pointer for CFRU/DPE builds.
- CFRU PR #3: records direct `gLevelUpLearnsets` runtime repoints into `generatedrepoints`.
- CFRU PR #2: adds the `gLevelUpLearnsets` runtime repoint and Ogerpon internal mappings.
- DPE PR #1: adds Ogerpon Terastal learnset mappings.

## Sanitized Evidence

- PokemonCount: 1439.
- PokedexCount: 1290.
- maxInternalSpeciesId: 1439.
- accepted count after guard: 1185.
- excluded count: 7.
- excluded no usable learnset: 1.
- excluded invalid/missing front battle sprite pointer: 6.
- excluded invalid/missing normal palette pointer: 6.
- cfruRuntimeLearnsetPointerOffset: `0x1167134`.
- chosenLearnsetTableBase: `0x1167134`.
- Ogerpon movesLearntCount: 20.
- Ogerpon learnsetPointerValid: true.
- Ogerpon remains excluded because of invalid/missing front battle sprite pointer.
- Private paths, hashes, full logs and screenshots are omitted.

## Effect

The learnset runtime pointer blocker is resolved for the sanitized local report: the Pool Asset Report improved from 436 accepted / 756 no-learnset exclusions to 1185 accepted / 1 no-learnset exclusion.

Ogerpon now has a valid learnset and moves in the report. The next technical blocker is Ogerpon's invalid or missing front battle sprite pointer, not learnset loading.

## Boundary

No P1 status changes are made by this sync. This is evidence for the asset-guard/report baseline and the next GUI compatibility blocker only.
