# M-007 Shortened Oak Parcel Flow — sanitized runtime smoke

**Status:** `PASS_TARGETED_RUNTIME_SMOKE_WITH_CAVEATS`

## Evidence classification

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS:** The
runtime-tested CFRU M-007 candidate is
`00e316532be65f4fdd8e4561b2b2579817a1f64f`.

The integrated CFRU revision is
`62298cf81d4a2b487c8793bad8b6e29906c705f4`. It is one commit ahead of the
tested candidate with no additional file changes, but is not claimed to have
been separately runtime-tested.

## Reported checks

| Check | Result |
|---|---|
| M-006 Mom/start/starter/Rival flow remains functional | **PASS** |
| Temporary Pallet parcel Oak is hidden before Parcel acquisition | **PASS** |
| Original Route 1 Potion Clerk remains functional | **PASS** |
| Route 1 Parcel handoff from all four trigger positions | **PASS** |
| Parcel awarded exactly once; temporary Clerk disappears | **PASS** |
| Save/reload after Parcel preserves expected state | **PASS** |
| Viridian Mart does not duplicate the Parcel handoff | **PASS** |
| Pallet Oak return handoff from both trigger positions | **PASS** |
| Oak removes Parcel and grants Pokedex/unlock state plus five Poke Balls | **PASS** |
| Temporary Oak remains gone afterward | **PASS** |
| Post-Parcel Viridian Mart state is normal | **PASS** |
| Old Man road block/tutorial is skipped | **PASS** |
| Daisy/Town Map and Route 22 post-Parcel state | **PASS** |
| Oak's Lab does not replay the vanilla Parcel scene | **PASS** |
| M-005 Potion and M-006 flow remain intact | **PASS** |

## Scope and caveats

This is targeted, user-supplied runtime evidence for M-007 only. It does not
prove a broad playthrough, target-emulator compatibility, Ironmon Tracker
compatibility, randomizer behavior beyond the recorded checks, or a stable
support profile.

No ROMs, saves, emulator states, builds, tool binaries, private paths, hashes,
screenshots, raw logs, tokens, secrets, or `.env` files are included.
