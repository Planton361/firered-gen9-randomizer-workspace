# Next Steps

## Aktueller Arbeitsblock

P1 Evolution-Scope und Species-Write fuer CFRU/DPE.

Aktueller Workspace-Branch:

```text
compat/upr-fvx-cfru-dpe-evolutions-scope-and-write
```

UPR-FVX-Branch:

```text
compat/upr-fvx-cfru-dpe-evolutions-scope-and-write
```

Zieldokumente:

```text
08_tests/randomizer/026_evolutions_scope_write_diagnostics.md
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
docs: record CFRU DPE evolution species fix diagnostics
```

4. Branches pushen und PRs erstellen:

- UPR-FVX PR gegen `Planton361/universal-pokemon-randomizer-fvx`
- Workspace PR gegen `Planton361/firered-gen9-randomizer-workspace` mit explizitem `--repo`

## Diagnosebefund

- UPR-FVX-Basis: `56ec749eca12a8637c20f943b520a9bb6a9d469a`.
- UPR-FVX-Fix: `18766c4986db091d1e669c71302aa295195b039b`.
- Evolution-Species-only Settings mit Seed `274269061345323`.
- Species-Coverage bleibt vollstaendig: `PokemonCount=1439`, `speciesList.size=1415`.
- Evolution-Pool enthaelt Gen1-Gen9: `evolutionPool.size=1414`.
- Interner Source-Index liest `218` Evolution-Eintraege ueber `190` Quell-Species.
- Evolution-Picks erreichen Gen7/8/9: `after.pickedGen7plus=51`.
- `saveSuccessful=true`; Output-ROM entsteht.
- `logSuccessful=true`; CLI-Log ist nicht leer und enthaelt Evolution-Picks aus Gen7/8/9.
- Logger-Fallbacks: zwei Eintraege fuer `unknown item #1732`; kein `<unknown>` im Evolution-Log.
- Ein bestehender `Bad Egg`-Quell-Evolutionseintrag bleibt sichtbar; dieser Branch filtert keine Evolution-Sonder-Species.
- Write/Reload ist stabil: `writeReloadCompared=1414`, `writeReloadMismatches=0`.
- Reload erhaelt Gen8/9-Ziele.
- Evolution-Species-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand jetzt P1-supported.

## Danach

Naechster minimaler Folgebranch nach Review/Merge:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-or-held-items
```

Ziel:

- den naechsten kleinsten P1-Trainer-Folgepfad diagnostizieren
- Trainer-Movesets und Trainer-Held-Items getrennt bewerten, falls die Settings separat steuerbar sind
- keine Evolution-, Wild-, Starter-, Static/Gift-, Learnset-, TM-/Tutor-, Ability- oder Palette-Fixes im selben Block

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
- keine CFRU-/DPE-Aenderungen
- keine Wild-, Starter-, Static/Gift-, Trainer-, Learnset-, TM-/Tutor-, Ability-, Palette- oder Day/Night-Fixes in diesem Branch
- keine Evolution-Methoden-Featurearbeit ausserhalb Species-only Write/Reload und Logging
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
