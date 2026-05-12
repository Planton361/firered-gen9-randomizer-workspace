# Trainer Held Items Lazy Movesets Diagnostics

## Datum

2026-05-12

## Branch

Workspace:

```text
compat/upr-fvx-cfru-dpe-trainer-held-items-lazy-movesets
```

UPR-FVX:

```text
compat/upr-fvx-cfru-dpe-trainer-held-items-lazy-movesets
```

## Ziel

Den P1-Blocker aus `027_p1_trainer_held_items_only.md` gezielt beheben und diagnostisch bestaetigen:

- Trainer-Held-Items-only darf `getMovesLearnt()` nicht eager laden
- Moveset-/Learnset-Kontext wird fuer Held Items nur gebraucht, wenn sensible movebasierte Itemauswahl aktiv ist oder ein `resetMoves`-Pokemon tatsaechlich Moves am Level berechnen muss
- keine Trainer-Species-, Trainer-Moveset-, Learnset-, TM-/Tutor-, Ability-, Wild-, Starter-, Static/Gift-, Evolution- oder Palette-Fixes in diesem Branch

## Codeaenderung

UPR-FVX-Commit:

```text
3864ad0e7efda4ed8a329fb22edb3a28db1040e8
```

Geaenderte UPR-FVX-Datei:

- `random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java`

Kurzfassung:

- `randomizeTrainerHeldItems()` laedt `romHandler.getMovesLearnt()` nicht mehr bedingungslos.
- Fuer nicht-sensible Trainer-Held-Items-only-Laeufe werden vorhandene Trainer-Moves direkt verwendet und kein Learnset-/Moveset-Table-Pointer gelesen.
- Bei `sensibleItemsOnlyForTrainers=true` wird der Moveset-Kontext weiterhin genutzt; `getMovesLearnt()` wird lazy erst dann geladen, wenn ein `resetMoves`-Trainer-Pokemon ihn tatsaechlich braucht.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Route-1-Fallback-Teststand wie in Protokoll 021 bis 027. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/**` und wurden nicht committed.

Seed:

```text
274269061345323
```

Trainer Held Items-only Settings-String:

```text
422AAgEAQQBAAQABwAEAAHkAwARAAEUAAAUAEAEAAEA/////wAAAADkBOQBAAgJ5AYEAOQHAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjBORz/G48M4ig==
```

Settings-Intent:

- Trainer-Held-Items: an fuer Boss-, Important- und Regular-Trainer
- Trainer-Species: aus
- Trainer-Movesets: aus
- Wild: aus
- Starters: aus
- Static/Gift: aus
- Evolutions: aus
- Learnsets/Movesets: aus
- TM/HM/Tutor: aus
- Abilities: aus
- Palette-/Sprite-Randomization: aus
- `limitPokemon=false`

## Build

UPR-FVX:

```text
./gradlew clean :random:jar
BUILD SUCCESSFUL
```

## Item-Pool-Auswertung

```text
items.totalSlots=1375
items.nonNull=374
items.allowed=244
items.nonBad=181
trainerHeldItemPool.size=52
```

Erste 20 Trainer-Held-Items:

```text
43-Berry Juice
149-Cheri Berry
150-Chesto Berry
151-Pecha Berry
152-Rawst Berry
153-Aspear Berry
154-Leppa Berry
155-Oran Berry
156-Persim Berry
157-Lum Berry
158-Sitrus Berry
159-Figy Berry
160-Wiki Berry
161-Mago Berry
162-Aguav Berry
163-Iapapa Berry
201-Liechi Berry
202-Ganlon Berry
203-Salac Berry
204-Petaya Berry
```

## Trainer-Load und Held-Item-Status

Vor der Randomization:

```text
before.trainers=255
before.trainerPokemon=481
before.nullSpecies=0
before.heldItemEntries=0
before.noItemEntries=481
```

Nach der Randomization:

```text
after.trainers=255
after.trainerPokemon=481
after.nullSpecies=0
after.heldItemEntries=481
after.noItemEntries=0
```

Nach Reload der Output-ROM:

```text
reload.trainers=255
reload.trainerPokemon=481
reload.nullSpecies=0
reload.heldItemEntries=481
reload.noItemEntries=0
```

## Randomization-Ergebnis

Der direkte `GameRandomizer.Results`-Diagnoselauf meldet:

```text
saveSuccessful=true
logSuccessful=true
outputRomExists=true
outputRomBytes=33554432
logNonEmpty=true
directLogBytes=25719
logContainsTrainerPokemon=true
logContainsBadEgg=false
logContainsUnknown=false
```

Der fruehere Fehlerpfad aus Protokoll 027 wird nicht mehr erreicht:

```text
Gen3RomHandler.getMovesLearnt() -> No valid pointer at 0x25e49c
```

## Write/Reload

```text
writeReloadCompared=481
writeReloadMismatches=0
writeReloadFirstMismatch=null
```

Alle `481` Trainer-Pokemon haben nach Randomization und Reload ein Held Item. Der Reload erhaelt die geschriebenen Held-Item-IDs ohne Mismatch.

## Interpretation

Trainer Held Items-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand jetzt P1-supported:

- der Trainer-Held-Item-Pool ist vorhanden
- Trainerdaten laden stabil
- Held Items werden fuer alle `481` Trainer-Pokemon geschrieben
- Save und Log gelingen
- Output-ROM und nichtleerer Trainer-Log entstehen
- `Bad Egg` und `<unknown>` erscheinen nicht im Log
- Write/Reload ist stabil mit `writeReloadMismatches=0`

Der Fix ist absichtlich auf den eager Moveset-/Learnset-Load im Held-Item-Pfad begrenzt. Sensible movebasierte Held-Item-Auswahl, Trainer-Movesets und das CFRU/DPE-Learnset-Datenmodell bleiben separate Themen.

## Risiken

- Es wurde kein BizHawk-Gameplay-Smoke gegen die erzeugte Output-ROM ausgefuehrt.
- Sensible movebasierte Trainer-Held-Item-Auswahl wurde nicht separat getestet; sie kann weiterhin ein korrektes CFRU/DPE-Learnset-Modell benoetigen.
- Trainer-Movesets-only bleibt nicht diagnostiziert.
- Die Diagnose nutzt einen temporaeren lokalen `/tmp`-Harness; dieser wurde nicht ins Repo aufgenommen.

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
- Keine CFRU-/DPE-Aenderungen.

## Naechster minimaler Schritt

Nach Review/Merge der UPR-FVX- und Workspace-PRs:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-only
```

Zweck: Trainer-Movesets-only separat diagnostizieren, ohne Trainer-Held-Items-, Trainer-Species-, Learnset-, TM-/Tutor-, Ability-, Wild-, Starter-, Static/Gift-, Evolution- oder Palette-Fixes im selben Branch.
