# Session State

## 2026-05-13 - CFRU/DPE Base Stats + Types Scope-and-Write Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write`

Aktueller Stand:

- Workspace PR #88 als gemerged geprueft.
- UPR-FVX-Fix `20f16d07ab4ea62e5cd3f27ef09a6d5b036d2392` erstellt.
- CFRU/DPE-gegatetes BaseStats-Type-Mapping implementiert: raw `0x17` wird als `Type.FAIRY` gelesen und `Type.FAIRY` als `0x17` geschrieben.
- CFRU/DPE-TypeTable-Pool enthaelt Fairy, aber kein Stellar; Stellar-/unsupported Primary-Type-Species werden im Type-Randomizer defensiv uebersprungen.
- Neues Diagnoseprotokoll `08_tests/randomizer/051_base_stats_types_scope_write_diagnostics.md` erstellt.
- Base Stats-only, Types-only und Base Stats + Types liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `writeReloadBaseStatsMismatches=0` und `typeIdMismatches=0`.
- Keine Hidden-Ability-, Encounter-Held-Item-, Move-Data-Write-, Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Hidden Abilities separat fixen oder vorher Item-/Bad-Item-Modell fuer Encounter Held Items starten.

## 2026-05-13 - CFRU/DPE Base Stats, Types, Abilities Model

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model`

Aktueller Stand:

- UPR-FVX PR #25 und Workspace PR #87 als gemerged geprueft.
- Neues read-only Protokoll `08_tests/randomizer/050_p1_base_stats_types_abilities_model.md` erstellt.
- `gBaseStats` fuer den getesteten CFRU/DPE Gen9-BPRE-Stand modelliert: Pointer-Ort `0x080001BC`, Entry-Size `0x1C`, internes Species-Indexing bis `SPECIES_PECHARUNT=0x59F` / `NUM_SPECIES=1440`.
- CFRU BaseStats-Felder eingeordnet: Stats, `type1/type2`, `item1/item2`, `ability1/ability2` und `hiddenAbility` bei Offset `0x1A`.
- FVX-Risiken dokumentiert: Gen3-Type-Mapping liest/schreibt Fairy aktuell nicht korrekt, Stellar ist nicht im FVX-Type-Enum, Hidden Ability wird nicht gelesen/geschrieben, Ability-Count ist `77` statt CFRU `255`, Encounter Held Items haengen am erweiterten Itemmodell.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein ROM-/Build-/Log-Artefakt.

Naechster sinnvoller Schritt:

- `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write` als kleinen ersten Fixbranch planen.
- Hidden Abilities und Encounter Held Items getrennt behandeln; Encounter Held Items erst nach Item-/Bad-Item-Modell.

## 2026-05-13 - CFRU/DPE Learnset GUI Flow Safety Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`

Aktueller Stand:

- UPR-FVX-Fix `086d2a9177df7624a0e7ca1876b210a200d7aa98` erstellt.
- Logger-Nullsafety, Learnset-Repointing-Multiwrite-Safety, Trainer-Movesets-Key-Fallbacks sowie TM/HM-/Tutor-Level-Up-Sanity defensiv stabilisiert.
- Neues Protokoll `08_tests/randomizer/049_p1_learnset_gui_flow_safety_fix_diagnostics.md` erstellt.
- Sieben GameRandomizer-nahe Movesets/Learnsets-Laeufe diagnostiziert: Movesets-only, Trainer-Movesets, Reorder-Damaging, TM/HM-Sanity, Tutor-Sanity, gekoppelte Egg Moves und TM/HM+Tutor-Sanity.
- Alle Laeufe liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true` und `writeReloadLearnsetMismatches=0`.
- Reorder-Damaging nutzt zwei freie Learnset-Blob-Bloecke innerhalb `0x1219A48-0x1600000`; der zweite Write blockiert nicht mehr an einem statischen FreeSpace-Start.
- Keine Move-Data-Write-, Tutor-Text/Menu-, Special-Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.
- Danach Move-Data-Write, Items/Shops/Field, Palette/Graphics und Special-Tutor/Text/Menu separat modellieren.

## 2026-05-13 - CFRU/DPE Learnset GUI Combination Diagnostics

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-learnset-gui-combinations`

