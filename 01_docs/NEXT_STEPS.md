# Next Steps

## Aktueller Arbeitsblock

P1 Static/Gift Scope und interner Species-Write fuer CFRU/DPE.

Aktueller Workspace-Branch:

```text
compat/upr-fvx-cfru-dpe-static-gift-scope-and-write
```

UPR-FVX-Branch:

```text
compat/upr-fvx-cfru-dpe-static-gift-scope-and-write
```

Zieldokumente:

```text
08_tests/randomizer/022_static_gift_scope_write_diagnostics.md
08_tests/randomizer/README.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
01_docs/references/tool-manifest.md
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
docs: record CFRU DPE static gift fix diagnostics
```

3. Branches pushen und PRs erstellen:

- UPR-FVX PR gegen `Planton361/universal-pokemon-randomizer-fvx`
- Workspace PR gegen `Planton361/firered-gen9-randomizer-workspace` mit explizitem `--repo`

## Diagnosebefund

- UPR-FVX-Commit: `009178e8848b4272e6b8be54a8bf5b2bed34d5f2`.
- Static/Gift-only Settings mit Seed `274269061345323`.
- Species-Coverage bleibt vollstaendig: `PokemonCount=1439`, `speciesList.size=1415`.
- Static/Gift-Pool: `staticPool.size=1414`, Gen1-Gen9 enthalten.
- Direkte `GameRandomizer.Results`: `saveSuccessful=true`, `logSuccessful=true`.
- Output-ROM und nichtleerer Static/Gift-Log entstehen.
- Gen7/8/9 sind im echten Static/Gift-Log sichtbar.
- Null-Sonderfaelle bleiben erhalten: `nullBefore=4`, `nullAfterWrite=4`, `nullReloaded=4`.
- Write/Reload ist stabil: `writeReloadMismatches=0`.

## Danach

Naechster minimaler Folgebranch:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-species-only
```

Ziel:

- Trainer-Species-only mit Gen1-Gen9-Pool diagnostizieren.
- `trainerPokemonToBytes()`-Species-Write separat bewerten.
- Trainer-Movesets, Learnsets, Items, Abilities und EV-Spreads nicht im selben Block fixen.

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
- keine weiteren Codeaenderungen ausserhalb von `02_external/upr-fvx/**`
- keine CFRU-/DPE-Aenderungen
- keine Trainer-, Learnset-, Evolution-, TM-/Tutor-, Ability-, Wild- oder Day/Night-Fixes in diesem Branch
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
