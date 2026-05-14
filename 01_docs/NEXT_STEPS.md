# Next Steps

## Aktueller Fokus

CFRU/DPE Wild-Filter-Carrier-Nullslot-Fix ist umgesetzt und sanitisiert dokumentiert. Diagnoseprotokoll: `08_tests/randomizer/075_wild_filter_carrier_nullslot_fix_diagnostics.md`.

## Priorisierte naechste Arbeitsbloecke

1. PRs fuer Wild-Filter-Carrier-Nullslot-Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Diagnose 075 und Submodule-Pin reviewen und mergen.

2. Nach Merge: restliche 070-Blocker getrennt fortsetzen
   - `FVX-FOE-009` Trainer Type Diversity / Type Themes gegen Trainer-Type-Diversity-/Null-Type-Scope.
   - `FVX-TRAIT-018` Evolutions Similar Strength gegen Evolution-Reload-Mismatches, `Bad Egg` und BST-basierte Zielauswahl.
   - `FVX-TRAIT-019` Evolutions Same Typing gegen Evolution-Same-Typing-/Null-Scope.
   - Weiter ohne TypeChart, MoveData Write, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level-Modifier oder Text/Menu/Graphics.

3. Wild-Suboptionen konservativ halten
   - `FVX-WILD-011` und `FVX-WILD-004` sind im `FVX-WILD-001` Carrier-Fix-Smoke stabil.
   - Evolution Restrictions, Catch Em All, Minimum Catch Rate und Level-Balance bleiben getrennte Wild-Scope-Themen.

4. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

5. `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
   - Nur nach separater Freigabe: eng gegateten MoveData-Writer mit Preserve-Policy und Reload-Diagnose umsetzen.

6. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

7. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
