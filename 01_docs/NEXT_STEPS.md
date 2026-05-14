# Next Steps

## Aktueller Fokus

CFRU/DPE Trainer Type Diversity Code Diagnosis ist read-only dokumentiert. Diagnose: `08_tests/randomizer/077_p1_trainer_type_diversity_code_diagnosis.md`.

## Priorisierte naechste Arbeitsbloecke

1. PRs fuer Wild-Filter-Carrier-Nullslot-Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Diagnose 075 und Submodule-Pin reviewen und mergen.

2. `FVX-FOE-009` Trainer Type Diversity / Type Themes eng gegatet fixen
   - Naechster Arbeitsblock: UPR-FVX-Fix fuer defensiven Trainer-Type-Diversity-Null-Type-Scope in `TrainerPokemonRandomizer`.
   - Wahrscheinliche Ursache aus 077: `updateUsedTypes(...)` schreibt `primaryType == null` in ein `EnumSet<Type>`.
   - Trainer Similar Strength unter `FVX-FOE-001` als Regression getrennt halten, weil dieser Pfad stabil war.
   - Weiter ohne Wild, Evolution, TypeChart, MoveData Write, Palette, Items, Text/Menu, Graphics, Level-Modifier oder andere offene Writer.

3. Weitere 070-Blocker getrennt fortsetzen
   - `FVX-TRAIT-018` Evolutions Similar Strength gegen Evolution-Reload-Mismatches, `Bad Egg` und BST-basierte Zielauswahl.
   - `FVX-TRAIT-019` Evolutions Same Typing gegen Evolution-Same-Typing-/Null-Scope.
   - Weiter ohne TypeChart, MoveData Write, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level-Modifier oder Text/Menu/Graphics.

4. Wild-Suboptionen konservativ halten
   - `FVX-WILD-011` und `FVX-WILD-004` sind im `FVX-WILD-001` Carrier-Fix-Smoke stabil.
   - Evolution Restrictions, Catch Em All, Minimum Catch Rate und Level-Balance bleiben getrennte Wild-Scope-Themen.

5. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

6. `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
   - Nur nach separater Freigabe: eng gegateten MoveData-Writer mit Preserve-Policy und Reload-Diagnose umsetzen.

7. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

8. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
