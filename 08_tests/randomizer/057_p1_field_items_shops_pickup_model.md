# 057 - P1 Field Items / Shops / Pickup Item-Modell fuer CFRU/DPE Gen9-BPRE

## Ziel

Dieses read-only Protokoll modelliert Field Items, Shops, Pickup und allgemeine Item-Randomization fuer den getesteten CFRU/DPE Gen9-BPRE-Stand. Es ist getrennt von Encounter Held Items aus Diagnose 054 und fuehrt keine Fixumsetzung aus.

Scope:

- Nur bestehende Protokolle und read-only `rg`-/Quellbefunde.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine neuen Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, ROM-Namen, Hashes, Secrets oder `.env`-Inhalte gelesen oder dokumentiert.

Grenzen:

- Diagnose 054 bleibt die Grenze fuer Encounter Held Items.
- Diagnose 056 bleibt die Grenze fuer Move-Data-Write.
- Diagnose 055 bleibt die Grenze fuer Log-Hygiene und Fallback-Marker.
- Item-Text, Menues, Descriptions und Type-Chart bleiben out of scope.

## Genutzte Belege

Primaere Belege:

- `047_fvx_gui_options_compatibility_matrix.md`
- `053_p1_item_data_and_bad_item_model.md`
- `054_encounter_held_items_scope_write_diagnostics.md`
- `055_type_log_placeholder_hygiene.md`
- `056_p1_move_data_write_model.md`

Read-only `rg`-Befunde:

- `Field Items`
- `Shop`
- `Pickup`
- `ItemRandomizer`
- `getAllowedItems`
- `getNonBadItems`
- `badItems`
- `bannedItems`
- `ItemCount`
- `ItemData`
- `item.count`

Ergaenzende read-only Codebefunde aus dem lokalen Workspace:

- `ItemRandomizer.randomizeFieldItems()` trennt Field-Item-TMs und Nicht-TMs und schreibt ueber `romHandler.setFieldItems(...)`.
- Field-Item-Randomization nutzt fuer Nicht-TMs `getNonBadItems()` oder `getAllowedItems()` und entfernt TMs aus dem Nicht-TM-Pool.
- `ItemRandomizer.randomizeShopItems()` nutzt Shop-Listen, Special-Shop-Scope, Main-Game-/Non-Main-Game-Trennung, Bad-/Regular-/OP-Shop-Filter sowie optionale Guaranteed Evolution-/X-Items.
- `ItemRandomizer.randomizePickupItems()` nutzt `getPickupItems()`, erhaelt bestehende Probability-Slots und waehlt neue Items aus `getNonBadItems()` oder `getAllowedItems()`.
- Gen3-Shopdaten werden ueber `ShopPointerOffsets` gelesen/geschrieben; Shoplisten sind `u16`-Itemstreams mit Terminator.
- Gen3-Pickup nutzt `PickupTableStartLocator`, `PickupItemCount` und schreibt `u16`-Item-IDs bei erhaltener Tabellenstruktur.
- CFRU/DPE-Quellen enthalten eigene Shop-/Pickup- und Item-Tabellen, darunter `sPickupCommonItems`, `sPickupRareItems`, `gItemData`, `ITEM_FREE_SPACE3` und DPE `ITEM_SHINY_SPACE20`.

## Grenze zu Encounter Held Items aus 054

Diagnose 054 bestaetigt nur den Encounter-Held-Item-Scope:

| Bereich | Stand aus 054 |
|---|---|
| Datenort | `gBaseStats` |
| Felder | `item1` / `item2` |
| Offsets | `0x0C` / `0x0E` |
| Entry-Size | `0x1C` |
| Item-Scope im Test | `item.count=778` |
| Reload-Kriterium | `writeReloadEncounterHeldItemMismatches=0` |

Nicht durch 054 abgedeckt:

- Field Items / Overworld Items.
- Shops und Shop-Preise.
- Pickup-Tabellen.
- Allgemeine Item-Randomization ausserhalb `gBaseStats`.
- Item-Text, Menues oder Descriptions.

Damit darf 054 nicht als P1-Nachweis fuer Field Items, Shops oder Pickup gelesen werden. Es beweist nur, dass der erweiterte Item-Scope und die modernen Bad-/Banned-Filter fuer den eng gegateten Encounter-Held-Item-Pfad stabil genutzt wurden.

## Item-Scope-Stand aus 053/054

Aus 053:

| Quelle | Modellwert | Bedeutung |
|---|---:|---|
| klassischer FVX-FRLG-`ItemCount` | `374` | zu niedrig fuer CFRU/DPE moderne Items |
| CFRU `ITEM_FREE_SPACE3` | `778` | CFRU-naher oberer Scope |
| CFRU `ITEMS_COUNT` | `779` | `ITEM_FREE_SPACE3 + 1` |
| DPE `ITEM_SHINY_SPACE20 + 1` | ca. `799` | DPE-Header-Scope mit Shiny-Space-Platzhaltern |
| bekannte moderne Beispiele | `Booster Energy`, `Tera Orb`, `Portable PC` | oberhalb klassischer FVX-Grenzen |

Aus 054:

| Feld | Wert |
|---|---:|
| `item.count` | `778` |
| hoechster geladener Eintrag | `1778:Free Space 3` |
| Itemname-Fallback-Zaehler | `0` |
| Bad-/Banned-Item count | `293` |
| banned item violations | `0` |

Einordnung fuer 057:

- Der erweiterte Item-Scope ist eine noetige Grundlage, aber kein vollstaendiger Field-/Shop-/Pickup-Nachweis.
- Items mit Fallback- oder implausiblem Namen duerfen nicht als Random-Picks zugelassen werden.
- Die DPE-Oberregion `779..798` war im 054-Test nicht plausibel lesbar und wurde deshalb nicht als Random-Pick-Scope verwendet.
- Moderne vorhandene IDs koennen Preserve-Faelle sein, aber das beweist keine sichere neue Platzierung in Field-, Shop- oder Pickup-Daten.

## Field-Item-Risiken

FVX-Field-Item-Randomization arbeitet ueber `romHandler.getFieldItems()` und `romHandler.setFieldItems(...)`.

Relevante Annahmen:

- Nur Items mit `item.isAllowed()` werden in der Gen3-Field-Item-Liste gesammelt und spaeter wieder geschrieben.
- TMs und Nicht-TMs werden getrennt behandelt; TMs muessen an TM-Positionen bleiben.
- `getRequiredFieldTMs()` erzwingt bestimmte TM-Felditems im TM-Pool.
- Nicht-TMs werden aus `getNonBadItems()` oder `getAllowedItems()` gepickt; TMs werden aus dem Nicht-TM-Pool entfernt.

Risiken fuer CFRU/DPE:

| Risiko | Klassifikation |
|---|---|
| Script-linked Items | Field Items koennen Progression, Scripts, Flags oder NPC-Logik beeinflussen. |
| Required TMs | TM-Positionen und required field TMs muessen erhalten oder gezielt modelliert werden. |
| Moderne TM/HM-Items | CFRU/DPE hat 128 TM/HM-Slots; klassisches Item-/TM-Modell allein reicht nicht fuer Field Items. |
| Key-/System-Items | Key Items, Tera Orb, Portable PC und aehnliche Systemitems duerfen nicht zufaellig platziert werden. |
| Fallback-/Placeholder-Items | `item #<id>`, Free-Space und Shiny-Space duerfen keine neuen Picks werden. |
| Map-/Offset-Scope | Field Items haengen an Map-/Event-/Overworld-Daten; 054 beruehrt diese Tabellen nicht. |

P1-Modellgrenze:

- Field Items bleiben open / not diagnosed.
- Ein spaeterer Fix braucht eigene Read/Write/Reload-Kriterien fuer Field-Item-Offsets.
- Der Encounter-Held-Item-Preserve-Fix aus 054 darf nicht als Field-Item-Write-Beweis genutzt werden.

## Shop-Randomization-Risiken

FVX-Shop-Randomization arbeitet ueber `romHandler.getShops()` und `romHandler.setShops(...)`.

Relevante Annahmen:

- Gen3-Shops werden ueber `ShopPointerOffsets` gelesen.
- Shop-Inventare sind `u16`-Itemlisten mit Terminator.
- `SkipShops` trennt nicht randomisierte Shops von Special Shops.
- `MainGameShops` beeinflusst die Platzierung garantierter Items.
- `randomizeShopItems()` filtert mit `getNonBadItems()` / `getAllowedItems()`, entfernt TMs, kann Regular-/OP-Shop-Items bannen und kann Evolution-/X-Items garantieren.
- `addCheapRareCandiesToShops()` kann Shopgroessen und Preise veraendern.
- `setShopPrices(...)` schreibt Preise ueber `ItemData`, `ItemEntrySize` und `ItemCount`.

