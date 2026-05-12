# UPR-FVX CFRU/DPE Gen9 Wild Post-Merge Smoke

Datum: 2026-05-12

## Ziel

Dieser Arbeitsblock bestaetigt die gemergte Gen9-Wild-only-Fixkette auf dem UPR-FVX-Zielbranch `compat/firered-gen9-cfru-dpe`.

Keine Codeaenderungen, keine neuen Fixes und keine ROM-/Build-Artefakte wurden committed.

## UPR-FVX Stand

```text
repo: Planton361/universal-pokemon-randomizer-fvx
branch: compat/firered-gen9-cfru-dpe
commit: ee82cb4e Merge pull request #11 from Planton361/compat/upr-fvx-cfru-dpe-skip-unchanged-palette-save
```

`git log --oneline -12` im Submodule zeigt die erwartete Fixkette:

```text
ee82cb4e Merge pull request #11 from Planton361/compat/upr-fvx-cfru-dpe-skip-unchanged-palette-save
8926912a compat: skip unchanged CFRU DPE palette save
b46836c1 Merge pull request #10 from Planton361/compat/upr-fvx-cfru-dpe-lazy-trainer-movesets
29c34084 compat: lazily load trainer movesets for CFRU DPE
8aa3c457 Merge pull request #9 from Planton361/compat/upr-fvx-cfru-dpe-defensive-palette-loading
aa19da09 Merge pull request #8 from Planton361/compat/upr-fvx-cfru-dpe-gen9-species-count
17e47254 compat: tolerate CFRU DPE missing pokemon palettes
8762b49b chore: initialize name scan diagnostics sentinels
8587cd90 Merge base branch and resolve Gen3RomHandler conflicts
58f3b5e6 Merge pull request #7 from Planton361/analysis/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics
d17b29a2 compat: detect CFRU DPE Gen9 species count
da97b97e chore: add CFRU DPE PokemonCount cutoff diagnostics
```

Der Workspace-Submodule-Pointer wurde von `8926912a` auf `ee82cb4e` aktualisiert.

## Build

```sh
cd 02_external/upr-fvx
./gradlew clean :random:jar
```

Ergebnis: `BUILD SUCCESSFUL`.

## Lokaler Smoke

Derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand wurde mit Wild-Randomization, `limitPokemon=false`, ohne Gen1-3-Einschraenkung und ohne Trainer-/Starter-/Evolution-/Learnset-/TM-/Tutor-/Ability-/Palette-/Sprite-Randomization gestartet.

ROM- und Output-Artefakte blieben lokal unter `05_builds/**` und wurden nicht committed.

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-gen9-wild-post-merge-smoke.gba \
  -S "<settings-string>" \
  -z 274269061345319 \
  -l
```

CLI-Exit-Code: `0`.

```text
Randomized successfully!
```

Lokale Artefakte:

```text
upr-fvx-cfru-dpe-gen9-wild-post-merge-smoke.gba      33554432 bytes
upr-fvx-cfru-dpe-gen9-wild-post-merge-smoke.gba.log     45726 bytes
```

Hashes:

```text
070e4c52e9d6a33e7ce4713b64d087f823e783cce492d2f935865b718108cf4f  upr-fvx-cfru-dpe-gen9-wild-post-merge-smoke.gba
23fb50b7cc71ba11f005d680f4f2252ea0cb7e2369400e1273e0844c470b0f1f  upr-fvx-cfru-dpe-gen9-wild-post-merge-smoke.gba.log
```

## Species-Coverage

Der gemergte Zielbranch erreicht weiterhin den vollstaendigen CFRU/DPE-Gen9-Species-Load:

```text
PokemonCount=1439
pokedexCount=1290
speciesList.size=1415
maxInternalSpeciesId=1439
maxSpeciesNumber=1290
maxSpeciesIdentityNumber=1439
generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Die erwarteten CFRU/DPE-Unblocker sind aktiv:

```text
[CFRU-DPE-PALETTE] skipped invalid pokemon palettes during load: normal=2 shiny=2
[CFRU-DPE-PALETTE] skipped unchanged pokemon palette save for CFRU/DPE Gen9 BPRE
```

