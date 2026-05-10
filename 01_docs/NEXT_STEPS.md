# Next Steps

## Aktueller Arbeitsblock

Workspace-Build- und Randomizer-Integration auf `planning/workspace-build-randomizer-integration` planen.

## Nächste Schritte

1. `01_docs/setup/workspace-build-randomizer-integration-plan.md` reviewen.
2. Zielstruktur fuer `02_external/`, `03_tools/releases/`, `04_private_roms/`, `05_builds/` und `08_tests/` pruefen.
3. Pruefen, ob die Clone-/Fork-Strategie fuer UPR FVX, CFRU/DPE-Gen9 und Referenz-Repos passt.
4. Pruefen, ob der geplante ROM-Hash-Workflow ausreichend ist, ohne ROM-Inhalte oder ROM-Dateien in Git/ChatGPT zu bringen.
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
- keine Forks verändern oder anlegen
- keine Tool-Binaries herunterladen, anfassen oder committen
- keine UPR-FVX-JARs herunterladen oder bauen
- keine Änderungen direkt auf `main`
- keine Installationen erzwingen
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen
- keine parallelen Agenten auf demselben Branch einsetzen

## Danach

Geplante Folge-Arbeitspakete nach gemergtem Integrationsplan-PR:

1. `setup/devkitpro-toolchain-install-check`
   - devkitPro/devkitARM installieren oder freigegebenen Installationsweg ausführen
   - `arm-none-eabi-gcc`, `DEVKITPRO`, `DEVKITARM`, Python und `make` pruefen
   - keine Builds, keine ROMs

2. `analysis/external-source-pinning`
   - externe Quellen read-only klonen oder ueber GitHub pruefen, falls freigegeben
   - Branches und Commit-Hashes fuer UPR FVX, CFRU/DPE-Gen9 und Referenzen pinnen
   - entscheiden, ob Forks noetig sind

3. `randomizer/upr-fvx-start-smoke-test`
   - UPR-FVX-JAR lokal beschaffen oder aus gepinntem Source-Stand bauen, je nach Freigabe
   - Java-Anforderung und Startbefehl dokumentieren
   - ohne ROM laden, sofern nicht separat freigegeben

4. `build/cfru-dpe-source-readiness`
   - CFRU/DPE-Gen9 strukturell pruefen
   - Build-Anforderungen und Konfigurationsdateien dokumentieren
   - keine ROM, kein Build

5. `rom/fire-red-private-hash-check`
   - private FeuerRot-Basis lokal in `04_private_roms/` pruefen
   - Dateiname und SHA-256-Pruefergebnis dokumentieren
   - keine ROM hochladen, keine ROM committen

6. `build/cfru-dpe-first-smoke-build`
   - erst nach Toolchain-, Quellen- und ROM-Freigabe
   - Build-Ergebnis in `05_builds/`, nicht in Git

7. `randomizer/custom-build-compatibility-smoke-test`
   - gebaute GBA lokal mit UPR FVX testen
   - Randomizer-Bereiche getrennt testen
   - Ergebnisse in `08_tests/` dokumentieren

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
