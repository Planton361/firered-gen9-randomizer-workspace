# Diagnose 130: Shop Guarantee Items Scope Plan

Datum: 2026-05-15
Branch: `analysis/upr-fvx-cfru-dpe-shop-guarantee-items-scope-plan`
Scope: Read-only Plan fuer `FVX-ITEM-008 Guarantee Evolution/X Items`

## Ziel

Dieser Block plant `FVX-ITEM-008 Guarantee Evolution/X Items` als separaten Shop-only Subscope nach den einzeln reloadstabilen Shop-Ban-Smokes aus Diagnose 127, 128 und 129.

Der Block ist read-only:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Build
- kein Randomizer-Lauf
- kein ROM-/Artefaktzugriff
- kein Shop Write/Save

## Scope

Nur `FVX-ITEM-008` wird geplant.

Getrennt betrachtet:

- Guarantee Evolution Items
- Guarantee X Items

Ausserhalb des Scopes:

- Ban-Kombinationen fuer `FVX-ITEM-007`; optionaler spaeterer Follow-up, aber kein Test in diesem Block
- `FVX-ITEM-009` Balance Shop Prices / Cheap Rare Candies
- Field Items
- Pickup
- Held Items
- TM/HM/Tutor/Learnset
- Trainer, Wild, Evolution und Text/Menu
- ROMs, Saves, Emulator States, Builds, Logs, Output-ROMs und Tool-Binaries

Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes und Scriptdaten wurden nicht dokumentiert.

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/121_shop_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/123_shop_items_scope_diagnostics_candidate.md`
- `08_tests/randomizer/124_shop_items_shuffle_reload_smoke.md`
- `08_tests/randomizer/125_shop_items_random_reload_smoke.md`
- `08_tests/randomizer/126_shop_item_bans_scope_plan.md`
- `08_tests/randomizer/127_shop_items_random_ban_bad_reload_smoke.md`
- `08_tests/randomizer/128_shop_items_random_ban_regular_reload_smoke.md`
- `08_tests/randomizer/129_shop_items_random_ban_op_reload_smoke.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `08_tests/randomizer/README.md`
- `01_docs/references/tool-manifest.md`

## Read-only Suche

Verwendet wurden `rg`, `rg --files` und gezielte Dateiauszuege. Es gab keinen Build, keinen Randomizer-Lauf und keinen ROM-/Artefaktzugriff.

Suchbegriffe:

- `guaranteeEvolutionItems`
- `guaranteeXItems`
- `addEvolutionItemsToShops`
- `addXItemsToShops`
- `MainGameShops`
- `SkipShops`
- `Shop`
- `ShopItemsMod`
- `maybeRandomizeShops`
- `randomizeShopItems`
- `ItemRandomizer`
- `Settings`
- `GameRandomizer`
- `getShops`
- `setShops`
- `Gen3RomHandler`
- `RomHandler`
- `ItemList`
- `evolution`
- `X Attack`
- `X Defend`
- `X Speed`
- `X Accuracy`
- `Dire Hit`
- `Guard Spec`
- `RandomizerGUI`
- `Bundle.properties`

## Guarantee-Scope-Einschaetzung

`FVX-ITEM-008 Guarantee Evolution/X Items` ist ein eigener Shop-only Subscope nach `FVX-ITEM-007`.

Begruendung:

- Diagnose 124 belegt `FVX-ITEM-005 Shop Items Shuffle`.
- Diagnose 125 belegt `FVX-ITEM-006 Shop Items Random` ohne Guarantee-/Preisoptionen.
- Diagnose 127, 128 und 129 belegen `FVX-ITEM-007` fuer Ban Bad, Ban Regular und Ban OP jeweils einzeln, nicht fuer Ban-Kombinationen.
- Guarantee Evolution Items und Guarantee X Items veraendern den Shop-Random-Placement-Pool und die Placement-Policy, aber nicht den Preiswriter.
- Guarantee-Items gehoeren in den Shop-Item-Writer-Scope und sind nicht aus Field Items, Pickup oder Held Items abzuleiten.

`FVX-ITEM-008` bleibt bis zu eigenen Shop-only Write/Reload-Smokes `Write modelliert`.

## Relevante Codepfade