Aktueller Stand:

- UPR-FVX PR #24 und Workspace PR #85 als gemerged geprueft.
- Neues Protokoll `08_tests/randomizer/048_p1_learnset_gui_combinations.md` erstellt.
- GameRandomizer-nahe Movesets/Learnsets-Laeufe diagnostiziert; keine Codeaenderung und keine `02_external/**`-Aenderung.
- Erster Learnset-Repointing-Write bleibt stabil: `plannedBlobBytes=30099`, `writtenBlobBytes=31771`, `pointertableEntriesUpdated=1413`, `writeReloadLearnsetMismatches=0`.
- Movesets-only, Movesets+TM/HM ohne Level-Up-Sanity, Movesets+Tutor ohne Level-Up-Sanity und gekoppelte Egg Moves speichern/reloaden stabil.
- Voller GUI-P1-Support bleibt blockiert durch Logger-Fehler, Trainer-Movesets-Kombinationen, Reorder-Damaging-Moves sowie TM/HM-/Tutor-Level-Up-Sanity.

Naechster sinnvoller Schritt:

- Fixbranch `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety` starten.
- Ziele: multi-write-sicheren Learnset-Repointing-Pfad, interne Species-ID-Key-Fallbacks fuer Sanity/Trainer-Movesets und Logger-Nullpfad beheben.


## 2026-05-13 - CFRU/DPE Learnset-Write Repointing Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`

Aktueller Stand:

- UPR-FVX-Fix `77de517da880bebb6ed690ca6e170e5bd10b9cad` erstellt.
- `setMovesLearnt()` schreibt fuer den eng gegateten CFRU/DPE Gen9-BPRE-Pfad neue Level-Up-Learnset-Blobs in die validierte FreeSpace-Region `0x1219A48-0x1600000`.
- Die bestehende `gLevelUpLearnsets`-Pointertable bei `0x25D7B4` bleibt erhalten und wird pro interner Species-ID aktualisiert.
- Diagnose 046 bestaetigt `plannedBlobBytes=17418`, `writtenBlobBytes=11547`, `uniqueBlobCount=416`, `pointertableEntriesUpdated=1413` und `writeReloadLearnsetMismatches=0`.
- Save, Reload, Output-ROM und nichtleerer Log waren im lokalen Diagnoseharness erfolgreich; lokale Artefakte blieben ignored unter `05_builds/**`.
- Keine Move-Data-Write-, Tutor-Text-, Special-Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs einen GUI-/Settings-Kombinationssmoke fuer Pokemon Movesets/Learnsets planen.
- Danach `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.


## 2026-05-13 - FVX GUI Options Compatibility Matrix

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-fvx-gui-options-matrix`

Aktueller Stand:

- Matrixprotokoll `08_tests/randomizer/047_fvx_gui_options_compatibility_matrix.md` erstellt.
- P1-supported Bereiche aus vorhandenen Diagnosen zusammengefuehrt: Standard/Fallback-Wild, Starters, Static/Gift, Trainer Species, Trainer Movesets, Trainer Held Items, Evolutions, Move-Data-Read, TM/HM 128-Slot, normale Tutor-Tabellen und direkte Egg Moves.
- Teilunterstuetzte Bereiche markiert: bounded Learnset-Write, Palette-Safety und Move-Data-Read ohne Write.
- Offene Hochrisiko-Writer priorisiert: Full Learnset Repointing, Base Stats/Types/Abilities, Move-Data-Write, Items/Shops/Field/Pickup und Palette/Graphics-Randomization.
- Keine Codeaenderung, keine `02_external/**`-Aenderung und keine ROM-/Build-/Tool-Artefakte.

Naechster sinnvoller Schritt:

