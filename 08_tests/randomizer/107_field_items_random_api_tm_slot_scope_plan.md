# 107 - Field Items Random API TM-slot scope plan

Datum: 2026-05-15
Branch: `analysis/upr-fvx-cfru-dpe-field-items-random-api-tm-slot-scope-plan`
Modus: read-only Planung, kein Codefix, kein Build, kein Randomizer-Lauf, kein ROM-/Output-Artefakt dokumentiert

## Ausgangslage

Workspace PR #151 (`docs: record field items random tm pool smoke`) ist gemerged. Der Workspace steht weiter auf dem UPR-FVX-Pin `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd`.

Diagnose 106 zeigt:

- `candidateLoaded=true`
- `smokeExecuted=true`
- `randomTmPoolDeficit=0`
- `randomTmLoadedPoolSize=50`
- `randomTmUniquePoolSize=50`
- `randomTmNeededSlots=0`
- `randomTmCurrentSlots=0`
- `randomTmRequiredTotal=24`
- `exceptionClass=RandomizationException`
- kein Save-/Output-/Reload-Ergebnis

Die Raw-Map-/Script-Diagnosen aus 100/101/102 belegen gleichzeitig:

- `fieldItemsTotal=339`
- `allowedFieldItemSlots=280`
- `disallowedFieldItemSlots=59`
- `tmFieldItemSlots=28`
- `nonTmFieldItemSlots=311`
- `requiredFieldTMsTotal=24`
- `requiredFieldTMPresent=24`
- `requiredFieldTMMissing=0`
- `scriptPatternUnmatchedItemBalls=10`

## Gelesene Dateien

Workspace-Dokumente:

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/097_field_items_shops_pickup_scope_plan.md`
- `08_tests/randomizer/098_field_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/099_field_items_scope_diagnostics.md`
- `08_tests/randomizer/100_field_items_scope_diagnostics_candidate.md`
- `08_tests/randomizer/101_field_items_allowed_slot_write_guard.md`
- `08_tests/randomizer/102_field_items_allowed_slot_reload_smoke.md`
- `08_tests/randomizer/103_field_items_random_reload_smoke.md`
- `08_tests/randomizer/104_field_items_random_tm_pool_blocker_plan.md`
- `08_tests/randomizer/105_field_items_random_tm_pool_fix.md`
- `08_tests/randomizer/106_field_items_random_tm_pool_reload_smoke.md`
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

UPR-FVX-Codepfade, read-only:

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractRomHandler.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/ItemRandomizer.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/constants/Gen3Constants.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Item.java`

## Codepfad-Befund

`Gen3RomHandler.preprocessMaps()` sammelt Field-Item-Offsets in `itemOffs` aus:

- sichtbaren Itemball-Scripts, wenn das bekannte Scriptmuster erkannt wird
- Hidden-Item-Signposts, wenn der Signpost-Typ passt und die Item-ID nicht `0` ist

`Gen3RomHandler.getFieldItems()` iteriert danach ueber `itemOffs`, liest die Item-ID und gibt den Slot nur zurueck, wenn `item.isAllowed()` wahr ist.

`Gen3RomHandler.setFieldItems(...)` nutzt denselben Filter: Es iteriert wieder ueber `itemOffs` und schreibt nur Slots, deren aktuelles Item `current.isAllowed()` ist.

`ItemRandomizer.randomizeFieldItems(...)` arbeitet ausschliesslich auf `romHandler.getFieldItems()`. Die Aufteilung in `tms` und `nonTMs` passiert erst nach diesem API-Filter ueber `item.isTM()`.

`ItemRandomizer.randomizeTMFieldItems(...)` bekommt daher nicht die Raw-TM-Slots, sondern nur TM-Slots, die bereits im `getFieldItems()`-API-Scope enthalten sind.

`AbstractRomHandler.checkFieldItemsTMsReplaceTMs(...)` vergleicht ebenfalls `getFieldItems()` mit der Replacement-Liste. Der Sicherheitscheck sieht damit nur die API-Slotliste, nicht den breiteren Raw-Map-/Script-Befund.

`Gen3RomHandler.loadItems()` setzt CFRU/DPE-spezifische Fallback-/unsafe Items auf `allowed=false` und markiert TM01..TM50 als `tm=true`. Diagnose 106 zeigt, dass TMs geladen und als Pool nutzbar sind (`randomTmLoadedPoolSize=50`, `randomTmUniquePoolSize=50`), aber im Field-Items-API-Scope keine TM-Slots sichtbar werden (`randomTmNeededSlots=0`, `randomTmCurrentSlots=0`).

## Blocker-Einschaetzung

Der aktive Blocker ist kein verbleibender TM-Filler-Pool-Defekt aus PR #36. Der Pool-Defizit-Zaehler ist `0`.

Der Blocker ist eine Scope-Differenz zwischen:

- Raw-Map-/Script-Diagnose: zaehlt alle erkannten Field-Item-Slots und klassifiziert darunter `28` TM-Slots.
- Randomizer-API: `getFieldItems()` gibt nur Slots mit `item.isAllowed()` zurueck und liefert im CFRU/DPE-Kandidaten fuer den Randomizer-Pfad `0` TM-Slots.

