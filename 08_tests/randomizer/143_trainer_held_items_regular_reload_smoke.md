# Diagnose 143: Regular Trainer Held Items Reload Smoke

## Scope

- Branch: `test/upr-fvx-cfru-dpe-trainer-held-items-regular-reload-smoke`
- Target: CFRU/DPE Gen9-BPRE candidate source, sanitized local-only harness.
- Feature scope: Trainer Held Items, Regular Trainers only.
- Settings scope:
  - `randomizeHeldItemsForBossTrainerPokemon=false`
  - `randomizeHeldItemsForImportantTrainerPokemon=false`
  - `randomizeHeldItemsForRegularTrainerPokemon=true`
  - Consumable-only filter disabled.
  - Sensible-only filter disabled.
  - Highest-level-only filter disabled.
- Explicitly out of scope: Boss Trainer Held Items, Important Trainer Held Items, Wild/Encounter Held Items, Starter Held Items, Field Items, Pickup, Shops, and all non-Held-Item randomizer scopes.

## Baseline

- Diagnose 138 established Trainer Held Items as readable through `TrainerPokemon.heldItem`.
- Diagnose 141 established Boss Trainer Held Items as reload-stable in the no-filter scope.
- Diagnose 142 established Important Trainer Held Items as reload-stable in the no-filter scope.
- Regular Trainer Held Items remained preserve-only stable in Diagnoses 141 and 142.

## Smoke result

PASS.

The Regular Trainer Held Items-only Write/Reload-Smoke completed successfully. Save, log, output ROM creation and reload all succeeded. Regular Trainer `TrainerPokemon.heldItem` values were reload-stable, Boss and Important Trainer Held Items stayed unchanged, `shouldNotGetBuffs` Trainer Held Items stayed unchanged, and no cross-scope changes were observed.

## Trainer Held Items findings

- `TrainerPokemon.heldItem` was used as the compared target structure.
- Total Trainer Pokémon held-item slots stayed stable across before/after/reload.
- Regular Trainer Held Items changed as the intended target class.
- Boss and Important Trainer Held Items were not targeted by this smoke.
- Existing bad-item count increased in the Regular-only target result because Ban Bad was not enabled; this is expected for this no-filter smoke and is not a failure criterion.
- TMs were not written as held items in this run.

## Preserve and trainer-class findings

- Boss Trainer Held Items stayed preserve-only stable.
- Important Trainer Held Items stayed preserve-only stable.
- `shouldNotGetBuffs` Trainer Held Items stayed preserve-only stable.
- Regular Trainer class slot count remained stable.

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
| `trainerHeldItemsNonZeroAfter` | `1577` |
| `trainerHeldItemsNonZeroReload` | `1577` |
| `trainerHeldItemsBadBefore` | `0` |
| `trainerHeldItemsBadAfter` | `394` |
| `trainerHeldItemsBadReload` | `394` |
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

- No active blocker for Regular Trainer Held Items in the tested no-filter scope.
- Bad items are possible without a Ban Bad option; this remains expected behavior for the no-filter Trainer Held Item scope and does not validate any Ban Bad behavior.
- Consumable-only, sensible-only and highest-level-only Trainer Held Item filters remain untested.
- Starter Held Items remain a separate unpromoted scope.

## Evaluation

Regular Trainer Held Items are GUI-compatible in the tested CFRU/DPE Gen9-BPRE no-filter scope. Boss and Important Trainer Held Items remain covered by their separate smoke protocols. This smoke does not promote Trainer Held Item filters, Starter Held Items, Wild Held Items, Field Items, Pickup, Shops or any other randomizer scope.

## Next minimal step

Decide whether Trainer Held Item filter options need separate coverage. If not, move to a Starter Held Items smoke.
