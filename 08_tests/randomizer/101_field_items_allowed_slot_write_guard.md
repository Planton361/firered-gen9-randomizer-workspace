# 101 - CFRU/DPE Field Items Allowed-slot Write Guard

Datum: 2026-05-14

Branch: `compat/upr-fvx-cfru-dpe-field-items-allowed-slot-write-guard`

## Ziel

Dieser Block bewertet den engen Field-Items-only Writer-Scope fuer `FVX-ITEM-001..004` im CFRU/DPE Gen9-BPRE-Stand. Der Fokus liegt auf dem allowed-slot Guard fuer Field Items und auf einem spaeteren sanitisierten Write-/Reload-Smoke.

Nicht enthalten sind Shops, Pickup, Encounter Held Items, Trainer Held Items, Starter Held Items, TM/HM/Tutor/Learnset-Writer, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer, Wild, Evolution und Text/Menu.

## Ausgangsbasis

- Workspace PR #145 (`docs: record field items candidate diagnostics`) wurde vor Branch-Erstellung als gemerged verifiziert.
- Branch wurde von aktuellem `origin/main` erstellt.
- UPR-FVX bleibt im Workspace auf `2697511da9a97df4c29c00dfda8b40e556020489` gepinnt.
- Diagnose 100 ist die aktuelle Field-Items-Datenbasis.

Sanitisierte Diagnose-100-Kernwerte:

- `candidateFilesChecked=94`
- `candidateLoaded=true`
- `fieldItemScanSuccessful=true`
- `fieldItemsTotal=339`
- `visibleFieldItemSlots=168`
- `hiddenFieldItemSlots=171`
- `allowedFieldItemSlots=280`
- `disallowedFieldItemSlots=59`
- `tmFieldItemSlots=28`
- `nonTmFieldItemSlots=311`
- `requiredFieldTMsTotal=24`
- `requiredFieldTMPresent=24`
- `requiredFieldTMMissing=0`
- `invalidFieldItemIds=0`
- `unloadedFieldItemIds=0`
- `scriptPatternUnmatchedItemBalls=10`
- `exceptionClass=none`
- `stacktrace=none`

## Gelesene Field-Items-Codepfade

UPR-FVX wurde read-only fuer den engen Field-Items-Scope geprueft:

- `GameRandomizer.maybeRandomizeFieldItems()`
- `Settings.FieldItemsMod`
- `Settings.banBadRandomFieldItems`
- `ItemRandomizer.randomizeFieldItems()`
- `ItemRandomizer.randomizeTMFieldItems(...)`
- `ItemRandomizer.randomizeNonTMFieldItems(...)`
- `Gen3RomHandler.preprocessMaps()`
- `Gen3RomHandler.getFieldItems()`
- `Gen3RomHandler.setFieldItems(...)`
- `RomHandler.getFieldItems()`
- `RomHandler.setFieldItems(...)`

## Guard-Entscheidung

Kein UPR-FVX-Codefix wurde in diesem Block vorgenommen.

Begruendung:

- `Gen3RomHandler.preprocessMaps()` sammelt erkannte sichtbare Itemball- und Hidden-Item-Slots in `itemOffs`.
- `Gen3RomHandler.getFieldItems()` iteriert ueber `itemOffs`, liest das aktuelle Item und gibt nur Slots zurueck, deren Item `isAllowed()` ist.
- `Gen3RomHandler.setFieldItems(...)` prueft zuerst per `checkFieldItemsTMsReplaceTMs(...)`, dass TM-Slots nur durch TMs und Non-TM-Slots nur durch Non-TMs ersetzt werden.
- `setFieldItems(...)` iteriert danach erneut ueber `itemOffs`, schreibt aber nur dann, wenn das aktuell gelesene ROM-Item `isAllowed()` ist.
- Dadurch bleiben disallowed/progression/key/system/pattern-unmatched Slots preserve-only, sofern sie nicht im allowed Field-Items-API-Scope auftauchen.
- Diagnose 100 passt zu diesem Modell: 339 erkannte Field-Item-Slots, davon 280 allowed Write-Scope und 59 disallowed Preserve-Scope.

Damit ist der bestehende Writer bereits ein allowed-slot Guard. Ein zusaetzlicher Codefix waere in diesem Block kein enger Bugfix, sondern wuerde ohne belegten Mismatch unnoetige Veraenderung in den UPR-FVX-Fork einbringen.

