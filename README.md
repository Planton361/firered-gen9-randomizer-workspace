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

- `02_external/upr-fvx` bleibt auf UPR-FVX PR #106 Merge-Commit `5bb1d853f132095922be2aceef55af2878192b85` gepinnt.
- PR #105 macht strict geladene generische `RUNTIME-SOURCE`-Trainer randomizer-eligible; diese Evidence bleibt mit dem PR-#106-Post-Audit-Tooling kompatibel.
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
