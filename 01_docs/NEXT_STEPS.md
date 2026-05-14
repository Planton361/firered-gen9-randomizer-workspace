# Next Steps

## Aktueller Fokus

CFRU/DPE Move Names fixed-length Reload-Smoke wurde versucht. Diagnose: `08_tests/randomizer/089_move_names_fixed_length_reload_smoke.md`.

`FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel. `FVX-MOVE-005` bleibt getrennt vom MoveData-Byte-Writer-Scope.

Ergebnis aus 089: Der fachliche Smoke ist blockiert, weil lokal kein freigegebener CFRU/DPE Gen9-BPRE-Kandidat mit `moves.total=992` und `991:PsychicNoise` gefunden wurde.

Naechster aktiver Arbeitsblock: denselben Name-only fixed-length Reload-Smoke erneut ausfuehren, sobald ein passender lokaler Smoke-Kandidat eindeutig verfuegbar ist.

## Priorisierte naechste Arbeitsbloecke

1. Move Names fixed-length Reload-Smoke erneut versuchen
   - Empfohlener Branch: `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke`.
   - Voraussetzung: freigegebener lokaler CFRU/DPE Gen9-BPRE-Kandidat muss mit `moves.total=992` und `991:PsychicNoise` erkennbar sein.
   - Ziel: `FVX-MOVE-005` Name-only im bestehenden Gen3 fixed-length Move-Namen-Pfad pruefen.
   - Kriterien: Save/Log/Output/Reload true, `moves.total=992`, `991:PsychicNoise`, `moveNameReloadMismatches=0`, `moveNameLengthViolations=0`, `moveNameTerminatorPaddingMismatches=0`, keine Description-/Pointer-Aenderung, `exceptionClass=none`, `stacktrace=none`.
   - Grenzen: keine Move Descriptions, keine Pointer-/Repointing- oder Text/Menu-Umsetzung, keine MoveData-Byte-Writer-Aenderung, keine TypeChart/TypeEffectiveness, keine Species-Type-, TM/HM-, Tutor-, Egg-, Learnset-, Palette-, Items-, Trainer-, Wild-, Evolution- oder Graphics-Arbeit.

2. Move Names fixed-length Reload-Smoke Ergebnis halten
   - Diagnose 089 dokumentiert den blockierten Versuch.
   - `FVX-MOVE-005` bleibt `Write modelliert`.
   - Keine Feature-Hochstufung ohne stabilen Name-only Reload.

3. Move Names / Descriptions Text/Menu-Scope Plan halten
   - Diagnose 088 dokumentiert `FVX-MOVE-005` als getrennten Text/Menu-Scope.
   - Name-only fixed-length Smoke ist realistisch.
   - Move Descriptions / Text/Menu-Repointing bleibt vorerst zurueckgestellt.

4. MoveData Fairy-Type-Byte-Fix post-merge halten
   - UPR-FVX PR #34 ist gemerged.
   - Workspace PR #129 ist gemerged.
   - Diagnose 087 bestaetigt `FVX-MOVE-004` mit Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`, `moves.total=992`, `991:PsychicNoise` und Preserve-Bytes `0` Mismatches.
   - `FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel; `FVX-MOVE-005` bleibt getrennt.

5. MoveData Types Reload-Smoke historisch einordnen
   - Branch: `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke`.
   - Diagnose 086 dokumentiert den Blocker fuer `FVX-MOVE-004`.
   - Save/Log/Output/Reload sind true; `moves.total=992` und `991:PsychicNoise` bleiben stabil.
   - Preserve-Bytes bleiben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
   - Der Blocker ist durch Diagnose 087 behoben.

6. MoveData Power/Accuracy/PP Reload-Smoke reviewen
   - Branch: `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke`.
   - Diagnose 085 bestaetigt `FVX-MOVE-001`, `FVX-MOVE-002` und `FVX-MOVE-003` mit Save/Log/Output/Reload true und `writeReloadMoveDataMismatches=0`.
   - `powerReloadMismatches=0`, `accuracyReloadMismatches=0`, `ppReloadMismatches=0`.
   - Preserve-Bytes bleiben bytegleich.

7. PRs fuer Wild-Filter-Carrier-Nullslot-Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Diagnose 075 und Submodule-Pin reviewen und mergen.

8. PRs fuer Trainer Type Diversity Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Diagnose 078 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `TrainerPokemonRandomizer` und den Force-Diverse-Types-/`usedTypes`-Pfad begrenzt.

9. PRs fuer Evolution Same Typing Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Diagnose 080 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `EvolutionRandomizer` und den Same-Typing-/Null-Primary-Type-Scope begrenzt.

10. PR fuer `FVX-TRAIT-018` Similar Strength Normalized Reload reviewen
   - Diagnose 082 bestaetigt den einzelnen Similar-Strength-Smoke mit Save/Log/Output/Reload true und `normalizedWriteReloadEvolutionMismatches=0`.
   - Der Reload-Vergleich nutzt nur persistierte Gen3-Evolution-Felder und Ziel-Species per interner `SpeciesSet`-Identitaet; `Evolution.forme` ist kein Mismatch-Kriterium.
   - `Bad Egg=true` ist nach 055 klassifiziert; `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
   - Fuer diesen engen `FVX-TRAIT-018`-Scope ist kein Fixbranch erforderlich. Evolution-Methoden-Writer und weitere Evolution-Suboptionen bleiben getrennt.

11. Wild-Suboptionen konservativ halten
   - `FVX-WILD-011` und `FVX-WILD-004` sind im `FVX-WILD-001` Carrier-Fix-Smoke stabil.
   - Evolution Restrictions, Catch Em All, Minimum Catch Rate und Level-Balance bleiben getrennte Wild-Scope-Themen.

12. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

13. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

14. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
