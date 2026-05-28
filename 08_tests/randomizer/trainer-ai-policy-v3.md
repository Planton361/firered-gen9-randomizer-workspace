# Trainer AI Policy v3 experiment

Stand: 2026-05-28

## Scope

This is the sanitized implementation and local smoke handoff for CFRU branch `experiment/trainer-ai-policy-v3`.

No ROMs, saves, emulator states, builds, tool binaries, screenshots, raw logs, ROM hashes, private paths, tokens, secrets or `.env` data are included.

## CFRU implementation summary

- Base CFRU commit: `caaf81b2582d5af0905281aab88658ac145b43eb`.
- Experiment CFRU commit: `74310deeb62c7f73ba6c7b11f921418617a9a740`.
- CFRU branch: `experiment/trainer-ai-policy-v3`.
- Workspace branch: `experiment/trainer-ai-policy-v3`.

Trainer-AI policy:

| Trainer AI profile | Implemented behavior |
| --- | --- |
| `Auto` | Compatibility mode: `GetTrainerAIProfile()` continues to derive from `Game Difficulty` while the profile var is unset. |
| `Vanilla` | Unchanged: trainer data `aiFlags` are preserved without policy uplift. |
| `Easy` | Unchanged: smart trainers are downgraded away from `CHECK_GOOD_MOVE`; other trainers use basic bad-move checking. |
| `Normal` | Unchanged: trainer data `aiFlags` are preserved without policy uplift. |
| `Smart` | All trainer battles receive full smart move AI: `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_SEMI_SMART`, and `AI_SCRIPT_CHECK_GOOD_MOVE`; Expert extras are not enabled. |
| `Hard` | All trainer battles receive full smart move AI plus fair anti-cheese / Protect-Fake-Out retarget reactions. Switch prediction, shift-switching, bench prediction, and hidden type-resist berry knowledge remain excluded. |
| `Expert` | All trainer battles receive full smart move AI and retain advanced Expert paths: anti-cheese, Protect/Fake-Out retargeting, switch/prediction behavior, shift-switching, and type-resist berry knowledge where the existing CFRU Expert path allows it. |

## Source-backed change points

- `src/Battle_AI/ai_master.c`
  - `GetAIFlags()` now grants full smart move AI to explicit `Smart`, `Hard`, and `Expert` trainer AI profiles.
  - The legacy smart trainer flag path also grants the full three move-AI scripts for trainer battles.
  - New local profile predicates avoid ordinal `>=` checks so explicit `Smart` is not accidentally treated as Expert.
  - Player-switch prediction is Expert-only for trainer profiles.
  - Repeated-switch / Choice-lock anti-cheese and Protect/Fake-Out retargeting are enabled for Hard and Expert.
- `src/Battle_AI/ai_switching.c`
  - Shift/Semi-Shift AI switching is Expert-only for trainer profiles.
- `src/damage_calc.c`
  - Type-resist berry knowledge remains Expert-only for trainer profiles; explicit `Smart` and `Hard` do not receive this hidden-knowledge path.

`src/damage_calc.c` is included because the requested `rg` search showed the type-resist berry Expert gate there.

## Unchanged boundaries

- No `VAR_GAME_DIFFICULTY` broad effects were changed.
- No trainer level scaling, IV, EV, friendship, PP, bag restriction, move restriction, wild AI, raid AI, DexNav, ability-capsule, UPR-FVX or DPE behavior was changed.
- `AI_TRY_TO_KILL_RATE` was not changed.
- No ROM build or full-playthrough result is claimed.

## Checks performed

- CFRU `git diff --check`: pass.
- CFRU syntax-only:
  - `arm-none-eabi-gcc -fsyntax-only src/Battle_AI/ai_master.c`: pass.
  - `arm-none-eabi-gcc -fsyntax-only src/Battle_AI/ai_switching.c`: pass.
  - `arm-none-eabi-gcc -fsyntax-only src/damage_calc.c`: pass.

Note: a first syntax-only attempt with broad `-I include` failed before reaching the changed source because CFRU's local `include/strings.h` shadows the toolchain's system `strings.h`. The successful checks used CFRU's relative source includes without that broad include override.

## Sanitized local mGBA smoke result

Result: `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`.

The CFRU Trainer-AI-Policy v3 experiment was locally built and the resulting local ROM candidate booted in mGBA. The in-game options menu exposed the `Trainer AI` values, and selected Trainer-AI values appeared to persist after changing them.

Sanitized local observations:

| Area | Result | Notes |
| --- | --- | --- |
| Build / boot | Pass | Local CFRU build completed and the local ROM candidate booted in mGBA. |
| Options menu | Pass | `Trainer AI` values were selectable and appeared to save correctly. |
| Rival Smokescreen / move-choice smoke | Pass with caveats | Targeted local observation only; no raw turn log, screenshot, save, state, ROM path or ROM hash is included. |
| `Smart` | Pass with caveats | Full Smart Move-AI appeared active. No Expert-extra behavior is claimed from this smoke. |
| `Hard` | Pass with caveats | Smart move choice plus stronger fair reactions appeared distinguishable from `Smart`; no obvious hidden-knowledge behavior was observed. |
| `Expert` | Pass with caveats | Strongest mode appeared plausibly active and distinguishable, with advanced behavior looking consistent with the intended Expert profile. |

This smoke confirms the local build/boot/menu and targeted move-choice behavior only. It is not a full-playthrough, BizHawk, Ironmon Tracker, statistical AI-quality or P1 support claim.

## Local mGBA smoke handoff

Use the same local ROM candidate and the same sanitized pre-battle setup across options. Do not commit ROMs, saves, emulator states, builds, screenshots, raw logs, hashes or private paths.

Suggested matrix:

| AI option | Expected policy result | Sanitized observations to record |
| --- | --- | --- |
| `Vanilla` | Trainer data AI only. | Turn-by-turn moves, Accuracy stage bucket, no private artifacts. |
| `Normal` | Trainer data AI only. | Same battle state and player actions as other rows. |
| `Smart` | Full smart move AI only; no Expert extras. | Whether Smokescreen repeats to minimum, whether Tackle is selected when damage is meaningful. |
| `Hard` | Full smart move AI plus fair anti-cheese / Protect-Fake-Out reactions; no prediction/hidden berry knowledge. | Same move-choice table; optionally a separate doubles Protect/Fake-Out micro-smoke. |
| `Expert` | Full smart move AI plus advanced Expert behavior. | Compare against Hard for prediction/anti-cheese differences without claiming full support. |
| `Auto` | Derived from `Game Difficulty`. | Record the current Game Difficulty value alongside the AI option. |

Result categories should stay conservative: plausible, suspicious, clear bug, or design mismatch. No full-playthrough or P1 support claim should be made from this experiment.
