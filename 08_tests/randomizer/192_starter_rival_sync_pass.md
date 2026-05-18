# 192 - Starter/Rival Sync Pass

## Scope

Sync merged UPR-FVX PR #97 and record sanitized local Starter/Rival sync smoke evidence.

Codex did not read, copy, change or generate ROMs.

## Synced Pin

- UPR-FVX PR #97: `fix: correct oak lab rival slot mapping`.
- Workspace submodule `02_external/upr-fvx`: `51d52a03235664154549105003dadfb45c76d0d0`.

## Root Cause

- The FireRed/CFRU-DPE Oak-Lab Rival uses raw `TrainerData` party rows that did not run through the normal loaded trainer list.
- PR #96 targeted that raw runtime source.
- PR #97 corrected the starter-slot projection to `[328, 326, 327]`.

Counter-slot rule:

- Player slot 0 -> Rival gets starter slot 1.
- Player slot 1 -> Rival gets starter slot 2.
- Player slot 2 -> Rival gets starter slot 0.

## Sanitized Evidence

- Starter slot 1: Groudon.
- Starter slot 2: Fearow.
- Starter slot 3: Mudbray.
- Player chose: Groudon.
- Expected Rival: Fearow.
- Observed Rival: Fearow.
- Rival matched randomized counter-slot: yes.
- Vanilla fallback observed: no.
- Same-starter bug observed: no.
- Crash observed: no.
- Softlock observed: no.

## Interpretation

- Starter Pokemon passed for the Oak-Lab first Rival smoke.
- Stable Visual Profile can now optionally include Starter Pokemon for local sampling.
- `Rival Carries Starter Through Game` remains a separate, not-tested full-rival path.

## Remaining Caveats

- This is a short targeted smoke, not a full playthrough.
- Trainer Class Names remains textlabel remapping only and can visually mismatch trainer sprites/class ids.
- Special-Wild, Day/Night and Swarms remain out-of-scope for the stable profile.
- No P1 promotion is made from this smoke.

## Next Recommended Block

- Run a Stable Visual Profile plus Starter Pokemon local smoke with Trainer Class Names and Special-Wild still disabled.
- Alternatively isolate `Rival Carries Starter Through Game` as a separate full-rival path.

## Safety Boundary

- No ROM paths.
- No output ROM paths.
- No hashes.
- No screenshots.
- No full logs.
- No saves or emulator states.
- No secrets, tokens or `.env` details.
- No UPR-FVX/CFRU/DPE code changes.
- No P1 promotion.
