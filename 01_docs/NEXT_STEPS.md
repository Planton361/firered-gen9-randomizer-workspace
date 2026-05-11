# Next Steps

## Aktueller Arbeitsblock

UPR-FVX/CFRU/DPE Species-Identity- und Generation-Mapping-Fix im UPR-FVX-Fork vorbereiten.

## Nächste Schritte

1. UPR-FVX-Branch `compat/upr-fvx-gen9-generation-mapping` reviewen.
2. Protokoll `08_tests/randomizer/upr-fvx-cfru-dpe-generation-mapping-fix.md` reviewen.
3. Lokal die Git-/Submodule-Pruefung nachziehen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
```

4. Nach Merge/Pin des UPR-FVX-Fixbranches denselben lokalen Diagnose-Lauf erneut ausfuehren und Werte vergleichen:
   - `speciesList.size` soll deutlich ueber `412` liegen.
   - `maxSpeciesIdentityNumber` soll `823` erreichen.
   - Gen4+-Beispiele sollen nicht mehr pauschal Gen3 sein.

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

Nächster empfohlener Arbeitsblock nach dem Fix-PR:

`analysis/upr-fvx-cfru-dpe-generation-mapping-diagnostics`

Ziel:

- Den lokalen CFRU/DPE-Teststand mit dem Generation-Mapping-Fix erneut laden.
- Diagnosewerte vor/nach dem Fix vergleichen.
- `<unknown>`-Nullslots weiterhin separat behandeln; keine Vermischung mit dem Generation-Mapping-Fix.

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
