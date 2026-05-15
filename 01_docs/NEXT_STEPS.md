# 2026-05-15 - Next: Wild Encounters read-only candidate diagnostic

Recommended next branch: `test/upr-fvx-cfru-dpe-wild-encounters-scope-diagnostics`.

Goal: scan Wild Encounter areas and slots read-only, classify encounter types and validate SpeciesSet identity mapping without writes, builds or Randomizer runs.

Keep out of scope: Wild Held Items, Trainer Pokemon, Starters, Static/Gift Pokemon, Field Items, Pickup, Shops and all non-Wild-Encounter features.

# 2026-05-15 - Next: next major Randomizer feature scope

Held Items scope is closed in the tested CFRU/DPE Gen9-BPRE scope after Diagnose 147.

Recommended next branch: create a new analysis branch for the next major Randomizer feature scope.

Keep out of scope unless explicitly reopened: Wild Held Items, Trainer Held Items, Starter Held Items, Field Items, Pickup, Shops and prior completed item scopes.

# 2026-05-15 - Next: Starter Held Items + Ban Bad

Recommended next branch: `test/upr-fvx-cfru-dpe-starter-held-items-ban-bad-reload-smoke`.

Goal: test Starter Held Items with `banBadRandomStarterHeldItems=true` after Diagnose 146 confirmed Starter Held Items reload stability without Ban Bad.

Keep out of scope: Wild Held Items, Trainer Held Items, Field Items, Pickup, Shops and non-Held-Item randomizer work.

# 2026-05-15 - Next: Starter Held Items or optional Trainer filter combinations

Recommended next branch: `test/upr-fvx-cfru-dpe-starter-held-items-reload-smoke` if Boss/Important filter combinations are not required.

Optional alternative: plan Boss/Important Trainer Held Item filter combinations only if product coverage requires them.

Keep out of scope for Starter: Wild Held Items, Trainer Held Items, Field Items, Pickup, Shops and non-Held-Item randomizer work.

# 2026-05-15 - Next: Trainer Held Item filter smoke

Recommended next branch: `test/upr-fvx-cfru-dpe-trainer-held-items-regular-filters-reload-smoke`.

Goal: test Regular Trainer Held Items with `Consumable Only`, `Sensible Items` and `Highest Level Only` enabled, while preserving Boss, Important, `shouldNotGetBuffs`, Wild, Starter, Field, Pickup and Shop scopes.

Fallback: if the combined filter smoke is too broad, split into Consumable-only, Sensible-only and Highest-Level-only smokes.

# 2026-05-15 - Next: Trainer Held Item filters or Starter Held Items

Recommended next branch: `analysis/upr-fvx-cfru-dpe-trainer-held-items-filters-scope-plan` if filter coverage is required, or `test/upr-fvx-cfru-dpe-starter-held-items-reload-smoke` to move to Starter Held Items.

Goal: decide whether Consumable/Sensible/Highest-Level Trainer Held Item filter options need separate coverage before moving to Starter Held Items.

Keep out of scope: Wild Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer work.

Required checks for any next smoke: save/log/output/reload success, class/preserve counters `0`, no invalid/unloaded/fallback/placeholder writes, and cross-scope isolation.

# 2026-05-15 - Next: Regular Trainer Held Items smoke

Recommended next branch: `test/upr-fvx-cfru-dpe-trainer-held-items-regular-reload-smoke`.

Goal: test Regular Trainer Held Items only, after Diagnose 142 confirmed Important Trainer Held Items reload stability.

Keep out of scope: Boss/Important expansion beyond the selected class, Consumable/Sensible/Highest-Level filters, Starter Held Items, Wild Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer work.

Required checks: save/log/output/reload success, Regular Trainer held item reload mismatches 0, Boss/Important/shouldNotGetBuffs preserve counters 0, no invalid/unloaded/fallback/placeholder writes, and Wild/Starter/Field/Pickup/Shop isolation.

# 2026-05-15 - Next: Important Trainer Held Items smoke

Recommended next branch: `test/upr-fvx-cfru-dpe-trainer-held-items-important-reload-smoke`.

Goal: test Important Trainer Held Items only, after Diagnose 141 confirmed Boss Trainer Held Items reload stability.

Keep out of scope: Boss/Regular expansion beyond the selected class, Consumable/Sensible/Highest-Level filters, Starter Held Items, Wild Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer work.

Required checks: save/log/output/reload success, Important Trainer held item reload mismatches 0, Boss/Regular/shouldNotGetBuffs preserve counters 0, no invalid/unloaded/fallback/placeholder writes, and Wild/Starter/Field/Pickup/Shop isolation.

# 2026-05-15 - Next: Trainer Held Items scope

Recommended next branch: `analysis/upr-fvx-cfru-dpe-trainer-held-items-scope-plan` or, if no extra planning block is needed, `test/upr-fvx-cfru-dpe-trainer-held-items-boss-reload-smoke`.

Goal: move from completed Wild/Encounter Held Items coverage to Trainer Held Items, starting with a narrow Boss Trainers-only scope without Consumable/Sensible/Highest-Level filters.

Keep out of scope: Starter Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer work.

Required checks for a smoke: save/log/output/reload success, trainer held item reload mismatches 0, preserve `shouldNotGetBuffs`, no invalid/unloaded/fallback/placeholder writes, and Wild/Starter/Field/Pickup/Shop isolation.

# 2026-05-15 - Next: Wild Held Items Ban Bad smoke

Recommended next branch: `test/upr-fvx-cfru-dpe-wild-held-items-ban-bad-reload-smoke`.

Goal: test Wild/Encounter Held Items with `banBadRandomWildPokemonHeldItems=true` only, after Diagnose 139 confirmed the no-Ban-Bad Wild/Encounter writer reloads with `wildHeldItemReloadMismatches=0`.

Keep out of scope: Trainer Held Items, Starter Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer work.

Required checks remain: save/log/output/reload success, no invalid/unloaded/fallback/placeholder writes, `badWildHeldItemWrites=0`, and scope isolation for Trainer/Starter/Field/Pickup/Shop.

# Next Steps Update - 2026-05-15 - Wild/Encounter Held Items smoke next

Aktueller Fokus:

