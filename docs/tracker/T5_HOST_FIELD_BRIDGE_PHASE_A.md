# #711 — detached Party/Battle-to-host field bridge

**TEST_ONLY; liveConfidence=UNKNOWN; production=DENIED.** Source/synthetic
candidate, pending independent CONTROL review and user merge. No normal Tracker
UI, loaded-output identity, live fields or Phase B acceptance is established.
Contract: [#711](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/711).
One writer; branch `feature/tracker-host-field-bridge-mock`.

## Entry and immutable boundary

Live GitHub main `17c859785015d9c48544558969bade7f0212ba0b`, tree
`4467d832eb0c8c6790c47738176ffdec4b266424`, verified before branch creation.
Accepted #707/PR #708 and #709/PR #710 CONTROL post-merge comments were read,
with AGENTS.md, all six canonical documents, #500, #691–#695 and the requested
T3/T4/T5/profile/consumer/guard records. Older canonical component references
are historical; the live Issue/product lock supplies this task's exact pins.

One live Project 4 check covered all 142 items. #711 is already present as
`PVTI_lAHOBYjlAs4BkHQfzg_aAdE`, position 142, with Status/Priority/Work Type
unset. No Doing/In Progress item was found. Closed #707/#709 are not competing
contracts. Explicit CONTROL routing authorizes this bounded Mac preparation.
No Project fields were modified or inferred; no repeated metadata gate.

Exactly five NEW paths: the detached extension `source_host_field_bridge.lua`,
its `run_cfru_dpe_host_field_bridge_mock_tests.py`,
`test_cfru_dpe_host_field_bridge_source.py`,
`tests/cfru_dpe_host_field_bridge_mock.lua`, and this document. The new exact-path
verifier checks all existing files against accepted main and all ten Gitlinks
against both main and product lock `3bdfe9919afc0b7bea55c79f37285e832be495c3`
(tree `f6bc65355811d7de153a91091b223fec9b50991e`), including tracked checkout
cleanliness. Production entrypoint, T1 profile/generator, previous modules,
fixtures/runners and components remain byte-identical.

| Gitlink under `02_external/` | Unchanged SHA |
| --- | --- |
| CFRU-expansion | `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2` |
| Dynamic-Pokemon-Expansion-Gen-9 | `d887185de1f6ae6a78e85c4311bbadde17041d00` |
| Ironmon-Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| references/cyansmp64-pokefirered-natdex | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| references/cyansmp64-upr-zx-natdex | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` |
| references/pret-pokefirered | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |
| references/upr-fvx-upstream | `e0788edc6529c2605f201996e4807ff30165354c` |
| references/upr-zx-ajarmar | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` |
| upr-fvx | `4670a5413104ec02bc08c09ff584470a8a6cb7bd` |

## Trust chain and accessor contract

`newMock(host, expected, bodies, publicJson, publicSources, multiText)` constructs
an internal instance of the unchanged #709 guard. It never accepts a supplied
guard, readMock closure, predecoded field table or verified/trusted boolean.
The unchanged guard binds four original body hashes, exact T1 serialization
SHA `8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981`,
profile ID `sha256:31be9e07697f939b274c56eea5d92a81dd10c43e7c876586effccb335535ca75`,
the five public T3 source texts and T4 `include/new/multi.h` source hash.
The Python bootstrap additionally compares all accepted dependencies to the
immutable #709 main blobs before execution. No public/private profile is generated.

`installMock`, `transitionMock`, `submitMock`, `teardownMock` delegate to this
internal guard. Only accepted submit results receive a bridge-owned opaque ticket;
its guard ticket is private. `contextMock(ticket)` and
`selectMock(ticket, "PLAYER"|"ENEMY", slot1to6, "PARTY"|"ACTIVE")` re-read
#709 on every request before selecting any field. Returned views are detached
read-only proxies, with `HISTORICAL_COPY_REQUERY_REQUIRED`; every field carries
confidence, optional value, reason, provenance, scope, profile, sampleEpoch,
TEST_ONLY/live UNKNOWN/production DENIED. No returned proxy is a current live
reference. Raw mutation of a historical caller proxy cannot affect the source
or a later request. Bridge tickets revoke even on same-epoch sample replacement.

Only supported two-battler wild/trainer singles accepted by #709 publish values.
T4 u16 indexes use +2 stride and explicit zero-based index to one-based slot
conversion, independently for each side. Active rows stay separate from parties;
there is no party fallback for an absent/invalid active field. The guard rejects
an entire invalid sample, so the bridge cannot retain even otherwise plausible
party fields from that rejected sample. Within an accepted sample, unknown
optional/effective fields leave verified HP, identity, moves and current PP intact.

Known double/multi flag requests are classified UNAVAILABLE by a **denial-only**
raw flag recognizer following guard rejection. This is not proof that their
context/bytes are valid; no values or accepted context accompany this diagnostic.
Unknown flags, stale/malformed/foreign samples are UNKNOWN. Outside an accepted
encounter, enemy and active selections are UNAVAILABLE. Invalid slots are UNKNOWN
and never clamped to another occupied slot.

## Field confidence and source matrix

V = VERIFIED **source/synthetic only**; U = UNKNOWN; N = UNAVAILABLE.
All live confidence stays UNKNOWN. Identity catalog labels describe baseline
source identity; they never prove current mechanics or randomized properties.

| Accessor field | Party source / confidence | Active source / confidence and precedence |
| --- | --- | --- |
| team, slot, occupied | Explicit side; six-slot T3 count/prefix; V including false occupancy | T4 side/position and u16 index; V for supported left battler; other active slot N |
| pokemonID, speciesIdentity/form aliases | T3 direct species u16 at 32, T1 internal ID; V including SPECIES_NONE | BattlePokemon species u16 at 0x00; V; active identity never overwrites party identity |
| level | Pokemon u8 at 84; V | BattlePokemon u8 at 0x2A; V |
| curHP, stats.hp (maxHP) | Pokemon u16 at 86/88; V | BattlePokemon u16 at 0x28/0x2C; V; 11/121 versus party 73/120 |
| heldItem | Pokemon u16 at 34 + effective CFRU item mapping; V, including absent 0 | BattlePokemon u16 at 0x2E; V; active 744 versus party 743 |
| primary status | Pokemon u32 at 80, source masks/locked FROSTBITE; V | BattlePokemon status1 u32 at 0x4C; V; active BURN remains distinct from party FROSTBITE |
| moves[i].id | Pokemon four u16 at 44 + T1 mapping; V including NONE 0 | BattlePokemon four u16 at 0x0C; V |
| moves[i].pp | Stored Pokemon u8 at 52; V, cap unproved | BattlePokemon u8 at 0x24; V only after #709/T4 cap gate; active 2 versus party 7 |
| moves[i].maxPP | U, no baseline maximum substitution | U, even though T4 acceptance requires declared same-sample synthetic ppCaps |
| moves[i].power/category/type/accuracy | U; no baseline/catalog/randomization heuristic | U; active identity/PP does not prove effective move properties |
| abilityID | U; GetMonAbility/TryRandomizeAbility unresolved | BattlePokemon u8 at 0x20 + accepted mapping; V ID 254 |
| abilityName, abilityNum | U; catalog name/stock two-slot selector never substituted | U; contextual name remains separate from verified ID |
| types[1..3] | U effective party types | BattlePokemon bytes 0x21/0x22/0x18; V mapped IDs |
| personality/trainerID/nature/experience/nickname/statStages/full stats | U; no DefaultPokemon/zero/default-stage synthesis | U; not borrowed from party |
| empty slot dependents | N for T3 unavailable HP/status/item/moves; explicit occupancy false and species 0 stay V | No active empty object accepted |
| trainer A/B | Not a party field | A U in supported trainer context, N in wild; B N; caller trainer trust rejected by #709 |
| derived damage/STAB, render/notes/BattleDetails | No accessor/calculation provided | Unsupported integration; NOT_RUN |

Source locators: CFRU `include/pokemon.h::Pokemon`,
`include/battle.h::BattlePokemon`, `gBattlerPartyIndexes` declaration and
`src/battle_util.c::GetBankPartyData`; `include/constants/battle.h` status/flags,
`include/new/multi.h` B alias; DPE `src/Base_Stats.c` and CFRU
`src/Tables/battle_moves.c` supply separately locked baseline mappings. T1 ARM
layout evidence supplies offsets; fixtures independently declare literal bytes.
Gen1 1, Gen8 1102, Gen9 **internal 1294 versus Dex 906**, regional 1022, nonzero
personality/OT bytes, six-to-one and player slot 6/enemy slot 2 are explicit oracles.

## Original execution versus synthetic stubs

The runner reuses #707 immutable extraction, independent REVIEWED body hashes
and restricted sandbox, via unchanged #709 bootstrap composition. It repeats
all 63 #707 controls (including 13 EXPECTED_STOCK_HAZARD cases) and adds bridge
controls marked PASS_TEST_ONLY. Only pure string byte/gsub/gmatch and the
already-reviewed synthetic namespace setter are added by #709's bootstrap.
No original body is rewritten. IO/process/network/GUI/memory/state/persistence,
reflection, loaders, global mutation and fallback catalog probes remain trapped.

| Bridge oracle execution | Original unchanged body | Scope |
| --- | --- | --- |
| TrackerAPI.getPlayerPokemon | TrackerAPI.lua:28–33 | default/explicit player slot, party and active facade, invalid/stale selections |
| TrackerAPI.getEnemyPokemon | TrackerAPI.lua:38–43 | separate enemy slot, encounter-only data, stale/outside nil |
| TrackerAPI.getActiveBattlePokemon | TrackerAPI.lua:47–59 | two selected left objects, zero after invalidation, no right objects |
| Battle.getViewedPokemon | Battle.lua:257–267 | own/enemy/view-side selection and stale denial |
| Tracker.getPokemon | **Synthetic stub in bridge oracle** | re-queries bridge, explicit PARTY or ACTIVE facade mode; never original coverage |
| Battle.inActiveBattle | **Synthetic stub in bridge oracle** | fresh bridge context/readiness on every call |
| Utils.inlineIf | **Synthetic stub** | pure conditional used by original Battle getter |
| Battle.Combatants / numBattlers | **Synthetic fixture values** | copied supported slots, no real host tables |

The stock active getter itself selects party slots; the explicit ACTIVE facade
supplies the bridge's separate active rows. These original bodies are selection
oracles only. Repeated #707 controls have their own original counts, traps and
expected hazards; they are not corrected bridge coverage. All guarded bridge
reader entries have zero original reader delegation, zero synthetic address
reads, zero forbidden host attempts and zero default/catalog fallback. Only
negative #707 controls deliberately attempt trapped operations; no backend exists.
Per-body counts and class totals are printed and recorded in the final PR.

## Lifecycle, failure and safety evidence

Start/end/switch/reset/reload/output/session/unknown events, unannounced host
profile/pin/session/output/encounter/epoch changes, foreign wrapper/namespace/
restart owners, duplicate install/unload, failed transactional install, stale
or cross-bridge tickets, same-epoch replacement, replay, truncation and caller
predecoded/closure/metatable/trainer trust are tested. Retained historical copies
stay labeled; fresh requests return no stale values. Tests assert species 1294,
party HP 73/PP 7 and active HP 11/PP 2 independently, reject poisoned u16 0x0105
and illegal zero-based 6, and refuse missing cap/ability/active HP without any
party/stock recovery. Wrong public source/profile/multi/body bytes reject factory
construction before a snapshot exists. Mutable proxy contamination cannot affect
re-query; guard tickets cannot be adopted as bridge tickets.

## Verification and hard stops

Use only installed Python 3 and `/opt/homebrew/bin/lua5.4` (reported 5.4.9).
Final post-commit runs/counts, exact head/base/tree and PR URL are in the PR,
avoiding a self-referential document commit SHA.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_host_field_bridge_mock_tests.py --python-source
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_host_field_bridge_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_preconsumer_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_host_consumer_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_extension_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_party_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_battle_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_ui_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 07_scripts/bootstrap/check_git_safety.py
git diff --check 17c859785015d9c48544558969bade7f0212ba0b HEAD
```

Development evidence: the first bridge run had 140 PASS / 2 FAIL because the
new field mapper lost VERIFIED boolean false through Lua and/or. The independent
empty-slot/six-to-one tests exposed it; explicit conditional assignment preserves
false. Final post-commit results supersede this development run.

Python: run all T2–T5, #707/#709 source/isolation and T1 ParserTests, plus the new
#711 tests. Individually exclude only:

- `HostConsumerSourceTests.test_exact_four_new_paths_all_gitlinks_and_component_status`:
  **NOT_RUN — superseded by #711's exact five-file verifier**.
- `PreconsumerSourceTests.test_exact_five_new_paths_existing_files_and_ten_clean_gitlinks`:
  **NOT_RUN — superseded by #711's exact five-file verifier**.

All other safe regressions remain required. LockedProfileTests (21) and generator
`--check` are NOT_RUN because they require Clang. Lua 5.1 is unavailable, NOT_RUN.
No C/Java build, generator, ROM/save/state/build/binary/private-manifest/offsets/
secret access, emulator or actual Tracker startup. CASUAL_NATDEX.rnqs is unread,
untouched, unstaged. Earlier documentation commands requiring Clang do not
supersede this Issue's explicit no-Clang boundary.

Direct DataHelper/TrackerScreen/BattleDetails rendering and persisted notes are
NOT_RUN: pinned DataHelper.lua:124–412 consumes defaults/catalog/notes; screen
TrackerScreen.lua:1102–1125 draws independent data; BattleDetailsScreen.lua:458
fans out into direct RAM consumers (743, 759, 879, 1113, 1287, 1433+); Tracker.lua:
583/612/632/680 records/saves/loads/verifies persisted state. Unknown effective
fields MUST NOT flow into those unmodified display/calculation paths. No
production adapter, live wrapper ownership, output/session or safe RAM provenance
is established. #689/#499, #691–#694 Phase B, #695 E2E, #500 and #501 stay gated;
UPSTREAM_CONTRIBUTION=DEFERRED. Never merge from Codex.

## Exactly one next bounded Mac proposal

A separate TEST_ONLY persistence/consumer gate contract: quarantine restored
notes/observations from current field confidence and test epoch revocation at
selected pinned consumer seams, without files, emulator, rendering or production
activation. This proposal is not authorized by #711.
