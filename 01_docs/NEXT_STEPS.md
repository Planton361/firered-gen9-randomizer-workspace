# Next Steps

## Aktueller Arbeitsblock

GBA-Toolchain-Vorgehen fuer Linux/CachyOS auf `setup/linux-gba-toolchain-plan` planen.

## Nächste Schritte

1. `01_docs/setup/linux-gba-toolchain-plan.md` reviewen.
2. Entscheidungspunkte fuer devkitPro/devkitARM, `arm-none-eabi-gcc` und optional `agbcc` pruefen.
3. Bestaetigen, dass keine Installation, kein Build und keine ROM-/Repo-Arbeit stattgefunden hat.
4. Naechsten Branch `setup/linux-gba-toolchain-source-review` vorbereiten.
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

Nächster sinnvoller Arbeitsblock nach gemergtem GBA-Toolchain-Plan-PR:

- Branch `setup/linux-gba-toolchain-source-review`
- offizielle devkitPro/devkitARM-Dokumentation und dokumentierte Ziel-Repos read-only auf Toolchain-Anforderungen pruefen
- weiterhin keine ROMs lesen, kopieren oder bearbeiten
- keine Installationen oder Build-Schritte ohne separaten Arbeitsblock durchfuehren
- keine externen Repos klonen oder Forks anlegen

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
