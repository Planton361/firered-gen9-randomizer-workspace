# Next Steps

## Aktueller Arbeitsblock

CFRU/DPE-Lazy-Trainer-Movesets-Unblocker dokumentieren.

Aktueller Branch:

```text
analysis/upr-fvx-cfru-dpe-lazy-trainer-movesets
```

Zieldokumente:

```text
08_tests/randomizer/upr-fvx-cfru-dpe-lazy-trainer-movesets-diagnostics.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
02_external/upr-fvx
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `08_tests/randomizer/upr-fvx-cfru-dpe-lazy-trainer-movesets-diagnostics.md`
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
docs: record CFRU DPE lazy trainer moveset diagnostics
```

4. Branch pushen und Workspace-PR nach `main` erstellen.

## Danach

Naechster minimaler Folgebranch:

```text
analysis/upr-fvx-cfru-dpe-palette-save-blocker
```

Ziel:

- UPR-FVX PR #8, PR #9 und PR #10 reviewen/mergen, falls noch offen.
- Den neuen nachgelagerten `savePokemonPalettes()`-Blocker bei `no compressed data found at offset 0x16b9c08` separat diagnostizieren.
- Ziel ist nur zu klaeren, warum der defensive Palette-Load den Load entblockt, der Palette-Save aber noch an einer nicht dekomprimierbaren Adresse scheitert.
- Weiterhin keine Static-/Gift-, Trainer-Species-, Count-, Learnset-Loader-, Wild- oder Day/Night-Fixes im selben Branch.
- ROM-/Build-Artefakte nicht committen.

## Fix-Reihenfolge

P0: GenRestrictions / finaler Gen4+ Allowed-Pool. Erledigt und post-merge bestaetigt.

P0b: Gen3/CFRU-DPE-Wild-Write-Mapping fuer interne Species-Identitaet. Erledigt und post-merge bestaetigt.

P1: Species-Schreibpfade. Analyse erledigt; Starter-Write-Fix ist als UPR-FVX PR #6 gemerged und diagnostisch bestaetigt. Static/Gifts und Trainer-Species bleiben pausiert, bis UPR-FVX mit `PokemonCount=1439` wieder vollstaendig bis Save/Log laeuft.

Learnsets/Movesets: der Save-Trainers-Unblocker ist als UPR-FVX PR #10 offen. `trainerPokemonToBytes()` laedt `getMovesLearnt()` nur noch lazy fuer echte `resetMoves`-Faelle. Voller DPE/CFRU-`gLevelUpLearnsets`-Support bleibt ein eigener Folgeblock.

Palette-Save: neuer Folgeblocker nach PR #10 ist `savePokemonPalettes()` mit `no compressed data found at offset 0x16b9c08`; dadurch bleibt `saveSuccessful=false` und es gibt noch keinen nutzbaren Wild-Log.

P2: CFRU Day/Night Custom Wild Tables. Separat nach P1-Schreibpfad-Diagnose.

P3: Nullslot-`<unknown>` mit `rawInternalSpeciesId=0`.

P4: BizHawk/Ironmon Tracker/RAM-Mapping.

## Nicht tun

- keine ROMs bewegen
- keine ROMs lesen, kopieren oder aendern
- keine Saves oder Emulator States anfassen
- keine Builds committen
- keine Randomizer-JARs oder Tool-Binaries anfassen oder committen
- keine Codeaenderungen in `02_external/**` in diesem Workspace-Dokumentationsbranch
- keine weiteren Wild-Write- oder Encounter-Fixes in diesem Branch
- keine weiteren Palette-, Count- oder Gen9-Coverage-Fixes in diesem Branch
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
