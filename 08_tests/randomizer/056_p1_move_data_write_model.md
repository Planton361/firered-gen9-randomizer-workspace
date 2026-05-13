# 056 - P1 Move-Data-Write-Modell fuer CFRU/DPE Gen9-BPRE

## Ziel

Dieses read-only Protokoll modelliert den CFRU/DPE Move-Data-Write-Scope fuer den getesteten Gen9-BPRE-Stand. Es bereitet keinen Fix vor, fuehrt keine neuen Randomizer-Laeufe aus und aendert keinen Code.

Scope:

- Nur bestehende Protokolle und read-only `rg`-/Quellbefunde.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine neuen Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, ROM-Namen, Hashes, Secrets oder `.env`-Inhalte gelesen oder dokumentiert.

Diagnose 055 ist die Grenze: Log-Hygiene, Placeholder-Namen und Unknown-Fallback-Marker werden nicht als Move-Data-Writer-Risiko gewertet, solange keine Save-/Log-/Output-/Reload-Instabilitaet oder Move-Data-Mismatches belegt sind.

## Genutzte Belege

Primaere Belege:

- `033_p1_move_data_model.md`
- `034_move_data_reader_fix_diagnostics.md`
- `047_fvx_gui_options_compatibility_matrix.md`
- `055_type_log_placeholder_hygiene.md`

Read-only `rg`-Befunde:

- `moves.total`
- `BattleMove`
- `split`
- `category`
- `saveMoves`
- `MoveData`
- `MOVES_COUNT`
- `PsychicNoise`
- `MOVE_PSYCHICNOISE`
- `moveCount`

Ergaenzende read-only Codebefunde aus dem lokalen Workspace:

- `Gen3RomHandler.loadMoves()` nutzt fuer den CFRU/DPE-Gate weiterhin 12-Byte-Move-Entries und liest Byte `+10` als Split-/Category-Quelle.
- `Gen3RomHandler.saveMoves()` schreibt aktuell Move-Namen sowie die ersten fuenf Bytes des MoveData-Records: `effect`, `power`, `type`, `accuracy` und `pp`.
- `CFRU_DPE_MOVES_COUNT` ist im lokalen UPR-FVX-Stand als `992` modelliert.
- CFRU/DPE-Quellen definieren `MOVE_PSYCHICNOISE = 0x3DF`, `LAST_MOVE_INDEX = MOVE_PSYCHICNOISE` und `MOVES_COUNT = MOVE_PSYCHICNOISE + 1`.

## Aktueller Move-Data-Read-Stand

Diagnose 034 bestaetigt fuer den getesteten CFRU/DPE Gen9-BPRE-Stand:

| Feld | Wert |
|---|---:|
| `moves.total` | `992` |
| `moves.highestLoaded` | `991` |
| `moves.highestLoadedName` | `PsychicNoise` |
| `moves.categoryPhysical` | `420` |
| `moves.categorySpecial` | `301` |
| `moves.categoryStatus` | `270` |

Bewertung:

- Der Reader ist fuer den dokumentierten P1-Read-Scope unterstuetzt.
- Trainer-Movesets und bereits dokumentierte TM/HM-, Tutor-, Egg- und Learnset-Pfade koennen gegen die geladene 992-Move-Liste validieren.
- Dieser Read-Stand beweist noch keinen sicheren Move-Data-Write fuer die GUI-Optionen, die Move-Daten selbst veraendern.

## BattleMove-Entry-Layout

Diagnose 033 modelliert das CFRU/DPE-`BattleMove`-Layout als 12-Byte-Struktur:

| Offset | Feld | Relevanz fuer FVX |
|---:|---|---|
| `+0` | `effect` | klassisches FVX-Move-Feld |
| `+1` | `power` | klassisches FVX-Move-Feld |
| `+2` | `type` | klassisches FVX-Move-Feld, Type-Mapping separat begrenzt |
| `+3` | `accuracy` | klassisches FVX-Move-Feld |
| `+4` | `pp` | klassisches FVX-Move-Feld |
| `+5` | `secondaryEffectChance` | wird gelesen, aktuell nicht vom Gen3-Writer geschrieben |
| `+6` | `target` | wird gelesen, aktuell nicht vom Gen3-Writer geschrieben |
| `+7` | `priority` | wird gelesen, aktuell nicht vom Gen3-Writer geschrieben |
| `+8` | `flags` | wird teilweise gelesen, aktuell nicht vom Gen3-Writer geschrieben |
| `+9` | `z_move_power` | CFRU/DPE-Zusatzfeld, im Writer zu preserven |
| `+10` | `split` | CFRU/DPE-Category-Quelle |
| `+11` | `z_move_effect` | CFRU/DPE-Zusatzfeld, im Writer zu preserven |

