# CFRU Hard Level Cap Menu Option Analysis

## Scope

Branch: `analysis/cfru-hard-level-cap-menu-option`

This is a documentation-only source analysis for exposing CFRU Hard Level Cap as the last practical Page-3 option in the CFRU option menu. No CFRU, DPE, UPR-FVX, Tracker, ROM, save, build, screenshot, raw log, hash, private path, secret, token, or `.env` data was changed or documented.

Requested source note: `01_docs/analysis/cfru-runtime-options-map.md` and `01_docs/analysis/cfru-dpe-config-runtime-settings-review.md` were not present on this branch or in fetched history under those exact names. The closest available runtime-options source was `01_docs/analysis/cfru-game-difficulty-map.md` on `analysis/cfru-runtime-options-map`; the config-runtime review branch did not contain a matching analysis file.

## Source Findings

### Flags and current storage

| Source | Finding |
| --- | --- |
| `02_external/CFRU-expansion/src/config.h:363-364` | Defines `FLAG_KEPT_LEVEL_CAP_ON = 0xA04` and `FLAG_HARD_LEVEL_CAP = 0xA05`. |
| `02_external/CFRU-expansion/src/config.h:347-392` | Project-local vars occupy `0x5150`, `0x5151`, `0x5153`, `0x5154`, `0x5155`, `0x5156`, `0x5157`, `0x5158`, `0x5159`, `0x515A`, and `0x515B`. `0x515C` is not currently defined in the audited CFRU source. |
| `02_external/CFRU-expansion/docs/cfru_feature_matrix.md:147` | Existing CFRU docs already classify `FLAG_NUZLOCKE`, `FLAG_HARD_LEVEL_CAP`, and `FLAG_KEPT_LEVEL_CAP_ON` as optional challenge-mode runtime flags requiring later investigation. |
| Exact source search | No `FLAG_HARD_LEVEL_CAP` or `FLAG_KEPT_LEVEL_CAP_ON` writer was found in scripts, items, or option-menu code. The only writer found was `FlagClear(FLAG_KEPT_LEVEL_CAP_ON)` in battle-start logic. |
| DPE / UPR-FVX exact search | No matching `GetCurrentLevelCap`, `FLAG_HARD_LEVEL_CAP`, or `FLAG_KEPT_LEVEL_CAP_ON` use was found in DPE or UPR-FVX. |

### Current cap calculation

`GetCurrentLevelCap()` is implemented in `02_external/CFRU-expansion/src/exp.c:90-107`.

`GetBadgeCount()` counts the eight badge flags `FLAG_BADGE01_GET` through `FLAG_BADGE08_GET` in `src/exp.c:59-88`. `GetCurrentLevelCap()` then maps badge count to:

| Badge count | Cap |
| ---: | ---: |
| `0` | `15` |
| `1` | `20` |
| `2` | `25` |
| `3` | `30` |
| `4` | `35` |
| `5` | `40` |
| `6` | `45` |
| `7` | `50` |
| `8` | `100` |

Therefore the cap before Brock is `15`. The cap rises only when badge flags increase the badge count; after all eight badges it becomes `100`.

## Affected Hard-Level-Cap Paths

| System | Source | Behavior when `FLAG_HARD_LEVEL_CAP` is set |
| --- | --- | --- |
| EXP gain | `src/exp.c:221-225`, `622-633`, `732-733`, `796-797` | A party mon at or above the current cap is treated as affected by hard cap. Initial battle EXP is reduced to effectively no gain, and subsequent level-up carryover EXP is stopped once the cap is reached. |
| Rare Candy | `src/party_menu.c:2813-2845` | Rare Candy has no level-up effect at `MAX_LEVEL` or at/above `GetCurrentLevelCap()`. It can still trigger evolution if the mon has an evolution target. |
| Daycare | `assembly/hooks/general_hooks.s:574-580`; `src/daycare.c:1088-1116` | Daycare step EXP is routed through `GetExperienceAfterDaycareSteps()`. If hard cap is enabled and the computed level would reach or exceed the cap, EXP is clamped to the cap level; if already at/above cap, no additional daycare EXP is added. |
| Wild level selection | `src/wild_encounter.c:93-180` | Normal wild encounter maximum level is clamped to the current cap. In the project-local `VAR_WILD_LEVEL_SCALING == 1` path, scaled wild levels are also capped before final min/max cleanup. |
| DexNav | `src/dexnav.c:1333-1355` | DexNav encounter level is `base + chain bonus`, with a rare `+10` bonus, but returns `GetCurrentLevelCap()` instead if hard cap is enabled and the generated level would exceed the cap. |
| Wild boss / catchable boss scaling | `src/build_pokemon.c:1578-1600` | `GetScaledWildBossLevel()` clamps catchable scaled bosses to the current cap when hard cap is enabled. |
| Battle start bookkeeping | `src/battle_start_turn_start.c:222-245`, `264-272` | At battle start, if the game is not cleared, hard cap is on, and `FLAG_KEPT_LEVEL_CAP_ON` is set, CFRU scans the party. If any non-egg mon is above the current cap, it clears `FLAG_KEPT_LEVEL_CAP_ON`. |

