# CFRU Expert AI isolation

Stand: 2026-05-24

## Executive summary

CFRU Expert Difficulty is not a clean "smarter trainer move choice only" switch. For ordinary trainer battles, `GetAIFlags` gives Expert the same conservative trainer-AI uplift that `FLAG_SMART_TRAINER_AI` v2 already applies: trainers without `AI_SCRIPT_CHECK_GOOD_MOVE` gain `AI_SCRIPT_SEMI_SMART`; existing stronger trainer flags are preserved.

That means the local smoke observation "Expert picked smarter moves than Smart Trainer AI v1/v2" is probably not explained by a stronger generic Expert trainer flag combination. The source-backed alternatives are:

- Expert changes trainer construction, especially base IVs, PP and level scaling, which can make damaging moves score better because actual damage/KO calculations change.
- Expert enables separate situational AI behavior outside ordinary move scoring: wild AI, shift-switch logic, switch/anti-cheese handling and item-knowledge behavior.
- `FLAG_SMART_TRAINER_AI` v2 still leaves pure Accuracy-down moves technically valid. Without a damage/KO boost, Sand Attack can remain tied or competitive even without `AI_SCRIPT_CHECK_GOOD_MOVE`.

For v3, a "copy Expert AI" branch is not the right minimal fix. The smallest source-backed direction is either a targeted Smart Trainer AI scoring/tie-break adjustment for utility moves such as Sand Attack, or a deeper Vanilla/NatDex `AI_CheckViability` / `AI_TryToFaint` source-port if exact Ironmon-style behavior is the priority.

## Scope

This analysis is documentation-only. It does not change CFRU source, DPE source, ROMs, saves, builds, emulator states, logs, screenshots or tool binaries.

Primary CFRU paths checked:

- `02_external/CFRU-expansion/src/Battle_AI/ai_master.c`
- `02_external/CFRU-expansion/src/Battle_AI/ai_negatives.c`
- `02_external/CFRU-expansion/src/Battle_AI/ai_positives.c`
- `02_external/CFRU-expansion/src/Battle_AI/ai_advanced.c`
- `02_external/CFRU-expansion/src/Battle_AI/ai_util.c`
- `02_external/CFRU-expansion/src/Battle_AI/ai_switching.c`
- `02_external/CFRU-expansion/src/battle_controller_opponent.c`
- `02_external/CFRU-expansion/src/build_pokemon.c`
- `02_external/CFRU-expansion/src/damage_calc.c`
- `02_external/CFRU-expansion/src/battle_util.c`
- `02_external/CFRU-expansion/src/move_menu.c`

## Key source findings

| File / function | Expert condition | Effect | Category | Smart-AI-only fit |
| --- | --- | --- | --- | --- |
| `ai_master.c` / `GetAIFlags` | `difficulty == OPTIONS_EXPERT_DIFFICULTY` and trainer battle | If trainer lacks `AI_SCRIPT_CHECK_GOOD_MOVE`, ORs `AI_SCRIPT_SEMI_SMART`; does not globally add `AI_SCRIPT_CHECK_GOOD_MOVE`. | Trainer move AI flags | Already matched by v2 for ordinary trainers. |
| `ai_master.c` / `GetAIFlags` | `FLAG_SMART_TRAINER_AI` and trainer battle | v2 ORs `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`; `VAR_GAME_DIFFICULTY` is not read or changed by the hook. | Trainer move AI flags | Current minimal hook. |
| `ai_master.c` / `sBattleAIScriptTable` | Runtime AI flag bits | Bit 0 runs `AIScript_Negatives`, bit 1 runs `AIScript_SemiSmart`, bit 2 runs `AIScript_Positives`. | Move scoring | Important because v1's bit 2 is broader than Expert's regular-trainer uplift. |
| `ai_positives.c` / `AIScript_SemiSmart` | Active only when `AI_SCRIPT_CHECK_GOOD_MOVE` is absent | Delegates selected effects and damaging moves into positive scoring; pure `EFFECT_ACCURACY_DOWN` is not in the SemiSmart effect list. | Move scoring | Safe-ish, but still not a damage-only policy. |
| `ai_negatives.c` / stat-drop negatives | `EFFECT_ACCURACY_DOWN` | Penalizes Accuracy-down only when Accuracy cannot be lowered or Substitute blocks it. A valid Sand Attack is not made bad. | Move scoring | Explains why v2 can still pick Sand Attack in ties. |
| `ai_positives.c` / `AIScript_Positives` | `AI_SCRIPT_CHECK_GOOD_MOVE` | `EFFECT_ACCURACY_DOWN` can gain status viability through `GoodIdeaToLowerAccuracy`. | Move scoring | Do not re-add globally for v3 without targeted tests. |
| `ai_positives.c` / `DamageMoveViabilityIncrease` | Positive/SemiSmart damage path | KO/strongest-damage moves get boosts when damage conditions are met. | Move scoring | Stronger Expert-built mons can make this path fire more often. |
| `build_pokemon.c` / trainer party build | Expert+ | Opponent base IV becomes 31. | Trainer build strength | Not acceptable for Smart-AI-only. |
| `build_pokemon.c` / `GetTrainerMonMovePPBonus` | Expert+ | Trainer move PP bonus becomes max PP. | Trainer build strength | Not acceptable. |
| `build_pokemon.c` / level scaling | Hard+/Expert+ | Hard+ enters average-level scaling; Expert uses smaller subtractor and can force evolution after scaling. | Level scaling / trainer strength | Not acceptable. |
| `battle_controller_opponent.c` / `OpponentHandleChooseMove` | Expert wild battle | Wild Pokemon use the AI move-choice path in Expert. | Wild AI | Not part of Trainer Smart AI. |
| `ai_master.c` / `IsPlayerTryingToCheeseAI` | Expert+ and `AI_SCRIPT_CHECK_GOOD_MOVE` | Rechooses moves against repeated switching / first-turn choice-lock cheese. | Anti-cheese AI | Isolatable only as a separate high-risk feature; not Sand Attack fix. |
| `ai_master.c` / `TryChangeMoveTargetToCounterPlayerProtectCheese` | Expert+ and `AI_SCRIPT_CHECK_GOOD_MOVE` in doubles | Retargets selected moves around Protect-like player behavior. | Doubles anti-cheese AI | Separate feature, not baseline v3. |
| `ai_switching.c` / `ShouldDoAIShiftSwitch` | Hard+ on Shift, Expert+ on Semi-Shift | AI may perform shift-style switch handling after a player KO. | Switch AI | Isolatable separately, but not move scoring. |
| `damage_calc.c` / defender damage-calc data | Expert+ | AI is not forced to hide player type-resist berry knowledge below Expert. | Damage / item knowledge | Situational; not a broad trainer move-selection fix. |
| `move_menu.c` / bag and move restrictions | Hard / Expert | Hard limits items; Expert disables bag and blocks player Minimize/Evasion Up 2. | Player restriction | Not acceptable. |
| `battle_util.c` / sleep clause | Expert+ | Sleep Clause can apply against the player. | Battle rule | Not acceptable. |

