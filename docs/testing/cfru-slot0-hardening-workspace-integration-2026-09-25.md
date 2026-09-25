# CFRU Slot-0 Hardening Workspace Integration Evidence

Date: 2026-09-25. Contract: Workspace Issue #530. Result submitted for CONTROL review:

**`WORKSPACE_CFRU_SLOT0_HARDENING_PIN_READY`**

This result means the accepted CFRU source-hardening merge is pinned and its source/integration gates pass. It does not clear #529's runtime blocker or claim runtime acceptance.

## Revision identity

| Item | Value |
|---|---|
| Workspace base | `4a03fcea95c08475526679127f4844bd363e066f` (`main`) |
| Workspace branch | `integration/cfru-slot0-hardening-pin` |
| Target | `main` |
| Final Workspace head | The evidence-bearing PR head is recorded verbatim in the revision-bound #530 handoff and PR after push; a commit cannot contain its own object ID. |
| Old CFRU Gitlink | `fa83aae29818434cca6813be28f509b04c5dd68b` |
| New CFRU Gitlink | `b8e58508f2474db1702c5fa0429a24dc076f1abc` |
| Accepted CFRU PR #55 head | `9ffd5fd29b7250733bda501c2fb6d7aa49939949` |
| Merged CFRU pin / target ref | `b8e58508f2474db1702c5fa0429a24dc076f1abc` (`compat/firered-gen9-randomizer`) |
| Accepted-head and merge tree | `e46cb57201a67e6813125cec5153946ae4ac0e7c` |

The exact Workspace change set is limited to:

1. `02_external/CFRU-expansion` — mode-160000 Gitlink update from `fa83aae29818434cca6813be28f509b04c5dd68b` to `b8e58508f2474db1702c5fa0429a24dc076f1abc`.
2. `docs/testing/cfru-slot0-hardening-workspace-integration-2026-09-25.md` — this evidence.

No other Workspace file or Component Gitlink is changed.

### Accepted-head to merge proof

At the CFRU submodule:

- `b8e58508f2474db1702c5fa0429a24dc076f1abc` has parents `fa83aae29818434cca6813be28f509b04c5dd68b` and accepted head `9ffd5fd29b7250733bda501c2fb6d7aa49939949`.
- `git rev-list --count 9ffd5fd29b7250733bda501c2fb6d7aa49939949..b8e58508f2474db1702c5fa0429a24dc076f1abc` returns `1`; that sole commit is the two-parent PR merge commit.
- `git diff --name-status` and `git diff-tree --no-commit-id --name-status -r` between accepted head and merge return no paths.
- Both revisions resolve to tree `e46cb57201a67e6813125cec5153946ae4ac0e7c`.
- The exact start Workspace commit is `4a03fcea95c08475526679127f4844bd363e066f`.

### Other Component pins

| Component | Revision | Disposition |
|---|---|---|
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | Unchanged |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` | Unchanged |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` | Unchanged |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | Unchanged |

Direct base-tree Gitlink inspection and recursive submodule status confirm these exact four pins remain unchanged.

## Exact merged-pin CFRU gates

All commands ran from `02_external/CFRU-expansion` at exact `HEAD` `b8e58508f2474db1702c5fa0429a24dc076f1abc`; each exited 0.

| Command | Result |
|---|---|
| `python3 scripts/tests/run_standard_ai_tests.py` | **PASS** — Standard production twins `4096 / 0`; Ironmon production twins `1024 / 0`; Badge twins `16 / 0`; Badge oracle `663000 / 663000`; damage oracle `98304`; replacement, dispatch, layout and save-delta witnesses pass. Legacy Smart isolation passes. |
| `python3 scripts/tests/run_ironmon_ai_tests.py` | **PASS** — Ironmon parity `63 / 63`; mandatory tags `58 / 58`; accepted host digests unchanged. |
| `python3 scripts/tests/run_settings_defaults_tests.py` | **PASS** — raw settings compatibility, legacy Auto/unknown preservation, fresh defaults and Ironmon preset mapping. |
| `python3 scripts/tests/run_replacement_safety_tests.py` | **PASS** — party ownership/range, safe fallback, invalid candidate rejection, repeated two-/three-mon replacement, final-faint stop and voluntary target identity. |
| `python3 scripts/tests/run_ai_runtime_quality_tests.py` | **PASS** — 991-move source census, runtime-quality witnesses and production-vs-Workspace-host differential. |
| `python3 scripts/tests/run_ai_controller_fallback_tests.py` | **PASS** — exact policy status codes, bounded own-move emergency, no silent slot-0 coercion, source-owned Oak reveal lifecycle, profile routing and controller-buffer parity. |
| `python3 scripts/tests/audit_ai_damage_overrides.py` | **PASS** — all 131 named damage-engine overrides audited. |

