# Agent entry point

Use this short entry point for repository work. The canonical workflow is in:

- [docs/PROJECT.md](docs/PROJECT.md)
- [docs/ENGINEERING_RULES.md](docs/ENGINEERING_RULES.md)
- [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md)
- [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md)
- [docs/ROADMAP.md](docs/ROADMAP.md)
- [docs/milestones/M-000R.md](docs/milestones/M-000R.md)

`01_docs/` and `08_tests/` are historical/supporting evidence, not the
normative workflow baseline. Read relevant evidence when a task requires it.

## Operating boundaries

- **CONFIRMED CURRENT STATE:** GitHub and this repository are the persistent
  source of truth; Linux/POSIX is the default environment; `main` is stable
  and protected.
- Work only on a bounded, approved branch. Never commit, push, or merge on
  `main`; never merge a PR.
- Default to one writing agent per branch. Do not create artificial parallel
  agent teams.
- Do not read, modify, stage, or commit ROMs, saves, emulator states, builds,
  tool binaries, `.env` files, tokens, keys, secrets, or the protected paths
  named in [docs/ENGINEERING_RULES.md](docs/ENGINEERING_RULES.md).
- Do not change a submodule Gitlink unless the task explicitly authorizes it.

## Stop rules

Stop and report when the branch is `main`, an unexpected worktree change is
found, the task crosses a protected boundary, product scope becomes necessary,
or the requested evidence is insufficient to make a safe decision. Do not
silently resolve product conflicts.

Before a change, read the canonical files relevant to its scope, run
`python3 07_scripts/bootstrap/check_git_safety.py`, and inspect `git status
--short`. Use `rg`/`rg --files` for repository search. Keep the diff minimal
and verify it in proportion to risk.
