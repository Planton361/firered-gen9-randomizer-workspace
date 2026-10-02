# M-014 final current-pin R0 source recheck — 2026-10-03

Contract: [#614](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/614).
Parent: [#498](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498).

**Verdict:** `ROM_SCOPE_READY_FOR_ACCEPTANCE`.
**Package state:** `M014_FINAL_REBASELINE_READY / ROM_RUN_PENDING`.
**Blocker inventory:** `MISSING_BLOCKER = 0`; `UNKNOWN_BLOCKER = 0`.
**Evidence classification:** CONFIRMED CURRENT STATE for pinned source and
CONFIRMED USER DECISION for selected scope; INTENDED FUTURE STATE for final
R1/R2 acceptance. No `ROM_PROFILE_READY` or `RANDOMIZER_PROFILE_READY` is claimed.

## Exact integrated basis and method

| Repository / role | Exact revision |
|---|---|
| Workspace product-source / future test basis | `1a3e73871730783f7fe2108b335e3d86f69adbe8` |
| CFRU runtime / QoL owner | `237e1dfaa785af332ddad72af906b3bba5beaab9` |
| DPE data / representation owner | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX supported-output owner; execution remains R2 | `7bf79ee1e7c46c972f7a9c84942970a950be0723` |
| Pinned pret FireRed structural reference | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |

The clean persistent checkout matched the exact Workspace base and recursive
component pins before the approved branch was created. Canonical instructions,
#614, parent #498 and relevant CONTROL comments, the
[UX decision audit](final-rom-ux-completeness-2026-10-01.md), the historical
[#563 R0 audit](m014-r0-final-rom-scope-2026-09-29.md), and both existing
acceptance documents were read. Current component source was inspected directly
at the verified pins. Git ancestry and source diffs establish continuity; old
inventory or runtime results are not promoted to current source proof.

All ten accepted CFRU implementation merges for M-001–M-009 and M-013 are
ancestors of the current pin. A source-range comparison from the #563 CFRU pin
confirmed no changes to `src/Battle_AI/`, `src/Tables/level_up_learnsets.c`,
`src/hidden_item_sparkle.c`, `src/m009_overworld_frame.c`, `src/item.c`, or
`src/renewable_hidden_items.c`. Later changed settings/save/hook/script/menu
owners were inspected rather than assumed unchanged. DPE and UPR-FVX pins
remain identical to #563. No build, production-host test, emulator or Randomizer
was executed for this source/documentation recheck.

## Current-source anchor register

C paths below refer to [CFRU at the exact current pin](https://github.com/Planton361/CFRU-expansion/tree/237e1dfaa785af332ddad72af906b3bba5beaab9),
D paths to [DPE at its exact pin](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/tree/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc),
U paths to [UPR-FVX at its exact pin](https://github.com/Planton361/upr-fvx/tree/7bf79ee1e7c46c972f7a9c84942970a950be0723),
and P paths to [pret at its pinned revision](https://github.com/pret/pokefirered/tree/e060ab955b5dc9ac1c4904c2cd141683615cf477).
They are source anchors, not generated binary or runtime observations.

| Area | Current source finding / anchor |
|---|---|
| M-001 / Center services | C `mapobjectoverlays` retains the 29 gold TM/HM graphics replacements, 19 Name Rater appends and ordinary-Center Nurse script replacements. `assembly/overworld_scripts/name_rater_pokecenter.s`, Forest Nurse and instant-Center scripts retain bounded service owners; Forest replacement remains `(29,58)`, Trainer Tower outside the ordinary-Center list. |
| M-004 | C `src/renewable_hidden_items.c`: `RENEWABLE_ITEM_STEP_LIMIT=1500`, approved Underground/Sevii groups and unchanged Mt. Moon random boundary. |
| M-005 / M-006 | C `assembly/overworld_scripts/oaks_lab_potion.s`, Player-PC initialization, `talk_to_mom.s` and `mapobjectoverlays` retain empty initial PC, one-time Potion, house exit guard, Mom warp, Oak `(6,3)`, scene-1 positioning and scene-2 starter handoff. The later Sign Lady scene write `0x4070=1` is present. |
| M-007 / Dex timing | C `shortened_oak_parcel_flow.s:95–127`: remove Parcel, ordinary Dex flag/unlock, one `SPECIAL_ENABLE_NATIONAL_POKEDEX` (`0x016F`), five balls, final story variables and hide flag. P `data/specials.inc` / `src/event_data.c:EnableNationalPokedex` establish full national state. No fresh-game activation is added. |
| M-008 | C `optional_bill_sevii.s` and conditional map-script overlay replace only outdoor automatic Bill; original Center Yes/No travel remains. |
| M-009 | C `functionrewrites:M009_OverworldBasic`, `src/m009_overworld_frame.c` retain ScriptContext → tasks → sprites → camera → Quest Log arrival → panning → OAM → palette → tiles → BG copies → sparkle scanner. `src/hidden_item_sparkle.c` retains eligibility and transient-effect ownership. |
| M-013 | C `src/item.c:1065–1080`: successful ball-pocket transaction quantity/10, capacity-reduced Premier award; other reward policy remains. No later source delta in this owner. |
| F01 / D01 | C `functionrewrites:21–22`, `BPRE.ld:Task_OakSpeech_FadeOutOak`, `src/oak_minimal_exposition.c`: wait initialization fade/text, destroy hidden intro sprite, call original FadeOutOak, zero presentation timer only. P `src/oak_speech.c` retains gender, player/rival naming/defaults/retry/cleanup; P New Game retains Trainer ID generation. Integration is CFRU #67, not a fixed-identity skip. |
| F02 | C `repoints` has three YES operands to `EventScript_ChoseStarterNoFlavor`; `starter_flavor.s` hides picture/removes selected ball then resumes original restore/award tail at `0x08169C80`. Confirmation, nickname, chosen species, Rival and story tail are retained; CFRU #68 integrated. |
| Native running / fresh defaults | C `src/save.c:NewGameWipeNewSaveData` wipes expanded save RAM; `assembly/hooks/general_hooks.s:FreshNewGameSettingsHook` calls defaults at the post-initialization site then retained avatar/playtime/script initialization. C `src/settings.c:ApplyFreshNewGameSettings` writes raw `4/1/0/7`; running uses native early-running integration, not the historical pre-init flag write. `read_keys.c` / `overworld.c` retain L Auto-Run and B walking inversion/restrictions. Pewter scene-1 cleanup stays distinct from scene-0 Gym Guide. |
| AI / Options | C `src/settings.c`, `src/util.c`, Standard/Ironmon AI owners and `strings/option_menu.string` retain independent raw settings, legacy fallback, `Auto (Diff.)` for Trainer Scaling/AI only, Hard Cap `Auto`, and distinct Standard/Ironmon choices. No one-click preset UI is required. |
| HM / Route 10 | C `src/config.h:ONLY_CHECK_ITEM_FOR_HM_USAGE`, `src/overworld.c:PartyHasMonWithFieldMovePotential` require HM item and compatible/knowing non-egg party member; field badge/location gates remain. `route10_hm05.s:14–36` checks bag space/shared `FLAG_GOT_HM05`, awards once/removes Hiker; exact append remains `(17,22)` with original Route 2 shared flag. D TM/Tutor tables supply compatibility, not a new HM menu. |
| D11 | C `src/config.h:FLAG_FAST_BATTLE_MESSAGES=0x925`; `option_menu.c:ApplyFastBattleMessagesMode`, menu load/save/input and strings expose Off/On flag state. Fresh expanded flags are wiped and defaults do not set it: fresh Off. `general_bs_commands.c:atk12_waitmessage` skips completed-message waits only after `gBattleExecBuffer==0`; existing animation-disabled pause branches also consult the flag. Text renderer is unchanged. CFRU #69 integrated. |
| D22 input | C `src/move_menu.c:CanUseBQuickRunHere`, `HandleInputChooseAction`: ordinary wild flags only, raid/special/unknown flags fail closed; B partner-cancel checked first, explicit B+A override retained, then B goes to `NORMAL_RUN`. A-on-RUN and R path still use normal Run. No escape algorithm or Shiny policy added. CFRU #70 integrated. |
| D22 hint | C `move_menu.c:HandleChooseAction` uses same eligibility predicate and keeps second-battler Back menu higher priority. `strings/move_menu_strings.string` has B glyph beside Run. `RemapBQuickRunHint` maps glyph pixels locally in window 2; shared palette entries serving PSS icons are not changed. CFRU #71 integrated. |
| D20 | C `src/scripting.c:scrB3_CheckCoins` retains `GetVarPointer(ScriptReadHalfword(ctx))`, reads u32 Coins, exports `min(coins,0xFFFF)` to u16. Full-width Get/Set/Give/Take owners remain. `REPLACE_SOME_VANILLA_SPECIALS` stays disabled; acquire images remain enabled and stale warning removed. CFRU #72 integrated. |
| DPE data | D `include/species.h:1439–1443` reaches Pecharunt `0x59F` / NUM_SPECIES; `src/Base_Stats.c`, `src/Learnsets.c`, representation/Dex/icon/cry/TM tables remain at accepted pin. C active `gLevelUpLearnsets` still includes Pecharunt and accepted coherent tables. Data assignments/names do not establish missing modern mechanics. |
| UPR profile | U `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`: detected Gen9 BPRE profile validates species/data and supported runtime learnset writer; bounded pointer/allocation errors fail safely. `rejectUnsupportedCfruDpePickup` requires Pickup Unchanged. `miscTweaksAvailable` and `applyMiscTweak` omit/ignore stale National-Dex-at-start request for this profile. |
| D07 | Same U handler `miscTweaksAvailable`, `applyMiscTweak`, `applyFastestTextPatch:8482`: selected `MiscTweak.FASTEST_TEXT` capability applies configured tweak or text-speed values `{4,1,0}`. Capability source exists; exact output applicability/reload/runtime still requires R2, not an additional CFRU Instant Text option. |

## R0 classification and post-#563 reconciliation

Each row uses #498 vocabulary. Runtime-required rows have present source owners;
they are not implementation gaps. Earlier targeted PASS remains revision-bound
supporting evidence, including later D11/D22/hint runs.

| Selected area / disposition | R0 class |
|---|---|
| M-001 29 gold TM/HM targets, ordinary-item control | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-002 Forest Nurse, poison refusal | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-003 instant 19 ordinary-Center healing; Tower control | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-004 1,500-step guaranteed approved renewal groups | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-004 Mt. Moon vanilla/random boundary | `INTENTIONAL_DIFFERENCE` |
| M-005 empty initial PC / one-time Lab Potion | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-006 mandatory Mom / safe shortened Lab handoff, normal starter/Rival flow | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-007 shortened Parcel, normal Dex handoff, five balls once, Old Man bypass | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-008 optional Bill/Sevii and original YES/NO story travel | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-009 always-on eligible sparkle, frame/lifecycle regression coverage | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| M-010 accepted pilot data/engine/QoL decision | `REQUIRED_PRESENT` |
| M-011 Hospitality experiments and missing Commander/Hospitality/Embody Aspect mechanics | `OUT_OF_PILOT` |
| M-012 analysis-only inventory/ownership boundary | `REQUIRED_PRESENT` |
| M-013 Premier transaction/capacity policy | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Gen1–9 Base Stats, coherent learnsets, ability assignments/names and safe representation | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Partial Palafin/Terapagos, unsupported forms/effects, sentinels and safe writer exclusions | `INTENTIONAL_DIFFERENCE` |
| Standard/Ironmon AI, native running, Auto-Run, fresh independent defaults and Options UX | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| 19-Center Name Rater, Repel reuse, reusable TMs, forgettable HMs, Party Move Items, service-specific Select-from-PC and acquire UI | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Current HM item + compatible non-egg party + badge/location eligibility; Route 10 HM05 shared reward flag | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Full NatDex no-compatible-party HM model; National Dex at Fresh New Game | `INTENTIONAL_DIFFERENCE` |
| Full National Dex at ordinary Parcel/Pokédex handoff | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Two Island mushroom-priced Move Maniac | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Early Celadon House2 Reminder (no normal entrance warp) | `INTENTIONAL_DIFFERENCE` |
| Cinnabar paid duplicate Reminder / alternative service placement | `OPTIONAL_BACKLOG` |
| F01/D01 minimal exposition with normal gender/free player/rival naming, retries and generated identity; #592/#593/#594 closure supersedes old optional-intro disposition | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| F02 isolated energetic starter flavor removal; #595/#596/#597 accepted closure | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| Audit F03 #598 skipped/not planned: original pre-Brock Guide accepted; scene-1 Aide preserved | `INTENTIONAL_DIFFERENCE` |
| Audit F04 #599 skipped/not planned: original Brock reward/tutorial retained | `INTENTIONAL_DIFFERENCE` |
| Presentation-only audit D03 Rival / F05 Captain tutorial: later user decision nonblocking/deprioritized, no automatic implementation route | `OPTIONAL_BACKLOG` |
| D11 integrated Fast Battle Messages, fresh Off, flag-backed persistence; #600/#601/#602 | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| D22 B normal Run and context-sensitive glyph; #603/#604/#605 and #606/#607/#608 | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| D20 saturation repair and accepted source/host/native boundary proof; #609→#610→#611→#612/#613 | `REQUIRED_PRESENT` |
| D20 ordinary Prize Room smoke at natural Celadon arrival, B13 | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` |
| D07 UPR FASTEST_TEXT selected capability; locked-profile output/reload/runtime verification stays R2 | `REQUIRED_PRESENT` |
| UPR supported-profile detection/writers, Pickup Unchanged guard, stale National-Dex request protection | `REQUIRED_PRESENT` |
| Unselected #589 D candidates: no-Mom skip, extra story trimming, BGM Off/chooser, sparkle toggle, faster fishing, Friendship service, Portable PC distribution, Bag/save expansion, wider Itemfinder/ball marks, Safari change, Pickup bell, Nature colors, low-HP beep, room colors, national Aide thresholds, accented keyboard | `INTENTIONAL_DIFFERENCE` |
| Whole-game acceleration, debug/gift/cheat promotion, broad story/content/UI imports, expanded name ABI or invented DPE settings architecture | `OUT_OF_PILOT` |
| Missing Gen9 mechanics, broad battle-engine refactors, Scarlet/Violet parity or new Terastal/form-transition systems solely for parity | `OUT_OF_PILOT` |
| BizHawk/Tracker/profile freeze and upstream contribution work in this contract | `OUT_OF_PILOT` |

**Namespace warning:** audit closure F03/F04 are unrelated to M-014 case
F03/F04, which test Bill NO/repeat/reload and continued Gym/League progression
without accepting optional travel. No package case is
deleted or waived by #598/#599. Audit D07/D11/D20/D22 are feature labels, not
changes to the similarly named progression IDs. Package D03/F05 also retain
their original progression/travel obligations.

#563/#565 are LEGACY / OBSOLETE as operative gates, retained as historical
supporting provenance. The #589 report remains the decision inventory, but its
nine-fix queue is superseded by later accepted source integrations and explicit
user dispositions above. Native early running/stateless post-init defaults and
Sign Lady repair also supersede #563's older lifecycle description. No stale
Workspace/CFRU revision is used as the current run basis.

## Acceptance overlays and evidence boundary

The existing package/report retain exactly 115 base IDs: A17 + B27 + C10 +
D16 + E7 + F7 + G6 + H15 + P10. Ownership remains 89 R1-only, 16 R2-only,
and 10 split IDs; therefore 99 R1 units and 26 R2 units. All runtime rows and
split variants remain `NOT_RUN`. There is no second matrix or renumbering.

- R1 D11: A01/B16/B27 and battle checkpoints cover fresh Off, On/Off,
  completed-wait skip, ordinary text animation, setting isolation/persistence.
- R1 D22: C04 and progression battles cover ordinary-wild glyph/B normal
  Run, success/failure/restrictions, trainer exclusion, manual A/R controls,
  FIGHT PSS/move-type colors, convenient local-double Back/partner-cancel.
  No Shiny safeguard requirement is added.
- R1 D20: B13 at natural Celadon arrival requires one normal inexpensive prize,
  correct reward and single Coins deduction, intact UI/control and return/exit.
  No memory editing, artificial 65,536-Coin balance or special save is required.
- R2 D07: H15 combined-profile variant verifies FASTEST_TEXT against the locked
  ROM, output/reload coherence and selected behavior in actual output runtime.
  No duplicate CFRU Instant Text requirement. R2 remains behind ROM_PROFILE_READY.
- F01/F02 creation, identity/retry and starter/nickname witnesses extend A01/A05;
  original Bill/Sevii F03/F04 remain intact.

**CONFIRMED USER-SUPPLIED EXACT-PIN NATIVE BUILD EVIDENCE:** #611 and #614
record CONTROL acceptance at the revision table above: data-owner verification,
M-009 frame/scanner/Pewter/stateless-entry/insertion invariants, AI ownership/
linker/load-span, ARM allocation/result/observation, exact objcopy re-extraction,
and final CFRU insertion PASS. D20 high-balance saturation is covered by accepted
production-source host regression and native-build evidence. This is supporting/
pre-run evidence only; no artifact was inspected and no build/test rerun is
claimed here. It does not make any M-014 runtime case PASS.

## Limitations, verification and handoff

Source proof cannot certify final runtime visuals, lifecycle, identity persistence,
continuous progression, emulator compatibility or randomized-output behavior.
Emulator identity/version/core, run label, configuration differences and actual
Fresh New Game execution remain user-owned placeholders. Unsupported forms/
mechanics use existing BLOCKED/N/A/reviewer-approved profile-exclusion rules;
no universal Gen1–9 mechanics claim is made. Genuine fresh continuous D01–D16
is required; earlier targeted observations cannot substitute for that run.

Focused document/source-identity verification completed:

- Exact Workspace base and CFRU/DPE/UPR/pret HEAD identities: PASS.
- Both actual case matrices: exactly 115 unique IDs, exact baseline order and
  matching IDs; report phase ownership unchanged: PASS. Phase-map references
  such as B18 are metadata, not additional base case rows.
- All 115 report runtime rows and both split portions remain NOT_RUN; 89/16/10
  ownership recount gives 99 R1 units / 26 R2 units: PASS.
- D11/D20/D22 R1 and D07 R2 overlays, current R0 link, historical #563/#565
  disposition, namespace warning and absence of old current-basis SHAs: PASS.
- Relative document links and exact three-file allowlist: PASS.
- Ten recursive Gitlink identities match the base, index and component HEADs;
  all component checkouts clean; no source/Gitlink changes: PASS.
- Workspace safety and `git diff --check`: PASS. Final staged/committed diff
  and clean checkout are verified again for the PR handoff.

`UNKNOWN`: future user-run identity/results and final support behavior remain
unknown; these are acceptance work, not an unresolved mandatory source gap.
`CONFLICT`: none identified. `MISSING_BLOCKER = 0`; `UNKNOWN_BLOCKER = 0`.

Final R0 verdict: `ROM_SCOPE_READY_FOR_ACCEPTANCE`.
After review and user acceptance/merge of #614, the next eligible gate is the
user-owned Phase R1 run; R2 remains gated. This task performs no runtime,
Randomizer, private-artifact, build or emulator work and no merge. No ROM/save/
emulator state/build/tool binary/private path/secret was read or modified.
`UPSTREAM_CONTRIBUTION = DEFERRED`.
