# CFRU/DPE Tracker profile contract

**T1 #690 source/synthetic PASS; T2 #691 Phase A source/mock candidate only.**
[Phase A evidence](T2_PHASE_A.md) records source PASS and Lua mock `NOT_RUN`.
Production activation and T2 Phase B / T3–T6 remain **INTENDED FUTURE STATE**.
`CFRUDPE_TRACKER_PROFILE_READY` confirms the public source profile only, not a
runtime-ready profile. The exact locked revisions and source evidence are in
[README.md](README.md). No local runtime addresses or protected artifacts were
used to establish this contract.

## T1 implementation and source evidence

The existing [generator](../../07_scripts/tracker/generate_cfru_dpe_source_data.py)
produces [source-data.json](../../03_tools/tracker-extensions/CFRUDPEExtension/data/source-data.json)
as schema `cfru-dpe-tracker-source-profile`, version 2. The concrete serialization,
field meanings, rejection rules and reproducibility commands are in the extension
[schema](../../03_tools/tracker-extensions/CFRUDPEExtension/SCHEMA.md) and
[README](../../03_tools/tracker-extensions/CFRUDPEExtension/README.md).
T2 Phase A now locks the complete public serialization in Lua before decoding.
Its detached synthetic adapter cannot activate production; Lua execution and
full Phase A acceptance remain pending.

The profile separately binds locked product Workspace
`3bdfe9919afc0b7bea55c79f37285e832be495c3` / tree
`f6bc65355811d7de153a91091b223fec9b50991e` and T0 contract merge
`e6e0e867a5cca4fd2d373acf82504af45986e6fa` / tree
`d3b5b87fd8575ef4313e32be9c3e9490c3fe9b11`. Component/Tracker/reference pins
remain those in the README. Exact generator and public input hashes plus the
canonical content hash identify the T1 implementation without a circular
self-reference to the commit containing the generated output.

**CONFIRMED SOURCE FACTS:** source bounds are species 1440, moves 992,
abilities 255 (the count macro is in CFRU), effective CFRU items 779 and types
25. Counts include holes/sentinels. The 779 `gItemData` rows match active CFRU
IDs with `EXPANDED_NEW_ITEMS` enabled and `UNBOUND` disabled. Three final free
slots are reserved; DPE Shiny slots 779–798 have no effective CFRU rows and are
explicitly `UNAVAILABLE`, not silently admitted under DPE's 799 bound.

Names use source string-row order/encoding and actual item-name tokens.
Numeric aliases are explicit; inactivated UNBOUND definitions are excluded.
The Ogerpon color/Terastal spellings at 1426–1429 and DPE `ABILITY_UNUSED` /
CFRU `ABILITY_LINGERINGAROMA` at 77 are recorded as cross-component slot
differences. Ability dynamic-name selection remains `UNRESOLVED`: the baseline
table name and catalog are source facts, not a live-name fallback. Species
252–276 are ID holes; 706/835/836 lack explicit BaseStats initializers and their
zero-initialized baseline data is unavailable.

Target proof uses Clang ARM `thumbv4t-none-eabi` syntax-only record layouts of
full extracted declarations and source-checked typedefs/constants. No game build
or object is emitted. Sizes are Pokemon 100, BattlePokemon 88, BattleMove 12,
BaseStats 28, Trainer 40, TrainerMonItemCustomMoves 32 and Item 44 bytes. All
member offsets, bitfields and alignment carry source provenance. These are
declared GBA ABI facts, not private-output or runtime validation.

The focused synthetic suite covers representative Gen1/mid-dex/Gen8/Gen9 and
regional IDs, six party slots, expanded moves/abilities/items, byte-10 move
category, aliases/holes/sentinels, missing/invalid source definitions,
schema/revision rejection, dubious layouts/descriptors and byte-identical
regeneration. `--check` validates exact regeneration, including unknown keys.
All address descriptors retain `runtimeAddress: UNRESOLVED`; capability runtime
confidence is `UNKNOWN` with no sample epoch. No T2 activation or BizHawk gate
is satisfied by these tests.

