# UPR-FVX CFRU/DPE Species Write Paths

## Datum

2026-05-12

## Arbeitsbranch

`analysis/upr-fvx-cfru-dpe-p1-species-write-paths`

## Ziel und Sicherheitsrahmen

Read-only Analyse der Species-Schreibpfade ausserhalb von Standard-Wild nach abgeschlossenem P0. Dieser Block nimmt keine Codeaenderungen, keine Builds und keine ROM-Zugriffe vor.

Vorbedingungen:

- Workspace PR #37 ist gemerged.
- UPR-FVX `compat/firered-gen9-cfru-dpe` enthaelt PR #3, PR #4 und PR #5.
- P0 ist fuer Standard-Wild/Grass, Surfing, Fishing und Rock Smash supported.
- CFRU Day/Night, Swarms, Roamers und Raids bleiben unsupported oder separat.

## Kurzfazit

P0 hat Standard-Wild stabilisiert, aber mehrere Gen3-Schreibpfade verwenden weiterhin die alte Annahme:

```text
pokedexToInternal[species.getNumber()]
```

Bei erweiterten CFRU/DPE-BPRE-Hacks ist `Species.number` jedoch Dex-/Pokedex-ID, nicht interne Tabellenidentitaet. Nach PR #3 ist die interne Identitaet fuer den geladenen Species-Pool in `Species.speciesSetIdentityNumber` verfuegbar. Damit koennen kleine P1-Fixes wahrscheinlich denselben Ansatz wie der Wild-Write-Fix wiederverwenden, aber nicht alle Pfade sind gleich sicher.

Hohes Risiko und klein testbar:

- Starters
- Static Pokemon / Gifts
- Trainer Pokemon

Mittleres bis hohes Risiko mit eigenem Datenmodellbedarf:

- Evolutions
- Learnsets / Movesets
- TM/HM compatibility
- Move Tutors
- Abilities / Hidden Abilities

Nicht als erster Fix starten:

- CFRU Trainer-EV-Spreads
- DPE TM/Tutor-Generator-Modell
- Hidden Ability BaseStats-Erweiterung
- Battle Tower / Frontier-Spread-Tabellen

## Source-of-Truth-Pfade

UPR-FVX:

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Species.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/SpeciesSet.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/constants/Gen3Constants.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/StarterRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/StaticPokemonRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/SpeciesMovesetRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TMHMTutorCompatibilityRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/SpeciesAbilityRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/ItemRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/log/RandomizationLogger.java`

CFRU/DPE:

- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/base_stats.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/evolution.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/tutors.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Evolution Table.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Learnsets.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/TM_Tutor_Tables.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/tm_compatibility/`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/tutor_compatibility/`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/scripts/tm_tutor.py`
- `02_external/CFRU-expansion/include/constants/species.h`
- `02_external/CFRU-expansion/include/constants/tmshms.h`
- `02_external/CFRU-expansion/include/constants/tutors.h`
- `02_external/CFRU-expansion/src/Tables/trainer_data.c`
- `02_external/CFRU-expansion/src/Tables/trainer_parties.h`
- `02_external/CFRU-expansion/src/Tables/trainers_with_evs_table.h`
- `02_external/CFRU-expansion/src/Tables/pokemon_tables.c`
- `02_external/CFRU-expansion/src/Tables/level_up_learnsets.c`
- `02_external/CFRU-expansion/src/Tables/battle_tower_spreads.h`
- `02_external/CFRU-expansion/src/build_pokemon.c`
- `02_external/CFRU-expansion/src/tm_case.c`

## Gemeinsames ID-Modell

| ID | Bedeutung im lokalen CFRU/DPE-Modell | UPR-FVX-Stand nach P0 |
|---|---|---|
| interne Species-ID | ROM-Tabellenindex, `SPECIES_*`, Wild-/Trainer-/Starter-/Evolution-/Learnset-Identitaet | liegt in `pokesInternal` und nach PR #3 in `speciesSetIdentityNumber` |
| Dex-/Pokedex-ID | Anzeige-/Pokedex-Raum aus `PokedexOrder` | liegt in `Species.number`; kann bei DPE kompakt oder kollidierend sein |
| SpeciesSet identity | Set-/Map-Identitaet fuer Species | bei erweiterten BPRE-Hacks interne ID; verhindert Pool-Kollaps |
| Formes | DPE/CFRU-Formen als eigene interne Species | noch kein klassisches FVX-Gen3-Forme-Modell |

