# 203 Runtime Source Trainer Randomization Smoke

## Scope

Sanitized local evidence for UPR-FVX PR #105 after PR #104 strict runtime-source sync.

This records that strict runtime-source TrainerData rows are not only loaded and
saved, but also made eligible for Trainer Pokemon randomization.

Codex did not run a ROM, create an output ROM, read private ROM data, inspect
raw logs, or document private paths.

## Pin

- UPR-FVX PR: #105
- Workspace branch: `randomizer/sync-runtime-source-trainer-randomization`
- Workspace submodule pin: `c0d8e33f3547020c6fd2fe5baffbc80ec93f9197`

## Local Sanitized Evidence

The PR #105 branch was tested locally outside Codex with a private ROM and a
new output ROM.

Targeted runtime-source audit for Viridian Forest trainer IDs `531/532`:

| trainerId | loadedParty | rawParty | loadedRawPartyComparison |
|---:|---|---|---|
| 531 | `[Klawf Lv7, Togepi Lv8]` | `[Klawf Lv7, Togepi Lv8]` | `match` |
| 532 | `[Eiscue Lv7, Rampardos Lv7, Aron Lv7]` | `[Eiscue Lv7, Rampardos Lv7, Aron Lv7]` | `match` |

Ingame smoke:

- The Viridian Forest trainer that previously still showed vanilla
  Metapod/Caterpie now shows Eiscue.
- This confirms the strict runtime-source TrainerData row is loaded, randomized,
  saved, and used by the observed in-game battle for this targeted case.

## Status Impact

- Trainer/Foe runtime-source strict sync plus randomizer eligibility is locally
  confirmed for Viridian Forest trainer IDs `531/532`.
- This evidence is targeted, not a full Trainer/Foe P1 promotion.
- Loaded-mismatch, invalid-pointer, empty-party and out-of-range audit rows
  remain follow-up scope.
- Further trainer battles still need separate sanitized local evidence when they
  are suspected of using different runtime sources.

## Safety

Do not commit or post ROMs, output ROMs, real logs, private paths, hashes,
screenshots, saves, emulator states, secrets, tokens or `.env` data.
