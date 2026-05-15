# Diagnose 145: Regular Trainer Held Items Filtered Reload Smoke

## Scope

- Branch: `test/upr-fvx-cfru-dpe-trainer-held-items-regular-filtered-reload-smoke`
- Target: CFRU/DPE Gen9-BPRE candidate source, sanitized local-only harness.
- Feature scope: Trainer Held Items, Regular Trainers only, combined filters.
- Settings scope:
  - `randomizeHeldItemsForBossTrainerPokemon=false`
  - `randomizeHeldItemsForImportantTrainerPokemon=false`
  - `randomizeHeldItemsForRegularTrainerPokemon=true`
  - `consumableItemsOnlyForTrainers=true`
  - `sensibleItemsOnlyForTrainers=true`
  - `highestLevelGetsItemsForTrainers=true`
- Explicitly out of scope: Boss Trainer Held Items, Important Trainer Held Items, Wild/Encounter Held Items, Starter Held Items, Field Items, Pickup, Shops, Trainer Ban Bad and all non-Held-Item randomizer scopes.

## Baseline

- Diagnose 143 established Regular Trainer Held Items as reload-stable without filters.
- Diagnose 144 identified `Consumable Only`, `Sensible Items` and `Highest Level Only` as separate Trainer Held Item filter settings in the shared Trainer Held Item path.
- Highest-Level Only changes expected write-count semantics: one highest-level Pokemon per eligible targeted trainer is expected, not every Regular TrainerPokemon slot.
- Sensible Items uses move context; with Consumable Only enabled it constrains the sensible held-item pool to consumable items.

## Smoke result

PASS.

The Regular Trainer Held Items combined-filter Write/Reload-Smoke completed successfully. Save, log, output ROM creation and reload all succeeded. Regular Trainer `TrainerPokemon.heldItem` values were reload-stable, Boss and Important Trainer Held Items stayed unchanged, `shouldNotGetBuffs` Trainer Held Items stayed unchanged, and no cross-scope changes were observed.

## Trainer Held Items findings

- `TrainerPokemon.heldItem` was used as the compared target structure.
- Total Trainer Pokemon held-item slots stayed stable across before/after/reload.
- Regular Trainer slot count stayed stable.
- Highest-Level Only targeted one Pokemon per eligible Regular Trainer.
- Existing bad-item count after filtering is not treated as a Ban Bad failure because no Trainer Held Item Ban Bad option was enabled or confirmed.
- TMs were not written as Trainer Held Items in this run.

## Filter findings

- `highestLevelEligibleTrainerCount=697`.
- `highestLevelEligiblePokemonCount=697`.
- `highestLevelHeldItemWrites=697`.
- `consumableHeldItemWrites=697`.
- `nonConsumableHeldItemWrites=0`.
- `sensibleHeldItemWrites=697`.
- `nonSensibleHeldItemWrites=0`.
- The combined filter path behaved as expected for Regular Trainers only: one highest-level write per eligible Regular Trainer, all writes in the consumable sensible pool.

## Preserve and trainer-class findings

- Boss Trainer Held Items stayed preserve-only stable.
- Important Trainer Held Items stayed preserve-only stable.
- `shouldNotGetBuffs` Trainer Held Items stayed preserve-only stable.
- Boss, Important and Regular class slot counts remained stable.

## Reload findings

- Reload succeeded.
- Regular Trainer Held Item reload mismatches: `0`.
- Boss Trainer preserve mismatches after/reload: `0` / `0`.
- Important Trainer preserve mismatches after/reload: `0` / `0`.
- `shouldNotGetBuffs` preserve mismatches after/reload: `0` / `0`.

## Scope isolation findings

- Wild/Encounter Held Items changed: `false`.
- Starter Held Items changed: `false`.
- Field Items changed: `false`.
- Pickup changed: `false`.
- Shops changed: `false`.

## Metrics

