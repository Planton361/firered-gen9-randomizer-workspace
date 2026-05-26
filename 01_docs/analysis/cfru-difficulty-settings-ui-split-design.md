# CFRU Difficulty Settings UI Split Design

## Scope

Branch: `analysis/cfru-difficulty-settings-ui-split-design`

This is a documentation-only design. No CFRU, DPE, UPR-FVX, ROM, save, build, screenshot, raw-log, hash, private-path, or secret data was changed or documented.

The requested source search covered:

- `VAR_GAME_DIFFICULTY`
- `OPTIONS_EASY_DIFFICULTY`
- `OPTIONS_NORMAL_DIFFICULTY`
- `OPTIONS_HARD_DIFFICULTY`
- `OPTIONS_EXPERT_DIFFICULTY`

Exact-symbol results were found in `02_external/CFRU-expansion/**`. The same exact-symbol search found no matches in `02_external/Dynamic-Pokemon-Expansion-Gen-9/**` or `02_external/upr-fvx/**`.

## Current CFRU Model

CFRU currently uses one runtime var for multiple concerns. `src/config.h:378` defines `VAR_GAME_DIFFICULTY` as the difficulty var, with values described as normal/vanilla, easy, hard, and expert. `include/global.h:167-173` defines the actual enum order:

| Value | Current CFRU enum |
| --- | --- |
| `0` | `OPTIONS_NORMAL_DIFFICULTY` |
| `1` | `OPTIONS_EASY_DIFFICULTY` |
| `2` | `OPTIONS_HARD_DIFFICULTY` |
| `3` | `OPTIONS_EXPERT_DIFFICULTY` |

The option menu stores and restores this single var from `MENUITEM_GAME_DIFFICULTY` (`src/option_menu.c:80`, `src/option_menu.c:219-225`, `src/option_menu.c:251`, `src/option_menu.c:347`, `src/option_menu.c:458-459`). Hall of Fame display also reads the same var to print a difficulty label (`src/hall_of_fame.c:474-488`).

The important design constraint is that this single setting is not one behavior. It currently drives trainer power, trainer level scaling, AI behavior, player restrictions, raid/wild rules, and one randomizer-only evolution path.

## Mapping Table

