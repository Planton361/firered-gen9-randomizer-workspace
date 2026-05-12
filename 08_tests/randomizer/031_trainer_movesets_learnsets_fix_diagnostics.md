# 031 - Trainer Movesets Learnsets Fix Diagnostics

## Datum

2026-05-13

## Branches

Workspace:

```text
compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets
```

UPR-FVX:

```text
compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets
```

## Ziel

Trainer Movesets-only fuer CFRU/DPE Gen9-BPRE entblocken. Minimaler Fix: `Gen3RomHandler.getMovesLearnt()` liest fuer erkannte CFRU/DPE-Gen9-BPRE-Hacks Level-Up-Learnsets defensiv als CFRU/DPE-Read-Pool. Kein `setMovesLearnt()`-/Learnset-Write-Ausbau.

## UPR-FVX-Fix

Commit:

```text
655764816f9fefedb9433f33e4da0bc9d44bcda7
```

Geaendert wurde nur:

```text
02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java
```

Fix-Verhalten:

- `getMovesLearnt()` verzweigt nur bei `useCfruDpeGen9SpeciesCount && !jamboMovesetHack` auf den CFRU/DPE-Pfad.
- Vanilla-Gen3- und Jambo-Pfade bleiben unveraendert.
- Der CFRU/DPE-Pfad nutzt weiterhin `PokemonMovesets` als Tabellenbasis und interne Species-IDs ueber `pokedexToInternal`.
- Ungueltige Learnset-Pointer werden fuer den Read-Pool als leere Learnsets behandelt, statt den gesamten Trainer-Movesets-Lauf abzubrechen.
- CFRU/DPE-Level-Up-Eintraege werden als `u16 move` + `u8 level` bis Sentinel `move == 0 && level == 0xFF` gelesen.
- Pro Learnset werden maximal `50` Eintraege gelesen.
- Move-IDs werden nur uebernommen, wenn sie im aktuell geladenen FVX-Move-Array vorhanden sind.
- `abilityName()` gibt fuer nicht geladene CFRU/DPE-Ability-IDs defensiv `ability #n` aus, damit der Trainer-Log nicht an erweiterten Ability-IDs abbricht.
- `setMovesLearnt()` und Learnset-Write wurden nicht erweitert.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Route-1-Fallback-Teststand wie in Protokoll 021 bis 030. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/**` und wurden nicht committed.

Seed:

```text
274269061345323
```

Trainer Movesets-only Settings-String:

```text
422AAgEAQQBAAQABwAEAAHkAwARAAEUAAAUAEAEAAEA/////wAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAADgJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjABxHo348M4ig==
```

Lokaler Artefaktordner:

```text
05_builds/randomizer-smoke/031_trainer_movesets_learnsets_fix/
```

## Diagnose-Ergebnis

Move- und Trainer-Load vor Randomization:

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

Direkter `GameRandomizer.Results`-Lauf:

```text
saveSuccessful=true
logSuccessful=true
outputRomExists=true
outputRomBytes=33554432
logNonEmpty=true
directLogBytes=38171
logContainsTrainerPokemon=true
logContainsBadEgg=false
logContainsUnknownSpecies=false
logContainsUnknownMove=false
logContainsGen8MoveSamples=false
logContainsGen9MoveSamples=false
```

Nach Randomization:

```text
after.trainers=255
after.trainerPokemon=481
after.nullSpecies=0
after.movesetEntries=417
after.zeroMovePokemon=64
after.resetMoves=0
after.moveSlots=1924
after.zeroMoveSlots=566
after.invalidMoves=0
after.unknownNamedMoves=0
beforeAfterMoveSignatureChanges=418
```

Reload-Vergleich:

```text
reload.trainers=255
reload.trainerPokemon=481
reload.nullSpecies=0
reload.movesetEntries=417
reload.zeroMovePokemon=64
reload.resetMoves=0
reload.moveSlots=1924
reload.zeroMoveSlots=566
reload.invalidMoves=0
reload.unknownNamedMoves=0
writeReloadCompared=481
writeReloadMismatches=0
writeReloadFirstMismatch=null
```

## Ergebnisbewertung

Trainer Movesets-only ist fuer den getesteten CFRU/DPE Gen9-BPRE-Stand auf diesem Fixstand entblockt:

- Der vorherige `No valid pointer at 0x25e49c`-Abbruch tritt nicht mehr auf.
- Save ist erfolgreich.
- Log ist erfolgreich und nicht leer.
- Output-ROM entsteht.
- Trainer-Movesets werden sichtbar randomisiert: `beforeAfterMoveSignatureChanges=418`.
- Reload erhaelt die geschriebenen Trainer-Movesets: `writeReloadMismatches=0`.
- Kein `Bad Egg`, kein `<unknown>` und keine Unknown-Move-Marker im Trainer-Log.
- Keine invaliden oder unbekannt benannten Move-IDs in after/reload.

## Einschraenkungen und Risiken

- Der CFRU/DPE-Pfad ist bewusst Read-Pool-orientiert; Learnset-Write bleibt unmodelliert.
- Move-IDs oberhalb der geladenen FVX-Move-Liste werden fuer Trainer-Moveset-Pools gefiltert. Das entblockt P1, ist aber noch kein vollstaendiges Gen8/9-Move-Datenmodell.
- Einige CFRU/DPE-Ability-IDs sind im FVX-Ability-Namenarray noch nicht geladen; der Log nutzt dafuer `ability #n`-Fallbacks.
- TM-/Tutor-/Egg-Move-Datenmodelle koennen in spaeteren Kombinationslaeufen noch eigene Blocker zeigen.
- Kein BizHawk-Gameplay-Smoke in diesem Block.

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

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets, Tokens oder `.env`-Dateien committed oder dokumentiert.
- Lokale ROM-/Output-/Log-Artefakte blieben ignored unter `05_builds/**`.
- Keine Original-Upstreams kontaktiert.
- Kein breiter Refactor.
- `setMovesLearnt()` / Learnset-Write nicht ausgeweitet.

## Naechster minimaler Schritt

Nach Review/Merge der UPR-FVX- und Workspace-PRs: Trainer Movesets-only als P1-supported baseline fuer spaetere Kombinationslaeufe verwenden. Naechste offene Risiken sind vollstaendige Gen8/9-Move-Daten, TM/Tutor/Egg-Move-Tabellen und sensible movebasierte Trainer-Held-Item-Auswahl gegen CFRU/DPE-Learnsets.
