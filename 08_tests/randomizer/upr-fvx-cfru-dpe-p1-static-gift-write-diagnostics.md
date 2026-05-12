# UPR-FVX CFRU/DPE P1 Static/Gift Write Diagnostics

Datum: 2026-05-12

## Kontext

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-static-gift-write-diagnostics`
- UPR-FVX-Submodule-Commit: `39c57880`
- UPR-FVX-Submodule-Branch lokal: `compat/upr-fvx-cfru-dpe-starter-internal-species-write`
- UPR-FVX PR #6: gemerged
- Workspace PR #40: gemerged
- Ziel: Static-/Gift-only Diagnose nach P0 und P1a Starter-Fix, ohne Codeaenderungen.

## Read-only Codebefund

UPR-FVX liest Gen3-Static/Gift-Species bereits als interne ROM-Werte:

- `Gen3RomHandler.StaticPokemon.getPokemon()` liest `readWord(speciesOffsets[0])` und gibt `pokesInternal[...]` zurueck.
- `Gen3RomHandler.getStaticPokemon()` baut daraus `StaticEncounter`-Eintraege.

Der Schreibpfad nutzt dagegen weiter Dex-/Pokedex-Nummern:

- `Gen3RomHandler.StaticPokemon.setPokemon()` schreibt `pokedexToInternal[pkmn.getNumber()]`.
- `Gen3RomHandler.setStaticPokemon()` nutzt diesen Pfad fuer `romEntry.getStaticPokemon()`.
- Die hardcoded FRLG/RSE-Faelle `StaticFirstBattleTweak` und `GhostMarowakTweak` schreiben ebenfalls `pokedexToInternal[...getNumber()]`.
- `setRoamers()` nutzt ebenfalls `StaticPokemon.setPokemon()`, bleibt aber fuer diesen Diagnoseblock separater Scope.

Der Logger ist fuer diese Diagnose nur bedingt nutzbar:

- `RandomizationLogger.logStaticPokemon()` liest neue Werte nach dem Schreiben erneut ueber `romHandler.getStaticPokemon()`.
- Wenn der Schreibpfad auf Gen1-3 zurueckfaellt, wuerde der Log den Reload-Zustand zeigen, nicht den urspruenglich gewaehlten Kandidaten.

## Build

Ausgefuehrt:

```sh
cd 02_external/upr-fvx
./gradlew clean :random:jar
```

Ergebnis:

- Build erfolgreich.
- Gradle meldete nur bestehende Deprecation-Warnungen.
- Keine Build-Artefakte wurden committed.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Teststand wie in den P0/P1a-Diagnosen. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/`.

Settings-Intent:

- Static Pokemon: `COMPLETELY_RANDOM`
- Wild: aus
- Starters: aus
- Trainer: aus
- Evolutions: aus
- Movesets/Learnsets: aus
- TM/Tutor: aus
- Abilities: aus
- `limitPokemon=false`
- `currentRestrictions=null`
- keine Gen1-3-Einschraenkung

Verwendete Settings-Zeichenfolge:

```text
422AAgEAQQBAAQABwAEAAHkAwARAAQUAAAUAEAEAAEA/////wAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjABFo1648M4ig==
```

CLI-Lauf:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-p1-static-gift-write-diagnostics-seed274269061345323.gba \
  -S "<settings>" \
  -z 274269061345323 \
  -l
```

## Species-/Pool-Diagnose

Console-Diagnose beim Laden:

```text
ROM code=BPRE version=0 isRomHack=true
PokemonCount=823 pokedexCount=386 speciesList.size=799 maxInternalSpeciesId=823 maxSpeciesNumber=411 maxSpeciesIdentityNumber=823
generationCounts={1=177, 2=104, 3=161, 4=139, 5=178, 6=64}
```

Unrestricted Species-Pool fuer Static/Gift:

```text
speciesList/all: size=798, gen4plus=381
nonLeg: size=756, gen4plus=360
```

Damit ist Gen4+ fuer Static/Gift-Auswahl im Pool vorhanden.

## Static/Gift-Read-Befund

`romHandler.canChangeStaticPokemon()` bleibt nach `Settings.tweakForRom()` aktiv:

```text
beforeTweak.staticPokemonMod=COMPLETELY_RANDOM
afterTweak.staticPokemonMod=COMPLETELY_RANDOM
canChangeStaticPokemon=true
staticCount=29
```

Die ersten 25 gelesenen Static/Gift-Eintraege sind regulaere Gen1-3-Species, z. B.:

```text
0: Eevee gen=1 number=133 identity=133 level=25
5: Zapdos gen=1 number=145 identity=145 level=50
12: Deoxys gen=3 number=386 identity=410 level=30
18: Lapras gen=1 number=131 identity=131 level=25
24: Porygon gen=1 number=137 identity=137 level=26
```

Die letzten vier Eintraege werden im lokalen Teststand als Null-Species gelesen:

```text
25: <null> level=0
26: <null> level=50
27: <null> level=50
28: <null> level=50
```

Diese Eintraege liegen im Static/Roamer-/hardcoded-FRLG-Scope und blockieren den Static/Gift-only Randomizer-Lauf, bevor Write/Reload sinnvoll bewertet werden kann.

## Static/Gift-Pick-Diagnose

Ein read-only Hilfscheck hat den `COMPLETELY_RANDOM`-Pick-Pfad fuer Seed `274269061345323` ohne ROM-Schreiben nachgebildet.

Auszug:

```text
staticCount=29
poolSize=798 gen4plus=381
0: Eevee -> Butterfree gen=1 number=12 identity=12
1: Hitmonlee -> Pawniard gen=5 number=96 identity=677
2: Hitmonchan -> Scraggy gen=5 number=385 identity=612
4: Electrode -> Klang gen=5 number=53 identity=653
5: Zapdos -> Meloetta gen=5 number=190 identity=746
9: Snorlax -> Delphox gen=6 number=209 identity=763
12: Deoxys -> Arceus gen=4 number=154 identity=720
13: Ho-Oh -> Goomy gen=6 number=401 identity=812
16: Omanyte -> Phantump gen=6 number=405 identity=816
17: Kabuto -> Meowstic gen=6 number=240 identity=786
19: Magikarp -> Kricketot gen=4 number=291 identity=454
20: Abra -> Tornadus gen=5 number=198 identity=754
26: <null> -> Meloetta gen=5 number=135 identity=701
pickedGen4plus=14
```

Interpretation:

- Die Static/Gift-Auswahl kann Gen4+-Species aus dem unrestricted Pool ziehen.
- Die Auswahl erreicht Gen4+/Gen5/Gen6-Kandidaten bereits mit demselben Seed wie der Starter-Block.
- Der praktische Write/Reload-Beweis ist blockiert, weil der echte Randomizer-Lauf an Null-Static-Eintraegen abbricht.

## CLI-/Log-Befund

Der CLI-Lauf schrieb nur ein leeres Log mit BOM:

```text
upr-fvx-cfru-dpe-p1-static-gift-write-diagnostics-seed274269061345323.gba.log: 3 bytes
```

Ein direkter `GameRandomizer`-Diagnoselauf zeigt den eigentlichen Fehler:

```text
saveSuccessful=false
java.lang.NullPointerException: Cannot invoke "com.uprfvx.romio.gamedata.Species.getNumber()" because the return value of "com.uprfvx.romio.gamedata.StaticEncounter.getSpecies()" is null
    at com.uprfvx.random.randomizers.StaticPokemonRandomizer.randomizeStaticPokemon(StaticPokemonRandomizer.java:283)
