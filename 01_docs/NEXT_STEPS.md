# Next Steps

## Aktueller Arbeitsblock

P1 Trainer-Scope und Trainer-Species-Write fuer CFRU/DPE.

Aktueller Workspace-Branch:

```text
compat/upr-fvx-cfru-dpe-trainer-scope-and-write
```

UPR-FVX-Branch:

```text
compat/upr-fvx-cfru-dpe-trainer-scope-and-write
```

Zieldokumente:

```text
08_tests/randomizer/024_trainer_scope_write_diagnostics.md
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
docs: record CFRU DPE trainer species fix diagnostics
```

4. Branch pushen und Workspace-PR erstellen:

- Workspace PR gegen `Planton361/firered-gen9-randomizer-workspace` mit explizitem `--repo`

## Diagnosebefund

- UPR-FVX-Basis: `009178e8848b4272e6b8be54a8bf5b2bed34d5f2`.
- UPR-FVX-Fix-Commit: `56ec749eca12a8637c20f943b520a9bb6a9d469a`.
- UPR-FVX PR: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/14`.
- Trainer-Species-only Settings mit Seed `274269061345323`.
- Species-Coverage bleibt vollstaendig: `PokemonCount=1439`, `speciesList.size=1415`.
- Trainer-Pool vor Filter: `trainerPoolBefore.size=1414`, Gen1-Gen9 enthalten.
- Trainer-Pool nach Filter: `trainerPoolAfter.size=1406`, Gen7/8/9 weiterhin enthalten.
- Acht Zero-Ability-/Zero-BST-Sonder-Species werden ausgeschlossen, darunter `Bad Egg`, zwei Zygarde-Sonderslots und vier Gen9-Ogerpon-Formslots.
- `getRandomAbilitySlot()` ist defensiv gegen Zero-Ability-Species.
- `saveSuccessful=true`, `logSuccessful=true`, Output-ROM und Trainer-Log entstehen.
- Write/Reload ueber interne SpeciesSet-Identitaet: `writeReloadCompared=481`, `writeReloadMismatches=0`.

## Danach

Naechster minimaler Folgebranch nach Review/Merge:

```text
analysis/upr-fvx-cfru-dpe-p1-evolution-species-only
```

Ziel:

- Naechsten P1-Species-Pfad separat diagnostizieren.
- Keine Trainer-Movesets, Learnsets, Items, Ability-Randomization oder EV-Spreads im selben Block fixen.

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
- keine weiteren Codeaenderungen ausserhalb des dokumentierten UPR-FVX-Trainer-Scope-/Write-Fixes
- keine CFRU-/DPE-Aenderungen
- keine Learnset-, Evolution-, TM-/Tutor-, allgemeine Ability-, Wild- oder Day/Night-Fixes in diesem Branch
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
