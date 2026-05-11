# Workspace Build Randomizer Smoke Summary

## Datum

2026-05-11

## Arbeitsbranch

`setup/workspace-build-randomizer-smoke`

## Ziel der Session

Workspace praktisch um UPR-FVX, devkitPro/devkitARM, DPE Gen9 und CFRU-expansion erweitern und einen ersten lokalen Build-/Randomizer-/Emulator-Smoke-Test durchführen.

## Eingebundene externe Repos

### UPR-FVX

- Fork: `Planton361/universal-pokemon-randomizer-fvx`
- Lokaler Pfad: `02_external/upr-fvx`
- Branch: `compat/firered-gen9-cfru-dpe`
- Einbindung: Git-Submodule
- Buildsystem: Gradle
- Java: JDK 25
- Build-Befehl: `JAVA_HOME=/usr/lib/jvm/java-25-openjdk ./gradlew clean :random:jar`
- JAR: `02_external/upr-fvx/random/build/libs/UPR-FVX.jar`

### Dynamic Pokemon Expansion Gen 9

- Fork: `Planton361/Dynamic-Pokemon-Expansion-Gen-9`
- Lokaler Pfad: `02_external/Dynamic-Pokemon-Expansion-Gen-9`
- Branch: `compat/firered-gen9-randomizer`
- Einbindung: Git-Submodule
- Build-Befehl: `python3 scripts/make.py`
- Input-ROM lokal als `BPRE0.gba`
- Output: `test.gba`, `offsets.ini`

### CFRU-expansion

- Fork: `Planton361/CFRU-expansion`
- Lokaler Pfad: `02_external/CFRU-expansion`
- Branch: `compat/firered-gen9-randomizer`
- Einbindung: Git-Submodule
- Build-Befehl: `python3 scripts/make.py`
- Input: DPE-Output als `BPRE0.gba`
- Output: `test.gba`, `offsets.ini`
- CFRU-Fix-Commit: `184dc035 fix: avoid builtin strlen in mini printf`

## Toolchain

### devkitPro/devkitARM

- Installationspfad: `/opt/devkitpro`
- `DEVKITPRO=/opt/devkitpro`
- `DEVKITARM=/opt/devkitpro/devkitARM`
- `arm-none-eabi-gcc`: `/opt/devkitpro/devkitARM/bin/arm-none-eabi-gcc`
- Version: `arm-none-eabi-gcc (devkitARM) 15.2.0`
- `grit`: `/opt/devkitpro/tools/bin/grit`

### Zusatztools

- `wav2agb.exe` und `mid2agb.exe` lagen als Windows-EXE in den DPE/CFRU-Repos.
- Lokale Wine-Wrapper wurden unter `03_tools/releases/local-bin/` angelegt.
- `03_tools/releases/` ist ignored und wird nicht committed.
- `wine` wird benötigt, damit die Wrapper funktionieren.

## Build-Ergebnisse

### DPE Gen9 Build

- Input: lokale private ROM-Kopie als `02_external/Dynamic-Pokemon-Expansion-Gen-9/BPRE0.gba`
- Build erfolgreich: ja
- Lokaler Output: `05_builds/dpe-gen9-first-smoke/`
- committed: nein

### CFRU auf DPE Build

- Input: DPE-Output als `02_external/CFRU-expansion/BPRE0.gba`
- Build erfolgreich: ja
- Lokaler Output: `05_builds/cfru-dpe-gen9-first-smoke/test.gba`
- bekannter Output-Hash aus Session:
    - `test.gba`: `0610ad0850dbc1fecaac1f2898f7a614860a3420db2c7072d11027267db9666c`
    - `offsets.ini`: `0a4de34650e24165e13e8a2292bc83ed3192f4c7ea999f4fee6ad2a29f92e012`
- committed: nein

## UPR-FVX-Kompatibilitätsfixes

Im UPR-FVX-Fork wurden lokale Kompatibilitätsfixes auf `compat/firered-gen9-cfru-dpe` vorgenommen:

- ROM-Load-Exceptions werden auf stderr ausgegeben.
- Gen3 held item IDs außerhalb der bekannten FVX-Itemliste werden beim Laden toleriert.
- Ungültige Egg-Group-IDs werden beim Laden defensiv behandelt.
- Pokedex-/interne Species-Arraygröße wurde für CFRU/DPE robuster gemacht.
- Out-of-range Trainer-Tags werden ignoriert.
- Null-Species in `CheckValueCalculator` werden übersprungen.
- Fehlende `BreedingInfo` wird beim Speichern nicht zurückgeschrieben.
- Null-Species im Wild-Pokémon-Logger werden als `<unknown>` behandelt.

