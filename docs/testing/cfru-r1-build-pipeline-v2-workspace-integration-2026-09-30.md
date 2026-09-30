# CFRU R1 Build Pipeline v2 Workspace Integration

Issue #569 integrates the accepted CFRU R1 build-pipeline repair by advancing
only the Workspace CFRU Gitlink. This records the frozen pin, merge provenance,
and the ROM-free verification performed at the integrated component revision.

## Frozen identity and scope

- Workspace base: `f61a312974950323764830c9f4b7b4d9dc99e4ca`
- CFRU previous pin: `8af56bc2fb71a6a392d7e79d3a22732a4de4fae6`
- Accepted #567 source head: `6ae9badcefe2adebef260206067c1782eadb4dc8`
- CFRU merged/current compat pin: `c9a7f19f1e8aaebd33213503f32fa7bba59ce81c`
- Workspace branch: `integration/cfru-r1-build-pipeline-v2-pin`

The accepted source head is an ancestor of the compat merge. The merge is one
commit ahead of that head, has no commits behind it, and has an identical tree
(zero changed files). Relative to the old Workspace pin, the CFRU merge changes
only `scripts/check_hidden_item_sparkle.py`, `scripts/make.py`, and
`scripts/tests/test_make_insert_fail_fast.py`.

The Workspace integration changes exactly these paths:

- `02_external/CFRU-expansion` — Gitlink `8af56bc...` → `c9a7f19...`
- `docs/testing/cfru-r1-build-pipeline-v2-workspace-integration-2026-09-30.md` —
  this evidence record

All nine other component/reference Gitlinks retain their base revisions. No
protected paths or product files are part of the Workspace change.

## Verification at CFRU `c9a7f19`

All checks below ran from the exact integrated CFRU pin, without a ROM or runtime.

| Gate | Result and relevant witness |
| --- | --- |
| `python3 scripts/build.py` | PASS, exit 0; generated build output was not inspected. |
| `python3 scripts/tests/test_make_assignment_updates.py` | PASS. |
| `python3 scripts/tests/test_make_insert_fail_fast.py` | PASS, 6/6: successful insert, nonzero insert, execution exception, failed build, combined mock success, and stale synthetic output with failed insert. |
| Missing-source-ROM behavior | PASS as a synthetic `FileNotFoundError` mock; `make.main()` returned nonzero. No ROM was opened. |
| `python3 scripts/check_hidden_item_sparkle.py` | PASS: M-009 source ownership, frame/scanner/resource/persistence and preflight guards, host-scanner checks, overlay composition, and rejection fixtures. `#538` exact state and that state plus an independent Route 10-style row pass; 34 owned-contract/preflight/composition mutations are rejected. Reference census: CyanNatDex 426 maps and max BG 36; pret 425 maps and max BG 36. |
| `python3 scripts/check_coherent_learnsets.py` | PASS: 144,000 host cases; 27 reserved sentinels; invalid pointers, non-sentinel level-one gaps, invalid rows, outside-range/shared/null pointers, and invalid configuration cases rejected. |
| `python3 scripts/tests/test_settings_legacy_ux.py` | PASS; legacy label widths and page-three help layout checks pass. |
| `python3 scripts/tests/run_settings_defaults_tests.py` | PASS: raw witness diff 4, trainer-scale 1, wild 0, trainer-AI 7, Ironmon 8. |
| `python3 scripts/tests/run_standard_ai_tests.py` | PASS: 131 named overrides; 4,096 adapter twin pairs with 0 mismatches; 98,304 envelope cases; 1,024 Ironmon twin pairs with 0 mismatches; 663,000 badge-oracle cases. Host-size ABI observations are host-only witnesses. |
| `python3 scripts/tests/run_ironmon_ai_tests.py` | PASS with the #515 corpus: admission 491/533, equal-four 245/256/262/261, C host parity 63/63, tags 58/58, expected digests. Temporary host objects were removed by the runner. |
| `python3 scripts/tests/run_early_running_pewter_tests.py` | PASS, including Pewter replacement coverage. |
| `python3 scripts/insert.py --check-map-object-overlays` | PASS. |
| `python3 scripts/check_premier_bonus.py` | PASS: callback thresholds, capacities 0–100, A/B, 16-bit quantities, 11,110 ball cases, single reward, failure/no-input, and non-ball controls. |
| `python3 scripts/check_renewable_hidden_items.py` | PASS. |
| Route 10 functional tests | PASS, 5/5 functional methods. The historical sixth exact-file-set guard (`test_script_awards_once_and_route2_source_is_untouched`) was not run or changed. |
| `python3 scripts/tests/audit_m007_national_dex_handoff.py` | Source assertions pass; the unchanged historical #549 exact changed-file-set guard stops on subsequently accepted #557/#547 scope. Disposition: `EXPECTED_HISTORICAL_SCOPE_GUARD`. The guard was not changed. |

The Route 10 `5/5` result is the current-pin functional run; it makes no claim
about the historical sixth guard. National-Dex scope is likewise kept separate
from the source assertions.

## Integration safety

Before editing the evidence file, the Workspace branch was verified at the
exact base, with the old CFRU pin and all other Gitlinks unchanged. The staged
pin delta was one mode-`160000` entry. Final `git diff --check` and
`python3 07_scripts/bootstrap/check_git_safety.py` both passed; the Workspace
change remains limited to the two paths listed above.

The component change is build/guard/test tooling only. It does not change
gameplay, data, map content, save layout, ABI/struct layout, AI policy, settings
semantics, National-Dex behavior, or HM behavior.

## Explicit non-claims

- No ROM was opened and no ROM insertion was performed.
- No `scripts/make.py` ROM build, emulator, runtime, save, or state was used.
- No Randomizer output was created.
- No build artifact was inspected.
- No R2 or #568 runner work was performed.
- No merge of the Workspace PR is implied by this integration.
