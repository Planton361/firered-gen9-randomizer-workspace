# 072 - P1 Wild 070 Blockers Diagnostics Plan

Datum: 2026-05-14

Branch: `analysis/upr-fvx-cfru-dpe-p1-wild-070-blockers-diagnostics`

## Ziel

Dieses read-only Protokoll plant die Diagnose fuer die gemeinsamen Wild-Blocker aus Diagnose 070:

- `FVX-WILD-011` Wild Similar Strength.
- `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary.

Es fuehrt keine Tests aus, startet keine Randomizer-Laeufe und aendert keinen Code. Der Fokus liegt nur auf dem `FVX-WILD-001` Standard/Fallback-Wild-Carrier, Wild-Nullslot-/Placeholder-Scope, Species-Pool/BST-Filtern und Species-Type-Filtern.

## Belege

Primaere Belege:

- `055_type_log_placeholder_hygiene.md`
- `069_p1_similar_strength_same_type_regression_smoke.md`
- `070_p1_similar_strength_same_type_regression_smoke_results.md`
- `071_p1_070_blocked_slices_followup_plan.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`

## Grenzen

Folgende Bereiche bleiben ausgeschlossen und duerfen nicht in die Wild-Diagnose eingeschleust werden:

- TypeChart / TypeEffectiveness.
- MoveData Write.
- Palette.
- Items / Field Items / Shops / Pickup.
- Encounter Held Items.
- custom Day/Night-Wild.
- Catch Em All / Minimum Catch Rate.
- Level Modifier.
- Text / Menu / Graphics.
- Alle anderen offenen Writer.

072 ist nur ein Diagnoseplan. Es stuft `FVX-WILD-011` oder `FVX-WILD-004` nicht hoch und bestaetigt keine neuen GUI-Kombinationen.

## Wild-Blocker-Klassifikation

| Slice | Befund aus 070 | Klassifikation | Primaere Pruefspur |
|---|---|---|---|
| `FVX-WILD-011` Wild Similar Strength | Echter Save-Blocker im `FVX-WILD-001` Standard/Fallback-Wild-Carrier; kein Output/Reload; `IllegalStateException` | Wild-Carrier-/BST-Poolfilter-Blocker | BST-/Species-Pool-Filter plus Nullslot-/Placeholder-Scope |
| `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary | Echter Save-Blocker im gleichen Carrier; kein Output/Reload; `IllegalStateException`; `filterViolations=0` nur bis Abbruch | Wild-Carrier-/Typefilter-Blocker | Species-Type-Filter plus Nullslot-/Placeholder-Scope |

Beide Slices werden gemeinsam betrachtet, weil sie denselben `FVX-WILD-001` Carrier und dieselbe Exception-Klasse treffen. Die Diagnose muss dennoch BST-/Species-Pool-Filter und Species-Type-Filter getrennt auswertbar halten.

## Gemeinsame Hypothesen

Die spaetere Diagnose soll diese Ursachen getrennt pruefbar machen:

- Wild-Nullslots oder Placeholder-Wild-Entries werden im Filter-/Carrier-Pfad nicht defensiv genug behandelt.
- Area-/Encounter-Slot-Scope enthaelt Eintraege, die der Standard/Fallback-Wild-Writer allein toleriert, die aber bei Similar Strength oder Type Restrictions ungueltig werden.
- Species-Pool-/BST-Filter erzeugt leere, ungueltige oder nicht schreibbare Pools.
- Species-Type-Filter trifft Placeholder-, Special- oder unsupported-Type-Species.
- `FVX-WILD-001` ist als Standard/Fallback-Wild P1-supported, aber diese Suboptionen nutzen strengere Vorauswahl und brauchen eigene Scope-Grenzen.

## Pruefspuren

### Carrier- und Slot-Scope

Die Diagnose soll zuerst klaeren, ob der `IllegalStateException`-Abbruch aus dem Wild-Carrier-Scope selbst oder aus der Filtervorauswahl entsteht:

- Welche Standard/Fallback-Wild-Areas und Encounter-Slots werden vom Carrier betrachtet?
- Gibt es Nullslots, Placeholder-Species oder anderweitig nicht schreibbare Entries im zu filternden Scope?
- Sind solche Entries im reinen Standard/Fallback-Wild-Writer bereits defensiv toleriert, aber in Similar-Strength-/Type-Filterpfaden nicht?

### `FVX-WILD-011` Similar Strength

Die Diagnose soll fuer den BST-basierten Filter klaeren:

- Ob der Species-Pool fuer einzelne Encounter-Slots leer oder ungueltig wird.
- Ob BST-zero-, Placeholder- oder Special-Species als Vergleichs- oder Zielkandidaten in die Auswahl gelangen.
- Ob die Similar-Strength-Vorauswahl andere Poolgrenzen nutzt als der belegte Standard/Fallback-Wild-Writer.

### `FVX-WILD-004` Type Restrictions / Type Themes / Keep Primary

Die Diagnose soll fuer den Species-Type-Filter klaeren:

- Ob Null-/Placeholder-Species oder unsupported-Type-Species typisiert werden, bevor sie defensiv ausgeschlossen sind.
- Ob `filterViolations=0` aus 070 nur ein Vor-Abbruch-Zwischenstand ist oder spaeter nach Save/Reload als Endmetrik nutzbar wird.
- Ob der Type-Filter ausschliesslich Species-Type-Felder aus dem belegten Datenpfad nutzt und keinen TypeChart-Support voraussetzt.

## Spaetere Diagnosemetriken

Spaetere Diagnose- oder Testprotokolle sollen pro Slice mindestens folgende Werte sanitisiert dokumentieren, ohne neue Werte in diesem Plan zu erfinden:

| Kategorie | Metrik |
|---|---|
| Save | `saveSuccessful` |
| Log | `logSuccessful`, `logNonEmpty` |
| Output | `outputRomExists`, ohne Pfad oder ROM-Namen |
| Reload | Reload erfolgreich |
| Reload-Vergleich | `writeReloadWildPokemonMismatches` |
| Filter | `filterViolations`, nur als Endzustandsmetrik nach erfolgreichem Save/Reload |
| Scope | `areaCount` / `changedAreaCount`, nur sanitisiert und nur falls bereits verfuegbar oder spaeter freigegeben |
| Placeholder | skipped/null/placeholder counts, nur sanitisiert |
| Fehler | `exceptionClass` / `stacktraceClass`, nur sanitisiert |
| Log-Hygiene | `Bad Egg` / `<unknown>` nach 055 klassifizieren |
| Settings | aktive Feature-ID und normalisierte Settings |
| Carrier | `FVX-WILD-001` Standard/Fallback-Wild-Carrier klar benennen |

Keine spaeteren Protokolle duerfen private Pfade, ROM-Namen, Hashes, Loginhalte, Output-ROM-/Build-Pfade, Secrets, Tokens oder `.env`-Inhalte dokumentieren.

## Folgeentscheidung

Empfohlene Reihenfolge:

1. Erst read-only Diagnose/Harness-Plan oder Diagnose fuer den Wild-Filter-Carrier erstellen.
2. Danach, falls die Ursache klar ist, einen eng gegateten Wild-Pool-/Placeholder-Scope-Fix planen.
3. Keinen Fixbranch starten, solange die Ursache zwischen Carrier-Scope, BST-Poolfilter und Species-Type-Filter nicht getrennt ist.

Ein spaeterer Fixbranch muss klein bleiben und darf nicht gleichzeitig TypeChart, MoveData, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level Modifier, Text/Menu oder Graphics beruehren.

## Stop-Regeln

Spaetere Diagnose oder Fixplanung stoppt, wenn:

- ein offener Writer aktiviert werden muss.
- ein Randomizer-Lauf ohne separate Freigabe noetig waere.
- TypeChart, MoveData Write, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level Modifier, Text/Menu oder Graphics beruehrt werden.
- private Artefaktpfade, ROM-Namen, Hashes oder Loginhalte fuer die Bewertung noetig waeren.
- ein Ergebnis ohne Save/Log/Output/Reload-Stabilitaet als Support-Nachweis gedeutet werden muesste.
- `Bad Egg` oder `<unknown>` nicht eindeutig nach 055 eingeordnet werden kann.
- `writeReloadWildPokemonMismatches` ungleich `0` waere und trotzdem eine Hochstufung versucht wuerde.

## Ergebnis

Die Wild-070-Blocker bleiben ein gemeinsamer Diagnose-Scope:

- `FVX-WILD-011` prueft den BST-/Species-Pool-Filter.
- `FVX-WILD-004` prueft den Species-Type-Filter.
- Beide laufen ueber `FVX-WILD-001` und teilen den Verdacht auf Wild-Nullslot-/Placeholder-/Carrier-Grenzen.

Naechster sinnvoller Arbeitsblock ist ein separater read-only Diagnose-/Harness-Plan oder eine freigegebene read-only Diagnose fuer den Wild-Filter-Carrier. Ein Fixbranch folgt erst nach klarer Ursache.
