# Next Steps Update - 2026-05-15 - Field Items Random Even Ban Bad smoke next

Aktueller Fokus:

- Diagnose 112 confirms a Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=true`.
- Save/log/output/reload succeeded, `fieldItemReloadMismatches=0`, Required Field TMs stayed complete, and `badFieldItemWrites=0`.
- `FVX-ITEM-004` is tested for `FieldItemsMod.RANDOM`, but not fully GUI-compatible because Random Even + Ban Bad remains unsmoked and the 75er Ban-Bad baseline from Diagnose 111 was not reproduced in this run.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke`: sanitized Field-Items-only smoke for `FVX-ITEM-003 Field Items Random even distribution` with `banBadRandomFieldItems=true`.


Aktueller Fokus:

- Diagnose 111 plans `FVX-ITEM-004 Field Items Ban Bad Items` read-only.
- `banBadRandomFieldItems` affects the Non-TM Field-Items random pool only; TM slots and Required Field TMs stay in the separate TM path.
- Baseline Ban-Bad count from Diagnose 100: `badFieldItems=75` / `badItemBanCandidates=75`.
- `FVX-ITEM-004` remains `Write modelliert` until at least the first Ban-Bad reload smoke passes.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `test/upr-fvx-cfru-dpe-field-items-random-ban-bad-reload-smoke`: sanitized Field-Items-only smoke for `FVX-ITEM-002 Field Items Random` with `banBadRandomFieldItems=true`; keep Random Even + Ban Bad separate afterward.

# Next Steps Update - 2026-05-15 - Field Items Ban Bad scope plan next

Aktueller Fokus:

- Diagnose 110 confirms `FVX-ITEM-003 Field Items Random even distribution` as `GUI-kompatibel` in the narrow Field-Items-only scope with `banBadRandomFieldItems=false`.
- Confirmed counters include `fieldItemReloadMismatches=0`, `apiTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`, `randomTmPoolDeficit=0`, and `requiredFieldTMMissingAfter=0`.
- `FVX-ITEM-004 Field Items Ban Bad Items` remains `Write modelliert` and should be planned separately before activation.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `analysis/upr-fvx-cfru-dpe-field-items-ban-bad-scope-plan`: read-only plan for `FVX-ITEM-004 Field Items Ban Bad Items`, preserving the same allowed-slot, TM/Non-TM, Required-TM and API-TM-slot criteria.

# Next Steps Update - 2026-05-15 - Field Items Random Even smoke next

Aktueller Fokus:

- Diagnose 109 confirms `FVX-ITEM-002 Field Items Random` as `GUI-kompatibel` in the narrow Field-Items-only scope with `banBadRandomFieldItems=false`.
- Confirmed counters include `fieldItemReloadMismatches=0`, `apiTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`, `randomTmPoolDeficit=0`, and `requiredFieldTMMissingAfter=0`.
- `FVX-ITEM-003 Field Items Random even distribution` remains `Write modelliert` and should be tested separately next.
- `FVX-ITEM-004 Ban Bad Items` remains separate and inactive.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `test/upr-fvx-cfru-dpe-field-items-random-even-reload-smoke`: sanitized Field-Items-only smoke for `FVX-ITEM-003` without Ban Bad Items, preserving the same allowed-slot, TM/Non-TM, Required-TM and API-TM-slot criteria.

# Next Steps Update - 2026-05-15 - Field Items API TM-slot reload smoke next

Aktueller Fokus:

