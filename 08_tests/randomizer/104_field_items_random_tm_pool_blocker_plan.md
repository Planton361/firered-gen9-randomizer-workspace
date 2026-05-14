# 104 - CFRU/DPE Field Items Random TM-pool Blocker Plan

Datum: 2026-05-15

Branch: `analysis/upr-fvx-cfru-dpe-field-items-random-tm-pool-blocker-plan`

## Ziel

Dieser read-only Plan untersucht, warum `FVX-ITEM-002 Field Items Random` im Field-Items-Random-TM-Pool mit `RandomizationException` blockiert.

Keine Codeaenderung, kein Randomizer-Lauf, kein Build, kein Fix, keine Aenderung an `02_external/**` und keine Submodule-Pin-Aenderung wurden vorgenommen.

## Ausgangsbasis

- Workspace PR #148 (`docs: record field items random smoke`) wurde vor Branch-Erstellung als gemerged verifiziert.
- Branch wurde von aktuellem `origin/main` erstellt.
- UPR-FVX bleibt auf `2697511da9a97df4c29c00dfda8b40e556020489` gepinnt.
- Diagnose 102 bestaetigt `FVX-ITEM-001 Field Items Shuffle` als `GUI-kompatibel` im engen allowed-slot Scope.
- Diagnose 103 blockiert `FVX-ITEM-002 Field Items Random` mit `RandomizationException` vor Output/Reload.

Relevante Diagnose-103-Werte:

- `candidateLoaded=true`
- `smokeExecuted=true`
- `saveSuccessful=false`
- `outputRomExists=false`
- `reloadSuccessful=false`
- `fieldItemsTotalBefore=339`
- `fieldItemsTotalAfter=339`
- `requiredFieldTMMissingAfter=0`
- `disallowedFieldItemWrites=0`
- `scriptPatternExpansion=0`
- `badFieldItemWrites=0`
- `exceptionClass=com.uprfvx.random.exceptions.RandomizationException`

Relevante Diagnose-100-Werte:

- `fieldItemsTotal=339`
- `allowedFieldItemSlots=280`
- `disallowedFieldItemSlots=59`
- `tmFieldItemSlots=28`
- `nonTmFieldItemSlots=311`
- `requiredFieldTMsTotal=24`
- `requiredFieldTMPresent=24`
- `requiredFieldTMMissing=0`
- `scriptPatternUnmatchedItemBalls=10`

## Gelesene Codepfade

Read-only geprueft wurden:

- `GameRandomizer.maybeRandomizeFieldItems()`
- `Settings.FieldItemsMod.RANDOM`
- `Settings.banBadRandomFieldItems`
- `ItemRandomizer.randomizeFieldItems()`
- `ItemRandomizer.randomizeTMFieldItems(...)`
- `ItemRandomizer.randomizeNonTMFieldItems(...)`
- `Gen3RomHandler.getRequiredFieldTMs()`
- `Gen3RomHandler.getFieldItems()`
- `Gen3RomHandler.setFieldItems(...)`
- `AbstractRomHandler.checkFieldItemsTMsReplaceTMs(...)`
- `RomHandler.getFieldItems()` / `setFieldItems(...)` API-Vertrag
- `Gen3Constants.frlgRequiredFieldTMs`
- `Gen3Constants.tmCount`
- vorhandene `ItemRandomizerTest`-Abdeckung

## Blocker-Einschaetzung

`ItemRandomizer.randomizeTMFieldItems(...)` ist der einzige eng gefundene Field-Items-spezifische `RandomizationException`-Wurf in diesem Pfad.

Der relevante Algorithmus:

- `randomizeFieldItems()` liest `romHandler.getFieldItems()` und trennt die allowed Field Items in TM- und Non-TM-Stacks.
- Bei `FieldItemsMod.RANDOM` und `RANDOM_EVEN` werden zuerst `randomizeTMFieldItems(tms)` und danach `randomizeNonTMFieldItems(nonTMs)` ausgefuehrt.
- `randomizeTMFieldItems(...)` baut `allTMs` aus allen geladenen Items mit `Item::isTM`.
- `requiredTMs` kommt aus `romHandler.getRequiredFieldTMs()`.
- `neededTMAmount = tms.size()` entspricht der Anzahl aktueller allowed TM-Field-Item-Slots.
- `newTMs` startet als Set aus `requiredTMs`.
- Danach werden zufaellige TMs aus `allTMs` ergaenzt, bis `newTMs.size() == neededTMAmount` oder `newTMs.size() >= allTMs.size()`.
- Wenn `newTMs.size() != neededTMAmount`, wird `RandomizationException("Could not randomize TM field items, too many TMs requested.")` geworfen.

