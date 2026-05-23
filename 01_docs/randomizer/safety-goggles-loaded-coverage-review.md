# Safety Goggles Loaded Coverage Review

## Executive Summary

`Safety Goggles` wirkt nicht wie ein echter ItemData-Load-Fehler. Der erwartete Source-Constant existiert lokal, und die CFRU/DPE ItemData-Tabelle enthaelt einen Eintrag fuer dieselbe Item-ID. Der wahrscheinliche Grund fuer den verbleibenden `EXPECTED_NOT_LOADED` ist ein lokaler Anzeigename: Die ItemData setzt den Namen auf `Safe Guard`, waehrend der Coverage Auditor aus `ITEM_SAFETY_GOGGLES` den Expected-Key `safety_goggles` ableitet.

Empfohlene Folge: **Alias im Auditor ergaenzen**: `Safe Guard` bzw. normalisiert `safeguard` sollte im Item-Alias-Layer auf `Safety Goggles` gemappt werden.

## Findings

| Frage | Ergebnis | Evidence |
| --- | --- | --- |
| Existiert `ITEM_SAFETY_GOGGLES` als Source-Constant? | Ja. | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/items.h` und `02_external/CFRU-expansion/include/constants/items.h` definieren `ITEM_SAFETY_GOGGLES 0x2CA`. |
| Gibt es CFRU/DPE ItemData fuer den Eintrag? | Ja. | `02_external/CFRU-expansion/src/Tables/item_tables.c` enthaelt einen ItemData-Eintrag mit `.itemId = ITEM_SAFETY_GOGGLES`, Preis, `ITEM_EFFECT_SAFETY_GOGGLES`, Description und Held-Item-Metadaten. |
| Wird der geladene Name wahrscheinlich anders exportiert? | Ja. | Dieselbe ItemData setzt `.name = {_S, _a, _f, _e, _SPACE, _G, _u, _a, _r, _d, _END}`, also `Safe Guard`. |
| Ist der Auditor-Alias aktuell vorhanden? | Nein. | `ITEM_ALIAS_DISPLAY` enthaelt viele lokale Kurz-/Ingame-Namen, aber keinen `safeguard -> Safety Goggles`-Eintrag. |
| Ist ein echter Randomizer-/ItemData-Fix belegt? | Nein. | Source-Constant und ItemData sind vorhanden; der Load-Manifest-Exporter exportiert Items aus `romHandler.getItems()` mit `item.getName()`, also dem geladenen Anzeigenamen. |

## Code Path Notes

- Expected-Index:
  - `randomizer_coverage_auditor.py` liest `ITEM_*`-Constants aus lokalen DPE/CFRU-Headers.
  - `ITEM_SAFETY_GOGGLES` wird zu Display `Safety Goggles` und canonical key `safety_goggles`.
- ROM-load / Loaded-Manifest:
  - `Gen3RomHandler.loadItems()` liest Itemnamen aus der ROM-ItemData und erzeugt `Item(id, name)`.
  - `LoadedManifestExporter.writeItemsManifest()` schreibt `canonicalize(tmHmLabel(item))`, `item.getName()` und `item.getId()`.
  - Bei lokalem CFRU/DPE-ItemData-Namen `Safe Guard` waere der loaded canonical key `safe_guard`, nicht `safety_goggles`.
- Compare:
  - Der Auditor vergleicht Items bewusst primaer ueber canonical/name aliases, nicht ueber rohe Item-IDs, weil CFRU/DPE Source-IDs und UPR-FVX Standard-IDs kollidieren koennen.
  - Ohne Alias sind `safety_goggles` und `safe_guard` unterschiedliche Keys.

## Interpretation

Das sieht nach einem Alias-/Loaded-Name-Problem aus, nicht nach einem fehlenden Item:

- `ITEM_SAFETY_GOGGLES` ist in beiden lokalen Constant-Quellen vorhanden.
- Die ItemData ist vorhanden und nutzt die erwartete Item-ID.
- Battle-/Held-Item-Metadaten referenzieren den Safety-Goggles-Effekt.
- Der einzige Bruch ist der lokale ItemData-Anzeigename `Safe Guard`.

Die verbleibende Unsicherheit ist, dass Codex kein privates ROM und kein echtes loaded manifest gelesen hat. Aus den lokalen Source-Tabellen ist aber plausibel, dass Antons `items_loaded.tsv` den Eintrag als `Safe Guard` exportiert.

## Recommended Follow-Up

Genau eine Folge: **Alias im Auditor ergaenzen**.

Konkreter Fix-Vorschlag fuer einen separaten Tooling-Branch:

- In `ITEM_ALIAS_DISPLAY` `safeguard: "Safety Goggles"` ergaenzen.
- Einen ROM-freien Unit-Test hinzufuegen:
  - `canonical_key_for_observed("Safe Guard", "item") == "safety_goggles"`.
  - Expected `ITEM_SAFETY_GOGGLES` plus loaded `Safe Guard` ergibt nicht `EXPECTED_NOT_LOADED`, sondern `LOADED_NOT_OBSERVED` oder `EXPECTED_AND_OBSERVED`.

Kein UPR-FVX- oder ItemData-Fix erscheint auf Basis dieser Evidence noetig.
