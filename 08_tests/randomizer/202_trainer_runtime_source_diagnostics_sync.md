# 202 Trainer Runtime Source Diagnostics Sync

## Scope

Workspace sync for merged UPR-FVX PR #100:
<https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/100>

Workspace branch:
`randomizer/sync-trainer-runtime-source-diagnostics`

Pinned UPR-FVX merge commit:
`87bba797620dd2043f02c11c67f7b752a7238a00`

## What PR #100 Adds

- No-ROM helper coverage for mapping FRLG `trainerbattle` script trainer IDs to `TrainerData` rows.
- Synthetic tests for:
  - valid `trainerbattle` ID to `TrainerData` row mapping
  - invalid/out-of-range trainer IDs producing safe diagnostic entries
  - party pointer and first raw species extraction from synthetic bytes
- An opt-in local diagnostic report extension for trainerbattle runtime-source rows.
- A developer note explaining sanitized evidence expectations.

## Diagnosis Boundary

Trainer Pokemon logs are not writer/runtime proof. UPR-FVX randomization mutates the loaded in-memory trainer list, and the log prints that same list. The Gen3 writer later serializes `TrainerData`, while the CFRU/DPE runtime may use a different script trainer ID, a copied/raw party source, or another battle setup source.

Current hypotheses:

- Script uses a different `trainerbattle` trainer ID than the vanilla FRLG tag expected for the affected battle.
- Runtime uses a separate or copied raw party source instead of the loaded `TrainerData` row that was logged.
- Writer updates a valid `TrainerData` source, but not the source actually used by the affected battle at runtime.

## Workspace Status

Foe Trainer coverage remains CLI-log-clean from exact coverage batches, but ingame status is partial/caveated until local sanitized runtime-source evidence confirms the affected battles use the same `TrainerData` rows and party pointers that UPR-FVX logs and writes.

Known affected local-smoke examples to validate outside this PR:

- second Rival battle
- Brock / first Gym Leader
- selected normal trainers

## Sanitized Evidence Needed

Provide only:

- affected battle label
- expected/logged trainer ID if visible
- observed in-game party summary if known
- redacted runtime-source diagnostic lines showing `trainerId`, `trainerOffset`, `partyPointer`, `partyPointerValid`, and `firstRawSpeciesId`
- whether the runtime source matches the logged/written `TrainerData` source

Do not document ROM paths, output paths, hashes, full logs, screenshots, saves, emulator states, secrets, tokens, or `.env` values.

## Safety

- Codex did not run a ROM.
- Codex did not create an output ROM.
- No private path, hash, full log, screenshot, save, emulator state, secret, token, or `.env` detail is documented.
- No UPR-FVX/CFRU/DPE code change is made in this workspace PR.
- No P1 promotion.
