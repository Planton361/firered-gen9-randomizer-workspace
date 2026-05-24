# CFRU/DPE Runtime Options Map

Branch: `analysis/cfru-runtime-options-map`

Scope: documentation-only source review of local CFRU/DPE runtime options, compile-time options, existing script/menu/field-item surfaces and whether a source-backed Settings NPC would be useful. No ROMs, builds, generated output, raw logs, private paths or hashes were used.

## Executive Summary

CFRU/DPE settings in this workspace fall into three practical groups:

- Compile-time macros and numeric constants in `02_external/CFRU-expansion/src/config.h`. These are changed by editing source and rebuilding. They control table dimensions, mechanics, UI behavior, EXP profile pieces and feature availability.
- Runtime flags/vars declared in `src/config.h` and read through `FlagGet`, `FlagSet`, `FlagClear`, `VarGet` and `VarSet`. These can be changed by scripts, field item callbacks, source-backed UI or the option menu, but only while their compile-time code paths remain present.
- Existing runtime surfaces: the expanded option menu, field item callbacks for key items, general system scripts and several Pallet/Viridian demo-style overworld scripts.

The most mature runtime surface is the option menu second page in `src/option_menu.c`. It already writes R-button mode, battle music, wild level scaling, bag auto-sort and game difficulty. Exp Share and Portable PC are handled as field items through `src/party_menu.c` and `assembly/overworld_scripts/system_scripts.s`. Auto-run is toggled with the L button in `src/read_keys.c` when running is enabled.

A Settings NPC is useful only for runtime flags/vars that are not already ergonomically covered by the option menu or field items. Good candidates are Exp Share, Portable PC, Auto Run, Running Enabled and Hard Level Cap. Compile-time-only features such as the EXP formula profile, expanded TM/HM counts, reusable TMs, hidden item visual behavior, major battle mechanic macros and faster intro controls cannot be made real runtime options by an NPC without source support.

I did not find a stable all-purpose settings NPC or mother settings script in the reviewed CFRU/DPE source. Pallet and Viridian scripts exist, but several look like demo/test helpers that grant Pokemon/items, set feature flags or exercise Tera/follower behavior. A production settings interface should therefore be source-backed and reviewable in Git, not a Hex Maniac-only ROM edit.

## Runtime Option Inventory

