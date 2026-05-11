# UPR-FVX CFRU/DPE Starter Internal Species Write Diagnostics

Datum: 2026-05-12

## Ziel

Diagnose des minimalen Starter-Write-Fixes fuer erweiterte CFRU/DPE-BPRE-Hacks. Geprueft wurde, ob `Gen3RomHandler.writeStarterBytes()` Gen4+-Starter nach Write und Reload als interne SpeciesSet-Identitaet erhaelt.

Keine Wild-, Static-, Trainer-, Evolution-, Learnset-, TM-/Tutor-, Ability- oder Day/Night-Wild-Fixes wurden umgesetzt.

## UPR-FVX-Stand

- Fork: `Planton361/universal-pokemon-randomizer-fvx`
- Basisbranch: `compat/firered-gen9-cfru-dpe`
- Arbeitsbranch: `compat/upr-fvx-cfru-dpe-starter-internal-species-write`
- Commit: `39c57880`
- Commit-Titel: `compat: write CFRU DPE starters by internal identity`
- PR: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/6`

Basis enthielt die P0-Fixkette bis UPR-FVX Merge-Commit `843b75a8`.

## Codepfad-Befund

Read-only vor dem Patch belegt:

- `Gen3RomHandler.getStarters()` liest Starter-Werte aus dem ROM als interne Species-IDs und loest sie mit `pokesInternal[readWord(...)]` auf.
- `Gen3RomHandler.setStarters()` ruft `writeStarterBytes(starters)` und danach `writeStarterText(starters)` auf.
- `writeStarterBytes()` schrieb vorher alle drei Starter ueber `pokedexToInternal[starters.get(i).getNumber()]`.
- Bei erweiterten CFRU/DPE-BPRE-Hacks ist `Species.number` Dex-/Pokedex-nahe Nummer, nicht die interne DPE-Species-Identitaet.

Implementiert:

- Nur `Gen3RomHandler.writeStarterBytes()` nutzt jetzt eine kleine Hilfsmethode.
- Fuer `usesInternalSpeciesIdentityForExtendedBpreHack()` schreibt sie `species.getSpeciesSetIdentityNumber()`.
- Fuer Vanilla und normale Gen3-Hacks bleibt der alte `pokedexToInternal[species.getNumber()]`-Pfad erhalten.

Nicht geaendert:

- Starter-Auswahl-Pool
- Settings / `GenRestrictions`
- Logger
- Wild, Static, Trainer, Evolution, Learnset, TM/Tutor, Ability
- Day/Night-Wildtabellen
- SpeciesSet-Identity-Modell

## Build und Checks

UPR-FVX:

```sh
cd 02_external/upr-fvx
git status --short
git diff --stat
git diff --check
./gradlew test
./gradlew clean :random:jar
```

Ergebnis:

- `git diff --check`: sauber.
- `./gradlew test`: `BUILD SUCCESSFUL`, meldet aber weiterhin die bekannten Testfehler:
  - `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()`
  - `Gen1CmpTest.dummyTest()`
- `./gradlew clean :random:jar`: `BUILD SUCCESSFUL`.

## Lokaler Teststand

- Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Teststand wie in `upr-fvx-cfru-dpe-p1-starter-write-diagnostics.md`.
- Input-ROM, Output-ROM und Randomizer-Log blieben lokal/ignored unter `05_builds/`.
- Keine ROMs, Builds, Randomizer-JARs, Saves oder Emulator States wurden committed.
- Keine privaten absoluten Pfade werden dokumentiert.

## Settings und Startbefehl

Settings-Intent:

- Starter Pokemon: `COMPLETELY_RANDOM`
- Wild Pokemon: aus
- Trainer Pokemon: aus
- Evolutions: aus
- Movesets/Learnsets: aus
- TM/Tutor/Ability-Pfade: aus
- `limitPokemon=false`
- keine Gen1-3-Einschraenkung

Settings-String:

```text
422AAgEAQIBAAQABwAEAAHkAwARAAEUAAAUAEAEAAEA/////wAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjC05xvZ48M4ig==
```

CLI-Befehl ohne private absolute Pfade:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-starter-internal-species-write-diagnostics-seed274269061345323.gba \
  -S "422AAgEAQIBAAQABwAEAAHkAwARAAEUAAAUAEAEAAEA/////wAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjC05xvZ48M4ig==" \
  -z 274269061345323 \
  -l
```

