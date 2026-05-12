# P1 Evolution Scope and Write Diagnostics

## Datum

2026-05-12

## Branch

Workspace:

```text
compat/upr-fvx-cfru-dpe-evolutions-scope-and-write
```

UPR-FVX:

```text
compat/upr-fvx-cfru-dpe-evolutions-scope-and-write
```

## Ziel

Den P1-Blocker aus `025_p1_evolutions_species_only.md` gezielt beheben und diagnostisch bestaetigen:

- Evolution-Source- und Ziel-Species fuer erweiterte CFRU/DPE-BPRE-Hacks ueber interne `SpeciesSet`-Identitaet lesen und schreiben
- Reload muss dieselben Evolution-Zielspecies wieder als dieselben internen Identitaeten erkennen
- Evolution-Logger darf bei nicht aufloesbaren Item-/Move-/Species-/Location-ExtraInfos nicht crashen
- keine Evolution-Methoden-Featurearbeit und keine Wild-, Starter-, Static/Gift-, Trainer-, Learnset-, TM-/Tutor-, Ability- oder Palette-Fixes in diesem Branch

## Codeaenderung

UPR-FVX-Commit:

```text
18766c4986db091d1e669c71302aa295195b039b
```

Geaenderte UPR-FVX-Dateien:

- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `random/src/main/java/com/uprfvx/random/log/RandomizationLogger.java`

Kurzfassung:

