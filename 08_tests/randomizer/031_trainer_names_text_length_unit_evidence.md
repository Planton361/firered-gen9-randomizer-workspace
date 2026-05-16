# 031 - Trainer Names Text Length Unit Evidence

## Scope

This document records the merged ROM-free UPR-FVX unit-test evidence from PR #52 for `FVX-FOE-013` Trainer Names / Class Names text-length risks.

No ROM, save, emulator state, output ROM, build artifact, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented in this workspace block. No UPR-FVX production code change, Writer-/Reload fix, text-encoding implementation, ROM-facing smoke or P1 promotion is included.

## Pin

- UPR-FVX repository: `02_external/upr-fvx`
- UPR-FVX branch: `compat/firered-gen9-cfru-dpe`
- Merged PR: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/52>
- Workspace submodule pin: `7357b244e01ef2c7790b858d50c19c31ac72e955`
- Previous workspace submodule pin: `d20eb1367c62a4f14c8778bc61ad6904ea76a6d6`

## Tested

The merged UPR-FVX PR extends the existing ROM-free `TrainerNameRandomizerTest` style. It uses a synthetic fake `RomHandler` whose `internalStringLength(...)` can differ from Java `String.length()`.

Covered by the focused unit test:

- ASCII Trainer name inside the encoded/internal limit.
- Trainer name exactly at the encoded/internal limit.
- Trainer name over the encoded/internal limit.
- A synthetic escaped-token-style case where Java length differs from encoded/internal length.
- Trainer Class Name risk where Java `changeTo.length()` can allow a candidate whose synthetic encoded/internal length exceeds the configured class-name limit.

## Not Covered

This evidence does not cover:

- ROM-facing Writer/Reload behavior.
- Real Gen3 fixed-field byte writes.
- Terminator/Padding validity in an actual ROM field.
- Decoded reload equality.
- Actual Gen3 text-encoding safety for arbitrary custom text.
- Any Writer-/Reload fix.
- Any P1 promotion.

## Status

`FVX-FOE-013` remains `tested-non-rom`, not P1-supported.

The new unit test improves synthetic length-risk coverage and makes the `changeTo.length()` class-name risk visible. It does not remove the need for later separately authorized ROM-facing or equivalent writer/reload evidence before any Trainer Names/Class Names P1 discussion.
