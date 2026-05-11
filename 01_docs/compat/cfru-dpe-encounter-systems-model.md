# CFRU/DPE Encounter Systems Model

## Datum

2026-05-12

## Arbeitsbranch

`analysis/upr-fvx-cfru-dpe-p1-encounter-systems`

## Ziel und Sicherheitsrahmen

Read-only Diagnose der Encounter-Systeme nach abgeschlossenem P0. Dieser Block nimmt keine Codeaenderungen, keine Builds und keine ROM-Zugriffe vor.

Vorbedingungen:

- Workspace PR #36 ist gemerged.
- UPR-FVX `compat/firered-gen9-cfru-dpe` enthaelt PR #3, PR #4 und PR #5.
- P0 ist fuer Vanilla/Fallback-Wild mit sichtbaren Gen4+-Wild-Encounters bestaetigt.

## Kurzfazit

UPR-FVX randomisiert aktuell die Gen3-Standard-Wildtabellen, also `gWildMonHeaders`-kompatible Walking/Grass-Cave-, Surfing-, Rock-Smash- und Fishing-Slots. Nach P0 sind diese Vanilla/Fallback-Daten fuer erweiterte CFRU/DPE-BPRE-Hacks supported, inklusive Gen4+ und interner Species-Identitaet.

CFRU fuegt mehrere Laufzeitsysteme hinzu, die FVX nicht direkt modelliert:

- Time-of-Day-Wild-Header koennen Standarddaten fuer Morning/Day/Evening/Night uebersteuern.
- Swarms koennen Land-Encounters zur Laufzeit ersetzen oder ergaenzen.
- Roamers koennen Land-/Water-Encounters vor dem normalen Wild-Mon abfangen.
- DexNav liest lokale Wild-/Swarm-Daten und erzeugt eigene suchbare Encounters.
- Wild Double Battles sind ein Laufzeitmodus ueber Flags und zweite Wild-Erzeugung.
- Raid Encounters haben eigene Tabellen und Battle-Erzeugung.
- Altering Cave und Tanoby Ruins sind Vanilla-Sonderfaelle im CFRU-Wildpfad.

Der naechste echte Fix sollte nicht Day/Night sein, solange P1-Trainer/Starters/Static/Evolution/Learnset-Schreibpfade noch ungeprueft sind. Fuer den Kompatibilitaetsbuild sollten CFRU-Day/Night-Custom-Wild, Swarms, DexNav, Raids und zusaetzliche Runtime-Randomizer-Effekte vorerst als unsupported oder bewusst deaktiviert gelten, damit P0 reproduzierbar bleibt.

## Source-of-Truth-Pfade

