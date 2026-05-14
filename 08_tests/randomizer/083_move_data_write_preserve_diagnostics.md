# 083 - CFRU/DPE MoveData Write Preserve Diagnostics

## Ziel

Dieser Arbeitsblock dokumentiert den engen UPR-FVX-Fix fuer MoveData Write / Update Moves im getesteten CFRU/DPE Gen9-BPRE-Scope.

Der Fix soll die klassischen Gen3-MoveData-Felder weiter schreiben, CFRU/DPE `BattleMove.split` gezielt erhalten bzw. aktualisieren und alle nicht modellierten Bytes bytegleich unangetastet lassen.

## Branches

- Workspace: `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
- UPR-FVX: `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
- UPR-FVX Commit: `bb5ee11978e38839979e654ff1c14ba60a0cde93`
- UPR-FVX PR: https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/33

## Code-Scope

Geaendert wurde nur der enge MoveData-Writer in UPR-FVX:

- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

Der bestehende klassische Write bleibt erhalten:

- `+0 effect`
- `+1 power`
- `+2 type`
- `+3 accuracy`
- `+4 pp`

Im bestehenden CFRU/DPE-Gen9-BPRE-Gate wird zusaetzlich `BattleMove.split` bei Byte `+10` geschrieben:

| MoveCategory | split |
|---|---:|
| `PHYSICAL` | `0` |
| `SPECIAL` | `1` |
| `STATUS` | `2` |

Nicht modellierte Bytes werden nicht beschrieben und bleiben dadurch bytegleich erhalten:

- `+5 secondaryEffectChance`
- `+6 target`
- `+7 priority`
- `+8 flags`
- `+9 z_move_power`
- `+11 z_move_effect`

## Abgrenzung

Nicht geaendert wurden:

- Vanilla-, Jambo- und andere Gen3-Pfade ausserhalb des bestehenden CFRU/DPE-Gates
- Move-Namen, Move-Descriptions, Text/Menu
- TM/HM, Tutor, Egg Moves oder Learnsets
- TypeChart / TypeEffectiveness
- Palette, Items, Field Items, Shops, Pickup
- Trainer, Wild, Evolutions oder Graphics

## Checks

UPR-FVX:

- `git status --short`
- `git diff --stat`
- `git diff --check`
- `./gradlew test`
- `./gradlew clean :random:jar`

Ergebnis:

- `git diff --check` war sauber.
- `./gradlew clean :random:jar` war erfolgreich.
- `./gradlew test` endete mit `BUILD SUCCESSFUL`, meldete aber bestehende Test-Failures ausserhalb des MoveData-Scopes:
  - `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE`
  - `Gen1CmpTest.dummyTest`

## Reload-Sanity

Kein lokaler Randomizer-/ROM-Lauf wurde in diesem Arbeitsblock ausgefuehrt. Daher sind die folgenden MoveData-Reload-Kriterien noch nicht als Ergebnis belegt:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `writeReloadMoveDataMismatches=0`
- `moves.total=992`
- hoechster Move bleibt `991:PsychicNoise`
- category/split reload stabil
- Preserve-Bytes fuer unveraenderte Moves bytegleich
- `exceptionClass=none`
- `stacktrace=none`

Diese Kriterien bleiben der naechste sinnvolle Smoke fuer diesen Fix. `<unknown>`-Marker sind nur als Log-/Scope-Marker zu bewerten, solange die MoveData-Mismatch-Zaehler stabil bleiben.

## Ergebnis

Der UPR-FVX-Fix ist implementiert und als PR #33 im Planton361-Fork geoeffnet. Der Workspace pinnt das Submodule auf `bb5ee11978e38839979e654ff1c14ba60a0cde93`.

Die fachliche Hochstufung der MoveData-Write-Optionen bleibt bis zu einem sanitisierten Reload-Smoke konservativ offen.