- Diagnose 138 confirms read-only Held Items candidate structure for Wild/Encounter, Trainer and Starter paths.
- Wild/Encounter Held Items are the first recommended write/reload smoke because the Species/BaseStats structure is readable and should be tested before Trainer or Starter Held Items.
- Fallback/placeholder held items exist in the current read-only inventory and must be measured as write-safety counters.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-wild-encounter-held-items-reload-smoke`

Ziel des Folgeblocks:

- Test only Wild/Encounter Held Items without Ban Bad.
- Keep Trainer Held Items, Starter Held Items, Field Items, Pickup, Shops and all other randomizer scopes disabled.

# Next Steps Update - 2026-05-15 - Held Items diagnostics next

Aktueller Fokus:

- Diagnose 137 plans Held Items as a separate scope after the tested Shop Items scope was closed by Diagnose 136.
- Held Items are split into Wild/Encounter, Trainer and Starter subscopes.
- No Held-Item feature is promoted by the plan; a read-only candidate diagnostic is required before any Held-Items write smoke.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-held-items-scope-diagnostics`

Ziel des Folgeblocks:

- Read-only Held-Items candidate diagnostic for Species/BaseStats held items, TrainerPokemon held items and Starter held items.
- No Field Items, Pickup, Shops, Trainer Randomization, Wild Randomization, Evolution, Learnset, TM/HM/Tutor, Move, Ability, TypeChart, Palette, Graphics or Text/Menu work.

# Next Steps Update - 2026-05-15 - Shop Items scope closed

Aktueller Fokus:

- Diagnose 136 closes the tested Shop Items scope after the Balance Prices + Cheap Rare Candies combination passed reload.
- FVX-ITEM-005, FVX-ITEM-006, the individually tested FVX-ITEM-007 Ban flags, the individually tested FVX-ITEM-008 Guarantee flags, and FVX-ITEM-009 individual plus combination price/Rare-Candy paths are GUI-compatible in the tested Shop-only CFRU/DPE Gen9-BPRE scope.
- Ban combinations and Evolution+X combination remain optional regression follow-ups, not blockers for closing the tested Shop scope.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-held-items-scope-diagnostics-plan`

Ziel des Folgeblocks:

- Held Items als naechsten separaten Item-writer Scope read-only planen.
- Keine Shops, Field Items, Pickup, Encounter/Trainer/Starter Held Items-Ausweitung ohne eigene Scope-Trennung, keine TM/HM/Tutor/Learnset-, Wild-, Trainer-, Evolution-, Text/Menu-, Palette/Graphics-, MoveData/MoveNames- oder TypeChart-Arbeit.

# Next step - 2026-05-15

- Minimal decision: either run a narrow Balance Prices + Cheap Rare Candies combination smoke or close the current Shop Items scope.
- Do not treat the two individual FVX-ITEM-009 passes as automatic combination coverage.
- Keep Ban combinations, Evolution+X combination, Field Items, Pickup and Held Items separate unless explicitly scoped.

# Next step - 2026-05-15

- Minimal next branch: `test/upr-fvx-cfru-dpe-shop-cheap-rare-candies-reload-smoke`.
- Scope: Shop-only Cheap Rare Candies with `ShopItemsMod.UNCHANGED`, `balanceShopPrices=false`, `addCheapRareCandiesToShops=true`; no Bans, no Guarantees, no Field/Pickup/Held Items.
- Measure Shop-list growth, Rare Candy price reload, terminators, skipped-Shop policy, and foreign-scope stability.

# Next step - 2026-05-15

- Recommended next branch: `test/upr-fvx-cfru-dpe-shop-balance-prices-reload-smoke`.
- Scope: Shop-only Balance Shop Prices with `ShopItemsMod.UNCHANGED`, no Cheap Rare Candies, no Ban combinations, no Guarantee combination, no Field/Pickup/Held Items.
- Measure price table read/write/reload stability before any Rare-Candy Shop-list growth smoke.

# Next step - 2026-05-15

- Minimal decision: either run a narrow Evolution+X combination smoke for FVX-ITEM-008 or move to the FVX-ITEM-009 prices/Cheap Rare Candies scope plan.
- Do not treat the individual Guarantee Evolution and Guarantee X passes as automatic combination coverage.
- Keep Ban combinations and price/Rare-Candy logic separate unless explicitly scoped.

# Next step - 2026-05-15

- Minimal next step: run a Shop-only Guarantee X Items Write/Reload-Smoke for FVX-ITEM-008 if the same candidate source and safety constraints are explicitly released.
- Do not combine Guarantee Evolution + X until both single-feature smokes are reload-stable.
- Keep FVX-ITEM-009 Balance Shop Prices/Cheap Rare Candies separate.

# 2026-05-15 - Naechster Schritt nach Diagnose 130

- Empfohlen: `test/upr-fvx-cfru-dpe-shop-guarantee-evolution-items-reload-smoke`.
- Scope: nur `ShopItemsMod.RANDOM + guaranteeEvolutionItems=true`; keine Guarantee X Items, keine Ban-Kombinationen, keine Preis- oder Cheap-Rare-Candy-Optionen.
- Pflicht: MainGame-Special-Placement, SkipShop-Preserve, Laengen/Terminatoren, Reload und Preis/Field/Pickup/Held-Fremdscopes messen.

# 2026-05-15 - Naechster Schritt nach Diagnose 129

- Entscheiden, ob `FVX-ITEM-007` Ban-Kombinationsdeckung braucht oder ob direkt `FVX-ITEM-008 Guarantee Evolution/X Items` geplant wird.
- Wenn Kombinationen getestet werden: nur nach separater Scope-Entscheidung und ohne Preis/Rare-Candy-Optionen.
- Nicht ausweiten auf `FVX-ITEM-009`, Field Items, Pickup oder Held Items.

# 2026-05-15 - Naechster Schritt nach Diagnose 128

- Empfohlen: Shop Random + Ban OP als separaten Subscope planen oder smoken.
- Voraussetzung: OP-Shop-Item-Pool bleibt klar klassifizierbar und getrennt von Ban Bad/Regular.
- Nicht ausweiten auf Ban-Kombinationen, Guarantee Evolution/X Items, Preise, Cheap Rare Candies, Field Items, Pickup oder Held Items.

# 2026-05-15 - Naechster Schritt nach Diagnose 127

- Empfohlen: Shop Random + Ban Regular als separaten Subscope planen oder smoken.
- Voraussetzung: Regular-Shop-Item-Pool bleibt klar getrennt von Ban Bad und OP-Ban.
- Nicht ausweiten auf OP-Ban-Kombinationen, Guarantee Evolution/X Items, Preise, Cheap Rare Candies, Field Items, Pickup oder Held Items.

# Next Steps Update - 2026-05-15 - Shop Random Ban Bad smoke next

Aktueller Fokus:

- Diagnose 126 plans `FVX-ITEM-007 Shop Item Bans` as a Shop-only sub-scope.
- Ban flags act only in `ShopItemsMod.RANDOM` through `ItemRandomizer.randomizeShopItems()` / `setupPossible()`.
- First recommended Ban test is Ban Bad only because Diagnose 125 already provides `allowedShopItemPoolSize=536` and `nonBadShopItemPoolSize=485`.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-shop-items-random-ban-bad-reload-smoke`

