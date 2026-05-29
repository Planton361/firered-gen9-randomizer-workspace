# Pokemon ability behavior risk audit

Date: 2026-05-29
Branch: `analysis/pokemon-ability-behavior-risk-audit`
Scope: read-only CFRU/DPE Ability behavior audit for Gen9/newer Ability names.

## Purpose

This audit checks whether local Gen9-looking Ability names are backed by CFRU battle behavior or are only aliases to older Ability IDs/effects. It does not change CFRU, DPE, Pokemon data tables, Showdown data, submodule pins, ROMs, builds, raw reports, hashes or private paths.

## Source set

Reviewed local source paths:

- CFRU `include/constants/abilities.h`
- DPE `include/abilities.h`
- CFRU `strings/ability_name_table.string`
- CFRU `strings/ability_descriptions.string`
- CFRU `assembly/data/ability_tables.json`
- CFRU `src/ability_battle_effects.c`
- CFRU `src/ability_util.c`
- CFRU `include/new/ability_tables.h`
- DPE `src/Base_Stats.c`
- Additional behavior-hook files found by `rg`: CFRU `src/damage_calc.c`, `src/battle_start_turn_start.c`, `src/battle_script_util.c`, `src/cmd49.c`, `src/stat_buffs.c`, `src/accuracy_calc.c`, `src/Battle_AI/ai_util.c`, `src/Battle_AI/ai_partner.c`, `src/Battle_AI/ai_negatives.c`, `src/Battle_AI/ai_switching.c`, `src/build_pokemon.c`, and battle-script assembly call sites.

## Classification legend

- `implemented-alias-hooked`: local Ability ID is an older alias, but CFRU has source-backed species-gated behavior hooks for the Gen9 behavior core.
- `partial-alias-hooked`: CFRU has source-backed hooks, but the implementation is visibly partial, species/side scoped, or piggybacks on an old effect in a risky way.
- `alias-only-risk`: the local name aliases to an older effect and no battle hook beyond display/species helper was found in the reviewed sources.
- `display-or-definition-risk`: name/description/species helper exists, but the assignment or trigger path is inconsistent or uncertain.
- `missing-local`: no local Ability constant/name/behavior path was found in the reviewed CFRU/DPE sources.

## High-risk focus matrix

