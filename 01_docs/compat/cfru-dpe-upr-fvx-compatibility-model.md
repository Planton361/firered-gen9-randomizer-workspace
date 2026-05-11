# CFRU/DPE UPR-FVX Compatibility Model

## Datum

2026-05-11

## Arbeitsbranch

`analysis/cfru-dpe-upr-fvx-compatibility-model`

## Ziel und Sicherheitsrahmen

Read-only Gesamtanalyse des Kompatibilitaetsmodells zwischen dem lokalen CFRU/DPE-FireRed-Gen9-Teststand und UPR-FVX. Dieser Block nimmt keine Codeaenderungen, keine Builds, keine ROM-Zugriffe und keinen GenRestrictions-Fix vor.

Vorbedingungen:

- Workspace `main` ist aktuell.
- Workspace PR #28 ist gemerged; der Gen4+-Wild-Pool-Diagnosebefund ist in `main` verfuegbar.
- UPR-FVX PR #3 ist gemerged; der lokale Submodule-Stand bleibt fuer diese Analyse auf `223ee9ef compat: preserve CFRU DPE species identity`.
- ROMs, Builds, Saves, Emulator States, Tool-Binaries und private absolute Pfade bleiben ausserhalb von Git und ChatGPT.

## Relevante Dokumentationsquellen

Workspace-Protokolle:

- `08_tests/session/workspace-build-randomizer-smoke-summary.md`
- `08_tests/randomizer/route-1-fallback-wild-randomizer-check.md`
- `08_tests/randomizer/upr-fvx-cfru-dpe-species-pool-analysis.md`
- `08_tests/randomizer/upr-fvx-cfru-dpe-species-diagnostics-run.md`
- `08_tests/randomizer/upr-fvx-cfru-dpe-generation-mapping-fix.md`
- `08_tests/randomizer/upr-fvx-cfru-dpe-generation-mapping-diagnostics-run.md`
- `08_tests/randomizer/upr-fvx-gen4plus-wild-pool-diagnostics.md`

CFRU/DPE Source-of-Truth-Pfade:

- `02_external/Dynamic-Pokemon-Expansion-Gen-9/README.md`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/pokedex.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/base_stats.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/evolution.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Evolution Table.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Learnsets.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Species_To_Pokdex_Table.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Pokedex_Orders.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/offsets.ini`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/scripts/make.py`
- `02_external/CFRU-expansion/README.md`
- `02_external/CFRU-expansion/include/constants/species.h`
- `02_external/CFRU-expansion/include/constants/pokedex.h`
- `02_external/CFRU-expansion/include/wild_encounter.h`
- `02_external/CFRU-expansion/include/new/wild_encounter.h`
- `02_external/CFRU-expansion/src/Tables/wild_encounter_tables.c`
- `02_external/CFRU-expansion/src/wild_encounter.c`
- `02_external/CFRU-expansion/src/Tables/pokemon_tables.c`
- `02_external/CFRU-expansion/src/Tables/level_up_learnsets.c`
- `02_external/CFRU-expansion/src/Tables/trainer_data.c`
- `02_external/CFRU-expansion/src/Tables/trainer_parties.h`
- `02_external/CFRU-expansion/offsets.ini`
- `02_external/CFRU-expansion/scripts/make.py`

UPR-FVX Source-of-Truth-Pfade:

- `02_external/upr-fvx/README.md`
- `02_external/upr-fvx/docs/src/_wikipages/structure.md`
- `02_external/upr-fvx/docs/src/_wikipages/cli_randomizer.md`
- `02_external/upr-fvx/docs/src/_wikipages/wild_pokemon.md`
- `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romio/RomOpener.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Species.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/SpeciesSet.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/GenRestrictions.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/services/RestrictedSpeciesService.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/Settings.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/cli/CliRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/WildEncounterRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/StarterRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/SpeciesMovesetRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/ItemRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/log/RandomizationLogger.java`

## CFRU/DPE-Datenmodell

DPE Gen9 ist der primaere Source-of-Truth fuer die erweiterte Pokemon-Datenbasis. Der README beschreibt eine dynamische FireRed-Dateninsertion mit beliebig vielen Species/Formen, bis zu 1025 Pokedex-Eintraegen ohne Alternate Forms, erweiterten Sprites, Icons, Cries, TM/HM- und Tutor-Kompatibilitaet. Im lokalen Fork sind die Kernzahlen in den Headern sichtbar:

- `include/species.h`: interne Species-Konstanten. `SPECIES_NONE = 0`, `SPECIES_SKRELP = 0x31E`, `SPECIES_SPRIGATITO = 0x50E`, `NUM_SPECIES = SPECIES_PECHARUNT + 1`.
- `include/pokedex.h`: National-Dex-Konstanten und Dex-Strukturen.
- `src/Species_To_Pokdex_Table.c`: Mapping von interner Species-ID auf National-Dex-ID.
- `src/Pokedex_Orders.c`: regionale, alphabetische, Gewicht-, Hoehen- und Typ-Dex-Listen.
- `src/Base_Stats.c`: Base-Stats-Tabelle indiziert nach interner Species-ID.
- `src/Evolution Table.c`: Evolutionstabelle indiziert nach interner Species-ID.
- `src/Learnsets.c`: Level-up-Learnsets indiziert nach interner Species-ID.
- `offsets.ini`: generierte Symbol-/Tabellenadressen nach einem lokalen Insertionslauf.

CFRU-expansion ist der primaere Source-of-Truth fuer Engine-, Battle-, Item-, Wild- und Laufzeitverhalten. Der README nennt den Gen9-Umfang (`Pokedex: 1025`, `Species: 1439`, `Items: 798`, `Abilities: 288`) und empfiehlt DPE Gen9 als Basis. Fuer die aktuelle Randomizer-Kompatibilitaet sind besonders wichtig:

- `include/constants/species.h`: CFRU-interne Species-Konstanten spiegeln den DPE-Gen9-ID-Raum.
- `include/wild_encounter.h`: Vanilla-kompatible Wild-Datenstrukturen mit `u16 species`.
- `src/wild_encounter.c`: Laufzeitentscheidung fuer Day/Night-Header, Fallback auf `gWildMonHeaders`, Encounter-Indexwahl und `CreateWildMon`.
- `src/Tables/wild_encounter_tables.c`: CFRU-Custom-Morning/Day/Evening/Night-Header. Im aktuellen Workspace-Kompatibilitaetsstand ist `FIRERED_GEN9_ENABLE_ROUTE1_CUSTOM_WILD 0`, dadurch fallen Route-1-Custom-Wilddaten auf Vanilla/Fallback zurueck.
- `src/Tables/trainer_data.c` und `src/Tables/trainer_parties.h`: Trainer-Daten.
- `src/Tables/level_up_learnsets.c`, `pokemon_tables.c` und DPE-Tabellen: Learnsets, Species-Tabellen und verwandte Daten.

Die generierten `offsets.ini`-Dateien sind fuer externe Tools nur dann belastbar, wenn sie zum konkret gebauten lokalen Teststand passen. Sie sind kein Ersatz fuer ein UPR-FVX-ROM-Profil, aber eine wichtige Quelle fuer spaetere Tabellenmodellierung.

## UPR-FVX-Workflowmodell

FVX ist modular getrennt: `romio` liest und schreibt ROM-Daten, `random` enthaelt Settings, GUI/CLI, Randomizer-Logik und Logger.

Der relevante Ablauf fuer den lokalen CFRU/DPE-Teststand:

1. `CliRandomizer` oder GUI laedt Settings und ROM.
2. `RomOpener` erkennt den passenden RomHandler ueber ROM-Code/Version und die `gen3_offsets.ini`.
3. `Gen3RomHandler.midLoadingSetUp()` aktiviert fuer veraenderte BPRE-1.0-ROMs `basicBPRE10HackSupport()`.
4. `basicBPRE10HackSupport()` erkennt `PokemonCount`, Moves, Trainer und wichtige Tabellen nicht DPE-spezifisch, sondern heuristisch ueber Namen, Moveset-Pointer, PokedexOrder und bekannte Pointer.
5. `loadPokemonNames()`, `loadPokedexOrder()` und `loadSpeciesStats()` erzeugen `pokesInternal`, `pokes` und `speciesList`.
6. PR #3 setzt fuer erweiterte BPRE-Hacks eine separate `SpeciesSet`-Identitaet auf die interne Species-ID, damit `speciesList` nicht auf den kompakten Dex-Raum kollabiert.
7. `Settings.tweakForRom()` passt Settings an die ROM-Generation an.
8. `GameRandomizer.setupSpeciesRestrictions()` setzt den `RestrictedSpeciesService`.
9. Die eigentlichen Randomizer verwenden entweder direkt den RomHandler oder die eingeschraenkten Sets aus `RestrictedSpeciesService`.
10. `RandomizationLogger` schreibt das finale Log; Wild-`<unknown>` kommt derzeit nur aus null Species im Encounter-Objekt, der Rohwert steht in den temporaeren stderr-Diagnosen aus `Gen3RomHandler`.

