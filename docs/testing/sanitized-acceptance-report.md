# Sanitized acceptance result

**State:** `R1_RUN_PACKAGE_READY / ROM_RUN_PENDING`
**Evidence classification:** **CONFIRMED CURRENT STATE** for accepted R0;
**INTENDED FUTURE STATE** for Phase R1/R2 runtime acceptance.
**Preparation status:** All 115 required case rows remain `NOT_RUN`; no M-014 runtime execution occurred.

This is a user-run package for Workspace Issue #498. Agents must not open or
inspect ROMs, saves, emulator states, generated builds, tool binaries,
screenshots, raw private runtime logs or private filesystem paths. Agents must
not run an emulator, randomize a ROM, produce an output ROM, or perform private
runtime acceptance. The user may execute private runtime operations locally;
only sanitized text results return to GitHub/CONTROL. No artifact hashes are
required.

Phase R0 is complete and integrated on current `main`. The accepted [ROM
finish-readiness audit](../audits/rom-finish-readiness-2026-09-20.md) records
`ROM_SCOPE_READY_FOR_ACCEPTANCE`, `MISSING_BLOCKER = 0`, and
`UNKNOWN_BLOCKER = 0`. Its documented intentional differences, optional
backlog and out-of-pilot items are profile boundaries, not runtime failures.

Historical source: Workspace PR #489 / commit
`391a200a20bd217feee9ca9b973b200c089e6de1`; historical documentation
evidence only, freshly materialized for #498. Do not reopen, merge, cherry-pick
or make PR #489 operative.

## Immutable Phase R1 Git revision identity

These exact revisions define the Phase R1 Workspace/source-test basis. The
repair branch tip is provenance only and is not the tested Workspace basis.

| Identity | Exact revision |
|---|---|
| Workspace source/test basis | `b1dc157a4cfb000c1fa14a0e3323210c350d767a` |
| CFRU Expansion | `8bc8c38210ddba0b05c933dbda06cb4539254c7a` |
| DPE Gen 9 | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX | `boundary/reference only during Phase R1 — 0e3be63e94e34215cc35308d64e8db15e9a3c48c` |

## Phase R1 user-owned ROM identity — record before the first R1 case

Phase R1 runtime must not begin until every field below has sanitized text.
Randomizer settings, seed/run labels and output-profile identity are not R1
prerequisites and belong only to the Phase R2 section.

| Required field | Entry before Phase R1 runtime |
|---|---|
| Source configuration differences | `<RECORD BEFORE RUN>` |
| Emulator identity / version / core | `<RECORD BEFORE RUN>` |
| Non-sensitive ROM run label | `<RECORD BEFORE RUN>` |
| Fresh New Game status | `<RECORD BEFORE RUN>` |
| Clean/full source-build disposition | `<RECORD BEFORE RUN>` |
| ROM-owned module-test disposition | `<RECORD BEFORE RUN>` |

## Phase R2 user-owned Randomizer identity — record before any R2 case

Phase R2 cannot begin until `ROM_PROFILE_READY` is accepted. Record
Randomizer/output values separately:

| Required field | Entry before Phase R2 runtime |
|---|---|
| Randomizer settings | `<RECORD BEFORE R2 RUN>` |
| Randomizer seed/run label | `<RECORD BEFORE R2 RUN>` |
| Output profile identity | `<RECORD BEFORE R2 RUN>` |
| Randomizer source/module-test disposition | `<RECORD BEFORE R2 RUN>` |

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

## Phase ownership and acceptance gates

All 115 existing IDs are preserved. The phase owner is recorded per row below:

| Ownership | Case IDs / variants | Count and initial status |
|---|---|---|
| R1 ROM-only | A01–A17, B01–B17, B19–B27, C01–C10, D01–D16, E01–E07, F01–F07, G01–G06 | 89 case IDs; NOT_RUN |
| R2 Randomizer-only | B18, H01–H15 | 16 case IDs; NOT_RUN and R2-gated |
| Split | P01–P10 ordinary-shop portion = R1; randomized-shop portion = R2 | 10 case IDs / 20 variants; both NOT_RUN |