Risiken fuer CFRU/DPE:

| Risiko | Klassifikation |
|---|---|
| Shop-Pointer-Scope | CFRU/DPE kann Shopdaten, Scriptbindung oder Pointerlagen veraendert haben; 054 prueft das nicht. |
| Shopgroessen | Hinzufuegen von Items kann Rewriting/Repointing-Semantik betreffen. |
| Main-Game-/Special-Shop-Policy | Garantierte Evolution-/X-Items duerfen Progression nicht brechen. |
| Preise | Preis-Balancing nutzt `ItemData`; klassischer `ItemCount` und erweiterter Scope muessen zusammenpassen. |
| Moderne Bad-/Banned-Items | Moderne Key-/System-/Placeholder-Items duerfen nicht in Shops landen. |
| Text/Menu | Shop-Menues und Itemtexte bleiben out of scope; 057 modelliert nur Daten-/Scope-Risiko. |

P1-Modellgrenze:

- Shops bleiben open / not diagnosed.
- Ein spaeterer Fix muss Shop-Inventar-Reload, Shopgroessen und ggf. Preise getrennt nachweisen.
- Item-Text/Menu/Description darf nicht im selben P1-Datenfix erzwungen werden.

## Pickup-Table-Risiken

FVX-Pickup-Randomization arbeitet ueber `romHandler.getPickupItems()` und `romHandler.setPickupItems(...)`.

Relevante Annahmen:

- Gen3 nutzt `PickupTableStartLocator` und `PickupItemCount`.
- FRLG-Pickup ist im klassischen RomEntry mit `PickupItemCount=16` modelliert.
- Der Writer schreibt pro Pickup-Eintrag eine interne `u16`-Item-ID.
- `randomizePickupItems()` erhaelt die bestehenden Probability-Slots je `PickupItem`.
- TMs werden entfernt, wenn TMs nicht held-faehig oder wiederverwendbar sind.

CFRU/DPE-Befunde:

- CFRU enthaelt eigene Pickup-Tabellen `sPickupCommonItems` und `sPickupRareItems`.
- CFRU-Pickup-Logik waehlt aus Common-/Rare-Reihen und haengt an Battle-/End-of-Battle-Logik.
- DPE/CFRU Item-Grenzen reichen deutlich ueber klassische FRLG-Items hinaus.

Risiken:

| Risiko | Klassifikation |
|---|---|
| Tabellenmodell | Klassischer Locator/Count muss nicht das aktive CFRU/DPE-Pickup-Modell vollstaendig treffen. |
| Common/Rare-Semantik | CFRU trennt Common/Rare-Tabellen; ein flacher klassischer Count kann Semantik verlieren. |
| Probability-Slots | Wahrscheinlichkeitsverteilung muss erhalten bleiben oder explizit modelliert werden. |
| Moderne Item-Pools | Bad-/Banned-/Fallback-/Placeholder-Items duerfen nicht in Pickup-Pools gelangen. |
| Runtime-Sonderlogik | CFRU kann Items nach Battle-/Ability-Logik anders behandeln als Vanilla-FRLG. |

P1-Modellgrenze:

- Pickup bleibt open / not diagnosed.
- Ein spaeterer Fix braucht eigene Kriterien fuer gelesene Pickup-Items, Probability-Slots, geschriebenen Reload und banned item violations.

## Allgemeine Item-Randomization- und Bad-/Banned-Item-Risiken

Zentrale Poolquellen:

- `getAllowedItems()`: alle nicht-null und erlaubten Items.
- `getNonBadItems()`: `getAllowedItems()` ohne `item.isBad()`.
- `bannedItems`: klassische Unique-/Key-/HM-nahe Bans.
- `badItemsFRLG` / `badItemsRSE`: klassische problematische Items.
- 054 ergaenzt moderne CFRU/DPE-Bans fuer den Encounter-Held-Item-Fix.

Fuer Field Items, Shops und Pickup reicht der Encounter-Held-Item-Poolnachweis nicht aus, weil jeder Pfad andere fachliche Risiken hat:

| Pfad | Zusaetzliche Poolfrage |
|---|---|
| Field Items | Darf dieses Item in einem Map-/Script-Kontext liegen? |
| Shops | Darf dieses Item kaufbar sein, mit Preis und Progression? |
| Pickup | Darf dieses Item zufaellig durch Ability-Pickup entstehen? |
| Encounter Held Items | Darf dieses Item von wilden Pokemon getragen werden? |