| Option | Flag/Var | Values | Existing setter | Existing reader | Current default/source | NPC suitable? | Risk |
|---|---|---|---|---|---|---|---|
| Exp Share | `FLAG_EXP_SHARE` (`0x906`) | Flag clear/set | `FieldUseFunc_ExpShare` in `src/party_menu.c` launches `SystemScript_Exp_Share_On` / `Off` in `system_scripts.s` | `src/exp.c` checks `FlagGet(FLAG_EXP_SHARE)` under the compile-time macro; party menu checks it to choose toggle script | Runtime flag default is save/story dependent; compile-time path is enabled by `src/config.h` | Yes | Medium/high: affects team-wide EXP distribution and interacts with EXP profile macros |
| Portable PC | `FLAG_PORTABLE_PC` (`0xA0B`) | Flag clear/set | Example Pallet script sets `0xA0B`; field item itself reads the flag and opens on/off script | `FieldUseFunc_PortablePC` and `SystemScript_Portable_PC_On` / `Off` | Runtime flag default is save/story dependent; key item exists as `ITEM_PORTABLE_PC` | Yes | Medium: opens PC/heal behavior from field item and affects access/balance |
| Wild Level Scaling | `VAR_WILD_LEVEL_SCALING` (`0x5153`) | `0` Off, `1` On | Option menu second page | `src/wild_encounter.c` in `ChooseWildMonLevel()` | Option menu var; default not proven without ROM/save init | Yes, but option menu already covers it | Medium: changes wild encounter levels and indirectly EXP |
| Game Difficulty | `VAR_GAME_DIFFICULTY` (`0x5157`) | `0` Normal, `1` Easy, `2` Hard, `3` Expert | Option menu second page | Many readers in AI, trainer building, battle calculations, wild encounter logic, move menu and Hall of Fame | Option menu var; default not proven without ROM/save init | Maybe | High: broad gameplay and AI surface |
| Auto Run | `FLAG_AUTO_RUN` (`0x914`) | Flag clear/set | L-button toggle in `src/read_keys.c` if running is enabled; system scripts show enable/disable messages | `src/overworld.c` `ShouldPlayerRun()` | Runtime flag default is save/story dependent | Yes | Low/medium: input expectation change; conflicts with L=A per config comment |
| Running Enabled | `FLAG_RUNNING_ENABLED` (`0x82F`) | Flag clear/set | Script-controlled; local Viridian demo script sets `0x82F` | `src/read_keys.c` gates auto-run toggle; `src/overworld.c` blocks running if unset | If macro is removed, running is always enabled; current macro requires flag | Maybe | Medium: story/progression semantics for running shoes |
| Hard Level Cap | `FLAG_HARD_LEVEL_CAP` (`0xA05`), `FLAG_KEPT_LEVEL_CAP_ON` (`0xA04`) | Flag clear/set | No stable player-facing setter found in this source review | `src/exp.c`, `src/party_menu.c`, `src/daycare.c`, `src/dexnav.c`, `src/battle_start_turn_start.c`, `src/build_pokemon.c` | Runtime flag default is save/story dependent; compile-time macro is present | Maybe | High: can suppress EXP, Rare Candy/daycare leveling and encounter levels above cap |
| R Button Mode | `VAR_R_BUTTON_MODE` (`0x5150`) | DexNav, Pokemon menu, Items menu | Option menu second page; DexNav registration can set DexNav mode | `src/read_keys.c`, `src/dexnav.c` | Option menu var; default not proven without ROM/save init | Usually no | Low/medium: already user-facing in option menu |
| Battle Music | `VAR_BATTLE_MUSIC` (`0x5151`) | FRLG, RSE | Option menu second page | `src/battle_start_turn_start.c` chooses trainer/wild battle music | Option menu var; default not proven without ROM/save init | Usually no | Low: cosmetic/audio preference |
| Auto Sort Bag | `VAR_AUTO_SORT_BAG` (`0x5154`) | Off, ByName, ByType, ByAmount | Option menu second page | `src/start_menu.c` sorts bag pockets before opening the bag | Option menu var; default not proven without ROM/save init | Usually no | Low/medium: can reorder bag unexpectedly |
| Text Speed | `gSaveBlock2->optionsTextSpeed` | Slow, Mid, Fast | Standard option menu page | Text printer/menu helpers use the saveblock option; `INSTANT_TEXT` is separate compile-time macro | Vanilla-style saveblock option | No | Low: already standard option menu behavior |
| Battle Scene / Style / Sound / Button Mode / Frame | SaveBlock2 option fields | Standard option values | Standard option menu page | Standard engine/UI readers | Vanilla-style saveblock options | No | Low: already standard option menu behavior |
| Fast Battle Messages | `FLAG_FAST_BATTLE_MESSAGES` (`0x925`) | Flag clear/set | No stable player-facing setter found in this source review | `src/general_bs_commands.c` checks flag under compile-time macro | Runtime flag exists, default not proven | Maybe | Medium: battle text timing and pacing |
| Battle Team Preview Trigger | `FLAG_IN_BATTLE_TEAM_PREVIEW` (`0xA00`) | Flag clear/set | No stable player-facing setter found in this source review | Battle trigger code under `TEAM_PREVIEW_TRIGGER` | Runtime flag exists, default not proven | Maybe | Medium: battle information/balance |
| Last Used Ball Trigger | `FLAG_ALWAYS_SHOW_LAST_BALL` (`0xA01`) | Flag clear/set | No stable player-facing setter found in this source review | Battle ball shortcut code under `LAST_USED_BALL_TRIGGER` | Runtime flag exists, default not proven | Maybe | Low/medium: convenience feature |
| Tera Battle Enable | `FLAG_TERA_BATTLE` (`0xA08`) | Flag set before trainerbattle | Script-controlled battle setup | Terastal battle code when `TERASTAL_FEATURE` is compiled | Terastal compile-time feature is enabled | No for global settings menu | High: battle-specific mechanic flag, not a general profile toggle |

