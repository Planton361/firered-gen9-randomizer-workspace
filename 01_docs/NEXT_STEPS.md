# Next Steps

## Aktueller Fokus

CFRU/DPE Move-Data-Write ist read-only modelliert. Diagnose: `08_tests/randomizer/056_p1_move_data_write_model.md`.

## Priorisierte naechste Arbeitsbloecke

1. `analysis/upr-fvx-cfru-dpe-p1-field-items-shops-pickup-model`
   - Field Items, Shops, Pickup und allgemeine Item-Randomization getrennt von Encounter Held Items modellieren.

2. `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`
   - Vorhandene Palette-Safety von echter Palette-/Graphics-Randomization trennen und Write-/Repointing-Risiken modellieren.

3. `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`
   - Type-Chart- und moderne Type-Interaktion getrennt von Pokemon-Type-Read/Write modellieren.

4. `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
   - Nur nach separater Freigabe: eng gegateten MoveData-Writer mit Preserve-Policy und Reload-Diagnose umsetzen.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
