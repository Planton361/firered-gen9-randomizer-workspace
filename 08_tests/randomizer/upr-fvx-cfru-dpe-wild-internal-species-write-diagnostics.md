# UPR-FVX CFRU/DPE Wild Internal Species Write Diagnostics

## Datum

2026-05-11

## Ziel

Pruefen, ob der Gen3-Wild-Encounter-Schreibpfad fuer erweiterte CFRU/DPE-BPRE-Hacks randomisierte Wild-Species mit interner Species-Identitaet schreibt, statt ueber `pokedexToInternal[Species.number]` auf `0` oder Gen1-3 zurueckzufallen.

## UPR-FVX-Stand

- Fork: `Planton361/universal-pokemon-randomizer-fvx`
- Branch: `compat/upr-fvx-cfru-dpe-wild-internal-species-write`
- Basis: `compat/firered-gen9-cfru-dpe`
- Basis enthielt UPR-FVX PR #4 als Merge-Commit `03b42a1216f5a087d42a3e94a7e81a15db2e977b`.
- Commit: `5f68ec0fc8e1592079486f6d22cf5a122eb08d01`
- Commit-Titel: `compat: write CFRU DPE wild species by internal identity`
- PR: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/5`

## Codepfad-Befund

Read-only belegt:

- `Gen3RomHandler.readEncounterArea()` liest Wild-Rohwerte aus den Vanilla/Fallback-Wildtabellen als interne Species-ID und loest sie mit `pokesInternal[rawSpecies]` auf.
- `Gen3RomHandler.setEncounters()` schreibt Vanilla/Fallback-Wildtabellen ueber `writeEncounterArea()`.
- `writeEncounterArea()` schrieb vor diesem Fix immer `pokedexToInternal[enc.getSpecies().getNumber()]`.
- Bei erweiterten CFRU/DPE-BPRE-Hacks ist `Species.number` Dex-/Pokedex-ID, nicht die stabile interne Species-Identitaet.

Implementiert:

- Nur `Gen3RomHandler.writeEncounterArea()` nutzt eine neue kleine Hilfsmethode.
- Fuer `usesInternalSpeciesIdentityForExtendedBpreHack()` schreibt sie `species.getSpeciesSetIdentityNumber()`.
- Fuer Vanilla und normale Gen3-Hacks bleibt der alte `pokedexToInternal[species.getNumber()]`-Pfad erhalten.

Nicht geaendert:

- keine Settings-/GenRestrictions-Logik
- keine CFRU-Day/Night-Wildtable-Unterstuetzung
- keine Nullslot-Sonderlogik
- keine SpeciesSet-Identity-Aenderung
- keine Trainer-/Starter-/Evolution-/Learnset-/TM-/Tutor-Fixes

## Lokaler Teststand

- Verwendet wurde derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand wie in `upr-fvx-cfru-dpe-gen-restrictions-diagnostics-run.md`.
- Input-ROM, Output-ROM, Konsolenlog und Randomizer-Log blieben lokal/ignored unter `05_builds/`.
- Keine ROMs, Builds, Randomizer-JARs, Saves oder Emulator States wurden committed.
- Keine privaten absoluten Pfade werden dokumentiert.

## Build

```sh
cd 02_external/upr-fvx
./gradlew test
./gradlew clean :random:jar
```

Ergebnis:

- `./gradlew test`: Prozess beendete mit Exitcode `0`, meldete aber weiterhin bestehende Testfehler in `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` und `Gen1CmpTest.dummyTest()`.
- `./gradlew clean :random:jar`: `BUILD SUCCESSFUL`.

## Settings und Startbefehl

Verwendeter CLI-Lauf, relativ zum Workspace:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics.gba \
  -S "422AAgEAQQBAAQABwAEAAHkCAARAQEUAAAUAEAEAAEA/wAAAAAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjD84HA048M4ig==" \
  -z 274269061345319 \
  -l
```

Settings-Intent:

- Wild Pokemon Randomization: aktiv
- Wild mode: `GAME`
- `limitPokemon=false`
- keine Gen1-3-Einschraenkung
- keine Wild-Type-, Similar-Strength- oder Evolution-Stage-Einschraenkung
- Time-based Encounters: aus

## Lokale Artefakte

Nicht committed:

- Console/stderr: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics-console.log`
- Randomizer-Log: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics.gba.log`
- Output-ROM: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics.gba`

Hashes:

```text
f8ed5540cd09b220279f1c677886b9b5b0a1e854651031d2aa7d5188cd6f6028  upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics.gba
6cedfa895e0c7da5dda0c5eb5bb885a4aa27ca3cdd7d64cebe2fced17b6709c5  upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics.gba.log
535e60e9dd7aedf3925e6c43140938d1c5485450c3c33506cc72e2cc17081f13  upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics-console.log
```

## Species-Pool-Diagnose

stderr-Diagnose aus `Gen3RomHandler`:

```text
ROM code=BPRE
version=0
isRomHack=true
PokemonCount=823
pokedexCount=386
speciesList.size=799
maxInternalSpeciesId=823
maxSpeciesNumber=411
maxSpeciesIdentityNumber=823
generationCounts={1=177, 2=104, 3=161, 4=139, 5=178, 6=64}
```

`RestrictedSpeciesService`-Befund aus dem vorherigen PR-#4-Diagnoselauf bleibt Voraussetzung und unveraendert:

```text
limitPokemon=false
currentRestrictions=null
all pool size=798
all pool gen4plus=381
nonLegendary pool size=756
nonLegendary pool gen4plus=360
```

## Wild-Log-Auswertung

Ausgewertet wurden die sichtbaren Namen im Randomizer-Wild-Pokemon-Log.

| Generation | Wild-Slots |
|---|---:|
| Gen1 | 354 |
| Gen2 | 388 |
| Gen3 | 404 |
| Gen4 | 398 |
| Gen5 | 528 |
| Gen6 | 104 |
| Gen7+ | 0 |
| `<unknown>` | 0 |

Weitere Werte:

- Gesamt ausgewertete Wild-Slots: `2176`
- Sichtbare Gen4+-Wild-Slots: `1030`
- Gen4+-Beispiele: `Floatzel`, `Starly`, `Arceus`, `Garchomp`, `Hippowdon`, `Shinx`, `Bonsly`, `Darkrai`, `Burmy`, `Gastrodon`, `Shellos`, `Cherrim`, `Manaphy`, `Cherubi`, `Mime Jr.`, `Glameow`, `Staraptor`, `Rampardos`, `Drapion`.
- Gen5-Beispiele: `Gothorita`, `Purrloin`, `Cryogonal`, `Minccino`, `Keldeo`, `Liepard`, `Crustle`, `Venipede`, `Swanna`, `Sewaddle`, `Munna`, `Sandile`, `Volcarona`, `Simipour`, `Eelektross`, `Conkeldurr`, `Deerling`, `Lampent`, `Larvesta`, `Samurott`, `Roggenrola`.
- Gen6-Beispiele: `Quilladin`, `Bergmite`, `Meowstic`, `Avalugg`, `Braixen`, `Flabébé`, `Vivillon`, `Slurpuff`.

## Area-Sanity

Die Vanilla/Fallback-Wildtabellen wirken weiterhin randomisiert:

- Route 1 Grass/Cave: `Minccino` und `Qwilfish`.
- Route 22 Grass/Cave: `Qwilfish`, `Loudred`, `Unown`.
- Viridian Forest Grass/Cave: `Arceus`, `Garchomp`, `Murkrow`, `Bergmite`, `Ivysaur`.

Der Route-1-Fallback-Teststand bleibt damit fuer die Vanilla/Fallback-Wilddaten sichtbar randomisiert. CFRU-Day/Night-Custom-Wildtabellen wurden nicht geprueft und nicht geaendert.

## `<unknown>` und `rawInternalSpeciesId=0`

Vor diesem Fix blieb der finale Wild-Log trotz Gen4+-Allowed-Pool bei Gen1-3 und enthielt `17` sichtbare `<unknown>`-Slots mit `rawInternalSpeciesId=0`.

Nach diesem Fix:

- Finaler Randomizer-Wild-Log: `<unknown>=0`.
- Console/stderr beim finalen Log-Reload meldet keine `wild encounter resolved to <unknown>`-Eintraege.

Interpretation: Die vorherigen `rawInternalSpeciesId=0`-Eintraege waren in diesem Lauf mindestens teilweise Folge des falschen Wild-Schreibpfads. Gen4+-Auswahlen wurden ueber `pokedexToInternal[Species.number]` als `0` zurueckgeschrieben. Dieser Branch fuehrt keine eigene Nullslot-Sonderlogik ein; er verhindert nur den fehlerhaften `0`-Write fuer erweiterte BPRE-Hack-Species.

## Diagnose vorher/nachher

| Wert | Vor Wild-Write-Fix | Nach Wild-Write-Fix |
|---|---:|---:|
| `PokemonCount` | 823 | 823 |
| `speciesList.size` | 799 | 799 |
| `maxSpeciesIdentityNumber` | 823 | 823 |
| RestrictedSpeciesService Gen4+ bei `limitPokemon=false` | 381 | 381 |
| sichtbare Gen1-Wild-Slots | 841 | 354 |
| sichtbare Gen2-Wild-Slots | 527 | 388 |
| sichtbare Gen3-Wild-Slots | 791 | 404 |
| sichtbare Gen4-Wild-Slots | 0 | 398 |
| sichtbare Gen5-Wild-Slots | 0 | 528 |
| sichtbare Gen6-Wild-Slots | 0 | 104 |
| sichtbare Gen4+-Wild-Slots gesamt | 0 | 1030 |
| `<unknown>` | 17 | 0 |

## Technische Entscheidung

Fuer erweiterte CFRU/DPE-aehnliche BPRE-Hacks ist die interne Species-Identitaet die richtige Schreibidentitaet fuer Vanilla/Fallback-Wild-Encounter-Slots. Der Patch nutzt dafuer die bereits mit PR #3 eingefuehrte `speciesSetIdentityNumber`, ohne `Species.number` umzudeuten.

Der alte Dex-/Pokedex-Schreibpfad bleibt fuer Vanilla und normale Gen3-Hacks erhalten. Dadurch bleibt der Scope eng und die bestehenden Gen3-Annahmen werden nicht global veraendert.

## Risiken

- Der Fix betrifft nur Vanilla/Fallback-Wildtabellen. CFRU-Day/Night-Custom-Wildtabellen bleiben P2.
- Der lokale Teststand erkennt `PokemonCount=823`; Gen7-Gen9 sind in diesem Lauf nicht repraesentiert.
- `./gradlew test` meldet weiterhin bestehende Testfehler trotz Exitcode `0`.
- Trainer-, Starter-, Static-, Evolution-, Learnset-, TM- und Tutor-Schreibpfade nutzen weiterhin teils Dex-basierte Umrechnungen und bleiben Folgearbeit.

## Naechster minimaler Schritt

UPR-FVX PR #5 reviewen und mergen, wenn keine Regressionen sichtbar sind.

Danach ein neuer Diagnoseblock fuer Trainer/Starter/Static-Schreibpfade:

```text
analysis/upr-fvx-cfru-dpe-p1-encounter-systems
```

Ziel: getrennt pruefen, welche weiteren Gen3-Schreibpfade bei erweiterten CFRU/DPE-BPRE-Hacks interne Species-Identitaet statt Dex-/Pokedex-ID brauchen. Keine Day/Night-Wildtable- oder Nullslot-Fixes in diesem Folgeblock.