## T1 extension evolution lock repair — Issue #699

**CONFIRMED SOURCE/SYNTHETIC EVIDENCE:** the T1 generator verifies historical
extension blob `294cac84152e87010eb806c6331c90100d204a83` only at the immutable
T0 contract above. Later authorized extension development at Workspace HEAD no
longer invalidates locked source facts. Exact product/contract trees, all five
current HEAD component Gitlinks, component checkout revisions, allowlisted
committed inputs, configuration, schema and ARM ABI checks remain required.
Extension/runtime compatibility remains the independent, unproved #691/T2 gate.

The generator change intentionally regenerates schema v2 without changing
source facts. Only `metadata.generator.sha256` and `metadata.profileId` differ
from the #690 profile; every input hash, mapping, layout and historical reference
is preserved. The whole public JSON hash also changes:

| Identity | Accepted #690 | Repaired #699 |
| --- | --- | --- |
| Generator SHA-256 | `1e515d7cf924ac7ab2f3bc311c8f4f6b2f348c25656d4e307356390341422210` | `9c6fcf0a631557defaef64f5ac78db8df483d359d4f6e7a4708011ee2dd70beb` |
| Canonical profileId | `sha256:3986250cf9fa35ec26b063c785b034c2d96406e681b77e4c557922c948225235` | `sha256:31be9e07697f939b274c56eea5d92a81dd10c43e7c876586effccb335535ca75` |
| source-data.json SHA-256 | `c89e9767bdd40dc2a2c127c0273cb61ee35c0fdb24ff25c728821ac3271fa353` | `8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981` |

Regression coverage permits an evolved HEAD extension while retaining identical
source output and unresolved runtime capabilities. It rejects a wrong T0
extension blob/tree, drift in each HEAD component Gitlink, and altered generator
or historical-extension provenance even with a recomputed profile identity.
The existing wrong-checkout/input/configuration/schema/mapping/layout/alias tests
remain required.

**Required follow-up after user merge:** resume #691 Phase A on its same draft
branch with a normal integration of current main, without history rewrite or
force-push. Update only that branch's own locked source SHA/profileId constants
and fixtures to the accepted T1 identity, then finish its independent Lua
execution gate. #699 does not change PR #698, its branch or runtime code.

## Identity and trust boundaries

A profile identifies the locked Workspace commit/tree, CFRU, DPE, UPR-FVX and
Tracker commits from the README, the extension/schema revision, relevant public
configuration and the generated mapping/layout revision. A descriptive name
such as `cfru-dpe-gen9` is a selector, not evidence of identity. Keep the locked
product basis distinct from subsequent Workspace documentation/extension commits.

Manual selection is allowed only to choose a candidate. A FireRed header,
species count, plausible Pokemon, filename, successful JSON import or matching
source pins cannot prove that the loaded output belongs to that candidate.
NatDex's marker and metadata addresses are expressly excluded.

Activation requires three independently recorded layers:

1. **Source identity:** exact pins, schema compatibility, relevant configuration,
   unambiguous mappings/layout dependencies and deterministic generation.
2. **Local output binding:** an explicit local record binds the selected output
   to that source profile and its Control/Casual NatDex/IronMON NatDex variant,
   resolved address provenance and allowed randomization semantics. This record
   remains local/ignored; a schema-valid declaration by itself is not proof.
3. **Runtime validation:** later user-owned host/profile acceptance and safe
   identity/layout checks bind that local record to the loaded session, followed
   by per-field sanity and context checks. Any reset, reload or output switch
   invalidates the session binding and requires revalidation.

