# Diagnose 162: In-Game Trades writer preserve test plan

## Scope

This is a read-only plan for a later small ROM-free Gen3 writer preserve test for the In-Game Trades null/invalid Species guard.

No test code is written. No build, Randomizer run, ROM smoke, ROM file, save, emulator state, output ROM, log, Randomizer JAR, tool binary, private path, hash, secret, token or `.env` file is touched.

## Preconditions

- Workspace PR #206 / Follow-up 161B is merged into `main`.
- Workspace branch: `test/upr-fvx-cfru-dpe-ingame-trades-writer-preserve-test-plan`.
- UPR-FVX submodule pin remains `1eaee2873cd69682335223f817b124bf36d004f2`.
- PR #40 added the non-ROM `TradeRandomizerTest` mutation-guard harness.
- In-Game Trades remain `blocked-pending-evidence`; no ROM-Smoke or Species-Write-Smoke is authorized.

## Plan result

Classification: `writer-test-plan-ready`.

A small ROM-free writer preserve test is worth doing, but it should not try to construct a full ROM-backed `Gen3RomHandler`. The current writer guard is in the right place, but the useful test needs one narrow seam because the relevant guard helpers and handler state are private.

Recommended later implementation: add a tiny `:romio:test` unit test around a package-visible or extracted Gen3 In-Game-Trade row write decision. The test should prove that unsafe rows return before any byte write and leave a synthetic in-memory byte buffer unchanged.

Without that seam, a direct test would be brittle because it would need reflection into private `Gen3RomHandler` fields such as `romEntry`, `pokesInternal`, `pokedexToInternal`, text tables and the backing ROM byte array.

## Read-only writer findings

Reviewed file:

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

`setInGameTrades(...)` reads `TradeTableOffset`, `TradeTableSize`, `TradesUnused`, iterates 60-byte rows and advances through modeled non-unused `InGameTrade` entries.

For each non-unused row, the writer does:

1. `InGameTrade trade = trades.get(tradeOffset++)`
2. `if (!canWriteInGameTrade(trade)) { continue; }`
3. only then writes nickname, given Species, IVs, OT ID, held item, OT name and requested Species

The preserve guard therefore runs before all row byte writes. Unsafe rows are skipped before fixed-length text writes, Species writes, IV writes, OT ID writes, held-item writes, OT-name writes and requested-Species writes.

`canWriteInGameTrade(...)` rejects null trades and delegates both given and requested Species to `canWriteInGameTradeSpecies(...)`.

`canWriteInGameTradeSpecies(...)` rejects:

- null Species
- Species number `<= 0`
- Species number outside `pokedexToInternal`
- null Species names
- placeholder names: `Bad Egg`, `?`, names containing `unused`
- internal Species mappings `<= 0`
- mappings outside `pokesInternal`
- mappings whose `pokesInternal[internalSpecies] == null`

## Read-only test-structure findings

Existing tests:

- `random/src/test/java/com/uprfvx/random/randomizers/TradeRandomizerTest.java` now covers the ROM-free mutation guard.
- `romio/src/test/java/com/uprfvx/romio/romhandlers/RomHandlerIngameTradeTest.java` exists, but extends ROM-dependent `RomHandlerTest` and loads ROM fixtures.
- `romio/build.gradle.kts` excludes `*RomHandler*Test` from normal `:romio:test` and routes them to `testROMs`.
- `romio/src/testFixtures/java/com/uprfvx/romio/romhandlers/RomHandlerTest.java` is fixture infrastructure for ROM-backed tests, not suitable for this plan.
- No ROM-free Gen3 writer unit test for In-Game Trades exists in `romio/src/test`.

## Recommended writer-test scope

Recommended later UPR-FVX branch:

- add a ROM-free unit test under `romio/src/test/java/com/uprfvx/romio/romhandlers/`, for example `Gen3InGameTradeWriterTest.java`
- keep it in normal `:romio:test`, not `testROMs`
- use synthetic `InGameTrade` rows only
- use synthetic Species objects and minimal mapping arrays or a tiny extracted predicate/row-writer helper
- use an in-memory byte array with sentinel bytes if row-write preservation is tested directly

Target assertions:

- `requestedSpecies == null` is rejected before row write
- placeholder Species such as `Bad Egg` or `?` are rejected before row write
- out-of-mapping Species are rejected before row write
- the writer decision reports skipped/preserved for unsafe rows
- synthetic row bytes remain unchanged for skipped rows
- no nickname, OT, IV or held-item write is exercised or promoted

Safe rows should stay out of the first writer-preserve test unless the seam makes a fully synthetic positive-path row trivial. This plan is about proving the unsafe-row preserve branch, not authorizing valid active row writes.

## Minimal seam recommendation

The smallest acceptable seam is one of:

- make the Gen3 In-Game-Trade write eligibility helper package-visible and directly unit-testable, plus keep a code-review assertion that `setInGameTrades(...)` calls it before writes
- better: extract a package-visible row helper that returns `false` before any byte write when `canWriteInGameTrade(...)` fails, allowing a byte-array unchanged assertion

Do not introduce a broad handler test harness, public API, ROM fixture, save/reload path or writer refactor. Do not expose text, Nickname/OT, IV or Trade Held Item behavior.

## Why this is small

The production behavior already has the correct ordering: guard before byte writes. A later test should only make that ordering observable without ROM files.

The test is small if it limits itself to:

- one unsafe null-request row
- one unsafe placeholder Species row
- one unchanged synthetic row-buffer assertion
- optional predicate-only assertions for out-of-range Species mappings

The test becomes blocked if it needs to construct a real `Gen3RomHandler` through ROM detection/loading, populate private handler state through reflection, use ROM fixtures, or change unrelated writer architecture.

## Stop criteria for a later code-test PR

Stop the later implementation if any of these become necessary:

- ROM file, save file, emulator state, output ROM, log, Randomizer JAR, tool binary, private path or hash
- `:romio:testROMs`, Randomizer CLI/GUI, ROM-Smoke or Species-Write-Smoke
- broad `Gen3RomHandler` refactor
- public API added only for tests
- reflection into private ROM handler state as the main test strategy
- text, Nickname/OT, IV or Trade Held Item randomization changes
- valid active-row Species write promotion
- Workspace code changes outside the follow-up documentation block

## Allowed checks in a later code-test PR

Allowed for a later explicitly scoped UPR-FVX test PR:

- `./gradlew --offline :romio:test`
- `./gradlew --offline :random:test`
- `git status --short`
- `git diff --stat`
- `git diff --check`
- focused `rg` checks for `Gen3RomHandler`, `InGameTrade`, `requestedSpecies`, `preserve`, `skip`, `TradeRandomizerTest`

## Status

In-Game Trades remain `blocked-pending-evidence`.

This plan makes a ROM-free writer preserve test ready as the next narrow evidence step. It does not authorize code changes in this workspace block, does not authorize ROM-facing smoke, and does not promote any In-Game Trade subfeature.
