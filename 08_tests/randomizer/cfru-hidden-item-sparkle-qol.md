# CFRU hidden item sparkle QoL blocked handoff

Status: `BLOCKED_NEEDS_SOURCE_BACKED_OVERWORLD_FRAME_HOOK`.

CFRU Revert candidate: branch `revert/cfru-hidden-item-sparkle-pilot`, commit `acf1cf38a0acab1fd8a88be9b687e3b02faeb50b`, Draft PR `https://github.com/Planton361/CFRU-expansion/pull/33`.

Failed CFRU Draft PR #32 and failed Workspace Draft PR #461 are closed without merge. No pass is claimed.

## Sanitized failure record

- The original map-entry one-shot ended before the player reached the distant Viridian Forest item positions and was not visibly useful.
- Transition/resume task and Sprite-ownership variants could lose or starve the second Hidden Item.
- Stray Sparkles appeared at unrelated positions.
- A rejected private Small-Sprite/graphics/palette path caused player and NPC/OBJ palette corruption and possible environment tinting at runtime.
- The later simple-spawn task still produced a correct first Sparkle but did not make the second item reliable.

Screenshots, ROMs, Saves, Emulator States, Savestates, builds and raw logs remain local and are not committed. Savestates created by older ROM builds are not compatibility or acceptance evidence.

## Revert result

The CFRU Revert removes the complete pilot from `src/overworld.c`:

- Viridian Forest pilot constants, coordinates, data structure and table;
- transition and resume startup calls;
- pilot task and task cooldown/state;
- BG-event, visibility and readiness helpers;
- Sprite-slot discovery, ownership and marker state;
- manual `FieldEffectStop` and pilot active-list cleanup;
- all later simple-spawn pilot logic.

The cumulative pilot history added 186 lines to `src/overworld.c`. The Revert removes exactly those 186 lines, and the resulting file matches pre-pilot commit `9c105d156e219e7a59069f47d5ee49f1fdcfb6dc` exactly. Name-Rater rollout, map-object overlays and unrelated Compat behavior are preserved.

## Blocker

The source-faithful CyanSMP64/NatDex architecture calls its BG-event scan in the normal Overworld frame after `CameraUpdate`. CFRU does not expose a source-backed C extension point there: `OverworldBasic` and `CB2_OverworldBasic` are bound to Vanilla addresses in `BPRE.ld`, and the active slow-camera replacement is fixed byte replacement.

A future implementation requires an approved source-backed post-`CameraUpdate` hook and a proven camera-focus coordinate API. Raw addresses, byte replacement and a larger `OverworldBasic` port are not approved for this feature scope.

## Revert checks

- CFRU `git diff --check`: pass.
- Pilot-name and Potion/Antidote pilot-coordinate searches: no matches.
- Syntax-only compile of `src/overworld.c`: pass.
- `python3 scripts/build.py`: build and full link pass; existing RWX linker warning only.
- CFRU Git status after build: no ROM or build artifact.
- Runtime Hidden-Item-Sparkle smoke: not applicable because the marker is removed.

## Acceptance boundary

Accepting this Revert confirms only that the unstable pilot is absent and CFRU still builds/links. It does not implement a Hidden-Item marker, Itemfinder behavior, global rollout, private assets, DPE/UPR-FVX changes, BizHawk/Tracker support or P1 support.
