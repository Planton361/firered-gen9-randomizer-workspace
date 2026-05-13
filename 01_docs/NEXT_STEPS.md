# Next Steps

## Aktueller Fokus

CFRU/DPE Learnset GUI-Kombinationsdiagnose ist dokumentiert in `08_tests/randomizer/048_p1_learnset_gui_combinations.md`.

## Priorisierte naechste Arbeitsbloecke

1. `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`
   - Logger-Fehler, Trainer-Movesets-Key-Luecke, Reorder-Damaging-Zweitwrite und TM/HM-/Tutor-Level-Up-Sanity nach Diagnose 048 entblocken.

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
