# 041 - P1 Egg-Move-Modell fuer CFRU/DPE Gen9-BPRE

## Kontext

Ziel dieses Analyseblocks war, das CFRU/DPE-Egg-Move-Species-/Move-ID-Modell read-only zu untersuchen und einzuordnen, ob das aktuelle FVX-Gen3-Egg-Move-Streamformat fuer interne CFRU/DPE-Species und Move-IDs bis `991` stabil ist.

Gepruefter Stand:

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-egg-move-model`
- Voraussetzung: UPR-FVX PR #21 und Workspace PR #77 gemerged.
- UPR-FVX-Stand im Workspace: `4ce93754de390e9177efd2541c02edba0afbb0c4`
- Keine Codeaenderung.
- Keine Aenderung an `02_external/**`.
- Keine Learnset-Write-, Move-Data-Write-, Tutor-Text- oder Special-Tutor-Ausweitung.

## Relevante Pfade

UPR-FVX:

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/SpeciesMovesetRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`
- `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/constants/GlobalConstants.java`

CFRU/DPE:

- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Egg_Moves.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/moves.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/repointall`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/hooks`
- `02_external/CFRU-expansion/hooks`

## CFRU/DPE Egg-Move-Streamformat

DPE definiert `gEggMoves[]` in `src/Egg_Moves.c` als `u16`-Stream.

Relevante Konstanten und Makros:

- `EGG_MOVES_SPECIES_OFFSET = 20000`
- `EGG_MOVES_TERMINATOR = 0xFFFF`
- `egg_moves(species, moves...) (SPECIES_##species + EGG_MOVES_SPECIES_OFFSET), moves`
- `const u16 gEggMoves[] = { ... EGG_MOVES_TERMINATOR }`

Das Format bleibt damit formal kompatibel zum klassischen Gen3-Decomp-Prinzip:

- Ein Wert `> 20000` ist ein Species-Marker.
- Der Species-Wert ist `marker - 20000`.
- Folgende Werte `<= 20000` sind `u16`-Move-IDs.
- `0xFFFF` beendet den Stream.

CFRU/DPE-Runtime-Code sucht ebenfalls nach `species + EGG_MOVES_SPECIES_OFFSET` und liest danach Moves bis zum naechsten Wert `> EGG_MOVES_SPECIES_OFFSET`. Dadurch ist die klassische Marker-Semantik weiterhin aktiv.

## Pointer-/Tabellenbefund

DPE `repointall` dokumentiert:

- `gEggMoves 08045C50`

DPE `hooks` dokumentiert:

- `GetEggMoves 8045C28 2`

CFRU `hooks` dokumentiert:

- `GetAllEggMoves 801D784 3`

Interpretation:

- `0x08045C50` ist der relevante Pointer-/Literal-Ort, ueber den der CFRU/DPE-Runtime-Egg-Move-Code auf `gEggMoves` zugreift.
- Das konkrete Ziel des Pointers wurde in diesem read-only Analyseblock nicht aus einer ROM-Datei ausgelesen, weil keine ROMs angefasst werden sollten.
- FVX nutzt aktuell fuer FireRed-BPRE weiterhin den statischen RomEntry-Wert `EggMoves=0x25EF0C` aus `gen3_offsets.ini`.
- Der BPRE-Hack-Support in `Gen3RomHandler.basicBPRE10HackSupport()` aktualisiert aktuell TM/HM-, Evolution-, Tutor-, Move-Description- und Trainer-Pointer, aber nicht `EggMoves`.

Risiko daraus:

- Selbst wenn das Streamformat kompatibel ist, kann FVX im CFRU/DPE-Stand noch den falschen Egg-Move-Tabellenort lesen/schreiben.
- Ein Folge-Fix sollte `EggMoves` fuer sicher erkannte CFRU/DPE-Gen9-BPRE-Hacks ueber `readPointer(0x45C50)` beziehungsweise den dokumentierten Pointer-Ort ableiten und validieren.

## Aktuelles FVX-Egg-Move-Format

`Gen3RomHandler.getEggMoves()` liest den Gen3-Stream so:

- Startoffset: `romEntry.getIntValue("EggMoves")`
- `u16`-Read pro Eintrag.
- `0xFFFF` beendet den Stream.
- `val > 20000` startet eine neue Species.
- `species = val - 20000`.
- Moves werden unveraendert als numerische Move-IDs gesammelt.

Problematische aktuelle Species-Abbildung:

- Beim Lesen speichert FVX `eggMoves.put(internalToPokedex[currentSpecies], currentMoves)`.
- Beim Schreiben nutzt FVX `pokedexToInternal[species] + 20000`.
- Damit ist der Egg-Move-Map-Key aktuell Pokédex-ID-orientiert, nicht interne CFRU/DPE-SpeciesSet-Identitaet.

Fuer Vanilla Gen3 ist diese Annahme passend. Fuer CFRU/DPE Gen9 ist sie riskant, weil DPE-Egg-Move-Marker intern mit `SPECIES_*`-IDs arbeiten, inklusive Formes und Gen8/9-Species.

## Species-Abdeckung im DPE-Egg-Move-Stream

Source-Auswertung von `src/Egg_Moves.c` gegen `include/species.h`:

| Feld | Wert |
|---|---:|
| Egg-Move-Species-Eintraege | `437` |
| Gen8-Eintraege im normalen Gen8-Bereich `0x44E..0x4D1` | `41` |
| PLA/Hisuian-Eintraege `0x4D2..0x4EB` | `5` |
| G-Max-Eintraege `0x4EC..0x50D` | `0` |
| Paldea-/Gen9-Eintraege `0x50E..0x59F` | `47` |
| Hoechste Species im Egg-Move-Stream | `SPECIES_WOOPER_P`, ID `0x584` / `1412` |

Beispiele fuer Gen8-/PLA-/Gen9-Species im Stream:

- Gen8: `GROOKEY`, `SCORBUNNY`, `SOBBLE`, `SKWOVET`, `ROOKIDEE`, `DREEPY`
- PLA/Hisuian: `GROWLITHE_H`, `SNEASEL_H`, `QWILFISH_H`, `BASCULIN_H`, `ZORUA_H`
- Paldea/Gen9: `SPRIGATITO`, `FUECOCO`, `QUAXLY`, `TANDEMAUS`, `FIDOUGH`, `FRIGIBAX`, `WOOPER_P`

Folgerung:

- Gen8/9-Species sind im Egg-Move-Stream eindeutig enthalten.
- Ein Pokédex-ID-basierter FVX-Read/Write ist fuer diesen Stream nicht stabil genug, weil die Marker interne Species-IDs enthalten.

## Move-ID-Abdeckung im DPE-Egg-Move-Stream

Source-Auswertung von `src/Egg_Moves.c` gegen `include/moves.h`:

| Feld | Wert |
|---|---:|
| Move-Werte im Stream | `4121` |
| Eindeutige Move-IDs | `465` |
| Eindeutige Move-IDs `>=559` | `77` |
| Gen9-Moves `>=0x39B` | `3` |
| Hoechste Move-ID im Egg-Move-Stream | `MOVE_TIDYUP`, ID `0x3C7` / `967` |

Gen9-Moves im Stream:

- `MOVE_CHILLINGWATER`, ID `0x3A1` / `929`, einmal sichtbar.
- `MOVE_COMEUPPANCE`, ID `0x3A5` / `933`, einmal sichtbar.
- `MOVE_TIDYUP`, ID `0x3C7` / `967`, zweimal sichtbar.

Weitere hohe Move-ID-Beispiele oberhalb alter FVX-Grenzen:

- `MOVE_ANCHORSHOT`, `MOVE_BURNUP`, `MOVE_LIQUIDATION`, `MOVE_LUNGE`, `MOVE_GRASSYTERRAIN`, `MOVE_CELEBRATE`, `MOVE_THUNDEROUSKICK`, `MOVE_TRIPLEAXEL`.

Folgerung:

- Das `u16`-Streamformat traegt Move-IDs bis mindestens `967` korrekt.
- Nach dem Move-Data-Reader-Fix ist `moves.total=992`, daher sind diese Move-IDs prinzipiell im geladenen FVX-Move-Modell enthalten.
- Der aktuelle Egg-Move-Randomizer hat trotzdem noch ein separates hohes-Move-ID-Risiko in den globalen Ban-Arrays.

## Aktuelle FVX-Randomizer-Annahmen und Abbruchrisiken

`GameRandomizer.maybeRandomizeMovesets()` ruft Egg-Move-Randomization nur zusammen mit Species-Moveset-Randomization auf:

- `speciesMovesetRandomizer.randomizeMovesLearnt()`
- danach `speciesMovesetRandomizer.randomizeEggMoves()`

Damit ist Egg-Move-only fachlich nicht sauber isoliert; ein Lauf mit Movesets-Randomization beruehrt auch Level-Up-Learnset-Write (`setMovesLearnt()`). Das ist fuer diesen Analyseblock und fuer die bisherige CFRU/DPE-Grenzziehung wichtig, weil Learnset-Write weiterhin out of scope ist.

`SpeciesMovesetRandomizer.randomizeEggMoves()` nutzt:

- `romHandler.getEggMoves()`
- `createSetsOfMoves(...)`
- `findSpeciesInPoolWithSpeciesID(rSpecService.getAll(true), pkmnNum)`
- `romHandler.setEggMoves(movesets)`

Bekannte Risiken:

1. Falscher Tabellenort.

   FVX aktualisiert `EggMoves` fuer CFRU/DPE nicht ueber `0x45C50`, sondern nutzt weiter den FireRed-RomEntry-Wert `0x25EF0C`.

2. Species-ID-Verlust.

   `getEggMoves()` konvertiert interne Species-Marker nach `internalToPokedex[currentSpecies]`; `setEggMoves()` schreibt ueber `pokedexToInternal[species]`. Das kann Gen8/9- und Forme-Marker verlieren oder falsch zusammenfalten.

3. Hohe Move-ID-Arraygrenze.

   `GlobalConstants.bannedRandomMoves` und `bannedForDamagingMove` haben Laenge `827`. `SpeciesMovesetRandomizer.createSetsOfMoves()` indiziert beide Arrays direkt mit `mv.number`. Bei `moves.total=992` kann ein Move mit ID `827..991` einen `ArrayIndexOutOfBoundsException` ausloesen. Dieser Pfad wurde fuer TM/Tutor bereits separat defensiv behandelt, aber nicht fuer Species-/Egg-Movesets.

4. Kein echter Egg-Move-only-Schalter.

   Der aktuelle FVX-Ablauf koppelt Egg-Move-Randomization an allgemeine Moveset-Randomization und damit an Level-Up-Learnset-Write. Ein minimaler CFRU/DPE-Egg-Move-Fix sollte deshalb zuerst einen eng begrenzten Diagnose-/Harness-Pfad oder einen klar gegateten Egg-Move-Teilpfad nutzen, ohne Learnset-Write mitzuziehen.

## Bewertung: Ist das FVX-Streamformat stabil?

Teilweise.

Stabil:

- Das grundlegende `u16`-Streamformat mit `species + 20000` und `0xFFFF` gilt in CFRU/DPE weiterhin.
- Move-IDs bis `991` passen in das Format.
- Der konkrete DPE-Stream enthaelt Gen8/9-Species und Move-IDs bis `967`.

Nicht stabil genug fuer P1-Support:

- FVX nutzt aktuell wahrscheinlich den falschen Egg-Move-Tabellenort fuer CFRU/DPE.
- FVX mappt Species-Marker ueber Pokédex-ID statt ueber interne SpeciesSet-Identitaet.
- Der Randomizer-Poolaufbau fuer Movesets/Egg-Moves ist noch nicht defensiv gegen `moves.total=992` und Ban-Array-Laenge `827`.
- Egg-Move-Randomization ist im normalen Settings-Pfad nicht von Learnset-Write isoliert.

## Empfohlener minimaler Folge-Fixpfad

1. CFRU/DPE-Egg-Move-Pfad eng gaten.

   Bedingung sollte dieselbe sichere CFRU/DPE-Gen9-Erkennung nutzen wie die bisherigen Species-, Move-, TM/HM- und Tutor-Fixes, z. B. `useCfruDpeGen9SpeciesCount`.

2. `EggMoves`-Tabellenort fuer CFRU/DPE aus dem Pointer-Ort `0x45C50` ableiten.

   Zielpointer validieren und nur dann `romEntry.EggMoves` ueberschreiben. Vanilla-/Jambo-/andere Gen3-Pfade unveraendert lassen.

3. Egg-Move-Map-Key fuer CFRU/DPE auf interne SpeciesSet-Identitaet umstellen.

   Beim Lesen: Marker-Species direkt als interne ID beziehungsweise SpeciesSet-Identity erhalten. Beim Schreiben: dieselbe interne ID + `20000` schreiben. Kein Rueckfall ueber Pokédex-ID fuer CFRU/DPE.

4. Hohe Move-IDs im SpeciesMoveset-/Egg-Move-Pool defensiv behandeln.

   Direkte Arrayzugriffe auf `GlobalConstants.bannedRandomMoves[mv.number]` und `bannedForDamagingMove[mv.number]` muessen fuer `mv.number >= array.length` abgesichert oder die entsprechenden Moves aus dem Randomizer-Pool ausgeschlossen werden.

5. Egg-Move-Diagnose ohne Learnset-Write-Ausweitung bauen.

   Fuer P1 sollte zuerst `getEggMoves()`/`setEggMoves()` mit Write/Reload auf dem Egg-Move-Stream validiert werden. `setMovesLearnt()` bleibt separat.

## Offene Fragen

- Welcher Zielpointer steht im getesteten ROM konkret an `0x08045C50`?
- Ist der CFRU/DPE-Egg-Move-Stream im ROM lueckenlos und ausreichend gross fuer in-place Write/Reload nach FVX-Randomization?
- Soll Egg-Move-Randomization im UI/Settings-Pfad von Level-Up-Moveset-Randomization trennbar werden, oder reicht ein interner Diagnose-/Fixpfad?
- Wie sollen Formes und kosmetische Formen im Egg-Move-Map-Key langfristig behandelt werden?
- Sollen Gen9-Egg-Moves wie `Tidy Up`, `Chilling Water` und `Comeuppance` im Auswahlpool bleiben oder zunaechst defensiv gefiltert werden?

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
