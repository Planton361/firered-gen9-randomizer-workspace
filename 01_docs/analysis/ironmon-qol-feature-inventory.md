# Ironmon / NatDex / FireRed QoL feature inventory

Status: documentation-only source inventory for branch `analysis/ironmon-qol-feature-inventory`.

No CFRU, DPE, UPR-FVX or Tracker source file was changed. No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash value, private path, token, secret or `.env` data was changed or documented.

## Purpose

This inventory collects source-backed Quality-of-Life feature candidates that are relevant to a CFRU/DPE/UPR-FVX FireRed Gen9 randomizer workspace, with special attention to Ironmon-style run flow, NatDex/FireRed field-item behavior, and randomizer interactions.

The inventory is not an implementation plan for immediate code changes. It separates:

- low-risk QoL settings that are already represented in local CFRU/UPR-FVX source or workspace smoke docs;
- medium-risk overworld/script features that need CFRU source work before implementation;
- randomizer-output interaction features where UPR-FVX field-item behavior must remain the owner;
- high-risk or unclear-source ideas that should not be ported from binary patches.

## Source set

Local source/docs read:

- `README.md`, `AGENTS.md`, `01_docs/PROJECT_BRIEF.md`, `01_docs/SESSION_STATE.md`, `01_docs/NEXT_STEPS.md`, `01_docs/DECISIONS_INDEX.md`
- `01_docs/references/source-index.md`, `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`
- `08_tests/randomizer/099_field_items_scope_diagnostics.md`
- `08_tests/randomizer/102_field_items_allowed_slot_reload_smoke.md`
- `08_tests/randomizer/106_field_items_random_tm_pool_reload_smoke.md`
- `08_tests/randomizer/109_field_items_api_tm_slot_reload_smoke.md`
- `08_tests/randomizer/110_field_items_random_even_reload_smoke.md`
- `08_tests/randomizer/113_field_items_random_even_ban_bad_reload_smoke.md`
- `08_tests/randomizer/205_intro_mon_visual_source_fix_smoke.md`
- `08_tests/randomizer/210_misc_tweaks_behavior_smoke.md`
- `08_tests/randomizer/212_gen_limit_special_form_item_smoke.md`
- `08_tests/randomizer/cfru-randomizer-baseline-config.md`
- `01_docs/analysis/cfru-game-difficulty-map.md`
- `02_external/CFRU-expansion/src/config.h`, `src/option_menu.c`, `src/wild_encounter.c`, `src/overworld.c`, `bytereplacement`, `assembly/overworld_scripts/system_scripts.s`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/ItemRandomizer.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/RomHandler.java`, `Gen3RomHandler.java`
- `02_external/references/pret-pokefirered/src/itemfinder.c`, `src/field_control_avatar.c`, `src/field_effect_helpers.c`, `include/constants/event_objects.h`, `src/data/object_events/object_event_graphics_info.h`

Public web/docs checked:

- PyroMikeGit/SuperKaizoIronMON README, especially Smart AI / QoL patch notes and Ironmon hidden-item rules: <https://github.com/PyroMikeGit/SuperKaizoIronMON>
- Ironmon Tracker wiki page "New Runs Setup": <https://github.com/besteon/Ironmon-Tracker/wiki/New-Runs-Setup>
- UPR-FVX About page, especially optional randomization, field-item, shop, Pickup, seed and log scope: <https://upr-fvx.github.io/universal-pokemon-randomizer-fvx/about.html>

## Local architecture notes

- CFRU is the best target for compile-time and runtime QoL that changes FireRed flow, option menu flags, hidden-item presentation, object graphics, field effects, or scripts.
- UPR-FVX is the best target only when the feature changes generated randomizer output, especially Field Items and TM/HM item placement.
- DPE is not a target for these QoL features unless a future feature directly changes Pokemon data tables.
- Workspace docs are the right target for pins, caveats, smoke protocols, and implementation sequencing.

## Feature catalog

| Feature | Description | Source / evidence | Target repo | Affected files / subsystem | Implementation type | Risk | Effort | Recommendation | Smoke-test proposal |
|---|---|---|---|---|---|---|---|---|---|
| Skip Intro Controls Guide | Skip FireRed's intro controls guide / help-flow interruption. | CFRU `src/config.h` defines `SKIP_INTRO_CONTROLS_GUIDE`; CFRU `bytereplacement` has a guarded skip block; baseline config smoke records it as implemented but not separately gameplay-proven. | CFRU | `src/config.h`, `bytereplacement`, new-game intro flow | Compile-time config | Low | XS | Keep in the low-risk QoL package; do not reopen unless a regression appears. | New-game smoke: start a fresh save, confirm controls guide is skipped, no freeze before player control. |
| Remove Oak Tutorial Battle | Remove Oak's tutorial battle/new-game battle interruption. | CFRU `src/config.h` has `TUTORIAL_BATTLES` commented with "remove Oak's Tutorial"; `src/overworld.c` gates `TRAINER_BATTLE_OAK_TUTORIAL`; baseline config documents disabled tutorial battles. | CFRU | `src/config.h`, `src/overworld.c`, tutorial battle path | Compile-time config | Low/medium | XS | Low-risk if kept as compile-time profile setting; smoke separately because tutorial flow can affect new-game script state. | New-game smoke through Pallet/Route 1 intro: confirm no Oak tutorial battle and no script softlock. |
| Faster text / run flow misc tweaks | Fastest Text, Run Without Running Shoes, Running Shoes Indoors, Randomize PC Potion, Catching Tutorial randomization mapping, Fast Egg Hatching. | `08_tests/randomizer/210_misc_tweaks_behavior_smoke.md`; UPR-FVX Misc Tweaks smoke is targeted pass with caveats. | UPR-FVX + Workspace | Misc Tweaks settings/profile docs; CFRU/DPE BPRE compatibility caveats | Randomizer settings/profile plus docs | Low for documented pass paths | XS/S | Treat as already available targeted QoL; do not duplicate Reusable TMs / Forgettable HMs when CFRU provides them. | Re-run targeted Misc Tweaks smoke after any profile or pin change. |
| Ironmon Tracker New Runs compatibility note | Keep generated-run workflow compatible with Tracker's New Runs mode. This is documentation/workflow, not a ROM feature. | Ironmon Tracker wiki says New Runs loads a different randomized ROM and can generate a ROM from source ROM + randomizer jar + settings. | Workspace | Tool manifest, setup docs, Tracker compatibility docs | Documentation / workflow | Low | XS | Document as compatibility target only; never commit generated ROMs or quickload artifacts. | Tracker dry setup review only: confirm docs say source ROM, randomizer jar and settings stay local/ignored. |
| Nuzlocke runtime toggle | Option-menu toggle for CFRU `FLAG_NUZLOCKE`. | CFRU `src/config.h` defines `FLAG_NUZLOCKE`; `src/option_menu.c` clears/sets and initializes it; baseline config smoke reports targeted settings pass. | CFRU | `src/config.h`, `src/option_menu.c`, Nuzlocke gated runtime paths | Runtime option | Low/medium | S | Keep as low-risk runtime option, with caveat that turning off does not unwind already-created Nuzlocke side state. | Menu smoke: Off clears only `FLAG_NUZLOCKE`, On sets only it, opening/closing preserves current value. |
| Wild Prebattle runtime toggle | Option-menu toggle for the CFRU Ignore/Engage prebattle screen. | CFRU `src/config.h` defines `IgnoreWildPokemon` and `FLAG_ENABLE_WILD_PMN_PREBATTLE_SCREEN`; `src/wild_encounter.c` checks the enable flag before prebattle screen generation; `src/option_menu.c` clears/sets only the enable flag. | CFRU | `src/config.h`, `src/wild_encounter.c`, `src/option_menu.c` | Runtime option | Low/medium | S | Keep; it is an ergonomic Ironmon/randomizer-facing toggle and is already scoped away from encounter table behavior. | Menu + one wild encounter smoke: Off gives normal encounter flow; On shows prebattle screen; no table/randomizer changes. |
| Runtime difficulty / AI profile split | Keep Smart/Hard/Expert AI and difficulty effects separate so Ironmon-like AI does not accidentally enable broad difficulty rules. | `01_docs/analysis/cfru-game-difficulty-map.md` shows `VAR_GAME_DIFFICULTY` affects AI, trainer builds, level scaling, item/move restrictions and battle rules; Trainer AI v3 docs already split profiles. | CFRU + Workspace | `src/option_menu.c`, AI profile vars, difficulty docs | Runtime option / policy | Medium | M | Prefer existing split-profile path over using CFRU Hard/Expert as "Ironmon Smart AI". | A/B battle smoke across Vanilla/Normal/Smart/Hard/Expert with sanitized turn summaries. |
| Old EXP / Flat EXP / Poison / Catch malus baseline | Ironmon-near baseline balance toggles: old EXP split, flat EXP formula, poison can faint, SwSh catch-level malus disabled. | CFRU `src/config.h` comments and current baseline config; roadmap records targeted build/boot/settings smoke with some gameplay rows inconclusive. | CFRU | `src/config.h`, `src/exp.c`, `src/overworld.c`, `src/catching.c` | Compile-time config | Low/medium | XS/S | Keep in low-risk QoL package, but run separate gameplay smoke before stronger claims. | Four micro-smokes: EXP distribution, poison faint, higher-level catch chance no malus, no build regression. |
| Hidden item Itemfinder behavior | Itemfinder detects hidden-item BG events, distinguishes underfoot items, plays response effects, and can dig up underfoot items. | pret FireRed `src/itemfinder.c`; `src/field_control_avatar.c` reads hidden-item attributes and launches hidden-item script; CFRU system script adds item sprite display when picking hidden item. | CFRU | Itemfinder, BG events, hidden-item scripts, `system_scripts.s` | Overworld/script QoL | Medium | M | Good medium package: improve visibility or feedback without changing randomizer placement. Keep read-only source parity with FireRed hidden-item flags. | In-game smoke with one normal hidden item and one underfoot hidden item; confirm flag set, item acquired once, no repeat pickup. |
| Hidden item sparkle / field-effect cue | Use existing field-effect plumbing to create a visible sparkle cue for hidden items or scan results. | pret `field_effect_helpers.c` implements `FldEff_Sparkle`; CFRU `system_scripts.s` already calls `FLDEFF_SPARKLE` in mining scan and shows item sprite for hidden item pickup. | CFRU | Field effects, hidden-item scripts, Itemfinder flow | Overworld/script QoL | Medium | M | Candidate after baseline smokes. Prefer opt-in or narrow cue on discovery/pickup, not always-on map scanning. | Hidden-item smoke: sparkle appears only for intended event, stops cleanly, item flag and game stat update once. |
| Item picture on acquire / hidden acquire presentation | Show item sprite when finding/obtaining hidden items; potentially extend to visible item balls. | CFRU `src/config.h` has `ITEM_PICTURE_ACQUIRE`; CFRU `system_scripts.s` calls `ShowItemSpriteOnFindHidden` / `ClearItemSpriteAfterFindHidden`. | CFRU | Item acquire script, item icon/sprite display | Existing config / script presentation | Low/medium | S | Inventory as mostly present. Do not combine with randomizer output changes. | Pick visible item and hidden item; confirm acquire UI appears, clears, and does not break Game Corner caveat if applicable. |
| Itemball object graphics baseline | FireRed represents visible field items with `OBJ_EVENT_GFX_ITEM_BALL` and one generic ItemBall graphics info entry. | pret FireRed `include/constants/event_objects.h` defines `OBJ_EVENT_GFX_ITEM_BALL`; `object_event_graphics_info.h` defines 16x16 inanimate `gObjectEventGraphicsInfo_ItemBall`; UPR-FVX Gen3 offsets include `ItemBallPic`. | CFRU / UPR-FVX only if output-owned | Object event graphics, map object templates, Gen3 field-item scan | Overworld graphics / randomizer scanner | Medium | M | Low priority unless visual clarity is needed. Keep generic ball stable; per-item graphics would be a larger object-event graphics feature. | Visual smoke in multiple maps: item balls render, pickup hides object, no palette/OAM corruption. |
| TM/HM item ball visual distinction | Make TM/HM field item balls visually distinct from regular items. | Evidence is indirect: UPR-FVX preserves TM-vs-non-TM slot type; FireRed object graphics are generic. No reviewed source shows a ready per-slot TM ball graphics implementation. | CFRU + possibly UPR-FVX metadata | Map object graphics, itemball script pattern, TM/HM field item classification | New feature | High | L | Do not implement first. Needs a source-backed design for how visible object graphics follow randomized output without corrupting map scripts. | If later implemented: generate output with field item randomization, verify TM slots use TM graphic and non-TM slots keep normal graphic after reload. |
| Field Items Shuffle | Shuffle existing field item set while preserving slot class and guarded slots. | `08_tests/randomizer/102_field_items_allowed_slot_reload_smoke.md` passes in allowed-slot scope. | UPR-FVX + Workspace | `ItemRandomizer`, `RomHandler.getFieldItems/setFieldItems`, Gen3 map/script parser | Randomizer output interaction | Low within tested scope | XS | Already GUI-compatible in the tested narrow scope; keep as documented support. | Re-run allowed-slot reload smoke after UPR-FVX field-item changes. |
| Field Items Random | Replace field items with random picks while preserving TM slots, required field TMs, invalid/unloaded/fallback/placeholder/progression-sensitive slots. | `08_tests/randomizer/109_field_items_api_tm_slot_reload_smoke.md` passes after API TM-slot fix. UPR-FVX `RomHandler` requires TMs replace TMs and non-TMs replace non-TMs. | UPR-FVX | `ItemRandomizer`, Gen3 field-item API, required field TMs | Randomizer output interaction | Medium | S/M | Keep supported in narrow field-items-only scope. Do not expand to shops/pickup/gifts. | Field-items-only save/reload smoke with required-TM, TM-slot, non-TM-slot and disallowed-slot counters. |
| Field Items Random Even | Evenly distribute field-item picks while preserving slot policies. | `08_tests/randomizer/110_field_items_random_even_reload_smoke.md` passes in narrow scope. | UPR-FVX | `ItemRandomizer.randomizeNonTMFieldItems`, field-item API | Randomizer output interaction | Medium | S/M | Keep supported with same caveats as Field Items Random. | Random-even reload smoke; verify queue/refill behavior and no slot-type drift. |
| Field Items Ban Bad Items | Exclude bad items from Field Items Random/Random Even pools. | `08_tests/randomizer/113_field_items_random_even_ban_bad_reload_smoke.md` passes; `212` documents mechanic item categories but caveats static/gift/NPC sources. | UPR-FVX | Item pools, mechanic item filters, field-item randomizer | Randomizer output interaction | Medium | S/M | Keep, but avoid promising broader item-source coverage. | Random and Random Even with Ban Bad; verify bad writes are zero and shop/pickup/held scopes unchanged. |
| Required Field TMs policy | Keep required field TMs available when field items are randomized. | UPR-FVX `RomHandler.getRequiredFieldTMs()` comments explain required TMs must be included; field item smokes show required TMs present/missing counters. | UPR-FVX | Required-TM table, TM field item pool | Randomizer output interaction | Medium | S | Treat as a hard invariant for any Field Items change. | Settings smoke with all field-item modes; assert required-field-TM missing count stays zero. |
| Shops / Pickup separation | Keep Shops and Pickup separate from Field Items QoL. | `057_p1_field_items_shops_pickup_model.md` says Field Items, Shops and Pickup have separate risks; smokes verify shop/pickup scopes unchanged during Field Items runs. | UPR-FVX + Workspace | Shop writer, Pickup writer, item pools | Randomizer output interaction | Medium/high | M/L | Not part of this QoL implementation train; plan separately. | Dedicated shop and pickup diagnostics, not piggybacked on field items. |
| Mechanic item exclusions | Avoid placing Mega/Z/Dynamax-GMax and other mechanic/system items into unsafe pools without policy. | `212_gen_limit_special_form_item_smoke.md` documents source-backed mechanic item category fixes and caveats Plates/Drives/Memories/Nectars and static/gift/NPC item sources. | UPR-FVX + Workspace | Item pool filters, profile caveats | Randomizer output interaction | Medium | M | Keep filters source-backed; add user-facing policy only after separate review. | Pool audit: count excluded mechanic items by category and verify no unsafe field-item writes. |
| Binary QoL patch ports | Maple QoL / Ironmon QoL patches are publicly referenced, but not source-backed here. | PyroMike README links a FireRed/LeafGreen Smart AI patch and Maple QoL patch, but this task forbids binary patches and no source was used. | None for now | n/a | Blocked / source-needed | High | Unknown | Do not port. Use as feature inspiration only until public source/docs exist. | n/a |

## Priority packages

### Package A - Low-risk QoL features

Recommended first implementation/smoke package:

1. Keep existing CFRU Randomizer baseline config: skip controls guide, remove Oak tutorial, old/flat EXP, poison faint, catch malus off.
2. Keep existing runtime option rows: Nuzlocke and Wild Prebattle.
3. Keep UPR-FVX Misc Tweaks from the current stable profile: Fastest Text, PC Potion, Running Shoes fixes, Catching Tutorial species mapping, Fast Egg Hatching guard.
4. Document Tracker New Runs compatibility as workflow only.

Why first: most are already source-backed or locally smoked; no randomizer-output ownership conflict.

### Package B - Medium overworld/script features

Recommended second package:

1. Hidden item Itemfinder feedback audit.
2. Hidden-item sparkle/acquire-presentation design.
3. Item picture on acquire regression smoke.
4. Optional visible itemball presentation audit.

Why second: these touch scripts, field effects and object events, but can stay in CFRU and avoid randomizer writer changes.

### Package C - Randomizer-output interaction features

Recommended third package:

1. Preserve current Field Items Shuffle/Random/Random Even/Ban Bad status.
2. Treat Required Field TMs as an invariant.
3. Keep TM-vs-non-TM slot typing stable.
4. Do not expand to Shops, Pickup, gifts, static/NPC items, or per-itemball graphics without a separate source-backed plan.

Why third: UPR-FVX already owns these outputs, and the smokes are good, but future CFRU visual changes could accidentally depend on randomized output metadata.

### Package D - High-risk or unclear-source features

Keep out of the first implementation train:

1. Maple QoL / binary patch ports.
2. TM/HM-specific itemball object graphics.
3. Always-visible hidden-item sparkles across all maps.
4. Static Script/Gift/NPC item randomizer interaction.
5. Shops/Pickup changes.

Why last: source is incomplete or ownership crosses CFRU map scripts, UPR-FVX output, and player progression.

## Recommended implementation order

1. Documentation-only pin: accept this inventory and add a short "first implementation block" handoff.
2. Low-risk CFRU baseline gameplay smoke: new-game flow, Oak tutorial, controls guide, EXP, poison, catch malus.
3. Runtime option regression smoke: Nuzlocke and Wild Prebattle only.
4. Medium hidden-item design branch: no randomizer output change; use existing FireRed hidden-item and CFRU field-effect source.
5. Field Items regression smoke after any UPR-FVX or CFRU object/script change.
6. Only after those pass, evaluate itemball graphics or TM/HM visual differentiation.

## Handoff for first real implementation block

Suggested branch: `feature/cfru-qol-baseline-smoke-hardening`

Scope:

- No new CFRU code unless a smoke finds a regression.
- Run source/syntax checks and targeted local gameplay smoke for the already-documented baseline:
  - controls guide skipped;
  - Oak tutorial removed;
  - old/flat EXP behavior;
  - poison can faint in overworld;
  - SwSh catch-level malus off;
  - Nuzlocke row and Wild Prebattle row preserve/clear/set only their owning flags.

Explicit exclusions:

- No UPR-FVX changes.
- No DPE changes.
- No field-item writer changes.
- No itemball graphics changes.
- No hidden-item sparkle implementation.
- No binary patch ports.
- No ROM/build/log/private artifact commits.

Smoke output should be sanitized and should not include ROM names, paths, hashes, screenshots, raw logs, saves, states, build artifacts, or private local details.
