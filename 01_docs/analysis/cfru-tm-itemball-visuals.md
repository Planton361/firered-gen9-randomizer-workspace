# CFRU TM/HM itemball visual distinction design

Date: 2026-07-13

Workspace branch: `design/cfru-tm-itemball-visuals`

Status: `DESIGN_READY_FOR_PILOT`

## Scope and decision

This is a source-backed design only. It does not change CFRU, DPE, UPR-FVX,
graphics, palettes, submodule pins, ROMs or build output.

The design is ready for a one-slot CFRU pilot because the ownership boundary can
remain intact:

- UPR-FVX continues to own the item value in every recognized Field Item slot.
- CFRU owns the Object Event `graphicsId` used to draw the visible object.
- The CFRU 16-bit graphics id can select a new graphics table through its upper
  byte while retaining vanilla `OBJ_EVENT_GFX_ITEM_BALL` (`92`, `0x5C`) in its
  lower byte.
- UPR-FVX's Gen 3 reader currently checks only byte 1 of the object template,
  so a proposed gold id of `0x065C` still satisfies `pSprite == ItemBallPic`
  when `ItemBallPic=92`.
- No runtime scan, Overworld-frame hook, item-value lookup or UPR-FVX graphics
  write is required.

The lower-byte compatibility rule is mandatory. A custom id whose low byte is
not `92` would make the object invisible to the current UPR-FVX Field Item
reader and is therefore rejected.

## Sources reviewed

### CFRU

- `include/global.fieldmap.h`: `EventObjectTemplate` and
  `EventObjectGraphicsInfo` layouts, including `graphicsIdUpperByte`.
- `include/constants/maps.h`: `MAP_MT_MOON_1F` is map group `1`, map number
  `1`.
- `include/constants/map_objects.h`: current map-object ids.
- `include/constants/event_objects.h`: CFRU's expanded object-graphics ids.
- `include/follower_mon_sprites.h`: regular Object Event OAM, subsprite and
  GraphicsInfo patterns.
- `src/character_customization.c`: `gOverworldTableSwitcher`,
  `GetEventObjectGraphicsInfo()` and `GetEventObjectGraphicsId()` split and
  reconstruct the 16-bit graphics id. Tables `0..5` are occupied; index `6` is
  currently unregistered.
- `src/dynamic_ow_pals.c`: named Object Event palette tags are loaded and
  reference-counted through the regular Overworld palette path.
- `scripts/build.py`: recursively compiles PNG graphics with their local
  `gritflags.txt` and links the generated symbol normally.
- `scripts/insert.py` and `mapobjectoverlays`: the existing generator resolves a
  map by bank/number, reads and copies the current object table, emits a new
  object table and `MapEvents`, preserves warp/coord/BG pointers and repoints
  only `MapHeader.events`. The current command supports `append` only.

### UPR-FVX

- `random/.../ItemRandomizer.java`: Field Items are split into TM and non-TM
  stacks. Shuffle, Random and Random Even preserve the type of every API slot.
- `romio/.../Gen3RomHandler.java`: `preprocessMaps()` recognizes a visible
  Field Item only when object-template byte 1 equals `ItemBallPic` and its
  script has the standard `finditem` byte shape. Hidden Items are discovered
  separately through signposts. `getFieldItems()` / `setFieldItems()` use the
  collected item offsets.
- `romio/.../AbstractRomHandler.java` and `RomHandler.java`:
  `checkFieldItemsTMsReplaceTMs()` enforces TM-for-TM and non-TM-for-non-TM at
  every exposed index.
- `romio/.../Gen3Constants.java`: vanilla TM01..TM50 are TMs; HM01..HM08 are
  banned from normal pools. The FRLG required-Field-TM policy contains 24 TMs.
- Existing diagnostics `100`, `102`, `109`, `110`, `112` and `113`: the tested
  CFRU/DPE candidate has 28 raw/API TM Field Item slots; Shuffle, Random,
  Random Even and Ban Bad reload smokes preserve TM/non-TM typing and required
  TMs.

### FireRed source references

- pret and CyanSMP64 NatDex `data/maps/*/map.json`: visible balls are Object
  Events with `OBJ_EVENT_GFX_ITEM_BALL`; Hidden Items are BG events and have no
  visible Object Event.
- pret `data/scripts/item_ball_scripts.inc` and `data/scripts/obtain_item.inc`:
  standard visible Field Items call `finditem`; successful pickup removes the
  last-talked object.
