# CFRU Pokecenter map object ownership smoke handoff

Status: `DESIGN_ONLY_NO_CODE`

## Purpose

This smoke handoff gates a future implementation that adds a source-backed map
object ownership layer for extra Pokecenter NPCs.

No runtime smoke was run in this design block. No CFRU, DPE, UPR-FVX, ROM,
binary patch, save, emulator state, build, tool binary, screenshot, raw log,
private path, token, secret or `.env` data is included.

## Design result

Decision: `implementable-medium`.

Recommended path: add a CFRU-owned map-object overlay/generator that derives
the target map header by map bank and map number, copies existing object-event
templates from the source ROM during insertion, appends source-defined extra
objects, emits a replacement object table and replacement `MapEvents`, preserves
original warp/coord/bg pointers, then repoints `MapHeader.events`.

Rejected for implementation:

- in-place object table extension;
- fixed raw-address object table replacement;
- existing-NPC replacement as the rollout model;
- full copied pret map source files.

## Viridian pilot acceptance gate

Target map:

- `MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F`
- map bank `5`, map number `4`

Expected before state:

- object count `4`
- original Gentleman remains at `(12, 5)` with original dialogue

Expected pilot addition:

- new zero-based object table row `4`
- new local id `5`
- sprite `MAP_OBJ_GFX_GENTLEMAN`
- candidate coordinate `(10, 5)`
- elevation `3`
- movement `MOVEMENT_TYPE_FACE_DOWN`
- script `EventScript_PokeCenterNameRater`

## Manual smoke proposal

Run after the future implementation creates a playable local candidate:

1. Enter Viridian City Pokecenter 1F.
2. Confirm object count increase is represented by the new NPC, not by
   replacing any existing NPC.
3. Talk to the original Gentleman at `(12, 5)` and confirm his original
   dialogue remains.
4. Talk to the Boy and Youngster and confirm their original dialogue remains.
5. Confirm the Nurse still heals normally.
6. Confirm PC access still opens normally.
7. Confirm all four warps still work as before, including the upstairs warp.
8. Talk to the added Name Rater NPC.
9. Choose `No` at the intro and confirm clean script exit.
10. Choose `Yes`, select an eligible player-owned non-Egg party mon, and
    confirm the nickname screen opens.
11. Cancel from nickname entry and confirm field control returns.
12. Enter a changed nickname and confirm the new nickname is applied.
13. If available, select an Egg and confirm the rejection path.
14. If available, select a traded/non-player-OT mon and confirm the rejection
    path.
15. Leave and re-enter the Pokecenter and confirm the added NPC respawns once,
    with no duplicate object.
16. Confirm no Runtime Options, Field Items, hidden-item cues, itemball graphics
    or randomizer-output behavior changed.

## Rollout gate after Viridian

Before adding more Pokecenters:

- document each target map bank and map number;
- document original object count;
- document new local id and zero-based table row;
- verify no local-id collision;
- verify object count remains below runtime active object limits;
- for maps with coord/bg events, confirm those event pointers are preserved.

The first non-Viridian rollout smoke should include at least one high-count
Pokecenter and one map with coord/bg events, with One Island treated as a
special preservation case.

## Caveats

- Candidate Viridian coordinate `(10, 5)` is not collision-proven by this
  design block.
- The future generator/inserter must fail closed if the current object count or
  expected original table shape does not match the reviewed source expectation.
