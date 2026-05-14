# Next Steps

## Aktueller Fokus

CFRU/DPE Palette Randomization Preserve/Repoint Plan ist erstellt. Aktuelle Diagnose: `08_tests/randomizer/091_palette_randomization_preserve_repoint_plan.md`.

`FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel. `FVX-MOVE-005` bleibt getrennt vom MoveData-Byte-Writer-Scope.

Ergebnis aus 090: Der erneute Candidate-Preflight ist blockiert. `candidateFilesChecked=94`, `candidatePreflightSuccessful=false`, `candidateMovesTotal=not available`, `candidateHighestMove=not available`. Es gab keinen fachlichen Name-only fixed-length Reload-Smoke.

Planergebnis aus 091: echte `PokemonPalettesMod.RANDOM`-Randomization ist wegen compressed-data-, shared-pointer-, missing/invalid-pointer-, FreeSpace-/Repointing- und Forme-/Mapping-Risiken noch nicht direkt fixbar. Zuerst ist eine read-only Palette-Pointer-/Compression-Diagnose noetig.

Naechster aktiver Arbeitsblock: `analysis/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics-plan`.

## Priorisierte naechste Arbeitsbloecke

1. Palette Pointer / Compression Diagnostics planen
   - Empfohlener Branch: `analysis/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics-plan`.
   - Ziel: read-only klaeren, welche CFRU/DPE Normal-/Shiny-Paletten dekomprimierbar, single-owner, shared, missing oder invalid sind.
   - Grundlage: Diagnose 058 und 091.
   - Grenzen: keine Codeaenderung, keine Randomizer-Laeufe, keine Builds, keine ROM-/Output-Artefakte dokumentieren.

2. Palette Randomization Preserve/Repoint Plan halten
   - Diagnose 091 dokumentiert: direkter Fix noch nicht eng genug.
   - `FVX-GFX-001..004` bleiben `Write modelliert`.
   - Spaeterer Fix darf nur single-owner/dekomprimierbare Paletten schreiben oder muss eine vollstaendige Secondary-Pointer-/Shared-Pointer-Policy liefern.

3. Move Names fixed-length Reload-Smoke erst mit eindeutigem Kandidaten wiederholen
   - Empfohlener Branch: `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke-candidate`.
   - Voraussetzung: freigegebener lokaler CFRU/DPE Gen9-BPRE-Kandidat muss mit `moves.total=992` und `991:PsychicNoise` erkennbar sein.
   - Ziel: `FVX-MOVE-005` Name-only im bestehenden Gen3 fixed-length Move-Namen-Pfad pruefen.
   - Kriterien: Save/Log/Output/Reload true, `moves.total=992`, `991:PsychicNoise`, `moveNameReloadMismatches=0`, `moveNameLengthViolations=0`, `moveNameTerminatorPaddingMismatches=0`, keine Description-/Pointer-Aenderung, `exceptionClass=none`, `stacktrace=none`.
   - Grenzen: keine Move Descriptions, keine Pointer-/Repointing- oder Text/Menu-Umsetzung, keine MoveData-Byte-Writer-Aenderung, keine TypeChart/TypeEffectiveness, keine Species-Type-, TM/HM-, Tutor-, Egg-, Learnset-, Palette-, Items-, Trainer-, Wild-, Evolution- oder Graphics-Arbeit.

4. Move Names fixed-length Reload-Smoke Retry-Ergebnis halten
   - Diagnose 089 dokumentiert den blockierten Versuch.
   - Diagnose 090 dokumentiert den blockierten Retry-Preflight mit 94 geprueften lokalen Kandidatendateien und ohne fachliche Smoke-Auswertung.
   - `FVX-MOVE-005` bleibt `Write modelliert`.
   - Keine Feature-Hochstufung ohne stabilen Name-only Reload.

5. Move Names / Descriptions Text/Menu-Scope Plan halten
   - Diagnose 088 dokumentiert `FVX-MOVE-005` als getrennten Text/Menu-Scope.
   - Name-only fixed-length Smoke ist realistisch.
   - Move Descriptions / Text/Menu-Repointing bleibt vorerst zurueckgestellt.

6. MoveData Fairy-Type-Byte-Fix post-merge halten
   - UPR-FVX PR #34 ist gemerged.
   - Workspace PR #129 ist gemerged.
   - Diagnose 087 bestaetigt `FVX-MOVE-004` mit Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`, `moves.total=992`, `991:PsychicNoise` und Preserve-Bytes `0` Mismatches.
   - `FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel; `FVX-MOVE-005` bleibt getrennt.

7. MoveData Types Reload-Smoke historisch einordnen
   - Branch: `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke`.
   - Diagnose 086 dokumentiert den Blocker fuer `FVX-MOVE-004`.
   - Save/Log/Output/Reload sind true; `moves.total=992` und `991:PsychicNoise` bleiben stabil.
   - Preserve-Bytes bleiben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
   - Der Blocker ist durch Diagnose 087 behoben.

8. MoveData Power/Accuracy/PP Reload-Smoke halten
   - Branch: `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke`.
   - Diagnose 085 bestaetigt `FVX-MOVE-001`, `FVX-MOVE-002` und `FVX-MOVE-003` mit Save/Log/Output/Reload true und `writeReloadMoveDataMismatches=0`.
   - `powerReloadMismatches=0`, `accuracyReloadMismatches=0`, `ppReloadMismatches=0`.
   - Preserve-Bytes bleiben bytegleich.

9. PRs fuer Wild-Filter-Carrier-Nullslot-Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Diagnose 075 und Submodule-Pin reviewen und mergen.

10. PRs fuer Trainer Type Diversity Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Diagnose 078 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `TrainerPokemonRandomizer` und den Force-Diverse-Types-/`usedTypes`-Pfad begrenzt.

11. PRs fuer Evolution Same Typing Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Diagnose 080 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `EvolutionRandomizer` und den Same-Typing-/Null-Primary-Type-Scope begrenzt.

12. PR fuer `FVX-TRAIT-018` Similar Strength Normalized Reload reviewen
   - Diagnose 082 bestaetigt den einzelnen Similar-Strength-Smoke mit Save/Log/Output/Reload true und `normalizedWriteReloadEvolutionMismatches=0`.
   - Der Reload-Vergleich nutzt nur persistierte Gen3-Evolution-Felder und Ziel-Species per interner `SpeciesSet`-Identitaet; `Evolution.forme` ist kein Mismatch-Kriterium.
   - `Bad Egg=true` ist nach 055 klassifiziert; `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
   - Fuer diesen engen `FVX-TRAIT-018`-Scope ist kein Fixbranch erforderlich. Evolution-Methoden-Writer und weitere Evolution-Suboptionen bleiben getrennt.

13. Wild-Suboptionen konservativ halten
   - `FVX-WILD-011` und `FVX-WILD-004` sind im `FVX-WILD-001` Carrier-Fix-Smoke stabil.
   - Evolution Restrictions, Catch Em All, Minimum Catch Rate und Level-Balance bleiben getrennte Wild-Scope-Themen.

14. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

15. `analysis/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics-plan`
   - Naechster empfohlener P1-Folgeblock: read-only Palette-Pointer-/Compression-Diagnose planen, bevor ein Palette-Randomization-Fix versucht wird.

16. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
