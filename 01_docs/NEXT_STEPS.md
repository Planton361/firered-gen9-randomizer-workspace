# Next Steps

## Aktueller Arbeitsblock

Read-only Diagnose der CFRU/DPE Encounter-Systeme nach abgeschlossenem P0 abschliessen.

Aktueller Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-encounter-systems
```

Zieldokumente:

```text
01_docs/compat/cfru-dpe-encounter-systems-model.md
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `01_docs/compat/cfru-dpe-encounter-systems-model.md`
   - `01_docs/SESSION_STATE.md`
   - `01_docs/NEXT_STEPS.md`
   - `00_project-control/roadmap/roadmap-status.md`
   - `01_docs/references/source-index.md`
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
docs: model CFRU DPE encounter systems
```

4. Branch pushen und Workspace-PR nach `main` vorbereiten.

## Danach

Naechster minimaler Diagnosebranch:

```text
analysis/upr-fvx-cfru-dpe-p1-species-write-paths
```

Ziel:

- Trainer, Starters, Static Pokemon, Evolutions, Learnsets und verwandte Species-Schreibpfade fuer erweiterte CFRU/DPE-BPRE-Hacks getrennt diagnostizieren.
- Fokus: interne Species-ID vs. Dex-/Pokedex-ID und `pokedexToInternal[Species.number()]`-Risiken.
- Der Folgeblock darf keine CFRU-Day/Night-Wildtables, Swarms, DexNav, Raids oder Nullslot-Logik vermischen.
- Erst nach Diagnose entscheiden, welche P1-Fixbranches klein und sicher sind.

## Fix-Reihenfolge

P0: GenRestrictions / finaler Gen4+ Allowed-Pool. Erledigt und post-merge bestaetigt.

P0b: Gen3/CFRU-DPE-Wild-Write-Mapping fuer interne Species-Identitaet. Erledigt und post-merge bestaetigt.

P1: Trainer, Starters, Evolutions, Learnsets und TM/Tutor-Kompatibilitaet.

P2: CFRU Day/Night Custom Wild Tables. Separat nach P1-Schreibpfad-Diagnose.

P3: Nullslot-`<unknown>` mit `rawInternalSpeciesId=0`.

P4: BizHawk/Ironmon Tracker/RAM-Mapping.

## Nicht tun

- keine ROMs bewegen
- keine ROMs lesen, kopieren oder aendern
- keine Saves oder Emulator States anfassen
- keine Builds committen
- keine Randomizer-JARs oder Tool-Binaries anfassen oder committen
- keine Codeaenderungen in `02_external/**` in diesem Workspace-Dokumentationscommit
- keine weiteren Wild-Write- oder Encounter-Fixes in diesem Branch
- keine Day/Night-Wild-Fixes
- keine Swarm-, Roamer-, DexNav- oder Raid-Fixes
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