## Existing Runtime Surfaces

### Option Menu

Primary file: `02_external/CFRU-expansion/src/option_menu.c`

What it sets:

- Standard saveblock options: text speed, battle scene, battle style, sound, button mode and frame.
- CFRU second-page vars: `VAR_R_BUTTON_MODE`, `VAR_BATTLE_MUSIC`, `VAR_WILD_LEVEL_SCALING`, `VAR_AUTO_SORT_BAG` and `VAR_GAME_DIFFICULTY`.

What it does not set:

- Exp Share, Portable PC, Auto Run, Running Enabled, Hard Level Cap, Fast Battle Messages, Team Preview trigger or Last Used Ball trigger.
- Compile-time mechanics or table-size macros.

Project fit:

- Best current surface for player-adjustable preferences.
- Suitable for options that are already low-risk and repeatedly user-facing.
- Duplicating these options in an NPC is unnecessary unless the project wants one central "profile" menu early in the game.

### Field Items

Primary files:

- `02_external/CFRU-expansion/src/party_menu.c`
- `02_external/CFRU-expansion/assembly/overworld_scripts/system_scripts.s`
- `02_external/CFRU-expansion/src/Tables/item_tables.c`

Relevant behavior:

- `ITEM_EXP_SHARE` uses `FieldUseFunc_ExpShare`, which runs `SystemScript_Exp_Share_On` or `SystemScript_Exp_Share_Off` and sets/clears `FLAG_EXP_SHARE`.
- `ITEM_PORTABLE_PC` uses `FieldUseFunc_PortablePC`, which chooses `SystemScript_Portable_PC_On` or `SystemScript_Portable_PC_Off` based on `FLAG_PORTABLE_PC`.
- `ITEM_EVIV_DISPLAYER` uses a field-use function to open the EV/IV viewer.

What it does not set:

- The option menu vars.
- Compile-time behavior.
- Stable initial defaults for flags unless another source-backed script grants/sets them.

Project fit:

- Good for item-like toggles the player expects to use from the Bag.
- Less suitable as a general settings profile surface because it scatters settings across items.

### Scripts / NPCs

Primary files reviewed:

- `02_external/CFRU-expansion/assembly/overworld_scripts/system_scripts.s`
- `02_external/CFRU-expansion/assembly/overworld_scripts/Pallet_town.s`
- `02_external/CFRU-expansion/assembly/overworld_scripts/viridian_city.s`

Observed behavior:

- `system_scripts.s` contains general system scripts for Exp Share, Portable PC, Auto Run messages and field menu entry points.
- `Pallet_town.s` contains local scripts that set feature flags such as follower/prebattle/Portable PC flags, grant Pokemon/eggs and expose a Tera type NPC flow.
- `viridian_city.s` contains a demo-style script that grants items/Pokemon and sets `0x82F` (`FLAG_RUNNING_ENABLED`).

What they do not prove:

- They do not prove a stable project settings NPC already exists.
- They do not prove map object placement or story availability without a ROM/map review, which was out of scope.

Project fit:

- Source-backed scripts are the right mechanism for a future settings NPC.
- Demo/test scripts should not be treated as final project settings UI.

### Mother / Pallet Scripts

Search found Mom/Mother object constants and Pallet scripts, but no dedicated source-backed "mother as settings menu" script in the reviewed local CFRU/DPE source. `MAP_PLAYER_HOME` is defined in `src/config.h`, and `overworld.c` uses it for whiteout text handling, but that is not a settings UI.

Using the mother as a settings NPC is feasible as a design choice, but it would require a source-backed map/script change. It should not be done as a private Hex Maniac-only edit if the setting behavior is meant to be reproducible and reviewed.

### Debug / Demo Surfaces

Debug and demo-like code exists, including `src/debug_menu.c`, Pallet scripts, Viridian scripts and several system scripts. These are useful as source examples for how to set flags/vars, but they are not a stable player-facing settings profile by themselves.

## Compile-Time-Only Settings

