# 105 - CFRU/DPE Field Items Random TM-pool Fix

Datum: 2026-05-15

Workspace-Branch: `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix`

UPR-FVX-Commit: `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd`

UPR-FVX PR: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/36>

## Ziel

Enger Fix fuer den `FVX-ITEM-002 Field Items Random` TM-Field-Items-Pool-Blocker aus Diagnose 103/104.

Scope bleibt Field-Items-only:

- `Settings.FieldItemsMod.RANDOM`
- `banBadRandomFieldItems=false`
- TM-Field-Items-Random-Pool
- kein `FVX-ITEM-003 Random Even`
- kein `FVX-ITEM-004 Ban Bad Items`
- keine Shops
- kein Pickup
- keine Encounter-/Trainer-/Starter-Held-Items
- keine TM/HM/Tutor/Learnset-Writer-Ausweitung
- keine Scriptparser-Erweiterung

## Ausgangsbefund

Diagnose 103 blockierte `FVX-ITEM-002 Field Items Random` mit `RandomizationException` vor Output/Reload.

Sanitisierte Ausgangswerte aus den vorherigen Diagnosen:

- `fieldItemsTotalBefore=339`
- `fieldItemsTotalAfter=339`
- `tmFieldItemSlots=28`
- `nonTmFieldItemSlots=311`
- `requiredFieldTMsTotal=24`
- `requiredFieldTMPresent=24`
- `requiredFieldTMMissing=0`
- `disallowedFieldItemSlots=59`
- `scriptPatternUnmatchedItemBalls=10`

Diagnose 104 grenzte den Fehler auf `ItemRandomizer.randomizeTMFieldItems(...)` ein.

## Fix-Entscheidung

Der Fix bleibt auf `random/src/main/java/com/uprfvx/random/randomizers/ItemRandomizer.java` begrenzt.

Geaendert wurde nur der TM-Field-Items-Random-Pool:

- `neededTMAmount = tms.size()` bleibt die Zielgroesse.
- Required Field TMs aus `romHandler.getRequiredFieldTMs()` bleiben Pflicht.
- Wenn mehr Required TMs als TM-Field-Item-Slots vorhanden sind, bricht der Randomizer weiterhin sauber mit `RandomizationException` ab.
- Filler-TMs werden dedupliziert aufgebaut.
- Filler-TMs kommen aus geladenen TM-Items und den aktuellen Field-TM-Slots.
- `null`, Nicht-TMs, Required-Duplikate und weitere Duplikate werden ausgeschlossen.
- Der Filler-Pool wird gemischt und exakt auf `neededTMAmount - requiredTMs.size()` aufgefuellt.
- Bei Pooldefizit bleibt eine klare `RandomizationException` erhalten.
- TM-Slots bleiben TM-Slots; Non-TM-Slots bleiben Non-TM-Slots.

Damit bleibt der Fix eng und behebt den konkreten Pool-/Required-TM-/Unique-Selection-Pfad, ohne den Field-Item-Writer oder Script-/Map-Erkennung zu erweitern.

## Sanitisierte Fix-Metriken

Der Fix ist so ausgelegt, dass ein spaeterer ROM-Smoke folgende Metriken auswerten kann:

- `randomTmNeededSlots=28`
- `randomTmCurrentSlots=28`
- `randomTmRequiredTotal=24`
- `randomTmRequiredPresent=24`
- `randomTmRequiredMissingBefore=0`
- `randomTmRequiredMissingAfter=0`
- `randomTmLoadedPoolSize` dokumentieren
- `randomTmAllowedPoolSize` dokumentieren, falls der Harness diese Kategorie trennt
- `randomTmUniquePoolSize >= 28`
- `randomTmFillerNeeded=4`
- `randomTmFillerAvailable >= 4`
- `randomTmDuplicateSelections=0` im Ergebnis
- `randomTmPoolDeficit=0`
- `randomTmResultSize=28`
- `randomTmResultUniqueSize=28`

## Smoke-/Reload-Ergebnis

In diesem Arbeitsblock wurde kein fachlicher ROM-Write-/Reload-Smoke ausgefuehrt.

Grund:

- Der UPR-FVX-Codefix wurde vorbereitet und gepusht.
- Es wurde kein konkreter lokaler Smoke-Harness oder Kandidatenaufruf verwendet, der ohne private Pfad-/Artefaktberuehrung in diesem Chat sicher ausgefuehrt werden konnte.
- Keine ROMs, Output-ROMs, Logs, Pointer, Offsets, Raw-Map-Daten oder privaten Pfade wurden dokumentiert.

