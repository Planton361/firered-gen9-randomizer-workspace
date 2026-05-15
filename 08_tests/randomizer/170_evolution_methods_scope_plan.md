# 170 - Evolution Methods Scope Plan

## Datum

2026-05-15

## Branch

```text
test/upr-fvx-cfru-dpe-evolution-methods-scope-plan
```

## Voraussetzung

PR #218 / Follow-up 169B wurde vor diesem Plan als in `main` enthalten bestaetigt. UPR-FVX bleibt im Workspace auf:

```text
587e857088cac4fba41c6559d3a6f6e2a7aad71f
```

## Scope

Read-only Plan fuer die getrennten Evolution-Methoden-/Improvement-Slices:

- `FVX-TRAIT-024` Change Impossible Evolutions
- `FVX-TRAIT-025` Make Evolutions Easier
- `FVX-TRAIT-026` Use Estimated Evolution Levels
- `FVX-TRAIT-027` Remove Time-Based Evolutions

Nicht ausgefuehrt:

- kein Testcode
- kein ROM-Smoke
- kein Randomizer-Lauf
- kein Build
- keine Codeaenderung
- keine Aenderung an `02_external/upr-fvx`

## Ergebnis

Klassifikation:

```text
methods-plan-ready
```

Die vier Slices haben klare Codepfade und koennen in einem spaeteren Block getrennt geplant oder getestet werden. Sie sind aber keine Fortsetzung der Non-ROM Filter-Evidenz aus 169B und werden nicht zu `tested-non-rom` oder P1-supported hochgestuft.

## Read-only Befund

### Dispatch

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`

`maybeApplyEvolutionImprovements()` ist vom Species-Carrier `maybeRandomizeEvolutions()` getrennt:

- `settings.isChangeImpossibleEvolutions()` ruft `romHandler.removeImpossibleEvolutions(changeMoveEvos, useEstimatedLevels)` auf.
- `settings.isMakeEvolutionsEasier()` ruft zuerst `romHandler.condenseLevelEvolutions(settings.getMakeEvolutionsEasierLvl())` und danach `romHandler.makeEvolutionsEasier(wildsRandomizer, useEstimatedLevels)` auf.
- `settings.isRemoveTimeBasedEvolutions()` ruft `romHandler.removeTimeBasedEvolutions()` auf.
- `settings.useEstimatedLevelsForEvolutionImprovements()` wirkt nur als Zusatzflag fuer die Methodenpfade, nicht als eigenstaendige Species-Randomization.

### Datenmodell

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Evolution.java`

