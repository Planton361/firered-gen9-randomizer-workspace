# M-014 R0 final ROM scope — exact-basis reconciliation

**Workspace Issue:** [#563](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/563) · **Parent:** [#498](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498) · **Date:** 2026-09-29<br>
**Verdict:** `ROM_SCOPE_READY_FOR_ACCEPTANCE`<br>
**Evidence level:** current pinned source/repository and ROM-free host checks. This is not ROM runtime acceptance or `ROM_PROFILE_READY`.

## Exact source basis and method

| Repository | Exact checked-out revision |
| --- | --- |
| Workspace `main` / R1 source-test basis | `b20454789e375383eb852d749c0357d58af461dc` |
| CFRU | `8af56bc2fb71a6a392d7e79d3a22732a4de4fae6` |
| DPE Gen 9 | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX, compatibility boundary; final output acceptance remains R2 | `7bf79ee1e7c46c972f7a9c84942970a950be0723` |
| Ironmon Tracker reference | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| NatDexExtension reference | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| Workspace-pinned Cyan FireRed NatDex reference | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| Current public NatDex behavior reference used by #537/#558 | `CyanSMP64/pokefirered@b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7` |
| Workspace-pinned pret FireRed reference | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |

The separate GitHub-reconstructed checkout was clean at the exact Workspace base before branching. Recursive Gitlink inspection also found the unchanged UPR-ZX NatDex, UPR-FVX upstream, and ajarmar reference pins. Branch `audit/563-m014-r0-final-scope` was created at that base; the only Workspace change for this report is this file. The earlier dirty local checkout was left untouched and its local changes remain UNKNOWN. GitHub Project #563 is `P0 / Verification / Doing`; #498 remains `P0 / Runtime Acceptance / Blocked`.

All accepted CFRU source commits for M-001 through M-009 and M-013 were checked as ancestors of the current CFRU pin. The [original #498 R0 audit](rom-finish-readiness-2026-09-20.md) and the [#537 merged audit](rom-qol-finish-refresh-2026-09-28.md) are revision-bound inputs. Current source at the pins above, [#535](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/535), [#538/#539](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/539), [#545](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/545), [#549/#551](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/551), [#550/#553](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/553), [#557/#559](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/559), [#558](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/558), and [#547/#561](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/561) supply the accepted later decisions. The [current A–G package](../testing/feature-complete-acceptance.md) is a supporting test plan, not a final runtime result.

## Current-pin source proof

| Boundary | Direct source finding |
| --- | --- |
| Data and owner continuity | DPE `include/species.h` reaches `SPECIES_PECHARUNT=0x59F` and `NUM_SPECIES`; DPE `src/Base_Stats.c` and `src/Learnsets.c` remain at the accepted pin. CFRU `src/Tables/level_up_learnsets.c` remains unchanged from the pre-#538 accepted owner. The coherent-learnset host audit passed 144,000 initial-moveset cases and its exact table/pointer contract. |
| Early Running | CFRU `src/save.c:506-514` invokes `ApplyFreshNewGameSettings()` after new-save wipe; `src/settings.c:117-132` sets `FLAG_RUNNING_ENABLED` while leaving `FLAG_AUTO_RUN` alone. `src/read_keys.c:233-248` still gates L-toggle; `src/overworld.c:1749-1780` retains B/Auto-Run and terrain/run restrictions. `mapobjectoverlays:67-76` has the exact Pewter Aide and three CoordEvent script-pointer replacements. |
| Normal National Dex handoff | CFRU `assembly/overworld_scripts/shortened_oak_parcel_flow.s:99-107` contains exactly one `SPECIAL_ENABLE_NATIONAL_POKEDEX` call after Parcel removal, ordinary Pokédex flag and unlock special, before five Poké Balls. Named special `0x016F` calls FireRed's `EnableNationalPokedex()`: pret `data/specials.inc:378`, `src/event_data.c:99-105` prove the magic `0xB9`, var `0x6258`, and national flag are set together. CFRU Fresh-New-Game paths contain no activation; the #549 audit's source assertions passed before its historical changed-path guard. |
| UPR-FVX National Dex guard | `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java:8394-8396` omits `NATIONAL_DEX_AT_START` from availability for detected CFRU/DPE Gen-9 BPRE. `:8431-8436` returns before the generic patch on a stale/direct request; vanilla FRLG still reaches `patchForNationalDex()`. The accepted #553 synthetic 30/30 evidence remains revision-bound and its guard source is at the current pin. |
| Route 10 HM05 | CFRU `mapobjectoverlays:137-141` has exactly one `append_object_exact 3 28 10 5 0 8` row: Hiker local ID 11, graphics `0x38`, `(17,22)`, `FLAG_GOT_HM05`. `assembly/overworld_scripts/route10_hm05.s:14-36` checks shared flag and bag space, awards item 343 once, sets flag and removes object. The pret Route 2 Aide script still awards HM05 under the same flag; five current functional synthetic Route 10 checks passed. The accepted #557 map-event/object-table repoint is a known layout delta, not a new #563 migration. |
| Settings, raw values and dispatch | CFRU `strings/option_menu.string:70-117` and `src/option_menu.c:276-303` show `Auto (Diff.)` only on Trainer Scaling raw 0 and Trainer AI raw 0; Hard Cap keeps `Auto`. Explicit AI choices are `Legacy Vanil.`, `Legacy Easy`, `Legacy Normal`, `Legacy Hard`, `Legacy Expert`, `Legacy Smart`, then unchanged `Standard` and `Ironmon Smart`. `src/settings.c:1-132` and `src/util.c:155-197` retain raw/fallback and default/preset mappings; `src/Battle_AI/ai_standard.c:1200-1218` and `ai_ironmon.c:674-691` keep distinct ordinary Trainer Single dispatch. Raw unknown/original-raw/dirty preservation passed host tests. `Legacy Vanil.` measures 73/78 px; Page 3 help ends at 228/240 px. |
| HM and Move Reminder | `src/config.h:265` retains `ONLY_CHECK_ITEM_FOR_HM_USAGE`; `src/overworld.c:2397-2432` requires item and a non-egg compatible/knowing party Pokémon, with field badge/location gates such as Flash and Surf still present. The pret and current public NatDex `data/maps/TwoIsland_House/map.json` and `scripts.inc` retain `MoveManiac` and the one Big Mushroom / two Tiny Mushrooms price. The public NatDex `CeladonCity_House2` object exists but `CeladonCity/map.json` has no entrance warp to House2; #558 resolved it as unreachable early Celadon. |
| Later integration ownership | CFRU ancestry from Early Running merge `11bd0bd…` to `8af56bc…` comprises #542 build/check tooling, #549 handoff, #557 Route 10, and #547 Options presentation. Exact range diff is quiet for `src/Battle_AI/`, `src/battle_controller_opponent.c`, `src/util.c`, `src/settings.c`, `src/save.c`, `src/Tables/level_up_learnsets.c`, `src/hidden_item_sparkle.c`, `src/m009_overworld_frame.c`, and `src/item.c`. DPE remains the same pin. UPR-FVX changed exactly its Gen3 handler and focused guard test from its prior pin. No unreviewed AI/data/QoL owner was found. |

## #498 R0 classification matrix

One classification applies to each row. “Needs runtime acceptance” means the source contract is present but the final continuous R1 run at this exact basis has not passed. Earlier milestone and D01/D02 runtime results do not supply that pass.

| Area | Current integrated disposition | R0 class |
| --- | --- | --- |
| Gen 1–9 species IDs, Base Stats and selected data profile | DPE and CFRU tables present; representative summary/battle/save behavior belongs to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Coherent level-up learnsets and supported form pointers | Exact current host audit passes; start/level-up/Reminder persistence belongs to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Ability names/assignments and selected existing engine effects | Data is present; supported representative effects belong to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Open-risk forms, Ally Switch-blocked tables, blocked ability behavior and sentinels | Explicit safe representation/profile limits from the accepted data audit; no universal mechanic claim. | `INTENTIONAL_DIFFERENCE` |
| Selected CFRU/DPE engine boundary | Existing expansion, Mega/Dynamax/Terastal features remain; test only supported profile cases. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-010 compatibility audit | Accepted engine/data boundary and excluded-case decision remain present. | `REQUIRED_PRESENT` |
| M-011 Hospitality; Commander; Embody Aspect; missing Gen-9 mechanics | No new implementation is authorized in the pilot. | `OUT_OF_PILOT` |
| New Terastal/form-transition systems solely for parity | Existing CFRU Terastal feature is not a promise of new universal Gen-9 transitions. | `OUT_OF_PILOT` |
| Standard Trainer AI and Ironmon Smart | Distinct appended raw profiles, ordinary Trainer Single gates, legacy fallback and accepted fairness/policy host tests remain; final gameplay acceptance belongs to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Fresh New Game, Ironmon preset, Difficulty/Trainer/Wild Scaling separation | Fresh raw `4/1/0/7`; preset `4/1/0/8`; raw 0 legacy fallback and unknown preservation unchanged. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Settings UX | `Auto (Diff.)` only on two Difficulty-derived rows; Hard Cap `Auto`; accepted Legacy/Standard/Ironmon labels and geometry intact. Visual save/reload check belongs to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Early Running and post-Brock Aide | Fresh running flag, separate Auto-Run, restrictions and exact short non-gating Pewter cleanup remain. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-001 gold TM/HM Item Balls | Accepted 29-target overlay graphics remains; no broad Item Ball recolor. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-002 Viridian Forest Nurse | Exact overlay remains; service/poison restrictions belong to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-003 instant ordinary-Center healing | Overlay self-check passes; Trainer Tower exclusion stays intentional. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-004 guaranteed renewable step items | Current source-table check passes; Mt. Moon boundary remains. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-005 empty initial PC / Lab Potion | Current overlay and new-game path remain; duplicate protection belongs to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-006 Mom, Lab, naming, starter and Rival handoff | Accepted shortened but stateful opening flow remains; no fixed-name/gender skip. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-007 Route 1 Parcel, normal Pokédex, Old-Man bypass | Exact current overlay check passes; full flow including new National-Dex timing belongs to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-008 optional Bill/Sevii handoff | Automatic Cinnabar scene bypass and interactive Center Bill path remain. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-009 eligible hidden-item sparkle | Accepted always-on frame/scanner owner remains; lifecycle and visual check belongs to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-012 QoL audit and accepted retained CFRU services | Decision matrix remains an audit, not a new implementation requirement. | `REQUIRED_PRESENT` |
| M-013 ordinary-shop Premier Ball bonus | Current callback and 11,110-case ROM-free host check pass; shop behavior belongs to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Existing 19-Center Name Rater rollout | Accepted Center service remains; service UI belongs to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Repel reuse, indoor run, L Auto-Run, reusable TMs, forgettable HMs, Select-from-PC capability and party Move Items | CFRU defines and source paths remain; Select-from-PC is service-specific, not universal UI. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| HM field-use eligibility | HM item, compatible non-egg party member, badge and location remain required. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| NatDex modern Start-menu HM/no-compatible-party model | This would replace the accepted HM challenge rule. | `INTENTIONAL_DIFFERENCE` |
| Route 10 HM05 and original Route 2 Aide | Exact one-object append and shared reward flag are present; no double reward is claimed without R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| National Dex at normal Pokédex handoff | Full BPRE special at the single M-007 handoff, not Fresh New Game; actual activation/persistence belongs to R1. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| National Dex at Fresh New Game | Later normal-Dex handoff is the accepted timing. | `INTENTIONAL_DIFFERENCE` |
| UPR-FVX National-Dex-at-start availability and stale/direct-request guard | Both checks are integrated at exact pin; final Randomizer/output behavior remains R2. | `REQUIRED_PRESENT` |
| Two Island Move Maniac | Original source-present pilot service and mushroom price retained; R1 service check applies. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Early Celadon Move Reminder | Current NatDex House2 is not normally reachable; #558 accepted holding this placement. | `INTENTIONAL_DIFFERENCE` |
| Cinnabar duplicate Reminder and Celadon Restaurant retarget | Alternative paid-service placement requires a later product decision. | `OPTIONAL_BACKLOG` |
| Text Speed Slow / Mid / Fast | Current Options table is the accepted state; `INSTANT` string elsewhere is not a selected fourth option. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Blanket Instant Text or full fixed-name Professor skip | Current bounded pacing preserves naming and Slow/Mid/Fast choices. | `INTENTIONAL_DIFFERENCE` |
| Generic mandatory-dialogue/tutorial shortening | No source-proven specific remaining mandatory delay; future targeted polish is secondary. | `OPTIONAL_BACKLOG` |
| Pickup activation sound and faster fishing | #537 retained both as secondary choices, with no required defect. | `OPTIONAL_BACKLOG` |
| Optional sparkle toggle, global BGM Off, Portable PC expansion, Friendship Boost | Held #537 QoL candidates; accepted M-009 sparkle remains always on. | `OPTIONAL_BACKLOG` |
| Bag-capacity expansion and broader Itemfinder/Item Ball visuals | No finish-blocking capacity or visual defect was established. | `OPTIONAL_BACKLOG` |
| Randomizer R2, BizHawk #499, Tracker #500, upstream contribution | Separate downstream contracts; `UPSTREAM_CONTRIBUTION = DEFERRED`. | `OUT_OF_PILOT` |
| Save/ABI/struct/layout migration from late integrations | No new SaveBlock or AI/data ABI change in the #538→current source range; #557's reviewed Route 10 MapEvents/object repoint remains the known layout delta. | `REQUIRED_PRESENT` |

**Blocker inventory:** `MISSING_BLOCKER = 0`; `UNKNOWN_BLOCKER = 0`. No protected-input test is used to erase or downgrade a source blocker.

## #536 legacy audit reconciliation

[#536](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/536) is **LEGACY / OBSOLETE**, not another active blocker queue. Its provisional Instant Text `REQUIRED_POLISH` was superseded by the accepted #537 Slow/Mid/Fast `KEEP_AS_IS` decision; the current Options source confirms that menu state. Its generic dialogue/pacing ideas became #537 retained flow or optional targeted shortening. Pickup sound, faster fishing and optional sparkle toggling became optional; accepted M-009 visible sparkle remains present. Its actual required follow-ups were resolved through bounded Early Running #538/#539, National Dex #545/#549/#551 plus UPR guard #550/#553, Route 10 #557/#559, Settings #547/#561, and the #558 Move Reminder correction. The #537 report's earlier “reachable Celadon House2” inference is itself superseded by #558: registered object, no normal entrance warp. That correction makes early Celadon an accepted intentional difference, not an unimplemented required item.

## ROM-free gates at the current pin

All CFRU commands below ran at `8af56bc2fb71a6a392d7e79d3a22732a4de4fae6`. No ROM, insertion input, emulator, randomizer output or protected build was used.

| Command | Exact result |
| --- | --- |
| `python3 scripts/tests/test_settings_legacy_ux.py` | PASS; widths: Auto (Diff.) 64/78, Legacy Vanil. 73/78, Easy 65/78, Normal 76/78, Hard 65/78, Expert 76/78, Smart 70/78, Standard 45/78, Ironmon Smart 73/78 px; Page 3 help 187 px at x=41, end 228/240. |
| `python3 scripts/tests/run_settings_defaults_tests.py` | PASS; Difficulty 0–4, Trainer AI 0–8, raw 0, unknown/original-raw/dirty preservation; Fresh `4/1/0/7`, preset `4/1/0/8`; temporary host objects deleted. |
| `python3 scripts/tests/run_standard_ai_tests.py` | PASS; 4,096 Standard production pairs and 1,024 Ironmon pairs with 0 mismatches, 98,304 damage-envelope cases, dispatch/legacy, layout and save-delta checks. |
| `python3 scripts/tests/run_ironmon_ai_tests.py` | PASS; 63/63 parity fixtures, 58/58 mandatory tags and unchanged accepted policy digests; temporary host objects deleted. |
| `python3 scripts/tests/run_early_running_pewter_tests.py` | PASS; Fresh running lifecycle, Pewter and related map-overlay self-checks. |
| `python3 scripts/insert.py --check-map-object-overlays` | PASS; source/synthetic overlays only, including Parcel/Pewter; no ROM insertion. |
| `python3 scripts/check_coherent_learnsets.py` | PASS; 144,000 initial-moveset cases, 820 exact replacements, two new form tables, seven rebindings, 27 reserved sentinels, negative mutations. |
| `python3 scripts/check_premier_bonus.py` | PASS; 11,110 ball cases plus capacity, failure and non-ball controls. |
| `python3 scripts/check_renewable_hidden_items.py` | PASS; source-table contract. |
| Five `Route10HM05Tests` selected with `python3 -m unittest`: source identity/counts; exact append; wrong-count fail closed; invalid/truncated table fail closed; invalid preserved pointers fail closed | PASS, 5 tests, 0 failures. |
| `python3 scripts/tests/audit_m007_national_dex_handoff.py` | Source assertions passed through its final guard, then exit 1: the #549-only exact-changed-file guard sees later accepted #557/#547 paths. It is historical scope validation, not a current-pin 6/6 claim or a National-Dex source defect; guard unchanged. Current source order and overlay self-check above supply current-pin proof. |

The source-only audit did not run `scripts/build.py`, the UPR Gradle suite, a ROM insertion, or R1. Earlier #551/#553/#559/#561 build and host results remain revision-bound supporting evidence.

## R1 handoff and non-claims

Use Workspace source/test revision `b20454789e375383eb852d749c0357d58af461dc`, CFRU `8af56bc2fb71a6a392d7e79d3a22732a4de4fae6`, DPE `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`, and UPR-FVX boundary pin `7bf79ee1e7c46c972f7a9c84942970a950be0723`. The audit commit is provenance only and does not change this source/test basis. Before private R1, update the user-owned/sanitized run identity and package expectations to these revisions. In particular, old A12 wording about “no accidental early National Dex policy change” must now assert full National Dex **at** the normal Pokédex handoff, never at Fresh New Game.

**Recommendation:** restart the final continuous R1 run from a genuine Fresh New Game on this exact basis. Earlier D01/D02 and other runtime evidence remain historical/revision-bound; none is promoted to a final-pin PASS or substituted for continuous D01–D16. Keep the existing R1 A–G and ordinary-shop Premier matrix; R2-owned H/B18/randomized-shop cases remain gated by `ROM_PROFILE_READY`.

Add these minimum targeted user-owned runtime observations to the final R1 plan:

1. **Settings UX:** inspect Page 3 cycling for full readable labels/help without clipping or stale pixels; verify `Auto (Diff.)` only on Trainer Scaling and Trainer AI raw 0, Hard Cap `Auto`, all Legacy labels, unchanged Standard/Ironmon Smart, independent scaling/Difficulty/AI choices, and save/reload/original-raw behavior.
2. **Route 10 HM05:** encounter the Hiker at `(17,22)` before Rock Tunnel; test no-room/retry, one HM05 award, shared flag persistence and absence after re-entry/reload, original Route 2 Aide non-duplication, and separate HM item/compatible party/badge/location field-use gates.
3. **National Dex:** verify no national state at Fresh New Game or before Parcel; at the one normal Pokédex handoff verify full national view/registration behavior and five-ball accounting, then save/reload and revisit for persistence and no duplicate award/script. Keep UPR stale/direct-request output protection for R2, not as an R1 ROM claim.

This report does not claim runtime visuals, private ROM insertion, full build at this audit pin, final save compatibility in play, R1 completion, `ROM_PROFILE_READY`, Randomizer R2, BizHawk, Tracker, or a merged PR. No ROM, save, emulator state, generated build, tool binary, screenshot, private path/log, `.env`, token, key, or secret was read or used as agent input. No Gitlink/component/protected file was changed.
