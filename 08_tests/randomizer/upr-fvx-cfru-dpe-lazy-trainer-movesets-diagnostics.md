# UPR-FVX CFRU/DPE Lazy Trainer Movesets Diagnostics

Datum: 2026-05-12

## Ziel

Dieser Arbeitsblock prueft einen engen UPR-FVX-Unblocker im Gen3-Trainer-Save-Pfad.

Ziel ist nur:

- `trainerPokemonToBytes()` soll `getMovesLearnt()` erst laden, wenn Trainer-Moves wirklich ueber `resetMoves` neu berechnet werden muessen.
- Wild-only-/Coverage-Laeufe sollen nicht mehr am alten/falsch erkannten `PokemonMovesets`-Pointer `0x25e49c` in `saveTrainers()` abbrechen.

Nicht Ziel dieses Branches:

- kein DPE/CFRU-`gLevelUpLearnsets`-Loader
- kein Moveset-Format-Fix
- keine `PokemonMovesets`-Erkennung
- keine Trainer-Randomizer-Featureaenderung
- keine Count-, Palette-, Wild-, Static/Gift-, Starter-, Evolution-, TM/Tutor-, Ability- oder Day/Night-Fixes

## Branches und Commits

UPR-FVX:

```text
repo: Planton361/universal-pokemon-randomizer-fvx
base: compat/firered-gen9-cfru-dpe
branch: compat/upr-fvx-cfru-dpe-lazy-trainer-movesets
commit: 29c34084 compat: lazily load trainer movesets for CFRU DPE
PR: https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/10
```

Workspace:

```text
repo: Planton361/firered-gen9-randomizer-workspace
branch: analysis/upr-fvx-cfru-dpe-lazy-trainer-movesets
```

## Implementierte technische Entscheidung

Vorher lud `trainerPokemonToBytes()` die globale Moveset-Map immer am Methodenanfang:

```text
Map<Integer, List<MoveLearnt>> movesets = this.getMovesLearnt();
```

Das passierte auch fuer Trainer ohne Custom-Moves und fuer Custom-Move-Trainer, deren Moves unveraendert aus `tp.getMoves()` geschrieben werden.

Nachher wird die Map nur lazy geladen:

```text
Map<Integer, List<MoveLearnt>> movesets = null;

if (tp.isResetMoves()) {
    if (movesets == null) {
        movesets = this.getMovesLearnt();
    }
    int[] pokeMoves = getMovesAtLevel(...);
}
```

Damit bleibt das bestehende Verhalten fuer echte Reset-Move-Faelle erhalten. Unveraenderte Trainer-Pokemon koennen ohne Learnset-Zugriff serialisiert werden.

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

CLI-Lauf:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-lazy-trainer-movesets-diagnostics.gba \
  -S "422AAgEAQQBAAQABwAEAAHkCAARAQEUAAAUAEAEAAEA/wAAAAAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjD84HA048M4ig==" \
  -z 274269061345319 \
  -l
```

CLI-Exit-Code: `0`.

Wichtig: Der CLI meldet wie in frueheren Diagnosebloecken `Randomized successfully!`, obwohl `GameRandomizer.Results.wasSaveSuccessful=false` sein kann. Deshalb wurde zusaetzlich lokal per JShell `GameRandomizer.Results` ausgelesen, ohne Codeaenderung.

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

Der Palette-Load bleibt defensiv:

```text
[CFRU-DPE-PALETTE] skipped invalid pokemon palettes during load: normal=2 shiny=2
```

## Save-/Moveset-Blocker Vorher/Nachher

Vorheriger Blocker nach Palette-Fix:

```text
java.lang.IllegalArgumentException: No valid pointer at 0x25e49c.
  at Gen3RomHandler.readPointer(...)
  at Gen3RomHandler.getMovesLearnt(...)
  at Gen3RomHandler.trainerPokemonToBytes(...)
  at Gen3RomHandler.saveTrainers(...)
