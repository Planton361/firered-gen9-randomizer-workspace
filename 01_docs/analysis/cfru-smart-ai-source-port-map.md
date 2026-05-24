# CFRU Smart Trainer AI Source-Port Map

## Executive Summary

This note maps the CFRU code paths that could support a future "Smart Trainer AI only" option without setting `VAR_GAME_DIFFICULTY` to Hard or Expert.

The cleanest source-port target is trainer AI flag selection in `GetAIFlags`: CFRU Hard/Expert can add `AI_SCRIPT_SEMI_SMART` for trainers that do not already have `AI_SCRIPT_CHECK_GOOD_MOVE`. That behavior is narrower than full runtime difficulty and can plausibly be isolated behind a new trainer-AI option.

Follow-up mapping against the Ironmon/NatDex `0x07` finding changes the implementation recommendation: if the goal is to be close to the NatDex/Ironmon Smart-AI Randomizer, CFRU v1 should prefer the three-bit trainer-AI combination `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE` over `AI_SCRIPT_SEMI_SMART` alone. `AI_SCRIPT_SEMI_SMART` alone remains the more conservative CFRU-only uplift, but it is not the closest `0x07` equivalent.

The full `VAR_GAME_DIFFICULTY` path is not suitable as a Smart-AI-only switch. Hard/Expert also affect trainer Pokemon construction, trainer level scaling, player item and move restrictions, battle rules, wild encounters and raid edge cases. Those paths should not be ported into a Randomizer/Ironmon-style "better trainer AI" option unless explicitly requested as a broader hard-mode profile.

## Source Anchors

| File / function | Existing condition | Effect | Portability for Smart Trainer AI only |
| --- | --- | --- | --- |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c` / `GetAIFlags` | `VarGet(VAR_GAME_DIFFICULTY) == OPTIONS_EASY_DIFFICULTY` for trainer battles | Downgrades trainer AI: removes `AI_SCRIPT_CHECK_GOOD_MOVE` and adds `AI_SCRIPT_SEMI_SMART`, or falls back to `AI_SCRIPT_CHECK_BAD_MOVE`. | Do not port for Smart AI. This is Easy-mode weakening, not smarter trainer behavior. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c` / `GetAIFlags` | `OPTIONS_HARD_DIFFICULTY` for trainer battles | If trainer lacks `AI_SCRIPT_CHECK_GOOD_MOVE`, adds `AI_SCRIPT_SEMI_SMART`. | Best minimal source-port target. It improves trainer AI flags without requiring trainer stat or rule changes. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c` / `GetAIFlags` | `OPTIONS_EXPERT_DIFFICULTY` for trainer battles | Same trainer uplift as Hard when no `AI_SCRIPT_CHECK_GOOD_MOVE`; wild battles get a separate smart-wild path. | Trainer portion is portable; wild portion should be separate. |
| `02_external/CFRU-expansion/include/battle.h` | `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_SEMI_SMART`, `AI_SCRIPT_CHECK_GOOD_MOVE` | Defines the AI flag tiers used by battle AI. | A new option should alter these flags, not `VAR_GAME_DIFFICULTY`. |
| `02_external/CFRU-expansion/src/battle_controller_opponent.c` / `OpponentHandleChooseMove` | Trainer, Oak, Safari, Roamer, `FLAG_SMART_WILD`, Expert wild, Shadow Warrior, `WildMonIsSmart`, raid checks | Decides when to run battle AI move choice via `BattleAI_SetupAIData` and `BattleAI_ChooseMoveOrAction`. | Trainer-AI mode can reuse the normal trainer path. Wild/raid entry conditions should remain separate. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_switching.c` / smart-switch heuristics | Several checks use `AI_THINKING_STRUCT->aiFlags > AI_SCRIPT_CHECK_BAD_MOVE` | Better AI flags can indirectly enable stronger switching/item-style heuristics, not just move scoring. | Important side effect. Must be tested if `AI_SCRIPT_SEMI_SMART` is added globally for trainers. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c` / `ShouldPredictRandomPlayerSwitch` | Frontier or `VarGet(VAR_GAME_DIFFICULTY) >= OPTIONS_HARD_DIFFICULTY` | Allows player-switch prediction in some AI paths. | Optional second tier only; tightly tied to difficulty today. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_switching.c` / `ShouldDoAIShiftSwitch` | Shift style plus Hard+, or Semi-Shift plus Expert+ | Lets AI use shift-switch behavior after predictions. | Optional and invasive enough to gate separately from basic Smart Trainer AI. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c` / `IsPlayerTryingToCheeseAI` | Very-smart AI plus Expert+ for repeated switch or choice-lock cheese detection | Detects selected anti-cheese patterns from player behavior. | Do not include in the baseline Smart Trainer AI option; consider only as an explicit advanced tier. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c` / `TryChangeMoveTargetToCounterPlayerProtectCheese` | Doubles, non-Frontier, Expert+, very-smart AI, opponent side | Retargets moves to counter repeated Protect-style behavior. | Do not include in baseline. This is Expert-specific anti-cheese behavior. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c` / `WildMonIsSmart` | `FLAG_SMART_WILD`, special wild forms, Hard+ smartWild, raids, `WILD_ALWAYS_SMART` | Adds smart flags to wild AI. | Keep separate from trainer AI. Do not reuse as the trainer toggle. |
| `02_external/CFRU-expansion/src/end_battle.c` | `ClearFlag(FLAG_SMART_WILD)` | Clears one-time smart-wild state after battle. | Wild-only lifecycle; not a trainer-AI source-port point. |
| `02_external/CFRU-expansion/src/config.h` | `FLAG_SMART_WILD`, `WILD_ALWAYS_SMART` | Existing wild-AI flag and compile-time wild-AI define. | Useful reference for naming, but not a trainer-only runtime option. |

## NatDex / Ironmon `0x07` Flag Mapping In CFRU

The Ironmon/NatDex Smart-AI patch/randomizer finding is that trainer `aiFlags` are upgraded with `|= 0x07`. In local NatDex FireRed sources that maps to:

- bit 0: `AI_SCRIPT_CHECK_BAD_MOVE`
- bit 1: `AI_SCRIPT_CHECK_VIABILITY`
- bit 2: `AI_SCRIPT_TRY_TO_FAINT`

CFRU has two relevant naming layers:

| Source | Bit 0 | Bit 1 | Bit 2 | Meaning for this task |
| --- | --- | --- | --- | --- |
| `02_external/CFRU-expansion/include/constants/battle_ai.h` | `AI_SCRIPT_CHECK_BAD_MOVE` | `AI_SCRIPT_TRY_TO_FAINT` | `AI_SCRIPT_CHECK_VIABILITY` | Legacy/Gen3-style constants are still present, but the `TRY_TO_FAINT` and `CHECK_VIABILITY` names are only found in this constants header in the requested CFRU source search. |
| `02_external/CFRU-expansion/include/battle.h` | `AI_SCRIPT_CHECK_BAD_MOVE` | `AI_SCRIPT_SEMI_SMART` | `AI_SCRIPT_CHECK_GOOD_MOVE` | Runtime CFRU battle AI flag names used by `GetAIFlags`, `AI_THINKING_STRUCT->aiFlags`, and the AI script table. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c` / `sBattleAIScriptTable` | `AIScript_Negatives` | `AIScript_SemiSmart` | `AIScript_Positives` | Actual CFRU runtime scripts executed for bits 0, 1 and 2. |

