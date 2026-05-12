# 030 - P1 Learnsets model for CFRU/DPE `gLevelUpLearnsets`

## Ziel

CFRU/DPE-Level-Up-Learnset- und Trainer-Moveset-Datenmodell fuer den getesteten Gen9-BPRE-Stand read-only einordnen. Kein Fix und keine Randomizer-Codeaenderung in diesem Branch.

## Kontext

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-learnsets-model`
- Voraussetzung: Workspace PR #66 ist gemerged.
- UPR-FVX-Stand: `3864ad0e7efda4ed8a329fb22edb3a28db1040e8`
- Vorheriger Befund: `029_p1_trainer_movesets_only.md` blockiert vor Save/Log in `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel()` durch `Gen3RomHandler.getMovesLearnt()` mit `No valid pointer at 0x25e49c`.
- Analyseart: read-only Source-/Modellpruefung; keine ROM-, Save-, Emulator-State-, Build-Artefakte oder Tool-Binaries committed.

## Relevante Dateien und Symbole

### UPR-FVX

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
  - `readPointer(int offset)`
  - `getMovesLearnt()`
  - `readMovesLearnt(int offset)`
  - `setMovesLearnt(...)`
  - `movesLearntToBytes(...)`
  - Jambo-Erkennung um `readLong(0x3EB20) == 0x47084918`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TrainerMovesetRandomizer.java`
  - `getMoveSelectionPoolAtLevel(...)`
- `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`
  - `[Fire Red (U) 1.0]`
  - `PokemonMovesets=0x25D7B4`

### CFRU/DPE

- `02_external/CFRU-expansion/src/Tables/level_up_learnsets.c`
  - `LEVEL_UP_MOVE(lvl, move)`
  - `LEVEL_UP_END`
  - `gLevelUpLearnsets[]`
  - `sPecharuntLevelUpLearnset[]`
- `02_external/CFRU-expansion/src/learn_move.c`
  - `gLevelUpLearnsets`
  - `GiveBoxMonInitialMoveset(...)`
  - `GetLevelUpMovesBySpecies(...)`
  - `GetLevelUpMovePairsBySpecies(...)`
- `02_external/CFRU-expansion/include/constants/species.h`
  - `SPECIES_ZYGARDE 0x33A`
  - `SPECIES_PECHARUNT 0x59F`
  - `NUM_SPECIES (SPECIES_PECHARUNT + 1)`
- `02_external/CFRU-expansion/include/constants/moves.h`
  - `MOVE_TERASTARSTORM 0x3D3`
  - `MOVE_PSYCHICNOISE 0x3DF`
  - `MOVES_COUNT (MOVE_PSYCHICNOISE + 1)`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Learnsets.c`
  - `struct __attribute__((packed)) LevelUpMove { u16 move; u8 level; }`
  - `LEVEL_UP_MOVE(lvl, move) {move, lvl}`
  - `LEVEL_UP_END {0x0, 0xFF}`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/repointall`
  - `gLevelUpLearnsets 0803EA7C` unter `EXPAND_LEARNSETS`

## Aktuelle UPR-FVX-Annahmen

UPR-FVX behandelt Gen3-Level-Up-Movesets im aktuellen Pfad als klassische Gen3-Pointertabelle:

- `PokemonMovesets` zeigt auf eine Tabelle mit 4-Byte-GBA-Pointern.
- Pro Species wird der Pointer ueber `baseOffset + pokedexToInternal[pk.getNumber()] * 4` gelesen.
- `readPointer()` akzeptiert nur Werte, die nach Subtraktion von `0x08000000` im ROM-Bereich liegen.
- Ohne Jambo-Hack wird jeder Move-Learn-Eintrag als 2 Byte gelesen:
  - Move-ID: Low-Byte plus Bit 0 des zweiten Bytes als 9. Bit.
  - Level: Bits 1-7 des zweiten Bytes.
  - Sentinel: `0xFFFF`.
- Mit Jambo-Hack wird jeder Eintrag als 3 Byte gelesen:
  - `u16 move`
  - `u8 level`
  - Sentinel: `00 00 FF`.
- `setMovesLearnt()` schreibt im selben Format zurueck und nutzt denselben Pointertabellen-/Indexpfad.

Trainer Movesets-only nutzt diesen Pfad zwingend:

- `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel()` laedt beim ersten Trainer-Pokemon `romHandler.getMovesLearnt()`.
- Danach wird per `allLevelUpMoves.get(romHandler.getAltFormeOfSpecies(tp.getSpecies(), tp.getForme()).getNumber())` gefiltert.
- Die resultierenden `MoveLearnt.move`-IDs werden mit `moves.get(ml.move)` in FVX-Moveobjekte umgesetzt.