- Wenn Phase 2 FreeSpace-Nachweis positiv ist, `compat/upr-fvx-cfru-dpe-learnset-write-repointing` fortsetzen.
- Andernfalls zuerst `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #80 ist gemerged.
- UPR-FVX PR #23 und Workspace PR #81 sind gemerged.
- UPR-FVX-Stand im Workspace: `20f16d07ab4ea62e5cd3f27ef09a6d5b036d2392`.
- TM/HM-only ist im getesteten CFRU/DPE-128-Slot-Scope P1-supported.
- Tutor-only ist im getesteten CFRU/DPE-152-Slot-Scope P1-supported.
- Egg-Move direct scope ist P1-supported.
- Learnset-Write bounded in-place ist implementiert und diagnostisch stabil fuer strikt validierte same-size Writes.
- Full Learnset-Write-Repointing ist im direkten `setMovesLearnt()`-Scope implementiert und diagnostisch stabil.
- Pokemon Movesets/Learnsets sind im getesteten GUI-/Settings-nahen Flow P1-supported.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model`

## Aktueller Arbeitsblock

CFRU/DPE Base Stats + Types Scope-and-Write-Fix.

## Ziel

Base Stats und Types fuer den getesteten CFRU/DPE Gen9-BPRE-Stand minimal gegatet schreiben/reloaden; Fairy `0x17` mappen und Stellar preserve/skip.

## In diesem Arbeitsblock geprueft / geaendert

- UPR-FVX PR #25 und Workspace PR #87 als gemerged geprueft.
- Workspace-Branch `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` erstellt; nicht auf `main` gearbeitet.
- UPR-FVX, CFRU und DPE read-only untersucht.
- Neues Protokoll erstellt: `08_tests/randomizer/050_p1_base_stats_types_abilities_model.md`.
- `08_tests/randomizer/README.md`, `SESSION_STATE.md`, `NEXT_STEPS.md` und Roadmap aktualisiert.

## Ergebnis

- `gBaseStats` wird im CFRU/DPE-Stand ueber Pointer-Ort `0x080001BC` gefuehrt und nutzt eine `0x1C`-Entry-Size.
- CFRU/DPE Species-Scope reicht bis `SPECIES_PECHARUNT=0x59F`, `NUM_SPECIES=0x5A0` / `1440`.
- Types sind in BaseStats bei `0x06/0x07`; `TYPE_FAIRY=0x17` und `TYPE_STELLAR=0x18` brauchen CFRU/DPE-spezifische Behandlung.
- Ability1/2 liegen bei `0x16/0x17`; Hidden Ability liegt bei `0x1A` und wird von FVX Gen3 aktuell nicht modelliert.
- Encounter Held Items liegen als `item1/item2` bei `0x0C/0x0E`; moderne Item-IDs und Bad-/Key-Item-Filter brauchen separates Itemmodell.

## Noch nicht gestartet

- Special-Tutor-Modell/Fix
- Move-Data-Write/`saveMoves()` fuer CFRU/DPE
- Base Stats + Fairy-Type-Scope-and-Write-Fix
- Hidden-Ability-Scope-and-Write-Fix
- Item-/Bad-Item-Datenmodellierung fuer Encounter Held Items
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen.

Lokale Diagnose-Artefakte blieben ignored unter `05_builds/**` und wurden nicht committed.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

UPR-FVX wurde nur im erlaubten Fixscope geaendert; andere `02_external/**`-Repos blieben unangetastet.

Keine Move-Data-Write-, Tutor-Text/Menu-, Special-Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Keine MCP-Configs mit Secrets angelegt.

## Naechste Pruefung

Lokal im Workspace nach den Dokumentationsaenderungen pruefen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

## Naechster empfohlener Branch

Nach Merge dieses Analyseblocks: `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write`. Hidden Abilities, Encounter Held Items, Move-Data-Write, Special Tutors, Tutor-Text/Menu-Rewrites, Items/Shops/Field und Palette/Graphics bleiben eigene Folgebranches.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-learnset-repointing-model

- UPR-FVX PR #23 und Workspace PR #81 als gemerged geprueft.
- CFRU/DPE Learnset-Repointing-Modell read-only dokumentiert.
- `gLevelUpLearnsets` Pointer-Ort `0x03EA7C` zeigt auf die aktive Pointertable bei `0x25D7B4`.
- Quellenanalyse: `1408` Pointertable-Zuweisungen, `1104` eindeutige Learnset-Ziele, `148` Shared-Zielgruppen.
- Kein statisch freier Append-Bereich belastbar belegt; spaeterer Fix muss FreeSpace im konkreten ROM nachweisen.
- Kein Fix, keine Aenderung an `02_external/**`, kein Repointing.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-learnset-write-bounded

