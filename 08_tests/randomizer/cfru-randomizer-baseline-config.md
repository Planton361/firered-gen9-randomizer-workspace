# CFRU Randomizer Baseline Config

Stand: 2026-05-29

## Scope

This records the source-backed CFRU Randomizer-/Ironmon-near baseline configuration on CFRU branch `feature/cfru-randomizer-baseline-config`.

No ROMs, saves, emulator states, builds, tool binaries, screenshots, raw logs, ROM hashes, private paths, tokens, secrets or `.env` data are included.

## CFRU implementation summary

- Base CFRU commit: `74310deeb62c7f73ba6c7b11f921418617a9a740`.
- Baseline CFRU commit: `53273184bab06f91cdc3ad6e0e5af4a8ba41591a`.
- CFRU branch: `feature/cfru-randomizer-baseline-config`.
- Workspace branch: `feature/cfru-randomizer-baseline-config`.

Compile-time baseline:

| Setting | Result |
| --- | --- |
| Oak Tutorial | `TUTORIAL_BATTLES` disabled. |
| Overworld Poison | `POISON_1_HP_SURVIVAL` disabled, so poisoned Pokemon can faint in the overworld. |
| SwSh catch level malus | `SWSH_CATCHING_DIFFICULTY_MODIFIER` disabled. |
| Old EXP system | `OLD_EXP_SPLIT` enabled. |
| Flat EXP formula | `FLAT_EXP_FORMULA` enabled. |
| Intro Controls Guide | `SKIP_INTRO_CONTROLS_GUIDE` enabled. |
| Wild Ignore/Engage compile gate | `IgnoreWildPokemon` left enabled because source shows it compiles the prebattle feature and runtime use is gated by flags. |

Runtime option-menu toggles:

| Toggle | Backing state | Implementation |
| --- | --- | --- |
| `Nuzlocke = Off/On` | `FLAG_NUZLOCKE` | Page 3 option row. It only clears/sets `FLAG_NUZLOCKE`. |
| `Wild Prebattle = Off/On` | `FLAG_ENABLE_WILD_PMN_PREBATTLE_SCREEN` | Page 3 option row. It only clears/sets the enable flag. |

`FLAG_WILD_POKEMON_PREBATTLE_SCREEN` is intentionally not menu-owned. Source shows it is a transient encounter/window flag set while generating the prebattle screen and cleared by `CreateWindowFromRect()`.

## Source-backed toggle analysis

Nuzlocke source reads found:

- `src/battle_controller_opponent.c`: nickname behavior is gated by `FlagGet(FLAG_NUZLOCKE)`.
- `src/party_menu.c`: revive-item blocking is gated by `FlagGet(FLAG_NUZLOCKE)`.
- `src/overworld.c`: map transition, battle-end, whiteout and eraser behavior are gated by `FlagGet(FLAG_NUZLOCKE)`.

No permanent script activation path was added, and the option menu does not set Nuzlocke-related helper flags or vars.

Wild Prebattle source reads found:

- `src/wild_encounter.c`: prebattle screen generation is gated by `FlagGet(FLAG_ENABLE_WILD_PMN_PREBATTLE_SCREEN)`.
- `src/wild_encounter.c`: `FLAG_WILD_POKEMON_PREBATTLE_SCREEN` is set only when the prebattle script is launched.
- `src/scripting.c`: `FLAG_WILD_POKEMON_PREBATTLE_SCREEN` is read for window/palette behavior and cleared in `CreateWindowFromRect()`.

The menu therefore owns only `FLAG_ENABLE_WILD_PMN_PREBATTLE_SCREEN`.

## Checks performed

- CFRU `git diff --check`: pass.
- CFRU syntax-only:
  - `arm-none-eabi-gcc -fsyntax-only src/option_menu.c`: pass.

## Sanitized local build / mGBA smoke

Result: `PASS_TARGETED_LOCAL_BUILD_BOOT_SETTINGS_SMOKE_WITH_CAVEATS`.

Local reported evidence:

- CFRU commit `53273184bab06f91cdc3ad6e0e5af4a8ba41591a` was synchronized into the local Mac build workspace.
- A local clean rebuild completed successfully.
- `wav2agb` and `mid2agb` were found through local `local-bin` wrappers.
- The local ROM candidate booted in mGBA.
- The new/adjusted in-game settings worked in the local smoke.

No ROMs, saves, emulator states, screenshots, raw logs, hashes, build outputs, tool binaries, private paths, tokens, secrets or `.env` data are included.

| Area | Result | Notes |
| --- | --- | --- |
| Build / boot | Pass | Local clean rebuild succeeded and the local ROM candidate booted in mGBA. |
| Options / settings | Pass | New/adjusted settings were reported working in game. |
| Oak Tutorial removed | Inconclusive | Not separately documented in this sanitized report. |
| Poison overworld faint | Inconclusive | Not separately documented in this sanitized report. |
| SwSh catch-level malus off | Inconclusive | Not separately documented in this sanitized report. |
| Old / flat EXP | Inconclusive | Not separately documented in this sanitized report. |
| Intro Controls Guide skipped | Inconclusive | Not separately documented in this sanitized report. |
| Nuzlocke toggle | Pass | Covered by the reported in-game settings smoke. |
| Wild Prebattle toggle | Pass | Covered by the reported in-game settings smoke. |

## Caveats

- This is a targeted local build/boot/settings smoke only, not a full-playthrough result.
- No BizHawk validation, Ironmon Tracker validation or P1 support claim is included.
- Turning `Nuzlocke` off only clears `FLAG_NUZLOCKE`; it does not unwind any already-created Nuzlocke side state such as caught-area tracking or no-catching flags.
- `Wild Prebattle` controls the existing enable flag only; no gameplay logic, encounter tables, randomizer behavior or prebattle script logic was changed.
