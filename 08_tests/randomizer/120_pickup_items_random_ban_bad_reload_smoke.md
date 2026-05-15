# 120 - CFRU/DPE Pickup Items Random Ban Bad Reload-Smoke

## Scope

Sanitized Pickup-only Write/Reload-Smoke for `FVX-ITEM-010 Pickup Items Random` with `Settings.PickupItemsMod.RANDOM` and `banBadRandomPickupItems=true`.

This block used the existing UPR-FVX pin `a2373888ad17145f270ebf6ff17303af41aa86eb` and did not change code, submodule pins, Field Items, Shops, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution, Scriptparser or Text/Menu scope.

Local harness, output ROM and log artifacts stayed ignored under `05_builds/**` and are not committed. No private paths, ROM names, hashes, pointers, offsets, raw bytes, script data or log excerpts are documented.

## Preconditions checked

- Workspace PR #164 was merged before branch creation.
- Branch was created from current `origin/main`.
- Workspace submodule `02_external/upr-fvx` is pinned to `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- A local CFRU/DPE Gen9-BPRE candidate was explicitly approved for this Pickup-only smoke.

## Smoke settings

- Feature: `FVX-ITEM-010 Pickup Items Random / Ban Bad Items`.
- `PickupItemsMod=RANDOM`.
- `banBadRandomPickupItems=true`.
- Field Items unchanged.
- Shops unchanged.
- Held Items unchanged.
- No Pickup codefix or submodule update.

## Sanitized result

| Metric | Value |
| --- | --- |
| `candidateFilesChecked` | `101` |
| `candidateLoaded` | `true` |
| `smokeExecuted` | `true` |
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| `reloadSuccessful` | `true` |
| `pickupLocatorSuccessful` | `true` |
| `pickupItemsTotalBefore` | `16` |
| `pickupItemsTotalAfter` | `16` |
| `pickupItemsTotalReload` | `16` |
| `pickupExpectedCount` | `16` |
| `pickupEntrySize` | `4` |
| `pickupProbabilitySlots` | `10` |
| `pickupProbabilityModelStable` | `true` |
| `pickupItemReloadMismatches` | `0` |
| `pickupTableLengthMismatches` | `0` |
| `pickupProbabilityMismatches` | `0` |
| `pickupCommonRarePolicyViolations` | `0` |
| `invalidPickupItemWrites` | `0` |
| `unloadedPickupItemWrites` | `0` |
| `fallbackPickupItemWrites` | `0` |
| `placeholderPickupItemWrites` | `0` |
| `badPickupItemWrites` | `0` |
| `pickupBadItemPoolCandidates` | `51` |
| `pickupBadItemPoolExcluded` | `51` |
| `pickupPoolNonBadSize` | `485` |
| `nonBadPickupPoolSize` | `485` |
| `pickupTmPolicyViolations` | `0` |
| `pickupPoolAllowedSize` | `536` |
| `pickupTmPoolPolicy` | `tms allowed` |
| `canTMsBeHeld` | `true` |
| `isTMsReusable` | `false` |
| `pickupLocatorMode` | `stable-metadata` |
| `pickupContentLocatorUsed` | `false` |
| `pickupLocatorCandidateCount` | `1` |
| `pickupLocatorStableAfterWrite` | `true` |
| `pickupReloadLocatorRegression` | `false` |
| `fieldItemScopeChanged` | `false` |
| `shopItemScopeChanged` | `false` |
| `heldItemScopeChanged` | `false` |
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

## Interpretation

The Pickup Ban Bad smoke passes in the same reload-stable table scope proven by Diagnose 118.

`banBadRandomPickupItems=true` correctly restricts the Pickup candidate pool from the allowed pool to the non-bad allowed pool:

- `pickupPoolAllowedSize=536`.
- `pickupPoolNonBadSize=485`.
- `pickupBadItemPoolCandidates=51`.
- `pickupBadItemPoolExcluded=51`.
- `badPickupItemWrites=0`.

Reload confirms the written Pickup item IDs persist exactly:

- `pickupItemReloadMismatches=0`.
- `pickupTableLengthMismatches=0`.
- `pickupProbabilityMismatches=0`.
- `pickupReloadLocatorRegression=false`.

## Preserve / skip result

- Only the clearly located Pickup table was written.
- Table length `16` was preserved.
- Entry size `4` was preserved.
- Probability slots `10` were preserved.
- `setPickupItems(...)` remained limited to item-ID fields.
- Invalid, unloaded, fallback, placeholder and bad items were not written.
- TMs remained allowed for Pickup because `canTMsBeHeld=true` and `isTMsReusable=false`.
- Field Items, Shops and Held Items were unchanged.

## Feature status

`FVX-ITEM-010 Pickup Items Random / Ban Bad Items` is now `GUI-kompatibel` in the tested Pickup-only scope:

- `PickupItemsMod.RANDOM`.
- `banBadRandomPickupItems=false` from Diagnose 118.
- `banBadRandomPickupItems=true` from Diagnose 120.

No status upgrade is made for Field Items, Shops, Encounter Held Items, Trainer Held Items or Starter Held Items.

## Next recommendation

Proceed to a separate Shops-only scope plan before any Shop writer smoke.
