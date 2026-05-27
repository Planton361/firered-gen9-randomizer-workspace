# CFRU Game Difficulty Vanilla Option Analysis

## Scope

Branch: `analysis/cfru-game-difficulty-vanilla-option`

This is a documentation-only source analysis for whether CFRU `Game Difficulty` needs an explicit `Vanilla` / `Off` value after the split into Difficulty, Trainer Level Scaling, and Trainer AI. No CFRU, DPE, UPR-FVX, Tracker, ROM, save, build, screenshot, raw log, hash, private path, secret, token, or `.env` data was changed or documented.

## Current Source Model

`src/config.h:379` defines `VAR_GAME_DIFFICULTY = 0x5157` and documents raw `0` as `normal(vanilla)`, raw `1` as Easy, raw `2` as Hard, and raw `3` as Expert.

`include/global.h:167-180` defines the current raw order:

| Raw | Current enum | Current helper mode |
| --- | --- | --- |
| `0` | `OPTIONS_NORMAL_DIFFICULTY` | `DIFFICULTY_MODE_NORMAL` |
| `1` | `OPTIONS_EASY_DIFFICULTY` | `DIFFICULTY_MODE_EASY` |
| `2` | `OPTIONS_HARD_DIFFICULTY` | `DIFFICULTY_MODE_HARD` |
| `3` | `OPTIONS_EXPERT_DIFFICULTY` | `DIFFICULTY_MODE_EXPERT` |

`src/util.c:44-59` makes `GetGameDifficultyMode()` clamp unknown/raw invalid values to `DIFFICULTY_MODE_NORMAL`. Therefore existing saves with unset or raw `0` currently mean Normal, not a distinct Vanilla/Off mode.

`src/option_menu.c:322` loads `VAR_GAME_DIFFICULTY` directly into the option menu, and `src/option_menu.c:433` writes it back directly. The current Difficulty row values remain raw-backed, while split `Level Scaling` and `Trainer AI` use separate vars and legacy-preserving dirty/original tracking.

## What Normal Means Today

After the split, `DIFFICULTY_MODE_NORMAL` means the baseline CFRU Difficulty bundle, not a strict "disable all CFRU difficulty power/rules" mode.

Normal is already free from many Hard/Expert-only effects:

- no Expert forced trainer IVs to 31,
- no Hard+ max EV injection for boss/rival-style classes,
- no Hard+ max friendship,
- no Expert trainer move PP bonus,
- no Expert bag lockout,
- no Expert Minimize/evasion restriction,
- no Expert sleep clause,
- no Expert raid start-shields,
- no Expert scripted-wild max PP,
- no Expert DexNav/Ability Capsule hidden-Imposter restriction.

Normal is not fully FireRed-/Ironmon-near if the goal is "no CFRU Difficulty side effects":

- `TRAINERS_WITH_EVS` is enabled in `src/config.h:214`. In `src/build_pokemon.c:1092-1121`, trainer EV spreads are applied for Normal/Hard/Expert but skipped only on Easy. This is the clearest source-backed Normal-vs-Vanilla difference for trainer power.
- Runtime randomized trainer species can evolve when `FLAG_POKEMON_RANDOMIZER` is set and `gameDifficulty != DIFFICULTY_MODE_EASY` (`src/build_pokemon.c:1078-1089`). This is adjacent to the desired "Trainer Evolution remains UPR-FVX" boundary and should not stay coupled to Normal if strict Vanilla is added.
- Raid bosses can attack again after player item use on any non-Easy difficulty (`src/cmd49.c:1427-1435`). Normal therefore gets the raid item-punishment rule.
- Fog uses the harsher `0.6` accuracy multiplier unless Difficulty is Easy before postgame and outside Frontier (`src/accuracy_calc.c:512-519`, `src/accuracy_calc.c:623-630`). Normal has the default CFRU fog penalty, while Easy has a mitigation.
- Bad Thoughts / Nightmare-style damage uses the same `1/16` divisor for Easy and Normal, while Hard and Expert are harsher (`src/end_turn.c:2025-2038`). Normal is acceptable here if the goal is no hardening, but not if the goal is removing the mechanic entirely.

