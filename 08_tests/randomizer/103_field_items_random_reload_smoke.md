# 103 - CFRU/DPE Field Items Random Reload-Smoke

Datum: 2026-05-15

Branch: `test/upr-fvx-cfru-dpe-field-items-random-reload-smoke`

## Ziel

Dieser Block fuehrt einen engen, sanitisierten Field-Items-only Write-/Reload-Smoke fuer `FVX-ITEM-002 Field Items Random` aus.

Der Smoke prueft nur `Settings.FieldItemsMod.RANDOM` mit `banBadRandomFieldItems=false` auf dem bestehenden UPR-FVX-Pin `2697511da9a97df4c29c00dfda8b40e556020489`.

Nicht enthalten sind Field Items Shuffle, Random Even Distribution, Ban Bad Items, Shops, Pickup, Encounter Held Items, Trainer Held Items, Starter Held Items, TM/HM/Tutor/Learnset-Writer, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer, Wild, Evolution, Text/Menu und Scriptparser-Erweiterungen.

## Voraussetzungen

- Workspace PR #147 (`docs: record field items reload smoke`) wurde vor Branch-Erstellung als gemerged verifiziert.
- Branch wurde von aktuellem `origin/main` erstellt.
- Der lokale CFRU/DPE Gen9-BPRE-Kandidat war fuer diesen Field-Items-only Write-/Reload-Smoke explizit freigegeben.
- Kein UPR-FVX-Codefix und keine Submodule-Pin-Aenderung.

## Sanitizing

Dokumentiert werden nur aggregierte Zaehler und boolesche Ergebnisse.

Nicht dokumentiert werden private Pfade, ROM-Namen, Hashes, Raw Pointer, Offsets, Raw-Map-Daten, Script-Bytes, Logauszuege oder Output-ROM-Pfade.

Der lokale Harness und seine Output-Artefakte blieben ignored unter `05_builds/**` und wurden nicht committed.

## Smoke-Scope

Aktiv:

- `FVX-ITEM-002 Field Items Random`
- `Settings.FieldItemsMod.RANDOM`
- `banBadRandomFieldItems=false`
- bestehender `Gen3RomHandler.getFieldItems()` / `setFieldItems(...)` allowed-slot Guard

Nicht aktiv:

- `FVX-ITEM-001 Field Items Shuffle`
- `FVX-ITEM-003 Field Items Random even distribution`
- `FVX-ITEM-004 Field Items Ban Bad Items`
- Shops
- Pickup
- Held Items
- TM/HM/Tutor/Learnset-Ausweitung
- Scriptparser-Erweiterung

## Ergebnis

Der Field-Items-only Random-Smoke ist fachlich blockiert.

Der Kandidat wurde geladen und der Field-Items-Scope wurde vor dem Save stabil erfasst, aber der Randomizer brach beim Save mit `RandomizationException` ab. Es wurde keine Output-ROM erzeugt und kein Reload ausgefuehrt.

Pflichtmetriken:

- `candidateFilesChecked=9`
- `candidateLoaded=true`
- `smokeExecuted=true`
- `saveSuccessful=false`
- `logSuccessful=true`
- `outputRomExists=false`
- `logNonEmpty=false`
- `reloadSuccessful=false`
- `fieldItemsTotalBefore=339`
- `fieldItemsTotalAfter=339`
- `fieldItemsTotalReload=0`
- `fieldItemReloadMismatches=339`
- `visibleFieldItemReloadMismatches=339`
- `hiddenFieldItemReloadMismatches=339`
- `tmFieldItemSlotMismatches=339`
- `nonTmFieldItemSlotMismatches=339`
- `requiredFieldTMMissingAfter=0`
- `requiredItemPolicyViolations=0`
- `progressionItemPolicyViolations=0`
- `invalidFieldItemWrites=0`
- `unloadedFieldItemWrites=0`
- `fallbackFieldItemWrites=0`
- `placeholderFieldItemWrites=0`
- `disallowedFieldItemWrites=0`
- `scriptPatternExpansion=0`
- `badFieldItemWrites=0`
- `exceptionClass=com.uprfvx.random.exceptions.RandomizationException`
- `stacktrace=com.uprfvx.random.exceptions.RandomizationException`

