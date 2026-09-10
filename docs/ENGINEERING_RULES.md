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

## Engine, data and QoL boundary

**CONFIRMED USER DECISION:** Apply the [pilot contract](PROJECT.md#pilot-product-contract)
to each work package before assigning component ownership.

- Data: Base Stats, Level-up Learnsets and Ability assignments/names may be
  modernized only where existing CFRU/DPE semantics represent them safely.
  DPE owns expanded data; CFRU owns its runtime integration and any corresponding
  engine-side tables. Data or names alone do not prove battle behavior.
- Engine: missing/partial upstream mechanics are documented baseline limitations,
  not implementation requirements. Commander, Hospitality, Embody Aspect,
  Scarlet/Violet mechanics expansion, new Terastal/form-transition systems
  solely for Gen-9 parity, and broad battle-engine refactors are outside the
  pilot. Reopening these requires an explicit separate post-pilot project.
- Randomizer: UPR-FVX owns selection and output writing, including necessary
  preservation, guards or exclusions for unsafe cases. Compatibility work must
  not silently turn into a ROM engine expansion.
- QoL: explicitly desired source-backed behavior may change ROM source in a
  separately bounded implementation milestone. CFRU owns runtime/script/flow
  behavior; UPR-FVX owns randomized-output behavior; DPE is involved only when
  Pokémon data is affected. The reference goal serves Ironmon and casual play.

Use the [source index](../01_docs/references/source-index.md) with its established
reference roles: selected CFRU/DPE and UPR-FVX sources establish actual target
behavior; CFRU/DPE upstream supplies architecture context; CyanSMP64 FireRed
NatDex and its associated NatDex/randomizer references supply parity comparisons;
pret FireRed supplies the vanilla structure/symbol baseline. Use FVX upstream
and Ajarmar ZX for randomizer lineage comparisons as relevant. Reference models
are not drop-in replacements for the selected CFRU/DPE model. Preserve this
source-first approach and do not port opaque binary patches.

M-010 findings are supporting compatibility evidence. The M-011 experimental
candidates in [M-010](milestones/M-010.md#m-011--superseded-hospitality-train)
must not be integrated or pinned. [M-012](milestones/M-012.md) closes as an
analysis-only audit; its closure authorizes no implementation or component pin
change. Future implementation candidates require a separate bounded work package.

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
