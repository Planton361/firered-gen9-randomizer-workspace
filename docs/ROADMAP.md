# Roadmap

This file owns the stable product finish line and dependency order. Operational
priority/status belongs to the GitHub Project and Workspace Issues; this file is
not a day-to-day queue.

## M-000R closure

**CONFIRMED CURRENT STATE:** M-000R — Workflow Adoption: **COMPLETE**. The
canonical workflow baseline was activated by merge commit
`65da597b6b57d40d4698a221809741912abe8e3c`. Historical work is neither
renumbered nor rewritten.

## Completed regular milestone

**CONFIRMED CURRENT STATE:** M-001 — 29-slot TM/HM Itemball Acceptance /
Integration Restart is **COMPLETE**. The 29-slot TM/HM itemball rollout is
integrated, and CFRU PR #35 is merged. No subsequent milestone is started by
this closure.

**CONFIRMED CURRENT STATE:** The Excel roadmap is a derived visual dashboard,
not canonical truth.

## M-002 closure

**CONFIRMED CURRENT STATE:** M-002 — Viridian Forest Nurse is **COMPLETE**.
CFRU PR #36 integrated the bounded Nurse implementation at merge revision
`9548877aa481750b825c765c4d72fce90d633c16`. It replaces the original
non-trainer at `(29,58,3)` with Nurse Joy, keeps the existing map contract
fail-closed, and includes the corrected two-line poison-refusal text.

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS for tested
candidate `98cc40664080f7c956edbb81769acb7d112ce2ee`:** Nurse
visibility/interactivity, healing, poison refusal, and the prompt, success,
and corrected refusal texts passed targeted runtime smoke. This evidence is
revision-specific and caveated; it is not a broad support-profile claim. The
integrated merge revision is not claimed to have been separately runtime-tested.

**CONFIRMED CURRENT STATE:** The workspace closure pins only the integrated
CFRU merge revision. Workspace PR #477 is merged.

## M-003 closure

**CONFIRMED CURRENT STATE:** M-003 — Instant PokeCenter Healing is
**COMPLETE**. CFRU PR #37 integrated the bounded normal-Pokemon-Center Nurse
fast path at merge revision `215bd44d340c16076b1817b9c6db038d54fe5f76` while
retaining the short healing effect and Trainer Tower's original Nurse
interaction.

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS for tested
candidate `d6571f4a8c371075da1cf6341c5d01f89903d426`:** instant healing,
short healing effect, full-party healing, repeat use, a second Kanto Center,
and a Sevii Center passed. Trainer Tower retained its original interaction;
Name Rater, PC, and warps showed no regression; status, PP, and fainted-party
restoration checks passed where tested. This evidence is revision-specific and
caveated; the integrated merge revision is not claimed to have been separately
runtime-tested.

**CONFIRMED CURRENT STATE:** The workspace closure pins only the integrated
CFRU M-003 merge revision. No subsequent milestone is started by this closure.

## M-004 closure

**CONFIRMED CURRENT STATE:** M-004 — Guaranteed Renewable Step Items is
**COMPLETE**. CFRU PR #38 integrated the bounded renewable hidden-item
regeneration behavior at merge revision
`520fc7feeb7494b5f8f0555e348c13f0e847304b`. The implementation preserves the
1,500-step cycle, guarantees eligible Underground Pass and approved Sevii
renewable groups, and leaves Mt. Moon vanilla/random.

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS for tested
candidate `aad9c76d537cf812673e1cd3e69faffd435ff692`:** Underground Pass spawn
and repeat regeneration, a representative Sevii group, Mt. Moon's
vanilla/random control, Itemfinder, normal one-time hidden items, and a
representative UPR-FVX Field Items smoke passed. This evidence is
revision-specific and caveated; the integrated merge revision is not claimed
to have been separately runtime-tested.

**CONFIRMED CURRENT STATE:** The workspace closure pins only the integrated
CFRU M-004 merge revision. No subsequent milestone is started by this closure.

## M-005 closure

