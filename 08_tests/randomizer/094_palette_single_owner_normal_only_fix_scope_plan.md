# 094 - CFRU/DPE Palette Single-owner Normal-only Fix-Scope Plan

Datum: 2026-05-14

Branch: `analysis/upr-fvx-cfru-dpe-palette-single-owner-normal-only-fix-scope-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

## Ziel

Read-only-Plan fuer einen engen spaeteren Palette-Fix-/Smoke-Scope, der ausschliesslich die in Diagnose 093 ermittelten dekomprimierbaren Single-owner-Normal-Palette-Kandidaten betrifft.

Keine Codeaenderung, kein Build, kein Randomizer-Lauf, kein ROM-Zugriff, keine Dokumentation privater Artefakte.

## Gelesene Grundlagen

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/058_p1_palette_randomization_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `08_tests/randomizer/091_palette_randomization_preserve_repoint_plan.md`
- `08_tests/randomizer/092_palette_pointer_compression_diagnostics_plan.md`
- `08_tests/randomizer/093_palette_pointer_compression_diagnostics.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

## Ausgangsbefund aus Diagnose 093

- `candidateLoaded=true`
- `palettePointerScanSuccessful=true`
- `candidateSpeciesTotal=1439`
- `normalPalettePointersTotal=1439`
- `shinyPalettePointersTotal=1439`
- `normalPaletteDecodeFailures=313`
- `shinyPaletteDecodeFailures=312`
- `normalPaletteDecodeSuccesses=1031`
- `shinyPaletteDecodeSuccesses=592`
- `singleOwnerNormalPalettes=919`
- `singleOwnerShinyPalettes=535`
- `sharedNormalPalettes=192`
- `sharedShinyPalettes=137`
- `missingNormalPalettePointers=1`
- `missingShinyPalettePointers=37`
- `invalidNormalPalettePointers=94`
- `invalidShinyPalettePointers=498`
- `duplicateNormalPalettePointers=192`
- `duplicateShinyPalettePointers=137`
- `crossKindSharedPalettePointers=1809`
- `sharedPointerGroups=775`
- `largestSharedPointerGroupSize=156`
- `singleOwnerBothNormalAndShinySpecies=0`
- `candidateWritablePalettes=385`
- `candidateWritableNormalPalettes=385`
- `candidateWritableShinyPalettes=0`
- `skipPaletteEntries=2493`
- `exceptionClass=none`
- `stacktrace=none`

## Scope-Einschaetzung

Ein spaeterer Fix-/Smoke-Scope ist reviewbar, wenn er strikt auf Normal-Paletten beschraenkt bleibt und die Diagnose-093-Kategorie als Obergrenze behandelt:

- Normal-Palette
- dekomprimierbar
- single-owner
- gueltiger Pointer
- nicht shared
- nicht missing/null
- nicht out-of-ROM/invalid
- nicht decode-failed
- keine cross-kind shared Pointer
- keine unsicheren Forme-/Expanded-Species-Mapping-Faelle

Der Scope ist kein vollstaendiger Palette-Randomization-Fix. Er ist ein begrenzter Nachweis, dass echte geaenderte Normal-Paletten fuer sichere Single-owner-Kandidaten geschrieben, reloadbar gelesen und alle ausgeschlossenen Kategorien bytegleich erhalten werden koennen.

## Spaetere Write-/Skip-Policy

Spaeterer Writer darf nur schreiben, wenn alle Bedingungen gleichzeitig erfuellt sind:

- Palette-Art ist Normal, nicht Shiny.
- Pointer ist vorhanden, gueltig und innerhalb der ROM-Grenzen.
- Palette ist vor dem Write dekomprimierbar.
- Pointer ist single-owner in der Normal-Palette-Klassifikation.
- Pointer ist nicht shared, nicht duplicate und nicht cross-kind shared.
- Die Species-/Forme-Zuordnung ist eindeutig.
- Der spaetere Write-Versuch bleibt innerhalb der ermittelten Kandidatenobergrenze.

Spaeterer Writer muss skippen/preserven:

- alle Shiny-Paletten
- shared Pointer
- missing/null Pointer
- invalid/out-of-ROM Pointer
- decode-failed Paletten
- duplicate Pointer
- cross-kind shared Pointer
- unsichere Forme-/Expanded-Species-Mapping-Faelle
- alle Kategorien ausserhalb Normal-Palette

Die Gate-Entscheidung muss unmittelbar vor dem Write oder aus einer unveraenderten Preflight-Klassifikation erfolgen. GUI- oder Randomizer-Optionen duerfen keine Shiny-, Shared-, Invalid-, Missing- oder Decode-failed-Paletten indirekt in den Write-Pfad ziehen.

## Repoint-/Compression-Entscheidung

Der bestehende Gen3-Pfad arbeitet ueber komprimierte Palette-Daten. Nach Diagnose 058/091 liegt der relevante Write-Pfad bei `savePokemonPalettes()` ueber `rewriteCompressedPalette()` und `DataRewriter`.

Planentscheidung:

- Ein sinnvoller echter Write-Smoke wird voraussichtlich Repointing verwenden muessen, wenn die bestehende `rewriteCompressedPalette()`-/`DataRewriter`-Semantik beibehalten wird.
- Kein In-place-Overwrite ohne eigene Groessen-, Compression- und Reload-Policy annehmen.
- Repointing ist nur fuer die sichere Normal-Single-owner-Kategorie akzeptabel.
- Alte shared komprimierte Daten duerfen nicht freigegeben oder ueberschrieben werden.
- Pointer-Updates duerfen nur fuer eindeutig bekannte Normal-Palette-Tabellen erfolgen.
- Falls ein spaeterer Fix Repointing komplett vermeiden soll, ist kein aussagekraeftiger echter Randomization-Write-Smoke realistisch; dann muesste der Block zurueckgestellt oder auf Skip-/Preserve-Diagnose reduziert werden.