| Ability family | Local definition / DPE assignment | CFRU behavior evidence | Category | Risk |
| --- | --- | --- | --- | --- |
| `HADRONENGINE` | CFRU/DPE define it as `ABILITY_ELECTRICSURGE`; Miraidon uses `ABILITY_HADRONENGINE` in DPE `Base_Stats.c`. | Electric Surge terrain activation comes from the alias; CFRU `damage_calc.c` has a `SpeciesHasHadronEngine` Sp. Atk boost under Electric Terrain. | `implemented-alias-hooked` | Medium: core terrain plus boost is source-backed, but still depends on old ID plumbing and species helper. |
| `ORICHALCUMPULSE` | CFRU/DPE define it as `ABILITY_DROUGHT`; Koraidon uses `ABILITY_ORICHALCUMPULSE`. | Drought sun activation comes from the alias; CFRU `damage_calc.c` has `SpeciesHasOrichalcumPulse` Attack boost in sun. | `implemented-alias-hooked` | Medium: core behavior is covered through alias plus hook. |
| Ruin abilities | CFRU/DPE alias `BEADSOFRUIN`, `SWORDOFRUIN`, `TABLETOFRUIN`, `VESSELOFRUIN` to `ABILITY_STALL`; DPE assigns `ABILITY_STALL` to Wo-Chien, Chien-Pao, Ting-Lu and Chi-Yu. | CFRU `ability_util.c` supplies species-gated names/descriptions, `battle_start_turn_start.c` excludes Ruin species from Stall speed penalty, and `damage_calc.c` applies 25% stat reductions by species helper. | `partial-alias-hooked` | Medium-high: behavior exists, but the damage hook uses side/stall detection and should be battle-smoked before treating as faithful Gen9 behavior. |
| `GOODASGOLD` | CFRU/DPE define it as `ABILITY_CLEARBODY`; Gholdengo uses `ABILITY_GOODASGOLD`. | CFRU display override is under `ABILITY_CLEARBODY`; `ability_battle_effects.c` has `ABILITY_GOODASGOLD` status/status-move blocks gated by `SpeciesHasGoodAsGold`. | `partial-alias-hooked` | Medium-high: behavior is source-backed, but mixed `CLEARBODY`/`GOODASGOLD` plumbing deserves a targeted smoke. |
| `TOXICDEBRIS` | CFRU/DPE define it as `ABILITY_POISONPOINT`; Glimmet/Glimmora use `ABILITY_TOXICDEBRIS`. | CFRU `ability_battle_effects.c` branches under `ABILITY_POISONPOINT` to set Toxic Spikes on physical hits when `SpeciesHasToxicDebris`. | `implemented-alias-hooked` | Medium: core hook is clear; still uses old Poison Point ID when species helper is false. |
| `ZEROTOHERO` | CFRU/DPE define it as `ABILITY_TORRENT`; Palafin forms use `ABILITY_ZEROTOHERO`. | CFRU `ability_battle_effects.c` shows a switch-in message under `ABILITY_TORRENT`; no source-backed Palafin-to-Hero form-change path was found in the reviewed snippets. | `partial-alias-hooked` | High: display/message evidence exists, but true switch-out transformation is not confirmed by this audit. |
| `POISONPUPPETEER` | CFRU/DPE define it as `ABILITY_PLUS`; Pecharunt uses `ABILITY_POISONPUPPETEER`. | CFRU `battle_script_util.c` has `TrySetPoisonPuppeterEffect`, battle scripts call it, and `ability_util.c` excludes Poison Puppeteer from Plus/Minus pairing. | `implemented-alias-hooked` | Medium: source-backed confusion-on-poison hook exists; spelling is `Puppeter` in local symbols/strings. |
| `TERA SHIFT` / `TERA SHELL` | No `ABILITY_TERASHIFT` or `ABILITY_TERASHELL` constants found. DPE gives base Terapagos `ABILITY_ICEFACE`, Terastal/Stellar forms `ABILITY_COLORCHANGE`. | CFRU has names/descriptions and helpers, Ice Face switch-in form change to `SPECIES_TERAPAGOS_TERASTAL`, and Tera Shell damage reduction hook. Helpers refer to `SPECIES_TERAPAGOS_TERA`, while constants use `SPECIES_TERAPAGOS_TERASTAL`. | `display-or-definition-risk` | High: source has partial hooks, but naming/assignment mismatch means runtime display/behavior needs source fix or proof before data generation relies on it. |
| `COMMANDER` | No `ABILITY_COMMANDER` constant/name/behavior found. | No reviewed CFRU/DPE behavior path found. | `missing-local` | High: do not map as supported. |
| `HOSPITALITY` | No `ABILITY_HOSPITALITY` constant/name/behavior found. | No reviewed CFRU/DPE behavior path found. | `missing-local` | High: do not map as supported. |
| `EMBODYASPECT*` | No `ABILITY_EMBODYASPECT*` constants found. Ogerpon Terastal forms in DPE use older abilities (`DEFIANT`, `WATERABSORB`, `MOLDBREAKER`, `STURDY`). | No reviewed CFRU Embody Aspect behavior found. | `missing-local` | High: Ogerpon Terastal species exist, but Embody Aspect behavior is not locally represented. |

## Broader Gen9 alias review

