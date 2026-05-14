# Next Steps Update - 2026-05-14 - Field Items diagnostics candidate needed

Recommended next block only after an explicitly approved local CFRU/DPE Gen9-BPRE candidate is available:

`test/upr-fvx-cfru-dpe-field-items-scope-diagnostics-candidate`

Goal: run the sanitized Field-Items-only read-only diagnostic from protocol 098/099 and report only aggregated counters for visible Itemballs, Hidden Items/Signposts, TM/Non-TM slots, Required Field TMs, progression-sensitive items, bad items, modern item IDs and invalid/unloaded item IDs. Keep Shops, Pickup, held items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution and Text/Menu out of scope.

# Next Steps Update - 2026-05-14 - Field Items diagnostics scope

Recommended next block:

`test/upr-fvx-cfru-dpe-field-items-scope-diagnostics`

Goal: run a sanitized Field-Items-only diagnostic that reports aggregated visible Itemball, Hidden Item/Signpost, TM-slot, Non-TM-slot, Required Field TM, bad-item, modern-item and invalid-item counters. Keep Shops, Pickup, held items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution and Text/Menu out of scope.

# Next Steps - 2026-05-14 Field Items / Shops / Pickup Plan

Aktiver Anschlussblock:

- `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`

Ziel: Field Items als ersten getrennten Item-Writer read-only planen/diagnostizieren. Fokus auf sichtbare Itemballs, Hidden Items, TM-Slots, Required Field TMs, Progression-/Key-/System-Item-Preserve, invalid/fallback Items und Reload-Kriterien.

Entscheidung aus Diagnose 097:

- Field Items, Shops und Pickup nicht gemeinsam fixen.
- Field Items: Map-/Script-/Signpost-Offset-Writer, naechster engster Block.
- Pickup: separater Table-/Locator-/Probability-Scope.
- Shops: separater Shoplisten-/Terminator-/DataRewriter-/Repointing-/Preis-Scope.
- Gemeinsame Item-Pool-Bans sind noetig, aber kein gemeinsamer Writer-Fix.

Grenzen: keine Shops, kein Pickup, keine Encounter Held Items, keine Trainer/Starter Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Umsetzung.

# Next Steps - 2026-05-14 Post-Merge Palette Sync

Aktiver Anschlussblock:

- `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan`

Ziel: Field Items, Shops und Pickup read-only als eigenen P1-Scope planen. Keine Umsetzung, kein Randomizer-Lauf, kein Build und keine Vermischung mit Palette, Graphics, TypeChart, Trainer, Wild, Evolution, Text/Menu, MoveData oder MoveNames.

Post-Merge-Status aus Diagnose 096:

- Workspace PR #140 ist gemerged.
- `FVX-GFX-001` hat den UPR-FVX Guard-Fix aus PR #35/#139, aber der Reload-Smoke ist blockiert.
- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- `candidateSpeciesTotal=0`
- kein fachlicher Palette-Write-/Reload-Smoke
- keine Hochstufung fuer `FVX-GFX-001`
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`.

`FVX-GFX-001` wartet auf einen explizit freigegebenen UPR-FVX-ladbaren CFRU/DPE Gen9-BPRE-Kandidaten mit `candidateSpeciesTotal=1439`, bevor ein gleicher Normal-only Single-owner Reload-Smoke erneut sinnvoll ist.

# Next Steps - 2026-05-14 Update

Aktiver Anschlussblock nach Diagnose 096:

- `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke-retry`

Ziel: Den engen `FVX-GFX-001` Normal-only Single-owner Reload-Smoke erst wiederholen, wenn ein explizit freigegebener UPR-FVX-ladbarer CFRU/DPE-Gen9-BPRE-Kandidat verfügbar ist und `candidateSpeciesTotal=1439` erfüllt.

Status aus Diagnose 096:

- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- kein fachlicher Palette-Write-/Reload-Smoke
- keine Hochstufung für `FVX-GFX-001`
- `FVX-GFX-002/003/004` bleiben `Write modelliert`

Nicht ausweiten auf Shiny, Shared-Paletten, Graphics/Sprites, TypeChart/TypeEffectiveness, Species-Type-Write, Evolution-Writer, Items, Trainer/Wild, Text/Menu, MoveData oder MoveNames.

# Next Steps

## Aktueller Fokus

CFRU/DPE Palette Normal Single-owner Write Guard Fix ist dokumentiert. Aktuelle Diagnose: `08_tests/randomizer/095_palette_normal_single_owner_write_guard_fix_diagnostics.md`.

`FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel. `FVX-MOVE-005` bleibt getrennt vom MoveData-Byte-Writer-Scope.

Ergebnis aus 090: Der erneute Candidate-Preflight ist blockiert. `candidateFilesChecked=94`, `candidatePreflightSuccessful=false`, `candidateMovesTotal=not available`, `candidateHighestMove=not available`. Es gab keinen fachlichen Name-only fixed-length Reload-Smoke.

Planergebnis aus 091: echte `PokemonPalettesMod.RANDOM`-Randomization ist wegen compressed-data-, shared-pointer-, missing/invalid-pointer-, FreeSpace-/Repointing- und Forme-/Mapping-Risiken noch nicht direkt fixbar.

Diagnoseergebnis aus 093: der sanitisierten read-only Lauf findet `candidateWritablePalettes=385`, aber nur `candidateWritableNormalPalettes=385` und `candidateWritableShinyPalettes=0`. Shared/invalid/missing/decode-failed Paletten bleiben preserve-only.

Planergebnis aus 094: ein spaeterer Fix-/Smoke-Scope ist reviewbar, aber nur fuer Normal-Paletten, die single-owner, dekomprimierbar, gueltig, nicht shared, nicht missing, nicht invalid, nicht decode-failed und nicht cross-kind shared sind. Repointing muss bewusst abgesichert werden.

Fixstand aus 095: UPR-FVX `2697511da9a97df4c29c00dfda8b40e556020489` implementiert den Normal-only-Single-owner-Guard. Kein ROM-/Reload-Smoke wurde in diesem Block ausgefuehrt; `FVX-GFX-001` bleibt bis zum separaten Reload-Smoke `Write modelliert`.

Naechster aktiver Arbeitsblock: `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`.

## Priorisierte naechste Arbeitsbloecke

1. Palette Normal Single-owner Reload-Smoke ausfuehren
   - Empfohlener Branch: `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`.
   - Ziel: den UPR-FVX-Guard-Fix aus 095 fachlich mit einem sanitisierten Reload-Smoke bestaetigen.
   - Erwartet: `normalPaletteWriteCandidates=385`, `normalPaletteWriteAttempts <= 385`, `normalPaletteReloadMismatches=0`, `shinyPaletteWriteAttempts=0`, `sharedPaletteWriteAttempts=0`, `invalidPaletteWriteAttempts=0`, `missingPaletteWriteAttempts=0`, `decodeFailedPaletteWriteAttempts=0`, `crossKindSharedWriteAttempts=0`, `exceptionClass=none`, `stacktrace=none`.
   - Grenzen: keine Shiny-/Shared-/Graphics-/Sprite-, TypeChart-, Species-Type-, Evolution-, Items-, Trainer-, Wild-, Text/Menu- oder MoveData-Arbeit.

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

15. `analysis/upr-fvx-cfru-dpe-palette-single-owner-normal-only-fix-scope-plan`
   - Abgeschlossen: Diagnose 094 plant den normal-palette-only, single-owner/decompressible Fix-/Smoke-Scope; kein Shiny-Write, kein shared-pointer Write, kein Repointing ohne eigene Policy.

16. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