- `loadEvolutions()` und `writeEvolutions()` nutzen im erkannten erweiterten CFRU/DPE-BPRE-Modus interne `SpeciesSet`-Identitaet fuer Evolution-Source-Zeilen und Evolution-Zielspecies.
- Vanilla/normal Gen3 bleibt beim bestehenden `pokedexToInternal[Species.number]`-Pfad.
- `RandomizationLogger.evolutionMethodToString()` prueft Item-, Move-, Species- und Location-ExtraInfos defensiv und faellt bei unbekannten Werten auf numerische Marker wie `unknown item #1732` zurueck.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Route-1-Fallback-Teststand wie in Protokoll 021 bis 025. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/**` und wurden nicht committed.

Seed:

```text
274269061345323
```

Evolution-Species-only Settings-String:

```text
422AAgEAQQBAAQABwAEAAHkAwARAAEUAAAUAEAEAAIA/wAAAAAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjBxDuFr48M4ig==
```

Settings-Intent:

- Evolutions randomisieren: an
- Evolution methods/conditions nicht gezielt erweitert
- Wild: aus
- Starters: aus
- Static/Gift: aus
- Trainer: aus
- Learnsets/Movesets: aus
- TM/HM/Tutor: aus
- Abilities: aus
- Palette-/Sprite-Randomization: aus
- `limitPokemon=false`
- keine Gen1-3-Einschraenkung

## Build und CLI

UPR-FVX:

```text
./gradlew clean :random:jar
BUILD SUCCESSFUL
```

CLI-Ergebnis:

```text
Randomized successfully!
Output-ROM: erzeugt
Log: nicht leer
Log-Groesse: 14344 bytes
```

Der direkte `GameRandomizer.Results`-Diagnoselauf meldet jetzt:

```text
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
directLogBytes=14341
```

## Species-Load

Der Species-Load bleibt auf dem erwarteten Gen9-Coverage-Stand:

```text
PokemonCount=1439
speciesList.size=1415
maxSpeciesIdentityNumber=1439
generationCounts={1=271, 2=118, 3=188, 4=149, 5=191, 6=127, 7=123, 8=127, 9=120}
```

## Evolution-Pool-Auswertung

Der Evolution-Replacement-Pool erreicht Gen1-Gen9:

```text
evolutionPool.size=1414
evolutionPool.generationCounts={1=271, 2=118, 3=188, 4=149, 5=191, 6=127, 7=123, 8=127, 9=120}
evolutionPool.hasGen7=true
evolutionPool.hasGen8=true
evolutionPool.hasGen9=true
```

Vor der Randomization werden durch den internen Source-Index jetzt 218 Evolution-Eintraege ueber 190 Quell-Species gelesen:

```text
before.evolutionSources=190
before.evolutionEntries=218
before.toGenerationCounts={1=79, 2=48, 3=63, 4=26, 8=2}
before.hasToGen7=false
before.hasToGen8=true
before.hasToGen9=false
```

Nach der Randomization werden Gen7/8/9-Ziele gepickt:

```text
after.evolutionSources=190
after.evolutionEntries=218
after.toGenerationCounts={1=44, 2=19, 3=26, 4=26, 5=25, 6=27, 7=22, 8=15, 9=14}
after.pickedGen4plus=129
after.pickedGen7plus=51
after.hasToGen7=true
after.hasToGen8=true
after.hasToGen9=true
```

Beispiele fuer Gen7/8/9-Picks:

```text
Tentacruel -> Silvally
Exeggcute -> Tapu Fini
Rhydon -> Meltan
Goldeen -> Eldegoss
Kabuto -> Lycanroc
Sunflora -> Coalossal
Forretress -> Klawf
Mawile -> Maushold
```

## Evolution-Log-Auswertung

Der CLI-Log enthaelt den Evolution-Abschnitt und wird vollstaendig geschrieben:

```text
Pokemon Evolutions-------------------------------{PKEV}
Pokemon Evolutions: Randomized/Changed
```

Beispiele aus dem Evolution-Log:

```text
Tentacruel|Silvally  |Level-up, lvl. 22+
Exeggcute |Tapu Fini |Level-up, lvl. 16+
Rhydon    |Meltan    |Use Moon Stone (estimated evo lvl. 53)
Goldeen   |Eldegoss  |Use Fire Stone (estimated evo lvl. -1)
Forretress|Klawf     |Use Link Cable (estimated evo lvl. 39)
Mawile    |Maushold  |Level-up, lvl. 42+
```

Logger-Fallbacks:

```text
fallbacks.count=2
fallbacks.list=[
  Trade, holding unknown item #1732
  Use unknown item #1732
]
```

Im Evolution-Log wurde kein `<unknown>` beobachtet. Ein bestehender `Bad Egg`-Quell-Evolutionseintrag bleibt im geladenen Evolution-Kontext sichtbar:

```text
Bad Egg -> Vivillon
```

Dieser Branch filtert keine Evolution-Sonder-Species, weil der Scope nur Species-Write/Reload und defensives Logging umfasst.

## Write/Reload

Der Reload-Vergleich nutzt interne `SpeciesSet`-Identitaet:

```text
reload.evolutionSources=190
reload.evolutionEntries=218
reload.toGenerationCounts={1=44, 2=19, 3=26, 4=26, 5=25, 6=27, 7=22, 8=15, 9=14}
reload.hasToGen7=true
reload.hasToGen8=true
reload.hasToGen9=true
writeReloadCompared=1414
writeReloadMismatches=0
writeReloadFirstMismatch=null
```

Gen8/9-Ziele bleiben nach Reload erhalten.

## Interpretation

Evolution-Species-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand jetzt P1-supported:

- der vollstaendige Gen1-Gen9-Evolution-Pool bleibt erreichbar
- Source-Zeilen und Ziel-Species werden im erweiterten BPRE-Modus ueber interne `SpeciesSet`-Identitaet behandelt
- Save und Log sind erfolgreich
- Output-ROM und nichtleerer Evolution-Log entstehen
- Reload erhaelt Gen7/8/9-Ziele und meldet `writeReloadMismatches=0`

Die Logger-Fallbacks zeigen weiterhin, dass einzelne DPE/CFRU-Evolution-ExtraInfos ausserhalb der Standard-FVX-Itemliste liegen. Das blockiert aber Save/Log nicht mehr und ist kein Evolution-Methoden-Featurefix.

## Risiken

- Es wurde kein BizHawk-Gameplay-Smoke gegen die erzeugte Output-ROM ausgefuehrt.
- `Bad Egg` bleibt als bestehende Evolution-Quell-Species sichtbar; dieser Branch filtert keine Evolution-Sonder-Species.
- Die Logger-Fallbacks fuer `unknown item #1732` sind bewusst diagnostisch, nicht fachlich als DPE-Item-Modell geloest.
- Trainer-Movesets, Held Items, Learnsets/Movesets, TM/Tutor, Ability, Palette und CFRU Day/Night bleiben separate Folgearbeiten.

## Checks

UPR-FVX:

```text
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
```

Workspace:

```text
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

## Sicherheitsstatus

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env`-Dateien committed oder dokumentiert.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`.
- Keine Original-Upstreams kontaktiert.
- Keine CFRU-/DPE-Aenderungen.

## Naechster minimaler Schritt

Nach Review/Merge der UPR-FVX- und Workspace-PRs:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-or-held-items
```
