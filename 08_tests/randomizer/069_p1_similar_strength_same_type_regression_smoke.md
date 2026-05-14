# 069 - P1 Similar Strength / Same Type Regression-Smoke-Plan

## Ziel

Dieses read-only Protokoll plant spaetere Regression-Smokes fuer BST- und Type-basierte Poolfilter im CFRU/DPE Gen9-BPRE-Scope:

- Similar Strength
- Same Type / Same Typing
- Type Themes
- Type Restrictions

Es fuehrt keine Tests aus, startet keine Randomizer-Laeufe und aendert keinen Code.

Der Plan nutzt nur bereits belegte Datenpfade:

- Species-Pools und interne SpeciesSet-Identitaet aus den belegten Species-Writern.
- BaseStats/BST aus Diagnose 051.
- Species-Type-Felder aus Diagnose 051.

Same Type, Type Themes und Type Restrictions nutzen Species-Type-Felder aus `gBaseStats`. Sie beweisen keinen TypeChart- oder TypeEffectiveness-Support. TypeChart-Folgesmokes sind separat in 068 dokumentiert und bleiben hier ausdruecklich ausserhalb des Scopes.

## Belege

Primaere Belege:

- `047_fvx_gui_options_compatibility_matrix.md`
- `051_base_stats_types_scope_write_diagnostics.md`
- `055_type_log_placeholder_hygiene.md`
- `060_p1_gui_suboptions_regression_matrix.md`
- `061_p1_regression_smoke_plan.md`
- `064_p1_global_species_pool_regression_smoke_results.md`
- `065_p1_starters_suboptions_regression_smoke_results.md`
- `068_type_effectiveness_followup_smoke_results.md`

Feature-Coverage-Belege:

- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`

## Datenpfade

| Datenpfad | Beleg | Nutzung im spaeteren Smoke |
|---|---|---|
| Species-Pool / SpeciesSet-Identitaet | 047, 060, belegte Species-Writer | Replacement-Pool und Reload-Vergleich der Carrier-Writer |
| BaseStats / BST | 051 | Similar-Strength-Filter und ggf. BST-nahe Validierung |
| Species-Type-Felder | 051 | Same Type, Type Themes, Type Restrictions und Type Diversity |
| Log-Hygiene-Marker | 055 | Klassifikation von `Bad Egg`, `<unknown>` und Unknown-/Fallback-Markern |
| TypeChart / TypeEffectiveness | 068 | Nur Abgrenzungsbeleg; nicht Teil von 069 |

## Geplante Smoke-Slices

| Slice | Feature-ID | Carrier | Ziel | Abgrenzung |
|---|---|---|---|---|
| Wild Similar Strength | `FVX-WILD-011` | `FVX-WILD-001` Standard/Fallback Wild Species Writer | BST-basierter Wild-Poolfilter gegen BaseStats/BST aus 051 | Kein Wild-Level-Modifier, kein Catch Em All, keine Wild held items, keine custom Day/Night-Wilddaten |
| Wild Type Restrictions / Type Themes / Keep Primary | `FVX-WILD-004` | `FVX-WILD-001` Standard/Fallback Wild Species Writer | Wild-Type-Poolfilter ueber Species-Type-Felder aus 051 | Kein TypeChart-/TypeEffectiveness-Nachweis |
| Trainer Similar Strength | Suboption unter `FVX-FOE-001`, sofern keine eigene Feature-ID existiert | Trainer-Species-Writer | Trainer-Species-Poolfilter via BST | Keine Better Movesets, keine Held Items, keine Trainer-Level-Modifier, keine Additional Pokemon |
| Trainer Type Diversity / Type Themes | `FVX-FOE-009` | `FVX-FOE-001` Trainer Pokemon | Trainer-Team-Type-Constraints ueber Species-Type-Felder aus 051 | Kein Trainer-Level-/Additional-Pokemon-/Battle-Style-/Text-Scope |
| Evolutions Similar Strength | `FVX-TRAIT-018` | `FVX-TRAIT-016` Evolution-Species-Writer | Evolutionsziel-Pool via BST | Keine Evolution-Methoden-, Item-, Move- oder Level-Rewrites |
| Evolutions Same Typing | `FVX-TRAIT-019` | `FVX-TRAIT-016` Evolution-Species-Writer | Evolutionsziel-Pool via Species-Type-Felder | Kein TypeChart-/TypeEffectiveness-Nachweis |

Trainer Similar Strength wird konservativ als Suboption unter `FVX-FOE-001` gefuehrt, solange die Feature-Coverage-Matrix keine eigene dedizierte Feature-ID fuer diese Trainer-Suboption fuehrt. `FVX-FOE-009` bleibt der dedizierte Eintrag fuer Force Diverse Types / Type-Diversity-nahe Trainer-Type-Constraints.

## Geeignete Carrier

Primaere Carrier:

- `FVX-WILD-001` Standard/Fallback Wild fuer Wild Similar Strength und Wild Type Restrictions.
- `FVX-FOE-001` Trainer Pokemon fuer Trainer Similar Strength, Type Themes und Type Diversity.
- `FVX-TRAIT-016` Evolution Randomization fuer Similar Strength und Same Typing bei Evolutions.

Nicht-primaere Carrier:

- Starter: 064/065 belegen bereits Global-Pool, Type Restrictions und BST-Min/Max im Starter-Species-Writer-Scope. Das ist ein Vergleichsbeleg, aber kein Ersatz fuer Wild-/Trainer-/Evolution-Smokes.
- `FVX-SST-012` Static Pokemon Random similar strength: optionaler Referenzpunkt, aber nicht primaerer 069-Scope.
- TM/Tutor Prefer Same Type: fuehrt in Move-/Compatibility-Pfade und ist kein reiner Species-Writer-Scope. TM/Tutor-Same-Type bleibt fuer separate Moveset-/Compatibility-Smokes.

## Explizit Ausgeschlossen

Nicht in spaetere 069-Smokes einschleusen:

- TypeChart / TypeEffectiveness.
- MoveData Write / Update Moves.
- Field Items / Shops / Pickup.
- Encounter Held Items.
- Palette Randomization / Follow Types / Follow Evolutions / Shiny Palette.
- Graphics / Sprites / Repointing.
- Text / Menu / Description.
- Trainer/Wild Level Modifier.
- Evolution-Methoden-Writer.
- Starter Held Items.
- Race Mode / Intro Mon.
- Better Movesets.
- Trainer Additional Pokemon.
- Trainer Battle Style.
- Trainer Names/Class Names.
- Catch Em All.
- Minimum Catch Rate.
- Wild held items.
- custom Day/Night-Wild.

## Erwartete Spaetere Metriken

Spaetere Testprotokolle sollen pro Slice mindestens folgende Kriterien sanitisiert dokumentieren, ohne Werte aus lokalen Pfaden oder Artefakten offenzulegen:

| Kriterium | Erwartung |
|---|---|
| Save | `saveSuccessful=true` |
| Log | `logSuccessful=true`, `logNonEmpty=true` |
| Output | `outputRomExists=true`, ohne Pfad oder ROM-Namen |
| Reload | Reload erfolgreich |
| Mismatches | relevanter Writer-Mismatch-Zaehler `0` |
| Filter | `filterViolations=0`, wo sinnvoll |
| Log-Hygiene | `Bad Egg=false` oder nach 055 als Marker klassifiziert |
| Log-Hygiene | `<unknown>=false` oder nach 055 als Marker klassifiziert |
| Fehler | `stacktrace=none` |
| Traceability | aktive Feature-IDs dokumentiert |
| Settings | normalisierte Settings dokumentiert |
| Carrier | Carrier-Writer klar benannt |
| Artefakte | keine ROMs, Logs, Output-ROMs, Builds, JARs, private Pfade, Hashes oder Secrets dokumentiert oder committed |

Pfadspezifische Mismatch-Zaehler sollen den jeweiligen Carrier eindeutig benennen, z. B. Wild-Species-, Trainer-Species- oder Evolution-Species-Write/Reload-Mismatches. Falls ein Harness einen anders benannten aequivalenten Zaehler nutzt, muss das Ergebnisprotokoll die Bedeutung kurz erklaeren.

## Stop-Regeln

Spaetere Ausfuehrung sofort stoppen und keinen Erfolgsstatus dokumentieren, wenn:

- ein offener Writer aktiviert werden muss oder versehentlich aktiv ist.
- ein Slice TypeChart, MoveData, Palette, Items, Text oder Graphics beruehrt.
- Save, Log, Output oder Reload fehlschlagen.
- der relevante Mismatch-Zaehler ungleich `0` ist.
- `filterViolations > 0`.
- `Bad Egg` oder `<unknown>` nicht sauber als 055-Logmarker klassifizierbar ist.
- ein Stacktrace entsteht.
- private Artefaktpfade, ROM-Namen, Hashes oder Loginhalte fuer die Auswertung noetig waeren.

## Einordnung

069 ist nur ein Plan. Es stuft keine Feature-ID hoch und bestaetigt keine neuen GUI-Kombinationen.

Der naechste sinnvolle Arbeitsblock ist ein separater Testbranch, der die sechs geplanten Slices einzeln ausfuehrt und sanitisiert dokumentiert. Dabei bleibt jeder Slice eng an genau einen Carrier und genau einen BST-/Type-basierten Filter gebunden, damit offene Writer nicht verdeckt aktiviert werden.