Interpretation der Mismatch-Zaehler:

- Die Reload-Mismatch-Zaehler sind Folge des fehlenden Output-ROM-/Reloads, nicht ein bestaetigter persistierter Field-Item-Write-Mismatch.
- `fieldItemsTotalBefore=339` und `fieldItemsTotalAfter=339` zeigen, dass der erkannte Field-Items-Scope bis zum Abbruch stabil blieb.
- Preserve-/Skip-Zaehler bleiben bis zum Abbruch unauffaellig: keine disallowed, invalid, unloaded, fallback oder placeholder writes.

## Blocker-Einordnung

Read-only Codepruefung des engen Pfads:

- `ItemRandomizer.randomizeFieldItems()` trennt allowed Field Items in TM- und Non-TM-Slots.
- Bei `Settings.FieldItemsMod.RANDOM` wird zuerst `randomizeTMFieldItems(...)` und danach `randomizeNonTMFieldItems(...)` ausgefuehrt.
- `randomizeTMFieldItems(...)` kann eine `RandomizationException` werfen, wenn der TM-Field-Item-Pool nicht auf die benoetigte Slotanzahl gebracht werden kann.
- Der Blocker liegt damit im Field-Items-Random-TM-Pool-Scope, nicht im allowed-slot Preserve-Guard.

## Preserve-/Skip-Ergebnis

Bis zum Abbruch bestaetigt:

- Field-Item-Gesamtscope bleibt vor/nach Randomizer-Abbruch stabil: `339 -> 339`.
- Required Field TMs fehlen nach dem Abbruch nicht: `requiredFieldTMMissingAfter=0`.
- Disallowed/progression-sensitive Slots werden nicht beschrieben: `disallowedFieldItemWrites=0`, `progressionItemPolicyViolations=0`.
- Invalid/unloaded/fallback/placeholder Writes bleiben `0`.
- Die nicht gematchten Itemball-Scriptmuster werden nicht erweitert oder geschrieben: `scriptPatternExpansion=0`.
- Ban-Bad-Items bleibt inaktiv; `badFieldItemWrites=0` ist fuer diesen Block kein Ban-Bad-Nachweis.

## Field-Items-Statusentscheidung

- `FVX-ITEM-001` bleibt `GUI-kompatibel` fuer den engen Shuffle-Scope aus Diagnose 102.
- `FVX-ITEM-002` bleibt `Write modelliert` und ist durch diesen Smoke blockiert.
- `FVX-ITEM-003` bleibt `Write modelliert`.
- `FVX-ITEM-004` bleibt `Write modelliert`.

Keine Hochstufung fuer `FVX-ITEM-002`, weil Save/Output/Reload nicht erfolgreich waren.

## Risiken / Annahmen

- Die Bewertung gilt fuer den explizit freigegebenen lokalen CFRU/DPE Gen9-BPRE-Kandidaten und den engen Random-Carrier mit `banBadRandomFieldItems=false`.
- Der konkrete Fehler wird nur als Exception-Klasse dokumentiert; private Artefakte, Raw-Offets und Logauszuege werden nicht uebernommen.
- Ein spaeterer Fix muss Field-Items-Random-TM-Pool und Required-TM-Policy behandeln, ohne Shops, Pickup, Held Items oder TM/HM/Tutor/Learnset-Writer auszuweiten.

## Naechster minimaler Schritt

`analysis/upr-fvx-cfru-dpe-field-items-random-tm-pool-blocker-plan`

Ziel:

- Read-only planen, warum `FVX-ITEM-002 Field Items Random` im TM-Field-Items-Pool mit `RandomizationException` blockiert.
- Pruefen, ob der Fix eng im Field-Items-Random-TM-Pool-Scope bleiben kann.
- Keine Shops, kein Pickup, keine Held Items und keine TM/HM/Tutor/Learnset-Ausweitung.
