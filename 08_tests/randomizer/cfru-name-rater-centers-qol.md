# CFRU Name Rater Pokecenter pilot

Status: `IMPLEMENTED_PILOT_SOURCE_BACKED`

## Scope

This block implements exactly one QoL pilot: a Name Rater hook in one selected
Pokecenter.

Pilot map: `MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F`.

No global Pokecenter rollout was added. No Pewter City, other Pokecenter,
Faster Intro, Oak/Lab/Parcel, Bill-Sevii, Repel-Reuse, auto-run, poison, EXP,
Runtime Options, Hidden Items, Itemfinder sparkle, itemball graphics, Field
Items, UPR-FVX writer, DPE data, Viridian-Forest-Nurse, Step Item Guarantees,
Friendship Boost or binary patch work was changed.

## Read-only source findings

Current CFRU already has nickname-capable vanilla special plumbing:

- `02_external/CFRU-expansion/src/scripting.c`
  - `sp07C_BufferNickname`
  - `sp07D_CheckTradedPokemon`
  - `sp09E_NicknamePokemon`
- `02_external/CFRU-expansion/src/config.h`
  - `AUTO_NAMING_SCREEN_SWAP` is enabled.
  - `REPLACE_SOME_VANILLA_SPECIALS` is disabled, so the vanilla special table
    remains compatible for the Name Rater flow.
- `02_external/CFRU-expansion/routinepointers`
  - Documents optional replacement addresses for `sp07C`, `sp07D`, and
    `sp09E` if `REPLACE_SOME_VANILLA_SPECIALS` is enabled later.
- `02_external/CFRU-expansion/eventscripts`
  - Provides a local source-backed event-script pointer replacement surface by
    map bank, map number, object event id, and script symbol.

Vanilla reference flow checked read-only:

- `02_external/references/pret-pokefirered/data/maps/LavenderTown_House2/scripts.inc`
  - Existing Name Rater flow: choose party mon, reject eggs/traded mons, open
    nickname screen, then report whether the name changed.
- `02_external/references/pret-pokefirered/data/maps/LavenderTown_House2/text.inc`
  - Text shape only; no file copied.
- `02_external/references/pret-pokefirered/data/specials.inc`
  - Relevant special ids: `NameRaterWasNicknameChanged`, `BufferMonNickname`,
    `IsMonOTIDNotPlayers`, `ChangePokemonNickname`, `ChoosePartyMon`,
    `GetPartyMonSpecies`, and `IsMonOTNameNotPlayers`.
- `02_external/references/pret-pokefirered/data/maps/ViridianCity_PokemonCenter_1F/map.json`
  - Viridian Pokecenter 1F has object event id `1`, a Gentleman at `(12, 5)`,
    separate from the Nurse and PC/link-area objects.
- `02_external/references/pret-pokefirered/data/maps/PewterCity_PokemonCenter_1F/map.json`
  - Pewter also has candidate NPCs, but was not selected because the task
    allows only one pilot map and Viridian is earlier/recommended.

## Implemented hook

Changed CFRU files:

- `02_external/CFRU-expansion/eventscripts`
- `02_external/CFRU-expansion/assembly/overworld_scripts/name_rater_pilot.s`
- `02_external/CFRU-expansion/strings/Scripts/name_rater_pilot.string`

Implementation details:

- Repoints only Viridian Pokecenter 1F object event id `1`:
  `npc 5 4 1 EventScript_PilotPokeCenterNameRater`.
- Keeps Nurse/healing, PC, Cable Club upstairs warp, Runtime Options and other
  maps untouched.
- Uses one existing object-event hook instead of adding map-object structure.
- Uses vanilla Name-Rater-capable specials by id:
  - `0x7B` nickname-changed check
  - `0x7C` buffer nickname
  - `0x7D` OT ID ownership check
  - `0x9E` nickname screen
  - `0x9F` party chooser
  - `0x147` party mon species
  - `0x150` OT name ownership check
- Adds short project-local text rather than copying vanilla text/source files.

## Manual smoke proposal

Use a local gameplay candidate and record only sanitized pass/fail notes:

1. Enter Viridian City Pokecenter 1F.
2. Confirm the Nurse still heals normally.
3. Confirm PC access still opens normally.
4. Talk to the Gentleman object at the right side of the room.
5. Choose `No` at the Name Rater intro and confirm the script exits normally.
6. Talk again, choose `Yes`, select an eligible player-owned non-Egg party mon,
   and confirm the nickname screen opens.
7. Cancel from the naming screen and confirm field control returns without
   softlock.
8. Repeat, enter a changed nickname, and confirm the new nickname is applied.
9. Select an Egg if available and confirm the Egg rejection path.
10. Select a traded/non-player-OT mon if available and confirm the rejection
    path.
11. Confirm no Runtime Options, healing, PC, upstairs warp, Field Items,
    hidden-item cues or randomizer-output behavior changed.

## Rollout handoff

Do not roll this out globally until the Viridian pilot smoke passes.

If the pilot passes, a later rollout design should:

- choose whether every Pokecenter receives a replacement existing NPC hook or a
  real new object-event ownership model;
- list each target map bank, map number, object event id, and original NPC
  behavior being replaced;
- decide whether the Name Rater should stay party-only or support boxed Pokemon
  by enabling/reviewing CFRU special replacements;
- keep healing, PC, link rooms, Runtime Options, Field Items, randomizer writer,
  DPE data and unrelated QoL unchanged.

## Caveats

- This pilot repoints an existing Viridian Pokecenter Gentleman NPC; it does
  not add a new object event.
- Visual identity remains the existing Gentleman object event.
- No ROM build, emulator run, save/state inspection, screenshot, raw log, hash,
  private path or generated artifact is included.
