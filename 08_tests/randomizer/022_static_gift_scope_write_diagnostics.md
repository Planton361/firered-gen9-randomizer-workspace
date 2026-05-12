# P1 Static/Gift Scope and Write Diagnostics

## Datum

2026-05-12

## Branch

Workspace:

```text
compat/upr-fvx-cfru-dpe-static-gift-scope-and-write
```

UPR-FVX:

```text
compat/upr-fvx-cfru-dpe-static-gift-scope-and-write
```

## Ziel

Den P1-Blocker aus `021_p1_static_gift_species_only.md` gezielt beheben und diagnostisch bestaetigen:

- vier `<null>`-Static-Eintraege duerfen Static/Gift-Randomization und Save nicht blockieren
- echte Gen3-Static/Gift-Species muessen fuer erweiterte CFRU/DPE-BPRE-Hacks ueber interne SpeciesSet-Identitaet schreiben und nach Reload erhalten bleiben
- keine Wild-, Starter-, Trainer-, Evolution-, Learnset-, TM-/Tutor-, Ability- oder Palette-Fixes in diesem Branch

## Codeaenderung

UPR-FVX-Commit:

```text
009178e8848b4272e6b8be54a8bf5b2bed34d5f2
```

UPR-FVX PR:

```text
https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/13
```

Geaenderte UPR-FVX-Dateien:

- `random/src/main/java/com/uprfvx/random/randomizers/StaticPokemonRandomizer.java`
- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

Kurzfassung:

- Null-StaticEncounter-Species werden im Static-Pokemon-Randomizer unveraendert durchgereicht und nicht randomisiert.
- `Gen3RomHandler.StaticPokemon.setPokemon()` ueberspringt Null-Species defensiv.
- Gen3 Static/Gift, RSE Static-First-Battle-Tweak und FRLG Ghost-Marowak-Tweak schreiben fuer erweiterte BPRE-Hacks interne `SpeciesSet`-Identitaet statt `pokedexToInternal[Species.number]`.
- Roamer bleiben im bestehenden Gen3-Scope, werden aber nicht durch Null-Species-Schreibversuche blockiert.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Route-1-Fallback-Teststand wie in Protokoll 021. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/**` und wurden nicht committed.

Seed:

```text
274269061345323
```

Settings-Intent:

- Static Pokemon: `COMPLETELY_RANDOM`
- Wild: aus
- Starters: aus
- Trainer: aus
- Evolutions: aus
- Movesets/Learnsets: aus
- TM/Tutor: aus
- Abilities: aus
- Palettes/Sprites: aus
- `limitPokemon=false`

## Build und CLI

UPR-FVX:

```text
./gradlew clean :random:jar
BUILD SUCCESSFUL
```

CLI-Lauf:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/022_static_gift_scope_write/upr-fvx-cfru-dpe-static-gift-scope-write-seed274269061345323.gba \
  -S "<Static/Gift-only settings>" \
  -z 274269061345323 \
  -l
```

CLI-Ergebnis:

```text
Randomized successfully!
Output-ROM: erzeugt
Log: nicht leer
Log-Groesse: 3991 bytes
```

## Static/Gift-Pool-Auswertung

Der Species-Load bleibt gegenueber Protokoll 021 unveraendert:

```text
PokemonCount=1439
pokedexCount=1290
speciesList.size=1415
maxInternalSpeciesId=1439
maxSpeciesNumber=1290
maxSpeciesIdentityNumber=1439
generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Der Static/Gift-Pool bleibt:

```text
staticPool.size=1414
```

Die vier Null-Sonderfaelle bleiben als Scope-Eintraege erhalten, blockieren aber nicht mehr:

```text
nullBefore=4
nullAfterWrite=4
nullReloaded=4
```

## Static/Gift-Log-Auswertung

Der Randomizer-Log enthaelt wieder den Static-Pokemon-Abschnitt. Beispiele aus dem Lauf:

```text
Eevee => Rockruff
Mewtwo => Fidough
Snorlax(2) => Baxcalibur
Deoxys => Finizen
Omanyte => IronLeaves
Magikarp => Hydrapple
Clefairy => Mimikyu
null => null
null(2) => null
null(3) => null
null(4) => null
```

Damit sind Gen7/8/9-Picks im echten Log sichtbar. Die Null-Sonderfaelle werden protokolliert, aber nicht in echte Species-Writes gezwungen.

## Direct Results und Reload

Ein temporaerer lokaler Helper ausserhalb des Repos las `GameRandomizer.Results` aus und verglich die geschriebenen Static/Gift-Species nach Reload ueber `SpeciesSet`-Identitaet.

```text
saveSuccessful=true
logSuccessful=true
directLogBytes=3988
staticCountBefore=29
staticCountAfterWrite=29
staticCountReloaded=29
pickedGen4plus=15
pickedGen7plus=7
reloadedGen4plus=15
reloadedGen7plus=7
writeReloadMismatches=0
```

Beispiele fuer erhaltene interne Identitaet nach Reload:

```text
slot=0  after=Rockruff[identity=961,number=0,gen=7]  reloaded=Rockruff[identity=961,number=0,gen=7]
slot=8  after=Fidough[identity=1316,number=0,gen=9]  reloaded=Fidough[identity=1316,number=0,gen=9]
slot=10 after=Baxcalibur[identity=1395,number=0,gen=9] reloaded=Baxcalibur[identity=1395,number=0,gen=9]
slot=12 after=Finizen[identity=1356,number=0,gen=9] reloaded=Finizen[identity=1356,number=0,gen=9]
slot=16 after=IronLeaves[identity=1408,number=0,gen=9] reloaded=IronLeaves[identity=1408,number=0,gen=9]
slot=19 after=Hydrapple[identity=1431,number=0,gen=9] reloaded=Hydrapple[identity=1431,number=0,gen=9]
slot=25 after=<null> reloaded=<null>
```

## Interpretation

Static/Gift-Species-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand jetzt P1-supported:

- der vollstaendige Gen1-Gen9-Species-Pool bleibt erreichbar
- Null-Sonderfaelle blockieren weder Randomization noch Save
- Output-ROM und nichtleerer Static/Gift-Log entstehen
- echte Static/Gift-Picks mit `Species.number=0` werden ueber interne SpeciesSet-Identitaet geschrieben und nach Reload ohne Mismatch erhalten

Der Fix ist absichtlich auf Static/Gift-Scope und Static/Gift-Species-Write begrenzt. Trainer-, Evolution-, Learnset-, TM-/Tutor-, Ability-, Wild- und Day/Night-Pfade bleiben separate Folgearbeiten.

## Risiken

- Die vier Null-Eintraege sind weiter nur als Scope-Sonderfaelle erhalten; ihre fachliche Herkunft bleibt fuer einen spaeteren Roamer-/hardcoded-FRLG-Scope-Block dokumentierbar.
- Die Generationserkennung einzelner DPE-Sondernamen bleibt nicht perfekt, aber die Reload-Bewertung nutzt interne Identitaet und zeigt konkrete Gen7/9-Beispiele.
- Es wurde kein BizHawk-Gameplay-Smoke fuer einzelne Static/Gift-Events ausgefuehrt.

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

Workspace-PR fuer diesen Pin und die Diagnose mergen. Danach als separaten P1-Block Trainer-Species-only diagnostizieren, weil `Gen3RomHandler.trainerPokemonToBytes()` weiterhin als eigener `pokedexToInternal[Species.number]`-Pfad dokumentiert ist.
