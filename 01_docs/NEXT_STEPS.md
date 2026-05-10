# Next Steps

## Aktueller Arbeitsblock

Dokumentationsstand nach gemergtem PR #9 synchronisieren und den nächsten kleinen Arbeitsblock vorbereiten.

## Nächste Schritte

1. Toolchain-/Workspace-Inventur ohne ROM-/Build-Arbeit prüfen.
2. Dafür den nächsten Branch `setup/toolchain-local-inventory` vorbereiten.
3. GitHub CLI ist installiert und authentifiziert; PR-Erstellung kann mit `gh pr create` erfolgen.
4. Sicherstellen, dass kein Clone/Fork/Download und keine ROM-/Build-Arbeit erfolgt.
5. Lokale Checks ausführen:

```powershell
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
git status --short
git diff --stat
```

6. Für das nächste Arbeitspaket nur Inventur dokumentieren:

```powershell
git switch -c setup/toolchain-local-inventory
```

## Nicht tun

- keine ROMs bewegen
- keine Builds starten
- keine externen Repos klonen
- keine Forks verändern
- keine Tool-Binaries committen
- keine Änderungen direkt auf `main`

## Danach

Nächster sinnvoller Arbeitsblock:

- lokale Toolchain-/Workspace-Inventur prüfen
- vorhandene Tools und Pfade dokumentieren
- keine ROMs lesen, kopieren oder bearbeiten
- keine Builds starten

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
