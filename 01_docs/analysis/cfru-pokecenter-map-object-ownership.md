# CFRU Pokecenter map object ownership design

Status: `IMPLEMENTABLE_MEDIUM_DESIGN_ONLY`

Branch: `design/cfru-pokecenter-map-object-ownership`

## Scope

This is a design-only analysis for adding extra Pokecenter NPCs to CFRU in a
source-backed way. No CFRU, DPE, UPR-FVX, ROM, binary patch, build artifact,
tool binary, save, emulator state, screenshot, raw log, private path, token,
secret or `.env` data was read, changed or documented.

The immediate feature pressure is the rejected Name Rater pilot: the desired
target is an added, uniform Name Rater NPC per Pokecenter, not replacement of
existing local NPCs.

## Current CFRU source model

Reviewed local CFRU surfaces:

- `02_external/CFRU-expansion/include/global.fieldmap.h`
- `02_external/CFRU-expansion/include/global.h`
- `02_external/CFRU-expansion/include/constants/maps.h`
- `02_external/CFRU-expansion/include/constants/map_objects.h`
- `02_external/CFRU-expansion/include/event_object_movement.h`
- `02_external/CFRU-expansion/scripts/insert.py`
- `02_external/CFRU-expansion/eventscripts`
- selected read-only uses in `src/overworld.c`, `src/follow_me.c`, and
  `src/Tables/movement_action.tables.c`

CFRU's field-map structs match the FireRed shape at the important ownership
points:

- `MapHeader` offset `0x04`: pointer to `MapEvents`
- `MapEvents`: four counts followed by four table pointers:
  `eventObjectCount`, `warpCount`, `coordEventCount`, `bgEventCount`,
  then `eventObjects`, `warps`, `coordEvents`, `bgEvents`
- `EventObjectTemplate`: `0x18` bytes in the current CFRU header, with
  `localId`, graphics id bytes, coordinates, elevation, movement, range,
  trainer metadata, script pointer, `flagId`, and CFRU-local `flagId2`

Current CFRU map-event source ownership is limited. The local repo exposes
`eventscripts`, but not source-owned `map.json` or generated map-event arrays
for Viridian/Pewter Pokecenters.

`scripts/insert.py` handles `eventscripts` by resolving the map bank and map
number through the ROM map-bank table, then:

- reads `MapHeader.events`;
- reads the current object count from `MapEvents`;
- rejects any `npc` id greater than or equal to that count;
- writes only the script pointer field at
  `npcTable + eventId * 0x18 + 0x10`.

So the current hook can repoint existing object-event scripts. It cannot append
objects, update `eventObjectCount`, allocate a replacement object table, or
repoint the map header to a replacement `MapEvents`.

Runtime capacity is not the immediate blocker: CFRU keeps
`MAP_OBJECTS_COUNT` at `16` active object slots and saveblock
`eventObjectTemplates[64]`. Pokecenters are below those limits even after one
added NPC. The blocker is source ownership of the map event table.

## Vanilla / pret reference model

Reviewed read-only pret FireRed surfaces:

- `02_external/references/pret-pokefirered/include/global.fieldmap.h`
- `02_external/references/pret-pokefirered/asm/macros/map.inc`
- `02_external/references/pret-pokefirered/tools/mapjson/mapjson.cpp`
- `02_external/references/pret-pokefirered/data/map_events.s`
- `02_external/references/pret-pokefirered/data/maps/map_groups.json`
- `02_external/references/pret-pokefirered/data/maps/*PokemonCenter_1F/map.json`
- `02_external/references/pret-pokefirered/src/overworld.c`
- `02_external/references/pret-pokefirered/src/event_object_movement.c`

pret owns map events through `data/maps/<MapName>/map.json`. `mapjson` emits:

- an object-event array from `object_events`;
- warp, coord, and bg arrays;
- a `<MapName>_MapEvents` struct with generated counts and pointers.

The `object_event` macro assigns local ids as one-based `i + 1`, while CFRU's
`eventscripts` file addresses existing object table rows by zero-based table
index. For Viridian, prior `npc 5 4 1 ...` therefore meant table row `1`, which
is local id `2` in vanilla macro terms.

pret's runtime loader copies `gMapHeader.events->objectEvents` into
`gSaveBlock1Ptr->objectEventTemplates`, then object lookup and script lookup
resolve by local id, map number, and map group.

Pokecenter 1F object counts in the pret reference vary substantially:

| Map | Object count | Notes |
|---|---:|---|
| Two Island | 3 | Smallest reviewed 1F Pokecenter. |
| Viridian, Celadon, Four Island, Fuchsia, Six Island, Three Island | 4 | Viridian is in this group. |
| Five Island, Lavender, Route 10 | 5 | Moderate. |
| One Island, Route 4, Saffron, Seven Island | 6 | One Island also has coord/bg events. |
| Cerulean, Cinnabar, Pewter, Vermilion | 7 | Larger local NPC sets. |
| Indigo Plateau | 8 | Largest reviewed 1F Pokecenter. |

