# CFRU QoL coverage analysis

Status: documentation-only coverage analysis for branch `analysis/cfru-qol-coverage`.

No CFRU, DPE or UPR-FVX source file was changed. The local CFRU checkout at `02_external/CFRU-expansion` was read only, is clean, and points at the Planton361 fork on `compat/firered-gen9-randomizer`.

## Scope

This analysis compares the Ironmon / FireRed QoL baseline from `01_docs/analysis/ironmon-qol-feature-inventory.md` and the completed manual smoke matrix in `08_tests/randomizer/cfru-qol-new-game-smoke.md` against the current local Planton361 CFRU source.

It separates:

- CFRU features already present and not worth duplicating;
- compile-time or script/runtime features that should be verified and preserved;
- missing QoL features that need new CFRU design before implementation;
- UPR-FVX-owned Field Items behavior;
- DPE-unrelated items.

## Key findings

- `BW_REPEL_SYSTEM` is active in current CFRU source: `src/config.h` defines it, `src/overworld.c` stores the last used repel and routes expiration into `EventScript_BwRepelWoreOff`, and `assembly/overworld_scripts/system_scripts.s` asks whether to reuse another Repel / Super Repel / Max Repel.
- Repel reuse is compile-time plus script behavior. No Options-menu or other runtime toggle was found for it.
- Repel reuse should not be newly built. It should be preserved and covered by a small gameplay smoke.
- Several Ironmon-near baseline items are already provided by CFRU config or project-local runtime options: controls-guide skip, Oak tutorial battle absence, running indoors, auto-run flag path, poison faint behavior, old/flat EXP profile, reusable TMs, select-from-PC support, item acquire pictures/descriptions, auto lowercase naming screen, multiple Premier Balls, HM field-use convenience, Portable PC, and current Runtime Options pages.
- Missing or only partially covered baseline items remain real CFRU work: broader Faster Intro / New Game Flow, shortened Oak/Lab/Parcel flow, visible Hidden Items / always-on sparkle policy, yellow/golden TM/HM or important itemballs, Name Rater in Poke Centers, and Bill-Sevii auto-ask removal.
- Field Items randomizer output remains UPR-FVX-owned. CFRU should not infer itemball graphics or TM/HM slot semantics from randomized output without a separate source-backed design.

## Coverage matrix

