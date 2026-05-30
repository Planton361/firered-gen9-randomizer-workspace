# CFRU Bill Sevii QoL handoff

Status: `STOPPED_SOURCE_HOOK_NOT_FOUND`

## Scope

This record covers the requested isolated QoL feature: Bill should not
automatically push or ask the player to go to Sevii after Blaine.

No CFRU, DPE, UPR-FVX, Field Item, hidden-item, itemball, randomizer-writer,
ROM, save, build, tool-binary, log, screenshot, secret, token or `.env` file
was changed.

## Read-only CFRU findings

The current CFRU tree exposes Bill / Sevii / Blaine flow symbols, but not the
source-backed map scripts that own the behavior.

- `02_external/CFRU-expansion/include/constants/flags.h`
  - `FLAG_HIDE_CINNABAR_BILL`
  - `FLAG_HIDE_CINNABAR_SEAGALLOP`
  - `FLAG_HIDE_CINNABAR_POKECENTER_BILL`
  - `FLAG_HIDE_ONE_ISLAND_BILL`
  - `FLAG_HIDE_ONE_ISLAND_POKECENTER_BILL`
  - `FLAG_HIDE_ONE_ISLAND_POKECENTER_CELIO`
  - `FLAG_SEVII_DETOUR_FINISHED`
  - `FLAG_GOT_TM38_FROM_BLAINE`
  - `FLAG_DEFEATED_BLAINE`
  - `FLAG_SYS_SEVII_MAP_123`
  - `FLAG_SYS_SEVII_MAP_4567`
  - `FLAG_WORLD_MAP_CINNABAR_ISLAND`
  - `FLAG_WORLD_MAP_ONE_ISLAND`
- `02_external/CFRU-expansion/include/constants/vars.h`
  - `VAR_MAP_SCENE_CINNABAR_ISLAND`
  - `VAR_MAP_SCENE_CINNABAR_ISLAND_2`
  - `VAR_MAP_SCENE_ONE_ISLAND_HARBOR`
  - `VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F`
- `02_external/CFRU-expansion/include/constants/items.h`
  - `ITEM_TRI_PASS`
- `02_external/CFRU-expansion/include/constants/maps.h`
  - Cinnabar Island, Cinnabar Pokemon Center, One Island, One Island Harbor,
    and One Island Pokemon Center map constants.
- `02_external/CFRU-expansion/src/Tables/trainer_data.c`
  - Blaine trainer data only.
- `02_external/CFRU-expansion/src/debug_menu.c`
  - debug-only Sevii map flag setup.
- `02_external/CFRU-expansion/src/roamer.c`
  - commented Sevii map flag debug note only.
- `02_external/CFRU-expansion/src/Tables/item_tables.c`
  - Tri-Pass, Ruby and Sapphire item table data only.

The local CFRU script surfaces checked were:

- `02_external/CFRU-expansion/eventscripts`
- `02_external/CFRU-expansion/assembly/overworld_scripts/*.s`
- `02_external/CFRU-expansion/bytereplacement`
- `02_external/CFRU-expansion/src/scripting.c`
- `02_external/CFRU-expansion/include/script*.h`

Those surfaces do not contain source-backed Cinnabar Island, Cinnabar Pokemon
Center, One Island Harbor, One Island Pokemon Center, Celio, Tri-Pass, or
Blaine post-battle map scripts. The remaining CFRU surface for this behavior
would be raw address replacement, which is out of scope for this task.

## Vanilla reference flow

The pret FireRed reference shows the relevant behavior is map-script driven and
spans several subflows:

- `data/maps/CinnabarIsland_Gym/scripts.inc`
  - After Blaine is defeated, `CinnabarIsland_Gym_EventScript_DefeatedBlaine`
    sets `FLAG_DEFEATED_BLAINE`, `FLAG_BADGE07_GET`,
    `VAR_MAP_SCENE_CINNABAR_ISLAND = 1`, clears
    `FLAG_HIDE_CINNABAR_BILL`, and gives TM38.
- `data/maps/CinnabarIsland/scripts.inc`
  - `VAR_MAP_SCENE_CINNABAR_ISLAND = 1` triggers
    `CinnabarIsland_EventScript_BillScene` on frame.
  - Bill approaches the player outdoors and asks whether to go to One Island.
  - Yes calls `CinnabarIsland_EventScript_SailToOneIsland`.
  - No sets `VAR_MAP_SCENE_CINNABAR_ISLAND = 2`, removes outdoor Bill, and
    clears `FLAG_HIDE_CINNABAR_POKECENTER_BILL`.
  - Returning from Sevii uses `VAR_MAP_SCENE_CINNABAR_ISLAND = 3` and then
    moves the flow to state `4`.
- `data/maps/CinnabarIsland_PokemonCenter_1F/scripts.inc`
  - Bill in the Pokemon Center asks whether the player is ready to sail.
  - Yes hides the Pokemon Center Bill, sets
    `VAR_MAP_SCENE_CINNABAR_ISLAND_2 = 1`, clears
    `FLAG_HIDE_CINNABAR_BILL`, and warps outside for the sailing scene.
  - No leaves Bill waiting in the Pokemon Center.
- `data/maps/OneIsland_Harbor/scripts.inc`
  - `VAR_MAP_SCENE_ONE_ISLAND_HARBOR = 1` turns and walks the player out of
    the harbor, then moves the scene state to `2`.