Ziel des Folgeblocks:

- Run only Shop Random + `banBadRandomShopItems=true`.
- Keep `banRegularShopItems=false`, `banOPShopItems=false`, Guarantee Evolution/X Items, Balance Prices, Cheap Rare Candies, Field Items, Pickup and Held Items out of scope.
- Required focus metrics: save/log/output/reload, `shopItemReloadMismatches=0`, skipped-shop preservation, `badShopItemWrites=0`, `banBadShopItemPoolCandidates=51`, price unchanged and foreign scopes unchanged.

# Next Steps Update - 2026-05-15 - Shop Item Bans next

Aktueller Fokus:

- Diagnose 125 confirms `FVX-ITEM-006 Shop Items Random` as reload-stable in the Shop-only CFRU/DPE Gen9-BPRE scope.
- Stable criteria: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `shopItemReloadMismatches=0`, skipped-shop mismatches `0`, price reload mismatches `0`, and Field/Pickup/Held scope changes `false`.
- `FVX-ITEM-007..009` remain separate and are not upgraded by the Random smoke.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-shop-item-bans-scope-plan`

Ziel des Folgeblocks:

- Plan `FVX-ITEM-007 Shop Item Bans` as the next Shop-only sub-scope.
- Keep Guarantee Evolution/X Items, Balance Prices, Cheap Rare Candies, Field Items, Pickup and Held Items out of scope.
- Decide whether the next executable smoke should test Ban Bad first, or split Bad/Regular/OP ban policies into separate smokes.

# Next Steps Update - 2026-05-15 - Shop Random smoke next

Aktueller Fokus:

- Diagnose 124 confirms `FVX-ITEM-005 Shop Items Shuffle` as reload-stable in the Shop-only CFRU/DPE Gen9-BPRE scope.
- Stable criteria: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `shopItemReloadMismatches=0`, skipped-shop mismatches `0`, price reload mismatches `0`, and Field/Pickup/Held scope changes `false`.
- `FVX-ITEM-006..009` remain separate and are not upgraded by the Shuffle smoke.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-shop-items-random-reload-smoke`

Ziel des Folgeblocks:

- Run only `FVX-ITEM-006 Shop Items Random` as a Shop-only Write/Reload-Smoke.
- Keep Shop Bans, Guarantee Evolution/X Items, Balance Prices, Cheap Rare Candies, Field Items, Pickup and Held Items out of scope.
- Reuse the Diagnose-123/124 structure criteria: counts, lengths, terminators, skipped shops, special policy, prices and foreign scopes must stay stable.

# Next Steps Update - 2026-05-15 - Shop Shuffle smoke next

Aktueller Fokus:

- Diagnose 123 confirms a stable read-only Shop structure for the approved CFRU/DPE Gen9-BPRE candidate.
- Shop metrics are stable enough for the next minimal write/reload test: `shopScanSuccessful=true`, `shopCount=23`, `shopItemsTotal=157`, `terminatorModelStable=true`, `shopLengthMismatch=0`, invalid/unloaded/fallback/placeholder Shop items all `0`.
- `dataRewriterOrRepointingRisk=true` remains a required Smoke criterion because `Gen3RomHandler.setShops(...)` uses `DataRewriter<Shop>`.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-shop-items-shuffle-reload-smoke`

Ziel des Folgeblocks:

- Run only `FVX-ITEM-005 Shop Items Shuffle` as a Shop-only Write/Reload-Smoke.
- Prove stable Shop count, item total, min/max length, terminators, preserved skipped shops, Special/MainGame policy and no price, Field, Pickup or Held scope changes.
- Do not include Shop Random, Shop Bans, Guarantee Evolution/X Items, Balance Prices, Cheap Rare Candies, Field Items, Pickup, Held Items, TM/HM/Tutor/Learnset, Trainer, Wild, Evolution, Text/Menu, Palette/Graphics, MoveData/MoveNames or TypeChart.

# Next Steps Update - 2026-05-15 - Shop Items candidate needed

Aktueller Fokus:

- Diagnose 122 is blocked/preflight because no explicitly approved local CFRU/DPE Gen9-BPRE candidate source was provided for the Shop read-only scan.
- The codepath model remains valid: Shops are pointer-list, terminator, length, `DataRewriter`/repointing and price-adjacent scope, separate from Field Items, Pickup and Held Items.
- Do not run Shop Shuffle, Random, Ban, Guarantee or Price smokes before a successful read-only Shop candidate diagnostic.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-candidate`

Ziel des Folgeblocks:

- Use an explicitly approved local CFRU/DPE Gen9-BPRE candidate source.
- Read-only scan only Shops and report aggregated `candidateLoaded`, `shopScanSuccessful`, `shopCount`, `mainGameShopCount`, `skippedShopCount`, `specialShopCount`, `emptyShopCount`, `shopItemsTotal`, min/max length, terminator stability, item-safety counters and price-table untouched status.
- Keep Field Items, Pickup, Held Items, prices, Shop writes, builds, Randomizer writes/saves and private artefact documentation out of scope.

# Next Steps Update - 2026-05-15 - Shop Items scope diagnostics next

Aktueller Fokus:

- Diagnose 121 confirms Shops as the next separate CFRU/DPE Gen9-BPRE Item writer scope after Field Items and Pickup.
- `FVX-ITEM-005..009` remain Shop-only and are not upgraded by Field Items, Pickup or Held Item results.
- `Gen3RomHandler.setShops(...)` uses `DataRewriter<Shop>`, so Shop writes must treat terminators, lengths, pointers, skipped/special/main-game policy and price fields as explicit reload criteria.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics`

Ziel des Folgeblocks:

- Run a sanitized read-only Shop candidate diagnostic.
- Report only aggregated counters: `candidateLoaded`, `shopScanSuccessful`, `shopCount`, `mainGameShopCount`, `skippedShopCount`, `specialShopCount`, item counts, terminator/length mismatches, invalid/unloaded/fallback/placeholder/bad items, skipped-shop preservation expectations and price-table readability.
- Do not run a Shop write smoke yet and keep Field Items, Pickup, Held Items, TM/HM/Tutor/Learnset, Trainer, Wild, Evolution, Text/Menu, Palette/Graphics, MoveData/MoveNames and TypeChart out of scope.

# Next Steps Update - 2026-05-15 - Shops-only scope next

Current recommended branch:

- `analysis/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-plan`

Goal:

- Plan Shops as the next separate Item writer scope after Field Items and Pickup.
- Keep Field Items, Pickup, Encounter Held Items, Trainer Held Items and Starter Held Items out of the Shop plan.
- Start read-only: identify Shop item lists, terminators, lengths, special shops, price handling, bad-item policy and CFRU/DPE Gen9-BPRE risks before any writer smoke.

Current Pickup status:

- `FVX-ITEM-010 Pickup Items Random / Ban Bad Items` is `GUI-kompatibel` for the tested Pickup-only Random scope with `banBadRandomPickupItems=false` and `true`.
- UPR-FVX remains pinned to `a2373888ad17145f270ebf6ff17303af41aa86eb`.

# Next Steps Update - 2026-05-15 - Pickup Items Ban Bad smoke next

Current recommended branch:

- `test/upr-fvx-cfru-dpe-pickup-items-random-ban-bad-reload-smoke`

Goal:

- Run a sanitized Pickup-only Write/Reload-Smoke for `FVX-ITEM-010 Pickup Items Random` with `Settings.PickupItemsMod.RANDOM` and `banBadRandomPickupItems=true`.
- Reuse UPR-FVX `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- Keep scope limited to Pickup Items; no Field Items, Shops, Held Items, TM/HM/Tutor/Learnset, Scriptparser, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution or Text/Menu work.

