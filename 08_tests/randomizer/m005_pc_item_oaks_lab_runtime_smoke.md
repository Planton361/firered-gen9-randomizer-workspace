# M-005 PC Item -> Oak's Lab — sanitized runtime smoke

**Status:** `PASS_TARGETED_RUNTIME_SMOKE_WITH_CAVEATS`

## Evidence classification

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS:** The
runtime-tested CFRU M-005 candidate is
`10a338eca514c3ca1f614586d1054a89f039010a`.

The integrated CFRU revision is
`4a9698467600500d18ec8c08f9269f0d6ad008e6`. It is one commit ahead of the
tested candidate with no additional file changes, but is not claimed to have
been separately runtime-tested.

## Reported checks

| Check | Result |
|---|---|
| Fresh New Game has no starter Potion in Player PC storage | **PASS** |
| Oak's Lab Potion Item Ball works | **PASS** |
| Pickup disappearance and persistence | **PASS** |
| Starter, Rival, Oak's Lab flow, and warps remain intact | **PASS** |
| Normal Player PC storage remains functional | **PASS** |
| Representative UPR-FVX Field Items behavior remains compatible | **PASS** |

## Scope and caveats

This is targeted, user-supplied runtime evidence for M-005 only. It does not
prove a broad playthrough, target-emulator compatibility, Ironmon Tracker
compatibility, randomizer behavior beyond the recorded checks, or a stable
support profile.

No ROMs, saves, emulator states, builds, tool binaries, private paths, hashes,
screenshots, raw logs, tokens, secrets, or `.env` files are included.