Damit trifft `randomizeTMFieldItems(...)` auf:

- benoetigte TM-Slots aus API-Sicht: `0`
- Required Field TMs: `24`

Der neue Guard aus PR #36 blockiert korrekt, weil Required Field TMs nicht in `0` sichtbare API-TM-Slots passen.

Interpretation: Die TM-Field-Item-Slots sind raw vorhanden und required-TM-stabil, werden aber durch den bestehenden `item.isAllowed()`-basierten Field-Items-API-Scope aus dem Randomizer-Pfad herausgefiltert.

## Antworten auf die Planfragen

1. Raw-Diagnose findet `tmFieldItemSlots=28`, weil sie breiter auf Map-/Script-/Signpost-Slots schaut als `romHandler.getFieldItems()`.
2. Ja. Der bestehende API-Pfad filtert Field Items ueber `Item::isAllowed`; TMs, die im CFRU/DPE-Itemmodell nicht allowed sind, erreichen `ItemRandomizer.randomizeTMFieldItems(...)` nicht.
3. Ja. TMs sind geladen und als `Item::isTM` markiert; Diagnose 106 zeigt einen geladenen Unique-TM-Pool von `50`. Der API-Slot-Scope bleibt dennoch `0`, weil die Slotaufnahme an `isAllowed()` haengt.
4. Ja. Die Raw-Diagnose ist bewusst breiter als der bestehende allowed-slot API-Scope.
5. Ein spaeterer Fix muss entweder TMs im Field-Items-API-Scope gezielt erlauben, einen getrennten TM-Field-Items-API-Pfad einfuehren oder den Field-Items-Random-TM-Pfad auf raw klassifizierte Slotkandidaten stuetzen.
6. Risiken liegen bei Required Field TMs, TM-/Non-TM-Slottreue, disallowed/progression/key/system Slots und dem bestehenden `checkFieldItemsTMsReplaceTMs(...)`-Invarianzcheck.
7. Ein Fix kann eng auf `FVX-ITEM-002` bleiben, wenn er nur den CFRU/DPE-Field-Items-Random-TM-Slot-Scope erweitert und keine globalen Item-Allow-Listen, Shops, Pickup, Held Items oder TM/HM/Tutor/Learnset-Pfade aendert.

## Moegliche Fix-Optionen

### Option A - CFRU/DPE Field-Items-API laesst TM-Slots gezielt zu

`Gen3RomHandler.getFieldItems()` / `setFieldItems(...)` wuerden im sicheren CFRU/DPE-Gen9-BPRE-Gate Field-Item-Slots aufnehmen, wenn das aktuelle Item entweder `allowed` oder ein Field-TM-Slot ist.

Vorteile:

- kleinstmoegliche Aenderung nahe am bestehenden API-Vertrag
- `ItemRandomizer.randomizeFieldItems(...)` kann weiter unveraendert in TM/Non-TM splitten
- `checkFieldItemsTMsReplaceTMs(...)` bleibt nutzbar, wenn Current- und Replacement-Listen dieselbe API-Slotreihenfolge haben

Risiken:

- Der Field-Items-API-Scope wird breiter; das muss CFRU/DPE-gated und auf Field Items begrenzt bleiben.
- TMs duerfen dadurch nicht global fuer Shops, Pickup oder Held Items allowed werden.
- Die erwartete API-Slotanzahl aendert sich und muss im Smoke separat gemessen werden.

### Option B - Getrennter TM-Field-Items-API-Pfad

Ein neuer enger Helper liefert nur Field-TM-Slots fuer `FVX-ITEM-002`, waehrend `getFieldItems()` den bisherigen allowed-slot Scope behaelt.

Vorteile:

- bestehender API-Vertrag bleibt stabil
- Required-TM-/TM-Slot-Policy kann explizit modelliert werden

Risiken:

- invasiver als Option A, weil `ItemRandomizer` oder `RomHandler` API erweitert werden muesste
- hoeheres Review-Risiko durch neue Writer-Oberflaeche

### Option C - Raw-Slot-Metadatenmodell fuer Field Items

Spaeteres Modell mit Slottyp, Raw-ID, API-Policy, Visible/Hidden, TM/Non-TM, allowed/disallowed und preserve-only Status.

Vorteile:

- fachlich sauberste Trennung zwischen Raw-Diagnose und Write-Policy
- kann langfristig `FVX-ITEM-003` und `FVX-ITEM-004` besser absichern

Risiken:

- groesserer Refactor, nicht passend fuer den naechsten engen `FVX-ITEM-002`-Fix
- hoeheres Risiko, versehentlich Shops/Pickup/Held Items oder Scriptparser-Logik mitzuziehen

### Nicht empfohlene Option - TMs global allowed setzen

TMs global `allowed=true` zu setzen, waere zu breit. Das koennte Shops, Pickup, Held Items oder andere Item-Pools veraendern und ist fuer den engen Field-Items-Random-TM-Slot-Blocker nicht reviewbar.

## Empfehlung