This variation is the reason existing-NPC replacement is not a good rollout
model.

## Strategy evaluation

### 1. Extend existing map object arrays in place

Description: append one `EventObjectTemplate` after the existing object table
and increment the existing count.

- Affected subsystems: map event tables, `MapEvents.eventObjectCount`,
  object-event template arrays.
- Raw-address replacement: yes with current CFRU source, because the original
  object arrays are not locally source-owned and may not have contiguous free
  space after them.
- Runtime risk: high. Overwriting adjacent map data is likely unless each table
  layout is proven.
- Reviewability: poor. The diff would be offsets or binary-like table patches.
- Rollout scalability: poor. Every map needs table-specific proof.
- UPR-FVX / Field Items / Hidden Items compatibility: unsafe if bg/item tables
  or adjacent event data are damaged.
- Smoke gate: full map entry, all original NPCs, warps, hidden/bg events, and
  target NPC per modified map.

Decision: reject for this project. It is not a source-backed rollout model.

### 2. Repoint complete `MapEvents` with copied existing object table plus additions

Description: add a CFRU insertion surface that resolves a map by bank/number,
copies the existing object table from the source ROM at insertion time, appends
source-defined new object templates, emits a new object table and replacement
`MapEvents`, preserves original warp/coord/bg pointers, then repoints
`MapHeader.events` at offset `0x04`.

- Affected subsystems: `scripts/insert.py`, a new source manifest for map-object
  additions, linked symbols for new scripts/text, map header event pointer
  repointing.
- Raw-address replacement: no fixed raw address is needed if the tool derives
  map header and original event pointers from map bank/number, like
  `eventscripts` already does. It still writes ROM pointers during insertion,
  but source ownership is the manifest plus deterministic generator.
- Runtime risk: medium. The replacement `MapEvents` must preserve warp, coord,
  and bg pointers exactly, copy all original object templates correctly, and
  respect CFRU's `EventObjectTemplate` layout including `flagId2`.
- Reviewability: good if the manifest lists only map id and appended object
  fields; mediocre if generated binary table bytes are committed.
- Rollout scalability: good. A per-map manifest row can add one Name Rater to
  each Pokecenter without replacing local NPCs.
- UPR-FVX / Field Items / Hidden Items compatibility: good if warp/coord/bg
  pointers are preserved and no bg event tables are rewritten. Field Items and
  Hidden Items remain UPR-FVX/CFRU owners respectively.
- Smoke gate: for each pilot map, original NPCs/scripts, warps, PC/Nurse, new
  NPC, and any coord/bg events. One Island needs extra care because it has
  coord and bg events.

Decision: recommended implementation path. This is implementable-medium, not
implementable-small.

### 3. Repoint complete object-event table only

Description: keep the existing `MapEvents` struct but change its
`eventObjectCount` and `eventObjects` pointer to a new object array.

- Affected subsystems: object table pointer and count inside `MapEvents`.
- Raw-address replacement: yes unless the existing `MapEvents` struct itself is
  source-owned or a safe derived pointer writer is added.
- Runtime risk: medium/high. Mutating only the embedded count/pointer in an
  original event header is a partial ownership model.
- Reviewability: weaker than Strategy 2 because the original `MapEvents`
  struct remains split-owned.
- Rollout scalability: moderate if tool-driven, poor if manual.
- UPR-FVX / Field Items / Hidden Items compatibility: acceptable only if warp,
  coord, and bg table pointers are untouched.
- Smoke gate: same as Strategy 2.

Decision: inferior to Strategy 2. Use only if a future design explicitly proves
that patching the existing `MapEvents` count/pointer is safer in CFRU's build
pipeline than replacing the whole `MapEvents` pointer.

### 4. CFRU-owned runtime map-object override system

Description: hook map load or transition logic so CFRU checks the current map
and spawns additional object templates at runtime, without replacing
`MapHeader.events`.

- Affected subsystems: overworld map-load path, object-event spawning,
  script-pointer lookup, saveblock templates, object visibility/flags.
- Raw-address replacement: not necessarily, if hookable through existing CFRU
  source. It may require a function hook if the load path is vanilla-owned.
- Runtime risk: medium/high. `SpawnSpecialEventObject` can create object events,
  but vanilla script lookup normally resolves through map object templates by
  local id and map. A spawned object whose local id is absent from
  `gMapHeader.events->objectEvents` may need script-lookup overrides to avoid
  null/incorrect scripts.
- Reviewability: good for a small table of overrides; more complex for hooks.
- Rollout scalability: good after the system exists.
- UPR-FVX / Field Items / Hidden Items compatibility: good if it does not touch
  bg/item tables, but runtime object limits and local-id collisions must be
  guarded.
- Smoke gate: map entry/re-entry, object visibility, talk script lookup, object
  reload after screen transitions, follower/temporary object coexistence.

