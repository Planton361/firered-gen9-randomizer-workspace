# 079 - P1 Evolution Same Typing Code Diagnosis

Datum: 2026-05-14

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-evolution-same-typing-blocker-diagnostics`

## Scope

Dieses Protokoll ist eine read-only Code-/Protokollanalyse fuer den 070-Blocker `FVX-TRAIT-019` Evolutions Same Typing.

Untersucht wurden nur Evolution-Randomizer-, Evolution-Pool- und Same-Typing-Codepfade. Es gab keine Codeaenderung, keinen Fix und keine Randomizer-Laeufe.

Ausgeschlossen bleiben Wild, Trainer, TypeChart / TypeEffectiveness, MoveData Write, Palette, Items, Text/Menu, Graphics und Evolution-Methoden-Writer.

## Ausgangsbefund aus 070

`FVX-TRAIT-019` Evolutions Same Typing:

- Carrier: `FVX-TRAIT-016` Evolution-Species-Writer.
- Aktive Settings: Evolution Randomization mit `evosSameTyping=true`.
- `saveSuccessful=false`.
- Kein Output/Reload.
- `NullPointerException`.
- `filterViolations=0` nur bis Abbruch, nicht als vollstaendige Erfolgsaussage.
- `Bad Egg=false`, `<unknown>=false`, `stacktrace=none` im sanitisierten Ergebnis.

Vergleich: `FVX-TRAIT-018` Evolutions Similar Strength erreicht Save/Log/Output/Reload, meldet aber `writeReloadEvolutionMismatches=24` und `Bad Egg=true`. Das ist ein separater Reload-/Placeholder-Scope und nicht dieselbe Abbruchursache wie Same Typing.

## Gefundene Codepfade

### GameRandomizer Entry

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`

- `maybeRandomizeEvolutions()` ruft bei aktivierter Evolution-Randomization `evoRandomizer.randomizeEvolutions()` auf.
- Der 070-Befund blockiert vor Save/Output/Reload und liegt damit plausibel im Randomizer-Pfad vor dem Gen3-Evolution-Write.

### EvolutionRandomizer Carrier und Pool

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`

- Der Randomizer liest `similarStrength = settings.isEvosSimilarStrength()` und `sameType = settings.isEvosSameTyping()`.
- Der Species-Pool kommt aus `RestrictedSpeciesService.getSpecies(false, romHandler.altFormesCanHaveDifferentEvolutions(), false)`.
- Danach werden einzelne Forme-Bans angewendet, aber kein allgemeiner Null-Primary-Type-, BST-zero-, Placeholder- oder unsupported-Type-Filter.
- `randomizeEvolutionsInner()` iteriert ueber den Pool, entfernt vorhandene Evolutionen und sucht fuer jede Original-Evolution passende Ziele via `findPossibleReplacements(from, evo)`.

### Same-Typing-Filter

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`

Der Same-Typing-Pfad fuegt in `findPossibleReplacements(...)` einen Type-Filter hinzu:

```java
if (sameType) {
    if (from.getNumber() == SpeciesIDs.eevee && !evolveEveryLevel) {
        filters.add(to -> to.hasSharedType(evo.getTo()));
    } else {
        filters.add(to -> to.hasSharedType(from));
    }
}
```

Damit wird der Kandidat `to` direkt ueber `Species.hasSharedType(...)` bewertet. Dieser Pfad wird von Similar Strength nicht genutzt.

### Species.hasSharedType

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Species.java`

`hasSharedType(Species other)` dereferenziert `getPrimaryType(false)` des Empfaengers:

```java
return getPrimaryType(false).equals(other.getPrimaryType(false)) || ...
```

Wenn eine Kandidaten-Species `to` einen `primaryType == null` hat, wirft `to.hasSharedType(...)` eine `NullPointerException`.

Ein `null`-Typ auf der Vergleichs-Species `from` oder `evo.getTo()` ist weniger kritisch, solange `to.getPrimaryType(false)` nicht null ist, weil `nonNullType.equals(null)` safe ist. Die konkrete Null-Gefahr sitzt im Same-Typing-Filter daher primaer auf dem Kandidaten `to`.

### SpeciesSet Filterverhalten

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/SpeciesSet.java`

- `SpeciesSet.add(...)` ignoriert Java-`null`, der Pool enthaelt also keine null-Objekte.
- `SpeciesSet.filter(Predicate<Species>)` reicht jede Species an das Predicate weiter und faengt keine `NullPointerException`.
- Eine NPE aus `to.hasSharedType(...)` propagiert deshalb direkt aus der Poolfilterung.

### Type-Read-Scope

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

- Base-Stats-Typen werden ueber `byteToBaseStatsType(...)` gelesen.
- Fairy raw `0x17` wird fuer CFRU/DPE als `Type.FAIRY` erkannt.
- Nicht unterstuetzte Typwerte wie Stellar raw `0x18` bleiben ueber die Gen3-Type-Tabelle `null`.

Damit kann eine valide geladene Species im erweiterten CFRU/DPE-BPRE-Hack ein Species-Objekt mit `primaryType == null` sein. Das ist kein Java-null-Species-Slot, sondern ein unsupported-/unaufloesbarer Type-Scope.

### Evolution Read/Write

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

- `loadEvolutions()` baut Evolutionen aus internen Species-Zielen.
- `writeEvolutions()` schreibt Evolution-Ziele bei erweiterten BPRE-Hacks ueber interne SpeciesSet-Identitaet.