- `Settings.ShopItemsMod`: `UNCHANGED`, `SHUFFLE`, `RANDOM`.
- `Settings.guaranteeEvolutionItems`: GUI-/Settings-Flag fuer garantierte Evolution Items.
- `Settings.guaranteeXItems`: GUI-/Settings-Flag fuer garantierte X Items, inklusive Guard Spec. und Dire Hit.
- `RandomizerGUI`: liest und schreibt `shGuaranteeEvolutionItemsCheckBox` und `shGuaranteeXItemsCheckBox` in `Settings`.
- `Bundle.properties`: beschreibt `Guarantee Evolution Items` und `Guarantee X Items` als Shop-Guarantee-Optionen.
- `GameRandomizer.maybeRandomizeShops()`: ruft bei `ShopItemsMod.SHUFFLE` nur `shuffleShopItems()` auf; bei `ShopItemsMod.RANDOM` ruft es `randomizeShopItems()` auf. Danach laufen separat Preis-/Rare-Candy-Pfade, falls aktiv.
- `ItemRandomizer.randomizeShopItems()`: baut `possible`, `guaranteed`, kopiert Shops, erzeugt `newItems`, platziert Items und schreibt ueber `romHandler.setShops(...)`.
- `ItemRandomizer.setupGuaranteed()`: nimmt `romHandler.getEvolutionItems()` bei `guaranteeEvolutionItems=true` und `romHandler.getXItems()` bei `guaranteeXItems=true` in den Guaranteed-Set auf.
- `ItemRandomizer.setupNewItems(...)`: startet mit allen Guaranteed Items, reduziert die zu fuellende Shop-Slot-Anzahl um `guaranteed.size()`, entfernt Guaranteed Items aus `possible` und fuellt den Rest aus dem Random-Pool.
- `ItemRandomizer.placeNewItems(...)`: splittet Special Shops in MainGame und Non-MainGame; Non-MainGame-Special-Shops ueberspringen Guaranteed Items, MainGame-Special-Shops erhalten den Rest inklusive Guaranteed Items.
- `RomHandler.getEvolutionItems()` / `getXItems()`: Quellen der Guarantee-Sets.
- `AbstractRomHandler.getXItems()`: nutzt die globale X-Item-Liste, darunter Guard Spec., Dire Hit, X Attack, X Defend, X Speed und X Accuracy.
- `Gen3RomHandler.getShops()` / `setShops(...)`: liest `MainGameShops`, `SkipShops` und `ShopPointerOffsets`; schreibt ueber `DataRewriter<Shop>` mit terminierter Shopliste.

Hinweis: Im untersuchten Code gibt es keine separaten `addEvolutionItemsToShops`- oder `addXItemsToShops`-Methoden. Die Guarantee-Logik ist in `setupGuaranteed()`, `setupNewItems(...)` und `placeNewItems(...)` integriert.

## Wirkung nach ShopItemsMod

Die Guarantee-Optionen wirken nur, wenn `ShopItemsMod.RANDOM` aktiv ist.

Einordnung:

- `ShopItemsMod.UNCHANGED`: `maybeRandomizeShops()` ruft keinen Shop-Item-Randomizer auf; Guarantee-Flags haben keine Shoplisten-Wirkung.
- `ShopItemsMod.SHUFFLE`: `maybeRandomizeShops()` ruft `shuffleShopItems()` auf; `shuffleShopItems()` nutzt Guarantee-Flags nicht.
- `ShopItemsMod.RANDOM`: `maybeRandomizeShops()` ruft `randomizeShopItems()` auf; dort wirken Guarantee-Flags ueber `setupGuaranteed()` und `placeNewItems(...)`.

Folge fuer Tests:

- Guarantee-Smokes muessen mit `Settings.ShopItemsMod=RANDOM` laufen.
- Ein Shuffle + Guarantee Smoke waere nicht aussagekraeftig fuer `FVX-ITEM-008`.
- Preis-/Rare-Candy-Optionen bleiben deaktiviert, damit `FVX-ITEM-009` nicht vermischt wird.

## Placement-/Policy-Befund

- `Gen3RomHandler.getShops()` setzt `Shop.isMainGame` ueber `MainGameShops` und `Shop.isSpecialShop` ueber `!SkipShops.contains(i)`.
- `ItemRandomizer.placeNewItems(...)` betrachtet nur Shops mit `isSpecialShop=true`.
- SkipShops bleiben dadurch preserve-only, solange sie nicht als Special Shops markiert sind.
- Non-MainGame-Special-Shops werden zuerst gefuellt und ueberspringen Guaranteed Items.
- MainGame-Special-Shops werden danach gefuellt und erhalten die verbleibenden Items inklusive Guaranteed Items.
- Guarantee-Items ersetzen vorhandene Shop-Slots im Shop-Random-Placement; die Methode verlaengert Shoplisten nicht.
- Listenlaengen sollten bei Guarantee Evolution und Guarantee X stabil bleiben, solange `guaranteed.size()` die verfuegbare Special-Shop-Slotanzahl nicht uebersteigt.
- `setShops(...)` schreibt trotzdem terminierte Listen ueber `DataRewriter<Shop>`; Reload bleibt Pflichtkriterium.
- Preislogik bleibt unberuehrt, solange `balanceShopPrices=false` und `addCheapRareCandiesToShops=false` gesetzt sind.

## Risiken / Blocker

