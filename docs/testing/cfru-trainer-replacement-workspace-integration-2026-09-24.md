# CFRU trainer-replacement Workspace integration — merged-pin evidence

Date: 2026-09-24

Contract: [Workspace Issue #524](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/524)

Target: `WORKSPACE_CFRU_REPLACEMENT_REPAIR_PIN_READY`

Evidence classification: **CONFIRMED CURRENT STATE** for the exact source,
host and integration checks recorded here. The original S1 remains a
**CONFIRMED USER-SUPPLIED RUNTIME OBSERVATION**; this evidence does not claim
that it is fixed at runtime. This report is submitted for CONTROL review and
does not self-claim the target.

## Revision identity and Gitlink scope

| Item | Exact value |
|---|---|
| Workspace base (`main`) | `21f2d4288920a02a7f4de26ab93217c84c48a5d9` |
| Workspace branch | `integration/cfru-trainer-replacement-pin` |
| Final Workspace commit | The exact SHA is recorded in the PR head and the sanitized #524 evidence return; a commit cannot encode its own SHA in its tree. |
| Old CFRU Gitlink | `3c2f38140ed07991a04ae63ff1108ff2f25547a6` |
| Accepted #523 CFRU PR head | `481a953bf692548576ba03554b31b8f42528739f` |
| New CFRU Gitlink / merged #53 pin | `423f96f0dcd501a64c2327d726a98f1964937ac1` |
| CFRU target branch | `compat/firered-gen9-randomizer` |

`git rev-list --left-right --count 481a953...423f96f` returned `0 1`. The
merged CFRU commit parents are the old Workspace pin `3c2f381...` and accepted
PR head `481a953...`; `git diff --name-status 481a953 423f96f` returned no
paths. The accepted #523 source tree is therefore unchanged by the merge
commit.

Only the CFRU component Gitlink changed. The other component pins are
unchanged:

| Component | Final pin | Result |
|---|---|---|
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | unchanged |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` | unchanged |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` | unchanged |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | unchanged |

The intended Workspace change set is exactly:

1. `02_external/CFRU-expansion` — mode `160000`, `3c2f381...` to `423f96f...`;
2. `docs/testing/cfru-trainer-replacement-workspace-integration-2026-09-24.md` — this report.

No other Gitlink, source file, canonical status document or protected path is
changed.

## Exact merged-pin source and host gates

The following checks ran at CFRU `423f96f0dcd501a64c2327d726a98f1964937ac1`.

| Gate | Result |
|---|---|
| `python3 scripts/tests/run_replacement_safety_tests.py` | **PASS** — controller routing/ownership/emission audit; valid Standard/Ironmon two-mon replacements; `PARTY_SIZE` and out-of-range safe fallback; dead, empty, egg and current-slot rejection; opponent-party range isolation; repeated two-/three-mon replacement and final-faint behavior; voluntary target identity preserved. |
| `python3 scripts/tests/run_settings_defaults_tests.py` | **PASS** — settings wiring, raw `0..8` Trainer AI mapping and unknown-value preservation; fresh defaults `4/1/0/7`; Ironmon preset `4/1/0/8`; unrelated settings unchanged. |
| `python3 scripts/tests/run_standard_ai_tests.py` | **PASS** — Standard adapter twins `4,096 / 0` mismatches; damage-envelope oracle `98,304` cases; Standard forced replacement chooses the valid second mon; dispatch/exclusion and Ironmon replacement timing pass. |
| `python3 scripts/tests/run_ironmon_ai_tests.py` | **PASS** — Ironmon parity `63 / 63`; mandatory tags `58 / 58`; accepted v1/v2/v3 digests unchanged. |
| Workspace AI host suite | **PASS** — 98 tests. |
| `python3 scripts/check_coherent_learnsets.py` | **PASS** — 144,000 initial-moveset cases; 820 exact replacements, two form tables, seven rebindings, 27 reserved sentinel bindings; invalid edits rejected. |
| M-013/Premier source-host gate | **PASS** — 11,110 ball cases plus capacity, single-reward and non-ball controls. |
| Renewable hidden-item source gate | **PASS** — accepted table and source behavior. |
| M-009 compiled scanner host | **PASS** — actual scanner compiled and exercised against host services. |
| M-009 rejection cases | **PASS** — eight in-memory invalid ownership/order/scanner candidates rejected. |
| M-009 reference-map census | **PASS** — 426 Cyan/NatDex maps and 425 pret maps; maximum 36 BG events in each. |

The Standard host gate also retained accepted policy identities and
noninterference witnesses:

- Ironmon production twins: **1,024 / 0 mismatches**; Badge ownership twins:
  **16 / 0 mismatches**; Badge Defense/SpDef oracle: **663,000 cases**.
- Uniform-legal v1 digest:
  `71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7`.
- Standard v2 digest:
  `227ecebc2b937671cc4f2fbab1694abf1b7c186f7e455ed7daf22014b62d0a85`.
- Ironmon Smart v3 digest:
  `0a637d0bc42cb2e37701bbfa33677ae95c878b1f9a67ec55a60e15a4fbdb85d7`.
- Host layout witness: target ARM `BattleStruct=0x200`, host harness
  `BattleStruct=0x208`; save delta **0**.

### Tackle / Water Gun witness

The deterministic level-5 Charmander versus Squirtle production-adapter
witness reports both moves legal. Tackle has expected damage 3, envelope
3–18, utility 14, and is not near-best. Water Gun has expected damage 11,
envelope 10–42, utility 54, and is the sole near-best move. Water Gun is
selected from a one-move pool with zero draws and unchanged policy RNG
(`1A0B5156 -> 1A0B5156`).

The incident's exact runtime levels, stats and configuration were not
reconstructed. Its disposition remains
`RUNTIME_STATE_INSUFFICIENT_FOR_POLICY_VERDICT`; no move-scoring policy change
was made.

### M-009 scope-wrapper disposition

`python3 scripts/check_hidden_item_sparkle.py` ran and correctly failed closed
at its historical allowed-file boundary. It named these 11 later #520/#523
settings and replacement files:

`include/new/ai_opponent_replacement.h`, `include/new/settings.h`,
`scripts/tests/audit_opponent_replacement.py`,
`scripts/tests/audit_settings_defaults.py`,
`scripts/tests/opponent_replacement_host.c`,
`scripts/tests/run_replacement_safety_tests.py`,
`scripts/tests/run_settings_defaults_tests.py`,
`scripts/tests/settings_defaults_host.c`, `src/option_menu.c`, `src/save.c`,
and `src/settings.c`.

The M-009 wrapper was not edited or broadened. Its existing source ownership,
rejection, scanner-host and census functions were invoked with an in-memory
scope filter limited to those exact non-M-009 paths; the source/rejection/
host/census checks passed. No tracked M-009 source was modified.

## ARM, build and ABI disposition

`ARM_RECHECK_UNAVAILABLE_ENVIRONMENT`: `arm-none-eabi-gcc` is not available in
this session. Therefore no new ARM syntax/object, undefined-symbol, BPRE
binding or direct relocatable-link result is claimed. A native syntax-only
check of `src/battle_controller_opponent.c` passed at the merged pin, with
three existing pointer-cast warnings at unchanged controller lines 672, 742
and 749.

`FULL_SOURCE_BUILD_NOT_RUN_TOOLCHAIN_UNAVAILABLE`: the already-approved
`arm-none-eabi-gcc`, `wav2agb` and `mid2agb` tools are unavailable. No tools
were installed or downloaded and no build, ROM or runtime substitute was
used.

The accepted #523 repair changes only the controller, replacement helper,
host/audit tests and sanitized component evidence. No save fields, ABI
declarations, persistent structure fields or assembly hooks changed. The host
save-delta witness remains zero; no SaveBlock migration/expansion, DPE ABI or
randomizer table/repoint change is introduced. No fresh target object or
runtime-equivalence claim is made.

## Control plane, safety and limits

- Project `FireRed Gen 9 Randomizer — Pilot Finish`: #523 = `P0 / Integration /
  Done`; #524 = `P0 / Integration / Doing`; #498 = `P0 / Runtime Acceptance /
  Blocked`; #520/#521 remain Done; #499/#500/#501 remain unchanged.
- Required #498 rebaseline:
  [issuecomment-5821011661](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498#issuecomment-5821011661).
- The bounded-branch safety check passed. CFRU worktree is clean and recursive
  Workspace pins show only the authorized CFRU Gitlink at the target revision.
- `git diff --check` passed for the CFRU accepted-head-to-merge range. Workspace
  diff and final clean state are recorded in the #524 evidence return.

No ROM, save, emulator state, generated build, tool binary, screenshot, private
path, `.env`, token, key, secret or raw private log was accessed or copied. No
emulator/runtime, Randomizer R2, BizHawk/Tracker, Expert/Omniscient, missing
Gen-9 mechanics, Hospitality/M-011, upstream PR or merge work was performed.
`UPSTREAM_CONTRIBUTION = DEFERRED`.

The earlier R1 run remains revision-bound. `ROM_PROFILE_READY` remains blocked
until a fresh affected R1 rerun is completed and accepted after this Workspace
pin is user-merged and CONTROL-verified.
