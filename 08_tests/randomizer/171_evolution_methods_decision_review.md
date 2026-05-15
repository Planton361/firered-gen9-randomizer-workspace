# 171 - Evolution Methods Decision Review

## Scope

- Branch: `test/upr-fvx-cfru-dpe-evolution-methods-decision-review`
- Voraussetzung: Workspace PR #219 / Diagnose 170 ist in `main` gemerged.
- Modus: read-only Diagnose und Non-ROM-Testplanung.
- Ergebnis: `decision-review-ready`

Nicht ausgefuehrt: ROM-Smoke, Randomizer-Lauf, Build, UPR-FVX-Codeaenderung, Submodule-Aenderung, Writer-/Reload-Test, Output-ROM, Save, Emulator oder Log-Artefakt.

## Gelesene Evidenz

- Workspace-Diagnosen 167 bis 170 fuer Evolution-Suboptionen und Methoden-Scope.
- UPR-FVX `GameRandomizer.java` Dispatch fuer Evolution-Improvement-Optionen.
- UPR-FVX `Gen3RomHandler.java` fuer Gen3 `loadEvolutions()`, `writeEvolutions()` und `removeImpossibleEvolutions(...)`.
- UPR-FVX `AbstractRomHandler.java` fuer `removeTimeBasedEvolutions()`, `markImprovedEvolutions(...)` und `hadEvolutionOfType(...)`.
- UPR-FVX `EvolutionType.java` fuer `usesTime()`, `oppositeTime()`, `timeless()`, `isDayType()` und item/level classification.
- UPR-FVX `Evolution.java` fuer `updateEvolutionMethod(...)` und `useEstimatedLevels`.
- Vorhandene Tests: `EvolutionTest`, ROM-backed `RomHandlerEvolutionTest`, Non-ROM `EvolutionFilterOptionsTest`.

## Dispatch-Befund

`FVX-TRAIT-024` und `FVX-TRAIT-027` sind keine Species-Carrier-Filter wie `017/020-023`. Sie mutieren Evolution-Methoden und `extraInfo` direkt:

- `FVX-TRAIT-024` Change Impossible Evolutions: Gen3-spezifisch in `Gen3RomHandler.removeImpossibleEvolutions(changeMoveEvos, useEstimatedLevels)`.
- `FVX-TRAIT-027` Remove Time-Based Evolutions: handler-uebergreifend in `AbstractRomHandler.removeTimeBasedEvolutions()`.

Damit ist der naechste sinnvolle Testpfad ein kleiner ROM-freier Decision-Test, nicht Writer/Reload und nicht ROM-Smoke.

## FVX-TRAIT-024 - Change Impossible Evolutions

### Gesehene Method-Mappings

| Quelle | Bedingung | Ziel-Methode | Ziel-`extraInfo` | Anmerkung |
|---|---|---|---|---|
| `HAPPINESS_DAY` | nur FRLG | `STONE` | `ItemIDs.sunStone` | day happiness wird zu Sun Stone |
| `HAPPINESS_NIGHT` | nur FRLG | `STONE` | `ItemIDs.moonStone` | night happiness wird zu Moon Stone |
| `HIGH_BEAUTY` | nur FRLG | `LEVEL` | `35` oder `estimatedEvoLvl` | Feebas-/Beauty-Ersatz |
| `TRADE` | alle Gen3-Pfade | `LEVEL` | `37` oder `estimatedEvoLvl` | pure Trade |
| `TRADE_ITEM` | Poliwhirl | `LEVEL` | `37` oder `estimatedEvoLvl` | branch nach Source-Species |
| `TRADE_ITEM` | Slowpoke | `STONE` | `ItemIDs.waterStone` | branch nach Source-Species |
| `TRADE_ITEM` | Seadra | `LEVEL` | `40` oder `estimatedEvoLvl` | branch nach Source-Species |
| `TRADE_ITEM` | Clamperl + `deepSeaTooth` | `LEVEL` | `30` oder `estimatedEvoLvl` | branch nach Item-`extraInfo` |
| `TRADE_ITEM` | Clamperl + `deepSeaScale` | `STONE` | `ItemIDs.waterStone` | branch nach Item-`extraInfo` |
| `TRADE_ITEM` | sonstige Trade-Item-Evos | `LEVEL` | `30` oder `estimatedEvoLvl` | Onix/Scyther/Porygon-Kommentar im Code |

