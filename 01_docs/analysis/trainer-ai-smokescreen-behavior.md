# Trainer AI Smokescreen behavior

Stand: 2026-05-28

## Scope

This is a source-backed analysis and local mGBA smoke plan for the observed Trainer-AI behavior where a Rival Pokemon with `Tackle` plus `Smokescreen` repeatedly used `Smokescreen` until the player's Accuracy reached minimum.

No CFRU, DPE or UPR-FVX code was changed. No ROMs, saves, emulator states, builds, tool binaries, screenshots, raw logs, hashes, private paths, tokens, secrets or `.env` data are included.

## Sanitized observation

- Battle type: Rival trainer battle.
- Opposing Pokemon moves observed: `Tackle` and `Smokescreen`.
- Behavior observed: the opposing Pokemon repeatedly selected `Smokescreen` until the player's Accuracy reached the minimum stage.
- Current interpretation: source-backed plausible but suspicious for Randomizer/Ironmon expectations. It should be A/B-smoked across Trainer AI options before any code fix is designed.

## Source findings

| Area | Source-backed finding | Interpretation |
| --- | --- | --- |
| AI flag bits | `02_external/CFRU-expansion/include/battle.h:523-525` maps bit 0 to `AI_SCRIPT_CHECK_BAD_MOVE`, bit 1 to `AI_SCRIPT_SEMI_SMART`, and bit 2 to `AI_SCRIPT_CHECK_GOOD_MOVE`. | CFRU bit names differ from NatDex/Ironmon classic `0x07` semantics. |
| AI script table | `02_external/CFRU-expansion/src/Battle_AI/ai_master.c:44-48` maps those bits to `AIScript_Negatives`, `AIScript_SemiSmart`, and `AIScript_Positives`. | `CHECK_GOOD_MOVE` activates CFRU positive utility scoring. |
| Base move scores | `ai_master.c:122-130` initializes usable move scores at `100`; disabled moves become `0` later. | A status move can win if damage moves do not receive enough boost. |
| Trainer AI profile hook | `ai_master.c:195-226` applies Easy/Hard/Expert profile logic for trainer battles, then `IsSmartTrainerAIEnabled()` ORs `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`. | Current Smart profile/v2 is conservative and does not globally add `CHECK_GOOD_MOVE`. |
| AI profile storage | `02_external/CFRU-expansion/src/util.c:137-200` derives Auto from game difficulty, maps explicit `Vanilla/Easy/Normal/Hard/Expert/Smart AI`, and treats explicit Smart as the smart flag owner. | Option-menu labels do not always mean difficulty; they feed trainer-AI profile helpers. |
| Option menu | `02_external/CFRU-expansion/src/option_menu.c:263-280`, `397-399`, `512-515` show `Trainer AI` values `Auto`, `Vanilla`, `Easy`, `Normal`, `Hard`, `Expert`, `Smart`, with raw `0` preserved unless changed. | Local A/B smoke can compare these values without changing CFRU source. |
| Tackle | `02_external/CFRU-expansion/src/Tables/battle_moves.c:545-558` defines `Tackle` as `EFFECT_HIT`, 40 power, 100 accuracy, physical. | Tackle is a simple damage option. |
| Smokescreen | `battle_moves.c:1773-1786` defines `Smokescreen` as `EFFECT_ACCURACY_DOWN`, 0 power, 100 accuracy, status. | It shares the same Accuracy-down AI class as Sand Attack. |
| Negative scoring | `02_external/CFRU-expansion/src/Battle_AI/ai_negatives.c:1327-1333` penalizes Accuracy-down only when Accuracy cannot be lowered; `ai_negatives.c:437-443` also penalizes into Keen Eye. | Repeating Smokescreen while Accuracy can still fall is not rejected by `CHECK_BAD_MOVE`. |
| Positive scoring | `02_external/CFRU-expansion/src/Battle_AI/ai_positives.c:532-536` boosts Accuracy-down if `GoodIdeaToLowerAccuracy(...)` is true. | Any profile or trainer data that includes `CHECK_GOOD_MOVE` can actively prefer Smokescreen. |
| Accuracy-lower helper | `02_external/CFRU-expansion/src/Battle_AI/ai_util.c:3414-3425` mostly checks KO shortcut, stat-lowering blockers, Mind's Eye, Clear Body-like behavior, Contrary and Clear Amulet. | It does not appear to ask whether repeated Accuracy drops are strategically better than available damage in the simple Tackle/Smokescreen case. |
| Status boost size | `02_external/CFRU-expansion/src/Battle_AI/ai_advanced.c:1726-1798` can turn a one-point status boost into larger class-dependent score bumps. | `CHECK_GOOD_MOVE` utility scoring can outweigh non-KO damage. |
| Damage boost | `ai_positives.c:2761-2862` boosts damaging moves for KO, strongest-move and desperation contexts. | If Tackle is not a KO or strongly favored damage move, Smokescreen can remain competitive. |
| SemiSmart boundary | `ai_positives.c:2865-2869` says SemiSmart only works when `CHECK_GOOD_MOVE` is not already set. | The old v1 all-three-flags behavior was mainly `Negatives + Positives`, not additive SemiSmart plus Positives. |
| NatDex/Ironmon reference | `02_external/references/cyansmp64-upr-zx-natdex/.../Gen3RomHandler.java:2067-2068` ORs `0x07`; NatDex FireRed maps bits to `CHECK_BAD_MOVE`, `CHECK_VIABILITY`, `TRY_TO_FAINT` at `include/constants/battle_ai.h:37-39`. | NatDex `0x07` is not semantically identical to CFRU `BAD | SEMI | GOOD`. |

