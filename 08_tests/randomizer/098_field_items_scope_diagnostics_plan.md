# 098 - CFRU/DPE Field Items Scope Diagnostics Plan

## Ziel

Dieser Plan trennt Field Items als ersten eigenstaendigen Item-Writer-Scope fuer den CFRU/DPE Gen9-BPRE-Stand ab. Er beschreibt eine spaetere read-only Diagnose fuer sichtbare Itemballs, Hidden Items/Signposts, TM- und Non-TM-Slots sowie required/progression-sensitive Items.

Dieser Block enthaelt keine Umsetzung, keinen Randomizer-Lauf, keinen Build, keine ROM-Arbeit und keine Codeaenderung.

## Ausgangslage

- Vorheriger Scope-Plan 097 trennt Field Items, Shops und Pickup als eigene Folgearbeiten.
- Field Items betreffen `FVX-ITEM-001` bis `FVX-ITEM-004`.
- Shops (`FVX-ITEM-005` bis `FVX-ITEM-009`) und Pickup (`FVX-ITEM-010`) bleiben ausserhalb dieses Blocks.
- UPR-FVX bleibt im Workspace auf dem bestehenden Pin `2697511da9a97df4c29c00dfda8b40e556020489`.
- Dieser Plan dokumentiert nur aggregierte Diagnoseanforderungen; keine privaten Pfade, ROM-Namen, Hashes, Pointer oder Offsets.

## Read-only gepruefte Field-Item-Codepfade

### GUI / Settings / Randomizer-Orchestrierung

- `Settings.FieldItemsMod` modelliert die Field-Items-Modi `UNCHANGED`, `SHUFFLE`, `RANDOM` und `RANDOM_EVEN`.
- `Settings.banBadRandomFieldItems` steuert die Bad-Item-Ban-Option fuer Random Field Items.
- `GameRandomizer.maybeRandomizeFieldItems()` ist der zentrale Orchestrierungs-Pfad fuer Field Items.
- `maybeRandomizeFieldItems()` ruft `ItemRandomizer.randomizeFieldItems(...)` nur fuer `SHUFFLE`, `RANDOM` und `RANDOM_EVEN` auf.
- GUI-/Bundle-Pfade schalten Field Items getrennt von Shops und Pickup.

### ItemRandomizer

- `ItemRandomizer.randomizeFieldItems(...)` liest die aktuellen Field Items aus dem ROM-Handler und trennt TM- von Non-TM-Slots.
- `SHUFFLE` mischt TM- und Non-TM-Slots getrennt und kombiniert sie danach wieder positionsstabil nach Slot-Typ.
- `RANDOM` und `RANDOM_EVEN` nutzen getrennte Generatoren fuer TM- und Non-TM-Field-Items.
- `randomizeTMFieldItems(...)` nutzt die geladene TM-Liste und `getRequiredFieldTMs()`; required Field TMs muessen bei der spaeteren Diagnose explizit gezaehlt und erhalten werden.
- `randomizeNonTMFieldItems(...)` nutzt erlaubte Items bzw. Non-Bad-Items, entfernt TMs aus dem Non-TM-Pool und kann bei gleichmaessiger Verteilung eine Queue nutzen.
- Der Randomizer verlaesst sich auf `setFieldItems(...)`, um TM-Slots nicht mit Non-TMs und Non-TM-Slots nicht mit TMs zu ersetzen.

### Gen3 ROM-Handler

- `Gen3RomHandler.preprocessMaps()` baut den internen Field-Item-Slot-Scope aus Map-Daten auf.
- Sichtbare Itemballs werden ueber Itemball-Sprites und ein erwartetes Script-Muster erkannt.
- Hidden Items werden ueber Signpost-Typen erkannt; Coin-/Null-Faelle werden nicht als normale Item-Slots behandelt.
- `Gen3RomHandler.getFieldItems()` liest nur erlaubte Items aus den erkannten Field-Item-Slots.
- `Gen3RomHandler.setFieldItems(...)` schreibt nur Slots, deren aktuelle Items erlaubt sind, und prueft vorher die TM-vs-Non-TM-Ersetzung.
- `RomHandler.getFieldItems()` und `RomHandler.setFieldItems(...)` definieren den generischen API-Vertrag; der Gen3-Kommentar verlangt, dass TMs durch TMs und Non-TMs durch Non-TMs ersetzt werden.

## Diagnose-Scope

Die spaetere Diagnose soll ausschliesslich Field Items klassifizieren:

- sichtbare Itemballs
- Hidden Items / Signposts
- TM-Slots
- Non-TM-Slots
- Required Field TMs
- required/progression-sensitive Items
- Key-/System-/Placeholder-/Fallback-/Bad-Items
- moderne Item-IDs
- invalid oder nicht geladene Item-IDs
- Script-/Map-Erkennungsrisiken

Nicht in diesem Scope:

- Shops
- Pickup
- Encounter Held Items
- Trainer Held Items
- Starter Held Items
- TM/HM/Tutor/Learnset-Writer
- Palette / Graphics
- MoveData / MoveNames
- TypeChart / TypeEffectiveness
- Trainer
- Wild
- Evolution
- Text/Menu

## Geplante aggregierte Diagnosemetriken

