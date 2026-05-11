# Next Steps

## Aktueller Arbeitsblock

UPR-FVX PR #3 lokal diagnostisch gegen denselben CFRU/DPE-Teststand pruefen.

## Nächste Schritte

1. Diagnoseprotokoll `08_tests/randomizer/upr-fvx-cfru-dpe-generation-mapping-diagnostics-run.md` reviewen.
2. UPR-FVX PR #3 mergen, falls der Befund akzeptiert wird.
3. Lokal die Git-/Submodule-Pruefung nachziehen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
```

4. Danach gezielten Wild-Pool-Test mit Gen4+-Settings planen:
   - Bestaetigen, dass Gen4+-Species in der finalen Wild-Auswahl landen.
   - `<unknown>`-Nullslots weiterhin separat halten.

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

`analysis/upr-fvx-cfru-dpe-wild-pool-gen4-settings`

Ziel:

- Den lokalen CFRU/DPE-Teststand mit gezielten Generation-Restrictions erneut randomisieren.
- Pruefen, ob der Wild-Randomizer Gen4+-Species aus dem erweiterten RomHandler-Pool auswaehlt.
- `<unknown>`-Nullslots weiterhin separat behandeln; keine Day/Night-Wild-Tabellen-Fixes.

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
