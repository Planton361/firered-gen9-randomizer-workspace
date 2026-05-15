# 2026-05-15 - Diagnose 127 Shop Items Ban Bad

- `FVX-ITEM-007` ist fuer `ShopItemsMod.RANDOM + banBadRandomShopItems=true` im Shop-only Write/Reload-Smoke GUI-kompatibel.
- `badShopItemWrites=0`; Reload, Skip-Shops, Preis- und Fremdscopes bleiben stabil.
- Regular-Ban und OP-Ban bleiben eigene ausstehende Subscopes; `FVX-ITEM-008` und `FVX-ITEM-009` bleiben nicht hochgestuft.

# Roadmap Status Update - 2026-05-15 - Shop Item Bans scope plan

- Neuer Plan: `08_tests/randomizer/126_shop_item_bans_scope_plan.md`.
- `FVX-ITEM-007 Shop Item Bans` ist als separater Shop-only Subscope nach `FVX-ITEM-006` geplant.
- Codepfad-Befund: `banBadRandomShopItems`, `banRegularShopItems` und `banOPShopItems` wirken nur in `ItemRandomizer.randomizeShopItems()` unter `ShopItemsMod.RANDOM`; Shuffle/Unchanged belegen sie nicht.
- Pool-Basis aus Diagnose 125: no-ban/no-TM `allowedShopItemPoolSize=536`, non-bad/no-TM `nonBadShopItemPoolSize=485`; vorhandene `badShopItems=36` bleiben Bestand, kein Ban-Ergebnis.
- `FVX-ITEM-005` und `FVX-ITEM-006` bleiben `GUI-kompatibel`; `FVX-ITEM-007..009` bleiben `Write modelliert`.
- Naechster Minimalblock: Shop Random + Ban Bad Smoke.

# Roadmap Status Update - 2026-05-15 - Shop Items Random reload smoke

- Neuer Befund: `08_tests/randomizer/125_shop_items_random_reload_smoke.md`.
- `FVX-ITEM-006 Shop Items Random` ist im getesteten Shop-only CFRU/DPE Gen9-BPRE Scope `GUI-kompatibel`.
- Smoke-Ergebnis: Save/Log/Output/Reload true, `shopCountBefore/After/Reload=23`, `shopItemsTotalBefore/After/Reload=157`, `shopItemReloadMismatches=0`, Laengen-/Skip-/Special-Policy-Mismatches `0`.
- Pool-Befund: aktiver no-ban/no-TM Shop-Random-Pool `allowedShopItemPoolSize=536`, Vergleichspool `nonBadShopItemPoolSize=485`, invalid/unloaded/fallback/placeholder Writes `0`.
- Preise, Field Items, Pickup und Held Items blieben unveraendert: `priceTableTouched=false`, `priceReloadMismatches=0`, Fremdscope-Flags `false`.
- `FVX-ITEM-007..009` bleiben `Write modelliert`; naechster Minimalblock ist ein Shop Item Bans Scope-Plan.

# Roadmap Status Update - 2026-05-15 - Shop Items Shuffle reload smoke

- Neuer Befund: `08_tests/randomizer/124_shop_items_shuffle_reload_smoke.md`.
- `FVX-ITEM-005 Shop Items Shuffle` ist im getesteten Shop-only CFRU/DPE Gen9-BPRE Scope `GUI-kompatibel`.
- Smoke-Ergebnis: Save/Log/Output/Reload true, `shopCountBefore/After/Reload=23`, `shopItemsTotalBefore/After/Reload=157`, `shopItemReloadMismatches=0`, Laengen-/Skip-/Special-Policy-Mismatches `0`.
- Preise, Field Items, Pickup und Held Items blieben unveraendert: `priceTableTouched=false`, `priceReloadMismatches=0`, Fremdscope-Flags `false`.
- `FVX-ITEM-006..009` bleiben `Write modelliert`; naechster Minimalblock ist `test/upr-fvx-cfru-dpe-shop-items-random-reload-smoke`.

# Roadmap Status Update - 2026-05-15 - Shop Items candidate diagnostics

- Neuer Befund: `08_tests/randomizer/123_shop_items_scope_diagnostics_candidate.md`.
- Read-only Shop-Kandidatendiagnose ist stabil: `candidateLoaded=true`, `shopScanSuccessful=true`, `shopCount=23`, `shopItemsTotal=157`, `terminatorModelStable=true`, `shopLengthMismatch=0`.
- Item-Safety fuer den sichtbaren Shopbestand: invalid/unloaded/fallback/placeholder `0`; vorhandene `badShopItems=36` und `tmShopItems=6` bleiben spaetere Pool-/Ban-Themen.
- `FVX-ITEM-005..009` bleiben `Write modelliert`; Diagnose 123 belegt nur die Voraussetzung fuer einen Shop Shuffle Smoke.
- Naechster Minimalblock: `test/upr-fvx-cfru-dpe-shop-items-shuffle-reload-smoke`.

# Roadmap Status Update - 2026-05-15 - Shop Items diagnostics preflight

- Neuer Befund: `08_tests/randomizer/122_shop_items_scope_diagnostics.md`.
- Shop read-only Kandidatendiagnose ist blockiert, weil keine explizit freigegebene lokale CFRU/DPE Gen9-BPRE-Kandidatenquelle fuer diesen Block vorlag.
- `FVX-ITEM-005..009` bleiben `Write modelliert`; kein Shop Shuffle Smoke vor erfolgreichem Kandidatenscan.
- Codepfad-Risiko bleibt bestaetigt: Shoplisten nutzen Pointer, Terminatoren, Laengen und `DataRewriter<Shop>`/Repointing; Preisfelder bleiben separat.
- Keine Codeaenderung, kein Build, kein Randomizer-Write/Save, keine Submodule-Pin-Aenderung.

# Roadmap Status Update - 2026-05-15 - Shop Items scope diagnostics plan

- Neuer Plan: `08_tests/randomizer/121_shop_items_scope_diagnostics_plan.md`.
- Shops werden als eigener CFRU/DPE Gen9-BPRE Item-Writer-Scope nach Field Items und Pickup gefuehrt.
- `FVX-ITEM-005..009` bleiben `Write modelliert`; Diagnose 121 definiert erst Codepfade, Datenstruktur, Risiken, Preserve-/Skip-Policy, Metriken und Reihenfolge.
- Naechster Minimalblock: `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics`.
- Keine Codeaenderung, kein Build, kein Randomizer-Lauf, keine Submodule-Pin-Aenderung.

# Roadmap Status Update - 2026-05-15 - Pickup Ban Bad complete

- `FVX-ITEM-010 Pickup Items Random / Ban Bad Items` is now `GUI-kompatibel` in the Pickup-only Random scope after Diagnose 118 and 120.
- Diagnose 120 confirms Ban Bad with `badPickupItemWrites=0`, non-bad pool `485`, and reload mismatches `0`.
- Field Items retain their documented GUI-compatible sub-scope status.
- Shops and Held Items remain separate and are not upgraded by Pickup results.
- Next active P1 block: `analysis/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-plan`.

# Roadmap Status Update - 2026-05-15 - Pickup Ban Bad planning

- `FVX-ITEM-010 Pickup Items Random` is reload-stable and GUI-compatible for `banBadRandomPickupItems=false` after Diagnose 118.
- Diagnose 119 plans the remaining Pickup Ban Bad sub-scope.
- No fix is recommended before the next smoke because Ban Bad only swaps the Pickup candidate pool to `getNonBadItems()`.
- Next active P1 block: `test/upr-fvx-cfru-dpe-pickup-items-random-ban-bad-reload-smoke`.
- Field Items remain at their documented status; Shops and Held Items remain separate scopes.

# Roadmap Status Update - 2026-05-15 - Pickup reload locator fix

- Added `08_tests/randomizer/118_pickup_items_reload_locator_fix.md`.
- UPR-FVX PR #38 fixes the Pickup table reload locator in the CFRU/DPE Gen9-BPRE gate without changing Pickup pool policy.
- Pickup Random with `banBadRandomPickupItems=false` now saves, logs, outputs and reloads with `pickupItemReloadMismatches=0`.
- `FVX-ITEM-010 Pickup Items Random` is GUI-compatible only for the no-Ban-Bad Pickup-only scope.
- Pickup Ban Bad, Shops and Held Items remain separate.

# Roadmap Status Update - 2026-05-15 - Pickup reload locator blocker planned

- Added `08_tests/randomizer/117_pickup_items_reload_locator_blocker_plan.md`.
- `FVX-ITEM-010 Pickup Items Random` remains `Write modelliert`: save/log/output/reopen works, but fresh reload cannot locate the Pickup table after random write.
- Likely root cause: the Gen3 pickup table locator is content-based and searches for the pre-randomization item sequence; the same handler succeeds only because it caches the found table offset.
- Next recommended block: `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- Pickup Ban Bad, Shops and Held Items remain separate and are not upgraded.

# Roadmap Status Update - 2026-05-15 - Field Items Random Ban Bad reload smoke

- Added `08_tests/randomizer/112_field_items_random_ban_bad_reload_smoke.md`.
- Field Items: `FVX-ITEM-002` with `banBadRandomFieldItems=true` saves, logs, reloads and preserves Field-Item slot policy with `fieldItemReloadMismatches=0` and `badFieldItemWrites=0`.
- `FVX-ITEM-004` is tested for `FieldItemsMod.RANDOM`, but remains not fully GUI-compatible until Random Even + Ban Bad is smoked separately.
- Next P1 step: `test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke`.

# Roadmap Status Update - 2026-05-15 - Field Items Ban Bad scope plan

- Added `08_tests/randomizer/111_field_items_ban_bad_scope_plan.md`.
- Field Items: `FVX-ITEM-004` is planned as a Non-TM random-pool filter, not a separate writer.
- Ban Bad should be smoked first with `FieldItemsMod.RANDOM` and `banBadRandomFieldItems=true`; Random Even + Ban Bad remains a second smoke.
- `FVX-ITEM-001`, `FVX-ITEM-002`, and `FVX-ITEM-003` keep their documented narrow GUI-compatible statuses; `FVX-ITEM-004` remains `Write modelliert`.
- Next P1 step: Field-Items-only Random Ban-Bad reload smoke.

# Roadmap Status Update - 2026-05-15 - Field Items Random Even reload smoke

- Added `08_tests/randomizer/110_field_items_random_even_reload_smoke.md`.
- Field Items: `FVX-ITEM-003` now has a successful CFRU/DPE Field-Items-only Random-Even Write-/Reload-Smoke with `banBadRandomFieldItems=false`.
- API/raw TM-slot alignment remains stable: `apiTmFieldItemSlots=28`, `rawTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`; TMs were not made globally allowed.
- `FVX-ITEM-001`, `FVX-ITEM-002`, and `FVX-ITEM-003` are `GUI-kompatibel` in their documented narrow Field-Items scopes; `FVX-ITEM-004` remains `Write modelliert`.
- Next P1 step: separate Ban-Bad-Items scope plan before enabling the option.

# Roadmap Status Update - 2026-05-15 - Field Items API TM-slot reload smoke

- Added `08_tests/randomizer/109_field_items_api_tm_slot_reload_smoke.md`.
- Field Items: `FVX-ITEM-002` now has a successful CFRU/DPE Field-Items-only Random Write-/Reload-Smoke with `banBadRandomFieldItems=false`.
- API/raw TM-slot alignment is stable: `apiTmFieldItemSlots=28`, `rawTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`; TMs were not made globally allowed.
- `FVX-ITEM-001` remains `GUI-kompatibel`; `FVX-ITEM-002` is `GUI-kompatibel` only for the narrow Random scope with Ban Bad inactive; `FVX-ITEM-003` and `FVX-ITEM-004` remain `Write modelliert`.
- Next P1 step: separate Field-Items-only Random Even reload smoke.

# Roadmap Status Update - 2026-05-15 - Field Items API TM-slot fix prepared

- Added `08_tests/randomizer/108_field_items_api_tm_slot_scope_fix.md`.
- UPR-FVX PR #37 is open for the CFRU/DPE Field-Items API TM-slot scope fix.
- Workspace now pins `02_external/upr-fvx` to `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- `FVX-ITEM-002` remains below GUI-compatible until a separate reload smoke passes.

# Roadmap Status Update - 2026-05-15 - Field Items API TM-slot scope plan

- Added `08_tests/randomizer/107_field_items_random_api_tm_slot_scope_plan.md`.
- Field Items Random remains blocked after the TM-pool fix because the existing Gen3 Field-Items API filters TM slots through `Item::isAllowed`.
- Current recommendation: `compat/upr-fvx-cfru-dpe-field-items-api-tm-slot-scope-fix`, limited to `FVX-ITEM-002` and the CFRU/DPE Field-Items API TM-slot scope.
- `FVX-ITEM-001` remains GUI-compatible for Shuffle; `FVX-ITEM-002..004` remain below GUI-compatible except for their documented narrow statuses.

# Roadmap Status Update - 2026-05-15 - Field Items Random API TM-slot blocker

- Field Items: Diagnose 106 keeps `FVX-ITEM-002` blocked after the PR #36 TM-pool fix.
- Pool metrics are sufficient, but `getFieldItems()` exposes `0` TM slots to the Randomizer while raw diagnostics previously found `28` TM Field Item slots.
- `FVX-ITEM-001` remains `GUI-kompatibel`; `FVX-ITEM-002`, `FVX-ITEM-003`, and `FVX-ITEM-004` remain `Write modelliert`.
- Next P1 step: read-only API TM-slot scope plan before any further fix.

# Roadmap Status Update - 2026-05-15 - Field Items Random TM-pool fix prepared

- Field Items: `FVX-ITEM-002` TM-pool fix is prepared in UPR-FVX PR #36 and pinned in this workspace branch.
- `FVX-ITEM-001` remains `GUI-kompatibel` for the narrow Shuffle allowed-slot scope.
- `FVX-ITEM-002` remains pending until the dedicated reload smoke passes.
- `FVX-ITEM-003` and `FVX-ITEM-004` remain `Write modelliert`.
- Next P1 step: Field-Items-only Random TM-pool reload smoke; Shops and Pickup remain separate.

# Roadmap Status Update - 2026-05-15 - Field Items Random TM-pool blocker planned

- Field Items: Diagnose 104 plans the `FVX-ITEM-002` Random TM-pool blocker read-only.
- `FVX-ITEM-001` remains `GUI-kompatibel` for the narrow Shuffle scope.
- `FVX-ITEM-002`, `FVX-ITEM-003`, and `FVX-ITEM-004` remain `Write modelliert`.
- Next P1 step: narrow UPR-FVX Field-Items-Random TM-pool fix branch.
- Shops and Pickup remain separate follow-up scopes.

# Roadmap Status Update - 2026-05-15 - Field Items Random blocked

