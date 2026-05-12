# P1 Trainer Species-only Diagnostics

## Datum

2026-05-12

## Branch

Workspace:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-species-only
```

UPR-FVX:

```text
compat/upr-fvx-cfru-dpe-static-gift-scope-and-write
```

## Ziel

Trainer-Species-only mit vollstaendigem Gen1-Gen9-Species-Pool diagnostizieren.

Keine Codeaenderung, kein Fix:

- Wild: aus
- Starters: aus
- Static/Gift: aus
- Trainer-Species: an
- Trainer-Moves/Movesets: aus
- Trainer-Held-Items: aus
- Evolutions: aus
- Learnsets/Movesets: aus
- TM/HM/Tutor: aus
- Abilities: aus
- Palette-/Sprite-Randomization: aus
- `limitPokemon=false`

## Basis

Workspace `main` enthaelt PR #58 und pinnt `02_external/upr-fvx` auf:

```text
009178e8848b4272e6b8be54a8bf5b2bed34d5f2
```

UPR-FVX-Remote:

```text
https://github.com/Planton361/universal-pokemon-randomizer-fvx.git
```

Der getestete UPR-FVX-Commit enthaelt den Static/Gift-Scope- und Species-Write-Fix aus UPR-FVX PR #13. Static/Gift Species-only ist auf diesem Stand P1-supported.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Route-1-Fallback-Teststand wie in Protokoll 021 und 022. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/**` und wurden nicht committed.

Seed:

```text
274269061345323
```

Trainer-Species-only Settings-String:

```text
422AAgEAQQBAAQABwAEAALkAwARAAEUAAAUAEAEAAEA/wAAAAAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjDnKwhm48M4ig==
```

Der Settings-String wurde lokal aus dem Static/Gift-only Baseline-String erzeugt und auf Trainer-Species-only umgestellt. Die Diagnose-Hilfsprogramme lagen temporaer ausserhalb des Repos.

## Build

UPR-FVX:

```text
./gradlew clean :random:jar
BUILD SUCCESSFUL
```

## Species- und Trainer-Load

Der Species-Load bleibt auf dem erwarteten Gen9-Coverage-Stand:

```text
PokemonCount=1439
speciesList.size=1415
maxSpeciesIdentityNumber=1439
generationCounts={1=271, 2=118, 3=188, 4=149, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Der Trainer-Load selbst blockiert nicht:

```text
trainers=255
trainerPokemon=481
nullSpecies=0
trainerGenerationCounts={1=481}
```

## Trainer-Pool-Auswertung

Der Trainer-Replacement-Pool enthaelt den vollstaendigen Gen1-Gen9-Basis-Species-Pool:

```text
trainerPool.size=1414
trainerPool.maxSpeciesIdentityNumber=1439
trainerPool.generationCounts={1=271, 2=118, 3=188, 4=149, 5=191, 6=127, 7=123, 8=127, 9=120}
trainerPool.hasGen7=true
trainerPool.hasGen8=true
trainerPool.hasGen9=true
```

Im Trainer-Pool liegen aber acht Zero-BST-/Zero-Ability-Sonder-Species:

```text
trainerPool.zeroAbilitySpecies=8
trainerPool.zeroBstSpecies=8
```

Beispiele:

```text
Bad Egg#identity=412#number=252#gen=3#bst=0#abilities=0/0/0
Warrior#identity=706#number=140#gen=1#bst=0#abilities=0/0/0
Zygarde#identity=835#number=1020#gen=6#bst=0#abilities=0/0/0
Zygarde#identity=836#number=480#gen=6#bst=0#abilities=0/0/0
Ogerpon#identity=1426#number=0#gen=9#bst=0#abilities=0/0/0
Ogerpon#identity=1427#number=0#gen=9#bst=0#abilities=0/0/0
Ogerpon#identity=1428#number=0#gen=9#bst=0#abilities=0/0/0
Ogerpon#identity=1429#number=0#gen=9#bst=0#abilities=0/0/0
```

Bad Egg ist damit im Trainer-Pool vorhanden. `<unknown>` wurde im Pool nicht als Name beobachtet.

## Trainer-Randomization-Ergebnis

`TrainerPokemonRandomizer.randomizeTrainerPokes()` erreicht bei Trainer-Species-only keinen Abschluss innerhalb des Diagnose-Timeouts.

Gezielte Isolierung:

```text
trainers-load:done before.trainers=255 before.trainerPokemon=481 before.nullSpecies=0 before.generationCounts={1=481}
randomizeTrainerPokes:start
timeout=60s
```

Ein separater Stack-Dump nach 10 Sekunden zeigt den blockierenden Pfad:

```text
thread=main state=RUNNABLE
  at com.uprfvx.random.randomizers.TrainerPokemonRandomizer.getRandomAbilitySlot(TrainerPokemonRandomizer.java:647)
  at com.uprfvx.random.randomizers.TrainerPokemonRandomizer.randomizeTrainerPokes(TrainerPokemonRandomizer.java:274)
```

Technische Ursache im Diagnosebefund:

- Trainer-Species-Randomization waehlt eine Ersatz-Species aus dem vollen Pool.
- Danach setzt der Trainer-Pfad auch bei ausgeschalteter Ability-Randomization einen Ability-Slot ueber `getRandomAbilitySlot(newSp)`.
- Fuer Pool-Species mit `ability1=0`, `ability2=0` und `ability3=0` hat diese Schleife keinen gueltigen Slot und beendet sich nicht.

## Trainer-Log-Auswertung

Der Lauf erreicht Save/Log nicht:

```text
saveSuccessful=not reached
logSuccessful=not reached
Output-ROM erzeugt=false
Log nicht leer=false
Gen7/8/9 in Trainer-Picks=not reached
Write/Reload Trainer-Species=not run
```

Es wurde keine Output-ROM erzeugt und kein Trainer-Log geschrieben. Dadurch ist eine Write-/Reload-Bewertung in diesem Diagnoseblock nicht moeglich.

## Interpretation

Trainer-Species-only ist auf dem getesteten CFRU/DPE-Gen9-BPRE-Stand noch nicht P1-supported.

Der Pool selbst ist nicht der Engpass: Gen1-Gen9 ist erreichbar, und der Trainer-Load liefert 255 Trainer mit 481 Trainer-Pokemon ohne Null-Species. Der erste praktische Blocker liegt im Trainer-Randomizer-Scope: Zero-Ability-/Zero-BST-Sonder-Species sind im Trainer-Replacement-Pool erlaubt und koennen den Ability-Slot-Auswahlpfad endlos laufen lassen.

Ein spaeterer Fix sollte mindestens den Trainer-Scope gegen nicht kampffaehige/Trainer-ungeeignete Sonder-Species absichern oder den Ability-Slot-Pfad defensiv behandeln. Danach muss der Trainer-Species-Write/Reload separat bewertet werden, weil der bekannte Gen3-Schreibpfad weiterhin `pokedexToInternal[tp.getSpecies().getNumber()]` verwendet und damit fuer `Species.number=0` Gen7/8/9-Picks riskant bleibt.

## Risiken

- Die Diagnose stoppt vor Save; dadurch sind Trainer-Picks, echter Trainer-Log und Write/Reload noch nicht pruefbar.
- Die verwendeten Timeout-/Stack-Dump-Hilfen lagen ausserhalb des Repos und sind kein dauerhafter Test-Harness.
- Der Befund zeigt einen Trainer-Scope-/Ability-Slot-Blocker; ein nachfolgender Write-Fix kann zusaetzlich noetig sein.
- Keine BizHawk-Gameplay-Pruefung wurde ausgefuehrt.

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
