# 114 - CFRU/DPE Pickup Items Scope Diagnostics Plan

Datum: 2026-05-15

## Ziel

Dieser Block plant read-only den naechsten getrennten Item-Writer-Scope fuer Pickup Items im CFRU/DPE Gen9-BPRE-Stand. Es wird kein Fix umgesetzt, kein Randomizer-Lauf ausgefuehrt, kein Build gestartet und kein ROM-/Output-Artefakt dokumentiert.

Pickup bleibt getrennt von Field Items, Shops, Encounter Held Items, Trainer Held Items, Starter Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer/Wild/Evolution, Text/Menu und Scriptparser-Arbeit.

## Voraussetzungen / Ausgangsstand

- Workspace PR #158 (`docs: record field items random even ban bad smoke`) wurde vor Branch-Erstellung als gemerged verifiziert.
- Branch wurde von aktuellem `origin/main` erstellt.
- Workspace-Submodule `02_external/upr-fvx` bleibt auf `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Field Items `FVX-ITEM-001..004` sind im getesteten engen Field-Items-only Scope GUI-kompatibel.
- Shops und Pickup bleiben separate Writer-Scope-Bloecke.

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/097_field_items_shops_pickup_scope_plan.md`
- `08_tests/randomizer/113_field_items_random_even_ban_bad_reload_smoke.md`
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

Optionaler Kontext aus Field-Items-Diagnosen 098 bis 113 wurde nur zur Abgrenzung herangezogen.

## Relevante Codepfade

### GUI / Settings / Orchestrierung

- `Settings.PickupItemsMod`: `UNCHANGED`, `RANDOM`.
- `Settings.banBadRandomPickupItems`: Ban-Bad-Filter fuer Pickup-Item-Pool.
- `GameRandomizer.maybeRandomizePickupItems()`: ruft `ItemRandomizer.randomizePickupItems()` nur bei `PickupItemsMod.RANDOM` auf.
- GUI-Pfade: `RandomizerGUI` setzt `puRandomRadioButton` und `puBanBadItemsCheckBox`; `Bundle.properties` beschreibt `Pickup Items`, `Random` und `Ban Bad Items`.

### Randomizer

`ItemRandomizer.randomizePickupItems()`:

- waehlt den Pool aus `romHandler.getAllowedItems()` oder bei aktivem Ban Bad aus `romHandler.getNonBadItems()`.
- entfernt TMs, wenn `!romHandler.canTMsBeHeld()` oder `romHandler.isTMsReusable()`.
- liest aktuelle Eintraege via `romHandler.getPickupItems()`.
- erzeugt fuer jeden aktuellen Pickup-Slot ein neues `PickupItem` mit zufaelligem Item.
- kopiert die `PickupItem.PROBABILITY_SLOTS` aus dem aktuellen Eintrag in das neue Modell.
- schreibt via `romHandler.setPickupItems(newItems)`.

### Gen3 ROM-Handler

`Gen3RomHandler.getPickupItems()`:

- nutzt `PickupItemCount` aus der ROM-Entry-Konfiguration.
- nutzt `PickupTableStartLocator`, um die Tabelle per Byte-Pattern zu lokalisieren.
- setzt die Entry-Groesse auf `2` fuer Emerald, sonst `4`.
- liest pro Eintrag ein `u16` Item-Feld und mappt ueber `Gen3Constants.itemIDToStandard(...)`.
- fuellt Wahrscheinlichkeiten modellseitig anhand des Rom-Typs:
  - Ruby/Sapphire: klassische 10er-Verteilung.
  - FRLG: 16 Eintraege mit festen Levelbereich-Wahrscheinlichkeiten.
  - Emerald/sonstige Gen3-Typen: 29er-Common/Rare-Layout mit Levelbereich-Semantik.

`Gen3RomHandler.setPickupItems(...)`:

- schreibt nur die Item-ID-Felder in die lokalisierte Tabelle zurueck.
- nutzt dieselbe Entry-Groesse wie `getPickupItems()`.
- schreibt `Gen3Constants.itemIDToInternal(pickupItems.get(i).getItem().getId())` als `u16`.
- schreibt keine Wahrscheinlichkeitsspalten separat.

### API / Modell

- `RomHandler.getPickupItems()` / `setPickupItems(...)` definieren den generischen Pickup-Writer-Vertrag.
- `AbstractRomHandler.getAllowedItems()` liefert nur geladene allowed Items.
- `AbstractRomHandler.getNonBadItems()` filtert `getAllowedItems()` um `!item.isBad()`.
- `PickupItem.PROBABILITY_SLOTS=10`; `PickupItem.equals(...)` vergleicht Item und Wahrscheinlichkeiten.
- Vorhandene Tests decken klassische ROMs ab: Get/Set bleibt stabil, Ban Bad entfernt Bad Items, TMs werden je nach Holdable-/Reusable-Policy erlaubt oder entfernt.

