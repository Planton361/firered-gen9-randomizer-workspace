# Next Steps

## Aktueller Arbeitsblock

UPR-FVX/CFRU/DPE-Species-Pool auf `analysis/upr-fvx-cfru-dpe-species-pool` read-only analysieren und dokumentieren.

## Nächste Schritte

1. `08_tests/randomizer/upr-fvx-cfru-dpe-species-pool-analysis.md` reviewen.
2. Lokal im echten Workspace die Git-/Submodule-Pruefung nachziehen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
```

3. Analysebefund fachlich pruefen:
   - `Gen3RomHandler` nutzt fuer BPRE-Hacks Heuristiken statt DPE-spezifischer Species-Metadaten.
   - `PokemonCount` kann durch Namen-, Moveset- oder `PokedexOrder`-Plausibilitaetschecks abgeschnitten werden.
   - `generationOf()` im Gen3-Handler ist auf Gen1-3 hardcoded.
   - Der Wild-Randomizer-Pool kommt ueber `RestrictedSpeciesService` und `romHandler.getSpeciesSetInclFormes()`.
   - `<unknown>` im Wild-Log spricht fuer ein Species-ID-/Count-/Mapping-Problem.
4. Branch reviewen, committen/pushen bzw. PR nach `main` fuehren. PR nicht mergen.

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

`analysis/log-cfru-dpe-species-diagnostics`

Ziel:

- Im UPR-FVX-Fork `Planton361/universal-pokemon-randomizer-fvx` nur Diagnose-Logging/Analyseausgabe ergänzen.
- Noch keine funktionale Randomizer-Aenderung vornehmen.
- Zu protokollieren:
  - erkannter `PokemonCount`
  - `pokedexCount`
  - maximale interne Species-ID
  - maximale Pokedex-/Species-Nummer
  - `speciesList.size()`
  - Counts pro `Species.generation`
  - Beispiele fuer Species `> 386`
  - Roh-Species-ID fuer Wild-Log-`<unknown>` inklusive Area/Encounter-Type
- Danach denselben lokalen CFRU/DPE-Teststand erneut laden und Logauszug in `08_tests/randomizer/` dokumentieren, ohne ROMs, Builds oder Tool-Binaries zu committen.

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
