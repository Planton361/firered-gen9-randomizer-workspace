# Next Steps

## Aktueller Arbeitsblock

Post-Merge-Dokumentationsstatus nach PR #17 auf `docs/post-merge-agent-best-practices-sync` synchronisieren.

## Nächste Schritte

1. Agent-Best-Practices-Refresh als gemerged/erledigt markieren.
2. Aktuellen Stand auf main/post-merge-synchronisiert setzen.
3. Nächsten Arbeitsbranch `setup/linux-gba-toolchain-plan` bestätigen.
4. Keine neuen Workflow-Regeln ergänzen.
5. Abschluss-Checks ausführen:

```sh
git status --short
git diff --stat
# falls verfügbar:
07_scripts/bootstrap/check-git-safety.ps1 oder vorhandenes Safety-Check-Fallback
```

6. Branch committen, pushen und als PR nach `main` führen. PR nicht mergen.

## Nicht tun

- keine ROMs bewegen
- keine ROMs lesen, kopieren oder ändern
- keine Saves oder Emulator States anfassen
- keine Builds starten oder committen
- keine externen Repos klonen
- keine Forks verändern
- keine Tool-Binaries anfassen oder committen
- keine Änderungen direkt auf `main`
- keine Installationen erzwingen
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen
- keine parallelen Agenten auf demselben Branch einsetzen

## Danach

Nächster sinnvoller Arbeitsblock nach gemergtem Post-Merge-Sync-PR:

- Branch `setup/linux-gba-toolchain-plan`
- devkitPro/devkitARM- und `arm-none-eabi-gcc`-Vorgehen für Linux/CachyOS planen
- weiterhin keine ROMs lesen, kopieren oder bearbeiten
- keine Installationen oder Build-Schritte ohne separaten Arbeitsblock durchführen
- JetBrains MCP erst nach Toolchain-Inventur separat evaluieren

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
