# Next Steps

## Aktueller Fokus

CFRU/DPE Wild-Filter-Carrier-Codeanalyse ist read-only dokumentiert. Diagnoseprotokoll: `08_tests/randomizer/074_p1_wild_filter_carrier_code_diagnosis.md`.

## Priorisierte naechste Arbeitsbloecke

1. PR fuer `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-code-diagnosis`
   - Read-only Codeanalyse 074 reviewen und mergen.

2. Eng gegateter Fixbranch fuer Wild-Mapping-/Nullslot-Scope
   - Ausgangspunkt: 074 grenzt die wahrscheinliche Ursache auf `WildEncounterRandomizer` GAME-Mapping, `areaInformationMap`, `EncounterArea.getSpeciesInArea()` und `SpeciesSet.add(null)` ein.
   - Ziel: `FVX-WILD-011` und `FVX-WILD-004` duerfen nicht mehr an einem nicht aufloesbaren/null Wild-Encounter-Slot mit `IllegalStateException` abbrechen.
   - Weiter ohne TypeChart, MoveData Write, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level-Modifier oder Text/Menu/Graphics.

3. Optional vor dem Fix: separater lokaler Wild-Carrier-Diagnosebranch
   - Nur falls ein sanitisiert belegter Area-/Slot- oder Exception-Message-Nachweis vor Fixfreigabe gewuenscht ist.
   - Keine ROM-/Log-/Output-/Build-Pfade, ROM-Namen, Hashes oder Loginhalte dokumentieren; keine Fixumsetzung in diesem optionalen Diagnosebranch.

4. Nach Fix: zwei getrennte Sanitized Smokes
   - `FVX-WILD-011` Wild Similar Strength.
   - `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary.
   - Erfolgskriterien: Save/Log/Output/Reload true, `writeReloadWildPokemonMismatches=0`, `Bad Egg`/`<unknown>` nach 055 klassifiziert und `stacktrace=none`.

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
