# UPR-FVX Gen4+ Wild Pool Diagnostics

## Datum

2026-05-11

## Ziel

Gezielt pruefen, ob Gen4+-Species nach UPR-FVX PR #3 im finalen Wild-Randomizer-Pool und in der tatsaechlichen Wild-Auswahl landen, wenn die verwendeten Settings Gen4+ nicht absichtlich ausschliessen.

## UPR-FVX-Stand

- Fork: `Planton361/universal-pokemon-randomizer-fvx`
- PR: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/3`
- PR-Status laut `gh pr view`: offen.
- Lokaler Branch: `compat/upr-fvx-gen9-generation-mapping`
- Lokaler Commit: `223ee9efaf1a29435674cbe6a03f25011364b2a1`
- Commit-Titel: `compat: preserve CFRU DPE species identity`

## Lokaler Teststand

- Verwendet wurde derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand aus `05_builds/`.
- Input-ROM, Output-ROM, Konsolenlog und Randomizer-Log blieben lokal/ignored unter `05_builds/`.
- Keine ROMs, Builds, Randomizer-JARs, Saves oder Emulator States wurden committed.
- Keine privaten absoluten Pfade werden in diesem Protokoll dokumentiert.

## Build

```sh
cd 02_external/upr-fvx
./gradlew clean :random:jar
```

Ergebnis: `BUILD SUCCESSFUL`.

## Settings und Startbefehl

Verwendeter CLI-Lauf, relativ zum Workspace:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-gen4plus-wild-pool-diagnostics.gba \
  -S "422AAgEAQQBAAQABwAEAAHkCAARAQEUAAAUAEAEAAEA/wAAAAAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjD84HA048M4ig==" \
  -z 274269061345319 \
  -l
```

Settings-Intent:

- Wild Pokemon Randomization aktiv.
- `limitPokemon=false`.
- Generation-Restrictions im Settings-String explizit auf alle bekannten `GenRestrictions`-Bits gesetzt (`1` bis `7`, plus evolutionary relatives).

Wichtiger Befund: Der Randomizer-Log schreibt die Settings canonical wieder mit `currentRestrictions=-1`, semantisch ebenfalls "alle" vor ROM-Tweak. Trotzdem werden die Restrictions waehrend `Settings.tweakForRom()` fuer Gen3-ROMs auf `romHandler.generationOfPokemon()` begrenzt.

## Lokale Artefakte

Nicht committed:

- Console/stderr: `05_builds/randomizer-smoke/upr-fvx-gen4plus-wild-pool-diagnostics-console.log`
- Randomizer-Log: `05_builds/randomizer-smoke/upr-fvx-gen4plus-wild-pool-diagnostics.gba.log`
- Output-ROM: `05_builds/randomizer-smoke/upr-fvx-gen4plus-wild-pool-diagnostics.gba`

Hashes:

```text
9deaf9277d37506101a9ec55b2bba74ebcd322af36227fc088575b557630c200  upr-fvx-gen4plus-wild-pool-diagnostics.gba
24cefc1c95c0feffed9a2f205d7aebd366b0c0f4379974507335d10ac6f7dfb8  upr-fvx-gen4plus-wild-pool-diagnostics.gba.log
70ca71e03c2ad8af81e0e87409b5549d11ac95efc821a6efb48d21b3130d1315  upr-fvx-gen4plus-wild-pool-diagnostics-console.log
```

## Species-Pool-Diagnose

stderr-Diagnose aus `Gen3RomHandler`:

```text
ROM code=BPRE
version=0
isRomHack=true
PokemonCount=823
pokedexCount=386
speciesList.size=799
maxInternalSpeciesId=823
maxSpeciesNumber=411
maxSpeciesIdentityNumber=823
generationCounts={1=177, 2=104, 3=161, 4=139, 5=178, 6=64}
```

Beispiel-Species ueber 386:

| Internal ID | Interne Identitaet | Dex-/Species-Nummer | Name | Generation |
|---:|---:|---:|---|---:|
| 798 | 798 | 387 | Skrelp | 6 |
| 799 | 799 | 388 | Dragalge | 6 |
| 800 | 800 | 389 | Clauncher | 6 |
| 801 | 801 | 390 | Clawitzer | 6 |
| 802 | 802 | 391 | Helioptile | 6 |
| 803 | 803 | 392 | Heliolisk | 6 |
| 804 | 804 | 393 | Tyrunt | 6 |
| 805 | 805 | 394 | Tyrantrum | 6 |
| 806 | 806 | 395 | Amaura | 6 |
| 807 | 807 | 396 | Aurorus | 6 |
| 808 | 808 | 397 | Sylveon | 6 |
| 809 | 809 | 398 | Hawlucha | 6 |

