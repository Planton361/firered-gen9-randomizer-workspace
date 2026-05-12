# P1 Trainer Scope and Write Diagnostics

## Datum

2026-05-12

## Branch

Workspace:

```text
compat/upr-fvx-cfru-dpe-trainer-scope-and-write
```

UPR-FVX:

```text
compat/upr-fvx-cfru-dpe-trainer-scope-and-write
```

## Ziel

Den P1-Blocker aus `023_p1_trainer_species_only.md` gezielt beheben und diagnostisch bestaetigen:

- nicht kampffaehige CFRU/DPE-Sonder-Species duerfen nicht im Trainer-Replacement-Pool bleiben
- `getRandomAbilitySlot()` darf fuer Zero-Ability-Species nicht endlos laufen
- echte Trainer-Species muessen fuer erweiterte CFRU/DPE-BPRE-Hacks ueber interne SpeciesSet-Identitaet schreiben und nach Reload erhalten bleiben
- keine Wild-, Starter-, Static-/Gift-, Evolution-, Learnset-, TM-/Tutor-, allgemeine Ability- oder Palette-Fixes in diesem Branch

## Codeaenderung

UPR-FVX-Commit:

```text
56ec749eca12a8637c20f943b520a9bb6a9d469a
```

UPR-FVX PR:

```text
https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/14
```

Geaenderte UPR-FVX-Dateien:

- `random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java`
- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

Kurzfassung:

- Im erkannten erweiterten CFRU/DPE-BPRE-Modus werden Trainer-Replacement-Species mit `BST=0` oder ohne gueltige Ability aus dem Trainer-Pool entfernt.
- `getRandomAbilitySlot()` waehlt nur noch aus real vorhandenen Ability-Slots und faellt defensiv auf Slot 1 zurueck, falls keine Ability vorhanden ist.
- Gen3-Trainer-Species schreiben fuer erweiterte BPRE-Hacks interne `SpeciesSet`-Identitaet statt `pokedexToInternal[Species.number]`.
- Mossdeep-Steven-Trainer-Species nutzen denselben internen Trainer-Species-Write-Helfer.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Route-1-Fallback-Teststand wie in Protokoll 021 bis 023. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/**` und wurden nicht committed.

Seed:

```text
274269061345323
```

Trainer-Species-only Settings-String:

```text
422AAgEAQQBAAQABwAEAALkAwARAAEUAAAUAEAEAAEA/wAAAAAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjDnKwhm48M4ig==
```

Settings-Intent:

- Trainer Pokemon randomisieren: an
- Trainer Moves/Movesets: aus
- Trainer Held Items: aus
- Wild: aus
- Starters: aus
- Static/Gift: aus
- Evolutions: aus
- Learnsets/Movesets: aus
- TM/HM/Tutor: aus
- Abilities: aus
- Palette-/Sprite-Randomization: aus
- `limitPokemon=false`
- keine Gen1-3-Einschraenkung

## Build und CLI

UPR-FVX:

```text
./gradlew clean :random:jar
BUILD SUCCESSFUL
```

CLI-Ergebnis:

```text
Randomized successfully!
Output-ROM: erzeugt
Log: nicht leer
Log-Groesse: 17842 bytes
```

## Species- und Trainer-Load

Der Species-Load bleibt auf dem erwarteten Gen9-Coverage-Stand:

```text
PokemonCount=1439
speciesList.size=1415
maxSpeciesIdentityNumber=1439
generationCounts={1=271, 2=118, 3=188, 4=149, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Der Trainer-Load bleibt stabil:

```text
trainers=255
trainerPokemon=481
nullSpecies=0
```

## Trainer-Pool-Auswertung

Vor dem neuen CFRU/DPE-Trainer-Sonderfilter:

```text
trainerPoolBefore.size=1414
trainerPoolBefore.generationCounts={1=271, 2=118, 3=188, 4=149, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Der Filter entfernt acht nicht kampffaehige Sonder-Species:

```text
excludedSpecialSpecies.count=8
excludedSpecialSpecies.list=[
  Ogerpon#identity=1426#number=0#gen=9#bst=0#abilities=0/0/0,
  Ogerpon#identity=1427#number=0#gen=9#bst=0#abilities=0/0/0,
  Ogerpon#identity=1428#number=0#gen=9#bst=0#abilities=0/0/0,
  Ogerpon#identity=1429#number=0#gen=9#bst=0#abilities=0/0/0,
  Warrior#identity=706#number=140#gen=1#bst=0#abilities=0/0/0,
  Bad Egg#identity=412#number=252#gen=3#bst=0#abilities=0/0/0,
  Zygarde#identity=836#number=480#gen=6#bst=0#abilities=0/0/0,
  Zygarde#identity=835#number=1020#gen=6#bst=0#abilities=0/0/0
]
```

Nach dem Filter:

```text
trainerPoolAfter.size=1406
trainerPoolAfter.generationCounts={1=270, 2=118, 3=187, 4=149, 5=191, 6=125, 7=123, 8=127, 9=116}
trainerPoolAfter.hasGen7=true
trainerPoolAfter.hasGen8=true
trainerPoolAfter.hasGen9=true
```

## Trainer-Randomization-Ergebnis

Der direkte Diagnose-Lauf erreicht Save, Log und Reload:

```text
before.trainers=255
before.trainerPokemon=481
before.nullSpecies=0
after.trainers=255
after.trainerPokemon=481
after.nullSpecies=0
after.generationCounts={1=93, 2=36, 3=62, 4=51, 5=77, 6=39, 7=46, 8=39, 9=38}
after.pickedGen4plus=290
after.pickedGen7plus=123
after.hasGen7=true
after.hasGen8=true
after.hasGen9=true
after.badEggOrUnknown=false
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
logBytes=17839
logContainsTrainerPokemon=true
logBadEggOrUnknown=false
```

Beispiele fuer Gen7/8/9-Picks im Direct Results-Lauf:

```text
Dachsbun#identity=1317
Silvally#identity=1051
Lycanroc#identity=1082
Kartana#identity=1015
Urshifu#identity=1184
Glimmora#identity=1364
Inteleon#identity=1110
Tadbulb#identity=1331
Toxtricity#identity=1285
```

## Trainer-Log-Auswertung

Der echte CLI-Log enthaelt wieder den Trainer-Pokemon-Abschnitt:

```text
Trainer Pokemon: Randomized/Changed
Trainer Movesets: Unchanged
Trainer Names: Unchanged
```

Beispiele aus dem Trainer-Log:

```text
Dachsbun Lv5
Silvally Lv5
Lycanroc Lv5
Kartana Lv5
Urshifu Lv5
Glimmora Lv5
Tadbulb Lv5
Terapagos Lv5
Meltan Lv5
```

Im Trainer-Log wurden `Bad Egg` und `<unknown>` nicht beobachtet.

## Write/Reload

Der Reload-Vergleich nutzt interne `SpeciesSet`-Identitaet:

```text
reload.trainers=255
reload.trainerPokemon=481
reload.nullSpecies=0
reload.generationCounts={1=93, 2=36, 3=62, 4=51, 5=77, 6=39, 7=46, 8=39, 9=38}
reload.hasGen7=true
reload.hasGen8=true
reload.hasGen9=true
reload.badEggOrUnknown=false
writeReloadCompared=481
writeReloadMismatches=0
writeReloadFirstMismatch=null
```

## Interpretation

Trainer-Species-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand jetzt P1-supported:

- der Trainer-Replacement-Pool bleibt Gen1-Gen9-faehig
- nicht kampffaehige Sonder-Species werden aus dem Trainer-Scope entfernt
- der dokumentierte `getRandomAbilitySlot()`-Endloslauf ist behoben
- Output-ROM und nichtleerer Trainer-Log entstehen
- echte Trainer-Picks mit `Species.number=0` werden ueber interne SpeciesSet-Identitaet geschrieben und nach Reload ohne Mismatch erhalten

Der Fix ist absichtlich auf Trainer-Species-Scope, defensive Trainer-Ability-Slot-Auswahl und Trainer-Species-Write begrenzt. Trainer-Movesets, Learnsets, Trainer-Held-Items, allgemeine Ability-Randomization, Wild, Starter, Static/Gift, Evolutions, TM-/Tutor- und Palette-Pfade bleiben separate Folgearbeiten.

## Risiken

- Es wurde kein BizHawk-Gameplay-Smoke gegen die erzeugte Output-ROM ausgefuehrt.
- Die Sonderfilter-Regel ist fuer CFRU/DPE-BPRE bewusst konservativ und basiert auf `BST=0` oder komplett fehlenden Ability-Slots; weitere fachliche Sonderformen koennen spaeter separat klassifiziert werden.
- Trainer-Moveset- und Held-Item-Pfade blieben absichtlich ausgeschaltet und sind damit nicht durch diesen Lauf bestaetigt.

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

## Naechster minimaler Schritt

UPR-FVX PR #14 und den Workspace-Pin/Diagnose-PR reviewen und mergen. Danach den naechsten P1-Species-Pfad als separaten Diagnoseblock starten, ohne Trainer-Moveset-/Learnset-/Item-/Ability-Randomization zu vermischen.
