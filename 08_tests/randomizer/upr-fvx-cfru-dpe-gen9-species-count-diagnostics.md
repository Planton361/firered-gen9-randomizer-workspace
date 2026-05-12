# UPR-FVX CFRU/DPE Gen9 Species Count Diagnostics

Datum: 2026-05-12

## Ziel

Dieser Arbeitsblock prueft den konservativen CFRU/DPE-BPRE-spezifischen SpeciesCount-Fix fuer UPR-FVX. Der Fix soll `PokemonCount` im lokalen CFRU/DPE-Gen9-Teststand nicht mehr durch `PokemonMovesets` oder `PokedexOrder` auf Gen6/Teilbereiche kappen, wenn `PokemonNames` und BaseStats den DPE-Gen9-Umfang plausibel belegen.

Keine Static-/Gift-, Trainer-, Learnset-, Moveset-, Wild-, Day/Night- oder GenRestrictions-Fixes wurden umgesetzt.

## Branches und Commits

UPR-FVX:

```text
repo: Planton361/universal-pokemon-randomizer-fvx
base: compat/firered-gen9-cfru-dpe
branch: compat/upr-fvx-cfru-dpe-gen9-species-count
commit: d17b29a2 compat: detect CFRU DPE Gen9 species count
PR: https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/8
```

Workspace:

```text
repo: Planton361/firered-gen9-randomizer-workspace
branch: analysis/upr-fvx-cfru-dpe-gen9-species-count
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
- `./gradlew test`: Gradle beendet mit Exit-Code `0`, meldet aber bestehende Test-Failures in `PlayerCharacterGraphicsTest > fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` und `Gen1CmpTest > dummyTest()`.
- `./gradlew clean :random:jar`: erfolgreich.

## Implementierte technische Entscheidung

Der Fix ist auf konservativ erkannte CFRU/DPE-Gen9-BPRE-Hacks begrenzt:

- ROM-Code `BPRE`
- ROM-Hack-Erkennung aktiv
- Name-Scan erreicht mindestens interne ID `1439`
- erwartete Sentinel-Namen sind vorhanden:
  - ID `824`: `Xerneas`
  - ID `1000`: `Hakamo-o`
  - ID `1294`: `Sprigatito`
  - ID `1439`: `Pecharunt`
- BaseStats fuer diese Sentinel-IDs sind plausibel.

Nur in diesem Modus:

- bleibt `PokemonCount` beim aus `PokemonNames` plus BaseStats-Sanity abgeleiteten Count;
- `PokemonMovesets` kappt den Count nicht mehr auf `930`;
- `PokedexOrder > 1023` kappt den Count nicht mehr auf `823`;
- `PokedexOrder` wird weiterhin gelesen, aber uebergrosse Werte werden in diesem Modus nicht in `pokedexToInternal` indiziert.

Vanilla und nicht passende Gen3-Hacks bleiben auf der bestehenden Heuristik.

## Lokaler Diagnose-Lauf

Der lokale CFRU/DPE-Teststand wurde mit demselben ROM-/Settings-Profil wie die vorherige Count-Cutoff-Diagnose gestartet. ROM- und Output-Artefakte blieben lokal unter `05_builds/**` und wurden nicht committed.

CLI-Lauf:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-gen9-species-count-diagnostics.gba \
  -S "<settings-string>" \
  -z 274269061345319 \
  -l
```

Exit-Code: `1`.

Der Count-Fix greift vor dem Abbruch:

```text
[temporary CFRU/DPE species diagnostics] using PokemonNames+BaseStats PokemonCount=1439; skipped Moveset/PokedexOrder count caps for CFRU/DPE Gen9 BPRE
[temporary CFRU/DPE species diagnostics] PokemonCount=1439 pokedexCount=1290 speciesList.size=1415 maxInternalSpeciesId=1439 maxSpeciesNumber=1290 maxSpeciesIdentityNumber=1439
[temporary CFRU/DPE species diagnostics] generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Danach bricht das vollstaendige Laden in einem separaten Tabellenpfad ab:

```text
java.lang.IllegalArgumentException: No valid pointer at 0x1a495d8.
  at com.uprfvx.romio.romhandlers.Gen3RomHandler.loadPokemonPalettes(...)
```

## Count Vorher/Nachher

| Wert | Vorher | Nachher |
|---|---:|---:|
| Name-Scan | `1439` | `1439` |
| nach Moveset-Check | `930` | nicht als Count-Grenze genutzt |
| nach PokedexOrder-Check | `823` | nicht als Count-Grenze genutzt |
| finaler `PokemonCount` | `823` | `1439` |
| `speciesList.size` | `799` | `1415` |
| `maxSpeciesIdentityNumber` | `823` | `1439` |

## Generation-Coverage

Vorheriger P0-Post-Merge-Smoke mit `PokemonCount=823`:

```text
Gen1 354, Gen2 388, Gen3 404, Gen4 398, Gen5 528, Gen6 104, Gen7 0, Gen8 0, Gen9 0
```

Nach dem Count-Fix beim Species-Load:

```text
generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Damit sind Gen7, Gen8 und Gen9 im FVX-Species-Load sichtbar.

## Wild-Log-Auswertung

Der Lauf erreicht die Wild-Randomization nicht. Nach erfolgreichem Species-Load bricht der ROM-Load in `loadPokemonPalettes()` ab. Deshalb gibt es in diesem Arbeitsblock keinen neuen Wild-Log und keine sichtbaren Gen7/8/9-Wild-Encounter-Beispiele.

Der Abbruch ist ein separater Kompatibilitaetsbefund: Mit `PokemonCount=1439` werden weitere Tabellenpfade sichtbar, die noch auf `pokedexToInternal[Species.number]` und alte Gen3-Tabellenannahmen angewiesen sind. Dieser Branch behebt diesen Palettenpfad bewusst nicht.

## Technische Interpretation

Der urspruengliche `PokemonCount=823`-Cutoff ist fuer CFRU/DPE geloest: `PokedexOrder` und Moveset-Pointer blockieren den Count nicht mehr, solange die konservative CFRU/DPE-Gen9-Erkennung greift.

Die naechste Blockade liegt nicht mehr in `basicBPRE10HackSupport()`, sondern beim vollstaendigen Laden nach `loadSpeciesStats()`. `loadPokemonPalettes()` verwendet weiterhin Dex-/Pokedex-basierte Indizes und liest fuer den erweiterten CFRU/DPE-Speciesraum einen ungueltigen Pointer.

Moveset-Pointer bleiben ein separates Thema. Der Count-Fix nutzt Movesets nicht als Count-Grenze, repariert aber keine Learnsets oder Moveset-Tabellen.

## Risiken

- Die Erkennung ist bewusst eng auf den aktuellen englischen CFRU/DPE-Gen9-BPRE-Teststand zugeschnitten.
- Pokedex-/Dex-ID-Mapping ist weiterhin nicht voll modelliert.
- Paletten, Movesets, Trainer, Static/Gifts, Evolutions, Learnsets, TM/Tutor und weitere P1/P2-Pfade koennen mit `PokemonCount=1439` neue Folgefehler zeigen.
- Der lokale Wild-Randomizer-Smoke ist noch nicht wieder erfolgreich, weil der Palettenpfad vorher abbricht.

## Naechster minimaler Schritt

UPR-FVX PR #8 reviewen. Danach in einem separaten Analyse-/Fixbranch den naechsten Loader-Blocker `loadPokemonPalettes()` fuer erweiterte CFRU/DPE-BPRE-Hacks modellieren, ohne Movesets, Static/Gifts oder Trainer-Fixes zu vermischen.
