# UPR-FVX Trainer Better Movesets Pool Rules

Date: 2026-05-26

## Executive Summary

UPR-FVX Trainer Better Movesets is not a strict "current level-up moves only" system. It builds a candidate pool for each eligible trainer Pokemon from the final in-memory ROM state at the time Trainer Better Movesets runs:

- level-up moves for the final trainer species at or below the trainer level,
- some pre-evolution level-up moves at or below the trainer level,
- compatible TM/HM moves,
- compatible Move Tutor moves,
- some egg moves from the first evolution stage,
- then filters, de-duplicates, weights, and picks moves using ability/stat/STAB/move-synergy heuristics.

This means the result is species-/compatibility-legal for the current randomized ROM state, but it is not necessarily level-legal in the narrow "would naturally know this by Lv7" sense. TM, Tutor, and Egg candidates can enter independent of learn level, with probability gates.

## Source-Backed Pool Construction

| Source | Code path | Rule | Level-bound? | Notes |
| --- | --- | --- | --- | --- |
| Final trainer species | `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel` lines 576-585 | Uses `romHandler.getAltFormeOfSpecies(tp.getSpecies(), tp.getForme())`, then `getMovesetForSpecies(...)` for that final trainer species. | Yes for level-up. | This runs after Trainer Pokemon randomization in `GameRandomizer.applyRandomizers` lines 307-308. |
| Level-up moves | `TrainerMovesetRandomizer` lines 578-585 | Adds moves with `ml.level <= tp.getLevel()` and excludes level 0 unless trainer level is at least 30. | Yes. | For CFRU/DPE, `Gen3RomHandler.getMovesLearnt` uses CFRU/DPE level-up learnsets when expanded mode is active. |
| Pre-evolution moves | `TrainerMovesetRandomizer` lines 587-605 | Walks backward through `getEvolutionsTo()`, adds pre-evo level-up moves at or below trainer level with 50% probability per move. | Yes. | Disabled for cyclic evolutions. |
| TM/HM moves | `TrainerMovesetRandomizer` lines 607-624 | Reads current `getTMHMCompatibility()` and current `getTMMoves()`, then probabilistically adds compatible moves. | Not strictly. | Strong damaging moves are favored only when `level * 3 > power * hitCount`; otherwise any TM still has a low `level / 200` chance. |
| Move Tutor moves | `TrainerMovesetRandomizer` lines 626-645 | Same structure as TM/HM, using current `getMoveTutorCompatibility()` and `getMoveTutorMoves()`. | Not strictly. | Requires `romHandler.hasMoveTutors()`. For FRLG/CFRU/DPE this is true. |
| Egg moves | `TrainerMovesetRandomizer` lines 647-665 | Walks to the first evo stage and adds egg moves with 10% probability per move. | No. | Disabled for cyclic evolutions. |
| Final filter | `TrainerMovesetRandomizer` lines 667-675 | Removes null and `MOVE_NONE`, then distincts. | N/A | This is the final raw pool before trimming/scoring. |

## Current Randomized State Matters

`GameRandomizer.applyRandomizers` applies species moveset randomization, TM move randomization, TM/HM compatibility randomization, Move Tutor move randomization, and Move Tutor compatibility randomization before trainer species and Trainer Better Movesets (`GameRandomizer` lines 295-308).

Therefore Better Movesets reads current post-randomization learnsets and compatibility, not necessarily the vanilla/static DPE tables. If Move Tutor Compatibility is randomized or full, a move that is not statically legal for Graveler can still become legal for Better Movesets in that randomized run. If Move Tutor Moves are randomized, an otherwise compatible tutor slot can also teach a different move than in the source table.

For CFRU/DPE Gen9 specifically:

