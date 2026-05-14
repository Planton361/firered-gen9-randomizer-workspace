# Next Steps

## Aktueller Fokus

CFRU/DPE Similar Strength / Same Type Regression-Smoke-Ergebnisse sind sanitisiert dokumentiert. Ergebnisprotokoll: `08_tests/randomizer/070_p1_similar_strength_same_type_regression_smoke_results.md`.

## Priorisierte naechste Arbeitsbloecke

1. PR fuer `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`
   - Ergebnisprotokoll 070 reviewen und mergen.

2. Read-only Folgeanalyse fuer blockierte 070-Slices
   - Wild Similar Strength und Wild Type Restrictions gegen Wild-Nullslot-/Placeholder-Scope pruefen.
   - `FVX-FOE-009` gegen Trainer-Type-Diversity-/Null-Type-Scope pruefen.
   - `FVX-TRAIT-018/019` gegen Evolution-Reload-Mismatches, `Bad Egg` und Null-Evolution-Scope pruefen.
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
