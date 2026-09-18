# Extended session handoff — 2026-09-15

All six queue items were worked in order through safe source-only gates.
**Nine draft PRs; nothing merged; current component pins unchanged.**
Three concrete defects have bounded source candidates. Full builds and runtime
acceptance are not complete. ROM FEATURE COMPLETE / ROM FROZEN are not declared.

## Completed reviewable work

| Task | Result | Draft PR / exact candidate |
|---|---|---|
| 1 M-013 | Any ball-pocket purchase: floor(qty/10) Premier Balls per transaction, capacity-clamped, awarded once. Legacy non-ball policy preserved. | [CFRU #45](https://github.com/Planton361/CFRU-expansion/pull/45): `d8468e1d12dbe33f646e2778bbde51ece7010a73` |
| 1 canonical evidence | NatDex/pret/pinned CFRU comparison, current upstream callback recheck, scope and runtime handoff/ROADMAP. | [Workspace #492](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/492): `0d071dba7d788be7be1f937ef360878e2f1f3671` |
| 2 compatibility fix | Reject unsupported CFRU Pickup randomization before legacy-table read/write, including empty writes. Keep Pickup Unchanged. | [UPR #185](https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/185): `0df4ed3d83fba6176f19a3c3146bd3c27561e47e` |
| 2 reconciliation | Every requested randomizer feature classified against exact current pilot source; historical GUI/log evidence not promoted to runtime proof. | [Workspace #488](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/488): `44ea58b376d976edf22d13833d0a2f214f6ee01a` |
| 3 data repair | Restore five empty active learnsets from tracked pre-sync source: Pikachu, Rotom, Necrozma, Zacian, Zamazenta; 31 existing form pointers unchanged. | [CFRU #46](https://github.com/Planton361/CFRU-expansion/pull/46): `5ea11537ef0def6a718d007ce5f4a765f6585205` (stacked on #45) |
| 3 final status | Reproducible pinned-object audit and full discrepancy inventories. Candidate structural coverage reaches 1,025 National Dex identities. Exact modern authority remains UNKNOWN. | [Workspace #487](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/487): `559013955f6b25848748579a75523a40c1539fca` |
| 4 acceptance | 115 cases plus variants covering A–H and M-013; PASS/STOP, severity and minimal sanitized report. All runtime rows NOT_RUN. | [Workspace #489](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/489): `391a200a20bd217feee9ca9b973b200c089e6de1` |
| 5 freeze readiness | Current pins, open/closed candidates, risk/gate table, optional/excluded scope and feature-complete/freeze conditions. | [Workspace #490](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/490), this report branch; exact head is recorded in the final session response/PR metadata. |
| 6 tracker discovery | Current Tracker/NatDex/BizHawk source, exact layout assertions, fail-closed profiles and seven bounded follow-ups; design only, no live activation. | [Workspace #491](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/491): `d6034ae39cbc2e5a551289db685f4687388ce59d` |

The earlier CFRU candidates `8a677e73` and `94404bce` were superseded in this
session: final review kept the wider quantity calculation Premier-only, then
rebased the session-owned stacked learnset draft onto that correction. #46 was
updated with an explicit expected-old-SHA lease; no pre-existing user branch was
rewritten. Use final candidates above, not earlier PR notifications.

## Checks actually passed

- M-013 compiles the actual callback into a synthetic host harness: 11,110 ball
  cases (quantity including 255/256/999, capacity0..100, A/B), plus single-award,
  add failure, no input, separate transactions and all non-ball controls, now
  including large-quantity legacy behavior. UBSan/bounds checks enabled.
- M-009 source contract, eight negative ownership/order/scanner mutations and
  compiled host scanner pass on final candidates. Frame checks were retained;
  map census was not rerun because map/event sources were unchanged.
- Five restored tables match tracked reference exactly; no unrelated table or
  pointer edits; 31 form bindings retained. ARM syntax checks pass for item.c
  and the entire learnset translation unit.
- UPR host regression compiles actual Pickup get/set/guard methods against
  synthetic services: fail before table access/write for CFRU; vanilla16-row
  read/write and ten probability-sum controls preserved. New JUnit regression
  committed but NOT executed by a module runner in this environment.
- Baseline/final pinned-source audits run successfully, no active invalid
  move/level encodings, zero shared move/ability ID drift, no missing National
  Dex identity after restoration; compact JSON preserves baseline semantics.
- ARM compile-only layout assertions pass for Pokemon/Box/Battle/BaseStats/
  Move/Trainer, all trainer row flags, packed learnsets, Item and MapHeader.
- Acceptance case IDs unique (A17/B27/C10/D16/E7/F7/G6/H15/P10); report links
  checked; whitespace and workspace Git safety pass before/after work.

## Build results and blockers

No clean/full component build passed. Fresh CFRU source build attempts,
including final stacked `5ea11537`, completed C/assembly/strings/images and
stopped at audio with missing `wav2agb`; `mid2agb` is also absent. Existing
compiler warnings were observed, not silently treated as new resolved defects.
The final verification used a separate fresh detached source-only worktree;
implementation remained on bounded isolated branches. No generated build was
opened as a user artifact, and no ROM insertion ran.

UPR affected-module test/build command was attempted but Gradle is unavailable;
installed Java23 does not satisfy the project's Java25 requirement. No wrapper,
audio converter or other tool binary was downloaded/accessed as an artifact.
Later module results must include zero failures/errors, not just a build exit
code, because Gradle test failure ignoring is configured.

Authoritative Gen1–9 parity is still UNKNOWN: approved aliases/scripts and old
reports are tracked, but raw reproducible upstream dataset inputs are not.
The five-table restoration fixes demonstrably lost source data, not a claim of
final Scarlet/Violet move parity. No new dataset or missing mechanic was added.

## Current component pins (unchanged)

Workspace origin/main and original checkout both remain
`7437cd551545ab5e4dcd57a2ff5dbf9672193d74`.

| Component | Pinned source SHA |
|---|---|
| CFRU | `827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec` |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX | `1a597a667129b50284dd88afb231372b5bd01d7f` |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| Cyan FireRed natdex reference | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| Cyan UPR-ZX natdex reference | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` |
| pret FireRed reference | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |
| FVX upstream reference | `e0788edc6529c2605f201996e4807ff30165354c` |
| Ajarmar ZX reference | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` |

Current public heads used for discovery are separately recorded in #491/#492;
none replace these pins. Original dirty/untracked files, component branches and
existing worktrees were preserved. All new worktrees remain available for review;
no cleanup or merge was performed. No protected artifact was requested/opened.

## Runtime tests and exact next user actions

1. Review #492/#488/#487, then component #45/#46/#185; resolve approved local
   build tooling and run clean/full CFRU and affected UPR module/JUnit checks.
2. On user-owned exact candidates, run M-013 quantity/capacity/transaction matrix;
   five learnset families/shared forms; explicit Pickup rejection and native
   Unchanged control. Share only sanitized text results using #489's template.
3. After gate acceptance, user merge order is CFRU #45 → retarget/rebase #46 to
   the pilot compatibility branch → #46. UPR #185 is independent. Documentation
   PRs may be reviewed/merged independently; this agent never merges.
4. Create a separate workspace pin-update PR with actual integrated source
   SHAs. Do not substitute a draft head for an integration commit. Do not merge
   closed M-011 CFRU #44 / DPE #5 / UPR #184 experimental mechanics work.
5. Resolve the authoritative-data UNKNOWN with separately approved reproducible
   source evidence or explicitly accept the historical bounded baseline and
   remaining limitations. Do not equate source bounds with complete modern data.
6. Run final integration A–H: Fresh New Game/Mom/Parcel; all QoL and save/reload;
   broad M-009 camera/OAM/menu/warp/battle/palette/script/Quest Log regression;
   continuous Brock→Hall of Fame; renewals; optional Bill/Sevii; Gen1–9
   display/form sanity; per-family and combined randomized output smoke.
7. Close S0/S1 and mandatory gates, dispose remaining caveats, then declare
   FEATURE COMPLETE for an explicit supported profile. Freeze only after final
   pins/config/toolchain/profile and final revision-wide acceptance are locked
   and change control is defined. Full criteria: [freeze readiness](rom-freeze-readiness.md).
8. Begin tracker roadmap only after exact revision/profile identity is settled.
   T01 importer and T02 decoder/domain fixes are bounded source-only follow-ups;
   live addresses and activation remain gated. Tracker is not silently made a
   ROM-freeze prerequisite.

## NO CODE REQUIRED / deferred scope

Tasks1–3 were not closed NO CODE REQUIRED: each found a concrete scoped defect.
No DPE fix was needed for the active-pilot defect; no stats/ability/name encoding
bug beyond documented aliases/limits was established. Tasks4/5 are intentionally
documentation-only. Task6 stops at design/test preparation; production tracker
changes are deferred, not falsely labeled unnecessary.

Optional backlog: Cinnabar Move Reminder, exact active-Pickup randomization,
improved text/logging/profile support, later box/bag/advanced tracker details.
Explicitly out of scope: missing Gen9 battle mechanics, M-011 experiments,
broader HM/intro/economy/content changes, protected artifacts and any merge.
