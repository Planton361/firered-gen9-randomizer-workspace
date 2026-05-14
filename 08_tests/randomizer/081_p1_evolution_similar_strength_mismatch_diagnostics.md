# 081 - P1 Evolution Similar Strength Mismatch Diagnostics

Datum: 2026-05-14

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-evolution-similar-strength-mismatch-diagnostics`

## Scope

Dieses Protokoll ist eine read-only Code-/Protokollanalyse fuer den verbleibenden 070-Blocker `FVX-TRAIT-018` Evolutions Similar Strength.

Es gab keine Codeaenderung, keinen Fix und keine Randomizer-Laeufe. Untersucht wurden nur Evolution-Randomizer-, Similar-Strength-/BST-Auswahl- und Evolution-Write-/Reload-Codepfade.

Ausgeschlossen bleiben Wild, Trainer, TypeChart / TypeEffectiveness, MoveData Write, Palette, Items, Text/Menu, Graphics und Evolution-Methoden-Writer.

`FVX-TRAIT-019` Evolutions Same Typing ist nach Diagnose 080 im engen Same-Typing-/Null-Primary-Type-Scope entblockt. Dieser Befund wird hier nur als Abgrenzung genutzt und nicht mit `FVX-TRAIT-018` vermischt.

## Ausgangsbefund aus 070

`FVX-TRAIT-018` Evolutions Similar Strength:

- Carrier: `FVX-TRAIT-016` Evolution-Species-Writer.
- Aktive Settings: Evolution Randomization mit `evosSimilarStrength=true`.
- `saveSuccessful=true`.
- `logSuccessful=true`.
- `outputRomExists=true`.
- `logNonEmpty=true`.
- Reload erfolgreich: `true`.
- `writeReloadEvolutionMismatches=24`.
- `Bad Egg=true`.
- `<unknown>=false`.
- `stacktrace=none`.
- Exception-Klasse: `none`.

Stop-Regel aus 070: Der Reload-Mismatch-Zaehler war ungleich `0`; deshalb durfte `Bad Egg=true` dort nicht als reine 055-Log-Hygiene freigegeben werden.

## Relevante Codepfade

### EvolutionRandomizer Entry und Carrier

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`

- `randomizeEvolutions()` liest `similarStrength = settings.isEvosSimilarStrength()` und `sameType = settings.isEvosSameTyping()`.
- Der Carrier-Pool kommt aus `RestrictedSpeciesService.getSpecies(false, romHandler.altFormesCanHaveDifferentEvolutions(), false)`.
- `randomizeEvolutionsInner()` iteriert ueber `pokemonPool`, holt die gecachten Original-Evolutionen und waehlt pro Original-Evolution ein neues Ziel.
- Bei `similarStrength=true` nutzt die Zielauswahl `possible.getRandomSimilarStrengthSpecies(evo.getTo(), random)`.

Der Similar-Strength-Pfad erreicht damit die BST-basierte Auswahl, aber nicht den Same-Typing-`hasSharedType(...)`-Filter.

### Similar-Strength-/BST-Auswahl

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/SpeciesSet.java`

- `getRandomSimilarStrengthSpecies(Species match, Random random)` leitet an `getRandomSimilarStrengthSpecies(match, false, -1, random)` weiter.
- Bei fehlendem Override nutzt der Pfad `match.getBSTForPowerLevels()` als Ziel-BST.
- Der Kandidatenpool wird iterativ um Ziel-BST-Bereiche erweitert, bis die Mindestpoolgroesse erreicht ist.

Der Pfad benutzt keine Type-Pruefung und ruft nicht `Species.hasSharedType(...)` auf. Der Null-Primary-Type-Fix aus 080 wirkt daher nicht direkt auf Similar Strength.

### Evolution-Objekt und kosmetische Forme

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`

- `prepareNewEvolution(...)` uebernimmt Evolution-Type, ExtraInfo und Estimated-Level aus der Original-Evolution.
- Danach setzt der Randomizer immer `newEvo.setForme(picked.getRandomCosmeticFormeNumber(random))`.

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Species.java`

- `getRandomCosmeticFormeNumber(...)` kann bei Species mit kosmetischen Formes einen nicht-null beziehungsweise nicht-default Forme-Wert liefern.

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Evolution.java`

- `Evolution.toString()` gibt `forme:%d` aus, wenn `forme != 0`.
- `Evolution.equals(...)` vergleicht dagegen Type, ExtraInfo, From und To, aber nicht `forme` und nicht `estimatedEvoLvl`.

### Gen3 Evolution Write/Reload

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

