# UPR-FVX CFRU/DPE P1 Starter Write Diagnostics

Datum: 2026-05-12

## Ziel

Starters-only Diagnose nach abgeschlossenem P0. Geprueft wurde, ob UPR-FVX bei einem erweiterten CFRU/DPE-BPRE-Teststand Gen4+-Species als Starter auswaehlen, schreiben und nach Reload sichtbar erhalten kann.

Keine Codeaenderungen, keine funktionalen Fixes.

## Stand

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-starter-write-diagnostics`
- UPR-FVX-Branch: `compat/firered-gen9-cfru-dpe`
- UPR-FVX-Commit: `843b75a8f1016fa41a1879408fbeca45de7e030a`
- PR-Stand: P0-Fixkette PR #3/#4/#5 ist im Branch enthalten.
- Teststand: lokaler CFRU/DPE-BPRE-Smoke-Teststand unter `05_builds/`, ohne private absolute Pfade dokumentiert.

## Build

UPR-FVX wurde lokal neu gebaut:

```sh
cd 02_external/upr-fvx
./gradlew clean :random:jar
```

Ergebnis: erfolgreich.

## Settings

Starters-only Randomizer-Lauf:

- Starter Pokemon: `COMPLETELY_RANDOM`
- Wild Pokemon: aus
- Trainer Pokemon: aus
- Evolutions: aus
- Movesets/Learnsets: aus
- TM/Tutor/Ability-Pfade: aus
- `limitPokemon=false`
- keine Gen1-3-Einschraenkung

Verwendeter Settings-String:

```text
422AAgEAQIBAAQABwAEAAHkAwARAAEUAAAUAEAEAAEA/////wAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjC05xvZ48M4ig==
```

Relevanter CLI-Befehl ohne private absolute Pfade:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-p1-starter-write-diagnostics-seed274269061345323.gba \
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

Read-only Pool-Gegenpruefung mit `RestrictedSpeciesService.setRestrictions(null)`:

```text
all=798
gen4plus=381
```

Damit ist der P0-Pool fuer Starters grundsaetzlich gross genug und enthaelt Gen4+-Species.

## Starter-Log und Reload-Befund

Fuer Seed `274269061345323` ergibt der Starters-only Pick aus dem unrestricted Starter-Pool:

| Slot | Erwartete Auswahl vor Write | Generation | Species.number | SpeciesSet identity |
|---|---:|---:|---:|---:|
| 1 | Butterfree | 1 | 12 | 12 |
| 2 | Pawniard | 5 | 96 | 677 |
| 3 | Scraggy | 5 | 385 | 612 |

Der Randomizer-Log nach `setStarters()` meldet dagegen:

```text
Mode: Random (completely)
Set starter 1 to Butterfree
Set starter 2 to Drowzee
Set starter 3 to Jirachi
```

Reload der erzeugten ROM ueber UPR-FVX bestaetigt denselben geschriebenen Zustand:

| Slot | Reload-Starter | Generation | Species.number | SpeciesSet identity |
|---|---:|---:|---:|---:|
| 1 | Butterfree | 1 | 12 | 12 |
| 2 | Drowzee | 1 | 96 | 96 |
| 3 | Jirachi | 3 | 385 | 409 |

Zusatzprobe ueber mehrere Seeds zeigte dasselbe Muster: sichtbare Starter bleiben Gen1-3, obwohl der unrestricted Starter-Pool Gen4+ enthaelt. Bei einzelnen Seeds entstanden sogar Dubletten im Log, was zu einem Dex-/Internal-ID-Mapping-Symptom passt.

## Ingame-Befund

Nicht ausgefuehrt. Es lag keine separate Freigabe fuer einen BizHawk-/Ingame-Smoke in diesem Block vor.

## Technische Interpretation

UPR-FVX kann nach P0 Gen4+-Species im Starter-Pool erreichen. Der Fehler liegt nicht in `Settings.tweakForRom()`, `GenRestrictions` oder `RestrictedSpeciesService`.

Der kritische Schreibpfad ist weiterhin `Gen3RomHandler.writeStarterBytes()`:

```java
int starter0 = pokedexToInternal[starters.get(0).getNumber()];
int starter1 = pokedexToInternal[starters.get(1).getNumber()];
int starter2 = pokedexToInternal[starters.get(2).getNumber()];
```

Bei erweiterten CFRU/DPE-BPRE-Hacks ist `Species.number` die Dex-/Pokedex-nahe Nummer und nicht die stabile interne Species-Identitaet. Dadurch werden Gen4+-Starter nach dem Write ueber `pokedexToInternal[Species.number]` auf alte interne Gen1-3-Species abgebildet.

Beispiel:

- Pawniard: `generation=5`, `Species.number=96`, `identity=677`
- geschrieben/gelesen: Drowzee, weil interne Species-ID `96` Drowzee ist

## Bewertung

Ein Starter-Write-Fix ist noetig, wenn Gen4+-Starter fuer CFRU/DPE-BPRE-Hacks supportet werden sollen.

Der naechste Fix sollte klein bleiben:

- nur `Gen3RomHandler.writeStarterBytes()` fuer erweiterte CFRU/DPE-BPRE-Hacks anpassen
- Vanilla-Gen3-ROMs unveraendert lassen
- analog zum Wild-Write-Fix die interne SpeciesSet-Identitaet verwenden
- keine Static-, Trainer-, Evolution-, Learnset-, TM-, Tutor-, Ability- oder Day/Night-Wild-Pfade vermischen

## Risiken

- Starter-Text wird aktuell aus der vor dem Write gewaehlen Species-Liste erzeugt; dadurch koennen Text und tatsaechlich geschriebene Ball-Species bei Gen4+ auseinanderlaufen.
- Ingame wurde in diesem Block nicht geprueft.
- Static/Gift- und Trainer-Pfade koennen dasselbe `pokedexToInternal[Species.number]`-Problem haben und brauchen separate Diagnose/Fixes.
- Lokale ROM- und Build-Artefakte liegen weiterhin nur unter ignored `05_builds/` beziehungsweise Gradle-Buildpfaden und wurden nicht committed.

## Naechster minimaler Schritt

UPR-FVX-Fixbranch fuer Starters-only:

```text
compat/upr-fvx-cfru-dpe-starter-internal-species-write
```

Ziel: `Gen3RomHandler.writeStarterBytes()` fuer erweiterte CFRU/DPE-BPRE-Hacks auf interne Species-Identitaet umstellen und danach denselben Starters-only Seed erneut diagnostizieren.