logSuccessful=true
logBytes=0
```

Wichtig: Die CLI-Ausgabe meldete trotzdem `Randomized successfully!`, obwohl `GameRandomizer.Results.wasSaveSuccessful=false` war und keine Output-ROM geschrieben wurde. Fuer diesen Diagnoseblock wurde deshalb kein breiterer Randomizer-Lauf ausgefuehrt.

## Technische Interpretation

Static/Gift ist noch nicht P1-supported.

Es gibt zwei getrennte Befunde:

1. Der geladene Static-/Roamer-Scope enthaelt Null-Species-Eintraege. Diese loesen im StaticPokemonRandomizer einen NPE aus, noch bevor ein stabiler Write/Reload-Vergleich moeglich ist.
2. Der Gen3-Schreibpfad benutzt weiter `pokedexToInternal[Species.number]`. Sobald der Null-Scope behoben oder ausgeklammert ist, besteht fuer erweiterte CFRU/DPE-BPRE-Hacks dasselbe Dex-ID-vs-interne-ID-Risiko wie zuvor bei Wild und Startern.

Der naechste Fix sollte deshalb nicht blind nur `setPokemon()` umstellen, sondern zuerst den Static/Gift-Scope sauber trennen:

- echte Static/Gift-Offsets
- hardcoded Ghost Marowak / StaticFirstBattle
- FRLG-Roamer
- Null-/uninitialisierte Eintraege

Danach kann der interne SpeciesSet-Identity-Schreibpfad fuer echte Static/Gift-Eintraege minimal umgesetzt und erneut gegen Reload geprueft werden.

## Ergebnis

- Gen4+ ist im Static/Gift-Pool vorhanden: ja.
- Der Pick-Pfad kann Gen4+ auswaehlen: ja, im read-only Pick-Check `14/29`.
- Echter CLI-Write/Reload erfolgreich: nein.
- Randomizer-Log Static/Gift: nein, Log bleibt leer, weil der Lauf vor Save/Logging abbricht.
- Static/Gift-Write-Fix noetig: ja, aber nur zusammen mit einer vorherigen Static/Roamer-/Null-Scope-Abgrenzung.

## Risiken

- Der Hilfscheck bildet den `COMPLETELY_RANDOM`-Pick-Pfad nach, schreibt aber nicht in die ROM und ersetzt keinen echten Randomizer-Log.
- Die letzten vier `<null>`-Eintraege koennen Roamer-/Patch-/hardcoded-FRLG-Scope sein; sie duerfen nicht unbesehen als normale Gift-Pokemon behandelt werden.
- Ein Fix, der alle StaticPokemon-Eintraege pauschal intern schreibt, koennte Roamer oder hardcoded Spezialfaelle unbeabsichtigt veraendern.

## Naechster minimaler Schritt

Neuer UPR-FVX-Diagnose-/Fixbranch fuer Static/Gift-Scope:

```text
compat/upr-fvx-cfru-dpe-static-gift-scope-and-write
```

Ziel:

- Null-/Roamer-/hardcoded-Eintraege im FRLG-Static-Scope sauber klassifizieren.
- Echte Static/Gift-Eintraege fuer erweiterte CFRU/DPE-BPRE-Hacks ueber interne SpeciesSet-Identitaet schreiben.
- Roamer-Fixes weiterhin separat halten, falls sie ein eigenes Datenmodell brauchen.
