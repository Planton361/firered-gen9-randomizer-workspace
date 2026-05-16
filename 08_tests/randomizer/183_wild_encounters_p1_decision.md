# 183 - Wild Encounters P1 Decision

## Decision

Wild Encounters can be promoted to `P1-supported` for the documented Standard/Fallback Wild Encounter writer/reload scope in the tested private target context.

## Evidence Reviewed

- ROM-free Wild Encounter decision/option slices are present.
- ROM-free synthetic Writer/Reload Equality is present.
- Opt-in ROM-facing smoke harness is present.
- Sanitized local ROM-facing smoke after UPR-FVX PR #66 passed:
  - Test: `Gen3WildEncounterRomSmokeTest`
  - Tests: 1
  - Failures: 0
  - Errors: 0
  - Skipped: 0

## Scope Boundaries

- This decision does not cover CFRU Day/Night Wild, Swarms, Roamers, DexNav, Raids, Wild Double Battles or other special Wild systems.
- No new ROM execution was performed for this decision.
- No ROM path, ROM hash, full log, output ROM, save, emulator state, build artifact, tool binary, secret, token or `.env` detail is documented.
