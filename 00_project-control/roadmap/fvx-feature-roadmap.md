# FVX Feature Roadmap Update - 2026-05-15 - Pickup Ban Bad next

- Pickup Random without Ban Bad is reload-stable after UPR-FVX PR #38 and Diagnose 118.
- Pickup Ban Bad is the next narrow Item sub-scope; it should be tested directly before Shops or Held Items.
- Recommended branch: `test/upr-fvx-cfru-dpe-pickup-items-random-ban-bad-reload-smoke`.
- Preserve separation from Field Items, Shops, Encounter Held Items, Trainer Held Items and Starter Held Items.

# Roadmap Note - 2026-05-15 - Pickup reload locator fix

- Diagnose 118 closes the Pickup Random reload-locator blocker for `banBadRandomPickupItems=false`.
- UPR-FVX PR #38 keeps the fix scoped to Pickup table localization and leaves pool policy unchanged.
- Next Pickup sub-scope is Ban Bad planning/smoke; Shops and Held Items remain separate.

# Roadmap Note - 2026-05-15 - Pickup reload locator blocker

- Diagnose 117 keeps Pickup as the active separated Item-writer track after Field Items.
- Next recommended implementation branch is `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- The intended fix stays below Pickup pool policy: make the Pickup table locator reload-stable after `PickupItemsMod.RANDOM` changes item IDs.
- Pickup Ban Bad, Shops and Held Items remain blocked/separate until Pickup Random without Ban Bad reloads stably.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random Ban Bad reload smoke

- Diagnose 112 confirms the Field-Items Random Ban-Bad carrier: `FVX-ITEM-002` with `banBadRandomFieldItems=true` has a successful CFRU/DPE Field-Items-only reload smoke.
- `FVX-ITEM-004` can be treated as tested for `FieldItemsMod.RANDOM`, but not fully GUI-compatible until Random Even + Ban Bad passes separately.
- Keep Shops, Pickup and Held Items separate from Field Items Ban Bad.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Ban Bad scope plan

- Diagnose 111 plans `FVX-ITEM-004 Field Items Ban Bad Items` as a Field-Items Non-TM pool-filter validation.
- First smoke should use `FVX-ITEM-002 Field Items Random` with `banBadRandomFieldItems=true`; Random Even + Ban Bad should follow separately.
- Keep Shops, Pickup and Held Items separate from Field Items Ban Bad.
- Next step is `test/upr-fvx-cfru-dpe-field-items-random-ban-bad-reload-smoke`.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random Even reload smoke

- Diagnose 110 confirms `FVX-ITEM-003 Field Items Random even distribution` with a successful CFRU/DPE Field-Items-only reload smoke.
- `FVX-ITEM-003` can move to `GUI-kompatibel` only for the narrow Field-Items Random-Even scope with `banBadRandomFieldItems=false`.
- Keep `FVX-ITEM-004` Ban Bad Items as a separate follow-up block.
- Next step is `analysis/upr-fvx-cfru-dpe-field-items-ban-bad-scope-plan`; do not fold Shops or Pickup into that work.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items API TM-slot reload smoke

- Diagnose 109 confirms the UPR-FVX PR #37 Field-Items API TM-slot fix with a successful `FVX-ITEM-002 Field Items Random` reload smoke.
- `FVX-ITEM-002` can move to `GUI-kompatibel` only for the narrow Field-Items Random scope with `banBadRandomFieldItems=false`.
- Keep `FVX-ITEM-003` Random Even and `FVX-ITEM-004` Ban Bad Items as separate follow-up blocks.
- Next step is `test/upr-fvx-cfru-dpe-field-items-random-even-reload-smoke`; do not fold Shops or Pickup into that work.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items API TM-slot fix prepared

- UPR-FVX PR #37 prepares the narrow `FVX-ITEM-002` API TM-slot scope fix.
- The fix stays in Gen3RomHandler Field-Items get/set and exposes CFRU/DPE Field-TM slots without making TMs globally allowed.
- Next step is a separate sanitized reload smoke before any `FVX-ITEM-002` GUI-compatible upgrade.
- Keep `FVX-ITEM-003` Random Even and `FVX-ITEM-004` Ban Bad Items separate.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items API TM-slot scope plan

- Diagnose 107 explains the post-PR-36 `FVX-ITEM-002` blocker: raw diagnostics find `28` TM Field-Item slots, but `getFieldItems()` exposes none because the API filters on `Item::isAllowed`.
- Next fix should stay in the CFRU/DPE Field-Items API TM-slot scope and must not make TMs globally allowed.
- Keep `FVX-ITEM-002` below GUI-compatible until a narrow API-scope fix and reload smoke pass.
- Keep `FVX-ITEM-003` Random Even and `FVX-ITEM-004` Ban Bad Items separate.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random API TM-slot blocker

- Diagnose 106 shows UPR-FVX PR #36 removes the original Unique-TM-Filler pool deficit for `FVX-ITEM-002`.
- The remaining blocker is an API TM-slot scope mismatch: raw Field-Item diagnostics found `tmFieldItemSlots=28`, but `ItemRandomizer.randomizeTMFieldItems(...)` receives `0` TM slots through `getFieldItems()`.
- Keep `FVX-ITEM-002` below GUI-compatible until the API TM-slot scope is understood and a later smoke passes.
- Do not proceed to `FVX-ITEM-003` or `FVX-ITEM-004` before `FVX-ITEM-002` reloads successfully.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random TM-pool fix prepared

- UPR-FVX PR #36 prepares the narrow `FVX-ITEM-002 Field Items Random` TM-pool fix.
- The fix is limited to the TM Field Items randomization pool and does not expand Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even or Ban Bad Items.
- `FVX-ITEM-002` should only be upgraded after a separate sanitized reload smoke confirms `randomTmPoolDeficit=0`, `fieldItemReloadMismatches=0`, and `requiredFieldTMMissingAfter=0`.
- Do not proceed to `FVX-ITEM-003` or `FVX-ITEM-004` before this `FVX-ITEM-002` reload smoke passes.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random TM-pool blocker planned

- Diagnose 104 narrows `FVX-ITEM-002 Field Items Random` to a TM-pool / Required-TM algorithm blocker.
- Next fix should stay inside Field Items Random TM-pool handling and avoid Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even and Ban Bad Items.
- Do not proceed to `FVX-ITEM-003` or `FVX-ITEM-004` until `FVX-ITEM-002` has a successful reload smoke.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Random blocked

- Field Items Random has a blocked smoke in Diagnose 103: candidate loaded, but save fails with `RandomizationException` before output/reload.
- Keep `FVX-ITEM-002` as `Write modelliert` until the Random TM-pool blocker is planned and fixed.
- Do not proceed to Random Even or Ban Bad Items until the Random carrier is stable.
- Do not fold Shops or Pickup into the Field Items Random blocker work.

# FVX Feature Roadmap Update - 2026-05-15 - Field Items Shuffle complete

- Field Items Shuffle has a successful allowed-slot Write-/Reload-Smoke in Diagnose 102.
- `FVX-ITEM-001` can be treated as `GUI-kompatibel` for the narrow Shuffle scope.
- Continue Field Items in separate slices: Random first, Random Even second, Ban Bad Items third.
- Do not fold Shops or Pickup into the Field Items Random follow-up.

# FVX Feature Roadmap Update - 2026-05-14 - Field Items allowed-slot guard

- Field Items remain the first active Item-writer track after Palette.
- Diagnose 101 records that the existing Gen3 Field-Items writer already guards writes to allowed slots.
- No UPR-FVX code change is planned until a Write-/Reload-Smoke proves a concrete mismatch.
- Next minimal validation block: `test/upr-fvx-cfru-dpe-field-items-allowed-slot-reload-smoke` for `FVX-ITEM-001 Field Items Shuffle` only.
- Shops and Pickup stay separate and must not be folded into the first Field-Items smoke.

# FVX Feature Roadmap

Diese Datei ist die feature-orientierte Roadmap fuer Universal Pokemon Randomizer FVX. Sie verdichtet `01_docs/randomizer/fvx-feature-coverage.md` auf planbare Arbeitspakete.

Die detaillierte Status- und Feature-ID-Matrix bleibt in:

```text
01_docs/randomizer/fvx-feature-coverage.md
```

## Gesamtstand aus Feature-Matrix

| Status | Anzahl |
|---|---:|
| Nicht begonnen | 39 |
| Plan erstellt | 28 |
| Read modelliert | 0 |
| Write modelliert | 15 |
| Getestet | 10 |
| GUI-kompatibel | 38 |
| In Arbeit | 0 |
| **Gesamt** | **130** |

## Feature-Pakete

| Paket | Feature-Zeilen | Leitstatus | Ziel |
|---|---:|---|---|
| General Options | 4 | Gemischt | `FVX-GEN-001/002` sind im Starter-Carrier-Smoke getestet; Race Mode und Intro-Mon separat pruefen |
| Pokemon Traits | 28 | Gemischt | Base Stats, Types, Abilities, Evolutions, EXP Curves und Suboptionen systematisch absichern; Evolution Similar Strength und Same Typing sind im engen `FVX-TRAIT-016`-Scope stabil, weitere Evolution-Suboptionen getrennt halten |
| Starters, Statics & Trades | 15 | Gemischt | Starter-Filter sind im Starter-Species-Writer-Smoke getestet; Starter-Held-Items, Trades und Level-Subpfade ergaenzen |
| Moves & Movesets | 11 | Gemischt | Learnset-/Moveset-GUI halten; MoveData `Update Moves`, Power/Accuracy/PP und Move Types sind stabil; Move Names ist als Name-only Smoke planbar, aber Diagnosen 089/090 sind mangels lokalem 992-Move-Kandidaten mit `991:PsychicNoise` blockiert; Move Descriptions / Text/Menu-Repointing bleibt getrennt |
| Foe Pokemon | 14 | Gemischt | Trainer-Species/-Movesets/-Held-Items halten; Trainer Similar Strength und `FVX-FOE-009` sind im `FVX-FOE-001` Carrier stabil |
| Wild Pokemon | 12 | Gemischt | Standard/Fallback-Wild halten; Similar Strength und Type Restrictions sind nach Diagnose 075 im `FVX-WILD-001` Carrier wieder stabil |
| TM/HMs & Tutors | 15 | Gemischt | TM/Tutor-Tabellen halten; Preserve-/Filter-/Follow-Evolution-Suboptionen testen |
| Items | 10 | Write modelliert | Field Items, Shops und Pickup als getrennte Writer implementieren/testen |
| Types | 3 | Getestet | TypeEffectiveness Random, Balanced, Keep Type Identities, Inverse, Add Immunities und Update Type Effectiveness sind einzeln im TypeChart-Scope getestet |
| Graphics | 6 | Gemischt | Diagnose 095 implementiert den Normal-Palette-Single-owner-Guard; Reload-Smoke steht noch aus, Shiny/shared/invalid/missing/decode-failed bleiben preserve-only, Custom Player Graphics separat modellieren |
| Misc Tweaks | 12 | Nicht begonnen | jeden Misc-Tweak als eigenen Patch-/Risk-Scope inventarisieren |
| GUI-Suboptions-Regressionsmatrix | n/a | Erledigt | vorhandene Diagnose 060 als technische Regressionssicht nutzen |
| Regression-Smoke-Plan | n/a | In Arbeit | konkrete Smoke-/Regression-Laeufe aus Feature-IDs ableiten und sanitisiert dokumentieren |

## Priorisierte Roadmap ab jetzt

### P0 - Coverage und Smoke-Plan

| Reihenfolge | Branch | Ziel | Status |
|---|---|---|---|
| P0.1 | `docs/fvx-feature-coverage-matrix` | FVX-GUI-Features als Requirements-/Coverage-Matrix dokumentieren | In Arbeit |
| P0.2 | `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan` | Smoke-/Regression-Plan fuer priorisierte GUI-Suboptionen erstellen, ohne neue Randomizer-Laeufe im Planblock | Erledigt |
| P0.3 | `test/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke` | Global-Species-Pool-Smoke fuer `FVX-GEN-001/002` im Starter-Carrier-Scope sanitisiert dokumentieren | Erledigt |
| P0.4 | `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke` | Starter-Suboptions-Smoke fuer `FVX-SST-003/004/005/006/009` sanitisiert dokumentieren | Erledigt |
| P0.5 | `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke` | Similar-Strength-/Same-Type-/Type-Restrictions-Smoke sanitisiert dokumentieren | Review/Test |

### P1 - Offene Writer mit vorhandenen Modellen

| Reihenfolge | Branch | Paket | Ziel |
|---|---|---|---|
| P1.1 | `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness` + `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes` | Types | erledigt: TypeEffectiveness Random, Balanced, Keep Type Identities, Inverse, Add Immunities und Update Type Effectiveness mit Reload-/Terminator-/Preserve-Kriterien abgesichert |
| P1.2 | `compat/upr-fvx-cfru-dpe-move-data-write-preserve` + `test/upr-fvx-cfru-dpe-move-data-write-preserve-reload-smoke` | Moves & Movesets | erledigt: UPR-FVX PR #33, Workspace PR #124 und Workspace PR #125 sind gemerged; Diagnose 084 bestaetigt `Update Moves` mit `writeReloadMoveDataMismatches=0`, stabilem category/split-Reload und bytegleich erhaltenen Preserve-Bytes |
| P1.2a | `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke` | Moves & Movesets | erledigt: Diagnose 085 bestaetigt `FVX-MOVE-001/002/003` mit `writeReloadMoveDataMismatches=0`, stabilen `+1/+3/+4` Bytes und bytegleich erhaltenen Preserve-Bytes |
| P1.2b | `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke` | Moves & Movesets | blockiert: Diagnose 086 zeigt Save/Log/Output/Reload true und Preserve-Bytes stabil, aber `writeReloadMoveDataMismatches=54` durch Fairy-Type-Byte-Mismatches im MoveData-`+2 type`-Writer |
| P1.2c | `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte` | Moves & Movesets | erledigt und gemerged: UPR-FVX PR #34, Workspace PR #129 und Diagnose 087 bestaetigen `FVX-MOVE-004` mit `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0` und bytegleich erhaltenen Preserve-Bytes |
| P1.2d | `analysis/upr-fvx-cfru-dpe-move-names-text-menu-scope-plan` | Moves & Movesets | erledigt: Diagnose 088 klassifiziert `FVX-MOVE-005` als getrennten Text/Menu-Scope; Name-only fixed-length Smoke ist realistisch, Move Descriptions / Text/Menu-Repointing bleibt zurueckgestellt |
| P1.2e | `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke` | Moves & Movesets | blockiert: Diagnose 089 fand keinen freigegebenen lokalen CFRU/DPE Gen9-BPRE-Kandidaten mit `moves.total=992` und `991:PsychicNoise`; `FVX-MOVE-005` bleibt `Write modelliert` |
| P1.2f | `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke-retry` | Moves & Movesets | abgeschlossen/blockiert: Workspace PR #133 ist gemerged; Diagnose 090 wiederholte den Candidate-Preflight sanitisiert, `candidateFilesChecked=94`, `candidatePreflightSuccessful=false`; kein fachlicher Name-only Smoke, keine Feature-Hochstufung |
| P1.3 | `analysis/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint-plan` | Graphics | erledigt: Diagnose 091 trennt Safety von echter Palette-Randomization und empfiehlt vor Fix eine read-only Pointer-/Compression-Diagnose |
| P1.3a | `analysis/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics-plan` | Graphics | erledigt: Diagnose 092 plant Normal-/Shiny-Palette-Pointer read-only nach dekomprimierbar, single-owner, shared, missing und invalid zu klassifizieren |
| P1.3b | `test/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics` | Graphics | erledigt: Diagnose 093 klassifiziert Pointer/Compression; `candidateWritablePalettes=385`, davon `385` Normal und `0` Shiny |
| P1.3c | `analysis/upr-fvx-cfru-dpe-palette-single-owner-normal-only-fix-scope-plan` | Graphics | erledigt: Diagnose 094 plant den spaeteren Scope nur fuer Normal-Paletten, single-owner, dekomprimierbar, gueltig, non-shared und non-cross-kind; Shiny/shared/invalid/missing/decode-failed preserve-only |
| P1.3d | `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write` | Graphics | Review/Test: UPR-FVX PR #35 implementiert den Normal-only-Single-owner-Guard; kein ROM-/Reload-Smoke in diesem Block |
| P1.3e | `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke` | Graphics | naechster Schritt: sanitisierten Reload-Smoke fuer `FVX-GFX-001` Normal-only-Single-owner-Subset ausfuehren |
| P1.3f | `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint` | Graphics | wartet: breitere Shared-/Shiny-/Repoint-Policy erst nach Normal-Single-owner-Smoke separat planen |
| P1.4 | `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write` | Items | Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern |

### P2 - Suboptionen der bereits GUI-kompatiblen Pakete

| Paket | Ziel |
|---|---|
| Pokemon Traits | Follow Evolutions, Force Dual Types, Ability-Ban-/Allow-Filter, EXP Curves testen; `FVX-TRAIT-018` aus 082 und `FVX-TRAIT-019` aus 080 halten, Evolution-Methoden weiter getrennt behandeln |
| Starters, Statics & Trades | Starter-Held-Items und In-Game-Trades absichern; Starter-Type-/Legendary-/BST-Filter ausserhalb des Starter-Species-Writer-Smokes nur separat hochstufen |
| Foe Pokemon | Additional Pokemon, League-Unique, Battle Style, Rival Carry, Trainer Names/Class Names absichern; Force Diverse Types / `FVX-FOE-009` aus 078 im `FVX-FOE-001` Carrier halten |
| Wild Pokemon | Evolution Restrictions, Catch Rate, Catch-em-all und Level-Balance absichern; Wild Similar Strength und Type Restrictions aus 075 im `FVX-WILD-001` Carrier halten |
| TM/HMs & Tutors | Keep Field Moves, No Game-Breaking, Good-Damaging-%, Follow-Evolutions und Full-HM-Kompatibilitaet absichern |

### P3 - Noch nicht begonnene Sonderbereiche

| Paket | Ziel |
|---|---|
| General Options | Limit Pokemon und No Premature Evolutions ausserhalb des Starter-Carrier-Smokes weiter pruefen; No Random Intro Mon und Race Mode separat inventarisieren |
| Misc Tweaks | alle 12 Misc Tweaks inventarisieren und pro Tweak Risiko/Writer bestimmen |
| Custom Player Graphics | getrennt von Pokemon-Palette-Randomization modellieren |
| In-Game Trades Text/Items/IVs | Spezies-, Text-, Item- und IV-Writer getrennt pruefen |

## Roadmap-Regel

- Neue Einzeltests referenzieren mindestens eine `FVX-*` Feature-ID aus der Matrix.
- Die Feature-Matrix ist fuer Vollstaendigkeit und Zaehlregel massgeblich.
- Diese Roadmap ist fuer Reihenfolge und Arbeitsbranch-Zuschnitt massgeblich.
- `roadmap-status.md` bleibt die allgemeine Projekt-Roadmap und sollte nur grobe Statuswechsel aufnehmen.
- Keine ROMs, Saves, Builds, Tool-Binaries, private Pfade oder Secrets in Roadmap-Dateien aufnehmen.

## 2026-05-14 - Palette Follow-up nach Diagnose 096

Diagnose 096 blockiert den `FVX-GFX-001` Normal-only Single-owner Reload-Smoke mangels UPR-FVX-ladbarem `candidateSpeciesTotal=1439` Kandidaten. Der nächste Palette-Schritt ist kein Scope-Ausbau, sondern ein Retry desselben engen Smoke-Scope nach expliziter Kandidatenfreigabe.

Nicht in den Retry aufnehmen: Shiny-Palette-Writes, Shared-Palette-Writes, Graphics/Sprites, TypeChart/TypeEffectiveness, Species-Type-Write, Evolution-Writer, Items, Trainer/Wild, Text/Menu, MoveData oder MoveNames.

## 2026-05-14 - P1-Reihenfolge nach blockiertem Palette-Smoke

Nach Diagnose 096 bleibt Palette konservativ: `FVX-GFX-001` hat einen Guard-Fix, aber keinen erfolgreichen Reload-Smoke; `FVX-GFX-001..004` bleiben `Write modelliert`. Ein Palette-Retry wird erst mit explizit freigegebenem UPR-FVX-ladbarem `candidateSpeciesTotal=1439` Kandidaten sinnvoll.

Der naechste empfohlene P1-Block ist deshalb kein Palette-Scope-Ausbau, sondern `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan` als read-only Planung fuer Field Items, Shops und Pickup.

## 2026-05-14 - Item-P1-Aufteilung nach Diagnose 097

Field Items, Shops und Pickup bleiben im Items-Paket, werden aber nicht als gemeinsamer Fixbranch empfohlen. Reihenfolge: Field Items zuerst, danach Pickup, Shops zuletzt wegen Terminator-/DataRewriter-/Repointing- und Preisrisiken. Gemeinsame Item-Pool-Bans bleiben Querschnitt, aber jeder Writer braucht eigene Reload-Kriterien.

## 2026-05-14 - Field Items diagnostics scope

- Field Items are split into their own first item-writer diagnostic branch: `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`.
- Follow-up should diagnose only Field Items before any fix: visible Itemballs, Hidden Items/Signposts, TM-vs-Non-TM slots, Required Field TMs, progression-sensitive items, bad items, modern item IDs and invalid/unloaded item IDs.
- Shops and Pickup stay separate; no shared fix block is recommended until each writer has its own sanitized diagnostics.

## 2026-05-14 - Field Items diagnostics candidate needed

- Field-Items-only diagnostics from protocol 099 are blocked until an explicitly approved local CFRU/DPE Gen9-BPRE candidate is available.
- No Field-Item fix should start before the aggregated diagnostics from 098 can report visible Itemballs, Hidden Items/Signposts, TM/Non-TM slots, Required Field TMs, bad items, modern item IDs and invalid/unloaded item IDs.
- Shops and Pickup remain separate follow-up tracks.

## 2026-05-14 - Field Items candidate diagnostics

- Field-Items-only diagnostics now have sanitized candidate data: `fieldItemsTotal=339`, visible `168`, hidden `171`, allowed `280`, disallowed `59`, TM slots `28`, Non-TM slots `311`, and `requiredFieldTMMissing=0`.
- The next reviewable scope is a guarded Field-Items write/smoke for allowed slots only; disallowed, progression-sensitive, key/system and script-pattern-unmatched slots stay preserve-only.
- Shops and Pickup remain separate follow-up tracks.

## 2026-05-15 - Field Items completion in tested scope

Diagnosen 102, 109, 110, 112 und 113 schliessen `FVX-ITEM-001..004` fuer Field Items im getesteten engen CFRU/DPE Gen9-BPRE-Scope ab:

- Shuffle, Random und Random Even reloaden stabil.
- Ban Bad ist fuer Random und Random Even bestaetigt.
- Field-Item-Gesamtzahl bleibt `339`, Reload-Mismatches bleiben `0`, Required Field TMs bleiben vollstaendig.
- CFRU/DPE Field-TM-Slots bleiben im API-Scope sichtbar, ohne TMs global allowed zu setzen.

Naechste Item-Reihenfolge:

1. Pickup Items separat read-only planen und diagnostizieren.
2. Shops separat planen, weil Terminatoren, Shoplisten-Laengen, Preise und Repointing ein eigener Scope sind.
3. Held Items bleiben getrennt von Field Items / Shops / Pickup.

## 2026-05-15 - Pickup Items diagnostics scope planned

Pickup folgt nach Field Items als separater Item-Writer-Scope:

- `FVX-ITEM-010` bleibt `Write modelliert`, bis eine Pickup-only Kandidatendiagnose und danach eigene Reload-Smokes vorliegen.
- Der Gen3-Pfad nutzt `PickupTableStartLocator`, `PickupItemCount`, `PickupItem.PROBABILITY_SLOTS=10` und schreibt nur Item-ID-Felder.
- CFRU/DPE-Risiken: falscher Locator, abweichende Common/Rare-Struktur, Probability-Semantik, moderne/fallback/bad Items und TM-Holdability-/Reusable-Policy.
- Reihenfolge: read-only Diagnose, Random ohne Ban Bad, Random mit Ban Bad.
- Shops bleiben wegen Terminator-/Repointing-/Preis-Scope separat.

## 2026-05-15 - Pickup Items candidate diagnostics completed

Pickup read-only diagnostics are complete for the next Item writer slice:

- `FVX-ITEM-010` remains `Write modelliert` until a dedicated Write-/Reload-Smoke passes.
- Diagnose 115 establishes `pickupLocatorSuccessful=true`, `pickupItemsTotal=16`, `pickupExpectedCount=16`, `pickupEntrySize=4`, `pickupProbabilitySlots=10` and `pickupProbabilityModelStable=true`.
- Invalid/unloaded/fallback/placeholder Pickup IDs were not found in the current table.
- Ban Bad remains a separate follow-up because `pickupBadItemPoolCandidates=51` and `pickupBadItemPoolExcluded=51` must be validated through the Pickup poolfilter.
- Reihenfolge: Pickup Random ohne Ban Bad, danach Pickup Random mit Ban Bad.

## 2026-05-15 - Pickup Items Random reload blocker

Pickup Random reached save/log/output but is not reload-stable:

- `FVX-ITEM-010` remains `Write modelliert`.
- Diagnose 116 shows `pickupItemsTotalBefore=16` and `pickupItemsTotalAfter=16`, but fresh reload reports `pickupLocatorSuccessful=false` and `pickupItemsTotalReload=0`.
- The likely narrow issue is the content-based `PickupTableStartLocator` no longer matching after item IDs are randomized.
- Next step: read-only locator-blocker plan before any codefix or Ban-Bad smoke.
