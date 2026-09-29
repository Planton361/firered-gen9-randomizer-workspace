# CFRU build-pipeline Workspace integration — 2026-09-29

## Revision identity

- Workspace base: `fabe288dfc94fed4a9d9fcfe7ac7b4223dd1ae21`.
- Workspace branch: `integration/cfru-build-pipeline-pin`; final branch head is the head recorded by the linked Workspace PR.
- CFRU Gitlink before: `11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec`.
- CFRU Gitlink after: `ec4e1b7410a65b23e081010c580ecb8c078a64a1`.
- Accepted #542 source head: `f0d5c70a7d41efef6b6b2fa7a3e6965cd84d81e5`.
- Merged CFRU PR #58 revision: `ec4e1b7410a65b23e081010c580ecb8c078a64a1`.
- PR #58 is merged. Accepted source head to merge is one commit; the merge commit has zero file changes relative to the accepted head. The `compat/firered-gen9-randomizer` branch resolves to the merge revision.

## Workspace scope and pins

The only changed Workspace paths are:

- `02_external/CFRU-expansion` — Gitlink `11bd0bd…` → `ec4e1b7…`.
- `docs/testing/cfru-build-pipeline-workspace-integration-2026-09-29.md` — this report.

All other component Gitlinks match the base:

| Component | Revision |
|---|---|
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |

Recursive Gitlink review showed exactly the authorized CFRU mode-`160000` change. No protected Workspace path changed.

## Exact-pin ROM-free verification

All checks below ran in CFRU `ec4e1b7410a65b23e081010c580ecb8c078a64a1`:

| Gate | Result |
|---|---|
| `python3 scripts/build.py` | PASS; complete compile/link. Existing RWX LOAD-segment linker warning remains. |
| `python3 scripts/check_coherent_learnsets.py` | PASS; 820 table replacements, 2 new form tables, 7 rebindings; active, unrelated, duplicate and mutated config changes rejected. |
| `python3 scripts/check_hidden_item_sparkle.py` | PASS; M-009 frame/scanner/preflight/composition checks, map census and 21 mutation fixtures. |
| `python3 scripts/tests/test_make_assignment_updates.py` | PASS; import/blank-line shift, preserved text, exact-one assignment failures and linker matching. |
| `python3 scripts/tests/run_early_running_pewter_tests.py` | PASS; Early Running lifecycle and exact Pewter overlay/script-pointer checks. |
| `python3 scripts/tests/run_settings_defaults_tests.py` | PASS; settings source, raw preservation and defaults checks. |
| `python3 scripts/tests/run_standard_ai_tests.py` | PASS; fairness, host parity, bounds, dispatch and state/layout checks. |
| `python3 scripts/tests/run_ironmon_ai_tests.py` | PASS; fairness/source, host parity, admission, response and lifecycle checks. |
| `python3 scripts/insert.py --check-map-object-overlays` | PASS; serialized overlay and accepted feature composition checks. |
| `git diff --check` | PASS. |
| Workspace `python3 07_scripts/bootstrap/check_git_safety.py` | PASS on the bounded non-main branch. |

The `make.py` regression confirms semantic exact-one updates to `OFFSET_TO_PUT` and `SOURCE_ROM`; zero or multiple matches fail before writing, and shifted imports/blank lines cannot corrupt `insert.py`. The linker ROM-origin update is exact-one and fail-closed.

Coherent-learnset and M-009 ownership/preflight checks remain fail-closed. Only the two exact disabled AI diagnostic comments are normalized. The M-009 frame owner, bindings, call sequence, scanner/resource constraints and insertion preflight are preserved. Accepted #538 Pewter overlay composition is exact; unrelated linker, overlay and preflight mutations are rejected.

## Product and artifact disposition

The merged CFRU change is tooling/tests only. This integration introduces no gameplay C/source change, Pokémon data change, SaveBlock or expanded Vars/flags layout change, Pokémon/Trainer/BattleMove/NewBattleStruct layout change, DPE ABI change, randomizer-visible table change, map content change, or product-semantics change.

Verification used no ROM input, save, emulator state, screenshot, private log, secret, `.env`, or private path. The source build completed without ROM insertion. The private clean FireRed → DPE `make.py` → CFRU `make.py` pipeline and all runtime behavior remain untested; no private-ROM or runtime PASS is claimed. The user's private pipeline remains the first validation against protected ROM input after Workspace merge and CONTROL verification.
