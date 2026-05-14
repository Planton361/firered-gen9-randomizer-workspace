# Next Steps

## Aktueller Fokus

CFRU/DPE Wild-Filter-Carrier-Diagnose-/Harness-Plan ist read-only dokumentiert. Planprotokoll: `08_tests/randomizer/073_p1_wild_filter_carrier_diagnostics_plan.md`.

## Priorisierte naechste Arbeitsbloecke

1. PR fuer `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-diagnostics`
   - Read-only Wild-Filter-Carrier-Diagnoseplan 073 reviewen und mergen.

2. Read-only Code-/Protokollanalyse fuer den Wild-Filter-Carrier
   - `FVX-WILD-011` und `FVX-WILD-004` gemeinsam gegen Carrier-Scope, Wild-Nullslot-/Placeholder-Scope, Area-/Encounter-Slot-Scope, Species-Pool/BST-Filter und Species-Type-Filter trennen.
   - Pruefen, ob vorhandene Dokumente und Codepfade reichen, bevor lokale Diagnose-Laeufe freigegeben werden.
   - Weiter ohne TypeChart, MoveData Write, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level-Modifier oder Text/Menu/Graphics.

3. Falls read-only nicht ausreicht: separater lokaler Wild-Carrier-Diagnosebranch
   - Nur mit expliziter Freigabe, sanitisierten Metriken und ohne Fixumsetzung.
   - Keine ROM-/Log-/Output-/Build-Pfade, ROM-Namen, Hashes oder Loginhalte dokumentieren.

4. Danach ggf. eng gegateter Wild-Pool-/Placeholder-Scope-Fix
   - Nur nach klarer Ursache; kein Fixbranch, solange Carrier-Scope, BST-Poolfilter und Species-Type-Filter nicht getrennt sind.

5. Danach getrennte Diagnosebloecke fuer die restlichen 070-Blocker
   - `FVX-FOE-009` gegen Trainer-Type-Diversity-/Null-Type-Scope.
   - `FVX-TRAIT-018` gegen Evolution-Reload-Mismatches, `Bad Egg` und BST-basierte Zielauswahl.
   - `FVX-TRAIT-019` gegen Evolution-Same-Typing-/Null-Scope.

6. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

7. `compat/upr-fvx-cfru-dpe-move-data-write-preserve`
   - Nur nach separater Freigabe: eng gegateten MoveData-Writer mit Preserve-Policy und Reload-Diagnose umsetzen.

8. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

9. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
