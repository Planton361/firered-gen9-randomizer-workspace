# ROM-free freeze readiness — 2026-09-15

**NOT FEATURE-COMPLETE-ACCEPTED; NOT FROZEN.** Source candidates and reviewable
test preparation are available. Runtime-only gates remain open. This report
contains no ROM/save/state/build artifact, binary, private path/hash or secret.
No component pin or existing checkout was changed and nothing was merged.

## Exact current pins

These are Gitlinks from fetched workspace `origin/main` at
`7437cd551545ab5e4dcd57a2ff5dbf9672193d74`, not HEADs of pre-existing dirty
component checkouts. CFRU has no `main`; its pilot integration branch is
`compat/firered-gen9-randomizer`, distinct from its default Experiments branch.
UPR's integration is `compat/firered-cfru-dpe`. New work starts from the
workspace's current source pins, not an unrelated upstream default branch.

| Component | Current pinned SHA |
|---|---|
| CFRU | `827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec` |
| DPE Gen9 | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX | `1a597a667129b50284dd88afb231372b5bd01d7f` |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| Cyan FireRed natdex reference | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| Cyan UPR-ZX natdex reference | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` |
| pret FireRed reference | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |
| FVX upstream reference | `e0788edc6529c2605f201996e4807ff30165354c` |
| Ajarmar ZX reference | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` |

## Current candidates / open review

PR state queried from GitHub 2026-09-15. All session PRs are draft and unmerged.

