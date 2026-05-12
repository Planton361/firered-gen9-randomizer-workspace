# Next Steps

## Aktueller Arbeitsblock

UPR-FVX Wild-Sonder-Species-Fix im Workspace pinnen.

Aktueller Branch:

```text
docs/pin-upr-fvx-wild-special-species-fix
```

Zieldokumente:

```text
01_docs/references/tool-manifest.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
02_external/upr-fvx
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `01_docs/references/tool-manifest.md`
   - `01_docs/SESSION_STATE.md`
   - `01_docs/NEXT_STEPS.md`
   - `00_project-control/roadmap/roadmap-status.md`
2. Workspace-Checks ausfuehren:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

3. Commit erstellen:

```text
chore: pin UPR FVX wild special species fix
```

4. Branch pushen und Workspace-PR nach `main` erstellen.

## Pin-Stand

- Workspace-Submodule `02_external/upr-fvx` ist auf `0f127e9bb9a5c47306fe1f2af11e8e9fe1802717` gepinnt.
- Submodule-Branch: `compat/upr-fvx-cfru-dpe-wild-banned-special-species`.
- Top-Commit: `0f127e9b compat: ban CFRU DPE special species from wild pool`.
- Der Stand dient als Basis fuer die anschliessende P1 Static/Gift Species-only Diagnose.

## Danach

Naechster minimaler Folgebranch:

```text
analysis/upr-fvx-cfru-dpe-p1-static-gift-write-diagnostics
```

Ziel:

- Static-/Gift-Species-only Schreibpfad auf dem gepinnten Gen9-Wild-sauberen UPR-FVX-Stand diagnostizieren.
- Roamer ausklammern.
- Kein Learnset-, Trainer-, Palette-, Day/Night- oder Nullslot-Fix im selben Branch.

Offene Folgethemen (separat, nicht in diesem Branch):

- Static/Gift
- Trainer
- Learnsets/Movesets
- TM/Tutor/Abilities
- CFRU Day/Night Custom Wild Tables
- Ironmon-Tracker-Tests

## Nicht tun

- keine ROMs bewegen
- keine ROMs committen oder in ChatGPT hochladen
- keine Saves oder Emulator States anfassen
- keine weiteren Builds starten oder committen
- keine weiteren Randomizer-Laeufe starten
- keine Randomizer-JARs oder Tool-Binaries anfassen oder committen
- keine weiteren Codeaenderungen in `02_external/**`
- keine Submodule-Aenderungen
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine Installationen erzwingen
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen
- keine parallelen Agenten auf demselben Branch einsetzen

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
