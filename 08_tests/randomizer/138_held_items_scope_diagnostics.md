# Diagnose 138 - Held Items Scope Diagnostics

Datum: 2026-05-15
Branch: `test/upr-fvx-cfru-dpe-held-items-scope-diagnostics`
Scope: Read-only CFRU/DPE Gen9-BPRE Held Items candidate diagnostic

## Ziel

Dieser Block fuehrt eine read-only Kandidatendiagnose fuer Held Items aus.

Diagnostizierte Subscopes:

- Wild/Encounter Held Items ueber Species/BaseStats-Held-Item-Felder.
- Trainer Held Items ueber `TrainerPokemon.heldItem`.
- Starter Held Items ueber `getStarterHeldItems()`.

Ausdruecklich ausserhalb des Scopes:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Build
- kein Randomizer-Lauf
- kein Write oder Save
- kein Output-ROM
- keine Field Items
- kein Pickup
- keine Shops
- keine Trainer-/Wild-Randomization ausser read-only Held-Item-Strukturerfassung
- keine Starter-Randomization ausser read-only Starter-Held-Item-Strukturerfassung
- keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes, Scriptdaten, Secrets, Tokens oder `.env`-Inhalte dokumentieren
- keine Original-Upstreams kontaktieren

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/137_held_items_scope_diagnostics_plan.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `08_tests/randomizer/README.md`
- `01_docs/references/tool-manifest.md`

## Diagnosemethode

- Verwendet wurde ein temporaerer read-only Harness ausserhalb des Repositories.
- Der Harness oeffnete lokale Kandidaten nur zum Lesen ueber vorhandene UPR-FVX-/ROMIO-JARs.
- Es wurde kein Projekt-Build ausgefuehrt.
- Es wurde kein Randomizer-Lauf, Write, Save, Output-ROM oder Log erzeugt.
- Die Ausgabe wurde vor Dokumentation sanitisiert; private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes und Scriptdaten werden nicht wiedergegeben.

Zaehldefinition:

- `wildHeldItemsTotal` zaehlt gelesene Species-/Forme-Held-Item-Slots: Guaranteed, Common, Rare und Dark-Grass Slots.
- `wildHeldItemsNonZero` zaehlt nicht-leere Wild-Held-Item-Slots.
- `trainerHeldItemsTotal` zaehlt gelesene TrainerPokemon-Held-Item-Slots.
- `trainerHeldItemsNonZero` zaehlt nicht-leere TrainerPokemon-Held-Item-Slots.
- `starterHeldItemsTotal` zaehlt gelesene Starter-Held-Item-Slots.
- Bad-/TM-/Fallback-/Placeholder-Zaehler beziehen sich auf nicht-leere Held-Item-Werte.

## Diagnose-Ergebnis

PASS fuer read-only Strukturdiagnose.

```text
candidateFilesChecked=3
candidateLoaded=true
heldItemScanSuccessful=true
wildHeldItemsReadable=true
wildHeldItemsTotal=5656
wildHeldItemsNonZero=526
wildHeldItemsBad=174
wildHeldItemsTM=0
trainerHeldItemsReadable=true
trainerHeldItemsTotal=1754
trainerHeldItemsNonZero=87
trainerHeldItemsBad=0
trainerHeldItemsTM=0
bossTrainerHeldItemsTotal=74
importantTrainerHeldItemsTotal=117
regularTrainerHeldItemsTotal=1563
trainerShouldNotGetBuffsSlots=3
starterHeldItemsReadable=true
starterHeldItemsTotal=1
starterHeldItemsNonZero=0
starterHeldItemsBad=0
starterHeldItemsTM=0
invalidHeldItemIds=0
unloadedHeldItemIds=0
fallbackHeldItems=109
placeholderHeldItems=130
heldItemPoolAllowedSize=212
heldItemPoolNonBadSize=161
canTMsBeHeld=true
fieldItemScopeChanged=false
pickupScopeChanged=false
shopScopeChanged=false
exceptionClass=none
stacktrace=none
```

## Wild/Encounter-Held-Items-Befund

- Wild/Encounter Held Items sind lesbar: `wildHeldItemsReadable=true`.
- Die Diagnose nutzt Species-/BaseStats-Held-Item-Felder und verwechselt sie nicht mit Encounter-Slots.
- `wildHeldItemsTotal=5656` gelesene Wild-Held-Item-Slots.
- `wildHeldItemsNonZero=526` nicht-leere Wild-Held-Item-Slots.
- `wildHeldItemsBad=174` vorhandene Bad Items im Wild-Held-Item-Bestand.
- `wildHeldItemsTM=0`.

Bewertung:

- Die Wild/Encounter-Held-Item-Struktur ist read-only sichtbar.
- Der Bestand enthaelt Bad Items; das ist kein Diagnosefehler, aber der Ban-Bad-Pfad muss separat nach einem Basis-Smoke getestet werden.
- Der naechste Smoke sollte zunaechst Wild/Encounter Held Items ohne Ban Bad testen, damit Writer-/Reload-Stabilitaet von der Poolfilter-Wirkung getrennt bleibt.

