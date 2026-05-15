# Diagnose 144: Trainer Held Items Filters Scope Plan

## Scope

- Branch: `analysis/upr-fvx-cfru-dpe-trainer-held-items-filters-scope-plan`
- Goal: plan Trainer Held Item filter coverage after Boss, Important and Regular Trainer Held Items passed in no-filter smokes.
- Mode: read-only planning only.
- No ROM access, no Randomizer run, no build and no code changes.
- Explicitly out of scope: Wild/Encounter Held Items, Starter Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer scopes.

## Baseline

- Diagnose 138 confirmed Trainer Held Items are readable via `TrainerPokemon.heldItem`.
- Diagnose 141 confirmed Boss Trainer Held Items reload stability in the no-filter scope.
- Diagnose 142 confirmed Important Trainer Held Items reload stability in the no-filter scope.
- Diagnose 143 confirmed Regular Trainer Held Items reload stability in the no-filter scope.
- Boss, Important and Regular no-filter scopes remain GUI-compatible in the tested CFRU/DPE Gen9-BPRE scope.

## Filter scope assessment

Trainer Held Item filters are a separate Trainer-Held-Items sub-scope. The no-filter Trainer class smokes already prove the base writer path for Boss, Important and Regular classes, but they do not prove the item-pool narrowing or highest-level placement logic.

The filter sub-scope should not promote Wild Held Items, Starter Held Items, Field Items, Pickup or Shops. It should also not promote Trainer Ban Bad behavior because no separate Trainer Held Item Ban Bad flag was found in the searched Settings/GUI/Randomizer paths.

## Relevant code paths

- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`
  - `maybeRandomizeTrainerHeldItems()` calls `trainerPokeRandomizer.randomizeTrainerHeldItems()` when any Boss/Important/Regular Trainer Held Item class flag is enabled.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java`
  - `randomizeTrainerHeldItems()` gates target trainers by Boss/Important/Regular flags and skips `shouldNotGetBuffs()` trainers.
  - `highestLevelOnly` selects one highest-level `TrainerPokemon` per targeted trainer instead of all team members.
  - `randomizeHeldItem(...)` selects the item pool.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/Settings.java`
  - Trainer class flags: `randomizeHeldItemsForBossTrainerPokemon`, `randomizeHeldItemsForImportantTrainerPokemon`, `randomizeHeldItemsForRegularTrainerPokemon`.
  - Filter flags: `consumableItemsOnlyForTrainerPokemon`, `sensibleItemsOnlyForTrainerPokemon`, `highestLevelOnlyGetsItemsForTrainerPokemon`.
  - Settings byte stores and restores all three filter flags.
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/gui/RandomizerGUI.java`
  - GUI reads/writes the Trainer Held Item class and filter checkboxes.
  - GUI save path should be watched because the Boss Trainer Held Item setting assignment appears to depend on the Regular Trainer item checkbox in the observed source path.
- `02_external/upr-fvx/random/src/main/resources/com/uprfvx/random/gui/Bundle.properties`
  - Defines GUI text/tooltips for Boss, Important, Regular, Consumable Only, Sensible Items and Highest Level Only.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/TrainerPokemon.java`
  - Target field: `heldItem`.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Trainer.java`
  - Preserve and policy inputs: `shouldNotGetBuffs()`, `isBoss()`, `isImportant()`, `isRequiresUniqueHeldItems()`, `pokemonHaveUniqueHeldItems()`.

## Settings and GUI findings

- `Consumable Only` is an independent Trainer Held Item filter flag.
- `Sensible Items` is an independent Trainer Held Item filter flag.
- `Highest Level Only` is an independent Trainer Held Item placement flag.
- `Sensible Items` takes precedence over the plain consumable pool path; when both Sensible and Consumable are enabled, the randomizer calls the sensible pool path with `consumableItemsOnly=true`.
- Without Sensible, Consumable uses `romHandler.getAllConsumableHeldItems()`.
- Without Sensible and without Consumable, the no-filter path uses `romHandler.getAllHeldItems()`.
- Highest-Level does not narrow the item pool by itself; it narrows placement to one highest-level Pokemon per targeted trainer.
- The filters apply inside the shared Trainer Held Item randomizer path and therefore can affect Boss, Important and Regular target classes whenever their class flags are enabled.
- No separate Trainer Held Item Ban Bad flag was found. Ban Bad exists for Starter and Wild Held Items in the searched paths, but not as a Trainer Held Item filter.

