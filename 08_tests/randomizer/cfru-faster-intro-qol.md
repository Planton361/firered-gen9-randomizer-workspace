# CFRU Faster Intro QoL handoff

Status: `STOPPED_MINIMAL_PROPOSAL_NO_CODE`.

This records the first Faster-Intro / New-Game / Oak-Lab-Parcel implementation pass for branch `feature/cfru-faster-intro-qol`. The branch stayed within the source-backed stop rules: no CFRU, DPE or UPR-FVX source file was changed because the smallest new Faster-Intro script change was not locally isolatable as one safe feature.

## Scope decision

The requested block allowed exactly one small Faster-Intro / New-Game / Oak-Lab-Parcel change. Read-only CFRU review found that the current local source already covers the intro controls-guide skip and Oak tutorial absence, but does not expose editable source scripts for a broader Oak speech, Lab, Route 1 Parcel, Viridian Mart Parcel or return-to-Oak shortening.

The next possible changes would require either:

- raw address-level replacement in the existing byte-replacement surface, or
- a multi-map script replacement/design using external decomp reference as guidance.

Both options exceed this block: they are broader than one isolated QoL feature, and the second option would need a dedicated design pass to avoid copying upstream script source or changing multiple subflows at once.

## Read-only source reviewed

| Area | Local evidence | Result |
|---|---|---|
| Intro controls guide | `02_external/CFRU-expansion/src/config.h` defines `SKIP_INTRO_CONTROLS_GUIDE`; `02_external/CFRU-expansion/bytereplacement` has the guarded controls-guide skip block. | Already CFRU-covered; accepted without additional preserve-smoke; not retested in this block. |
| Oak tutorial battle | `src/config.h` leaves `TUTORIAL_BATTLES` disabled; `src/overworld.c` gates tutorial trainer battle behavior through that compile-time path. | Already CFRU-covered; accepted without additional preserve-smoke; not retested in this block. |
| Oak intro visuals | `src/scripting.c`, `src/catching.c` and `assembly/hooks/general_hooks.s` contain Oak intro visual/pokeball helper paths. | Visual/support plumbing only; not a safe New-Game-flow shortening target. |
| Local Pallet scripts | `eventscripts`, `assembly/overworld_scripts/Pallet_town.s` and `strings/Scripts/Pallet_town.string` add local NPC/test/convenience scripts. | Not the vanilla Oak/Lab/Parcel script flow. |
| Local Viridian scripts | `eventscripts`, `assembly/overworld_scripts/viridian_city.s` and `strings/Scripts/viridian_city.string` add local NPC/test scripts. | Not the vanilla Viridian Mart Parcel flow. |
| Local overworld script inventory | `assembly/overworld_scripts/` contains system/support scripts plus a small set of local map additions. | No editable local source for the full early-game Parcel chain was found. |
| External decomp reference | Public decomp map scripts show that Oak/Lab/Parcel spans multiple vanilla maps and state flags. | Useful as design evidence only; not copied or ported in this block. |

## CFRU-covered QoL explicitly not touched

Per the user decision, these are treated as covered by the merged CFRU coverage analysis and are not retested or preserve-smoked here.

| Feature | Block status |
|---|---|
| `BW_REPEL_SYSTEM` / Repel-Reuse | CFRU-covered; accepted without additional preserve-smoke; not retested in this block. |
| Auto-run / running indoors | CFRU-covered; accepted without additional preserve-smoke; not retested in this block. |
| Poison / EXP / Runtime Options | CFRU-covered; accepted without additional preserve-smoke; not retested in this block. |
| Reusable TM/HM behavior | CFRU-covered; accepted without additional preserve-smoke; not retested in this block. |
| Item-acquire picture / description presentation | CFRU-covered; accepted without additional preserve-smoke; not retested in this block. |
| Move Items / Select-from-PC / Portable-PC plumbing | CFRU-covered; accepted without additional preserve-smoke; not retested in this block. |

## Minimal implementation proposal

Recommended next block: create a design-only branch that selects exactly one early-game subflow and identifies the local hook before code.

Preferred target: `Oak-Lab-Parcel flow design`.

Design inputs to resolve before implementation:

1. Exact subflow boundary: for example only Viridian Mart Parcel handoff, only return-to-Oak reward flow, or only one lab dialogue compression.
2. Exact ownership: CFRU source hook, script replacement mechanism, byte-replacement policy, or rejected if only raw address patching is possible.
3. Required story state: flags, vars, items, map object visibility, rival/Oak/player positioning and dialogue exits.
4. Non-goals: no controls-guide retest, no Repel/Runtime/TM/HM preserve-smoke, no Field Items, no hidden sparkle, no itemball graphics, no randomizer writer change.

First implementable candidate after that design: one Parcel-chain subflow only, if and only if the design identifies a local CFRU script hook that can be edited without copying external source scripts and without changing additional early-game flows.

## Smoke handoff

If a later implementation branch makes one Faster-Intro / early-script change, use this targeted manual smoke:

| Test | Expected behavior | Pass criteria | Fail criteria |
|---|---|---|---|
| Fresh New Game reaches player control | Existing intro controls-guide skip remains covered by CFRU; the new change does not block initial control. | Player reaches overworld control and can open the menu. | Freeze, missing player object, broken intro state or no control. |
| Selected subflow only | Only the designed Oak/Lab/Parcel subflow is shortened. | The chosen dialogue/script segment is skipped or compressed as designed. | Any unrelated Oak, rival, Route 1, Viridian or Lab state changes. |
| Parcel/story state | Required items, flags and vars are correct after the subflow. | The player can continue the early-game route without duplicate grants or missing story gates. | Softlock, repeated grant, missing required item, blocked exit or broken NPC state. |
| CFRU-covered QoL not retested | Covered QoL remains accepted from prior analysis. | Result notes say CFRU-covered, accepted without additional preserve-smoke, not retested. | Result claims new preserve-smoke coverage for Repel, Runtime Options, TM/HM, item acquire or party/PC QoL. |
| Randomizer boundary | No Field Item, item ball, hidden sparkle or writer behavior is touched. | Existing randomizer-output ownership remains unchanged. | Any randomizer writer/output claim appears in the Faster-Intro result. |

## Caveats

- No new Faster-Intro code was implemented in this block.
- No local build or gameplay run is claimed.
- The current safe implementation boundary is blocked until a dedicated design pass identifies one concrete source hook.
- Existing CFRU-covered QoL remains accepted without additional preserve-smoke and was not retested here.
