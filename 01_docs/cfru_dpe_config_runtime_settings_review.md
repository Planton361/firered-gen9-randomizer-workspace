# CFRU/DPE Config and Runtime Settings Review

Branch: `analysis/cfru-config-runtime-settings-review`

Scope: documentation-only source review of local CFRU/DPE configuration, runtime flags/vars, script-controlled settings and EXP behavior. No ROMs, builds, generated output, private paths or raw logs were used.

## Executive Summary

The local checkout has two different "config" layers:

- `02_external/CFRU-expansion/include/config.h` is minimal and currently only covers debug/language style defines such as `ENGLISH` and `UNITS_IMPERIAL`.
- `02_external/CFRU-expansion/src/config.h` is the real CFRU feature/settings header. It contains compile-time feature macros, numeric constants and the event var/flag IDs used by runtime code and scripts.

Most engine features are compile-time gated by `#ifdef`, `#ifndef` or numeric constants. Changing these requires a rebuild and can affect table size, save layout, item/TM behavior or battle logic. Commenting out a macro only disables behavior where the code checks whether the macro is defined; for runtime flags such as `FLAG_EXP_SHARE`, the macro being defined also enables the code path that later reads the in-game flag.

Runtime settings exist, but they are not free-standing unless their compile-time macro is present. CFRU uses event flags and vars through `FlagGet`, `FlagSet`, `FlagClear`, `VarGet` and `VarSet`. Some are changed by scripts, field item callbacks or the option menu.

EXP behavior is mixed:

- The EXP formula is compile-time: `FLAT_EXP_FORMULA` selects the Gen 2-4/6 style flat formula; removing it selects the scaled Gen 5/7 style formula.
- The Gen 6+ Exp Share code path is compile-time gated by `FLAG_EXP_SHARE`, then runtime toggled by the flag value `0x906`.
- Current source already defines `FLAT_EXP_FORMULA`, so the current formula is not level-scaled in `exp.c`; however Gen 7 base EXP yields, trainer EXP boost, capture EXP and affection boost are still enabled.
- Full Gen 3 standard EXP is not a single runtime toggle. It would require a deliberate source/config patch and rebuild.

For Anton, the practical model is: use `src/config.h` as the compile-time profile, use the option menu / scripts / items for runtime vars and flags, and treat EXP changes as a small source/config branch rather than an NPC/script setting.

## `config.h` Mechanics

