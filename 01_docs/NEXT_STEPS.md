# Next Steps

## Aktueller Arbeitsblock

Lokale Toolchain-/Workspace-Inventur auf `setup/toolchain-local-inventory` dokumentieren und als PR nach `main` führen.

## Nächste Schritte

1. PR `setup/toolchain-local-inventory` reviewen.
2. Dokumentierte Inventurergebnisse im Tool-Manifest prüfen.
3. Entscheiden, ob `gh` PATH und devkitARM PATH separat nachgezogen werden sollen.
4. Safety-Checks vor PR-Abschluss erneut ausführen:

```powershell
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
git status --short
git diff --stat
```

5. PR nach Review mergen, nicht durch Codex.

## Nicht tun

- keine ROMs bewegen
- keine Builds starten
- keine externen Repos klonen
- keine Forks verändern
- keine Tool-Binaries committen
- keine Änderungen direkt auf `main`
- keine Installationen erzwingen

## Danach

Nächster sinnvoller Arbeitsblock nach gemergtem Inventur-PR:

- lokalen Inventur-Output auswerten
- fehlende PATH-Einträge für `gh` und `arm-none-eabi-gcc` als Setup-Entscheidung dokumentieren
- weiterhin keine ROMs lesen, kopieren oder bearbeiten
- weiterhin keine Builds starten, bis Toolchain-Status freigegeben ist

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