- Field Items: Diagnose 103 blocks `FVX-ITEM-002 Field Items Random` with `RandomizationException` before output/reload.
- `FVX-ITEM-001` remains `GUI-kompatibel` for the narrow Shuffle scope.
- `FVX-ITEM-002`, `FVX-ITEM-003` and `FVX-ITEM-004` remain `Write modelliert`.
- Next P1 step: read-only Random TM-pool blocker plan before any codefix.
- Shops and Pickup remain separate follow-up scopes.

# Roadmap Status Update - 2026-05-15 - Field Items Shuffle smoke complete

- Field Items: Diagnose 102 completes the first allowed-slot Write-/Reload-Smoke for `FVX-ITEM-001 Field Items Shuffle`.
- `FVX-ITEM-001` is `GUI-kompatibel` for the tested narrow Shuffle scope.
- `FVX-ITEM-002`, `FVX-ITEM-003` and `FVX-ITEM-004` remain `Write modelliert` and require separate smokes.
- Next P1 step: Field Items Random smoke without Ban Bad Items.
- Shops and Pickup remain separate follow-up scopes.

# Roadmap Status Update - 2026-05-14 - Field Items allowed-slot guard

- Field Items: Diagnose 101 bestaetigt den bestehenden allowed-slot Guard im Gen3 Writer read-only; kein UPR-FVX-Codefix und keine Submodule-Pin-Aenderung.
- `FVX-ITEM-001..004` bleiben `Write modelliert`, weil der fachliche Write-/Reload-Smoke ohne explizite Kandidatenfreigabe nicht ausgefuehrt wurde.
- Naechster P1-Schritt: separater `FVX-ITEM-001 Field Items Shuffle` Write-/Reload-Smoke mit explizit freigegebenem Kandidaten.
- Shops und Pickup bleiben getrennte Folge-Scope-Bloecke.

# Roadmap Status

Dieses Dokument ist die textbasierte Spiegelung der Excel-Roadmap. GitHub und Codex sollen dieses Dokument bevorzugt nutzen, weil Aenderungen hier sauber per Git-Diff nachvollziehbar sind.

## Statuslegende

| Status | Bedeutung |
|---|---|
| Erledigt | abgeschlossen und in GitHub dokumentiert |
| Review/Test | umgesetzt, aber noch zu prüfen oder zu mergen |
| Als Nächstes | nächster aktiver Arbeitsblock |
| In Arbeit | aktuell aktiv bearbeitet |
| Warten/Blockiert | wartet auf Entscheidung, Tool, Quelle oder externen Schritt |
| Noch offen | noch nicht begonnen |

## Aktueller Gesamtstand

| Feld | Wert |
|---|---|
| Projekt | FireRed Gen9 Randomizer Workspace |
| GitHub-Repo | `Planton361/firered-gen9-randomizer-workspace` |
| Source of Truth | GitHub + Markdown-Dokumente |
| Excel-Roadmap | visuelles Dashboard |
| Standardterminal | Linux/CachyOS Shell |
| Stabiler Branch | `main` |
| Branch Protection | eingerichtet |
| Aktueller Branch | `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write` |
| Nächster Branch | `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke` |
| Aktueller Fokus | CFRU/DPE Palette Normal Single-owner Write Guard Fix |
| ROM-/Build-Arbeit | UPR-FVX nicht-ROM Build-Checks; kein ROM-/Reload-Smoke und keine Output-ROMs |
| Externe Repos | als Submodule auf Planton361-Forks eingebunden |
| Forks | Planton361-Forks fuer UPR-FVX, DPE Gen9 und CFRU dokumentiert |
| Installationen | devkitPro/devkitARM lokal dokumentiert; keine Installation in diesem Analyseblock |

## Erledigt

