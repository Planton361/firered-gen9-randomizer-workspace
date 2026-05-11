# Next Steps

## Aktueller Arbeitsblock

Gen4+-Wild-Pool nach UPR-FVX PR #3 mit All-Gens-Settings diagnostisch pruefen.

## Nächste Schritte

1. Diagnoseprotokoll `08_tests/randomizer/upr-fvx-gen4plus-wild-pool-diagnostics.md` reviewen.
2. UPR-FVX-Folgefix fuer Generation-Restrictions vorbereiten:
   - `compat/upr-fvx-cfru-dpe-gen-restrictions`
3. Lokal die Git-/Submodule-Pruefung nachziehen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
```

4. Danach denselben Gen4+-Wild-Pool-Diagnoselauf wiederholen.

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

`compat/upr-fvx-cfru-dpe-gen-restrictions`

Ziel:

- Im UPR-FVX-Fork die Settings-/Restriction-Begrenzung fuer erweiterte CFRU/DPE-BPRE-Hacks korrigieren.
- Keine Species-Identity-, Nullslot- oder Day/Night-Wild-Tabellen-Fixes vermischen.
- Danach erneut pruefen, ob Gen4+-Species in der finalen Wild-Auswahl landen.

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
