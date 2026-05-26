# CFRU Difficulty Split Var/Mode Plan

## Scope

Branch: `analysis/cfru-difficulty-split-var-mode-plan`

This is a documentation-only implementation plan for the internal vars, enums, and helper boundaries needed before splitting CFRU's current difficulty behavior. No CFRU/DPE/UPR-FVX code, ROMs, saves, builds, screenshots, raw logs, private paths, or secrets were changed or documented.

This plan builds on `01_docs/analysis/cfru-difficulty-settings-ui-split-design.md`.

## Source Findings

### Existing difficulty and Smart AI storage

- `src/config.h:378` defines `VAR_GAME_DIFFICULTY` as `0x5157`.
- `include/global.h:167-173` defines the current difficulty values in saved/UI order: Normal `0`, Easy `1`, Hard `2`, Expert `3`.
- `src/option_menu.c:74-82`, `219-228`, `247-251`, and `343-347` show the current option menu stores one second-page `MENUITEM_GAME_DIFFICULTY` value directly in `VAR_GAME_DIFFICULTY`.
- `src/config.h:47` defines existing project-local `FLAG_SMART_TRAINER_AI` as `0xA0E`.
- `src/Battle_AI/ai_master.c:226-229` uses `FLAG_SMART_TRAINER_AI` only in trainer battles to add smart-ish AI flags.
- `assembly/overworld_scripts/Pallet_town.s:10-14` currently sets `0xA0E` as a local smoke activation for Smart Trainer AI.

### Existing var ranges

| Range / ID | Source | Current status | Plan |
| --- | --- | --- | --- |
| `0x4000..0x40FF` | `include/constants/vars.h:5`, `include/constants/vars.h:305` | Vanilla save vars; `VARS_COUNT` is 256 in `include/global.h:703-704`. | Do not allocate CFRU split settings here. |
| `0x8000..0x8014` | `include/constants/vars.h:307-331` | Special vars. | Do not allocate persistent settings here. |
| `0x5000..0x51FF` | `src/save.c:594-608` with `SAVE_BLOCK_EXPANSION` from `src/config.h:229` | Expanded save vars. `GetExpandedVarPointer()` accepts this range when save expansion is enabled. | Use this range for new persistent CFRU settings. |
| `0x5000..0x503D` | `src/config.h:17-31`, `85-118`, `185-190` | Existing CFRU vars for terrain, battle facility, player sprites, runtime-changeable, healing, mugshots, etc. | Do not use. |
| `0x5150`, `0x5151`, `0x5153..0x5159` | `src/config.h:345-349`, `355`, `365`, `378`, `387-388` | Current option/debug cluster: R button, battle music, wild level scaling, auto-sort, Pokevial, wild battle count, game difficulty, debug custom var/value. | Do not reuse. |
| `0x5152` | Gap between `VAR_BATTLE_MUSIC` and `VAR_WILD_LEVEL_SCALING`; `move_menu.c:2240-2241` references optional `VAR_ITEM_RESTRICTIONS` but config does not define it. | Looks locally free, but plausibly intended for item restrictions or another option-menu value. | Avoid unless explicitly assigned after a separate item-restrictions audit. |
| `0x515A..0x51FF` | No `#define VAR_...` hits in `src/config.h` for this range; non-source numeric hits were palette/address data and are not var definitions. | Locally free within expanded var storage. | Preferred allocation range for the split settings. |

Recommended new var IDs:

| New var | Proposed ID | Rationale |
| --- | --- | --- |
| `VAR_TRAINER_LEVEL_SCALING_MODE` | `0x515A` | First free ID after the existing `0x5150..0x5159` option/debug cluster. |
| `VAR_TRAINER_AI_PROFILE` | `0x515B` | Adjacent to level-scaling mode for the split settings. |
| `VAR_CFRU_SETTINGS_SCHEMA` | `0x515C` | Optional migration/version marker. Not required if all new mode vars use `0 = legacy/unset`, but useful if future UI needs a one-time migration marker. |

Do not introduce a new `VAR_CFRU_DIFFICULTY_MODE` in the first implementation. Keep `VAR_GAME_DIFFICULTY` as the backing store for `DifficultyMode` so old saves, scripts, Hall of Fame display, and the existing option-menu value keep the same meaning.

### Existing flag ranges

