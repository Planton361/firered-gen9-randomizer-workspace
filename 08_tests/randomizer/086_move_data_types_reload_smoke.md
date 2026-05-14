# CFRU/DPE MoveData Types Reload-Smoke

## Zweck

Dieses Protokoll dokumentiert einen engen, sanitisierten GUI-nahen Reload-Smoke fuer:

- `FVX-MOVE-004` Randomize Move Types

Der Smoke prueft ausschliesslich das MoveData-Type-Byte `+2` im bestehenden MoveData-Writer-Preserve-Scope. TypeChart, TypeEffectiveness, Species-Type-Write, Fairy/Stellar-TypeChart-Logik, Move Names, Move Descriptions, TM/HM, Tutor, Egg, Learnsets, Palette, Items, Trainer, Wild, Evolutions, Text/Menu und Graphics sind nicht Teil dieses Blocks.

## Basis

- Workspace-Branch: `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke`
- UPR-FVX-Pin: `bb5ee11978e38839979e654ff1c14ba60a0cde93`
- Baseline:
  - Diagnose 084: MoveData Write Preserve / `Update Moves` reloadet stabil.
  - Diagnose 085: MoveData Power / Accuracy / PP reloadet stabil.
- Lokale Artefakte blieben ignored unter `05_builds/**`.
- Private Pfade, ROM-Namen, Hashes, Logs und Output-ROMs werden nicht dokumentiert.

## Scope

Gepruefte MoveData-Bytes:

| Byte | Feld | Erwartung |
|---:|---|---|
| `+2` | `type` | Randomisierte Move-Types muessen nach Save/Reload stabil bleiben |

Preserve-Bytes:

| Byte | Feld | Erwartung |
|---:|---|---|
| `+5` | `secondaryEffectChance` | bytegleich erhalten |
| `+6` | `target` | bytegleich erhalten |
| `+7` | `priority` | bytegleich erhalten |
| `+8` | `flags` | bytegleich erhalten |
| `+9` | `z_move_power` | bytegleich erhalten |
| `+11` | `z_move_effect` | bytegleich erhalten |

## Ergebnis

Der Smoke ist fuer `FVX-MOVE-004` blockiert.

Save, Log, Output und Reload funktionieren, aber der Reload-Vergleich findet Fairy-Type-Mismatches im MoveData-Type-Byte-Scope.

| Kriterium | Ergebnis |
|---|---:|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| Reload | erfolgreich |
| `writeReloadMoveDataMismatches` | `54` |
| `moves.total` | `992` |
| hoechster Move | `991:PsychicNoise` |
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

## Reload- und Mismatch-Zaehler

| Zaehler | Wert |
|---|---:|
| `typeChangedMoves` | `940` |
| `modeledChangedMoves` | `940` |
| `unchangedMoves` | `51` |
| `typeReloadMismatches` | `54` |
| `typeByteMismatches` | `0` |
| `expectedFairyMoves` | `54` |
| `fairyReloadMismatches` | `54` |
| `cfruDpeTypeByteMismatches` | `54` |
| `invalidMoveTypeBytes` | `0` |
| `unknownMoveTypeMarkers` | `0` |

Interpretation:

- `typeByteMismatches=0` bedeutet nur, dass die Output-Bytes zur aktuellen FVX-Writer-Mappingfunktion passen.
- Die aktuelle Gen3-`typeToByte`-Mappingfunktion schreibt `FAIRY` im MoveData-Pfad faktisch als Fallback `0x00`.
- Fuer den getesteten CFRU/DPE Gen9-BPRE-Stand muss das MoveData-Type-Byte fuer Fairy im sicheren Gate als `0x17` geschrieben werden.
- Alle `54` Reload-Mismatches sind Fairy-bezogen: `expectedFairyMoves=54`, `fairyReloadMismatches=54`, `cfruDpeTypeByteMismatches=54`.
- Das ist ein MoveData-`+2 type`-Writer-Problem, kein TypeChart-/TypeEffectiveness-/Species-Type-Write-Problem.

## Preserve-Byte-Ergebnis

| Zaehler | Wert |
|---|---:|
| `preserveByteMismatchesAllMoves` | `0` |
| `preserveByteMismatchesUnchangedMoves` | `0` |

Die CFRU/DPE-Zusatzbytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` bleiben bytegleich erhalten. Der Preserve-Fix aus Diagnose 083/084 bleibt damit fuer diesen Smoke stabil.

## Feature-Status

| Feature | Status nach diesem Smoke | Begruendung |
|---|---|---|
| `FVX-MOVE-001` Randomize Move Power | `GUI-kompatibel` | durch Diagnose 085 bestaetigt |
| `FVX-MOVE-002` Randomize Move Accuracy | `GUI-kompatibel` | durch Diagnose 085 bestaetigt |
| `FVX-MOVE-003` Randomize Move PP | `GUI-kompatibel` | durch Diagnose 085 bestaetigt |
| `FVX-MOVE-004` Randomize Move Types | `Write modelliert` | blockiert durch Fairy-Type-Byte-Reload-Mismatches |
| `FVX-MOVE-005` Randomize Move Names | `Write modelliert` | ausserhalb dieses Scopes |
| `FVX-MOVE-006` Update Moves to Generation | `GUI-kompatibel` | durch Diagnose 084 bestaetigt |

## Nicht-Ziele

- Keine Move Names oder Move Descriptions.
- Keine TM/HM-, Tutor-, Egg- oder Learnset-Write-Ausweitung.
- Keine TypeChart- oder TypeEffectiveness-Aenderung.
- Keine Species-Type-Write-Aenderung.
- Keine Palette-, Items-, Field-/Shops-/Pickup-, Trainer-, Wild-, Evolution-, Text/Menu- oder Graphics-Arbeit.
- Keine Submodule-Pin-Aenderung.
- Keine Codeaenderung in diesem Workspace-Branch.

## Folgefix

Naechster enger Fixbranch:

- UPR-FVX: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`
- Workspace-Doku/Pin danach: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`

Ziel:

- `Gen3RomHandler.saveMoves()` beziehungsweise der dortige MoveData-Type-Byte-Write muss im sicheren CFRU/DPE-Gen9-BPRE-Gate `FAIRY` als raw `0x17` schreiben.
- Der Fix darf nicht TypeChart, TypeEffectiveness oder Species-Type-Write beruehren.
- Vanilla-, Jambo- und andere Gen3-Pfade muessen unveraendert bleiben.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` muessen weiter bytegleich erhalten bleiben.

Erwartete Reload-Kriterien nach Fix:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `writeReloadMoveDataMismatches=0`
- `typeReloadMismatches=0`
- `cfruDpeTypeByteMismatches=0`
- `moves.total=992`
- hoechster Move bleibt `991:PsychicNoise`
- Preserve-Byte-Mismatches bleiben `0`
- `exceptionClass=none`
- `stacktrace=none`
