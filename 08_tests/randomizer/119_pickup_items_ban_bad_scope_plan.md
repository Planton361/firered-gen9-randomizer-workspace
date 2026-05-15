# 119 - CFRU/DPE Pickup Items Ban Bad Scope Plan

## Scope

Read-only planning block for `FVX-ITEM-010 Pickup Items Random` with `banBadRandomPickupItems=true` on the CFRU/DPE Gen9-BPRE workspace baseline.

This block does not run the Randomizer, does not build, does not change code, does not touch ROM/output artifacts, and does not change `02_external/**`.

## Preconditions checked

- Workspace PR #163 is merged.
- UPR-FVX PR #38 is merged.
- Workspace branch was created from current `origin/main`.
- Workspace submodule `02_external/upr-fvx` is expected at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- Diagnose 118 establishes reload-stable Pickup Random with `banBadRandomPickupItems=false`.

## Relevant code paths

- `Settings.PickupItemsMod.RANDOM` selects Pickup randomization.
- `Settings.banBadRandomPickupItems` is serialized/restored as the Pickup Ban Bad suboption.
- `GameRandomizer.maybeRandomizePickupItems()` calls `ItemRandomizer.randomizePickupItems()` only when `PickupItemsMod.RANDOM` is active.
- `ItemRandomizer.randomizePickupItems()` chooses the candidate pool:
  - `banBadRandomPickupItems=false`: `romHandler.getAllowedItems()`.
  - `banBadRandomPickupItems=true`: `romHandler.getNonBadItems()`.
- `AbstractRomHandler.getAllowedItems()` filters loaded items by `Item::isAllowed`.
- `AbstractRomHandler.getNonBadItems()` filters the allowed set by `!Item::isBad`.
- `ItemRandomizer.randomizePickupItems()` removes TMs only when TMs cannot be held or TMs are reusable.
- `Gen3RomHandler.getPickupItems()` / `setPickupItems(...)` provide the Gen3 Pickup table read/write path.
- Diagnose 118 confirms the reload-stable CFRU/DPE Pickup locator path after PR #38.

## Existing sanitized baseline

From Diagnose 115 and Diagnose 118:

- `pickupItemsTotal=16` / `pickupItemsTotalReload=16`.
- `pickupExpectedCount=16`.
- `pickupEntrySize=4`.
- `pickupProbabilitySlots=10`.
- `pickupProbabilityModelStable=true`.
- `pickupPoolAllowedSize=536`.
- `pickupPoolNonBadSize=485`.
- `pickupBadItemPoolCandidates=51`.
- `pickupBadItemPoolExcluded=51`.
- Existing table diagnostic saw `pickupBadItems=7`, which is a source-table observation, not an allowed future write when Ban Bad is enabled.
- `pickupTmItems=1` in the source table.
- `pickupTmPoolPolicy=tms allowed`.
- `canTMsBeHeld=true`.
- `isTMsReusable=false`.
- Diagnose 118 reload-stable result: `pickupItemReloadMismatches=0`, `pickupLocatorMode=stable-metadata`, `pickupContentLocatorUsed=false`, `pickupReloadLocatorRegression=false`.

## Pickup Ban-Bad scope assessment

A direct Pickup Ban Bad smoke is reviewable and preferred before any fix work.

Reasoning:

- The Ban Bad toggle only changes the item candidate pool from allowed to non-bad allowed items.
- The Pickup table locator/write path was already stabilized by Diagnose 118 / UPR-FVX PR #38.
- Probability slots, table length, entry size and Common/Rare semantics are independent of the Ban Bad pool choice.
- TMs remain allowed for Pickup on this baseline because `canTMsBeHeld=true` and `isTMsReusable=false`.
- No evidence from 115/118 points to a code fix need before testing Ban Bad.

The later smoke should therefore test exactly `PickupItemsMod.RANDOM` plus `banBadRandomPickupItems=true` and should not combine any other Item writer or Held Item scope.

## Bad-item handling policy

