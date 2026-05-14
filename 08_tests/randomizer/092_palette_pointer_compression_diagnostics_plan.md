# 092 - CFRU/DPE Palette Pointer / Compression Diagnostics Plan

Datum: 2026-05-14

Branch: `analysis/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

## Ziel

Dieser Plan beschreibt eine read-only Diagnose fuer CFRU/DPE Gen9-BPRE Palette-Pointer und komprimierte Normal-/Shiny-Paletten. Der Block plant nur die Klassifikation; er fuehrt keine Randomizer-Laeufe, Builds, ROM-Zugriffe, Writes, Repointing- oder Palette-Randomization-Umsetzung aus.

Die Diagnose soll einen spaeteren engen Fix-/Smoke-Scope vorbereiten, der nur sichere Palette-Faelle behandelt. Unsichere, geteilte, ungueltige oder nicht dekomprimierbare Strukturen bleiben preserve-only.

## Gelesene Grundlagen

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/058_p1_palette_randomization_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `08_tests/randomizer/091_palette_randomization_preserve_repoint_plan.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

## Relevante UPR-FVX-Codepfade

Read-only-Suche bestaetigt folgende Palette-Pfade als relevant:

- `Gen3RomHandler` liest die ROM-Entry-Werte `PokemonNormalPalettes` und `PokemonShinyPalettes` aus Gen3-Pointer-Quellen.
- `loadPokemonPalettes()` und defensive Varianten laden Normal-/Shiny-Paletten pro Pokemon.
- Der Gen3-Palette-Tabellenzugriff nutzt die interne Spezieszuordnung ueber `pokedexToInternal[pk.getNumber()]`.
- Palette-Tabelleneintraege werden im bestehenden Pfad als feste Strukturen mit Pointer-Slot behandelt.
- `savePokemonPalettes()` schreibt Normal- und Shiny-Paletten ueber `rewriteCompressedPalette(...)`.
- `rewriteCompressedPalette(...)` fuehrt in den allgemeinen compressed-data-Rewrite-Pfad.
- `AbstractGBRomHandler.DataRewriter` liest alte Pointer, bestimmt alte compressed length, schreibt neue Daten in Free Space, aktualisiert Pointer und kann alte Datenbereiche freigeben.
- `GameRandomizer` ruft fuer Gen3-5 `Gen3to5PaletteRandomizer` auf, wenn `Settings.PokemonPalettesMod.RANDOM` aktiv ist.
- GUI-/Settings-Pfade enthalten `PokemonPalettesMod.RANDOM`, `Follow Types`, `Follow Evolutions` und `Shiny From Normal`.

## Diagnose-Scope

Die spaetere Diagnose ist ein eigener read-only Block. Sie soll:

- einen lokal explizit freigegebenen CFRU/DPE Gen9-BPRE-Kandidaten laden, ohne private Artefakte zu dokumentieren,
- Normal- und Shiny-Palette-Pointer klassifizieren,
- Dekomprimierbarkeit pruefen,
- Owner-Counts pro Pointer aggregieren,
- sichere Single-Owner-Kandidaten von shared/invalid/missing/decode-failed Eintraegen trennen,
- keine Palette schreiben,
- keine Randomization ausfuehren,
- keine Output-ROM erzeugen,
- keine Pointer, ROM-Namen, Hashes, lokalen Pfade oder Logauszuege dokumentieren.

Die Diagnose trennt ausdruecklich:

- Palette-Pointer-/Compression-Diagnose
- echte Palette-Randomization
- Graphics/Sprites
- TypeChart/TypeEffectiveness
- Species-Type-Write
- Evolution-Writer
- MoveData / Move Names
- Items / Field / Shops / Pickup
- Trainer / Wild / Text/Menu

## Klassifikationsmodell

Pro Palette-Art wird getrennt klassifiziert:

- `normal`: normale Pokemon-Palette
- `shiny`: Shiny-Palette

Pro Palette-Eintrag soll die Diagnose intern bestimmen:

- Tabellenquelle: Normal- oder Shiny-Palette-Tabelle.
- Tabellenindex: UPR-FVX-interner Speziesindex aus dem bestehenden Gen3-Pfad.
- Pointer-Slot vorhanden oder fehlend.
- Pointer-Ziel gueltig innerhalb der geladenen ROM-Daten.
- Pointer-Ziel dekomprimierbar als erwartete Palette-Daten.
- Pointer ist single-owner oder shared.
- Pointer ist Duplicate innerhalb derselben Tabelle.
- Pointer ist Duplicate ueber Normal-/Shiny-Tabellen hinweg.
- Eintrag ist Kandidat fuer spaeteren sicheren Write.
- Eintrag muss preserve-only bleiben.

Raw Pointer-Werte, Offsets, Dateinamen, Hashes und lokale Pfade duerfen nicht in die Dokumentation.

## Geplante Metriken

Mindestmetriken fuer einen spaeteren Diagnose-Lauf:

- `candidateLoaded`
- `palettePointerScanSuccessful`
- `speciesScanned`
- `normalPalettePointersTotal`
- `shinyPalettePointersTotal`
- `normalPaletteDecodeFailures`
- `shinyPaletteDecodeFailures`
- `singleOwnerNormalPalettes`
- `singleOwnerShinyPalettes`
- `sharedNormalPalettes`
- `sharedShinyPalettes`
- `missingNormalPalettePointers`
- `missingShinyPalettePointers`
- `invalidNormalPalettePointers`
- `invalidShinyPalettePointers`
- `duplicateNormalPalettePointers`
- `duplicateShinyPalettePointers`
- `crossKindSharedPalettePointers`
- `candidateWritablePalettes`
- `skipPaletteEntries`
- `skippedSharedPalettes`
- `skippedInvalidPalettes`
- `exceptionClass`
- `stacktrace`