R1 owns the ROM-side A–G scope, ROM-owned B cases, and ordinary-shop Premier
transactions. R2 owns H01–H15, B18 randomized Field/TM variants, and the
randomized-shop Premier variants. R1-owned units total 99 including the ten
ordinary-shop split variants; R2-owned units total 26 including the ten
randomized-shop split variants.

`ROM_PROFILE_READY` may be accepted when all mandatory R1-owned units have
PASS or approved N/A/profile exclusion, no unresolved S0/S1 remains, every
S2/S3 has an explicit disposition, D01–D16 is continuous, and the relevant
M-009/M-013/data/form/QoL gates are satisfied. R2-only units remaining
`NOT_RUN` do not block that R1 decision, but they do block final #498 and
`RANDOMIZER_PROFILE_READY`. `RANDOMIZER_PROFILE_READY` is not permitted before
`ROM_PROFILE_READY`.

## Case results

One row is present for every required package case ID. The procedure in
`docs/testing/feature-complete-acceptance.md` defines the required
variants and PASS criteria. During the run, expand location/settings rows where
the procedure requires it (including B24, B26, C and H12); no omitted row may
be treated as PASS.

| Case ID | Phase owner | Required case/variant coverage | Result | Observed result (sanitized) | Defect / reason |
|---|---|---|---|---|---|
| A01 | R1 ROM | All procedure-prescribed variants for A01 | NOT_RUN | | |
| A02 | R1 ROM | All procedure-prescribed variants for A02 | NOT_RUN | | |
| A03 | R1 ROM | All procedure-prescribed variants for A03 | NOT_RUN | | |
| A04 | R1 ROM | All procedure-prescribed variants for A04 | NOT_RUN | | |
| A05 | R1 ROM | All procedure-prescribed variants for A05 | NOT_RUN | | |
| A06 | R1 ROM | All procedure-prescribed variants for A06 | NOT_RUN | | |
| A07 | R1 ROM | All procedure-prescribed variants for A07 | NOT_RUN | | |
| A08 | R1 ROM | All procedure-prescribed variants for A08 | NOT_RUN | | |
| A09 | R1 ROM | All procedure-prescribed variants for A09 | NOT_RUN | | |
| A10 | R1 ROM | All procedure-prescribed variants for A10 | NOT_RUN | | |
| A11 | R1 ROM | All procedure-prescribed variants for A11 | NOT_RUN | | |
| A12 | R1 ROM | All procedure-prescribed variants for A12 | NOT_RUN | | |
| A13 | R1 ROM | All procedure-prescribed variants for A13 | NOT_RUN | | |
| A14 | R1 ROM | All procedure-prescribed variants for A14 | NOT_RUN | | |
| A15 | R1 ROM | All procedure-prescribed variants for A15 | NOT_RUN | | |
| A16 | R1 ROM | All procedure-prescribed variants for A16 | NOT_RUN | | |
| A17 | R1 ROM | All procedure-prescribed variants for A17 | NOT_RUN | | |
| B01 | R1 ROM | All procedure-prescribed variants for B01 | NOT_RUN | | |
| B02 | R1 ROM | All procedure-prescribed variants for B02 | NOT_RUN | | |
| B03 | R1 ROM | All procedure-prescribed variants for B03 | NOT_RUN | | |
| B04 | R1 ROM | All procedure-prescribed variants for B04 | NOT_RUN | | |
| B05 | R1 ROM | All procedure-prescribed variants for B05 | NOT_RUN | | |
| B06 | R1 ROM | All procedure-prescribed variants for B06 | NOT_RUN | | |
| B07 | R1 ROM | All procedure-prescribed variants for B07 | NOT_RUN | | |
| B08 | R1 ROM | All procedure-prescribed variants for B08 | NOT_RUN | | |
| B09 | R1 ROM | All procedure-prescribed variants for B09 | NOT_RUN | | |
| B10 | R1 ROM | All procedure-prescribed variants for B10 | NOT_RUN | | |
| B11 | R1 ROM | All procedure-prescribed variants for B11 | NOT_RUN | | |
| B12 | R1 ROM | All procedure-prescribed variants for B12 | NOT_RUN | | |
| B13 | R1 ROM | All procedure-prescribed variants for B13 | NOT_RUN | | |
| B14 | R1 ROM | All procedure-prescribed variants for B14 | NOT_RUN | | |
| B15 | R1 ROM | All procedure-prescribed variants for B15 | NOT_RUN | | |
| B16 | R1 ROM | All procedure-prescribed variants for B16 | NOT_RUN | | |
| B17 | R1 ROM | All procedure-prescribed variants for B17 | NOT_RUN | | |
| B18 | R2 Randomizer | Randomized Field/TM variants from H12; R2 only | NOT_RUN | | |
| B19 | R1 ROM | All procedure-prescribed variants for B19 | NOT_RUN | | |
| B20 | R1 ROM | All procedure-prescribed variants for B20 | NOT_RUN | | |
| B21 | R1 ROM | All procedure-prescribed variants for B21 | NOT_RUN | | |
| B22 | R1 ROM | All procedure-prescribed variants for B22 | NOT_RUN | | |
| B23 | R1 ROM | All procedure-prescribed variants for B23 | NOT_RUN | | |
| B24 | R1 ROM | All procedure-prescribed variants for B24 | NOT_RUN | | |
| B25 | R1 ROM | All procedure-prescribed variants for B25 | NOT_RUN | | |
| B26 | R1 ROM | All procedure-prescribed variants for B26 | NOT_RUN | | |
| B27 | R1 ROM | All procedure-prescribed variants for B27 | NOT_RUN | | |
| C01 | R1 ROM | All procedure-prescribed variants for C01 | NOT_RUN | | |
| C02 | R1 ROM | All procedure-prescribed variants for C02 | NOT_RUN | | |
| C03 | R1 ROM | All procedure-prescribed variants for C03 | NOT_RUN | | |
| C04 | R1 ROM | All procedure-prescribed variants for C04 | NOT_RUN | | |
| C05 | R1 ROM | All procedure-prescribed variants for C05 | NOT_RUN | | |
| C06 | R1 ROM | All procedure-prescribed variants for C06 | NOT_RUN | | |
| C07 | R1 ROM | All procedure-prescribed variants for C07 | NOT_RUN | | |
| C08 | R1 ROM | All procedure-prescribed variants for C08 | NOT_RUN | | |
| C09 | R1 ROM | All procedure-prescribed variants for C09 | NOT_RUN | | |
| C10 | R1 ROM | All procedure-prescribed variants for C10 | NOT_RUN | | |
| D01 | R1 ROM | All procedure-prescribed variants for D01 | NOT_RUN | | |
| D02 | R1 ROM | All procedure-prescribed variants for D02 | NOT_RUN | | |
| D03 | R1 ROM | All procedure-prescribed variants for D03 | NOT_RUN | | |
| D04 | R1 ROM | All procedure-prescribed variants for D04 | NOT_RUN | | |
| D05 | R1 ROM | All procedure-prescribed variants for D05 | NOT_RUN | | |
| D06 | R1 ROM | All procedure-prescribed variants for D06 | NOT_RUN | | |
| D07 | R1 ROM | All procedure-prescribed variants for D07 | NOT_RUN | | |
| D08 | R1 ROM | All procedure-prescribed variants for D08 | NOT_RUN | | |
| D09 | R1 ROM | All procedure-prescribed variants for D09 | NOT_RUN | | |
| D10 | R1 ROM | All procedure-prescribed variants for D10 | NOT_RUN | | |
| D11 | R1 ROM | All procedure-prescribed variants for D11 | NOT_RUN | | |
| D12 | R1 ROM | All procedure-prescribed variants for D12 | NOT_RUN | | |
| D13 | R1 ROM | All procedure-prescribed variants for D13 | NOT_RUN | | |
| D14 | R1 ROM | All procedure-prescribed variants for D14 | NOT_RUN | | |
| D15 | R1 ROM | All procedure-prescribed variants for D15 | NOT_RUN | | |
| D16 | R1 ROM | All procedure-prescribed variants for D16 | NOT_RUN | | |
| E01 | R1 ROM | All procedure-prescribed variants for E01 | NOT_RUN | | |
| E02 | R1 ROM | All procedure-prescribed variants for E02 | NOT_RUN | | |
| E03 | R1 ROM | All procedure-prescribed variants for E03 | NOT_RUN | | |
| E04 | R1 ROM | All procedure-prescribed variants for E04 | NOT_RUN | | |
| E05 | R1 ROM | All procedure-prescribed variants for E05 | NOT_RUN | | |
| E06 | R1 ROM | All procedure-prescribed variants for E06 | NOT_RUN | | |
| E07 | R1 ROM | All procedure-prescribed variants for E07 | NOT_RUN | | |
| F01 | R1 ROM | All procedure-prescribed variants for F01 | NOT_RUN | | |
| F02 | R1 ROM | All procedure-prescribed variants for F02 | NOT_RUN | | |
| F03 | R1 ROM | All procedure-prescribed variants for F03 | NOT_RUN | | |
| F04 | R1 ROM | All procedure-prescribed variants for F04 | NOT_RUN | | |
| F05 | R1 ROM | All procedure-prescribed variants for F05 | NOT_RUN | | |
| F06 | R1 ROM | All procedure-prescribed variants for F06 | NOT_RUN | | |
| F07 | R1 ROM | All procedure-prescribed variants for F07 | NOT_RUN | | |
| G01 | R1 ROM | All procedure-prescribed variants for G01 | NOT_RUN | | |
| G02 | R1 ROM | All procedure-prescribed variants for G02 | NOT_RUN | | |
| G03 | R1 ROM | All procedure-prescribed variants for G03 | NOT_RUN | | |
| G04 | R1 ROM | All procedure-prescribed variants for G04 | NOT_RUN | | |
| G05 | R1 ROM | All procedure-prescribed variants for G05 | NOT_RUN | | |
| G06 | R1 ROM | All procedure-prescribed variants for G06 | NOT_RUN | | |
| H01 | R2 Randomizer | Randomizer/output procedure variants for H01; R2 only | NOT_RUN | | |
| H02 | R2 Randomizer | Randomizer/output procedure variants for H02; R2 only | NOT_RUN | | |
| H03 | R2 Randomizer | Randomizer/output procedure variants for H03; R2 only | NOT_RUN | | |
| H04 | R2 Randomizer | Randomizer/output procedure variants for H04; R2 only | NOT_RUN | | |
| H05 | R2 Randomizer | Randomizer/output procedure variants for H05; R2 only | NOT_RUN | | |
| H06 | R2 Randomizer | Randomizer/output procedure variants for H06; R2 only | NOT_RUN | | |
| H07 | R2 Randomizer | Randomizer/output procedure variants for H07; R2 only | NOT_RUN | | |
| H08 | R2 Randomizer | Randomizer/output procedure variants for H08; R2 only | NOT_RUN | | |
| H09 | R2 Randomizer | Randomizer/output procedure variants for H09; R2 only | NOT_RUN | | |
| H10 | R2 Randomizer | Randomizer/output procedure variants for H10; R2 only | NOT_RUN | | |
| H11 | R2 Randomizer | Randomizer/output procedure variants for H11; R2 only | NOT_RUN | | |
| H12 | R2 Randomizer | Randomizer/output procedure variants for H12; R2 only | NOT_RUN | | |
| H13 | R2 Randomizer | Randomizer/output procedure variants for H13; R2 only | NOT_RUN | | |
| H14 | R2 Randomizer | Randomizer/output procedure variants for H14; R2 only | NOT_RUN | | |
| H15 | R2 Randomizer | Randomizer/output procedure variants for H15; R2 only | NOT_RUN | | |
| P01 | Split: R1 ordinary shop / R2 randomized shop | Ordinary-shop and randomized-shop variants for P01 | NOT_RUN | | |
| P02 | Split: R1 ordinary shop / R2 randomized shop | Ordinary-shop and randomized-shop variants for P02 | NOT_RUN | | |
| P03 | Split: R1 ordinary shop / R2 randomized shop | Ordinary-shop and randomized-shop variants for P03 | NOT_RUN | | |
| P04 | Split: R1 ordinary shop / R2 randomized shop | Ordinary-shop and randomized-shop variants for P04 | NOT_RUN | | |
| P05 | Split: R1 ordinary shop / R2 randomized shop | Ordinary-shop and randomized-shop variants for P05 | NOT_RUN | | |
| P06 | Split: R1 ordinary shop / R2 randomized shop | Ordinary-shop and randomized-shop variants for P06 | NOT_RUN | | |
| P07 | Split: R1 ordinary shop / R2 randomized shop | Ordinary-shop and randomized-shop variants for P07 | NOT_RUN | | |
| P08 | Split: R1 ordinary shop / R2 randomized shop | Ordinary-shop and randomized-shop variants for P08 | NOT_RUN | | |
| P09 | Split: R1 ordinary shop / R2 randomized shop | Ordinary-shop and randomized-shop variants for P09 | NOT_RUN | | |
| P10 | Split: R1 ordinary shop / R2 randomized shop | Ordinary-shop and randomized-shop variants for P10 | NOT_RUN | | |

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

