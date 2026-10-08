# Pre-Linux pilot assurance — 2026-10-08

Refs [#705](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/705). One writer; `audit/pre-linux-pilot-assurance`. This is an evidence audit, not a new product acceptance, implementation, release or upstream contribution.

**Result:** no newly demonstrated selected-profile product regression. Existing acceptance remains **ACCEPTED WITH RECORDED LIMITATIONS**. Current interpreted checks: **111 Python + 237 Lua tests PASS**, no observed failures. Full source-profile regeneration, Java/C tests, generation and emulator execution are **NOT_RUN**. The present Tracker implementation is a guarded, detached Phase-A implementation, not a usable live integration. The current-head matrix rejection is reproduced and classified as a provenance guard/usability limitation, not a ROM failure.

The companion [TSV](pre-linux-pilot-assurance-2026-10-08.tsv) separates capability, selected setting, historical method/revision, carry-forward, current execution and remaining witness. `SOURCE_INSPECTED` is not a newly executed component test; `HISTORICAL_ACCEPTED` is not a test rerun. UNKNOWN remains UNKNOWN. No existing acceptance is revoked or expanded.

## 1. Exact basis and live control plane

Read AGENTS.md and docs/{PROJECT,ENGINEERING_RULES,ENVIRONMENT,REPRODUCIBILITY,ROADMAP,MODEL_POLICY}. Historical inventories/status mirrors were used as checklists only. Remote main, local object and tree agree:

| Basis | Commit | Tree |
|---|---|---|
| Audited Workspace main | `89f83c914d430f20a304e67be76483c02c8b67c8` | `e3305feca3f09b3fcd6e84934bd814990a743726` |
| Accepted product lock | `3bdfe9919afc0b7bea55c79f37285e832be495c3` | `f6bc65355811d7de153a91091b223fec9b50991e` |

All ten entries are mode 160000, equal their source checkout HEAD, and have no tracked checkout changes. Source-file existence was checked using tracked `.c/.h/.java/.lua` paths; counts below are availability, not compilation or full asset validation. No protected asset contents were inspected.

| Source checkout | Exact Gitlink/HEAD | Source files present/listed |
|---|---|---:|
| `02_external/CFRU-expansion` | `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2` | 468/468 |
| `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `d887185de1f6ae6a78e85c4311bbadde17041d00` | 39/39 |
| `02_external/Ironmon-Tracker` | `c450ecaee2d8131a2789bb656e3be792a93712fb` | 104/104 |
| `02_external/NatDexExtension` | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | 1/1 |
| `02_external/references/cyansmp64-pokefirered-natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | 731/731 |
| `02_external/references/cyansmp64-upr-zx-natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | 117/117 |
| `02_external/references/pret-pokefirered` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | 720/720 |
| `02_external/references/upr-fvx-upstream` | `e0788edc6529c2605f201996e4807ff30165354c` | 291/291 |
| `02_external/references/upr-zx-ajarmar` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | 117/117 |
| `02_external/upr-fvx` | `4670a5413104ec02bc08c09ff584470a8a6cb7bd` | 385/385 |

All ten product-lock Gitlinks equal current main. The product-to-main diff comprises 29 Tracker extension/profile/runner/test/documentation files, not CFRU/DPE/UPR changes. Thus product evidence carries at identical component source; Tracker evidence must use the newer Workspace revision. No repinning occurred. In this report C, D, U and T abbreviate the exact CFRU, DPE, UPR and Tracker pins above; W denotes audited Workspace main.

Live GitHub Issue bodies/comments and [Project 4](https://github.com/users/Planton361/projects/4) were queried through `gh` on 2026-10-08. Project data was accessible (not inferred from PRs). Snapshot:

| Issue(s) | Issue state | Actual Project Status | Actual Priority / Work Type |
|---|---|---|---|
| #498 | CLOSED | Done | P0 / Runtime Acceptance |
| #499 | OPEN | Done | P1 / Tracker-BizHawk |
| #500 | OPEN | Backlog | P1 / Tracker-BizHawk |
| #501 | OPEN | Backlog | P1 / Release |
| #681, #685, #686, #688, #690 | CLOSED | Done | UNKNOWN / UNKNOWN |
| #691, #692 | OPEN | Done | UNKNOWN / UNKNOWN |
| #689, #693, #694, #695, #705 | OPEN | UNKNOWN | UNKNOWN / UNKNOWN |

#499 and #691/#692 have a real Issue/Project status discrepancy: Done does not establish Linux readiness or Phase-B completion. #705 requests P0 / Analysis-Verification in its body; those fields are not populated in the observed item. Missing fields are UNKNOWN. Routing remains #705 verification supporting #500 and #501; Linux host work under #499/#689, production Tracker work under #500/Phase B, final freeze under #501. No status fields or Issues were changed.

## 2. Acceptance reconstructed, with carry-forward boundaries

- [#635 final acceptance](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/635#issuecomment-5974792957): Workspace `58d0ae45fddb74e04eb1dc997b439cdbb900735e`, C/D equal today, U then `7bf79ee1e7c46c972f7a9c84942970a950be0723`. User-owned fresh native DPE→CFRU build/link/insertion and B-quick-run ordinary wild / Prebattle OFF, Ignore, Engage and excluded scripted/special controls passed. No S0/S1. D04–D16 and later B/C/E/F/G/P coverage remained NOT_RUN and accepted nonblocking. The source candidate and merged C tree are equivalent; these witnesses are historical, not repeated here.
- [#660](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/660) at Workspace `cbfab73f8a2ea08d0146bebdbe9a98439e1cc014`, U `61c188fab8b98029871f69b79ff11d6d28b54a4f`: trainer identity, species/form/assets and broad safe evolution gaps led to bounded repairs. [#670](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/670), Workspace `f2f2598f2b34dce12dde9d934df9bbe9744cf364`, U `75eab27a6e7eab0713534596303d19722f06127e`, accepted those P0 closures; the selected IronMON ability policy was the remaining blocker. This chronology prevents reusing an older unsafe ability verdict as today's truth.
- [#675 acceptance](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/675#issuecomment-6024841012): Workspace `762054f19c6f070110b2fde3f08e90697a604cd5`, U `48f657b3958bc2ff902fe85ca866ba11c5250a50`; #672/UPR #195 handler-owned ability semantics closed the selected blocker. Historical 1,542 relevant ROM-free tests had zero failures/errors/skips. This was source readiness only. The later legendary classification repair UPR #196 reached `213ed055e301263c4577ac329b81a6cb9ff587a9` before replay repair.
- [#676 final](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/676#issuecomment-6044184674) and [#498 final](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498#issuecomment-6044186528): explicit user acceptance at the product lock, current C/D/U pins, for CONTROL_UNCHANGED, CASUAL_NATDEX and IRONMON_NATDEX. ROM_PROFILE_READY and RANDOMIZER_PROFILE_READY passed **with recorded limitations**. This is neither universal Gen1–9 mechanics certification nor BizHawk/Tracker/freeze acceptance.
- #676 carries generation, settings/reopen/replay/boot and CC01 preservation evidence; Casual observations include Drednaw starter, early wild/trainer paths, field items/shop/save, gift Magikarp→Staravia, Starly→Weepinbell at 14, TM39 Power Swap teach/use/reuse, tutor teach/use, forgettable HM, trade, hidden-item and TM-ball paths. Ordinary Gen9 and safe regional fixed-seed runtime placement were not separately observed. IM01–IM05 were not individually completed. Those remain accepted residuals, not new PASS or newly imposed blockers.
- [#681](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/681), [#685](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/685), [#686](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/686) and [UPR #197](https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/197): the genuine transient seed-677 MAX_SAFE_COMBINED ReplayMismatch was fixed by deterministic palette-selector constructor calibration, `new Random()` → `new Random(0)`. Caller-seeded cosmetic selection is unchanged. UPR production delta from `213ed055…` to U is confined to `Gen3to5TypeColors.java`; three replay fixture/probe/test files accompany it. Unaffected paths carry by source equivalence. Final historical confirmation was ten independent direct `attempt(..., replay=True)` runs at the product lock, not another full 297-case run and not emulator proof.

The historical 130-row `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` covers 11 GUI families. It is a checklist, not 130 current support claims. Current source counts are 159 overlay IDs, 4 generator-unsupported, 13 target-excluded, 142 required overlays. The 297 intents comprise 3 selected + 142 overlays + 56 modes + 12 full families + 66 pairs + 12 triples + 5 maximal + 1 diagnostic. Historical 234 unique effective states are a different denominator. Earlier 302-case evidence and its 44 failures must not be relabeled as the final inventory.

## 3. Source findings by ownership

### Data, identity and engine

D `include/species.h`, `src/Base_Stats.c` and U `SpecialFormPredicates.cfruDpePoolCategory` distinguish internal identities from Dex numbers. Sprigatito is Dex 906 / internal 1294, Pecharunt internal 1439, and regional rows retain separate identities. Generic `getAltFormes()` being empty does not mean DPE regional rows are absent: they are base identities. The pool policy rejects unused 0xFC–0x114, egg 0x19C, missing source rows, Mega/Primal/G-Max/Eternamax/Tera/temporary and condition-dependent states before allowing ordinary, regional and persistent alternate forms. Minior cores and Origin-form configuration are source-specific, not generic form-flag guesses. `Gen3RomHandler.getCfruDpeRandomPoolEligibility` additionally requires positive stats/type, an internal-ID learnset and valid front-image/normal-palette pointers. This establishes a guarded pool, not all assets or mechanics for every row.

C `src/config.h` enables EXPAND_MOVESETS; D `src/defines.h` leaves EXPAND_LEARNSETS disabled. C's `src/Tables/level_up_learnsets.c` is the active learnset owner. Historical data-parity/TM07 reports distinguish comparable data from unmodeled mechanics: a zero comparable mismatch ledger is not universal ability behavior, move implementation, egg/tutor acquisition or form lifecycle parity. Hospitality/M-011, Commander, Embody Aspect and missing Gen9/Z/Max/G-Max/Terastal semantics are not new work authorized here. FROSTBITE is enabled; a stock Tracker Freeze label would be semantically wrong.

CFRU ability assignments and numeric aliases are distinct from runtime semantics. U's handler-owned immutable `AbilityRandomizationPolicy.cfruDpe()` uses 1..0xFE, excludes Forecast/Portal Power as candidates (252), and yields the accepted selected IronMON 230-ID pool. Generic numeric filters would confuse, for example, 129 Strong Jaw with Defeatist, 112 Quick Feet with Slow Start, and 103 Download with Klutz. U's current randomizer consumes the handler policy; these are repaired historical defects, not current reopened blockers. Ability display names can still be contextual aliases; a static catalog does not prove which ability a party member currently has.

### Preservation, writers and selected profiles

U `Gen3RomHandler` retains raw move types, unchanged ability tuples (including zero second slot and hidden slot), evolution rows and opaque trainer data. `saveBasicPokeStats` preserves zero slot 2 only when the whole loaded tuple is unchanged; intentional randomization retains the accepted fallback and updates the saved snapshot. Ordinary stats/types are read from the chosen species' data; changing the selected species does not itself randomize those fields.

Trainer writers use the Species/internal identity for CFRU learnset lookup, avoiding the Dex/internal collision. Expanded item/custom-move rows are 32 bytes with separate item/move/ability/nature/IV/EV/Tera fields; AI fields are not overwritten by ordinary species serialization. CFRU owns Standard raw 7 (Control/Casual) and Ironmon Smart raw 8. IronMON's +50% level modifier is UPR-owned; native trainer/wild scaling remains OFF. Better Trainer Movesets and Sensible Held Items remain OFF by profile, with generic heuristic/semantic limitations; this is not a blanket declaration that every held-item mode is unsupported.

Evolution serialization compares original raw rows against the current buffer, preserves unchanged slots/holes/metadata, validates planned ordinary targets and rejects unmodeled changed relationships before writing. RANDOM_EVERY_LEVEL and incomplete generic evolution improvement consumers remain guarded/excluded. The earlier evolution-improvement overlay failures (25/27) and palette follow-types/shiny-from-normal failures were capability limits, not reasons to weaken guards. Reusable-TM overlay 11 is excluded because CFRU already owns the behavior. A successful sensible-held diagnostic does not establish sensible-item semantics.

| Setting | Control | Casual | IronMON |
|---|---|---|---|
| Species selection | unchanged | selected randomization | selected randomization |
| Base stats / abilities / learnsets | unchanged | unchanged | randomized; four starting moves |
| Types | unchanged | unchanged | unchanged |
| Ordinary evolutions / TM-tutor / items-shops | unchanged control | selected randomization | selected randomization |
| Better trainer movesets / sensible held items | OFF | OFF | OFF |
| Palettes | OFF | OFF | OFF |
| CFRU AI / native scaling | Standard 7 / OFF | Standard 7 / OFF | Smart 8 / OFF |
| UPR trainer level modifier | unchanged | unchanged | +50% |
| Selected UPR Misc | none (mask 0) | Fastest Text | Fastest Text |

Pickup randomization remains UNCHANGED/unsupported for the accepted target. Settings serialization/reopen/replay is historical accepted evidence; the matrix's target-bound Gen-limit normalization witness permits true→false and mask 0x3FE→null only under its target/CRC checks. It must not be presented as an effective Gen1–9 filter. Race/preset/seed behavior remains within accepted selected settings, not arbitrary GUI combinations.

### TM07, QoL and low-level invariants

[#626](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/626) and [TM07 integration audit](tm07-policy-a-integration-2026-10-03.md) close only the approved Policy-A membership contract: slot 7 / `gTMHMMoves[6]` / Low Kick source header agree, 212 exact unique members, 1,440 rows × 128 bits (16 bytes), bit 0x40, all other 127 bits preserved. Tutor layout is 152 bits / 19 bytes. Historical source-builder replay hash is `7f7685bd360fdf79c9136e64ba53330a29fa4da6cec48a7d546e9095d2c387da`; it was not regenerated here. C/D are identical to that acceptance. The zero ledger does not establish every acquisition/inheritance rule or every runtime machine path.

The [R0 scope audit](m014-r0-final-rom-scope-2026-10-03.md) supplies the QoL checklist: Name Rater/centers, renewal exclusions, starter/Parcel/Bill flow, initial PC/Lab/Mom behavior, Premier Ball quantity, field-HM predicates, fast messages, hidden-item sparkle and coin ABI. Current C owns early/indoor running, reusable TMs and forgettable HMs; U's National-Dex-at-start guard and targeted running signature checks prevent blind vanilla patches. Fastest Text is the selected Casual/IronMON UPR tweak; Control has no Misc tweaks; native fast-battle-message flag 0x925 is a distinct setting.

Current C `ScrCmd_dowildbattle` consumes and clears Var800B==0xB632 **before** battle start, records the battle-local origin bit, and preserves the vanilla scripted-wild setup sequence. `CanUseBQuickRunHere` accepts only ordinary wild or the exact consumed prebattle-origin pair (after masking master/double), rejects raids and retains normal downstream escape restrictions. Ignore never starts battle. Thus no persistent scratch variable is used as battle-time provenance. The hook is an 8-byte entry replacement within the documented 16-byte command span; `ctx` remains in r0. M009's named function rewrite preserves frame ordering; coin `checkcoins` preserves the halfword operand and saturates the u32 wallet export to u16. These are inspected source and carried accepted ABI/hook evidence, not fresh native/emulator validation. No hook, pointer, persistent layout or ABI was changed here.

## 4. Test soundness and actual execution

Every executed runner/test and its relevant helper was read first. Python matrix private operations are mocked; temporary data is synthetic. Tracker Lua suites import public source data and detached modules with memory/host traps. No full Tracker entrypoint was loaded. Python 3.9.6 and installed Lua 5.4.9 were used; no installation.

Commands (Workspace root unless `cd` shown):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s 07_scripts/randomizer/tests -p test_upr_generation_matrix.py -v
(cd 07_scripts/tracker && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_cfru_dpe_extension_source test_cfru_dpe_party_source test_cfru_dpe_battle_source test_cfru_dpe_ui_source test_generate_cfru_dpe_source_data.ParserTests -v)
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_extension_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_party_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_battle_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_ui_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/randomizer/upr_generation_matrix.py --dry-run
```

| Check | Current result | Meaning / limit |
|---|---|---|
| Matrix unittest file | PASS 89; zero failures/errors/skips | mocks, guards, normalization, replay/failure accounting; no real generation |
| Tracker source suites | PASS 4 + 3 + 4 + 3 | source boundaries, detached modules |
| Source generator ParserTests | PASS 8 | parser/alias/layout-input rejection, not full regeneration |
| Lifecycle Lua | PASS 55 | synthetic activation, transaction/rollback/epoch/ownership failures |
| Party Lua | PASS 43 | source-shaped bytes; direct CFRU layout |
| Battle Lua | PASS 76 | u16 indices, context/epoch, unknown states |
| UI Lua | PASS 63 | detached projection, no host/persistence fallback |
| Lua 5.1 | NOT_RUN | installed compatible interpreter unavailable |
| Generator `--check` and LockedProfileTests (21) | NOT_RUN | invokes clang `-cc1 -triple thumbv4t-none-eabi -fsyntax-only -fdump-record-layouts-complete`; crosses this contract's C-compilation boundary |
| Matrix dry-run | EXPECTED_GUARD_REJECTION, exit 1 | exact current-head provenance rejection; not PASS for runner usability |
| Java/JUnit, native C harnesses, builds, generation, emulator | NOT_RUN | explicitly outside this audit |

The full generator was inspected, not run with its compiler mocked away. Public profile bytes are checked by the executed source/Lua tests: 1,092,720 bytes, SHA-256 `8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981`, profile ID `sha256:31be9e07697f939b274c56eea5d92a81dd10c43e7c876586effccb335535ca75`. That verifies the checked-in source artifact's lock, not regenerating its ARM layouts or binding runtime addresses. Historical larger aggregate Python counts are not this command's denominator; current matrix-file discovery is 89.

**JUnit oracle defect/risk:** U `build.gradle.kts:28` sets `ignoreFailures = true`; `random` and `romio` testROMs do likewise. Name-based exclusions in ordinary test tasks do not prove a ROM-free suite. Disabled tests and assumption aborts can produce skips, and a missing/filtered suite can produce no meaningful evidence. A zero Gradle exit is insufficient. Future separately authorized ROM-free Java execution must use an exact reviewed suite allowlist, fixed U/toolchain, fresh task-specific XML, required suite/test identities and expected counts; reject any failure, error, skip, missing/zero suite, unexpected task exclusion or stale/up-to-date-only report. Preserve logs/process errors too. No existing build reports/binaries were read here.

Smallest Java evidence contract, if separately chosen by CONTROL: the five PR-197 suites (5 replay + 7 palette bounds + 8 evolution target + 9 ability policy + 3 synthetic palette = 32), reviewed fixtures, no testROMs/optional-ROM classes, no dependency installation, fresh-process seed-677 repetitions plus 0/1/20261005658. It would reproduce a bounded historical claim, not all UPR functionality. This is an alternative future decision, not a second proposed next task.

**Fixture limits:** `CombinedReplayFixture` removes species whose Dex number exceeds 151; its `CfruDpeEvolutionFixture` superclass returns no alt forms. It uses source-shaped synthetic models and in-memory evolution bytes; several outputs are snapshots, not a full generated-ROM writer/reopen. Equality proves determinism, not data correctness or Gen1–9/regional coverage. Independent pre-fix constructor calibration seeds expose the palette divergence; caller/gameplay versus cosmetic RNG separation has its own assertion. Historical pre-fix 100 fresh JVMs at seed 677 split 68/32; post-fix 20 were stable, with other seeds checked. None of those Java runs was repeated here. Tracker fixtures include representative Gen1/8/9/regional identities but still do not execute the real host consumers.

First failure is evidence: #681's initial seed-677 replay mismatch remains a FAIL despite a successful retry. Subsequent repair and ten independent passes are a new revision-bound result. Required-case and diagnostic outcomes remain separate; cardinalities count intents/effective settings differently. Neither retries nor a shared fixture/oracle justify universal coverage.

**Current matrix provenance:** `verify_pins` anchors Workspace `4e7bffa45d2d68919e48d5329ad8bcb55dc8408e`, tree `6186d011e5daf958142e6fd0c9a98099f96fa85f`, and permits only U's Gitlink plus the three runner/test paths. On the clean audited HEAD, before these report files existed, the ROM-free dry-run returned `Workspace has unexpected changes; CONTROL rebaseline required.` The 29 accepted Tracker/docs paths exceed the allowlist. Untracked CASUAL is ignored by the tracked-only status check and did not cause this rejection.

Exact reproducible runner choice: retain runner/source at accepted product commit `3bdfe9919afc0b7bea55c79f37285e832be495c3` with tree `f6bc65355811d7de153a91091b223fec9b50991e`, its ten Gitlinks/checkouts, clean tracked files and exact live U target verification. Its diff from the runner basis is only the U Gitlink, Python runner and matrix test file, all allowed. This source-only proof does not claim that a private run was performed. Do not copy the old runner onto new main and call that the same provenance. Alternatively a separate narrow contract could explicitly rebaseline audited immutable source identities and test accepted docs/Tracker deltas versus forbidden pin/runner/profile drift. No bypass, broad ignore rule or guard weakening is recommended or implemented.

## 5. Tracker: implemented seams versus unimplemented consumers

Reviewed [#688](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/688), [#690](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/690), [#691](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/691), [#692](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/692), [#693](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/693), [#694](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/694), [#695](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/695), [#689](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/689) and current `docs/tracker/T2_PHASE_A.md` through `T5_PHASE_A.md` / PROFILE_CONTRACT. Phase-A acceptance does not close Phase B. The #689 host runbook is preparation, not a Linux execution result.

| Pinned source path/function | Actual state and remaining implementation |
|---|---|
| W `CFRUDPEExtension.lua`: lifecycle / initialize guard | Real early GameSettings guard quarantines production (`mock=false`); synthetic factory validates imports/identity, rolls back owned changes and preserves foreign wrapper replacements. Restart tombstone prevents late reentry. Production activation is deliberately denied. |
| W party/battle/UI modules | Detached pure decoders/projection; not loaded into the production Tracker path. TEST_ONLY / live UNKNOWN. No notes/save fallbacks. |
| T `Program.lua:827 updatePokemonTeams`, `:888 readNewPokemon` | Still stock encrypted/XOR/24-substructure decoding. Real updates mutate party and verification/persistence state; invalid occupied slots can leave prior data. Source-correct direct CFRU layout/clear-before-update is not wired. Outside-battle enemy PP may be replaced by static MoveData. |
| T `Battle.lua:269 updateViewSlots` | Stock byte reads at strides 0/2/4/6 and clamping; CFRU indices require u16, 0..5 validation and one-based conversion without fabricated defaults. Detached T4 tests do not replace this. |
| T `TrackerAPI.lua:28/38/47/64/73/134/141` | Shared party objects and stock ability/types/trainer readers; no effective BattlePokemon source. Updating this API alone would miss other consumers. |
| T `DataHelper.lua:124 buildTrackerScreenDisplay`, `TrackerScreen.lua:1102 drawScreen` | DataHelper independently reads Battle/Program, static PokemonData/MoveData and persisted notes; derives BST/evolution/EXP/stages/moves/STAB/PP. Renderer consumes that view and carousel. Current detached projection is not this host route. |
| T `data/MoveData.lua:338 readMoveInfoFromMemory` | Stock byte/flag category interpretation is not CFRU BattleMove.split at byte 0x0A; effective randomized category/PP require their own reader. |
| T `BattleDetailsScreen.lua:458 updateData`, `:730 updateTerrain` | Direct field/status2/status3/side/disable/wish/weather reads bypass TrackerAPI. Requires explicit gate/invalidation; inventory is not implementation. |
| T `Battle.lua:739 beginNewBattle` | GameOverScreen temporary save-state call occurs before extension afterBattleBegins. A late callback cannot make the host read-only. End hooks also follow host mutation paths. |
| T `Tracker.lua:583/612/632` | Notes keyed by species×1000+level, save/load with file calls and hash/overwrite semantics, plus `verifyDataForPlayer` mutation. Requires session/profile-aware quarantine and ownership-safe persistence boundaries. |

Unresolved implementation inputs are finite but real: output/session identity, public RAM provenance and dynamic pointer validation; effective randomized stats/moves/types/category/max PP; selected party ability; contextual ability names; authoritative occupancy and trainer identity; all consumers' invalidation before start/end/switch/reset/output changes. Source profile sizes (Pokemon 100, BattlePokemon 88, BattleMove 12) do not supply live addresses. UNRESOLVED runtime addresses cannot be replaced by stock addresses. Unknown maximum PP must not become baseline PP; unknown ability must not become a catalog guess. Singles support does not establish doubles/special contexts. Safe UNKNOWN is required behavior but does not deliver the intended live function.

## 6. Finite remaining work and one next contract

| Class / order | Work and evidence boundary |
|---|---|
| MAC_NOW 1 | Test actual pinned Tracker consumers in the isolated sandbox specified below; highest-value gap between current mocks and real call graph. |
| MAC_NOW 2, separate decision | Full source-profile regeneration needs explicit compiler authorization; bounded Java XML/replay execution needs a separate reviewed contract. Neither is an interpreted-test PASS here. |
| MAC_NOW 3, separate decision | Document exact old runner reuse or authorize a narrow provenance rebaseline; retain all negative guards. No product repair is implied. |
| LINUX_RUNTIME_ONLY | #499/#689 host start/core/Lua/extension setup and live lifecycle checks; subsequent Phase-B binding, effective output data, UI and read-only/persistence acceptance. Current runbook alone cannot satisfy these. |
| ACCEPTED_LIMITATION | #635 residual D04–D16/later reach; ordinary Gen9/regional witnesses and IM01–IM05 individually incomplete; broader engine/acquisition limitations. No retroactive new blocker. |
| SEPARATE_DECISION | Enabling excluded optional modes, new mechanics, upstream work and #501 launch/freeze. |

**Exactly one proposed next work package:** a fresh #705-follow-up verification contract, “Pinned Tracker host-consumer sandbox,” owned by #500, one writer, new bounded approved branch. Proposed exact write allowlist:

- `07_scripts/tracker/run_cfru_dpe_host_consumer_mock_tests.py`
- `07_scripts/tracker/tests/cfru_dpe_host_consumer_mock.lua`
- `07_scripts/tracker/test_cfru_dpe_host_consumer_source.py`
- `docs/tracker/T5_HOST_CONSUMER_SANDBOX.md`

No implementation in this audit. The follow-up must load only explicitly selected function definitions from pinned T source into an isolated Lua environment (no inherited real `_G`, no Tracker/Main entrypoint). Exercise real `Program.updatePokemonTeams/readNewPokemon`, `Battle.updateViewSlots`, TrackerAPI accessors and the minimal DataHelper display-building route; stub only their external dependencies. Fail if the selected production functions drift or the harness silently substitutes its own algorithm. Use synthetic byte arrays with exact read-width/address allowlists. Trap file/network/process access, unrestricted require/load, emulator/state APIs, memory writes, save/load/notes mutation and all unapproved host callbacks. BattleDetails and persistence entry calls must be trapped/recorded as hazards, not executed against a host or merely omitted without an assertion.

Negative cases: high-byte index 0x0105 and illegal slot 6; Dex/internal collision 906/1294 and regional 1022; occupied→invalid must expose stale-party behavior; unknown ability/max PP/category must reveal stock fallback; party versus active-battle precedence; reset/end/switch/output/session changes; shared returned-table mutation; before-hook save-state/persistence calls and foreign-wrapper ownership. Characterize current stock behavior honestly (known incompatibilities are expected observations, not a falsely passing integration). Output a per-consumer dependency/required-adapter result. Acceptance: deterministic ROM-free execution, independent expected values, traps proven to fire, no host side effects, no source/Gitlink changes, live confidence UNKNOWN. This gives the next production contract concrete seams without prematurely authorizing live activation.

## 7. Upstream and launch advisory

`UPSTREAM_CONTRIBUTION = DEFERRED`.

1. Best reusable candidate: UPR #197's isolated palette-selector calibration. Target is `upr-fvx/universal-pokemon-randomizer-fvx`, not the whole CFRU/DPE fork. Live master on 2026-10-08 was [`956168804d5b39901ea12848b4fe5052c6f7c78b`](https://github.com/upr-fvx/universal-pokemon-randomizer-fvx/commit/956168804d5b39901ea12848b4fe5052c6f7c78b); its `Gen3to5TypeColors.java` still constructs with `new Random()`. This proves that exact line remains, not that every upstream call path has been retested. A future port needs an upstream-native minimal fixture, constructor-ceiling oracle, fresh-process regressions and non-CFRU controls; the Gen1 CFRU combined fixture is not sufficient universal coverage. GPL-3.0 is reported by the upstream repository/license; retain original authorship and notices. The current contribution-idea template recommends prior discussion, and PR template requires an associated contribution Issue. No such contact or port was made.
2. Handler policy/identity/preservation repairs may be reusable where upstream supports the exact expanded format, but depend on CFRU/DPE detection, constants and guarded serializers. Separate generic fixes from target-specific support before any proposal; vanilla regression evidence and author attribution are required. Do not submit the full fork as one change.
3. CFRU QoL/ABI repairs and Tracker lifecycle/decoder contracts have different owners and configuration assumptions. CFRU README requests credits to the respective code makers; DPE's root LICENSE is WTFPL. Neither public visibility nor a root license establishes rights to every third-party graphic, script, data source or asset. Provenance/credits and redistribution decisions remain unresolved per item; no ROM/assets were examined or prepared for distribution.

Launch remains #501-owned: exact supported U/C/I profile matrix and known limits; pinned setup/host/core/Lua instructions; trustworthy runner/JUnit evidence rules; user-owned input workflow and reproducibility; credits/rights inventory; sanitized issue-report template; rollback to exact supported source and controlled profile changes. Gate on live #499 host and #500 consumer/lifecycle acceptance before claiming Tracker support, then explicit freeze review. No public announcement, tag, release, distribution or upstream branch is part of #705.

## 8. Change boundary and verification

Only this report and its TSV are authorized changes. Safety check passed before changes; the pre-existing untracked `CASUAL_NATDEX.rnqs` was neither read nor staged. No protected inputs, real local manifests, offsets.ini, binaries, ROMs/saves/states, builds or secrets were read. No Java/C compilation, generation or emulator operation occurred.

Handoff verification checks the exact two-path diff, `git diff --check`, all ten unchanged Gitlinks/checkouts and `check_git_safety.py`; relevant Python source/mocked checks are repeated against the final report commit. Lua results bind to W's unchanged implementation/test bytes. The final commit hash and PR are reported in the PR/handoff rather than inserted self-referentially into this file. CONTROL reviews; user merges. No automatic Issue closure and no merge.
