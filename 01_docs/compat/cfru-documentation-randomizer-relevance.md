# CFRU Documentation Randomizer Relevance

## Datum

2026-05-11

## Arbeitsbranch

`analysis/cfru-documentation-randomizer-relevance`

## Ziel und Sicherheitsrahmen

Dieses Dokument extrahiert die projektrelevanten Erkenntnisse aus `02_external/CFRU-expansion/CFRU Documentation.pdf` fuer die UPR-FVX/CFRU/DPE-Kompatibilitaet. Der Arbeitsblock ist read-only: keine Codeaenderungen, keine Builds, keine ROM-Zugriffe, keine Release-Assets und keine Aenderungen in `02_external/**`.

Die PDF wurde lokal gelesen und mit den vorhandenen Workspace-Modellen abgeglichen:

- `01_docs/compat/cfru-dpe-upr-fvx-compatibility-model.md`
- `01_docs/compat/randomizer-natdex-reference-sources.md`
- `01_docs/compat/randomizer-workflow-model.md`
- `01_docs/compat/natdex-reference-implementation-notes.md`

## Kurzfazit

Die CFRU-Dokumentation bestaetigt, dass CFRU nicht nur eine Datenexpansion ist, sondern ein eigenes Laufzeitmodell mit Flags, Time-of-Day-Wild-Tabellen, Swarms, Roamers, Save-Erweiterung, Trainer-EV-Spreads und optionalen In-Game-Randomizer-Flags. Fuer UPR-FVX heisst das:

- P0 bleibt Settings/GenRestrictions/finaler Wild-Pool.
- P1 muss Trainer, Starters, Evolutions, Learnsets, TM/HM, Tutor und Ability-Daten getrennt diagnostizieren.
- P2 muss CFRU-Time-of-Day-Wild-Header separat modellieren.
- P3 bleibt Nullslot-`<unknown>`.
- P4 bleibt BizHawk/Ironmon/RAM-Mapping, weil Save-/RAM-Erweiterungen erst nach stabiler ROM-Randomizer-Kompatibilitaet sinnvoll sind.

## DPE vor CFRU

Die CFRU-Dokumentation beschreibt die empfohlene Reihenfolge klar: Erst DPE und andere Basis-Hacks in die eigentliche Projekt-ROM einbauen, danach CFRU gegen eine Vanilla-FireRed-ROM am geplanten Offset erzeugen und die generierten Offsets/Tabellenuebernahmen in die DPE-basierte Projekt-ROM uebertragen.

Relevanz fuer dieses Projekt:

- DPE ist der primaere Source-of-Truth fuer den erweiterten Species-/Dex-/BaseStats-/Evolution-/Learnset-Raum.
- CFRU ist der primaere Source-of-Truth fuer Engine-, Runtime-, Wild-, Trainer-, Item-, Move-, Ability- und Save-Verhalten.
- UPR-FVX darf den lokalen Teststand nicht wie eine normale Vanilla-BPRE-ROM behandeln, sondern muss DPE-Datenmodell und CFRU-Laufzeitmodell getrennt respektieren.
- Generierte `offsets.ini`-Dateien sind nur fuer den konkret gebauten lokalen Stand belastbar.

## Defines und ID-Raeume

### Species Defines

Die CFRU-Dokumentation verweist darauf, dass Species-Defines auch in Assembly-Konstanten gespiegelt werden muessen. Im lokalen CFRU/DPE-Stand sind die relevanten Source-of-Truth-Pfade:

- `02_external/CFRU-expansion/include/constants/species.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`
- `02_external/CFRU-expansion/asm_defines.s`

Der konkrete lokale Stand zeigt:

- `SPECIES_NONE = 0x0`
- `SPECIES_SKRELP = 0x31E`
- `SPECIES_PECHARUNT = 0x59F`
- `NUM_SPECIES = SPECIES_PECHARUNT + 1`

Folge fuer UPR-FVX:

- Interne Species-ID ist die ROM-Tabellenidentitaet.
- `SPECIES_NONE=0` darf nie als echte Species behandelt oder randomisiert werden.
- PR #3 ist weiterhin die richtige Richtung: `Species.number` bleibt Dex-/Pokedex-ID, `SpeciesSet`-Identitaet kann fuer erweiterte BPRE-Hacks die interne ID sein.

### Pokedex Defines

Pokedex-Defines bilden den Dex-/Anzeige-Raum ab. Im lokalen Modell sind sie nicht deckungsgleich mit der internen Species-ID. Das passt zum bisherigen Diagnosebefund:

- `PokemonCount=823`
- `pokedexCount=386`
- `maxSpeciesIdentityNumber=823`
- `maxSpeciesNumber=411`

Folge fuer UPR-FVX:

- Dex-ID darf nicht als eindeutige SpeciesSet-Identitaet fuer CFRU/DPE-Hacks verwendet werden.
- Schreibpfade, die `pokedexToInternal[species.getNumber()]` nutzen, bleiben P1-Risiko.
- P0 darf diese ID-Schreibpfade nicht nebenbei umbauen.

### `asm_defines.s`

Die PDF macht deutlich, dass C-Defines und Assembly-Defines synchron bleiben muessen. Fuer externe Tools ist das ein Hinweis: Nicht nur C-Header koennen Source-of-Truth sein, sondern auch ASM-Konstanten und generierte Symbole.

Folge fuer spaetere Fixes:

- Wenn UPR-FVX langfristig CFRU/DPE-Tabellen anhand von Symbolen oder Offsets erkennt, muessen C-Header, `asm_defines.s` und generierte `offsets.ini` zusammen betrachtet werden.
- Fuer P0 ist das noch nicht noetig, weil der Fix nur Settings/Restrictions betrifft.

## Harte Species-Spezialfaelle

Die CFRU-Dokumentation listet viele Species, die wegen Vanilla-Code, Breeding, Signature Items, Formwechseln, Signature Abilities, Roamern oder Sondermoves nicht beliebig verschoben oder entfernt werden sollen. Beispiele aus dieser Kategorie sind:

- `SPECIES_NONE`: Null-/Leerwert.
- Vanilla-Roamer wie Bulbasaur/Charmander/Raikou/Entei/Suicune in FireRed-Codepfaden.
- Breeding-Sonderfaelle wie Nidoran, Baby-Pokemon und Incense-Abhaengigkeiten.
- Ditto fuer Daycare.
- Unown, Burmy, Cherrim, Castform, Rotom, Shaymin, Darmanitan, Keldeo, Meloetta, Aegislash, Zygarde, Wishiwashi, Minior und Mimikyu wegen Form-/Ability-Logik.
- Primal-, Mega-, Ultra- und Gigantamax-Formen wegen Evolutions-/Battle-Runtime.

Randomizer-Gefahr:

- Ein externer Randomizer darf den erweiterten Species-Pool nicht nur als flache Liste behandeln.
- Banned-/Special-Case-Tabellen muessen spaeter bewusst ausgewertet werden.
- P0 darf keine neuen Spezialfall-Entscheidungen treffen. Der Erfolg von P0 ist nur, dass Gen4+ ueberhaupt in den finalen erlaubten Wild-Pool gelangen koennen.

## CFRU-interne Randomizer-Optionen

Die CFRU-Dokumentation beschreibt eigene In-Game-Randomizer-Flags:

| Symbol | Bedeutung fuer CFRU | Relevanz fuer UPR-FVX |
|---|---|---|
| `FLAG_POKEMON_RANDOMIZER` | CFRU kann beim Erzeugen von Pokemon Species austauschen | Darf nicht mit UPR-FVX-Offline-Randomisierung verwechselt werden |
| `FLAG_POKEMON_LEARNSET_RANDOMIZER` | CFRU kann Level-up-Learnsets randomisieren | P1-Learnset-Tests muessen klaeren, ob diese Flag aktiv/inaktiv ist |
| `FLAG_ABILITY_RANDOMIZER` | CFRU kann Faehigkeiten beim Erzeugen austauschen | P1-Ability-Diagnose, nicht P0 |
| `NUM_SPECIES_RANDOMIZER` | Obergrenze fuer CFRU-eigenes Randomizer-Species-Sampling | Separat von UPR-FVX `PokemonCount`/`speciesList` behandeln |
| `gRandomizerSpeciesBanList` | CFRU-Species-Banliste fuer Runtime-Randomizer | Spaetere Banned-Species-Referenz |
| `gRandomizerAbilityBanList` | CFRU-Ability-Banliste fuer Runtime-Randomizer | Spaetere Ability-Randomizer-Referenz |