- `Gen3RomHandler.getMovesLearnt` uses CFRU/DPE `gLevelUpLearnsets` in expanded mode (`Gen3RomHandler` lines 5290-5325).
- `getTMMoves` / `getTMHMCompatibility` use CFRU/DPE `gTMHMMoves` and `gTMHMLearnsets` with 120 TM and 128 TM/HM slots (`Gen3RomHandler` lines 6302-6310 and 6442-6458).
- `getMoveTutorMoves` / `getMoveTutorCompatibility` use CFRU/DPE `gMoveTutorMoves` and `gTutorLearnsets` with 152 tutor slots (`Gen3RomHandler` lines 6534-6545 and 6640-6646).
- `getEggMoves` uses CFRU/DPE `gEggMoves` in expanded mode (`Gen3RomHandler` lines 5877-5984).

## How Moves Are Trimmed And Picked

After the pool is built, `trimMoveList` removes globally useless moves, double-battle-only moves when the game is not only multi-battles, obsolete weaker moves, unsupported dependent moves, and hard ability anti-synergy candidates (`TrainerMovesetRandomizer` lines 375-440).

If the remaining pool has 1-4 moves, UPR-FVX writes that whole distinct list directly. If the pool is larger, it:

- duplicates STAB damaging moves into the weighted pool,
- duplicates ability-synergy candidates,
- duplicates stat-synergy candidates,
- biases toward physical or special moves based on the species Attack/Special Attack ratio,
- tries to pick a "good damaging" move first when possible,
- then adjusts later picks using hard/soft move synergies and anti-synergies.

This is why a low-level trainer can receive a mixed set like one high-power damaging move plus setup/status moves if the legal candidate pool includes them.

## Graveler Lv7 Example

Local sanitized observation:

- trainerId `103`
- Graveler Lv7
- raw moves `[412, 393, 111, 97]`
- Tracker names: Hurricane / Rock Polish / Defense Curl / Agility

Source-backed ID mapping:

- `MOVE_HURRICANE` is `0x19C`, decimal `412`, in DPE/CFRU `moves.h`.
- `MOVE_ROCKPOLISH` is `0x189`, decimal `393`.
- `MOVE_DEFENSECURL` is `0x6F`, decimal `111`.
- `MOVE_AGILITY` is `0x61`, decimal `97`.

For stock/static DPE Graveler:

- Graveler's level-up learnset includes Defense Curl at level 1, Rock Polish at levels 1 and 6, and not Hurricane or Agility near level 7.
- TM69 Rock Polish lists Graveler as compatible.
- Tutor 123 Hurricane does not list Graveler.
- Tutor 76 Agility does not list Graveler.

So, with unchanged static DPE compatibility, Hurricane and Agility are not explained as natural Lv7 Graveler moves. They become plausible only if the current randomized ROM state changed tutor/TM compatibility, changed tutor/TM move slots, changed learnsets/egg moves, or used full compatibility. This matches UPR-FVX's ordering: Better Movesets reads the current in-memory compatibility and learnsets after those earlier randomizers.

One more source-backed detail: even a high-power tutor/TM candidate can enter a low-level pool. For TM/Tutor moves, the code first favors damaging moves only when `level * 3 > power * hitCount`, but the fallback branch still allows any move with `random.nextInt(200) < level`. At Lv7 that is a low but nonzero chance per compatible move.

## What This Means For Randomizer Expectations

Better Movesets should be described as "current species/compatibility legal plus heuristic scoring", not as "level-legal moves only".

The local Graveler/Hurricane example is not by itself evidence of stale original trainer moves or bad CFRU runtime move construction. It is evidence that Better Movesets can select powerful, level-independent legal moves when compatibility or tutor/TM sources make them available.

To prove the exact source for one sampled move, the next diagnostic needs the final in-memory sources for that trainer species at the time `TrainerMovesetRandomizer` runs:

- final trainer species and level,
- final `getMovesLearnt()` entries,
- final TM/HM moves and compatibility flags for the species,
- final Move Tutor moves and compatibility flags for the species,
- final egg moves for the first evo stage,
- whether Movesets/TM/Tutor/compatibility randomizers were active.

No ROM paths, raw logs, seeds, output ROMs, saves, hashes, screenshots, or private local addresses should be committed.
