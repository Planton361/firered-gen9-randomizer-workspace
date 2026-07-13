# CFRU TM/HM itemball NatDex parity and rollout handoff

Date: 2026-07-13

Status: `ROLLOUT_READY_FOR_29_TM_HM_CFRU_POLICY`

## Result

The planned whitelist has exact map-object parity with the local CyanSMP64
NatDex reference: 29 standard visible `finditem` slots, consisting of 28 TMs
and HM07. Map, bank/number, object count, local id, coordinate, elevation,
movement/range, script and flag all match. There are no extra NatDex TM slots,
no missing local slots, and no coordinate, script or flag differences.

NatDex uses
`OBJ_EVENT_GFX_UNUSED_MALE_RECEPTIONIST` (numeric ID `67`) for exactly the 28
TM slots, but its HM07 object in `FourIsland_IcefallCave_1F` uses the normal
`OBJ_EVENT_GFX_ITEM_BALL` (ID `92`). This difference is consciously accepted:
the project policy is that all 29 visible TM/HM Field Item slots, including
HM07, use the existing gold CFRU ball. HM07 changes only its Object Graphics
ID from `0x005C` to `0x065C`; item, `finditem` script, flag, pickup behavior
and preserve-only randomizer policy remain unchanged.

NatDex ID `67` is reference evidence only. It must not be copied into CFRU.
The CFRU contract remains exactly gold ID `0x065C`, low byte `0x5C` / `92`,
table `6`, index `92`, and palette `0x1106`.

## Live and pin state

- Workspace PR #464 is merged into `main` as `1d805e4`; it contains the
  existing workspace pin `e63625392ac54c7e460f8b8c2de744b168e02c1f`.
- CFRU PR #34 is merged into `compat/firered-gen9-randomizer` as
  `8927ba7a`; candidate `e6362539` is its first-parent feature commit.
- Thus Workspace `main` does **not** pin the merged CFRU Compat commit. This
  is an open, separate submodule-pin cleanup only; this analysis changes no
  pin or external checkout.

## Exact 29-slot inventory

`CFRU base` is the source object value before an overlay (`0x005C`) and
`target` is the proposed rollout value. The existing one-slot TM09 overlay is
already `0x065C`; all other rows currently have no graphics replacement.
`67` means NatDex's reception-graphic identifier, not a CFRU target.