Fuer den getesteten CFRU/DPE Gen9-BPRE-Stand ist die kritische Konstellation:

- `tmFieldItemSlots=28`
- `requiredFieldTMsTotal=24`
- `requiredFieldTMPresent=24`
- `requiredFieldTMMissing=0`

Damit braucht der Random-TM-Pfad exakt 28 eindeutige TM-Items, muss aber zwingend die 24 required Field TMs einbauen. Der Blocker ist daher sehr wahrscheinlich ein Pool-Size-/Required-TM-/Duplicate-/Selection-Problem im TM-Field-Items-Random-Pfad, nicht ein Fehler im allowed-slot Preserve-Guard.

Wichtige Abgrenzung:

- `Gen3Constants.tmCount=50` und der klassische Gen3-Code markiert `TM01..TM50` als TM.
- Fuer CFRU/DPE koennen Item-Load-, Allowed-/Banned- und Required-TM-Policy trotzdem dazu fuehren, dass der effektiv verwendbare Random-TM-Pool nicht sauber zum required-plus-needed-Vertrag passt.
- Diagnose 103 dokumentiert nur die Exception-Klasse, keine privaten Logdetails. Ein spaeterer Fixblock sollte den TM-Pool nur sanitisiert mit aggregierten Zaehlern instrumentieren.

## Mögliche Fix-Optionen

Option A: enger Required-TM-Clamp fuer Field-Items-Random

- Wenn `requiredTMs.size() > neededTMAmount`, waehle nur required TMs, die bereits im Field-Item-Scope vorkommen, oder waehle eine deterministische Teilmenge.
- Vorteil: verhindert den offensichtlichen Set-Size-Overflow.
- Risiko: kann Required-TM-Verfuegbarkeit verletzen, wenn ein required TM dadurch nicht mehr als Field Item auftaucht.
- Bewertung: nur zulassen, wenn Reload-Kriterium `requiredFieldTMMissingAfter=0` belegbar bleibt.

Option B: TM-Pool-Fallback auf aktuelle Field-TM-Slots plus Required-TMs

- Baue den Random-TM-Pool aus aktuellen Field-TM-Slots und required TMs, nicht blind aus allen geladenen TMs.
- Vorteil: bleibt eng im Field-Items-Writer-Scope und vermeidet moderne/unsichere TM-Pool-Ausweitung.
- Risiko: Randomness begrenzt; kann bei nur 28 Slots wenig Variation liefern.
- Bewertung: reviewbar, wenn `tmFieldItemSlotMismatches=0` und `requiredFieldTMMissingAfter=0` stabil bleiben.

Option C: vorhandene 28 TM-Slots randomisieren, Required-TMs zuerst reservieren

- Reserviere required TMs, fuelle nur die verbleibenden `neededTMAmount - requiredTMs.size()` Slots aus einem validierten TM-Pool.
- Der Pool muss dedupliziert, geladen, `isTM`, nicht null und nicht unsicher/fallback sein.
- Vorteil: passt zum bestehenden Algorithmus, aber macht die Poolbildung expliziter.
- Risiko: wenn `requiredTMs.size()` groesser als `neededTMAmount` ist, bleibt der Blocker bestehen und muss explizit als nicht fixbar klassifiziert werden.
- Bewertung: wahrscheinlich bester erster Fix, falls die naechste Diagnose zeigt, dass genug valide Filler-TMs existieren.

Option D: Random-TM-Field-Items fuer CFRU/DPE vorerst konservativ auf Shuffle degradieren

