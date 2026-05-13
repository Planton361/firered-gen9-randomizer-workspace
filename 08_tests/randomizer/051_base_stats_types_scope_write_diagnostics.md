# 051 - CFRU/DPE Base Stats + Types Scope/Write Diagnostics

## Kontext

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write`

UPR-FVX-Fix: `20f16d07ab4ea62e5cd3f27ef09a6d5b036d2392`

Ziel dieses Fixes war ein minimal gegateter CFRU/DPE-BaseStats-/Types-Pfad:

- `gBaseStats` weiter ueber den bestehenden `romEntry.PokemonStats`-Pfad nutzen.
- Entry-Size `0x1C` beibehalten.
- Fairy im CFRU/DPE-Scope als Type-Byte `0x17` lesen und schreiben.
- Stellar `0x18` nicht als randomisierbaren FVX-Type einfuehren; unrepresentierbare/Null-Primary-Type-Species werden im Type-Randomizer defensiv uebersprungen.
- Keine Hidden-Ability-, Encounter-Held-Item-, Move-Data-Write-, Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Lokale ROM-, Log- und Output-Artefakte blieben ignored unter `05_builds/**`. Private Pfade, ROM-Namen und Hashes wurden nicht dokumentiert.

## Fix-Zusammenfassung

### Base Stats / Type Bytes

`Gen3RomHandler` liest und schreibt BaseStats-Type-Bytes im CFRU/DPE-Gen9-BPRE-Scope ueber eng gegatete Helper:

- CFRU/DPE Read: `0x17 -> Type.FAIRY`.
- CFRU/DPE Write: `Type.FAIRY -> 0x17`.
- CFRU/DPE Preserve: bestehendes raw `0x18` bleibt erhalten, wenn der FVX-Type nicht representierbar ist.
- Vanilla-/Jambo-/andere Gen3-Pfade nutzen weiterhin die bestehende Gen3-Type-Map.

### Type Randomizer

`SpeciesTypeRandomizer` skippt Species mit nicht representierbarem/null Primary Type defensiv, statt Stellar-/Placeholder-Slots auf Normal/Fairy/null umzuschreiben.

### Type Pool

Der CFRU/DPE-gegatete TypeTable-Pool verwendet Fairy, aber kein Stellar. Damit kann Type-Randomization Fairy schreiben, ohne Stellar in Random-Pools aufzunehmen.

## Diagnose-Harness

Lokaler Harness: `05_builds/randomizer-smoke/051_base_stats_types_scope_write/`.

Gepruefte Mindestlaeufe:

1. Base Stats-only
2. Types-only
3. Base Stats + Types

Verglichen wurden die mutierten Handler-Daten gegen Reload aus der Output-ROM:

- BaseStats-Signatur: HP, Attack, Defense, Sp. Attack, Sp. Defense, Speed.
- Raw Type-ID-Signatur: `type1/type2` aus `gBaseStats`.
- Fairy-/Stellar-Counts aus raw Type-Bytes.

## Diagnose-Ergebnisse

| Lauf | Optionen | saveSuccessful | logSuccessful | outputRomExists | logNonEmpty | writeReloadBaseStatsMismatches | typeIdMismatches | fairyReadCount | fairyWriteCount | stellarSkippedCount | Bad Egg im Log | Unknown-Type-Marker |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Base Stats-only | Base Stats random | true | true | true | true | 0 | 0 | 3 | 3 | 9 | true | true |
| Types-only | Types random | true | true | true | true | 0 | 0 | 3 | 36 | 9 | true | true |
| Base Stats + Types | Base Stats random + Types random | true | true | true | true | 0 | 0 | 3 | 39 | 9 | true | true |

Gemeinsame Strukturwerte:

- `species.total=423` im aktuell von FVX geladenen SpeciesSet-Scope.
- Hoechste Species im geladenen Scope: `1065:Minior`.
- `baseStatsEntrySize=0x1C`.
- `gBaseStats` Pointer-Ort: `0x080001BC`.
- `gBaseStats` Ziel-ROM-Offset: `0x19FC4CC`.
- `unsupportedPrimaryTypeBytesBefore=9`.
- `unsupportedPrimaryTypeBytesReload=9`.
- `stacktrace=none` in allen drei Laeufen.

## Bewertung

Base Stats und Types sind im getesteten CFRU/DPE Gen9-BPRE-Scope fuer die geprueften GUI-nahen Einzel- und Kombinationslaeufe P1-supported:

- Save/Log/Output funktionieren.
- BaseStats-Write/Reload bleibt mismatch-frei.
- Raw Type-ID-Write/Reload bleibt mismatch-frei.
- Fairy wird im CFRU/DPE-Scope gelesen und wieder als `0x17` geschrieben.
- Stellar wird nicht in den Random-Pool aufgenommen und nicht auf Normal/Fairy/null gemappt.

Einschraenkung:

- Der Log enthaelt weiterhin `Bad Egg` und Unknown-Type-/`null`-Marker aus bestehenden Placeholder-/unsupported-Type-Species im geladenen SpeciesSet-Scope. Das blockiert Save/Reload nicht, bleibt aber ein separates Log-Hygiene-/Placeholder-Scope-Risiko.
- Hidden Ability bei BaseStats-Offset `0x1A` und Encounter Held Items bei `0x0C/0x0E` bleiben out of scope.

## Risiken / Annahmen

- Der Fix ist an `useCfruDpeGen9SpeciesCount` gegatet und setzt voraus, dass dieser Gate nur fuer sicher erkannte CFRU/DPE Gen9-BPRE-Hacks aktiv wird.
- Type-Effectiveness fuer Fairy wird nicht erweitert; der Branch entblockt BaseStats-/Species-Type-Read/Write, nicht Type-Chart-Randomization.
- Stellar bleibt mangels FVX-Type-Enum unrepresentiert. Eine echte Stellar-Unterstuetzung braucht einen separaten Type-Enum-/TypeService-/Logger-Plan und ist nicht Teil dieses P1-Fixes.
- Die Diagnose prueft den von FVX geladenen SpeciesSet-Scope, nicht alle `NUM_SPECIES=1440` BaseStats-Eintraege.

## Checks

UPR-FVX:

```sh
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
```

Ergebnis: erfolgreich; UPR-FVX-Fix committed als `20f16d07ab4ea62e5cd3f27ef09a6d5b036d2392`.

Workspace-Checks werden nach Dokumentationsupdate im Workspace ausgefuehrt.

## Folgebranches

Empfohlen:

1. `compat/upr-fvx-cfru-dpe-abilities-hidden-ability-scope-and-write`
2. `analysis/upr-fvx-cfru-dpe-p1-item-data-and-bad-item-model`
3. `analysis/upr-fvx-cfru-dpe-p1-type-log-placeholder-hygiene`
4. `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`
5. `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`
