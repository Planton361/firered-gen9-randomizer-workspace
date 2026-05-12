# Next Steps

## Aktueller Arbeitsblock

Bad-Egg-Eintraege im bestaetigten CFRU/DPE-Gen9-Wild-Log diagnostizieren.

Aktueller Branch:

```text
analysis/upr-fvx-cfru-dpe-wild-bad-egg-diagnostics
```

Zieldokumente:

```text
08_tests/randomizer/upr-fvx-cfru-dpe-wild-bad-egg-diagnostics.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `08_tests/randomizer/upr-fvx-cfru-dpe-wild-bad-egg-diagnostics.md`
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
docs: diagnose CFRU DPE wild bad egg entries
```

4. Branch pushen und Workspace-PR nach `main` erstellen.

## Diagnosebefund

- Der lokale Wild-only-Lauf mit Seed `274269061345319` reproduziert `saveSuccessful=true`.
- Coverage bleibt stabil: `PokemonCount=1439`, `speciesList.size=1415`, `maxSpeciesIdentityNumber=1439`, Gen7/8/9 sichtbar.
- `<unknown>` bleibt `0`.
- `Bad Egg=12`.
- Alle `12` `Bad Egg`-Eintraege liegen in `Area #174 - ALTERING CAVE Grass/Cave (rate=5)`, Slots 1-12.
- DPE/CFRU definieren `SPECIES_EGG=0x19C`, und die DPE-Namensquelle zeigt fuer diesen Slot `Bad Egg`.
- FVX bannt im Gen3/FRLG-Wild-Pfad aktuell nur Unown; `SPECIES_EGG` wird nicht explizit aus dem Wild-Allowed-Pool entfernt.

Wahrscheinlichste Ursache:

```text
SPECIES_EGG gelangt als regulaere Species in den CFRU/DPE-Wild-Allowed-Pool.
```

## Danach

Naechster minimaler Folgebranch:

```text
compat/upr-fvx-cfru-dpe-wild-banned-special-species
```

Ziel:

- CFRU/DPE-spezifisch `SPECIES_NONE`, `SPECIES_EGG` und belegte Dummy-/Gap-Species aus Wild-Replacement-Pools entfernen.
- Vanilla/normal Gen3 unveraendert lassen.
- Kein Static/Gift-, Trainer-, Learnset-, Palette-, Day/Night- oder allgemeiner Gen3-Fix im selben Branch.

Optionaler Vorlauf:

- Ein kleiner UPR-FVX-Diagnosebranch kann vor dem Fix Wild-Replacement-Roh-IDs loggen, falls ein wasserdichter `Bad Egg -> SPECIES_EGG=0x19C`-Nachweis im PR gewuenscht ist.

## Fix-Reihenfolge

P0: GenRestrictions / finaler Gen4+ Allowed-Pool. Erledigt und post-merge bestaetigt.

P0b: Gen3/CFRU-DPE-Wild-Write-Mapping fuer interne Species-Identitaet. Erledigt und post-merge bestaetigt.

Gen9-Coverage: SpeciesCount, defensiver Palette-Load, Lazy-Trainer-Movesets und Skip-Unchanged-Palette-Save sind in UPR-FVX `compat/firered-gen9-cfru-dpe` gemerged und im Post-Merge-Wild-Smoke bestaetigt. Wild-only Save/Log laeuft mit `PokemonCount=1439`, Gen7/8/9-Wild-Beispielen und `<unknown>=0`.

P1: Species-Schreibpfade. Analyse erledigt; Starter-Write-Fix ist als UPR-FVX PR #6 gemerged und diagnostisch bestaetigt. Static/Gifts sind jetzt der naechste minimale Diagnosepfad.

Learnsets/Movesets: Lazy-Trainer-Movesets ist gemerged und entblockt Wild-only Save. Voller DPE/CFRU-`gLevelUpLearnsets`-Support bleibt ein eigener Folgeblock.

Palette-Save: Skip-Unchanged-Palette-Save ist gemerged und post-merge bestaetigt. CFRU/DPE-Palette-Randomization bleibt partial/unsupported.

Bad-Egg-Folgeauffaelligkeit: Die Diagnose zeigt `SPECIES_EGG=0x19C` als wahrscheinlichsten Allowed-Pool-Kandidaten. Naechster Schritt ist ein CFRU/DPE-spezifischer Special-Species-Wild-Ban.

P2: CFRU Day/Night Custom Wild Tables. Separat nach P1-Schreibpfad-Diagnose.

P3: Nullslot-`<unknown>` mit `rawInternalSpeciesId=0`. Im aktuellen Post-Merge-Wild-Smoke bleibt `<unknown>=0`.

P4: BizHawk/Ironmon Tracker/RAM-Mapping.

## Nicht tun

- keine ROMs bewegen
- keine ROMs lesen, kopieren oder aendern, ausser explizit freigegebene lokale Smoke-Laeufe unter `05_builds/**`
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
