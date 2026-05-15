# 168 - Evolution Filter Harness Plan

## Datum

2026-05-15

## Branch

```text
test/upr-fvx-cfru-dpe-evolution-filter-harness-plan
```

## Scope

Read-only Plan fuer einen kleinen Non-ROM-Harness zu den Evolution-Filter-Slices:

- `FVX-TRAIT-017` Evolutions: Random Every Level
- `FVX-TRAIT-020` Evolutions: Limit to Three Stages
- `FVX-TRAIT-021` Evolutions: No Convergence
- `FVX-TRAIT-022` Evolutions: Force Change
- `FVX-TRAIT-023` Evolutions: Force Growth

Nicht ausgefuehrt:

- kein Testcode
- kein ROM-Smoke
- kein Randomizer-Lauf
- kein Build
- keine Codeaenderung
- keine Aenderung an `02_external/upr-fvx`

UPR-FVX blieb im Workspace auf:

```text
dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c
```

## Ergebnis

Klassifikation:

```text
harness-plan-ready
```

Alle fuenf Ziel-Slices sind im aktuellen UPR-FVX-Code ROM-frei testbar, wenn der Test synthetische `Species`, `Evolution`-Kanten und einen minimalen `RomHandler`-Proxy/Fake verwendet. Ein Produktivcode-Seam ist voraussichtlich nicht noetig.

## Read-only Befund

