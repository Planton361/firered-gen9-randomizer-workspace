# Diagnose 148: Wild Encounters Scope Diagnostics Plan

## Scope

- Branch: `analysis/upr-fvx-cfru-dpe-wild-encounters-scope-diagnostics-plan`
- Goal: plan Wild Encounters / Wild Pokemon Randomization as a new CFRU/DPE Gen9-BPRE Randomizer scope after the tested Held Items scope was closed.
- Mode: read-only planning only.
- No ROM access, no Randomizer run, no build and no code changes.
- Explicitly out of scope: Wild Held Items, Trainer Pokemon, Starters, Static/Gift Pokemon, Field Items, Pickup, Shops and all non-Wild-Encounter randomizer scopes.

## Baseline

- Diagnose 138 established Held Items candidate diagnostics.
- Diagnose 147 closed the tested Held Items scope for CFRU/DPE Gen9-BPRE.
- Wild Encounters must start as a new feature/package scope and must not reuse Wild Held Item evidence.

## Wild Encounters scope assessment

Wild Encounters / Wild Pokemon Randomization is a distinct writer scope because it writes `EncounterArea` / `Encounter` species and level data through `getEncounters(...)` and `setEncounters(...)`. It is separate from Wild Held Items, which write Species/BaseStats held-item fields, and separate from Trainer, Starter, Static/Gift and Item scopes.

No feature promotion happens in this planning block. A read-only candidate diagnostic must run first to confirm encounter table readability, encounter type counts, slot counts, SpeciesSet identity mapping, level ranges and scope isolation before any write/reload smoke.

## Relevant code paths

- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`
  - Wild Pokemon randomization is dispatched through the Wild Encounter randomizer path before held-item-specific scopes.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/WildEncounterRandomizer.java`
  - `randomizeEncounters(...)` reads encounter areas, prepares areas, applies level modifiers, selects allowed/banned Species pools, randomizes zones and calls `romHandler.setEncounters(...)`.
  - Zone modes include game-wide, named location, map, encounter set and no-zone randomization.
  - Option families include type themes, keep primary type, basic-only / same-evolution-stage, keep evolution families, catch-em-all, similar strength, low-level balancing, legendary bans and alt-form handling.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
  - `getEncounters(boolean useTimeOfDay)` reads the Gen3 wild encounter pointer list and builds `EncounterArea` objects.
  - `setEncounters(boolean useTimeOfDay, List<EncounterArea>)` writes existing fixed encounter areas back through their original table pointers.
  - `readEncounterArea(...)` reads rate, levels and raw species IDs into `Encounter` slots.
  - `writeEncounterArea(...)` writes level bytes and internal species IDs back to fixed slots.
  - `getWildEncounterInternalSpeciesId(...)` uses internal SpeciesSet identity for extended BPRE hacks.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/EncounterArea.java`
  - Holds rate, display name, map index, location tag, encounter type, banned species and slot list.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Encounter.java`
  - Holds level, max level, species and forme number for one encounter slot.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/EncounterType.java`
  - Defines `WALKING`, `SURFING`, `FISHING`, `INTERACT`, `AMBUSH`, `SPECIAL` and `UNUSED`; Gen3 FRLG path observed uses Walking, Surfing, Fishing and Rock Smash as `INTERACT`.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/Settings.java`
  - Wild Pokemon settings include `randomizeWildPokemon`, `WildPokemonZoneMod`, split-by-encounter-type, type theme mods, evolution mods, similar strength, catch-em-all, time-based encounters, level modifier and held-item-specific flags.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/gui/RandomizerGUI.java`
  - GUI maps Wild Pokemon checkboxes/radio buttons to `Settings` for zone, type, evolution, catch-em-all, similar-strength, time-based and minimum-catch-rate options.
- `02_external/upr-fvx/random/src/main/resources/com/uprfvx/random/gui/Bundle.properties`
  - Provides Wild Pokemon GUI labels/tooltips and should be used to confirm user-facing option names in later plans.

## Settings and GUI findings

- Main enable flag: `randomizeWildPokemon`.
- Zone modes: `NONE`, `ENCOUNTER_SET`, `MAP`, `NAMED_LOCATION`, `GAME`.
- Optional split: `splitWildZoneByEncounterTypes`.
- Type options: none, random type themes, keep primary type, plus keep type themes.
- Evolution options: none, basic only, keep stage, plus keep evolution families.
- Other Wild Encounter options: similar strength, catch-em-all, use time-based encounters, minimum catch rate, wild level modifier, legendary block, alt-form handling and balance shaking grass.
- Wild Held Items settings are separate (`randomizeWildPokemonHeldItems`, `banBadRandomWildPokemonHeldItems`) and remain out of this scope.

## Expected data structure

- Gen3 wild encounter pointer list keyed by map bank/map entries and terminated by `0xFF/0xFF` bank/map marker.
- Per map entry may point to separate encounter tables for:
  - Walking / Grass / Cave.
  - Surfing / Water.
  - Rock Smash as `INTERACT`, if present.
  - Fishing, covering rod tables through the Gen3 fishing slot table.
- `EncounterArea` stores encounter rate, display name, map index, location tag, encounter type and fixed slot list.
- `Encounter` stores min level, max level, Species and forme number.
- Gen3 write path preserves table shape and writes fixed slot counts using Gen3 constants for walking, surfing, rock smash and fishing.
- CFRU/DPE extended BPRE species writes use SpeciesSet identity number, not vanilla Pokedex-to-internal mapping.

## Risks and blockers

- SpeciesSet / Gen9 mapping risk: write path must use internal SpeciesSet identity for extended BPRE hacks and avoid invalid or unloaded species.
- Null/unresolved species risk: `readEncounterArea(...)` can encounter unknown raw species and logs diagnostics; future diagnostics must count null/unloaded/fallback/placeholder species without documenting raw IDs.
- Encounter table length risk: Gen3 slot counts are fixed; future writes must preserve area and slot counts.
- Slot/level risk: min/max level bytes and level modifier options can create mismatches if compared incorrectly.
- Encounter type risk: Walking, Surfing, Fishing and Rock Smash/Interact must not be conflated.
- Map/area risk: zone modes can group by encounter set, map, named location, game and optionally split by encounter type.
- Rate risk: encounter rates should stay stable unless a later option explicitly changes them.
- Scope leakage risk: Wild Held Items, Trainer, Starter, Static/Gift and Item scopes must remain unchanged.
- Special-table risk: Ambush/Special/Unused types exist in shared model but may not appear in Gen3 FRLG candidate; diagnostics must count observed types instead of assuming absence.

## Preserve and skip policy

- Preserve encounter area count, slot count, encounter rates, encounter types, map/location tags and level ranges during read-only diagnostics.
- For write smokes, preserve all non-target scopes: held items, trainer data, starter data, static/gift data and item scopes.
- Do not assume Rock Smash or special tables exist; detect and report observed counts.
- Do not document private map names, raw species IDs, offsets, pointer values or raw bytes.
- Treat unresolved/null species as diagnostic blockers for write smokes until classified.

## Recommended diagnostic and smoke order

1. Wild Encounters read-only candidate diagnostic.
2. Narrow Wild Encounters Random smoke with baseline options only, if the candidate diagnostic confirms stable table structure.
3. Zone-mode smoke for the smallest relevant mode, likely Encounter Set or Game, depending on code/GUI baseline selected.
4. Area/type-specific smokes only if split-by-encounter-type is selected for coverage.
5. Similar-strength, catch-em-all, type-themed, evolution-stage and level-modifier options as separate follow-up scopes.
6. Do not retest Held Items in this scope; only assert `heldItemScopeChanged=false` in later write diagnostics.

## Future diagnostic and smoke metrics

- `candidateFilesChecked`
- `candidateLoaded`
- `encounterScanSuccessful`
- `encounterSetCount`
- `encounterAreaCount`
- `encounterSlotCount`
- `landEncounterSlotCount`
- `waterEncounterSlotCount`
- `fishingEncounterSlotCount`
- `rockSmashEncounterSlotCount`
- `ambushEncounterSlotCount`
- `specialEncounterSlotCount`
- `unusedEncounterSlotCount`
- `encounterRateCount`
- `minEncounterLevel`
- `maxEncounterLevel`
- `invalidEncounterSpecies`
- `unloadedEncounterSpecies`
- `fallbackEncounterSpecies`
- `placeholderEncounterSpecies`
- `nullEncounterSpecies`
- `speciesSetIdentityModelObserved`
- `encounterLevelMismatches`
- `encounterRateMismatches`
- `encounterTypeMismatches`
- `encounterSlotCountMismatches`
- `encounterReloadMismatches`
- `heldItemScopeChanged=false`
- `trainerScopeChanged=false`
- `starterScopeChanged=false`
- `staticGiftScopeChanged=false`
- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `shopScopeChanged=false`
- `exceptionClass`
- `stacktrace`

## Evaluation

Wild Encounters are ready to enter a new separate diagnostics scope, but no Wild Encounter feature is promoted in this plan. The next block must be a read-only candidate diagnostic that confirms encounter data can be scanned safely and that CFRU/DPE Gen9-BPRE species mapping is stable enough for later write/reload smokes.

## Next minimal step

Run a Wild Encounters read-only candidate diagnostic.
