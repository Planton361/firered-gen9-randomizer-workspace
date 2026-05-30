# CFRU Name Rater Pokecenter rollout design

Status: `DESIGN_ONLY_ROLLOUT_PLAN`

Branch: `design/cfru-name-rater-centers-rollout`

## Scope

This is a design-only rollout plan for adding uniform Name Rater NPCs to
Pokecenter 1F maps after the Viridian overlay MVP passed manual smoke with
caveats.

No CFRU, DPE, UPR-FVX, rollout code, ROM, binary patch, build artifact, save,
emulator state, screenshot, raw log, private path, token, secret or `.env` data
was read, changed or documented.

## Source basis

Reviewed source surfaces:

- `02_external/CFRU-expansion/include/constants/maps.h`
- `02_external/references/pret-pokefirered/data/maps/map_groups.json`
- `02_external/references/pret-pokefirered/data/maps/*PokemonCenter_1F/map.json`
- `01_docs/analysis/cfru-pokecenter-map-object-ownership.md`
- `08_tests/randomizer/cfru-pokecenter-map-object-ownership.md`
- `08_tests/randomizer/cfru-name-rater-centers-qol.md`

The Viridian MVP is the confirmed pattern:

- target map: `MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F`
- map bank `5`, map number `4`
- original object count `4`
- appended row `4`, local id `5`
- sprite `MAP_OBJ_GFX_GENTLEMAN`
- coordinate `(10, 5)`
- elevation `3`
- movement `MOVEMENT_TYPE_FACE_DOWN`
- script `EventScript_PokeCenterNameRater`
- status `MVP_PASS_WITH_CAVEATS`

The smoke caveat is important: the NPC became visible only after a clean CFRU
build using `python3 scripts/clean.py BUILD` followed by `python3 scripts/make.py`,
and after entering the map fresh from outside.

## Common rollout row

For each additional Pokecenter, keep the overlay row mechanically uniform:

- new zero-based row: current object count
- new local id: current object count + 1
- sprite: `MAP_OBJ_GFX_GENTLEMAN`
- elevation: `3`
- movement: `MOVEMENT_TYPE_FACE_DOWN`
- movement range: `1, 1`
- trainer fields: `0, 0`
- script: `EventScript_PokeCenterNameRater`
- flags: `0, 0`

Coordinates below are design candidates based on reviewed object and warp
coordinates. They are not implementation proof. Every rollout map still needs
a clean-build and fresh-entry smoke before promotion.

## Target inventory

| Phase | Map | Bank | Map | Existing object count | New row | New local id | Candidate coordinate | Sprite | Movement | Elevation | Script | Warp / coord / BG risk | Overlay possible | Smoke focus |
|---|---|---:|---:|---:|---:|---:|---|---|---|---:|---|---|---|---|
| 0 done | `ViridianCity_PokemonCenter_1F` | 5 | 4 | 4 | 4 | 5 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events | confirmed by MVP | preserve original NPCs, Nurse, PC, warps, Name Rater No/Cancel/Confirm |
| 1 safe Kanto | `CeladonCity_PokemonCenter_1F` | 10 | 12 | 4 | 4 | 5 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events | yes, low risk | standard Pokecenter plus existing NPC dialogue |
| 1 safe Kanto | `FuchsiaCity_PokemonCenter_1F` | 11 | 5 | 4 | 4 | 5 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events | yes, low risk | standard Pokecenter plus existing NPC dialogue |
| 1 safe Kanto | `LavenderTown_PokemonCenter_1F` | 8 | 0 | 5 | 5 | 6 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events | yes, low risk | standard Pokecenter plus five existing objects |
| 1 safe Kanto | `Route10_PokemonCenter_1F` | 21 | 0 | 5 | 5 | 6 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events | yes, low risk | standard Pokecenter plus Aide script remains intact |
| 1 safe Kanto | `Route4_PokemonCenter_1F` | 16 | 0 | 6 | 6 | 7 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events | yes, low/moderate risk | Magikarp salesman and newspaper object remain intact |
| 1 safe Kanto | `SaffronCity_PokemonCenter_1F` | 14 | 6 | 6 | 6 | 7 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events | yes, low/moderate risk | Pokemon Journal invisible objects remain intact |
| 2 high-count Kanto | `CeruleanCity_PokemonCenter_1F` | 7 | 3 | 7 | 7 | 8 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events, 2 invisible journal objects | yes, but high-count smoke needed | confirm seven originals plus added NPC and journal objects |
| 2 high-count Kanto | `CinnabarIsland_PokemonCenter_1F` | 12 | 5 | 7 | 7 | 8 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events, Bill object present | yes, but story/NPC smoke needed | confirm Bill-related NPC state is not disturbed |
| 2 high-count Kanto | `PewterCity_PokemonCenter_1F` | 6 | 5 | 7 | 7 | 8 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events, wireless-club NPCs | yes, but high-count smoke needed | Jigglypuff, GBA kids, Mystery Event Club woman |
| 2 high-count Kanto | `VermilionCity_PokemonCenter_1F` | 9 | 1 | 7 | 7 | 8 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 4 warps, no coord/BG events, journal invisible objects | yes, but high-count smoke needed | VS Seeker woman and journal objects remain intact |
| 3 special layout | `IndigoPlateau_PokemonCenter_1F` | 13 | 0 | 8 | 8 | 9 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 3 warps, no coord/BG events, different larger layout | yes, but special-layout smoke needed | clerk, League room warp, nurse, PC, door guard |
| 4 Sevii later | `TwoIsland_PokemonCenter_1F` | 33 | 2 | 3 | 3 | 4 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 2 warps, no coord/BG events, Sevii map | yes, but defer | standard Pokecenter plus Sevii travel state |
| 4 Sevii later | `ThreeIsland_PokemonCenter_1F` | 34 | 1 | 4 | 4 | 5 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 2 warps, no coord/BG events, Sevii map | yes, but defer | standard Pokecenter plus local NPC scripts |
| 4 Sevii later | `FiveIsland_PokemonCenter_1F` | 36 | 0 | 5 | 5 | 6 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 2 warps, no coord/BG events, Sevii map | yes, but defer | standard Pokecenter plus journal invisible objects |
| 4 Sevii later | `SixIsland_PokemonCenter_1F` | 37 | 0 | 4 | 4 | 5 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 2 warps, no coord/BG events, Sevii map, Blue object has null script | yes, but defer | Blue object state, local NPCs, standard services |
| 4 Sevii later | `SevenIsland_PokemonCenter_1F` | 31 | 3 | 6 | 6 | 7 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 2 warps, no coord/BG events, Sevii map, journal invisible objects | yes, but defer | local NPCs plus journal objects |
| 5 coord/BG Sevii | `FourIsland_PokemonCenter_1F` | 35 | 1 | 4 | 4 | 5 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 2 warps, 0 coord events, 2 BG events | yes, but BG preservation smoke required | Pokemon Journal BG signs plus standard services |
| 5 coord/BG Sevii | `OneIsland_PokemonCenter_1F` | 32 | 0 | 6 | 6 | 7 | `(10, 5)` | `MAP_OBJ_GFX_GENTLEMAN` | `MOVEMENT_TYPE_FACE_DOWN` | 3 | `EventScript_PokeCenterNameRater` | 2 warps, 4 coord events, 9 BG events, Bill/Celio/Network Machine | yes, but highest risk | Bill/Celio, leave-island triggers, Network Machine BG events |

