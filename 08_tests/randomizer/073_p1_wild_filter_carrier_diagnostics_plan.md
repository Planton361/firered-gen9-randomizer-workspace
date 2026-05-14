# 073 - P1 Wild Filter Carrier Diagnostics Plan

Datum: 2026-05-14

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-diagnostics`

## Ziel

Dieses Protokoll plant read-only die naechste Diagnose-/Harness-Entscheidung fuer den Wild-Filter-Carrier aus 072.

Scope:

- `FVX-WILD-011` Wild Similar Strength
- `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary
- gemeinsamer Carrier: `FVX-WILD-001` Standard/Fallback-Wild

Nicht Teil dieses Blocks:

- keine Codeaenderung
- kein Fix
- keine Randomizer-Laeufe
- keine Laufwerte oder Support-Hochstufung

## Ausgangsbefunde aus 070

| Slice | Carrier | Befund | Einordnung |
|---|---|---|---|
| `FVX-WILD-011` Wild Similar Strength | `FVX-WILD-001` | `saveSuccessful=false`, kein Output/Reload, `IllegalStateException` | echter Save-Blocker; Pruefspur BST-/Species-Pool-Filter plus Wild-Nullslot-/Placeholder-Scope |
| `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary | `FVX-WILD-001` | `saveSuccessful=false`, kein Output/Reload, `IllegalStateException`, `filterViolations=0` nur bis Abbruch | echter Save-Blocker; Pruefspur Species-Type-Filter plus Wild-Nullslot-/Placeholder-Scope |

## Praezisierung gegenueber 072

073 setzt 072 nicht als Diagnoseausfuehrung fort, sondern praezisiert die Entscheidung vor dem naechsten technischen Schritt:

1. Zuerst read-only Code-/Protokollanalyse planen.
2. Pruefen, ob vorhandene Dokumente und Codepfade ausreichen, um `FVX-WILD-001` Carrier-Scope von Similar-Strength- und Type-Restriction-Filter-Scope zu trennen.
3. Falls das nicht ausreicht, eine spaetere lokale Diagnose als separaten Freigabeschritt formulieren.
4. Keine Fixumsetzung, keine neuen Laufwerte und keine P1-Support-Hochstufung aus diesem Plan ableiten.

## Wild-Carrier-Pruefplan

### 1. Read-only Code-/Protokollanalyse

Zuerst sollen nur vorhandene Protokolle und Codepfade gelesen werden. ROMs, Logs, Output-ROMs, Builds, Tool-Binaries, private Pfade, Hashes und Loginhalte bleiben ausgeschlossen.

Zu trennen sind:

- `FVX-WILD-001` Standard/Fallback-Wild-Carrier: Area- und Encounter-Slot-Enumeration, tolerierte Null-/Placeholder-Eintraege und Schreibgrenzen.
- `FVX-WILD-011` Similar Strength: Species-Pool-Aufbau, BST-/BaseStats-Zugriff, leere oder ungueltige Ersatzpools und Verhalten bei Placeholder-/Special-Species.
- `FVX-WILD-004` Type Restrictions / Type Themes / Keep Primary: Species-Type-Felder, Type-Filter, unsupported-Type-Species und Verhalten bei Nullslot-/Placeholder-Species.
- Exception-Grenze: ob `IllegalStateException` bereits aus Carrier-Scope, Filter-Scope oder aus der Uebergabe zwischen beiden entsteht.

### 2. Harness-Plan nur bei separater Freigabe

Falls die read-only Analyse die Ursache nicht eindeutig trennt, soll ein eigener Diagnoseblock freigegeben werden. Dieser spaetere Block darf nur sanitisiert dokumentieren:

- boolesche Save-/Log-/Output-/Reload-Kriterien
- relevante Mismatch-Zaehler
- Area-/Encounter-/Placeholder-Zaehler, nur aggregiert und ohne Pfade
- Exception-Klasse und Stacktrace-Klasse, nur sanitisiert
- aktive Feature-IDs und normalisierte Settings

Die beiden Slices bleiben getrennt auswertbar, teilen aber denselben Carrier-Vergleich.

### 3. Entscheidungs-Gates

- Wenn die read-only Analyse eine klare Nullslot-/Placeholder- oder Filter-Scope-Ursache belegt, folgt ein kleiner Fixplan fuer Wild-Pool-/Placeholder-Scope.
- Wenn die Ursache nicht eindeutig ist, folgt ein separater Test-/Diagnosebranch fuer lokale Wild-Carrier-Diagnose.
- Kein Fixbranch wird gestartet, solange Carrier-Scope, BST-/Species-Pool-Filter und Species-Type-Filter nicht getrennt sind.

## Hypothesen / Pruefspuren

- Nullslot-/Placeholder-Wild-Entries werden in Filterpfaden nicht defensiv genug behandelt.
- Area-/Encounter-Slot-Scope enthaelt Eintraege, die der Standard/Fallback-Wild-Writer toleriert, die aber Similar Strength oder Type Restrictions brechen.
- Species-Pool/BST-Filter erzeugt leere oder ungueltige Pools.
- Species-Type-Filter trifft Placeholder-, Special- oder unsupported-Type-Species.
- `FVX-WILD-001` bleibt als Carrier belegt, aber diese Suboptionen verwenden strengere Vorauswahl und brauchen eigene Grenzen.

## Spaetere Diagnosemetriken

073 traegt keine neuen Werte ein. Fuer einen spaeter freigegebenen Diagnoseblock sind nur folgende sanitisierten Metriken vorgesehen:

| Metrik | Erwartete Dokumentation |
|---|---|
| `saveSuccessful` | boolean |
| `logSuccessful` | boolean |
| `outputRomExists` | boolean, ohne Pfad oder ROM-Name |
| `logNonEmpty` | boolean |
| Reload erfolgreich | boolean |
| `writeReloadWildPokemonMismatches` | Zaehler oder nicht anwendbar, ohne Output-Pfad |
| `filterViolations` | Zaehler, falls fuer den Slice sinnvoll |
| `areaCount` / `changedAreaCount` | nur aggregiert und sanitisiert |
| skipped/null/placeholder counts | nur aggregiert und sanitisiert |
| `exceptionClass` / `stacktraceClass` | nur sanitisiert, keine Pfade oder Loginhalte |
| `Bad Egg` / `<unknown>` | nach 055 klassifizieren |

## Grenzen

Ausgeschlossen bleiben:

- TypeChart / TypeEffectiveness
- MoveData Write / Update Moves
- Palette Randomization
- Items / Field Items / Shops / Pickup
- Encounter Held Items
- custom Day/Night-Wild
- Catch Em All / Minimum Catch Rate
- Wild oder Trainer Level Modifier
- Text / Menu / Graphics / Sprites
- weitere offene Writer

## Risiken / Stop-Regeln

- Stop, wenn statt Diagnose ein Fix erforderlich wuerde.
- Stop, wenn Randomizer-Laeufe ohne separate Freigabe erforderlich werden.
- Stop, wenn TypeChart, MoveData Write, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level Modifier oder Text/Menu/Graphics beruehrt werden.
- Stop, wenn private Pfade, ROM-Namen, Hashes, Logs oder Build-/Output-Pfade fuer die Auswertung gebraucht wuerden.
- Kein Fix ohne klare Ursache.

## Ergebnis dieses Blocks

073 dokumentiert nur den read-only Diagnose-/Harness-Plan fuer den Wild-Filter-Carrier. Es wurden keine neuen Diagnosewerte erhoben, keine Randomizer-Laeufe ausgefuehrt, keine Codeaenderungen vorgenommen und keine Support-Aussage hochgestuft.