| Paket | Aufgabe | Ergebnis |
|---|---|---|
| 01 Initial Setup | GitHub-Repo erstellt | `Planton361/firered-gen9-randomizer-workspace` existiert |
| 01 Initial Setup | `main` eingerichtet | `main` ist Default Branch und stabil |
| 01 Initial Setup | Branch Protection eingerichtet | `main` ist geschützt |
| 01 Initial Setup | Grundstruktur angelegt | `00_project-control`, `01_docs`, `02_external`, `03_tools`, `04_private_roms`, `05_builds`, `06_patches`, `07_scripts`, `08_tests` |
| 01 Initial Setup | `.gitignore` angelegt | ROMs, Saves, Builds, Tool-Binaries und private Dateien werden ausgeschlossen |
| 02 Projektkontext | Projektkontext angelegt | README, AGENTS, PROJECT_BRIEF, SESSION_STATE, NEXT_STEPS, DECISIONS_INDEX |
| 03 Repo Governance | Governance-Dokumente erstellt | Git-, Fork-, Codex-, Security- und Rebuild-Regeln dokumentiert |
| 04 Codex Start | Workflow-/Agent-Regeln dokumentiert | PRs #9, #10, #17, #18 gemerged |
| 05 Externe Quellen | read-only Analyseblock dokumentiert | Quellen und Tool-Manifest ohne Clone/Fork präzisiert |
| 06 Toolchain | Linux/CachyOS-Migration dokumentiert | Linux/CachyOS ist primaere lokale Umgebung; Windows-Befunde sind historisch |
| 06 Toolchain | Linux-GitHub-Auth dokumentiert | `gh` und `git fetch origin` nutzbar dokumentiert |
| 06 Toolchain | devkitPro/devkitARM lokal dokumentiert | `/opt/devkitpro`, `DEVKITARM`, `arm-none-eabi-gcc` und `grit` im Smoke-Test dokumentiert |
| 07 Build-Basis | DPE Gen9 Smoke-Build dokumentiert | Build erfolgreich; Output blieb lokal unter `05_builds/` |
| 07 Build-Basis | CFRU auf DPE Smoke-Build dokumentiert | Build erfolgreich; Output blieb lokal unter `05_builds/` |
| 08 Randomizer-Kompatibilität | UPR-FVX Source-Build dokumentiert | `compat/firered-gen9-cfru-dpe` baut/startet lokal |
| 08 Randomizer-Kompatibilität | erster Randomizer-/BizHawk-Smoke-Test dokumentiert | CFRU/DPE-ROM konnte geladen, minimal randomisiert, gespeichert und in BizHawk gebootet werden |
| 08 Randomizer-Kompatibilität | Route-1-Fallback-Wilddaten dokumentiert | CFRU Route-1-Custom-Day/Night-Wilddaten per Macro deaktiviert; Route 1 wieder als FVX-Fallback-Area sichtbar |
| 08 Randomizer-Kompatibilität | CFRU/DPE-Species-Diagnose dokumentiert | UPR-FVX PR #2 lokal gebaut/ausgefuehrt; Count-, Generation- und `<unknown>`-Rohwerte protokolliert |
| 08 Randomizer-Kompatibilität | CFRU/DPE-Species-Identity-Fix vorbereitet | UPR-FVX-Fixbranch trennt Dex-ID von SpeciesSet-Identitaet fuer erweiterte BPRE-Hacks |
| 08 Randomizer-Kompatibilität | CFRU/DPE-Species-Identity-Fix diagnostiziert | PR #3 hebt `speciesList.size` von 412 auf 799 und `maxSpeciesIdentityNumber` auf 823 |
| 08 Randomizer-Kompatibilität | Gen4+-Wild-Pool-Diagnose dokumentiert | All-Gens-Settings werden fuer Gen3-ROMs auf Gen1-3 gekappt; finaler Wild-Log enthaelt Gen4+ `0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE-UPR-FVX-Kompatibilitaetsmodell dokumentiert | RAM-Mapping zurueckgestellt; P0 bis P4 Fix-Reihenfolge dokumentiert |
| 08 Randomizer-Kompatibilität | Randomizer-/NatDex-Referenzen dokumentiert | Quelleninventar, Workflowmodell und Implementierungsnotizen fuer P0/P1 festgehalten |
| 08 Randomizer-Kompatibilität | CFRU-Documentation-Randomizer-Relevanz dokumentiert | PDF-Befunde zu Defines, Randomizer-Flags, Day/Night-Wild, Trainer-EVs, Save/RAM und Roadmap-Folgen festgehalten |
| 08 Randomizer-Kompatibilität | UPR-FVX Gen-Restrictions-Folgefix | PR #4 gemerged; finaler `RestrictedSpeciesService`-Pool enthaelt Gen4+-Species bei `limitPokemon=false` |
| 08 Randomizer-Kompatibilität | UPR-FVX Wild-Write-Folgefix | PR #5 gemerged; Vanilla/Fallback-Wild-Species werden fuer erweiterte BPRE-Hacks per interner Identitaet geschrieben |
| 08 Randomizer-Kompatibilität | P0-Post-Merge-Smoke | PR #3/#4/#5-Fixkette auf UPR-FVX Merge-Commit `843b75a8` bestaetigt; sichtbarer Wild-Log enthaelt Gen4+ `1030`, `<unknown>` `0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Encounter-Systemmodell | P0-supported sind Standard-Wild/Grass-Cave, Surfing, Fishing und Rock Smash; Day/Night, Swarms, Roamers, DexNav und Raids bleiben separat |
| 08 Randomizer-Kompatibilität | P1-Species-Schreibpfadmodell | Starters, Static/Gifts und Trainer-Species als kleinste praktische P1-Pfade priorisiert |
| 08 Randomizer-Kompatibilität | P1-Starters-only Diagnose | Seed `274269061345323` zeigte vor Fix Pawniard/Scraggy -> Drowzee/Jirachi durch Dex-ID-Schreibpfad |
| 08 Randomizer-Kompatibilität | P1-Starter-Write-Fix | UPR-FVX PR #6 gemerged; Starter werden fuer erweiterte BPRE-Hacks per interner SpeciesSet-Identitaet geschrieben |
| 08 Randomizer-Kompatibilität | Gen9-Species-Coverage-Analyse | DPE/CFRU-Source reicht bis Pecharunt/`NUM_SPECIES=1440`; aktueller FVX-Load bleibt bei `PokemonCount=823` |
| 08 Randomizer-Kompatibilität | PokemonCount-Cutoff-Diagnose | UPR-FVX PR #7 offen; Diagnose belegt `PokedexOrder`-Kappung bei interner ID `824` mit `pdEntry=1808` |
| 08 Randomizer-Kompatibilität | PokedexOrder-Modell | DPE `PokedexOrder` als Species-ID-Sortierlisten eingeordnet; FVX-Count-Sanity auf `pdEntry > 1023` ist fuer CFRU/DPE ungeeignet |
| 08 Randomizer-Kompatibilität | CFRU/DPE-Gen9-SpeciesCount-Fix | UPR-FVX PR #8 gemerged; Count erreicht `PokemonCount=1439`, Gen7/8/9 werden im Species-Load sichtbar |
| 08 Randomizer-Kompatibilität | Palette-Loader-Blocker-Modell | `loadPokemonPalettes()`-Abbruch auf `SPECIES_CUBONE_A`/`gMonPaletteTable[1038]` eingeordnet; Palette-Load ist P0/Wild-fachlich nicht noetig |
| 08 Randomizer-Kompatibilität | Defensiver Palette-Load/-Save-Fix | UPR-FVX PR #9 gemerged; fehlende Palette-Slots brechen den Load nicht mehr ab |
| 08 Randomizer-Kompatibilität | Save-Trainers-/Moveset-Blocker-Modell | `0x25e49c` als `PokemonMovesets + 826*4` eingeordnet; Ursache ist wahrscheinlich alter/falscher Learnset-Tabellenzugriff plus eager `saveTrainers()`-Moveset-Load |
| 08 Randomizer-Kompatibilität | Lazy-Trainer-Movesets-Unblocker | UPR-FVX PR #10 gemerged; Wild-only Save blockiert nicht mehr bei `saveTrainers()`/`getMovesLearnt()` |
| 08 Randomizer-Kompatibilität | Palette-Save-Blocker-Modell | `0x16b9c08` als DPE `gFrontSprite252Pal` eingeordnet; FVX schreibt unveraenderte/geteilte Paletten bedingungslos neu |
| 08 Randomizer-Kompatibilität | Skip-Unchanged-Palette-Save-Unblocker | UPR-FVX PR #11 gemerged; unveraenderte CFRU/DPE-Pokemon-Paletten werden nicht mehr neu geschrieben |
| 08 Randomizer-Kompatibilität | Gen9-Wild-Post-Merge-Smoke | UPR-FVX Merge-Commit `ee82cb4e` bestaetigt: `PokemonCount=1439`, Gen7/8/9 im Wild-Log, `<unknown>=0`, Save erfolgreich |
| 08 Randomizer-Kompatibilität | Randomizer-Smoke-Artefaktordnung | Lokale ignored Smoke-Outputs unter `05_builds/randomizer-smoke/` bereinigt; `08_tests/randomizer/README.md` dokumentiert Nummerierung und Latest-Konvention |
| 08 Randomizer-Kompatibilität | Wild-Bad-Egg-Diagnose | `12` `Bad Egg`-Slots liegen komplett in `Area #174 - ALTERING CAVE`; Ursache ist sehr wahrscheinlich `SPECIES_EGG=0x19C` im CFRU/DPE-Wild-Allowed-Pool |
| 08 Randomizer-Kompatibilität | CFRU/DPE-Special-Species-Wild-Ban | UPR-FVX PR #12 offen; lokaler Smoke zeigt `Bad Egg=0`, `<unknown>=0`, `saveSuccessful=true` |
| 08 Randomizer-Kompatibilität | UPR-FVX Wild-Fix-Pin | Workspace-Submodule `02_external/upr-fvx` ist auf Planton361-Fork-Commit `0f127e9b` fuer den CFRU/DPE-Wild-Sonder-Species-Fix gepinnt |
| 08 Randomizer-Kompatibilität | P1 Static/Gift Species-only Diagnose | Gen1-Gen9-Pool vorhanden und Pick erreicht Gen7/8/9; echter Save/Log blockiert an vier `<null>`-Static-Eintraegen |
| 08 Randomizer-Kompatibilität | P1 Static/Gift Scope und Write | UPR-FVX PR #13 gemerged; `009178e8` bestaetigt `saveSuccessful=true`, nichtleeren Static/Gift-Log und `writeReloadMismatches=0` |
| 08 Randomizer-Kompatibilität | P1 Trainer-Species-only Diagnose | Trainer-Pool enthaelt Gen1-Gen9, aber `randomizeTrainerPokes()` haengt vor Save/Log in `getRandomAbilitySlot()` auf Zero-Ability-Sonder-Species |
| 08 Randomizer-Kompatibilität | P1 Trainer-Scope und Species-Write | UPR-FVX PR #14 gemerged; Workspace PR #60 gemerged; `56ec749e` bestaetigt `saveSuccessful=true`, nichtleeren Trainer-Log und `writeReloadMismatches=0` |
| 08 Randomizer-Kompatibilität | P1 Evolution-Species-only Diagnose | Evolution-Pool Gen1-Gen9 bestaetigt; `saveSuccessful=true`, aber Direct Log-Fehler und `writeReloadMismatches=146` blockieren P1-Support |
| 08 Randomizer-Kompatibilität | P1 Evolution-Scope und Species-Write | UPR-FVX PR #15 gemerged; Workspace PR #63 gemerged; `18766c49` bestaetigt `saveSuccessful=true`, `logSuccessful=true`, Gen7/8/9 im Log und `writeReloadMismatches=0` |
| 08 Randomizer-Kompatibilität | P1 Trainer Held Items-only Diagnose | Trainer-Held-Item-Pool `52` und Trainer-Load `255`/`481` bestaetigt; Lauf blockiert vor Save/Log in `getMovesLearnt()` bei `0x25e49c` |
| 08 Randomizer-Kompatibilität | P1 Trainer Held Items lazy Moveset-/Learnset-Load | UPR-FVX `3864ad0e` bestaetigt `saveSuccessful=true`, nichtleeren Trainer-Log, `heldItemEntries=481` nach Reload und `writeReloadMismatches=0` |
| 08 Randomizer-Kompatibilität | P1 Trainer Movesets-only Diagnose | Trainer-Load stabil, aber `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel()` blockiert vor Save/Log in `getMovesLearnt()` bei `0x25e49c` |
| 08 Randomizer-Kompatibilität | P1 Trainer Movesets Learnsets-Fix | UPR-FVX PR #17 und Workspace PR #68 gemerged; `6557648` bestaetigt `saveSuccessful=true`, `logSuccessful=true`, `after/reload.movesetEntries=417` und `writeReloadMismatches=0` |
| 08 Randomizer-Kompatibilität | P1 Trainer Movesets Kombinationen | Workspace PR #69 gemerged; Movesets-only, Movesets+Species, Movesets+Held Items normal und sensible Held Items sind P1-stabil |
| 08 Randomizer-Kompatibilität | Gen8/9-Move-Datenmodell | Diagnose 033 dokumentiert `moves.total=559` vs. CFRU/DPE `MOVES_COUNT=992` und minimale Move-Data-Reader-Richtung |
| 08 Randomizer-Kompatibilität | CFRU/DPE Move-Data-Reader | UPR-FVX PR #18 und Workspace PR #71 gemerged; `moves.total=992`, hoechster Move `PsychicNoise` |
| 08 Randomizer-Kompatibilität | P1 TM/HM-only Diagnose | Workspace PR #72 gemerged; klassischer `50+8`-Scope blockierte an hohem Move-ID-Limit und Null-Type-Species |
| 08 Randomizer-Kompatibilität | P1 TM/HM Scope und Safety | UPR-FVX `32e43ac0` bestaetigt TM moves + Compatibility, Compatibility-only und TM moves-only mit Save/Log/Reload und `writeReloadMismatches=0` im klassischen `50+8`-Scope |
| 08 Randomizer-Kompatibilität | P1 TM/HM 128-Slot-Modell | CFRU/DPE `gTMHMMoves` als `u16[128]` ueber Pointer `0x8125A8C`, HMs Slots `121..128`, Compatibility 16 Bytes pro Species ueber `0x8043C68` dokumentiert |
| 08 Randomizer-Kompatibilität | P1 TM/HM 128-Slot-Fix | UPR-FVX `58379ffd` bestaetigt `tmCount=120`, `hmCount=8`, Save/Log/Reload fuer TM moves-only, Compatibility-only und TM moves + Compatibility mit `writeReloadMismatches=0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Tutor-/Special-Tutor-Modell | `gMoveTutorMoves` `u16[152]`, `gTutorLearnsets` `152` Bits und Special-Tutor-Sonderlogik read-only dokumentiert; Tutor-only noch nicht P1-supported |
| 08 Randomizer-Kompatibilität | CFRU/DPE Tutor-Scope-and-Compatibility-Fix | UPR-FVX `4ce93754` bestaetigt `tutorMoveCount=152`, 19-Byte-Compatibility-Stride und Save/Log/Reload fuer Tutor moves-only, Compatibility-only und kombinierte Tutor-Laeufe mit `writeReloadMismatches=0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Egg-Move-Modell | `gEggMoves` als `u16`-Stream mit `species + 20000` und `0xFFFF` dokumentiert; DPE-Stream enthaelt Gen8/9-Species und Move-IDs bis `967`; Egg-Move-only braucht separaten Fix |
| 08 Randomizer-Kompatibilität | CFRU/DPE Egg-Move-Scope und Write | UPR-FVX `18168b78` bestaetigt `gEggMoves` ueber `0x45C50`, interne SpeciesSet-Keys, Gen8/9-Species und Gen9-Moves mit `writeReloadEggMoveMismatches=0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Learnset-Write-Modell | `gLevelUpLearnsets` ueber `0x03EA7C`, internes Species-Indexing, `u16 move + u8 level`, Sentinel `{0, 0xFF}` und bounded-in-place-Folgepfad dokumentiert |
| 08 Randomizer-Kompatibilität | CFRU/DPE Learnset-Write bounded in-place | UPR-FVX `dd9d80c1` bestaetigt sicheren bounded Writer fuer validierte same-size Learnsets mit `writeReloadLearnsetMismatches=0`; Full Write bleibt separat |
| 08 Randomizer-Kompatibilität | FVX-GUI-Options-Kompatibilitaetsmatrix | P1-supported, teilunterstuetzte, offene und blockierte FVX-GUI-Optionsbereiche fuer den getesteten CFRU/DPE Gen9-BPRE-Stand dokumentiert |
| 08 Randomizer-Kompatibilität | CFRU/DPE Learnset-Write Repointing-Fix | UPR-FVX `77de517d` bestaetigt Full `setMovesLearnt()`-Repointing mit validierter FreeSpace-Region, `pointertableEntriesUpdated=1413` und `writeReloadLearnsetMismatches=0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Learnset GUI-Kombinationsdiagnose | Diagnose 048 bestaetigt ersten GameRandomizer-Repointing-Write mit `writeReloadLearnsetMismatches=0`, blockiert aber vollen GUI-P1-Support durch Logger, Trainer-Movesets, Reorder-Damaging und Level-Up-Sanity |
| 08 Randomizer-Kompatibilität | CFRU/DPE Learnset GUI-Flow-Safety-Fix | UPR-FVX `086d2a91` bestaetigt Movesets-only, Trainer-Movesets, Reorder-Damaging, TM/HM-Sanity, Tutor-Sanity, gekoppelte Egg Moves und TM/HM+Tutor-Sanity mit Save/Log/Output/Reload und `writeReloadLearnsetMismatches=0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Base Stats, Types, Abilities Modell | `gBaseStats` ueber `0x080001BC`, Entry-Size `0x1C`, Species-Scope `NUM_SPECIES=1440`, Fairy/Stellar-Type-, Hidden-Ability-, Ability-Count- und Item-Count-Risiken dokumentiert |
| 08 Randomizer-Kompatibilität | CFRU/DPE Base Stats + Types Scope-and-Write-Fix | UPR-FVX `20f16d07` bestaetigt Base Stats-only, Types-only und Base Stats + Types mit Save/Log/Reload, `writeReloadBaseStatsMismatches=0` und `typeIdMismatches=0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Ability1/2 + Hidden Ability Scope-and-Write-Fix | UPR-FVX Commit `639c7e61`; Diagnose 052 bestaetigt Ability1/2-only, Hidden Ability-only, Ability1/2 + Hidden Ability und Base Stats + Types + Abilities mit Save/Log/Reload, `writeReloadAbilityMismatches=0` und `writeReloadHiddenAbilityMismatches=0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Item-/Bad-Item-/Encounter-Held-Item-Modell | Diagnose 053 dokumentiert CFRU/DPE Itemgrenzen `779`/ca. `799`, klassischen FVX-`ItemCount=374`, moderne Bad-/Key-Item-Risiken und Encounter-Held-Item-Felder `item1/item2` bei `0x0C`/`0x0E`; Encounter Held Items brauchen separaten Fixbranch |
| 08 Randomizer-Kompatibilität | CFRU/DPE Encounter Held Items Scope-and-Write-Fix | UPR-FVX Commit `5c7170b6`; Diagnose 054 bestaetigt Item-Scope bis `778`, moderne Bad-/Banned-Filter und Encounter Held Items-only sowie Kombinationen mit Base Stats, Abilities und Types mit Save/Log/Reload und `writeReloadEncounterHeldItemMismatches=0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Type-Log-/Placeholder-Hygiene | Diagnose 055 klassifiziert `Bad Egg`, `<unknown>`, Unknown-Type-/Ability-/Item-Fallbacks und Null-/BST-zero-/all-zero-Ability-Species aus bestehenden Protokollen; Marker aus 051/052/054 blockieren P1-Support nicht bei stabilen Save/Log/Output/Reload-Kriterien und `0` Mismatches |
| 08 Randomizer-Kompatibilität | CFRU/DPE Move-Data-Write-Modell | Diagnose 056 modelliert `moves.total=992`, `991:PsychicNoise`, `BattleMove.split`, aktuelle `saveMoves()`-Teilfeldwrites, Preserve-Policy und Reload-Kriterien fuer spaeteren Fix |
| 08 Randomizer-Kompatibilität | CFRU/DPE MoveData Write Preserve Fix | UPR-FVX `bb5ee119` schreibt klassische MoveData-Bytes `+0..+4` weiter und im CFRU/DPE-Gate `BattleMove.split` bei `+10`; Preserve-Bytes bleiben unangetastet |
| 08 Randomizer-Kompatibilität | CFRU/DPE MoveData Write Preserve Reload-Smoke | Workspace PR #125 gemerged; Diagnose 084 bestaetigt `Update Moves` mit Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `moves.total=992`, `991:PsychicNoise`, stabiler category/split-Reload und `preserveByteMismatchesUnchangedMoves=0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE MoveData Power/Accuracy/PP Reload-Smoke | Diagnose 085 bestaetigt `FVX-MOVE-001/002/003` mit Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, stabilen `+1/+3/+4` Bytes und `preserveByteMismatchesAllMoves=0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE MoveData Types Reload-Smoke | Diagnose 086 dokumentiert `FVX-MOVE-004` mit Save/Log/Output/Reload true und stabilen Preserve-Bytes, blockiert aber durch Fairy-Type-Byte-Mismatches: `writeReloadMoveDataMismatches=54`, `typeReloadMismatches=54`, `cfruDpeTypeByteMismatches=54` |
| 08 Randomizer-Kompatibilität | CFRU/DPE MoveData Fairy-Type-Byte Fix | UPR-FVX PR #34 und Workspace PR #129 gemerged; UPR-FVX `fad56f60` und Diagnose 087 bestaetigen `FVX-MOVE-004` mit Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0` und Preserve-Bytes bytegleich |
| 08 Randomizer-Kompatibilität | MoveData Writer / Update Moves / Power / Accuracy / PP / Types | `FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel; MoveData-Writer-Preserve, Split, Power, Accuracy, PP und Fairy-Type-Byte sind im CFRU/DPE Gen9-BPRE-Scope belegt |
| 08 Randomizer-Kompatibilität | Move Names / Descriptions Text/Menu-Scope Plan | Diagnose 088 dokumentiert `FVX-MOVE-005` als getrennten Text/Menu-Scope; Name-only fixed-length Smoke ist realistisch, Move Descriptions / Text/Menu-Repointing bleibt zurueckgestellt |
| 08 Randomizer-Kompatibilität | Move Names fixed-length Reload-Smoke Versuch | Diagnose 089 dokumentiert den blockierten Name-only-Smoke: kein freigegebener lokaler CFRU/DPE Gen9-BPRE-Kandidat mit `moves.total=992` und `991:PsychicNoise`; `FVX-MOVE-005` bleibt `Write modelliert` |
| 08 Randomizer-Kompatibilität | Move Names fixed-length Reload-Smoke Retry | Diagnose 090 dokumentiert den blockierten Retry-Preflight: `candidateFilesChecked=94`, `candidatePreflightSuccessful=false`, kein fachlicher Smoke; `FVX-MOVE-005` bleibt `Write modelliert` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Field Items/Shops/Pickup-Modell | Diagnose 057 modelliert Field Items, Shops, Pickup und allgemeine Item-Randomization getrennt von Encounter Held Items; eigene Preserve-/Skip-Policy und Reload-Kriterien dokumentiert |
| 08 Randomizer-Kompatibilität | CFRU/DPE Palette-Randomization-Modell | Diagnose 058 trennt Palette-Safety/Skip-Unchanged-Save von echter geaenderter Palette-Randomization; compressed/shared/repointing risks, Preserve-/Skip-Policy, Reload-Kriterien und Graphics/P2-Abgrenzung dokumentiert |
| 08 Randomizer-Kompatibilität | CFRU/DPE Palette Randomization Preserve/Repoint Plan | Diagnose 091 dokumentiert echte `PokemonPalettesMod.RANDOM`-Randomization als komprimierten Repointing-/Shared-Pointer-Writer; direkter Fix noch nicht eng genug, zuerst read-only Pointer-/Compression-Diagnose |
| 08 Randomizer-Kompatibilität | CFRU/DPE Palette Pointer / Compression Diagnostics Plan | Diagnose 092 plant die read-only Klassifikation von Normal-/Shiny-Palette-Pointern, Dekomprimierbarkeit, Single-Owner/Shared, missing/invalid und sicheren Kandidaten; kein Fix, kein Repointing |
| 08 Randomizer-Kompatibilität | CFRU/DPE Palette Pointer / Compression Diagnostics Run | Diagnose 093 bestaetigt sanitisiert `candidateLoaded=true`, `candidateWritablePalettes=385`, aber `candidateWritableShinyPalettes=0`; naechster Scope nur normal-palette-only single-owner/decompressible |
| 08 Randomizer-Kompatibilität | CFRU/DPE Type-Chart-Modell | Diagnose 059 trennt Pokemon-Type-Read/Write aus 051 von Type-Chart-/Effectiveness-Randomization; Fairy `0x17`, Stellar/unsupported `0x18`, TypeTable-Risiken, Preserve-/Skip-Policy und Reload-Kriterien dokumentiert |
| 08 Randomizer-Kompatibilität | CFRU/DPE GUI-Suboptions-Regressionsmatrix | Diagnose 060 ordnet konkrete FVX-GUI-Hauptoptionen und Suboptionen konservativ nach P1-supported, wahrscheinlich supported, modelliert/open und out-of-scope ein |
| 08 Randomizer-Kompatibilität | CFRU/DPE P1 Regression-Smoke-Plan | Diagnose 061 plant priorisierte Regression-Smoke-Gruppen aus 060 und der FVX Feature-Coverage-Matrix, ohne Testausfuehrung oder offene Writer zu vermischen |
| 08 Randomizer-Kompatibilität | CFRU/DPE Global Species Pool Regression-Smoke-Plan | Diagnose 062 plant `FVX-GEN-001` Limit Pokemon inklusive Generation Limits / related Pokemon und `FVX-GEN-002` No Premature Evolutions gegen einen einzelnen stabilen Species-Carrier, ohne offene Writer und ohne Testausfuehrung |
| 08 Randomizer-Kompatibilität | CFRU/DPE Starters Suboptions Regression-Smoke-Plan | Diagnose 063 plant `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` ueber den belegten `FVX-SST-002`-Starter-Carrier; Starter Held Items und offene Writer bleiben ausgeschlossen |
| 08 Randomizer-Kompatibilität | CFRU/DPE Global Species Pool Regression-Smoke-Ergebnisse | Diagnose 064 dokumentiert sanitisiert Baseline Carrier, `FVX-GEN-001` Generation Limits, `FVX-GEN-001` related Pokemon und `FVX-GEN-002` No Premature Evolutions im `FVX-SST-002`-Starter-Carrier-Smoke mit Save/Log/Reload true, `Starter-Mismatches=0` und `stacktrace=none` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Starters Suboptions Regression-Smoke-Ergebnisse | Diagnose 065 dokumentiert sanitisiert `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` im Starter-Species-Writer-Smoke mit Save/Log/Reload true, `Starter-Mismatches=0`, `Filterverletzungen=0` und `stacktrace=none` |
| 08 Randomizer-Kompatibilität | CFRU/DPE TypeChart Preserve Effectiveness Fix | UPR-FVX `36707e01` und Diagnose 066 bestaetigen TypeEffectiveness-only mit Save/Log/Output/Reload true, `writeReloadTypeChartMismatches=0`, Fairy-Reload als raw `0x17`, unsupported/Stellar-Preserve und erhaltene Foresight-/Endtable-Terminatoren |
| 08 Randomizer-Kompatibilität | CFRU/DPE TypeEffectiveness-Folgesmoke-Plan | Diagnose 067 plant read-only einzelne Slices fuer `FVX-TYPE-001` Balanced, Keep Type Identities und Inverse, `FVX-TYPE-002` Add Random Immunities sowie `FVX-TYPE-003` Update Type Effectiveness |
| 08 Randomizer-Kompatibilität | CFRU/DPE TypeEffectiveness-Folgesmoke-Ergebnisse | Diagnose 068 bestaetigt Balanced, Keep Type Identities, Inverse, Add Random Immunities und Update Type Effectiveness jeweils mit Save/Log/Output/Reload true, `writeReloadTypeChartMismatches=0`, erhaltenen Terminatoren und `stacktrace=none` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Similar Strength / Same Type Regression-Smoke-Plan | Diagnose 069 plant Wild-, Trainer- und Evolution-Slices fuer Similar Strength, Same Type, Type Themes und Type Restrictions ohne Testausfuehrung und ohne offene Writer |
| 08 Randomizer-Kompatibilität | CFRU/DPE Similar Strength / Same Type Regression-Smoke-Ergebnisse | Diagnose 070 dokumentiert sanitisiert: Trainer Similar Strength unter `FVX-FOE-001` stabil; Wild Similar Strength, Wild Type Restrictions, `FVX-FOE-009` und Evolutions Same Typing blockieren; Evolutions Similar Strength reloadet mit Mismatches |
| 08 Randomizer-Kompatibilität | CFRU/DPE 070 Blocked Slices Follow-up Plan | Diagnose 071 plant read-only getrennte Folgeanalysen fuer Wild-Carrier-/Placeholder-Scope, Trainer-Type-Diversity, Evolution-Reload-/Bad-Egg-Scope und Evolution-Same-Typing-/Null-Scope |
| 08 Randomizer-Kompatibilität | CFRU/DPE Wild 070 Blockers Diagnostics Plan | Diagnose 072 plant read-only die gemeinsame Wild-Diagnose fuer `FVX-WILD-011` und `FVX-WILD-004` im `FVX-WILD-001` Carrier, getrennt nach BST-/Species-Pool-Filter, Species-Type-Filter und Wild-Nullslot-/Placeholder-Scope |
| 08 Randomizer-Kompatibilität | CFRU/DPE Wild Filter Carrier Diagnostics Plan | Diagnose 073 plant read-only Code-/Protokollanalyse und ggf. einen separaten Freigabeschritt fuer lokale Wild-Carrier-Diagnose, um Carrier-Scope von BST-/Type-Filter-Scope zu trennen |
| 08 Randomizer-Kompatibilität | CFRU/DPE Wild Filter Carrier Code Diagnosis | Diagnose 074 grenzt die wahrscheinliche Ursache der 070-Wild-`IllegalStateException` auf den `GAME`-Mapping-/InfoMap-Nullslot-Pfad im WildEncounterRandomizer ein |
| 08 Randomizer-Kompatibilität | CFRU/DPE Wild Filter Carrier Nullslot Fix | UPR-FVX `acaada51` und Diagnose 075 bestaetigen `FVX-WILD-011` und `FVX-WILD-004` mit Save/Log/Output/Reload true, `writeReloadWildPokemonMismatches=0`, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none` |
| 08 Randomizer-Kompatibilität | CFRU/DPE Trainer Type Diversity Null-Type Fix | UPR-FVX `d89fc64e` und Diagnose 078 bestaetigen `FVX-FOE-009` mit Save/Log/Output/Reload true, `writeReloadTrainerPokemonMismatches=0`, `filterViolations=0`, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`; Trainer Similar Strength bleibt stabil |
| 08 Randomizer-Kompatibilität | CFRU/DPE Evolution Same Typing Code Diagnosis | Diagnose 079 grenzt die wahrscheinliche Ursache von `FVX-TRAIT-019` auf `to.hasSharedType(...)` im `EvolutionRandomizer` Same-Typing-Filter mit Null-Primary-Type-Kandidaten ein |
| 08 Randomizer-Kompatibilität | CFRU/DPE Evolution Same Typing Null-Type Fix | UPR-FVX `74d88a7a` und Diagnose 080 bestaetigen `FVX-TRAIT-019` mit Save/Log/Output/Reload true, `writeReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`; `Bad Egg` bleibt nach 055 klassifiziert |
| 08 Randomizer-Kompatibilität | CFRU/DPE Evolution Similar Strength Mismatch Diagnostics | Diagnose 081 grenzt `FVX-TRAIT-018` wahrscheinlich auf einen zu breiten Diagnosevergleich gegen nicht persistierte Forme-/Zusatzfelder ein; naechster Schritt ist ein normalisierter Diagnose-Smoke, kein sofortiger Fix |
| 08 Randomizer-Kompatibilität | CFRU/DPE Evolution Similar Strength Normalized Reload Diagnostics | Diagnose 082 bestaetigt `FVX-TRAIT-018` mit Save/Log/Output/Reload true, `normalizedWriteReloadEvolutionMismatches=0`, `rawWithFormeWriteReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`; `Bad Egg=true` bleibt nach 055 klassifiziert |

## In Arbeit

| Paket | Aufgabe | Ziel |
|---|---|---|
| 08 Randomizer-Kompatibilität | Palette Pointer / Compression Diagnostics Run | Branch `test/upr-fvx-cfru-dpe-palette-pointer-compression-diagnostics`; Diagnose 093 dokumentieren und PR vorbereiten |

## Als Nächstes

| Paket | Aufgabe | Ziel |
|---|---|---|
| 08 Randomizer-Kompatibilität | Palette Single-owner Normal-only Fix-Scope Plan | read-only klaeren, ob ein Fix-/Smoke-Scope fuer `candidateWritableNormalPalettes=385` eng genug ist; Shiny/shared/invalid/missing/decode-failed preserve-only |
| 08 Randomizer-Kompatibilität | Evolution-Methoden-Writer und weitere Evolution-Suboptionen getrennt planen | Nicht aus Diagnose 082 ableiten; getrennte Scope- und Reload-Kriterien definieren |
| 08 Randomizer-Kompatibilität | Move Names fixed-length Reload-Smoke nur mit eindeutigem Kandidaten wiederholen | warten, bis ein freigegebener lokaler CFRU/DPE Gen9-BPRE-Kandidat vorab `moves.total=992` und `991:PsychicNoise` meldet; `FVX-MOVE-005` bleibt `Write modelliert` |

## Noch offen

| Paket | Aufgabe | Hinweise |
|---|---|---|
| 08 Randomizer-Kompatibilität | Trainer-Pokémon erweitern | Trainer-Species-only, Trainer-Held-Items-only und Trainer-Movesets-Kombinationen sind im getesteten P1-Scope supported; Gen8/9-Move-Datenmodell bleibt separat |
| 08 Randomizer-Kompatibilität | DPE-Gesamtumfang/PokemonCount praktisch bewerten | Count-Diagnose zeigt: Names bis Pecharunt, Movesets kappen auf 930, PokedexOrder kappt final auf 823; Modell empfiehlt Count nicht aus PokedexOrder abzuleiten |
| 08 Randomizer-Kompatibilität | Wild-Log-`<unknown>` aufloesen | eindeutige Rohwerte sind `rawInternalSpeciesId=0`; Nullslots separat klassifizieren |
| 08 Randomizer-Kompatibilität | CFRU-Day/Night-Custom-Wild-Tabellen analysieren | getrennt vom Vanilla/Fallback-Wild-Pool behandeln |
| 08 Randomizer-Kompatibilität | Learnsets testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Items/Moves/Abilities testen | späterer Einzeltest |
| 09 Ironmon | BizHawk-/Ironmon-Tracker-Anbindung prüfen | erst nach stabiler Randomizer-Kompatibilität |

## Geplante Folge-Arbeitspakete

| Reihenfolge | Branch | Ziel | Grenzen |
|---|---|---|---|
| P0 | `compat/upr-fvx-cfru-dpe-gen-restrictions` | finalen Gen4+-Allowed-Pool fuer erweiterte CFRU/DPE-BPRE-Hacks freigeben | PR #4 gemerged und post-merge bestaetigt |
| P0b | `compat/upr-fvx-cfru-dpe-wild-internal-species-write` | Wild-Encounter-Schreibpfade auf interne Species-Identitaet fuer erweiterte BPRE-Hacks pruefen | PR #5 gemerged und post-merge bestaetigt |
| P1 | `analysis/upr-fvx-cfru-dpe-p1-species-write-paths` | Trainer, Starters, Static Pokemon, Evolutions, Learnsets und TM/Tutor-Kompatibilitaet diagnostizieren | Analysebranch; Ergebnis priorisiert Starters, Static/Gifts und Trainer-Species als erste praktische Tests |
| P1a | `analysis/upr-fvx-cfru-dpe-p1-starter-write-diagnostics` | Starters-only Write-/Reload-Diagnose | Diagnose zeigt: Pool enthaelt Gen4+, Write/Reload faellt ueber Dex-ID auf Gen1-3 zurueck |
| P1b | `compat/upr-fvx-cfru-dpe-starter-internal-species-write` | Starter-Schreibpfad auf interne SpeciesSet-Identitaet fuer erweiterte BPRE-Hacks umstellen | UPR-FVX PR #6 gemerged; Seed `274269061345323` reloadet Pawniard/Scraggy korrekt |
| Coverage | `analysis/upr-fvx-cfru-dpe-gen9-species-coverage` | Source-Umfang bis Gen9 gegen FVX-Load bis `PokemonCount=823` einordnen | read-only Dokumentation; keine ROM-Zugriffe |
| Coverage follow-up | `analysis/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics` | konkrete Count-Abbruchursache lokal mit ROM diagnostizieren | UPR-FVX PR #7; direkte Ursache ist `PokedexOrder` ID `824` = `1808`, keine Fixes |
| Coverage model | `analysis/upr-fvx-cfru-dpe-pokedex-order-model` | sichere Count-Strategie fuer CFRU/DPE-Gen9 modellieren | PokedexOrder und Moveset-Pointer getrennt bewerten; kein Static/Gift-Fix |
| Coverage fix | `compat/upr-fvx-cfru-dpe-gen9-species-count` | CFRU/DPE-spezifischen Count-Fix vorbereiten | UPR-FVX PR #8 gemerged; Count erreicht 1439 |
| Coverage follow-up | `analysis/upr-fvx-cfru-dpe-palette-loader-blocker` | Paletten-Loader-Blocker nach `PokemonCount=1439` modellieren | `SPECIES_CUBONE_A`-Palette-Nullslot als erster Abbruch; kein Fix |
| Coverage unblock | `compat/upr-fvx-cfru-dpe-defensive-palette-loading` | defensiver Palette-Load/-Save fuer CFRU/DPE | UPR-FVX PR #9 gemerged; kein Count-, Moveset-, Static/Gift-, Trainer- oder Learnset-Fix |
| Coverage follow-up | `analysis/upr-fvx-cfru-dpe-save-trainers-moveset-blocker` | `saveTrainers()`-/`getMovesLearnt()`-Blocker nach Palette-Fix analysieren | `0x25e49c` entspricht internem ID-Slot `826` / `SPECIES_ZYGARDE`; kein Fix |
| Coverage unblock | `compat/upr-fvx-cfru-dpe-save-trainers-lazy-movesets` | Learnset-Load im Trainer-Save nur bei tatsaechlichem Reset-Moves-Bedarf ausloesen | UPR-FVX PR #10 gemerged; kein Count-, Palette-, Learnset-Loader-, Static/Gift- oder Day/Night-Fix |
| Coverage follow-up | `analysis/upr-fvx-cfru-dpe-palette-save-blocker` | `savePokemonPalettes()`-Blocker nach Lazy-Trainer-Movesets analysieren | `saveSuccessful=false` bei `no compressed data found at offset 0x16b9c08`; kein Fix |
| Coverage unblock | `compat/upr-fvx-cfru-dpe-skip-unchanged-palette-save` | Palette-Save fuer unveraenderte CFRU/DPE-Pokemon-Paletten ueberspringen | UPR-FVX PR #11 gemerged; kein Count-, Learnset-, Trainer-, Static/Gift-, Wild- oder Day/Night-Fix |
| Coverage smoke | `analysis/upr-fvx-cfru-dpe-gen9-wild-post-merge-smoke` | komplette Gen9-Wild-only-Fixkette nach PR #11 bestaetigen | erledigt; `saveSuccessful=true`, Gen7/8/9 im Wild-Log, `<unknown>=0` |
| Maintenance | `maintenance/randomizer-smoke-artifact-cleanup` | lokale Smoke-Artefakte bereinigen und Protokoll-/Latest-Konvention dokumentieren | aktueller Dokumentationsbranch; keine Codeaenderungen, keine Builds, keine Randomizer-Laeufe |
| Wild cleanup | `analysis/upr-fvx-cfru-dpe-wild-bad-egg-diagnostics` | `Bad Egg` im bestaetigten Gen9-Wild-Log klassifizieren | Diagnosebranch; `SPECIES_EGG=0x19C` ist wahrscheinlich im Allowed Pool |
| Wild cleanup | `compat/upr-fvx-cfru-dpe-wild-banned-special-species` | CFRU/DPE-Sonder-Species aus Wild-Replacement-Pools bannen | UPR-FVX PR #12 offen; `SPECIES_EGG=0x19C` entfernt, `Bad Egg=0` bestaetigt |
| P1c | `analysis/upr-fvx-cfru-dpe-p1-static-gift-species-only` | Static-/Gift-Species-only Diagnose | Pool/Pick bestaetigt Gen1-Gen9; Save/Log blockiert an Null-Static-Scope |
| P1d | `compat/upr-fvx-cfru-dpe-static-gift-scope-and-write` | Static/Gift-Scope und interner Species-Write | UPR-FVX `009178e8`; lokal bestaetigt mit `saveSuccessful=true`, Gen7/8/9 im Log und `writeReloadMismatches=0` |
| P1e | `analysis/upr-fvx-cfru-dpe-p1-trainer-species-only` | Trainer-Species-only Diagnose | Trainer-Pool Gen1-Gen9 bestaetigt; blockiert vor Save in `getRandomAbilitySlot()` auf Zero-Ability-Sonder-Species |
| P1f | `compat/upr-fvx-cfru-dpe-trainer-scope-and-write` | Trainer-Scope und Species-Write | UPR-FVX `56ec749e`; lokal bestaetigt mit `saveSuccessful=true`, Gen7/8/9 im Log und `writeReloadMismatches=0` |
| P1g | `analysis/upr-fvx-cfru-dpe-p1-evolutions-species-only` | Evolution-Species-only Diagnose | Pool/Pick bestaetigt Gen1-Gen9; Save erzeugt Output-ROM, aber Direct-Log-Fehler und `writeReloadMismatches=146` |
| P1h | `compat/upr-fvx-cfru-dpe-evolutions-scope-and-write` | Evolution-Scope und Species-Write | UPR-FVX `18766c49`; lokal bestaetigt mit `saveSuccessful=true`, `logSuccessful=true`, Gen7/8/9 im Log und `writeReloadMismatches=0` |
| P1i | `analysis/upr-fvx-cfru-dpe-p1-trainer-held-items-only` | Trainer Held Items-only Diagnose | Pool/Trainer-Load bestaetigt; blockiert vor Save/Log in `getMovesLearnt()` bei `0x25e49c` |
| P1j | `compat/upr-fvx-cfru-dpe-trainer-held-items-lazy-movesets` | Trainer-Held-Items entblocken | UPR-FVX `3864ad0e`; lokal bestaetigt mit `saveSuccessful=true`, `heldItemEntries=481` nach Reload und `writeReloadMismatches=0` |
| P1k | `analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-only` | Trainer-Movesets-only Diagnose | blockiert vor Save/Log in `getMovesLearnt()` bei `0x25e49c`; kein Fix |
| P1l | `analysis/upr-fvx-cfru-dpe-p1-learnsets-model` | CFRU/DPE-Learnset-Modell analysieren | read-only Modell fuer `gLevelUpLearnsets`, bevor Trainer-Movesets-Fix versucht wird |
| P1m | `compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets` | Trainer-Movesets durch CFRU/DPE-Learnset-Reader entblocken | UPR-FVX PR #17 und Workspace PR #68 gemerged; `writeReloadMismatches=0` |
| P1n | `analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations` | Trainer-Movesets-Kombinationen diagnostizieren | erledigt; Movesets-only, Movesets+Species, Movesets+Held Items normal und sensible Held Items sind P1-stabil |
| P1o | `analysis/upr-fvx-cfru-dpe-p1-move-data-model` | Gen8/9-Move-Datenmodell analysieren | erledigt; Diagnose 033 dokumentiert `moves.total=559` vs. CFRU/DPE `MOVES_COUNT=992` |
| P1p | `compat/upr-fvx-cfru-dpe-move-data-reader` | CFRU/DPE-Move-Data-Reader minimal erweitern | erledigt; UPR-FVX PR #18 und Workspace PR #71 gemerged, `moves.total=992` |
| P1q | `analysis/upr-fvx-cfru-dpe-p1-tm-hm-only` | TM/HM-only Diagnose | erledigt; Workspace PR #72 gemerged, Fixbedarf fuer hohes Move-ID-Limit und Null-Type-Species belegt |
| P1r | `compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety` | TM/HM Scope und Safety | erledigt; `50+8`-Scope entblockt, kein 128-Slot-, Tutor-, Egg-, Learnset-Write- oder Move-Data-Write-Fix |
| P1s | `analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model` | TM/HM 128-Slot-Modell | aktueller Analysebranch; `gTMHMMoves`/`gTMHMLearnsets` Pointermodell dokumentiert, kein Fix |
| P1t | `compat/upr-fvx-cfru-dpe-tm-hm-128-slot` | TM/HM 128-Slot-Fix | erledigt; UPR-FVX `58379ffd` bestaetigt 120 TMs, 8 HMs, 128-Slot-Write/Reload und 128-Bit-Compatibility |
| P1u | `analysis/upr-fvx-cfru-dpe-p1-tutor-model` | Tutor-/Special-Tutor-Modell | erledigt; normale Tutor-Tabelle 152 Slots, Special Tutors separat |
| P1v | `compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility` | Tutor-Scope und Compatibility | erledigt; UPR-FVX `4ce93754` bestaetigt 152 Tutor-Moves, 19-Byte-Compatibility und Reload ohne Mismatches |
| P1w | `analysis/upr-fvx-cfru-dpe-p1-egg-move-model` | Egg-Move-Modell | erledigt; `gEggMoves` Streamformat und Gen8/9-Scope dokumentiert |
| P1x | `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write` | Egg-Move-Scope und Write | erledigt; UPR-FVX `18168b78` bestaetigt direct Egg-Move Write/Reload ohne Mismatches |
| P1y | `analysis/upr-fvx-cfru-dpe-p1-learnset-write-model` | Learnset-Write-Modell | erledigt; bounded in-place als minimaler Folgefix empfohlen |
| P1z | `compat/upr-fvx-cfru-dpe-learnset-write-bounded` | Learnset-Write bounded in-place | erledigt; UPR-FVX `dd9d80c1` speichert sichere same-size Learnsets ohne Repointing, voller Learnset-Write bleibt separat |
| P1aa | `analysis/upr-fvx-cfru-dpe-p1-learnset-repointing-model` | Learnset-Repointing-Modell | erledigt; Pointertable, Shared-Pointer-Policy und FreeSpace-Risiken read-only dokumentiert |
| P1ab | `analysis/upr-fvx-cfru-dpe-fvx-gui-options-matrix` | FVX-GUI-Options-Kompatibilitaetsmatrix | erledigt; P1-supported, teilunterstuetzte, offene und blockierte GUI-Optionsbereiche konsolidiert |
| P1ac | `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety` | Learnset GUI-Flow-Safety-Fix | erledigt; Logger, Multiwrite-Repointing, Trainer-Movesets und Level-Up-Sanity fuer Pokemon Movesets/Learnsets entblockt |
| P1ad | `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` | Base Stats, Types, Abilities Modell | erledigt; gemeinsames Datenmodell und getrennte Folgefixes dokumentiert |
| P1ae | `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write` | Base Stats + Types Scope-and-Write | erledigt; UPR-FVX `20f16d07` bestaetigt Fairy `0x17` Read/Write, Stellar preserve/skip und Reload ohne Mismatches |
| P1af | `compat/upr-fvx-cfru-dpe-abilities-hidden-ability-scope-and-write` | Ability1/2 + Hidden Ability Scope-and-Write | erledigt; Diagnose 052 bestaetigt `abilitiesPerSpecies=3`, `highestAbilityIndex=254` und Reload ohne Ability-/Hidden-Ability-Mismatches |
| P1ag | `analysis/upr-fvx-cfru-dpe-p1-item-data-and-bad-item-model` | Item-/Bad-Item-Modell fuer Encounter Held Items | erledigt; Diagnose 053 dokumentiert Item-ID-/Itemnamen-Scope, moderne Bad-/Key-Item-Risiken und Encounter-Held-Item-Folgefix |
| P1ah | `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write` | Encounter Held Items Scope-and-Write | erledigt; UPR-FVX `5c7170b6` und Diagnose 054 bestaetigen Save/Log/Reload ohne Encounter-Held-Item-Mismatches |
| P1ai | `analysis/upr-fvx-cfru-dpe-p1-type-log-placeholder-hygiene` | Type-Log-/Placeholder-Hygiene | erledigt; Diagnose 055 klassifiziert bestehende `Bad Egg`-/Unknown-/Fallback-/Null-Species-Marker read-only und trennt sie von Fix- und Text-/Name-Scope |
| P1aj | `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model` | Move-Data-Write-Modell | erledigt; Diagnose 056 dokumentiert 992-Move-Scope, `BattleMove.split`, Preserve-Policy und Reload-Kriterien |
| P1aj-fix | `compat/upr-fvx-cfru-dpe-move-data-write-preserve` | MoveData Write Preserve Fix | Review/Test; UPR-FVX `bb5ee119` implementiert klassischen MoveData-Write plus CFRU/DPE `BattleMove.split`-Write, Reload-Smoke noch offen |
| P1ak | `analysis/upr-fvx-cfru-dpe-p1-field-items-shops-pickup-model` | Field Items/Shops/Pickup-Modell | erledigt; Diagnose 057 trennt Field Items, Shops, Pickup und allgemeine Item-Randomization von Encounter Held Items |
| P1al | `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model` | Palette-Randomization-Modell | erledigt; Diagnose 058 trennt Palette-Safety von echter geaenderter Palette-Randomization und Graphics/Sprites |
| P1am | `analysis/upr-fvx-cfru-dpe-p1-type-chart-model` | Type-Chart-Modell | erledigt; Diagnose 059 trennt `gBaseStats`-Type-Read/Write aus 051 von Type-Chart-/Effectiveness-Randomization |
| P1an | `analysis/upr-fvx-cfru-dpe-p1-gui-suboptions-regression-matrix` | GUI-Suboptions-Regressionsmatrix | erledigt; Diagnose 060 konsolidiert konkrete FVX-GUI-Hauptoptionen und Suboptionen gegen den P1-Supportstand |
| P1ao | `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan` | P1 Regression-Smoke-Plan | erledigt; Diagnose 061 plant Smoke-Gruppen aus 060 und der FVX Feature-Coverage-Matrix ohne Testausfuehrung |
| P1ap | `analysis/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke` | Global Species Pool Regression-Smoke-Plan | erledigt; Diagnose 062 plant `FVX-GEN-001` und `FVX-GEN-002` gegen einen stabilen Species-Carrier ohne offene Writer und ohne Testausfuehrung |
| P1aq | `analysis/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke` | Starters Suboptions Regression-Smoke-Plan | erledigt; Diagnose 063 plant Starter-Poolfilter ueber `FVX-SST-002` ohne Starter Held Items und ohne offene Writer |
| P1ar | `test/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke` | Global Species Pool Regression-Smoke-Ergebnisse | erledigt; Diagnose 064 dokumentiert `FVX-GEN-001/002` im Starter-Carrier-Smoke als getestet, nicht global vollabgedeckt |
| P1as | `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke` | Starters Suboptions Regression-Smoke-Ergebnisse | erledigt; Diagnose 065 dokumentiert `FVX-SST-003/004/005/006/009` im Starter-Species-Writer-Smoke als getestet, Starter Held Items bleiben separat |
| P1at | `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness` | TypeChart Preserve Effectiveness Fix | erledigt; UPR-FVX `36707e01` und Diagnose 066 bestaetigen TypeEffectiveness Random mit Fairy-Reload und `writeReloadTypeChartMismatches=0` |
| P1au | `analysis/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes` | TypeEffectiveness-Folgesmoke-Plan | erledigt; Diagnose 067 plant einzelne Slices fuer Balanced, Keep Type Identities, Inverse, Add Random Immunities und Update Type Effectiveness ohne Ausfuehrung |
| P1av | `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes` | TypeEffectiveness-Folgesmoke-Ergebnisse | erledigt; Diagnose 068 bestaetigt alle geplanten TypeEffectiveness-Folgeslices ohne Codeaenderung |
| P1aw | `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke` | Similar Strength / Same Type Regression-Smoke-Plan | erledigt; Diagnose 069 plant Wild-, Trainer- und Evolution-Slices fuer BST-/Type-basierte Poolfilter ohne Testausfuehrung |
| P1ax | `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke` | Similar Strength / Same Type Regression-Smoke-Ergebnisse | erledigt; Diagnose 070 dokumentiert gemischte Ergebnisse und blockierte Folge-Slices |
| P1ay | `analysis/upr-fvx-cfru-dpe-p1-070-blocked-slices-followup-plan` | 070 Blocked Slices Follow-up Plan | erledigt; Diagnose 071 plant getrennte Folgeanalysen ohne Codeaenderung, Fix oder Randomizer-Laeufe |
| P1az | `analysis/upr-fvx-cfru-dpe-p1-wild-070-blockers-diagnostics` | Wild 070 Blockers Diagnostics Plan | erledigt; Diagnose 072 plant die gemeinsame Wild-Diagnose fuer `FVX-WILD-011` und `FVX-WILD-004` ohne Codeaenderung, Fix oder Randomizer-Laeufe |
| P1ba | `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-diagnostics` | Wild Filter Carrier Diagnostics Plan | erledigt; Diagnose 073 plant read-only Code-/Protokollanalyse und ggf. einen separaten Harness-Freigabeschritt fuer den Wild-Filter-Carrier |
| P1bb | `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-code-diagnosis` | Wild Filter Carrier Code Diagnosis | erledigt; Diagnose 074 grenzt die wahrscheinliche Ursache auf `GAME`-Mapping, `areaInformationMap` und Null-/unaufloesbare Encounter-Slots ein |
| P1bc | `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix` | Wild Filter Carrier Nullslot Fix | aktueller Fixbranch; UPR-FVX `acaada51` und Diagnose 075 bestaetigen `FVX-WILD-011` und `FVX-WILD-004` im `FVX-WILD-001` Carrier |
| P1bd | `analysis/upr-fvx-cfru-dpe-p1-trainer-type-diversity-blocker-diagnostics` | Trainer Type Diversity Blocker Diagnostics Plan | erledigt; Diagnose 076 plant die read-only Folge-Diagnose fuer `FVX-FOE-009` ohne Codeaenderung, Fix oder Randomizer-Laeufe |
| P1be | `analysis/upr-fvx-cfru-dpe-p1-trainer-type-diversity-code-diagnosis` | Trainer Type Diversity Code Diagnosis | erledigt; Diagnose 077 grenzt die wahrscheinliche Ursache auf Null-Primary-Type-Species im Force-Diverse-Types-/`EnumSet`-Pfad ein |
| P1bf | `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix` | Trainer Type Diversity Null-Type Fix | aktueller Fixbranch; UPR-FVX `d89fc64e` und Diagnose 078 bestaetigen `FVX-FOE-009` im `FVX-FOE-001` Carrier |
| P1bg | `analysis/upr-fvx-cfru-dpe-p1-evolution-same-typing-blocker-diagnostics` | Evolution Same Typing Code Diagnosis | erledigt; Diagnose 079 grenzt `FVX-TRAIT-019` auf Same-Typing-Null-Primary-Type-Kandidaten ein |
| P1bh | `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix` | Evolution Same Typing Null-Type Fix | Review/Test; UPR-FVX `74d88a7a` und Diagnose 080 bestaetigen `FVX-TRAIT-019` im `FVX-TRAIT-016` Carrier |
| P1bi | `analysis/upr-fvx-cfru-dpe-p1-evolution-similar-strength-mismatch-diagnostics` | Evolution Similar Strength Mismatch Diagnostics | erledigt; Diagnose 081 grenzt die 070-Mismatches wahrscheinlich auf Diagnosevergleich/Normalisierung statt harten Write-Fehler ein |
| P1bj | `test/upr-fvx-cfru-dpe-p1-evolution-similar-strength-normalized-reload` | Evolution Similar Strength Normalized Reload Diagnostics | aktueller Testbranch; Diagnose 082 bestaetigt `FVX-TRAIT-018` mit normalisiertem Evolution-Reload-Vergleich und `0` Mismatches |
| P2 | `randomizer/cfru-day-night-wild-table-analysis` | CFRU-Custom-Day/Night-Wild-Tabellen separat untersuchen | erst nach P1-Schreibpfad-Diagnose; Route-1-Fallback bleibt stabil |
| P3 | noch festlegen | Nullslot-`<unknown>` mit `rawInternalSpeciesId=0` klassifizieren | nicht mit GenRestrictions vermischen |
| P4 | noch festlegen | BizHawk-/Ironmon-Tracker-/RAM-Mapping pruefen | erst nach stabiler ROM-Randomizer-Kompatibilitaet |

## Aktuelle Sicherheitsregeln

- Keine ROMs in GitHub.
- Keine ROMs in ChatGPT hochladen.
- Keine Saves oder Emulator States committen.
- Keine Builds committen.
- Keine Tool-Binaries committen.
- Keine `.env`, Tokens, privaten Keys oder lokalen Secrets committen.
- Keine Änderungen direkt auf `main`.
- Externe Original-Upstreams nicht kontaktieren.
- Submodules sollen nur `origin` auf Planton361-Forks nutzen.
- PRs nur mit explizitem `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltem Planton361-Repository erstellen.
- Tool-Binaries bleiben in `03_tools/releases/` und damit lokal/ignored.
- ROMs bleiben in `04_private_roms/` und damit lokal/ignored.
- Build-Ergebnisse bleiben in `05_builds/` und damit lokal/ignored.
- Nicht parallel mehrere schreibende Agenten auf demselben Branch nutzen.

