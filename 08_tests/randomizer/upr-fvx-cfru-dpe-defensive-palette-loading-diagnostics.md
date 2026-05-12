# UPR-FVX CFRU/DPE Defensive Palette Loading Diagnostics

Datum: 2026-05-12

## Ziel

Dieser Arbeitsblock prueft den isolierten UPR-FVX-Fix fuer defensives Pokemon-Palette-Loading/-Saving bei konservativ erkannten CFRU/DPE-Gen9-BPRE-Hacks.

Der Branch aendert keine Count-, Moveset-, Trainer-, Learnset-, Static/Gift-, Starter-, Evolution-, TM/Tutor-, Ability- oder Day/Night-Logik.

## Branches und Commits

UPR-FVX:

```text
repo: Planton361/universal-pokemon-randomizer-fvx
base: d17b29a2 compat: detect CFRU DPE Gen9 species count
branch: compat/upr-fvx-cfru-dpe-defensive-palette-loading
commit: 17e47254 compat: tolerate CFRU DPE missing pokemon palettes
PR: https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/9
```

Workspace:

```text
repo: Planton361/firered-gen9-randomizer-workspace
branch: analysis/upr-fvx-cfru-dpe-defensive-palette-loading
```

## Implementierte technische Entscheidung

`Gen3RomHandler.loadPokemonPalettes()` bleibt fuer Vanilla und normale Gen3-Hacks unveraendert streng.

Nur wenn der bestehende CFRU/DPE-Gen9-Count-Modus aktiv ist:

- liest FVX Normal-/Shiny-Palette-Pointer defensiv;
- fehlende, nullinitialisierte oder ungueltige Palette-Slots brechen den ROM-Load nicht mehr ab;
- betroffene Species behalten `null` fuer die nicht geladene Palette;
- `savePokemonPalettes()` ueberspringt Species mit fehlender geladener Normal- oder Shiny-Palette und schreibt keine neuen Pointer fuer diese Slots.

Die Diagnoseausgabe ist kompakt mit `[CFRU-DPE-PALETTE]` markiert.

## UPR-FVX Checks

```sh
git status --short
git diff --stat
git diff --check
./gradlew test
./gradlew clean :random:jar
```

Ergebnis:

- `git diff --check`: ohne Befund.
- `./gradlew test`: Gradle beendet mit Exit-Code `0`, meldet aber die bekannten bestehenden Test-Failures:
  - `PlayerCharacterGraphicsTest > fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()`
  - `Gen1CmpTest > dummyTest()`
- `./gradlew clean :random:jar`: erfolgreich.

## Lokaler Diagnose-Lauf

Derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand wurde mit Wild-Randomization, `limitPokemon=false`, ohne Gen1-3-Einschraenkung und ohne Palette-/Sprite-Randomization gestartet.

ROM- und Output-Artefakte blieben lokal unter `05_builds/**` und wurden nicht committed.

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-defensive-palette-loading-diagnostics.gba \
  -S "<settings-string>" \
  -z 274269061345319 \
  -l
```

CLI-Exit-Code: `0`.

Wichtig: Der CLI meldet trotz internem Save-Fehler `Randomized successfully!`; der Fehler wurde deshalb zusaetzlich lokal ueber `GameRandomizer.Results` ausgelesen.

## Palette-Loader Vorher/Nachher

Vorher:

```text
java.lang.IllegalArgumentException: No valid pointer at 0x1a495d8.
  at Gen3RomHandler.loadPokemonPalettes(...)
```

Nachher:

```text
[CFRU-DPE-PALETTE] skipped invalid pokemon palettes during load:
normal=2 shiny=2
```

Belegte Beispiele:

| Art | Name | Identity | Tabellenindex | Pointer-Slot | Grund |
|---|---:|---:|---:|---:|---|
| normal | Cubone | `1038` | `1038` | `0x1A495D8` | invalid pointer |
| shiny | Cubone | `1038` | `1038` | `0x1A57F1C` | invalid pointer |
| normal | Oricorio | `1043` | `1038` | `0x1A495D8` | invalid pointer |
| shiny | Oricorio | `1043` | `1038` | `0x1A57F1C` | invalid pointer |

Interpretation:

- Der bekannte `SPECIES_CUBONE_A`-/`gMonPaletteTable[1038]`-Nullslot bricht den Load nicht mehr ab.
- Dass `Oricorio` ebenfalls ueber Tabellenindex `1038` laeuft, bestaetigt das bereits dokumentierte Dex-/`pokedexToInternal`-Mapping-Risiko im Grafikpfad. Dieser Branch behebt dieses Mapping bewusst nicht.

## Count und Generation-Coverage

Die Count-/Species-Diagnose bleibt stabil:

```text
PokemonCount=1439
pokedexCount=1290
speciesList.size=1415
maxInternalSpeciesId=1439
maxSpeciesNumber=1290
maxSpeciesIdentityNumber=1439
generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Vorheriger Zustand:

- vor Gen9-Count-Fix: `PokemonCount=823`, keine Gen7/8/9 im FVX-Species-Load;
- nach Gen9-Count-Fix, vor Palette-Fix: `PokemonCount=1439`, Gen7/8/9 sichtbar, aber Abbruch in `loadPokemonPalettes()`;
- nach Palette-Fix: `PokemonCount=1439`, Gen7/8/9 sichtbar, Palette-Load bricht nicht mehr ab.

## Wild-Log-Auswertung

In diesem Lauf wurde kein neuer nutzbarer Wild-Log erzeugt. Der Palette-Load ist entblockt, aber der anschliessende Save bricht vor `logger.logResults()` in einem separaten Trainer/Learnset-Pfad ab:

```text
java.lang.IllegalArgumentException: No valid pointer at 0x25e49c.
  at Gen3RomHandler.readPointer(...)
  at Gen3RomHandler.getMovesLearnt(...)
  at Gen3RomHandler.trainerPokemonToBytes(...)
  at Gen3RomHandler.saveTrainers(...)
```

Damit gibt es in diesem Arbeitsblock keine neuen sichtbaren Gen7/8/9-Wild-Encounter-Beispiele. Der Befund ist trotzdem eindeutig fuer den Scope dieses Branches: fehlende Palette-Slots blockieren den ROM-Load nicht mehr; der naechste Blocker liegt nachgelagert im Trainer-/Learnset-Save-Pfad.

## Risiken

- Pokemon-Palette-Randomization fuer CFRU/DPE bleibt partial/unsupported fuer Species/Formes ohne gueltig geladene Paletten.
- Der Palette-Pfad nutzt weiterhin `pokedexToInternal[Species.number]`; die semantisch saubere DPE/CFRU-Grafikzuordnung bleibt ein spaeteres eigenes Profilthema.
- `savePokemonPalettes()` wurde defensiv gemacht, wurde im lokalen End-to-End-Lauf aber nicht erreicht, weil `saveTrainers()` vorher am Learnset-Pointer stoppt.
- Movesets/Learnsets/Trainer-Save sind separate P1/P1-Learnset-Themen und wurden nicht veraendert.

## Naechster minimaler Schritt

UPR-FVX PR #9 reviewen. Danach den neuen nachgelagerten Blocker `saveTrainers()`/`getMovesLearnt()` fuer `PokemonCount=1439` separat modellieren oder diagnostizieren, ohne Palette-, Count-, Static/Gift- oder Wild-Fixes zu vermischen.