Konsequenz:

- "Nicht bad" ist fuer Field/Shop/Pickup nicht automatisch "sicher".
- Moderne Key-/System-/Form-/Mega-/Z-/Plate-/Mask-/Tera-/Booster-/Placeholder-Bereiche muessen pro Pfad bewertet werden.
- Fallback-Namen sind nach 055 Log-/Namen-Hygiene, aber als Random-Pick-Signal fuer Datenpfade unsafe.

## Preserve-/Skip-Policy fuer spaetere Fixes

Ein spaeterer Fixbranch sollte konservativ modellieren:

1. Bestehende unbekannte oder fallbackbenannte Items nicht neu random-picken.
2. Bestehende moderne IDs preserven, wenn der Pfad sie nur lesen/schreiben muss und keine sichere Replacement-Semantik vorliegt.
3. Free-Space-, Placeholder- und Shiny-Space-Items immer skippen oder bannen.
4. Key-/System-/Progression-Items nicht zufaellig in Field, Shop oder Pickup platzieren.
5. TMs/HMs getrennt nach Pfad behandeln; Field-Item-TM-Positionen muessen TM-Positionen bleiben.
6. Shop-Listen, Terminatoren, Main-Game-/Special-Shop-Markierungen und Preise nur in einem explizit modellierten Scope aendern.
7. Pickup-Probability-Slots und Common-/Rare-Semantik erhalten.
8. Item-Text, Menues und Descriptions nicht im selben Datenmodell mitschreiben.

## Reload-/Diagnosekriterien fuer spaetere Fixbranches

Dieses Protokoll erhebt keine neuen Diagnosewerte. Ein spaeterer Fix sollte getrennte Kriterien pro Pfad dokumentieren:

### Gemeinsame Kriterien

| Kriterium | Erwartung |
|---|---|
| Save | `saveSuccessful=true` |
| Log | `logSuccessful=true`, `logNonEmpty=true` |
| Output | Output-ROM vorhanden, ohne privaten Pfad oder ROM-Namen zu dokumentieren |
| Reload | Reload der geschriebenen ROM-Daten erfolgreich |
| Item-Scope | dokumentierter `item.count`, hoechste geladene Item-ID, Fallback-Zaehler |
| Pool-Safety | `banned item violations=0` oder aequivalenter Zaehler |
| IDs | invalid/missing item IDs `0` |
| Markers | `Bad Egg`, `<unknown>` und Unknown-Item-Marker nach 055 klassifizieren, nicht vermischen |

### Field Items

- Field-Item-Anzahl before/after/reload.
- TM-Field-Item-Anzahl before/after/reload.
- Required-field-TM-Erhaltung.
- `writeReloadFieldItemMismatches=0` oder klar aequivalenter Zaehler.
- Keine script-linked oder unsafe Items als neue Picks.

### Shops

- Shop-Anzahl und Special-Shop-Anzahl before/after/reload.
- Shop-Item-Anzahl je Shop oder zusammengefasst before/after/reload.
- Terminator-/Pointer-Rewrite stabil.
- Preis-Reload nur, wenn Preisoption im Scope ist.
- `writeReloadShopItemMismatches=0` und ggf. `writeReloadShopPriceMismatches=0`.

### Pickup

- Pickup-Item-Anzahl before/after/reload.
- Probability-Slots before/after/reload erhalten.
- Common-/Rare- oder klassischer Count-Scope klar dokumentiert.
- `writeReloadPickupItemMismatches=0`.

## Explizite Nicht-Ziele

057 erweitert nicht:

- Encounter Held Items aus `gBaseStats`.
- Move-Data-Write oder `saveMoves()`.
- Log-Hygiene, Unknown-Fallbacks oder sichtbare Namen.
- Item-Text, Item-Menues, Descriptions oder Shop-UI.
- Type-Chart oder Type-Effectiveness.
- ROM-/Build-/Harness-Diagnosen.

## Ergebnis

Field Items, Shops, Pickup und allgemeine Item-Randomization bleiben fuer den getesteten CFRU/DPE Gen9-BPRE-Stand open / not diagnosed. Die bestehende Item-Scope-Erweiterung aus 054 ist eine wichtige Grundlage, beweist aber nur Encounter Held Items. Fuer die uebrigen Item-Pfade muessen spaetere Fixbranches eigene Scope-, Preserve-, Pool- und Reload-Kriterien nachweisen.
