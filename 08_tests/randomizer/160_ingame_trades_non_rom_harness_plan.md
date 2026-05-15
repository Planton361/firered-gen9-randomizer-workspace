# Diagnose 160: In-Game Trades non-ROM harness plan

## Scope

This is a read-only plan for a later small non-ROM harness or unit-test scope for the UPR-FVX In-Game Trades Null-/Invalid-Species guard.

No harness code is written. No build, Randomizer run, ROM smoke, ROM file, save, emulator state, output ROM, log, Randomizer JAR, tool binary, private path, hash, secret, token or `.env` file is touched.

## Preconditions

- Workspace PR #204 / Diagnose 159 is merged into `main`.
- Workspace branch: `test/upr-fvx-cfru-dpe-ingame-trades-non-rom-harness-plan`.
- UPR-FVX submodule pin remains `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Diagnose 159 result is `review-pass-with-risks`.

## Plan result

Classification: `harness-plan-ready`.

A small non-ROM harness is worth doing and can be kept bounded. The first useful test should target `TradeRandomizer.randomizeIngameTrades()` with synthetic `InGameTrade` rows and a fake/test `RomHandler` implementation. This covers the highest-risk behavior without a ROM file:

- unsafe rows skip before mutation
- all-skipped input does not call `setInGameTrades(...)`
- `changesMade=false` remains possible
- skip counters are observable through `getSkippedNullRequestedSpeciesTrades()`, `getSkippedUnsafeSpeciesTrades()` and `hasSkippedTrades()`

A writer preserve/skip assertion for `Gen3RomHandler.setInGameTrades(...)` is also useful, but it should be a second, narrower step only if it can be exposed without ROM bytes, broad refactor or private-path fixtures.

## Read-only test-structure findings

The UPR-FVX submodule already has JUnit-based module tests:

- root Gradle config applies JUnit Jupiter `5.10.0`
- `random/src/test/java/com/uprfvx/random/randomizers/` contains randomizer unit tests and `TestRomHandler`
- `romio/src/test/java/com/uprfvx/romio/romhandlers/RomHandlerIngameTradeTest.java` exists, but it extends ROM-dependent `RomHandlerTest`
- `romio/build.gradle.kts` excludes `*RomHandler*Test` from normal `:romio:test` and moves those tests to `testROMs`

Existing trade-relevant test hooks:

- `TestRomHandler` currently has `getInGameTrades()`, `setInGameTrades(...)`, `hasDVs()`, `maxTradeNicknameLength()` and `maxTradeOTNameLength()` as not implemented.
- `TestRomHandler.getSpeciesSetInclFormes()` and Species-list helpers already exist.
- No `TradeRandomizerTest` exists in the searched `random/src/test` tree.
- Existing ROM-handler In-Game Trade round-trip tests are not suitable for this scope because they load ROM fixtures.

## Recommended harness scope

Recommended later UPR-FVX code-test branch:

- add `random/src/test/java/com/uprfvx/random/randomizers/TradeRandomizerTest.java`
- add the smallest possible test fake, either by extending `TestRomHandler` for trade-only methods or by using a local minimal `RomHandler` test double if that is less invasive
- keep tests under `:random:test`
- do not use `romio:testROMs`
- do not add ROM resources, save files, emulator state, output ROMs, logs, Randomizer JARs or tool binaries

The fake handler needs only enough surface for `TradeRandomizer.randomizeIngameTrades()`:

- `getInGameTrades()` returns synthetic rows
- `setInGameTrades(...)` records whether it was called and captures rows
- `getSpeciesSetInclFormes()` returns a controlled SpeciesSet
- `getSpecies()` / `getSpeciesInclFormes()` provide a randomization pool with at least two safe Species
- `getAllowedItems()` can return an empty or minimal list because item randomization must remain disabled
- `hasDVs()`, `maxTradeNicknameLength()`, `maxTradeOTNameLength()` only need safe defaults if the test enables no optional trade extras
- `internalStringLength(...)` can be left unused or return string length if optional Nickname/OT flags stay false

## Guard edge cases to test later

The first non-ROM harness should prove these cases:

1. Null requested Species:
   - a row with safe given Species and `requestedSpecies == null` is skipped
   - `getSkippedNullRequestedSpeciesTrades() == 1`
   - `hasSkippedTrades() == true`
   - no row mutation occurs
   - `setInGameTrades(...)` is not called when all rows skip

2. Null or unsafe given Species:
   - `givenSpecies == null` is skipped as unsafe
   - placeholder names such as `Bad Egg`, `?` or names containing `unused` are skipped
   - Species not present in `getSpeciesSetInclFormes()` are skipped
   - `getSkippedUnsafeSpeciesTrades()` reflects the skipped rows

3. Mixed safe and unsafe rows:
   - unsafe rows preserve their original fields
   - at least one safe row can change, causing one `setInGameTrades(...)` call
   - skipped rows remain unmodified in the captured list

4. All-skipped run:
   - no writer call
   - `changesMade=false`
   - counters remain visible

5. Optional trade extras disabled:
   - settings keep `randomizeInGameTradesNicknames=false`
   - settings keep `randomizeInGameTradesOTs=false`
   - settings keep `randomizeInGameTradesIVs=false`
   - settings keep `randomizeInGameTradesItems=false`
   - the test asserts only skip/preserve behavior, not text, OT, IV or held-item randomization

## Optional writer preserve test

The Gen3 writer guard would ideally get one tiny non-ROM test after the randomizer-level harness:

- synthetic `InGameTrade` rows with invalid/null/placeholder Species should fail the writer eligibility check
- failing rows should not reach any fixed-length string, Species, IV, OT ID, held item, OT name or requested Species write
- valid rows should remain outside this first preserve-only check unless a later valid-row proof is explicitly authorized

However, `Gen3RomHandler.setInGameTrades(...)` is tied to ROM-entry offsets, internal arrays and byte writes. A later implementation must stop if testing this requires a ROM file, raw private bytes, broad visibility changes or a larger refactor. If a writer seam is needed, it should be planned separately and defensively, for example by extracting or package-scoping only the predicate/row-write decision instead of constructing a ROM-backed handler.

## Allowed checks in a later code-test PR

Allowed for a later explicitly scoped UPR-FVX test PR:

- `./gradlew --offline :random:test`
- `./gradlew --offline :romio:test` only if the added test is non-ROM and does not enter `testROMs`
- `git status --short`
- `git diff --stat`
- `git diff --check`
- focused `rg` checks for `TradeRandomizerTest`, `requestedSpecies`, `skip`, `preserve`, `InGameTrade`, `setInGameTrades`

Do not run `:romio:testROMs`, Randomizer CLI, GUI, ROM smoke, save/reload smoke, emulator checks or output-ROM generation for this harness.

## Forbidden scope remains

The later harness must not:

- use ROM files, saves, emulator states, output ROMs, logs, Randomizer JARs, tool binaries, private paths or hashes
- add text randomization
- add Nickname/OT randomization
- add IV randomization
- add Trade Held Item randomization
- promote Given Species, Requested Species, Trade Held Item, IV, Nickname/OT or text subfeatures
- prepare or run Species-Write-Smoke
- touch Static/Gift, Starter, Trainer, Wild, Held Items, Field Items, Pickup, Shops or unrelated item scopes

## Exit criteria

The harness plan can move to a later implementation branch only if all of these remain true:

- the test can run without ROM files or generated artifacts
- the write set is limited to UPR-FVX test code and, if unavoidable, a minimal trade-test fake
- all optional trade extras stay disabled
- skipped rows are proven unmutated
- all-skipped input is proven to avoid `setInGameTrades(...)`
- no GUI-compatible In-Game Trade status is claimed

If a later branch cannot meet these constraints, the plan should fall back to `harness-plan-blocked` and keep In-Game Trades `blocked-pending-evidence`.

## Status

In-Game Trades remain `blocked-pending-evidence`.

This plan makes a non-ROM harness ready as the next narrow evidence step. It does not authorize code changes in this workspace block and does not authorize any ROM-facing smoke or In-Game Trade feature promotion.