| QoL feature | CFRU evidence | Current status | Coverage | Ironmon-QoL baseline relation | Risk | Recommended next step | Smoke-test proposal |
|---|---|---|---|---|---|---|---|
| Repel-Reuse / BW Repel System | `src/config.h` defines `BW_REPEL_SYSTEM`; `src/overworld.c` uses `gLastUsedRepel` and `EventScript_BwRepelWoreOff`; `system_scripts.s` handles reuse prompts and step reset. | active | already provided | Direct QoL baseline item. | Low | Do not implement again; add preserve smoke. | Use one Repel, let it expire while another matching Repel is in Bag, choose Yes/No and verify step count/message behavior. |
| Runtime Repel option | No `option_menu.c` row or runtime flag found for `BW_REPEL_SYSTEM`; behavior is controlled by compile-time define and scripts. | absent | reject | Not required by baseline; runtime toggle would be extra. | Low/medium | Keep compile-time. Only design runtime toggle if explicitly requested. | n/a unless a toggle is later added. |
| Auto-run | `src/config.h` defines `FLAG_AUTO_RUN`; `src/read_keys.c` toggles with L when running is enabled; `src/overworld.c` makes B walk when auto-run is on. | configurable | verify-preserve | Useful low-friction run QoL. | Low/medium | Preserve; document that it depends on running being enabled. | Toggle L after running is available; verify auto-run on/off signs and B-to-walk inversion. |
| Running indoors | `src/config.h` defines `CAN_RUN_IN_BUILDINGS`; `src/overworld.c` only blocks indoor running when the define is absent. | active | already provided | Direct run-flow QoL. | Low | Do not rebuild. | After running is available, verify running on one indoor map and one outdoor map. |
| Poison overworld behavior | `src/config.h` leaves `NO_POISON_IN_OW` and `POISON_1_HP_SURVIVAL` commented; `src/overworld.c` can faint poisoned Pokemon. | active | already provided | Already manually smoked as pass with caveats. | Low/medium | Preserve. | Keep existing poison faint smoke as regression gate. |
| Fast battle messages | `src/config.h` defines `FLAG_FAST_BATTLE_MESSAGES`; `src/general_bs_commands.c` skips waits when the flag is set. No Options row found. | configurable | needs smoke | Useful speed QoL, but not proven as user-facing toggle. | Medium | Decide owner for setting/clearing the flag before relying on it. | Set flag through a sanctioned script/test path only, then compare message wait behavior. |
| Reusable TMs / TM-HM handling | `src/config.h` defines `REUSABLE_TMS`; `src/item.c` checks TM/HM pocket behavior, quantity/sell/buy paths; `bytereplacement` has guarded reusable-TM changes. | active | already provided | Baseline-compatible; do not duplicate in UPR-FVX Misc Tweaks. | Medium | Preserve; avoid randomizer-side duplicate patch. | Use/buy one TM, verify it remains owned and cannot be repurchased if already owned. |
| Select Pokemon from PC directly | `src/config.h` defines `SELECT_FROM_PC`; `src/scripting.c` has guarded PC selection paths. | active | verify-preserve | Convenience feature; not DPE-owned. | Medium | Preserve and smoke if a script uses it. | Trigger a script that supports selecting from party/PC and verify cancel/selection behavior. |
| Move Items on Party Screen | `include/new/party_menu.h` explicitly documents moving items between Pokemon from party menu; `src/party_menu.c` has `CursorCb_MoveItem` path. | active | needs smoke | Party QoL; already CFRU-owned. | Medium | Smoke before changing party menu. | Move a held item between two party Pokemon; verify no duplication/loss and cancel path. |
| Configurable Start Menu / PokeTools | `src/config.h` defines `FLAG_SYS_*` menu flags; `src/start_menu.c` builds DexNav/PokeTools and standard menu entries by flags. | configurable | verify-preserve | Runtime UI QoL, not Ironmon-specific. | Medium | Preserve; no baseline implementation needed. | Toggle known flags through existing story/test path and verify menu entries appear/hide. |
| Runtime Options pages | `src/option_menu.c` handles text speed, R button mode, battle music, wild scaling, auto-sort bag, game difficulty, trainer level scaling, trainer AI, hard cap, Nuzlocke, and Wild Prebattle. | active | already provided | Existing manual smoke is `PASS_FULL_WITH_CAVEATS`. | Medium | Do not add duplicate settings; use existing rows. | Keep page navigation, dirty-row preservation, Nuzlocke and Wild Prebattle ownership smokes. |
| Instant text | `src/config.h` has `INSTANT_TEXT` commented; `src/text_printer.c` gates instant text on that define. | inactive | needs implementation | Possible speed QoL, but pacing-sensitive. | Medium | Do not enable by default without baseline decision. | If enabled later, smoke long dialogue, yes/no prompts, fanfares, and script waits. |
| Autoscroll text | `src/config.h` defines `AUTOSCROLL_TEXT_BY_HOLDING_R`; `src/text_printer.c` references it. | active | verify-preserve | Nice-to-have text QoL. | Low/medium | Preserve; smoke only if text/input code changes. | Hold R during dialogue and verify scrolling without prompt skip breakage. |
| Auto lowercase naming screen | `src/config.h` defines `AUTO_NAMING_SCREEN_SWAP`; `src/scripting.c` references naming-screen swap behavior. | active | already provided | Naming QoL. | Low | Preserve. | Open naming screen; verify case swap after first uppercase letter. |
| Multiple Premier Balls | `src/config.h` defines `MULTIPLE_PREMIER_BALLS_AT_ONCE`; `src/item.c` applies purchase reward quantity behavior. | active | verify-preserve | Shop QoL; not randomizer-owned. | Low/medium | Preserve. | Buy 10, 20, and non-multiple Poke Balls and verify reward count. |
| Item picture / description on obtain | `src/config.h` defines `ITEM_PICTURE_ACQUIRE` and `ITEM_DESCRIPTION_ACQUIRE`; `src/scripting.c` shows item icon/description on first obtain and hidden item pickup. | active | already provided | Covers acquire presentation, not visible map balls. | Medium | Preserve and keep Game Corner caveat visible. | Pick normal and hidden item; verify picture/description appears and clears. |
| Expanded Safari balls/steps | `src/config.h` defines `EXPAND_SAFARI_BALLS`, `SAFARI_ZONE_MAX_STEPS`, `SAFARI_ZONE_BALL_START`, `MAX_SAFARI_BALLS`; `assembly/main.s` and `src/scripting.c` adjust counters. | configurable | verify-preserve | QoL/engine capacity, not core Ironmon baseline. | Medium | Preserve; no baseline promotion. | Enter Safari Zone, verify starting balls/steps and battle/window counters. |
| HM usage / field move QoL | `src/config.h` defines `ONLY_CHECK_ITEM_FOR_HM_USAGE`; `src/overworld.c` and `src/party_menu.c` guard field move checks on item ownership plus compatible party Pokemon. | active | already provided | Useful baseline convenience, CFRU-owned. | Medium | Preserve; avoid randomizer writer coupling. | With HM item in Bag and compatible Pokemon, use field move without learned move; verify badge checks still apply. |
| Summary / Pokedex info QoL | `src/config.h` defines `DISPLAY_REAL_MOVE_TYPE_ON_MENU`, `DISPLAY_REAL_ACCURACY_ON_MENU`, `DISPLAY_REAL_POWER_ON_MENU`, `DISPLAY_EFFECTIVENESS_ON_MENU`, and `FRIENDSHIP_HEART_ON_SUMMARY_SCREEN`; BW summary/nature colors are commented. | mixed | verify-preserve | Helpful, but not part of requested Ironmon baseline. | Low/medium | Preserve active display helpers; do not enable inactive summary redesign by default. | Inspect move menu and summary after one known friendship/value setup. |
| Oak Tutorial battle config | `src/config.h` leaves `TUTORIAL_BATTLES` commented; `src/overworld.c` gates tutorial trainer battle paths; `FLAG_ACTIVATE_TUTORIAL` exists for optional scripted activation. | inactive | already provided | Direct baseline item: tutorial battle absent. | Medium | Do not rebuild; preserve current compile-time absence. | Keep existing New Game / Oak Tutorial absent smoke. |
| Intro Controls Guide skip | `src/config.h` defines `SKIP_INTRO_CONTROLS_GUIDE`; `bytereplacement` has guarded skip bytes. | active | already provided | Direct baseline item, already manually smoked. | Low/medium | Preserve; no broader intro claim. | Keep existing controls-guide skipped smoke. |
| Broader Faster Intro / New Game Flow | No broad Oak speech/player setup/lab flow shortening source found beyond controls-guide skip and tutorial battle config. | absent | needs implementation | Baseline candidate, but current CFRU only covers pieces. | Medium/high | Design separately if desired. | New-game start-to-control timing/path smoke after any script edits. |
| Shortened Oak/Lab/Parcel flow | Local CFRU overworld script additions are limited; no source-backed parcel/lab skip implementation found. | absent | needs implementation | Baseline candidate. | High | Separate script-design branch only after decision. | Start fresh, reach Parcel/Lab checkpoints, verify flags/items/dialogue and no softlock. |
| Teachy-TV unchanged | No dedicated Teachy-TV QoL implementation found; manual smoke records unchanged behavior. | absent | reject | Not in current baseline as a change. | Low | Leave unchanged unless requested. | Keep as non-regression check only. |
| Visible Hidden Items / always-on sparkle | CFRU improves hidden item acquire presentation, but no always-visible hidden item marker source was found. `system_scripts.s` uses hidden pickup sprite; `FLDEFF_SPARKLE` exists elsewhere. | absent | needs implementation | Candidate medium CFRU overworld feature. | Medium/high | Design opt-in cue; do not make always-on map scan by default. | Verify one hidden item cue, pickup once, flag set, no repeat. |
| Hidden Itemfinder / sparkle cue | CFRU has Itemfinder item table entry and hidden pickup script presentation; `FLDEFF_SPARKLE` is available. No reviewed Itemfinder sparkle-on-detect implementation found. | unclear | needs implementation | Candidate Itemfinder QoL. | Medium | Source-design against FireRed Itemfinder flow before code. | Use Itemfinder near/under hidden item and verify cue plus vanilla messages. |
| Field item balls / generic Poke Ball object graphics | CFRU uses vanilla-style `MAP_OBJ_GFX_ITEM_BALL` constant and generic item-ball script behavior; no per-item graphics source found. | active generic | verify-preserve | Baseline only if generic field balls must keep working. | Medium | Preserve generic behavior. | Pick visible itemball on two maps; object hides and item grants once. |
| Yellow/golden TM/HM/important itemballs | No current CFRU per-TM/HM/important-field-item object graphics implementation found. | absent | needs implementation | Baseline candidate, but crosses map object graphics and randomizer metadata. | High | Defer until after Field Items ownership decision. | If later built, test randomized TM and non-TM slots after reload. |
| Name Rater in Poke Centers | Search found party nickname functionality, but no Poke Center Name Rater placement implementation. | absent | needs implementation | Convenience baseline candidate. | Medium | New script/NPC design if accepted. | In a Poke Center, rename eligible Pokemon and verify ineligible/error paths. |
| Portable PC / Lab convenience | `src/config.h` defines `FLAG_PORTABLE_PC`; `ITEM_PORTABLE_PC` has `FieldUseFunc_PortablePC`; `system_scripts.s` can open PC box or heal when enabled. No lab-specific convenience flow found. | configurable | verify-preserve | Covers PC convenience partly; lab convenience remains absent. | Medium | Preserve Portable PC; decide if baseline wants item/flag distribution. | Enable portable PC through valid path, open PC/heal, then verify disabled message. |
| Bill-Sevii auto-ask removal | No Sevii/Bill source implementation found in local CFRU script additions. | absent | needs implementation | Baseline candidate for post-E4 flow. | Medium/high | Separate script audit/design. | Reach relevant Bill/Sevii prompt state and verify prompt suppression only after implementation. |
| Randomizer Field Items Shuffle/Random/Random Even/Ban Bad | Existing workspace docs and UPR-FVX source own Field Items through `ItemRandomizer`, `getFieldItems()` / `setFieldItems(...)`, required-TM policy, and reload smokes. | active in UPR-FVX scope | verify-preserve | Randomizer-output interaction, not CFRU QoL implementation. | Medium/high | Keep UPR-FVX-owned; CFRU visual work must not alter writer semantics. | Re-run Field Items reload smokes after any itemball or hidden-item visual change. |
| DPE impact | No QoL feature above requires Pokemon species/base-stat data changes. | absent | reject | DPE-unrelated. | Low | Do not involve DPE. | n/a |
| Balance/rules exclusions | Broader difficulty, Smart/Hard/Expert AI, Nuzlocke, level caps, wild prebattle and EXP/catch settings can change run rules. | configurable | verify-preserve / reject as default | Keep outside baseline unless explicitly selected. | Medium/high | Preserve existing options; avoid making rule features mandatory. | Options smoke plus targeted battle/encounter checks only when selected. |

