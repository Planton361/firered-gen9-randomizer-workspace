# 165 - Evolution Similar Strength Diagnostics

## Datum

2026-05-15

## Branch

```text
test/upr-fvx-cfru-dpe-evolution-similar-strength-diagnostics
```

## Scope

Read-only Diagnose fuer `FVX-TRAIT-018` Evolution Similar Strength im getesteten CFRU/DPE Gen9-BPRE-Scope.

Nicht ausgefuehrt:

- kein ROM-Smoke
- kein Species-Write-Smoke
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

`FVX-TRAIT-018` ist fuer den bereits dokumentierten engen Evolution-Species-Carrier-Scope nicht mehr als aktiver Fixblocker einzuordnen. Die historische Blockerzeile aus Diagnose 070 wird durch die spaeteren Diagnosen 081 und 082 neu bewertet:

- Diagnose 070 meldete fuer Evolution Similar Strength Save/Log/Output/Reload true, aber `writeReloadEvolutionMismatches=24` und `Bad Egg=true`.
- Diagnose 081 zeigte read-only, dass der Mismatch-Zaehler sehr wahrscheinlich aus einem zu breiten Vergleich gegen nicht persistierte Forme-/Zusatzfelder stammte.
- Diagnose 082 bestaetigte den normalisierten Scope mit Save/Log/Output/Reload true, `normalizedWriteReloadEvolutionMismatches=0`, `rawWithFormeWriteReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- `Bad Egg=true` bleibt nach Diagnose 055 ein bestehender Evolution-Log-/Sonder-Species-Marker, solange der normalisierte Reload-Vergleich stabil bleibt und keine Mismatches oder Abbrueche auftreten.

## Bereits supported

### Evolution Species-only

Diagnose 026 bestaetigt `FVX-TRAIT-016` Evolution-Species-Writer im getesteten CFRU/DPE Gen9-BPRE-Scope:

- Evolution-Replacement-Pool erreicht Gen1-Gen9.
- Gen7/8/9-Ziele werden gepickt.
- `loadEvolutions()` und `writeEvolutions()` nutzen im erweiterten BPRE-Hack interne `SpeciesSet`-Identitaet.
- Reload nutzt dieselbe Ziel-Species-Identitaet.
- `writeReloadMismatches=0`.
- Evolution-Logger faellt bei unbekannten ExtraInfo-Werten defensiv auf Marker wie `unknown item #1732` zurueck.

### Evolution Similar Strength

Diagnose 082 bestaetigt `FVX-TRAIT-018` im engen `FVX-TRAIT-016` Evolution-Species-Carrier:

- Similar Strength aktiv, Same Typing inaktiv.
- Evolution-Methoden-Writer, MoveData, TypeChart, Palette, Items, Text/Menu und Graphics aus Scope.
- Reload-Vergleich normalisiert auf persistierte Gen3-Evolution-Felder:
  - Evolution-Type
  - ExtraInfo mit Gen3-Item-ID-Normalisierung
  - Ziel-Species per interner `SpeciesSet`-Identitaet
  - `Evolution.forme` nicht als Mismatch-Kriterium
- Ergebnis stabil mit `normalizedWriteReloadEvolutionMismatches=0`.

## Read-only Codepfad

### EvolutionRandomizer

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`

- `randomizeEvolutions()` liest `settings.isEvosSimilarStrength()` und reicht den Wert an den inneren Randomizer weiter.
- `randomizeEvolutionsInner()` iteriert ueber den Evolution-Pool, ermittelt moegliche Ziele und nutzt bei `similarStrength=true`:

```text
possible.getRandomSimilarStrengthSpecies(evo.getTo(), random)
```

- `prepareNewEvolution(...)` uebernimmt Type, ExtraInfo und Estimated-Level aus der Original-Evolution und setzt danach optional einen kosmetischen Forme-Wert.
- Der Same-Typing-Null-Type-Guard ist ein separater Pfad: Similar Strength nutzt die BST-Auswahl, nicht den `hasUsableSharedType(...)`-Filter.

### SpeciesSet Similar Strength

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/SpeciesSet.java`

- `getRandomSimilarStrengthSpecies(Species match, Random random)` leitet an den gemeinsamen Similar-Strength-Helper weiter.
- Der Helper nutzt bei fehlendem Override `match.getBSTForPowerLevels()` als Ziel-BST.
- Der Kandidatenpool wird ueber wachsende BST-Bereiche aufgebaut und daraus zufaellig gewaehlt.