Conclusion: the three NatDex names do not exist 1:1 as CFRU runtime AI scripts. Numerically, however, NatDex/Ironmon `0x07` corresponds directly to CFRU runtime bits 0, 1 and 2:

```c
AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE
```

`AI_SCRIPT_SEMI_SMART` is not just an alias or bundle. CFRU maps bit 1 to the dedicated `AIScript_SemiSmart` function, and that function explicitly returns without doing its semi-smart work if `AI_SCRIPT_CHECK_GOOD_MOVE` is also present. Therefore, setting all three bits mostly means:

- always run the baseline negative/bad-move scoring,
- mark the AI as smarter than basic for shared `aiFlags > AI_SCRIPT_CHECK_BAD_MOVE` checks,
- run the good-move/positive scoring path,
- skip the inner semi-smart scoring body because good-move AI supersedes it.

This is still the closest CFRU equivalent to NatDex/Ironmon `0x07`, because CFRU intentionally replaced the old bit-1/bit-2 names with `SEMI_SMART` and `CHECK_GOOD_MOVE` semantics on the same bit positions.

Flags that are too invasive for v1:

- `AI_SCRIPT_ROAMING`, `AI_SCRIPT_SAFARI`, and `AI_SCRIPT_FIRST_BATTLE`, because they are special battle-mode scripts rather than trainer-smartness levels.
- Any wild/raid path from `WildMonIsSmart`, `FLAG_SMART_WILD`, `WILD_ALWAYS_SMART`, scripted wild battles, or raid checks.
- Any difficulty-gated switch prediction, shift-switch, or Expert anti-cheese behavior outside the normal consequences of setting trainer `aiFlags`.
- Any non-AI difficulty effects in `build_pokemon.c`, move-menu restrictions, battle-rule changes, wild construction or raid logic.

## Isolatable AI Improvements From Hard / Expert

The most isolated trainer improvement is in `GetAIFlags`: Hard and Expert add `AI_SCRIPT_SEMI_SMART` for trainer battles when the trainer does not already have `AI_SCRIPT_CHECK_GOOD_MOVE`.

This is the best future source-port candidate because it:

- Reads the same base trainer AI flags CFRU already uses.
- Does not require `VAR_GAME_DIFFICULTY` to be Hard or Expert.
- Does not require `build_pokemon.c` changes.
- Avoids trainer IV, EV, friendship, PP and level-scaling effects.
- Keeps stronger hand-authored trainers with `AI_SCRIPT_CHECK_GOOD_MOVE` intact instead of downgrading or overwriting them.

Important caveat: adding `AI_SCRIPT_SEMI_SMART` is not only move selection. CFRU switching code also checks whether `aiFlags > AI_SCRIPT_CHECK_BAD_MOVE`, so a trainer-AI option can change switching/item-style decisions indirectly. That is still AI behavior, but it is broader than a single move-scoring script.

## AI Improvements Tightly Coupled To `VAR_GAME_DIFFICULTY`

These paths are AI-related but are currently coupled to runtime difficulty:

- `ShouldPredictRandomPlayerSwitch`: Hard+ allows switch prediction outside the Battle Frontier.
- `ShouldDoAIShiftSwitch`: Hard+/Expert+ gates shift-switch behavior depending on battle style.
- `IsPlayerTryingToCheeseAI`: Expert+ enables repeated switch and choice-lock anti-cheese checks for very-smart AI.
- `TryChangeMoveTargetToCounterPlayerProtectCheese`: Expert+ retargets moves in doubles to punish Protect-style behavior.
- `WildMonIsSmart`: Hard+ can upgrade selected smart wild encounters, while `FLAG_SMART_WILD` and `WILD_ALWAYS_SMART` provide separate wild-AI sources.
- `OpponentHandleChooseMove`: Expert wild battles and special wild/raid states can enter the AI chooser outside the normal trainer path.

These should not be silently included in a first Smart Trainer AI option. They either affect player agency more aggressively, are wild/raid-specific, or are tied to battle-style assumptions that need targeted playtesting.

## Code Paths Not To Port

The future Smart Trainer AI option should explicitly avoid these non-AI difficulty effects:

| Category | Source path | Existing difficulty effect to avoid |
| --- | --- | --- |
| Trainer IVs | `02_external/CFRU-expansion/src/build_pokemon.c` | Expert sets trainer base IVs to 31 in eligible cases. |
| Trainer EVs | `02_external/CFRU-expansion/src/build_pokemon.c` / `ShouldGiveTrainerMonBestStatsMaxEVs` | Hard+ can give best-stat max EV treatment. |
| Trainer friendship | `02_external/CFRU-expansion/src/build_pokemon.c` / `ShouldGiveTrainerMonMaxFriendship` | Hard+ can give max friendship where applicable. |
| Trainer PP | `02_external/CFRU-expansion/src/build_pokemon.c` / `GetTrainerMonMovePPBonus` | Expert can give maximum PP bonus. |
| Level scaling | `02_external/CFRU-expansion/src/build_pokemon.c` | Multiple trainer, boss and wild-boss level-scaling branches read difficulty. |
| Bag restrictions | `02_external/CFRU-expansion/src/move_menu.c` / `IsBagDisabled` | Hard/Expert restrict player item use. |
| Player move restrictions | `02_external/CFRU-expansion/src/move_menu.c` | Expert can block selected player evasion/minimize behavior outside Frontier. |
| Battle rules | `02_external/CFRU-expansion/src/battle_util.c` | Expert applies additional player-side sleep-clause behavior. |
| Battle calculations | `02_external/CFRU-expansion/src/accuracy_calc.c`, `02_external/CFRU-expansion/src/damage_calc.c`, `02_external/CFRU-expansion/src/end_turn.c` | Difficulty changes selected fog, berry-knowledge and damage/rule calculations. |
| Wild/Raid construction | `02_external/CFRU-expansion/src/wild_encounter.c`, `02_external/CFRU-expansion/src/dynamax.c`, `02_external/CFRU-expansion/src/cmd49.c` | Expert/Hard/Easy affect wild move PP, Shadow Warrior abilities, raid shields and raid repeated-move behavior. |

## Recommended Option Shape

Prefer `VAR_TRAINER_AI_MODE` over a single flag if there is any chance of future tiers:

| Value | Intended meaning | Suggested behavior |
| --- | --- | --- |
| `0` | Off / CFRU normal | Use existing trainer AI flags unchanged. |
| `1` | Semi-smart trainers | For trainer battles, add `AI_SCRIPT_SEMI_SMART` when `AI_SCRIPT_CHECK_GOOD_MOVE` is absent. |
| `2` | Predictive trainers | Consider adding switch prediction and/or shift-switch behavior after separate testing. |
| `3` | Anti-cheese trainers | Consider Expert-style anti-cheese only as an explicit opt-in, not as the default Smart AI. |