## CFRU/DPE-Learnset-Struktur

Der getestete CFRU/DPE-Stand verwendet kein komprimiertes Bitfeld im Vanilla-Gen3-Sinn, sondern ein erweitertes Level-Up-Modell:

- `gLevelUpLearnsets[]` ist eine Pointertabelle auf Species-Learnset-Arrays.
- Tabellenindex ist die interne Species-ID, nicht die National-Dex-ID.
- DPE repointet `gLevelUpLearnsets` ueber `0803EA7C`; das entspricht dem Vanilla-BPRE-Codepointer, von dem FVX aktuell `PokemonMovesets` ermittelt.
- Ein Learnset-Eintrag ist im DPE-Modell gepackt als:
  - `u16 move`
  - `u8 level`
- CFRU-Tabellenmacro:
  - `LEVEL_UP_MOVE(lvl, move) {move, lvl}`
  - `LEVEL_UP_END {0x0, 0xFF}`
- CFRU-Laufzeitcode prueft den Sentinel explizit als `move == 0 && level == 0xFF`.
- `MAX_LEARNABLE_MOVES` ist `50`.

Species/Forme-Befunde:

- `SPECIES_ZYGARDE` ist `0x33A` beziehungsweise dezimal `826`.
- `SPECIES_ZYGARDE_CELL`, `SPECIES_ZYGARDE_CORE`, `SPECIES_ZYGARDE_10` und `SPECIES_ZYGARDE_COMPLETE` sind eigene interne Species-IDs und zeigen im Learnset-Table auf dasselbe `sZygardeLevelUpLearnset`.
- `SPECIES_PECHARUNT` ist `0x59F`; `NUM_SPECIES` ist `SPECIES_PECHARUNT + 1`, also `0x5A0` beziehungsweise dezimal `1440`.
- `gLevelUpLearnsets[]` enthaelt Eintraege bis Pecharunt und danach weitere Forme-/Gigantamax-Zuweisungen.

Move-ID-Befunde:

- CFRU/DPE-Moves reichen bis `MOVE_PSYCHICNOISE 0x3DF`; `MOVES_COUNT` ist `0x3E0` beziehungsweise dezimal `992`.
- Beispiele fuer Gen8/9-Relevanz in Learnsets sind `MOVE_TERASTARSTORM 0x3D3` und `MOVE_MALIGNANTCHAIN 0x3D9`.
- Die Trainer-Movesets-only-Diagnose 029 sah in FVX dagegen `moves.total=559`. Selbst nach einem Learnset-Reader-Fix koennen daher CFRU/DPE-Move-IDs oberhalb der aktuell geladenen FVX-Move-Liste ein separater Blocker werden, wenn sie in Trainer-Moveset-Pools gelangen.

## Pointer-/Offset-Befund um `0x25e49c`

FVX nutzt fuer BPRE aktuell `PokemonMovesets=0x25D7B4`.

Der Fehleroffset aus Diagnose 029 laesst sich exakt als Tabellenindex erklaeren:

```text
0x25D7B4 + 0x33A * 4 = 0x25E49C
```

`0x33A` ist `SPECIES_ZYGARDE`. Der Abbruch passiert also beim Lesen des Pointertabellen-Eintrags fuer Zygarde.

Interpretation:

- FVX ermittelt zwar eine `PokemonMovesets`-Basis, behandelt die CFRU/DPE-Tabelle aber weiterhin als FVX-kompatible Gen3-/Jambo-Pointertabelle.
- Bei `0x25e49c` steht kein Wert, den `readPointer()` als GBA-ROM-Pointer akzeptiert.
- Der Pfad bricht deshalb bereits waehrend `getMovesLearnt()` ab, bevor Trainer-Movesets geschrieben, gespeichert, geloggt oder reload-geprueft werden koennen.
- Der konkrete Offset ist kein Trainerdatenproblem. Er ist ein Learnset-Tabellenmodellproblem, sichtbar geworden durch Trainer Movesets-only.

## Warum der aktuelle Pfad scheitert

Der aktuelle FVX-Pfad vermischt drei Annahmen, die fuer den getesteten CFRU/DPE-Stand nicht ausreichend abgesichert sind:

1. `PokemonMovesets` ist eine direkt mit `pokedexToInternal[pk.getNumber()]` indizierbare Pointertabelle fuer alle geladenen Species.
2. Die Eintraege sind entweder Vanilla-Gen3-2-Byte-Learnsets oder Jambo-3-Byte-Learnsets.
3. Die von `getMovesLearnt()` gelieferten Move-IDs sind in `romHandler.getMoves()` vollstaendig vorhanden.

