# CFRU Ironmon Smart Workspace integration — merged-pin evidence

Date: 2026-09-21

Contract: Workspace Issue [#518](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/518)

Target: `WORKSPACE_CFRU_IRONMON_SMART_PIN_READY`

Evidence classification: **CONFIRMED CURRENT STATE** for the exact revisions,
source checks, host checks, Gitlink proof, and safety checks recorded here.
`ARM_RECHECK_UNAVAILABLE_ENVIRONMENT` and
`FULL_SOURCE_BUILD_NOT_RUN_TOOLCHAIN_UNAVAILABLE` are explicit environment
limitations. Runtime gameplay, settings/defaults, `ROM_PROFILE_READY`,
Randomizer R2, BizHawk, Tracker, and final freeze remain unclaimed.

## Revision identity

| Item | Exact value |
|---|---|
| Workspace base (`main`) | `20fac580a3dcf23cdaa2f3665c1d734e8ec32666` |
| Workspace branch | `integration/518-cfru-ironmon-smart-pin` |
| Final Workspace commit | The commit containing this document; its exact SHA is returned in the PR and sanitized #518 handoff because a commit cannot contain its own SHA. |
| Old CFRU Gitlink | `dfcfb9901ea725c6856a1aca6a5a6faf62f0bcbd` |
| Accepted CFRU #517 source head | `87c1a4d5eba05eab5125205851e53b0ab7bf4568` |
| New CFRU Gitlink / merged pin | `56525d781a21a835ac857ca8e5830e081e319a68` |
| CFRU target branch | `compat/firered-gen9-randomizer` |

The merged pin is one commit ahead of and zero commits behind the accepted
source head (`git rev-list --left-right --count` = `0 1`). The range contains
one merge commit. Its parents are `dfcfb990...` and `87c1a4d5...`, and
`git diff --name-status 87c1a4d5... 56525d78...` produced no paths: the
accepted source head and merge tree have zero file differences.

At the read-only `main` preflight, the root status showed only the expected
CFRU submodule checkout difference: the index recorded `dfcfb990...` while the
clean CFRU worktree was at the accepted #517 source head `87c1a4d5...`. No
reset or clean operation was performed. The bounded branch then checked out
the merged pin and staged only the authorized Gitlink.

## Gitlink scope

| Component | Base pin | Final pin | Result |
|---|---|---|---|
| CFRU Expansion | `dfcfb9901ea725c6856a1aca6a5a6faf62f0bcbd` | `56525d781a21a835ac857ca8e5830e081e319a68` | **CHANGED — authorized** |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | unchanged |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` | unchanged |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` | `c450ecaee2d8131a2789bb656e3be792a93712fb` | unchanged |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | unchanged |

The intended Workspace change set is exactly:

1. `02_external/CFRU-expansion` — mode `160000`, old pin to new pin;
2. `docs/testing/cfru-ironmon-smart-workspace-integration-2026-09-21.md` —
   this sanitized evidence document.

No other Gitlink, source file, canonical status document, or protected path is
changed.

## Exact merged-pin source and host gates

All CFRU commands below ran from the checked-out Gitlink at exact
`56525d781a21a835ac857ca8e5830e081e319a68` with a clean component worktree.

| Gate | Command / result |
|---|---|
| Standard source and production suite | `python3 scripts/tests/run_standard_ai_tests.py` — **PASS** |
| Ironmon pure C parity and production suite | `python3 scripts/tests/run_ironmon_ai_tests.py` — **PASS** |
| Workspace accepted AI host suite | `python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'` — **98 tests, PASS** |
| Coherent learnsets/source ownership | `python3 scripts/check_coherent_learnsets.py` — **PASS**; 144,000 initial-moveset cases, 820 exact replacements, 2 new form tables, 7 rebindings, 27 reserved sentinel bindings, and rejection cases |
| M-009 source/host/rejection/census | `python3 scripts/check_hidden_item_sparkle.py` — **PASS**; compiled scanner, source ownership, 8 invalid candidates rejected, 426 Cyan/NatDex maps and 425 pret maps, maximum 36 BG events in each census |
| M-013/Premier | `python3 scripts/check_premier_bonus.py` — **PASS**; 11,110 ball cases plus threshold/capacity, single-reward, failure, and non-ball controls |
| Renewable hidden items | `python3 scripts/check_renewable_hidden_items.py` — **PASS** |

The Standard/Ironmon source suites reproduced the accepted invariants at the
merged tree:

- Ironmon v3 parity: **63/63**; mandatory tags: **58/58**;
- accepted v1/v2/v3 digests unchanged:
  `71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7`,
  `227ecebc2b937671cc4f2fbab1694abf1b7c186f7e455ed7daf22014b62d0a85`, and
  `0a637d0bc42cb2e37701bbfa33677ae95c878b1f9a67ec55a60e15a4fbdb85d7`;
- repaired +12/+8 sequence: **491 admitted / 533 rejected**, zero
  below-threshold selections, zero invalid selections, zero replay mismatches;
- equal-four counts: **245/256/262/261**; +20/+16 ordering and singleton
  zero-draw checks **PASS**;
- Ironmon production twins: **1,024 / 0 mismatches**;
- Standard production twins: **4,096 / 0 mismatches**;
- Badge-ownership twins: **16 / 0 mismatches**;
- full-stat Badge Defense/SpDef oracle: **663,000 / 663,000**;
- explicit base 100 / level 50 / stage 6 possible Badge Defense:
  **167 -> 183**;
- sequencing, faint/recovery, hazard and response, forced replacement, Trick
  Room/order/modifier, setup threshold/order mismatch, repeat/loop, public
  move-count/history, unsupported-effect fail-closed, Standard/Legacy and
  excluded-mode isolation witnesses: **PASS**;
- `StandardMechanicsInput=34`, `DamageEnvelope=16`;
- no save/persistent delta; no unsupported runtime helper was observed in the
  accepted source-head ARM evidence described below.

The host/source results are revision-bound evidence. They do not certify a ROM
build, emulator behavior, or gameplay strength.

## ABI, layout, and object evidence

The merged tree is file-identical to the accepted #517 source head, so the
accepted source-head structural evidence remains applicable to the same tree:

- `BattlePokemon=0x58`, `BattleMove=0x0C`;
- host harness `BattleStruct=0x208` is **host-only**;
- target ARM compile-time layout assertion is `BattleStruct=0x200`;
- host-reported `IronmonCandidate=196`, `IronmonObservation=1836`,
  `IronmonResult=304`, `IronmonResponse=8`, `IronmonBranch=16`, and Ironmon
  AI fields `52`;
- aligned `NewBattleStruct` delta `56` and save delta `0`;
- no Trainer/Pokemon/BattleMove layout, DPE ABI, randomizer-owned table/layout,
  ROM repoint, save, or persistent-storage change is introduced by this
  Workspace Gitlink update.

## ARM/object-runtime gate

`command -v arm-none-eabi-gcc` did not resolve in this session. Therefore the
exact merged-pin ARM rerun was not executed and is recorded as:

`ARM_RECHECK_UNAVAILABLE_ENVIRONMENT`

Per the contract, no fresh ARM PASS is fabricated. The accepted #517 source
head evidence is preserved: approved devkitARM 16.1.0 previously passed ARM
syntax for 14 changed/integration C files, production-CFLAGS temporary objects,
`nm -u` helper/BPRE binding, direct relocatable `ld -r` closure, the target
`BattleStruct=0x200` assertion, and no unsupported compiler runtime helpers.
The verified zero-file-difference merge ancestry above shows that the merged
tree contains the same source files; final merged-pin ARM execution, final
object sizes, and static-stack figures remain unrefreshed in this environment.

## Full source build

`FULL_SOURCE_BUILD_NOT_RUN_TOOLCHAIN_UNAVAILABLE`

The complete approved source-build toolchain was not available: `wav2agb` and
`mid2agb` were missing, and the ARM compiler/binutils lookup was unavailable in
this session. `python3 scripts/build.py` and `scripts/make.py` were not run.
No missing tool was installed or downloaded, and no build cache or generated
artifact was used.

## Safety and non-claims

- `git diff --check`: **PASS**;
- `python3 07_scripts/bootstrap/check_git_safety.py` on the bounded branch:
  **PASS**;
- staged raw Gitlink diff: exactly one mode-`160000` entry, CFRU only;
- final handoff must show a clean Workspace and CFRU submodule worktree;
- no ROM, save, emulator state, generated build, emulator, runtime insertion,
  tool binary, private path, `.env`, token, key, secret, screenshot, or raw
  binary was accessed or copied;
- no settings/default change, Expert/Omniscient work, Randomizer R2, #499/#500,
  upstream PR, or merge was performed; `UPSTREAM_CONTRIBUTION = DEFERRED`.

This integration does not claim `ROM_PROFILE_READY`, runtime gameplay
acceptance, Standard as the New Game default, Ironmon settings activation,
full source-build PASS, universal Gen-1–9 mechanics parity, BizHawk readiness,
Tracker readiness, release/support status, or final freeze.

The required sanitized #498 rebaseline comment, Project metadata verification,
Workspace PR number, final commit SHA, and post-commit clean-worktree proof are
returned in the live #518 handoff after those external control-plane actions
complete.