- Im sicheren CFRU/DPE-Gate wuerde Random fuer TM-Field-Slots nur die vorhandenen TM-Field-Slots shufflen, Non-TMs aber randomisieren.
- Vorteil: maximal preserve-orientiert, keine Required-TM-Verletzung.
- Risiko: Semantik von `Random` ist fuer TM-Field-Items abgeschwaecht.
- Bewertung: nur als Fallback, wenn ein echter Random-TM-Pool nicht sicher belegbar ist.

Nicht empfohlen:

- TM/HM/Tutor/Learnset-Writer erweitern.
- Shops/Pickup/Held-Item-Pools einbeziehen.
- Required Field TMs ignorieren.
- Scriptparser erweitern.
- Disallowed/progression-sensitive Slots freigeben.

## Preserve-/Skip-Policy

Muss fuer jeden spaeteren Fix erhalten bleiben:

- Write nur ueber bestehenden allowed Field-Items-API-Scope.
- Preserve-only:
  - `disallowedFieldItemSlots=59`
  - progression/key/system Slots
  - invalid/unloaded/fallback/placeholder Slots
  - `scriptPatternUnmatchedItemBalls=10`
  - nicht erkannte Script-/Map-Strukturen
- TM-Slots bleiben TM-Slots.
- Non-TM-Slots bleiben Non-TM-Slots.
- Required Field TMs bleiben vollstaendig verfuegbar.
- Ban-Bad-Items bleibt fuer `FVX-ITEM-002` inaktiv.
- Keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung.

## Spaetere Fix-/Smoke-Kriterien

Ein spaeterer Fix- oder Smoke-Block fuer `FVX-ITEM-002` braucht mindestens:

- `candidateLoaded=true`
- `smokeExecuted=true`
- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- `reloadSuccessful=true`
- `fieldItemsTotalBefore=339`
- `fieldItemsTotalAfter=339`
- `fieldItemsTotalReload=339`
- `fieldItemReloadMismatches=0`
- `visibleFieldItemReloadMismatches=0`
- `hiddenFieldItemReloadMismatches=0`
- `tmFieldItemSlotMismatches=0`
- `nonTmFieldItemSlotMismatches=0`
- `requiredFieldTMMissingAfter=0`
- `requiredItemPolicyViolations=0`
- `progressionItemPolicyViolations=0`
- `invalidFieldItemWrites=0`
- `unloadedFieldItemWrites=0`
- `fallbackFieldItemWrites=0`
- `placeholderFieldItemWrites=0`
- `disallowedFieldItemWrites=0`
- `scriptPatternExpansion=0`
- `badFieldItemWrites=0` or `not evaluated` because `banBadRandomFieldItems=false`
- `randomTmNeededSlots=28`
- `randomTmRequiredTotal=24`
- `randomTmCandidatePoolSize >= 28`
- `randomTmPoolDeficit=0`
- `exceptionClass=none`
- `stacktrace=none`

Empfohlene zusaetzliche Diagnosemetriken fuer den Fixblock:

- `randomTmCurrentSlots`
- `randomTmRequiredPresent`
- `randomTmRequiredMissingBefore`
- `randomTmRequiredMissingAfter`
- `randomTmLoadedPoolSize`
- `randomTmAllowedPoolSize`
- `randomTmUniquePoolSize`
- `randomTmFillerNeeded`
- `randomTmFillerAvailable`
- `randomTmDuplicateSelections`
- `randomTmPoolDeficit`

## Empfehlung

Ein spaeterer Fix ist reviewbar, wenn er eng im `ItemRandomizer.randomizeTMFieldItems(...)`-Scope oder einem kleinen privaten Helper bleibt und nur `FVX-ITEM-002`/Field-Items-Random-TM-Pool betrifft.

Vor einem Codefix sollte ein separater Fixbranch die TM-Pool-Metriken sanitisiert erfassen und den kleinstmoeglichen Algorithmus waehlen. `FVX-ITEM-003 Random Even` und `FVX-ITEM-004 Ban Bad Items` bleiben danach separate Slices.

## Naechster minimaler Schritt

`compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix`

Ziel:

- Minimalen UPR-FVX-Fix fuer den Field-Items-Random-TM-Pool vorbereiten.
- Keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung.
- Danach sanitisierten `FVX-ITEM-002` Write-/Reload-Smoke wiederholen.
