# 043 - CFRU/DPE Learnset Write Model for `gLevelUpLearnsets`

## Ziel

CFRU/DPE Learnset-Write-Modell fuer Gen9-BPRE read-only einordnen. Kein Fix, keine Codeaenderung und keine Ausweitung von `setMovesLearnt()` in diesem Branch.

## Kontext

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-learnset-write-model`
- Voraussetzung: UPR-FVX PR #22 und Workspace PR #79 sind gemerged.
- Ausgangsstand: Egg-Move direct scope ist in Diagnose 042 P1-supported; Trainer-Movesets-Learnset-Read ist seit Diagnose 031 entblockt.
- Offener Scope: `setMovesLearnt()` / Level-Up-Learnset-Write fuer CFRU/DPE `gLevelUpLearnsets`.

## Relevante Dateien und Symbole

### UPR-FVX

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
  - `getMovesLearnt()`
  - `getCfruDpeMovesLearnt()`
  - `readCfruDpeMovesLearnt(int offset)`
  - `setMovesLearnt(...)`
  - `movesLearntToBytes(...)`
  - `writeMoveLearnt(...)`
  - `lengthOfMovesLearntAt(int offset)`
  - `jamboMovesetHack`
  - `useCfruDpeGen9SpeciesCount`
  - `CFRU_DPE_MAX_LEARNABLE_MOVES = 50`

### CFRU/DPE

- `02_external/Dynamic-Pokemon-Expansion-Gen-9/repointall`
  - `gLevelUpLearnsets 0803EA7C` under `EXPAND_LEARNSETS`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Learnsets.c`
  - `struct __attribute__((packed)) LevelUpMove { u16 move; u8 level; }`
  - `LEVEL_UP_MOVE(lvl, move) {move, lvl}`
  - `LEVEL_UP_END {0x0, 0xFF}`
- `02_external/CFRU-expansion/src/Tables/level_up_learnsets.c`
  - `gLevelUpLearnsets[]`
  - per-species `s<Name>LevelUpLearnset[]` arrays
  - shared entries for many formes, e.g. Gigantamax and form variants point to base-form learnsets
- `02_external/CFRU-expansion/src/learn_move.c`
  - runtime access through `gLevelUpLearnsets[species][i]`
  - `GetLevelUpMovesBySpecies(...)`
  - `GetLevelUpMovePairsBySpecies(...)`
- `02_external/CFRU-expansion/include/new/learn_move.h`
  - `MAX_LEARNABLE_MOVES 50`
- `02_external/CFRU-expansion/include/constants/species.h`
  - `SPECIES_NONE 0x0`
  - `SPECIES_EGG 0x19C`
  - `SPECIES_ZYGARDE 0x33A`
  - `SPECIES_WOOPER_P 0x584`
  - `SPECIES_PECHARUNT 0x59F`
  - `NUM_SPECIES (SPECIES_PECHARUNT + 1)` = `0x5A0` / `1440`
- `02_external/CFRU-expansion/include/constants/moves.h`
  - `MOVE_NONE 0x0`
  - `MOVE_TIDYUP 0x3C7`
  - `MOVE_TERASTARSTORM 0x3D3`
  - `MOVE_MALIGNANTCHAIN 0x3D9`
  - `MOVE_PSYCHICNOISE 0x3DF`
  - `MOVES_COUNT (MOVE_PSYCHICNOISE + 1)` = `0x3E0` / `992`

## Pointertable-Ort und Zielpointer

CFRU/DPE repointet `gLevelUpLearnsets` ueber den Pointer-Ort:

```text
0x0803EA7C
```

Als ROM-Offset entspricht das:

```text
0x03EA7C
```

Dieser Ort ist ein Pointer-Ort, nicht zwingend der Tabellenanfang. Das Modell ist analog zu den bereits gefixten CFRU/DPE-Pfaden fuer TM/HM, Tutor und Egg Moves: der Pointer-Ort muss gelesen und der Zielpointer muss gegen ROM-Grenzen validiert werden.

