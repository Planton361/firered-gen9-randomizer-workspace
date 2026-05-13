# Next Steps

## Aktueller Fokus

UPR FVX GUI-Features werden als Requirements-/Coverage-Basis dokumentiert.

Neue Steuerungsdateien auf Branch `docs/fvx-feature-coverage-matrix`:

- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `01_docs/decisions/DEC-011-fvx-feature-coverage.md`

## Priorisierte naechste Arbeitsbloecke

1. `docs/fvx-feature-coverage-matrix`
   - PR reviewen und mergen, falls Feature-Zaehlung, Statusmodell und Roadmap-Pakete passen.

2. `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan`
   - Smoke-/Regression-Plan fuer priorisierte GUI-Suboptionen aus `01_docs/randomizer/fvx-feature-coverage.md` erstellen, ohne neue Randomizer-Laeufe im Planblock.

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
