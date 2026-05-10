# Usage Optimization

## Ziel

Dieses Dokument hält fest, wie ChatGPT, Codex und optionale Agent-Tools im Projekt sparsam und reproduzierbar genutzt werden, ohne neue Bürokratie einzuführen.

## Grundsätze

- Ein Arbeitspaket pro Chat.
- Ein Arbeitsbranch pro klar abgegrenztem Thema.
- Kontext über Dateipfade statt kopierte Dateiinhalte.
- Stabile Regeln in `AGENTS.md`, nicht in jedem Prompt wiederholen.
- Handoff-Prompts statt langer Chat-Verläufe.
- Nur notwendige Tools aktivieren.

## Ein Arbeitspaket pro Chat

Ein Chat soll genau einen Arbeitsblock steuern:

- ein Ziel
- ein Branch
- eine erlaubte Dateiliste
- klare Stop-Regeln
- klare Checks
- Handoff am Ende

Nicht bündeln:

- Dokumentation + Build-Setup + externe Repo-Analyse
- mehrere Agent-Tools gleichzeitig
- mehrere externe Repos gleichzeitig
- Refactor + Feature + Testinfrastruktur

Wenn ein Block größer wird als erwartet, wird er beendet und als neuer minimaler Folgeblock übergeben.

## Kontext über Dateipfade

Prompts sollen auf Dateien verweisen, statt ganze Dokumente zu kopieren:

```text
Lies zuerst:
- README.md
- AGENTS.md
- 01_docs/PROJECT_BRIEF.md
- 01_docs/SESSION_STATE.md
- 01_docs/NEXT_STEPS.md
```

Nur relevante Auszüge werden eingefügt, wenn ein Tool die Datei nicht lesen kann oder wenn eine konkrete Stelle diskutiert wird.

## Stabile Regeln in AGENTS.md

Regeln, die dauerhaft gelten, gehören nach `AGENTS.md` oder in passende Setup-Dokumente:

- keine Änderungen direkt auf `main`
- keine ROMs, Saves, Emulator States, Builds oder Tool-Binaries anfassen
- keine Secrets, Tokens oder `.env`-Dateien veröffentlichen
- nur auf freigegebenen Branches arbeiten
- bei unerwarteten Dateien stoppen

Der einzelne Prompt muss diese Regeln nur kurz referenzieren und aufgabenbezogene Ergänzungen nennen.

## Handoff statt langer Chat-Verlauf

Jeder Arbeitsblock endet mit einem kompakten Handoff:

- Branch
- PR-Link oder PR-Befehl
- letzter Commit oder offener Commit-Status
- geänderte Dateien
- Checks
- Risiken
- nächster minimaler Schritt

Der nächste Chat startet aus Repo-Dateien und Handoff, nicht aus einem vollständigen Chat-Protokoll.

## Tool- und MCP-Sparsamkeit

Nicht jedes Tool muss aktiviert sein.

Empfohlen:

- Codex CLI als primärer Worker für klar abgegrenzte Repo-Änderungen.
- ChatGPT als Analyse-, QA- und Handoff-Ebene.
- `rg`/`rg --files` für Suche.
- GitHub CLI nur für Branch, Commit, Push und PR, wenn lokal verfügbar.
- MCP nur, wenn ein konkreter lokaler Nutzen besteht.

Vermeiden:

- parallele Agenten auf demselben Branch
- mehrere IDE-Agenten gleichzeitig
- MCP-Server ohne klaren Zweck
- Tool-Konfigurationen, die Secrets oder private Pfade enthalten
- lange Preambles, starre Pläne oder wiederholte Governance-Blöcke in jedem Prompt

## Kompakter Standardablauf

1. Arbeitsbranch prüfen.
2. Projektkontext über Dateipfade lesen.
3. Erlaubte Dateien und Stop-Regeln prüfen.
4. Änderung klein halten.
5. Checks ausführen.
6. Commit und PR erstellen, wenn erlaubt und verfügbar.
7. Handoff liefern.

## Definition of Done

- Der Chat behandelt genau ein Arbeitspaket.
- Die Änderung ist klein und reviewbar.
- Statusdokumente sind aktualisiert, wenn sich Projektstatus geändert hat.
- Keine verbotenen Artefakte wurden gelesen, kopiert, geändert oder committed.
- Handoff-Prompt liegt vor.
