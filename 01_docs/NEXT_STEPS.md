# Next Steps

## Aktueller Arbeitsblock

P1 Trainer-Species-only Diagnose fuer CFRU/DPE.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-species-only
```

UPR-FVX-Branch:

```text
compat/upr-fvx-cfru-dpe-static-gift-scope-and-write
```

Zieldokumente:

```text
08_tests/randomizer/023_p1_trainer_species_only.md
08_tests/randomizer/README.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
```

## Naechste Schritte in diesem Block

1. Workspace-Checks abschliessen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

2. Workspace-Commit erstellen:

```text
docs: diagnose Gen9 CFRU DPE trainer species only
```

3. Branch pushen und Workspace-PR erstellen:

- Workspace PR gegen `Planton361/firered-gen9-randomizer-workspace` mit explizitem `--repo`

## Diagnosebefund

- UPR-FVX-Commit: `009178e8848b4272e6b8be54a8bf5b2bed34d5f2`.
- Trainer-Species-only Settings mit Seed `274269061345323`.
- Species-Coverage bleibt vollstaendig: `PokemonCount=1439`, `speciesList.size=1415`.
- Trainer-Pool: `trainerPool.size=1414`, Gen1-Gen9 enthalten.
- Trainer-Load: `trainers=255`, `trainerPokemon=481`, `nullSpecies=0`.
- Der Trainer-Pool enthaelt acht Zero-Ability-/Zero-BST-Sonder-Species, darunter `Bad Egg`, zwei Zygarde-Sonderslots und vier Gen9-Ogerpon-Formslots.
- `randomizeTrainerPokes()` erreicht Save/Log nicht und haengt im Stack-Dump in `TrainerPokemonRandomizer.getRandomAbilitySlot()`.
- Output-ROM und Trainer-Log entstehen nicht.
- Write/Reload ist noch nicht pruefbar.

## Danach

Naechster minimaler Folgebranch:

```text
compat/upr-fvx-cfru-dpe-trainer-scope-and-write
```

Ziel:

- Trainer-Species-Scope gegen nicht kampffaehige/Trainer-ungeeignete Sonder-Species absichern oder Ability-Slot-Auswahl defensiv behandeln.
- Danach Trainer-Species-Write/Reload separat bewerten.
- Trainer-Movesets, Learnsets, Items, Ability-Randomization und EV-Spreads nicht im selben Block fixen.

Offene Folgethemen:

- Trainer-Species-Write
- Learnsets/Movesets
- Evolutions
- TM/Tutor/Abilities
- CFRU Day/Night Custom Wild Tables
- Ironmon-Tracker-Tests

## Nicht tun

- keine ROMs bewegen
- keine ROMs committen oder in ChatGPT hochladen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine Codeaenderungen in diesem Analysebranch
- keine CFRU-/DPE-Aenderungen
- keine Trainer-, Learnset-, Evolution-, TM-/Tutor-, Ability-, Wild- oder Day/Night-Fixes in diesem Analysebranch
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
