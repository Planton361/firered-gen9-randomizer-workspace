# CFRU National Dex Workspace integration — 2026-09-29

**Evidence classification:** CONFIRMED CURRENT STATE, limited to the exact revisions and ROM-free checks below.

## Revision basis

- Workspace base: `003b3af696168d226ca7800031e174fd4b00189e`
- Workspace branch: `integration/cfru-national-dex-pin`
- Workspace pin commit / verification head: `e374a49e9dbdc7a1ab5bcecad9e884393059efc7`
- CFRU Gitlink: `ec4e1b7410a65b23e081010c580ecb8c078a64a1` → `818f65090b1af2b60287f9dbc60302c2b27ac404`
- Accepted CFRU #549 head: `974f203f2feac10dafee86bb6b781f1c147e248b`
- CFRU #59 merged revision: `818f65090b1af2b60287f9dbc60302c2b27ac404`

CFRU PR #59 is merged into `compat/firered-gen9-randomizer`. The merge commit has the previous CFRU pin and accepted #549 head as its parents; the accepted head is its first parent. The accepted-head-to-merge range contains one commit, and `git diff --quiet 974f203f2feac10dafee86bb6b781f1c147e248b 818f65090b1af2b60287f9dbc60302c2b27ac404` reports identical trees. The live compat branch resolves to the merged revision.

The exact-pin checks below ran with the Workspace Gitlink staged at the target. Workspace commit `e374a49e9dbdc7a1ab5bcecad9e884393059efc7` records that pin; the evidence-file commit follows it without changing the pin.

## Workspace scope and Gitlinks

The final Workspace PR diff contains exactly:

1. `02_external/CFRU-expansion`
2. `docs/testing/cfru-national-dex-workspace-integration-2026-09-29.md`

The recursive Gitlink diff against the Workspace base contains one mode-`160000` change: CFRU from `ec4e1b7410a65b23e081010c580ecb8c078a64a1` to `818f65090b1af2b60287f9dbc60302c2b27ac404`.

Every other Gitlink matches the Workspace base:

| Path | Unchanged pin |
|---|---|
| `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| `02_external/Ironmon-Tracker` | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| `02_external/NatDexExtension` | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| `02_external/references/cyansmp64-pokefirered-natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| `02_external/references/cyansmp64-upr-zx-natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` |
| `02_external/references/pret-pokefirered` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |
| `02_external/references/upr-fvx-upstream` | `e0788edc6529c2605f201996e4807ff30165354c` |
| `02_external/references/upr-zx-ajarmar` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` |
| `02_external/upr-fvx` | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` |

## Exact-pin ROM-free gates

All commands ran from the CFRU checkout at `818f65090b1af2b60287f9dbc60302c2b27ac404`.

| Gate | Command | Result |
|---|---|---|
| M-007 National-Dex handoff audit | `python3 scripts/tests/audit_m007_national_dex_handoff.py` | PASS; named special is `0x016F`, appears once, and the handoff order is preserved. Fresh New Game, save/ABI/layout, and M-007 scope assertions passed. |
| M-007 insertion / Parcel checks | `python3 scripts/insert.py --check-map-object-overlays` | PASS; shortened Oak Parcel Flow map-event and script checks passed. This check mode does not open or insert a ROM. |
| Early Running | `python3 scripts/tests/run_early_running_pewter_tests.py` | PASS; lifecycle/Pewter audit and insertion checks passed. |
| Settings defaults | `python3 scripts/tests/run_settings_defaults_tests.py` | PASS; source audit and temporary host tests passed; temporary host objects were deleted. |
| Standard AI | `python3 scripts/tests/run_standard_ai_tests.py` | PASS; policy, fairness, mechanics, dispatch, layout, and save-delta checks passed. |
| Ironmon AI | `python3 scripts/tests/run_ironmon_ai_tests.py` | PASS; source/fairness checks, 63/63 parity fixtures, all 58 mandatory tags, and accepted digests passed. |
| Full source build | `python3 scripts/build.py` | PASS; complete source build and its writable-state audit completed. The linker emitted an RWX `LOAD` segment warning. No tools were installed or downloaded. |
| CFRU commit-range whitespace | `git diff --check ec4e1b7410a65b23e081010c580ecb8c078a64a1 818f65090b1af2b60287f9dbc60302c2b27ac404` | PASS. |
| Workspace safety | `python3 07_scripts/bootstrap/check_git_safety.py` | PASS before the pin change and after staging it. |

## Preserved behavior and boundaries

- `SPECIAL_ENABLE_NATIONAL_POKEDEX` binds once to `0x016F`; exactly one National-Dex special call appears in the Pallet Oak handoff.
- The M-007 order remains Parcel removal → ordinary Pokédex-get flag → `0x0181` unlocked-Pokédex special → `0x016F` National-Dex special → five Poké Balls → existing story transitions.
- Fresh New Game remains unchanged and does not activate National Dex.
- No direct function-address call, direct or partial National-Dex state write, or substitute setter was introduced.
- CFRU #59 changes only the M-007 assembly script, its insertion/Parcel self-check, and the focused ROM-free audit. No save, ABI, or layout source changed.
- No DPE, UPR-FVX, Tracker, NatDexExtension, or reference Gitlink changed. #550, #546, and #547 were not implemented.
- No ROM, save, emulator state, finalized ROM build, private artifact, secret, or `.env` was used or requested. The required source build generated its source-build outputs; they were not separately opened or used as agent inputs. No protected-input insertion or runtime test was performed.

This is source, host-test, and full source-build evidence only. It does not claim ROM insertion or runtime acceptance.
