# 074 - P1 Wild Filter Carrier Code Diagnosis

Datum: 2026-05-14

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-code-diagnosis`

## Ziel

Dieses Protokoll dokumentiert eine konkrete read-only Code-/Protokollanalyse fuer die 070-Wild-Blocker:

- `FVX-WILD-011` Wild Similar Strength
- `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary
- gemeinsamer Carrier: `FVX-WILD-001` Standard/Fallback-Wild

Es wurden keine Codeaenderungen vorgenommen, keine Randomizer-Laeufe ausgefuehrt und keine ROM-, Log-, Output-ROM-, Build-, Tool- oder privaten Artefakte gelesen oder dokumentiert.

## Ausgangsbefunde

Aus 070:

| Slice | Aktive Settings | Befund |
|---|---|---|
| `FVX-WILD-011` Wild Similar Strength | `randomizeWildPokemon=true`, `wildPokemonZoneMod=GAME`, `similarStrengthEncounters=true` | `saveSuccessful=false`, kein Output/Reload, `IllegalStateException` |
| `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary | `randomizeWildPokemon=true`, `wildPokemonZoneMod=GAME`, `wildPokemonTypeMod=KEEP_PRIMARY` | `saveSuccessful=false`, kein Output/Reload, `IllegalStateException`, `filterViolations=0` nur bis Abbruch |

Beide Slices laufen nicht nur ueber denselben Gen3-Wild-Carrier, sondern auch ueber denselben `GAME`-1:1-Mapping-Pfad im Wild-Randomizer.

## Relevante Codepfade

### Entry und Settings

- `random/src/main/java/com/uprfvx/random/GameRandomizer.java`
  - `setupSpeciesRestrictions()` ruft `romHandler.getRestrictedSpeciesService().setRestrictions(...)` vor der Randomization auf.
  - `maybeRandomizeWildPokemon()` ruft `wildEncounterRandomizer.randomizeEncounters()`.
- `random/src/main/java/com/uprfvx/random/Settings.java`
  - `WildPokemonZoneMod` enthaelt `NONE`, `ENCOUNTER_SET`, `MAP`, `NAMED_LOCATION`, `GAME`.
  - Default und 070-Slices nutzen `wildPokemonZoneMod=GAME`.
  - `WildPokemonTypeMod` enthaelt `NONE`, `RANDOM_THEMES`, `KEEP_PRIMARY`.

### Wild-Randomizer

- `random/src/main/java/com/uprfvx/random/randomizers/WildEncounterRandomizer.java`
  - `randomizeEncounters()` liest Encounter-Areas ueber `romHandler.getEncounters(useTimeOfDay)`.
  - `prepEncounterAreas()` kopiert die Area-Liste nur flach und entfernt nur `EncounterType.UNUSED` oder LocationTag `UNUSED`.
  - `game1to1Encounters()` setzt `useMapping=true` und behandelt alle Areas als eine Zone, wenn nicht nach Encounter-Type gesplittet wird.
  - `randomizeZones()` ruft bei `useMapping=true` immer `setupAreaInfoMap(zone)`.
  - `setupAreaInfoMap()` baut `areaInformationMap` aus `area.getSpeciesInArea()`.
  - `randomizeArea()` iteriert danach ueber die echten `Encounter`-Slots und ruft `setupAllowedForReplacement(current, area, zoneType, enc.getLevel())`.
  - `setupAllowedForReplacementUsingInfoMap()` wirft `IllegalStateException("Info was null for encounter's species!")`, wenn `areaInformationMap.get(current)` kein Info-Objekt liefert.

### Encounter-Modelle

- `romio/src/main/java/com/uprfvx/romio/gamedata/EncounterArea.java`
  - `getSpeciesInArea()` baut einen `SpeciesSet` aus allen `Encounter.getSpecies()`-Werten.
- `romio/src/main/java/com/uprfvx/romio/gamedata/SpeciesSet.java`
  - `add(Species)` ignoriert `null` bewusst und fuegt Null-Species nicht in den Set ein.
  - `getRandomSimilarStrengthSpecies(...)` ist der BST-Auswahlpfad fuer Similar Strength.
  - `sortByType(..., typeService.getTypes())` baut Type-Pools fuer die Type-Filter.
- `romio/src/main/java/com/uprfvx/romio/gamedata/Species.java`
  - `getBSTForPowerLevels()` ist die BST-Basis fuer Similar Strength.
  - `getPrimaryType(true)` / `getSecondaryType(true)` sind die Type-Datenbasis fuer `KEEP_PRIMARY`.

### Gen3 Wild Read/Write

- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
  - `getEncounters()` liest Standard/Fallback-Wild-Areas und ruft `readEncounterArea(...)`.
  - `readEncounterArea(...)` liest jeden Slot als raw internal Species ID und setzt `enc.setSpecies(pokesInternal[rawSpecies])`.
  - Wenn `pokesInternal[rawSpecies]` nicht aufloesbar ist, bleibt `enc.getSpecies()` `null`; der Code protokolliert dann nur diagnostisch einen `<unknown>`-Hinweis.
  - `setEncounters()` schreibt spaeter alle Areas wieder via `writeEncounterArea(...)`.
  - `writeEncounterArea(...)` schreibt `getWildEncounterInternalSpeciesId(enc.getSpecies())`; fuer erweiterte BPRE-Hacks wird die interne `SpeciesSet`-Identitaet verwendet.
  - `getBannedForWildEncounters()` bannt fuer CFRU/DPE `SPECIES_NONE` und `SPECIES_EGG`, aber `SPECIES_NONE` kann nicht als normale Species gebannt werden, wenn `pokesInternal[0]` `null` ist.

### Restricted Species

- `romio/src/main/java/com/uprfvx/romio/services/RestrictedSpeciesService.java`
  - Wird ueber `GameRandomizer.setupSpeciesRestrictions()` initialisiert.
  - Der `Restrictions not set.`-Pfad ist fuer 070 unwahrscheinlich, weil andere Slices denselben GameRandomizer-Setup-Pfad erfolgreich nutzen und der Wild-Code erst nach dem Setup laeuft.

## Wahrscheinlich konkrete Ursache

Die wahrscheinlich konkrete Ursache ist kein Gen3-Schreibpfad-Fehler und kein eigenstaendiger BST- oder Type-Filterfehler, sondern ein Mapping-Scope-Fehler im Wild-Randomizer:

1. `GAME`-Wild-Randomization setzt `useMapping=true`.
2. `setupAreaInfoMap()` baut seine Infos aus `area.getSpeciesInArea()`.
3. `EncounterArea.getSpeciesInArea()` benutzt `SpeciesSet.add(...)`.
4. `SpeciesSet.add(...)` ignoriert `null`.
5. Ein Wild-Encounter-Slot, dessen Species im Gen3-Read-Pfad nicht aufloesbar ist, bleibt im `Encounter` selbst als `null`, bekommt aber keinen Eintrag in `areaInformationMap`.
6. `randomizeArea()` iteriert anschliessend ueber diesen Slot und ruft den InfoMap-Pfad auf.
7. `setupAllowedForReplacementUsingInfoMap()` findet fuer `current == null` kein Info-Objekt und wirft `IllegalStateException("Info was null for encounter's species!")`.

Diese Stelle passt zu beiden 070-Befunden:

- Beide Slices verwenden `wildPokemonZoneMod=GAME`, also den Mapping-Pfad.
- Beide haben dieselbe Exception-Klasse.
- Der Abbruch passiert vor Output/Reload.
- `FVX-WILD-004` meldet `filterViolations=0` nur bis Abbruch, was dazu passt, dass der Type-Filter-Endzustand nie erreicht wird.

## Trennung der Problemklassen

### Carrier-Problem

Der `FVX-WILD-001` Gen3-Carrier kann Standard/Fallback-Wild-Areas lesen und schreiben, wenn alle im Randomizer beruehrten Slots auf gueltige `Species` zeigen. Der aktuelle Befund zeigt aber eine Carrier-Grenze fuer nicht aufloesbare oder Nullslot-Entries:

- `Gen3RomHandler.readEncounterArea()` kann `Encounter`-Slots mit `species=null` erzeugen.
- `WildEncounterRandomizer` behandelt diese Slots im Mapping-Modus nicht defensiv.
- `Gen3RomHandler.writeEncounterArea()` haette ohne vorherige Ersetzung ebenfalls kein Preserve-Modell fuer `species=null`, weil `Encounter` die raw Species ID nicht speichert.

Damit ist der Carrier nicht allgemein defekt, aber fuer Nullslot-/unaufloesbare Wild-Slots nicht voll defensiv.

### BST-/Similar-Strength-Filterproblem

`FVX-WILD-011` erreicht den BST-Auswahlpfad wahrscheinlich nicht fuer den blockierenden Slot. Die Similar-Strength-Auswahl liegt in `SpeciesSet.getRandomSimilarStrengthSpecies(...)`, wird aber erst nach erfolgreichem `setupAllowedForReplacementUsingInfoMap()` aufgerufen.

Latentes Folgerisiko: Placeholder-/BST-zero-Species koennen spaeter eigene Probleme erzeugen, insbesondere wenn `getBSTForPowerLevels()` `0` liefert. Der dokumentierte 070-`IllegalStateException`-Befund zeigt aber primaer auf den InfoMap-/Nullslot-Pfad vor der BST-Auswahl.

### Type-Filterproblem

`FVX-WILD-004` erreicht den fachlichen `KEEP_PRIMARY`-Endzustand wahrscheinlich ebenfalls nicht fuer den blockierenden Slot. `setupAllowedForReplacementUsingInfoMap()` muss zuerst ein Info-Objekt finden; erst danach wird `info.getTheme(keepPrimaryType)` genutzt.

Latentes Folgerisiko: Species mit `null` oder unsupported Primary Type koennen in `remainingByType`/`allowedByType` spaeter eigene NPE- oder Leerpool-Probleme erzeugen. Die beobachtete `IllegalStateException` spricht aber staerker fuer den fehlenden InfoMap-Eintrag.

### Placeholder-/Nullslot-/Special-Species-Problem

Dies ist die primaere Spur. 055 klassifiziert Null-Species und BST-zero-/Special-Species als echte Blocker, sobald ein Randomizer-Pfad sie dereferenziert oder schreiben will. Genau das passiert hier wahrscheinlich:

- Null-/unaufloesbare Slots werden nicht in `SpeciesSet` aufgenommen.
- Der Mapping-Pfad erwartet aber fuer jede Encounter-Species einen InfoMap-Eintrag.
- `SPECIES_EGG` wird inzwischen fuer Wild gebannt, aber `SPECIES_NONE`/raw `0` bleibt kein normales `Species`-Objekt und kann deshalb nicht rein ueber den bestehenden `banned`-Pool abgefangen werden.

## Treffen beide Slices denselben Fehlerpfad?

Ja, mit hoher Wahrscheinlichkeit.

Der gemeinsame Pfad ist:

```text
GameRandomizer.maybeRandomizeWildPokemon()
-> WildEncounterRandomizer.randomizeEncounters()
-> InnerRandomizer.game1to1Encounters()
-> InnerRandomizer.randomizeZones()
-> InnerRandomizer.setupAreaInfoMap()
-> InnerRandomizer.randomizeArea()
-> InnerRandomizer.setupAllowedForReplacementUsingInfoMap()
-> IllegalStateException: Info was null for encounter's species!
```

`FVX-WILD-011` und `FVX-WILD-004` unterscheiden sich erst in den nachgelagerten Auswahlfiltern. Der dokumentierte Exception-Typ und der gemeinsame `GAME`-Mapping-Scope sprechen dafuer, dass beide vorher am gleichen Nullslot-/InfoMap-Problem scheitern.

## Voraussichtliche Fix-Dateien

Ein spaeterer Fixbranch sollte klein bleiben und voraussichtlich diese Dateien beruehren:

- `random/src/main/java/com/uprfvx/random/randomizers/WildEncounterRandomizer.java`
  - Defensive Behandlung von `Encounter`-Slots mit `species == null` oder anderweitig nicht randomisierbaren Placeholder-Species im Mapping-Pfad.
  - Klare Entscheidung, ob solche Slots uebersprungen, aus prepped Areas entfernt oder mit einem gueltigen Replacement ersetzt werden.
- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
  - Nur falls Preserve/Skip fuer raw Nullslot-Wild-Entries noetig ist. Aktuell speichert `Encounter` keine raw Species ID, daher kann der Writer einen `null`-Slot nicht unveraendert rekonstruieren.
- Tests oder Diagnose-Harness im UPR-FVX-Repo
  - Minimaler Test fuer `GAME`-Wild-Mapping mit einem Encounter-Slot ohne aufloesbare Species.
  - Separate Assertions fuer Similar Strength und Keep Primary, damit BST- und Type-Filter nicht versehentlich vermischt werden.

Nicht als erste Fix-Ziele geeignet:

- `SpeciesSet.add(...)`: Das Ignorieren von `null` ist ein globales Modellverhalten und ein breiter Eingriff waere riskant.
- TypeChart / TypeEffectiveness, MoveData, Palette, Items, Text/Menu oder Graphics.

## Ist ein lokaler Diagnose-Lauf noch noetig?

Fuer die Fixplanung ist ein weiterer lokaler Randomizer-Lauf nicht zwingend noetig: Der Codepfad erklaert den gemeinsamen `IllegalStateException`-Befund konsistent und eng genug.

Ein separater lokaler Diagnose-Lauf waere nur dann sinnvoll, wenn vor dem Fix noch die konkrete Area-/Slot-Klasse oder die genaue Exception-Message sanitisiert bestaetigt werden soll. Dieser Lauf muesste separat freigegeben werden und duerfte nur aggregierte Null-/Placeholder-Zaehler, `exceptionClass`/`stacktraceClass` und keine Pfade, ROM-Namen, Hashes oder Loginhalte dokumentieren.

## Ist ein Fixbranch sinnvoll?

Ja. Ein eng gegateter Fixbranch ist sinnvoll, aber nur fuer den Wild-Filter-Carrier-Scope:

- Ziel: `GAME`-Wild-Mapping darf nicht an Null-/unaufloesbaren Encounter-Slots abbrechen.
- Nachweis: je ein sanitisiertes Ergebnis fuer `FVX-WILD-011` und `FVX-WILD-004`.
- Erfolgskriterien: Save/Log/Output/Reload true, `writeReloadWildPokemonMismatches=0`, `Bad Egg`/`<unknown>` nach 055 klassifiziert, `stacktrace=none`.

Der Fixbranch darf keine offenen Writer einschleusen und darf nicht mit TypeChart, MoveData, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level Modifier, Text/Menu oder Graphics vermischt werden.

## Ergebnis

074 grenzt die Ursache auf den `GAME`-Wild-Mapping-Pfad ein. Die wahrscheinlich konkrete Stelle ist `WildEncounterRandomizer.InnerRandomizer.setupAllowedForReplacementUsingInfoMap()`, das fuer einen Encounter-Slot ohne InfoMap-Eintrag `IllegalStateException` wirft. Der fehlende InfoMap-Eintrag entsteht wahrscheinlich, weil `EncounterArea.getSpeciesInArea()` einen `SpeciesSet` nutzt und `SpeciesSet.add(...)` `null`-Species ignoriert, waehrend `randomizeArea()` den urspruenglichen Nullslot weiterhin iteriert.