## Species-ID-Modell

### Interne Species-ID

Die interne Species-ID ist die ROM-Tabellenidentitaet. In CFRU/DPE ist sie der `SPECIES_*`-Wert aus `include/species.h` bzw. `include/constants/species.h`; in UPR-FVX ist sie der Index in `pokesInternal`. Wild-Encounter-Rohwerte, Trainer-Species, Starters, BaseStats, Learnsets und Evolutions zeigen auf diesen Raum.

Diagnosebefund:

- `PokemonCount=823`
- `maxInternalSpeciesId=823`
- Beispiel: `SPECIES_SKRELP = 0x31E = 798`; die Diagnose sah Skrelp bei Internal ID `798`.

### Dex-/Pokedex-ID

Die Dex-ID ist der National-/Pokedex-Wert. FVX `Gen3RomHandler` liest `PokedexOrder` und setzt `Species.number` auf `internalToPokedex[i]`. Im lokalen Teststand blieb dieser Raum kompakt:

- `pokedexCount=386`
- `maxSpeciesNumber=411`
- Skrelp bis Hawlucha hatten Dex-/Species-Nummern `387` bis `398`, obwohl ihre internen IDs `798` bis `809` waren.

`Species.number` muss deshalb fuer Gen3-Schreibpfade vorerst Dex-/Pokedex-ID bleiben, weil viele Pfade weiterhin `pokedexToInternal[species.getNumber()]` verwenden.

### SpeciesSet-Identitaet

Vor PR #3 nutzten `Species.equals()`/`hashCode()` effektiv die `number`. Mehrere interne Species mit kollidierenden/kompakten Dex-Nummern konnten im `SpeciesSet` zusammenfallen. PR #3 fuehrte fuer erweiterte BPRE-Hacks eine separate SpeciesSet-Identitaet ein:

```text
isRomHack && romCode == BPRE && PokemonCount > Gen3Constants.unhackedMaxPokedex
```

In diesem Modus bleibt `Species.number` Dex-basiert, aber `SpeciesSet` unterscheidet nach interner ID. Der diagnostische Effekt:

- `speciesList.size`: `412 -> 799`
- `maxSpeciesIdentityNumber=823`
- Skrelp bis Hawlucha werden als Gen6 statt Gen3 klassifiziert.

### Formes

DPE/CFRU enthaelt viele Formen und Gigantamax-/Regional-/Sonderformen im selben erweiterten Species-Raum. UPR-FVX `Gen3RomHandler` meldet weiterhin keine funktionalen Gen3-Formes im klassischen RomHandler-Sinn. Fuer diese Kompatibilitaet bedeutet das:

- Base-Form- und Forme-Modellierung ist noch nicht abgeschlossen.
- Der aktuelle Gen4+-Wild-Pool-Fokus darf nicht voraussetzen, dass alle DPE-Formen wie moderne FVX-Formes behandelt werden.
- Spaetere Trainer/Starter/Static/Evolution-Tests muessen pruefen, ob Formes als eigenstaendige interne Species stabil gelesen und geschrieben werden.

## Wild-Encounter-Modell

### Vanilla/Fallback

FVX liest Gen3-Wilddaten ueber `romEntry.getIntValue("WildPokemon")`. `Gen3RomHandler.getEncounters()` iteriert `gWildMonHeaders`-artige Eintraege, liest Land/Surf/RockSmash/Fishing-Pointer und loest jede Species ueber `pokesInternal[rawSpecies]` auf. `setEncounters()` schreibt wiederum interne IDs ueber `pokedexToInternal[enc.getSpecies().getNumber()]`.

Die lokalen Smoke-Tests zeigen: Vanilla/Fallback-Wildtabellen werden von FVX erkannt, randomisiert und in BizHawk sichtbar.

### CFRU Day/Night Custom Tables

