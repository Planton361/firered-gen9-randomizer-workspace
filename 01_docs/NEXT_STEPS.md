# Next Steps

## Aktueller Arbeitsblock

UPR-FVX/CFRU/DPE-Species-Diagnose auf Basis von UPR-FVX PR #2 lokal auswerten und dokumentieren.

## Nächste Schritte

1. `08_tests/randomizer/upr-fvx-cfru-dpe-species-diagnostics-run.md` reviewen.
2. Lokal die Git-/Submodule-Pruefung nachziehen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
```

3. Diagnosebefund fachlich pruefen:
   - `PokemonCount=823`, aber `pokedexCount=386` und `speciesList.size=412`.
   - Beispiel-Species `> 386` werden geladen, aber als Gen3 klassifiziert.
   - Eindeutige `<unknown>`-Rohwerte aus dem Gen3-Wild-Leser sind `rawInternalSpeciesId=0`.
4. Workspace-Dokumentationsbranch reviewen, committen/pushen und als PR nach `main` fuehren. PR nicht mergen.

## Nicht tun

- keine ROMs bewegen
- keine ROMs lesen, kopieren oder ändern
- keine Saves oder Emulator States anfassen
- keine Builds starten oder committen
- keine Randomizer-JARs oder Tool-Binaries anfassen oder committen
- keine Codeaenderungen in `02_external/**` in diesem Analysebranch
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` bzw. eindeutig ausgewaehltes Planton361-Repository
- keine Änderungen direkt auf `main`
- keine Installationen erzwingen
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen
- keine parallelen Agenten auf demselben Branch einsetzen

## Danach

Nächster empfohlener Arbeitsblock:

`compat/upr-fvx-gen9-generation-mapping`

Ziel:

- Im UPR-FVX-Fork `Planton361/universal-pokemon-randomizer-fvx` die Generation-Zuordnung fuer Gen4-Gen9-Species korrigieren.
- Keine gleichzeitige Aenderung an `PokemonCount`-Heuristik oder Wild-Pool-ID-Mapping.
- Danach denselben lokalen CFRU/DPE-Teststand erneut mit Diagnoseausgabe laden und vergleichen.
- `<unknown>`-Nullslots separat untersuchen; zuerst klaeren, ob sie legitime leere/sonderfallartige Wild-Slots oder ein Lesefehler sind.

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
