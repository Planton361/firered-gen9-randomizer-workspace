# CFRU hidden item sparkle QoL smoke handoff

Status: Viridian Forest pilot implemented in CFRU branch `feature/cfru-hidden-item-sparkle-pilot`; pending manual smoke.

No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, private path, token, secret, `.env`, binary patch, raw address port, Itemfinder feature, Field Item randomizer writer, or itemball graphics change is included.

## Current result

Decision: `IMPLEMENTED_PILOT_PENDING_MANUAL_SMOKE`.

Implemented pilot: Viridian Forest, map bank `1`, map number `0`.

Visible behavior: a source-backed CFRU helper scans current-map hidden-item BG events on map transition and spawns one-shot `FLDEFF_SPARKLE` cues only for the two pilot hidden-item coordinates while their hidden-item flags are unset.

Permanent sparkle behavior remains out of scope and should wait for owned marker lifetime and cleanup infrastructure, likely using `FLDEFF_REPEATING_SPARKLES` only after sprite/effect tracking and post-pickup cleanup are explicit.

## Source-backed implementation notes

- Hook: CFRU `RunOnTransitionMapScript`, after the map transition script tag runs.
- Scope guard: `MAP_IS(VIRIDIAN_FOREST)` plus exact current-map BG-event matches for kind `7`, coordinate, elevation and hidden-item offset.
- Sparkle source: existing one-shot `FLDEFF_SPARKLE`; no repeating sparkle lifetime state is added.
- Flag gate: existing hidden-item flag state, using `FLAG_HIDDEN_ITEMS_START + offset`.
- Randomizer boundary: item id is not used for the pilot match, so the cue is tied to coordinate/hidden-item flag slot and does not require Field Item randomizer writer changes.
- Non-scope preserved by design: hidden-item pickup, Itemfinder, visible item balls, Pickup, trainers, warps and other maps.

## Pilot inventory

| Map | Hidden item | Coordinate | Elevation | Flag/state | Quantity | Underfoot | Marker |
|---|---|---:|---:|---|---:|---|---|
| `MAP_VIRIDIAN_FOREST` | `ITEM_POTION` | `(3, 22)` | `3` | `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_POTION`; CFRU offset `0` | `1` | `false` | one-shot `FLDEFF_SPARKLE` |
| `MAP_VIRIDIAN_FOREST` | `ITEM_ANTIDOTE` | `(28, 57)` | `0` | `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_ANTIDOTE`; CFRU offset `1` | `1` | `false` | one-shot `FLDEFF_SPARKLE` |

## Manual smoke matrix

Clean build before smoke from the CFRU root:

```sh
python3 scripts/clean.py BUILD
python3 scripts/make.py
```

| Case | Setup | Expected result |
|---|---|---|
| Map entry, both hidden items uncollected | enter Viridian Forest from outside with both hidden-item flags unset | sparkle cues appear at both hidden-item coordinates |
| Normal hidden pickup still works | press A facing the Potion hidden-item spot | item grants once through existing hidden-item pickup flow; hidden-item flag is set |
| Flag-gated re-entry after one pickup | leave and re-enter Viridian Forest after picking up Potion only | Potion cue is absent; Antidote cue remains |
| Flag-gated re-entry after both pickups | pick up both hidden items, leave and re-enter | no hidden-item sparkle cues appear |
| Existing map behavior | interact with signs, trainers, visible item balls, and exits | behavior remains unchanged |
| Randomizer ownership | use an output generated with existing UPR-FVX Field Items behavior, if later requested | hidden marker follows coordinate/flag slot only; no writer, TM slot, shop, Pickup, static/gift/NPC item-source behavior changes |
| Itemfinder non-scope | use Itemfinder near the pilot items, if later tested | vanilla/CFRU Itemfinder behavior remains unchanged; sparkle QoL does not depend on Itemfinder |

## Implementation checks run

- `git status --short`
- `git -C 02_external/CFRU-expansion status --short`
- CFRU source diff review limited to the hidden-item sparkle helper and transition hook
- no ROM/build/save/log artifact staged
- CFRU syntax-only check for `src/overworld.c`
- no clean CFRU build run in this block; build and runtime smoke are manual handoff
- `git diff --check`

## Caveats

- This protocol does not prove full-playthrough compatibility.
- This protocol does not prove BizHawk or Ironmon Tracker compatibility.
- This protocol does not cover underfoot hidden items.
- This protocol does not cover renewable hidden-item reset behavior.
- This protocol does not cover every map with many hidden items.
- Permanent markers require additional cleanup proof beyond this one-shot sparkle MVP.
