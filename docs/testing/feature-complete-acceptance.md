# Feature-complete manual acceptance package

Prepared 2026-09-15; **all cases NOT_RUN in this session**. Documentation only.
This is a user-run package, not permission for an agent to open an emulator,
ROM, save, state or generated build. Share sanitized text results only.

## Release identity, prerequisites and execution policy

Record the exact workspace/CFRU/DPE/UPR source SHAs, candidate PRs, source config
changes, randomizer version/settings/seed label, emulator name/version/core,
and a user-chosen non-sensitive run label. Do not supply artifact hashes, paths,
memory dumps, screenshots, tool binaries, settings files containing paths,
ROMs, saves, states, tokens or keys. Source Git SHAs are permitted identifiers.

Baseline workspace: `7437cd551545ab5e4dcd57a2ff5dbf9672193d74`; CFRU
`827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec`; DPE
`22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`; UPR
`1a597a667129b50284dd88afb231372b5bd01d7f`. New candidates are CFRU
[#45](https://github.com/Planton361/CFRU-expansion/pull/45) / stacked
[#46](https://github.com/Planton361/CFRU-expansion/pull/46), and UPR
[#185](https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/185).
Do not call a candidate or integration PASS based on another revision's result.

Before runtime acceptance, complete the clean/full source builds and affected
module tests. This session's CFRU builds stopped at missing audio tools; UPR's
full module build/JUnit could not run (Gradle absent; Java 23 vs required 25).
No final runtime result is implied by static/host tests or past milestone PASS.

Run order: A → early B/C → D with B/C repeated at checkpoints → E/F when
reachable → G → H. Use a genuine Fresh New Game on the final integrated
revision, not an earlier-candidate save, for the main path. The user may keep
private recovery points for destructive-risk isolation; never upload them.
Reach branches through normal gameplay. If a boundary needs inaccessible items,
forms or quantities, record BLOCKED and a prerequisite; do not force memory,
invent a fixture result, or expand engine scope. In particular, 999-ball and
rare-form cases may need a separately approved user-owned test setup.

For every case record PASS / FAIL / BLOCKED / NOT_RUN / N/A with reason.
PASS requires all stated results, return of input control, no unrelated state
mutation, and no new visual/script corruption. A family cannot pass by sampling
one row unless that row explicitly specifies representatives. N/A requires a
source-backed profile exclusion and reviewer acceptance; it is not a skipped
mandatory gate. No cheats or tracker extensions in the control run.

## Severity and STOP rules

| Severity | Definition | Response |
|---|---|---|
| S0 critical | Save corruption/loss, persistent invalid data, destructive write | Stop that run immediately; avoid overwriting the last known-good private save; report sanitized reproduction. |
| S1 high | Crash/hang, progression softlock, wrong active writer/table, duplicate key reward, invalid species/move, unrecoverable control loss | Stop affected run/path; do not use its downstream results as acceptance. Independent clean tests may continue. |
| S2 medium | Reproducible functional mismatch with safe workaround, incorrect reward amount, missing expected UI/learn prompt | Fail affected case and log a defect; continue only if independent state remains trustworthy. |
| S3 low | Cosmetic/text-only issue without gameplay/data effect | Log and continue; acceptance needs explicit disposition, not silent waiver. |

Global STOP: source revision/settings mismatch, unknown profile, requirement to
access a protected artifact through the agent, unexpected write/invalid ID,
resource leak accumulating across transitions, or loss of reproducibility.
For a runtime hang, record the last action and approximate duration; do not
guess its engine cause. A failed capacity test must not be repeated against
valuable progress. ROM freeze requires zero unresolved S0/S1 and explicit
disposition of every S2/S3. Stop only the affected test; continue independent work.

## A. Fresh New Game and early-game state

For alternate trigger approaches, start an independent fresh run or a private
user-maintained pre-event checkpoint from this exact revision. The main run
must still complete the entire flow once without restoring an older checkpoint.

| ID | Procedure / variants | PASS criteria |
|---|---|---|
| A01 | Start New Game, naming and intro | No controls-guide detour; naming/Oak introduction completes; mixed-case name entry works; correct room/input/camera. |
| A02 | Open Player PC before Mom | No initial Potion in item storage; no phantom occupied slot. |
| A03 | Attempt house exit before talking to Mom; repeat | Mandatory exit guard prevents departure, gives coherent response, releases input; cannot bypass by repeated direction/menu. |
| A04 | Talk to Mom | Handoff occurs once; fast Lab scene reaches direct starter selection, Oak at (6,3) facing down; correct camera/player placement. |
| A05 | Each of the three starter choices on separate starts | Chosen species matches display and party; Rival chooses intended counterpart; no old starter species/script mismatch. |
| A06 | Complete Rival battle, win and separate loss branch | Battle returns to correct Lab state; exit/warps/input work; no replayed starter or accidental second starter. |
| A07 | Obtain Lab Potion before/after battle as accessible; attempt duplicate | Normal one-time Item Ball, correct item+quantity; disappears and stays gone after re-entry/reload. |
| A08 | Return to Mom with damage after Rival | Post-rival healing restores expected party HP/status; no repeat starter warp. |
| A09 | Check Pallet before Parcel; talk to original Route 1 Potion Clerk | Temporary parcel Oak absent; original Potion Clerk reward/dialogue remains independent and one-time. |
| A10 | Approach temporary Route 1 Parcel Clerk from each of its four scripted trigger tiles | Each approach awards Parcel once, removes temporary Clerk, retains input/Route 1 travel; item/name/flags coherent. |
| A11 | Re-enter/reload after Parcel acquisition but before delivery; visit Viridian Mart | Parcel retained exactly once; temporary Clerk stays absent; Mart cannot give another Parcel. |
| A12 | Return to Pallet through each of outdoor Oak's two scripted trigger tiles | Parcel removed; Pokédex/unlock state and exactly five Poké Balls awarded once; Oak disappears; no accidental early National Dex policy change. |
| A13 | Revisit/reload Pallet, Lab and Mart after delivery | No duplicate Dex/balls, no vanilla Lab parcel replay, normal Mart purchasing, no stranded temporary objects. |
| A14 | Walk past Old Man; interact if available | No roadblock/forced catching tutorial; normal control and northward progression. |
| A15 | Talk to Daisy after parcel, acquire/use Town Map; repeat | Map granted through intended dialogue once and works; no blocked post-parcel state. |
| A16 | Route 22 early Rival/League approach before and after relevant story state | Intended optional Rival encounter/state and badge gate; no premature progression or stale parcel block. |
| A17 | Save/reload after starter, after Parcel, after Dex (three milestones) | Correct party, key items, five-ball accounting and persistent one-time event flags at each point. |

## B. General QoL and item semantics

| ID | Procedure / variants | PASS criteria |
|---|---|---|
| B01 | After running is enabled, hold B indoors in house/Center/large interior | Indoor running works on legal tiles; collisions, restricted terrain and doors remain correct. |
| B02 | L auto-run on/off, B inversion; repeat after menu/warp/reload | L toggles only when available, B walks in auto-run, normal controls restored on toggle; configured persistence recorded. |
| B03 | Test L=A option vs normal L mapping | Document known conflict; no stuck buttons or unintended service selection; return to standard mapping for acceptance. |
| B04 | Exhaust Repel/Super/Max (100/200/250 steps), choose Yes/No, no remaining stock | Correct expiry/reuse prompt, exact one-item consumption on Yes, none on No; no negative count or loop when empty. |
| B05 | Teach same TM to two compatible Pokemon, including four-move replacement; cancel once | Reusable TM remains; selected move taught/replaced only on success; canceled/incompatible teaching changes nothing. |
| B06 | Overwrite an HM move via normal learning | Forgettable HM behavior works; no unintended forced permanence or lost unrelated move. |
| B07 | Cut/Surf/Strength/Flash convenience without move learned | Requires corresponding item, compatible party member, badge and valid location. Flash uses target TM70 mapping; no false assumption of NatDex's larger HM menu. |
| B08 | B07 negative variants: no item / no compatible member / no badge / wrong location | Each missing prerequisite blocks use safely; compatible member restored permits expected action. |
| B09 | Script-aware Select from PC at a service that explicitly exposes it; cancel/select/full-party variants | Correct boxed target/party identity and data preserved; no forced deposit/lost Pokemon. If no installed service exposes it, record capability-only N/A with source reason, not universal UI failure. |
| B10 | Party Move Items: transfer to empty holder, swap two items, cancel | Exact items transfer/swap once; Bag quantities unchanged; held icons and summaries agree. |
| B11 | Move Items self/egg/invalid target; mail if supported | Invalid targets safely reject; no item duplication/loss. Mail-only unavailable path may be N/A with reason. |
| B12 | Obtain new item then repeat same item, visible/hidden/shop/gift paths | Correct item icon/name/pocket and first-obtain description; input/effects release; subsequent acquisition doesn't corrupt or block. |
| B13 | Game Corner prize-room acquisition and subsequent menu/warp | Record existing presentation caveat; no crash/stuck sprite/control loss. Cosmetic deviation is logged, not presumed fixed. |
| B14 | Player PC item deposit/withdraw, no initial Potion, full/empty boundaries | Correct inventory counts and safe capacity refusal; Lab reward remains independent. |
| B15 | Pokemon PC deposit/withdraw/move/swap, box edge/last slot, summary | Identity/moves/ability/item/stat data preserved; no deleted/duplicated Pokemon or bad icons. |
| B16 | Every exposed Options page; change/revert text/button/music selections; Start menus before/after flags | Valid labels/cursors, intended availability, cancel/return correct; configuration persists as designed; no overlapping AI/difficulty flag side effects. |
| B17 | M-001 gold TM ball and HM07 ball, ordinary non-TM control | Gold graphic only approved targets; correct underlying reward, quantity and persistence; ordinary item graphic unchanged. |
| B18 | M-001 randomized field/TM variants (H12) | 28 TM slots and HM07 distinction retained; gold does not force a non-TM into TM pool or make HM07 randomizable. |
| B19 | Visible normal hidden item before/after pickup, stand directly on tile | Sparkle while eligible/in view; absent underfoot and after collection; actual A-button pickup unchanged. |
| B20 | Hidden item with full Bag, then space available | Safe failed pickup retains availability; later successful pickup gives correct item once, then marker removed. |
| B21 | Itemfinder near, far, underfoot and after collection | Native direction/underfoot behavior and availability correct; sparkle is not the pickup mechanism. |
| B22 | Forest Nurse (29,58): healthy/damaged party, Yes/No | Yes heals expected HP/PP/status; No changes nothing; normal interaction exits. |
| B23 | Forest Nurse with any poisoned member, including non-lead | Refuses coherently and does not silently heal/consume/alter party; after poison removed, Yes path works. |
| B24 | Instant heal in every one of the 19 ordinary Center targets during traversal | Short path heals HP/PP/status, returns control; no residual ball animation/palette; healing/stat bookkeeping preserved. Record each Center by name. |
| B25 | Trainer Tower healer control; accessible Union Room entry/cancel | Excluded Tower behavior preserved; ordinary Center bookkeeping doesn't break upstairs/Union Room flow. Do not require network partner; external link functionality may be N/A. |
| B26 | Center Name Rater: own Pokemon rename/cancel; egg and traded rejection | Correct target named, lowercase behavior and cancellation safe; egg/traded policy retained. Record each exposed Center NPC's accessibility; test rejection paths at least once. |
| B27 | Save/reload after item transfer, rename, options change and healing | All intended persistent data retained; no duplicate transient UI/effects or event replay. |

## C. M-009 global-frame regression pass

Repeat C01–C09 in early outdoors, dense Game Corner/interior, cave, and late
town/Sevii. Record per-location results. Legacy targeted sparkle PASS does not
cover these global lifecycle risks. Do not manufacture >36 events or new maps.

| ID | Procedure / variants | PASS criteria |
|---|---|---|
| C01 | Walk/run all directions, scroll near map edges/objects and visible hidden items | Camera follows without jitter; object/OAM positions, priorities, visibility and collisions stable. |
| C02 | Rapid repeated Bag/party/summary/PC/Start/options open/cancel while marker nearby | No marker over menus, stuck tasks, lost input or accumulation after repeated cycles. |
| C03 | Indoor/outdoor warp, stairs, cave ladders, map connections in all legal directions | Correct camera/object placement; old map effects disappear; new map markers correspond to new events. |
| C04 | Wild/trainer battle → field, flee/catch/win/loss variants | Correct postbattle callback/input/map; no stuck palette, invisible actor, residual battle sprite or stale marker. |
| C05 | Fade/flash transitions, healing, field moves and map palettes | Palette updates and fades complete; no tint leaks, flicker or mismatched sprites after returning. |
| C06 | Leave view/collect item while sparkle active; revisit/reload | Effects expire and are recreated only for eligible events; no ghost sparkles, growing sprite/task exhaustion or wrong-location effects. |
| C07 | Dense object/script locations and repeated travel cycles | No missing actors, broken script movement or resource-related slowdown; Game Corner existing maximum event map remains usable. |
| C08 | Mom/Lab/Parcel, Gym and rival cutscenes, Bill boat travel | Script locks release, scripted camera/pan and actor movement complete; no scene timing/overlap regression. |
| C09 | Quest Log record/replay after representative warp/battle/item/heal where practical | Playback/arrival behavior and exit correct; no re-awarded item or event-state mutation. If unavailable, BLOCKED with prerequisite rather than PASS. |
| C10 | Save/reload and fresh boot after dense transition session | No persistent corruption, stale effects or changed map/event state; unrelated progress intact. |

## D. Story progression through Hall of Fame

Use one continuous main run; optional ordering is allowed but record the actual
order. At every badge/chapter: verify reward once, map exits/return, relevant HM
gate, Center/PC and save/reload; perform C02/C03/C04. Battle balance is not a
Gen9 mechanics acceptance claim. An unfair random seed is separate from an
engine softlock; keep a non-randomized progression control.

| ID | Chapter | PASS criteria |
|---|---|---|
| D01 | Pewter / Brock | Gym battle/reward/badge, exit and onward Route 3 gate work once. |
| D02 | Mt. Moon / Cerulean / Misty | Fossil sequence, route transitions, Rival and Gym reward/state work. |
| D03 | Nugget Bridge / Bill's house / ticket | Required NPC/script chain and ticket complete; Cerulean exit and travel not softlocked. |
| D04 | Vermilion / SS Anne / Cut | Boarding, Rival, Captain/HM01, ship departure and return flow correct; Cut opens intended paths with constraints. |
| D05 | Lt. Surge / Diglett route / Flash access | Gym puzzle/badge, return travel and Flash item/convenience coherent; no badge gate bypass. |
| D06 | Route 9 / Rock Tunnel / Lavender | Cave connections/light/escape and town arrival function; Tower initially respects story gates. |
| D07 | Celadon / Erika / Rocket Game Corner | Gym reward, hideout switches/lift key/Giovanni/Silph Scope all work; dense objects and hidden items stable. |
| D08 | Pokemon Tower / Mr. Fuji / Poke Flute | Scope-gated ghost sequence, rescue and Flute grant once; both Snorlax paths wake/resolve appropriately. |
| D09 | Fuchsia / Koga / Safari Surf and Warden Strength | Safari admission/timeout/exit, Surf/teeth/Strength chain and badge work; required items not randomized away. |
| D10 | Saffron access / Silph / Sabrina | Entry gate, teleporters/Card Key/Rival/boss/Lapras-reward/President and Gym all progress; no linked static/script mismatch. |
| D11 | Surf routes / Seafoam / Cinnabar Mansion | Surf transitions, boulder puzzle and optional static interaction safe; Secret Key permits Gym. |
| D12 | Blaine / optional Bill | Badge works; no forced Sevii trip on Gym exit; F tests complete independently. |
| D13 | Viridian Gym / Giovanni | Final Gym unlock, puzzle, reward and departure flags correct. |
| D14 | Route 22 final Rival / badge checks / Victory Road | Correct later Rival team/state, all badge gates and Strength puzzle work; League reachable. |
| D15 | Elite Four / Champion | All four rooms, inter-battle healing/menus, Champion and defeat/retry where safely testable function; no invalid trainer/custom move row. |
| D16 | Hall of Fame / credits / postgame return | Correct party recorded, credits exit, save/reload and Pallet return work; no progress or party corruption. |

## E. M-004 renewable representatives

Source contract: 1,500-step counter checked on entry to an eligible map. Renewal
selects a populated tier, not necessarily the same tile or every item. Before a
cycle, collect the group's available items; count steps manually in a repeatable
route and re-enter. Record the count method and picked slot/item names. No
memory-counter manipulation is needed or authorized. Boundary precision that
cannot be established by normal gameplay is BLOCKED, not guessed.

| ID | Procedure | PASS criteria |
|---|---|---|
| E01 | North–South Underground Path, below-cycle revisit then ≥1,500 steps and re-entry; repeat cycle | No unexplained early reset; every completed cycle has a nonempty eligible tier; items may vary, not guaranteed all slots. |
| E02 | East–West Underground Path, completed cycle | Same guaranteed group behavior; no wrong-path flag cross-contamination. |
| E03 | One Island Treasure Beach and Three Island Berry Forest completed cycles | At least one approved renewable tier active each; normal pickup/Itemfinder/sparkle and repeated cycle work. |
| E04 | Later representative Seven Island Tanoby Ruins (rare-only group) | Completed cycle cannot choose an empty tier; normal hidden item works. If unreachable, BLOCKED until postgame access. |
| E05 | Mt. Moon B1F control over several cycles | Remains random/non-guaranteed. A nonempty sample is not evidence of a regression; no claim that finite samples prove randomness. |
| E06 | Ordinary one-time hidden item outside group, collect then cycle | Does not respawn; renewable reset cannot globally clear normal collection flags. |
| E07 | Randomized eligible slot through repeated cycles | Regeneration restores the slot's randomized reward, never hardcoded vanilla item; quantity, sprite/text, Itemfinder correct. |

Other approved groups for additional coverage: Bond Bridge, Four Island,
Memorial Pillar, Resort Gorgeous, Outcast Island, Green Path, Seven Island
Trainer Tower exterior. Routes 20/21 and Mt. Moon are non-guaranteed controls.

## F. M-008 optional Bill / Sevii

| ID | Procedure | PASS criteria |
|---|---|---|
| F01 | Defeat Blaine, leave Gym, walk/re-enter town | No automatic outdoor Bill dialogue/prompt/forced boat travel; no outdoor Bill duplicate. |
| F02 | Visit Cinnabar Center | Bill is available interactively; instant Nurse and Name Rater still accessible and functional. |
| F03 | Bill NO, repeat, exit/re-enter and save/reload | Remains optional and available; no consumed invitation or blocked Kanto progression. |
| F04 | Continue to final Gym/League without accepting | Main story remains completable; optional trip is not mandatory. |
| F05 | Accept YES when ready | Original One Island departure/arrival and Celio sequence complete once, without duplicate Bill/boat actors. |
| F06 | Two/Three Island intended errands, return travel and later revisit | Original island progression, services and return-from-Sevii scene work; no broken return ticket/warp flags. |
| F07 | Save/reload after NO, after arrival, after return | Correct optional/completed state retained at each checkpoint; no replay or stranded player. |

## G. Gen1–9 display, crash and form sanity only

No new battle-mechanics acceptance is requested. Commander/Hospitality/Embody
Aspect and partial Palafin/Terapagos behavior remain documented baseline limits.
Do not interpret a displayed Gen9 name as implementation of its modern effect.

| ID | Procedure | PASS criteria |
|---|---|---|
| G01 | Safely accessible representative of each generation 1–9: encounter/party/summary/PC | Species name, sprite/icon, types, six stats and moves display without out-of-range IDs/crash; note internal species/form name. |
| G02 | Male/female and ordinary alternate/regional form representatives | Stable identity and correct source-owned presentation across party/PC/battle; no assumption all transitional forms are wild-eligible. |
| G03 | Normal ability slots 1/2 and hidden slot on supported representatives | Summary names match species-context assignment; save/reload preserves slot/identity; no generic alias mislabel. No new effect demanded. |
| G04 | Pikachu, Rotom, Necrozma, Zacian, Zamazenta restored data | Nonempty legal starting moves and expected later restored learning boundary; shared-form representative per family where safely reachable; exact source list controls expected result. |
| G05 | Late table bounds: safely supported Gen9 species including final entry Pecharunt; late move/item labels | Correct names/assets and safe navigation; no truncation into neighboring rows or null pointer crash. Unreachable forms remain BLOCKED/N/A by explicit profile. |
| G06 | Capture/rename/deposit/withdraw/save/reload a later-gen representative | Identity, held item, ability slot, moves and nickname retained; no vanilla encrypted-struct assumption in any active service. |

## H. Randomized output smoke

Use UPR candidate #185 or its user-integrated descendant and final CFRU/DPE
pins. First run an Unchanged control, then one family at a time, then a recorded
combined profile. Keep Pickup **Unchanged**, special wild disabled, unsupported
forms excluded, and Type Effectiveness Unchanged for the first full playthrough.
Do not promise generic ability-ban semantics for aliased IDs. All enabled rows
need output save/reload and actual runtime verification; a spoiler log is only
supporting evidence. The user performs private output operations; share text only.

| ID | Feature / operation | PASS criteria |
|---|---|---|
| H01 | Load exact pilot, Unchanged output, reload in UPR and boot fresh | Correct recognized table counts, no false unsupported detection, coherent unchanged data and A01–A06. |
| H02 | Random starters, all three choices, early/late Rival | Choice/display/party and actual Rival script/team synchronized; no old species reference. |
| H03 | Standard/Fallback wild; land/surf/old-good-super rod and repeated maps | Actual encounters match selected slots/levels; no invalid species/form or unintended special-wild claim. |
| H04 | Ordinary/custom trainer rows, Rival, Gym, E4 | Correct species, level, item, ability and four legal moves; no neighboring-row corruption. Record IV normalization/tera metadata caveat. |
| H05 | Level-up and trainer movesets; short/long/late species | UPR reload matches changes, learning at boundary works, no runaway END scan or overwritten neighbors. |
| H06 | Abilities: all three slots and safe alias representatives | Output/summary identity correct within CFRU semantics; hidden slot preserved; unsupported semantic ban options excluded or separately qualified. |
| H07 | TM moves and TM/HM compatibility; first/last TM and every HM boundary | 120 TMs + 8 HMs, changed TM labels/teaching coherent, HM moves unchanged, compatibility and field convenience agree. |
| H08 | Tutors: first/last slots, teaching and compatibility | 152-move/19-byte contract, taught move matches actual menu/selection. Stale scripted text is a logged caveat, not successful display parity. |
| H09 | Configured shops, normal/expanded inventory; buy ball/nonball | Actual offerings/prices/quantities coherent; no terminator overrun; run Premier matrix below on actual purchased ball pocket. |
| H10 | Enable Pickup Random once; then restore Unchanged | Candidate rejects with actionable message before output table mutation; no claimed successful Pickup log. With Unchanged, native level-based Pickup remains usable. |
| H11 | Trade and static representatives, linked gift/roamer/ghost where configured | Requested/given species, held items/names and actual encounter match; required story links remain valid; null unsupported slots preserved. |
| H12 | Field items: Unchanged, Shuffle, Random, Ban Bad, random TM field items, combined active profile | For each row inspect ordinary ball, gold TM, HM07 control, Lab Potion, hidden item and renewable slot. Item typing/pool rules and required progression items preserved; no HM07 rewrite. |
| H13 | Base Stats, Move Data, optional bounded Type Effectiveness | Source-width values survive output/reload and representative gameplay; category/type translation correct. Oversize chaos chart must safely reject, never truncate or overflow. |
| H14 | Logging and output error paths | Settings/run label and changed feature summaries consistent; no claim that Field Items have a full detailed log. Capacity/unsupported errors produce no usable partial-success result. |
| H15 | Combined supported settings output; reopen then A, selected B/C, early/mid/late battles | No option interaction, invalid writer pointer, corrupted form/name or game softlock. A complete randomized playthrough is still required for a broad support claim. |

### Premier bonus exact transaction matrix (M-013)

Run on ordinary and randomized shop inventories where the user can safely
obtain required stock/money. Count net purchases separately from rewards. All
ball-pocket types qualify, including Premier itself. Nonball policy is preserved.

| ID | Case | PASS criteria |
|---|---|---|
| P01 | 1, 9, 10, 19, 20, 21 of Poke/Great/Ultra plus another ball type | Premier bonus respectively 0,0,1,1,2,2; no Dusk/Luxury custom reward for Great/Ultra. |
| P02 | Separate 9+9 transactions, then 10+10 | First pair no reward; second pair one each. No cumulative remainder/carry. |
| P03 | 99, 255, 256, 999 quantity boundary where supported | floor(quantity/10) = 9,25,25,99; no u8 wrap; displayed count correct. |
| P04 | Buy Premier Balls themselves | Purchased count plus floor(quantity/10), subject to remaining capacity; purchase not confused with award. |
| P05 | Partial Premier stack capacity less than reward | Only remaining capacity awarded; coherent message/count, no loss/overflow. |
| P06 | Full ball pocket with existing Premier stack space vs no Premier capacity | Existing free stack capacity used; no room gives zero safely; ordinary purchase persists correctly. |
| P07 | Purchase uses last free slot/capacity | Bonus uses capacity after purchase, not stale pre-purchase capacity. |
| P08 | Cancel / insufficient funds / failed purchase / repeated A or B after success | No bonus on unsuccessful transaction; one award only per successful transaction; normal list return. |
| P09 | Nonball at each configured reward threshold and just below | Existing nonball reward table unchanged; no Premier award for nonball purchase. |
| P10 | Exit/re-enter shop and save/reload after reward | Correct money/inventory persists; no duplicate bonus/task on return. |

## Evidence and minimal sanitized report

Use [the report template](sanitized-acceptance-report.md). One row per case and
variant, with concise observed quantities/state and deviation. Include exact
source SHAs and settings text, not an attached private settings/output file.
For a defect include first failing case, initial state, minimal steps, expected
vs observed, frequency, severity and whether a clean unchanged control reproduces.
Do not infer a cause from a symptom or copy raw logs containing private paths.

Completion requires every mandatory row PASS on the final integrated candidate
or an explicitly approved scope exclusion, no unresolved STOP defect, and the
full D01–D16 continuous run. Past targeted evidence remains useful but cannot
replace the new A–H integration gates. Tracker integration is a later independent
profile gate and is not silently enabled during this control acceptance.
