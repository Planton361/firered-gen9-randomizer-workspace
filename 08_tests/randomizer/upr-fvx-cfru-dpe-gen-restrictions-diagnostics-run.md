# UPR-FVX CFRU/DPE Gen Restrictions Diagnostics Run

## Datum

2026-05-11

## Ziel

Pruefen, ob der P0-Fix fuer erweiterte CFRU/DPE-BPRE-Hacks die blinde Gen1-3-Kappung aus `Settings.tweakForRom()` und dem finalen `RestrictedSpeciesService`-Pool entfernt, ohne Wild-Tabellenlogik, Nullslots oder andere Randomizer-Systeme zu veraendern.

## UPR-FVX-Stand

- Fork: `Planton361/universal-pokemon-randomizer-fvx`
- Branch: `compat/upr-fvx-cfru-dpe-gen-restrictions`
- Basis: `compat/firered-gen9-cfru-dpe`
- Commit: `61a15e521811c5181025e216b3acc27340a495de`
- Commit-Titel: `compat: allow CFRU DPE extended generation restrictions`
- PR: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/4`

## Codepfade

Geaendert im UPR-FVX-Fork:

- `random/src/main/java/com/uprfvx/random/Settings.java`
- `random/src/main/java/com/uprfvx/random/GameRandomizer.java`
- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

Scope:

- Erweiterte CFRU/DPE-aehnliche BPRE-Hacks werden nicht mehr blind durch `Settings.tweakForRom()` auf `generationOfPokemon() == 3` begrenzt.
- `GameRandomizer.setupSpeciesRestrictions()` setzt bei `limitPokemon=false` den unrestricted Pool via `setRestrictions(null)`.
- Vanilla-Gen3-ROMs bleiben praktisch unveraendert, weil ihr RomHandler-Pool selbst nur die geladenen Gen1-3-Species enthaelt.

Nicht geaendert:

- keine Wild-Encounter-Tabellenlogik
- keine Day/Night-CFRU-Wildtable-Unterstuetzung
- keine Nullslot-`<unknown>`-Logik
- keine SpeciesSet-Identity-Aenderung
- keine Trainer-/Starter-/Evolution-/Learnset-/TM-/Tutor-Fixes

## Lokaler Teststand

- Verwendet wurde derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand wie im vorherigen Gen4+-Wild-Pool-Diagnoselauf.
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

- `./gradlew test`: Prozess beendete mit Exitcode `0`, meldete aber bestehende Testfehler in `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` und `Gen1CmpTest.dummyTest()`.
- `./gradlew clean :random:jar`: `BUILD SUCCESSFUL`.

## Settings und Startbefehl

Verwendeter CLI-Lauf, relativ zum Workspace:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-gen-restrictions-diagnostics.gba \
  -S "422AAgEAQQBAAQABwAEAAHkCAARAQEUAAAUAEAEAAEA/wAAAAAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjD84HA048M4ig==" \
  -z 274269061345319 \
  -l
```

Der Randomizer schreibt die Settings canonical als:

```text
422AAgEAQQBAAQABwAEAAHkCAARAAEUAAAUAEAEAAEA/////wAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjC/hq0048M4ig==
```

Dekodierte relevante Settings nach ROM-Tweak:

- Wild Pokemon Randomization: aktiv
- Wild mode: `GAME`
- `limitPokemon=false`
- `currentRestrictions=null`
- GenRestrictions im Settings-String: Gen1-7 erlaubt
- keine Wild-Type-, Similar-Strength- oder Evolution-Stage-Einschraenkung
- Time-based Encounters: aus

## Lokale Artefakte

Nicht committed:

- Console/stderr: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-gen-restrictions-diagnostics-console.log`
- Randomizer-Log: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-gen-restrictions-diagnostics.gba.log`
- Output-ROM: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-gen-restrictions-diagnostics.gba`

Hashes:

```text
9deaf9277d37506101a9ec55b2bba74ebcd322af36227fc088575b557630c200  upr-fvx-cfru-dpe-gen-restrictions-diagnostics.gba
533f3408eede8e2be94dc354e3bf0e2aa870e5279371a6fe0bc65dd181afdd48  upr-fvx-cfru-dpe-gen-restrictions-diagnostics.gba.log
70ca71e03c2ad8af81e0e87409b5549d11ac95efc821a6efb48d21b3130d1315  upr-fvx-cfru-dpe-gen-restrictions-diagnostics-console.log
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

