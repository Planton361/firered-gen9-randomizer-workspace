# CFRU Smart Trainer AI activation smoke plan

Stand: 2026-05-24

## Scope

This is a documentation-only activation and smoke-test plan for CFRU `FLAG_SMART_TRAINER_AI`.

No ROMs, output ROMs, saves, emulator states, builds, full logs, screenshots, tool binaries, private paths, secrets, tokens or `.env` data are part of this plan or should be committed as evidence.

Source baseline:

- `02_external/CFRU-expansion/src/config.h` defines `FLAG_SMART_TRAINER_AI 0xA0E`.
- `02_external/CFRU-expansion/src/Battle_AI/ai_master.c` / `GetAIFlags` ORs trainer battle flags with `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE` when `FlagGet(FLAG_SMART_TRAINER_AI)` is true.
- `02_external/CFRU-expansion/assembly/overworld_scripts/Pallet_town.s` / `EventScript_Pallet_FatGuy` sets `0xA0E` as a local smoke activation path for `FLAG_SMART_TRAINER_AI` and shows `Smart Trainer AI enabled.`.
- `VAR_GAME_DIFFICULTY` stays independent. Normal difficulty is `OPTIONS_NORMAL_DIFFICULTY = 0`.
- There is no final UI, settings NPC, option-menu or randomizer-profile wiring for this flag yet.

## Implemented Smoke Activation

The current minimal activation path is the existing Pallet Town test script:

- Script: `EventScript_Pallet_FatGuy`
- Source: `02_external/CFRU-expansion/assembly/overworld_scripts/Pallet_town.s`
- Activation line: `setflag 0xA0E @ FLAG_SMART_TRAINER_AI local smoke activation.`
- Visible confirmation: `Smart Trainer AI enabled.`

This was chosen because the script is already a debug/test-style path: it is wired to the Pallet test NPC entries in `eventscripts`, grants test Pokemon, calls setup specials and shows `gText_TestScript`. It is not a final player-facing Smart AI UX.

For local A/B smoke:

- Flag off: use Normal Difficulty and do not trigger `EventScript_Pallet_FatGuy` before the sampled trainer battle.
- Flag on: use Normal Difficulty, trigger `EventScript_Pallet_FatGuy` once, confirm the `Smart Trainer AI enabled.` message, then run the same sampled trainer battle route.

Do not interpret this test script as the final activation design. It is only a source-backed local smoke path for verifying the already implemented `GetAIFlags` hook.

## Activation Options

| Option | How it would activate the flag | Pros | Cons / risk | Fit for next step |
| --- | --- | --- | --- | --- |
| Early script sets flag automatically | Add a project-local startup/new-game/map-entry script step that sets `FLAG_SMART_TRAINER_AI` once for the test profile. | Smallest runtime behavior; no player UI; good for one focused smoke profile. | Requires a script-source change later; must avoid accidentally making the test profile look like default behavior if undocumented. | Best next implementation step for local smoke. |
| Temporary debug/test setter | Add a temporary debug-only script, key path, or test hook that can set/clear `FLAG_SMART_TRAINER_AI`. | Easy A/B testing in one save if implemented carefully; can test flag off/on without rebuilding separate profiles. | Must not ship as production UI; any temporary hook needs strong cleanup discipline. | Good for developer-only local testing, but not the cleanest persistent project path. |
| Settings NPC | Add an NPC that toggles Smart Trainer AI and explains it separately from Difficulty. | Clear player-facing semantics; can be available in a controlled place. | Requires map/script/text work; UI copy must not imply it changes `VAR_GAME_DIFFICULTY`; needs persistence and reset behavior decisions. | Good after smoke proves behavior. |
| Option Menu | Add Smart Trainer AI to the existing settings menu near Game Difficulty. | Discoverable and persistent; matches existing option-menu pattern. | More invasive UI/code/text change; easy to confuse with `VAR_GAME_DIFFICULTY`; needs menu count/layout handling and save display tests. | Not minimal for v1 smoke. |
| Randomizer-profile wiring | Have a randomizer profile or generated patch/script set the flag for an Ironmon/Smart-AI profile. | Best long-term fit for reproducible Randomizer/Ironmon profiles. | Requires deciding where UPR-FVX or workspace tooling should express CFRU runtime flags; must not require ROM/build artifacts in repo. | Good long-term follow-up after CFRU-side smoke. |

## Recommended Smallest Next Step

Use the Pallet Town test script activation for the first local smoke profile.

Rationale:

- It exercises the actual production flag path in `GetAIFlags`.
- It avoids adding permanent player-facing UI before behavior is proven.
- It keeps Smart Trainer AI separate from `VAR_GAME_DIFFICULTY`.
- It is simpler than option-menu layout work and safer than presenting an unproven setting to players.
- It reuses an existing test-script path instead of adding a Settings NPC, Option Menu entry or randomizer-profile writer.

