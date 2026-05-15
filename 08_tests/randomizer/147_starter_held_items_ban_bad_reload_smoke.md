# Diagnose 147: Starter Held Items Ban Bad Reload Smoke

## Scope

- Branch: `test/upr-fvx-cfru-dpe-starter-held-items-ban-bad-reload-smoke`
- Target: CFRU/DPE Gen9-BPRE candidate source, sanitized local-only harness.
- Feature scope: Starter Held Items with Ban Bad.
- Settings scope:
  - `randomizeStartersHeldItems=true`
  - `banBadRandomStarterHeldItems=true`
  - `randomizeWildPokemonHeldItems=false`
  - Trainer Held Items disabled for Boss, Important and Regular Trainers.
- Explicitly out of scope: Wild/Encounter Held Items, Trainer Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer scopes.

## Baseline

- Diagnose 146 established Starter Held Items without Ban Bad as reload-stable.
- Gen3/FRLG model: one shared Starter Held Item slot.
- `heldItemPoolAllowedSize=212`.
- `heldItemPoolNonBadSize=161`.
- `canTMsBeHeld=true`.

## Smoke result

PASS.

The Starter Held Items + Ban Bad Write/Reload-Smoke completed successfully. Save, log, output ROM creation and reload all succeeded. The shared Starter Held Item slot was written from the non-bad pool, reloaded stably and did not affect Wild, Trainer, Field Item, Pickup or Shop scopes.

## Starter Held Items findings

- `getStarterHeldItems()` / `setStarterHeldItems(...)` behavior remained reload-stable with Ban Bad enabled.
- One shared Starter Held Item slot was observed.
- The slot changed from empty to non-empty after randomization.
- No bad item and no TM was written in this run.
- No invalid, unloaded, fallback or placeholder item write was observed.

## Ban Bad and pool findings

- Allowed held-item pool size: `212`.
- Non-bad held-item pool size: `161`.
- Bad starter held-item pool candidates considered/excluded: `212` / `51`.
- Bad Starter Held Item writes: `0`.
- Starter Held Items + Ban Bad is therefore validated in the tested narrow Starter-only scope.

## Reload findings

- Reload succeeded.
- Starter Held Item reload mismatches: `0`.
- Starter Held Item total stayed stable: `1 / 1 / 1`.
- Non-zero count stayed reload-stable: `0 / 1 / 1`.

## Scope isolation findings

- Wild/Encounter Held Items changed: `false`.
- Trainer Held Items changed: `false`.
- Field Items changed: `false`.
- Pickup changed: `false`.
- Shops changed: `false`.

## Held Items scope closure assessment

The tested Held Items scope is complete for CFRU/DPE Gen9-BPRE in the documented individual scopes:

- Wild/Encounter Held Items without Ban Bad: passed.
- Wild/Encounter Held Items with Ban Bad: passed.
- Trainer Held Items Boss no-filter: passed.
- Trainer Held Items Important no-filter: passed.
- Trainer Held Items Regular no-filter: passed.
- Trainer Held Items Regular combined filters: passed.
- Starter Held Items without Ban Bad: passed.
- Starter Held Items with Ban Bad: passed.

Boss/Important filter combinations remain intentionally unpromoted because they were not requested after the Regular combined-filter pass. No other Held Items follow-up is required for the tested scope unless broader class/filter-combination coverage is explicitly requested.

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
| `starterHeldItemsTotalBefore` | `1` |
| `starterHeldItemsTotalAfter` | `1` |
| `starterHeldItemsTotalReload` | `1` |
| `starterHeldItemsNonZeroBefore` | `0` |
| `starterHeldItemsNonZeroAfter` | `1` |
| `starterHeldItemsNonZeroReload` | `1` |
| `starterHeldItemsBadBefore` | `0` |
| `starterHeldItemsBadAfter` | `0` |
| `starterHeldItemsBadReload` | `0` |
| `starterHeldItemsTMBefore` | `0` |
| `starterHeldItemsTMAfter` | `0` |
| `starterHeldItemsTMReload` | `0` |
| `starterHeldItemReloadMismatches` | `0` |
| `invalidStarterHeldItemWrites` | `0` |
| `unloadedStarterHeldItemWrites` | `0` |
| `fallbackStarterHeldItemWrites` | `0` |
| `placeholderStarterHeldItemWrites` | `0` |
| `badStarterHeldItemWrites` | `0` |
| `heldItemPoolAllowedSize` | `212` |
| `heldItemPoolNonBadSize` | `161` |
| `badStarterHeldItemPoolCandidates` | `212` |
| `badStarterHeldItemPoolExcluded` | `51` |
| `canTMsBeHeld` | `true` |
| `wildHeldItemScopeChanged` | `false` |
| `trainerHeldItemScopeChanged` | `false` |
| `fieldItemScopeChanged` | `false` |
| `pickupScopeChanged` | `false` |
| `shopScopeChanged` | `false` |
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

## Risks and blockers

- No active blocker for Starter Held Items + Ban Bad in the tested scope.
- Boss/Important Trainer filter combinations remain unpromoted by design.
- The next Randomizer feature scope should start separately; this smoke does not promote any non-Held-Item scope.

## Evaluation

Starter Held Items + Ban Bad are GUI-compatible in the tested CFRU/DPE Gen9-BPRE scope. The tested Held Items scope can be closed.

## Next minimal step

Close Held Items scope and prepare the next major Randomizer feature scope.