Status der fachlichen Smoke-Metriken in diesem Block:

- `candidateLoaded=not evaluated`
- `smokeExecuted=false`
- `saveSuccessful=not evaluated`
- `logSuccessful=not evaluated`
- `outputRomExists=not evaluated`
- `logNonEmpty=not evaluated`
- `reloadSuccessful=not evaluated`
- `fieldItemsTotalBefore=not evaluated`
- `fieldItemsTotalAfter=not evaluated`
- `fieldItemsTotalReload=not evaluated`
- `fieldItemReloadMismatches=not evaluated`
- `visibleFieldItemReloadMismatches=not evaluated`
- `hiddenFieldItemReloadMismatches=not evaluated`
- `tmFieldItemSlotMismatches=not evaluated`
- `nonTmFieldItemSlotMismatches=not evaluated`
- `requiredFieldTMMissingAfter=not evaluated`
- `requiredItemPolicyViolations=not evaluated`
- `progressionItemPolicyViolations=not evaluated`
- `invalidFieldItemWrites=not evaluated`
- `unloadedFieldItemWrites=not evaluated`
- `fallbackFieldItemWrites=not evaluated`
- `placeholderFieldItemWrites=not evaluated`
- `disallowedFieldItemWrites=not evaluated`
- `scriptPatternExpansion=not evaluated`
- `badFieldItemWrites=not evaluated`
- `exceptionClass=none`
- `stacktrace=none`

## UPR-FVX Checks

- `git status --short`: nur erwartete Codeaenderung vor Commit; sauber nach Commit.
- `git diff --stat`: `ItemRandomizer.java` only.
- `git diff --check`: sauber.
- `./gradlew :random:test --tests com.uprfvx.random.randomizers.ItemRandomizerTest`: `:random:compileJava` erfolgreich; Gradle bricht mit `No tests found for given includes` ab.
- `./gradlew test --tests '*ItemRandomizerTest'`: Compile-/Jar-Schritte erfolgreich; Gradle bricht mit `No tests found for given includes` im Root-/devtools-Testfilter ab.

Die Gradle-Ergebnisse belegen einen Compile-Durchlauf des geaenderten `random`-Moduls, aber keinen erfolgreich ausgefuehrten Testfall.

## Preserve-/Skip-Policy

Unveraendert aus Diagnose 101/102/103/104:

- Write nur ueber den bestehenden allowed Field-Items-API-Scope.
- Preserve-only: `disallowedFieldItemSlots=59`.
- Preserve-only: progression/key/system Slots.
- Preserve-only: invalid/unloaded/fallback/placeholder Slots.
- Preserve-only: `scriptPatternUnmatchedItemBalls=10`.
- Preserve-only: nicht erkannte Script-/Map-Strukturen.
- TM-Slots bleiben TM-Slots.
- Non-TM-Slots bleiben Non-TM-Slots.
- Required Field TMs muessen vollstaendig bleiben.
- Ban-Bad-Items bleibt inaktiv.

## Feature-Status

- `FVX-ITEM-001 Field Items Shuffle`: bleibt `GUI-kompatibel` im engen allowed-slot Scope aus Diagnose 102.
- `FVX-ITEM-002 Field Items Random`: Fix vorbereitet, aber ohne fachlichen ROM-Reload-Smoke noch nicht hochgestuft.
- `FVX-ITEM-003 Field Items Random even distribution`: bleibt `Write modelliert`.
- `FVX-ITEM-004 Field Items Ban Bad Items`: bleibt `Write modelliert`.

## Naechster Schritt

Nach Merge von UPR-FVX PR #36 und Workspace-PR zu diesem Protokoll:

- `test/upr-fvx-cfru-dpe-field-items-random-tm-pool-reload-smoke`

Ziel:

- `FVX-ITEM-002 Field Items Random` mit `banBadRandomFieldItems=false` erneut fachlich als Field-Items-only Write-/Reload-Smoke ausfuehren.
- Erwartet: `saveSuccessful=true`, `reloadSuccessful=true`, `fieldItemReloadMismatches=0`, `requiredFieldTMMissingAfter=0`, `randomTmPoolDeficit=0`, `randomTmResultSize=28`, `randomTmResultUniqueSize=28`.
