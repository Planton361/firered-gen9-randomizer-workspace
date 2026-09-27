# CFRU Fair-AI Runtime Scratch Workspace Integration Evidence

Date: 2026-09-26. Contract: Workspace Issue [#533](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/533).

Submitted for CONTROL review as:

**`WORKSPACE_CFRU_FAIR_AI_RUNTIME_SCRATCH_PIN_READY`**

This result integrates the accepted CFRU PR #56 source tree. It does not
self-accept this Workspace integration, resume broad R1, or claim
`ROM_PROFILE_READY`.

## Revision identity

| Item | Value |
|---|---|
| Workspace base | `30f776cec15dd69eb542d25bf97e2d05998aa378` (`main`) |
| Workspace branch | `integration/cfru-fair-ai-runtime-scratch-pin` |
| Target | `main` |
| Final Workspace branch head | Recorded as the PR's exact `headRefOid` and in its description. A commit cannot embed its own object ID without changing that ID. |
| Old CFRU Gitlink | `b8e58508f2474db1702c5fa0429a24dc076f1abc` |
| New CFRU Gitlink | `d851256f2bb897042fbe865b4533e55fc7586ba9` |
| Accepted CFRU PR #56 head | `b4ce28485a97703a9345d45bd47361407334063d` |
| Merged CFRU pin | `d851256f2bb897042fbe865b4533e55fc7586ba9` |
| Accepted-head / merge tree | `a21628e2b0012ad7042e05f22bdfd36ece0473fa` |

### Accepted head to merge proof

At `02_external/CFRU-expansion`:

- Merge parents are exactly `b8e58508f2474db1702c5fa0429a24dc076f1abc`
  and accepted PR head `b4ce28485a97703a9345d45bd47361407334063d`.
- `git rev-list --count b4ce28485a97703a9345d45bd47361407334063d..d851256f2bb897042fbe865b4533e55fc7586ba9` returns `1`; that commit is the two-parent PR merge.
- `git diff --name-status` between accepted head and merge returns no paths.
- Both `^{tree}` values are exactly
  `a21628e2b0012ad7042e05f22bdfd36ece0473fa`.

The accepted source tree and merged pin are therefore tree-identical. The
workspace integration does not alter either CFRU commit.

## Workspace change boundary and component pins

The PR diff contains exactly these two Workspace paths:

1. `02_external/CFRU-expansion` — mode-160000 Gitlink update from
   `b8e58508f2474db1702c5fa0429a24dc076f1abc` to
   `d851256f2bb897042fbe865b4533e55fc7586ba9`.
2. `docs/testing/cfru-fair-ai-runtime-scratch-workspace-integration-2026-09-26.md` — this evidence.

All other component Gitlinks match the exact start basis:

| Component | Revision | Disposition |
|---|---|---|
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | Unchanged |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` | Unchanged |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` | Unchanged |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | Unchanged |

No DPE, UPR-FVX, Tracker, NatDexExtension, reference-component, or other
Workspace path is changed.

## Preserved #532 runtime evidence

**CONFIRMED USER-SUPPLIED, revision-bound runtime PASS:** The two independent
full mGBA cold starts were run on accepted CFRU PR #56 head
`b4ce28485a97703a9345d45bd47361407334063d`, with a fresh New Game, no
randomization, Ironmon Smart, and Charmander. Oak's-Lab Rival Squirtle
produced `Water Gun / Water Gun / Water Gun` on each cold start.

The merged pin `d851256f2bb897042fbe865b4533e55fc7586ba9` has the same tree as
the runtime-tested accepted head. This integration records that source/tree
relationship; it does not claim a new private runtime execution at the merge
SHA. The earlier warm-session Tail Whip observation remains superseded as
mGBA session contamination, per #532's final CONTROL disposition.

## Exact-pin CFRU gates

All seven required commands were run from the CFRU submodule at exact `HEAD`
`d851256f2bb897042fbe865b4533e55fc7586ba9`; each exited zero.

| Command | Result |
|---|---|
| `python3 scripts/tests/run_standard_ai_tests.py` | **PASS** — Standard twins `4096/0`, Ironmon twins `1024/0`, Badge twins `16/0`, Badge oracle `663000/663000`, damage oracle `98304`; source/layout/save and Legacy Smart isolation witnesses pass. |
| `python3 scripts/tests/run_ironmon_ai_tests.py` | **PASS** — Ironmon parity `63/63`, mandatory coverage tags `58/58`; accepted v1/v2/v3 digests unchanged. |
| `python3 scripts/tests/run_settings_defaults_tests.py` | **PASS** — raw settings compatibility; Fresh New Game Standard raw `7`; Ironmon Smart preset raw `8`; unknown/legacy raw preservation. |
| `python3 scripts/tests/run_replacement_safety_tests.py` | **PASS** — safe 2-/3-mon replacements, ownership/range, invalid candidate handling, final-faint stop and voluntary target identity. |
| `python3 scripts/tests/run_ai_runtime_quality_tests.py` | **PASS** — `991`-move census (`721` damaging, `270` status; D0/D1/D2/D3 `49/117/110/445`), all five quality counters zero, production/Workspace-host differential `10/10`, zero mismatches. |
| `python3 scripts/tests/run_ai_controller_fallback_tests.py` | **PASS** — policy result/fallback/controller parity, Oak reveal routing, full action → pending → move lifecycle, capped-Defense witness and diagnostic class witnesses. |
| `python3 scripts/tests/audit_ai_damage_overrides.py` | **PASS** — `131` named damage overrides audited. |

Accepted policy fixture digests remain:

- v1 `uniform_legal`: `71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7`.
- v2 `standard`: `227ecebc2b937671cc4f2fbab1694abf1b7c186f7e455ed7daf22014b62d0a85`.
- v3 `ironmon_smart`: `0a637d0bc42cb2e37701bbfa33677ae95c878b1f9a67ec55a60e15a4fbdb85d7`.

The #532 production-equivalent lifecycle witnesses still select Water Gun on
fresh revealed Oak state and a productive Tackle at minimum Defense for
Standard and Ironmon Smart; neither enters bounded emergency fallback. Injected
policy/handoff failures still exercise the separate #529 bounded emergency
witness. Legacy Smart routing, policy RNG isolation, settings compatibility,
Replacement Safety, the sole all-futile `NO_PRODUCTIVE_ACTION` fallback and
save delta `0` remain intact. No scoring, policy RNG, fallback, or Legacy Smart
semantics were retuned by this Workspace pin.

## Writable-state, storage, hook, and layout evidence

At the exact merged pin, these available #532 source/host gates passed:

- `python3 scripts/tests/audit_ai_writable_state.py` — **PASS**. Ironmon
  observation/result and diagnostic mutable state are `gNewBS` tail fields;
  the `EWRAM_DATA` static scratch and static diagnostic globals are absent.
  The source audit confirms the existing battle-lifetime allocation is
  `Calloc(sizeof(struct NewBattleStruct))`, freed at battle end, within the
  managed heap contract `0x02000000..0x0201C000`; pointer slot `gNewBS` remains
  `0x0203E038`. No fixed EWRAM gap, ROM payload, save block, or persistent
  scratch was added.
- `python3 scripts/tests/audit_trainer_ai_storage.py` — **PASS**. Profile raw
  `7/8`, expanded-var index `0x15B`, address `0x0203B62A`, production pointer,
  New Game clear/default order, and tracked source write/clear audit pass.
- `python3 scripts/tests/audit_runtime_dispatch_closure.py` — **PASS** for
  source/inserter/Thumb closure. Five runtime hook symbols, sites, parser,
  Thumb encoding, 26 exclusion flags and diagnostic preprocessing isolation
  pass. Both diagnostic switches are disabled by default and absent from
  release preprocessing.
- `run_standard_ai_tests.py` host layout witnesses — **PASS**. Host-harness
  `NewBattleStruct` sizes are `0x1468` release and `0x1470` diagnostic; both
  keep save delta `0` (host sizes are not target ARM ABI values).

The accepted #532 evidence at the tree-identical head records target ARM
layout: release `NewBattleStruct=0x143C`, observation `+0xBE0/0x72C`, result
`+0x130C/0x130`; capped diagnostic `0x1448`, with diagnostic state
`+0x143C/0xC`. Its ARM source-object and layout assertions passed on that
accepted tree. They were not recompiled in this worker because the approved
ARM tools are absent.

At this exact pin, linked-object/objcopy writable-state closure and linked
insertion-symbol resolution report **NOT RUN** in this worker: they require an
approved complete ARM-linked object. No full linked result is inferred from
the source/host audits or from #532's synthetic linker self-test.

## Workspace policy, data-reference, and source-ownership gates

| Gate | Result |
|---|---|
| `07_scripts/ai_policy/cli.py validate` | **PASS** — 122 fixtures, schemas v1/v2/v3. |
| Standard policy `run`, `replay`, `summarize` | **PASS** — 30/30 oracle and near-best agreement; zero deterministic, hidden-information, submitted-action, future-RNG twin mismatches or quality violations. |
| Ironmon Smart policy `run`, `replay`, `summarize` | **PASS** — 63/63 oracle and near-best agreement; zero twin mismatches or quality violations. |
| `python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'` | **PASS** — 98 tests. |
| CFRU `scripts/check_premier_bonus.py` | **PASS** — 11,110 purchase cases and capacity/failure/non-ball controls. |
| CFRU `scripts/check_renewable_hidden_items.py` | **PASS** — accepted source-table contract. |
| CFRU `scripts/insert.py --check-map-object-overlays` | **PASS** — existing map overlay contracts. This mode reads no ROM. |

The historical `check_coherent_learnsets.py` and its dependent support-only
`check_hidden_item_sparkle.py` fail closed against their older engine/config
baseline because the accepted #532 change adds exactly two **commented-out**
diagnostic switches to `src/config.h`. Those defaults are disabled; the
historical scripts were not changed or weakened. The exact two-line config
delta was isolated in memory, after which coherent learnset provenance/table
hash validation, 144,000 actual initial-moveset host cases, rejection
mutations, the M-009 compiled scanner host, and the 426 Cyan / 425 pret
reference-map census all passed. The M-009 frame/scanner/ownership source set
and Premier callback are unchanged between the old CFRU pin and #56 merge.

## ARM, full build, ABI, and save disposition

`ARM_RECHECK_UNAVAILABLE_ENVIRONMENT`: this worker has none of the approved
`arm-none-eabi-gcc`, `arm-none-eabi-as`, `arm-none-eabi-ld`, `arm-none-eabi-nm`,
`arm-none-eabi-objdump`, or `arm-none-eabi-objcopy` tools.

`FULL_SOURCE_BUILD_NOT_RUN_TOOLCHAIN_UNAVAILABLE`: `python3 scripts/build.py`
was not run. The complete approved build chain also lacks `wav2agb` and
`mid2agb`; no tools were installed or downloaded. No full target link,
objcopy payload, or insertion binary is claimed. The ROM-free map-overlay
check above does not access ROM input.

The managed battle-lifetime `NewBattleStruct` grows only for #532's tail-owned
runtime scratch and compile-gated diagnostic state. No save schema, save
expansion, Trainer/Pokemon/BattleMove layout, DPE ABI, randomizer table, or
fixed-address owner changed. Host/source save delta remains `0`; fresh target
ARM ABI/link confirmation is unavailable in this worker.

## R1 routing and completion boundary

Live #498 remains **Blocked** at Phase R1 pending this separate Workspace
integration and post-merge CONTROL verification. Once the user merges this PR
and CONTROL verifies the Workspace merge/pins, CONTROL may route one fresh
exact-basis smoke before broader R1 resumes. This integration does not claim
that run, does not self-accept, and does not claim `ROM_PROFILE_READY`.

No AI tuning, Tail Whip/Water Gun product special-case, Legacy Smart redesign,
DPE/UPR/Tracker/NatDex change, other Gitlink, R2/BizHawk/Tracker scope,
upstream PR, merge, or history rewrite is included. `UPSTREAM_CONTRIBUTION =
DEFERRED`.

## Final disposition

**`WORKSPACE_CFRU_FAIR_AI_RUNTIME_SCRATCH_PIN_READY`** — submitted for CONTROL
review; not self-accepted and not merged.
