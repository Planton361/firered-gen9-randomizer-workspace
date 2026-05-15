# Diagnose 125 - Shop Items Random reload smoke

Datum: 2026-05-15

## Scope

- Feature: `FVX-ITEM-006 Shop Items Random`.
- Branch: `test/upr-fvx-cfru-dpe-shop-items-random-reload-smoke`.
- Kandidat: dieselbe lokal freigegebene CFRU/DPE Gen9-BPRE-Quelle wie in Diagnose 123/124, nur fuer diesen Shop-only Smoke genutzt.
- Modus: `Settings.ShopItemsMod.RANDOM` beziehungsweise aequivalenter GUI-Pfad.
- Artefakte: lokale Output-ROM, Log und Harness-Dateien blieben ignored und wurden nicht committed.

Nicht im Scope:

- `FVX-ITEM-007 Shop Item Bans`.
- `FVX-ITEM-008 Guarantee Evolution/X Items`.
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`.
- Field Items, Pickup, Held Items, TM/HM/Tutor/Learnset, Encounter, Trainer, Starter, Wild, Evolution, Text/Menu, Palette/Graphics, MoveData/MoveNames, TypeChart.

## Vorbedingungen

- PR #169 war vor Start gemerged.
- `main` wurde per Fast-forward aktualisiert.
- Arbeitsbranch wurde von sauberem `main` erstellt.
- Diagnose 123 lieferte die stabile read-only Shop-Struktur.
- Diagnose 124 bestaetigte `FVX-ITEM-005 Shop Items Shuffle` im getesteten Shop-only Scope als `GUI-kompatibel`.

## Smoke-Ergebnis

Der Shop-only Random Write/Reload-Smoke ist erfolgreich.

- Save erfolgreich.
- Log erfolgreich und nicht leer.
- Lokale Output-ROM wurde erzeugt.
- Reload der Output-ROM erfolgreich.
- Shop-Anzahl, MainGame-/Skip-/Special-Zuordnung, Item-Gesamtzahl, min/max Shoplaenge und Terminator-Modell blieben stabil.
- Skipped Shops blieben unveraendert.
- Preislogik blieb unveraendert.
- Field Items, Pickup und Held Items blieben ausserhalb des Scopes.
- Der Writer-Pool war der Shop-Random-Pool ohne TMs und ohne aktive Ban-/Guarantee-Optionen.

Damit ist `FVX-ITEM-006 Shop Items Random` im getesteten Shop-only Random-Scope `GUI-kompatibel`.

`FVX-ITEM-007..009` bleiben unveraendert `Write modelliert`.

## Shop-Struktur / Reload-Befund

| Metrik | Wert |
|---|---:|
| `candidateFilesChecked` | `3` |
| `candidateLoaded` | `true` |
| `smokeExecuted` | `true` |
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| `reloadSuccessful` | `true` |
| `shopCountBefore` | `23` |
| `shopCountAfter` | `23` |
| `shopCountReload` | `23` |
| `mainGameShopCountBefore` | `3` |
| `mainGameShopCountAfter` | `3` |
| `mainGameShopCountReload` | `3` |
| `skippedShopCountBefore` | `20` |
| `skippedShopCountAfter` | `20` |
| `skippedShopCountReload` | `20` |
| `specialShopCountBefore` | `3` |
| `specialShopCountAfter` | `3` |
| `specialShopCountReload` | `3` |
| `shopItemsTotalBefore` | `157` |
| `shopItemsTotalAfter` | `157` |
| `shopItemsTotalReload` | `157` |
| `minShopLengthBefore` | `2` |
| `minShopLengthAfter` | `2` |
| `minShopLengthReload` | `2` |
| `maxShopLengthBefore` | `9` |
| `maxShopLengthAfter` | `9` |
| `maxShopLengthReload` | `9` |
| `terminatorModelStableAfter` | `true` |
| `terminatorModelStableReload` | `true` |
| `shopLengthMismatchesAfter` | `0` |
| `shopLengthMismatchesReload` | `0` |
| `shopItemReloadMismatches` | `0` |

## Preserve-/Skip-Befund

| Metrik | Wert |
|---|---:|
| `skippedShopItemMismatchesAfter` | `0` |
| `skippedShopItemMismatchesReload` | `0` |
| `specialShopPolicyMismatches` | `0` |
| `priceTableTouched` | `false` |
| `priceReloadMismatches` | `0` |
| `fieldItemScopeChanged` | `false` |
| `pickupScopeChanged` | `false` |
| `heldItemScopeChanged` | `false` |

## Pool-/Item-Befund

| Metrik | Wert |
|---|---:|
| `invalidShopItemWrites` | `0` |
| `unloadedShopItemWrites` | `0` |
| `fallbackShopItemWrites` | `0` |
| `placeholderShopItemWrites` | `0` |
| `badShopItemsBefore` | `36` |
| `badShopItemsAfter` | `36` |
| `badShopItemsReload` | `36` |
| `tmShopItemsBefore` | `6` |
| `tmShopItemsAfter` | `6` |
| `tmShopItemsReload` | `6` |
| `allowedShopItemPoolSize` | `536` |
| `nonBadShopItemPoolSize` | `485` |

Interpretation:

- `allowedShopItemPoolSize` und `nonBadShopItemPoolSize` sind Shop-Writer-nahe Poolgroessen nach TM-Ausschluss.
- Ban Bad war deaktiviert, daher ist `allowedShopItemPoolSize=536` der aktive Random-Pool.
- `nonBadShopItemPoolSize=485` ist nur Vergleichsmetrik fuer einen spaeteren Ban-Bad-Block.
- Die unveraenderten `badShopItemsBefore/After/Reload=36` sind kein Ban-Nachweis; Shop Item Bans bleiben separat.

## Fehlerstatus

| Metrik | Wert |
|---|---|
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

## Risiken / Blocker

- Kein aktueller Blocker fuer `FVX-ITEM-006` im getesteten Shop-only Random-Scope.
- Shop Item Bans muessen separat pruefen, ob `banBadRandomShopItems`, `banRegularShopItems` und `banOPShopItems` die passenden Pools begrenzen.
- Guarantee Evolution/X Items muessen separat pruefen, ob MainGame-/Skip-/Special-Policy erhalten bleibt.
- Preislogik und Cheap Rare Candies bleiben separat, weil sie Preisfelder und Listenlaengen anders belasten koennen.
- `DataRewriter<Shop>` / Repointing bleibt fuer weitere Shop-Optionen ein Reload-Kriterium, auch wenn Random in diesem Lauf stabil war.

## Bewertung

- `FVX-ITEM-005 Shop Items Shuffle`: bleibt `GUI-kompatibel` aus Diagnose 124.
- `FVX-ITEM-006 Shop Items Random`: `GUI-kompatibel` im getesteten Shop-only CFRU/DPE Gen9-BPRE Random-Scope.
- `FVX-ITEM-007 Shop Item Bans`: unveraendert `Write modelliert`.
- `FVX-ITEM-008 Guarantee Evolution/X Items`: unveraendert `Write modelliert`.
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`: unveraendert `Write modelliert`.

## Naechster minimaler Schritt

Shop Item Bans Scope-Plan oder enger Shop-only Ban-Smoke fuer `FVX-ITEM-007`, wenn der naechste Block wieder eine explizit freigegebene lokale Kandidatenquelle erlaubt.