Fuer Gen3-Vanilla ist `pokedexToInternal[Species.number]` normal. Fuer CFRU/DPE-BPRE ist dieser Ausdruck riskant, sobald eine randomisierte Gen4+-Species eine kompakte Dex-ID hat, die nicht der internen DPE-ID entspricht.

## Species-Schreibpfad-Matrix

| Pfad | UPR-FVX-Lesen | UPR-FVX-Schreiben | verwendete Species-ID | CFRU/DPE-Datenquelle | Risiko fuer CFRU/DPE | naechster Test | Fixgroesse |
|---|---|---|---|---|---|---|---|
| Starters | `getStarters()` liest `StarterPokemon` per `pokesInternal[readWord(...)]` | `writeStarterBytes()` schreibt `pokedexToInternal[starter.getNumber()]`; `writeStarterText()` nur Text | Lesen interne ID; Schreiben Dex-ID -> intern | FRLG/RSE Starter-Script-/Data-Offsets im ROM-Profil; DPE/CFRU Species-IDs | Gen4+-Starter koennen auf falsche interne Species oder `0` geschrieben werden; Starter-Text kann trotzdem richtig aussehen | CLI-Lauf nur Starters randomisieren, drei Starter-Offsets nach Reload im Log/Handler pruefen, optional BizHawk-Starterwahl nach Freigabe | klein |
| Static Pokemon / Gifts | `StaticPokemon.getPokemon()` liest `pokesInternal[readWord(offset)]`; Hardcoded-Fights lesen Rohwort | `StaticPokemon.setPokemon()` und Tweak-Pfade schreiben `pokedexToInternal[species.getNumber()]`; Roamers werden ueber `setRoamers()` separat geschrieben | Lesen interne ID; Schreiben Dex-ID -> intern | `romEntry.getStaticPokemon()`, FRLG Ghost Marowak, RSE first battle, CFRU runtime/build-pokemon-Pfade | Gift-/Static-Gen4+ kann falsch geschrieben werden; Roamer-Sonderpfade duerfen nicht mitfixen | Static-only Diagnose mit bekannten Gifts/Statics, Reload-Log und Offset-Sanity ohne Day/Night/Roamer-Scope | klein bis mittel |
| Trainer Pokemon | `loadTrainers()` liest Party-Species per `pokesInternal[readWord(...)]`; vier Gen3-Partyformate | `trainerPokemonToBytes()` schreibt `pokedexToInternal[tp.getSpecies().getNumber()]`; Mossdeep-Steven ebenso | Lesen interne ID; Schreiben Dex-ID -> intern; Movesets beim Reset nutzen `tp.getSpecies().getNumber()` | CFRU `trainer_data.c`, `trainer_parties.h`, `trainers_with_evs_table.h`, `build_pokemon.c` | Randomisierte Gen4+-Trainer koennen falsch zurueckgeschrieben werden; Custom moveset reset kann falsche Learnsets nutzen; EV-spread-Modus kann Semantik aendern | Trainer-only Diagnose ohne Moveset-/Item-/Ability-Randomization starten; danach Reload der Trainer-Log-Generationen pruefen | klein fuer Species-Write, mittel fuer Moves/EV-Spreads |
| Evolutions | `loadEvolutions()` iteriert `speciesList`, berechnet Tabellenindex mit `pokedexToInternal[pk.getNumber()]`, Ziel per `pokesInternal[evolvingTo]` | `writeEvolutions()` schreibt Quelle per Dex-Index und Ziel per `pokedexToInternal[evo.getTo().getNumber()]` | Quelle und Ziel teilweise Dex-ID -> intern; Ziel-Lesen interne ID | DPE `src/Evolution Table.c`, `include/evolution.h`; CFRU Spezialmethoden/Forms | Kann falsche Quelle lesen und falsches Ziel schreiben; moderne DPE-Evo-Methoden koennen ausserhalb FVX-Gen3-Modell liegen | Erst read-only Reload-Diagnose ohne Evolution-Randomization: Anzahl/Beispiele Gen4+ Evo-Kanten; danach kleiner Write-Test nur wenn Modell klar | mittel |
| Learnsets / Movesets | `getMovesLearnt()` iteriert `speciesList`, Pointerindex `pokedexToInternal[pk.getNumber()]`, Map-Key `pk.getNumber()` | `setMovesLearnt()` gleiche Pointerindexierung; Trainer-Move-Reset nutzt `getMovesAtLevel(tp.getSpecies().getNumber(), ...)` | Pointerindex Dex-ID -> intern; Map-Key Dex-ID | DPE `src/Learnsets.c`, CFRU `src/Tables/level_up_learnsets.c`, `EXPAND_MOVESETS`-Konfiguration | Gen4+-Learnsets koennen von falscher Species gelesen/geschrieben werden; aktive CFRU- vs. DPE-Quelle muss zuerst feststehen | Moveset read-only Diagnose: Gen4+-Species-Beispiele mit Lernmoves; keine Randomization bis aktive Quelle bestaetigt | mittel bis gross |
| TM/HM compatibility | `getTMHMCompatibility()` nutzt Tabellenindex `pokedexToInternal[pkmn.getNumber()]`, feste Gen3-Breite 8 Byte | `setTMHMCompatibility()` schreibt gleiche feste Breite und Dex-ID-Index | Dex-ID -> intern; feste 50 TM + 8 HM-Annahme | DPE `scripts/tm_tutor.py`, `src/tm_compatibility/`, `TM_HM_COUNT=128`; CFRU `include/constants/tmshms.h`, `tm_case.c` | Sehr hohes Tabellenbreitenrisiko: DPE nutzt 128 TM/HM, FVX Gen3 nutzt 8 Byte/58 Flags | Erst Datenmodell dokumentieren und ROM-Profil/Offsets klaeren; keine kleine Fixannahme | gross |
| Move Tutors | `getMoveTutorMoves()` liest MoveTutorData; `getMoveTutorCompatibility()` nutzt dynamische `MoveTutorMoves`, aber Speciesindex `pokedexToInternal[pkmn.getNumber()]` | `setMoveTutorMoves()` schreibt Moves/Text; `setMoveTutorCompatibility()` schreibt Dex-ID-Index | Tutor-Moves nicht Species-ID; Compatibility Dex-ID -> intern | DPE `TUTOR_COUNT=152`, `src/tutor_compatibility/`, `include/tutors.h`, `src/TM_Tutor_Tables.c`; CFRU tutor constants/docs | Speciesindex riskant und Tutor-Anzahl/Tabellenquelle koennen vom Gen3-Profil abweichen | Erst Tutor-count/bytesRequired/Offset-Diagnose ohne Write; dann entscheiden | mittel bis gross |
| Abilities / Hidden Abilities | `loadBasicPokeStats()` liest Gen3 `ability1` und `ability2` bei Offsets 0x16/0x17 | `saveBasicPokeStats()` schreibt nur `ability1` und `ability2`; `SpeciesAbilityRandomizer` setzt `ability1/2/3` im Modell | Tabellenindex kommt aus Stats-Speicherung; Hidden Ability wird nicht aus Gen3-DPE-Byte 0x1A gelesen/geschrieben | DPE `include/base_stats.h` hat `hiddenAbility` bei 0x1A; CFRU Runtime-Flags und `ability_util.c` | Hidden Ability geht verloren/bleibt unmodelliert; `highestAbilityIndex` ist Gen3 `77`, nicht CFRU Gen9 Ability-Raum | Ability-Diagnose read-only: BaseStats-Stride, `hiddenAbility`, highestAbilityIndex, CFRU Runtime-Flags | gross |
| Items / Held Items | BaseStats-Items werden in `loadBasicPokeStats()` gelesen; Trainer held items werden in `loadTrainers()` gelesen | `saveBasicPokeStats()` schreibt Species-held-items; `trainerPokemonToBytes()` schreibt Trainer-held-items via item internal mapping | Nicht Species-ID, aber an Species-/Trainerdatensaetze gekoppelt | DPE BaseStats item fields; CFRU trainer party item fields; expanded item constants | Item-ID-Raum kann erweitert sein; Species-Zuordnung kann falsch sein, wenn BaseStats-Index falsch ist | Nicht als eigener erster P1-Test; mit Trainer/BaseStats-Diagnose mitloggen | mittel |
| Catching tutorial / scripted tutorial | `hasCatchingTutorial()`/Offsets im RomEntry; kein normaler Static-Pfad | `setCatchingTutorial()` begrenzt per `opponent.getNumber()` und schreibt `pokedexToInternal[...]` in ASM immediates | Dex-ID -> intern plus hardcoded 8-/9-bit Limits | Vanilla FRLG/RSE Tutorial-Code; CFRU kann abweichen | Gen4+ wird durch `getNumber()`-Limits oder falsches Mapping abgelehnt/falsch geschrieben | Spaeter Spezialfall, nicht P1a | mittel |

