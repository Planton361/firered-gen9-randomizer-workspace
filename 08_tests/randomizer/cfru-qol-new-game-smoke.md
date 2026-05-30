# CFRU QoL New Game Smoke Plan

Status: documentation-only smoke-test hardening plan for branch `test/cfru-qol-new-game-smoke`.

No CFRU, DPE, UPR-FVX, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash value, private path, token, secret or `.env` data is included.

## Scope

This plan hardens the existing CFRU QoL / New Game behavior that was inventoried in `01_docs/analysis/ironmon-qol-feature-inventory.md`.

It does not implement a new QoL feature. It defines sanitized manual smoke coverage for:

- New Game Start.
- Intro controls guide skip / faster-intro-adjacent behavior.
- Oak Tutorial / Teachy-TV / controls-guide presence or absence.
- Runtime Options / Config Flags.
- Randomizer compatibility without Field Item, item ball, hidden sparkle or writer changes.

## Read-only source findings

| Area | Existing evidence found | Interpretation for this smoke |
|---|---|---|
| CFRU baseline config | `02_external/CFRU-expansion/src/config.h` has `SKIP_INTRO_CONTROLS_GUIDE` defined, `TUTORIAL_BATTLES` commented, `OLD_EXP_SPLIT` and `FLAT_EXP_FORMULA` defined, `POISON_1_HP_SURVIVAL` commented, `SWSH_CATCHING_DIFFICULTY_MODIFIER` commented, `IgnoreWildPokemon` defined, and runtime flags/vars for Nuzlocke, Wild Prebattle, difficulty, trainer scaling, trainer AI and hard cap. | The smoke should verify behavior, not re-argue config ownership. Compile-time rows require a rebuilt local candidate outside committed evidence. |
| Intro controls guide | `02_external/CFRU-expansion/bytereplacement` has a guarded `SKIP_INTRO_CONTROLS_GUIDE` block. `01_docs/cfru_dpe_config_runtime_settings_review.md` also treats this as a partial faster-intro source, not a full intro skip. | Pass criterion is only "controls guide skipped"; do not claim full faster intro. |
| Oak tutorial battle | `02_external/CFRU-expansion/src/overworld.c` gates `TRAINER_BATTLE_OAK_TUTORIAL` through `TUTORIAL_BATTLES`. The current config comments out that macro. | Smoke should prove no Oak tutorial battle and no softlock around early-game script flow. |
| Poison overworld faint | `02_external/CFRU-expansion/src/overworld.c` calls the poison script when `POISON_1_HP_SURVIVAL` is not defined. | Smoke should exercise one sanitized poison-step faint path if a local candidate is available. |
| EXP profile | `02_external/CFRU-expansion/src/exp.c` uses `OLD_EXP_SPLIT` for participant split behavior and `FLAT_EXP_FORMULA` for the flat formula path. Prior docs note exact Gen 3 EXP is broader than these two macros. | Smoke can verify old/flat profile symptoms, but must not claim exact FireRed EXP semantics. |
| Runtime options | `02_external/CFRU-expansion/src/option_menu.c` initializes Page 3 options from vars/flags and applies dirty rows for Level Scaling, Trainer AI, Hard Cap, Nuzlocke and Wild Prebattle. `08_tests/randomizer/cfru-settings-split-final-smoke.md` and `cfru-randomizer-baseline-config.md` already have targeted menu evidence. | This smoke should protect ownership boundaries: menu close without dirty row preserves raw state; explicit choices only affect owning vars/flags. |
| Wild Prebattle | `02_external/CFRU-expansion/src/wild_encounter.c` generates the prebattle screen only when `FLAG_ENABLE_WILD_PMN_PREBATTLE_SCREEN` is set. | Smoke should verify encounter flow changes without changing encounter tables or randomizer output. |
| Teachy-TV / Controls Guide | Source search found Teachy-TV item/table references, but no source-backed task requirement to alter Teachy-TV. The controls-guide skip is separate and compile-time. | Teachy-TV should remain unchanged unless a later source-backed feature asks for it. |
| Field Items / Randomizer | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/RomHandler.java` documents required field TMs and TM-vs-non-TM slot preservation. Existing field-item smokes cover UPR-FVX output behavior separately. | This branch should only assert that New Game QoL smoke does not touch Field Items, item balls, shops, pickup, gifts, static items or randomizer writers. |

## Smoke matrix

| Test | Preconditions | Manual steps | Expected behavior | Pass criteria | Fail criteria | Known risk |
|---|---|---|---|---|---|---|
| New Game Start reaches player control | Local candidate built from the current CFRU baseline profile. Fresh local state. | Start New Game; proceed through title/new-game intro using normal inputs; stop after the player gains overworld control. | Intro proceeds without freeze, crash, garbled UI or missing required player/object state. | Player reaches controllable overworld state and can open the menu. | Freeze, softlock, missing player object, corrupt intro graphics, or no control after intro. | Intro byte replacement and Oak intro species/visual hooks are small but early-flow sensitive. |
| Intro Controls Guide skipped | Same candidate as above. | During New Game intro, watch for the FireRed controls-guide/help-flow segment. | Controls guide does not interrupt the intro. | No controls-guide prompt/flow appears, and intro continues to player setup/control. | Controls guide appears, or skip causes broken text/script state. | This proves only `SKIP_INTRO_CONTROLS_GUIDE`, not a full faster intro. |
| Oak Tutorial battle absent | Candidate with `TUTORIAL_BATTLES` disabled. | Progress through the earliest Oak/tutorial path normally enough to reach the first relevant overworld route/lab flow. | Oak tutorial battle does not start. Script flow continues normally. | No Oak tutorial battle occurs; no trainer-battle script softlock; early game remains playable. | Oak tutorial battle starts unexpectedly, or a skipped tutorial leaves blocked movement/dialogue. | Tutorial battle mode fallback also supports dynamic trainer battle behavior; watch for script-state regressions. |
| Teachy-TV unchanged | Any candidate from this branch. | Confirm no new Teachy-TV behavior is claimed or required by this smoke. If encountered naturally, do not treat it as a QoL pass/fail unless it blocks flow. | Teachy-TV remains ordinary item/table behavior. | No documentation or gameplay claim says Teachy-TV was changed. | Smoke result claims Teachy-TV skip/removal without a source-backed change. | Teachy-TV is easy to conflate with controls/tutorial QoL; keep it out of scope. |
| Runtime menu Page 3 layout | Candidate with existing settings split/baseline config. | Open Options; navigate to Page 3; inspect row names and selectable values. | Page 3 contains the expected runtime rows and remains navigable. | `Level Scaling`, `Trainer AI`, `Hard Cap`, `Nuzlocke`, `Wild Prebattle`, and `Cancel` are visible and usable if included by the current source. | Missing rows, broken navigation, clipped unusable values, or save/close failure. | Page capacity and dirty-row save logic can regress if rows are reordered later. |
| Runtime menu close preserves unchanged rows | Candidate with known local default state. | Open Options; visit Page 3; do not change Nuzlocke/Wild Prebattle/Hard Cap; close Options. Reopen and inspect state. | Opening/closing does not change non-dirty option rows. | Previously observed values remain unchanged after close/reopen. | Any untouched option flips state. | Dirty flags protect Level Scaling/Trainer AI/Hard Cap; Nuzlocke/Wild Prebattle apply only when dirty. |
| Nuzlocke toggle ownership | Candidate with Page 3 Nuzlocke row. | Toggle `Nuzlocke` Off then On, using one save/close/reopen cycle for each direction. | The row controls only `FLAG_NUZLOCKE` semantics. | Off disables Nuzlocke-gated behavior for future checks; On enables it; no unrelated settings are visibly changed. | Toggle affects Wild Prebattle, difficulty, trainer scaling, hard cap, field items or randomizer behavior. | Turning Off does not unwind already-created Nuzlocke side state; test from clean local state when possible. |
| Wild Prebattle toggle ownership | Candidate with Page 3 Wild Prebattle row. | Set Wild Prebattle Off; trigger one ordinary land encounter. Set On; trigger one ordinary land encounter. | Off uses normal encounter flow. On shows the prebattle/Ignore-Engage flow. | Encounter species/table still comes from normal local randomizer/game data; only presentation flow changes. | Toggle changes field item output, encounter tables, or leaves transient prebattle UI flags stuck. | The prebattle feature is compile-gated by `IgnoreWildPokemon`; only the enable flag is menu-owned. |
| Old / flat EXP symptom smoke | Candidate with stable small battle route. | Use a controlled battle with at least one participating party member; if practical, compare with a non-participant/Exp Share state that is easy to observe. | EXP behavior matches the current old-split/flat-profile expectation well enough for a targeted smoke. | No crash; battle completes; observed EXP distribution is consistent with old participant split / flat formula expectations. | Battle crash, no EXP, scaled-level-looking anomaly that contradicts the configured profile, or impossible-to-interpret result. | This is not an exact Gen 3 EXP proof because other modern EXP macros may still be enabled. |
| Poison overworld faint | Candidate with a local controlled poison state. | Put a party Pokemon in poisoned, low-HP state locally; walk until poison step processing triggers. | Poison can faint in overworld when `POISON_1_HP_SURVIVAL` is absent. | Pokemon can faint from poison; poison script resolves without softlock. | Pokemon is held at 1 HP, or poison script softlocks/crashes. | Needs a safe local setup; do not commit saves, states, screenshots, paths or raw logs. |
| SwSh catch-level malus absent | Candidate with a safe local catch comparison setup. | Attempt a small controlled catch scenario where the wild Pokemon is higher level than the active Pokemon; keep notes qualitative unless a compact sanitized comparison is available. | No extra SwSh higher-level catch penalty is observed from the disabled macro. | Catch behavior does not show obvious higher-level malus symptoms and no crash occurs. | Clear higher-level catch malus behavior is observed despite disabled macro, or capture flow breaks. | Catch RNG makes this weaker than source evidence; keep result caveated. |
| Randomizer compatibility without Field Item changes | Randomized output candidate generated by existing UPR-FVX flow, with no new field-item settings changed for this branch. | Run one New Game / Options smoke on a randomized candidate whose Field Items mode is unchanged or already covered by existing field-item smokes. | New Game QoL behavior does not depend on Field Items, shops, pickup, item balls or randomizer writer output. | Smoke can be completed without touching or re-randomizing Field Items. Existing field-item smokes remain the owner for those claims. | This branch changes or claims changes to Field Items, item balls, hidden sparkle, shops, pickup, gifts, static/NPC items or randomizer writers. | Future visual QoL could accidentally depend on randomizer metadata; this branch must not. |

## Result recording template

Use one compact sanitized row per local run:

| Date | Candidate type | New Game | Controls Guide | Oak Tutorial | Runtime Options | EXP | Poison | Catch malus | Randomizer no-field-items | Result | Caveat |
|---|---|---|---|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | local CFRU baseline / randomized output | pass/fail/skip | pass/fail/skip | pass/fail/skip | pass/fail/skip | pass/fail/skip | pass/fail/skip | pass/fail/skip | pass/fail/skip | PASS_WITH_CAVEATS / FAIL / BLOCKED | sanitized note only |

Do not record ROM names, file paths, hashes, screenshots, raw emulator logs, save names, state names, build output paths, tool binary paths, local addresses, tokens, secrets or `.env` content.

## Pass / fail policy

Overall `PASS_WITH_CAVEATS` requires:

- New Game reaches player control.
- Controls guide skip and Oak tutorial absence behave as expected.
- Runtime option rows are usable and do not alter unrelated settings.
- No Field Item, item ball, shop, pickup, gift/static/NPC item, hidden sparkle or randomizer writer behavior is changed or claimed.

Overall `FAIL` if:

- New Game cannot reach player control.
- Intro/control/tutorial skip causes a softlock or corrupt state.
- Runtime options toggle unrelated systems.
- Any Field Item or randomizer writer behavior changes in this branch.

Overall `BLOCKED` if:

- No local candidate is available for gameplay smoke.
- The candidate is not built from the expected CFRU baseline.
- Evidence would require committing or documenting forbidden artifacts.

## Handoff

First small implementation block after this plan should stay smoke-first:

1. Run the New Game / Controls Guide / Oak Tutorial smoke on a fresh local candidate.
2. Run Page 3 runtime-option preservation and toggle ownership checks.
3. Record only sanitized results in this file or a follow-up smoke result file.
4. Implement code only if a smoke reveals a concrete regression.

Still out of scope:

- Hidden sparkle implementation.
- Field Item or itemball graphics changes.
- Randomizer writer changes.
- DPE data changes.
- UPR-FVX settings/profile changes.
- Binary patch ports.
