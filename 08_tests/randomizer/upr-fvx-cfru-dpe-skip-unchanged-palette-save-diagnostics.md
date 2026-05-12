# UPR-FVX CFRU/DPE Skipped Palette Save Diagnostics

Datum: 2026-05-12

## Ziel

Dieser Arbeitsblock prueft einen engen UPR-FVX-Unblocker im Gen3-Pokemon-Palette-Save-Pfad.

Ziel ist nur:

- Fuer konservativ erkannte CFRU/DPE-Gen9-BPRE-Hacks soll `savePokemonPalettes()` unveraenderte Pokemon-Paletten nicht neu schreiben.
- Wild-only-/Coverage-Laeufe sollen nicht mehr am geteilten DPE-Palette-Datenblock `gFrontSprite252Pal` / `0x16b9c08` abbrechen.

Nicht Ziel dieses Branches:

- keine Palette-/Sprite-Randomization-Unterstuetzung
- kein DPE/CFRU-Graphics-Profil
- kein Count-Fix
- kein Moveset-/Learnset-/Trainer-/Static-/Wild-/Starter-Fix
- kein Day/Night-Fix

## Branches und Commits

UPR-FVX:

```text
repo: Planton361/universal-pokemon-randomizer-fvx
base: compat/firered-gen9-cfru-dpe
branch: compat/upr-fvx-cfru-dpe-skip-unchanged-palette-save
commit: 8926912a compat: skip unchanged CFRU DPE palette save
PR: https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/11
```

Workspace:

```text
repo: Planton361/firered-gen9-randomizer-workspace
branch: analysis/upr-fvx-cfru-dpe-skip-unchanged-palette-save
```

## Implementierte technische Entscheidung

`Gen3RomHandler.loadPokemonPalettesDefensively()` merkt fuer den CFRU/DPE-Gen9-BPRE-Modus die geladenen Normal-/Shiny-Palette-Bytes pro `Species`.

`savePokemonPalettes()` prueft in diesem Modus vor dem bestehenden Save-Pfad:

- Wenn alle geladenen Paletten unveraendert sind, wird der Pokemon-Palette-Save uebersprungen.
- Wenn irgendeine Palette geaendert wurde, bleibt der bestehende Save-Pfad aktiv. Damit wird echte Palette-Randomization nicht still als erfolgreich behandelt.
- Vanilla und normale Gen3-Hacks behalten den bisherigen Save-Pfad.

Diagnosemarker:

```text
[CFRU-DPE-PALETTE] skipped unchanged pokemon palette save for CFRU/DPE Gen9 BPRE
```

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
- `./gradlew test`: Gradle beendet mit Exit-Code `0`, meldet aber weiterhin die bekannten bestehenden Test-Failures:
  - `PlayerCharacterGraphicsTest > fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()`
  - `Gen1CmpTest > dummyTest()`
- `./gradlew clean :random:jar`: erfolgreich.

## Lokaler Diagnose-Lauf

Derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand wurde mit Wild-Randomization, `limitPokemon=false`, ohne Gen1-3-Einschraenkung und ohne Trainer-/Moveset-/Palette-/Sprite-Randomization gestartet.

ROM- und Output-Artefakte blieben lokal unter `05_builds/**` und wurden nicht committed.

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-skip-unchanged-palette-save-diagnostics.gba \
  -S "<settings-string>" \
  -z 274269061345319 \
  -l
