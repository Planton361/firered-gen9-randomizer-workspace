# 039 - P1 Tutor-/Special-Tutor-Modell fuer CFRU/DPE Gen9-BPRE

## Kontext

Ziel dieses Analyseblocks war, die CFRU/DPE Tutor- und Special-Tutor-Tabellen fuer den getesteten Gen9-BPRE-Stand read-only zu modellieren. Es wurden keine Codeaenderungen vorgenommen und keine Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder TM/HM-Item-Text-Pfade erweitert.

Gepruefter Stand:

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-tutor-model`
- Voraussetzungen: UPR-FVX PR #20 und Workspace PR #75 gemerged.
- UPR-FVX-Stand im Submodule: `58379ffd3146fcd6bb0eb416647cdf9b752cfc0e`
- Ausgangsbefund aus Diagnose 038: `moves.total=992`, hoechster Move `PsychicNoise` ID `991`, TM/HM-128-Slot-Scope P1-supported.
- Keine Aenderung an `02_external/**`.
- Kein ROM-Zugriff und keine neuen lokalen Build-/Smoke-Artefakte.

## Relevante Pfade

UPR-FVX:

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TMTutorMoveRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TMHMTutorCompatibilityRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TrainerMovesetRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`

CFRU/DPE:

- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/tutors.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/defines.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/TM_Tutor_Tables.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/assembly/generated/tutor_compatibility.s`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/moves.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/repointall`
- `02_external/CFRU-expansion/src/item.c`
- `02_external/CFRU-expansion/src/config.h`
- `02_external/CFRU-expansion/include/constants/tutors.h`

## CFRU/DPE Tutor-Konstanten

DPE definiert in `include/tutors.h` ein Tutor-Enum mit zwei fachlich getrennten Bereichen:

- Normale Tutor-IDs: `TUTOR00_FIRE_PUNCH` bis `TUTOR127_SOLAR_BLADE`, also IDs `0..127`.
- Special Tutors: `TUTOR_SPECIAL_DRACO_METEOR` bis `TUTOR_SPECIAL_STEEL_BEAM`, kommentiert als IDs `128..136`.
- `LAST_TOTAL_TUTOR_NUM = 136` im DPE-Header.

Der aktive DPE-Tabellenstand nutzt in `src/defines.h`:

- `NUM_MOVE_TUTOR_MOVES = 152`.

Der eingebundene CFRU-Config-Stand zeigt parallel:

- `NUM_MOVE_TUTORS = 152`.
- `LAST_TOTAL_TUTOR_NUM = 161`.

Einordnung:

- Die sichtbare DPE-Header-Kommentierung beschreibt 128 normale Tutor-IDs plus 9 Special-Tutors.
- Die aktive normale Tutor-Move-Tabelle ist groesser: `152` Eintraege.
- Dadurch sind mindestens zwei Zaehllogiken zu unterscheiden: normale table-backed Tutor-Moves und Special-Tutor-/Gesamt-Tutor-IDs.
- Ein Fix darf `LAST_TOTAL_TUTOR_NUM` nicht blind als normale Tabellenlaenge interpretieren.

## Normale Tutor-Move-Tabelle

`src/TM_Tutor_Tables.c` definiert:

```c
const u16 gMoveTutorMoves[NUM_MOVE_TUTOR_MOVES]
```

Befunde:

- Die Tabelle ist eine direkte `u16`-Move-ID-Tabelle.
- Der aktuelle Initializer enthaelt `152` Eintraege.
- Slot 0 entspricht fachlich Tutor 1 in den Kommentaren, analog zum TM/HM-Tabellenstil.
- Erster Eintrag: `MOVE_FIREPUNCH`.
- Letzte sichtbare Eintraege: `MOVE_CHILLINGWATER`, `MOVE_POUNCE`, `MOVE_TRAILBLAZE`, `MOVE_ICESPINNER`, `MOVE_TERABLAST`.
- `MOVE_TERABLAST = 0x3C6`, also Move-ID `966`.
- Weitere hohe Tutor-Move-IDs im Tabellenende liegen im Gen8/9-Bereich, zum Beispiel `MOVE_CHILLINGWATER = 0x3A1`, `MOVE_POUNCE = 0x3BA`, `MOVE_TRAILBLAZE = 0x3C9`.

Die Move-ID-Breite ist damit fuer CFRU/DPE eindeutig `u16` und liegt innerhalb der nach Diagnose 038 geladenen FVX-Move-Coverage `0..991`.

## Special-Tutor-Modell

DPE `include/tutors.h` markiert die Special Tutors explizit als `Not in Table`:

- `DRACO_METEOR`
- `SECRET_SWORD`
- `RELIC_SONG`
- `VOLT_TACKLE`
- `DRAGON_ASCENT`
- `THOUSAND_ARROWS`
- `THOUSAND_WAVES`
- `CORE_ENFORCER`
- `STEEL_BEAM`

CFRU `item.c` prueft Tutor-Kompatibilitaet zweistufig:

- Fuer `tutorId < NUM_MOVE_TUTORS` wird `gTutorLearnsets` gelesen.
- Fuer `tutorId >= NUM_MOVE_TUTORS` folgt Special-Tutor-Sonderlogik.

Einordnung:

- Special Tutors sind nicht Teil von `gMoveTutorMoves`.
- Special Tutors duerfen nicht durch einen normalen `setMoveTutorMoves()`-Write ueberschrieben werden.
- Special-Tutor-Kompatibilitaet ist fachlich regelbasiert, nicht einfach ein weiteres Bitfeld hinter den normalen Slots.

## Tutor-Compatibility- / Learnability-Modell

DPE `assembly/generated/tutor_compatibility.s` definiert `gTutorLearnsets` als generierte Byte-Daten pro Species.

Befunde aus den ersten Datensaetzen:

- Pro sichtbarer Species-Zeile werden `19` Bytes ausgegeben.
- `19` Bytes entsprechen `152` Bits.
- Das passt exakt zu `NUM_MOVE_TUTOR_MOVES = 152`, wenn kein Dummy-Bit vorangestellt wird.
- Die FVX-interne Boolean-Darstellung verwendet dagegen ueblich `moveCount + 1` Flags und reserviert Index `0` als Dummy.

CFRU `item.c` castet `gTutorLearnsets` je nach `NUM_MOVE_TUTORS` auf `u32`-Bitfeldarrays. Bei `NUM_MOVE_TUTORS = 152` ergibt die generische Makroform rechnerisch `5 * u32 = 20` Bytes, waehrend die DPE-generierte Assembly sichtbar `19` Bytes pro Species zeigt. Dieser Unterschied ist ein wichtiges Risiko fuer einen Writer: Vor einem Fix muss am konkreten ROM-Zielpointer und per Reload bestaetigt werden, ob der aktive Build wirklich 19-Byte-kompakt oder 20-Byte-aligned gelesen wird.

## Pointer-Locations

DPE `repointall` dokumentiert:

- `gTutorLearnsets 08120C30`
- `gMoveTutorMoves 08120BE4`

Interpretation analog zu den bereits bestaetigten TM/HM-Pointern:

- `0x8120C30` ist die Pointer-Location fuer `gTutorLearnsets`.
- `0x8120BE4` ist die Pointer-Location fuer `gMoveTutorMoves`.
- Zielpointer wurden in diesem read-only Source-Modell nicht aus einem ROM gelesen; sie bleiben fuer einen Folge-Diagnose-/Fixbranch zu bestaetigen.

## Aktueller FVX-Tutor-Pfad

UPR-FVX `Gen3RomHandler` nutzt fuer FRLG/Em Tutor-Pfade weiterhin das klassische Gen3-Modell:

- `hasMoveTutors()` ist fuer Emerald und FRLG aktiv.
- `getMoveTutorMoves()` liest `romEntry.getIntValue("MoveTutorMoves")` `u16`-Eintraege ab `MoveTutorData`.
- `setMoveTutorMoves()` schreibt dieselbe Anzahl und ruft anschliessend `writeMoveTutorText()` auf.
- `getMoveTutorCompatibility()` berechnet `bytesRequired = ((moveCount + 7) & ~7) / 8` und liest pro Species genau diese Bytezahl.
- `setMoveTutorCompatibility()` schreibt denselben Scope zurueck.

Der BPRE-Hack-Support ueberschreibt aktuell nur den Compatibility-Pointer:

- `MoveTutorCompatibility = readPointer(0x120C30)`.

Nicht erkennbar ist aktuell ein entsprechender CFRU/DPE-Override fuer:

- `MoveTutorData` aus Pointer-Location `0x8120BE4`.
- `MoveTutorMoves = 152`.
- ein Special-Tutor-Modell.

Fuer FireRed-BPRE steht im RomEntry klassisch:

- `MoveTutorData=0x459B60`
- `MoveTutorMoves=15`

Folgerung:

- FVX erkennt den CFRU/DPE-Tutor-Move-Scope aktuell nicht vollstaendig.
- FVX liest voraussichtlich nur `15` Tutor-Moves, waehrend CFRU/DPE `152` table-backed Tutor-Moves nutzt.
- Der Compatibility-Pointer kann bereits auf `gTutorLearnsets` zeigen, wird aber mit der zu kleinen FVX-Laenge `15` ausgewertet. Daraus folgen nur `2` Bytes pro Species statt `19` beziehungsweise eventuell `20` Bytes.

## Randomizer-Pfade und Abbruchrisiken

`GameRandomizer` ruft Tutor-Pfade separat auf:

- `maybeRandomizeMoveTutorMoves()` fuer Tutor-Move-Randomization.
- `maybeRandomizeMoveTutorCompatibility()` fuer Tutor-Compatibility, Full-Compatibility, Sanity und Evolution-Sanity.

`TMTutorMoveRandomizer.randomizeMoveTutorMoves()`:

- nutzt `romHandler.getMoves()` mit `moves.total=992`.
- schliesst TMs und HMs aus.
- nutzt `romHandler.getMoveTutorMoves()` als alten Tutorbestand und fuer die Zielanzahl.
- schreibt per `romHandler.setMoveTutorMoves()`.

Risiken:

- Mit aktuellem FVX-Scope werden nur `15` Slots randomisiert und geschrieben, nicht die CFRU/DPE-`152`-Slot-Tabelle.
- Wenn spaeter `152` Slots geladen werden, kann `writeMoveTutorText()` an zu wenigen oder unpassenden Event-Text-Eintraegen scheitern. Ein minimaler CFRU/DPE-Fix sollte Tutor-Text-Writes analog zum TM51..TM120-Text-Scope zunaechst vermeiden oder eng nachweisen.
- Alte Move-Ban-Arrays wurden fuer TM/HM bereits defensiv abgesichert; Tutor-Move-Randomization muss denselben Schutz fuer hohe Move-IDs behalten.

`TMHMTutorCompatibilityRandomizer.randomizeMoveTutorCompatibility()`:

- nutzt `getMoveTutorCompatibility()` und `getMoveTutorMoves()`.
- nutzt `moveIDs.size()` als Flag-Scope.
- hat bereits eine Schutzlogik gegen Null-/Placeholder-Species im erweiterten BPRE-Hack-Species-Pool.
- prueft Move-IDs gegen die geladene Move-Liste.

Risiken:

- Mit `MoveTutorMoves=15` werden nur die ersten 15 Tutor-Flags randomisiert.
- Wenn `152` Flags geladen werden, muss das Flagmodell exakt zu `gTutorLearnsets` passen, sonst drohen verschobene Writes ueber Species-Grenzen.
- Sanity-Pfade `ensureMoveTutorCompatSanity()` laden `getMovesLearnt()` und bleiben fuer Learnset-Read/Write-Risiken relevant; Learnset-Write bleibt out of scope.

`TrainerMovesetRandomizer` nutzt Tutor-Pfade ebenfalls als Move-Pool-Quelle:

- `allTutorCompat = romHandler.getMoveTutorCompatibility()`.
- `allTutorMoves = romHandler.getMoveTutorMoves()`.

Dadurch kann ein korrigierter Tutor-Scope auch Trainer-Movesets beeinflussen. Der bestehende Trainer-Movesets-P1-Support sollte nach einem Tutor-Fix erneut als Regressionstest laufen.

## Klassischer FVX-Scope vs CFRU/DPE-Scope

| Thema | FVX aktuell | CFRU/DPE-Modell |
|---|---|---|
| Tutor-Move-Count | FireRed-BPRE klassisch `15` | `NUM_MOVE_TUTOR_MOVES=152` |
| Tutor-Move-Tabelle | `MoveTutorData=0x459B60` aus RomEntry | `gMoveTutorMoves` ueber Pointer-Location `0x8120BE4` |
| Move-ID-Format | `u16` | `u16` |
| Tutor-Compatibility-Pointer | fuer BPRE-Hack bereits `readPointer(0x120C30)` | `gTutorLearnsets` ueber Pointer-Location `0x8120C30` |
| Compatibility-Breite | bei 15 Moves: `2` Bytes pro Species | sichtbar `19` Bytes / `152` Bits pro Species |
| Special Tutors | kein separates CFRU/DPE-Modell | 9 Special-Tutors, nicht in normaler Tabelle |
| Text-Write | `writeMoveTutorText()` fuer RomEntry-Events | CFRU/DPE-Scope nicht nachgewiesen; riskant fuer 152 Slots |

## Bewertung fuer P1

Tutor-only ist noch nicht P1-supported.

Gruende:

- FVX nutzt im Tutor-Move-Pfad noch den klassischen FireRed-Scope `15` statt CFRU/DPE `152`.
- FVX erkennt `gMoveTutorMoves` ueber `0x8120BE4` aktuell nicht als Tutor-Move-Tabelle.
- Die Compatibility-Breite wird aus dem zu kleinen FVX-MoveCount berechnet und passt nicht zum `152`-Bit-Modell.
- Special Tutors sind Sonderlogik und duerfen nicht als normale table-backed Tutor-Slots randomisiert werden.
- Der konkrete ROM-Zielpointer und die 19-vs-20-Byte-Stride-Frage muessen vor einem Writer geklaert werden.

Positiv:

- Move-Daten-Coverage ist nach Diagnose 038 ausreichend fuer die dokumentierten Tutor-Move-IDs bis `TERABLAST` ID `966`.
- Das normale Tutor-Move-Format ist einfach `u16[]`.
- Der bestehende Randomizer hat bereits defensive Move-ID- und Null-Type-Schutzlogik, die fuer einen gegateten CFRU/DPE-Pfad wiederverwendbar ist.

## Empfohlener minimaler Folge-Fixpfad

1. CFRU/DPE-Tutor-Pfad eng ueber dieselbe sichere CFRU/DPE-Gen9-BPRE-Erkennung gaten, die fuer Species, Move Data und TM/HM genutzt wird.

2. `gMoveTutorMoves` ueber Pointer-Location `0x8120BE4` lesen und validieren.

3. Fuer normale Tutor-Moves `152` `u16`-Eintraege lesen. Special Tutors nicht in diese Tabelle hineinmischen.

4. `setMoveTutorMoves()` fuer CFRU/DPE zunaechst nur die `152` `u16`-Slots schreiben und Tutor-Text-Rewrites nicht ausweiten, solange CFRU/DPE-Tutor-Text-Scope nicht separat nachgewiesen ist.

5. `gTutorLearnsets` ueber Pointer-Location `0x8120C30` lesen und vor dem Schreiben am konkreten ROM klaeren, ob die aktive Stride `19` Bytes oder `20` Bytes pro Species ist.

6. Compatibility intern als `boolean[153]` modellieren, falls das aktive Tabellenmodell 152 normale Tutor-Flags plus Dummy-Index 0 verwendet.

7. Species-Indexing wie bei TM/HM defensiv ueber interne SpeciesSet-Identitaet und Null-/Placeholder-Species-Schutz fuehren.

8. Diagnose nach Fix mindestens fuer Tutor moves-only, Tutor compatibility-only, Tutor moves + compatibility und Trainer Movesets-Regression ausfuehren.

## Offene Fragen

- Welcher Zielpointer steht im getesteten ROM an `0x8120BE4` fuer `gMoveTutorMoves`?
- Welcher Zielpointer steht im getesteten ROM an `0x8120C30` fuer `gTutorLearnsets`?
- Ist der aktive `gTutorLearnsets`-Stride im ROM wirklich `19` Bytes pro Species oder wird zur Laufzeit ein `20`-Byte-/`u32[5]`-Layout erwartet?
- Warum differieren DPE `LAST_TOTAL_TUTOR_NUM=136` und CFRU-Config `LAST_TOTAL_TUTOR_NUM=161` im aktuellen Submodule-Stand?
- Welche Special-Tutor-IDs sollen fuer Randomizer-P1 unveraendert bleiben, und welche duerfen langfristig modelliert werden?
- Gibt es CFRU/DPE-Tutor-Text-/Menu-Tabellen, die fuer eine UI-korrekte Tutor-Move-Randomization separat nachgezogen werden muessen?

## Checks

UPR-FVX:

- `git status --short`
- `git diff --stat`
- `git diff --check`
- `./gradlew clean :random:jar`

Workspace:

- `git status --short`
- `git submodule status --recursive`
- `git diff --stat`
- `git diff --submodule`
- `git diff --check`