**CONFIRMED CURRENT STATE:** M-005 — PC Item -> Oak's Lab is **COMPLETE**.
CFRU PR #39 integrated the bounded Player PC initialization and Oak's Lab
Potion Item Ball behavior at merge revision
`4a9698467600500d18ec8c08f9269f0d6ad008e6`.

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS for tested
candidate `10a338eca514c3ca1f614586d1054a89f039010a`:** a fresh New Game has no
starter Potion in PC storage; the Oak's Lab Potion Item Ball, pickup
disappearance/persistence, starter/Rival/Oak Lab flow, warps, normal Player PC
storage, and representative UPR-FVX Field Items behavior passed. This evidence
is revision-specific and caveated; the integrated merge revision is not claimed
to have been separately runtime-tested.

**CONFIRMED CURRENT STATE:** The workspace closure pins only the integrated
CFRU M-005 merge revision. No subsequent milestone is started by this closure.

## M-006 closure

**CONFIRMED CURRENT STATE:** M-006 — Talk to Mom / Faster New Game handoff is
**COMPLETE**. CFRU PR #40 integrated the bounded mandatory Mom interaction and
fast scene-1 Oak's Lab handoff at merge revision
`237fc61ac52bea6978f4b434c06fc3f1f11e5dcc`.

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS for final
tested candidate `574318a1af2801c161cd40d9687ed2b65dd3b92a`:** the Player
House exit blocker, Mom handoff, fast Lab player/camera state, Oak's normal
`(6,3)` facing-down position, direct starter choice, starter/Rival flow,
Lab exit and warps, M-005 Potion, and post-rival Mom healing passed. Earlier
M-006 candidates with runtime defects were superseded and are not promoted to
PASS. This evidence is revision-specific and caveated; the integrated merge
revision is not claimed to have been separately runtime-tested.

**CONFIRMED CURRENT STATE:** The workspace closure pins only the integrated
CFRU M-006 merge revision. No M-007 or other subsequent milestone is started
by this closure.

## M-007 closure

**CONFIRMED CURRENT STATE:** M-007 — Shortened Oak Parcel Flow is
**COMPLETE**. CFRU PR #41 integrated the bounded Route 1 Clerk and Pallet Town
Oak Parcel handoff at merge revision
`62298cf81d4a2b487c8793bad8b6e29906c705f4`.

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS for tested
candidate `00e316532be65f4fdd8e4561b2b2579817a1f64f`:** M-006's Mom/start and
starter/Rival flow, the hidden temporary Oak, original Route 1 Potion Clerk,
all Route 1 and Pallet handoff trigger positions, single Parcel award,
save/reload, no Mart duplicate, Pokedex/unlock plus five Poke Balls,
post-Parcel story state, the skipped Old Man tutorial, M-005 Potion, and M-006
flow passed targeted runtime smoke. This evidence is revision-specific and
caveated; the integrated merge revision is not claimed to have been separately
runtime-tested.

**CONFIRMED CURRENT STATE:** The workspace closure pins only the integrated
CFRU M-007 merge revision. No M-008 or other subsequent milestone is started
by this closure.

## M-008 closure

**CONFIRMED CURRENT STATE:** M-008 — Optional Bill / Sevii handoff is
**COMPLETE**. CFRU PR #42 integrated the bounded automatic outdoor-Bill scene
bypass at merge revision `a869c3526d7f76c54082bc71e236742564319e02`.

**CONFIRMED CURRENT STATE — user-supplied sanitized runtime PASS for tested
candidate `07b86d44b9c98354c815ae56f7f26072fcc0147a`:** Blaine completion, no
automatic Bill dialogue/prompt/travel, outdoor Bill removal, Center Bill
availability and NO persistence, save/reload, original YES travel, Sevii and
return scenes, M-003 instant Nurse, Name Rater, and M-005 through M-007 passed
targeted runtime smoke. This evidence is revision-specific and caveated; the
integrated merge revision is not claimed to have been separately runtime-tested.

**CONFIRMED CURRENT STATE:** The workspace closure pins only the integrated
CFRU M-008 merge revision. No further mandatory ROM-QoL milestone is invented
by this closure.