Accepted digest identities remain unchanged:

- v1 `uniform_legal`: `71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7`.
- v2 `standard`: `227ecebc2b937671cc4f2fbab1694abf1b7c186f7e455ed7daf22014b62d0a85`.
- v3 `ironmon_smart`: `0a637d0bc42cb2e37701bbfa33677ae95c878b1f9a67ec55a60e15a4fbdb85d7`.

The exact-pin source census is `991` moves: `721` damaging and `270` status; D0/D1/D2/D3 counts are `49 / 117 / 110 / 445`. Production-vs-Workspace-host differential parity is `10 / 10`, with `0` field, decision or RNG mismatches. Runtime-quality counters remain zero for illegal/no-effect selection with a productive alternative, missed robust KO, third harmful same-family repeat, below-epsilon selection, and unsupported selection below a clearly superior supported alternative. The sole all-futile fallback remains `NO_PRODUCTIVE_ACTION`.

## Oak's-Lab opening Rival and slot-0 hardening

The primary witness binds `TRAINER_RIVAL_OAKS_LAB_SQUIRTLE` (trainer ID 326), level 5, with `TrainerMonNoItemDefaultMoves`. At the unchanged DPE pin `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`, the suite compiles and runs production `GiveBoxMonInitialMoveset`, production `GiveMoveToBoxMon`, and the pinned level-up table using bounded box-mon storage. It derives and asserts, rather than hand-entering, these moves:

| Slot | Move ID | Move |
|---:|---:|---|
| 0 | 33 | Tackle |
| 1 | 39 | Tail Whip |
| 2 | 55 | Water Gun |
| 3 | 0 | None |

The witness starts with player `standardDisplayedSpecies == SPECIES_NONE` and public types unavailable. It calls the production `PrepareStringBattle(STRINGID_INTROSENDOUT, bank)` for opponent bank 1 and player bank 0, then executes the same exported Illusion-aware public-species helper retained at the production `STRINGID_INTROSENDOUT` and `STRINGID_SWITCHINMON` call sites. CONTROL's accepted #529 source-order review confirms the player print-string -> `BufferStringBattle` reveal occurs before first opponent AI choice; the reviewed path sets `gActiveBattler` to the requested bank and no AI setup/cache clear erases the player public identity before selection.

Before reveal, player public species is `SPECIES_NONE` (`0`) and public types are unavailable. After reveal, player public species is Charmander (`4`), public types are available `[10,10,25]`, and opponent public species is Squirtle. Battle flags are `0x00000008` (`BATTLE_TYPE_TRAINER`); the Standard/Ironmon support predicates route only to the matching requested profile. Both `gBattleMons[1].moves[0..3]` and controller `moveInfo->moves[0..3]` are `[33,39,55,0]`; the observation count is 4.

### Positive revealed decision

