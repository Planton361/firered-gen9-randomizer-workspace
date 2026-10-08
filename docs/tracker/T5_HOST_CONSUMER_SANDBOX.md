# Pinned Tracker host-consumer sandbox — #707

**Result: characterization PASS, TEST_ONLY; liveConfidence=UNKNOWN; production=DENIED.**
This executes selected original Tracker definitions; it installs no adapter. The final
commit and post-commit results are bound in the PR/handoff, avoiding a self-referential SHA.
CONTROL independent source review is still required before the Issue exit marker.

## Authorized basis and entry decision

[Issue #707](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/707)
and [CONTROL PROCEED](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/707#issuecomment-6058970189)
authorize exactly four new files on `test/tracker-pinned-host-consumer-mock`.
Base/main `c16db3221ca772701c0a38dd0a181f4721ed528e`, tree
`3284e5e68fe7b2e7e5bfe7e158b2185b6903989a`; #706 MERGED, #705 CLOSED/COMPLETED.
Project 4 read-only observation: all 140 items, #707 item
`PVTI_lAHOBYjlAs4BkHQfzg_YFBU`, Doing/P0, sole Doing item; Work Type unset.
CONTROL explicitly waived only that metadata requirement. No Project field was changed
or fabricated, and no material order conflict was reported after that observation.

Product lock `3bdfe9919afc0b7bea55c79f37285e832be495c3` / tree
`f6bc65355811d7de153a91091b223fec9b50991e` remains separate from the newer test basis.
All ten Gitlinks equal the product lock and available checkout HEADs; tracked component
status is clean. CFRU `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2`, DPE
`d887185de1f6ae6a78e85c4311bbadde17041d00`, UPR
`4670a5413104ec02bc08c09ff584470a8a6cb7bd`, Tracker v9.3.1
`c450ecaee2d8131a2789bb656e3be792a93712fb`, NatDexExtension
`a94b8844800308248bb5090b6c36c8b2d7e5d7b9` remain unchanged.
AGENTS/six canonical docs, #705/#706 audit and TSV, #500/#691–#695,
T5_PHASE_A/README/PROFILE_CONTRACT were reviewed as contract/evidence.

## Extraction and isolation

The Python runner reads exactly eight allowlisted public Tracker `.lua` paths,
compares checkout bytes with immutable Git blobs at the pin, and verifies Tracker
HEAD/Gitlink. It never reads or executes Main.lua, the launcher or another module.
A bounded Lua lexer skips comments/quoted/long strings and balances function/if,
for/while-do, standalone do, repeat-until and nested anonymous functions. It
rejects missing/duplicate/unbalanced definitions. Separate Python tests bind all
15 extracted bodies to reviewed line ranges and literal SHA-256 digests.
The runner prints file blob, range and body SHA-256 on every invocation.
This is a reviewed-syntax extractor, not a general Lua compiler or license to
execute arbitrary new source. Pin/content drift fails before Lua starts.

The trusted bootstrap compiles only selected original definitions into a fresh
restricted environment per case. Counter wrappers invoke those original bodies
unchanged. Fixed negative probe strings separately test denied capabilities in
that same environment. The original definitions are not handwritten replacements.
The bootstrap's compiler/debug hook are inaccessible to consumer code. A two-million
instruction budget per case and 30-second subprocess timeout bound execution.

No inherited global environment is supplied. Global reads/writes outside the
allowlist trap, including replacement of existing top-level globals. Namespaces
allow only declared synthetic volatile state after installation; function rewrites
and unknown keys trap. Trusted fixture overrides stay outside the restricted code.
Frozen config/catalog/notes/persistence tables cannot be mutated, including existing
keys; their pairs iterator does not leak its backing table. Standard functions are
explicitly allowlisted. Only the pinned, reviewed code and fixed negative probes
are compiled; this is not an arbitrary untrusted-code execution service.

Memory reads resolve only exact width/address pairs in synthetic 100-byte party
rows and an eight-byte index fixture at symbolic locations 0x1000/0x2000/0x3000.
These are not GBA addresses. The only accepted domain is SYNTHETIC (or omitted,
which names that same synthetic domain). Unknown width/address/domain and truncated
buffers trap. No actual memory backend exists. Every memory write API is refused.
The new harness reads no manifests or source-data JSON and loads no detached extension.
Existing regression runners read only their accepted public source/profile fixtures.

Raw stock results remain untrusted local test objects. Only characterization records
are emitted, labeled TEST_ONLY/liveConfidence=UNKNOWN/production=DENIED. No result
is published into Tracker, persistence, emulator, GUI or a production extension.

## Actual original function coverage

Counts include nested calls and deliberately trapped entries, not just top-level tests.
PASS here means assertions about characterized behavior passed, including hazards.
A trapped entry does not prove the remainder of its function.

| Original function | Pinned file lines | Invocations | Result / execution limit |
|---|---|---:|---|
| `Program.readNewPokemon` | `Program.lua:888–1015` | 33 | PASS literal stock controls + EXPECTED_STOCK_HAZARD direct CFRU bytes |
| `Program.updatePokemonTeams` | `Program.lua:827–886` | 12 | PASS transitions + EXPECTED_STOCK_HAZARD retention/PP; persistence/capture blocked |
| `Program.validPokemonData` | `Program.lua:1432–1453` | 25 | PASS real accessors/selection; no effective gBattleMons reader |
| `Battle.inActiveBattle` | `Battle.lua:112–114` | 74 | PASS real accessors/selection; no effective gBattleMons reader |
| `Battle.getViewedPokemon` | `Battle.lua:257–267` | 8 | PASS real accessors/selection; no effective gBattleMons reader |
| `Battle.updateViewSlots` | `Battle.lua:269–318` | 6 | PASS singles/four-slot synthetic controls + EXPECTED_STOCK_HAZARD u8/clamping/right retention |
| `Battle.beginNewBattle` | `Battle.lua:739–810` | 1 | PASS safety; stopped at createTempSaveState; remainder NOT_RUN |
| `TrackerAPI.getPlayerPokemon` | `TrackerAPI.lua:28–33` | 14 | PASS real accessors/selection; no effective gBattleMons reader |
| `TrackerAPI.getEnemyPokemon` | `TrackerAPI.lua:38–43` | 6 | PASS real accessors/selection; no effective gBattleMons reader |
| `TrackerAPI.getActiveBattlePokemon` | `TrackerAPI.lua:47–59` | 4 | PASS real accessors/selection; no effective gBattleMons reader |
| `Tracker.getPokemon` | `Tracker.lua:105–140` | 36 | PASS real party selection; shared-reference hazard; ghost/egg branches NOT_RUN |
| `Tracker.saveData` | `Tracker.lua:612–615` | 1 | PASS safety; stopped at FileManager.writeTableToFile |
| `Tracker.loadData` | `Tracker.lua:632–676` | 1 | PASS safety; stopped at FileManager.extractFileExtensionFromPath; load/reset/overwrite NOT_RUN |
| `Tracker.verifyDataForPlayer` | `Tracker.lua:680–697` | 2 | PASS safety; first Tracker.Data mutation denied; remainder NOT_RUN |
| `DataHelper.buildTrackerScreenDisplay` | `data/DataHelper.lua:124–412` | 8 | PASS own minimal display; enemy entry traps notes; complete enemy/derived paths NOT_RUN |

### Dependency ownership (no stub is counted as original-function coverage)

`Program.readNewPokemon` uses real byte reads with synthetic address constants,
first two explicitly declared GAEM/GAME permutation entries, pure XOR/getbits,
identity nickname formatting, fixed gender and IV-table dependencies, and a
DefaultPokemon:new stub returning its input. Gender, IV conversion and default
constructor behavior are NOT_RUN. The identity control has personality=OTID=24;
the shuffled control has personality=25, OTID=24 and literal key-1 encrypted words.
Expected species/level/HP/move/PP are literal fixture declarations, never computed
by a second decoder or derived from the target output.

Team update calls the real readNewPokemon and validPokemonData. Positive player
cases use a pure verification stub, fixed EXP results and synthetic catalog validity.
The actual verifyDataForPlayer is exercised separately and in a blocked update.
Gacha/capture mutation is never allowed. Real catalogs, level-up EXP calculation,
full validity semantics outside declared fixtures and production wrapper ownership
are NOT_RUN. The catalogs deliberately label every name/value as synthetic.
Gen9 internal 1294 versus Dex 906 and regional 1022 follow the independently accepted
T3 identity fixtures; this does not validate real stock catalog/resource integration.

DataHelper calls real Battle.getViewedPokemon/inActiveBattle and Tracker.getPokemon.
Remaining dependencies provide deterministic synthetic map/types, baseline species,
move/ability tables, nature multiplier, moves header, route/extras/heals/defaults,
empty tracked moves, no associated GachaMon and disabled variable damage/effectiveness.
Unknown current ability is deliberately separate from the supplied static selection.
Completed own paths use four move slots. No stock UI, genuine note read, randomizer
binding, damage/catch/EXP computation, hidden-power or resource/rendering acceptance
follows. An enemy path reaches and is blocked at Tracker.getAbilities.

## Negative cases and stock findings

All 13 EXPECTED_STOCK_HAZARD cases are successful characterization assertions,
**not corrected functionality**. The expected hazard must be observed exactly;
a changed or missing observation fails the case.

| Case | Independently expected observation | Required adapter |
|---|---|---|
| Direct CFRU row / nonzero key | Declared internal species 1294 becomes stock-decoded 1295 | Direct CFRU layout and guarded reader |
| Invalid occupied species | Both prior player/enemy table references remain | Clear/rebuild invalid slots atomically |
| Invalid held item/move | Prior player row remains | Field validity and fail-closed clearing |
| Enemy outside battle | Declared current PP 7 becomes static maximum 35 | Effective PP ownership; no baseline substitution |
| Missing static maximum | PP becomes nil | Explicit UNKNOWN max-PP/effective fields |
| u16 index 0x0105 | Stock reads only low byte 5, chooses slot 6 | Read u16 and reject 261 |
| Invalid zero-based slot 6 | Stock clamps to lead slot 1 | Reject invalid slot, no fabricated default |
| Four to two battlers | Prior RightOwn slot 6 survives | Context/transition clearing |
| API active objects | Party HP 73 returned versus declared active HP 11; returned-table mutation changes team | Effective battle snapshot plus copy boundary |
| Battle end | Active list empty, enemy party API still returns prior row | Explicit party/battle freshness/epoch gate |
| Reset/output/session stimuli | Team replacement cannot revoke old table references | Snapshot ownership and epoch invalidation |
| Unknown contextual ability | Static synthetic ability name is displayed | Effective/contextual ability trust |
| Missing effective move fields | Static category/power displayed; max PP absent | Per-field effective-data and derived-view gates |

Literal GAEM/XOR/GAME controls, six-to-one/empty transitions, internal/Dex distinction,
regional ID/types, invalid API slots, four-party selection, missing catalog category,
invalid-map hiding and move-table copy isolation also PASS. Safe UNKNOWN behavior
from our existing detached modules does not establish these stock adapters.

Reset/output/session tests explicitly replace synthetic owner tables and query the
real API. They DO NOT invoke or prove actual Tracker reset/output/session hooks.
The foreign wrapper fixture proves only fresh-environment separation and preserving
another environment's function; live wrapper install/unload remains NOT_RUN.

## Safety evidence

There are **47 distinct confirmed trap identifiers and 56 rejected invocations**.
Every refused operation is asserted to fail with its specific TRAP identifier,
not merely a generic exception. Confirmed categories:

- `Memory.writebyte`, lower-case memory u8/u16/u32/array writes;
- unapproved read address/width, foreign domain and truncation;
- file write/read/load path helpers, io.open, os.execute, socket/http, package.loadlib;
- savestate.save/load and actual Battle.beginNewBattle -> createTempSaveState;
- actual Tracker.saveData/loadData/verifyDataForPlayer entry traps;
- Tracker.Data/Tracker.BattleNotes writes and Gacha capture persistence entry;
- emulator frameadvance, event callbacks, client, forms, GUI and CustomCode callbacks;
- require/load/loadfile/dofile/loadstring, raw access/metatable/debug reflection, _G;
- unknown/global replacement, config/math mutation, unauthorized function replacement.

Battle.beginNewBattle is stopped before memory reads and afterBattleBegins; the
late hook is therefore insufficient to protect the stock save-state entry.
Tracker.loadData is blocked even before file-extension validation; actual successful
load, reset, hash/overwrite and migration are NOT_RUN. No host function exists behind
any trap. Fixed hostile compiled probes additionally exercise real restricted name
resolution and deny file/process/module/memory/state/persistence/global writes.

## Explicit NOT_RUN source witnesses

Only inventory (immutable blobs compared; Python witness assertions), no renderer:
`TrackerScreen.lua:1102–1125 drawScreen` calls updateButtonStates, Drawing background,
DataHelper display builder, info/stats/carousel/moves/favorites/ball-picker paths.
It consumes independently built data and calls Tracker.getPokemon directly.
Adapting TrackerAPI alone cannot cover it.

`BattleDetailsScreen.lua:458 SCREEN.updateData` fans out to field/status2/status3,
side/disable/wish consumers. Direct reads are visible at 743 (terrain), 759–760
(weather), 879 (gBattleMons status2), 1113 (gStatuses3), 1287 (gSideStatuses) and
1433 onward (disable/wish). These depend on SCREEN-local structures, contextual
addresses, pagination and callbacks not supplied by this minimal sandbox. Execution
is NOT_RUN; no fake BattleDetails function replaces them. Future ownership must gate
these direct consumers before any read and clear their paged data on invalidation.

`Tracker.lua:583 recordBattleMoveByPokemonLevel` uses species*1000+level note keys;
612/632/680 save/load/verification entries are trapped as above. Full notes record,
load/reset/migration/overwrite and endCurrentBattle (Battle.lua:812) are NOT_RUN.
They need profile/output/session-scoped persistence quarantine and early save-state
suppression, with ownership-safe wrappers. Real reset and output identity remain
UNKNOWN. A separate contract must implement those adapters before runtime evidence.

## Verification commands and results

Python 3.9.6 and installed Lua 5.4.9; no installation. Execute at Workspace root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_host_consumer_mock_tests.py --lua /opt/homebrew/bin/lua5.4
(cd 07_scripts/tracker && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_cfru_dpe_host_consumer_source test_cfru_dpe_extension_source test_cfru_dpe_party_source test_cfru_dpe_battle_source test_cfru_dpe_ui_source test_generate_cfru_dpe_source_data.ParserTests -v)
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_extension_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_party_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_battle_mock_tests.py --lua /opt/homebrew/bin/lua5.4
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/tracker/run_cfru_dpe_ui_mock_tests.py --lua /opt/homebrew/bin/lua5.4
python3 07_scripts/bootstrap/check_git_safety.py
git diff --check
```

| Test class | PASS | FAIL | EXPECTED_STOCK_HAZARD included in PASS | NOT_RUN |
|---|---:|---:|---:|---|
| New party | 12 | 0 | 5 | Full real stock catalogs/defaults/gender/IVs |
| New battle | 5 | 0 | 3 | Full context/reset/end/lifecycle hooks |
| New API | 5 | 0 | 3 | Real gBattleMons/output/session adapters |
| New display | 6 | 0 | 2 | Full enemy/derived paths, renderer/BattleDetails |
| New safety | 35 | 0 | 0 | Actual host/file/state/persistence effects |
| New Python source/isolation | 7 | 0 | 0 | None in its bounded source scope |
| Existing T2–T5 Python + parser | 22 | 0 | 0 | Generator --check / 21 LockedProfileTests (Clang frontend) |
| Existing lifecycle/party/battle/UI Lua | 55 / 43 / 76 / 63 | 0 | 0 | Lua 5.1 unavailable; real host |

New Lua total **63 PASS / 0 FAIL**, with **13 expected hazards**. Old Lua total
**237 PASS**; total Lua 300. Python total **29 PASS**, no failures/errors/skips.
The final PR records reruns against the committed revision. No Java/C compilation,
generation, ROM/build/save/state access, real manifests, binary inspection, emulator,
BizHawk or normal Tracker startup occurs. Lua 5.1 and all live acceptance are NOT_RUN.

Git safety, exact four new paths, whitespace, base/HEAD and product-lock Gitlinks,
all checkout heads/clean tracked status are checked. CASUAL_NATDEX.rnqs remains
unread, unstaged and untouched. Existing production guard/implementations/tests and
components are byte-identical to the accepted base. No automatic Issue closure.

## One next CONTROL step

Review this exact delivered revision, original-source provenance, fixture oracles,
trap results and NOT_RUN boundaries for #707 characterization acceptance. Any later
adapter implementation requires its own bounded contract; live gates #499/#689 and
#691–#695 remain unaccepted. Production DENIED; UPSTREAM_CONTRIBUTION DEFERRED.

## Complete direct dependency inventory of extracted definitions

This lexical inventory lists capitalized/global property paths in the exact original
bodies, including branches NOT_RUN. Local row members are omitted. Standard builtins
are covered by the allowlist above. Each unprovided call traps; inclusion is not
execution coverage. Body hashes/ranges are fixed independently in the Python suite.

- `Program.readNewPokemon`: `Constants.HIDDEN_INFO`, `GameSettings.GameCharMap`, `GameSettings.game`, `Memory.readbyte`, `Memory.readdword`, `MiscData.TableData.attack`, `MiscData.TableData.effort`, `MiscData.TableData.growth`, `MiscData.TableData.misc`, `MiscData.getMonGender`, `Program.Addresses.nicknameCharEnd`, `Program.Addresses.offsetPokemonStatsDefSpe`, `Program.Addresses.offsetPokemonStatsLvCurHp`, `Program.Addresses.offsetPokemonStatsMaxHpAtk`, `Program.Addresses.offsetPokemonStatsSpaSpd`, `Program.Addresses.offsetPokemonStatus`, `Program.Addresses.offsetPokemonSubstruct`, `Program.Addresses.sizeofPokemonNickname`, `Program.DefaultPokemon:new`, `Program.Values.ShinyOdds`, `Program.readNewPokemon`, `Utils.bit_xor`, `Utils.convertIVNumberToTable`, `Utils.formatSpecialCharacters`, `Utils.getbits`.
- `Program.updatePokemonTeams`: `Battle.inActiveBattle`, `GachaMonData.tryAddToRecentMons`, `GameSettings.estats`, `GameSettings.pstats`, `Memory.readdword`, `MoveData.Moves`, `Program.Addresses.sizeofPokemonStruct`, `Program.GameData.EnemyTeam`, `Program.GameData.PlayerTeam`, `Program.getNextLevelExp`, `Program.readNewPokemon`, `Program.updatePokemonTeams`, `Program.validPokemonData`, `Tracker.Data.isNewGame`, `Tracker.verifyDataForPlayer`.
- `Program.validPokemonData`: `MiscData.getTotalItems`, `MoveData.isValid`, `PokemonData.isValid`, `Program.validPokemonData`.
- `Battle.inActiveBattle`: `Battle.dataReady`, `Battle.inActiveBattle`, `Battle.inBattleScreen`.
- `Battle.getViewedPokemon`: `Battle.Combatants.LeftOther`, `Battle.Combatants.LeftOwn`, `Battle.Combatants.RightOther`, `Battle.Combatants.RightOwn`, `Battle.getViewedPokemon`, `Battle.inActiveBattle`, `Battle.isViewingLeft`, `Battle.isViewingOwn`, `Tracker.getPokemon`, `Utils.inlineIf`.
- `Battle.updateViewSlots`: `Battle.BattleParties`, `Battle.Combatants.LeftOther`, `Battle.Combatants.LeftOwn`, `Battle.Combatants.RightOther`, `Battle.Combatants.RightOwn`, `Battle.changeOpposingPokemonView`, `Battle.numBattlers`, `Battle.resetAbilityMapPokemon`, `Battle.updateViewSlots`, `GameSettings.gBattlerPartyIndexes`, `Memory.readbyte`, `Utils.inlineIf`.
- `Battle.beginNewBattle`: `Battle.AbilityChangeData.prevAction`, `Battle.AbilityChangeData.recordNextMove`, `Battle.Combatants`, `Battle.Synchronize.attacker`, `Battle.Synchronize.battlerTarget`, `Battle.Synchronize.turnCount`, `Battle.beginNewBattle`, `Battle.damageReceived`, `Battle.dataReady`, `Battle.enemyHasAttacked`, `Battle.firstActionTaken`, `Battle.inBattleScreen`, `Battle.isGhost`, `Battle.isViewingLeft`, `Battle.isViewingOwn`, `Battle.isWildEncounter`, `Battle.opposingTrainerId`, `Battle.partySize`, `Battle.populateBattlePartyObject`, `Battle.prevDamageTotal`, `Battle.recentBattleWasTutorial`, `Battle.trySwapScreenBackToMain`, `Battle.turnCount`, `CustomCode.afterBattleBegins`, `GachaMonData.clearNewestMonToShow`, `GameOverScreen.createTempSaveState`, `GameOverScreen.isDisplayed`, `GameSettings.gBattleTypeFlags`, `GameSettings.gPlayerPartyCount`, `GameSettings.gTrainerBattleOpponent_A`, `GameSettings.game`, `Memory.readbyte`, `Memory.readdword`, `Memory.readword`, `Program.Frames.Others`, `Tracker.getPokemon`, `Tracker.resetBattleNotes`, `Tracker.tryTrackWhichRival`, `Utils.getbits`.
- `TrackerAPI.getPlayerPokemon`: `Battle.Combatants.LeftOwn`, `Battle.inActiveBattle`, `Tracker.getPokemon`, `TrackerAPI.getPlayerPokemon`.
- `TrackerAPI.getEnemyPokemon`: `Battle.Combatants.LeftOther`, `Battle.inActiveBattle`, `Tracker.getPokemon`, `TrackerAPI.getEnemyPokemon`.
- `TrackerAPI.getActiveBattlePokemon`: `Battle.Combatants.LeftOther`, `Battle.Combatants.LeftOwn`, `Battle.Combatants.RightOther`, `Battle.Combatants.RightOwn`, `Battle.inActiveBattle`, `Battle.numBattlers`, `TrackerAPI.getActiveBattlePokemon`, `TrackerAPI.getEnemyPokemon`, `TrackerAPI.getPlayerPokemon`.
- `Tracker.getPokemon`: `Battle.isGhost`, `Program.GameData.EnemyTeam`, `Program.GameData.PlayerTeam`, `Tracker.getGhostPokemon`, `Tracker.getPokemon`.
- `Tracker.saveData`: `FileManager.writeTableToFile`, `QuickloadScreen.getGameProfileTdatPath`, `Tracker.Data`, `Tracker.saveData`.
- `Tracker.loadData`: `FileManager.Extensions.TRACKED_DATA:sub`, `FileManager.extractFileExtensionFromPath`, `FileManager.readTableFromFile`, `GameSettings.getRomHash`, `QuickloadScreen.getGameProfileTdatPath`, `Tracker.Data`, `Tracker.LoadStatus`, `Tracker.LoadStatusKeys.ERROR`, `Tracker.LoadStatusKeys.LOAD_SUCCESS`, `Tracker.LoadStatusKeys.NEW_GAME`, `Tracker.checkForLegacyTrackedData`, `Tracker.loadData`, `Tracker.resetData`, `Utils.isNilOrEmpty`.
- `Tracker.verifyDataForPlayer`: `Tracker.Data.isNewGame`, `Tracker.Data.playtime`, `Tracker.Data.trainerID`, `Tracker.resetData`, `Tracker.verifyDataForPlayer`.
- `DataHelper.buildTrackerScreenDisplay`: `AbilityData.Abilities`, `AbilityData.isValid`, `Battle.getDoublesCursorTargetInfo`, `Battle.getViewedPokemon`, `Battle.inActiveBattle`, `Battle.isGhost`, `Battle.isViewingLeft`, `Battle.isViewingOwn`, `Battle.isWildEncounter`, `Constants.BLANKLINE`, `Constants.HIDDEN_INFO`, `Constants.OrderedLists.STATSTAGES`, `GachaMonData.getAssociatedRecentMon`, `GachaMonData.hasNewestMonToShow`, `MiscData.Items`, `MiscData.StatusCodeMap`, `MoveData.BlankMove`, `MoveData.BlankMove.name`, `MoveData.HIDDEN_POWER_NOT_SET`, `MoveData.IsRand.moveAccuracy`, `MoveData.IsRand.movePP`, `MoveData.IsRand.movePower`, `MoveData.IsRand.moveType`, `MoveData.Moves`, `MoveData.Values.HiddenPowerId`, `MoveData.adjustVariableMoveValues`, `MoveData.getCategory`, `MoveData.isValid`, `PokemonData.BlankPokemon`, `PokemonData.Evolutions.FRIEND`, `PokemonData.Evolutions.FRIEND_READY`, `PokemonData.IsRand.types`, `PokemonData.Pokemon`, `PokemonData.Types.UNKNOWN`, `PokemonData.Values.DefaultBaseFriendship`, `PokemonData.Values.GhostId`, `PokemonData.calcCatchRate`, `PokemonData.canShowUnknownAbilities`, `PokemonData.canShowUnknownMoveLearnSets`, `PokemonData.canShowUnknownStats`, `PokemonData.getAbilityId`, `PokemonData.isGameDataRandomized`, `Program.GameData.Items.healingPercentage`, `Program.GameData.Items.healingTotal`, `Program.GameData.Items.healingValue`, `Program.GameData.friendshipRequired`, `Program.GameData.mapId`, `Program.getExtras`, `Program.getPokemonTypes`, `Program.isValidMapLocation`, `RouteData.Info`, `RouteData.hasRoute`, `Tracker.Data.centerHeals`, `Tracker.Data.hasCheckedSummary`, `Tracker.getAbilities`, `Tracker.getDefaultPokemon`, `Tracker.getEncounters`, `Tracker.getHiddenPowerType`, `Tracker.getLastLevelSeen`, `Tracker.getMoves`, `Tracker.getPokemon`, `Utils.calculateMoveStars`, `Utils.formatSpecialCharacters`, `Utils.getMovesLearnedHeader`, `Utils.getNatureMultiplier`, `Utils.isNilOrEmpty`, `Utils.isSTAB`, `Utils.netEffectiveness`, `Utils.toLowerUTF8`.