Expected focus metrics:

- Preserve Diagnose 118 reload baseline: `pickupItemsTotalReload=16`, `pickupItemReloadMismatches=0`, `pickupProbabilityMismatches=0`, `pickupReloadLocatorRegression=false`.
- Add Ban-Bad assertions: `badPickupItemWrites=0`, `pickupBadItemPoolCandidates=51`, `pickupBadItemPoolExcluded=51`, `pickupPoolNonBadSize=485`.
- Confirm `fieldItemScopeChanged=false`, `shopItemScopeChanged=false`, and `heldItemScopeChanged=false`.

# Next Steps Update - 2026-05-15 - Pickup Ban Bad next

Aktueller Fokus:

- Diagnose 118 fixes and verifies the Pickup reload locator for `FVX-ITEM-010 Pickup Items Random` with `banBadRandomPickupItems=false`.
- `FVX-ITEM-010 Pickup Items Random` is now GUI-compatible only in that narrow no-Ban-Bad Pickup-only scope.
- Pickup Ban Bad remains untested and separate.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-pickup-items-ban-bad-scope-plan`

Ziel des Folgeblocks:

- Read-only planen, wie Pickup Ban Bad fuer `FVX-ITEM-010` getestet werden soll.
- Danach erst einen Pickup-only Random smoke mit `banBadRandomPickupItems=true` vorbereiten.
- Keine Field Items, Shops, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu oder Scriptparser-Arbeit.

# Next Steps Update - 2026-05-15 - Pickup reload locator fix next

Aktueller Fokus:

- Diagnose 116 blocks `FVX-ITEM-010 Pickup Items Random` after successful save/log/output/reopen because fresh reload cannot locate the Pickup table.
- Diagnose 117 narrows the likely cause to the content-based `PickupTableStartLocator`: the current handler keeps a cached table offset after write, but a fresh handler searches for the old item-ID pattern, which Pickup Random has changed.
- `FVX-ITEM-010` remains `Write modelliert` / reload-blocked.
- Pickup Ban Bad remains blocked until Random without Ban Bad reloads stably.

Naechster empfohlener Minimalblock:

- `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`

Ziel des Folgeblocks:

- Minimalen UPR-FVX-Fix fuer eine reloadstabile Pickup-Table-Lokalisierung vorbereiten.
- Bevorzugt eine stabile ROM-Entry-Adresse oder nicht item-inhaltsabhaengige Referenz im sicheren CFRU/DPE-/FRLG-Gate nutzen.
- Den bestehenden `PickupTableStartLocator` nur als klassischen Fallback erhalten.
- Danach Pickup-only Random-Smoke mit `banBadRandomPickupItems=false` wiederholen.
- Keine Pickup Ban Bad, Field Items, Shops, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu oder Scriptparser-Arbeit.

# Next Steps Update - 2026-05-15 - Pickup Items reload locator blocker

Aktueller Fokus:

- Diagnose 116 blockiert `FVX-ITEM-010 Pickup Items Random` nach erfolgreichem Save/Log/Output beim Reload-Locator.
- Der frische Reload findet die Pickup-Tabelle nicht mehr: `pickupLocatorSuccessful=false`, `pickupItemsTotalReload=0`.
- Vor und direkt nach Write bleibt der aktive Handler stabil: `pickupItemsTotalBefore=16`, `pickupItemsTotalAfter=16`.
- Field Items, Shops und Held Items blieben unveraendert.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-pickup-items-reload-locator-blocker-plan`

Ziel des Folgeblocks:

- Read-only klaeren, warum `PickupTableStartLocator` nach `PickupItemsMod.RANDOM` nicht mehr greift.
- Einen engen spaeteren Fix-Scope fuer `Gen3RomHandler.getPickupItems()` / `setPickupItems(...)` oder einen privaten Pickup-Table-Helper planen.
- Keine Ban-Bad-Pickup-Arbeit, keine Field Items, keine Shops, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Arbeit.

# Next Steps Update - 2026-05-15 - Pickup Items random smoke next

Aktueller Fokus:

- Diagnose 115 hat Pickup Items read-only klassifiziert.
- Locator, Count, Entry-Size und Probability-Modell sind fuer den Kandidaten stabil: `pickupLocatorSuccessful=true`, `pickupItemsTotal=16`, `pickupExpectedCount=16`, `pickupEntrySize=4`, `pickupProbabilityModelStable=true`.
- Item-ID-Sicherheit ist fuer den aktuellen Pickup-Scope stabil: `pickupInvalidItemIds=0`, `pickupUnloadedItemIds=0`, `pickupFallbackItems=0`, `pickupPlaceholderItems=0`.
- Ban Bad bleibt separat, weil `pickupBadItemPoolCandidates=51` und `pickupBadItemPoolExcluded=51` eine eigene Poolfilter-Wirkung zeigen.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-pickup-items-random-reload-smoke`

Ziel des Folgeblocks:

- Nur `FVX-ITEM-010 Pickup Items Random` mit `banBadRandomPickupItems=false` als Write-/Reload-Smoke testen.
- Erwartet: Save/Log/Output/Reload true, `pickupItemsTotalBefore/After/Reload=16`, `pickupItemReloadMismatches=0`, Tabellenlaenge und Probability-Modell stabil, keine invalid/unloaded/fallback/placeholder Writes.
- Keine Field-Items-Arbeit, keine Shops, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Arbeit.

# Next Steps Update - 2026-05-15 - Pickup Items diagnostics next

Aktueller Fokus:

- Field Items `FVX-ITEM-001..004` sind im getesteten engen Field-Items-only Scope abgeschlossen.
- Pickup Items sind als naechster getrennter Item-Writer-Scope geplant.
- Diagnose 114 empfiehlt zuerst eine read-only Pickup-Kandidatendiagnose, bevor ein Write-/Reload-Smoke gestartet wird.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics`

