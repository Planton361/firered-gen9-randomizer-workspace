# Next Steps

## Aktueller Fokus

CFRU/DPE TypeEffectiveness-Folgesmokes sind einzeln lokal ausgefuehrt und sanitisiert dokumentiert. Ergebnisprotokoll: `08_tests/randomizer/068_type_effectiveness_followup_smoke_results.md`.

## Priorisierte naechste Arbeitsbloecke

1. PR fuer `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes`
   - Ergebnisse fuer Balanced, Keep Type Identities, Inverse, Add Random Immunities und Update Type Effectiveness reviewen und mergen.

2. `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`
   - BST-/Type-basierte Pooling-Suboptionen pruefen, ohne TypeChart oder MoveData-Write zu aktivieren.

3. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

4. `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
   - Nur nach separater Freigabe: eng gegateten MoveData-Writer mit Preserve-Policy und Reload-Diagnose umsetzen.

5. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

6. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