## Trainer-Held-Items-Befund

- Trainer Held Items sind lesbar: `trainerHeldItemsReadable=true`.
- `trainerHeldItemsTotal=1754` gelesene TrainerPokemon-Held-Item-Slots.
- `trainerHeldItemsNonZero=87` nicht-leere TrainerPokemon-Held-Item-Slots.
- `trainerHeldItemsBad=0`.
- `trainerHeldItemsTM=0`.
- `bossTrainerHeldItemsTotal=74` TrainerPokemon-Slots in Boss-Trainer-Scope.
- `importantTrainerHeldItemsTotal=117` TrainerPokemon-Slots in Important-Trainer-Scope.
- `regularTrainerHeldItemsTotal=1563` TrainerPokemon-Slots in Regular-Trainer-Scope.
- `trainerShouldNotGetBuffsSlots=3` preserve-only relevante TrainerPokemon-Slots.

Bewertung:

- Trainer-Held-Items und Boss/Important/Regular-Klassifikation sind read-only sichtbar.
- Die Struktur ist fuer spaetere Smokes ausreichend klassifizierbar.
- Der erste Trainer-Held-Items-Smoke sollte trotzdem separat und eng bleiben, empfohlen Boss Trainers only ohne Consumable/Sensible/Highest-Level-Filter.

## Starter-Held-Items-Befund

- Starter Held Items sind lesbar: `starterHeldItemsReadable=true`.
- `starterHeldItemsTotal=1`.
- `starterHeldItemsNonZero=0`.
- `starterHeldItemsBad=0`.
- `starterHeldItemsTM=0`.

Bewertung:

- Der eigene Starter-Held-Item-Pfad ist read-only diagnostizierbar.
- Fuer Gen3/FRLG ist ein einzelner gemeinsamer Starter-Held-Item-Slot erwartbar.
- Starter-Held-Items muessen nicht den Wild/Trainer-Folgeblock blockieren; sie bleiben ein eigener spaeterer Subscope.

## Pool-/Item-Safety-Befund

- `heldItemPoolAllowedSize=212`.
- `heldItemPoolNonBadSize=161`.
- `canTMsBeHeld=true`.
- `invalidHeldItemIds=0`.
- `unloadedHeldItemIds=0`.
- `fallbackHeldItems=109`.
- `placeholderHeldItems=130`.

Bewertung:

- Es wurden keine invaliden oder ungeladenen Held-Item-IDs im read-only Bestand festgestellt.
- Fallback-/Placeholder-Held-Items sind im Bestand sichtbar und muessen spaeter als Safety-Risiko gemessen werden.
- `canTMsBeHeld=true` bedeutet, dass spaetere Held-Item-Smokes TM-Zahlen explizit messen muessen; im aktuellen Bestand wurden keine TM-Held-Items gezaehlt.

## Scope-Safety-Befund

- `fieldItemScopeChanged=false`.
- `pickupScopeChanged=false`.
- `shopScopeChanged=false`.
- Keine Field Items, Pickup-Tabellen oder Shops wurden veraendert.
- Es gab keinen Randomizer-Lauf und keinen Write.

## Risiken / Blocker

Kein Blocker fuer den naechsten Wild/Encounter Held Items Smoke ohne Ban Bad.

Weiterhin relevant:

- Fallback-/Placeholder-Held-Items existieren im Bestand und duerfen nicht unbemerkt geschrieben werden.
- Wild/Encounter-Held-Items schreiben Species/BaseStats-Felder; Reload-Vergleich muss per Species-/Forme-Identitaet laufen.
- Trainer-Held-Items besitzen eigene Teamflag-/TrainerPokemon-Struktur und duerfen nicht mit Wild/Encounter kombiniert werden.
- Starter-Held-Items sind lesbar, aber bleiben ein separater Subscope.
- Ban Bad fuer Wild/Starter bleibt separat, weil `heldItemPoolAllowedSize=212` und `heldItemPoolNonBadSize=161` einen Poolunterschied zeigen.
- Field/Pickup/Shop-Scope muss in jedem spaeteren Smoke unveraendert bleiben.

## Feature-Status

- Held Items Scope: read-only Kandidatenstruktur diagnostiziert.
- Keine Held-Item-Feature-Hochstufung in diesem Block.
- Shop Items Scope bleibt abgeschlossen im getesteten CFRU/DPE Gen9-BPRE Scope.
- Field Items, Pickup und Shops bleiben unveraendert.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-wild-encounter-held-items-reload-smoke`: Wild/Encounter Held Items Smoke ohne Ban Bad, nur wenn dieselbe Kandidaten-/Artefakt-Safety eingehalten wird.