| Range / ID | Source | Current status | Plan |
| --- | --- | --- | --- |
| `0x001..0x8E0` plus system/trainer flags | `include/constants/flags.h:3-34`, `1317-1440`; `include/global.h:703-704` | Vanilla/temp/system/trainer flag space. | Do not allocate new split flags here. |
| `0x900..0x18FF` | `src/save.c:573-584` with save expansion | Expanded flags are addressable in this range. | Existing CFRU custom flags live here; new flags are possible but not needed for this split. |
| `0x900..0x942` | `src/config.h:33-70`, `85`, `190`, `198-201` | Existing CFRU battle, menu, facility, and randomizer flags. | Do not reuse. |
| `0xA00..0xA0E` | `src/config.h:335-399` plus `FLAG_SMART_TRAINER_AI` at `src/config.h:47` | Current local feature flags, including Smart Trainer AI at `0xA0E`. | Keep `0xA0E`; do not add more flags for mode storage. |
| `0xE00..0xEFF` | `src/config.h:70`, `wild_encounter.c:516-517` | Daily event flag block. | Do not use. |
| `0x1300` onward | `src/config.h:366` | Nuzlocke visited-area start. | Do not use for difficulty split. |

Recommended flag plan:

- Keep `FLAG_SMART_TRAINER_AI` as the legacy/script compatibility flag.
- Do not allocate a new flag for `TrainerAIProfile`.
- Do not use a flag as a migration sentinel unless a later implementation proves a var-only sentinel cannot cover the UI/save cases.

## Internal Modes

Use C-side enums with stable behavior names, and keep raw save encoding hidden behind helpers.

```c
enum DifficultyMode {
    DIFFICULTY_MODE_NORMAL = 0,
    DIFFICULTY_MODE_EASY,
    DIFFICULTY_MODE_HARD,
    DIFFICULTY_MODE_EXPERT,
};

enum TrainerLevelScalingMode {
    TRAINER_LEVEL_SCALING_OFF = 0,
    TRAINER_LEVEL_SCALING_EASY,
    TRAINER_LEVEL_SCALING_NORMAL,
    TRAINER_LEVEL_SCALING_HARD,
    TRAINER_LEVEL_SCALING_EXPERT,
};

enum TrainerAIProfile {
    TRAINER_AI_PROFILE_VANILLA = 0,
    TRAINER_AI_PROFILE_EASY,
    TRAINER_AI_PROFILE_NORMAL,
    TRAINER_AI_PROFILE_HARD,
    TRAINER_AI_PROFILE_EXPERT,
    TRAINER_AI_PROFILE_SMART_AI,
};
```

Raw save encoding for the new vars should reserve `0` as `legacy/unset`:

| Setting var | Raw `0` | Raw explicit values |
| --- | --- | --- |
| `VAR_TRAINER_LEVEL_SCALING_MODE` | Derive legacy behavior from `VAR_GAME_DIFFICULTY`. | `1=Off`, `2=Easy`, `3=Normal`, `4=Hard`, `5=Expert`. |
| `VAR_TRAINER_AI_PROFILE` | Derive legacy trainer-AI behavior from `VAR_GAME_DIFFICULTY` and existing `FLAG_SMART_TRAINER_AI`. | `1=Vanilla`, `2=Easy`, `3=Normal`, `4=Hard`, `5=Expert`, `6=Smart AI`. |

`VAR_GAME_DIFFICULTY` should keep current raw encoding: `0=Normal`, `1=Easy`, `2=Hard`, `3=Expert`.

## Helper Plan

### `GetGameDifficultyMode()`

Purpose: read and clamp `VAR_GAME_DIFFICULTY`.

Rules:

- Return `DIFFICULTY_MODE_NORMAL`, `EASY`, `HARD`, or `EXPERT` using the current CFRU enum order.
- Clamp out-of-range saved values to `DIFFICULTY_MODE_NORMAL`.
- This helper owns trainer power, player restrictions, and battle/wild rules from the previous mapping.
- It should not decide trainer level scaling or trainer AI profile.

### `GetTrainerLevelScalingMode()`

Purpose: read explicit trainer level scaling when set, otherwise preserve legacy behavior.

Rules:

- If `VAR_TRAINER_LEVEL_SCALING_MODE` is `0`, derive from `GetGameDifficultyMode()`:
  - legacy Easy -> `TRAINER_LEVEL_SCALING_EASY`
  - legacy Normal -> `TRAINER_LEVEL_SCALING_NORMAL`
  - legacy Hard -> `TRAINER_LEVEL_SCALING_HARD`
  - legacy Expert -> `TRAINER_LEVEL_SCALING_EXPERT`
- If raw value is `1..5`, return the explicit mode `Off/Easy/Normal/Hard/Expert`.
- Clamp invalid explicit values to legacy-derived behavior, not to Off, so corrupted values do not silently weaken existing saves.

Important boundary: CFRU's scaling-linked evolution in `build_pokemon.c:1531-1536` is not UPR-FVX Trainer Evolution. Keep it attached to `TRAINER_LEVEL_SCALING_EXPERT` only while that behavior is intentionally described as scaling-linked evolution. Do not wire UPR-FVX Better Movesets or Trainer Evolution into this helper.

### `GetTrainerAIProfile()`