Pflichtkriterien bei Repointing:

- Free-Space-Allocation ist nachvollziehbar und reloadbar.
- Repointed Pointer zeigen auf gueltige dekomprimierbare Palette-Daten.
- Nur geschriebene Normal-Single-owner-Kandidaten erhalten erwartete Pointer-Aenderungen.
- Skipped Paletten behalten Pointer und dekomprimierte Daten bytegleich.
- Keine secondary-pointer- oder shared-owner-Freigabe ohne expliziten Eigentumsnachweis.

## GUI-Suboptionen fuer spaeteren Smoke

- `FVX-GFX-001 Pokemon Palettes Random`: fuer einen ersten Fix-/Smoke-Block geeignet, aber nur als Normal-only-Farbtraeger mit strengem Writer-Gate.
- `FVX-GFX-002 Follow Types`: nicht im ersten Fix-Smoke. Spaeter nur als separate Normal-only-Variante, bei der Typen ausschliesslich als Farbquelle dienen und keine TypeChart-, TypeEffectiveness- oder Species-Type-Write-Arbeit entsteht.
- `FVX-GFX-003 Follow Evolutions`: vorerst ausklammern, weil keine Evolution-Writer- oder Evolutionsgraph-Ausweitung in diesen Scope gehoert.
- `FVX-GFX-004 Shiny From Normal`: ausklammern, weil Diagnose 093 `candidateWritableShinyPalettes=0` gezeigt hat.

## Spaetere Smoke-/Review-Kriterien

Pflichtkriterien fuer einen spaeteren Fix-/Smoke-Block:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `normalPaletteWriteCandidates=385`
- `normalPaletteWriteAttempts <= 385`
- `normalPaletteReloadMismatches=0`
- `shinyPaletteWriteAttempts=0`
- `sharedPaletteWriteAttempts=0`
- `invalidPaletteWriteAttempts=0`
- `missingPaletteWriteAttempts=0`
- `decodeFailedPaletteWriteAttempts=0`
- `crossKindSharedWriteAttempts=0`
- `skippedPaletteEntries` dokumentiert
- `palettePointerMismatches=0`, falls Pointer unveraendert bleiben sollen
- `unexpectedPalettePointerMismatches=0`, falls Repointing fuer geschriebene Kandidaten erwartet ist
- `repointedPalettePointersValid=true`, falls Repointing stattfindet
- `compressedPaletteDecodeFailuresAfter=0` fuer geschriebene Kandidaten
- `preservedSkippedPaletteByteMismatches=0`
- `oldSharedDataFreeAttempts=0`
- `secondaryPointerPolicyViolations=0`
- `exceptionClass=none`
- `stacktrace=none`

Sinnvolle Zusatzmetriken:

- `normalPaletteWritesSucceeded`
- `normalPaletteWritesSkipped`
- `shinyPaletteByteMismatches=0`
- `sharedPaletteByteMismatches=0`
- `invalidPaletteTouched=false`
- `missingPaletteTouched=false`
- `decodeFailedPaletteTouched=false`
- `crossKindSharedTouched=false`
- `freeSpaceAllocations`
- `repointedNormalPalettePointers`
- `writtenPaletteDecodeSuccessesAfter`

## Feature-Status-Empfehlung

Nach einem erfolgreichen spaeteren Normal-only-Single-owner-Smoke waere hoechstens eine eingeschraenkte Hochstufung fuer `FVX-GFX-001` gerechtfertigt:

- `FVX-GFX-001`: maximal `Getestet` fuer den expliziten Normal-only-Single-owner-Subset, nicht voll `GUI-kompatibel`.
- `FVX-GFX-002`: bleibt `Write modelliert`, bis ein eigener Follow-Types-Normal-only-Smoke erfolgt.
- `FVX-GFX-003`: bleibt `Write modelliert`.
- `FVX-GFX-004`: bleibt `Write modelliert`.

Eine volle `GUI-kompatibel`-Einstufung fuer Palette Randomization waere erst vertretbar, wenn GUI-nahe Suboptionen, Shiny-/Shared-Policies und Repoint-/Preserve-Verhalten vollstaendig abgedeckt sind.

## Risiken / Annahmen

- Die 385 Kandidaten sind eine Diagnose-093-Obergrenze, keine Garantie fuer tatsaechliche Write-Versuche.
- Bestehende Compression kann neue Datenlaengen erzeugen und Repointing erforderlich machen.
- Shared- und cross-kind Pointer sind Hochrisiko und bleiben preserve-only.
- `singleOwnerBothNormalAndShinySpecies=0` bestaetigt, dass Shiny nicht in diesen engen Scope gehoert.
- Expanded-Species-/Forme-Mapping muss konservativ behandelt werden.
- `Follow Types` darf nicht mit TypeChart, TypeEffectiveness oder Species-Type-Write vermischt werden.
- `Follow Evolutions` darf nicht mit Evolution-Writer-Arbeit vermischt werden.

## Empfehlung

Fix vorbereiten, aber nur als enges `FVX-GFX-001` Normal-Palette-Single-owner-Gate:

- UPR-FVX-Writer-Gate fuer Normal-only Single-owner/decode-success/valid/non-shared.
- Kein Shiny-Write.
- Kein Shared-Write.
- Kein breiter Graphics-/Sprite-Scope.
- Kein TypeChart-, Species-Type- oder Evolution-Writer-Scope.
- Sanitisierten Reload-Smoke mit den oben genannten Zaehlern als Abnahmekriterium einplanen.

Empfohlener Folgebranch:

- `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`
