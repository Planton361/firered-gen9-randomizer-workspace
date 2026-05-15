# 169 - Evolution Filter Non-ROM Harness Follow-up

## Datum

2026-05-15

## Branch

```text
test/upr-fvx-cfru-dpe-evolution-filter-non-rom-harness-followup
```

## Voraussetzung

UPR-FVX PR #42 wurde vor diesem Workspace-Follow-up als gemerged bestaetigt:

```text
https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/42
```

Merge-Ziel:

```text
compat/firered-gen9-cfru-dpe
```

## Submodule-Pin

Der Workspace-Submodule-Gitlink `02_external/upr-fvx` wurde auf den gemergten UPR-FVX-Stand gepinnt:

```text
587e857088cac4fba41c6559d3a6f6e2a7aad71f
```

Urspruenglicher UPR-FVX-Testcommit aus 169A:

```text
e71a126c test: cover evolution filter options
```

Vorheriger Workspace-Pin:

```text
dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c
```

## Geaenderte UPR-FVX-Datei

```text
random/src/test/java/com/uprfvx/random/randomizers/EvolutionFilterOptionsTest.java
```

## Getestete Feature-IDs

Der gemergte Non-ROM-Harness deckt diese Evolution-Filter-Slices ab:

| Feature-ID | Feature | Teststatus |
|---|---|---|
| `FVX-TRAIT-017` | Evolutions: Random Every Level | `tested-non-rom` |
| `FVX-TRAIT-020` | Evolutions: Limit to Three Stages | `tested-non-rom` |
| `FVX-TRAIT-021` | Evolutions: No Convergence | `tested-non-rom` |
| `FVX-TRAIT-022` | Evolutions: Force Change | `tested-non-rom` |
| `FVX-TRAIT-023` | Evolutions: Force Growth | `tested-non-rom` |

## Test-/Seam-Entscheidung

- Kein Produktivcode-Seam wurde benoetigt.
- Der Test nutzt synthetische `Species`- und `Evolution`-Daten.
- Ein minimaler `RomHandler`-Proxy/Fake stellt `RestrictedSpeciesService` und die benoetigten Species-Sets bereit.
- Der Test bleibt im `:random:test`-Scope und beruehrt keinen Gen3 Writer.
- Kein ROM reload/smoke, kein Save, kein Emulator und kein Output-ROM sind Teil des Nachweises.
- `FVX-TRAIT-024` bis `FVX-TRAIT-027` bleiben ausserhalb dieses Scopes.

## Checks aus 169A

Die UPR-FVX-Implementierungsseite meldete:

```text
./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.EvolutionFilterOptionsTest
BUILD SUCCESSFUL

./gradlew --offline :random:test
BUILD SUCCESSFUL
```

## Statuswirkung

`FVX-TRAIT-017` und `FVX-TRAIT-020` bis `FVX-TRAIT-023` werden von `harness-plan-ready` auf `tested-non-rom` hochgestuft.

Diese Hochstufung bedeutet:

- Die Filterlogik ist ROM-frei im `EvolutionRandomizer` mit synthetischen Daten belegt.
- Es ist keine automatische `P1-supported`-Freigabe, weil kein ROM-Smoke, kein Reload und kein Gen3-Evolution-Writer-Scope in diesem Block ausgefuehrt wurden.
- Die Slices bleiben konservativ als Evolution-Species-Carrier-/Filter-Evidenz gefuehrt.
- `FVX-TRAIT-024` bis `FVX-TRAIT-027` bleiben nicht begonnen und separat, weil sie Evolution-Methoden, ExtraInfo, Level, Items oder Time-Pfade betreffen.

## Grenzen

Nicht ausgefuehrt und nicht freigegeben:

- kein ROM-Smoke
- kein Gen3 Writer-Test
- kein Reload
- kein Randomizer-Lauf
- kein Output-ROM
- kein Scope fuer `FVX-TRAIT-024` bis `FVX-TRAIT-027`
- keine Feature-Hochstufung zu `P1-supported`

## Naechster sinnvoller Schritt

Naechster enger Evolution-Pfad:

1. `FVX-TRAIT-024` bis `FVX-TRAIT-027` getrennt als Evolution-Methoden-/Improvement-Scope planen.
2. Optional spaeter entscheiden, ob fuer `FVX-TRAIT-017` und `020-023` ein separat freigegebener ROM-Smoke ueberhaupt notwendig ist.

## Sicherheitsnotizen

- Es wurden keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Tool-Binaries, Logs, Output-ROMs, privaten Pfade, Hashes, Secrets, Tokens oder `.env`-Dateien beruehrt oder dokumentiert.
- In diesem Workspace-Block wurden keine UPR-FVX-Codeaenderungen vorgenommen; nur der Submodule-Gitlink wurde auf den gemergten Stand gepinnt.
- Keine Original-Upstreams wurden kontaktiert.