Purpose: read explicit trainer AI profile when set, otherwise preserve legacy trainer-AI behavior.

Rules:

- If `VAR_TRAINER_AI_PROFILE` is `0`, derive trainer-battle AI profile from `GetGameDifficultyMode()`:
  - legacy Easy -> `TRAINER_AI_PROFILE_EASY`
  - legacy Normal -> `TRAINER_AI_PROFILE_NORMAL`
  - legacy Hard -> `TRAINER_AI_PROFILE_HARD`
  - legacy Expert -> `TRAINER_AI_PROFILE_EXPERT`
- If raw value is `1..6`, return the explicit mode `Vanilla/Easy/Normal/Hard/Expert/Smart AI`.
- Clamp invalid explicit values to legacy-derived behavior.
- Trainer-only helper uses should require `gBattleTypeFlags & BATTLE_TYPE_TRAINER` at the call site or inside a narrowly named helper.

Do not use `GetTrainerAIProfile()` for generic wild or raid AI in the first implementation. Current source has difficulty-coupled wild/raid AI gates in `battle_controller_opponent.c`, `ai_master.c`, `dynamax.c`, and raid repeated-move handling. To avoid accidental behavior changes, leave those gates on `GetGameDifficultyMode()` until a separate explicit Wild/Raid AI setting is designed.

### `IsSmartTrainerAIEnabled()`

Purpose: centralize Smart Trainer AI compatibility.

Rules:

- If `VAR_TRAINER_AI_PROFILE` is unset (`0`), return `FlagGet(FLAG_SMART_TRAINER_AI)` for legacy/script compatibility.
- If `VAR_TRAINER_AI_PROFILE` is explicit `Smart AI`, return true.
- If `VAR_TRAINER_AI_PROFILE` is any explicit non-Smart profile, return false even if the legacy flag remains set.
- This helper is trainer-only. It must not make wild Pokemon or raid bosses smart.

## Default and Migration Rules

### Existing saves

Existing saves that only have `VAR_GAME_DIFFICULTY` must keep old behavior until a new split setting is explicitly set:

- `VAR_GAME_DIFFICULTY` continues to drive `DifficultyMode`.
- `VAR_TRAINER_LEVEL_SCALING_MODE == 0` means "derive old level-scaling behavior from `VAR_GAME_DIFFICULTY`".
- `VAR_TRAINER_AI_PROFILE == 0` means "derive old trainer-AI behavior from `VAR_GAME_DIFFICULTY`; also honor `FLAG_SMART_TRAINER_AI` as the legacy trainer-only Smart AI override".

This avoids a one-time migration pass for old saves and avoids losing the old `Normal = 0` meaning.

### New explicit profiles

New UI/profile writes should set the split vars explicitly:

| Profile intent | Difficulty raw | Level scaling raw | AI profile raw | Smart flag |
| --- | --- | --- | --- | --- |
| Preserve legacy by difficulty | write `VAR_GAME_DIFFICULTY`; leave new vars `0` | `0` | `0` | legacy scripts may still set/read it |
| Explicit Normal baseline | `0` | `3` | `3` | optional clear |
| Ironmon/Vanilla profile requested here | `0` | `1` | `6` | optional clear; AI profile raw owns Smart AI |

The Ironmon/Vanilla profile therefore means:

- Difficulty: Normal/vanilla battle restrictions and trainer-power rules.
- Trainer Level Scaling: Off.
- Trainer AI Profile: Smart AI for trainers only.

### Compatibility decision

Recommended first implementation strategy:

1. Keep `VAR_GAME_DIFFICULTY` as the only difficulty backing var.
2. Add the two new mode vars at `0x515A` and `0x515B`.
3. Optionally reserve `0x515C` for schema/migration if the UI needs to distinguish "never opened split UI" from "explicitly selected legacy derive". If raw `0 = legacy/unset` is enough, do not use `0x515C` yet.
4. Replace direct reads gradually with helpers, preserving exact old behavior while new vars are unset.

## Risks

- `0x5152` looks locally unused but may be the intended home for `VAR_ITEM_RESTRICTIONS`; avoid it until item restrictions are audited.
- Existing `FLAG_SMART_TRAINER_AI` is currently set by a local Pallet Town smoke script. A later implementation should decide whether that script remains test-only, becomes profile UI plumbing, or is removed in a separate branch.
- Trainer AI and wild/raid AI are currently intertwined through difficulty in several files. This plan intentionally keeps `TrainerAIProfile` trainer-only for the first implementation to avoid accidental Wild/Raid AI changes.
- Scaling-linked evolution in CFRU runtime scaling can look similar to UPR-FVX Trainer Evolution, but they are separate layers. Do not merge them.
- The option menu currently has fixed second-page item counts. Adding two new controls may require UI layout work beyond just adding vars/helpers.