## Current option-menu interpretation

This table describes probable trainer-battle move-AI effects only. It does not include separate Difficulty, Level Scaling, trainer strength, wild/raid AI or battle-rule effects.

| Trainer AI option | Raw/profile behavior | Likely trainer move-AI effect |
| --- | --- | --- |
| `Auto` | raw `0`; `GetTrainerAIProfile()` derives from `VAR_GAME_DIFFICULTY`; legacy `FLAG_SMART_TRAINER_AI` can still enable Smart. | Normal/Vanilla difficulty derives `Normal`; Easy/Hard/Expert derive their matching profile. If the legacy flag is set, Smart v2 ORs `BAD | SEMI`. |
| `Vanilla` | explicit `TRAINER_AI_PROFILE_VANILLA`; `IsSmartTrainerAIEnabled()` returns false. | Preserves trainer data `aiFlags`; no Easy downgrade, Hard/Expert SemiSmart uplift, or Smart v2 hook. |
| `Easy` | explicit `TRAINER_AI_PROFILE_EASY`. | If a trainer has `CHECK_GOOD_MOVE`, it is downgraded to SemiSmart; otherwise trainers are forced to `CHECK_BAD_MOVE`. |
| `Normal` | explicit `TRAINER_AI_PROFILE_NORMAL`; Smart helper false. | Preserves trainer data `aiFlags`, similar to Vanilla for the current trainer-AI hook. |
| `Hard` | explicit `TRAINER_AI_PROFILE_HARD`. | Trainers without `CHECK_GOOD_MOVE` gain `SEMI_SMART`; trainers already marked very smart keep their stronger flags. |
| `Expert` | explicit `TRAINER_AI_PROFILE_EXPERT`. | Same regular-trainer SemiSmart uplift as Hard in `GetAIFlags`; other Expert-like anti-cheese hooks may check profile elsewhere, but this is not a clean Smokescreen fix by itself. |
| `Smart` | explicit `TRAINER_AI_PROFILE_SMART_AI`; `IsSmartTrainerAIEnabled()` true. | Current v2 behavior ORs `CHECK_BAD_MOVE | SEMI_SMART`; it does not globally add `CHECK_GOOD_MOVE`. |

Key caveat: if the sampled Rival trainer data already includes `CHECK_GOOD_MOVE`, even `Normal`, `Hard`, `Expert` or `Smart` may preserve that source trainer flag. The smoke should therefore compare observed behavior, not infer final flags from the menu label alone.

## Behavior assessment matrix