If the project only wants one binary option, `FLAG_SMART_TRAINER_AI` is simpler and should map only to the value-1 behavior above.

Wild AI should stay separate. Use a separate future control such as `FLAG_SMART_WILD_AI` or a small wild AI mode var. Do not overload `FLAG_SMART_WILD`, because CFRU already uses it as a one-time smart-wild state that is cleared at battle end.

## Implemented v1 Runtime Flag

Implementation branch: `feature/cfru-smart-trainer-ai-mode`.

The first source implementation uses a single binary runtime flag:

```c
#define FLAG_SMART_TRAINER_AI 0xA0E
```

When `FLAG_SMART_TRAINER_AI` is set, `GetAIFlags` ORs trainer battle flags with:

```c
AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE
```

This is intentionally close to the NatDex/Ironmon `aiFlags |= 0x07` behavior and does not change `VAR_GAME_DIFFICULTY`. The hook only runs in the trainer-data branch of `GetAIFlags`; it does not add wild, raid, Frontier, Safari, roaming, first-battle, trainer-build, level-scaling, bag-restriction, move-restriction, battle-rule, Expert anti-cheese, or shift-switch logic.

Important caveat: `AI_SCRIPT_CHECK_GOOD_MOVE` enables stronger CFRU AI paths than `AI_SCRIPT_SEMI_SMART` alone. v1 is closer to NatDex/Ironmon `0x07`, but it needs battle smoke coverage to confirm the resulting trainer behavior is acceptable for the Randomizer/Ironmon profile.

The flag currently has no UI, NPC, option-menu, or randomizer-profile wiring. It is available only as a runtime flag for scripts or later integration work.

## Minimal Later Code Approach

No code changes are made by this document. A later implementation can stay small:

1. Keep `VAR_GAME_DIFFICULTY` at Normal for the Randomizer/Ironmon baseline.
2. Add a new trainer-AI runtime option, preferably `VAR_TRAINER_AI_MODE` if tiering is desired.
3. In `GetAIFlags`, after base trainer AI flags are known, add `AI_SCRIPT_SEMI_SMART` for trainer battles when the new option is enabled and `AI_SCRIPT_CHECK_GOOD_MOVE` is not already present.
4. Do not change `build_pokemon.c`; trainer IVs, EVs, friendship, PP and levels must remain Normal-equivalent.
5. Do not change bag restrictions, player move restrictions, battle rules, wild encounter construction or raid behavior for the baseline trainer-AI option.
6. Treat `ShouldPredictRandomPlayerSwitch`, `ShouldDoAIShiftSwitch`, `IsPlayerTryingToCheeseAI` and `TryChangeMoveTargetToCounterPlayerProtectCheese` as separate later decisions, not part of the minimal port.

## Risks And Test Needs

- `AI_SCRIPT_SEMI_SMART` can affect more than move selection because other AI code branches on `aiFlags > AI_SCRIPT_CHECK_BAD_MOVE`.
- Battle Frontier and hand-authored `AI_SCRIPT_CHECK_GOOD_MOVE` trainers already have special behavior; the new option must avoid downgrading or double-upgrading them.
- Shift-switch and switch-prediction behavior may feel like a battle-rule change in Ironmon contexts, even though it is implemented as AI.
- Expert anti-cheese logic can be perceived as punitive rather than simply smarter; keep it out of the baseline.
- Wild AI has independent state through `FLAG_SMART_WILD`, `WILD_ALWAYS_SMART`, raid checks and special wild forms; trainer and wild controls should not share one switch.
- Randomizer fairness needs a focused smoke matrix with randomized moves, items and trainer parties, because smarter AI may exploit coverage combinations that vanilla CFRU balance did not assume.
- Regression checks should compare Normal difficulty plus Smart Trainer AI against Normal difficulty without it and confirm unchanged trainer IVs, EVs, friendship, PP, levels, player bag access, player move access, battle rules, wild construction and raid behavior.

## Recommendation

Implementing Smart Trainer AI only looks realistic, but it should be a source-port of selected CFRU AI flag behavior rather than a wrapper around `VAR_GAME_DIFFICULTY`.

Recommended baseline if the goal is CFRU-native conservatism: `VAR_TRAINER_AI_MODE = 1`, equivalent to "add `AI_SCRIPT_SEMI_SMART` to regular trainer AI where `AI_SCRIPT_CHECK_GOOD_MOVE` is absent."

Recommended baseline if the goal is Ironmon/NatDex `0x07` closeness: `VAR_TRAINER_AI_MODE = 1` should OR normal trainer flags with `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`, while still leaving `VAR_GAME_DIFFICULTY` Normal and avoiding all trainer-build, wild/raid, player-restriction and battle-rule side effects.

Use `FLAG_SMART_TRAINER_AI` only if the project intentionally wants a single non-tiered toggle. Keep wild AI separate behind a new wild-specific control.