- MainGameShop-Placement: Guaranteed Items muessen tatsaechlich in MainGame-Special-Shops landen und nicht in Non-MainGame- oder Skip-Shops ausweichen.
- Slotkapazitaet: Wenn das Guaranteed-Set groesser als die verfuegbare Special-Shop-Slotzahl ist, kann `setupNewItems(...)` negative Restslots erzeugen oder `placeNewItems(...)` mit uebrigen Items fehlschlagen.
- Listenlaengen: Die aktuelle Guarantee-Logik ersetzt Slots und sollte Laengen erhalten; Reload muss `shopItemsTotal`, min/max Laenge und Laengenmismatches pruefen.
- Terminatoren: Auch bei gleicher Laenge muss der Gen3 terminierte `u16`-Stream reloadstabil bleiben.
- `DataRewriter` / Repointing: `setShops(...)` kann repointen; Reload muss Struktur, Inhalt und Preserve-Policy nachweisen.
- SkipShop-Verletzung: SkipShops duerfen nicht veraendert werden.
- Special-Shop-Policy: Nur Special Shops werden geschrieben; MainGame-Special-Shop-Metriken muessen getrennt beobachtet werden.
- Preislogik: Preistabelle muss unveraendert bleiben; `priceTableTouched=false` und `priceReloadMismatches=0` sind Pflicht.
- Kombinationen: Guarantee Evolution + Guarantee X erst nach Einzel-Smokes; Ban-Kombinationen bleiben eigener optionaler Follow-up.

## Empfohlene Testreihenfolge

1. Guarantee Evolution Items Smoke.
2. Guarantee X Items Smoke.
3. Kombination Guarantee Evolution + Guarantee X nur, falls beide Einzel-Smokes reloadstabil sind.

Empfohlener erster Smoke:

- `Settings.ShopItemsMod=RANDOM`
- `guaranteeEvolutionItems=true`
- `guaranteeXItems=false`
- `banBadRandomShopItems=false`
- `banRegularShopItems=false`
- `banOPShopItems=false`
- `balanceShopPrices=false`
- `addCheapRareCandiesToShops=false`

## Spaetere Smoke-Metriken

Pflichtmetriken fuer Guarantee-Smokes:

```text
candidateLoaded
smokeExecuted
saveSuccessful
logSuccessful
outputRomExists
logNonEmpty
reloadSuccessful
shopCountBefore
shopCountAfter
shopCountReload
mainGameShopCountBefore
mainGameShopCountAfter
mainGameShopCountReload
skippedShopCountBefore
skippedShopCountAfter
skippedShopCountReload
specialShopCountBefore
specialShopCountAfter
specialShopCountReload
shopItemsTotalBefore
shopItemsTotalAfter
shopItemsTotalReload
minShopLengthBefore
minShopLengthAfter
minShopLengthReload
maxShopLengthBefore
maxShopLengthAfter
maxShopLengthReload
terminatorModelStableAfter
terminatorModelStableReload
shopLengthMismatchesAfter
shopLengthMismatchesReload
shopItemReloadMismatches
skippedShopItemMismatchesAfter
skippedShopItemMismatchesReload
specialShopPolicyMismatches
guaranteedEvolutionItemsPresent
guaranteedEvolutionItemsMissing
guaranteedXItemsPresent
guaranteedXItemsMissing
guaranteePlacementShopCount
invalidShopItemWrites
unloadedShopItemWrites
fallbackShopItemWrites
placeholderShopItemWrites
priceTableTouched=false
priceReloadMismatches=0
fieldItemScopeChanged=false
pickupScopeChanged=false
heldItemScopeChanged=false
exceptionClass
stacktrace
```

Zusatzmetriken empfohlen:

```text
evolutionItemsSetSize
xItemsSetSize
mainGameSpecialShopCount
mainGameSpecialShopSlots
nonMainGameSpecialShopCount
nonMainGameSpecialShopSlots
guaranteeSlotCapacitySufficient
guaranteedItemsInSkippedShops
```

## Feature-Status

- `FVX-ITEM-005 Shop Items Shuffle`: bleibt `GUI-kompatibel` im getesteten Shop-only Scope.
- `FVX-ITEM-006 Shop Items Random`: bleibt `GUI-kompatibel` im getesteten Shop-only Scope.
- `FVX-ITEM-007 Shop Item Bans`: Ban Bad, Ban Regular und Ban OP sind jeweils einzeln `GUI-kompatibel`; Ban-Kombinationen bleiben optional separat.
- `FVX-ITEM-008 Guarantee Evolution/X Items`: bleibt bis Smoke `Write modelliert`.
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`: bleibt separat und wird nicht hochgestuft.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-shop-guarantee-evolution-items-reload-smoke`: Shop-only Write/Reload-Smoke fuer `ShopItemsMod.RANDOM` mit nur `guaranteeEvolutionItems=true`.
