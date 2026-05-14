# 108 - Field Items API TM-slot scope fix

Datum: 2026-05-15
Workspace-Branch: `compat/upr-fvx-cfru-dpe-field-items-api-tm-slot-scope-fix`
UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-field-items-api-tm-slot-scope-fix`
UPR-FVX-Commit: `328e4441c2981d37aba9e2707a6f27f779b026e2`
UPR-FVX PR: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/37>

## Ziel

Minimaler CFRU/DPE-gated Field-Items-API-TM-Slot-Fix fuer `FVX-ITEM-002 Field Items Random`.

Der Fix soll bewirken, dass der Randomizer-API-Pfad die raw belegten Field-TM-Slots sieht, ohne TMs global allowed zu setzen und ohne Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even oder Ban Bad Items auszuweiten.

## Ausgangsbefund

Diagnose 107 hat den aktiven Blocker eingegrenzt:

- Raw-Diagnosen sehen `tmFieldItemSlots=28`.
- `requiredFieldTMsTotal=24` und `requiredFieldTMMissing=0` sind belegt.
- Der Randomizer-API-Pfad sah in Diagnose 106 aber `randomTmNeededSlots=0` / `randomTmCurrentSlots=0`.
- Ursache: `Gen3RomHandler.getFieldItems()` und `setFieldItems(...)` filterten den API-Slot-Scope ausschliesslich ueber `Item::isAllowed`.
- TMs waren geladen und als `Item::isTM` markiert, wurden aber nicht in den Field-Items-API-Scope aufgenommen.

## Fix-Entscheidung

Option A aus Diagnose 107 wurde umgesetzt.

Geaendert wurde nur:

- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`

Implementierung:

- Neuer privater Helper `isFieldItemRandomizerApiSlot(Item item)`.
- Bisherige allowed Slots bleiben im API-Scope.
- Im sicheren CFRU/DPE-Gen9-Gate (`useCfruDpeGen9SpeciesCount`) werden Field-TM-Slots zusaetzlich in den Field-Items-API-Scope aufgenommen.
- `getFieldItems()` und `setFieldItems(...)` nutzen denselben Helper.
- `checkFieldItemsTMsReplaceTMs(...)` sieht dadurch weiter konsistente Current- und Replacement-Listen in derselben Slotreihenfolge.

Nicht geaendert:

- `Item.allowed` wird nicht global fuer TMs veraendert.
- Keine globale ItemList-/allowedItems-Ausweitung.
- Keine Shops.
- Kein Pickup.
- Keine Held Items.
- Keine TM/HM/Tutor/Learnset-Writer.
- Keine Scriptparser-Erweiterung.
- Keine Random Even Distribution.
- Keine Ban-Bad-Items-Umsetzung.

## UPR-FVX Checks

Ausgefuehrt:

- `git status --short`
- `git diff --stat`
- `git diff --check`
- `./gradlew :random:classes`

Ergebnis:

- `git diff --check`: keine Whitespace-/Patchfehler.
- `./gradlew :random:classes`: erfolgreich.

## Smoke-/Reload-Ergebnis

Kein fachlicher ROM Write-/Reload-Smoke wurde in diesem Codefix-Block ausgefuehrt.

Begruendung:

- Der Codefix und Compile-Check konnten ohne ROM-Zugriff vorbereitet werden.
- Im committed Workspace wurde kein wiederverwendbarer, nicht-privater Smoke-Harness gefunden, der ohne Dokumentation privater Artefakte direkt ausgefuehrt werden kann.
- Die Feature-Hochstufung fuer `FVX-ITEM-002` bleibt deshalb ausgesetzt, bis ein separater sanitiserter Field-Items-only Reload-Smoke auf dem neuen UPR-FVX-Pin laeuft.

Sanitisiertes Smoke-Ziel fuer den naechsten Block:

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
- `apiTmFieldSlotWrites` dokumentiert
- `scriptPatternExpansion=0`
- `badFieldItemWrites=0` oder `not evaluated`, weil `banBadRandomFieldItems=false`
- `randomTmNeededSlots=28`
- `randomTmCurrentSlots=28`
- `randomTmRequiredTotal=24`
- `randomTmRequiredPresent=24`
- `randomTmRequiredMissingBefore=0`
- `randomTmRequiredMissingAfter=0`
- `randomTmLoadedPoolSize=50`
- `randomTmUniquePoolSize >= 28`
- `randomTmFillerNeeded=4`
- `randomTmFillerAvailable >= 4`
- `randomTmDuplicateSelections=0`
- `randomTmPoolDeficit=0`
- `randomTmResultSize=28`
- `randomTmResultUniqueSize=28`
- `apiTmFieldItemSlots=28`
- `rawTmFieldItemSlots=28`
- `rawApiTmSlotAlignmentMismatches=0`
- `tmGloballyAllowedChanged=false`
- `shopItemScopeChanged=false`
- `pickupItemScopeChanged=false`
- `heldItemScopeChanged=false`
- `exceptionClass=none`
- `stacktrace=none`

## Preserve-/Skip-Policy

Write bleibt nur im Field-Items-API-Scope.

Zusaetzlich sichtbar werden nur CFRU/DPE Field-TM-Slots, weil sie Field-Item-Slots sind und fuer Required-Field-TM-Erhaltung gebraucht werden.

Preserve-only bleibt fuer:

- disallowed non-TM Field-Item-Slots
- progression-/key-/system-sensitive Slots
- invalid/unloaded/fallback/placeholder Slots
- `scriptPatternUnmatchedItemBalls=10`
- nicht erkannte Script-/Map-Strukturen
- Shops
- Pickup
- Encounter Held Items
- Trainer Held Items
- Starter Held Items
- TM/HM/Tutor/Learnset-Writer
- Palette/Graphics
- MoveData/MoveNames
- TypeChart/TypeEffectiveness
- Trainer/Wild/Evolution/Text/Menu

Invarianten:

- TMs werden nicht global allowed.
- TM-Slots muessen TM-Slots bleiben.
- Non-TM-Slots muessen Non-TM-Slots bleiben.
- Required Field TMs muessen vollstaendig bleiben.
- `scriptPatternUnmatchedItemBalls=10` wird nicht erweitert und nicht geschrieben.

## Feature-Status

- `FVX-ITEM-001 Field Items Shuffle`: bleibt `GUI-kompatibel` im engen Shuffle-Scope.
- `FVX-ITEM-002 Field Items Random`: Fix vorbereitet, aber bis zum separaten Reload-Smoke weiter `Write modelliert` / nicht GUI-kompatibel.
- `FVX-ITEM-003 Field Items Random even distribution`: bleibt `Write modelliert`.
- `FVX-ITEM-004 Field Items Ban Bad Items`: bleibt `Write modelliert`.

## Naechster minimaler Schritt

Branch: `test/upr-fvx-cfru-dpe-field-items-api-tm-slot-reload-smoke`

Ziel: Den neuen UPR-FVX-Pin `328e4441c2981d37aba9e2707a6f27f779b026e2` mit einem sanitisierten Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke pruefen, `banBadRandomFieldItems=false`, keine Scope-Ausweitung.
