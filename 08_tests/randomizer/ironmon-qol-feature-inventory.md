# Ironmon QoL Feature Inventory Smoke

Status: documentation-only inventory smoke for branch `analysis/ironmon-qol-feature-inventory`.

No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash value, private path, token, secret, `.env`, CFRU source change, DPE source change, UPR-FVX source change, or upstream PR/push is included.

## Scope

This smoke records that the Ironmon/NatDex/FireRed QoL inventory was created from public/local source references and existing sanitized workspace evidence.

Inventory file:

- `01_docs/analysis/ironmon-qol-feature-inventory.md`

Covered target areas:

- Faster Intro / Controls Guide / Oak Tutorial / New Game Flow.
- Hidden Items / Itemfinder / Sparkle / Field Effects.
- Field Item Balls / Pokeball object graphics / TM-HM item balls.
- Runtime Options / Config Flags.
- Randomizer interaction with Field Items.

## Read-only evidence summary

| Area | Evidence result | Caveat |
|---|---|---|
| Branch and worktree preflight | Work proceeded on `analysis/ironmon-qol-feature-inventory` after the clean `main` handoff. | No implementation was performed. |
| CFRU baseline QoL | Source and existing smoke docs show skip controls guide, Oak tutorial disabled, old/flat EXP, poison faint, catch malus off, Nuzlocke toggle and Wild Prebattle toggle as existing baseline candidates. | Some gameplay rows remain targeted-smoke or inconclusive until separately exercised. |
| Hidden item / Itemfinder source | FireRed source shows hidden-item BG-event handling, Itemfinder range/underfoot logic, and hidden-item pickup script flow; CFRU has field-effect and item-sprite presentation hooks. | No hidden-item QoL implementation was added. |
| Field item balls / graphics | FireRed source shows generic `OBJ_EVENT_GFX_ITEM_BALL`; UPR-FVX Gen3 has an `ItemBallPic` scanner value. | No per-item or TM/HM object-graphics source implementation was identified. |
| UPR-FVX Field Items | Existing sanitized smokes show Field Items Shuffle, Random, Random Even and Ban Bad stable in the narrow field-items-only scope. | Shops, Pickup, static/gift/NPC item sources and broader item policies remain separate scopes. |
| Ironmon / Tracker context | Public Ironmon and Tracker docs support Smart AI / QoL patch context and New Runs workflow. | Binary patches were not downloaded, copied, used, or ported. |

## Feature-status impact

- New analysis handoff: `01_docs/analysis/ironmon-qol-feature-inventory.md`.
- No support level is promoted beyond existing targeted smoke evidence.
- No CFRU/DPE/UPR-FVX implementation is claimed.
- Recommended first real implementation block is smoke-hardening the existing CFRU QoL baseline, not adding new logic.

## Recommended first smoke block

Suggested future branch:

`feature/cfru-qol-baseline-smoke-hardening`

Targeted checks:

- Fresh new-game flow reaches player control.
- Intro controls guide is skipped.
- Oak tutorial battle is absent and no script state breaks.
- Old/flat EXP behavior is observed in one controlled battle.
- Poison can faint in overworld in one controlled state.
- SwSh catch-level malus is not active in one controlled catch comparison if practical.
- Nuzlocke and Wild Prebattle menu rows only affect their owning flags.

Keep this future smoke sanitized: no ROM names, paths, hashes, screenshots, raw logs, saves, states, build outputs, tool binaries or private local details.

## Checks for this documentation block

Planned checks:

- `git status --short`
- `git diff --stat`
- `git diff --check`

No script was added, so no `python3 -m py_compile` check is required.
