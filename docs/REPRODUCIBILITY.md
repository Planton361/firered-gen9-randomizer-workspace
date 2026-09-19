# Reproducibility

## Revision-specific evidence

**CONFIRMED CURRENT STATE:** Evidence applies only to the documented workspace
commit, submodule Gitlinks, configuration, and declared test scope. A later
upstream revision or local artifact is not covered automatically.

Current baseline Gitlinks are repository evidence, including CFRU
`8bc8c38210ddba0b05c933dbda06cb4539254c7a`, DPE
`22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`, UPR-FVX
`0e3be63e94e34215cc35308d64e8db15e9a3c48c`, Ironmon Tracker
`c450ecaee2d8131a2789bb656e3be792a93712fb`, and NatDexExtension
`a94b8844800308248bb5090b6c36c8b2d7e5d7b9`.

The inspected Workspace baseline before this documentation closure is
`85a963626791ff8ccbfad63bec04b2733558d41e` (Workspace PR #494 merge). CFRU
#45/#48 and UPR-FVX #185 are integrated in the pins above; DPE is unchanged.

**CONFIRMED USER-SUPPLIED REVISION-BOUND RUNTIME PASS:** The targeted
[Runtime Gate 1 report](testing/runtime-gate-1-2026-09-19.md) records the user's
PASS report against Workspace/test basis
`85a963626791ff8ccbfad63bec04b2733558d41e`, CFRU
`8bc8c38210ddba0b05c933dbda06cb4539254c7a`, DPE
`22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`, and UPR-FVX
`0e3be63e94e34215cc35308d64e8db15e9a3c48c`. The run predates this
documentation branch; the documentation commit that introduced this report is
`264d30505db4da820a3f1289470d8dedbf7ce0e5`, not the tested Workspace
revision.

**CONFIRMED CURRENT STATE, with targeted runtime caveat:** At M-009 closure,
the
user-accepted, runtime-tested CFRU candidate is
`3da0547d782fb62fc993431278d63575912025da`. The pinned integrated merge
`827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec` is exactly one commit ahead,
has that candidate as its merge base, and has no additional file changes.
The merge revision was not separately runtime-tested. The supplied acceptance
is `PASS_TARGETED_VISIBLE_SPARKLE_WITH_CAVEATS`; see
[M-009](milestones/M-009.md). Every other component pin is unchanged.

## Evidence levels

1. Source/static analysis
2. Syntax/structural check
3. Build or randomizer load/save/reload evidence
4. Emulator boot and targeted runtime smoke
5. Broad playthrough, target-emulator, and support-profile evidence

**CONFIRMED CURRENT STATE:** Build, randomizer, and runtime evidence are
separate. Do not promote a feature or support claim beyond completed evidence.

## Protected artifacts

ROMs, saves, emulator states, builds, tool releases, private paths, and
secrets are local/private artifacts. They may support a local test but must not
enter Git, prompts, or agent context. Sanitized evidence records the revision,
scope, method, result, caveats, and next required level without exposing them.

**UNKNOWN:** A stable support profile is not established until all required
evidence for its explicitly defined scope is completed.

## Pinned Gen1–9 data reference

**CONFIRMED NEW REFERENCE:** Pokemon Showdown
`b1156ff19204e48089e2384eb2c9c1a8004f57ce` is the explicit reproducible pilot
reference. It is not the historical sync source, whose exact revision remains
**UNKNOWN**. The [coherent-generation closure](audits/coherent-learnsets-2026-09-15.md)
supersedes the earlier per-move-union policy and CFRU #47's 89-table evidence.
It records one selected generation per species/form, reviewed form ownership,
all source/configuration hashes, fresh inventories and exact replay commands.
Zero safe diffs, non-sentinel L1 gaps and unbound pointers do not certify
unsupported battle mechanics or replace the remaining build/runtime/profile
gates. The audit's old-pin statements are historical; current component pins
are recorded above and the integration change is reconciled in the
[draft-PR audit](audits/draft-pr-reconciliation-2026-09-19.md). The
[earlier audit](audits/gen1-9-closure-2026-09-15.md) is historical evidence only.
