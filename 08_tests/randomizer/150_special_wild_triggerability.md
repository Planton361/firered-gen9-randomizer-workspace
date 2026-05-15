# Diagnose 150: Special Wild Triggerability

## Scope

- Branch: `analysis/upr-fvx-cfru-dpe-special-wild-triggerability`
- Goal: document which CFRU/DPE special Wild/Encounter systems exist, whether they are active in the current tracked source state, and how they would be triggered.
- Mode: read-only triggerability analysis only.
- No ROM access, no Randomizer run, no build, no scripts triggered, no save/RAM/emulator state touched and no code changes.
- Standard Wild / Grass-Cave / Surfing / Fishing / Rock Smash is not retested; it remains P0-supported.

## Evidence sources

- Current workspace and roadmap documents.
- `01_docs/compat/cfru-dpe-encounter-systems-model.md`.
- Diagnose 148 Wild Encounters scope plan.
- Diagnose 149 coverage reconciliation.
- Read-only `rg` over documented workspace files and CFRU source paths, excluding private/build/release artifacts.

## System matrix

| System | Exists in source | Current tracked table/state | Normal Wild automatic? | Triggerability | Recommended status | UPR-FVX relevance now | Recommended action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Day/Night Wild | Yes | Time headers exist, but current custom Route 1 block is disabled and Morning/Day/Evening/Night headers are sentinel-only | No, because tracked special headers are empty/sentinel and fallback handles standard wild | Needs `TIME_ENABLED` and non-empty time headers | dormant | Do not randomize now | Document only; later table diagnostic if time headers become non-empty |
| Swarms | Yes | `gSwarmTable` exists and has a tracked example entry; `gSwarmTableLength` is non-zero | Runtime overlay for land encounters, not a standard table write path | Needs swarm runtime selection via Var/time/order logic | runtime-only / manual-state | Do not randomize with Standard Wild | Later read-only table diagnostic, then separate parser/write plan only if product wants Swarms |
| Roamers | Yes | Roamer code/state exists; species live in save/RAM state after script initialization | Can intercept land/water encounters before normal Wild | Needs `sp129_InitRoamer` or equivalent script/save state | runtime-only | Do not randomize as Wild Encounters | Future RAM/script-aware scope; not current Randomizer writer |
| DexNav | Yes | DexNav code/UI exists and reads local Wild/Swarm data | Not automatic standard Wild; player/UI/state-driven | Needs DexNav UI/start-menu/search state and map/tile conditions | partial / future scope | Indirectly sees base Wild data but has separate UI/state logic | Document only; later BizHawk/in-game trigger test if needed |
| Raids | Yes | Raid tables and `gRaidsByMapSection` exist with many entries; battle scripts/functions exist | No | Needs raid den/map section/flags/scripts such as create/start raid flow | manual/script-triggered / future scope | Separate from Wild Encounter randomization | Later own parser/write plan; not part of Wild Encounter diagnostics |
| Altering Cave | Yes, vanilla special path | Uses standard header selection plus var-driven header index shifting | Partially, through standard wild header lookup plus runtime var | Needs `VAR_ALTERING_CAVE_WILD_SET` | partial / manual-state | Standard data may be visible, semantic var behavior not modeled | Document only; special-case read-only diagnostic if needed |
| Tanoby / Unown | Yes | Unown special letter logic exists; standard slots plus flag/letter gating | Partially, through standard slots plus special runtime logic | Needs Tanoby unlock condition and Unown letter logic | partial / manual-state | Species slots may be randomized, letter/forme gating not modeled | Document only; later special-case in-game test if needed |
| Wild Double Battles | Yes | Flag-gated runtime mode exists | Uses underlying Wild data but changes battle generation | Needs `FLAG_DOUBLE_WILD_BATTLE`, tile or Sweet Scent/runtime conditions | runtime-only | Base slots already covered; double-battle runtime not randomized | Later in-game/BizHawk trigger test only if required |
| `gWildDataSwitch` runtime override | Yes | Runtime pointer override exists | Can override current Wild header if set to a valid runtime pointer | Needs script/runtime pointer state | runtime-only / unsupported | Not a static Randomizer table | Preserve-only; no Randomizer action now |