| Classification | Evidence shape | Interpretation | Possible fix direction |
| --- | --- | --- | --- |
| Plausible behavior | Smokescreen is selected while Accuracy can still be lowered, especially when Tackle is weak, non-KO, resisted, or tied by score. | CFRU `CHECK_BAD_MOVE` does not reject valid Accuracy-down moves, and neutral status can tie or beat low-impact damage. | No immediate code fix; document as AI personality unless local A/B shows poor default behavior. |
| Suspicious behavior | Smokescreen is selected on most or all turns until Accuracy minimum when Tackle is a reasonable damage option and no stall/residual setup exists. | Likely utility/tie-break issue for Randomizer/Ironmon expectations. | Add a targeted smoke first; possible later v3 tie-break or repeated-Accuracy-down dampening. |
| Clear bug | Smokescreen is selected after Accuracy can no longer be lowered, into Keen Eye/stat-block immunity, or while a guaranteed KO is available. | Contradicts the negative-scoring and KO-shortcut intent. | Source fix likely in Accuracy-down negative checks, `GoodIdeaToLowerAccuracy`, or final move tie-break/repetition handling. |
| Design mismatch | `CHECK_GOOD_MOVE` profiles repeatedly choose Smokescreen because `AIScript_Positives` boosts it as good utility. | Known v1-style CFRU utility behavior, not NatDex/Ironmon `0x07` fidelity. | Do not re-add `CHECK_GOOD_MOVE` globally; consider NatDex-style `CHECK_VIABILITY` / `TRY_TO_FAINT` source-port or narrower CFRU scoring adjustment. |

## Local mGBA A/B smoke plan

Use the same local ROM candidate and the same Rival battle state for all variants. Do not commit ROMs, saves, emulator states, builds, screenshots, raw logs, hashes or private paths.

1. Prepare one reproducible local save/state immediately before the Rival battle.
2. Confirm the opposing Pokemon has exactly the relevant observed choice set: at minimum `Tackle` and `Smokescreen`.
3. Run the same first-battle segment under these Trainer AI menu values: `Auto`, `Vanilla`, `Normal`, `Hard`, `Expert`, and `Smart`. Add `Easy` only if a weaker-AI comparison is useful.
4. For each variant, record only sanitized turn summaries:
   - AI option
   - turn number
   - enemy move selected: `Tackle`, `Smokescreen`, or other
   - player Accuracy stage bucket: neutral, lowered, minimum
   - whether Tackle looked like a likely KO / meaningful damage / chip only
   - result category: plausible, suspicious, clear bug
5. Repeat each option at least three times if RNG changes the chosen move among ties.
6. Keep Game Difficulty, Level Scaling, Hard Cap, party, items and player actions fixed unless the row explicitly tests a different option.
7. Do not use screenshots or raw emulator logs as committed evidence; summarize observations in a future sanitized test note only.

Suggested result table for the later smoke:

| AI option | Runs | Smokescreen before min | Smokescreen at/after min | Tackle selected | Notes |
| --- | --- | --- | --- | --- | --- |
| Auto | TBD | TBD | TBD | TBD | Sanitized only |
| Vanilla | TBD | TBD | TBD | TBD | Sanitized only |
| Normal | TBD | TBD | TBD | TBD | Sanitized only |
| Hard | TBD | TBD | TBD | TBD | Sanitized only |
| Expert | TBD | TBD | TBD | TBD | Sanitized only |
| Smart | TBD | TBD | TBD | TBD | Sanitized only |

## Recommendation

Do not change CFRU or UPR-FVX code from the single Smokescreen observation.

Run the mGBA A/B smoke first. If only `CHECK_GOOD_MOVE`-preserving profiles spam Smokescreen, treat it as the known CFRU positive-utility behavior and avoid global `CHECK_GOOD_MOVE` for Smart Trainer AI. If `Smart` v2 or `Hard/Expert` still spam Smokescreen to minimum in a simple Tackle/Smokescreen Rival case, design a narrow v3 proposal around repeated Accuracy-down dampening or damage-over-neutral-utility tie-breaks.

## Risks and assumptions

- The observed battle was reported as sanitized local evidence and was not reproduced by Codex.
- The exact trainer data flags for the observed Rival row were not committed here; a future local smoke should keep that private if derived from ROM/runtime artifacts.
- `Vanilla` and `Normal` are currently very similar for the trainer-AI hook, but may differ elsewhere in difficulty-owned game rules.
- A/B results can be affected by RNG tie-breaking, damage rolls, speed, player actions, held items, abilities, and whether the Rival trainer already has `CHECK_GOOD_MOVE`.
