# Fork Strategy

## Ziel

Dieses Dokument beschreibt, wann Forks, Remotes und externe Repos verwendet werden.

## Aktueller Stand

Für diesen Arbeitsblock werden keine externen Repos geklont und keine Forks angelegt.

Das Workspace-Repo bleibt die Source of Truth:

```text
origin -> Planton361/firered-gen9-randomizer-workspace
main   -> stabiler geschützter Branch
```

## Grundmodell für spätere Forks

Wenn ein externes Projekt geändert werden muss:

- `origin` zeigt auf den eigenen Fork.
- `upstream` zeigt auf das Originalrepo.
- Änderungen erfolgen nur auf Arbeitsbranches.
- Commit-Hashes, Branches und lokale Pfade werden im Tool-Manifest dokumentiert.
- Das Workspace-Repo dokumentiert die Entscheidung, enthält aber keine fremde Repo-Historie als Kopie.

Keine Forks ohne dokumentierte Entscheidung und Tool-Manifest-Eintrag.

## Wann nur lesen?

Nur lesen reicht, wenn:

- ein Repo nur Referenz ist
- keine Patches geplant sind
- nur README, Issues, Branches oder Dateistruktur analysiert werden
- ein Tool nur lokal genutzt, aber nicht verändert wird

## Wann forken?

Ein Fork ist sinnvoll, wenn:

- eigene Änderungen an UPR FVX, CFRU, DPE oder Tracker-Code nötig werden
- ein PR upstream vorbereitet wird
- Experimente isoliert versioniert werden müssen

## Regeln

Nicht erlaubt:

- blind externe Repos klonen
- mehrere externe Repos gleichzeitig ändern
- Forks ohne Eintrag im Tool-Manifest produktiv nutzen
- Forks ohne dokumentierte Entscheidung anlegen
- ROMs, Saves, Builds oder Tool-Binaries in externe Repos kopieren
- private lokale Pfade oder Secrets veröffentlichen

Erlaubt:

- Repos read-only analysieren
- Commit-Hashes dokumentieren
- Fork-Entscheidungen als Decision Log festhalten
- kleine Branches für klar abgegrenzte Änderungen verwenden
