# CFRU settings/defaults Workspace integration — merged-pin evidence

Date: 2026-09-22

Contract: Workspace Issue [#521](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/521)

Target: `WORKSPACE_CFRU_SETTINGS_DEFAULTS_PIN_READY`

Evidence classification: **CONFIRMED CURRENT STATE** for the exact revisions,
source/host checks, ARM/object checks, Gitlink proof, and safety checks recorded
here. This is source and integration evidence only. Runtime gameplay,
`ROM_PROFILE_READY`, Randomizer R2, BizHawk, Tracker, Expert/Omniscient work,
and final freeze remain unclaimed.

## Revision identity and Gitlink scope

| Item | Exact value |
|---|---|
| Workspace base (`main`) | `ef0455228461cedfc190e895cf12b48579499bcf` |
| Workspace branch | `integration/cfru-settings-defaults-pin` |
| Final Workspace commit | The commit containing this document; its exact SHA is returned in the PR and sanitized #521 handoff because a commit cannot contain its own SHA. |
| Old CFRU Gitlink | `56525d781a21a835ac857ca8e5830e081e319a68` |
| Accepted #520 CFRU source head | `cb10bb682ff8b5ddab962cc74bdceb44756e78b7` |
| New CFRU Gitlink / merged pin | `3c2f38140ed07991a04ae63ff1108ff2f25547a6` |
| CFRU target branch | `compat/firered-gen9-randomizer` |

`git rev-list --left-right --count cb10bb68...3c2f381` returned `0 1`.
The one added commit is merge `3c2f381` with parents `56525d78` and
`cb10bb68`; `git diff --name-status cb10bb68 3c2f381` returned no paths.
Thus the accepted #520 head and the merged integration tree have zero file
differences.

| Component | Base pin | Final pin | Result |
|---|---|---|---|
| CFRU Expansion | `56525d781a21a835ac857ca8e5830e081e319a68` | `3c2f38140ed07991a04ae63ff1108ff2f25547a6` | **CHANGED — explicitly authorized** |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | same | unchanged |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` | same | unchanged |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` | same | unchanged |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | same | unchanged |

The intended Workspace change set is exactly:

1. `02_external/CFRU-expansion` — mode `160000`, `56525d78...` to `3c2f381...`;
2. `docs/testing/cfru-settings-defaults-workspace-integration-2026-09-22.md` — this sanitized evidence document.

No other Gitlink, source file, canonical status document, or protected path is
changed.

## Exact merged-pin source and host gates

All CFRU checks ran from a clean component worktree at exact
`3c2f38140ed07991a04ae63ff1108ff2f25547a6`.

| Gate | Result |
|---|---|
| `python3 scripts/tests/run_settings_defaults_tests.py` | **PASS** |
| `python3 scripts/tests/run_standard_ai_tests.py` | **PASS** |
| `python3 scripts/tests/run_ironmon_ai_tests.py` | **PASS** |
| Workspace AI host suite | **98 tests, PASS** |
| `python3 scripts/check_coherent_learnsets.py` | **PASS**: 144,000 cases, 820 replacements, 2 form tables, 7 rebindings, 27 sentinel bindings, rejection cases |
| M-013/Premier source-host gate | **PASS**: 11,110 ball cases plus controls |
| Renewable hidden-item source gate | **PASS** |
| M-009 compiled scanner host gate | **PASS** |
| M-009 reference-map census | **PASS**: 426 Cyan/NatDex and 425 pret maps; maximum 36 BG events |

The settings/defaults suite reproduced the required compatibility witnesses:

- Trainer AI raw `0..6` meanings are retained; raw `7` is Standard and raw
  `8` is Ironmon Smart; unsupported Trainer AI raws are preserved when
  untouched.
- Unknown Difficulty (`5`, `0xFFFF`), Trainer Scaling, and Wild Scaling
  (`2`, `0xFFFF`) values use bounded display values and survive untouched
  close, including the combined four-setting open/close witness.
- Fresh defaults are `Difficulty=4`, `Trainer Scaling=1`, `Wild=0`,
  `Trainer AI=7`; unrelated Vars remain unchanged.
- The source-owned Ironmon helper is `Difficulty=4`, `Trainer Scaling=1`,
  `Wild=0`, `Trainer AI=8`; unrelated rules remain unchanged.

Accepted policy and noninterference evidence remained unchanged:

- Standard production twins: **4,096 / 0 mismatches**.
- Ironmon production twins: **1,024 / 0 mismatches**; Badge-ownership twins:
  **16 / 0 mismatches**.
- Badge full-stat Defense/SpDef oracle: **663,000 / 663,000**.
- Ironmon C parity: **63 / 63**; mandatory tags: **58 / 58**.
- Digests: v1 `71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7`,
  Standard v2 `227ecebc2b937671cc4f2fbab1694abf1b7c186f7e455ed7daf22014b62d0a85`,
  Ironmon v3 `0a637d0bc42cb2e37701bbfa33677ae95c878b1f9a67ec55a60e15a4fbdb85d7`.

### M-009 scope-wrapper disposition

`python3 scripts/check_hidden_item_sparkle.py` correctly fail-closed at its
historical source-contract boundary. Its exact rejection named the seven
accepted #520 settings/defaults files:
`include/new/settings.h`, `src/settings.c`, `src/option_menu.c`, `src/save.c`,
`scripts/tests/audit_settings_defaults.py`,
`scripts/tests/run_settings_defaults_tests.py`, and
`scripts/tests/settings_defaults_host.c`.

The wrapper was not changed to admit unrelated later work. The independently
applicable actual-scanner host gate and both fixed-reference map censuses above
passed. The zero-file-difference #520 accepted-head-to-merge proof preserves
the reviewed source basis; no M-009 source file is changed by this Workspace
Gitlink integration.

## ARM, ABI, and source-build disposition

The already-approved devkitARM 16.1.0 compiler at
`/opt/devkitpro/devkitARM/bin/arm-none-eabi-gcc` was available and used at the
exact merged pin with `dirty=False`.

- The repository ARM runner passed syntax for 18 changed/integration C files,
  including `src/settings.c`, `src/option_menu.c`, and `src/save.c`.
- Production-CFLAGS temporary objects, undefined-symbol inspection, helper
  assembly and BPRE binding, direct `ld -r` closure, static-stack reporting,
  and supported compiler-runtime-helper checks passed for the Standard/Ironmon
  integration path; unsupported helpers: **NONE**.
- Focused production-CFLAGS Settings/Defaults objects passed: `settings.c`
  280 bytes, `option_menu.c` 3307 bytes, `save.c` 2000 bytes. Their direct
  relocatable closure passed; expected unresolved engine symbols include
  `VarGet`, `VarSet`, `Memset`, and `Memcpy`, all present in `BPRE.ld`.
- Layout witnesses retain target `BattleStruct=0x200`, host-only
  `BattleStruct=0x208`, existing `BattlePokemon=0x58`, `BattleMove=0x0C`, and
  save delta `0`. No SaveBlock expansion/migration, Trainer/Pokemon/
  BattleMove/NewBattleStruct layout change, DPE ABI change, or randomizer
  table/repoint change is introduced.
- Temporary ARM objects were deleted after the checks.

`FULL_SOURCE_BUILD_NOT_RUN_TOOLCHAIN_UNAVAILABLE`

`wav2agb` and `mid2agb` were unavailable. No full source build, ROM tooling,
generated/private build, cache bypass, emulator, or runtime work was run.

## Control-plane, safety, and limits

- `git diff --check`: **PASS**.
- `python3 07_scripts/bootstrap/check_git_safety.py` on the bounded branch:
  **PASS**.
- Raw Gitlink review shows exactly one mode-`160000` component entry changed.
- Project `FireRed Gen 9 Randomizer — Pilot Finish`: #520 is `P0 / Integration
  / Done`; #521 is `P0 / Integration / Doing`; #498 remains Blocked; #499,
  #500, and #501 remain unchanged.
- Required sanitized #498 rebaseline comment:
  [issuecomment-5777936804](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498#issuecomment-5777936804).

No ROM, save, emulator state, generated build, tool binary, private path,
`.env`, token, key, secret, screenshot, or raw binary was accessed or copied.
No runtime acceptance, Randomizer R2, BizHawk/Tracker work, Expert/Omniscient
policy, missing Gen-9 mechanics, Hospitality/M-011 work, upstream PR, or merge
was performed. `UPSTREAM_CONTRIBUTION = DEFERRED`.
