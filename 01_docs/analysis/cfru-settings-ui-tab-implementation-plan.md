# CFRU Settings UI Tab Implementation Plan

## Scope

Branch: `analysis/cfru-settings-ui-tab-implementation-plan`

This is a documentation-only implementation plan for exposing the split CFRU difficulty settings in the CFRU option menu. No CFRU, DPE, UPR-FVX, ROM, save, build, screenshot, raw-log, hash, private-path, or secret data was changed or documented.

This plan builds on:

- `01_docs/analysis/cfru-difficulty-settings-ui-split-design.md`
- `01_docs/analysis/cfru-difficulty-split-var-mode-plan.md`

## Source Findings

### Current option-menu structure

`02_external/CFRU-expansion/src/option_menu.c` currently has two option pages:

| Source | Finding |
| --- | --- |
| `src/option_menu.c:61-83` | Page 1 and page 2 menu item enums are hard-coded. Page 2 currently has `R Button Mode`, `Battle Music`, `Wild Level Scaling`, `Auto Sort Bag`, `Game Difficulty`, and `Cancel`. |
| `src/option_menu.c:92-101` | `struct OptionMenu` stores page 1 values in `option[]` and page 2 values in `option_secondPage[]`, sized by the enum counts. |
| `src/option_menu.c:117-135` | Page item labels are fixed arrays indexed by menu item enum values. |
| `src/option_menu.c:194-225` | Page option value text arrays are fixed per setting. `sGameDifficultyOptions` is currently `Normal`, `Easy`, `Hard`, `Expert` in raw save order. |
| `src/option_menu.c:227-228` | Per-item value counts are positional fixed arrays. Page 2 currently uses `{3, 2, 2, 4, 4, 0}`. |
| `src/option_menu.c:247-251` | Page 2 load reads CFRU vars directly into `option_secondPage[]`; `MENUITEM_GAME_DIFFICULTY` reads `VAR_GAME_DIFFICULTY`. |
| `src/option_menu.c:343-347` | Page 2 close writes all stored values back to vars; `MENUITEM_GAME_DIFFICULTY` writes `VAR_GAME_DIFFICULTY`. |
| `src/option_menu.c:401-467` | Value display is a switch over page and menu item; page 2 values are drawn from `option_secondPage[selection]`. |
| `src/option_menu.c:469-581` | Left/right cycles the current setting by the count array; up/down wraps from first item to cancel and cancel to first item. |
| `src/option_menu.c:606-624` | Item labels are drawn for every item count entry, so adding rows only requires enum/array/count consistency, not another loop. |
| `include/options_menu.h:8-24` | Option menu entry points and long-called vanilla helpers are declared, but the menu item enums are local to `option_menu.c`. |

### Current split setting storage

| Source | Finding |
| --- | --- |
| `src/config.h:378` | `VAR_GAME_DIFFICULTY = 0x5157` remains the backing store for `DifficultyMode`. |
| `src/config.h:379` | `VAR_TRAINER_LEVEL_SCALING_MODE = 0x515A`; raw `0` is legacy/unset, explicit values are `enum TrainerLevelScalingMode + 1`. |
| `src/config.h:380` | `VAR_TRAINER_AI_PROFILE = 0x515B`; raw `0` is legacy/unset, explicit values are `enum TrainerAIProfile + 1`. |
| `include/global.h:175-200` | C-side modes are `DifficultyMode`, `TrainerLevelScalingMode`, and `TrainerAIProfile`. |
| `src/util.c:44-164` | Helpers derive legacy Level Scaling and AI Profile from `VAR_GAME_DIFFICULTY` while split vars are raw `0`; invalid raw values also fall back to legacy-derived behavior. |

### Current text availability

`option_menu.c` already references short option values for `Off`, `Easy`, `Normal`, `Hard`, and `Expert`. It does not currently define/reuse visible option-menu strings for `Trainer Level Scaling`, `Trainer AI Profile`, `Vanilla`, or `Smart AI`.

`include/strings.h` declares `gText_Smart`, but there is no source-visible `gText_SmartAI` or `gText_Vanilla` in the searched CFRU source tree. The implementation should therefore add local option-menu text constants for the new labels and values instead of depending on unrelated global contest/category text.

## UI Structure Decision

Use the existing second option-menu page as the CFRU Settings page for the first implementation. Do not add a third page/tab yet.

Reasoning:

- The existing second page already hosts CFRU/project-specific settings and `Game Difficulty`.
- The page loop is count-driven and can render additional rows if the enum, name array, count array, load/save, and display switch are kept consistent.
- Adding a new page would require broader navigation state, L/R behavior, page hint text, and likely long-called vanilla helper assumptions. That is not needed for the first split UI.
- Keeping the first implementation in page 2 reduces the blast radius and keeps the later UPR-FVX-facing CFRU Settings tab design separate from the in-ROM CFRU option menu.

Recommended page 2 order:

1. `R Button Mode`
2. `Battle Music`
3. `Wild Level Scaling`
4. `Auto Sort Bag`
5. `Difficulty`
6. `Level Scaling`
7. `Trainer AI`
8. `Cancel`