| Item | Map ID / name | B/N | Obj | LID | XY / E | movement / range | Script | Flag | NatDex gfx | CFRU base -> target |
|---|---|---:|---:|---:|---|---|---|---|---:|---|
| TM09 | `MAP_MT_MOON_1F` / MtMoon_1F | 1/1 | 14 | 9 | 11,35 / 3 | FACE_DOWN / 1,1 | `MtMoon_1F_EventScript_ItemTM09` | `FLAG_HIDE_MT_MOON_1F_TM09` | 67 | `0x005C -> 0x065C` |
| TM46 | `MAP_MT_MOON_B2F` / MtMoon_B2F | 1/3 | 11 | 9 | 35,5 / 3 | FACE_DOWN / 1,1 | `MtMoon_B2F_EventScript_ItemTM46` | `FLAG_HIDE_MT_MOON_B2F_TM46` | 67 | `0x005C -> 0x065C` |
| TM05 | `MAP_ROUTE4` / Route4 | 3/22 | 7 | 3 | 67,5 / 3 | FACE_DOWN / 1,1 | `Route4_EventScript_ItemTM05` | `FLAG_HIDE_ROUTE4_TM05` | 67 | `0x005C -> 0x065C` |
| TM45 | `MAP_ROUTE24` / Route24 | 3/43 | 8 | 8 | 11,4 / 3 | FACE_DOWN / 1,1 | `Route24_EventScript_ItemTM45` | `FLAG_HIDE_ROUTE24_TM45` | 67 | `0x005C -> 0x065C` |
| TM43 | `MAP_ROUTE25` / Route25 | 3/44 | 13 | 10 | 26,2 / 3 | FACE_DOWN / 1,1 | `Route25_EventScript_ItemTM43` | `FLAG_HIDE_ROUTE25_TM43` | 67 | `0x005C -> 0x065C` |
| TM31 | `MAP_SSANNE_1F_ROOM2` / SSAnne_1F_Room2 | 1/13 | 4 | 4 | 5,7 / 3 | FACE_DOWN / 1,1 | `SSAnne_1F_Room2_EventScript_ItemTM31` | `FLAG_HIDE_SSANNE_1F_ROOM2_TM31` | 67 | `0x005C -> 0x065C` |
| TM44 | `MAP_SSANNE_B1F_ROOM2` / SSAnne_B1F_Room2 | 1/25 | 2 | 2 | 3,2 / 3 | FACE_DOWN / 1,1 | `SSAnne_B1F_Room2_EventScript_ItemTM44` | `FLAG_HIDE_SSANNE_B1F_ROOM2_TM44` | 67 | `0x005C -> 0x065C` |
| TM40 | `MAP_ROUTE9` / Route9 | 3/27 | 12 | 11 | 12,17 / 3 | FACE_DOWN / 1,1 | `Route9_EventScript_ItemTM40` | `FLAG_HIDE_ROUTE9_TM40` | 67 | `0x005C -> 0x065C` |
| TM12 | `MAP_ROCKET_HIDEOUT_B2F` / RocketHideout_B2F | 1/43 | 5 | 4 | 5,7 / 3 | FACE_DOWN / 1,1 | `RocketHideout_B2F_EventScript_ItemTM12` | `FLAG_HIDE_ROCKET_HIDEOUT_B2F_TM12` | 67 | `0x005C -> 0x065C` |
| TM21 | `MAP_ROCKET_HIDEOUT_B3F` / RocketHideout_B3F | 1/44 | 5 | 4 | 19,14 / 3 | FACE_DOWN / 1,1 | `RocketHideout_B3F_EventScript_ItemTM21` | `FLAG_HIDE_ROCKET_HIDEOUT_B3F_TM21` | 67 | `0x005C -> 0x065C` |
| TM49 | `MAP_ROCKET_HIDEOUT_B4F` / RocketHideout_B4F | 1/45 | 9 | 7 | 1,6 / 3 | FACE_DOWN / 1,1 | `RocketHideout_B4F_EventScript_ItemTM49` | `FLAG_HIDE_ROCKET_HIDEOUT_B4F_TM49` | 67 | `0x005C -> 0x065C` |
| TM48 | `MAP_ROUTE12` / Route12 | 3/30 | 14 | 10 | 18,36 / 3 | FACE_DOWN / 1,1 | `Route12_EventScript_ItemTM48` | `FLAG_HIDE_ROUTE12_TM48` | 67 | `0x005C -> 0x065C` |
| TM18 | `MAP_ROUTE15` / Route15 | 3/33 | 14 | 11 | 20,6 / 3 | FACE_DOWN / 1,1 | `Route15_EventScript_ItemTM18` | `FLAG_HIDE_ROUTE15_TM18` | 67 | `0x005C -> 0x065C` |
| TM11 | `MAP_SAFARI_ZONE_EAST` / SafariZone_East | 1/64 | 4 | 3 | 31,18 / 3 | FACE_DOWN / 1,1 | `SafariZone_East_EventScript_ItemTM11` | `FLAG_HIDE_SAFARI_ZONE_EAST_TM11` | 67 | `0x005C -> 0x065C` |
| TM47 | `MAP_SAFARI_ZONE_NORTH` / SafariZone_North | 1/65 | 3 | 2 | 28,9 / 3 | FACE_DOWN / 1,1 | `SafariZone_North_EventScript_ItemTM47` | `FLAG_HIDE_SAFARI_ZONE_NORTH_TM47` | 67 | `0x005C -> 0x065C` |
| TM32 | `MAP_SAFARI_ZONE_WEST` / SafariZone_West | 1/66 | 4 | 2 | 17,13 / 3 | FACE_DOWN / 1,1 | `SafariZone_West_EventScript_ItemTM32` | `FLAG_HIDE_SAFARI_ZONE_WEST_TM32` | 67 | `0x005C -> 0x065C` |
| TM01 | `MAP_SILPH_CO_5F` / SilphCo_5F | 1/51 | 9 | 7 | 1,18 / 3 | FACE_DOWN / 1,1 | `SilphCo_5F_EventScript_ItemTM01` | `FLAG_HIDE_SILPH_CO_5F_TM01` | 67 | `0x005C -> 0x065C` |
| TM08 | `MAP_SILPH_CO_7F` / SilphCo_7F | 1/53 | 11 | 11 | 30,11 / 3 | FACE_DOWN / 1,1 | `SilphCo_7F_EventScript_ItemTM08` | `FLAG_HIDE_SILPH_CO_7F_TM08` | 67 | `0x005C -> 0x065C` |
| TM17 | `MAP_POWER_PLANT` / PowerPlant | 1/95 | 8 | 2 | 40,22 / 3 | FACE_DOWN / 1,1 | `PowerPlant_EventScript_ItemTM17` | `FLAG_HIDE_POWER_PLANT_TM17` | 67 | `0x005C -> 0x065C` |
| TM25 | `MAP_POWER_PLANT` / PowerPlant | 1/95 | 8 | 3 | 46,37 / 3 | FACE_DOWN / 1,1 | `PowerPlant_EventScript_ItemTM25` | `FLAG_HIDE_POWER_PLANT_TM25` | 67 | `0x005C -> 0x065C` |
| TM14 | `MAP_POKEMON_MANSION_B1F` / PokemonMansion_B1F | 1/62 | 6 | 4 | 23,4 / 3 | FACE_DOWN / 1,1 | `PokemonMansion_B1F_EventScript_ItemTM14` | `FLAG_HIDE_POKEMON_MANSION_B1F_TM14` | 67 | `0x005C -> 0x065C` |
| TM22 | `MAP_POKEMON_MANSION_B1F` / PokemonMansion_B1F | 1/62 | 6 | 1 | 6,21 / 3 | FACE_DOWN / 1,1 | `PokemonMansion_B1F_EventScript_ItemTM22` | `FLAG_HIDE_POKEMON_MANSION_B1F_TM22` | 67 | `0x005C -> 0x065C` |
| TM02 | `MAP_VICTORY_ROAD_1F` / VictoryRoad_1F | 1/39 | 7 | 4 | 14,1 / 3 | FACE_DOWN / 1,1 | `VictoryRoad_1F_EventScript_ItemTM02` | `FLAG_HIDE_VICTORY_ROAD_1F_TM02` | 67 | `0x005C -> 0x065C` |
| TM07 | `MAP_VICTORY_ROAD_2F` / VictoryRoad_2F | 1/40 | 13 | 7 | 40,7 / 3 | FACE_DOWN / 1,1 | `VictoryRoad_2F_EventScript_ItemTM07` | `FLAG_HIDE_VICTORY_ROAD_2F_TM07` | 67 | `0x005C -> 0x065C` |
| TM37 | `MAP_VICTORY_ROAD_2F` / VictoryRoad_2F | 1/40 | 13 | 9 | 14,13 / 3 | FACE_DOWN / 1,1 | `VictoryRoad_2F_EventScript_ItemTM37` | `FLAG_HIDE_VICTORY_ROAD_2F_TM37` | 67 | `0x005C -> 0x065C` |
| TM50 | `MAP_VICTORY_ROAD_3F` / VictoryRoad_3F | 1/41 | 12 | 6 | 12,9 / 3 | FACE_DOWN / 1,1 | `VictoryRoad_3F_EventScript_ItemTM50` | `FLAG_HIDE_VICTORY_ROAD_3F_TM50` | 67 | `0x005C -> 0x065C` |
| HM07 | `MAP_FOUR_ISLAND_ICEFALL_CAVE_1F` / FourIsland_IcefallCave_1F | 1/111 | 2 | 2 | 12,16 / 3 | FACE_DOWN / 1,1 | `FourIsland_IcefallCave_1F_EventScript_ItemHM07` | `FLAG_HIDE_FOUR_ISLAND_ICEFALL_CAVE_1F_HM07` | **92** | `0x005C -> 0x065C` |
| TM36 | `MAP_FIVE_ISLAND_ROCKET_WAREHOUSE` / FiveIsland_RocketWarehouse | 1/114 | 10 | 8 | 17,3 / 0 | FACE_DOWN / 1,1 | `FiveIsland_RocketWarehouse_EventScript_ItemTM36` | `FLAG_HIDE_FIVE_ISLAND_ROCKET_WAREHOUSE_TM36` | 67 | `0x005C -> 0x065C` |
| TM41 | `MAP_SILPH_CO_4F` / SilphCo_4F | 1/50 | 8 | 8 | 30,18 / 0 | FACE_DOWN / 1,1 | `SilphCo_4F_EventScript_ItemTM41` | `FLAG_HIDE_SILPH_CO_4F_TM41` | 67 | `0x005C -> 0x065C` |

