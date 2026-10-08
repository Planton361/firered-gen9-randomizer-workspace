# #713 — detached note/observation quarantine

**TEST_ONLY; liveConfidence=UNKNOWN; production=DENIED.** Candidate evidence
for [#713](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/713),
pending CONTROL review and user merge. The exit marker is reserved for CONTROL
post-merge acceptance. No normal Tracker adapter, notes support or live field
confidence follows from this source/synthetic work.

## Entry and boundary

One writer, fresh branch `feature/tracker-note-consumer-quarantine-mock`.
Live GitHub main `17e1351c079863cb9797f520f2dc4cb4530deb2a`, tree
`1623813b1fd066aa118b810ffd5dfbe3ba9dcc34`, confirmed before branching. The
previous local #711 head had exactly that tree. AGENTS.md, six canonical
documents, complete #713, current #500/#689/#691–#695, accepted CONTROL
post-merge #707/#709/#711 and the profile/consumer/guard/bridge records were
read. Existing files stay byte-identical. The known untracked
`CASUAL_NATDEX.rnqs` remains unread, untouched and unstaged.

A single paginated Project 4 inventory covered 142 items: no OPEN Doing/In
Progress or other competing eligible active contract. #499/#500/#501 are P1
or backlog; #689/#691–#695 remain host/dependency gated. Closed predecessor
contracts do not compete. #713 was absent from that inventory and was added
alone as `PVTI_lAHOBYjlAs4BkHQfzg_aylQ`. Status/Priority/Work Type remain unset;
no field values were invented. The earlier incomplete GraphQL request had a
syntax error; the successful complete inventory supplied the order decision.

Exactly five NEW paths:

- `03_tools/tracker-extensions/CFRUDPEExtension/source_note_consumer_quarantine.lua`
- `07_scripts/tracker/run_cfru_dpe_note_consumer_mock_tests.py`
- `07_scripts/tracker/tests/cfru_dpe_note_consumer_mock.lua`
- `07_scripts/tracker/test_cfru_dpe_note_consumer_source.py`
- `docs/tracker/T5_NOTE_CONSUMER_QUARANTINE_PHASE_A.md`

The exact-five-file verifier rejects any modified/deleted existing file or
extra path, and compares all ten Gitlinks with both base and product lock
`3bdfe9919afc0b7bea55c79f37285e832be495c3` / tree
`f6bc65355811d7de153a91091b223fec9b50991e`. Each checkout HEAD and tracked
cleanliness is checked. No production entrypoint imports the candidate.

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

## Internal trust chain and consumer contract

`newMock(host, expected, bodies, publicJson, publicSources, multiText)` constructs
the real unchanged #711 bridge, which constructs the unchanged #709 guard.
It accepts no injected bridge, guard, reader, predecoded fields or verified
labels. The Python runner locks accepted dependencies to base blobs before
Lua execution; the underlying modules independently validate the public source
texts, four original reader bodies, T1 profile SHA
`8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981` and profile ID
`sha256:31be9e07697f939b274c56eea5d92a81dd10c43e7c876586effccb335535ca75`.

Current data traverses owned `newMock → installMock → transitionMock →
submitMock → bridge.contextMock/selectMock`. Consumer tickets wrap private
bridge tickets; observation tickets are a separate owned identity. Every read
rechecks bridge ownership, complete synthetic binding and freshness before
selecting anything. Every install, submit, transition and teardown invalidates
the consumer revision and observation registry. Thus same-epoch replacement
also revokes old tickets. Foreign or contaminated tickets cannot be adopted.

`quarantineMock(snapshot)` does not inspect, traverse, copy, store or mutate
its argument, including metatable-bearing inputs or forged matching identities.
It returns only `QUARANTINED`, a count of **snapshot submissions**, and a
content-free reason. The count does not inventory records. The caller retains
its historical snapshot unchanged: quarantine is distinct from deletion.
There is no loader, importer, migration, real note clear or file operation.

`observeMock(consumerTicket, witness)` checks a bounded numeric/string witness
against the current ACTIVE bridge row: internal species, side, occupied active
slot, move slot/ID, level, known current PP and synthetic encounter association.
All extra fields, text, trusted labels, mismatches and unsupported slots fail.
The gate creates an ephemeral observation ticket after these independent
checks. This proves only a matching **source/synthetic move identity**; it does
not prove a real attack event, output identity, persisted note or ability.

`readMock(consumerTicket, category, side, slot, observationTicket)` returns a
fresh detached read-only historical record. Every category result has
confidence, reason, provenance, profileId, epoch/sampleEpoch, TEST_ONLY,
live UNKNOWN, production DENIED and `HISTORICAL_COPY_REQUERY_REQUIRED`.
Only VERIFIED results have a value. Requery with both owned tickets is required
for current move use; already-returned copies cannot be retroactively erased.
Mutating a retained caller proxy cannot alter any later query. These records
are not normal Tracker.Data, display rows or calculation inputs.

| Category / state | Current view policy and evidence |
| --- | --- |
| Saved `note` | UNKNOWN, no text or empty-string fallback; old notes always quarantined |
| Tracked `abilities` | UNKNOWN, no names/IDs or `{id=0}` fallback; active ID alone is not a tracked observation/name |
| Tracked `moves` without owned observation | UNKNOWN, no historical moves/PP or stock catalog values |
| Current owned move observation | VERIFIED, reason `VERIFIED_SOURCE_SYNTHETIC_ONLY`; only observedMoveId/species/side/slot/level |
| Last seen `eL` | UNKNOWN; current level is not proof of a previous observation |
| `FourMovesIfAllKnown` | UNAVAILABLE; no proof of four observed moves/order; no species+level key exposed |
| Empty slot / enemy outside battle | UNAVAILABLE; no species/ability/move defaults |
| End/reset/reload/switch/output/session, no/replayed/replaced/invalid sample, foreign owner/ticket | UNKNOWN/non-ready; no old value or fallback |
| Known unsupported double/multi sample | UNAVAILABLE denial inherited from #711; no current accepted field |
| maxPP/category/power/contextual ability name/nickname/trainer identity | UNKNOWN/unproved; no catalog/party/stock recovery |

Actual persistence identity — loaded output/hash, session/owner, TDAT format,
migration and effective ability semantics — is UNKNOWN. Matching caller
strings never establish it. Real user-notes preservation, review or
reassociation needs a later user decision and runtime evidence.

## Unchanged original getter oracle versus stubs

At Tracker v9.3.1 `c450ecaee2d8131a2789bb656e3be792a93712fb`, Tracker.lua blob
`5e9701f06d1a0450b8311b4d60bceed5ea0adf10`, #707's exact lexical extractor is
reused with four independently frozen reviewed digests:

| Original getter | Lines | SHA-256 of unchanged definition | Note-oracle calls |
| --- | --- | --- | ---: |
| Tracker.getMoves | 387–397 | `8aa1972accd4379dc26dd3a4d29ebdae97304efc2cb43e0b921a03280e8947ec` | 4 |
| Tracker.getAbilities | 402–408 | `ad7f0f3adee3aef83c35ac6716720da635a82323d35925fda842879f5d73f060` | 3 |
| Tracker.getNote | 488–494 | `8e641e5effb5267cc836b9cd572851e6b812aabb824fc1ec3ad9fff2e0cf4cd3` | 3 |
| Tracker.getLastLevelSeen | 520–523 | `8ef4ef42c0bd1db2d707af6f167b60576f45eb9f912472c1ebfe82235d2dcb98` | 3 |

`Tracker.getOrCreateTrackedPokemon` is a read-only synthetic fixture stub
(11 calls); `Battle.inActiveBattle` is a boolean synthetic stub (3 calls).
GhostId=999 is a declared constant stub; ghost branch and catalogs are NOT_RUN.
No stub is counted as original-function coverage. Gate-path original getter,
reader/record/save/load, host read, persistence, renderer and fallback counts
are zero. Counts here belong only to the new note oracle; repeated #707
original execution counts are printed separately.

The original definitions run unchanged in frozen synthetic historical
Tracker.Data/BattleNotes environments. Two separately labeled synthetic
sessions return the same unscoped key `1294*1000+51=1294051` value, move ID 98,
instead of stored move ID 99. Outside battle stored ID 99/PP35 wins. Notes
`STALE_NOTE`, ability 65 and eL88 survive solely by species. Empty note/zero
abilities/empty move list/nil last-seen characterize defaults. These are four
**EXPECTED_STOCK_HAZARD** cases, never accepted current fields.

Source witnesses only: Tracker.lua:583–608 recordBattleMoveByPokemonLevel;
612–615 saveData; 632–676 loadData; 680–697 verifyDataForPlayer; 760+ AutoSave
file-profile/migration paths. New oracle entry points for all these paths are
traps, not original execution. DataHelper.lua:124–412 consumes stored
last-level/abilities/moves, and :448 notes; TrackerScreen.lua:699–720 notes and
1002+ notes/ability editing lead into persistence/UI. DataHelper,
TrackerScreen and BattleDetails remain outside corrected gate consumers.
Full persistence/UI paths, popup/default creation and drawing are NOT_RUN.
The repeated accepted #707 controls retain their intentionally trapped original
save/load/verify entries; these are refused attempts, not successful persistence.

## Isolation, independent oracles and verification

The candidate module is itself compiled into a restricted environment. Its
only bootstrap loader resolves the exact preloaded accepted #711 module; that
loader/debug capability is removed after construction. No runtime loader,
file/process/network/emulator/global/UI capability is present. Forbidden name
resolution or writes throw and increment a counter checked to remain zero on
gate paths. Accepted dependencies are trusted, immutable pure modules loaded
by the source-only Python/Lua bootstrap. #707 sandbox traps remain executed.
Trusted fixture construction adds only frozen-table access and reviewed body
installation; these capabilities are absent inside original function envs.
No original definition body is rewritten or concatenated with adjacent code.

Literal byte fixtures inherit the SHA-locked #711 declarations, without its
test registrations: internal species 1294 vs Dex906, regional1022, player
Pokemon PP7/level50 and BattlePokemon PP2/level51/move33, six rows, direct
species ABI and u16 index stride. Existing bridge regressions independently
assert HP73/11 and PP7/2; the new gate compares current move identity only.
New negatives include wrong species/side/slot/level/encounter, arbitrary text,
zero/mismatching move, metatable/labels, poisoned u16 0x0105, illegal engine
slot6, missing PP caps, invalid occupied species/HP, absent/replayed/replaced
samples, six-to-one, all lifecycle events, unannounced bindings, different
output/session, foreign wrappers/namespaces/restart owners, tickets and aliases.

Use already installed Python 3 and `/opt/homebrew/bin/lua5.4`. Final post-commit
counts/base/head/tree and the PR link are recorded in the PR/handoff.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_note_consumer_mock_tests.py --python-source
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_note_consumer_mock_tests.py --lua /opt/homebrew/bin/lua5.4
```

Also run unchanged Lua runners for host_field_bridge, preconsumer,
host_consumer, extension, party, battle and ui. The composite #713 suite
repeats #707's 63 controls / 13 hazards; each composite #709/#711 also repeats
those controls. Repetition is reported, not treated as distinct new coverage.
Python runs all applicable T1 ParserTests, T2–T5/#707/#709/#711 source checks,
plus #713. Individually excluded only:

- HostConsumerSourceTests.test_exact_four_new_paths_all_gitlinks_and_component_status
- PreconsumerSourceTests.test_exact_five_new_paths_existing_files_and_ten_clean_gitlinks
- HostFieldBridgeSourceTests.test_exact_five_added_paths_all_existing_bytes_and_ten_gitlinks

Each is **NOT_RUN — superseded by #713's exact-five-new-file verifier**.
No historical suite is edited. 21 Clang-dependent LockedProfileTests and
generator `--check` are NOT_RUN (prohibited). Lua5.1, C/Java, ROM generation,
real host/Tracker startup, notes/TDAT, files, emulator/BizHawk, actual rendering,
loaded-output/session/RAM identity, Phase B #691–#694, E2E #695 and freeze #501
remain NOT_RUN/UNKNOWN. No CI execution is claimed; upstream remains deferred.

Development failures are separate from final evidence: initial fixture had a
missing closing table brace (Lua startup parse error, corrected); a subsequent
run had 122 PASS/1 FAIL because hashing a large altered multi.h exhausted the
instruction budget. The negative test now uses a small incorrect source text
and still rejects it through the actual source lock. No safety/fallback failure
was observed. Final post-commit runs supersede development evidence.

## Exactly one next bounded proposal

After CONTROL acceptance and user merge, perform a documentation-only Mac
exit/pre-Linux readiness review of the existing B1 Linux runbook and ordered
#689/#499 → live T2–T5 → #695 gates, with exact pins, unresolved runtime
identity/consumer/notes decisions and sanitized user-run handoff. This is more
useful than further mock-only work because this contract closes the identified
historical-data reintroduction gap in the detached model; remaining uncertainty
requires host evidence and separately authorized real adapters. No new work is
started here, and Linux execution waits for the user's availability signal.