- `data/maps/OneIsland_PokemonCenter_1F/scripts.inc`
  - `VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F = 0` triggers the Bill/Celio
    first-meeting scene.
  - The scene gives the Meteorite and `ITEM_TRI_PASS`, sets
    `FLAG_SYS_SEVII_MAP_123`, disables PC storage for the detour, and advances
    the scene to `1`.
  - The leave-One-Island triggers later set `FLAG_HIDE_ONE_ISLAND_POKECENTER_BILL`,
    `VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F = 3`,
    `VAR_MAP_SCENE_CINNABAR_ISLAND = 3`, and sail back to Cinnabar.
  - Later Celio/Ruby/Sapphire/Network Machine states reuse this same map scene
    family and must remain untouched.
- `data/scripts/seagallop.inc` and `src/seagallop.c`
  - Cinnabar and One Island scenes hand off to `EventScript_SetSail` with
    `SEAGALLOP_CINNABAR_ISLAND` / `SEAGALLOP_ONE_ISLAND`.

Relevant vanilla text/event labels checked:

- `CinnabarIsland_Text_HeyIfItIsntPlayer`
- `CinnabarIsland_Text_ComeWithMeToOneIsland`
- `CinnabarIsland_Text_AllRightLetsGo`
- `CinnabarIsland_Text_IllBeWaitingInPokeCenter`
- `CinnabarIsland_Text_MyPalsBoatArrived`
- `CinnabarIsland_Text_IfYouHaveTriPassYouCanGoAgain`
- `CinnabarIsland_PokemonCenter_1F_Text_ReadyToSailToOneIsland`
- `CinnabarIsland_PokemonCenter_1F_Text_OhNotDoneYet`
- `CinnabarIsland_PokemonCenter_1F_Text_LetsGo`
- `OneIsland_PokemonCenter_1F_Text_BillHeyThereCelio`
- `OneIsland_PokemonCenter_1F_Text_ThisIsMyBuddyCelio`
- `OneIsland_PokemonCenter_1F_Text_CanYouDeliverThisMeteoritePlayer`
- `OneIsland_PokemonCenter_1F_Text_AcceptedMeteoriteFromBill`
- `OneIsland_PokemonCenter_1F_Text_ObtainedTriPass`
- `OneIsland_PokemonCenter_1F_Text_PassLetsYouTravelBetweenIslands`
- `OneIsland_PokemonCenter_1F_Text_BillCatchYouLater`
- `OneIsland_PokemonCenter_1F_Text_BillWeGotItDone`
- `OneIsland_PokemonCenter_1F_Text_BillWeShouldHeadBackToKanto`
- `OneIsland_PokemonCenter_1F_Text_CelioPromiseIllShowYouAroundSometime`
- `OneIsland_PokemonCenter_1F_Text_HandedRubyToCelio`
- `OneIsland_PokemonCenter_1F_Text_HandedSapphireToCelio`
- `OneIsland_PokemonCenter_1F_Text_MachineLinkedWithKanto`
- `OneIsland_PokemonCenter_1F_Text_MachineLinkedWithKantoAndHoenn`

## Decision

No code change was made.

The smallest behavior-level target appears to be the transition immediately
after Blaine: avoid setting the outdoor Cinnabar scene to Bill's automatic
approach while still making Bill optionally available in the Cinnabar Pokemon
Center. However, that is not available as a local CFRU source-backed hook in
the current tree.

Implementing it safely would require one of these out-of-scope approaches:

- a raw address replacement for the vanilla Cinnabar Gym / Cinnabar Island
  scripts; or
- adding and owning multiple map-script subflows for Blaine, Cinnabar Island,
  Cinnabar Pokemon Center, and the Sevii return path; or
- changing several flag/object/scene states together without a source-backed
  script owner in this repo.

Because the user stop rules reject raw address replacements and multi-subflow
changes, this block stops as a design handoff.

## Manual smoke proposal

Future implementation should use a manual route that starts from gameplay before
Blaine and checks only this feature:

1. Defeat Blaine and receive TM38.
2. Exit the gym to Cinnabar.
3. Confirm Bill does not automatically approach or ask to sail to One Island.
4. Enter Cinnabar Pokemon Center.
5. Confirm Bill is present as an optional NPC.
6. Decline Bill's Pokemon Center prompt and confirm no warp or forced sailing
   occurs.
7. Talk to Bill again, accept, and confirm sailing to One Island still works.
8. Confirm the One Island Harbor arrival, Bill/Celio first meeting, Meteorite,
   Tri-Pass, and Sevii map page still work.
9. Complete the detour return path and confirm Cinnabar return state still
   works.
10. Spot-check that later Celio Ruby/Sapphire/Network Machine states are not
    regressed.

Do not combine this smoke with Faster Intro, Parcel, Oak/Lab, Repel-Reuse,
auto-run, poison, EXP, Runtime Options, Hidden Items, Itemfinder sparkle,
itemball graphics, Field Items, UPR-FVX writer, DPE data, Name Rater,
Viridian-Forest-Nurse, Step Item Guarantees, Friendship Boost, or binary patch
work.

## Next design block

Before implementation, identify one accepted source owner:

- either import/own the specific vanilla map script sources as a separately
  reviewed CFRU script-ownership design; or
- find an existing local CFRU source hook that runs after Blaine and before the
  Cinnabar outdoor frame script, and can atomically set the needed scene and
  visibility state.

That design must name every changed flag, var, object visibility state, warp,
and text/event hook before code.