## Pfaddetails

### Starters

Der Starter-Lesepfad ist bereits intern-ID-basiert, weil `getStarters()` aus den Starter-Worten direkt `pokesInternal[...]` nutzt. Der Schreibpfad ist dagegen weiterhin Dex-ID-basiert:

```text
int starter0 = pokedexToInternal[starters.get(0).getNumber()];
```

Das ist derselbe Fehler-Typ wie vor PR #5 im Standard-Wild-Schreibpfad. Ein kleiner Fix koennte fuer erweiterte BPRE-Hacks die `speciesSetIdentityNumber` schreiben, waehrend Vanilla unveraendert bleibt.

### Static Pokemon / Gift Pokemon

Static-/Gift-Pokemon werden aus den ROM-Offsets als interne IDs gelesen. `StaticPokemon.setPokemon()` schreibt aber `pokedexToInternal[pkmn.getNumber()]`. Das gilt auch fuer FRLG Ghost Marowak und RSE Static First Battle Tweak. Roamers werden im selben `setStaticPokemon()`-Ablauf angehaengt, sollten aber getrennt bleiben, weil sie im Encounter-Systemmodell als unsupported/RAM-nahe klassifiziert sind.

Ein erster Static-Test sollte deshalb Gifts/Statics ohne Roamer-Semantik auswaehlen und nur Reload-Werte vergleichen.

