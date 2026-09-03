# Engineering rules

## Git and work packages

- **CONFIRMED CURRENT STATE:** `main` remains stable/protected. Use a bounded
  work branch and PR for each change; never merge from Codex.
- One milestone block per Codex session is the default. Keep one writing agent
  per branch. An independent reviewer is for substantial risk, not ritual.
- Start by confirming branch, `git status --short`, submodule status, scope,
  and protected paths. Stop on unexpected changes.
- Prefer existing patterns and the minimal necessary diff. No broad refactors,
  dependency migrations, architecture modernization, or unrelated cleanup.

## Safety boundaries

Do not read, modify, stage, or commit `04_private_roms/`, `05_builds/`,
`03_tools/releases/`, ROMs, saves, emulator states, generated builds, tool
binaries, `.env`, tokens, keys, or secrets. Do not alter a submodule Gitlink
unless explicitly authorized. MCP is optional and read-only when concretely
useful.

## Verification and completion

Verification is proportional to change risk. Documentation or Python helper
changes need focused checks; product work needs its separately authorized
evidence plan. A successful check does not promote support beyond its evidence
level.

Definition of Done:

1. Scope, evidence classification, and allowed files were observed.
2. The diff is minimal and does not cross protected or product boundaries.
3. Relevant checks, `git diff --check`, status, stat, and submodule/Gitlink
   review are recorded.
4. Status/decision documents are updated only when the durable state or a
   decision actually changes; no mandatory `SESSION_STATE` or `NEXT_STEPS`
   edit follows every tiny session.
5. A PR uses a body file, identifies milestone/task contract, scope,
   verification, risks/deviations, artifact safety, and next handoff.

## Stop conditions

Stop for `main`, an unexpected worktree change, protected data, unapproved
external coordination, an unapproved product conflict, missing evidence, or a
scope expansion. Technical conflicts may be resolved only when the repository
and current environment unambiguously establish the answer; document that
resolution. Product conflicts remain **CONFLICT** until directed.
