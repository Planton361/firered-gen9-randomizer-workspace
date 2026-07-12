# CFRU hidden item sparkle QoL smoke handoff

Status: `FIX_CANDIDATE_PENDING_LOCAL_REBUILD` on CFRU branch `fix/cfru-hidden-item-sparkle-pilot-visibility`, follow-up commit `05b4231d847a1aa71d53f846b818403e887f4d3f`.

CFRU PR #29 is already merged at prior commit `b32e2ec0fc10902408322848217ae63f9161073a`; the follow-up commit is not part of that merged PR. No replacement branch or PR is created in this block.

No pass result is documented. No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, private path, token, secret, `.env`, binary patch, raw address port, Itemfinder feature, Field Item randomizer writer, visible itemball graphics, other map or DPE change is included.

## Root cause and fix candidate

The failed smoke is consistent with the prior lifecycle: `RunOnTransitionMapScript` started one-shot `FLDEFF_SPARKLE` effects before `InitMap`, once for each distant Viridian Forest coordinate. A one-shot effect is camera-relative and finite, so an off-screen map-entry sparkle ends before the player reaches its tile.

The first task-based fix candidate then failed the user's complete local clean build at link time with undefined reference to `gFieldEffectObjectTemplatePointers`. Its syntax-only compile could not expose that missing linkable definition. The follow-up removes the direct template-table dependency and identifies the new sparkle by snapshotting all sprite `inUse` states before the synchronous field-effect start, then selecting only a slot that transitions from unused to used.

The fix keeps existing one-shot `FLDEFF_SPARKLE` rendering but moves scheduling into a Viridian-Forest-only task:

- wait for `CB2_Overworld`, inactive palette fade, and a live player sprite;
- validate the exact hidden-item BG event before every candidate start;
- require the coordinate to be fully inside the current display;
- check the matching hidden-item flag before every start and while a pilot sprite is active;
- repeat on a 90-frame interval while visible and uncollected;
- own at most one marked pilot sparkle sprite at once;
- stop the owned sprite immediately after its flag is set;
- destroy the owned sprite and task on map change;
- re-establish the task from transition and resume hooks after overworld task resets.

`FLDEFF_REPEATING_SPARKLES` is not used. Its source shows a looping sprite with explicit DexNav ownership/cleanup, not built-in lifecycle semantics for two positions and two hidden-item flags. Field-effect active-list source also permits duplicate IDs while removing one matching entry at a time, so the pilot deliberately serializes one-shot sparkle ownership.

Source verification for the linker follow-up:

- `FieldEffectStart` runs the selected field-effect script synchronously to completion.
- CFRU `FldEff_Sparkle` invokes exactly one `CreateSpriteAtEnd`.
- `UpdateSparkleFieldEffect` uses `data[0]` and `data[1]`; `data[7]` remains available for the pilot ownership marker.
- A full sprite table prevents the start.
- If no slot transitions to `inUse`, the new `FLDEFF_SPARKLE` active-list entry is removed and the start returns failure without recording sprite ownership.

## Pilot inventory

| Map | Hidden item | Coordinate | Elevation | Flag/state | Quantity | Underfoot | Candidate marker |
|---|---|---:|---:|---|---:|---|---|
| `MAP_VIRIDIAN_FOREST` | `ITEM_POTION` | `(3, 22)` | `3` | `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_POTION`; offset `0` | `1` | `false` | visible-range one-shot sparkle, repeated every 90 frames |
| `MAP_VIRIDIAN_FOREST` | `ITEM_ANTIDOTE` | `(28, 57)` | `0` | `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_ANTIDOTE`; offset `1` | `1` | `false` | visible-range one-shot sparkle, repeated every 90 frames |

## Manual smoke matrix

Clean build before smoke from the CFRU root:

```sh
python3 scripts/clean.py BUILD
python3 scripts/make.py
```

| Case | Setup | Expected result | Result |
|---|---|---|---|
| Fresh entry/readiness | enter Viridian Forest from outside with both flags unset | no load/fade artifact; normal overworld appears | not run |
| Potion approach | walk to `(3, 22)` without using Itemfinder | clear sparkle begins when the tile enters the visible area and repeats while nearby | not run |
| Potion duplicate guard | remain near `(3, 22)` through several intervals | one controlled sparkle sequence at a time; no accumulating identical sprites | not run |
| Potion pickup/flag stop | pick up Potion normally, then remain nearby | normal grant/text flow; no new Potion sparkle after the flag is set | not run |
| Antidote approach | walk to `(28, 57)` with its flag unset | clear sparkle begins on approach and repeats while nearby | not run |
| Antidote pickup/flag stop | pick up Antidote normally, then remain nearby | normal grant/text flow; no new Antidote sparkle after the flag is set | not run |
| One collected / one unset | re-enter with Potion collected and Antidote unset | no Potion sparkle; Antidote still repeats on approach | not run |
| Both collected | re-enter with both flags set | neither pilot position sparkles | not run |
| Map-change cleanup | leave Viridian Forest while a pilot sparkle is visible | no sparkle or pilot-task symptom on the destination map | not run |
| Resume behavior | return from a menu/battle or re-enter the forest with one flag unset | remaining marker scheduling resumes after overworld readiness | not run |
| Existing map behavior | test signs, trainers, exits and visible item balls | unchanged | not run |
| Itemfinder non-scope | optionally use Itemfinder near each pilot | existing behavior remains unchanged; pilot does not depend on Itemfinder | not run |

## Automated/source checks

- CFRU `git diff --check`: pass.
- CFRU syntax-only compile of `src/overworld.c`: pass.
- `rg -n "gFieldEffectObjectTemplatePointers|FLDEFFOBJ_SMALL_SPARKLE" src/overworld.c`: no matches.
- Workspace `git diff --check`: pass.
- Prior complete local CFRU clean build: user-reported linker fail on undefined `gFieldEffectObjectTemplatePointers`.
- Clean CFRU rebuild on follow-up commit `05b4231d847a1aa71d53f846b818403e887f4d3f`: pending user run; not run by Codex because `scripts/make.py` reads/modifies the local ROM and repository rules prohibit Codex from reading or modifying ROM files.
- Runtime smoke: not run.

## Acceptance boundary

Do not promote beyond `FIX_CANDIDATE_PENDING_LOCAL_REBUILD` until the new complete clean build links successfully. After that, all core approach, repeat, duplicate-guard, post-pickup and map-cleanup rows still require manual smoke. Even after a pass, this remains a two-item Viridian Forest pilot, not evidence for a global rollout, underfoot/renewable hidden items, full playthrough, BizHawk, Ironmon Tracker or P1 support.