## Meaning of `FLAG_KEPT_LEVEL_CAP_ON`

`FLAG_KEPT_LEVEL_CAP_ON` is not a second enforcement flag. Enforcement checks use `FLAG_HARD_LEVEL_CAP`.

The only source-backed behavior found for `FLAG_KEPT_LEVEL_CAP_ON` is achievement/state tracking: `TryClearLevelCapKeptOn()` clears it at battle start if the player is in the main game, hard cap is enabled, the flag is still set, and any non-egg party mon is above the current cap.

No source writer was found that sets `FLAG_KEPT_LEVEL_CAP_ON`. That means a menu implementation must not blindly set it whenever Hard Cap is enabled unless the project explicitly wants to start or reset a "kept cap on" challenge tracking state from the option menu.

## Trainer Level Scaling Relationship

No direct `GetCurrentLevelCap()` use was found in the trainer party level-scaling path. The audited `build_pokemon.c` cap use is the wild boss / catchable boss cap path, not generic trainer level scaling.

This matters for UI semantics:

- Hard Level Cap controls player EXP/Rare Candy/Daycare and several wild/DexNav level ceilings.
- Trainer Level Scaling controls trainer levels separately via `VAR_TRAINER_LEVEL_SCALING_MODE`.
- Enabling Hard Level Cap does not, by itself, cap trainer scaling in the source-backed paths found here.

If trainer scaled levels must be bounded by the current cap, that should be a separate design decision. It should not be smuggled into the menu-only Hard Cap row.

## Existing UI Shape

Current Page 3 in `02_external/CFRU-expansion/src/option_menu.c`:

| Source | Finding |
| --- | --- |
| `src/option_menu.c:90-96` | Page 3 enum has `MENUITEM_TRAINER_LEVEL_SCALING`, `MENUITEM_TRAINER_AI_PROFILE`, and `MENUITEM_CANCEL_PAGE_3`. |
| `src/option_menu.c:105-118` | `struct OptionMenu` has `option_thirdPage[]` plus original-raw/dirty tracking for Level Scaling and Trainer AI. |
| `src/option_menu.c:156-160` | Page 3 labels are `Level Scaling`, `Trainer AI`, and `Cancel`. |
| `src/option_menu.c:256-278` | Page 3 value counts are `{6, 7, 0}` for `Auto/Off/Easy/Normal/Hard/Expert`, `Auto/Vanilla/Easy/Normal/Hard/Expert/Smart`, and Cancel. |
| `src/option_menu.c:597-606` | Page 3 value display already branches on the two split settings. |
| `src/option_menu.c:620-688` | Left/right mutates `option_thirdPage[]` and calls `MarkThirdPageOptionDirty()` for Page 3 settings. |
| `src/option_menu.c:720-745` | Page 3 up/down wraps between first setting and Cancel. |
| `src/option_menu.c:749-769` | R/L navigation reaches Page 3 and returns to Page 2. |
| `src/option_menu.c:835-865`; `strings/option_menu.string:19-20` | Page 3 footer text already exists and says Page 3 with L/R, pick, switch, and cancel hints. |

Page 3 can safely hold one more compact row:

1. `Level Scaling`
2. `Trainer AI`
3. `Hard Cap`
4. `Cancel`

The row count is smaller than Page 2 and should leave footer/cancel space intact.

## Menu Option Design

### Recommended UI: `Hard Cap = Auto / Off / On`

Use a new var, preferably `VAR_HARD_LEVEL_CAP_MODE = 0x515C`, with raw values:

| Raw | UI | Meaning |
| ---: | --- | --- |
| `0` | `Auto` | Legacy/script-owned. Do not change `FLAG_HARD_LEVEL_CAP` or `FLAG_KEPT_LEVEL_CAP_ON` on menu close. |
| `1` | `Off` | Explicitly clear `FLAG_HARD_LEVEL_CAP`. Do not set or reset `FLAG_KEPT_LEVEL_CAP_ON`. |
| `2` | `On` | Explicitly set `FLAG_HARD_LEVEL_CAP`. Do not automatically set `FLAG_KEPT_LEVEL_CAP_ON` unless a separate challenge-start flow is designed. |