### Trainer Pokemon

`loadTrainers()` liest alle vier Gen3-Partyformate mit `pokesInternal[readWord(...)]`. `trainerPokemonToBytes()` schreibt dagegen bei Custom-Moves- und Standard-Partyformaten:

```text
pokedexToInternal[tp.getSpecies().getNumber()]
```

Der Species-Write selbst wirkt klein fixbar. Trainer sind aber nicht nur Species: Custom Moves, held items, ability slot und CFRU `TRAINERS_WITH_EVS` koennen das Laufzeitmodell veraendern. Deshalb sollte der erste Trainer-Diagnoselauf mit minimalen Settings starten: Trainer Pokemon randomisieren, aber Trainer Moves/Items/Abilities moeglichst unveraendert lassen.

### Evolutions

Evolutionen sind riskanter als Starters/Statics/Trainers, weil Quelle und Ziel an unterschiedlichen Stellen gemappt werden:

- Tabellenquelle: `pokedexToInternal[pk.getNumber()]`
- Ziel beim Lesen: `pokesInternal[evolvingTo]`
- Ziel beim Schreiben: `pokedexToInternal[evo.getTo().getNumber()]`

Bei CFRU/DPE sollte die Evolutionstabelle nach interner Species-ID indiziert sein. Fuer Gen4+-Species kann der aktuelle Code also sowohl falsche Quellzeilen lesen als auch falsche Zielwerte schreiben. Zusaetzlich erweitert DPE moderne Evolutionsmethoden, die FVX-Gen3 nicht zwingend vollstaendig modelliert.

### Learnsets / Movesets

Movesets nutzen ebenfalls `pokedexToInternal[pk.getNumber()]` fuer Pointerindexierung und `pk.getNumber()` als Map-Key. Dieser Pfad kann Gen4+-Learnsets falsch zuordnen. Trainer-Move-Reset greift wiederum mit `tp.getSpecies().getNumber()` auf diese Map zu.