| Source | Current behavior | Proposed category | Reason |
| --- | --- | --- | --- |
| `docs/cfru_feature_matrix.md:83` | Existing workspace note says the var affects friendship, EVs, IVs, AI style, and scaling decisions. | unklar/offen | Reference row, not runtime behavior. Keep as source index input. |
| `src/config.h:378` | Defines the shared runtime var. | unklar/offen | Shared plumbing. Future implementation should either keep this var only for `DifficultyMode` or migrate it with compatibility handling. |
| `include/global.h:167-173` | Defines Normal/Easy/Hard/Expert enum values. | unklar/offen | Shared enum plumbing. New split should not reuse one enum for all concerns. |
| `src/option_menu.c:80`, `219-225`, `251`, `347`, `458-459` | UI exposes and persists one Game Difficulty option. | unklar/offen | Existing UI plumbing must become separate controls. |
| `src/hall_of_fame.c:474-488` | Prints the current difficulty label in Hall of Fame. | Difficulty | Display should follow `DifficultyMode` unless later design wants a full settings summary. |
| `src/build_pokemon.c:793-795` | Expert forces opposing trainer IVs to 31. | Difficulty | Trainer power. |
| `src/build_pokemon.c:1097-1098` | Unbound Rival EV spread changes on Hard/Expert gates. | Difficulty | Trainer power. |
| `src/build_pokemon.c:1112-1113` | Easy suppresses configured trainer EV spread application. | Difficulty | Trainer power. |
| `src/build_pokemon.c:1186-1201`, `1278-1308`, `1310-1333`, `1615-1625` | Hard+ boss/rival classes can receive best-stat max EVs and max friendship. | Difficulty | Trainer power. |
| `src/build_pokemon.c:1336-1344` | Expert gives trainer moves max PP bonus. | Difficulty | Trainer power. |
| `src/wild_encounter.c:1506-1508` | Expert gives wild custom-move encounters max PP bonus. | Difficulty | Wild rule / enemy power. |
| `src/wild_encounter.c:1546-1547` | Unbound Shadow Warrior gets hidden ability on Expert. | Difficulty | Wild/special encounter power. |
| `src/party_menu.c:2601-2606` | Expert blocks a pre-clear hidden ability capsule edge case for Imposter in Unbound. | Difficulty | Player restriction. |
| `src/dexnav.c:1411-1416` | Expert blocks pre-clear DexNav hidden Imposter ability in Unbound. | Difficulty | Wild/player restriction. |
| `src/cmd49.c:1427-1435` | Raid boss can attack again after player item use, except Easy. | Difficulty | Battle/raid rule. |
| `src/move_menu.c:1874-1881` | Expert blocks player Minimize/evasion-up selection outside Frontier. | Difficulty | Player battle restriction. |
| `src/move_menu.c:2234-2272` | Hard limits trainer-battle item use to four; Expert disables items in trainer battles and some uncapturable non-raid battles. | Difficulty | Player restriction / battle rule. |
| `src/battle_util.c:2028-2033` | Expert applies sleep clause only against the player side. | Difficulty | Battle rule. |
| `src/accuracy_calc.c:512-519`, `623-630` | Easy reduces fog accuracy penalty before postgame outside Frontier. | Difficulty | Battle rule. |
| `src/dynamax.c:1663-1665` | Expert plus raid no-force-end flag starts raid shields up. | Difficulty | Wild/raid rule. |
| `src/end_turn.c:2025-2038` | Nightmare damage is harsher on Hard and harshest on Expert. | Difficulty | Battle rule. |
| `src/build_pokemon.c:859-870` | Easy disables trainer level scaling except Pokemon League and special partner/wild-boss cases. | Trainer Level Scaling | Direct level-scaling gate. |
| `src/build_pokemon.c:1409-1414` | Easy disables pseudo-boss classification for level scaling. | Trainer Level Scaling | Direct level-scaling classification. |
| `src/build_pokemon.c:1428-1433` | Easy disables boss trainer class classification for level scaling. | Trainer Level Scaling | Direct level-scaling classification. |
| `src/build_pokemon.c:1465-1468` | Easy still allows partner scaling in wild boss battles. | Trainer Level Scaling | Direct level-scaling exception. |
| `src/build_pokemon.c:1475-1505` | Expert uses a smaller level subtractor so trainers scale closer to the player average. | Trainer Level Scaling | Direct level-scaling formula. |
| `src/build_pokemon.c:1514-1518` | Hard+ enters average-team scaling even without the normal over-level threshold. | Trainer Level Scaling | Direct level-scaling trigger. |
| `src/build_pokemon.c:1531-1536` | Expert can force evolution after scaling for regular trainers. | Trainer Level Scaling | Scaling-linked evolution, separate from UPR-FVX's randomizer setting. |
| `src/build_pokemon.c:1575-1612` | Easy scales wild boss level below biased average; non-Easy scales to biased average + 1. | Trainer Level Scaling | Wild boss level-scaling rule. |
| `src/damage_calc.c:2424-2434` | AI knowledge of player weakness berries is hidden below Expert and in Frontier. | Trainer AI Profile | AI knowledge behavior. |
| `src/battle_controller_opponent.c:37-50` | Expert makes wild Pokemon use smart AI selection. | Trainer AI Profile | AI profile behavior, with open naming issue because current behavior includes wild AI. |
| `src/Battle_AI/ai_master.c:165-220` | Easy downgrades trainer AI; Hard/Expert upgrade regular trainer AI to semi-smart where needed. | Trainer AI Profile | Core trainer AI profile. |
| `src/Battle_AI/ai_master.c:1069-1072` | Hard+ makes `smartWild` species semi-smart. | Trainer AI Profile | AI profile behavior, again wild-inclusive. |
| `src/Battle_AI/ai_master.c:1577-1650` | Difficulty gates AI move rechoice and anti-switch/choice-lock cheese prediction. | Trainer AI Profile | AI prediction behavior. |
| `src/Battle_AI/ai_master.c:1726-1748` | Expert lets very smart doubles AI retarget through player Protect cheese. | Trainer AI Profile | AI counterplay behavior. |
| `src/Battle_AI/ai_master.c:1761-1768` | Easy prevents smart raid boss repeated-move selection. | Trainer AI Profile | AI move-choice behavior. |
| `src/Battle_AI/ai_negatives.c:161-169` | Easy lowers basic AI try-to-kill rate. | Trainer AI Profile | AI aggressiveness behavior. |
| `src/Battle_AI/ai_switching.c:45-48`, `2596-2639`, `2641-2660` | Difficulty-gated helper and Hard/Expert shift-switch logic. | Trainer AI Profile | AI switching behavior. |
| `src/build_pokemon.c:1079-1089` | When CFRU's Pokemon randomizer flag is active and not temp-disabled, non-Easy lets randomized trainer species evolve naturally by level. | Randomizer-only | This is tied to runtime randomizer state, not base difficulty. Future control should belong with Trainer Evolution randomizer settings. |
| `random/src/main/java/com/uprfvx/random/GameRandomizer.java:584-590` | UPR-FVX evolves trainer Pokemon when `isTrainersEvolveTheirPokemon()` is selected and trainers were not otherwise randomized in that branch. | Randomizer-only | Source-backed UPR-FVX Trainer Evolution setting. |
| `random/src/main/resources/com/uprfvx/random/gui/Bundle.properties:235-238` | UPR-FVX UI describes Trainer Evolution and its evolution-level modifier. | Randomizer-only | Existing randomizer UI, not CFRU runtime difficulty. |
| `random/src/main/java/com/uprfvx/random/GameRandomizer.java:606-611` | UPR-FVX runs trainer moveset randomization when any Better Movesets bucket is enabled. | Randomizer-only | Existing randomizer write-time behavior. |
| `random/src/main/resources/com/uprfvx/random/gui/Bundle.properties:714-720` | UPR-FVX UI exposes Better Movesets for boss, important, and regular trainers. | Randomizer-only | Existing randomizer UI, not CFRU runtime difficulty. |
| `random/src/main/java/com/uprfvx/random/gui/RandomizerGUI.java:3002-3013` | Better Movesets checkboxes are availability-gated by ROM handler support. | Randomizer-only | Existing randomizer capability gating. |

