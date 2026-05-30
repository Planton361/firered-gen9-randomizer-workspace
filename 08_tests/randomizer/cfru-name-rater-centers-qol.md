# CFRU Name Rater Pokecenter pilot

Status: `MVP_PASS_WITH_CAVEATS`

## Manual smoke result - 2026-05-30

Branch: `test/cfru-map-object-overlay-viridian-smoke`

Sanitized user-reported result:

- Clean-build was run in the local Mac CFRU build checkout.
- The added Name Rater became visible only after running
  `python3 scripts/clean.py BUILD` followed by `python3 scripts/make.py`.
- Viridian City Pokecenter 1F was entered fresh from outside the map.
- No ROM name, hash, save, screenshot, raw log, private path or generated
  artifact detail is included.

Smoke matrix:

| Case | Result |
|---|---|
| Clean build with `clean.py BUILD` plus `make.py` | pass |
| Viridian Pokecenter loads | pass |
| Viridian Pokecenter entered from outside | pass |
| Added Name Rater NPC visible | pass |
| Nurse works | pass |
| PC works | pass |
| Existing NPCs remain present and interactable | pass |
| Name Rater `No` path works | pass |
| Nickname screen opens | pass |
| Nickname cancel path works | pass |
| Nickname confirm / rename path works | pass |
| No visible Runtime Options side effect | pass |
| No visible Field Item side effect | pass |
| No visible randomizer-output side effect | pass |
| Egg rejection path | not run |
| Traded/non-player-OT rejection path | not run |
| Broader Pokecenter rollout | not run |

Result decision: the Viridian-only overlay MVP is accepted as
`MVP_PASS_WITH_CAVEATS`.

Caveats:

- Manual smoke only; no automated test or full playthrough.
- Egg and traded-mon rejection paths were not run in this result.
- No claim is made for additional Pokecenters, rollout readiness, BizHawk,
  Ironmon Tracker, P1 support, Hidden Items, itemball graphics, Field Items or
  Randomizer writer behavior beyond the targeted visible side-effect check.

## Smoke fail debug - 2026-05-30

Branch: `debug/cfru-name-rater-overlay-smoke-fail`

User-reported result: after locally rebuilding and starting the current CFRU
compat candidate, no visible or interactable Name Rater was found in Viridian
City Pokecenter 1F.

Read-only source diagnosis found:

- Workspace `main` contains PR #452.
- Workspace submodule pin points to CFRU compat merge
  `f40a35a295ce23294557f19dfff220240056386f`.
- CFRU local branch is `compat/firered-gen9-randomizer` at the same commit.
- `scripts/make.py` calls `scripts/build.py` and then `scripts/insert.py`.
- `scripts/insert.py` does call `InsertMapObjectOverlays(...)`; the overlay
  function is not dead code.
- The overlay call runs after existing `eventscripts` pointer repoints and
  before song pointer insertion. No later source-backed map-event writer was
  found in `insert.py`.
- `MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F` is map bank `5`, map number `4`.
- The pret Viridian Pokecenter 1F reference has object count `4`, matching the
  overlay's expected count.
- The requested added object row/local-id model remains correct: appended row
  `4`, local id `5`.
- `MAP_OBJ_GFX_GENTLEMAN`, coordinate `(10, 5)`, elevation `3`, and
  `MOVEMENT_TYPE_FACE_DOWN` resolve to normal object-template fields.
- The `1 1 0 0` fields are movement range `1, 1`, trainer type `0`, and
  trainer range `0`; they are not visibility flags.
- The object-template byte layout in `BuildEventObjectTemplate` matches the
  local CFRU `EventObjectTemplate` layout and the pret `object_event` macro
  shape for the fields used by this MVP.
- `assembly/overworld_scripts/name_rater_pokecenter.s` and
  `strings/Scripts/name_rater_pokecenter.string` are under the recursive
  `scripts/build.py` assembly/string globs.
- The script and text symbols are internally consistent in source.

No small source-backed code defect was identified in this pass.

Local generated build intermediates needed to verify concrete linked symbols
and inserted output were not present in this checkout, so the final ROM/output
state was not inspected. No ROM, save, emulator state, screenshot, raw log,
hash, private path or build artifact is documented here.

Debug decision: no CFRU code change in this branch. Treat the current failure
as blocked pending a clean rebuild and map-reload smoke from the CFRU root.

Clean rebuild / smoke handoff:

1. From `02_external/CFRU-expansion`, confirm branch
   `compat/firered-gen9-randomizer` and commit
   `f40a35a295ce23294557f19dfff220240056386f`.
2. Remove stale generated build/intermediate outputs locally if present.
3. Run `python3 scripts/make.py` from the CFRU root, not only
   `scripts/build.py`.
4. Load the newly inserted local output, not an older candidate.
5. Enter Viridian City Pokecenter 1F from outside the map after the new output
   is loaded; do not rely on an emulator state already inside the map.
6. Check for the added Gentleman-like Name Rater at `(10, 5)`.
7. If still absent, the next debug block should verify the inserted
   `MapHeader.events` pointer and generated object count from a sanitized
   local inspection path, without documenting ROM names, hashes, private paths
   or raw binary dumps.

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

CFRU feature commit: `648ce6042a93b71796c2d478fc816687e2ec060a`

CFRU compat merge commit pinned by the final Workspace PR:
`f40a35a295ce23294557f19dfff220240056386f`

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