## Difficulty Power/Rules Path Audit

| Category | Source | Normal behavior | Vanilla/Off delta if added |
| --- | --- | --- | --- |
| Trainer IVs | `src/build_pokemon.c:793-803` | Uses trainer-class base IV / `STANDARD_IV`; Expert alone forces 31 for non-partners. | Same as Normal unless the project wants true FireRed IV tables. |
| Runtime randomized trainer evolution | `src/build_pokemon.c:1078-1089` | Evolves randomized trainer species when randomizer flag is active and difficulty is not Easy. | Should be disabled or moved to a separate randomizer/runtime setting. |
| Trainer EV spreads | `src/build_pokemon.c:1092-1121`; `src/config.h:214` | Applies configured EV/IV spread table when valid and not Easy. | Should skip Difficulty-owned EV spread application for FireRed-/Ironmon-near rules. |
| Rival EV spread challenge | `src/build_pokemon.c:1096-1098` | No Normal effect; Hard/Expert only. | Same as Normal. |
| Boss/rival max EVs | `src/build_pokemon.c:1185-1192`, `1277-1307` | No Normal effect; Hard+ only. | Same as Normal. |
| Boss/rival max friendship | `src/build_pokemon.c:1194-1201`, `1309-1333` | No Normal effect; Hard+ only. | Same as Normal. |
| Trainer move PP bonus | `src/build_pokemon.c:1336-1344` | No Normal effect; Expert only. | Same as Normal. |
| Wild boss level difficulty fallback | `src/build_pokemon.c:1569-1582` | Non-Easy path scales wild boss level to biased average + 1 when wild boss scaling is active. | Needs explicit policy; if Vanilla means no Difficulty side effects, use non-hardening/no-scaling behavior or keep this under Trainer Level Scaling / wild-boss setting, not Difficulty. |
| Player move restriction | `src/move_menu.c:1874-1881` | No Normal effect; Expert blocks Minimize/evasion-up selection. | Same as Normal. |
| Player bag restriction | `src/move_menu.c:2236-2272` | No trainer-battle restriction from Difficulty; Hard limits to four, Expert disables. Normal still allows raid item-punishment elsewhere. | Same for bag lockout, but pair with raid item-punishment change below. |
| Sleep clause | `src/battle_util.c:2028-2033` | No Normal effect; Expert only. | Same as Normal. |
| Bad Thoughts damage | `src/end_turn.c:2025-2038` | Same as Easy: `1/16`. Hard/Expert are harsher. | Same as Normal if "no hardening" is enough; different only if Vanilla should remove the mechanic entirely. |
| Fog accuracy | `src/accuracy_calc.c:512-519`, `623-630` | Uses default `0.6` fog loss. Easy pre-clear/non-Frontier uses milder `0.8`. | Needs explicit policy: either keep CFRU default fog, or define Vanilla as no Difficulty fog adjustment / no CFRU fog hardening. |
| Scripted wild custom-move PP | `src/wild_encounter.c:1506-1512` | No Normal effect; Expert maxes PP. | Same as Normal. |
| Unbound Shadow Warrior HA | `src/wild_encounter.c:1546-1547` | No Normal effect; Expert only. | Same as Normal. |
| Raid item punishment | `src/cmd49.c:1427-1435` | Active in Normal because only Easy opts out. | Vanilla should opt out. |
| Raid start shields | `src/dynamax.c:1663-1665` | No Normal effect; Expert only. | Same as Normal. |
| DexNav hidden Imposter gate | `src/dexnav.c:1411-1416` | No Normal effect; Expert only. | Same as Normal. |
| Ability Capsule hidden Imposter gate | `src/party_menu.c:2601-2606` | No Normal effect; Expert only. | Same as Normal. |
| Hall of Fame display | `src/hall_of_fame.c:475-488` | Shows `Normal`. | Needs `Vanilla` label if a new mode exists. |

