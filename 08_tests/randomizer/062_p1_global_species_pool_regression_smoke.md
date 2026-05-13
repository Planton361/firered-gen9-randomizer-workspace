# 062 - P1 Global Species Pool Regression-Smoke-Plan

## Ziel

Dieses read-only Protokoll plant den ersten spaeteren Regression-Smoke aus Diagnose 061 fuer Global Species Pools / Generation Limits. Es fuehrt keinen Randomizer-Lauf aus, erhebt keine neuen Diagnosewerte und aendert keinen Code.

Der Smoke soll Pool-Filter wie `Limit Pokemon`, Generation Limits und related Pokemon gegen einen bereits stabilen Species-Writer isolieren. Offene Writer bleiben ausgeschaltet.

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

Feature- und Roadmap-Belege:

- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`

Wichtige Grenzen aus den Belegen:

- 047 klassifiziert Species Pools / Gen restrictions fuer die belegten Species-Pfade als P1-supported, aber nicht jede GUI-Suboption als einzeln gesmoked.
- 055 trennt `Bad Egg`, `<unknown>` und Unknown-/Fallback-Marker von echten Save-/Reload-Blockern.
- 060 stuft aktiviertes `Limit Pokemon`, Generation Limits, related Pokemon und premature-evolution bans als `wahrscheinlich supported, aber nicht einzeln getestet` ein.
- 061 priorisiert Global Species Pools / Generation Limits als ersten Smoke, ohne offene Writer aus 056-059 zu vermischen.

## Feature-IDs

Primaere Feature-IDs fuer 062:

| Feature-ID | Feature | Coverage-Status | 060-Status | 062-Einordnung |
|---|---|---|---|---|
| `FVX-GEN-001` | Limit Pokemon | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | primaerer Smoke-Scope |
| `FVX-GEN-002` | No Premature Evolutions | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | eigener Poolfilter-Slice |

Generation Limits und related-Pokemon-Scope werden in 062 unter `FVX-GEN-001` geplant, weil die Feature-Coverage-Matrix dafuer keine separaten Feature-IDs fuehrt.

Explizit nicht Teil dieses Smokes:

| Feature-ID | Feature | Grund |
|---|---|---|
| `FVX-GEN-003` | No Random Intro Mon | eigener Intro-/hardcoded-Pfad, nicht Teil Global Species Pool 062 |
| `FVX-GEN-004` | Race Mode | eigener Reproduzierbarkeits-/Settings-Pfad, nicht Teil Global Species Pool 062 |

## Minimaler Carrier

Der Poolfilter braucht fuer einen spaeteren Lauf eine kleine, stabile Schreib-/Reload-Oberflaeche. 062 plant deshalb einen einzelnen P1-stabilen Species-Writer als Carrier.

Bevorzugter Carrier:

| Feature-ID | Feature | Rolle in 062 | Beleg |
|---|---|---|---|
| `FVX-SST-002` | Starter Pokemon: Random completely | kleiner kontrollierbarer Species-Writer fuer Poolfilter-Smoke | 047 und Feature-Coverage: GUI-kompatibel / P1-supported |

Der Carrier wird in 062 nicht neu hochgestuft. Er dient nur als Schreib-/Reload-Oberflaeche fuer `FVX-GEN-001` und `FVX-GEN-002`.

Optional spaeter separat:

| Feature-ID | Feature | Rolle |
|---|---|---|
| `FVX-WILD-001` | Randomize Wild Pokemon | zweiter separater Smoke gegen Standard-/Fallback-Wild, ohne weitere Wild-Suboptionen |

## Geplante Smoke-Slices

062 definiert nur spaetere Smoke-Slices. Es fuehrt sie nicht aus.

| Slice | Aktive Hauptidee | Feature-IDs | Carrier | Zweck |
|---|---|---|---|---|
| A | Baseline Carrier ohne `Limit Pokemon` | `FVX-SST-002` | Starter | Carrier stabil halten und Vergleichsoberflaeche ohne Global-Poolfilter planen |
| B | `Limit Pokemon` mit Generation Limits | `FVX-GEN-001`, `FVX-SST-002` | Starter | Generation-Limit-Poolfilter gegen einen stabilen Writer isolieren |
| C | `Limit Pokemon` mit related Pokemon | `FVX-GEN-001`, `FVX-SST-002` | Starter | related-Pokemon-Scope gegen denselben stabilen Writer isolieren |
| D | `No Premature Evolutions` | `FVX-GEN-002`, `FVX-SST-002` | Starter | premature-evolution-Poolfilter getrennt von `Limit Pokemon` pruefbar machen |
| E | Optionaler Wild-Vergleich | `FVX-GEN-001` oder `FVX-GEN-002`, `FVX-WILD-001` | Wild Standard/Fallback | gleicher Poolfilter gegen Wild nur nach separater Freigabe, ohne weitere Wild-Suboptionen |

Settings werden spaeter normalisiert als Feature-IDs, Carrier, aktivierte Poolfilter und ausgeschlossene Writer dokumentiert. 062 traegt keine Laufwerte ein.

## Erlaubte Settings fuer spaetere Laeufe

Nur diese Settings duerfen fuer den spaeteren 062-Smoke aktiv sein:

- genau ein Carrier-Writer, bevorzugt `FVX-SST-002`.
- `FVX-GEN-001` fuer `Limit Pokemon`.
- Generation Limits als Subscope von `FVX-GEN-001`.
- related Pokemon als Subscope von `FVX-GEN-001`.
- `FVX-GEN-002` nur in einem eigenen Slice.

Alle anderen GUI-Optionen sollen auf unveraendert oder aus bleiben, soweit sie nicht technisch noetig sind, um den Carrier ueberhaupt auszufuehren.

## Explizit ausgeschlossene Writer

Diese Bereiche duerfen nicht in den 062-Smoke-Plan eingeschleust werden:

- MoveData Write / Move Power / Accuracy / PP / Type / Category / Name / Update Moves.
- Field Items, Shops, Pickup.
- Wild Held Items und Starter Held Items, soweit nicht explizit eigener spaeterer Test.
- Palette Randomization, Follow Types, Follow Evolutions, Shiny Palette.
- TypeChart / Type Effectiveness / Balanced / Inverse / Immunities.
- Graphics / Sprites / Repointing.
- Text / Menu / Description.
- Evolution-Writer wie Random Evolutions, Change Impossible Evolutions, Make Evolutions Easier, method/item/move/location changes.
- Trainer/Wild Level Modifier.
- Race Mode und No Random Intro Mon.

## Erwartete spaetere Metriken

Ein spaeterer, separat freigegebener Lauf soll folgende Kriterien dokumentieren. 062 traegt keine Werte ein.

| Kriterium | Erwartung |
|---|---|
| Save | `saveSuccessful=true` |
| Log | `logSuccessful=true`, `logNonEmpty=true` |
| Output | Output-ROM vorhanden, ohne Pfad oder ROM-Namen zu dokumentieren |
| Reload | Reload erfolgreich |
| Mismatches | relevanter Writer-Mismatch-Zaehler `0` |
| Stacktrace | `stacktrace=none` |
| Feature-Trace | aktive Feature-IDs und normalisierte Settings dokumentiert |
| Carrier | Carrier-Writer klar benannt |
| Marker | Marker aus 055 nur klassifizieren, nicht automatisch als neuen Fehler werten |
| Artefakte | keine ROMs, Logs, Output-ROMs, Builds, JARs, private Pfade, Hashes oder Secrets dokumentiert oder committed |

Der relevante Mismatch-Zaehler muss zum Carrier passen, z. B. ein Starter-Write-/Reload-Zaehler fuer `FVX-SST-002` oder ein Wild-Write-/Reload-Zaehler fuer `FVX-WILD-001`. Der genaue Zaehlername darf erst aus dem tatsaechlichen spaeteren Diagnosepfad uebernommen werden.

## Artefakt- und Datenschutzregeln

Falls ein spaeterer Lauf separat freigegeben wird:

- Lokale Outputs bleiben ignored, z. B. unter einem passenden `05_builds/randomizer-smoke/062_p1_global_species_pool_regression_smoke/`-Arbeitsordner.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs oder Tool-Binaries werden committed.
- Keine privaten Pfade, ROM-Namen, Hashes, Seeds mit privatem Kontext, Secrets, Tokens oder `.env`-Inhalte werden dokumentiert.
- Aus Logs werden nur freigegebene, sanitisiert zusammengefasste Metriken uebernommen.

## Stop-Regeln

Ein spaeterer 062-Umsetzungs- oder Laufblock stoppt, wenn:

1. Der Branch `main` ist oder der Worktree unerwartete fremde Aenderungen enthaelt.
2. Ein Lauf ROMs, Logs, Builds, Output-ROMs, Tool-Binaries, private Pfade, ROM-Namen, Hashes, Secrets, Tokens oder `.env`-Inhalte offenlegen wuerde.
3. Ein offener Writer aus 056-059 oder aus der Ausschlussliste aktiviert werden muesste.
4. Mehr als ein Writer aktiv waere und ein Mismatch nicht eindeutig dem Poolfilter oder Carrier zugeordnet werden koennte.
5. `FVX-GEN-001`-Suboptionen als P1-supported hochgestuft werden sollen, obwohl 060 sie nur als `wahrscheinlich supported, aber nicht einzeln getestet` einordnet.
6. Neue Diagnosewerte ohne tatsaechlichen, separat freigegebenen Lauf eingetragen werden muessten.
7. `Bad Egg`, `<unknown>` oder Unknown-/Fallback-Marker ohne 055-Kontext als neuer Fehler bewertet werden sollen.

## Ergebnis

062 legt den ersten konkreten Regression-Smoke-Plan fuer Global Species Pools / Generation Limits fest. Der Plan bleibt read-only: keine Ausfuehrung, keine neuen Werte, kein Fix. `FVX-GEN-001` und `FVX-GEN-002` werden gegen einen einzelnen stabilen Species-Carrier geplant, bevorzugt `FVX-SST-002`, waehrend offene Writer strikt ausgeschlossen bleiben.

Naechster sinnvoller Block nach diesem Plan:

- `analysis/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke` fuer Starter-Poolfilter wie random basic/two evolutions, Type Restrictions, No Legendaries und BST-Min/Max, getrennt von Starter-Held-Items.
