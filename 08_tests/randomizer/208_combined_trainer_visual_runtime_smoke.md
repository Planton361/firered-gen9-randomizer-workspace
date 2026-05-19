# 208 Combined Trainer Visual Runtime Smoke

Status: sanitized local combined trainer visual runtime smoke. No ROM run by Codex. No P1 promotion.

## Scope

- Uses the current workspace UPR-FVX pin from PR #117: `5983011752273e00c402e25cc1ae1a9baca110f1`.
- Exercises a combined visual runtime path covering Intro Mon, Starter/Rival counter behavior, Rival sprite consistency, Trainer Class Sprite Sync and early trainer visuals.
- This is a targeted runtime smoke, not a full playthrough, global trainer sweep, all-starter-choice matrix or P1 promotion.

## Sanitized Evidence

Available sanitized local evidence:

- Combined trainer visual runtime smoke passed with caveats.
- Intro Mon was visibly randomized.
- Player starter was Charmander.
- Oak-Lab Rival starter was Squirtle.
- Route 22 Rival starter was Squirtle.
- Route 22 Rival non-starter Pokemon observed: Silvally Lv9.
- Interpretation: Rival Carries Starter Through Game protects/corrects the Rival starter slot only; non-starter Rival Pokemon remain eligible for Foe Pokemon randomization.
- Route 22 Rival sprite was randomized and consistent with the Oak-Lab Rival sprite.
- Viridian Forest trainer sprites were randomized.
- No crash, freeze or garbled sprite was observed.

## Status Impact

- Combined trainer visual runtime smoke: `PASS_WITH_CAVEATS`.
- Intro Mon visual: local pass.
- Rival Oak-Lab counter-starter: local pass.
- Rival Route 22 starter carry: local pass.
- Rival Route 22 sprite consistency: local pass.
- Viridian Forest class/sprite sync: local pass.
- No crash/freeze/garbled sprite observed.
- No P1 promotion.

## Follow-Up Scope

Future local-only evidence can strengthen confidence by sampling:

- additional Rival appearances beyond Route 22.
- additional player-starter choices.
- more regular trainer maps/classes with Trainer Class Sprite Sync enabled.
- longer combined visual runtime play.

Keep ROM paths, output paths, hashes, full logs, screenshots, saves, emulator states, secrets, tokens and `.env` content out of reports.
