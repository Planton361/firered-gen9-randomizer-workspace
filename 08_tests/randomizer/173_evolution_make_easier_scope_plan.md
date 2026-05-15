# 173 - Evolution Make Evolutions Easier Scope Plan

## Scope

- Branch: `test/upr-fvx-cfru-dpe-evolution-make-easier-scope-plan`
- Voraussetzung: Workspace PR #221 / Follow-up 172B ist in `main` gemerged.
- Modus: read-only Diagnose und Scope-Plan.
- Ergebnis: `make-easier-plan-ready`

Nicht ausgefuehrt: ROM-Smoke, Randomizer-Lauf, Build, UPR-FVX-Codeaenderung, Submodule-Aenderung, Writer-/Reload-Test, Output-ROM, Save, Emulator oder Log-Artefakt.

## Gelesene Evidenz

- Diagnose 170: Evolution methods/improvement slices sind getrennt geplant; `FVX-TRAIT-025` ist in Condense-Logik und Gen3-Happiness-Byte-Patch zu splitten.
- Diagnose 171: `FVX-TRAIT-024` und `027` sind Decision-Review-ready; `025` bleibt getrennt.
- Diagnose 172B: `FVX-TRAIT-024` und `027` sind durch UPR-FVX PR #43 `tested-non-rom`; keine P1-Promotion.
- UPR-FVX `GameRandomizer.maybeApplyEvolutionImprovements()`.
- UPR-FVX `AbstractRomHandler.condenseLevelEvolutions(...)`, `estimateEvolutionLevels(...)` und `Evolution.updateEvolutionMethod(...)`.
- UPR-FVX `Gen3RomHandler.makeEvolutionsEasier(...)` und `Gen3Constants.friendshipValueForEvoLocator`.
- Vorhandene Tests: ROM-backed `RomHandlerEvolutionTest`, ROM-freie `EvolutionTest` und die neuen Non-ROM Decision-/Filter-Tests.

## Dispatch-Befund

`FVX-TRAIT-025` ist kein einzelner homogener Writer-Pfad. `GameRandomizer.maybeApplyEvolutionImprovements()` fuehrt bei aktivem Make-Easier-Flag zwei getrennte Aktionen aus:

1. `romHandler.condenseLevelEvolutions(settings.getMakeEvolutionsEasierLvl())`
2. `romHandler.makeEvolutionsEasier(wildsRandomizer, useEstimatedLevels)`

Der erste Pfad mutiert `Evolution`-Datenmodellwerte im Arbeitsspeicher. Der zweite Gen3-Pfad sucht eine Friendship-Locator-Signatur im ROM-Bytearray und patcht die Happiness-Schwellenwerte von 220 auf 160. Deshalb muss `025` fuer weitere Arbeit getrennt werden.

## FVX-TRAIT-025A - Condense-/Level-/Decision-Logik

| Aspekt | Bewertung |
|---|---|
| Erwarteter Pfad | `AbstractRomHandler.condenseLevelEvolutions(int maxLevel)` laeuft ueber `getSpeciesSetInclFormes()`, senkt Level-Threshold-`extraInfo` und `estimatedEvoLvl`, markiert betroffene Evolutions und aktualisiert `highestEvoLvl`. |
| Datenmodell | `Evolution.type`, `extraInfo`, `estimatedEvoLvl`, `Species.evolutionsFrom`, `Species.evolutionsTo`; intermediate stages werden auf `ceil(0.75 * maxLevel)` begrenzt, finale Stufen auf `maxLevel`. |
| ROM-frei testbar? | Ja. Synthetische `Species`-Ketten und `Evolution`-Objekte reichen fuer Condense-Entscheidungen, ohne ROM-Datei, Save, Reload oder Writer. |
| Writer-/Reload-Evidenz noetig? | Ja fuer P1, weil ein Non-ROM-Test nur die In-Memory-Decision prueft. Persistenz der Evolution-Tabelle bleibt ein separater Writer-/Reload-Scope. |
| Test-Seam noetig? | Wahrscheinlich klein. Entweder ein schmaler Test-Handler mit synthetischem SpeciesSet oder ein package-private Helper fuer die Condense-Decision; kein breiter Handler-Refactor. |
| Risiken | `highestEvoLvl`-Vorbedingung, Zwischenstufen-Erkennung ueber `to.evolutionsFrom`, `estimatedEvoLvl` fuer nicht-Level-Methoden, Formes im SpeciesSet, Gleichlauf von `extraInfo` und `estimatedEvoLvl`. |
| Empfohlener Mini-Scope | Spaeterer UPR-FVX Non-ROM `:romio:test` fuer synthetische 2- und 3-Stufen-Ketten: keine Aenderung bei `maxLevel >= highestEvoLvl`, intermediate cap, final cap, non-level `estimatedEvoLvl` cap und `highestEvoLvl`-Update. |

## FVX-TRAIT-025B - Gen3 Happiness-Byte-Patch / writer-like Scope

