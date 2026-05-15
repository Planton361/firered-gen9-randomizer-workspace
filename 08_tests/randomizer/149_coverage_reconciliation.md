# Diagnose 149: Randomizer Feature Coverage Reconciliation

## Scope

- Branch: `analysis/upr-fvx-cfru-dpe-coverage-reconciliation`
- Goal: reconcile current coverage and roadmap state after the tested Held Items scope closed and the Wild Encounters plan was merged.
- Mode: read-only documentation reconciliation only.
- No code changes, no build, no Randomizer run, no ROM or artifact access.
- Historical diagnostics are not rewritten; only current-state documentation is updated.

## Inputs checked

- Current workspace state documents and roadmap files.
- Feature coverage matrix.
- Randomizer diagnostics README.
- CFRU/DPE encounter systems model.
- Diagnose 148 Wild Encounters scope diagnostics plan.
- Tool manifest for status context; no manifest change was needed.
- Additional `rg` pass for: starter, static, gift, trainer species, evolution, learnset, moveset, ability, hidden ability, move data, move names, type chart, trade, palette, graphics, misc, day night, swarm, dexnav and raid.

## Already completed major scopes

The current documentation supports treating these large scopes as completed or covered in their tested CFRU/DPE Gen9-BPRE slices:

- Standard Wild / Surfing / Fishing / Rock Smash P0.
- Starter Species.
- Static/Gift Species.
- Trainer Species.
- Evolutions Species.
- Base Stats / Types / Abilities.
- Ability1/2 and Hidden Ability write coverage.
- Trainer Movesets and Movesets combinations after Learnset reader fixes.
- Learnsets/Movesets coverage where documented, including bounded/repointing learnset write and GUI-flow safety.
- MoveData read/model coverage where documented.
- TM/HM and Tutor compatibility/write scopes where documented.
- Field Items.
- Pickup Items.
- Shop Items.
- Held Items, closed by Diagnose 147 in the tested individual scopes.

## Partially covered or open scopes

These remain consciously separate, partially covered or open:

- CFRU Day/Night Wild encounters.
- Swarms.
- Roamers.
- DexNav.
- Raids.
- Altering Cave / Tanoby and other special-case encounter systems.
- In-Game Trades.
- Move Names / descriptions / text-menu paths.
- Type Chart / Type Effectiveness.
- Palettes / Graphics, beyond defensive palette load/save and documented palette model work.
- Misc Tweaks.
- Evolution method writer and additional evolution suboptions beyond the documented species/similar-strength/same-typing slices.
- Learnset edge cases not covered by completed bounded/repointing/GUI-flow diagnostics.
- Optional combinations that were intentionally not required, such as Boss/Important Trainer Held Item filter combinations.

## Corrected coverage and roadmap assessment

Standard Wild Encounters should not be treated as the next fresh major scope. The current roadmap should distinguish between:

- Completed Standard Wild P0 coverage: regular Gen3 encounter tables for walking/grass/cave, surfing, fishing and rock smash in the prior P0/P1 history.
- Newly planned Wild Encounter diagnostics in Diagnose 148: useful only if scoped to the remaining CFRU/DPE encounter-system risks and candidate structure validation, not as a retest of already covered Standard Wild.
- Open special encounter systems: Day/Night, Swarms, Roamers, DexNav, Raids and Altering Cave/Tanoby-style special cases.

Therefore, the next major scope should be a read-only CFRU/DPE special Wild Encounter systems diagnostic rather than a broad Standard Wild Encounter write smoke.

## Recommended next major scope

Recommended next scope: CFRU Day/Night and special Wild Encounter systems read-only diagnostics.

Rationale:

- Held Items are closed in the tested scope.
- Standard Wild / Surfing / Fishing / Rock Smash P0 is already listed as done.
- Diagnose 148 correctly separated Wild Encounters from Wild Held Items, but the reconciliation narrows the next practical step to unresolved encounter-system variants.
- The encounter systems model and rg sweep point to Day/Night, Swarm, Roamer, DexNav, Raid and special-table concerns as genuinely open work.
- A read-only diagnostic can classify what is present in the candidate without risking ROM writes or redoing old Standard Wild coverage.

## Recommended next branch

`analysis/upr-fvx-cfru-dpe-special-wild-encounter-systems-scope-plan`

Alternative if the team wants to continue directly from Diagnose 148 naming:

`test/upr-fvx-cfru-dpe-wild-encounters-special-systems-diagnostics`

## Required next diagnostic questions

- Which CFRU/DPE special encounter systems are present in the candidate source?
- Are Day/Night encounter tables separate from standard Gen3 tables?
- Are Swarm, Roamer, DexNav, Raid, Altering Cave or Tanoby-like tables discoverable through existing FVX handlers?
- Which systems are read-only detectable but unsupported for write?
- Which systems should remain preserve-only?
- Which systems require a new parser/model before any smoke?
- How can Standard Wild P0 be kept out of the next diagnostic?

## Future metrics for the next scope

- `candidateLoaded`
- `specialEncounterScanSuccessful`
- `standardWildRetested=false`
- `dayNightSystemObserved`
- `dayNightTableCount`
- `swarmSystemObserved`
- `swarmTableCount`
- `roamerSystemObserved`
- `roamerCount`
- `dexNavSystemObserved`
- `dexNavTableCount`
- `raidSystemObserved`
- `raidTableCount`
- `alteringCaveOrTanobyObserved`
- `specialEncounterUnsupportedCount`
- `specialEncounterPreserveOnlyCount`
- `invalidSpecialEncounterSpecies`
- `unloadedSpecialEncounterSpecies`
- `fallbackSpecialEncounterSpecies`
- `placeholderSpecialEncounterSpecies`
- `heldItemScopeChanged=false`
- `trainerScopeChanged=false`
- `starterScopeChanged=false`
- `staticGiftScopeChanged=false`
- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `shopScopeChanged=false`

## Risks and assumptions

- This reconciliation relies on documented current-state files and rg evidence; it does not rerun old diagnostics.
- Some older entries are historical and may use older status language; they are not edited here.
- Standard Wild is considered covered only for the documented P0 standard table scope, not for CFRU/DPE special encounter systems.
- Open special systems may require separate parser/model work before any write smoke.
- No private paths, ROM names, hashes, raw pointers, offsets, raw bytes or script data are documented.

## Conclusion

The coverage matrix should move forward from completed Held Items and already covered Standard Wild P0 toward special Wild Encounter systems. The next minimal step is a read-only scope plan or diagnostic for CFRU Day/Night and other special encounter systems, explicitly avoiding a duplicate Standard Wild Encounter retest.
