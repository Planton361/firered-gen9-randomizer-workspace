# 077 - P1 Trainer Type Diversity Code Diagnosis

Datum: 2026-05-14

Branch: `analysis/upr-fvx-cfru-dpe-p1-trainer-type-diversity-code-diagnosis`

## Ziel

Dieses read-only Protokoll analysiert konkret den 070/076-Blocker:

- `FVX-FOE-009` Trainer Type Diversity / Type Themes
- Carrier: `FVX-FOE-001` Trainer Pokemon

Es fuehrt keine Randomizer-Laeufe aus und aendert keinen Code. Der Scope bleibt auf Trainer Pokemon, Trainer Type Diversity und Trainer Type Themes begrenzt. Wild, Evolution, TypeChart, MoveData, Palette, Items, Text/Menu, Graphics und Level-Modifier bleiben ausgeschlossen.

## Ausgangsbefund

Aus Diagnose 070:

- Aktive Settings: `trainersMod=RANDOM`, `diverseTypesForBossTrainers=true`, `diverseTypesForImportantTrainers=true`, `diverseTypesForRegularTrainers=true`
- `saveSuccessful=false`
- kein Output/Reload
- `writeReloadTrainerPokemonMismatches=-1` wegen fehlendem Output
- `filterViolations=112` nur bis Abbruch
- `Bad Egg=false`
- `<unknown>=false`
- `stacktrace=none`
- Exception-Klasse: `NullPointerException`

Trainer Similar Strength unter `FVX-FOE-001` war im selben 070-Block stabil: Save/Log/Output/Reload true und `writeReloadTrainerPokemonMismatches=0`.

## Relevante Codepfade

Read-only Code-Referenzen:

| Datei | Relevante Stellen | Bedeutung |
|---|---|---|
| `random/src/main/java/com/uprfvx/random/GameRandomizer.java` | `maybeRandomizeTrainerPokemon()` | startet den Trainer-Species-Carrier ohne Trainer-Movesets/Items/Names |
| `random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java` | `randomizeTrainerPokes()` Zeilen 44-318 | gemeinsamer Trainer-Species-Carrier, Similar Strength, Type Themes und Force Diverse Types |
| `random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java` | `updateUsedTypes(...)` Zeilen 320-327 | wahrscheinlich konkrete NPE-Stelle bei `EnumSet.add(null)` |
| `random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java` | `pickTrainerPokeReplacement(...)` Zeilen 482-594 | Replacement-Pool, Similar Strength und `bannedTypes`-Filter |
| `random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java` | `isNotUsableTrainerSpecies(...)` Zeilen 666-669 | filtert `BST == 0` und all-zero Abilities, aber keinen Null-Primary-Type |
| `romio/src/main/java/com/uprfvx/romio/gamedata/SpeciesSet.java` | `sortByType(...)`, `getRandomSimilarStrengthSpecies(...)` | Type- und BST-basierte SpeciesSet-Helfer |
| `romio/src/main/java/com/uprfvx/romio/gamedata/Species.java` | `getPrimaryType(...)`, `hasType(...)`, `hasSecondaryType(...)` | `primaryType` kann `null` sein; `hasType(null, ...)` ist defensiv |
| `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | Trainer read/write um `getTrainerPokemonInternalSpeciesId(...)` | Write-/Reload-Pfad, aber nicht primaere 070-Ursache |

### Aufrufpfad

- `GameRandomizer.maybeRandomizeTrainerPokemon()`
  - ruft `trainerPokeRandomizer.randomizeTrainerPokes()` auf, wenn `settings.getTrainersMod() != UNCHANGED` oder Additional Pokemon aktiv ist.
  - Level Modifier, Additional Pokemon und Battle Style sind separate Vorpfade und waren fuer 070 ausgeschlossen.

### Trainer-Species-Carrier

- `TrainerPokemonRandomizer.randomizeTrainerPokes()`
  - baut `cachedAll` aus `rSpecService.getSpecies(noLegendaries, includeFormes, false)`.
  - entfernt fuer erweiterte BPRE-Hacks `isNotUsableTrainerSpecies(...)`.
  - `isNotUsableTrainerSpecies(...)` filtert derzeit nur `BST == 0` oder all-zero Abilities.
  - der Filter prueft keinen `primaryType == null` und keine unsupported-Type-Species.

### Similar-Strength-Pfad

- `usePowerLevels = settings.isTrainersUsePokemonOfSimilarStrength()`.
- Die Similar-Strength-Auswahl passiert erst am Ende von `pickTrainerPokeReplacement(...)`:
  - `pickFrom.getRandomSimilarStrengthSpecies(current, random)`.
- Dieser Pfad nutzt BST-Naehe, aber nicht automatisch `forceTypeDiverse` und nicht `usedTypes`.
- Dadurch kann Trainer Similar Strength im `FVX-FOE-001` Carrier stabil bleiben, solange kein anderer Pfad Null-Type-Species dereferenziert.

### Type-Diversity-/Type-Themes-Pfad

- `bossDiversity`, `importantDiversity` und `regularDiversity` werden in `randomizeTrainerPokes()` gelesen.
- Pro Trainer setzt `forceTypeDiverse` die Diversity-Regel anhand Boss/Important/Regular.
- `usedTypes` ist ein `EnumSet<Type>`.
- Nach jedem gesetzten Replacement ruft der Randomizer `updateUsedTypes(forceTypeDiverse, typeForTrainer, usedTypes, newSp)` auf.
- `updateUsedTypes(...)` fuegt bei Force-Diverse-Types ohne festen Trainer-Theme-Typ direkt `sp.getPrimaryType(false)` und ggf. `sp.getSecondaryType(false)` in das `EnumSet` ein.
- `EnumSet` kann keine `null`-Elemente aufnehmen. Wenn `sp.getPrimaryType(false) == null`, ist `usedTypes.add(...)` die wahrscheinlich konkrete `NullPointerException`-Stelle.

### Poolfilter gegen verwendete Typen

- `pickTrainerPokeReplacement(...)` nimmt `bannedTypes` entgegen.
- Wenn `bannedTypes` nicht leer ist, filtert es Kandidaten mit:
  - `!bannedTypes.contains(sp.getPrimaryType(false))`
  - und, falls vorhanden, `!bannedTypes.contains(sp.getSecondaryType(false))`
- Dieser Filter entfernt bereits verwendete Typen, entfernt aber nicht explizit Species mit `primaryType == null`.
- Eine Null-Type-Species kann also im Type-Diversity-Kandidatenpool bleiben und spaeter in `updateUsedTypes(...)` scheitern.

### Species-/Type-Helfer

- `Species.getPrimaryType(false)` kann `null` zurueckgeben.
- `Species.hasType(type, ...)` behandelt `type == null` defensiv als `false`.
- `Species.hasSecondaryType(...)` ist nur ein Nullcheck auf `getSecondaryType(...)`.
- `SpeciesSet.sortByType(...)` und `filterByType(...)` sind fuer Type-Themes relevant, aber 070 aktiviert `trainersMod=RANDOM` mit Diversity-Checkboxen; damit ist der wahrscheinlichere Pfad `forceTypeDiverse` plus `updateUsedTypes(...)`, nicht Group-Type-Theme-Zuweisung.

### Gen3 Trainer Read/Write

- `Gen3RomHandler` liest Trainer-Pokemon ueber `pokesInternal[...]` in `TrainerPokemon`.
- Der Trainer-Write nutzt fuer erweiterte BPRE-Hacks `getTrainerPokemonInternalSpeciesId(tp.getSpecies())` und schreibt interne `SpeciesSet`-Identitaet.
- Der 070-Befund bricht vor Output/Reload ab; der Write-Pfad ist deshalb nicht die primaere Ursache, bleibt aber spaeterer Reload-Nachweis.

## Wahrscheinlich konkrete Ursache

Wahrscheinlich entsteht die `NullPointerException` in:

```text
TrainerPokemonRandomizer.updateUsedTypes(...)
```

Der konkrete Mechanismus:

1. `FVX-FOE-009` aktiviert Force-Diverse-Types fuer Boss-, Important- und Regular-Trainer.
2. `randomizeTrainerPokes()` waehlt ein Replacement aus `cachedAll`.
3. `cachedAll` ist im erweiterten BPRE-Hack zwar gegen `BST == 0` und all-zero Abilities gefiltert, aber nicht gegen `primaryType == null`.
4. Der Diversity-Pfad speichert die bereits verwendeten Typen in einem `EnumSet<Type>`.
5. Wenn ein Replacement mit `primaryType == null` gewaehlt wird, ruft `updateUsedTypes(...)` `usedTypes.add(null)` auf.
6. `EnumSet.add(null)` wirft `NullPointerException`.

Damit ist `filterViolations=112` aus 070 plausibel ein Vor-Abbruch-Symptom: Die Diversity-Filterung konnte bis zu einem Teilzustand beobachtet werden, aber der Endzustand wurde wegen Save-Abbruch nie erreicht.

## Abgrenzung zu Similar Strength

Trainer Similar Strength unter `FVX-FOE-001` war stabil, weil:

- der Slice `trainersUsePokemonOfSimilarStrength=true` nutzt.
- die Auswahl ueber `getRandomSimilarStrengthSpecies(current, random)` laeuft.
- `forceTypeDiverse` in diesem Slice nicht aktiv ist.
- `updateUsedTypes(...)` bei `forceTypeDiverse == false` keine Typen in `EnumSet` schreibt.

Damit kann derselbe Trainer-Species-Carrier stabil sein, waehrend der Diversity-Pfad an Null-/unsupported-Type-Species scheitert.

## Placeholder-/Null-Type-/BST-zero-Scope

Vorhandene Scope-Regeln decken einen Teil ab:

- 024/Trainer-Scope und aktueller Code filtern im erweiterten BPRE-Hack `BST == 0` und all-zero Ability Species aus dem Trainer-Replacement-Pool.
- 055 klassifiziert `BST == 0`, Placeholder-/Null-Species und unsupported-Type-Species als potentielle echte Blocker, wenn ein Randomizer-Pfad sie dereferenziert.
- Andere Pfade besitzen bereits lokale Null-Type-Schutzregeln, zum Beispiel TM/HM-/Tutor-Compatibility mit `pkmn == null || pkmn.getPrimaryType(false) == null`.

Fuer `FVX-FOE-009` fehlt diese Grenze im Type-Diversity-Pfad:

- `isNotUsableTrainerSpecies(...)` prueft keinen Null-Primary-Type.
- `pickTrainerPokeReplacement(...)` entfernt Null-Primary-Type-Kandidaten nicht, wenn `bannedTypes` aktiv ist.
- `updateUsedTypes(...)` prueft weder `sp == null` noch `sp.getPrimaryType(false) == null`, bevor es in `EnumSet` schreibt.

## Spaeterer Fix-Scope

Ein spaeterer Fix sollte voraussichtlich eng in UPR-FVX liegen:

- `random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java`

Moegliche Fixgrenzen:

- Null-/unsupported-Type-Species defensiv aus dem Trainer-Type-Diversity-Kandidatenpfad ausschliessen.
- `updateUsedTypes(...)` gegen `sp == null` und `primaryType == null` absichern.
- Bestehende Trainer-Scope-Regeln fuer `BST == 0` und all-zero Abilities nicht aufweichen.
- Similar Strength im Trainer-Carrier nicht regressieren.

Nicht Teil des Fixes:

- Trainer Level Modifier.
- Additional Pokemon.
- Better Movesets.
- Battle Style.
- Trainer Names / Class Names.
- Wild.
- Evolution.
- TypeChart / TypeEffectiveness.
- MoveData Write.
- Items.
- Palette.
- Text/Menu/Graphics.

## Diagnose-Lauf noch noetig?

Ein lokaler Diagnose-Lauf ist fuer die Fixplanung nicht zwingend noetig. Die Codepfade erklaeren den Unterschied zwischen stabilem Similar Strength und blockierendem Force-Diverse-Types-Pfad konkret genug.

Optional waere ein separat freigegebener, sanitisiert dokumentierter lokaler Diagnose-Lauf sinnvoll, wenn vor dem Fix die genaue `exceptionClass`/`stacktraceClass` oder ein reiner Null-Primary-Type-Zaehler bestaetigt werden soll. Dieser Lauf duerfte keine ROM-/Log-/Output-Pfade, ROM-Namen, Hashes oder Loginhalte dokumentieren.

## Fixbranch sinnvoll?

Ja. Ein eng gegateter Fixbranch ist sinnvoll, wenn er auf `TrainerPokemonRandomizer` und den Trainer-Type-Diversity-/Type-Scope begrenzt bleibt.

Empfohlene Folge:

1. UPR-FVX-Fix fuer defensiven Trainer-Type-Diversity-Null-Type-Scope.
2. Nur passende lokale Smokes:
   - `FVX-FOE-009` Trainer Type Diversity / Type Themes.
   - optional Trainer Similar Strength als Regression gegen den stabilen Vergleichspfad.
3. Sanitisiertes Workspace-Protokoll mit Save/Log/Output/Reload, `writeReloadTrainerPokemonMismatches`, `filterViolations`, `Bad Egg`, `<unknown>` und `exceptionClass/stacktraceClass`.

## Ergebnis

Die wahrscheinlich konkrete Ursache des 070/076-Blockers ist ein fehlender Null-/unsupported-Type-Schutz im `FVX-FOE-009` Type-Diversity-Pfad. Der Trainer-Species-Carrier selbst und der Similar-Strength-Pfad sind dadurch nicht die primaere Ursache. Ein spaeterer Fix sollte klein bleiben und den Type-Diversity-Scope in `TrainerPokemonRandomizer` defensiv gegen Null-Primary-Type-Species absichern.
