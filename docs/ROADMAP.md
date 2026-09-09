# Roadmap

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

## Integrated M-001 rollout and legacy handoff

**CONFIRMED CURRENT STATE:** CFRU PR #35 is merged at
`8e3fa8378d67dfe4011d6994469c3806f32764c4`, integrating its accepted candidate
head `08b869032735118539411adbcffa421c8a697caa` for the 28 TM plus HM07 scope.
M-001 acceptance is revision-specific and does not establish a broader support
profile.

**LEGACY / OBSOLETE:** Workspace PR #467 is closed unmerged. Its
`feature/cfru-tm-itemball-29-slot-rollout-pin` branch is historical supporting
evidence; the M-001 workspace branch and PR supersede it for integration.

## Later tracks

- **INTENDED FUTURE STATE:** Controlled Gen 1–9 data risk closure.
- **INTENDED FUTURE STATE:** Randomizer regression hardening.
- **INTENDED FUTURE STATE:** Remaining source-backed QoL.
- **INTENDED FUTURE STATE:** BizHawk validation.
- **INTENDED FUTURE STATE:** Ironmon Tracker integration.
- **INTENDED FUTURE STATE:** Stable support profile, only after completed
  evidence.

## Preserved status

- **CONFIRMED CURRENT STATE:** Name Rater complete pass is completed, with its
  recorded manual-smoke caveats.
- **CONFIRMED CURRENT STATE — blocked feature:** Hidden Item sparkle needs a
  source-backed Overworld frame hook.
- **LEGACY / OBSOLETE:** Prior roadmap numbering, detailed queues,
  and status remain in
  [00_project-control/roadmap/roadmap-status.md](../00_project-control/roadmap/roadmap-status.md)
  without renumbering.
