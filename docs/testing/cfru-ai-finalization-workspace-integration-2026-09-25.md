# CFRU AI Finalization Workspace Integration — 2026-09-25

Evidence classification: **CONFIRMED CURRENT STATE** for the source, host and repository checks below. This is an integration evidence return for CONTROL review. It does not self-accept `WORKSPACE_CFRU_AI_FINALIZATION_PIN_READY` and does not claim ROM/runtime acceptance.

## Workspace and CFRU identity

- Workspace repository: `Planton361/firered-gen9-randomizer-workspace`.
- Exact Workspace base and `main` SHA: `f817b37261228f4013a9106cc9608e9f0042bfb8`.
- Branch: `integration/cfru-ai-finalization-pin`; base target: `main`.
- The branch was created from the exact base SHA above. The current final branch head OID is recorded in the #527 evidence handoff and the Workspace PR head; this report is part of that same head and cannot contain its own commit SHA.
- CFRU old Workspace Gitlink: `423f96f0dcd501a64c2327d726a98f1964937ac1`.
- CFRU accepted PR #54 head: `f0cf999a1f7277e02870044b605a3f31045a0141`.
- CFRU merged pin / new Gitlink: `fa83aae29818434cca6813be28f509b04c5dd68b`.
- Live `compat/firered-gen9-randomizer` branch and local detached CFRU checkout both resolve to `fa83aae29818434cca6813be28f509b04c5dd68b`.

### Accepted-head to merge proof

- GitHub compare `f0cf999a1f7277e02870044b605a3f31045a0141...fa83aae29818434cca6813be28f509b04c5dd68b`: `ahead_by=1`, `behind_by=0`, `total_commits=1`, changed file list empty.
- Merge commit `fa83aae29818434cca6813be28f509b04c5dd68b` has parents `423f96f0dcd501a64c2327d726a98f1964937ac1` and `f0cf999a1f7277e02870044b605a3f31045a0141`.
- Accepted head and merge commit have the identical tree SHA `edd68c0d26a3a9d5d90d5ff65b917a614231896e`.
- The accepted head is therefore preserved by exactly one CFRU merge commit, with zero source/file changes.

### Component pins

| Workspace path | Base and final Gitlink | Disposition |
|---|---|---|
| `02_external/CFRU-expansion` | `423f96f0dcd501a64c2327d726a98f1964937ac1` → `fa83aae29818434cca6813be28f509b04c5dd68b` | Explicitly authorized change |
| `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | Unchanged |
| `02_external/upr-fvx` | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` | Unchanged |
| `02_external/Ironmon-Tracker` | `c450ecaee2d8131a2789bb656e3be792a93712fb` | Unchanged |
| `02_external/NatDexExtension` | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | Unchanged |

At the Workspace base, direct mode-`160000` Gitlink inspection confirmed all five values in the table. The recursive submodule review after checkout showed the same four unchanged component pins and CFRU at the authorized new pin.

## Workspace diff boundary

The final PR is limited to these two paths:

1. `02_external/CFRU-expansion` — one mode-`160000` Gitlink update.
2. `docs/testing/cfru-ai-finalization-workspace-integration-2026-09-25.md` — this report.

No other Workspace path or component Gitlink is authorized or changed.

## Exact-pin CFRU gates

All six required CFRU commands ran from `02_external/CFRU-expansion` at `fa83aae29818434cca6813be28f509b04c5dd68b` and exited 0:

| Command | Result |
|---|---|
| `python3 scripts/tests/run_standard_ai_tests.py` | **PASS** — Standard production twins 4096 pairs / 0 mismatches; Ironmon production twins 1024 / 0; Badge twins 16 / 0; Badge oracle 663000 / 663000; damage-envelope oracle 98304 cases. Standard/Ironmon dispatch, hidden-state/submitted-action/future-RNG twins, replacement, battle-local layout and save-delta witnesses passed. Legacy Smart isolation passed. |
| `python3 scripts/tests/run_ironmon_ai_tests.py` | **PASS** — Ironmon parity 63 / 63; mandatory coverage tags 58 / 58; accepted v1/v2/v3 digests unchanged. |
| `python3 scripts/tests/run_settings_defaults_tests.py` | **PASS** — raw Trainer AI 0..8 mapping, legacy Auto and untouched unknown preservation; fresh defaults Difficulty/Trainer Scaling/Wild Scaling/AI = 4/1/0/7; Ironmon preset = 4/1/0/8; unrelated settings/rules unchanged. |
| `python3 scripts/tests/run_replacement_safety_tests.py` | **PASS** — Standard/Ironmon ownership/range checks, safe fallback, dead/empty/egg/current candidate rejection, repeated two-/three-mon replacement, final-faint stop and voluntary target identity. |
| `python3 scripts/tests/run_ai_runtime_quality_tests.py` | **PASS** — 991-move census, source witnesses, ten production-vs-Workspace-host differential states and runtime-quality counters. |
| `python3 scripts/tests/audit_ai_damage_overrides.py` | **PASS** — all 131 named damage-engine overrides audited. |

