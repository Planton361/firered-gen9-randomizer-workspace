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

## Wichtige Dateien

- `AGENTS.md` – Regeln für Codex und andere Coding Agents
- `01_docs/PROJECT_BRIEF.md` – Projektüberblick
- `01_docs/SESSION_STATE.md` – aktueller Projektstand
- `01_docs/NEXT_STEPS.md` – nächste Arbeitsschritte
- `01_docs/DECISIONS_INDEX.md` – getroffene Entscheidungen
- `01_docs/references/source-index.md` – Quellen und Referenzen
- `01_docs/references/tool-manifest.md` – Tools, Versionen, Pfade, Branches

## Arbeitsweise

- Windows PowerShell ist das Standardterminal.
- GitHub ist die Source of Truth.
- Änderungen laufen über Branches und Pull Requests.
- `main` ist der stabile Branch.
- Codex arbeitet nur auf freigegebenen Arbeitsbranches.
- Private und rechtlich sensible Dateien bleiben lokal.
