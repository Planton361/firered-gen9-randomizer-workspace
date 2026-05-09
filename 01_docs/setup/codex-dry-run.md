# Codex Dry Run

## Ziel

Dieser Dry Run prüft, ob die dokumentierten Codex-Regeln praktisch nutzbar sind.

Der Dry Run verändert keine ROMs, Saves, Builds, Tool-Binaries, externen Repos oder privaten Dateien.

## Ausgangslage

Vorhandene Governance-Dateien:

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `01_docs/setup/git-workflow.md`
- `01_docs/setup/fork-strategy.md`
- `01_docs/setup/codex-workflow.md`
- `01_docs/setup/security-rules.md`
- `01_docs/setup/workspace-rebuild.md`
- `01_docs/setup/codex-dry-run.md`

Vorhandene Safety-Scripts:

- `07_scripts/bootstrap/bootstrap-workspace.ps1`
- `07_scripts/bootstrap/check-git-safety.ps1`
- `07_scripts/bootstrap/check-remotes.ps1`

## Dry-Run-Scope

Codex soll nur Dokumentation prüfen.

Erlaubte Dateien:

- `01_docs/setup/codex-dry-run.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `00_project-control/roadmap/roadmap-status.md`

Nicht erlaubt:

- ROMs lesen, kopieren, ändern oder committen
- Saves oder Emulator States anfassen
- Builds starten oder committen
- Tool-Binaries anfassen
- externe Repos klonen
- Forks anlegen
- Änderungen direkt auf `main`
- private Pfade, Tokens, `.env` oder Secrets veröffentlichen

## Standardprompt für Codex

```text
Lies zuerst README.md, AGENTS.md, 01_docs/PROJECT_BRIEF.md, 01_docs/SESSION_STATE.md, 01_docs/NEXT_STEPS.md und die Setup-Dokumente in 01_docs/setup/.

Aufgabe: Prüfe, ob die Repo-Governance-Dokumentation konsistent, verständlich und praktisch nutzbar ist.

Erlaubte Änderung: Nur kleine Dokumentationskorrekturen in codex-dry-run.md, SESSION_STATE.md, NEXT_STEPS.md und roadmap-status.md.

Verboten: ROMs, Saves, Builds, Tool-Binaries, externe Downloads, Forks, private Dateien, Secrets und Änderungen direkt auf main.

Abgabeformat: Summary, geänderte Dateien, Checks/Tests, Risiken/Annahmen, nächster minimaler Schritt.
```

## Erwartete Prüfpunkte

1. Sind Git-, Fork-, Codex- und Security-Regeln widerspruchsfrei?
2. Ist klar, dass `main` stabil bleibt?
3. Ist klar, dass Arbeitsbranches Pflicht sind?
4. Ist klar, dass ROMs, Saves, Builds, Tool-Binaries und Secrets ausgeschlossen sind?
5. Ist klar, dass externe Repos erst nach Dokumentation geklont oder geforkt werden?
6. Sind die PowerShell-Kommandos Windows-tauglich?
7. Sind die Bootstrap-/Safety-Scripts für einen neuen Workspace verständlich?

## Lokale Checks

```powershell
pwsh -File .\07_scripts\bootstrap\check-remotes.ps1
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
git status --short
git diff --stat
```

## Ergebnis dieses Dry Runs

Durchgeführt am 2026-05-10 auf Branch `setup/codex-dry-run-results`.

Ergebnis:

- Git-, Fork-, Codex- und Security-Regeln sind inhaltlich widerspruchsfrei.
- `main` ist durchgängig als stabiler Branch beschrieben.
- Arbeitsbranches sind für Änderungen durchgängig Pflicht.
- ROMs, Saves, Builds, Tool-Binaries, private Dateien und Secrets sind klar ausgeschlossen.
- Externe Repos werden erst nach dokumentierter Entscheidung und Manifest-Eintrag geklont oder geforkt.
- Die dokumentierten Kommandos sind PowerShell-/Windows-tauglich und verwenden keine Bash-Brace-Expansion.
- Bootstrap- und Safety-Scripts sind für einen neuen Workspace verständlich: Bootstrap legt lokale Ordner an, `check-remotes.ps1` prüft `origin`/`upstream`, `check-git-safety.ps1` prüft Branch und verbotene Dateien.

Kleine Statuskorrekturen wurden in den freigegebenen Dokumenten vorgenommen. Bestehende `.idea`-Arbeitsbaumänderungen gehören nicht zum Dry Run und bleiben unangetastet.

## Nächster Schritt nach Dry Run

Wenn der Dry Run erfolgreich ist:

- PR nach `main`
- danach erster read-only Analyseblock für externe Quellen
- weiterhin keine ROM-/Build-Arbeit