## Save-Erfolg

Der Lauf erreicht Save und Log-Erzeugung:

```text
saveSuccessful=true
```

Belege:

- CLI-Exit-Code `0`
- `Randomized successfully!`
- Output-ROM wurde lokal erzeugt
- Randomizer-Wild-Log wurde lokal erzeugt
- kein Abbruch in `loadPokemonPalettes()`
- kein Abbruch in `saveTrainers()` / `getMovesLearnt()`
- kein Abbruch in `savePokemonPalettes()` bei `0x16b9c08`

## Wild-Log-Auswertung

Der Randomizer-Log meldet:

```text
Wild Pokemon: Randomized/Changed
Pokemon Palettes: Unchanged
```

Ausgewertet wurden `2176` sichtbare Wild-Slots im Log.

| Generation / Kategorie | Wild-Slots |
|---|---:|
| Gen1 | 407 |
| Gen2 | 417 |
| Gen3 | 228 |
| Gen4 | 196 |
| Gen5 | 381 |
| Gen6 | 35 |
| Gen7 | 85 |
| Gen8 | 126 |
| Gen9 | 289 |
| `Bad Egg` | 12 |
| `<unknown>` | 0 |

Hinweise zur Auswertung:

- `Unown P` und `Unown Y` wurden als Gen2 gezählt.
- `Baculegion` wurde als Gen8 gezählt.
- Der im Log gekuerzte Name `BruteBonet` wurde als Gen9 gezählt.
- `Bad Egg` bleibt eine separate Folgeauffaelligkeit, ist aber nicht der fruehere `<unknown>`-Nullslot.

## Beispiele

Beispielhafte Gen7-Wild-Encounter aus dem Log:

```text
Magearna
Meltan
Mudsdale
Araquanid
Necrozma
Oranguru
```

Beispielhafte Gen8-Wild-Encounter aus dem Log:

```text
Hatenna
Calyrex
Sandaconda
Carkol
Cinderace
Baculegion
```

Beispielhafte Gen9-Wild-Encounter aus dem Log:

```text
Glimmet
Toedscool
Tatsugiri
Floragato
Iron Crown
Hydrapple
```

Konkrete Log-Auszüge:

```text
Area #2 - PALLET TOWN Fishing
Glimmet Lvs15-25

Area #5 - VIRIDIAN CITY Fishing
Magearna Lvs5-15
Hatenna Lvs5-15
Tatsugiri Lvs20-30

Toedscool Lv24
Calyrex Lv23
Meltan Lv25
```

## Ergebnis

Gen9-Standard-/Fallback-Wild-Randomization ist auf dem gemergten UPR-FVX-Zielbranch bestaetigt.

Die Fixkette haelt im Post-Merge-Smoke:

- `PokemonCount=1439`
- `speciesList.size=1415`
- Gen7/8/9 sind im Species-Load sichtbar
- Wild-Randomization erreicht Save und Log
- Gen7/8/9 erscheinen im Wild-Log
- `<unknown>` bleibt `0`

## Risiken

- `Bad Egg` erscheint `12` Mal im Wild-Log und sollte separat klassifiziert werden.
- CFRU/DPE-Pokemon-Palette-Randomization bleibt partial/unsupported.
- DPE/CFRU-Learnsets sind weiter nicht korrekt als `gLevelUpLearnsets`-Profil modelliert.
- Static/Gift-, Trainer-, Evolution-, TM-/Tutor-, Ability- und Day/Night-Custom-Wild-Pfade bleiben ungetestet.
- Die `[CFRU-DPE-COUNT-DIAG]`- und `[temporary CFRU/DPE species diagnostics]`-Ausgaben sind noch sichtbar und sollten spaeter hinter Debug-Logging oder aus dem Zielbranch entfernt werden.

## Naechster minimaler Schritt

P1 Static/Gift-Species-only Diagnose wieder aufnehmen, ohne Learnset-, Trainer-, Palette-, Day/Night- oder Nullslot-Fixes im selben Branch zu vermischen.
