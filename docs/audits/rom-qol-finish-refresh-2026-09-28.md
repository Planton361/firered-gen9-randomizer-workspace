# ROM Finish Refresh — Ironmon QoL, Settings & Flow Audit

**Workspace Issue:** [#537](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/537)<br>
**Audit date:** 2026-09-28<br>
**Verdict:** `ROM_QOL_POLISH_REQUIRED`<br>
**Scope:** source and public-documentation review; no implementation

## Decision summary

The current integrated profile is coherent and retains its accepted M-001–M-013 QoL. Four bounded polish families remain before calling the ROM finish polished:

1. Add early duplicate Move Reminder access in Celadon while preserving the Two Island NPC and mushroom price — `PROMOTE_TO_REQUIRED_QOL`.
2. Add the one-time Route 10 HM05 convenience NPC before Rock Tunnel while retaining the Route 2 source and current HM rules — `PROMOTE_TO_REQUIRED_QOL`.
3. Enable the National Pokédex when the existing normal Pokédex is received after the Parcel flow — `POLISH_REQUIRED`.
4. Clarify Trainer AI legacy labels and the Difficulty-derived meaning of `Auto`, without changing setting values or save behavior — `POLISH_REQUIRED`.

Early Running and the current HM use model are confirmed and are not finish blockers. Four held or secondary options, plus additional tutorial shortening, remain non-blocking as classified below.

## Revision and evidence basis

The original Issue #537 body contains a stale revision basis. Its newest CONTROL comments, especially [the 2026-09-28 rebaseline](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/537#issuecomment-5877082184) and [focused source refresh](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/537#issuecomment-5877233407), govern this audit.

| Source | Exact revision used |
|---|---|
| Workspace `main` basis | `c63b30dc5c4baf172f0cb7e81c8bd8d68f76a1d5` |
| CFRU | `11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec` |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX boundary/reference | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| NatDexExtension historical pin | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| Current public NatDex FireRed source | [`CyanSMP64/pokefirered@b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7`](https://github.com/CyanSMP64/pokefirered/tree/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7), linked by [NatDexExtension v1.2.1](https://github.com/CyanSMP64/NatDexExtension/releases/tag/v1.2.1) |
| Faster FireRed | [release 1.3.2](https://github.com/DrMaple/Faster-FireRed/releases/tag/1.3.2) |
| IronMON Patch Editor | [public release 1.2](https://github.com/DrMaple/IronMONPatchEditor/releases/tag/1.2) |

The local workspace branch is `audit/537-rom-qol-finish-refresh`, created from the exact Workspace basis above. Current [M-012](../milestones/M-012.md), [M-013](../milestones/M-013.md), [Early Running integration evidence](../testing/cfru-early-running-workspace-integration-2026-09-28.md), and the current roadmap were used as supporting context. Historical `01_docs/`, `08_tests/`, `00_project-control/`, and prior audit material were not treated as the current decision baseline.

Issues [#538](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/538) and [#539](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/539) show that Early Running is integrated on the current source basis. #538 source checks passed; its completion evidence explicitly does not claim runtime acceptance. [#498](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498) remains the open umbrella; runtime acceptance remains separate, and final Randomizer alignment and #499/#500 remain downstream. This report does not declare `ROM_PROFILE_READY` or user runtime acceptance.

## Settings and UX matrix

The Options UI has three pages. The accepted Fresh New Game profile explicitly sets Game Difficulty `Vanilla`, Trainer Level Scaling `Off`, Wild Level Scaling `Off`, and Trainer AI `Standard`. Other settings inherit the existing FRLG/save defaults; no source evidence in this audit supports changing them. CFRU preserves original raw values for the custom options until the player edits those rows, so any proposed wording change must leave raw values, mappings, and that compatibility path intact.

| Page / setting | Current choices and source-backed meaning | Classification | Disposition |
|---|---|---|---|
| 1 — Text Speed | `Slow / Mid / Fast`; standard text-rate preference. | `KEEP_AS_IS` | Preserve. Further targeted text reduction is a separate secondary candidate below. |
| 1 — Battle Scene | `On / Off`; controls battle transition/scene presentation. | `KEEP_AS_IS` | Preserve. |
| 1 — Battle Style | `Shift / Set`; controls battle switch prompt behavior. | `KEEP_AS_IS` | Preserve. |
| 1 — Sound | `Mono / Stereo`. | `KEEP_AS_IS` | Preserve. The requested global BGM-off option is separately held. |
| 1 — Button Mode | Help / L-R / L=A; FRLG control remapping. | `KEEP_AS_IS` | Preserve choices. Source shows L=A remaps L to A and suppresses the L-button action path used to toggle Auto-Run. Treat that as the existing control-mode tradeoff; it does not change the accepted Early Running decision. |
| 1 — Frame | Existing frame selection (0–9). | `KEEP_AS_IS` | Cosmetic choice; preserve. |
| 2 — R Button Mode | DexNav / Pokémon / Items. | `KEEP_AS_IS` | Preserve the current multifunction setting. |
| 2 — Battle Music | FRLG / RSE. | `KEEP_AS_IS` | Preserve; separate from the held global BGM-off request. |
| 2 — Wild Level Scaling | `Off / On`; accepted fresh default is Off. | `KEEP_AS_IS` | Preserve as a separate wild-scaling choice. |
| 2 — AutoSort Bag | `Off / By Name / By Type / By Amount`. | `KEEP_AS_IS` | Preserve. |
| 2 — Game Difficulty | `Vanilla / Easy / Normal / Hard / Expert`; accepted fresh default is Vanilla. | `KEEP_AS_IS` | Preserve. Difficulty remains a separate axis from Trainer Level Scaling and Trainer AI. |
| 3 — Trainer Level Scaling | `Auto / Off / Easy / Normal / Hard / Expert`; fresh default is Off. Raw 0 / `Auto` resolves through Game Difficulty (Easy→Easy, Hard→Hard, Expert→Expert, Vanilla/Normal→Normal). | `POLISH_REQUIRED` | Clarify that `Auto` follows Game Difficulty. Keep raw 0, all explicit values, and behavior unchanged. |
| 3 — Trainer AI | `Auto / Vanilla / Easy / Normal / Hard / Expert / Smart / Standard / Ironmon Smart`; fresh default is Standard. Raw 0 / `Auto` follows the legacy Difficulty mapping. | `POLISH_REQUIRED` | Relabel the six legacy explicit AI choices as `Legacy Vanilla`, `Legacy Easy`, `Legacy Normal`, `Legacy Hard`, `Legacy Expert`, and `Legacy Smart` if GBA text-width review permits. Keep `Standard` and `Ironmon Smart`; preserve all stored values and mappings. Clarify `Auto` as Difficulty-derived. |
| 3 — Hard Cap | `Auto / Off / On`. | `KEEP_AS_IS` | Preserve current behavior and raw values. No evidence supports a change. |
| 3 — Nuzlocke | `Off / On`. | `KEEP_AS_IS` | Preserve as an explicit rules choice. |
| 3 — Wild Prebattle | `Off / On`. | `KEEP_AS_IS` | Preserve as an explicit encounter-presentation choice. |

The strongest UX issue is visual reuse of difficulty words in the Trainer AI list, which makes three independently stored settings look coupled. The source confirms that only `Auto` intentionally inherits the legacy Difficulty mapping; explicit AI and scaling choices remain separate. This is a text/help polish, not a settings redesign. Do not change defaults, raw values, or mappings.

The `L=A` note is a control-mode tradeoff, not a proposal to alter Auto-Run. Normal running from Fresh New Game remains available independently; a player choosing L=A gives up L’s other function by the same remapping that makes L act as A.

## Current NatDex and Faster FireRed deltas

Current NatDex documentation is refreshed from its current public QoL page, and implementation claims below use the current FireRed source linked by v1.2.1. The older `16b8b9…` NatDex source is historical/supporting only for this comparison. In particular, the current source shows the original Two Island Move Maniac still present, so the Celadon service is duplicate early access even though some docs describe the NPC as “moved.”

| Candidate | Current evidence and target | Classification |
|---|---|---|
| Celadon Move Reminder access | Current NatDex source adds a Celadon City house NPC that invokes the existing Two Island Move Maniac script; the Two Island NPC remains, and the service still costs one Big Mushroom or two Tiny Mushrooms. CFRU has no corresponding Celadon overlay. Add only the early duplicate access and retain the original service and price. | `PROMOTE_TO_REQUIRED_QOL` |
| Route 10 HM05 convenience | Current NatDex source adds a one-time Hiker at Route 10 `(17,22)` hidden by `FLAG_GOT_HM05`; he gives HM05 and explains Flash. The Route 2 Aide remains. CFRU has no Route 10 equivalent. Add a one-time Route 10 path while retaining Route 2 access and all current HM use gates. | `PROMOTE_TO_REQUIRED_QOL` |
| National Dex from Fresh New Game | NatDex calls its RSE National Dex enable routine during New Game setup. This is earlier than the target for this project. | `INTENTIONAL_DIFFERENCE` |
| National Dex at the normal Pokédex handoff | Faster FireRed 1.3.2 documents granting the National Dex alongside the normal Pokédex. Current M-007 grants the normal Dex after Parcel but deliberately defers National Dex. The project target is to enable National Dex at that existing handoff, not at Fresh New Game. Use FireRed’s full `EnableNationalPokedex()` operation, which writes National-Dex save metadata, its var, and flag; setting only a flag is insufficient. | `POLISH_REQUIRED` |
| Exact current BPRE call binding for National Dex | The public pret source proves what `EnableNationalPokedex()` writes. The exact native/special binding available to the current CFRU-backed M-007 script has not been established in this audit and must be proven before implementation. | `UNKNOWN_NEEDS_SOURCE_PROOF` |
| Pickup activation sound | Documented by current NatDex, with no product requirement or source-backed defect in the integrated profile. | `OPTIONAL_QOL` |
| Bag capacity | NatDex documentation reports capacity increasing from 42 to 120. Current CFRU defines `BAG_ITEMS_COUNT` as 42 and has separate counts for other pockets. No finish-blocking capacity failure was established; do not treat unlike pocket totals as a proven total-bag comparison. | `OPTIONAL_QOL` |
| Hidden-item sparkle | Existing M-009 sparkle behavior is accepted and current NatDex FireRed source also uses sparkles. Keep the accepted current behavior. | `KEEP_AS_IS` |
| Optional sparkle toggle | The toggle remains a user-requested secondary option; it is not needed to retain the accepted sparkle behavior. | `OPTIONAL_QOL` |
| Global BGM Off | Present in NatDex documentation, but explicitly held by the current user decision. | `OPTIONAL_QOL` |
| Faster Battle Engine | Present in NatDex documentation, but explicitly held. No broad battle-engine refactor is proposed. | `OPTIONAL_QOL` |
| Faster Fishing | Present in NatDex documentation and explicitly secondary. | `OPTIONAL_QOL` |
| NatDex Start-menu HM system | NatDex’s modern mode exposes field HMs from Start and does not require a compatible party Pokémon before executing the action. This is intentionally different from the locked project HM model. | `INTENTIONAL_DIFFERENCE` |

NatDex public sources: [v1.2.1 release](https://github.com/CyanSMP64/NatDexExtension/releases/tag/v1.2.1), [QoL documentation](https://github.com/CyanSMP64/NatDexExtension/wiki/Quality-of-Life-features), [Celadon map](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/data/maps/CeladonCity_House2/map.json), [Two Island map](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/data/maps/TwoIsland_House/map.json), [Route 10 map](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/data/maps/Route10/map.json), [Move Maniac script](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/data/maps/TwoIsland_House/scripts.inc), and [New Game setup](https://github.com/CyanSMP64/pokefirered/blob/b84ca974fb33bd5ee69f1e3597d44e8f7d4e3fc7/src/new_game.c). The current integrated map overlay manifest is [CFRU `mapobjectoverlays`](https://github.com/Planton361/CFRU-expansion/blob/11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec/mapobjectoverlays); its existing entries include the accepted Lab, Parcel, and Pewter overlays but no matching Celadon or Route 10 access. CFRU configuration and source checks are in [`config.h`](https://github.com/Planton361/CFRU-expansion/blob/11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec/src/config.h), [`overworld.c`](https://github.com/Planton361/CFRU-expansion/blob/11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec/src/overworld.c), and [`global.h`](https://github.com/Planton361/CFRU-expansion/blob/11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec/include/global.h). FireRed’s metadata-writing routine is in [pret `event_data.c`](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/src/event_data.c).

### Faster FireRed 1.3.2 comparison

| Documented reference feature | Current project disposition | Classification |
|---|---|---|
| Mom start / shortened opening | M-006 already shortens the start while preserving the project’s chosen setup. | `KEEP_AS_IS` |
| Shortened Parcel | M-007 already implements the accepted faster Parcel flow. | `KEEP_AS_IS` |
| Repel reuse | Already integrated. | `KEEP_AS_IS` |
| Gold TMs | M-001’s item-ball reward behavior is already accepted. | `KEEP_AS_IS` |
| Name Raters in Centers | Current 19-Center rollout is accepted. | `KEEP_AS_IS` |
| Instant Center healing | M-003 is already integrated. | `KEEP_AS_IS` |
| Guaranteed renewable step items | M-004 is already integrated; retain the current deterministic project contract. | `KEEP_AS_IS` |
| Lab PC item | M-005 already covers the empty initial PC item. | `KEEP_AS_IS` |
| Optional Bill / Sevii handoff | M-008 already makes the Bill/Sevii path optional. | `KEEP_AS_IS` |
| Hidden-item marking | The project retains the accepted M-009 sparkle presentation rather than importing a second marking system. | `INTENTIONAL_DIFFERENCE` |
| Viridian Forest Nurse | M-002 is already integrated. | `KEEP_AS_IS` |
| National Dex timing | Grant at normal Pokédex handoff; see the NatDex table. | `POLISH_REQUIRED` |
| Friendship Boost | Explicitly held; do not change catch/growth-related values in this finish pass. | `OPTIONAL_QOL` |
| Item/TM RNG compatibility notes | Relevant to the later UPR-FVX/randomizer alignment, not this ROM-side QoL audit. | `OUT_OF_PILOT` |

The public Faster FireRed README also documents one-time friendship boosting and other patch behavior. No opaque IPS/BPS was inspected. Its [1.3.2 release notes](https://github.com/DrMaple/Faster-FireRed/releases/tag/1.3.2) state National Dex is granted at the same time as the normal Pokédex; this supports the handoff target above.

## IronMON Patch Editor / run-speed reference

| Candidate | Source-backed comparison | Classification |
|---|---|---|
| Full Professor speech skip | Patch Editor 1.2 offers full speech skipping but requires predefined gender and player name (and, for FireRed, rival name). The pilot retains normal player naming and uses its existing shortened intro as a deliberate middle ground. | `INTENTIONAL_DIFFERENCE` |
| Instant Center healing | Already provided by M-003 and CFRU. | `KEEP_AS_IS` |
| Step-item policy | Patch Editor exposes Always or Random policy. M-004’s current guaranteed renewable project behavior is accepted; do not replace it with a random policy. | `KEEP_AS_IS` |

Reference: [IronMON Patch Editor 1.2](https://github.com/DrMaple/IronMONPatchEditor/releases/tag/1.2).

## Targeted mandatory-flow and text matrix

The story and state transitions below remain; the audit focuses on interaction delays and repeated-run friction. These scenes are generally one-time per save, but Fresh New Game restarts make their delays recur across Ironmon attempts. No source-backed evidence justified a blanket text rewrite.

| Flow | Text / delay type | Current state and audit disposition | Classification |
|---|---|---|---|
| Oak intro, gender and naming | One-time setup; naming is state-bearing, speech is partly tutorial/exposition. | M-006 shortens the entry flow while retaining ordinary name choice. Full fixed-name/gender skip stays a deliberate Patch Editor difference. | `KEEP_AS_IS` |
| Mom handoff | One-time setup and story state. | Existing faster Mom start is accepted; preserve handoff state. | `KEEP_AS_IS` |
| Lab, starter and Rival | Choice, battle, and story-state transitions; some tutorial text. | Preserve starter choice, rival encounter, and state transitions. No bounded source-backed additional delay was shown to justify a change. | `KEEP_AS_IS` |
| Parcel / Pokédex / Poké Balls | Reward and progression state, plus tutorial text. | M-007 shortening and existing balls handoff stay. National Dex timing at the normal Pokédex event is the separate required polish above. | `POLISH_REQUIRED` |
| Viridian Old Man | Repeated-route movement and tutorial delay. | Accepted bypass is already in M-007. | `KEEP_AS_IS` |
| Pewter post-Brock / Running Shoes Aide | Reward acknowledgement, tutorial, flavor, Mom-letter exposition, and approach/exit movement. | Running is already enabled from Fresh New Game; Auto-Run remains separate; the post-Brock gate is the accepted short, non-gating cleanup. Do not reopen. | `KEEP_AS_IS` |
| Gym reward / TM tutorial text | One-time reward/tutorial blocks; some dialogue is explanatory or flavor. | Further generic shortening remains secondary. No specific block from source review is a finish blocker. | `OPTIONAL_QOL` |
| Pokémon Center healing | High-frequency repeated action. | Instant heal is already integrated by M-003. | `KEEP_AS_IS` |
| Bill / Sevii handoff | Optional story and movement. | The accepted optional Bill handoff remains in M-008. | `KEEP_AS_IS` |
| Other mandatory tutorial/exposition | Tutorial and flavor; varies by event. | No additional bounded high-impact repeated delay was proven in this source pass; keep any later work targeted and secondary. | `OPTIONAL_QOL` |

### Running Shoes Aide alternatives

The decision is already locked by the current Workspace profile and #538/#539 evidence.

| Model | Disposition | Classification |
|---|---|---|
| Keep normal Running Shoes gate and only shorten the Aide handoff | Not selected: running is already enabled from Fresh New Game. | `INTENTIONAL_DIFFERENCE` |
| Grant Running Shoes automatically on Brock’s reward | Not selected: it would replace the accepted early-run flag model and make a second state change. | `INTENTIONAL_DIFFERENCE` |
| Enable normal running on Fresh New Game; retain separate Auto-Run and movement restrictions; use the accepted short non-gating post-Brock cleanup | Current integrated behavior. `FLAG_RUNNING_ENABLED` uses existing CFRU semantics; Auto-Run has its own flag. | `KEEP_AS_IS` |

The source check for [CFRU running settings](https://github.com/Planton361/CFRU-expansion/blob/11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec/src/settings.c), the [movement gate](https://github.com/Planton361/CFRU-expansion/blob/11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec/src/overworld.c), and the [current integration evidence](../testing/cfru-early-running-workspace-integration-2026-09-28.md) supports this disposition. The existing flag is set for Fresh New Game; no save-load path or movement restriction is being proposed for change.

## HM model

| Candidate | Current contract | Classification |
|---|---|---|
| CFRU/DPE HM use model | HM item required; badge and location requirements remain; at least one non-egg party Pokémon must know the move or be compatible with the HM; the compatible Pokémon need not have the move in its moveset. No NatDex Start-menu HM system is used. | `KEEP_AS_IS` |
| NatDex modern HM menu / remove compatible-party requirement | A different product model; NatDex’s Start-menu path checks item, badge, and field/location state without the CFRU compatible-party gate. No clear benefit justifies changing this user-locked challenge rule. | `INTENTIONAL_DIFFERENCE` |

CFRU’s `ONLY_CHECK_ITEM_FOR_HM_USAGE` comment and `PartyHasMonWithFieldMovePotential()` prove the current item-plus-compatible-party behavior; field paths retain their badge and location checks. DPE provides compatibility data used by the check; it does not own the HM UI. The implementation references are the pinned [CFRU config](https://github.com/Planton361/CFRU-expansion/blob/11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec/src/config.h) and [overworld checks](https://github.com/Planton361/CFRU-expansion/blob/11bd0bdeb9e06e9f3b868856b7742d913a7ad7ec/src/overworld.c).

## Consolidated classifications

### `KEEP_AS_IS`

- M-001 gold TM/HM Item Balls; M-002 Viridian Forest Nurse; M-003 instant Center healing; M-004 guaranteed renewable step items; M-005 Lab Potion / empty initial PC item; M-006 Mom / faster New Game handoff; M-007 shortened Parcel / Old Man bypass; M-008 optional Bill / Sevii handoff; M-009 hidden-item sparkle; M-013 Premier Ball behavior.
- 19-Center Name Rater rollout; Repel reuse; running indoors; Early Running; separate Auto-Run; current movement restrictions; reusable TMs; forgettable HMs; item acquire picture/description; party Move Items; Select-from-PC; current HM model; auto-lowercase naming; accepted Standard / Ironmon Smart AI and Difficulty/scaling separation.
- Options-page settings retained in the settings matrix, except the specific label/help rows classified `POLISH_REQUIRED`.
- Existing instant Center healing and step-item policy in the Patch Editor comparison.

### `PROMOTE_TO_REQUIRED_QOL`

- Early duplicate Move Reminder access in Celadon, retaining Two Island and mushroom cost.
- One-time Route 10 HM05 convenience NPC, retaining Route 2 and all HM use rules.

### `POLISH_REQUIRED`

- Grant National Dex at the existing normal Pokédex handoff, using the real metadata-writing enable operation.
- Clarify Trainer Level Scaling and Trainer AI `Auto` semantics; prefix the six legacy AI choices if text fit is proven, preserving raw/save behavior.
- Parcel/Pokédex flow row is covered by the National Dex handoff candidate, not a separate dialogue rewrite.

### `OPTIONAL_QOL`

- Portable PC easier/default availability; Friendship Boost; Faster Battle Engine; global BGM Off.
- Pickup activation sound; Faster Fishing; optional Hidden-Item sparkle toggle; larger bag capacity.
- Further generic tutorial-text shortening and additional unproven mandatory exposition reduction.

### `INTENTIONAL_DIFFERENCE`

- NatDex Start-menu HM system and no-compatible-party model; NatDex Fresh-New-Game National Dex timing; Faster FireRed hidden-item marking versus the accepted M-009 sparkle presentation; Patch Editor full Professor skip that fixes identity inputs; the unselected Running Shoes gate and Brock-grant alternatives.

### `OUT_OF_PILOT`

- Item/TM RNG compatibility preparation for later UPR-FVX/randomizer alignment; Hospitality / M-011; Commander; Embody Aspect; missing Gen-9 mechanics; new Terastal/form-transition systems solely for parity; broad battle-engine refactor; upstream-contribution preparation. `UPSTREAM_CONTRIBUTION` remains deferred.

### `UNKNOWN_NEEDS_SOURCE_PROOF`

- Exact current BPRE native/special call binding for `EnableNationalPokedex()` from the M-007 handoff. The behavior target is clear, but the callable binding must be established before any code change.

## Recommended follow-up order

No follow-up Issue is created by this analysis-only task. After the user accepts the targets, create one bounded implementation Issue per coherent change family:

1. **Settings wording only — CFRU owner.** Clarify `Auto` help and legacy Trainer AI names. Keep all raw values, original-raw dirty/save compatibility, mappings, and defaults. Verify GBA text width before settling final strings.
2. **National Dex at Parcel handoff — Workspace/CFRU integration owner.** Prove the exact current BPRE call binding first, then invoke the full FireRed enable operation at the existing normal Pokédex handoff. Do not enable it on Fresh New Game. Preserve the current shortened Parcel, Pokédex, and Poké Ball flow.
3. **Celadon Move Reminder — Workspace/CFRU map integration owner.** Add the source-backed duplicate NPC, keep Two Island, and preserve the mushroom menu/payment script.
4. **Route 10 HM05 convenience — Workspace/CFRU map integration owner.** Add the one-time NPC immediately before Rock Tunnel with the existing HM05 obtained flag; retain Route 2 and current badge/location/party compatibility requirements.

Keep these as separate bounded changes so each has its own source evidence and review. Randomizer alignment, emulator/runtime acceptance, and the #498 umbrella remain downstream contracts.

## Work performed and limits

This deliverable is analysis only. No gameplay/source code, component Gitlink, issue, or project metadata was changed. No ROM, save, emulator state, build artifact, tool binary, IPS, or BPS was read. No build, runtime session, or test suite was run. The report makes source-backed findings and follow-up recommendations; it does not claim runtime acceptance.
