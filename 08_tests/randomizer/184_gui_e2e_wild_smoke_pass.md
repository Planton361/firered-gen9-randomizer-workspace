# 184 - GUI E2E Wild Smoke Pass

## Scope

This records the first successful local GUI end-to-end smoke for the CFRU/DPE Gen9 ROM path with UPR-FVX pinned at `04bdd8b2f2769bedb1bf6c6ff8fcdecbbf84e29c`.

Codex did not run the GUI, read ROM files, create output ROMs, boot an emulator or inspect logs/screenshots. This document records sanitized local evidence only.

## Sanitized Evidence

- Correct CFRU/DPE Gen9 ROM loaded: yes.
- PokemonCount: 1439.
- PokedexCount: 1290.
- Generation counts include 4-9: yes.
- Options used: Wild Standard/Fallback only.
- Randomization completed: yes.
- Output ROM created: yes.
- Emulator boot: yes.
- First wild encounter reached: yes.
- First encounter species: Avalugg Lv2.
- Private paths/logs/hashes/screenshots omitted: yes.

## Result

GUI-0 through GUI-3 passed for the minimal Wild Standard/Fallback route:

- GUI-0: the correct CFRU/DPE Gen9 ROM loads in the UPR-FVX GUI.
- GUI-1: Wild Standard/Fallback only randomization completes and creates a local output ROM.
- GUI-2: the output ROM boots locally in BizHawk.
- GUI-3: the first wild encounter is reached.

## Boundary

This does not change P1 status. Standard/Fallback Wild Encounters were already P1-supported before this GUI E2E smoke. This pass adds GUI workflow evidence only.

Do not infer support for Trainer Names/Class Names, Learnsets, Items/Moves/Abilities, Special Wild systems, Day/Night Wild, Swarms, Roamers, DexNav, Raids, Wild Double Battles or full randomization from this smoke.

## Next Step

Move to GUI-4 by adding one option group at a time. Start with either a Trainer-Core slice or a Learnsets slice. Do not jump directly to full randomization.
