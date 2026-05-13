# Next Steps

## Aktueller Fokus

FVX-GUI-Options-Kompatibilitaetsmatrix fuer den getesteten CFRU/DPE Gen9-BPRE-Stand ist dokumentiert in `08_tests/randomizer/047_fvx_gui_options_compatibility_matrix.md`.

## Priorisierte naechste Arbeitsbloecke

1. `compat/upr-fvx-cfru-dpe-learnset-write-repointing`
   - Nur fortsetzen, wenn Phase 2 genug reservierbaren FreeSpace fuer den actual Learnset-Blob-Bedarf nachweist.

2. `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model`
   - Base Stats, Types, Ability Slots, Hidden Abilities und Encounter Held Items auf ein gemeinsames CFRU/DPE-Species-Datenmodell zurueckfuehren.

3. `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`
   - Move-Data-Write fuer `moves.total=992`, `BattleMove.split` und CFRU/DPE-Felder read-only modellieren.

4. `analysis/upr-fvx-cfru-dpe-p1-items-shops-field-model`
   - Field Items, Shops, Pickup und Item-ID-/Bad-Item-Scope fuer CFRU/DPE Gen9 inventarisieren.

5. `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`
   - Vorhandene Palette-Safety von echter Palette-/Graphics-Randomization trennen und Write-/Repointing-Risiken modellieren.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