| Setting / Macro | Typ | Werteform | Auswirkung | Änderung braucht Rebuild? | Risiko |
|---|---|---|---|---|---|
| `02_external/CFRU-expansion/include/config.h` | COMPILE_TIME_DEFINE | `#define ENGLISH`; derived `UNITS_IMPERIAL` | Language/unit preprocessor path only in this checkout | Yes | Low for gameplay scope; not the main feature config file |
| `02_external/CFRU-expansion/src/config.h` | COMPILE_TIME_DEFINE | Header included through `defines.h` / source includes | Main CFRU configuration surface | Yes | High: broad engine behavior |
| `EXPANDED_TMSHMS` | COMPILE_TIME_DEFINE | Defined/commented | Enables expanded TM/HM handling; code uses different TM/HM bitset widths and item mapping | Yes | High: table/compatibility assumptions |
| `NUM_TMS`, `NUM_HMS`, `NUM_MOVE_TUTORS`, `LAST_TOTAL_TUTOR_NUM` | COMPILE_TIME_NUMERIC | Integer constants | TM/HM/Tutor counts and generated table dimensions | Yes | High: mismatch breaks compile/runtime table reads |
| `DELETABLE_HMS`, `REUSABLE_TMS` | COMPILE_TIME_DEFINE | Defined/commented | HM deletion and reusable TM behavior in item code | Yes | Medium; randomizer profile should not duplicate CFRU-provided behavior |
| `NATIONAL_DEX_COUNT`, `NUM_SPECIES_RANDOMIZER` | COMPILE_TIME_NUMERIC | Integer/expression | CFRU internal Dex/randomizer limits | Yes | High for Gen9 coverage if changed incorrectly |
| `MAX_LEVEL`, `EV_CAP`, `POWER_ITEM_EV_YIELD` | COMPILE_TIME_NUMERIC | Integer constants | Level cap bounds, EV caps and item yield behavior | Yes | High; comments note matching assembly defines may also be needed |
| `MEGA_EVOLUTION_FEATURE`, `DYNAMAX_FEATURE`, `TERASTAL_FEATURE` | COMPILE_TIME_DEFINE | Defined/commented | Enables/removes major battle mechanics code paths | Yes | High; affects items, forms, battle UI and feature availability |
| `OLD_BURN_DAMAGE`, `OLD_PARALYSIS_SPD_DROP`, `OLD_MOVE_SPLIT`, `OLD_CRIT_DAMAGE` | COMPILE_TIME_DEFINE | Mostly commented legacy toggles | Restores selected older battle mechanics | Yes | Medium/high; broad balance impact |
| `TRAINER_EXP_BOOST` | COMPILE_TIME_DEFINE | Defined | Trainer battle EXP multiplier in `src/exp.c` | Yes | Medium; part of modern-ish EXP profile |
| `OLD_EXP_SPLIT` | COMPILE_TIME_DEFINE | Currently commented | Restores old split among participants/Exp Share holders depending on Exp Share mode | Yes | Medium/high; interacts with Exp Share |
| `FLAT_EXP_FORMULA` | COMPILE_TIME_DEFINE | Currently defined | Selects flat Gen 2-4/6 EXP formula in `src/exp.c` | Yes | Medium; removing it enables scaled Gen 5/7 formula |
| `GEN_7_BASE_EXP_YIELD` | COMPILE_TIME_DEFINE | Defined | Uses `gBaseExpBySpecies` from `src/Tables/experience_tables.c` | Yes | Medium; not Gen 3 base yield |
| `CAPTURE_EXPERIENCE` | COMPILE_TIME_DEFINE | Defined | Catch-success battle script calls `getexp` | Yes | Medium; modern behavior |
| `EXP_AFFECTION_BOOST` | COMPILE_TIME_DEFINE | Defined | Friendship >= 220 can boost EXP | Yes | Medium; modern behavior |
| `FLAG_EXP_SHARE` | RUNTIME_FLAG plus COMPILE_TIME_DEFINE | Macro defines flag ID `0x906`; runtime flag toggled | Enables Gen 6+ Exp Share code path and runtime on/off flag | Compile macro: yes; flag value: no | High: if macro is removed, field toggle code path changes |
| `FLAG_HARD_LEVEL_CAP`, `FLAG_KEPT_LEVEL_CAP_ON` | RUNTIME_FLAG plus COMPILE_TIME_DEFINE | Macro defines flag IDs | Runtime hard cap enforcement in EXP, Rare Candy, DexNav and battle-start checks | Compile macro: yes; flag value: no | Medium/high; can block EXP above cap |
| `VAR_WILD_LEVEL_SCALING` | RUNTIME_VAR | Var ID `0x5153`; option menu writes 0/1 | Wild encounter level scaling in `src/wild_encounter.c` | Macro change: yes; value change: no | Medium; current source uses var directly |
| `VAR_GAME_DIFFICULTY` | RUNTIME_VAR | Var ID `0x5157`; option values Normal/Easy/Hard/Expert | AI, trainer-building, battle and misc difficulty conditionals | Macro change: yes; value change: no | Medium/high; many readers |
| `VAR_R_BUTTON_MODE`, `VAR_BATTLE_MUSIC`, `VAR_AUTO_SORT_BAG` | RUNTIME_VAR | Option menu vars | R-button function, battle music style, bag sorting | Macro change: yes; value change: no | Low/medium |
| `FLAG_AUTO_RUN`, `FLAG_RUNNING_ENABLED`, `CAN_RUN_IN_BUILDINGS` | RUNTIME_FLAG / COMPILE_TIME_DEFINE | Flag IDs plus compile macro | Running shoes/auto-run/indoor running behavior | Macro change: yes; flag value: no | Low/medium; affects input expectations |
| `ITEM_PICTURE_ACQUIRE`, `ITEM_DESCRIPTION_ACQUIRE` | COMPILE_TIME_DEFINE | Currently commented | Optional item sprite/description popup when obtaining items | Yes | Medium; comment warns about Game Corner prize room |
| `SKIP_INTRO_CONTROLS_GUIDE` | COMPILE_TIME_DEFINE | Defined | Removes intro controls guide per config comment | Yes | Low/medium; not the same as full faster intro |