### Accepted identities and runtime-quality result

- Standard production adapter: 4096 pairs / 0 mismatches.
- Ironmon production adapter: 1024 pairs / 0 mismatches.
- Badge-ownership twins: 16 pairs / 0 mismatches; Badge oracle: 663000 / 663000.
- Damage-envelope oracle: 98304 cases.
- Ironmon policy parity: 63 / 63; mandatory tags: 58 / 58.
- Accepted digest identities remain unchanged:
  - v1 `uniform_legal`: `71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7`.
  - v2 `standard`: `227ecebc2b937671cc4f2fbab1694abf1b7c186f7e455ed7daf22014b62d0a85`.
  - v3 `ironmon_smart`: `0a637d0bc42cb2e37701bbfa33677ae95c878b1f9a67ec55a60e15a4fbdb85d7`.
- Production-vs-Workspace-host differential: 10 / 10 states PASS; 0 field, decision or RNG mismatches.
- Runtime-quality counters: illegal/no-effect with productive alternative **0**; missed robust KO **0**; third harmful same-family repeat **0**; below-epsilon selection **0**; unsupported selection below clearly superior supported alternative **0**.
- The sole fallback is one all-futile case: `NO_PRODUCTIVE_ACTION`.

### 991-move census and deterministic source witnesses

The deterministic census reads the pinned CFRU source move table; it is not ROM-derived.

| Census item | Count |
|---|---:|
| Total moves excluding `MOVE_NONE` | 991 |
| Damaging / status | 721 / 270 |
| D0 ordinary direct damage | 49 |
| D1 direct damage with bounded secondary | 117 |
| D2 priority/accuracy variants | 110 |
| D3 complex or unsupported/fail-closed | 445 |
| Fully evaluated / direct-damage-only / unsupported | 92 / 184 / 445 |

D0+D1+D2 cover 276 ordinary directly evaluated attacks. Rock Tomb is D2: its 60-power physical Rock damage at 95% accuracy remains scored even though the Speed-drop secondary receives no unsupported tactical credit. The 131-entry damage-engine override list is audited; 70 damaging moves are classified under the engine-override D3 reason.

D3 fail-closed reasons: non-target 2; named engine override 70; multi-hit 29; fixed damage 8; recoil 14; drain 12; self-KO 4; two-turn/charge 16; counter-like 4; OHKO 4; other effect 94; Z/Max pseudo range 154; recharge/lock 20; conditional script 14.

| Witness | Source-backed disposition |
|---|---|
| Rival / Ironmon Smart / Charmander vs Squirtle | With public target identity, Water Gun is the sole near-best action: the Standard level-5 fixture reports Tackle damage 3, envelope 3–18, utility 14 versus Water Gun damage 11, envelope 10–42, utility 54; singleton selection consumes zero draws. The additional known-public-species differential witness reports Tackle utility 19 vs Water Gun 54. If public species is still `UNKNOWN`, both can be admitted as unknown-potentially-productive and seed 2 selects Tackle; source text now captures the Illusion-aware public appearance before the next decision. This is a source explanation for a possible path, not a replay or final verdict on the private runtime incident. |
| Brock / Onix | Source trainer has Tackle, Bind and Rock Tomb. Standard gives Tackle damage 9 / utility 17 and Rock Tomb damage 37 / utility 72; Ironmon utilities 21 vs 90. Rock Tomb is selected as sole near-best with zero draws. Bind stays fail-closed D3. |
| Sandshrew / Accuracy | Marginal gains at stages 6→5, 5→4, 4→3 are 25, 15, 10. The first and second successful same-family uses are eligible; a third harmful pure-status repeat is hard-floor excluded and Tackle is selected. Sand Attack and Smokescreen share memory; misses do not count as successful reductions; turn progression and same-active replacement retain accepted memory. |
| Caterpie / String Shot | The first use that certifiably flips public turn order is admitted. Once the marginal order value is gone, Tackle wins. |

