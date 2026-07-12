# CFRU hidden item sparkle QoL smoke handoff

Status: `SMALL_VISUAL_FIX_PENDING_MANUAL_SMOKE` on CFRU branch `fix/cfru-hidden-item-sparkle-small-visual`, commit `d77da7fdb6c1ceeb946615bb2b31dcd2bbcf9ddd`, Draft PR `https://github.com/Planton361/CFRU-expansion/pull/31`.

Base: current `compat/firered-gen9-randomizer` commit `325212e325023284bd6198a3a9cd75b60e0c21f8`, including linker fix `05b4231d847a1aa71d53f846b818403e887f4d3f`.

No pass result is documented. No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, private path, token, secret, `.env`, binary patch, raw address port, Itemfinder feature, Field Item randomizer writer, visible itemball graphics, other map or DPE change is included.

## Root cause and fix candidate

The failed smoke is consistent with the prior lifecycle: `RunOnTransitionMapScript` started one-shot `FLDEFF_SPARKLE` effects before `InitMap`, once for each distant Viridian Forest coordinate. A one-shot effect is camera-relative and finite, so an off-screen map-entry sparkle ends before the player reaches its tile.

The first task-based fix candidate then failed the user's complete local clean build at link time with undefined reference to `gFieldEffectObjectTemplatePointers`. Its syntax-only compile could not expose that missing linkable definition. The follow-up removes the direct template-table dependency and identifies the new sparkle by snapshotting all sprite `inUse` states before the synchronous field-effect start, then selecting only a slot that transitions from unused to used.

The linker-fixed pilot is now user-confirmed visible and repeating, but its general CFRU `FLDEFF_SPARKLE` visual is too large and bright, producing a strong cross-star. The small-visual candidate replaces only this pilot asset with a local Cyan-derived 16x16, two-frame sparkle and subtle palette.

The existing Viridian-Forest-only task still:

- wait for `CB2_Overworld`, inactive palette fade, and a live player sprite;
- validate the exact hidden-item BG event before every candidate start;
- require the coordinate to be fully inside the current display;
- check the matching hidden-item flag before every start and while a pilot sprite is active;
- repeat on a source-backed 16-frame interval while visible and uncollected;
- own at most one marked pilot sparkle sprite at once;
- stop the owned sprite immediately after its flag is set;
- destroy the owned sprite and task on map change;
- re-establish the task from transition and resume hooks after overworld task resets.

The visible pilot no longer uses `FLDEFF_SPARKLE` or `FLDEFF_REPEATING_SPARKLES`. A CFRU-owned local SpriteTemplate creates the compact sprite directly, so unrelated global Field Effects and the Field Effect active list remain untouched. Its 3/5/5 animation-end callback frees local sprite/palette resources; pickup and map-change cleanup use the same resource-free path.

## Cyan small-sparkle comparison

| Property | Prior CFRU pilot | Cyan reference / candidate |
|---|---|---|
| Visible asset | general `FLDEFF_SPARKLE`, strong bright cross-star | dedicated compact small sparkle |
| OAM | global/private asset behavior | local 16x16 OAM |
| Frames | global sparkle lifecycle | two frames |
| Animation | longer general effect | `3 / 5 / 5`, then destroy |
| Palette | bright general Field Effect palette | subtle white/cyan palette |
| Cooldown | 90 frames | 16 frames |
| Ownership | Field Effect active list plus tracked sprite | local SpriteTemplate/callback; no active-list entry |

Source verification for the linker follow-up:

- `FieldEffectStart` runs the selected field-effect script synchronously to completion.
- CFRU `FldEff_Sparkle` invokes exactly one `CreateSpriteAtEnd`.
- `UpdateSparkleFieldEffect` uses `data[0]` and `data[1]`; `data[7]` remains available for the pilot ownership marker.
- A full sprite table prevents the start.
- If no slot transitions to `inUse`, the new `FLDEFF_SPARKLE` active-list entry is removed and the start returns failure without recording sprite ownership.

## Pilot inventory

| Map | Hidden item | Coordinate | Elevation | Flag/state | Quantity | Underfoot | Candidate marker |
|---|---|---:|---:|---|---:|---|---|
| `MAP_VIRIDIAN_FOREST` | `ITEM_POTION` | `(3, 22)` | `3` | `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_POTION`; offset `0` | `1` | `false` | local 16x16 two-frame sparkle, cooldown 16 |
| `MAP_VIRIDIAN_FOREST` | `ITEM_ANTIDOTE` | `(28, 57)` | `0` | `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_ANTIDOTE`; offset `1` | `1` | `false` | local 16x16 two-frame sparkle, cooldown 16 |

## Manual smoke matrix

Clean build before smoke from the CFRU root:

```sh
python3 scripts/clean.py BUILD
python3 scripts/make.py
```

| Case | Setup | Expected result | Result |
|---|---|---|---|
| Fresh entry/readiness | enter Viridian Forest from outside with both flags unset | no load/fade artifact; normal overworld appears | not run |
| Potion visual/approach | walk to `(3, 22)` without using Itemfinder | compact, less bright 16x16 sparkle begins when visible and remains readable | not run |
| Potion duplicate guard | remain near `(3, 22)` through several intervals | one controlled sparkle sequence at a time; no accumulating identical sprites | not run |
| Potion pickup/flag stop | pick up Potion normally, then remain nearby | normal grant/text flow; no new Potion sparkle after the flag is set | not run |
| Antidote visual/approach | walk to `(28, 57)` with its flag unset | same compact, less bright sparkle begins on approach | not run |
| Antidote pickup/flag stop | pick up Antidote normally, then remain nearby | normal grant/text flow; no new Antidote sparkle after the flag is set | not run |
| One collected / one unset | re-enter with Potion collected and Antidote unset | no Potion sparkle; Antidote still repeats on approach | not run |
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
- Workspace `git diff --check`: pass.
- Prior complete local CFRU clean build: user-reported linker fail on undefined `gFieldEffectObjectTemplatePointers`.
- Clean CFRU ROM insertion build for the small-visual candidate: pending user run; not run by Codex because `scripts/make.py` reads/modifies the local ROM and repository rules prohibit Codex from reading or modifying ROM files.
- Runtime smoke: not run.

## Acceptance boundary

Do not promote beyond `SMALL_VISUAL_FIX_PENDING_MANUAL_SMOKE` until both pilot positions visibly use the compact, less bright sparkle and all repeat, duplicate-guard, post-pickup, map-cleanup and global-sparkle-regression rows pass. Even after a pass, this remains a two-item Viridian Forest pilot, not evidence for a global rollout, underfoot/renewable hidden items, full playthrough, BizHawk, Ironmon Tracker or P1 support.
