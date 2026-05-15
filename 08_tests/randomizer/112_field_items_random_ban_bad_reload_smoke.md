# 112 - CFRU/DPE Field Items Random Ban Bad Reload Smoke

Datum: 2026-05-15

## Scope

- Repo: `Planton361/firered-gen9-randomizer-workspace`
- Branch: `test/upr-fvx-cfru-dpe-field-items-random-ban-bad-reload-smoke`
- UPR-FVX-Pin: `328e4441c2981d37aba9e2707a6f27f779b026e2`
- Feature: `FVX-ITEM-002 Field Items Random` mit `banBadRandomFieldItems=true`
- Bewerteter Ban-Bad-Teil: `FVX-ITEM-004 Field Items Ban Bad Items` fuer `FieldItemsMod.RANDOM`

Dieser Smoke prueft nur den Field-Items-only Write-/Reload-Pfad fuer `Settings.FieldItemsMod.RANDOM` mit aktivem Ban-Bad-Filter. Random Even + Ban Bad, Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer/Wild/Evolution, Text/Menu und Scriptparser bleiben ausserhalb des Scopes.

## Sicherheits- und Sanitizing-Grenzen

- Es wurden nur aggregierte Zaehler und boolesche Ergebnisse dokumentiert.
- Keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Map-Daten, Script-Bytes oder Logauszuege werden dokumentiert.
- Lokaler Harness, Output-ROM und Logs bleiben ignored unter `05_builds/**`.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein Submodule-Pin-Wechsel und kein Build.

## Ergebnis

```text
candidateFilesChecked=9
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
disallowedFieldItemWrites=0
apiTmFieldSlotWrites=27
scriptPatternExpansion=0
badFieldItemWrites=0
badFieldItemPoolCandidates=47
badFieldItemPoolExcluded=47
nonBadFieldItemPoolSize=485
randomTmNeededSlots=28
randomTmCurrentSlots=28
randomTmRequiredTotal=24
randomTmRequiredPresent=24
randomTmRequiredMissingBefore=0
randomTmRequiredMissingAfter=0
randomTmLoadedPoolSize=50
randomTmAllowedPoolSize=0
randomTmUniquePoolSize=50
randomTmFillerNeeded=4
randomTmFillerAvailable=26
randomTmDuplicateSelections=0
randomTmPoolDeficit=0
randomTmResultSize=28
randomTmResultUniqueSize=28
apiFieldItemsTotal=308
apiTmFieldItemSlots=28
apiNonTmFieldItemSlots=280
rawTmFieldItemSlots=28
rawApiTmSlotAlignmentMismatches=0
tmGloballyAllowedChanged=false
shopItemScopeChanged=false
pickupItemScopeChanged=false
heldItemScopeChanged=false
exceptionClass=none
stacktrace=none
```

## Bewertung

Der Write-/Reload-Smoke ist fachlich stabil:

- Save, Log, Output und Reload waren erfolgreich.
- Field-Items-Anzahl bleibt stabil bei `339`.
- Reload-Mismatches bleiben `0` fuer Gesamt-, sichtbare und Hidden-Field-Items.
- TM-/Non-TM-Slottypen bleiben stabil.
- Required Field TMs bleiben vollstaendig.
- Keine invaliden, unloaded, fallback, placeholder oder disallowed Non-TM-Field-Item-Writes wurden beobachtet.
- Ban Bad erzeugt keine Bad-Item-Writes: `badFieldItemWrites=0`.
- Der TM-Pool bleibt stabil: `randomTmNeededSlots=28`, `randomTmRequiredTotal=24`, `randomTmFillerNeeded=4`, `randomTmPoolDeficit=0`, `randomTmResultUniqueSize=28`.
- TMs wurden nicht global allowed gesetzt, und Shop-, Pickup- sowie Held-Item-Scope blieben unveraendert.

Konservative Einschraenkung:

- Diagnose 111 erwartete fuer den ersten Ban-Bad-Smoke `badFieldItemPoolCandidates=75` und `badFieldItemPoolExcluded=75` aus der frueheren Field-Items-Diagnosebasis.
- Der lokale Smoke-Zaehler fuer diesen Lauf fand im geladenen fachlichen Kandidaten `badFieldItemPoolCandidates=47` und `badFieldItemPoolExcluded=47`.
- Da der Write-/Reload-Pfad trotzdem `badFieldItemWrites=0` und alle Preserve-/Reload-Zielwerte erreicht, ist der Ban-Bad-Filter fuer `FieldItemsMod.RANDOM` funktional belegt, aber die 75er-Baseline aus Diagnose 111 wird nicht als reproduziert behauptet.

## Preserve-/Skip-Policy

- Write nur ueber den Field-Items-API-Scope.
- CFRU/DPE Field-TM-Slots bleiben eng sichtbar.
- TMs werden nicht global allowed gesetzt.
- TM-Slots bleiben TM-Slots.
- Non-TM-Slots bleiben Non-TM-Slots.
- Required Field TMs bleiben vollstaendig.
- Ban Bad veraendert nur die Auswahl aus dem Non-TM-Random-Pool.
- Preserve-only bleiben:
  - disallowed non-TM Field-Item-Slots
  - progression/key/system Slots
  - invalid/unloaded/fallback/placeholder Slots
  - `scriptPatternUnmatchedItemBalls=10`
  - nicht erkannte Script-/Map-Strukturen
- Shops, Pickup und Held Items bleiben ausserhalb dieses Scopes.

## Feature-Status

- `FVX-ITEM-001 Field Items Shuffle` bleibt `GUI-kompatibel` im getesteten allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random` bleibt `GUI-kompatibel` im engen Field-Items-Random-Scope; dieser Lauf bestaetigt zusaetzlich `banBadRandomFieldItems=true` fuer `FieldItemsMod.RANDOM`.
- `FVX-ITEM-003 Field Items Random even distribution` bleibt `GUI-kompatibel` nur fuer `banBadRandomFieldItems=false`.
- `FVX-ITEM-004 Field Items Ban Bad Items` ist fuer `FieldItemsMod.RANDOM` getestet, aber noch nicht vollstaendig GUI-kompatibel, weil Random Even + Ban Bad separat aussteht und die 75er-Baseline aus Diagnose 111 in diesem Lauf nicht reproduziert wurde.
- Shops, Pickup und Held Items werden nicht hochgestuft.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke`: denselben Field-Items-only Ban-Bad-Smoke fuer `Settings.FieldItemsMod.RANDOM_EVEN` ausfuehren und Random-Even-Queue-/Verteilungsstabilitaet separat bewerten.
