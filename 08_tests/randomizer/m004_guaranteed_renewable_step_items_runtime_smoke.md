# M-004 Guaranteed Renewable Step Items — sanitized runtime smoke

**Status:** `PASS_TARGETED_RUNTIME_SMOKE_WITH_CAVEATS`

## Evidence classification

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS:** The
runtime-tested CFRU M-004 candidate is
`aad9c76d537cf812673e1cd3e69faffd435ff692`.

The integrated CFRU revision is
`520fc7feeb7494b5f8f0555e348c13f0e847304b`. It is one commit ahead of the
tested candidate with no additional file changes, but is not claimed to have
been separately runtime-tested.

## Reported checks

| Check | Result |
|---|---|
| Underground Pass guaranteed renewable spawn | **PASS** |
| Underground Pass repeat regeneration cycle | **PASS** |
| Representative Sevii renewable group | **PASS** |
| Mt. Moon remains vanilla/random and is not guaranteed | **PASS** |
| Itemfinder behavior | **PASS** |
| Normal one-time hidden-item behavior remains unchanged | **PASS** |
| Representative UPR-FVX Field Items smoke preserves randomized item semantics | **PASS** |

## Scope and caveats

This is targeted, user-supplied runtime evidence for M-004 only. It does not
prove a broad playthrough, target-emulator compatibility, Ironmon Tracker
compatibility, randomizer behavior beyond the recorded checks, or a stable
support profile.

No ROMs, saves, emulator states, builds, tool binaries, private paths, hashes,
screenshots, raw logs, tokens, secrets, or `.env` files are included.
