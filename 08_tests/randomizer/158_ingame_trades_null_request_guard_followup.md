# Diagnose 158B: In-Game Trades null-request guard follow-up

## Scope

This follow-up records the merged UPR-FVX defensive In-Game Trades Null-/Invalid-Species guard and updates the workspace submodule pin.

No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file is touched. No Workspace code is changed. No further UPR-FVX code change is made in this block.

## Merge evidence

- UPR-FVX PR #39: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/39>
- PR state checked locally with `gh pr view 39 --repo Planton361/universal-pokemon-randomizer-fvx --json state,mergedAt,mergeCommit,baseRefName,headRefName,url`.
- Result: `state=MERGED`, `baseRefName=compat/firered-gen9-cfru-dpe`.
- Original fix commit: `1d3062d1 fix: skip unsafe ingame trade rows`.
- Merged UPR-FVX commit / workspace submodule pin: `a86315e8d82e0854e0fd59549f50e2c49f523c40`.

## Affected UPR-FVX files

- `random/src/main/java/com/uprfvx/random/randomizers/TradeRandomizer.java`
- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

## Implementation decision

The merged UPR-FVX guard implements the narrow defensive shape planned in Diagnose 157:

- unsafe In-Game Trade rows are skipped before mutation in `TradeRandomizer.java`
- rows with `requestedSpecies == null` are not mutated
- rows with null, invalid or placeholder offered/requested Species are not mutated
- unsafe Gen3 rows are preserved/skipped before byte writes in `Gen3RomHandler.java`
- skipped rows do not receive new Species, fixed-length text, Nickname/OT, IV or held-item writes
- no text randomization, Nickname/OT randomization, IV randomization or Trade Held Item randomization is added

## Result status

Follow-up result: guard merged and pinned; In-Game Trades remain without Species-Write-Smoke clearance.

This changes the failure mode from unsafe mutation/write risk to guarded preserve/skip behavior for null-request or unsafe Species rows. It does not prove valid active Trade rows and does not promote any In-Game Trade subfeature to GUI-compatible.

Current classification remains `blocked-pending-evidence`.

## Check context from 158A

The implementation block ran `./gradlew --offline :romio:test :random:test`. Gradle reported `BUILD SUCCESSFUL`, while the existing `:romio:test` report still contained a known/old failure line:

- `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()`
- `expected: <RSE-separate> but was: <RSE-sheet>`

This follow-up records that as a risk/assumption, not as new In-Game Trades evidence.

## Next allowed step

Do not run a ROM Species-Write-Smoke from this follow-up alone.

The next valid In-Game Trades step is one of:

1. a targeted read-only/code-review of PR #39 behavior against the CFRU/DPE Gen9-BPRE In-Game Trades path
2. an explicitly allowed non-ROM unit or harness test that proves skipped/preserved rows cannot mutate or write
3. a later, separately scoped candidate-structure diagnostic that proves valid active rows before any Species write smoke

Text, Nickname/OT, IV and Trade Held Item scopes remain closed.

## Safety

- No ROM, save, emulator state, output ROM, log, Randomizer JAR, tool binary, build artifact, private path, hash, secret, token or `.env` file is committed.
- No Workspace code change is made.
- No Original-Upstream contact or Original-Upstream PR is made.
