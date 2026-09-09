# M-006 Talk to Mom / Faster New Game handoff — sanitized runtime smoke

**Status:** `PASS_TARGETED_RUNTIME_SMOKE_WITH_CAVEATS`

## Evidence classification

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS:** The final
runtime-tested CFRU M-006 candidate is
`574318a1af2801c161cd40d9687ed2b65dd3b92a`.

The integrated CFRU revision is
`237fc61ac52bea6978f4b434c06fc3f1f11e5dcc`. It is one commit ahead of the
tested candidate with no additional file changes, but is not claimed to have
been separately runtime-tested.

## Reported checks

| Check | Result |
|---|---|
| Fresh New Game cannot leave Player House before talking to Mom | **PASS** |
| Player House exit blocker | **PASS** |
| Mom magic-trick handoff | **PASS** |
| Fast Oak's Lab scene player/camera state | **PASS** |
| Oak at `(6,3)`, facing down | **PASS** |
| Direct starter-choice state | **PASS** |
| Starter selection | **PASS** |
| Rival starter selection and battle | **PASS** |
| Oak's Lab exit and warps | **PASS** |
| M-005 Oak's Lab Potion remains functional | **PASS** |
| Post-rival Mom healing | **PASS** |

## Superseded candidates

Earlier M-006 candidates had runtime defects and were superseded by final
candidate `574318a1af2801c161cd40d9687ed2b65dd3b92a`. This record does not
promote those earlier candidates to PASS.

## Scope and caveats

This is targeted, user-supplied runtime evidence for M-006 only. It does not
prove a broad playthrough, target-emulator compatibility, Ironmon Tracker
compatibility, randomizer behavior beyond the recorded checks, or a stable
support profile.

No ROMs, saves, emulator states, builds, tool binaries, private paths, hashes,
screenshots, raw logs, tokens, secrets, or `.env` files are included.
