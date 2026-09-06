# M-002 Viridian Forest Nurse — sanitized runtime smoke

**Status:** `PASS_TARGETED_RUNTIME_SMOKE_WITH_CAVEATS`

## Evidence classification

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS:** The
workspace M-002 candidate pins the exact CFRU candidate from Draft PR #36.

## Reported checks

| Check | Result |
|---|---|
| Nurse visible and usable | **PASS** |
| Whole-party healing | **PASS** |
| Poison blocks healing | **PASS** |
| Prompt text displays correctly | **PASS** |
| Success text displays correctly | **PASS** |
| Corrected poison-refusal text displays correctly | **PASS** |

The corrected refusal text is:

```text
Sorry, but I can't heal if
you have a poisoned Pokémon.
```

## Scope and caveats

This is targeted, user-supplied runtime evidence for M-002 only. It does not
prove a broad playthrough, target-emulator compatibility, Ironmon Tracker
compatibility, randomizer behavior beyond the existing preserved contract, or
a stable support profile.

No ROMs, saves, emulator states, builds, tool binaries, private paths, hashes,
screenshots, raw logs, tokens, secrets, or `.env` files are included.
