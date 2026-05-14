# 111 - CFRU/DPE Field Items Ban Bad Scope Plan

Datum: 2026-05-15

## Scope

- Repo: `Planton361/firered-gen9-randomizer-workspace`
- Branch: `analysis/upr-fvx-cfru-dpe-field-items-ban-bad-scope-plan`
- UPR-FVX-Pin: `328e4441c2981d37aba9e2707a6f27f779b026e2`
- Feature: `FVX-ITEM-004 Field Items Ban Bad Items`
- Modus: read-only Planung, keine Codeaenderung, kein Randomizer-Lauf, kein Build

Dieser Block plant, wie `FVX-ITEM-004` im CFRU/DPE Gen9-BPRE Field-Items-Scope getestet oder bei Bedarf gefixt werden soll. Shops, Pickup, Held Items, TM/HM/Tutor/Learnset und Scriptparser bleiben ausserhalb des Scopes.

## Gelesene Grundlagen

- Diagnose 100: Field-Items-Kandidatendiagnose mit `fieldItemsTotal=339`, `allowedFieldItemSlots=280`, `disallowedFieldItemSlots=59`, `tmFieldItemSlots=28`, `requiredFieldTMMissing=0`, `badFieldItems=75`, `badItemBanCandidates=75`.
- Diagnose 109: `FVX-ITEM-002 Field Items Random` ist mit `banBadRandomFieldItems=false` stabil und `GUI-kompatibel` im engen Field-Items-only Scope.
- Diagnose 110: `FVX-ITEM-003 Field Items Random even distribution` ist mit `banBadRandomFieldItems=false` stabil und `GUI-kompatibel` im engen Field-Items-only Scope.
- UPR-FVX-Codepfad: `GameRandomizer.maybeRandomizeFieldItems()` ruft fuer `SHUFFLE`, `RANDOM` und `RANDOM_EVEN` `ItemRandomizer.randomizeFieldItems()` auf.
- UPR-FVX-Codepfad: `ItemRandomizer.randomizeFieldItems()` trennt aktuelle API-Field-Items in TM- und Non-TM-Stacks und kombiniert spaeter positionsgleich wieder.
- UPR-FVX-Codepfad: `ItemRandomizer.randomizeTMFieldItems(...)` nutzt Required Field TMs und einen deduplizierten TM-Filler-Pool. Dieser Pfad liest `banBadRandomFieldItems` nicht.
- UPR-FVX-Codepfad: `ItemRandomizer.randomizeNonTMFieldItems(...)` waehlt bei `banBadRandomFieldItems=true` `romHandler.getNonBadItems()`, sonst `romHandler.getAllowedItems()`, entfernt danach TMs und randomisiert nur Non-TM-Slots.
- UPR-FVX-Codepfad: `AbstractRomHandler.getNonBadItems()` ist `getAllowedItems().stream().filter(item -> !item.isBad())`.
- UPR-FVX-Codepfad: `Gen3RomHandler.getFieldItems()` / `setFieldItems(...)` exponiert im CFRU/DPE-Gate allowed Slots plus Field-TM-Slots, ohne TMs global allowed zu setzen.

## Ban-Bad-Scope-Einschaetzung

`FVX-ITEM-004` ist kein eigener Writer. Es ist ein Pool-Filter fuer Field Items Random / Random Even.

Konkrete Wirkung:

- Ban Bad betrifft den Non-TM-Pool in `randomizeNonTMFieldItems(...)`.
- Ban Bad betrifft nicht den TM-Pool in `randomizeTMFieldItems(...)`.
- Required Field TMs sind durch Ban Bad nicht direkt gefaehrdet, weil sie im separaten TM-Pfad vor den Non-TM-Pools behandelt werden.
- Indirekt muessen Required Field TMs trotzdem im Smoke erneut geprueft werden, weil `setFieldItems(...)` die kombinierten TM-/Non-TM-Listen schreibt.
- Der bekannte CFRU/DPE-Diagnosewert fuer Ban-Bad-Kandidaten ist `75` (`badFieldItems=75`, `badItemBanCandidates=75`).
- Der bestehende API-TM-Slot-Fix bleibt Voraussetzung, damit TM-Slots sichtbar bleiben und nicht mit Non-TM-Slots vermischt werden.

## Empfohlene erste Smoke-Reihenfolge

1. `test/upr-fvx-cfru-dpe-field-items-random-ban-bad-reload-smoke`
2. Scope: `FVX-ITEM-002 Field Items Random` mit `Settings.FieldItemsMod.RANDOM` und `banBadRandomFieldItems=true`.
3. Ziel: belegen, dass Ban Bad den Non-TM-Pool filtert, ohne TM-Slots, Required Field TMs oder preserve-only Slots zu verletzen.
4. Danach separat: `test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke` fuer `FVX-ITEM-003` mit `RANDOM_EVEN` und `banBadRandomFieldItems=true`.
5. `FVX-ITEM-004` sollte erst nach beiden Smokes als umfassend GUI-kompatibel fuer Random und Random Even bewertet werden. Nach dem ersten Smoke ist nur die `RANDOM + Ban Bad` Kombination getestet.

Begruendung:

- `RANDOM` und `RANDOM_EVEN` nutzen denselben Ban-Bad-Non-TM-Pool, aber unterschiedliche Auswahlalgorithmen.
- Der erste Smoke sollte die einfachere `RANDOM`-Auswahl pruefen und keine Random-Even-Verteilung gleichzeitig bewerten.
- Random Even kann danach dieselben Pool- und Preserve-Kriterien mit zusaetzlicher Verteilungs-/Queue-Stabilitaet pruefen.

## Preserve-/Skip-Policy