## Runtime-/NPC-Settings

The source shows several runtime surfaces. Some are explicit scripts, some are item callbacks, and some are option-menu vars.

| Runtime surface | NPC/Script/File | Variable/Flag set | Feature code reading it | Compile-time prerequisite |
|---|---|---|---|---|
| Exp Share field item toggle | `assembly/overworld_scripts/system_scripts.s`, `SystemScript_Exp_Share_On` / `Off`; launched by `FieldUseFunc_ExpShare` in `src/party_menu.c` | `setflag FLAG_EXP_SHARE` / `clearflag FLAG_EXP_SHARE` (`0x906`) | `src/exp.c` checks `FlagGet(FLAG_EXP_SHARE)` under `#ifdef FLAG_EXP_SHARE`; party menu also reads it | `FLAG_EXP_SHARE` must remain defined |
| Portable PC field item | `system_scripts.s`, `SystemScript_Portable_PC_On` / `Off`; launched by `FieldUseFunc_PortablePC` | Reads `FLAG_PORTABLE_PC` (`0xA0B`) to choose on/off script | `src/party_menu.c` chooses PC script; script opens PC/heal party if flag set | `FLAG_PORTABLE_PC` must remain defined and item callback present |
| Option menu page 2 | `src/option_menu.c` | `VAR_R_BUTTON_MODE`, `VAR_BATTLE_MUSIC`, `VAR_WILD_LEVEL_SCALING`, `VAR_AUTO_SORT_BAG`, `VAR_GAME_DIFFICULTY` | `src/read_keys.c`, `src/battle_start_turn_start.c`, `src/wild_encounter.c`, `src/start_menu.c`, AI/battle code | Var macros must remain defined; individual code may also be `#ifdef` gated |
| Auto-run L-button toggle | `src/read_keys.c` | `FLAG_AUTO_RUN` toggled if `FLAG_RUNNING_ENABLED` is set | `src/overworld.c` `ShouldPlayerRun()` and `IsRunningDisabledByFlag()` | `FLAG_AUTO_RUN` and `FLAG_RUNNING_ENABLED` must remain defined |
| Running shoes gate | Source/scripts; example local script `assembly/overworld_scripts/viridian_city.s` sets `0x82F` | `FLAG_RUNNING_ENABLED` (`0x82F`) | `src/overworld.c` blocks running when flag not set | If `FLAG_RUNNING_ENABLED` is undefined, running is always enabled per source |
| Wild level scaling | Option menu writes `VAR_WILD_LEVEL_SCALING` | `0`/`1` | `src/wild_encounter.c` scales random wild levels when var is `1` | `VAR_WILD_LEVEL_SCALING` currently defined; old flag-based check is commented in one path |
| Game difficulty | Option menu writes `VAR_GAME_DIFFICULTY` | `0..3` | AI, wild, trainer-building, move menu, damage/accuracy and Hall of Fame code | `VAR_GAME_DIFFICULTY` currently defined |
| Hard level cap | Script/source controlled flag, no specific NPC found in this review | `FLAG_HARD_LEVEL_CAP`, `FLAG_KEPT_LEVEL_CAP_ON` | `src/exp.c`, `src/party_menu.c`, `src/daycare.c`, `src/dexnav.c`, `src/battle_start_turn_start.c` | Flags must remain defined |
| Tera type NPC/test scripts | `assembly/overworld_scripts/Pallet_town.s`, `EventScript_ChangeTeraTypeNPC` | Uses temporary vars `0x8001/0x8002/...` and callasm `ChangeTeraTypeInOW` | `src/terastallization.c` helpers use `VarGet(Var8002)` / `VarGet(Var8001)` | `TERASTAL_FEATURE` and related code must remain enabled |
| Hidden item pickup replacement | `system_scripts.s`, `SystemScript_PickedUpHiddenItem` | Uses hidden-item variables and `special 0x96` SetHiddenItemFlag | `src/scripting.c` optional item sprite functions | `ITEM_PICTURE_ACQUIRE` required for sprite popup; no separate sparkle toggle found for hidden items |