Reasoning:

- Existing saves/scripts may already set or clear `FLAG_HARD_LEVEL_CAP`. `Auto` preserves that source of truth.
- Opening and closing the option menu must not accidentally clear or set script-owned flags.
- Off/On gives the player explicit runtime control.
- A var is useful because flags alone cannot distinguish "user explicitly chose Off" from "legacy/script Auto currently off".

### Why not only `Off / On`

`Off / On` is simpler but unsafe for migration. Loading current flag state and writing it back on close would silently convert script-owned or legacy behavior into explicit menu ownership. It also cannot preserve a future script that temporarily sets hard cap while the option menu remains in "legacy" behavior.

### Interaction with `FLAG_KEPT_LEVEL_CAP_ON`

Do not expose `FLAG_KEPT_LEVEL_CAP_ON` as the Page-3 row.

Recommended handling:

- `Auto`: leave both flags untouched.
- `Off`: clear only `FLAG_HARD_LEVEL_CAP`; leave `FLAG_KEPT_LEVEL_CAP_ON` untouched unless product explicitly decides turning cap off should fail/clear the challenge tracker immediately.
- `On`: set only `FLAG_HARD_LEVEL_CAP`; leave `FLAG_KEPT_LEVEL_CAP_ON` untouched.

If the project later wants an Ironmon-style "kept level cap on from start" badge/achievement, create a separate explicit challenge-start/reset workflow. The source currently only clears the kept flag; it does not prove safe rules for setting it.

## Implementation Plan

No code change in this branch. For a later implementation branch:

1. Define `VAR_HARD_LEVEL_CAP_MODE = 0x515C` in CFRU config, unless a schema var has already claimed `0x515C`.
2. Add a local `HardCapMode` raw convention for the option menu: `0=Auto`, `1=Off`, `2=On`.
3. Add Page-3 enum item `MENUITEM_HARD_LEVEL_CAP` before `MENUITEM_CANCEL_PAGE_3`.
4. Add label `Hard Cap` and values `Auto / Off / On` to `strings/option_menu.string` and `option_menu.c`.
5. Extend `option_thirdPage[]` count array from `{6, 7, 0}` to `{6, 7, 3, 0}`.
6. Add original-raw/dirty tracking for `VAR_HARD_LEVEL_CAP_MODE`, matching the existing split-setting pattern.
7. On load:
   - raw `0` displays `Auto`;
   - raw `1` displays `Off`;
   - raw `2` displays `On`;
   - invalid raw displays `Auto` and preserves original raw unless changed.
8. On unchanged close, preserve original raw and do not change flags.
9. On dirty close:
   - write selected raw to `VAR_HARD_LEVEL_CAP_MODE`;
   - for raw `1`, clear `FLAG_HARD_LEVEL_CAP`;
   - for raw `2`, set `FLAG_HARD_LEVEL_CAP`;
   - for raw `0`, do not change `FLAG_HARD_LEVEL_CAP`.
10. Do not modify EXP, Rare Candy, Daycare, DexNav, wild encounter, wild boss, or trainer-level-scaling behavior in the UI branch.

## Risks

- `0x515C` is currently free in the audited CFRU source, but it was previously mentioned as an optional CFRU settings schema var. Confirm it is still unclaimed immediately before implementation.
- `Auto` can display as `Auto` while the effective flag is currently on or off due to scripts. That is intentional compatibility, but the UI text should be accepted before implementation.
- `FLAG_KEPT_LEVEL_CAP_ON` has only a clear path in source. Setting it from the option menu could create false "kept cap on" state.
- Trainer Level Scaling is separate and is not capped by the hard-level-cap source paths found here. If users expect trainer levels to respect cap, that requires a separate source-backed change.
- Hard Cap affects wild, DexNav, Rare Candy, Daycare, EXP gain, and catchable wild bosses. A menu row is not just a display setting.

## Recommendation

Implement `Hard Cap = Auto / Off / On` as the last Page-3 option, backed by new `VAR_HARD_LEVEL_CAP_MODE = 0x515C`, and keep enforcement on the existing `FLAG_HARD_LEVEL_CAP`.

Do not use `FLAG_KEPT_LEVEL_CAP_ON` for menu state. Treat it as legacy challenge tracking and leave it untouched until a separate challenge-state design exists.