## Expert vs `FLAG_SMART_TRAINER_AI`

For ordinary trainer battles, Expert and Smart Trainer AI v2 are closer than the smoke result suggests.

`GetAIFlags` flow:

- Existing trainer flags are loaded from `gTrainers[...]`.
- Hard Difficulty: if this is a trainer battle and the trainer does not already have `AI_SCRIPT_CHECK_GOOD_MOVE`, add `AI_SCRIPT_SEMI_SMART`.
- Expert Difficulty: for trainer battles, the same regular-trainer branch applies; for non-trainers, Expert uses wild smart AI.
- `FLAG_SMART_TRAINER_AI` v2: if this is a trainer battle and the flag is set, OR `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`.

Implication:

- If the sampled trainer starts with only `AI_SCRIPT_CHECK_BAD_MOVE`, Expert and v2 both reach `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`.
- If the sampled trainer already has `AI_SCRIPT_CHECK_GOOD_MOVE`, both Expert and v2 preserve it.
- v1 differed from Expert for regular trainers because v1 forcibly added `AI_SCRIPT_CHECK_GOOD_MOVE`; Expert does not do that for all trainers.

So a simple "move the hook elsewhere in `GetAIFlags`" is unlikely to explain or fix the observed difference for normal trainers.

## Why Expert can look smarter

Expert can still look smarter in local smoke for reasons that are not pure trainer move-AI flags:

- Expert-built opponents can be stronger. `build_pokemon.c` sets opponent base IVs to 31 on Expert+, gives max PP on Expert+, and uses harder level-scaling behavior. Higher stats and levels can change `CanKnockOut`, `MoveKnocksOutXHits`, `StrongestMoveGoesFirst` and related damage checks used by `DamageMoveViabilityIncrease`.
- Expert can alter the battle context. If the comparison accidentally includes wild battles, Expert routes wild opponents into the AI chooser and applies smart wild logic. That is not equivalent to trainer-only Smart AI.
- Expert has situational anti-cheese behavior. Repeated-switch/choice-lock handling and Protect retargeting are Expert-gated and also require `AI_SCRIPT_CHECK_GOOD_MOVE`, but these are not general offensive move-selection rules.
- Expert has selected item/damage knowledge behavior. Type-resist berry knowledge can affect AI damage calculations at Expert, but only in item-specific scenarios.
- Expert shift-switch logic changes switching opportunities, not the per-turn score of Sand Attack versus Tackle.

## Sand Attack explanation

`MOVE_SANDATTACK` has `EFFECT_ACCURACY_DOWN` in the battle move table.

Relevant scoring behavior:

- `AIScript_Negatives` only lowers the score of Accuracy-down moves when the target's Accuracy cannot be lowered or the move is blocked by Substitute. If Sand Attack is legal and useful enough by CFRU's basic checks, it can stay at the default score.
- `AIScript_SemiSmart` only runs when `AI_SCRIPT_CHECK_GOOD_MOVE` is absent. It delegates many effects to `AIScript_Positives`, but pure `EFFECT_ACCURACY_DOWN` is not in that SemiSmart effect list.
- For damaging moves, `AIScript_SemiSmart` can call `DamageMoveViabilityIncrease`, but only non-status moves get that path. A Tackle-like move needs a strongest-move, KO, speed or desperation condition to outscore a still-valid utility move.
- `AIScript_Positives` does directly boost Accuracy-down through `GoodIdeaToLowerAccuracy`; this is why v1 was especially prone to Sand Attack / utility spam.

Inference from source: v2 Sand Attack spam is likely not caused by SemiSmart actively boosting pure Accuracy-down. It is more likely that Sand Attack remains an unpenalized default-score move while Tackle does not receive a large enough damage boost in that state. Expert can hide this by changing damage-relevant stats/levels, not necessarily by using a better generic trainer AI flag mix.

## Isolatable Expert AI components

These pieces can be considered separately from `VAR_GAME_DIFFICULTY`, but each needs its own design and smoke tests:

- Trainer SemiSmart uplift: already isolated by `FLAG_SMART_TRAINER_AI` v2.
- Switch-out intelligence in `ai_switching.c`: many paths key off `AI_THINKING_STRUCT->aiFlags > AI_SCRIPT_CHECK_BAD_MOVE`; v2 may already enable some of these during trainer AI processing. This is switch behavior, not direct move scoring.
- Shift-switch prediction: `ShouldDoAIShiftSwitch` is difficulty-gated and could theoretically be ported behind a separate flag, but it changes battle pacing and is not an offensive move-choice fix.
- Expert anti-cheese: `IsPlayerTryingToCheeseAI` and `TryChangeMoveTargetToCounterPlayerProtectCheese` are isolatable only as explicit "anti-cheese" features. They require careful fairness decisions and do not address early Sand Attack behavior.
- Item/damage knowledge: Expert's type-resist berry behavior is isolatable but narrow and item-specific.

## Not acceptable for Smart-AI-only

Do not use these Expert Difficulty effects for the baseline Smart Trainer AI option:

- Opponent base IV 31 on Expert.
- Hard+/Expert EV and friendship helpers.
- Expert max PP bonus.
- Hard+/Expert level scaling and Expert evolution-after-scaling behavior.
- Player bag restrictions.
- Player Minimize / Evasion Up 2 restrictions.
- Expert Sleep Clause and other battle-rule changes.
- Expert wild AI activation.
- Raid-specific behavior.
- Broad Expert anti-cheese or shift-switch behavior unless it is separately requested and tested.
- Any `VAR_GAME_DIFFICULTY` change from Normal as an activation shortcut.

## v3 recommendation

Recommended v3 direction:

1. Keep `FLAG_SMART_TRAINER_AI` v2 as the baseline flag behavior for now.
2. Do not add `AI_SCRIPT_CHECK_GOOD_MOVE` back globally.
3. Add a targeted source-backed scoring experiment only if local v2 smoke remains bad:
   - penalize repeated or pure Accuracy-down utility when a damaging move is available, or
   - add a Smart Trainer AI tie-break that prefers reasonable damage over neutral utility, or
   - implement a closer Vanilla/NatDex `AI_CheckViability` / `AI_TryToFaint` source-port.

Ranking of candidate approaches:

| Option | Fit | Reason |
| --- | --- | --- |
| Expert-AI-only branch without difficulty side effects | Weak | The generic trainer flag part is already v2; other Expert pieces are situational or invasive. |
| Vanilla/NatDex source-port | Strong if Ironmon fidelity matters | Public source analysis points to trainer `aiFlags |= 0x07` with different vanilla scoring semantics than CFRU `AIScript_Positives`. |
| Different hook in `GetAIFlags` | Weak | The v2 hook runs after difficulty handling and already produces the Expert-like trainer flag uplift. |
| Flag combination plus Sand Attack / utility adjustment | Strongest minimal v3 | Directly targets the observed failure without importing trainer strength or player restrictions. |

## Open questions

- Does the local Expert smoke use the exact same trainer, party, RNG path and player state as the v2 smoke?
- Was the Expert comparison against a trainer battle only, or did it include wild behavior?
- Did the sampled trainer already have `AI_SCRIPT_CHECK_GOOD_MOVE` in trainer data?
- Did Expert level/IV scaling change whether Tackle could KO or become the strongest boosted move?
- Should v3 be "Ironmon fidelity" or "randomizer-friendly offensive pressure"? Those may require different scoring rules.
