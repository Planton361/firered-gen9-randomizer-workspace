# Next Steps

## Aktueller Fokus

CFRU/DPE Item-ID-, Itemnamen-, Bad-/Key-Item- und Encounter-Held-Item-Modell ist read-only dokumentiert in `08_tests/randomizer/053_p1_item_data_and_bad_item_model.md`.

## Priorisierte naechste Arbeitsbloecke

1. `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`
   - CFRU/DPE-gated ItemCount-/Itemnamen-Scope validieren und erweitern.
   - Moderne Bad-/Banned-Item-Filter fuer Key/System Items, TMs/HMs, Mail, Balls, Free-/Shiny-Space und Form-/Mega-/Z-/Plate-/Mask-/Tera-Sonderitems absichern.
   - Encounter Held Items in `gBaseStats` bei `item1/item2` (`0x0C`/`0x0E`) schreiben/reloaden.

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