- pret `src/event_object_movement.c`: removing an Object Event sets its template
  flag, and map spawning skips templates whose flag is set.
- Cyan `object_event_graphics.h`, `object_event_pic_tables.h`,
  `object_event_graphics_info.h` and pointer table: the normal item ball is one
  16x16, one-frame, inanimate Object Event using the standard 16x16 OAM path.

No patch file, raw-address port or binary-patch data was used as a design
source.

## Answers to the design questions

### 1. Where the visible graphic is selected

The map's `ObjectEventTemplate.graphicsId` selects the Object Event
`GraphicsInfo`. In vanilla source all standard visible Field Item objects use
`OBJ_EVENT_GFX_ITEM_BALL` (`92`). `GraphicsInfo` then selects the 16x16 frame,
palette tag, OAM, subsprite table and animation.

CFRU preserves the vanilla lower byte and adds `graphicsIdUpperByte` as the
graphics-table selector. `GetEventObjectGraphicsId()` reconstructs
`lower | upper << 8`; `GetEventObjectGraphicsInfo()` indexes the selected table
by the lower byte.

### 2. Do visible Field Items share one graphics id?

Yes for the standard FireRed `finditem` slots: all 168 visible standard slots in
the pret source use `OBJ_EVENT_GFX_ITEM_BALL`. Of those, 28 contain TMs and one
contains HM07.

There are ten additional objects which reuse the ball graphic but are not the
standard Field Item set: three starter balls, Eevee, two Fighting Dojo choices,
two Electrode encounters, Silph Scope and Lift Key. They are not selected by
this feature. Gifts, NPC rewards, shops and Hidden Items are also excluded.

### 3-5. Regular gold graphics and palette ownership

A second regular 16x16 inanimate Object Event is feasible through CFRU's
existing multi-table Object Graphics system:

- reserve table index `6` only after a build-time assertion confirms it is
  still unused;
- register a table whose designated entry `[92]` points to the new gold
  `EventObjectGraphicsInfo`;
- use graphics id `0x065C`, retaining low byte `0x5C` / `92`;
- reuse the existing 16x16 OAM, 16x16 subsprite table and a one-frame inanimate
  animation;
- use the regular build-discovered PNG/grit path.

No new palette is needed for the pilot. The existing static NPC-white palette
used by the normal item ball already contains an unused three-color muted-gold
ramp at indices 5, 6 and 7. The normal ball uses the red ramp at indices 8, 9
and 10. A gold tile can therefore retain palette tag `0x1106` and substitute
the gold indices without consuming another OBJ palette slot.

If visual review later rejects that ramp, a new static palette would have to be
added to CFRU's normal `gObjectEventSpritePalettes11` registry with a unique
`0x11xx` tag and loaded by the existing dynamic Overworld palette manager. A
private `LoadSpritePalette`/`FreeSpritePaletteByTag` lifecycle is not allowed.
That alternative is not part of the first pilot.

### 6-7. Overlay behavior and field preservation

The current `mapobjectoverlays` implementation cannot replace an existing
entry; it only appends. Its source-backed ownership model is nevertheless
sufficient for a small extension: add a `replace_graphics` operation that
copies the existing 24-byte template, validates it, changes only graphics-id
bytes 1 and 3, and emits the same replacement table/`MapEvents` structure used
by `append`.

The following fields must remain byte-identical:

- `localId`
- connection state
- `x` / `y`
- elevation
- movement type and X/Y range
- trainer type and range
- script pointer
- object flag and secondary flag

Object count, warp pointer, coord-event pointer and BG-event pointer also remain
unchanged. A replacement is rejected if any expected field differs.

### 8. Separating visible Field Items from other sources

The rollout list is an explicit whitelist derived from objects that satisfy all
of these source conditions:

1. an Object Event, not a BG/hidden event;
2. `graphics_id == OBJ_EVENT_GFX_ITEM_BALL`;
3. a standard script in `item_ball_scripts.inc` whose command is
   `finditem ITEM_TMxx` or `finditem ITEM_HMxx`;
4. a unique map/local-id/coordinate/flag tuple.

NPC `giveitem` scripts, gifts, shops, Pickup, starters, static encounters,
special key-item scripts and Hidden Items fail this selection and stay normal
or invisible as before.

### 9-10. Vanilla visible TM/HM ball inventory

