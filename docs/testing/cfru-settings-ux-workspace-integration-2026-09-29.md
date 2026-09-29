# CFRU Settings UX Workspace integration — 2026-09-29

**Contract:** Workspace Issue #561; accepted Settings UX Issue #547 and merged CFRU PR #61.
**Evidence classification:** CONFIRMED CURRENT STATE for the exact revisions, source checks, host tests, Gitlink review, and source build below. The Settings display has not been visually accepted in a running ROM at this pin; runtime appearance remains UNKNOWN.

## Revision identity

- Workspace `main` base: `7272390b9d3a6c547ccabe33e3701f9f49a35366`.
- Workspace branch: `integration/cfru-settings-ux-pin`.
- Workspace Gitlink pin commit: `a04fa8b543ddc1791502a5612c7c2255e66af400`.
- Final delivery head: the PR head containing this evidence file; its exact SHA is recorded in the PR and handoff because a commit cannot contain its own SHA.
- CFRU Gitlink: `b17f2e3c5dd0dad89db4d363d9254ef2f97ba9c3` → `8af56bc2fb71a6a392d7e79d3a22732a4de4fae6`.
- Accepted #547 source head: `bcdb977bb066b85e59cf87ccfc1b26a896563dca`.
- CFRU PR #61 merged revision and current `compat/firered-gen9-randomizer`: `8af56bc2fb71a6a392d7e79d3a22732a4de4fae6`.

The CFRU merge has first parent `b17f2e3c5dd0dad89db4d363d9254ef2f97ba9c3` and second parent `bcdb977bb066b85e59cf87ccfc1b26a896563dca`. The accepted source head is zero commits ahead and one behind the compat head (`git rev-list --left-right --count` returned `0 1`); the range has one merge commit and `git diff --exit-code` returned success with **zero file changes**. The fetched compat ref resolved exactly to `8af56bc2fb71a6a392d7e79d3a22732a4de4fae6`.

A separate Workspace checkout was reconstructed directly from GitHub. Before branch creation its Workspace status was clean, HEAD and all recursive Gitlinks matched the Issue basis, and `check_git_safety.py --allow-main` passed. The new non-`main` branch passed `check_git_safety.py` before the Gitlink change. The earlier unrelated dirty checkout was not modified; the meaning of its local changes remains UNKNOWN.

## Workspace scope and pins

The branch diff against the Workspace base contains exactly:

1. `02_external/CFRU-expansion` — the single authorized mode-`160000` Gitlink change.
2. `docs/testing/cfru-settings-ux-workspace-integration-2026-09-29.md` — this sanitized evidence.

All other component and reference Gitlinks are byte-identical to the Workspace base:

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

The CFRU range from old to new pin changes only `src/option_menu.c`, `strings/option_menu.string`, `scripts/tests/audit_settings_defaults.py`, and `scripts/tests/test_settings_legacy_ux.py`. The Workspace integration adds no new CFRU source change beyond those already accepted in #547.

## Exact-pin Settings and regression evidence

Every CFRU command below ran from a clean component worktree at exactly `8af56bc2fb71a6a392d7e79d3a22732a4de4fae6`.

| Gate | Result |
|---|---|
| `python3 scripts/tests/test_settings_legacy_ux.py` | PASS: exact menu labels, raw-index order, font/window geometry, every label width, 78 px clearing, and Page 3 help alignment. |
| `python3 scripts/tests/run_settings_defaults_tests.py` | PASS: raw mappings, raw-0 fallbacks, unknown/original-raw/dirty preservation, Fresh New Game defaults and Ironmon preset. |
| `python3 scripts/tests/run_standard_ai_tests.py` | PASS: Standard/legacy dispatch and policy regression, including 4,096 production twins with zero mismatches. |
| `python3 scripts/tests/run_ironmon_ai_tests.py` | PASS: Ironmon Smart dispatch, 63/63 host parity, 58/58 mandatory tags and accepted policy digests. |
| `python3 scripts/tests/run_early_running_pewter_tests.py` | PASS. |
| `python3 scripts/insert.py --check-map-object-overlays` | PASS. |
| Five functional `scripts.tests.test_route10_hm05` tests | PASS, 5/5 at this pin. |
| `python3 scripts/build.py` | PASS, exit 0; compiler warnings were emitted in unchanged sources. No private ROM or insertion input was used. |
| CFRU `git diff --check` old/new pin | PASS. |
| Workspace `git diff --check` and `check_git_safety.py` | PASS. |

Trainer Level Scaling raw 0 and Trainer AI raw 0 display `Auto (Diff.)` (64/78 px); Hard Cap raw 0 still displays `Auto`. Trainer AI raw 1–6 display `Legacy Vanil.` (73), `Legacy Easy` (65), `Legacy Normal` (76), `Legacy Hard` (65), `Legacy Expert` (76), and `Legacy Smart` (70). The full `Legacy Vanilla` is 79 px and would exceed the 78 px field. Raw 7 `Standard` (45) and raw 8 `Ironmon Smart` (73) are unchanged. The existing normal-font value alignment remains x=130 in a 208 px window; the clear region covers the same 78 px value field. The unchanged small-font Page 3 help is 187 px, right aligned at x=41 and ending at 228/240 px. No menu geometry, page order, truncation rule, or per-setting description region changed.

The Settings host suite retained raw Difficulty `0..4`, Trainer Level Scaling `0..5`, Trainer AI `0..8`, Hard Cap `0..2`, and the legacy raw-0 fallback behavior. Unknown raw values remain safely displayed and survive untouched open/close; original-raw/dirty handling still determines writes after editing. Fresh New Game remains Difficulty `4` (Vanilla), Trainer Scaling `1` (Off), Wild Scaling `0` (Off), Trainer AI `7` (Standard), running enabled and Auto-Run untouched. The Ironmon preset retains `4/1/0/8` and leaves unrelated rules unchanged. Standard and Ironmon Smart remain separate appended AI dispatch profiles.

### Route 10 disposition

The five functional Route-10 tests passed at `8af56bc…`. The sixth test is the historical #557 exact-changed-file-set guard; it intentionally rejects later #547 files when comparing to the #557 start pin. It was not modified or claimed as a fresh 6/6 result here. The old-to-new CFRU file list above proves that #547 changed no Route-10 production or test path. The earlier 6/6 at the #557 pin remains historical, revision-bound evidence.

## ABI, runtime, and protected boundaries

The Workspace diff is a Gitlink plus evidence only. The accepted #547 CFRU range contains presentation labels, option-table string references, value-field clearing, and tests; no raw enum/mapping, defaults, preset, AI/scaling runtime, SaveBlock, ABI struct, persistence, map, National Dex, Route 10, Move Reminder, DPE, or UPR-FVX source is changed. Save delta and layout remain as at the old CFRU pin; this integration introduces no migration or repoint.

This is source, host, Gitlink, and source-build evidence. It is **not** a visual ROM-runtime pass, private-ROM insertion result, renewed M-014 acceptance, `ROM_PROFILE_READY`, or permission to start Randomizer R2, BizHawk, or Tracker work. CONTROL must re-read the current ROM-finish gates after a user merge.

The GitHub Project item for #561 was verified as `P0 / Integration / Doing`. This PR remains evidence for review, not an independent work queue.

No ROM, save, emulator state, generated build, screenshot, private log or path, tool binary, `.env`, token, key, or secret was opened or used as agent input. Build outputs were generated by the required source-build command and were not inspected, staged, or committed. No absolute local path or protected artifact enters this evidence or the PR.