## Phase R1 summary — ROM runtime acceptance

Initial R1-owned preparation counts: 99 units NOT_RUN; 0 PASS; 0 FAIL;
0 BLOCKED; 0 N/A. This is 89 R1-only case IDs plus the ten ordinary-shop
Premier variants from P01–P10.

- Continuous D01–D16 Brock→Hall of Fame progression: `NOT_RUN`.
- Unresolved S0/S1: `NOT_RUN` — no runtime execution occurred, so no runtime
  defect disposition exists yet.
- S2/S3 dispositions: `NOT_RUN` — every future defect requires an explicit
  severity and disposition.
- M-009 broad-frame QA (C01–C10): `NOT_RUN`.
- M-013 ordinary-shop Premier matrix (P01–P10 ordinary variants): `NOT_RUN`.
- Gen1–9 ROM display/form/data sanity (G01–G06): `NOT_RUN`.
- ROM-owned A–G and B cases: `NOT_RUN`.
- Reviewer decision: `NOT_ACCEPTED`.

R1 may become `ROM_PROFILE_READY` only after all mandatory R1-owned units have
PASS or approved N/A/profile exclusion, no unresolved S0/S1 remains, every
S2/S3 has an explicit disposition, D01–D16 is continuous, and the relevant
M-009/M-013/data/form/QoL gates are satisfied. R2-only cases remaining
`NOT_RUN` do not block that R1 decision.

## Phase R2 summary — UPR-FVX / randomized-output acceptance

Initial R2-owned preparation counts: 26 units NOT_RUN; 0 PASS; 0 FAIL;
0 BLOCKED; 0 N/A:

- B18 randomized Field/TM variants: `NOT_RUN`; R2-gated.
- H01–H15 Randomizer/output acceptance: `NOT_RUN`; R2-gated.
- P01–P10 randomized-shop variants: `NOT_RUN`; R2-gated.
- Combined supported profile: `NOT_RUN`.
- Reviewer decision: `NOT_ACCEPTED`.

`RANDOMIZER_PROFILE_READY` is forbidden before `ROM_PROFILE_READY`. These R2
units remain required for final #498 acceptance even if R1 is accepted first.

## Overall package state

All 115 base case IDs and all split variants remain `NOT_RUN`. No ROM runtime,
Randomizer output, emulator or private acceptance execution occurred in this
repair. Record the complete Phase R1 identity and user-owned ROM results first;
only after `ROM_PROFILE_READY` may the Phase R2 identity and randomized-output
results be recorded.
