# 095 - CFRU/DPE Palette Normal Single-owner Write Guard Fix Diagnostics

Datum: 2026-05-14

Workspace-Branch: `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`

UPR-FVX-Fix-Commit: `2697511da9a97df4c29c00dfda8b40e556020489`

UPR-FVX PR: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/35`

## Ziel

Enger UPR-FVX-Fix fuer `FVX-GFX-001` als Normal-only-Farbtraeger. Der CFRU/DPE-Gen9-BPRE-Palette-Writer darf nur sichere Normal-Palette-Kandidaten in den komprimierten Rewriter geben.

Der Fix ist kein vollstaendiger Palette-Randomization-Fix und kein Shiny-/Shared-/Graphics-/Sprite-Scope.

## Fix-Erklaerung

Geaenderter UPR-FVX-Pfad:

- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

Der CFRU/DPE-Pfad in `savePokemonPalettes()` verzweigt nun in einen eigenen Normal-only-Guard:

- Shiny-Paletten werden im CFRU/DPE-Palette-Randomization-Scope nicht geschrieben.
- Normal-Paletten werden nur geschrieben, wenn der Pointer vorhanden, gueltig, decode-success, single-owner, non-shared und non-cross-kind ist.
- Unveraenderte Normal-Paletten werden nicht neu geschrieben.
- Shared, missing/null, invalid/out-of-ROM, decode-failed, duplicate/cross-kind shared und unsichere Forme-Faelle werden nicht an `rewriteCompressedPalette()` / `DataRewriter` uebergeben.
- `Unown`/Forme-Sonderpfade bleiben im CFRU/DPE-Gate preserve-only.

Der Vanilla-/Nicht-CFRU-Pfad bleibt beim bisherigen Normal+Shiny-Write-Verhalten.

## Writer-Policy

Write-only:

- Normal-Palette
- single-owner
- decode-success
- gueltiger Pointer
- non-shared
- non-cross-kind
- keine unsichere Forme-/Expanded-Mapping-Situation

Skip/preserve:

- alle Shiny-Paletten
- shared Pointer
- missing/null Pointer
- invalid/out-of-ROM Pointer
- decode-failed Paletten
- duplicate/cross-kind shared Pointer
- unsichere Forme-/Expanded-Mapping-Faelle

## Smoke-Ergebnis

Kein ROM-/Reload-Smoke wurde in diesem Block ausgefuehrt.

Grund:

- Der Fix wurde implementiert und mit nicht-ROM-Checks gebaut.
- Ein sanitisiert dokumentierbarer lokaler CFRU/DPE Gen9-BPRE-Reload-Smoke wurde in diesem Arbeitsblock nicht gestartet.
- Es wurden keine ROMs, Saves, Logs, Output-ROMs, privaten Pfade, ROM-Namen, Hashes, Pointer oder Offsets dokumentiert.

Die fachliche Reload-Bestaetigung bleibt ein separater Folgeblock.

## Erwartete spaetere Reload-/Mismatch-Zaehler

Ein spaeterer Smoke soll mindestens pruefen:

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
- `preservedSkippedPaletteByteMismatches=0`
- `repointedPalettePointersValid=true`, falls Repointing stattfindet
- `compressedPaletteDecodeFailuresAfter=0` fuer geschriebene Kandidaten
- `exceptionClass=none`
- `stacktrace=none`

## Feature-Status

- `FVX-GFX-001` bleibt nach diesem Code-/Build-Fix konservativ `Write modelliert`, bis ein Reload-Smoke den Normal-only-Single-owner-Subset bestaetigt.
- `FVX-GFX-002` bleibt `Write modelliert`.
- `FVX-GFX-003` bleibt `Write modelliert`.
- `FVX-GFX-004` bleibt `Write modelliert`.

Eine spaetere Hochstufung fuer `FVX-GFX-001` waere maximal `Getestet` fuer das explizite Normal-only-Single-owner-Subset, nicht voll `GUI-kompatibel`.

## Checks

UPR-FVX:

- `git status --short`: nur `Gen3RomHandler.java` vor Commit geaendert
- `git diff --stat`: eine eng betroffene Datei
- `git diff --check`: sauber
- `./gradlew test`: Gradle beendet mit Status 0, meldet aber bestehende Failures in `PlayerCharacterGraphicsTest` und `Gen1CmpTest`
- `./gradlew clean :random:jar`: erfolgreich

Workspace:

- Submodule wird auf `2697511da9a97df4c29c00dfda8b40e556020489` gepinnt.

## Risiken / Annahmen

- Ohne Reload-Smoke ist noch nicht belegt, dass `normalPaletteWriteCandidates=385` im Writer-Lauf exakt erreicht wird.
- Repointing bleibt ein komprimierter DataRewriter-Pfad und braucht im spaeteren Smoke Pointer-/Reload-Nachweis.
- Der Fix schuetzt Shiny/shared/invalid/missing/decode-failed/cross-kind Faelle dadurch, dass sie nicht an den Rewriter uebergeben werden.
- Bestehende externe Test-Failures wurden nicht in diesem Scope behoben.

## Ergebnis

Der UPR-FVX-Fix ist implementiert und gebaut. Der Workspace pinnt den neuen Fix-Commit und dokumentiert, dass die fachliche Reload-Bestaetigung als separater Smoke nachzuholen ist.
