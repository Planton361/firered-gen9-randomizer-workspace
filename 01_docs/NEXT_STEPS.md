# Next Steps

## Aktueller Fokus

CFRU/DPE Field Items / Shops / Pickup ist read-only modelliert. Diagnose: `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`.

## Priorisierte naechste Arbeitsbloecke

1. `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`
   - Vorhandene Palette-Safety von echter Palette-/Graphics-Randomization trennen und Write-/Repointing-Risiken modellieren.

2. `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`
   - Type-Chart- und moderne Type-Interaktion getrennt von Pokemon-Type-Read/Write modellieren.

3. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

4. `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
   - Nur nach separater Freigabe: eng gegateten MoveData-Writer mit Preserve-Policy und Reload-Diagnose umsetzen.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