| Metric | Value |
| --- | --- |
| `candidateFilesChecked` | `3` |
| `candidateLoaded` | `true` |
| `smokeExecuted` | `true` |
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| `reloadSuccessful` | `true` |
| `trainerHeldItemsTotalBefore` | `1754` |
| `trainerHeldItemsTotalAfter` | `1754` |
| `trainerHeldItemsTotalReload` | `1754` |
| `trainerHeldItemsNonZeroBefore` | `87` |
| `trainerHeldItemsNonZeroAfter` | `750` |
| `trainerHeldItemsNonZeroReload` | `750` |
| `trainerHeldItemsBadBefore` | `0` |
| `trainerHeldItemsBadAfter` | `259` |
| `trainerHeldItemsBadReload` | `259` |
| `trainerHeldItemsTMBefore` | `0` |
| `trainerHeldItemsTMAfter` | `0` |
| `trainerHeldItemsTMReload` | `0` |
| `bossTrainerHeldItemsTotalBefore` | `74` |
| `bossTrainerHeldItemsTotalAfter` | `74` |
| `bossTrainerHeldItemsTotalReload` | `74` |
| `importantTrainerHeldItemsTotalBefore` | `117` |
| `importantTrainerHeldItemsTotalAfter` | `117` |
| `importantTrainerHeldItemsTotalReload` | `117` |
| `regularTrainerHeldItemsTotalBefore` | `1563` |
| `regularTrainerHeldItemsTotalAfter` | `1563` |
| `regularTrainerHeldItemsTotalReload` | `1563` |
| `regularTrainerHeldItemReloadMismatches` | `0` |
| `bossTrainerHeldItemMismatchesAfter` | `0` |
| `bossTrainerHeldItemMismatchesReload` | `0` |
| `importantTrainerHeldItemMismatchesAfter` | `0` |
| `importantTrainerHeldItemMismatchesReload` | `0` |
| `shouldNotGetBuffsTrainerHeldItemMismatchesAfter` | `0` |
| `shouldNotGetBuffsTrainerHeldItemMismatchesReload` | `0` |
| `highestLevelEligibleTrainerCount` | `697` |
| `highestLevelEligiblePokemonCount` | `697` |
| `highestLevelHeldItemWrites` | `697` |
| `consumableHeldItemWrites` | `697` |
| `nonConsumableHeldItemWrites` | `0` |
| `sensibleHeldItemWrites` | `697` |
| `nonSensibleHeldItemWrites` | `0` |
| `invalidTrainerHeldItemWrites` | `0` |
| `unloadedTrainerHeldItemWrites` | `0` |
| `fallbackTrainerHeldItemWrites` | `0` |
| `placeholderTrainerHeldItemWrites` | `0` |
| `heldItemPoolAllowedSize` | `212` |
| `heldItemPoolNonBadSize` | `161` |
| `canTMsBeHeld` | `true` |
| `wildHeldItemScopeChanged` | `false` |
| `starterHeldItemScopeChanged` | `false` |
| `fieldItemScopeChanged` | `false` |
| `pickupScopeChanged` | `false` |
| `shopScopeChanged` | `false` |
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

## Risks and blockers

- No active blocker for Regular Trainer Held Items with the combined Consumable/Sensible/Highest-Level filter scope.
- Boss and Important Trainer filter combinations remain unpromoted.
- Trainer Ban Bad remains untested and unplanned unless a separate Trainer Held Item Ban Bad path is later confirmed.
- Starter Held Items remain a separate unpromoted scope.

## Evaluation

Regular Trainer Held Items with combined `Consumable Only`, `Sensible Items` and `Highest Level Only` filters are GUI-compatible in the tested CFRU/DPE Gen9-BPRE scope. This smoke does not promote Boss/Important filter combinations, Wild Held Items, Starter Held Items, Field Items, Pickup, Shops or any other randomizer scope.

## Next minimal step

Move to Starter Held Items smoke unless Boss/Important Trainer Held Item filter combinations are explicitly required.
