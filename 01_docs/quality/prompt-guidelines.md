# Prompt Guidelines

Dieses Dokument sammelt wiederverwendbare Prompt-Regeln für ChatGPT und Codex.

## Grundsatz

Prompts sollen klein, eindeutig und reviewbar sein.

Stabile Regeln gehören in Repo-Dateien wie `AGENTS.md`, `codex-workflow.md`, `git-workflow.md` und `security-rules.md`. Prompts sollen diese Regeln nur referenzieren und nicht jedes Mal lang duplizieren.

## Best Practices

- Kurz schreiben: ein Ziel, ein Arbeitsbranch, eine erlaubte Dateiliste.
- Klare Aufgabe formulieren: nummerierte Schritte statt offener Sammelaufträge.
- Erlaubte Dateien konkret nennen: keine impliziten Freigaben.
- Verbotene Aktionen explizit nennen: `main`, ROMs, Saves, Builds, Tool-Binaries, Secrets, externe Repos.
- Definition of Done angeben: Checks, Statusdokumente, Commit, PR oder PR-Befehl.
- Handoff-Prompt verlangen: nächster Chat soll ohne lange Rekonstruktion starten können.

## Codex-Prompt-Mindestangaben

Jeder Codex-Prompt sollte enthalten:

- gelesene Kontextdateien
- klare Aufgabe
- erlaubte Dateien
- ausdrücklich verbotene Dateien und Aktionen
- Definition of Done
- erwartetes Abgabeformat
- Handoff-Prompt oder nächster minimaler Schritt

## Zu vermeiden

- mehrere unabhängige Ziele in einem Prompt
- offene Formulierungen wie „mach alles fertig“
- unklare Dateifreigaben
- Refactors ohne explizite Freigabe
- externe Downloads ohne vorherige Entscheidung
- ROM-, Save-, Build-, Tool-Binary- oder Secret-Bezug

## Standard-Abgabeformat

Codex soll liefern:

- Summary
- geänderte Dateien
- Checks/Tests
- Risiken/Annahmen
- PR-Link oder PR-Befehl, wenn ein PR Teil der Aufgabe ist
- Handoff-Prompt für den nächsten Chat

## Vorlagen

Siehe `01_docs/quality/prompt-templates.md`.