### Gen3 Evolution Read/Write

`02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

- `loadEvolutions()` liest Method, ExtraInfo und Ziel-Species aus der Gen3-Evolution-Tabelle.
- `writeEvolutions()` schreibt Method, ExtraInfo, Ziel-Species und Padding.
- Im erweiterten BPRE-Hack nutzt `getEvolutionInternalSpeciesId(...)` `species.getSpeciesSetIdentityNumber()`.
- `Evolution.forme` ist kein persistiertes Gen3-Evolution-Tabellenfeld und darf fuer diesen Reload-Vergleich nicht als Write-Mismatch gewertet werden.

### Evolution-Logger

`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/log/RandomizationLogger.java`

- `evolutionMethodToString(...)` nutzt defensive Fallbacks fuer Item-, Move-, Species- und Location-ExtraInfo.
- Unbekannte Item-ExtraInfos werden als `unknown item #<id>` geloggt, statt den Logpfad zu crashen.
- Sichtbare `Bad Egg`-Namen bleiben pro Diagnose 055 kontextabhaengige Log-/Sonder-Species-Marker.

## Was blockierte vorher

Der relevante alte Blocker war nicht Save oder Reload selbst, sondern die 070-Kombination:

```text
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
reloadSuccessful=true
writeReloadEvolutionMismatches=24
Bad Egg=true
```

Diese Stop-Regel war in 070 korrekt, weil `Bad Egg=true` nicht zusammen mit einem Mismatch-Zaehler freigegeben werden durfte.

Nach 081/082 ist der belegte Restbefund:

- der Mismatch war ein zu breiter oder falsch normalisierter Diagnosevergleich, kein bestaetigter Writer-Fehler.
- ein normalisierter Vergleich der persistierten Gen3-Felder meldet `0` Mismatches.
- `Bad Egg=true` ist in diesem stabilen Zustand nicht als neuer Fixblocker belegt.

## Fehlende Evidenz

Diese Diagnose erhebt keine neue ROM-nahe Evidenz und ersetzt keinen neuen Smoke auf dem aktuellen Arbeitsbranch.

Weiterhin nicht aus `FVX-TRAIT-018` ableitbar:

- allgemeiner Evolution-Methoden-Writer-Support
- Change Impossible Evolutions
- Make Evolutions Easier
- Use Estimated Evolution Levels
- Remove Time-Based Evolutions
- Text/Menu- oder Itemnamen-Vollabdeckung
- globale Kombinationen mit anderen noch offenen Writer-Slices

## Naechster minimaler Pfad

Kein enger UPR-FVX-Fixblock ist als naechster Schritt gerechtfertigt.

Empfohlener Pfad:

1. `FVX-TRAIT-018` im Workspace/Dashboard aus dem aktiven Blockerstatus nehmen und als im engen Evolution-Species-Carrier stabil dokumentieren.
2. Bei weiterem Evidenzbedarf zuerst einen read-only Code-Review oder einen kleinen Non-ROM-Harness-Plan fuer die Similar-Strength-Auswahl/Normalisierung erstellen.
3. Einen neuen ROM-Smoke nur mit separater expliziter Freigabe starten.

## Reopen-Kriterien

`FVX-TRAIT-018` wieder als aktiver Fixblocker oeffnen, wenn eines davon belegt wird:

- ein normalisierter Reload-Vergleich meldet wieder Evolution-Mismatches ungleich `0`.
- Similar Strength waehlt Placeholder-/Special-Species als neues Ziel in einem nicht freigegebenen Kontext.
- `Bad Egg` korreliert mit Save-/Log-/Reload-Abbruch oder falschem Write.
- eine neue Kombination mit Evolution-Methoden, MoveData, TypeChart, Items, Text/Menu oder Graphics erzeugt einen separaten Fehler.

## Sicherheitsnotizen

- Es wurden nur bestehende Markdown-Diagnosen und lokale UPR-FVX-Quellen read-only inspiziert.
- Kein ROM, Save, Emulator State, Build, Randomizer-JAR, Tool-Binary, Log, Output-ROM, privater Pfad, Hash, Secret, Token oder `.env`-Inhalt wurde gelesen, kopiert, geaendert oder dokumentiert.
- Keine Original-Upstreams wurden kontaktiert.
