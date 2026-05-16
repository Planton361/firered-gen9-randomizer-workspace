# 179 - Trainer Special Rules Follow-up

## Ergebnis

- Follow-up: `179_trainer_special_rules_followup`
- Workspace branch: `test/upr-fvx-cfru-dpe-trainer-special-rules-followup`
- UPR-FVX PR: #49, <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/49>
- UPR-FVX base branch: `compat/firered-gen9-cfru-dpe`
- Original UPR-FVX commit: `6489dd1e61d1bcb35345ae006032b884527e0a97`
- Merged UPR-FVX commit: `bc46fdc49741643d8f09dd302b67b5b2d35d24c5`
- Workspace submodule: `02_external/upr-fvx` pinned to `bc46fdc49741643d8f09dd302b67b5b2d35d24c5`

UPR-FVX PR #49 is merged and the workspace now records the merged Trainer Special Rules Non-ROM harness commit.

## UPR-FVX Scope

Affected UPR-FVX test file:

- `random/src/test/java/com/uprfvx/random/randomizers/TrainerSpecialRulesTest.java`

The test uses synthetic Trainer, Party, Species and Evolution data. It does not use ROM files, saves, emulator state, output ROMs or logs.

## Getestete Feature-IDs

| Feature-ID | Feature | Statuswirkung |
|---|---|---|
| `FVX-FOE-010` | Pokemon League Has Unique Pokemon | `tested-non-rom`, not P1-supported |
| `FVX-FOE-012` | Rival Carries Starter Through Game | `tested-non-rom`, not P1-supported |
| `FVX-FOE-014` | Trainers Evolve Their Pokemon + Level Modifier | `tested-non-rom`, not P1-supported |

## Check-Evidenz aus UPR-FVX PR #49

- `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.TrainerSpecialRulesTest`: `BUILD SUCCESSFUL`
- `./gradlew --offline :random:test --tests '*Trainer*'`: `BUILD SUCCESSFUL`
- `./gradlew --offline :random:test`: `BUILD SUCCESSFUL`

## Grenzen

- Non-ROM-only; no ROM-Smoke was run.
- No Trainer writer/reload ROM evidence is added.
- No output ROM, Randomizer run, save or emulator state is involved.
- `FVX-FOE-011` Battle Style remains a separate scope.
- `FVX-FOE-013` Trainer Names/Class Names/Text remains a separate Text scope.
- No P1-supported promotion is made for `FVX-FOE-010`, `FVX-FOE-012` or `FVX-FOE-014`.

## Statuswirkung

Trainer Special Rules now have Non-ROM harness evidence for League Unique, Rival Carries Starter and Trainers Evolve Their Pokemon + Level Modifier. These slices should be tracked as `tested-non-rom` until a separately authorized ROM-/Reload-evidence scope exists.

`FVX-FOE-011` and `FVX-FOE-013` stay unpromoted and must not be folded into the Special Rules follow-up.

## Naechster Schritt

If Trainer Special Rules need P1 promotion later, plan a separate, explicit ROM-/Reload-scope for `FVX-FOE-010`, `FVX-FOE-012` and `FVX-FOE-014`. Keep Battle Style and Trainer Names/Class Names/Text separate.