CFRU `src/wild_encounter.c` priorisiert bei aktivem `TIME_ENABLED` Morning/Day/Evening/Night-Header. Wenn dort kein passender Header existiert, faellt CFRU auf `GetCurrentMapWildMonDaytimeHeader()` und damit auf die Vanilla/Fallback-Header zurueck.

Das erklaert den Route-1-Befund:

- Mit Custom-Day/Night-Route-1-Tabelle kann CFRU die von FVX geaenderten Vanilla/Fallback-Daten zur Laufzeit uebergehen.
- Im aktuellen Kompatibilitaetsbuild ist `FIRERED_GEN9_ENABLE_ROUTE1_CUSTOM_WILD 0`; Route 1 nutzt damit wieder den von FVX randomisierten Fallback.

Day/Night-Custom-Wild ist deshalb ein separates Tabellenmodellierungsproblem und darf nicht mit dem GenRestrictions-Fix vermischt werden.

### `rawInternalSpeciesId=0` Nullslots

Die `<unknown>`-Wild-Log-Zeilen sind nach PR #2/#3 eindeutig kein Gen4+-Species-Mappingproblem. Die stderr-Diagnose sah fuer alle eindeutigen Faelle:

```text
rawInternalSpeciesId=0
```

Das spricht fuer leere/Sonderfall-Slots oder Tabellenbereiche, die FVX aktuell als normale Encounter-Slots loggt. Dieses Thema bleibt P3, nach dem finalen Wild-Pool-Fix.

## GenRestrictions-Problem

PR #3 behebt den RomHandler-Pool, aber nicht den finalen Randomizer-Pool.

Der aktuelle Block `08_tests/randomizer/upr-fvx-gen4plus-wild-pool-diagnostics.md` zeigte:

- RomHandler-Pool: `speciesList.size=799`, `maxSpeciesIdentityNumber=823`.
- Settings wurden mit "alle Generationen" getestet.
- Finaler Wild-Log: Gen1 `841`, Gen2 `527`, Gen3 `791`, Gen4+ `0`, `<unknown>` `17`.

Read-only-Codebefund:

- `Settings.tweakForRom()` ruft fuer valide Gen3-ROMs `currentRestrictions.limitToGen(rh.generationOfPokemon())`.
- `Gen3RomHandler.generationOfPokemon()` ist weiterhin `3`, auch fuer CFRU/DPE-BPRE-Hacks.
- `GameRandomizer.setupSpeciesRestrictions()` ruft immer `romHandler.getRestrictedSpeciesService().setRestrictions(settings.getCurrentRestrictions())`, auch wenn `limitPokemon=false`.
- `RestrictedSpeciesService` filtert dann nach `sp.getBaseForme().getGeneration() == gen`.
- `WildEncounterRandomizer` baut den erlaubten Wild-Pool aus `rSpecService.getSpecies(...)`.

Damit wird ein erweiterter, korrekt geladener CFRU/DPE-Species-Pool nachtraeglich auf Gen1-3 reduziert.

Zusaetzliche Modellgrenze: `GenRestrictions.MAX_GENERATION` ist in FVX aktuell `7`, passend zur offiziellen FVX-Unterstuetzung bis Gen7. Fuer ein echtes Gen9-Ziel muss der naechste Fix mindestens bewusst entscheiden, ob er DPE-Gen8/Gen9 in diesem Settings-Modell abbildet oder fuer den aktuellen lokalen Teststand zunaechst nur den vorhandenen Gen4-Gen6-Pool freigibt.

## Was PR #2 und PR #3 loesen

PR #2 (`analysis/log-cfru-dpe-species-diagnostics`, `6a8ea276`) loest keine Funktionalitaet, aber liefert die temporaeren Diagnosepunkte:

- ROM-Code/Version, `isRomHack`
- `PokemonCount`, `pokedexCount`, `speciesList.size`
- maximale interne ID, maximale Dex-/Species-Nummer
- Counts pro `Species.generation`
- Beispiel-Species ueber 386
- Wild-`<unknown>` mit Area, Encounter-Type, Slot, Roh-ID und Datenoffset

PR #3 (`compat/upr-fvx-gen9-generation-mapping`, `223ee9ef`, gemerged als `c0f623f...`) loest:

- SpeciesSet-Kollaps durch Dex-ID-Kollisionen.
- separate interne SpeciesSet-Identitaet fuer erweiterte BPRE-Hacks.
- `speciesList` aus `pokesInternal` statt dem kollabierenden Dex-Index.
- Gen4+-Generation-Mapping ueber Species-Namen/`SpeciesIDs`.

PR #3 loest nicht:

- GenRestrictions/Settings-Kappung auf Gen3.
- Day/Night-Custom-Wildtabellen.
- Nullslot-`<unknown>`.
- vollstaendige Trainer/Starter/Evolution/Learnset-Kompatibilitaet.
- RAM-/Tracker-Mapping.

## Explizite Antworten

### Ist RAM-Mapping jetzt noetig?

Nein. RAM-Mapping ist jetzt nicht der richtige naechste Schritt. Die offenen Fehler liegen im ROM- und Randomizer-Modell:

- Species-Identitaet und finaler RestrictedSpeciesService-Pool.
- Schreib-/Lese-Semantik fuer Wild, Trainer, Starter, Evolutions und Learnsets.
- CFRU-Day/Night-Tabellen, die Vanilla/Fallback-Wilddaten uebersteuern koennen.

BizHawk/Ironmon-RAM-Mapping wird erst sinnvoll, wenn der Randomizer stabil ROM-Daten erzeugt, die im Spiel sichtbar und reproduzierbar sind.

### Welche ROM-Daten muessen zuerst modelliert werden?

1. Species-Identitaet: interne ID, Dex-ID, SpeciesSet-Identitaet, Namen und Generation.
2. GenRestrictions/finaler Species-Pool: Settings, `RestrictedSpeciesService`, Randomizer-Pool.
3. Vanilla/Fallback-Wildtabellen: interne IDs beim Lesen/Schreiben, Nullslots getrennt behandeln.
4. Trainer-/Starter-/Static-Species: alle Schreibpfade pruefen, die aktuell `pokedexToInternal[species.getNumber()]` verwenden.
5. Evolutions/Learnsets/TM-/Tutor-Kompatibilitaet: besonders kritisch, weil mehrere Pfade mit `speciesList`, `Species.number` und `pokedexToInternal` arbeiten.
6. CFRU-Custom-Day/Night-Wildtabellen: separate Header- und Laufzeit-Override-Quelle.

### Welche CFRU/DPE-Dokumente sind Source-of-Truth?

Primaer die lokalen Planton361-Submodule:

- DPE README fuer Zielumfang und Insertionsmodell.
- DPE `include/species.h`, `include/pokedex.h`, `src/Species_To_Pokdex_Table.c`, `src/Base_Stats.c`, `src/Evolution Table.c`, `src/Learnsets.c`, `src/Pokedex_Orders.c`.
- DPE `offsets.ini` nur passend zum konkret generierten lokalen Teststand.
- CFRU README fuer Engine-Zielumfang.
- CFRU `include/constants/species.h`, `include/wild_encounter.h`, `include/new/wild_encounter.h`, `src/wild_encounter.c`, `src/Tables/wild_encounter_tables.c`, Trainer-/Learnset-/Pokemon-Tabellen und `offsets.ini`.

### Welche UPR-FVX-Codepfade sind Source-of-Truth?

- ROM-Erkennung/Offsets: `RomOpener`, `Gen3RomHandler`, `gen3_offsets.ini`.
- Species-Modell: `Gen3RomHandler`, `Species`, `SpeciesSet`, `SpeciesIDs`, `Gen3Constants`.
- Restrictions: `Settings.tweakForRom()`, `GameRandomizer.setupSpeciesRestrictions()`, `GenRestrictions`, `RestrictedSpeciesService`.
- Wild: `WildEncounterRandomizer`, `Gen3RomHandler.getEncounters()`, `Gen3RomHandler.setEncounters()`, `RandomizationLogger`.
- Trainer/Starter/Evolutions/Learnsets: `TrainerPokemonRandomizer`, `StarterRandomizer`, `EvolutionRandomizer`, `SpeciesMovesetRandomizer` und die entsprechenden Gen3RomHandler-Lese-/Schreibmethoden.

### Welche Fix-Reihenfolge ist sinnvoll?

Zuerst den kleinsten nachgewiesenen Block beheben, dann jeden weiteren Datenbereich separat diagnostizieren. Der GenRestrictions-Fix sollte nicht nebenbei Trainer-, Day/Night- oder Nullslot-Verhalten aendern.