- Workspace PR #80 als gemerged geprueft.
- UPR-FVX-Fix `dd9d80c16936a99bac1d7ef777b43baa7c2f029d` erstellt.
- `setMovesLearnt()` erhaelt einen eng gegateten CFRU/DPE bounded in-place Write-Pfad fuer `gLevelUpLearnsets`.
- Kein Repointing: Growth wird diagnostiziert und uebersprungen.
- Diagnose 044 bestaetigt Save/Log/Output/Reload und `writeReloadLearnsetMismatches=0`.
- Writer akzeptiert im Test `boundedWrites=1` und skippt `1412` unsafe Pointer; voller Learnset-Write braucht ein separates Repointing-Modell.
- Keine Move-Data-Write-, Tutor-Text-, Special-Tutor- oder Egg-Move-Ausweitung.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-egg-move-model

- UPR-FVX PR #21 und Workspace PR #77 als gemerged geprueft.
- CFRU/DPE Egg-Move-Modell read-only dokumentiert.
- `gEggMoves` als `u16`-Stream mit Species-Marker `species + 20000` und Terminator `0xFFFF` eingeordnet.
- DPE `repointall` zeigt `gEggMoves 08045C50`; FVX nutzt aktuell noch `EggMoves=0x25EF0C` aus dem FireRed-RomEntry.
- DPE-Egg-Move-Stream enthaelt Gen8-/PLA-/Paldea-Species und Move-IDs bis `MOVE_TIDYUP` ID `967`.
- Aktuelle FVX-Risiken: Pokédex-ID-Mapping statt interner Species-ID, globale Move-Ban-Arrays mit Laenge `827`, Egg-Move-Randomization an Learnset-Write gekoppelt.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility

- Workspace PR #76 als gemerged geprueft.
- UPR-FVX-Fix `4ce93754de390e9177efd2541c02edba0afbb0c4` erstellt.
- CFRU/DPE-Tutor-Pfad eng ueber `useCfruDpeGen9SpeciesCount` gegatet.
- `gMoveTutorMoves` als `u16[152]` ueber `0x8120BE4` gelesen/geschrieben.
- `gTutorLearnsets` als 19-Byte-/152-Bit-Compatibility pro Species ueber `0x8120C30` gelesen/geschrieben.
- Diagnose 040 bestaetigt Tutor moves-only, Compatibility-only und Tutor moves + Compatibility mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Special-Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder Tutor-Text-Rewrite-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tutor-model

- UPR-FVX PR #20 und Workspace PR #75 als gemerged geprueft.
- CFRU/DPE Tutor-/Special-Tutor-Modell read-only dokumentiert.
- `gMoveTutorMoves` als `u16[152]` ueber Pointer-Location `0x8120BE4` eingeordnet.
- `gTutorLearnsets` als 152-Bit-/19-Byte-Compatibility pro Species ueber Pointer-Location `0x8120C30` eingeordnet.
- Special Tutors als Sonderlogik ausserhalb der normalen Tabelle dokumentiert.
- FVX nutzt aktuell weiterhin klassischen FireRed-Tutor-Scope `15`; Tutor-only bleibt nicht P1-supported.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tm-hm-128-slot

- Workspace PR #74 als gemerged geprueft.
- UPR-FVX-Fix `58379ffd3146fcd6bb0eb416647cdf9b752cfc0e` erstellt.
- CFRU/DPE-128-Slot-TM/HM-Pfad eng ueber `useCfruDpeGen9SpeciesCount` gegatet.
- `gTMHMMoves` als `u16[128]` ueber `0x8125A8C` gelesen/geschrieben; TMs `0..119`, HMs `120..127`.
- `gTMHMLearnsets` als 16-Byte-/128-Bit-Compatibility pro Species ueber `0x8043C68` gelesen/geschrieben.
- Diagnose 038 bestaetigt TM moves-only, Compatibility-only und TM moves + Compatibility mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder TM51..TM120-Item-Text-/Palette-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model