All rows have `TRAINER_TYPE_NONE` / trainer range `0`. The two elevation-0
rows are TM36 and TM41; the Sevii rows are HM07 and TM36.

## Exclusions and differences

- Dedicated NatDex graphic: 28 TM rows yes; HM07 no. This is the sole NatDex
  difference and is an explicitly accepted CFRU policy, not a blocker.
- Additional NatDex TM slots: none. The complete NatDex reception-graphic
  scan returns the same 28 TMs and no non-TM/HM source.
- Missing local slots, coordinates, scripts or flags: none.
- Standard-ball lookalikes are excluded: three Oak Lab starter balls, the
  Eevee ball, two Fighting Dojo choice balls, two Power Plant Electrode
  encounters, Silph Scope and Lift Key. Their scripts are starter/gift/battle
  or special-item flows, not the whitelist's `finditem ITEM_TMxx/HM07` shape.
- NPC gifts, Gym TMs, shops, Hidden Items and every non-object source are
  outside the overlay. No starter ball, Electrode, Eevee, Silph Scope or Lift
  Key is a rollout row.

## CFRU implementation assessment

The merged CFRU implementation already reuses the gold graphics unchanged:
`MAP_OBJ_GFX_GOLD_TM_ITEM_BALL == 0x065C`, table `6`, `[92]`, palette
`0x1106`, 16x16, one frame and inanimate. `GetEventObjectGraphicsId()`
reconstructs the upper/lower-byte id; UPR-FVX still sees lower byte `92`.

`replace_graphics` parses each overlay line independently and can operationally
process multiple rows. Its present self-test is deliberately pilot-shaped: it
asserts exactly one `replace_graphics` row. A rollout must change that
self-test to validate all 28/29 expected lines and prove each serialized
before/after template changes only byte 3, while preserving object count and
warp/coord/BG pointers. This is not an overlay limitation; it is a necessary
fail-closed rollout hardening task.

## Approved 29-slot rollout handoff

The policy permits all 29 rows. The only later CFRU changes are:

1. add one `replace_graphics` row per approved whitelist entry to
   `mapobjectoverlays`, with the exact table above and `0x005C -> 0x065C`;
2. extend `scripts/insert.py --check-map-object-overlays` from its one-row
   assertion to a complete ordered whitelist/self-test and assert all controls
   and non-object pointers remain byte-identical;
3. update the rollout smoke document with static, randomizer and runtime
   evidence; do not add graphics, palettes, UPR-FVX or DPE changes.

The existing graphics resource is reused. No new graphics resource or palette
work, runtime hook or randomizer graphics writer is needed.