Split-/Category-Semantik:

| Raw Split | Category |
|---:|---|
| `0` | `PHYSICAL` |
| `1` | `SPECIAL` |
| `2` | `STATUS` |

Fuer CFRU/DPE ist Byte `+10` fachlich wichtig. Es ersetzt die klassische Gen3-Ableitung "physische Typen sind Physical, andere Damaging-Moves sind Special, `power == 0` ist Status" nicht global, sondern nur im erkannten CFRU/DPE-Gen9-Gate.

## Klassische FVX-Write-Annahmen in `saveMoves()`

Der aktuelle lokale UPR-FVX-Stand zeigt fuer Gen3:

- `saveMoves()` iteriert von Move-ID `1` bis `MoveCount`.
- Der Writer nutzt dieselbe `MoveData`-Basis und dieselbe 12-Byte-Stride-Annahme.
- Der Writer schreibt Move-Namen zurueck.
- Der Writer schreibt pro Move nur die ersten fuenf MoveData-Bytes:
  - `+0 effect`
  - `+1 power`
  - `+2 type`
  - `+3 accuracy`
  - `+4 pp`

Nicht geschrieben werden im aktuellen Gen3-Writer:

- `+5 secondaryEffectChance`
- `+6 target`
- `+7 priority`
- `+8 flags`
- `+9 z_move_power`
- `+10 split`
- `+11 z_move_effect`

Damit ist Move-Data-Randomization fuer CFRU/DPE nicht allein durch den Reader-Fix abgesichert. Besonders kritisch ist, dass FVX intern `Move.category` nach dem Reader korrekt sehen kann, `saveMoves()` aber keine Category-Aenderung nach `BattleMove.split` zurueckschreibt.

## CFRU/DPE-Risiken bei 992 Moves

| Risiko | Klassifikation | Beleg / Grenze |
|---|---|---|
| 992-Move-Tabellengrenze | Writer-Scope-Risiko | `MOVES_COUNT=992`; Writer muss `MoveCount=991` als hoechste echte ID plus Slot `0` korrekt behandeln. |
| Hohe Move-IDs | Pool-/Array-Risiko | Fruehere TM-/Egg-/Learnset-Protokolle nennen alte globale Move-Ban-Array-Grenzen und hohe Move-IDs als separate Risiken. |
| Category-Write | Semantik-Risiko | CFRU/DPE nutzt `split` bei Byte `+10`; aktueller Gen3-Writer schreibt es nicht. |
| Type-Byte | Mapping-Risiko | Move-Type-Byte bleibt von Pokemon-Type-/Type-Chart-Arbeit getrennt; ungueltige Type-Indizes fallen beim Reader defensiv auf `NORMAL` zurueck. |
| Zusatzfelder | Preserve-Risiko | `secondaryEffectChance`, `target`, `priority`, `flags`, `z_move_power`, `z_move_effect` duerfen nicht durch einen spaeteren Writer genullt oder neu abgeleitet werden. |
| Move-Namen | Text-Risiko | `saveMoves()` schreibt Namen; Move-Text/Menu-/Description-Support bleibt nicht Teil dieses Modells. |
| Log-Fallbacks | Kein Writer-Beweis | Unknown-/Placeholder-Logmarker aus 055 sind getrennt und beweisen keinen MoveData-Fehler. |

## Preserve-Policy

Fuer einen spaeteren Fixbranch gilt als Modellgrenze:

1. Unmodellierte Bytes in jedem 12-Byte-`BattleMove`-Entry muessen erhalten bleiben.
2. Ein spaeterer Writer darf nur Felder schreiben, deren CFRU/DPE-Semantik explizit modelliert ist.
3. Category-Aenderungen duerfen fuer CFRU/DPE nicht nur im Java-`Move`-Objekt verbleiben; sie muessten gezielt nach `split` bei Byte `+10` abgebildet werden.
4. Z-Move-Felder, Target, Priority, Flags und Secondary-Effect-Chance bleiben preserve-only, bis ein eigenes Modell sie fachlich absichert.
5. Move-Namen-/Description-/Text-/Menu-Rewrites bleiben ein eigenes Thema und duerfen nicht als Voraussetzung fuer den MoveData-Writer gelten.

Diese Preserve-Policy ist enger als "den ganzen 12-Byte-Record neu schreiben". Sie vermeidet, dass ein spaeterer Fix beim Schreiben klassischer FVX-Felder CFRU/DPE-Zusatzsemantik verliert.

## Reload-Kriterien fuer einen spaeteren Fix

Ein spaeterer Move-Data-Write-Fix sollte mindestens folgende Kriterien nachweisen, ohne private Artefakte zu dokumentieren:

| Kriterium | Erwartung |
|---|---|
| Save | `saveSuccessful=true` |
| Log | `logSuccessful=true`, `logNonEmpty=true` |
| Output | Output-ROM vorhanden, ohne privaten Pfad oder ROM-Namen zu dokumentieren |
| Reload | Reload der geschriebenen ROM-Daten erfolgreich |
| MoveData-Mismatches | `writeReloadMoveDataMismatches=0` oder aequivalenter klar benannter Zaehler |
| MoveCount | `moves.total=992`, hoechster Move weiterhin `991:PsychicNoise` |
| Category | geaenderte oder preservte Categories reloaden nach `split`-Semantik korrekt |
| Preserve | Nicht modellierte Bytes bleiben fuer unveraenderte Moves bytegleich |
| Scope | Keine TM/HM-, Tutor-, Egg-, Learnset-, Type-Chart-, Text/Menu- oder Log-Hygiene-Ausweitung im selben Fix |

Neue Diagnosewerte duerfen nur in einem spaeteren, freigegebenen Diagnose-/Fixblock erhoben werden. Dieses Protokoll erfindet keine neuen Laufwerte.

## Grenze zu Diagnose 055 / Log-Hygiene

Diagnose 055 klassifiziert `Bad Egg`, `<unknown>`, Unknown-Type-/Unknown-Ability-/Unknown-Item-Marker und Placeholder-/Null-Species als Log-Hygiene- oder Scope-Themen, solange Save/Log/Output/Reload stabil bleiben und die jeweiligen Mismatch-Zaehler `0` sind.

Fuer Move-Data-Write bedeutet das:

- Sichtbare Unknown-/Placeholder-Marker sind kein Beweis fuer einen MoveData-Writer-Fehler.
- Move-Data-Write-Risiken beginnen erst bei falschem Move-Count, falschen MoveData-Bytes, verlorener Split-/Category-Semantik, verlorenen CFRU/DPE-Zusatzfeldern, Save-/Log-/Output-Abbruch oder Reload-Mismatch.
- Type-Chart, Pokemon-Type-Mapping, Ability-Namen, Item-Namen, Species-Scope und Placeholder-Filter bleiben getrennte Folgearbeiten.

## Keine Fixumsetzung in diesem Branch

Dieses Protokoll macht keinen Codevorschlag als Umsetzung. Sinnvolle spaetere Folgebranches waeren getrennt:

1. `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
   - Eng gegateter CFRU/DPE-MoveData-Writer mit Preserve-Policy und Reload-Diagnose.
2. `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`
   - Type-Chart und moderne Type-Interaktionen getrennt von MoveData schreiben.
3. `analysis/upr-fvx-cfru-dpe-p2-move-text-menu-model`
   - Move-Namen, Descriptions und UI-/Textpfade getrennt modellieren.

## Ergebnis

Der getestete CFRU/DPE Gen9-BPRE-Stand hat einen dokumentierten Move-Data-Read-Support mit `moves.total=992` und `991:PsychicNoise`. Der bestehende Gen3-`saveMoves()`-Pfad schreibt aber nur klassische Teilfelder und bildet CFRU/DPE-`split`/Category sowie Zusatzfelder nicht als Writer ab. Move-Data-Write bleibt deshalb ein offener Hochrisiko-Writer, dessen spaeterer Fix eng gegatet, preserve-orientiert und reload-diagnostisch abgesichert werden muss.
