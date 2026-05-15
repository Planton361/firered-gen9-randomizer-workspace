# Diagnose 124 - Shop Items Shuffle reload smoke

Datum: 2026-05-15

## Scope

- Feature: `FVX-ITEM-005 Shop Items Shuffle`.
- Branch: `test/upr-fvx-cfru-dpe-shop-items-shuffle-reload-smoke`.
- Kandidat: lokal freigegebene CFRU/DPE Gen9-BPRE-Quelle, nur fuer diesen Shop-only Smoke genutzt.
- Modus: `Settings.ShopItemsMod.SHUFFLE` beziehungsweise aequivalenter GUI-Pfad.
- Artefakte: lokale Output-ROM, Log und Harness-Dateien blieben ignored und wurden nicht committed.

Nicht im Scope:

- `FVX-ITEM-006 Shop Items Random`.
- `FVX-ITEM-007 Shop Item Bans`.
- `FVX-ITEM-008 Guarantee Evolution/X Items`.
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`.
- Field Items, Pickup, Held Items, TM/HM/Tutor/Learnset, Encounter, Trainer, Starter, Wild, Evolution, Text/Menu, Palette/Graphics, MoveData/MoveNames, TypeChart.

## Vorbedingungen

- PR #168 war vor Start gemerged.
- `main` wurde per Fast-forward aktualisiert.
- Arbeitsbranch wurde von sauberem `main` erstellt.
- Diagnose 123 lieferte die stabile read-only Shop-Baseline:
  - `candidateLoaded=true`
  - `shopScanSuccessful=true`
  - `shopCount=23`
  - `mainGameShopCount=3`
  - `skippedShopCount=20`
  - `specialShopCount=3`
  - `shopItemsTotal=157`
  - `terminatorModelStable=true`
  - invalid/unloaded/fallback/placeholder Shop items `0`

## Smoke-Ergebnis

Der Shop-only Shuffle Write/Reload-Smoke ist erfolgreich.

- Save erfolgreich.
- Log erfolgreich und nicht leer.
- Lokale Output-ROM wurde erzeugt.
- Reload der Output-ROM erfolgreich.
- Shop-Anzahl, MainGame-/Skip-/Special-Zuordnung, Item-Gesamtzahl, min/max Shoplaenge und Terminator-Modell blieben stabil.
- Skipped Shops blieben unveraendert.
- Preislogik blieb unveraendert.
- Field Items, Pickup und Held Items blieben ausserhalb des Scopes.

Damit ist `FVX-ITEM-005 Shop Items Shuffle` im getesteten Shop-only Shuffle-Scope `GUI-kompatibel`.

`FVX-ITEM-006..009` bleiben unveraendert `Write modelliert`.

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

## Item-Safety-Metriken

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

Die vorhandenen bad/TM Shop Items sind Baseline-Bestand aus Diagnose 123 und kein Ban-/Pool-Ergebnis dieses Smokes.

## Fehlerstatus

| Metrik | Wert |
|---|---|
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

## Risiken / Blocker

- `DataRewriter<Shop>` und Repointing bleiben fuer weitere Shop-Optionen ein Risiko, auch wenn Shuffle in diesem Lauf reloadstabil war.
- Shop Random muss separat pruefen, ob Pool-Auswahl keine invalid/unloaded/fallback/placeholder Items schreibt.
- Shop Item Bans muessen separat pruefen, ob Bad/Regular/OP-Filter korrekt wirken.
- Guarantee Evolution/X Items muessen separat pruefen, ob MainGame-/Skip-/Special-Policy erhalten bleibt.
- Preislogik und Cheap Rare Candies bleiben separat, weil sie Preisfelder und Listenlaengen anders belasten koennen.

## Bewertung

- `FVX-ITEM-005 Shop Items Shuffle`: `GUI-kompatibel` im getesteten Shop-only CFRU/DPE Gen9-BPRE Shuffle-Scope.
- `FVX-ITEM-006 Shop Items Random`: unveraendert `Write modelliert`.
- `FVX-ITEM-007 Shop Item Bans`: unveraendert `Write modelliert`.
- `FVX-ITEM-008 Guarantee Evolution/X Items`: unveraendert `Write modelliert`.
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`: unveraendert `Write modelliert`.

## Naechster minimaler Schritt

Shop Random Smoke fuer `FVX-ITEM-006`, nur wenn der naechste Block wieder eine explizit freigegebene lokale Kandidatenquelle erlaubt.
