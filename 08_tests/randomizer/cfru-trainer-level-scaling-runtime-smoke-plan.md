# CFRU Trainer Level Scaling Runtime Smoke Plan

Stand: 2026-05-27

## Scope

This is a sanitized smoke plan for the CFRU trainer-level-scaling runtime gate. It does not include ROMs, output ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, local addresses, secrets, tokens, or `.env` data.

## Source Baseline

- `src/config.h` defines `SCALED_TRAINERS`, so `CreateNPCTrainerParty()` compiles the trainer-level-scaling setup instead of the no-scaling fallback.
- `src/config.h` defines `VAR_TRAINER_LEVEL_SCALING_MODE 0x515A`.
- `src/util.c` maps raw `VAR_TRAINER_LEVEL_SCALING_MODE == 0` to legacy Difficulty-derived scaling and raw explicit values to `Off / Easy / Normal / Hard / Expert`.
- `src/build_pokemon.c` uses `GetTrainerLevelScalingMode()` in the trainer-scaling enable gate and in the generic/boss scaling formulas.

## Smoke Matrix

| Case | Game Difficulty | Level Scaling row | Expected trainer level behavior |
| --- | --- | --- | --- |
| A: Off override | Expert | Off | Trainer level scaling stays disabled; early generic trainers remain at source levels. |
| B: Auto legacy | Expert | Auto | Raw `0` derives from Difficulty and should use Expert-era trainer scaling. |
| C: Explicit Expert | Any | Expert | Generic trainer scaling should visibly raise early trainers toward the party average. |

## Focused Runtime Check

Use a sanitized early generic trainer case, such as a Viridian Forest-style Bug Catcher:

- player party: one Lv17 Pokemon,
- trainer category: generic trainer, not boss, not pseudo-boss,
- expected explicit Expert result: roughly Lv15 for flat early source-level teams, not Lv9/Lv10.

If the trainer still stays around Lv9/Lv10 with explicit Expert, re-check whether the build used the CFRU commit with `SCALED_TRAINERS` enabled and whether the options menu wrote raw `VAR_TRAINER_LEVEL_SCALING_MODE == 5`.

## Regression Boundaries

Do not use this smoke to change or validate:

- Trainer AI Profile,
- Smart Trainer AI,
- Better Movesets,
- Wild Level Scaling,
- UI page layout,
- UPR-FVX, DPE, or Tracker behavior.

## Final Local Smoke Result

Status: `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`

Sanitized local observation for the current CFRU difficulty-split settings:

- Page 3 displays `Level Scaling` and `Trainer AI` cleanly.
- `Level Scaling` values `Off`, `Easy`, `Normal`, `Hard`, and `Expert` visibly change trainer levels according to the selected setting.
- `Level Scaling = Off` keeps trainer scaling disabled rather than acting like Easy Difficulty.
- Explicit scaling modes no longer require changing `Game Difficulty`.
- `Game Difficulty` remains separate and still controls Difficulty-owned rules, including the Expert bag restriction.
- `Trainer AI` remains separately selectable and did not need Level Scaling or Game Difficulty changes to show runtime effect.

Interpretation:

- The `SCALED_TRAINERS` gate is active for trainer runtime scaling.
- The split `VAR_TRAINER_LEVEL_SCALING_MODE` setting is reaching trainer battle construction.
- The smoke is targeted local evidence, not a Full-Playthrough or full route/trainer matrix.

Previously validated baseline:

- Better Movesets and trainer row write/reload behavior had already been validated separately, so this smoke was focused on CFRU split-setting runtime behavior rather than reopening Trainer Rows or Better Movesets.

## Vanilla Difficulty Follow-up

When `Difficulty = Vanilla` is available, smoke it as a separate battle-profile case rather than as a replacement for legacy Normal:

| Case | Difficulty | Level Scaling | Trainer AI | Expected boundary |
| --- | --- | --- | --- | --- |
| D: Vanilla profile | Vanilla | Off | Smart | No Difficulty-owned trainer EV/power, player restriction, fog penalty, raid item-punishment, wild boss scaling, or Expert rules; trainer levels stay unscaled because Level Scaling is explicitly Off; Trainer AI remains active because it is separately set. |

Raw `VAR_GAME_DIFFICULTY == 0` must still behave as legacy Normal. Vanilla should be tested through its explicit raw value only.
