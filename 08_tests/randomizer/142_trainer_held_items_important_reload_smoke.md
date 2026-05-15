# Diagnose 142 - Important Trainer Held Items Reload Smoke

Datum: 2026-05-15
Branch: `test/upr-fvx-cfru-dpe-trainer-held-items-important-reload-smoke`
Scope: CFRU/DPE Gen9-BPRE Important Trainer Held Items Write/Reload-Smoke

## Ziel

Dieser Block testet ausschliesslich Trainer Held Items im engen Important-Trainers-only Scope.

Getesteter Scope:

- `randomizeHeldItemsForBossTrainerPokemon=false`
- `randomizeHeldItemsForImportantTrainerPokemon=true`
- `randomizeHeldItemsForRegularTrainerPokemon=false`
- `consumableItemsOnlyForTrainers=false`
- `sensibleItemsOnlyForTrainers=false`
- `highestLevelGetsItemsForTrainers=false`
- keine Wild/Encounter Held Items
- keine Starter Held Items
- keine Field Items
- kein Pickup
- keine Shops

Ausdruecklich ausserhalb des Scopes:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Projekt-Build
- keine Boss Trainer Held Items
- keine Regular Trainer Held Items
- keine Wild/Encounter Held Items
- keine Starter Held Items
- keine Field Items
- kein Pickup
- keine Shops
- keine Evolution-, Learnset-, TM/HM/Tutor-, Move-, Ability-, TypeChart-, Palette-, Graphics- oder Text/Menu-Arbeit
- keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs oder Tool-Binaries committen
- keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes, Scriptdaten, Secrets, Tokens oder `.env`-Inhalte dokumentieren
- keine Original-Upstreams kontaktieren

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/137_held_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/138_held_items_scope_diagnostics.md`
- `08_tests/randomizer/141_trainer_held_items_boss_reload_smoke.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `08_tests/randomizer/README.md`
- `01_docs/references/tool-manifest.md`

## Smoke-Methode

- Verwendet wurde ein temporaerer Harness ausserhalb des Repositories.
- Die lokal freigegebene CFRU/DPE Gen9-BPRE-Kandidatenquelle wurde fuer diesen Block verwendet.
- Der Harness setzte nur den Important-Trainer-Held-Items-Pfad.
- Lokale Output-ROM- und Log-Artefakte blieben ausserhalb der Dokumentation und wurden nicht committed.
- Die Dokumentation enthaelt nur aggregierte, sanitizte Metriken.
- Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes und Scriptdaten werden nicht wiedergegeben.

Vergleichsmodell:

- Trainer Held Items wurden ueber `TrainerPokemon.heldItem` verglichen, nicht ueber Species/BaseStats.
- Important Trainer wurden als Write-Scope gemessen.
- Boss Trainer, Regular Trainer und `shouldNotGetBuffs`-Trainer wurden preserve-only gemessen.
- Wild/Encounter und Starter Held Items wurden als Fremdscopes per Fingerprint abgesichert.
- Field Items, Pickup und Shops wurden als Fremdscopes unveraendert erwartet.

## Smoke-Ergebnis

PASS.

```text
candidateFilesChecked=3
candidateLoaded=true
smokeExecuted=true
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
reloadSuccessful=true
trainerHeldItemsTotalBefore=1754
trainerHeldItemsTotalAfter=1754
trainerHeldItemsTotalReload=1754
trainerHeldItemsNonZeroBefore=87
trainerHeldItemsNonZeroAfter=195
trainerHeldItemsNonZeroReload=195
trainerHeldItemsBadBefore=0
trainerHeldItemsBadAfter=25
trainerHeldItemsBadReload=25
trainerHeldItemsTMBefore=0
trainerHeldItemsTMAfter=0
trainerHeldItemsTMReload=0
bossTrainerHeldItemsTotalBefore=74
bossTrainerHeldItemsTotalAfter=74
bossTrainerHeldItemsTotalReload=74
importantTrainerHeldItemsTotalBefore=117
importantTrainerHeldItemsTotalAfter=117
importantTrainerHeldItemsTotalReload=117
regularTrainerHeldItemsTotalBefore=1563
regularTrainerHeldItemsTotalAfter=1563
regularTrainerHeldItemsTotalReload=1563
importantTrainerHeldItemReloadMismatches=0
bossTrainerHeldItemMismatchesAfter=0
bossTrainerHeldItemMismatchesReload=0
regularTrainerHeldItemMismatchesAfter=0
regularTrainerHeldItemMismatchesReload=0
shouldNotGetBuffsTrainerHeldItemMismatchesAfter=0
shouldNotGetBuffsTrainerHeldItemMismatchesReload=0
invalidTrainerHeldItemWrites=0
unloadedTrainerHeldItemWrites=0
fallbackTrainerHeldItemWrites=0
placeholderTrainerHeldItemWrites=0
heldItemPoolAllowedSize=212
heldItemPoolNonBadSize=161
canTMsBeHeld=true
wildHeldItemScopeChanged=false
starterHeldItemScopeChanged=false
fieldItemScopeChanged=false
pickupScopeChanged=false
shopScopeChanged=false
exceptionClass=none
stacktrace=none
```

