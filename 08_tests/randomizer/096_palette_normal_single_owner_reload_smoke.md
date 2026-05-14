# 096 - CFRU/DPE Palette Normal Single-owner Reload-Smoke

Datum: 2026-05-14
Branch: `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`
Scope: `FVX-GFX-001` Pokemon Palettes Random, begrenzt auf Normal-only Single-owner Palette-Write-Guard
UPR-FVX-Pin: `2697511da9a97df4c29c00dfda8b40e556020489`

## Ziel

Dieser Block sollte den in Diagnose 095 implementierten CFRU/DPE-Gen9-BPRE Palette-Write-Guard per Reload-Smoke prüfen.

Getestet werden sollte ausschließlich der guarded Normal-Palette-Write-Scope:

- Normal-Paletten
- single-owner
- decode-success
- valid pointer
- non-shared
- non-cross-kind
- nicht missing/null
- nicht invalid/out-of-ROM
- keine unsichere Forme-/Expanded-Mapping-Situation

Explizit nicht im Scope:

- Shiny-Palette-Writes
- Shared-Palette-Writes
- Graphics/Sprites
- TypeChart / TypeEffectiveness
- Species-Type-Write
- Evolution-Writer
- Items / Field / Shops / Pickup
- Trainer / Wild / Text/Menu
- MoveData / MoveNames

## Preflight-Ergebnis

Der lokale Smoke wurde sanitisiert vorbereitet und hat keine privaten Pfade, ROM-Namen, Hashes, Raw Pointer, Offsets oder Logauszüge dokumentiert.

Aggregierte Preflight-Zähler:

- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- `candidateSpeciesTotal=0`
- `exceptionClass=none`
- `stacktrace=none`

Bewertung: blockiert. Es stand kein UPR-FVX-ladbarer CFRU/DPE-Gen9-BPRE-Kandidat mit `candidateSpeciesTotal=1439` für den fachlichen Reload-Smoke zur Verfügung.

## Smoke-Ergebnis

Der fachliche Palette-Reload-Smoke wurde nicht ausgeführt, weil die Kandidaten-Preflight-Bedingung nicht erfüllt war.

Sanitisierte Ergebniszähler:

- `saveSuccessful=false`
- `logSuccessful=false`
- `outputRomExists=false`
- `logNonEmpty=false`
- `reloadSuccessful=false`
- `normalPaletteWriteCandidates=0`
- `normalPaletteWriteAttempts=-1`
- `normalPaletteWriteSuccesses=0`
- `normalPaletteReloadMismatches=0`
- `shinyPaletteWriteAttempts=-1`
- `sharedPaletteWriteAttempts=0`
- `invalidPaletteWriteAttempts=0`
- `missingPaletteWriteAttempts=0`
- `decodeFailedPaletteWriteAttempts=0`
- `crossKindSharedWriteAttempts=0`
- `preservedSkippedPaletteByteMismatches=0`
- `compressedPaletteDecodeFailuresAfter=0`
- `palettePointerMismatches=0`
- `sharedPalettePolicyViolations=0`
- `invalidPalettePointersAfter=0`
- `paletteDecodeFailuresAfter=0`
- `exceptionClass=none`
- `stacktrace=none`

Die `false`-/`-1`-Werte sind Blockerwerte aus dem nicht erreichten Smoke-Pfad, keine fachlichen Writer-Mismatches.

## Skip-/Preserve-Ergebnis

Nicht fachlich bewertet, da kein Zielkandidat geladen wurde.

Die Preserve-/Skip-Policy aus Diagnose 095 bleibt unverändert:

- Shiny-Paletten preserve/skip
- Shared Pointer preserve/skip
- missing/null Pointer preserve/skip
- invalid/out-of-ROM Pointer preserve/skip
- decode-failed Paletten preserve/skip
- duplicate/cross-kind shared Pointer preserve/skip
- unsichere Forme-/Expanded-Mapping-Fälle preserve/skip

## Repoint-/Pointer-Ergebnis

Nicht fachlich bewertet, da kein Zielkandidat geladen wurde.

Sanitisierte Zähler:

- `repointedPalettePointersValid=false`
- `repointedPalettePointers=0`
- `unchangedPalettePointers=0`
- `palettePointerMismatches=0`

`repointedPalettePointersValid=false` ist hier ein Blockerwert, weil kein Write-/Reload-Pfad erreicht wurde.

## Feature-Status

Keine Hochstufung.

- `FVX-GFX-001` bleibt nicht `GUI-kompatibel`; der Fix ist vorhanden, aber der Normal-only Single-owner Reload-Smoke ist lokal blockiert.
- `FVX-GFX-002` bleibt `Write modelliert`.
- `FVX-GFX-003` bleibt `Write modelliert`.
- `FVX-GFX-004` bleibt `Write modelliert`.

## Risiken / Annahmen

- Diagnose 093 konnte Palette-Pointer roh klassifizieren, aber der 096-Smoke benötigt einen durch UPR-FVX ladbaren Kandidaten, damit der tatsächliche Writer- und Reload-Pfad geprüft wird.
- Ohne solchen Kandidaten darf `FVX-GFX-001` nicht als getestet oder GUI-kompatibel markiert werden.
- Keine privaten Artefaktwerte wurden dokumentiert.

## Nächster empfohlener Block

`test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke-retry`

Ziel: denselben engen Smoke erst wiederholen, wenn ein explizit freigegebener UPR-FVX-ladbarer CFRU/DPE-Gen9-BPRE-Kandidat verfügbar ist und die Preflight-Bedingung `candidateSpeciesTotal=1439` erfüllt.
