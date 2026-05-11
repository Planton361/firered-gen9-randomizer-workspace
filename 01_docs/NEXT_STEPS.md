# Next Steps

## Aktueller Arbeitsblock

P0-GenRestrictions-Fix fuer erweiterte CFRU/DPE-BPRE-Hacks abschliessen und diagnostisch dokumentieren.

Aktueller Branch:

```text
analysis/upr-fvx-cfru-dpe-gen-restrictions
```

Zieldokumente:

```text
08_tests/randomizer/upr-fvx-cfru-dpe-gen-restrictions-diagnostics-run.md
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `08_tests/randomizer/upr-fvx-cfru-dpe-gen-restrictions-diagnostics-run.md`
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
docs: record CFRU DPE gen restrictions diagnostics
```

4. Branch pushen und Workspace-PR nach `main` vorbereiten.

## Danach

Naechster minimaler UPR-FVX-Fixbranch:

```text
compat/upr-fvx-cfru-dpe-wild-internal-species-write
```

Ziel:

- Gen3/CFRU-DPE-Wild-Encounter-Schreibpfade pruefen, die aktuell `pokedexToInternal[enc.getSpecies().getNumber()]` nutzen.
- Fuer erweiterte BPRE-Hacks soll die interne Species-Identitaet beim Schreiben/Reload erhalten bleiben.
- Der Fix darf keine CFRU-Day/Night-Wildtables, Nullslot-Logik oder Trainer-/Starter-/Evolution-/Learnset-/TM-/Tutor-Themen vermischen.
- Danach denselben Wild-Diagnoselauf wiederholen und sichtbare Gen4+-Wild-Encounter pruefen.

## Fix-Reihenfolge

P0: GenRestrictions / finaler Gen4+ Allowed-Pool.

P0b: Gen3/CFRU-DPE-Wild-Write-Mapping fuer interne Species-Identitaet.

P1: Trainer, Starters, Evolutions, Learnsets und TM/Tutor-Kompatibilitaet.

P2: CFRU Day/Night Custom Wild Tables.

P3: Nullslot-`<unknown>` mit `rawInternalSpeciesId=0`.

P4: BizHawk/Ironmon Tracker/RAM-Mapping.

## Nicht tun

- keine ROMs bewegen
- keine ROMs lesen, kopieren oder aendern
- keine Saves oder Emulator States anfassen
- keine Builds committen
- keine Randomizer-JARs oder Tool-Binaries anfassen oder committen
- keine weiteren Codeaenderungen in `02_external/**` in diesem Workspace-Dokumentationscommit
- keinen weiteren GenRestrictions-Fix in diesem Branch
- keine Day/Night-Wild-Fixes
- keine Nullslot-Fixes
- keine Trainer-/Starter-/Evolution-/Learnset-/TM-/Tutor-Fixes
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