| Feature | Macro/Config | Why compile-time | Runtime NPC possible? | Recommendation |
|---|---|---|---|---|
| EXP formula/profile pieces | `FLAT_EXP_FORMULA`, `OLD_EXP_SPLIT`, `TRAINER_EXP_BOOST`, `GEN_7_BASE_EXP_YIELD`, `CAPTURE_EXPERIENCE`, `EXP_AFFECTION_BOOST` | `src/exp.c`, battle scripts and tables compile different code paths | Not as true runtime formula selection | Keep as separate config/source profile decision |
| Expanded TM/HM counts | `EXPANDED_TMSHMS`, `NUM_TMS`, `NUM_HMS` | Affects table sizes, bitsets, item mapping and compatibility assumptions | No | Do not expose via NPC |
| Expanded move tutors | `EXPANDED_MOVE_TUTORS`, `NUM_MOVE_TUTORS`, `LAST_TOTAL_TUTOR_NUM` | Affects tutor table dimensions and compile-time constants | No | Do not expose via NPC |
| Mega/Dynamax/Terastal feature availability | `MEGA_EVOLUTION_FEATURE`, `DYNAMAX_FEATURE`, `TERASTAL_FEATURE` | Adds/removes feature code, forms, items and battle UI paths | Only battle-specific runtime flags after feature is compiled | Keep compile-time; no generic runtime toggle |
| Reusable TMs / deletable HMs | `REUSABLE_TMS`, `DELETABLE_HMS` | Item behavior and assumptions are compiled | No practical NPC toggle | Keep source-profile controlled |
| Hidden item visuals / item popups | `ITEM_PICTURE_ACQUIRE`, `ITEM_DESCRIPTION_ACQUIRE`; hidden item script calls sprite helpers when compiled | Popup rendering code is compile-time gated; current hidden item script is not a general sparkle setting | Not without new source code | Separate source-map branch before changes |
| Yellow TM field item visuals | No runtime setting found; likely field object graphics/table/source work | Field object visual behavior is not exposed as a flag/var in reviewed source | Not without source work | Analyze separately |
| Faster intro / control guide | `SKIP_INTRO_CONTROLS_GUIDE`, `OAK_INTRO_SPECIES`; full faster intro not exposed as runtime setting | Intro behavior is source/config/randomizer-side behavior | No | Analyze separately; current macro is only partial |
| Text behavior macros | `INSTANT_TEXT`, `AUTOSCROLL_TEXT_BY_HOLDING_R`, `EXPANDED_TEXT_BUFFERS` | Changes text printer behavior at compile time | Standard text speed is runtime; these macros are not | Keep compile-time |
| Major battle mechanics | `OLD_BURN_DAMAGE`, `OLD_PARALYSIS_SPD_DROP`, `OLD_MOVE_SPLIT`, `OLD_CRIT_DAMAGE`, terrain/weather/capture macros and similar | Battle code compiles different rules | No | Do not expose via NPC without a deliberate mechanics profile |
| Save expansion | `SAVE_BLOCK_EXPANSION` | Config comment warns removing it requires hook removal and breaks features | No | Do not touch |
| Randomizer flags | `FLAG_POKEMON_RANDOMIZER`, `FLAG_POKEMON_LEARNSET_RANDOMIZER`, `FLAG_ABILITY_RANDOMIZER` | Runtime flags exist, but they belong to CFRU in-game creation behavior, not UPR-FVX profile options | No for player settings NPC | Keep separate from UPR-FVX randomization workflow |

## Settings-NPC Design Options