These are deterministic host/source witnesses. They do not certify private runtime behavior or broad battle-mechanics coverage.

### Settings, replacement and compatibility

- Settings/raw compatibility: **PASS**. Legacy raw mappings and Legacy Smart meaning are preserved; Standard/Ironmon selections do not alter Difficulty, scaling or unrelated rules; fresh defaults and Ironmon preset match the accepted 4/1/0/7 and 4/1/0/8 mappings.
- Replacement Safety: **PASS**. Opponent-party ownership/range is preserved; invalid/sentinel candidates fail closed; two-/three-mon and final-faint paths pass.
- Legacy Smart remains the isolated legacy CFRU path. No profile redefinition, Expert/Omniscient work or excluded-mode rerouting is claimed.
- Save delta: **0**. No SaveBlock expansion/migration, persistent-field change, DPE ABI/table change or randomizer table/repoint change is reported by the accepted CFRU source witness.

## Workspace host/reference and source-ownership gates

All Workspace commands below ran on `integration/cfru-ai-finalization-pin`, rooted at base `f817b37261228f4013a9106cc9608e9f0042bfb8`; source-side checks used the exact checked-out CFRU Gitlink above:

| Command | Result |
|---|---|
| `python3 07_scripts/ai_policy/cli.py validate` | **PASS** — 122 fixtures; schemas v1/v2/v3. |
| `python3 07_scripts/ai_policy/cli.py run --policy standard --replicate 0 >/dev/null` | **PASS**. |
| `python3 07_scripts/ai_policy/cli.py replay --fixture-id standard_equal_four --policy standard --replicate 37 >/dev/null` | **PASS**. |
| `python3 07_scripts/ai_policy/cli.py summarize --policy standard --replicate 0` | **PASS** — 30 decisions, 30/30 oracle agreement, zero deterministic/hidden/submitted-action/future-RNG mismatches, zero illegal/no-effect/missed-KO/redundant-status violations. |
| `python3 07_scripts/ai_policy/cli.py run --policy ironmon_smart --replicate 0 >/dev/null` | **PASS**. |
| `python3 07_scripts/ai_policy/cli.py replay --fixture-id ironmon_equal_four --policy ironmon_smart --replicate 37 >/dev/null` | **PASS**. |
| `python3 07_scripts/ai_policy/cli.py summarize --policy ironmon_smart --replicate 0` | **PASS** — 63 decisions; accepted threshold, response and near-best constraints; zero replay/twin mismatches. |
| `python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'` | **PASS** — 98 tests. |
| `python3 scripts/check_coherent_learnsets.py` | **PASS** — 144000 initial-moveset cases; 820 exact replacements; two form tables; seven rebindings; 27 reserved sentinels; invalid rows/pointers rejected. |
| `python3 scripts/check_premier_bonus.py` | **PASS** — 11110 purchase cases plus capacity, reward, failure and non-ball controls. |
| `python3 scripts/check_renewable_hidden_items.py` | **PASS** — accepted renewable table/source behavior. |

The three CFRU `check_*` source commands ran in the CFRU submodule working directory. The Workspace AI CLI and unittest commands ran from the Workspace root.

### M-009 historical wrapper and direct gates

`python3 scripts/check_hidden_item_sparkle.py` was run at the exact pin and failed closed at its historical allowed-file boundary. It reported these 19 later accepted #520/#523/#526 source/test paths:

`include/new/ai_damage_engine_overrides.inc`, `include/new/ai_opponent_replacement.h`, `include/new/settings.h`, `scripts/tests/ai_runtime_differential.py`, `scripts/tests/ai_runtime_quality_host.c`, `scripts/tests/audit_ai_damage_overrides.py`, `scripts/tests/audit_opponent_replacement.py`, `scripts/tests/audit_settings_defaults.py`, `scripts/tests/opponent_replacement_host.c`, `scripts/tests/run_ai_runtime_quality_tests.py`, `scripts/tests/run_replacement_safety_tests.py`, `scripts/tests/run_settings_defaults_tests.py`, `scripts/tests/settings_defaults_host.c`, `src/battle_strings.c`, `src/general_bs_commands.c`, `src/option_menu.c`, `src/save.c`, `src/settings.c`, `src/switching.c`.

