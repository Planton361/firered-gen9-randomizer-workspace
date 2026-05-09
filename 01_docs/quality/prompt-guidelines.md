# Prompt Guidelines

Dieses Dokument sammelt wiederverwendbare Prompt-Regeln für ChatGPT und Codex.

## Grundsatz

Prompts sollen klein, eindeutig und reviewbar sein.

## Codex-Prompt-Mindestangaben

Jeder Codex-Prompt sollte enthalten:

- gelesene Kontextdateien
- klare Aufgabe
- erlaubte Dateien
- ausdrücklich verbotene Dateien und Aktionen
- erwartetes Abgabeformat
- nächster minimaler Schritt

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
- nächster minimaler Schritt
