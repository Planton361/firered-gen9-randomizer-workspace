# CFRU Game Difficulty Map

## Executive Summary

`VAR_GAME_DIFFICULTY` is a runtime CFRU option stored at `0x5157`. It is not a pure "Smart AI" toggle. Source reads show that the value affects battle AI flags, trainer Pokemon construction, trainer level scaling, trainer PP/IV/EV/friendship strength, player item and move restrictions, wild/raid edge cases, and a few battle-calculation rules.

The source uses `OPTIONS_*_DIFFICULTY` enum names, not `DIFFICULTY_*` names:

| Conceptual name | CFRU source enum | Value |
|---|---|---:|
| `DIFFICULTY_NORMAL` | `OPTIONS_NORMAL_DIFFICULTY` | 0 |
| `DIFFICULTY_EASY` | `OPTIONS_EASY_DIFFICULTY` | 1 |
| `DIFFICULTY_HARD` | `OPTIONS_HARD_DIFFICULTY` | 2 |
| `DIFFICULTY_EXPERT` | `OPTIONS_EXPERT_DIFFICULTY` | 3 |

Primary source anchors:

- `02_external/CFRU-expansion/src/config.h`: defines `VAR_GAME_DIFFICULTY 0x5157` and documents Normal/Easy/Hard/Expert semantics.
- `02_external/CFRU-expansion/include/global.h`: defines the `OPTIONS_*_DIFFICULTY` enum order.
- `02_external/CFRU-expansion/src/option_menu.c`: reads and writes the runtime option from the option menu.
- `02_external/CFRU-expansion/src/build_pokemon.c`: most trainer-strength effects.
- `02_external/CFRU-expansion/src/Battle_AI/ai_master.c`, `src/Battle_AI/ai_switching.c`, `src/Battle_AI/ai_negatives.c`, `src/battle_controller_opponent.c`: battle AI effects.

DPE Gen9 had no relevant `VAR_GAME_DIFFICULTY` or `OPTIONS_*_DIFFICULTY` logic in the requested search. Its matching `Hard` text was Pokedex/string content, not runtime difficulty logic.

## Source Values

`include/global.h` defines the values in enum order:

- `OPTIONS_NORMAL_DIFFICULTY = 0`
- `OPTIONS_EASY_DIFFICULTY = 1`
- `OPTIONS_HARD_DIFFICULTY = 2`
- `OPTIONS_EXPERT_DIFFICULTY = 3`

`src/config.h` defines:

- `VAR_GAME_DIFFICULTY 0x5157`

The same `config.h` comment says `0` is normal/vanilla, `1` is Easy, `2` is Hard, and `3` is Expert. The comment still mentions `ShouldGiveTrainerMonMaxEVs`, but the implemented helper found in `build_pokemon.c` is named `ShouldGiveTrainerMonBestStatsMaxEVs`.

## Effect Table

