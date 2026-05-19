# 207 Rival Counter Starter and Combined Visual Smoke

Status: sanitized workspace sync for merged UPR-FVX PR #117. No ROM run by Codex. No P1 promotion.

## Pin

- UPR-FVX PR #117 is merged.
- Workspace submodule `02_external/upr-fvx` is pinned to merge commit `5983011752273e00c402e25cc1ae1a9baca110f1`.
- Branch: `randomizer/sync-rival-counter-starter-and-visual-smoke`.

## Implemented Scope

- Rival Carries Starter Through Game protects/corrects the Rival starter after Foe Pokemon randomization.
- For vanilla starter slots, the Rival keeps the vanilla counter-starter.
- For randomized starter slots, the Rival uses the randomized counter-starter from the matching starter-slot mapping.
- Known FRLG Rival runtime-source rows keep Rival tags so runtime-source Rival rows participate in the carry/correction path.
- The Intro Mon randomizer rejects invalid species `0` and uses internal species identity for extended CFRU/DPE BPRE pools.

## Sanitized Evidence

Available sanitized local evidence:

- Combined visual Rival test passed after PR #117.
- Intro Mon was visibly Blissey; the Species `0` regression was gone.
- Rival counter-starter path was correct for the sampled route: Player Charmander -> Rival Squirtle.
- Trainer Class Sprite Sync remained visually okay from prior checks:
  - Viridian Forest trainers received per-trainer randomized classes/sprites.
  - Rival kept a consistent sprite/class across appearances.
- No crash, freeze or garbled sprite was reported in the targeted local smoke.

This confirms targeted combined visual smoke for the sampled Intro Mon, Rival counter-starter and Trainer Class Sprite Sync interactions. It is not a full playthrough, global runtime-source proof, broad trainer-category sweep or P1 promotion.

## Follow-Up Scope

Future local-only evidence can strengthen confidence by sampling:

- additional player-starter choices across all Rival appearances
- randomized-starter slot mappings beyond the sampled Charmander -> Squirtle counter path
- more Intro Mon randomized species after the Species `0` guard
- longer combined visual profile play with Trainer Class Sprite Sync enabled
- keep ROM paths, output paths, hashes, full logs, screenshots, saves, emulator states, secrets, tokens and `.env` content out of reports
