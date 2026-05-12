# Next Steps

## Aktueller Arbeitsblock

CFRU/DPE-Special-Species-Wild-Ban diagnostisch bestaetigen.

Aktueller Branch:

```text
analysis/upr-fvx-cfru-dpe-wild-banned-special-species
```

Zieldokumente:

```text
08_tests/randomizer/upr-fvx-cfru-dpe-wild-banned-special-species-diagnostics.md
08_tests/randomizer/README.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
02_external/upr-fvx
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `08_tests/randomizer/upr-fvx-cfru-dpe-wild-banned-special-species-diagnostics.md`
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
docs: record CFRU DPE wild special species ban diagnostics
```

4. Branch pushen und Workspace-PR nach `main` erstellen.

## Diagnosebefund

- UPR-FVX PR #12 ist offen.
- Der Fix bannt im erkannten CFRU/DPE-Gen9-BPRE-Modus `SPECIES_NONE=0` und `SPECIES_EGG=0x19C` aus dem Wild-Pool.
- Vanilla/normal Gen3 bleiben unveraendert.
- Lokaler Wild-only-Smoke mit Seed `274269061345319`: `saveSuccessful=true`.
- Coverage bleibt stabil: `PokemonCount=1439`, `speciesList.size=1415`, `maxSpeciesIdentityNumber=1439`.
- `Bad Egg` faellt von `12` auf `0`.
- `<unknown>` bleibt `0`.
- `Area #174 - ALTERING CAVE Grass/Cave` enthaelt jetzt `Meowscrada` in allen 12 Slots.

## Danach

Naechster minimaler Folgebranch:

```text
compat/upr-fvx-cfru-dpe-wild-banned-special-species
```

Ziel:

- CFRU/DPE-spezifisch `SPECIES_NONE`, `SPECIES_EGG` und belegte Dummy-/Gap-Species aus Wild-Replacement-Pools entfernen.
- Vanilla/normal Gen3 unveraendert lassen.
- Kein Static/Gift-, Trainer-, Learnset-, Palette-, Day/Night- oder allgemeiner Gen3-Fix im selben Branch.

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
