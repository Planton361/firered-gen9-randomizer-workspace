# CFRU Early Running Workspace Integration Evidence

**Target:** WORKSPACE_CFRU_EARLY_RUNNING_PIN_READY
**Classification:** revision-bound source/integration evidence; no runtime acceptance.

## Workspace and source revisions

- Workspace base: 124f6c760a0d2f6aaccd1283d6df5d39618fffc7
- Workspace branch: integration/cfru-early-running-pin
- Final Workspace branch SHA: the containing PR head; the exact SHA is recorded in the revision-bound #539 handoff comment after push.
- CFRU Gitlink before: d851256f2bb897042fbe865b4533e55fc7586ba9
- CFRU Gitlink after: 11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec
- Accepted #538 CFRU source head: e10c27175acc7a3541567eac0965ca39c9d301de
- User-merged CFRU revision: 11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec
- CFRU PR #57: https://github.com/Planton361/CFRU-expansion/pull/57

Live GitHub comparison proves the accepted source head is exactly one commit behind the merge revision, with zero changed files. The current CFRU compat/firered-gen9-randomizer branch equals the merged revision.

Unchanged component Gitlinks:

- DPE: 22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc
- UPR-FVX: 0e3be63e94e34215cc35308d64e8db15e9a3c48c
- Ironmon Tracker: c450ecaee2d8131a2789bb656e3be792a93712fb
- NatDexExtension: a94b8844800308248bb5090b6c36c8b2d7e5d7b9

## Workspace diff proof

The exact changed Workspace paths are:

1. 02_external/CFRU-expansion — one 160000 Gitlink entry, old SHA d851256f2bb897042fbe865b4533e55fc7586ba9, new SHA 11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec.
2. docs/testing/cfru-early-running-workspace-integration-2026-09-28.md — this evidence document.

All other Gitlinks are byte-identical to the Workspace base. No other ordinary Workspace source file changed.

## Exact-pin checks

All checks below ran from CFRU revision 11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec.

- scripts/tests/run_early_running_pewter_tests.py — PASS.
- scripts/tests/run_settings_defaults_tests.py — PASS.
- scripts/tests/run_standard_ai_tests.py — PASS.
- scripts/tests/run_ironmon_ai_tests.py — PASS.
- scripts/insert.py --check-map-object-overlays — PASS when run directly; it is also included in the Early Running runner.
- CFRU git diff --check — PASS.
- Workspace safety check and Workspace git diff --check — PASS.

The Fresh New Game defaults remain Difficulty Vanilla, Trainer Level Scaling Off, Wild Level Scaling Off, and Trainer AI Standard. Trainer AI raw mappings remain unchanged. Difficulty, Trainer Scaling, and Wild Scaling remain independent. Ironmon preset mappings remain unchanged and do not modify running flags. The Standard AI suite and Ironmon Smart suite pass without retuning.

## Accepted Early Running and Pewter invariants

Fresh New Game calls ApplyFreshNewGameSettings() after the new-save wipe and sets the existing FLAG_RUNNING_ENABLED. FLAG_AUTO_RUN remains untouched, ordinary save loading does not call fresh initialization, FLAG_RUNNING_ENABLED remains defined, and the L Auto-Run path remains gated by it. B-button behavior and metatile, DexNav, underwater, and indoor-running restrictions remain unchanged.

Brock's trainer and reward flow remains unmodified. Public Pewter structure remains bank/map 3/2 with event counts 7/7/7/6. Exactly one Aide object script pointer and three Scene-1 CoordEvent script pointers are replaced. All four routes share EventScript_PewterRunningShoesCleanup. The cleanup advances the scene to 2, hides and removes the Aide, releases control, and ends without Running-Shoes tutorial dialogue, a Mom letter, or a long movement sequence.

Synthetic exact-pointer and fail-closed checks pass. Wrong map, event counts, object fields, or CoordEvent fields terminate the insertion without fallback. The checks confirm only the four existing 4-byte script-pointer fields are changed; map-header and event-table pointers/counts are not repointed.

## ABI, layout, and save disposition

This pin introduces no SaveBlock layout or expanded Vars/flags layout change; it uses the existing running flag. Pokémon, Trainer, BattleMove, and NewBattleStruct layouts are unchanged. DPE ABI and randomizer-visible table formats are unchanged. There is no pointer/repoint contract change: the four existing Pewter script-pointer values are replaced, with no map-header or event-table repoint.

## ARM and full-build disposition

ARM_RECHECK_UNAVAILABLE_ENVIRONMENT. arm-none-eabi-as, arm-none-eabi-gcc, and arm-none-eabi-ld are unavailable in this environment. No tools were installed or downloaded. A full CFRU source build was not run because the required devkitARM / arm-none-eabi toolchain is unavailable; make alone is insufficient.

## Protected boundary and runtime limit

No ROM, save, emulator state, generated build, screenshot, raw private log, ROM hash, tool binary, private path, .env file, token, key, or secret was accessed or included. Protected-boundary safety checks passed.

No emulator or runtime test was run. This evidence establishes source and integration checks at the exact pin only; early-running runtime acceptance remains user-owned.

## Routing and Project metadata

#537 remains the active ROM Finish audit. #498 remains the umbrella/blocking acceptance contract. After Workspace merge and CONTROL verification, #537 resumes the remaining ROM Finish/QoL decisions; final Randomizer alignment remains downstream of ROM QoL finish, followed by #499 BizHawk and #500 Tracker. #499, #500, and #501 were left unchanged. UPSTREAM_CONTRIBUTION = DEFERRED.

Project metadata verified live after the update: #538 Done; #539 P0 / Integration / Doing; #537 P0 / Discover / Doing (Project work type used for the active audit); #498 P0 / Runtime Acceptance / Blocked; #499, #500, and #501 remain P1 / Tracker-BizHawk / Backlog, P1 / Tracker-BizHawk / Backlog, and P1 / Release / Backlog respectively.
