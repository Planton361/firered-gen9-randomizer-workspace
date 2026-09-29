# Sanitized acceptance result

**State:** `R1_RUN_PACKAGE_FINAL_REBASELINE_READY / ROM_RUN_PENDING`
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

The sole operative R0 gate is the accepted #563
[final ROM scope audit](../audits/m014-r0-final-rom-scope-2026-09-29.md),
merged through #564: `ROM_SCOPE_READY_FOR_ACCEPTANCE`, `MISSING_BLOCKER = 0`,
`UNKNOWN_BLOCKER = 0`. Earlier R0 audits are historical supporting evidence
only. Final R1 can be released only on this #563 closure and after #565 is
accepted and merged. This preparation does not claim `ROM_PROFILE_READY`.
Intentional differences, optional backlog and out-of-pilot items are profile
boundaries, not runtime failures.

Historical source: Workspace PR #489 / commit
`391a200a20bd217feee9ca9b973b200c089e6de1`; historical documentation
evidence only, freshly materialized for #498. Do not reopen, merge, cherry-pick
or make PR #489 operative.

## Immutable Phase R1 Git revision identity

These exact revisions define the final Phase R1 ROM product-source identity.

| Identity | Exact revision |
|---|---|
| Workspace ROM product-source basis | `b20454789e375383eb852d749c0357d58af461dc` |
| CFRU Expansion | `8af56bc2fb71a6a392d7e79d3a22732a4de4fae6` |
| DPE Gen 9 | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX | `boundary/reference only during Phase R1 — 7bf79ee1e7c46c972f7a9c84942970a950be0723` |

### Workspace repository/package provenance

Current accepted Workspace repository/documentation base:
`87ae5807cd7f5e72831256256c84eb7ae2440a1f`. After product-source basis
`b20454789e375383eb852d749c0357d58af461dc`, this revision contains only the
accepted #563/#564 R0 audit documentation; no component source or Gitlink
changed. These later documentation commits do not change the ROM product-source
basis. Package, PR, audit and later documentation commit SHAs are provenance
only and must never replace the ROM product-source basis above.

Exact-pin source/host evidence from #563 and earlier integration Issues may be
cited as revision-bound supporting evidence only, never as final runtime PASS.
Older-pin build/module PASS results must not be transferred to this final pin.

## Phase R1 user-owned ROM identity — record before the first R1 case

Phase R1 runtime must not begin until every field below has sanitized text
recording the current disposition at the exact final product-source identity.
Complete the required clean/full source build and ROM-owned module tests before
the private run; older-pin build PASS results do not establish these gates.
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

The final continuous D01–D16 main run must restart from a genuine Fresh New
Game on the final ROM product-source basis; no earlier-candidate save or
historical D01/D02 result can replace it. The Fresh-New-Game source profile is
Game Difficulty = Vanilla, Trainer Level Scaling = Off, Wild Level Scaling =
Off, Trainer AI = Standard. Normal running is already enabled; Auto-Run is
separate and initially Off until the user toggles it. The post-Brock Running
Shoes Aide is only the accepted short, non-gating cleanup and does not unlock
normal running.

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
Runtime Gate 1 remains separate targeted evidence. Historical D01/D02 results
remain revision-bound supporting evidence only; all final results stay NOT_RUN
until the new final-pin run. Add sanitized variant observations under existing
IDs only; do not add official case IDs or change package scope.

## Integrated Trainer-AI/settings witness coverage

These are additional variants of existing A01, B16 and B27 coverage; no new
base case IDs are added. Every witness remains `NOT_RUN` until the user-owned
Phase R1 run records sanitized observations.

| Existing row | Required R1 witness | Initial status |
|---|---|---|
| A01 | Fresh Options visibly show Game Difficulty = Vanilla, Trainer Level Scaling = Off, Wild Level Scaling = Off and Trainer AI = Standard; normal running already enabled, separate Auto-Run initially Off; National Dex inactive; no unrelated rule or setting changes implicitly. | NOT_RUN |
| B16 | Standard and Ironmon Smart are selectable/displayable with legacy entries distinct; open/close without editing does not rewrite settings; Trainer AI changes do not alter Difficulty, Trainer Scaling, Wild Scaling, Hard Cap/Nuzlocke or other independent rules, and those settings do not rewrite Trainer AI. | NOT_RUN |
| B27 | Explicit Trainer AI plus relevant Difficulty/Scaling values persist through save/reload as designed; no save/state artifact is returned to agents. | NOT_RUN |
| B16/B27 variant | One representative ordinary trainer battle under Standard and one under Ironmon Smart, checking only runtime routing, stability and profile integration; no AI-strength conclusion. Restore Standard for the continuous main run after the targeted Ironmon Smart check unless using an independent private checkpoint/run. | NOT_RUN |

