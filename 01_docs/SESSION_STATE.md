# Session update - CFRU TM/HM itemball visual design

- Branch: `design/cfru-tm-itemball-visuals` from clean current `main` after Workspace PR #462.
- Added a documentation-only, source-backed design for gold/yellow visible TM/HM Object Events while normal visible Field Items and invisible Hidden Items remain unchanged.
- Final design status: `DESIGN_READY_FOR_PILOT`.
- Vanilla inventory: 29 visible TM/HM balls, comprising 28 TM slots and the preserve-only HM07 ball. Standard visible `finditem` slots use the same lower graphics id `92`.
- Key compatibility contract: CFRU reconstructs a 16-bit Object Graphics id from lower/upper bytes, while UPR-FVX's Gen 3 Field Item scanner checks only object-template byte 1 against `ItemBallPic=92`. Proposed gold id `0x065C` selects free CFRU table 6 and retains low byte 92, so UPR-FVX continues to own and write the item value.
- UPR-FVX source and existing reload smokes confirm TM/non-TM slot typing is preserved by Shuffle, Random and Random Even; Ban Bad only changes the non-TM pool. HM07 is banned from normal pools and remains unchanged.
- The current CFRU overlay generator only appends. A future pilot may add a fail-closed `replace_graphics` operation which copies the existing object template and changes only the graphics-id upper byte.
- Pilot/control: MtMoon_1F bank 1/map 1, expected 14 objects; TM09 local id 9 at `(11, 35)` becomes gold, Potion local id 10 at `(26, 32)` remains the normal control.
- Graphics plan: regular 16x16 one-frame inanimate Object Graphics entry; reuse existing palette tag `0x1106` and its unused muted-gold ramp, with no new or dynamic palette.
- No CFRU, UPR-FVX or DPE code, graphics, palettes, submodule pins, ROMs, saves, states, screenshots, builds, generated artifacts, raw-address ports or binary patches were changed.

# Session update - CFRU hidden item sparkle pilot removed and blocked

- Failed Draft PRs were closed without merge: CFRU #32 and Workspace #461.
- CFRU Revert branch/commit/Draft PR: `revert/cfru-hidden-item-sparkle-pilot`, `acf1cf38a0acab1fd8a88be9b687e3b02faeb50b`, `https://github.com/Planton361/CFRU-expansion/pull/33`, targeting `compat/firered-gen9-randomizer`.
- The cumulative pilot inventory from pre-pilot `9c105d156e219e7a59069f47d5ee49f1fdcfb6dc` through Compat `325212e325023284bd6198a3a9cd75b60e0c21f8` was limited to 186 added lines in `src/overworld.c`. The Revert removes exactly those lines without resetting the branch or changing unrelated Compat history.
- Removed: Viridian pilot defines/data/coordinates, transition and resume calls, task/cooldown state, BG-event/visibility/readiness helpers, Sprite-slot discovery/ownership/marker code, manual stop/active-list cleanup, and all later simple-spawn pilot work.
- Sanitized failure record: the map-entry one-shot was not visible when the distant coordinates were reached; task/ownership variants lost the second item; stray Sparkles occurred; the rejected private graphics/palette path caused runtime palette corruption; and the source-faithful Cyan frame scan cannot be installed without a source-backed Overworld hook after `CameraUpdate`.
- `OverworldBasic` and `CB2_OverworldBasic` remain bound to Vanilla addresses in CFRU. Raw-address/byte replacement and a larger `OverworldBasic` port are not approved for this feature scope.
- Status: `BLOCKED_NEEDS_SOURCE_BACKED_OVERWORLD_FRAME_HOOK`. No Hidden-Item marker remains in the Revert candidate.
- CFRU checks passed: exact pre-pilot file comparison, pilot-name/coordinate searches, `git diff --check`, syntax-only compile of `src/overworld.c`, and `python3 scripts/build.py` including link with only the existing RWX warning.

# Session update - CFRU hidden item sparkle pilot

- Branch: `feature/cfru-hidden-item-sparkle-pilot`.
- PR #459 was merged into current `main` before this branch was created.
- CFRU branch: `feature/cfru-hidden-item-sparkle-pilot`.
- CFRU Draft PR: `https://github.com/Planton361/CFRU-expansion/pull/28`.
- Implemented a source-backed Viridian Forest hidden-item sparkle pilot for exactly two BG hidden items: Potion at `(3, 22)` / offset `0` and Antidote at `(28, 57)` / offset `1`.
- CFRU change is limited to `src/overworld.c`: `RunOnTransitionMapScript` now calls a Viridian-Forest-only helper that scans the current map's BG events and starts one-shot `FLDEFF_SPARKLE` only when the matching hidden-item flag is unset.
- The pilot does not use Itemfinder behavior, does not change hidden-item pickup, does not change the UPR-FVX Field Item writer, does not add visible item balls, and does not touch other maps.
- Updated `08_tests/randomizer/cfru-hidden-item-sparkle-qol.md` to `IMPLEMENTED_PILOT_PENDING_MANUAL_SMOKE`, including the clean-build command pair and the re-entry smoke matrix.
- Workspace submodule `02_external/CFRU-expansion` now points at the CFRU hidden-item sparkle pilot branch tip for review while the CFRU Draft PR remains unmerged.
- Checks run: CFRU `diff --check`, CFRU syntax-only compile for `src/overworld.c`, workspace `diff --check`.
- No DPE, UPR-FVX, Name Rater, Faster Intro, Bill-Sevii, visible itemball, Pickup, Itemfinder, Field Item randomizer writer, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, private path, token, secret or `.env` data was changed or documented.

# Session update - CFRU hidden item sparkle QoL design

- Branch: `design/cfru-hidden-item-sparkle-qol`.
- PR #458 was merged into current `main` before this branch was created.
- Added `01_docs/analysis/cfru-hidden-item-sparkle-qol.md` as a source-backed, documentation-only design for visible hidden-item sparkle cues without Itemfinder behavior.
- Added `08_tests/randomizer/cfru-hidden-item-sparkle-qol.md` as the future Viridian Forest pilot smoke handoff.
- Faster-FireRed boundary: public evidence documents visually marked hidden items and a no-hidden-item-marks patch variant, but no portable source implementation was used. No IPS/BPS/UPS, binary patch data or raw address port is accepted.
- CFRU finding: hidden items are represented through BG-event data with item/id/quantity/underfoot state and hidden-item flags; pickup already calls item-sprite presentation and `SetHiddenItemFlag`; CFRU also exposes `FLDEFF_SPARKLE`, CFRU-added `FLDEFF_REPEATING_SPARKLES`, and a map-transition source path that could scan current `gMapHeader.events->bgEvents`.
- pret finding: vanilla FireRed generates hidden items from `map.json` `hidden_item` BG events, checks the hidden-item flag before pickup, and uses Itemfinder-only scanning for nearby/underfoot response behavior. Itemfinder behavior remains out of scope.
- Decision: `implementable-medium`. A one-shot map-load `FLDEFF_SPARKLE` cue is the recommended small MVP; permanent repeating sparkles need owned cleanup infrastructure; object-event markers are fallback only.
- Pilot map: Viridian Forest, map bank `1`, map number `0`, hidden Potion at `(3, 22)` with `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_POTION` / offset `0`, hidden Antidote at `(28, 57)` with `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_ANTIDOTE` / offset `1`.
- No CFRU, DPE, UPR-FVX, Hidden Item implementation, Itemfinder feature, Field Item randomizer writer, itemball graphics, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, private path, token, secret or `.env` data was changed or documented.

# Session update - CFRU complete Name Rater rollout smoke pass

- Branch: `test/cfru-name-rater-complete-rollout-smoke`.
- CFRU PR #27 and Workspace PR #457 were present in current `main` before creating this branch.
- Updated `08_tests/randomizer/cfru-name-rater-centers-rollout.md` with the sanitized user-reported final manual smoke result for the complete Pokecenter Name Rater rollout.
- User finding: all core behavior works.
- Status promoted to `COMPLETE_ROLLOUT_PASS_WITH_CAVEATS`.
- Caveats remain explicit: manual smoke only, no automated test, no full playthrough, Egg rejection path not run, traded/non-player-OT rejection path not run, and no BizHawk/Ironmon Tracker/P1 support claim.
- No CFRU, DPE, UPR-FVX, Hidden Item, itemball graphics, Field Item, Randomizer writer, ROM, save, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - CFRU complete Name Rater Pokecenter rollout

- Branch: `feature/cfru-name-rater-centers-rollout-complete`.
- PR #456 was fast-forwarded into current `main` before creating this branch.
- CFRU branch: `feature/cfru-name-rater-centers-rollout-complete`.
- CFRU Draft PR: `https://github.com/Planton361/CFRU-expansion/pull/27`.
- CFRU change is limited to `mapobjectoverlays`: 12 remaining Pokecenter 1F append rows were added for Cerulean, Cinnabar, Pewter, Vermilion, Indigo Plateau, Two Island, Three Island, Four Island, Five Island, Six Island, Seven Island and One Island.
- Existing Viridian and safe-Kanto batch rows are unchanged. No rollout-table Pokecenter 1F maps were skipped.
- Each new row uses the design-provided fail-closed expected object count, local id, coordinate `(10, 5)`, `MAP_OBJ_GFX_GENTLEMAN`, elevation `3`, `MOVEMENT_TYPE_FACE_DOWN`, and `EventScript_PokeCenterNameRater`.
- Updated `08_tests/randomizer/cfru-name-rater-centers-rollout.md` to `COMPLETE_ROLLOUT_PENDING_MANUAL_SMOKE`, with One Island called out as the highest-risk smoke target because of Bill/Celio/Network Machine and coord/BG-event preservation.
- Workspace submodule `02_external/CFRU-expansion` now points at the CFRU complete-rollout feature commit for review while the CFRU Draft PR remains unmerged.
- No CFRU script/Python/ASM, DPE, UPR-FVX, Hidden Item, itemball graphics, Field Item, Randomizer writer, ROM, save, build artifact, tool binary, screenshot, raw log, private path, token, secret or `.env` data was changed or documented.

# Session update - CFRU safe Kanto Name Rater Pokecenter rollout batch

- Branch: `feature/cfru-name-rater-centers-rollout-kanto-1`.
- PR #455 was fast-forwarded into current `main` before creating this branch.
- CFRU branch: `feature/cfru-name-rater-centers-rollout-kanto-1`.
- CFRU Draft PR: `https://github.com/Planton361/CFRU-expansion/pull/26`.
- CFRU change is limited to `mapobjectoverlays`: six safe-Kanto-first append rows were added for Celadon, Fuchsia, Lavender, Route 10, Route 4 and Saffron Pokecenter 1F.
- Existing Viridian overlay row is unchanged. No high-count Kanto maps, Indigo Plateau, Sevii centers or One Island were added.
- Each new row uses the design-provided fail-closed expected object count, local id, coordinate `(10, 5)`, `MAP_OBJ_GFX_GENTLEMAN`, elevation `3`, `MOVEMENT_TYPE_FACE_DOWN`, and `EventScript_PokeCenterNameRater`.
- Updated `08_tests/randomizer/cfru-name-rater-centers-rollout.md` with the implementation candidate and pending manual smoke matrix.
- Workspace submodule `02_external/CFRU-expansion` now points at the CFRU safe-Kanto feature commit for review while the CFRU Draft PR remains unmerged.
- No CFRU script/Python/ASM, DPE, UPR-FVX, Hidden Item, itemball graphics, Field Item, Randomizer writer, ROM, save, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - CFRU Name Rater Pokecenter rollout design

- Branch: `design/cfru-name-rater-centers-rollout`.
- PR #454 was fast-forwarded into current `main` before creating this branch.
- Added `01_docs/analysis/cfru-name-rater-centers-rollout.md` as a design-only rollout inventory for added Name Rater NPCs in Pokecenter 1F maps.
- Added `08_tests/randomizer/cfru-name-rater-centers-rollout.md` as the clean-build and map-by-map smoke handoff for future rollout work.
- Read-only source inventory covered CFRU map constants and pret `*PokemonCenter_1F/map.json` files. It identified 19 target Pokecenter 1F maps, with per-map bank, map number, object count, new row/local id, candidate coordinate, event risk and smoke focus.
- Viridian remains the only implemented/passed MVP pattern: status `MVP_PASS_WITH_CAVEATS`, clean build required, and map entry from outside required.
- Recommended rollout order is staged: safe Kanto maps first, high-count Kanto and Indigo Plateau separately, Sevii maps later, and One Island last because of Bill/Celio/Network Machine plus coord/BG-event preservation risk.
- No CFRU, DPE, UPR-FVX, rollout code, additional Pokecenter implementation, Hidden Item, itemball graphics, Field Item, Randomizer writer, ROM, save, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - CFRU Viridian Name Rater overlay smoke pass

- Branch: `test/cfru-map-object-overlay-viridian-smoke`.
- PR #453 was verified as merged into current `main` before creating this branch.
- Updated `08_tests/randomizer/cfru-name-rater-centers-qol.md` with the sanitized successful manual Viridian Pokecenter Name Rater overlay smoke.
- User-reported result: a local Mac CFRU clean-build using `python3 scripts/clean.py BUILD` followed by `python3 scripts/make.py` made the added Name Rater visible; Viridian Pokecenter was entered fresh from outside the map.
- Smoke rows reported pass: Viridian Pokecenter loads, added Name Rater visible, Nurse works, PC works, existing NPCs remain present/interactable, Name Rater No path works, nickname screen opens, cancel works, confirm/rename works, and no visible Runtime Options / Field Item / randomizer-output side effect was observed.
- Not run: Egg rejection path, traded/non-player-OT rejection path, broader Pokecenter rollout.
- Status promoted to `MVP_PASS_WITH_CAVEATS` for the Viridian-only overlay MVP. No CFRU, DPE, UPR-FVX, additional Pokecenter, rollout, Hidden Item, itemball graphics, Field Item, Randomizer writer, ROM, save, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - CFRU Name Rater overlay smoke fail debug

- Branch: `debug/cfru-name-rater-overlay-smoke-fail`.
- Workspace `main` was fast-forwarded to PR #452 before creating this branch.
- CFRU local branch: `compat/firered-gen9-randomizer`.
- CFRU commit: `f40a35a295ce23294557f19dfff220240056386f`.
- User-reported smoke fail: after a local CFRU build/start, no visible or interactable Viridian Pokecenter Name Rater was found.
- Read-only source diagnosis found that `scripts/make.py` calls `scripts/insert.py`, `InsertMapObjectOverlays(...)` is actually invoked, the Viridian map bank/map number and expected object count remain source-backed, the appended row/local id and object-template fields are plausible, and the Name Rater script/text are under the recursive build globs.
- No small source-backed CFRU code defect was identified. No CFRU source, UPR-FVX, DPE, ROM, save, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data was changed or documented.
- Updated `08_tests/randomizer/cfru-name-rater-centers-qol.md` with a smoke-fail debug handoff. The next gate is a clean rebuild from the CFRU root and a fresh map-entry smoke; if still absent, the next debug block should verify the inserted `MapHeader.events` pointer and generated object count through a sanitized local inspection path.

# Session update - CFRU Viridian Pokecenter map object overlay MVP

- Branch: `feature/cfru-map-object-overlay-generator`.
- PR #449 was verified as merged into current `main` before creating this branch.
- CFRU feature branch: `feature/cfru-map-object-overlay-generator`.
- CFRU feature commit: `648ce6042a93b71796c2d478fc816687e2ec060a`.
- CFRU compat merge: PR #25 into `compat/firered-gen9-randomizer`, merge commit `f40a35a295ce23294557f19dfff220240056386f`.
- Workspace submodule pin now points at CFRU compat merge commit `f40a35a295ce23294557f19dfff220240056386f`.
- Workspace PRs for this branch were merged as #450 and #451; #451 is the final main-facing pin cleanup.
- Implemented a minimal CFRU-owned `mapobjectoverlays` insertion surface for exactly one map: Viridian City Pokecenter 1F, map bank `5`, map number `4`.
- The inserter now derives the map header by bank/number, reads existing `MapHeader.events`, fail-closes on object count mismatch, copies the existing object-event table, appends one source-defined object, emits a replacement object table plus replacement `MapEvents`, preserves original warp/coord/bg pointers, and repoints only `MapHeader.events`.
- Added one new Viridian Pokecenter Name Rater object event as row `4` / local id `5`, `MAP_OBJ_GFX_GENTLEMAN`, coordinate `(10, 5)`, elevation `3`, `MOVEMENT_TYPE_FACE_DOWN`, script `EventScript_PokeCenterNameRater`.
- Existing Viridian Pokecenter Nurse, Gentleman, Boy, Youngster, warps, coord events and bg events are intended to remain owned by the original source data and preserved by copy/pointer preservation; manual runtime smoke is still required.
- Updated `08_tests/randomizer/cfru-name-rater-centers-qol.md` with the implemented overlay MVP, added-NPC details, smoke gate and caveats.
- No global Pokecenter rollout, Pewter change, Faster Intro, Oak/Lab/Parcel, Bill-Sevii, Repel-Reuse, auto-run/running indoors, poison, EXP, Runtime Options, Hidden Items, Itemfinder sparkle, itemball graphics, Field Items, UPR-FVX writer, DPE data, binary patch, ROM, save, build, tool binary, raw log, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - CFRU Pokecenter map object ownership design

- Branch: `design/cfru-pokecenter-map-object-ownership`.
- PR #448 was fast-forwarded into current `main` before creating this branch.
- Added `01_docs/analysis/cfru-pokecenter-map-object-ownership.md` as a design-only source-backed analysis for adding extra Pokecenter NPCs without existing-NPC replacement.
- Added `08_tests/randomizer/cfru-pokecenter-map-object-ownership.md` as the future manual smoke and rollout handoff.
- Read-only CFRU review found that `eventscripts` only repoints existing object-event script pointers; it cannot append objects, update object counts, allocate a new object-event table, or repoint `MapHeader.events`.
- Read-only pret review found the source-owned model: `map.json` object events are generated into object arrays and `MapEvents` structs by `tools/mapjson/mapjson.cpp`.
- Result decision: `implementable-medium`. Recommended path is a CFRU-owned map-object overlay/generator that derives map headers by bank/number, copies existing object templates during insertion, appends source-defined objects, emits replacement object table plus replacement `MapEvents`, preserves original warp/coord/bg pointers, and repoints `MapHeader.events`.
- Viridian pilot design records current object count `4`, desired new zero-based table row `4` / local id `5`, `MAP_OBJ_GFX_GENTLEMAN`, candidate coordinate `(10, 5)`, elevation `3`, `MOVEMENT_TYPE_FACE_DOWN`, and future `EventScript_PokeCenterNameRater`.
- No CFRU, DPE, UPR-FVX, Hidden Item, itemball, Field Item, Faster Intro, Bill-Sevii, ROM, binary patch, build, save, emulator state, tool binary, screenshot, raw log, private path, token, secret or `.env` data was changed or documented.

# Session update - CFRU Name Rater Pokecenter pilot correction

- Branch: `feature/cfru-name-rater-centers-qol`.
- CFRU submodule branch: `feature/cfru-name-rater-centers-qol`.
- CFRU commit: `5658d5e4cb13f4acaeabf1c0809f7ed05f9f225b`.
- PR #448 review correction rejected the existing Viridian Pokecenter replacement pilot as a rollout basis because it repointed object event id `1`, the existing Gentleman at `(12, 5)`.
- Source-backed CFRU review found that `eventscripts` can only repoint existing object-event script pointers. `scripts/insert.py` reads the existing object count and rejects object ids outside that count; it does not add object events, increment counts, allocate a new object-event table, or repoint the map event header.
- No local CFRU source-owned Viridian/Pewter Pokecenter object-event table was found. Adding a fifth Viridian Pokecenter NPC would require raw map-event-table replacement or a broader map-object ownership/refactor design, which is out of scope.
- Removed the prior CFRU replacement hook and unused pilot script/text, restoring the original Viridian Pokecenter Gentleman ownership.
- Updated `08_tests/randomizer/cfru-name-rater-centers-qol.md` as a Stop/Handoff for an added-NPC design instead of an implemented pilot.
- No global Pokecenter rollout, Pewter change, Faster Intro, Oak/Lab/Parcel, Bill-Sevii, Repel-Reuse, auto-run/running indoors, poison, EXP, Runtime Options, Hidden Items, Itemfinder sparkle, itemball graphics, Field Items, UPR-FVX writer, DPE data, Viridian-Forest-Nurse, Step Item Guarantees, Friendship Boost, binary patch, ROM, save, build, tool binary, raw log, screenshot, token, secret or `.env` data was changed or documented.

# Session update - CFRU Name Rater Pokecenter pilot

- Branch: `feature/cfru-name-rater-centers-qol`.
- PR #447 was verified as merged by fast-forwarding `main` to merge commit `cd3fb73` before creating this branch.
- CFRU submodule branch: `feature/cfru-name-rater-centers-qol`.
- CFRU commit: `0a0af84a6b4ee649ea4bff7135ba4efd4f3f2c3e`.
- Read-only CFRU review found existing nickname special plumbing in `src/scripting.c`, optional vanilla-special replacement wiring in `routinepointers`, and a source-backed map object script repoint surface in `eventscripts`.
- Read-only vanilla reference review identified the Name Rater flow in `LavenderTown_House2`, plus Viridian and Pewter Pokecenter object-event candidates.
- Implemented exactly one pilot map: Viridian City Pokecenter 1F object event id `1` now points to `EventScript_PilotPokeCenterNameRater`.
- Added a project-local Name Rater pilot script and text, using existing vanilla special ids for party selection, nickname buffering, ownership checks, nickname screen, and changed-name detection.
- Added `08_tests/randomizer/cfru-name-rater-centers-qol.md` with source findings, Pilot-Map details, manual smoke proposal, caveats, and rollout handoff.
- No global Pokecenter rollout, Pewter change, Faster Intro, Oak/Lab/Parcel, Bill-Sevii, Repel-Reuse, auto-run/running indoors, poison, EXP, Runtime Options, Hidden Items, Itemfinder sparkle, itemball graphics, Field Items, UPR-FVX writer, DPE data, Viridian-Forest-Nurse, Step Item Guarantees, Friendship Boost, binary patch, ROM, save, build, tool binary, raw log, screenshot, token, secret or `.env` data was changed or documented.

# Session update - CFRU Bill Sevii QoL

- Branch: `feature/cfru-bill-sevii-qol`.
- PR #446 was verified as merged before switching to current `main`, pulling with fast-forward only, and creating this branch.
- Read-only CFRU review covered Bill, Sevii, Blaine, Cinnabar, One Island, Celio, Tri-Pass, Ruby/Sapphire and Network Machine source surfaces.
- Vanilla reference review found the target behavior across Blaine post-battle, Cinnabar outdoor Bill scene, Cinnabar Pokemon Center Bill prompt, One Island Harbor arrival, One Island Pokemon Center Bill/Celio first meeting, Tri-Pass grant, and the Sevii return path.
- Stop rule triggered: current CFRU source exposes constants, item data, trainer data, debug helpers and general script engine surfaces, but not the Cinnabar/One-Island map scripts that own the behavior. Implementing this now would require raw address replacement or owning multiple map-script subflows.
- Added `08_tests/randomizer/cfru-bill-sevii-qol.md` as the sanitized no-code handoff, including current flow notes, rejected hook decision, and future manual smoke proposal.
- No CFRU/DPE/UPR-FVX source, Field Item behavior, hidden sparkle, itemball graphics, randomizer writer, roadmap status, tool pin, ROM, save, build, tool binary, raw log, screenshot, token, secret or `.env` data was changed or documented.

# Session update - CFRU Faster Intro QoL

- Branch: `feature/cfru-faster-intro-qol`.
- PR #445 was verified as merged before creating this branch from current `main`.
- Read-only CFRU review covered the New Game / intro / Oak / Lab / Route 1 Parcel / Viridian early-script area in local source surfaces.
- The only locally confirmed Faster-Intro-adjacent coverage is existing CFRU behavior: controls-guide skip and Oak tutorial battle absence. Per user decision, CFRU-covered QoL is accepted without additional preserve-smoke and was not retested in this block.
- Stop rule triggered for new implementation: a broader Oak/Lab/Parcel change would require either raw address-level replacement or a multi-map script design, not one isolated source-backed QoL feature.
- Added `08_tests/randomizer/cfru-faster-intro-qol.md` as the sanitized no-code handoff, including the minimal next design proposal and future smoke gate.
- No CFRU/DPE/UPR-FVX source, Field Item behavior, hidden sparkle, itemball graphics, randomizer writer or forbidden local artifact was changed or documented.

# Session update - CFRU QoL coverage analysis

- Branch: `analysis/cfru-qol-coverage`.
- Verified PR #444 was merged before creating the branch from current `main`.
- Added `01_docs/analysis/cfru-qol-coverage.md` as a source-backed, documentation-only coverage map of current Planton361 CFRU QoL features against the Ironmon / FireRed baseline.
- Added `08_tests/randomizer/cfru-qol-coverage.md` as the sanitized coverage handoff and preserve-smoke proposal.
- Main finding: `BW_REPEL_SYSTEM` is active in current CFRU source and should be tested/preserved, not newly built. It is compile-time plus script behavior, and no runtime Options-menu toggle was found.
- Already-covered CFRU areas include controls-guide skip, Oak tutorial battle absence, Repel-Reuse, auto-run path, running indoors, poison faint behavior, old/flat EXP profile, reusable TMs, select-from-PC, party move-item path, item picture/description acquire behavior, auto lowercase naming screen, multiple Premier Balls, HM field-use convenience, Portable PC plumbing and current Runtime Options pages.
- Needs-design items remain separate: broader Faster Intro / New Game Flow, shortened Oak/Lab/Parcel flow, visible Hidden Items / Itemfinder sparkle cue, yellow/golden TM/HM or important itemballs, Name Rater in Poke Centers, lab-specific convenience and Bill-Sevii auto-ask removal.
- Scope remains documentation-only. No CFRU/DPE/UPR-FVX source file or submodule pin was changed, and no forbidden local artifact was documented.

# Session update - CFRU QoL New Game remaining smoke results

- Branch: `test/cfru-qol-new-game-smoke-remaining`.
- PR #443 was verified as merged, and this branch was created from current `origin/main`.
- Updated `08_tests/randomizer/cfru-qol-new-game-smoke.md` with the remaining sanitized manual CFRU QoL / New Game smoke results.
- User-reported result: New Game Start, intro controls guide skipped, Oak Tutorial battle absent, Teachy-TV unchanged, old/flat EXP symptom smoke, poison overworld faint, SwSh catch-level malus absent, and Randomizer compatibility without Field Item changes all functioned.
- Overall smoke status is now `PASS_FULL_WITH_CAVEATS`: all planned manual smoke cases are green by user report, but coverage remains manual and non-automated.
- Caveats remain explicit: no full-playthrough, BizHawk validation, Ironmon Tracker validation, P1 support, Field Item writer coverage, hidden-sparkle behavior, itemball graphics behavior, Randomizer writer change, binary patch use, CFRU/DPE/UPR-FVX code change or submodule repin is claimed.
- No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash value, private path, token, secret or `.env` data was changed or documented.

# Session update - CFRU QoL New Game settings smoke result

- Branch: `test/cfru-qol-new-game-smoke-results`.
- PR #442 was verified as merged, and the branch was confirmed against current `origin/main` before documenting results.
- Updated `08_tests/randomizer/cfru-qol-new-game-smoke.md` with a sanitized manual Runtime / Settings smoke result.
- User-reported result: existing Runtime / Settings functionality was manually checked, appeared to work, and showed no obvious regression.
- Status is deliberately narrow: `PASS_SETTINGS_ONLY_WITH_CAVEATS`. New Game Start, controls guide skip, Oak Tutorial absence, Teachy-TV, EXP, poison overworld faint, SwSh catch-level malus and Randomizer no-Field-Items compatibility remain `not run` for this result.
- Scope remains documentation-only. No CFRU/DPE/UPR-FVX source, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash value, private path, token, secret or `.env` data was changed or documented.
- Roadmap status was not changed because this records a narrow settings result only and does not promote the full smoke matrix.

# Session update - CFRU QoL New Game smoke plan

- Branch: `test/cfru-qol-new-game-smoke`.
- PR #441 was verified as merged before creating this branch from the updated Workspace `main`.
- Added `08_tests/randomizer/cfru-qol-new-game-smoke.md` as a documentation-only smoke-test plan for the existing CFRU QoL / New Game baseline.
- Read-only source review covered current CFRU config, intro controls guide skip, Oak tutorial gating, EXP/poison/catch config surfaces, option-menu runtime rows, Wild Prebattle gating, existing workspace smokes, and UPR-FVX Field Items ownership notes.
- Planned smoke coverage: New Game reaches player control, controls guide skip, Oak tutorial absence, Teachy-TV unchanged/out of scope, runtime option preservation and toggle ownership, old/flat EXP symptom smoke, poison overworld faint, SwSh catch-level malus absence, and randomizer compatibility without Field Item changes.
- Scope remains documentation-only. No CFRU/DPE/UPR-FVX source, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash value, private path, token, secret or `.env` data was changed or documented.
- Roadmap status was not changed because this plan does not promote support status; it only defines the next sanitized smoke protocol.

# Session update - Ironmon QoL feature inventory

- Branch: `analysis/ironmon-qol-feature-inventory`.
- Added `01_docs/analysis/ironmon-qol-feature-inventory.md` as a source-backed, documentation-only inventory of Ironmon-/NatDex-/FireRed-QoL feature candidates for the CFRU/DPE/UPR-FVX workspace.
- Added `08_tests/randomizer/ironmon-qol-feature-inventory.md` as the sanitized inventory smoke and first implementation handoff.
- Inventory target areas: Faster Intro / Controls Guide / Oak Tutorial / New Game Flow; Hidden Items / Itemfinder / Sparkle / Field Effects; Field Item Balls / Pokeball object graphics / TM-HM item balls; Runtime Options / Config Flags; Randomizer interaction with Field Items.
- Main recommendation: first harden the already-documented low-risk CFRU QoL baseline with targeted gameplay smokes, then handle medium hidden-item/script presentation, then preserve existing UPR-FVX Field Items support with regression smokes.
- High-risk or unclear-source items remain blocked: binary QoL patch ports, TM/HM-specific itemball graphics, always-visible hidden-item sparkles, static/gift/NPC item interaction, Shops and Pickup.
- Scope remains documentation-only. No CFRU/DPE/UPR-FVX/Tracker source file or submodule pin was changed. No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash value, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon Showdown data local build/boot smoke

- Branch: `data/showdown-pokemon-data-gen1-9`.
- Documented the sanitized local build/boot smoke after the CFRU learnset syntax repair.
- Current pinned data candidates: DPE `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`; CFRU `8c2d69b48aee8923098912ee06c188d3db93d231`.
- Local reported evidence: DPE build pass, CFRU build on the new DPE ROM pass, mGBA boot pass, no crash before first gameplay pass, and the CFRU learnset syntax repair is included.
- Updated `08_tests/randomizer/showdown-pokemon-data-gen1-9.md` with the sanitized smoke matrix.
- Scope remains documentation-only. No DPE code, CFRU code, UPR-FVX code, submodule pin, ROM, save, emulator state, screenshot, raw log, hash, private path, token, secret or `.env` data was changed or documented.
- Caveat: targeted local build/boot smoke only; no full-playthrough, BizHawk, Ironmon Tracker, or P1 support claim.

# Session update - Pokemon Showdown Pokemon Data Gen1-9 sync

- Workspace branch: `data/showdown-pokemon-data-gen1-9`.
- DPE branch: `data/showdown-pokemon-data-gen1-9`; final DPE commit `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`.
- CFRU branch: `data/showdown-pokemon-data-gen1-9`; final CFRU commit `8c2d69b48aee8923098912ee06c188d3db93d231`.
- Added `07_scripts/data_audit/showdown_pokemon_data_sync.py` as a fail-closed helper that reads external Pokemon Showdown data, local CFRU/DPE constants, and the reviewed alias table; it writes only with `--write`.
- Updated DPE `src/Base_Stats.c` and `src/Learnsets.c` generation-by-generation from Pokemon Showdown for safe mapped Species and allowed fields.
- Updated CFRU `src/Tables/level_up_learnsets.c` for Gen1-8; Gen9 produced no CFRU learnset diff.
- Final dry-runs for Gen1-9 report `base_species_with_changes: 0` and `base_field_changes: 0`.
- Aggregate ready learnset validation covered `1109` DPE/CFRU expected-output blocks with `0` drift.
- Remaining blockers are intentional and source-visible: Ability behavior risk, Move open-risk such as Ally Switch, missing Showdown form learnsets, reviewed Species open-risk families, and reviewed ignores.
- Added `08_tests/randomizer/showdown-pokemon-data-gen1-9.md` as the sanitized data-sync smoke and handoff.
- Scope excludes Pokemon Showdown data copies, raw reports, ROMs, saves, emulator states, builds, tool binaries, screenshots, hashes, private paths, tokens, secrets, `.env`, full-playthrough, BizHawk, Ironmon Tracker, and P1 support claims.

# Session update - DPE Base Stats full source sync audit

- Branch: `analysis/dpe-base-stats-full-source-sync`.
- Added `01_docs/analysis/dpe-base-stats-full-source-sync.md` as a read-only source-backed audit for whether DPE `src/Base_Stats.c` can be fully or mostly replaced from a current compatible source.
- Added `08_tests/randomizer/dpe-base-stats-full-source-sync.md` as the sanitized smoke record.
- Finding: no full replace is recommended. Planton DPE `origin/master` is compatible but identical for the audited files; Shiny-Miner DPE Gen9 is structurally close but older than the local accepted table state; Skeli DPE, pokeemerald-expansion, and Pokemon Showdown are not drop-in sources.
- Key blockers: local Ogerpon Terastal rows, form naming/open-risk families, and Gen9 Ability names that alias to older local Ability IDs/effects.
- Scope remains documentation-only. No DPE/CFRU/UPR-FVX source, submodule pin, Pokemon Showdown data, external repo, raw report, ROM, save, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed.

# Session update - DPE Base Stats tranche 1

- Workspace branch: `data/dpe-base-stats-tranche-1`.
- DPE branch: `data/dpe-base-stats-tranche-1`.
- DPE commit: `1c8d53870e38d7019c681a68a17c9425a3490611`.
- Implemented the first narrow DPE `Base_Stats.c` tranche from the merged plan PR #434.
- Changed exactly the planned non-Ability fields for 10 Species: Crobat, Magnezone, Sylveon, Brionne, Primarina, Ursaluna, Sneasel-Hisui, Sneasler, Toedscool, and Toedscruel.
- No Ability fields, Catch Rate, EXP Yield, EV Yield, Growth Rate, held items, base stats, moves, learnsets, TM/Tutor compatibility, CFRU code, UPR-FVX code or other DPE files were changed.
- Dry-diff after the tranche: safe candidate Species with non-Ability field diffs dropped from `225` to `215`; `eggGroup1`, `eggGroup2`, `type1`, `type2`, and `genderRatio` counts dropped consistently with the 10-Species tranche.
- Added `08_tests/randomizer/dpe-base-stats-tranche-1.md` as the sanitized source/diff smoke.
- Scope excludes ROMs, saves, builds, tool binaries, screenshots, raw reports, hashes, private paths, tokens, secrets and `.env` data.

# Session update - DPE Base Stats Gen9 tranche 1 plan

- Branch: `analysis/dpe-base-stats-gen9-tranche-1-plan`.
- Added `01_docs/analysis/dpe-base-stats-gen9-tranche-1-plan.md` as the documentation-only plan for the first real DPE `Base_Stats.c` update tranche.
- Added `08_tests/randomizer/dpe-base-stats-gen9-tranche-1-plan.md` as the sanitized planning smoke.
- Ran the read-only dry-diff helper against the external Pokemon Showdown data directory with `--limit 25`; result remained `PASS_READ_ONLY_WITH_BLOCKERS`.
- Recommended tranche 1 is 10 Species: Sneasel-Hisui, Sneasler, Ursaluna, Toedscool, Toedscruel, Primarina, Brionne, Sylveon, Magnezone, and Crobat.
- Tranche 1 intentionally excludes Ability fields, Catch Rate, EXP Yield, EV Yield, Growth Rate, moves, learnsets, TM/Tutor compatibility, Species `open-risk`, reviewed ignores, cosmetic Pikachu forms, representation-only gender differences, egg-group order-only churn, and obvious local stat/type balance changes.
- Scope remains planning/documentation only. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, Pokemon Showdown source, raw report, ROM, save, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - DPE Base Stats Gen9 safe dry diff

- Branch: `analysis/dpe-base-stats-gen9-safe-dry-diff`.
- Added `07_scripts/data_audit/dpe_base_stats_dry_diff.py` as a read-only dry-diff helper for DPE `src/Base_Stats.c` against external Pokemon Showdown `pokedex.ts`.
- The helper uses `showdown_mapping_audit.py` normalization and `showdown_aliases.json`; it writes no DPE/CFRU tables and emits only a compact sanitized summary.
- Dry-diff result against the external Pokemon Showdown data directory: `PASS_READ_ONLY_WITH_BLOCKERS`.
- Sanitized counts: `1317` tested Species, `29` Species `open-risk` skipped, `167` reviewed Species ignores skipped, `65` Species blocked from safe candidate promotion by Ability blockers, `4` missing local entries after alias/ignore handling, and `225` safe candidate Species with non-Ability field diffs.
- Ability assignment differences are reported separately and remain analysis-only while Ability behavior/open-risk blockers remain.
- Showdown `pokedex.ts` did not provide Catch Rate, EXP Yield, EV Yield, or Growth Rate for this pass; those fields require a secondary source before any real DPE update.
- Added `01_docs/analysis/dpe-base-stats-gen9-safe-dry-diff.md` and `08_tests/randomizer/dpe-base-stats-gen9-safe-dry-diff.md`.
- Scope remains read-only tooling/documentation only. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, Pokemon Showdown source, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon data generator dry-run plan

- Branch: `analysis/pokemon-data-generator-dry-run-plan`.
- Added `07_scripts/data_audit/pokemon_data_dry_run.py` as a read-only dry-run gate for future Pokemon Showdown-to-CFRU/DPE data generator work.
- The helper uses `showdown_mapping_audit.py` normalization, `showdown_aliases.json`, external Showdown data inputs, and local CFRU/DPE table-shape counts; it writes no reports or data tables.
- Dry-run result against the external Showdown data directory: `BLOCKED_BY_REVIEWED_POLICY`, with 0 uncategorized Species/Move/Ability keys but blocking reviewed Species `open-risk`, Move `open-risk`, and Ability `behavior-risk` / `open-risk` categories.
- Documented per-block inputs, blockers, expected output, risk, and first implementation PR for Base Stats, Ability Assignments, Level-up Learnsets, Egg Moves, TM Compatibility, and Tutor Compatibility in `01_docs/analysis/pokemon-data-generator-dry-run-plan.md`.
- Added `08_tests/randomizer/pokemon-data-generator-dry-run-plan.md` as the sanitized dry-run smoke.
- Scope remains read-only tooling/documentation only. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, Pokemon Showdown source, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon data species alias table final

- Branch: `analysis/pokemon-data-species-alias-table-final`.
- Expanded `07_scripts/data_audit/showdown_aliases.json` from 239 to 471 reviewed entries with Species-only final classifications.
- Classified the remaining Species unresolved buckets from the external Pokemon Showdown audit: Showdown-without-local Species are now 319 classified / 0 still uncategorized; local-without-Showdown Species are now 221 classified / 0 still uncategorized.
- Added explicit Species classifications for additional local shortforms, GMax/Giga naming, cosmetic forms, CAP/Fan/Pokestar/Totem/non-project ignores, local sentinel/helper/project extras, and blocking open-risk form families.
- Blocking Species groups remain Alcremie cream/sweet forms, Basculin/Basculegion form semantics, Battle Bond Greninja, Pumpkaboo/Gourgeist size naming, Ogerpon mask-vs-form naming, Sinistea/Polteageist antique/chipped naming, Rockruff Dusk, and Tatsugiri form color/name semantics.
- Updated `01_docs/analysis/pokemon-data-reviewed-alias-table.md` and `08_tests/randomizer/pokemon-data-reviewed-alias-table.md` with sanitized counts and caveats.
- Scope remains alias-table/documentation only. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, Pokemon Showdown source, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon data ability risk table final

- Branch: `analysis/pokemon-data-ability-risk-table-final`.
- Expanded `07_scripts/data_audit/showdown_aliases.json` from 215 to 239 reviewed entries with Ability-only final classifications.
- Classified the remaining Ability unresolved buckets from the external Pokemon Showdown audit: Showdown-without-local Abilities are now 36 classified / 0 still uncategorized; local-without-Showdown Abilities are now 8 classified / 0 still uncategorized.
- Added source-backed legacy merges for Air Lock, Iron Barbs, Power of Alchemy, Propeller Tail, Pure Power, Queenly Majesty, Solid Rock, Tangling Hair, Vital Spirit, White Smoke, and Wimp Out where CFRU/DPE comments or shared paths show intentional local merges.
- Added blocking classifications for As One name mismatches, pure Chilling Neigh missing-local risk, Full Metal Body alias-plus-hook risk, and Libero / Protean behavior risk.
- Added explicit non-project ignores for Showdown `isNonstandard` Future/CAP Ability names and a sentinel-only `noability` / `ABILITY_NONE` name-mismatch ignore.
- Updated `01_docs/analysis/pokemon-data-reviewed-alias-table.md` and `08_tests/randomizer/pokemon-data-reviewed-alias-table.md` with sanitized counts and caveats.
- Scope remains alias-table/documentation only. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, Pokemon Showdown source, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon data ability risk table

- Branch: `analysis/pokemon-data-ability-risk-table`.
- Expanded `07_scripts/data_audit/showdown_aliases.json` from 191 to 215 reviewed entries with Ability-only risk classifications from the source-backed CFRU/DPE Ability behavior audit.
- Ability categories now include `alias-plus-hook` behavior-risk, blocking `behavior-risk`, `missing-local` open-risk, blocking `name-mismatch`, non-blocking `intentionally-merged`, and `local-only` ignores.
- Marked the requested focus set: Hadron Engine, Orichalcum Pulse, Toxic Debris, Poison Puppeteer, Sharpness, Rocky Payload, Seed Sower, Wind Power, Wind Rider, Ruin abilities, Good as Gold, Zero to Hero, Terapagos Tera abilities, Commander, Hospitality, and Embody Aspect variants.
- Ability entries with behavior/open risk carry blocking generator policy; only explicit legacy merges and local-only ignores are non-blocking classifications.
- Updated `01_docs/analysis/pokemon-data-reviewed-alias-table.md` and `08_tests/randomizer/pokemon-data-reviewed-alias-table.md` with the sanitized counts and caveats.
- Scope remains alias-table/documentation only. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, Pokemon Showdown source, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon ability behavior risk audit

- Branch: `analysis/pokemon-ability-behavior-risk-audit`.
- Added `01_docs/analysis/pokemon-ability-behavior-risk-audit.md` as a source-backed, read-only CFRU/DPE audit of Gen9/newer Ability behavior risk.
- Added `08_tests/randomizer/pokemon-ability-behavior-risk-audit.md` as the sanitized audit smoke record.
- Key finding: most Gen9-looking Ability names are local aliases to older Ability IDs, but many have species-gated CFRU behavior hooks that make them stronger than pure name aliases.
- Focus findings: Hadron Engine, Orichalcum Pulse, Toxic Debris and Poison Puppeteer have source-backed alias-plus-hook behavior; Ruin abilities and Good as Gold have behavior hooks but remain medium/high risk because of alias plumbing; Zero to Hero is not fully confirmed as true form-change behavior by this source pass.
- Missing/high-risk findings: Commander, Hospitality and Embody Aspect were not found as local Ability constants/behavior; Terapagos Tera Shift / Tera Shell has name/assignment/helper inconsistency and remains blocked for generator-safe behavior assumptions.
- Scope remains documentation-only. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, Showdown source, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon data alias table move final

- Branch: `analysis/pokemon-data-alias-table-move-final`.
- Expanded `07_scripts/data_audit/showdown_aliases.json` from 169 to 191 reviewed entries.
- Classified the remaining Move unresolved buckets only; no Species or Ability entries were expanded.
- Added Move `open-risk` entries for `allyswitch` and 13 Let's Go partner moves because no reviewed local CFRU/DPE engine-backed move exists.
- Added Move `ignore` entries for 3 Showdown CAP moves, 1 Showdown nonstandard Future move, 2 local helper constants, and 2 local CFRU/DPE project moves.
- External-data audit now classifies 104 Showdown-only Move keys and 143 local-only Move keys; 0 Showdown-only Move keys and 0 local-only Move keys remain uncategorized.
- `open-risk` Move entries remain unresolved behavior/mapping gaps, not solved aliases.
- Scope remains read-only alias/data-audit documentation. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, Pokemon Showdown source, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon data alias table move splits

- Branch: `analysis/pokemon-data-alias-table-move-splits`.
- Expanded `07_scripts/data_audit/showdown_aliases.json` from 107 to 169 reviewed entries.
- Added only explicit reviewed Move `split-move` aliases for remaining Z-Move, Max Move, and G-Max Move physical/special local split constants.
- Alias table categories now include Species `form-name` 4, Species `gmax-giga` 32, Species `local-shortform` 55, Move `split-move` 69, Move `hidden-power-variant` ignore 1, Move `spelling` 1, Ability `name-mismatch` 1, and Ability `behavior-risk` 6.
- External-data audit now classifies 86 Showdown-only Move keys and 139 local-only Move keys; 18 Showdown-only Move keys and 4 local-only Move keys remain uncategorized by design.
- Species and Ability alias coverage was intentionally not expanded in this batch.
- Remaining uncategorized Move keys include real behavior/content risks such as Ally Switch, Let's Go-style moves, CAP/fan moves, and local extras; they are not treated as solved aliases.
- Scope remains read-only alias/data-audit documentation. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, Pokemon Showdown source, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon data alias table batch 2

- Branch: `analysis/pokemon-data-alias-table-batch-2`.
- Expanded `07_scripts/data_audit/showdown_aliases.json` from 28 to 107 reviewed entries.
- Added explicit Species-only Batch 2 aliases for regional/local shortforms and the remaining reviewed GMax/Giga Species names.
- Alias table categories now include Species `form-name` 4, Species `gmax-giga` 32, Species `local-shortform` 55, Move `split-move` 7, Move `hidden-power-variant` ignore 1, Move `spelling` 1, Ability `name-mismatch` 1, and Ability `behavior-risk` 6.
- External-data audit now classifies 91 Showdown-only Species keys and 95 local-only Species keys; 228 Showdown-only Species keys and 126 local-only Species keys remain uncategorized by design.
- Move split aliases and Ability behavior-risk expansion were intentionally left for later batches so uncategorized keys stay visible and reviewable.
- Scope remains read-only alias/data-audit documentation. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, Pokemon Showdown source, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon data reviewed alias table

- Branch: `analysis/pokemon-data-reviewed-alias-table`.
- Added `07_scripts/data_audit/showdown_aliases.json` as the first small machine-readable Pokemon Showdown-to-CFRU/DPE alias/ignore table.
- Updated `07_scripts/data_audit/showdown_mapping_audit.py` to load the alias file, summarize reviewed categories, and classify unresolved Showdown/local keys without copying Showdown data into the repo.
- Added `01_docs/analysis/pokemon-data-reviewed-alias-table.md` and `08_tests/randomizer/pokemon-data-reviewed-alias-table.md` as the sanitized review and smoke handoff.
- Initial table coverage: Ogerpon Terastal form aliases, GMax/Giga species naming examples, regional/local shortform examples, Z/Max/GMax physical-special move splits, Hidden Power typed-variant ignore rule, `visegrip` to `vicegrip`, and Ability alias/behavior-risk entries.
- Local external-data audit classified 12 Species Showdown-only keys, 16 local-only Species keys, 24 Showdown-only Move keys, 15 local-only Move keys, and one Ability name mismatch on each side; remaining unresolved mappings stay uncategorized by design.
- Ability aliases remain behavior risks, not solved Gen9 behavior.
- Scope is read-only documentation/tooling. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data was changed or documented.

# Session update - Pokemon data Showdown mapping audit

- Branch: `analysis/pokemon-data-showdown-mapping-audit`.
- Added `01_docs/analysis/pokemon-data-showdown-mapping-audit.md` as the read-only mapping audit plan for Pokemon Showdown data against local CFRU/DPE constants.
- Added `07_scripts/data_audit/showdown_mapping_audit.py` as a small read-only helper that parses local Species/Move/Ability constants and optionally compares against an external Pokemon Showdown `data/` directory without downloading or vendoring Showdown data.
- Added `08_tests/randomizer/pokemon-data-showdown-mapping-audit.md` as the sanitized local-only helper smoke.
- Local-only findings: Species constants are count-matched between CFRU and DPE but Ogerpon Terastal form names differ on `0x592` through `0x595`; Move constants are count/name matched between CFRU and DPE; Ability constants show CFRU-only `EVAPORATE` / `LINGERINGAROMA`, DPE-only `UNUSED`, same value `0x4D` named differently, and 67 total local alias define rows across the two headers.
- Ability aliases remain a separate behavior-risk class; name coverage is not enough for true Gen9 ability behavior.
- Scope is read-only/documentation/tooling. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data was changed.

# Session update - Pokemon data Gen9 inventory

- Branch: `analysis/pokemon-data-gen9-inventory`.
- Added `01_docs/analysis/pokemon-data-gen9-inventory.md` as a source-backed inventory of current CFRU/DPE Pokemon data tables and a conservative update path.
- Source finding: local CFRU/DPE species and move constants already reach Gen9 markers through `SPECIES_PECHARUNT` and `MOVE_PSYCHICNOISE`; level-up learnsets include Gen9 blocks in both CFRU and DPE.
- Source finding: DPE owns primary Pokemon-facing data for base stats, ability assignments, egg moves, and TM/Tutor compatibility inputs; CFRU owns battle move behavior, ability behavior, runtime TM/Tutor bitset reads, and mirrored constants.
- Key caveat: several Gen9 ability names are aliases to older CFRU ability IDs/effects, so ability assignment freshness is not the same as true Gen9 ability behavior.
- Recommended update order: freeze constants/form mapping, generate a read-only Showdown-to-CFRU/DPE mapping diff, then update base stats/ability assignments, move data, learnsets, egg moves, TM compatibility, and tutor compatibility last.
- Scope is documentation-only. No CFRU, DPE, UPR-FVX, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data was changed.

# Session update - CFRU Randomizer baseline config local smoke

- Branch: `feature/cfru-randomizer-baseline-config`.
- Documented the sanitized local build / mGBA smoke result for CFRU Randomizer Baseline Config in `08_tests/randomizer/cfru-randomizer-baseline-config.md`.
- Result: `PASS_TARGETED_LOCAL_BUILD_BOOT_SETTINGS_SMOKE_WITH_CAVEATS`.
- Local reported evidence: CFRU commit `53273184bab06f91cdc3ad6e0e5af4a8ba41591a` was synchronized into the local Mac build workspace, a local clean rebuild completed, `wav2agb` / `mid2agb` were found through local `local-bin` wrappers, the local ROM candidate booted in mGBA, and the new/adjusted in-game settings worked.
- Smoke matrix: Build/Boot pass, Options/Settings pass, Nuzlocke Toggle pass, Wild Prebattle Toggle pass.
- Oak Tutorial removed, Poison Overworld Faint, SwSh Catch-Level-Malus off, Old/Flat EXP, and Intro Controls Guide skipped remain marked inconclusive in this sanitized report because they were not separately documented.
- Scope is documentation-only. No CFRU code, UPR-FVX, DPE, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, ROM hash, private path, token, secret or `.env` data was changed or documented.
- Caveat: targeted local build/boot/settings smoke only; no full-playthrough, BizHawk, Ironmon Tracker or P1 support claim.

# Session update - CFRU Randomizer baseline config

- Branch: `feature/cfru-randomizer-baseline-config`.
- CFRU branch: `feature/cfru-randomizer-baseline-config`.
- CFRU base: `74310deeb62c7f73ba6c7b11f921418617a9a740`.
- CFRU baseline commit: `53273184bab06f91cdc3ad6e0e5af4a8ba41591a`.
- Implemented a narrow CFRU Randomizer-/Ironmon-near baseline configuration.
- Compile-time changes: `TUTORIAL_BATTLES` disabled, `POISON_1_HP_SURVIVAL` disabled, `SWSH_CATCHING_DIFFICULTY_MODIFIER` disabled, `OLD_EXP_SPLIT` enabled, `FLAT_EXP_FORMULA` enabled, and `SKIP_INTRO_CONTROLS_GUIDE` enabled.
- `IgnoreWildPokemon` was left enabled because source search shows it compiles the prebattle feature while runtime generation is gated by `FLAG_ENABLE_WILD_PMN_PREBATTLE_SCREEN`; it does not by itself always ignore wild Pokemon.
- Added Page 3 option-menu toggles `Nuzlocke = Off/On` and `Wild Prebattle = Off/On`.
- `Nuzlocke` only clears/sets `FLAG_NUZLOCKE`; no permanent script activation or helper-state reset was added.
- `Wild Prebattle` only clears/sets `FLAG_ENABLE_WILD_PMN_PREBATTLE_SCREEN`; `FLAG_WILD_POKEMON_PREBATTLE_SCREEN` remains transient encounter/window state.
- Added `08_tests/randomizer/cfru-randomizer-baseline-config.md` as the source-backed implementation and local build/smoke handoff.
- Checks: CFRU `diff --check` passed; `arm-none-eabi-gcc -fsyntax-only src/option_menu.c` passed; workspace `diff --check` passed.
- Scope excludes UPR-FVX, DPE, Trainer AI, Trainer Level Scaling, Hard Cap, Difficulty logic, Wild Encounter Tables, Randomizer code, ROMs, saves, emulator states, builds, tool binaries, screenshots, raw logs, ROM hashes, private paths, tokens, secrets and `.env` data.
- Caveat: no local ROM build, emulator boot, BizHawk/Ironmon Tracker validation, full-playthrough coverage or P1 support claim is included.

# Session update - Trainer AI Policy v3 local smoke

- Branch: `experiment/trainer-ai-policy-v3`.
- Documented the sanitized local mGBA smoke result for Trainer-AI-Policy v3 in `08_tests/randomizer/trainer-ai-policy-v3.md`.
- Result: `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`.
- Local reported evidence: CFRU Trainer-AI-Policy v3 built locally, the local ROM candidate booted in mGBA, `Trainer AI` option values were selectable and appeared to save, and Smart/Hard/Expert appeared distinguishable.
- Rival Smokescreen / move-choice smoke is documented as pass with caveats.
- `Smart` appeared to have Full Smart Move-AI active; `Hard` appeared to add stronger fair reactions without obvious hidden-knowledge behavior; `Expert` appeared to be the strongest profile with plausible advanced behavior.
- Scope is documentation-only. No CFRU code, UPR-FVX, DPE, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, ROM hash, private path, token, secret or `.env` data was changed or documented.
- Caveat: targeted local mGBA smoke only; no full-playthrough, BizHawk, Ironmon Tracker, statistical AI-quality or P1 support claim.

# Session update - Trainer AI Policy v3 experiment

- Branch: `experiment/trainer-ai-policy-v3`.
- CFRU branch: `experiment/trainer-ai-policy-v3`.
- CFRU base: `caaf81b2582d5af0905281aab88658ac145b43eb`.
- CFRU experiment commit: `74310deeb62c7f73ba6c7b11f921418617a9a740`.
- Implemented Trainer-AI Policy v3 as a narrow CFRU experiment.
- `Trainer AI = Smart`, `Hard`, and `Expert` now give all trainer battles full smart move AI: `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`.
- `Smart` remains move-AI-only and no longer falls into Expert-style gates through enum ordering.
- `Hard` gets the fair anti-cheese / Protect-Fake-Out retarget gates, but not switch prediction, shift-switching, bench/prediction behavior or type-resist berry hidden knowledge.
- `Expert` keeps the advanced Expert paths: anti-cheese, Protect/Fake-Out retargeting, switch/prediction behavior, shift-switching, and Expert type-resist berry knowledge where the existing CFRU path permits it.
- `Auto` remains compatibility mode through `GetTrainerAIProfile()` deriving from `Game Difficulty` while the trainer-AI profile var is unset.
- `Vanilla`, `Easy`, and `Normal` were left unchanged except for sharing the explicit enum-safe gate boundaries.
- Added `08_tests/randomizer/trainer-ai-policy-v3.md` as the sanitized implementation and local mGBA smoke handoff.
- Checks: CFRU `diff --check` passed; `arm-none-eabi-gcc -fsyntax-only` passed for `src/Battle_AI/ai_master.c`, `src/Battle_AI/ai_switching.c`, and `src/damage_calc.c`; workspace `diff --check` passed.
- Scope excludes `VAR_GAME_DIFFICULTY` broad effects, trainer level scaling, IV/EV/friendship/PP logic, bag/move restrictions, wild/raid/DexNav/ability-capsule logic, `AI_TRY_TO_KILL_RATE`, UPR-FVX, DPE, ROMs, saves, emulator states, builds, screenshots, raw logs, ROM hashes, private paths, tokens, secrets and `.env` data.

# Session update - Trainer AI Smokescreen behavior analysis

- Branch: `analysis/trainer-ai-smokescreen-behavior`.
- Added `01_docs/analysis/trainer-ai-smokescreen-behavior.md` as a source-backed documentation-only analysis for the Rival `Tackle` + `Smokescreen` Trainer-AI observation.
- Sanitized observed case: Rival trainer battle, opposing Pokemon had `Tackle` + `Smokescreen`, and `Smokescreen` was repeatedly selected until the player's Accuracy reached minimum.
- Source-backed interpretation: this is plausible but suspicious. CFRU `CHECK_BAD_MOVE` only rejects Accuracy-down when Accuracy cannot be lowered or the move is blocked, while `CHECK_GOOD_MOVE` can actively boost Accuracy-down through positive utility scoring. Current Smart Trainer AI v2 only ORs `CHECK_BAD_MOVE | SEMI_SMART`, but existing trainer data with `CHECK_GOOD_MOVE` can still preserve very-smart behavior.
- Documented current Trainer AI option interpretation for `Auto`, `Vanilla`, `Easy`, `Normal`, `Hard`, `Expert`, and `Smart`, plus a local mGBA A/B smoke plan.
- Scope is documentation-only. No CFRU, DPE, UPR-FVX, Tracker, ROM, save, emulator state, build artifact, screenshot, raw log, hash, private path, local address, secret, token, `.env` data, external repo or submodule pin was changed or documented.

# Session update - MacBook rebuild success status sync

- Branch: `docs/macbook-rebuild-success`.
- Documented the sanitized MacBook rebuild status as `01_docs/setup/macbook-rebuild-success.md`.
- Confirmed local UPR-FVX submodule pin: `1a597a667129b50284dd88afb231372b5bd01d7f` on `02_external/upr-fvx`.
- Local UPR-FVX status: `./gradlew clean :random:jar` completed, and the UPR-FVX GUI starts with Java 25.
- Local GBA tooling status: devkitPro/devkitARM, `arm-none-eabi-gcc` 15.2.0, `gbafix`, `grit`, GNU Make 4.4.1, and local Wine wrappers for `wav2agb.exe` / `mid2agb.exe` are present.
- Local rebuild status: DPE and CFRU builds completed successfully.
- Local smoke status: the final local CFRU+DPE Gen9 ROM candidate loads in UPR-FVX and boots in mGBA.
- BizHawk/Ironmon Tracker remains open follow-up scope.
- Scope is documentation-only. No UPR-FVX, CFRU, DPE, Tracker, ROM, save, emulator state, build artifact, screenshot, raw log, ROM hash, private path, local address, secret, token, `.env` data or external repo was changed or documented.

# Session update - CFRU settings split final smoke

- Branch: `test/cfru-settings-split-final-smoke`.
- Added `08_tests/randomizer/cfru-settings-split-final-smoke.md` as the sanitized final local smoke record for the CFRU settings-split UI.
- Result: `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`.
- Page 3 layout is documented as clean with `Level Scaling`, `Trainer AI`, `Hard Cap`, and `Cancel`.
- Runtime smoke interpretation: Level Scaling works per setting, Trainer AI works separately, `Game Difficulty` `Vanilla` / `Normal` / `Expert` are separately usable, Hard Cap `Auto` / `Off` / `On` is visible and plausibly active, and Wild Level Scaling remains separate from Game Difficulty and Trainer Level Scaling.
- Better Movesets / Trainer Rows remain a previously validated UPR-FVX baseline and were not reopened in this final CFRU UI smoke.
- Scope is documentation-only. No CFRU, DPE, UPR-FVX, Tracker, ROM, save, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU hard level cap option row

- Branch: `feature/cfru-settings-hard-level-cap-option`.
- CFRU branch `feature/cfru-settings-hard-level-cap-option` adds a Page 3 option-menu row for `Hard Cap`.
- Added `VAR_HARD_LEVEL_CAP_MODE = 0x515C` because that var ID was still free in the audited CFRU config range.
- UI values are `Auto`, `Off`, and `On`; raw `0=Auto` preserves legacy/script-owned `FLAG_HARD_LEVEL_CAP` state, raw `1=Off` clears `FLAG_HARD_LEVEL_CAP`, and raw `2=On` sets `FLAG_HARD_LEVEL_CAP`.
- `FLAG_KEPT_LEVEL_CAP_ON` remains untouched by the menu and is not used as menu state.
- Scope: CFRU option-menu var/flag plumbing plus Workspace pin/docs only. No EXP, Rare Candy, Daycare, DexNav, Wild, Trainer Level Scaling, Difficulty, Trainer AI, UPR-FVX, DPE, Tracker, ROM, save, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU hard level cap menu option analysis

- Branch: `analysis/cfru-hard-level-cap-menu-option`.
- Added `01_docs/analysis/cfru-hard-level-cap-menu-option.md` as a source-backed documentation-only analysis for adding Hard Level Cap as the final practical CFRU option-menu Page 3 row.
- Source finding: `FLAG_HARD_LEVEL_CAP` controls enforcement across EXP gain, Rare Candy, Daycare, wild encounters, DexNav, and catchable wild-boss caps; `FLAG_KEPT_LEVEL_CAP_ON` is only cleared at battle start when a party mon exceeds cap and should not be used as menu state.
- Cap calculation is badge-count based in `GetCurrentLevelCap()`: before Brock the cap is `15`, then `20/25/30/35/40/45/50`, and after all eight badges `100`.
- Recommendation: later implementation should use `Hard Cap = Auto / Off / On` on Page 3, backed by a new `VAR_HARD_LEVEL_CAP_MODE = 0x515C` if still free, while keeping enforcement on `FLAG_HARD_LEVEL_CAP` and leaving `FLAG_KEPT_LEVEL_CAP_ON` untouched.
- Scope is documentation-only. No CFRU, DPE, UPR-FVX, Tracker, ROM, save, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU game difficulty vanilla option analysis

- Branch: `analysis/cfru-game-difficulty-vanilla-option`.
- Added `01_docs/analysis/cfru-game-difficulty-vanilla-option.md` as a source-backed analysis of whether `Game Difficulty` needs an explicit `Vanilla` / `Off` value after the Difficulty, Trainer Level Scaling, and Trainer AI split.
- Finding: current raw `0` is legacy `Normal`, not a separate off mode; Normal avoids many Hard/Expert rules but still is not a strict FireRed-/Ironmon-near no-Difficulty-bundle mode because trainer EV spreads, runtime randomized-trainer evolution, non-Easy raid item punishment, and some wild/raid/fog behavior can still differ.
- Recommendation: add a later explicit `Difficulty = Vanilla` mode if strict no-Difficulty power/rules are desired; do not reinterpret raw `0`, use a new explicit raw value and map behavior through helpers/predicates.
- Scope is documentation-only. No CFRU, DPE, UPR-FVX, Tracker, ROM, save, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU trainer level scaling gate

- Branch: `feature/cfru-enable-trainer-level-scaling-gate`.
- CFRU branch `feature/cfru-enable-trainer-level-scaling-gate` enables the compile-time trainer level-scaling path with `SCALED_TRAINERS`.
- Source-backed cause: `CreateNPCTrainerParty()` and the generic/boss scaling formulas already used `GetTrainerLevelScalingMode()`, but they were behind `#if (defined SCALED_TRAINERS && !defined DEBUG_NO_LEVEL_SCALING)`.
- Added the missing project-local `FLAG_SCALE_WILD_BOSS_LEVEL` definition because the compiled trainer-scaling path already references that optional flag for wild-boss partner scaling; it remains inactive unless scripts explicitly set it.
- Added the existing `include/new/exp.h` include to `build_pokemon.c` so the newly compiled hard-level-cap branch sees `GetCurrentLevelCap()`.
- Compatibility rule: explicit `Trainer Level Scaling = Off` still disables trainer scaling, raw `0` / `Auto` still derives from `VAR_GAME_DIFFICULTY`, and Easy/Normal/Hard/Expert now reach the existing trainer scaling formulas.
- Checks: CFRU `diff --check` passed; `arm-none-eabi-gcc -fsyntax-only` passed for `src/build_pokemon.c`.
- Scope: CFRU trainer-level-scaling compile gate plus Workspace docs only. No UPR-FVX, DPE, Tracker, Trainer AI, Better Movesets, UI layout, ROM, save, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU trainer AI profile option row

- Branch: `feature/cfru-settings-trainer-ai-profile-option`.
- CFRU branch `feature/cfru-settings-trainer-ai-profile-option` adds only a second-page options-menu row for `Trainer AI`.
- UI values are `Auto`, `Vanilla`, `Easy`, `Normal`, `Hard`, `Expert`, and `Smart`; `Auto` maps to raw `VAR_TRAINER_AI_PROFILE == 0` and keeps legacy Difficulty-/flag-derived Trainer-AI behavior.
- Added original-raw plus dirty tracking for the new row so opening and closing the menu without changing `Trainer AI` preserves the existing raw value, including legacy raw `0`.
- The row writes only `VAR_TRAINER_AI_PROFILE` when changed; the existing `Game Difficulty` row, Level Scaling behavior, Smart-AI flag logic, and gameplay logic outside the options menu were left unchanged.
- Checks: CFRU `diff --check` passed; `arm-none-eabi-gcc -fsyntax-only` passed for `src/option_menu.c`; targeted `rg` checks confirmed the new Trainer-AI var in `option_menu.c` and limited Level Scaling changes to existing row/page-array context.
- Scope: CFRU options-menu row/text plus Workspace pin/docs only. No UPR-FVX, DPE, Tracker, Difficulty reorder, Trainer-Level-Scaling behavior change, ROM, save, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU level scaling option row

- Branch: `feature/cfru-settings-level-scaling-option`.
- CFRU branch `feature/cfru-settings-level-scaling-option` adds only a second-page options-menu row for `Level Scaling`.
- UI values are `Auto`, `Off`, `Easy`, `Normal`, `Hard`, and `Expert`; `Auto` maps to raw `VAR_TRAINER_LEVEL_SCALING_MODE == 0` and keeps legacy Difficulty-derived scaling behavior.
- Added original-raw plus dirty tracking for the new row so opening and closing the menu without changing `Level Scaling` preserves the existing raw value, including legacy raw `0`.
- The row writes only `VAR_TRAINER_LEVEL_SCALING_MODE` when changed; the existing `Game Difficulty` row, Trainer AI profile storage, Difficulty ordering, and gameplay logic outside the options menu were left unchanged.
- Checks: CFRU `diff --check` passed; `arm-none-eabi-gcc -fsyntax-only` passed for `src/option_menu.c`; targeted `rg` checks confirmed the new level-scaling var in `option_menu.c` and no new `VAR_TRAINER_AI_PROFILE` UI path.
- Scope: CFRU options-menu row/text plus Workspace pin/docs only. No UPR-FVX, DPE, Tracker, Trainer-AI UI, Difficulty reorder, ROM, save, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU settings UI split implementation plan

- Branch: `analysis/cfru-settings-ui-tab-implementation-plan`.
- Added `01_docs/analysis/cfru-settings-ui-tab-implementation-plan.md` as a source-backed implementation plan for exposing split CFRU difficulty settings in the CFRU option menu.
- Source-backed UI finding: `src/option_menu.c` currently has two hard-coded pages; page 2 already contains CFRU/project settings and `Game Difficulty`, so the first implementation should extend page 2 instead of adding a third page/tab.
- Planned UI rows: `Difficulty` backed by `VAR_GAME_DIFFICULTY`, `Level Scaling` backed by `VAR_TRAINER_LEVEL_SCALING_MODE`, and `Trainer AI` backed by `VAR_TRAINER_AI_PROFILE`.
- Critical implementation rule: split vars use raw `0 = legacy/unset`, but `CloseAndSaveOptionMenu()` currently writes all page-2 vars on close, so implementation must add dirty/original-raw tracking before displaying derived helper values.
- Recommended order: implement Trainer Level Scaling display/write first, then Trainer AI Profile, then decide whether to reorder Difficulty display from raw order to requested Easy/Normal/Hard/Expert order.
- Scope is documentation-only. No CFRU/DPE/UPR-FVX code, ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, local addresses, secrets, tokens, or `.env` data was changed or documented.

# Session update - CFRU difficulty power/rules mode split

- Branch: `feature/cfru-difficulty-power-rules-mode`.
- CFRU branch `feature/cfru-difficulty-power-rules-mode` migrates remaining clear Difficulty Power/Rules reads from direct `VAR_GAME_DIFFICULTY` checks to `GetGameDifficultyMode()`.
- Migrated trainer-power paths: trainer IV force-to-31 on Expert, trainer EV spread Easy suppression, Unbound Rival EV spread challenge gates, boss/rival max-EV and max-friendship gates, and trainer move PP bonus on Expert.
- Migrated player/battle-rule paths: bag restrictions, Minimize/evasion move restriction, sleep clause, Bad Thoughts damage, and fog accuracy penalty.
- Migrated wild/raid/special-rule paths: wild scripted custom-move PP bonus, Shadow Warrior hidden ability, wild smart-move difficulty fallback, smart-wild special species gate, raid attack-again item punishment, raid start-shield gate, DexNav hidden Imposter restriction, ability-capsule hidden Imposter restriction, wild boss level difficulty fallback, non-trainer AI item/damage knowledge fallback, and Hall of Fame difficulty display read.
- Classification of remaining direct difficulty storage reads: `src/util.c` intentionally owns `GetGameDifficultyMode()` compatibility over `VAR_GAME_DIFFICULTY`; `src/option_menu.c` intentionally remains existing UI/storage plumbing for the single legacy difficulty var in this no-UI branch.
- Already separated paths left intact: Trainer Level Scaling stays on `GetTrainerLevelScalingMode()`, Trainer AI Profile stays on `GetTrainerAIProfile()` / `IsSmartTrainerAIEnabled()`, and Smart Trainer AI compatibility behavior is unchanged.
- Open semantic caveat: CFRU runtime randomized-trainer evolution and wild/raid AI gates still derive from DifficultyMode for compatibility; they were not split into new randomizer or Wild/Raid AI settings in this branch.
- Checks: CFRU `diff --check` passed; `arm-none-eabi-gcc -fsyntax-only` passed for changed CFRU C files, with pre-existing warnings observed in `dexnav.c` and `wild_encounter.c`.
- Scope: CFRU Difficulty Power/Rules helper migration plus Workspace pin/docs only. No UPR-FVX, DPE, Tracker, UI tab, ROM, save, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU trainer AI profile mode split

- Branch: `feature/cfru-trainer-ai-profile-mode`.
- CFRU branch `feature/cfru-trainer-ai-profile-mode` migrates clear Trainer-AI profile gates to `GetTrainerAIProfile()` and `IsSmartTrainerAIEnabled()`.
- Migrated paths: `GetAIFlags()` trainer Difficulty AI uplifts/downgrades, `FLAG_SMART_TRAINER_AI` compatibility hook, Easy-profile basic AI kill-rate reduction, trainer anti-switch/anti-cheese prediction gates, trainer Protect-cheese retarget gate, Shift/Semi-Shift trainer switching gate, and trainer weakness-berry AI knowledge gate.
- Compatibility rule: when `VAR_TRAINER_AI_PROFILE` is unset/`0`, `GetTrainerAIProfile()` derives from `VAR_GAME_DIFFICULTY`, and `IsSmartTrainerAIEnabled()` keeps honoring `FLAG_SMART_TRAINER_AI`.
- Explicit `TRAINER_AI_PROFILE_VANILLA` keeps trainer data AI flags without Difficulty AI uplifts; explicit Easy/Normal/Hard/Expert affects only migrated Trainer-AI logic; explicit SmartAI or the legacy Smart flag keeps the Smart-Trainer hook active.
- Intentionally not migrated in this block: Wild AI, Raid AI, Trainer IV/EV/friendship/PP power, Trainer Level Scaling, bag/move restrictions, sleep clause, Bad Thoughts, fog, and UI/menu storage.
- Scope: CFRU Trainer-AI profile migration plus Workspace pin/docs only. No UPR-FVX, DPE, Tracker, UI tab, ROM, save, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU trainer level scaling mode split

- Branch: `feature/cfru-trainer-level-scaling-mode`.
- CFRU branch `feature/cfru-trainer-level-scaling-mode` migrates only trainer level-scaling call sites in `src/build_pokemon.c` to `GetTrainerLevelScalingMode()`.
- Migrated paths: `CreateNPCTrainerParty` trainer-scaling enable gate, pseudo-boss level-scaling classification, boss trainer-class level-scaling classification, Hard/Expert generic trainer scaling formulas, and scaling-linked evolution after generic trainer scaling.
- Compatibility rule: when `VAR_TRAINER_LEVEL_SCALING_MODE` is unset/`0`, `GetTrainerLevelScalingMode()` derives from `VAR_GAME_DIFFICULTY`, preserving old Easy/Normal/Hard/Expert trainer-scaling behavior.
- Explicit `TRAINER_LEVEL_SCALING_OFF` now disables the trainer level-scaling path without enabling Easy Difficulty.
- Intentionally not migrated in this block: trainer IV/EV/friendship/PP power, randomizer-only trainer species evolution, bag/move restrictions, AI behavior, Wild/Raid AI, Wild Boss level scaling, and UI/menu storage.
- Scope: CFRU trainer-level-scaling migration plus Workspace pin/docs only. No UPR-FVX, DPE, Tracker, UI tab, ROM, save, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU difficulty split mode helpers

- Branch: `feature/cfru-difficulty-split-mode-helpers`.
- CFRU branch `feature/cfru-difficulty-split-mode-helpers` adds split-mode storage constants and helper plumbing without moving existing Difficulty call sites.
- Added CFRU vars `VAR_TRAINER_LEVEL_SCALING_MODE` at `0x515A` and `VAR_TRAINER_AI_PROFILE` at `0x515B`; no schema var was added because raw `0 = legacy/unset` covers the first migration path.
- Added internal CFRU modes for `DifficultyMode`, `TrainerLevelScalingMode`, and `TrainerAIProfile`.
- Added helpers `GetGameDifficultyMode()`, `GetTrainerLevelScalingMode()`, `GetTrainerAIProfile()`, and `IsSmartTrainerAIEnabled()`.
- Compatibility rule: while the new split vars are `0`, level scaling and AI profile helpers derive from `VAR_GAME_DIFFICULTY`; `IsSmartTrainerAIEnabled()` continues to honor `FLAG_SMART_TRAINER_AI` unless an explicit non-Smart AI profile is set.
- Scope: CFRU helper/storage plumbing plus Workspace pin/docs only. No UPR-FVX, DPE, Tracker, UI tab, ROM, save, emulator state, build artifact, screenshot, raw log, hash, private path, local address, secret, token, or `.env` data was changed or documented.

# Session update - CFRU difficulty split var/mode plan

- Branch: `analysis/cfru-difficulty-split-var-mode-plan`.
- Added `01_docs/analysis/cfru-difficulty-split-var-mode-plan.md` as a source-backed plan for CFRU split-setting vars, modes, helpers, default behavior, and migration rules.
- Var audit result: keep `VAR_GAME_DIFFICULTY` at `0x5157` as the `DifficultyMode` backing store; prefer new expanded vars `0x515A` / `0x515B` for Trainer Level Scaling and Trainer AI Profile; reserve `0x515C` only if a schema marker is actually needed; avoid `0x5152` until optional item restrictions are audited.
- Flag audit result: keep existing `FLAG_SMART_TRAINER_AI` at `0xA0E` as a legacy/script compatibility flag and do not add new flags for split mode storage.
- Migration rule: new mode vars use raw `0 = legacy/unset`, so existing saves with only `VAR_GAME_DIFFICULTY` keep old behavior until the split settings are explicitly written.
- Scope is documentation-only. No CFRU/DPE/UPR-FVX code, ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, local addresses, secrets, tokens, or `.env` data was changed or documented.

# Session update - CFRU difficulty settings UI split design

- Branch: `analysis/cfru-difficulty-settings-ui-split-design`.
- Added `01_docs/analysis/cfru-difficulty-settings-ui-split-design.md` as a source-backed design for splitting current CFRU `VAR_GAME_DIFFICULTY` behavior into `DifficultyMode`, `TrainerLevelScalingMode`, `TrainerAIProfile`, and Randomizer-only settings.
- Exact-symbol search for `VAR_GAME_DIFFICULTY`, `OPTIONS_EASY_DIFFICULTY`, `OPTIONS_NORMAL_DIFFICULTY`, `OPTIONS_HARD_DIFFICULTY`, and `OPTIONS_EXPERT_DIFFICULTY` found runtime uses in `02_external/CFRU-expansion/**`; the same exact-symbol search found no matches in DPE or UPR-FVX.
- Key design outcome: Difficulty should own trainer power, player restrictions, and battle/wild rules; Trainer Level Scaling should own runtime scaling; Trainer AI Profile should own AI flag/choice/switching behavior; Better Movesets and Trainer Evolution remain UPR-FVX Randomizer-only settings.
- Scope is documentation-only. No CFRU/DPE/UPR-FVX code, ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, local addresses, secrets, tokens, or `.env` data was changed or documented.

# Session update - Final Trainer Better Movesets smoke

- Branch: `test/final-trainer-better-movesets-smoke`.
- Documented the final sanitized local Trainer / Better Movesets / Route 22 smoke as `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`.
- Local smoke result: Randomizer save completed without the previous FreedSpace-overlap crash, the UPR-FVX Write/Reload-Audit completed, Route 22 weak Rival protected slot `1` carried the Oak-Lab-Rival starter correctly, slot `0` remained randomizable, and no leading empty move slots were observed.
- Better Movesets interpretation is now explicit: it is not level-up-only, and the Graveler/Hurricane case was explained by the Better-Movesets source audit as a Tutor fallback.
- Scope is documentation-only. No UPR-FVX behavior, CFRU/DPE code, Tracker code, ROMs, saves, builds, screenshots, raw logs, hashes, private paths, local addresses, secrets, tokens, or `.env` data was changed or documented.

# Session update - UPR-FVX Better Movesets source audit

- Branch: `diagnosis/upr-fvx-better-movesets-source-audit` / UPR-FVX `diagnosis/upr-fvx-better-movesets-source-audit`.
- Added a diagnose-only Trainer Better Movesets source audit behind Java system properties.
- The audit records Better-Movesets pool provenance while the existing pool builder runs, then reports selected moves with trainer id, zero-based slot, species, level, chosen move, source categories, and TM/Tutor fallback yes/no.
- Source categories currently reported: `LEVEL_UP`, `PRE_EVOLUTION_LEVEL_UP`, `TM_HM`, `TUTOR`, and `EGG`.
- Scope is diagnostic/test-only. It does not change Better-Movesets scoring, selected move assignment, Trainer Species randomization, CFRU/DPE code, Tracker code, ROMs, saves, builds, screenshots, raw logs, hashes, private paths, local addresses, secrets, tokens, or `.env` data.

# Session update - UPR-FVX Better Movesets pool rules

- Branch: `analysis/upr-fvx-better-movesets-pool-rules`.
- Added `01_docs/analysis/upr-fvx-better-movesets-pool-rules.md` to document source-backed how Trainer Better Movesets builds move pools.
- Key finding: Better Movesets is not strict level-only. It starts from final trainer species level-up moves, then can add pre-evolution, TM/HM, Move Tutor, and egg moves from the current in-memory randomized ROM state before applying ability/stat/STAB/move-synergy heuristics.
- The sanitized Graveler Lv7 `Hurricane / Rock Polish / Defense Curl / Agility` observation is plausible only if the current randomized compatibility/learnset/tutor/TM state makes Hurricane and Agility available; static DPE Graveler does not naturally learn Hurricane or Agility at Lv7.
- Scope is documentation-only. No UPR-FVX behavior, CFRU/DPE code, Tracker code, ROM, save, build, screenshot, raw log, hash, private path, local address, `.local.json`, secret, token, or `.env` data was changed or documented.

# Session update - UPR-FVX runtime trainer source overlap-free save

- Branch: `fix/upr-fvx-runtime-trainer-source-overlap-free` / UPR-FVX `fix/upr-fvx-runtime-trainer-source-overlap-free`.
- Confirmed the save-crash cause in the Runtime Trainer Source save path: after CFRU/DPE `partyFlags=3` rows became 32-byte rows, multiple runtime source rows can expose shared or overlapping old party ranges. The per-row `DataRewriter` then tries to `free()` an overlapping range more than once and `FreedSpace` correctly aborts with `Can't free a space that is already freed`.
- Fix scope: runtime source rows now collect old party ranges before writing, merge overlaps, free each merged old range once, and then repoint/write each runtime row without a second per-row free. The `FreedSpace` safety check remains unchanged.
- Added ROM-free coverage for overlapping CFRU/DPE held-item custom-move runtime source rows.
- Safety boundary: no CFRU/DPE or Tracker files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - UPR-FVX CFRU held-item custom-move rows

- Branch: `diagnosis/upr-fvx-cfru-held-item-custom-moves` / UPR-FVX `diagnosis/upr-fvx-cfru-held-item-custom-moves`.
- Confirmed the source-backed layout mismatch for Trainer rows with held item plus custom moves: classic Gen3 uses `partyFlags=3` as a 16-byte row with item at `+6` and moves at `+8`, while CFRU `TrainerMonItemCustomMoves` is a 32-byte row with ability/nature/IV/EV fields, held item at `+20`, moves at `+22`, and tera type at `+30`.
- Updated UPR-FVX Gen3 trainer load/write diagnostics and CFRU/DPE mode writer/reloader to use the expanded `partyFlags=3` layout while keeping no-item custom rows and held-item default rows on their existing layouts.
- Added ROM-free coverage for classic-vs-CFRU decode divergence and for the CFRU/DPE held-item custom-move writer shape.
- Safety boundary: no CFRU/DPE or Tracker files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - CFRU runtime custom move construction

- Branch: `analysis/cfru-runtime-custom-move-construction`.
- Added `01_docs/analysis/cfru-runtime-custom-move-construction.md` to explain why the UPR-FVX write/reload audit can be clean while CFRU runtime `gBattleMons` still shows leading empty move slots.
- Source-backed finding: CFRU `SET_MOVES` copies custom trainer moves 0-based and exactly; it does not compact `MOVE_NONE` out of slot 0.
- Source-backed finding: CFRU `CreateNPCTrainerParty` skips applying custom trainer moves when `FLAG_POKEMON_RANDOMIZER` is active, unless Battle Facility or temp-disable-randomizer applies.
- Source-backed layout risk: UPR-FVX currently writes/reloads classic 16-byte held-item custom-move rows, while CFRU `TrainerMonItemCustomMoves` is an expanded layout with ability/nature/IV/EV fields, held item, moves, and tera type.
- Scope is documentation-only. No UPR-FVX behavior, CFRU/DPE code, Tracker extension, ROM, save, build, screenshot, raw log, hash, private path, local address, `.local.json`, secret, token, or `.env` data was changed or documented.

# Session update - CFRU runtime trainer vs Tracker slot

- Branch: `analysis/cfru-runtime-trainer-vs-tracker-slot`.
- Added `01_docs/analysis/cfru-runtime-trainer-vs-tracker-slot.md` to separate clean UPR-FVX trainer write/reload evidence from CFRU runtime trainer construction and Tracker live-reader risks.
- Source-backed finding: CFRU `struct BattlePokemon` has `moves[4]` at offset `0x0C` and row size `0x58`, so the extension's move offsets/order are plausible; CFRU `gBattlerPartyIndexes` is `u16[MAX_BATTLERS_COUNT]`, so the prior byte reader made `partySlot` unreliable.
- Hardened `CFRUDPEExtension` diagnostics to read party indexes as 16-bit slots, only display plausible slots `0..5`, and optionally include `gBattleTypeFlags` plus `gTrainerBattleOpponent_A/B` in the active-battle snapshot.
- Scope remains diagnostic/Tracker-extension-only. No UPR-FVX behavior, CFRU/DPE code, Tracker core, NatDexExtension, ROM, save, build, screenshot, raw log, hash, private path, local `.local.json`, secret, token, or `.env` data was changed or documented.

# Session update - CFRU/DPE Tracker party-index snapshot

- Branch: `feature/cfru-dpe-tracker-party-index-snapshot`.
- Extended the workspace-owned `CFRUDPEExtension` active-battle diagnostic snapshot with optional `gBattlerPartyIndexes` reads.
- If local ignored `game-addresses.local.json` provides `Addresses.gBattlerPartyIndexes`, the player-left and opponent-left rows now include zero-based `partySlot[...]` values alongside the existing `gBattleMons` fields.
- If the key is missing or unreadable, the snapshot shows `partySlot[-]` and keeps reading the rest of the battle row without throwing.
- Scope remains Tracker-extension-only. No Tracker-core fork, NatDexExtension change, CFRU/DPE change, UPR-FVX change, ROM, save, build, screenshot, raw log, hash, private path, local `.local.json`, secret, token, or `.env` data was changed or documented.

# Session update - UPR-FVX CFRU/DPE output ROM reload detection

- Branch: `fix/upr-fvx-output-rom-cfru-dpe-reload-detection` / UPR-FVX `fix/upr-fvx-output-rom-cfru-dpe-reload-detection`.
- Fixed the randomized CFRU/DPE output-ROM reload path so expanded mode is not lost when the species-name scan stops before Gen9.
- Source-backed cause: CFRU/DPE mode previously required a fully detected name-count plus specific Gen9 names/BaseStats; the private audit showed the output ROM reloaded with `cfruDpeMode=false`, `loadedSpeciesCount=823`, and `loadedMoveCount=558`, so trainer Species/Move IDs from the expanded pool were then treated as out-of-bounds.
- Fix scope: a second CFRU/DPE table-profile detector now accepts plausible Gen9 BaseStats anchors plus known CFRU/DPE pointer tables and raises the reload Species bound to DPE `NUM_SPECIES` before trainer rows are decoded.
- Scope remains reload detection only. No Rival logic, Better Movesets logic, trainer writer normalization, CFRU/DPE code, Tracker code, ROM, save, build, screenshot, raw log, hash, private path, secret, token, or `.env` data was changed or documented.

# Session update - UPR-FVX output ROM expanded bounds reload

- Branch: `analysis/upr-fvx-output-rom-expanded-bounds-reload` / UPR-FVX `analysis/upr-fvx-output-rom-expanded-bounds-reload`.
- Extended the trainer-load bounds diagnostics for randomized CFRU/DPE output-ROM reloads with sanitized loaded table state.
- New fields include `cfruDpeMode`, `loadedSpeciesCount`, and `loadedMoveCount` alongside the existing raw failing-slot Species/Item/Move values.
- This targets the current private-ROM audit failure where `rawSpecies=1375` and `rawMove=643` should be valid for CFRU/DPE Gen9 counts but are reported out-of-bounds during output-ROM reload.
- Scope remains reload/audit diagnosis only. No Randomizer behavior, CFRU/DPE code, Tracker code, ROM, save, build, screenshot, raw log, hash, private path, secret, token, or `.env` data was changed or documented.

# Session update - UPR-FVX trainer-load raw slot diagnostics

- Branch: `analysis/upr-fvx-trainer-load-slot-raw-values` / UPR-FVX `analysis/upr-fvx-trainer-load-slot-raw-values`.
- Extended the diagnostic-only trainer-load bounds context with sanitized raw values for the failing slot.
- New fields include `rawSpecies` plus `speciesStatus`, optional `rawItem` plus `itemStatus`, `rawMoves=[...]` plus per-slot `moveStatus=[...]`, `expectedLayout`, and `bytesPerSlot`.
- This targets the current private-ROM audit failure where trainer `1`, slot `0`, `custom-moves` layout has in-ROM trainer/party/slot offsets but still crashes with `ArrayIndexOutOfBoundsException`.
- Scope remains reload/audit diagnosis only. No Randomizer behavior, CFRU/DPE code, Tracker code, ROM, save, build, screenshot, raw log, hash, private path, secret, token, or `.env` data was changed or documented.

# Session update - UPR-FVX trainer-load bounds diagnostics

- Branch: `analysis/upr-fvx-trainer-load-bounds-diagnostics` / UPR-FVX `analysis/upr-fvx-trainer-load-bounds-diagnostics`.
- Extended the diagnostic-only Gen3 ROM load path for trainer-load bounds failures.
- When a randomized output ROM crashes during `trainer load`, the private-ROM audit can now report sanitized row context: trainer ID, slot or header, trainer party layout, party flags, party count, and classified trainer/party/slot offset state.
- Expected failure shape is now `Configured randomized ROM could not be loaded during trainer load at trainer=<id> slot=<slot> layout=<layout> ... reason=<ExceptionClass>`.
- Scope remains reload/audit diagnosis only. No Randomizer behavior, CFRU/DPE code, Tracker code, ROM, save, build, screenshot, raw log, hash, private path, secret, token, or `.env` data was changed or documented.

# Session update - UPR-FVX randomized output ROM reload diagnostics

- Branch: `analysis/upr-fvx-output-rom-reload-failure` / UPR-FVX `analysis/upr-fvx-output-rom-reload-failure`.
- Added diagnostic-only phase reporting for Gen3 ROM loading used by the private-ROM trainer write/reload audit.
- Source-backed load phases now distinguish detection, setup, item table load, pokemon data load, evolution load, move table load, pokemon palette load, trainer load, ability table load, and evolution-level estimate.
- The private-ROM audit keeps paths redacted but can now fail with role plus phase, e.g. `Configured randomized ROM could not be loaded during trainer load: ArrayIndexOutOfBoundsException`.
- Scope is reload/audit diagnosis only. No Randomizer behavior, CFRU/DPE code, Tracker code, ROM, save, build, screenshot, raw log, hash, private path, secret, token, or `.env` data was changed or documented.

# Session update - UPR-FVX trainer audit ROM loading hardening

- Branch: `fix/upr-fvx-trainer-audit-report-output` / UPR-FVX `test/trainer-audit-report-output`.
- Hardened `Gen3OakLabRivalRuntimeSourceRomTest` ROM loading for opt-in private-ROM audits.
- `loadGen3Rom` now accepts a role (`single`, `base`, `randomized`) and wraps both `factory.isLoadable(...)` and `romHandler.loadRom(...)` failures with path-free messages.
- Expected failure shape is role-specific and sanitized, e.g. `Configured base ROM could not be loaded: ArrayIndexOutOfBoundsException`.
- Scope is test/diagnostic output only. No Randomizer behavior, CFRU/DPE code, Tracker code, ROM, save, build, screenshot, raw log, hash, private path, secret, token, or `.env` data was changed or documented.

# Session update - UPR-FVX trainer audit property forwarding

- Branch: `fix/upr-fvx-trainer-audit-report-output` / UPR-FVX `test/trainer-audit-report-output`.
- Updated `romio:test` so the opt-in private-ROM audit system properties are forwarded from the Gradle process into the forked test JVM.
- Forwarded properties: `uprfvx.trainerRuntimeSourceBaseRom` and `uprfvx.trainerRuntimeSourceRandomizedRom`.
- Updated the audit plan to note that normal `-D...` invocation should now reach the test executor and that continued `SKIPPED` results should be checked in local Gradle test XML/HTML before interpreting missing reports.
- Scope is Gradle test configuration and documentation only. No Randomizer behavior, CFRU/DPE code, Tracker code, ROM, save, build, screenshot, raw log, hash, private path, secret, token, or `.env` data was changed or documented.

# Session update - UPR-FVX trainer audit report output

- Branch: `fix/upr-fvx-trainer-audit-report-output`.
- Updated the opt-in `Gen3OakLabRivalRuntimeSourceRomTest` diagnostics so report writes are easier to find and harder to miss.
- The diagnostic writer now creates the report directory, writes the report, verifies the file exists and is non-empty, and fails with a relative report path if writing fails.
- The post-randomization private-ROM audit prints a sanitized relative `build/reports/diagnostics/...` report path, summary counts, and core warning lines to test output.
- Scope is test/diagnostic output only. No Randomizer behavior, CFRU/DPE code, Tracker code, ROM, save, build, screenshot, raw log, hash, private path, secret, token, or `.env` data was changed or documented.

# Session update - UPR-FVX trainer write/reload audit

- Branch: `analysis/upr-fvx-trainer-write-reload-audit`.
- Added diagnostic-only UPR-FVX coverage to separate final in-memory trainer state, raw output-ROM trainer rows, and CFRU runtime `gBattleMons` observations for the remaining Route-22 Rival / Better-Movesets symptoms.
- Source-backed diagnostic scope: FRLG raw trainer-party diagnostics now include raw custom move words, post-randomization runtime-source audit reports warn on `MOVE_NONE` in slot 0 with later real moves, and Route-22 protected Rival starter slots are compared against the final Oak-Lab opening Rival starter raw Species.
- Added ROM-free regression coverage proving the audit catches raw `[-/Move/Move/Move]` rows and Route-22 protected starter mismatches. This does not change trainer randomization, Better Movesets, writer normalization, CFRU runtime, or Tracker code.
- Added `08_tests/randomizer/trainer-write-reload-audit-plan.md` with local private-ROM audit instructions and sanitized interpretation rules.
- Safety boundary: no CFRU/DPE or Tracker files were changed; no ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, tool binaries, local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - UPR-FVX actual Route-22 Rival starter slot

- Branch: `fix/upr-fvx-route22-rival-starter-slot-actual`.
- Implemented a follow-up for the actual Route-22 Rival starter carryover failure after local smoke showed Oak Lab Rival starter `Magcargo Lv5` but Route-22 Rival starter context `Arctozolt Lv9`.
- Source-backed trainer IDs and slots: Oak Lab Rival `326/327/328` use starter slot `0`; weak Route 22 `329/330/331` uses protected starter slot `1`; strong Route 22 `435/436/437` uses protected starter slot `5`.
- Source-backed cause: `GameRandomizer` corrected all Rival carryover before the FRLG-specific opening Rival sync, then `makeFirstRivalCarryStarter()` could finalize Oak Lab from the actual FRLG opening trainer source without propagating that final `RIVAL1-x` Species to Route 22.
- Fix scope: when `Rival Carries Starter Through Game` is enabled, FRLG now syncs weak and strong Route-22 protected slots from the final `RIVAL1-x` opening Rival starter after the Oak Lab reapply. Nonstarter slots remain randomizable.
- Added ROM-free regressions for concrete weak Route-22 ID `0x149` / slot `1` and strong Route-22 ID `0x1B3` / slot `5`.
- Safety boundary: no CFRU/DPE or Tracker files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - UPR-FVX Route-22 Rival starter carryover

- Branch: `fix/upr-fvx-route22-rival-starter-carryover`.
- Implemented a focused UPR-FVX fix for the remaining Route-22 Rival carryover issue after final trainer custom-move normalization.
- Source-backed cause: FRLG Rival tags identified Route-22 battles but did not carry explicit protected starter-slot metadata. The generic Rival carryover heuristic can pick the wrong party member when the nonstarter slot is higher level or when runtime FRLG trainer-source rows are loaded without force-slot metadata.
- Fix scope: FRLG Rival tag assignment now applies explicit force starter positions for Oak Lab (`RIVAL1`, slot 0), weak Route 22 (`RIVAL2`, slot 1), and strong Route 22 (`RIVAL7`, slot 5). Runtime FRLG trainer-source rows now receive the same tag metadata.
- Added ROM-free regressions proving the weak Route-22 protected starter slot keeps the lab counter-starter while the nonstarter slot remains randomizable.
- Safety boundary: no CFRU/DPE or Tracker files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - UPR-FVX final trainer move normalization

- Branch: `fix/upr-fvx-final-trainer-move-normalization`.
- Implemented a final UPR-FVX guard for lingering Trainer Better Movesets / trainer custom-move rows with a leading empty slot, e.g. sanitized local `moves[-/Tackle/Growl/Sandattack]`.
- Source-backed cause: PR #170 normalized moves inside the normal Gen3 trainer byte writer, but the trainer custom-move decision still used pre-normalized `TrainerPokemon` state and the Emerald Steven special writer still wrote `tp.getMoves()` directly.
- Fix scope: Gen3 trainer saves now normalize non-reset custom moves before deciding party row width; real moves compact forward, empty slots trail, and all-empty custom rows restore `resetMoves=true`. The Emerald Steven special writer now uses the same normalized/fallback move resolution.
- Added ROM-free regressions for stale original-Pidgey-style moves, all-empty custom moves, Better Movesets empty pool with leading stale moves, and Better Movesets off preserving trainer state.
- Safety boundary: no CFRU/DPE or Tracker files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - UPR-FVX Route-22 Rival final moveslot normalization

- Branch: `fix/upr-fvx-route22-rival-final-moveslots`.
- Implemented a final UPR-FVX move-slot guard after the local follow-up smoke still showed a live `gBattleMons` row like `Decidueye Lv47` with `moves[-/Blizzard/Crunch/Psychocut]`.
- Confirmed source-backed cause for the remaining leading-empty-slot path: `AbstractRomHandler.getMovesAtLevel()` could include `MoveLearnt.move == 0` in a reset-move fallback array, and `Gen3RomHandler.trainerPokemonToBytes()` wrote fallback/custom move arrays exactly as provided.
- Fix scope: `getMovesAtLevel()` skips `MOVE_NONE` placeholders; Gen3 trainer custom-move writing normalizes move slots immediately before writing so real moves are compacted forward and empty slots trail.
- Added ROM-free tests for `MOVE_NONE` placeholder skipping, final move-slot normalization, and a Route-22-style low-level Rival starter staying weak-stage instead of inheriting a later/evolved Rival context.
- Safety boundary: no CFRU/DPE or Tracker files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - UPR-FVX Rival starter / trainer move-slot regression

- Branch: `fix/upr-fvx-rival-starter-moveslot-regression`.
- Implemented a focused UPR-FVX follow-up in `TrainerMovesetRandomizer`: Better Movesets now filters `MOVE_NONE` / null moves before clearing `resetMoves` and writes compact nonzero move slots.
- Added ROM-free `TrainerMovesetDecisionTest` coverage for a non-empty Better-Movesets pool that includes `MOVE_NONE`; expected output now compacts to `[move1, move2, move3, 0]`, not `[0, move1, move2, move3]`.
- Added a Route-22-style Rival guardrail in `TrainerSpecialRulesTest`: after Foe Pokemon randomization and Rival carry reapply, the equal-level last starter slot remains the counter-starter while the nonstarter slot can still be randomized.
- Source-backed interpretation: Route-22 active enemy sightings must identify the party slot before being classified as Rival-starter failure; nonstarter Rival Pokemon remain eligible for Foe Pokemon randomization by design.
- Safety boundary: no CFRU/DPE or Tracker files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - UPR-FVX Trainer Better Movesets empty-pool fix

- Branch: `fix/upr-fvx-trainer-better-movesets-empty-pool`.
- Implemented the UPR-FVX fix in `TrainerMovesetRandomizer`: Better Movesets no longer clears `resetMoves` before a non-empty move pool actually writes move slots.
- `trimMoveList()` now returns the reduced candidate list instead of writing moves directly, so all Better-Movesets writes go through one helper that writes slots and then clears `resetMoves`.
- Added ROM-free `TrainerMovesetDecisionTest` coverage for the empty-pool case and the non-empty-pool case.
- Source-backed fallback audit: `Gen3RomHandler.getMovesAtLevel()` already maps external species numbers through `pokedexToInternal` for CFRU/DPE Gen9 when the moveset map lacks the external key and contains the internal key.
- Safety boundary: no CFRU/DPE or Tracker files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - UPR-FVX Trainer Better Movesets with randomized species

- Branch: `analysis/upr-fvx-trainer-better-movesets-randomized-species`.
- Added source-backed analysis for the local `gBattleMons` smoke where a randomized trainer Pokemon could appear with stale/original moves despite Better Movesets being enabled.
- Key finding: `GameRandomizer` orders Trainer Pokemon randomization before Trainer Better Movesets, so the likely issue is not global ordering. The risky path is `TrainerMovesetRandomizer` setting `resetMoves=false` before proving a non-empty replacement move pool, allowing old `tp.getMoves()` to be written when the pool is empty.
- Rival starter logic remains separately source-backed: opening and through-game Rival starter correction is reapplied after Trainer Pokemon randomization. The current Incineroar smoke needs trainer ID/slot context before it can be called a Rival-starter failure.
- Added a sanitized smoke plan for randomized Trainer Species plus Better Movesets, Rival starter slot checks, and `gBattleMons` validation.
- Safety boundary: no `02_external/**` files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, local addresses, secrets, tokens, or `.env` data were read or documented.

# Session update - CFRU/DPE tracker extension readers

- Branch: `feature/cfru-dpe-tracker-extension-readers`.
- Extended `03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua` so the extension-owned `gBattleMons` debug snapshot includes source-backed `BattlePokemon` fields for type pair, ability, held item, and primary status.
- Source-backed offsets used: `type3 0x18`, `ability 0x20`, `type1/type2 0x21/0x22`, `item 0x2E`, and `status1/status2 0x4C/0x50` from CFRU `include/pokemon.h`.
- Type names use `source-data.json` if future type mappings exist, otherwise CFRU/DPE type constants are used as a local fallback. Ability and item names continue to resolve through committed `source-data.json`.
- Logging remains change-based; `idle/no valid rows` remains a non-error no-battle/transition state. `type3` and raw `status2` are stored as diagnostics but not formatted as pass/fail fields yet.
- Scope: no Tracker-core fork, no NatDexExtension changes, no `Program.readNewPokemon` changes, no memory writes, and no `02_external/**` edits.
- Safety boundary: no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, real addresses, local JSON values, `offsets.ini`, tool binaries, secrets, tokens, or `.env` data were committed or documented.

# Session update - CFRU/DPE battle reader debug view

- Branch: `feature/cfru-dpe-battle-reader-debug-view`.
- Extended `03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua` with an extension-owned active-battle snapshot formatter and change-based debug logging.
- Scope: no Tracker-core fork, no NatDexExtension changes, no memory writes, no `02_external/**` edits, and no stock Tracker screen injection.
- Behavior: valid `gBattleMons` snapshots now log a compact `active-battle=snapshot P:... | E:...` line with species, level, HP/max HP, and move/PP slots. Repeated identical snapshots are not re-logged.
- State transitions: no-battle/transition reads now report `active-battle=idle/no valid rows`, treated as a non-error diagnostic state.
- Updated README and Tracker compat smoke plan with local copy steps and expected sanitized status output.
- Safety boundary: no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, real addresses, local JSON values, `offsets.ini`, tool binaries, secrets, tokens, or `.env` data were committed or documented.

# Session update - CFRU/DPE gBattleMons reader smoke results

- Branch: `test/cfru-dpe-gbattlemons-reader-results`.
- Added `08_tests/randomizer/cfru-dpe-gbattlemons-reader-smoke-results.md`.
- Scope: documentation-only sanitized local smoke results for the extension-owned `gBattleMons` active-battle reader; no code changes.
- Result: `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`.
- Sanitized observations: the installed Tracker loaded the extension, `source-data.json` reported species `1440`, moves `992`, abilities `255`, items `799`, both local ignored manifests loaded, and active-battle rows plausibly reported player-left `Charmander` plus opponent-left `Rattata` / `Pidgey` in local battles.
- Caveat: `active-battle=no valid rows` can appear outside valid battle state or during transitions; stock Tracker UI remains unchanged because v1 only fills `extension.state.activeBattleMons`.
- Safety boundary: no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, real addresses, local JSON values, `offsets.ini`, tool binaries, secrets, tokens, `.env` data, or code changes were committed or documented.

# Session update - CFRU/DPE gBattleMons reader

- Branch: `feature/cfru-dpe-gbattlemons-reader`.
- Extended `03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua` with an extension-owned, read-only `gBattleMons` active-battle diagnostic reader.
- Scope: no Tracker-core fork, no NatDexExtension changes, no memory writes and no `02_external/**` edits.
- Behavior: when local `game-addresses.local.json` provides `gBattleMons`, the extension reads player-left and opponent-left `BattlePokemon` rows using source-backed size `0x58`, maps IDs through `source-data.json`, and stores results in `extension.state.activeBattleMons`.
- Local manifest boundary: `gBattleMons` is required for the reader; `gBattlersCount` is optional for stale-row filtering. Real address values remain local-only and ignored.
- Updated the extension README and Tracker smoke plan with loader plus `gBattleMons` smoke expectations.

# Session update - CFRU/DPE gBattleMons reader design

- Branch: `analysis/cfru-dpe-gbattlemons-reader-design`.
- Added `01_docs/analysis/cfru-dpe-gbattlemons-reader-design.md`.
- Scope: documentation-only design for a minimal extension-owned CFRU/DPE active-battle reader over `gBattleMons`; no code, no Tracker-core fork and no `02_external/**` changes.
- Key recommendation: do not depend on stock `TrackerAPI.getActiveBattlePokemon` for v1 because it returns party objects populated by the vanilla `Program.readNewPokemon` path. Instead, read CFRU `struct BattlePokemon` rows directly into extension-owned state.
- v1 target: require local `gBattleMons`, prefer `gBattlersCount`, use source-backed `BattlePokemon` size `0x58`, and display player-left/enemy-left species, level, HP, moves, PP, ability and item as a read-only diagnostic.
- Safety boundary: no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, `offsets.ini`, real local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - CFRU/DPE Tracker live RAM anchors

- Branch: `analysis/cfru-dpe-tracker-live-ram-anchors`.
- Added `01_docs/analysis/cfru-dpe-tracker-live-ram-anchors.md`.
- Scope: documentation-only source review of why the CFRUDPEExtension can load `source-data`, `game-addresses.local`, and `tracker-overrides.local` while Player/Starter and Wild battle data remain unreadable.
- Key finding: the current failure is primarily live-RAM anchoring plus stock-reader assumptions. Ironmon Tracker needs `pstats`/`gPlayerParty`, `estats`/`gEnemyParty`, `gBattleMons`, and battle-state anchors, while CFRU's direct expanded `struct Pokemon` does not match Tracker's vanilla encrypted Gen III party decoder.
- Recommended v1 direction: validate required local symbol presence without documenting values, then implement a CFRU/DPE active battle reader around `gBattleMons` before full party, bag, or SaveBlock support.
- Safety boundary: no `02_external/**` files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, `offsets.ini`, real local addresses, secrets, tokens, or `.env` data were committed or documented.

# Session update - CFRU/DPE local tracker overrides generator

- Branch: `feature/cfru-dpe-tracker-overrides-local-generator`.
- Added `07_scripts/tracker/generate_cfru_dpe_tracker_overrides_local.py` to generate ignored `CFRUDPEExtension/data/tracker-overrides.local.json`.
- Scope: local Tracker layout-smoke helper only. The generator emits source-backed layout candidates for recognized `Program`, `PokemonData`, and `MoveData` override sections and no ROM/RAM/runtime/build addresses.
- Generated categories include `BattleMove`, `BattlePokemon`, `BaseStats`, and Trainer header sizes/offsets. Bag item slot/pocket candidates and CFRU-only layout risks are documented in manifest metadata, not emitted as effective overrides.
- Caveat remains: TrackerAPI accepts tracker override JSON, but local smoke must verify whether imported keys update the effective nested `*.Addresses` tables consumed by Tracker read paths.
- Safety boundary: no `02_external/**` files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, secrets, tokens, `.env` data, `offsets.ini`, or generated local override JSON were committed.

# Session update - CFRU/DPE local address generator

- Branch: `feature/cfru-dpe-address-local-generator`.
- Added `07_scripts/tracker/generate_cfru_dpe_game_addresses_local.py` to generate ignored `CFRUDPEExtension/data/game-addresses.local.json` from a local read-only `offsets.ini`.
- Scope: local Tracker smoke helper only. The generator omits the input path from JSON, writes no committed real addresses, and reports missing live RAM/SaveBlock/bag symbols as warnings.
- Recognized symbol targets include CFRU/DPE table and name symbols such as `gBattleMoves`, `gMoveNames`, `gAbilityNames`, `gTrainers`, `gLevelUpLearnsets`, `gTrainerClassNames`, `gTypeNames`, `gBaseStats`, `gSpeciesInfo`, `gSpeciesNames`, and `sTMHMMoves` when present.
- Updated the extension README and Tracker smoke plan with local-only generation and install steps.
- Safety boundary: no `02_external/**` files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, secrets, tokens, `.env` data, `offsets.ini`, or generated local address JSON were committed.

# Session update - CFRU/DPE Tracker manifest path resolution

- Branch: `feature/cfru-dpe-extension-manifest-loader-smoke`.
- Fixed `CFRUDPEExtension.lua` manifest path resolution for real Tracker installs outside the workspace.
- The extension now resolves `data/` relative to the loaded `CFRUDPEExtension.lua` file via `debug.getinfo(1, "S").source`, then falls back to `FileManager.getExtensionsFolderPath()` if needed.
- Local install shape is now documented as `Lua/extensions/CFRUDPEExtension.lua` plus `Lua/extensions/data/source-data.json` and optional `.local.json` files.
- Scope remains loader/path smoke only. No Tracker-core fork, NatDexExtension change, `02_external/**` edit, ROM, save, emulator state, build, screenshot, raw log, hash, private path, `offsets.ini` data or real runtime address was added.

# Session update - CFRU/DPE Tracker manifest loader smoke

- Branch: `feature/cfru-dpe-extension-manifest-loader-smoke`.
- Extended `03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua` so startup reads committed `data/source-data.json` and logs source-derived counts.
- Local manifest filenames are now explicit and ignored: `data/game-addresses.local.json` and `data/tracker-overrides.local.json`.
- Loader behavior: missing local manifests are reported as missing without failing extension startup; present local manifests are passed to `TrackerAPI.loadGameSettingsFromJson` and `TrackerAPI.loadTrackerOverridesFromJson` with explicit paths and logged return status.
- Scope remains loader smoke only. No Tracker-core fork, NatDexExtension change, `02_external/**` edit, ROM, save, emulator state, build, screenshot, raw log, hash, private path, `offsets.ini` data or real runtime address was added.

# Session update - CFRU/DPE Tracker layout overrides

- Branch: `analysis/cfru-dpe-tracker-layout-overrides`.
- Added `01_docs/analysis/cfru-dpe-tracker-layout-overrides.md`.
- Scope: documentation-only source review of CFRU/DPE struct layouts and Ironmon Tracker override fields. No ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, `offsets.ini` data, real addresses or `02_external/**` edits were used.
- Key finding: `BattleMove`, `BattlePokemon`, `BaseStats`, `Trainer` header fields, simple TrainerMon row sizes, bag `ItemSlot`, and bag pocket counts have source-derived layout candidates suitable for example manifests.
- Key risk: CFRU `struct Pokemon` is a direct expanded layout and does not match the vanilla encrypted party substruct model that stock `Program.readNewPokemon` decodes. Player/enemy party correctness likely needs a CFRU-aware reader or metadata-backed extension logic, not only offset overrides.
- Tracker override caveat: inspected Tracker consumers read nested `*.Addresses` tables, while `GameSettings.importTrackerOverridesFromJson` must be locally validated to prove the example JSON shape updates those effective fields.
- Updated `tracker-overrides.example.json` with safe candidate status, explicit non-address policy, bag layout candidates and validation notes.

# Session update - CFRU/DPE Tracker source-data generator

- Branch: `feature/cfru-dpe-source-data-generator`.
- Added `07_scripts/tracker/generate_cfru_dpe_source_data.py`.
- Generated `03_tools/tracker-extensions/CFRUDPEExtension/data/source-data.json` from CFRU/DPE source headers only.
- Scope: counts and ID mappings only. No ROMs, saves, emulator states, builds, raw logs, hashes, private paths, `offsets.ini` data, real addresses, Tracker-core changes, NatDexExtension changes or `02_external/**` edits.
- Current generated counts: species `1440`, moves `992`, abilities `255`, items `799`.
- Warnings document DPE/CFRU item-count conflict (`799` vs `779`) and duplicate/alias constants.
- Added `03_tools/tracker-extensions/CFRUDPEExtension/README.md` with generator usage and current extension/data boundaries.

# Session update - Tracker Lua source inventory

- Branch: `analysis/tracker-lua-source-inventory`.
- Added `01_docs/analysis/tracker-lua-source-inventory.md`.
- Scope: documentation-only inventory of existing source inputs for a future CFRU/DPE/Gen9 Ironmon Tracker Lua extension. No implementation, generator, real manifest data, ROMs, builds, saves, emulator states, raw logs, hashes or private paths were added.
- Key finding: high-priority v1 inputs are Tracker `TrackerAPI.lua`/`CustomCode.lua`/`GameSettings.lua`/`Program.lua`, NatDexExtension as a pattern, CFRU/DPE ID headers, CFRU struct headers, CFRU/DPE source tables, and the current `CFRUDPEExtension` skeleton/example JSONs.
- Local `offsets.ini` files exist under CFRU and DPE and contain useful symbol classes for table/name addresses, but they are ignored/generated local artifacts. They must remain local-only and are not sufficient by themselves for live party/battle RAM and SaveBlock support.
- Updated the Tracker compat smoke plan with the source-inventory boundary and next implementation order.
- Safety boundary: no `02_external/**` files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, secrets, tokens or `.env` data were read or documented.

# Session update - CFRU/DPE Tracker manifest source map

- Branch: `analysis/cfru-dpe-tracker-manifest-source-map`.
- Added `01_docs/analysis/cfru-dpe-tracker-manifest-source-map.md`.
- Scope: documentation-only source map for CFRU/DPE/Gen9 Tracker manifest values; no ROMs, builds, saves, emulator states, raw logs, hashes, private paths or generated artifacts were used.
- Key finding: species, move, ability counts, many enum mappings, layout candidates and source-declared pointer slots are commit-safe as source-derived data. Actual target addresses for party, battle, trainer, saveblock and repointed tables remain local override / build-symbol / metadata-table values.
- Updated the CFRU/DPE Tracker extension example JSONs with source-derived count candidates, pointer-slot metadata and layout-candidate notes while keeping all real address fields as TODOs.
- Item-count caveat: DPE item headers imply 799 IDs while CFRU constants imply 779 IDs; a generator must reconcile the final source of truth before committing item mappings.
- Safety boundary: no `02_external/**` files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, secrets, tokens or `.env` data were read or documented.

# Session update - CFRU/DPE Tracker extension skeleton

- Branch: `feature/cfru-dpe-tracker-extension-skeleton`.
- Added the first workspace-owned external Tracker extension skeleton under `03_tools/tracker-extensions/CFRUDPEExtension/`.
- Files added: `CFRUDPEExtension.lua`, `data/game-addresses.example.json`, `data/tracker-overrides.example.json`, and `data/source-data.example.json`.
- Scope: minimal external Ironmon Tracker extension skeleton plus manifest prototypes only. No Tracker-core fork, no NatDexExtension modification, no `02_external/**` changes.
- Behavior: the skeleton defines metadata and hooks, prepares a manual CFRU/DPE profile path, and only loads real non-example local manifests named `data/game-addresses.json` and `data/tracker-overrides.json` if the user provides them.
- Documentation updated with local install shape, skeleton-only smoke expectations, required future manifest values, and current limitations.
- Safety boundary: no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, secrets, tokens or `.env` data were read or documented.

# Session update - CFRU/DPE Tracker extension design

- Branch: `analysis/cfru-dpe-tracker-extension-design`.
- Added `01_docs/analysis/cfru-dpe-tracker-extension-design.md`.
- Scope: documentation-only design for a future external `CFRUDPEExtension.lua` after the NatDexExtension pattern, without Tracker-core fork or implementation.
- Key recommendation: use a two-artifact approach: a small read-only Tracker extension plus source-derived CFRU/DPE profile manifests for addresses, sizes, offsets, counts and species/move/ability/item mappings.
- v1 target: manual profile activation first, then prove species/move/ability/item data plus player party and live enemy battle data. Static trainer-party data remains caveated because CFRU/randomizer runtime construction can change the final battle Pokemon.
- Updated `08_tests/randomizer/ironmon-tracker-cfru-dpe-compat-plan.md` with the extension-design follow-up and minimal smoke focus.
- Safety boundary: no `02_external/**` files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, secrets, tokens or `.env` data were read or documented.

# Session update - Tracker memory API map

- Branch: `analysis/tracker-memory-api-map`.
- Added `01_docs/analysis/tracker-memory-api-map.md` and `08_tests/randomizer/ironmon-tracker-cfru-dpe-compat-plan.md`.
- Scope: documentation-only source review of Ironmon Tracker, NatDexExtension `dev_new`, and CFRU/DPE/Gen9 memory/data assumptions.
- Key finding: stock Ironmon Tracker relies on vanilla Gen 3 ROM detection, address JSON, static Pokemon/move/ability/item/trainer tables, and vanilla party/battle/trainer layouts. CFRU/DPE/Gen9 breaks those assumptions through expanded species/moves/items/abilities, hidden ability, Tera/Gigantamax fields, and richer trainer-party/runtime build logic.
- NatDexExtension is documented as a useful extension pattern, not a drop-in CFRU/DPE adapter: it activates on `Memory.read32(0x08000170) == 1258` and expects CyanSMP64/NatDex-specific pointer metadata.
- Recommendation: prefer a small CFRU/DPE Tracker extension or source-derived address/data manifest over forcing stock NatDexExtension.
- Note: the requested prior files `01_docs/analysis/ironmon-tracker-cfru-dpe-compat.md` and `08_tests/randomizer/ironmon-tracker-cfru-dpe-compat-plan.md` were not present at task start; the compat plan was created in this block.
- Safety boundary: no `02_external/**` files were changed; no ROMs, saves, emulator states, builds, screenshots, raw logs, hashes, private paths, tool binaries, secrets, tokens or `.env` data were read or documented.

# Session update - Tracker source references

- Branch: `setup/tracker-source-references`.
- Added workspace documentation for the new read-only source submodules `02_external/Ironmon-Tracker` and `02_external/NatDexExtension`.
- Ironmon Tracker is documented on branch `main` at commit `c450ecaee2d8131a2789bb656e3be792a93712fb`.
- NatDexExtension is documented as the `dev_new` source on commit `a94b8844800308248bb5090b6c36c8b2d7e5d7b9`.
- BizHawk remains a local tool target only: no BizHawk source submodule, release zip, AppImage, build output or binary is part of the repo.
- `02_external/Ironmon-Tracker/ironmon_tracker/TrackerAPI.lua` is now documented as the central Tracker API analysis source; this corresponds to the project shorthand `IronmonTrackerAPI.lua`.
- `.gitmodules` was synchronized so existing CFRU/DPE/UPR/reference mappings remain present while the two tracker references are added.
- Safety boundary: no ROMs, saves, emulator states, builds, tool binaries, screenshots, raw logs, hashes, private paths, secrets, tokens or `.env` data were read or documented.

# Session update - CFRU Expert AI isolation

- Branch: `analysis/cfru-expert-ai-isolation`.
- Added `01_docs/analysis/cfru-expert-ai-isolation.md`.
- Scope: documentation-only source review explaining why CFRU Expert Difficulty can look smarter than `FLAG_SMART_TRAINER_AI` v1/v2 without being a clean Smart-AI-only option.
- Key finding: for ordinary trainer battles, Expert's `GetAIFlags` uplift is effectively the same conservative trainer path as Smart Trainer AI v2: trainers without `AI_SCRIPT_CHECK_GOOD_MOVE` gain `AI_SCRIPT_SEMI_SMART`. Expert does not globally add `AI_SCRIPT_CHECK_GOOD_MOVE` to regular trainers.
- Interpretation: if Expert looked smarter in local smoke, the likely source-backed causes are trainer-build/level/stat side effects, context differences, or situational Expert-only behavior rather than a better generic trainer AI flag mix.
- v3 recommendation: do not copy Expert wholesale; keep `VAR_GAME_DIFFICULTY` Normal and prefer either a targeted Sand Attack / utility scoring adjustment or a deeper Vanilla/NatDex `AI_CheckViability` / `AI_TryToFaint` source-port.
- Safety boundary: no CFRU/DPE code changes, no ROMs, saves, emulator states, builds, logs, screenshots, hashes, tool binaries, private paths, secrets, tokens or `.env` data were read or documented.

# Session update - Smart AI patch source verification

- Branch: `analysis/smart-ai-patch-source-verification`.
- Added `01_docs/analysis/smart-ai-patch-source-verification.md`.
- Scope: documentation-only verification of the original tom-overton FireRed/LeafGreen Smart-AI source branch, CyanSMP64 NatDex randomizer Smart AI integration, and CFRU v1/v2 comparison.
- Key finding: tom-overton `smart-ai` functional source change is trainer-data-only: `src/data/trainers.h` upgrades trainer `aiFlags` to `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY`; no Battle-AI scoring scripts or command code changed.
- NatDex randomizer finding: Gen3 `smartAiMode` sets the trainer AI flag byte with `|= 0x07`, which maps in local NatDex FireRed to `CHECK_BAD_MOVE`, `CHECK_VIABILITY`, and `TRY_TO_FAINT`.
- CFRU comparison: v1 was only numerically close to `0x07`; CFRU runtime bit 2 is `AI_SCRIPT_CHECK_GOOD_MOVE` / `AIScript_Positives`, not Vanilla/NatDex `TRY_TO_FAINT`. v2 remains the safer current smoke candidate with `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`.
- Documentation cross-links updated in `01_docs/analysis/ironmon-smart-ai-patch-map.md`, `01_docs/analysis/smart-ai-scoring-comparison.md`, and `01_docs/references/source-index.md`.
- Safety boundary: no ROMs, saves, emulator states, builds, screenshots, raw logs, tool binaries, patch assets, private paths, secrets, tokens or `.env` data were read or documented. No external repos were cloned.

# Session update - CFRU Smart Trainer AI v2 utility-spam reduction

- Branch: `fix/cfru-smart-trainer-ai-v2-reduce-utility-spam`.
- CFRU commit: `992d3dc6a8db33b3c633dd4d504c40fb6efe37d1` (`fix: reduce smart trainer ai utility spam`).
- Scope: reduced only the `FLAG_SMART_TRAINER_AI` hook in CFRU `GetAIFlags`.
- CFRU v1 was technically active in local smoke, but showed utility/Accuracy-drop spam. Sanitized local observation: an opposing Pidgey/Taubsi used Sand Attack/Sandwirbel four times in a row despite Tackle being available.
- CFRU v2 changes the trainer flag uplift from `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE` to `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`.
- Behavior boundary: no `VAR_GAME_DIFFICULTY`, wild/raid AI, trainer IV/EV/friendship/PP, level-scaling, bag/move restriction, battle-rule, Option Menu, Settings NPC, or `build_pokemon.c` change was made.
- Documentation updated in `01_docs/analysis/smart-ai-scoring-comparison.md` and `08_tests/randomizer/cfru-smart-trainer-ai-smoke-plan.md` so the next smoke targets conservative CFRU-native Smart Trainer AI without `CHECK_GOOD_MOVE`.
- Safety boundary: no ROMs, saves, emulator states, builds, logs, screenshots, tool binaries, private paths, hashes, secrets, tokens or `.env` data were read or documented.

# Session update - Smart AI move scoring comparison

- Branch: `analysis/smart-ai-scoring-comparison`.
- Added `01_docs/analysis/smart-ai-scoring-comparison.md`.
- Scope: documentation-only comparison of NatDex/Ironmon Smart AI `0x07` move scoring vs. CFRU `FLAG_SMART_TRAINER_AI` v1 scoring.
- Key finding: CFRU v1 is numerically close to NatDex/Ironmon `0x07`, but not behavior-identical. CFRU `AI_SCRIPT_CHECK_GOOD_MOVE` runs `AIScript_Positives`, a broader utility/status scoring path; NatDex `0x07` runs classic `AI_CheckBadMove`, `AI_CheckViability`, and `AI_TryToFaint`.
- Sand Attack explanation: CFRU does not penalize Accuracy-down when it is technically possible, and `AIScript_Positives` can boost it through `GoodIdeaToLowerAccuracy` plus class-based `IncreaseStatusViability`; this can outscore non-KO damage moves.
- Updated `08_tests/randomizer/cfru-smart-trainer-ai-smoke-plan.md` so future smoke treats Sand Attack/status-heavy behavior as a scoring question, not automatically as hook failure or exact Ironmon equivalence.
- Safety boundary: no CFRU/DPE source changes, no ROMs, saves, emulator states, builds, logs, screenshots, tool binaries, private paths, secrets, tokens or `.env` data were read or documented.

# Session update - CFRU Smart Trainer AI smoke confirmation

- Branch: `feature/cfru-smart-trainer-ai-smoke-script`.
- Added a visible confirmation to the existing Pallet smoke activation path.
- CFRU script scope: `EventScript_Pallet_FatGuy` still sets `0xA0E` for `FLAG_SMART_TRAINER_AI`, then shows `Smart Trainer AI enabled.` through the Pallet script string table.
- Behavior boundary: no `VAR_GAME_DIFFICULTY`, Battle AI, trainer-build, wild/raid AI, Option Menu, Settings NPC, toggle, or `build_pokemon.c` change was made.
- Documentation updated in `08_tests/randomizer/cfru-smart-trainer-ai-smoke-plan.md` so local flag-on smoke expects the visible confirmation before sampled trainer battles.
- Safety boundary: no ROMs, saves, emulator states, builds, logs, screenshots, tool binaries, private paths, secrets, tokens or `.env` data were read or documented.

# Session update - CFRU Smart Trainer AI smoke activation

- Branch: `feature/cfru-smart-trainer-ai-smoke-script`.
- Implemented the minimal source-backed test activation path for `FLAG_SMART_TRAINER_AI`.
- CFRU script scope: `02_external/CFRU-expansion/assembly/overworld_scripts/Pallet_town.s` / `EventScript_Pallet_FatGuy` now sets `0xA0E` as a local smoke activation for `FLAG_SMART_TRAINER_AI`.
- Rationale: `EventScript_Pallet_FatGuy` is an existing Pallet Town debug/test-style script wired in `eventscripts`, already granting test Pokemon and showing `gText_TestScript`; it is not a final Settings NPC, Option Menu, or player UX path.
- Behavior boundary: `VAR_GAME_DIFFICULTY` remains unchanged; no trainer-build strength, level scaling, wild/raid AI, bag/move restriction, battle-rule, Expert anti-cheese, shift-switch, or `build_pokemon.c` changes were made.
- Documentation updated in `08_tests/randomizer/cfru-smart-trainer-ai-smoke-plan.md` with flag-off vs. flag-on local smoke instructions.
- Safety boundary: no ROMs, saves, emulator states, builds, logs, screenshots, tool binaries, private paths, secrets, tokens or `.env` data were read or documented.

# Session update - CFRU Smart Trainer AI activation smoke plan

- Branch: `test/cfru-smart-trainer-ai-activation-plan`.
- Added `08_tests/randomizer/cfru-smart-trainer-ai-smoke-plan.md`.
- Scope: documentation-only activation and smoke-test plan for CFRU `FLAG_SMART_TRAINER_AI 0xA0E`; no CFRU/DPE code changes.
- Recommendation: first local smoke should use an early script-set activation for a dedicated test profile, with a debug setter only for local A/B convenience if needed; Settings NPC, Option Menu and Randomizer-profile wiring should wait until behavior is smoke-confirmed.
- Smoke matrix: Normal Difficulty + flag off vs. Normal Difficulty + flag on, checking trainer move-choice improvement and explicitly confirming no IV/EV/friendship/PP, level, wild/raid, bag/move restriction, battle-rule, Expert anti-cheese or shift-switch side effects.
- Safety boundary: no ROMs, saves, emulator states, builds, logs, screenshots, tool binaries, private paths, secrets, tokens or `.env` data were read or documented.

# Session update - CFRU Smart Trainer AI runtime flag

- Branch: `feature/cfru-smart-trainer-ai-mode`.
- Implemented v1 Smart Trainer AI in CFRU source with project-local `FLAG_SMART_TRAINER_AI 0xA0E`.
- CFRU commit: `eb1f3bff3fef83b46999e0513a7598b6bde601b8` (`feat: add smart trainer ai runtime flag`).
- Code scope: `src/config.h` defines the runtime flag; `src/Battle_AI/ai_master.c` adds `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE` to trainer battle AI flags when the flag is set.
- Intended behavior: close to NatDex/Ironmon `aiFlags |= 0x07`, while leaving `VAR_GAME_DIFFICULTY` unchanged and avoiding trainer-build, level-scaling, wild/raid, bag/move restriction, battle-rule, Expert anti-cheese and shift-switch changes.
- Documentation updated in `01_docs/analysis/cfru-smart-ai-source-port-map.md`; the flag currently has no UI/NPC/option-menu/randomizer-profile wiring.
- Risk to test: `AI_SCRIPT_CHECK_GOOD_MOVE` activates stronger CFRU AI paths than `AI_SCRIPT_SEMI_SMART` alone, so v1 needs focused battle smoke before broader use.

# Session update - CFRU Smart AI flag mapping

- Branch: `feature/cfru-smart-trainer-ai-mode`.
- Updated `01_docs/analysis/cfru-smart-ai-source-port-map.md` with the CFRU-side mapping for the NatDex/Ironmon `0x07` Smart-AI finding.
- Key finding: CFRU does not expose `AI_SCRIPT_CHECK_VIABILITY` and `AI_SCRIPT_TRY_TO_FAINT` as runtime battle-AI script names. Runtime CFRU bits 0, 1 and 2 are `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_SEMI_SMART`, and `AI_SCRIPT_CHECK_GOOD_MOVE`.
- Recommendation: for closest NatDex/Ironmon `0x07` behavior, v1 should OR trainer flags with `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`; `AI_SCRIPT_SEMI_SMART` alone remains a safer CFRU-native uplift but is not the closest `0x07` equivalent.
- Boundary: no `02_external/**` files were changed. No ROMs, saves, builds, emulator states, tool binaries, external downloads, resets, stashes, cleans or checkouts were used.
- Note: `01_docs/analysis/ironmon-smart-ai-patch-map.md` was not present on this feature branch, so the mapping used the user-provided `0x07` context plus local CFRU source.

# Session update - Ironmon / NatDex Smart AI patch map

- Branch: `analysis/ironmon-smart-ai-patch-map`.
- Added `01_docs/analysis/ironmon-smart-ai-patch-map.md`.
- Scope: documentation-only source-backed map of the Ironmon/Super-Kaizo/NatDex Smart-AI patch/randomizer behavior for comparison against the CFRU `FLAG_SMART_TRAINER_AI` design.
- Key finding: the locally available CyanSMP64 NatDex randomizer implements Gen3 Smart AI Mode by OR-ing each trainer AI flag byte with `0x07`, which maps in the local FireRed NatDex source to `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_CHECK_VIABILITY`, and `AI_SCRIPT_TRY_TO_FAINT`.
- Comparison: the CFRU `FLAG_SMART_TRAINER_AI` approach is directionally close if it only extends trainer AI flags and keeps `VAR_GAME_DIFFICULTY` Normal; a pure `AI_SCRIPT_SEMI_SMART` lift is safer but weaker than the NatDex/Ironmon `0x07` evidence.
- Boundaries: no ROMs, BPS/IPS/UPS patches, randomizer release zips, builds, saves, emulator states, private paths, secrets, tokens or `.env` data were downloaded, read or documented.
- No code changes were made.

# Session update - CFRU Smart AI source-port map

- Branch: `analysis/cfru-runtime-options-map`.
- Added `01_docs/analysis/cfru-smart-ai-source-port-map.md`.
- Scope: documentation-only source-port map for a future Smart Trainer AI option that does not set `VAR_GAME_DIFFICULTY` to Hard or Expert.
- Key finding: the cleanest isolatable CFRU AI behavior is the Hard/Expert trainer branch in `GetAIFlags`, which adds `AI_SCRIPT_SEMI_SMART` when a trainer does not already have `AI_SCRIPT_CHECK_GOOD_MOVE`.
- Recommendation: prefer a future `VAR_TRAINER_AI_MODE` if tiering is possible, or `FLAG_SMART_TRAINER_AI` for a single binary toggle; keep wild AI separate from trainer AI.
- Non-goal documented: do not port trainer IV/EV/friendship/PP buffs, level scaling, bag or player-move restrictions, battle-rule changes, wild/raid construction changes, or Expert anti-cheese into the baseline Smart Trainer AI option.
- Known dirty CFRU submodule state remains local and unmodified. No `02_external/**` changes were made, staged, reset, stashed or committed.
- No ROMs, saves, emulator states, builds, tool binaries, private paths, secrets, tokens or `.env` files were read or documented.

# Session update - CFRU Smart AI only design

- Branch: `analysis/cfru-runtime-options-map`.
- Added `01_docs/analysis/cfru-smart-ai-only-design.md`.
- Scope: documentation-only follow-up explaining why CFRU `VAR_GAME_DIFFICULTY` is too invasive to label as Smart AI for the Randomizer/Ironmon target.
- Key finding: the true AI hooks are mainly `GetAIFlags`, `OpponentHandleChooseMove`, `WildMonIsSmart`, `ShouldDoAIShiftSwitch`, switch prediction, and Expert anti-cheese helpers; the same runtime difficulty also changes trainer IV/EV/friendship/PP, level scaling, bag/move restrictions, battle rules, wild encounters, and raid behavior.
- Recommendation: keep runtime difficulty Normal for the baseline randomizer profile unless a deliberate Hard-mode profile is requested; design any "Smart AI only" behavior as a separate future CFRU source-port with trainer and wild controls separated.
- Known dirty CFRU submodule state remains local and unmodified. No `02_external/**` changes were made, staged, reset, stashed or committed.
- No ROMs, saves, emulator states, builds, tool binaries, private paths, secrets, tokens or `.env` files were read or documented.

# Session update - CFRU game difficulty map

- Branch: `analysis/cfru-runtime-options-map`.
- Added `01_docs/analysis/cfru-game-difficulty-map.md`.
- Scope: source-backed documentation of CFRU `VAR_GAME_DIFFICULTY 0x5157` effects across Normal/Easy/Hard/Expert and comparison against a narrower Ironmon/NatDex Smart-AI-style patch.
- Key finding: `VAR_GAME_DIFFICULTY` is broader than Smart AI. It affects battle AI, trainer IV/EV/friendship/PP strength, trainer level scaling, player item/move restrictions, wild/raid edge cases, and selected battle calculations/rules.
- The source uses `OPTIONS_NORMAL_DIFFICULTY`, `OPTIONS_EASY_DIFFICULTY`, `OPTIONS_HARD_DIFFICULTY`, and `OPTIONS_EXPERT_DIFFICULTY`; no `DIFFICULTY_*` symbols were found in the requested source search.
- DPE Gen9 had no relevant `VAR_GAME_DIFFICULTY` logic in the requested search.
- Known dirty CFRU submodule state remains local and unmodified: `02_external/CFRU-expansion/src/config.h` has uncommitted config edits, including local `FLAT_EXP_FORMULA` enabled. This is documented as balance-relevant but not directly `VAR_GAME_DIFFICULTY`-specific.
- No ROMs, saves, emulator states, builds, tool binaries, private paths, secrets, tokens or `.env` files were read or documented.
- No CFRU/DPE code was changed, staged, reset, stashed or committed.

# Session update - Rival starter consistency smoke plan

- New branch: `analysis/rival-starter-consistency-smoke`.
- Added `08_tests/randomizer/rival_starter_consistency_smoke.md`.
- Scope: documentation-only Rival Starter Consistency Smoke Plan for Oak-Lab Rival counter-starter, Route 22 Rival carry consistency, Rival non-starter randomization interpretation, and runtime-source evidence boundaries.
- Existing evidence is sufficient for a focused local smoke plan: `192_starter_rival_sync_pass.md`, `207_rival_counter_starter_and_combined_visual_smoke.md`, `208_combined_trainer_visual_runtime_smoke.md`, `212_gen_limit_special_form_item_smoke.md`, runtime-source evidence `202` through `204`, `fvx_feature_test_status_matrix.tsv`, and `fvx-feature-decision-matrix.md`.
- The plan defines tested settings, expected log/ingame observations, PASS/FAIL/BLOCKED criteria, sanitized evidence requirements and caveats.
- No ROMs, builds, output ROMs, raw logs, private paths, hashes, screenshots, saves, emulator states, secrets, tokens or `.env` data were read or documented.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion were made.

# Session update - FVX compatibility implementation report

- New branch: `analysis/fvx-compat-implementation-report`.
- Added `01_docs/randomizer/fvx-compat-implementation-report.md`.
- Scope: documentation-only technical report explaining the UPR-FVX CFRU/DPE compatibility implementation path through compat commit `8349daf5ce005f0defc5674cbc3a3468f009218c` / PR #152.
- The report summarizes architecture, affected code paths, PR/evidence references, feature-by-feature fixes, remaining caveats, data-quality vs compatibility separation, and a recommended next evaluation matrix.
- No UPR-FVX, CFRU/DPE or workspace code was changed.
- No ROMs, builds, output ROMs, saves, emulator states, screenshots, full logs, private paths, hashes, secrets, tokens or `.env` data were read or documented.
- No P1 promotion was made.

# Session update - Gen Limit / Special Form / Mechanic Item final smoke

- New branch: `randomizer/sync-gen-limit-special-form-item-final-smoke`.
- Synced `02_external/upr-fvx` to merged UPR-FVX compat commit `8349daf5ce005f0defc5674cbc3a3468f009218c` after the Gen-Limit, Special-Form, Trainer-Class-Sprite-Sync, Oak-Lab-Rival, Mechanic-Item and Trainer-Held-Item fix chain through PR #152.
- Updated `08_tests/randomizer/212_gen_limit_special_form_item_smoke.md` with sanitized local final-smoke evidence.
- Local evidence: Gen-Limit 1-9 infrastructure works; Gen1-only and Gen1-6 log smokes looked correct; Gen7/8/9 Intro Mon no longer crashes and supports valid visual-table candidates; Mega/GMax/Regional/Irregular/Special-form filtering works in latest local checks; Evolutionary Relatives remain an explicit cross-gen-family override; Regional forms are not pulled in by Evolutionary Relatives unless Regional Forms across Gen Limit is enabled.
- Additional local evidence: Trainer Class Sprite Sync is now GUI-exposed and should be enabled when Trainer Class Names are randomized; Oak-Lab Rival counter-starter is preserved independently of Rival Carries Starter Through Game; mechanic item filtering uses source-backed CFRU/DPE categories for Mega/Z/Dynamax-GMax items; Trainer Held Items / Sensible Items run without the earlier missing-pool or missing-movepool NPEs; no current crash was observed in the latest GUI smoke; no current issue was observed with Pokemon special-form filtering after latest local checks.
- Status impact: Gen Limit / Special Form / Mechanic Item Exclusions are `PASS_TARGETED_LOG_VISUAL_SMOKE_WITH_CAVEATS`.
- Caveats: targeted local smoke only, no full playthrough; no full held-item distribution audit; Plates/Drives/Memories/Nectars are categorized but do not yet have separate user-facing policies; Static Script/Gift/NPC item sources remain caveated if they do not run through randomizer item replacement pools; custom/future form encodings outside documented CFRU/DPE identity blocks remain audit-required.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, ROM hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Misc Tweaks behavior smoke

- New branch: `randomizer/sync-misc-tweaks-behavior-smoke`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #127 commit `155fac0b33474f6ed5b3fbaed7dd9bf24b4e1315`.
- This pin includes PR #125 for CFRU/DPE BPRE Running Shoes misc tweaks, PR #126 for CFRU/DPE BPRE Catching Tutorial species mapping and PR #127 for Fast Egg Hatching missing-`BreedingInfo` handling.
- Added `08_tests/randomizer/210_misc_tweaks_behavior_smoke.md` with sanitized local evidence.
- Local evidence: Fastest Text pass, Randomize PC Potion pass, Ban Lucky Egg likely pass / no issue observed, Run Without Running Shoes pass, Running Shoes Indoors pass, Randomize Catching Tutorial pass with no question-mark sprite/name, Fast Egg Hatching no longer crashes on missing `BreedingInfo` and output loads.
- Reusable TMs and Forgettable HMs are treated as CFRU-provided behavior and should not be duplicated by the UPR-FVX stable profile.
- Status impact: Misc Tweaks are `PASS_TARGETED_BEHAVIOR_SMOKE_WITH_CAVEATS`.
- Caveats: Fast Egg Hatching is crash-free randomization/output-load evidence, not full hatch-cycle proof; Ban Lucky Egg remains likely pass without stronger dedicated evidence; no full playthrough and no P1 promotion.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, ROM hash, screenshot, save, emulator state, secret, token or `.env` data was documented.

# Session update - Type Effectiveness battle smoke

- New branch: `randomizer/record-type-effectiveness-battle-smoke`.
- Added `08_tests/randomizer/211_type_effectiveness_battle_smoke.md` with sanitized local battle-smoke evidence.
- Local evidence: Type Effectiveness was tested in battle, effectiveness behavior looked appropriate and no battle crashes were reported.
- Status impact: Type Effectiveness is `PASS_TARGETED_BATTLE_SMOKE_WITH_CAVEATS`.
- Caveats: targeted battle smoke only, not a full type-chart matchup matrix, not a full playthrough and not a P1 promotion.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, ROM hash, screenshot, save, emulator state, secret, token or `.env` data was documented.

# Session update - Graphics/Palettes visual smoke

- New branch: `randomizer/sync-graphics-palettes-visual-smoke`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #124 commit `0eb815418470fa1ac000695b95d09cb084338dca`.
- This pin includes UPR-FVX PR #123 for Gen3/CFRU-DPE palette output writes and PR #124 for expanded trainer logging bounds/fallbacks.
- Added `08_tests/randomizer/209_graphics_palettes_visual_smoke.md` with sanitized local evidence.
- Sanitized local evidence: `Pokemon Palettes: Randomized/Changed`; CFRU-DPE palette copy save completed with `normalPaletteWriteAttempts=841`; Palette Audit reported `sampledCount=21`, `normalChangedCount=21`, `shinyChangedCount=0`, `unchangedCount=0`; Charmander, Squirtle, Caterpie, Pikachu and Blissey had `normalChangedFromBase=yes`; changed palettes were visually observed; final run had no `Error during logging`.
- Status impact: Graphics/Palettes targeted visual/audit smoke is locally passed with caveats. Normal palette output writes are evidenced for sampled species; shiny coverage remains caveated by `shinyChangedCount=0`.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Graphics/Palettes smoke settings prep

- New branch: `randomizer/prepare-graphics-palettes-smoke`.
- Prepared local ignored manual settings input `05_builds/randomizer-smoke/settings/manual/graphics_palettes_smoke.rnqs`.
- Source profile: existing generated `05_builds/randomizer-smoke/settings/exact-coverage-batch-09/risk_graphics_palettes_visual.rnqs`.
- Intended scope: isolated Graphics/Palettes visual smoke for `FVX-GFX-001` through `FVX-GFX-004` only.
- Excluded from the profile scope: Wild, Foe, Items, Misc, TypeEffectiveness/type chaos, Custom Player Graphics and Character-to-Replace manual graphics.
- No RNQS byte-patching was done; the manual input reuses a generated UPR-FVX settings-profile artifact.
- No ROM run by Codex, no output ROM, no smoke evidence update and no P1 promotion were made.

# Session update - Wild encounter output audit sync

- New branch: `randomizer/sync-wild-encounter-output-audit`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #118 commit `ed692d07bfc81405706f2b94fda06639426e6a75`.
- PR #118 adds an opt-in Wild Encounter Base-vs-Output Audit for Gen3/FRLG/CFRU-DPE.
- Status impact: Wild Encounter Base-vs-Output Audit is available as a diagnostic-only report; it does not change writer or randomizer behavior.
- Scope: modeled Gen3 base `WildPokemon` table path. The report compares local Base-ROM and Output-ROM slots with map/area identifier where available, encounter type, slot index, base species, output species and `changedFromBase`, plus total/changed/unchanged/changed percentage summary.
- CFRU/DPE special/runtime wild sources remain follow-up if ingame behavior and the modeled-table audit diverge.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Combined trainer visual runtime smoke

- Follow-up branch: `randomizer/update-route22-rival-starter-evidence`.
- Corrected `08_tests/randomizer/208_combined_trainer_visual_runtime_smoke.md` after additional sanitized local evidence: Player starter Charmander, Oak-Lab Rival starter Squirtle and Route-22 Rival starter Squirtle.
- Route-22 Rival non-starter Pokemon observed: Silvally Lv9.
- Interpretation: `Rival Carries Starter Through Game` protects/corrects the Rival starter slot only; non-starter Rival Pokemon remain eligible for Foe Pokemon randomization.
- Combined trainer visual runtime smoke remains `PASS_WITH_CAVEATS` because it is targeted visual/runtime smoke, not a full playthrough or all-starter-choice matrix.
- No crash/freeze/garbled sprite was observed. No P1 promotion follows from this correction.

- New branch: `randomizer/record-combined-trainer-visual-runtime-smoke`.
- Added `08_tests/randomizer/208_combined_trainer_visual_runtime_smoke.md` with sanitized local evidence.
- Combined trainer visual runtime smoke status: `PASS_WITH_CAVEATS`.
- Sanitized local evidence: Intro Mon was visibly randomized; player starter was Charmander; Oak-Lab Rival starter was Squirtle; Route 22 Rival starter was Squirtle; Route 22 Rival sprite was randomized and consistent with the Oak-Lab Rival sprite; Viridian Forest trainer sprites were randomized; no crash/freeze/garbled sprite was observed.
- No P1 promotion follows from this smoke.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented.

# Session update - Rival counter starter and combined visual smoke

- New branch: `randomizer/sync-rival-counter-starter-and-visual-smoke`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #117 commit `5983011752273e00c402e25cc1ae1a9baca110f1`.
- Added `08_tests/randomizer/207_rival_counter_starter_and_combined_visual_smoke.md` with sanitized local evidence.
- PR #117 preserves/corrects the Rival counter-starter after Foe Pokemon randomization and prevents invalid Intro Mon species `0` writes in the extended CFRU/DPE BPRE pool.
- Sanitized local evidence: combined visual Rival test fixed; Intro Mon was visibly Blissey and Species `0` regression was gone; Player Charmander -> Rival Squirtle; Trainer Class Sprite Sync remained visually okay from prior checks with Viridian Forest per-trainer classes/sprites and Rival grouped sprite/class consistency.
- No crash, freeze or garbled sprite was reported.
- Caveat: targeted visual smoke only, not a full playthrough, global runtime-source proof, broad trainer-category sweep or P1 promotion.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Trainer Class Sprite Sync final smoke

- New branch: `randomizer/sync-trainer-class-sprite-sync-final`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #116 commit `36dd431d059bc69eb1bee3311200e28c872c6cc9`.
- Updated `08_tests/randomizer/206_trainer_class_sprite_sync.md` with final sanitized local Trainer Class Sprite Sync evidence.
- `MODE-TRAINER-CLASS-SPRITE-SYNC` is locally smoke-confirmed for the targeted visual path.
- Semantics: `Randomize Trainer Names` remains personal-name-only; without `MODE-TRAINER-CLASS-SPRITE-SYNC`, `Randomize Trainer Class Names` remains legacy/textlabel-only; with Sync enabled, class label, `trainerClass` and visible `trainerPic` follow the class assignment.
- Regular trainers use per-trainer class/sprite assignments. Rival/Friend rows use grouped class/sprite consistency across appearances. Runtime-source rows are included in sync where eligible.
- Sanitized local evidence: Viridian Forest Bug Catcher classes were randomized per trainer; Rival kept the first randomized sprite across later appearances; other sampled trainers appeared aligned; no garbled sprite or crash was reported.
- Caveat: this is targeted visual smoke only, not a full playthrough or global route/category sweep.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Trainer Class Sprite Sync

- New branch: `randomizer/sync-trainer-class-sprite-sync`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #111 commit `4805a5a930bc97203199816222465c76de2f2150`.
- Added `08_tests/randomizer/206_trainer_class_sprite_sync.md`.
- PR #111 adds opt-in `MODE-TRAINER-CLASS-SPRITE-SYNC` for Gen 3 Trainer Class Sprite Sync.
- Semantics after the pre-merge correction: `Randomize Trainer Names` remains separate and changes only trainer personal names; without `MODE-TRAINER-CLASS-SPRITE-SYNC`, `Randomize Trainer Class Names` remains legacy/textlabel-only; with Sync enabled, Sprite Sync follows the Trainer Class Names `oldClassId -> targetClassId` mapping and sets `trainerClass` plus `trainerPic` to match the target class.
- Special target classes such as Rival, Gym Leader, Elite Four and Champion are not globally excluded. Target classes without an observed valid `trainerPic` are skipped.
- Sanitized evidence available before this workspace sync: a regular trainer battle started, the visible sprite changed, and the log showed class/sprite sync markers. The earlier Regular-only semantic mismatch was corrected before merge.
- Status impact: Trainer Class Sprite Sync is available as an opt-in feature, but final local smoke on the merged PR #111 pin is still required before stronger support claims.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Intro Mon visual source fix smoke

- New branch: `randomizer/sync-intro-mon-visual-source-fix`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #109 commit `a9bb4a5f201c5078ec02fe1f2f8417695448afe9`.
- PR #109 fixes the CFRU/DPE Gen9 BPRE Intro Mon visual mismatch by syncing the Nidoran female `PokemonFrontImages` and `PokemonNormalPalettes` entries to the selected intro species' asset pointers when Intro Mon is randomized.
- Added `08_tests/randomizer/205_intro_mon_visual_source_fix_smoke.md`.
- Previous sanitized local finding: known FRLG Intro sources changed from Nidoran female to Hitmontop, but the visible ingame Oak intro sprite stayed Nidoran female.
- Sanitized local smoke after PR #109: the visible Oak intro sprite changed away from Nidoran female, with no crash, freeze or garbled sprite observed.
- Status impact: `FVX-GEN-003` / Intro Mon visual mismatch is locally fixed for the targeted CFRU/DPE Gen9 BPRE smoke.
- Caveat: this is targeted ingame smoke, not a full playthrough or global visual-source proof. No P1 promotion was made.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented.

# Session update - Intro Mon visual source diagnostics sync

- New branch: `randomizer/sync-intro-mon-visual-source-diagnostics`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #107 commit `a7e098a5158d824b1ddec62a286f2a6ffafce8e4`.
- PR #107 adds an opt-in Intro Mon Visual-Source diagnostic for known FRLG Intro Mon literals and pointers, with optional Base-ROM vs randomized Output-ROM comparison for local use.
- Setting semantics are documented: `No Random Intro Mon` is the negative GUI option; internally `randomizeIntroMon=true` is the active Randomize Intro Mon path.
- `MODE-INTRO-RANDOM` sets `randomizeIntroMon=true`; `MODE-NO-RANDOM-INTRO` and `FVX-GEN-003` set `randomizeIntroMon=false`.
- Status impact: Intro Mon Visual-Source-Diagnose ist verfuegbar, aber sie ist Diagnose-only. Sie bestaetigt keine sichtbare Ingame-Aenderung und enthaelt keinen Writer-/Offset-Fix.
- Local follow-up should run the opt-in report with private Base/Output ROMs and share only sanitized candidate source names, offsets, decoded species, `changedFromBase` yes/no and observed visible Intro Mon label.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Runtime source trainer randomization smoke evidence refresh

- New branch: `randomizer/sync-runtime-source-trainer-randomization-smoke`.
- `02_external/upr-fvx` remains pinned to merged UPR-FVX PR #106 commit `5bb1d853f132095922be2aceef55af2878192b85`; no pin rewind is introduced.
- Added `08_tests/randomizer/204_runtime_source_trainer_randomization_smoke.md`.
- PR #105 makes generic `RUNTIME-SOURCE` trainers randomizer-eligible by treating them as regular trainers while preserving known Rival 2/Brock special tags; the evidence applies to that fix and remains compatible with PR #106 post-audit tooling.
- Sanitized local evidence confirms Viridian Forest runtime-source trainer IDs `531/532` are loaded, randomized and saved: `531` loaded/raw party is `[Klawf Lv7, Togepi Lv8]`, `532` loaded/raw party is `[Eiscue Lv7, Rampardos Lv7, Aron Lv7]`, and both loaded/raw comparisons match.
- Ingame smoke observed the formerly vanilla Metapod/Caterpie Viridian Forest trainer showing Eiscue.
- Runtime-source audit on the randomized output ROM reported `trainer runtime source audit mode=unloaded-valid-parties` with `total=0`, equivalent to no remaining valid runtime-not-loaded rows in that focused audit view.
- Additional sanitized examples: Rival 2 trainer IDs `329/330/331` show randomized parties, and Brock trainer ID `414` shows `[Drifloon Lv12, Growlithe Lv14]`.
- Status impact: strict runtime-source sync plus `RUNTIME-SOURCE` Trainer Pokemon randomization is locally confirmed for the targeted Viridian Forest `531/532` case; loaded-mismatch, invalid-pointer, empty-party, out-of-range rows and full playthrough coverage remain follow-up scope.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Runtime trainer post-randomization audit sync

- New branch: `randomizer/sync-runtime-trainer-post-audit`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #106 commit `5bb1d853f132095922be2aceef55af2878192b85`.
- PR #106 adds an opt-in Pre/Post Runtime-Trainer-Audit for comparing a private base ROM with a private randomized output ROM.
- The audit reports valid script-referenced runtime trainer rows deduped by `trainerId`, including base/output raw parties, loaded output party, output classification, changed-from-base state and loaded/raw comparison.
- Status impact: Pre/Post Runtime-Trainer-Audit is available for local verification that valid runtime trainers were loaded, randomized and written back, but this workspace sync documents audit-only behavior.
- Scope boundary: no new writer, sync or randomizer behavior is added by this workspace PR; no ROM run, output ROM, private path, hash, full log, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.
- Local next evidence should compare the user's Base-ROM and randomized Output-ROM through the opt-in audit and share only sanitized trainer IDs, party summaries, classifications, warning markers and pass/fail observations.

# Session update - Runtime source trainer randomization smoke

- New branch: `randomizer/sync-runtime-source-trainer-randomization`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #105 commit `c0d8e33f3547020c6fd2fe5baffbc80ec93f9197`.
- PR #105 makes generic `RUNTIME-SOURCE` trainers randomizer-eligible by treating them as regular trainers while preserving known Rival 2/Brock special tags.
- Added `08_tests/randomizer/203_runtime_source_trainer_randomization_smoke.md`.
- Sanitized local evidence confirms Viridian Forest runtime-source trainer IDs `531/532` are randomized and saved: `531` loaded/raw party is `[Klawf Lv7, Togepi Lv8]`, `532` loaded/raw party is `[Eiscue Lv7, Rampardos Lv7, Aron Lv7]`, and both loaded/raw comparisons match.
- Ingame smoke observed the formerly vanilla Metapod/Caterpie Viridian Forest trainer showing Eiscue.
- Status impact: Trainer/Foe runtime-source strict sync plus randomizer eligibility is locally confirmed for Viridian Forest `531/532`; loaded-mismatch, invalid-pointer, empty-party and out-of-range rows remain follow-up scope.
- Scope boundary: no ROM run by Codex, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Strict runtime trainer source sync

- New branch: `randomizer/sync-strict-runtime-trainer-source-sync`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #104 commit `6dcda7e499cd3e22319c447c7d7df9ddbd67de60`.
- PR #104 implements strict auto-sync for FRLG/CFRU-DPE `trainerbattle` runtime-source `TrainerData` rows that the audit classifies as `VALID_RUNTIME_NOT_LOADED`.
- Strict sync is intentionally constrained to valid in-bounds TrainerData rows with valid party pointers, party size 1..6, readable raw parties and plausible first raw species. Invalid-pointer, empty-party, out-of-range, loaded-mismatch and likely false-positive rows remain diagnosis/follow-up scope.
- Status impact: Trainer/Foe remains CLI-log-clean, and the strict runtime sync is now merged and pinned, but local private-ROM audit plus ingame smoke is still required before stronger support claims.
- Viridian Forest trainer IDs `531/532` should be covered by strict sync if local audit still classifies them as `VALID_RUNTIME_NOT_LOADED`.
- Scope boundary: no ROM run, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No UPR-FVX/CFRU/DPE code change was made in this workspace PR. No P1 promotion was made.

# Session update - Runtime trainer source audit sync

- New branch: `randomizer/sync-runtime-trainer-source-audit`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #103 commit `14c1c8c0c6960f1b4a0cf0246a1117628ca1f3cc`.
- PR #103 adds an opt-in global FRLG Trainer Runtime Source Audit to the existing runtime-source diagnostics.
- The audit is enabled locally through system property `uprfvx.trainerRuntimeSourceAudit` or env `UPRFVX_TRAINER_RUNTIME_SOURCE_AUDIT`.
- Supported audit modes are `all`, `unloaded-valid-parties`, `loaded-mismatch` and `invalid`.
- The audit dedupes script-referenced trainer IDs and reports script offsets, battle types, trainer/party pointer metadata, raw/loaded party summaries and classification.
- Status impact: Runtime Trainer Source Audit is available, but it is audit-only. No automatic sync/write behavior, no SaveTrainers expansion and no normal Randomizer behavior change are documented in this workspace sync.
- Further fixes for additional vanilla-looking trainers must wait for sanitized local audit evidence proving specific valid in-game runtime rows.
- Scope boundary: no ROM run, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Runtime trainer party fix sync

- New branch: `randomizer/sync-runtime-trainer-party-fix`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #102 commit `eabbcd7eccb1703f98000f85669d969f516e1247`.
- PR #102 fixes the confirmed CFRU/DPE FireRed Trainer Pokemon runtime-source mismatch for Rival 2 trainer IDs `329/330/331` and Brock trainer ID `414` by loading and saving validated raw `TrainerData` runtime-source rows that sit outside the normal loaded trainer count.
- Foe Trainer remains CLI-log-clean from exact coverage; the specific Rival 2 and Brock runtime-source fix is now merged and pinned.
- Ingame smoke is still required before stronger Foe Trainer support claims.
- Further vanilla-looking trainer battles should only extend the runtime-source sync after targeted, redacted runtime-source evidence confirms valid raw `TrainerData` rows and party pointers.
- Scope boundary: no ROM run, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No UPR-FVX/CFRU/DPE code change was made in this workspace PR. No P1 promotion was made.

# Session update - Trainer runtime source diagnostics sync

- New branch: `randomizer/sync-trainer-runtime-source-diagnostics`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #100 commit `87bba797620dd2043f02c11c67f7b752a7238a00`.
- PR #100 adds No-ROM/synthetic diagnostics for mapping FRLG `trainerbattle` script trainer IDs to `TrainerData` rows, party pointers and first raw party species.
- Added `08_tests/randomizer/202_trainer_runtime_source_diagnostics_sync.md`.
- Status impact: Foe Trainer remains CLI-log-clean from exact coverage, but ingame status is partial/caveated because second Rival, Brock and selected normal trainers may use runtime sources that differ from the logged/written trainer list.
- The next evidence needed is local-only and sanitized: affected battle label, trainer ID if visible, party summary if known, and redacted runtime-source diagnostic rows showing whether script/runtime and logged/written `TrainerData` match.
- Scope boundary: no ROM run, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Settings profile variant overlays sync

- New branch: `randomizer/sync-settings-profile-variant-overlays`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #99 commit `4c8e7394a230e6e8471977036be268c80883ac0b`.
- PR #99 adds exact No-ROM `settings-profile` `MODE-*` overlays for Foe Pokemon modes, Wild replacement/location modes, TypeEffectiveness modes and Intro Mon toggles.
- Updated the coverage manifest and generator/runner docs so `feature_overlays` can carry Feature IDs or `MODE-*` overlay IDs.
- Added disabled opt-in exact variant rows for Foe modes, Wild locations, TypeEffectiveness modes and Intro random/no-random.
- Documented `MODE-GEN-LIMIT-1-9*` variants as unsupported because current Settings cannot encode Gen 8/9 restrictions or GMax exclusion.
- Scope boundary: no ROM run, output ROM, full log, private path, hash, screenshot, save, emulator state, secret, token or `.env` data was documented. No P1 promotion was made.

# Session update - Exact coverage batches 03-18

- New branch: `randomizer/sync-exact-coverage-batches-03-18`.
- Added `08_tests/randomizer/201_exact_coverage_batches_03_18.md`.
- Sanitized local exact-coverage Batch 03 through 18 CLI log-smoke/helper results: Batches 03 through 17 processed 165 generator-capable exact/cumulative/mode profiles.
- All Batch 03 through 17 PASS profiles had 0 bad markers and 0 warnings; Batch 18 confirmed 4 Gen-Limit `MODE-*` overlays fail as expected because they are unsupported by the current Settings format.
- Updated `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` for affected generator-capable Feature IDs across TM/Tutor, Wild, Foe, General/Traits, Starters/Statics/Trades, Moves, Graphics/Palettes, Misc, Types, cumulative coverage and exact Foe/Wild/Type/Intro mode overlays.
- Preserved caveats and non-promotions: Graphics/Palettes remain `PASS_LOG_WITH_CAVEAT` with visual smoke needed, sensible Trainer Held Items remains caveated because of previous NPE history, Intro Mon needs visual confirmation, Gen-Limit-1-9 `MODE-*` overlays remain unsupported by Settings format, Special-Wild remains separate, `FVX-SST-001` and `FVX-GFX-005/006` remain manual/unsupported, and `FVX-MOVE-006` remains out-of-scope for CFRU/DPE Gen9.
- Updated the FVX progress dashboard snapshot/package status and completed-diagnosis references without shortening the full Feature-ID list.
- Scope boundary: no ROM paths, hashes, full logs, output paths, screenshots, saves, emulator states, secrets, tokens or `.env` data were documented. No UPR-FVX/CFRU/DPE code change and no P1 promotion were made.

# Session update - Exact coverage batch 02 items

- New branch: `randomizer/sync-exact-coverage-batch-02-items`.
- Added `08_tests/randomizer/200_exact_coverage_batch_02_items.md`.
- Sanitized local exact-coverage Batch 02 Item CLI log-smoke result: dry-run disabled, 13 profiles processed.
- All 13 profiles passed with 0 bad markers and 0 warnings.
- Updated `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` only for `FVX-ITEM-001` through `FVX-ITEM-010`.
- The updated Item rows cite `200 exact coverage batch 02 items`, keep ingame follow-up required, and do not promote P1.
- Existing Item caveats remain visible: Required-TM forcing and supported/special shop coverage still need item-specific ingame follow-up.
- Updated the FVX progress dashboard snapshot/diagnosis references without shortening the full Feature-ID list.
- Scope boundary: no ROM paths, hashes, full logs, output paths, screenshots, saves, emulator states, secrets, tokens or `.env` data were documented. No UPR-FVX/CFRU/DPE code change and no P1 promotion were made.

# Session update - Exact coverage batch 01

- New branch: `randomizer/sync-exact-coverage-batch-01`.
- Added `08_tests/randomizer/199_exact_coverage_batch_01.md`.
- Sanitized local exact-coverage Batch 01 CLI log-smoke result: dry-run disabled, 19 profiles processed.
- All 19 profiles passed with 0 bad markers and 0 warnings.
- Updated `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` only for the requested Feature IDs: `FVX-TRAIT-017`, `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-009`, `FVX-SST-010`, `FVX-SST-012`, `FVX-FOE-005`, `FVX-FOE-006`, `FVX-FOE-007`, `FVX-FOE-009` and `FVX-FOE-011`.
- The updated rows cite `199 exact coverage batch 01`, keep ingame follow-up required, and do not promote P1.
- Updated the FVX progress dashboard snapshot/diagnosis references without shortening the full Feature-ID list.
- Scope boundary: no ROM paths, hashes, full logs, output paths, screenshots, saves, emulator states, secrets, tokens or `.env` data were documented. No UPR-FVX/CFRU/DPE code change and no P1 promotion were made.

# Session update - Coverage CLI profile matrix pass

- New branch: `randomizer/sync-coverage-profile-matrix-pass`.
- Added `08_tests/randomizer/198_cli_profile_matrix_coverage_run.md`.
- Sanitized local coverage-generated `.rnqs` CLI profile matrix result: dry-run disabled, 14 profiles processed.
- PASS profiles with 0 bad markers and 0 warnings: `00_baseline`, `01_traits_full`, `02_starters_statics_trades_full`, `03_moves_movesets_full`, `04_foe_base`, `04_foe_held_items_basic`, `05_wild_full`, `06_tm_tutor_full`, `07_items_full` and `08_types_full`.
- UNEXPECTED_PASS profiles with 0 bad markers and 0 warnings: `04_foe_held_items_sensible_expected_fail`, `09_graphics_palettes`, `10_misc_tweaks` and `11_special_wild`.
- Updated `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` only for rows exactly enabled by the executed coverage profile overlays; unexpected-pass rows remain `PASS_LOG_WITH_CAVEAT`.
- Updated the FVX progress dashboard snapshot/package summaries without shortening the full Feature-ID list.
- Scope boundary: no ROM paths, hashes, full logs, output paths, screenshots, saves, emulator states, secrets, tokens or `.env` data were documented. No UPR-FVX/CFRU/DPE code change and no P1 promotion were made.

# Session update - FVX profile coverage audit

- New branch: `randomizer/profile-coverage-audit`.
- Added `08_tests/randomizer/fvx_profile_coverage_plan.md`.
- Added `08_tests/randomizer/cli_profile_matrix.coverage.example.tsv`.
- Audited the current generated settings profiles against all 130 FVX Feature IDs.
- Result: the current 14-profile matrix is valid as broad tab/cumulative log-smoke evidence, but not as exact per-feature coverage.
- Identified Feature IDs that need single/variant profiles instead of related broad-profile assumptions: `FVX-TRAIT-017`, several Starter/Static variants, several Foe variants and Item Shuffle/Even/Shop-Shuffle variants.
- Extended `07_scripts/randomizer/generate_settings_profiles_from_matrix.sh` so manifest rows can use an optional comma-separated `feature_overlays` column and call `settings-profile --enable <FEATURE_ID>`.
- Updated `07_scripts/randomizer/run_cli_profile_matrix.sh` to tolerate the optional generator-only column.
- Superseded by UPR-FVX PR #99: TypeEffectiveness exact mode coverage can now use `MODE-TYPE-*` overlays for Random, Random-Balanced, Keep-Identities and Inverse.
- Scope boundary: no ROMs, output ROMs, full logs, private paths, hashes, screenshots, saves, emulator states, secrets, tokens or `.env` data were documented. No UPR-FVX/CFRU/DPE code change and no P1 promotion were made.

# Session update - Generated CLI profile matrix results

- New branch: `randomizer/sync-cli-profile-matrix-results`.
- Added `08_tests/randomizer/197_cli_profile_matrix_generated_run.md`.
- Sanitized local generated `.rnqs` CLI profile matrix result: 14 profiles processed.
- All profiles produced CLI log smoke pass or unexpected pass.
- Bad markers were 0 for all profiles; warnings were 0 for all profiles.
- Unexpected passes: `04_foe_held_items_sensible_expected_fail`, `09_graphics_palettes`, `10_misc_tweaks` and `11_special_wild`.
- Updated `08_tests/randomizer/fvx_feature_test_status_matrix.tsv`: expected-pass profile rows are raised to log-pass where appropriate, and unexpected-pass profile rows remain `PASS_LOG_WITH_CAVEAT`.
- Updated the FVX progress dashboard snapshot and package/status summaries without shortening the full feature list.
- Scope boundary: no ROM paths, hashes, full logs, output paths, screenshots, saves, emulator states, secrets, tokens or `.env` data were documented. No UPR-FVX/CFRU/DPE code change and no P1 promotion were made.

# Session update - Settings profile generator sync

- New branch: `randomizer/sync-settings-profile-generator`.
- Prerequisite verified: current `main` is at `c8ea5fddf6f73a63604b0dccb3fb11b64dbfda31`, and UPR-FVX PR #98 is merged into `origin/compat/firered-gen9-cfru-dpe`.
- Synced `02_external/upr-fvx` to merged UPR-FVX PR #98 commit `81fa4cf35af48bce19996e4581f1e4a688ebfa3b`.
- Added `07_scripts/randomizer/generate_settings_profiles_from_matrix.sh`.
- Added `08_tests/randomizer/196_settings_profile_generator_sync.md`.
- Updated the CLI profile matrix documentation: generated profiles now use `UPR-FVX.jar settings-profile` instead of saved GUI-only `.rnqs` files.
- The new workspace wrapper accepts `--upr-dir`, `--base-settings`, `--profile-manifest` and `--output-settings-dir`, and calls the UPR-FVX helper once per enabled profile.
- Scope boundary: No-ROM settings generation only. Codex did not read a ROM, run randomization, create output ROMs, commit real logs or document private paths/hashes/screenshots.
- No UPR-FVX code change was made in this workspace PR, and no P1 promotion was made.

# Session update - FVX feature test status matrix

- New branch: `randomizer/fvx-feature-test-status-matrix`.
- Prerequisite verified: PR #268 is merged and this branch starts from current `main` at `1c2ca82c7cc96191c6ab57f198956542e95e44d6`.
- Added `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` with all 130 Feature IDs from `01_docs/randomizer/fvx-progress-dashboard.md`.
- Added `08_tests/randomizer/195_fvx_feature_test_status_matrix.md` explaining the matrix purpose, status model, CLI profile relationship and update rules.
- The TSV maps every Feature ID to a CLI profile, test mode, log status, ingame status, caveat/blocker/evidence fields and next step.
- This historical matrix-update block captured the sanitized evidence at the time; later updates now supersede Palettes/Graphics and Misc Tweaks with targeted smoke caveats, while Trainer Class Names remains textlabel-only, trainer held Sensible Items remains expected-fail and Special-Wild remains out-of-scope.
- Dashboard remains the human overview; TSV is the machine-readable worklist for future CLI profile matrix updates.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made.

# Session update - CLI profile matrix pipeline

- New branch: `randomizer/settings-profile-matrix-pipeline`.
- Prerequisite verified: PR #267 is merged and this branch starts from current `main` at `204184e4d5aab834fa2a3725fa76f341995cd042`.
- Added `07_scripts/randomizer/run_cli_profile_matrix.sh` to execute multiple saved FVX settings profiles through the existing CLI log smoke helper and write a sanitized aggregate summary.
- Added `07_scripts/randomizer/generate_cli_smoke_profiles.sh` as a manifest scaffold generator only.
- Added `08_tests/randomizer/194_cli_profile_matrix_pipeline.md` and `08_tests/randomizer/cli_profile_matrix.example.tsv`.
- Technical decision: FVX `.rnqs` settings are versioned Base64 plus CRC/checksum state, so workspace shell/Python scripts must not byte-patch settings. The matrix currently uses saved local settings profiles; a future UPR-FVX helper or Java helper should generate derived profiles through FVX `Settings` APIs.
- `cli_log_smoke_pipeline.sh` now records warning marker counts in sanitized reports.
- Codex tested only help/syntax/dry-run paths. No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made.

# Session update - CLI log smoke pipeline

- New branch: `randomizer/cli-log-smoke-pipeline`.
- Added `07_scripts/randomizer/cli_log_smoke_pipeline.sh` as a repo-safe local helper for UPR-FVX CLI smoke runs.
- Added `08_tests/randomizer/193_cli_log_smoke_pipeline.md` to document the local-only CLI log smoke flow, pass criteria and sanitized handoff format.
- Scope: the helper wraps `UPR-FVX.jar cli` with `-l`, writes only a sanitized summary report and scans local stdout/detailed logs for fatal or known bad markers.
- The helper supports `--dry-run` so repository checks can validate the wrapper without reading a ROM or creating an output ROM.
- Current UPR-FVX pin remains `51d52a03235664154549105003dadfb45c76d0d0`.
- Stable Visual Profile and Starter Pokemon/Oak-Lab first Rival sync remain the current smoke-passed baseline; Trainer Class Names remains textlabel-only, Special-Wild remains out-of-scope and `Rival Carries Starter Through Game` remains untested.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made.

# Session update - Starter/Rival sync pass

- New branch: `randomizer/sync-starter-rival-sync-pass`.
- Synced merged UPR-FVX PR #97 into the workspace pin.
- `02_external/upr-fvx` now pins merge commit `51d52a03235664154549105003dadfb45c76d0d0`.
- Root cause recorded: the real FireRed/CFRU-DPE Oak-Lab Rival uses raw `TrainerData` party rows that did not run through the normal loaded trainer list. PR #96 hit that raw source, and PR #97 corrected the slot projection to `[328, 326, 327]`.
- Counter-slot rule preserved: player slot 0 -> starter slot 1, player slot 1 -> starter slot 2 and player slot 2 -> starter slot 0.
- Added `08_tests/randomizer/192_starter_rival_sync_pass.md`.
- Sanitized local Starter/Rival smoke evidence: starter slots were Groudon, Fearow and Mudbray; the player chose Groudon; expected Rival was Fearow; observed Rival was Fearow.
- Starter Pokemon passed for the Oak-Lab first Rival smoke. No vanilla fallback, same-starter bug, crash or softlock was observed.
- Stable Visual Profile can now optionally include Starter Pokemon for local sampling.
- `Rival Carries Starter Through Game` remains a separate, not-tested full-rival path.
- Known exclusions remain: Trainer Class Names visual mismatch and Special-Wild out-of-scope.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made in this workspace sync.

# Session update - Stable Visual Profile smoke

- New branch: `randomizer/sync-stable-visual-profile-smoke`.
- Workspace PR #262 is treated as merged baseline for the GUI Working Settings Matrix.
- Added `08_tests/randomizer/191_stable_visual_profile_smoke.md`.
- Sanitized local Stable Visual Profile smoke passed after the Working Settings Matrix sync.
- ON profile: Wild Standard/Fallback, Trainer Pokemon core, Pokemon Movesets -> Random completely, Trainer Movesets, Trainer Names, Field Items basic, Pokemon Abilities, TM/HM Compatibility, TM Moves, Move Tutor Moves, Move Tutor Compatibility, Shop Items, Pickup Items, In-Game Trades, Static Pokemon, Type Effectiveness, Pokemon Base Statistics and Move Data Power/Accuracy/PP/Type/Names.
- OFF profile: Starter Pokemon, Trainer Class Names, Evolution Randomization and Special-Wild/Day-Night/Swarms.
- Sanitized evidence: randomization completed, output ROM booted, a short run was played, wild encounters worked, a trainer battle worked and items/shops/moves/abilities showed no blockers during the short run.
- Evolutions unchanged remain expected.
- No missing sprites, move-less Pokemon, crash, freeze or softlock were observed in this short smoke.
- Known exclusions remain: Starter/Rival sync is unresolved, Trainer Class Names can visually mismatch sprites because it is textlabel remapping only and Special-Wild remains out-of-scope.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made in this workspace sync.

# Session update - GUI working settings matrix

- New branch: `randomizer/sync-gui-settings-matrix-pass`.
- Synced merged UPR-FVX PR #88 and PR #89 into the workspace pin.
- `02_external/upr-fvx` now pins merge commit `f3a6d04ff6db8d48468800194e0baffbafb7505c`.
- Added `08_tests/randomizer/190_gui_working_settings_matrix.md`.
- Sanitized local GUI Working Settings Matrix evidence is recorded after UPR-FVX fixes through PR #89.
- Passed settings: Wild Standard/Fallback, Trainer Pokemon core, Pokemon Movesets -> Random completely, Trainer Movesets, Trainer Names, Field Items basic, Pokemon Abilities, TM/HM Compatibility, TM Moves, Move Tutor Moves, Move Tutor Compatibility, Shop Items, Pickup Items, In-Game Trades, Static Pokemon, Type Effectiveness, Pokemon Base Statistics and Move Data Power/Accuracy/PP/Type/Names.
- In-Game Trades no longer show `NEW GIVEN = ?` after PR #89 in sanitized evidence.
- Evolutions unchanged are preserved; swarms remain disabled by CFRU `SWARM_CHANCE=0`.
- Trainer Class Names is documented as textlabel remapping only; sprite/class-id mismatch is expected and the option is recommended off for a stable visual profile.
- Starter Pokemon remains caveated: player starter choices randomize, but rival first-battle sync is unresolved/blocked.
- Special-Wild remains out-of-scope. Supported/special shops are confirmed, Pickup Items are log-confirmed, Static null placeholders remain null and Base Stats ability-name log display can appear truncated while ingame names are correct.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made in this workspace sync.

# Session update - Trainer Names/Class Names GUI smoke

- New branch: `randomizer/sync-trainer-names-class-names-pass`.
- Synced merged UPR-FVX PR #83, PR #85 and PR #86 into the workspace pin.
- `02_external/upr-fvx` now pins merge commit `f86315e7528ba3257df03b80c0c75ccc69ef574b`.
- Added `08_tests/randomizer/190_trainer_names_class_names_pass.md`.
- Sanitized local GUI-smoke evidence: Trainer Names and Trainer Class Names were enabled on top of the stable Wild Standard/Fallback, Trainer Pokemon core and Pokemon Movesets -> Random completely path.
- Trainer Names are visibly changed in the Trainer Pokemon log.
- Trainer Class Names no longer collapse to `Director` or `[PKMN] BREEDER`.
- Trainer Class Names now pass as global class-label remapping: the same original class maps to the same new class label.
- Per-trainer class assignment is not part of the current option and remains a separate possible future feature.
- Evolutions remain correct in the tested path; Squirtle evolved into Wartortle at Lv16.
- Wild Standard/Fallback, Trainer Pokemon core and Pokemon Movesets -> Random completely remain stable; swarms remain disabled.
- Missing sprites were not observed and move-less Pokemon were not observed.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made in this workspace sync.

# Session update - CFRU/DPE evolution row stride fix

- New branch: `randomizer/sync-cfru-dpe-evolution-row-stride-fix`.
- Synced merged UPR-FVX PR #82 into the workspace pin.
- `02_external/upr-fvx` now pins merge commit `485f0b899c84470f3fab82317331a671ec023ac1`.
- CFRU/DPE uses `EVOS_PER_MON=16`; UPR-FVX PR #82 now uses `evolutionSlotsPerSpecies=16` and `evolutionRowSize=0x80` for the CFRU/DPE Gen9 evolution path.
- Root cause recorded: the old UPR-FVX evolution read/write/report path used vanilla 5-slot row stride (`0x28` bytes), so the report could read the private input ROM incorrectly and the old writer could damage output evolutions.
- Sanitized local report evidence after PR #82: Input ROM starter chains correct and new Output ROM starter chains correct.
- Starter chain evidence: Bulbasaur -> Ivysaur Lv16, Ivysaur -> Venusaur Lv32, Charmander -> Charmeleon Lv16, Charmeleon -> Charizard Lv36, Squirtle -> Wartortle Lv16 and Wartortle -> Blastoise Lv36.
- Sanitized ingame smoke evidence after PR #82: Squirtle evolved at Lv16 in a new FVX output.
- Previous bad/Test13-style outputs are invalid/stale because they were created by the old writer path; do not use them for current validation.
- Recommended next isolated option block: Trainer Names/Class Names or a first Items/Moves/Abilities slice, with Special-Wild systems still disabled.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made in this workspace sync.

# Session update - GUI-4B no-swarms pass

- New branch: `randomizer/sync-gui4b-no-swarms-pass`.
- Synced merged UPR-FVX PR #79, UPR-FVX PR #80 and CFRU PR #5 into workspace pins.
- `02_external/upr-fvx` now pins merge commit `226bcacc4f66cee5689caa128d5e35ef4acc001d`.
- `02_external/CFRU-expansion` now pins merge commit `c4c90373fe7f24acd5dcfa3a8fbdd5cb573bfe29`.
- Added `08_tests/randomizer/188_gui4b_learnsets_no_swarms_pass.md`.
- Sanitized local GUI-4B evidence: correct CFRU/DPE Gen9 ROM loaded with `isRomHack=true`, PokemonCount 1439, PokedexCount 1290 and generations 1-9 present.
- Options used: Wild Standard/Fallback, Trainer Pokemon core and Pokemon Movesets -> Random completely. Trainer Names/Class Names, Items/Moves/Abilities, TM/HM/Tutor and Special-Wild systems were not enabled.
- Result: output ROM was created locally, emulator boot succeeded, wild encounters and a trainer battle were checked, missing sprites were not observed and move-less Pokemon were not observed.
- Learnset empty-moveset crash status: `SpeciesMovesetRandomizer` `IndexOutOfBoundsException` was not reproduced after the UPR-FVX guard.
- Swarm status: CFRU `SWARM_CHANCE=0` is synced, Route 1 no-swarm rebuild check did not observe Swarm-Frigibax and an example Route 1 encounter was Urshifu Lv3 displayed correctly.
- Ogerpon remains valid and pool-eligible.
- Remaining guarded invalid palette candidates are known console warnings and not blockers.
- CFRU Day/Night Wild and other Special-Wild systems remain out-of-scope for the current normal walkthrough goal.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made in this workspace sync.

# Session update - GUI-4A Ogerpon Wild/Trainer pass

- New branch: `randomizer/sync-gui4a-ogerpon-wild-trainer-pass`.
- Synced merged UPR-FVX PR #78 into the workspace pin.
- `02_external/upr-fvx` now pins merge commit `18e184b2c22451c74b4ba46bd7203c579d3bc9e7`.
- Added `08_tests/randomizer/187_gui4a_wild_trainer_ogerpon_pass.md`.
- Sanitized local GUI-4A evidence: correct CFRU/DPE Gen9 ROM loaded with `isRomHack=true`, PokemonCount 1439, PokedexCount 1290 and generations 1-9 present.
- Options used: Wild Standard/Fallback plus Trainer Pokemon core; Trainer Names/Class Names, Learnsets, Items/Moves/Abilities and Special-Wild systems were not enabled.
- Result: GUI randomization completed, output ROM was created locally, emulator boot succeeded, wild encounters were checked and a trainer battle was checked.
- Missing sprites observed: no. Move-less Pokemon observed: no.
- Ogerpon appears in Trainer output/log and is now pool-eligible after the Ogerpon Learnset/Sprite/Palette fixes.
- Remaining known guarded exclusions: Bad Egg has no usable learnset; Warrior, Exeggcute, Cubone, Koffing and Mime Jr. still have invalid/missing front battle sprite/palette.
- CFRU Day/Night Wild, Swarms and other Special-Wild systems remain out-of-scope for the current normal walkthrough goal.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made in this workspace sync.

# Session update - Ogerpon asset fix sync

- New branch: `randomizer/sync-ogerpon-asset-fix`.
- Synced merged DPE PR #2 and UPR-FVX PR #77.
- Workspace pins now include DPE `3d0ac870fadc91e55f6ff19c0f7aae3cac2014a1` and UPR-FVX `d6415d59a8b94b4d6d4c1e424a73c0f426993d03`.
- Added `08_tests/randomizer/186_ogerpon_asset_fix_sync.md`.
- Sanitized local Pool Asset Report evidence after local DPE+CFRU rebuild: PokemonCount 1439, PokedexCount 1290, candidate count before guard 1192, accepted count after guard 1186, excluded count 6, excluded no usable learnset 1, invalid/missing front battle sprite pointer 5 and invalid/missing normal palette pointer 5.
- Ogerpon internal slots 1422..1429 now report movesLearntCount 20, learnsetPointerValid true, frontSpritePointerValid true and palettePointerValid true.
- Ogerpon status: accepted.
- Remaining invalid candidates: Bad Egg has no usable learnset; Warrior, Exeggcute, Cubone, Koffing and Mime Jr. still have invalid/missing front battle sprite pointers.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made in this workspace sync.

# Session update - CFRU/DPE learnset runtime fixes sync

- New branch: `randomizer/sync-cfru-dpe-learnset-runtime-fixes`.
- Synced merged learnset-runtime related fixes: UPR-FVX PR #76, CFRU PR #3, CFRU PR #2 and DPE PR #1.
- Workspace pins now include UPR-FVX `808cbe823772187ec3ecc13e484a87eb449aaac5`, CFRU `1c99ca5abeeb577f8214247e523e62575443bb81` and DPE `0a1ca7811fd00f981dad19d7476b92513fe62cdc`.
- Added `08_tests/randomizer/185_cfru_dpe_learnset_runtime_fixes_sync.md`.
- Sanitized local Pool Asset Report evidence after local rebuild: PokemonCount 1439, PokedexCount 1290, maxInternalSpeciesId 1439, accepted count after guard 1185, excluded count 7, excluded no usable learnset 1, invalid/missing front battle sprite pointer 6, invalid/missing normal palette pointer 6, cfruRuntimeLearnsetPointerOffset `0x1167134`, chosenLearnsetTableBase `0x1167134`, Ogerpon movesLearntCount 20 and Ogerpon learnsetPointerValid true.
- Status: learnset runtime pointer blocker is resolved; Pool Asset Report improved from 436 accepted / 756 no-learnset exclusions to 1185 accepted / 1 no-learnset exclusion.
- Ogerpon now has moves/learnset, but remains excluded because of invalid/missing front battle sprite pointer.
- Next technical block: diagnose Ogerpon/front battle sprite pointer.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX/CFRU/DPE code change and no P1 promotion was made in this workspace sync.

# Session update - GUI E2E Wild smoke pass

- New branch: `randomizer/gui-e2e-wild-pass-sync`.
- UPR-FVX pin remains `04bdd8b2f2769bedb1bf6c6ff8fcdecbbf84e29c`; no submodule change was made.
- Added `08_tests/randomizer/184_gui_e2e_wild_smoke_pass.md`.
- Sanitized local GUI E2E evidence: correct CFRU/DPE Gen9 ROM loaded yes, PokemonCount 1439, PokedexCount 1290, generation counts include 4-9 yes, options used Wild Standard/Fallback only, randomization completed yes, output ROM created yes, emulator boot yes, first wild encounter reached yes, first encounter species Avalugg Lv2, private paths/logs/hashes/screenshots omitted yes.
- Status: GUI-0 through GUI-3 passed for the minimal Wild Standard/Fallback route.
- No ROM, output ROM, save, emulator state, screenshot, full log, ROM path, hash, CRC, private path, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX code change, no submodule pin change and no P1 promotion was made; Standard/Fallback Wild was already P1-supported.
- Next local step: GUI-4, expand one option group at a time, starting with Trainer-Core or Learnsets rather than full randomization.

# Session update - GUI load null species fix sync

- New branch: `randomizer/gui-load-null-species-fix-sync`.
- UPR-FVX PR #68 is merged and `02_external/upr-fvx` now pins merged commit `04bdd8b2f2769bedb1bf6c6ff8fcdecbbf84e29c`.
- Previous GUI-0 blocker: `RandomizerGUI.populateDropdowns()` could throw a NullPointerException when sparse Custom-ROM Species mappings contained null Species.
- Fix: null Species are filtered out of GUI dropdown Species lists and are not selectable dropdown entries.
- Sanitized local GUI-0 result after the fix: GUI opened yes, custom ROM loaded yes, randomization not yet, output ROM not yet, private paths/logs/hashes/screenshots omitted yes.
- Status: GUI-0 passed for Custom ROM load in the local GUI path.
- Next local step: GUI-1 with Wild Standard/Fallback only randomization.
- No ROM, save, emulator state, output ROM, build artifact, tool binary, private path, hash, full log, screenshot, secret, token or `.env` detail was read, copied, changed or documented by Codex.
- No UPR-FVX code change was made in this workspace sync, no Output-ROM evidence exists yet and no P1 promotion was made.

# Session update - GUI E2E smoke pipeline

- New branch: `randomizer/gui-e2e-smoke-pipeline`.
- Added `08_tests/randomizer/gui_e2e_smoke_pipeline.md` as a short local-only GUI E2E smoke pipeline for the private custom ROM.
- Fastest order: GUI-0 load the custom ROM in UPR-FVX GUI without randomization, GUI-1 randomize only Wild Standard/Fallback, GUI-2 boot the output ROM locally, GUI-3 reach the first wild encounter, GUI-4+ add further option groups only after the minimal path is clean.
- Initially disabled: Trainer Names/Class Names, Learnsets, Items/Moves/Abilities, Special Wild systems, Day/Night Wild, Swarms, Roamers, DexNav, Raids and Wild Double Battles.
- Sanitized feedback format is yes/no only for GUI opened, custom ROM loaded, options used, output ROM created, emulator boot, first wild encounter reached and a short sanitized error summary.
- Codex did not run ROM, GUI or emulator smokes; no ROM path, ROM hash, full log, output ROM, save, emulator state, build artifact, screenshot with private paths, secret, token or `.env` detail was read, copied, changed or documented.
- No UPR-FVX code change, no submodule pin change and no P1 promotion was made.

# Session update - Trainer text ROM smoke harness sync

- New branch: `randomizer/trainer-text-rom-smoke-harness-sync`.
- UPR-FVX PR #67 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins verified merged UPR-FVX commit `9bde3d4e2f983bfb96875c5fe9697f87763d8665`.
- PR #67 adds the opt-in Gen3 Trainer Names/Class Names ROM-facing smoke harness `Gen3TrainerTextRomSmokeTest`.
- Evidence scope: harness prepared only; default no-ROM execution skips cleanly with Tests 1, Skipped 1, Failures 0, Errors 0.
- The real local ROM smoke has not been documented yet, and byte-exact Terminator/Padding inspection is not directly proven.
- Status remains below P1-supported; no P1 promotion is made in this sync.
- No ROM path, ROM hash, full log, output ROM, save, emulator state, build artifact, tool binary, private path, secret, token or `.env` detail was read, copied, changed or documented.
- No new UPR-FVX code change in this workspace sync.
- Note: the expected SHA `a5a8887e0dac0bdbe4bfe87bfdc2e7a27fb79b75` was not the actual PR #67 merge commit; GitHub reports `9bde3d4e2f983bfb96875c5fe9697f87763d8665`.

# Session update - Wild encounters P1 decision

- New branch: `randomizer/wild-encounters-p1-decision`.
- UPR-FVX pin remains `f4d0cbbe3143cab4b963d2444b8354d97fa96403`; no submodule change was made.
- Decision: Wild Encounters are now `P1-supported` for the documented Standard/Fallback Wild Encounter writer/reload scope in the tested private target context.
- Basis: ROM-free Wild Encounter decision/option slices, ROM-free synthetic Writer/Reload Equality, opt-in ROM-facing smoke harness and sanitized local `Gen3WildEncounterRomSmokeTest` pass after PR #66.
- Scope boundary: CFRU Day/Night Wild, Swarms, Roamers, DexNav, Raids, Wild Double Battles and other special Wild systems remain separate/non-promoted scopes.
- No new ROM execution, UPR-FVX code change, submodule pin change, ROM path, ROM hash, full log or output ROM was added.

# Session update - Wild encounters ROM smoke evidence sync

- New branch: `randomizer/wild-encounters-rom-smoke-evidence-sync`.
- UPR-FVX PR #66 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `f4d0cbbe3143cab4b963d2444b8354d97fa96403`.
- PR #66 fixes the Gen3 Evolution load blocker that previously stopped the opt-in Wild Encounter ROM smoke before the Wild Encounter writer/reload portion.
- Sanitized local evidence after PR #66: `Gen3WildEncounterRomSmokeTest` passed with Tests 1, Failures 0, Errors 0, Skipped 0.
- Evidence scope: local ROM-facing Writer/Reload smoke evidence for Wild Encounters in the private target context.
- Status: Wild Encounters is a P1 candidate, but no P1 promotion is made in this sync; promotion requires a separate short decision/evaluation.
- No ROM path, ROM hash, full log, output ROM, save, emulator state, build artifact, tool binary, private path, secret, token or `.env` detail was read, copied, changed or documented.
- No new UPR-FVX code change in this workspace sync.

# Session update - Wild encounters ROM smoke harness sync

- New branch: `randomizer/wild-encounters-rom-smoke-harness-sync`.
- UPR-FVX PR #65 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins verified merged UPR-FVX commit `f224862c91aed8e7a75fe843f5088cadea734da4`.
- Evidence scope: ROM-facing Wild Encounter smoke harness prepared in UPR-FVX; default no-ROM execution skips cleanly.
- The real local ROM smoke has not been executed in this workspace sync.
- Status remains below P1-supported; no private ROM path, hash, log, output ROM, Randomizer run, ROM evidence result or P1 promotion was added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No new UPR-FVX code change in this workspace sync.
- Note: the requested SHA `c7a07a4643a570b2e27de059804f1a249616aaf0` was not reachable in the UPR-FVX fork; GitHub reports PR #65 merge commit `f224862c91aed8e7a75fe843f5088cadea734da4`.

# Session update - Wild encounters reload equality evidence sync

- New branch: `randomizer/wild-encounters-p1-track`.
- UPR-FVX PR #64 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `d49837fea305157a2fe94f3f57d09cedc8ab25f8`.
- Evidence scope: ROM-free synthetic Writer/Reload Equality evidence for Wild Encounters in `WildCatchLevelDecisionTest`; a reloadable fake `RomHandler` deep-copies `setEncounters(...)` data and reloads fresh `getEncounters(...)` copies.
- Covered invariants: Area metadata, Slot-Anzahlen, Levelbereiche, allowed Species pool and high Species IDs above `1000` remain reload-equal.
- Status remains below P1-supported; no real Gen3 ROM byte writer proof, output ROM, Randomizer run, ROM-Smoke or P1 promotion was added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No new UPR-FVX code change in this workspace sync.

# Session update - Items first test slice sync

- New branch: `docs/sync-items-first-slice`.
- UPR-FVX PR #63 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `d88a0cdb8c11473d2a3448028e937422eaf38679`.
- Evidence scope: third ROM-free Items/Moves/Abilities slice for Items; synthetic `ItemDecisionTest` verifies `ItemRandomizer.randomizeFieldItems()` for Non-TM Field Items keeps choices inside the non-bad allowed Item pool, excludes bad/key-style Items, keeps output non-empty, preserves Field-Item count and allows high Item IDs `1001..1003`.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Moves first test slice sync

- New branch: `docs/sync-moves-first-slice`.
- UPR-FVX PR #62 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `a5b1b63b134149bd88e62af27a9b45332f617d9e`.
- Evidence scope: second ROM-free Items/Moves/Abilities slice for Moves; synthetic `TMTutorMoveDecisionTest` verifies `TMTutorMoveRandomizer.randomizeTMMoves()` keeps TM choices inside the allowed Move pool, excludes HM/game-breaking/levelup-banned/illegal Moves, preserves the Field-Move-TM slot, keeps output count stable and allows high Move IDs `1001..1003`.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Items/Moves/Abilities first test slice sync

- New branch: `docs/sync-items-moves-abilities-first-slice`.
- UPR-FVX PR #61 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `c365b96399ed36881ed637edce0721c059c442d1`.
- Evidence scope: first ROM-free Items/Moves/Abilities slice for Abilities; synthetic `SpeciesAbilityDecisionTest` verifies `SpeciesAbilityRandomizer` keeps Ability choices inside the allowed pool, rejects banned Ability candidates, produces non-empty two-Ability output and keeps high Species ID `1025` in the path.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Learnsets evolution moves test slice sync

- New branch: `docs/sync-learnsets-evolution-moves-slice`.
- UPR-FVX PR #60 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `c40fbbd796db5b43a3bc53e547dc890a853cef20`.
- Evidence scope: fourth ROM-free `LearnsetDecisionTest` slice for Learnsets; synthetic Evolution Moves for All data verifies exactly one Level-0 Evolution-Move slot is added while existing Level-1/later level slots, Move pool and high Species ID `1025` path remain stable.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Learnsets starting moves test slice sync

- New branch: `docs/sync-learnsets-starting-moves-slice`.
- UPR-FVX PR #59 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `0d217db45086d8d03b4eb606ae2621633396d768`.
- Evidence scope: third ROM-free `LearnsetDecisionTest` slice for Learnsets; synthetic Guaranteed Starting Moves data verifies expected Level-1 slots are added while the later level slot, Move pool and high Species ID `1025` path remain stable.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Learnsets option test slice sync

- New branch: `docs/sync-learnsets-option-slice`.
- UPR-FVX PR #58 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `6ed75f5b1e5b8b354e2db694c880407c8e0a10dd`.
- Evidence scope: second ROM-free `LearnsetDecisionTest` slice for Learnsets; synthetic `orderDamagingMovesByDamage()` data verifies damaging Moves are sorted by damage while Evolution-/Non-Damaging-Slots, Level-/Slot-Anzahl, Move pool and high Species ID `1025` remain stable.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Learnsets first test slice sync

- New branch: `docs/sync-learnsets-first-test-slice`.
- UPR-FVX PR #57 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `56cae7eb0c2ddc626dc31c4802d3f696a42959bf`.
- Evidence scope: first ROM-free `LearnsetDecisionTest` slice for Learnsets; synthetic `randomizeMovesLearnt()` data verifies non-empty Learnsets, preserved Level-/Slot-Anzahl, allowed Move-pool selection and high Species ID `1025`.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Wild encounters option test slice sync

- New branch: `docs/sync-wild-encounters-option-slice`.
- UPR-FVX PR #56 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `b3b9a8ab5e8726f4b4d2d4e23efa733cce7287ac`.
- Evidence scope: third ROM-free `WildCatchLevelDecisionTest` slice for Wild Encounters; synthetic `BlockWildLegendaries` coverage verifies legendary Species stay out of the replacement pool while Slot-/Level-/Area structure remains stable.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Wild encounters multi-area test slice sync

- New branch: `docs/sync-wild-encounters-multi-area-slice`.
- UPR-FVX PR #55 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `8f88e25d458996b560189ba23d3216ee0c775f14`.
- Evidence scope: second ROM-free `WildCatchLevelDecisionTest` slice for Wild Encounters; synthetic multi-area data verifies that different Areas, Slot-Anzahlen, Levelbereiche, encounter types, rates and map/location metadata stay structurally stable.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Wild encounters first test slice sync

- New branch: `docs/sync-wild-encounters-first-slice`.
- UPR-FVX PR #54 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `8d67f8686e16b3a9d3e77da5789a06889a645e5f`.
- Evidence scope: first ROM-free `WildCatchLevelDecisionTest` slice for Wild Encounters; synthetic encounters verify preserved Slot-/Level-/Area structure, non-empty encounter areas, allowed Species selection and high-numbered Species IDs above `1000`.
- Status remains ROM-free unit-test evidence only, not P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or P1 promotion is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Trainer Class Names encoded length fix sync

- New branch: `docs/sync-trainer-class-names-encoded-length-fix`.
- UPR-FVX PR #53 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `955c852cf07f155a046b18865a39e6912a6ee09c`.
- Fix scope: Trainer Class Names max-length filtering now uses encoded/internal length through `romHandler.internalStringLength(...)` instead of Java `changeTo.length()`.
- Evidence scope: focused ROM-free `TrainerNameRandomizerTest` coverage for class names inside limit, exactly at limit, over limit and Java length != internal length.
- Status remains `tested-non-rom`, not P1-supported; no ROM-facing Writer/Reload, real Terminator/Padding proof, decoded reload equality or Text-Encoding safety claim is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload smoke, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Trainer Names text length unit evidence

- New branch: `docs/trainer-names-text-length-unit-evidence`.
- UPR-FVX PR #52 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `7357b244e01ef2c7790b858d50c19c31ac72e955`.
- Added evidence document `08_tests/randomizer/031_trainer_names_text_length_unit_evidence.md`.
- Evidence scope: ROM-free `TrainerNameRandomizerTest` extension for Trainer Names/Class Names text-length risks: ASCII inside limit, exactly at encoded/internal limit, over encoded/internal limit, Java length != internal length, escaped-token-style divergence and Class-Names `changeTo.length()` risk exposure.
- Status remains `tested-non-rom`, not P1-supported; no ROM-facing Writer/Reload, real Terminator/Padding proof, decoded reload equality or Text-Encoding safety claim is added.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change in this workspace block, Writer-/Reload fix, ROM-Smoke, Randomizer run or P1 promotion was performed.

# Session update - Trainer Names text harness design

- New branch: `analysis/trainer-names-text-harness-design`.
- Added read-only design `08_tests/randomizer/030_trainer_names_text_harness_design.md` for a future ROM-free Trainer Names/Class Names harness.
- Decision: later implementation should be a focused UPR-FVX unit-test scope, with a fake `RomHandler` whose `internalStringLength(...)` can differ from Java length; workspace-only/manual plan, local helper and separate diagnosis harness are less suitable for the first ROM-free step.
- The design keeps byte truncation, terminator/padding and decoded reload equality as a separate synthetic byte-model layer or later ROM-facing evidence, not as proven support.
- Status remains `tested-non-rom`, not P1-supported; no Text-Encoding safety claim is made and `changeTo.length()` remains an open class-name risk.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, hash, secret, token or `.env` file was read, copied, changed or documented.
- No implementation, UPR-FVX code change, Writer-/Reload fix, external download, smoke run, build or P1 promotion was performed.

# Session update - Trainer Names text evidence harness plan

- New branch: `analysis/trainer-names-text-evidence-harness-plan`.
- Added read-only plan `08_tests/randomizer/029_trainer_names_text_evidence_harness_plan.md` for Trainer Names/Class Names only.
- The plan derives minimal later cases from 027/028: ASCII inside limit, ASCII exactly at limit, encoded over-limit rejection, Gen3 escaped/control-token length divergence, terminator/padding checks and decoded reload equality.
- Status remains `tested-non-rom`, not P1-supported; the plan makes no Text-Encoding safety claim and keeps `changeTo.length()` as an open class-name risk.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, hash, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change, Writer-/Reload fix, Text-Encoding implementation, smoke run, build or P1 promotion was performed.

# Session update - Trainer writer/reload/text field review

- New branch: `analysis/trainer-writer-reload-text-field-review`.
- Added read-only review `08_tests/randomizer/028_trainer_writer_reload_text_field_review.md`.
- Identified Trainer writer/reload fields in the Gen3 `loadTrainers()` / `saveTrainers()` path: team flags, Trainer name text, battle mode byte, party size, Pokemon data pointer, per-Pokemon species, level, IV/strength, held item and moves, plus Mossdeep Steven as a special separate team writer.
- Identified Trainer text checks for later evidence: Gen3 `translateString(...)`, `internalStringLength(...)`, `writeFixedLengthString(...)`, `TrainerNameLength`, `TrainerClassNameLength`, terminator/padding behavior and decoded reload equality.
- Open risk remains: Trainer class-name max filtering contains a Java `changeTo.length()` check, so later evidence must prove encoded/internal byte length safety before any Text P1 promotion.
- No ROM, save, emulator state, output ROM, build, tool binary, private path, hash, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code change, Writer-/Reload fix, Text-Encoding implementation, smoke run, build or P1 promotion was performed.

# Session update - Trainer ROM/Reload/Text evidence plan

- New branch: `analysis/trainer-rom-reload-text-evidence-plan`.
- Added a read-only plan for later Trainer ROM-/Reload-/Text-Encoding evidence: `08_tests/randomizer/027_trainer_rom_reload_text_evidence_plan.md`.
- The plan records current Trainer suboptions `FVX-FOE-005` through `FVX-FOE-014` as applicable `tested-non-rom`, not P1-supported, based on recent synthetic harness follow-ups.
- Missing evidence is kept separate: later ROM-/Reload evidence, Trainer text-encoding proof, and the `changeTo.length()` length-measurement risk each need their own proof before any promotion.
- No Roadmap status promotion is made: no ROM, save, emulator state, output ROM, log, build artifact, Randomizer JAR, tool binary, private path, hash, secret, token or `.env` file was read, copied, changed or documented.
- No UPR-FVX code, Writer-/Reload fix, Text-Encoding implementation, Randomizer run or P1 promotion was performed.

# Session update - Diagnose 181

- New branch: `test/upr-fvx-cfru-dpe-trainer-names-followup`.
- UPR-FVX PR #51 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `d20eb1367c62a4f14c8778bc61ad6904ea76a6d6`.
- Original UPR-FVX test commit: `f49f5aa9 test: cover trainer name decisions`.
- Follow-up 181 records the Non-ROM `TrainerNameRandomizerTest` harness for `FVX-FOE-013` Trainer Names/Class Names.
- Covered decisions: `canChangeTrainerText=false`, Trainer Names singles-/doubles-pools, repeated-name translation, `MAX_LENGTH`, `MAX_LENGTH_WITH_CLASS`, Trainer Class Name pools through `getDoublesTrainerClasses()` and fixed class-name length.
- Statuswirkung: `FVX-FOE-013` moves to `tested-non-rom`, not P1-supported.
- Checks from PR #51 are recorded as `git diff --check`, focused `:random:test --tests '*TrainerNameRandomizer*'` and broader `:random:test --tests '*Trainer*'`, all successful.
- No Gen3 Writer/Reload, ROM-Smoke, text-encoding proof, output-ROM generation, Randomizer run, `changeTo.length()` fix or P1-promotion was performed.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, secret, token or `.env` file was committed.

# Session update - Diagnose 180B

- New branch: `test/upr-fvx-cfru-dpe-battle-style-followup`.
- UPR-FVX PR #50 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `5e2d351966ce4a96d02cdb6ca676b39bde7a9505`.
- Original UPR-FVX test commit: `99f46cce7464750ea5cdc4055b1e9168e59bc1a0`.
- Follow-up 180B records the Non-ROM `TrainerBattleStyleTest` harness for `FVX-FOE-011` Battle Style.
- Statuswirkung: `FVX-FOE-011` moves to `tested-non-rom`, not P1-supported.
- Checks from PR #50 are recorded as `git diff --check`, focused `:random:test --tests '*TrainerBattleStyle*'`, broader `:random:test --tests '*Trainer*'` and full `:random:test`, all successful.
- No Writer/Reload, ROM-Smoke, output-ROM generation, Randomizer run, Trainer Names/Class Names/Text work or P1-promotion was performed.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, secret, token or `.env` file was committed.

# Session update - Diagnose 179B

- New branch: `test/upr-fvx-cfru-dpe-trainer-special-rules-followup`.
- UPR-FVX PR #49 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `bc46fdc49741643d8f09dd302b67b5b2d35d24c5`.
- Original UPR-FVX test commit: `6489dd1e61d1bcb35345ae006032b884527e0a97`.
- Follow-up 179B records the Non-ROM `TrainerSpecialRulesTest` harness for Trainer Special Rules.
- Statuswirkung: `FVX-FOE-010`, `FVX-FOE-012` and `FVX-FOE-014` move to `tested-non-rom`, not P1-supported.
- `FVX-FOE-011` Battle Style and `FVX-FOE-013` Trainer Names/Class Names/Text remain separate and unpromoted.
- Checks from PR #49 are recorded as focused `:random:test --tests com.uprfvx.random.randomizers.TrainerSpecialRulesTest`, broader `:random:test --tests '*Trainer*'` and full `:random:test`, all `BUILD SUCCESSFUL`.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was committed.

# Session update - Diagnose 178B

- New branch: `test/upr-fvx-cfru-dpe-trainer-additional-pokemon-followup`.
- UPR-FVX PR #48 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `32ab7d969e5439d38e5781670c9a68e0ea418d0a`.
- Original UPR-FVX test commit: `cdc09eaee12c44a7f3ba5ca24a091ce4da2ef8ac`.
- Follow-up 178B records the Non-ROM `TrainerAdditionalPokemonTest` harness for Additional Pokemon on Boss, Important and Regular Trainers.
- Guard/Fix: `TrainerPokemonRandomizer` clones additional Pokemon only from original slots with non-null Species; trainers without a safe template are skipped, while max party size 6 and multi-battle limit 3 are covered.
- Statuswirkung: `FVX-FOE-005`, `FVX-FOE-006` and `FVX-FOE-007` move to `tested-non-rom`, not P1-supported.
- Checks from PR #48 are recorded as focused `:random:test --tests com.uprfvx.random.randomizers.TrainerAdditionalPokemonTest`, broader `:random:test --tests '*Trainer*'` and full `:random:test`, all `BUILD SUCCESSFUL`.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was committed.

# Session update - Diagnose 177B

- New branch: `test/upr-fvx-cfru-dpe-trainer-type-diversity-followup`.
- UPR-FVX PR #47 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `ea5269706eb7d04eb0b305f88e8fa20bfb21f92a`.
- Original UPR-FVX test commit: `60f6664e556cc750801ad1d47ba970ded8d6af85`.
- Follow-up 177B records the Non-ROM `TrainerTypeDiversityGuardTest` harness for Trainer Type Diversity / Type Themes.
- Statuswirkung: `FVX-FOE-009` moves to `tested-non-rom`, not P1-supported.
- Checks from PR #47 are recorded as focused `:random:test --tests com.uprfvx.random.randomizers.TrainerTypeDiversityGuardTest`, broader `:random:test --tests '*Trainer*'` and full `:random:test`, all `BUILD SUCCESSFUL`.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was committed.

# Session update - Diagnose 176B

- New branch: `test/upr-fvx-cfru-dpe-wild-catch-level-followup`.
- UPR-FVX PR #46 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `c86221d758bece06b216b1f4fb23dd8e4a6c8ec0`.
- Original UPR-FVX test commit: `8665eb4f070567fd908327b272c7f1da5abdef68`.
- Follow-up 176B records the Non-ROM `WildCatchLevelDecisionTest` harness for Wild catch/level decision paths.
- Statuswirkung: `FVX-WILD-007`, `FVX-WILD-010` and `FVX-WILD-012` move to `tested-non-rom`, not P1-supported.
- Checks from PR #46 are recorded as focused `:random:test --tests com.uprfvx.random.randomizers.WildCatchLevelDecisionTest`, broader `:random:test --tests '*Wild*'` and full `:random:test`, all `BUILD SUCCESSFUL`.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was committed.

# Session update - Diagnose 175B

- New branch: `test/upr-fvx-cfru-dpe-movedata-write-followup`.
- UPR-FVX PR #45 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `1be6f51779906af017f6177f264e41f8c7902d8e`.
- Original UPR-FVX test commit: `60996b166113d40f4ff848d8063e98661415a599`.
- Follow-up 175B records the Non-ROM `Gen3MoveDataWriterTest` and `MoveUpdateDecisionTest` harnesses for MoveData writer/updater decisions.
- Statuswirkung: `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` and `FVX-MOVE-006` move to `tested-non-rom`, not P1-supported.
- `FVX-MOVE-005` Move Names/Text remains out of scope.
- Checks from PR #45 are recorded as focused `:romio:test --tests '*Move*'`, focused `:random:test --tests '*Move*'`, full `:romio:test` and full `:random:test`, all `BUILD SUCCESSFUL`; the known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was committed.

# Session update - Diagnose 174B

- New branch: `test/upr-fvx-cfru-dpe-make-evolutions-easier-followup`.
- UPR-FVX PR #44 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `85b282112322f8991dd11b14cc98d6dd68fd3fd4`.
- Original UPR-FVX test commit: `a0fc6515b60ad3032a8d94c554bbc3021e10a33f`.
- Follow-up 174B records the Non-ROM `EvolutionMakeEasierDecisionTest` harness for `FVX-TRAIT-025A` Make Evolutions Easier Condense-/Level-/Decision logic.
- Test-/Seam-Entscheidung: small package-private helper in `AbstractRomHandler`; synthetic `Species` / `Evolution` chains; intermediate/final level caps, non-level `estimatedEvoLvl` capping and `highestEvoLvl` behavior are covered.
- Statuswirkung: `FVX-TRAIT-025A` moves to `tested-non-rom`; `FVX-TRAIT-025B` remains a separate Gen3 Happiness-byte patch / writer-like scope; `FVX-TRAIT-026` remains helper-only with no standalone support claim.
- Checks from 174A are recorded as `./gradlew --offline :romio:test --tests '*Evolution*'` and `./gradlew --offline :romio:test`, both `BUILD SUCCESSFUL`; the known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 173

- New branch: `test/upr-fvx-cfru-dpe-evolution-make-easier-scope-plan`.
- PR #221 / Follow-up 172B was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `3b33412e80d1cb2d97725ad7a7dd01529aa56919`.
- Diagnose 173 plans `FVX-TRAIT-025` Make Evolutions Easier as a split scope.
- Result: `make-easier-plan-ready`.
- `025A` is ROM-free Condense-/Level-/Decision logic around `AbstractRomHandler.condenseLevelEvolutions(...)`, synthetic Species/Evolution chains, `extraInfo`, `estimatedEvoLvl` and `highestEvoLvl`.
- `025B` is the separate Gen3 Happiness-byte patch / writer-like scope around `Gen3RomHandler.makeEvolutionsEasier(...)` and `Gen3Constants.friendshipValueForEvoLocator`.
- `FVX-TRAIT-026` remains a helper flag for `024/025`, with no standalone support claim.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 172B

- New branch: `test/upr-fvx-cfru-dpe-evolution-method-decisions-followup`.
- UPR-FVX PR #43 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `3b33412e80d1cb2d97725ad7a7dd01529aa56919`.
- Original UPR-FVX test commit: `4b049ee82cf8716cb2fc17d0b6244020cddd22e4`.
- Follow-up 172B records the Non-ROM `EvolutionMethodDecisionTest` harness for `FVX-TRAIT-024` Change Impossible Evolutions and `FVX-TRAIT-027` Remove Time-Based Evolutions.
- Test-/Seam-Entscheidung: small package-private decision seams in `Gen3RomHandler` and `AbstractRomHandler`; synthetic `Species` / `Evolution` objects; no ROM file, Gen3 writer, reload, ROM-Smoke or Randomizer run.
- Statuswirkung: `FVX-TRAIT-024` and `FVX-TRAIT-027` move from `decision-review-ready` to `tested-non-rom`, not P1-supported.
- `FVX-TRAIT-025` remains split into condense-level logic and Gen3 happiness-byte patch risk; `FVX-TRAIT-026` remains a helper flag for `024/025`.
- Checks from 172A are recorded as `./gradlew --offline :romio:test --tests '*Evolution*'` and `./gradlew --offline :romio:test`, both `BUILD SUCCESSFUL`; the known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 171

- New branch: `test/upr-fvx-cfru-dpe-evolution-methods-decision-review`.
- PR #219 / Diagnose 170 was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- Diagnose 171 reviews the Evolution method decision paths for `FVX-TRAIT-024` Change Impossible Evolutions and `FVX-TRAIT-027` Remove Time-Based Evolutions.
- Result: `decision-review-ready`.
- Finding for `024`: Gen3 `removeImpossibleEvolutions(...)` maps FRLG happiness/beauty, Trade and Trade-Item branches to deterministic Stone or Level methods, with `extraInfo` carrying standard Item IDs or levels and `useEstimatedLevels` affecting Level targets only.
- Finding for `027`: `removeTimeBasedEvolutions()` maps `LEVEL_DUSK` to Dusk Stone, paired day/night time evolutions to Sun/Moon Stone, and unpaired time evolutions to `EvolutionType.timeless()` while preserving `extraInfo`.
- Recommended next minimal scope is a small ROM-free UPR-FVX `:romio:test` decision harness for `024/027`; writer/reload and ROM-Smoke remain separate.
- `FVX-TRAIT-025` remains split into condense-level logic and Gen3 happiness-byte patch risk; `FVX-TRAIT-026` remains a helper flag for `024/025`.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 170

- New branch: `test/upr-fvx-cfru-dpe-evolution-methods-scope-plan`.
- PR #218 / Follow-up 169B was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- Diagnose 170 plans the separate Evolution methods/improvement slices `FVX-TRAIT-024` through `FVX-TRAIT-027`.
- Result: `methods-plan-ready`.
- Finding: `GameRandomizer.maybeApplyEvolutionImprovements()` dispatches `024`, `025` and `027` through `RomHandler` improvement methods, while `026` is an estimated-level helper flag for `024/025`.
- `FVX-TRAIT-024` and `FVX-TRAIT-027` need method-mapping decision evidence before any writer/reload scope; `FVX-TRAIT-025` splits into ROM-free condense-level logic and Gen3 happiness-byte patch risk; `FVX-TRAIT-026` should not be promoted standalone.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 169B

- New branch: `test/upr-fvx-cfru-dpe-evolution-filter-non-rom-harness-followup`.
- UPR-FVX PR #42 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- Original UPR-FVX test commit: `e71a126c test: cover evolution filter options`.
- Follow-up 169B records the Non-ROM `EvolutionFilterOptionsTest` harness for `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023`.
- Statuswirkung: these slices move from `harness-plan-ready` to `tested-non-rom`, but not to P1-supported because there was no ROM-Smoke, Gen3 writer test, reload or output-ROM scope.
- 169A checks are recorded as `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.EvolutionFilterOptionsTest` and `./gradlew --offline :random:test`, both `BUILD SUCCESSFUL`.
- `FVX-TRAIT-024` through `FVX-TRAIT-027` remain separate not-started Evolution-improvement/method slices.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 168

- New branch: `test/upr-fvx-cfru-dpe-evolution-filter-harness-plan`.
- PR #216 / Diagnose 167 was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 168 plans a Non-ROM harness for Evolution filter slices `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023`.
- Result: `harness-plan-ready`.
- Finding: the target slices are all in `EvolutionRandomizer` Species-carrier/filter logic and can be tested with synthetic `Species` / `Evolution` data plus a small `RomHandler` proxy/fake, likely in `EvolutionRandomizerTest` or a new `EvolutionFilterRandomizerTest`.
- No production-code seam is expected; no ROM-Smoke, Randomizer run, build, testcode, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 167

- New branch: `test/upr-fvx-cfru-dpe-evolution-suboptions-consolidation`.
- PR #215 / Diagnose 166 was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 167 consolidates Evolution suboptions `FVX-TRAIT-016` through `FVX-TRAIT-027`.
- Result: `evolution-scope-consolidated`.
- Consolidated status: `FVX-TRAIT-016` remains P1-supported; `FVX-TRAIT-018` and `FVX-TRAIT-019` are `diagnosis-ready`; `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023` remain plan-only Species-Carrier filters; `FVX-TRAIT-024` through `FVX-TRAIT-027` remain not-started Evolution-improvement/method slices outside the narrow Species-Carrier.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 166

- New branch: `test/upr-fvx-cfru-dpe-evolution-same-typing-diagnostics`.
- PR #214 / Diagnose 165 was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 166 reclassifies `FVX-TRAIT-019` Evolution Same Typing read-only as `diagnosis-ready`.
- Finding: the original 070 Same-Typing blocker (`saveSuccessful=false`, no Output/Reload, `NullPointerException`) is superseded by Diagnose 079/080. The current `EvolutionRandomizer` Same-Typing filter uses `hasUsableSharedType(...)` and guards candidate null/unsupported Primary Type before `candidate.hasSharedType(reference)`.
- Diagnose 080 confirms Save/Log/Output/Reload true, `writeReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` and `stacktrace=none` for the narrow Same-Typing scope.
- No immediate UPR-FVX fixblock is recommended for this narrow Same-Typing scope; next minimal work is status reconciliation or, if extra evidence is requested, a read-only code-review / Non-ROM harness plan.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 165

- New branch: `test/upr-fvx-cfru-dpe-evolution-similar-strength-diagnostics`.
- PR #213 / Diagnose 164 was verified as merged into `main` before this block.
- UPR-FVX submodule remains clean and pinned at `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 165 reclassifies `FVX-TRAIT-018` Evolution Similar Strength read-only as `diagnosis-ready`.
- Finding: the original 070 blocker (`writeReloadEvolutionMismatches=24` plus `Bad Egg=true`) is superseded by Diagnose 081/082. The normalized reload comparison in 082 confirms Save/Log/Output/Reload true, `normalizedWriteReloadEvolutionMismatches=0`, `rawWithFormeWriteReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` and `stacktrace=none`.
- No immediate UPR-FVX fixblock is recommended for this narrow Similar-Strength scope; next minimal work is status reconciliation or, if extra evidence is requested, a read-only code-review / Non-ROM harness plan.
- No ROM-Smoke, Randomizer run, build, code change, submodule change, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 164

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-final-classification`.
- UPR-FVX submodule remains pinned at `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 164 closes In-Game Trades in the tested CFRU/DPE Gen9-BPRE scope as `guarded/preserve-only, not supported`.
- Rationale: no valid active In-Game Trade rows are confirmed; `P1-supported`, `candidate-confirmed` and hard `unsupported-dummy` are not justified by the current evidence.
- Achieved evidence remains valuable: mutation guard, writer-preserve guard, non-ROM `TradeRandomizerTest`, and ROM-free `Gen3InGameTradeWriterTest`.
- No ROM-Smoke, Species-Write-Smoke, Randomizer run, build, code change, text/Nickname/OT, IV or Trade Held Item randomization was performed or authorized.

# Session update - FVX dashboard XLSX export script

- New branch: `docs/fvx-dashboard-xlsx-export-script`.
- Added `07_scripts/randomizer/export_fvx_progress_dashboard_xlsx.py`, a Python standard-library exporter for selected Markdown tables from `01_docs/randomizer/fvx-progress-dashboard.md`.
- Exported sheets include Summary, Gesamtfortschritt, GUI-Feature-Gruppen, Vollstaendige Feature-Liste, Offene Blocker, Naechste Arbeitspakete, Zuletzt PRs Diagnosen and Carrier-tested nicht global.
- The exporter refuses to write if the complete feature list is shortened from 130 data rows.
- No external dependency, dependency installation, ROM/save/build/tool-binary/private path/hash/secret/`.env` access, UPR-FVX code change or generated dashboard workbook commit is required.

# Session update - Diagnose 163B

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-writer-preserve-followup`.
- UPR-FVX PR #41 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Diagnose 163B records the ROM-free Gen3 In-Game Trades writer-preserve test follow-up. The pinned `Gen3InGameTradeWriterTest` uses synthetic `InGameTrade` rows and synthetic bytes to verify unsafe/null-request rows are skipped before byte writes and preserved unchanged.
- UPR-FVX PR #41 implementation-side checks are recorded as `./gradlew --offline :romio:test` and focused `./gradlew --offline :romio:test --tests com.uprfvx.romio.romhandlers.Gen3InGameTradeWriterTest`, both with `BUILD SUCCESSFUL`.
- The known existing report failure line for `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` remains documented as a risk/assumption.
- In-Game Trades remain `blocked-pending-evidence`; no ROM-Smoke, Species-Write-Smoke, valid-active-row promotion, text, Nickname/OT, IV or Trade Held Item randomization is authorized.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 162

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-writer-preserve-test-plan`.
- PR #206 / Follow-up 161B was verified as merged before this block.
- UPR-FVX submodule remains pinned at `1eaee2873cd69682335223f817b124bf36d004f2`.
- Diagnose 162 plans a ROM-free Gen3 In-Game Trades writer-preserve test. Result: `writer-test-plan-ready`.
- Read-only finding: `Gen3RomHandler.setInGameTrades(...)` checks `canWriteInGameTrade(...)` before nickname, Species, IV, OT ID, held-item, OT-name and requested-Species byte writes, so unsafe rows are preserve/skipped before row mutation.
- A later test should add only a narrow `:romio:test` seam around the Gen3 row-write decision or eligibility helper; direct construction of a ROM-backed handler is not recommended.
- In-Game Trades remain `blocked-pending-evidence`; no code, build, Randomizer run, ROM-Smoke, Species-Write-Smoke, text, Nickname/OT, IV or Trade Held Item scope was performed.

# Session update - Diagnose 161B

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-non-rom-harness-followup`.
- UPR-FVX PR #40 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `1eaee2873cd69682335223f817b124bf36d004f2`.
- Diagnose 161B records the non-ROM In-Game Trades `TradeRandomizerTest` harness follow-up. The harness uses synthetic `InGameTrade` rows and a minimal `RomHandler` proxy/fake to cover null-request and placeholder/unsafe Species skips, all-skipped no `setInGameTrades(...)`, `isChangesMade=false`, skip counters and `hasSkippedTrades()`.
- UPR-FVX PR #40 implementation-side check is recorded as `./gradlew --offline :random:test` with `BUILD SUCCESSFUL`.
- In-Game Trades remain `blocked-pending-evidence`; no Gen3 writer test, ROM-Smoke, Species-Write-Smoke, text, Nickname/OT, IV or Trade Held Item randomization is authorized.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 160

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-non-rom-harness-plan`.
- PR #204 / Diagnose 159 was verified as merged before this block.
- UPR-FVX submodule remains pinned at `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Diagnose 160 plans a small non-ROM harness for the In-Game Trades guard. Result: `harness-plan-ready`.
- Recommended first scope: `TradeRandomizer` unit tests with synthetic `InGameTrade` rows and a fake/test `RomHandler`, proving null-request and unsafe Species rows skip before mutation, all-skipped input avoids `setInGameTrades(...)`, and skip counters stay observable.
- Optional Gen3 writer preserve coverage is useful only if it can be done without ROM bytes, broad refactor or generated artifacts.
- In-Game Trades remain `blocked-pending-evidence`; no Species-Write-Smoke, ROM smoke, build, Randomizer run, code change, submodule change, text, Nickname/OT, IV or Trade Held Item scope was performed.

# Session update - Diagnose 159

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-guard-code-review`.
- PR #203 / Follow-up 158B was verified as merged before this block.
- UPR-FVX submodule remains pinned at `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Diagnose 159 reviews `TradeRandomizer.java` and `Gen3RomHandler.java` read-only against the Diagnose 156 Preserve/Skip policy.
- Result: `review-pass-with-risks`. Unsafe In-Game Trade rows are skipped before mutation and preserved/skipped before Gen3 byte writes; no text, Nickname/OT, IV or Trade Held Item path was expanded.
- In-Game Trades remain `blocked-pending-evidence`; Species-Write-Smoke remains blocked. A later non-ROM harness is useful before any ROM-facing smoke is considered.
- No code, build, Randomizer run, ROM/save/output/log access, submodule change or external download was performed.

# Session update - Diagnose 158B

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-null-request-guard-followup`.
- UPR-FVX PR #39 was verified as merged into `compat/firered-gen9-cfru-dpe`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Diagnose 158B records the In-Game Trades Null-/Invalid-Species guard follow-up: `TradeRandomizer.java` skips unsafe rows before mutation and `Gen3RomHandler.java` preserves/skips unsafe rows before byte writes.
- In-Game Trades remain `blocked-pending-evidence`; no Species-Write-Smoke, text randomization, Nickname/OT randomization, IV randomization or Trade Held Item randomization is authorized by this follow-up.
- 158A Gradle context is recorded as an assumption/risk: `./gradlew --offline :romio:test :random:test` reported `BUILD SUCCESSFUL`, while an existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` failure line remained in the romio report.
- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file was touched.

# Session update - Diagnose 157

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-null-request-guard-plan`.
- PR #201 / Diagnose 156 is contained in `main` before this block.
- Diagnose 157 documents a read-only defensive Null-Requested-Species Skip/Guard plan for In-Game Trades.
- Result: In-Game Trades remain `blocked-pending-evidence`; the later minimal fix would skip/preserve rows with `requestedSpecies == null` or invalid/placeholder Species before mutation/write and report skipped/preserved rows clearly.
- No code, build, Randomizer run, Species-Write-Smoke, text randomization, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 156

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-preserve-skip-policy`.
- PR #200 / Diagnose 155 is contained in `main` before this block.
- Diagnose 156 defines the In-Game Trades Preserve/Skip policy from Diagnoses 152, 154 and 155.
- Result: `blocked-pending-evidence`. All modeled In-Game Trade rows stay preserve-only; no Species-Write-Smoke, Trade Held Item, IV, Nickname/OT or other In-Game Trade write work is allowed.
- `unsupported-dummy` remains plausible but unproven without additional read-only candidate-structure evidence; no code, build, Randomizer run, ROM/save/output/log access or external download was performed.

# Session update - Diagnose 155

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-active-row-candidates`.
- Diagnose 155 performs the requested read-only In-Game Trades active-row candidate check from UPR-FVX `TradeTableOffset`, `TradeTableSize`, `TradesUnused` and the 60-byte Gen3 row model.
- Result: blocked. The BPRE model exposes three non-unused rows, but Diagnose 152 evidence still has `requestedSpeciesNullCount=3`, `invalidTradeSpecies=6` and `placeholderTradeSpecies=6`, so no valid active row is confirmed.
- `unsupported-dummy` remains plausible but unproven; no Species-Write-Smoke, text randomization, build, Randomizer run, ROM/save/output/log access or code change was performed.

# Session update - Diagnose 154

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-table-model-diagnostics`.
- Diagnose 154 documents the UPR-FVX Gen3/FireRed In-Game Trades locator/table model using read-only source and documentation inspection.
- Result: blocked. The model expects ROM-entry `TradeTableOffset`, `TradeTableSize`, `TradesUnused` and 60-byte rows, but Diagnose 152 remains unresolved with null/invalid/placeholder Species fields.
- No code changes, no build, no Randomizer run, no ROM/save/output access, no write smoke and no text randomization were performed.

# Session update - Diagnose 153

- New branch: `analysis/upr-fvx-cfru-dpe-ingame-trades-table-model-blocker-plan`.
- PR #197 was merged; `main` was fast-forwarded before planning.
- Diagnose 153 documents the In-Game Trades locator/table-model blocker: `TradeTableOffset`, `TradeTableSize` and `TradesUnused` come from the Gen3 ROM entry, while `setInGameTrades(...)` dereferences requested Species and therefore is unsafe after Diagnose 152 null/invalid Species results.
- No code changes, no build, no Randomizer run, no write/save, no ROM/artifact access and no `02_external/**` edits were made.

# Session update - Diagnose 152

- New branch: `test/upr-fvx-cfru-dpe-ingame-trades-scope-diagnostics`.
- PR #196 was merged; `main` was fast-forwarded before the diagnostic.
- Read-only In-Game Trades candidate diagnostic completed as blocked/preflight. The candidate loaded, but the current UPR-FVX Gen3 BPRE trade-table model produced null/invalid Species fields and unstable fixed-length text terminator classification.
- No code changes, no build, no Randomizer run, no write/save, no output ROM and no private paths, ROM names, hashes, offsets or raw bytes were documented.

# Session update - Diagnose 151

- New branch: `analysis/upr-fvx-cfru-dpe-ingame-trades-scope-plan`.
- PR #195 was merged; `main` was fast-forwarded before planning.
- Diagnose 151 adds the In-Game Trades diagnostics scope plan as the next genuinely open GUI scope after Standard Wild, Special Wild documentation, item scopes and Held Items.
- Codepath finding: `GameRandomizer.maybeRandomizeInGameTrades()` dispatches to `TradeRandomizer.randomizeIngameTrades()`, which mutates `InGameTrade` records and writes through `RomHandler.setInGameTrades(...)`; Gen3 uses fixed-size trade table entries with Species, IV, held-item, nickname and OT fields.
- No code changes, no build, no Randomizer run, no ROM/artifact access and no `02_external/**` edits were made.

# 2026-05-15 - Diagnose 150

- Current branch documents CFRU/DPE Special Wild triggerability read-only.
- Result: no Special Wild system currently requires immediate UPR-FVX randomization for the tracked compatibility state.
- Day/Night headers exist but are sentinel-only/dormant; Swarms, Roamers, Wild Double and `gWildDataSwitch` are runtime-state driven; DexNav is partial/future; Raids need a separate future parser/write scope if required.
- Standard Wild remains P0-supported and was not retested.

# 2026-05-15 - Diagnose 149

- Current branch reconciles Randomizer feature coverage after Held Items closure and the merged Wild Encounters plan.
- Assessment: Standard Wild/Surfing/Fishing/Rock Smash P0 is already covered; do not spend the next block retesting Standard Wild.
- Genuinely open major scope: CFRU Day/Night and special Wild Encounter systems such as Swarms, Roamers, DexNav, Raids and Altering Cave/Tanoby-style cases.
- No code, build, Randomizer run, ROM access or tool-manifest change was made.

# 2026-05-15 - Diagnose 148

- Current branch plans Wild Encounters/Wild Pokemon Randomization as the next separate CFRU/DPE Gen9-BPRE scope after Held Items closure.
- Scope is explicitly separate from Wild Held Items, Trainer Pokemon, Starters, Static/Gift Pokemon, Field Items, Pickup and Shops.
- Code findings: Gen3 `getEncounters`/`setEncounters` use fixed EncounterArea/Encounter slot tables for Walking, Surfing, Rock Smash/Interact and Fishing, with CFRU/DPE extended BPRE species writes using SpeciesSet identity.
- No feature is promoted in this plan; next step is read-only Wild Encounters candidate diagnostics.

# 2026-05-15 - Diagnose 147

- Current branch records Starter Held Items + Ban Bad Write/Reload-Smoke.
- Smoke result: PASS; save/log/output/reload succeeded and `starterHeldItemReloadMismatches=0`.
- Ban Bad result: `badStarterHeldItemWrites=0`, `heldItemPoolAllowedSize=212`, `heldItemPoolNonBadSize=161`, `badStarterHeldItemPoolExcluded=51`.
- Safety metrics: invalid/unloaded/fallback/placeholder writes all `0`; Wild, Trainer, Field, Pickup and Shop scopes stayed unchanged.
- The tested Held Items scope is closed.

# 2026-05-15 - Diagnose 146

- Current branch records Starter Held Items Write/Reload-Smoke without Ban Bad.
- Smoke result: PASS; save/log/output/reload succeeded and `starterHeldItemReloadMismatches=0`.
- Starter model result: one shared Gen3/FRLG Starter Held Item slot changed from empty to non-empty and reloaded stably.
- Safety metrics: bad/TM/invalid/unloaded/fallback/placeholder Starter-Held-Item writes all `0`; Wild, Trainer, Field, Pickup and Shop scopes stayed unchanged.
- Starter Ban Bad remains the only open Starter Held Items sub-scope.

# 2026-05-15 - Diagnose 145

- Current branch records Regular Trainer Held Items filtered Write/Reload-Smoke.
- Smoke result: PASS; save/log/output/reload succeeded and `regularTrainerHeldItemReloadMismatches=0`.
- Filter result: `highestLevelHeldItemWrites=697`, `consumableHeldItemWrites=697`, `sensibleHeldItemWrites=697`, with `nonConsumableHeldItemWrites=0` and `nonSensibleHeldItemWrites=0`.
- Preserve result: Boss, Important and `shouldNotGetBuffs` Trainer Held Items stayed unchanged; Wild, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Next minimal scope is Starter Held Items unless Boss/Important filter combinations are explicitly required.

# 2026-05-15 - Diagnose 144

- Current branch plans Trainer Held Item filters as a separate sub-scope after Boss, Important and Regular no-filter smokes passed.
- Code findings: `Consumable Only`, `Sensible Items` and `Highest Level Only` are separate Trainer Held Item settings; no separate Trainer Held Item Ban Bad flag was found.
- Recommended next smoke: Regular Trainers only with the combined filter set, or split filters if narrower isolation is preferred.
- Starter Held Items remain unpromoted and should follow after the filter coverage decision.

# 2026-05-15 - Diagnose 143

- Current branch records Regular Trainer Held Items Write/Reload-Smoke.
- Smoke result: PASS; `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `regularTrainerHeldItemReloadMismatches=0`.
- Preserve result: Boss, Important and `shouldNotGetBuffs` Trainer Held Items stayed unchanged with mismatch counters all `0`.
- Safety metrics: invalid/unloaded/fallback/placeholder Trainer-Held-Item writes all `0`; Wild, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Trainer Held Items are now covered for Boss, Important and Regular Trainers in the tested no-filter scopes; filters and Starter Held Items remain open.

# 2026-05-15 - Diagnose 142

- Current branch records Important Trainer Held Items Write/Reload-Smoke.
- Smoke result: PASS; `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `importantTrainerHeldItemReloadMismatches=0`.
- Preserve result: Boss, Regular and `shouldNotGetBuffs` Trainer Held Items stayed unchanged with mismatch counters all `0`.
- Safety metrics: invalid/unloaded/fallback/placeholder Trainer-Held-Item writes all `0`; Wild, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Trainer Held Items are now covered for Boss and Important Trainers in the tested scopes; Regular, filters and Starter Held Items remain open.

# 2026-05-15 - Diagnose 141

- Current branch records Boss Trainer Held Items Write/Reload-Smoke.
- Smoke result: PASS; `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `bossTrainerHeldItemReloadMismatches=0`.
- Preserve result: Important, Regular and `shouldNotGetBuffs` Trainer Held Items stayed unchanged with mismatch counters all `0`.
- Safety metrics: invalid/unloaded/fallback/placeholder Trainer-Held-Item writes all `0`; Wild, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Trainer Held Items are now covered only for Boss Trainers in the tested scope; Important, Regular, filters and Starter Held Items remain open.

# 2026-05-15 - Diagnose 140

- Current branch records Wild/Encounter Held Items + Ban Bad Write/Reload-Smoke.
- Smoke result: PASS; `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `wildHeldItemReloadMismatches=0`.
- Ban Bad result: `badWildHeldItemWrites=0`, `wildHeldItemsBadBefore/After/Reload=174/0/0`, `badWildHeldItemPoolCandidates=51`, `badWildHeldItemPoolExcluded=51`.
- Safety metrics: invalid/unloaded/fallback/placeholder Wild-Held-Item writes all `0`; Trainer, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Wild/Encounter Held Items are now covered with and without Ban Bad in the tested scope; Trainer Held Items and Starter Held Items remain open.

# 2026-05-15 - Diagnose 139

- Current branch records Wild/Encounter Held Items Write/Reload-Smoke without Ban Bad.
- Smoke result: PASS; `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `wildHeldItemReloadMismatches=0`.
- Wild held item slots stayed stable at `5656/5656/5656`; non-zero slots changed as expected `526/312/312`.
- Safety metrics: invalid/unloaded/fallback/placeholder Wild-Held-Item writes all `0`; Trainer, Starter, Field, Pickup and Shop scopes stayed unchanged.
- Wild/Encounter Held Items without Ban Bad are GUI-compatible in the tested scope; Ban Bad, Trainer Held Items and Starter Held Items remain open.

# 2026-05-15 - Diagnose 138

- Current branch records read-only CFRU/DPE Gen9-BPRE Held Items candidate diagnostics.
- Result: PASS for read-only structure; `candidateLoaded=true`, `heldItemScanSuccessful=true`, Wild/Encounter, Trainer and Starter held-item paths are readable.
- Key metrics: `wildHeldItemsTotal=5656`, `wildHeldItemsNonZero=526`, `trainerHeldItemsTotal=1754`, `trainerHeldItemsNonZero=87`, `starterHeldItemsTotal=1`, `starterHeldItemsNonZero=0`.
- Safety metrics: invalid/unloaded held item IDs `0`, fallback held items `109`, placeholder held items `130`, `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `shopScopeChanged=false`.
- No feature promotion; next minimal block is Wild/Encounter Held Items smoke without Ban Bad.

# 2026-05-15 - Diagnose 137

- Current branch plans Held Items as the next separate CFRU/DPE Gen9-BPRE Randomizer scope after closed Shop Items.
- Scope split: Wild/Encounter Held Items, Trainer Held Items, and Starter Held Items if the candidate exposes a stable starter-held-item path.
- Read-only codepath finding: Wild/Encounter writes Species/BaseStats held-item fields, Trainer writes `TrainerPokemon.heldItem`, and Starter uses `getStarterHeldItems()` / `setStarterHeldItems(...)`.
- No smoke, no code changes, no ROM/artifact access, no submodule pin change, and no Held-Item feature promotion in this block.

# 2026-05-15 - Diagnose 136

- Current branch records Shop-only FVX-ITEM-009 Balance Prices + Cheap Rare Candies Write/Reload-Smoke.
- Smoke result: PASS with `ShopItemsMod.UNCHANGED`, `balanceShopPrices=true`, `addCheapRareCandiesToShops=true`.
- Shop-list result: `shopItemsTotal=157/180/180`, deltas `+23/+23`, `rareCandyWrites=23`, `skippedShopRareCandyWrites=20`, `shopItemReloadMismatches=0`.
- Price result: `balancedPriceWrites=132`, `rareCandyPriceTouched=true`, `rareCandyPriceReloadStable=true`, `priceReloadMismatches=0`.
- Shop Items scope is closed for the tested CFRU/DPE Gen9-BPRE GUI-compatible paths; Held Items diagnostics plan is the next major scope.

# Session update - 2026-05-15 - Diagnose 135

- Current branch records Shop-only FVX-ITEM-009 Cheap Rare Candies Write/Reload-Smoke.
- Smoke result: PASS with `ShopItemsMod.UNCHANGED`, `addCheapRareCandiesToShops=true`, `balanceShopPrices=false`.
- Shop-list result: `shopItemsTotal=157/180/180`, deltas `+23/+23`, `rareCandyWrites=23`, `skippedShopRareCandyWrites=20`, `shopItemReloadMismatches=0`.
- Price result: `rareCandyPriceTouched=true`, `rareCandyPriceReloadStable=true`, `priceReloadMismatches=0`.
- FVX-ITEM-009 is now individually covered for Balance Shop Prices and Cheap Rare Candies; their combination remains untested.

# Session update - 2026-05-15 - Diagnose 134

- Current branch records Shop-only FVX-ITEM-009 Balance Shop Prices Write/Reload-Smoke.
- Smoke result: PASS with `ShopItemsMod.UNCHANGED`, `balanceShopPrices=true`, `addCheapRareCandiesToShops=false`.
- Price result: `priceTableTouched=true`, `balancedPriceWrites=132`, `priceReloadMismatches=0`, price entry counts stay `1779`.
- Shop-list result: `shopCount=23`, `shopItemsTotal=157`, `shopItemReloadMismatches=0`, skipped Shop mismatches 0.
- FVX-ITEM-009 is promoted only for Balance Shop Prices; Cheap Rare Candies remain open.

# Session update - 2026-05-15 - Diagnose 133

- Current branch plans `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies` as a separate Shop-only subscope.
- Read-only codepath finding: Balance Shop Prices runs after the `ShopItemsMod` switch and can write prices independently of Shop item shuffle/random.
- Cheap Rare Candies appends one Rare Candy to each Shop via `setShops(...)` and sets the Rare-Candy price via `setShopPrices(...)`, so it combines Shop-list growth with price writes.
- Recommended order: Balance Shop Prices smoke first, Cheap Rare Candies smoke second, combination only after both individual smokes are reload-stable.
- FVX-ITEM-005..008 stay GUI-compatible only in their documented individual scopes; FVX-ITEM-009 remains Write modelliert until smoke.

# Session update - 2026-05-15 - Diagnose 132

- Current branch records Shop-only FVX-ITEM-008 Guarantee X Items Write/Reload-Smoke.
- Smoke result: PASS; `guaranteedXItemsExpected=7`, `guaranteedXItemsPresent=7`, `guaranteedXItemsReloadPresent=7`, missing counts stay 0.
- Stable metrics: `shopCount=23`, `mainGameShopCount=3`, `skippedShopCount=20`, `specialShopCount=3`, `shopItemsTotal=157`, `minShopLength=2`, `maxShopLength=9`, reload mismatches 0.
- Foreign scopes stayed false: `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`; prices stayed untouched.
- FVX-ITEM-008 now has separate GUI-compatible evidence for Guarantee Evolution Items and Guarantee X Items; the Evolution+X combination and FVX-ITEM-009 remain open.

# Session update - 2026-05-15 - Diagnose 131

- Current branch records Shop-only FVX-ITEM-008 Guarantee Evolution Items Write/Reload-Smoke.
- Smoke result: PASS; `guaranteedEvolutionItemsExpected=6`, `guaranteedEvolutionItemsPresent=6`, `guaranteedEvolutionItemsReloadPresent=6`, missing counts stay 0.
- Stable metrics: `shopCount=23`, `mainGameShopCount=3`, `skippedShopCount=20`, `specialShopCount=3`, `shopItemsTotal=157`, `minShopLength=2`, `maxShopLength=9`, reload mismatches 0.
- Foreign scopes stayed false: `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`; prices stayed untouched.
- FVX-ITEM-008 is promoted only for Guarantee Evolution Items in the tested Shop-only Random scope; Guarantee X Items and FVX-ITEM-009 remain open.

# 2026-05-15 - Shop Guarantee Items Scope Plan

- Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-shop-guarantee-items-scope-plan`.
- Diagnose 130 plant `FVX-ITEM-008 Guarantee Evolution/X Items` als separaten Shop-only Subscope.
- Read-only Befund: Guarantee Evolution/X wirkt nur bei `ShopItemsMod.RANDOM` ueber `setupGuaranteed()` und `placeNewItems(...)`.
- Placement zielt auf Special Shops; Guaranteed Items werden fuer MainGame-Special-Shops reserviert, SkipShops bleiben preserve-only.
- `FVX-ITEM-005`, `FVX-ITEM-006` und die einzeln getesteten `FVX-ITEM-007` Ban-Flags bleiben GUI-kompatibel; `FVX-ITEM-008` bleibt bis Smoke `Write modelliert`, `FVX-ITEM-009` bleibt offen.

# 2026-05-15 - Shop Items Random + Ban OP Smoke

- Arbeitsbranch: `test/upr-fvx-cfru-dpe-shop-items-random-ban-op-reload-smoke`.
- Diagnose 129 dokumentiert den Shop-only `FVX-ITEM-007` Subscope `ShopItemsMod.RANDOM + banOPShopItems=true`.
- Smoke bestanden: `opShopSetClassifiable=true`, Save, Log, Output und Reload erfolgreich; `shopItemReloadMismatches=0`, `opShopItemBannedWrites=0`, Skip-Shops und Preise unveraendert.
- `FVX-ITEM-007` ist fuer Ban Bad, Ban Regular und Ban OP einzeln belegt; Ban-Kombinationen, `FVX-ITEM-008` und `FVX-ITEM-009` bleiben offen.

# 2026-05-15 - Shop Items Random + Ban Regular Smoke

- Arbeitsbranch: `test/upr-fvx-cfru-dpe-shop-items-random-ban-regular-reload-smoke`.
- Diagnose 128 dokumentiert den Shop-only `FVX-ITEM-007` Subscope `ShopItemsMod.RANDOM + banRegularShopItems=true`.
- Smoke bestanden: `regularShopSetClassifiable=true`, Save, Log, Output und Reload erfolgreich; `shopItemReloadMismatches=0`, `regularShopItemBannedWrites=0`, Skip-Shops und Preise unveraendert.
- `FVX-ITEM-007` ist fuer Ban Bad und Ban Regular einzeln belegt; OP-Ban, `FVX-ITEM-008` und `FVX-ITEM-009` bleiben offen.

# 2026-05-15 - Shop Items Random + Ban Bad Smoke

- Arbeitsbranch: `test/upr-fvx-cfru-dpe-shop-items-random-ban-bad-reload-smoke`.
- Diagnose 127 dokumentiert den Shop-only `FVX-ITEM-007` Subscope `ShopItemsMod.RANDOM + banBadRandomShopItems=true`.
- Smoke bestanden: Save, Log, Output und Reload erfolgreich; `shopItemReloadMismatches=0`, `badShopItemWrites=0`, Skip-Shops und Preise unveraendert.
- `FVX-ITEM-005` und `FVX-ITEM-006` bleiben im getesteten Shop-only Scope GUI-kompatibel.
- `FVX-ITEM-007` ist nur fuer Ban Bad hochgestuft; Regular-Ban, OP-Ban, `FVX-ITEM-008` und `FVX-ITEM-009` bleiben offen.

# Session State Update - 2026-05-15 - Shop Item Bans scope plan

- Branch: `analysis/upr-fvx-cfru-dpe-shop-item-bans-scope-plan`.
- Workspace PR #170 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/126_shop_item_bans_scope_plan.md`.
- Read-only UPR-FVX analysis confirms `FVX-ITEM-007 Shop Item Bans` as a Shop-only sub-scope after `FVX-ITEM-006`.
- The Ban flags affect `ItemRandomizer.randomizeShopItems()` through `setupPossible()` and therefore require `ShopItemsMod.RANDOM`; they do not affect `ShopItemsMod.SHUFFLE` or `UNCHANGED`.
- Baseline from Diagnose 125 remains the pool anchor: `allowedShopItemPoolSize=536`, `nonBadShopItemPoolSize=485`, with `badShopItemsBefore/After/Reload=36` treated as existing inventory, not a Ban result.
- Recommended first executable smoke: Shop Random + Ban Bad only, with `banBadRandomShopItems=true` and Regular/OP/Guarantee/Price/Rare-Candy options disabled.
- `FVX-ITEM-005` and `FVX-ITEM-006` remain `GUI-kompatibel` in their tested Shop-only scopes. `FVX-ITEM-007` remains `Write modelliert`; `FVX-ITEM-008..009`, Field Items, Pickup and Held Items are not upgraded.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run, no ROM/log/output artefacts and no private artefact documentation.

# Session State Update - 2026-05-15 - Shop Items Random reload smoke

- Branch: `test/upr-fvx-cfru-dpe-shop-items-random-reload-smoke`.
- Workspace PR #169 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/125_shop_items_random_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Shop-only `FVX-ITEM-006 Shop Items Random` Write/Reload-Smoke.
- Sanitized result: `candidateFilesChecked=3`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`.
- Shop reload stayed stable: `shopCountBefore=23`, `shopCountAfter=23`, `shopCountReload=23`, `shopItemsTotalBefore=157`, `shopItemsTotalAfter=157`, `shopItemsTotalReload=157`, `shopItemReloadMismatches=0`, `shopLengthMismatchesAfter=0`, `shopLengthMismatchesReload=0`.
- Preserve/scope result: `skippedShopItemMismatchesAfter=0`, `skippedShopItemMismatchesReload=0`, `specialShopPolicyMismatches=0`, `priceTableTouched=false`, `priceReloadMismatches=0`, `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`.
- Pool result: active no-ban/no-TM Shop Random pool `allowedShopItemPoolSize=536`; comparison non-bad pool `nonBadShopItemPoolSize=485`; invalid/unloaded/fallback/placeholder writes all `0`.
- `FVX-ITEM-006 Shop Items Random` is now `GUI-kompatibel` in the tested Shop-only scope. `FVX-ITEM-007..009`, Field Items, Pickup and Held Items are not upgraded by this block.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Shop Items Shuffle reload smoke

- Branch: `test/upr-fvx-cfru-dpe-shop-items-shuffle-reload-smoke`.
- Workspace PR #168 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/124_shop_items_shuffle_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Shop-only `FVX-ITEM-005 Shop Items Shuffle` Write/Reload-Smoke.
- Sanitized result: `candidateFilesChecked=3`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`.
- Shop reload stayed stable: `shopCountBefore=23`, `shopCountAfter=23`, `shopCountReload=23`, `shopItemsTotalBefore=157`, `shopItemsTotalAfter=157`, `shopItemsTotalReload=157`, `shopItemReloadMismatches=0`, `shopLengthMismatchesAfter=0`, `shopLengthMismatchesReload=0`.
- Preserve/scope result: `skippedShopItemMismatchesAfter=0`, `skippedShopItemMismatchesReload=0`, `specialShopPolicyMismatches=0`, `priceTableTouched=false`, `priceReloadMismatches=0`, `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`.
- `FVX-ITEM-005 Shop Items Shuffle` is now `GUI-kompatibel` in the tested Shop-only scope. `FVX-ITEM-006..009`, Field Items, Pickup and Held Items are not upgraded by this block.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Shop Items candidate diagnostics

- Branch: `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-candidate`.
- Workspace PR #167 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/123_shop_items_scope_diagnostics_candidate.md`.
- An explicitly approved local CFRU/DPE Gen9-BPRE candidate source was used read-only for Shop diagnostics only; no private paths, ROM names, hashes, pointers, offsets, raw bytes or script data are documented.
- Sanitized result: `candidateFilesChecked=3`, `candidateLoaded=true`, `shopScanSuccessful=true`, `shopCount=23`, `mainGameShopCount=3`, `skippedShopCount=20`, `specialShopCount=3`, `emptyShopCount=0`, `shopItemsTotal=157`, `minShopLength=2`, `maxShopLength=9`.
- Structure/safety result: `terminatorModelStable=true`, `shopLengthMismatch=0`, `invalidShopItemIds=0`, `unloadedShopItemIds=0`, `fallbackShopItems=0`, `placeholderShopItems=0`, `badShopItems=36`, `tmShopItems=6`.
- Scope result: `shopPointerModelObserved=true`, `dataRewriterOrRepointingRisk=true`, `skipShopsPreserved=true`, `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`, `priceTableTouched=false`, `priceTableReadable=true`, `exceptionClass=none`, `stacktrace=none`.
- `FVX-ITEM-005..009` are not upgraded. Diagnose 123 only clears the prerequisite for a Shop-only Shuffle smoke. No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer write/save and no committed artefacts.

# Session State Update - 2026-05-15 - Shop Items scope diagnostics preflight

- Branch: `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics`.
- Workspace PR #166 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/122_shop_items_scope_diagnostics.md`.
- No explicitly approved local CFRU/DPE Gen9-BPRE candidate source was provided for this block; no private search was expanded and no ROM was touched.
- Result is blocked/preflight: `candidateFilesChecked=0`, `candidateLoaded=false`, `shopScanSuccessful=false`; Shop counts, lengths, terminator stability and item-safety counters remain `not_available`.
- Read-only codepath review keeps `shopPointerModelObserved=true` and `dataRewriterOrRepointingRisk=true` because Gen3 Shops use `ShopPointerOffsets`, `MainGameShops`, `SkipShops`, `Shop` and `DataRewriter<Shop>` in `Gen3RomHandler.setShops(...)`.
- `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`, `priceTableTouched=false`. No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer write/save and no private artefact documentation.

# Session State Update - 2026-05-15 - Shop Items scope diagnostics plan

- Branch: `analysis/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-plan`.
- Workspace PR #165 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/121_shop_items_scope_diagnostics_plan.md`.
- Shops are confirmed as the next separate CFRU/DPE Gen9-BPRE Item writer scope after Field Items and Pickup.
- Feature IDs stay separated: `FVX-ITEM-005` Shop Items Shuffle, `FVX-ITEM-006` Shop Items Random, `FVX-ITEM-007` Shop Item Bans, `FVX-ITEM-008` Guarantee Evolution/X Items and `FVX-ITEM-009` Balance Shop Prices / Cheap Rare Candies.
- Read-only UPR-FVX analysis identifies `Settings.ShopItemsMod`, `GameRandomizer.maybeRandomizeShops()`, `ItemRandomizer.shuffleShopItems()`, `randomizeShopItems()`, `addCheapRareCandiesToShops()`, `RomHandler.getShops()`/`setShops(...)`, `getShopPrices()`/`setShopPrices(...)`, `Gen3RomHandler` and `Shop` as the relevant paths.
- `Gen3RomHandler.setShops(...)` uses `DataRewriter<Shop>` and can repoint terminated Shop item lists, so later diagnostics must measure pointers, terminators, lengths, skipped/special/main-game policy and price writes separately.
- No Field Items, Pickup or Held Items are upgraded by this plan. No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run and no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items Random Ban Bad reload smoke

- Branch: `test/upr-fvx-cfru-dpe-pickup-items-random-ban-bad-reload-smoke`.
- Workspace PR #164 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/120_pickup_items_random_ban_bad_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Pickup-only `FVX-ITEM-010 Pickup Items Random` smoke with `banBadRandomPickupItems=true`.
- Sanitized result: `candidateFilesChecked=101`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`.
- Pickup reload stayed stable: `pickupItemsTotalBefore=16`, `pickupItemsTotalAfter=16`, `pickupItemsTotalReload=16`, `pickupItemReloadMismatches=0`, `pickupTableLengthMismatches=0`, `pickupProbabilityMismatches=0`, `pickupReloadLocatorRegression=false`.
- Ban-Bad result: `badPickupItemWrites=0`, `pickupBadItemPoolCandidates=51`, `pickupBadItemPoolExcluded=51`, `pickupPoolNonBadSize=485`.
- `FVX-ITEM-010 Pickup Items Random / Ban Bad Items` is now `GUI-kompatibel` in the tested Pickup-only scope. Field Items, Shops and Held Items remain separate scopes and are not upgraded by this block.
- No code changes, no `02_external/**` changes, no submodule pin change, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items Ban Bad scope plan

- Branch: `analysis/upr-fvx-cfru-dpe-pickup-items-ban-bad-scope-plan`.
- UPR-FVX PR #38 and Workspace PR #163 were verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/119_pickup_items_ban_bad_scope_plan.md`.
- Read-only UPR-FVX analysis confirms `banBadRandomPickupItems=true` only switches the Pickup candidate pool from `getAllowedItems()` to `getNonBadItems()` inside `ItemRandomizer.randomizePickupItems()`.
- Baseline from 115/118 remains valid: Pickup table count `16`, entry size `4`, probability slots `10`, allowed pool `536`, non-bad pool `485`, bad pool candidates `51`, TMs allowed for Pickup because `canTMsBeHeld=true` and `isTMsReusable=false`.
- Recommendation: run a direct Pickup-only Random Ban-Bad reload smoke next; no code fix is planned before that smoke.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run, no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items reload locator fix

- Branch: `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- Workspace PR #162 was verified as merged before branch creation.
- UPR-FVX fix commit: `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- UPR-FVX PR #38 opened: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/38>.
- Workspace now pins `02_external/upr-fvx` to `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- New protocol: `08_tests/randomizer/118_pickup_items_reload_locator_fix.md`.
- Fix is limited to `Gen3RomHandler` Pickup table localization: classic `PickupTableStartLocator` remains first path; CFRU/DPE Gen9-BPRE gets a metadata fallback that ignores randomized item-ID words and requires exactly one table candidate.
- Sanitized Pickup-only Random smoke with `banBadRandomPickupItems=false` passed: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `pickupLocatorSuccessful=true`, `pickupItemsTotalReload=16`, `pickupItemReloadMismatches=0`, `pickupLocatorMode=stable-metadata`, `pickupContentLocatorUsed=false`, `pickupReloadLocatorRegression=false`.
- `FVX-ITEM-010 Pickup Items Random` is GUI-compatible only for `banBadRandomPickupItems=false`; Pickup Ban Bad remains separate.
- No Field Items, Shops, Held Items, TM/HM/Tutor/Learnset, Scriptparser, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution or Text/Menu work was done.

# Session State Update - 2026-05-15 - Pickup Items reload locator blocker plan

- Branch: `analysis/upr-fvx-cfru-dpe-pickup-items-reload-locator-blocker-plan`.
- Workspace PR #161 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- New protocol: `08_tests/randomizer/117_pickup_items_reload_locator_blocker_plan.md`.
- Read-only UPR-FVX analysis narrows the Pickup Random reload blocker to table localization, not to the direct item write: `getPickupItems()` finds `PickupTableStartLocator` by content pattern and caches the offset only within the handler instance; `setPickupItems(...)` then changes the item ID words that are part of that pattern.
- This explains Diagnose 116: same-handler `pickupItemsTotalAfter=16`, but fresh reload has no cache and reports `pickupLocatorSuccessful=false` / `pickupItemsTotalReload=0`.
- Recommended next branch: `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- Pickup Ban Bad remains blocked until Pickup Random without Ban Bad is reload-stable.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run, no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items Random reload smoke blocked

- Branch: `test/upr-fvx-cfru-dpe-pickup-items-random-reload-smoke`.
- Workspace PR #160 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- New protocol: `08_tests/randomizer/116_pickup_items_random_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Pickup-only `FVX-ITEM-010 Pickup Items Random` smoke with `banBadRandomPickupItems=false`.
- Sanitized result: `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`.
- Blocker: after write, fresh reload cannot locate the Pickup table: `pickupLocatorSuccessful=false`, `pickupItemsTotalReload=0`, `pickupItemReloadMismatches=16`, `pickupTableLengthMismatches=1`, `pickupProbabilityMismatches=16`.
- Direct write-scope safety remained clean: `pickupItemsTotalBefore=16`, `pickupItemsTotalAfter=16`, `invalidPickupItemWrites=0`, `unloadedPickupItemWrites=0`, `fallbackPickupItemWrites=0`, `placeholderPickupItemWrites=0`, `fieldItemScopeChanged=false`, `shopItemScopeChanged=false`, `heldItemScopeChanged=false`.
- `FVX-ITEM-010` remains `Write modelliert` / reload-blocked. Pickup Ban Bad remains untested.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items scope diagnostics

- Branch: `test/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics`.
- Workspace PR #159 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- New protocol: `08_tests/randomizer/115_pickup_items_scope_diagnostics.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was scanned read-only for Pickup Items only.
- Sanitized result: `candidateFilesChecked=97`, `candidateLoaded=true`, `pickupScanSuccessful=true`, `pickupLocatorSuccessful=true`, `pickupItemsTotal=16`, `pickupExpectedCount=16`, `pickupEntrySize=4`, `pickupProbabilitySlots=10`, `pickupProbabilityModelStable=true`, `pickupTableLengthMismatch=0`, `pickupLocatorCandidateCount=1`.
- Item safety result: `pickupInvalidItemIds=0`, `pickupUnloadedItemIds=0`, `pickupFallbackItems=0`, `pickupPlaceholderItems=0`, `pickupBadItems=7`, `pickupTmItems=1`.
- Pool result: `pickupPoolAllowedSize=536`, `pickupPoolNonBadSize=485`, `pickupBadItemPoolCandidates=51`, `pickupBadItemPoolExcluded=51`, `pickupTmPoolPolicy=tms allowed`, `canTMsBeHeld=true`, `isTMsReusable=false`.
- Recommendation: run a Pickup-only Random write/reload smoke without Ban Bad first; keep Ban Bad separate afterwards.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer write/save, no Output-ROM committed, no private artefact documentation.

# Session State Update - 2026-05-15 - Pickup Items diagnostics scope plan

- Branch: `analysis/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics-plan`.
- Workspace PR #158 was verified as merged before branch creation.
- UPR-FVX pin remains `02_external/upr-fvx` at `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- New protocol: `08_tests/randomizer/114_pickup_items_scope_diagnostics_plan.md`.
- Pickup was split as the next separate Item writer scope after Field Items.
- Read-only UPR-FVX analysis identifies the active paths: `Settings.PickupItemsMod`, `GameRandomizer.maybeRandomizePickupItems()`, `ItemRandomizer.randomizePickupItems()`, `Gen3RomHandler.getPickupItems()` and `setPickupItems(...)`, plus `PickupItem.PROBABILITY_SLOTS=10`.
- Plan result: do a Pickup-only read-only candidate diagnostic before any write smoke, because `PickupTableStartLocator`, `PickupItemCount`, table length, Common/Rare/probability semantics and Item-ID pool safety must be confirmed for CFRU/DPE Gen9-BPRE.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run, no ROM/output/log/private artefact documentation.

# Session State Update - 2026-05-15 - Field Items Random Even Ban Bad reload smoke

- Branch: `test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke`.
- Workspace PR #157 was verified as merged before branch creation.
- UPR-FVX pin confirmed: `02_external/upr-fvx` at `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- New protocol: `08_tests/randomizer/113_field_items_random_even_ban_bad_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-003 Field Items Random even distribution` smoke with `banBadRandomFieldItems=true`.
- Sanitized result: `candidateFilesChecked=9`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`.
- Field-Items scope stayed stable: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`, visible/hidden mismatches `0`, TM/Non-TM slot mismatches `0`, `requiredFieldTMMissingAfter=0`.
- Ban-Bad result: `badFieldItemWrites=0`, `badFieldItemPoolCandidates=47`, `badFieldItemPoolExcluded=47`, `nonBadFieldItemPoolSize=485`.
- Random-Even result: `randomEvenQueueUsed=true`, `randomEvenTmDistributionStable=true`, `randomEvenNonTmDistributionStable=true`, `nonBadFieldItemQueueRefills=0`.
- `FVX-ITEM-004` is now `GUI-kompatibel` for Field Items Random and Random Even. Shops, Pickup and Held Items remain separate scopes and are not upgraded.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Field Items API TM-slot scope fix

- UPR-FVX fix commit: `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- UPR-FVX PR #37 opened: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/37>.
- New protocol: `08_tests/randomizer/108_field_items_api_tm_slot_scope_fix.md`.
- Fix is limited to Gen3RomHandler Field-Items get/set: CFRU/DPE Field-TM slots are exposed through the Field-Items API while TMs are not made globally allowed.
- `./gradlew :random:classes` passed in UPR-FVX.
- No fachlicher ROM Write-/Reload-Smoke ran in this block; `FVX-ITEM-002` remains `Write modelliert` until a separate sanitized reload smoke passes.
- Workspace now pins `02_external/upr-fvx` to `328e4441c2981d37aba9e2707a6f27f779b026e2`.

# Session State Update - 2026-05-15 - Field Items Random API TM-slot scope plan

- New protocol: `08_tests/randomizer/107_field_items_random_api_tm_slot_scope_plan.md`.
- Read-only UPR-FVX analysis confirms the active `FVX-ITEM-002` blocker is not the PR #36 TM-filler pool anymore: raw Field-Item diagnostics see `tmFieldItemSlots=28`, while `Gen3RomHandler.getFieldItems()` exposes `0` TM slots because the Field-Items API only includes slots whose current item is `isAllowed()`.
- TMs are loaded and classified as TMs, but the existing allowed-slot API scope filters them before `ItemRandomizer.randomizeTMFieldItems(...)`.
- `FVX-ITEM-001` remains `GUI-kompatibel`; `FVX-ITEM-002` remains `Write modelliert` until a CFRU/DPE-gated API TM-slot scope fix and reload smoke pass; `FVX-ITEM-003` and `FVX-ITEM-004` remain `Write modelliert`.

# Session State Update - 2026-05-15 - Field Items Random TM-pool reload smoke blocked

- Branch: `test/upr-fvx-cfru-dpe-field-items-random-tm-pool-reload-smoke`.
- UPR-FVX PR #36 and Workspace PR #150 were verified as merged before branch creation.
- Workspace pin confirmed: `02_external/upr-fvx` at `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd`.
- New protocol: `08_tests/randomizer/106_field_items_random_tm_pool_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-002 Field Items Random` smoke with `banBadRandomFieldItems=false`.
- Result remains blocked before output/reload: `saveSuccessful=false`, `outputRomExists=false`, `reloadSuccessful=false`, `exceptionClass=com.uprfvx.random.exceptions.RandomizationException`.
- The PR #36 pool deficit is no longer the active blocker: `randomTmUniquePoolSize=50`, `randomTmFillerAvailable=26`, `randomTmPoolDeficit=0`.
- New blocker: API TM-slot scope mismatch. Raw diagnostics established `tmFieldItemSlots=28`, but the Randomizer API path sees `randomTmNeededSlots=0` / `randomTmCurrentSlots=0`, so Required Field TMs (`24`) exceed visible TM slots.
- `FVX-ITEM-002` remains `Write modelliert`; no GUI-compatible upgrade.

# Session State Update - 2026-05-15 - Field Items Random TM-pool fix

- Branch: `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix`.
- Workspace PR #149 was verified as merged before branch creation.
- UPR-FVX fix commit: `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd`.
- UPR-FVX PR #36 opened: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/36>.
- New protocol: `08_tests/randomizer/105_field_items_random_tm_pool_fix.md`.
- Fix is limited to `ItemRandomizer.randomizeTMFieldItems(...)`: Required Field TMs stay mandatory, the filler pool is deduplicated from loaded TM items plus current Field-TM slots, and pool deficits now fail with a clear `RandomizationException`.
- No ROM Write-/Reload-Smoke was executed in this block; `FVX-ITEM-002` is not upgraded until a separate sanitized Field-Items-only reload smoke passes.
- Workspace now pins `02_external/upr-fvx` to `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd`.
- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Scriptparser, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution or Text/Menu work was done.

# Session State Update - 2026-05-15 - Field Items Random TM-pool blocker plan

- Branch: `analysis/upr-fvx-cfru-dpe-field-items-random-tm-pool-blocker-plan`.
- Workspace PR #148 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/104_field_items_random_tm_pool_blocker_plan.md`.
- Read-only analysis confirms the likely blocker for `FVX-ITEM-002 Field Items Random`: `ItemRandomizer.randomizeTMFieldItems(...)` requires the generated unique TM set size to exactly match the current TM Field Item slot count and throws `RandomizationException` otherwise.
- Relevant data: `tmFieldItemSlots=28`, `requiredFieldTMsTotal=24`, `requiredFieldTMPresent=24`, `requiredFieldTMMissing=0`; Diagnose 103 failed before output/reload but preserve counters stayed stable.
- `FVX-ITEM-001` remains `GUI-kompatibel`; `FVX-ITEM-002`, `FVX-ITEM-003`, and `FVX-ITEM-004` remain `Write modelliert`.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no Randomizer run, no private artefact documentation.

# Session State Update - 2026-05-15 - Field Items Random reload smoke blocked

- Branch: `test/upr-fvx-cfru-dpe-field-items-random-reload-smoke`.
- Workspace PR #147 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/103_field_items_random_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=false`.
- Sanitized result: `candidateFilesChecked=9`, `candidateLoaded=true`, `smokeExecuted=true`, but `saveSuccessful=false`, `outputRomExists=false`, `reloadSuccessful=false`, `exceptionClass=com.uprfvx.random.exceptions.RandomizationException`, `stacktrace=com.uprfvx.random.exceptions.RandomizationException`.
- Field-Items scope remained stable until abort: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `requiredFieldTMMissingAfter=0`, `disallowedFieldItemWrites=0`, `scriptPatternExpansion=0`, `badFieldItemWrites=0`.
- `FVX-ITEM-001` remains `GUI-kompatibel` for the narrow Shuffle scope; `FVX-ITEM-002` remains `Write modelliert` and blocked by the Random TM-pool path; `FVX-ITEM-003` and `FVX-ITEM-004` remain `Write modelliert`.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-15 - Field Items allowed-slot reload smoke

- Branch: `test/upr-fvx-cfru-dpe-field-items-allowed-slot-reload-smoke`.
- Workspace PR #146 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/102_field_items_allowed_slot_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-001 Field Items Shuffle` Write-/Reload-Smoke.
- Sanitized result: `candidateFilesChecked=94`, `candidateLoaded=true`, `smokeExecuted=true`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `reloadSuccessful=true`, `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`, visible/hidden reload mismatches `0`, TM/Non-TM slot mismatches `0`, `requiredFieldTMMissingAfter=0`, `disallowedFieldItemWrites=0`, `scriptPatternExpansion=0`, `exceptionClass=none`, `stacktrace=none`.
- `FVX-ITEM-001` is now `GUI-kompatibel` for the tested narrow Shuffle scope.
- `FVX-ITEM-002`, `FVX-ITEM-003` and `FVX-ITEM-004` remain `Write modelliert` pending separate Random / Random Even / Ban Bad Items smokes.
- No code changes, no `02_external/**` changes, no submodule pin change, no build, no committed ROM/log/output artefacts, no private artefact documentation.

# Session State Update - 2026-05-14 - Field Items allowed-slot guard decision

- Branch: `compat/upr-fvx-cfru-dpe-field-items-allowed-slot-write-guard`.
- Workspace PR #145 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/101_field_items_allowed_slot_write_guard.md`.
- UPR-FVX remains pinned to `2697511da9a97df4c29c00dfda8b40e556020489`; no UPR-FVX code change or submodule pin change was needed.
- Guard decision: existing `Gen3RomHandler.getFieldItems()` / `setFieldItems(...)` already restricts writes to allowed Field-Item slots and preserves disallowed/progression/key/system/pattern-unmatched slots.
- No Write-/Reload-Smoke ran in this block because no local CFRU/DPE Gen9-BPRE candidate was explicitly approved for this write block.
- `FVX-ITEM-001..004` remain `Write modelliert` pending a separate Field-Items-only Write-/Reload-Smoke, preferably starting with `FVX-ITEM-001 Field Items Shuffle`.
- No code changes, no `02_external/**` changes, no Randomizer write/save, no build, no output ROM, no private artefact documentation.

# Session State Update - 2026-05-14 - Field Items candidate diagnostics

- Branch: `test/upr-fvx-cfru-dpe-field-items-scope-diagnostics-candidate`.
- Workspace PR #144 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/100_field_items_scope_diagnostics_candidate.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was scanned read-only for Field Items only.
- Sanitized result: `candidateFilesChecked=94`, `candidateLoaded=true`, `fieldItemScanSuccessful=true`, `fieldItemsTotal=339`, `visibleFieldItemSlots=168`, `hiddenFieldItemSlots=171`, `allowedFieldItemSlots=280`, `disallowedFieldItemSlots=59`, `tmFieldItemSlots=28`, `nonTmFieldItemSlots=311`, `requiredFieldTMMissing=0`, `invalidFieldItemIds=0`, `unloadedFieldItemIds=0`, `scriptPatternUnmatchedItemBalls=10`, `exceptionClass=none`, `stacktrace=none`.
- No code changes, no `02_external/**` changes, no Randomizer write/save, no build, no output ROM, no private artefact documentation.
- `FVX-ITEM-001..004` remain `Write modelliert`; next recommended block is a guarded Field-Items write/smoke branch.

# Session State Update - 2026-05-14 - Field Items diagnostics blocked

- Branch: `test/upr-fvx-cfru-dpe-field-items-scope-diagnostics`.
- Workspace PR #143 was verified as merged before branch creation.
- New protocol: `08_tests/randomizer/099_field_items_scope_diagnostics.md`.
- Field-Items-only diagnostics did not run because no explicitly approved local CFRU/DPE Gen9-BPRE candidate was provided in this block.
- Sanitized preflight: `candidateFilesChecked=0`, `candidateLoaded=false`, `fieldItemScanSuccessful=false`, `exceptionClass=none`, `stacktrace=none`.
- No code changes, no `02_external/**` changes, no Randomizer write/save, no build, no output ROM, no ROM/private artefact documentation.
- `FVX-ITEM-001..004` remain `Write modelliert`.
- Planned next block when a candidate is explicitly approved: `test/upr-fvx-cfru-dpe-field-items-scope-diagnostics-candidate`.

# Session State Update - 2026-05-14 - Field Items diagnostics scope plan

- Branch: `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`.
- New protocol: `08_tests/randomizer/098_field_items_scope_diagnostics_plan.md`.
- Field Items were split from the combined Field Items / Shops / Pickup planning track as the first dedicated item-writer diagnostic scope.
- Scope remains read-only: no code changes, no `02_external/**` changes, no Randomizer run, no build, no ROM or private artefact documentation.
- Planned next block: `test/upr-fvx-cfru-dpe-field-items-scope-diagnostics` for an aggregated Field-Items-only diagnostic run.

## 2026-05-14 - CFRU/DPE Field Items / Shops / Pickup Scope Plan

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/097_field_items_shops_pickup_scope_plan.md` erstellt.
- UPR-FVX bleibt auf `2697511da9a97df4c29c00dfda8b40e556020489` gepinnt.
- Palette Diagnose 096 bleibt blockiert abgeschlossen; `FVX-GFX-001..004` bleiben `Write modelliert`.
- Field Items, Shops und Pickup wurden gegen `GameRandomizer`, `Settings`, `ItemRandomizer`, `Gen3RomHandler`, `RomHandler`, `Shop`, `PickupItem`, `Item` und GUI-Texte read-only getrennt.
- Ergebnis: kein gemeinsamer Fixblock. Field Items sind Map-/Script-/Hidden-Item-Offset-Writer, Pickup ist ein begrenzter Table-Writer, Shops sind Terminator-/DataRewriter-/Repointing- und Preis-Scope.
- Gemeinsame Item-Pool-/Bad-/Banned-Policy ist noetig, aber die Write-/Reload-Risiken muessen getrennt bleiben.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build, kein Randomizer-Lauf und kein ROM-/Artefaktzugriff.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`: Field Items zuerst read-only planen/diagnostizieren; Shops und Pickup separat halten.

## 2026-05-14 - Post-Merge Sync nach blockiertem Palette Normal Single-owner Reload-Smoke

Workspace-Branch: `docs/post-merge-palette-normal-smoke-blocked-sync`

Post-Merge-Stand:

- UPR-FVX PR #35 ist gemerged.
- Workspace PR #139 ist gemerged.
- Workspace PR #140 ist gemerged.
- Workspace pinnt `02_external/upr-fvx` weiter auf `2697511da9a97df4c29c00dfda8b40e556020489`.
- Diagnose 096 ist auf `main` verfuegbar und als blockierter Reload-Smoke abgeschlossen.

Diagnose 096 bleibt blockiert:

- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- `candidateSpeciesTotal=0`
- kein fachlicher Palette-Write-/Reload-Smoke
- keine Hochstufung fuer `FVX-GFX-001`

Feature-Status:

- `FVX-GFX-001` bleibt `Write modelliert`: Guard-Fix vorhanden, Reload-Smoke blockiert bis ein UPR-FVX-ladbarer CFRU/DPE Gen9-BPRE-Kandidat mit `candidateSpeciesTotal=1439` verfuegbar ist.
- `FVX-GFX-002` bleibt `Write modelliert`.
- `FVX-GFX-003` bleibt `Write modelliert`.
- `FVX-GFX-004` bleibt `Write modelliert`.

Naechster empfohlener P1-Block:

- `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan`

Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build, kein Randomizer-Lauf und kein ROM-/Artefaktzugriff.

## 2026-05-14 - Palette Normal Single-owner Reload-Smoke blockiert

Arbeitsbranch: `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`

Diagnose 096 wurde als sanitisiert blockierter Reload-Smoke dokumentiert. Der lokale Preflight fand 94 BPRE-Kandidaten, aber keinen UPR-FVX-ladbaren CFRU/DPE-Gen9-BPRE-Zielkandidaten mit `candidateSpeciesTotal=1439`.

Aggregierte Zähler:

- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- `exceptionClass=none`
- `stacktrace=none`

Es wurde kein fachlicher Palette-Write-/Reload-Smoke ausgeführt. `FVX-GFX-001` wird nicht hochgestuft; `FVX-GFX-001..004` bleiben im Palette-Bereich konservativ bewertet. UPR-FVX bleibt auf `2697511da9a97df4c29c00dfda8b40e556020489` gepinnt.

# Session State

# Session State Update - 2026-05-15 - Field Items Random Ban Bad reload smoke

- New protocol: `08_tests/randomizer/112_field_items_random_ban_bad_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=true` on UPR-FVX `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Save/log/output/reload succeeded with `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, and `fieldItemReloadMismatches=0`.
- Required Field TMs remained complete, TM/Non-TM slot mismatches stayed `0`, `badFieldItemWrites=0`, and no Shop/Pickup/Held-Item scope change was observed.
- The smoke measured `badFieldItemPoolCandidates=47` and `badFieldItemPoolExcluded=47`, not the 75er baseline expected by Diagnose 111; therefore `FVX-ITEM-004` is only tested for `FieldItemsMod.RANDOM`, not fully GUI-compatible.
- Recommended next block: `test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke`.


# Session State Update - 2026-05-15 - Field Items Ban Bad scope plan

- New protocol: `08_tests/randomizer/111_field_items_ban_bad_scope_plan.md`.
- Read-only UPR-FVX analysis confirms `banBadRandomFieldItems` affects only `ItemRandomizer.randomizeNonTMFieldItems(...)`: it switches the Non-TM pool from `getAllowedItems()` to `getNonBadItems()` and removes TMs afterward.
- `randomizeTMFieldItems(...)` does not read `banBadRandomFieldItems`; Required Field TMs remain a separate TM-pool requirement.
- Diagnose 100 provides the key Ban-Bad baseline: `badFieldItems=75`, `badItemBanCandidates=75`, `badItemBanRemovalsNeeded=75`.
- Recommended first smoke: `test/upr-fvx-cfru-dpe-field-items-random-ban-bad-reload-smoke` for `FVX-ITEM-002 Field Items Random` with `banBadRandomFieldItems=true`; Random Even + Ban Bad stays separate afterward.
- `FVX-ITEM-004` remains `Write modelliert`; no code change, no Randomizer run, no build, no `02_external/**` change and no private artifact documentation.

# Session State Update - 2026-05-15 - Field Items Random Even reload smoke

- New protocol: `08_tests/randomizer/110_field_items_random_even_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-003 Field Items Random even distribution` Write-/Reload-Smoke with `banBadRandomFieldItems=false` on UPR-FVX `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Save/log/output/reload succeeded. Field Items remained stable: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`.
- API TM-slot scope remains stable: `apiTmFieldItemSlots=28`, `rawTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`, `tmGloballyAllowedChanged=false`.
- Random-Even TM pool is stable: `randomTmNeededSlots=28`, `randomTmCurrentSlots=28`, `randomTmRequiredTotal=24`, `randomTmFillerNeeded=4`, `randomTmFillerAvailable=26`, `randomTmPoolDeficit=0`, `randomTmResultUniqueSize=28`.
- Preserve counters stayed stable: `disallowedFieldItemWrites=0`, `invalidFieldItemWrites=0`, `unloadedFieldItemWrites=0`, `fallbackFieldItemWrites=0`, `placeholderFieldItemWrites=0`, `scriptPatternExpansion=0`.
- `FVX-ITEM-003` is now `GUI-kompatibel` only for the narrow Field-Items Random-Even scope with `banBadRandomFieldItems=false`; `FVX-ITEM-004` Ban Bad Items remains `Write modelliert`.

# Session State Update - 2026-05-15 - Field Items API TM-slot reload smoke

- New protocol: `08_tests/randomizer/109_field_items_api_tm_slot_reload_smoke.md`.
- A locally approved CFRU/DPE Gen9-BPRE candidate was used for a Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=false` on UPR-FVX `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Save/log/output/reload succeeded. Field Items remained stable: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`.
- API TM-slot scope is confirmed: `apiTmFieldItemSlots=28`, `rawTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`, `tmGloballyAllowedChanged=false`.
- Random-TM pool is stable: `randomTmNeededSlots=28`, `randomTmCurrentSlots=28`, `randomTmRequiredTotal=24`, `randomTmFillerNeeded=4`, `randomTmFillerAvailable=26`, `randomTmPoolDeficit=0`, `randomTmResultUniqueSize=28`.
- Preserve counters stayed stable: `disallowedFieldItemWrites=0`, `invalidFieldItemWrites=0`, `unloadedFieldItemWrites=0`, `fallbackFieldItemWrites=0`, `placeholderFieldItemWrites=0`, `scriptPatternExpansion=0`.
- `FVX-ITEM-002` is now `GUI-kompatibel` only for the narrow Field-Items Random scope with `banBadRandomFieldItems=false`; `FVX-ITEM-003` Random Even and `FVX-ITEM-004` Ban Bad Items remain `Write modelliert`.

## 2026-05-14 - CFRU/DPE Palette Normal Single-owner Write Guard Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`

UPR-FVX-Pin: `2697511da9a97df4c29c00dfda8b40e556020489`

Aktueller Stand:

- UPR-FVX-Fix erstellt: `2697511da9a97df4c29c00dfda8b40e556020489`.
- UPR-FVX PR #35 geoeffnet: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/35`.
- Neues Diagnose-/Fixprotokoll `08_tests/randomizer/095_palette_normal_single_owner_write_guard_fix_diagnostics.md` erstellt.
- `Gen3RomHandler.savePokemonPalettes()` nutzt im CFRU/DPE-Gen9-BPRE-Gate nun einen Normal-only-Single-owner-Guard.
- Shiny-, Shared-, Missing-, Invalid-, Decode-failed-, Cross-kind-shared- und unsichere Forme-Faelle werden nicht an `rewriteCompressedPalette()` / `DataRewriter` uebergeben.
- Vanilla-/Nicht-CFRU-Palette-Pfade bleiben unveraendert.
- UPR-FVX Checks: `git diff --check` sauber, `./gradlew clean :random:jar` erfolgreich.
- `./gradlew test` beendet mit Gradle-Status 0, meldet aber bestehende Failures in `PlayerCharacterGraphicsTest` und `Gen1CmpTest`.
- Kein ROM-/Reload-Smoke wurde in diesem Block ausgefuehrt; `FVX-GFX-001` bleibt bis zu einem separaten Reload-Smoke `Write modelliert`.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit.

Naechster sinnvoller Schritt:

- `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`: den Normal-only-Single-owner-Palette-Guard mit einem sanitisierten Reload-Smoke fachlich bestaetigen. Erwartet: `normalPaletteWriteCandidates=385`, `normalPaletteWriteAttempts <= 385`, `normalPaletteReloadMismatches=0`, ausgeschlossene Kategorien mit `WriteAttempts=0`, `exceptionClass=none`, `stacktrace=none`.

## 2026-05-14 - CFRU/DPE Palette Single-owner Normal-only Fix-Scope Plan

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-palette-single-owner-normal-only-fix-scope-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/094_palette_single_owner_normal_only_fix_scope_plan.md` erstellt.
- Diagnose 093 bleibt die Datenbasis: `candidateWritablePalettes=385`, `candidateWritableNormalPalettes=385`, `candidateWritableShinyPalettes=0`, `skipPaletteEntries=2493`, `crossKindSharedPalettePointers=1809`.
- Planergebnis: ein spaeterer Fix-/Smoke-Scope ist reviewbar, aber nur fuer Normal-Paletten, die single-owner, dekomprimierbar, gueltig, nicht shared, nicht missing, nicht invalid, nicht decode-failed und nicht cross-kind shared sind.
- Shiny-, Shared-, Invalid-, Missing-, Decode-failed- und unsichere Forme-/Expanded-Mapping-Faelle bleiben preserve-only.
- Der bestehende komprimierte Palette-Writer laeuft ueber `rewriteCompressedPalette()`/`DataRewriter`; ein echter Write-Smoke muss Repointing entweder bewusst zulassen und nachweisen oder den Fix zurueckstellen.
- Fuer den ersten spaeteren Smoke ist nur `FVX-GFX-001 Pokemon Palettes Random` als Normal-only-Farbtraeger geeignet.
- `FVX-GFX-002 Follow Types` bleibt ein separater spaeterer Normal-only-Smoke ohne TypeChart-/Species-Type-Scope.
- `FVX-GFX-003 Follow Evolutions` und `FVX-GFX-004 Shiny From Normal` bleiben ausserhalb des ersten Fix-Smokes.
- `FVX-GFX-001..004` bleiben aktuell `Write modelliert`.
- Keine Codeaenderung, kein Build, kein Randomizer-Lauf, kein ROM-Zugriff, keine Submodule-Pin-Aenderung.

Naechster sinnvoller Schritt:

- `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`: engen UPR-FVX-Writer-Gate-Fix fuer sichere Normal-Palette-Single-owner-Kandidaten vorbereiten und mit sanitisiertem Reload-Smoke dokumentieren.

## 2026-05-14 - CFRU/DPE Palette Pointer / Compression Diagnostics Run

Workspace-Branch: `test/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neuer sanitiserter Diagnosebericht `08_tests/randomizer/093_palette_pointer_compression_diagnostics.md` erstellt.
- Der lokale Diagnose-Harness blieb ignored unter `05_builds/**` und wurde nicht committed.
- Der Lauf blieb read-only: keine Palette-Randomization, kein Writer-Fix, kein Repointing, kein Build, keine Output-ROM.
- Kandidaten-Preflight: `candidateFilesChecked=94`, `candidateLoaded=true`, `palettePointerScanSuccessful=true`, `candidateSpeciesTotal=1439`, `exceptionClass=none`, `stacktrace=none`.
- Pointer-/Compression-Ergebnis: `candidateWritablePalettes=385`, `candidateWritableNormalPalettes=385`, `candidateWritableShinyPalettes=0`.
- Skip-/Preserve-Scope: `skipPaletteEntries=2493`, `skippedSharedPalettes=329`, `skippedInvalidPalettes=592`, `skippedMissingPalettes=38`, `skippedDecodeFailedPalettes=625`.
- Risikobefund: `crossKindSharedPalettePointers=1809`, `sharedPointerGroups=775`, `largestSharedPointerGroupSize=156`, `singleOwnerBothNormalAndShinySpecies=0`.
- Ergebnis: ein spaeterer enger Fix-/Smoke-Scope ist nur normal-palette-only, single-owner/decompressible realistisch; Shiny und alle shared/invalid/missing/decode-failed Paletten bleiben preserve-only.
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`.
- Keine privaten Pfade, ROM-Namen, Hashes, Raw Pointer, Offsets, Logs oder Output-ROM-Pfade dokumentiert.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-palette-single-owner-normal-only-fix-scope-plan`: read-only planen, ob ein normal-palette-only Single-owner/decompressible Fix-/Smoke-Scope reviewbar eng genug ist. Shiny, shared, invalid, missing und decode-failed Paletten preserve-only lassen.

## 2026-05-14 - CFRU/DPE Palette Pointer / Compression Diagnostics Plan

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/092_palette_pointer_compression_diagnostics_plan.md` erstellt.
- Der Plan konkretisiert die von Diagnose 091 geforderte Palette-Pointer-/Compression-Diagnose.
- Relevante Codepfade: `Gen3RomHandler` mit `PokemonNormalPalettes`, `PokemonShinyPalettes`, `loadPokemonPalettes()`, `savePokemonPalettes()`, `rewriteCompressedPalette(...)`, `pokedexToInternal[...]`, `AbstractGBRomHandler.DataRewriter`, `GameRandomizer`, `Settings.PokemonPalettesMod` und `Gen3to5PaletteRandomizer`.
- Die spaetere Diagnose soll Normal-/Shiny-Palette-Pointer aggregiert klassifizieren: dekomprimierbar, nicht dekomprimierbar, single-owner, shared, missing/null, invalid/out-of-ROM, duplicate und candidateWritable.
- Raw Pointer, Offsets, ROM-Namen, Hashes, lokale Pfade, Logauszuege und Output-ROMs duerfen nicht dokumentiert werden.
- Policy: shared, missing, invalid und decode-failed Paletten bleiben preserve-only; nur dekomprimierbare single-owner Kandidaten kommen fuer einen spaeteren engen Fix-/Smoke-Scope in Frage.
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build, kein Randomizer-Lauf und kein ROM-/Artefaktzugriff.

Naechster sinnvoller Schritt:

- `test/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics`: nur bei expliziter lokaler Freigabe einen sanitisierten read-only Diagnose-Lauf fuer Palette-Pointer, Compression, Owner-Counts und sichere Kandidaten ausfuehren. Kein Palette-Fix, kein Repointing.

## 2026-05-14 - CFRU/DPE Palette Randomization Preserve/Repoint Plan

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/091_palette_randomization_preserve_repoint_plan.md` erstellt.
- Der Plan trennt bestehende Palette-Safety/Skip-Unchanged-Save von echter geaenderter `PokemonPalettesMod.RANDOM`-Randomization.
- Relevante Codepfade: `GameRandomizer.maybeRandomizePokemonPalettes()`, `Settings.PokemonPalettesMod`, `RandomizerGUI`, `Gen3to5PaletteRandomizer`, `Gen3RomHandler.loadPokemonPalettes()`, `savePokemonPalettes()`, `rewriteCompressedPalette()` und `AbstractGBRomHandler.DataRewriter`.
- Ergebnis: echte Palette-Randomization ist fuer CFRU/DPE ein komprimierter Repointing-/Shared-Pointer-Writer und noch nicht direkt fixbar.
- Belegte Safety bleibt: missing/invalid Paletten defensiv laden/skippen und unveraenderte Paletten beim Save nicht neu schreiben.
- Offene Risiken: compressed decode, FreeSpace/Repointing, Single-Pointer-Annahme, Shared-Palette-Pointer, fehlende/invalid Slots, Forme-/Alt-Species-Zuordnung und `pokedexToInternal`-Grafikpfad.
- Empfehlung: vor jedem Fix eine read-only Palette-Pointer-/Compression-Diagnose fuer dekomprimierbare, single-owner, shared, missing und invalid Normal-/Shiny-Paletten.
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build, kein Randomizer-Lauf und kein ROM-/Artefaktzugriff.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics-plan`: read-only Diagnoseplan fuer Palette-Pointer-Eigentum, Dekomprimierbarkeit, Shared-Pointer, missing/invalid Slots und moegliche spaetere single-owner Write-Grenzen.

## 2026-05-14 - Post-Merge-Doku-Sync nach blockiertem Move Names Retry

Workspace-Branch: `docs/post-merge-move-names-retry-blocked-sync`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Workspace PR #133 ist gemerged.
- Diagnose 090 ist als blockierter Retry abgeschlossen.
- `candidateFilesChecked=94`.
- `candidatePreflightSuccessful=false`.
- Es gab keinen fachlichen Name-only fixed-length Reload-Smoke, weil kein explizit freigegebener CFRU/DPE Gen9-BPRE-Kandidat mit `moves.total=992` und `991:PsychicNoise` verfuegbar war.
- `FVX-MOVE-005` wird nicht hochgestuft und bleibt `Write modelliert`.
- `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` und `FVX-MOVE-006` bleiben GUI-kompatibel.
- UPR-FVX PR #34 ist weiterhin als gemerged dokumentiert; der Workspace-Pin bleibt `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build und kein Randomizer-Lauf.

Naechster sinnvoller Schritt:

- P1-Arbeit auf `analysis/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint-plan` verschieben. `FVX-MOVE-005` bleibt wartend, bis ein explizit freigegebener 992-/`991:PsychicNoise`-Kandidat verfuegbar ist.

## 2026-05-14 - CFRU/DPE Move Names fixed-length Reload-Smoke Retry

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke-retry`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/090_move_names_fixed_length_reload_smoke_retry.md` erstellt.
- Ziel war ein erneuter enger Candidate-Preflight fuer `FVX-MOVE-005` Randomize Move Names im bestehenden Gen3 fixed-length `MoveNames`-Pfad.
- Das lokale Preflight pruefte freigegebene private/ignored Kandidaten, ohne private Pfade, ROM-Namen, Hashes, Logauszuege oder Output-ROMs zu dokumentieren.
- Ergebnis: `candidateFilesChecked=94`, `candidatePreflightSuccessful=false`, `candidateMovesTotal=not available`, `candidateHighestMove=not available`.
- Der fachliche Name-only Reload-Smoke wurde nicht ausgefuehrt, weil kein Kandidat die Mindestkriterien `moves.total=992` und `991:PsychicNoise` erfuellte.
- `saveSuccessful`, `logSuccessful`, Output-, Reload-, Name-Length-, Terminator-/Padding-, Description-Pointer- und Name-Reload-Zaehler bleiben daher nicht fachlich ausgewertet.
- Keine Move Descriptions, keine Pointer-/Repointing- oder Text/Menu-Umsetzung, keine MoveData-Byte-Writer-Aenderung.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build und kein Randomizer-Smoke nach blockiertem Preflight.
- `FVX-MOVE-005` wird nicht hochgestuft und bleibt `Write modelliert`; `FVX-MOVE-001/002/003/004/006` bleiben GUI-kompatibel.

Naechster sinnvoller Schritt:

- `FVX-MOVE-005` vorerst konservativ halten. Den Name-only fixed-length Smoke nur erneut starten, wenn ein lokal freigegebener CFRU/DPE Gen9-BPRE-Kandidat vorab eindeutig `moves.total=992` und `991:PsychicNoise` meldet; ansonsten keinen Smoke ausfuehren.

## 2026-05-14 - CFRU/DPE Move Names fixed-length Reload-Smoke

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/089_move_names_fixed_length_reload_smoke.md` erstellt.
- Ziel war ein enger Name-only Reload-Smoke fuer `FVX-MOVE-005` Randomize Move Names im bestehenden Gen3 fixed-length `MoveNames`-Pfad.
- Ein lokaler, nicht committeter Harness unter ignored `05_builds/**` wurde erstellt.
- Der fachliche Smoke konnte nicht ausgewertet werden, weil lokal kein freigegebener CFRU/DPE Gen9-BPRE-Kandidat mit `moves.total=992` und hoechstem Move `991:PsychicNoise` gefunden wurde.
- Ein automatisch gefundener erster Kandidat war kein CFRU/DPE-Gen9-Stand und wurde verworfen; danach fand die stumme Kandidatensuche keinen passenden 992-Move-Kandidaten.
- `saveSuccessful`, `logSuccessful`, Reload-, Name-Length-, Terminator-/Padding-, Description-Pointer- und Name-Reload-Zaehler bleiben daher nicht fachlich ausgewertet.
- Keine Move Descriptions, keine Pointer-/Repointing- oder Text/Menu-Umsetzung, keine MoveData-Byte-Writer-Aenderung.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Build.
- `FVX-MOVE-005` wird nicht hochgestuft und bleibt `Write modelliert`; `FVX-MOVE-001/002/003/004/006` bleiben GUI-kompatibel.

Naechster sinnvoller Schritt:

- Den gleichen Name-only fixed-length Smoke erneut ausfuehren, sobald ein freigegebener lokaler CFRU/DPE Gen9-BPRE-ROM-Kandidat fuer den Smoke eindeutig verfuegbar ist. Scope unveraendert eng halten: keine Move Descriptions, kein Pointer-/Repointing, keine Text/Menu-Umsetzung.

## 2026-05-14 - CFRU/DPE Move Names / Descriptions Text/Menu-Scope Plan

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-move-names-text-menu-scope-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- Neuer read-only Planbericht `08_tests/randomizer/088_move_names_text_menu_scope_plan.md` erstellt.
- `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` und `FVX-MOVE-006` bleiben GUI-kompatibel.
- `FVX-MOVE-005` Randomize Move Names / Move Descriptions bleibt getrennt vom MoveData-Byte-Writer-Scope `+0..+11`.
- UPR-FVX-Codepfad: GUI/Settings aktivieren `randomizeMoveNames`, `GameRandomizer` ruft `MoveNameRandomizer.randomizeMoveNames()` auf, und `Gen3RomHandler.saveMoves()` schreibt `Move.name` ueber `writeFixedLengthString(...)` in die fixed-length Move-Namen-Tabelle.
- Fuer Gen3/CFRU/DPE ist der direkte Name-Writer kein Pointer-/Repointing-Pfad, sondern ein in-place fixed-length Textpfad mit `MoveNameLength` und sichtbarer `getMaxMoveNameLength() = 12`.
- Move Descriptions werden durch `FVX-MOVE-005` nicht als eigener Randomizer-Pfad geschrieben; sichtbare `MoveDescriptions`-Nutzung gehoert zu getrennten TM-/Item-Textpfaden.
- Planentscheidung: enger Name-only Reload-Smoke ist realistisch; Move Descriptions / Text/Menu-Repointing bleibt vorerst zurueckgestellt, bis ein eigener Description-/Pointer-Befund vorliegt.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Submodule-Pin-Aenderung, kein Randomizer-Lauf, kein Build und kein ROM-/Artefaktzugriff.

Naechster sinnvoller Schritt:

- Separater Smoke-Branch `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke`: nur `FVX-MOVE-005` Name-only pruefen, Move-Descriptions nicht schreiben, keine Pointer-/Repointing- oder Text/Menu-Umsetzung.

## 2026-05-14 - CFRU/DPE MoveData Fairy-Type-Byte Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

Aktueller Stand:

- UPR-FVX PR #34 ist gemerged.
- Workspace PR #129 ist gemerged.
- Diagnose 087 ist abgeschlossen und auf `main`.
- UPR-FVX-Fix `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3` erstellt.
- Der Fix bleibt auf `Gen3RomHandler` und das MoveData-Type-Byte `+2` begrenzt.
- Im sicheren CFRU/DPE-Gen9-BPRE-Gate liest `typeFromMoveData(...)` raw `0x17` als `Type.FAIRY`.
- Im selben Gate schreibt `moveDataTypeToByte(...)` `Type.FAIRY` als raw `0x17`.
- Vanilla-, Jambo- und andere Gen3-Pfade bleiben beim bestehenden Mapping.
- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/087_move_data_fairy_type_byte_fix_diagnostics.md` erstellt.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadMoveDataMismatches=0`, `moves.total=992`, hoechster Move `991:PsychicNoise`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`, `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`, `exceptionClass=none` und `stacktrace=none`.
- `typeByteMismatches=54` bleibt als Legacy-Mapping-Vergleich gegen `Gen3Constants.typeToByte(...)` sichtbar und ist in diesem Fix-Smoke kein CFRU/DPE-Reload-Fehler.
- `FVX-MOVE-004` Randomize Move Types ist damit GUI-kompatibel.
- `FVX-MOVE-005` Move Names/Descriptions bleibt ausserhalb dieses Scopes.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit.
- Keine TypeChart-/TypeEffectiveness-, Species-Type-, Stellar-/Typenmodell-, Name-, Description-, Palette-, Item-, Field-/Shop-/Pickup-, Trainer-, Wild-, Evolution-, Text/Menu-, Graphics-, TM/HM-, Tutor-, Egg- oder Learnset-Write-Aenderung.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`; private Pfade, ROM-Namen, Hashes, Logs und Output-ROMs wurden nicht dokumentiert.

Naechster sinnvoller Schritt:

- Separater Planungsbranch `analysis/upr-fvx-cfru-dpe-move-names-text-menu-scope-plan`: nur entscheiden und modellieren, ob `FVX-MOVE-005` Move Names / Move Descriptions als eigener Text/Menu-Scope machbar ist oder vorerst zurueckgestellt bleibt. Keine Umsetzung in diesem Sync-Block.

## 2026-05-14 - CFRU/DPE MoveData Types Reload-Smoke

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke`

UPR-FVX-Pin: `bb5ee11978e38839979e654ff1c14ba60a0cde93`

Aktueller Stand:

- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/086_move_data_types_reload_smoke.md` erstellt.
- Der Smoke blieb eng auf `FVX-MOVE-004` Randomize Move Types und das MoveData-Type-Byte `+2` begrenzt.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `moves.total=992`, hoechster Move `991:PsychicNoise`, `exceptionClass=none` und `stacktrace=none`.
- Der Smoke ist fachlich blockiert: `writeReloadMoveDataMismatches=54`, `typeReloadMismatches=54`, `expectedFairyMoves=54`, `fairyReloadMismatches=54` und `cfruDpeTypeByteMismatches=54`.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` blieben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
- Einordnung: Die aktuelle Gen3-MoveData-Type-Mappingfunktion schreibt `FAIRY` im MoveData-Pfad faktisch als Fallback `0x00`; fuer den getesteten CFRU/DPE Gen9-BPRE-Stand muss `FAIRY` im sicheren MoveData-Gate als raw `0x17` geschrieben werden.
- Dies ist kein TypeChart-/TypeEffectiveness-/Species-Type-Write-Befund.
- `FVX-MOVE-004` bleibt `Write modelliert`; `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003` und `FVX-MOVE-006` bleiben GUI-kompatibel.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`; private Pfade, ROM-Namen, Hashes, Logs und Output-ROMs wurden nicht dokumentiert.
- Keine Aenderung an `02_external/upr-fvx`; der Submodule-Pin bleibt `bb5ee11978e38839979e654ff1c14ba60a0cde93`.
- Keine TypeChart-/TypeEffectiveness-, Species-Type-, Name-, Description-, Palette-, Item-, Field-/Shop-/Pickup-, Trainer-, Wild-, Evolution-, Text/Menu-, Graphics-, TM/HM-, Tutor-, Egg- oder Learnset-Write-Aenderung.

Naechster sinnvoller Schritt:

- Enger UPR-FVX-Fixbranch `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`: im sicheren CFRU/DPE-Gen9-BPRE-MoveData-Writer-Gate `FAIRY` fuer Byte `+2 type` als raw `0x17` schreiben; Vanilla/Jambo/andere Gen3-Pfade sowie TypeChart/TypeEffectiveness/Species-Type-Write unveraendert lassen.

## 2026-05-14 - CFRU/DPE MoveData Power/Accuracy/PP Reload-Smoke

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke`

UPR-FVX-Pin: `bb5ee11978e38839979e654ff1c14ba60a0cde93`

Aktueller Stand:

- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/085_move_data_power_accuracy_pp_reload_smoke.md` erstellt.
- Der Smoke blieb eng auf MoveData Power / Accuracy / PP begrenzt.
- Aktiviert wurden nur `FVX-MOVE-001` Randomize Move Power, `FVX-MOVE-002` Randomize Move Accuracy und `FVX-MOVE-003` Randomize Move PP.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadMoveDataMismatches=0`, `moves.total=992`, hoechster Move `991:PsychicNoise`, `powerReloadMismatches=0`, `accuracyReloadMismatches=0`, `ppReloadMismatches=0`, `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`, `exceptionClass=none` und `stacktrace=none`.
- Rohbytes fuer `+1 power`, `+3 accuracy` und `+4 pp` reloadeten stabil: `powerByteMismatches=0`, `accuracyByteMismatches=0`, `ppByteMismatches=0`.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` blieben bytegleich.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`; private Pfade, ROM-Namen, Hashes, Logs und Output-ROMs wurden nicht dokumentiert.
- Keine Aenderung an `02_external/upr-fvx`; der Submodule-Pin bleibt `bb5ee11978e38839979e654ff1c14ba60a0cde93`.
- Keine Type-, Name-, Description-, Palette-, Item-, Field-/Shop-/Pickup-, TypeChart-/TypeEffectiveness-, Trainer-, Wild-, Evolution-, Text/Menu-, Graphics-, TM/HM-, Tutor-, Egg- oder Learnset-Write-Aenderung.

Naechster sinnvoller Schritt:

- Separater Folgebranch fuer `FVX-MOVE-004` Randomize Move Types. `FVX-MOVE-005` Move Names/Descriptions bleibt out of scope.

## 2026-05-14 - CFRU/DPE MoveData Write Preserve Reload-Smoke

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-data-write-preserve-reload-smoke`

UPR-FVX-Pin: `bb5ee11978e38839979e654ff1c14ba60a0cde93`

Aktueller Stand:

- Workspace PR #125 ist gemerged; Diagnose 084 ist abgeschlossen.
- UPR-FVX PR #33 und Workspace PR #124 sind gemerged; der Workspace bleibt auf `02_external/upr-fvx` Commit `bb5ee11978e38839979e654ff1c14ba60a0cde93` gepinnt.
- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/084_move_data_write_preserve_reload_smoke.md` erstellt.
- Der Smoke blieb eng auf MoveData / Update Moves und Preserve-Verhalten begrenzt.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadMoveDataMismatches=0`, `moves.total=992`, hoechster Move `991:PsychicNoise`, `categorySplitMismatches=0`, `categoryReloadMismatches=0`, `preserveByteMismatchesUnchangedMoves=0`, `exceptionClass=none` und `stacktrace=none`.
- Der Harness erzwang genau eine Category-Aenderung, weil `Update Moves` in diesem Stand keine Category-Aenderung erzeugte; damit wurde der CFRU/DPE-`BattleMove.split`-Write bei Byte `+10` konkret geprueft.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` blieben fuer unveraenderte Moves bytegleich.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`; private Pfade, ROM-Namen, Hashes, Logs und Output-ROMs wurden nicht dokumentiert.
- Keine Aenderung an `02_external/upr-fvx`; der Submodule-Pin bleibt `bb5ee11978e38839979e654ff1c14ba60a0cde93`.
- Keine Palette-, Item-, Field-/Shop-/Pickup-, TypeChart-/TypeEffectiveness-, Trainer-, Wild-, Evolution-, Text/Menu-, Graphics-, TM/HM-, Tutor-, Egg- oder Learnset-Write-Aenderung.

Naechster sinnvoller Schritt:

- Separater Folgebranch `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke` fuer GUI-nahe Reload-Smokes von `FVX-MOVE-001` Randomize Move Power, `FVX-MOVE-002` Randomize Move Accuracy und `FVX-MOVE-003` Randomize Move PP. `FVX-MOVE-004` Randomize Move Types danach separat halten; `FVX-MOVE-005` Move Names/Descriptions bleibt out of scope.

## 2026-05-14 - CFRU/DPE MoveData Write Preserve Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-move-data-write-preserve`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-move-data-write-preserve`

Aktueller Stand:

- UPR-FVX PR #33 und Workspace PR #124 sind gemerged.
- UPR-FVX-Fix `bb5ee11978e38839979e654ff1c14ba60a0cde93` erstellt.
- Der Fix bleibt auf `Gen3RomHandler.saveMoves()` begrenzt.
- Klassische MoveData-Felder werden weiter geschrieben: `+0 effect`, `+1 power`, `+2 type`, `+3 accuracy`, `+4 pp`.
- Im bestehenden CFRU/DPE-Gen9-BPRE-Gate wird zusaetzlich `BattleMove.split` bei Byte `+10` geschrieben: `PHYSICAL -> 0`, `SPECIAL -> 1`, `STATUS -> 2`.
- Nicht modellierte Bytes `+5 secondaryEffectChance`, `+6 target`, `+7 priority`, `+8 flags`, `+9 z_move_power` und `+11 z_move_effect` bleiben bytegleich erhalten.
- `./gradlew clean :random:jar` war erfolgreich.
- `./gradlew test` endete mit `BUILD SUCCESSFUL`, meldete aber bestehende Failures ausserhalb des MoveData-Scopes in `PlayerCharacterGraphicsTest` und `Gen1CmpTest`.
- Der lokale Randomizer-/ROM-Reload-Smoke wurde separat in Diagnose 084 ausgefuehrt und bestaetigt.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit und dokumentiert Diagnose 083.
- Keine Palette-, Item-, Field-/Shop-/Pickup-, TypeChart-/TypeEffectiveness-, Trainer-, Wild-, Evolution-, Text/Menu-, Graphics-, TM/HM-, Tutor-, Egg- oder Learnset-Write-Aenderung.

Naechster sinnvoller Schritt:

- Fix- und Reload-Smoke-PRs sind gemerged. Naechster MoveData-Schritt ist ein separater Power/Accuracy/PP-Reload-Smoke; Move Types und Move Names bleiben getrennt.

## 2026-05-14 - CFRU/DPE Evolution Similar Strength Normalized Reload Diagnostics

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-evolution-similar-strength-normalized-reload`

Aktueller Stand:

- Neuer sanitiserter Ergebnisbericht `08_tests/randomizer/082_evolution_similar_strength_normalized_reload_diagnostics.md` erstellt.
- Es wurde nur `FVX-TRAIT-018` Evolutions Similar Strength im Carrier `FVX-TRAIT-016` Evolution-Species-Writer lokal ausgefuehrt.
- Der Reload-Vergleich wurde auf persistierte Gen3-Evolution-Felder normalisiert: Evolution-Type, ExtraInfo mit Item-ID-Normalisierung und Ziel-Species per interner `SpeciesSet`-Identitaet.
- `Evolution.forme` wurde nicht als Mismatch-Kriterium gewertet.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `normalizedWriteReloadEvolutionMismatches=0`, `rawWithFormeWriteReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- `Bad Egg=true` bleibt nach 055 als bestehender Evolution-Log-/Sonder-Species-Marker klassifiziert, weil der normalisierte Reload stabil ist und der Mismatch-Zaehler `0` bleibt.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.
- `FVX-TRAIT-019`, Wild, Trainer, TypeChart, MoveData, Palette, Items, Text/Menu, Graphics und Evolution-Methoden-Writer blieben ausgeschlossen.

Naechster sinnvoller Schritt:

- PR fuer Diagnose 082 reviewen und mergen. Danach Evolution-Methoden-Writer und weitere Evolution-Suboptionen getrennt planen; fuer `FVX-TRAIT-018` ist in diesem engen Similar-Strength-Scope kein Fixbranch erforderlich.

## 2026-05-14 - CFRU/DPE Evolution Similar Strength Mismatch Diagnostics

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-evolution-similar-strength-mismatch-diagnostics`

Aktueller Stand:

- Neues read-only Code-/Protokollanalyse-Protokoll `08_tests/randomizer/081_p1_evolution_similar_strength_mismatch_diagnostics.md` erstellt.
- 081 untersucht den verbliebenen 070-Blocker `FVX-TRAIT-018` Evolutions Similar Strength im Carrier `FVX-TRAIT-016` Evolution-Species-Writer.
- Relevante Codepfade sind `EvolutionRandomizer.randomizeEvolutionsInner()`, `findPossibleReplacements(...)`, `prepareNewEvolution(...)`, `SpeciesSet.getRandomSimilarStrengthSpecies(...)`, `Gen3RomHandler.loadEvolutions()`, `writeEvolutions()` und `Evolution.toString()/equals(...)`.
- Wahrscheinlichste Einordnung: `writeReloadEvolutionMismatches=24` aus 070 ist eher ein zu breiter Diagnosevergleich auf nicht persistierte Forme-/Zusatzfelder als ein harter Evolution-Species-Write-Fehler.
- `prepareNewEvolution(...)` setzt `Evolution.forme`, aber der Gen3-Evolution-Write-/Reload-Pfad persistiert dieses Feld nicht; 026 definiert den Reload-Erfolg ueber persistierte Evolution-Felder und Ziel-Species per interner `SpeciesSet`-Identitaet.
- `Bad Egg=true` korreliert nicht zwingend mit den 070-Mismatches: 026 und 080 zeigen `Bad Egg` im Evolution-Scope bei `0` Reload-Mismatches.
- Der Same-Typing-Fix aus 080 bleibt getrennt; `FVX-TRAIT-018` nutzt den BST-/Similar-Strength-Pfad und nicht den Same-Typing-`hasSharedType(...)`-Guard.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater, eng freigegebener Diagnose-Smoke fuer `FVX-TRAIT-018` mit normalisiertem Reload-Vergleich auf persistierte Gen3-Evolution-Felder und interne Ziel-Species-Identitaet. `Evolution.forme` nicht als Mismatch-Kriterium werten; `Bad Egg` nach 055 separat klassifizieren.

## 2026-05-14 - CFRU/DPE Evolution Same Typing Null-Type Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`

Aktueller Stand:

- UPR-FVX-Fix `74d88a7ab1d306e1e09ccabb851dffd7f6922b66` erstellt.
- Der Fix bleibt auf `EvolutionRandomizer` begrenzt und behandelt Species mit `primaryType == null` defensiv im Evolutions-Same-Typing-Filter.
- `FVX-TRAIT-019` Evolutions Same Typing wurde lokal sanitisiert ausgefuehrt: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- `Bad Egg=true` bleibt nach 055 als bestehender Evolution-Log-/Sonder-Species-Marker klassifiziert, weil Save/Log/Output/Reload stabil sind und der Reload-Mismatch-Zaehler `0` ist.
- `FVX-TRAIT-018` Evolutions Similar Strength wurde nur getrennt als Regression ausgefuehrt und bleibt nicht mit dem Same-Typing-Fix vermischt.
- Neues Diagnoseprotokoll `08_tests/randomizer/080_evolution_same_typing_nulltype_fix_diagnostics.md` erstellt.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit und aktualisiert README, Session, Next Steps, Roadmap, Feature-Coverage und Tool-Manifest.
- Keine Wild-, Trainer-, TypeChart-, MoveData-, Palette-, Item-, Text/Menu-, Graphics- oder Evolution-Methoden-Writer-Aenderung.

Naechster sinnvoller Schritt:

- UPR-FVX-PR und Workspace-PR reviewen und mergen. Danach verbleibende Evolution-Suboptionen weiter getrennt behandeln, insbesondere Evolution-Methoden-Writer und weitere Poolfilter.

## 2026-05-14 - CFRU/DPE Evolution Same Typing Code Diagnosis

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-evolution-same-typing-blocker-diagnostics`

Aktueller Stand:

- Neues read-only Codeanalyse-Protokoll `08_tests/randomizer/079_p1_evolution_same_typing_code_diagnosis.md` erstellt.
- 079 untersucht konkret den 070-Blocker `FVX-TRAIT-019` Evolutions Same Typing im Carrier `FVX-TRAIT-016` Evolution-Species-Writer.
- Relevante Codepfade sind `GameRandomizer.maybeRandomizeEvolutions()`, `EvolutionRandomizer.randomizeEvolutions()`, `findPossibleReplacements(...)`, `SpeciesSet.filter(...)`, `Species.hasSharedType(...)` und der Gen3 Base-Stats-Type-Read-Scope.
- Wahrscheinlich konkrete Ursache: Der Same-Typing-Filter ruft `to.hasSharedType(...)` auf. Wenn ein Kandidat aus dem Evolution-Replacement-Pool `primaryType == null` hat, dereferenziert `Species.hasSharedType(...)` diesen Null-Type und wirft eine `NullPointerException`.
- Der allgemeine Evolution-Species-Carrier bleibt abgegrenzt: `FVX-TRAIT-016` ist belegt, aber Same Typing nutzt einen zusaetzlichen Species-Type-Filter vor der Zielauswahl.
- `FVX-TRAIT-018` Evolutions Similar Strength bleibt getrennt, weil es nicht denselben `hasSharedType(...)`-Pfad nutzt und in 070 stattdessen Save/Reload mit `writeReloadEvolutionMismatches=24` und `Bad Egg=true` erreichte.
- Ein lokaler Diagnose-Lauf ist fuer die Fixplanung nicht zwingend noetig; ein spaeterer Fix-Smoke fuer `FVX-TRAIT-019` bleibt erforderlich.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Eng gegateten UPR-FVX-Fixbranch fuer `EvolutionRandomizer` Same-Typing-/Null-Primary-Type-Scope vorbereiten. `FVX-TRAIT-018` separat halten und nicht durch denselben Fix als supported hochstufen.

## 2026-05-14 - CFRU/DPE Trainer Type Diversity Null-Type Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`

Aktueller Stand:

- UPR-FVX-Fix `d89fc64e3b0223b03a65466422847dc7df30d03c` erstellt.
- Der Fix bleibt auf `TrainerPokemonRandomizer` begrenzt und behandelt Species mit `primaryType == null` defensiv im Force-Diverse-Types-/`usedTypes`-Pfad.
- Null-Primary-Type-Species werden im erweiterten BPRE-Hack nicht mehr als valide Type-Diversity-/Type-Themes-Replacements genutzt; `EnumSet<Type>` erhaelt keine `null`-Eintraege.
- Bestehende BST-zero-, all-zero-Ability- und Placeholder-/Special-Species-Grenzen bleiben unveraendert.
- `FVX-FOE-009` Trainer Type Diversity / Type Themes wurde lokal sanitisiert ausgefuehrt: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTrainerPokemonMismatches=0`, `filterViolations=0`, `Bad Egg=false`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- Trainer Similar Strength unter `FVX-FOE-001` wurde als Regression lokal sanitisiert ausgefuehrt und bleibt mit Save/Log/Output/Reload true sowie `writeReloadTrainerPokemonMismatches=0` stabil.
- Neues Diagnoseprotokoll `08_tests/randomizer/078_trainer_type_diversity_nulltype_fix_diagnostics.md` erstellt.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit und aktualisiert README, Session, Next Steps, Roadmap, Feature-Coverage und Tool-Manifest.
- Keine Wild-, Evolution-, TypeChart-, MoveData-, Palette-, Item-, Text/Menu-, Graphics-, Trainer-Level-, Additional-Pokemon-, Better-Movesets-, Battle-Style- oder Trainer-Names/Class-Names-Aenderung.

Naechster sinnvoller Schritt:

- UPR-FVX-PR und Workspace-PR reviewen und mergen. Danach die verbleibenden 070-Evolution-Blocker `FVX-TRAIT-018` und `FVX-TRAIT-019` getrennt fortsetzen.

## 2026-05-14 - CFRU/DPE Trainer Type Diversity Code Diagnosis

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-trainer-type-diversity-code-diagnosis`

Aktueller Stand:

- Neues read-only Codeanalyse-Protokoll `08_tests/randomizer/077_p1_trainer_type_diversity_code_diagnosis.md` erstellt.
- 077 untersucht konkret den 070/076-Blocker `FVX-FOE-009` Trainer Type Diversity / Type Themes im Carrier `FVX-FOE-001` Trainer Pokemon.
- Relevante Codepfade sind `GameRandomizer.maybeRandomizeTrainerPokemon()`, `TrainerPokemonRandomizer.randomizeTrainerPokes()`, `pickTrainerPokeReplacement(...)` und `updateUsedTypes(...)`.
- Wahrscheinlich konkrete Ursache: Der Force-Diverse-Types-Pfad schreibt `sp.getPrimaryType(false)` in ein `EnumSet<Type>`. Wenn eine Replacement-Species `primaryType == null` hat, wirft `EnumSet.add(null)` eine `NullPointerException`.
- Der Trainer-Species-Pool filtert im erweiterten BPRE-Hack bereits `BST == 0` und all-zero Ability Species, aber keinen Null-Primary-Type-/unsupported-Type-Scope.
- Trainer Similar Strength ist abgegrenzt: Der stabile 070-Slice nutzt `getRandomSimilarStrengthSpecies(...)`, aktiviert aber nicht den Force-Diverse-Types-/`usedTypes`-Pfad.
- Ein lokaler Diagnose-Lauf ist fuer die Fixplanung nicht zwingend noetig; optional waere er nur fuer sanitisierten Stacktrace-/Null-Primary-Type-Zaehler-Beleg.
- Empfohlen ist ein eng gegateter UPR-FVX-Fixbranch fuer Trainer-Type-Diversity-Null-Type-Scope in `TrainerPokemonRandomizer`, ohne Wild, Evolution, TypeChart, MoveData, Palette, Items, Text/Menu, Graphics oder Level-Modifier.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Fixbranch fuer defensiven Trainer-Type-Diversity-Null-Type-Scope vorbereiten. Danach nur `FVX-FOE-009` und optional Trainer Similar Strength als Regression lokal sanitisiert pruefen.

## 2026-05-14 - CFRU/DPE Trainer Type Diversity Blocker Diagnostics Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-trainer-type-diversity-blocker-diagnostics`

Aktueller Stand:

- Neues read-only Diagnoseplan-Protokoll `08_tests/randomizer/076_p1_trainer_type_diversity_blocker_diagnostics_plan.md` erstellt.
- 076 fokussiert nur den verbliebenen 070-Blocker `FVX-FOE-009` Trainer Type Diversity / Type Themes im Carrier `FVX-FOE-001` Trainer Pokemon.
- Der Befund aus 070 bleibt als echter Save-Blocker klassifiziert: `saveSuccessful=false`, kein Output/Reload, `NullPointerException` und `filterViolations=112` nur bis Abbruch.
- Trainer Similar Strength unter `FVX-FOE-001` bleibt bewusst getrennt, weil dieser Slice in 070 mit Save/Log/Output/Reload true und `writeReloadTrainerPokemonMismatches=0` stabil war.
- Pruefspuren sind Trainer-Type-Diversity-Auswahl gegen Null-Type-, Placeholder-, BST-zero- oder unsupported-Type-Species, Trainer-Pool-Scope, Team-Type-Constraints und fehlende Skip-/Scope-Regeln im Type-Diversity-/Type-Themes-Pfad.
- Spaetere Diagnosemetriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater read-only Code-/Protokollanalysebranch fuer `FVX-FOE-009`, der Trainer-Randomizer- und Type-Diversity-Codepfade identifiziert und den Unterschied zum stabilen Trainer Similar Strength Slice klaert. Kein Fixbranch ohne klare Ursache.

## 2026-05-14 - CFRU/DPE Wild Filter Carrier Nullslot Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`

Aktueller Stand:

- UPR-FVX-Fix `acaada514d04b1d306581ce872d2d77fe1b4c5b3` erstellt.
- Der Fix bleibt auf `WildEncounterRandomizer` begrenzt und behandelt `Encounter`-Slots mit `species == null` defensiv vor der Mapping-/InfoMap-Auswahl.
- Null/unaufloesbare Wild-Encounter-Slots werden nicht als `zoneMap`-/InfoMap-Anker genutzt; sie erhalten ein Replacement aus bestehenden `remaining`-/`allowed`-Pools, mit vorhandener Theme-Grenze und Area-Bans.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary wurden einzeln lokal sanitisiert ausgefuehrt.
- Beide Slices melden `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadWildPokemonMismatches=0`, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`.
- `FVX-WILD-004` meldet `filterViolations=0`; fuer `FVX-WILD-011` wurde kein eigener Filterverletzungszaehler behauptet.
- Die lokalen Fix-Smokes beobachteten `nullSlotsBefore=0` und `nullSlotsAfter=0`; der Fix bleibt trotzdem auf den in 074 identifizierten defensiven Null-/unaufloesbar-Scope begrenzt.
- Neues Diagnoseprotokoll `08_tests/randomizer/075_wild_filter_carrier_nullslot_fix_diagnostics.md` erstellt.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit und aktualisiert README, Session, Next Steps, Roadmap, Feature-Coverage und Tool-Manifest.
- Keine TypeChart-, MoveData-, Palette-, Item-, Encounter-Held-Item-, custom-Day/Night-Wild-, Catch-Em-All-, Minimum-Catch-Rate-, Level-Modifier-, Text/Menu- oder Graphics-Aenderung.

Naechster sinnvoller Schritt:

- UPR-FVX-PR und Workspace-PR reviewen und mergen. Danach die restlichen 070-Blocker getrennt fortsetzen: `FVX-FOE-009` Trainer Type Diversity sowie `FVX-TRAIT-018/019` Evolution-Slices.

## 2026-05-14 - CFRU/DPE Wild Filter Carrier Code Diagnosis

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-code-diagnosis`

Aktueller Stand:

- Neues read-only Codeanalyse-Protokoll `08_tests/randomizer/074_p1_wild_filter_carrier_code_diagnosis.md` erstellt.
- 074 untersucht konkret die 070-Wild-Blocker `FVX-WILD-011` und `FVX-WILD-004` im gemeinsamen `FVX-WILD-001` Standard/Fallback-Wild-Carrier.
- Beide Slices nutzen `wildPokemonZoneMod=GAME` und laufen daher durch `WildEncounterRandomizer.InnerRandomizer.game1to1Encounters()` mit `useMapping=true`.
- Wahrscheinlich konkrete Ursache: `setupAreaInfoMap()` baut seine Infos aus `EncounterArea.getSpeciesInArea()`, dieses nutzt `SpeciesSet`, und `SpeciesSet.add(...)` ignoriert `null`; ein nicht aufloesbarer/null Encounter-Slot bleibt aber in `randomizeArea()` erhalten und trifft danach `setupAllowedForReplacementUsingInfoMap()`, das `IllegalStateException("Info was null for encounter's species!")` wirft.
- Damit treffen `FVX-WILD-011` und `FVX-WILD-004` wahrscheinlich denselben InfoMap-/Nullslot-Pfad, bevor Similar-Strength-BST- oder Keep-Primary-Type-Filter fachlich greifen.
- Ein lokaler Diagnose-Lauf ist fuer die Fixplanung nicht zwingend noetig; optional waere er nur fuer sanitisierten Area-/Slot- oder Exception-Message-Beleg.
- Empfohlen ist ein eng gegateter Fixbranch fuer Wild-Mapping-/Nullslot-Scope, ohne TypeChart, MoveData, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level Modifier, Text/Menu oder Graphics.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- PR fuer 074 reviewen und mergen; danach Fixbranch fuer defensiven Wild-Filter-Carrier-/Nullslot-Scope vorbereiten oder optional einen separat freigegebenen lokalen Diagnosebranch fuer sanitisierten Exception-/Area-Beleg starten.

## 2026-05-14 - CFRU/DPE Wild Filter Carrier Diagnostics Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-diagnostics`

Aktueller Stand:

- Neues read-only Diagnose-/Harness-Planprotokoll `08_tests/randomizer/073_p1_wild_filter_carrier_diagnostics_plan.md` erstellt.
- 073 fokussiert nur `FVX-WILD-011` Wild Similar Strength, `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary und den gemeinsamen `FVX-WILD-001` Standard/Fallback-Wild-Carrier.
- Ausgangsbefunde aus 070 bleiben: beide Wild-Slices sind echte Save-Blocker mit `saveSuccessful=false`, keinem Output/Reload und `IllegalStateException`; `FVX-WILD-004` hatte `filterViolations=0` nur bis Abbruch.
- 073 plant zuerst read-only Code-/Protokollanalyse, um Carrier-Scope von Similar-Strength- und Type-Restriction-Filter-Scope zu trennen.
- Falls vorhandene Dokumente und Codepfade nicht ausreichen, soll eine spaetere lokale Diagnose nur als separater Freigabeschritt erfolgen.
- Hypothesen zu Wild-Nullslot-/Placeholder-Eintraegen, Area-/Encounter-Slot-Scope, leeren oder ungueltigen BST-/Species-Pools, Species-Type-Filtern und strengeren Suboption-Grenzen sind dokumentiert.
- Spaetere Metriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- PR fuer 073 reviewen und mergen; danach read-only Code-/Protokollanalyse fuer den Wild-Filter-Carrier oder, falls nicht ausreichend, ein separat freigegebener lokaler Diagnosebranch.

## 2026-05-14 - CFRU/DPE Wild 070 Blockers Diagnostics Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-070-blockers-diagnostics`

Aktueller Stand:

- Neues read-only Diagnoseplan-Protokoll `08_tests/randomizer/072_p1_wild_070_blockers_diagnostics_plan.md` erstellt.
- 072 plant die gemeinsame Folge-Diagnose fuer `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary.
- Beide Slices bleiben echte Save-Blocker im `FVX-WILD-001` Standard/Fallback-Wild-Carrier: kein Output/Reload und `IllegalStateException`.
- `FVX-WILD-011` wird als BST-/Species-Pool-Filter-Scope plus Wild-Nullslot-/Placeholder-Scope eingeordnet.
- `FVX-WILD-004` wird als Species-Type-Filter-Scope plus Wild-Nullslot-/Placeholder-Scope eingeordnet; `filterViolations=0` aus 070 bleibt nur ein Vor-Abbruch-Befund.
- Gemeinsame Hypothesen sind dokumentiert: Nullslot-/Placeholder-Wild-Entries, Area-/Encounter-Slot-Scope, leere/ungueltige Pools, Placeholder-/Special-/unsupported-Type-Species und strengere Suboption-Vorauswahl trotz P1-supported `FVX-WILD-001` Carrier.
- Spaetere Diagnosemetriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- TypeChart/TypeEffectiveness, MoveData Write, Palette, Items/Field/Shops/Pickup, Encounter Held Items, custom Day/Night-Wild, Catch Em All / Minimum Catch Rate, Level Modifier und Text/Menu/Graphics bleiben ausgeschlossen.
- Keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater read-only Diagnose-/Harness-Plan oder freigegebene read-only Diagnose fuer den Wild-Filter-Carrier; kein Fixbranch ohne klare Ursache.

## 2026-05-14 - CFRU/DPE 070 Blocked Slices Follow-up Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-070-blocked-slices-followup-plan`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/071_p1_070_blocked_slices_followup_plan.md` erstellt.
- 071 plant die Folgeanalyse fuer die in 070 blockierten Similar Strength / Same Type / Type Themes Slices, ohne Codeaenderung, Fix oder Randomizer-Laeufe.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary werden gemeinsam als Wild-Carrier-/Placeholder-Scope modelliert, weil beide `FVX-WILD-001` Carrier und `IllegalStateException` teilen.
- `FVX-FOE-009` Trainer Type Diversity / Type Themes bleibt ein eigener Trainer-Type-Diversity-/Null-Type-Scope.
- `FVX-TRAIT-018` Evolutions Similar Strength bleibt ein eigener Evolution-Reload-/Bad-Egg-Scope; `Bad Egg` kann dort nicht als reine 055-Log-Hygiene freigegeben werden, solange `writeReloadEvolutionMismatches` ungleich `0` ist.
- `FVX-TRAIT-019` Evolutions Same Typing bleibt ein eigener Evolution-Same-Typing-/Null-Scope.
- Spaetere Diagnosemetriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- TypeChart/TypeEffectiveness, MoveData Write, Palette, Items/Field/Shops/Pickup, Graphics/Sprites, Text/Menu, Level Modifier und Evolution-Methoden-Writer bleiben ausgeschlossen.
- Keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater read-only Diagnoseplan oder Diagnosebranch fuer Wild Similar Strength + Wild Type Restrictions, ohne offene Writer und ohne Fixarbeit.

## 2026-05-14 - CFRU/DPE Similar Strength / Same Type Regression-Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/070_p1_similar_strength_same_type_regression_smoke_results.md` erstellt.
- Die in 069 geplanten Similar-Strength-/Same-Type-/Type-Theme-/Type-Restriction-Slices wurden einzeln lokal ausgefuehrt und sanitisiert dokumentiert.
- Trainer Similar Strength unter `FVX-FOE-001` ist im Trainer-Species-Carrier-Smoke stabil: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTrainerPokemonMismatches=0`, `Bad Egg=false`, `<unknown>=false`, `stacktrace=none`.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary blockieren beim Save mit `IllegalStateException`; kein Output/Reload.
- `FVX-FOE-009` Trainer Type Diversity / Type Themes blockiert beim Save mit `NullPointerException`; kein Output/Reload.
- `FVX-TRAIT-018` Evolutions Similar Strength speichert und reloadet, meldet aber `writeReloadEvolutionMismatches=24` und `Bad Egg=true`; der Marker wird wegen der Mismatches nicht als unkritischer 055-Marker freigegeben.
- `FVX-TRAIT-019` Evolutions Same Typing blockiert beim Save mit `NullPointerException`; kein Output/Reload.
- TypeChart/TypeEffectiveness, MoveData Write, Field Items/Shops/Pickup, Encounter Held Items, Palette/Graphics, Text/Menu, Level-Modifier, Evolution-Methoden-Writer, Starter Held Items, Race Mode / Intro Mon, Better Movesets, Trainer Additional Pokemon, Battle Style, Trainer Names/Class Names, Catch Em All, Minimum Catch Rate, Wild held items und custom Day/Night-Wild blieben ausgeschlossen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.
- Lokale ROM-, Log-, Output-ROM-, Build- und Diagnoseartefakte blieben ignored und werden nicht committed oder dokumentiert.

Naechster sinnvoller Schritt:

- Read-only Diagnoseplan fuer die blockierten 070-Slices: Wild Similar Strength/Type Restrictions gegen Wild-Nullslot-/Placeholder-Scope, `FVX-FOE-009` gegen Trainer-Type-Diversity-/Null-Type-Scope und `FVX-TRAIT-018/019` gegen Evolution-Reload-Mismatches, `Bad Egg` und Null-Evolution-Scope.

## 2026-05-14 - CFRU/DPE Similar Strength / Same Type Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/069_p1_similar_strength_same_type_regression_smoke.md` erstellt.
- 069 plant spaetere Regression-Smokes fuer BST-/Type-basierte Poolfilter: Similar Strength, Same Type / Same Typing, Type Themes und Type Restrictions.
- Geplante Slices: `FVX-WILD-011` Wild Similar Strength, `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary, Trainer Similar Strength konservativ als Suboption unter `FVX-FOE-001`, `FVX-FOE-009` Trainer Type Diversity / Type Themes, `FVX-TRAIT-018` Evolutions Similar Strength und `FVX-TRAIT-019` Evolutions Same Typing.
- Geeignete Carrier sind `FVX-WILD-001` Standard/Fallback Wild, `FVX-FOE-001` Trainer Pokemon und `FVX-TRAIT-016` Evolution Randomization.
- 069 nutzt Species-Pools, BaseStats/BST und Species-Type-Felder aus belegten Datenpfaden; Same Type / Type Themes beweisen keinen TypeChart- oder TypeEffectiveness-Support.
- Starter-Type/BST aus 065 und `FVX-SST-012` Static Similar Strength bleiben nur Referenz-/Vergleichsbelege, nicht primaerer Scope.
- TypeChart/TypeEffectiveness, MoveData Write, Field Items/Shops/Pickup, Encounter Held Items, Palette/Graphics, Text/Menu, Level-Modifier, Evolution-Methoden-Writer, Starter Held Items, Race Mode / Intro Mon, Better Movesets, Trainer Additional Pokemon, Battle Style, Trainer Names/Class Names, Catch Em All, Minimum Catch Rate, Wild held items und custom Day/Night-Wild bleiben ausgeschlossen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`: die in 069 geplanten Wild-, Trainer- und Evolution-Slices einzeln lokal ausfuehren und sanitisiert dokumentieren, weiter ohne offene Writer.

## 2026-05-14 - CFRU/DPE TypeEffectiveness Follow-up Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/068_type_effectiveness_followup_smoke_results.md` erstellt.
- Die in 067 geplanten TypeEffectiveness-Folgesmokes wurden einzeln lokal ausgefuehrt und sanitisiert dokumentiert: `FVX-TYPE-001` Balanced, Keep Type Identities und Inverse, `FVX-TYPE-002` Add Random Immunities sowie `FVX-TYPE-003` Update Type Effectiveness.
- Alle fuenf Slices melden `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTypeChartMismatches=0` und `stacktrace=none`.
- Foresight- und Endtable-Terminatoren blieben in allen Slices erhalten.
- Unsupported/Stellar wurde in keinem Slice eingefuehrt oder still normalisiert.
- `Bad Egg=false` und `<unknown>=false` in allen Slice-Logs.
- Balanced erzeugte Fairy-Rohtriplets und reloadete sie als raw `0x17`; Keep Type Identities, Inverse, Add Random Immunities und Update Type Effectiveness erzeugten keine Fairy-Rohtriplets und kein Fehlmapping.
- `FVX-TYPE-002` Add Random Immunities wurde getrennt als eigener Risikopunkt getestet.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.
- Lokale ROM-, Log-, Output-ROM-, Build- und Diagnoseartefakte blieben ignored und werden nicht committed.

Naechster sinnvoller Schritt:

- PR fuer `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes` reviewen und mergen; danach zu `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke` zurueckkehren oder einen offenen Writer separat freigeben.

## 2026-05-14 - CFRU/DPE TypeEffectiveness Follow-up Smoke Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/067_type_effectiveness_followup_smoke_plan.md` erstellt.
- Der gemergte TypeChart-Fix aus Diagnose 066 bleibt Referenz: TypeEffectiveness-only Random war Save/Log/Output/Reload-stabil, `writeReloadTypeChartMismatches=0`, Fairy reloadete als raw `0x17`, unsupported/Stellar wurde nicht eingefuehrt oder still normalisiert und Terminatoren blieben erhalten.
- 067 stellt klar, dass der Random-Smoke aus 066 die Einzelpruefung weiterer TypeEffectiveness-GUI-Modi nicht ersetzt.
- Geplante spaetere Slices: `FVX-TYPE-001` Balanced, `FVX-TYPE-001` Keep Type Identities, `FVX-TYPE-001` Inverse, `FVX-TYPE-002` Add Random Immunities und `FVX-TYPE-003` Update Type Effectiveness.
- `FVX-TYPE-002` Add Random Immunities bleibt als eigener Risikopunkt getrennt geplant.
- Gemeinsame spaetere Erfolgskriterien dokumentiert: Save/Log/Output/Reload true, `writeReloadTypeChartMismatches=0`, Fairy raw `0x17`, unsupported/Stellar nicht eingefuehrt oder normalisiert, Foresight-/Endtable-Terminatoren erhalten, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`.
- MoveData, Palette-Randomization, Items/Field Items/Shops/Pickup, Graphics/Sprites, Text/Menu und Species-Type-Write bleiben ausgeschlossen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Spaeterer Test-/Diagnosebranch fuer die geplanten TypeEffectiveness-Folgesmokes, der die Slices einzeln ausfuehrt und sanitisiert dokumentiert, oder Rueckkehr zu `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`.

## 2026-05-14 - CFRU/DPE TypeChart Preserve Effectiveness Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`

Aktueller Stand:

- UPR-FVX-Fix `36707e0190d3d9fa587550dfc5631fcaa9abd6b1` erstellt.
- Der Fix trennt TypeChart-raw-Type-Mapping von `gBaseStats`-Type-Mapping: Fairy `0x17` wird im CFRU/DPE-TypeChart gelesen und geschrieben, waehrend Stellar/raw `0x18` unsupported bleibt.
- Unsupported raw TypeChart-Triplets werden preserve-/skip-only behandelt und nicht still auf Normal, Fairy oder null normalisiert.
- Foresight-Block und Endtable-Terminator bleiben erhalten; die CFRU/DPE-Kapazitaetspruefung nutzt den vorhandenen TypeChart-Bereich.
- Neues Diagnoseprotokoll `08_tests/randomizer/066_type_chart_preserve_effectiveness_fix_diagnostics.md` erstellt.
- TypeEffectiveness-only Smoke: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTypeChartMismatches=0`, `fairyNonNeutralReload=13`, `rawFairyEntriesReload=13`, `unsupportedRawEntriesPreserved=true`, Terminatoren erhalten und `stacktrace=none`.
- `Bad Egg=false` und `<unknown>=false` im TypeEffectiveness-only Log.
- Keine Species-Type-Write-Aenderung aus 051, kein STELLAR-Enum, keine MoveData-, Palette-, Item-, Graphics- oder Text/Menu-Aenderung.
- Workspace dokumentiert den neuen UPR-FVX-Submodule-Pin; lokale Diagnoseartefakte bleiben ignored und werden nicht committed.

Naechster sinnvoller Schritt:

- PRs fuer UPR-FVX-Fix und Workspace-Submodule-/Diagnoseupdate pruefen; danach optional einzelne TypeEffectiveness-Folgesmokes fuer Balanced, Keep Identities, Inverse/Add Immunities und Update Type Effectiveness planen.

## 2026-05-14 - CFRU/DPE Starters Suboptions Regression-Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/065_p1_starters_suboptions_regression_smoke_results.md` erstellt.
- Die lokal ausgefuehrten 063-Slices wurden sanitisiert dokumentiert: Baseline `FVX-SST-002`, `FVX-SST-003` basic with 2 evolutions, `FVX-SST-004` any basic, `FVX-SST-005` type restrictions, `FVX-SST-006` no legendaries und `FVX-SST-009` BST min/max.
- Alle sechs Slices melden Save/Log/Reload true, `Starter-Mismatches=0`, `Filterverletzungen=0` und `stacktrace=none`.
- `Bad Egg=false` und `<unknown>=false` in allen Slice-Logs.
- Starter Held Items `FVX-SST-007`/`FVX-SST-008`, MoveData Write, Field Items/Shops/Pickup, Palette-Randomization, TypeChart und Text/Menu/Graphics blieben aus.
- `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` wurden konservativ als getestet im Starter-Species-Writer-Smoke dokumentiert, nicht als globale Vollabdeckung fuer Wild-/Trainer-/Evolution-Kombinationen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe im Dokumentationsblock, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`: BST-/Type-basierte Pooling-Suboptionen pruefen, ohne TypeChart oder MoveData-Write zu aktivieren.

## 2026-05-14 - CFRU/DPE Global Species Pool Regression-Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/064_p1_global_species_pool_regression_smoke_results.md` erstellt.
- Die lokal ausgefuehrten 062-Slices wurden sanitisiert dokumentiert: Baseline Carrier, `FVX-GEN-001` Generation Limits, `FVX-GEN-001` related Pokemon und `FVX-GEN-002` No Premature Evolutions.
- Alle vier Slices melden Save/Log/Reload true, `Starter-Mismatches=0` und `stacktrace=none`.
- `Bad Egg` und `<unknown>` traten in den Slice-Logs nicht auf.
- Aktiv war nur `FVX-SST-002` als Starter-Species-Carrier plus jeweiliger Poolfilter.
- Held Items, MoveData-Write, Palette-Randomization, TypeChart, Evolution-Methoden-Fixes und Intro/Race Mode blieben aus.
- `FVX-GEN-001` und `FVX-GEN-002` wurden konservativ als getestet im Starter-Carrier-Smoke dokumentiert, nicht als globale Vollabdeckung fuer Wild-/Trainer-/Evolution-Kombinationen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe im Dokumentationsblock, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`: die in 063 geplanten Starter-Suboptions-Slices lokal ausfuehren, weiter ohne Starter Held Items und ohne offene Writer.

## 2026-05-14 - CFRU/DPE Starters Suboptions Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/063_p1_starters_suboptions_regression_smoke.md` erstellt.
- Starter-Suboptionen aus Diagnose 061/062 ueber den belegten Starter-Species-Writer geplant.
- `FVX-SST-002` bleibt nur belegter Basis-/Carrier-Pfad.
- Geplante Slices dokumentiert: `FVX-SST-003`/`FVX-SST-004` Basic-/Evolution-Filter, `FVX-SST-005` Type Restrictions, `FVX-SST-006` Legendary Filter und `FVX-SST-009` BST-Min/Max separat.
- Starter Held Items `FVX-SST-007`/`FVX-SST-008`, Field Items/Shops/Pickup, Encounter Held Items, MoveData Write, Palette/Graphics, TypeChart, Text/Menu, Level Modifier und Evolution-Methoden-Writer bleiben ausgeschlossen.
- Erwartete spaetere Metriken, Artefaktregeln und Stop-Regeln dokumentiert; keine Hochstufung der Starter-Suboptionen auf P1-supported ohne separaten spaeteren Lauf.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`: BST-/Type-basierte Pooling-Suboptionen planen, ohne TypeChart oder MoveData-Write zu aktivieren.

## 2026-05-14 - CFRU/DPE Global Species Pool Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/062_p1_global_species_pool_regression_smoke.md` erstellt.
- Erster konkreter Regression-Smoke aus Diagnose 061 fuer Global Species Pools / Generation Limits geplant.
- Primaere Feature-IDs festgelegt: `FVX-GEN-001` Limit Pokemon und `FVX-GEN-002` No Premature Evolutions.
- Generation Limits und related-Pokemon-Scope werden unter `FVX-GEN-001` gefuehrt, weil keine separaten Feature-IDs existieren.
- `FVX-GEN-003` No Random Intro Mon und `FVX-GEN-004` Race Mode sind ausdruecklich nicht Teil dieses Smokes.
- Minimaler Carrier fuer spaetere Laeufe ist ein einzelner P1-stabiler Species-Writer, bevorzugt `FVX-SST-002`; optionaler Wild-Vergleich gegen `FVX-WILD-001` bleibt separat.
- Spaetere Smoke-Slices, erlaubte Settings, ausgeschlossene offene Writer, erwartete Metriken, Artefaktregeln und Stop-Regeln dokumentiert.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`: Starter-Poolfilter wie random basic/two evolutions, Type Restrictions, No Legendaries und BST-Min/Max getrennt von Starter-Held-Items planen.

## 2026-05-13 - CFRU/DPE P1 Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/061_p1_regression_smoke_plan.md` erstellt.
- Priorisierte Smoke-Gruppen aus Diagnose 060 und der FVX Feature-Coverage-Matrix abgeleitet.
- Feature-Coverage mit `130` Feature-/Suboption-Zeilen eingebunden; spaetere Smokes sollen Feature-IDs referenzieren.
- Smoke-Gruppen festgelegt: Global Species Pools / Generation Limits, Similar Strength / Same Type Pooling, Evolutions-Suboptionen ohne offene Method-/Item-/Move-Writer, Starters, Movesets/TM/Tutor/Egg, Trainer Level Modifier separat und Wild Level Modifier separat.
- Offene Writer explizit als Nicht-Smoke-Fixbereiche markiert: MoveData Write, Field Items/Shops/Pickup, Palette Randomization, TypeChart, Graphics/Sprites und Text/Menu.
- Allgemeine spaetere Metriken definiert: Save/Log/Output/Reload, relevanter Mismatch-Zaehler `0`, `stacktrace=none`, keine verbotenen Artefakte und Marker nur nach 055 klassifizieren.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke`: erster spaeterer Regression-Smoke fuer `Limit Pokemon`, Generation Limits und related Pokemon, strikt ohne offene Writer.

## 2026-05-13 - CFRU/DPE GUI-Suboptions-Regressionsmatrix

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-gui-suboptions-regression-matrix`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md` erstellt.
- Konkrete FVX-GUI-Hauptoptionen und Suboptionen wurden gegen den aktuellen CFRU/DPE-P1-Supportstand eingeordnet.
- Statusklassen festgelegt: `P1-supported`, `wahrscheinlich supported, aber nicht einzeln getestet`, `modelliert, Fix offen`, `open-not-diagnosed` und `out of scope`.
- Direkt belegte Datenpfade wurden von nur wahrscheinlich stabilen Suboptionen, modellierten offenen Writern und ungetesteten GUI-Kombinationen getrennt.
- Similar Strength, Same Type / Prefer Same Type, Follow Evolutions, Level Modifier, Force Change, Change Impossible Evolutions und Make Evolutions Easier wurden konservativ nach Datenpfad- und Writer-Risiko eingeordnet.
- Diagnose 055 bleibt Log-Hygiene-Grenze, 056 MoveData-Grenze, 057 Field-/Shop-/Pickup-Grenze, 058 Palette-/Graphics-Grenze und 059 TypeChart-Grenze.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan`: read-only Smoke-/Regression-Plan fuer priorisierte Suboptionen erstellen, bevor mehrere offene Writer in einem Fixbranch vermischt werden.

## 2026-05-13 - CFRU/DPE Type-Chart-Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/059_p1_type_chart_model.md` erstellt.
- Pokemon-Type-Read/Write aus Diagnose 051 wurde strikt von Type-Chart-/Effectiveness-Randomization getrennt.
- Klar dokumentiert: 051 beweist `gBaseStats`-Type-Read/Write inklusive Fairy `0x17` und `typeIdMismatches=0`, aber keinen Type-Chart-Support.
- Fairy `0x17` in Species-Daten wurde von Fairy-Effectiveness-Eintraegen in der TypeTable getrennt.
- Stellar `0x18` bleibt unsupported/preserve-only und darf nicht stillschweigend in Random-Pools oder TypeChart-Writes eingefuehrt werden.
- `TypeEffectivenessRandomizer`, `getTypeTable()`/`setTypeTable()`, `TypeEffectivenessOffset`, Foresight-/End-Table-Terminatoren und `nonNeutralEffectivenessCount` wurden als eigener Hochrisiko-Writer klassifiziert.
- Preserve-/Skip-Policy und Reload-/Diagnosekriterien fuer spaetere TypeChart-Fixbranches festgelegt.
- Diagnose 058 bleibt Palette-Grenze, 057 Item-/Field-/Shop-/Pickup-Grenze, 056 MoveData-Grenze und 055 Log-Hygiene-Grenze.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-gui-suboptions-regression-matrix`: GUI-Suboptionen nach den read-only Modellen 055-059 regressionsorientiert konsolidieren.

## 2026-05-13 - CFRU/DPE Palette-Randomization-Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/058_p1_palette_randomization_model.md` erstellt.
- Bestehende Palette-Safety wurde strikt von echter geaenderter Palette-Randomization getrennt.
- Safety-Stand eingeordnet: defensiver `loadPokemonPalettes()` fuer missing/invalid Slots und Skip-Unchanged-`savePokemonPalettes()` fuer unveraenderte CFRU/DPE-Pokemon-Paletten.
- Klar dokumentiert: `PokemonPalettesMod.RANDOM` und `Gen3to5PaletteRandomizer` sind echte Writer-Pfade und nicht durch die Safety-Diagnosen als P1-supported belegt.
- `savePokemonPalettes()`, `rewriteCompressedPalette()` und der komprimierte `DataRewriter`-Repointing-Pfad wurden als offene Hochrisiko-Writer klassifiziert.
- Shared/missing Palette-Pointer-Risiken dokumentiert, inklusive `SPECIES_CUBONE_A`-/`gMonPaletteTable[1038]`-Nullslot, DPE-Gap-Slots `[252]..[276]` und `gFrontSprite252Pal`/`gBackShinySprite252Pal`.
- Preserve-/Skip-Policy und Reload-/Diagnosekriterien fuer spaetere Palette-Fixbranches festgelegt.
- Graphics/Sprites bleiben ein eigenes P2-Modell; keine Vermischung mit Pokemon-Palette-Randomization.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`: Type-Chart- und moderne Type-Interaktion getrennt von Pokemon-Type-Read/Write modellieren.

## 2026-05-13 - CFRU/DPE Field Items / Shops / Pickup Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-field-items-shops-pickup-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md` erstellt.
- Field Items, Shops, Pickup und allgemeine Item-Randomization wurden strikt von Encounter Held Items aus Diagnose 054 getrennt.
- Item-Scope-Stand aus 053/054 eingeordnet: klassischer FVX-FRLG-`ItemCount=374`, CFRU-naher Scope bis `778`/`779`, DPE-Header-Scope bis ca. `799`, getesteter 054-Scope `item.count=778`.
- Field-Item-Risiken dokumentiert: Map-/Script-Kontext, required field TMs, moderne TM/HM-Items, Key-/System-/Placeholder-Items und eigener Reload-Nachweis.
- Shop-Randomization-Risiken dokumentiert: `ShopPointerOffsets`, Special-/Main-Game-Shop-Scope, Shopgroessen, Preise, Guaranteed Items und Text/Menu-Grenze.
- Pickup-Risiken dokumentiert: klassischer `PickupTableStartLocator`/`PickupItemCount`, CFRU `sPickupCommonItems`/`sPickupRareItems`, Probability-Slots und moderne Item-Pools.
- Preserve-/Skip-Policy und Reload-/Diagnosekriterien fuer spaetere Fixbranches festgelegt.
- Diagnose 055 bleibt Log-Hygiene-Grenze; Diagnose 056 bleibt Move-Data-Write-Grenze.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`: Vorhandene Palette-Safety von echter Palette-/Graphics-Randomization trennen und Write-/Repointing-Risiken modellieren.

## 2026-05-13 - CFRU/DPE Move-Data-Write-Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/056_p1_move_data_write_model.md` erstellt.
- Der aktuelle Move-Data-Read-Stand wurde aus vorhandenen Diagnosen eingeordnet: `moves.total=992`, hoechster geladener Move `991:PsychicNoise`, Category-Verteilung aus Diagnose 034.
- Das CFRU/DPE-`BattleMove`-Layout wurde als 12-Byte-Entry mit `split` bei Byte `+10` dokumentiert.
- Der aktuelle Gen3-`saveMoves()`-Pfad wurde read-only klassifiziert: Move-Namen und die ersten fuenf MoveData-Bytes werden geschrieben; `secondaryEffectChance`, `target`, `priority`, `flags`, `z_move_power`, `split` und `z_move_effect` bleiben nicht als Writer modelliert.
- Preserve-Policy und Reload-Kriterien fuer einen spaeteren Move-Data-Write-Fix wurden festgelegt.
- Diagnose 055 bleibt die Grenze: Log-Hygiene/Fallback-Marker sind getrennt von echten MoveData-Writer-/Scope-Risiken.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-field-items-shops-pickup-model`: Field Items, Shops, Pickup und allgemeine Item-Randomization getrennt von Encounter Held Items modellieren.

## 2026-05-13 - CFRU/DPE Type Log / Placeholder Hygiene

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-type-log-placeholder-hygiene`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/055_type_log_placeholder_hygiene.md` erstellt.
- `Bad Egg`, `<unknown>`, Unknown-Type-/Unknown-Ability-/Unknown-Item-Marker und Placeholder-/Null-Species wurden strikt aus bestehenden Protokollen und read-only `rg`-Befunden klassifiziert.
- Die Marker aus 051/052/054 blockieren den dokumentierten P1-Support nicht, solange Save/Log/Output/Reload stabil bleiben und die jeweiligen Mismatch-Zaehler `0` sind.
- Echte Blocker bleiben getrennt: Null-Species-/BST-zero-/all-zero-Ability-Species sind nur dann Blocker, wenn ein konkreter Randomizer-Pfad abbricht, falsch schreibt oder falsch reloadet.
- Log-Hygiene wurde getrennt von Type-Chart-, Ability-Name-, Item-Name-, Species-Scope- und Fix-Themen dokumentiert.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`: Move-Data-Write fuer `moves.total=992`, `BattleMove.split` und CFRU/DPE-Felder read-only modellieren.

## 2026-05-13 - CFRU/DPE Encounter Held Items Scope-and-Write Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`

Aktueller Stand:

- Workspace PR #91 als gemerged geprueft.
- UPR-FVX-Fix `5c7170b654b09e1fc27ced6857dd50a8e4711f08` erstellt.
- CFRU/DPE-gegateter Item-Scope implementiert: DPE-Oberregion bis `798` wird nur bei plausiblen Itemnamen genutzt, sonst konservativer Scope bis `778`.
- Itemnamen-Fallbacks bleiben sichtbar als `item #<id>` und werden nicht als Random-Pick zugelassen.
- Moderne Bad-/Banned-Filter fuer Encounter Held Items ergaenzt: TMs/HMs, Mail, Balls, Free-/Placeholder-/Shiny-Space, Booster Energy, Tera Orb, Portable PC und modellierte Form-/Mega-/Z-/Plate-/Mask-/Utility-Items.
- Encounter Held Items in `gBaseStats` bei `item1/item2` (`0x0C`/`0x0E`) werden read/write/reload-stabil behandelt; moderne bestehende IDs werden preserved statt zu `0` zu kollabieren.
- Neues Diagnoseprotokoll `08_tests/randomizer/054_encounter_held_items_scope_write_diagnostics.md` erstellt.
- Encounter Held Items-only, Encounter Held Items + Base Stats, + Abilities und + Types liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true` und `writeReloadEncounterHeldItemMismatches=0`.
- Keine Field-Items-, Shops-, Pickup-, Move-Data-, Tutor-, Egg-Move-, Palette/Graphics-, Type-Chart- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs einen der offenen Matrixbereiche modellieren: Move-Data-Write, Field Items/Shops/Pickup, Palette/Graphics, Type-Chart oder Placeholder-/Bad-Egg-Log-Hygiene.

## 2026-05-13 - CFRU/DPE Item-/Bad-Item-/Encounter-Held-Item Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-item-data-and-bad-item-model`

Aktueller Stand:

- Workspace PR #90 und UPR-FVX PR #27 als gemerged geprueft.
- Neues read-only Analyseprotokoll `08_tests/randomizer/053_p1_item_data_and_bad_item_model.md` erstellt.
- CFRU/DPE Itemgrenzen eingeordnet: CFRU-naher Scope bis `ITEM_FREE_SPACE3=778` / `ITEMS_COUNT=779`, DPE-Header-Scope bis `ITEM_SHINY_SPACE20 + 1` / ca. `799`.
- FVX-Risiko dokumentiert: klassischer FireRed `ItemCount=374`, `itemIDToStandard(...)`-Fallback ueber `UNIQUE_OFFSET` und unvollstaendige moderne Itemnamen-/Bad-Item-Abdeckung.
- Encounter Held Items liegen in `gBaseStats` als `u16 item1/item2` bei Offsets `0x0C/0x0E`; Felder sind eng fixbar, aber nicht sicher ohne erweiterten Item-Scope und moderne Bad-/Key-Item-Filter.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.

Naechster sinnvoller Schritt:

- Fixbranch `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`: CFRU/DPE-gated ItemCount-/Itemnamen-Scope, moderne Bad-/Banned-Item-Filter und Encounter-Held-Item-Read/Write/Reload diagnostisch absichern.

## 2026-05-13 - CFRU/DPE Abilities + Hidden Ability Scope-and-Write Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-abilities-hidden-ability-scope-and-write`

Aktueller Stand:

- Workspace PR #89 und UPR-FVX PR #26 als gemerged geprueft.
- UPR-FVX-Fix `639c7e61adbeffea2e29b1d0dafdba8a02a83f89` erstellt.
- CFRU/DPE-gegatetes Ability-Modell implementiert: Ability1/2 bleiben bei BaseStats-Offsets `0x16/0x17`, Hidden Ability wird bei Offset `0x1A` gelesen/geschrieben.
- CFRU/DPE meldet `abilitiesPerSpecies=3` und `highestAbilityIndex=254` / `0xFE`.
- Ability-Namen werden bis `0xFE` geladen; fehlende moderne Namen fallen sichtbar auf `ability #<id>` zurueck.
- `SpeciesAbilityRandomizer` skippt Placeholder-/Null-Species, `BST == 0`, all-zero-Ability-Species und invalid Ability-IDs defensiv.
- Neues Diagnoseprotokoll `08_tests/randomizer/052_abilities_hidden_ability_scope_write_diagnostics.md` erstellt.
- Ability1/2-only, Hidden Ability-only, Ability1/2 + Hidden Ability und Base Stats + Types + Abilities liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `writeReloadAbilityMismatches=0` und `writeReloadHiddenAbilityMismatches=0`.
- Keine Encounter-Held-Item-, Move-Data-Write-, Tutor-, Egg-Move-, Palette/Graphics-, Type-Chart- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Item-/Bad-Item-Modell fuer Encounter Held Items starten oder vorher Placeholder-/Unknown-Type-/Bad-Egg-Log-Hygiene separat einordnen.

## 2026-05-13 - CFRU/DPE Base Stats + Types Scope-and-Write Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write`

Aktueller Stand:

- Workspace PR #88 als gemerged geprueft.
- UPR-FVX-Fix `20f16d07ab4ea62e5cd3f27ef09a6d5b036d2392` erstellt.
- CFRU/DPE-gegatetes BaseStats-Type-Mapping implementiert: raw `0x17` wird als `Type.FAIRY` gelesen und `Type.FAIRY` als `0x17` geschrieben.
- CFRU/DPE-TypeTable-Pool enthaelt Fairy, aber kein Stellar; Stellar-/unsupported Primary-Type-Species werden im Type-Randomizer defensiv uebersprungen.
- Neues Diagnoseprotokoll `08_tests/randomizer/051_base_stats_types_scope_write_diagnostics.md` erstellt.
- Base Stats-only, Types-only und Base Stats + Types liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `writeReloadBaseStatsMismatches=0` und `typeIdMismatches=0`.
- Keine Hidden-Ability-, Encounter-Held-Item-, Move-Data-Write-, Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Hidden Abilities separat fixen oder vorher Item-/Bad-Item-Modell fuer Encounter Held Items starten.

## 2026-05-13 - CFRU/DPE Base Stats, Types, Abilities Model

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model`

Aktueller Stand:

- UPR-FVX PR #25 und Workspace PR #87 als gemerged geprueft.
- Neues read-only Protokoll `08_tests/randomizer/050_p1_base_stats_types_abilities_model.md` erstellt.
- `gBaseStats` fuer den getesteten CFRU/DPE Gen9-BPRE-Stand modelliert: Pointer-Ort `0x080001BC`, Entry-Size `0x1C`, internes Species-Indexing bis `SPECIES_PECHARUNT=0x59F` / `NUM_SPECIES=1440`.
- CFRU BaseStats-Felder eingeordnet: Stats, `type1/type2`, `item1/item2`, `ability1/ability2` und `hiddenAbility` bei Offset `0x1A`.
- FVX-Risiken dokumentiert: Gen3-Type-Mapping liest/schreibt Fairy aktuell nicht korrekt, Stellar ist nicht im FVX-Type-Enum, Hidden Ability wird nicht gelesen/geschrieben, Ability-Count ist `77` statt CFRU `255`, Encounter Held Items haengen am erweiterten Itemmodell.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein ROM-/Build-/Log-Artefakt.

Naechster sinnvoller Schritt:

- `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write` als kleinen ersten Fixbranch planen.
- Hidden Abilities und Encounter Held Items getrennt behandeln; Encounter Held Items erst nach Item-/Bad-Item-Modell.

## 2026-05-13 - CFRU/DPE Learnset GUI Flow Safety Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`

Aktueller Stand:

- UPR-FVX-Fix `086d2a9177df7624a0e7ca1876b210a200d7aa98` erstellt.
- Logger-Nullsafety, Learnset-Repointing-Multiwrite-Safety, Trainer-Movesets-Key-Fallbacks sowie TM/HM-/Tutor-Level-Up-Sanity defensiv stabilisiert.
- Neues Protokoll `08_tests/randomizer/049_p1_learnset_gui_flow_safety_fix_diagnostics.md` erstellt.
- Sieben GameRandomizer-nahe Movesets/Learnsets-Laeufe diagnostiziert: Movesets-only, Trainer-Movesets, Reorder-Damaging, TM/HM-Sanity, Tutor-Sanity, gekoppelte Egg Moves und TM/HM+Tutor-Sanity.
- Alle Laeufe liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true` und `writeReloadLearnsetMismatches=0`.
- Reorder-Damaging nutzt zwei freie Learnset-Blob-Bloecke innerhalb `0x1219A48-0x1600000`; der zweite Write blockiert nicht mehr an einem statischen FreeSpace-Start.
- Keine Move-Data-Write-, Tutor-Text/Menu-, Special-Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.
- Danach Move-Data-Write, Items/Shops/Field, Palette/Graphics und Special-Tutor/Text/Menu separat modellieren.

## 2026-05-13 - CFRU/DPE Learnset GUI Combination Diagnostics

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-learnset-gui-combinations`

Aktueller Stand:

- UPR-FVX PR #24 und Workspace PR #85 als gemerged geprueft.
- Neues Protokoll `08_tests/randomizer/048_p1_learnset_gui_combinations.md` erstellt.
- GameRandomizer-nahe Movesets/Learnsets-Laeufe diagnostiziert; keine Codeaenderung und keine `02_external/**`-Aenderung.
- Erster Learnset-Repointing-Write bleibt stabil: `plannedBlobBytes=30099`, `writtenBlobBytes=31771`, `pointertableEntriesUpdated=1413`, `writeReloadLearnsetMismatches=0`.
- Movesets-only, Movesets+TM/HM ohne Level-Up-Sanity, Movesets+Tutor ohne Level-Up-Sanity und gekoppelte Egg Moves speichern/reloaden stabil.
- Voller GUI-P1-Support bleibt blockiert durch Logger-Fehler, Trainer-Movesets-Kombinationen, Reorder-Damaging-Moves sowie TM/HM-/Tutor-Level-Up-Sanity.

Naechster sinnvoller Schritt:

- Fixbranch `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety` starten.
- Ziele: multi-write-sicheren Learnset-Repointing-Pfad, interne Species-ID-Key-Fallbacks fuer Sanity/Trainer-Movesets und Logger-Nullpfad beheben.


## 2026-05-13 - CFRU/DPE Learnset-Write Repointing Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`

Aktueller Stand:

- UPR-FVX-Fix `77de517da880bebb6ed690ca6e170e5bd10b9cad` erstellt.
- `setMovesLearnt()` schreibt fuer den eng gegateten CFRU/DPE Gen9-BPRE-Pfad neue Level-Up-Learnset-Blobs in die validierte FreeSpace-Region `0x1219A48-0x1600000`.
- Die bestehende `gLevelUpLearnsets`-Pointertable bei `0x25D7B4` bleibt erhalten und wird pro interner Species-ID aktualisiert.
- Diagnose 046 bestaetigt `plannedBlobBytes=17418`, `writtenBlobBytes=11547`, `uniqueBlobCount=416`, `pointertableEntriesUpdated=1413` und `writeReloadLearnsetMismatches=0`.
- Save, Reload, Output-ROM und nichtleerer Log waren im lokalen Diagnoseharness erfolgreich; lokale Artefakte blieben ignored unter `05_builds/**`.
- Keine Move-Data-Write-, Tutor-Text-, Special-Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs einen GUI-/Settings-Kombinationssmoke fuer Pokemon Movesets/Learnsets planen.
- Danach `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.


## 2026-05-13 - FVX GUI Options Compatibility Matrix

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-fvx-gui-options-matrix`

Aktueller Stand:

- Matrixprotokoll `08_tests/randomizer/047_fvx_gui_options_compatibility_matrix.md` erstellt.
- P1-supported Bereiche aus vorhandenen Diagnosen zusammengefuehrt: Standard/Fallback-Wild, Starters, Static/Gift, Trainer Species, Trainer Movesets, Trainer Held Items, Evolutions, Move-Data-Read, TM/HM 128-Slot, normale Tutor-Tabellen und direkte Egg Moves.
- Teilunterstuetzte Bereiche markiert: bounded Learnset-Write, Palette-Safety und Move-Data-Read ohne Write.
- Offene Hochrisiko-Writer priorisiert: Full Learnset Repointing, Base Stats/Types/Abilities, Move-Data-Write, Items/Shops/Field/Pickup und Palette/Graphics-Randomization.
- Keine Codeaenderung, keine `02_external/**`-Aenderung und keine ROM-/Build-/Tool-Artefakte.

Naechster sinnvoller Schritt:

- Wenn Phase 2 FreeSpace-Nachweis positiv ist, `compat/upr-fvx-cfru-dpe-learnset-write-repointing` fortsetzen.
- Andernfalls zuerst `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #80 ist gemerged.
- UPR-FVX PR #23 und Workspace PR #81 sind gemerged.
- UPR-FVX-Stand im Workspace: `5c7170b654b09e1fc27ced6857dd50a8e4711f08`.
- TM/HM-only ist im getesteten CFRU/DPE-128-Slot-Scope P1-supported.
- Tutor-only ist im getesteten CFRU/DPE-152-Slot-Scope P1-supported.
- Egg-Move direct scope ist P1-supported.
- Learnset-Write bounded in-place ist implementiert und diagnostisch stabil fuer strikt validierte same-size Writes.
- Full Learnset-Write-Repointing ist im direkten `setMovesLearnt()`-Scope implementiert und diagnostisch stabil.
- Pokemon Movesets/Learnsets sind im getesteten GUI-/Settings-nahen Flow P1-supported.
- Encounter Held Items sind im getesteten CFRU/DPE-`gBaseStats`-Scope P1-supported.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`

## Aktueller Arbeitsblock

CFRU/DPE Palette-Randomization-Modell.

## Ziel

Read-only modellieren, wie bestehende Palette-Safety von echter geaenderter Palette-/Graphics-Randomization zu trennen ist.

## In diesem Arbeitsblock geprueft / geaendert

- Workspace-Branch `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model` genutzt; nicht auf `main` gearbeitet.
- Pflichtdokumente und Diagnosen 047/055/056/057 sowie vorhandene Palette-Safety-Protokolle gelesen.
- Read-only `rg`-Suche nach Palette-, `PokemonPalettesMod.RANDOM`-, `Gen3to5PaletteRandomizer`-, `savePokemonPalettes()`-, `rewriteCompressedPalette()`-, compressed-, repoint-, sprite- und graphics-Markern ausgefuehrt.
- Neues Protokoll erstellt: `08_tests/randomizer/058_p1_palette_randomization_model.md`.
- `08_tests/randomizer/README.md`, `SESSION_STATE.md`, `NEXT_STEPS.md` und Roadmap aktualisiert.
- Tool-Manifest nicht geaendert, weil kein Tool-/Repo-/Commit-/Submodule-Stand geaendert wurde.

## Ergebnis

- Palette-Safety ist nur fuer defensive Loads, missing/invalid Slots und unveraenderte Palette-Saves belegt.
- Echte geaenderte Palette-Randomization ueber `PokemonPalettesMod.RANDOM` / `Gen3to5PaletteRandomizer` bleibt open / not diagnosed.
- `savePokemonPalettes()` faellt bei geaenderten Paletten in compressed Write-/Repointing-Semantik.
- Shared/missing Palette-Pointer, Dex-/Pokedex-Mapping und FreeSpace/Repointing bleiben eigene Risiken.
- Graphics/Sprites bleiben ein separates P2-Modell.

## Noch nicht gestartet

- Special-Tutor-Modell/Fix
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Vollstaendige Nullslot-`<unknown>`-Analyse ausserhalb der bereits dokumentierten Klassifikation
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen.

Lokale Diagnose-Artefakte blieben ignored unter `05_builds/**` und wurden nicht committed.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

UPR-FVX und andere `02_external/**`-Repos blieben in diesem Analyseblock unangetastet.

Keine Type-Chart-, Ability-Name-, Item-Name-, Move-Data-Write-, Tutor-Text/Menu-, Special-Tutor-, Egg-Move-, Graphics/Sprite- oder Text/Menu-Ausweitung.

Keine MCP-Configs mit Secrets angelegt.

## Naechste Pruefung

Lokal im Workspace nach den Dokumentationsaenderungen pruefen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

## Naechster empfohlener Branch

Nach Merge dieses Analyseblocks: `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`. Graphics/Sprites, Special Tutors, Tutor-Text/Menu-Rewrites und spaetere Palette- oder Field-Items-/Shops-/Pickup-Fixes bleiben eigene Folgebranches.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-learnset-repointing-model

- UPR-FVX PR #23 und Workspace PR #81 als gemerged geprueft.
- CFRU/DPE Learnset-Repointing-Modell read-only dokumentiert.
- `gLevelUpLearnsets` Pointer-Ort `0x03EA7C` zeigt auf die aktive Pointertable bei `0x25D7B4`.
- Quellenanalyse: `1408` Pointertable-Zuweisungen, `1104` eindeutige Learnset-Ziele, `148` Shared-Zielgruppen.
- Kein statisch freier Append-Bereich belastbar belegt; spaeterer Fix muss FreeSpace im konkreten ROM nachweisen.
- Kein Fix, keine Aenderung an `02_external/**`, kein Repointing.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-learnset-write-bounded

- Workspace PR #80 als gemerged geprueft.
- UPR-FVX-Fix `dd9d80c16936a99bac1d7ef777b43baa7c2f029d` erstellt.
- `setMovesLearnt()` erhaelt einen eng gegateten CFRU/DPE bounded in-place Write-Pfad fuer `gLevelUpLearnsets`.
- Kein Repointing: Growth wird diagnostiziert und uebersprungen.
- Diagnose 044 bestaetigt Save/Log/Output/Reload und `writeReloadLearnsetMismatches=0`.
- Writer akzeptiert im Test `boundedWrites=1` und skippt `1412` unsafe Pointer; voller Learnset-Write braucht ein separates Repointing-Modell.
- Keine Move-Data-Write-, Tutor-Text-, Special-Tutor- oder Egg-Move-Ausweitung.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-egg-move-model

- UPR-FVX PR #21 und Workspace PR #77 als gemerged geprueft.
- CFRU/DPE Egg-Move-Modell read-only dokumentiert.
- `gEggMoves` als `u16`-Stream mit Species-Marker `species + 20000` und Terminator `0xFFFF` eingeordnet.
- DPE `repointall` zeigt `gEggMoves 08045C50`; FVX nutzt aktuell noch `EggMoves=0x25EF0C` aus dem FireRed-RomEntry.
- DPE-Egg-Move-Stream enthaelt Gen8-/PLA-/Paldea-Species und Move-IDs bis `MOVE_TIDYUP` ID `967`.
- Aktuelle FVX-Risiken: Pokédex-ID-Mapping statt interner Species-ID, globale Move-Ban-Arrays mit Laenge `827`, Egg-Move-Randomization an Learnset-Write gekoppelt.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility

- Workspace PR #76 als gemerged geprueft.
- UPR-FVX-Fix `4ce93754de390e9177efd2541c02edba0afbb0c4` erstellt.
- CFRU/DPE-Tutor-Pfad eng ueber `useCfruDpeGen9SpeciesCount` gegatet.
- `gMoveTutorMoves` als `u16[152]` ueber `0x8120BE4` gelesen/geschrieben.
- `gTutorLearnsets` als 19-Byte-/152-Bit-Compatibility pro Species ueber `0x8120C30` gelesen/geschrieben.
- Diagnose 040 bestaetigt Tutor moves-only, Compatibility-only und Tutor moves + Compatibility mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Special-Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder Tutor-Text-Rewrite-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tutor-model

- UPR-FVX PR #20 und Workspace PR #75 als gemerged geprueft.
- CFRU/DPE Tutor-/Special-Tutor-Modell read-only dokumentiert.
- `gMoveTutorMoves` als `u16[152]` ueber Pointer-Location `0x8120BE4` eingeordnet.
- `gTutorLearnsets` als 152-Bit-/19-Byte-Compatibility pro Species ueber Pointer-Location `0x8120C30` eingeordnet.
- Special Tutors als Sonderlogik ausserhalb der normalen Tabelle dokumentiert.
- FVX nutzt aktuell weiterhin klassischen FireRed-Tutor-Scope `15`; Tutor-only bleibt nicht P1-supported.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tm-hm-128-slot

- Workspace PR #74 als gemerged geprueft.
- UPR-FVX-Fix `58379ffd3146fcd6bb0eb416647cdf9b752cfc0e` erstellt.
- CFRU/DPE-128-Slot-TM/HM-Pfad eng ueber `useCfruDpeGen9SpeciesCount` gegatet.
- `gTMHMMoves` als `u16[128]` ueber `0x8125A8C` gelesen/geschrieben; TMs `0..119`, HMs `120..127`.
- `gTMHMLearnsets` als 16-Byte-/128-Bit-Compatibility pro Species ueber `0x8043C68` gelesen/geschrieben.
- Diagnose 038 bestaetigt TM moves-only, Compatibility-only und TM moves + Compatibility mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder TM51..TM120-Item-Text-/Palette-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model

- UPR-FVX PR #19 und Workspace PR #73 als gemerged geprueft.
- CFRU/DPE-128-Slot-TM/HM-Modell read-only dokumentiert.
- `gTMHMMoves` ist `u16[128]` ueber Pointer `0x8125A8C`; TMs `1..120`, HMs `121..128`.
- `gTMHMLearnsets` ist 128-Bit-/16-Byte-Compatibility pro Species ueber Pointer `0x8043C68`.
- FVX-`50+8`-Pfad bleibt P1-supported, bildet aber das 128-Slot-Modell nicht ab.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety

- Workspace PR #72 als gemerged geprueft.
- UPR-FVX-Fix `32e43ac03a5762542773213a13be4e0389f1deae` erstellt.
- TM-Move-Randomization fuer CFRU/DPE gegen Move-IDs oberhalb der alten FVX-Sicherheitslisten abgesichert.
- TM/HM-Compatibility fuer CFRU/DPE gegen Placeholder-Species und `null`-Typen abgesichert.
- Diagnose 036 bestaetigt TM moves + Compatibility, Compatibility-only und TM moves-only mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder 128-Slot-TM/HM-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-only

- UPR-FVX PR #18 und Workspace PR #71 als gemerged geprueft.
- TM/HM-only Diagnose auf UPR-FVX `c71fd75e67f5a839560bbf5de7c6f17317a64bd1` ausgefuehrt.
- FVX erkennt nur klassisches `50+8`-TM/HM-Modell.
- TM-Move-Randomization blockiert an altem Move-Ban-Array-Limit.
- TM/HM-Compatibility-only blockiert separat an Null-Type-Species.
- Neues Protokoll erstellt: `08_tests/randomizer/035_p1_tm_hm_only.md`.
- Kein Fix, keine Randomizer-Codeaenderung, keine committed ROM-/Build-Artefakte.

## 2026-05-13 - CFRU/DPE Egg-Move scope/write fix

- Active branch: `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write`.
- UPR-FVX fix commit: `18168b78b973a4c39f34053ac58f21279a26d8d2`.
- Implemented a gated CFRU/DPE `gEggMoves` reader/writer through pointer location `0x45C50` while preserving the classic `u16` stream, `species + 20000` markers, and `0xFFFF` sentinel.
- Preserved internal `SpeciesSet` identity for Egg-Move keys and guarded high move-ID flag-array access in `SpeciesMovesetRandomizer`.
- Added diagnosis `08_tests/randomizer/042_egg_moves_scope_and_write_fix_diagnostics.md`.
- Direct Egg-Move harness result: `moves.total=992`, highest loaded move `991:PsychicNoise`, target pointer `0x09A0E94C`, species entries `436 -> 436 -> 436`, highest species `1412`, highest move after/reload `991`, `writeReloadEggMoveMismatches=0`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`.
- No Learnset-Write, Move-Data-Write, Tutor-Text, Special-Tutor, or `setMovesLearnt()` expansion was included.

## 2026-05-13 - CFRU/DPE Learnset-Write-Modell

- Active branch: `analysis/upr-fvx-cfru-dpe-p1-learnset-write-model`.
- UPR-FVX PR #22 und Workspace PR #79 als gemerged geprueft.
- `gLevelUpLearnsets` Write-Modell read-only dokumentiert; keine Aenderung an `02_external/**`.
- Neues Protokoll: `08_tests/randomizer/043_p1_learnset_write_model.md`.
- Befund: Pointer-Ort `0x03EA7C` / `0x0803EA7C`, interne Species-ID-Pointertabelle, Eintraege `u16 move + u8 level`, Sentinel `{0, 0xFF}`, `MAX_LEARNABLE_MOVES=50`, Species bis `SPECIES_PECHARUNT=0x59F`, Moves bis `MOVE_PSYCHICNOISE=0x3DF`.
- Empfehlung: Folgefix nur eng gegatet und zunaechst bounded in-place; Repointing separat modellieren.