## Randomizer-Smoke-Test

### Minimaler Randomizer-Test

- Input-ROM: `05_builds/cfru-dpe-gen9-first-smoke/test.gba`
- Randomizer: `02_external/upr-fvx/random/build/libs/UPR-FVX.jar`
- Einstellung: `No Random Intro Mon` aktiviert
- Output-ROM: `05_builds/randomizer-smoke/randomizer-smoke.gba`
- Output-Hash:
    - `dddaf7285a8c72eb32657bc951dd9533bb2b6f5286fcda458903b3dd03ff148b`
- committed: nein
- Ergebnis: UPR-FVX konnte die CFRU/DPE-ROM laden, minimal randomisieren und speichern.

### BizHawk-Smoke-Test

- ROM: `05_builds/randomizer-smoke/randomizer-smoke.gba`
- BizHawk startet: ja
- Neues Spiel startet: ja
- Pokémon/Starterwahl möglich: ja
- Rivalenkampf startet und ist spielbar: ja
- Crash bis dahin: nein

## Wild-Encounter-Erkenntnisse

### CFRU-Encounter-Pools

- CFRU-Datei: `02_external/CFRU-expansion/src/Tables/wild_encounter_tables.c`
- Dort ist aktuell explizit nur `ROUTE_1` als Custom-Day/Night-Wild-Pool definiert.
- Route 1 hat separate Pools für:
    - Morning
    - Day
    - Evening
    - Night
- Route 2 und Route 22 sind dort nicht als eigene CFRU-Custom-Pools definiert.
- Route 22 unrandomized zeigte Rattfratz und Mankey, also wahrscheinlich Vanilla-/Fallback-Wilddaten.

### FVX Wild Randomization

- FVX randomisiert offenbar Vanilla-/Fallback-Wilddaten.
- Route 22 randomized zeigte unter anderem Golbat/Zubat.
- Viridian Forest randomized zeigte Relaxo.
- Der Randomizer-Log zeigte Wild-Pokémon nur aus Gen 1–3.
- Interpretation: FVX behandelt die ROM weiterhin als `Pokemon Fire Red (U) 1.0` und nutzt aktuell nur den Gen3/Vanilla-kompatiblen Species-Pool.
- Nächster großer Kompatibilitätspunkt: CFRU/DPE Gen4–Gen9 Species-Pool in FVX nutzbar machen.
- Zusätzlich prüfen: ob FVX die CFRU-Day/Night-Wild-Encounter-Tabellen überhaupt randomisiert oder nur Vanilla-Encounter-Tabellen.

## Repo-Sicherheitsentscheidung

- Original-Repos sollen nicht versehentlich kontaktiert werden.
- Upstream-Remotes sollen lokal aus Submodules entfernt bleiben.
- Submodules sollen nur `origin` auf `Planton361/...` zeigen.
- PRs nur mit explizitem `--repo Planton361/<repo>` erstellen.
- Keine GitHub-Web-UI-Aktion `Contribute -> Open pull request` gegen Originalrepos verwenden.
- Keine Upstream-PRs ohne ausdrückliche Entscheidung.

## Sicherheitsgrenzen

- Keine ROMs committed.
- Keine randomized ROMs committed.
- Keine Saves oder Emulator States committed.
- Keine Build-Artefakte committed.
- Keine Tool-Binaries committed.
- Private ROM bleibt unter `04_private_roms/`.
- Build- und Randomizer-Outputs bleiben unter `05_builds/`.
- Lokale Toolwrapper bleiben unter `03_tools/releases/`.

## Nächste technische Themen

1. UPR-FVX-Fixes committen/pushen, falls noch offen.
2. Workspace-Submodule-Pointer und Testprotokolle committen/pushen.
3. Workspace-PR nach `main` erstellen.
4. Route-1-randomized vs unrandomized prüfen.
5. FVX Species-Pool für CFRU/DPE Gen4–Gen9 analysieren.
6. Einzeltests:
    - Wild Encounters
    - Trainer Pokémon
    - Starters
    - Moves/Learnsets
    - Evolutions
    - Items/TMs/Tutors
    - Emulator/Ironmon Tracker