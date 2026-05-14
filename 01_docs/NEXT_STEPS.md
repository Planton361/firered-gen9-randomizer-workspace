# Next Steps

## Aktueller Fokus

CFRU/DPE TypeChart Preserve Effectiveness Fix ist implementiert und sanitisiert dokumentiert. Ergebnisprotokoll: `08_tests/randomizer/066_type_chart_preserve_effectiveness_fix_diagnostics.md`.

## Priorisierte naechste Arbeitsbloecke

1. PRs fuer `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`
   - UPR-FVX-Fix und Workspace-Submodule-/Diagnoseupdate reviewen und mergen.

2. `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`
   - BST-/Type-basierte Pooling-Suboptionen pruefen, ohne TypeChart oder MoveData-Write zu aktivieren.

3. `analysis/upr-fvx-cfru-dpe-type-effectiveness-followup-smokes`
   - Optional: Balanced, Keep Identities, Inverse/Add Immunities und Update Type Effectiveness einzeln planen/testen.

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