- `writeEvolutions()` schreibt pro Evolution-Slot Method, ExtraInfo, Ziel-Species und Padding.
- Im erweiterten BPRE-Hack nutzt `getEvolutionInternalSpeciesId(...)` die interne `SpeciesSet`-Identitaet fuer Ziel-Species.
- `writeEvolutions()` schreibt keinen `Evolution.forme`-Wert.
- `loadEvolutions()` liest Method, ExtraInfo und Ziel-Species zurueck und erzeugt neue `Evolution(...)`-Objekte ohne Forme-Wert.

Das entspricht dem stabilen Scope aus Diagnose 026: Der Reload-Vergleich muss dieselben Evolution-Zielspecies wieder als dieselben internen Identitaeten erkennen. Kosmetische Forme-Werte sind in diesem Gen3-Schreibpfad kein persistiertes Feld.

### Evolution-Log / Bad Egg

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/log/RandomizationLogger.java`

- `logEvolutions()` iteriert ueber `romHandler.getSpeciesInclFormes()` und schreibt `pk.getFullName()` sowie `evo.getTo().getFullName()`.
- Ein bestehender Sonder-Species-Name wie `Bad Egg` wird dadurch sichtbar, wenn diese Species als Evolution-Quelle oder -Ziel im Log steht.

Diagnose 026 dokumentierte bereits einen Evolution-Log-Eintrag `Bad Egg -> ...` bei stabilem Save/Log/Output/Reload und `writeReloadMismatches=0`. 055 klassifiziert `Bad Egg` daher pro Pfad: sichtbar allein ist kein Fehler; kritisch wird der Marker erst zusammen mit Abbruch, falschem Write oder Reload-Mismatches.

## Ursache oder eingegrenzte Hypothese

Wahrscheinlichste Einordnung des 070-Befunds:

`writeReloadEvolutionMismatches=24` war sehr wahrscheinlich kein harter Evolution-Species-Write-Fehler, sondern ein zu breiter oder falsch normalisierter Diagnosevergleich fuer `FVX-TRAIT-018`.

Die Codepfade zeigen:

- Similar Strength waehlt Ziel-Species via BST und nutzt den stabilen `FVX-TRAIT-016` Evolution-Species-Writer.
- Der Writer schreibt Ziel-Species im erweiterten BPRE-Hack ueber interne `SpeciesSet`-Identitaet.
- `prepareNewEvolution(...)` setzt zusaetzlich einen kosmetischen `forme`-Wert.
- Der Gen3-Write-/Reload-Pfad persistiert diesen `forme`-Wert nicht und rekonstruiert ihn beim Reload nicht.
- `Evolution.toString()` kann Forme-Werte sichtbar machen, obwohl `Evolution.equals(...)` und die 026-Reload-Semantik sie nicht als Write-/Reload-Kriterium behandeln.

Damit passt der Befund zu einem Diagnose-Harness, der Forme- oder komplette String-/Objekt-Darstellung verglichen hat, statt nur die persistierten Evolution-Felder beziehungsweise die Ziel-Species-Identitaet nach 026. Eine Zahl wie `24` ist plausibel als Anzahl von Evolutionen mit nicht-default kosmetischem Forme-Wert oder anderem nicht-persistiertem Zusatzfeld im Similar-Strength-Lauf.

Nicht ausgeschlossen, aber weniger wahrscheinlich ohne neuen lokalen Lauf:

- einzelne Similar-Strength-Picks koennten Placeholder-/Special-Species erreichen.
- einzelne Original-Evolutionen koennten Sonder-Species wie `Bad Egg` als Quelle behalten.
- ein Vergleich koennte Estimated-Level oder Forme-Felder einbeziehen, obwohl der Gen3-Writer sie nicht im gleichen Sinn persistiert.

## Bad Egg Einordnung

`Bad Egg=true` korreliert aus den vorhandenen Belegen nicht zwingend mit dem 070-Mismatch:

- 026 zeigt `Bad Egg` im Evolution-Log bei `writeReloadMismatches=0`.
- 080 zeigt fuer den getrennten Similar-Strength-Regressionslauf ebenfalls `Bad Egg=true`, aber `writeReloadEvolutionMismatches=0`.
- Der Logger schreibt sichtbare Species-Namen aus den Evolution-Quellen/-Zielen; er beweist damit nicht allein einen falschen Write.

Im 070-Dokument war die konservative Stop-Regel trotzdem korrekt: Solange gleichzeitig `writeReloadEvolutionMismatches=24` dokumentiert war, durfte `Bad Egg=true` nicht als unkritischer 055-Marker freigegeben werden.

Nach der Code-/Protokollanalyse ist die wahrscheinlichere Trennung:

- `Bad Egg=true`: bestehender Evolution-Log-/Sonder-Species-Marker, nach 055 klassifizierbar, wenn der Reload-Vergleich korrekt auf persistierte Felder normalisiert und `0` Mismatches meldet.
- `writeReloadEvolutionMismatches=24`: wahrscheinlich Diagnosevergleichs-/Normalisierungsproblem, nicht Same-Typing- oder TypeChart-Problem.

## Abgrenzung zu Diagnose 080

Der 080-Fix wirkt nur im Same-Typing-Filter:

- Er guardet Kandidaten mit `primaryType == null`, bevor `hasSharedType(...)` ausgewertet wird.
- Dieser Helper wird nur im `if (sameType)`-Block genutzt.
- Bei `FVX-TRAIT-018` ist `evosSameTyping=false`; der Similar-Strength-Pfad nutzt `getRandomSimilarStrengthSpecies(...)`.

080 beeinflusst Similar Strength daher nicht fachlich. Die optionale 080-Regression ist trotzdem ein wichtiger Hinweis: Mit einem auf Ziel-Species-Identitaet normalisierten Reload-Vergleich kann `FVX-TRAIT-018` Save/Log/Output/Reload true und `writeReloadEvolutionMismatches=0` erreichen, ohne denselben Fixpfad wie Same Typing zu nutzen.

## Braucht es noch einen lokalen Diagnose-Smoke?

Ja, aber nicht als Fixbranch und nicht im ersten Schritt.

Empfohlen ist ein separater, eng freigegebener Test-/Diagnoseblock fuer `FVX-TRAIT-018` mit einem explizit normalisierten Reload-Vergleich:

- Vergleiche pro Evolution-Quelle nur persistierte Gen3-Felder: Type, ExtraInfo nach Item-ID-Normalisierung und Ziel-Species per interner `SpeciesSet`-Identitaet.
- Vergleiche `forme` nicht als Write-/Reload-Kriterium, solange kein Evolution-Forme-Writer modelliert ist.
- Dokumentiere optional, wie viele nicht-default Forme-Werte vor dem Write im Arbeitsspeicher existieren, aber nur als diagnostischen Zaehler.
- Klassifiziere `Bad Egg` nach 055 getrennt vom Mismatch-Zaehler.

Ein Code-Fix ist nach dieser read-only Analyse nicht als erster Schritt sinnvoll. Zuerst sollte der 070-Befund mit einem korrekten Diagnosevergleich reproduziert oder widerlegt werden.

## Voraussichtliche Fix- oder Testoberflaeche

Kein sofortiger UPR-FVX-Fix empfohlen.

Falls der naechste Diagnose-Smoke mit normalisiertem Vergleich `writeReloadEvolutionMismatches=0` ergibt:

- Workspace-Dokumentation aktualisieren.
- `FVX-TRAIT-018` konservativ als stabilen Similar-Strength-Scope im `FVX-TRAIT-016` Carrier einordnen.
- Kein UPR-FVX-Code-Fix noetig.

Falls der normalisierte Vergleich weiterhin Mismatches ungleich `0` ergibt:

- Danach erst einen eng gegateten Fixplan fuer `EvolutionRandomizer` Similar-Strength-/Pool-Scope erstellen.
- Potentielle Fixflaeche waere primaer `EvolutionRandomizer` beziehungsweise der Evolution-Replacement-Pool.
- Nicht automatisch Evolution-Methoden-Writer, TypeChart, MoveData, Palette, Items, Text/Menu oder Graphics einbeziehen.

## Empfohlener naechster Prompt

```text
Arbeitsbranch:
test/upr-fvx-cfru-dpe-p1-evolution-similar-strength-normalized-reload

