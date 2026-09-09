# M-008 Optional Bill / Sevii handoff — sanitized runtime smoke

**Status:** `PASS_TARGETED_RUNTIME_SMOKE_WITH_CAVEATS`

## Evidence classification

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS:** The
runtime-tested CFRU M-008 candidate is
`07b86d44b9c98354c815ae56f7f26072fcc0147a`.

The integrated CFRU revision is
`a869c3526d7f76c54082bc71e236742564319e02`. It is one commit ahead of the
tested candidate with no additional file changes, but is not claimed to have
been separately runtime-tested.

## Reported checks

| Check | Result |
|---|---|
| Blaine completion | **PASS** |
| No automatic Bill dialogue after leaving the Gym | **PASS** |
| No automatic Yes/No Sevii prompt or forced One Island travel | **PASS** |
| Outdoor Bill is removed | **PASS** |
| Bill is available in Cinnabar Pokémon Center | **PASS** |
| Choosing NO leaves Bill available | **PASS** |
| Re-entry/save-reload preserves the optional state | **PASS** |
| Choosing YES uses the original One Island travel flow | **PASS** |
| Sevii travel and return-from-Sevii scene | **PASS** |
| M-003 instant Nurse remains functional | **PASS** |
| Name Rater remains functional | **PASS** |
| M-005 through M-007 remain intact | **PASS** |

## Scope and caveats

This is targeted, user-supplied runtime evidence for M-008 only. It does not
prove a broad playthrough, target-emulator compatibility, Ironmon Tracker
compatibility, randomizer behavior beyond the recorded checks, or a stable
support profile.

No ROMs, saves, emulator states, builds, tool binaries, private paths, hashes,
screenshots, raw logs, tokens, secrets, or `.env` files are included.
