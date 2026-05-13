# Next Steps

## Aktueller Fokus

CFRU/DPE Global Species Pool Regression-Smoke-Plan ist read-only erstellt. Diagnose: `08_tests/randomizer/062_p1_global_species_pool_regression_smoke.md`.

## Priorisierte naechste Arbeitsbloecke

1. `analysis/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`
   - Starter-Poolfilter wie random basic/two evolutions, Type Restrictions, No Legendaries und BST-Min/Max getrennt von Starter-Held-Items pruefen.

2. `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`
   - BST-/Type-basierte Pooling-Suboptionen pruefen, ohne TypeChart oder MoveData-Write zu aktivieren.

3. `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`
   - Nur nach separater Freigabe: Type-Effectiveness-Table mit Fairy-Reload, unsupported/Stellar-Preserve und Terminator-/Kapazitaetskriterien absichern.

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
