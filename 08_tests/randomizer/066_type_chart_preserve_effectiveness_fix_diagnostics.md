# 066 - CFRU/DPE TypeChart Preserve Effectiveness Fix Diagnostics

## Kontext

Workspace-Branch: `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`

UPR-FVX-Fix: `36707e0190d3d9fa587550dfc5631fcaa9abd6b1`

Ziel dieses Fixes war ein eng gegateter CFRU/DPE Gen9-BPRE TypeChart-/TypeEffectiveness-Pfad auf Grundlage von Diagnose 059.

Nicht Teil dieses Fixes:

- `gBaseStats`-Species-Type-Read/Write aus Diagnose 051.
- `STELLAR` als FVX-Type-Enum.
- MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Randomization.
- Original-Upstream-Kontakte oder Original-Upstream-PRs.

Lokale ROM-, Log-, Output-ROM- und Build-Artefakte blieben ignored. Private Pfade, ROM-Namen und Hashes werden nicht dokumentiert.

## Fix-Zusammenfassung

Der UPR-FVX-Fix trennt im Gen3-Handler das TypeChart-raw-Type-Mapping vom bestehenden BaseStats-Type-Mapping:

- CFRU/DPE TypeChart-Read: raw `0x17` wird als `Type.FAIRY` gelesen.
- CFRU/DPE TypeChart-Write: `Type.FAIRY` wird als raw `0x17` geschrieben.
- Unsupported raw Type IDs, insbesondere `0x18` / Stellar, werden nicht ins FVX-Type-Enum aufgenommen und nicht in Random-Pools aufgenommen.
- Unsupported TypeChart-Triplets werden beim TypeChart-Write raw preserved, statt still auf Normal, Fairy oder null normalisiert zu werden.
- Foresight-Block und Endtable-Terminator bleiben erhalten.
- Die Kapazitaetspruefung nutzt im CFRU/DPE-Gate den vorhandenen TypeChart-Bereich, damit Preserve-Triplets und Terminatoren nicht ueber die bestehende Tabelle hinaus schreiben.

## Diagnose-Scope

Ausgefuehrt wurde genau ein TypeEffectiveness-only Smoke:

- Type Effectiveness Random.
- Keine Species-Type-Randomization.
- Keine MoveData-Write-Optionen.
- Keine Field Items, Shops, Pickup oder Held Items.
- Keine Palette-Randomization.
- Keine Graphics- oder Text/Menu-Optionen.

Der Reload-Vergleich vergleicht die nach dem Randomizer-Write im Handler vorhandene TypeTable gegen die aus der Output-ROM neu geladene TypeTable. Zusaetzlich werden raw Fairy-, Stellar-/unsupported- und Terminator-Befunde aus dem TypeChart-Bytebereich gezaehlt.

## Diagnose-Ergebnisse

| Slice | Save | Log | Output | Reload | TypeChart-Mismatches | Stacktrace |
|---|---:|---:|---:|---:|---:|---|
| TypeEffectiveness-only | true | true | true | true | 0 | none |

Struktur- und Preserve-Werte:

| Metrik | Wert |
|---|---:|
| `typeChartTypes` | 18 |
| `nonNeutralEffectivenessBefore` | 110 |
| `nonNeutralEffectivenessAfter` | 110 |
| `nonNeutralEffectivenessReload` | 110 |
| `fairyNonNeutralBefore` | 0 |
| `fairyNonNeutralAfter` | 13 |
| `fairyNonNeutralReload` | 13 |
| `rawFairyEntriesBefore` | 0 |
| `rawFairyEntriesAfter` | 13 |
| `rawFairyEntriesReload` | 13 |
| `rawStellarEntriesBefore` | 0 |
| `rawStellarEntriesAfter` | 0 |
| `rawStellarEntriesReload` | 0 |
| `unsupportedRawEntriesBefore` | 0 |
| `unsupportedRawEntriesAfter` | 0 |
| `unsupportedRawEntriesReload` | 0 |
| `unsupportedRawEntriesPreserved` | true |
| `foresightTerminatorBefore` | true |
| `foresightTerminatorReload` | true |
| `endtableTerminatorBefore` | true |
| `endtableTerminatorReload` | true |

Log-Hygiene:

| Marker | Wert |
|---|---:|
| `Bad Egg` | false |
| `<unknown>` | false |

## Bewertung

Der TypeEffectiveness-only Smoke bestaetigt den engen Fixscope:

- Save, Log, Output und Reload sind stabil.
- `writeReloadTypeChartMismatches=0`.
- Fairy wird in der geaenderten TypeChart als raw `0x17` geschrieben und nach Reload wieder als Fairy gelesen.
- Unsupported/Stellar-Triplets werden nicht in Random-Pools eingefuehrt und nicht still normalisiert.
- Foresight- und Endtable-Terminatoren bleiben erhalten.

Diese Diagnose bestaetigt den Random-TypeEffectiveness-Write im getesteten CFRU/DPE Gen9-BPRE-TypeChart-Scope. Sie ist kein Nachweis fuer:

- Pokemon-Type-Read/Write aus `gBaseStats`; das bleibt Diagnose 051.
- Stellar-Battle-Semantik oder Stellar als FVX-Type.
- Move-Type-Bytes aus MoveData.
- Palette Follow Types.
- Balanced, Keep Identities, Inverse, Add Random Immunities oder Update Type Effectiveness als einzeln getestete GUI-Modi.

## Checks

UPR-FVX:

```sh
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
```

Ergebnis: erfolgreich; UPR-FVX-Fix committed als `36707e0190d3d9fa587550dfc5631fcaa9abd6b1`.

Workspace-Checks werden nach Dokumentationsupdate im Workspace ausgefuehrt.

## Folgearbeit

Empfohlen:

1. Workspace-Submodule-Pin auf `36707e0190d3d9fa587550dfc5631fcaa9abd6b1` dokumentieren und per PR nach `main` bringen.
2. Optional spaetere TypeEffectiveness-Folgesmokes fuer Balanced, Keep Identities, Inverse, Add Random Immunities und Update Type Effectiveness einzeln planen.
3. Danach zu den bereits priorisierten offenen Writern zurueckkehren: MoveData Write, Palette Randomization, Field Items/Shops/Pickup.