Naechster minimaler Fix: Option A als enger CFRU/DPE-gated Field-Items-API-TM-Slot-Fix pruefen.

Der Fix sollte nur im Field-Items-API-/Writer-Scope wirken und nur fuer aktuell erkannte Field-Item-Slots gelten. TMs duerfen nicht global allowed werden.

Wenn Option A im Code zu breit wird oder den bestehenden `checkFieldItemsTMsReplaceTMs(...)`-Vergleich unsauber macht, auf Option B wechseln. Option C bleibt eine spaetere Strukturverbesserung, nicht der naechste P1-Fix.

## Preserve-/Skip-Policy fuer einen spaeteren Fix

Preserve-only bleibt unveraendert fuer:

- `disallowedFieldItemSlots=59`, sofern nicht gezielt als TM-Field-Slot im engen CFRU/DPE-Gate freigegeben
- progression-/key-/system-sensitive Slots
- invalid/unloaded/fallback/placeholder Slots
- `scriptPatternUnmatchedItemBalls=10`
- nicht erkannte Script-/Map-Strukturen
- Shops
- Pickup
- Encounter Held Items
- Trainer Held Items
- Starter Held Items
- TM/HM/Tutor/Learnset-Writer
- Palette/Graphics
- MoveData/MoveNames
- TypeChart/TypeEffectiveness
- Trainer/Wild/Evolution/Text/Menu

Schreibpolicy:

- Write nur ueber den bestehenden Field-Items-Slot-Scope plus eng freigegebene CFRU/DPE TM-Field-Slots.
- TM-Slots bleiben TM-Slots.
- Non-TM-Slots bleiben Non-TM-Slots.
- Required Field TMs muessen vollstaendig erhalten bleiben.
- Ban-Bad-Items bleibt fuer diesen Fix inaktiv.
- Keine Scriptparser-Erweiterung.

## Spaetere Smoke-/Reload-Kriterien

Pflicht fuer den naechsten Fix-/Smoke-Block:

- `candidateLoaded=true`
- `smokeExecuted=true`
- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- `reloadSuccessful=true`
- `fieldItemsTotalBefore=339`
- `fieldItemsTotalAfter=339`
- `fieldItemsTotalReload=339`
- `fieldItemReloadMismatches=0`
- `visibleFieldItemReloadMismatches=0`
- `hiddenFieldItemReloadMismatches=0`
- `tmFieldItemSlotMismatches=0`
- `nonTmFieldItemSlotMismatches=0`
- `requiredFieldTMMissingAfter=0`
- `requiredItemPolicyViolations=0`
- `progressionItemPolicyViolations=0`
- `invalidFieldItemWrites=0`
- `unloadedFieldItemWrites=0`
- `fallbackFieldItemWrites=0`
- `placeholderFieldItemWrites=0`
- `disallowedFieldItemWrites=0`, ausser separat als `apiTmFieldSlotWrites` fuer die eng freigegebenen TM-Slots gezaehlt
- `scriptPatternExpansion=0`
- `badFieldItemWrites=0` oder `not evaluated`, weil `banBadRandomFieldItems=false`
- `randomTmNeededSlots=28`
- `randomTmCurrentSlots=28`
- `randomTmRequiredTotal=24`
- `randomTmRequiredPresent=24`
- `randomTmRequiredMissingBefore=0`
- `randomTmRequiredMissingAfter=0`
- `randomTmLoadedPoolSize=50`
- `randomTmUniquePoolSize >= 28`
- `randomTmFillerNeeded=4`
- `randomTmFillerAvailable >= 4`
- `randomTmDuplicateSelections=0`
- `randomTmPoolDeficit=0`
- `randomTmResultSize=28`
- `randomTmResultUniqueSize=28`
- `exceptionClass=none`
- `stacktrace=none`

Zusaetzliche API-Scope-Metriken fuer den Fix:

- `apiFieldItemsTotal`
- `apiTmFieldItemSlots=28`
- `apiNonTmFieldItemSlots`
- `rawTmFieldItemSlots=28`
- `rawApiTmSlotAlignmentMismatches=0`
- `tmGloballyAllowedChanged=false`
- `shopItemScopeChanged=false`
- `pickupItemScopeChanged=false`
- `heldItemScopeChanged=false`

## Feature-Status

- `FVX-ITEM-001 Field Items Shuffle`: bleibt `GUI-kompatibel` im getesteten engen allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random`: bleibt `Write modelliert` / blockiert bis API-TM-Slot-Scope-Fix plus Reload-Smoke erfolgreich sind.
- `FVX-ITEM-003 Field Items Random even distribution`: bleibt `Write modelliert`.
- `FVX-ITEM-004 Field Items Ban Bad Items`: bleibt `Write modelliert`.

## Naechster minimaler Schritt

Branch: `compat/upr-fvx-cfru-dpe-field-items-api-tm-slot-scope-fix`

Ziel: minimalen CFRU/DPE-gated Field-Items-API-TM-Slot-Fix pruefen, ohne TMs global allowed zu setzen und ohne Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even oder Ban Bad Items auszuweiten.