No one-click Ironmon preset is required: #520 intentionally added no
user-facing preset UI. The trainer-battle smoke and settings witnesses remain
user-owned runtime checks, separate from accepted host/policy and source/ARM
evidence.

## Mandatory Phase R1 final-pin overlays within existing cases

These mandatory observations extend the named existing cases; they add no
case IDs and do not change phase ownership or the 115-ID count. Record each
observation as a sanitized variant of its mapped case. Every overlay remains
`NOT_RUN`; no mapped case may pass while a required overlay is undisposed.
The package's severity, STOP and approved-exclusion rules still apply.

| Overlay / existing cases | Required final-pin observations | Initial status |
|---|---|---|
| Settings UX — A01, B16, B27 | Page 3 labels/help fully visible with no clipped labels; cycle long to short values with no stale pixels. Trainer Level Scaling raw 0 = `Auto (Diff.)`; Trainer AI raw 0 = `Auto (Diff.)`; Hard Cap raw 0 = `Auto`. Legacy labels render as `Legacy Vanil.`, `Legacy Easy`, `Legacy Normal`, `Legacy Hard`, `Legacy Expert`, `Legacy Smart`; `Standard` and `Ironmon Smart` render correctly. Difficulty, Trainer Level Scaling and Trainer AI remain independent; relevant selections and original-raw behavior remain correct after Save/Reload. | NOT_RUN |
| Route 10 HM05 — D06, B07, B08, B27 | Before reward, Hiker present at `(17,22)`. Full-Bag/no-room path awards no HM05 and leaves the NPC available for retry. Retry awards exactly one HM05 and sets the shared reward flag. After success, Hiker remains absent after re-entry and Save/Reload; original Route 2 Aide cannot award a second HM05. Check HM field-use independently: corresponding HM item present, compatible non-egg Party Pokémon, required badge, and valid location/field condition; each missing prerequisite safely blocks use. | NOT_RUN |
| National Dex — A01, A09, A12, A13, A17 | No National Dex at genuine Fresh New Game or before Parcel/normal Pokédex handoff. Parcel removed at the normal Pokédex handoff, ordinary Pokédex unlocked, full National Dex activated exactly there, exactly five Poké Balls awarded once, and Oak/story state ends correctly. National View/Registration works afterward. Save/Reload preserves national state; revisit/reload repeats neither Dex handoff, reward nor script; five-ball accounting remains exactly once and normal onward progression is intact. | NOT_RUN |

The UPR-FVX stale/direct National-Dex request guard is an integrated
compatibility boundary, not an R1 ROM runtime result. Its Randomizer/output
behavior belongs to R2 and remains gated there.

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
| A01 | R1 ROM | Start/intro plus fresh Vanilla / Off / Off / Standard Options witness; all other procedure-prescribed A01 variants | NOT_RUN | | |
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
| A12 | R1 ROM | Parcel removed, normal Dex unlocked and full National Dex activated exactly at handoff; five Poké Balls exactly once, Oak/story state correct; all procedure-prescribed A12 variants | NOT_RUN | | |
| A13 | R1 ROM | National-Dex persistence, no duplicate Dex/balls/script, intact onward progression; all procedure-prescribed A13 variants | NOT_RUN | | |
| A14 | R1 ROM | All procedure-prescribed variants for A14 | NOT_RUN | | |
| A15 | R1 ROM | All procedure-prescribed variants for A15 | NOT_RUN | | |
| A16 | R1 ROM | All procedure-prescribed variants for A16 | NOT_RUN | | |
| A17 | R1 ROM | Pre-handoff inactive / post-handoff persistent National Dex and exactly-once five-ball accounting; all procedure-prescribed A17 variants | NOT_RUN | | |
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
| B16 | R1 ROM | Options isolation plus Standard/Ironmon Smart/legacy display and trainer-battle integration variants; all other procedure-prescribed B16 variants | NOT_RUN | | |
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
| B27 | R1 ROM | Save/reload persistence for AI/Difficulty/Scaling plus all procedure-prescribed B27 variants | NOT_RUN | | |
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
| D06 | R1 ROM | Route 10 HM05 final-pin overlay plus all procedure-prescribed D06 variants | NOT_RUN | | |
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
#565 rebaseline. Record the complete Phase R1 identity and user-owned ROM
results first;
only after `ROM_PROFILE_READY` may the Phase R2 identity and randomized-output
results be recorded.
