# CFRU Name Rater Pokecenter pilot

Status: `STOPPED_ADDITIONAL_OBJECT_EVENT_NOT_SOURCE_BACKED`

## Scope

This block re-checks the Name Rater Pokecenter pilot after review feedback on
PR #448.

Desired pilot map: `MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F`.

Desired target state: add one new, uniform Name Rater NPC to Viridian City
Pokecenter 1F without replacing or repointing an existing NPC.

No global Pokecenter rollout was added. No Pewter City, other Pokecenter,
Faster Intro, Oak/Lab/Parcel, Bill-Sevii, Repel-Reuse, auto-run, poison, EXP,
Runtime Options, Hidden Items, Itemfinder sparkle, itemball graphics, Field
Items, UPR-FVX writer, DPE data, Viridian-Forest-Nurse, Step Item Guarantees,
Friendship Boost or binary patch work was changed.

## Read-only source findings

Current CFRU still has nickname-capable vanilla special plumbing:

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
  - Viridian Pokecenter 1F has four object events:
    - object event id `0`: Nurse at `(7, 2)`
    - object event id `1`: Gentleman at `(12, 5)`
    - object event id `2`: Boy at `(4, 7)`
    - object event id `3`: Youngster at `(2, 3)`
- `02_external/CFRU-expansion/include/constants/maps.h`
  - `MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F` is map bank `5`, map number `4`.

## Rejected prior pilot

PR #448 previously used:

```text
npc 5 4 1 EventScript_PilotPokeCenterNameRater
```

That changed Viridian Pokecenter object event id `1`, the existing Gentleman at
`(12, 5)`, into the Name Rater pilot hook.

This is rejected as the rollout basis because Pokecenters have different
existing NPCs and scripts. A uniform rollout model needs an added Name Rater
object event per target Pokecenter, not replacement of map-specific local
dialogue NPCs.

The CFRU branch now removes the prior replacement hook and removes the unused
local pilot script/text. The original Gentleman object event is left owned by
the vanilla map object table and script pointer.

## Additional object-event check

The available local CFRU source-backed event surface is
`02_external/CFRU-expansion/eventscripts`, parsed by
`02_external/CFRU-expansion/scripts/insert.py`.

For `npc`, `trainer`, and `item` rows, the inserter:

- reads the target map header from the ROM map-bank table;
- reads the event header and existing object-event count;
- rejects any object id greater than or equal to the existing count;
- writes only the script pointer field at `npcTable + eventId * 0x18 + 0x10`.

That means `eventscripts` can repoint scripts on existing object events, but it
cannot add a fifth object event to
`MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F`, increment the object count, allocate a
new object-event table, or repoint the map event header to that new table.

No local CFRU source file was found that owns Viridian/Pewter Pokecenter
`object_events` in source form. Implementing an added NPC from the current
source surface would require a raw map-event-table replacement or a broader
map-object ownership/refactor design, both outside this block.

## Stop decision

No new Name Rater NPC is implemented in this correction.

Reason: a new Viridian Pokecenter object event is not source-backed by the
current CFRU hook surface. The only small hook found is replacement of an
existing object event, and that replacement model is explicitly rejected for
the desired rollout.

## Future smoke proposal

Run this only after a future source-backed map-object ownership design adds a
real fifth object event to Viridian Pokecenter:

1. Enter Viridian City Pokecenter 1F.
2. Confirm the original Gentleman still has his normal dialogue.
3. Confirm the Nurse still heals normally.
4. Confirm PC access still opens normally.
5. Talk to the added Name Rater NPC.
6. Choose `No` at the Name Rater intro and confirm the script exits normally.
7. Talk again, choose `Yes`, select an eligible player-owned non-Egg party mon,
   and confirm the nickname screen opens.
8. Cancel from the naming screen and confirm field control returns without
   softlock.
9. Repeat, enter a changed nickname, and confirm the new nickname is applied.
10. Select an Egg if available and confirm the Egg rejection path.
11. Select a traded/non-player-OT mon if available and confirm the rejection
    path.
12. Confirm no Runtime Options, healing, PC, upstairs warp, Field Items,
    hidden-item cues or randomizer-output behavior changed.

## Rollout handoff

Do not roll this out globally from object replacement.

A later accepted design should first add or expose source ownership for map
object events, then pilot exactly one added NPC in Viridian Pokecenter. That
design must list map bank, map number, new object event id, sprite, coordinates,
movement, elevation, script symbol, and any event-table ownership changes before
code.

## Caveats

- This correction intentionally leaves no playable Name Rater in Viridian
  Pokecenter.
- No ROM build, emulator run, save/state inspection, screenshot, raw log, hash,
  private path or generated artifact is included.
