# Next Steps

## Aktueller Arbeitsblock

P1 Trainer Held Items lazy Moveset-/Learnset-Load fuer CFRU/DPE Gen9-BPRE.

Aktueller Workspace-Branch:

```text
compat/upr-fvx-cfru-dpe-trainer-held-items-lazy-movesets
```

UPR-FVX-Branch:

```text
compat/upr-fvx-cfru-dpe-trainer-held-items-lazy-movesets
```

Zieldokumente:

```text
08_tests/randomizer/028_trainer_held_items_lazy_movesets_diagnostics.md
08_tests/randomizer/README.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
01_docs/references/tool-manifest.md
```

## Naechste Schritte in diesem Block

1. UPR-FVX-Checks abschliessen:

```sh
cd 02_external/upr-fvx
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
cd ../..
```

2. Workspace-Checks abschliessen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

3. Workspace-Commit erstellen:

```text
docs: record trainer held items fix diagnosis
```

4. Branches pushen und PRs erstellen:

- UPR-FVX PR gegen `Planton361/universal-pokemon-randomizer-fvx`
- Workspace PR gegen `Planton361/firered-gen9-randomizer-workspace` mit explizitem `--repo`

## Diagnosebefund

- UPR-FVX-Basis: `18766c4986db091d1e669c71302aa295195b039b`.
- UPR-FVX-Fix: `3864ad0e7efda4ed8a329fb22edb3a28db1040e8`.
- Trainer Held Items-only Settings mit Seed `274269061345323`.
- Trainer-Held-Item-Pool ist sichtbar: `trainerHeldItemPool.size=52`.
- Trainer-Load funktioniert: `trainers=255`, `trainerPokemon=481`, `nullSpecies=0`.
- Vor Randomization: `before.heldItemEntries=0`, `before.noItemEntries=481`.
- Nach Randomization: `after.heldItemEntries=481`, `after.noItemEntries=0`.
- Nach Reload: `reload.heldItemEntries=481`, `reload.noItemEntries=0`.
- `saveSuccessful=true`; Output-ROM entsteht.
- `logSuccessful=true`; Direct Log ist nicht leer und enthaelt den Trainer-Pokemon-Abschnitt.
- `Bad Egg` und `<unknown>` wurden im Log nicht beobachtet.
- Write/Reload ist stabil: `writeReloadCompared=481`, `writeReloadMismatches=0`.
- Trainer Held Items-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand jetzt P1-supported.

## Danach

Naechster minimaler Folgebranch nach Review/Merge:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-only
```

Ziel:

- Trainer-Movesets-only separat diagnostizieren
- keine Trainer-Held-Items-, Trainer-Species-, Learnset-, TM-/Tutor-, Ability-, Wild-, Starter-, Static/Gift-, Evolution- oder Palette-Fixes im selben Branch

Offene Folgethemen:

- Trainer-Movesets-only Diagnose
- Sensible movebasierte Trainer-Held-Item-Auswahl gegen CFRU/DPE-Learnsets
- Learnsets/Movesets
- TM/Tutor/Abilities
- CFRU Day/Night Custom Wild Tables
- Ironmon-Tracker-Tests

## Nicht tun

- keine ROMs bewegen
- keine ROMs committen oder in ChatGPT hochladen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine CFRU-/DPE-Aenderungen
- keine Wild-, Starter-, Static/Gift-, Trainer-Species-, Learnset-, TM-/Tutor-, Ability-, Palette- oder Day/Night-Fixes in diesem Branch
- keine breiten Refactors
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
