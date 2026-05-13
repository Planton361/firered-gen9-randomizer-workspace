# Next Steps

## Aktueller Fokus

CFRU/DPE Learnset GUI-Flow-Safety-Fix ist dokumentiert in `08_tests/randomizer/049_p1_learnset_gui_flow_safety_fix_diagnostics.md`.

## Priorisierte naechste Arbeitsbloecke

1. `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model`
   - Base Stats, Types, Ability Slots, Hidden Abilities und Encounter Held Items auf ein gemeinsames CFRU/DPE-Species-Datenmodell zurueckfuehren.

2. `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`
   - Move-Data-Write fuer `moves.total=992`, `BattleMove.split` und CFRU/DPE-Felder read-only modellieren.

3. `analysis/upr-fvx-cfru-dpe-p1-items-shops-field-model`
   - Field Items, Shops, Pickup und Item-ID-/Bad-Item-Scope fuer CFRU/DPE Gen9 inventarisieren.

4. `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`
   - Vorhandene Palette-Safety von echter Palette-/Graphics-Randomization trennen und Write-/Repointing-Risiken modellieren.

5. `analysis/upr-fvx-cfru-dpe-p1-special-tutor-text-menu-model`
   - Special-Tutors sowie Tutor-Text-/Menu-Rewrites getrennt vom normalen 152-Slot-Tutor-Scope modellieren.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