| Ability | Local alias target | Behavior evidence found | Category |
| --- | --- | --- | --- |
| `ANGERSHELL` | `WEAKARMOR` | HP crossing half triggers `BattleScript_AngerShellActivates` under Weak Armor. | `implemented-alias-hooked` |
| `ARMORTAIL` | `DAZZLING` | Priority-block behavior is inherited from Dazzling; display helper exists. | `implemented-alias-hooked` |
| `COSTAR` | `CURIOUSMEDICINE` | Switch-in partner stat-copy branch exists under Curious Medicine. | `implemented-alias-hooked` |
| `CUDCHEW` | `HARVEST` | Cud Chew counter branches exist under Harvest end-turn handling. | `partial-alias-hooked` |
| `EARTHEATER` | `VOLTABSORB` | Absorbing logic swaps Electric/Ground behavior when `SpeciesHasEarthEater`; AI helpers reference the helper. | `implemented-alias-hooked` |
| `ELECTROMORPHOSIS` | `COLORCHANGE` | Hit reaction branches away from Color Change into Electromorphosis charge-style scripts. | `implemented-alias-hooked` |
| `GUARDDOG` | `INNERFOCUS` | Intimidate/stat-lowering exceptions and Attack-lowering prevention hooks exist. | `partial-alias-hooked` |
| `MINDSEYE` | `SCRAPPY` | Scrappy inherited; accuracy-lowering prevention hooks exist in accuracy/stat logic. | `partial-alias-hooked` |
| `MYCELIUMMIGHT` | `MOLDBREAKER` in CFRU/DPE alias block, with some display paths also checking `ABILITY_MINUS` | Status moves are forced late in `battle_start_turn_start.c`; `IsTargetAbilityIgnored` uses Mycelium-specific ignored ability flags. | `partial-alias-hooked` |
| `OPPORTUNIST` | `DANCER` | `cmd49.c` branches Dancer behavior to buff-move copying when `SpeciesHasOportunist`. | `implemented-alias-hooked` |
| `PROTOSYNTHESIS` | `QUARKDRIVE` | Sunny-weather highest-stat boost logic exists in `damage_calc.c`; activation scripts are present. | `partial-alias-hooked` |
| `PURIFYINGSALT` | `IMMUNITY` | Status immunity and Ghost damage-reduction hooks exist. | `implemented-alias-hooked` |
| `ROCKYPAYLOAD` | `STEELWORKER` | Rock-type power boost branch exists under Steelworker. | `implemented-alias-hooked` |
| `SEEDSOWER` | `GRASSYSURGE` | Entry Grassy Surge is suppressed for Seed Sower; hit reaction sets terrain. | `implemented-alias-hooked` |
| `SHARPNESS` | `STRONGJAW` | Slicing-move power boost branch exists under Strong Jaw. | `implemented-alias-hooked` |
| `SUPREMEOVERLORD` | `HUGEPOWER` | Switch-in message and damage boost based on fainted player-party mons exist. | `partial-alias-hooked` |
| `SUPERSWEETSYRUP` | `INTIMIDATE` | Species/name/description helper found; no safe source-backed Evasion-drop behavior was confirmed in reviewed snippets. | `alias-only-risk` |
| `THERMALEXCHANGE` | `STEAMENGINE` | Burn immunity and Fire-hit Attack boost branches exist. | `implemented-alias-hooked` |
| `TOXICCHAIN` | `POISONTOUCH` | Toxic Chain helpers are referenced by battle scripts, AI and move-effect logic. | `implemented-alias-hooked` |
| `WELLBAKEDBODY` | `STEAMENGINE` | Fire-hit Defense boost branch exists; inherited Steam Engine speed branch is skipped when species helper matches. | `implemented-alias-hooked` |
| `WINDPOWER` | `BERSERK` | Wind-move charge-style branch exists under Berserk. | `implemented-alias-hooked` |
| `WINDRIDER` | `ANGERPOINT` | Wind move block and Attack boost branches exist; AI helpers reference Wind Rider. | `implemented-alias-hooked` |

## Source-backed caveats

- The reviewed Gen9 Ability names mostly do not allocate new unique Ability IDs. CFRU/DPE rely on aliases to older IDs plus species-gated display and behavior hooks.
- `ability_name_table.string` and `ability_descriptions.string` include many Gen9 labels/descriptions, but display text is not behavior proof.
- `assembly/data/ability_tables.json` and `include/new/ability_tables.h` did not show dedicated Gen9 alias entries for the focused names in the reviewed `rg` search; behavior is mostly in C hooks and battle scripts.
- DPE `Base_Stats.c` can assign Gen9-looking macros that compile to older IDs. Data generation must not treat local macro names as proof of native behavior.
- Terapagos is the largest concrete inconsistency found: source references `SPECIES_TERAPAGOS_TERA` in helpers while local constants/DPE use `SPECIES_TERAPAGOS_TERASTAL`; DPE form abilities also do not line up with the displayed Tera Shell override target.

## Recommended follow-up order

1. Add these categories to the alias/behavior policy as source-backed behavior risk labels, without changing CFRU/DPE data tables.
2. Smoke-test only the `implemented-alias-hooked` focus abilities before promoting them to generator-safe behavior.
3. Treat `partial-alias-hooked` entries as supported only after targeted battle smokes or source fixes.
4. Block `missing-local`, `alias-only-risk`, and Terapagos `display-or-definition-risk` from automated Gen9 data generation until source-backed behavior is added or an explicit non-support policy exists.

## Handoff

Next useful task: extend the reviewed machine-readable alias table with an Ability behavior-risk section that distinguishes `implemented-alias-hooked`, `partial-alias-hooked`, `alias-only-risk`, `display-or-definition-risk`, and `missing-local`. Keep it policy-only unless a separate implementation task explicitly changes CFRU/DPE behavior.
