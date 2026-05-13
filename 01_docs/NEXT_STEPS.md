# Next Steps

## Aktueller Fokus

CFRU/DPE Base Stats + Types Scope-and-Write ist implementiert und dokumentiert in `08_tests/randomizer/051_base_stats_types_scope_write_diagnostics.md`.

## Priorisierte naechste Arbeitsbloecke

1. `compat/upr-fvx-cfru-dpe-abilities-hidden-ability-scope-and-write`
   - Ability1/2, Hidden Ability, Ability-Count bis `0xFE` und Ability-Logger-Fallbacks separat entblocken.

2. `analysis/upr-fvx-cfru-dpe-p1-item-data-and-bad-item-model`
   - Item-ID-Grenzen, Bad-/Key-Item-Filter und moderne Held-Item-Sicherheit fuer Encounter Held Items modellieren.

3. `analysis/upr-fvx-cfru-dpe-p1-type-log-placeholder-hygiene`
   - `Bad Egg`-/Unknown-Type-/`null`-Marker aus Placeholder- oder unsupported-Type-Species im BaseStats-/Traits-Log einordnen.

4. `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`
   - Move-Data-Write fuer `moves.total=992`, `BattleMove.split` und CFRU/DPE-Felder read-only modellieren.

5. `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`
   - Vorhandene Palette-Safety von echter Palette-/Graphics-Randomization trennen und Write-/Repointing-Risiken modellieren.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
