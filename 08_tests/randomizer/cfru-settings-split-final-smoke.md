# CFRU Settings Split Final Smoke

Stand: 2026-05-27

## Scope

This is a documentation-only record of the final local smoke for the CFRU settings-split UI.

No ROMs, output ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, local addresses, secrets, tokens, or `.env` data are included or required as committed evidence.

## Settings Under Smoke

| Setting area | UI values checked | Expected ownership |
| --- | --- | --- |
| Page 3 layout | `Level Scaling`, `Trainer AI`, `Hard Cap`, `Cancel` | New split settings fit on Page 3; Page 2 remains the existing CFRU settings page. |
| Trainer Level Scaling | `Auto`, `Off`, `Easy`, `Normal`, `Hard`, `Expert` | Trainer level scaling only, backed by `VAR_TRAINER_LEVEL_SCALING_MODE`. |
| Trainer AI | `Auto`, `Vanilla`, `Easy`, `Normal`, `Hard`, `Expert`, `Smart` | Trainer AI profile only, backed by `VAR_TRAINER_AI_PROFILE`. |
| Game Difficulty | `Vanilla`, `Normal`, `Expert` spot checks | Difficulty-owned trainer power, player restrictions, and battle/wild rules only. |
| Hard Cap | `Auto`, `Off`, `On` | Menu-owned hard-cap preference backed by `VAR_HARD_LEVEL_CAP_MODE` and applied through `FLAG_HARD_LEVEL_CAP`. |
| Wild Level Scaling | Existing separate behavior | Remains separate from Trainer Level Scaling and Game Difficulty. |
| Randomizer-only trainer settings | Better Movesets / Trainer Rows baseline | Remain UPR-FVX-side behavior and are not CFRU Page 3 settings. |

## Final Smoke Result

Status: `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`

| Area | Result | Sanitized observation |
| --- | --- | --- |
| Page 3 layout | Pass | Page 3 displays `Level Scaling`, `Trainer AI`, `Hard Cap`, and `Cancel` cleanly; footer/cancel navigation remains usable. |
| Trainer Level Scaling | Pass | `Off`, `Easy`, `Normal`, `Hard`, and `Expert` visibly change trainer levels according to the selected setting. |
| Trainer AI | Pass | Trainer AI behavior is separately controllable and can be exercised without changing Game Difficulty or Trainer Level Scaling. |
| Game Difficulty | Pass | `Vanilla`, `Normal`, and `Expert` are separately usable; Difficulty-owned effects remain separate from Level Scaling and Trainer AI. |
| Hard Cap | Pass with caveat | `Auto`, `Off`, and `On` are visible on Page 3 and behave plausibly through the menu-owned mode/flag plumbing. |
| Wild Level Scaling | Pass | Wild Level Scaling remains separate from Trainer Level Scaling and from Game Difficulty. |
| Better Movesets / Trainer Rows | Baseline retained | Previously validated Better Movesets and Trainer Row behavior was not reopened in this UI smoke. |

## Interpretation

- The CFRU settings split is locally smoke-confirmed as a usable UI/runtime split for the tested profile.
- `Level Scaling` can be changed independently from `Game Difficulty`.
- `Trainer AI` can be changed independently from `Game Difficulty` and Trainer Level Scaling.
- `Game Difficulty = Vanilla` is available as the no-Difficulty-power/rules profile without reinterpreting legacy raw `0` Normal.
- `Hard Cap = Auto / Off / On` is visible as the final Page 3 row and uses the intended menu-owned state boundary.
- Wild Level Scaling and UPR-FVX Randomizer-only trainer settings remain outside the CFRU Page 3 split settings.

## Caveats

- This is targeted local smoke evidence, not a full playthrough.
- It is not a full route/trainer matrix, a statistical Trainer-AI quality evaluation, or a complete hard-cap boundary matrix.
- The hard-cap result is menu/runtime-plumbing smoke only; EXP, Rare Candy, Daycare, DexNav, Wild, and Trainer Level Scaling enforcement code paths were intentionally not changed in that UI block.
- Do not use this smoke to claim changes to Better Movesets, Trainer Evolution, UPR-FVX, DPE, Tracker, or ROM/build tooling.

## Handoff

- Treat this file as the current sanitized final local smoke record for the CFRU settings-split UI.
- If a later regression appears, isolate it by setting owner first: Game Difficulty, Trainer Level Scaling, Trainer AI, Hard Cap, Wild Level Scaling, or UPR-FVX Randomizer-only trainer settings.
- Keep future evidence sanitized: no ROMs, saves, screenshots, raw logs, hashes, private paths, builds, local addresses, secrets, tokens, or `.env` data.
