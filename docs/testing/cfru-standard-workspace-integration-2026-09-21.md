# CFRU Standard AI Workspace integration evidence

Date: 2026-09-21. Contract: Workspace Issue #513. Result:
**`WORKSPACE_CFRU_STANDARD_PIN_READY`**, subject to review and user merge of the
Workspace PR.

## Revision identity and scope

| Item | Value |
|---|---|
| Workspace source basis | `bcc8023ceb8c725dffe04bc6cbe623f91f5744ab` |
| Workspace branch | `integration/513-cfru-standard-pin` |
| Final Workspace commit | The commit containing this evidence file; its exact SHA is recorded in the Workspace PR and the sanitized #513 evidence comment after creation. A commit cannot contain its own SHA. |
| Old CFRU Gitlink | `8bc8c38210ddba0b05c933dbda06cb4539254c7a` |
| New CFRU Gitlink | `dfcfb9901ea725c6856a1aca6a5a6faf62f0bcbd` |
| Accepted CFRU source head | `c8addb96a651d6f2534d643d0fa3e49c474f6cc4` |
| CFRU target branch | `compat/firered-gen9-randomizer` |
| DPE, unchanged | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX, unchanged | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` |
| Ironmon Tracker, unchanged | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| NatDexExtension, unchanged | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |

Evidence classification: the revision, Gitlink, source-test, host-test, ARM,
and source-gate results below are **CONFIRMED CURRENT STATE** for the exact
revisions listed above. Runtime gameplay, settings/defaults, later AI profiles,
Randomizer acceptance, and final freeze remain unperformed future gates.

The exact Workspace change set is limited to:

- `02_external/CFRU-expansion` (mode-160000 Gitlink only);
- `docs/testing/cfru-standard-workspace-integration-2026-09-21.md`.

No other Component file or Gitlink is changed.

## Pre-integration evidence

Before the authorized Gitlink move:

- branch: `integration/513-cfru-standard-pin`;
- Workspace `HEAD`: `bcc8023ceb8c725dffe04bc6cbe623f91f5744ab`;
- `git status --short`: clean;
- `python3 07_scripts/bootstrap/check_git_safety.py`: PASS on the bounded
  non-`main` branch;
- recursive submodule status had no `+`, `-`, or dirty marker;
- CFRU: `8bc8c38210ddba0b05c933dbda06cb4539254c7a`;
- DPE: `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`;
- UPR-FVX: `0e3be63e94e34215cc35308d64e8db15e9a3c48c`;
- Ironmon Tracker: `c450ecaee2d8131a2789bb656e3be792a93712fb`;
- NatDexExtension: `a94b8844800308248bb5090b6c36c8b2d7e5d7b9`.

The initial read-only `main` preflight also verified that local `main`, local
`main`'s commit, and `origin/main` all resolved to the exact required basis and
that `git status --short` was clean. The explicit `--allow-main` safety check
passed before the bounded branch was created.

## Component merge and Gitlink proof

Live GitHub and Git evidence independently established:

- CFRU PR #50 is merged; its merge commit is
  `dfcfb9901ea725c6856a1aca6a5a6faf62f0bcbd`;
- `refs/heads/compat/firered-gen9-randomizer` resolves to that exact commit;
- accepted source head `c8addb96a651d6f2534d643d0fa3e49c474f6cc4`
  is an ancestor and the second parent of the merge commit;
- `git rev-list --left-right --count c8addb96...dfcfb990` returned `0 1`;
- the accepted-head-to-merge range contains exactly one commit and exactly one
  merge commit;
- `git diff --name-status c8addb96 dfcfb990` returned no paths: the accepted
  source head and merge commit have identical file trees.

After checkout, the raw Workspace diff contains exactly one changed mode-160000
entry and it is:

```text
02_external/CFRU-expansion
8bc8c38210ddba0b05c933dbda06cb4539254c7a -> dfcfb9901ea725c6856a1aca6a5a6faf62f0bcbd
```

Direct `git ls-tree` and recursive submodule checks retain the exact DPE,
UPR-FVX, Ironmon Tracker, and NatDexExtension revisions in the table above.
No other Gitlink moved. No protected path or artifact changed.

## Exact merged-pin tests

All CFRU commands below ran from `02_external/CFRU-expansion` at exact `HEAD`
`dfcfb9901ea725c6856a1aca6a5a6faf62f0bcbd`, with a clean component worktree.

### Standard source and adapter suite

```sh
python3 scripts/tests/run_standard_ai_tests.py
```

Result: **PASS**.

The source-owned pure C policy parity and production adapter checks passed,
including KO dominance; signed utility and int32 saturation; epsilon/RNG and
singleton no-draw behavior; Speed, setup, status, recovery, Accuracy, and
UNKNOWN-damage witnesses; emergency/forced/switch-loop behavior; Legacy
isolation; and excluded special-mode isolation. The bounded-saturation host
oracle asserted all 17,496 combinations.

Production fairness evidence reproduced at the merged pin:

- 4,096 hidden/private/submitted-action/future-RNG twin pairs, zero mismatches;
- public reveal transition PASS;
- 98,304 independent damage-envelope IV/EV/nature/roll cases PASS;
- maximum arithmetic product plus 10 fail-closed boundary witnesses PASS;
- exact entry costs, entry-KO handling, forced replacement, and singleton RNG
  witnesses PASS.

### Workspace host policy suite

```sh
python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'
```

Result: **PASS — 71 tests in 0.774 seconds; 0 failures, 0 errors**.

### Existing source regressions

```sh
python3 scripts/check_coherent_learnsets.py
```

Result: **PASS** — 144,000 actual initial-moveset cases, 820 exact table
replacements, 27 reserved sentinel bindings, and the ownership/rejection cases.

```sh
python3 scripts/check_hidden_item_sparkle.py
```

Result: **PASS** — M-009 exact frame/source ownership, compiled scanner host
checks, and 8 in-memory rejection cases. The local public reference checkouts
were available, so the external map census also ran and passed: 426 Cyan/NatDex
maps and 425 pret maps, with a maximum of 36 BG events in each census.

```sh
python3 scripts/check_premier_bonus.py
```

Result: **PASS** — M-013 real callback/source-host checks, 11,110 ball cases,
capacity and threshold coverage, single-reward behavior, and non-ball controls.

```sh
python3 scripts/check_renewable_hidden_items.py
```

Result: **PASS** — renewable hidden-item source-table contract.

## ARM syntax and object/runtime-helper closure

The already-approved devkitARM compiler and binutils were available at the
established devkitPro location. No tool was installed or downloaded.

```sh
python3 scripts/tests/run_standard_ai_tests.py \
  --arm-cc /opt/devkitpro/devkitARM/bin/arm-none-eabi-gcc
