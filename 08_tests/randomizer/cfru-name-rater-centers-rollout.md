# CFRU Name Rater Pokecenter rollout smoke handoff

Status: `IMPLEMENTED_PENDING_MANUAL_SMOKE`

## Implementation candidate - safe Kanto batch 1

Branch: `feature/cfru-name-rater-centers-rollout-kanto-1`

CFRU Draft PR: `https://github.com/Planton361/CFRU-expansion/pull/26`

Implemented in CFRU `mapobjectoverlays` only:

| Map | Bank | Map | Expected count | New local id | Coordinate | Script | Result |
|---|---:|---:|---:|---:|---|---|---|
| `CeladonCity_PokemonCenter_1F` | 10 | 12 | 4 | 5 | `(10, 5)` | `EventScript_PokeCenterNameRater` | pending smoke |
| `FuchsiaCity_PokemonCenter_1F` | 11 | 5 | 4 | 5 | `(10, 5)` | `EventScript_PokeCenterNameRater` | pending smoke |
| `LavenderTown_PokemonCenter_1F` | 8 | 0 | 5 | 6 | `(10, 5)` | `EventScript_PokeCenterNameRater` | pending smoke |
| `Route10_PokemonCenter_1F` | 21 | 0 | 5 | 6 | `(10, 5)` | `EventScript_PokeCenterNameRater` | pending smoke |
| `Route4_PokemonCenter_1F` | 16 | 0 | 6 | 7 | `(10, 5)` | `EventScript_PokeCenterNameRater` | pending smoke |
| `SaffronCity_PokemonCenter_1F` | 14 | 6 | 6 | 7 | `(10, 5)` | `EventScript_PokeCenterNameRater` | pending smoke |

Existing Viridian overlay entry remains unchanged and is not re-smoked by this
candidate.

Skipped by design in this batch:

- high-count Kanto: Cerulean, Cinnabar, Pewter, Vermilion;
- special layout: Indigo Plateau;
- Sevii centers: Two, Three, Four, Five, Six, Seven Island;
- One Island.

Manual smoke is required before promoting this batch. Use the clean-build and
fresh-map-entry rules below for every implemented map.

## Purpose

This file gates a future rollout of added Name Rater NPCs to Pokecenter 1F
maps. It is based on the passed Viridian overlay MVP and the rollout inventory
in `01_docs/analysis/cfru-name-rater-centers-rollout.md`.

No CFRU, DPE, UPR-FVX, rollout code, ROM, binary patch, build artifact, save,
emulator state, screenshot, raw log, private path, token, secret or `.env` data
is included.

## Global smoke rules

For any rollout implementation:

1. Start from the CFRU root.
2. Run a clean build with `python3 scripts/clean.py BUILD`.
3. Run `python3 scripts/make.py`.
4. Load the newly inserted local candidate.
5. Enter each target Pokecenter from outside the map.
6. Do not use an emulator state already inside the target map for first proof.
7. Record only sanitized pass/fail/not-run rows.

## Required per-map checks

For every added Name Rater map:

| Case | Required result |
|---|---|
| Map loads after fresh entry | pass |
| Added Name Rater NPC is visible once | pass |
| Added Name Rater NPC is interactable | pass |
| Name Rater `No` path exits cleanly | pass |
| Nickname screen opens for eligible player-owned mon | pass |
| Nickname cancel returns field control | pass |
| Nickname confirm applies changed nickname | pass |
| Nurse healing still works | pass |
| PC still opens normally | pass |
| Existing NPCs remain present and interactable | pass |
| Door and upstairs warps remain correct | pass |
| No visible Runtime Options side effect | pass |
| No visible Field Item side effect | pass |
| No visible randomizer-output side effect | pass |
| Egg rejection path | optional until specifically available |
| Traded/non-player-OT rejection path | optional until specifically available |

## Extra gates by risk group

Safe Kanto batch:

- Include all standard per-map checks.
- Confirm each map's expected object count changed only by one added object.
- Confirm no existing local id is reused.

High-count Kanto maps:

- Confirm all original visible NPCs remain present.
- Confirm invisible Pokemon Journal or service objects still behave as before
  when applicable.
- Confirm the added local id does not exceed the active-object runtime budget.

Special layout maps:

- For `IndigoPlateau_PokemonCenter_1F`, confirm League room warp, exterior
  warp, clerk, door guard, nurse and PC behavior separately.

Sevii maps:

- Smoke after the relevant map is reachable in a normal progression state.
- Confirm travel/story NPCs remain intact where present.
- Do not combine all Sevii maps into the first rollout.

Coord/BG-event maps:

- For `FourIsland_PokemonCenter_1F`, confirm Pokemon Journal BG signs still
  work.
- For `OneIsland_PokemonCenter_1F`, confirm Bill, Celio, Network Machine BG
  events and leave-island coord triggers are preserved.
- Treat One Island as the final rollout candidate, not a first batch map.

## Suggested rollout order

1. Safe Kanto batch: Celadon, Fuchsia, Lavender, Route 10, Route 4, Saffron.
2. High-count Kanto proof: one of Cerulean, Pewter, Vermilion or Cinnabar.
3. Special layout proof: Indigo Plateau.
4. Sevii low-risk batch: Two, Three, Five, Six, Seven Island.
5. BG/coord proof: Four Island, then One Island last.

Each phase should get its own clean-build smoke result before the next phase is
implemented.

## Stop conditions

Stop and open a design/debug handoff if:

- any existing NPC is replaced instead of an appended object being added;
- expected original object count mismatch occurs;
- a fixed raw address, ROM edit or binary patch is needed;
- warp, coord or BG event pointers are rewritten instead of preserved;
- UPR-FVX, DPE, Field Items, Hidden Items, itemball graphics or Randomizer
  writer code would be touched;
- a local build requires documenting ROM names, hashes, saves, screenshots,
  raw logs, private paths, tool binary paths, secrets, tokens or `.env` data.
