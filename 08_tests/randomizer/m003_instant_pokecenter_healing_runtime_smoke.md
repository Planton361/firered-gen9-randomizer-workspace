# M-003 Instant PokeCenter Healing — sanitized runtime smoke

**Status:** `PASS_TARGETED_RUNTIME_SMOKE_WITH_CAVEATS`

## Evidence classification

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS:** The
runtime-tested CFRU M-003 candidate is
`d6571f4a8c371075da1cf6341c5d01f89903d426`.

The integrated CFRU revision is
`215bd44d340c16076b1817b9c6db038d54fe5f76`. It is one commit ahead of the
tested candidate with no additional file changes, but is not claimed to have
been separately runtime-tested.

## Reported checks

| Check | Result |
|---|---|
| Healing begins without the normal Nurse dialogue sequence | **PASS** |
| Short PokeCenter healing effect plays | **PASS** |
| Full-party healing | **PASS** |
| Status, PP, and fainted-party restoration where tested | **PASS** |
| Repeated Nurse interaction | **PASS** |
| Second Kanto Center | **PASS** |
| Sevii Center | **PASS** |
| Trainer Tower retains original Nurse interaction | **PASS** |
| Name Rater, PC, and warps show no regression | **PASS** |

## Scope and caveats

This is targeted, user-supplied runtime evidence for M-003 only. It does not
prove a broad playthrough, target-emulator compatibility, Ironmon Tracker
compatibility, randomizer behavior beyond the recorded checks, or a stable
support profile.

No ROMs, saves, emulator states, builds, tool binaries, private paths, hashes,
screenshots, raw logs, tokens, secrets, or `.env` files are included.
