# Next Steps

## Aktueller Arbeitsblock

PATH-Folgeklärung für lokale Toolchain auf `setup/path-toolchain-followup` vorbereiten.

## Nächste Schritte

1. Dokumentierte PATH-Folgeklärung im Tool-Manifest reviewen.
2. Für `gh` klären, ob Windows Terminal neu geöffnet oder PATH in PowerShell neu geladen werden soll.
3. Für `arm-none-eabi-gcc` klären, ob devkitARM installiert ist und nur PATH/Umgebungsvariablen fehlen.
4. Optional `agbcc` nur dokumentieren, falls es später für eine konkrete Build-Basis nötig wird.
5. Safety-Checks ausführen:

```powershell
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
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
- keine PATH- oder Umgebungsvariablen in dieser Dokumentationssession ändern

## Danach

Nächster sinnvoller Arbeitsblock nach gemergtem PATH-Follow-up-PR:

- konkrete Entscheidung treffen, ob PATH lokal angepasst werden soll
- falls ja, Änderung außerhalb des Repos durchführen und danach nur das Ergebnis dokumentieren
- weiterhin keine ROMs lesen, kopieren oder bearbeiten
- weiterhin keine Builds starten, bis Toolchain-Status freigegeben ist

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