- UPR-FVX PR #37 prepares the narrow CFRU/DPE Field-Items API TM-slot scope fix.
- Workspace pins `02_external/upr-fvx` to `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- `FVX-ITEM-002` remains below GUI-compatible until a separate Field-Items-only reload smoke confirms `randomTmNeededSlots=28`, `apiTmFieldItemSlots=28`, and `fieldItemReloadMismatches=0`.

Empfohlener naechster Branch:

- `test/upr-fvx-cfru-dpe-field-items-api-tm-slot-reload-smoke`

Ziel:

- Run a sanitized Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=false` on UPR-FVX `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Keep Random Even, Ban Bad Items, Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Scriptparser, Palette, MoveData, Trainer, Wild, Evolution and Text/Menu out of scope.

# Next Steps Update - 2026-05-15 - Field Items API TM-slot scope fix next

Aktueller Fokus:

- Diagnose 107 narrows the `FVX-ITEM-002 Field Items Random` blocker to the Field-Items API TM-slot scope.
- Raw diagnostics show `tmFieldItemSlots=28` and `requiredFieldTMsTotal=24`; `getFieldItems()` currently exposes `0` TM slots because it filters on `Item::isAllowed`.
- Do not proceed to `FVX-ITEM-003` or `FVX-ITEM-004` until `FVX-ITEM-002` reloads successfully.

Empfohlener naechster Branch:

- `compat/upr-fvx-cfru-dpe-field-items-api-tm-slot-scope-fix`

Ziel:

- Prepare a minimal CFRU/DPE-gated Field-Items API TM-slot scope fix for `FVX-ITEM-002` with `banBadRandomFieldItems=false`.
- Do not make TMs globally allowed and do not expand Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even, Ban Bad Items, Scriptparser, Palette, MoveData, Trainer, Wild, Evolution or Text/Menu.

# Next Steps Update - 2026-05-15 - Field Items Random API TM-slot scope plan next

Aktueller Fokus:

- Diagnose 106 blocks `FVX-ITEM-002 Field Items Random` after PR #36.
- The Unique-TM-Filler pool is sufficient: `randomTmUniquePoolSize=50`, `randomTmFillerAvailable=26`, `randomTmPoolDeficit=0`.
- Active blocker is now the `getFieldItems()` API TM-slot scope: raw diagnostics show `tmFieldItemSlots=28`, but Randomizer API metrics show `randomTmNeededSlots=0` / `randomTmCurrentSlots=0`.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-field-items-random-api-tm-slot-scope-plan`

Ziel des Folgeblocks:

- Read-only klaeren, warum der Gen3/CFRU-DPE Field-Items-API-Scope keine TM-Field-Item-Slots an `ItemRandomizer.randomizeTMFieldItems(...)` uebergibt.
- Weiterhin keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Random Even Distribution und keine Ban-Bad-Items-Umsetzung.

# Next Steps Update - 2026-05-15 - Field Items Random TM-pool reload smoke next

Aktueller Fokus:

- UPR-FVX PR #36 contains the narrow `FVX-ITEM-002 Field Items Random` TM-pool fix.
- Workspace pins `02_external/upr-fvx` to `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd` in this branch.
- `FVX-ITEM-002` remains pending until a Field-Items-only Write-/Reload-Smoke confirms the fix.

Naechster empfohlener Minimalblock nach Merge:

- `test/upr-fvx-cfru-dpe-field-items-random-tm-pool-reload-smoke`

Ziel des Folgeblocks:

- `FVX-ITEM-002 Field Items Random` mit `banBadRandomFieldItems=false` fachlich erneut testen.
- Erwartete TM-Pool-Metriken: `randomTmNeededSlots=28`, `randomTmRequiredTotal=24`, `randomTmFillerNeeded=4`, `randomTmPoolDeficit=0`, `randomTmResultSize=28`, `randomTmResultUniqueSize=28`.
- Erwartete Reload-Metriken: `saveSuccessful=true`, `reloadSuccessful=true`, `fieldItemReloadMismatches=0`, `requiredFieldTMMissingAfter=0`, `disallowedFieldItemWrites=0`, `scriptPatternExpansion=0`.
- Weiterhin keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Random Even Distribution und keine Ban-Bad-Items-Umsetzung.

# Next Steps Update - 2026-05-15 - Field Items Random TM-pool fix next

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` bleibt `GUI-kompatibel` im engen allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random` bleibt blockiert durch den TM-Field-Items-Random-Pool.
- Diagnose 104 empfiehlt einen engen Fix nur fuer `ItemRandomizer.randomizeTMFieldItems(...)` bzw. einen kleinen privaten Helper.

