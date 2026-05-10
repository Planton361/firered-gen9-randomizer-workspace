# Next Steps

## Aktueller Arbeitsblock

Agent-Best-Practices-Refresh auf `docs/agent-best-practices-refresh` dokumentieren.

## Nächste Schritte

1. Kompakte Codex-Prompt-Vorlagen in `01_docs/quality/prompt-templates.md` reviewen.
2. Usage-Optimierung in `01_docs/quality/usage-optimization.md` reviewen.
3. Agent-Tooling-Policy in `01_docs/setup/agent-tooling-policy.md` reviewen.
4. MCP-Policy in `01_docs/setup/mcp-policy.md` reviewen.
5. `.aiignore` und `.github/pull_request_template.md` prüfen.
6. Abschluss-Checks ausführen:

```sh
git status --short
git diff --stat
# falls verfügbar:
07_scripts/bootstrap/check-git-safety.ps1 oder vorhandenes Safety-Check-Fallback
```

7. Branch committen, pushen und als PR nach `main` führen. PR nicht mergen.

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

Nächster sinnvoller Arbeitsblock nach gemergtem Agent-Best-Practices-PR:

- Branch `setup/linux-gba-toolchain-plan`
- devkitPro/devkitARM- und `arm-none-eabi-gcc`-Vorgehen für Linux/CachyOS planen
- weiterhin keine ROMs lesen, kopieren oder bearbeiten
- keine Installationen oder Build-Schritte ohne separaten Arbeitsblock durchführen
- JetBrains MCP erst nach Toolchain-Inventur separat evaluieren

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
