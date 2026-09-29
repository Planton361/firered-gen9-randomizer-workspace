# CFRU Route 10 HM05 Workspace integration — 2026-09-29

**Evidence classification:** CONFIRMED CURRENT STATE for the exact revisions and ROM-free checks below. Runtime behavior remains unverified at this pin.

## Revision basis

- Contract: Workspace Issue #559; CFRU source contract #557; CFRU PR #60.
- Workspace base: `eb1b82eb366d631a1be1dcf2bc3a46e5cd108b92`.
- Workspace branch: `integration/cfru-route10-hm05-pin`.
- Workspace pin commit and exact-pin verification head: `c97249d34a4f8b28d22b4706e295b68e3715fc56`.
- Final delivery branch head: the PR head containing this evidence file; its SHA is recorded in the PR and delivery report. A commit cannot contain its own SHA.
- CFRU Gitlink: `818f65090b1af2b60287f9dbc60302c2b27ac404` → `b17f2e3c5dd0dad89db4d363d9254ef2f97ba9c3`.
- Accepted #557 source head: `08fbe3e0c6c8f8bcb26477f5d9926eed35ecb443`.
- CFRU PR #60 merged revision and current `compat/firered-gen9-randomizer`: `b17f2e3c5dd0dad89db4d363d9254ef2f97ba9c3`.

The CFRU merge commit has first parent `818f65090b1af2b60287f9dbc60302c2b27ac404` and second parent `08fbe3e0c6c8f8bcb26477f5d9926eed35ecb443`. The accepted head is zero commits ahead and one behind the merge. `git diff --quiet` between the accepted head and merge returns success: zero file changes. The live CFRU compat branch resolves to the merge revision.

A separate checkout was reconstructed from GitHub. Its initial Workspace status was clean, its `main` revision and all initialized recursive Gitlinks matched the Issue basis, and `check_git_safety.py --allow-main` passed before the #559 branch was created. The prior dirty checkout was left untouched; the origin or equivalence of its changes remains UNKNOWN.

## Workspace scope and Gitlinks

The PR diff against the Workspace base contains exactly:

1. `02_external/CFRU-expansion`
2. `docs/testing/cfru-route10-hm05-workspace-integration-2026-09-29.md`

The recursive Gitlink diff contains one mode-`160000` change: the CFRU Gitlink above. All other Gitlinks are byte-identical to the Workspace base:

| Path | Unchanged pin |
|---|---|
| `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| `02_external/upr-fvx` | `7bf79ee1e7c46c972f7a9c84942970a950be0723` |
| `02_external/Ironmon-Tracker` | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| `02_external/NatDexExtension` | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| `02_external/references/cyansmp64-pokefirered-natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| `02_external/references/cyansmp64-upr-zx-natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` |
| `02_external/references/pret-pokefirered` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |
| `02_external/references/upr-fvx-upstream` | `e0788edc6529c2605f201996e4807ff30165354c` |
| `02_external/references/upr-zx-ajarmar` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` |

## Exact-pin ROM-free gates

All CFRU commands ran at `b17f2e3c5dd0dad89db4d363d9254ef2f97ba9c3`. The full source build completed without a private ROM or insertion input.

| Gate | Command | Result |
|---|---|---|
| Route 10 HM05 | `python3 scripts/tests/test_route10_hm05.py` | PASS; 6/6 ROM-free tests. |
| Map-object overlays | `python3 scripts/insert.py --check-map-object-overlays` | PASS; legacy overlay and M-007 Parcel checks included. |
| Early Running / Pewter | `python3 scripts/tests/run_early_running_pewter_tests.py` | PASS. |
| Settings defaults | `python3 scripts/tests/run_settings_defaults_tests.py` | PASS; source/host checks and original-raw preservation. |
| Standard AI | `python3 scripts/tests/run_standard_ai_tests.py` | PASS; policy, dispatch, fairness, ABI/layout and save-delta host checks. |
| Ironmon AI | `python3 scripts/tests/run_ironmon_ai_tests.py` | PASS; 63/63 parity fixtures, 58/58 mandatory tags, and accepted Workspace-corpus digests. |
| Full source build | `python3 scripts/build.py` | PASS, exit 0; compiler warnings were emitted. No tool installation or download was performed. |
| CFRU change whitespace | `git diff --check 818f65090b1af2b60287f9dbc60302c2b27ac404 b17f2e3c5dd0dad89db4d363d9254ef2f97ba9c3` | PASS. |
| Workspace whitespace and safety | `git diff --check`; `python3 07_scripts/bootstrap/check_git_safety.py` | PASS. |

The #557 CFRU range changes exactly five source/test paths: `assembly/overworld_scripts/route10_hm05.s`, `mapobjectoverlays`, `scripts/insert.py`, `scripts/tests/test_route10_hm05.py`, and `strings/Scripts/route10_hm05.string`. The historical M-007 changed-path audit is scoped to #549 and was not reported as a #559 PASS; the current overlay self-check covered its relevant Parcel behavior.

## Preserved #557 behavior and boundaries

- Route 10 is map `(3,28)`. The exact pre-counts are `10/5/0/8`, and the intended post-counts are `11/5/0/8`.
- The overlay appends one 24-byte non-trainer Hiker object: local ID 11, graphics `0x38`, coordinates `(17,22)`, hidden by `FLAG_GOT_HM05 = 0x23B`.
- The script checks the shared flag and bag space, awards `ITEM_HM05_FLASH = 343` once, sets the flag, and removes the Hiker. The original Route 2 HM05 source path remains present and unchanged.
- `append_object_exact` resolves the MapHeader and MapEvents pointers during user-owned insertion. It fails closed on any of the four event-count mismatches or invalid source spans/pointers; the synthetic suite checks the byte-identical ten-object prefix and preservation of warp/coord/BG counts and pointers. Legacy overlay actions retain their paths.
- The existing HM eligibility model remains unchanged. This Workspace integration changes no CFRU source beyond the already merged #557 revision and changes no DPE, UPR-FVX, save, or ABI source.
- The accepted Route 10 MapEvents/object-table repoint is the already reviewed #557 layout delta. This pin introduces no additional map registration or layout behavior. No Celadon Move Reminder, Settings UX, National-Dex timing, Randomizer R2, BizHawk, or Tracker work was started.

## Deviations, risk, and protected artifacts

No #559 scope deviation was found. The source build emitted warnings but succeeded. The exact merged pin has ROM-free source, host-test, and source-build evidence only; no private-ROM insertion, emulator runtime, or broad M-014 acceptance is claimed.

No ROM, save, emulator state, finalized ROM, private log, screenshot, protected artifact path, `.env`, token, key, or secret was read, staged, or committed. No absolute local path is included in this evidence or the PR. Required source-build outputs were generated by the build command and were not opened or used as agent inputs. No protected artifact enters the PR.