## Residual AI/Wild/Raid Note

Trainer AI has a separate profile setting, but current source still uses `GetGameDifficultyMode()` for several non-trainer or mixed enemy-AI paths:

- wild Expert move choice in `src/battle_controller_opponent.c:38-47`,
- non-trainer wild AI fallback in `src/Battle_AI/ai_master.c:224-228`,
- smart-wild special species on Hard+ in `src/Battle_AI/ai_master.c:1070-1072`,
- non-trainer switch/protect anti-cheese fallbacks in `src/Battle_AI/ai_master.c:1577-1646` and `1728-1748`,
- raid repeated-move Easy suppression in `src/Battle_AI/ai_master.c:1769-1770`,
- non-trainer weakness-berry knowledge fallback in `src/damage_calc.c:2429-2432`,
- Easy basic-AI kill-rate suppression for non-trainer battles in `src/Battle_AI/ai_negatives.c:166-169`.

These are not trainer-power paths, but they matter for a "no CFRU Difficulty side effects" profile. If `Vanilla` is added, the implementation should decide whether these remain Difficulty-owned Wild/Raid rules or move later to a Wild/Raid AI profile.

## Variant A: No New Vanilla Value

Use this if the project defines Normal as the CFRU baseline and only wants to avoid Hard/Expert side effects.

Pros:

- No save migration.
- No enum/raw compatibility risk.
- Existing raw `0` behavior and Hall of Fame display stay intact.
- Most visible harsh rules are already absent in Normal.

Cons:

- Normal still applies configured trainer EV spreads when present.
- Normal still allows the runtime randomized trainer evolution path when CFRU randomizer flag is active.
- Normal still gets non-Easy raid item-punishment behavior.
- Normal is not a clean "FireRed/Ironmon-near no Difficulty bundle" switch.

Conclusion: Variant A is acceptable only if "Normal" means "CFRU Normal" rather than "Vanilla/Off".

## Variant B: Add DifficultyMode Vanilla

Recommended if the desired profile is strict FireRed-/Ironmon-near rules while keeping Trainer Level Scaling and Trainer AI independently selectable.

### Semantics

`Difficulty = Vanilla` should mean:

- no Difficulty-forced trainer IV boost,
- no Difficulty-applied trainer EV spread upgrade,
- no Difficulty max friendship,
- no Difficulty trainer or scripted-wild PP bonus,
- no Difficulty player bag/move restrictions,
- no Difficulty sleep clause,
- no Hard/Expert Bad Thoughts amplification,
- no non-Easy raid item-punishment rule,
- no Expert raid start-shields,
- no Difficulty DexNav/Ability Capsule hidden-Imposter restriction,
- no Difficulty-owned wild/raid AI hardening unless a separate Wild/Raid AI design keeps it.

Trainer Level Scaling and Trainer AI stay controlled only by their split settings:

- `Trainer Level Scaling = Off` for Ironmon-/FireRed-near no runtime scaling.
- `Trainer AI = Smart` if the profile wants Smart Trainer AI without Difficulty power/rules.

### Raw Value / Migration

Do not repurpose raw `0`.

Existing saves and scripts already use raw `0` as Normal. Reinterpreting raw `0` as Vanilla would silently weaken old saves and change Hall of Fame output. Use a new explicit raw value, preferably:

| Raw | Meaning |
| --- | --- |
| `0` | existing Normal, legacy-compatible |
| `1` | Easy |
| `2` | Hard |
| `3` | Expert |
| `4` | new Vanilla |