Der bestehende FVX-Reader nutzt aktuell weiter `romEntry.PokemonMovesets` als Tabellenbasis und liest pro Species `baseOffset + internalSpecies * 4`. Diagnose 030 erklaerte den alten Abbruch so:

```text
0x25D7B4 + 0x33A * 4 = 0x25E49C
```

`0x33A` ist `SPECIES_ZYGARDE`. Der alte Abbruch war deshalb ein Tabellenmodellproblem, nicht ein Trainerdatenproblem. Fuer einen sicheren Writer sollte die CFRU/DPE-Pointerbasis nicht implizit aus dem klassischen `PokemonMovesets`-Offset abgeleitet werden, sondern ueber den dokumentierten Pointer-Ort `0x03EA7C` beziehungsweise `0x0803EA7C` validiert werden.

## Species-Indexing

CFRU/DPE indiziert `gLevelUpLearnsets[]` mit internen Species-IDs:

- `SPECIES_NONE = 0`
- echte Species/Formes bis `SPECIES_PECHARUNT = 0x59F`
- `NUM_SPECIES = 0x5A0` / `1440`

FVX hat nach den vorherigen CFRU/DPE-Fixes fuer erweiterte BPRE-Hacks eine getrennte `SpeciesSet`-Identitaet. Learnset-Write darf deshalb nicht ueber National-Dex-IDs roundtrippen. Fuer CFRU/DPE muss ein Writer denselben internen Species-Schluessel verwenden, der bereits fuer Wild, Starter, Static/Gift, Trainer, Evolution und Egg Moves relevant war.

Besondere Risiken:

- `SPECIES_NONE` und `SPECIES_EGG` sind Sonder-/Placeholder-Species und sollten nicht randomisiert geschrieben werden.
- Viele Formes teilen Learnset-Zielarrays mit ihrer Basisform. Ein blindes In-place-Write auf ein shared Zielarray kann mehrere Species/Formes gleichzeitig veraendern.
- `Species.getNumber()` ist fuer diesen Scope nicht ausreichend, wenn der gewuenschte Schreibschluessel interne SpeciesSet-Identitaet ist.

## Entry-Format und Sentinel

CFRU/DPE-Level-Up-Eintraege sind gepackt:

```text
u16 move
u8 level
```

Das Tabellenmacro lautet:

```text
LEVEL_UP_MOVE(lvl, move) {move, lvl}
```

Der Sentinel lautet:

```text
move == 0 && level == 0xFF
```

Bytes im ROM:

```text
00 00 FF
```

Die Laufzeitfunktionen lesen bis zu `MAX_LEARNABLE_MOVES = 50` Eintraege oder bis zum Sentinel. Level `0` ist fuer Evo-/Initialmoves sichtbar und darf nicht als Sentinel interpretiert werden, solange `move != 0`.

## Bestehende FVX-Reader-/Writer-Annahmen

Aktueller Stand nach den bisherigen Fixes:

- `getMovesLearnt()` verzweigt fuer erkannte CFRU/DPE Gen9-BPRE-Hacks auf `getCfruDpeMovesLearnt()`.
- Der CFRU/DPE-Reader liest Eintraege als `u16 move + u8 level` und stoppt bei `{0, 0xFF}` oder nach `50` Eintraegen.
- Ungueltige Pointer werden im Read-Pool leer behandelt, damit Trainer Movesets-only nicht blockiert.
- Move-IDs werden nur uebernommen, wenn sie im geladenen FVX-Movearray vorhanden sind.
- `setMovesLearnt()` ist noch der alte generische Writer.

Der alte Writer nimmt weiterhin an:

- `PokemonMovesets` ist direkt beschreibbare Pointertabelle.
- Map-Keys sind `pk.getNumber()` / Pokédex-orientierte Species-Nummern.
- Vanilla ohne Jambo schreibt 2-Byte-Eintraege mit 9-Bit-Move-ID.
- Jambo schreibt 3-Byte-Eintraege, aber nur wenn `jamboMovesetHack` aktiv ist.
- `lengthOfMovesLearntAt()` misst bestehende Laenge ueber `readMovesLearnt(...)`, nicht ueber den CFRU/DPE-Reader.
- `DataRewriter` kann Daten umschreiben, aber es gibt fuer CFRU/DPE keinen belegten freien Speicher-/Repointing-Plan in diesem Branch.

Damit ist `setMovesLearnt()` fuer CFRU/DPE aktuell nicht sicher: Format, Keying, Laengenmessung und Repointing-Semantik sind nicht CFRU/DPE-spezifisch genug.

## In-place-Write-Bewertung

In-place-Write waere nur sicher, wenn alle folgenden Bedingungen erfuellt sind:

1. Der Zielpointer fuer jede betroffene interne Species wird valide gelesen.
2. Das Zielarray gehoert nicht ungewollt mehreren Species/Formes, oder die Kopplung ist fachlich akzeptiert.
3. Der neue Learnset-Bytebedarf ist kleiner/gleich dem vorhandenen Bytebedarf am Zielarray.
4. Der Sentinel `{0, 0xFF}` bleibt exakt erhalten.
5. Alle geschriebenen Move-IDs liegen in `1..991` und sind im aktuellen FVX-Movearray geladen.
6. Placeholder-/Null-Species werden uebersprungen.

Randomization kann Learnsets groesser machen, wenn der Randomizer mehr Eintraege erzeugt als das originale Array an diesem Zielpointer. Da jedes Element `3` Bytes plus `3` Byte Sentinel nutzt, ist die Kapazitaet pro Species:

```text
originalEntryCount * 3 + 3 bytes
```

Ein In-place-Writer ohne Repointing darf also nur `newEntryCount <= originalEntryCount` schreiben. Alles andere riskiert Ueberschreiben des naechsten Learnset-Arrays oder anderer Daten.

## Repointing-Bewertung

Ein robuster Voll-Writer muesste vermutlich repointen koennen:

- neue per-Species Learnset-Arrays in freien ROM-Space schreiben,
- die interne `gLevelUpLearnsets[]`-Pointertabelle aktualisieren,
- shared base-form/forme Learnsets bewusst behandeln,
- freie Speicherbereiche sicher finden oder verwalten,
- ROM-Erweiterung/IPS-/UPS-Kompatibilitaet beruecksichtigen.

Das ist fuer einen minimalen P1-Folgefix zu breit. In diesem Projekt sollte Repointing fuer Learnsets nicht implizit durch `DataRewriter` aktiviert werden, solange Tabellenort, freie Speicherstrategie und Write/Reload-Modell nicht separat diagnostiziert sind.

## Move-ID-Grenzen

CFRU/DPE definiert `MOVES_COUNT = 992`, mit `MOVE_PSYCHICNOISE = 991` als letztem dokumentierten Move. Nach Diagnose 034 und 042 laedt FVX fuer den getesteten Stand ebenfalls `moves.total=992`.

Fuer Learnset-Write heisst das:

- `move == 0` ist nur im Sentinel gueltig.
- geschriebene Move-IDs muessen `0 < move < moves.total` sein.
- hohe Move-IDs duerfen keine alten FVX-Arrays mit Laenge `827` indexieren.
- Write-Diagnosen muessen explizit `invalidMoves`, Unknown-Move-Marker und Gen8/9-Move-Beispiele auswerten.

## Placeholder-/Null-Species

Mindestens folgende interne IDs sind fachlich sensibel:

- `SPECIES_NONE = 0x0`
- `SPECIES_EGG = 0x19C`
- Zygarde-/Forme-Sonderbereiche, insbesondere wenn Runtime- oder Randomizer-Pools sie bereits als Placeholder/Sonderslot klassifiziert haben
- Formes mit shared Learnset-Zielarray

