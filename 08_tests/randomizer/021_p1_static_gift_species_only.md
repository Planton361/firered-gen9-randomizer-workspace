# UPR-FVX CFRU/DPE P1 Static/Gift Species-only Diagnostics

Datum: 2026-05-12

## Ziel

Dieser Arbeitsblock diagnostiziert Static/Gift-Randomization auf dem Gen9-Wild-sauberen UPR-FVX-Stand.

Keine Codeaenderung, kein Fix und keine Static/Gift-Scope-Aenderung wurden umgesetzt.

## Stand

```text
Workspace-Branch: analysis/upr-fvx-cfru-dpe-p1-static-gift-species-only
Workspace-main Voraussetzung: PR #56 gemerged
UPR-FVX Submodule: 0f127e9bb9a5c47306fe1f2af11e8e9fe1802717
UPR-FVX Branch lokal: compat/upr-fvx-cfru-dpe-wild-banned-special-species
UPR-FVX Commit: 0f127e9b compat: ban CFRU DPE special species from wild pool
```

Der Stand enthaelt die bestaetigte Gen9-Wild-Fixkette inklusive Wild-Sonder-Species-Ban.

## Build und Checks

UPR-FVX:

```sh
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
```

Ergebnis:

- UPR-FVX-Working-Tree vor dem Build sauber.
- `git diff --stat`: leer.
- `git diff --check`: ok.
- `./gradlew clean :random:jar`: `BUILD SUCCESSFUL`.

## Teststand und Settings

Verwendet wurde derselbe lokale CFRU/DPE-BPRE-Route-1-Fallback-Teststand wie in den vorherigen Randomizer-Smokes. ROM-, Output- und Log-Artefakte blieben lokal/ignored unter `05_builds/**` und wurden nicht committed.

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
- keine Gen1-3-Einschraenkung

Seed:

```text
274269061345323
```

## Species-Coverage

Der ROM-Load erreicht weiterhin den vollstaendigen CFRU/DPE-Gen9-Species-Stand:

```text
PokemonCount=1439
pokedexCount=1290
speciesList.size=1415
maxInternalSpeciesId=1439
maxSpeciesNumber=1290
maxSpeciesIdentityNumber=1439
generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Die bekannten CFRU/DPE-Unblocker sind aktiv:

```text
[CFRU-DPE-PALETTE] skipped invalid pokemon palettes during load: normal=2 shiny=2
```

## Static/Gift-Pool-Auswertung

Der direkte Diagnose-Lauf bestaetigt, dass Static/Gift denselben uneingeschraenkten Gen1-Gen9-Speciesraum erreicht:

```text
staticPokemonMod=COMPLETELY_RANDOM
limitPokemon=false
canChangeStaticPokemon=true
allNoFormes.size=1414 generations={1=271, 2=118, 3=188, 4=149, 5=191, 6=127, 7=123, 8=127, 9=120}
allWithFormesNonCosmetic.size=1414 generations={1=271, 2=118, 3=188, 4=149, 5=191, 6=127, 7=123, 8=127, 9=120}
staticBanned.size=0 generations={}
staticPool.size=1414 generations={1=271, 2=118, 3=188, 4=149, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Hinweis: `speciesList.size=1415`, aber der Static/Gift-Pool ohne Formes enthaelt `1414` Species. Der Unterschied ist fuer diesen Diagnoseblock nicht der Blocker; Gen7/8/9 sind im Pool vorhanden.

## Static/Gift-Read-Auswertung

UPR-FVX liest `29` Static/Gift-Eintraege aus dem lokalen CFRU/DPE-Teststand.

Die ersten `25` Eintraege sind regulaere Gen1-3-Static/Gift-Species, darunter:

```text
Eevee Lv25
Hitmonlee Lv25
Hitmonchan Lv25
Zapdos Lv50
Articuno Lv50
Moltres Lv50
Mewtwo Lv70
Deoxys Lv30
Ho-Oh Lv70
Lugia Lv70
Lapras Lv25
Porygon Lv26
```

Die letzten vier Eintraege werden weiterhin als Null-Species gelesen:

```text
static[25] species=<null> level=0
static[26] species=<null> level=50
static[27] species=<null> level=50
static[28] species=<null> level=50
staticNullCount=4
```

Diese Eintraege liegen im Static/Roamer-/hardcoded-FRLG-Scope und muessen separat klassifiziert werden.

## Static/Gift-Pick-Auswertung

Ein temporaerer read-only Diagnose-Helper ausserhalb des Repos hat den `COMPLETELY_RANDOM`-Pick-Pfad fuer Seed `274269061345323` ohne Codeaenderung nachgebildet.

Auszug:

```text
pick[00] Eevee -> Rockruff gen=7 identity=961
pick[08] Mewtwo -> Fidough gen=9 identity=1316
pick[10] Snorlax -> Baxcalibur gen=9 identity=1395
pick[12] Deoxys -> Finizen gen=9 identity=1356
pick[13] Ho-Oh -> Arceus gen=4 identity=721
pick[16] Omanyte -> IronLeaves gen=9 identity=1408
pick[19] Magikarp -> Hydrapple gen=9 identity=1431
pick[21] Clefairy -> Mimikyu gen=7 identity=1072
pick[25] <null> -> Silvally gen=7 identity=1063
pick[28] <null> -> Dialga gen=4 identity=919
pickedGen4plus=18
pickedGen7plus=8
```

Bewertung:

- Static/Gift-Auswahl erreicht Gen4+ klar.
- Gen7/8/9 sind im Pick-Pfad erreichbar.
- Mehrere DPE/CFRU-Form-/Paradox-/Gen9-Eintraege haben `Species.number=0`, aber stabile `SpeciesSet identity`-Werte. Das bestaetigt, dass ein spaeterer Write-Fix nicht ueber Dex-/Pokedex-Nummern gehen darf.

## CLI-/Log-Auswertung

Der CLI-Lauf wurde mit Static/Gift-only Settings, Seed `274269061345323` und `-l` gestartet.

CLI:

```text
Randomized successfully!
```

Lokale Log-Auswertung:

```text
*.gba.log: 3 bytes
Log-Inhalt: nur UTF-8 BOM
Static/Gift-Log: keine Eintraege
Output-ROM: nicht erzeugt
```

Der CLI-Erfolg ist deshalb irrefuehrend. Direkt ueber `GameRandomizer.Results` ergibt derselbe Lauf:

```text
saveSuccessful=false
exceptionClass=java.lang.NullPointerException
exceptionMessage=Cannot invoke "com.uprfvx.romio.gamedata.Species.getNumber()" because the return value of "com.uprfvx.romio.gamedata.StaticEncounter.getSpecies()" is null
stack=com.uprfvx.random.randomizers.StaticPokemonRandomizer.randomizeStaticPokemon(StaticPokemonRandomizer.java:283)
logSuccessful=true
directLogBytes=0
```

## Technische Interpretation

Static/Gift ist auf dem aktuellen Gen9-Wild-sauberen Stand noch nicht P1-supported.

Die Diagnose trennt drei Befunde:

1. Der Static/Gift-Pool ist nicht mehr Gen1-3-gekappt. Er enthaelt Gen1-Gen9 und erreicht `1414` Species.
2. Der Pick-Pfad kann Gen7/8/9 auswaehlen; im Seed `274269061345323` entstehen `18/29` Gen4+-Picks und `8/29` Gen7+-Picks.
3. Der echte Write-/Save-/Log-Pfad bricht vor dem Save an vier `<null>`-Static-Eintraegen ab. Dadurch gibt es noch keinen belastbaren Reload-Beweis.

Zusatzrisiko fuer den spaeteren Fix:

- Der bekannte Gen3-Static-Schreibpfad schreibt ueber `pokedexToInternal[Species.number]`.
- Mehrere aktuelle Pick-Kandidaten haben `Species.number=0` bei gueltiger interner `SpeciesSet identity`.
- Ein spaeterer Write-Fix muss deshalb echte Static/Gift-Eintraege ueber interne SpeciesSet-Identitaet schreiben und vorher Null-/Roamer-/hardcoded-Scope abgrenzen.

## Ergebnis

| Frage | Befund |
|---|---|
| Vollstaendiger Gen1-Gen9 Static/Gift-Pool vorhanden | ja |
| Gen7/8/9 im Static/Gift-Pick-Pfad erreichbar | ja |
| CLI meldet Erfolg | ja, aber irrefuehrend |
| `saveSuccessful` laut `GameRandomizer.Results` | false |
| Static/Gift-Log auswertbar | nein, Log bleibt leer |
| Output-ROM erzeugt | nein |
| Spaeterer Scope-Fix noetig | ja |
| Spaeterer Write-Fix noetig | sehr wahrscheinlich ja |

## Risiken

- Der temporaere Diagnose-Helper lag ausserhalb des Repos und wurde nicht committed.
- Der Pick-Check bildet den Static/Gift-Pick-Pfad nach, ersetzt aber keinen echten Reload-Beweis.
- Die vier `<null>`-Eintraege duerfen nicht pauschal als normale Gift-Pokemon behandelt werden.
- Roamer, Ghost Marowak, StaticFirstBattle und echte Gifts muessen vor einem Fix getrennt werden.
- Die CLI meldet trotz internem `saveSuccessful=false` Erfolg; fuer Static/Gift muss deshalb bis zu einem CLI-Fix direkt auf `GameRandomizer.Results` oder erzeugte Output-Artefakte geachtet werden.

## Naechster minimaler Schritt

Neuer UPR-FVX-Diagnose-/Fixbranch:

```text
compat/upr-fvx-cfru-dpe-static-gift-scope-and-write
```

Ziel:

- Static/Gift-, Roamer- und hardcoded-FRLG-Eintraege sauber klassifizieren.
- Null-Species-Eintraege aus dem normalen Static/Gift-Randomizer-Pfad ausklammern oder korrekt modellieren.
- Echte Static/Gift-Species fuer erweiterte CFRU/DPE-BPRE-Hacks ueber interne SpeciesSet-Identitaet schreiben.
- Danach denselben Seed erneut mit Reload-/Log-Beweis pruefen.
