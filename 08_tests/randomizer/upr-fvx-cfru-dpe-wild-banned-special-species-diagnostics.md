# UPR-FVX CFRU/DPE Wild Banned Special Species Diagnostics

Datum: 2026-05-12

## Ziel

Dieser Arbeitsblock bestaetigt den kleinen CFRU/DPE-spezifischen Wild-Ban fuer belegte nicht-wild-taugliche Sonder-Species.

Keine Count-, Palette-, Moveset-, Trainer-, Static-, Starter- oder Day/Night-Fixes wurden umgesetzt.

## UPR-FVX Stand

```text
repo: Planton361/universal-pokemon-randomizer-fvx
base: compat/firered-gen9-cfru-dpe
branch: compat/upr-fvx-cfru-dpe-wild-banned-special-species
commit: 0f127e9b compat: ban CFRU DPE special species from wild pool
PR: https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/12
```

## Code-Aenderung

Geaendert wurde nur:

```text
02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java
```

Der bestehende FRLG-Unown-Ban bleibt unveraendert. Zusaetzlich werden nur im erkannten CFRU/DPE-Gen9-BPRE-Modus die belegten internen Sonder-Species aus dem Wild-Banned-Set entfernt:

```text
SPECIES_NONE = 0
SPECIES_EGG  = 0x19C
```

FVX hat keine `SpeciesIDs.egg`-/`badEgg`-Konstante. Der Patch nutzt deshalb den aus DPE/CFRU belegten internen Wert `0x19C` nur hinter dem vorhandenen CFRU/DPE-Gen9-BPRE-Erkennungsflag `useCfruDpeGen9SpeciesCount`.

Weitere Dummy-/Gap-Slots wurden nicht gebannt, weil sie in der aktuellen Diagnose nicht sicher genug als nicht-wild-taugliche konkrete interne IDs belegt waren.

## Checks UPR-FVX

```sh
git status --short
git diff --stat
git diff --check
./gradlew test
./gradlew clean :random:jar
```

Ergebnisse:

- `git diff --check`: ok
- `./gradlew clean :random:jar`: `BUILD SUCCESSFUL`
- `./gradlew test`: Gradle beendet mit Exit-Code `0` / `BUILD SUCCESSFUL`, die Testreports melden aber weiterhin zwei bestehende Failures:
  - `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE`
  - `Gen1CmpTest.dummyTest`

Diese Test-Failures liegen ausserhalb des geaenderten Wild-Ban-Pfads.

## Lokaler Diagnose-Lauf

Derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand wurde mit dem Bad-Egg-Diagnose-Seed gestartet:

```text
seed=274269061345319
```

Settings:

- Wild-Randomization aktiv
- `limitPokemon=false`
- keine Gen1-3-Einschraenkung
- Trainer/Starter/Evos/Learnsets/TM/Tutor/Abilities aus
- Palette-/Sprite-Randomization aus

ROM- und Output-Artefakte blieben lokal unter `05_builds/**` und wurden nicht committed.

CLI-Ergebnis:

```text
Randomized successfully!
saveSuccessful=true
```

## Species-Coverage

Die Species-Coverage bleibt stabil:

```text
PokemonCount=1439
pokedexCount=1290
speciesList.size=1415
maxInternalSpeciesId=1439
maxSpeciesNumber=1290
maxSpeciesIdentityNumber=1439
generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Die bestehenden CFRU/DPE-Unblocker bleiben aktiv:

```text
[CFRU-DPE-PALETTE] skipped invalid pokemon palettes during load: normal=2 shiny=2
[CFRU-DPE-PALETTE] skipped unchanged pokemon palette save for CFRU/DPE Gen9 BPRE
```

## Bad Egg vorher/nachher

| Befund | Vorher | Nachher |
|---|---:|---:|
| `Bad Egg` | 12 | 0 |
| `<unknown>` | 0 | 0 |
| `saveSuccessful` | true | true |

Vorher lagen alle `12` `Bad Egg`-Eintraege in `Area #174 - ALTERING CAVE Grass/Cave`, Slots 1-12.

Nachher enthaelt dieselbe Area keine `Bad Egg`-Eintraege mehr:

```text
Area #174 - ALTERING CAVE Grass/Cave (rate=5)
Meowscrada Lv22
Meowscrada Lv24
Meowscrada Lv20
Meowscrada Lv26
Meowscrada Lv22
Meowscrada Lv24
Meowscrada Lv28
Meowscrada Lv18
Meowscrada Lv20
Meowscrada Lv26
Meowscrada Lv20
Meowscrada Lv26
```

## Wild-Log-Auswertung

Ausgewertet wurden `2176` sichtbare Wild-Slots.

Generation-Auswertung des Logs:

| Generation | Wild-Slots |
|---|---:|
| Gen1 | 644 |
| Gen2 | 61 |
| Gen3 | 281 |
| Gen4 | 122 |
| Gen5 | 214 |
| Gen6 | 249 |
| Gen7 | 92 |
| Gen8 | 101 |
| Gen9 | 412 |

Beispielhafte Gen7-Wild-Encounter:

```text
Silvally
Cosmoem
```

Beispielhafte Gen8-Wild-Encounter:

```text
Snom
Cramorant
Sandaconda
```

Beispielhafte Gen9-Wild-Encounter:

```text
Farigiraf
Hydrapple
Tadbulb
Grafaiai
Flamigo
Meowscrada
```

## Technische Entscheidung

Der Fix ist absichtlich enger als ein allgemeiner Dummy-/Gap-Filter:

- kein Ban nach Namen wie `?` oder `Bad Egg`
- kein globaler `SpeciesIDs`-Eintrag fuer Egg
- kein Eingriff in `RestrictedSpeciesService`
- kein Eingriff in die Randomizer-Pool-Mechanik
- kein Eingriff in Vanilla/normal Gen3

Der Wild-Ban nutzt die bereits vorhandene CFRU/DPE-Gen9-BPRE-Erkennung, weil nur dieser Modus den vollstaendigen DPE-internen Speciesraum als Wild-Pool nutzt.

## Risiken

- Weitere DPE/CFRU-Dummy-/Gap-Slots koennen spaeter sichtbar werden; sie wurden hier nicht spekulativ gebannt.
- Altering Cave bleibt im Encounter-Systemmodell partial/unsupported. Dieser Fix bestaetigt nur, dass `SPECIES_EGG` nicht mehr als Standard-/Fallback-Wild-Replacement erscheint.
- `./gradlew test` meldet weiterhin bestehende Testreport-Failures trotz Gradle-Exit-Code `0`; diese sollten separat eingeordnet werden.

## Ergebnis

Der konkrete `Bad Egg`-Befund ist fuer den bestaetigten Gen9-Standard-/Fallback-Wild-Smoke behoben:

- `Bad Egg=0`
- `<unknown>=0`
- `saveSuccessful=true`
- Gen7/8/9 bleiben im Wild-Log sichtbar
