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

- `02_external/upr-fvx` ist auf UPR-FVX PR #111 Merge-Commit `4805a5a930bc97203199816222465c76de2f2150` gepinnt.
- PR #111 fuehrt das opt-in Feature `MODE-TRAINER-CLASS-SPRITE-SYNC` ein. Ohne diesen Modus bleibt `Randomize Trainer Class Names` legacy/textlabel-only; mit Sync folgen `trainerClass` und sichtbarer `trainerPic` der Trainer-Class-Name-Zuordnung. `Randomize Trainer Names` bleibt separat und aendert keine `classId`/`pic`.
- Ziel ist Class label / classId / pic consistency, nicht Regular-only-Remapping. Special-Zielklassen wie Rival/Gym/Elite/Champion werden nicht pauschal ausgeschlossen; Zielklassen ohne beobachteten validen `trainerPic` werden uebersprungen.
- Bisherige sanitized Evidence: Regular trainer battle started, visible sprite changed, log showed class/sprite sync markers, and the earlier semantic mismatch was corrected before merge. Final local smoke on the merged PR #111 pin is still needed. Keine P1-Promotion.
- `08_tests/randomizer/206_trainer_class_sprite_sync.md` dokumentiert den aktuellen Sync- und Handoff-Stand.
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
