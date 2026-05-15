# 166 - Evolution Same Typing Diagnostics

## Datum

2026-05-15

## Branch

```text
test/upr-fvx-cfru-dpe-evolution-same-typing-diagnostics
```

## Scope

Read-only Diagnose fuer `FVX-TRAIT-019` Evolution Same Typing im getesteten CFRU/DPE Gen9-BPRE-Scope.

Nicht ausgefuehrt:

- kein ROM-Smoke
- kein Randomizer-Lauf
- kein Build
- keine Codeaenderung
- keine Aenderung an `02_external/upr-fvx`

UPR-FVX blieb im Workspace auf:

```text
dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c
```

## Ergebnis

Klassifikation:

```text
diagnosis-ready
```

`FVX-TRAIT-019` ist fuer den bereits dokumentierten engen Evolution-Species-Carrier-Scope nicht mehr als aktiver Fixblocker einzuordnen. Der alte 070-Same-Typing-Blocker war ein Save-Abbruch durch den Same-Typing-Type-Filter. Diagnose 079 grenzte die Ursache auf `to.hasSharedType(...)` mit null/unsupported Primary-Type-Kandidaten ein; Diagnose 080 dokumentiert den engen UPR-FVX-Fix und bestaetigt den Same-Typing-Scope mit Save/Log/Output/Reload true und `writeReloadEvolutionMismatches=0`.

## Bereits supported

### Evolution Species-only

Diagnose 026 bestaetigt `FVX-TRAIT-016` Evolution-Species-Writer im getesteten CFRU/DPE Gen9-BPRE-Scope:

- Evolution-Replacement-Pool erreicht Gen1-Gen9.
- Gen7/8/9-Ziele werden gepickt.
- `loadEvolutions()` und `writeEvolutions()` nutzen im erweiterten BPRE-Hack interne `SpeciesSet`-Identitaet.
- Reload nutzt dieselbe Ziel-Species-Identitaet.
- `writeReloadMismatches=0`.
- Evolution-Logger faellt bei unbekannten ExtraInfo-Werten defensiv auf Marker wie `unknown item #1732` zurueck.

### Evolution Same Typing

Diagnose 080 bestaetigt `FVX-TRAIT-019` im engen `FVX-TRAIT-016` Evolution-Species-Carrier:

- Same Typing aktiv, Similar Strength inaktiv.
- Evolution-Methoden-Writer, MoveData, TypeChart, Palette, Items, Text/Menu und Graphics aus Scope.
- Same-Typing-Kandidaten mit `primaryType == null` laufen nicht mehr in `candidate.hasSharedType(reference)`.
- Ergebnis stabil mit:
  - `saveSuccessful=true`
  - `logSuccessful=true`
  - `outputRomExists=true`
  - Reload erfolgreich `true`
  - `writeReloadEvolutionMismatches=0`
  - `<unknown>=false`
  - `exceptionClass=none`
  - `stacktrace=none`
- `Bad Egg=true` bleibt nach Diagnose 055 als bestehender Evolution-Log-/Sonder-Species-Marker klassifiziert, weil der Evolution-Reload-Mismatch-Zaehler `0` bleibt.

## Alter Blockerstatus

Diagnose 070 dokumentierte fuer `FVX-TRAIT-019`:

```text
saveSuccessful=false
outputRomExists=false
reloadSuccessful=false
writeReloadEvolutionMismatches=-1
exceptionClass=NullPointerException
Bad Egg=false
<unknown>=false
```

Dieser alte Blocker ist durch Diagnose 079/080 ueberholt:

- 079 fand den plausiblen Abbruchpfad im Same-Typing-Filter.
- 080 implementierte den engen Guard nur in `EvolutionRandomizer`.
- 080 bestaetigte den Same-Typing-Slice mit Save/Log/Output/Reload true und `writeReloadEvolutionMismatches=0`.

## Read-only Codepfad

### EvolutionRandomizer

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`

- `randomizeEvolutions()` liest `settings.isEvosSameTyping()` und reicht den Wert an den inneren Randomizer weiter.
- `randomizeEvolutionsInner()` iteriert ueber den Evolution-Pool, ermittelt moegliche Ziele und ruft `findPossibleReplacements(from, evo)` auf.
- Bei `sameType=true` nutzt der aktuelle Code nicht mehr direkt `to.hasSharedType(...)`, sondern:

```text
hasUsableSharedType(to, evo.getTo())
hasUsableSharedType(to, from)
```

- `hasUsableSharedType(...)` prueft `candidate != null`, `reference != null` und `candidate.getPrimaryType(false) != null`, bevor `candidate.hasSharedType(reference)` ausgefuehrt wird.
- Damit ist der in 079 dokumentierte Kandidaten-Primary-Type-NPE-Pfad fuer Same Typing defensiv geschlossen.

### Species.hasSharedType

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Species.java`