I did not find a general "settings NPC" that owns all runtime options. In this checkout, global runtime options are mainly the option menu page 2 plus field item scripts. Some Pallet/Viridian scripts look like local test/demo NPC scripts and should not be treated as a stable global settings UI without an ingame map/script review.

## EXP-System Analysis

EXP is handled primarily by:

- `02_external/CFRU-expansion/src/exp.c`
- `02_external/CFRU-expansion/assembly/battle_scripts/fainting_battle_scripts.s`
- `02_external/CFRU-expansion/src/catching.c`
- `02_external/CFRU-expansion/src/Tables/experience_tables.c`
- supporting level-cap checks in `src/party_menu.c`, `src/daycare.c`, `src/dexnav.c` and `src/battle_start_turn_start.c`

### Formula and Toggles

| EXP Area | Classification | Current source state | Evidence | Result |
|---|---|---|---|---|
| Formula: flat vs scaled | CONFIG_ONLY | `FLAT_EXP_FORMULA` is defined | `ExpCalculator()` uses `#ifdef FLAT_EXP_FORMULA`; `#else` is "Scaled Formula Gens 5, 7" | Current source uses flat formula |
| Full Gen 3 standard formula | SOURCE_PATCH_REQUIRED | No single Gen 3 profile/toggle found | Current config still enables trainer boost, Gen7 base yield, capture EXP, affection boost and modern Exp Share path | Needs deliberate config/source patch |
| Gen 6+ Exp Share | RUNTIME_TOGGLE plus CONFIG_ONLY | `FLAG_EXP_SHARE` defined, runtime flag toggles active state | `exp.c` compiles new Exp Share loop only under `#ifdef FLAG_EXP_SHARE`; scripts set/clear flag `0x906` | Runtime on/off is possible if compiled in |
| Old held-item Exp Share path | CONFIG_ONLY | Activated only when `FLAG_EXP_SHARE` macro is not defined | `#ifndef FLAG_EXP_SHARE` uses held item `ITEM_EFFECT_EXP_SHARE` path | Requires rebuild and impacts field toggle |
| Old participant split | CONFIG_ONLY | `OLD_EXP_SPLIT` currently commented | Split divisor branches in `exp.c` | Requires rebuild |
| Trainer EXP boost | CONFIG_ONLY | `TRAINER_EXP_BOOST` defined | Trainer battle bonus goes from 10 to 15 | Requires rebuild to disable |
| Gen 7 base yields | CONFIG_ONLY | `GEN_7_BASE_EXP_YIELD` defined | `baseExp = gBaseExpBySpecies[...]` and `experience_tables.c` guarded by macro | Requires rebuild to use BaseStats `expYield` instead |
| Capture EXP | CONFIG_ONLY | `CAPTURE_EXPERIENCE` defined | Catch success script calls `getexp BANK_TARGET`; `catching.c` selects custom success script | Requires rebuild to disable |
| Affection boost | CONFIG_ONLY | `EXP_AFFECTION_BOOST` defined | Friendship >= 220 branch in `MonGetsAffectionBoost()` | Requires rebuild |
| Hard level cap | RUNTIME_FLAG plus CONFIG_ONLY | `FLAG_HARD_LEVEL_CAP` defined | `exp.c` returns minimal EXP above cap if flag set; Rare Candy/daycare/DexNav also check it | Runtime flag controls active cap |
| Wild level scaling | RUNTIME_TOGGLE | `VAR_WILD_LEVEL_SCALING` option menu value | `wild_encounter.c` chooses scaled levels when var is `1` | Runtime option, separate from EXP formula |

