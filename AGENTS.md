# Agent entry point

Use this short entry point for repository work. The canonical workflow is in:

- [docs/PROJECT.md](docs/PROJECT.md)
- [docs/ENGINEERING_RULES.md](docs/ENGINEERING_RULES.md)
- [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md)
- [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/MODEL_POLICY.md](docs/MODEL_POLICY.md)
- [docs/milestones/M-000R.md](docs/milestones/M-000R.md)

`01_docs/` and `08_tests/` are historical/supporting evidence, not the
normative workflow baseline. Read relevant evidence when a task requires it.

## Operating boundaries

- **CONFIRMED CURRENT STATE:** GitHub and this repository are the persistent
  source of truth; Linux/POSIX is the default environment; `main` is stable
  and protected.
- Read-only inspection is allowed on `main`. Any repository write requires a
  bounded, approved non-`main` branch. Never commit, push, or merge on
  `main`; never merge a PR.
- The operating model is GitHub Project -> Workspace Issue -> bounded
  Component/Integration task -> branch -> PR/evidence -> review -> user
  merge/acceptance. PRs are evidence/revisions, not a second queue.
- A new Issue, materially new scope, or new branch starts a fresh Codex session.
  Repair of the same contract on the same branch may resume.
- Default to one writing agent per branch. Do not create artificial parallel
  agent teams.
- `docs/ROADMAP.md` owns the stable finish line and dependencies, not daily
  status. `01_docs/SESSION_STATE.md`, `01_docs/NEXT_STEPS.md`, historical
  handoffs, `00_project-control/`, and similar legacy status material are
  non-operative supporting evidence.
- Historical pointer/repoint/offset/ROM-layout/ABI/compatibility evidence remains
  available on demand and must not be discarded merely because it is historical.
- Do not read, modify, stage, or commit ROMs, saves, emulator states, builds,
  tool binaries, `.env` files, tokens, keys, secrets, or the protected paths
  named in [docs/ENGINEERING_RULES.md](docs/ENGINEERING_RULES.md).
- Do not change a submodule Gitlink unless the task explicitly authorizes it.
- `UPSTREAM_CONTRIBUTION` remains deferred unless a later explicit project
  opens that phase.

## Stop rules

For writing work, stop and report when the branch is `main`. Read-only
inspection on `main` is permitted. Also stop for an unexpected worktree
change, protected boundary, product-scope expansion, or insufficient evidence.
Do not silently resolve product conflicts.

Before a change, read the canonical files relevant to its scope, run
`python3 07_scripts/bootstrap/check_git_safety.py`, and inspect `git status
--short`. Use `rg`/`rg --files` for repository search. Keep the diff minimal
and verify it in proportion to risk.
