# 097 - CFRU/DPE Field Items / Shops / Pickup Scope Plan

Datum: 2026-05-14
Branch: `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan`
UPR-FVX-Pin: `2697511da9a97df4c29c00dfda8b40e556020489`

## Ziel

Dieser Block plant read-only den engen P1-Scope fuer Field Items, Shops und Pickup im CFRU/DPE Gen9-BPRE-Stand. Ziel ist die Entscheidung, ob diese drei Writer gemeinsam behandelt werden koennen oder getrennte Folgeblocks brauchen.

Nicht ausgefuehrt:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Randomizer-Lauf
- kein Build
- kein ROM-, Save-, Emulator-State-, Output-ROM-, Log- oder Tool-Binary-Zugriff
- keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets oder Secrets dokumentiert

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

Zusaetzlich beruecksichtigt wurden fruehere Item-/Held-Item-Protokolle ueber `rg`-Treffer, insbesondere Diagnose 053/054 als Grenze fuer Item-Scope und Encounter Held Items.

## Read-only UPR-FVX-Codepfade

### Gemeinsamer Einstieg

`GameRandomizer` fuehrt die drei Itempfade separat aus:

- `maybeRandomizeFieldItems()`
- `maybeRandomizeShops()`
- `maybeRandomizePickupItems()`

Alle drei laufen ueber `ItemRandomizer`, teilen aber unterschiedliche `RomHandler`-APIs:

- Field Items: `getFieldItems()` / `setFieldItems(...)`
- Shops: `getShops()` / `setShops(...)` / `setShopPrices(...)`
- Pickup: `getPickupItems()` / `setPickupItems(...)`

### Field Items

Feature-IDs:

- `FVX-ITEM-001` Field Items Shuffle
- `FVX-ITEM-002` Field Items Random
- `FVX-ITEM-003` Field Items Random even distribution
- `FVX-ITEM-004` Field Items Ban Bad Items

Codepfade:

- `Settings.FieldItemsMod`: `UNCHANGED`, `SHUFFLE`, `RANDOM`, `RANDOM_EVEN`
- `Settings.banBadRandomFieldItems`
- `ItemRandomizer.randomizeFieldItems()`
- `ItemRandomizer.randomizeTMFieldItems(...)`
- `ItemRandomizer.randomizeNonTMFieldItems(...)`
- `Gen3RomHandler.preprocessMaps()`
- `Gen3RomHandler.getFieldItems()`
- `Gen3RomHandler.setFieldItems(...)`

Datenstruktur:

- sichtbare Itemballs werden in Map-Event-Person-Scripts erkannt
- Hidden Items werden in Signpost-Entries erkannt
- `itemOffs` sammelt die konkreten `u16` Item-ID-Felder
- `setFieldItems(...)` schreibt nur vorhandene erlaubte Field-Item-Slots zurueck
- TM-Slots muessen TM-Slots bleiben; Nicht-TM-Slots muessen Nicht-TM-Slots bleiben
- Required Field TMs werden ueber `getRequiredFieldTMs()` im TM-Pool erzwungen

CFRU/DPE-Risiko:

- Map-/Script-Erkennung kann bei Hack-spezifischen Scriptformen unvollstaendig sein
- Progression-/Required-/Key-Items duerfen nicht blind ersetzt werden
- moderne TM/HM- und Systemitems brauchen pfadspezifische Bans
- Fallback-/Placeholder-Items duerfen nicht neu gepickt werden
- Hidden Items und sichtbare Itemballs sollten getrennt zaehlbar bleiben

### Shops

Feature-IDs:

- `FVX-ITEM-005` Shop Items Shuffle
- `FVX-ITEM-006` Shop Items Random
- `FVX-ITEM-007` Shop Item Bans
- `FVX-ITEM-008` Guarantee Evolution/X Items
- `FVX-ITEM-009` Balance Shop Prices / Cheap Rare Candies

Codepfade:

- `Settings.ShopItemsMod`: `UNCHANGED`, `SHUFFLE`, `RANDOM`
- `Settings.banBadRandomShopItems`
- `Settings.banRegularShopItems`
- `Settings.banOPShopItems`
- `Settings.guaranteeEvolutionItems`
- `Settings.guaranteeXItems`
- `Settings.balanceShopPrices`
- `Settings.addCheapRareCandiesToShops`
- `ItemRandomizer.shuffleShopItems()`
- `ItemRandomizer.randomizeShopItems()`
- `ItemRandomizer.addCheapRareCandiesToShops()`
- `Gen3RomHandler.getShops()`
- `Gen3RomHandler.setShops(...)`
- `Gen3RomHandler.getShopPrices()`
- `Gen3RomHandler.setShopPrices(...)`

