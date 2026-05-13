# Next Steps

## Aktueller Fokus

CFRU/DPE Ability1/2 + Hidden Ability Scope-and-Write ist implementiert und dokumentiert in `08_tests/randomizer/052_abilities_hidden_ability_scope_write_diagnostics.md`.

## Priorisierte naechste Arbeitsbloecke

1. `analysis/upr-fvx-cfru-dpe-p1-item-data-and-bad-item-model`
   - Item-ID-Grenzen, Bad-/Key-Item-Filter und moderne Held-Item-Sicherheit fuer Encounter Held Items modellieren.

2. `analysis/upr-fvx-cfru-dpe-p1-type-log-placeholder-hygiene`
   - `Bad Egg`-/Unknown-Type-/`null`-Marker aus Placeholder- oder unsupported-Type-Species im BaseStats-/Traits-Log einordnen.

3. `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`
   - Move-Data-Write fuer `moves.total=992`, `BattleMove.split` und CFRU/DPE-Felder read-only modellieren.

4. `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`
   - Vorhandene Palette-Safety von echter Palette-/Graphics-Randomization trennen und Write-/Repointing-Risiken modellieren.

5. `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`
   - Type-Chart- und moderne Type-Interaktion getrennt von Pokemon-Type-Read/Write modellieren.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
