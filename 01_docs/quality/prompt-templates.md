# Prompt Templates

Dieses Dokument enthält kurze Vorlagen für wiederholbare ChatGPT-/Codex-Arbeitsblöcke.

## Codex-Arbeitspaket

Ziel: Codex bekommt genug Kontext für eine kleine, reviewbare Änderung, aber keine langen Preambles oder starre Plan-Ausgaben.

```text
Arbeitsbranch:
<branch>

Ziel:
<ein klares Ergebnis in 1-2 Sätzen>

Lies zuerst:
- README.md
- AGENTS.md
- 01_docs/PROJECT_BRIEF.md
- 01_docs/SESSION_STATE.md
- 01_docs/NEXT_STEPS.md

Aufgabe:
- <konkreter Schritt 1>
- <konkreter Schritt 2>
- <konkreter Abschluss-/Doku-Schritt>

Suche:
- Nutze `rg` und `rg --files` für Suche und Dateifindung.
- Falls `rg` fehlt, nutze `git ls-files`, `find` oder ein anderes lokales Read-only-Fallback.
- Kopiere keine langen Dateiinhalte in den Prompt; nutze Dateipfade.

Erlaubte Dateien:
- <pfad>
- <pfad>

Stop-Regeln:
- Stoppe, wenn du auf `main` bist.
- Stoppe bei unerwarteten Änderungen im Arbeitsbaum.
- Stoppe, wenn ROMs, Saves, Emulator States, Builds, Tool-Binaries, private Pfade, Secrets, Tokens oder `.env`-Dateien betroffen wären.
- Stoppe, wenn eine Aufgabe externe Repos, Forks, Installationen oder große Refactors braucht, die nicht ausdrücklich freigegeben sind.
- Stoppe, wenn Checks verbotene Artefakte melden.

Arbeitsweise:
- Keine langen Vorabpläne erzwingen.
- Kurze Statusupdates nur bei längeren oder blockierten Schritten.
- Kleine, zusammenhängende Änderungen bevorzugen.
- Nicht parallel andere Agenten/IDEs auf demselben Branch arbeiten lassen.

Checks:
- `git status --short`
- `git diff --stat`
- Falls verfügbar: Safety-Check aus `07_scripts/bootstrap/` ausführen.
- Nur aufgabenspezifische Tests/Checks ergänzen, wenn sie lokal verfügbar und erlaubt sind.

Commit/PR:
- Commit: `<type>: <kurze beschreibung>`
- Push auf den Arbeitsbranch.
- PR nach `main` erstellen, wenn `gh` verfügbar ist.
- PR nicht mergen.

Abgabeformat:
- Summary
- geänderte Dateien
- Checks
- Risiken
- PR-Link oder PR-Befehl
- Handoff-Prompt für den nächsten neuen Chat
```

## Minimaler Codex-Fixprompt

```text
Branch: <branch>

Fixe nur:
<konkretes Problem>

Erlaubte Dateien:
- <pfad>

Nutze `rg`/`rg --files` für Suche.
Stoppe bei unerwarteten Dateien, verbotenen Artefakten oder Bedarf für externe Downloads/Installationen.

Checks:
- `git status --short`
- `git diff --stat`
- <konkreter Check>

Abgabe: Summary, Dateien, Checks, Risiken, PR/Handoff.
```

## Handoff-Prompt

```text
Du arbeitest im Repo Planton361/firered-gen9-randomizer-workspace.

Aktueller Stand:
- Branch: <branch>
- PR: <link oder offen>
- Letzter Commit: <hash oder offen>
- Checks: <ausgeführt/fehlend>

Nächster minimaler Schritt:
<ein konkreter Schritt>

Lies zuerst:
- README.md
- AGENTS.md
- 01_docs/PROJECT_BRIEF.md
- 01_docs/SESSION_STATE.md
- 01_docs/NEXT_STEPS.md

Erlaubte Dateien:
- <pfad>

Verboten:
- keine Änderungen direkt auf main
- keine ROMs, Saves, Emulator States, Builds oder Tool-Binaries anfassen
- keine Secrets oder privaten Pfade veröffentlichen
- keine externen Repos klonen oder Forks anlegen, außer ausdrücklich freigegeben

Abgabeformat:
- Summary
- geänderte Dateien
- Checks
- Risiken
- nächster minimaler Schritt
```