## M-009 closure

**CONFIRMED CURRENT STATE, with targeted runtime caveat:**
[M-009 — Hidden Item Sparkle / source-owned Overworld frame integration](milestones/M-009.md)
is **COMPLETE**. CFRU PR #43 is integrated at
`827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec`. The old slow-camera byte owner
was intentionally superseded by a named functionrewrite with the exact
pret/Cyan frame order and a frame-tail Hidden Item scanner.

**CONFIRMED CURRENT STATE — user-supplied
`PASS_TARGETED_VISIBLE_SPARKLE_WITH_CAVEATS`:** Hidden Item sparkle behavior
was observed in runtime and visually judged appropriate on the exact
candidate `3da0547d782fb62fc993431278d63575912025da`. The merge is exactly
one commit ahead, has the candidate as merge base, and has no additional file
changes. The integrated merge was not separately runtime-tested.

This closes the former source-hook blocker. Earlier failed sparkle pilots
remain **LEGACY / OBSOLETE** evidence. Separate coverage of every Start/Bag/
Party/Quest-Log/resource-pressure/lifecycle permutation is not claimed;
broader global-frame regressions belong to the later feature-complete
playthrough gate. This is not a broad support or release claim.

M-009 did not start another milestone. The subsequent M-012 audit is closed
below under the confirmed pilot scope decision recorded in M-010.

## M-010 closure — Gen-9 engine-boundary compatibility audit