## Risks and blockers

- GUI flag wiring risk: the observed GUI write path for Boss Trainer Held Items appears to read the Regular Trainer item checkbox. A later filter smoke should prefer a direct Settings-equivalent harness unless GUI-specific behavior is explicitly being tested.
- Sensible Items needs move context and can load moves/movesets for reset-move TrainerPokemon, so later metrics must include save/reload stability and exception capture.
- Highest-Level Only changes expected write count semantics: unchanged lower-level team members are expected, not a preserve failure.
- Unique held-item trainers can trigger rerolls until uniqueness is satisfied; later smoke metrics should track invalid/unloaded/fallback/placeholder writes and reload mismatches.
- `shouldNotGetBuffs()` trainers must remain preserve-only regardless of filter choice.
- No Trainer Ban Bad flag was found; any Ban-Bad follow-up needs a separate code/GUI confirmation before a smoke is planned.
- Starter Held Items remain blocked from promotion until their own smoke runs.

## Recommended test order

1. Regular Trainers only + Sensible Items + Consumable Only + Highest Level Only as the narrow combined filter smoke.
2. If the combined smoke fails, split into Regular + Consumable Only, then Regular + Sensible Items, then Regular + Highest Level Only.
3. If the combined smoke passes but product confidence requires isolated semantics, add separate Regular-only smokes for each filter.
4. Do not run Trainer Ban Bad unless a separate Trainer Held Item Ban Bad setting/path is later identified.
5. After filter coverage decision, move to Starter Held Items.

## Future smoke metrics

- `candidateFilesChecked`
- `candidateLoaded`
- `smokeExecuted`
- `saveSuccessful`
- `logSuccessful`
- `outputRomExists`
- `logNonEmpty`
- `reloadSuccessful`
- `trainerHeldItemsTotalBefore/After/Reload`
- `trainerHeldItemsNonZeroBefore/After/Reload`
- `trainerHeldItemsBadBefore/After/Reload`
- `trainerHeldItemsTMBefore/After/Reload`
- `bossTrainerHeldItemsTotalBefore/After/Reload`
- `importantTrainerHeldItemsTotalBefore/After/Reload`
- `regularTrainerHeldItemsTotalBefore/After/Reload`
- `regularTrainerHeldItemReloadMismatches`
- `bossTrainerHeldItemMismatchesAfter/Reload`
- `importantTrainerHeldItemMismatchesAfter/Reload`
- `shouldNotGetBuffsTrainerHeldItemMismatchesAfter/Reload`
- `highestLevelEligibleTrainerCount`
- `highestLevelWrittenPokemonCount`
- `nonHighestLevelWriteCount`
- `consumableOnlyWrites`
- `sensibleItemWrites`
- `nonConsumableWrites`
- `nonSensibleWrites`
- `invalidTrainerHeldItemWrites`
- `unloadedTrainerHeldItemWrites`
- `fallbackTrainerHeldItemWrites`
- `placeholderTrainerHeldItemWrites`
- `heldItemPoolAllowedSize`
- `heldItemPoolNonBadSize`
- `consumableHeldItemPoolSize`
- `sensibleHeldItemPoolObserved`
- `canTMsBeHeld`
- `wildHeldItemScopeChanged=false`
- `starterHeldItemScopeChanged=false`
- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `shopScopeChanged=false`
- `exceptionClass`
- `stacktrace`

## Evaluation

Trainer Held Item filters are ready for a separate narrow smoke plan, but remain unpromoted until at least one filter smoke proves save/log/output/reload stability, pool correctness and class preserve behavior. Boss, Important and Regular no-filter Trainer Held Item scopes remain documented as GUI-compatible in their tested scopes. Starter Held Items remain the next major Held Items scope after the filter decision.

## Next minimal step

Run a Regular Trainers only filter smoke with `Consumable Only`, `Sensible Items` and `Highest Level Only` enabled, unless the next block decides to split the filters before execution.
