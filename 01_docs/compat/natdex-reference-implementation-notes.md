# NatDex Reference Implementation Notes

## Datum

2026-05-11

## Arbeitsbranch

`analysis/randomizer-natdex-reference-sources`

## Scope

Kompakte Implementierungsnotizen aus pret FireRed, CyanSMP64 FireRed NatDex, CFRU/DPE und UPR-FVX. Dieser Block ist read-only und enthaelt keine funktionalen Fixes.

## Datenmodellvergleich

| Modell | Species-ID | Dex-ID | Tabellen | Randomizer-Relevanz |
|---|---|---|---|---|
| pret FireRed | kompakter Gen3-Speciesraum, `NUM_SPECIES SPECIES_EGG` | `NATIONAL_DEX_COUNT NATIONAL_DEX_DEOXYS` | `gSpeciesInfo`, `gEvolutionTable`, `gLevelUpLearnsets`, Wild/Trainer-Tabellen | Vanilla-BPRE-Baseline fuer UPR-FVX-Gen3-Pfade |
| CyanSMP64 FireRed NatDex | eigener erweiterter NatDex-Speciesraum, z. B. `SPECIES_PECHARUNT 1050` | `NATIONAL_DEX_COUNT NATIONAL_DEX_TERAPAGOS_STELLAR` | Decomp-Tabellen plus ROM-Header-Metadaten | Referenz fuer zusammen entwickelte ROM- und Randomizer-Erweiterung |
| DPE Gen9 | DPE-interne IDs, z. B. `SPECIES_SKRELP 0x31E`, `SPECIES_PECHARUNT 0x59F` | `NATIONAL_DEX_PECHARUNT 1025`, `NATIONAL_DEX_COUNT FINAL_DEX_ENTRY + 1` | `Base_Stats.c`, `Evolution Table.c`, `Learnsets.c`, Mapping- und Order-Tabellen | Source-of-Truth fuer lokalen CFRU/DPE-Speciesraum |
| CFRU-expansion | spiegelt DPE-ID-Raum, `NUM_SPECIES SPECIES_PECHARUNT + 1` | `NATIONAL_DEX_PECHARUNT 1025` | Engine-, Wild-, Trainer-, Item-, Move-, Ability-Tabellen | Source-of-Truth fuer Laufzeitverhalten und Day/Night-Wild |
| UPR-FVX nach PR #3 | `Species.number` bleibt Dex-ID; `speciesSetIdentityNumber` kann interne ID sein | `PokedexOrder`/`internalToPokedex` | `pokesInternal`, `pokes`, `speciesList`, `SpeciesSet` | externer Randomizer muss ID-Raeume trennen |

## Interne Species-ID vs Dex-ID

Die interne Species-ID ist die Tabellenidentitaet der ROM. In CFRU/DPE zeigen BaseStats, Evolutions, Learnsets, Wild-Encounters, Trainer-Parties, Starters und Static Pokemon auf diesen Raum.

Die Dex-ID ist ein Anzeige-/Pokedex-Raum. Sie ist nicht automatisch identisch mit der internen Species-ID. Im lokalen Diagnosebefund war genau das sichtbar:

- `PokemonCount=823`
- `pokedexCount=386`
- `speciesList.size=799` nach PR #3
- `maxSpeciesIdentityNumber=823`
- `maxSpeciesNumber=411`
- Skrelp bis Hawlucha hatten interne IDs `798..809`, aber Dex-/Species-Nummern `387..398`.

Implementation-Folge:

- Fuer DPE/CFRU-BPRE-Hacks darf `SpeciesSet` nicht nach Dex-ID kollabieren.
- `Species.number` darf nicht nebenbei auf interne ID umgestellt werden, solange Gen3-Schreibpfade `pokedexToInternal[species.getNumber()]` verwenden.
- Langfristig braucht FVX fuer Gen3-Hacks einen klaren Zugriff auf interne Species-ID, statt sie nur ueber `speciesSetIdentityNumber` indirekt zu tragen.

## NUM_SPECIES und Umfang

Vanilla pret FireRed:

- `include/constants/species.h`: `NUM_SPECIES SPECIES_EGG`.
- `include/constants/pokedex.h`: `NATIONAL_DEX_COUNT NATIONAL_DEX_DEOXYS`.
- Tabellen sind grob auf Gen3/Deoxys-Umfang ausgelegt.

CyanSMP64 FireRed NatDex:

- `SPECIES_NACLI 957`, `SPECIES_CYCLIZAR 992`, `SPECIES_PECHARUNT 1050`.
- `NUM_SPECIES SPECIES_EGG`.
- `NATIONAL_DEX_COUNT NATIONAL_DEX_TERAPAGOS_STELLAR`.
- `src/rom_header_gf.c` exportiert Metadaten wie `pokedexCount`, `speciesInfo`, `gLevelUpLearnsets`, `gTrainers`, `sTMHMMoves` und Groessenfelder.

DPE/CFRU:

- DPE: `SPECIES_PECHARUNT 0x59F`, `NUM_SPECIES (SPECIES_PECHARUNT + 1)`.
- CFRU: `NUM_SPECIES_GEN_7`, `NUM_SPECIES_GEN_8`, `NUM_SPECIES (SPECIES_PECHARUNT + 1)`.
- DPE README nennt dynamische Insertion, bis zu `1025` Pokedex-Eintraege ohne Alternate Forms, bis zu `128` TM/HM und `152` Move Tutors.
- CFRU README nennt `Pokedex: 1025`, `Species: 1439`, `Items: 798`, `Abilities: 288`.

## Wild

pret und CyanSMP64 FireRed NatDex:

- `include/wild_encounter.h` deklariert `gWildMonHeaders`.
- `src/wild_encounter.c` sucht den aktuellen Header nach Map Group/Map Num.
- `src/data/wild_encounters.json` liefert die Vanilla-artige Headerquelle.
- Wild-Pokemon tragen `u16 species` und werden ueber `GenerateWildMon`/`TryGenerateWildMon` erzeugt.

CFRU:

- `src/wild_encounter.c` deklariert zusaetzlich `gWildMonMorningHeaders`, `gWildMonDayHeaders`, `gWildMonEveningHeaders`, `gWildMonNightHeaders`.
- `GetCurrentMapWildMonHeader()` waehlt bei aktivem Time-System eine Tageszeit-Tabelle und faellt sonst auf `GetCurrentMapWildMonDaytimeHeader()`/`gWildMonHeaders` zurueck.
- `src/Tables/wild_encounter_tables.c` ist Source-of-Truth fuer CFRU-Custom-Day/Night-Wild.

UPR-FVX:

- `Gen3RomHandler.getEncounters()` liest Vanilla/Fallback-Header aus dem ROM-Profil.
- `setEncounters()` schreibt weiterhin ueber `pokedexToInternal[enc.getSpecies().getNumber()]`.
- P0 betrifft nur den finalen Allowed-Pool, nicht die Day/Night-Custom-Header.

## Trainer

pret/CyanSMP64:

- Trainer-Metadaten: `src/data/trainers.h`.
- Parties: `src/data/trainer_parties.h`.
- Runtime-Zugriff ueber `gTrainers`.

CFRU:

- Trainerdaten liegen in `src/Tables/trainer_data.c` und `src/Tables/trainer_parties.h`.
- CFRU erweitert Difficulty-/Rematch-/Custom-Move-Faelle; die Tabellen muessen separat gegen FVX-Gen3-Schreibpfade diagnostiziert werden.

UPR-FVX-Risiko:

- Gen3-Schreibpfade fuer Trainer nutzen intern weiter Dex-ID-basierte Umrechnung.
- P1 muss pruefen, ob neue Species mit kompakter oder kollidierender Dex-ID korrekt zur internen DPE-ID zurueckgeschrieben werden.

## Evolutions

pret:

- `src/data/pokemon/evolution.h` definiert `gEvolutionTable[NUM_SPECIES][EVOS_PER_MON]`.

DPE:

- `src/Evolution Table.c` definiert ebenfalls `gEvolutionTable[NUM_SPECIES][EVOS_PER_MON]`.
- Enthalten sind moderne Methoden wie Mega, Gigantamax, Location-/Move-/Time-Varianten.

