# Next Steps

## Aktueller Fokus

CFRU/DPE Type-Chart und moderne Type-Interaktion sind read-only modelliert. Diagnose: `08_tests/randomizer/059_p1_type_chart_model.md`.

## Priorisierte naechste Arbeitsbloecke

1. `analysis/upr-fvx-cfru-dpe-p1-gui-suboptions-regression-matrix`
   - GUI-Suboptionen nach den read-only Modellen 055-059 regressionsorientiert konsolidieren.

2. `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`
   - Nur nach separater Freigabe: Type-Effectiveness-Table mit Fairy-Reload, unsupported/Stellar-Preserve und Terminator-/Kapazitaetskriterien absichern.

3. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

4. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

5. `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
   - Nur nach separater Freigabe: eng gegateten MoveData-Writer mit Preserve-Policy und Reload-Diagnose umsetzen.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
