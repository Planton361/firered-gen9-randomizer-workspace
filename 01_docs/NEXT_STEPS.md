# Next Steps

## Aktueller Fokus

CFRU/DPE MoveData Fairy-Type-Byte Fix ist dokumentiert. Diagnose: `08_tests/randomizer/087_move_data_fairy_type_byte_fix_diagnostics.md`.

`FVX-MOVE-004` Randomize Move Types ist nach dem engen CFRU/DPE-MoveData-Fairy-Type-Byte-Fix reload-stabil.

UPR-FVX PR #34 und Workspace PR #129 sind gemerged. Der Workspace pinnt `02_external/upr-fvx` auf `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`.

Naechster aktiver Arbeitsblock: konservativer Planungsblock fuer `FVX-MOVE-005` Move Names / Move Descriptions als getrennten Text/Menu-Scope.

## Priorisierte naechste Arbeitsbloecke

1. Move Names / Descriptions Text/Menu-Scope planen
   - Empfohlener Branch: `analysis/upr-fvx-cfru-dpe-move-names-text-menu-scope-plan`.
   - Ziel: read-only entscheiden und dokumentieren, ob `FVX-MOVE-005` Move Names / Move Descriptions als eigener Text/Menu-Scope machbar ist oder vorerst zurueckgestellt bleibt.
   - Fokus: Move-Namen-Tabellen, Move-Descriptions, Stringlaengen, Pointer-/Text-/Menu-Risiken, CFRU/DPE-Gen9-BPRE-Gates und sichere Reload-Kriterien modellieren.
   - Grenzen: keine Umsetzung, keine Randomizer-Laeufe, keine Builds, keine ROM-/Log-/Output-Artefakte dokumentieren; nicht mit MoveData `+0..+11`, TypeChart, TypeEffectiveness, Species-Type-Write, TM/HM, Tutor, Egg, Learnsets, Palette, Items, Trainer, Wild, Evolutions oder Graphics vermischen.

2. MoveData Fairy-Type-Byte-Fix post-merge halten
   - UPR-FVX PR #34 ist gemerged.
   - Workspace PR #129 ist gemerged.
   - Diagnose 087 bestaetigt `FVX-MOVE-004` mit Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`, `moves.total=992`, `991:PsychicNoise` und Preserve-Bytes `0` Mismatches.
   - `FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel; `FVX-MOVE-005` bleibt getrennt.

3. MoveData Types Reload-Smoke historisch einordnen
   - Branch: `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke`.
   - Diagnose 086 dokumentiert den Blocker fuer `FVX-MOVE-004`.
   - Save/Log/Output/Reload sind true; `moves.total=992` und `991:PsychicNoise` bleiben stabil.
   - Preserve-Bytes bleiben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
   - Der Blocker ist durch Diagnose 087 behoben.

4. MoveData Power/Accuracy/PP Reload-Smoke reviewen
   - Branch: `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke`.
   - Diagnose 085 bestaetigt `FVX-MOVE-001`, `FVX-MOVE-002` und `FVX-MOVE-003` mit Save/Log/Output/Reload true und `writeReloadMoveDataMismatches=0`.
   - `powerReloadMismatches=0`, `accuracyReloadMismatches=0`, `ppReloadMismatches=0`.
   - Preserve-Bytes bleiben bytegleich.

5. PRs fuer Wild-Filter-Carrier-Nullslot-Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Diagnose 075 und Submodule-Pin reviewen und mergen.

6. PRs fuer Trainer Type Diversity Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Diagnose 078 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `TrainerPokemonRandomizer` und den Force-Diverse-Types-/`usedTypes`-Pfad begrenzt.

7. PRs fuer Evolution Same Typing Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Diagnose 080 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `EvolutionRandomizer` und den Same-Typing-/Null-Primary-Type-Scope begrenzt.

8. PR fuer `FVX-TRAIT-018` Similar Strength Normalized Reload reviewen
   - Diagnose 082 bestaetigt den einzelnen Similar-Strength-Smoke mit Save/Log/Output/Reload true und `normalizedWriteReloadEvolutionMismatches=0`.
   - Der Reload-Vergleich nutzt nur persistierte Gen3-Evolution-Felder und Ziel-Species per interner `SpeciesSet`-Identitaet; `Evolution.forme` ist kein Mismatch-Kriterium.
   - `Bad Egg=true` ist nach 055 klassifiziert; `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
   - Fuer diesen engen `FVX-TRAIT-018`-Scope ist kein Fixbranch erforderlich. Evolution-Methoden-Writer und weitere Evolution-Suboptionen bleiben getrennt.

9. Wild-Suboptionen konservativ halten
   - `FVX-WILD-011` und `FVX-WILD-004` sind im `FVX-WILD-001` Carrier-Fix-Smoke stabil.
   - Evolution Restrictions, Catch Em All, Minimum Catch Rate und Level-Balance bleiben getrennte Wild-Scope-Themen.

10. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

11. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

12. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
