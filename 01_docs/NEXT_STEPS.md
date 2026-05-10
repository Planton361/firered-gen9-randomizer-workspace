# Next Steps

## Aktueller Arbeitsblock

Linux/CachyOS-Workspace-Migration auf `setup/linux-workspace-migration` dokumentieren.

## Nächste Schritte

1. README und AGENTS-Regeln auf Linux/CachyOS-first reviewen.
2. Windows-PowerShell- und Windows-PATH-Angaben als historischen Stand einordnen.
3. Tool-Manifest auf Linux-Inventur vorbereiten.
4. Roadmap-Status auf OS-Migration und danach Linux-Toolchain-Inventur umstellen.
5. Safety-Checks ausführen:

```sh
git status --short
git diff --stat
# optional, falls pwsh installiert ist:
pwsh -File ./07_scripts/bootstrap/check-git-safety.ps1
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
- keine lokalen Pfade als bestätigt dokumentieren, bevor sie auf Linux geprüft wurden

## Danach

Nächster sinnvoller Arbeitsblock nach gemergtem Linux-Migrations-PR:

- Linux-Toolchain-/Workspace-Inventur durchführen
- Git, GitHub CLI, Java, make, devkitPro/devkitARM und optional pwsh auf Linux prüfen
- Ergebnisse nur dokumentieren, keine Builds starten
- weiterhin keine ROMs lesen, kopieren oder bearbeiten

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
