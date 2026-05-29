# Pokemon data reviewed alias table

Date: 2026-05-29
Branch: `analysis/pokemon-data-reviewed-alias-table`
Scope: read-only Pokemon Showdown-to-CFRU/DPE mapping classification.

## Purpose

This document records the first small, reviewable alias/ignore table for the Pokemon Showdown mapping audit. The machine-readable table is `07_scripts/data_audit/showdown_aliases.json`.

The table is classification-only. It does not authorize CFRU or DPE data-table edits, does not vendor Pokemon Showdown data, and does not include raw audit reports.

## Alias table shape

Each entry uses:

- `kind`: `species`, `moves`, or `abilities`.
- `category`: review category such as `form-name`, `gmax-giga`, `local-shortform`, `split-move`, `hidden-power-variant`, `spelling`, `cap-fan-move`, `fan-future-move`, `lgpe-partner-move`, `missing-engine-move`, `local-helper-constant`, `local-project-move`, `name-mismatch`, or `behavior-risk`.
- `status`: `alias`, `ignore`, `open-risk`, or `behavior-risk`.
- `showdown_key` or `showdown_pattern`: normalized Showdown key or regex pattern to classify.
- `local_keys`: normalized local CFRU/DPE keys when the entry maps to local constants.
- `local_constants`: human-readable constants for review.
- `note`: reviewer-facing rationale.

Ability `behavior-risk` entries may also record `local_alias_target` to show that a local Gen9-looking ability name still aliases to an older effect.

## Initial reviewed coverage

The first table contains 28 entries:

- Species aliases: 12 entries.
- Move aliases or ignores: 9 entries.
- Ability aliases or behavior risks: 7 entries.

Species coverage starts with:

- Ogerpon Terastal form-name aliases between Showdown names, CFRU color shorthand, and DPE `*_TERASTAL` names.
- Four GMax/Giga examples where Showdown uses `gmax` and local constants use `GIGA`.
- Four regional/local-shortform examples: Hisui `H`, Galar `G`, and Indeedee female naming.

Move coverage starts with:

- Z-Move physical/special local splits for `Breakneck Blitz`, `All-Out Pummeling`, and `Black Hole Eclipse`.
- Max/GMax physical/special local splits for `Max Strike`, `Max Airstream`, `G-Max Vine Lash`, and `G-Max Wildfire`.
- Hidden Power typed variants as an ignore pattern because Showdown exposes typed keys while local CFRU/DPE does not model each type as a separate move constant.
- `visegrip` to `vicegrip` spelling alias.

Ability coverage starts with:

- `tabletsofruin` to `tabletofruin` as a name mismatch.
- Six explicit `behavior-risk` entries where the local name exists but aliases to an older effect: `Hadron Engine`, `Orichalcum Pulse`, `Poison Puppeteer`, `Good as Gold`, `Toxic Debris`, and `Zero to Hero`.

## Batch 2 reviewed coverage

Batch 2 expands the table to 107 entries while keeping the scope to safe Species name-shape mappings:

- Species `gmax-giga`: expanded from 4 to 32 entries, covering the remaining Showdown `gmax` keys with local `GIGA` constants.
- Species `local-shortform`: expanded from 4 to 55 entries, covering reviewed Alola `A`, Galar `G`, Hisui `H`, Paldea `P`, and the existing gender-form short alias.
- Existing Move and Ability entries were not broadened in this batch; remaining split moves and behavior-risk abilities stay visible as follow-up work.

No broad regex rule was added for regional forms or GMax/Giga names. Each mapping remains an explicit reviewed entry with local constants.

## Move split batch reviewed coverage

The move-split batch expands the table to 169 entries while keeping the scope to safe Move physical/special split aliases:

- Move `split-move`: expanded from 7 to 69 entries.
- Added explicit reviewed Z-Move physical/special aliases for the remaining local `P`/`S` split constants.
- Added explicit reviewed Max Move physical/special aliases for the remaining local `P`/`S` split constants.
- Added explicit reviewed G-Max Move physical/special aliases for the remaining local `P`/`S` split constants.
- Existing Species and Ability entries were not broadened in this batch.