Naechster empfohlener Minimalblock:

- `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix`

Ziel des Folgeblocks:

- Minimalen UPR-FVX-Fix fuer `FVX-ITEM-002` vorbereiten.
- Sanitisiert pruefen: `randomTmNeededSlots=28`, `randomTmRequiredTotal=24`, `randomTmCandidatePoolSize >= 28`, `randomTmPoolDeficit=0`.
- Danach Field-Items-Random Write-/Reload-Smoke wiederholen.
- Keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Random Even Distribution, keine Ban-Bad-Items-Umsetzung.

# Next Steps Update - 2026-05-15 - Field Items Random TM-pool blocker next

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` bleibt durch Diagnose 102 `GUI-kompatibel` im engen allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random` ist durch Diagnose 103 blockiert: Save bricht mit `RandomizationException` ab, kein Output-ROM, kein Reload.
- `FVX-ITEM-003 Field Items Random even distribution` und `FVX-ITEM-004 Ban Bad Items` bleiben `Write modelliert`.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-field-items-random-tm-pool-blocker-plan`

Ziel des Folgeblocks:

- Read-only den Random-TM-Field-Items-Pool und Required-TM-Policy untersuchen.
- Klaeren, ob ein spaeterer Fix eng auf `FVX-ITEM-002` Field Items Random begrenzt werden kann.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution und Text/Menu bleiben ausserhalb.

# Next Steps Update - 2026-05-15 - Field Items Random smoke next

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` ist durch Diagnose 102 im engen allowed-slot Scope `GUI-kompatibel`.
- `FVX-ITEM-002 Field Items Random`, `FVX-ITEM-003 Field Items Random even distribution` und `FVX-ITEM-004 Ban Bad Items` bleiben `Write modelliert`.
- Shops, Pickup und Held Items bleiben getrennte Writer-Scope-Bloecke.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-field-items-random-reload-smoke`

Ziel des Folgeblocks:

- Nur `FVX-ITEM-002 Field Items Random` testen.
- `banBadRandomFieldItems=false` lassen; `FVX-ITEM-004` separat spaeter testen.
- Dieselben allowed-slot-, TM-/Non-TM-, Required-TM- und preserve-only-Metriken wie Diagnose 102 pruefen.

# Next Steps Update - 2026-05-14 - Field Items allowed-slot smoke next

Aktueller Fokus:

- `FVX-ITEM-001..004` Field Items bleiben `Write modelliert`.
- Diagnose 101 bestaetigt read-only, dass der bestehende Gen3 Field-Items-Writer bereits nur allowed Slots schreibt.
- Ein fachlicher Write-/Reload-Smoke wurde nicht ausgefuehrt, weil fuer diesen Block keine explizite lokale Kandidatenfreigabe fuer einen ROM-Write vorlag.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-field-items-allowed-slot-reload-smoke`

Ziel des Folgeblocks:

- Explizit freigegebenen CFRU/DPE Gen9-BPRE-Kandidaten verwenden.
- Nur `FVX-ITEM-001 Field Items Shuffle` als ersten Field-Items-Carrier pruefen.
- Erwartet: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`, TM-/Non-TM-Mismatches `0`, `requiredFieldTMMissingAfter=0`, `disallowedFieldItemWrites=0`, `scriptPatternExpansion=0`.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution und Text/Menu bleiben ausserhalb.

# Next Steps Update - 2026-05-14 - Field Items guarded write/smoke

Recommended next block:

`compat/upr-fvx-cfru-dpe-field-items-allowed-slot-write-guard`

Goal: implement and smoke a narrow Field-Items-only guard for allowed slots, preserving disallowed/progression-sensitive/key-system slots, keeping TM slots as TMs and Non-TM slots as Non-TMs, and maintaining `requiredFieldTMMissingAfter=0`. Keep Shops, Pickup, held items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution and Text/Menu out of scope.

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
