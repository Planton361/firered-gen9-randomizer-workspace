# 167 - Evolution Suboptions Consolidation

## Datum

2026-05-15

## Branch

```text
test/upr-fvx-cfru-dpe-evolution-suboptions-consolidation
```

## Scope

Read-only Konsolidierung der Evolution-Feature-IDs `FVX-TRAIT-016` bis `FVX-TRAIT-027` im getesteten CFRU/DPE Gen9-BPRE-Scope.

Nicht ausgefuehrt:

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
evolution-scope-consolidated
```

Der enge Evolution-Species-Carrier ist sauber getrennt von Evolution-Methoden-/Improvement-Writern:

- `FVX-TRAIT-016` bleibt P1-supported.
- `FVX-TRAIT-018` und `FVX-TRAIT-019` sind nach Diagnose 165/166 `diagnosis-ready` und nicht mehr aktive 070-Blocker.
- `FVX-TRAIT-017` und `FVX-TRAIT-020` bis `FVX-TRAIT-023` bleiben plan-only, weil sie zwar im `EvolutionRandomizer`-Species-Carrier liegen, aber noch keine eigene CFRU/DPE-Gen9-BPRE-Evidenz haben.
- `FVX-TRAIT-024` bis `FVX-TRAIT-027` bleiben nicht begonnen und ausserhalb des engen Species-Carrier, weil sie Evolution-Methoden, ExtraInfo, Level, Items, Time oder ROM-Handler-Improvement-Pfade beruehren.

## Konsolidierte Matrix

| Feature-ID | Feature | Status | Evidenz | Im engen Evolution-Species-Carrier? | Naechster minimaler Schritt |
|---|---|---|---|---|---|
| `FVX-TRAIT-016` | Pokemon Evolutions randomisieren | P1-supported | Diagnose 026 | ja, Basis-Carrier | Kein Fix; nur Regression bei neuer Evidenz |
| `FVX-TRAIT-017` | Evolutions: Random Every Level | plan-only | Diagnose 060/061, UPR-FVX `EvolutionRandomizerTest` read-only | ja, aber nicht CFRU/DPE-spezifisch bestaetigt | Non-ROM-Harness-Plan oder spaeter eng freigegebener Smoke |
| `FVX-TRAIT-018` | Evolutions: Similar Strength | diagnosis-ready | Diagnose 081/082/165 | ja | Kein Fix; optional Code-Review/Harness-Plan |
| `FVX-TRAIT-019` | Evolutions: Same Typing | diagnosis-ready | Diagnose 079/080/166 | ja | Kein Fix; optional Code-Review/Harness-Plan |
| `FVX-TRAIT-020` | Evolutions: Limit to Three Stages | plan-only | Diagnose 060/061, UPR-FVX `EvolutionRandomizerTest` read-only | ja, Graph-Constraint | Non-ROM-Harness-Plan fuer Graph-Constraint |
| `FVX-TRAIT-021` | Evolutions: No Convergence | plan-only | Diagnose 060/061, UPR-FVX `EvolutionRandomizerTest` read-only | ja, Graph-Constraint | Non-ROM-Harness-Plan fuer Graph-Constraint |
| `FVX-TRAIT-022` | Evolutions: Force Change | plan-only | Diagnose 060/061, UPR-FVX `EvolutionRandomizerTest` read-only | ja, Ziel-Filter | Non-ROM-Harness-Plan fuer Ziel-Filter |
| `FVX-TRAIT-023` | Evolutions: Force Growth | plan-only | Diagnose 060/061, UPR-FVX `EvolutionRandomizerTest` read-only | ja, BST-Filter | Non-ROM-Harness-Plan fuer BST-Filter |
| `FVX-TRAIT-024` | Change Impossible Evolutions | nicht begonnen | Diagnose 060/061 als Ausschluss; UPR-FVX `GameRandomizer.maybeApplyEvolutionImprovements()` read-only | nein | Separater read-only Methoden-/ExtraInfo-Plan |
| `FVX-TRAIT-025` | Make Evolutions Easier | nicht begonnen | Diagnose 060/061 als Ausschluss; `condenseLevelEvolutions(...)` / `makeEvolutionsEasier(...)` read-only | nein | Separater read-only Level-/Methoden-Plan |
| `FVX-TRAIT-026` | Use Estimated Evolution Levels | nicht begonnen | Diagnose 061 als Ausschluss; nur mit 024/025 relevant | nein, Improvement-Zusatzflag | Mit 024/025 planen, nicht standalone promoten |
| `FVX-TRAIT-027` | Remove Time-Based Evolutions | nicht begonnen | Diagnose 060/061 als Ausschluss; `removeTimeBasedEvolutions()` read-only | nein | Separater read-only Time-Based-Methoden-Plan |

## Read-only Codebefund

### EvolutionRandomizer-Species-Carrier

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`

