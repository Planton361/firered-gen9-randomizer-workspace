# 205 - Intro Mon Visual Source Fix Smoke

## Scope

Sanitized local evidence for the UPR-FVX PR #109 Intro Mon visual-source fix.

Codex did not read, copy, modify, generate or run any ROMs. This file intentionally contains no ROM paths, hashes,
full logs, screenshots, saves, emulator states, output ROM names, secrets, tokens or `.env` details.

## Context

- Previous local finding: known FRLG Intro Mon sources changed from Nidoran female to Hitmontop, but the visible Oak
  intro sprite stayed Nidoran female ingame.
- PR #108 diagnostic evidence found plausible unchanged visual sources in the normal Species asset tables:
  `PokemonFrontImages` and `PokemonNormalPalettes` entries for Nidoran female.
- PR #109 fix: detected CFRU/DPE Gen9 BPRE now syncs the Nidoran female `PokemonFrontImages` and
  `PokemonNormalPalettes` entries to the selected intro species' asset pointers when Intro Mon is randomized.

## Local Smoke

- PR #109 was tested locally by the user.
- Visible Oak intro sprite changed away from Nidoran female.
- No crash, freeze or garbled sprite was observed during the targeted ingame smoke.

## Status

- `FVX-GEN-003` / Intro Mon visual mismatch is locally fixed for the targeted CFRU/DPE Gen9 BPRE smoke.
- This is targeted ingame-smoke evidence, not a full playthrough.
- No P1 promotion is made.

## Follow-up

- Keep a broader caveat for untested Intro Mon edge cases and full-playthrough coverage.
- Continue sharing only sanitized evidence for any follow-up Intro Mon or visual-source issue.