No broad regex rule was added for Z/Max/GMax names. Each split remains an explicit reviewed entry with local constants, so real Move behavior gaps stay visible.

## Move final reviewed coverage

The move-final batch expands the table to 191 entries while keeping the scope to remaining Move-only classifications:

- Added 13 `open-risk/lgpe-partner-move` entries for Let's Go partner moves that are present in Showdown but have no reviewed local CFRU/DPE engine-backed move.
- Added 1 `open-risk/missing-engine-move` entry for `allyswitch`, which has no reviewed local CFRU/DPE move.
- Added 3 `ignore/cap-fan-move` entries for Showdown CAP moves.
- Added 1 `ignore/fan-future-move` entry for Showdown nonstandard Future move data.
- Added 2 `ignore/local-helper-constant` entries for `MOVE_NAME_LENGTH` and `MOVE_NONE`.
- Added 2 `ignore/local-project-move` entries for local CFRU/DPE project moves `MOVE_LEECHFANG` and `MOVE_STEELYHIT`.
- Existing Species and Ability entries were not broadened in this batch.

`open-risk` entries are deliberately not solved mappings. They exist so the audit report can distinguish known missing Move behavior from accidentally uncategorized keys.

## Script integration

`07_scripts/data_audit/showdown_mapping_audit.py` now loads the reviewed alias file by default and prints:

- alias table entry count,
- category counts,
- samples,
- reviewed classifications for Showdown keys without local constants,
- reviewed classifications for local constants without Showdown keys,
- still-uncategorized keys.

Without an external Pokemon Showdown data directory, the script remains local-only and reports CFRU/DPE constant drift plus the alias table summary.

With an external Pokemon Showdown data directory, the script classifies unresolved keys without copying Showdown data into this repository.

## Full-audit summary

Against the external Pokemon Showdown data directory used locally, the move-final batch classified these unresolved buckets:

- Species Showdown-without-local: 91 classified, 228 still uncategorized.
- Species local-without-Showdown: 95 classified, 126 still uncategorized.
- Moves Showdown-without-local: 104 classified, 0 still uncategorized.
- Moves local-without-Showdown: 143 classified, 0 still uncategorized.
- Abilities Showdown-without-local: 1 classified, 35 still uncategorized.
- Abilities local-without-Showdown: 1 classified, 7 still uncategorized.

Ability behavior-risk entries are intentionally counted in the alias table summary even when they are not unresolved by name. A normalized-name match is not proof that local CFRU/DPE implements Gen9 behavior.

The remaining Move gaps are now classified rather than uncategorized: `allyswitch` and the Let's Go partner moves are `open-risk`, while CAP/Future non-target moves and local helper/project constants are explicit `ignore` entries.

## Policy

Use this table to separate reviewed name-shape differences from real unresolved mapping work.

Rules:

- Treat `alias` entries as reviewed name mappings only.
- Treat `ignore` entries as deliberate non-actionable Showdown-only keys.
- Treat `open-risk` entries as known unresolved mapping/behavior gaps, not solved aliases.
- Treat `behavior-risk` entries as unresolved behavior work, not solved mappings.
- Fail closed for generated data work: do not silently apply uncategorized Species, Move, or Ability mappings.
- Keep Ability aliases in their own risk class until CFRU ability behavior is source-audited.
- Keep Pokemon Showdown data external; do not commit vendored Showdown files or raw comparison reports.

## Handoff

Next useful step: expand `showdown_aliases.json` in small review batches for high-risk Ability behavior aliases and remaining Species form/name policy. Keep Move `open-risk` entries blocked until source-backed CFRU/DPE behavior or an explicit non-support policy exists.

Do not edit CFRU/DPE Pokemon data tables until unresolved mappings are either classified or intentionally blocked.