Pflichtmetriken fuer einen spaeteren Diagnose-Lauf:

- `candidateLoaded`
- `fieldItemScanSuccessful`
- `mapBanksScanned`
- `mapsScanned`
- `fieldItemsTotal`
- `visibleFieldItemSlots`
- `hiddenFieldItemSlots`
- `allowedFieldItemSlots`
- `disallowedFieldItemSlots`
- `tmFieldItemSlots`
- `nonTmFieldItemSlots`
- `requiredFieldTMsTotal`
- `requiredFieldTMPresent`
- `requiredFieldTMMissing`
- `progressionSensitiveFieldItems`
- `keyOrSystemFieldItems`
- `placeholderFieldItems`
- `fallbackFieldItems`
- `badFieldItems`
- `modernFieldItemIds`
- `invalidFieldItemIds`
- `unloadedFieldItemIds`
- `scriptPatternUnmatchedItemBalls`
- `hiddenItemSignpostSlots`
- `coinOrNullHiddenItemSlots`
- `exceptionClass`
- `stacktrace`

Optionale sinnvolle Metriken:

- `fieldItemUniqueItems`
- `fieldItemDuplicateItems`
- `tmFieldItemUniqueItems`
- `nonTmFieldItemUniqueItems`
- `requiredProgressionItemsPreservedByCurrentPolicy`
- `badItemBanCandidates`
- `badItemBanRemovalsNeeded`
- `modernItemIdsAllowed`
- `modernItemIdsRejected`
- `fieldItemScanWarnings`

Sanitizing-Regel: Nur aggregierte Zaehler und boolesche Ergebnisse dokumentieren. Keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Map-Daten, Script-Bytes oder Logauszuege.

## Preserve-/Skip-Policy fuer Field Items

Spaetere Field-Item-Fixes oder Smokes sollen folgende enge Policy verwenden:

- Required Field TMs bleiben erhalten oder werden nur durch sichere TM-Slot-Policy ersetzt, wenn die Required-TM-Abdeckung nach Reload stabil bleibt.
- TM-Slots duerfen nur TM-Ersatz erhalten.
- Non-TM-Slots duerfen keinen TM-Ersatz erhalten.
- Required/progression-sensitive Items sind preserve-only, bis eine explizite Progression-Policy existiert.
- Key-/System-/Placeholder-/Fallback-Items sind preserve-only oder aus dem Random-Pool ausgeschlossen.
- Bad Items werden nur ueber die Field-Items-Ban-Policy ausgeschlossen; keine globale Item-Pool-Annahme auf Shops/Pickup uebertragen.
- Invalide oder nicht geladene Item-IDs werden nicht geschrieben und bleiben preserve-only.
- Moderne Item-IDs duerfen nur geschrieben werden, wenn sie vom CFRU/DPE-Stand geladen, erlaubt und reload-stabil sind.
- Sichtbare Itemballs und Hidden Items behalten ihre Slot-Kategorie; keine Umdeutung in Shops, Pickup oder Scripts ausserhalb der Field-Item-Erkennung.
- Nicht erkannte oder vom erwarteten Muster abweichende Itemball-/Signpost-Strukturen werden nicht geschrieben.
- Coin-/Null-Hidden-Item-Faelle bleiben ausserhalb normaler Item-Randomization.
- Die Diagnose und spaetere Fixes dokumentieren keine Raw Pointer, Offsets oder Scriptdaten.

## Spaetere Reload-/Review-Kriterien fuer Field Items

Ein spaeterer Field-Items-Smoke soll mindestens folgende Kriterien berichten:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `fieldItemScanSuccessful=true`
- `fieldItemsTotalBefore == fieldItemsTotalAfter`
- `fieldItemsTotalAfter == fieldItemsTotalReload`
- `fieldItemReloadMismatches=0`
- `fieldItemByteMismatches=0`
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
- `badFieldItemWrites=0` when `banBadRandomFieldItems=true`
- `scriptPatternExpansion=0` unless a separate Script-/Map-parser plan approves it
- `exceptionClass=none`
- `stacktrace=none`

Falls ein spaeterer Lauf private Artefakte benoetigt, duerfen nur aggregierte Zaehlwerte dokumentiert werden.

## Scope-Einschaetzung

Field Items sind reviewbar als erster getrennter Item-Writer-Diagnoseblock, aber noch nicht als Fixblock. Der kritische erste Schritt ist eine read-only Diagnose, die den tatsaechlichen CFRU/DPE-BPRE-Slot-Scope, die TM-/Non-TM-Verteilung, Required Field TMs und invalid/moderne Item-IDs aggregiert.

Ein direkter Fix ohne diese Diagnose waere zu breit, weil Map-/Script-Erkennung, Required Items und moderne Item-IDs sonst nicht sauber von Shops, Pickup und anderen Item-Pfaden getrennt waeren.

## Empfehlung

Naechster minimaler Schritt: ein sanitiserter Field-Items-Diagnose-Lauf ohne Writer-Fix auf einem lokal freigegebenen CFRU/DPE Gen9-BPRE-Kandidaten. Vorgeschlagener Folgebranch:

`test/upr-fvx-cfru-dpe-field-items-scope-diagnostics`
