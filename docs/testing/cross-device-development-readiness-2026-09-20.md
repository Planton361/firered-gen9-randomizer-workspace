# Cross-device Development Readiness — Source Checkpoint Evidence

## Contract identity

- Issue: #497 — Cross-device Development Readiness
- Repository: `Planton361/firered-gen9-randomizer-workspace`
- Branch: `verification/497-cross-device-readiness`
- Evidence classification: **INTENDED FUTURE STATE — active verification contract**
- Source platform: Linux/POSIX (non-identifying)
- State: `SOURCE_CHECKPOINT_READY / RECEIVER_PENDING`

`HANDOFF_READY` is not accepted by this source-side checkpoint. Receiver-side
reconstruction and verification are still pending. `TASK_TOOLCHAIN_READY` is a
separate concept: receiving-host ROM, build, runtime, or other task-toolchain
capability is not required for this checkpoint and is not asserted here.

## Workspace and Issue identity

The live repository identity was verified as
`Planton361/firered-gen9-randomizer-workspace`, and the live Issue identity was
verified as #497, `Cross-device Development Readiness`.

The routing-time approved `origin/main` revision was
`ee7e2bc30170dd297540bbe0ed5e0792f490e0fb`. `origin/main` matched that exact
revision before branch creation, and this branch was created directly from
that verified revision.

The final checkpoint commit SHA is intentionally not recorded in the commit
that creates this document. It is recorded in the sanitized Issue #497
comment after the clean push.

## Recursive Gitlink inventory

The following inventory was read from the Workspace Git tree with
`git ls-tree -r --full-tree HEAD` and cross-checked with
`git submodule status --recursive`:

| Gitlink path | Gitlink SHA |
|---|---|
| `02_external/CFRU-expansion` | `8bc8c38210ddba0b05c933dbda06cb4539254c7a` |
| `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| `02_external/Ironmon-Tracker` | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| `02_external/NatDexExtension` | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| `02_external/references/cyansmp64-pokefirered-natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| `02_external/references/cyansmp64-upr-zx-natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` |
| `02_external/references/pret-pokefirered` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |
| `02_external/references/upr-fvx-upstream` | `e0788edc6529c2605f201996e4807ff30165354c` |
| `02_external/references/upr-zx-ajarmar` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` |
| `02_external/upr-fvx` | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` |

No Workspace Gitlink was changed. The required submodule sync/init was used
only to make the tracked public checkouts available for this verification.

## Physical checkout alignment

Each physical checkout HEAD was compared with the corresponding Workspace
Gitlink using `git -C <component> rev-parse HEAD`:

| Component | Workspace Gitlink | Physical checkout HEAD | Result |
|---|---|---|---|
| CFRU | `8bc8c38210ddba0b05c933dbda06cb4539254c7a` | `8bc8c38210ddba0b05c933dbda06cb4539254c7a` | **ALIGNED** |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | **ALIGNED** |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` | **ALIGNED** |

The component comparison passed for CFRU, DPE, and UPR-FVX. No component
source, branch, or Gitlink was modified.

## Project metadata for #497

The exact Project inspected was `FireRed Gen 9 Randomizer — Pilot Finish`.
The live fields for #497 were verified as follows:

| Field | Before | After |
|---|---|---|
| Issue | #497 | #497 |
| Priority | `P0` | `P0` |
| Work Type | `Verification` | `Verification` |
| Status | `Backlog` | `Doing` |

The live Status options were discovered from the Project as `Done`, `Backlog`,
`Ready`, `Doing`, `Review`, and `Blocked`. The Project has no option literally
named `In Progress`; `Doing` is the available active execution option, and
only #497 was moved to it. #498, #499, #500, and #501 were inspected and left
unchanged.

## One-writer evidence

This branch had one designated writing agent. No parallel writing agent was
launched for it. No private filesystem or worktree paths were inspected or
published to establish this statement.

## Source-side checks

- The verified starting branch was clean (`git status --short` produced no
  entries) before the evidence document was created.
- `python3 07_scripts/bootstrap/check_git_safety.py --allow-main` passed for
  the read-only baseline inspection.
- After branch creation,
  `python3 07_scripts/bootstrap/check_git_safety.py` passed.
- The recursive Gitlink inventory and `git submodule status --recursive`
  matched; the three required physical checkout comparisons passed.
- `git diff --submodule=short` showed no Gitlink changes.
- Before commit, `git diff --check`, `git diff --stat`, and full `git diff`
  review passed with this document as the only repository change.
- After commit and push, `git status --short` is rechecked clean; the pushed
  checkpoint SHA and durable clean-push result are recorded in the Issue #497
  comment.

## GitHub-only receiving procedure

On the receiving macOS host, start from GitHub state in a fresh checkout. Do
not use copied IDE state, a copied local checkout, or a previous Codex
conversation as an authority.

1. Obtain the repository from GitHub and run `git fetch origin`.
2. Switch to or track
   `origin/verification/497-cross-device-readiness`.
3. If the local branch already exists, integrate remote movement only with
   fast-forward semantics, such as
   `git merge --ff-only origin/verification/497-cross-device-readiness`.
4. Run `git submodule sync --recursive` and
   `git submodule update --init --recursive` as required.
5. Verify the exact Workspace revision with `git rev-parse HEAD`, inspect the
   recursive Gitlinks with Git, and compare physical CFRU, DPE, and UPR-FVX
   checkout HEADs with their Workspace Gitlinks.
6. Run `python3 07_scripts/bootstrap/check_git_safety.py` and confirm a clean
   `git status --short`.
7. Reconstruct Issue #497 from the live GitHub Issue plus the canonical
   repository files, including `AGENTS.md`, `docs/PROJECT.md`,
   `docs/ENGINEERING_RULES.md`, `docs/ENVIRONMENT.md`,
   `docs/REPRODUCIBILITY.md`, `docs/ROADMAP.md`, and `docs/MODEL_POLICY.md`.

The receiving-side result is deliberately not executed or simulated in this
source-side contract. No prior Codex session or IDE-local state is required.

## Scope boundary

This checkpoint changes only this sanitized evidence document. It does not
touch product implementation, component source, protected artifacts, ROMs,
saves, emulator states, builds, tool binaries, `.env` files, tokens, keys,
secrets, private paths, or any of Issues #498–#501. No merge, force-push,
history rewrite, or upstream-contribution preparation was performed;
`UPSTREAM_CONTRIBUTION = DEFERRED`.