| File / function | Difficulty value | Effect | Category |
|---|---|---|---|
| `src/option_menu.c` / option menu init and save | all | Reads `VarGet(VAR_GAME_DIFFICULTY)` into the second option page and writes it back with `VarSet`. | UI/runtime option |
| `strings/option_menu.string` | all | Provides option labels `Normal`, `Easy`, `Hard`, `Expert`. | UI text |
| `src/hall_of_fame.c` / `HallOfFame_PrintWelcomeText` | all | Prints the selected difficulty label in Hall of Fame. | UI/display |
| `src/build_pokemon.c` / `CreateNPCTrainerParty` | Expert+ | Opponent trainer Pokemon get base IV `31` instead of trainer-class/default IVs. Partners are excluded by `side != B_SIDE_PLAYER`. | Trainer-mon build |
| `src/build_pokemon.c` / `CreateNPCTrainerParty` | not Easy | Trainer level scaling is enabled except for documented special cases such as Pokemon League and scaled wild-boss partner handling. | Trainer level scaling |
| `src/build_pokemon.c` / `CreateNPCTrainerParty` | not Easy | Randomized trainer Pokemon may evolve naturally by level when `FLAG_POKEMON_RANDOMIZER` is active and not temporarily disabled. | Trainer-mon build/randomizer interaction |
| `src/build_pokemon.c` / `CreateNPCTrainerParty` | not Easy | Existing trainer EV spreads are applied when valid; Easy skips applying these spreads. | Trainer-mon build |
| `src/build_pokemon.c` / `ShouldGiveTrainerMonBestStatsMaxEVs` | Hard+ | Selected major trainer classes get max EVs in the two best base stats if the mon has no EVs already. | Trainer-mon build |
| `src/build_pokemon.c` / `ShouldGiveTrainerMonMaxFriendship` | Hard+ | Champion, Rival, Rival 2, Leader, and Elite Four get max friendship; Frustration users get friendship `0`. | Trainer-mon build |
| `src/build_pokemon.c` / `GetTrainerMonMovePPBonus` | Expert+ | Trainer Pokemon moves get max PP bonus. | Trainer-mon build |
| `src/build_pokemon.c` / `IsPseudoBossTrainerPartyForLevelScaling` | Easy | Custom-move trainer parties are not treated as pseudo-bosses for scaling. | Trainer level scaling |
| `src/build_pokemon.c` / `IsBossTrainerClassForLevelScaling` | Easy | Boss trainer classes are not treated as bosses for scaling. | Trainer level scaling |
| `src/build_pokemon.c` / `ModifySpeciesAndLevelForGenericBattle` | Hard+ | Normal enemies can scale from the player average-team-level path earlier/more broadly. | Trainer level scaling |
| `src/build_pokemon.c` / `ModifySpeciesAndLevelForGenericBattle` | Expert+ | Level subtractor is reduced to `2`, so trainers scale closer to the player's average level; regular trainers can evolve after scaling. | Trainer level scaling |
| `src/build_pokemon.c` / `GetScaledWildBossLevel` | Easy | Scaled wild boss level is biased average player level minus 2; otherwise biased average plus 1. | Wild boss scaling |
| `src/Battle_AI/ai_master.c` / `GetAIFlags` | Easy | Trainer AI is weakened: smart trainers lose `AI_SCRIPT_CHECK_GOOD_MOVE` and become semi-smart; other trainers become basic `AI_SCRIPT_CHECK_BAD_MOVE`. | Battle AI |
| `src/Battle_AI/ai_master.c` / `GetAIFlags` | Hard | Regular trainers without good-move AI gain `AI_SCRIPT_SEMI_SMART`. | Battle AI |
| `src/Battle_AI/ai_master.c` / `GetAIFlags` | Expert | Trainer behavior matches Hard's semi-smart upgrade for regular trainers; wild Pokemon get `AI_SCRIPT_CHECK_BAD_MOVE | WildMonIsSmart(...)`. | Battle AI / wild AI |
| `src/battle_controller_opponent.c` / `OpponentHandleChooseMove` | Expert | Wild battles enter the AI move-choice path even outside trainer battles. | Battle AI / wild AI |
| `src/Battle_AI/ai_master.c` / `WildMonIsSmart` | Hard+ | Species marked `smartWild` get semi-smart wild AI. Separately, compile-time `WILD_ALWAYS_SMART` gives wild Pokemon basic smartness independent of difficulty. | Wild AI |
| `src/Battle_AI/ai_negatives.c` | Easy | `AI_TRY_TO_KILL_RATE` is reduced to one fifth for basic AI. | Battle AI |
| `src/Battle_AI/ai_switching.c` / `ShouldDoAIShiftSwitch` | Hard+ / Expert+ | AI can do shift-style switches in trainer single battles: Shift style at Hard+, Semi-Shift at Expert+. | Battle AI |
| `src/Battle_AI/ai_master.c` / switch prediction helpers | Hard+ | AI may predict player switches in Frontier or Hard+ modes. | Battle AI |
| `src/Battle_AI/ai_master.c` / `IsPlayerTryingToCheeseAI` | Expert+ | Very-smart AI can rechoose moves against repeated-switch/Choice-lock cheese outside Frontier. | Battle AI |
| `src/Battle_AI/ai_master.c` / `TryChangeMoveTargetToCounterPlayerProtectCheese` | Expert+ | In doubles, very-smart opposing AI can retarget against first-turn Protect/Fake Out style cheese outside Frontier. | Battle AI |
| `src/Battle_AI/ai_master.c` / `PickRaidBossRepeatedMove` | not Easy | Smart raid boss repeated-move repick is allowed; Easy blocks this smart repick condition. | Raid AI |
| `src/move_menu.c` / move selection restrictions | Expert+ | Player-controlled Minimize / Evasion Up 2 moves are blocked outside Frontier; the comment notes AI can still use Minimize. | Player restriction |
| `src/move_menu.c` / `IsBagDisabled` | Hard | Player bag in trainer battles is disabled after 4 item uses. | Player item restriction |
| `src/move_menu.c` / `IsBagDisabled` | Expert+ | Player bag is disabled in trainer battles and in some uncatchable non-raid wild battles. | Player item restriction |
| `src/accuracy_calc.c` / `AccuracyCalcPassDefAbilityItemEffect`, `VisualAccuracyCalc_NoTarget` | Easy | Fog accuracy loss is milder before game clear outside Frontier: `0.8` multiplier instead of `0.6`. | Battle calculation |
| `src/damage_calc.c` / defender data load for AI calc | Expert+ | AI calc can keep knowledge of player-held type-resist berries; below Expert/Frontier this knowledge is hidden/replaced with recorded item effect. | Battle calculation / AI knowledge |
| `src/end_turn.c` / `GetBadThoughtsDamage` | Easy/Normal, Hard, Expert | Bad Thoughts residual damage is `1/16`, `1/12`, and `1/7` max HP respectively outside Frontier. | Battle calculation |
| `src/battle_util.c` / `IsSleepClauseInEffect` | Expert+ | Sleep Clause applies only against the player side outside supported facilities; opponent side is protected from being put to sleep. | Rule restriction |
| `src/wild_encounter.c` | Expert+ | Wild custom moves get max PP bonus when `FLAG_WILD_CUSTOM_MOVES` is active. | Wild encounter build |
| `src/wild_encounter.c` | Expert | Unbound-only Shadow Warrior gets hidden ability in Expert. | Wild encounter build |
| `src/dynamax.c` / `ShouldStartWithRaidShieldsUp` | Expert+ | Raid battles with `FLAG_RAID_BATTLE_NO_FORCE_END` can start with shields up. | Raid |
| `src/cmd49.c` / raid repeated attacks | not Easy | Raid boss may attack again when the player used an item; Easy blocks this branch as "too mean". | Raid |
| `src/dexnav.c` / `DexNavGenerateHiddenAbility` | Expert+ | Unbound-only: blocks pre-game-clear DexNav generation of Imposter hidden ability. | DexNav/player acquisition |
| `src/party_menu.c` / ability capsule path | Expert+ | Unbound-only: blocks pre-game-clear hidden ability capsule access to Imposter unless the game is cleared. | Player acquisition |

