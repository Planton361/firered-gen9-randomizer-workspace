# Next Steps

## Aktueller Fokus

CFRU/DPE P1 Regression-Smoke-Plan ist read-only erstellt. Diagnose: `08_tests/randomizer/061_p1_regression_smoke_plan.md`.

## Priorisierte naechste Arbeitsbloecke

1. `analysis/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke`
   - Ersten spaeteren Regression-Smoke fuer `Limit Pokemon`, Generation Limits und related Pokemon vorbereiten oder ausfuehren, strikt ohne offene Writer.

2. `analysis/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`
   - Starter-Poolfilter wie random basic/two evolutions, Type Restrictions, No Legendaries und BST-Min/Max getrennt von Starter-Held-Items pruefen.

3. `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`
   - BST-/Type-basierte Pooling-Suboptionen pruefen, ohne TypeChart oder MoveData-Write zu aktivieren.

4. `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`
   - Nur nach separater Freigabe: Type-Effectiveness-Table mit Fairy-Reload, unsupported/Stellar-Preserve und Terminator-/Kapazitaetskriterien absichern.

5. `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
   - Nur nach separater Freigabe: eng gegateten MoveData-Writer mit Preserve-Policy und Reload-Diagnose umsetzen.

6. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

7. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