For A/B testing, use two local builds/profiles or one debug-only local setter outside committed evidence:

- Baseline: Normal Difficulty, `FLAG_SMART_TRAINER_AI` clear.
- Test: Normal Difficulty, `FLAG_SMART_TRAINER_AI` set through `EventScript_Pallet_FatGuy` before the sampled trainer battles.

Do not commit the built ROMs, saves, output logs, screenshots, emulator state, or private paths used for the smoke.

## Smoke Matrix

| Case | Runtime difficulty | Smart Trainer AI flag | Expected AI | Must remain unchanged |
| --- | --- | --- | --- | --- |
| A: Baseline | Normal / `OPTIONS_NORMAL_DIFFICULTY` | Off / clear | Trainer AI uses existing trainer `aiFlags` only. | Trainer stats, levels, moves, PP, bag access, player move access, wild/raid behavior and battle rules match current Normal behavior. |
| B: Smart Trainer AI | Normal / `OPTIONS_NORMAL_DIFFICULTY` | On / set | Trainer battles get `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE` added to their trainer AI flags. | Same non-AI behavior as Case A. |

## Battle Behavior Checks

Use one or more early, repeatable trainer battles where the trainer has multiple plausible moves and where a bad move can be distinguished from a stronger move choice.

For each sampled trainer:

1. Record sanitized setup only: trainer label/route category, difficulty Normal, flag state off/on, and a verbal move-choice observation.
2. Run Case A with flag off.
3. Run Case B with flag on under the same randomizer/profile conditions as far as practical.
4. Check whether the flag-on case avoids clearly bad moves or chooses more threatening moves more often.
5. Do not overclaim from one battle. Treat this as targeted smoke, not a statistical AI evaluation.

Acceptable evidence format:

- `PASS`: flag-on trainer behavior visibly differs in the expected direction, and no non-AI side effects are observed.
- `PASS_WITH_CAVEATS`: AI appears smarter in sampled battles, but sample size is small or move-choice randomness limits certainty.
- `FAIL`: flag-on case shows no plausible AI improvement, breaks trainer battle behavior, or changes non-AI systems.
- `BLOCKED`: cannot activate the flag or cannot observe comparable trainer behavior without extra tooling.

## Non-AI Regression Checks

The smoke should explicitly compare flag off vs. flag on and confirm:

- `VAR_GAME_DIFFICULTY` remains Normal.
- Trainer IVs do not change because of the flag.
- Trainer EV behavior does not change because of the flag.
- Trainer friendship does not change because of the flag.
- Trainer move PP bonuses do not change because of the flag.
- Trainer levels and level scaling do not change because of the flag.
- Trainer species, held items and movesets do not change because of the flag.
- Player bag access does not change because of the flag.
- Player move restrictions do not change because of the flag.
- Battle rules such as Sleep Clause, Fog behavior and Bad Thoughts damage do not change because of the flag.
- Wild AI and wild encounter construction do not change because of the flag.
- Raid AI, raid shields and raid repeated-move behavior do not change because of the flag.
- Expert anti-cheese and difficulty-gated switch prediction are not enabled merely by the flag.

## Source Checks Before Smoke

Before running a local smoke, confirm source state only:

```sh
rg "FLAG_SMART_TRAINER_AI|VAR_GAME_DIFFICULTY|ShouldGiveTrainerMonBestStatsMaxEVs|ShouldGiveTrainerMonMaxFriendship|GetTrainerMonMovePPBonus|ShouldDoAIShiftSwitch|IsPlayerTryingToCheeseAI|TryChangeMoveTargetToCounterPlayerProtectCheese|WildMonIsSmart" 02_external/CFRU-expansion/src 02_external/CFRU-expansion/include
```

Expected interpretation:

- `FLAG_SMART_TRAINER_AI` should be limited to `config.h` and the trainer branch in `GetAIFlags`.
- Existing difficulty, trainer-build, wild/raid and anti-cheese paths may still exist, but they should not read `FLAG_SMART_TRAINER_AI`.

## Evidence Hygiene

Commit only sanitized conclusions or this plan.

Do not commit:

- ROMs or output ROMs
- saves or save states
- emulator states
- builds or build artifacts
- full randomizer logs
- screenshots
- private paths
- hashes tied to private ROMs
- tool binaries
- secrets, tokens or `.env` files

## Open Follow-ups

- Run the first local A/B smoke through `EventScript_Pallet_FatGuy` and document only sanitized pass/fail observations.
- Decide whether a later set/clear helper is needed for faster repeated A/B testing.
- After smoke, decide whether the user-facing activation should be Settings NPC, Option Menu, or randomizer-profile wiring.
- If adding UI later, keep wording separate from CFRU Game Difficulty and avoid describing `VAR_GAME_DIFFICULTY` as Smart AI.
- If randomizer-profile wiring is chosen, define how UPR-FVX/workspace tooling records CFRU runtime flags without committing ROM artifacts.
