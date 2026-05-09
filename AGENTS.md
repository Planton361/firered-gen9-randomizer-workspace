# AGENTS.md

## Projektkontext

Dieses Repository ist ein dokumentierter Workspace für einen Pokémon FireRed Gen9 Randomizer-Hack.

Hauptziel:
- FireRed-basierter Custom Hack
- Gen9-Pokémon über CFRU/DPE-nahe Basis
- spätere Kompatibilität mit Universal Pokémon Randomizer FVX
- spätere Kompatibilität mit BizHawk und Ironmon Tracker

## Grundregeln

- Keine ROMs lesen, ändern, kopieren oder committen.
- Keine Saves, Emulator States oder Builds committen.
- Keine privaten Dateien aus `04_private_roms/`, `05_builds/` oder `03_tools/releases/` anfassen, außer der Nutzer fordert es ausdrücklich.
- Keine Pushes ohne ausdrückliche Freigabe.
- Keine großen Refactors ohne vorherige Zusammenfassung und Zustimmung.
- Kleine, reviewbare Änderungen bevorzugen.
- Jede Änderung muss dokumentierbar sein.

## Arbeitsmodus

Vor jeder Änderung:

1. relevanten Kontext lesen
2. geplante Änderung kurz zusammenfassen
3. betroffene Dateien nennen
4. Risiken nennen
5. danach erst ändern

Nach jeder Änderung:

1. `git diff --stat`
2. relevante Dateiänderungen zusammenfassen
3. Tests oder Checks nennen
4. nächsten sinnvollen Schritt vorschlagen

## Wichtige Dokumente

Immer berücksichtigen:

- `README.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `01_docs/DECISIONS_INDEX.md`
- `01_docs/references/source-index.md`
- `01_docs/references/tool-manifest.md`

## Terminal

Dieses Projekt nutzt Windows PowerShell als primäre Shell.

Keine Bash-Brace-Expansion verwenden.
Stattdessen PowerShell-native Befehle wie `New-Item`, `Set-Content`, `Test-Path`.

## Git-Regeln

- Standardbranch: `main`
- Arbeit erfolgt auf Feature-/Setup-Branches
- Commitnachrichten kurz und konkret
- Keine direkten Pushes auf `main`, außer der Nutzer fordert es ausdrücklich
