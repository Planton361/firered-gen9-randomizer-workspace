# M-000R adoption report

## Previous workflow

**LEGACY / OBSOLETE AS NORMATIVE POLICY:** `01_docs/`, `08_tests/`, and
`00_project-control/` accumulated useful project history, handoffs, templates,
and evidence, but no single short canonical baseline. Their content remains
supporting evidence.

## Current technical state

**CONFIRMED CURRENT STATE:** This is a GitHub-backed workspace with pinned
submodules for DPE, CFRU, UPR-FVX, Tracker, and references. Linux/CachyOS and
POSIX commands are the canonical development baseline. mGBA is the current
targeted smoke emulator; BizHawk and Tracker work are later targets.

## Existing agent/AI setup

**CONFIRMED CURRENT STATE:** Existing guidance establishes branches, protected
artifacts, GitHub PRs, Linux, and optional MCP. It also embeds PowerShell and
per-session-state assumptions in historical material.

## Conflicts found

| Finding | Classification | Resolution |
|---|---|---|
| PowerShell safety check versus Linux/POSIX default | **CONFLICT** | Add standard-library Python check; retain PowerShell as compatibility guidance |
| Historical session/next-step files presented as current | **CONFLICT** | Add canonical-pointer notices; preserve content |
| Current physical CFRU checkout differs from `origin/main` Gitlink | **SUSPENDED** | Do not alter/stage Gitlink; record in-flight PR work |
| Historical product statuses may disagree | **CONFLICT** | Do not silently resolve; canonical roadmap preserves stated suspension/blockers |

## Decisions preserved

**CONFIRMED CURRENT STATE:** GitHub truth, protected `main`, bounded branches
and PRs, private artifact exclusion, submodule pins, revision-specific
evidence, one writer per branch, and optional read-only MCP are preserved.

## Decisions replaced

**LEGACY / OBSOLETE AS DEFAULT:** PowerShell is no longer the default workflow;
mandatory `SESSION_STATE`/`NEXT_STEPS` writes after every small session are
removed; long duplicated workflow instructions are replaced by canonical docs.

## Deferred improvements

| Category | Items |
|---|---|
| Blocking | M-001 TM/HM rollout acceptance; source-backed Hidden Item Overworld frame hook |
| Opportunistic | Consolidate historical evidence when separately authorized; version inventory from evidenced hosts |
| Cosmetic | Rewrite/translate legacy documentation or dashboard presentation |

## New source of truth

**CONFIRMED CURRENT STATE AFTER MERGE:** `AGENTS.md` and `docs/` are the
repository-backed workflow baseline. GitHub remains persistent truth.

## Workflow baseline

**INTENDED FUTURE STATE:** Effective only after merge to `main`.

Final merge SHA: `TBD after merge`