`randomizeEvolutions()` liest diese Optionen und fuehrt sie im Species-Replacement-Pfad zusammen:

- `settings.getEvolutionsMod() == RANDOM_EVERY_LEVEL`
- `settings.isEvosSimilarStrength()`
- `settings.isEvosSameTyping()`
- `settings.isEvosMaxThreeStages()`
- `settings.isEvosNoConvergence()`
- `settings.isEvosForceChange()`
- `settings.isEvosForceGrowth()`

Der aktuelle Code trennt die Filter sauber:

- Random Every Level erzeugt pro Species eine Level-1-Evolution.
- Similar Strength nutzt `SpeciesSet.getRandomSimilarStrengthSpecies(...)`.
- Same Typing nutzt `hasUsableSharedType(...)` und schuetzt vor null/unsupported Primary-Type-Kandidaten.
- Limit to Three Stages nutzt `breaksStageLimit(...)`.
- No Convergence verlangt leere `EvolutionsTo`.
- Force Change schliesst originale Ziele aus.
- Force Growth verlangt hoeheren BST-Wert.

Diese Pfade sind technisch Species-Carrier-/Filterlogik, aber nur `018` und `019` haben nach 165/166 neu konsolidierte CFRU/DPE-Evidenz. `017` und `020` bis `023` bleiben deshalb nicht promoted.

### Gen3 Evolution Read/Write

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

Diagnose 026 bleibt die Basis fuer `FVX-TRAIT-016`:

- `loadEvolutions()` und `writeEvolutions()` lesen/schreiben Method, ExtraInfo und Ziel-Species.
- Im erweiterten BPRE-Hack nutzt `getEvolutionInternalSpeciesId(...)` `species.getSpeciesSetIdentityNumber()`.
- Der Reload-Vergleich aus 026 meldete `writeReloadMismatches=0`.

### Evolution-Improvement-Pfade

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`

`maybeApplyEvolutionImprovements()` ist ein anderer Block als `maybeRandomizeEvolutions()`:

- `Change Impossible Evolutions` ruft `romHandler.removeImpossibleEvolutions(changeMoveEvos, useEstimatedLevels)` auf.
- `Make Evolutions Easier` ruft `condenseLevelEvolutions(...)` und `makeEvolutionsEasier(...)` auf.
- `Remove Time-Based Evolutions` ruft `removeTimeBasedEvolutions()` auf.
- `Use Estimated Evolution Levels` wirkt als Zusatzflag fuer 024/025.

Damit sind `024` bis `027` keine automatische Fortsetzung des Species-Carrier-Supports und duerfen nicht aus `016`, `018` oder `019` hochgestuft werden.

## Was durch 165/166 bereinigt ist

Der alte 070-Blocker ist fuer die engen Slices nicht mehr aktiv:

- `FVX-TRAIT-018`: Diagnose 081/082/165 zeigen, dass der alte Mismatch-Zaehler durch Normalisierung ueberholt ist; normalisierter Reload meldet `0` Mismatches.
- `FVX-TRAIT-019`: Diagnose 079/080/166 zeigen, dass der alte Same-Typing-Null-Primary-Type-Abbruch durch den Guard ueberholt ist; Same Typing meldet Save/Log/Output/Reload true und `writeReloadEvolutionMismatches=0`.

Nicht bereinigt sind die offenen Graph-/Filter-Suboptionen `017` und `020` bis `023` sowie die Improvement-/Methoden-Slices `024` bis `027`.

## Empfohlener naechster Pfad

Kein UPR-FVX-Fixblock ist aus dieser Konsolidierung direkt abzuleiten.

Naechster minimaler Arbeitspfad:

1. Wenn Evolution-Suboptionen weiter priorisiert bleiben, zuerst einen read-only Non-ROM-Harness-Plan fuer `017` und `020` bis `023` erstellen.
2. Danach die Improvement-/Methoden-Slices `024` bis `027` separat planen, beginnend mit `Change Impossible Evolutions`, weil dieser Pfad Method/ExtraInfo und optional Move-Evolution-Abhaengigkeiten beruehrt.
3. ROM-Smoke oder Writer-Ausfuehrung nur mit separater expliziter Freigabe.

## Sicherheitsnotizen

- Es wurden nur bestehende Markdown-Diagnosen, Statusdokumente und lokale UPR-FVX-Quellen read-only inspiziert.
- Kein ROM, Save, Emulator State, Build, Randomizer-JAR, Tool-Binary, Log, Output-ROM, privater Pfad, Hash, Secret, Token oder `.env`-Inhalt wurde gelesen, kopiert, geaendert oder dokumentiert.
- Keine Original-Upstreams wurden kontaktiert.
