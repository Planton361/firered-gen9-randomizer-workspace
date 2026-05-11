# Next Steps

## Aktueller Arbeitsblock

Read-only CFRU/DPE-UPR-FVX-Kompatibilitaetsmodell dokumentieren.

Aktueller Branch:

```text
analysis/cfru-dpe-upr-fvx-compatibility-model
```

Zieldokument:

```text
01_docs/compat/cfru-dpe-upr-fvx-compatibility-model.md
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `01_docs/compat/cfru-dpe-upr-fvx-compatibility-model.md`
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
docs: model CFRU DPE UPR-FVX compatibility
```

4. Branch pushen und Workspace-PR nach `main` vorbereiten.

## Danach

Naechster minimaler UPR-FVX-Fixbranch:

```text
compat/upr-fvx-cfru-dpe-gen-restrictions
```

Ziel:

- Nur die Settings-/Restriction-Begrenzung fuer erweiterte CFRU/DPE-BPRE-Hacks korrigieren.
- Nach PR #3 soll der finale Wild-Randomizer-Pool Gen4+-Species enthalten koennen.
- Keine Species-Identity-, Trainer-, Starter-, Evolution-, Learnset-, Nullslot- oder Day/Night-Wild-Tabellen-Fixes vermischen.
- Danach denselben Gen4+-Wild-Pool-Diagnoselauf wiederholen.

## Fix-Reihenfolge

P0: GenRestrictions / finaler Gen4+ Wild-Pool.

P1: Trainer, Starters, Evolutions, Learnsets und TM/Tutor-Kompatibilitaet.

P2: CFRU Day/Night Custom Wild Tables.

P3: Nullslot-`<unknown>` mit `rawInternalSpeciesId=0`.

P4: BizHawk/Ironmon Tracker/RAM-Mapping.

## Nicht tun

- keine ROMs bewegen
- keine ROMs lesen, kopieren oder aendern
- keine Saves oder Emulator States anfassen
- keine Builds starten oder committen
- keine Randomizer-JARs oder Tool-Binaries anfassen oder committen
- keine Codeaenderungen in `02_external/**` in diesem Analysebranch
- keinen GenRestrictions-Fix in diesem Branch
- keine Day/Night-Wild-Fixes
- keine Nullslot-Fixes
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` bzw. eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine Installationen erzwingen
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen
- keine parallelen Agenten auf demselben Branch einsetzen

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
