# 121 - CFRU/DPE Shop Items Scope Diagnostics Plan

Datum: 2026-05-15
Branch: `analysis/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-plan`
UPR-FVX-Pin: `a2373888ad17145f270ebf6ff17303af41aa86eb`

## Ziel

Dieser Block plant Shops als neuen separaten CFRU/DPE Gen9-BPRE Item-Writer-Scope nach Field Items und Pickup. Der Plan bleibt read-only: keine Codeaenderung, kein Build, kein Randomizer-Lauf, kein ROM-/Artefaktzugriff und keine Aenderung an `02_external/**`.

Shops werden nicht aus Field Items, Pickup oder Held Items hochgestuft. Der Scope ist ein eigener Shoplisten-/Terminator-/Laengen-/Repointing-/Preis-Scope.

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/097_field_items_shops_pickup_scope_plan.md`
- `08_tests/randomizer/113_field_items_random_even_ban_bad_reload_smoke.md`
- `08_tests/randomizer/120_pickup_items_random_ban_bad_reload_smoke.md`
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

## Read-only Suchumfang

Verwendet wurden nur `rg` und `rg --files` fuer Dokumentations- und Codepfad-Recherche. Es gab keinen Build, keinen Randomizer-Lauf und keinen ROM-/Artefaktzugriff.

Suchbegriffe umfassten die Shop-, Item-, Settings-, GUI- und RomHandler-Pfade, insbesondere `randomizeShopItems`, `shuffleShopItems`, `addCheapRareCandiesToShops`, `getShops`, `setShops`, `getShopPrices`, `setShopPrices`, `ShopPointerOffsets`, `MainGameShops`, `SkipShops`, `DataRewriter`, `balanceShopPrices`, `guaranteeEvolutionItems`, `guaranteeXItems`, `banBadRandomShopItems`, `banRegularShopItems`, `banOPShopItems`, `ShopItemsMod`, `ItemRandomizer`, `Gen3RomHandler`, `RomHandler`, `Settings`, `GameRandomizer`, `ItemList`, `getAllowedItems`, `getNonBadItems`, `isBad`, `isAllowed`, `isTM`, `RandomizerGUI` und `Bundle.properties`.

## Feature-IDs

Shops werden als getrenntes Feature-/Paket-Scope behandelt:

- `FVX-ITEM-005 Shop Items Shuffle`
- `FVX-ITEM-006 Shop Items Random`
- `FVX-ITEM-007 Shop Item Bans`
- `FVX-ITEM-008 Guarantee Evolution/X Items`
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`

Field Items `FVX-ITEM-001..004`, Pickup `FVX-ITEM-010` und Held Items bleiben ausserhalb dieses Plans.

## Relevante Codepfade

- `Settings.ShopItemsMod`: `UNCHANGED`, `SHUFFLE`, `RANDOM`.
- `Settings.banBadRandomShopItems`, `banRegularShopItems`, `banOPShopItems`, `guaranteeEvolutionItems`, `guaranteeXItems`, `balanceShopPrices`, `addCheapRareCandiesToShops`.
- `RandomizerGUI`: liest und schreibt die Shop-Radio-Buttons und Shop-Suboptionen in `Settings`.
- `GameRandomizer.maybeRandomizeShops()`: ruft je nach `ShopItemsMod` `shuffleShopItems()` oder `randomizeShopItems()` auf und fuehrt danach optionale Preis-/Rare-Candy-Logik aus.
- `ItemRandomizer.shuffleShopItems()`: arbeitet auf `romHandler.getShops()`, mischt Items nur fuer Shops mit aktivem Special-Shop-Flag und schreibt ueber `romHandler.setShops(...)` zurueck.
- `ItemRandomizer.randomizeShopItems()`: kopiert Shops, baut einen Itempool aus `getAllowedItems()` oder `getNonBadItems()`, entfernt TMs, wendet Ban-/Guarantee-Policies an und schreibt ueber `setShops(...)`.
- `ItemRandomizer.addCheapRareCandiesToShops()`: fuegt Rare Candies zu Shoplisten hinzu und schreibt ebenfalls ueber `setShops(...)`.
- `AbstractRomHandler.balanceShopPrices()`: liest `getShopPrices()` und schreibt `setShopPrices(...)`.
- `RomHandler.getShops()` / `setShops(...)` / `getShopPrices()` / `setShopPrices(...)`: gemeinsame Shop-API.
- `Gen3RomHandler.getShops()` / `setShops(...)`: Gen3/BPRE Shoplisten-Reader/-Writer.
- `Gen3RomHandler.getShopPrices()` / `setShopPrices(...)`: Gen3 Item-Preis-Reader/-Writer.
- `Shop`: Datenmodell mit `items`, `name`, `isMainGame` und `isSpecialShop`.
- `Item`, `ItemList`, `AbstractRomHandler.getAllowedItems()` und `getNonBadItems()`: Itempool- und Ban-Basis.