CFRU/DPE nutzt dagegen eine interne Species-ID-Tabelle bis Gen9/Formes, ein `{u16 move, u8 level}`-Modell mit `{0, 0xFF}`-Sentinel und Move-IDs bis mindestens `0x3DF`.

## Plausibler minimaler Fixpfad

Ein Folge-Fixbranch sollte eng auf CFRU/DPE-Level-Up-Learnsets fuer Trainer Movesets-only begrenzt bleiben:

1. In `Gen3RomHandler.getMovesLearnt()` einen schmal gegateten CFRU/DPE-Pfad einfuehren, statt den bestehenden Vanilla-/Jambo-Pfad breit umzubauen.
2. Den Pfad nur fuer erkannte erweiterte BPRE/CFRU-DPE-Gen9-Hacks aktivieren.
3. `gLevelUpLearnsets` als Pointertabelle mit interner Species-ID lesen.
4. Learnset-Eintraege als 3 Byte dekodieren: `u16 move`, `u8 level`, Sentinel `move == 0 && level == 0xFF`.
5. Die Map-Schluessel kompatibel zum bestehenden `TrainerMovesetRandomizer` halten oder den Zugriff minimal auf interne Species-Identitaet erweitern. Fuer Movesets-only mit unveraenderten Trainern reicht voraussichtlich Gen1-3-/National-Dex-Schluesselung; fuer kombinierte Trainer-Species/Movesets braucht es interne Species-/Forme-Identitaet.
6. Move-IDs defensiv pruefen, bevor `moves.get(ml.move)` genutzt wird. CFRU/DPE-Learnsets koennen Gen8/9-Move-IDs enthalten, die FVX aktuell noch nicht vollstaendig als `Move`-Objekte geladen hat.
7. `setMovesLearnt()` nicht automatisch fuer CFRU/DPE aktivieren, solange Write-/Relocation-Semantik fuer die erweiterten Learnset-Arrays nicht separat modelliert ist. Trainer Movesets-only muss zuerst nur lesen koennen.

## Risiken fuer Trainer Movesets-only

- Trainer Movesets-only ist nach Learnset-Read-Unblock moeglicherweise direkt vom Move-Datenmodell blockiert, weil CFRU/DPE `MOVES_COUNT=992` hat, FVX aber in 029 nur `moves.total=559` meldete.
- `TrainerMovesetRandomizer` nutzt `Species.getNumber()` als Map-Key. Das ist fuer Alt-Formes und Gen8/9-Species riskant, weil fruehere Fixes gezeigt haben, dass interne Species-Identitaet und Dex-/Species-Nummer getrennt behandelt werden muessen.
- TM-/Tutor-/Egg-Move-Kompatibilitaet wird im selben Poolaufbau lazy geladen. Nach dem Level-Up-Fix koennen diese Tabellen die naechsten CFRU/DPE-Blocker sein.
- Learnset-Write ist nicht gleich Learnset-Read. Repointing und freier Speicher duerfen nicht implizit angenommen werden.

## Offene Fragen fuer den Folge-Fixbranch

- Kann FVX im ROM sicher zwischen CFRU/DPE-3-Byte-Learnsets und Jambo-3-Byte-Learnsets unterscheiden, oder muss der Pfad ueber die bestehende CFRU/DPE-Hack-Erkennung gegatet werden?
- Soll `getMovesLearnt()` fuer CFRU/DPE doppelt schluesseln: National-/FVX-Nummer fuer bestehende Aufrufer und interne Species-ID fuer Forme-/Gen9-Pfade?
- Welche Move-IDs oberhalb `moves.total=559` treten bei Gen1-3-Trainer-Species tatsaechlich im Levelbereich der Vanilla-Trainer auf?
- Muss Trainer Movesets-only zunaechst nur Level-Up-Moves lesen und TM/Tutor/Egg-Move-Pools fuer CFRU/DPE defensiv deaktivieren/filtern?
- Ist `setMovesLearnt()` fuer CFRU/DPE in P1 ueberhaupt erforderlich, oder reicht fuer Trainer-Movesets-only ein read-only Learnset-Pool?

## Ergebnis

Die Diagnose 029 ist kein Trainer-Scope- oder Trainer-Write-Problem. Der Blocker ist das CFRU/DPE-Level-Up-Learnset-Datenmodell hinter `gLevelUpLearnsets`. FVX liest die Tabelle mit alten Gen3-/Jambo-Annahmen und scheitert bei der internen Species-ID `0x33A` am Pointeroffset `0x25e49c`. Der naechste sinnvolle Schritt ist ein minimal gegateter CFRU/DPE-Learnset-Reader fuer `getMovesLearnt()`, plus defensive Behandlung von Move-IDs und Map-Schluesseln.
