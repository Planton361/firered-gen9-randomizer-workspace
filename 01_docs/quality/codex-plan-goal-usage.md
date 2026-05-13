# Codex Plan/Goal Usage

## Ziel

Dieses Dokument beschreibt, wann Codex mit Plan- oder Goal-Modus gestartet werden soll. Es ergaenzt `prompt-templates.md` und `usage-optimization.md`.

## Grundregel

- Plan-Modus ist der bevorzugte Modus fuer groessere oder riskantere Arbeitspakete, bei denen zuerst Scope, Dateien, Stop-Regeln und Risiken geklaert werden sollen.
- Goal-Modus ist nur fuer lange, klar validierbare und moeglichst read-only Aufgaben geeignet.
- Normale kleine Diagnose- oder Fixbranches nutzen weiterhin kompakte Standardprompts ohne Slash-Command.

## Plan-Modus

Plan-Modus soll genutzt werden, wenn Codex zuerst einen Umsetzungsplan liefern soll, bevor Dateien geaendert werden.

Geeignet fuer:

- groessere read-only Modellierungsbloecke
- Repointing- oder Write-Scope-Analyse
- Randomizer-Matrix- oder Regression-Planung
- komplexe Fixbranches mit mehreren moeglichen Pfaden
- Situationen, in denen erlaubte Dateien, Gates oder Stop-Regeln vorab validiert werden muessen

Erwartung an Codex:

- keine Datei sofort aendern
- geplante Schritte nennen
- betroffene Dateien nennen
- Risiken und Stop-Regeln nennen
- offene Voraussetzungen nennen
- auf Freigabe warten, bevor Umsetzung startet

## Goal-Modus

Goal-Modus darf nur genutzt werden, wenn die Zielbedingung dauerhaft und eindeutig ist und die Aufgabe sicher autonom weiterlaufen kann.

Geeignet fuer:

- read-only Matrix- oder Zusammenfassungsaufgaben
- bestehende Diagnoseprotokolle auswerten
- offene Randomizer-Funktionsbereiche inventarisieren
- Dokumentations- und Priorisierungsarbeit ohne Codeaenderung

Nicht geeignet fuer:

- Repointing-Fixes
- Move-Data-Write
- ROM-nahe Writer
- grosse Multi-Fix-PRs
- Aufgaben mit unsicherer FreeSpace- oder Pointerlage
- Aufgaben, bei denen Codex private Pfade, ROMs, Builds oder Secrets sehen koennte

## Entscheidungsmatrix

| Aufgabe | Empfehlung |
|---|---|
| kleiner Diagnosebranch | Standardprompt |
| kleiner eng gegateter Fix | Standardprompt oder Plan-Modus, falls Risiko unklar |
| grosser read-only Modellierungsblock | Plan-Modus |
| Repointing-/Write-Scope mit unsicherem Modell | Plan-Modus, danach separater Fixprompt |
| Matrix aus vorhandenen Diagnosen | Goal-Modus moeglich |
| ROM-nahe Writer oder Multi-Fix-PR | kein Goal-Modus; kleine Branches nutzen |

## Projektregel

Bei Unsicherheit gilt:

```text
Plan-Modus vor Goal-Modus.
Kleine reviewbare Branches vor grossen Multi-Fix-PRs.
Read-only Analyse darf groesser sein als Codeaenderung.
```

## Handoff-Regel

Wenn ein naechster Chat einen grossen oder riskanten Block starten soll, soll der Handoff explizit sagen:

```text
Empfohlen: mit Plan-Modus starten.
```

Wenn ein naechster Chat eine lange, klar validierbare read-only Aufgabe starten soll, darf der Handoff sagen:

```text
Optional: Goal-Modus ist geeignet, weil die Aufgabe read-only und klar validierbar ist.
```