**UNKNOWN:** a sufficiently discriminating loaded-output identity check is not
established by T0. T1 defines the public identity material; T2 must specify and
test the local binding/verification mechanism before activation. Until it can
prove the association, the candidate remains `UNKNOWN`. Do not solve this by
guessing addresses, reading private artifacts in agent context, adding a ROM
marker or weakening the identity requirement. No new engine work is implied.
Only already validated, narrowly scoped identity reads may precede activation;
unknown address chains must not be probed to discover a profile.

## Manifest split and lifecycle

T1 versions the concrete serialization in the schema linked above. The following
fields/semantics are required; this document contains no executable runtime
address template.

| Artifact / area | Required contents and boundary |
| --- | --- |
| Public source profile | Schema/profile IDs, exact source/Tracker pins, extension compatibility, generator revision and input provenance, public configuration, ID mappings/aliases/holes/sentinels, authoritative names, type mappings, per-table bounds, target layout/ABI assumptions and capability dependencies. No runtime-ready flag inferred from generation success. |
| Public address descriptors | Symbol and source locator; kind (`fixed-symbol`, `pointer-slot`, `repoint-anchor`, `UNRESOLVED`), domain, width, indirection and validation requirements. Public source constants may be represented with provenance; repoint anchors are not automatically readable pointers. No resolved private-build addresses. |
| Local runtime binding | Exact public profile reference, selected output variant and local identity evidence, resolved table/RAM addresses with provenance and validation state, session binding. Existing `game-addresses.local.json` and `tracker-overrides.local.json` naming may be retained behind validation. Do not inspect these in Mac preparation. |
| Field capability | Source, mapping/layout dependencies, applicability, supported contexts, confidence/reason, and current sample epoch. Distinguish source-baseline values from effective output/live values. |
| Sanitized acceptance | Exact source/extension/Tracker/BizHawk/core revisions, output variant labels, tested fields/contexts and PASS/FAIL/NOT_RUN with limitations. No ROMs, saves, states, private paths, raw memory/logs or private artifact hashes. |

Source generation must be deterministic with stable ordering and explicit
schema versioning. Same pins/configuration/inputs must produce the same result.
Missing or ambiguous **required source facts** fail generation. Known optional
unsupported fields may be `UNAVAILABLE`; unresolved runtime targets are explicit
`UNRESOLVED` descriptors and do not prevent source-only T1 completion. They do
prevent activation of every dependent runtime capability. Do not fill required
counts with maximum-ID heuristics or silently select the first alias.

Changed pins, relevant configuration, schema, mapping or layout require a new
profile identity and invalidate old runtime bindings/acceptance for the affected
scope. Runtime/table pointers stay in memory or local ignored input. A source
layout may move from an old local override into the public source profile only
when independently derived from the locked source; copying a private resolved
value is not such a derivation.

Examples are documentation only. Reject placeholders, malformed values, unknown
schema/required keys, incompatible revisions, conflicting aliases, invalid
domains/alignment and out-of-range pointers before importing anything. Numeric
encoding must be explicit: the pinned Tracker interprets JSON strings as hex
and numeric values as decimal. A bare numeric string must not introduce ambiguity.

## Activation and teardown

T2 must implement an idempotent transaction around the early GameSettings seam:

1. Enter a non-ready state; clear all prior values, context and confidence.
2. Validate public profile, local binding and Tracker/extension compatibility.
   Compute the complete required dependency set for enabled capabilities.
3. Validate permitted identity/address descriptors and effective layout. Install
   guarded reader adapters before stock module initialization can consume data.
4. Apply allowlisted GameSettings and nested module overrides, retaining originals.
   Assert the effective fields actually consumed by the pinned reader, including
   party aliases and table sizes. On any partial failure, roll back the whole
   transaction and keep the Tracker on an explicit non-ready/unsupported path.
5. Populate mapped resources and supported data tables, then publish only fields
   whose individual verification conditions pass. No late correction may allow
   an earlier unverified value to enter views, notes or derived calculations.