## Triggerability findings

- Day/Night Wild: source support exists, but the current tracked custom header block is disabled and fallback headers are sentinel-only. It is dormant in the current tracked source state.
- Swarms: source support and a non-empty table exist, but triggering depends on runtime swarm state/order/time logic. It is not a normal static Wild table path for UPR-FVX today.
- Roamers: source support exists, but encounter behavior depends on initialized roamer save/RAM state and can intercept land/water encounters. It is runtime-only and script-triggered.
- DexNav: source/UI support exists and reads standard Wild/Swarm data, but its own scan/search/HUD/state logic means it is not proven by Standard Wild support.
- Raids: source support and large own tables exist. Raids use separate Species/item/ability/drop structures and script/battle flow, so they are future scope, not Wild Encounter scope.
- Altering Cave and Tanoby/Unown: vanilla-special runtime semantics exist. UPR-FVX may see underlying standard slots, but does not model var/flag/letter behavior.
- Wild Double Battles: uses base Wild slots but is triggered by runtime flags/tile/Sweet Scent conditions; no parser/write action is needed now.
- `gWildDataSwitch`: pointer override is purely runtime/script state and unsupported for static Randomizer coverage.

## Active / dormant / runtime-only assessment

- Active enough to require immediate Randomizer support: none.
- Dormant: Day/Night Wild in the current tracked source state.
- Runtime-only: Swarms, Roamers, Wild Double Battles, `gWildDataSwitch`.
- Manual/script-triggered: Roamers, Raids, Altering Cave, Tanoby/Unown, some Wild Double paths.
- Partial/future: DexNav, Altering Cave, Tanoby/Unown.
- Unsupported/future parser/write scope: Raids and any direct Swarm table randomization.

## Randomizer relevance

UPR-FVX does not need to randomize these systems now for the current compatibility target because none is both active and automatically exercised by the normal Standard Wild path in the current tracked source state.

The one exception is indirect visibility: DexNav, Wild Double Battles and some special vanilla cases can consume already-supported standard Wild data. That does not create a new Randomizer writer requirement. It only creates optional future in-game/BizHawk trigger tests if the feature must be supported as gameplay-facing compatibility.

## Risks and blockers

- A future hack branch can enable non-empty Day/Night headers; that would change Day/Night from dormant to active and require a table diagnostic.
- Swarms have a non-empty table but depend on runtime state; randomizing them without trigger semantics would not prove gameplay behavior.
- Roamers and `gWildDataSwitch` depend on save/RAM/script state and should not be treated as ROM table diagnostics.
- Raids are a separate table family with Species, items, abilities, drops and battle flow; they need a standalone parser/write plan if ever required.
- DexNav mixes standard Wild, Swarm, Unown, hidden ability, held item and UI/search state; a Randomizer write smoke would be the wrong first test.
- Special vanilla systems can make Standard Wild logs and in-game behavior diverge if var/flag state is ignored.

## Recommended next step

No parser/write diagnostic is required immediately.

Recommended next action: update coverage state to mark special Wild systems as documented and not currently requiring UPR-FVX randomization. If gameplay support becomes a product requirement, start with a read-only table diagnostic for the smallest active system:

1. Day/Night only if non-empty headers are enabled.
2. Swarms only if runtime trigger expectations are defined.
3. Raids only as an independent parser/write-plan scope.
4. DexNav or Wild Double only as in-game/BizHawk trigger tests after base table support.

## Conclusion

Special Wild systems exist in CFRU/DPE, but the current tracked state does not require a new Randomizer writer before moving on. Standard Wild remains P0-supported, Held Items are closed, and special systems should remain documented/future-scope until an active or realistically triggerable requirement is introduced.