- UPR-FVX PR #19 und Workspace PR #73 als gemerged geprueft.
- CFRU/DPE-128-Slot-TM/HM-Modell read-only dokumentiert.
- `gTMHMMoves` ist `u16[128]` ueber Pointer `0x8125A8C`; TMs `1..120`, HMs `121..128`.
- `gTMHMLearnsets` ist 128-Bit-/16-Byte-Compatibility pro Species ueber Pointer `0x8043C68`.
- FVX-`50+8`-Pfad bleibt P1-supported, bildet aber das 128-Slot-Modell nicht ab.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety

- Workspace PR #72 als gemerged geprueft.
- UPR-FVX-Fix `32e43ac03a5762542773213a13be4e0389f1deae` erstellt.
- TM-Move-Randomization fuer CFRU/DPE gegen Move-IDs oberhalb der alten FVX-Sicherheitslisten abgesichert.
- TM/HM-Compatibility fuer CFRU/DPE gegen Placeholder-Species und `null`-Typen abgesichert.
- Diagnose 036 bestaetigt TM moves + Compatibility, Compatibility-only und TM moves-only mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder 128-Slot-TM/HM-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-only

- UPR-FVX PR #18 und Workspace PR #71 als gemerged geprueft.
- TM/HM-only Diagnose auf UPR-FVX `c71fd75e67f5a839560bbf5de7c6f17317a64bd1` ausgefuehrt.
- FVX erkennt nur klassisches `50+8`-TM/HM-Modell.
- TM-Move-Randomization blockiert an altem Move-Ban-Array-Limit.
- TM/HM-Compatibility-only blockiert separat an Null-Type-Species.
- Neues Protokoll erstellt: `08_tests/randomizer/035_p1_tm_hm_only.md`.
- Kein Fix, keine Randomizer-Codeaenderung, keine committed ROM-/Build-Artefakte.

## 2026-05-13 - CFRU/DPE Egg-Move scope/write fix

- Active branch: `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write`.
- UPR-FVX fix commit: `18168b78b973a4c39f34053ac58f21279a26d8d2`.
- Implemented a gated CFRU/DPE `gEggMoves` reader/writer through pointer location `0x45C50` while preserving the classic `u16` stream, `species + 20000` markers, and `0xFFFF` sentinel.
- Preserved internal `SpeciesSet` identity for Egg-Move keys and guarded high move-ID flag-array access in `SpeciesMovesetRandomizer`.
- Added diagnosis `08_tests/randomizer/042_egg_moves_scope_and_write_fix_diagnostics.md`.
- Direct Egg-Move harness result: `moves.total=992`, highest loaded move `991:PsychicNoise`, target pointer `0x09A0E94C`, species entries `436 -> 436 -> 436`, highest species `1412`, highest move after/reload `991`, `writeReloadEggMoveMismatches=0`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`.
- No Learnset-Write, Move-Data-Write, Tutor-Text, Special-Tutor, or `setMovesLearnt()` expansion was included.

## 2026-05-13 - CFRU/DPE Learnset-Write-Modell

- Active branch: `analysis/upr-fvx-cfru-dpe-p1-learnset-write-model`.
- UPR-FVX PR #22 und Workspace PR #79 als gemerged geprueft.
- `gLevelUpLearnsets` Write-Modell read-only dokumentiert; keine Aenderung an `02_external/**`.
- Neues Protokoll: `08_tests/randomizer/043_p1_learnset_write_model.md`.
- Befund: Pointer-Ort `0x03EA7C` / `0x0803EA7C`, interne Species-ID-Pointertabelle, Eintraege `u16 move + u8 level`, Sentinel `{0, 0xFF}`, `MAX_LEARNABLE_MOVES=50`, Species bis `SPECIES_PECHARUNT=0x59F`, Moves bis `MOVE_PSYCHICNOISE=0x3DF`.
- Empfehlung: Folgefix nur eng gegatet und zunaechst bounded in-place; Repointing separat modellieren.
