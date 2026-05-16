# 181 - Trainer Names Follow-up

## Scope

- Workspace branch: `test/upr-fvx-cfru-dpe-trainer-names-followup`
- UPR-FVX PR: #51
- UPR-FVX base branch: `compat/firered-gen9-cfru-dpe`
- Workspace submodule pin: `02_external/upr-fvx` at `d20eb1367c62a4f14c8778bc61ad6904ea76a6d6`
- Feature: `FVX-FOE-013` Trainer Names/Class Names
- Ergebnisstatus: `tested-non-rom`

## Result

UPR-FVX PR #51 is merged and the workspace now records the merged Trainer Names/Class Names Non-ROM decision harness commit.

The pinned PR adds `TrainerNameRandomizerTest` and keeps the scope ROM-free:

- `canChangeTrainerText=false` keeps Trainer Names and Trainer Class Names as no-op paths.
- Trainer Names choose the singles pool for normal names.
- Trainer Names choose the doubles pool for names containing `&`.
- Repeated non-special names keep the same translation.
- Known repeated names such as `GRUNT` may be translated separately.
- `MAX_LENGTH` and `MAX_LENGTH_WITH_CLASS` constraints are respected.
- Trainer Class Names choose singles and doubles pools through `getDoublesTrainerClasses()`.
- `fixedTrainerClassNamesLength=true` preserves matching internal class-name length.
- `setTrainerNames(...)` and `setTrainerClassNames(...)` are only called on the change path.

## Statuswirkung

| Feature-ID | Feature | Status |
|---|---|---|
| `FVX-FOE-013` | Randomize Trainer Names / Class Names | `tested-non-rom`, not P1-supported |

This is not a P1-supported promotion. There is no Gen3 Writer-/Reload-ROM evidence, no ROM-Smoke, no output-ROM generation, no Randomizer run and no text-encoding proof in this follow-up.

## Checks From UPR-FVX PR #51

- `git diff --check`
- `./gradlew --offline :random:test --tests '*TrainerNameRandomizer*'`
- `./gradlew --offline :random:test --tests '*Trainer*'`

## Explicitly Out Of Scope

- No UPR-FVX code changes in this workspace follow-up.
- No Gen3 Writer/Reload test.
- No ROM-Smoke.
- No text-encoding implementation or proof.
- No fix for `changeTo.length()` vs `internalStringLength(...)`.
- No P1-supported promotion.
- No ROMs, saves, emulator states, builds, Randomizer JARs, tool binaries, logs, output ROMs, private paths, secrets, tokens or `.env` files.

## Decision

`FVX-FOE-013` Trainer Names/Class Names now has Non-ROM decision evidence and should be tracked as `tested-non-rom` only.

P1 promotion requires a separately authorized Gen3 Writer-/Reload-ROM or ROM-Smoke evidence scope. Text encoding remains unproven by this test-only follow-up.

## Next

Prepare the next Trainer block only if explicitly scoped, for example a separate ROM-/Reload/Text-Encoding evidence plan or another still-open Trainer suboption. Do not start Gen3 writer, reload, ROM-Smoke or text-encoding implementation from this follow-up.
