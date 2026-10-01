# Final ROM UX Completeness — 2026-10-01

Workspace contract: [#589](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/589). Parent: [#498](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498).

Target: `FINAL_ROM_UX_COMPLETENESS_REVIEW_READY` — **analysis/decision ready**, not ROM profile acceptance. One writer; analysis only; exactly this report changes. CONTROL creates later implementation Issues after user review. No implementation or merge is authorized here.

## Result

**CONFIRMED USER DECISION:** unnecessary forced tutorials/dialogues must go; Oak/character setup is reopened. The earlier #537/#563 optional intro/dialogue disposition is superseded. Other retained product rules, especially HM eligibility and National Dex timing, are not silently overturned.

**CONFIRMED CURRENT STATE — source/static:** five independent required closures are identified: F01 Oak exposition, F02 the unnecessary starter flavor line, F03 forced Pewter Gym Guide escort, F04 Brock's false consumable-TM tutorial, F05 Captain's forced Cut tutorial. These are proposed product requirements under #589, not implementation acceptance. Identity skipping and other small QoL require explicit decisions enumerated below. Ordinary story/battle/reward/choice flows remain distinguishable from tutorials.

**CONFIRMED USER-SUPPLIED REVISION-BOUND RUNTIME PASS:** B Running, L Auto-Run, Auto-Run + B walking inversion, Save/Reload Running, Pewter Running-Shoes Scientist/Aide cleanup, and absence of Pallet Sign Lady forced interruption. #577 is complete. These are `REQUIRED_PRESENT`; the different pre-Brock Gym Guide is still present. No newly missing Running or Sign Lady feature is claimed.

Final R1 rebaseline and the continuous acceptance run must wait until this review is accepted, every decision is resolved, and every selected fix is integrated (or expressly reclassified by the user). `REQUIRED_PRESENT` means source/selected behavior exists; except for the named user-supplied checkpoints it does not claim a new final-pin runtime PASS.

## Exact basis and method

| Owner/reference | Revision |
|---|---|
| Workspace base | `3f9b46b606626775c42be7f21fde58bd7423c1d2` |
| Audit branch / target | `audit/589-final-rom-ux-completeness` / `main` |
| CFRU | `78478c728501fe8c70bd84e01e51c6334250a6f0` |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX | `7bf79ee1e7c46c972f7a9c84942970a950be0723` |
| NatDexExtension pinned baseline | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| Cyan FireRed NatDex pinned source | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| Faster FireRed README | `DrMaple/Faster-FireRed@db21d777083757067f242c62f592534f40bb2c77` |
| IronMON Patch Editor public 1.2 source | `63d3a45076192b7bdc9c2d6e0f4e031feeb99a02` |
| pret FireRed structural reference | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |
| Public Cyan `natdex`, observed 2026-10-01, comparison only | `7d2172d9f4911657cd80c91786b8af6e2388bd6c` |
| Public NatDexExtension `dev_new`, observed 2026-10-01, comparison only | `c5c3f1f25c7d8e9876c613988dd90d384a8b3d8a` |

Read AGENTS and all six canonical docs first, then #589 and #498 (including latest decision/runtime comments), then [M-012](../milestones/M-012.md), [#537 refresh](rom-qol-finish-refresh-2026-09-28.md), and [#563 scope](m014-r0-final-rom-scope-2026-09-29.md). Historical candidates supply inventory, never current implementation truth. Canonical older pin/status paragraphs are historical where the exact #589 contract supersedes them; no other document is edited here.

The original implementation checkout is stale and has a pre-existing dirty CFRU submodule. It was not reset, cleaned, stashed, switched, staged, or overwritten. A separate clean Workspace worktree was created at the exact base on the approved branch. Its component directories remain uninitialized. Exact component source was read using revision-qualified Git objects in the existing repositories; no dirty component working file was used. Public sources were read through GitHub source APIs/browser pages only. No patch asset was followed.

CFRU is an overlay/hook integration into BPRE, not a full FireRed decompilation. In the matrices, **C** is exact current CFRU source and **P** is pinned pret structural source. P supplies original task/script/flag ownership; C's `eventscripts`, `mapobjectoverlays`, `hooks`, `functionrewrites`, and `bytereplacement` determine which owners are replaced. Symbol names are source proof, not a claim that every future BPRE hook address is already bound. Future implementation must fail closed on exact target identities before repointing. No binary inspection is needed or permitted to establish this review.

Source register (all C/N/P links below use the exact revisions above):

- C integration: [eventscripts](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/eventscripts), [mapobjectoverlays](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/mapobjectoverlays), [hooks](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/hooks), [functionrewrites](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/functionrewrites), [bytereplacement](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/bytereplacement).
- C flow: [talk_to_mom](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/assembly/overworld_scripts/talk_to_mom.s), [shortened_oak_parcel_flow](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/assembly/overworld_scripts/shortened_oak_parcel_flow.s), [optional_bill_sevii](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/assembly/overworld_scripts/optional_bill_sevii.s), [pewter_running_shoes_cleanup](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/assembly/overworld_scripts/pewter_running_shoes_cleanup.s).
- C UX: [config.h](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/config.h), [option_menu.c](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/option_menu.c), [start_menu.c](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/start_menu.c), [settings.c](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/settings.c), [overworld.c](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/overworld.c), [read_keys.c](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/read_keys.c), [text_printer.c](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/text_printer.c), [general_bs_commands.c](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/general_bs_commands.c), [hidden_item_sparkle.c](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/hidden_item_sparkle.c), [party_menu.c](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/party_menu.c), [item.c](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/src/item.c).
- P intro/state: [main_menu.c](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/src/main_menu.c), [oak_speech.c](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/src/oak_speech.c), [new_game.c](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/src/new_game.c), [overworld.c](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/src/overworld.c); C layout: [include/global.h](https://github.com/Planton361/CFRU-expansion/blob/78478c728501fe8c70bd84e01e51c6334250a6f0/include/global.h).

## A — Forced-dialogue/tutorial matrix

Every row has one final classification. “Required” below is about keeping the necessary state/choice, not requiring the original verbose text. A02–A06 concern the existing selectable setup; full fixed-identity replacement is a separate D01 decision. Forced means automatic when its trigger is crossed, even on an otherwise optional route. Optional services are not mandatory tutorials just because their scripts contain messages.

| ID / entry | Source owner; trigger / scene / flag / var | Forced / necessary state or choice / tutorial-only? | Current behavior and final classification |
|---|---|---|---|
| A01 Title → New Game | P `main_menu.c:474` → `StartNewGameScene`; `oak_speech.c:686,708` | Player selects New Game; initializes task/display/resources, not a tutorial. | Existing transition; retain initialization. `REQUIRED_PRESENT` |
| A02 Controls Guide | C `SKIP_INTRO_CONTROLS_GUIDE`; `bytereplacement:763–771`; P guide/Pikachu tasks | Vanilla forced instructions; no character choice/reward. | Guide path skipped; not a full speech skip. `REQUIRED_PRESENT` |
| A03 Oak Professor Speech | P `Task_OakSpeech_Init` → Welcome/ThisWorld/ReleaseNidoran/IStudy/TellMe; C only rewrites intro species | Forced exposition and timers; no identity value requires the exposition. | Present; F01 must bypass exposition while preserving setup/lifecycle. `REQUIRED_FIX` |
| A04 Gender Selection | P `Task_OakSpeech_AskPlayerGender/HandleGenderInput:1267–1324` | Forced genuine choice; writes SaveBlock2 `playerGender`; not tutorial-only. | Retained; remove only if D01 selects full fixed identity. `REQUIRED_PRESENT` |
| A05 Player Naming | P `Task_OakSpeech_DoNamingScreen:1440–1455`, `CB2_ReturnFromNamingScreen` | Genuine choice, player name buffer and confirmation/cancel/default machinery. | Retained; no invented default name. `REQUIRED_PRESENT` |
| A06 Rival Naming | Same tasks, `GetDefaultName`, SaveBlock1 `rivalName` | Genuine choice; name used by later trainer text; not tutorial-only. | Retained; full skip needs user-defined rival name. `REQUIRED_PRESENT` |
| A07 Player Room / Start | [PalletTown_PlayersHouse_2F](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/PalletTown_PlayersHouse_2F/scripts.inc); P `WarpToPlayersRoom/NewGameInitData` | First-warp scene 0→1, respawn; NES/PC/sign are player-initiated. | No compulsory room tutorial; empty initial PC owner retained. `REQUIRED_PRESENT` |
| A08 Mandatory Mom interaction | C `talk_to_mom.s:38–93`; house exit CoordEvent at Lab scene 0 | Mandatory exit blocker and player-initiated Mom; sets Oak/scene/music, warps to Lab; magic-trick text/motion is presentation. | Selected Faster FireRed start exists. Automatic Room→Lab/no-Mom replacement is D02, not inferred from already accepted Mom parity. `REQUIRED_PRESENT` |
| A09 Vanilla Oak grass interception | [PalletTown](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/PalletTown/scripts.inc) `OakTrigger`; C Mom sets `VAR_MAP_SCENE_PALLET_TOWN_OAK=1` | Vanilla coordinate trigger at scene 0; needed to prevent no-starter exit in vanilla. | Unreachable through normal selected opening; Mom owns equivalent safe handoff. `REQUIRED_PRESENT` |
| A10 Oak escort / walk into Lab | Same P grass scene / C Mom warp + `M006OaksLabOnWarp` | Vanilla forced walk; no additional choice. | Original escort bypassed; C six-tile player entrance remains. Further removal is D02. `REQUIRED_PRESENT` |
| A11 Lab entry exposition | C `EventScript_M006OaksLabChooseStarter`, Lab scene 1→2 | Forced minimal starter-selection prompt; positions/camera/music and scene are necessary. | Original multi-message Oak/Rival exposition and delays replaced; concise prompt retained. `REQUIRED_PRESENT` |
| A12a Starter selection — mechanical | [PalletTown_ProfessorOaksLab](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/PalletTown_ProfessorOaksLab/scripts.inc) `ConfirmStarterChoice/ChoseStarter:1082–1137` | Player-initiated Yes/No, mon picture, `givemon`, `VAR_STARTER_MON`, SYS_POKEMON, nickname choice. | Vanilla later starter owner retained; preserve choices and all three starter paths. `REQUIRED_PRESENT` |
| A12b Starter selection — pure flavor | Same P `ChoseStarter:1118`, `OakThisMonIsEnergetic` text | Forced after Yes; isolated flavor-only message before state/mon award. | Still present; F02 remove this message, retain reward/nickname/state. `REQUIRED_FIX` |
| A13 Rival starter selection | P Lab `RivalPicksStarter/RivalTakesStarter:1140–1178` | Automatic after player/nickname choice; removes correct ball and advances scene 3. Ceremony/text is story presentation. | Retained. Further ceremony/receive-fanfare/approach reduction is D03; no automatic battle or rival identity removal. `REQUIRED_PRESENT` |
| A14 Rival waiting dialogue | P Lab `ChooseStarterScene` waiting/no-fair messages; C replaces scene 1 | Forced pure exposition in vanilla. | Skipped by M-006; distinguish A13 later selection. `REQUIRED_PRESENT` |
| A15 Rival battle return / exit | P Lab `RivalBattle`, `EndRivalBattle`; C `TUTORIAL_BATTLES` disabled | Coordinate-triggered battle; HealPlayerParty, remove Rival, scene 4, BEAT_RIVAL flag necessary; exit taunt is ordinary story. | Battle/state retained; Oak battle coaching compiled out. Further exit-story shortening D03. `REQUIRED_PRESENT` |
| A16 Pallet Sign Lady / Trainer Tips | C `talk_to_mom.s` writes sign-lady scene `0x4070=1`; P Pallet SignLady triggers | Vanilla forced instructions depended on OPENED_START_MENU; no necessary reward. | Fixed by #586 and user PASS; optional signs may still be read. `REQUIRED_PRESENT` |
| A17 Route 1 original Potion Clerk | [Route1](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/Route1/scripts.inc) `MartClerk`; `FLAG_GOT_POTION_ON_ROUTE_1` | Player-initiated free Potion, room/failure/one-time flag; marketing text is optional. | Original clerk preserved by C append-only overlay; no forced Potion tutorial. `REQUIRED_PRESENT` |
| A18 Temporary Route 1 Parcel Clerk | C `shortened_oak_parcel_flow.s:38–83`; four coords (10…13,2), Mart scene `0x4057=0` | Forced on first Route 1 approach; awards Parcel, Mart scene 1, hides clerk, reveals outdoor Oak; concise handoff. | Accepted shorter parcel; unnecessary city/Lab round trip already eliminated. `REQUIRED_PRESENT` |
| A19 Viridian Mart Parcel path | [ViridianCity_Mart](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/ViridianCity_Mart/scripts.inc); C handoff sets Mart scene 1 before reward, then 2 | Vanilla entry-forced at scene 0, otherwise shop is player-initiated. | Original forced/duplicate parcel disabled by selected Route 1 handoff. `REQUIRED_PRESENT` |
| A20 Temporary outdoor Pallet Oak | C Parcel two coords (12/13,0), Lab scene `0x4055=5`, hide flag `0x152` | Forced on return; consumes Parcel and performs necessary Dex/reward/state changes. | Short existing handoff retained; long vanilla Lab Dex scene bypassed. `REQUIRED_PRESENT` |
| A21 Pokédex / five-ball handoff text | C `M007PalletOakHandoff:95–127` | Necessary SYS_POKEDEX, unlocked flags, special `0x16F`, five balls; concise reward acknowledgement, not old catching lecture. | Full National Dex at normal handoff; Old Man=2, Daisy/Route22=1, Teala=1, Lab=6. Preserve ordering and reward. `REQUIRED_PRESENT` |
| A22 Viridian Old Man / catching tutorial | [ViridianCity](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/ViridianCity/scripts.inc); C sets Old Man `0x4051=2` | Vanilla forced coord tutorial at scene 1; catching demo/Teachy TV unnecessary. | Bypassed; northern progression open; later NPC text optional. `REQUIRED_PRESENT` |
| A23 Daisy / Town Map | [PalletTown_RivalsHouse](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/PalletTown_RivalsHouse/scripts.inc); scene `0x4058=1` from handoff | Player-initiated item service, bag room and scene 2; map explanation optional on later talk. | Retained; no forced travel to Daisy or map tutorial. `REQUIRED_PRESENT` |
| A24 Route 22 early Rival | [Route22](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/Route22/scripts.inc) scene 1→2, starter-selected battle IDs | Forced if entering optional west-route coords; not required for Route 2; genuine trainer encounter/story. | Retained battle; no tutorial; do not remove encounter merely because automatic. `REQUIRED_PRESENT` |
| A25a Brock reward state | [PewterCity_Gym](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/PewterCity_Gym/scripts.inc) `DefeatedBrock/GiveTM39` | Player-initiated boss with compulsory return reward: badge, defeat, Gym trainers, Pewter scene 1, TM room/retry/once flag. | Retain badge/reward/acknowledgement and bag-full retry. `REQUIRED_PRESENT` |
| A25b Brock TM tutorial | Same `ExplainTM39:29`; P `text.inc:43–54` | Forced multi-page tutorial including false claim of one-use TMs; no state/reward in message. | Still vanilla; conflicts with C REUSABLE_TMS. F04 replace/remove tutorial, retain reward. `REQUIRED_FIX` |
| A26 Running-Shoes Scientist/Aide | C `pewter_running_shoes_cleanup.s`, exact Aide + scene-1 three coords overlays | Former forced running/letter tutorial; short state/NPC cleanup now. | Source present, user runtime PASS. This is not A30 Gym Guide. `REQUIRED_PRESENT` |
| A27 Other early tutorials / Rock Tunnel path | Individual A30–A39 entries below | Split actual triggers; no blanket “all dialogues optional” conclusion. | Coverage index, dispositions belong to individual entries. `REQUIRED_PRESENT` |
| A28 Bill / Sevii forced invitation | C `optional_bill_sevii.s`; Cinnabar OnFrame scene 1→2; Center Bill revealed | Former forced outdoor invitation; optional Yes/No travel retained. | No forced Blaine→Sevii invitation; M-008 present. `REQUIRED_PRESENT` |
| A29 Other high-friction mandatory scenes | Individual A40–A44 below; C/P trigger scan | Story, optional travel, tutorials classified separately. | No universal text deletion or bypass of story gates selected. `REQUIRED_PRESENT` |
| A30 Pewter Gym Guide escort | [PewterCity](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/PewterCity/scripts.inc) `GymGuideTriggerTop/Mid/Bottom`; map coords at scene 0, local Gym Guide hide flag | Forced east-exit walk back to gym, two messages; no reward/choice; Brock route gate still necessary. | No C replacement of these scene-0 coords. F03 remove escort/tutorial, keep badge gate with concise feedback and no early Route 3 bypass. `REQUIRED_FIX` |
| A31 Mt. Moon fossil gate | [MtMoon_B2F](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/MtMoon_B2F/scripts.inc) Miguel, fossil choice, scene/flags | Forced trainer then real fossil Yes/No/item choice; not tutorial-only. | Retain encounter and choices; optional fossil-regeneration follow-up text stays optional. `REQUIRED_PRESENT` |
| A32 Cerulean Rival / Fame Checker | [CeruleanCity](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/CeruleanCity/scripts.inc) Rival trigger; scene 0→1, GOT_FAME_CHECKER | Forced progression rival + item; named ExplainFameChecker text is mostly farewell/gossip flavor (P text lines 37–43). | Retain state/battle/reward; extra gift/return/exit flavor/movement reduction D04. It is not falsely labelled a pure mechanics tutorial. `REQUIRED_PRESENT` |
| A33 Nugget Bridge Rocket | [Route24](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/Route24/scripts.inc) RocketTrigger; scene 0→1, Nugget room check | Forced encounter with Nugget reward/retry and recruitment story; no real recruit option but trainer encounter is content. | Retain encounter/reward. No tutorial-only block proved. `REQUIRED_PRESENT` |
| A34 Bill Sea Cottage / S.S. Ticket | [Route25_SeaCottage](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/Route25_SeaCottage/scripts.inc) HELPED_BILL, GOT_SS_TICKET, PC teleporter | Player-initiated but progression required; helping Bill/PC/ticket state, animation; No returns to same help path. | Retain story and ticket; differs from A28 later Sevii invitation. Further story animation shortening D05. `REQUIRED_PRESENT` |
| A35 Misty reward | [CeruleanCity_Gym](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/CeruleanCity_Gym/scripts.inc) GiveTM03, BADGE02/GOT_TM03 | Compulsory badge/TM return after real boss; short move/badge description, not repeated how-to-use-TMs tutorial. | Retain state/reward; generic reward wording for randomized TMs is D06. `REQUIRED_PRESENT` |
| A36 S.S. Anne Rival | [SSAnne_2F_Corridor](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/SSAnne_2F_Corridor/scripts.inc) three Rival coords; scene 0→1 | Forced boss-route battle and story; not coaching/tutorial-only. | Retain; further approach/exit story trimming D03. `REQUIRED_PRESENT` |
| A37a Captain / HM01 state | [SSAnne_CaptainsOffice](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/SSAnne_CaptainsOffice/scripts.inc) Captain, GOT_HM01, Vermilion scene 1 | Player-initiated progression service; seasickness story, HM reward and departure state. | Retain reward/state/story and one-time flag. `REQUIRED_PRESENT` |
| A37b Captain Cut tutorial | Same `ExplainCut:19`; P text lines 28–32 | Forced extra field-use instruction after reward; no state in message. | Present; F05 remove extra tutorial while preserving GOT_HM01/scene/release. `REQUIRED_FIX` |
| A38 Surge / Rock Tunnel access | [VermilionCity_Gym](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/VermilionCity_Gym/scripts.inc) reward and switch puzzle; C Route10 HM05 NPC | Real boss/puzzle/choice; HM05 hiker player-initiated, shared GOT_HM05 room/retry/once flag. | Retain puzzle/badge/reward; Route10 convenience present. Hiker is player-initiated and keeps a one-line Flash hint; no automatic intercept. `REQUIRED_PRESENT` |
| A39 Optional services and advice before Rock Tunnel | P BikeShop, FanClub, Rod house, Route2/11 Aides, Museum, signs, gym advisers; Center `Teala` | Player-initiated services/advice; Teala first heal intro prevented by C handoff `0x407C=1`. Bike Voucher story is chosen service. | No compulsory service detour identified; M-003 instant heal covers ordinary Centers; advice remains readable by choice. `REQUIRED_PRESENT` |
| A40 Later gyms / Giovanni rewards | P Celadon/Fuchsia/Saffron/Cinnabar/Viridian Gym GiveTM scripts | Real battles/badges/retry/reward; move-specific prose may be stale in randomized outputs. | Retain content and acknowledgements; D06 governs a generic reward-text policy, not an unproven global tutorial port. `REQUIRED_PRESENT` |
| A41 Pokémon Tower / Fuji / Poké Flute | [PokemonTower_6F](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/PokemonTower_6F/scripts.inc), [PokemonTower_7F](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/maps/PokemonTower_7F/scripts.inc) / Lavender Volunteer House | Ghost encounter, Rocket battles, Fuji rescue and Flute reward/warp; stateful story, not generic tutorial. | Retained. No automated deletion of story/warp/reward states. `REQUIRED_PRESENT` |
| A42 Silph / Giovanni / guards / League | P SilphCo_11F, Saffron guards, Route22 late Rival, League badge gates, ChampionsRoom | Progression/story/battle/puzzle/reward/Hall-of-Fame initialization; not tutorial-only. | Retained. Wholesale story/encounter removal is O02. `REQUIRED_PRESENT` |
| A43 Optional Sevii trip after accepting Bill | P OneIsland harbor OnFrame scene 2; Center `MeetCelioScene` scene 0; ThreeIsland bikers | Automatic scenes inside player-selected travel; Tri-Pass/Meteorite/Celio/Bill/Biker/Lostelle stateful content. | Retained after deliberate opt-in. D05 covers faster chosen story scenes; no automatic content removal. `REQUIRED_PRESENT` |
| A44 Optional developer/content NPCs | C `eventscripts`, Pallet/Viridian scripts and `SystemScript_DebugMenu` | Player-initiated custom gifts, developer menu and mechanic demonstrations; not forced intro or desired QoL. | Not counted as mandatory friction; developer/content expansion O03. Existing reachability is disclosed, not permission to use it. `OUT_OF_PILOT` |

A27/A29 are coverage indexes, not additional fix contracts. A03/A12b/A30/A25b/A37b correspond exactly to F01–F05. D02–D06 enumerate only additional product choices, without downgrading those fixes.

The sweep covered original early map scripts/coordinate events and all current integration manifests, plus later automatic scenes for National Dex, Cinnabar/Sevii, Tower/Fuji, Silph, League and custom NPC owners. No ROM-global assertion that every text string was runtime-traversed is made. Ordinary trainer spotting/battle intro/defeat text, puzzle feedback, bag-full feedback and legitimate reward/selection prompts are retained. The source review found no additional compulsory tutorial in Route 3/4/9/10 or Rock Tunnel itself. Broad runtime progression remains R1.

## B — Oak / character setup variants

The current intro is C guide-skip + vanilla Oak identity tasks. C `CreateOakIntroPokemonSprite` at `0x08130F2C` changes the demonstration Pokémon; it is **not** an intro-skip owner. Existing guide byte edits target `0x0812EDAC…0x0812EE8C`; they do not initialize names/gender for a whole-task bypass. No current C config setting implements full speech/setup skip.

**Source-proven state/lifecycle invariant:** P `intro.c:1008` / `title_screen.c:741` prepare SaveBlock2/default options with Sav2_ClearSetDefault; `Task_NewGameScene` initializes display/windows, sprite manager, help context and allocated speech resources. Gender selection writes SaveBlock2 `playerGender`. Naming writes SaveBlock2 `playerName[8]` and SaveBlock1 `rivalName[8]` (seven encoded characters plus EOS); confirms/default-name/cancel/retry are task-owned. `Task_OakSpeech_FreeResources:1777–1785` frees windows/manager/resources, clears AB speedup, destroys task and hands off to `CB2_NewGame`. P `NewGameInitData` preserves rival name around `ClearSav1`, generates a **fresh** four-byte Trainer ID, clears/initializes party, events, Dex, money, bag/PC/storage, map flags and room warp. It does not require fixed Trainer ID or hardcoded starter. Player name/gender survive the SaveBlock1 clear. C owns PC initialization, expanded-save wipe and stateless four-setting initialization through `FreshNewGameSettingsHook` at `0x08056656` after `NewGameInitData` (`assembly/hooks/general_hooks.s:361–380`, `hooks:324–325`), replaying ResetInitialPlayerAvatarState, PlayTimeCounter_Start and ScriptContext_Init before continuing at `0x08056662`; preserve Difficulty/Trainer Scaling/Wild Scaling/AI raw `4/1/0/7`, Auto-Run independence and native start-with-running config.

| Variant | State and current task/script owner | Hooks/repoints and risk | Save/ABI/layout; fixed values? | Disposition |
|---|---|---|---|---|
| A — skip Oak exposition, keep full creation | Keep current gender menu, player/rival naming, defaults/confirmation/return tasks. Bypass Welcome/ThisWorld/Nidoran/IStudy text/timers; still initialize any sprites/resources consumed by later cleanup. | Source-owned task transition wrapper around P `Task_OakSpeech_Init` / entry to gender phase; guard exact BPRE instruction/pointer identity and current guide owner. Medium risk: allocation, sprite IDs, fade/task return. No opaque Patch Editor bytes. | Existing SaveBlock fields and generated Trainer ID; no new fields or migration. Adds code/hooks in ROM only. No fixed names/gender needed. | `REQUIRED_FIX` F01; recommended least disruptive delivery. |
| B — minimal setup + naming | Keep player/rival naming callbacks and meaningful gender selection. Remove professor/rival introductory/closing prose and shrink ceremony; resources and valid task data still initialized. If gender menu is removed, gender must be supplied elsewhere. | Small source-owned creation state machine using existing naming UI and native callbacks; more task entry/exit binding than A. Medium/high lifecycle risk; no unowned jumps into partly initialized vanilla tasks. | No layout change if existing fields used. Names remain choices. Fixed gender is **not** technically mandatory if a minimal choice is kept; removing it requires D01 gender decision. | `NEEDS_USER_DECISION` D01 alternative to F01's recommended A. |
| C — complete IronMON-style intro/speech/character skip | Set encoded player name, rival name and gender, then call native new-game initialization in the correct order. Keep random Trainer ID, save/event/bag/party/storage/settings initialization; skip all speech/naming UI. | Hook New Game selection/scene entry **after** normal new-save options preparation, before any speech allocation; use source-owned initializer/wrapper and native `CB2_NewGame`, not Patch Editor's unrelated ROM addresses. Medium/high initial binding risk, then fewer UI lifecycles. | No SaveBlock/ABI change needed; identity fields already exist. Fixed names and gender are required for this exact no-choice variant. Do not reuse previous-save identity or rely on zero-filled strings. | `NEEDS_USER_DECISION` D01. User must specify player gender (Male/Female), player name and rival name, each ≤7 encodable characters. None chosen here. |
| D — current CFRU/BPRE better mechanism | Native save/new-game owners can host a minimal selector followed by initialization, but C only exposes guide skip/intro species, not a ready full-skip toggle. Reuse native state fields and existing naming screen, avoid Patch Editor binary transplantation. | A fresh minimal identity screen is possible but creates UI to test. A is the smallest source-owned path now; D is not falsely claimed already implemented. Entry/exit addresses beyond existing owners must be source-bound in the future component Issue. | Same fields/Trainer ID; no fixed values if choices retained. Remembered identity across resets would require a separately decided persistence design and is not selected. | `NEEDS_USER_DECISION` D01 alternative; no additional default recommendation. |

IronMON reference is separate from Faster FireRed: [public 1.2 release](https://github.com/DrMaple/IronMONPatchEditor/releases/tag/1.2) and [MainWindow.cs](https://github.com/DrMaple/IronMONPatchEditor/blob/63d3a45076192b7bdc9c2d6e0f4e031feeb99a02/IronMONPatchEditor/MainWindow.cs). Source has distinct Speech Skip, player/rival name and gender controls, seven-character encoding and writes separate identity fields. Its FireRed paths assume an already patched intro and different addresses; they establish behavior/required input, not safe BPRE/CFRU hooks. No binary patch was examined, decoded, executed or copied.

## C — Faster FireRed README reconciliation

Exact [README](https://github.com/DrMaple/Faster-FireRed/blob/db21d777083757067f242c62f592534f40bb2c77/README.md) inspected via GitHub source API. It targets FireRed Rev 1; the Workspace target is BPRE with its selected overlays. This is behavior comparison, not address/binary compatibility. All twelve feature bullets are accounted; Mt. Moon exclusion is separately explicit. National Dex timing in later release notes is not invented as a bullet of this pinned README.

| README feature | Source proof / current selected result | Final classification |
|---|---|---|
| Visible Hidden Items | C `hidden_item_sparkle.c` + `m009_overworld_frame.c`: on-screen eligible hidden BG events, collected/underfoot excluded; accepted sparkle provides visibility rather than permanent map marks. | `REQUIRED_PRESENT` |
| Viridian Forest Nurse | C `viridian_forest.s` + exact non-trainer replacement (29,58); no poisoned party healing. | `REQUIRED_PRESENT` |
| Talk to Mom Start | C `talk_to_mom.s`, exact house/Lab overlays. Necessary handoff present; D02 is a further flow choice. | `REQUIRED_PRESENT` |
| Shortened Parcel | C Route1 Clerk/outdoor Oak script and exact append/coord overlays. | `REQUIRED_PRESENT` |
| Repel Reuse | C BW_REPEL_SYSTEM; `overworld.c`, system script remembers/consumes stocked Repel. | `REQUIRED_PRESENT` |
| Gold TMs | C `tm_itemball_graphics.c`, 29 exact overlays: 28 TMs + HM07. Existing slot/reward typing preserved. | `REQUIRED_PRESENT` |
| Name Raters in Centers | C `name_rater_pokecenter.s`; 19 Center appends; existing nickname/rejection service. | `REQUIRED_PRESENT` |
| Instant Center Healing | C `pokecenter_instant_healing.s`; 19 ordinary Centers; Trainer Tower handling retained. | `REQUIRED_PRESENT` |
| Guaranteed Underground / Sevii Step Items | C `renewable_hidden_items.c`: approved groups fallback to populated tier on the 1,500-step cycle; preserves item slots. | `REQUIRED_PRESENT` |
| Mt. Moon exclusion | Same owner: Mt. Moon not included in guarantee policy. | `REQUIRED_PRESENT` |
| PC Item moved to Lab | C `new_game_pc_items.c`, `oaks_lab_potion.s`; clear initial PC and one Lab Potion. | `REQUIRED_PRESENT` |
| No forced Bill / Sevii invitation | C `optional_bill_sevii.s`; outdoor scene replaced, interactive Center trip kept. | `REQUIRED_PRESENT` |
| One-use Friendship Boost | README service in Viridian; no matching boost in current C Viridian scripts/overlays. Ordinary friendship/summary heart is not the boost. D13 must select/reject one-use service and rule scope. | `NEEDS_USER_DECISION` |
| Separate IronMON Intro / Speech Skip | Public 1.2 source controls identity. Current C guide skip only, normal choices remain; see D01 and F01. Not a Faster README feature. | `NEEDS_USER_DECISION` |

Result: every README feature accounted, eleven feature families already selected/present; Friendship Boost unresolved. Extra full character skip unresolved separately. Permanent mark style/expanded visual classes are D16/D17; this does not downgrade accepted M-009 visible-item behavior.

## D — NatDex reconciliation (all M-012 K01–K23 and A01–A13)

Rows retain historical IDs solely for complete accounting. Bundled A10/A11/A13 are split below so no small choice disappears into a broad “too deep” category. “Present capability” does not promise it is offered by every NPC. Target proof uses current C owners, not M-012's obsolete pins.

| M-012 ID / candidate | Pinned NatDex comparison and current CFRU proof/state | Final classification |
|---|---|---|
| K01 Repel reuse | N `field_control_avatar.c`/repel scripts; C BW_REPEL_SYSTEM + `overworld.c:2027…`, system_scripts. | `REQUIRED_PRESENT` |
| K02 Indoor running | N bike/avatar restrictions reduced; C CAN_RUN_IN_BUILDINGS and existing tile restrictions. | `REQUIRED_PRESENT` |
| K03 Auto-Run | Current C `read_keys.c`, FLAG_AUTO_RUN `0x914`; L toggle and B inversion user PASS. Not a missing NatDex port. | `REQUIRED_PRESENT` |
| K04 Reusable TMs | N consumes TMs; C REUSABLE_TMS, item/party handling. Preserve selected better reuse behavior. | `REQUIRED_PRESENT` |
| K05 HM convenience | C ONLY_CHECK_ITEM_FOR_HM_USAGE + `PartyHasMonWithFieldMovePotential`: actual HM item, non-egg compatible/knowing party, badge/location gates. Not full N menu. | `REQUIRED_PRESENT` |
| K06 Forgettable HMs | N Summary accepts forgetting; C DELETABLE_HMS + CheckIsHmMove. | `REQUIRED_PRESENT` |
| K07 Select from PC | C SELECT_FROM_PC script-aware APIs in `scripting.c`; service-specific availability. Do not promise universal Name Rater box access. | `REQUIRED_PRESENT` |
| K08 Party Move Items | C `party_menu.c` MENU_MOVE_ITEM/transfer/swap guards; existing richer capability. | `REQUIRED_PRESENT` |
| K09 Item image/description acquire | C ITEM_PICTURE_ACQUIRE + ITEM_DESCRIPTION_ACQUIRE, `scripting.c`/system scripts; actual acquired item. Game Corner config caveat remains D20. | `REQUIRED_PRESENT` |
| K10 Options / Start Menu | C three pages and `start_menu.c:192…`; item/party/Dex gates and PokeTools. No inferred HM/BGM toggle. | `REQUIRED_PRESENT` |
| K11 Auto lowercase naming | N auto-swap commented; C AUTO_NAMING_SCREEN_SWAP in `scripting.c`; exceptions retained. | `REQUIRED_PRESENT` |
| K12 Premier Ball behavior | N ball-pocket bulk bonus; C current `item.c` Premier calculation/capacity-first callback, M-013 integrated. Non-ball reward policy separate A12. | `REQUIRED_PRESENT` |
| K13 Controls Guide skip | C config + guarded byte replacement; A02. | `REQUIRED_PRESENT` |
| K14 Name Rater | N Center service; C 19-Center rollout and nickname guards. | `REQUIRED_PRESENT` |
| K15 Gold TM/HM balls | Established Faster reference; C 29-slot exact graphics rollout, not a global recolor. | `REQUIRED_PRESENT` |
| K16 Forest Nurse | N poison refusal; C exact replacement/script, accepted M-002. | `REQUIRED_PRESENT` |
| K17 Instant Center healing | N shorter nurse path; C M-003 ordinary-Center owner, bookkeeping preserved. | `REQUIRED_PRESENT` |
| K18 Renewable step items | N still samples tiers randomly in pinned source; C approved guarantee for selected groups, Mt. Moon excluded. | `REQUIRED_PRESENT` |
| K19 Lab Potion / empty PC | N Lab item; C new-game PC clearing + one normal Lab finditem Potion. | `REQUIRED_PRESENT` |
| K20 Fast Mom/Lab | C M-006 exact house exit/Mom/Lab scene 1→2 replacement, original waiting exposition skipped. Further no-Mom skip D02. | `REQUIRED_PRESENT` |
| K21 Shortened Parcel | C M-007 with current full National Dex special; route states/rewards present. | `REQUIRED_PRESENT` |
| K22 Optional Bill/Sevii | C M-008 preserves opt-in Center Yes/No; no forced outdoor invitation. | `REQUIRED_PRESENT` |
| K23 Hidden-item sparkle | C M-009 on-screen normal hidden BG events, transient effect, task-budget guard and >36-event fail-closed bound; always-on policy. | `REQUIRED_PRESENT` |
| A01 Running from Fresh New Game | C FLAG_RUNNING_ENABLED undefined; terrain checks remain, no failed pending latch. User B/L/save PASS; unrelated to old #538 flag timing. | `REQUIRED_PRESENT` |
| A02 Cinnabar Move Reminder | N ResearchRoom second object invokes TwoIsland paid MoveManiac; C no Cinnabar overlay. TwoIsland service remains. D12 decides earlier duplicate access. | `NEEDS_USER_DECISION` |
| A03 Full modern HM menu / no compatible-party rule | N `hm_menu.c`, Start/Options alternate mode. Current user-locked C item+compatible-party model retained; changing eligibility is not mere UI polish. | `EXPLICITLY_NOT_WANTED` |
| A04 Global BGM Off | N optionsBGM + `sound.c` PlayBGM/FadeIn; C Sound Mono/Stereo and Battle Music FRLG/RSE only. D08. | `NEEDS_USER_DECISION` |
| A05 Sparkle On/Off | N activation flag/default off; C scanner has no preference gate. Accepted always-on sparkle stays present; opt-out D09. | `NEEDS_USER_DECISION` |
| A06 National Dex timing | C shortened handoff special 0x016F exactly after ordinary Dex unlock and before five balls. Later #549 supersedes M-012 exclusion. | `REQUIRED_PRESENT` |
| A07a Instant Text | N `strings.c:884` labels gText_TextSpeedFast “Instant”; `text.c:50,892` implements instant fast path despite three-choice table. C INSTANT_TEXT commented out, Slow/Mid/Fast only. D07. | `NEEDS_USER_DECISION` |
| A07b Held R text autoscroll | C AUTOSCROLL_TEXT_BY_HOLDING_R + `text_printer.c` wait/arrow/level-up callbacks. Available compile-time convenience. | `REQUIRED_PRESENT` |
| A07c Fast Battle Messages | C FLAG_FAST_BATTLE_MESSAGES `0x925`, `general_bs_commands.c:476,546,1260,2003`; no current Options exposure or selected new-game activation. D11. | `NEEDS_USER_DECISION` |
| A08 Oak exposition cleanup | Current vanilla task chain after guide skip; F01. Prior “too deep/optional” no longer final disposition. | `REQUIRED_FIX` |
| A09 Friendship Boost | No selected source service; distinct from normal friendship mechanics. D13; historical optional/non-standard is not an explicit final rejection. | `NEEDS_USER_DECISION` |
| A10a Portable PC availability/distribution | C FLAG_PORTABLE_PC, `party_menu.c:2998` field-use and system On/Off scripts. Capability exists; no selected Fresh-New-Game distribution/activation found. D14. | `NEEDS_USER_DECISION` |
| A10b Safari allowance/default | C 600-step/30-ball selected config; N 9999-step policy is a rules change. D18. | `NEEDS_USER_DECISION` |
| A10c Broad display redesign | New summary/menu redesign beyond existing small switches is O02; small nature-color switch separately N05. | `OUT_OF_PILOT` |
| A11a Broader Item Ball visuals | C selected gold scope only; global TM/HM/item recolor not selected. D17. | `NEEDS_USER_DECISION` |
| A11b Underfoot sparkle / broader Itemfinder visuals | N Itemfinder arrow/star sprites; C M-009 excludes underfoot and does not rewrite Itemfinder. Additional cue policy D16. | `NEEDS_USER_DECISION` |
| A12 Non-ball purchase bonuses | C ENABLE_MULTIPLE_PURCHASE_REWARDS + `item.c` table persists for non-balls; Premier fix isolated correctly. Existing selected policy retained; no global reward removal. | `REQUIRED_PRESENT` |
| A13a NatDex content / mechanics / rules transplant | Selected Gen-9 data/runtime boundaries, missing engines and arbitrary content remain O01/O02. Small Safari preference separated A10b. | `OUT_OF_PILOT` |
| A13b Workflow/tooling/Tracker/Randomizer work | Separate Workspace/R2/#499/#500 contracts; no port or upstream preparation here. O04. | `OUT_OF_PILOT` |
| N01 Route 10 HM05 | C `route10_hm05.s`, one Hiker at (17,22), exact map counts; shared FLAG_GOT_HM05 with Route2 Aide, room/retry/once. | `REQUIRED_PRESENT` |
| N02 Move Reminder existing access | P TwoIsland_House paid MoveManiac retained, C `move_relearner.c` runtime/current-level paths. No missing reminder engine; D12 placement only. | `REQUIRED_PRESENT` |
| N03 Faster Fishing | N `field_player_avatar.c:1730–1798`: fewer dots, guaranteed bite when fish table exists, skips reaction loop. C fishing hooks change encounters/graphics/follower, not native fishing timing state machine. D10. | `NEEDS_USER_DECISION` |
| N04 Pickup activation sound | N Cmd_pickup calls SE_DINKDONK. C `atkE5_pickupitemcalculation:5320…` uses straight-to-bag/message, no dedicated bell. D19 decides cue; preserve existing success/bag-full semantics. | `NEEDS_USER_DECISION` |
| N05 Nature-colored stats | N `pokemon_summary_screen.c:4947…` BufferStat; C NATURE_COLORS_ON_SUMMARY_SCREEN disabled, existing bounded source implementation at :277…; not a full Summary redesign. D21. | `NEEDS_USER_DECISION` |
| N06 Bag capacity | N Items pocket 120 in constants/global.h; C include/global.h Items 42, Key 30, Balls 13, TMHM 58, Berries 43. D15 must choose pocket/quantity and migration policy; do not add unlike totals. | `NEEDS_USER_DECISION` |
| N07 National Dex at Fresh New Game | N new-game initialization versus selected normal handoff. Earlier unlock remains deliberately rejected; full data availability is not an unlock requirement. | `EXPLICITLY_NOT_WANTED` |
| N08 Full fixed-identity skip | IronMON reference, not implied by NatDex guide skip; D01. | `NEEDS_USER_DECISION` |

**Correction to supporting M-012:** a three-entry Options table does not prove absence of Instant Text in N. Pinned N changes its third label and renderer. #589 does not silently adopt N's replacement of Fast; C may add a fourth choice or use a distinct toggle after D07. Likewise, #558's correction remains: registered Celadon House2 MoveManiac has no normal city entrance; Cinnabar ResearchRoom is the source-backed reachable alternative. No missing early-Celadon implementation is carried forward.

### Additional search and current-public delta

Pinned-source links: [src/option_menu.c](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/src/option_menu.c), [src/strings.c](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/src/strings.c), [src/text.c](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/src/text.c), [src/field_player_avatar.c](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/src/field_player_avatar.c), [src/battle_script_commands.c](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/src/battle_script_commands.c), [src/sound.c](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/src/sound.c), [src/itemfinder.c](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/src/itemfinder.c), [src/pokemon_summary_screen.c](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/src/pokemon_summary_screen.c), [include/constants/global.h](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/include/constants/global.h), [data/maps/CinnabarIsland_PokemonLab_ResearchRoom/map.json](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/data/maps/CinnabarIsland_PokemonLab_ResearchRoom/map.json), [data/maps/TwoIsland_House/scripts.inc](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/data/maps/TwoIsland_House/scripts.inc).

Public [QoL page](https://github.com/CyanSMP64/NatDexExtension/wiki/Quality-of-Life-features) and [complete change list](https://github.com/CyanSMP64/NatDexExtension/wiki/Complete-list-of-changes-from-vanilla), observed 2026-10-01, now mention Accelerator, random battle music, short low-HP beep, nature colors, longer nicknames, accented naming, national-count Aide rewards and S.S. Anne room colors. The pinned FireRed source remains the baseline. Current documentation is mutable and can disagree with code: renewal wording does not override C's source-owned 1,500-step policy; “moved” Reminder does not prove Two Island removal. The source checks below provide separate candidate proof and target limits.

GitHub's public source comparison reports 57 commits ahead of pinned N (file listing truncated by API limits, not used as an exhaustive patch diff). Direct current-source checks establish Accelerator `ITEM_ACCELERATOR=379` and `NewGameInitData` award; Battle BGM default Contextual Random; Pickup bell persists; Cinnabar ResearchRoom and TwoIsland service persist. Public metadata/source was read only, never added to Workspace Gitlinks. No newest-source data/mechanic feature becomes an automatic pilot requirement.

| ID / additional candidate | Source and current-target finding | Final classification |
|---|---|---|
| N09 B-button quick wild escape | Pinned N `battle_controller_player.c:308–316` submits Run except shiny wild; retains double-partner cancel path. C `move_menu.c:2006–2185`/`hooks:54` owns action input: R already submits Run; B normally retains partner cancellation (conditional B+A selection helper is not the N shortcut). No selected B-only/shiny-guard equivalent. D22 decides convenience and shiny safeguard; no guarantee of successful escape. | `NEEDS_USER_DECISION` |
| N10 Low-HP beep limit | Public change list advertises three loops; pinned N `battle_gfx_sfx_util.c:864…` starts SE_LOW_HEALTH and its song asset owns repetition (asset not inspected). C native HandleLowHpMusicChange bindings in `include/new/Vanilla_functions_battle.h`/`src/exp.c` remain, with no selected beep-limit setting; no assertion of a tested defect. D23 decides shorter beep or current alert; implementation must source-bind the exact controller before writing. | `NEEDS_USER_DECISION` |
| N11 S.S. Anne trainer-room colors | Public QoL + pinned N room/layout definitions; C has no corresponding room-map color port. Bounded visual navigation preference D24; maps/assets require separate source-owned plan, no screenshots/assets examined. | `NEEDS_USER_DECISION` |
| N12 Aide rewards using National caught count | Pinned N Route11 Aide sets 0x8004=1/GetPokedexCount; P vanilla count service and current C no matching universal Aide script repoint. National Dex activation alone does not change caught-count reward thresholds. D25 decides national count for existing Aides, preserve thresholds/prizes. | `NEEDS_USER_DECISION` |
| N13 Accented naming characters | Pinned N `naming_screen.c:380,386` adds É/é in keyboard rows; target automatic lowercase is unrelated. No selected target accent keyboard change established. D26 decides this small naming-UI choice; exact encoding/glyph/key ownership needs source binding if selected. | `NEEDS_USER_DECISION` |
| N14 Longer nicknames / trainer names | New storage/string/writer/OT/layout implications; not a safe global constant toggle. Existing identity lengths retained. O05. | `OUT_OF_PILOT` |
| N15 Vitamins / EV / evolution / forms / ability/encounter changes | Existing C battle/data semantics are the pilot, not a requested NatDex balance transplant. Compare only in separately authorized mechanics/data work. O01. | `OUT_OF_PILOT` |
| N16 Accelerator double-speed runtime | New public N key item, not in pinned baseline. Timer/frame/audio/NPC-sensitive engine change, not a small message-wait toggle. O06; no transplant. | `OUT_OF_PILOT` |
| N17 Contextual/random Battle BGM | Current public N new_game/Options setting; C FRLG/RSE selector only. D27 decides current themes versus a bounded theme-selection extension; importing new-generation music/content is O02. | `NEEDS_USER_DECISION` |
| N19 Existing CFRU R quick Run | C `move_menu.c:2172…` submits normal/raid Run through the existing action owner; doubles cancellation remains in NORMAL_RUN. Present alternate convenience, distinct from D22 B/shiny policy. | `REQUIRED_PRESENT` |
| N18 NatDex Super Kaizo / debug / randomizer rules | Rule/content/randomizer expansion outside this audit; not “missing small QoL.” O03/O04. | `OUT_OF_PILOT` |

All 36 historical M-012 IDs are accounted (23 K + 13 A); A07, A10, A11 and A13 have explicit subrows. Additional small preferences are decisions, never discarded merely because an old report did not enumerate them. Source uncertainty about a future binding is disclosed; no presumed defect is converted into implementation without that binding.

## E — CFRU settings and capabilities

Direct C proof: `src/option_menu.c` names arrays at 153–179, choice arrays at 223–313, counts `{3,2,2,2,3,10,0}`, `{3,2,2,4,5,0}`, and `{6,AI_COUNT,3,2,2,0}`; raw/dirty preservation and save handlers at 392…/517…. `strings/option_menu.string` supplies current labels. Fresh profile raw `4/1/0/7` is stateless `src/settings.c:117…`; no settings ABI migration.

| Page / player-facing row | Current choices / type | Final classification |
|---|---|---|
| 1 Text Speed | Slow / Mid / Fast; presentation preference. No Instant currently selected. | `REQUIRED_PRESENT` |
| 1 Battle Scene | On / Off; animation/presentation. | `REQUIRED_PRESENT` |
| 1 Battle Style | Shift / Set; gameplay rules choice. | `REQUIRED_PRESENT` |
| 1 Sound | Mono / Stereo; audio mix, not mute. | `REQUIRED_PRESENT` |
| 1 Button Mode | Help / L-R / L=A; control preference; L=A suppresses L Auto-Run action. | `REQUIRED_PRESENT` |
| 1 Frame | Ten existing frames; cosmetic. | `REQUIRED_PRESENT` |
| 2 R Button Mode | DexNav / Pokémon / Items; controls. | `REQUIRED_PRESENT` |
| 2 Battle Music | FRLG / RSE; theme preference, not global BGM Off. | `REQUIRED_PRESENT` |
| 2 Wild Level Scaling | Off / On; challenge/scaling. | `REQUIRED_PRESENT` |
| 2 AutoSort Bag | Off / Name / Type / Amount; inventory QoL. | `REQUIRED_PRESENT` |
| 2 Game Difficulty | Vanilla / Easy / Normal / Hard / Expert; rules/preset semantics. | `REQUIRED_PRESENT` |
| 3 Trainer Level Scaling | Auto (Diff.) / Off / Easy / Normal / Hard / Expert; rules, independent stored axis. | `REQUIRED_PRESENT` |
| 3 Trainer AI | Auto (Diff.), six Legacy profiles, Standard, Ironmon Smart; rules/AI. Legacy Vanilla displayed as Legacy Vanil.; no remap. | `REQUIRED_PRESENT` |
| 3 Hard Cap | Auto / Off / On; rules. | `REQUIRED_PRESENT` |
| 3 Nuzlocke | Off / On; challenge, not generic QoL. | `REQUIRED_PRESENT` |
| 3 Wild Prebattle | Off / On; encounter presentation/rules. | `REQUIRED_PRESENT` |

Start menu retains Dex/Party reward flags, Bag/Player/Save visibility flags, Options, secondary PokeTools/DexNav/time paths and Safari retire behavior. It contains no NatDex HM action menu. PC selection APIs do not mean Start-menu Portable PC is enabled or distributed.

| Capability category | Source/current result | Final disposition |
|---|---|---|
| Player-facing useful settings | Sixteen rows above; existing raw mappings/readability retained. | `REQUIRED_PRESENT` |
| Compile-time QoL selected | Repel, indoor/start running, reusable/deletable TM/HM, lowercase, acquire UI, R autoscroll, Move Items; existing R quick-Run shortcut, faster healthbar changes and real move power/type/accuracy/effectiveness display defines. These are active behavior, not newly promised Options rows. | `REQUIRED_PRESENT` |
| Instant Text | Disabled compile-time renderer/hook; not fourth speed choice. D07. | `NEEDS_USER_DECISION` |
| Global BGM Off | No current player-facing mute layer; mono/stereo/theme selection is insufficient. D08; audio hook coverage must include restart/fade/battle/map and preserve SE/cries/fanfare waits. | `NEEDS_USER_DECISION` |
| Hidden Item Sparkle Toggle | Scanner always active, no Options row. D09; preserve task cleanup when disabling. | `NEEDS_USER_DECISION` |
| Faster Fishing | No selected timing replacement; chain encounter hooks do not prove shorter fishing task. D10. | `NEEDS_USER_DECISION` |
| Fast Battle Messages | Existing flag 0x925 skips completed-message waits in general_bs_commands; no current Options row/selected automatic activation. D11; distinct from Instant or Accelerator. | `NEEDS_USER_DECISION` |
| Additional bounded display switch | Disabled Nature Colors; existing source can support D21 without wholesale Summary rewrite. | `NEEDS_USER_DECISION` |
| Challenge/rules options | Scaling/AI/Difficulty/Hard Cap/Nuzlocke, team-preview/last-ball flags, consumable-return/Exp Share, poison/Safari rules are not automatic QoL toggles to expose. Existing selected rules retained; D18 only for Safari preference. | `REQUIRED_PRESENT` |
| Debug/developer features | DEBUG_* largely disabled; separate Lab DebugMenu and demonstration/gift scripts exist in eventscripts. No “enable all debug options” recommendation; O03. | `OUT_OF_PILOT` |
| Battle-engine mechanics | Mega/Dynamax/Terastal, Frostbite, accuracy/power/ability algorithms, evolution/transitions etc. Existing source is not a mandate for new mechanics. O01. | `OUT_OF_PILOT` |

## F — DPE settings conclusion

Direct source: [src/defines.h](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/defines.h), [src/Base_Stats.c](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/Base_Stats.c), [src/Learnsets.c](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/Learnsets.c), [src/TM_Tutor_Tables.c](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/TM_Tutor_Tables.c), [src/Pokedex_Data_Table.c](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/Pokedex_Data_Table.c), [src/Icon_Table.c](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/Icon_Table.c), [src/Cry_Table.c](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/Cry_Table.c), [include/species.h](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/include/species.h), [repoints](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/repoints).

DPE owns species/forms (through Pecharunt), Base Stats/learnset and representation tables, Dex data/order/habitat, graphics/palette/icon/cry tables, TM/HM/tutor compatibility and expanded data structures/repoints. Its `src/defines.h` has author-time expansion switches and table counts (`NUM_TMSHMS=128`, tutor moves 152), not player preference storage, option labels, menu handlers or input/save-setting dispatch. Tracked `src`/`include` tree inventory and settings-symbol search found no Options/Start-menu setting layer. Some Dex rendering/data integration is player-visible, but it is not a configurable QoL UI.

DPE data/representation: `REQUIRED_PRESENT`. A new DPE settings layer: `OUT_OF_PILOT` O07. No artificial settings architecture is proposed. Runtime/script/menu QoL belongs to CFRU; randomized-output settings belong to UPR-FVX. DPE/TM compatibility data remain inputs to existing HM checks, not owners of a new HM menu.

## G — Final decision lists

Each listed candidate has exactly one final disposition. Cross-references in earlier matrices are the same candidate, not separate work queues. Presence of existing choice A04–A06 does not pre-decide D01's replacement preference.

### REQUIRED_FIX

- **F01 Oak exposition:** skip nonessential professor exposition/timers while preserving correctly initialized creation and new-game lifecycle. Recommended variant A; D01 can choose a different delivery.
- **F02 Starter flavor:** remove isolated `OakThisMonIsEnergetic` forced message; retain starter confirmation, picture, reward, nickname, rival selection and progression.
- **F03 Pewter Gym Guide:** remove forced escort/two-message tutorial before Brock, retain badge-dependent Route 3 gate with concise feedback; no Brock bypass.
- **F04 Brock TM tutorial:** remove/replace false one-use-TM teaching block and unnecessary multi-page lecture. Preserve badge, TM39, capacity/retry/once flag and useful reward acknowledgement.
- **F05 Captain Cut tutorial:** remove extra forced `ExplainCut` block after HM01 award; retain Captain story/service, reward and departure state.

### NEEDS_USER_DECISION

| Decision | Exact product choice needed; no default value silently selected |
|---|---|
| D01 Oak / Character Full Skip | Choose A/B/C/D. Recommended A keeps normal creation. C requires player gender and player/rival names (each ≤7 encodable characters). B without gender UI also needs a gender source/value. Decide whether skip is the profile default or a selectable path; no names/gender invented. |
| D02 No-Mom / shorter Lab arrival | Keep selected mandatory Mom magic-trick/warp/entrance or automatic Room→Lab handoff/minimal arrival. Safe no-starter exit blocking remains either way. |
| D03 Rival ceremony / normal story trimming | Keep normal Rival selection/received-mon fanfare and battle approach/exit story or shorten those specific presentations; battles/choices/state stay. Includes optional further S.S. Anne Rival trimming. |
| D04 Cerulean Fame Checker flavor | Keep normal item/story return/exit or shorten its extra flavor/movement while retaining Rival battle, item and flags. |
| D05 Stateful story animation pace | Keep Bill teleporter/optional chosen Sevii introductions or shorten the named presentation while preserving ticket/travel/Celio/Meteorite/rescue state. No wholesale content skip. |
| D06 Gym reward move wording | Keep ordinary short reward prose or use generic/actual-item descriptions for randomized TM rewards (Misty/Surge/later gyms). F04 false consumable tutorial is required regardless. |
| D07 Instant Text | Select/reject player-facing Instant; choose fourth speed versus separate toggle and fresh default. Keep Slow/Mid/Fast unless user explicitly replaces Fast. |
| D08 Global BGM Off | Select/reject music-only mute; decide UI/default. Sound effects/cries/fanfare completion remain valid. |
| D09 Hidden Item Sparkle Toggle | Select/reject in-game opt-out and fresh default. Existing accepted always-on visibility is present. No offline/randomizer flag contract silently added. |
| D10 Faster Fishing | Select/reject shorter timings; explicitly choose timing-only versus NatDex guaranteed bite/reaction-loop skip. Probability/rule changes are not implied by faster animation. |
| D11 Fast Battle Messages | Select/reject exposing existing wait-skip flag; decide menu/default. Does not mean Instant Text or broad faster engine. |
| D12 Cinnabar Move Reminder | Select/reject reachable ResearchRoom duplicate of existing paid service; preserve Two Island, mushroom price, cancellation/current-level rules and Metronome Tutor. No free/all-level relearner. |
| D13 Friendship Boost | Select/reject one-use Viridian boost and which rules profile permits it; explicit balance choice, not automatically “against Ironmon therefore rejected.” |
| D14 Portable PC availability | Keep current gated capability or specify distribution/unlock location and availability restrictions. No default new item/source invented. |
| D15 Bag capacity | Keep Items=42 or choose exact pocket/count and save-compatibility policy. Existing bag structs/offsets make this more than editing a number; source design required if selected. |
| D16 Broader Itemfinder / underfoot / permanent marks | Keep accepted on-screen sparkle + existing Itemfinder or select exact extra cue and event classes. No generic “broader visuals” port. |
| D17 Broader Item Ball visuals | Keep accepted 29-slot gold scope or name extra TM/HM/item classes; preserve randomized slot typing, low byte and discovery/writer ABI. |
| D18 Safari allowance | Keep current 600 steps/30 balls or explicitly choose changed limits; rules choice, not a default modernization. |
| D19 Pickup activation sound | Keep current straight-to-bag message or add success-only bell (choose existing sound versus new asset); bag-full/failure cue policy must be explicit. |
| D20 Acquire UI Game Corner caveat | Current config warns picture acquisition breaks prize room. Source comment is not a reproduced current failure. Decide whether supported final profile includes prize exchange; if included, source-only reachability design/targeted user-owned runtime must resolve caveat before acceptance. No blanket fix claimed. |
| D21 Nature stat colors | Select/reject existing bounded summary switch; no Summary redesign. |
| D22 B quick wild escape | Select/reject shortcut, retain doubles cancellation and decide shiny protection; no guaranteed escape. |
| D23 Short low-HP beep | Keep current alert or select capped loops, with exact source controller binding before implementation. |
| D24 S.S. Anne room colors | Select/reject bounded navigation cues; exact trainer/immediate-spotting classes before implementation. |
| D25 National-count Aide rewards | Keep vanilla reward eligibility or count National caught species at unchanged thresholds/prizes. |
| D26 Accented naming | Select/reject É/é keyboard access; source encoding/glyph plan if selected. |
| D27 Random Battle BGM | Keep FRLG/RSE or select a bounded random/contextual chooser using existing themes. No imported soundtrack expansion. |

No decision is needed to invent names for variant A. Preference unresolved is not the same as missing source proof; technical binding gates are documented separately and must precede later writes.

### EXPLICITLY_NOT_WANTED

These derive from retained confirmed product decisions, not new rejections invented by the audit:

- Full NatDex modern HM/no-compatible-party eligibility model in place of selected HM item + compatible non-egg party + badge/location contract.
- National Dex at Fresh New Game instead of the accepted normal Pokédex/Parcel handoff.
- Reverting selected reusable TMs / forgettable HMs / native start-with-running to vanilla limitations merely for literal reference parity.

Historical “held”, “optional”, “not standard Ironmon” and “no defect proved” do **not** establish explicit rejection of the D01–D27 choices.

### OUT_OF_PILOT

- **O01:** missing Gen-9 mechanics (Commander/Hospitality/Embody Aspect), new parity-driven form/Terastal transitions, NatDex battle/EV/evolution/ability/balance transplant and broad battle-engine refactors.
- **O02:** wholesale story/encounter/content removal, broad UI/graphics redesign, new soundtrack/content imports. Named small scene/visual choices remain D decisions, not hidden here.
- **O03:** debug/developer feature promotion, gift/demo/cheat systems and Super Kaizo rule/content expansion. Existing optional debug owners are disclosed only.
- **O04:** Randomizer R2 changes/runs, BizHawk, Tracker, CI/tooling/workflow modernization and upstream contribution. Separate downstream contracts; `UPSTREAM_CONTRIBUTION = DEFERRED`.
- **O05:** expanded nickname/trainer-name storage/ABI port.
- **O06:** public NatDex Accelerator/whole-game double-speed engine transplant.
- **O07:** invented DPE Options/settings layer.

### REQUIRED_PRESENT

Source and accepted scope already cover M-001–M-009/M-013 selected behavior, 19-Center Name Rater, Repel reuse, indoor/start running and Auto-Run, reusable/deletable TMs/HMs, current HM eligibility, PC-selection capability, Party Move Items, acquire image/description (D20 caveat), Options/Start menu and raw mappings, auto-lowercase, R autoscroll, Premier bonus/capacity handling, current non-ball bonuses, normal-handoff National Dex, Route10 HM05/shared Route2 flag and existing Two Island paid Reminder. Necessary creation/starter/Rival/badge/reward/story states remain present. DPE's data/representation role is present. The supplied Running/Sign Lady/Pewter Aide runtime passes are preserved without generalizing them to all R1 cases.

## H — Proposed independent implementation contracts/order

Every F entry gets its own future Workspace Issue and bounded CFRU Component PR. CONTROL owns issue creation after review. Workspace integration/pin changes are separate authorized contracts; none occur in #589. D-selected additions get their own independent contracts, not a giant follow-up PR. No fix requires DPE or UPR source changes by default.

All script replacements must first prove exact BPRE scene/object/coord/pointer identity from source/symbol evidence, preserve unrelated entries and fail closed on mismatch. No address is guessed from the Rev 1 Patch Editor or a different decompilation layout. No SaveBlock expansion, mutable file-static state or flags borrowed without ownership review. Runtime checks below are **future user-owned checks**, not requests for protected artifacts in this audit.

| Order / fix | Component owner; smallest change / expected files | Source owner | Source-only test boundary | Future runtime check |
|---|---|---|---|---|
| 1 F01 Oak exposition | CFRU; bounded intro task-transition wrapper preserving creation. Expected `src` intro owner, corresponding assembly hook, `hooks`/`functionrewrites` as proved, config only if a selected profile gate is needed. D01 may substitute minimal/full-skip design. | P oak_speech Init→gender/name tasks, FreeResources→CB2_NewGame; C guide/species owners and new-game settings lifecycle. | Exact entry/exit binding and resource initialized/freed invariants; no global save/layout changes; gender both paths, names/default/No/retry/callback, independent raw 4/1/0/7 and generated Trainer ID. Host tests must not stand in for target lifecycle proof. | Fresh New Game with both selectable genders/names or user-fixed C identity; starter OT/name/gender, Trainer Card, naming re-entry, save/reload, B/L running/settings. |
| 2 F02 Starter flavor | CFRU; replace only ChoseStarter message owner with equivalent flow omitting energetic flavor. Expected `assembly/overworld_scripts` new bounded owner, symbol/overlay manifest and focused source tests. No starter data changes. | P Lab ChoseStarter, `VAR_STARTER_MON`, SYS_POKEMON, nickname callback and RivalPicksStarter. | Guard exact scene/script binding; all three choices, No/retry/nickname Yes/No, correct reward/ball removal and scene 3; no hardcoded randomized species/new ABI. | All three starter paths/nickname choices, Rival battle win/loss continuation, Lab exit/Parcel progression and save/reload. |
| 3 F03 Pewter Gym Guide | CFRU; replace scene-0 guide CoordEvent handlers with concise badge-gate response/no escort; preserve Gym Guide object or deliberately harmless interaction, leave scene-1 Aide cleanup unchanged. Expected new script, `mapobjectoverlays`, focused overlay checks. | P Pewter scene-0 coords/GymGuide; C exact scene-1 Aide owner. | Prove 7-object/7-warp/7-coord/6-BG identity and all three reachable triggers; preserve inaccessible fourth entry unless source contract explicitly includes it; block before badge, pass after; no duplicate scene owner. | Attempt east exit pre-Brock: no escort/softlock, no early Route3; defeat Brock, cross all lanes/re-enter/save, existing Aide cleanup still PASS. |
| 4 F04 Brock tutorial | CFRU; bounded GiveTM39 path retaining award/failure flags and concise acknowledgement, omit consumable-TM/long tutorial. Expected new script/text if needed, exact binding manifest, focused reward checks. | P Pewter Gym GiveTM39/DefeatedBrock; C REUSABLE_TMS. | Badge/defeat/FameChecker/Gym trainers/Pewter scene preserved; room/full/retry and one-time TM award; no TM move/item IDs or teaching semantics altered. | Brock reward, full pocket/retry, no duplicate award, reusable TM after teaching; correct Pewter gate/Aide and reload. |
| 5 F05 Captain Cut tutorial | CFRU; bounded Captain reward script omitting only post-award ExplainCut; preserve seasickness story and native reward/scene/release. Expected new script + exact map object binding, source guard. | P SSAnne_CaptainsOffice Captain / GOT_HM01 / Vermilion scene. | Same HM01 reward, successful once flag, scene and release; preserve existing item-space semantics rather than silently redesigning them; no new Cut/menu/hook eligibility. | HM01 once, captain revisit, ship departure/Cut gate and bag/save persistence; no blocked release or repeated ship scene. |

F01 and D01 must be settled together; do not implement A then immediately replace it with C. F02–F05 are technically independent and do not depend on fixed names/gender. Highest-value selected decision additions next: D07/D11 message pace; D08/D09 simple preferences; D10/D19 repeated action feedback; D12 reminder access; then selected display/access/capacity/other choices. Each gets a fresh source binding/design contract and risk-appropriate tests. D15 bag growth needs explicit save/layout analysis before any code; it cannot be bundled with a cosmetic option.

After component reviews and user merges, integrate exact pins through CONTROL, perform targeted user-owned build/runtime observations, then refresh R1 once against the final selected profile. Rebaseline must account for every rejected decision explicitly and every selected capability's caveat. Only then run final continuous R1; Randomizer acceptance remains R2 behind ROM_PROFILE_READY.

## I — Verification and protected boundary

- Before writes: approved non-main branch at exact base, empty isolated `git status --short`, safety script PASS. Original implementation checkout preserved with its pre-existing dirty CFRU state; it is **not falsely certified clean**.
- Before handoff: `python3 07_scripts/bootstrap/check_git_safety.py` PASS; `git diff --check` and staged diff check PASS; base-to-final changed-file list exactly `docs/audits/final-rom-ux-completeness-2026-10-01.md`.
- Audit worktree clean after commit. Component source checkouts in audit worktree uninitialized, not a claimed build-ready environment; no component writes or tests/builds there. Clean source-writing checkout does not change the user's persistent build/runtime Workspace preference.
- Recursive Gitlink tree identity compared to base: unchanged, including all supporting references; no submodule checkout update or gitlink change.
- Completeness check: twelve Faster README bullets + separate Mt. Moon boundary + separate IronMON item; all K01–K23/A01–A13 IDs, additional small NatDex candidates; all user-named opening/dialogue entries; exact sixteen Options rows; each matrix row uses one allowed final class. Running, Sign Lady and post-Brock Aide classified present.
- This report is analysis/decision only: no product implementation, no implementation Issue created, no component PR, no Randomizer run/emulator/build or upstream PR, no merge. PR is review evidence against main only.
- No ROM, save, emulator state, screenshot, generated build, patch binary, tool binary, protected/private artifact path, `.env`, token, key or secret was read, used, requested, changed, staged or committed. Public source text and sanitized user-supplied checkpoint statements only. Git source-object access does not inspect protected local outputs.