Konkreter lokaler Codebezug:

- `02_external/CFRU-expansion/src/config.h`
- `02_external/CFRU-expansion/src/build_pokemon.c`
- `02_external/CFRU-expansion/src/Tables/pokemon_tables.c`

Folge fuer dieses Projekt:

- UPR-FVX randomisiert offline ROM-Tabellen; CFRU kann zusaetzlich zur Laufzeit randomisieren.
- Fuer reproduzierbare UPR-FVX-Tests muessen CFRU-Runtime-Randomizer-Flags bewusst deaktiviert oder dokumentiert sein.
- `NUM_SPECIES_RANDOMIZER` ist kein Ersatz fuer UPR-FVX-Species-Loading.

## Time-of-Day-Wild-Encounter-System

CFRU erweitert Vanilla-Wild-Encounters um Tageszeit-Header:

- `gWildMonMorningHeaders`
- `gWildMonDayHeaders`
- `gWildMonEveningHeaders`
- `gWildMonNightHeaders`

Die Runtime in `src/wild_encounter.c` waehlt bei aktivem Time-System den passenden Header. Wenn fuer eine Map keine Tageszeitdaten vorhanden sind, faellt CFRU auf die Standard-Day-/Vanilla-Daten zurueck.

Folge fuer UPR-FVX:

- FVX sieht aktuell primaer die Vanilla/Fallback-Wild-Daten.
- Randomisierte Vanilla-Daten koennen im Spiel unsichtbar bleiben, wenn CFRU fuer dieselbe Map aktive Morning/Day/Evening/Night-Header nutzt.
- Der Route-1-Fallback-Befund passt exakt dazu: Deaktivierte Route-1-Custom-Wilddaten machen die FVX-randomisierten Fallback-Daten wieder sichtbar.
- P2 muss CFRU-Day/Night-Wild-Header separat lesen/schreiben oder bewusst als unsupported markieren.

## Swarms und Roamers

Swarms und Roamers sind eigene Wild-Systeme, nicht nur normale Encounter-Slots:

- `gSwarmTable` liegt in `src/Tables/wild_encounter_tables.c`.
- CFRU-Roamer-Support liegt in `src/roamer.c` und `include/new/roamer.h`.
- Bei `SAVE_BLOCK_EXPANSION` unterstuetzt CFRU mehrere Roamer; ohne Save-Erweiterung faellt die Kapazitaet anders aus.

Folge fuer UPR-FVX:

- Swarms und Roamers duerfen nicht als Teil des P0-Wild-Pools behandelt werden.
- Roamer-Species sind fuer Tracker/RAM spaeter relevant, weil CFRU eigene Speicherbereiche nutzt.
- Eine Randomizer-Unterstuetzung fuer Swarms/Roamers waere ein eigener Folgeblock nach P2.

## TM/HM und Move Tutor Expansion

Die CFRU-Dokumentation nennt zwei wichtige Erweiterungen:

- `EXPANDED_TMSHMS`: bis zu 128 TM/HM-Eintraege.
- `EXPANDED_MOVE_TUTORS`: Tutor-Erweiterung ueber Vanilla hinaus.

DPE verwaltet TM-/Tutor-Kompatibilitaet ueber eigene Tabellen/Dateien. Die PDF weist darauf hin, dass bei DPE-Nutzung die bereitgestellten DPE-TM-Dateien gepflegt werden sollen.

Folge fuer UPR-FVX:

- TM/HM/Tutor-Kompatibilitaet ist P1, nicht P0.
- FVX-Gen3-Annahmen zu Tabellenbreite und Move-/Item-Indexraeumen muessen separat gegen den lokalen CFRU/DPE-Teststand geprueft werden.
- Keine P0-Aenderung darf TM-/Tutor-Tabellen anfassen.

## `EXPAND_MOVESETS` vs. DPE-Learnsets

CFRU kann mit `EXPAND_MOVESETS` eigene Level-up-Learnsets aus `src/Tables/learnsets.c` nutzen. Die Dokumentation weist zugleich darauf hin, dass dieses Define nicht genutzt werden sollte, wenn stattdessen DPE-Learnsets massgeblich sein sollen.

Folge fuer UPR-FVX:

- Learnsets sind nicht automatisch eindeutig, solange unklar ist, ob CFRU- oder DPE-Learnset-Tabellen im konkreten Build aktiv sind.
- Der lokale DPE-Pfad `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Learnsets.c` bleibt fuer DPE massgeblich.
- P1 muss zuerst die aktive Learnset-Quelle im konkreten Build bestimmen, bevor FVX-Learnset-Randomization bewertet wird.

## Hidden Ability im BaseStats-Byte `0x1A`

Die CFRU-Dokumentation beschreibt Hidden Abilities als Erweiterung im BaseStats-Datensatz. Im lokalen DPE-Header ist das sichtbar:

- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/base_stats.h`
- Feld `hiddenAbility` bei Offset `0x1A`

Folge fuer UPR-FVX:

- FVX darf bei CFRU/DPE-BaseStats nicht von reinen Vanilla-Gen3-Ability-Feldern ausgehen.
- Ability-Randomization ist P1 und muss `ability1`, `ability2` und `hiddenAbility` getrennt pruefen.
- `FLAG_ABILITY_RANDOMIZER` ist CFRU-Runtime-Verhalten und getrennt von offline FVX-Ability-Randomization.

## `TRAINERS_WITH_EVS` und Trainer-Spread-Risiken

CFRU kann Trainer-Pokemon anhand bestimmter Bedingungen mit EV-/IV-/Nature-/Ability-/Ball-Spreads aus `gTrainersWithEvsSpreads` erzeugen. Die Dokumentation beschreibt, dass Custom Moveset, Custom Item und ein als EV/IV-Wert genutzter Spread-Index zusammenspielen.

Konkrete Pfade:

- `02_external/CFRU-expansion/src/Tables/trainers_with_evs_table.h`
- `02_external/CFRU-expansion/src/build_pokemon.c`
- `02_external/CFRU-expansion/src/Tables/trainer_data.c`
- `02_external/CFRU-expansion/src/Tables/trainer_parties.h`

Folge fuer UPR-FVX:

- Trainer-Randomization darf nicht nur Species/Moves betrachten.
- FVX-Schreibpfade koennen unabsichtlich Spread-Indizes, held-item-Markierungen oder custom-moveset-Bedingungen beeinflussen.
- P1 braucht eigene Trainer-Diagnosen, insbesondere wenn FVX Trainer-Species, Moves, Items, Abilities oder IV/EV-Werte veraendert.

## Save Expansion und RAM-/Ironmon-Relevanz

CFRU erweitert Save-/Runtime-Daten, darunter zusaetzliche Flags, Vars, PC-Boxen, Roamer-Daten und weitere Engine-Features. `include/new/roamer.h` zeigt, dass Roamer-Speicherung je nach `SAVE_BLOCK_EXPANSION` unterschiedlich modelliert ist.

Folge fuer dieses Projekt:

- RAM-/Ironmon-Mapping ist real relevant, aber nicht P0.
- Vor Tracker-Arbeit muessen Randomizer-Ausgaben stabil und im Spiel sichtbar sein.
- P4 muss Save-Expansion, Roamer-Speicher, DexNav-/Map-/Wild-Runtime und BizHawk-RAM-Adressen zusammen betrachten.

## Table Compendium als Source-of-Truth-Landkarte

Das CFRU Table Compendium ist fuer dieses Projekt eine Landkarte, keine fertige UPR-FVX-Implementierung. Es zeigt, welche Tabellen fuer Randomizer-Kompatibilitaet spaeter gezielt modelliert werden muessen:

| Bereich | CFRU-Tabelle/Pfad | Roadmap-Relevanz |
|---|---|---|
| Randomizer-Banlisten | `gRandomizerSpeciesBanList`, `gRandomizerAbilityBanList` in `src/Tables/pokemon_tables.c` | P1 Bans/Special Cases |
| Time Wild | `gWildMonMorningHeaders`, `gWildMonEveningHeaders`, `gWildMonNightHeaders` in `src/Tables/wild_encounter_tables.c` | P2 |
| Swarms | `gSwarmTable` in `src/Tables/wild_encounter_tables.c` | nach P2 |
| Trainer EV-Spreads | `gTrainersWithEvsSpreads` in `src/Tables/trainers_with_evs_table.h` | P1 Trainer |
| Learnsets | `gLevelUpLearnsets` in `src/Tables/level_up_learnsets.c` oder DPE `src/Learnsets.c` | P1 Learnsets |
| Species/BaseStats | DPE/CFRU BaseStats und species defines | P1 Species/Abilities |
| Battle/Wild Music | Wild-species battle music tables | spaeter optional |

## Folgen fuer die Roadmap

### P0: GenRestrictions/finaler Gen4+ Wild-Pool

Minimaler Fix bleibt:

- erweiterte CFRU/DPE-BPRE-Hacks erkennen,
- `Settings.tweakForRom()` nicht blind auf `generationOfPokemon() == 3` kappen lassen,
- finalen `RestrictedSpeciesService`-Pool so setzen, dass Gen4+ aus dem RomHandler-Pool erreichbar bleiben.

Nicht in P0:

- CFRU-Runtime-Randomizer-Flags,
- Day/Night-Wild-Header,
- Swarms/Roamers,
- Trainer-Spread-Logik,
- Learnsets/TM/Tutor,
- Hidden Ability,
- Save-/RAM-/Tracker-Mapping.

### P1: Trainer, Starters, Evolutions, Learnsets, TM/Tutor, Abilities

P1 muss aus der CFRU-Dokumentation mindestens diese Risiken aufnehmen:

- harte Species-Spezialfaelle und Banlisten,
- `pokedexToInternal[species.getNumber()]`-Schreibpfade,
- `EXPAND_MOVESETS` vs. DPE-Learnsets,
- `EXPANDED_TMSHMS`/`EXPANDED_MOVE_TUTORS`,
- Hidden Ability bei BaseStats `0x1A`,
- `TRAINERS_WITH_EVS` und Spread-Indizes.

### P2: CFRU Day/Night Custom Wild Tables

P2 muss die vier CFRU-Time-of-Day-Header und Fallback-Semantik modellieren. Erfolgskriterium ist, dass FVX-randomisierte Wilddaten zur selben Tabelle passen, die CFRU zur Laufzeit wirklich verwendet.

### P3: Nullslot-`<unknown>`

`SPECIES_NONE=0` bestaetigt die bisherige Interpretation: `<unknown>` mit `rawInternalSpeciesId=0` ist ein Null-/Leerslot-Thema. Das bleibt getrennt vom GenRestrictions-Fix.

### P4: BizHawk/Ironmon Tracker/RAM-Mapping

P4 muss Save Expansion, Roamers, DexNav, Time-of-Day und CFRU-RAM-Adressen gemeinsam bewerten. Das ist erst sinnvoll, wenn P0/P1/P2 die ROM-/Randomizer-Ausgaben stabil machen.

## Naechster minimaler Schritt

Weiterhin:

```text
compat/upr-fvx-cfru-dpe-gen-restrictions
```

Ziel: Nur den finalen Gen4+-Wild-Pool fuer erweiterte CFRU/DPE-BPRE-Hacks freigeben. Keine CFRU-Day/Night-Wild-, Nullslot-, Trainer-, Learnset-, TM/Tutor-, Ability- oder RAM-Fixes im selben Branch.
