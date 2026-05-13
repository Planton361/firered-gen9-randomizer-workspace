# 053 - P1 Item Data / Bad Item / Encounter Held Item Model (CFRU/DPE Gen9-BPRE)

## Ziel

Read-only Modellierung der Item-ID-Grenzen, Itemnamen, Bad-/Key-Item-Filter und Encounter Held Items fuer den getesteten CFRU/DPE Gen9-BPRE-Stand.

Kein Fix, keine Codeaenderung und keine Aenderungen an `02_external/**`.

## Ausgangspunkt

- UPR-FVX PR #27: gemerged.
- Workspace PR #90: gemerged.
- Vorherige Diagnose 050: Base Stats, Types, Ability-Slots und Encounter-Held-Item-Felder in `gBaseStats` modelliert.
- Vorherige Diagnose 052: Ability1/2 und Hidden Ability sind P1-supported; Encounter Held Items blieben out of scope.
- Bereits P1-supported im relevanten Umfeld:
  - Trainer Held Items-only
  - Base Stats + Types
  - Ability1/2 + Hidden Ability

## Relevante Dateien und Codepfade

### UPR-FVX / romio

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
  - `loadItems()`
  - `loadBasicPokeStats(...)`
  - `saveBasicPokeStats(...)`
  - BaseStats-Itemfelder werden ueber `Gen3Constants.itemIDToStandard(...)` und `itemIDToInternal(...)` gelesen/geschrieben.
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/constants/Gen3Constants.java`
  - `baseStatsEntrySize`
  - `bsCommonHeldItemOffset`
  - `bsRareHeldItemOffset`
  - `itemIDToStandard(...)`
  - `itemIDToInternal(...)`
  - `bannedItems`
  - `badItemsFRLG` / `badItemsRSE`
  - `getBadItems(...)`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/EncounterHeldItemRandomizer.java`
  - `randomizeWildHeldItems()`
- `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/gen3_offsets.ini`
  - FireRed RomEntry `ItemData`, `ItemEntrySize`, `ItemCount`.

### CFRU/DPE Quellen

- `02_external/**/include/items.h`
  - DPE Item-Konstanten und `ITEMS_COUNT`.
- `02_external/**/asm_defines.s`
  - CFRU-seitige Item-Konstanten im getesteten Stand.
- `02_external/**/include/base_stats.h`
  - BaseStats-Feldlayout.
- `02_external/**/include/pokemon.h`
  - CFRU `struct BaseStats`-Layout.
- `02_external/**/src/item.c`
  - Runtime-Sanitizing von Item-IDs und Itemnamen-Zugriff.

## Item-ID-Modell

### CFRU/DPE Grenzen

| Quelle | Befund | Bedeutung |
|---|---:|---|
| CFRU `ITEM_FREE_SPACE3` | `778` | CFRU-Seite dokumentiert freien/placeholdernahen Bereich bis `ITEM_FREE_SPACE3` und nutzt im bekannten Scope `ITEMS_COUNT=779`. |
| DPE `ITEM_SHINY_SPACE20 + 1` | ca. `799` | DPE-generierte Item-Liste reicht ueber `ITEM_SHINY_SPACE1..20` bis `ITEM_SHINY_SPACE20`, also `ITEMS_COUNT=799`. |
| Klassisches FRLG-FVX `ItemCount` | `374` | Aktueller FVX-RomEntry-Scope ist fuer CFRU/DPE-Items deutlich zu niedrig. |
| TM01 | `0x121` / `289` | Interne Gen3-/DPE-ID. |
| TM50 | `0x152` / `338` | Letzte klassische TM im FVX-Item-Mapping. |
| HM01 | `0x153` / `339` | HMs liegen direkt nach TM50. |
| Booster Energy | `0x2E7` / `743` | Modernes Gen9-relevantes Item oberhalb klassischer FVX-Grenzen. |
| Tera Orb | `0x306` / `774` | Spezial-/Key-artiges modernes Item; kein sicherer Wild-Held-Item-Kandidat. |
| Portable PC | `0x307` / `775` | Spezial-/Key-artiges modernes Item; kein sicherer Wild-Held-Item-Kandidat. |

### Interpretation

Der getestete CFRU/DPE-Stand hat mindestens zwei relevante Item-Grenzen:

- CFRU-runtime-naher Scope bis `ITEM_FREE_SPACE3=778` / `ITEMS_COUNT=779`.
- DPE-generierter Header-Scope bis `ITEM_SHINY_SPACE20 + 1` / ca. `799`.

Fuer einen Randomizer-Fix ist die sichere Grenze nicht nur eine Konstante, sondern muss am aktiven ROM-Modell validiert werden:

- `ItemData`-Pointer muss valide sein.
- `ItemEntrySize` bleibt im FRLG-FVX-Modell relevant.
- `ItemCount` darf nicht beim klassischen FRLG-Wert `374` stehen bleiben, wenn moderne Encounter-Held-Items erhalten oder randomisiert werden sollen.
- Platzhalter-/Free-Space-/Shiny-Space-Items duerfen trotz geladenem Namen nicht automatisch in Random-Pools gelangen.

## FVX Item-Load- und Mapping-Annahmen

### Aktueller Item-Load

`Gen3RomHandler.loadItems()` nutzt:

- `romEntry.ItemData` als Tabellenbasis.
- `romEntry.ItemEntrySize` als Strukturlaenge.
- `romEntry.ItemCount` als interne Obergrenze.
- `Gen3Constants.itemIDToStandard(internal)` fuer die FVX-Standard-ID.

Der FireRed RomEntry ist klassisch ausgerichtet und dokumentiert `ItemCount=374`. Damit ist die aktuelle FVX-Itemnamen-Abdeckung fuer CFRU/DPE moderne Items unvollstaendig.

### Standard-ID-Mapping

FVX mappt klassische interne Gen3-Item-IDs auf standardisierte `ItemIDs`. Nicht bekannte interne IDs werden per `UNIQUE_OFFSET + internalID` abgebildet.

Risiken:

- Moderne CFRU/DPE-Items oberhalb der klassischen Map werden nur als Unique-IDs darstellbar.
- Wenn `items.size()` nicht fuer diese Unique-IDs erweitert wird, koennen Items nicht geladen oder nicht referenziert werden.
- Encounter-Held-Items mit internen IDs oberhalb der klassischen FVX-Grenze koennen beim Lesen als `null` enden.
- Beim Speichern schreibt `saveBasicPokeStats(...)` fuer `null`-Held-Items `0`, wodurch urspruengliche moderne Held Items verloren gehen koennen, sobald Species-Daten geschrieben werden.

## Itemnamen-Abdeckung

CFRU runtime-seitig werden Item-IDs ueber `SanitizeItemId(...)` abgesichert; out-of-range IDs werden zu `ITEM_NONE`. FVX muss trotzdem eigene robuste Grenzen haben, weil es Tabellen direkt liest und schreibt.

Aktueller Modellbefund:

- Klassische Itemnamen bis `ItemCount=374` sind im FVX-FRLG-Scope abgedeckt.
- Moderne Items wie Booster Energy, Masken, Mints, Tera Orb und Portable PC sind ohne CFRU/DPE-gated ItemCount-Erweiterung nicht verlaesslich als `Item`-Objekte verfuegbar.
- Logger- und Diagnosepfade brauchen Fallbacks wie `item #<internalId>` oder `item #<standardId>`, statt bei fehlendem Namen zu crashen oder `<unknown>` unklar zu lassen.

## Bad-/Key-Item-Filter

### Aktueller FVX-Filter

FVX setzt Item-Flags aus drei Quellen:

- `bannedItems`: klassische Gen3 Unique-/Key-Items und HMs.
- `badItemsFRLG` / `badItemsRSE`: klassische problematische Held-Items, Mail, Berries, Shoal-/Shard-/Contest-Items je ROM-Typ.
- TM-Markierung: klassische TM01..TM50 ueber `tmCount`.

### Nicht ausreichend abgedeckte CFRU/DPE-Bereiche

Die klassischen Filter decken moderne CFRU/DPE-Items nicht vollstaendig ab. Besonders kritisch fuer Encounter Held Items:

| Bereich | Risiko | Empfehlung |
|---|---|---|
| Key Items / System Items | Koennen Spielprogression oder Menues brechen. | Immer bannen. |
| TMs/HMs | Duerfen nicht als Wild-Held-Item-Pool in klassischer Logik landen. | Slot-/ID-basiert bannen. |
| Mail | Klassisch bereits bad; moderne Erweiterungen pruefen. | Weiter bannen. |
| Balls | Als wilde Held Items fachlich fragwuerdig und oft nicht als Held-Item gedacht. | Fuer sicheren P1-Scope bannen, ausser explizit erlaubt. |
| Berries | In FVX klassisch bad; fuer CFRU/DPE spaeter bewusst entscheiden. | Im ersten P1-Fix konservativ bannen oder bestehendes `banBadItems` respektieren. |
| Free-Space-/Placeholder-Items | Koennen unbenannt oder funktionslos sein. | Immer bannen. |
| Shiny-Space-Items | DPE-Platzhalter-/Erweiterungsbereich. | Immer bannen. |
| Form-/Mega-/Z-/Plate-/Mask-Items | Koennen Form-, Mega-, Z-, Arceus-/Silvally- oder Ogerpon-Logik beeinflussen. | Fuer P1 Encounter Held Items konservativ bannen. |
| Tera Orb | System-/Key-artiges Item. | Immer bannen. |
| Booster Energy | Modernes Held Item mit Kampfmechanik. | Potenziell erlaubbar, aber erst nach Item-Effect-Scope-Bewertung. |

## Encounter Held Items in `gBaseStats`

### Feldmodell

| Feld | Offset | Breite | Bedeutung |
|---|---:|---:|---|
| `item1` / common held item | `0x0C` | `u16` | Common Held Item |
| `item2` / rare held item | `0x0E` | `u16` | Rare Held Item |

Weitere bekannte Parameter:

- `gBaseStats` Pointer-Ort: `0x080001BC`.
- Entry-Size: `0x1C`.
- Species-Scope: interne CFRU/DPE Species-IDs, bis `NUM_SPECIES=1440` im getesteten Scope.
- Die Felder sind in-place `u16`; kein Repointing ist fuer Encounter Held Items selbst erforderlich.

### Unterschied zu Trainer Held Items

Trainer Held Items liegen in Trainer-Pokemon-Daten und wurden separat diagnostiziert. Encounter Held Items sind Species-BaseStats-Felder und verwenden den globalen Item-Pool. Trainer Held Items beweisen daher nicht, dass Encounter Held Items sicher sind.

### Aktueller Read-/Write-Risikopfad

1. `loadBasicPokeStats(...)` liest raw `u16` aus `item1/item2`.
2. Raw-ID wird ueber `Gen3Constants.itemIDToStandard(...)` gemappt.
3. FVX nimmt nur dann ein `Item`, wenn die gemappte ID in `items.size()` liegt und nicht `null` ist.
4. Moderne Items koennen dadurch als `null` geladen werden.
5. `saveBasicPokeStats(...)` schreibt fuer `null` `ITEM_NONE` / `0`.

Damit ist Encounter-Held-Item-Write ohne erweiterten Item-Load-/Mapping-Support potentiell destruktiv.

## EncounterHeldItemRandomizer-Pfad

`EncounterHeldItemRandomizer.randomizeWildHeldItems()` nutzt:

- `romHandler.getNonBadItems()`, falls Bad Items gebannt werden.
- `romHandler.getAllowedItems()`, falls Bad Items erlaubt sind.
- `romHandler.getSpeciesSetInclFormes()` als Species-Scope.

Der Randomizer ueberspringt aktuell Species ohne vorhandene Held Items, behandelt aber nicht alle CFRU/DPE-Sonderfaelle explizit:

- Placeholder-/Null-Species
- Species mit `BST == 0`
- fehlende Item-Objekte wegen ItemCount-/Mapping-Limit
- moderne Bad-/Key-/Placeholder-Items im Pool

## Bewertung: Ist Encounter Held Items allein fixbar?

Ja, aber nicht ohne kleinen CFRU/DPE-gated Item-Support davor oder im selben Branch.

Minimal noetig:

1. CFRU/DPE-gated ItemCount-/Itemnamen-Scope validieren und erweitern.
2. Items-Liste so dimensionieren, dass `UNIQUE_OFFSET + internalId` fuer moderne Items sicher darstellbar ist.
3. Fehlende Itemnamen mit sichtbarem Fallback behandeln.
4. Bad-/Banned-Item-Filter um moderne CFRU/DPE-Sonderbereiche erweitern.
5. Encounter-Held-Item-Read/Write ueber `item1/item2` bei `0x0C/0x0E` reload-stabil halten.
6. Placeholder-/Null-Species im Randomizer defensiv ueberspringen.

