# CFRU TM/HM itemball rollout smoke handoff

Date: 2026-07-13

Status: `M001_CANDIDATE_ACCEPTANCE_ACTIVE`

## M-001 candidate and acceptance boundary

**CONFIRMED CURRENT STATE:** The workspace pins CFRU candidate
`08b869032735118539411adbcffa421c8a697caa`. CFRU PR #35 is the active product
candidate. No final acceptance or product merge is claimed in this bootstrap.

**LEGACY / OBSOLETE:** Workspace PR #467 is closed unmerged. Its branch and
commit are supporting handoff evidence only; it is not the active integration
PR.

**CONFIRMED CURRENT STATE:** Static overlay, generator, build, and insertion
gates passed for this candidate. The runtime and fresh candidate-specific
six-row UPR-FVX gates below remain mandatory.

## Accepted 29-slot policy

NatDex uses its dedicated graphic for all 28 TM balls but leaves HM07 as
`OBJ_EVENT_GFX_ITEM_BALL`. The project consciously accepts that structural-only
reference divergence: HM07 also receives the gold CFRU ball. Never copy NatDex
graphics ID `67` into CFRU; every one of the 29 rows targets `0x065C` (table 6,
low byte 92, palette `0x1106`).

HM07 changes only Object Graphics ID. Its item, `finditem` script, flag,
pickup behavior and preserve-only randomizer policy remain unchanged. Existing
gold graphics and palette registration are reused; no extra graphics or palette
work is needed.

Seven rows have no suitable same-map normal `finditem` control ball. They are
source-backed target-only exceptions, not missing or invented controls: TM05
Route4, TM45 Route24, TM43 Route25, TM31 SSAnne 1F Room2, TM44 SSAnne B1F
Room2, TM18 Route15, and TM32 Safari Zone West. Every target retains its own
exact object/script/item/flag validation.

When unblocked, every selected row must preserve its existing object count,
local id, coordinate, elevation, movement/range, `finditem` script and flag as
listed in `01_docs/analysis/cfru-tm-itemball-natdex-parity.md`.

## Required static gate

- [x] `mapobjectoverlays` contains exactly the policy-approved whitelist;
  no starter ball, Electrode, Eevee, Silph Scope, Lift Key, NPC/gift/Gym TM,
  shop or Hidden Item is included.
- [x] Each row has source value `0x005C`, target `0x065C`, low byte `92`, and
  an exact target/control expectation.
- [x] `scripts/insert.py --check-map-object-overlays` proves every replacement
  changes only the graphics upper byte; all counts and warp/coord/BG pointers
  are preserved. The current one-row self-test must become a multiple-row
  whitelist test.
- [x] CFRU `git diff --check`, Python syntax check, full link and clean
  insertion pass without generated or private artifacts.

## Runtime spotcheck matrix

This is intentionally not 29 full playthroughs. Use a freshly built candidate,
an in-game save (not a savestate), and record only sanitized results.

| Case | Slot | Required observations |
|---|---|---|
| Existing pilot | TM09, MtMoon_1F, 1/1, LID 9 | Gold object, normal Potion control LID 10, pickup, original flags, both pickup orders, re-entry and save/reload. |
| Early Kanto | TM05, Route4, 3/22, LID 3 | Gold object, `finditem` reward, original flag and map transition remain correct. |
| Elevation 0 | TM41, SilphCo_4F, 1/50, LID 8 | Gold object at elevation 0, pickup/removal and map event behavior correct. |
| HM07 | FourIsland_IcefallCave_1F, 1/111, LID 2 | Gold object, preserved HM07 reward, original flag, pickup/removal and re-entry. |
| Sevii TM | TM36, FiveIsland_RocketWarehouse, 1/114, LID 8 | Gold object at elevation 0, pickup/removal, flag and map transition correct. |
| Normal control | Any nearby non-TM `OBJ_EVENT_GFX_ITEM_BALL` | Remains red/white, retains normal reward/flag, no palette or sprite corruption. |

For every case, also check player/NPC/environment palettes, no sprite/tile loss,
and no warp/trainer/object-event regression.

## Current user-reported runtime evidence

**CONFIRMED CURRENT STATE:** The user reports correct TM/HM-versus-normal-ball
color behavior, pickup/removal, map re-entry, in-game save/reload, and no
sprite/tile/palette corruption.

**UNKNOWN:** Representative-slot coverage is pending confirmation. The report
does not identify which required matrix slots were exercised, so no matrix row
is silently marked complete.

## Separate automated UPR-FVX gate

The six rows remain mandatory and separate from visual runtime acceptance. Each
uses a fresh candidate and fresh randomized output:

| Mode | Ban Bad | Required result |
|---|---|---|
| Unchanged | off | TM slot remains TM; normal control remains non-TM; reload counters zero. |
| Shuffle | off | Same, with required-TM set preserved and reload counters zero. |
| Random | off | Same; required Field TMs missing = 0; reload counters zero. |
| Random | on | Same; required Field TMs missing = 0; reload counters zero. |
| Random Even | off | Same; required Field TMs missing = 0; reload counters zero. |
| Random Even | on | Same; required Field TMs missing = 0; reload counters zero. |

All six require `rawApiTmSlotAlignmentMismatches=0`,
`tmFieldItemSlotMismatches=0`, `nonTmFieldItemSlotMismatches=0`,
`requiredFieldTMMissingAfter=0`, `fieldItemReloadMismatches=0`, and successful
discovery through low byte `92`.