### Betroffene ExtraInfo-Felder

- Stone-/Item-Ziele schreiben standardisierte Item-IDs in `extraInfo` auf Datenmodellebene.
- Level-Ziele schreiben Levelwerte in `extraInfo`.
- Wenn `useEstimatedLevels=true` und das Ziel eine Level-Schwelle nutzt, setzt `Evolution.updateEvolutionMethod(...)` statt des hart kodierten Levels den vorhandenen `estimatedEvoLvl`.
- Gen3-Writer-/Reader-Grenze bleibt separat: `loadEvolutions()` wandelt Item-`extraInfo` von internal nach standard, `writeEvolutions()` wandelt Item-`extraInfo` von standard nach internal.

### ROM-frei testbare Decisions

- Synthetische `Evolution`-Objekte koennen die Methode/`extraInfo`-Transformationen fuer Trade, Trade-Item, Beauty und FRLG-Happiness abdecken.
- `useEstimatedLevels=true/false` ist ueber `Evolution.updateEvolutionMethod(...)` bereits ROM-frei pruefbar und sollte fuer Level-Ziele in den `024`-Decision-Test aufgenommen werden.
- Die Clamperl-Zweige brauchen nur synthetische Source-Species-Nummer und `deepSeaTooth`/`deepSeaScale`-`extraInfo`.

### Spaetere Writer-/Reload-Evidenz

- Gen3 Method-Index und Item-ID-Konvertierung muessen spaeter in einem separaten Writer/Reload-Scope belegt werden.
- `attemptObedienceEvolutionPatches()` ist ein Gen3-seitiger Nebeneffekt des aktuellen `024`-Pfads und gehoert nicht in den ersten Decision-Test.
- CFRU/DPE-SpeciesSet-Identity und Evolution-Table-Reload bleiben nicht durch einen reinen Decision-Test bewiesen.

## FVX-TRAIT-027 - Remove Time-Based Evolutions

### Betroffene Time-Methoden

`EvolutionType.usesTime()` wird aus `timeless()` abgeleitet. Der untersuchte Stand enthaelt diese relevanten Time-Familien:

- `HAPPINESS_DAY` / `HAPPINESS_NIGHT`
- `ITEM_DAY` / `ITEM_NIGHT`
- `LEVEL_DAY` / `LEVEL_NIGHT`
- `LEVEL_GAME_THIS_DAY` / `LEVEL_GAME_THIS_NIGHT`
- `LEVEL_GAME_OTHER_DAY` / `LEVEL_GAME_OTHER_NIGHT`
- `LEVEL_DUSK`

### Gesehene Mapping-Entscheidungen

- `LEVEL_DUSK` wird vor dem allgemeinen Time-Zweig speziell zu `STONE` + `ItemIDs.duskStone`.
- Ungepaarte time-based Evolutions werden zu `et.timeless()` gemappt und behalten ihr altes `extraInfo`.
- Gepaarte Day/Night-Splits werden ueber `hadEvolutionOfType(pk, et.oppositeTime())` gegen `preImprovedEvolutions` erkannt.
- Gepaarte Day-Varianten werden zu `STONE` + `ItemIDs.sunStone`.
- Gepaarte Night-Varianten werden zu `STONE` + `ItemIDs.moonStone`.
- `TIME_PAIRS` enthaelt Paare fuer Happiness, Item, Level, Level-Game-This und Level-Game-Other; `LEVEL_DUSK` ist kein Paar, sondern Sonderfall.

