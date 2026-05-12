# UPR-FVX CFRU/DPE PokedexOrder Model

## Datum

2026-05-12

## Ziel und Sicherheitsrahmen

Read-only Modellierung des DPE/CFRU-PokedexOrder-/Dex-ID-Layouts und geeigneter Count-Quellen fuer vollstaendige Gen9-Coverage in UPR-FVX.

Dieser Block nimmt keine Codeaenderungen, keine Builds und keine ROM-Zugriffe vor. P1 Static/Gift bleibt pausiert. Der vorherige lokale Diagnosebefund bleibt die Grundlage: `PokemonNames` und `PokemonStats` reichen bis Gen9, aber `basicBPRE10HackSupport()` kappt final bei `PokemonCount=823`, weil `PokedexOrder` bei interner ID `824` den Wert `1808` liefert und FVX `pdEntry > 1023` als Count-Abbruch wertet.

## Kurzfazit

DPE/CFRU trennen mehrere ID-Raeume:

- Interne Species-ID: Tabellenidentitaet fuer Namen, BaseStats, Learnsets, Evolutions, Wild, Trainer, Starter und Forms. DPE/CFRU reichen bis `SPECIES_PECHARUNT = 0x59F`, also `NUM_SPECIES = 1440`.
- National Dex ID: Anzeige-/Pokedex-ID. DPE reicht bis `NATIONAL_DEX_PECHARUNT = 1025`, `NATIONAL_DEX_COUNT = FINAL_DEX_ENTRY + 1`.
- DPE PokedexOrder: Sortierlisten fuer Pokedex-Views, deren Eintraege Species-IDs sind, nicht Dex-IDs.
- FVX PokedexOrder: ein pro interner Species-ID gelesenes `u16`-Mapping nach `Species.number`/Dex-ID.

Die FVX-Heuristik `pdEntry > 1023 => PokemonCount cutoff` ist fuer CFRU/DPE falsch als Count-Quelle. Selbst wenn FVX auf eine echte DPE-Order-Liste zeigen wuerde, waeren dort Species-IDs `>1023` fuer Gen8/Gen9 und Forms normale, valide Werte. Im konkreten Diagnosebefund ist `pdEntry=1808` bei ID `824` zudem kein plausibler Xerneas-Dexwert und kein DPE-Xerneas-Specieswert; das spricht fuer einen nicht passenden Legacy-Offset oder fuer Daten, die FVX mit der falschen Semantik liest.

## Relevante Dateien