### EvolutionRandomizer

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`

Der relevante Pfad ist `randomizeEvolutions()`:

- liest `settings.getEvolutionsMod() == RANDOM_EVERY_LEVEL`
- liest `settings.isEvosMaxThreeStages()`
- liest `settings.isEvosNoConvergence()`
- liest `settings.isEvosForceChange()`
- liest `settings.isEvosForceGrowth()`
- baut den Pool ueber `romHandler.getRestrictedSpeciesService().getSpecies(...)`
- filtert in `findPossibleReplacements(...)`
- schreibt nur in die synthetischen `Species.getEvolutionsFrom()` / `getEvolutionsTo()`-Listen

Damit kann ein Non-ROM-Test den Mutationspfad ohne Gen3-ROM-Bytes, Save, Writer oder Reload pruefen.

### Bestehende Tests

`02_external/upr-fvx/random/src/test/java/com/uprfvx/random/randomizers/EvolutionRandomizerTest.java`

Es gibt bereits ROM-parametrisierte Tests fuer:

- Random Every Level erzeugt genau eine Level-1-Evolution.
- Random Every Level waehlt nicht sich selbst.
- Random Every Level erhaelt die Growth Curve.
- Random Every Level + Force Change.
- Random Every Level + Same Typing.
- Random Every Level + No Convergence.
- Limit to Three Stages.
- Force Change.
- Force Growth.
- No Convergence.

Diese Tests laden aber ueber `RandomizerTest` echte Test-ROMs aus `romsPath`. Der geplante Scope soll kleiner sein und keine ROM-Datei brauchen.

### Fake-/Proxy-Muster

`02_external/upr-fvx/random/src/test/java/com/uprfvx/random/randomizers/TradeRandomizerTest.java`

Der vorhandene Trade-Test zeigt ein brauchbares Non-ROM-Muster:

- `RomHandler` per `Proxy.newProxyInstance(...)`
- `RestrictedSpeciesService` und `TypeService` auf dem Proxy
- synthetischer `SpeciesSet`
- nur die vom Randomizer benoetigten `RomHandler`-Methoden werden beantwortet

Dieses Muster ist fuer Evolution-Filter direkt uebertragbar.

## Geplanter Test-Scope

Bevorzugte UPR-FVX-Testdatei:

```text
random/src/test/java/com/uprfvx/random/randomizers/EvolutionRandomizerTest.java
```

Alternativ, wenn die bestehende Datei durch ROM-parametrisierte Tests zu unuebersichtlich bleibt:

```text
random/src/test/java/com/uprfvx/random/randomizers/EvolutionFilterRandomizerTest.java
```

Der Test soll synthetische Species mit stabilen Feldern anlegen:

- `Species.number`
- `name`
- `growthCurve`
- BST-relevante Stats fuer Force Growth
- optionale Type-Felder nur wenn spaeter mit Same Typing kombiniert wird; fuer diesen Block nicht noetig
- `Evolution`-Kanten ueber `getEvolutionsFrom()` und `getEvolutionsTo()`

Der Fake/Proxy muss voraussichtlich beantworten:

- `getRestrictedSpeciesService`
- `getTypeService`, falls der Basiskonstruktor oder Services ihn anfragen
- `getSpeciesSetInclFormes`
- `getSpeciesSet`
- `getSpeciesInclFormes`
- `getSpecies`
- `getAltFormes`
- `getMegaEvolutions`
- `getIrregularFormes`
- `altFormesCanHaveDifferentEvolutions`
- `getAllowedItems`, falls `RestrictedSpeciesService` oder verwandte Services danach fragen

## Feature-ID-Plan

| Feature-ID | ROM-frei testbar? | Voraussichtliche Testdatei | Test-Seam noetig? | Sinnvolle Assertions | Weiter verboten |
|---|---|---|---|---|---|
| `FVX-TRAIT-017` | ja | `EvolutionRandomizerTest` oder `EvolutionFilterRandomizerTest` | nein, Proxy/Fake reicht | jede synthetische Species bekommt genau eine Evolution; Type `LEVEL`; `extraInfo=1`; keine Self-Evolution; `isChangesMade=true` | kein ROM, kein Save/Reload, kein Gen3 Writer |
| `FVX-TRAIT-020` | ja | `EvolutionRandomizerTest` oder `EvolutionFilterRandomizerTest` | nein | maximale Evolutionskette bleibt `<=3`; keine Zyklen; bestehende Growth-Curve-Constraint bleibt erhalten | keine Methoden-/ExtraInfo-Umschreibung |
| `FVX-TRAIT-021` | ja | `EvolutionRandomizerTest` oder `EvolutionFilterRandomizerTest` | nein | keine Ziel-Species hat mehr als eine `EvolutionsTo`-Kante; keine Konvergenz entsteht | keine Validierung per ROM-Reload |
| `FVX-TRAIT-022` | ja | `EvolutionRandomizerTest` oder `EvolutionFilterRandomizerTest` | nein | neue Ziel-Species ist nicht in der urspruenglichen Zielmenge der Source-Species | keine Species-Write-Smoke-Freigabe |
| `FVX-TRAIT-023` | ja | `EvolutionRandomizerTest` oder `EvolutionFilterRandomizerTest` | nein | jedes neue Ziel hat `getBSTForPowerLevels() > from.getBSTForPowerLevels()`; Testpool muss absichtlich ausreichend groessere Kandidaten enthalten | kein Similar-Strength-Smoke, kein Balance-/BST-Globaltest |

## Minimale Harness-Strategie

1. Einen synthetischen Pool mit mehreren Growth-Curve-kompatiblen Species erstellen.
2. Vor dem Randomizer explizite Original-Evolutionen setzen, damit `allOriginalEvos` und Filter wie Force Change/Stage Limit belastbar arbeiten.
3. Einen kleinen `RomHandler`-Proxy analog `TradeRandomizerTest` verwenden.
4. `RestrictedSpeciesService.setRestrictions(null)` im Fake-Setup ausloesen oder sicherstellen, dass der Service beim Randomizerzugriff bereits gesetzt ist.
5. Pro Feature-ID einen fokussierten Test schreiben; keine kombinierten Mega-Slices ausser einer bewusst kleinen `Random Every Level + No Convergence`-Regression, falls sie beim selben Fake kaum zusaetzlichen Scope kostet.

## Stop-Kriterien fuer spaeteren Code-Test-PR

Ein spaeterer UPR-FVX-Testblock soll stoppen, wenn:

- ein echtes ROM, ein Save, ein Emulator, ein Output-ROM oder ein privater ROM-Pfad noetig wird.
- ein Produktivcode-Seam groesser als ein enger package-private Testzugang noetig waere.
- `Gen3RomHandler.writeEvolutions()` oder ROM-Bytes getestet werden muessten.
- `FVX-TRAIT-024` bis `FVX-TRAIT-027` in denselben Testblock gezogen werden muessten.
- Text/Menu, Items, MoveData, TypeChart, Palette, Graphics, Wild, Trainer, Starter, Static/Gift oder In-Game-Trades betroffen waeren.

## Empfohlener naechster Schritt

Naechster Arbeitsblock, falls freigegeben:

- UPR-FVX-Branch fuer einen kleinen `:random:test` Non-ROM-Harness.
- Fokus nur auf `EvolutionRandomizer`.
- Keine ROM-Datei, kein `romsPath`, kein Gen3 Writer, kein Build-Artefakt-Commit.
- Erwarteter Testbefehl: `./gradlew --offline :random:test`, falls lokal ohne Downloads moeglich.

## Sicherheitsnotizen

- Es wurden nur bestehende Markdown-Diagnosen, Statusdokumente und lokale UPR-FVX-Quellen read-only inspiziert.
- Kein ROM, Save, Emulator State, Build, Randomizer-JAR, Tool-Binary, Log, Output-ROM, privater Pfad, Hash, Secret, Token oder `.env`-Inhalt wurde gelesen, kopiert, geaendert oder dokumentiert.
- Keine Original-Upstreams wurden kontaktiert.
