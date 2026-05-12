# Next Steps

## Aktueller Arbeitsblock

Randomizer-Smoke-Artefakte und Testprotokolle ordnen.

Aktueller Branch:

```text
maintenance/randomizer-smoke-artifact-cleanup
```

Zieldokumente:

```text
08_tests/randomizer/README.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
01_docs/references/tool-manifest.md
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `08_tests/randomizer/README.md`
   - `01_docs/SESSION_STATE.md`
   - `01_docs/NEXT_STEPS.md`
   - `00_project-control/roadmap/roadmap-status.md`
   - `01_docs/references/tool-manifest.md`
2. Workspace-Checks ausfuehren:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
git ls-files 05_builds 04_private_roms 03_tools/releases
```

3. Commit erstellen:

```text
docs: organize randomizer smoke artifacts
```

4. Branch pushen und Workspace-PR nach `main` erstellen.

## Neue Randomizer-Smoke-Konvention

- Dauerhafte Smoke-Protokolle liegen unter `08_tests/randomizer/`.
- Neue Smoke-Protokolle sollen nummerierte Dateinamen wie `001_<kurzer-zweck>.md`, `002_<kurzer-zweck>.md` nutzen.
- Bestehende unnummerierte Protokolle bleiben fuer stabile Verweise unveraendert und werden ueber `08_tests/randomizer/README.md` tabellarisch eingeordnet.
- Lokale Smoke-Artefakte sollen unter `05_builds/randomizer-smoke/NNN_<kurzer-zweck>/` abgelegt werden.
- Der neueste bestaetigte Stand wird in der Markdown-Tabelle als `Latest` markiert; ein `latest`-Symlink ist nicht erforderlich.

Aktueller Latest-Stand:

```text
Nr. 019 - Gen9 Standard-/Fallback Wild post-merge smoke
saveSuccessful=true
Gen7/8/9 im Wild-Log
```

## Cleanup-Stand

- Vor Cleanup: `05_builds=1.3G`, `05_builds/randomizer-smoke=1.1G`, `08_tests=196K`.
- Nach Cleanup: `05_builds=196M`, `05_builds/randomizer-smoke=0`.
- Entfernt wurden nur ignored lokale Smoke-Outputs im flachen `05_builds/randomizer-smoke/`-Ordner: `.gba`- und `.log`-Dateien.
- Nicht entfernt wurden Markdown-Protokolle, Source-Dateien, Submodules, Tool-Binaries, Saves oder Emulator States.
- `git ls-files 05_builds 04_private_roms 03_tools/releases` bleibt leer.

## Danach

Naechster minimaler Folgebranch:

```text
analysis/upr-fvx-cfru-dpe-p1-static-gift-write-diagnostics
```

Ziel:

- Nach bestaetigter Gen9-Wild-Coverage P1 Static-/Gift-Species-only Diagnose wieder aufnehmen.
- Weiterhin keine Learnset-, Trainer-, Palette-, Day/Night- oder Nullslot-Fixes im selben Branch.
- ROM-/Build-Artefakte nicht committen.

## Offene Randomizer-Themen

- Bad Egg Diagnose
- Static/Gift
- Trainer
- Learnsets/Movesets
- TM/Tutor/Abilities
- CFRU Day/Night Custom Wild Tables
- Ironmon-Tracker-Tests

## Nicht tun

- keine ROMs bewegen
- keine ROMs lesen, kopieren oder aendern
- keine Saves oder Emulator States anfassen
- keine Builds starten oder committen
- keine Randomizer-Laeufe starten
- keine Randomizer-JARs oder Tool-Binaries anfassen oder committen
- keine Codeaenderungen in `02_external/**`
- keine Submodule-Aenderungen
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine GitHub-Tokens oder lokale Secrets dokumentieren

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
