# Next Steps

## Aktueller Arbeitsblock

Lokale Toolchain-/Workspace-Inventur auf `setup/toolchain-local-inventory` dokumentieren und als PR nach `main` führen.

## Nächste Schritte

1. PR `setup/toolchain-local-inventory` reviewen.
2. Im lokalen Windows-Workspace die dokumentierten Inventurbefehle aus `01_docs/references/tool-manifest.md` ausführen.
3. Ergebnisse zu Versionen und Pfaden nur als Dokumentation nachtragen, falls sie lokal bestätigt wurden.
4. Safety-Checks lokal ausführen:

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
- fehlende Toolchain-Bestandteile als Installationsentscheidung dokumentieren
- weiterhin keine ROMs lesen, kopieren oder bearbeiten
- weiterhin keine Builds starten, bis Toolchain-Status freigegeben ist

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
