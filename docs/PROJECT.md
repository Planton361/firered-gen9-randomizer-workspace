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

## Pilot product contract

**CONFIRMED USER DECISION — repository sync pending merge of this scope
realignment:** The pilot targets FireRed using the existing CFRU/DPE engine
architecture, with Gen 1–9 Pokémon usable by UPR-FVX and modernized Gen-9 data
where the selected engine can represent it safely. This is the product target,
not a claim of complete compatibility or new battle-mechanic support.

Data modernization covers Base Stats, Level-up Learnsets, and Ability
assignments/names within existing CFRU/DPE engine semantics. A modern ability
name or assignment does not establish its upstream runtime behavior.

Pilot non-goals are missing Gen-9 battle-mechanic implementation, extending
CFRU into a Scarlet/Violet mechanics engine, Commander, Hospitality or Embody
Aspect engine implementation, new Terastal/form-transition systems solely for
Gen-9 parity, and broad battle-engine refactors.

When the selected CFRU/DPE baseline lacks an upstream/current-generation
mechanic, record the limitation. UPR-FVX may preserve, guard or exclude unsafe
cases when necessary; the ROM engine is not expanded solely to implement that
mechanic. The [M-010 decision record](milestones/M-010.md) retains the sanitized
compatibility findings and supersedes the M-011 Hospitality implementation
train. Engine expansion would require an explicit, separate post-pilot request.

## QoL contract

**CONFIRMED USER DECISION:** ROM source changes remain allowed for explicitly
desired, source-backed QoL behavior. The primary reference goal is appropriate
Ironmon NatDex-style quality-of-life and flow improvements for both Ironmon
players and normal/casual play.

Use the [repository source index](../01_docs/references/source-index.md) and
established reference roles/order described in
[Engineering rules](ENGINEERING_RULES.md#engine-data-and-qol-boundary).
Do not port opaque binary patches. [M-012](milestones/M-012.md) is COMPLETE
as an analysis-only parity audit of 36 entries; its findings become
**CONFIRMED CURRENT STATE** once this documentation closure is merged.
M-001 through M-009 remain complete and are not reopened.

**INTENDED FUTURE STATE:** M-013 — NatDex Premier Ball purchase bonus is the
remaining source-backed implementation candidate. Paid Move Reminder on
Cinnabar remains optional backlog, not required for pilot feature-complete
status unless explicitly promoted later. This closure starts no implementation,
introduces no missing Gen-9 battle-mechanic work, and changes no CFRU/DPE/UPR-FVX
source or component pins.

## Component ownership

| Component | Ownership boundary | State |
|---|---|---|
| Workspace | Workflow, manifests, decisions, evidence | **CONFIRMED CURRENT STATE** |
| DPE Gen 9 | Expanded Pokémon data and safe representation within the selected engine | **CONFIRMED CURRENT STATE** |
| CFRU Expansion | Existing runtime semantics, engine integration, and explicitly desired source-backed QoL | **CONFIRMED CURRENT STATE** |
| UPR-FVX | Randomizer settings, selection, output writing, and necessary preserve/guard/exclude policy for unsafe cases | **CONFIRMED CURRENT STATE** |
| mGBA | Current targeted smoke emulator | **CONFIRMED CURRENT STATE** |
| BizHawk / Ironmon Tracker | Later validation and integration targets | **INTENDED FUTURE STATE** |

## Support and completed M-001 rollout

**CONFIRMED CURRENT STATE:** General release/support status is not claimed;
evidence is scoped and revision-specific. The complete Name Rater rollout has
a documented manual pass with caveats.

**CONFIRMED CURRENT STATE:** M-001's accepted 29-slot TM/HM itemball rollout
(28 TMs plus HM07) is integrated. CFRU PR #35 merged at
`8e3fa8378d67dfe4011d6994469c3806f32764c4` from accepted candidate head
`08b869032735118539411adbcffa421c8a697caa`. This revision-specific acceptance
does not establish general release/support status.

**LEGACY / OBSOLETE:** Workspace PR #467 is closed unmerged and retained only
as historical supporting handoff evidence.

**CONFIRMED CURRENT STATE, with targeted runtime caveat:**
[M-009](milestones/M-009.md) integrates Hidden Item Sparkle through a narrowly
source-owned Overworld frame functionrewrite at CFRU
`827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec`. It intentionally supersedes the
old slow-camera byte owner, restores the pret/Cyan Quest Log arrival and OAM
order, and scans normal hidden-item BG events at the frame tail using the
existing transient effect, without persistent custom sprite/palette ownership.

The user observed sparkle behavior and visually judged it appropriate on
candidate `3da0547d782fb62fc993431278d63575912025da`:
`PASS_TARGETED_VISIBLE_SPARKLE_WITH_CAVEATS`. The integrated merge has the
same files but was not separately runtime-tested. Broader global-frame,
menu/lifecycle, Quest Log and resource-pressure regressions remain part of the
later feature-complete playthrough gate. Earlier failed sparkle pilots are
**LEGACY / OBSOLETE**, not evidence against the integrated source-owned
solution. No broad support or release claim follows from this acceptance.

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
Follow the pilot data/engine/QoL boundary in docs/PROJECT.md. Gen-9 data
modernization does not authorize missing battle mechanics.
For a task, state the evidence classification: CONFIRMED USER DECISION,
CONFIRMED CURRENT STATE, INTENDED FUTURE STATE, LEGACY / OBSOLETE, CONFLICT,
or UNKNOWN.
```