## Easy Effects

Easy is not just "Normal with weaker AI". Source-backed Easy effects include:

- Trainer AI is downgraded in `GetAIFlags`.
- Basic AI kill-rate pressure is reduced to one fifth when `AI_TRY_TO_KILL_RATE` is active.
- Trainer level scaling is disabled except for explicit exceptions.
- Trainer parties with custom moves are not treated as pseudo-bosses for level scaling.
- Boss trainer classes are not treated as bosses for level scaling.
- Existing trainer EV spreads are skipped.
- Randomized trainer Pokemon do not evolve naturally by level.
- Scaled wild bosses use biased average player level minus 2 instead of biased average plus 1.
- Fog accuracy loss is less severe before game clear outside Frontier.
- Raid item-use extra-attack punishment and smart repeated-move repick are reduced/blocked by Easy checks.

## Hard Effects

Hard adds both AI and non-AI pressure:

- Regular trainers are at least semi-smart if they did not already have good-move AI.
- Major trainer classes can receive max EVs in their two best base stats via `ShouldGiveTrainerMonBestStatsMaxEVs`.
- Champion/Rival/Rival 2/Leader/Elite Four can receive max friendship, or zero friendship for Frustration.
- Trainer level scaling is more aggressive because Hard+ enters the average-player-level scaling path more broadly.
- AI can predict player switches in Hard+ contexts.
- AI can use shift switches in Shift battle style at Hard+.
- Player item use in trainer battles is capped at 4.
- Bad Thoughts damage increases from `1/16` to `1/12`.
- `smartWild` species can receive semi-smart wild AI at Hard+.

## Expert Effects

Expert includes Hard-style pressure and additional rules:

