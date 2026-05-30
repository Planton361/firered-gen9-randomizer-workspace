# CFRU Name Rater Pokecenter pilot

Status: `IMPLEMENTED_VIRIDIAN_OVERLAY_MVP_NEEDS_MANUAL_SMOKE`

## Scope

This block implements the accepted Pilot target for the Name Rater Pokecenter
QoL: one additional Name Rater NPC in Viridian City Pokecenter 1F.

No existing Pokecenter NPC is replaced or repointed for this pilot. No global
Pokecenter rollout was added.

Out of scope and unchanged: Pewter City, other Pokecenters, Faster Intro,
Oak/Lab/Parcel, Bill-Sevii, Repel-Reuse, auto-run, poison, EXP, Runtime
Options, Hidden Items, Itemfinder sparkle, itemball graphics, Field Items,
UPR-FVX writer, DPE data, Viridian-Forest-Nurse, Step Item Guarantees,
Friendship Boost and binary patch work.

## Source-backed implementation

CFRU commit: `648ce6042a93b71796c2d478fc816687e2ec060a`

Changed CFRU files:

- `02_external/CFRU-expansion/scripts/insert.py`
- `02_external/CFRU-expansion/mapobjectoverlays`
- `02_external/CFRU-expansion/assembly/overworld_scripts/name_rater_pokecenter.s`
- `02_external/CFRU-expansion/strings/Scripts/name_rater_pokecenter.string`

The prior rejected model used `eventscripts` to repoint an existing Viridian
Pokecenter Gentleman object. That model remains rejected.

The new MVP adds a `mapobjectoverlays` insertion surface. During insertion it:

- derives the target map header from map bank and map number;
- reads the current `MapHeader.events`;
- requires the expected original object count to match;
- copies the existing object-event table from the current ROM candidate;
- appends one source-defined `EventObjectTemplate`;
- emits a replacement object table and replacement `MapEvents`;
- preserves the original warp, coord-event and bg-event counts and pointers;
- repoints only `MapHeader.events` for the target map to the generated
  replacement `MapEvents`.

This avoids fixed raw-address table ownership and avoids replacing any existing
object-event script pointer.

## Pilot map

Target map:

- `MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F`
- map bank `5`
- map number `4`

Expected original object count: `4`.

Existing object events preserved:

- row `0` / local id `1`: Nurse at `(7, 2)`
- row `1` / local id `2`: Gentleman at `(12, 5)`
- row `2` / local id `3`: Boy at `(4, 7)`
- row `3` / local id `4`: Youngster at `(2, 3)`

Added object event:

- new zero-based row: `4`
- new local id: `5`
- sprite: `MAP_OBJ_GFX_GENTLEMAN`
- coordinate: `(10, 5)`
- elevation: `3`
- movement: `MOVEMENT_TYPE_FACE_DOWN`
- movement range: `1, 1`
- trainer fields: `0, 0`
- script: `EventScript_PokeCenterNameRater`
- flags: `0, 0`

## Name Rater flow

The local script uses the existing vanilla-compatible Name Rater special ids:

- `ChoosePartyMon`
- `GetPartyMonSpecies`
- `BufferMonNickname`
- `IsMonOTIDNotPlayers`
- `IsMonOTNameNotPlayers`
- `ChangePokemonNickname`
- `NameRaterWasNicknameChanged`

The script supports:

- intro Yes/No;
- party selection cancel;
- Egg rejection;
- traded/non-player-OT rejection;
- nickname-screen cancel;
- changed-nickname confirmation.

## Manual smoke proposal

Run after creating a playable local candidate:

1. Enter Viridian City Pokecenter 1F.
2. Confirm the map loads without crash, freeze or visible event corruption.
3. Confirm the original Gentleman at `(12, 5)` still has his original dialogue.
4. Confirm the Boy and Youngster still have their original dialogue.
5. Confirm the Nurse still heals normally.
6. Confirm PC access still opens normally.
7. Confirm the upstairs and door warps still work as before.
8. Confirm the added Name Rater NPC is visible at `(10, 5)`.
9. Talk to the added Name Rater NPC and choose `No`; confirm clean script exit.
10. Talk again, choose `Yes`, select an eligible player-owned non-Egg party
    mon, and confirm the nickname screen opens.
11. Cancel from nickname entry and confirm field control returns.
12. Repeat, enter a changed nickname, and confirm the nickname is applied.
13. If available, select an Egg and confirm the rejection path.
14. If available, select a traded/non-player-OT mon and confirm the rejection
    path.
15. Leave and re-enter the Pokecenter and confirm the added NPC respawns once,
    with no duplicate object.
16. Confirm no Runtime Options, Field Items, hidden-item cues, itemball
    graphics or randomizer-output behavior changed.

## Checks

Local checks run:

- `python3 -m py_compile scripts/insert.py`
- `arm-none-eabi-as -o /dev/null overworld_scripts/name_rater_pokecenter.s`
- CFRU `git diff --cached --check`

Full CFRU build / ROM insertion was not run in this block because it would
touch local build/ROM artifacts. Manual runtime smoke remains required.

## Caveats

- The coordinate `(10, 5)` still needs gameplay collision and pathing smoke.
- The overlay generator has only one active manifest row in this MVP.
- This does not authorize a global Pokecenter rollout. Rollout should wait for
  a passed Viridian smoke and a separate design for high-count and coord/bg
  event Pokecenters.
- No ROM, save, emulator state, build artifact, tool binary, screenshot, raw
  log, hash, private path, token, secret or `.env` data is included.
