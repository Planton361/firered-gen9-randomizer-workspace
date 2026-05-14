# 063 - P1 Starters Suboptions Regression-Smoke-Plan

## Ziel

Dieses read-only Protokoll plant den naechsten Regression-Smoke fuer Starter-Suboptionen aus Diagnose 061/062. Es fuehrt keinen Randomizer-Lauf aus, erhebt keine neuen Diagnosewerte und aendert keinen Code.

Der Smoke soll Starter-Poolfilter ueber den bereits belegten Starter-Species-Writer isolieren. Starter Held Items und andere offene Writer bleiben ausgeschaltet.

Scope:

- Nur bestehende Protokolle, Feature-Coverage-Dokumentation und read-only Befunde.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, ROM-Namen, Hashes, Secrets oder `.env`-Inhalte gelesen oder dokumentiert.

## Belegbasis

Primaere Belege:

- `047_fvx_gui_options_compatibility_matrix.md`
- `055_type_log_placeholder_hygiene.md`
- `060_p1_gui_suboptions_regression_matrix.md`
- `061_p1_regression_smoke_plan.md`
- `062_p1_global_species_pool_regression_smoke.md`

Feature- und Roadmap-Belege:

- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`

Wichtige Grenzen aus den Belegen:

- 047 klassifiziert Starters als P1-supported fuer den belegten Starter-Species-Write/Reload-Pfad.
- 055 trennt `Bad Egg`, `<unknown>` und Unknown-/Fallback-Marker von echten Save-/Reload-Blockern.
- 060 stuft Starter-Poolfilter wie random basic/two evolutions, Type Restrictions, No Legendaries und BST limits konservativ als `wahrscheinlich supported, aber nicht einzeln getestet` ein.
- 061 plant Starter-Suboptionen als eigene Smoke-Gruppe ueber einen bereits stabilen Starter-Species-Writer, ohne Starter-Held-Item-Writer.
- 062 ist die Grenze fuer Global Species Pools / Generation Limits. 063 mischt diese Optionen nicht in den Starter-Smoke, ausser eine spaetere Kombination wird ausdruecklich separat freigegeben.

## Feature-IDs

Primaere Feature-IDs fuer 063:

| Feature-ID | Feature | Coverage-Status | 060-Status | 063-Einordnung |
|---|---|---|---|---|
| `FVX-SST-002` | Starter Pokemon: Random completely | GUI-kompatibel | P1-supported | belegter Basis-/Carrier-Pfad |
| `FVX-SST-003` | Starter Pokemon: Random basic with 2 evolutions | GUI-kompatibel | wahrscheinlich supported, aber nicht einzeln getestet | Regression-Kandidat |
| `FVX-SST-004` | Starter Pokemon: Random any basic | GUI-kompatibel | wahrscheinlich supported, aber nicht einzeln getestet | Regression-Kandidat |
| `FVX-SST-005` | Starter Type Restrictions | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-SST-006` | Starter: Don't Use Legendaries | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-SST-009` | Starter BST-Min/Max | Nicht begonnen | wahrscheinlich supported, aber nicht einzeln getestet | konservativer separater Slice |

`FVX-SST-002` wird nicht neu hochgestuft. Es dient als belegter Starter-Species-Writer, auf dem die Suboptionen spaeter isoliert beobachtet werden koennen.

## Geplante Smoke-Slices

063 definiert nur spaetere Smoke-Slices. Es fuehrt sie nicht aus.

| Slice | Aktive Hauptidee | Feature-IDs | Zweck |
|---|---|---|---|
| A | Baseline | `FVX-SST-002` | stabilen Starter-Writer ohne weitere Starter-Poolfilter als Vergleichsoberflaeche halten |
| B | Basic / Evolution Filter | `FVX-SST-003`, `FVX-SST-004` | random basic / two evolutions und random any basic ohne Type-/BST-/Legendary-Filter isolieren |
| C | Type Restrictions | `FVX-SST-005` | Starter-Type-Filter pruefbar machen; nutzt Species-Type-Felder, nicht TypeChart / Type Effectiveness |
| D | Legendary Filter | `FVX-SST-006` | Don't Use Legendaries getrennt von Alt-/Forme-Risiken isolieren |
| E | BST-Min/Max | `FVX-SST-009` | BST-Grenzen separat planen, damit Pool-Engpaesse nicht mit anderen Filtern vermischt werden |

Settings werden spaeter normalisiert als Feature-IDs, aktiver Slice, Starter-Carrier und ausgeschlossene Writer dokumentiert. 063 traegt keine Laufwerte ein.

## Erlaubte Settings fuer spaetere Laeufe

Nur diese Starter-Settings duerfen fuer den spaeteren 063-Smoke aktiv sein:

- `FVX-SST-002` als Baseline- bzw. Carrier-Pfad.
- `FVX-SST-003` und `FVX-SST-004` nur im Basic-/Evolution-Filter-Slice.
- `FVX-SST-005` nur im Type-Restrictions-Slice.
- `FVX-SST-006` nur im Legendary-Filter-Slice.
- `FVX-SST-009` nur im separaten BST-Min/Max-Slice.

Alle anderen GUI-Optionen sollen auf unveraendert oder aus bleiben, soweit sie nicht technisch noetig sind, um den Starter-Carrier ueberhaupt auszufuehren.

