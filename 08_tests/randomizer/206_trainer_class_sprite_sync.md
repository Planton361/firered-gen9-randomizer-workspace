# 206 Trainer Class Sprite Sync

Status: sanitized workspace sync for final merged UPR-FVX PR #116 Trainer Class Sprite Sync state. No ROM run by Codex. No P1 promotion.

## Pin

- UPR-FVX PR #116 is merged.
- Workspace submodule `02_external/upr-fvx` is pinned to merge commit `36dd431d059bc69eb1bee3311200e28c872c6cc9`.
- Branch: `randomizer/sync-trainer-class-sprite-sync-final`.

## Implemented Semantics

- `Randomize Trainer Names` remains separate and changes only trainer personal names.
- Without `MODE-TRAINER-CLASS-SPRITE-SYNC`, `Randomize Trainer Class Names` remains legacy textlabel-only behavior.
- With `MODE-TRAINER-CLASS-SPRITE-SYNC`, Trainer Class Sprite Sync follows the Trainer Class Names assignment:
  - regular trainers receive per-trainer target class assignments.
  - Rival/Friend rows share one grouped target class/pic across appearances.
  - `TrainerClassSpriteSyncRandomizer` sets `trainerClass` and `trainerPic` to match the target class.
  - the goal is class label / class ID / visible pic consistency.
- Special target classes such as Rival, Gym Leader, Elite Four and Champion are not globally excluded.
- Target classes without an observed valid `trainerPic` are skipped.
- Runtime-source rows are included where they are eligible and present in the synced TrainerData path.

## Sanitized Evidence

Available sanitized local evidence:

- Viridian Forest Bug Catcher class rows were randomized per trainer instead of as one old-class group.
- Rival/Friend rows kept the first randomized class/sprite identity across later appearances after PR #116.
- Other sampled trainers appeared to keep class label, `trainerClass` and visible `trainerPic` aligned.
- No garbled sprite or crash was reported in the targeted local smoke.
- Earlier semantic mismatches were corrected before this final pin:
  - Sprite Sync is not a Regular-only stable mode.
  - Regular trainers may become special-looking classes in chaos mode.
  - Sprite Sync follows the class assignment instead of choosing an independent sprite.
  - Rival/Friend rows are grouped while regular trainers remain per-trainer randomized.

This confirms the targeted visual smoke path for `MODE-TRAINER-CLASS-SPRITE-SYNC`, but it is not a full playthrough, broad route sweep or global visual-source proof.

## Follow-Up Scope

Future local-only evidence can strengthen confidence by sampling more battle categories:

- additional regular trainer classes across more maps
- additional Rival/Friend appearances
- eligible runtime-source trainers beyond the already sampled path
- longer playthrough sampling for garbled sprites, wrong labels or crashes
- keep ROM paths, output paths, hashes, full logs, screenshots, saves, emulator states, secrets, tokens and `.env` content out of reports
