# Lessons Learned

Dieses Dokument sammelt nur wiederverwendbare Erkenntnisse aus Projektabschnitten.

## Eintragsregel

Ein Eintrag gehört hierher, wenn mindestens eines gilt:

- der Fehler kann in späteren Sessions wieder auftreten
- Codex/ChatGPT braucht dafür eine klarere Regel
- der Prompt war zu groß, zu unklar oder nicht reviewbar
- ein Arbeitspaket war falsch geschnitten
- Sicherheits-, Reproduzierbarkeits- oder Usage-Risiken wurden sichtbar

Nicht hierher gehören:

- reine Statusmeldungen
- einmalige Tippfehler
- erledigte Kleinigkeiten ohne Prozesswert
- lange Chat-Zusammenfassungen

## Format

### LL-YYYY-MM-DD-001 – Kurztitel

**Beobachtung:**  
Was ist passiert?

**Einordnung:**  
Einmaliger Fehler oder dauerhaftes Prozessproblem?

**Lesson Learned:**  
Welche allgemeine Regel folgt daraus?

**Prozessänderung:**  
Welche Prompt-, Workflow- oder Dokumentationsregel wird angepasst?

**Betroffene Dateien:**  
- ...

**Nächster minimaler Schritt:**  
Kleinster prüfbarer Schritt.

### LL-2026-05-10-001 – Abschlussdokumentation gehört zur Definition of Done

**Beobachtung:**  
`NEXT_STEPS.md` und Roadmap-Status können nach gemergten PRs veralten, wenn die Abschlussdokumentation nicht Teil des Arbeitspakets ist.

**Einordnung:**  
Dauerhaftes Prozessproblem bei kurzen Codex-/GitHub-Arbeitsblöcken.

**Lesson Learned:**  
Ein Arbeitspaket ist erst abgeschlossen, wenn Session State, Next Steps und Roadmap bei Bedarf aktualisiert sind.

**Prozessänderung:**  
Definition of Done und Work-Package-Lifecycle nennen Abschlussdokumentation ausdrücklich.

**Betroffene Dateien:**  
- `01_docs/setup/work-package-lifecycle.md`
- `01_docs/quality/prompt-guidelines.md`
- `01_docs/NEXT_STEPS.md`
- `00_project-control/roadmap/roadmap-status.md`

**Nächster minimaler Schritt:**  
Bei jedem PR prüfen, ob Handoff- und Statusdokumente noch zum gemergten Stand passen.
