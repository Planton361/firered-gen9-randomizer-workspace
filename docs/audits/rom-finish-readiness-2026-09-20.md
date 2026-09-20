# M-014 Phase R0 — ROM Finish Readiness Audit

**Issue:** [#498](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498)
**Audit branch:** `audit/498-rom-finish-readiness`
**Audit date:** 2026-09-20
**Evidence classification:** CONFIRMED CURRENT STATE for the inspected source and
repository facts; INTENDED FUTURE STATE for the resulting runtime gate.

## Verdict

`ROM_SCOPE_READY_FOR_ACCEPTANCE`

The bounded ROM-side pilot has no `MISSING_BLOCKER` or `UNKNOWN_BLOCKER`.
All required implementation contracts found in the audit are present in the
current pinned source and are classified as needing the user-owned Phase R1
runtime acceptance. Explicit mechanics, form, workflow, and optional-QoL
limits are recorded rather than treated as silently working.

### Classification counts

The counts cover 48 unique rows below: 6 data rows, 6 engine-boundary rows,
and the 36 M-012/QoL rows. The Faster FireRed subsection cross-references
those rows and is not counted again.

| Disposition | Count |
| --- | ---: |
| `REQUIRED_PRESENT` | 0 |
| `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | 29 |
| `INTENTIONAL_DIFFERENCE` | 8 |
| `OPTIONAL_BACKLOG` | 2 |
| `OUT_OF_PILOT` | 9 |
| `MISSING_BLOCKER` | 0 |
| `UNKNOWN_BLOCKER` | 0 |

## Exact revision basis

| Identity | Exact revision used for this audit |
| --- | --- |
| Workspace source basis / expected `main` | `7b77600a3091cba1c26cac0b7ffc0bfeb63b291f` |
| CFRU Expansion | `8bc8c38210ddba0b05c933dbda06cb4539254c7a` |
| Dynamic Pokémon Expansion Gen 9 | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX, boundary reference only | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` |
| Cyan FireRed NatDex | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| Faster FireRed public README | `db21d777083757067f242c62f592534f40bb2c77` |

The audit branch was created from the expected Workspace `main` revision. The
UPR-FVX pin was read only to distinguish a ROM-owned behavior from a
randomizer output tweak; UPR-FVX is not accepted by this phase.

The Faster FireRed comparison uses only the public README at the exact commit
above. No IPS, BPS, UPS, binary patch, ROM, save, emulator state, screenshot,
generated build, tool binary, private log, secret, or protected path was
accessed.

## Product-finish definition

For this issue, “ROM-side ready for acceptance” means:

1. Gen 1–9 species/data tables provide the selected safe representation
   profile: species data, Base Stats, level-up learnsets, and reviewed ability
   assignments/names, without claiming universal modern mechanics.
2. The CFRU engine boundary is explicit. Existing supported semantics remain
   usable; unsupported Gen-9 mechanics and unsafe form/ability/move cases are
   bounded or excluded rather than implied to work.
3. M-001 through M-009, M-013, the earlier 19-Center Name Rater rollout,
   current CFRU QoL, all 36 M-012 entries, and every Faster FireRed README
   behavior relevant to the pilot have one explicit disposition.
4. The exact current source/build basis is sufficient for the user-owned Phase
   R1 run. Static/build evidence is not converted into a runtime claim.

This is the bounded pilot contract described by Issue #498 and the canonical
milestones. It is not literal 1:1 NatDexExtension or Faster FireRed parity,
universal Gen 1–9 mechanics, a full playthrough, a ROM freeze, or UPR-FVX
acceptance.

## Evidence method and source anchors

The audit inspected the current pinned CFRU/DPE source directly and used
milestone documents only as cross-references. In particular, the accepted
M-001–M-009 ancestry and M-013 merge were checked as ancestors of current CFRU
`8bc8…`:

| Accepted source point | Ancestor verified in current CFRU pin |
| --- | --- |
| M-001 | `8e3fa8378d67dfe4011d6994469c3806f32764c4` |
| M-002 | `9548877aa481750b825c765c4d72fce90d633c16` |
| M-003 | `215bd44d340c16076b1817b9c6db038d54fe5f76` |
| M-004 | `520fc7feeb7494b5f8f0555e348c13f0e847304b` |
| M-005 | `4a9698467600500d18ec8c08f9269f0d6ad008e6` |
| M-006 | `237fc61ac52bea6978f4b434c06fc3f1f11e5dcc` |
| M-007 | `62298cf81d4a2b487c8793bad8b6e29906c705f4` |
| M-008 | `a869c3526d7f76c54082bc71e236742564319e02` |
| M-009 | `827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec` |
| M-013 | `cf820ee2908fa81a1663f61d8dd84c9c76328565` |
| Coherent learnset integration | `c483410d44c1b592e8039e631556cadab2352b3a` |

The source files used most often are the [CFRU config at the exact
pin](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/config.h),
[overworld behavior](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/overworld.c),
[input handling](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/read_keys.c),
[item/purchase handling](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/item.c),
[map overlays](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/mapobjectoverlays),
[fast-start scripts](https://github.com/Planton361/CFRU-expansion/tree/8bc8c38210ddba0b05c933dbda06cb4539254c7a/assembly/overworld_scripts),
[M-009 frame hook](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/m009_overworld_frame.c),
[M-009 scanner](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/hidden_item_sparkle.c),
and [current integrated learnsets](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/Tables/level_up_learnsets.c).
The DPE checks used the [species definitions](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/include/species.h),
[Base Stats](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/Base_Stats.c),
and [learnset source](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/Learnsets.c).
The running ownership boundary was checked in [UPR-FVX's exact pinned
`Gen3RomHandler`](https://github.com/Planton361/upr-fvx/blob/0e3be63e94e34215cc35308d64e8db15e9a3c48c/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java).

## Gen 1–9 data closure

| ID / feature | Reference/source | Why it matters; owner | Actual current source behavior; existing evidence | Disposition | Exact remaining action |
| --- | --- | --- | --- | --- | --- |
| D01 Species and data availability | DPE `species.h`, `Base_Stats.c`; CFRU expanded tables and `NATIONAL_DEX_COUNT` | Randomizer outputs, summaries, encounters, and scripts need valid species IDs; DPE/CFRU data ownership | DPE defines IDs through `SPECIES_PECHARUNT` (`0x59F`) and `NUM_SPECIES`; current Base Stats includes Gen-9 entries such as Palafin, Ogerpon, Terapagos, and Pecharunt. Static source is current; Runtime Gate 1 user evidence passed representative Gen-9 data. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 G/H: exercise representative Gen-1, Gen-8, Gen-9 species, forms, display, save/reload, and crash boundaries. |
| D02 Base Stats and related species data | DPE `Base_Stats.c`; coherent data audit; current CFRU data tables | Stats, type/exp/egg behavior, randomizer data preservation; DPE owns source data and CFRU consumes the integrated tables | The current data review records 1,293 comparable approved Base Stats rows matching the selected reference, with blocked ability slots excluded; current source contains the reviewed Gen-9 rows. Runtime Gate 1 user evidence passed tested Stats. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 G/H: verify representative stats/types/abilities in summary and battle paths within the supported profile. |
| D03 Level-up learnsets | DPE `Learnsets.c`; CFRU `level_up_learnsets.c`; coherent learnset policy | Start moves, level-up, Move Reminder, and randomizer learnset preservation depend on one coherent table per species/form | Current CFRU contains the merged coherent table and explicit pointers for Gen-9 and reviewed form families, including Zarude, Pichu Spiky, Pikachu Cosplay, Zygarde, and Ogerpon families. The source contract, sanitizer, and negative mutations were recorded passing; Runtime Gate 1 user evidence passed representative learnsets and persistence. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 A/G/H: verify representative start, level-up, Move Reminder, Summary, and save/reload behavior. |
| D04 Ability assignments and names | DPE `Base_Stats.c`; CFRU ability tables and reviewed alias table | Abilities must be present and named without implying unsupported effect semantics; DPE/CFRU own data and engine interpretation | Current assignments/names are present for the selected data profile. Reviewed aliases preserve existing engine effects where applicable; the review records 44 behavior-blocked ability cases, not silently working Gen-9 mechanics. Runtime Gate 1 user evidence passed tested Abilities. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 G/H: verify supported assignments/names and fail-closed behavior for the explicitly blocked effect families. |
| D05 Reviewed form ownership and mappings | DPE form constants/data; CFRU integrated learnset pointers; Cyan/NatDex reference revisions | Forms must use stable ownership and coherent data rather than accidental union/fallback behavior; DPE/CFRU share the representation boundary | Current source explicitly maps reviewed families such as Pikachu Cosplay, Pichu Spiky, Rotom, Zygarde, Necrozma, Magearna, Zacian/Zamazenta, Zarude, Ogerpon, and Palafin data. No new form-transition engine is inferred from those tables. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 G: exercise supported representative forms and confirm unsupported form/state cases remain bounded. |
| D06 Safe representation limits and exclusions | Current data review; M-012/A13; DPE/CFRU source | Prevents a data table from being mistaken for complete Gen-9 mechanics | The reviewed boundary records 29 open-risk form families, 18 Ally Switch-blocked learnset tables, 44 behavior-blocked abilities, and the unsupported Shadow Warrior/sentinel cases. They remain explicit profile limits; no silent fallback or new mechanics were added. | `INTENTIONAL_DIFFERENCE` | Keep unsupported cases out of mandatory R1 inputs and record any encountered case as an approved profile exclusion, not as universal support. |

## Engine-boundary closure

| ID / feature | Reference/source | Why it matters; owner | Actual current source behavior; existing evidence | Disposition | Exact remaining action |
| --- | --- | --- | --- | --- | --- |
| E01 Selected CFRU/DPE semantics | CFRU config, battle/data tables, DPE source; M-012 and M-014 boundary | The pilot needs the selected data and existing engine semantics, not an unbounded battle rewrite; CFRU/DPE own this boundary | `EXPAND_MOVESETS`, expanded species/items, and existing Mega/Dynamax/Terastal systems are present. Current source does not claim every modern mechanic or every form transition. Targeted Runtime Gate 1 passed selected data paths only. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 G/H: run only the supported profile representatives and preserve the explicit exclusions below. |
| E02 Commander, Hospitality, Embody Aspect | Issue #498 boundary; ability review; CFRU source | These named mechanics would change battle behavior and are explicitly excluded from the pilot | Current tables may contain names or data aliases, but no accepted current implementation of the full Commander, Hospitality, or Embody Aspect mechanics was found. This is documented as an engine limit, not a hidden pass. | `OUT_OF_PILOT` | None for R0/R1; do not add these mechanics to the acceptance package. |
| E03 Modern ability/form state transitions | DPE data for Palafin/Ogerpon/Terapagos; current CFRU battle hooks | Data availability must not be confused with automatic modern state transitions | Data/form entries exist, but the audit does not establish universal Zero to Hero, mask/state, or other modern transition semantics. Those transitions are outside the accepted ROM profile. | `OUT_OF_PILOT` | None for ROM closure; test only explicitly supported static representations in R1. |
| E04 Terastal and new form-transition expansion | CFRU `TERASTAL_FEATURE`; Issue #498 explicit non-goal | Existing CFRU Terastal support must not be promoted into a new NatDex parity project | `TERASTAL_FEATURE` and its flag are defined in the current CFRU source. No new Terastal/form-transition system was added solely for Gen-9 parity, and no universal transition claim follows. | `OUT_OF_PILOT` | None; retain the current CFRU boundary and do not broaden R1. |
| E05 Ability effect aliases and blocked modern effects | Reviewed ability alias table; CFRU ability engine | Names/assignments can be usable while effects intentionally remain legacy or blocked | Current source preserves reviewed aliases to existing effects and does not implement the 44 blocked behavior families. This is an explicit semantic difference from a full modern engine. | `INTENTIONAL_DIFFERENCE` | Keep the reviewed supported/blocked list attached to R1 evidence. |
| E06 Unsupported move/form consumers and sentinel paths | Coherent learnset audit; CFRU pointer table | Fail-closed behavior is required so unsupported data cannot look accepted | The current table has no unbound pointer among the reviewed bound slots; Ally Switch-blocked tables retain their legacy data, and the sentinel/Shadow Warrior paths remain explicitly excluded. | `INTENTIONAL_DIFFERENCE` | Do not manufacture mandatory tests for excluded consumers; record any R1 encounter against the profile boundary. |

## QoL and game-flow closure matrix

The following 36 rows reconcile all M-012 entries against the current pinned
source. Each row has one top-level disposition. `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE`
means the implementation/configuration is present and source-backed, but R1
must still exercise the behavior; it does not mean that this audit ran it.

| ID / feature | Reference/source | Why it matters; owner | Actual current source behavior; existing evidence | Disposition | Exact remaining action |
| --- | --- | --- | --- | --- | --- |
| K01 Repel reuse | M-012 K01; CFRU `BW_REPEL_SYSTEM` | Reduces repetitive Bag interaction; CFRU overworld/scripts | Current source stores the last Repel and routes expiry to the reuse script with the configured step branches. Static source verified. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B/E: expire and reuse stocked Repels, including the stated branches. |
| K02 Running indoors | M-012 K02; CFRU `CAN_RUN_IN_BUILDINGS` | Indoor traversal is a ROM QoL; CFRU movement owns it | Current running restriction omits the indoor-map prohibition when `CAN_RUN_IN_BUILDINGS` is defined, while retaining tile, underwater, and availability checks. UPR's indoor-running patch is a no-op for this profile. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B: verify indoor running and retained disallowed-tile behavior. |
| K03 Auto-run | M-012 K03; CFRU `FLAG_AUTO_RUN`, `read_keys.c` | Comfort and reset speed; CFRU input/overworld | L toggles `FLAG_AUTO_RUN`; B walks while auto-run is active. The current source still gates running on `FLAG_RUNNING_ENABLED`. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B: verify L/B behavior after running is enabled and the documented L=A tradeoff. |
| K04 Reusable TMs | M-012 K04; CFRU `REUSABLE_TMS`, `item.c` | Repeated randomized TM use; CFRU item/TM handling | `REUSABLE_TMS` and `CheckReusableTMs` are active, with the required item metadata contract. This intentionally differs from the inspected consumable NatDex behavior but is the approved pilot model. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B/G: teach, replace, and re-use representative randomized TMs. |
| K05 HM convenience | M-012 K05; CFRU `ONLY_CHECK_ITEM_FOR_HM_USAGE` | Avoids forcing an HM move into a moveset; CFRU field/party checks | Current behavior requires the HM item and a compatible party Pokémon while retaining badge/location checks. It is not the NatDex modern HM menu/no-compatible-party model. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B: verify the approved item-plus-compatible-party behavior; do not test an unapproved menu rewrite. |
| K06 Forgettable HMs | M-012 K06; CFRU `DELETABLE_HMS`, `item.c` | Prevents permanent HM moves; CFRU item/learn flow | `CheckIsHmMove` returns the deletable-HM path under the active define. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B/G: delete and replace representative HMs. |
| K07 Select from PC | M-012 K07; CFRU `SELECT_FROM_PC`, `scripting.c`, hooks | Supports services that need box/party selection; CFRU script service | Select-from-PC capability and helpers are active. This does not claim every service, including the Name Rater, exposes PC selection. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B: exercise the accepted service path only; retain the universal-UI limitation. |
| K08 Party Move Items | M-012 K08; CFRU `party_menu.c` | Convenient held-item transfer; CFRU party menu | `MENU_MOVE_ITEM` reaches the transfer callback, rejects invalid targets, and updates held-item state/icons. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B: verify give/take/move and the supported invalid-target boundaries. |
| K09 Item acquire picture/description | M-012 K09; CFRU acquire config and `scripting.c` | Makes unfamiliar randomized items understandable; CFRU item/script UI | `ITEM_PICTURE_ACQUIRE` and `ITEM_DESCRIPTION_ACQUIRE` are active, including first-obtain descriptions and hidden-pickup paths. The source still documents the Game Corner caveat; it is not silently certified fixed. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B/G: verify normal and hidden item acquisition and record the documented caveat if reached. |
| K10 Options / Start plumbing | M-012 K10; CFRU options/start systems | Keeps rule and pacing controls usable; CFRU UI/flags | Current multi-page Options/Start plumbing and existing flag-owned modes are present. Exact NatDex HM/BGM additions are not implied. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B: verify the accepted current pages and defaults, not excluded NatDex menu features. |
| K11 Auto lowercase | M-012 K11; CFRU `AUTO_NAMING_SCREEN_SWAP` | Faster naming without losing exceptions; CFRU naming UI | Auto lower-case page swapping is active with the documented number/phrase/password exceptions. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B/G: verify representative naming screens and exceptions. |
| K12 Premier Balls | M-013; CFRU purchase callback | Required bounded purchase parity and economy safety; CFRU item/shop task | Current callback handles ball-pocket purchases separately, awards `floor(quantity / 10)`, clamps to capacity, and leaves non-ball reward policy in place. Exact source is in the current CFRU pin; Runtime Gate 1 user evidence passed quantity/capacity/cancel controls. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B: repeat the full Premier quantity, capacity, and cancellation cases in the exact run identity. |
| K13 Controls-guide skip | M-012 K13; CFRU `SKIP_INTRO_CONTROLS_GUIDE`, `bytereplacement` | Removes repeated control instruction in a fresh run; CFRU intro integration | The define and guarded byte replacement are active in current source. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 A: verify the actual fresh-game intro reaches the remaining Oak flow. |
| K14 Name Rater | Earlier accepted rollout; M-012 K14; CFRU overlays/script | Local renaming convenience; CFRU map overlays/script | `mapobjectoverlays` contains 19 Name Rater appends, and the current script retains egg and traded/OT rejection checks. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B: exercise representative Centers and rejection/rename paths. |
| K15 M-001 gold TM/HM balls | M-001, M-012 K15; CFRU overlays | Visual distinction for approved TM/HM pickup classes; CFRU map graphics | Current overlays contain 29 gold-ball graphics replacements: 28 TMs plus HM07, using the approved graphic; generic control balls remain unchanged. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B: verify representative TM, HM07, and non-target item-ball visuals. |
| K16 M-002 Forest Nurse | M-002, M-012 K16; CFRU Forest overlay/script | Early healing with the poison restriction; CFRU map/script | The current overlay replaces the intended Forest object and the script gates healing on a poisoned party before the normal Yes/No flow. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 A/B: verify poisoned refusal, clean-party healing, and persistence. |
| K17 M-003 instant PokéCenter | M-003, M-012 K17; CFRU Center overlays/scripts | Shorter repeated healing; CFRU Nurse scripts/overlays | There are 19 ordinary Center script replacements. Trainer Tower is excluded deliberately and its bookkeeping is preserved. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 B/D: verify ordinary Centers and confirm the Trainer Tower exception. |
| K18 M-004 renewable step items | M-004, M-012 K18; CFRU `renewable_hidden_items.c` | Predictable renewable resources; CFRU renewal hook/tables | Current source preserves the 1,500-step cycle and the approved Underground/Sevii guarantee policy while excluding Mt. Moon from that guarantee. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 E: exercise approved guaranteed groups, an excluded Mt. Moon case, and reset controls. |
| K19 M-005 Lab Potion / PC item relocation | M-005, M-012 K19; CFRU overlays and Lab/PC scripts | Visible early supply without duplicate PC grants; CFRU map/init | Current overlay appends one normal Potion ball to Oak's Lab and the source clears the old PC item slot without adding a duplicate Potion there. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 A/B: verify the Lab item, persistence, and no duplicate grant. |
| K20 M-006 faster New Game / Mom | M-006, M-012 K20; CFRU Mom/Lab scripts | Shorter fresh starts while retaining starter/Rival ownership; CFRU scripts/scene overlays | Mom handoff sets the Lab scene, places Oak/player, skips the vanilla entrance/eight-tile walk/Rival waiting dialogue, and reaches the existing starter prompt. Later starter/Rival scenes remain. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 A: verify Mom, camera/warp, starter, Rival, save, and early progression. |
| K21 M-007 shortened Oak Parcel | M-007, M-012 K21; CFRU Route 1/Pallet scripts | Removes delivery detour and Old Man roadblock; CFRU story scripts | Route 1 clerk gives the Parcel, Pallet Oak returns it, grants the existing story rewards, and sets the Old Man scene to skip the catching tutorial. National Dex timing remains intentionally unchanged. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 A: verify clerk/Oak handoff, one-time rewards, Old Man bypass, and downstream scenes. |
| K22 M-008 optional Bill / Sevii | M-008, M-012 K22; CFRU Cinnabar overlay/script | Removes a forced invitation while retaining player choice; CFRU story scripts | Current source replaces only the automatic scene-1 entry, removes the outdoor Bill interruption, and preserves the Center Bill Yes/No travel path. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 F: verify optional travel, return, and persistence. |
| K23 M-009 hidden-item sparkle | M-009, M-012 K23; CFRU frame/scanner | Makes eligible hidden items visible; CFRU frame tail/effect | The current frame tail scans visible normal hidden-item events, excludes collected/none/underfoot items, uses a transient task cache/cooldown, and fails closed for unsupported event counts. The accepted policy is always on rather than NatDex's optional flag. | `REQUIRED_NEEDS_RUNTIME_ACCEPTANCE` | R1 C: exercise global frame/lifecycle/menu/warp/battle/Quest Log cases and retain the recorded caveats. |
| A01 Running from the start | M-012 A01; CFRU running flags; UPR running tweak boundary | Distinguishes ROM-owned running from an output modification; CFRU/UPR own different layers | The ROM source keeps `FLAG_RUNNING_ENABLED` as the gate; it does not grant shoesless running at New Game. UPR-FVX has a separate CFRU-specific output tweak that bypasses the running branch, but that is not a ROM-source default and is not accepted here. | `INTENTIONAL_DIFFERENCE` | No R0 action. If a later product decision requires shoesless output, open/accept it in the randomizer phase after ROM profile lock. |
| A02 Cinnabar paid Move Relearner | M-012 A02; NatDex/Cyan reference; current CFRU overlays/events | Optional convenience, not required to close the bounded pilot; CFRU service/overlay | The existing relearner exists, but the NatDex-style Cinnabar placement is not in current overlays/events. | `OPTIONAL_BACKLOG` | Keep as a separate future decision/implementation contract; it does not block R1. |
| A03 Full modern HM menu / no compatible-party requirement | M-012 A03; NatDex HM/start/options references | A broader usability model would change field/menu semantics; CFRU field/menu | Current CFRU provides the approved item-plus-compatible-party convenience, not the full NatDex modern HM menu. | `OUT_OF_PILOT` | None; do not expand M-014 into this port. |
| A04 Global BGM on/off | M-012 A04; NatDex options/sound reference; CFRU options | A separate audio policy is not required by the confirmed finish line; CFRU options/audio | Current Options provide mono/stereo and battle-music choices, not the NatDex global BGM mute control. The historical “UNKNOWN” is resolved to out-of-pilot by the current product contract, not promoted to a blocker. | `OUT_OF_PILOT` | None for R0/R1; reopen only with an explicit product decision. |
| A05 Optional sparkle activation | M-012 A05; NatDex scanner/init; current M-009 source | Marker policy is a product choice; CFRU frame/scanner | Current M-009 has no activation flag and is always on. This is the accepted M-009 policy, not a missing sparkle implementation. | `INTENTIONAL_DIFFERENCE` | R1 tests always-on behavior; no opt-out patch is part of this gate. |
| A06 National Dex at Parcel | M-012 A06; NatDex Pallet handoff; current M-007 | Early Dex unlock changes progression; CFRU story state | M-007 deliberately does not call the early National Dex unlock and preserves the existing later-game policy. | `INTENTIONAL_DIFFERENCE` | None; retain the boundary in R1. |
| A07 Instant text / held-button scrolling / fast messages | M-012 A07; NatDex text/options; current CFRU text/input | Pacing choices should not be silently changed; CFRU text/input | Current source does not establish a blanket instant-text default. Existing options/fast battle-message paths remain available, and no universal dialogue rewrite is in the pilot. | `INTENTIONAL_DIFFERENCE` | R1 checks only the accepted current options; do not infer a mandatory instant mode. |
| A08 Broader Oak speech / pre-overworld intro rewrite | M-012 A08; NatDex intro; M-006 source | Full exposition rewrite is deeper than the approved fast handoff; CFRU story scripts | Controls-guide skip and M-006 handoff are present, but current source retains Oak's core speech/selection sequence and does not replace the whole intro. | `OUT_OF_PILOT` | None; do not reopen M-006 as a broad intro rewrite. |
| A09 Friendship Boost | Faster FireRed README; ROADMAP/M-012 A09 | Explicitly optional and contrary to the standard challenge intent; CFRU policy | No approved Friendship Boost service is present. Other friendship runtime features are not this README behavior. | `OPTIONAL_BACKLOG` | No action in ROM closure; only a later explicit product decision could promote it. |
| A10 Portable PC / Safari expansion / display redesign | M-012 A10; existing CFRU capabilities | These are capability/distribution choices, not required pilot behavior; CFRU items/flags/UI | Current CFRU has related capability/configuration, but no new distribution or broad display redesign is required by the pilot. | `OUT_OF_PILOT` | None; preserve existing capability without changing availability policy. |
| A11 Broader item-ball colors / underfoot sparkle / new Itemfinder cues | M-012 A11; NatDex sparkle/Itemfinder; M-001/M-009 | Avoids turning a finite visual contract into an unbounded graphics port; CFRU graphics/effects | M-001 covers the approved 29 gold-ball targets and M-009 covers eligible visible hidden items. No required missing visual class was established. | `OUT_OF_PILOT` | None; retain the approved classes and existing Itemfinder/pickup behavior. |
| A12 Non-ball purchase bonuses | M-012 A12; NatDex shop; current CFRU `sPurchaseRewards` | Economy differences must be explicit; CFRU purchase callback/table | The current callback fixes ball-pocket Premier parity while preserving the existing custom non-ball reward table. Removing those unrelated rewards is not part of M-013. | `INTENTIONAL_DIFFERENCE` | R1 verifies Premier behavior; do not broaden the economy contract. |
| A13 NatDex events/AI/rules/battle/workflow modernization | M-012 A13; Issue #498 explicit exclusions | Broad parity would expand product scope; CFRU/DPE engine and project contract | Current CFRU/DPE retains existing supported systems and selected options; no Commander, Hospitality, Embody Aspect, broad AI/rule/workflow rewrite, or Tracker integration is claimed. | `OUT_OF_PILOT` | None; keep these out of the ROM and R1 finish line. |

## Faster FireRed parity

The exact [Faster FireRed README](https://github.com/DrMaple/Faster-FireRed/blob/db21d777083757067f242c62f592534f40bb2c77/README.md)
lists twelve behavior references relevant here. Eleven are represented in the
current pilot source and are mapped to the required rows below. Friendship
Boost is the only README behavior intentionally not included in the pilot; it
is recorded as `OPTIONAL_BACKLOG`, not as a missing blocker.

| README behavior | Current pilot mapping and source conclusion |
| --- | --- |
| Visible hidden items | K23 / M-009 current frame/scanner source; present with the accepted always-on and lifecycle caveats. |
| Viridian Forest Nurse poison restriction | K16 / M-002 current overlay/script; present. |
| Talk to Mom to start | K20 / M-006 current Mom handoff; present. |
| Shortened Oak Parcel flow | K21 / M-007 current Route 1/Pallet scripts; present, with National Dex timing intentionally unchanged. |
| Repel reuse prompt | K01 / current `BW_REPEL_SYSTEM`; present. |
| Gold TMs | K15 / M-001 current 29-target overlay; present. |
| Name Raters in PokéCenters | K14 / current 19-overlay rollout and Name Rater script; present. |
| Instant Center healing | K17 / M-003 current 19 ordinary-Center replacements; present, with Trainer Tower intentionally excluded. |
| Guaranteed Underground/Sevii step items, excluding Mt. Moon | K18 / M-004 current renewal source; present with the stated group boundary. |
| PC item moved to Oak's Lab | K19 / M-005 current Lab overlay/PC initialization; present without a duplicate grant. |
| No forced Bill/Sevii invitation | K22 / M-008 current Cinnabar scene replacement; present while Center Bill travel remains interactive. |
| Optional one-use Friendship Boost | A09; no approved service; optional/non-standard and not required. |

Therefore the answer to the special parity question is: **yes, every
non-Friendship README behavior is present or bounded by an explicitly stated
intentional exception, and Friendship Boost is the only README behavior
excluded from the pilot.** No undocumented Faster FireRed behavior was
inferred from a binary patch.

### What Faster New Game actually skips

The current source has three distinct skips, not a claim that all Oak speech
is gone:

1. `SKIP_INTRO_CONTROLS_GUIDE` activates the existing controls-guide byte
   replacement.
2. M-006's Mom handoff sets Oak's Lab scene 1 and skips the vanilla Oak
   entrance, the eight-tile player walk, and the Rival waiting dialogue before
   reaching the existing starter prompt. Starter selection, later Rival flow,
   and Oak's core selection speech remain source-owned.
3. M-007's Parcel completion sets the Viridian Old Man scene to `2`, skipping
   the Old Man catching tutorial/roadblock after the Parcel handoff. It does
   not unlock the National Dex early.

`TUTORIAL_BATTLES` is commented out in the current CFRU config, so the
compile-time Oak tutorial battle is not enabled. A separate
`FLAG_ACTIVATE_TUTORIAL` hook remains in generic CFRU battle plumbing; that
capability is not evidence that the skipped Old Man flow is active. R1 A/C
must verify the actual fresh-game sequence and any applicable tutorial flags.

## NatDex / M-012 reconciliation

M-012 was an analysis matrix, not a source-free acceptance list. This audit
rechecked the current CFRU source for all 36 entries:

- K01–K11 are still source-backed current CFRU behavior.
- K12 is no longer an old “missing small QoL”: M-013's current purchase
  callback is present, including the ball-pocket path and capacity clamp.
- K13–K23 are source-backed current M-001–M-009 or earlier Name Rater
  behavior. The current map overlay census is 19 Name Rater appends, 19
  ordinary-Center script replacements, and 29 gold-ball graphics rows (28 TM
  rows plus HM07).
- A01 and A05–A07/A12 are deliberate current-policy differences.
- A02 is the only non-Faster optional implementation backlog identified by
  this audit: the Cinnabar paid Move Relearner placement.
- A03, A04, A08, A10, A11, and A13 are outside the bounded pilot. A04's old
  `UNKNOWN` wording is not carried forward because global BGM is not required
  by the confirmed finish line.
- A09 Friendship Boost remains optional/non-standard and does not block ROM
  closure.

The following historical inventory conclusions are therefore obsolete as
blockers when read without the current source: “missing” M-001–M-009 items,
the old M-013 Premier gap, and any statement that a broader Faster intro or
NatDex feature is silently required. The audit found no genuinely desired
required NatDex QoL absent from the confirmed pilot contract. The optional
Move Relearner, Friendship Boost, global BGM toggle, modern HM menu, early
National Dex timing, and shoesless running defaults remain explicitly deferred
or intentionally different.

## Running/auto-run ownership boundary

The current ROM source provides the desired indoor-running and auto-run model:
`CAN_RUN_IN_BUILDINGS` removes the indoor prohibition, `FLAG_AUTO_RUN` is
toggled by the CFRU input path, and movement retains its normal tile and
availability checks. The ROM does **not** make running available from the
start because `FLAG_RUNNING_ENABLED` remains defined and flag-gated.

UPR-FVX separately contains a CFRU/DPE output tweak for “run without running
shoes”; its current `Gen3RomHandler` path is an output mutation and is not a
ROM-source default. Therefore:

- indoor running and auto-run are ROM-owned behavior for R0/R1;
- shoesless running from New Game is an intentional boundary, not a ROM
  blocker;
- any later selected output tweak belongs to Randomizer acceptance after the
  ROM profile is accepted.

## Build and evidence readiness

The exact-pin source/build basis is sufficient to perform Phase R1:

- The Workspace branch starts from the expected main SHA and the current
  Gitlinks match the exact CFRU, DPE, and UPR-FVX basis above.
- Existing sanitized evidence records a successful full CFRU source build for
  `8bc8c38210ddba0b05c933dbda06cb4539254c7a`, including the authorized public
  audio-source route; the documented result was exit code 0 with only the
  existing linker RWX warning.
- The same current CFRU pin contains the M-013 merge and coherent learnset
  integration. The recorded source contracts, sanitizer/negative checks, and
  M-009 scanner/map checks passed.
- Runtime Gate 1 is a separate user-supplied targeted PASS against Workspace
  test basis `85a963626791ff8ccbfad63bec04b2733558d41e` and the same CFRU/DPE/
  UPR-FVX component pins. It supports selected data and Premier claims but is
  not this R0 audit and is not a full playthrough.

This audit did not rerun a build, inspect generated outputs, or promote any
source/build result into broad runtime acceptance. Phase R1 must record the
exact user-run identity and sanitized result for the 115-case M-014 package;
that is a normal next-gate requirement, not an R0 blocker.

## Mandatory blocker list

There are no mandatory blockers:

- `MISSING_BLOCKER`: **0**
- `UNKNOWN_BLOCKER`: **0**

No source implementation gap or unresolved product-scope question was found
that must be resolved before the user-owned ROM runtime acceptance. In
particular, missing Commander/Hospitality/Embody Aspect behavior, expanded
Terastal/form-transition mechanics, full modern HM menus, and other explicit
engine exclusions do not block this bounded contract.

## Non-blocking limitations and backlog

- Phase R1 remains required. This audit did not run a ROM, emulator, private
  runtime test, Randomizer output, or M-014 case.
- The accepted profile is not universal Gen 1–9 mechanics parity. The
  reviewed form, move, ability, sentinel, and Shadow Warrior limits remain in
  force.
- Cinnabar paid Move Relearner placement and Friendship Boost are optional
  backlog items.
- Global BGM mute, the full NatDex modern HM menu, shoesless-from-start output,
  early National Dex unlock, a broader Oak intro rewrite, broader sparkle/item
  graphics, and broad NatDex workflow/mechanics are intentionally deferred or
  out of pilot.
- The current always-on M-009 behavior and the M-003 Trainer Tower exception
  are intentional profile decisions.
- UPR-FVX, BizHawk, Ironmon Tracker, #499, #500, and upstream contribution
  work are not started by this audit.

## Exact recommended next gate

Proceed to **Phase R1 — ROM runtime acceptance** using the existing 115-case
M-014 A–H package and the exact frozen ROM-side profile:

1. The user runs the applicable ROM-owned cases privately against an exact
   recorded Workspace/build/component identity.
2. The user records sanitized PASS, FAIL, BLOCKED, or approved profile
   exclusion for every required case, with no unresolved S0/S1.
3. The result is accepted as `ROM_PROFILE_READY` only after the runtime
   evidence is reviewed.
4. Only then may Randomizer acceptance begin. BizHawk/#499 and
   Ironmon Tracker/#500 remain later gates.

The prepared package PR #504 remains supporting evidence only and must remain
Draft/HOLD until this gate sequence advances.

`ROM_SCOPE_READY_FOR_ACCEPTANCE`