Ziel:
Fuehre nur den FVX-TRAIT-018 Evolutions Similar Strength Smoke lokal aus und dokumentiere ihn sanitisiert. Keine Codeaenderung, kein Fix. Der Reload-Vergleich muss auf persistierte Gen3-Evolution-Felder normalisiert sein: Evolution-Type, ExtraInfo mit Item-ID-Normalisierung und Ziel-Species per interner SpeciesSet-Identitaet. Evolution.forme nicht als Mismatch-Kriterium werten; nicht-default Forme-Werte optional nur als sanitisierten Diagnosezaehler dokumentieren.

Ausgeschlossen:
Wild, Trainer, TypeChart, MoveData, Palette, Items, Text/Menu, Graphics, Evolution-Methoden-Writer und FVX-TRAIT-019 Same Typing.

Erwartete Metriken:
saveSuccessful, logSuccessful, outputRomExists, logNonEmpty, Reload erfolgreich, writeReloadEvolutionMismatches, Bad Egg / <unknown> nach 055 klassifizieren, exceptionClass, stacktrace.
```

## Sicherheitsnotizen

- Keine Codeaenderung.
- Keine Aenderung an `02_external/**`.
- Keine Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, privaten Pfade, ROM-Namen, Hashes, Secrets, Tokens oder `.env`-Inhalte gelesen, kopiert, geaendert oder dokumentiert.
- Keine Original-Upstreams wurden kontaktiert.