Implementation caveat: do not rely on raw numeric order for behavior. A raw `4` Vanilla must not satisfy `>= DIFFICULTY_MODE_HARD` or `>= DIFFICULTY_MODE_EXPERT`. The safe implementation is to decouple saved raw constants from behavior predicates:

- keep `OPTIONS_VANILLA_DIFFICULTY = 4` for save/UI compatibility,
- add `DIFFICULTY_MODE_VANILLA` as a behavior mode that is lower than Hard/Expert comparisons, or add explicit helper predicates such as `IsDifficultyHardOrHigher()` and `IsDifficultyExpertOrHigher()`,
- update `GetGameDifficultyMode()` to map raw `4` to Vanilla and invalid values to legacy Normal.

### UI

Recommended Difficulty row:

`Vanilla / Easy / Normal / Hard / Expert`

The row must use explicit menu-to-raw mapping because UI order would no longer match raw save order. Hall of Fame should display `Vanilla` for raw `4`.

### Suggested New Profile

For the requested Ironmon-/Vanilla-near profile:

| Setting | Value |
| --- | --- |
| Difficulty | `Vanilla` |
| Trainer Level Scaling | `Off` |
| Trainer AI | `Smart` |

This avoids the current workaround of using `Difficulty = Normal` while accepting Normal's trainer EV and non-Easy raid/randomizer side effects.

## Recommendation

Recommend Variant B: add an explicit `Difficulty = Vanilla` value, but only in a later implementation branch with careful raw/save mapping.

Reason:

- Source shows Normal is historically raw `0` and cannot be redefined safely.
- Source also shows Normal is not a pure "no Difficulty bundle" mode because trainer EV spreads and several non-Easy rules still apply.
- The split already made Level Scaling and Trainer AI independent, so adding Vanilla to Difficulty is the clean way to express "no CFRU Difficulty power/rules" while still allowing `Level Scaling = Off` and `Trainer AI = Smart`.

Do not implement it as `Off` unless the UI text clearly means "Difficulty effects off". `Vanilla` is clearer because the setting remains present and selected; it does not disable the options system.

## Risks

- Raw `4` Vanilla is safe for save migration, but unsafe if code compares raw enum values directly. Implementation must route behavior through helpers/predicates.
- Some "Normal" behavior is not purely Difficulty-owned. Fog, Bad Thoughts, wild boss scaling, raid behavior, and wild/raid AI need explicit product decisions before implementation.
- `TRAINERS_WITH_EVS` is a compile-time feature. A Vanilla mode can skip EV application at runtime, but it does not remove the feature or the table from the build.
- Runtime randomized trainer evolution is still tied to Difficulty in current source. If left unchanged, Vanilla semantics would remain leaky for randomizer profiles.
- Existing documentation and UI currently call raw `0` Normal/vanilla in places; future implementation must update wording without changing legacy raw `0` behavior.

## Handoff Prompt

Arbeitsbranch:
`feature/cfru-game-difficulty-vanilla-option`

Ziel:
Fuehre einen expliziten CFRU `Difficulty = Vanilla` Wert ein, ohne bestehende Saves zu migrieren oder raw `0 = Normal` umzudeuten.

Wichtige Regeln:

- Keine Umdeutung von `VAR_GAME_DIFFICULTY` raw `0`; bestehende Saves bleiben Normal.
- Neuer raw Wert bevorzugt `4 = Vanilla`.
- `GetGameDifficultyMode()` muss raw `4` auf einen eigenen Vanilla-Mode mappen; invalid raw values bleiben legacy Normal.
- Raw numeric order darf nicht versehentlich `Vanilla >= Hard/Expert` machen.
- Trainer Level Scaling und Trainer AI bleiben separate Settings.
- Vanilla soll Difficulty-owned trainer EV/power, player restriction, battle/wild hardening, raid item punishment und Hall-of-Fame-Label sauber behandeln.
- Keine UPR-FVX/DPE/Tracker-Aenderungen, keine ROMs/Saves/Builds/raw Logs/private Pfade.