Decision: viable but riskier than Strategy 2 for static service NPCs. Better
reserved for dynamic/conditional NPCs.

### 5. Generator or patch layer from JSON/map-source overlays

Description: create a project-local overlay manifest in a structured format,
for example only `append_object_events`, and generate the Strategy 2 replacement
tables from that overlay.

- Affected subsystems: new generator or `insert.py` extension, overlay data,
  optional validation against pret-like JSON fields.
- Raw-address replacement: no fixed raw address if map bank/number resolution is
  derived.
- Runtime risk: medium. Same as Strategy 2, plus generator validation quality.
- Reviewability: best if only overlay JSON/CSV and generated symbols are
  committed; avoid committing copied foreign full map files.
- Rollout scalability: best. A uniform Name Rater rollout can be represented as
  one row per Pokecenter.
- UPR-FVX / Field Items / Hidden Items compatibility: good if the generator
  copies original non-object event tables and refuses bg/hidden-item edits.
- Smoke gate: generator dry check, one-map pilot, then batch rollout smoke.

Decision: recommended form of Strategy 2. Use a minimal overlay, not full copied
pret map files.

### 6. Conscious reject

Description: reject added Pokecenter NPCs entirely and keep Name Rater only in
the vanilla location.

- Affected subsystems: none.
- Raw-address replacement: no.
- Runtime risk: none.
- Reviewability: excellent.
- Rollout scalability: n/a.
- UPR-FVX / Field Items / Hidden Items compatibility: no impact.
- Smoke gate: none.

Decision: not necessary. A source-backed medium path exists, so full reject is
too conservative.

## Viridian pilot design

Current map id:

- `MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F`
- CFRU map bank `5`, map number `4`

Current reference object count: `4`.

Existing reference object table:

| Zero-based table row | Local id in pret macro model | Sprite | Coordinate | Script |
|---:|---:|---|---|---|
| 0 | 1 | Nurse | `(7, 2)` | `ViridianCity_PokemonCenter_1F_EventScript_Nurse` |
| 1 | 2 | Gentleman | `(12, 5)` | `ViridianCity_PokemonCenter_1F_EventScript_Gentleman` |
| 2 | 3 | Boy | `(4, 7)` | `ViridianCity_PokemonCenter_1F_EventScript_Boy` |
| 3 | 4 | Youngster | `(2, 3)` | `ViridianCity_PokemonCenter_1F_EventScript_Youngster` |

Desired added object:

| Field | Proposed value |
|---|---|
| New zero-based table row | `4` |
| New local id | `5` |
| Sprite | `MAP_OBJ_GFX_GENTLEMAN` in CFRU, matching vanilla Name Rater identity |
| Candidate coordinate | `(10, 5)` |
| Elevation | `3` |
| Movement | `MOVEMENT_TYPE_FACE_DOWN` |
| Movement range | `1, 1` for parity with vanilla Name Rater, or `0, 0` if later validation prefers fixed service NPCs |
| Trainer type | `TRAINER_TYPE_NONE` |
| Sight / berry id | `0` |
| Script | future local `EventScript_PokeCenterNameRater` |
| Flag | `0` |
| CFRU `flagId2` | `0` |

The coordinate is a design candidate, not implementation proof. The
implementation block must verify collision/walkability in a local gameplay
smoke and move the NPC if it blocks player flow, PC access, Nurse access, or
warps.

Pointer/count changes required for Strategy 2:

1. Read original `MapHeader` for bank `5`, map `4`.
2. Read original `MapHeader.events`.
3. Read original `MapEvents.eventObjectCount == 4`.
4. Copy four original `EventObjectTemplate` entries from the original object
   table.
5. Append the new template as row `4` / local id `5`.
6. Emit a replacement object table with five entries.
7. Emit replacement `MapEvents` with `eventObjectCount == 5`, the replacement
   object table pointer, and the original warp/coord/bg counts and pointers.
8. Repoint `MapHeader.events` to the replacement `MapEvents`.

## Recommended implementation gate

Result decision: `implementable-medium`.

Do not implement this as a small one-file script hook. The next implementation
block should first add the map-object ownership infrastructure for exactly one
pilot map, then add the Viridian Name Rater through that infrastructure.

Recommended branch:

- `feature/cfru-pokecenter-map-object-override-pilot`

Recommended implementation boundaries:

- no full pret map-source copy;
- no fixed raw map-address replacements in checked-in source;
- no UPR-FVX, DPE, Field Item, Hidden Item or itemball graphics changes;
- first pilot only: Viridian Pokecenter 1F;
- generated/replacement data must preserve original warp/coord/bg tables.

## Caveats

- This design did not inspect a ROM or binary layout directly.
- The candidate Viridian coordinate still needs a gameplay/collision smoke.
- One Island and other maps with coord/bg events need extra preservation tests
  before rollout.
- Runtime object slot pressure is unlikely in Pokecenters but should still be
  asserted because CFRU uses `MAP_OBJECTS_COUNT == 16`.