## Species-/Pool-Diagnose

Konsolendiagnose beim Laden:

```text
ROM code=BPRE version=0 isRomHack=true
PokemonCount=823 pokedexCount=386 speciesList.size=799 maxInternalSpeciesId=823 maxSpeciesNumber=411 maxSpeciesIdentityNumber=823
generationCounts={1=177, 2=104, 3=161, 4=139, 5=178, 6=64}
```

Der vorherige Starters-only Diagnoseblock hatte bereits den unrestricted Starter-Pool belegt:

```text
all=798
gen4plus=381
```

## Starter-Diagnose vorher/nachher

Seed: `274269061345323`

| Slot | Erwartete Auswahl vor Write | Vor Fix nach Write/Reload | Nach Fix Log | Nach Fix Reload |
|---|---|---|---|---|
| 1 | Butterfree Gen1, identity 12 | Butterfree Gen1, identity 12 | Butterfree | Butterfree Gen1, identity 12 |
| 2 | Pawniard Gen5, identity 677 | Drowzee Gen1, identity 96 | Pawniard | Pawniard Gen5, identity 677 |
| 3 | Scraggy Gen5, identity 612 | Jirachi Gen3, identity 409 | Scraggy | Scraggy Gen5, identity 612 |

Randomizer-Log nach dem Fix:

```text
Mode: Random (completely)
Set starter 1 to Butterfree
Set starter 2 to Pawniard
Set starter 3 to Scraggy
```

Reload der erzeugten ROM ueber UPR-FVX nach dem Fix:

```text
1: Butterfree gen=1 number=12 identity=12
2: Pawniard gen=5 number=96 identity=677
3: Scraggy gen=5 number=385 identity=612
```

## Technische Entscheidung

Fuer erweiterte CFRU/DPE-aehnliche BPRE-Hacks ist die interne SpeciesSet-Identitaet die richtige Schreibidentitaet fuer Starter-Species. Der Patch verwendet die bereits vorhandene `speciesSetIdentityNumber` und den bestehenden Guard `usesInternalSpeciesIdentityForExtendedBpreHack()`.

Der alte Dex-/Pokedex-Schreibpfad bleibt fuer Vanilla und normale Gen3-Hacks erhalten. Dadurch bleibt der Fix eng auf den bereits diagnostizierten CFRU/DPE-Fall begrenzt.

## Bewertung

Der Starter-Write-Fix ist fuer den diagnostizierten Seed erfolgreich:

- Pawniard und Scraggy werden als Gen5-Starter geschrieben.
- Reload erhaelt die internen Identitaeten `677` und `612`.
- Der vorherige Rueckfall auf Drowzee und Jirachi ist nicht mehr sichtbar.

## Risiken

- Der Fix betrifft nur Starter-Bytes. Static/Gift- und Trainer-Species-Schreibpfade nutzen weiterhin teils `pokedexToInternal[Species.number]` beziehungsweise gleichwertige Dex-ID-Mappings und brauchen separate Arbeit.
- Ingame/BizHawk wurde in diesem Block nicht geprueft.
- Der lokale Teststand meldet `PokemonCount=823`; Gen7-Gen9 sind in diesem Lauf nicht repraesentiert.
- Die temporaeren CFRU/DPE-Diagnoseausgaben sind weiterhin im UPR-FVX-Zielbranch vorhanden und sollten spaeter entfernt oder hinter Debug-Logging gelegt werden.

## Naechster minimaler Schritt

UPR-FVX PR #6 reviewen und mergen, wenn keine Regressionen sichtbar sind.

Danach ein separater P1-Diagnoseblock fuer Static/Gift-Species:

```text
analysis/upr-fvx-cfru-dpe-p1-static-gift-write-diagnostics
```

Keine Trainer-, Evolution-, Learnset-, TM-/Tutor-, Ability-, Day/Night-Wild- oder Nullslot-Fixes in diesem Folgeblock.
