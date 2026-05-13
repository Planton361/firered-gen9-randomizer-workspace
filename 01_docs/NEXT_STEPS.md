# Next Steps

## Aktueller Arbeitsblock

Codex Plan-/Goal-Nutzung dokumentieren.

Aktueller Workspace-Branch:

```text
docs/codex-plan-goal-usage-guidance
```

## Ziel

Die Erkenntnis dokumentieren, wann Codex kuenftig mit Plan-Modus oder Goal-Modus arbeiten soll, damit spaetere Chats diese Regel ueber Projektdateien laden koennen.

## Geaendert in diesem Block

- Neues Quality-Dokument:
  - `01_docs/quality/codex-plan-goal-usage.md`
- Verweise/Template-Ergaenzungen:
  - `01_docs/quality/usage-optimization.md`
  - `01_docs/quality/prompt-templates.md`

## Regel fuer kuenftige Chats

- Kleine Diagnose- und Fixbranches: kompakter Standardprompt.
- Groessere oder riskantere Analyse-/Fixbloecke: Plan-Modus zuerst, damit Codex Scope, Dateien, Risiken und Stop-Regeln klaert.
- Lange, klar validierbare read-only Aufgaben: Goal-Modus optional.
- Kein Goal-Modus fuer Repointing-Fixes, Move-Data-Write, ROM-nahe Writer oder grosse Multi-Fix-PRs.
- Bei Unsicherheit: Plan-Modus vor Goal-Modus.

## Abschluss dieses Blocks

1. PR reviewen und mergen:

```text
docs: document Codex plan/goal usage guidance
```

2. Nach Merge in neuen Chats bei groesseren Aufgaben zusaetzlich lesen lassen:

```text
01_docs/quality/codex-plan-goal-usage.md
```

## Naechster empfohlener Arbeitsblock nach Merge

Zurueck zum technischen Randomizer-Track:

```text
compat/upr-fvx-cfru-dpe-learnset-write-repointing
```

Ziel bleibt:

- Full CFRU/DPE Learnset-Write mit Repointing nur dann implementieren, wenn freie ROM-Fläche diagnostisch nachgewiesen wird.
- Bestehende Pointertable bei `0x25D7B4` nutzen.
- Neue `u16 move + u8 level` Blobs schreiben und Pointertable-Eintraege pro interner Species-ID aktualisieren.
- Reload per interner SpeciesSet-Identitaet pruefen.

Empfohlen fuer diesen Folgeblock:

```text
Mit Plan-Modus starten.
```

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- keine technische Randomizer-Codeaenderung in diesem Docs-Block
