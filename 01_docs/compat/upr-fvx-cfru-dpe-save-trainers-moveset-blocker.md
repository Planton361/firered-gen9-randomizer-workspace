# UPR-FVX / CFRU / DPE Save-Trainers Moveset Blocker

Datum: 2026-05-12

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-save-trainers-moveset-blocker`

## Ziel

Read-only Diagnose des neuen Save-Pfad-Blockers nach:

- Gen9-SpeciesCount-Fix: `PokemonCount=1439`
- defensivem Palette-Load/-Save-Fix
- erhaltener Gen7/Gen8/Gen9-Species-Coverage

Kein Codefix, kein Build und kein ROM-Artefakt sind Bestandteil dieses Branches.

## Symptom

Der lokale CFRU/DPE-Gen9-Lauf kommt nach dem Palette-Fix weiter als zuvor:

- ROM-Load erreicht `PokemonCount=1439`
- `speciesList.size=1415`
- `maxSpeciesIdentityNumber=1439`
- `generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}`
- Palette-Load ueberspringt fehlende Slots defensiv

Danach bricht der Lauf im Save-Pfad ab:

```text
saveTrainers() / getMovesLearnt()
ungueltiger Pointer: 0x25e49c
```

Der Wild-Log nach Gen7/Gen8/Gen9 wird dadurch noch nicht erzeugt.

## Save-Codepfad

UPR-FVX ruft beim Speichern in `AbstractRomHandler.prepareSaveRom()` bedingungslos diese Schritte auf:

```text
saveSpeciesStats()
saveMoves()
saveTrainers()
savePokemonPalettes()
```

Quelle:

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractRomHandler.java`

`Gen3RomHandler.saveTrainers()` serialisiert anschliessend jeden Trainer neu:

- `saveTrainers()` iteriert ueber alle Trainerdaten.
- `DataRewriter` ruft pro Trainer `trainerPokemonToBytes()` auf.
- `trainerPokemonToBytes()` ruft direkt am Anfang `this.getMovesLearnt()` auf.

Quelle:

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

Wichtig: `getMovesLearnt()` wird aufgerufen, bevor `trainer.pokemonHaveCustomMoves()` und `tp.isResetMoves()` praktisch darueber entscheiden, ob Level-up-Moves fuer diesen Trainer ueberhaupt neu berechnet werden muessen. Deshalb kann ein Wild-only-Lauf den Learnset-Loader treffen, obwohl Trainer-Moves nicht Ziel des Tests sind.

## Pointer-Einordnung

Die fruehere Count-Diagnose dokumentierte:

```text
movesetsTable=0x25D7B4
jamboMovesetHack=false
firstInvalidMovesetIndex=1439
rawPointer=0x0
```

Der neue Fehlerpointer laesst sich auf denselben Tabellenbereich zurueckrechnen:

```text
0x25e49c - 0x25d7b4 = 0x0ce8
0x0ce8 / 4 = 826
```

Damit ist `0x25e49c` der Pointer-Slot:

```text
PokemonMovesets + 826 * 4
```

In DPE/CFRU ist interne Species-ID `826` `SPECIES_ZYGARDE`. Die vorherige Count-Diagnose zeigte in der Probe-Range bereits fuer Gen6/Gen7-nahe IDs unplausible Moveset-Rohpointer, unter anderem:

- ID `824` / Xerneas: raw `0x4000`, invalid
- ID `826` / Zygarde: raw `0x10000`, invalid
- ID `1000..1050`: raw `0x0`, invalid

Der aktuelle Save-Abbruch ist daher kein neuer SpeciesCount-Verlust. Er ist die naechste Auswirkung der alten oder falsch erkannten `PokemonMovesets`-Quelle.

## Ist Der Blocker Trainer-Spezifisch?

Nur der ausloesende Save-Pfad ist trainerbezogen. Die technische Ursache liegt allgemeiner im Moveset-/Learnset-Zugriff:

- `saveTrainers()` ruft `trainerPokemonToBytes()` fuer jeden Trainer auf.
- `trainerPokemonToBytes()` laedt die komplette globale Moveset-Map.
- `getMovesLearnt()` iteriert ueber alle realen Species.
- Der Fehler entsteht beim Lesen eines Moveset-Pointers, bevor eine konkrete Trainer-Species-/Level-Kombination zur Move-Neuberechnung entscheidend wird.

Ohne zusaetzliche ROM-Diagnose ist aus den vorhandenen Logs nicht belastbar ableitbar, welcher Trainer im Iterationslauf gerade serialisiert wurde. Der Pointer selbst identifiziert aber den globalen Moveset-Tabellenslot: interne ID `826` / `SPECIES_ZYGARDE`.

## UPR-FVX Moveset-Modell

`getMovesLearnt()` nutzt:

```text
baseOffset = romEntry["PokemonMovesets"]
pointerOffset = baseOffset + pokedexToInternal[pk.getNumber()] * 4
movesLearntOffset = readPointer(pointerOffset)
readMovesLearnt(movesLearntOffset)
```

`readMovesLearnt()` unterstuetzt zwei Formate:

- Vanilla Gen3: 2 Byte pro Eintrag, Terminator `FF FF`
- Jambo-Hack: 3 Byte pro Eintrag, Terminator `00 00 FF`

Im aktuellen lokalen Befund ist `jamboMovesetHack=false`. Der Code liest also die Vanilla-Variante, waehrend DPE/CFRU im Source ein 3-Byte-LevelUpMove-Modell nutzt.

## DPE/CFRU Learnset-Modell

DPE Gen9 definiert:

- `LEVEL_UP_MOVE(lvl, move) {move, lvl}`
- `LEVEL_UP_END {0x0, 0xFF}`
- `struct __attribute__((packed)) LevelUpMove { u16 move; u8 level; }`
- `gLevelUpLearnsets[NUM_SPECIES]`

Relevante Quellen:

- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Learnsets.c`
- `02_external/CFRU-expansion/src/Tables/level_up_learnsets.c`
- `02_external/CFRU-expansion/src/learn_move.c`

DPE/CFRU enthalten Learnsets bis Gen9:

- `sXerneasLevelUpLearnset`
- `sZygardeLevelUpLearnset`
- `sSprigatitoLevelUpLearnset`
- `sPecharuntLevelUpLearnset`
- Mapping wie `[SPECIES_ZYGARDE] = sZygardeLevelUpLearnset`
- Mapping wie `[SPECIES_PECHARUNT] = sPecharuntLevelUpLearnset`

Daraus folgt: Die Source-Daten fehlen fuer Gen7-Gen9 nicht grundsaetzlich. Der Randomizer liest aktuell sehr wahrscheinlich nicht die richtige `gLevelUpLearnsets`-Tabelle oder nicht mit dem richtigen Format.

## Zusammenhang Zur Moveset-Cutoff-Diagnose

Die fruehere Count-Diagnose hatte zwei getrennte Befunde:

1. `PokemonMovesets` haette den Count von `1439` auf `930` gekappt.
2. `PokedexOrder` kappte danach final auf `823`.

Der Gen9-SpeciesCount-Fix hat beide Count-Kappungen fuer den CFRU/DPE-BPRE-Modus aus dem SpeciesCount-Pfad entfernt. Damit bleiben Names/BaseStats bis Gen9 sichtbar.

Der Save-Blocker zeigt jetzt, dass der alte Moveset-Befund weiterhin funktional relevant ist:

- Er begrenzt nicht mehr den Count.
- Er bricht aber `getMovesLearnt()` ab, sobald ein Save-Pfad die Learnsets wirklich liest.

Das ist erwartbar, weil der Count-Fix ausdruecklich kein Learnset-/Moveset-Fix war.

## CyanSMP64 NatDex Vergleich

Die CyanSMP64 FireRed-NatDex-Referenz nutzt eine explizitere Strategie:

- `tools/inigen/inigen.c` schreibt `PokemonCount = NUM_SPECIES - 1`.
- `PokemonMovesets` wird aus dem Symbol `gLevelUpLearnsets` generiert.
- `src/rom_header_gf.c` exportiert Header-Metadaten fuer `gLevelUpLearnsets`, Entry-Groessen und Terminator.
- `src/pokemon.c` liest Learnsets ueber die dortige NatDex-Struktur.

Relevante Quellen:

- `02_external/references/cyansmp64-pokefirered-natdex/tools/inigen/inigen.c`
- `02_external/references/cyansmp64-pokefirered-natdex/src/rom_header_gf.c`
- `02_external/references/cyansmp64-pokefirered-natdex/src/pokemon.c`
- `02_external/references/cyansmp64-pokefirered-natdex/include/constants/pokemon.h`

Das ist keine direkte Drop-in-Loesung fuer CFRU/DPE, bestaetigt aber das Modell: erweiterte FireRed-Hacks brauchen fuer Learnsets eine profil- oder symbolbasierte Tabellenquelle statt alter BPRE-Heuristiken.

## Wahrscheinliche Ursache

Wahrscheinlichste Ursache:

- FVX verwendet fuer CFRU/DPE weiterhin eine alte oder falsch erkannte `PokemonMovesets`-Pointertabelle.
- `jamboMovesetHack` bleibt `false`, obwohl DPE/CFRU ein 3-Byte-LevelUpMove-Format nutzt.
- `saveTrainers()` erzwingt den globalen Learnset-Read auch dann, wenn Trainer-Moves im aktuellen Lauf nicht randomisiert oder neu berechnet werden muessen.

Der Pointer `0x25e49c` ist daher wahrscheinlich kein valider Learnset-Pointer, sondern ein Pointer-Slot in einer nicht passenden Tabellenregion.

## Fixoptionen

### Option A: DPE/CFRU-Learnset-Loader Korrekt Modellieren

FVX bekommt fuer erkannte CFRU/DPE-BPRE-Hacks eine korrekte `gLevelUpLearnsets`-Quelle und liest das 3-Byte-Format mit Terminator `00 00 FF`.

Bewertung:

- fachlich korrekt
- notwendig fuer spaetere Learnset-, TM/Tutor- und TrainerMoveset-Features
- groesserer Scope, weil Tabellenadresse/Profil/Format belastbar erkannt werden muessen
- sollte eigene Tests fuer Gen1-Gen9-Learnsets bekommen

### Option B: Fehlende Oder Ungueltige Movesets Defensiv Behandeln

`getMovesLearnt()` koennte fuer CFRU/DPE ungueltige Pointer ueberspringen oder leere Listen liefern.

Bewertung:

- kleiner als ein voller Learnset-Loader
- kann Save-Abbrueche reduzieren
- riskant, wenn dadurch echte falsche Tabellenadressen verdeckt werden
- spaetere Features koennten mit leeren Movesets falsche Ergebnisse erzeugen

### Option C: `saveTrainers()` Entkoppeln, Wenn Trainer Nicht Randomisiert Wurden

`trainerPokemonToBytes()` laedt Learnsets nur, wenn tatsaechlich Custom-Move-Trainer mit `resetMoves` serialisiert werden muessen.

Bewertung:

- minimaler naechster Unblocker fuer Wild-only- und Coverage-Laeufe
- vermeidet Learnset-Zugriff, solange Trainer-Moves nicht betroffen sind
- behebt den Learnset-Loader selbst nicht
- muss sicherstellen, dass unveraenderte Trainerdaten nicht semantisch veraendert werden

### Option D: Trainer-Save Fuer CFRU/DPE Profilbasiert Einschraenken

Trainerdaten werden fuer CFRU/DPE nur geschrieben, wenn Trainer-Randomizer-Features aktiv waren oder der Pfad explizit unterstuetzt ist.

Bewertung:

- schuetzt P0/Wild-only-Laeufe
- reduziert Risiko durch alte Trainer-/Learnset-Annahmen
- muss sauber mit `prepareSaveRom()` und anderen Save-Pfaden koordiniert werden
- kein Ersatz fuer echte Trainer-/Learnset-Kompatibilitaet

## Empfehlung

Minimaler naechster Fix:

1. `saveTrainers()`/`trainerPokemonToBytes()` so entkoppeln, dass `getMovesLearnt()` nur bei tatsaechlich benoetigter Move-Neuberechnung aufgerufen wird.
2. Keine Learnset-Tabellen neu interpretieren und keine Trainer-Species- oder Static/Gift-Fixes im selben Branch.
3. Danach den Wild-only-Gen9-Coverage-Lauf erneut auswerten.

Parallel als eigenes Folgepaket planen:

- DPE/CFRU-Learnset-Profil fuer `gLevelUpLearnsets`
- 3-Byte-LevelUpMove-Format
- valide Pointer-/Terminator-Sanity fuer interne IDs bis `1439`

## Risiken

- Ein defensives Ueberspringen falscher Moveset-Pointer kann echte Tabellenfehler maskieren.
- Ein voller Learnset-Fix kann P1-Features beruehren und sollte nicht mit dem P0/Wild-Coverage-Unblocker vermischt werden.
- Trainer-Save-Entkopplung muss beweisen, dass unveraenderte Trainerdaten nicht ungewollt neu berechnet werden.
- Gen9-Coverage bleibt in Species/BaseStats sichtbar, aber Wild-Log-Auswertung ist blockiert, solange der Save-Pfad vorher abbricht.

## Naechste Diagnose / Naechster Fix

Naechster minimaler Schritt:

- UPR-FVX-Fixbranch fuer einen kleinen Save-Trainers-Unblocker:
  - Learnsets in `trainerPokemonToBytes()` nur lazy laden, wenn `trainer.pokemonHaveCustomMoves()` und mindestens ein `TrainerPokemon.isResetMoves()` dies wirklich benoetigen.
  - Keine Count-, Palette-, Learnset-, Static/Gift-, Trainer-Species- oder Day/Night-Aenderungen.

Danach lokal:

- Wild-only CFRU/DPE-Lauf mit `PokemonCount=1439`
- `speciesList.size`
- `maxSpeciesIdentityNumber`
- `generationCounts`
- Wild-Log nach Generation
- Beispielhafte Gen7/8/9-Wild-Encounter-Namen
