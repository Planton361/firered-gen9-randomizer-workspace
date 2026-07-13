# CFRU TM/HM itemball visual pilot smoke

Date: 2026-07-13

Status: `PILOT_PENDING_MANUAL_SMOKE`

## Purpose

This is the smoke handoff for the implemented CFRU-only first pilot. CFRU branch
`feature/cfru-tm-itemball-visual-pilot`, commit
`e63625392ac54c7e460f8b8c2de744b168e02c1f` and Draft PR
<https://github.com/Planton361/CFRU-expansion/pull/34> contain the candidate.
No runtime pass is claimed. ROMs, saves, states, screenshots, builds and
generated artifacts remain local and uncommitted.

Pilot:

- gold TM ball: MtMoon_1F, bank `1`, map `1`, local id `9`, `(11, 35)`,
  elevation `3`, TM09 script/flag, expected object count `14`;
- normal control ball: same map, local id `10`, `(26, 32)`, elevation `3`,
  Potion script/flag, expected object count `14`.

## Build and static gates

- [x] CFRU branch starts from Compat merge commit `b1cb855b5432d607ac9162d58541ec90ec8fcfd9`.
- [x] Only files in the design allowlist are changed.
- [x] `git diff --check` passes.
- [x] Syntax-only compile passes for every changed C file.
- [x] `python3 scripts/build.py` links the complete CFRU source.
- [x] The normal local clean-build flow passes:
  `python3 scripts/clean.py BUILD` followed by `python3 scripts/make.py`.
- [x] No ROM, save, state, screenshot, build output or generated tool artifact is
  staged.
- [x] New graphics id is exactly `0x065C`: upper table `6`, lower byte `92`.
- [x] Table index `6` was free before registration and `[92]` is in bounds.
- [x] The new GraphicsInfo is 16x16, inanimate, one frame, regular Object Event
  OAM/subsprite lifecycle.
- [x] Palette tag remains the existing static `0x1106`; no palette load/free
  calls and no new palette slot exist.
- [x] Generator proves object count/local id/coordinate/elevation/movement/range,
  vanilla full graphics id, script shape, flag and unchanged control object.
- [x] Serialized target differs only in graphics-id upper byte; the lower byte
  remains `92`.

The generator check is `python3 scripts/insert.py --check-map-object-overlays`.
It proves that the only serialized object-table difference is target byte `3`,
that the Potion control is byte-identical, and that object count plus
warp/coord/BG pointers remain unchanged. The real clean insertion also passed
against the local build input. Existing CFRU compiler warnings and the RWX
linker warning remain; no new pilot-specific warning or error was observed.

## UPR-FVX save/reload matrix

Each row uses a newly built candidate and a fresh randomization. Reload the
saved output through the existing sanitized Field Item diagnostics; do not
reuse emulator states from another build.

| Mode | Ban Bad | TM pilot remains a TM slot | Control remains non-TM | Required TMs | Reload mismatches | Expected |
|---|---|---|---|---|---|---|
| Unchanged | off | yes | yes | unchanged | 0 | pass |
| Shuffle | off | yes | yes | unchanged set | 0 | pass |
| Random | off | yes | yes | 0 missing | 0 | pass |
| Random | on | yes | yes | 0 missing | 0 | pass |
| Random Even | off | yes | yes | 0 missing | 0 | pass |
| Random Even | on | yes | yes | 0 missing | 0 | pass |

Required sanitized assertions:

- `rawApiTmSlotAlignmentMismatches=0`
- `tmFieldItemSlotMismatches=0`
- `nonTmFieldItemSlotMismatches=0`
- `requiredFieldTMMissingAfter=0`
- `fieldItemReloadMismatches=0`
- gold pilot is still discovered by the Gen 3 reader despite upper graphics
  byte `6`
- no normal slot receives a TM and no TM slot receives a non-TM

## Runtime matrix

Use an in-game save. Savestates are not acceptance evidence.

| Scenario | Expected result |
|---|---|
| Fresh entry to MtMoon_1F | Map, trainers, warps and all 14 Object Events behave normally. |
| Approach local id 9 | A clearly gold/yellow 16x16 item ball is shown at `(11, 35)`. |
| Approach local id 10 | The existing normal red/white item ball remains at `(26, 32)`. |
| Both balls visible | No OBJ tile failure, sprite loss, flicker or palette corruption. |
| Player/NPC/environment palettes | No color change; gold ball reuses the registered static palette. |
| Pick up TM pilot | Randomized content is a TM; normal pickup text/fanfare, object removal and original flag work. |
| Pick up normal control | Randomized content is non-TM; normal pickup behavior and original flag work. |
| Leave/re-enter | Collected object stays hidden; uncollected object keeps the correct graphic. |
| In-game save/reload | Flags, graphics and randomized contents remain correct. |
| Repeat with opposite pickup order | Each object remains independent. |

## Regression boundary

- [ ] Hidden Items remain invisible and are not in the overlay list.
- [ ] Starter balls, Dojo choice balls, Electrode disguises, Silph Scope, Lift
  Key, Eevee, NPC gifts and shops remain unchanged.
- [ ] Normal visible Field Items on other maps remain the normal ball.
- [ ] Pickup scripts and object flags are unchanged.
- [ ] No runtime item scan, Overworld-frame hook or dynamic palette path exists.
- [ ] UPR-FVX and DPE source remain unchanged.

## Rollout gate

Do not add any second gold slot until every build, UPR save/reload and runtime
row above passes. A later rollout must use the 29-entry source whitelist from
`01_docs/analysis/cfru-tm-itemball-visuals.md` and retain the low-byte-92
contract for every replacement.