- Opponent trainer Pokemon get base IV `31`.
- Trainer moves get max PP bonus.
- Trainer level scaling uses a smaller level subtractor (`2`), keeping opponents closer to the player's average level.
- Regular trainers can evolve after scaling.
- Wild Pokemon can enter the AI move-choice path, and wild custom moves can receive max PP.
- Player bag is disabled in trainer battles, plus some uncatchable non-raid wild battles.
- Player-controlled Minimize / Evasion Up 2 moves are blocked outside Frontier.
- AI can retain more knowledge of player type-resist berries.
- Very-smart AI can react to repeated switching, Choice-lock cheese, and first-turn Protect/Fake Out target cheese outside Frontier.
- Sleep Clause becomes player-sided outside supported facilities.
- Bad Thoughts damage increases to `1/7`.
- Raid battles can start with shields up under `FLAG_RAID_BATTLE_NO_FORCE_END`.

## Smart AI Patch Comparison

A classic Ironmon/NatDex "Smart AI Patch" is usually understood as a narrower behavior change: improve move choice and trainer/wild decision-making while leaving the rest of the battle and trainer-build model largely alone.

`VAR_GAME_DIFFICULTY` overlaps with that idea only in the AI paths:

- `GetAIFlags` changes trainer and wild AI flags.
- `OpponentHandleChooseMove` lets Expert wild battles use the AI move-choice path.
- `ai_switching.c` enables AI shift-switch behavior on harder modes.
- `ai_master.c` adds switch prediction and anti-cheese reactions.
- `ai_negatives.c` weakens Easy's basic kill pressure.

But Hard and Expert are broader than Smart AI:

- They change Trainer Pokemon IVs, EVs, friendship, PP, evolution, and level scaling.
- They restrict player bag and some player moves.
- They alter battle calculations/rules such as Fog, Bad Thoughts, Sleep Clause, and AI knowledge of type-resist berries.
- They affect wild/raid/DexNav/ability-capsule edge cases.

No pure runtime "Smart AI only" switch was found in the requested source search. Relevant alternatives are not equivalent:

- `WILD_ALWAYS_SMART` is a compile-time define, not a runtime difficulty value, and applies to wild AI rather than trainer AI.
- `FLAG_SMART_WILD` is runtime-like but wild-specific.
- `VAR_GAME_DIFFICULTY` always carries broader effects beyond AI.

## Runtime Difficulty vs Compile-Time Defines

Runtime difficulty:

- `VAR_GAME_DIFFICULTY` is read with `VarGet(...)` and set through the option menu.
- It can vary by save/runtime state.
- Its source effects are the ones listed above.

Compile-time defines:

- `WILD_ALWAYS_SMART` is defined in `src/config.h` and changes wild AI behavior at compile time.
- `TRAINERS_WITH_EVS`, `SCALED_TRAINERS`, `FLAG_*` feature defines, and Unbound-specific guards determine whether some difficulty branches are compiled or reachable.
- These should not be described as user-selectable runtime difficulty settings unless there is a separate runtime variable or flag path.

The current local submodule worktree has known uncommitted `src/config.h` edits. Relevant local config state:

- `FLAT_EXP_FORMULA` is locally enabled, while source `HEAD` has it commented out.
- `FLAT_EXP_FORMULA` is balance-relevant for EXP gain but is not directly `VAR_GAME_DIFFICULTY`-specific.
- This analysis did not change, stage, reset, stash, or commit the CFRU submodule.
- Local config changes must remain separated from source-backed `VAR_GAME_DIFFICULTY` behavior.

## Open Questions / Next Analysis Points

- Confirm in a built/local run whether the option menu is exposed in the target ROM flow and what the initial/default value is before the player changes it. The enum/source establishes values, but this analysis does not prove save initialization defaults.
- Decide whether the randomizer stable profile should document `VAR_GAME_DIFFICULTY` as an external runtime balance setting rather than a UPR-FVX randomizer setting.
- If Ironmon compatibility needs "Smart AI only", identify whether a separate patch, script flag, or code change is required; no source-backed pure runtime switch was found here.
- Separate `WILD_ALWAYS_SMART`, `FLAG_SMART_WILD`, `TRAINERS_WITH_EVS`, `SCALED_TRAINERS`, and local `FLAT_EXP_FORMULA` into the broader CFRU runtime/config option map.
- If needed, audit exact reachability of Unbound-only branches for the current FireRed Gen9 target, because some difficulty hits are guarded by `#ifdef UNBOUND`.