## Update-Regeln

Nach jeder Session aktualisieren:

1. `01_docs/SESSION_STATE.md`
2. `01_docs/NEXT_STEPS.md`
3. dieses Dokument, falls sich Roadmap-Status geändert hat
4. `01_docs/DECISIONS_INDEX.md`, falls Entscheidungen getroffen wurden
5. `01_docs/references/tool-manifest.md`, falls Tools, Repos, Branches oder Commits geändert wurden
6. `01_docs/references/source-index.md`, falls Quellen oder Quellenentscheidungen geändert wurden

Excel-Roadmap:

- Die Excel-Datei dient als visuelles Dashboard.
- Statusänderungen sollen zuerst in Markdown nachvollziehbar sein.
- Excel wird regelmäßig aus dem dokumentierten Status aktualisiert.
- Bei größeren Roadmap-Änderungen wird eine neue Excel-Version committed.

## Nächster empfohlener Branch

```text
test/upr-fvx-cfru-dpe-p1-evolution-similar-strength-normalized-reload
```

Zweck: Diagnose 082 reviewen und mergen; danach Evolution-Methoden-Writer und weitere Evolution-Suboptionen getrennt behandeln.

## Arbeitsblock-Log

### 2026-05-14 – analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke

- Neuer read-only Plan erstellt: `08_tests/randomizer/069_p1_similar_strength_same_type_regression_smoke.md`.
- Geplante Slices: `FVX-WILD-011` Wild Similar Strength, `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary, Trainer Similar Strength unter `FVX-FOE-001`, `FVX-FOE-009` Trainer Type Diversity / Type Themes, `FVX-TRAIT-018` Evolutions Similar Strength und `FVX-TRAIT-019` Evolutions Same Typing.
- Primaere Carrier sind `FVX-WILD-001` Standard/Fallback Wild, `FVX-FOE-001` Trainer Pokemon und `FVX-TRAIT-016` Evolution Randomization.
- Same Type, Type Themes und Type Restrictions nutzen Species-Type-Felder aus 051 und beweisen keinen TypeChart-Support.
- TypeChart/TypeEffectiveness, MoveData Write, Items, Palette, Graphics, Text/Menu, Level-Modifier, Evolution-Methoden-Writer, Starter Held Items und weitere offene Writer bleiben ausgeschlossen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe.

### 2026-05-14 – test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes

- Neuer Ergebnisbericht erstellt: `08_tests/randomizer/068_type_effectiveness_followup_smoke_results.md`.
- Einzelne TypeEffectiveness-Folgesmokes ausgefuehrt: `FVX-TYPE-001` Balanced, Keep Type Identities und Inverse, `FVX-TYPE-002` Add Random Immunities sowie `FVX-TYPE-003` Update Type Effectiveness.
- Alle fuenf Slices melden Save/Log/Output/Reload true, `writeReloadTypeChartMismatches=0`, erhaltene Foresight-/Endtable-Terminatoren, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`.
- Unsupported/Stellar wurde nicht eingefuehrt oder still normalisiert; Balanced reloadete Fairy-Rohtriplets als raw `0x17`, die anderen Folgeslices erzeugten keine Fairy-Rohtriplets und kein Fehlmapping.
- Keine Codeaenderung, keine Aenderung an `02_external/**`; lokale Artefakte blieben ignored.