Diese Pfade sind fuer den 070-Same-Typing-Abbruch nicht die wahrscheinlich erste Ursache, weil der Slice vor Output/Reload abbricht. Sie bleiben aber die spaeteren Reload-Kriterien fuer einen Fix-Smoke.

## Ursache oder eingegrenzte Hypothese

Wahrscheinlich konkrete Ursache:

`EvolutionRandomizer.findPossibleReplacements(...)` wendet im Same-Typing-Slice `to.hasSharedType(...)` auf Kandidaten aus dem Evolution-Replacement-Pool an. Der Pool kann CFRU/DPE-Species mit `primaryType == null` enthalten. `Species.hasSharedType(...)` dereferenziert den Primary Type des Empfaengers ohne Null-Guard und wirft dann eine `NullPointerException`.

Das erklaert den 070-Befund:

- Der Abbruch passiert vor Save.
- Es gibt keinen Output und keinen Reload.
- `filterViolations=0` ist nur ein Vor-Abbruch-Zwischenstand.
- `Bad Egg=false` und `<unknown>=false` im Log beweisen hier keine Pool-Sauberkeit, weil der Slice vor einem vollstaendigen Schreib-/Reload-Zyklus endet.

## Abgrenzung

Carrier:

- `FVX-TRAIT-016` Evolution-Species-Writer ist grundsaetzlich belegt und wurde in frueheren Evolution-Scope-/Write-Diagnosen stabilisiert.
- Der 070-Same-Typing-Blocker liegt nicht im allgemeinen Evolution-Species-Carrier allein, sondern im zusaetzlichen Same-Typing-Filter vor der Zielauswahl.

Same Typing:

- Nutzt Species-Type-Felder aus Base Stats.
- Beweist keinen TypeChart- oder TypeEffectiveness-Support.
- Muss unsupported-/null-Type-Species defensiv aus dem Vergleichs-/Kandidatenpfad halten.

Similar Strength:

- Nutzt BST-basierte Auswahl und ruft den Same-Typing-`hasSharedType(...)`-Pfad nicht auf.
- Der 070-Similar-Strength-Befund mit `writeReloadEvolutionMismatches=24` und `Bad Egg=true` ist ein separater Evolution-Replacement-/Placeholder-/Reload-Scope.
- Same-Typing-Null-Type-Fix sollte nicht automatisch `FVX-TRAIT-018` als supported hochstufen.

Placeholder-/Special-/BST-zero-Scope:

- `RestrictedSpeciesService` liefert fuer den Evolution-Pool keinen allgemeinen Null-Type- oder BST-zero-Filter.
- Existing Scope-Regeln fuer andere Randomizer-Pfade werden hier nicht automatisch angewendet.
- Ein spaeterer Fix muss eng entscheiden, ob nur Null-Primary-Type-Kandidaten im Same-Typing-Pfad ausgeschlossen werden oder ob zusaetzliche Evolution-spezifische Placeholder-/Special-Species-Grenzen noetig sind.

## Voraussichtliche Fix-Oberflaeche

Primaere Fix-Datei:

- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`

Empfohlene Richtung:

- Same-Typing-Kandidaten nur vergleichen, wenn die Kandidaten-Species einen nutzbaren Primary Type hat.
- Optional auch die Vergleichs-Species `from` beziehungsweise `evo.getTo()` defensiv pruefen, damit der Filter bei unsupported-Type-Ankern keinen invaliden Zustand erzwingt.
- Similar Strength und allgemeine Evolution-Species-Carrier-Logik nicht vermischen.

Hoeherriskante Alternative:

- `Species.hasSharedType(...)` global null-safe machen. Das haette breitere Auswirkungen auf andere Featurepfade und sollte nur gewaehlt werden, wenn die globale Semantik bewusst gewollt ist.

## Braucht es noch einen lokalen Diagnose-Lauf?

Fuer die Fixplanung ist kein weiterer lokaler Diagnose-Lauf zwingend noetig: Die Codepfade reichen aus, um den NPE-Pfad auf `to.hasSharedType(...)` mit null Primary Type einzugrenzen.

Ein spaeterer lokaler Lauf ist nach einem Fix trotzdem noetig, aber dann als eng gegateter Smoke:

- `FVX-TRAIT-019` Evolutions Same Typing.
- Optional nur als getrennte Regression: `FVX-TRAIT-018` Evolutions Similar Strength, ohne dessen Reload-/Bad-Egg-Problem in denselben Fix zu ziehen.

## Empfehlung

Ein Fixbranch ist sinnvoll, aber eng zu gaten:

- Fokus nur `EvolutionRandomizer` Same-Typing-/Null-Primary-Type-Scope.
- Kein Wild-, Trainer-, TypeChart-, MoveData-, Palette-, Item-, Text/Menu-, Graphics- oder Evolution-Methoden-Writer-Fix.
- Keine Support-Hochstufung fuer `FVX-TRAIT-018`, solange dessen `writeReloadEvolutionMismatches` und `Bad Egg` separat offen sind.

Spaetere Erfolgskriterien fuer `FVX-TRAIT-019`:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `writeReloadEvolutionMismatches=0`
- `filterViolations=0`, falls fuer den Slice sinnvoll erhoben
- `Bad Egg` und `<unknown>` nach 055 klassifiziert
- `exceptionClass=none`
- `stacktrace=none`

## Sicherheitsnotizen

- Keine Codeaenderung.
- Keine Aenderung an `02_external/**`.
- Keine Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, privaten Pfade, ROM-Namen, Hashes, Secrets, Tokens oder `.env`-Inhalte gelesen, kopiert, geaendert oder dokumentiert.
