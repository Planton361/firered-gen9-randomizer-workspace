# 123 - CFRU/DPE Shop Items Scope Diagnostics Candidate

Datum: 2026-05-15
Branch: `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-candidate`
UPR-FVX-Pin: `a2373888ad17145f270ebf6ff17303af41aa86eb`

## Scope

Dieser Block fuehrt eine read-only Shop-Kandidatendiagnose fuer CFRU/DPE Gen9-BPRE aus.

Die lokale Kandidatenquelle wurde fuer diesen Block explizit freigegeben, aber nur read-only und nur fuer Shop-Diagnostik. Dokumentiert werden ausschliesslich aggregierte Zaehler und boolesche Befunde.

Ausdruecklich ausserhalb des Scopes:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Build
- kein Randomizer-Write oder Save
- kein Output-ROM
- keine Logs, Builds oder JARs committen
- keine Shop Writes
- keine Field Items
- kein Pickup
- keine Held Items
- keine Preisveraenderungen
- keine Guarantee-, Ban-, Shuffle- oder Random-Smokes
- keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes, Scriptdaten, Secrets, Tokens oder `.env`-Inhalte dokumentieren
- keine Original-Upstreams kontaktieren

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/121_shop_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/122_shop_items_scope_diagnostics.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `08_tests/randomizer/README.md`
- `01_docs/references/tool-manifest.md`

## Diagnosemethode

- Verwendet wurde ein temporaerer read-only Harness ausserhalb des Repositories.
- Der Harness oeffnete lokale Kandidaten nur zum Lesen ueber vorhandene UPR-FVX-Klassen/JARs.
- Es wurde kein Projekt-Build ausgefuehrt.
- Es wurde kein Randomizer-Write, Save oder Output-ROM erzeugt.
- Es wurden keine Artefakte, Logs oder Tool-Binaries committed.
- Die Ausgabe wurde vor Dokumentation sanitisiert; private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes und Scriptdaten werden nicht wiedergegeben.

## Diagnose-Ergebnis

```text
candidateFilesChecked=3
candidateLoaded=true
shopScanSuccessful=true
shopCount=23
mainGameShopCount=3
skippedShopCount=20
specialShopCount=3
emptyShopCount=0
shopItemsTotal=157
minShopLength=2
maxShopLength=9
terminatorModelStable=true
shopLengthMismatch=0
invalidShopItemIds=0
unloadedShopItemIds=0
fallbackShopItems=0
placeholderShopItems=0
badShopItems=36
tmShopItems=6
shopPointerModelObserved=true
dataRewriterOrRepointingRisk=true
skipShopsPreserved=true
fieldItemScopeChanged=false
pickupScopeChanged=false
heldItemScopeChanged=false
priceTableTouched=false
priceTableReadable=true
exceptionClass=none
stacktrace=none
```

## Shop-Struktur

Die read-only Diagnose bestaetigt fuer den geladenen Kandidaten:

- Der Shop-Reader konnte die Shopstruktur laden: `shopScanSuccessful=true`.
- `shopCount=23` Shops wurden ueber das Gen3/BPRE-Shopmodell sichtbar.
- `mainGameShopCount=3` Shops sind als Main-Game-Shops klassifiziert.
- `skippedShopCount=20` Shops sind preserve-/skip-relevant.
- `specialShopCount=3` Shops sind ueber die bestehende Special-Shop-Policy randomisierbar modelliert.
- `emptyShopCount=0`; alle sichtbaren Shops enthalten mindestens ein Item.
- `shopItemsTotal=157` mit `minShopLength=2` und `maxShopLength=9`.
- Das Terminator-Modell ist fuer den Reader stabil: `terminatorModelStable=true`, `shopLengthMismatch=0`.
- Das Pointerlistenmodell wurde beobachtet: `shopPointerModelObserved=true`.
- `dataRewriterOrRepointingRisk=true` bleibt bestehen, weil der spaetere Writer ueber `DataRewriter<Shop>` laufen kann.

## Item-Safety-Befund

- `invalidShopItemIds=0`
- `unloadedShopItemIds=0`
- `fallbackShopItems=0`
- `placeholderShopItems=0`
- `badShopItems=36`
- `tmShopItems=6`

Bewertung:

- Die vorhandenen Shop-Items sind fuer den Reader geladen und gueltig.
- Es wurden keine Fallback- oder Placeholder-Shop-Items im sichtbaren Shopbestand festgestellt.
- Bad Items und TMs existieren im aktuellen Shopbestand; das ist fuer diese read-only Diagnose kein Fehler, aber fuer spaetere Ban-/Random-Pool-Smokes separat zu bewerten.

## Preserve-/Skip-Befund

- `skipShopsPreserved=true`, weil diese Diagnose read-only lief und keine Shopdaten geschrieben wurden.
- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `heldItemScopeChanged=false`
- `priceTableTouched=false`
- Die Preistabelle wurde nicht veraendert; sie war nur lesbar: `priceTableReadable=true`.

## Risiken / Blocker

Kein aktueller Blocker fuer den naechsten Shop-Shuffle-Smoke aus der read-only Strukturdiagnose.

Weiterhin relevant fuer den Smoke:

- `DataRewriter<Shop>` kann bei spaeteren Writes repointen; der Smoke muss Pointer-/Reload-Stabilitaet indirekt ueber Reload-Metriken nachweisen.
- Skip-Shops muessen preserve-only bleiben.
- Special-/Main-Game-Policy muss beim Shuffle getrennt beobachtet werden.
- Terminatoren und Laengen muessen nach Write/Reload stabil bleiben.
- Bad Items und TMs im vorhandenen Shopbestand sind nicht automatisch Random-Pool-Freigaben.
- Preislogik bleibt ausserhalb des Shop-Shuffle-Smokes.

## Feature-Status

- `FVX-ITEM-005 Shop Items Shuffle`: Voraussetzung fuer den naechsten Shop-only Shuffle-Smoke ist durch die stabile read-only Strukturdiagnose belegt; noch keine Hochstufung.
- `FVX-ITEM-006 Shop Items Random`: bleibt `Write modelliert`.
- `FVX-ITEM-007 Shop Item Bans`: bleibt `Write modelliert`.
- `FVX-ITEM-008 Guarantee Evolution/X Items`: bleibt `Write modelliert`.
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`: bleibt `Write modelliert`.
- Field Items, Pickup und Held Items werden nicht geaendert oder hochgestuft.

## Empfehlung

Naechster minimaler Schritt: ein Shop-only Shuffle Write-/Reload-Smoke.

Empfohlener Branch:

- `test/upr-fvx-cfru-dpe-shop-items-shuffle-reload-smoke`

Erwartete Smoke-Grenzen:

- Nur `FVX-ITEM-005 Shop Items Shuffle`.
- Keine Shop Random, keine Bans, keine Guarantee Evolution/X Items, keine Balance Prices, keine Cheap Rare Candies.
- Keine Field Items, Pickup, Held Items, TM/HM/Tutor/Learnset, Trainer, Wild, Evolution, Text/Menu, Palette/Graphics, MoveData/MoveNames oder TypeChart.
- Metriken muessen mindestens Shop-Anzahl, Item-Gesamtzahl, min/max Laenge, Terminator-/Laengenstabilitaet, preserved skipped shops, Special-/MainGame-Policy und keine Preis-/Field-/Pickup-/Held-Scope-Aenderung abdecken.