## Repel-Reuse finding

`BW_REPEL_SYSTEM` is active in the current Planton361 CFRU branch. It is not a runtime Options-menu row in the reviewed source; it is compiled in through `src/config.h` and executed through overworld/script behavior.

Therefore Repel-Reuse does not need a new implementation. The next practical step is a preserve smoke that verifies the prompt, Yes/No branches, item removal and step reset for Repel, Super Repel and Max Repel.

## Already provided - do not duplicate

- Repel-Reuse / BW Repel System.
- Running indoors.
- Auto-run flag path.
- Poison overworld faint behavior.
- Old/flat EXP config profile.
- SwSh catch-level malus absent by config.
- Oak tutorial battle absent by config.
- Intro controls-guide skip.
- Reusable TMs and TM/HM handling.
- Select from PC support.
- Party move-item path.
- Item picture/description on obtain, including hidden pickup presentation.
- Auto lowercase naming screen.
- Multiple Premier Balls.
- HM field-use convenience.
- Current Runtime Options pages and Start Menu/PokeTools plumbing.

## Verify / preserve

- Repel-Reuse gameplay prompt and step reset.
- Auto-run after running is enabled.
- Running indoors in one safe indoor map.
- Fast battle messages only if a valid flag-setting path is chosen.
- Select-from-PC and party move-item behavior.
- Portable PC enable/disable behavior.
- Safari counters if Safari config matters to the profile.
- Item picture/description acquire behavior after any script change.
- Runtime Options dirty-row preservation.