## Proposed Internal Modes

### `DifficultyMode`

Purpose: CFRU runtime difficulty for trainer power, player restrictions, and battle/wild rules. It should not own trainer level scaling, trainer AI profile, Better Movesets, or Trainer Evolution.

Suggested values:

| Mode | Intended source-backed behavior |
| --- | --- |
| `NORMAL` | Current `OPTIONS_NORMAL_DIFFICULTY` default/vanilla-compatible behavior. |
| `EASY` | Easy-side restrictions and gentler battle rules such as reduced fog penalty and lower raid/item punishment. |
| `HARD` | Hard trainer-power and battle-rule gates such as stronger EV/friendship treatment and limited trainer-battle item use. |
| `EXPERT` | Expert trainer power, item restrictions, evasion restriction, sleep-clause behavior, raid/wild hardening, max PP, and other hardest battle/wild rules. |

Implementation note for later: keeping `VAR_GAME_DIFFICULTY` as the backing var for `DifficultyMode` is the lowest-risk compatibility route, but only after every non-Difficulty read is moved to a new setting.

### `TrainerLevelScalingMode`

Purpose: CFRU runtime level scaling independent of the difficulty bundle.

Requested values:

| Mode | Intended source-backed behavior |
| --- | --- |
| `OFF` | Disable dynamic trainer/wild-boss level scaling regardless of difficulty. |
| `EASY` | Current Easy-style scaling: trainer scaling mostly off, final/special exceptions preserved only if intentionally desired, wild boss scaling below biased average. |
| `NORMAL` | Current Normal-style scaling gates and subtractors. |
| `HARD` | Current Hard-style trigger that allows average-team scaling more aggressively. |
| `EXPERT` | Current Expert-style closer scaling and scaling-linked evolution behavior. |

Open design detail: `src/build_pokemon.c:1531-1536` evolves after level scaling on Expert. That is not the same as UPR-FVX Trainer Evolution. Keep it in `TrainerLevelScalingMode` only if it remains explicitly "scaling-linked evolution"; otherwise split a separate CFRU runtime toggle before implementation.

### `TrainerAIProfile`

Purpose: CFRU runtime AI behavior independent of difficulty and level scaling.

Requested values:

| Mode | Intended source-backed behavior |
| --- | --- |
| `VANILLA` | Use ROM trainer AI flags with no difficulty-based upgrades/downgrades. |
| `EASY` | Current Easy-style AI downgrades: less good-move checking, lower kill rate, fewer smart repeated-move choices. |
| `NORMAL` | Current Normal behavior: ROM trainer AI flags plus CFRU baseline special battle handling. |
| `HARD` | Current Hard-style regular-trainer semi-smart upgrades, smartWild semi-smart handling, switch prediction gates, and Shift-style switch behavior. |
| `EXPERT` | Current Expert-style AI upgrades, wild smart AI, anti-cheese retargeting/rechoice, and semi-shift gates. |
| `SMART_AI` | Explicit opt-in maximum AI profile. This should be implemented as a named profile, not as "Expert difficulty", and must be audited against `AI_SCRIPT_CHECK_GOOD_MOVE` and Frontier/special-battle exceptions before code is changed. |

Naming risk: current source-backed AI gates include wild AI and raid behavior. The UI can still label the setting "Trainer AI Profile" if the help text clarifies that Expert/Smart may also affect CFRU enemy wild/raid AI paths, or the implementation can choose to split wild AI later.

## Proposed CFRU Settings Tab

Tab title: `CFRU Settings`

Section: `Runtime Battle Profile`

- `Difficulty`: segmented control or combo box with `Easy`, `Normal`, `Hard`, `Expert`.
- Scope text in tooltip only: trainer power, player restrictions, battle/wild rules.
- Do not mention Better Movesets or Trainer Evolution here.

Section: `Trainer Level Scaling`

- `Trainer Level Scaling`: combo box with `Off`, `Easy`, `Normal`, `Hard`, `Expert`.
- Optional read-only status line if CFRU scaling support is not detected.
- Keep separate from existing randomizer trainer level modifier because this is runtime scaling, not write-time ROM trainer-level editing.

Section: `Trainer AI Profile`

- `Trainer AI Profile`: combo box with `Vanilla`, `Easy`, `Normal`, `Hard`, `Expert`, `Smart AI`.
- Tooltip should clarify the source-backed boundary: AI flags, switch prediction, anti-cheese behavior, and CFRU enemy AI upgrades.

Section: `Randomizer-only Settings`

- Keep existing `Better Movesets for...` checkboxes: `Boss Trainers`, `Important Trainers`, `Regular Trainers`.
- Keep existing `Trainers Evolve their Pokemon` and its evolution-level modifier with the trainer randomizer settings.
- Do not write these settings into CFRU runtime difficulty vars.

Recommended layout order:

1. Difficulty
2. Trainer Level Scaling
3. Trainer AI Profile
4. Randomizer-only Settings

This order matches the requested mental model: base runtime challenge first, dynamic level behavior second, enemy decision quality third, UPR-FVX write-time trainer transformations last.

## Migration Design

Proposed symbolic backing vars for later implementation:

| Internal setting | Suggested CFRU backing |
| --- | --- |
| `DifficultyMode` | Keep `VAR_GAME_DIFFICULTY` if compatibility is required, otherwise introduce `VAR_CFRU_DIFFICULTY_MODE`. |
| `TrainerLevelScalingMode` | New `VAR_TRAINER_LEVEL_SCALING_MODE`. |
| `TrainerAIProfile` | New `VAR_TRAINER_AI_PROFILE`. |

Do not assign numeric var IDs in the design. A later implementation must audit the CFRU var range first.

UPR-FVX profile fields should use Java-side enums rather than booleans:

```java
enum DifficultyMode {
    NORMAL,
    EASY,
    HARD,
    EXPERT
}

enum TrainerLevelScalingMode {
    OFF,
    EASY,
    NORMAL,
    HARD,
    EXPERT
}

enum TrainerAIProfile {
    VANILLA,
    EASY,
    NORMAL,
    HARD,
    EXPERT,
    SMART_AI
}
```

## Open Risks

- The exact numeric CFRU var IDs for new settings are not assigned. This needs a var-range audit before implementation.
- "Trainer AI Profile" is a narrower label than the source behavior. CFRU currently ties difficulty to trainer AI, wild smart AI, raid move choice, and anti-cheese behavior.
- CFRU Expert scaling-linked evolution is distinct from UPR-FVX Trainer Evolution. The implementation must avoid double-applying evolution changes.
- Existing scripts or saves may expect `VAR_GAME_DIFFICULTY` to hold the old combined value. Migration needs an explicit compatibility plan.
- The current option menu has one second-page item count for difficulty. Splitting into three CFRU controls may require UI capacity/layout work in CFRU and separate Swing layout work in UPR-FVX.
