# 091 - CFRU/DPE Palette Randomization Preserve/Repoint Plan

Datum: 2026-05-14

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

## Ziel

Dieses Protokoll plant read-only den engen P1-Scope fuer echte geaenderte Pokemon-Palette-Randomization im getesteten CFRU/DPE Gen9-BPRE-Stand.

Nicht ausgefuehrt:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- keine Randomizer-Laeufe
- keine Builds
- kein ROM-, Save-, Emulator-State-, Output-ROM-, Log- oder Tool-Binary-Zugriff

## Gelesene Grundlagen

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/058_p1_palette_randomization_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `08_tests/randomizer/upr-fvx-cfru-dpe-defensive-palette-loading-diagnostics.md`
- `08_tests/randomizer/upr-fvx-cfru-dpe-skip-unchanged-palette-save-diagnostics.md`
- `08_tests/randomizer/README.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`

Read-only Codepfade:

- `GameRandomizer.maybeRandomizePokemonPalettes()`
- `Settings.PokemonPalettesMod`
- `RandomizerGUI` Pokemon-Palettes-Controls
- `Bundle.properties` Pokemon-Palettes-Texte
- `Gen3to5PaletteRandomizer`
- `Gen3RomHandler.loadPokemonPalettes()`
- `Gen3RomHandler.savePokemonPalettes()`
- `Gen3RomHandler.rewriteCompressedPalette()`
- `AbstractGBRomHandler.DataRewriter`

## Relevante FVX-Codepfade

### GUI / Settings

Die sichtbare GUI-Gruppe ist `Pokemon Palettes` mit:

- `Unchanged`
- `Random`
- `Follow Types`
- `Follow Evolutions`
- `Shiny From Normal`

`Settings.PokemonPalettesMod` hat nur `UNCHANGED` und `RANDOM`. Die Zusatzflags werden separat gespeichert:

- `pokemonPalettesFollowTypes`
- `pokemonPalettesFollowEvolutions`
- `pokemonPalettesShinyFromNormal`

### Randomizer

`GameRandomizer` initialisiert fuer Gen3 bis Gen5 `Gen3to5PaletteRandomizer` und ruft `paletteRandomizer.randomizePokemonPalettes()` nur auf, wenn `PokemonPalettesMod.RANDOM` gesetzt ist.

`Gen3to5PaletteRandomizer`:

- nutzt `TypeBaseColorList` fuer zufaellige oder type-nahe Farben
- nutzt optional Evolution-Sanity ueber `copyUpEvolutionsHelper`
- kann optional Shiny aus der Normal-Palette ableiten
- liest Palette-Beschreibungen aus `pokePalettes<paletteFilesID>.txt`
- indiziert Palette-Beschreibungen ueber `pk.getNumber() - 1`
- enthaelt selbst TODOs fuer Formen und unterschiedliche/gleiche Form-Paletten

### Gen3 Palette Load/Save

`Gen3RomHandler.loadPokemonPalettes()` nutzt im CFRU/DPE-Gen9-Gate einen defensiven Pfad:

- fehlende oder ungueltige Normal-/Shiny-Palette-Pointer werden nicht geladen
- geladene Normal-/Shiny-Palette-Bytes werden fuer den Skip-Unchanged-Vergleich gemerkt

`Gen3RomHandler.savePokemonPalettes()`:

- ueberspringt im CFRU/DPE-Gate den Pokemon-Palette-Save nur, wenn keine geladene Palette geaendert wurde
- skippt Species mit fehlender geladener Normal- oder Shiny-Palette
- schreibt geaenderte Normal-/Shiny-Paletten ueber `rewriteCompressedPalette(...)`
- nutzt fuer Unown explizite Secondary-Pointer-Offsets, fuer normale Species aber den Single-Pointer-Pfad

`rewriteCompressedPalette(...)` ruft `rewriteCompressedData(...)` auf. Dieser Pfad:

- komprimiert neue Palette-Daten mit LZ10
- bestimmt die alte komprimierte Datenlaenge
- freed den alten Datenblock
- schreibt neue Daten in FreeSpace
- repointet den Primaerpointer
- validiert nur uebergebene Secondary-Pointer

## Bereits stabile Safety-/Skip-Pfade

Die vorhandenen Palette-Fixes sind Safety-Unblocker, keine echte Palette-Randomization-Unterstuetzung.

Stabil belegt:

