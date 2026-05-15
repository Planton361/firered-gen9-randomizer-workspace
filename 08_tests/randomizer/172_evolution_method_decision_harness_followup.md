# 172 - Evolution Method Decision Harness Follow-up

## Scope

- Branch: `test/upr-fvx-cfru-dpe-evolution-method-decisions-followup`
- Voraussetzung: UPR-FVX PR #43 ist in `Planton361/universal-pokemon-randomizer-fvx` auf `compat/firered-gen9-cfru-dpe` gemerged.
- Modus: Workspace-Follow-up, Submodule-Gitlink-Pin und Dokumentation.
- Ergebnis: `tested-non-rom` fuer `FVX-TRAIT-024` und `FVX-TRAIT-027`, ohne P1-Promotion.

Nicht ausgefuehrt: ROM-Smoke, Randomizer-Lauf, Build, Gen3-Writer-Test, Reload-Test, Output-ROM, Save, Emulator, Log-Artefakt oder weitere UPR-FVX-Codeaenderung.

## UPR-FVX PR

- PR: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/43>
- Fork-Base: `compat/firered-gen9-cfru-dpe`
- Urspruenglicher Commit: `4b049ee82cf8716cb2fc17d0b6244020cddd22e4`
- Gemergter UPR-FVX-Commit / Workspace-Pin:

```text
3b33412e80d1cb2d97725ad7a7dd01529aa56919
```

## Geaenderte UPR-FVX-Dateien

- `romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractRomHandler.java`
- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `romio/src/test/java/com/uprfvx/romio/romhandlers/EvolutionMethodDecisionTest.java`

## Test-/Seam-Entscheidung

- `Gen3RomHandler` enthaelt einen kleinen package-private Decision-Seam fuer Gen3 Change-Impossible-Mappings.
- `AbstractRomHandler` enthaelt einen kleinen package-private Decision-Seam fuer Time-Based-Mappings.
- `EvolutionMethodDecisionTest` nutzt synthetische `Species`-/`Evolution`-Objekte und keine ROM-Datei.
- Der Test deckt Mapping-/Decision-Logik ab, nicht Writer, Reload oder Randomizer-Ausfuehrung.

## Getestete Feature-IDs

### `FVX-TRAIT-024` - Change Impossible Evolutions

Getestete ROM-freie Decisions:

- FRLG `HAPPINESS_DAY` zu Sun Stone.
- FRLG `HAPPINESS_NIGHT` zu Moon Stone.
- FRLG `HIGH_BEAUTY` zu Level.
- Pure Trade zu Level.
- Trade-Item-Species-Branches fuer Poliwhirl, Slowpoke und Seadra.
- Clamperl-Item-Branches fuer `deepSeaTooth` und `deepSeaScale`.
- generischer Trade-Item-Fallback.
- `useEstimatedLevels` fuer Level-Zielmethoden.
- FRLG-only Happiness bleibt ausserhalb FRLG unveraendert.

Statuswirkung: `tested-non-rom`, aber keine P1-Freigabe. Writer-/Reload-Evidenz fuer Gen3 Method-Index und Standard-vs-internes Item-`extraInfo` bleibt offen.

### `FVX-TRAIT-027` - Remove Time-Based Evolutions

Getestete ROM-freie Decisions:

- gepaarte Day/Night-Evolutionen zu Sun/Moon Stone.
- `LEVEL_DUSK` zu Dusk Stone.
- ungepaarte Time-Based-Methode zu `timeless()` mit erhaltenem `extraInfo`.
- nicht zeitbasierte Methoden bleiben unveraendert.

Statuswirkung: `tested-non-rom`, aber keine P1-Freigabe. Writer-/Reload-Evidenz fuer Sun/Moon/Dusk-Stone-Item-Konvertierung und Evolution-Table-Reload bleibt offen.

## Checks aus 172A

- `./gradlew --offline :romio:test --tests '*Evolution*'`: `BUILD SUCCESSFUL`
- `./gradlew --offline :romio:test`: `BUILD SUCCESSFUL`
- bekannte bestehende Report-Failure-Zeile bleibt Risiko/Annahme:
  `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()`

## Grenzen

- Keine Writer-/Reload-Evidenz.
- Kein ROM-Smoke.
- Keine P1-Promotion.
- Kein vollstaendiger Gen3 `writeEvolutions()`- oder `loadEvolutions()`-Durchlauf.
- Kein `FVX-TRAIT-025`/`FVX-TRAIT-026`-Scope, ausser `useEstimatedLevels` als Decision-Input fuer `024`.

## Statuswirkung

- `FVX-TRAIT-024` steigt von `decision-review-ready` auf `tested-non-rom`.
- `FVX-TRAIT-027` steigt von `decision-review-ready` auf `tested-non-rom`.
- `FVX-TRAIT-025` bleibt separat zu splitten: ROM-freie Condense-Logik und Gen3-Happiness-Byte-Patch.
- `FVX-TRAIT-026` bleibt Helper-Flag fuer `024/025`, ohne standalone Support-Claim.

## Empfohlener naechster Schritt

Naechster minimaler Workspace-Pfad ist ein read-only Plan fuer `FVX-TRAIT-025`:

- Condense-Level-Logik ROM-frei abgrenzen.
- Gen3-Happiness-Byte-Patch separat als Writer-/Reload-Risiko behandeln.
- `FVX-TRAIT-026` nur als Zusatzflag in `024/025` fuehren.

Ein spaeterer Writer-/Reload- oder ROM-Smoke-Scope fuer `024/027` darf nur separat freigegeben werden.

## Sicherheitsnotizen

- Der Workspace pinnt nur den UPR-FVX-Submodule-Gitlink auf den gemergten PR-#43-Commit.
- Keine Workspace-Codeaenderung.
- Keine weiteren UPR-FVX-Codeaenderungen in diesem Block.
- Kein ROM, Save, Emulator State, Build, Randomizer-JAR, Tool-Binary, Log, Output-ROM, privater Pfad, Hash, Secret, Token oder `.env`-Inhalt wurde gelesen, kopiert, geaendert oder dokumentiert.
- Keine Original-Upstreams wurden kontaktiert.