### Can Gen 3 Standard EXP Be Restored?

Not by one runtime variable or NPC script found in this review.

A conservative Gen 3-ish follow-up would need to decide and test at least:

- Keep `FLAT_EXP_FORMULA` defined.
- Disable or adjust `GEN_7_BASE_EXP_YIELD` if Gen 3 base yields are required.
- Disable `TRAINER_EXP_BOOST` if strict Gen 3 no trainer multiplier is desired; note the comment says the boost is pre-Gen 7, so Anton should decide whether "Gen 3 standard" means exact FireRed behavior or broader pre-Gen7 behavior.
- Disable `CAPTURE_EXPERIENCE`.
- Disable `EXP_AFFECTION_BOOST`.
- Decide whether to remove `FLAG_EXP_SHARE` compile-time path or keep it compiled but runtime-off by default.
- Decide whether hard level cap flags are part of the game design; they are separate from EXP formula but can suppress gained EXP.

Risks:

- Trainer EXP: `TRAINER_EXP_BOOST` changes trainer-vs-wild rewards.
- Wild EXP: `GEN_7_BASE_EXP_YIELD` changes base yields even with flat formula.
- Exp Share: compile-time `FLAG_EXP_SHARE` changes both distribution loop and field item semantics.
- Lucky Egg: base Lucky Egg boost is always in `exp.c`; optional `VAR_LUCKY_EGG_LEVEL` can further modify it if defined elsewhere.
- Level caps: `FLAG_HARD_LEVEL_CAP` can reduce EXP to `1` when active and also blocks Rare Candy leveling at cap.
- Level scaling: `VAR_WILD_LEVEL_SCALING` affects encounter levels, not EXP formula, but it indirectly changes EXP via defeated level.

## Settings Matrix for This Project