| Profile | Trainer AI raw / resolved | Standard supported | Ironmon supported | Candidate slots (ID: move / damage / utility) | Admission / near-best | Policy result and emission |
|---|---|---:|---:|---|---|---|
| Standard | `7 / enum 6` | 1 | 0 | `0: Tackle / 3 / 12`; `1: Tail Whip / 0 / 7`; `2: Water Gun / 11 / 44`; `3: None / 0 / 0` | Occupied moves admitted; Water Gun alone near-best; None illegal | rc `0`, selected ID `2`, pending clear, returned slot `2`, emitted slot `2`, final move ID `55` Water Gun |
| Ironmon Smart | `8 / enum 7` | 0 | 1 | `0: Tackle / 3 / 14`; `1: Tail Whip / 0 / 0`; `2: Water Gun / 11 / 54`; `3: None / 0 / 0` | Occupied moves admitted; Water Gun alone near-best; None illegal | rc `0`, selected ID `2`, pending clear, returned slot `2`, emitted slot `2`, final move ID `55` Water Gun |

Ironmon records one response row (`ID 65535`, weight 1). The selected slot matches the controller slot and `gBattleMons[1].moves[2]`; parity passes. No emergency fallback is taken by either correct policy decision.

### Negative omitted-reveal decision

The negative witness uses the identical trainer, Level 5, derived moves, player state and flags but deliberately skips the public-reveal producer. Displayed player species remains UNKNOWN/`SPECIES_NONE`; public types remain unavailable; battle/controller move buffers remain `[33,39,55,0]`.

- Tackle ID 0 and Water Gun ID 2 are both legal; each has expected damage `0`, utility `0`, `unknown_potentially_productive=1`, and is in the near-best pool.
- Tail Whip is rejected below the productive-action floor (`floor/admission=128`); `None` is illegal.
- Standard and Ironmon Smart each return policy rc `0`, select ID `0`, leave pending state clear, and return/emit slot 0 Tackle ID `33`.

This is the diagnostic unknown-species Tackle/Water Gun tie, not a policy validation error or adapter emergency. It reproduces the slot-0-like runtime symptom only when reveal is omitted. The audited opening lifecycle runs reveal before the first AI decision, so this is not the valid Fresh-New-Game opening state. The older Cerulean level-18 witness is secondary only.

### Fallback and controller invariants

The merged source retains the #529 hardening: stable, distinct Standard policy results (`0`, `-1`, `-2`, `-3`) and Ironmon policy results (`0`, `-1`, `-2`), with response-builder validation separately identified. Policy errors, no admitted action, selected-ID lookup failure and invalid pending state route to the bounded own-move emergency; they do not silently become literal slot 0. Tests prove Standard validation error, no-action error, lookup miss, invalid pending state and Ironmon validation error separately. Normal Rival and Brock policy selections do not enter the emergency. Injected stale/permuted controller buffers are normalized from the active own `gBattleMons` slots before `EmitMoveChosen`; emitted slot and move ID match the selected authoritative move.

Policy epsilon, status/accuracy scoring, Legacy Smart meaning and accepted v1/v2/v3 digests remain unchanged. No Expert/Omniscient profile or battle-mechanics expansion is introduced.

## Workspace host/reference and source-ownership gates

All applicable Workspace-side commands passed at the exact Workspace branch source and CFRU Gitlink:

| Command / gate | Result |
|---|---|
| `python3 07_scripts/ai_policy/cli.py validate` | **PASS** — 122 fixtures; schemas v1/v2/v3. |
| Standard policy CLI run / replay / summarize | **PASS** — replicate 0 and `standard_equal_four` replicate 37; summary has 30/30 oracle agreement, zero deterministic/hidden/submitted-action/future-RNG twin mismatches and zero quality violations. |
| Ironmon Smart CLI run / replay / summarize | **PASS** — replicate 0 and `ironmon_equal_four` replicate 37; summary has 63/63 oracle agreement, zero deterministic/hidden/submitted-action/future-RNG twin mismatches and zero quality violations. |
| `python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'` | **PASS** — 98 tests. |
| `python3 scripts/check_coherent_learnsets.py` (CFRU) | **PASS** — 144,000 initial-moveset cases; 820 exact replacements; 2 new form tables; 7 rebindings; 27 reserved sentinels; invalid rows and pointers rejected. |
| `python3 scripts/check_premier_bonus.py` (CFRU) | **PASS** — 11,110 purchase cases plus capacity, reward, failure and non-ball controls. |
| `python3 scripts/check_renewable_hidden_items.py` (CFRU) | **PASS** — accepted renewable hidden-item source-table contract. |