| Aspekt | Bewertung |
|---|---|
| Erwarteter Pfad | `Gen3RomHandler.makeEvolutionsEasier(...)` sucht `Gen3Constants.friendshipValueForEvoLocator` im ROM-Bytearray und schreibt Happiness-Schwellenwerte nur, wenn die erwarteten Vanilla-Bytes vorhanden sind. |
| Datenmodell | ROM-Bytes statt Evolution-Objekte: Basis-Happiness an `offset`, fuer Nicht-FRLG zusaetzlich `offset + 38` und `offset + 66` fuer Day/Night-Happiness. |
| ROM-frei testbar? | Teilweise. Ein Bytearray-/Decision-Seam koennte ohne ROM-Datei pruefen, dass nur Vanilla-Bytes gepatcht und Nicht-Vanilla-Bytes preserved werden. Ein echter Handler-Durchlauf braucht ROM-/RomEntry-Zustand und ist fuer diesen Plan nicht erlaubt. |
| Writer-/Reload-Evidenz noetig? | Ja. Das ist ein writer-like Byte-Patch; P1 braucht spaeter einen separat freigegebenen Writer-/Reload- oder ROM-Smoke-Scope. |
| Test-Seam noetig? | Ja, wenn ROM-frei getestet werden soll: kleiner package-private Helper fuer Locator-/Offset-Entscheidung oder Byte-Patch-Operation. Kein echter Gen3-Writer-Test in diesem Plan. |
| Risiken | Locator nicht gefunden, mehrfacher Locator, FRLG-vs-Nicht-FRLG Day/Night-Offsets, Byte `vanillaHappinessToEvolve - 1`, Preserve-Policy fuer unerwartete Bytes, keine Evolution-Table-Reload-Evidenz. |
| Empfohlener Mini-Scope | Erst nach 025A: read-only Code-Review oder Non-ROM Byte-Patch-Testplan. Ein Implementierungsblock soll stoppen, wenn echte ROM-Fixtures, private Pfade, Output-ROMs, breite Reflection oder vollstaendige Handler-Konstruktion noetig werden. |

## FVX-TRAIT-026 - Helper-Flag

`FVX-TRAIT-026` Use Estimated Evolution Levels bleibt ein Helper-Flag, kein eigener Support-Claim.

- Relevant fuer `FVX-TRAIT-024`, wenn unmögliche Evolutions zu Level-Methoden umgeschrieben werden.
- Relevant fuer `FVX-TRAIT-025`, wenn Make-Easier-Entscheidungen Levelwerte aus `estimatedEvoLvl` statt hart kodierten Levels verwenden.
- Nicht relevant als eigenstaendiger GUI-Smoke, weil das Flag ohne `024` oder `025` keine eigene Writer-/Mutation-Aktion ausloest.
- Tests sollen `026` als Parameter/Assertion in `024`- oder `025A`-Faellen fuehren, nicht als separate Feature-Promotion.
- Status bleibt `helper-flag / no standalone support claim`.

## Ergebnis

```text
make-easier-plan-ready
```

`FVX-TRAIT-025` ist sauber in 025A und 025B trennbar. Der naechste kleinste sinnvolle Schritt ist 025A als ROM-freier Condense-/Level-Decision-Harness. 025B bleibt separater Gen3-Happiness-Byte-Patch-/Writer-Scope und darf nicht mit 025A vermischt werden.

## Statuswirkung

- `FVX-TRAIT-025` steigt von `methods-plan-ready / split planned` auf `make-easier-plan-ready / split into 025A+025B`.
- `FVX-TRAIT-026` bleibt Helper-Flag fuer `024/025`, ohne standalone Support-Claim.
- Keine P1-Promotion, kein `tested-non-rom` fuer `025`, keine Writer-/Reload-Freigabe.

## Empfohlener naechster Schritt

Spaeterer UPR-FVX Code-Test-Block nur fuer `025A`:

- Non-ROM `:romio:test` mit synthetischen Species/Evolution-Daten.
- Ziel: Condense-Level-Logik, `estimatedEvoLvl`-Kappung und `highestEvoLvl`-Verhalten pruefen.
- `025B` Happiness-Byte-Patch, ROM-Smoke, Writer/Reload, Save, Output-ROM und echte Gen3-ROM-Bytes bleiben verboten, bis separat freigegeben.

## Sicherheitsnotizen

- Es wurden nur bestehende Markdown-Diagnosen und lokale UPR-FVX-Quellen read-only inspiziert.
- Kein ROM, Save, Emulator State, Build, Randomizer-JAR, Tool-Binary, Log, Output-ROM, privater Pfad, Hash, Secret, Token oder `.env`-Inhalt wurde gelesen, kopiert, geaendert oder dokumentiert.
- `02_external/upr-fvx` wurde nicht geaendert.
- Keine Original-Upstreams wurden kontaktiert.
