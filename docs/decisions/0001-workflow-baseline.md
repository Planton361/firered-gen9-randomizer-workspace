# 0001 — Workflow baseline

**Status:** Accepted for M-000R; effective after merge to `main`.

## Decision

The canonical workflow is repository documentation in `AGENTS.md` and `docs/`.
GitHub/repository is persistent truth. Linux/CachyOS and POSIX commands are the
default. The adoption profile is STANDARD: one executor by default, optional
read-only MCP, and no introduced skill library.

`main` is stable/protected; changes use bounded branches and PRs. Codex may
commit, push, and create Draft PRs on an approved branch but never merge.
Protected local artifacts remain outside Git and agent context. Legacy docs
remain supporting evidence, not canonical policy.

## Consequences

M-000R introduces no product changes, broad refactors, dependency migrations,
or submodule Gitlink changes. The baseline takes effect only after merge; until
then this decision is **INTENDED FUTURE STATE**.