## Wild-Log-Auswertung

Ausgewertet wurden die sichtbaren Namen im Randomizer-Wild-Pokemon-Log.

| Generation | Wild-Slots |
|---|---:|
| Gen1 | 841 |
| Gen2 | 527 |
| Gen3 | 791 |
| Gen4 | 0 |
| Gen5 | 0 |
| Gen6 | 0 |
| Gen7+ | 0 |
| `<unknown>` | 17 |

Weitere Werte:

- Gesamt ausgewertete Wild-Slots: `2176`
- Eindeutige sichtbare Species-Namen: `105`
- Sichtbare Gen4+-Species im Wild-Log: keine
- `<unknown>`-stderr-Rohwerte: weiterhin ausschliesslich `rawInternalSpeciesId=0`

Top sichtbare Wild-Namen:

```text
Beedrill, Girafarig, Skitty, Anorith, Relicanth, Kecleon,
Aerodactyl, Spearow, Swalot, Poliwrath, Pupitar, Arcanine,
Slaking, Butterfree, Qwilfish, Pidgeotto, Unown, Marowak,
Lileep, Dragonite
```

## Read-only Ursachenanalyse

Relevante Codepfade:

- `random/src/main/java/com/uprfvx/random/GameRandomizer.java`
- `random/src/main/java/com/uprfvx/random/Settings.java`
- `romio/src/main/java/com/uprfvx/romio/services/RestrictedSpeciesService.java`
- `romio/src/main/java/com/uprfvx/romio/gamedata/GenRestrictions.java`
- `random/src/main/java/com/uprfvx/random/randomizers/WildEncounterRandomizer.java`

Der CLI-Settings-String erlaubt Gen4+ initial. `Settings.tweakForRom()` limitiert `currentRestrictions` aber fuer ROMs auf `rh.generationOfPokemon()`. Fuer `Gen3RomHandler` ist das `3`.

Danach ruft `GameRandomizer.setupSpeciesRestrictions()` immer:

```java
romHandler.getRestrictedSpeciesService().setRestrictions(settings.getCurrentRestrictions());
```

Das geschieht unabhaengig davon, ob `settings.isLimitPokemon()` false ist. `limitPokemon` steuert danach nur noch `removeEvosForPokemonPool()`, nicht ob die Restrictions fuer den erlaubten Species-Pool gelten.

`RestrictedSpeciesService` filtert anschliessend nach:

```java
sp.getBaseForme().getGeneration() == gen
```

Damit wird der erweiterte RomHandler-Pool trotz PR #3 vor dem Wild-Randomizer effektiv auf Gen1-3 begrenzt. `WildEncounterRandomizer` baut seinen Allowed-Pool aus `rSpecService.getSpecies(...)`; dadurch kann die finale Wild-Auswahl keine Gen4+-Species enthalten.

## Technische Interpretation

PR #3 wirkt weiterhin korrekt:

- Der RomHandler-Species-Pool ist erweitert (`speciesList.size=799`).
- Die interne Identitaet reicht bis `823`.
- Gen4-Gen6-Species werden im RomHandler korrekt klassifiziert.

Der fehlende Gen4+-Wild-Output ist ein nachgelagertes Settings-/Restriction-Problem:

- Die CLI/Settings-Verarbeitung behandelt einen Gen3-ROM-Hack weiter wie ein normales Gen3-Spiel.
- `currentRestrictions.limitToGen(3)` entfernt Gen4+ aus dem finalen RestrictedSpeciesService-Pool.
- `limitPokemon=false` verhindert diese Filterung nicht, weil `setupSpeciesRestrictions()` die Restrictions immer setzt.

## Ist ein weiterer UPR-FVX-Fix noetig?

Ja, aber als separater kleiner Fixbranch.

Empfohlener Scope:

- Fuer erweiterte CFRU/DPE-BPRE-Hacks mit `PokemonCount > Gen3Constants.unhackedMaxPokedex` darf `Settings.tweakForRom()` die Species-Restrictions nicht blind auf Gen3 kappen.
- Alternativ muss `GameRandomizer.setupSpeciesRestrictions()` bei `limitPokemon=false` den unrestricted Pool setzen, also `setRestrictions(null)` statt `settings.getCurrentRestrictions()`.
- Der Fix darf keine Nullslot- oder Day/Night-Wild-Tabellen-Themen vermischen.

## Naechster minimaler Schritt

Neuer UPR-FVX-Fixbranch:

```text
compat/upr-fvx-cfru-dpe-gen-restrictions
```

Ziel: Nur die Settings-/Restriction-Begrenzung fuer erweiterte Gen3-Hacks korrigieren und danach denselben Gen4+-Wild-Pool-Diagnoselauf wiederholen.