Workspace policy RNG isolation passes: decisions preserve determinism, hidden-information and submitted-action twins, and future RNG state. No generated build or protected artifact was used as test input.

### M-009 historical wrapper disposition

`python3 scripts/check_hidden_item_sparkle.py` was run and failed closed at its historical allowed-path boundary. It reported 24 later accepted source/test paths from #520/#523/#526/#529. The wrapper and its rules were not changed or weakened.

The current M-009 gates were then invoked separately from the unchanged wrapper in memory. A strict scope filter was allowed only after the wrapper's unapproved path set exactly matched the accepted later-source path set; it introduced no source changes and left all M-009 assertions intact. Results: source ownership/exact frame sequence **PASS**; eight invalid ownership/order/scanner candidates rejected **PASS**; actual compiled scanner host **PASS** (filtering, camera edges, packed counters, cooldowns, lifecycle, pickup/renewal and task pressure); reference-map census **PASS** — 426 Cyan/NatDex maps and 425 pret maps, maximum 36 BG events each. The historical all-in-one wrapper remains fail-closed for its known path-boundary limitation.

## ARM/object and full-build status

`ARM_RECHECK_UNAVAILABLE_ENVIRONMENT` — approved devkitARM is unavailable. `arm-none-eabi-as`, `arm-none-eabi-gcc`, `arm-none-eabi-ld`, `arm-none-eabi-nm` and `arm-none-eabi-objcopy` are missing. No ARM syntax/object, production-CFLAGS, undefined-symbol or relocatable/runtime-helper closure result is claimed. No tool was installed or downloaded.

`FULL_SOURCE_BUILD_NOT_RUN_TOOLCHAIN_UNAVAILABLE` — `python3 scripts/build.py` was not run because the complete approved toolchain is unavailable. Missing non-sensitive tool names: `arm-none-eabi-as`, `arm-none-eabi-gcc`, `arm-none-eabi-ld`, `arm-none-eabi-objcopy`, `wav2agb`, `mid2agb`. `scripts/make.py` was not used. No ROM was accessed.

## ABI, layout and save disposition

The exact-pin Standard host/source witnesses pass with save delta `0`. Recorded host/source layout values remain `BattlePokemon=0x58`, `BattleMove=0x0C`, `BattleStruct=0x208` in the host harness (`0x200` target ARM ABI), and `NewBattleStruct=0xC08`; Standard and Ironmon AI state layout witnesses pass. The Ironmon aligned `NewBattleStruct` delta remains 56 bytes. No Trainer/Pokemon/BattleMove/save schema, DPE ABI, randomizer table/repoint or persistent-storage change is included. Fresh target ARM ABI witnesses were not rerun because the compiler is unavailable.

## Runtime and project disposition

- #529 remains open with `RUNTIME_SOURCE_MISMATCH_BLOCKER`; the exact revealed source witness selects Water Gun, while only the invalid omitted-reveal state produces the Tackle tie.
- #498 remains **Blocked**. This integration establishes a prospective source basis only; it claims no runtime correction, no runtime acceptance, and no `ROM_PROFILE_READY`.
- After user merge of the Workspace PR and CONTROL post-merge verification, the required next step is a fresh non-randomized runtime build on that verified Workspace/CFRU basis, then the targeted Oak's-Lab Rival (Water Gun vs Tackle), Brock/Onix (Rock Tomb vs Tackle), Ironmon Smart menu/profile identity, and 2+ Pokémon replacement witnesses. If Oak still selects Tackle, stop and keep the runtime blocker. Continue Sandshrew/Caterpie and the rest of R1 only after the required targeted witnesses pass.
- Project #530 fields are set to `P0 / Integration / Doing`; #526/#527 remain Done. `ROM_PROFILE_READY` remains unclaimed and `UPSTREAM_CONTRIBUTION = DEFERRED`.

No ROM, save, emulator state, generated build input, screenshot, tool binary contents, private path, `.env`, token, key or secret was accessed or requested.