- Ban Bad must exclude every allowed item where `Item::isBad` is true from the Pickup candidate pool.
- The expected current aggregate from Diagnose 115 is `pickupBadItemPoolCandidates=51` and `pickupBadItemPoolExcluded=51`.
- The smoke should assert `badPickupItemWrites=0` after reload.
- Existing source-table bad items do not matter as long as the randomized output writes no bad Pickup items.
- Invalid, unloaded, fallback and placeholder items remain forbidden independent of Ban Bad.

## Preserve / skip policy

- Write only the clearly located Pickup table.
- Preserve table length `16`.
- Preserve entry size `4`.
- Preserve Pickup slot order.
- Preserve probability slots `10` and the probability model.
- `setPickupItems(...)` must continue writing only item-ID fields.
- Invalid, unloaded, fallback and placeholder items must not be selected.
- TMs remain selectable only according to `canTMsBeHeld=true` and `isTMsReusable=false`.
- No Field Items, Shops, Encounter Held Items, Trainer Held Items or Starter Held Items may change.
- No TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution, Scriptparser or Text/Menu work is in scope.

## Recommended smoke order

1. Run `test/upr-fvx-cfru-dpe-pickup-items-random-ban-bad-reload-smoke`.
2. Scope: only `FVX-ITEM-010 Pickup Items Random`, `Settings.PickupItemsMod.RANDOM`, `banBadRandomPickupItems=true`.
3. Reuse the UPR-FVX pin from Diagnose 118 unless a separate blocker appears.
4. If all target metrics pass, mark Pickup Ban Bad as tested/GUI-compatible for Pickup Random.
5. Do not upgrade Field Items, Shops or Held Items from this Pickup-only result.

## Later smoke / reload criteria

Required target metrics for the next smoke:

- `candidateLoaded=true`.
- `smokeExecuted=true`.
- `saveSuccessful=true`.
- `logSuccessful=true`.
- `outputRomExists=true`.
- `logNonEmpty=true`.
- `reloadSuccessful=true`.
- `pickupLocatorSuccessful=true`.
- `pickupItemsTotalBefore=16`.
- `pickupItemsTotalAfter=16`.
- `pickupItemsTotalReload=16`.
- `pickupExpectedCount=16`.
- `pickupEntrySize=4`.
- `pickupProbabilitySlots=10`.
- `pickupProbabilityModelStable=true`.
- `pickupItemReloadMismatches=0`.
- `pickupTableLengthMismatches=0`.
- `pickupProbabilityMismatches=0`.
- `pickupCommonRarePolicyViolations=0`.
- `invalidPickupItemWrites=0`.
- `unloadedPickupItemWrites=0`.
- `fallbackPickupItemWrites=0`.
- `placeholderPickupItemWrites=0`.
- `badPickupItemWrites=0`.
- `pickupBadItemPoolCandidates=51`.
- `pickupBadItemPoolExcluded=51`.
- `pickupPoolAllowedSize=536`.
- `pickupPoolNonBadSize=485`.
- `nonBadPickupPoolSize=485` or equivalent sanitized non-bad pool metric.
- `pickupTmPolicyViolations=0`.
- `pickupTmPoolPolicy=tms allowed`.
- `canTMsBeHeld=true`.
- `isTMsReusable=false`.
- `pickupLocatorMode=stable-metadata` or another documented reload-stable mode.
- `pickupContentLocatorUsed=false` after randomized reload, unless a fallback mode is explicitly justified.
- `pickupLocatorCandidateCount=1`.
- `pickupLocatorStableAfterWrite=true`.
- `pickupReloadLocatorRegression=false`.
- `fieldItemScopeChanged=false`.
- `shopItemScopeChanged=false`.
- `heldItemScopeChanged=false`.
- `exceptionClass=none`.
- `stacktrace=none`.

## Feature-status recommendation

If the later smoke passes all target metrics:

- `FVX-ITEM-010 Pickup Items Random` can be documented as GUI-compatible for Random with and without Ban Bad.
- The status must remain Pickup-only.
- Field Items, Shops and Held Items must not be upgraded by this result.

If the smoke fails:

- Keep `FVX-ITEM-010` limited to the already proven `banBadRandomPickupItems=false` scope.
- Plan the narrowest blocker analysis from the failing aggregate metric.