## Erwartete Shop-Datenstruktur

- `ShopPointerOffsets` liefert Pointerlisten auf einzelne Shop-Itemlisten.
- Jede Gen3-Shopliste ist ein terminierter `u16`-Itemstream.
- Der Terminator ist Teil der Speicherstruktur, aber nicht Teil von `Shop.items`.
- Die Shoplaenge ergibt sich aus der Anzahl gelesener Items bis zum Terminator.
- `MainGameShops` markiert Shops fuer Main-Game-/Guarantee-Placement.
- `SkipShops` trennt Shops, die nicht randomisiert werden sollen, von Special-/randomisierbaren Shops.
- `Shop.isMainGame` und `Shop.isSpecialShop` transportieren diese Policy in `ItemRandomizer`.
- Special Shops bleiben ein eigener Policy-Fall, weil der aktuelle Code die Randomisierung an `isSpecialShop()` koppelt.
- Preislogik laeuft getrennt von Shoplisten ueber Item-Preisfelder und darf nicht mit Itemlisten-Repointing vermischt werden.

## setShops(...)-Einordnung

`Gen3RomHandler.setShops(...)` ist kein einfacher In-place-Writer. Der Pfad nutzt `DataRewriter<Shop>` fuer die Shoplisten und kann dadurch repointen, wenn neue Shopdaten nicht an die alte Stelle passen.

Konsequenz: Jeder spaetere Shop-Smoke muss Pointer, Terminatoren und Laengen explizit reloaden. Ein stabiler Field-Items- oder Pickup-Smoke beweist diesen Shop-Pfad nicht.

## Risiken

- Terminatoren: fehlende, doppelte oder verschobene `0x0000`-Terminatoren koennen Shops zusammenlaufen lassen oder abschneiden.
- Listenlaengen: Shuffle sollte Laengen erhalten; Random/Guarantee/Rare-Candy kann Laengen oder Inhalte veraendern.
- Repointing: `DataRewriter` kann Pointer aendern; Reload muss gueltige Pointer und unveraenderte Preserve-Shops nachweisen.
- Preserve-/Skip-Policy: Skip-/nicht randomisierbare Shops duerfen nicht versehentlich veraendert werden.
- Special Shops: die Bedeutung von `isSpecialShop` ist policy-relevant und muss gegen `SkipShops` verifiziert werden.
- MainGameShops: Guarantee Evolution/X Items nutzt Main-Game-Placement und darf nicht in falsche Shopklassen ausweichen.
- Preislogik: `balanceShopPrices` und Cheap-Rare-Candy-Preiswirkung sind separat von Itemlisten zu messen.
- Itempool: invalid, unloaded, fallback, placeholder, bad, regular-banned, OP-banned und TM-Items duerfen nicht unkontrolliert in Shops gelangen.
- CFRU/DPE Gen9-BPRE: erweiterte Itemdaten koennen klassische Itempreis-/Allowed-/Bad-Item-Annahmen sprengen.

## Preserve-/Skip-Policy

