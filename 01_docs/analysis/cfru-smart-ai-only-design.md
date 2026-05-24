# CFRU Smart AI Only Design

## Executive Summary

For the Randomizer/Ironmon target, CFRU `VAR_GAME_DIFFICULTY` should not be treated as a "Smart AI" option. The source-backed difficulty map shows that Hard and Expert do improve AI behavior, but they also change trainer Pokemon strength, level scaling, player restrictions, battle rules, wild encounters, and raid behavior.

Recommendation: keep CFRU runtime difficulty on Normal for a baseline randomizer/Ironmon profile unless a deliberate Hard-mode profile is requested. If better AI is desired, treat it as a separate source-port/design topic: trainer AI, wild AI, and any anti-cheese behavior should be separable from IV/EV/friendship/PP boosts, level scaling, item bans, move bans, and special battle rules.

## Source Basis

Primary source summary: `01_docs/analysis/cfru-game-difficulty-map.md`.

Important CFRU source anchors:

- `02_external/CFRU-expansion/include/battle.h`: defines `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_SEMI_SMART`, and `AI_SCRIPT_CHECK_GOOD_MOVE`.
- `02_external/CFRU-expansion/src/Battle_AI/ai_master.c`: contains `GetAIFlags`, `WildMonIsSmart`, switch-prediction and anti-cheese helpers.
- `02_external/CFRU-expansion/src/battle_controller_opponent.c`: contains `OpponentHandleChooseMove`, including the Expert wild-AI route and `FLAG_SMART_WILD`.
- `02_external/CFRU-expansion/src/Battle_AI/ai_switching.c`: contains `ShouldDoAIShiftSwitch`.
- `02_external/CFRU-expansion/src/config.h`: defines `FLAG_SMART_WILD`, `WILD_ALWAYS_SMART`, and `VAR_GAME_DIFFICULTY`.

No CFRU/DPE source was changed for this design note.

## Problem

The project goal is better Trainer AI for a randomized/Ironmon-like experience, not a wholesale CFRU difficulty rebalance. `VAR_GAME_DIFFICULTY` is too invasive for that narrow goal because it bundles AI with unrelated gameplay changes:

- Trainer Pokemon can become stronger via IV, EV, friendship, PP, evolution, and level-scaling paths.
- Player options can be restricted through battle item and move-selection limits.
- Battle rules/calculations can shift, including Fog, Bad Thoughts damage, Sleep Clause, and AI knowledge of type-resist berries.
- Wild, raid, DexNav, and ability-capsule behavior can change.

This coupling makes Hard/Expert unsuitable as a transparent "Smart AI only" Randomizer option. Enabling them would change both the opponent's decisions and the underlying battle economy.

## AI Effects Only

These are the source-backed difficulty effects that are genuinely AI-oriented:

| Source path | Current trigger | Smart-AI-only design relevance |
|---|---|---|
| `Battle_AI/ai_master.c` / `GetAIFlags` | Easy/Hard/Expert branches on `VAR_GAME_DIFFICULTY` | Main trainer-AI hook. A trainer-only smart toggle would likely add `AI_SCRIPT_SEMI_SMART` or preserve `AI_SCRIPT_CHECK_GOOD_MOVE` behavior here without touching trainer stats. |
| `battle_controller_opponent.c` / `OpponentHandleChooseMove` | Expert, `FLAG_SMART_WILD`, `WildMonIsSmart`, raids, trainer battles | Main route deciding whether wild/non-trainer opponents use AI move choice. Wild AI should remain separate from trainer AI. |
| `Battle_AI/ai_master.c` / `WildMonIsSmart` | Hard+ for `smartWild`, compile-time `WILD_ALWAYS_SMART` | Wild-specific smartness. Useful as separate design axis, not trainer AI. |
| `Battle_AI/ai_switching.c` / `ShouldDoAIShiftSwitch` | Hard+ in Shift, Expert+ in Semi-Shift | Optional trainer-AI behavior. Should be explicit because it changes player battle-style expectations. |
| `Battle_AI/ai_master.c` / switch prediction helpers | Hard+ or Frontier | Optional advanced trainer-AI behavior. Needs fairness review for Ironmon. |
| `Battle_AI/ai_master.c` / `IsPlayerTryingToCheeseAI` | Expert+ and very-smart AI | Anti-cheese behavior. Stronger than basic smart AI and probably should be a separate tier. |
| `Battle_AI/ai_master.c` / `TryChangeMoveTargetToCounterPlayerProtectCheese` | Expert+ and very-smart AI in doubles | Anti-cheese target correction. Should not be silently included in a baseline smart-AI toggle. |
| `Battle_AI/ai_negatives.c` | Easy reduces `AI_TRY_TO_KILL_RATE` | Easy-specific AI weakening; not relevant to a smart-AI-only enable path except as a behavior to avoid. |