| Task / PR | Exact candidate SHA | Gate / dependency |
|---|---|---|
| M-013 [CFRU #45](https://github.com/Planton361/CFRU-expansion/pull/45) | `8a677e73ee3650e1f4e00769a7235b2860a68da1` | Source/host checks passed; clean full build and transaction/capacity runtime matrix open. |
| Pickup guard [UPR #185](https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/185) | `0df4ed3d83fba6176f19a3c3146bd3c27561e47e` | Synthetic actual-method regression passed; module/JUnit build and output smoke open; Pickup Unchanged required. |
| Five learnsets [CFRU #46](https://github.com/Planton361/CFRU-expansion/pull/46) | `94404bcebd92f3817da0d03963cc536d7b7f44c3` | Stacked on #45; exact tracked-source restore/ARM syntax passed; full build/runtime and authoritative-data uncertainty remain. |
| Data report [workspace #487](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/487) | `bb89b20bb46417d60d4de0bed5077d42b5307c5d` | Documentation and source-only reproducible audit; does not change Gitlinks. |
| Randomizer report [workspace #488](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/488) | `44ea58b376d976edf22d13833d0a2f214f6ee01a` | Every requested feature classified; runtime support not inferred. |
| Acceptance package [workspace #489](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/489) | `391a200a20bd217feee9ca9b973b200c089e6de1` | 115 uniquely identified cases plus variants; all NOT_RUN. |

At this snapshot these are the only open component PRs in CFRU/DPE/UPR and
the only pre-report open workspace PRs. Later revisions must be re-queried,
not substituted silently for this table. This readiness report's exact commit
is its PR head (a file cannot self-embed its own commit ID).

## Closed experimental work — do not integrate

| Closed/unmerged PR | Candidate | Disposition |
|---|---|---|
| [CFRU #44](https://github.com/Planton361/CFRU-expansion/pull/44) | `3c4ceaeb2bc2af513fb934627bf77bc7f6bacbc3` | M-011 Hospitality engine experiment; out of current scope. |
| [DPE #5](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/pull/5) | `9d0c3ceb9a1b6b4aed7281fcbfe66fa48b19e9ee` | Dependent Hospitality assignments; do not cherry-pick. |
| [UPR #184](https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/184) | `4da2201531142e6effd3007c2ed03a07615a241f` | Dependent experimental support; not this session's Pickup guard. |

## Unresolved defects and acceptance gates

Severity below is source-risk triage, not an invented observed runtime failure.

| Finding / gate | Severity / state | Required closure |
|---|---|---|
| Five empty active learnsets at current CFRU pin, 31 affected species/form pointers | S1 potential progression/data-integrity impact; candidate available | Review #46 restoration, full build, starting/level-up/shared-form and randomized-pool smoke. |
| UPR Pickup writer targets legacy FRLG table, not active CFRU common/rare arrays | S1 unsupported writer correctness; candidate available | Review #185, module tests, verify explicit rejection and no partial output; retain native Pickup via Unchanged. |
| Premier reward precedence and absent partial capacity clamp | S2 known source parity gap; candidate available | Review #45 and exact floor(quantity/10) per-transaction matrix including capacity and failed purchase. |
| CFRU clean/full build completion | BLOCKED tooling | Both fresh source builds completed C/assembly/string/image stages then failed at missing wav2agb; mid2agb also absent. Approved toolchain full build/link required; no download was attempted/requested. |
| UPR affected-module/JUnit build | BLOCKED tooling | Gradle unavailable, installed Java 23 vs source requirement 25. Host Java regression passed, not JUnit. Run module tests/build; inspect test failures/errors/skips because ignoreFailures is configured. |
| M-009 source-owned global frame lifecycle | NEEDS_FINAL_RUNTIME_SMOKE | Broad camera/OAM, menus, fades, warps/connections, battle return, scripts/cutscenes, resource lifecycle and Quest Log. Historical targeted sparkle PASS is not broad acceptance. |
| Full integrated early game and story | NEEDS_FINAL_RUNTIME_SMOKE | Fresh New Game A flow; one continuous Brock→Hall of Fame run with save/reload, all integrated QoL; optional Bill/Sevii separately. |
| Randomized integrated output | NEEDS_FINAL_RUNTIME_SMOKE | Single-family then combined-profile reload/gameplay; supported forms, trainer rows, learnset free-space placement, shops/TMs/tutors/trades/statics/fields/logging. No ROM-free source test can certify private insertion. |
| Exact final Gen1–9 authoritative data parity | UNKNOWN | Approved raw input snapshot is not tracked. The structural repair reaches 1,025 identities but historical move restoration is not final modern-data proof. Obtain separately approved reproducible authority or explicitly accept a bounded historical baseline; document decision. |
| Known UI/model caveats | OPEN disposition | Game Corner acquire presentation, tutor scripted text, aliased ability semantics/ban options, scalar trainer IV normalization/tera metadata, incomplete Field Items logging, service-specific Select from PC. Verify/dispose; no silent full support claim. |

No S0 runtime defect was observed because no emulator was used. Absence of
observations is not evidence of zero runtime defects. M-001–M-009 remain
historically complete for their named targeted candidates; their integration
history is not reopened or relabeled as final revision-wide PASS.

## Conditions for ROM FEATURE COMPLETE

1. User reviews and integrates only approved bounded candidates, records actual
   resulting source SHAs, then updates workspace Gitlinks in a separate bounded
   pin PR. Candidate, merge and runtime-tested SHAs remain distinct.
2. Clean/full affected source builds and module regressions pass on approved
   tooling; no hidden ignored-failure test result is accepted.
3. Data audit findings have explicit disposition: real data bugs fixed, aliases
   and engine limits retained, authoritative UNKNOWN resolved or explicitly
   scoped/accepted. Do not call all modern data verified without evidence.
4. The 115-case manual package and variants pass for the final integrated
   revision, or a reviewer approves a source-backed exclusion. All mandatory
   early game, broad frame, main story, item/progression and save gates close.
5. Supported randomizer profile is recorded precisely (Pickup Unchanged,
   standard/fallback wild, safe species/forms, stated alias/model caveats),
   tested per family and combined. No unsupported feature is advertised.
6. No unresolved S0/S1, and every S2/S3 either fixed/retested or explicitly
   accepted within a documented scope. Optional story/QoL branch tests are not
   erased because the main ending was reached.

## Additional conditions for ROM FROZEN

1. FEATURE COMPLETE is accepted, not merely source-implemented.
2. Final source/component pins, configuration, approved toolchain versions,
   randomizer support profile and reproducible user-owned build procedure are
   recorded without committing private artifacts or identifiers.
3. Final integrated output receives the named acceptance run; no untested
   source/data/settings change follows it. Record sanitized source revision/run
   labels, not ROM hashes or uploads.
4. No pending required feature/data change, unresolved critical/high defect or
   unreviewed compatibility write remains. Source tree and pin closure are
   reviewable and approved by the user; this agent never merges.
5. Freeze change control states which tests a later change invalidates; any
   functional source or layout/profile change requires a new candidate and
   appropriate rerun, not an in-place frozen-artifact edit.

Tracker readiness is a separate post-freeze contract. A tracker profile should
not delay the ROM freeze unless the user explicitly makes tracker support part
of the ROM acceptance scope. No such scope expansion is assumed here.

## Optional backlog and explicit exclusions

Optional: Cinnabar Move Reminder access as a separately approved small service
milestone; future exact active-Pickup randomization profile; improved tutor
dialogue/logging; stricter per-revision randomizer profiles; tracker integration
after freeze. None is silently implemented by this report.

Excluded: missing Gen9 battle mechanics, M-011 experiments, full modern HM menu,
early National Dex policy change, broad intro/BGM redesign, friendship/economy
changes, new encounter/form mechanics, broad shop refactor, DPE expansion-mode
changes, protected artifacts, emulator automation, and any merge.

## Review and user action order

1. Review reports #487/#488 and acceptance #489 (documentation can merge in any
   order at user discretion; no pin mutation).
2. Resolve approved build tooling and run full CFRU/UPR checks. Review CFRU #45,
   then stacked #46; after #45 is user-merged, retarget/rebase #46 to the pilot
   compatibility branch and inspect the bounded diff. UPR #185 is independent.
3. Perform user-owned runtime matrices on the exact candidates; integrate only
   accepted work and record actual integration SHAs in a new workspace pin PR.
4. Resolve/accept authoritative-data uncertainty explicitly. Run the complete
   acceptance package on final integrated pins and submit sanitized text report.
5. Close high-severity and mandatory gates, declare FEATURE COMPLETE, then apply
   the stricter freeze checklist. Start tracker profile implementation only
   after its revision/layout contract is fixed.

No new user interaction is needed to finish the independent source-only queue;
runtime/merge/protected-artifact gates are handed off, not crossed here.