Vor einem Fix muss geklaert sein, ob im lokalen CFRU/DPE-Build DPE `src/Learnsets.c` oder CFRU `src/Tables/level_up_learnsets.c` die aktive Quelle ist. Die CFRU-Doku weist darauf hin, dass `EXPAND_MOVESETS` und DPE-Learnsets nicht blind zusammen behandelt werden duerfen.

### TM/HM und Tutor

DPE `scripts/tm_tutor.py` definiert:

```text
TM_HM_COUNT = 128
TUTOR_COUNT = 152
SPECIES_COUNT = 0x59F + 1
```

FVX Gen3 nutzt fuer TM/HM-Kompatibilitaet dagegen feste 8 Byte pro Species und `Gen3Constants.tmCount + Gen3Constants.hmCount + 1`. Das ist nicht nur ein ID-Mapping-Problem, sondern ein Tabellenbreiten- und Datenmodellproblem. Tutor-Kompatibilitaet ist etwas dynamischer, nutzt aber weiterhin `pokedexToInternal[pkmn.getNumber()]` fuer den Speciesindex.

Dieser Bereich sollte nicht mit einem kleinen "write internal identity"-Patch begonnen werden.

### Abilities / Hidden Abilities

DPE `include/base_stats.h` erweitert `struct BaseStats` um:

```text
0x16 ability1
0x17 ability2
0x1A hiddenAbility
```

FVX Gen3 liest und schreibt nur `ability1` und `ability2` an den Gen3-Offsets und meldet `highestAbilityIndex = 77`. Das passt nicht zum CFRU/DPE-Gen9-Ability-Raum und modelliert Hidden Ability nicht. Ability-Randomization ist deshalb kein kleiner Species-ID-Fix.

## Prioritaetsmatrix

| Prioritaet | Pfad | Empfehlung | Begruendung |
|---|---|---|---|
| P1a | Starters | erster praktischer P1-Diagnoselauf | kleinster, isolierter Schreibpfad; direktes `pokedexToInternal[starter.getNumber()]`; gut reloadbar |
| P1b | Static Pokemon / Gifts | direkt danach | gleicher Fehler-Typ; wichtig fuer Gifts/Legendaries, aber Roamer abgrenzen |
| P1c | Trainer Pokemon | dritter praktischer Lauf | gleicher Species-Write-Fehler, aber mehr Seiteneffekte durch Moves/Items/EV-Spreads |
| P1d | Evolutions | erst nach P1a-c | Quelle und Ziel muessen intern-ID-basiert modelliert werden; moderne DPE-Methoden pruefen |
| P1e | Learnsets | nach Evolution-Modell | aktive Quelle und Map-Key-Modell klaeren; beeinflusst Trainer-Move-Reset |
| P1f | TM/Tutor/Abilities | eigenes Datenmodell vor Fix | Tabellenbreite, Counts, Hidden Ability und Ability-ID-Raum sind groesser als kleiner Patch |
| P1g | Items/Held Items | mit Trainer/BaseStats mitdiagnostizieren | nicht primaer Species-ID, aber an falsche Species-/Trainerdatensaetze gekoppelt |

## Explizite Antworten

### Welcher Pfad sollte als erster P1-Diagnoselauf praktisch getestet werden?

Starters. Der Pfad ist klein, gut isolierbar und zeigt denselben Fehler-Typ wie P0b: Lesen ueber interne ID, Schreiben ueber `pokedexToInternal[Species.number]`. Ein erfolgreicher Test kann ohne Day/Night, Trainer, Evolutions oder Learnsets bewertet werden.

### Welche Pfade koennen vermutlich den Wild-Fix-Ansatz wiederverwenden?

Wahrscheinlich klein wiederverwendbar:

- Starters
- Static Pokemon / Gifts
- Trainer Pokemon Species-Write
- Catching tutorial nur als spaeterer Spezialfall

Moeglicherweise wiederverwendbar, aber erst nach mehr Modellierung:

- Evolution-Zielwerte
- Evolution-Quellindex
- Learnset-Pointerindex
- TM/Tutor-Speciesindex

Nicht ausreichend:

- Abilities / Hidden Abilities
- TM/HM-Tabellenbreite
- CFRU Trainer-EV-Spreads

### Welche Pfade brauchen erst eigenes Datenmodell?

- Evolutions, wegen Quelle/Ziel und moderner DPE-Methoden.
- Learnsets, wegen aktiver CFRU-vs-DPE-Quelle und Map-Key-Semantik.
- TM/HM compatibility, wegen 128 TM/HM statt Gen3-Breite.
- Move Tutors, wegen 152 Tutor und separater DPE-Generatorstruktur.
- Abilities, wegen Hidden Ability bei BaseStats-Byte `0x1A` und erweitertem Ability-ID-Raum.
- Trainer-EV-Spreads/Battle Tower, wegen CFRU-spezifischer Runtime- und Spread-Strukturen.

### Gibt es Pfade, die vorlaeufig im CFRU/DPE-Profil deaktiviert werden sollten?

Ja, fuer reproduzierbare Kompatibilitaetstests:

- TM/HM compatibility randomization
- Move Tutor compatibility randomization
- Ability randomization
- Learnset randomization, bis aktive Datenquelle bestaetigt ist
- Trainer Moves/Items/Abilities, solange nur Trainer-Species getestet werden
- CFRU Runtime-Randomizer-Flags
- Roamers, Swarms, Raids, DexNav und Day/Night-Wild bleiben wie im Encounter-Systemmodell unsupported oder separat

Nicht deaktivieren muessen:

- Starters-only Diagnose
- Static/Gift-only Diagnose ohne Roamer-Scope
- Trainer-Species-only Diagnose mit Moves/Items unveraendert

## Empfohlene naechste praktische Tests

1. `analysis/upr-fvx-cfru-dpe-p1-starter-write-diagnostics`
   - Settings: nur Starter-Randomization aktiv, Gen4+ erlaubt, keine Trainer/Wild/Evolution/Learnset/TM/Tutor/Ability-Aenderungen.
   - Erfolg: Reload/Log zeigt Gen4+-Starter mit interner DPE-ID, kein Rueckfall auf Gen1-3 oder `0`.

2. `analysis/upr-fvx-cfru-dpe-p1-static-write-diagnostics`
   - Settings: nur Static/Gift randomisieren, Roamers separat ignorieren.
   - Erfolg: Gifts/Statics reloaden mit erwarteter interner ID.

3. `analysis/upr-fvx-cfru-dpe-p1-trainer-write-diagnostics`
   - Settings: nur Trainer-Species randomisieren; Moves, Items, Abilities unveraendert.
   - Erfolg: Trainer-Log nach Reload enthaelt Gen4+-Species und keine `0`-/Gen1-3-Rueckfaelle.

## Risiken

- Der lokale Smoke bestaetigt `PokemonCount=823`, nicht den vollen CFRU/DPE-Gen9-Raum.
- `Species.number` bleibt bewusst Dex-ID; ein globales Umdeuten waere riskant.
- Viele Randomizer verwenden `getMovesAtLevel(... getNumber())`; selbst ein korrekt geschriebener Trainer-Species-Wert kann falsche Moves erhalten, wenn Moveset-Keys noch Dex-basiert sind.
- TM/HM und Tutor sind in DPE nicht nur breiter, sondern anders organisiert als FVX-Gen3 erwartet.
- Hidden Ability und erweiterte Ability-IDs sind aktuell nicht vom FVX-Gen3-Ability-Modell abgedeckt.
- CFRU Runtime-Systeme koennen ROM-Tabellen zur Laufzeit anders interpretieren als FVX-Logs suggerieren.

## Naechster minimaler Schritt

Neuer Diagnosebranch:

```text
analysis/upr-fvx-cfru-dpe-p1-starter-write-diagnostics
```

Ziel: Starters-only Randomizer-Lauf mit Gen4+-Allowed-Pool, Reload-Diagnose und Dokumentation, ohne Codeaenderung und ohne Trainer/Static/Evolution/Learnset/TM/Tutor/Ability-Scope.
