# P1 Trainer Movesets-only Diagnostics

## Datum

2026-05-12

## Branch

Workspace:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-only
```

UPR-FVX:

```text
compat/upr-fvx-cfru-dpe-trainer-held-items-lazy-movesets
```

## Ziel

Trainer Movesets-only fuer den CFRU/DPE Gen9-BPRE-Teststand diagnostizieren.

Keine Codeaenderung, kein Fix:

- Trainer-Movesets: an fuer Boss-, Important- und Regular-Trainer
- Trainer-Species: aus
- Trainer-Held-Items: aus
- Wild: aus
- Starters: aus
- Static/Gift: aus
- Evolutions: aus
- Learnsets/Movesets: aus
- TM/HM/Tutor: aus
- Abilities: aus
- Palette-/Sprite-Randomization: aus
- `limitPokemon=false`

## Voraussetzungen

Vor dem Lauf wurden die Stop-Gates geprueft:

```text
UPR-FVX PR #16: MERGED, mergedAt=2026-05-12T21:40:02Z
Workspace PR #65: MERGED, mergedAt=2026-05-12T21:30:14Z
Workspace-Branch: analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-only
Workspace git status --short: leer
```

UPR-FVX-Submodule-Stand:

```text
3864ad0e7efda4ed8a329fb22edb3a28db1040e8
```

Der getestete UPR-FVX-Stand enthaelt den Trainer-Held-Items-lazy-Moveset-Fix aus UPR-FVX PR #16. `02_external/**` wurde nur read-only analysiert; es wurden keine UPR-FVX-Codeaenderungen vorgenommen.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Route-1-Fallback-Teststand wie in Protokoll 021 bis 028. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/**` und wurden nicht committed.

Seed:

```text
274269061345323
```

Trainer Movesets-only Settings-String:

```text
422AAgEAQQBAAQABwAEAAHkAwARAAEUAAAUAEAEAAEA/////wAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAADgJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjABxHo348M4ig==
```

Der Settings-String wurde lokal aus dem Trainer-Held-Items-only Baseline-String erzeugt und auf Trainer-Movesets-only umgestellt.

## Build

UPR-FVX:

```text
./gradlew clean :random:jar
BUILD SUCCESSFUL
```

## Move- und Trainer-Load

```text
moves.total=559
before.trainers=255
before.trainerPokemon=481
before.nullSpecies=0
before.movesetEntries=53
before.zeroMovePokemon=428
before.resetMoves=0
before.moveSlots=1924
before.zeroMoveSlots=1715
before.invalidMoves=0
before.unknownNamedMoves=0
```

Vor der Randomization sind keine ungueltigen Move-IDs und keine unbekannt benannten Moves im geladenen Trainerbestand sichtbar.

## Randomization-Ergebnis

Der direkte `GameRandomizer.Results`-Diagnoselauf meldet:

```text
saveSuccessful=false
logSuccessful=true
outputRomExists=false
outputRomBytes=0
logNonEmpty=false
directLogBytes=0
logContainsTrainerPokemon=false
logContainsBadEgg=false
logContainsUnknownSpecies=false
logContainsUnknownMove=false
logContainsGen8MoveSamples=false
logContainsGen9MoveSamples=false
```

Nach dem fehlgeschlagenen Randomization-Versuch bleibt der In-Memory-Trainerstand unveraendert:

```text
after.trainers=255
after.trainerPokemon=481
after.nullSpecies=0
after.movesetEntries=53
after.zeroMovePokemon=428
after.resetMoves=0
after.moveSlots=1924
after.zeroMoveSlots=1715
after.invalidMoves=0
after.unknownNamedMoves=0
beforeAfterMoveSignatureChanges=0
```

Es entsteht keine Output-ROM und kein nichtleerer Log. Dadurch sind Gen8/9-Moves, unbekannte Moves im Log und Write/Reload in diesem Block nicht pruefbar:

```text
writeReloadCompared=0
writeReloadMismatches=not run
writeReloadFirstMismatch=null
```

## Fehlerpfad

Der Lauf scheitert vor Save/Log im Trainer-Moveset-Randomizer:

```text
saveException.type=java.lang.IllegalArgumentException
saveException.message=No valid pointer at 0x25e49c.
```

Stacktrace:

```text
java.lang.IllegalArgumentException: No valid pointer at 0x25e49c.
    at com.uprfvx.romio.romhandlers.Gen3RomHandler.readPointer(Gen3RomHandler.java:1670)
    at com.uprfvx.romio.romhandlers.Gen3RomHandler.readPointer(Gen3RomHandler.java:1659)
    at com.uprfvx.romio.romhandlers.Gen3RomHandler.getMovesLearnt(Gen3RomHandler.java:2403)
    at com.uprfvx.random.randomizers.TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel(TrainerMovesetRandomizer.java:580)
    at com.uprfvx.random.randomizers.TrainerMovesetRandomizer.randomizeTrainerMovesets(TrainerMovesetRandomizer.java:45)
    at com.uprfvx.random.GameRandomizer.maybeRandomizeTrainerMovesets(GameRandomizer.java:583)
    at com.uprfvx.random.GameRandomizer.applyRandomizers(GameRandomizer.java:299)
    at com.uprfvx.random.GameRandomizer.randomize(GameRandomizer.java:205)
```

Der Pointer `0x25e49c` ist derselbe CFRU/DPE-Moveset-Tabellenpfad, der bereits in frueheren Diagnose- und Fixbloecken als Standard-Gen3-Learnset-/Moveset-Pfad eingeordnet wurde. Anders als bei Trainer-Held-Items ist dieser Zugriff fuer Trainer-Movesets-only fachlich zentral: `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel()` benoetigt Level-Up-Moves, Egg Moves, TM/HM- und Tutor-Kompatibilitaet, um neue Movesets zu bauen.

## Interpretation

Trainer Movesets-only ist auf dem getesteten CFRU/DPE-Gen9-BPRE-Stand noch nicht P1-supported.

Der Trainer-Load selbst ist nicht der Engpass:

- Trainerdaten laden stabil mit `255` Trainern und `481` Trainer-Pokemon.
- Es gibt keine Null-Species in Trainer-Pokemon.
- Bestehende Trainer-Moves enthalten keine ungueltigen Move-IDs.

Der praktische Blocker ist das fehlende CFRU/DPE-kompatible Learnset-/Moveset-Datenmodell fuer `getMovesLearnt()`:

- Trainer-Movesets-only erreicht direkt `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel()`.
- Dieser Pfad laedt `romHandler.getMovesLearnt()`.
- CFRU/DPE Gen9-BPRE hat fuer diesen FVX-Standard-Gen3-Pfad keinen gueltigen Pointer bei `0x25e49c`.
- Save, Log, Output-ROM und Write/Reload werden dadurch nicht erreicht.

Ein spaeterer Fix muss voraussichtlich das CFRU/DPE-Level-Up-Learnset-Modell fuer `gLevelUpLearnsets` korrekt lesen oder Trainer-Movesets fuer diesen ROM-Modus defensiv anders scopen. Das ist bewusst nicht Teil dieses Diagnoseblocks.

## Risiken

- Der Lauf stoppt vor Moveset-Vergabe; dadurch sind echte after/reload Moveset-Werte noch nicht pruefbar.
- Gen8/9-Moves und unbekannte Moves im Trainer-Log sind nicht bewertbar, weil kein Log entsteht.
- Es wurde kein BizHawk-Gameplay-Smoke ausgefuehrt.
- Die Diagnose nutzt einen temporaeren lokalen `/tmp`-Harness; dieser wurde nicht ins Repo aufgenommen.
- Die lokalen ROM-/Output-/Log-Artefakte unter `05_builds/**` bleiben ignored und wurden nicht committed.

## Checks

UPR-FVX:

```text
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
```

Workspace:

```text
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

## Sicherheitsstatus

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env`-Dateien committed oder dokumentiert.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`.
- Keine Original-Upstreams kontaktiert.
- Keine Aenderungen in `02_external/**`.
- Keine Codeaenderung und kein Fix in diesem Branch.

## Naechster minimaler Schritt

Nach Review/Merge dieses Diagnose-PRs:

```text
analysis/upr-fvx-cfru-dpe-p1-learnsets-model
```

Zweck: CFRU/DPE-Level-Up-Learnset- und Moveset-Datenmodell fuer `gLevelUpLearnsets` read-only modellieren, bevor ein Trainer-Movesets-Fix versucht wird.