## Smoke-/Reload-Status

Kein Field-Items Write-/Reload-Smoke wurde in diesem Block ausgefuehrt.

Grund:

- Der Auftrag erlaubt den Write-/Reload-Smoke nur, falls ein lokaler CFRU/DPE Gen9-BPRE-Kandidat fuer diesen Block explizit freigegeben ist.
- Eine solche explizite Freigabe wurde in diesem Block nicht erteilt.
- Daher wurden keine ROMs gelesen, keine Randomizer-Writes ausgefuehrt, keine Output-ROM erzeugt und keine Logs dokumentiert.

Sanitisierter Status:

- `smokeExecuted=false`
- `candidateLoaded=not evaluated in this block`
- `saveSuccessful=not run`
- `logSuccessful=not run`
- `outputRomExists=not run`
- `logNonEmpty=not run`
- `reloadSuccessful=not run`
- `fieldItemsTotalBefore=not run`
- `fieldItemsTotalAfter=not run`
- `fieldItemsTotalReload=not run`
- `fieldItemReloadMismatches=not run`
- `visibleFieldItemReloadMismatches=not run`
- `hiddenFieldItemReloadMismatches=not run`
- `tmFieldItemSlotMismatches=not run`
- `nonTmFieldItemSlotMismatches=not run`
- `requiredFieldTMMissingAfter=not run`
- `requiredItemPolicyViolations=not run`
- `progressionItemPolicyViolations=not run`
- `invalidFieldItemWrites=not run`
- `unloadedFieldItemWrites=not run`
- `fallbackFieldItemWrites=not run`
- `placeholderFieldItemWrites=not run`
- `disallowedFieldItemWrites=not run`
- `scriptPatternExpansion=0`
- `exceptionClass=none`
- `stacktrace=none`

## Preserve-/Skip-Policy

Spaetere Field-Items-Writes duerfen nur den bestehenden allowed Field-Items-API-Scope beschreiben.

Write-Kandidaten:

- nur Field-Item-Slots, die `getFieldItems()` liefert
- nur aktuell allowed Items
- TM-Slots bleiben TM-Slots
- Non-TM-Slots bleiben Non-TM-Slots
- `FVX-ITEM-001` Field Items Shuffle ist der bevorzugte erste Carrier, weil er den bestehenden Itembestand innerhalb der TM-/Non-TM-Gruppen permutiert

Preserve-only:

- `disallowedFieldItemSlots=59`
- required/progression-sensitive Slots, soweit nicht ausdruecklich durch den allowed Field-Items-API-Scope freigegeben
- Key-/System-Items
- Placeholder-/Fallback-Items
- invalid oder unloaded Item-IDs
- `scriptPatternUnmatchedItemBalls=10`
- nicht erkannte Script-/Map-Strukturen
- Shops
- Pickup
- alle Held-Item-Writer

Zusatzregeln:

- Keine Scriptparser-Erweiterung in diesem Scope.
- Keine Shop-/Pickup-/Held-Item-Policy in diesem Scope.
- Ban-Bad-Items darf nur den Random-Pool beeinflussen, nicht preserve-only Slots freigeben.
- Required Field TMs muessen nach jedem spaeteren Reload vollstaendig bleiben.

## Spaetere Reload-/Review-Kriterien

Ein spaeterer explizit freigegebener Field-Items Write-/Reload-Smoke soll mindestens pruefen:

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
- `exceptionClass=none`
- `stacktrace=none`

## Feature-Status

- `FVX-ITEM-001` bleibt `Write modelliert`: Guard ist im bestehenden Code nachvollzogen, aber der Write-/Reload-Smoke wurde nicht ausgefuehrt.
- `FVX-ITEM-002` bleibt `Write modelliert`.
- `FVX-ITEM-003` bleibt `Write modelliert`.
- `FVX-ITEM-004` bleibt `Write modelliert`.

## Empfehlung

Naechster minimaler Schritt ist ein separater, explizit freigegebener Field-Items-only Write-/Reload-Smoke auf demselben UPR-FVX-Pin. Der erste Carrier sollte `FVX-ITEM-001 Field Items Shuffle` sein, weil damit der allowed-slot Guard, TM-/Non-TM-Stabilitaet und preserve-only Scope ohne zusaetzliche Item-Pool-/Ban-Bad-Komplexitaet pruefbar sind.