**CONFIRMED USER DECISION:** M-010 is closed as a compatibility audit under
[the corrected pilot contract](PROJECT.md#pilot-product-contract), and the
repository sync was merged through Workspace PR #485. Its
[sanitized findings and decision record](milestones/M-010.md) are supporting
compatibility evidence: Commander, Hospitality and Embody Aspect are missing;
Palafin / Zero to Hero and Terapagos are partial. These are known limitations
of the selected baseline, not pilot implementation requirements or runtime
acceptance. Reopening mechanics requires an explicit separate post-pilot project.

## M-011 — superseded Hospitality implementation

**CONFIRMED USER DECISION:** The Hospitality implementation train is superseded
by the corrected pilot scope. CFRU PR #44, DPE PR #5 and UPR-FVX PR #184 are
experimental, unmerged work; their exact candidates and links are retained in
[M-010](milestones/M-010.md#m-011--superseded-hospitality-train). They must not
be integrated or pinned. At verification on 2026-09-10, all three PRs remain
open and unmerged. Once closed unmerged, their disposition is **LEGACY /
OBSOLETE**. This documentation closure changes no component PR state and
claims no runtime acceptance.

## M-012 — Ironmon NatDex QoL Parity Audit

**COMPLETE — analysis-only parity audit; 36 assessed entries.** The
[audit findings](milestones/M-012.md) are **CONFIRMED CURRENT STATE**. The
report reconciles the historical QoL inventories against pinned
source and accepted milestone evidence. M-001 through M-009 remain complete
and are not reopened.

**INTENDED FUTURE STATE — optional backlog:** Paid Move Reminder on Cinnabar
is not required for pilot feature-complete status unless explicitly promoted
later. No milestone number is assigned to this optional candidate.

No missing Gen-9 battle-mechanic work is introduced by M-012. Its historical
documentation closure changed no component source or Gitlinks; later component
and workspace pin integration is recorded below and in [M-013](milestones/M-013.md).

## M-013 closure — Premier Ball bonus and post-integration gate

**CONFIRMED CURRENT STATE:** M-013 is implemented in CFRU PR #45 and carried
by the current CFRU PR #48 merge pin
`8bc8c38210ddba0b05c933dbda06cb4539254c7a`. The bounded behavior is
documented in [M-013](milestones/M-013.md). UPR-FVX PR #185 is integrated at
`0e3be63e94e34215cc35308d64e8db15e9a3c48c`; DPE remains unchanged.

**CONFIRMED USER-SUPPLIED REVISION-BOUND RUNTIME PASS:** The user reported the
targeted [Runtime Gate 1](testing/runtime-gate-1-2026-09-19.md) scope as PASS
against the exact Workspace/test basis and component revisions recorded there.
The run predates this documentation branch; the later documentation HEAD is
not the tested Workspace revision. This remains targeted evidence and is not a
full feature-complete or release gate.

## M-014 — Feature-Complete Manual Acceptance Block

**INTENDED FUTURE STATE:** [M-014](milestones/M-014.md) is the next product
acceptance block after the workflow-only
[Cross-device Development Readiness](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/497)
gate. M-014 refreshes the existing A–H manual package to exact revision identity
and covers the remaining targeted regressions, continuous progression,
display/form sanity and supported randomized-output smoke. It does not
implement features or claim universal Gen-1–9 mechanics. Active execution is
owned by [Issue #498](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498).

## Integrated M-001 rollout and legacy handoff

**CONFIRMED CURRENT STATE:** CFRU PR #35 is merged at
`8e3fa8378d67dfe4011d6994469c3806f32764c4`, integrating its accepted candidate
head `08b869032735118539411adbcffa421c8a697caa` for the 28 TM plus HM07 scope.
M-001 acceptance is revision-specific and does not establish a broader support
profile.

**LEGACY / OBSOLETE:** Workspace PR #467 is closed unmerged. Its
`feature/cfru-tm-itemball-29-slot-rollout-pin` branch is historical supporting
evidence; the M-001 workspace branch and PR supersede it for integration.

## Pilot finish line

- **CONFIRMED CURRENT STATE:** Integrated Pilot Pins — **DONE**. The bounded
  coherent Gen 1–9 data closure is integrated within the selected CFRU/DPE
  semantics, with documented blocked forms, ability behavior and battle-mechanic
  limitations retained.
- **INTENDED FUTURE STATE — workflow gate:** Cross-device Development Readiness,
  owned by [Issue #497](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/497).
  It proves GitHub-based handoff; it is not a product capability gate.
- **INTENDED FUTURE STATE:** M-014 manual acceptance, owned by
  [Issue #498](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498).
- **INTENDED FUTURE STATE:** lock the accepted pilot revision/profile after
  M-014; M-014 alone does not declare freeze.
- **INTENDED FUTURE STATE:** BizHawk validation, owned by
  [Issue #499](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/499).
- **INTENDED FUTURE STATE:** Ironmon Tracker integration, owned by
  [Issue #500](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/500).
- **INTENDED FUTURE STATE:** Stable Support Profile / Final Freeze, owned by
  [Issue #501](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/501),
  only after completed evidence.

Hospitality/M-011, missing Gen-9 mechanics, optional QoL expansion and upstream
contribution preparation are not reactivated by this finish line.

## Preserved status

- **CONFIRMED CURRENT STATE:** Name Rater complete pass is completed, with its
  recorded manual-smoke caveats.
- **CONFIRMED CURRENT STATE, with targeted runtime caveat:** Hidden Item Sparkle
  is integrated through M-009's source-owned frame solution. Its acceptance is
  `PASS_TARGETED_VISIBLE_SPARKLE_WITH_CAVEATS`; broader regressions remain at
  the later feature-complete playthrough gate.
- **LEGACY / OBSOLETE:** Earlier failed sparkle pilots and their source-hook
  blocker describe the pre-M-009 state, not current integration status.
- **CONFIRMED CURRENT STATE:** Friendship Boost remains optional and
  non-standard for Ironmon; it is not a mandatory ROM-QoL milestone.
- **CONFIRMED USER-SUPPLIED REVISION-BOUND RUNTIME PASS:** Runtime Gate 1 is
  recorded for its targeted scope and exact tested revision set only; broad
  feature-complete coverage remains unresolved.
- **LEGACY / OBSOLETE:** Prior roadmap numbering, detailed queues,
  and status remain in
  [00_project-control/roadmap/roadmap-status.md](../00_project-control/roadmap/roadmap-status.md)
  without renumbering.
