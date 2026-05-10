# Prompt Templates

Dieses Dokument enthält kurze Vorlagen für wiederholbare ChatGPT-/Codex-Arbeitsblöcke.

## Codex-Arbeitspaket

```text
Arbeitsbranch:
<branch>

Ziel:
<ein klares Ergebnis>

Lies zuerst:
- README.md
- AGENTS.md
- 01_docs/PROJECT_BRIEF.md
- 01_docs/SESSION_STATE.md
- 01_docs/NEXT_STEPS.md

Aufgabe:
1. <kleiner Schritt>
2. <kleiner Schritt>

Erlaubte Dateien:
- <pfad>

Verboten:
- keine Änderungen direkt auf main
- keine ROMs, Saves, Emulator States, Builds oder Tool-Binaries anfassen
- keine externen Repos klonen oder Forks anlegen, außer ausdrücklich erlaubt
- keine Secrets, Tokens, .env-Dateien oder privaten Pfade veröffentlichen

Definition of Done:
- geänderte Dokumente sind kurz und reviewbar
- SESSION_STATE.md und NEXT_STEPS.md sind aktualisiert
- git status --short, git diff --stat und check-git-safety wurden ausgeführt
- Commit ist erstellt
- PR nach main ist erstellt oder der exakte gh pr create-Befehl ist genannt

Abgabeformat:
- Summary
- geänderte Dateien
- Checks/Tests
- Risiken/Annahmen
- PR-Link oder PR-Befehl
- Handoff-Prompt für den nächsten Chat
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

Abgabeformat:
- Summary
- geänderte Dateien
- Checks/Tests
- Risiken/Annahmen
- nächster minimaler Schritt
```
