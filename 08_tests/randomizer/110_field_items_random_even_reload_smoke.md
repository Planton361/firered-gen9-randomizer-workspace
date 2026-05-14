# 110 - CFRU/DPE Field Items Random Even Reload-Smoke

Datum: 2026-05-15

## Scope

- Repo: `Planton361/firered-gen9-randomizer-workspace`
- Branch: `test/upr-fvx-cfru-dpe-field-items-random-even-reload-smoke`
- UPR-FVX-Pin: `328e4441c2981d37aba9e2707a6f27f779b026e2`
- Feature: `FVX-ITEM-003 Field Items Random even distribution`
- Einstellung: `Settings.FieldItemsMod.RANDOM_EVEN`
- `banBadRandomFieldItems=false`

Dieser Block prueft ausschliesslich den Field-Items-only Random-Even-Write-/Reload-Scope. Es wurden keine Codeaenderungen und kein Submodule-Pin-Wechsel vorgenommen.

## Nicht-Ziele

- Keine Field Items Shuffle-Arbeit.
- Keine Field Items Random-Hochstufung erneut pruefen.
- Keine Ban-Bad-Items-Umsetzung.
- Keine Shops.
- Kein Pickup.
- Keine Encounter-, Trainer- oder Starter-Held-Items.
- Keine TM/HM/Tutor/Learnset-Ausweitung.
- Keine Palette-/Graphics-Arbeit.
- Keine MoveData-/MoveNames-Arbeit.
- Kein TypeChart / TypeEffectiveness.
- Keine Trainer-, Wild-, Evolution- oder Text/Menu-Arbeit.
- Keine Scriptparser-Erweiterung.

## Sanitizing

Dokumentiert werden nur aggregierte Zaehler, boolesche Ergebnisse und abgeleitete Scope-Bewertungen. Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Map-Daten, Script-Bytes, Logauszuege und Output-ROM-Pfade wurden nicht dokumentiert.

Lokale Harness-, Log- und Output-Artefakte blieben ignored unter `05_builds/**` und wurden nicht committed.

## Ergebnis

Der Field-Items-only `RANDOM_EVEN` Write-/Reload-Smoke lief erfolgreich durch.

```text
candidateFilesChecked=96
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
randomEvenQueueUsed=true (derived)
randomEvenTmDistributionStable=true (derived)
randomEvenNonTmDistributionStable=true (derived)
exceptionClass=none
stacktrace=none
```

## Bewertung

- `Settings.FieldItemsMod.RANDOM_EVEN` wurde als Field-Items-only Scope ausgefuehrt.
- Save, Log, Output und Reload sind erfolgreich.
- Field-Item-Gesamtzahl bleibt stabil: `339` vor Save, nach Save und nach Reload.
- Reload-Vergleich ist stabil: `fieldItemReloadMismatches=0`.
- Sichtbare und Hidden Field Items reloaden stabil.
- TM-/Non-TM-Slottypen bleiben stabil.
- Required Field TMs bleiben vollstaendig erhalten.
- API- und Raw-TM-Slot-Sicht bleiben ausgerichtet: `apiTmFieldItemSlots=28`, `rawTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`.
- Der TM-Pool bleibt stabil: `randomTmPoolDeficit=0`, `randomTmDuplicateSelections=0`, `randomTmResultUniqueSize=28`.
- `apiTmFieldSlotWrites=27` ist der eng freigegebene Field-TM-Slot-Schreibumfang. Er wird getrennt von disallowed non-TM Slots bewertet.
- Preserve-/Skip-Zaehler fuer disallowed, invalid, unloaded, fallback, placeholder und progression-sensitive Slots bleiben stabil.
- TMs wurden nicht global allowed gesetzt.
- Shops, Pickup und Held-Item-Scope wurden nicht veraendert.

## Feature-Status

- `FVX-ITEM-001 Field Items Shuffle`: bleibt `GUI-kompatibel` im getesteten allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random`: bleibt `GUI-kompatibel` im engen Field-Items-only Scope mit `banBadRandomFieldItems=false`.
- `FVX-ITEM-003 Field Items Random even distribution`: wird im engen Field-Items-only Scope mit `banBadRandomFieldItems=false` als `GUI-kompatibel` bewertet.
- `FVX-ITEM-004 Field Items Ban Bad Items`: bleibt `Write modelliert`; separater Smoke/Fix-Scope noetig.

## Preserve-/Skip-Policy

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
- Ban-Bad-Items bleibt inaktiv.
- Shops, Pickup und Held Items bleiben ausserhalb dieses Scopes.

## Naechster minimaler Schritt

Naechster enger Block: `analysis/upr-fvx-cfru-dpe-field-items-ban-bad-scope-plan` fuer `FVX-ITEM-004 Field Items Ban Bad Items`, bevor Ban-Bad-Items in einem Write-/Reload-Smoke aktiviert wird.
