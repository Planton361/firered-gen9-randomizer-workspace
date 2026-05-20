# 210 - Misc Tweaks Behavior Smoke

## Scope

This evidence records sanitized local Misc Tweaks behavior-smoke results after syncing UPR-FVX PR #125, PR #126 and
PR #127 into the `compat/firered-gen9-cfru-dpe` line.

Codex did not run ROMs, inspect ROMs, generate output ROMs or execute emulator/gameplay checks for this evidence.

## UPR-FVX Pin

- Base branch: `compat/firered-gen9-cfru-dpe`.
- PR #125 fixed CFRU/DPE BPRE Running Shoes misc-tweak behavior.
- PR #126 fixed CFRU/DPE BPRE Catching Tutorial species mapping.
- PR #127 made Fast Egg Hatching skip species without `BreedingInfo`.
- Workspace submodule `02_external/upr-fvx` is pinned to merged PR #127 commit `155fac0b33474f6ed5b3fbaed7dd9bf24b4e1315`.

## Local Evidence

| Feature / behavior | Local result | Caveat |
|---|---|---|
| Fastest Text | pass | Targeted behavior smoke only. |
| Randomize PC Potion | pass | Targeted behavior smoke only. |
| Ban Lucky Egg | likely pass / no issue observed | No stronger dedicated item-drop proof was provided. |
| Run Without Running Shoes | pass | Confirmed after the CFRU/DPE-specific running-shoes fix. |
| Running Shoes Indoors | pass | Confirmed after the CFRU/DPE-specific running-shoes fix. |
| Randomize Catching Tutorial | pass | No question-mark sprite or `????????` name observed after the species mapping fix. |
| Fast Egg Hatching | crash-free randomization smoke; output loads | No full hatch-cycle proof. |
| Reusable TMs | CFRU-provided; do not duplicate in UPR-FVX stable profile | Keep as profile caveat rather than a separate UPR-FVX behavior claim. |
| Forgettable HMs | CFRU-provided; do not duplicate in UPR-FVX stable profile | Keep as profile caveat rather than a separate UPR-FVX behavior claim. |

No crash or freeze was observed in the tested paths.

## Status

Misc Tweaks are `PASS_TARGETED_BEHAVIOR_SMOKE_WITH_CAVEATS` for the documented targeted behavior-smoke scope.

This is not a full playthrough, not a complete per-option proof for every Misc suboption, not a full hatch-cycle proof,
and not a P1 promotion.

## Safety

No output ROMs, private paths, ROM hashes, full logs, screenshots, saves, emulator states, secrets, tokens or `.env`
content are documented here.
