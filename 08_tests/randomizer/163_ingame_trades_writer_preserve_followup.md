# Diagnose 163B: In-Game Trades writer preserve follow-up

## Scope

This follow-up records the merged UPR-FVX ROM-free Gen3 In-Game Trades writer-preserve test and updates the workspace submodule pin.

No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file is touched or committed.

## Merge evidence

- UPR-FVX PR #41: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/41>.
- Verified state: merged into `compat/firered-gen9-cfru-dpe`.
- Original UPR-FVX test commit: `b71bd2ec test: cover ingame trade writer preserve guard`.
- Merged UPR-FVX commit and workspace submodule pin: `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.

## Affected UPR-FVX files

- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `romio/src/test/java/com/uprfvx/romio/romhandlers/Gen3InGameTradeWriterTest.java`

## Test and seam decision

UPR-FVX PR #41 adds a small ROM-free `:romio:test` for the Gen3 In-Game Trades writer preserve guard.

The implementation uses a narrow package-private static seam in `Gen3RomHandler` so the writer-safety decision can be tested without constructing a ROM-backed handler or using ROM fixtures. Production behavior remains unchanged: `setInGameTrades(...)` still checks the safety decision before row byte writes.

The test uses synthetic `InGameTrade` rows, synthetic Species mappings and synthetic row bytes. It verifies unsafe/null-request and placeholder Species rows are rejected before a byte write would occur, and that the synthetic bytes remain unchanged.

## Check context

Implementation-side checks recorded for UPR-FVX PR #41:

- `./gradlew --offline :romio:test`: `BUILD SUCCESSFUL`
- `./gradlew --offline :romio:test --tests com.uprfvx.romio.romhandlers.Gen3InGameTradeWriterTest`: `BUILD SUCCESSFUL`

The full `:romio:test` report still included the known existing failure line for `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()`. This follow-up records that as a risk/assumption, not as new In-Game Trades evidence.

This workspace follow-up did not rerun Gradle, build UPR-FVX, run the Randomizer or touch generated artifacts.

## Boundaries

Still not covered or authorized:

- no full ROM-backed `setInGameTrades(...)` run
- no ROM-Smoke
- no Species-Write-Smoke or Species-write clearance
- no valid active-row promotion
- no text randomization
- no Nickname/OT randomization
- no IV randomization
- no Trade Held Item randomization

## Follow-up result

Result: the ROM-free Gen3 writer-preserve test is merged and pinned in the workspace.

In-Game Trades remain `blocked-pending-evidence` for CFRU/DPE Gen9-BPRE. The guard now has ROM-free mutation-skip coverage and ROM-free writer-preserve-decision coverage, but it still does not prove valid active trade rows and does not authorize any Species-write smoke.

## Next allowed step

The next narrow step, if explicitly requested, is either a guarded/preserve-only closure decision for In-Game Trades or additional read-only evidence for valid active rows. ROM-Smoke and Species-Write-Smoke remain blocked unless valid active rows are separately proven and explicitly authorized.

## Safety

- No ROMs, saves, emulator states, output ROMs, Randomizer-JARs, tool binaries, logs, private paths, hashes, secrets, tokens or `.env` files were touched.
- No Workspace code was changed.
- No UPR-FVX code was changed in this workspace block.
- No original-upstream contact or original-upstream PR was made.