Ziel des Folgeblocks:

- Nur Pickup Items read-only klassifizieren: Locator, Tabellenlaenge, Entry-Size, Probability-Modell, Common/Rare-Hinweise, valide/geladene Item-IDs, Bad-/Fallback-/Placeholder-/TM-Pool-Sicherheit.
- Keine Pickup-Write-/Randomizer-Ausfuehrung, kein Build, keine Codeaenderung.
- Keine Field-Items-Arbeit, keine Shops, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Arbeit.

# Next Steps Update - 2026-05-15 - Field Items complete in tested scope

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` ist im engen allowed-slot Scope `GUI-kompatibel`.
- `FVX-ITEM-002 Field Items Random` ist im engen Field-Items-only Scope `GUI-kompatibel`, inklusive `banBadRandomFieldItems=true` fuer `FieldItemsMod.RANDOM`.
- `FVX-ITEM-003 Field Items Random even distribution` ist im engen Field-Items-only Scope `GUI-kompatibel`, inklusive `banBadRandomFieldItems=true` fuer `FieldItemsMod.RANDOM_EVEN`.
- `FVX-ITEM-004 Field Items Ban Bad Items` ist fuer Field Items Random und Random Even `GUI-kompatibel`.
- Shops, Pickup und Held Items bleiben nicht hochgestuft und muessen getrennt geplant werden.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics-plan`

Ziel des Folgeblocks:

- Pickup als separaten Item-Writer-Scope read-only planen.
- Keine Field-Items-Nacharbeit, keine Shops, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Arbeit.

# Next Steps Update - 2026-05-15 - Field Items Random Even Ban Bad smoke next

Aktueller Fokus:

- Diagnose 112 confirms a Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=true`.
- Save/log/output/reload succeeded, `fieldItemReloadMismatches=0`, Required Field TMs stayed complete, and `badFieldItemWrites=0`.
- `FVX-ITEM-004` is tested for `FieldItemsMod.RANDOM`, but not fully GUI-compatible because Random Even + Ban Bad remains unsmoked and the 75er Ban-Bad baseline from Diagnose 111 was not reproduced in this run.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke`: sanitized Field-Items-only smoke for `FVX-ITEM-003 Field Items Random even distribution` with `banBadRandomFieldItems=true`.


Aktueller Fokus:

- Diagnose 111 plans `FVX-ITEM-004 Field Items Ban Bad Items` read-only.
- `banBadRandomFieldItems` affects the Non-TM Field-Items random pool only; TM slots and Required Field TMs stay in the separate TM path.
- Baseline Ban-Bad count from Diagnose 100: `badFieldItems=75` / `badItemBanCandidates=75`.
- `FVX-ITEM-004` remains `Write modelliert` until at least the first Ban-Bad reload smoke passes.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `test/upr-fvx-cfru-dpe-field-items-random-ban-bad-reload-smoke`: sanitized Field-Items-only smoke for `FVX-ITEM-002 Field Items Random` with `banBadRandomFieldItems=true`; keep Random Even + Ban Bad separate afterward.

# Next Steps Update - 2026-05-15 - Field Items Ban Bad scope plan next

Aktueller Fokus:

- Diagnose 110 confirms `FVX-ITEM-003 Field Items Random even distribution` as `GUI-kompatibel` in the narrow Field-Items-only scope with `banBadRandomFieldItems=false`.
- Confirmed counters include `fieldItemReloadMismatches=0`, `apiTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`, `randomTmPoolDeficit=0`, and `requiredFieldTMMissingAfter=0`.
- `FVX-ITEM-004 Field Items Ban Bad Items` remains `Write modelliert` and should be planned separately before activation.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `analysis/upr-fvx-cfru-dpe-field-items-ban-bad-scope-plan`: read-only plan for `FVX-ITEM-004 Field Items Ban Bad Items`, preserving the same allowed-slot, TM/Non-TM, Required-TM and API-TM-slot criteria.

# Next Steps Update - 2026-05-15 - Field Items Random Even smoke next

Aktueller Fokus:

- Diagnose 109 confirms `FVX-ITEM-002 Field Items Random` as `GUI-kompatibel` in the narrow Field-Items-only scope with `banBadRandomFieldItems=false`.
- Confirmed counters include `fieldItemReloadMismatches=0`, `apiTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`, `randomTmPoolDeficit=0`, and `requiredFieldTMMissingAfter=0`.
- `FVX-ITEM-003 Field Items Random even distribution` remains `Write modelliert` and should be tested separately next.
- `FVX-ITEM-004 Ban Bad Items` remains separate and inactive.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `test/upr-fvx-cfru-dpe-field-items-random-even-reload-smoke`: sanitized Field-Items-only smoke for `FVX-ITEM-003` without Ban Bad Items, preserving the same allowed-slot, TM/Non-TM, Required-TM and API-TM-slot criteria.

# Next Steps Update - 2026-05-15 - Field Items API TM-slot reload smoke next

Aktueller Fokus:

- UPR-FVX PR #37 prepares the narrow CFRU/DPE Field-Items API TM-slot scope fix.
- Workspace pins `02_external/upr-fvx` to `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- `FVX-ITEM-002` remains below GUI-compatible until a separate Field-Items-only reload smoke confirms `randomTmNeededSlots=28`, `apiTmFieldItemSlots=28`, and `fieldItemReloadMismatches=0`.

Empfohlener naechster Branch:

- `test/upr-fvx-cfru-dpe-field-items-api-tm-slot-reload-smoke`

Ziel:

- Run a sanitized Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=false` on UPR-FVX `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Keep Random Even, Ban Bad Items, Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Scriptparser, Palette, MoveData, Trainer, Wild, Evolution and Text/Menu out of scope.

# Next Steps Update - 2026-05-15 - Field Items API TM-slot scope fix next

Aktueller Fokus:

- Diagnose 107 narrows the `FVX-ITEM-002 Field Items Random` blocker to the Field-Items API TM-slot scope.
- Raw diagnostics show `tmFieldItemSlots=28` and `requiredFieldTMsTotal=24`; `getFieldItems()` currently exposes `0` TM slots because it filters on `Item::isAllowed`.
- Do not proceed to `FVX-ITEM-003` or `FVX-ITEM-004` until `FVX-ITEM-002` reloads successfully.

Empfohlener naechster Branch:

- `compat/upr-fvx-cfru-dpe-field-items-api-tm-slot-scope-fix`

Ziel:

- Prepare a minimal CFRU/DPE-gated Field-Items API TM-slot scope fix for `FVX-ITEM-002` with `banBadRandomFieldItems=false`.
- Do not make TMs globally allowed and do not expand Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even, Ban Bad Items, Scriptparser, Palette, MoveData, Trainer, Wild, Evolution or Text/Menu.

# Next Steps Update - 2026-05-15 - Field Items Random API TM-slot scope plan next

Aktueller Fokus:

- Diagnose 106 blocks `FVX-ITEM-002 Field Items Random` after PR #36.
- The Unique-TM-Filler pool is sufficient: `randomTmUniquePoolSize=50`, `randomTmFillerAvailable=26`, `randomTmPoolDeficit=0`.
- Active blocker is now the `getFieldItems()` API TM-slot scope: raw diagnostics show `tmFieldItemSlots=28`, but Randomizer API metrics show `randomTmNeededSlots=0` / `randomTmCurrentSlots=0`.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-field-items-random-api-tm-slot-scope-plan`