| Feature | Current source setting | Recommended setting | Reason | Follow-up |
|---|---|---|---|---|
| EXP formula | `FLAT_EXP_FORMULA` defined | Keep unless Anton wants scaled EXP | Current source already avoids Gen5/7 scaled formula | Document as already flat; no urgent patch |
| Gen 3 exact EXP | Mixed modern/current flags remain enabled | Separate small config/profile branch | Exact Gen3 requires more than formula macro | `analysis/gen3-exp-profile-design` then fix branch |
| Exp Share behavior | `FLAG_EXP_SHARE` compile path plus runtime flag `0x906` | Keep compiled; default runtime-off/on should be project decision | Gives local runtime flexibility; removal is more invasive | Decide stable profile default |
| Level-scaling EXP | No EXP formula runtime toggle; wild level scaling var exists | Treat as encounter scaling, not EXP setting | `VAR_WILD_LEVEL_SCALING` changes wild levels only | Keep documented in settings profile |
| Modern mechanics toggles | Many compile-time macros in `src/config.h` | Do not globally change yet | Wide impact across battle/items/forms | Separate mechanics-profile audit |
| NPC runtime toggles | Exp Share item script, Portable PC script, option menu vars; no one global settings NPC found | Prefer option menu / controlled scripts over ad hoc NPC edits | Better traceability | `analysis/cfru-runtime-options-map` if needed |
| Hidden item sparkle | Hidden item script replaced; item sprite popup only if `ITEM_PICTURE_ACQUIRE`; no direct hidden-sparkle toggle found | Do not claim available without source patch | Search found `CreateSparkleSprite` for follower/surf, not hidden item sparkle config | Separate visual feature branch if wanted |
| TM field item visuals | TM items are in TM case pocket; item sprite popup treats TM case specially when enabled | Needs UPR/FVX or field object visual investigation | CFRU config does not expose a yellow TM overworld toggle found in this review | `analysis/tm-field-object-visuals` |
| Faster FireRed intro | `SKIP_INTRO_CONTROLS_GUIDE` defined; `OAK_INTRO_SPECIES` compile-time | Source patch or randomizer-side misc tweak, not general CFRU runtime toggle | This only removes controls guide, not full intro skip | Keep UPR-FVX Misc Tweaks path documented |
| Text speed | SaveBlock option menu plus optional `INSTANT_TEXT` compile macro commented | Keep existing option behavior; avoid `INSTANT_TEXT` unless desired | Instant text comment warns about pacing effects | No immediate source patch |
| Running shoes / running indoors | `FLAG_RUNNING_ENABLED`, `FLAG_AUTO_RUN`, `CAN_RUN_IN_BUILDINGS` defined | Keep current compiled flexibility | Runtime flag controls running permission; indoor running allowed | Stable profile can set initial flag/script |
| PC potion | Not found as CFRU config in reviewed source | Treat as UPR-FVX Misc Tweaks, not CFRU/DPE config | Prior workspace evidence says Randomize PC Potion is UPR-FVX-side | No CFRU action |

## Patchability

| Wanted Feature | Compile-Time or Runtime? | Patch difficulty | Safe branch name | Recommendation |
|---|---|---|---|---|
| Gen-3 Standard EXP | Compile-time/source profile | Medium | `analysis/gen3-exp-profile-design` then `config/gen3-standard-exp-profile` | Design exact desired semantics first; no blind toggle |
| Faster FireRed Intro | Likely source/randomizer patch; `SKIP_INTRO_CONTROLS_GUIDE` is only partial | Medium | `analysis/faster-intro-source-map` | Use UPR-FVX misc tweak evidence as baseline before CFRU edits |
| Yellow TM Field Items | Unknown/source patch | Medium | `analysis/tm-field-object-visuals` | Confirm field object graphics source before implementation |
| Hidden Item Sparkle | Unknown/source patch | Medium | `analysis/hidden-item-sparkle-source-map` | Current hidden-item script supports optional item icon, not proven sparkle |
| NPC-configurable options | Runtime scripts plus compile-time prerequisites | Low/medium | `analysis/cfru-runtime-options-map` | Document exact flag/var ownership before adding NPCs |
| CFRU/DPE settings profile | Compile-time profile plus runtime defaults | Medium | `config/cfru-dpe-stable-settings-profile` | Best next config work after EXP decision |

## Recommendation

Next implementable work should be a documentation/design branch for the intended CFRU/DPE stable settings profile, with EXP as the first explicit decision. The current source already uses a flat EXP formula, so the immediate question is not "turn off scaled EXP" but whether Anton wants exact FireRed/Gen3 EXP semantics by disabling Gen7 base yields, capture EXP, affection EXP and possibly the Gen6 Exp Share path.

Document-only for now:

- Option menu runtime vars: R-button mode, battle music, wild level scaling, auto-sort bag and difficulty.
- Field-item runtime scripts: Exp Share and Portable PC.
- Running shoes / auto-run flag semantics.

Do not touch yet:

- Major battle mechanic macros such as Mega/Dynamax/Terastal.
- Expanded TM/HM/Tutor counts.
- Save expansion.
- DPE species/item tables.
- Hidden item sparkle or TM field object visuals without a separate source-map branch.

Suggested small follow-up branches:

1. `analysis/gen3-exp-profile-design`
2. `analysis/cfru-runtime-options-map`
3. `analysis/tm-field-object-visuals`
