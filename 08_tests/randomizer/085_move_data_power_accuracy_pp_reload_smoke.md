# 085 - CFRU/DPE MoveData Power/Accuracy/PP Reload-Smoke

Datum: 2026-05-14

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke`

UPR-FVX-Pin: `bb5ee11978e38839979e654ff1c14ba60a0cde93`

## Ziel

Dieser Smoke prueft GUI-nah und eng begrenzt die klassischen MoveData-Randomizer-Suboptionen:

- `FVX-MOVE-001` Randomize Move Power
- `FVX-MOVE-002` Randomize Move Accuracy
- `FVX-MOVE-003` Randomize Move PP

Geprueft wurden nur die klassischen MoveData-Bytes:

- `+1 power`
- `+3 accuracy`
- `+4 pp`

Weiterhin wurde das Preserve-Verhalten fuer die CFRU/DPE-Zusatzbytes geprueft:

- `+5 secondaryEffectChance`
- `+6 target`
- `+7 priority`
- `+8 flags`
- `+9 z_move_power`
- `+11 z_move_effect`

Nicht geprueft und nicht erweitert wurden `FVX-MOVE-004` Randomize Move Types, `FVX-MOVE-005` Move Names, Move Descriptions, TM/HM, Tutor, Egg Moves, Learnsets, TypeChart, TypeEffectiveness, Palette, Items, Field Items, Shops, Pickup, Trainer, Wild, Evolutions, Text/Menu oder Graphics.

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

Der lokale Smoke oeffnete den getesteten CFRU/DPE Gen9-BPRE-Stand ueber den gepinnten UPR-FVX-Build und aktivierte nur:

- `setRandomizeMovePowers(true)`
- `setRandomizeMoveAccuracies(true)`
- `setRandomizeMovePPs(true)`

Nach dem Save wurde die Output-ROM reloadet. Der Vergleich pruefte die erwarteten Java-`Move`-Werte gegen den Reload und zusaetzlich die rohen BattleMove-Bytes fuer `power`, `accuracy` und `pp`.

Eine Category-/Split-Erzwingung wurde nicht ausgefuehrt; `BattleMove.split` wurde bereits in Diagnose 084 abgedeckt.

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
| `powerChangedMoves` | `575` |
| `accuracyChangedMoves` | `414` |
| `ppChangedMoves` | `882` |
| `modeledChangedMoves` | `961` |
| `unchangedMoves` | `30` |
| `powerReloadMismatches` | `0` |
| `accuracyReloadMismatches` | `0` |
| `ppReloadMismatches` | `0` |
| `powerByteMismatches` | `0` |
| `accuracyByteMismatches` | `0` |
| `ppByteMismatches` | `0` |
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

Die MoveData-Randomizer-Suboptionen fuer Power, Accuracy und PP sind im getesteten CFRU/DPE Gen9-BPRE-Stand reload-stabil:

- `FVX-MOVE-001` Randomize Move Power: `powerReloadMismatches=0`, `powerByteMismatches=0`.
- `FVX-MOVE-002` Randomize Move Accuracy: `accuracyReloadMismatches=0`, `accuracyByteMismatches=0`.
- `FVX-MOVE-003` Randomize Move PP: `ppReloadMismatches=0`, `ppByteMismatches=0`.
- `moves.total=992` und `991:PsychicNoise` bleiben nach Reload stabil.
- Nicht modellierte CFRU/DPE-Zusatzbytes bleiben erhalten.

`<unknown>` wird in diesem Scope nur als moeglicher Log-/Scope-Marker bewertet und nicht als MoveData-Fehler, solange die MoveData-Mismatch-Zaehler stabil `0` bleiben.

## Grenzen

Dieser Smoke ist kein Nachweis fuer:

- `FVX-MOVE-004` Randomize Move Types.
- `FVX-MOVE-005` Randomize Move Names.
- Move Description- oder Menu-Erweiterungen.
- TM/HM-, Tutor-, Egg- oder Learnset-Write.
- TypeChart oder TypeEffectiveness.
- Palette-, Item-, Trainer-, Wild-, Evolution-, Text/Menu- oder Graphics-Scope.

`FVX-MOVE-004` bleibt der naechste getrennte MoveData-Suboption-Scope. `FVX-MOVE-005` bleibt ausserhalb des MoveData-Writer-Preserve-Smokes.