6. On disable/error/reload/reset/output change, invalidate snapshots immediately,
   undo only extension-owned mutations and restart scripts if required to rebuild
   shared tables. Preserve other owners' function references; a wrapper conflict
   fails activation rather than silently composing incompatible adapters.

`GameSettings.gamename = "Unsupported Game"` is an existing early stop path in
`Main.Run`; the implementation may use it with a clear extension diagnostic.
Returning from a failed extension hook while stock FireRed initialization
continues is not fail-closed. T2 must test failure both before initialization
and after a previously successful session. Unloading while a CFRU/DPE output
remains loaded must keep its affected views non-ready, including across restart;
restoring originals alone is not permission to display stock interpretations.

All memory operations are reads. No ROM/RAM/save mutation, remote code download
or automatic reference update is part of activation. Host options/helpers that
write memory must be disabled or guarded for this profile, including the known
LR-button override. Mock tests must fail if a write function is called.

## Field confidence

Confidence belongs to each field and context, not to a row that merely looks
plausible. Keep the reason/provenance separate from its value.

| State | Meaning | Presentation and downstream behavior |
| --- | --- | --- |
| `VERIFIED` | Exact profile/session identity, field mapping/layout and runtime sanity have been established for this context, with the required revision-bound acceptance. | Display normally through the standard Tracker adapter. Dependent calculations may consume it. A source-only baseline fact must remain labeled as baseline, not promoted to a live value. |
| `UNAVAILABLE` | Known unsupported or inapplicable field/context, explicitly declared by the capability contract. | Show an unavailable indication or an intentionally absent field with a reason. Never manufacture a zero, species, ability or stock substitute. |
| `UNKNOWN` | Identity, binding, layout, mapping, read or context has not been proved, or a previously valid sample is stale/failed. | Hide/clear the value and dependent values; show a non-ready diagnostic. A later valid sample may recover only after all prerequisites pass. |

A global identity/layout failure makes all dependent fields `UNKNOWN`, even
when a previous frame was valid. Known absence (empty party slot, `MOVE_NONE`,
no held item or no primary status) is a verified value only after a successful
read and validated sentinel semantics; missing/read-failed is never equivalent
to zero. One unknown move mapping need not invalidate independently verified HP,
but must invalidate move-derived calculations. A known unsupported battle mode
is `UNAVAILABLE`; an unrecognized mode is `UNKNOWN`.

Use a profile/session/battle epoch to prevent stale rows after transitions.
Validate the context before and after each snapshot; discard inconsistent reads.
At minimum check occupied slot/count, valid mapped species/form, legal level,
HP/maxHP consistency, move IDs/PP, item and ability membership, battler count,
party-index bounds and field read widths. Bounds are necessary but not sufficient
proof of the layout. No fixed small set of plausible species can certify a reader.

## Data sources and precedence

