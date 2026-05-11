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

JetBrains MCP wurde im Arbeitsblock `setup/intellij-mcp-readonly-check` lokal read-only inventarisiert.

Lokaler Befund:

- IntelliJ IDEA ist über einen JetBrains-Toolbox-Launcher im PATH auffindbar.
- Die gefundene Version ist IntelliJ IDEA 2026.2 EAP, Build `IU-262.4852.50`.
- Damit ist die Mindestanforderung 2025.2 erfüllt.
- In der IDE-Distribution ist der gebündelte JetBrains-MCP-Server als Plugin `com.intellij.mcpServer` vorhanden.
- Die IDE-Konfiguration ist über `Settings | Tools | MCP Server` auffindbar.
- Die lokale Distribution enthält Hinweise auf Client-Auto-Configuration, einschließlich Codex-Unterstützung.

JetBrains MCP bleibt optional und nicht blockierend. Codex nutzt weiter Git/`rg` als Default.

Freigegebener Nutzungsrahmen:

- nur read-only für Code-Navigation, Symbolsuche, Dateisuche und IDE-Kontextanalyse
- keine automatischen Schreibaktionen über MCP
- keine Terminal-, Build-, Run-Configuration- oder Patch-Ausführung über MCP
- kein Brave Mode / keine Bestätigung-Bypasses
- keine Zugriffe auf ROM-, Save-, Emulator-State-, Build-, Tool-Binary- oder Secret-Pfade
- keine MCP-Konfigurationen mit Secrets committen
- keine privaten absoluten Nutzerpfade dokumentieren
- nicht parallel mit einem anderen schreibenden Agent auf demselben Branch nutzen

Vor einer tatsächlichen Nutzung muss die IDE-Seite manuell so eingeschränkt werden, dass nur erlaubte Workspace-Pfade sichtbar sind und schreibende MCP-Tools nicht exponiert werden.

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
