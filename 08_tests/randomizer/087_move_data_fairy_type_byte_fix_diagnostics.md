# CFRU/DPE MoveData Fairy-Type-Byte Fix Diagnostics

## Zweck

Dieses Protokoll dokumentiert den engen UPR-FVX-Fix fuer `FVX-MOVE-004` Randomize Move Types im getesteten CFRU/DPE Gen9-BPRE-Stand.

Der Fix behandelt ausschliesslich das MoveData-Type-Byte `+2` fuer Fairy im sicheren CFRU/DPE-Gate. TypeChart, TypeEffectiveness, Species-Type-Write, Stellar-/Typenmodell-Refactors, Move Names, Move Descriptions, TM/HM, Tutor, Egg, Learnsets, Palette, Items, Trainer, Wild, Evolutions, Text/Menu und Graphics sind nicht Teil dieses Blocks.

## Branches und Pins

- Workspace-Branch: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`
- UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`
- UPR-FVX-Ausgangscommit: `bb5ee11978e38839979e654ff1c14ba60a0cde93`
- UPR-FVX-Fixcommit: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`
- UPR-FVX PR: https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/34

## Ausgangsbefund aus Diagnose 086

Diagnose 086 zeigte fuer `FVX-MOVE-004`:

| Zaehler | Wert |
|---|---:|
| `writeReloadMoveDataMismatches` | `54` |
| `typeReloadMismatches` | `54` |
| `expectedFairyMoves` | `54` |
| `fairyReloadMismatches` | `54` |
| `cfruDpeTypeByteMismatches` | `54` |
| `preserveByteMismatchesAllMoves` | `0` |
| `preserveByteMismatchesUnchangedMoves` | `0` |

Die Ursache war auf MoveData Byte `+2 type` begrenzt: Fairy wurde im klassischen Gen3-Mapping faktisch nicht als CFRU/DPE-Fairy-Byte `0x17` persistiert beziehungsweise reloadet.

## Implementierter UPR-FVX-Fix

Geaenderte Datei:

- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

Der Fix bleibt im bestehenden CFRU/DPE-Gen9-BPRE-Gate:

- `typeFromMoveData(...)` liest raw `0x17` als `Type.FAIRY`.
- `moveDataTypeToByte(...)` schreibt `Type.FAIRY` als raw `0x17`.
- Alle anderen MoveData-Typen nutzen weiter das bestehende `Gen3Constants.typeToByte(...)`-Mapping.
- Vanilla-, Jambo- und andere Gen3-Pfade bleiben unveraendert.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` bleiben unangetastet.

## UPR-FVX Checks

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

## Sanitizing

Der Reload-Smoke nutzte lokale ignored Artefakte unter `05_builds/**`.

Nicht dokumentiert wurden:

- ROM-Namen.
- ROM-Pfade.
- Output-ROM-Pfade.
- Log-Pfade.
- ROM-Hashes.
- private lokale Pfade.
- Tool-Binaries.
- Secrets, Tokens oder `.env`-Inhalte.

## Reload-Sanity nach Fix

| Kriterium | Ergebnis |
|---|---:|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| Reload | erfolgreich |
| `writeReloadMoveDataMismatches` | `0` |
| `moves.total` | `992` |
| hoechster Move | `991:PsychicNoise` |
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

## Reload- und Mismatch-Zaehler

| Zaehler | Wert |
|---|---:|
| `typeChangedMoves` | `945` |
| `modeledChangedMoves` | `945` |
| `unchangedMoves` | `46` |
| `typeReloadMismatches` | `0` |
| `typeByteMismatches` | `54` |
| `expectedFairyMoves` | `54` |
| `fairyReloadMismatches` | `0` |
| `cfruDpeTypeByteMismatches` | `0` |
| `invalidMoveTypeBytes` | `0` |
| `unknownMoveTypeMarkers` | `0` |

Einordnung:

- `typeByteMismatches=54` ist kein Reload-Fehler in diesem Fix-Smoke.
- Dieser Zaehler vergleicht gegen das klassische `Gen3Constants.typeToByte(...)`-Mapping und zeigt damit genau die gewollte Abweichung fuer Fairy im CFRU/DPE-MoveData-Gate.
- Die fachlich relevanten CFRU/DPE-Reload-Zaehler sind stabil: `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`.

## Preserve-Byte-Ergebnis

| Zaehler | Wert |
|---|---:|
| `preserveByteMismatchesAllMoves` | `0` |
| `preserveByteMismatchesUnchangedMoves` | `0` |

Die CFRU/DPE-Zusatzbytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` bleiben bytegleich erhalten.

## Feature-Status

| Feature | Status nach diesem Fix-Smoke | Begruendung |
|---|---|---|
| `FVX-MOVE-001` Randomize Move Power | `GUI-kompatibel` | durch Diagnose 085 bestaetigt |
| `FVX-MOVE-002` Randomize Move Accuracy | `GUI-kompatibel` | durch Diagnose 085 bestaetigt |
| `FVX-MOVE-003` Randomize Move PP | `GUI-kompatibel` | durch Diagnose 085 bestaetigt |
| `FVX-MOVE-004` Randomize Move Types | `GUI-kompatibel` | durch Diagnose 087 bestaetigt |
| `FVX-MOVE-005` Randomize Move Names | `Write modelliert` | ausserhalb dieses Scopes |
| `FVX-MOVE-006` Update Moves to Generation | `GUI-kompatibel` | durch Diagnose 084 bestaetigt |

## Grenzen

- Kein TypeChart.
- Kein TypeEffectiveness.
- Kein Species-Type-Write.
- Kein Stellar-/Typenmodell-Refactor.
- Keine Move Names oder Move Descriptions.
- Keine TM/HM-, Tutor-, Egg- oder Learnset-Write-Ausweitung.
- Keine Palette-, Items-, Field-/Shops-/Pickup-, Trainer-, Wild-, Evolution-, Text/Menu- oder Graphics-Arbeit.

## Ergebnis

Der CFRU/DPE-MoveData-Type-Byte-Fix ist im getesteten Gen9-BPRE-Stand reload-stabil. `FVX-MOVE-004` Randomize Move Types ist damit im engen MoveData-Writer-Preserve-Scope GUI-kompatibel.