```

Nach dem Lazy-Fix:

- Der Lauf erreicht `saveTrainers()` ohne den `getMovesLearnt()`-/`0x25e49c`-Abbruch.
- Es gibt keinen Stacktrace mehr aus `saveTrainers()` oder `getMovesLearnt()`.
- Der Save-Pfad kommt bis zum nachgelagerten `savePokemonPalettes()`.

Per `GameRandomizer.Results`:

```text
saveSuccessful=false
logSuccessful=true
checkValue=-675822265
logBytes=0
```

Neuer nachgelagerter Blocker:

```text
java.lang.IllegalArgumentException: no compressed data found at offset 0x16b9c08
  at compressors.DSDecmp.Decompress(DSDecmp.java:41)
  at Gen3RomHandler.lengthOfCompressedDataAt(...)
  at AbstractGBRomHandler$DataRewriter.rewriteData(...)
  at Gen3RomHandler.rewriteCompressedPalette(...)
  at Gen3RomHandler.savePokemonPalettes(...)
  at AbstractRomHandler.prepareSaveRom(...)
```

Interpretation:

- Dieser Branch entkoppelt erfolgreich den Trainer-Save von unnoetigem Learnset-Loading.
- Der naechste technische Blocker liegt nicht mehr in `saveTrainers()`/`getMovesLearnt()`, sondern in `savePokemonPalettes()`.
- Dieser neue Palette-Save-Blocker ist ausserhalb des Branch-Scopes und wurde nicht gefixt.

## Wild-Log-Auswertung

Es gibt noch keinen nutzbaren Wild-Log:

- `logger.logResults()` wird zwar aufgerufen, schreibt aber wegen des vorherigen Save-Fehlers keinen Inhalt in den CLI-Log.
- Die erzeugte `.gba.log` enthaelt nur den UTF-8-BOM.
- Es wurden keine neuen Gen7/8/9-Wild-Encounter-Beispiele aus einem Randomizer-Log erzeugt.

Der Fortschritt ist trotzdem eindeutig: Der vorherige Save-Trainers-/Moveset-Blocker ist weg; der naechste Blocker liegt spaeter im Palette-Save-Pfad.

## Technische Interpretation

Level-up-Movesets werden im Gen3-Trainer-Save nur fuer eine konkrete Situation benoetigt:

- Trainer hat Custom-Move-Daten.
- Mindestens ein `TrainerPokemon` hat `resetMoves=true`.
- In diesem Fall muessen Moves per `getMovesAtLevel()` aus der Learnset-Map neu berechnet werden.

Fuer alle anderen Trainer-Save-Faelle reichen die bereits geladenen Trainer-Move-Werte oder die 8-Byte-Trainer-Pokemon-Struktur ohne Move-Daten. Deshalb ist der Lazy-Load semantisch kleiner und sicherer als ein defensiver Learnset-Reader.

## Risiken

- Jeder echte `resetMoves`-Fall nutzt weiterhin den bestehenden `getMovesLearnt()`-Pfad und kann fuer CFRU/DPE weiterhin am alten Learnset-Modell scheitern.
- Trainer-Moveset-Randomization, SpeciesMoveset-Randomization und held-item-sensible-moves-Pfade koennen weiterhin Learnsets laden; diese Branch-Aenderung betrifft nur `trainerPokemonToBytes()`.
- Der neue Palette-Save-Blocker verhindert weiterhin `saveSuccessful=true` und damit Wild-Log-Auswertung.
- Der CLI meldet trotz `saveSuccessful=false` `Randomized successfully!`; fuer weitere Diagnosen sollte `GameRandomizer.Results` oder ein aequivalenter Status ausgewertet werden.

## Naechster minimaler Schritt

Naechster separater Branch:

```text
analysis/upr-fvx-cfru-dpe-palette-save-blocker
```

Ziel:

- read-only oder eng begrenzte Diagnose des neuen `savePokemonPalettes()`-Blockers bei `0x16b9c08`
- klaeren, warum der defensive Palette-Fix den Load entblockt, der Save aber noch versucht, komprimierte Palette-Daten an einer nicht dekomprimierbaren Adresse umzuschreiben
- kein Learnset-, Trainer-, Static/Gift-, Wild-, Count- oder Day/Night-Fix im selben Branch