`Evolution` traegt `from`, `to`, `type`, `extraInfo` und `estimatedEvoLvl`. `updateEvolutionMethod(...)` haelt die Beziehung zwischen Level-basierten Methoden und `extraInfo` / `estimatedEvoLvl` zusammen. `EvolutionTest` deckt diesen Datenmodellteil bereits ROM-frei ab.

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/EvolutionType.java`

`EvolutionType` definiert:

- Level-Threshold-Methoden ueber `usesLevelThreshold()`
- Item-Methoden ueber `usesItem()`
- Zeit-Methoden ueber `usesTime()`, `oppositeTime()` und `timeless()`
- Split-Evo-Sonderfaelle ueber `skipSplitEvo()`

### Gen3 Read/Write-Grenze

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

`loadEvolutions()` liest je Species bis zu fuenf 8-Byte-Eintraege mit Methode, `extraInfo` und Ziel-Species. `writeEvolutions()` schreibt dieselbe Struktur zurueck, inklusive Item-ID-Konvertierung und CFRU/DPE-BPRE-internem SpeciesSet-Identity-Pfad ueber `getEvolutionInternalSpeciesId(...)`.

Damit ist fuer P1-Freigabe spaeter mehr noetig als ein ROM-freier Datenmodelltest: Method-Mapping, Item-/Level-`extraInfo`, Time-/Stone-Umwandlungen und Reload muessen mindestens in einem eng freigegebenen Writer-/Reload-Scope belegt werden.

## Feature-ID-Plan

| Feature-ID | Erwarteter Pfad / Datenmodell | ROM-frei testbar? | Writer-/Reload-Evidenz noetig? | Test-Seam noetig? | Risiken | Empfohlener Mini-Scope |
|---|---|---|---|---|---|---|
| `FVX-TRAIT-024` | `Gen3RomHandler.removeImpossibleEvolutions(...)` aendert Trade, Trade-Item, FRLG-Happiness-Day/Night und High-Beauty in Level- oder Stone-Methoden; `useEstimatedLevels` kann Level-`extraInfo` ersetzen. | teilweise: `Evolution.updateEvolutionMethod(...)` und kleine synthetische Handler-Decision sind ROM-frei testbar; der echte Gen3-Handler beruehrt aber ROM-/RomEntry-Zustand. | ja, fuer P1: Gen3 Method/ExtraInfo/Item-ID-Write und Reload. | wahrscheinlich ja, wenn ohne ROM ein enger Decision-Seam fuer Gen3-Methodenumwandlungen getestet werden soll. | falsches `EvolutionType`-Mapping, Standard-vs-internes Item-ID-Mapping, Level-`extraInfo`, FRLG-Zeitmethode, Trade-Item-Sonderfaelle. | Zuerst read-only/code-review oder kleiner Non-ROM Decision-Seam-Plan nur fuer Methodenumwandlung; danach separat Writer-/Reload-Smoke planen. |
| `FVX-TRAIT-025` | `AbstractRomHandler.condenseLevelEvolutions(...)` senkt Level-Thresholds und `estimatedEvoLvl`; `Gen3RomHandler.makeEvolutionsEasier(...)` patcht Happiness-Bytes im ROM. | teilweise: Condense-Logik ist mit synthetischen Species/Evolutionen ROM-frei testbar; Happiness-Byte-Patch braucht Gen3-ROM-Byte-Kontext oder engen Seam. | ja, fuer Happiness-Patch und Evolution-Reload. | fuer Condense nein oder klein; fuer Happiness-Patch wahrscheinlich ja. | `highestEvoLvl`, intermediate-vs-final Level, `estimatedEvoLvl`, Friendship-Locator, FRLG keine Day/Night-Happiness-Codepfade. | Zuerst Non-ROM Condense/estimated-level Harness planen; Happiness-Patch separat als Gen3 writer/preserve-readback Scope. |
| `FVX-TRAIT-026` | Zusatzflag `useEstimatedLevelsForEvolutionImprovements()` fuer `024/025`; nutzt `Evolution.estimatedEvoLvl`, wenn neue Methode Level-Threshold nutzt. | ja fuer Datenmodell und synthetische Improvement-Entscheidungen; nicht sinnvoll standalone ohne `024/025`. | ja, nur zusammen mit dem jeweiligen `024/025`-Writer-/Reload-Scope. | nein fuer `Evolution`-Datenmodell; eventuell mit `024/025`-Seam. | `estimatedEvoLvl=0` oder unplausible Schaetzung, Abweichung zwischen `extraInfo` und `estimatedEvoLvl`, falsche Anwendung auf Stone/Item-Methoden. | Mit `024` und `025` testen, nicht als eigener PR; vorhandenen `EvolutionTest` gezielt ergaenzen, falls spaeter Code-Test erlaubt ist. |
| `FVX-TRAIT-027` | `AbstractRomHandler.removeTimeBasedEvolutions()` ersetzt Zeitmethoden durch timeless Methoden oder bei gepaarten Split-Evos durch Sun-/Moon-Stone; nutzt `preImprovedEvolutions` ueber `markImprovedEvolutions(...)`. | teilweise: reine `EvolutionType.timeless()`-/Pair-Decision ist ROM-frei testbar; vollstaendige Methode braucht markierte Original-Evolutionen und Handler-Zustand. | ja, fuer Gen3 Method/Item-Write und Reload. | wahrscheinlich ja fuer einen kleinen synthetischen Handler oder package-private Helper, wenn kein ROM verwendet werden darf. | paired Day/Night-Split-Evos, `preImprovedEvolutions`-Vorbedingung, Sun/Moon-Stone-Item-ID-Mapping, `LEVEL_DUSK`-Sonderfall. | Zuerst Non-ROM Decision-Seam-Plan fuer time-based Umwandlung; danach enger Gen3 Writer-/Reload-Smoke nur mit Freigabe. |

## Bestehende Teststruktur

- `romio/src/test/java/com/uprfvx/romio/gamedata/EvolutionTest.java` deckt `Evolution.updateEvolutionMethod(...)` und `useEstimatedLevels` ROM-frei ab.
- `romio/src/test/java/com/uprfvx/romio/romhandlers/RomHandlerEvolutionTest.java` enthaelt ROM-parametrisierte Tests fuer Condense, Remove Impossible, Make Easier, Remove Time-Based und Level/Estimated-Level-Invarianten. Diese Tests sind fuer den aktuellen Workspace-Block nicht auszufuehren, weil sie ROM-Fixtures voraussetzen.
- `random/src/test/java/com/uprfvx/random/randomizers/EvolutionFilterOptionsTest.java` aus PR #42 ist ein gutes Muster fuer synthetische `Species` / `Evolution` Daten, deckt aber bewusst nicht `024` bis `027` ab.

## Empfohlener naechster Schritt

Naechster minimaler Block:

1. Read-only UPR-FVX Code-Review/Non-ROM-Testplan fuer `FVX-TRAIT-024` und `FVX-TRAIT-027` als Method-Mapping-Decision-Seams.
2. `FVX-TRAIT-025` in zwei Teile trennen: ROM-freie `condenseLevelEvolutions(...)`-Logik und Gen3-Happiness-Byte-Patch.
3. `FVX-TRAIT-026` nur zusammen mit `024/025` fuehren; kein standalone Smoke.

Ein spaeterer Code-Test-PR soll stoppen, wenn echte ROM-Fixtures, private Pfade, Output-ROMs, breite Handler-Refactors oder Gen3-Writer-/Reload-Ausfuehrung ohne separate Freigabe noetig werden.

## Statuswirkung

- `FVX-TRAIT-024` bis `FVX-TRAIT-027` werden von `Nicht begonnen` auf `methods-plan-ready` hochgestuft.
- Keine Feature-ID wird als `tested-non-rom`, `Getestet`, `Getestet im Carrier` oder P1-supported markiert.
- `FVX-TRAIT-017` und `FVX-TRAIT-020` bis `FVX-TRAIT-023` bleiben unveraendert `tested-non-rom`.

## Sicherheitsnotizen

- Es wurden nur bestehende Markdown-Diagnosen, Statusdokumente und lokale UPR-FVX-Quellen read-only inspiziert.
- Kein ROM, Save, Emulator State, Build, Randomizer-JAR, Tool-Binary, Log, Output-ROM, privater Pfad, Hash, Secret, Token oder `.env`-Inhalt wurde gelesen, kopiert, geaendert oder dokumentiert.
- Keine Original-Upstreams wurden kontaktiert.