- `hasSharedType(...)` dereferenziert weiterhin `getPrimaryType(false)` des Empfaengers.
- Der Fix liegt bewusst nicht global in `Species.hasSharedType(...)`, sondern eng im Same-Typing-Filter des `EvolutionRandomizer`.
- Diese Begrenzung vermeidet breitere Semantikaenderungen fuer andere Randomizer-Pfade.

### SpeciesSet / Pool

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/SpeciesSet.java`

- `SpeciesSet.filter(...)` reicht Kandidaten an das Predicate weiter und faengt keine `NullPointerException`.
- Der Same-Typing-Guard muss deshalb vor `candidate.hasSharedType(...)` sitzen; der aktuelle Code tut das.

### Gen3 Evolution Read/Write

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

- `loadEvolutions()` liest Method, ExtraInfo und Ziel-Species aus der Gen3-Evolution-Tabelle.
- `writeEvolutions()` schreibt Method, ExtraInfo, Ziel-Species und Padding.
- Im erweiterten BPRE-Hack nutzt `getEvolutionInternalSpeciesId(...)` `species.getSpeciesSetIdentityNumber()`.
- `Evolution.forme` ist kein persistiertes Gen3-Evolution-Tabellenfeld.

### Evolution-Logger

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/log/RandomizationLogger.java`

- `evolutionMethodToString(...)` nutzt defensive Fallbacks fuer Item-, Move-, Species- und Location-ExtraInfo.
- Unbekannte Item-ExtraInfos werden als `unknown item #<id>` geloggt, statt den Logpfad zu crashen.
- Sichtbare `Bad Egg`-Namen bleiben nach Diagnose 055 kontextabhaengige Log-/Sonder-Species-Marker.

## Was 081/082 entlastet oder nicht entlastet

081/082 entlasten direkt `FVX-TRAIT-018` Similar Strength, nicht Same Typing.

Fuer Same Typing relevant sind sie nur als Abgrenzung:

- Similar Strength nutzt die BST-Auswahl und nicht den Same-Typing-`hasUsableSharedType(...)`-Filter.
- Der in 081 diskutierte Forme-/Normalisierungsvergleich ist kein Same-Typing-Abbruchpfad.
- 082 bestaetigt die gemeinsame Reload-Normalisierung fuer persistierte Gen3-Evolution-Felder, aber die eigentliche Same-Typing-Freigabe kommt aus 080.

## Fehlende Evidenz

Diese Diagnose erhebt keine neue ROM-nahe Evidenz und ersetzt keinen neuen Smoke auf dem aktuellen Arbeitsbranch.

Weiterhin nicht aus `FVX-TRAIT-019` ableitbar:

- allgemeiner Evolution-Methoden-Writer-Support
- Change Impossible Evolutions
- Make Evolutions Easier
- Use Estimated Evolution Levels
- Remove Time-Based Evolutions
- TypeChart- oder TypeEffectiveness-Support
- Text/Menu- oder Itemnamen-Vollabdeckung
- globale Kombinationen mit anderen noch offenen Writer-Slices

## Naechster minimaler Pfad

Kein enger UPR-FVX-Fixblock ist als naechster Schritt gerechtfertigt.

Empfohlener Pfad:

1. `FVX-TRAIT-019` im Workspace/Dashboard aus dem aktiven Blockerstatus nehmen und als im engen Evolution-Species-Carrier stabil dokumentieren.
2. Bei weiterem Evidenzbedarf zuerst einen read-only Code-Review oder einen kleinen Non-ROM-Harness-Plan fuer den Same-Typing-Guard erstellen.
3. Einen neuen ROM-Smoke nur mit separater expliziter Freigabe starten.

## Reopen-Kriterien

`FVX-TRAIT-019` wieder als aktiver Fixblocker oeffnen, wenn eines davon belegt wird:

- ein Same-Typing-Slice wirft wieder eine `NullPointerException` oder anderen Save-Abbruch.
- ein normalisierter Reload-Vergleich meldet Evolution-Mismatches ungleich `0`.
- Same Typing waehlt Placeholder-/Special-Species als neues Ziel in einem nicht freigegebenen Kontext.
- `Bad Egg` korreliert mit Save-/Log-/Reload-Abbruch oder falschem Write.
- eine neue Kombination mit Evolution-Methoden, MoveData, TypeChart, Items, Text/Menu oder Graphics erzeugt einen separaten Fehler.

## Sicherheitsnotizen

- Es wurden nur bestehende Markdown-Diagnosen und lokale UPR-FVX-Quellen read-only inspiziert.
- Kein ROM, Save, Emulator State, Build, Randomizer-JAR, Tool-Binary, Log, Output-ROM, privater Pfad, Hash, Secret, Token oder `.env`-Inhalt wurde gelesen, kopiert, geaendert oder dokumentiert.
- Keine Original-Upstreams wurden kontaktiert.
