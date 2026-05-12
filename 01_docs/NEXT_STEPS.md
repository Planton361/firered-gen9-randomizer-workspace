# Next Steps

## Aktueller Arbeitsblock

P1 Static/Gift Species-only Diagnose auf Gen9-Wild-sauberem Stand.

Aktueller Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-static-gift-species-only
```

Zieldokumente:

```text
08_tests/randomizer/021_p1_static_gift_species_only.md
08_tests/randomizer/README.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `08_tests/randomizer/021_p1_static_gift_species_only.md`
   - `08_tests/randomizer/README.md`
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
docs: diagnose CFRU DPE static gift species only
```

4. Branch pushen und Workspace-PR nach `main` erstellen.

## Diagnosebefund

- Workspace-Submodule `02_external/upr-fvx` steht auf `0f127e9bb9a5c47306fe1f2af11e8e9fe1802717`.
- Static/Gift-only Settings mit Seed `274269061345323`.
- Species-Coverage bleibt vollstaendig: `PokemonCount=1439`, `speciesList.size=1415`.
- Static/Gift-Pool: `staticPool.size=1414`, Gen1-Gen9 enthalten.
- Pick-Pfad: `pickedGen4plus=18`, `pickedGen7plus=8`.
- CLI meldet `Randomized successfully!`, erzeugt aber nur ein leeres 3-Byte-Log und keine Output-ROM.
- Direkte `GameRandomizer.Results`: `saveSuccessful=false`.
- Blocker: vier `<null>`-Static-Eintraege im Static/Roamer-/hardcoded-FRLG-Scope.

## Danach

Naechster minimaler Folgebranch:

```text
compat/upr-fvx-cfru-dpe-static-gift-scope-and-write
```

Ziel:

- Static/Gift-, Roamer- und hardcoded-FRLG-Eintraege sauber klassifizieren.
- Null-Species aus dem normalen Static/Gift-Randomizer-Pfad ausklammern oder korrekt modellieren.
- Echte Static/Gift-Species fuer erweiterte CFRU/DPE-BPRE-Hacks ueber interne SpeciesSet-Identitaet schreiben.
- Danach denselben Seed erneut mit Reload-/Log-Beweis pruefen.

Offene Folgethemen (separat, nicht in diesem Branch):

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
