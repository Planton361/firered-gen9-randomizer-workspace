# CFRU hidden item sparkle QoL design

Status: documentation-only source-backed design for branch `design/cfru-hidden-item-sparkle-qol`.

No CFRU, DPE, UPR-FVX, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, private path, token, secret, `.env`, IPS/BPS/UPS patch, binary patch data, raw address port, Itemfinder feature, Field Item randomizer writer, or itemball graphics change is included.

## Scope

Goal: decide how hidden items could be made visible with sparkle-like presentation without building an Itemfinder feature and without porting Faster-FireRed binary patch data.

The desired behavior is a QoL marker for hidden items themselves:

- hidden item marker appears only for hidden-item BG events that are not collected;
- marker is driven by existing hidden-item flag/state where possible;
- pickup remains the existing hidden-item pickup path;
- UPR-FVX Field Items output remains untouched.

## Source set

Workspace docs read first:

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `01_docs/analysis/ironmon-qol-feature-inventory.md`
- `01_docs/analysis/cfru-qol-coverage.md`
- `01_docs/references/source-index.md`
- `01_docs/references/tool-manifest.md`

Local source reviewed read-only:

- CFRU: `02_external/CFRU-expansion/include/global.fieldmap.h`
- CFRU: `02_external/CFRU-expansion/include/constants/flags.h`
- CFRU: `02_external/CFRU-expansion/include/constants/field_effects.h`
- CFRU: `02_external/CFRU-expansion/assembly/overworld_scripts/system_scripts.s`
- CFRU: `02_external/CFRU-expansion/src/field_effects.c`
- CFRU: `02_external/CFRU-expansion/src/dexnav.c`
- CFRU: `02_external/CFRU-expansion/src/overworld.c`
- CFRU: `02_external/CFRU-expansion/scripts/insert.py`
- pret FireRed: `02_external/references/pret-pokefirered/include/global.fieldmap.h`
- pret FireRed: `02_external/references/pret-pokefirered/include/constants/event_bg.h`
- pret FireRed: `02_external/references/pret-pokefirered/include/constants/flags.h`
- pret FireRed: `02_external/references/pret-pokefirered/asm/macros/map.inc`
- pret FireRed: `02_external/references/pret-pokefirered/tools/mapjson/mapjson.cpp`
- pret FireRed: `02_external/references/pret-pokefirered/src/field_control_avatar.c`
- pret FireRed: `02_external/references/pret-pokefirered/src/itemfinder.c`
- pret FireRed: `02_external/references/pret-pokefirered/src/field_effect_helpers.c`
- pret FireRed: `02_external/references/pret-pokefirered/src/script.c`
- pret FireRed: `02_external/references/pret-pokefirered/data/scripts/obtain_item.inc`
- pret FireRed: `02_external/references/pret-pokefirered/data/scripts/itemfinder.inc`
- pret FireRed: `02_external/references/pret-pokefirered/data/maps/ViridianForest/map.json`
- pret FireRed: `02_external/references/pret-pokefirered/data/maps/ViridianForest/scripts.inc`

Public Faster-FireRed evidence checked only as documentation boundary:

- <https://github.com/DrMaple/Faster-FireRed>

## Faster-FireRed evidence boundary

Faster-FireRed publicly documents that hidden items are visually marked and also provides a variant without hidden item marks. The public repository surface reviewed here exposes README and patch artifact evidence, not a portable source implementation for how those marks are generated.

Decision boundary:

- Use Faster-FireRed only as feature inspiration.
- Do not port IPS/BPS/UPS/binary patch data.
- Do not port raw addresses.
- Do not infer exact marker implementation from patch files.
- Build any future implementation only from local CFRU/pret source surfaces.

## Hidden-item source finding

### CFRU current state

CFRU keeps the same core hidden-item shape visible in the decomp reference:

- `struct HiddenItemStruct` has `itemId`, `hiddenItemId`, `quantity`, and `isUnderfoot`.
- `union BgUnion` can hold a `hiddenItemStr` / packed hidden item data.
- `struct BgEvent` stores map coordinate, elevation, kind, and the BG union.
- `struct MapEvents` carries `bgEventCount` and `bgEvents`.

CFRU hidden-item flags are represented by `FLAG_HIDDEN_ITEMS_START`, a `FLAG_HIDDEN_ITEM(map, item)` macro, and per-hidden-item IDs such as `HIDDEN_ITEM_VIRIDIAN_FOREST_POTION` and `HIDDEN_ITEM_VIRIDIAN_FOREST_ANTIDOTE`.

CFRU already changes hidden-item pickup presentation:

- `SystemScript_PickedUpHiddenItem` calls `ShowItemSpriteOnFindHidden`.
- It then uses the existing hidden-item pickup messages, clears the shown item sprite, calls `SetHiddenItemFlag`, and increments `GAME_STAT_FOUND_HIDDEN_ITEM`.
- This is pickup presentation only. It does not create always-visible map markers before pickup.

CFRU already has usable sparkle field-effect source:

- `FLDEFF_SPARKLE` exists.
- `FLDEFF_REPEATING_SPARKLES` exists as a CFRU-added field effect.
- `FldEff_Sparkle` starts a small sparkle at field-effect arguments `x/y` and priority.
- `FldEff_Sparkles` starts a repeating sparkle sprite and tags it as `FLDEFF_REPEATING_SPARKLES`.
- DexNav uses `FLDEFF_REPEATING_SPARKLES` as an overworld marker and explicitly removes its active field effect during cleanup.

CFRU has a source-visible map-transition path:

- `RunOnTransitionMapScript` already runs CFRU transition work and then map script tag `3`.
- A future source-backed helper could scan `gMapHeader.events->bgEvents` during this transition path.
- No existing hidden-item sparkle scan/helper was found.

CFRU map-object overlay infrastructure exists, but it is not the first choice here:

- `scripts/insert.py` can append object-event templates, emit a replacement `MapEvents`, preserve original warp/coord/bg pointers, and repoint `MapHeader.events`.
- This is useful for object-event fallbacks, but it increases object counts and is heavier than a field-effect marker.

CFRU Itemfinder state:

- `ITEM_ITEMFINDER`, item table references, and a vanilla long-call field-use function are present.
- No CFRU-owned source implementation of an Itemfinder sparkle marker was found.
- This task explicitly excludes Itemfinder changes, so the Itemfinder path is reference-only.

### pret FireRed vanilla reference

pret FireRed confirms hidden items are BG events, not object events:

- `map.json` entries with `"type": "hidden_item"` are generated by `tools/mapjson/mapjson.cpp` into `bg_hidden_item_event`.
- `bg_hidden_item_event` packs item, hidden-item flag offset, quantity, and underfoot state.
- `BG_EVENT_HIDDEN_ITEM` identifies the BG-event kind.
- `field_control_avatar.c` checks hidden-item BG events when the player interacts, rejects nonmatching underfoot cases, fills script vars with item/flag/quantity, checks `FlagGet`, and returns the hidden-item pickup script only when the flag is unset.
- `obtain_item.inc` grants the item/coins and calls `SetHiddenItemFlag`.

pret Itemfinder confirms a useful scan model but is out of scope for behavior:

- `itemfinder.c` scans `gMapHeader.events->bgEvents`.
- It ignores already-collected hidden items with `FlagGet`.
- It scans connected maps for nearby normal hidden items.
- Underfoot items get a different flow that can dig up the item.
- Its arrows/stars are Itemfinder UI behavior, not the requested no-Itemfinder always-visible marker.

pret field effects confirm `FLDEFF_SPARKLE` behavior:

- `FldEff_Sparkle` uses field-effect args for map coordinates and creates a small sparkle sprite.
- Its update path stops the sparkle after the animation/lifetime.
- Stock `FLDEFF_SPARKLE` is therefore a one-shot cue, not a persistent marker by itself.

## Strategies without Itemfinder

| Strategy | Raw addresses needed? | Works without Itemfinder? | Can disappear after pickup? | Touches Randomizer Field Item output? | MapEvents/Object-count risk | Performance / overworld-sprite risk | Smoke-testable? | Decision |
|---|---:|---:|---:|---:|---|---|---:|---|
| Map-load one-shot `FLDEFF_SPARKLE` for every uncollected hidden item on the current map | no | yes | yes on next map load; immediate disappearance is not relevant because the effect ends itself | no | none if implemented as a runtime scan of existing BG events | low/medium; burst cost scales with hidden-item count on map entry | yes | implementable-small for cue-only MVP |
| Runtime field-effect marker on each uncollected hidden-item coordinate, preferably `FLDEFF_REPEATING_SPARKLES` with owned cleanup | no | yes | yes if helper tracks marker sprites/effects and removes or suppresses them after `SetHiddenItemFlag`; unclear without new cleanup | no | none if only scanning existing BG events | medium; persistent sprites can consume sprite slots on hidden-item-heavy maps | yes | implementable-medium |
| Invisible/neutral object-event marker per hidden item, appended by map-object overlay and hidden by the same hidden-item flag | no, if using source overlay infrastructure | yes | likely yes if object hide flag uses the collected hidden-item flag; exact local-id and object flag behavior must be proven | no | medium/high; object counts, local ids, collision/invisibility, and per-map append rows matter | medium/high; every marker is an object-event candidate | yes | fallback only |
| Itemfinder response sparkle/arrow extension | no for source design, but not in scope | no; it depends on Itemfinder use | yes | no | none | low/medium | yes | reject for this task |
| Faster-FireRed patch port | yes or binary patch data | unknown | unknown | unknown | unknown | unknown | no in this workspace | reject |
| UPR-FVX Field Item writer change | no, but wrong owner | yes | unclear | yes | none in CFRU | n/a | yes | reject |

## Recommended design

Result decision: `implementable-medium`.

Recommended first implementation later:

1. Add a CFRU-owned helper that scans `gMapHeader.events->bgEvents` on map transition.
2. For each `BG_EVENT_HIDDEN_ITEM`, decode item/flag/quantity/underfoot using the existing hidden-item structure.
3. Skip the marker when the hidden-item flag is already set.
4. For a low-risk MVP, spawn a one-shot `FLDEFF_SPARKLE` at the hidden-item coordinate on map entry.
5. If permanent markers are required, promote to owned repeating sparkle infrastructure that tracks sprite/effect ids and cleans them up on map exit and after pickup.

Why not object events first:

- Hidden items are already BG events.
- Field effects can mark coordinates without changing `MapEvents` object counts.
- The existing object-overlay path is heavier and should be reserved for cases where field effects cannot persist or cleanly layer.

Why not Itemfinder:

- The user requested no Itemfinder feature.
- Vanilla Itemfinder scan logic is useful proof that hidden items can be found by iterating BG events and flags, but the visible marker should not depend on using the Itemfinder item.

## Pilot map

Pilot: Viridian Forest.

Reason:

- Early, familiar map.
- Only two hidden items.
- No coord events in the pret source map.
- Existing BG events are signs plus two hidden items.
- CFRU map constant identifies it as map bank `1`, map number `0`.

Source-backed pilot inventory:

| Field | Value |
|---|---|
| Map name | `ViridianForest` / `MAP_VIRIDIAN_FOREST` |
| Map bank / map number | bank `1`, map `0` |
| Object events / warps / coord events / BG events in pret source | `11` / `0` / `0` / `8` |
| Hidden item 1 | coord `(3, 22)`, elevation `3`, `ITEM_POTION`, `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_POTION`, CFRU hidden-item id `HIDDEN_ITEM_VIRIDIAN_FOREST_POTION` / offset `0`, quantity `1`, underfoot `false` |
| Hidden item 2 | coord `(28, 57)`, elevation `0`, `ITEM_ANTIDOTE`, `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_ANTIDOTE`, CFRU hidden-item id `HIDDEN_ITEM_VIRIDIAN_FOREST_ANTIDOTE` / offset `1`, quantity `1`, underfoot `false` |
| Proposed marker source | `FLDEFF_SPARKLE` for first one-shot MVP; later `FLDEFF_REPEATING_SPARKLES` only with owned cleanup |
| Expected before pickup | entering map with both flags unset creates sparkle cues at both hidden-item coordinates |
| Expected after picking up Potion | Potion flag set; re-entering the map creates only the Antidote cue |
| Expected after picking up both | both flags set; re-entering creates no hidden-item cue |

Smoke proposal:

1. Build a later implementation from CFRU source only.
2. Enter Viridian Forest from an adjacent map with both hidden-item flags unset.
3. Confirm sparkles appear at the Potion and Antidote coordinates.
4. Pick up the Potion through normal hidden-item interaction.
5. Leave and re-enter Viridian Forest.
6. Confirm Potion sparkle is gone and Antidote sparkle remains.
7. Pick up Antidote, leave and re-enter again.
8. Confirm no hidden-item sparkles remain.
9. Confirm regular visible item balls, trainers, signs, warps, and hidden-item pickup messages still behave normally.
10. Confirm no Field Items randomizer output, TM/non-TM slot typing, shops, Pickup, static/gift/NPC item source, or Itemfinder behavior changed.

## Risks and caveats

- `FLDEFF_SPARKLE` is one-shot. It is safe-looking for a cue but not a permanent marker.
- `FLDEFF_REPEATING_SPARKLES` needs owned lifetime management. DexNav proves cleanup is possible, but hidden-item cleanup must be its own helper.
- Immediate disappearance after pickup requires either pickup-script integration, a flag-aware update loop, or map re-entry. The map-load one-shot MVP avoids this by not being persistent.
- Underfoot hidden items need special handling. Vanilla non-Itemfinder interaction rejects underfoot items, while Itemfinder can dig them up. A no-Itemfinder marker can still show them, but pickup behavior should not change.
- Connected-map scanning belongs to Itemfinder behavior. Always-visible map markers should probably mark only the current loaded map unless future design explicitly chooses otherwise.
- Object-event fallback risks object-count growth, local-id conflicts, collision/invisibility mistakes, and map-overlay maintenance.
- Hidden-item randomization is not changed here. If UPR-FVX changes hidden-item item IDs, a coordinate/flag marker still marks the slot, not the randomized item identity.

## Handoff

Recommended future implementation branch: `feature/cfru-hidden-item-sparkle-qol`.

First implementation should stay Viridian-Forest-only or globally gated by a compile-time/runtime feature flag. If globally gated, still use Viridian Forest as the first smoke map before broader maps.

Acceptance gate before broader rollout:

- no raw address or patch data;
- no Itemfinder dependency;
- no randomizer writer changes;
- no object-event overlay unless field-effect strategy is rejected by implementation evidence;
- one clean local build;
- one sanitized Viridian Forest manual smoke;
- one follow-up smoke on a map with more hidden items only after Viridian passes.
