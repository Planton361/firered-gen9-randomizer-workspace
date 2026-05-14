# 071 - P1 070 Blocked Slices Follow-up Plan

Datum: 2026-05-14

Branch: `analysis/upr-fvx-cfru-dpe-p1-070-blocked-slices-followup-plan`

## Ziel

Dieses read-only Protokoll plant die Folgeanalyse fuer die in Diagnose 070 blockierten Similar Strength / Same Type / Type Themes Slices.

Es fuehrt keine Tests aus, startet keine Randomizer-Laeufe und aendert keinen Code. Die blockierten Slices werden getrennt eingeordnet, bevor ein Fixbranch freigegeben wird.

## Belege

Primaere Belege:

- `055_type_log_placeholder_hygiene.md`
- `060_p1_gui_suboptions_regression_matrix.md`
- `069_p1_similar_strength_same_type_regression_smoke.md`
- `070_p1_similar_strength_same_type_regression_smoke_results.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`

## Grenzen

Folgende Bereiche bleiben ausgeschlossen und duerfen nicht in die Folgeanalyse eingeschleust werden:

- TypeChart / TypeEffectiveness.
- MoveData Write.
- Palette.
- Items / Field Items / Shops / Pickup.
- Graphics / Sprites.
- Text / Menu.
- Level Modifier.
- Evolution-Methoden-Writer.
- Alle anderen offenen Writer.

071 ist nur ein Plan. Es stuft keine Feature-ID hoch und bestaetigt keine neuen GUI-Kombinationen.

## Blocker-Klassifikation

| Slice | Befund aus 070 | Klassifikation | Primaere Pruefspur |
|---|---|---|---|
| `FVX-WILD-011` Wild Similar Strength | Echter Save-Blocker, kein Output/Reload, `IllegalStateException` | Wild-Carrier-/Poolfilter-Blocker | Nullslot-/Placeholder-Scope, Species-Pool/BST-Filter, Standard/Fallback-Wild-Carrier-Grenze |
| `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary | Echter Save-Blocker, kein Output/Reload, `IllegalStateException`, `filterViolations=0` nur bis Abbruch | Wild-Carrier-/Typefilter-Blocker | Nullslot-/Placeholder-Scope, Species-Type-Filter, Standard/Fallback-Wild-Carrier-Grenze |
| `FVX-FOE-009` Trainer Type Diversity / Type Themes | Echter Save-Blocker, kein Output/Reload, `NullPointerException`, `filterViolations=112` nur bis Abbruch | Trainer-Type-Diversity-Blocker | Trainer-Type-Diversity-/Null-Type-Scope, Placeholder-, BST-zero- oder unsupported-Type-Species |
| `FVX-TRAIT-018` Evolutions Similar Strength | Save/Log/Output/Reload true, aber `writeReloadEvolutionMismatches=24` und `Bad Egg=true` | Evolution-Reload-/Pool-Hygiene-Blocker | BST-basierte Zielauswahl, Placeholder/Special-Species, Evolution-Reload-Mismatches, Bad-Egg-Log-Hygiene nach 055 |
| `FVX-TRAIT-019` Evolutions Same Typing | Echter Save-Blocker, kein Output/Reload, `NullPointerException` | Evolution-Typefilter-/Null-Scope-Blocker | Null-Evolution-Scope, Species-Type-Filter, Placeholder-/unsupported-Type-Species |

Trainer Similar Strength unter `FVX-FOE-001` ist nicht Teil dieses Blockerplans, weil 070 diesen Slice im Trainer-Species-Carrier-Smoke mit Save/Log/Output/Reload true und `writeReloadTrainerPokemonMismatches=0` bestaetigt hat.

## Pruefspuren je Blocker

### `FVX-WILD-011` Wild Similar Strength

Spaetere read-only Diagnose soll klaeren:

- Ob der `IllegalStateException`-Abbruch aus Wild-Nullslots, Placeholder-Species oder einem Standard/Fallback-Wild-Carrier-Scope entsteht.
- Ob der BST-basierte Similar-Strength-Pool Sonder-Species, BST-zero-Species oder nicht poolfaehige Species als Kandidaten zulaesst.
- Ob der Wild-Carrier bereits vor dem Save einen Zustand erzeugt, der nicht geschrieben werden darf.

Erst nach dieser Diagnose ist ein eng gegateter Fixplan sinnvoll.

### `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary

Spaetere read-only Diagnose soll klaeren:

- Ob derselbe Wild-Carrier-Blocker wie bei `FVX-WILD-011` greift.
- Ob der Species-Type-Filter Null-/Placeholder-Species oder unsupported-Type-Species nicht defensiv genug behandelt.
- Ob `filterViolations=0` aus 070 nur ein unvollstaendiger Vor-Abbruch-Befund bleibt oder spaeter nach erfolgreichem Save/Reload als echte Endmetrik nutzbar ist.

`FVX-WILD-004` sollte gemeinsam mit `FVX-WILD-011` modelliert werden, weil beide denselben `FVX-WILD-001` Carrier und dieselbe Exception-Klasse treffen. Ein spaeterer Fix muss trotzdem getrennt nach BST-Filter und Type-Filter begruendet werden.

### `FVX-FOE-009` Trainer Type Diversity / Type Themes

Spaetere read-only Diagnose soll klaeren:

- Ob Type-Diversity Team-Constraints gegen Null-Type-, Placeholder-, BST-zero- oder unsupported-Type-Species laufen.
- Ob die `filterViolations=112` aus 070 ein Vor-Abbruch-Symptom der Diversity-Logik oder ein Folgeeffekt eines bereits invaliden Trainer-Team-Zustands sind.
- Ob das Problem im Type-Diversity-Constraint, in der Type-Themes-/Team-Poolbildung oder in der Save-Phase liegt.

Dieser Blocker bleibt getrennt von Better Movesets, Trainer Held Items, Additional Pokemon, Battle Style, Trainer Names/Class Names und Trainer Level Modifier.

### `FVX-TRAIT-018` Evolutions Similar Strength

Spaetere read-only Diagnose soll klaeren:

- Ob die BST-basierte Evolutionsziel-Auswahl Placeholder/Special-Species oder nicht reload-stabile Ziele waehlt.
- Warum Save/Log/Output/Reload zwar funktionieren, der Reload-Vergleich aber `writeReloadEvolutionMismatches=24` meldet.
- Ob der `Bad Egg`-Marker aus der Zielauswahl, aus Logger-/Placeholder-Hygiene oder aus einem echten Write/Reload-Fehler folgt.

`Bad Egg` kann hier nicht als reine 055-Log-Hygiene freigegeben werden, solange der relevante Mismatch-Zaehler ungleich `0` ist.

### `FVX-TRAIT-019` Evolutions Same Typing

Spaetere read-only Diagnose soll klaeren:

- Ob die Same-Typing-Filterung Null-Evolutionen, Placeholder-Species oder unsupported-Type-Species dereferenziert.
- Ob der `NullPointerException`-Abbruch vor der Save-Phase in der Poolbildung oder in der Vorbereitung des Evolution-Writes entsteht.
- Ob die Type-Felder aus 051 fuer diese Evolutions-Suboption ausreichen oder ob zusaetzliche defensive Scope-Grenzen noetig sind.

Dieser Blocker bleibt getrennt von Evolution-Methoden-Writern wie Change Impossible Evolutions, Make Evolutions Easier oder Remove Time-Based Evolutions.

## Priorisierte Reihenfolge

1. Wild Similar Strength + Wild Type Restrictions gemeinsam als read-only Diagnoseplan, weil beide `FVX-WILD-001` Carrier und `IllegalStateException` teilen.
2. `FVX-FOE-009` Trainer Type Diversity separat.
3. `FVX-TRAIT-018` Evolutions Similar Strength separat wegen Reload-Mismatches und `Bad Egg`.
4. `FVX-TRAIT-019` Evolutions Same Typing separat wegen Save-Abbruch und Null-/Type-Scope-Verdacht.

Diese Reihenfolge ist absichtlich nicht als Fixreihenfolge zu verstehen. Sie priorisiert nur die naechste read-only Diagnose, damit spaetere Fixbranches klein und getrennt bleiben.

## Spaetere Diagnosemetriken

Spaetere Diagnose- oder Testprotokolle sollen pro Slice mindestens folgende Werte sanitisiert dokumentieren:

| Kategorie | Metrik |
|---|---|
| Save | `saveSuccessful` |
| Log | `logSuccessful`, `logNonEmpty` |
| Output | `outputRomExists`, ohne Pfad oder ROM-Namen |
| Reload | Reload erfolgreich |
| Reload-Vergleich | relevanter Mismatch-Zaehler fuer Wild-, Trainer- oder Evolution-Species |
| Filter | `filterViolations`, nur wenn die Endzustandsmetrik nach Save/Reload sinnvoll ist |
| Log-Hygiene | `Bad Egg` / `<unknown>` nach 055 klassifizieren |
| Fehler | `exceptionClass` / `stacktraceClass` nur sanitisiert |
| Settings | aktive Feature-ID und normalisierte Settings |
| Carrier | Carrier-Writer klar benannt |

Keine spaeteren Protokolle duerfen private Pfade, ROM-Namen, Hashes, Log-Inhalte, Output-ROM-/Build-Pfade, Secrets, Tokens oder `.env`-Inhalte dokumentieren.

## Stop-Regeln

Spaetere Diagnose oder Fixplanung stoppt, wenn:

- ein offener Writer aktiviert werden muss.
- TypeChart, MoveData, Palette, Items, Graphics, Text/Menu, Level Modifier oder Evolution-Methoden-Writer beruehrt werden.
- private Artefaktpfade, ROM-Namen, Hashes oder Loginhalte fuer die Bewertung noetig waeren.
- ein Ergebnis ohne Save/Log/Output/Reload-Stabilitaet als Support-Nachweis gedeutet werden muesste.
- `Bad Egg` oder `<unknown>` nicht eindeutig nach 055 eingeordnet werden kann.
- Mismatch-Zaehler ungleich `0` sind und trotzdem eine Hochstufung versucht wuerde.

## Ergebnis

Die blockierten 070-Slices bleiben getrennte Folgeprobleme:

- Wild Similar Strength und Wild Type Restrictions teilen wahrscheinlich einen Wild-Carrier-/Placeholder-Scope.
- `FVX-FOE-009` ist ein eigener Trainer-Type-Diversity-Scope.
- `FVX-TRAIT-018` ist ein eigener Evolution-Reload-/Bad-Egg-Scope.
- `FVX-TRAIT-019` ist ein eigener Evolution-Same-Typing-/Null-Scope.

Naechster sinnvoller Arbeitsblock ist ein separater read-only Diagnoseplan oder Diagnosebranch fuer die Wild-Slices. Kein Fixbranch sollte alle fuenf Blocker zusammenfassen.
