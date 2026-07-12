# CFRU hidden item sparkle QoL smoke handoff

Status: `VISUAL_TUNING_AND_MULTI_ITEM_FIX_PENDING_MANUAL_SMOKE` on CFRU branch `fix/cfru-hidden-item-sparkle-small-visual`, commit `98c9038dd20e62ee58a7482bf9ef96485f06e4ad`, Draft PR `https://github.com/Planton361/CFRU-expansion/pull/31`.

Base: current `compat/firered-gen9-randomizer` commit `325212e325023284bd6198a3a9cd75b60e0c21f8`, including linker fix `05b4231d847a1aa71d53f846b818403e887f4d3f`.

No pass result is documented. No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, private path, token, secret, `.env`, binary patch, raw address port, Itemfinder feature, Field Item randomizer writer, visible itemball graphics, other map or DPE change is included.

## Current user fail

Prior candidate `d77da7fdb6c1ceeb946615bb2b31dcd2bbcf9ddd` failed manual acceptance:

- visible footprint remained somewhat too large;
- 16-frame starts caused excessive flicker;
- white/cyan was the wrong color direction;
- after collecting Antidote first, the remaining Potion marker never appeared again.

No case is promoted to pass from that smoke.

## Root cause and fix candidate

The failed smoke is consistent with the prior lifecycle: `RunOnTransitionMapScript` started one-shot `FLDEFF_SPARKLE` effects before `InitMap`, once for each distant Viridian Forest coordinate. A one-shot effect is camera-relative and finite, so an off-screen map-entry sparkle ends before the player reaches its tile.

The first task-based fix candidate then failed the user's complete local clean build at link time with undefined reference to `gFieldEffectObjectTemplatePointers`. Its syntax-only compile could not expose that missing linkable definition. The follow-up removes the direct template-table dependency and identifies the new sparkle by snapshotting all sprite `inUse` states before the synchronous field-effect start, then selecting only a slot that transitions from unused to used.

The linker-fixed pilot is now user-confirmed visible and repeating, but its general CFRU `FLDEFF_SPARKLE` visual is too large and bright, producing a strong cross-star. The small-visual candidate replaces only this pilot asset with a local Cyan-derived 16x16, two-frame sparkle and subtle palette.

The first small-visual callback used `FieldEffectFreeGraphicsResources` to destroy a local non-Field-Effect Sprite. It did not synchronously clear the owning task's Sprite id. That left correctness dependent on a later task-frame inspection of a mutable Sprite slot; during pickup/presentation transitions the single-ownership gate could remain stale and suppress the other item. The refined callback carries the task id, validates the task/function/Sprite id, clears ownership first, and then calls `DestroySprite`.

The pilot table no longer carries a duplicate hard-coded flag. Each flag is derived from the actually matched hidden-item BG event, so setting Antidote disables only Antidote and setting Potion disables only Potion. Independent cooldowns and round-robin selection keep both candidates eligible.

The existing Viridian-Forest-only task still:

- wait for `CB2_Overworld`, inactive palette fade, and a live player sprite;
- validate the exact hidden-item BG event before every candidate start;
- require the coordinate to be fully inside the current display;
- check the matching hidden-item flag before every start and while a pilot sprite is active;
- repeat on a tuned 60-frame interval while visible and uncollected;
- own at most one marked pilot sparkle sprite at once;
- stop the owned sprite immediately after its flag is set;
- destroy the owned sprite and task on map change;
- re-establish the task from transition and resume hooks after overworld task resets.

The visible pilot no longer uses `FLDEFF_SPARKLE` or `FLDEFF_REPEATING_SPARKLES`. A CFRU-owned local SpriteTemplate creates the compact sprite directly, so unrelated global Field Effects and the Field Effect active list remain untouched. Its 3/5/5 animation-end callback frees local sprite/palette resources; pickup and map-change cleanup use the same resource-free path.

## Cyan small-sparkle comparison

| Property | Prior CFRU pilot | Cyan reference / candidate |
|---|---|---|
| Visible asset | prior small visual still somewhat large | centered approximately 8x8 warm sparkle in stable 16x16 canvas |
| OAM | local 16x16 OAM | local 16x16 OAM retained for positioning |
| Frames | global sparkle lifecycle | two frames |
| Animation | excessive `3 / 5 / 5` flicker | calmer `6 / 10 / 8`, then destroy |
| Palette | unwanted white/cyan | warm gold, light yellow, yellow off-white |
| Cooldown | excessive 16-frame starts | 60 frames |
| Ownership | callback destroyed without atomic task notification | callback clears validated task/Sprite ownership before `DestroySprite` |

Source verification for the linker follow-up:

- `FieldEffectStart` runs the selected field-effect script synchronously to completion.
- CFRU `FldEff_Sparkle` invokes exactly one `CreateSpriteAtEnd`.
- `UpdateSparkleFieldEffect` uses `data[0]` and `data[1]`; `data[7]` remains available for the pilot ownership marker.
- A full sprite table prevents the start.
- If no slot transitions to `inUse`, the new `FLDEFF_SPARKLE` active-list entry is removed and the start returns failure without recording sprite ownership.

## Pilot inventory

| Map | Hidden item | Coordinate | Elevation | Flag/state | Quantity | Underfoot | Candidate marker |
|---|---|---:|---:|---|---:|---|---|
| `MAP_VIRIDIAN_FOREST` | `ITEM_POTION` | `(3, 22)` | `3` | matched BG-event offset `0` | `1` | `false` | centered ~8x8 warm sparkle, cooldown 60 |
| `MAP_VIRIDIAN_FOREST` | `ITEM_ANTIDOTE` | `(28, 57)` | `0` | matched BG-event offset `1` | `1` | `false` | centered ~8x8 warm sparkle, cooldown 60 |

## Manual smoke matrix

Clean build before smoke from the CFRU root:

```sh
python3 scripts/clean.py BUILD
python3 scripts/make.py
```

| Case | Setup | Expected result | Result |
|---|---|---|---|
| Fresh entry/readiness | enter Viridian Forest from outside with both flags unset | no load/fade artifact; normal overworld appears | not run |
| Potion visual/approach | walk to `(3, 22)` without using Itemfinder | centered ~8x8 warm-yellow sparkle is readable without dominant cross arms | not run |
| Potion duplicate guard | remain near `(3, 22)` through several intervals | one controlled sparkle sequence at a time; no accumulating identical sprites | not run |
| Potion pickup/flag stop | pick up Potion normally, then remain nearby | normal grant/text flow; no new Potion sparkle after the flag is set | not run |
| Antidote visual/approach | walk to `(28, 57)` with its flag unset | same tuned warm sparkle begins on approach | not run |
| Antidote pickup/flag stop | pick up Antidote normally, then remain nearby | normal grant/text flow; no new Antidote sparkle after the flag is set | not run |
| Antidote-first order | with both unset, collect Antidote first, then approach Potion | Antidote stops; Potion remains independently eligible and sparkles | not run |
| Potion-first order | from fresh both-unset state, collect Potion first, then approach Antidote | Potion stops; Antidote remains independently eligible and sparkles | not run |
| Both collected | re-enter with both flags set | neither pilot position sparkles | not run |
| Map-change cleanup | leave Viridian Forest while a pilot sparkle is visible | no sparkle or pilot-task symptom on the destination map | not run |
| Resume behavior | return from a menu/battle or re-enter the forest with one flag unset | remaining marker scheduling resumes after overworld readiness | not run |
| Existing map behavior | test signs, trainers, exits and visible item balls | unchanged | not run |
| Itemfinder non-scope | optionally use Itemfinder near each pilot | existing behavior remains unchanged; pilot does not depend on Itemfinder | not run |
| Global sparkle regression | trigger any unrelated global `FLDEFF_SPARKLE` use available in normal play | original unrelated visual remains unchanged | not run |

## Automated/source checks

- CFRU `git diff --check`: pass.
- CFRU syntax-only compile of `src/overworld.c`: pass.
- `rg -n "gFieldEffectObjectTemplatePointers|FLDEFFOBJ_SMALL_SPARKLE" src/overworld.c`: no matches.
- CFRU source build/link with `python3 scripts/build.py`: pass, with existing unrelated compiler/linker warnings only.
- Temporary local logic model: pass for Antidote-first, Potion-first, both collected, single ownership, map cleanup and resume with one remaining item.
- Workspace `git diff --check`: pass.
- Prior complete local CFRU clean build: user-reported linker fail on undefined `gFieldEffectObjectTemplatePointers`.
- Clean CFRU ROM insertion build for the small-visual candidate: pending user run; not run by Codex because `scripts/make.py` reads/modifies the local ROM and repository rules prohibit Codex from reading or modifying ROM files.
- Runtime smoke: not run.

## Acceptance boundary

Do not promote beyond `VISUAL_TUNING_AND_MULTI_ITEM_FIX_PENDING_MANUAL_SMOKE` until both pickup orders, tuned visual/frequency, duplicate guard, both-collected state, map cleanup, resume and global-sparkle regression pass. Even after a pass, this remains a two-item Viridian Forest pilot, not evidence for a global rollout, underfoot/renewable hidden items, full playthrough, BizHawk, Ironmon Tracker or P1 support.
