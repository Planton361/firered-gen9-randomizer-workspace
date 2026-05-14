# 076 - P1 Trainer Type Diversity Blocker Diagnostics Plan

Datum: 2026-05-14

Branch: `analysis/upr-fvx-cfru-dpe-p1-trainer-type-diversity-blocker-diagnostics`

## Ziel

Dieses read-only Protokoll plant die konkrete Folge-Diagnose fuer den verbliebenen 070-Blocker:

- `FVX-FOE-009` Trainer Type Diversity / Type Themes
- Carrier: `FVX-FOE-001` Trainer Pokemon

Es fuehrt keine Tests aus, startet keine Randomizer-Laeufe und aendert keinen Code. Der Scope bleibt ausschliesslich beim Trainer-Type-Diversity-/Type-Themes-Pfad und wird nicht mit Wild, Evolution, TypeChart, MoveData, Palette, Items, Text/Menu, Graphics oder Level-Modifier vermischt.

## Belege

Primaere Belege:

- `055_type_log_placeholder_hygiene.md`
- `070_p1_similar_strength_same_type_regression_smoke_results.md`
- `071_p1_070_blocked_slices_followup_plan.md`
- `075_wild_filter_carrier_nullslot_fix_diagnostics.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`

## Blocker-Klassifikation

`FVX-FOE-009` bleibt ein echter Save-Blocker aus Diagnose 070.

| Merkmal | Befund aus 070 |
|---|---|
| Feature-ID | `FVX-FOE-009` Trainer Type Diversity / Type Themes |
| Carrier | `FVX-FOE-001` Trainer Pokemon |
| Save | `saveSuccessful=false` |
| Output/Reload | kein Output/Reload |
| Exception | `NullPointerException` |
| Filter | `filterViolations=112` nur bis Abbruch |
| Einordnung | echter Save-Blocker, kein P1-Support-Nachweis |

Dieser Blocker ist getrennt vom positiven Trainer Similar Strength Slice unter `FVX-FOE-001`. Trainer Similar Strength war in 070 mit Save/Log/Output/Reload true und `writeReloadTrainerPokemonMismatches=0` stabil, belegt aber nicht den Type-Diversity-/Type-Themes-Pfad.

## Hypothesen und Pruefspuren

Die spaetere Diagnose soll die folgenden Spuren getrennt pruefen:

1. Type-Diversity-Auswahl dereferenziert Null-Type-, Placeholder-, BST-zero- oder unsupported-Type-Species.
2. Der Trainer-Pool enthaelt Species, die im normalen Trainer-Species-Writer toleriert oder gefiltert werden, im Type-Diversity-Pfad aber nicht.
3. Trainer-Team-Type-Constraints erzeugen vor Save einen invaliden Teamzustand.
4. `filterViolations=112` ist ein Vor-Abbruch-Symptom und keine Endmetrik, solange Save/Output/Reload fehlen.
5. Bestehende Skip-/Scope-Regeln aus Ability-, BaseStats- oder Trainer-Scope fehlen im Type-Diversity-/Type-Themes-Pfad oder greifen dort nicht.

Die Diagnose soll klaeren, ob der Fehler in der Team-Type-Auswahl, in der Poolbildung, in der Anwendung der Constraints oder erst in der Save-Vorbereitung entsteht.

## Spaetere Diagnosemetriken

Ein spaeterer freigegebener Diagnose- oder Fixblock soll pro Lauf sanitisiert dokumentieren:

| Kategorie | Metrik |
|---|---|
| Save | `saveSuccessful` |
| Log | `logSuccessful`, `logNonEmpty` |
| Output | `outputRomExists`, ohne Pfad oder ROM-Namen |
| Reload | Reload erfolgreich |
| Reload-Vergleich | `writeReloadTrainerPokemonMismatches` |
| Filter | `filterViolations`, nur als Endmetrik nach Save/Reload |
| Scope-Hygiene | skipped/null/placeholder counts, nur sanitisiert |
| Log-Hygiene | `Bad Egg` / `<unknown>` nach 055 klassifizieren |
| Fehler | `exceptionClass` / `stacktraceClass` nur sanitisiert |
| Settings | aktive Feature-ID und normalisierte Settings |
| Carrier | Carrier-Writer klar benannt |

Keine spaeteren Protokolle duerfen private Pfade, ROM-Namen, Hashes, Log-Inhalte, Output-ROM-/Build-Pfade, Secrets, Tokens oder `.env`-Inhalte dokumentieren.

## Grenzen und Stop-Regeln

Die Folgearbeit stoppt, wenn ein offener Writer noetig wird oder versehentlich aktiv ist.

Ausgeschlossen bleiben:

- Trainer Level Modifier.
- Trainer Additional Pokemon.
- Better Movesets.
- Trainer Battle Style.
- Trainer Names / Class Names.
- TypeChart / TypeEffectiveness.
- MoveData Write / Update Moves.
- Items.
- Palette.
- Text / Menu / Graphics.
- Wild-Slices.
- Evolution-Slices.

Weitere Stop-Regeln:

- Stop, wenn private Pfade, ROM-Namen, Hashes, Loginhalte oder Output-/Build-Pfade fuer die Bewertung noetig waeren.
- Stop, wenn `filterViolations=112` oder andere Vor-Abbruch-Werte als Endzustandsmetrik gedeutet werden muessten.
- Stop, wenn `Bad Egg` oder `<unknown>` nicht eindeutig nach 055 klassifizierbar ist.
- Stop, wenn ein Ergebnis ohne Save/Log/Output/Reload-Stabilitaet als Support-Nachweis gewertet werden muesste.
- Keine Diagnosewerte erfinden.

## Folgeentscheidung

Empfohlen ist als naechster Arbeitsblock eine konkrete read-only Code-/Protokollanalyse fuer den Trainer-Type-Diversity-Pfad:

- Trainer-Randomizer- und Team-Type-Diversity-Codepfade identifizieren.
- Poolbildung gegen Null-/Placeholder-/BST-zero-/unsupported-Type-Species pruefen.
- Abgrenzen, warum Trainer Similar Strength im selben Carrier stabil ist, `FVX-FOE-009` aber beim Save blockiert.
- Nur wenn die Ursache danach klar ist, einen eng gegateten Fixbranch planen.

Kein Fixbranch soll Wild-, Evolution-, TypeChart-, MoveData-, Palette-, Item-, Text/Menu-, Graphics- oder Level-Modifier-Themen einschliessen.

## Ergebnis

`FVX-FOE-009` bleibt ein separater Trainer-Type-Diversity-Blocker. 076 dokumentiert nur den Diagnoseplan und fuehrt keine Ausfuehrung, keine Codeaenderung und keine Support-Hochstufung durch.
