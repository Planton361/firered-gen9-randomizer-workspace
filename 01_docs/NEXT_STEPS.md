# Next Steps

## Aktueller Arbeitsblock

P1 Evolution-Species-only Diagnose fuer CFRU/DPE.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-evolutions-species-only
```

UPR-FVX-Branch:

```text
compat/upr-fvx-cfru-dpe-trainer-scope-and-write
```

Zieldokumente:

```text
08_tests/randomizer/025_p1_evolutions_species_only.md
08_tests/randomizer/README.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
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
docs: diagnose Gen9 CFRU DPE evolution species only
```

4. Branch pushen und Workspace-PR erstellen:

- Workspace PR gegen `Planton361/firered-gen9-randomizer-workspace` mit explizitem `--repo`

## Diagnosebefund

- UPR-FVX-Basis: `56ec749eca12a8637c20f943b520a9bb6a9d469a`.
- Evolution-Species-only Settings mit Seed `274269061345323`.
- Species-Coverage bleibt vollstaendig: `PokemonCount=1439`, `speciesList.size=1415`.
- Evolution-Pool enthaelt Gen1-Gen9: `evolutionPool.size=1414`.
- Evolution-Picks erreichen Gen7/8/9: `after.pickedGen7plus=43`.
- `saveSuccessful=true`; Output-ROM entsteht.
- CLI-Log ist nicht leer und enthaelt Evolution-Picks aus Gen7/8/9.
- Direct Results meldet `logSuccessful=false` durch `IndexOutOfBoundsException` in `RandomizationLogger.evolutionMethodToString()`.
- Write/Reload ist nicht stabil: `writeReloadCompared=1414`, `writeReloadMismatches=146`.
- Reload verliert Evolution-Eintraege und Gen8/9-Ziele.
- Evolution-Species-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand noch nicht P1-supported.

## Danach

Naechster minimaler Folgebranch nach Review/Merge:

```text
compat/upr-fvx-cfru-dpe-evolutions-scope-and-write
```

Ziel:

- Evolution-Source- und Evolution-Target-Species fuer CFRU/DPE ueber interne SpeciesSet-Identitaet absichern.
- Evolution-Reload ueber interne SpeciesSet-Identitaet bestaetigen.
- Evolution-Logger defensiv gegen nicht aufloesbare Item-/Methoden-ExtraInfos machen.
- Keine Wild-, Starter-, Static/Gift-, Trainer-, Learnset-, TM-/Tutor-, Ability- oder Palette-Fixes im selben Block.

Offene Folgethemen:

- Trainer-Movesets und Trainer-Held-Items
- Learnsets/Movesets
- TM/Tutor/Abilities
- CFRU Day/Night Custom Wild Tables
- Ironmon-Tracker-Tests

## Nicht tun

- keine ROMs bewegen
- keine ROMs committen oder in ChatGPT hochladen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine Codeaenderungen in diesem Diagnosebranch
- keine Aenderungen in `02_external/**`
- keine CFRU-/DPE-Aenderungen
- keine Wild-, Starter-, Static/Gift-, Trainer-, Learnset-, TM-/Tutor-, Ability-, Palette- oder Day/Night-Fixes in diesem Branch
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
