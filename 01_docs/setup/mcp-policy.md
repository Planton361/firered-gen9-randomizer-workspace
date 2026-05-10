# MCP Policy

## Ziel

Dieses Dokument beschreibt, wann MCP-Server im Projekt genutzt werden dürfen. MCP bleibt optional und darf den sicheren GitHub-/Codex-Workflow nicht verkomplizieren.

## Grundsatz

MCP ist ein optionales Integrationswerkzeug, kein Default.

Ein MCP-Server wird nur genutzt, wenn er für ein konkretes Arbeitspaket einen klaren Nutzen hat und keine privaten Daten, Secrets oder rechtlich sensiblen Artefakte gefährdet.

## Erlaubt

MCP darf genutzt werden für:

- lokale, read-only Navigation in freigegebenen Projektdateien
- dokumentierte Tool- oder IDE-Integration
- klar begrenzte Analyseaufgaben
- serverseitige Funktionen, die im Tool-Manifest dokumentiert sind

## Nicht erlaubt

MCP darf nicht genutzt werden für:

- Zugriff auf ROMs, Saves, Emulator States, Builds oder Tool-Binaries
- Zugriff auf private Keys, Tokens, `.env`-Dateien oder Passwortspeicher
- automatische Änderungen auf `main`
- unkontrollierte Full-Auto-Ausführung
- externe Downloads, Clone- oder Fork-Aktionen ohne Freigabe
- nicht dokumentierte Server aus unbekannter Quelle

## Vertrauensregel

Nur vertrauenswürdige MCP-Server verwenden:

- offizielle Anbieter oder nachvollziehbarer Quellcode
- klarer Zweck
- minimale Berechtigungen
- keine unnötigen Dateisystem- oder Netzwerkrechte
- keine Secrets in Configs
- keine privaten Pfade committen

## Kein Brave Mode als Default

Aggressive Auto-Run-, Brave-, YOLO- oder Full-Auto-Modi sind kein Default.

Solche Modi sind nur für kleine, klar erlaubte Repo-Änderungen vertretbar, wenn:

- Branch nicht `main` ist
- erlaubte Dateien vollständig genannt sind
- Stop-Regeln eindeutig sind
- keine ROM-/Build-/Tool-Binary-/Secret-Pfade betroffen sind
- Checks definiert sind

Für Toolchain-Installationen, externe Repos, Builds oder ROM-nahe Arbeit werden sie nicht verwendet.

## Secrets und private Pfade

MCP-Konfigurationen dürfen nicht enthalten:

- GitHub Tokens
- OpenAI/API Tokens
- private Keys
- `.env`-Werte
- lokale ROM-Pfade
- persönliche absolute Pfade, sofern sie nicht ausdrücklich als unkritischer Workspace-Pfad dokumentiert sind

Lokale Config-Dateien mit Secrets bleiben außerhalb von Git.

## Tool-Manifest-Pflicht

Jeder MCP-Server, der im Projekt aktiv genutzt oder empfohlen wird, muss in `01_docs/references/tool-manifest.md` dokumentiert werden:

- Name
- Zweck
- Quelle/Upstream
- lokaler Status
- Berechtigungen grob beschrieben
- ob Codex/Agenten ihn nutzen dürfen
- Sicherheitsnotizen

Nicht dokumentierte MCP-Server gelten als nicht freigegeben.

## JetBrains MCP

JetBrains MCP wird erst nach einer Toolchain-Inventur evaluiert.

Vorher klären:

- welche JetBrains-Version lokal genutzt wird
- ob ein offizieller oder nachvollziehbarer MCP-Server verwendet wird
- welche Projektpfade sichtbar wären
- ob Schreibzugriff nötig ist
- ob parallele Agent-Arbeit auf demselben Branch ausgeschlossen ist

Bis dahin bleibt JetBrains MCP optional und nicht freigegeben für automatische Änderungen.

## Minimaler Prüfablauf vor MCP-Nutzung

1. Zweck im Arbeitspaket nennen.
2. Serverquelle prüfen.
3. Berechtigungen minimal halten.
4. Keine Secrets oder privaten Pfade in Configs.
5. Server im Tool-Manifest dokumentieren.
6. Erst danach für den konkreten Branch freigeben.

## Definition of Done

- MCP wurde nur bei konkretem Nutzen eingesetzt.
- Server ist im Tool-Manifest dokumentiert.
- Keine Secrets oder verbotenen Artefakte wurden exponiert.
- Handoff nennt, ob MCP genutzt wurde.
