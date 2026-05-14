# 102 - CFRU/DPE Field Items Allowed-slot Reload-Smoke

Datum: 2026-05-15

Branch: `test/upr-fvx-cfru-dpe-field-items-allowed-slot-reload-smoke`

## Ziel

Dieser Block fuehrt einen engen, sanitisierten Field-Items-only Write-/Reload-Smoke fuer `FVX-ITEM-001 Field Items Shuffle` aus.

Der Smoke prueft nur den bestehenden allowed-slot Field-Items-Writer-Scope. Nicht enthalten sind Field Items Random, Random Even, Ban Bad Items, Shops, Pickup, Encounter Held Items, Trainer Held Items, Starter Held Items, TM/HM/Tutor/Learnset-Writer, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer, Wild, Evolution, Text/Menu und Scriptparser-Erweiterungen.

## Voraussetzungen

- Workspace PR #146 (`docs: record field items allowed slot guard`) wurde vor Branch-Erstellung als gemerged verifiziert.
- Branch wurde von aktuellem `origin/main` erstellt.
- Der lokale CFRU/DPE Gen9-BPRE-Kandidat war fuer diesen Field-Items-only Write-/Reload-Smoke explizit freigegeben.
- UPR-FVX bleibt auf `2697511da9a97df4c29c00dfda8b40e556020489` gepinnt.
- Kein UPR-FVX-Codefix und keine Submodule-Pin-Aenderung.

## Sanitizing

Dokumentiert werden nur aggregierte Zaehler und boolesche Ergebnisse.

Nicht dokumentiert werden private Pfade, ROM-Namen, Hashes, Raw Pointer, Offsets, Raw-Map-Daten, Script-Bytes, Logauszuege oder Output-ROM-Pfade.

Der lokale Harness und seine Output-Artefakte blieben ignored unter `05_builds/**` und wurden nicht committed.

## Smoke-Scope

Aktiv:

- `FVX-ITEM-001 Field Items Shuffle`
- `Settings.FieldItemsMod.SHUFFLE`
- `banBadRandomFieldItems=false`
- bestehender `Gen3RomHandler.getFieldItems()` / `setFieldItems(...)` allowed-slot Guard

Nicht aktiv:

- `FVX-ITEM-002 Field Items Random`
- `FVX-ITEM-003 Field Items Random even distribution`
- `FVX-ITEM-004 Field Items Ban Bad Items`
- Shops
- Pickup
- Held Items
- TM/HM/Tutor/Learnset-Ausweitung
- Scriptparser-Erweiterung

## Ergebnis

Der Field-Items-only Shuffle-Smoke war erfolgreich.

Pflichtmetriken:

- `candidateFilesChecked=94`
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
- `disallowedFieldItemWrites=0`
- `scriptPatternExpansion=0`
- `exceptionClass=none`
- `stacktrace=none`

## Preserve-/Skip-Ergebnis

Bestaetigt fuer diesen Shuffle-Smoke:

- Field-Item-Gesamtscope bleibt stabil: `339 -> 339 -> 339`.
- Reload-Mismatches bleiben `0` fuer sichtbare und Hidden-Field-Items.
- TM-Slots bleiben TM-Slots.
- Non-TM-Slots bleiben Non-TM-Slots.
- Required Field TMs bleiben nach Reload vollstaendig: `requiredFieldTMMissingAfter=0`.
- Disallowed/progression-sensitive Slots werden nicht beschrieben: `disallowedFieldItemWrites=0`, `progressionItemPolicyViolations=0`.
- Invalid/unloaded/fallback/placeholder Writes bleiben `0`.
- Die zehn nicht gematchten Itemball-Scriptmuster werden nicht erweitert oder geschrieben: `scriptPatternExpansion=0`.

## Field-Items-Statusentscheidung

- `FVX-ITEM-001` wird fuer den getesteten CFRU/DPE Gen9-BPRE-Stand als `GUI-kompatibel` im engen Shuffle-Scope bewertet.
- `FVX-ITEM-002` bleibt `Write modelliert`.
- `FVX-ITEM-003` bleibt `Write modelliert`.
- `FVX-ITEM-004` bleibt `Write modelliert`.

Begruendung:

- Der Smoke testet ausschliesslich Field Items Shuffle.
- Random, Random Even und Ban Bad Items fuehren zusaetzliche Item-Pool-/Bad-Item-Policy ein und muessen separat gesmoked werden.
- Shops und Pickup bleiben eigene Writer-Scope-Bloecke.

## Risiken / Annahmen

- Der Smoke nutzt den bestehenden UPR-FVX-Pin ohne Codeaenderung.
- Die Bewertung gilt fuer den explizit freigegebenen lokalen CFRU/DPE Gen9-BPRE-Kandidaten und den engen Shuffle-Carrier.
- Lokale UPR-FVX-Diagnoseausgaben waehrend des Laufs wurden nicht als Protokollinhalt uebernommen, weil sie Raw-Offets/Debugdetails enthalten koennen.
- `FVX-ITEM-002..004` duerfen nicht aus diesem Ergebnis hochgestuft werden.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-field-items-random-reload-smoke`

Ziel:

- Separater Field-Items-only Smoke fuer `FVX-ITEM-002 Field Items Random`.
- Ban-Bad-Items weiterhin auslassen, bis `FVX-ITEM-004` separat getestet wird.
- Erwartet sind dieselben allowed-slot-, TM-/Non-TM-, Required-TM- und preserve-only-Metriken wie in Diagnose 102.