The wrapper was not edited or broadened. The separate current gates passed by loading its existing checks in memory and calling `check_source_contract()`, `check_rejections()`, `check_host_algorithm()` and `check_map_census()`. The only in-memory scope filter removed the exact unapproved name-only paths above after confirming they are contained in the accepted source ancestry intervals #520 (`56525d78…`→`3c2f3814…`), #523 (`3c2f3814…`→`423f96f0…`) and #526 (`423f96f0…`→accepted head `f0cf999a…`). No source files or wrapper rules changed.

Results: source ownership and exact frame sequence **PASS**; eight invalid ownership/order/scanner candidates rejected **PASS**; compiled actual scanner host algorithm **PASS** (filtering, camera edges, 36 packed counters, independent cooldowns, map/reset lifecycle, pickup/renewal and task pressure); reference census **PASS** — 426 Cyan/NatDex maps and 425 pret maps, maximum 36 BG events each.

## ARM, full source build, ABI and save disposition

- `arm-none-eabi-gcc` and `arm-none-eabi-ld` are unavailable in this environment. No compiler was installed or downloaded.
- Required status: `ARM_RECHECK_UNAVAILABLE_ENVIRONMENT`. No fresh ARM syntax, target object, undefined-symbol, relocatable/runtime-helper closure or production-CFLAGS result is claimed for this integration.
- Required status: `FULL_SOURCE_BUILD_NOT_RUN_TOOLCHAIN_UNAVAILABLE`. `python3 scripts/build.py` was not run because the approved source toolchain is incomplete; missing non-sensitive tools are `arm-none-eabi-gcc`, `wav2agb` and `mid2agb`. `scripts/make.py` was not used.
- The accepted #526 exact source tree reports save delta 0 and no Trainer/Pokemon/BattleMove/NewBattleStruct layout regression. Its host layout witness distinguishes `BattleStruct=0x208` in the host harness from target ARM `BattleStruct=0x200`; `BattlePokemon=0x58`, `BattleMove=0xC`, `NewBattleStruct=0xC08`. Standard battle-local state and accepted Ironmon aligned fields remain within their recorded bounds. These are the accepted host/source witnesses, not a new ARM/object validation.
- The accepted-head/merge tree identity proves the merge added no layout or ABI source changes. No DPE ABI or randomizer table/repoint change is part of this Workspace integration.

## Project routing and #498 rebaseline

Project `FireRed Gen 9 Randomizer — Pilot Finish` was read and synchronized:

- #527 = **P0 / Integration / Doing**.
- #498 = **P0 / Runtime Acceptance / Blocked**.
- #526, #520, #521, #523 and #524 = **Done**.
- #499/#500/#501 remain **Backlog** with their existing P1 priorities and Work Types.

After the integration evidence and PR were prepared, a sanitized revision-bound #498 rebaseline comment was posted. It preserves prior runtime observations as historical revision-bound evidence, notes that the #523 Replacement Runtime PASS used the previous integrated CFRU basis `423f96f0dcd501a64c2327d726a98f1964937ac1`, and binds prospective CFRU `fa83aae29818434cca6813be28f509b04c5dd68b` only after the Workspace PR is user-merged and CONTROL post-merge-verifies it. The comment claims no new runtime correction and keeps `ROM_PROFILE_READY` blocked.

The first post-merge runtime witnesses required by that comment are:

1. Ironmon Smart Rival — Charmander vs Squirtle, Water Gun vs Tackle.
2. Brock / Onix — Rock Tomb vs Tackle.
3. Sandshrew — turn-by-turn Sand Attack, including successful use 1, successful use 2 and attempted use 3.
4. Caterpie — String Shot marginality and the subsequent attack.
5. Trainer with 2+ Pokémon — replacement-sanity regression.

Only if all targeted witnesses PASS should the remainder of #498 R1 continue. `ROM_PROFILE_READY` remains unclaimed; R2, #499 and #500 remain downstream.

## Safety and limitations

- No ROM, save, emulator state, generated/private build as input, screenshot, tool binary contents, `.env`, token, key, secret or private runtime path was accessed or requested. The M-009 scanner-host gate created and automatically removed its temporary test executable.
- No Workspace source/status file other than the single evidence document was changed; no component other than the authorized CFRU Gitlink moved.
- No emulator/runtime acceptance, fresh ROM build, full source build, ARM/object result, complete Gen-1–9 tactical mechanics coverage, `ROM_PROFILE_READY`, R2, BizHawk/Tracker readiness, Legacy Smart redefinition or upstream contribution is claimed.
- No PR was merged and no history was rewritten. `UPSTREAM_CONTRIBUTION = DEFERRED`.