- defensiver Palette-Load fuer missing/invalid Slots
- Skip von Species mit fehlender geladener Palette
- Skip-Unchanged-`savePokemonPalettes()` fuer unveraenderte CFRU/DPE-Pokemon-Paletten
- `Pokemon Palettes: Unchanged` als sicherer P1-Safety-Pfad

Nicht belegt:

- Schreiben geaenderter CFRU/DPE-Pokemon-Paletten
- Repointing geaenderter Normal-/Shiny-Paletten
- Shared-Palette-Secondary-Pointer-Policy
- Forme-/Alt-Species-Palette-Zuordnung
- `PokemonPalettesMod.RANDOM` mit Reload-Mismatch-Nachweis

## Relevante Datenstrukturen

Fuer den spaeteren Scope relevant:

- `PokemonNormalPalettes` Pointertabelle
- `PokemonShinyPalettes` Pointertabelle
- Normal-Palette pro Species
- Shiny-Palette pro Species
- komprimierte 16-Farb-Palette-Daten
- `pokedexToInternal[pk.getNumber()]` als aktueller Tabellenindex
- geladene Original-Palette-Bytes fuer Skip-Unchanged
- FreeSpace fuer neu komprimierte Palette-Daten
- Primaer- und moegliche Secondary-Pointer auf denselben komprimierten Datenblock

Front-/Back-Sprite-Images sind nicht Teil dieses Scopes. Die Palette-Daten werden zwar fuer Pokemon-Grafikdarstellung genutzt, aber dieser Plan implementiert keine Sprite-/Graphics-Repointing- oder Bilddaten-Logik.

## Hauptrisiken

### Compression

- Der Writer erwartet dekomprimierbare alte Palette-Daten.
- Der bekannte Save-Blocker `no compressed data found` zeigt, dass nicht alle DPE/CFRU-Grafikdaten in die klassische Annahme passen.
- Laengenbestimmung alter komprimierter Daten kann vor dem Repoint scheitern.
- Neue komprimierte Daten koennen groesser sein und brauchen belastbaren FreeSpace.

### Repointing

- Der normale `rewriteCompressedPalette(...)`-Pfad nutzt die Single-Pointer-Annahme.
- Bei Shared-Paletten kann das Freigeben des alten Datenblocks andere Species/Formes treffen.
- Secondary-Pointer werden nur validiert, wenn sie explizit bekannt und uebergeben werden.
- Pointer-Mismatches koennen auch bei scheinbar erfolgreichem Save erst nach Reload sichtbar werden.

### Shared / missing / invalid pointers

- Missing oder invalid Palette-Pointer sind bereits belegt und duerfen nicht als Randomization-Ziele behandelt werden.
- DPE-Gap-/Shared-Pointer-Faelle muessen preserve-only bleiben, bis eine Eigentums-/Secondary-Pointer-Policy existiert.
- `SPECIES_CUBONE_A`-/`gMonPaletteTable[1038]`-Nullslot und zugeordnete Shiny-Faelle bleiben Warnsignale.

### Species-/Forme-Zuordnung

- Der Gen3-Palette-Pfad nutzt weiterhin `pokedexToInternal[pk.getNumber()]`.
- Andere CFRU/DPE-Fixes fuer interne Species-Write-Identitaet loesen diesen Grafikpfad nicht automatisch.
- `Gen3to5PaletteRandomizer` indiziert Palette-Beschreibungen ueber `pk.getNumber() - 1`; das ist nicht automatisch die CFRU/DPE-interne Forme-/Species-Identitaet.
- Moderne Formes und Alt-Species koennen gemeinsame oder fehlende Palette-Daten haben.

### Follow Types / Follow Evolutions / Shiny From Normal

- `Follow Types` darf nicht mit TypeChart, TypeEffectiveness oder Species-Type-Write vermischt werden.
- `Follow Evolutions` darf nicht mit Evolution-Writer-Arbeit vermischt werden.
- `Shiny From Normal` setzt eine sicher geladene Normal-Palette voraus.
- Wenn Normal-Palette fehlt oder invalid ist, darf Shiny nicht daraus erzeugt werden.

## Preserve-/Skip-Policy

Ein spaeterer Fix oder Smoke muss konservativ sein:

1. Unveraenderte Paletten bleiben im bestehenden CFRU/DPE-Skip-Unchanged-Pfad.
2. Missing, invalid oder nicht geladene Normal-/Shiny-Paletten werden nicht geschrieben und nicht neu erzeugt.
3. Shared-Pointer-Faelle bleiben preserve-only, solange keine vollstaendige Secondary-Pointer-Policy vorliegt.
4. Geaenderte Paletten werden nur geschrieben, wenn alter Datenblock dekomprimierbar, single-owner oder vollstaendig secondary-pointer-modelliert ist.
5. Alte komprimierte Daten werden nicht freigegeben, wenn weitere Besitzer nicht ausgeschlossen sind.
6. Repointing ist nur erlaubt, wenn FreeSpace-Quelle, neue Pointer und Reload-Validierung dokumentiert sind.
7. `Follow Types` bleibt rein Palette-Farbwahl und triggert keine TypeChart-/TypeEffectiveness-/Species-Type-Write-Aenderung.
8. `Follow Evolutions` bleibt rein Palette-Farbwahl und triggert keine Evolution-Writer-Aenderung.
9. `Shiny From Normal` wird nur fuer Species mit sicher geladener Normal-Palette bewertet.
10. Sprite-/Graphics-Bilddaten bleiben out of scope.

## Spaetere Reload-/Review-Kriterien

Ein spaeterer Fix- oder Smoke-Block muss mindestens dokumentieren:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `pokemonPalettesMod=RANDOM`
- aktivierte Zusatzflags getrennt: `followTypes`, `followEvolutions`, `shinyFromNormal`
- `changedNormalPalettes`
- `changedShinyPalettes`
- `skippedMissingOrInvalidPalettes`
- `preservedSharedPalettePointers`
- `paletteReloadMismatches=0`
- `palettePointerMismatches=0`, falls Pointer bewusst veraendert werden
- `compressedPaletteDecodeFailures=0`
- `invalidPalettePointersAfter=0`
- `sharedPalettePolicyViolations=0`
- `repointedPalettePointersValid=true`, falls Repointing genutzt wird
- unveraenderte/geskippte Paletten bleiben bytegleich
- `exceptionClass=none`
- `stacktrace=none`

Wenn Repointing bewusst eingefuehrt wird, zusaetzlich:

- Anzahl repointeter Normal-/Shiny-Palette-Pointer
- FreeSpace-Region nur sanitisiert, ohne private Artefaktpfade
- Reload-Vergleich von Pointer-Zielen und dekomprimierten Palette-Bytes
- Nachweis, dass keine nicht modellierten Secondary-Pointer auf freigegebene alte Daten zeigen

## Scope-Grenzen

Dieser Plan trennt klar:

- Palette-Randomization: in scope, aber nur als Plan.
- Graphics/Sprites: out of scope.
- TypeChart/TypeEffectiveness: out of scope.
- Species-Type-Write: out of scope.
- Evolution-Writer: out of scope.
- MoveData / Move Names: out of scope.
- Items / Field / Shops / Pickup: out of scope.
- Trainer, Wild, Evolutions, Text/Menu: out of scope.

## Planentscheidung

Ein direkter Fix fuer echte Palette-Randomization ist noch nicht reviewbar eng genug.

Empfehlung:

1. Zuerst eine zusaetzliche read-only Palette-Pointer-/Compression-Diagnose planen.
2. Diese Diagnose soll ohne Randomizer-Write inventarisieren, welche geladenen Normal-/Shiny-Paletten dekomprimierbar, single-owner, shared, missing oder invalid sind.
3. Erst danach einen engen Fix- oder Smoke-Scope schneiden:
   - entweder nur single-owner/dekomprimierbare Paletten schreiben und alle anderen preserven,
   - oder Repointing mit vollstaendiger Secondary-Pointer-Policy implementieren.

Bis dahin bleiben `FVX-GFX-001` bis `FVX-GFX-004` `Write modelliert`.

## Nicht-Ziele

- keine Palette-Fixumsetzung
- keine Graphics-/Sprite-Umsetzung
- keine TypeChart-/TypeEffectiveness-Arbeit
- keine Species-Type-Write-Arbeit
- keine Evolution-Writer-Arbeit
- keine MoveData-/Move-Names-Arbeit
- keine Items-/Field-/Shops-/Pickup-Arbeit
- keine Trainer-, Wild-, Evolution-, Text/Menu- oder Graphics-Umsetzung
- keine ROM-/Build-/Randomizer-Artefakte
