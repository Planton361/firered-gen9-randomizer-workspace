# Diagnose 146: Starter Held Items Reload Smoke

## Scope

- Branch: `test/upr-fvx-cfru-dpe-starter-held-items-reload-smoke`
- Target: CFRU/DPE Gen9-BPRE candidate source, sanitized local-only harness.
- Feature scope: Starter Held Items without Ban Bad.
- Settings scope:
  - `randomizeStartersHeldItems=true`
  - `banBadRandomStarterHeldItems=false`
  - `randomizeWildPokemonHeldItems=false`
  - Trainer Held Items disabled for Boss, Important and Regular Trainers.
- Explicitly out of scope: Wild/Encounter Held Items, Trainer Held Items, Field Items, Pickup, Shops, Starter Ban Bad and all non-Held-Item randomizer scopes.

## Baseline

- Diagnose 138 established Starter Held Items as readable with `starterHeldItemsTotal=1` and no initial held item.
- Diagnose 139 and 140 established Wild Held Items as reload-stable without and with Ban Bad.
- Diagnoses 141, 142, 143 and 145 established Trainer Held Items as reload-stable for Boss, Important, Regular and Regular filtered scopes.
- Starter Held Items were previously unpromoted.

## Smoke result

PASS.

The Starter Held Items-only Write/Reload-Smoke completed successfully. Save, log, output ROM creation and reload all succeeded. The shared Gen3/FRLG Starter Held Item slot was written, reloaded stably and did not affect Wild, Trainer, Field Item, Pickup or Shop scopes.

## Starter Held Items findings

- `getStarterHeldItems()` / `setStarterHeldItems(...)` behavior was validated by before/after/reload comparison.
- One shared Starter Held Item slot was observed, matching the Gen3/FRLG model noted in earlier diagnostics.
- The slot changed from empty to non-empty after randomization.
- No bad item and no TM was written in this run.
- Starter Ban Bad was not enabled and is not promoted by this smoke.

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
| `heldItemPoolAllowedSize` | `212` |
| `heldItemPoolNonBadSize` | `161` |
| `canTMsBeHeld` | `true` |
| `wildHeldItemScopeChanged` | `false` |
| `trainerHeldItemScopeChanged` | `false` |
| `fieldItemScopeChanged` | `false` |
| `pickupScopeChanged` | `false` |
| `shopScopeChanged` | `false` |
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

## Risks and blockers

- No active blocker for Starter Held Items without Ban Bad in the tested scope.
- Starter Ban Bad remains unpromoted and requires a separate smoke.
- This smoke does not promote Wild Held Items, Trainer Held Items, Field Items, Pickup, Shops or other randomizer scopes beyond their already documented separate results.

## Evaluation

Starter Held Items without Ban Bad are GUI-compatible in the tested CFRU/DPE Gen9-BPRE scope. The Held Items scope is now covered for Wild, Wild+Ban Bad, Trainer Boss, Trainer Important, Trainer Regular, Trainer Regular filtered and Starter without Ban Bad in their respective tested scopes. Starter Ban Bad remains open.

## Next minimal step

Run Starter Held Items + Ban Bad smoke if Starter Ban Bad coverage is required.
