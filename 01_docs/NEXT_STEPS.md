# Next Steps

## Aktueller Arbeitsblock

P1 Trainer Held Items-only Diagnose fuer CFRU/DPE Gen9-BPRE.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-held-items-only
```

UPR-FVX-Stand:

```text
18766c4986db091d1e669c71302aa295195b039b
```

Zieldokumente:

```text
08_tests/randomizer/027_p1_trainer_held_items_only.md
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
test: document trainer held items only diagnosis
```

3. Branch pushen und PR erstellen:

```sh
git push -u origin analysis/upr-fvx-cfru-dpe-p1-trainer-held-items-only
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head analysis/upr-fvx-cfru-dpe-p1-trainer-held-items-only --title "test: document trainer held items only diagnosis" --body-file /tmp/pr-body-trainer-held-items.md
```

## Diagnosebefund

- UPR-FVX-Basis: `18766c4986db091d1e669c71302aa295195b039b`.
- Trainer Held Items-only Settings mit Seed `274269061345323`.
- Itemdaten laden: `items.totalSlots=1375`, `items.nonNull=374`, `items.allowed=244`, `items.nonBad=181`.
- Trainer-Held-Item-Pool ist sichtbar: `trainerHeldItemPool.size=52`.
- Trainer-Load funktioniert: `trainers=255`, `trainerPokemon=481`, `nullSpecies=0`.
- Vor Randomization: `before.heldItemEntries=0`, `before.noItemEntries=481`.
- Der Lauf scheitert vor Save/Log in `TrainerPokemonRandomizer.randomizeTrainerHeldItems()`.
- Fehlerpfad: `Gen3RomHandler.getMovesLearnt()` -> `readPointer()` -> `No valid pointer at 0x25e49c`.
- `saveSuccessful=false`; keine Output-ROM entsteht.
- `logSuccessful=true`, aber `directLogBytes=0` und `logNonEmpty=false`, weil der Log-Pfad nicht erreicht wird.
- `Bad Egg` und `<unknown>` werden im Log nicht erreicht.
- Write/Reload ist nicht pruefbar: `writeReloadCompared=0`, `writeReloadMismatches=not run`.
- Trainer Held Items-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand noch nicht P1-supported.

## Danach

Naechster minimaler Folgebranch nach Review/Merge:

```text
compat/upr-fvx-cfru-dpe-trainer-held-items-lazy-movesets
```

Ziel:

- Trainer-Held-Items-only entblocken
- `randomizeTrainerHeldItems()` soll `getMovesLearnt()` nur laden, wenn `resetMoves` oder sensible movebasierte Itemauswahl es tatsaechlich braucht
- keine Trainer-Species-, Trainer-Moveset-, Learnset-, TM-/Tutor-, Ability-, Wild-, Starter-, Static/Gift-, Evolution- oder Palette-Fixes im selben Branch

Offene Folgethemen:

- Trainer-Held-Items-Fix
- Trainer-Movesets-only Diagnose
- Learnsets/Movesets
- TM/Tutor/Abilities
- CFRU Day/Night Custom Wild Tables
- Ironmon-Tracker-Tests

## Nicht tun

- keine ROMs bewegen
- keine ROMs committen oder in ChatGPT hochladen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine Aenderungen an `02_external/**` in diesem Diagnosebranch
- keine CFRU-/DPE-Aenderungen
- keine Wild-, Starter-, Static/Gift-, Trainer-Species-, Trainer-Moveset-, Learnset-, TM-/Tutor-, Ability-, Palette- oder Day/Night-Fixes in diesem Branch
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
