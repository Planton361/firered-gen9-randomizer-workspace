# 068 - CFRU/DPE TypeEffectiveness Follow-up Smoke Results

## Kontext

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes`

Ziel dieses Blocks war die einzelne lokale Ausfuehrung der in 067 geplanten TypeEffectiveness-Folgesmokes nach dem gemergten TypeChart-Fix aus 066.

Scope:

- Nur TypeEffectiveness / TypeChart.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine Species-Type-Randomization und kein Species-Type-Write in `gBaseStats`.
- Keine MoveData-Write-Optionen.
- Keine Field Items, Shops, Pickup oder Item-Writer.
- Keine Palette-Randomization.
- Keine Graphics-, Sprites-, Text- oder Menu-Writer.
- Keine Trainer-, Wild-, Starter- oder Level-Modifier-Smokes.

Lokale ROM-, Log-, Output-ROM-, Build- und Diagnoseartefakte blieben ignored. Private Pfade, ROM-Namen und Hashes werden nicht dokumentiert.

## Ausgefuehrte Slices

| Slice | Feature-ID | GUI-Modus | Ergebnis |
|---|---|---|---|
| Balanced | `FVX-TYPE-001` | Random Balanced | stabil |
| Keep Type Identities | `FVX-TYPE-001` | Keep Type Identities | stabil |
| Inverse | `FVX-TYPE-001` | Inverse | stabil |
| Add Random Immunities | `FVX-TYPE-002` | Inverse + Add Random Immunities | stabil |
| Update Type Effectiveness | `FVX-TYPE-003` | Update Type Effectiveness | stabil |

## Ergebnisuebersicht

| Slice | Save | Log | Output | Log non-empty | Reload | TypeChart-Mismatches | Bad Egg | `<unknown>` | Stacktrace |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `FVX-TYPE-001` Balanced | true | true | true | true | true | 0 | false | false | none |
| `FVX-TYPE-001` Keep Type Identities | true | true | true | true | true | 0 | false | false | none |
| `FVX-TYPE-001` Inverse | true | true | true | true | true | 0 | false | false | none |
| `FVX-TYPE-002` Add Random Immunities | true | true | true | true | true | 0 | false | false | none |
| `FVX-TYPE-003` Update Type Effectiveness | true | true | true | true | true | 0 | false | false | none |

## TypeChart-Struktur

| Slice | Non-neutral before | Non-neutral after | Non-neutral reload | Fairy raw reload | Stellar raw reload | Unsupported preserved | Foresight terminator | Endtable terminator |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `FVX-TYPE-001` Balanced | 110 | 110 | 110 | 12 | 0 | true | true | true |
| `FVX-TYPE-001` Keep Type Identities | 110 | 110 | 110 | 0 | 0 | true | true | true |
| `FVX-TYPE-001` Inverse | 110 | 110 | 110 | 0 | 0 | true | true | true |
| `FVX-TYPE-002` Add Random Immunities | 110 | 110 | 110 | 0 | 0 | true | true | true |
| `FVX-TYPE-003` Update Type Effectiveness | 110 | 108 | 108 | 0 | 0 | true | true | true |

## Bewertung

Alle fuenf TypeEffectiveness-Folgesmokes waren im getesteten CFRU/DPE Gen9-BPRE-TypeChart-Scope stabil:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `writeReloadTypeChartMismatches=0`
- unsupported/Stellar wird nicht eingefuehrt oder still normalisiert
- Foresight- und Endtable-Terminatoren bleiben erhalten
- `Bad Egg=false`
- `<unknown>=false`
- `stacktrace=none`

Fairy-Reload:

- Balanced erzeugte neue Fairy-Rohtriplets und reloadete sie als raw `0x17`.
- Keep Type Identities, Inverse, Add Random Immunities und Update Type Effectiveness erzeugten in diesem Test keine Fairy-Rohtriplets; es gab dabei kein Fehlmapping auf unsupported/Stellar oder andere Raw-Types.

`FVX-TYPE-002` wurde bewusst getrennt als eigener Slice getestet, weil Add Random Immunities ein eigener Risikopunkt fuer Immunity-Verteilung, Kapazitaet und Preserve-Triplets ist.

## Ergebnis

Die geplanten TypeEffectiveness-Folgemodi aus 067 sind einzeln sanitisiert getestet:

- `FVX-TYPE-001` Balanced, Keep Type Identities und Inverse bleiben im getesteten Scope `Getestet`.
- `FVX-TYPE-002` Add Random Immunities kann im getesteten Scope von `Write modelliert` auf `Getestet` gesetzt werden.
- `FVX-TYPE-003` Update Type Effectiveness kann im getesteten Scope von `Write modelliert` auf `Getestet` gesetzt werden.

Das ist kein Nachweis fuer Species-Type-Write, MoveData, Palette, Items, Graphics/Sprites, Text/Menu oder Level-/Trainer-/Wild-/Starter-Optionen.