## Priorisierte Roadmap

### P0: GenRestrictions / finaler Gen4+ Wild-Pool

Ziel: Erweiterte CFRU/DPE-BPRE-Hacks duerfen nach PR #3 nicht durch `Settings.tweakForRom()` und `RestrictedSpeciesService` auf Gen1-3 gekappt werden.

Minimaler naechster Fixbranch:

```text
compat/upr-fvx-cfru-dpe-gen-restrictions
```

Entscheidungspunkt:

- Entweder `Settings.tweakForRom()` erkennt erweiterte BPRE-Hacks und kappt nicht blind auf Gen3.
- Oder `GameRandomizer.setupSpeciesRestrictions()` setzt bei `limitPokemon=false` wirklich unrestricted Restrictions (`null`).
- Zusaetzlich klaeren, ob `GenRestrictions.MAX_GENERATION` fuer Gen8/Gen9 erweitert oder fuer den aktuellen Teststand bewusst begrenzt bleibt.

Nachweis: derselbe Gen4+-Wild-Pool-Diagnoselauf muss sichtbare Gen4+-Species im finalen Wild-Log zeigen.

### P1: Trainer, Starters, Evolutions, Learnsets

Ziel: pruefen, welche Gen3RomHandler-Schreibpfade noch Dex-ID-basiert auf `pokedexToInternal[species.getNumber()]` zugreifen und ob sie bei DPE-Species mit kompakter Dex-ID stabil bleiben.

Hohe Risikopfade:

- `setStarters()`
- `setEncounters()`
- `saveTrainers()` / `trainerPokemonToBytes()`
- `getMovesLearnt()` / `setMovesLearnt()`
- `loadEvolutions()` / `saveEvolutions()`
- TM/HM- und Tutor-Kompatibilitaet

### P2: CFRU Day/Night Custom Wild Tables

Ziel: CFRU `gWildMonMorningHeaders`, `gWildMonDayHeaders`, `gWildMonEveningHeaders`, `gWildMonNightHeaders` als separate Wild-Quelle modellieren oder bewusst als nicht unterstuetzt markieren.

Der Vanilla/Fallback-Wild-Fix reicht nicht fuer Maps, auf denen CFRU zur Laufzeit Custom-Day/Night-Header findet.

### P3: Nullslot-`<unknown>`

Ziel: `rawInternalSpeciesId=0` als legitimen leeren/Sonderfall-Slot, Altering-Cave-/Sevii-Sonderdaten oder Lesefehler klassifizieren. Erst danach Logger- oder Lesefix entscheiden.

Wichtig: Nicht mit Gen4+-Pool oder Day/Night-Tabellen vermischen.

### P4: Ironmon/BizHawk Tracker/RAM-Mapping

Ziel: RAM- und Tracker-Kompatibilitaet erst nach stabiler ROM-Randomizer-Kompatibilitaet modellieren.

Voraussetzung:

- Gen4+-Wild-Pool sichtbar.
- Trainer/Starter/Evolutions/Learnsets diagnostiziert.
- CFRU-Custom-Wild-Override geklaert.
- Nullslots verstanden.

## Risiken

- Der lokale Teststand hat `PokemonCount=823`, obwohl DPE/CFRU-Quellen bis Gen9 reichen. Es ist offen, ob der konkrete ROM-Build absichtlich nur bis zu diesem Punkt laedt oder ob weitere DPE-Tabellen durch FVX-Heuristiken abgeschnitten werden.
- `Species.number` bleibt Dex-basiert. Viele Gen3-Schreibpfade nutzen weiterhin `pokedexToInternal[species.getNumber()]`; das kann fuer Species mit kollidierenden oder nicht eindeutigen Dex-IDs kritisch sein.
- `GenRestrictions.MAX_GENERATION=7` passt nicht zum Gen9-Ziel.
- CFRU-Day/Night-Header koennen FVX-randomisierte Vanilla/Fallback-Wilddaten im Spiel uebergehen.
- DPE-Formes werden aktuell nicht als klassische FVX-Gen3-Formes modelliert.
- Die temporaeren CFRU/DPE-Diagnoseausgaben aus PR #2/#3 sollten vor einem langfristigen UPR-FVX-Kompatibilitaetszweig entweder entfernt, hinter ein Debug-Flag gelegt oder bewusst als temporaer markiert bleiben.
