# Next Steps

## Aktueller Arbeitsblock

Linux/CachyOS-GitHub-CLI- und Git-Auth-Refresh auf `setup/linux-gh-auth-refresh` dokumentieren.

## Nächste Schritte

1. `gh auth status` erfolgreich prüfen.
2. `git fetch origin` erfolgreich prüfen.
3. Tool-Manifest und Roadmap-Status für nutzbare GitHub-CLI-/Git-Auth aktualisieren.
4. Dokumentieren, dass Push und PR-Erstellung auf Linux/CachyOS wieder nutzbar sind.
5. Abschluss-Checks ausführen:

```sh
git status --short
git diff --stat
git diff
```

6. Branch committen, pushen und als PR nach `main` führen. PR nicht durch Codex mergen.

## Nicht tun

- keine ROMs bewegen
- keine Builds starten
- keine externen Repos klonen
- keine Forks verändern
- keine Tool-Binaries committen
- keine Änderungen direkt auf `main`
- keine Installationen erzwingen
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- `.idea/` nicht stagen oder committen

## Danach

Nächster sinnvoller Arbeitsblock nach gemergtem Linux-GitHub-Auth-PR:

- Branch `setup/linux-gba-toolchain-plan`
- devkitPro/devkitARM- und `arm-none-eabi-gcc`-Vorgehen für Linux/CachyOS planen
- weiterhin keine ROMs lesen, kopieren oder bearbeiten
- keine Installationen oder Build-Schritte ohne separaten Arbeitsblock durchführen

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
