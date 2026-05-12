# Next Steps

## Aktueller Arbeitsblock

PokedexOrder-/Count-Quellenmodell abschliessen.

Aktueller Branch:

```text
analysis/upr-fvx-cfru-dpe-pokedex-order-model
```

Zieldokumente:

```text
01_docs/compat/upr-fvx-cfru-dpe-pokedex-order-model.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
01_docs/references/source-index.md
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `01_docs/compat/upr-fvx-cfru-dpe-pokedex-order-model.md`
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
docs: model CFRU DPE PokedexOrder handling
```

4. Branch pushen und Workspace-PR nach `main` erstellen.

## Danach

Naechster minimaler Fixbranch:

```text
noch festzulegen
```

Ziel:

- Nur fuer konservativ erkannte CFRU/DPE-BPRE-Hacks die `PokedexOrder`-Count-Kappung ersetzen.
- `PokemonCount` kurzfristig aus `PokemonNames` plus BaseStats-Sanity ableiten.
- `PokedexOrder` nicht als Count-Quelle nutzen, solange kein korrektes DPE/CFRU-Dex-Mapping geladen wird.
- Moveset-Pointer-Heuristik separat lassen; keine Static-/Gift-Fixes, keine Learnset-Fixes und keine ROM-/Build-Artefakte committen.

## Fix-Reihenfolge

P0: GenRestrictions / finaler Gen4+ Allowed-Pool. Erledigt und post-merge bestaetigt.

P0b: Gen3/CFRU-DPE-Wild-Write-Mapping fuer interne Species-Identitaet. Erledigt und post-merge bestaetigt.

P1: Species-Schreibpfade. Analyse erledigt; Starter-Write-Fix ist als UPR-FVX PR #6 gemerged und diagnostisch bestaetigt. Static/Gifts und Trainer-Species bleiben pausiert, bis ein CFRU/DPE-spezifischer Count-Fix Gen7-Gen9-Species sichtbar laedt.

P2: CFRU Day/Night Custom Wild Tables. Separat nach P1-Schreibpfad-Diagnose.

P3: Nullslot-`<unknown>` mit `rawInternalSpeciesId=0`.

P4: BizHawk/Ironmon Tracker/RAM-Mapping.

## Nicht tun

- keine ROMs bewegen
- keine ROMs lesen, kopieren oder aendern
- keine Saves oder Emulator States anfassen
- keine Builds committen
- keine Randomizer-JARs oder Tool-Binaries anfassen oder committen
- keine Codeaenderungen in `02_external/**`
- keine weiteren Wild-Write- oder Encounter-Fixes in diesem Branch
- keine Gen9-Coverage-Fixes in diesem Branch
- keine Day/Night-Wild-Fixes
- keine Swarm-, Roamer-, DexNav- oder Raid-Fixes
- keine Nullslot-Fixes
- keine Trainer-/Starter-/Static-/Evolution-/Learnset-/TM-/Tutor-/Ability-Fixes
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