UPR-FVX:

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/WildEncounterRandomizer.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/log/RandomizationLogger.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/EncounterArea.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/EncounterType.java`

CFRU/DPE:

- `02_external/CFRU-expansion/include/wild_encounter.h`
- `02_external/CFRU-expansion/include/new/wild_encounter.h`
- `02_external/CFRU-expansion/src/wild_encounter.c`
- `02_external/CFRU-expansion/src/Tables/wild_encounter_tables.c`
- `02_external/CFRU-expansion/src/roamer.c`
- `02_external/CFRU-expansion/include/new/roamer.h`
- `02_external/CFRU-expansion/src/dexnav.c`
- `02_external/CFRU-expansion/src/dynamax.c`
- `02_external/CFRU-expansion/include/new/dynamax.h`
- `02_external/CFRU-expansion/src/Tables/raid_encounters.h`

Referenzen:

- `02_external/references/pret-pokefirered/include/wild_encounter.h`
- `02_external/references/pret-pokefirered/src/wild_encounter.c`
- `02_external/references/pret-pokefirered/src/wild_pokemon_area.c`
- `02_external/references/cyansmp64-pokefirered-natdex/include/wild_encounter.h`
- `02_external/references/cyansmp64-pokefirered-natdex/tools/inigen/inigen.c`

## UPR-FVX Standard-Wild-Modell

`Gen3RomHandler.getEncounters()` liest den `WildPokemon`-Offset aus dem ROM-Entry und iteriert `WildPokemonHeader`-Eintraege mit 20 Byte:

- `mapGroup`
- `mapNum`
- Pointer auf Walking/Land
- Pointer auf Surfing/Water
- Pointer auf Rock Smash
- Pointer auf Fishing

FVX erzeugt daraus `EncounterArea`-Objekte:

- Walking/Land: `EncounterType.WALKING`
- Surfing/Water: `EncounterType.SURFING`
- Rock Smash: `EncounterType.INTERACT`
- Fishing: `EncounterType.FISHING`

Jeder Encounter-Slot ist Gen3-kompatibel aufgebaut:

```text
u8 minLevel
u8 maxLevel
u16 species
```

Nach PR #5 schreibt `Gen3RomHandler.writeEncounterArea()` fuer erweiterte CFRU/DPE-BPRE-Hacks die interne SpeciesSet-Identitaet. Vanilla und normale Gen3-Hacks bleiben auf dem bisherigen Dex-/Pokedex-Schreibpfad.

`WildEncounterRandomizer` kennt keine CFRU-spezifischen Zusatzsysteme. Er ruft nur:

```text
romHandler.getEncounters(useTimeOfDay)
romHandler.setEncounters(useTimeOfDay, encounterAreas)
```

Fuer Gen3 ignoriert `Gen3RomHandler` den `useTimeOfDay`-Parameter effektiv, weil der Handler keine CFRU-Time-of-Day-Header modelliert.

## CFRU Runtime-Wild-Modell

CFRU nutzt weiter die Vanilla-kompatible `WildPokemonHeader`-Struktur aus `include/wild_encounter.h`, erweitert aber den Runtime-Pfad in `src/wild_encounter.c`.

`GetCurrentMapWildMonHeader()` arbeitet grob so:

1. Wenn `gWildDataSwitch` einen echten Pointer enthaelt, wird dieser Header direkt verwendet.
2. Bei `TIME_ENABLED` wird passend zur Tageszeit in `gWildMonNightHeaders`, `gWildMonMorningHeaders`, `gWildMonEveningHeaders` oder `gWildMonDayHeaders` gesucht.
3. Wenn kein Time-of-Day-Header passt, faellt CFRU auf `GetCurrentMapWildMonDaytimeHeader()` zurueck.
4. `GetCurrentMapWildMonDaytimeHeader()` sucht in `gWildMonHeaders`, also in den Vanilla/Fallback-Daten, die FVX aktuell randomisiert.

`LoadProperMonsData()` verwendet den aktuellen Header und faellt bei fehlendem Time-of-Day-Teilheader nochmals auf den Daytime-/Fallback-Header zurueck. Dadurch kann CFRU pro Encounter-Typ mischen: z. B. Time-of-Day-Landdaten, aber Fallback-Fishingdaten.

## Statusmatrix

| System | Status | Datenquelle | Laufzeitpfad | FVX-Lese-/Schreibstatus | Risiko | Naechster Test/Fix |
|---|---|---|---|---|---|---|
| Standard Wild / Grass-Cave | Supported nach P0 | `gWildMonHeaders` landMonsInfo | `StandardWildEncounter()` -> `LoadProperMonsData(LAND_MONS_HEADER)` -> `TryGenerateWildMon()` | liest/schreibt `EncounterType.WALKING`; Gen4+ und interne ID bestaetigt | Wird von Time-of-Day-Landdaten oder Swarm/Roamer uebersteuert | P1 nicht noetig fuer Standard-Wild; nur Regressionstest spaeter |
| Surfing | Supported nach P0 | `gWildMonHeaders` waterMonsInfo | `StandardWildEncounter()` Water-Zweig | liest/schreibt `EncounterType.SURFING`; interne ID gilt wie fuer alle Standard-Slots | Time-of-Day-Waterdaten, Roamer und DexNav koennen Laufzeitverhalten beeinflussen | gezielter Surfing-Smoke nach P1/P2 |
| Fishing | Supported nach P0 | `gWildMonHeaders` fishingMonsInfo | `FishingWildEncounter()` -> `GenerateFishingWildMon()` | liest/schreibt `EncounterType.FISHING` | CFRU kann Time-of-Day-Fishingdaten liefern; DexNav liest Fishing separat | gezielter Fishing-Smoke nach P1/P2 |
| Rock Smash | Supported nach P0 | `gWildMonHeaders` rockSmashMonsInfo | `RockSmashWildEncounter()`/`LoadProperMonsData(ROCK_SMASH_MONS_HEADER)` | liest/schreibt `EncounterType.INTERACT` | Als `INTERACT` generisch; andere Interact-Systeme sind nicht automatisch abgedeckt | Rock-Smash-Smoke mit Gen4+ Slot |
| CFRU Morning/Day/Evening/Night | Unsupported / separates P2 | `gWildMonMorningHeaders`, `gWildMonDayHeaders`, `gWildMonEveningHeaders`, `gWildMonNightHeaders` | `GetCurrentMapWildMonHeader()` vor Fallback | FVX Gen3 liest/schreibt diese Tabellen nicht | Kann FVX-randomisierte Fallback-Daten komplett uebersteuern | eigener P2-Fix oder im Kompatibilitaetsbuild deaktivieren |
| Swarms | Unsupported / runtime overlay | `gSwarmTable`, `gSwarmTableLength`, `gSwarmOrders` | `TryGenerateSwarmMon()` in Land-Encounters und DexNav | FVX liest/schreibt Swarm-Tabelle nicht | Swarm-Species kann Standard-Landmon ersetzen; eigene Tages-/Indexlogik | vorerst deaktivieren oder als unsupported markieren; spaeter eigener Swarm-Block |
| Roamers | Unsupported / separate runtime state | `src/roamer.c`, `gRoamers`, script `sp129_InitRoamer()` | `TryStartRoamerEncounter()` vor normalem Land/Water | FVX Standard-Wild randomisiert Roamers nicht | Roamer-Species liegen in Save/RAM-State, nicht in Standard-Wildslots | P4/RAM-nahe Analyse; nicht P1-Fix |
| DexNav | Partial / depends on supported base tables | `src/dexnav.c` liest `LoadProperMonsData()` und `gSwarmTable` | DexNav HUD/Battle erzeugt eigene Encounters | FVX schreibt nur die Basis-Wildtabellen, nicht DexNav-spezifische State/GUI-Regeln | DexNav kann randomisierte Fallbackdaten anzeigen, aber Swarms, caught flags, hidden abilities und runtime randomizer beeinflussen Ergebnis | vorerst unsupported fuer Kompatibilitaetsziel; spaeter eigener DexNav-Test |
| Wild Double Battles | Partial runtime mode | gleiche WildPokemonInfo-Slots plus `FLAG_DOUBLE_WILD_BATTLE` / tile flag | `TryGenerateWildMon()` erzeugt zweiten Gegner | FVX randomisiert zugrunde liegende Standard-Slots; keine Double-Flag-Logik | zweiter Slot nutzt gleiche Tabellen, aber Battle-/Party-/Tag-Flags sind CFRU-runtime | erst nach Standard-/P1-Stabilitaet testen |
| Raid Encounters | Unsupported | `src/Tables/raid_encounters.h`, `gRaidsByMapSection` | `DetermineRaidSpecies()`, `sp117_CreateRaidMon()`, `sp118_StartRaidBattle()` | FVX liest/schreibt Raid-Tabellen nicht | eigene Species, Items, Abilities, Drops, Stars, Dynamax-Flags | bewusst unsupported; spaeter eigener Raid-Table-Block |
| Altering Cave | Partial vanilla special | Varianten in `gWildMonHeaders`; `VAR_ALTERING_CAVE_WILD_SET` | `GetCurrentMapWildMonDaytimeHeader()` verschiebt Header-Index | FVX kann Headerdaten lesen/schreiben, kennt aber die Var-Auswahl nicht semantisch | mehrere Header fuer gleiche Map koennen als normale Areas erscheinen; Laufzeitwaehler entscheidet | als special vanilla partial markieren; Test nur nach Basis-Pfade |
| Tanoby / Unown special | Partial vanilla special | `gWildMonHeaders`, `sUnownLetterSlots` | `CanEncounterUnownInTanobyRuins()`, `PickUnownLetter()` | FVX sieht Species-Slots, aber nicht Unown-Letter-Sonderlogik | Letter/Forme-Logik und Flag-Gating werden nicht modelliert | nicht fuer P1; spaeter Spezialfalltest |

## Systemdetails

### Standard Wild / Grass-Cave

Supported. P0 bestaetigt, dass Walking/Grass-Cave-Slots im Route-1-Fallback-Teststand Gen4+-Species enthalten koennen. Der Schreibpfad nutzt bei erweiterten BPRE-Hacks interne SpeciesSet-Identitaet.

Grenze: CFRU `TryGenerateSwarmMon()` kann Land-Encounters zur Laufzeit ersetzen, und `TryStartRoamerEncounter()` kann vor dem normalen Landmon greifen.

### Surfing

Supported fuer die Standardtabelle. FVX liest und schreibt Water/Surfing-Slots aus `gWildMonHeaders`. CFRU verwendet diese Daten, wenn kein passender Time-of-Day-Water-Header vorhanden ist.

Grenze: Roamer koennen auch Water-Encounters abfangen, und DexNav liest Water-Slots fuer eigene Anzeige/Suche.

### Fishing

Supported fuer die Standardtabelle. FVX liest und schreibt die Gen3-Fishing-Slots als `EncounterType.FISHING`. CFRU `GenerateFishingWildMon()` nutzt denselben `WildPokemonInfo`-Slotraum, wenn `LoadProperMonsData(FISHING_MONS_HEADER)` auf die Fallback-Daten zeigt.

Grenze: DexNav trennt Old/Good/Super-Rod-Slots aus derselben Fishing-Tabelle, waehrend FVX diese semantische Unterteilung nicht separat modelliert.

### Rock Smash

Supported fuer die Standardtabelle. FVX behandelt Rock Smash als `EncounterType.INTERACT`, liest und schreibt aber konkret den `rockSmashMonsInfo`-Pointer aus dem Gen3-Header.

Grenze: `INTERACT` ist in FVX generisch. Daraus folgt keine generelle Unterstuetzung fuer alle scripted/static/interact encounters.

### CFRU Time-of-Day Wild

Unsupported und separat zu fixen. CFRU definiert vier Header-Tabellen:

- `gWildMonMorningHeaders`
- `gWildMonDayHeaders`
- `gWildMonEveningHeaders`
- `gWildMonNightHeaders`

Im aktuellen Kompatibilitaetsstand sind diese Tabellen wegen `FIRERED_GEN9_ENABLE_ROUTE1_CUSTOM_WILD 0` leer beziehungsweise nur mit Sentinel belegt. Wenn Custom-Daten aktiv sind, sucht CFRU diese Tabellen vor dem Fallback. FVX schreibt derzeit nur `gWildMonHeaders`; die im Spiel sichtbaren Encounters koennen also von FVX-Daten abweichen.

### Swarms

Unsupported. CFRU `gSwarmTable` enthaelt im lokalen Stand mindestens einen Beispiel-Swarm (`MAPSEC_ROUTE_1`, `SPECIES_FRIGIBAX`). `TryGenerateSwarmMon()` kann bei Land-Encounters mit `SWARM_CHANCE` eine Swarm-Species erzeugen. DexNav bezieht Swarms ebenfalls ein.

FVX kennt diese Tabelle nicht und kann Swarm-Species nicht gezielt randomisieren oder loggen.

### Roamers

Unsupported. Roamers sind Save-/RAM-State und Script-Initialisierung, nicht Standard-Wildtabellen. `sp129_InitRoamer()` verwendet Script-Variablen oder FRLG-Starterlogik, und `TryStartRoamerEncounter()` kann Land-/Water-Encounters vor dem normalen Wildmon abfangen.

Das ist spaeter RAM-/Tracker-nah und gehoert nicht in einen kleinen Wildtable-Fix.

### DexNav

Partial im Sinne von: DexNav liest die lokalen Land/Water/Fishing-Daten ueber `LoadProperMonsData()`, also kann es indirekt FVX-randomisierte Fallbackdaten sehen. Es ist aber nicht FVX-supported, weil DexNav zusaetzlich Pokedex-Flags, Search Levels, Hidden Abilities, Swarms, Unown-Letters, UI-State und eigene Battle-Erzeugung nutzt.

Fuer den aktuellen Kompatibilitaetsbuild sollte DexNav nicht als Randomizer-Erfolgskriterium verwendet werden.

### Wild Double Battles

Partial. Wenn `FLAG_DOUBLE_WILD_BATTLE` gesetzt ist oder entsprechende Tile-/Sweet-Scent-Bedingungen greifen, erzeugt CFRU einen zweiten Wildmon aus denselben Basisdaten. FVX randomisiert diese Basisdaten, aber nicht die Double-Battle-Flags, Chancen, Partner-/Tag-Battle-Regeln oder Battle-Type-Logik.

### Raid Encounters

Unsupported. CFRU-Raids haben eigene Tabellen (`gRaidsByMapSection`) mit `struct Raid`, inklusive Species, Item, Ability und Drops. `DetermineRaidSpecies()` und `sp118_StartRaidBattle()` sind vom Standard-Wildpfad getrennt. FVX liest oder schreibt diese Tabellen nicht.

### Altering Cave / Tanoby / Special Vanilla

Partial. Diese Systeme liegen naeher an Vanilla, aber CFRU hat Sonderlogik:

- Altering Cave verschiebt den Header-Index anhand `VAR_ALTERING_CAVE_WILD_SET`.
- Tanoby Ruins koennen per `CanEncounterUnownInTanobyRuins()` ganz gesperrt sein und haben Unown-Letter-Sonderlogik.

FVX kann die zugrunde liegenden Header lesen/schreiben, kennt aber die Laufzeitbedingungen nicht semantisch.

## Welche Systeme sind P0-supported?

P0-supported:

- Standard Wild / Grass-Cave aus `gWildMonHeaders`
- Surfing aus `gWildMonHeaders`
- Fishing aus `gWildMonHeaders`
- Rock Smash aus `gWildMonHeaders`

P0-supported bedeutet hier: FVX kann die Tabellen lesen, den finalen Species-Pool inklusive Gen4+ nutzen und die Species fuer erweiterte CFRU/DPE-BPRE-Hacks mit interner Identitaet zurueckschreiben.

Nicht P0-supported:

- CFRU Morning/Day/Evening/Night-Custom-Wild
- Swarms
- Roamers
- DexNav als eigenes UX-/Battle-System
- Wild Double Battle Runtime-Flags
- Raids
- Altering Cave/Tanoby als semantisch verstandene Sonderfaelle

## Empfehlung: naechster Fix oder Test

Nicht als naechsten echten Fix Day/Night Custom Wildtables starten.

Begruendung:

- P0 hat Standard/Fallback-Wild stabilisiert.
- P1-Risiko aus den bisherigen Analysen betrifft viele weitere `pokedexToInternal[species.getNumber()]`-Schreibpfade und Species-Identitaetsannahmen bei Trainer, Starter, Static, Evolution und Learnset.
- Day/Night ist wichtig, aber ein eigenes Tabellenmodell. Es sollte nicht mit P1-Schreibpfaden vermischt werden.

Empfohlene Reihenfolge:

1. P1 read-only Diagnose fuer Trainer, Starters, Static Pokemon, Evolutions, Learnsets und verwandte Species-Schreibpfade.
2. Danach kleine Fixbranches fuer die P1-Pfade, falls sie denselben internen-ID-Fehler zeigen.
3. P2 eigener Day/Night-Custom-Wildtable-Analyse- und Fixbranch.
4. Danach Swarms/DexNav/Raids nur bei Bedarf und getrennt.

## Kompatibilitaetsbuild-Policy

Bewusst deaktivieren oder als unsupported markieren:

- CFRU Day/Night Custom Wildtables: im aktuellen Kompatibilitaetsbuild weiter leer/deaktiviert halten, bis P2 umgesetzt ist.
- Swarms: fuer reproduzierbare Wild-Smokes deaktivieren oder nicht als Erfolgskriterium werten.
- DexNav: nicht als Randomizer-Kompatibilitaetsbeweis verwenden.
- Raids: unsupported, nicht randomisiert.
- Roamers: unsupported fuer FVX-Wildrandomization; spaeter P4/RAM-nahe Betrachtung.
- CFRU Runtime-Randomizer-Flags: fuer UPR-FVX-Smokes deaktiviert halten.

Supported lassen:

- Vanilla/Fallback Walking, Surfing, Fishing und Rock Smash aus `gWildMonHeaders`.
- Route-1-Fallback-Macro bleibt sinnvoll, damit FVX-randomisierte Fallbackdaten ingame sichtbar bleiben.

## Risiken

- Der aktuelle lokale Teststand meldet `PokemonCount=823`; nicht der volle Gen9-Raum ist praktisch im Smoke bestaetigt.
- Time-of-Day-Header koennen pro Encounter-Typ partiell fallbacken; ein spaeterer P2-Fix muss Land/Water/Fishing/RockSmash getrennt behandeln.
- Swarms und DexNav verwenden teilweise dieselben Basisdaten, aber mit separatem Runtime-State. Eine naive Randomisierung kann Logs und Ingame-Verhalten auseinanderlaufen lassen.
- Roamers und Raids sind nicht normale Encounter-Slots und duerfen nicht als einfache Erweiterung von `getEncounters()` behandelt werden.

## Naechster minimaler Schritt

Neuer read-only Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-species-write-paths
```

Ziel: Trainer, Starters, Static Pokemon, Evolutions, Learnsets und weitere Species-Schreibpfade systematisch auf interne ID vs. Dex-ID pruefen.