| Field group | Source of truth and acceptance requirements |
| --- | --- |
| Species/form/name/type identity | Public DPE/CFRU ID and string sources, explicit internal-ID/form mappings and type IDs. Distinguish table holes, aliases and supported forms. Macro-name normalization alone is insufficient. |
| Baseline stats/moves/abilities/items | Locked public tables and names. Source verification is possible on Mac. These describe the baseline, not necessarily the selected randomized output. Names/assignments do not certify Gen-9 engine mechanics. |
| Effective species/move data | Later read the validated output's `gBaseStats`/`gBattleMoves` through accepted table bindings when randomization can change values. CFRU category comes from `BattleMove.split`, not vanilla type-derived category or flags bits. Missing table validation yields `UNKNOWN`. |
| Player party | `gPlayerParty` (`GameSettings.pstats`) plus source-correct occupied-slot/count rules and the direct CFRU `Pokemon` layout. Decode species/form, level, HP/maxHP, moves/PP, held item and primary status. Never use vanilla XOR/substructure shuffling. |
| Party ability | `hiddenAbility`, personality selector, effective base-stat assignments and the pinned `GetMonAbility`/`TryRandomizeAbility` semantics. A simple stock two-slot lookup is insufficient; unresolved randomization or alias/name semantics stay `UNKNOWN`. |
| Enemy party | `gEnemyParty` (`GameSettings.estats`) as constructed at runtime, gated to the current encounter. Static trainer rows and synthesized maximum PP cannot replace current party values. |
| Active battle values | Validated `gBattleMons` rows for current species/form, HP/maxHP, level, moves/PP, ability, held item, status and dynamic types/stages. These take precedence over party/base tables for battle-specific values; retain separate party and battle objects. |
| Battler / party mapping | `gBattlerPartyIndexes` read as `u16` at base + 2 × battler index; 0..5 engine slots convert explicitly to Tracker's 1..6 slots. Validate battler positions/side, count, battle flags and partner/two-opponent context before mapping; begin with left slots, expand only with evidence. |
| Trainer context | `gBattleTypeFlags` (`u32`) and validated trainer A/B identities (`u16`), only in an applicable trainer context. CFRU `include/new/multi.h` defines B as `ExtensionState.trainerBTrainerId` (field declared in `include/battle.h`); derive its effective binding and context rather than assume an independent vanilla global. `gTrainers` header/class/name is context only. |
| Extra fields / derived UI | Third type, secondary status interpretation, Tera/Gigantamax, bag, learnsets, static trainer teams, sprites and type/damage calculations need their own capability/mapping coverage. Hide or mark `UNAVAILABLE` when intentionally unsupported; do not inherit plausible stock data. No new engine mechanics or expanded product scope follows. |

GBA structure facts must carry source locators and a target ABI proof method.
CFRU's commented `BattlePokemon` offsets and byte-only `BattleMove` are useful
starting evidence. Bitfields, padding, pointer-containing structs and selected
configuration need explicit verification in T1/T3/T4. Native macOS `sizeof` is
not GBA ABI evidence. Source/synthetic fixtures can establish decoder behavior;
they cannot validate a local runtime address or emulator integration.

## Verification gates and unresolved work

| Owner | Required evidence / current unknown |
| --- | --- |
| T1 #690 | **Source/synthetic PASS:** schema v2, exact provenance, authoritative table names, explicit mapping boundaries, item coverage and ARM ABI extraction; synthetic/negative fixtures and byte-identical regeneration. The old v1 prototype is superseded. No runtime acceptance. |
| B1 #689 | **PENDING_LINUX_HOST / NOT_RUN:** exact BizHawk build/core/Lua settings, read domains/frame execution, boot/input/save-reload/battles. No emulator failure is inferred from host unavailability. |
| T2 #691 | Loaded-output identity mechanism, transactional import/read-back, early initialization guard, wrapper ownership, reset/reload/unload and zero memory writes. Mock wrong pins/schema, partial/missing manifests, invalid pointers and stale sessions; local Linux smoke follows CONTROL review. |
| T3 #692 | Direct party ABI/decoder and effective randomized values, hidden ability/name aliases, field and multi-slot fidelity. |
| T4 #693 | Stable battle gate, second-trainer semantics, supported doubles/multi mapping, dynamic field precedence and transition invalidation. Historical battle plausibility smoke does not satisfy this. |
| T5 #694 | Complete consumer/view coverage in unmodified Tracker, including suppression of stock derived values and persisted stale data. API/wrapper sufficiency must be demonstrated, not assumed. |
| T6 #695 | Revision-bound Control/Casual/IronMON E2E and residual limitations after B1–T5. No unresolved wrong-data S0/S1-equivalent defect; explicit unsupported fields. |

CONTROL's 2026-10-07 #691/#500 disposition additionally authorizes T2 Phase A
Mac-only source/mock preparation after #690 / PR #697. Its exit marker requires
actual mock PASS and is not live activation. Further Mac-only contracts still
need explicit CONTROL routing. No T0 source finding grants live compatibility,
#500 acceptance or #501 freeze. The dependency order and final markers are maintained in the README.
