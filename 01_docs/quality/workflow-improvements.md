# Workflow Improvements

Dieses Dokument sammelt wiederverwendbare Verbesserungen am Projektworkflow.

## Zweck

Workflow-Verbesserungen sollen nur dokumentiert werden, wenn sie zukünftige Arbeit messbar sicherer, effizienter oder reproduzierbarer machen.

## Eintragskriterien

Ein Eintrag gehört hierher, wenn mindestens eines gilt:

- wiederkehrender Fehler wird verhindert
- Codex-/ChatGPT-Usage wird reduziert
- Arbeitspakete werden besser reviewbar
- Sicherheitsrisiken werden früher erkannt
- lokale und GitHub-Stände werden besser synchronisiert
- Dokumentation wird reproduzierbarer

## Format

### WI-YYYY-MM-DD-001 – Kurztitel

**Problem:**  
Was war ineffizient, riskant oder unklar?

**Verbesserung:**  
Welche konkrete Regel oder Checkliste wird ergänzt?

**Betroffene Dateien:**  
- ...

**Minimaler nächster Schritt:**  
Kleinste sinnvolle Änderung.

### WI-2026-05-10-001 – Work-Package-Lifecycle mit Handoff-Prompt

**Problem:**  
Codex-Arbeitsblöcke können schnell umgesetzt werden, aber der nächste Chat muss den Stand oft aus mehreren Dateien rekonstruieren.

**Verbesserung:**  
Ein kurzer Lifecycle definiert Kontextlesen, Branch-Check, Abschlussdokumentation, Checks, Commit/PR und Handoff-Prompt als Standard.

**Betroffene Dateien:**  
- `01_docs/setup/work-package-lifecycle.md`
- `01_docs/quality/prompt-templates.md`
- `01_docs/quality/prompt-guidelines.md`
- `01_docs/setup/codex-workflow.md`

**Minimaler nächster Schritt:**  
Die Vorlage aus `prompt-templates.md` für den nächsten kleinen Arbeitsbranch verwenden.
