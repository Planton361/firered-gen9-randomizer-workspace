# 080 - Evolution Same Typing Null-Type Fix Diagnostics

Datum: 2026-05-14

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`

## Ziel

Dieses Protokoll dokumentiert den eng gegateten UPR-FVX-Fix fuer `FVX-TRAIT-019` Evolutions Same Typing.

Der Fix bleibt auf den Same-Typing-Filterpfad in `EvolutionRandomizer` begrenzt: Evolution-Replacement-Kandidaten mit `primaryType == null` duerfen nicht in `to.hasSharedType(...)` laufen.

Nicht geaendert wurden:

- `Species.hasSharedType(...)` als globale Methode.
- Wild.
- Trainer.
- TypeChart / TypeEffectiveness.
- MoveData Write.
- Palette.
- Items.
- Text/Menu.
- Graphics.
- Evolution-Methoden-Writer.

`FVX-TRAIT-018` Evolutions Similar Strength bleibt als eigener Slice getrennt. Die optionale Regression in diesem Protokoll ist kein eigener Fix und keine Vermischung mit dem Same-Typing-Fix.

## UPR-FVX-Fix

UPR-FVX-Commit:

```text
74d88a7ab1d306e1e09ccabb851dffd7f6922b66
```

Geaenderte UPR-FVX-Datei:

- `random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java`

Kurzfassung:

- Der Same-Typing-Filter ruft nicht mehr direkt `to.hasSharedType(...)` auf.
- Ein lokaler Helper prueft `candidate != null`, `reference != null` und `candidate.getPrimaryType(false) != null`, bevor `candidate.hasSharedType(reference)` ausgewertet wird.
- Kandidaten mit null/unsupported Primary Type werden im Same-Typing-Kontext defensiv aus dem Replacement-Pool gefiltert.
- Similar Strength, Evolution-Methoden, Evolution-Write und globale Species-Type-Semantik bleiben unveraendert.

## Checks

UPR-FVX:

```text
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
```

Build-Ergebnis:

```text
BUILD SUCCESSFUL
```

Lokale Smoke-Artefakte blieben ignored unter `05_builds/**` und werden nicht committed.

## Diagnose-Scope

Primaerer Smoke:

- `FVX-TRAIT-019` Evolutions Same Typing.
- Carrier: `FVX-TRAIT-016` Evolution-Species-Writer.

Optionale getrennte Regression:

- `FVX-TRAIT-018` Evolutions Similar Strength.
- Kein Support-Transfer aus dem Same-Typing-Fix.

Ausgeschlossen blieben:

- Wild.
- Trainer.
- TypeChart / TypeEffectiveness.
- MoveData Write / Update Moves.
- Field Items / Shops / Pickup.
- Encounter Held Items.
- Palette Randomization.
- Graphics / Sprites.
- Text / Menu.
- Trainer/Wild Level Modifier.
- Evolution-Methoden-Writer.
- Starter Held Items.
- Race Mode / Intro Mon.

## Diagnoseergebnisse

### `FVX-TRAIT-019` Evolutions Same Typing

- Aktive Feature-ID: `FVX-TRAIT-019`.
- Carrier-Writer: `FVX-TRAIT-016` Evolution-Species-Writer.
- Normalisierte Settings: `evolutionsMod=RANDOM`, `evosSameTyping=true`, `evosSimilarStrength=false`, `changeImpossibleEvolutions=false`, `makeEvolutionsEasier=false`, `updateMoves=false`, Wild-/Starter-Held-Items aus, Palette unveraendert, TypeEffectiveness unveraendert, Race Mode aus.
- `saveSuccessful=true`.
- `logSuccessful=true`.
- `outputRomExists=true`.
- `logNonEmpty=true`.
- Reload erfolgreich: `true`.
- `writeReloadEvolutionMismatches=0`.
- Null-Primary-Type-Species im geladenen Teststand: `0`.
- `Bad Egg=true`, nach 055 als bestehender Evolution-Log-/Sonder-Species-Marker klassifiziert, weil Save/Log/Output/Reload stabil sind und der Evolution-Reload-Mismatch-Zaehler `0` ist.
- `<unknown>=false`.
- `exceptionClass=none`.
- `stacktrace=none`.

Bewertung: `FVX-TRAIT-019` ist im eng getesteten Same-Typing-Scope entblockt. Der Nachweis gilt nicht fuer Evolution-Methoden-Writer oder andere Evolution-Suboptionen.

### `FVX-TRAIT-018` Evolutions Similar Strength Regression

- Aktive Feature-ID: `FVX-TRAIT-018`.
- Carrier-Writer: `FVX-TRAIT-016` Evolution-Species-Writer.
- Normalisierte Settings: `evolutionsMod=RANDOM`, `evosSameTyping=false`, `evosSimilarStrength=true`, `changeImpossibleEvolutions=false`, `makeEvolutionsEasier=false`, `updateMoves=false`, Wild-/Starter-Held-Items aus, Palette unveraendert, TypeEffectiveness unveraendert, Race Mode aus.
- `saveSuccessful=true`.
- `logSuccessful=true`.
- `outputRomExists=true`.
- `logNonEmpty=true`.
- Reload erfolgreich: `true`.
- `writeReloadEvolutionMismatches=0`.
- Null-Primary-Type-Species im geladenen Teststand: `0`.
- `Bad Egg=true`, nach 055 als bestehender Evolution-Log-/Sonder-Species-Marker klassifiziert, weil Save/Log/Output/Reload stabil sind und der Evolution-Reload-Mismatch-Zaehler `0` ist.
- `<unknown>=false`.
- `exceptionClass=none`.
- `stacktrace=none`.

Bewertung: Diese Regression zeigt, dass der Same-Typing-Fix den Similar-Strength-Pfad nicht regressiert. `FVX-TRAIT-018` bleibt als eigener Slice dokumentiert und wird nicht durch den Same-Typing-Fix vermischt.

## Sicherheitsnotizen

- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs oder Tool-Binaries wurden committed.
- Keine privaten Pfade, ROM-Namen, Hashes, Secrets, Tokens oder `.env`-Inhalte wurden dokumentiert.
- Lokale Diagnoseartefakte bleiben ignored unter `05_builds/**`.
- Keine Original-Upstreams wurden kontaktiert.
- Keine Original-Upstream-PRs wurden geoeffnet.