### ROM-frei testbare Decisions

- `EvolutionType`-Mapping kann direkt ROM-frei geprueft werden: `timeless()`, `oppositeTime()`, `usesTime()` und `isDayType()`.
- Ein kleiner Handler-Decision-Test kann synthetische Species mit zwei Evolutionen nutzen, um paarige Day/Night-Splits zu Sun/Moon Stone zu pruefen.
- Ein ungepaarter Time-Typ kann pruefen, dass `extraInfo` erhalten bleibt und nur die Methode timeless wird.
- `LEVEL_DUSK` kann pruefen, dass der Sonderfall vor dem allgemeinen `usesTime()`-Pfad greift.

### Spaetere Writer-/Reload-Evidenz

- Item-ID-Konvertierung fuer Sun/Moon/Dusk Stone und Gen3 Evolution-Method-Indizes bleibt Writer/Reload-Scope.
- `preImprovedEvolutions` muss im spaeteren Test sauber ueber `markImprovedEvolutions(...)` oder einen engen Decision-Seam kontrolliert werden; direkte ROM-Handler-Konstruktion ist fuer den ersten Test nicht noetig.
- Reload-Stabilitaet der umgeschriebenen Method-/`extraInfo`-Kombinationen bleibt offen.

## Empfohlener Non-ROM-Testplan

Empfohlen ist ein kleiner UPR-FVX `:romio:test`-Scope mit synthetischen `Species`/`Evolution`-Objekten:

- bevorzugt neue Testdatei nahe `romio/src/test/java/com/uprfvx/romio/romhandlers/EvolutionMethodDecisionTest.java` oder, fuer reine Enum-Checks, `romio/src/test/java/com/uprfvx/romio/gamedata/EvolutionTypeTest.java`;
- enger package-private Decision-Seam nur falls noetig, z. B. fuer die reine Mapping-Entscheidung ohne ROM-Handler-Zustand;
- keine ROM-Datei, keine Save-/Output-Artefakte, kein Gen3-Writer, kein Reload und kein Randomizer-Lauf;
- Assertions fuer `024`: Trade, Trade-Item-Spezialfaelle, FRLG-Happiness, Beauty und `useEstimatedLevels`;
- Assertions fuer `027`: timeless mapping, paired Day/Night split zu Sun/Moon Stone, `LEVEL_DUSK` zu Dusk Stone und Erhalt von `extraInfo` bei ungepaarten Time-Evos.

Wenn ein spaeterer Test nur ueber ROM-Fixtures, private ROM-Pfade, breite Reflection oder vollstaendige `Gen3RomHandler`-Konstruktion moeglich waere, soll der Scope stoppen und als blocked dokumentiert werden.

## Statuswirkung

- `FVX-TRAIT-024` wird von `methods-plan-ready` auf `decision-review-ready` gehoben.
- `FVX-TRAIT-027` wird von `methods-plan-ready` auf `decision-review-ready` gehoben.
- `FVX-TRAIT-025` bleibt getrennt geplant: ROM-freie `condenseLevelEvolutions(...)`-Logik plus separater Gen3-Happiness-Byte-Patch-Risiko-Pfad.
- `FVX-TRAIT-026` bleibt Helper-Flag fuer `024/025` und keine eigenstaendige Promotion.
- Keine dieser Methoden-Slices wird durch Diagnose 171 zu `tested-non-rom`, `Getestet`, `Getestet im Carrier` oder P1-supported.

## Ergebnis

`decision-review-ready`

Die fachlichen Mapping-Entscheidungen fuer `FVX-TRAIT-024` und `FVX-TRAIT-027` sind read-only nachvollzogen und klein genug fuer einen spaeteren ROM-freien Decision-Test. Writer-/Reload- und ROM-Smoke-Evidenz bleibt bewusst separat.
