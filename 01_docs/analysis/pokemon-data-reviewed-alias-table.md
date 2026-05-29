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
- `category`: review category such as `form-name`, `gmax-giga`, `local-shortform`, `split-move`, `hidden-power-variant`, `spelling`, `cap-fan-move`, `fan-future-move`, `lgpe-partner-move`, `missing-engine-move`, `local-helper-constant`, `local-project-move`, `name-mismatch`, `alias-plus-hook`, `behavior-risk`, `missing-local`, `intentionally-merged`, or `local-only`.
- `status`: `alias`, `ignore`, `open-risk`, or `behavior-risk`.
- `showdown_key` or `showdown_pattern`: normalized Showdown key or regex pattern to classify.
- `local_keys`: normalized local CFRU/DPE keys when the entry maps to local constants.
- `local_constants`: human-readable constants for review.
- `note`: reviewer-facing rationale.

Ability `behavior-risk` entries may also record `local_alias_target` to show that a local Gen9-looking ability name still aliases to an older effect.
Ability entries may also record `generator_policy`; unless the status and policy explicitly mark a non-blocking name merge or local-only ignore, Ability entries are behavior-gating classifications and do not authorize automated data generation.

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

## Ability risk-table reviewed coverage

The Ability risk-table batch expands the table to 215 entries while keeping the scope to Ability-only classification:

- Ability `alias-plus-hook`: 12 `behavior-risk` entries where local CFRU/DPE aliases point at older Ability IDs but the source-backed audit found species-gated or extra CFRU behavior hooks.
- Ability `behavior-risk`: 4 entries for Good as Gold, Zero to Hero, Tera Shift, and Tera Shell where source evidence remains incomplete, inconsistent, or not generator-safe.
- Ability `name-mismatch`: 1 blocking behavior-risk entry for `tabletsofruin` / `tabletofruin`.
- Ability `missing-local`: 7 `open-risk` entries for Commander, Hospitality, Embody Aspect variants, and Teraform Zero.
- Ability `intentionally-merged`: 2 non-blocking legacy merge entries for Teravolt and Turboblaze into local Mold Breaker-style behavior.
- Ability `local-only`: 5 ignore entries for local sentinel/project/placeholder constants.

The source-backed focus entries include `HADRONENGINE`, `ORICHALCUMPULSE`, `TOXICDEBRIS`, `POISONPUPPETEER`, `SHARPNESS`, `ROCKYPAYLOAD`, `SEEDSOWER`, `WINDPOWER`, `WINDRIDER`, the Ruin abilities, `GOODASGOLD`, `ZEROTOHERO`, Terapagos Tera abilities, `COMMANDER`, `HOSPITALITY`, and `EMBODYASPECT*`.

All Ability behavior-risk/open-risk entries include blocking generator policy. The table classifies the risk; it does not promote any Gen9 Ability behavior to generator-safe support.

## Ability final batch reviewed coverage

The Ability final batch expands the table to 239 entries and classifies the remaining Ability-only unresolved buckets:

- Ability `intentionally-merged`: expanded to 13 non-blocking legacy merge entries. Added reviewed CFRU/DPE source-comment-backed merges for Air Lock / Cloud Nine, Iron Barbs / Rough Skin, Power of Alchemy / Receiver, Propeller Tail / Stalwart, Pure Power / Huge Power, Queenly Majesty / Dazzling, Solid Rock / Filter, Tangling Hair / Gooey, Vital Spirit / Insomnia, White Smoke / Clear Body, and Wimp Out / Emergency Exit.
- Ability `alias-plus-hook`: expanded to 13 `behavior-risk` entries by adding Full Metal Body as a Clear Body-backed local assignment with CFRU species-gated display/helper paths.
- Ability `behavior-risk`: expanded to 5 entries by adding Libero / Protean as a blocked behavior-risk merge because current local behavior was not proven equivalent to current Showdown/Gen9 behavior.
- Ability `name-mismatch`: expanded to 3 blocking behavior-risk entries by adding Showdown `asoneglastrier` / `asonespectrier` mapped to local `asonechilling` / `asonegrim`.
- Ability `missing-local`: expanded to 8 `open-risk` entries by adding pure Chilling Neigh, because CFRU has conditional hooks but no reviewed local `ABILITY_CHILLINGNEIGH` constant.
- Ability `missing-local`: added 7 explicit `ignore` entries for Showdown `isNonstandard` Future/CAP Ability keys: Dragonize, Mega Sol, Mountaineer, Persistent, Piercing Drill, Rebound, and Spicy Spray.
- Ability `name-mismatch`: added 1 sentinel-only ignore for Showdown `noability` / local `ABILITY_NONE`.

After this batch, the external audit has no still-uncategorized Ability keys in either Showdown-without-local or local-without-Showdown buckets. Blocking Ability classifications still remain blocking; the batch classifies names and risk, not battle correctness.

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

Against the same external Pokemon Showdown data directory, the Ability risk-table batch classified these Ability unresolved buckets:

- Abilities Showdown-without-local: 12 classified, 24 still uncategorized.
- Abilities local-without-Showdown: 6 classified, 2 still uncategorized.

Most `alias-plus-hook` entries have matching local normalized keys, so they are represented in the alias table category summary rather than only in unresolved-key buckets.

Against the same external Pokemon Showdown data directory, the Ability final batch classified the remaining Ability unresolved buckets:

- Abilities Showdown-without-local: 36 classified, 0 still uncategorized.
- Abilities local-without-Showdown: 8 classified, 0 still uncategorized.

The remaining blocking Ability keys are the `behavior-risk` and `open-risk` classifications, including `asoneglastrier`, `asonespectrier`, `chillingneigh`, `commander`, `embodyaspect*`, `fullmetalbody`, `hospitality`, `libero`, `tabletsofruin`, `teraformzero`, `terashell`, and `terashift`.

## Policy

Use this table to separate reviewed name-shape differences from real unresolved mapping work.

Rules:

- Treat `alias` entries as reviewed name mappings only.
- Treat `ignore` entries as deliberate non-actionable Showdown-only keys.
- Treat `open-risk` entries as known unresolved mapping/behavior gaps, not solved aliases.
- Treat `behavior-risk` entries as unresolved behavior work, not solved mappings.
- Treat Ability `alias-plus-hook` entries as source-backed risk classifications, not automatic support clearance.
- Treat Ability `generator_policy = blocked` as not generator-safe unless a later source-backed task explicitly changes that policy.
- Fail closed for generated data work: do not silently apply uncategorized Species, Move, or Ability mappings.
- Keep Ability aliases in their own risk class until CFRU ability behavior is source-audited and, where needed, battle-smoked.
- Keep Pokemon Showdown data external; do not commit vendored Showdown files or raw comparison reports.

## Handoff

Next useful step: continue remaining Species form/name policy. Keep Move and Ability `open-risk` / `behavior-risk` entries blocked until source-backed CFRU/DPE behavior or an explicit non-support policy exists.

Do not edit CFRU/DPE Pokemon data tables until unresolved mappings are either classified or intentionally blocked.
