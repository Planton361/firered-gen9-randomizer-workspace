# Next Steps

## Aktueller Fokus

CFRU/DPE Similar Strength / Same Type Regression-Smoke-Plan ist read-only dokumentiert. Planprotokoll: `08_tests/randomizer/069_p1_similar_strength_same_type_regression_smoke.md`.

## Priorisierte naechste Arbeitsbloecke

1. PR fuer `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`
   - Read-only Plan fuer BST-/Type-basierte Poolfilter reviewen und mergen.

2. `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`
   - Die in 069 geplanten Slices einzeln ausfuehren: Wild Similar Strength, Wild Type Restrictions / Type Themes, Trainer Similar Strength, Trainer Type Diversity / Type Themes, Evolutions Similar Strength und Evolutions Same Typing.
   - Weiter ohne TypeChart, MoveData Write, Palette, Items, Graphics, Text/Menu, Level-Modifier oder Evolution-Methoden-Writer.

3. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

4. `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
   - Nur nach separater Freigabe: eng gegateten MoveData-Writer mit Preserve-Policy und Reload-Diagnose umsetzen.

5. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

6. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