The minimal "Smart Trainer AI" concept is therefore narrower than Expert:

- make weak trainer AI at least semi-smart, or
- preserve existing trainer `aiFlags` and optionally add semi-smart behavior to regular trainers,
- without changing trainer builds, scaling, player restrictions, or battle rules.

## Non-AI Effects To Exclude

The following difficulty effects are source-backed but should not be part of a Smart-AI-only option.

### Trainer Build

- Expert sets opponent trainer IVs to `31`.
- Valid trainer EV spreads are skipped on Easy and active outside Easy.
- Hard+ can add max EVs in the two best base stats via `ShouldGiveTrainerMonBestStatsMaxEVs`.
- Hard+ can set max friendship or zero friendship for Frustration via `ShouldGiveTrainerMonMaxFriendship`.
- Expert grants max PP bonus to trainer moves.
- Non-Easy lets randomized trainer Pokemon evolve naturally by level.

### Level Scaling

- Easy disables most trainer level scaling.
- Hard+ broadens average-player-level scaling.
- Expert reduces the level subtractor, keeping trainers closer to the player's average level.
- Boss/pseudo-boss classification changes are tied to difficulty.
- Wild boss scaling changes on Easy.

### Player Restrictions

- Hard limits trainer-battle item use after four items.
- Expert disables the bag in trainer battles and some uncatchable non-raid wild battles.
- Expert blocks player-controlled Minimize / Evasion Up 2 outside Frontier.

### Battle Rules / Calculations

- Easy changes Fog accuracy loss.
- Hard/Expert change Bad Thoughts residual damage.
- Expert changes AI knowledge behavior for player-held type-resist berries.
- Expert applies Sleep Clause asymmetrically against the player outside supported facilities.

### Wild / Raid / Acquisition Side Effects

- Expert gives wild custom moves max PP.
- Expert can force smarter wild behavior through the wild-AI route.
- Expert changes some raid shield/repeated-attack behavior.
- Unbound-guarded DexNav and ability-capsule paths can block Imposter hidden ability access before game clear.

## Why Not Call `VAR_GAME_DIFFICULTY` Smart AI

Calling `VAR_GAME_DIFFICULTY` "Smart AI" would be misleading for this project:

- Hard and Expert affect opponent decision-making, but also affect opponent stats and player restrictions.
- A randomized/Ironmon-style run needs predictable randomizer semantics; hidden EV/IV/PP/scaling changes alter difficulty in ways unrelated to AI quality.
- Expert includes anti-cheese and player-side rule changes that are qualitatively different from simply choosing better moves.
- Wild AI is already controlled through separate concepts (`WILD_ALWAYS_SMART`, `FLAG_SMART_WILD`, `WildMonIsSmart`) and should not be conflated with Trainer AI.

Project wording should use:

- "CFRU runtime difficulty" for `VAR_GAME_DIFFICULTY`.
- "Trainer Smart AI" only for a future isolated source-port/design.
- "Wild Smart AI" for `WILD_ALWAYS_SMART`, `FLAG_SMART_WILD`, or future wild-specific runtime control.

## Design Options

### Option 1: Keep Difficulty Normal

Keep `VAR_GAME_DIFFICULTY = OPTIONS_NORMAL_DIFFICULTY` for the baseline randomizer/Ironmon profile.

Pros:

- Avoids hidden trainer stat, level-scaling, item, move, rule, wild, and raid side effects.
- Keeps the randomizer profile easier to explain and reproduce.
- Requires no CFRU code changes.

Cons:

- Does not improve weak trainer AI beyond the trainer data's existing `aiFlags`.