### 2026-05-14 – analysis/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes

- Neuer read-only Plan erstellt: `08_tests/randomizer/067_type_effectiveness_followup_smoke_plan.md`.
- Geplante einzelne Folgesmoke-Slices: `FVX-TYPE-001` Balanced, Keep Type Identities und Inverse, `FVX-TYPE-002` Add Random Immunities sowie `FVX-TYPE-003` Update Type Effectiveness.
- Der TypeEffectiveness-only Random-Smoke aus 066 bleibt Referenz, ersetzt aber die Einzelpruefung dieser GUI-Modi nicht.
- Gemeinsame spaetere Erfolgskriterien dokumentiert: Save/Log/Output/Reload true, `writeReloadTypeChartMismatches=0`, Fairy raw `0x17`, unsupported/Stellar-Preserve, erhaltene Terminatoren, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe.

### 2026-05-14 – compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness

- UPR-FVX-Branch `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness` verwendet; keine Aenderung direkt auf `main`/`master`.
- UPR-FVX-Fix `36707e0190d3d9fa587550dfc5631fcaa9abd6b1` erstellt.
- TypeChart-raw-Type-Mapping wurde vom `gBaseStats`-Type-Mapping getrennt: Fairy `0x17` wird fuer TypeEffectiveness gelesen/geschrieben, Stellar/raw `0x18` bleibt unsupported.
- Unsupported raw TypeChart-Triplets bleiben preserve-/skip-only; kein STELLAR-Enum, keine Species-Type-, MoveData-, Palette-, Item-, Graphics- oder Text/Menu-Aenderung.
- TypeEffectiveness-only Smoke bestaetigt `saveSuccessful=true`, `logSuccessful=true`, Output-ROM und nichtleeren Log, Reload, `writeReloadTypeChartMismatches=0`, Fairy-Reload als raw `0x17`, erhaltene Terminatoren und `stacktrace=none`.
- Neues Protokoll erstellt: `08_tests/randomizer/066_type_chart_preserve_effectiveness_fix_diagnostics.md`.