Bewertung:

- Save, Log, Output und Reload waren erfolgreich.
- Important-Trainer-Held-Items reloaden stabil: `importantTrainerHeldItemReloadMismatches=0`.
- Boss Trainer, Regular Trainer und `shouldNotGetBuffs`-Trainer blieben unveraendert.
- Es entstanden keine invaliden, ungeladenen, Fallback- oder Placeholder-Writes.
- Wild Held Items, Starter Held Items, Field Items, Pickup und Shops blieben unveraendert.
- Trainer Held Items sind nur fuer Important Trainers im getesteten Scope GUI-kompatibel.

## Trainer-Held-Items-Befund

Baseline:

- Diagnose 138: `trainerHeldItemsTotal=1754`, `bossTrainerHeldItemsTotal=74`, `importantTrainerHeldItemsTotal=117`, `regularTrainerHeldItemsTotal=1563`.
- Diagnose 141: Boss Trainer Held Items ohne Zusatzfilter reloadstabil.

Smoke-Befund:

- TrainerPokemon-Held-Item-Slots blieben stabil: `1754/1754/1754`.
- Nicht-leere Trainer-Held-Items stiegen erwartungsgemaess durch Important-Trainer-Writes: `87/195/195`.
- Bad Items im Trainer-Held-Item-Bestand stiegen auf `0/25/25`, weil fuer Trainer in diesem Scope kein Ban-Bad-Filter aktiv ist.
- TM-Held-Items blieben bei `0/0/0`.
- Important-Trainer-Scope umfasst `117/117/117` TrainerPokemon-Slots.

## Preserve-/Trainerklasse-Befund

- Boss-Trainer-Slots blieben stabil: `74/74/74`.
- Regular-Trainer-Slots blieben stabil: `1563/1563/1563`.
- `bossTrainerHeldItemMismatchesAfter=0`.
- `bossTrainerHeldItemMismatchesReload=0`.
- `regularTrainerHeldItemMismatchesAfter=0`.
- `regularTrainerHeldItemMismatchesReload=0`.
- `shouldNotGetBuffsTrainerHeldItemMismatchesAfter=0`.
- `shouldNotGetBuffsTrainerHeldItemMismatchesReload=0`.

Bewertung:

- Important Trainers only wurde eingehalten.
- Boss und Regular Trainer wurden nicht veraendert.
- `shouldNotGetBuffs`-Trainer blieben preserve-only.

## Reload-Befund

- `reloadSuccessful=true`.
- `importantTrainerHeldItemReloadMismatches=0`.
- `invalidTrainerHeldItemWrites=0`.
- `unloadedTrainerHeldItemWrites=0`.
- `fallbackTrainerHeldItemWrites=0`.
- `placeholderTrainerHeldItemWrites=0`.

Bewertung:

- Die geschriebenen Important-Trainer-Held-Items reloaden stabil.
- Teamflags und TrainerPokemon-Strukturbreiten blieben fuer den dokumentierten Scope konsistent genug, um alle TrainerPokemon-Held-Item-Slots reloadstabil wiederzufinden.

## Scope-Isolation-Befund

- `wildHeldItemScopeChanged=false`.
- `starterHeldItemScopeChanged=false`.
- `fieldItemScopeChanged=false`.
- `pickupScopeChanged=false`.
- `shopScopeChanged=false`.

Bewertung:

- Keine Wild/Encounter-Held-Items wurden veraendert.
- Keine Starter-Held-Items wurden veraendert.
- Field Items, Pickup und Shops blieben ausserhalb des Scopes.

## Risiken / Blocker

Kein Blocker fuer den naechsten Regular Trainer Held Items Smoke.

Weiterhin relevant:

- Regular Trainer Held Items bleiben getrennt und werden durch Diagnose 142 nicht hochgestuft.
- Trainer-Bad-Items sind in diesem Scope erlaubt; ein separater Trainer-Poolfilter-Block waere noetig, falls ein Filter existiert oder gewuenscht ist.
- Consumable-, Sensible- und Highest-Level-Filter bleiben ungetestet.
- Starter Held Items bleiben ein eigener spaeterer Subscope.

## Feature-Status

- Wild/Encounter Held Items ohne Ban Bad: GUI-kompatibel im getesteten Scope durch Diagnose 139.
- Wild/Encounter Held Items + Ban Bad: GUI-kompatibel im getesteten Scope durch Diagnose 140.
- Trainer Held Items Boss Trainers only: GUI-kompatibel im getesteten Scope durch Diagnose 141.
- Trainer Held Items Important Trainers only: GUI-kompatibel im getesteten Scope durch Diagnose 142.
- Trainer Held Items Regular: offen.
- Starter Held Items: offen.
- Field Items, Pickup und Shops bleiben unveraendert.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-trainer-held-items-regular-reload-smoke`: Regular Trainer Held Items Smoke, nur wenn Important-Trainer-Held-Items-Reloadstabilitaet aus Diagnose 142 akzeptiert ist.
