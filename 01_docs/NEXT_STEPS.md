# Next Steps

## Aktueller Arbeitsblock

P1 CFRU/DPE-Learnset-Modell fuer Trainer Movesets-only fuer CFRU/DPE Gen9-BPRE.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-learnsets-model
```

UPR-FVX-Stand:

```text
3864ad0e7efda4ed8a329fb22edb3a28db1040e8
```

Zieldokumente:

```text
08_tests/randomizer/029_p1_trainer_movesets_only.md
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
docs: document cfru dpe learnsets model
```

3. Branch pushen und PR erstellen:

```sh
git push -u origin analysis/upr-fvx-cfru-dpe-p1-learnsets-model
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head analysis/upr-fvx-cfru-dpe-p1-learnsets-model --title "docs: document cfru dpe learnsets model" --body-file /tmp/pr-body-learnsets-model.md
```

## Diagnosebefund

- UPR-FVX-Basis: `3864ad0e7efda4ed8a329fb22edb3a28db1040e8`.
- Trainer Movesets-only Settings mit Seed `274269061345323`.
- Move-Daten laden: `moves.total=559`.
- Trainer-Load funktioniert: `trainers=255`, `trainerPokemon=481`, `nullSpecies=0`.
- Vor Randomization: `before.movesetEntries=53`, `before.zeroMovePokemon=428`, `before.resetMoves=0`.
- Bestehende Trainer-Moves sind nicht invalid: `before.invalidMoves=0`, `before.unknownNamedMoves=0`.
- Der Lauf scheitert vor Save/Log in `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel()`.
- Fehlerpfad: `Gen3RomHandler.getMovesLearnt()` -> `readPointer()` -> `No valid pointer at 0x25e49c`.
- `saveSuccessful=false`; keine Output-ROM entsteht.
- `logSuccessful=true`, aber `directLogBytes=0` und `logNonEmpty=false`, weil der Log-Pfad nicht erreicht wird.
- `Bad Egg`, `<unknown>` und unknown moves werden im Log nicht erreicht.
- Nach dem Fehlversuch bleibt der Trainer-Moveset-Stand unveraendert: `beforeAfterMoveSignatureChanges=0`.
- Write/Reload ist nicht pruefbar: `writeReloadCompared=0`, `writeReloadMismatches=not run`.
- Trainer Movesets-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand noch nicht P1-supported.

## Danach

Naechster minimaler Folgebranch nach Review/Merge:

```text
analysis/upr-fvx-cfru-dpe-p1-learnsets-model
```

Ziel:

- CFRU/DPE-Level-Up-Learnset- und Moveset-Datenmodell fuer `gLevelUpLearnsets` read-only modellieren
- klaeren, wie `getMovesLearnt()` fuer CFRU/DPE Gen9-BPRE sicher lesen kann
- kein Trainer-Movesets-, Held-Items-, TM-/Tutor-, Ability-, Wild-, Starter-, Static/Gift-, Evolution- oder Palette-Fix im selben Branch

Offene Folgethemen:

- CFRU/DPE-Learnset-Modell
- Trainer-Movesets-Fix
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
- keine Aenderungen an `02_external/**` in diesem Diagnosebranch
- keine CFRU-/DPE-Aenderungen
- keine Wild-, Starter-, Static/Gift-, Trainer-Species-, Trainer-Held-Items-, Trainer-Moveset-, Learnset-, TM-/Tutor-, Ability-, Palette- oder Day/Night-Fixes in diesem Branch
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.

## Naechster empfohlener Arbeitsblock nach 030

Branch:

```text
compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets
```

Ziel:

- Trainer Movesets-only entblocken, ohne breite Refactors.
- In UPR-FVX einen schmal gegateten CFRU/DPE-Learnset-Reader fuer `Gen3RomHandler.getMovesLearnt()` implementieren.
- `gLevelUpLearnsets` als interne Species-ID-Pointertabelle lesen.
- CFRU/DPE-Level-Up-Eintraege als `u16 move` + `u8 level` bis Sentinel `{0, 0xFF}` dekodieren.
- Move-IDs defensiv behandeln, weil CFRU/DPE bis `MOVES_COUNT=992` reicht und FVX in Diagnose 029 nur `moves.total=559` meldete.
- `setMovesLearnt()`/Learnset-Write nicht ausweiten, solange Trainer Movesets-only nur einen Read-Pool braucht.