### 2026-05-13 – analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model

- UPR-FVX PR #19 und Workspace PR #73 als gemerged geprueft.
- Analysebranch `analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model` erstellt; keine Aenderungen an `02_external/**`.
- CFRU/DPE-128-Slot-TM/HM-Modell read-only dokumentiert.
- `gTMHMMoves` ist `u16[128]` ueber Pointer `0x8125A8C`; Slots `1..120` sind TMs, Slots `121..128` sind HMs.
- `gTMHMLearnsets` ist 128-Bit-/16-Byte-Compatibility pro Species ueber Pointer `0x8043C68`.
- FVX-`50+8`-Pfad bleibt P1-supported, bildet aber das 128-Slot-Modell nicht ab.
- Neues Protokoll erstellt: `08_tests/randomizer/037_p1_tm_hm_128_slot_model.md`.

### 2026-05-13 – compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety

- Workspace PR #72 als gemerged geprueft.
- UPR-FVX-Fix `32e43ac03a5762542773213a13be4e0389f1deae` erstellt.
- TM-Move-Randomization fuer CFRU/DPE gegen Move-IDs oberhalb der vorhandenen FVX-Sicherheitslisten abgesichert.
- TM/HM-Compatibility fuer CFRU/DPE gegen Placeholder-Species, `null`-Typen und ungueltige Move-/Flag-Indizes abgesichert.
- Diagnose 036 bestaetigt TM moves + Compatibility, Compatibility-only und TM moves-only mit `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleerem Log und `writeReloadMismatches=0`.
- `50+8`-TM/HM-Scope ist P1-supported; CFRU/DPE-128-Slot-TM/HM bleibt separates Folgerisiko.

### 2026-05-13 – analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations

- UPR-FVX PR #17 und Workspace PR #68 als gemerged geprueft.
- Analysebranch `analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations` erstellt; keine Aenderungen an `02_external/**`.
- Vier Kombinationsdiagnosen mit Seed `274269061345323` ausgefuehrt.
- Movesets-only, Movesets+Species, Movesets+Held Items normal und Movesets+sensible Held Items melden jeweils `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleeren Trainer-Log und `writeReloadMoveMismatches=0`.
- Movesets+Species bestaetigt Gen8/9-Trainer-Pokemon nach Reload: `gen8plusSpecies=77`, `gen9Species=38`.
- Normale und sensible Trainer-Held-Item-Kombinationen schreiben `heldItemEntries=481` und reloaden ohne Held-Item-Mismatches.
- Kein `Bad Egg`, kein `<unknown>`, keine Unknown-Move-Marker und keine invaliden Move-IDs im Trainerbestand.
- Neues Protokoll erstellt: `08_tests/randomizer/032_p1_trainer_movesets_combinations.md`.

### 2026-05-12 – analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-only

- UPR-FVX PR #16 und Workspace PR #65 als gemerged geprueft.
- Analysebranch `analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-only` erstellt; keine Aenderungen an `02_external/**`.
- UPR-FVX read-only geprueft und gebaut: Submodule steht auf `3864ad0e7efda4ed8a329fb22edb3a28db1040e8`; `./gradlew clean :random:jar` erfolgreich.
- Trainer Movesets-only Diagnose mit Seed `274269061345323` ausgefuehrt.
- Befund: Trainer-Load `trainers=255`, `trainerPokemon=481`, `nullSpecies=0`; bestehende Movesets haben `before.invalidMoves=0`.
- Der Lauf blockiert vor Save/Log in `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel()` durch `Gen3RomHandler.getMovesLearnt()` bei `No valid pointer at 0x25e49c`.
- Keine Output-ROM und kein nichtleerer Trainer-Log entstehen; Write/Reload bleibt fuer einen spaeteren Learnset-/Moveset-Fixblock offen.
- Neues Protokoll erstellt: `08_tests/randomizer/030_p1_learnsets_model.md`.
- Keine Codeaenderungen, keine Fixes, keine committed ROM-/Build-Artefakte.

### 2026-05-12 – compat/upr-fvx-cfru-dpe-trainer-held-items-lazy-movesets

- Workspace PR #64 als gemerged geprueft und Branch `compat/upr-fvx-cfru-dpe-trainer-held-items-lazy-movesets` erstellt.
- UPR-FVX-Branch vom gepinnten `18766c4986db091d1e669c71302aa295195b039b`-Stand erstellt.
- Minimaler UPR-FVX-Fix umgesetzt: `randomizeTrainerHeldItems()` laedt `getMovesLearnt()` nicht mehr eager fuer normale Held-Items-only-Laeufe; Moveset-Kontext bleibt auf sensible movebasierte Itemauswahl begrenzt.
- UPR-FVX-Commit erstellt: `3864ad0e7efda4ed8a329fb22edb3a28db1040e8`.
- Diagnose mit Seed `274269061345323`: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM und nichtleerer Trainer-Log entstehen.
- Held Items werden fuer alle `481` Trainer-Pokemon geschrieben und nach Reload erhalten.
- Trainer-Log enthaelt kein `Bad Egg` und kein `<unknown>`; Reload-Vergleich meldet `writeReloadMismatches=0`.
- Neues Protokoll erstellt: `08_tests/randomizer/028_trainer_held_items_lazy_movesets_diagnostics.md`.

### 2026-05-12 – analysis/upr-fvx-cfru-dpe-p1-trainer-held-items-only

- UPR-FVX PR #15 und Workspace PR #63 als gemerged geprueft.
- Analysebranch `analysis/upr-fvx-cfru-dpe-p1-trainer-held-items-only` verwendet; keine Aenderungen an `02_external/**`.
- UPR-FVX read-only geprueft und gebaut: Submodule steht auf `18766c4986db091d1e669c71302aa295195b039b`; `./gradlew clean :random:jar` erfolgreich.
- Trainer Held Items-only Diagnose mit Seed `274269061345323` ausgefuehrt.
- Befund: Trainer-Held-Item-Pool `52`, Trainer-Load `trainers=255`, `trainerPokemon=481`, `nullSpecies=0`.
- Der Lauf blockiert vor Save/Log in `TrainerPokemonRandomizer.randomizeTrainerHeldItems()` durch eager `Gen3RomHandler.getMovesLearnt()` bei `No valid pointer at 0x25e49c`.
- Keine Output-ROM und kein nichtleerer Trainer-Log entstehen; Write/Reload bleibt fuer den naechsten Fix-/Diagnoseblock offen.
- Neues Protokoll erstellt: `08_tests/randomizer/027_p1_trainer_held_items_only.md`.
- Keine Codeaenderungen, keine Fixes, keine committed ROM-/Build-Artefakte.

### 2026-05-12 – compat/upr-fvx-cfru-dpe-evolutions-scope-and-write

- Workspace auf PR #61-Stand aktualisiert und Branch `compat/upr-fvx-cfru-dpe-evolutions-scope-and-write` erstellt.
- UPR-FVX-Branch vom gepinnten `56ec749eca12a8637c20f943b520a9bb6a9d469a`-Stand erstellt.
- Minimaler UPR-FVX-Fix umgesetzt: Evolution-Source- und Ziel-Species schreiben/lesen fuer erweiterte BPRE-Hacks ueber interne SpeciesSet-Identitaet; Evolution-Logger faellt bei nicht aufloesbaren ExtraInfos defensiv auf numerische Marker zurueck.
- UPR-FVX-Commit erstellt: `18766c4986db091d1e669c71302aa295195b039b`.
- Diagnose mit Seed `274269061345323`: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM und nichtleerer Evolution-Log entstehen.
- Evolution-Log enthaelt Gen7/8/9-Picks; zwei Logger-Fallbacks fuer `unknown item #1732` blockieren den Log nicht.
- Reload-Vergleich meldet `writeReloadMismatches=0`; Gen8/9-Ziele bleiben erhalten.
- Neues Protokoll erstellt: `08_tests/randomizer/026_evolutions_scope_write_diagnostics.md`.

### 2026-05-12 – analysis/upr-fvx-cfru-dpe-p1-evolutions-species-only

- UPR-FVX PR #14 und Workspace PR #60 als gemerged geprueft; `main` per Fast-Forward aktualisiert.
- Analysebranch `analysis/upr-fvx-cfru-dpe-p1-evolutions-species-only` erstellt.
- UPR-FVX read-only geprueft und gebaut: Submodule steht auf Planton361-Fork-Commit `56ec749eca12a8637c20f943b520a9bb6a9d469a`; `./gradlew clean :random:jar` erfolgreich.
- Evolution-Species-only Diagnose mit Seed `274269061345323` ausgefuehrt.
- Befund: `PokemonCount=1439`, `speciesList.size=1415`, Evolution-Pool `1414` mit Gen1-Gen9.
- Evolution-Picks erreichen Gen7/8/9: `after.pickedGen7plus=43`, `after.toGenerationCounts={1=35, 2=16, 3=24, 4=30, 5=20, 6=22, 7=18, 8=13, 9=12}`.
- Save gelingt und Output-ROM entsteht; CLI-Log ist nicht leer, Direct Results meldet aber `logSuccessful=false` in `RandomizationLogger.evolutionMethodToString()`.
- Write/Reload bleibt blockiert: Reload verliert Evolution-Eintraege und Gen8/9-Ziele; `writeReloadMismatches=146`.
- Neues Protokoll erstellt: `08_tests/randomizer/025_p1_evolutions_species_only.md`.
- Keine Codeaenderungen, keine Fixes, keine committed ROM-/Build-Artefakte.

### 2026-05-12 – compat/upr-fvx-cfru-dpe-trainer-scope-and-write

- Workspace auf PR #59-Stand aktualisiert und Branch `compat/upr-fvx-cfru-dpe-trainer-scope-and-write` erstellt.
- UPR-FVX-Branch vom gepinnten `009178e8848b4272e6b8be54a8bf5b2bed34d5f2`-Stand erstellt.
- Minimaler UPR-FVX-Fix umgesetzt: nicht kampffaehige CFRU/DPE-Sonder-Species werden aus dem Trainer-Replacement-Pool entfernt; `getRandomAbilitySlot()` ist gegen Zero-Ability-Species defensiv; echte Trainer-Species schreiben fuer erweiterte BPRE-Hacks interne SpeciesSet-Identitaet.
- UPR-FVX-Commit erstellt: `56ec749eca12a8637c20f943b520a9bb6a9d469a`; PR #14 erstellt.
- Diagnose mit Seed `274269061345323`: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM und nichtleerer Trainer-Log entstehen.
- Trainer-Log enthaelt Gen7/8/9-Picks; Reload-Vergleich meldet `writeReloadMismatches=0`.
- Neues Protokoll erstellt: `08_tests/randomizer/024_trainer_scope_write_diagnostics.md`.

### 2026-05-12 – analysis/upr-fvx-cfru-dpe-p1-trainer-species-only

- UPR-FVX PR #13 und Workspace PR #58 als gemerged geprueft; `main` per Fast-Forward aktualisiert.
- Analysebranch `analysis/upr-fvx-cfru-dpe-p1-trainer-species-only` erstellt.
- UPR-FVX read-only geprueft und gebaut: Submodule steht auf Planton361-Fork-Commit `009178e8848b4272e6b8be54a8bf5b2bed34d5f2`; `./gradlew clean :random:jar` erfolgreich.
- Trainer-Species-only Diagnose mit Seed `274269061345323` ausgefuehrt.
- Befund: `PokemonCount=1439`, `speciesList.size=1415`, Trainer-Pool `1414` mit Gen1-Gen9.
- Trainer-Load funktioniert: `trainers=255`, `trainerPokemon=481`, `nullSpecies=0`.
- Pool-Sonderfaelle: acht Zero-Ability-/Zero-BST-Species, darunter `Bad Egg`, zwei Zygarde-Sonderslots und vier Gen9-Ogerpon-Formslots.
- `randomizeTrainerPokes()` blockiert vor Save/Log; Stack-Dump zeigt `TrainerPokemonRandomizer.getRandomAbilitySlot()` als laufenden Pfad.
- Keine Output-ROM und kein Trainer-Log entstehen; Write/Reload bleibt fuer den naechsten Fix-/Diagnoseblock offen.
- Neues Protokoll erstellt: `08_tests/randomizer/023_p1_trainer_species_only.md`.
- Keine Codeaenderungen, keine Fixes, keine committed ROM-/Build-Artefakte.

### 2026-05-12 – compat/upr-fvx-cfru-dpe-static-gift-scope-and-write

- Workspace auf PR #57-Stand aktualisiert und Branch `compat/upr-fvx-cfru-dpe-static-gift-scope-and-write` erstellt.
- UPR-FVX-Branch vom gepinnten `0f127e9b`-Stand erstellt.
- Minimaler UPR-FVX-Fix umgesetzt: Null-Static-Species werden nicht randomisiert und blockieren den Save nicht; echte Static/Gift-Species schreiben fuer erweiterte BPRE-Hacks interne SpeciesSet-Identitaet.
- UPR-FVX-Commit erstellt: `009178e8848b4272e6b8be54a8bf5b2bed34d5f2`; PR #13 erstellt.
- Diagnose mit Seed `274269061345323`: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM und nichtleerer Static/Gift-Log entstehen.
- Static/Gift-Log enthaelt Gen7/8/9-Picks; Reload-Vergleich meldet `writeReloadMismatches=0`.
- Neues Protokoll erstellt: `08_tests/randomizer/022_static_gift_scope_write_diagnostics.md`.

### 2026-05-12 – analysis/upr-fvx-cfru-dpe-p1-static-gift-species-only

- PR #56 als gemerged geprueft und `main` per Fast-Forward aktualisiert.
- Analysebranch auf den gepinnten UPR-FVX-Stand `0f127e9b` gebracht.
- UPR-FVX read-only geprueft und gebaut: `./gradlew clean :random:jar` erfolgreich.
- Static/Gift-only Diagnose mit Seed `274269061345323` ausgefuehrt.
- Befund: `PokemonCount=1439`, `speciesList.size=1415`, Static/Gift-Pool `1414` mit Gen1-Gen9.
- Pick-Pfad erreicht Gen7/8/9: `pickedGen4plus=18`, `pickedGen7plus=8`.
- Echter Save/Log blockiert: CLI meldet Erfolg, aber `GameRandomizer.Results.wasSaveSuccessful=false`, Log ist leer und keine Output-ROM entsteht.
- Ursache im Diagnosebefund: vier `<null>`-Static-Eintraege im Static/Roamer-/hardcoded-FRLG-Scope.
- Neues Protokoll erstellt: `08_tests/randomizer/021_p1_static_gift_species_only.md`.
- Keine Codeaenderungen, keine Fixes, keine committed ROM-/Build-Artefakte.

### 2026-05-11 – setup/workspace-build-randomizer-smoke

- UPR-FVX, DPE Gen9 und CFRU-expansion als Submodule auf Planton361-Forks dokumentiert.
- DPE Gen9 und CFRU auf DPE bauten lokal erfolgreich.
- UPR-FVX konnte die CFRU/DPE-ROM laden, minimal randomisieren und speichern.
- BizHawk bootete die randomisierte ROM.
- Vanilla-/Fallback-Wild-Encounter-Randomization funktionierte; Route 22 und Viridian Forest zeigten randomisierte Encounters.
- Der Wild-Log zeigte weiterhin nur Gen1-3 bzw. `<unknown>`; Species-Pool-Analyse wurde als naechster Fokus identifiziert.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien wurden committed.

### 2026-05-11 – randomizer/route-1-fallback-wild-randomizer-check

- CFRU Route-1-Custom-Day/Night-Wild-Tabelle fuer den Randomizer-Kompatibilitaetsbuild per `FIRERED_GEN9_ENABLE_ROUTE1_CUSTOM_WILD 0` deaktiviert.
- FVX-Log erkannte Route 1 wieder als `Area #3 - ROUTE 1 Grass/Cave`.
- Route 1 zeigte im Log randomisierte Encounters wie Geodude und Abra.
- Gen4-Gen9-Species-Pool und `<unknown>` blieben separat offen.

### 2026-05-11 – analysis/upr-fvx-cfru-dpe-species-pool

- Branch `analysis/upr-fvx-cfru-dpe-species-pool` von `main`-Merge-Commit `5c2cc1eda7e600db461e56eac2eba2c31a575fcc` erstellt.
- UPR-FVX-Codepfade read-only analysiert: `Gen3RomHandler`, `RestrictedSpeciesService`, `SpeciesSet`, `Species`, `SpeciesIDs`, `Gen3Constants`, `WildEncounterRandomizer`, `Randomizer`.
- Ergebnis: `Gen3RomHandler` erkennt DPE-Species nicht ueber DPE-Metadaten, sondern ueber BPRE-Hack-Heuristiken; `generationOf()` ist auf Gen1-3 hardcoded; der Wild-Pool kommt ueber `RestrictedSpeciesService` und `romHandler.getSpeciesSetInclFormes()`.
- `<unknown>` im Wild-Log ist wahrscheinlich ein Null-/Fallback fuer nicht aufgeloeste Encounter-Species, verursacht durch Count-/ID-/Mapping-Probleme.
- Analyseprotokoll erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-species-pool-analysis.md`.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien wurden angefasst.

### 2026-05-11 – analysis/log-cfru-dpe-species-diagnostics

- UPR-FVX PR #2 auf Branch `analysis/log-cfru-dpe-species-diagnostics` lokal reviewt.
- PR #2 enthaelt nur temporaere Diagnoseausgaben in `Gen3RomHandler.java` und `RandomizationLogger.java`.
- UPR-FVX per Clean-Build neu gebaut und lokalen CFRU/DPE-Route-1-Fallback-Teststand per CLI geladen/randomisiert.
- Diagnosebefund dokumentiert: `PokemonCount=823`, `pokedexCount=386`, `speciesList.size=412`, `maxInternalSpeciesId=823`, `maxSpeciesNumber=411`, `generationCounts={1=328, 2=200, 3=295}`.
- Beispiel-Species ueber 386 werden als Gen3 klassifiziert; eindeutige Wild-Log-`<unknown>`-Rohwerte sind `rawInternalSpeciesId=0`.
- Neues Protokoll erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-species-diagnostics-run.md`.
- Keine ROMs, Builds, Randomizer-JARs, Saves oder Tool-Binaries wurden committed.

### 2026-05-11 – analysis/cfru-dpe-upr-fvx-compatibility-model

- Workspace PR #28 und UPR-FVX PR #3 als gemerged geprueft.
- CFRU/DPE- und UPR-FVX-Codepfade read-only als Kompatibilitaetsmodell zusammengefuehrt.
- Neues Modell erstellt: `01_docs/compat/cfru-dpe-upr-fvx-compatibility-model.md`.
- Ergebnis: RAM-Mapping ist noch nicht noetig; zuerst P0 GenRestrictions/finaler Gen4+-Wild-Pool, danach P1 Trainer/Starters/Evolutions/Learnsets, P2 CFRU Day/Night Wild, P3 Nullslot-`<unknown>`, P4 Ironmon/BizHawk/RAM-Mapping.
- Keine Codeaenderungen, keine Builds und keine ROM-Zugriffe.

### 2026-05-11 – analysis/randomizer-natdex-reference-sources

- Workspace `main` aktualisiert und Branch `analysis/randomizer-natdex-reference-sources` erstellt.
- Neue Referenz-Submodules read-only inventarisiert: UPR-FVX, UPR-FVX upstream, Ajarmar UPR-ZX, CyanSMP64 UPR-ZX NatDex, CyanSMP64 FireRed NatDex, pret FireRed, CFRU-expansion und DPE Gen9.
- Neues Quelleninventar erstellt: `01_docs/compat/randomizer-natdex-reference-sources.md`.
- Neues Workflowmodell erstellt: `01_docs/compat/randomizer-workflow-model.md`.
- Neue Implementierungsnotizen erstellt: `01_docs/compat/natdex-reference-implementation-notes.md`.
- Ergebnis: CyanSMP64 UPR-ZX NatDex ist eine wichtige Gen8/Gen9-Restriction-Referenz; fuer den lokalen CFRU/DPE-Teststand bleibt DPE/CFRU Source-of-Truth fuer interne Species-IDs.
- Keine Codeaenderungen, keine Builds, keine ROM-Zugriffe und keine Aenderungen in `02_external/**`.

### 2026-05-11 – analysis/cfru-documentation-randomizer-relevance

- Workspace `main` aktualisiert und Branch `analysis/cfru-documentation-randomizer-relevance` erstellt.
- `02_external/CFRU-expansion/CFRU Documentation.pdf` read-only ausgewertet.
- Neues Referenzdokument erstellt: `01_docs/compat/cfru-documentation-randomizer-relevance.md`.
- Bestehendes Kompatibilitaetsmodell um den CFRU-Doku-Querverweis ergaenzt.
- Ergebnis: CFRU-Runtime-Randomizer-Flags, Day/Night-Wild, Swarms, Roamers, Hidden Ability, Trainer-EV-Spreads, TM/Tutor/Learnsets und Save/RAM bleiben getrennte P1/P2/P4-Themen; P0 bleibt nur GenRestrictions/finaler Gen4+-Wild-Pool.
- Keine Codeaenderungen, keine Builds, keine ROM-Zugriffe und keine Aenderungen in `02_external/**`.

### 2026-05-11 – analysis/upr-fvx-cfru-dpe-gen-restrictions

- UPR-FVX Branch `compat/upr-fvx-cfru-dpe-gen-restrictions` von `compat/firered-gen9-cfru-dpe` erstellt.
- P0-Fix umgesetzt: erweiterte CFRU/DPE-BPRE-Hacks werden in `Settings.tweakForRom()` nicht mehr blind auf Gen3 gekappt; `GameRandomizer.setupSpeciesRestrictions()` nutzt bei `limitPokemon=false` `setRestrictions(null)`.
- UPR-FVX Commit `61a15e521811c5181025e216b3acc27340a495de` erstellt und PR #4 geoeffnet.
- Diagnose: finaler `RestrictedSpeciesService`-Pool enthaelt bei `limitPokemon=false` Gen4+-Species (`gen4plus=381`).
- Sichtbarer Wild-Log bleibt Gen1-3: Gen1 `841`, Gen2 `527`, Gen3 `791`, Gen4+ `0`, `<unknown>` `17`.
- Interpretation: P0-GenRestrictions ist geloest; naechster Engpass ist wahrscheinlich der Gen3/CFRU-DPE-Wild-Write-/Reload-Pfad ueber `pokedexToInternal[Species.number]`.
- Keine Day/Night-Wildtable-, Nullslot-, SpeciesSet-Identity-, Trainer-, Starter-, Evolution-, Learnset-, TM- oder Tutor-Fixes umgesetzt.

### 2026-05-11 – analysis/upr-fvx-cfru-dpe-wild-internal-species-write

- UPR-FVX Branch `compat/upr-fvx-cfru-dpe-wild-internal-species-write` von `compat/firered-gen9-cfru-dpe` erstellt.
- Basis enthaelt PR #4 als Merge-Commit `03b42a1216f5a087d42a3e94a7e81a15db2e977b`.
- Minimaler Wild-Write-Fix umgesetzt: erweiterte CFRU/DPE-BPRE-Hacks schreiben Vanilla/Fallback-Wild-Species ueber `speciesSetIdentityNumber`; Vanilla und normale Gen3-Hacks bleiben auf `pokedexToInternal[Species.number]`.
- UPR-FVX Commit `5f68ec0fc8e1592079486f6d22cf5a122eb08d01` erstellt und PR #5 geoeffnet.
- Diagnose: sichtbarer Wild-Log enthaelt jetzt Gen4+-Species: Gen1 `354`, Gen2 `388`, Gen3 `404`, Gen4 `398`, Gen5 `528`, Gen6 `104`, `<unknown>` `0`.
- Route 1, Route 22 und Viridian Forest wirken weiterhin sichtbar randomisiert.
- Keine Settings-/GenRestrictions-, Day/Night-Wildtable-, Nullslot-, SpeciesSet-Identity-, Trainer-, Starter-, Evolution-, Learnset-, TM- oder Tutor-Fixes umgesetzt.

### 2026-05-11 – analysis/upr-fvx-cfru-dpe-p0-post-merge-smoke

- UPR-FVX PR #5 ist gemerged; Submodule steht auf `compat/firered-gen9-cfru-dpe` bei Merge-Commit `843b75a8f1016fa41a1879408fbeca45de7e030a`.
- UPR-FVX per `./gradlew clean :random:jar` erfolgreich gebaut.
- Derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand wurde mit Wild-Randomization, `limitPokemon=false` und ohne Gen1-3-Einschraenkung randomisiert.
- Diagnose bleibt stabil: `PokemonCount=823`, `speciesList.size=799`, `maxSpeciesIdentityNumber=823`.
- Sichtbarer Wild-Log bestaetigt die P0-Kette: Gen1 `354`, Gen2 `388`, Gen3 `404`, Gen4 `398`, Gen5 `528`, Gen6 `104`, `<unknown>` `0`.
- Keine Codeaenderungen, keine neuen Fixes, keine ROMs/Builds/Tool-Binaries committed.

### 2026-05-12 – analysis/upr-fvx-cfru-dpe-p1-encounter-systems

- Workspace PR #36 als gemerged geprueft; UPR-FVX-Submodule steht weiter auf `843b75a8`.
- UPR-FVX-, CFRU/DPE- und Referenzpfade read-only analysiert.
- Neues Modell erstellt: `01_docs/compat/cfru-dpe-encounter-systems-model.md`.
- Ergebnis: P0-supported sind Standard-Wild/Grass-Cave, Surfing, Fishing und Rock Smash aus `gWildMonHeaders`.
- CFRU Time-of-Day-Wild, Swarms, Roamers, DexNav, Wild Double Battles, Raids, Altering Cave und Tanoby/Unown sind partial oder unsupported und bleiben getrennte Folgearbeit.
- Empfehlung: naechster Diagnoseblock zuerst P1-Species-Schreibpfade, nicht Day/Night-Fix.
- Keine Codeaenderungen, keine Builds und keine ROM-Zugriffe.

### 2026-05-12 – analysis/upr-fvx-cfru-dpe-gen9-wild-post-merge-smoke

- Workspace PR #51 als gemerged geprueft und Branch `analysis/upr-fvx-cfru-dpe-gen9-wild-post-merge-smoke` erstellt.
- UPR-FVX `compat/firered-gen9-cfru-dpe` auf Merge-Commit `ee82cb4e` aktualisiert; Submodule-Pointer im Workspace wurde nachgezogen.
- UPR-FVX per `./gradlew clean :random:jar` erfolgreich gebaut.
- Lokaler CFRU/DPE-Wild-only-Smoke beendet mit CLI-Exit-Code `0` und `Randomized successfully!`.
- Diagnose bleibt stabil: `PokemonCount=1439`, `speciesList.size=1415`, `maxSpeciesIdentityNumber=1439`, `generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}`.
- Wild-Log enthaelt Gen7 `85`, Gen8 `126`, Gen9 `289`; `<unknown>` bleibt `0`.
- `Bad Egg` erscheint `12` Mal und bleibt als separate Folgeauffaelligkeit offen.
- Keine Codeaenderungen, keine neuen Fixes, keine ROMs/Builds/Tool-Binaries committed.

### 2026-05-13 – compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets

- Branch `compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets` fuer Workspace und UPR-FVX verwendet.
- Minimaler UPR-FVX-Fix erstellt: CFRU/DPE-Level-Up-Learnsets fuer Trainer Movesets-only defensiv lesen; Learnset-Write bleibt unveraendert.
- UPR-FVX-Commit erstellt: `655764816f9fefedb9433f33e4da0bc9d44bcda7`.
- Diagnose 031 bestaetigt `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleeren Trainer-Log und `writeReloadMismatches=0`.
- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` committed oder dokumentiert.

## 2026-05-13 - Egg-Move P1 scope

- CFRU/DPE Gen9 BPRE Egg-Move reader/writer is now implemented in UPR-FVX on branch `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write` at `18168b78b973a4c39f34053ac58f21279a26d8d2`.
- Diagnosis 042 reports Egg-Move direct scope as P1-supported for the tested ROM: Save/Log/Output succeed and Write/Reload mismatches are `0`.
- Learnset-Write, Move-Data-Write, Special Tutors, and Tutor text remain separate roadmap items.

## 2026-05-13 - Learnset-Write model

- CFRU/DPE Gen9 BPRE Learnset-Write model documented in `08_tests/randomizer/043_p1_learnset_write_model.md`.
- `gLevelUpLearnsets` should be treated as an internal Species-ID pointertable via pointer location `0x03EA7C` / `0x0803EA7C`; entries are `u16 move + u8 level` with `{0, 0xFF}` sentinel.
- Recommended next status: bounded in-place CFRU/DPE `setMovesLearnt()` fix branch; full repointing remains out of scope.

## 2026-05-14 - Diagnose 096 Palette Normal Single-owner Reload-Smoke blockiert

- `FVX-GFX-001` hat den UPR-FVX Write-Guard-Fix aus Diagnose 095, aber der Reload-Smoke 096 ist lokal blockiert.
- Preflight: `candidateFilesChecked=94`, `candidateLoaded=false`, `candidateOpenFailures=2`, `candidateSpeciesTotalMismatches=92`.
- Keine Hochstufung auf `Getestet` oder `GUI-kompatibel`.
- Nächster konservativer Block: `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke-retry` mit explizit freigegebenem UPR-FVX-ladbarem `candidateSpeciesTotal=1439` Kandidaten.

## 2026-05-14 - Post-Merge Sync Palette Normal Single-owner Smoke blockiert

- Workspace PR #140 ist gemerged; Diagnose 096 ist als blockierter Reload-Smoke abgeschlossen.
- Palette Normal-only Guard ist in UPR-FVX `2697511da9a97df4c29c00dfda8b40e556020489` implementiert, aber nicht per fachlichem Reload-Smoke bestaetigt.
- Blockerwerte: `candidateFilesChecked=94`, `candidateLoaded=false`, `candidateOpenFailures=2`, `candidateSpeciesTotalMismatches=92`, `candidateSpeciesTotal=0`.
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert` und nicht GUI-kompatibel.
- Naechster P1-Analyseblock: `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan`.

## 2026-05-14 - Diagnose 097 Field Items / Shops / Pickup Scope Plan

- Diagnose 097 plant den naechsten Item-P1-Scope read-only.
- Ergebnis: Field Items, Shops und Pickup nicht gemeinsam fixen; unterschiedliche Writer-Risiken.
- Field Items: Map-/Script-/Hidden-Item-Offset-Writer mit TM-/Required-/Progression-Policy.
- Pickup: eigener Table-/Locator-/Probability-Scope.
- Shops: eigener Shoplisten-/Terminator-/DataRewriter-/Repointing-/Preis-Scope.
- Naechster Block: `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`.

## 2026-05-14 - Field Items diagnostics scope plan

- Added `08_tests/randomizer/098_field_items_scope_diagnostics_plan.md`.
- Field Items are now the next dedicated P1 item-writer diagnostic track after the combined Field Items / Shops / Pickup scope plan.
- Shops and Pickup remain separate follow-up tracks.
- No code, submodule, build, Randomizer, ROM, log or private artefact changes.

## 2026-05-14 - Field Items diagnostics blocked

- Added `08_tests/randomizer/099_field_items_scope_diagnostics.md`.
- Workspace PR #143 was verified as merged before starting this branch.
- Field-Items-only diagnostics are blocked because no explicitly approved local CFRU/DPE Gen9-BPRE candidate was provided in this block.
- Sanitized preflight: `candidateFilesChecked=0`, `candidateLoaded=false`, `fieldItemScanSuccessful=false`, `exceptionClass=none`, `stacktrace=none`.
- `FVX-ITEM-001..004` remain `Write modelliert`; no Field-Item fix or smoke evidence was produced.
- No code, submodule, build, Randomizer, ROM, log, output ROM or private artefact changes.

## 2026-05-14 - Field Items candidate diagnostics

- Added `08_tests/randomizer/100_field_items_scope_diagnostics_candidate.md`.
- Workspace PR #144 was verified as merged before branch creation.
- A locally approved CFRU/DPE Gen9-BPRE candidate was scanned read-only for Field Items only.
- Sanitized result: `candidateLoaded=true`, `fieldItemScanSuccessful=true`, `fieldItemsTotal=339`, `visibleFieldItemSlots=168`, `hiddenFieldItemSlots=171`, `allowedFieldItemSlots=280`, `disallowedFieldItemSlots=59`, `tmFieldItemSlots=28`, `nonTmFieldItemSlots=311`, `requiredFieldTMMissing=0`, `invalidFieldItemIds=0`, `unloadedFieldItemIds=0`, `scriptPatternUnmatchedItemBalls=10`.
- `FVX-ITEM-001..004` remain `Write modelliert`; next step is a guarded Field-Items write/smoke branch.
- No code, submodule, build, Randomizer write/save, ROM output, log or private artefact changes.

## 2026-05-15 - Field Items Random Even Ban Bad Reload-Smoke

- Diagnose 113 bestaetigt `FVX-ITEM-003 Field Items Random even distribution` mit `banBadRandomFieldItems=true` im engen Field-Items-only Scope.
- Save/log/output/reload sind true; `fieldItemReloadMismatches=0`, sichtbare/Hidden-Mismatches `0`, TM-/Non-TM-Slot-Mismatches `0`, `requiredFieldTMMissingAfter=0`.
- Ban Bad bleibt stabil: `badFieldItemWrites=0`; der fachliche Kandidat meldet `badFieldItemPoolCandidates=47` und `badFieldItemPoolExcluded=47`.
- Random-Even-Queue-/Verteilungsstabilitaet ist belegt: `randomEvenQueueUsed=true`, `randomEvenTmDistributionStable=true`, `randomEvenNonTmDistributionStable=true`, `nonBadFieldItemQueueRefills=0`.
- `FVX-ITEM-001..004` sind fuer Field Items im getesteten engen Scope `GUI-kompatibel`.
- Shops, Pickup und Held Items bleiben separate Writer-Scope-Bloecke ohne Hochstufung.
- Naechster empfohlener P1-Block: `analysis/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics-plan`.

## 2026-05-15 - Pickup Items Scope Diagnostics Plan

- Diagnose 114 plant Pickup Items als separaten Item-Writer-Scope nach Abschluss der Field-Items-Smokes.
- Relevante Pfade: `Settings.PickupItemsMod`, `GameRandomizer.maybeRandomizePickupItems()`, `ItemRandomizer.randomizePickupItems()`, `Gen3RomHandler.getPickupItems()` / `setPickupItems(...)`.
- Pickup bleibt ein Table-/Locator-/Probability-Scope; vor jedem Write-Smoke muss `PickupTableStartLocator`, `PickupItemCount`, Tabellenlaenge und Item-ID-Validitaet read-only gegen den CFRU/DPE Gen9-BPRE-Kandidaten geprueft werden.
- Empfohlene Reihenfolge: Pickup read-only Kandidatendiagnose, danach Pickup Random ohne Ban Bad, danach Pickup Random mit Ban Bad.
- Field Items bleiben abgeschlossen; Shops und Held Items bleiben ohne Hochstufung getrennte Scopes.

## 2026-05-15 - Pickup Items Scope Diagnostics

- Diagnose 115 scanned Pickup Items read-only and sanitized.
- Pickup locator/count/table model is stable for the candidate: `pickupLocatorSuccessful=true`, `pickupItemsTotal=16`, `pickupExpectedCount=16`, `pickupEntrySize=4`, `pickupProbabilitySlots=10`, `pickupProbabilityModelStable=true`, `pickupTableLengthMismatch=0`.
- Item-ID safety is clean for invalid/unloaded/fallback/placeholder values, but Ban Bad remains a separate poolfilter concern: `pickupBadItems=7`, `pickupBadItemPoolCandidates=51`, `pickupBadItemPoolExcluded=51`.
- `FVX-ITEM-010` remains `Write modelliert` until a Pickup Random Write-/Reload-Smoke passes.
- Next recommended block: `test/upr-fvx-cfru-dpe-pickup-items-random-reload-smoke` with `banBadRandomPickupItems=false`.

## 2026-05-15 - Pickup Items Random Reload-Smoke blocked

- Diagnose 116 ran the Pickup-only Random smoke with `banBadRandomPickupItems=false`.
- Save/log/output/reopen succeeded, but Pickup reload is blocked: `pickupLocatorSuccessful=false`, `pickupItemsTotalReload=0`, `pickupItemReloadMismatches=16`, `pickupTableLengthMismatches=1`, `pickupProbabilityMismatches=16`.
- Direct write-scope safety stayed clean: `invalidPickupItemWrites=0`, `unloadedPickupItemWrites=0`, `fallbackPickupItemWrites=0`, `placeholderPickupItemWrites=0`; Field Items, Shops and Held Items were unchanged.
- `FVX-ITEM-010` remains `Write modelliert` until the Pickup reload-locator blocker is fixed and re-smoked.
- Next recommended block: `analysis/upr-fvx-cfru-dpe-pickup-items-reload-locator-blocker-plan`.
