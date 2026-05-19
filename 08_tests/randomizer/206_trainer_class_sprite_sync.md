# 206 Trainer Class Sprite Sync

Status: sanitized workspace sync for merged UPR-FVX PR #111. No ROM run by Codex. No P1 promotion.

## Pin

- UPR-FVX PR #111 is merged.
- Workspace submodule `02_external/upr-fvx` is pinned to merge commit `4805a5a930bc97203199816222465c76de2f2150`.
- Branch: `randomizer/sync-trainer-class-sprite-sync`.

## Implemented Semantics

- `Randomize Trainer Names` remains separate and changes only trainer personal names.
- Without `MODE-TRAINER-CLASS-SPRITE-SYNC`, `Randomize Trainer Class Names` remains legacy textlabel-only behavior.
- With `MODE-TRAINER-CLASS-SPRITE-SYNC`, Trainer Class Sprite Sync follows the Trainer Class Names mapping:
  - `TrainerNameRandomizer` records `oldClassId -> targetClassId`.
  - `TrainerClassSpriteSyncRandomizer` sets `trainerClass` and `trainerPic` to match the target class.
  - The goal is class label / class ID / visible pic consistency.
- Special target classes such as Rival, Gym Leader, Elite Four and Champion are not globally excluded.
- Target classes without an observed valid `trainerPic` are skipped.

## Sanitized Evidence So Far

Available sanitized pre-merge evidence:

- a regular trainer battle started
- the visible trainer sprite changed
- the randomizer log showed class/sprite sync markers
- an earlier semantic mismatch was corrected before merge: the feature is not Regular-only target remapping, but class-label/class-ID/pic synchronization

This evidence is not final merged-pin proof. A fresh local smoke is still required on commit `4805a5a930bc97203199816222465c76de2f2150`.

## Follow-Up Smoke

Local-only evidence needed after the merged pin:

- confirm `MODE-TRAINER-CLASS-SPRITE-SYNC` is enabled together with Trainer Class Names
- verify the log marker old/new class and old/new pic values
- verify the visible trainer sprite matches the displayed target class in words
- include at least one normal trainer and one special target class if available
- keep ROM paths, output paths, hashes, full logs, screenshots, saves, emulator states, secrets, tokens and `.env` content out of reports
