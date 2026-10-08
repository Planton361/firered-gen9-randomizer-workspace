# #709 — early pre-consumer guard, synthetic host only

**TEST_ONLY; liveConfidence=UNKNOWN; production=DENIED.** This candidate
intercepts four actual pinned Tracker functions through a restricted synthetic
function-table facade. It never delegates to them, including in accepted mock
sessions. No production entrypoint imports this module. CONTROL review and user
merge remain separate; no live acceptance or Issue #500/#691–#695 closure follows.

Contract: [#709](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/709).
Base/main `e7485c591c46e4e0ca06b236fc7339bbe0453731`, tree
`343e9f0e6064820ef9caa5d3f8a09910e22343d1`; fresh branch
`feature/tracker-preconsumer-guard-mock`, one writer. Final head, executed
post-commit commands/results and PR link are recorded in the PR/handoff instead
of a self-referential commit identifier here.

## Entry evidence and exact boundary

AGENTS.md, six canonical files, #500/#691–#695, #707 including CONTROL review,
T2–T5 records, PROFILE_CONTRACT and the pinned original function bodies were
read. Live main/tree, all ten Gitlinks and clean component checkouts matched.
The known untracked `CASUAL_NATDEX.rnqs` is explicitly excepted by #709 and
remains unread, untouched and unstaged.

Actual Project 4 observation on 2026-10-08: 141 items; #709 item
`PVTI_lAHOBYjlAs4BkHQfzg_ZLE4`, position 141, Status/Priority/Work Type unset;
#707 position 140, Done/P0, CLOSED. No Doing/In Progress item or competing
eligible OPEN active work was observed. Remaining parent/live/E2E work is
backlog or host-gated. The explicit single CONTROL routing in #709 authorizes
this bounded preparation; optional Work Type is nonblocking. No Project field
was changed and no Doing/P0 field success is claimed.

Exactly five new files: `source_preconsumer_guard.lua` in the extension;
`run_cfru_dpe_preconsumer_mock_tests.py`, `test_cfru_dpe_preconsumer_source.py`
and `tests/cfru_dpe_preconsumer_mock.lua` in `07_scripts/tracker/`; this document.
All existing files, production guard, generator/profile, T3/T4/T5 modules,
#707 harness and component source remain byte-identical.

Locked product `3bdfe9919afc0b7bea55c79f37285e832be495c3`, tree
`f6bc65355811d7de153a91091b223fec9b50991e`, is distinct from the test base.

| Gitlink | Exact unchanged SHA |
| --- | --- |
| CFRU-expansion | `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2` |
| Dynamic-Pokemon-Expansion-Gen-9 | `d887185de1f6ae6a78e85c4311bbadde17041d00` |
| Ironmon-Tracker v9.3.1 | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| references/cyansmp64-pokefirered-natdex | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| references/cyansmp64-upr-zx-natdex | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` |
| references/pret-pokefirered | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |
| references/upr-fvx-upstream | `e0788edc6529c2605f201996e4807ff30165354c` |
| references/upr-zx-ajarmar | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` |
| upr-fvx | `4670a5413104ec02bc08c09ff584470a8a6cb7bd` |

## Ownership and invalidation contract

`newMock(host, expected, bodies, publicJson, publicSources, multiText)` accepts
plain, allowlisted synthetic function tables. Expected function references must
match the current slots. All four original body digests are literal reviewed
#707 digests; public profile/source locks come from the unchanged T3/T4 factories.
Wrong serialized profile/schema/pin/source bytes or foreign wrappers reject
construction. The public JSON hash is
`8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981`, profile ID
`sha256:31be9e07697f939b274c56eea5d92a81dd10c43e7c876586effccb335535ca75`.
Only exact immutable accepted strings are cached, never caller profile objects.

`installMock()` first stages owned deny-only stops at all four validated seams
without callbacks/yields, then installs updatePokemonTeams, readNewPokemon,
updateViewSlots and beginNewBattle data guards all or none, with reference read-back. The only injection API
is an explicit synthetic throw/drop stage 1–4; there is no importer or arbitrary
callback. Failure restores only owned staging stops and permanently closes that
adapter: zero active data guards, four safe stops, no stock fallback even through
direct calls. A separate restart tombstone remains on
the synthetic `Lifecycle.startTracker`; it never calls a stock initializer.
This safety stop is outside the four-function data-wrapper transaction.

After successful install every call checks all four owners, the namespace
references, the restart owner and the complete synthetic session declaration.
There is no composition with foreign wrappers. Teardown revokes tickets and
replaces only still-owned wrappers with deny-only tombstones, preserving later
foreign replacements. It deliberately retains stops for the selected unknown
profile. Duplicate install/teardown/factory attempts cannot reopen vanilla paths.
Cached originals or later foreign code called directly are outside mediation;
this prototype cannot constrain another owner's execution. Restart/namespace
reconstruction and real unload detection remain live-host work.

Each start/end/switch/reset/reload/output/session event clears current data and
advances a monotonic epoch. Recovery uses an exact allowlisted `SYNTHETIC_ONLY`
declaration with profile/pin/output/session/encounter/epoch matching the mock
host. No caller `trusted`/`validated` boolean is accepted. Synthetic declarations
are deterministic fixtures, never proof of a real loaded output. End/reset/reload
stay disarmed; only explicit start/switch/session/output can arm fresh decoding.

`submitMock` requires matching before/after context, increasing sample ID,
600-byte direct-layout player/enemy parties and coherent T4 singles when in an
encounter. u16 indices must select occupied side-specific party slots. Invalid
occupied fields, active rows, PP/caps, unknown flags, unsupported doubles/multi,
replay or session drift revoke readiness. Outside an encounter there is no enemy
view or static PP substitution. Caller trainer trust declarations are rejected;
trainer identity stays UNKNOWN/UNAVAILABLE.

Wrappers return typed UNKNOWN or opaque revocable tickets. `readMock(ticket)`
rechecks current ownership/session/epoch and returns a fresh historical copy.
Old tickets cannot retrieve stale data. Already-read copies carry their sample
epoch and are historical values, not live views; mutations cannot affect the
adapter or stock teams. Confidence fields remain source/synthetic, stamped
TEST_ONLY. Party and active HP/PP are distinct. Contextual ability names,
effective move power/category and max-PP derivation remain unproved. The module
does not construct DefaultPokemon, update GameData/Combatants/Trainer, render,
or read/write notes, memory, files or save states.

## Original-source execution and early safety evidence

The new runner reuses #707's immutable extraction/invocation implementation.
Its 15 independently hashed original bodies are unchanged. It checks the exact
accepted #707 bootstrap hash
`2bd09683acd3b6b95012c35cfda85aa7b84dc569518c0d42e9489556b4dfe48c`
and all 63 original control registrations, including 13 EXPECTED_STOCK_HAZARD
assertions. Each run prints original pin/blob/line range/body digest.

Two reviewed bootstrap-only changes in memory allow pure string byte/gsub/gmatch
methods needed by T3/T4 and a trusted synthetic namespace fixture setter for
the late-hook control. No original body is rewritten. string.dump, loaders,
reflection, global mutation, IO/process/network, write/read-address traps and
all other #707 denials remain exercised. The guard loads only existing pure
T3/T4/SHA modules before constructing restricted stock environments. Full
source hashing is warmed before the bounded test driver; only exact-string
cache hits are reused. A subprocess timeout and per-case instruction limit
bound execution; no host backend exists.

The negative control installs a real synthetic `afterBattleBegins` hook and
invokes the actual pinned `beginNewBattle`. The pre-hook save-state trap fires,
with original invocation count 1 and late-hook count 0. This is a refused attempt,
not successful state creation. Guarded calls assert zero original invocations,
zero host reads and zero forbidden attempts, rather than catching damage later.

| Original function | Unguarded controls | Guarded original calls |
| --- | ---: | ---: |
| Program.readNewPokemon | 33 | 0 |
| Program.updatePokemonTeams | 12 | 0 |
| Program.validPokemonData | 25 | 0 |
| Battle.inActiveBattle | 74 | 0 |
| Battle.getViewedPokemon | 8 | 0 |
| Battle.updateViewSlots | 6 | 0 |
| Battle.beginNewBattle | 2 (one prior control + installed-late-hook control) | 0 |
| TrackerAPI.getPlayerPokemon / getEnemyPokemon / getActiveBattlePokemon | 14 / 6 / 4 | 0 |
| Tracker.getPokemon | 36 | 0 |
| Tracker.saveData / loadData / verifyDataForPlayer | 1 / 1 / 2 | 0 |
| DataHelper.buildTrackerScreenDisplay | 8 | 0 |

The 13 stock hazards retain #707's independent expected values: XOR species
1295 instead of direct 1294, invalid occupied-row retention, static enemy PP
35/nil, poisoned u16 0x0105 and slot-6 clamping, 4→2 stale right slot, party versus
active HP, alias mutation, stale enemy/session references and baseline ability/
move substitution. Guard negative cases reject corresponding malformed/stale
samples before all four original entries; corrected controls decode direct
1294, keep party HP 73 versus active 11 and stored PP 7 versus active 2, clear
unused slots and keep effective names/category/power UNKNOWN. Independent
internal Gen1/Gen8/Gen9/regional controls and copy/ticket isolation also execute.

## Verification and limits

Use existing Python and `/opt/homebrew/bin/lua5.4`; no installation. Final
post-commit counts, guarded entry counts and actual commands are in the PR.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_preconsumer_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_host_consumer_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_extension_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_party_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_battle_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_ui_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 07_scripts/bootstrap/check_git_safety.py
git diff --check
```

Run all new Python checks and applicable prior T2–T5/#707 source checks plus
T1 ParserTests. The #707 historical `test_exact_four_new_paths...` is NOT_RUN:
its prior-contract four-path allowlist excludes this contract's five new files.
The new five-file test independently enforces existing-byte and all-ten-pin/
checkout boundaries. Full LockedProfileTests and generator `--check` require
Clang and remain NOT_RUN as #709 requires. Python compilation uses in-memory
`compile`, producing no build/bytecode artifacts.

Pre-final development run: 128 assertions PASS, one FAIL from the fixture's
instruction budget when four namespace scenarios were combined in one case;
no incorrect original delegation or host side effect occurred. The scenarios
were split into independently budgeted cases. Final execution evidence supersedes
that development result and must report any further FAIL honestly.

Lua 5.1, real C/Java/Clang generation, ROM/build/save/state access, local
manifests/addresses, emulator execution, real Tracker field bridge/UI/persistence,
live lifecycle/output/session validation, #689/#499 host, #691–#694 Phase B,
#695 E2E and #501 freeze are NOT_RUN. Production DENIED; upstream deferred.
Source/mock PASS is neither working normal Tracker UI nor live wrapper safety.

## Exactly one next bounded Mac proposal

After CONTROL reviews this early interposer evidence: a ROM-free,
source-correct party/battle-to-host field bridge with per-field confidence and
explicit unknown effective values, under a separate bounded contract. No
implementation or activation of that proposal is authorized by this PR.