| Approach | Pros | Cons | Reproducibility | Risk | Recommendation |
|---|---|---|---|---|---|
| No NPC; use existing Option Menu | Uses already implemented UI for R-button, battle music, wild scaling, bag sort, difficulty and standard options | Does not cover Exp Share, Portable PC, hard cap or running flags in one place | High | Low | Best default for options already present there |
| Add a dedicated Settings NPC | Centralizes project-specific flags and can document defaults in one script | Requires source-backed map/script work and careful menu text/state handling | High if done in source | Medium | Good follow-up if Anton wants one stable profile interface |
| Use the mother as Settings NPC | Early-game, thematically easy for initial settings/profile setup | Mixes story/home NPC with system settings; no existing dedicated script found | High only if source-backed | Medium | Plausible, but design first; avoid private-only ROM edit |
| Use Field Items as toggles | Already fits Exp Share and Portable PC | Poor for global profile options; depends on item access | High if source-backed | Low/medium | Keep for item-like features only |
| Hex Maniac prototype only | Fast local proof of NPC/menu placement | Not reviewable in Git, can drift from source and risks private ROM-offset documentation | Low | High for project state | Accept only as local throwaway prototype, not final workflow |
| Source-backed script change | Reviewable, reproducible, branchable and PR-friendly | Needs source build later and script discipline | High | Medium | Preferred implementation path |

## Suggested Settings-NPC Menu

A Settings NPC is sensible if it only exposes real runtime flags/vars and does not duplicate the normal option menu too aggressively.

Good menu candidates:

- Exp Share: On/Off via `FLAG_EXP_SHARE`.
- Portable PC: On/Off via `FLAG_PORTABLE_PC`, if this is intended to be globally available.
- Auto Run: On/Off via `FLAG_AUTO_RUN`.
- Running Enabled: On/Off via `FLAG_RUNNING_ENABLED`, or set once after intro/running-shoes acquisition.
- Hard Level Cap: On/Off via `FLAG_HARD_LEVEL_CAP`; decide how `FLAG_KEPT_LEVEL_CAP_ON` should be handled before exposing it.
- Fast Battle Messages: On/Off via `FLAG_FAST_BATTLE_MESSAGES`, if the project wants faster battle pacing as a runtime preference.

Possible but already covered elsewhere:

- Wild Level Scaling: `VAR_WILD_LEVEL_SCALING`; already in option menu.
- Game Difficulty: `VAR_GAME_DIFFICULTY`; already in option menu and has wide behavior impact.
- Battle Music, R Button Mode and Auto Sort Bag: already in option menu.

Do not show as runtime options:

- EXP formula/profile pieces.
- Expanded TM/HM/Tutor counts.
- Mega/Dynamax/Terastal compile-time feature availability.
- Reusable TMs and deletable HMs.
- Hidden item visual behavior and yellow TM field visuals.
- Faster intro/source patch behavior.
- Save expansion or DPE table dimensions.

Default handling:

- This review did not read ROM/save init state, so it should not assert actual runtime defaults.
- A future stable settings profile should set desired initial runtime flags/vars through a source-backed initialization or early-game script and document those defaults next to the script.

## Hex Maniac vs Source-Backed

Hex Maniac is practical for a local prototype: finding a map object, proving an NPC can open a multichoice, or checking whether the mother is a good early-game interaction point. It is not a good final workflow for project settings because the edit can live only in a private ROM, can drift from source, and is hard to review without documenting offsets, ROM paths or private artifacts.

Source-backed changes are better for this project:

- The setting behavior is visible in Git.
- Branches and PRs can review exact flags/vars and text.
- Anton can rebuild from source later without recreating a manual ROM edit.
- The workspace can avoid private ROM paths, offsets, hashes and screenshots in documentation.

Use Hex Maniac only for local throwaway validation. Once the desired menu is known, implement the script or source changes in the CFRU/DPE source tree on a dedicated branch.

## Recommended Next Work Packages

1. `analysis/settings-npc-source-design`
2. `config/cfru-dpe-stable-settings-profile`
3. `analysis/tm-field-object-visuals`
4. `analysis/hidden-item-sparkle-source-map`
5. `analysis/faster-intro-source-map`

EXP should be covered as one decision inside the stable settings/profile work, but it should not be the only runtime-options follow-up.

## Handoff

Current source evidence supports a narrow conclusion: CFRU/DPE already has real runtime options, but they are split between the option menu, field items and script-controlled flags. A Settings NPC is technically reasonable for project-specific runtime flags, especially Exp Share, Portable PC, Auto Run, Running Enabled and Hard Level Cap. It cannot replace compile-time source/config decisions, and it should be source-backed rather than a Hex Maniac-only ROM edit.
