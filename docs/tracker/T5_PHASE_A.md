# T5 #694 — Mac-first detached UI confidence projection

Contract: [Workspace #694](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/694),
Mac-first Phase A only, as authorized by CONTROL on 2026-10-08. Fresh session
and branch `feature/694-source-ui-confidence-mock` start at accepted main
`ed38910a7931855e1fad6aa871e1931a26fed659`, tree
`88c9e5d33dae77df77ae2c0d761135dd03a800a1`. Remote main and checkout pins were
checked before changes. The earlier local #693 branch had the identical tree;
this branch starts from the accepted merge, not that candidate commit.

Review target: `IRONMON_TRACKER_UI_CONFIDENCE_MOCK_READY`.
**NOT_ESTABLISHED pending CONTROL review/acceptance.** Execution evidence below
supports a Phase A candidate only. It does not establish
`IRONMON_TRACKER_CFRUDPE_UI_READY`, a working Tracker screen, extension API
sufficiency, complete consumer coverage or BizHawk compatibility. #694 stays open.

## Inspected source / consumer and side-effect matrix

All Tracker observations below refer to the checked-out read-only v9.3.1 pin
`c450ecaee2d8131a2789bb656e3be792a93712fb`, not upstream latest. Paths are
relative to `02_external/Ironmon-Tracker/ironmon_tracker/`; line locators are
bound to that pin. This is a focused inventory of checked entry points, not an
exhaustive screen/plugin/network audit. Future replacement/gating remains a
Phase B proposal; no wrapper or host mutation is installed here.

| Checked entry point | Actual consumer / side effect and stock hazard | Future CFRU/DPE seam / required gate |
| --- | --- | --- |
| `Program.lua:827`, `updatePokemonTeams` | Reads both parties; identifies occupied rows through personality/OT, calls `readNewPokemon`, `validPokemonData`, verifies player data, calculates experience, assigns `GameData.PlayerTeam/EnemyTeam`. Invalid nonempty reads skip assignment without clearing the previous row. Outside battle, enemy PP is replaced with `MoveData.Moves[id].pp` at line 866. Lead updates can add GachaMons. | Guard before stock reads and side effects; replace with validated direct-layout snapshots and explicit count. Clear failures transactionally; no synthesized enemy PP, experience or downstream persistence from an unknown sample. Post-read hooks alone are too late. |
| `Program.lua:888`, `readNewPokemon` | Uses personality/OT XOR and `%24` shuffled 12-byte substructures; stock ability bit, freeze/status map, nature, IV/EV fields and neutral stages enter `DefaultPokemon`. CFRU direct layout and FROSTBITE differ. | T3 direct CFRU decoder; only separately verified fields. Defaults/zero/stage=6 cannot stand in for unknown data. Party ability needs effective assignments and `GetMonAbility/TryRandomizeAbility`, not the stock two-slot selector. |
| `Battle.lua:116/202/208/269`, `update`, high/low updates, `updateViewSlots`; `Combatants` | Update hooks run after stock battle consumers. Index reads at 276–290 use **u8** at offsets 0/2/4/6; invalid indices become plausible slots 1/2. CFRU declares **u16[]**. Update paths track moves/abilities/encounters, stages and lookup values. | T4 u16 mapping, positions/side/count/u32 flags and same-epoch checks before any read/track operation. Singles only until wider ownership is proven; never clamp failed mapping into a real slot. |
| `Battle.lua:739/812/960`, `beginNewBattle`, `endCurrentBattle`, `populateBattlePartyObject` | Begin reads flags/trainer A, initializes slot defaults, calls the host's temporary-save-state helper and copies party moves/stock-selected abilities into `BattleParties`; ends clear that table, reset party stages, clear details and schedule saving. Dynamic ability tracking subsequently modifies these objects. | Separate active `gBattleMons` values from party values; invalidate on begin/end/switch/reset before drawing or tracking. Exclude memory/state-writing host helpers from the later read-only acceptance path. Mock never calls these functions. |
| `Tracker.lua:105/144`, `getPokemon/getViewedPokemon`; `Battle.lua:257`, `getViewedPokemon` | Return shared `Program.GameData` party objects; personality/OT checks, egg search and Ghost dummy can change the selected object. Viewed slots come from `Combatants`. | Return only current gated view identities; preserve explicit party-vs-active ownership and unknown/unsupported selection. Do not select another plausible Pokémon as recovery for an unknown reader. |
| `TrackerAPI.lua:28/38/47`, player/enemy/active endpoints | Active API returns party objects selected by `Combatants`, not a new `BattlePokemon` read. | Gate/replace through supported API or reversible owned wrappers after predecessor acceptance; returning a valid party table does not prove an active battle sample. |
| `TrackerAPI.lua:64/73/134/141/245/253/261/300` | Ability endpoint delegates to `PokemonData.getAbilityId`; types delegates to stock two-type memory reads in `Program.lua:1356`. Trainer ID reads A directly, trainer data delegates to static reader. Info endpoints copy global species/move/ability tables; item name uses host catalog. | Each endpoint needs independent identity/context/field gates, mapped source catalog labels and effective-data distinction. Trainer context is not constructed enemy-party truth; type3 and contextual ability naming are separate capabilities. |
| `Program.lua:1020`, `readTrainerGameData` | Reads trainer header/class/name/items and static party shapes based on flags; FRLG Rival name additionally follows a save-block path. | Source-correct layout/table/output binding for headers; gate static predictions, class/name, Rival/save dependencies separately. `gEnemyParty` and `gBattleMons` own actual created/current teams. Mock exposes only T4 trusted synthetic trainer-A ID, no name/class/team prediction; B unsupported. |
| `TrackerScreen.lua:1102/1127/1361/1454`, screen/info/stats/moves | `drawScreen` uses **`DataHelper.buildTrackerScreenDisplay`**, not just `Tracker.getViewedPokemon`. Draw paths display types, stats, ability lines, category icons and move PP; buttons at 280/306 select stock or tracked abilities. Carousel and note pad use prior moves/notes/abilities. | Gate the display builder, buttons, carousel and data-dependent draw paths. A gated API getter alone cannot prove these consumers safe. No rendering code is executed in Phase A. |
| `data/DataHelper.lua:124`, `buildTrackerScreenDisplay`; info builders at 414/480/539 | Uses `Battle.getViewedPokemon`, defaults for missing/map/summary state, species baseline BST/evolution/stats, experience 0/100, friendship defaults, neutral stages, stock or persisted abilities/moves. Copies `MoveData.Moves`, adjusts Hidden Power/variable damage, STAB and PP. Calculates catch rate; info pages also read baseline and notes. | Per-field presentation and dependency gates, including types, effective move properties and persisted consumer paths. Option-based spoiler hiding/randomization heuristics are not confidence proof. Unknown values must not reach any calculation or regain defaults on another view. |
| `data/PokemonData.lua:234/293/438/557/602/706` | Builds `gBaseStats`-derived BST/two types/two abilities; stock randomization probes drive reveal rules. `getAbilityId` returns a baseline assignment or 0. Type effectiveness, catch-rate and learnset consumers have Gen3 tables/formulas/layouts. | Explicit CFRU/DPE mapping, third/hidden ability and source configuration; effective randomized table validation separate from source baseline. Gate BST, types, mechanics/catch/learnsets until individually proved. A form name does not certify form mechanics. |
| `data/MoveData.lua:310/341/364/496/509/547/591` | Static Gen3 catalog remains when not detected randomized. Reader interprets category bits from a selected flags byte; rebuild can derive category from type. Expected-power/Hidden Power/variable functions use baseline assumptions. | Effective CFRU 12-byte `BattleMove.split` byte at 0x0A, independent of vanilla type category. No source power/PP/category promoted to randomized truth; withhold dependent damage/STAB/coverage when inputs or semantics are unproved. |
| `data/AbilityData.lua:32/51/82` | Resource names/descriptions overwrite static catalog; `buildData` does no effective runtime rebuilding. Defensive ability list supplies type-calculation assumptions. | Gate selected contextual name and mechanics separately from source ID mapping. Catalog names/descriptions/assignments cannot prove active name/behavior. |
| `screens/BattleDetailsScreen.lua:458/489/573`, `GameFuncs.read*` at 730–1695 | Direct memory consumers for terrain/weather/field effects/status2/status3/side/disable/wish structs; summary picks first stored detail and uses static names/tracked abilities. Does not obtain everything from TrackerAPI. | Gate the entire unsupported reader/summary surface and clear built data on invalidation. T4 opaque status2 is not interpreted status2/status3/counter/cross-battler semantics. All battle details deliberately unavailable in this mock. |
| `Tracker.lua:161/172/209/317/387/402/488/583/612/632/760`, tracked data, battle notes, save/load/autosave; `FileManager.lua:833/856` | Species-keyed observations/notes/moves/abilities persist in `Tracker.Data`; save serializes it. Load restores matching-schema keys after ROM-hash comparison; explicit overwrite bypasses hash mismatch. Battle notes also cache moves by level. Display builders consume these later. | Keep user notes conceptually separate from verified current fields; no restored/observed data substitutes for unknown current sample. Future observation writes require provenance/output/session gates and safe load handling. Phase A has no persistence input/output; local traps forbid calls/mutations. |

Linked pinned-source entry points:
[Program](../../02_external/Ironmon-Tracker/ironmon_tracker/Program.lua),
[Battle](../../02_external/Ironmon-Tracker/ironmon_tracker/Battle.lua),
[Tracker](../../02_external/Ironmon-Tracker/ironmon_tracker/Tracker.lua),
[TrackerAPI](../../02_external/Ironmon-Tracker/ironmon_tracker/TrackerAPI.lua),
[TrackerScreen](../../02_external/Ironmon-Tracker/ironmon_tracker/screens/TrackerScreen.lua),
[DataHelper](../../02_external/Ironmon-Tracker/ironmon_tracker/data/DataHelper.lua),
[BattleDetailsScreen](../../02_external/Ironmon-Tracker/ironmon_tracker/screens/BattleDetailsScreen.lua).

## Detached projection / trust boundary

[source_ui_projection.lua](../../03_tools/tracker-extensions/CFRUDPEExtension/source_ui_projection.lua)
creates **one inert view model**, never a host-compatible `DefaultPokemon`, screen,
TrackerAPI override or extension hook. `newMock(publicJson, publicSourceTexts,
publicMultiText)` constructs the unchanged accepted T3/T4 decoders internally.
Only their results enter the positive projection path; callers cannot supply
callbacks, preverified field objects or profile objects to authorize a value.
Missing/altered source evidence rejects construction. The T3 exact serialization
lock still binds every source pin/schema/configuration/layout/input fact:

- Public JSON SHA-256: `8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981`.
- Profile ID: `sha256:31be9e07697f939b274c56eea5d92a81dd10c43e7c876586effccb335535ca75`.
- CFRU `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2`, DPE `d887185de1f6ae6a78e85c4311bbadde17041d00`, UPR-FVX `4670a5413104ec02bc08c09ff584470a8a6cb7bd`.
- Tracker pin above; NatDexExtension `a94b8844800308248bb5090b6c36c8b2d7e5d7b9`.

The runner uses exactly the five allowlisted public T3 source texts plus T4's
`CFRU:include/new/multi.h`, retrieved through existing `LockedSources`. No new
profile/schema/generated source data or local address/input file is created.

`transition(event, proof)` clears the current projection and retires its epoch
**before** considering proof. Only `start/switch/session/output` plus a fresh
plain-table `SYNTHETIC_ONLY` proof arm decoding. Proof requires exact profile ID,
`trusted=true`, new projection epoch, bounded synthetic output/session/roster
tokens and a battle token or explicit `false` outside battle. Returned projection
and T4 epochs let fixtures build fresh samples. This is a fixture declaration,
not loaded-output/session/runtime acceptance. `end/reset/error` and unknown
events stay disarmed. Same-species replacements require an explicit transition
and changed roster declaration; live detection is unproved.

`decodeMock(sample)` accepts matching before/after proof, increasing integer
`sampleId`, optional `{bytes,count}` player/enemy parties and a T4 battle sample.
Parties are synthetic 600-byte strings only. Enemy party requires a supported
battle context; its projected T3 fields do not establish live enemy-party fidelity.
Battle sample output/battle/T4 epoch must match the projection binding; the
unchanged T4 decoder gates flags/count/positions/u16 indices/trainer/PP caps and
before/after context. Missing party rows are never borrowed from previous values.
Roster IDs and active species changes without a transition retire the epoch;
ordinary HP updates can advance the sample within one coherent epoch.

Malformed blocks/counts, context drift, replays, cross-output results and thrown
decoder errors clear current values and revoke the binding. Fresh proof is
required to recover. Supported T4 singles are wild/trainer only. Its declared
double/multi contexts clear all prior teams and expose unavailable active context;
unknown flags expose unknown context. No unsupported mode becomes supported.

Snapshots are deep copies. Old returned copies are historical samples carrying
their old epoch, never current screen state. There is no external sink callback;
tests use local tables only. Host/global tables, notes, saves, stock defaults,
preverified field tables, cycles in forbidden inputs and table metatables cannot
enter the allowlisted positive path. No real `Tracker.Data` is accessed/mutated.

## Field and dependency policy

Every projected confidence field (including nested source-baseline fields) has
a reason, exact profile, current projection epoch, scope and `TEST_ONLY` label.
**Production/live confidence is always `UNKNOWN`.**

| Surface | Projection policy |
| --- | --- |
| Player/enemy party and active battle | Separate objects; never use party HP/moves/items as active fallback. Species prerequisite gates dependent fields. Empty slots retain verified absence/occupancy and unavailable dependent fields. Eggs' display dependents are deliberately unavailable. |
| Species/move/type/item mapping | Synthetic ID uses exact source mapping; names are explicitly source-baseline identity labels, preserving aliases/internal forms/truncation. Unsupported/unknown mapping yields no value; invalid move only removes that move's dependents, not independently verified HP. |
| HP/level/status | Validated direct T3/T4 fields only. Derived HP percentage requires both HP and maxHP from that same current row; no baseline stats or old values. FROSTBITE uses locked CFRU configuration. |
| Ability | Party selection remains unknown. Active ID can be synthetically verified; its display object intentionally contains ID/absence only, never a catalog name. Contextual `abilityName` always unknown. Source-baseline assignments stay in the separate baseline field. |
| Move PP/effective calculations | T3 stored current PP is labeled as stored current PP with unproved cap. T4 current PP requires its explicit same-epoch synthetic cap. Maximum PP always unknown; no source maximum substitution. Effective power/category/type and dependent damage stay unknown. Coverage intentionally unavailable. |
| Types / baseline | T4 mapped three active type IDs may project; party effective types remain unknown. `sourceBaseline` remains separate and marked source-baseline, including unresolved form/effective fields. Nothing consumes it to calculate randomized values. |
| Trainer / battle details | Context and trusted synthetic A ID projected independently. Missing/untrusted A unknown; wild/outside A and singles B unavailable. No class/name/static trainer team. Opaque secondary status does not authorize a details interpretation; details are unavailable. |
| Notes/save | Explicitly unavailable; never read, imported, written or used as confidence evidence. No persistence recovery path. |

## Execution and safety evidence

Use the existing `/opt/homebrew/bin/lua5.4` (Lua 5.4.9); no install or host setup.
The following commands are required again **after the final commit**; the PR
records the exact delivered commit and post-commit execution results.

```sh
python3 07_scripts/tracker/run_cfru_dpe_ui_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 07_scripts/tracker/run_cfru_dpe_battle_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 07_scripts/tracker/run_cfru_dpe_party_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 07_scripts/tracker/run_cfru_dpe_extension_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 -m unittest discover -s 07_scripts/tracker -p 'test_*.py' -v
python3 07_scripts/tracker/generate_cfru_dpe_source_data.py --check
python3 07_scripts/bootstrap/check_git_safety.py
git diff --check
```

| Check | Candidate result (exact post-commit evidence in PR) |
| --- | --- |
| T5 Lua 5.4 projection/confidence/lifecycle fixtures | PASS — 63/63 |
| T4 / T3 / T2 Lua regression suites | PASS — 76/76, 43/43, 55/55 |
| Full T1–T5 Python discovery / isolation | PASS — 43/43 (40 prior + 3 new) |
| New Python compilation without emitted bytecode | PASS — 2 files |
| T1 profile `--check` | PASS — byte-identical |
| Git safety / whitespace / explicit paths / Gitlinks / immutable boundaries | PASS; exact revision and post-commit rerun in PR |
| Lua 5.1 | NOT_RUN; no compatibility claim |
| Real Tracker UI/API, emulator memory, production activation, Linux/BizHawk | NOT_RUN / PENDING_LINUX_HOST; activation DENIED |

Tests cover Gen1/Gen8/Gen9/regional identities, 1-/6-slot parties, wild/trainer,
unsupported contexts, invalid IDs, independent item/PP/ability failures, HP
dependencies, source evidence corruption, identity/session/output/epoch drift,
replays, immediate clearing, alias contamination and persistence/default traps.
Python source checks lock unchanged production/T1/T3/T4 bytes and Gitlinks and
check the detached module/runner's source isolation. Traps detect forbidden mock
host/notes/persistence/memory calls; the negative write injection raises, while
ordinary projection uses zero host calls. This proves only these mock behaviors,
not the normal Tracker's real side-effect coverage.

No executed check failed. `FAIL: none` does not turn any `NOT_RUN` gate into PASS.

`CFRUDPEExtension.lua` (including its production-denied early guard),
`profile_sha256.lua`, T1 generator/public profile, T3/T4 decoders and all component
source/Gitlinks are unchanged. No ROM/save/state/build/tool binary/private
manifest/`offsets.ini`/secret was inspected. Known untracked `CASUAL_NATDEX.rnqs`
remains untouched and unstaged. No engine, randomizer, T6, live UI or production
extension work occurs; #689/#499 and #691–#693 live gates remain open.

Next: CONTROL reviews the PR's exact commit, consumer matrix and post-commit
synthetic evidence for Phase A marker acceptance; user merge remains separate.