There are **29** visible TM/HM item-ball slots: **28 TM slots and one HM slot**.

| Item | Map | Local ID | Coordinate | Elevation | Expected objects |
|---|---|---:|---:|---:|---:|
| TM09 | MtMoon_1F | 9 | (11, 35) | 3 | 14 |
| TM46 | MtMoon_B2F | 9 | (35, 5) | 3 | 11 |
| TM05 | Route4 | 3 | (67, 5) | 3 | 7 |
| TM45 | Route24 | 8 | (11, 4) | 3 | 8 |
| TM43 | Route25 | 10 | (26, 2) | 3 | 13 |
| TM31 | SSAnne_1F_Room2 | 4 | (5, 7) | 3 | 4 |
| TM44 | SSAnne_B1F_Room2 | 2 | (3, 2) | 3 | 2 |
| TM40 | Route9 | 11 | (12, 17) | 3 | 12 |
| TM12 | RocketHideout_B2F | 4 | (5, 7) | 3 | 5 |
| TM21 | RocketHideout_B3F | 4 | (19, 14) | 3 | 5 |
| TM49 | RocketHideout_B4F | 7 | (1, 6) | 3 | 9 |
| TM48 | Route12 | 10 | (18, 36) | 3 | 14 |
| TM18 | Route15 | 11 | (20, 6) | 3 | 14 |
| TM11 | SafariZone_East | 3 | (31, 18) | 3 | 4 |
| TM47 | SafariZone_North | 2 | (28, 9) | 3 | 3 |
| TM32 | SafariZone_West | 2 | (17, 13) | 3 | 4 |
| TM01 | SilphCo_5F | 7 | (1, 18) | 3 | 9 |
| TM08 | SilphCo_7F | 11 | (30, 11) | 3 | 11 |
| TM17 | PowerPlant | 2 | (40, 22) | 3 | 8 |
| TM25 | PowerPlant | 3 | (46, 37) | 3 | 8 |
| TM14 | PokemonMansion_B1F | 4 | (23, 4) | 3 | 6 |
| TM22 | PokemonMansion_B1F | 1 | (6, 21) | 3 | 6 |
| TM02 | VictoryRoad_1F | 4 | (14, 1) | 3 | 7 |
| TM07 | VictoryRoad_2F | 7 | (40, 7) | 3 | 13 |
| TM37 | VictoryRoad_2F | 9 | (14, 13) | 3 | 13 |
| TM50 | VictoryRoad_3F | 6 | (12, 9) | 3 | 12 |
| HM07 | FourIsland_IcefallCave_1F | 2 | (12, 16) | 3 | 2 |
| TM36 | FiveIsland_RocketWarehouse | 8 | (17, 3) | 0 | 10 |
| TM41 | SilphCo_4F | 8 | (30, 18) | 0 | 8 |

HM01-HM06 are obtained from NPC/script rewards (SS Anne Captain, Route 16
house, Safari Zone Secret House, Warden, Route 2 aide and Ember Spa) and are
explicitly outside this visual feature. Gym rewards and other non-ball TM
sources are also outside the whitelist.

### 11-14. Randomizer slot semantics

The static slot design is safe for the currently supported modes, with two
different source-backed reasons:

- The 28 TM slots are exposed as `Item.isTM()`. Shuffle uses a separate TM
  stack. Random and Random Even generate a separate TM result, and the writer
  rejects a TM/non-TM mismatch. Ban Bad only changes the non-TM pool.
- HM07 is globally banned from normal item pools, is not marked as `Item.isTM()`
  and is therefore excluded from the CFRU/DPE Field Item API slot set. The
  writer leaves it unchanged.

Consequently, a normal exposed slot cannot receive a TM in Shuffle, Random or
Random Even, and the one preserved HM ball remains HM07. The gold classification
does not need to follow output metadata at runtime.

The custom graphics id must retain low byte `92`. `Gen3RomHandler` reads only
that byte while locating visible Field Items. With proposed id `0x065C`, UPR-FVX
continues to find the same script/item field and writes only its item value.
No new metadata or graphics writer is required.

### 15-16. First pilot and normal control

Use one map for both cases:

| Role | Map | Bank / number | Local ID | Coordinate | Elevation | Objects | Script | Flag |
|---|---|---|---:|---:|---:|---:|---|---|
| Gold TM pilot | MtMoon_1F | 1 / 1 | 9 | (11, 35) | 3 | 14 | `MtMoon_1F_EventScript_ItemTM09` | `FLAG_HIDE_MT_MOON_1F_TM09` |
| Normal control | MtMoon_1F | 1 / 1 | 10 | (26, 32) | 3 | 14 | `MtMoon_1F_EventScript_ItemPotion` | `FLAG_HIDE_MT_MOON_1F_POTION` |

TM09 is early, source-simple and shares a map with an unchanged normal
`finditem` ball. Only local id 9 receives the overlay. Local id 10 is an
asserted, untouched control.

### 17. Reload and runtime proof

The first pilot must prove all three ownership layers:

1. CFRU clean build and link register the graphics table and asset normally.
2. UPR-FVX scans the gold object because its low graphics byte is still 92,
   writes a TM to the same script field, saves and reloads with zero Field Item
   mismatch.
3. Runtime shows a gold TM ball and a normal control ball, grants the randomized
   items, sets each original object flag, and keeps each collected object hidden
   after an in-game save/reload.

## Fail-closed pilot contract

The future `replace_graphics` generator operation must stop the build unless all
of these are true:

- map bank `1`, map number `1` resolve successfully;
- object count is exactly `14`;
- exactly one template has local id `9`;
- local id 9 is `(11, 35)`, elevation `3`;
- movement is face-down with range `1/1`;
- trainer type/range are none/`0`;
- current full graphics id is vanilla `0x005C`;
- script pointer is non-null and the source-backed standard `finditem` script
  shape contains TM09 before randomization;
- object flag is `FLAG_HIDE_MT_MOON_1F_TM09` and secondary flag is unchanged;
- local id 10 still matches the normal Potion control at `(26, 32)` with full
  graphics id `0x005C`;
- target id is exactly `0x065C`, table index `6` is registered exactly once and
  its entry array contains index `92`;
- the serialized before/after templates differ only at graphics-id byte 3;
  byte 1 deliberately remains `92`.

The script pointer itself has no CFRU linker symbol. The generator must not add
a raw pointer constant. It can preserve the pointer byte-for-byte and validate
the standard script structure/item operand source-backed from pret and the
existing UPR-FVX parser.

## Later pilot file allowlist

Only the following CFRU files are allowed for the first implementation, subject
to verifying the same paths again at the implementation commit:

- `graphics/Overworld/TM_Item_Ball/TMItemBall.png` (new 16x16 indexed tile)
- `graphics/Overworld/TM_Item_Ball/gritflags.txt` (new regular grit config)
- `include/constants/map_objects.h` (one 16-bit graphics-id constant)
- `include/new/tm_itemball_graphics.h` (new declarations/constants only)
- `src/Tables/tm_itemball_graphics.c` (one frame, one GraphicsInfo, one table)
- `src/character_customization.c` (register table index 6 only)
- `scripts/insert.py` (fail-closed `replace_graphics` operation)
- `mapobjectoverlays` (one MtMoon_1F TM09 replacement row)

No UPR-FVX, DPE, Overworld frame, pickup script, hidden-item, dynamic-palette,
normal item-ball or other-map file is allowed in the pilot.

## Resource risks and controls

- **OBJ palette:** no additional slot; reuse tag `0x1106`. Confirm gold and
  normal balls coexist without palette changes to player/NPC/environment.
- **OBJ VRAM:** a second graphic present on the same map can allocate another
  128 bytes/four tiles. Smoke MtMoon_1F with both balls visible and all NPCs.
- **OAM/sprites:** object count is unchanged; one object still owns one sprite.
- **Table bounds:** the new table must have a designated `[92]` entry; CFRU does
  not bounds-check the low-byte index before dereference.
- **Weather/reflection:** mirror the normal inanimate 16x16 item-ball settings;
  no reflection palette and no private palette lifecycle.
- **Randomizer discovery:** retain low byte `92`; add a source-level assertion or
  test around the constant.
- **Generator composition:** replacement must preserve existing overlays and
  all non-object event pointers; no reset of the Compat history.

## Design conclusion

`DESIGN_READY_FOR_PILOT`

The result is static and build-time, but remains output-correct because the
supported UPR-FVX modes preserve TM slots and the single HM object is
preserve-only. CFRU can select a second regular Object Graphics table through
the upper graphics-id byte without changing the lower byte used by UPR-FVX's
Field Item reader.