Beispiel-Species ueber 386:

| Internal ID | Interne Identitaet | Dex-/Species-Nummer | Name | Generation |
|---:|---:|---:|---|---:|
| 798 | 798 | 387 | Skrelp | 6 |
| 799 | 799 | 388 | Dragalge | 6 |
| 800 | 800 | 389 | Clauncher | 6 |
| 801 | 801 | 390 | Clawitzer | 6 |
| 802 | 802 | 391 | Helioptile | 6 |
| 803 | 803 | 392 | Heliolisk | 6 |
| 804 | 804 | 393 | Tyrunt | 6 |
| 805 | 805 | 394 | Tyrantrum | 6 |
| 806 | 806 | 395 | Amaura | 6 |
| 807 | 807 | 396 | Aurorus | 6 |
| 808 | 808 | 397 | Sylveon | 6 |
| 809 | 809 | 398 | Hawlucha | 6 |

## RestrictedSpeciesService-Pool

Ein temporaerer lokaler Inspector gegen die gebaute JAR wurde nur fuer die Diagnose genutzt und nicht committed. Er lud denselben Teststand, dekodierte die Settings, fuehrte `settings.tweakForRom(rh)` aus und setzte danach dieselben Restrictions wie `GameRandomizer.setupSpeciesRestrictions()`.

Ergebnis:

```text
limitPokemon=false
currentRestrictions=null
speciesList: size=798 maxNumber=411 maxIdentity=823 gens={1=152, 2=104, 3=161, 4=139, 5=178, 6=64} gen4plus=381
all: size=798 maxNumber=411 maxIdentity=823 gens={1=152, 2=104, 3=161, 4=139, 5=178, 6=64} gen4plus=381
nonLeg: size=756 maxNumber=411 maxIdentity=823 gens={1=147, 2=98, 3=151, 4=134, 5=168, 6=58} gen4plus=360
```

Beispiel aus dem finalen unrestricted Pool:

```text
Turtwig#280/id440 g4
Grotle#281/id441 g4
Torterra#282/id442 g4
Chimchar#283/id443 g4
Monferno#284/id444 g4
Infernape#285/id445 g4
Piplup#286/id446 g4
Prinplup#287/id447 g4
Empoleon#288/id448 g4
```

Interpretation: Der P0-Fix entfernt die Gen1-3-Kappung im finalen `RestrictedSpeciesService`-Pool.

## Wild-Log-Auswertung

Ausgewertet wurden die sichtbaren Namen im Randomizer-Wild-Pokemon-Log.

| Generation | Wild-Slots |
|---|---:|
| Gen1 | 841 |
| Gen2 | 527 |
| Gen3 | 791 |
| Gen4 | 0 |
| Gen5 | 0 |
| Gen6 | 0 |
| Gen7+ | 0 |
| `<unknown>` | 17 |

Weitere Werte:

- Gesamt ausgewertete Wild-Slots: `2176`
- Eindeutige sichtbare Species-Namen: `105`
- Sichtbare Gen4+-Species im Wild-Log: keine
- Repraesentative Gen4+/Gen6-Namen wie `Turtwig`, `Chimchar`, `Piplup`, `Skrelp`, `Dragalge`, `Sylveon` und `Hawlucha` tauchen nicht sichtbar im Wild-Log auf.
- `<unknown>`-stderr-Rohwerte: weiterhin ausschliesslich `rawInternalSpeciesId=0`.

## `<unknown>`-Befund

Die eindeutigen `<unknown>`-Eintraege bleiben unveraendert und betreffen nur Nullslots:

| Area | Encounter-Type | Slots | Datenoffsets | rawInternalSpeciesId |
|---|---|---|---|---:|
| VIRIDIAN FOREST Grass/Cave | WALKING | 7, 8, 10 | `0x3C7528` | 0 |
| POKéMON TOWER Grass/Cave | WALKING | 6, 7, 9 | `0x3C7DF4`, `0x3C7E2C`, `0x3C7E64`, `0x3C7E9C`, `0x3C7ED4` | 0 |
| PATTERN BUSH Grass/Cave | WALKING | 1 | `0x3C8450` | 0 |
| SEVAULT CANYON Grass/Cave | WALKING | 2 | `0x3C8DC0` | 0 |
| ROUTE 24 Grass/Cave | WALKING | 8 | `0x3C96C0` | 0 |
| ROUTE 25 Grass/Cave | WALKING | 8 | `0x3C9744` | 0 |

## Diagnose vorher/nachher

| Wert | Vor P0-Fix | Nach P0-Fix |
|---|---:|---:|
| `PokemonCount` | 823 | 823 |
| `pokedexCount` | 386 | 386 |
| `speciesList.size` | 799 | 799 |
| `maxSpeciesIdentityNumber` | 823 | 823 |
| RomHandler-Gen4+-Species | vorhanden | vorhanden |
| RestrictedSpeciesService-Gen4+-Species bei `limitPokemon=false` | durch Gen3-Restrictions entfernt | vorhanden (`gen4plus=381`) |
| sichtbare Gen4+-Wild-Log-Slots | 0 | 0 |
| `<unknown>` | `rawInternalSpeciesId=0` | `rawInternalSpeciesId=0` |

## Technische Interpretation

Der P0-Fix erreicht den vorgesehenen Settings-/Restrictions-Teil:

- `Settings.tweakForRom()` kappt erweiterte CFRU/DPE-BPRE-Hacks nicht mehr blind auf Gen3.
- `GameRandomizer.setupSpeciesRestrictions()` setzt bei `limitPokemon=false` den unrestricted Pool.
- Der finale Pool im `RestrictedSpeciesService` enthaelt Gen4+-Species.

Der sichtbare Wild-Log bleibt trotzdem Gen1-3. Weil der unrestricted Pool nachweislich Gen4+ enthaelt, ist der verbleibende Befund kein GenRestrictions-Problem mehr. Der wahrscheinlichste naechste Engpass liegt im Gen3-Wild-Write-/Reload-Pfad: Gen3-Schreibpfade nutzen weiterhin `pokedexToInternal[enc.getSpecies().getNumber()]`. Bei CFRU/DPE ist `Species.number` nicht die stabile interne Species-Identitaet. Dadurch koennen Gen4+-Auswahlen beim Schreiben oder anschliessenden Loggen wieder auf Gen1-3/Dex-Nummer-Mapping kollabieren.

Das ist ein Folgeproblem und wurde in diesem Branch nicht gefixt.

## Entscheidung

- UPR-FVX PR #4 ist als P0-GenRestrictions-Fix sinnvoll.
- PR #4 allein beweist, dass Gen4+ im finalen Allowed-Pool ankommt.
- Sichtbare Gen4+-Wild-Encounters erfordern einen weiteren, klar getrennten Fix fuer Gen3/CFRU-DPE-interne Species-ID-Schreibpfade.

## Risiken

- `./gradlew test` meldet bestehende Testfehler trotz Exitcode `0`; diese muessen separat bewertet werden.
- Der lokale Teststand reicht nur bis `PokemonCount=823`; Gen7-Gen9 sind damit in diesem Build nicht repraesentiert.
- Sichtbare Wild-Ausgabe bleibt ohne naechsten Write-Path-Fix Gen1-3.
- `<unknown>`-Nullslots bleiben P3 und sind bewusst unveraendert.

## Naechster minimaler Schritt

Neuer UPR-FVX-Fixbranch fuer Gen3/CFRU-DPE-Wild-Write-Mapping:

```text
compat/upr-fvx-cfru-dpe-wild-internal-species-write
```

Ziel: Nur pruefen und korrigieren, dass Wild-Encounter-Schreibpfade fuer erweiterte BPRE-Hacks die interne Species-Identitaet statt `pokedexToInternal[Species.number]` verwenden. Keine Day/Night-Wildtables, keine Nullslot-Fixes und keine Trainer-/Starter-/Evolution-/Learnset-Erweiterungen in diesem Branch.