UPR-FVX-Risiko:

- `loadEvolutions()` und `saveEvolutions()` muessen spaeter auf interne ID vs Dex-ID geprueft werden.
- P0 darf Evolutionen nicht aendern.

## Learnsets

pret:

- `src/data/pokemon/level_up_learnset_pointers.h` definiert `gLevelUpLearnsets[NUM_SPECIES]`.

DPE:

- `src/Learnsets.c` nutzt bei `EXPAND_LEARNSETS` gepackte LevelUpMove-Eintraege und `NUM_SPECIES`.

CFRU:

- `src/Tables/level_up_learnsets.c` ist fuer den CFRU-Stand relevant.

UPR-FVX-Risiko:

- Moveset-Pointer werden in der BPRE-Hack-Heuristik bereits zur `PokemonCount`-Validierung genutzt.
- P1 muss `getMovesLearnt()` und `setMovesLearnt()` isoliert pruefen.

## TM/HM und Tutor

pret/CyanSMP64:

- `src/data/pokemon/tmhm_learnsets.h` und `src/data/pokemon/tutor_learnsets.h`.
- `src/data/party_menu.h`/`party_menu.c` enthalten Laufzeitlogik fuer TM/HM und Tutor.

DPE:

- README nennt bis zu `128` TM/HM und `152` Move Tutors.
- `src/tm_compatibility/**` und `src/tutor_compatibility/**` sind nach Move/Tutor-Dateien organisiert, nicht primaer nach Species.
- `include/tutors.h` und `src/TM_Tutor_Tables.c` verbinden Tutor-IDs und Tabellen.

UPR-FVX-Risiko:

- TM/HM- und Tutor-Kompatibilitaet sind P1, weil Tabellenbreite und Species-Indexierung gegen den konkreten CFRU/DPE-ROM-Stand geprueft werden muessen.
- Kein P0-Fix darf diese Tabellen anfassen.

## P0-Fixnotizen fuer GenRestrictions

Minimaler Fix:

- Fuer erweiterte CFRU/DPE-aehnliche BPRE-Hacks darf `Settings.tweakForRom()` die bereits gesetzten Restrictions nicht auf Gen3 reduzieren.
- Die Erkennung sollte dieselbe konservative Bedingung wie PR #3 nutzen oder aus einer kleinen gemeinsamen Hilfsmethode kommen.
- Bei `limitPokemon=false` sollte geprueft werden, ob `GameRandomizer.setupSpeciesRestrictions()` wirklich `setRestrictions(null)` setzen muss. Das ist semantisch sauber, aber potentiell breiter als nur CFRU/DPE.

Nicht im P0-Fix:

- Keine Aenderung an `generationOfPokemon()`.
- Keine Aenderung an `Species.number`.
- Keine Aenderung am Wild-Tabellenleser/-schreiber.
- Keine CFRU-Day/Night-Header.
- Keine Nullslot-`<unknown>`.
- Keine Trainer/Starter/Evolution/Learnset/TM/Tutor-Korrekturen.

Erfolgstests:

- Bestehende ROM-freie Tests fuer `GenRestrictions`/Settings erweitern, falls ohne ROM moeglich.
- Diagnose-Lauf mit bekanntem CFRU/DPE-Teststand wiederholen, erst nach separater Build-/ROM-Freigabe.
- Erfolg: finaler Wild-Log zeigt sichtbare Gen4+-Species; `rawInternalSpeciesId=0` bleibt getrennt.
- Regression vermeiden: Vanilla Gen3 muss weiter auf Gen1-3 begrenzbar bleiben.

## Priorisierte Folgearbeit

P0: GenRestrictions/finaler Gen4+-Wild-Pool.

P1: Trainer, Starters, Evolutions, Learnsets, TM/HM und Tutor.

P2: CFRU Day/Night Custom Wild Tables.

P3: Nullslot-`<unknown>` mit `rawInternalSpeciesId=0`.

P4: BizHawk/Ironmon Tracker/RAM-Mapping.
