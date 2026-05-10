# Next Steps

## Aktueller Arbeitsblock

Linux/CachyOS-Toolchain-Inventur auf `setup/linux-toolchain-inventory` dokumentieren.

## Nächste Schritte

1. Tool-Manifest und Roadmap-Status für Linux/CachyOS-Inventur reviewen.
2. GitHub-CLI-Auth-Fund als offenen Punkt einordnen, ohne Secrets zu dokumentieren.
3. Fehlende GBA-Toolchain-Komponenten als offen dokumentieren.
4. Windows-Toolchain-Befunde weiterhin als historischen Stand markieren.
5. Abschluss-Checks ausführen:

```sh
git status --short
git diff --stat
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

## Danach

Nächster sinnvoller Arbeitsblock nach gemergtem Linux-Toolchain-Inventur-PR:

- Branch `setup/linux-gh-auth-refresh`
- GitHub CLI auf Linux neu authentifizieren bzw. ungültigen Token bereinigen
- danach `gh auth status` erneut prüfen
- weiterhin keine ROMs lesen, kopieren oder bearbeiten
- keine Installationen oder Build-Schritte ohne separaten Arbeitsblock durchführen

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