- Field Items, Pickup und Held Items bleiben unveraendert: `fieldItemScopeChanged=false`, `pickupScopeChanged=false`, `heldItemScopeChanged=false`.
- Shops aus `SkipShops` bleiben preserve-only, bis eine separate Policy sie freigibt.
- Nicht randomisierte Shops muessen byte-/reload-stabil bleiben oder als bewusst repointed mit identischem Inhalt nachgewiesen werden.
- Special-Shop- und Main-Game-Markierungen muessen pro Shop erhalten und in Metriken getrennt gezaehlt werden.
- Invalid/unloaded/fallback/placeholder Items sind keine neuen Kandidaten.
- Bad-/Regular-/OP-Bans gelten nur fuer den Shop-Pool und nicht automatisch fuer Field Items, Pickup oder Held Items.
- Preiswrites laufen nur, wenn die jeweilige Preisoption aktiv ist; andernfalls muss die Preistabelle unveraendert bleiben.

## Spaetere Diagnose-/Smoke-Metriken

Read-only Kandidatendiagnose:

```text
candidateLoaded
shopScanSuccessful
shopCount
mainGameShopCount
skippedShopCount
specialShopCount
shopItemsTotal
mainGameShopItemsTotal
skippedShopItemsTotal
specialShopItemsTotal
shopTerminatorScanSuccessful
shopTerminatorMismatches
shopLengthMismatches
invalidShopItemIds
unloadedShopItemIds
fallbackShopItems
placeholderShopItems
badShopItems
regularBannedShopItems
opBannedShopItems
shopTmItems
shopAllowedPoolSize
shopNonBadPoolSize
shopBadItemPoolCandidates
shopBadItemPoolExcluded
priceTableReadable
fieldItemScopeChanged=false
pickupScopeChanged=false
heldItemScopeChanged=false
```

Write-/Reload-Smokes:

```text
candidateLoaded=true
smokeExecuted=true
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
reloadSuccessful=true
shopCountBefore
shopCountAfter
shopCountReload
shopItemsTotalBefore
shopItemsTotalAfter
shopItemsTotalReload
shopItemReloadMismatches=0
shopTerminatorMismatches=0
shopLengthMismatches=0
shopPointerMismatches=0 fuer preserve-only Shops
repointedShopPointersValid=true falls Repointing stattfindet
invalidShopItemWrites=0
unloadedShopItemWrites=0
fallbackShopItemWrites=0
placeholderShopItemWrites=0
badShopItemWrites=0 bei Ban Bad
regularBannedShopItemWrites=0 bei Ban Regular
opBannedShopItemWrites=0 bei Ban OP
preservedSkippedShops=true
specialShopPolicyViolations=0
mainGameShopPolicyViolations=0
guaranteeEvolutionItemsPresent je nach Option
guaranteeXItemsPresent je nach Option
priceTableChanged je nach Preisoption
priceTableUnchanged je nach deaktivierter Preisoption
cheapRareCandyShopMismatches=0 je nach Option
fieldItemScopeChanged=false
pickupScopeChanged=false
heldItemScopeChanged=false
exceptionClass=none
stacktrace=none
```

## Empfohlene Reihenfolge

1. Shop read-only Kandidatendiagnose.
2. Shop Shuffle Smoke.
3. Shop Random Smoke.
4. Shop Item Bans.
5. Guarantee Evolution/X Items.
6. Balance Shop Prices / Cheap Rare Candies separat.

Diese Reihenfolge minimiert Risiko: zuerst Reader/Terminatoren/Laengen/Policy pruefen, dann inhaltsgleiche Shuffle-/Random-Writes, danach Pool-Bans und erst zuletzt Platzierungs- und Preis-/Laengenaenderungen.

## Scope-Einschaetzung

Shops sind ein eigener CFRU/DPE Gen9-BPRE Feature-/Paket-Scope. Der Shop-Pfad beruehrt terminierte Itemlisten, Pointerlisten, `DataRewriter`-/Repointing-Verhalten, Special-/Skip-/Main-Game-Policy und optionale Preisfelder. Das ist nicht derselbe Writer-Typ wie Field Items, Pickup oder Held Items.

`FVX-ITEM-005..009` bleiben nach diesem Plan `Write modelliert` bzw. geplant, bis separate Shop-only Kandidatendiagnosen und Smokes einen stabilen Reload nachweisen.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics`: sanitized read-only Shop-Kandidatendiagnose mit aggregierten Shop-, Terminator-, Laengen-, Policy-, Itempool- und Preislese-Metriken. Kein Shop-Write-Smoke vor dieser Diagnose.
