# UPR FVX CFRU/DPE Minimal Randomize Smoke Test

## Datum

2026-05-11

## Zweck

Pruefen, ob der UPR-FVX-Fork die lokal gebaute CFRU/DPE-Gen9-ROM laden und minimal randomisiert speichern kann.

## Randomizer

- Fork: Planton361/universal-pokemon-randomizer-fvx
- Branch: `compat/firered-gen9-cfru-dpe`
- Commit: 6af5ba3972fd7d8c98844596fb88c367daf5be8d
- JAR: `02_external/upr-fvx/random/build/libs/UPR-FVX.jar`
- JAR SHA-256: 03c93c5e3f65e9215973b34333d25ced393aa0d24616df5d1a8591f07fe09606

## Input-ROM

- Quelle: `05_builds/cfru-dpe-gen9-first-smoke/test.gba`
- SHA-256: 0610ad0850dbc1fecaac1f2898f7a614860a3420db2c7072d11027267db9666c
- committed: nein

## Randomizer-Einstellungen

- `No Random Intro Mon`: aktiviert
- Weitere Einstellungen: minimaler Smoke-Test

## Output-ROM

- Pfad: `05_builds/randomizer-smoke/randomizer-smoke.gba`
- SHA-256: dddaf7285a8c72eb32657bc951dd9533bb2b6f5286fcda458903b3dd03ff148b
- committed: nein
- ignored: ja, via `05_builds/`

## Ergebnis

- GUI gestartet: ja
- CFRU/DPE-ROM geladen: ja
- Invalid-ROM-Warnung angezeigt: ja
- Minimal randomisierte ROM gespeichert: ja

## UPR-FVX-Kompatibilitaetsfixes in diesem Stand

- ROM-Load-Exceptions werden auf stderr ausgegeben.
- Gen3 held item IDs ausserhalb der bekannten FVX-Itemliste werden beim Laden toleriert.
- Ungueltige Egg-Group-IDs werden beim Laden defensiv behandelt.
- Pokedex-/interne Species-Arraygroesse wurde fuer CFRU/DPE robuster gemacht.
- Out-of-range Trainer-Tags werden ignoriert.
- Null-Species in CheckValueCalculator werden uebersprungen.
- Fehlende BreedingInfo wird beim Speichern nicht zurueckgeschrieben.

## Sicherheitsgrenzen

- Keine ROM wurde committed.
- Keine randomized ROM wurde committed.
- Build- und Randomizer-Ausgaben bleiben lokal in `05_builds/`.