## Needs implementation

- Full Faster Intro / New Game Flow beyond controls-guide skip.
- Shortened Oak/Lab/Parcel flow.
- Visible Hidden Items or Itemfinder sparkle cue.
- Yellow/golden TM/HM/important itemballs.
- Name Rater in Poke Centers.
- Lab-specific convenience flow.
- Bill-Sevii auto-ask removal.

## UPR-FVX-owned

- Field Items Shuffle / Random / Random Even / Ban Bad output.
- Required Field TM preservation.
- TM-vs-non-TM field-item slot typing.
- Randomizer compatibility after any Field Item visual work.

## DPE-unrelated

All reviewed QoL features are engine, script, UI, item, randomizer-output, or workspace-policy concerns. DPE should stay out of this QoL block unless a later feature directly changes Pokemon data.

## Recommended package order

1. Preserve already-provided CFRU QoL: Repel-Reuse, Auto-run/running, runtime pages, item acquire presentation, TM/HM handling, party item movement.
2. Decide baseline policy for missing medium CFRU script/overworld features: hidden-item cue, Name Rater placement, Portable PC distribution, lab/parcel/Bill-Sevii flow.
3. Only after that, design Field Item visuals with UPR-FVX as owner for generated output and CFRU as owner for runtime presentation.
4. Keep balance/rules toggles optional and outside the default QoL baseline unless explicitly selected.