## Explizit ausgeschlossene Writer und Suboptionen

Diese Bereiche duerfen nicht in den 063-Smoke-Plan eingeschleust werden:

- `FVX-SST-007` Starter Held Items randomisieren.
- `FVX-SST-008` Starter Held Items: Ban Bad Items.
- Field Items, Shops, Pickup.
- Encounter Held Items als eigener Datenpfad.
- MoveData Write / Update Moves.
- Palette Randomization / Graphics / Sprites.
- TypeChart / Type Effectiveness.
- Text / Menu / Description.
- Trainer/Wild Level Modifier.
- Evolution-Methoden-Writer wie Change Impossible Evolutions, Make Evolutions Easier, method/item/move/location changes.
- Global Species Pool Optionen aus 062, ausser wenn ausdruecklich als eigene spaetere Kombination freigegeben.

## Grenzen

### Grenze zu Starter Held Items

`FVX-SST-007` und `FVX-SST-008` bleiben ausserhalb von 063. Starter Held Items sind ein eigener Item-Writer bzw. Item-Poolfilter und werden nicht durch Encounter Held Items aus 054, Field-/Shop-/Pickup-Modell 057 oder den Starter-Species-Writer belegt.

### Grenze zu Global Species Pools

062 plant `FVX-GEN-001` und `FVX-GEN-002` als eigene Global-Species-Pool-Smokes. 063 darf diese Optionen nicht stillschweigend dazunehmen, weil sonst unklar waere, ob ein Pool-Engpass aus Starter-Filtern oder Global-Filtern stammt.

### Grenze zu TypeChart

`FVX-SST-005` nutzt Species-Type-Felder aus dem belegten Type-Read/Write-Scope, aber beweist keinen TypeChart- oder Type-Effectiveness-Support. TypeChart bleibt durch Diagnose 059 begrenzt.

## Erwartete spaetere Metriken

Ein spaeterer, separat freigegebener Lauf soll folgende Kriterien dokumentieren. 063 traegt keine Werte ein.

| Kriterium | Erwartung |
|---|---|
| Save | `saveSuccessful=true` |
| Log | `logSuccessful=true`, `logNonEmpty=true` |
| Output | Output-ROM vorhanden, ohne Pfad oder ROM-Namen zu dokumentieren |
| Reload | Reload erfolgreich |
| Mismatches | Starter-relevanter Write/Reload-Mismatch-Zaehler `0` |
| Stacktrace | `stacktrace=none` |
| Feature-Trace | aktive Feature-IDs und normalisierte Settings dokumentiert |
| Carrier | Starter-Carrier klar benannt |
| Marker | Marker aus 055 nur klassifizieren, nicht automatisch als Fehler werten |
| Artefakte | keine ROMs, Logs, Output-ROMs, Builds, JARs, private Pfade, Hashes oder Secrets dokumentiert oder committed |

Der genaue Starter-Mismatch-Zaehler darf erst aus einem tatsaechlichen spaeteren Diagnosepfad uebernommen werden.

## Artefakt- und Datenschutzregeln

Falls ein spaeterer Lauf separat freigegeben wird:

- Lokale Outputs bleiben ignored, z. B. unter einem passenden `05_builds/randomizer-smoke/063_p1_starters_suboptions_regression_smoke/`-Arbeitsordner.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs oder Tool-Binaries werden committed.
- Keine privaten Pfade, ROM-Namen, Hashes, Seeds mit privatem Kontext, Secrets, Tokens oder `.env`-Inhalte werden dokumentiert.
- Aus Logs werden nur freigegebene, sanitisiert zusammengefasste Metriken uebernommen.

## Stop-Regeln

Ein spaeterer 063-Umsetzungs- oder Laufblock stoppt, wenn:

1. Der Branch `main` ist oder der Worktree unerwartet dirty ist.
2. Starter Held Items aktiviert werden muessten.
3. Ein offener Writer aus 056-059 oder aus der Ausschlussliste in den Smoke geraet.
4. Type Restrictions als TypeChart- oder Type-Effectiveness-Support interpretiert werden sollen.
5. BST-Min/Max mit anderen Poolfiltern vermischt werden soll.
6. `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` oder `FVX-SST-009` ohne separaten spaeteren Lauf auf P1-supported hochgestuft werden sollen.
7. Ein Lauf ROMs, Logs, Builds, Output-ROMs, Tool-Binaries, private Pfade, ROM-Namen, Hashes, Secrets, Tokens oder `.env`-Inhalte offenlegen wuerde.
8. Neue Diagnosewerte ohne tatsaechlichen, separat freigegebenen Lauf eingetragen werden muessten.
9. `Bad Egg`, `<unknown>` oder Unknown-/Fallback-Marker ohne 055-Kontext als neuer Fehler bewertet werden sollen.

## Ergebnis

063 legt den read-only Regression-Smoke-Plan fuer Starter-Suboptionen fest. Der Plan bleibt ohne Ausfuehrung, ohne neue Werte und ohne Fix. `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` werden ueber den belegten Starter-Species-Writer geplant, waehrend Starter Held Items und offene Writer strikt ausgeschlossen bleiben.

Naechster sinnvoller Block nach diesem Plan:

- `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke` fuer BST-/Type-basierte Pooling-Suboptionen, ohne TypeChart oder MoveData-Write zu aktivieren.
