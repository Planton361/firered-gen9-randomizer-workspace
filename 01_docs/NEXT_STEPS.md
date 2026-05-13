# Next Steps

## Aktueller Fokus

CFRU/DPE Base Stats, Types, Abilities und Encounter Held Items Modell ist dokumentiert in `08_tests/randomizer/050_p1_base_stats_types_abilities_model.md`.

## Priorisierte naechste Arbeitsbloecke

1. `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write`
   - Base Stats und Fairy-Type-Mapping eng gegatet schreiben/reloaden; Stellar zunaechst preserve/skip.

2. `compat/upr-fvx-cfru-dpe-abilities-hidden-ability-scope-and-write`
   - Ability1/2, Hidden Ability, Ability-Count bis `0xFE` und Ability-Logger-Fallbacks separat entblocken.

3. `analysis/upr-fvx-cfru-dpe-p1-item-data-and-bad-item-model`
   - Item-ID-Grenzen, Bad-/Key-Item-Filter und moderne Held-Item-Sicherheit fuer Encounter Held Items modellieren.

4. `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`
   - Move-Data-Write fuer `moves.total=992`, `BattleMove.split` und CFRU/DPE-Felder read-only modellieren.

5. `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`
   - Vorhandene Palette-Safety von echter Palette-/Graphics-Randomization trennen und Write-/Repointing-Risiken modellieren.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