```

Result: **PASS** with devkitARM GCC 16.1.0 at exact revision
`dfcfb9901ea725c6856a1aca6a5a6faf62f0bcbd`, `dirty=False`.

- ARM syntax passed for all 11 C files changed relative to old CFRU basis
  `8bc8c38210ddba0b05c933dbda06cb4539254c7a`;
- exact production `CFLAGS` compiled temporary policy, mechanics, and adapter
  objects;
- `nm -u` inspection found only the existing bound 32-bit division/remainder
  wrappers plus ordinary engine/BPRE dependencies;
- the unchanged `thumb_compiler_helper.s` dependencies were verified against
  `BPRE.ld`;
- direct `arm-none-eabi-ld -r` runtime-symbol closure passed;
- no unsupported helper remained, including `__aeabi_lmul`,
  `__aeabi_uldivmod`, `__udivdi3`, `__divdi3`, `__moddi3`, `__umoddi3`, or
  `__muldi3`;
- all temporary objects were deleted by the test runner.

The only compiler diagnostics were the two pre-existing unused-local warnings
for `x2` and `y2` in `src/battle_anims.c`.

## Full source-build disposition

`FULL_SOURCE_BUILD_NOT_RUN_TOOLCHAIN_UNAVAILABLE`

The environment was checked. devkitARM/binutils, `grit`, and `make` are
available; the complete approved source toolchain is not. Missing tools:

- `wav2agb`;
- `mid2agb`.

Therefore `python3 scripts/build.py` was not run. No missing tool was installed
or downloaded, no generated build artifact was inspected or reused, and
`scripts/make.py` was not run. This is an explicit non-PASS for a future full
source-build/freeze gate; it does not override the source, host, ARM object, and
runtime-helper evidence above.

## ABI, layout, repoint, and memory disposition

The merged pin has zero file differences from accepted source head `c8addb96`;
therefore the #512 accepted source-layout disposition transfers exactly to the
merge tree and was rechecked by the merged-pin source/ARM suite.

- no Trainer, Pokemon, or BattleMove layout change;
- no DPE ABI or randomizer-owned table-layout change;
- no ROM table/repoint change;
- no save-layout or persistent-storage change and no save migration;
- no IWRAM addition;
- total battle-local Standard state is 240 bytes, including the accepted
  round-2 +4-byte sticky type-uncertainty delta;
- Standard candidate/observation/result sizes remain 52/472/192 bytes;
- mechanics input is 32 bytes and damage envelope is 16 bytes;
- battle allocation/zeroing remains the reset owner;
- bounded local scratch is non-recursive and dynamically allocates no memory.

Exact optimized target stack/cycle cost and gameplay behavior are not certified
by these source/object gates and remain later build/runtime evidence.

## Safety, limitations, and explicit non-claims

`git diff --cached --check`: **PASS**. The final Workspace safety check: **PASS**.
The staged raw diff contains exactly the authorized mode-160000 Gitlink update
and this evidence document. Recursive submodule review shows CFRU at the new
pin and every other component at its unchanged recorded pin. The exact final
commit and clean post-commit worktree confirmation are recorded in the PR and
sanitized #513 handoff because they necessarily occur after this file is
committed. None of these checks accesses a ROM or other protected artifact.

This integration does not claim:

- a full CFRU source-build PASS;
- runtime gameplay acceptance or final target performance;
- `ROM_PROFILE_READY` or final freeze;
- Standard as the New Game default;
- Ironmon Smart, Expert, or Omniscient Challenge implementation;
- Randomizer R2 authorization;
- BizHawk or Ironmon Tracker readiness;
- implementation of unsupported Gen-9 mechanics;
- release/support acceptance.

No ROM, save, emulator state, generated build, screenshot, private path,
`.env`, token, key, secret, or protected artifact was accessed or modified. No
runtime, emulator, ROM insertion, upstream contribution, force push, or merge
was performed. `UPSTREAM_CONTRIBUTION = DEFERRED`.