Unveraendert aus Diagnosen 101, 109 und 110:

- Write nur ueber den Field-Items-API-Scope.
- CFRU/DPE Field-TM-Slots bleiben eng sichtbar.
- TMs werden nicht global allowed gesetzt.
- TM-Slots bleiben TM-Slots.
- Non-TM-Slots bleiben Non-TM-Slots.
- Required Field TMs bleiben vollstaendig.
- Preserve-only bleiben:
  - disallowed non-TM Field-Item-Slots
  - progression/key/system Slots
  - invalid/unloaded/fallback/placeholder Slots
  - `scriptPatternUnmatchedItemBalls=10`
  - nicht erkannte Script-/Map-Strukturen
- Ban Bad darf nur die Auswahl aus dem Non-TM-Random-Pool veraendern.
- Ban Bad darf keine Field-Item-Slots erweitern und keine Scriptparser-Erkennung veraendern.
- Shops, Pickup und Held Items bleiben ausserhalb dieses Scopes.

## Risiken

- Moderne Items koennen loaded und allowed sein, muessen aber weiterhin anhand `Item.isBad()` gefiltert werden, wenn Ban Bad aktiv ist.
- Fallback-, Placeholder-, invalid- und unloaded Items duerfen weder als Pool-Filler noch als Write-Ziel auftauchen.
- Key-/System-/Progression-Items duerfen nicht durch Ban-Bad-Poollogik in disallowed Slots geschrieben werden.
- `getNonBadItems()` filtert aus `getAllowedItems()`, nicht aus der CFRU/DPE-erweiterten Field-TM-Slot-Sicht; das ist fuer Non-TM-Ban-Bad korrekt, darf aber nicht als TM-Allowed-Policy missverstanden werden.
- Bad-Item-Erkennung ist global am `Item`-Flag modelliert; ein spaeterer Smoke muss zaehlen, ob noch `badFieldItemWrites` in Non-TM-Slots auftreten.
- Random Even muss separat geprueft werden, weil der Queue-/Refill-Algorithmus bei reduziertem Non-Bad-Pool eigene Risiken hat.

## Spaetere Smoke-/Reload-Kriterien

Pflicht fuer den ersten `RANDOM + banBadRandomFieldItems=true` Smoke:

```text
candidateLoaded=true
smokeExecuted=true
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
reloadSuccessful=true
fieldItemsTotalBefore=339
fieldItemsTotalAfter=339
fieldItemsTotalReload=339
fieldItemReloadMismatches=0
visibleFieldItemReloadMismatches=0
hiddenFieldItemReloadMismatches=0
tmFieldItemSlotMismatches=0
nonTmFieldItemSlotMismatches=0
requiredFieldTMMissingAfter=0
requiredItemPolicyViolations=0
progressionItemPolicyViolations=0
invalidFieldItemWrites=0
unloadedFieldItemWrites=0
fallbackFieldItemWrites=0
placeholderFieldItemWrites=0
disallowedFieldItemWrites=0, ausser eng separat als apiTmFieldSlotWrites
scriptPatternExpansion=0
badFieldItemWrites=0
badFieldItemPoolCandidates=75
badFieldItemPoolExcluded=75
nonBadFieldItemPoolSize > 0
randomTmNeededSlots=28
randomTmCurrentSlots=28
randomTmRequiredTotal=24
randomTmRequiredPresent=24
randomTmRequiredMissingBefore=0
randomTmRequiredMissingAfter=0
randomTmLoadedPoolSize=50
randomTmUniquePoolSize >= 28
randomTmFillerNeeded=4
randomTmFillerAvailable >= 4
randomTmDuplicateSelections=0
randomTmPoolDeficit=0
randomTmResultSize=28
randomTmResultUniqueSize=28
apiTmFieldItemSlots=28
rawTmFieldItemSlots=28
rawApiTmSlotAlignmentMismatches=0
tmGloballyAllowedChanged=false
shopItemScopeChanged=false
pickupItemScopeChanged=false
heldItemScopeChanged=false
exceptionClass=none
stacktrace=none
```

Zusaetzlich fuer den spaeteren `RANDOM_EVEN + banBadRandomFieldItems=true` Smoke:

```text
randomEvenQueueUsed=true
randomEvenTmDistributionStable=true
randomEvenNonTmDistributionStable=true
nonBadFieldItemQueueRefills >= 0
badFieldItemWrites=0
```

## Feature-Status-Empfehlung

- `FVX-ITEM-001` bleibt `GUI-kompatibel` im getesteten Shuffle-Scope.
- `FVX-ITEM-002` bleibt `GUI-kompatibel` im getesteten Random-Scope mit `banBadRandomFieldItems=false`.
- `FVX-ITEM-003` bleibt `GUI-kompatibel` im getesteten Random-Even-Scope mit `banBadRandomFieldItems=false`.
- `FVX-ITEM-004` bleibt bis mindestens zum ersten `RANDOM + banBadRandomFieldItems=true` Smoke `Write modelliert`.
- Nach erfolgreichem ersten Smoke kann `FVX-ITEM-004` als getestet fuer `FieldItemsMod.RANDOM` notiert werden, aber noch nicht fuer `RANDOM_EVEN`.
- Keine Hochstufung fuer Shops, Pickup, Encounter Held Items, Trainer Held Items oder Starter Held Items.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-field-items-random-ban-bad-reload-smoke`: sanitisierten Field-Items-only Write-/Reload-Smoke fuer `FVX-ITEM-002 Field Items Random` mit `banBadRandomFieldItems=true` ausfuehren, ohne Random Even, Shops, Pickup, Held Items oder Scriptparser-Arbeit.
