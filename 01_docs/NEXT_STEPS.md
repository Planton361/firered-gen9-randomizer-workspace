# Next Steps

## Aktueller Fokus

CFRU/DPE Evolution Same Typing Code Diagnosis ist read-only dokumentiert. Diagnose: `08_tests/randomizer/079_p1_evolution_same_typing_code_diagnosis.md`.

## Priorisierte naechste Arbeitsbloecke

1. PRs fuer Wild-Filter-Carrier-Nullslot-Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Diagnose 075 und Submodule-Pin reviewen und mergen.

2. PRs fuer Trainer Type Diversity Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Diagnose 078 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `TrainerPokemonRandomizer` und den Force-Diverse-Types-/`usedTypes`-Pfad begrenzt.

3. `FVX-TRAIT-019` Evolutions Same Typing eng gegatet fixen
   - `FVX-FOE-009` ist im eng getesteten Trainer-Type-Diversity-Scope entblockt.
   - Wahrscheinlich konkrete Ursache aus 079: `EvolutionRandomizer` Same-Typing-Filter ruft `to.hasSharedType(...)` auf Kandidaten mit `primaryType == null` auf.
   - Fix nur fuer Same-Typing-/Null-Primary-Type-Scope in `EvolutionRandomizer`.
   - Kein Wild, Trainer, TypeChart, MoveData Write, Palette, Items, Text/Menu, Graphics oder Evolution-Methoden-Writer.

4. Weitere 070-Evolution-Blocker getrennt fortsetzen
   - `FVX-TRAIT-018` Evolutions Similar Strength gegen Evolution-Reload-Mismatches, `Bad Egg` und BST-basierte Zielauswahl.
   - `FVX-TRAIT-019` nach Fix separat mit Save/Log/Output/Reload und `writeReloadEvolutionMismatches=0` pruefen.
   - Weiter ohne TypeChart, MoveData Write, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level-Modifier oder Text/Menu/Graphics.

5. Wild-Suboptionen konservativ halten
   - `FVX-WILD-011` und `FVX-WILD-004` sind im `FVX-WILD-001` Carrier-Fix-Smoke stabil.
   - Evolution Restrictions, Catch Em All, Minimum Catch Rate und Level-Balance bleiben getrennte Wild-Scope-Themen.

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
