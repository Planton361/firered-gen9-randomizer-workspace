# 084 - CFRU/DPE MoveData Write Preserve Reload-Smoke

Datum: 2026-05-14

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-data-write-preserve-reload-smoke`

UPR-FVX-Pin: `bb5ee11978e38839979e654ff1c14ba60a0cde93`

## Ziel

Dieser Smoke prueft eng begrenzt den CFRU/DPE-Gen9-BPRE MoveData-Writer aus dem UPR-FVX-Fix fuer MoveData Write Preserve.

Geprueft wurde nur:

- MoveData / Update Moves.
- CFRU/DPE `BattleMove.split` bei Byte `+10`.
- Preserve-Verhalten fuer nicht modellierte BattleMove-Bytes.
- Reload-Stabilitaet der geschriebenen MoveData-Felder.

Nicht geprueft und nicht erweitert wurden Palette, Items, Field Items, Shops, Pickup, TypeChart, TypeEffectiveness, Trainer, Wild, Evolutions, Text/Menu, Graphics, Move-Namen, Move-Descriptions, TM/HM, Tutor, Egg Moves oder Learnset-Writer.

## Sanitizing

Der Lauf nutzte lokale ignored Artefakte unter `05_builds/**`.

Nicht dokumentiert wurden:

- ROM-Namen.
- ROM-Pfade.
- Output-ROM-Pfade.
- Log-Pfade.
- ROM-Hashes.
- private lokale Pfade.
- Tool-Binaries.
- Secrets, Tokens oder `.env`-Inhalte.

## Methode

Der lokale Smoke oeffnete den getesteten CFRU/DPE Gen9-BPRE-Stand ueber den gepinnten UPR-FVX-Build und fuehrte einen engen `Update Moves to Generation 9`-Flow aus.

Da `Update Moves` in diesem Stand keine Category-Aenderung erzeugte, wurde im Harness genau eine Move-Category-Aenderung erzwungen, um den neuen CFRU/DPE-Writer fuer `BattleMove.split` bei Byte `+10` konkret zu pruefen. Danach wurde gespeichert, reloadet und gegen die erwarteten MoveData- und Preserve-Kriterien verglichen.

## Ergebnis

| Kriterium | Ergebnis |
|---|---|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| Reload erfolgreich | `true` |
| `writeReloadMoveDataMismatches` | `0` |
| `moves.total` | `992` |
| hoechster geladener Move | `991:PsychicNoise` |
| `categoryChangedMoves` | `1` |
| `forcedCategoryChangeApplied` | `true` |
| `modeledChangedMoves` | `8` |
| `unchangedMoves` | `983` |
| `categorySplitMismatches` | `0` |
| `categoryReloadMismatches` | `0` |
| `preserveByteMismatchesAllMoves` | `0` |
| `preserveByteMismatchesUnchangedMoves` | `0` |
| `exceptionClass` | `none` |
| `logExceptionClass` | `none` |
| `stacktrace` | `none` |

## Preserve-Bytes

Folgende nicht modellierte CFRU/DPE-Bytes blieben bytegleich erhalten:

- `+5 secondaryEffectChance`
- `+6 target`
- `+7 priority`
- `+8 flags`
- `+9 z_move_power`
- `+11 z_move_effect`

Der Smoke meldete sowohl ueber alle Moves als auch fuer unveraenderte Moves `0` Preserve-Byte-Mismatches.

## Bewertung

Der enge MoveData-Writer-Preserve-Fix ist fuer `Update Moves` im getesteten CFRU/DPE Gen9-BPRE-Stand reload-stabil:

- klassische MoveData-Felder bleiben schreibbar,
- CFRU/DPE `BattleMove.split` wird im sicheren Gate bei Byte `+10` persistiert,
- nicht modellierte Bytes bleiben erhalten,
- `moves.total=992` und `991:PsychicNoise` bleiben nach Reload stabil.

`<unknown>` wird in diesem Scope nur als moeglicher Log-/Scope-Marker bewertet und nicht als MoveData-Fehler, solange die MoveData-Mismatch-Zaehler stabil `0` bleiben.

## Grenzen

Dieser Smoke ist kein Nachweis fuer:

- Randomize Move Names.
- Move Description- oder Menu-Erweiterungen.
- TM/HM-, Tutor-, Egg- oder Learnset-Write.
- TypeChart oder TypeEffectiveness.
- Palette-, Item-, Trainer-, Wild-, Evolution-, Text/Menu- oder Graphics-Scope.

Die einzelnen MoveData-Randomizer-Suboptionen fuer Power, Accuracy, PP und Types teilen den Writer-Scope, bleiben aber konservativ bis zu eigenen GUI-nahen Smokes nicht separat hochgestuft.