Optional sinnvolle Zusatzmetriken:

- `normalPalettePointerSlotsScanned`
- `shinyPalettePointerSlotsScanned`
- `outOfRomNormalPalettePointers`
- `outOfRomShinyPalettePointers`
- `compressedPaletteDecodeFailures`
- `singleOwnerPaletteCandidates`
- `sharedPaletteClusters`
- `largestSharedPaletteCluster`
- `normalShinyPointerCollisions`
- `decodeSuccessfulWritableCandidates`
- `decodeFailedWritableCandidates`

## Preserve-/Skip-Policy

Die Diagnose bewertet nur, ob ein spaeterer enger Writer ueberhaupt sichere Kandidaten hat. Daraus folgt:

- Missing/null Palette-Pointer: immer skip/preserve.
- Invalid/out-of-ROM Pointer: immer skip/preserve.
- Nicht dekomprimierbare Palette-Daten: immer skip/preserve.
- Shared Pointer: im ersten Fix-Scope preserve-only.
- Cross-kind shared Pointer zwischen Normal und Shiny: preserve-only.
- Duplicate Pointer innerhalb einer Tabelle: preserve-only.
- Single-owner und dekomprimierbare Normal-/Shiny-Paletten: moegliche spaetere Kandidaten.
- Alte compressed Daten duerfen ohne Eigentumsnachweis nicht freigegeben werden.
- Pointer-Updates duerfen spaeter nur fuer eindeutig bekannte Palette-Tabellen erfolgen.
- Unveraenderte oder geskippten Paletten muessen bytegleich erhalten bleiben.

Shared Pointer werden nicht implizit als Fehler bewertet. Sie sind ein Scope-Signal, das spaeter eine eigene Secondary-Pointer-Policy oder bewusstes Preserve erfordert.

## Repoint-/Compression-Risiken

Die groessten Risiken liegen nicht im Farbmodell, sondern in Pointer- und Compression-Eigenschaften:

- Compressed Palette-Daten haben variable Laengen.
- Alter compressed Block und neuer compressed Block koennen unterschiedliche Groessen haben.
- Blindes Ueberschreiben kann Nachbardaten beschaedigen.
- Repointing braucht Free-Space-Auswahl und Reload-Nachweis.
- Shared Pointer koennen mehrere Species/Formes gleichzeitig betreffen.
- Freigabe alter Daten ist nur sicher, wenn alle Owner bekannt sind.
- Gen9-/Forme-/Expanded-Species-Grenzen koennen Mapping- oder Tabellenannahmen brechen.
- Shiny-from-Normal ist unsicher, wenn die Normal-Palette nicht sicher geladen/dekomprimiert wurde.
- Follow Types darf keine TypeChart-/Species-Type-Write-Logik ausweiten.
- Follow Evolutions darf keine Evolution-Writer-Arbeit ausloesen.

## Spaetere Diagnose-/Review-Kriterien

Ein spaeterer Diagnose-Lauf gilt nur als verwertbar, wenn:

- `candidateLoaded=true`
- `palettePointerScanSuccessful=true`
- `normalPalettePointersTotal` dokumentiert ist
- `shinyPalettePointersTotal` dokumentiert ist
- `compressedPaletteDecodeFailures=0` fuer writable candidates gilt
- `singleOwnerPaletteCandidates > 0` oder die Abwesenheit solcher Kandidaten klar als Blocker dokumentiert ist
- `candidateWritablePalettes > 0` oder die Abwesenheit klar als Blocker dokumentiert ist
- `skippedSharedPalettes` dokumentiert ist
- `skippedInvalidPalettes` dokumentiert ist
- `exceptionClass=none`
- `stacktrace=none`
- keine privaten Artefaktwerte dokumentiert sind

Ein spaeterer Fix-/Smoke-Block braucht zusaetzlich:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `paletteReloadMismatches=0`
- `palettePointerMismatches=0` fuer bewusst geaenderte Pointer
- `compressedPaletteDecodeFailures=0` fuer writable candidates
- `invalidPalettePointersAfter=0`
- `sharedPalettePolicyViolations=0`
- `repointedPalettePointersValid=true`, falls Repointing verwendet wird
- unveraenderte/geskippte Paletten bytegleich erhalten
- `exceptionClass=none`
- `stacktrace=none`

## Empfehlung

Empfehlung: Zuerst einen separaten read-only Diagnose-Lauf planen und ausfuehren. Ein direkter Palette-Fix ist noch nicht eng genug, weil Single-Owner-Anteil, Shared-Cluster, Decode-Failures und Pointer-Gueltigkeit fuer den CFRU/DPE Gen9-BPRE-Kandidaten noch nicht klassifiziert sind.

Falls die Diagnose ausreichend viele dekomprimierbare Single-Owner-Kandidaten findet, ist danach ein enger Fix-/Smoke-Scope realistisch:

- nur Single-Owner Normal-/Shiny-Paletten,
- nur dekomprimierbare Kandidaten,
- shared/invalid/missing/decode-failed preserve-only,
- Repointing nur mit Free-Space- und Reload-Nachweis.

Falls keine sicheren Kandidaten gefunden werden oder Shared-/Compression-Risiken dominieren, sollte echte Palette-Randomization vorerst zurueckgestellt und erst eine Pointer-/Owner-Policy modelliert werden.