## Risk groups

Safe first candidates:

- `CeladonCity_PokemonCenter_1F`
- `FuchsiaCity_PokemonCenter_1F`
- `LavenderTown_PokemonCenter_1F`
- `Route10_PokemonCenter_1F`
- `Route4_PokemonCenter_1F`
- `SaffronCity_PokemonCenter_1F`

These maps use the same general Pokecenter 1F pattern, have no coord/BG
events, and do not touch Sevii story state. Route 4 and Saffron should still be
treated as moderate because they have six existing objects.

High-count or special Kanto candidates:

- `CeruleanCity_PokemonCenter_1F`
- `CinnabarIsland_PokemonCenter_1F`
- `PewterCity_PokemonCenter_1F`
- `VermilionCity_PokemonCenter_1F`
- `IndigoPlateau_PokemonCenter_1F`

These should be smoke-gated separately because object counts are seven or
eight, some include invisible Pokemon Journal objects, and Indigo Plateau uses
a different larger interior layout.

Risky or later Sevii candidates:

- `TwoIsland_PokemonCenter_1F`
- `ThreeIsland_PokemonCenter_1F`
- `FiveIsland_PokemonCenter_1F`
- `SixIsland_PokemonCenter_1F`
- `SevenIsland_PokemonCenter_1F`
- `FourIsland_PokemonCenter_1F`
- `OneIsland_PokemonCenter_1F`

The Sevii group should not be bundled into the first rollout. Four Island has
BG events. One Island is the special preservation case because it has Bill,
Celio, Network Machine BG events, and four leave-island coord triggers.

## Recommendation

Decision: `design-needed-before-rollout-code`.

The overlay system appears source-backed enough for map-by-map rollout rows,
but the next implementation should not be global. Use staged rollout:

1. Add a small safe Kanto batch only after this design is reviewed.
2. Run a clean-build smoke after the batch, entering each map from outside.
3. Add one high-count Kanto map in a separate block to prove object-count
   scaling.
4. Add one BG-event Sevii map in a separate block to prove BG pointer
   preservation.
5. Keep One Island last because it is the Bill/Celio/Network Machine and coord
   trigger preservation case.

Do not implement any rollout without keeping the map-by-map expected object
count checks fail-closed.

## Caveats

- All coordinates other than Viridian are design candidates, not gameplay-smoke
  proof.
- The common `(10, 5)` coordinate avoids reviewed object and warp coordinates,
  but collision/pathing still needs runtime smoke on every map.
- This design does not inspect or document ROM output, binary data, local build
  products, saves, emulator states, screenshots, raw logs, hashes, private
  paths, secrets, tokens or `.env` data.
- No claim is made for BizHawk, Ironmon Tracker, P1 support or full playthrough
  behavior.
