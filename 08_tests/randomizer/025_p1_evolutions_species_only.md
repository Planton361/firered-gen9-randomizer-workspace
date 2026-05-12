# P1 Evolution Species-only Diagnose

## Datum

2026-05-12

## Branch

Workspace:

```text
analysis/upr-fvx-cfru-dpe-p1-evolutions-species-only
```

UPR-FVX:

```text
compat/upr-fvx-cfru-dpe-trainer-scope-and-write
```

## Ziel

Evolution-Species-only mit vollstaendigem Gen1-Gen9-Species-Pool fuer den aktuellen CFRU/DPE-Gen9-BPRE-Teststand diagnostizieren.

Dieser Block ist read-only gegen UPR-FVX/CFRU/DPE:

- keine Codeaenderungen
- keine funktionalen Fixes
- keine Wild-, Starter-, Static-/Gift-, Trainer-, Learnset-, TM-/Tutor-, Ability-, Palette- oder Day/Night-Fixes

## Voraussetzung

UPR-FVX ist im Workspace auf folgenden Planton361-Fork-Commit gepinnt:

```text
56ec749eca12a8637c20f943b520a9bb6a9d469a
```

Der Commit enthaelt den zuvor bestaetigten Trainer-Scope- und Trainer-Species-Write-Fix. Trainer-Species-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand P1-supported.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Route-1-Fallback-Teststand wie in Protokoll 021 bis 024. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/**` und wurden nicht committed.

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
Log-Groesse: 6833 bytes
```

Der direkte `GameRandomizer.Results`-Diagnoselauf meldet abweichend zur CLI einen Log-Fehler nach erfolgreichem Save:

```text
saveSuccessful=true
logSuccessful=false
logExceptionClass=java.lang.IndexOutOfBoundsException
logExceptionMessage=Index 1732 out of bounds for length 1375
```

Fehlerpfad:

```text
RandomizationLogger.evolutionMethodToString
RandomizationLogger.logEvolutions
RandomizationLogger.logOptionalSections
RandomizationLogger.logResults
GameRandomizer.randomize
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

Vor der Randomization wurden 190 Evolution-Eintraege ueber 165 Quell-Species gelesen:

```text
before.evolutionSources=165
before.evolutionEntries=190
before.toGenerationCounts={1=142, 2=24, 3=7, 4=13, 8=4}
before.hasToGen7=false
before.hasToGen8=true
before.hasToGen9=false
before.badEggOrUnknown=false
```

Nach der Randomization werden Gen7/8/9-Ziele gepickt:

```text
after.evolutionSources=165
after.evolutionEntries=190
after.toGenerationCounts={1=35, 2=16, 3=24, 4=30, 5=20, 6=22, 7=18, 8=13, 9=12}
after.pickedGen4plus=115
after.pickedGen7plus=43
after.hasToGen7=true
after.hasToGen8=true
after.hasToGen9=true
after.badEggOrUnknown=false
```

Beispiele fuer Gen7/8/9-Picks im Direct Results-Lauf:

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

Der echte CLI-Log enthaelt einen nichtleeren Evolution-Abschnitt:

```text
Pokemon Evolutions-------------------------------{PKEV}
Pokemon Evolutions: Randomized/Changed
```

Beispiele aus dem Evolution-Log:

```text
Tentacruel|Silvally|Level-up, lvl. 22+
Exeggcute|Tapu Fini|Level-up, lvl. 16+
Rhydon|Meltan|Use Moon Stone (estimated evo lvl. 53)
Goldeen|Eldegoss|Use Fire Stone (estimated evo lvl. 32)
Forretress|Klawf|Use Link Cable (estimated evo lvl. 34)
Mawile|Maushold|Level-up, lvl. 42+
```

Im Direct Results und im CLI-Log wurden `Bad Egg` und `<unknown>` im Evolution-Kontext nicht beobachtet.

## Write/Reload

Der Reload-Vergleich zeigt, dass Evolution-Species nicht stabil ueber interne SpeciesSet-Identitaet erhalten bleiben:

```text
reload.evolutionSources=122
reload.evolutionEntries=129
reload.toGenerationCounts={1=43, 2=37, 3=35, 4=4, 6=7, 7=3}
reload.hasToGen7=true
reload.hasToGen8=false
reload.hasToGen9=false
reload.badEggOrUnknown=false
writeReloadCompared=1414
writeReloadMismatches=146
writeReloadFirstMismatch=Venusaur#identity=3#number=3#gen=1 expected=[1229:LEVEL:16:0] actual=[404:LEVEL:16:0]
```

Der Write/Reload-Befund ist damit nicht P1-supported:

- die Zahl der reloadbaren Evolution-Eintraege faellt von `190` auf `129`
- Gen8/9-Ziele verschwinden im Reload
- `146` Mismatches werden beim Vergleich ueber interne SpeciesSet-Identitaet gefunden
- der erste Mismatch zeigt einen Ziel-Species-Kollaps von interner Identitaet `1229` auf `404`

## Interpretation

Evolution-Species-only erreicht den vollstaendigen Gen1-Gen9-Replacement-Pool und der Pick-Pfad waehlt Gen7/8/9-Ziele. Der Save erzeugt eine Output-ROM, und der CLI-Log ist nicht leer.

Der Pfad ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand trotzdem noch nicht P1-supported:

- Evolution-Write/Reload erhaelt Species nicht ueber interne SpeciesSet-Identitaet.
- Der Reload verliert viele Evolution-Eintraege und Gen8/9-Ziele.
- Der direkte Logger laeuft nach erfolgreichem Save in `RandomizationLogger.evolutionMethodToString()` auf einen Item-/Methoden-Index ausserhalb der geladenen Item-Liste.

Der Befund passt zum bekannten Risiko im Gen3-Evolution-Schreibpfad: Source- und Target-Species werden dort fuer erweiterte CFRU/DPE-BPRE-Hacks noch nicht konsequent ueber interne SpeciesSet-Identitaet behandelt.

## Benoetigter Folgefix

Ein spaeterer Evolution-Scope-/Write-Fix ist noetig.

Minimaler Scope fuer den naechsten Fixblock:

- Evolution-Source-Zeilen fuer CFRU/DPE ueber interne SpeciesSet-Identitaet behandeln.
- Evolution-Target-Species fuer echte Evolution-Picks ueber interne SpeciesSet-Identitaet schreiben.
- Evolution-Reload per interner SpeciesSet-Identitaet absichern.
- Den Evolution-Logger defensiv gegen nicht aufloesbare Item-/Methoden-ExtraInfos machen.
- Keine Wild-, Starter-, Static/Gift-, Trainer-, Learnset-, TM-/Tutor-, Ability- oder Palette-Fixes im selben Block.

## Risiken

- Es wurde kein BizHawk-Gameplay-Smoke gegen die erzeugte Output-ROM ausgefuehrt.
- Der CLI meldet trotz direktem Log-Fehler Erfolg und schreibt einen nichtleeren Teil-Log; die technische Bewertung basiert deshalb auf direktem `GameRandomizer.Results` plus Write/Reload-Vergleich.
- Die Diagnose nutzt denselben lokalen CFRU/DPE-BPRE-Teststand wie die vorherigen Protokolle; andere ROM-Staende koennen andere Evolution-Methoden-/Item-Tabellenlaengen haben.

## Sicherheitsstatus

- Keine Codeaenderungen.
- Keine Aenderungen in `02_external/**`.
- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env`-Dateien committed oder dokumentiert.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`.
- Keine Original-Upstreams kontaktiert.

## Naechster minimaler Schritt

Nach Review/Merge dieses Diagnosebranches:

```text
compat/upr-fvx-cfru-dpe-evolutions-scope-and-write
```

Ziel: Evolution-Species-Scope, Evolution-Species-Write/Reload und Evolution-Log defensiv fuer CFRU/DPE absichern, ohne andere Randomizer-Pfade zu veraendern.
