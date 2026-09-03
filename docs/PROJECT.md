# Project

## Purpose

**CONFIRMED CURRENT STATE:** This repository coordinates a reproducible,
revision-pinned compatibility workspace for a private FireRed Gen 9 setup and
UPR-FVX randomization. It records source ownership, integration decisions, and
sanitized evidence; it does not distribute a playable game or protected game
assets.

## Scope and non-goals

**CONFIRMED CURRENT STATE:** The workspace owns orchestration, repository
documentation, small safety helpers, source references, and cross-component
evidence.

**INTENDED FUTURE STATE:** Work may advance only through bounded milestones and
evidence appropriate to its risk.

**NON-GOALS:** This baseline does not modernize product architecture, migrate
dependencies, introduce CI/containers/skill libraries, or perform broad
refactors. ROMs, saves, emulator states, builds, tool binaries, secrets, and
`.env` remain outside Git and agent context.

## Component ownership

| Component | Ownership boundary | State |
|---|---|---|
| Workspace | Workflow, manifests, decisions, evidence | **CONFIRMED CURRENT STATE** |
| DPE Gen 9 | Expanded Pokémon data and representation | **CONFIRMED CURRENT STATE** |
| CFRU Expansion | Engine behavior and source-backed QoL | **CONFIRMED CURRENT STATE** |
| UPR-FVX | Randomizer settings, selection, and output writing | **CONFIRMED CURRENT STATE** |
| mGBA | Current targeted smoke emulator | **CONFIRMED CURRENT STATE** |
| BizHawk / Ironmon Tracker | Later validation and integration targets | **INTENDED FUTURE STATE** |

## Support and suspended work

**CONFIRMED CURRENT STATE:** General release/support status is not claimed;
evidence is scoped and revision-specific. The complete Name Rater rollout has
a documented manual pass with caveats.

**SUSPENDED:** CFRU PR #35 and Workspace PR #467 are in-flight TM/HM itemball
rollout work. They are neither canceled nor promoted by this milestone. Their
acceptance/integration is the next candidate milestone after M-000R.

**BLOCKED:** Hidden Item sparkle remains blocked until a source-backed
Overworld frame hook is available. No raw-address or opaque binary workaround
is authorized.

## Canonical project instruction for ChatGPT Project settings

After M-000R is merged, paste this into ChatGPT Project settings:

```text
Work from the repository as the source of truth. Start with AGENTS.md, then
docs/PROJECT.md, docs/ENGINEERING_RULES.md, docs/ENVIRONMENT.md,
docs/REPRODUCIBILITY.md, and docs/ROADMAP.md. Treat 01_docs/, 08_tests/, and
00_project-control/ as historical/supporting evidence only. Use Linux/POSIX
commands by default. Keep work to one bounded milestone and approved branch;
never work directly on or merge main. Do not access or request ROMs, saves,
emulator states, builds, tool binaries, .env files, tokens, keys, or secrets.
For a task, state the evidence classification: CONFIRMED CURRENT STATE,
INTENDED FUTURE STATE, LEGACY / OBSOLETE, CONFLICT, or UNKNOWN.
```
