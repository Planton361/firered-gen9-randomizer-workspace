# Sanitized acceptance result

**State:** `RUN_PACKAGE_READY / USER_RUN_PENDING`
**Evidence classification:** **INTENDED FUTURE STATE — active Runtime Acceptance contract.**
**Preparation status:** All 115 required case rows begin `NOT_RUN`; no M-014 runtime execution occurred.

This is a user-run package for Workspace Issue #498. Agents must not open or
inspect ROMs, saves, emulator states, generated builds, tool binaries,
screenshots, raw private runtime logs or private filesystem paths. Agents must
not run an emulator, randomize a ROM, produce an output ROM, or perform private
runtime acceptance. The user may execute private runtime operations locally;
only sanitized text results return to GitHub/CONTROL. No artifact hashes are
required.

Historical source: Workspace PR #489 / commit
`391a200a20bd217feee9ca9b973b200c089e6de1`; historical documentation
evidence only, freshly materialized for #498. Do not reopen, merge, cherry-pick
or make PR #489 operative.

## Immutable Git revision identity

These exact revisions define the M-014 Workspace/test basis. The later
documentation branch commit is not the tested Workspace revision.

| Identity | Exact revision |
|---|---|
| Workspace/test basis | `7b77600a3091cba1c26cac0b7ffc0bfeb63b291f` |
| CFRU Expansion | `8bc8c38210ddba0b05c933dbda06cb4539254c7a` |
| DPE Gen 9 | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` |

## User-owned runtime/profile identity — record before the first case

M-014 runtime execution must not begin until every field below has sanitized
text. The placeholders are intentionally not runtime results.

| Required field | Entry |
|---|---|
| Source configuration differences | `<RECORD BEFORE RUN>` |
| Randomizer settings | `<RECORD BEFORE RUN>` |
| Non-sensitive seed/run label | `<RECORD BEFORE RUN>` |
| Emulator identity / version / core | `<RECORD BEFORE RUN>` |
| Fresh New Game status | `<RECORD BEFORE RUN>` |
| Clean/full source-build/module-test disposition where required | `<RECORD BEFORE RUN>` |

The immutable Git identity above, user-owned runtime/profile identity here, and
later observations/results are distinct evidence layers. Do not substitute a
documentation branch checkpoint for the Workspace/test basis.

## Pilot scope boundary

No Hospitality/M-011 reactivation, Commander, Embody Aspect, missing Gen-9
battle-mechanic implementation, Scarlet/Violet mechanics expansion, new
Terastal/form-transition implementation solely for parity, optional QoL
expansion or upstream contribution preparation is part of this report.
Unsupported forms/mechanics use the package's BLOCKED, N/A or profile-exclusion
rules. This is not universal Gen-1–9 compatibility testing.
`UPSTREAM_CONTRIBUTION = DEFERRED`.

## Result semantics and preparation rule

- `PASS`: every stated procedure/variant criterion is satisfied and the
  sanitized observation is recorded.
- `FAIL`: an acceptance criterion is not met; include a defect.
- `BLOCKED`: a prerequisite, accessibility or safe-profile boundary
  prevents execution; record the prerequisite/reason.
- `NOT_RUN`: no M-014 result exists yet; this is the initial status for
  every row below.
- `N/A`: an explicit source-backed pilot/profile exclusion accepted by
  review; never use it to skip a mandatory case.

Do not report, infer, copy forward or promote any M-014 PASS from Runtime Gate 1,
earlier milestone runtime passes, PR #489 or historical acceptance records.
Runtime Gate 1 remains separate targeted evidence. Add any independent
case/variant rows needed during the user run without changing the base IDs or
package scope.

## Case results

One row is present for every required package case ID. The procedure in
`docs/testing/feature-complete-acceptance.md` defines the required
variants and PASS criteria. During the run, expand location/settings rows where
the procedure requires it (including B24, B26, C and H12); no omitted row may
be treated as PASS.

| Case ID | Required case/variant coverage | Result | Observed result (sanitized) | Defect / reason |
|---|---|---|---|---|
| A01 | All procedure-prescribed variants for A01 | NOT_RUN | | |
| A02 | All procedure-prescribed variants for A02 | NOT_RUN | | |
| A03 | All procedure-prescribed variants for A03 | NOT_RUN | | |
| A04 | All procedure-prescribed variants for A04 | NOT_RUN | | |
| A05 | All procedure-prescribed variants for A05 | NOT_RUN | | |
| A06 | All procedure-prescribed variants for A06 | NOT_RUN | | |
| A07 | All procedure-prescribed variants for A07 | NOT_RUN | | |
| A08 | All procedure-prescribed variants for A08 | NOT_RUN | | |
| A09 | All procedure-prescribed variants for A09 | NOT_RUN | | |
| A10 | All procedure-prescribed variants for A10 | NOT_RUN | | |
| A11 | All procedure-prescribed variants for A11 | NOT_RUN | | |
| A12 | All procedure-prescribed variants for A12 | NOT_RUN | | |
| A13 | All procedure-prescribed variants for A13 | NOT_RUN | | |
| A14 | All procedure-prescribed variants for A14 | NOT_RUN | | |
| A15 | All procedure-prescribed variants for A15 | NOT_RUN | | |
| A16 | All procedure-prescribed variants for A16 | NOT_RUN | | |
| A17 | All procedure-prescribed variants for A17 | NOT_RUN | | |
| B01 | All procedure-prescribed variants for B01 | NOT_RUN | | |
| B02 | All procedure-prescribed variants for B02 | NOT_RUN | | |
| B03 | All procedure-prescribed variants for B03 | NOT_RUN | | |
| B04 | All procedure-prescribed variants for B04 | NOT_RUN | | |
| B05 | All procedure-prescribed variants for B05 | NOT_RUN | | |
| B06 | All procedure-prescribed variants for B06 | NOT_RUN | | |
| B07 | All procedure-prescribed variants for B07 | NOT_RUN | | |
| B08 | All procedure-prescribed variants for B08 | NOT_RUN | | |
| B09 | All procedure-prescribed variants for B09 | NOT_RUN | | |
| B10 | All procedure-prescribed variants for B10 | NOT_RUN | | |
| B11 | All procedure-prescribed variants for B11 | NOT_RUN | | |
| B12 | All procedure-prescribed variants for B12 | NOT_RUN | | |
| B13 | All procedure-prescribed variants for B13 | NOT_RUN | | |
| B14 | All procedure-prescribed variants for B14 | NOT_RUN | | |
| B15 | All procedure-prescribed variants for B15 | NOT_RUN | | |
| B16 | All procedure-prescribed variants for B16 | NOT_RUN | | |
| B17 | All procedure-prescribed variants for B17 | NOT_RUN | | |
| B18 | All procedure-prescribed variants for B18 | NOT_RUN | | |
| B19 | All procedure-prescribed variants for B19 | NOT_RUN | | |
| B20 | All procedure-prescribed variants for B20 | NOT_RUN | | |
| B21 | All procedure-prescribed variants for B21 | NOT_RUN | | |
| B22 | All procedure-prescribed variants for B22 | NOT_RUN | | |
| B23 | All procedure-prescribed variants for B23 | NOT_RUN | | |
| B24 | All procedure-prescribed variants for B24 | NOT_RUN | | |
| B25 | All procedure-prescribed variants for B25 | NOT_RUN | | |
| B26 | All procedure-prescribed variants for B26 | NOT_RUN | | |
| B27 | All procedure-prescribed variants for B27 | NOT_RUN | | |
| C01 | All procedure-prescribed variants for C01 | NOT_RUN | | |
| C02 | All procedure-prescribed variants for C02 | NOT_RUN | | |
| C03 | All procedure-prescribed variants for C03 | NOT_RUN | | |
| C04 | All procedure-prescribed variants for C04 | NOT_RUN | | |
| C05 | All procedure-prescribed variants for C05 | NOT_RUN | | |
| C06 | All procedure-prescribed variants for C06 | NOT_RUN | | |
| C07 | All procedure-prescribed variants for C07 | NOT_RUN | | |
| C08 | All procedure-prescribed variants for C08 | NOT_RUN | | |
| C09 | All procedure-prescribed variants for C09 | NOT_RUN | | |
| C10 | All procedure-prescribed variants for C10 | NOT_RUN | | |
| D01 | All procedure-prescribed variants for D01 | NOT_RUN | | |
| D02 | All procedure-prescribed variants for D02 | NOT_RUN | | |
| D03 | All procedure-prescribed variants for D03 | NOT_RUN | | |
| D04 | All procedure-prescribed variants for D04 | NOT_RUN | | |
| D05 | All procedure-prescribed variants for D05 | NOT_RUN | | |
| D06 | All procedure-prescribed variants for D06 | NOT_RUN | | |
| D07 | All procedure-prescribed variants for D07 | NOT_RUN | | |
| D08 | All procedure-prescribed variants for D08 | NOT_RUN | | |
| D09 | All procedure-prescribed variants for D09 | NOT_RUN | | |
| D10 | All procedure-prescribed variants for D10 | NOT_RUN | | |
| D11 | All procedure-prescribed variants for D11 | NOT_RUN | | |
| D12 | All procedure-prescribed variants for D12 | NOT_RUN | | |
| D13 | All procedure-prescribed variants for D13 | NOT_RUN | | |
| D14 | All procedure-prescribed variants for D14 | NOT_RUN | | |
| D15 | All procedure-prescribed variants for D15 | NOT_RUN | | |
| D16 | All procedure-prescribed variants for D16 | NOT_RUN | | |
| E01 | All procedure-prescribed variants for E01 | NOT_RUN | | |
| E02 | All procedure-prescribed variants for E02 | NOT_RUN | | |
| E03 | All procedure-prescribed variants for E03 | NOT_RUN | | |
| E04 | All procedure-prescribed variants for E04 | NOT_RUN | | |
| E05 | All procedure-prescribed variants for E05 | NOT_RUN | | |
| E06 | All procedure-prescribed variants for E06 | NOT_RUN | | |
| E07 | All procedure-prescribed variants for E07 | NOT_RUN | | |
| F01 | All procedure-prescribed variants for F01 | NOT_RUN | | |
| F02 | All procedure-prescribed variants for F02 | NOT_RUN | | |
| F03 | All procedure-prescribed variants for F03 | NOT_RUN | | |
| F04 | All procedure-prescribed variants for F04 | NOT_RUN | | |
| F05 | All procedure-prescribed variants for F05 | NOT_RUN | | |
| F06 | All procedure-prescribed variants for F06 | NOT_RUN | | |
| F07 | All procedure-prescribed variants for F07 | NOT_RUN | | |
| G01 | All procedure-prescribed variants for G01 | NOT_RUN | | |
| G02 | All procedure-prescribed variants for G02 | NOT_RUN | | |
| G03 | All procedure-prescribed variants for G03 | NOT_RUN | | |
| G04 | All procedure-prescribed variants for G04 | NOT_RUN | | |
| G05 | All procedure-prescribed variants for G05 | NOT_RUN | | |
| G06 | All procedure-prescribed variants for G06 | NOT_RUN | | |
| H01 | All procedure-prescribed variants for H01 | NOT_RUN | | |
| H02 | All procedure-prescribed variants for H02 | NOT_RUN | | |
| H03 | All procedure-prescribed variants for H03 | NOT_RUN | | |
| H04 | All procedure-prescribed variants for H04 | NOT_RUN | | |
| H05 | All procedure-prescribed variants for H05 | NOT_RUN | | |
| H06 | All procedure-prescribed variants for H06 | NOT_RUN | | |
| H07 | All procedure-prescribed variants for H07 | NOT_RUN | | |
| H08 | All procedure-prescribed variants for H08 | NOT_RUN | | |
| H09 | All procedure-prescribed variants for H09 | NOT_RUN | | |
| H10 | All procedure-prescribed variants for H10 | NOT_RUN | | |
| H11 | All procedure-prescribed variants for H11 | NOT_RUN | | |
| H12 | All procedure-prescribed variants for H12 | NOT_RUN | | |
| H13 | All procedure-prescribed variants for H13 | NOT_RUN | | |
| H14 | All procedure-prescribed variants for H14 | NOT_RUN | | |
| H15 | All procedure-prescribed variants for H15 | NOT_RUN | | |
| P01 | All procedure-prescribed variants for P01 | NOT_RUN | | |
| P02 | All procedure-prescribed variants for P02 | NOT_RUN | | |
| P03 | All procedure-prescribed variants for P03 | NOT_RUN | | |
| P04 | All procedure-prescribed variants for P04 | NOT_RUN | | |
| P05 | All procedure-prescribed variants for P05 | NOT_RUN | | |
| P06 | All procedure-prescribed variants for P06 | NOT_RUN | | |
| P07 | All procedure-prescribed variants for P07 | NOT_RUN | | |
| P08 | All procedure-prescribed variants for P08 | NOT_RUN | | |
| P09 | All procedure-prescribed variants for P09 | NOT_RUN | | |
| P10 | All procedure-prescribed variants for P10 | NOT_RUN | | |

## Defect (repeat as needed)

ID / severity S0–S3:
First failing case / exact source revision:
Initial state (sanitized species/item/story stage):
Minimal numbered steps:
Expected:
Observed:
Frequency / attempts:
Unchanged control reproduces: YES / NO / NOT_TESTED
Run stopped / independent tests continued:
Known-good private recovery preserved: YES / NO / N/A
No cause inferred unless separately demonstrated:

### Severity definitions

| Severity | Definition | Response |
|---|---|---|
| S0 critical | Save corruption/loss, persistent invalid data, destructive write | Stop that run immediately; preserve the last known-good private save and report sanitized reproduction. |
| S1 high | Crash/hang, progression softlock, wrong active writer/table, duplicate key reward, invalid species/move, unrecoverable control loss | Stop the affected run/path; do not use downstream results as acceptance. |
| S2 medium | Reproducible functional mismatch with safe workaround, incorrect reward amount, missing expected UI/learn prompt | Fail the affected case and log a defect; continue only if independent state remains trustworthy. |
| S3 low | Cosmetic/text-only issue without gameplay/data effect | Log and continue; acceptance needs explicit disposition, not silent waiver. |

## Gate summary

Initial preparation counts: 115 NOT_RUN; 0 PASS; 0 FAIL; 0 BLOCKED; 0 N/A.

Passed cases / failed cases / blocked / not run / accepted exclusions:
Continuous D01–D16 Brock→Hall of Fame progression result: NOT_RUN
Unresolved S0/S1 summary: NOT_RUN — no runtime defect disposition exists before the user run.
S2/S3 disposition: NOT_RUN — no runtime defect disposition exists before the user run.
M-009 broad frame QA summary: NOT_RUN
M-013 transaction/capacity matrix summary: NOT_RUN — P01–P10 remain NOT_RUN.
Five restored learnset-family summary: NOT_RUN
Randomized combined-profile smoke summary: NOT_RUN
Reviewer decision: NOT_ACCEPTED
Remaining work: record the complete run identity, execute the user-run package,
and return sanitized results for every mandatory case or approved profile
exclusion.