Ziel des Folgeblocks:

- Read-only klaeren, warum der Gen3/CFRU-DPE Field-Items-API-Scope keine TM-Field-Item-Slots an `ItemRandomizer.randomizeTMFieldItems(...)` uebergibt.
- Weiterhin keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Random Even Distribution und keine Ban-Bad-Items-Umsetzung.

# Next Steps Update - 2026-05-15 - Field Items Random TM-pool reload smoke next

Aktueller Fokus:

- UPR-FVX PR #36 contains the narrow `FVX-ITEM-002 Field Items Random` TM-pool fix.
- Workspace pins `02_external/upr-fvx` to `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd` in this branch.
- `FVX-ITEM-002` remains pending until a Field-Items-only Write-/Reload-Smoke confirms the fix.

Naechster empfohlener Minimalblock nach Merge:

- `test/upr-fvx-cfru-dpe-field-items-random-tm-pool-reload-smoke`

Ziel des Folgeblocks:

- `FVX-ITEM-002 Field Items Random` mit `banBadRandomFieldItems=false` fachlich erneut testen.
- Erwartete TM-Pool-Metriken: `randomTmNeededSlots=28`, `randomTmRequiredTotal=24`, `randomTmFillerNeeded=4`, `randomTmPoolDeficit=0`, `randomTmResultSize=28`, `randomTmResultUniqueSize=28`.
- Erwartete Reload-Metriken: `saveSuccessful=true`, `reloadSuccessful=true`, `fieldItemReloadMismatches=0`, `requiredFieldTMMissingAfter=0`, `disallowedFieldItemWrites=0`, `scriptPatternExpansion=0`.
- Weiterhin keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Random Even Distribution und keine Ban-Bad-Items-Umsetzung.

# Next Steps Update - 2026-05-15 - Field Items Random TM-pool fix next

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` bleibt `GUI-kompatibel` im engen allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random` bleibt blockiert durch den TM-Field-Items-Random-Pool.
- Diagnose 104 empfiehlt einen engen Fix nur fuer `ItemRandomizer.randomizeTMFieldItems(...)` bzw. einen kleinen privaten Helper.

Naechster empfohlener Minimalblock:

- `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix`

Ziel des Folgeblocks:

- Minimalen UPR-FVX-Fix fuer `FVX-ITEM-002` vorbereiten.
- Sanitisiert pruefen: `randomTmNeededSlots=28`, `randomTmRequiredTotal=24`, `randomTmCandidatePoolSize >= 28`, `randomTmPoolDeficit=0`.
- Danach Field-Items-Random Write-/Reload-Smoke wiederholen.
- Keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Random Even Distribution, keine Ban-Bad-Items-Umsetzung.

# Next Steps Update - 2026-05-15 - Field Items Random TM-pool blocker next

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` bleibt durch Diagnose 102 `GUI-kompatibel` im engen allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random` ist durch Diagnose 103 blockiert: Save bricht mit `RandomizationException` ab, kein Output-ROM, kein Reload.
- `FVX-ITEM-003 Field Items Random even distribution` und `FVX-ITEM-004 Ban Bad Items` bleiben `Write modelliert`.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-field-items-random-tm-pool-blocker-plan`

Ziel des Folgeblocks:

- Read-only den Random-TM-Field-Items-Pool und Required-TM-Policy untersuchen.
- Klaeren, ob ein spaeterer Fix eng auf `FVX-ITEM-002` Field Items Random begrenzt werden kann.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution und Text/Menu bleiben ausserhalb.

# Next Steps Update - 2026-05-15 - Field Items Random smoke next

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` ist durch Diagnose 102 im engen allowed-slot Scope `GUI-kompatibel`.
- `FVX-ITEM-002 Field Items Random`, `FVX-ITEM-003 Field Items Random even distribution` und `FVX-ITEM-004 Ban Bad Items` bleiben `Write modelliert`.
- Shops, Pickup und Held Items bleiben getrennte Writer-Scope-Bloecke.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-field-items-random-reload-smoke`

Ziel des Folgeblocks:

- Nur `FVX-ITEM-002 Field Items Random` testen.
- `banBadRandomFieldItems=false` lassen; `FVX-ITEM-004` separat spaeter testen.
- Dieselben allowed-slot-, TM-/Non-TM-, Required-TM- und preserve-only-Metriken wie Diagnose 102 pruefen.

# Next Steps Update - 2026-05-14 - Field Items allowed-slot smoke next

Aktueller Fokus:

- `FVX-ITEM-001..004` Field Items bleiben `Write modelliert`.
- Diagnose 101 bestaetigt read-only, dass der bestehende Gen3 Field-Items-Writer bereits nur allowed Slots schreibt.
- Ein fachlicher Write-/Reload-Smoke wurde nicht ausgefuehrt, weil fuer diesen Block keine explizite lokale Kandidatenfreigabe fuer einen ROM-Write vorlag.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-field-items-allowed-slot-reload-smoke`

Ziel des Folgeblocks:

- Explizit freigegebenen CFRU/DPE Gen9-BPRE-Kandidaten verwenden.
- Nur `FVX-ITEM-001 Field Items Shuffle` als ersten Field-Items-Carrier pruefen.
- Erwartet: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`, TM-/Non-TM-Mismatches `0`, `requiredFieldTMMissingAfter=0`, `disallowedFieldItemWrites=0`, `scriptPatternExpansion=0`.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution und Text/Menu bleiben ausserhalb.

# Next Steps Update - 2026-05-14 - Field Items guarded write/smoke

Recommended next block:

`compat/upr-fvx-cfru-dpe-field-items-allowed-slot-write-guard`

Goal: implement and smoke a narrow Field-Items-only guard for allowed slots, preserving disallowed/progression-sensitive/key-system slots, keeping TM slots as TMs and Non-TM slots as Non-TMs, and maintaining `requiredFieldTMMissingAfter=0`. Keep Shops, Pickup, held items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution and Text/Menu out of scope.

# Next Steps Update - 2026-05-14 - Field Items diagnostics candidate needed

Recommended next block only after an explicitly approved local CFRU/DPE Gen9-BPRE candidate is available:

`test/upr-fvx-cfru-dpe-field-items-scope-diagnostics-candidate`

Goal: run the sanitized Field-Items-only read-only diagnostic from protocol 098/099 and report only aggregated counters for visible Itemballs, Hidden Items/Signposts, TM/Non-TM slots, Required Field TMs, progression-sensitive items, bad items, modern item IDs and invalid/unloaded item IDs. Keep Shops, Pickup, held items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution and Text/Menu out of scope.

# Next Steps Update - 2026-05-14 - Field Items diagnostics scope

Recommended next block:

`test/upr-fvx-cfru-dpe-field-items-scope-diagnostics`

Goal: run a sanitized Field-Items-only diagnostic that reports aggregated visible Itemball, Hidden Item/Signpost, TM-slot, Non-TM-slot, Required Field TM, bad-item, modern-item and invalid-item counters. Keep Shops, Pickup, held items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution and Text/Menu out of scope.

# Next Steps - 2026-05-14 Field Items / Shops / Pickup Plan

Aktiver Anschlussblock:

- `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`

Ziel: Field Items als ersten getrennten Item-Writer read-only planen/diagnostizieren. Fokus auf sichtbare Itemballs, Hidden Items, TM-Slots, Required Field TMs, Progression-/Key-/System-Item-Preserve, invalid/fallback Items und Reload-Kriterien.

Entscheidung aus Diagnose 097:

- Field Items, Shops und Pickup nicht gemeinsam fixen.
- Field Items: Map-/Script-/Signpost-Offset-Writer, naechster engster Block.
- Pickup: separater Table-/Locator-/Probability-Scope.
- Shops: separater Shoplisten-/Terminator-/DataRewriter-/Repointing-/Preis-Scope.
- Gemeinsame Item-Pool-Bans sind noetig, aber kein gemeinsamer Writer-Fix.

Grenzen: keine Shops, kein Pickup, keine Encounter Held Items, keine Trainer/Starter Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Umsetzung.

# Next Steps - 2026-05-14 Post-Merge Palette Sync

Aktiver Anschlussblock:

- `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan`

Ziel: Field Items, Shops und Pickup read-only als eigenen P1-Scope planen. Keine Umsetzung, kein Randomizer-Lauf, kein Build und keine Vermischung mit Palette, Graphics, TypeChart, Trainer, Wild, Evolution, Text/Menu, MoveData oder MoveNames.

Post-Merge-Status aus Diagnose 096:

- Workspace PR #140 ist gemerged.
- `FVX-GFX-001` hat den UPR-FVX Guard-Fix aus PR #35/#139, aber der Reload-Smoke ist blockiert.
- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- `candidateSpeciesTotal=0`
- kein fachlicher Palette-Write-/Reload-Smoke
- keine Hochstufung fuer `FVX-GFX-001`
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`.

`FVX-GFX-001` wartet auf einen explizit freigegebenen UPR-FVX-ladbaren CFRU/DPE Gen9-BPRE-Kandidaten mit `candidateSpeciesTotal=1439`, bevor ein gleicher Normal-only Single-owner Reload-Smoke erneut sinnvoll ist.

# Next Steps - 2026-05-14 Update

Aktiver Anschlussblock nach Diagnose 096:

- `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke-retry`

Ziel: Den engen `FVX-GFX-001` Normal-only Single-owner Reload-Smoke erst wiederholen, wenn ein explizit freigegebener UPR-FVX-ladbarer CFRU/DPE-Gen9-BPRE-Kandidat verfügbar ist und `candidateSpeciesTotal=1439` erfüllt.

Status aus Diagnose 096:

- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- kein fachlicher Palette-Write-/Reload-Smoke
- keine Hochstufung für `FVX-GFX-001`
- `FVX-GFX-002/003/004` bleiben `Write modelliert`

Nicht ausweiten auf Shiny, Shared-Paletten, Graphics/Sprites, TypeChart/TypeEffectiveness, Species-Type-Write, Evolution-Writer, Items, Trainer/Wild, Text/Menu, MoveData oder MoveNames.

# Next Steps

## Aktueller Fokus

CFRU/DPE Palette Normal Single-owner Write Guard Fix ist dokumentiert. Aktuelle Diagnose: `08_tests/randomizer/095_palette_normal_single_owner_write_guard_fix_diagnostics.md`.

`FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel. `FVX-MOVE-005` bleibt getrennt vom MoveData-Byte-Writer-Scope.

Ergebnis aus 090: Der erneute Candidate-Preflight ist blockiert. `candidateFilesChecked=94`, `candidatePreflightSuccessful=false`, `candidateMovesTotal=not available`, `candidateHighestMove=not available`. Es gab keinen fachlichen Name-only fixed-length Reload-Smoke.

Planergebnis aus 091: echte `PokemonPalettesMod.RANDOM`-Randomization ist wegen compressed-data-, shared-pointer-, missing/invalid-pointer-, FreeSpace-/Repointing- und Forme-/Mapping-Risiken noch nicht direkt fixbar.

Diagnoseergebnis aus 093: der sanitisierten read-only Lauf findet `candidateWritablePalettes=385`, aber nur `candidateWritableNormalPalettes=385` und `candidateWritableShinyPalettes=0`. Shared/invalid/missing/decode-failed Paletten bleiben preserve-only.

Planergebnis aus 094: ein spaeterer Fix-/Smoke-Scope ist reviewbar, aber nur fuer Normal-Paletten, die single-owner, dekomprimierbar, gueltig, nicht shared, nicht missing, nicht invalid, nicht decode-failed und nicht cross-kind shared sind. Repointing muss bewusst abgesichert werden.

Fixstand aus 095: UPR-FVX `2697511da9a97df4c29c00dfda8b40e556020489` implementiert den Normal-only-Single-owner-Guard. Kein ROM-/Reload-Smoke wurde in diesem Block ausgefuehrt; `FVX-GFX-001` bleibt bis zum separaten Reload-Smoke `Write modelliert`.

Naechster aktiver Arbeitsblock: `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`.

## Priorisierte naechste Arbeitsbloecke

1. Palette Normal Single-owner Reload-Smoke ausfuehren
   - Empfohlener Branch: `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`.
   - Ziel: den UPR-FVX-Guard-Fix aus 095 fachlich mit einem sanitisierten Reload-Smoke bestaetigen.
   - Erwartet: `normalPaletteWriteCandidates=385`, `normalPaletteWriteAttempts <= 385`, `normalPaletteReloadMismatches=0`, `shinyPaletteWriteAttempts=0`, `sharedPaletteWriteAttempts=0`, `invalidPaletteWriteAttempts=0`, `missingPaletteWriteAttempts=0`, `decodeFailedPaletteWriteAttempts=0`, `crossKindSharedWriteAttempts=0`, `exceptionClass=none`, `stacktrace=none`.
   - Grenzen: keine Shiny-/Shared-/Graphics-/Sprite-, TypeChart-, Species-Type-, Evolution-, Items-, Trainer-, Wild-, Text/Menu- oder MoveData-Arbeit.

2. Palette Randomization Preserve/Repoint Plan halten
   - Diagnose 091 dokumentiert: direkter Fix noch nicht eng genug.
   - `FVX-GFX-001..004` bleiben `Write modelliert`.
   - Spaeterer Fix darf nur single-owner/dekomprimierbare Paletten schreiben oder muss eine vollstaendige Secondary-Pointer-/Shared-Pointer-Policy liefern.

3. Move Names fixed-length Reload-Smoke erst mit eindeutigem Kandidaten wiederholen
   - Empfohlener Branch: `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke-candidate`.
   - Voraussetzung: freigegebener lokaler CFRU/DPE Gen9-BPRE-Kandidat muss mit `moves.total=992` und `991:PsychicNoise` erkennbar sein.
   - Ziel: `FVX-MOVE-005` Name-only im bestehenden Gen3 fixed-length Move-Namen-Pfad pruefen.
   - Kriterien: Save/Log/Output/Reload true, `moves.total=992`, `991:PsychicNoise`, `moveNameReloadMismatches=0`, `moveNameLengthViolations=0`, `moveNameTerminatorPaddingMismatches=0`, keine Description-/Pointer-Aenderung, `exceptionClass=none`, `stacktrace=none`.
   - Grenzen: keine Move Descriptions, keine Pointer-/Repointing- oder Text/Menu-Umsetzung, keine MoveData-Byte-Writer-Aenderung, keine TypeChart/TypeEffectiveness, keine Species-Type-, TM/HM-, Tutor-, Egg-, Learnset-, Palette-, Items-, Trainer-, Wild-, Evolution- oder Graphics-Arbeit.

4. Move Names fixed-length Reload-Smoke Retry-Ergebnis halten
   - Diagnose 089 dokumentiert den blockierten Versuch.
   - Diagnose 090 dokumentiert den blockierten Retry-Preflight mit 94 geprueften lokalen Kandidatendateien und ohne fachliche Smoke-Auswertung.
   - `FVX-MOVE-005` bleibt `Write modelliert`.
   - Keine Feature-Hochstufung ohne stabilen Name-only Reload.

5. Move Names / Descriptions Text/Menu-Scope Plan halten
   - Diagnose 088 dokumentiert `FVX-MOVE-005` als getrennten Text/Menu-Scope.
   - Name-only fixed-length Smoke ist realistisch.
   - Move Descriptions / Text/Menu-Repointing bleibt vorerst zurueckgestellt.

6. MoveData Fairy-Type-Byte-Fix post-merge halten
   - UPR-FVX PR #34 ist gemerged.
   - Workspace PR #129 ist gemerged.
   - Diagnose 087 bestaetigt `FVX-MOVE-004` mit Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`, `moves.total=992`, `991:PsychicNoise` und Preserve-Bytes `0` Mismatches.
   - `FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel; `FVX-MOVE-005` bleibt getrennt.

7. MoveData Types Reload-Smoke historisch einordnen
   - Branch: `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke`.
   - Diagnose 086 dokumentiert den Blocker fuer `FVX-MOVE-004`.
   - Save/Log/Output/Reload sind true; `moves.total=992` und `991:PsychicNoise` bleiben stabil.
   - Preserve-Bytes bleiben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
   - Der Blocker ist durch Diagnose 087 behoben.

8. MoveData Power/Accuracy/PP Reload-Smoke halten
   - Branch: `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke`.
   - Diagnose 085 bestaetigt `FVX-MOVE-001`, `FVX-MOVE-002` und `FVX-MOVE-003` mit Save/Log/Output/Reload true und `writeReloadMoveDataMismatches=0`.
   - `powerReloadMismatches=0`, `accuracyReloadMismatches=0`, `ppReloadMismatches=0`.
   - Preserve-Bytes bleiben bytegleich.

9. PRs fuer Wild-Filter-Carrier-Nullslot-Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Diagnose 075 und Submodule-Pin reviewen und mergen.

10. PRs fuer Trainer Type Diversity Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Diagnose 078 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `TrainerPokemonRandomizer` und den Force-Diverse-Types-/`usedTypes`-Pfad begrenzt.

11. PRs fuer Evolution Same Typing Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Diagnose 080 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `EvolutionRandomizer` und den Same-Typing-/Null-Primary-Type-Scope begrenzt.

12. PR fuer `FVX-TRAIT-018` Similar Strength Normalized Reload reviewen
   - Diagnose 082 bestaetigt den einzelnen Similar-Strength-Smoke mit Save/Log/Output/Reload true und `normalizedWriteReloadEvolutionMismatches=0`.
   - Der Reload-Vergleich nutzt nur persistierte Gen3-Evolution-Felder und Ziel-Species per interner `SpeciesSet`-Identitaet; `Evolution.forme` ist kein Mismatch-Kriterium.
   - `Bad Egg=true` ist nach 055 klassifiziert; `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
   - Fuer diesen engen `FVX-TRAIT-018`-Scope ist kein Fixbranch erforderlich. Evolution-Methoden-Writer und weitere Evolution-Suboptionen bleiben getrennt.

13. Wild-Suboptionen konservativ halten
   - `FVX-WILD-011` und `FVX-WILD-004` sind im `FVX-WILD-001` Carrier-Fix-Smoke stabil.
   - Evolution Restrictions, Catch Em All, Minimum Catch Rate und Level-Balance bleiben getrennte Wild-Scope-Themen.

14. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

15. `analysis/upr-fvx-cfru-dpe-palette-single-owner-normal-only-fix-scope-plan`
   - Abgeschlossen: Diagnose 094 plant den normal-palette-only, single-owner/decompressible Fix-/Smoke-Scope; kein Shiny-Write, kein shared-pointer Write, kein Repointing ohne eigene Policy.

16. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
