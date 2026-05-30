# CFRU hidden item sparkle QoL smoke handoff

Status: design-only smoke protocol for branch `design/cfru-hidden-item-sparkle-qol`.

No implementation was made in this block. No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, private path, token, secret, `.env`, binary patch, raw address port, Itemfinder feature, Field Item randomizer writer, or itemball graphics change is included.

## Current result

Decision: `implementable-medium`.

Recommended pilot: Viridian Forest, map bank `1`, map number `0`.

Recommended first visible behavior: a source-backed CFRU helper that scans current-map hidden-item BG events on map transition and spawns one-shot `FLDEFF_SPARKLE` cues only for hidden items whose flags are unset.

Permanent sparkle behavior should wait for owned marker lifetime and cleanup infrastructure, likely using `FLDEFF_REPEATING_SPARKLES` only after sprite/effect tracking and post-pickup cleanup are explicit.

## Pilot inventory

| Map | Hidden item | Coordinate | Elevation | Flag/state | Quantity | Underfoot | Marker |
|---|---|---:|---:|---|---:|---|---|
| `MAP_VIRIDIAN_FOREST` | `ITEM_POTION` | `(3, 22)` | `3` | `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_POTION`; CFRU offset `0` | `1` | `false` | one-shot `FLDEFF_SPARKLE` |
| `MAP_VIRIDIAN_FOREST` | `ITEM_ANTIDOTE` | `(28, 57)` | `0` | `FLAG_HIDDEN_ITEM_VIRIDIAN_FOREST_ANTIDOTE`; CFRU offset `1` | `1` | `false` | one-shot `FLDEFF_SPARKLE` |

## Future smoke matrix

| Case | Setup | Expected result |
|---|---|---|
| Map entry, both hidden items uncollected | enter Viridian Forest from outside with both hidden-item flags unset | sparkle cues appear at both hidden-item coordinates |
| Normal hidden pickup still works | press A facing the Potion hidden-item spot | item grants once through existing hidden-item pickup flow; hidden-item flag is set |
| Flag-gated re-entry after one pickup | leave and re-enter Viridian Forest after picking up Potion only | Potion cue is absent; Antidote cue remains |
| Flag-gated re-entry after both pickups | pick up both hidden items, leave and re-enter | no hidden-item sparkle cues appear |
| Existing map behavior | interact with signs, trainers, visible item balls, and exits | behavior remains unchanged |
| Randomizer ownership | use an output generated with existing UPR-FVX Field Items behavior, if later requested | hidden marker follows coordinate/flag slot only; no writer, TM slot, shop, Pickup, static/gift/NPC item-source behavior changes |
| Itemfinder non-scope | use Itemfinder near the pilot items, if later tested | vanilla/CFRU Itemfinder behavior remains unchanged; sparkle QoL does not depend on Itemfinder |

## Checks for a later implementation branch

- `git status --short`
- CFRU source diff review limited to the hidden-item sparkle helper and optional feature flag
- no CFRU/DPE/UPR-FVX submodule movement unless explicitly requested
- no ROM/build/save/log artifact staged
- one clean CFRU build
- one sanitized manual Viridian Forest smoke
- `git diff --check`

## Caveats

- This protocol does not prove full-playthrough compatibility.
- This protocol does not prove BizHawk or Ironmon Tracker compatibility.
- This protocol does not cover underfoot hidden items.
- This protocol does not cover renewable hidden-item reset behavior.
- This protocol does not cover every map with many hidden items.
- Permanent markers require additional cleanup proof beyond this one-shot sparkle MVP.