### Option 2: Separate Trainer Smart AI Toggle

Add a future source-level control such as `FLAG_SMART_TRAINER_AI` or `VAR_AI_DIFFICULTY`.

Likely hook points:

- `GetAIFlags`: add semi-smart or good-move behavior for trainer battles while leaving `VAR_GAME_DIFFICULTY` checks intact for actual difficulty.
- `ShouldDoAIShiftSwitch`: decide whether trainer smart mode should include shift-switching, or gate it behind a higher AI tier.
- `IsPlayerTryingToCheeseAI` and `TryChangeMoveTargetToCounterPlayerProtectCheese`: decide whether anti-cheese is included, excluded, or separately tiered.

Pros:

- Matches the desired behavior: better trainer decisions without trainer-stat or player-restriction side effects.
- Can be documented as a clean randomizer/Ironmon compatibility axis.

Cons:

- Requires CFRU source work and testing.
- Needs careful interaction rules with existing trainer `aiFlags`, Battle Frontier logic, difficulty, and battle style.

### Option 3: Separate Wild Smart AI Toggle

Keep wild AI independent from trainer AI.

Existing pieces:

- `WILD_ALWAYS_SMART` is compile-time and applies broad wild basic smartness.
- `FLAG_SMART_WILD` is a runtime flag for smarter one-time wild battles and is cleared after battle.
- `WildMonIsSmart` already handles species-specific smart wild behavior and Hard+ upgrades for `smartWild` species.

Pros:

- Avoids accidentally making all random wild encounters more tactical when only trainer AI was requested.
- Keeps wild-boss/raid behavior separate from normal trainer AI.

Cons:

- Existing `WILD_ALWAYS_SMART` is compile-time, so a user-facing runtime setting would need source work.
- `FLAG_SMART_WILD` is temporary/wild-specific, not a global trainer-AI solution.

### Option 4: No External ROM Smart-AI Patch Without Source Port

Do not layer an external Ironmon/NatDex-style Smart AI patch blindly on top of CFRU/DPE.

Pros:

- Avoids patch conflicts with CFRU's existing AI engine, hooks, flags, and expanded battle behavior.
- Keeps the source-backed workspace reproducible.

Cons:

- Any desired external Smart AI behavior must be mapped and ported intentionally into CFRU source, then tested.

## Recommended Project Policy

- Do not expose `VAR_GAME_DIFFICULTY` as a normal randomizer option for Smart AI.
- Keep runtime difficulty Normal in the baseline profile unless the user explicitly chooses a Hard-mode profile.
- Treat trainer AI, wild AI, trainer strength, level scaling, and player restrictions as separate axes.
- If "Smart AI only" becomes a goal, design it as a CFRU source-port with explicit trainer-only and wild-only controls.
- For Ironmon-style fairness, start with trainer move-choice improvement only; defer shift-switch, switch prediction, anti-cheese, wild AI, and player-restriction behavior to separate decisions.

## Open Code Questions

- Should `FLAG_SMART_TRAINER_AI` be a simple on/off flag, or should `VAR_AI_DIFFICULTY` provide tiers such as semi-smart, good-move, switch-aware, and anti-cheese?
- In `GetAIFlags`, should a trainer smart mode add `AI_SCRIPT_SEMI_SMART` only to regular trainers, or also upgrade trainers that already have `AI_SCRIPT_CHECK_GOOD_MOVE`?
- Should smart trainer AI apply to partner trainers, tag battles, two-opponent battles, and Battle Frontier, or should those preserve existing behavior?
- Should `ShouldDoAIShiftSwitch` be included in Smart Trainer AI, or reserved for a higher AI tier because it interacts with Shift/Semi-Shift battle style?
- Should switch prediction and anti-cheese logic remain Expert-only, or become optional AI tiers?
- Should wild AI remain compile-time (`WILD_ALWAYS_SMART`), one-shot (`FLAG_SMART_WILD`), species-driven (`smartWild`), or become a new runtime option?
- How should a future trainer smart toggle resolve conflicts if `VAR_GAME_DIFFICULTY` is Hard or Expert at the same time?
- What local smoke tests would prove "AI only" did not change IVs, EVs, friendship, PP, level scaling, bag restrictions, move restrictions, or battle rules?