Use shorter in-ROM labels for fit:

- `Difficulty`
- `Level Scaling`
- `Trainer AI`

Keep the longer product/UI labels in external UI or documentation:

- `Difficulty`
- `Trainer Level Scaling`
- `Trainer AI Profile`

## Proposed UI Options

### Difficulty

| Field | Plan |
| --- | --- |
| Label | `Difficulty` or keep current `Game Difficulty` if text/layout risk is preferred. |
| Values | `Easy`, `Normal`, `Hard`, `Expert` in user-facing order. |
| Current raw storage | `VAR_GAME_DIFFICULTY`: `0=Normal`, `1=Easy`, `2=Hard`, `3=Expert`. |
| Display mapping | If user-facing order changes to Easy-first, map menu selection to raw difficulty explicitly instead of indexing `sGameDifficultyOptions` by raw value. |
| Save mapping | Write raw CFRU difficulty value to `VAR_GAME_DIFFICULTY`. |
| Legacy/unset behavior | None; this var is the canonical DifficultyMode backing store. |

Implementation note: the current menu displays `Normal`, `Easy`, `Hard`, `Expert` because raw save order is used directly. The requested UI order is `Easy`, `Normal`, `Hard`, `Expert`, so the implementation should either add conversion helpers or deliberately keep the current order and document the deviation. Prefer conversion helpers so the UI matches the requested order.

### Trainer Level Scaling

| Field | Plan |
| --- | --- |
| Label | `Level Scaling` in the ROM option menu; `Trainer Level Scaling` in external UI/docs. |
| Values | `Off`, `Easy`, `Normal`, `Hard`, `Expert`. |
| Backing var | `VAR_TRAINER_LEVEL_SCALING_MODE`. |
| Explicit raw save values | `1=Off`, `2=Easy`, `3=Normal`, `4=Hard`, `5=Expert`. |
| Raw `0` | Legacy/unset: helper derives the old behavior from `VAR_GAME_DIFFICULTY`. |
| Display when raw `0` | Show the helper-derived mode: legacy Easy -> `Easy`, legacy Normal -> `Normal`, legacy Hard -> `Hard`, legacy Expert -> `Expert`. |
| Save when raw `0` and unchanged | Preserve raw `0`; do not write an explicit value just because the option menu was opened. |
| Save after user changes value | Write explicit raw `menuSelection + 1`. |

Critical implementation detail: `CloseAndSaveOptionMenu()` currently writes every setting on close. For split vars, this would accidentally migrate legacy saves if the menu loads raw `0`, displays a derived mode, and then writes that derived mode back. Add dirty/original-raw tracking for split settings before saving them.

### Trainer AI Profile

| Field | Plan |
| --- | --- |
| Label | `Trainer AI` in the ROM option menu; `Trainer AI Profile` in external UI/docs. |
| Values | `Vanilla`, `Easy`, `Normal`, `Hard`, `Expert`, `Smart AI`. |
| Backing var | `VAR_TRAINER_AI_PROFILE`. |
| Explicit raw save values | `1=Vanilla`, `2=Easy`, `3=Normal`, `4=Hard`, `5=Expert`, `6=Smart AI`. |
| Raw `0` | Legacy/unset: helper derives Easy/Normal/Hard/Expert from `VAR_GAME_DIFFICULTY`; `IsSmartTrainerAIEnabled()` separately honors `FLAG_SMART_TRAINER_AI`. |
| Display when raw `0` | Show the helper-derived profile from `GetTrainerAIProfile()`. Do not display `Smart AI` solely because `FLAG_SMART_TRAINER_AI` is set; that flag is a compatibility override, not a full explicit profile var. |
| Save when raw `0` and unchanged | Preserve raw `0`; do not write explicit profile just because the option menu was opened. |
| Save after user changes value | Write explicit raw `menuSelection + 1`. |

Open UX caveat: legacy raw `0` plus `FLAG_SMART_TRAINER_AI` can make Smart Trainer AI behavior active while the displayed derived profile remains Easy/Normal/Hard/Expert. That is accurate to the current compatibility model. A later Advanced/Debug view can expose legacy flag status if needed.

## Option-Menu Implementation Plan

### Shared helpers

Add small local conversion helpers in `option_menu.c` rather than duplicating raw math at every load/save/display call site:

- `static u16 DifficultyRawToMenuSelection(u16 raw)`
- `static u16 DifficultyMenuSelectionToRaw(u16 selection)`
- `static u16 TrainerLevelScalingRawToMenuSelection(u16 raw)`
- `static u16 TrainerLevelScalingMenuSelectionToRaw(u16 selection)`
- `static u16 TrainerAIProfileRawToMenuSelection(u16 raw)`
- `static u16 TrainerAIProfileMenuSelectionToRaw(u16 selection)`

For split vars, raw-to-menu should use helper-derived modes when raw is `0` or invalid. Menu-to-raw should write explicit `enum + 1` only after the user changes that option.