```

CLI-Exit-Code: `0`.

Der Output-ROM und der Log wurden lokal erzeugt:

```text
upr-fvx-cfru-dpe-skip-unchanged-palette-save-diagnostics.gba
upr-fvx-cfru-dpe-skip-unchanged-palette-save-diagnostics.gba.log
log size: 45726 bytes
```

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

Der defensive Palette-Load bleibt aktiv:

```text
[CFRU-DPE-PALETTE] skipped invalid pokemon palettes during load: normal=2 shiny=2
```

Der unveraenderte Palette-Save wird uebersprungen:

```text
[CFRU-DPE-PALETTE] skipped unchanged pokemon palette save for CFRU/DPE Gen9 BPRE
```

## Palette-Save Vorher/Nachher

Vorheriger Blocker nach Lazy-Trainer-Movesets:

```text
java.lang.IllegalArgumentException: no compressed data found at offset 0x16b9c08
  at compressors.DSDecmp.Decompress(DSDecmp.java:41)
  at Gen3RomHandler.lengthOfCompressedDataAt(...)
  at AbstractGBRomHandler$DataRewriter.rewriteData(...)
  at Gen3RomHandler.rewriteCompressedPalette(...)
  at Gen3RomHandler.savePokemonPalettes(...)
  at AbstractRomHandler.prepareSaveRom(...)
```

Nach dem Skip-Unblocker:

- kein `0x16b9c08`-Abbruch;
- `savePokemonPalettes()` wird fuer unveraenderte CFRU/DPE-Pokemon-Paletten uebersprungen;
- CLI erzeugt Output-ROM und nicht-leeren Wild-Log;
- `Randomized successfully!` wird ausgegeben.

## Wild-Log-Auswertung

Der Wild-Log entsteht wieder. Er bestaetigt, dass Wild-Randomization nach dem Palette-Save-Unblocker wieder bis zur Log-Ausgabe kommt.

Auszug:

```text
Pokemon Palettes: Unchanged
Wild Pokemon: Randomized/Changed

Area #1 - PALLET TOWN Surfing
Cofagrigus Lvs5-10

Area #2 - PALLET TOWN Fishing
Glimmet Lvs15-25

Area #5 - VIRIDIAN CITY Fishing
Magearna Lvs5-15
Hatenna Lvs5-15
Tatsugiri Lvs20-30
```

Beispielhafte Gen7/8/9-Wild-Encounter aus dem Log:

| Generation | Beispiele |
|---|---|
| Gen7 | `Magearna`, `Meltan` |
| Gen8 | `Hatenna`, `Sandaconda`, `Carkol`, `Calyrex` |
| Gen9 | `Glimmet`, `Toedscool`, `Tatsugiri` |

Weitere sichtbare Beispiele:

```text
Toedscool Lv24
Calyrex Lv23
Meltan Lv25
Tatsugiri Lv16
Glimmet Lvs15-25
```

## Technische Interpretation

Der vorherige Save-Blocker war kein Count-, Trainer- oder Learnset-Problem. Er entstand, weil der Gen3-Palette-Save alle geladenen Pokemon-Paletten neu schrieb, obwohl die Settings `Pokemon Palettes: Unchanged` meldeten.

Der kleine Guard ist bewusst konservativ:

- Er greift nur, wenn der CFRU/DPE-Gen9-BPRE-Count-Modus aktiv ist.
- Er greift nur, wenn die geladenen Palette-Bytes unveraendert sind.
- Er laesst geaenderte Paletten in den bestehenden Save-Pfad fallen, statt Palette-Randomization fuer CFRU/DPE vorzutäuschen.

## Risiken

- CFRU/DPE-Pokemon-Palette-Randomization bleibt partial/unsupported.
- Wenn ein Palette-Randomizer spaeter Paletten wirklich aendert, kann der bestehende Save-Pfad weiterhin an geteilten oder anders organisierten DPE-Grafikdaten scheitern.
- Der Grafikpfad nutzt weiterhin `pokedexToInternal[Species.number]`; ein DPE/CFRU-Graphics-Profil bleibt ein spaeteres eigenes Thema.
- Nach diesem Unblocker koennen weitere Save-/Reload-/Write-Pfade sichtbar werden.

## Naechster minimaler Schritt

UPR-FVX PR #11 reviewen. Danach einen Post-Merge-Wild-Smoke auf `compat/firered-gen9-cfru-dpe` dokumentieren und erst danach P1 Static/Gift wieder aufnehmen.
