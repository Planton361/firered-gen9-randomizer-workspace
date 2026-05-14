# Next Steps

## Aktueller Fokus

CFRU/DPE Folgeanalyse-Plan fuer die in 070 blockierten Similar Strength / Same Type / Type Themes Slices ist read-only dokumentiert. Planprotokoll: `08_tests/randomizer/071_p1_070_blocked_slices_followup_plan.md`.

## Priorisierte naechste Arbeitsbloecke

1. PR fuer `analysis/upr-fvx-cfru-dpe-p1-070-blocked-slices-followup-plan`
   - Read-only Folgeanalyse-Plan 071 reviewen und mergen.

2. Naechster read-only Diagnoseblock fuer Wild 070-Blocker
   - Wild Similar Strength und Wild Type Restrictions gemeinsam gegen Wild-Nullslot-/Placeholder-Scope, Species-Pool/BST-Filter, Species-Type-Filter und Standard/Fallback-Wild-Carrier-Grenzen pruefen.
   - Weiter ohne TypeChart, MoveData Write, Palette, Items, Graphics, Text/Menu, Level-Modifier oder Evolution-Methoden-Writer.

3. Danach getrennte Diagnosebloecke fuer die restlichen 070-Blocker
   - `FVX-FOE-009` gegen Trainer-Type-Diversity-/Null-Type-Scope.
   - `FVX-TRAIT-018` gegen Evolution-Reload-Mismatches, `Bad Egg` und BST-basierte Zielauswahl.
   - `FVX-TRAIT-019` gegen Evolution-Same-Typing-/Null-Scope.

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