| Bereich | Datei | Bedeutung |
|---|---|---|
| DPE interne Species-ID | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h` | `SPECIES_*`, Forms, `NUM_SPECIES = SPECIES_PECHARUNT + 1` |
| CFRU interne Species-ID | `02_external/CFRU-expansion/include/constants/species.h` | gespiegelter DPE-ID-Raum, `NUM_SPECIES_GEN_7`, `NUM_SPECIES_GEN_8`, `NUM_SPECIES` |
| DPE National Dex ID | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/pokedex.h` | `NATIONAL_DEX_*`, `FINAL_DEX_ENTRY`, `NATIONAL_DEX_COUNT` |
| CFRU Dex Count | `02_external/CFRU-expansion/src/config.h` | `NATIONAL_DEX_COUNT 1025`, `NUM_SPECIES_RANDOMIZER NUM_SPECIES` |
| DPE Species-to-Dex | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Species_To_Pokdex_Table.c` | `gSpeciesToNationalPokedexNum[NUM_SPECIES - 1]`, internes Species-Mapping auf National-Dex |
| DPE Pokedex Orders | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Pokedex_Orders.c` | `gPokedexOrder_Regional`, Alphabetical, Weight, Height, Type; Species-ID-Sortierlisten |
| DPE Pokedex Runtime | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/updated_code.c` | nutzt `SpeciesToNationalPokedexNum(gPokedexOrder_Regional[i])` und `NationalPokedexNumToSpecies()` |
| FVX Count/Load | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | `basicBPRE10HackSupport()`, `loadPokedexOrder()`, `loadSpeciesStats()` |
| FVX Gen3 Offsets | `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini` | Vanilla-BPRE `PokedexOrder=0x251FEE` und weitere Legacy-Offsets |
| Cyan FireRed NatDex | `02_external/references/cyansmp64-pokefirered-natdex/tools/inigen/inigen.c`, `src/rom_header_gf.c` | explizite Count-/Symbol-Metadaten statt reiner Hack-Heuristik |
| Cyan UPR-ZX NatDex | `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/config/gen3_offsets.ini` | vorab generierter `PokemonCount=1283` fuer NatDex-FireRed |

## DPE/CFRU ID-Raeume

### Interne Species-ID

Die interne Species-ID ist die Tabellenidentitaet. Beispiele:

| Symbol | Wert | Bedeutung |
|---|---:|---|
| `SPECIES_XERNEAS` | `0x338` / `824` | erste Species direkt hinter dem aktuellen FVX-Cutoff |
| `SPECIES_SILVALLY` | `0x3DE` / `990` | Gen7-Basisform |
| `SPECIES_HAKAMO_O` | `0x3E8` / `1000` | Diagnoseprobe in `1000..1050` |
| `SPECIES_KOMMO_O` | `0x3E9` / `1001` | Diagnoseprobe in `1000..1050` |
| `SPECIES_SILVALLY_FIGHT` | `0x418` / `1048` | Form-Species mit gleicher Dex-ID wie Silvally |
| `SPECIES_SPRIGATITO` | `0x50E` / `1294` | Gen9-Start |
| `SPECIES_TERAPAGOS` | `0x59C` / `1436` | Gen9-Endbereich |
| `SPECIES_PECHARUNT` | `0x59F` / `1439` | letzte DPE/CFRU-Species |
| `NUM_SPECIES` | `1440` | Slots inklusive `SPECIES_NONE = 0` |

Diese IDs koennen und muessen oberhalb `1023` liegen, weil DPE/CFRU mehr interne Species- und Form-Slots als reine National-Dex-Eintraege haben.

### National Dex ID

DPE `include/pokedex.h` und CFRU `include/constants/pokedex.h` definieren den Anzeige-/Dex-Raum:

| Symbol | Wert |
|---|---:|
| `NATIONAL_DEX_TERAPAGOS` | `1024` |
| `NATIONAL_DEX_PECHARUNT` | `1025` |
| `FINAL_DEX_ENTRY` | `NATIONAL_DEX_PECHARUNT` |
| DPE `NATIONAL_DEX_COUNT` | `FINAL_DEX_ENTRY + 1` |
| CFRU `NATIONAL_DEX_COUNT` | `1025` |

Forms koennen dieselbe National-Dex-ID wie ihre Basisform nutzen. DPE `Species_To_Pokdex_Table.c` mappt z. B. alle Silvally-Type-Forms auf `NATIONAL_DEX_SILVALLY`, alle Terapagos-Forms auf `NATIONAL_DEX_TERAPAGOS` und Xerneas-Natural auf `NATIONAL_DEX_XERNEAS`.

### DPE Species-to-Dex Mapping

`gSpeciesToNationalPokedexNum[NUM_SPECIES - 1]` ist das fuer FVX semantisch passendste Dex-Mapping: Es ist nach interner Species-ID minus eins indiziert und liefert einen National-Dex-Wert.

Beispiele:

```text
[SPECIES_XERNEAS - 1] = NATIONAL_DEX_XERNEAS
[SPECIES_SILVALLY_FIGHT - 1] = NATIONAL_DEX_SILVALLY
[SPECIES_XERNEAS_NATURAL - 1] = NATIONAL_DEX_XERNEAS
[SPECIES_SPRIGATITO - 1] = NATIONAL_DEX_SPRIGATITO
[SPECIES_TERAPAGOS_STELLAR - 1] = NATIONAL_DEX_TERAPAGOS
[SPECIES_PECHARUNT - 1] = NATIONAL_DEX_PECHARUNT
```

Wenn FVX fuer CFRU/DPE eine Dex-ID setzen will, ist diese Tabelle oder ein daraus abgeleitetes Mapping die richtige Quelle, nicht `gPokedexOrder_Regional`.

## Bedeutung von DPE PokedexOrder

DPE `src/Pokedex_Orders.c` definiert mehrere `u16`-Listen:

- `gPokedexOrder_Regional`
- `gPokedexOrder_Alphabetical`
- `gPokedexOrder_Weight`
- `gPokedexOrder_Height`
- `gPokedexOrder_Type`

Diese Listen enthalten Species-IDs. Die DPE-Pokedex-Runtime bestaetigt das:

- Regional-Counts pruefen `SpeciesToNationalPokedexNum(gPokedexOrder_Regional[i])`.
- `SpeciesToRegionalDexNum(species)` sucht die Species direkt in `gPokedexOrder_Regional`.
- `LoadPokedexViews()` setzt `u16 species = dexList[i]` und verwendet `gSpeciesNames[species]`.
- Die National-Dex-Ansicht iteriert dagegen `i < NATIONAL_DEX_COUNT` und ruft `NationalPokedexNumToSpecies(i)`.

Folge: Ein DPE-PokedexOrder-Eintrag `>1023` kann eine voellig valide interne Species-ID sein. `SPECIES_SPRIGATITO = 1294`, `SPECIES_TERAPAGOS = 1436` und `SPECIES_PECHARUNT = 1439` sind im regionalen Dex-Endbereich normale Werte.

## Warum `pdEntry=1808` bei ID 824 auftreten kann

Der Diagnosebefund:

```text
pokedexOrderOffset=0x251FEE
firstPdEntryAbove1023Index=824
firstPdEntryAbove1023Value=1808
countAfterPokedexOrderCheck=823
```

FVX verwendet fuer FireRed 1.0 den Legacy-Offset `PokedexOrder=0x251FEE` aus `gen3_offsets.ini` und liest dort `readWord(pdOffset + (i - 1) * 2)`.

Fuer CFRU/DPE gibt es drei wichtige Schlussfolgerungen:

1. `1808` ist kein sinnvoller National-Dex-Wert fuer Xerneas. Xerneas ist National-Dex `716`.
2. `1808` ist auch kein sinnvoller DPE-Xerneas-Specieswert. `SPECIES_XERNEAS = 824`.
3. Wenn FVX auf `gSpeciesToNationalPokedexNum` zeigen wuerde, muesste ID `824` bei `SPECIES_XERNEAS - 1` den Xerneas-Dexwert liefern, nicht `1808`.

Damit ist `1808` am wahrscheinlichsten kein semantisch gueltiger Dex-ID-Eintrag, sondern ein Beleg dafuer, dass der Vanilla/FVX-Offset im gepatchten CFRU/DPE-ROM nicht mehr als lineares internes-Species-zu-Dex-Mapping nutzbar ist. Es kann anderer Tabelleninhalt, alter Vanilla-/Legacy-Rest, gepatchter Code, sortierte Species-Order oder misaligned gelesene Daten sein. Ohne ROM-Zugriff bleibt die genaue Herkunft offen; fuer die Count-Strategie reicht der Befund: Diese Tabelle darf nicht den Species-Count begrenzen.

## Warum die FVX-Heuristik falsch ist

`basicBPRE10HackSupport()` behandelt `PokedexOrder` als Sanity-Grenze:

```text
if (pdEntry > 1023) iPokemonCount = i - 1
```

Diese Annahme passt fuer konventionelle alte Gen3-Hacks, in denen `PokedexOrder` ein Dex-ID-Mapping im Bereich `0..1023` bleibt. Sie passt nicht fuer CFRU/DPE:

- DPE interne Species-IDs reichen bis `1439`.
- DPE PokedexOrder-Listen speichern Species-IDs, nicht Dex-IDs.
- DPE National Dex reicht selbst bis `1025`, womit `>1023` fuer Pecharunt-nahe Dexwerte nicht mehr pauschal ungueltig ist.
- Der konkrete Offset liefert bei ID `824` einen Wert, der nicht als National-Dex-Mapping belastbar ist.

Als Count-Heuristik schneidet `PokedexOrder` daher gueltige Daten weg, obwohl `PokemonNames` bis `Pecharunt` und BaseStats ueber ID `823` hinaus vorhanden sind.

## Belege fuer valide Gen9-Coverage

### Source-Belege

| Datenbereich | Beleg |
|---|---|
| Species-Grenze | DPE/CFRU `SPECIES_PECHARUNT = 0x59F`, `NUM_SPECIES = SPECIES_PECHARUNT + 1` |
| Dex-Grenze | DPE `NATIONAL_DEX_PECHARUNT = 1025`, `NATIONAL_DEX_COUNT = FINAL_DEX_ENTRY + 1` |
| Species-to-Dex | DPE `gSpeciesToNationalPokedexNum[NUM_SPECIES - 1]` bis Pecharunt |
| Pokedex Runtime | DPE nutzt `SpeciesToNationalPokedexNum()` fuer Species-Order-Listen |
| Learnsets | DPE/CFRU Learnset-Tabellen enthalten Gen7-Gen9 bis Pecharunt |

### Diagnose-Belege

Aus dem vorherigen lokalen Diagnose-Lauf:

- `PokemonNames`: `nameScanStopIndex=1440`, letzter valider Name ID `1439` = `Pecharunt`.
- BaseStats: Proben ueber ID `823` plausibel, z. B. `824 Xerneas`, `1000 Hakamo-o`, `1001 Kommo-o`, `1002 Tapu Koko`, `1019 Marshadow`, `1048/1050 Silvally`.
- FVX-Load bleibt nur wegen Count-Kappung bei `PokemonCount=823`.

## Movesets sind ein separates Thema

Der Diagnose-Lauf zeigte:

```text
movesetsTable=0x25D7B4
jamboMovesetHack=false
firstInvalidMovesetIndex=1439
firstInvalidMovesetRawPointer=0x0
countAfterMovesetCheck=930
```

Damit ist die Moveset-Heuristik ebenfalls nicht Gen9-sicher. Sie ist aber nicht die direkte `823`-Ursache, weil `PokedexOrder` danach noch staerker kappt.

Fuer den naechsten Fix bedeutet das:

- Count-Fix und Moveset-Pointer-Modellierung duerfen nicht vermischt werden.
- Ein Count-Fix kann Gen9-Species sichtbar machen, aber Learnset-Randomization bleibt P1/P1-Learnset-Risiko.
- Die alte `PokemonMovesets`-Pointerquelle muss spaeter gegen aktive DPE/CFRU-Learnset-Symbole oder generierte Offsets geprueft werden.

## CyanSMP64 NatDex Vergleich

CyanSMP64 verfolgt eine robustere NatDex-Strategie:

- FireRed NatDex `tools/inigen/inigen.c` generiert `PokemonCount=%d` direkt aus `NUM_SPECIES - 1`.
- Dieselbe INI-Generierung schreibt Tabellenadressen aus Symbolen wie `gLevelUpLearnsets`, `gEvolutionTable` und Wild-Header.
- `src/rom_header_gf.c` exportiert `pokedexCount = NATIONAL_DEX_COUNT`.
- CyanSMP64 UPR-ZX NatDex `gen3_offsets.ini` enthaelt statisch `PokemonCount=1283`, statt ihn fuer den NatDex-Build aus Vanilla-BPRE-Heuristiken zu raten.
- CyanSMP64 UPR-ZX NatDex hat Gen8/Gen9-Restriction-Bits und Form-/Regional-Form-Kategorien.

Das ist kein direkter Drop-in fuer CFRU/DPE, aber die Architekturentscheidung ist relevant: Fuer einen bekannten NatDex-/Expansion-Build sollte der Randomizer Count und Tabellenquellen aus expliziten Profil-/Symbolmetadaten oder aus robusten Expansion-Tabellen beziehen, nicht aus Vanilla-PokedexOrder-Sanity.

## FVX-Modell fuer CFRU/DPE

FVX sollte fuer erweiterte CFRU/DPE-BPRE-Hacks vier Werte strikt trennen:

| FVX-Konzept | Bedeutung | Empfohlene Quelle |
|---|---|---|
| `PokemonCount` | hoechste interne Species-ID, die FVX als ROM-Species laedt | DPE/CFRU-Profil oder Names + BaseStats-Sanity; fuer den Teststand Ziel `1439` |
| `PokedexCount` | hoechste Dex-/Anzeige-ID | DPE/CFRU `NATIONAL_DEX_COUNT`/`FINAL_DEX_ENTRY`, nicht `max(PokedexOrder legacy)` |
| SpeciesSet identity max | eindeutige Randomizer-Species-Identitaet | interne Species-ID |
| Dex display number / `Species.number` | National-Dex-/Anzeige-ID und Legacy-Dex-Mapping | `gSpeciesToNationalPokedexNum` oder aequivalentes Mapping |

Wichtig: `Species.number` sollte nicht einfach auf interne Species-ID umgestellt werden, solange zahlreiche Gen3-Schreibpfade noch `pokedexToInternal[species.getNumber()]` nutzen. Die sichere Richtung bleibt:

- interne ID fuer Identitaet und Schreiben in CFRU/DPE-Pfade,
- Dex-ID fuer Anzeige und Legacy-Kompatibilitaet,
- explizite Hilfsmethode fuer interne ID statt indirekter `pokedexToInternal`-Rueckrechnung.

## Sichere Fix-Strategie

Empfohlene Strategie fuer den naechsten Fix:

1. Nur fuer konservativ erkannte CFRU/DPE-BPRE-Hacks die `PokedexOrder`-Count-Kappung deaktivieren oder ersetzen.
2. `PokemonCount` primaer aus einer DPE/CFRU-spezifischen Quelle bestimmen:
   - kurzfristig: `PokemonNames`-Scan bis Pecharunt, begrenzt und validiert durch BaseStats-Sanity;
   - mittelfristig: explizites CFRU/DPE-Profil mit `PokemonCount=1439` bzw. aus generierten Symbol-/Offsetdaten;
   - langfristig: Symbol-/Profilquelle analog CyanSMP64 inigen, z. B. `gNumSpecies`/`NUM_SPECIES - 1`.
3. `PokedexOrder` nicht mehr als Count-Grenze verwenden, solange der Offset nicht als internes-Species-zu-National-Dex-Mapping verifiziert ist.
4. Dex-ID fuer `Species.number` aus `gSpeciesToNationalPokedexNum` oder einer neuen CFRU/DPE-Mappingquelle laden. Falls diese Quelle im Fix noch nicht sicher erreichbar ist, Forms und Species mit unklarer Dex-ID explizit als Mapping-Risiko dokumentieren und keine P1-Schreibpfade freigeben.
5. `pokedexToInternal` fuer kollidierende Form-Dex-IDs bewusst als "erste Species fuer Dex-ID" behandeln; interne Schreibpfade muessen fuer CFRU/DPE weiter ueber interne SpeciesSet-Identitaet laufen.
6. Moveset-Pointer-Kappung fuer CFRU/DPE getrennt behandeln: entweder nicht als Count-Sanity nutzen oder nur warnen, bis aktive Learnset-Tabelle sicher modelliert ist.

### Regression-Checks

Minimal noetige Checks fuer einen spaeteren Fix:

- Vanilla FireRed 1.0 bleibt bei `PokemonCount=411` und unveraendertem `PokedexOrder`-Load.
- Nicht-CFRU/DPE Gen3-Hacks behalten die bisherige Heuristik.
- CFRU/DPE-Teststand laedt `PokemonCount=1439`, letzter Name `Pecharunt`.
- `speciesList` enthaelt Gen7/Gen8/Gen9 und keine `<unknown>`-Species fuer valide Namen.
- `Species.number` fuer Basis-Gen9-Species entspricht National-Dex-ID, z. B. Sprigatito `906`, Terapagos `1024`, Pecharunt `1025`.
- Form-Beispiele teilen erwartete Dex-ID, z. B. Silvally-Forms und Terapagos-Forms.
- Wild-Standardtabellen bleiben schreibbar ueber interne Species-ID.
- Learnset-Randomization bleibt disabled/unsupported oder separat diagnostiziert, bis `PokemonMovesets` geklaert ist.

## Entscheidungsmatrix

| Option | Beschreibung | Sicherheit | Aufwand | Risiko fuer Vanilla | Risiko fuer P1-Features | Bewertung |
|---|---|---|---|---|---|---|
| A | `PokedexOrder`-Sanity nur fuer CFRU/DPE deaktivieren | mittel | niedrig | niedrig, wenn Erkennung konservativ ist | hoch, weil Dex-ID-Mapping weiter unklar bleibt | guter kurzfristiger Diagnose-/Unlock-Schritt, aber kein vollstaendiges Modell |
| B | Count aus `PokemonNames` + BaseStats-Sanity ableiten | mittel-hoch | mittel | niedrig, wenn nur CFRU/DPE | mittel, weil Movesets/Dex-Mapping getrennt offen bleiben | beste kurzfristige Count-Quelle ohne neue Symbolinfrastruktur |
| C | Count aus `NUM_SPECIES`/Source-Konstanten/Offsets ableiten | hoch, wenn Offset/Symbol zum ROM passt | mittel-hoch | niedrig | mittel | sauber, aber braucht belastbare generierte Profil-/Offsetquelle fuer den konkreten Build |
| D | eigenes CFRU/DPE-Profil mit explizitem SpeciesCount und Mappingquellen | hoch | hoch | sehr niedrig | niedrig-mittel | beste langfristige Strategie; erlaubt klare Trennung von Count, Dex-ID, Forms und P1-Pfaden |

Empfehlung: Fuer den naechsten kleinen Fix B plus A kombinieren, aber als CFRU/DPE-spezifische Sonderbehandlung kapseln: `PokedexOrder` darf nicht kappen; Count kommt aus Names + BaseStats-Sanity mit erwarteter Obergrenze `1439`. Parallel sollte D vorbereitet werden, damit spaeter `gSpeciesToNationalPokedexNum`, `gNumSpecies` und aktive Learnset-/Evolutionstabellen aus einem Profil oder generierten Symbolen kommen.

## Risiken

- Ohne ROM-Zugriff bleibt die genaue Herkunft von `pdEntry=1808` offen.
- Names + BaseStats-Sanity beweist Species-Existenz, aber nicht die Korrektheit aller P1-Tabellen.
- Forms teilen Dex-IDs; `pokedexToInternal` bleibt als eindeutige Rueckabbildung ungeeignet.
- `PokemonMovesets` ist bereits als separater Cutoff-Faktor sichtbar und darf nicht durch einen Count-Fix verdeckt werden.
- Ein breiter Fix in `basicBPRE10HackSupport()` kann alte Gen3-Hacks gefaehrden, wenn er nicht strikt auf CFRU/DPE-BPRE-Hacks begrenzt wird.

## Naechster minimaler Schritt

Einen separaten UPR-FVX-Fixbranch vorbereiten, der ausschliesslich fuer konservativ erkannte CFRU/DPE-BPRE-Hacks die `PokedexOrder`-Count-Kappung ersetzt und `PokemonCount` aus `PokemonNames` plus BaseStats-Sanity ableitet. Kein Static/Gift-Fix, kein Learnset-Fix und keine generelle Gen3-Heuristik-Aenderung in demselben Branch.
