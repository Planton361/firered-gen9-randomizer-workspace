# 093 - CFRU/DPE Palette Pointer / Compression Diagnostics

Datum: 2026-05-14

Branch: `test/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

## Ziel

Dieser Diagnose-Lauf klassifiziert read-only CFRU/DPE Gen9-BPRE Normal-/Shiny-Palette-Pointer und komprimierte Palette-Daten. Der Lauf erzeugt keine Output-ROM, schreibt keine Palette, fuehrt keine Palette-Randomization aus und verwendet kein Repointing.

Alle Ergebnisse sind sanitisiert. Dokumentiert werden nur aggregierte Zaehler. Keine privaten Pfade, ROM-Namen, Hashes, Raw Pointer, Offsets, Logauszuege, Output-ROM-Pfade, Tool-Binaries, Secrets, Tokens oder `.env`-Inhalte werden dokumentiert.

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
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

## Diagnosemethode

Der lokale Lauf verwendete einen ignored Diagnose-Harness unter `05_builds/**`. Der Harness wurde nicht committed.

Vorgehen:

- lokale Kandidaten read-only pruefen,
- nur einen BPRE-/CFRU-DPE-Gen9-nahe erkannten Kandidaten fuer die Pointer-Klassifikation verwenden,
- Normal- und Shiny-Palette-Tabellen getrennt scannen,
- Pointer-Slots klassifizieren,
- LZ10-Dekomprimierbarkeit auf erwartete 16-Farb-/32-Byte-Palette pruefen,
- Owner-Counts pro Pointer aggregieren,
- Single-owner, shared, missing/null, invalid/out-of-ROM, duplicate und cross-kind shared zaehlen,
- keine Palette schreiben,
- keine alte komprimierte Palette freigeben oder ueberschreiben,
- keine Output-ROM erzeugen.

Der Lauf ist bewusst ein raw-read-only Pointer-/Compression-Scan und kein Randomizer-Run.

## Kandidaten-/Preflight-Ergebnis

```text
candidateFilesChecked=94
candidateLoaded=true
palettePointerScanSuccessful=true
candidateSpeciesTotal=1439
exceptionClass=none
stacktrace=none
```

Interpretation:

- Ein lokal freigegebener BPRE-/CFRU-DPE-Gen9-nahe Kandidat wurde fuer die aggregierte Pointer-Diagnose geladen.
- Der Scan blieb read-only.
- Keine privaten Artefaktwerte wurden dokumentiert.

## Diagnose-Metriken

```text
normalPalettePointersTotal=1439
shinyPalettePointersTotal=1439
normalPaletteDecodeFailures=313
shinyPaletteDecodeFailures=312
normalPaletteDecodeSuccesses=1031
shinyPaletteDecodeSuccesses=592
singleOwnerNormalPalettes=919
singleOwnerShinyPalettes=535
sharedNormalPalettes=192
sharedShinyPalettes=137
missingNormalPalettePointers=1
missingShinyPalettePointers=37
invalidNormalPalettePointers=94
invalidShinyPalettePointers=498
duplicateNormalPalettePointers=192
duplicateShinyPalettePointers=137
crossKindSharedPalettePointers=1809
sharedPointerGroups=775
largestSharedPointerGroupSize=156
singleOwnerBothNormalAndShinySpecies=0
candidateWritablePalettes=385
candidateWritableNormalPalettes=385
candidateWritableShinyPalettes=0
skipPaletteEntries=2493
skippedSharedPalettes=329
skippedInvalidPalettes=592
skippedMissingPalettes=38
skippedDecodeFailedPalettes=625
```

## Preserve-/Skip-Einordnung

Direkt preserve-only:

- `sharedNormalPalettes=192`
- `sharedShinyPalettes=137`
- `missingNormalPalettePointers=1`
- `missingShinyPalettePointers=37`
- `invalidNormalPalettePointers=94`
- `invalidShinyPalettePointers=498`
- `normalPaletteDecodeFailures=313`
- `shinyPaletteDecodeFailures=312`
- `crossKindSharedPalettePointers=1809`

Skip-/Preserve-Gesamt:

```text
skipPaletteEntries=2493
skippedSharedPalettes=329
skippedInvalidPalettes=592
skippedMissingPalettes=38
skippedDecodeFailedPalettes=625
```

Shared Pointer sind kein automatischer Fehler, aber sie sind fuer einen ersten Fix nicht direkt beschreibbar. Cross-kind shared Pointer sind besonders riskant, weil Normal-/Shiny-Tabellen denselben komprimierten Datenblock beruehren koennen.

## Fix-Kandidaten-Einschaetzung

Sichere Kandidaten nach Diagnose-Policy:

```text
candidateWritablePalettes=385
candidateWritableNormalPalettes=385
candidateWritableShinyPalettes=0
singleOwnerBothNormalAndShinySpecies=0
```

Ein spaeterer enger Fix-/Smoke-Scope ist nur fuer dekomprimierbare Single-owner-Paletten realistisch. Der aktuelle Befund spricht gegen einen breiten `PokemonPalettesMod.RANDOM`-Fix, weil keine Species gleichzeitig sichere Normal- und Shiny-Kandidaten hat.

Konservativer naechster Scope:

- Normal-Palette-only Single-owner/decompressible Proof-of-Scope planen.
- Shiny-Paletten im ersten Fix preserve-only halten.
- Shared, invalid, missing und decode-failed Paletten nicht schreiben.
- Keine alte komprimierte Palette freigeben, solange Owner nicht eindeutig single-owner sind.
- Kein Repointing ohne eigenen Free-Space- und Reload-Nachweis.

## Feature-Status

- `FVX-GFX-001` bleibt `Write modelliert`.
- `FVX-GFX-002` bleibt `Write modelliert`.
- `FVX-GFX-003` bleibt `Write modelliert`.
- `FVX-GFX-004` bleibt `Write modelliert`.
- Keine Hochstufung auf `GUI-kompatibel` in diesem Diagnose-Lauf.

## Risiken / Annahmen

- Der Diagnose-Lauf klassifiziert Pointer und Compression, beweist aber keinen Writer.
- `candidateWritablePalettes=385` ist ein enger Kandidatenpool, kein GUI-Support.
- `candidateWritableShinyPalettes=0` blockiert einen vollstaendigen Normal+Shiny-Palette-Randomization-Fix.
- `crossKindSharedPalettePointers=1809` zeigt, dass eine naive Single-Pointer-Rewrite-Strategie zu riskant ist.
- `largestSharedPointerGroupSize=156` macht Shared-Pointer-Policy oder Preserve zwingend.
- Ein spaeterer Fix muss weiter strikt von Graphics/Sprites, TypeChart/TypeEffectiveness, Species-Type-Write, Evolution-Writer, MoveData, Move Names, Items, Field/Shops/Pickup, Trainer, Wild und Text/Menu getrennt bleiben.

## Ergebnis

Die read-only Diagnose findet einen kleinen, realen Single-owner/decompressible Kandidatenpool fuer Normal-Paletten. Shiny-Paletten sind in diesem Kandidatenstand nicht als direkt writable klassifiziert. Ein naechster Fix-/Smoke-Scope ist deshalb nur als normal-palette-only, single-owner/decompressible, preserve-everything-else realistisch. Breite Palette-Randomization bleibt nicht freigegeben.
