# 109 - CFRU/DPE Field Items API TM-slot Reload-Smoke

Datum: 2026-05-15

## Scope

- Repo: `Planton361/firered-gen9-randomizer-workspace`
- Branch: `test/upr-fvx-cfru-dpe-field-items-api-tm-slot-reload-smoke`
- UPR-FVX-Pin: `328e4441c2981d37aba9e2707a6f27f779b026e2`
- Feature: `FVX-ITEM-002 Field Items Random`
- Einstellung: `Settings.FieldItemsMod.RANDOM`
- `banBadRandomFieldItems=false`

Dieser Block prueft fachlich den UPR-FVX-Fix aus PR #37 fuer den CFRU/DPE Field-Items-API-TM-Slot-Scope. Es wurden keine Codeaenderungen und kein Submodule-Pin-Wechsel vorgenommen.

## Nicht-Ziele

- Keine Field Items Shuffle-Arbeit.
- Keine Random Even Distribution.
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

Dokumentiert werden nur aggregierte Zaehler und boolesche Ergebnisse. Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Map-Daten, Script-Bytes, Logauszuege und Output-ROM-Pfade wurden nicht dokumentiert.

Lokale Harness-, Log- und Output-Artefakte blieben ignored unter `05_builds/**` und wurden nicht committed.

## Ergebnis

Der Field-Items-only Write-/Reload-Smoke lief erfolgreich durch.

```text
candidateFilesChecked=95
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
exceptionClass=none
stacktrace=none
```

## Bewertung

- Der PR-#37-Fix ist im getesteten CFRU/DPE Gen9-BPRE Field-Items-Random-Scope fachlich bestaetigt.
- `Gen3RomHandler.getFieldItems()` / `setFieldItems(...)` sehen im CFRU/DPE-Gate die `28` Field-TM-Slots; Raw- und API-Sicht bleiben ausgerichtet.
- `randomizeTMFieldItems(...)` sieht `randomTmNeededSlots=28` und `randomTmCurrentSlots=28`.
- Required Field TMs bleiben vollstaendig erhalten: `randomTmRequiredMissingAfter=0` und `requiredFieldTMMissingAfter=0`.
- Der TM-Filler-Pool ist ausreichend und eindeutig: `randomTmFillerNeeded=4`, `randomTmFillerAvailable=26`, `randomTmPoolDeficit=0`, `randomTmDuplicateSelections=0`, `randomTmResultUniqueSize=28`.
- `apiTmFieldSlotWrites=27` ist der eng freigegebene Field-TM-Slot-Schreibumfang. Er wird getrennt von disallowed non-TM Slots bewertet.
- Preserve-/Skip-Zaehler fuer disallowed, invalid, unloaded, fallback, placeholder und progression-sensitive Slots bleiben stabil.
- Shops, Pickup und Held-Item-Scope wurden nicht veraendert.

## Feature-Status

- `FVX-ITEM-001 Field Items Shuffle`: bleibt `GUI-kompatibel` im getesteten allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random`: wird im engen Field-Items-only Scope mit `banBadRandomFieldItems=false` als `GUI-kompatibel` bewertet.
- `FVX-ITEM-003 Field Items Random even distribution`: bleibt `Write modelliert`; separater Smoke noetig.
- `FVX-ITEM-004 Field Items Ban Bad Items`: bleibt `Write modelliert`; separater Smoke/Fix-Scope noetig.

## Preserve-/Skip-Policy

- Write nur ueber den Field-Items-API-Scope.
- CFRU/DPE Field-TM-Slots sind eng zusaetzlich sichtbar.
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

Naechster enger Block: `test/upr-fvx-cfru-dpe-field-items-random-even-reload-smoke` fuer `FVX-ITEM-003 Field Items Random even distribution`, ohne Ban Bad Items und mit denselben Field-Items-only Preserve-/Reload-Kriterien.
