# P1 Trainer Held Items-only Diagnostics

## Datum

2026-05-12

## Branch

Workspace:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-held-items-only
```

UPR-FVX:

```text
compat/upr-fvx-cfru-dpe-evolutions-scope-and-write
```

## Ziel

Trainer Held Items-only fuer den CFRU/DPE Gen9-BPRE-Teststand diagnostizieren.

Keine Codeaenderung, kein Fix:

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

## Voraussetzungen

Vor dem Lauf wurden die Stop-Gates geprueft:

```text
UPR-FVX PR #15: MERGED, mergedAt=2026-05-12T20:19:26Z
Workspace PR #63: MERGED, mergedAt=2026-05-12T20:19:02Z
Workspace-Branch: analysis/upr-fvx-cfru-dpe-p1-trainer-held-items-only
Workspace git status --short: leer
```

UPR-FVX-Submodule-Stand:

```text
18766c4986db091d1e669c71302aa295195b039b
```

Der getestete UPR-FVX-Stand enthaelt den Evolution-Scope-/Write-Fix aus UPR-FVX PR #15. `02_external/**` wurde nur read-only analysiert; es wurden keine UPR-FVX-Codeaenderungen vorgenommen.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Route-1-Fallback-Teststand wie in Protokoll 021 bis 026. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/**` und wurden nicht committed.

Seed:

```text
274269061345323
```

Trainer Held Items-only Settings-String:

```text
422AAgEAQQBAAQABwAEAAHkAwARAAEUAAAUAEAEAAEA/////wAAAADkBOQBAAgJ5AYEAOQHAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjBORz/G48M4ig==
```

Der Settings-String wurde lokal aus dem Trainer-Species-only Baseline-String erzeugt und auf Trainer-Held-Items-only umgestellt.

## Build

UPR-FVX:

```text
./gradlew clean :random:jar
BUILD SUCCESSFUL
```

## Item-Pool-Auswertung

Der RomHandler laedt die Itemdaten und stellt einen Trainer-Held-Item-Pool bereit:

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

Sichtbarer Ausschluss aus `allowed`, aber nicht Trainer-Held-Item-Pool:

```text
excludedAllowedNotHeld.count=192
excludedAllowedNotHeld.first40=[1-Master Ball, 2-Ultra Ball, 3-Great Ball, 4-Poké Ball, 5-Safari Ball, 6-Net Ball, 7-Dive Ball, 8-Nest Ball, 9-Repeat Ball, 10-Timer Ball, 11-Luxury Ball, 12-Premier Ball, 17-Potion, 18-Antidote, 19-Burn Heal, 20-Ice Heal, 21-Awakening, 22-Paralyz Heal, 23-Full Restore, 24-Max Potion, 25-Hyper Potion, 26-Super Potion, 27-Full Heal, 28-Revive, 29-Max Revive, 30-Fresh Water, 31-Soda Pop, 32-Lemonade, 33-Moomoo Milk, 34-Energy Powder, 35-Energy Root, 36-Heal Powder, 37-Revival Herb, 38-Ether, 39-Max Ether, 40-Elixir, 41-Max Elixir, 42-Lava Cookie, 44-Sacred Ash, 45-HP Up]
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

Nach dem fehlgeschlagenen Randomization-Versuch bleibt der In-Memory-Trainerstand unveraendert:

```text
after.trainers=255
after.trainerPokemon=481
after.nullSpecies=0
after.heldItemEntries=0
after.noItemEntries=481
```

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
logContainsUnknown=false
```

Es entsteht keine Output-ROM und kein nichtleerer Log. Deshalb sind echte Held-Item-Writes und Reload in diesem Block nicht pruefbar:

```text
writeReloadCompared=0
writeReloadMismatches=not run
writeReloadFirstMismatch=null
```

## Fehlerpfad

Der Lauf scheitert vor Save/Log in `randomizeTrainerHeldItems()`:

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
    at com.uprfvx.random.randomizers.TrainerPokemonRandomizer.randomizeTrainerHeldItems(TrainerPokemonRandomizer.java:1086)
    at com.uprfvx.random.GameRandomizer.maybeRandomizeTrainerHeldItems(GameRandomizer.java:599)
    at com.uprfvx.random.GameRandomizer.applyRandomizers(GameRandomizer.java:302)
    at com.uprfvx.random.GameRandomizer.randomize(GameRandomizer.java:205)
```

Der Pointer `0x25e49c` ist derselbe CFRU/DPE-Moveset-Tabellenpfad, der bereits im frueheren Save-Trainers-/Moveset-Blocker eingeordnet wurde. Hier wird er erneut erreicht, weil `TrainerPokemonRandomizer.randomizeTrainerHeldItems()` `romHandler.getMovesLearnt()` eager laedt, obwohl Trainer-Movesets ausgeschaltet sind und fuer nicht-sensible, nicht-consumable Held-Items kein Moveset-Kontext benoetigt wird.

## Interpretation

Trainer Held Items-only ist auf dem getesteten CFRU/DPE-Gen9-BPRE-Stand noch nicht P1-supported.

Der Item- und Trainer-Load selbst ist nicht der Engpass:

- Trainerdaten laden stabil mit `255` Trainern und `481` Trainer-Pokemon.
- Es gibt keine Null-Species in Trainer-Pokemon.
- Der Trainer-Held-Item-Pool ist sichtbar und umfasst `52` Items.

Der praktische Blocker liegt vor der eigentlichen Held-Item-Vergabe im eager Learnset-/Moveset-Load:

- `randomizeTrainerHeldItems()` laedt `getMovesLearnt()` bedingungslos.
- CFRU/DPE Gen9-BPRE hat fuer diesen FVX-Pfad keinen gueltigen Standard-Gen3-Moveset-Pointer bei `0x25e49c`.
- Save, Log, Output-ROM und Write/Reload werden dadurch nicht erreicht.

Ein spaeterer Fix sollte den Trainer-Held-Item-Pfad so begrenzen, dass `getMovesLearnt()` nur geladen wird, wenn es fuer `resetMoves` oder sensible movebasierte Itemauswahl tatsaechlich gebraucht wird. Alternativ bleibt ein separater CFRU/DPE-Learnset-Loader noetig, aber das ist nicht Teil dieses Diagnoseblocks.

## Risiken

- Der Lauf stoppt vor Held-Item-Vergabe; dadurch sind echte after/reload Held-Item-Werte noch nicht pruefbar.
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
compat/upr-fvx-cfru-dpe-trainer-held-items-lazy-movesets
```

Zweck: Trainer-Held-Items-only entblocken, indem der Held-Item-Pfad `getMovesLearnt()` nur bei tatsaechlichem Bedarf laedt. Keine Trainer-Species-, Trainer-Moveset-, Learnset-, TM-/Tutor-, Ability-, Wild-, Starter-, Static/Gift-, Evolution- oder Palette-Fixes im selben Branch.