Datenstruktur:

- `ShopPointerOffsets` zeigt auf Shop-Itemlisten
- Shoplisten sind `u16` Item-Streams mit `0x0000` Terminator
- `SkipShops` markiert nicht randomisierte Shops
- `MainGameShops` beeinflusst garantierte Evolution-/X-Item-Platzierung
- `setShops(...)` nutzt `DataRewriter` und kann Shoplisten repointen
- Preisoptionen schreiben in `ItemData` bei Preis-Offset innerhalb der Item-Entries

CFRU/DPE-Risiko:

- Shoplisten koennen Script-/Menu-gebunden sein
- `DataRewriter` macht Shops zu einem Repointing-Scope, nicht zu einfachem In-place-Write
- Shopgroessen koennen sich bei Cheap Rare Candies aendern
- Terminatoren und Pointer muessen reloadbar erhalten oder bewusst geaendert werden
- Preise nutzen `ItemData` und muessen mit dem erweiterten Item-Scope zusammenpassen
- garantierte Evolution-/X-Items koennen Progression oder Balancing beeinflussen

### Pickup

Feature-ID:

- `FVX-ITEM-010` Pickup Items Random / Ban Bad Items

Codepfade:

- `Settings.PickupItemsMod`: `UNCHANGED`, `RANDOM`
- `Settings.banBadRandomPickupItems`
- `ItemRandomizer.randomizePickupItems()`
- `Gen3RomHandler.getPickupItems()`
- `Gen3RomHandler.setPickupItems(...)`

Datenstruktur:

- `PickupTableStartLocator` sucht den Tabellenstart
- `PickupItemCount` bestimmt die Anzahl klassischer Eintraege
- Gen3-FRLG nutzt eine flache Tabelle mit `u16` Item-IDs und erhaelt Probability-Slots im Modell
- `PickupItem.PROBABILITY_SLOTS=10`
- `setPickupItems(...)` schreibt nur die Item-ID-Felder; Wahrscheinlichkeiten werden nicht separat geschrieben

CFRU/DPE-Risiko:

- CFRU/DPE kann Common-/Rare-Pickup-Tabellen statt klassischer flacher FRLG-Tabelle nutzen
- ein klassischer Locator/Count kann den aktiven CFRU/DPE-Pickup-Scope nur teilweise treffen
- Probability-Slots muessen als Semantik erhalten bleiben
- moderne Bad-/Banned-/Placeholder-Items duerfen nicht in Pickup gelangen

## Abgrenzung zu anderen Itempfaden

Nicht Teil dieses Scopes:

- Encounter Held Items: bereits eigener `gBaseStats`-Scope aus Diagnose 054
- Trainer Held Items: Trainer-Party-Daten, seit frueheren Diagnosen separat stabil
- Starter Held Items: eigener Starter-Scope, nicht durch Field/Shop/Pickup belegt
- TM/HM/Tutor/Learnset: eigene Writer und Kompatibilitaetstabellen
- Item-Text, Menues, Descriptions: Text/Menu-Scope, nicht Item-Daten-Writer

Nicht mit diesem Plan vermischen:

- MoveData / MoveNames
- Palette / Graphics
- TypeChart / TypeEffectiveness
- Trainer / Wild / Evolution
- Species-Type-Write

## Preserve-/Skip-Policy

Gemeinsame Policy fuer spaetere Blocks:

1. Fallbackbenannte oder unbekannte Items nicht als neue Random-Picks verwenden.
2. Free-Space-, Placeholder-, Shiny-Space-, Key-/System-/Progression-Items preserve-only oder explizit bannen.
3. Bestehende moderne IDs nur preserven, solange keine pfadspezifische sichere Replacement-Semantik existiert.
4. Invalide oder nicht geladene Item-IDs nie neu schreiben; als Blocker oder Preserve-Fall dokumentieren.
5. TMs/HMs pfadspezifisch behandeln; Field-TM-Slots muessen TM-Slots bleiben.
6. Field required/progression Items zuerst konservativ preserve-only behandeln, bis eine explizite Required-Policy existiert.
7. Shop-Terminatoren, Pointer, Laengen und Special-/Skip-Shop-Markierungen erhalten oder gezielt mit Reload-Nachweis aendern.
8. Pickup-Tabellenlaenge und Probability-/Common-/Rare-Semantik erhalten.
9. Bad-/Banned-Item-Filter muessen pfadspezifisch sein; Encounter-Held-Item-Bans aus 054 sind Grundlage, aber nicht automatisch ausreichend.

## Scope-Einschaetzung

Ein gemeinsamer Fixblock fuer Field Items, Shops und Pickup ist nicht reviewbar eng genug.

Begruendung:

- Field Items sind Map-/Script-Offset-Writer mit TM-/Required-Policy.
- Pickup ist ein begrenzter Table-Writer mit Locator-/Count-/Probability-Semantik.
- Shops sind Shoplisten mit Terminatoren, Repointing via `DataRewriter`, Special-/Main-Game-Policy und optional Preiswrites.
- Alle drei teilen Item-Pool- und Bad-/Banned-Filter, aber nicht denselben Write-/Reload-Risiko-Typ.

## Vorgeschlagene Aufteilung

Empfohlene Reihenfolge:

1. `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`
   - Field Items zuerst, weil der Writer vorhandene Item-ID-Felder in Map-/Script-/Signpost-Slots ersetzt und keine Shoplisten-Repointing-Semantik braucht.
   - Ziel: sichtbare Itemballs, Hidden Items, TM-Slots, Required-TMs, invalid/fallback Items und progression-sensitive Slots aggregiert klassifizieren.

2. `analysis/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics-plan`
   - Pickup danach, weil der Write-Pfad klein ist, aber CFRU/DPE Common-/Rare-Semantik und Locator/Count validiert werden muessen.
   - Ziel: Tabellenlaenge, Common/Rare-Abdeckung, Probability-Slots und invalid/fallback Item-Pool pruefen.

3. `analysis/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-plan`
   - Shops zuletzt, weil `setShops(...)` Repointing, Terminatoren, Shopgroessen und Preise beruehren kann.
   - Ziel: Shopliste/Terminator/Pointer/Laenge/Special-Shop/Preis-Scope separat modellieren.

Optionaler gemeinsamer Vorblock:

- `analysis/upr-fvx-cfru-dpe-item-pool-path-bans-plan`
- Zweck: pfadspezifische Item-Pool-Bans fuer Field, Shop und Pickup aus dem erweiterten CFRU/DPE-Item-Scope ableiten.
- Nur sinnvoll, wenn ein spaeterer Fix zuerst die gemeinsame Poolbasis verbessern soll.

## Spaetere Reload-/Review-Kriterien

### Gemeinsame Kriterien

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `itemCount` dokumentiert
- hoechste geladene Item-ID dokumentiert
- `itemNameFallbacks=0` fuer Random-Pick-Kandidaten oder Fallbacks als banned/unsafe klassifiziert
- `bannedItemViolations=0`
- `invalidItemWrites=0`
- `exceptionClass=none`
- `stacktrace=none`
- keine privaten Artefaktwerte dokumentiert

### Field Items

- `fieldItemsTotalBefore`
- `fieldItemsTotalAfter`
- `fieldItemsTotalReload`
- `fieldItemReloadMismatches=0`
- `fieldItemByteMismatches=0`
- `visibleFieldItemReloadMismatches=0`
- `hiddenFieldItemReloadMismatches=0`
- `tmFieldItemSlotMismatches=0`
- `requiredFieldTMPreservedOrPresent=true`
- `requiredItemPolicyViolations=0`
- `invalidFieldItemWrites=0`
- `fieldItemTerminatorMismatches=0`, falls ein spaeterer Harness Terminator-/Scriptgrenzen modelliert

### Shops

- `shopsTotalBefore`
- `shopsTotalAfter`
- `shopsTotalReload`
- `shopItemReloadMismatches=0`
- `shopTerminatorMismatches=0`
- `shopLengthMismatches=0`
- `shopPointerMismatches=0` fuer unveraenderte Shops
- `repointedShopPointersValid=true`, falls Repointing stattfindet
- `specialShopPolicyViolations=0`
- `mainGameShopPolicyViolations=0`
- `invalidShopItemWrites=0`
- `shopPriceReloadMismatches=0`, falls Preise betroffen sind
- `cheapRareCandyShopMismatches=0`, falls Cheap Rare Candies im Scope ist

### Pickup

- `pickupItemsTotalBefore`
- `pickupItemsTotalAfter`
- `pickupItemsTotalReload`
- `pickupItemReloadMismatches=0`
- `pickupTableLengthMismatches=0`
- `pickupProbabilityMismatches=0`
- `pickupCommonRarePolicyViolations=0`
- `invalidPickupItemWrites=0`
- `pickupLocatorSuccessful=true`

## Empfehlung

Empfehlung: getrennte Fixes/Smokes, keine gemeinsame Umsetzung.

Direkt naechster sinnvoller Block ist eine Field-Items-Diagnoseplanung, weil Field Items der naechste engste Datenpfad sind und Shops wegen Repointing/Preisen groesser bleiben. Pickup ist ebenfalls klein, braucht aber zuerst die CFRU/DPE-Table-Semantik gegen den aktiven Kandidaten.

Empfohlener Folgebranch:

- `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`