## Pickup-Scope-Einschaetzung

Pickup ist ein eigener enger Table-Writer, aber vor einem Write-Smoke braucht er eine read-only Kandidatendiagnose.

Begruendung:

- Der Gen3-Pfad sucht die Tabelle ueber `PickupTableStartLocator`; fuer CFRU/DPE muss zuerst belegt werden, dass der Locator die aktive Pickup-Tabelle trifft.
- FRLG erwartet klassisch `PickupItemCount=16`; CFRU/DPE kann eine modernisierte oder andere Pickup-Struktur verwenden.
- `getPickupItems()` modelliert Wahrscheinlichkeiten aus dem Rom-Typ statt sie aus einer separaten Probability-Tabelle zu lesen.
- `setPickupItems(...)` schreibt nur Item-IDs; ein spaeterer Smoke muss deshalb nachweisen, dass Tabellenlaenge, Slotreihenfolge und Reload der Item-IDs stabil bleiben und keine Common/Rare-/Probability-Semantik versehentlich verletzt wird.
- Ban Bad ist nur ein Poolfilter und sollte nach einem Random-ohne-Ban-Smoke separat getestet werden.

Betroffene Feature-ID:

- `FVX-ITEM-010 Pickup Items Random / Ban Bad Items`.

## Erwartete Datenstruktur / offene Diagnosefragen

Der aktuelle Gen3-BPRE-Pfad erwartet fuer FRLG:

- eine per Locator gefundene flache Pickup-Tabelle.
- `PickupItemCount=16`.
- ein Item-ID-Feld pro Eintrag, bei non-Emerald Entry-Groesse `4`.
- 10 modellierte Probability-Slots pro Eintrag.
- feste FRLG-Wahrscheinlichkeitsverteilung pro Levelbereich.

Die read-only Kandidatendiagnose muss klaeren:

- ob `pickupLocatorSuccessful=true` ist.
- ob `pickupItemsTotal=16` oder ein anderer CFRU/DPE-Wert vorliegt.
- ob alle gelesenen Item-IDs valide, geladen und sinnvoll gemappt sind.
- ob die aktuelle Tabelle Common/Rare-Semantik oder nur klassische FRLG-Semantik abbildet.
- ob Duplicate-/Bad-/Fallback-/Placeholder-/Modern-Items im aktuellen Pickup-Scope vorkommen.
- ob TMs/HMs in Pickup-Slots vorhanden oder nach Policy ausgeschlossen sind.
- ob `canTMsBeHeld` und `isTMsReusable` fuer den aktiven Stand TMs aus dem Pickup-Random-Pool entfernen.

## Risiken

- Locator trifft eine klassische FRLG-Tabelle, aber nicht den aktiven CFRU/DPE-Pickup-Pfad.
- CFRU/DPE nutzt Common/Rare- oder Levelbereichstabellen, die vom aktuellen `PickupItemCount`/Entry-Size-Modell nur teilweise getroffen werden.
- Probability-Slots werden nur modelliert und nicht aus separaten Daten gelesen; ein Write-Smoke kann Item-ID-Stabilitaet beweisen, aber keine unbekannte externe Probability-Tabelle reparieren.
- `setPickupItems(...)` schreibt so viele Eintraege, wie der Randomizer liefert; eine falsche Tabellenlaenge waere ein Writer-Risiko.
- Moderne Item-IDs koennen geladen sein, muessen aber allowed/non-bad/fallback-sicher sein.
- Bad-/Banned-Policy aus Field Items darf nicht blind uebernommen werden; Pickup nutzt `banBadRandomPickupItems` und `getNonBadItems()` separat.
- TMs sind wegen `canTMsBeHeld()` und `isTMsReusable()` pfadspezifisch zu behandeln und duerfen nicht mit Field-TM-Slots verwechselt werden.

## Preserve-/Skip-Policy

Fuer Pickup-only Folgeblocks gilt:

- Erst read-only klassifizieren, dann schreiben.
- Nur geladene, valide Pickup-Slots schreiben, deren Tabelle durch den Locator eindeutig gefunden wurde.
- Tabellenlaenge und Slotreihenfolge muessen erhalten bleiben.
- Probability-Slots muessen im Modell unveraendert bleiben; bei unbekannter externer Probability-/Common-/Rare-Struktur keine Write-Freigabe.
- Invalide, unloaded, fallback, placeholder oder nicht gemappte Items nicht als Random-Picks verwenden.
- Bad Items nur bei `banBadRandomPickupItems=true` ausschliessen; zuerst Random ohne Ban Bad testen.
- TMs nur entsprechend `canTMsBeHeld()` und `isTMsReusable()` zulassen; keine globale TM-Allow-Policy ableiten.
- Keine Shops, Field Items, Encounter Held Items, Trainer Held Items oder Starter Held Items beruehren.
- Keine TM/HM/Tutor/Learnset-Ausweitung.

## Spaetere Diagnosemetriken

Ein read-only Pickup-Kandidatendiagnoseblock sollte mindestens aggregiert berichten:

```text
candidateFilesChecked
candidateLoaded
pickupScanSuccessful
pickupLocatorSuccessful
pickupItemsTotal
pickupExpectedCount
pickupEntrySize
pickupProbabilitySlots
pickupProbabilityModelStable
pickupUniqueItems
pickupDuplicateItems
pickupAllowedItems
pickupDisallowedItems
pickupBadItems
pickupTmItems
pickupNonTmItems
pickupModernItemIds
pickupInvalidItemIds
pickupUnloadedItemIds
pickupFallbackItems
pickupPlaceholderItems
pickupCommonSlots
pickupRareSlots
pickupCommonRareModelDetected
pickupTableLengthMismatch
pickupPoolAllowedSize
pickupPoolNonBadSize
pickupTmPoolPolicy
canTMsBeHeld
isTMsReusable
exceptionClass
stacktrace
```

Sanitizing: keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes, Logs oder Output-ROM-Pfade dokumentieren.

## Spaetere Smoke-/Reload-Kriterien

### Pickup Random ohne Ban Bad

```text
candidateLoaded=true
smokeExecuted=true
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
reloadSuccessful=true
pickupLocatorSuccessful=true
pickupItemsTotalBefore == pickupItemsTotalAfter
pickupItemsTotalAfter == pickupItemsTotalReload
pickupItemReloadMismatches=0
pickupTableLengthMismatches=0
pickupProbabilityMismatches=0
pickupCommonRarePolicyViolations=0
invalidPickupItemWrites=0
unloadedPickupItemWrites=0
fallbackPickupItemWrites=0
placeholderPickupItemWrites=0
badPickupItemWrites=not evaluated or documented
pickupTmPolicyViolations=0
shopItemScopeChanged=false
fieldItemScopeChanged=false
heldItemScopeChanged=false
exceptionClass=none
stacktrace=none
```

### Pickup Random mit Ban Bad

Zusaetzlich:

```text
banBadRandomPickupItems=true
badPickupItemWrites=0
badPickupPoolCandidates documented
badPickupPoolExcluded documented
nonBadPickupPoolSize > 0
pickupItemReloadMismatches=0
exceptionClass=none
stacktrace=none
```

## Empfohlene Reihenfolge

1. `test/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics`
   - read-only Kandidatendiagnose.
   - Ziel: Locator, Tabellenlaenge, Item-ID-Validitaet, Probability-Modell, Common/Rare-Hinweise und Pool-Sicherheit aggregiert belegen.

2. `test/upr-fvx-cfru-dpe-pickup-items-random-reload-smoke`
   - nur `FVX-ITEM-010 Pickup Items Random` mit `banBadRandomPickupItems=false`.
   - Ziel: Item-ID-Write-/Reload-Stabilitaet ohne Ban-Bad-Komplexitaet.

3. `test/upr-fvx-cfru-dpe-pickup-items-random-ban-bad-reload-smoke`
   - nur wenn Random ohne Ban Bad stabil ist.
   - Ziel: Ban-Bad-Poolfilter fuer Pickup separat belegen.

## Nicht-Hochstufung anderer Scopes

- Field Items bleiben durch Diagnose 113 abgeschlossen, werden in Pickup-Folgeblocks aber nicht erneut hochgestuft.
- Shops bleiben eigener Repointing-/Terminator-/Preis-Scope.
- Encounter Held Items, Trainer Held Items und Starter Held Items bleiben getrennte Itempfade.
- TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer/Wild/Evolution und Text/Menu bleiben ausserhalb.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics`: sanitisierten read-only Pickup-only Kandidatendiagnose-Lauf planen/ausfuehren, falls ein lokaler CFRU/DPE Gen9-BPRE-Kandidat explizit freigegeben ist. Ohne Kandidatenfreigabe als blockierte Diagnose dokumentieren.
