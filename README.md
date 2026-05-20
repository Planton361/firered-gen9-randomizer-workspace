# FireRed Gen9 Randomizer Workspace

Dieses Repository ist die Source of Truth für den dokumentierten Workspace eines Pokémon FireRed Gen9 Randomizer-Projekts.

## Ziel

Ein FireRed-basierter Custom Hack soll perspektivisch:

- Gen9-Pokémon enthalten
- mit Universal Pokémon Randomizer FVX kompatibel werden
- mit BizHawk laufen
- mit Ironmon Tracker nutzbar werden
- reproduzierbar dokumentiert und versioniert sein

## Rolle dieses Repositories

Dieses Repository enthält:

- Projektstruktur
- Dokumentation
- Roadmap
- Tool-Manifest
- Quellenindex
- Bootstrap- und Check-Scripts
- Testprotokolle
- Codex-/Agent-Regeln

Dieses Repository enthält nicht:

- ROMs
- Saves
- Emulator States
- Builds
- Tool-Binaries
- private `.env`-Dateien
- urheberrechtlich relevante Artefakte

## Aktueller Randomizer-Pin

- `02_external/upr-fvx` ist auf den UPR-FVX compat-Merge-Commit `765d8ec0ab298bbaab4aa9f8f31b93c7259a47e5` gepinnt.
- Dieser Pin enthaelt die finalen Gen-Limit-/Special-Form-/Mechanic-Item-Fixes bis UPR-FVX PR #150 auf `compat/firered-gen9-cfru-dpe`.
- Gen Limit / Special Form / Mechanic Item Exclusions sind als `08_tests/randomizer/212_gen_limit_special_form_item_smoke.md` dokumentiert: Gen-Limit 1-9 infrastructure pass, Gen1-only und Gen1-6 log smokes korrekt, Gen7/8/9 Intro Mon crash-free mit valid visual-table candidates, Mega/GMax/Regional/Irregular/Special-form filtering lokal unauffaellig, Evolutionary Relatives bleiben expliziter Cross-Gen-Family-Override, Regionalformen werden ohne Regional-Override nicht durch Evolutionary Relatives reingezogen, Trainer Class Sprite Sync ist GUI-exposed, Oak-Lab Rival counter-starter bleibt unabhaengig von Rival Carries Starter Through Game erhalten, und Mechanic-Item-Filtering nutzt source-backed CFRU/DPE Kategorien fuer Mega/Z/Dynamax-GMax Items.
- Status: `PASS_TARGETED_LOG_VISUAL_SMOKE_WITH_CAVEATS`.
- Caveat: targeted local smoke only, kein Full-Playthrough, Plates/Drives/Memories/Nectars haben noch keine separaten user-facing Policies, Static Script/Gift/NPC item sources bleiben caveated falls sie nicht durch Randomizer-Item-Replacement-Pools laufen, custom/future form encodings ausserhalb dokumentierter CFRU/DPE identity blocks bleiben audit-required und keine P1-Promotion.
- Vorheriger Pin: UPR-FVX PR #127 Merge-Commit `155fac0b33474f6ed5b3fbaed7dd9bf24b4e1315`.
- Dieser Pin enthaelt zusaetzlich PR #125 Running-Shoes-Misc-Tweaks fuer CFRU/DPE BPRE, PR #126 Catching-Tutorial-Species-Mapping fuer CFRU/DPE BPRE und PR #127 Fast-Egg-Hatching-Null-`BreedingInfo`-Guard.
- Type Effectiveness Battle Smoke ist als `08_tests/randomizer/211_type_effectiveness_battle_smoke.md` dokumentiert: lokaler Battle-Smoke pass, Effektivitaetsverhalten wirkte passend, keine Battle-Crashes gemeldet.
- Caveat: targeted battle smoke, keine vollstaendige Type-Matchup-Matrix, kein Full-Playthrough und keine P1-Promotion.
- Misc Tweaks Behavior Smoke ist als `08_tests/randomizer/210_misc_tweaks_behavior_smoke.md` dokumentiert: Fastest Text pass, PC Potion pass, Run Without Running Shoes pass, Running Shoes Indoors pass, Catching Tutorial pass ohne Fragezeichen-Sprite/-Name, Fast Egg Hatching crash-free randomization smoke mit ladendem Output, Ban Lucky Egg likely pass / no issue observed.
- Reusable TMs und Forgettable HMs bleiben als CFRU-provided Stable-Profile-Caveat dokumentiert und sollen nicht doppelt durch das UPR-FVX stable profile aktiviert werden.
- Caveat: targeted behavior smoke, kein Full-Playthrough, kein Full-Hatch-Cycle-Proof, keine dedizierte Ban-Lucky-Egg-Drop-Proof-Evidence und keine P1-Promotion.
- Vorheriger Pin: UPR-FVX PR #124 Merge-Commit `0eb815418470fa1ac000695b95d09cb084338dca`.
- PR #124 enthaelt den PR-#123-Palette-Output-Write-Fix und den PR-#124-Expanded-Trainer-Logging-Fallback.
- Graphics/Palettes Evidence ist als `08_tests/randomizer/209_graphics_palettes_visual_smoke.md` dokumentiert: `Pokemon Palettes: Randomized/Changed`, CFRU-DPE palette copy save mit `normalPaletteWriteAttempts=841`, Base-vs-Output Palette Audit `sampledCount=21`, `normalChangedCount=21`, `shinyChangedCount=0`, `unchangedCount=0`, und sichtbare geaenderte Paletten.
- Der finale Lauf meldete kein `Error during logging`.
- Caveat: targeted visual/audit smoke, keine Full-Playthrough-, breite Shiny- oder P1-Promotion.
- Vorheriger Pin: UPR-FVX PR #118 Merge-Commit `ed692d07bfc81405706f2b94fda06639426e6a75`.
- PR #118 ergaenzt einen opt-in Wild Encounter Base-vs-Output Audit fuer Gen3/FRLG/CFRU-DPE.
- Der Audit ist diagnostic-only: keine Writer-/Randomizer-Verhaltensaenderung, keine P1-Promotion.
- Scope: modeled Gen3 base `WildPokemon` table path. Der Report vergleicht Base- und Output-ROM lokal pro Encounter-Slot mit Map-/Area-Identifier soweit verfuegbar, Encounter-Typ, Slot-Index, Base-Species, Output-Species und `changedFromBase`, plus Summary fuer total/changed/unchanged/changed percentage.
- CFRU/DPE special/runtime wild sources bleiben Follow-up, falls Audit und Ingame-Beobachtung auseinanderlaufen.
- Vorheriger Pin: UPR-FVX PR #117 Merge-Commit `5983011752273e00c402e25cc1ae1a9baca110f1`.
- PR #117 fixt `Rival Carries Starter Through Game` fuer CFRU/DPE Gen9 BPRE nach Foe-Pokemon-Randomization und verhindert die Intro-Mon-Species-0-Regression im extended BPRE-Pool.
- Combined Trainer Visual Runtime Smoke ist als `PASS_WITH_CAVEATS` dokumentiert: Intro Mon sichtbar randomisiert, Player Charmander -> Oak-Lab Rival Squirtle und Route-22 Rival Squirtle, Route-22-Rival-Sprite konsistent zum Oak-Lab-Rival-Sprite, Viridian-Forest-Trainer-Sprites randomisiert, keine Crash/Freeze/garbled-sprite-Beobachtung. Route-22 Rival non-starter Pokemon Silvally Lv9 zeigt, dass Rival Carries Starter Through Game den Starter-Slot schuetzt/korrigiert, waehrend Non-Starter-Rival-Pokemon fuer Foe-Pokemon-Randomization eligible bleiben.
- `08_tests/randomizer/208_combined_trainer_visual_runtime_smoke.md` dokumentiert diesen aktuellen kombinierten Runtime-Smoke.
- Sanitized local evidence bestaetigt: Combined visual Rival test fixed, Intro Mon sichtbar Blissey statt Species 0, Player Charmander -> Rival Squirtle, Trainer Class Sprite Sync bleibt visuell okay aus den vorherigen Checks, und kein Crash/Freeze/garbled sprite wurde gemeldet. Caveat: targeted smoke, kein Full-Playthrough. Keine P1-Promotion.
- `08_tests/randomizer/207_rival_counter_starter_and_combined_visual_smoke.md` dokumentiert den aktuellen Rival-Counter-Starter- und Combined-Visual-Smoke-Stand.
- Vorheriger Pin: UPR-FVX PR #116 Merge-Commit `36dd431d059bc69eb1bee3311200e28c872c6cc9`.
- PR #116 schliesst den finalen `MODE-TRAINER-CLASS-SPRITE-SYNC`-Stand ab. Ohne diesen Modus bleibt `Randomize Trainer Class Names` legacy/textlabel-only; mit Sync folgen `trainerClass` und sichtbarer `trainerPic` der Trainer-Class-Assignment. `Randomize Trainer Names` bleibt separat und aendert keine `classId`/`pic`.
- Ziel ist Class label / classId / pic consistency, nicht Lore-/Plausibility-Stabilitaet. Regular Trainer werden per-trainer randomisiert; Rival/Friend-Zeilen teilen eine gruppierte Zielklasse/einen gruppierten `trainerPic`; Runtime-Source-Zeilen sind enthalten, wo sie eligible sind.
- Sanitized local evidence bestaetigt: Viridian-Forest-Bug-Catcher-Klassen werden per-trainer unterschiedlich randomisiert, Rival behaelt seinen ersten randomisierten Sprite ueber spaetere Auftritte, weitere getestete Trainer wirkten passend, und kein garbled sprite / crash wurde gemeldet. Caveat: targeted visual smoke, kein Full-Playthrough. Keine P1-Promotion.
- `08_tests/randomizer/206_trainer_class_sprite_sync.md` dokumentiert den finalen Sync- und Smoke-Stand.
- Vorheriger Pin: UPR-FVX PR #109 Merge-Commit `a9bb4a5f201c5078ec02fe1f2f8417695448afe9`.
- PR #109 synchronisiert fuer CFRU/DPE Gen9 BPRE die sichtbare Intro-Mon-Visual-Quelle: die Nidoran-female `PokemonFrontImages`- und `PokemonNormalPalettes`-Eintraege werden beim Intro-Mon-Randomize-Pfad auf die Asset-Pointer der Ziel-Spezies gesetzt.
- Sanitized local evidence bestaetigt: der sichtbare Oak-Intro-Sprite wechselte nach dem Fix weg von Nidoran female; kein Crash, Freeze oder garbled sprite wurde im targeted Ingame-Smoke beobachtet.
- PR #107/#108 stellen weiterhin die Intro-Mon Visual-Source-Diagnose bereit: `No Random Intro Mon` ist die negative GUI-Option, intern ist `randomizeIntroMon=true` der aktive Intro-Mon-Randomize-Pfad; `MODE-INTRO-RANDOM` setzt true, `MODE-NO-RANDOM-INTRO` und `FVX-GEN-003` setzen false.
- Intro Mon bleibt targeted-smoke-bestaetigt, nicht Full-Playthrough- oder P1-promoted.
- PR #105 macht strict geladene generische `RUNTIME-SOURCE`-Trainer randomizer-eligible; diese Evidence bleibt mit dem PR-#106-Post-Audit-Tooling und dem PR-#109-Pin kompatibel.
- Viridian Forest runtime-source trainer IDs `531/532` sind durch sanitized local evidence fuer Load, Randomize, Save und Ingame-Smoke bestaetigt.
- Der randomized Output-ROM Audit meldete fuer `unloaded-valid-parties` `total=0`; Rival 2 `329/330/331` und Brock `414` zeigten ebenfalls randomisierte Parties in sanitized local evidence.
- Loaded-mismatch, invalid-pointer, empty-party, out-of-range Runtime-Rows und Full-Playthrough bleiben Follow-up-Scope. Keine P1-Promotion.

## Wichtige Dateien

- `AGENTS.md` – Regeln für Codex und andere Coding Agents
- `01_docs/PROJECT_BRIEF.md` – Projektüberblick
- `01_docs/SESSION_STATE.md` – aktueller Projektstand
- `01_docs/NEXT_STEPS.md` – nächste Arbeitsschritte
- `01_docs/DECISIONS_INDEX.md` – getroffene Entscheidungen
- `01_docs/references/source-index.md` – Quellen und Referenzen
- `01_docs/references/tool-manifest.md` – Tools, Versionen, Pfade, Branches

## Arbeitsweise

- Linux/CachyOS ist die primäre lokale Entwicklungsumgebung.
- POSIX-Shell-kompatible Kommandos sind der neue Standard für lokale Arbeitsschritte.
- Windows PowerShell bleibt nur historischer/Legacy-Kontext für bereits dokumentierte frühere Arbeitsblöcke.
- GitHub ist die Source of Truth.
- Änderungen laufen über Branches und Pull Requests.
- `main` ist der stabile Branch.
- Codex arbeitet nur auf freigegebenen Arbeitsbranches.
- Private und rechtlich sensible Dateien bleiben lokal.