Nicht noetig fuer den minimalen Encounter-Held-Item-Fix:

- Field Items
- Shops
- Pickup
- Item-Text-/Description-Rewrite
- Move-Data-Write
- Tutor/Egg/Learnset-Ausweitung

## Empfohlener minimaler Folge-Fixpfad

Branch-Vorschlag:

- `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`

Scope:

1. `Gen3RomHandler.loadItems()` CFRU/DPE-gated erweitern:
   - aktiven `ItemData`-Pointer validieren,
   - `ItemCount` fuer den getesteten CFRU/DPE-Scope auf validierte Grenze heben,
   - Item-Liste fuer Unique-IDs robust dimensionieren,
   - Namen fallbacken.
2. `Gen3Constants` CFRU/DPE-spezifisch um moderne Banned-/Bad-Item-IDs erweitern:
   - Free-Space und Shiny-Space,
   - Key/System Items,
   - TMs/HMs,
   - Mail,
   - konservativ Form-/Mega-/Z-/Plate-/Mask-/Tera-/Booster-Sonderitems, sofern nicht bewusst erlaubt.
3. `EncounterHeldItemRandomizer` absichern:
   - Placeholder-/Null-Species skippen,
   - leeren Item-Pool stoppen oder diagnostizieren,
   - invalid/missing item IDs zaehlen.
4. Diagnose ausfuehren:
   - Encounter Held Items-only,
   - Encounter Held Items + Base Stats,
   - Encounter Held Items + Abilities/Types smoke.

## Erwartete Diagnosewerte fuer Folge-Fix

- `item.count`
- hoechste geladene Item-ID
- hoechster geladener Itemname
- `gBaseStats` Pointer-Ort und Zielpointer
- `baseStatsEntrySize=0x1C`
- `item1Offset=0x0C`
- `item2Offset=0x0E`
- Species total / hoechste Species
- Encounter-Held-Item entries before/after/reload
- hoechste Encounter-Held-Item-ID before/after/reload
- Bad-/Banned-Item count
- moderne banned item examples
- skipped Placeholder-/Null-Species
- invalid item IDs
- missing item name fallback count
- `writeReloadEncounterHeldItemMismatches`
- `saveSuccessful`
- `logSuccessful`
- `outputRomExists`
- `logNonEmpty`
- Bad Egg / `<unknown>` im Log
- Unknown-Item-Marker
- Stacktrace/Fehlerpfad bei Scheitern

## Risiken und offene Fragen

- Aktiver ItemCount muss am getesteten ROM-Modell validiert werden; CFRU und DPE Quellen nennen unterschiedliche sinnvolle Grenzen (`779` vs ca. `799`).
- DPE-Header enthaelt moderne Items und Shiny-Space-Platzhalter; nicht alle geladenen IDs duerfen randomisierbar sein.
- CFRU `asm_defines.s` und DPE `items.h` koennen bei einzelnen modernen Items voneinander abweichen, z. B. bei Mint-Konstanten.
- Bestehendes FVX-Standard-ID-Mapping ist fuer klassische Gen3-Items gebaut; moderne Unique-ID-Abbildung muss listen- und loggerfest sein.
- Wenn moderne Encounter Held Items derzeit als `null` geladen werden, kann jeder BaseStats-Save diese Felder auf `0` setzen.
- Balls/Berries/Booster Energy sind fachliche Pool-Entscheidungen; fuer P1 sollte konservativ gefiltert werden.
- Field Items, Shops und Pickup nutzen ebenfalls Itemmodelle, bleiben aber bewusst out of scope und duerfen durch den Encounter-Held-Item-Fix nicht mitveraendert werden.

## Ergebnis

Encounter Held Items sind technisch eng fixbar, weil die Daten in `gBaseStats` als `u16 item1/item2` vorliegen. Blockierend ist nicht das BaseStats-Feldmodell, sondern der zu kleine/klassische FVX-Item-Scope und der unvollstaendige Bad-/Key-Item-Filter fuer moderne CFRU/DPE-Items.

P1-Einstufung nach dieser Modellierung:

- Item-Datenmodell: teilweise verstanden, Fix erforderlich.
- Bad-/Key-Item-Filter: nicht P1-supported fuer moderne CFRU/DPE-Items.
- Encounter Held Items: noch nicht P1-supported; wahrscheinlich mit engem Item-Scope-Fix entblockbar.