### Preserve legacy/unset without accidental migration

Add dirty/original tracking for the two split settings. Two implementation shapes are acceptable:

1. Add per-setting original raw fields and dirty bits to `struct OptionMenu`.
2. Add a small `splitSettingDirty[]`/`splitSettingOriginalRaw[]` array keyed by split menu item.

Rules:

- On load, store original raw values for `VAR_TRAINER_LEVEL_SCALING_MODE` and `VAR_TRAINER_AI_PROFILE`.
- Convert raw values to display selections.
- In `OptionMenu_ProcessInput()`, mark split setting dirty only when left/right changes that item.
- In `CloseAndSaveOptionMenu()`, if original raw was `0` and dirty is false, write raw `0` back or skip writing the split var.
- If dirty is true, write explicit raw value from the current menu selection.
- If original raw was explicit and dirty is false, write the same explicit raw value back.

This keeps existing saves compatible and makes the first explicit UI change the point where the split var becomes explicit.

### Page 2 additions

Implementation touch points in `src/option_menu.c`:

| Area | Required change |
| --- | --- |
| Menu enum | Add `MENUITEM_TRAINER_LEVEL_SCALING` and `MENUITEM_TRAINER_AI_PROFILE` before `MENUITEM_CANCEL_PAGE_2`. |
| `struct OptionMenu` | Add original raw/dirty tracking for split vars. |
| Label externs/text | Add local strings or externs for `Level Scaling`, `Trainer AI`, `Vanilla`, and `Smart AI`. |
| `sOptionMenuItemsNames_SecondPage` | Add labels for the two new items. |
| Value arrays | Add `sTrainerLevelScalingOptions` and `sTrainerAIProfileOptions`. |
| `sOptionMenuItemCounts_SecondPage` | Update to include counts `5` and `6` for the new items. |
| `CB2_OptionsMenuFromStartMenu()` | Load raw split vars, store originals, and convert to display selections. |
| `CloseAndSaveOptionMenu()` | Write split vars using dirty/original rules. |
| `BufferOptionMenuString()` | Add display cases for the new item values. |
| `OptionMenu_ProcessInput()` | Mark split vars dirty when changed. |

The existing page-switch behavior can remain L/R: page 1 -> page 2 via R, page 2 -> page 1 via L.

## Implementation Order

### Step 1: Trainer Level Scaling display/write

Implement only `Trainer Level Scaling` first.

- Add one menu item and value array.
- Add raw/display conversion for `VAR_TRAINER_LEVEL_SCALING_MODE`.
- Add dirty/original tracking.
- Verify that raw `0` remains raw `0` after opening and closing the menu without changing the setting.
- Verify that changing the item writes explicit raw `1..5`.

This is the safest first UI step because level-scaling behavior is already isolated behind `GetTrainerLevelScalingMode()`.

### Step 2: Trainer AI Profile display/write

Add `Trainer AI Profile` after Level Scaling.

- Reuse the dirty/original tracking pattern.
- Add `Vanilla` and `Smart AI` display text.
- Verify raw `0` remains raw `0` when unchanged.
- Verify explicit non-Smart profiles override the legacy `FLAG_SMART_TRAINER_AI` through existing helper behavior.
- Verify explicit `Smart AI` writes raw `6`.

Do not change Wild/Raid AI behavior or Smart Trainer AI flag scripts in this step.

### Step 3: Difficulty display order

After split vars work, decide whether to change the Difficulty display order from current raw order `Normal/Easy/Hard/Expert` to requested UI order `Easy/Normal/Hard/Expert`.

- If changed, add explicit raw/display conversion for `VAR_GAME_DIFFICULTY`.
- If not changed, document that in-ROM raw order was preserved and external UI can still present Easy-first.

### Step 4: Later Custom/Advanced settings

Do not add these in the first implementation:

- Better Movesets
- Trainer Evolution
- Wild/Raid AI profile
- CFRU runtime randomized-trainer evolution toggle
- Schema var UI
- Debug display for raw legacy/unset values

Those need separate product decisions and source-backed behavior plans.

## Risks

- The current option menu has no dirty tracking, so split vars can lose `0 = legacy/unset` unless the implementation explicitly preserves raw `0`.
- Long labels may overlap the value column. Use short ROM labels (`Level Scaling`, `Trainer AI`) or audit text widths before using full labels.
- Adding two rows to page 2 likely fits the existing loop, but the layout should still be verified in a ROM-free build/syntax pass and later visually in-game by the maintainer.
- `sOptionMenuItemsNames_SecondPage` is currently declared with `[MENUITEM_COUNT]` rather than `[MENUITEM_PAGE2_COUNT]`. It works today because page 2 has no more entries than page 1; adding two page-2 items may require resizing that array to `MENUITEM_PAGE2_COUNT`.
- Legacy `FLAG_SMART_TRAINER_AI` is not a full explicit `Smart AI` profile. The UI should not silently collapse that distinction.
- No Better Movesets or Trainer Evolution options belong in CFRU; those remain UPR-FVX Randomizer settings.
