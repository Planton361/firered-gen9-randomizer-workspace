# 204 Runtime Source Trainer Randomization Smoke

## Scope

Sanitized local evidence for UPR-FVX PR #105 after PR #104 strict
runtime-source sync.

This records that strict `VALID_RUNTIME_NOT_LOADED` runtime-source TrainerData
rows are loaded, made eligible for Trainer Pokemon randomization, saved, and
observed in-game for the targeted Viridian Forest case.

Codex did not run a ROM, create an output ROM, read private ROM data, inspect
raw logs, or document private paths.

## Pin

- UPR-FVX PR: #105
- Workspace branch: `randomizer/sync-runtime-source-trainer-randomization-smoke`
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

Runtime-source audit on the randomized output ROM:

- `trainer runtime source audit mode=unloaded-valid-parties`
- `total=0`

This is equivalent to `outputValidRuntimeNotLoadedCount=0` for the focused
audit view: no valid script-referenced runtime TrainerData rows remained in the
unloaded-valid-parties report after the randomized output was created.

Additional observed examples:

- Rival 2 trainer IDs `329/330/331` show randomized parties.
- Brock trainer ID `414` shows randomized party `[Drifloon Lv12, Growlithe Lv14]`.

## Status Impact

- Strict Runtime Trainer Source Sync plus `RUNTIME-SOURCE` Trainer Pokemon
  randomization is locally confirmed for the targeted Viridian Forest `531/532`
  case.
- The randomized output audit reports `unloaded-valid-parties total=0`.
- This evidence is targeted and does not promote broader Trainer/Foe P1 support.
- Loaded-mismatch, invalid-pointer, empty-party, out-of-range rows and full
  playthrough coverage remain follow-up scope.

## Safety

Do not commit or post ROMs, output ROMs, real logs, private paths, hashes,
screenshots, saves, emulator states, secrets, tokens or `.env` data.