Ein minimaler Folgefix sollte nur echte geladene Species mit stabiler `SpeciesSet`-Identitaet schreiben und Placeholder-/Null-Species zaehlen, aber nicht mutieren.

## Empfohlener minimaler Folge-Fixpfad

1. `setMovesLearnt()` fuer CFRU/DPE eng ueber `useCfruDpeGen9SpeciesCount` gaten.
2. `gLevelUpLearnsets` ueber Pointer-Ort `0x03EA7C` lesen; Pointer validieren wie bei TM/HM, Tutor und Egg Moves.
3. Eine CFRU/DPE-spezifische Laengenmessung implementieren: `u16 move + u8 level` bis `{0, 0xFF}`, maximal `50` Eintraege.
4. Map-Keying auf interne `SpeciesSet`-Identitaet ausrichten; nicht ueber Pokédex-ID roundtrippen.
5. Placeholder-/Null-Species und Species ohne valide Zielpointer ueberspringen und diagnostisch zaehlen.
6. Zunaechst nur bounded in-place write erlauben: wenn `newBytes <= oldBytes`, schreiben; wenn groesser, nicht schreiben und als `needsRepoint`/`skippedGrowth` diagnostizieren.
7. Keine automatische Repointing- oder freie-Space-Strategie im ersten Fixbranch.
8. Shared Zielpointer erkennen: mehrere Species koennen auf dasselbe Learnset zeigen. Entweder nur einmal schreiben oder Konflikte/mehrere unterschiedliche Zielinhalte als nicht sicher skippen.
9. Nach Write Reload-Vergleich ueber interne Species-Identitaet: `writeReloadLearnsetMismatches`, `skippedGrowth`, `sharedPointerConflicts`, `invalidMoves`, `unknownMoveMarker`, `Bad Egg`/`<unknown>`.
10. Erst wenn bounded in-place Write stabil ist, separaten Repointing-Branch planen.

## Diagnosepfad fuer den Folgebranch

Ein sinnvoller Fixbranch sollte nicht direkt den vollen Randomizer-Settings-Flow verwenden, wenn dieser mehr als Learnset-Write aktiviert. Besser ist ein schmaler Harness:

- ROM laden.
- `getMoves()` und `getMovesLearnt()` laden.
- Originale Learnsets nach interner Species-Identitaet zusammenfassen.
- Kontrollierte Mutation erzeugen, die pro Species nicht groesser als das originale Learnset ist.
- `setMovesLearnt()` aufrufen.
- Save ausfuehren.
- Output-ROM reloaden.
- Learnsets erneut lesen und vergleichen.

Zu sammeln:

- `moves.total`
- hoechster Move / letzter Move-Name
- `gLevelUpLearnsets` Pointer-Ort und Zielpointer
- Species count / hoechste interne Species
- Learnset entries before/after/reload
- maximale und typische Learnset-Laengen im geladenen ROM-Scope
- shared Zielpointer count und Konflikte
- skipped Placeholder-/Null-Species
- skipped growth / needsRepoint
- invalid moves
- Gen8/9-Moves im geschriebenen/reloadeten Learnset
- `writeReloadLearnsetMismatches`
- Save/Log/Output/LogNonEmpty, falls ueber Randomizer-Flow pruefbar

## Ergebnis

CFRU/DPE-Learnset-Write ist modellseitig machbar, aber nicht als breite Erweiterung des bestehenden `setMovesLearnt()`-Pfads. Der sichere P1-Folgepfad ist ein eng gegateter CFRU/DPE-Writer mit Pointer-Ort `0x03EA7C`, internem Species-Keying, `3`-Byte-Entryformat, `{0, 0xFF}`-Sentinel, Move-ID-Guards bis `991` und zunaechst strikt bounded In-place-Write. Repointing sollte separat bleiben, bis freier Speicher, Pointertable-Update und shared Learnset-Zielpointer diagnostisch abgesichert sind.
