# 038 - TM/HM 128-Slot-Fix Diagnostics fuer CFRU/DPE Gen9-BPRE

Ziel dieses Fixblocks war, das aktive CFRU/DPE-128-Slot-TM/HM-Modell minimal und eng gegatet in UPR-FVX zu unterstuetzen. Keine Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung wurde vorgenommen.

## Stand

- Workspace-Branch: `compat/upr-fvx-cfru-dpe-tm-hm-128-slot`
- UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-tm-hm-128-slot`
- UPR-FVX-Commit: `58379ffd3146fcd6bb0eb416647cdf9b752cfc0e`
- Basis: Workspace PR #74 gemerged; Diagnose 037 hat das aktive 128-Slot-Modell nachgewiesen.
- Test-ROM: lokaler CFRU/DPE Gen9-BPRE-Teststand unter `05_builds/**`, nicht committed.
- Seed: `274269061345323`

## Implementierter Scope

Geaendert wurde nur `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` im UPR-FVX-Submodule.

Der neue Pfad ist auf sicher erkannte CFRU/DPE-Gen9-BPRE-Hacks begrenzt (`useCfruDpeGen9SpeciesCount`):

- `gTMHMMoves` wird ueber Pointer-Location `0x8125A8C` gelesen.
- Zielpointer im Teststand: `0x09A5981A`, ROM-Offset `0x1A5981A`.
- `gTMHMMoves` wird als `u16[128]` behandelt.
- TM-Slots sind `0..119` (`getTMCount() = 120`).
- HM-Slots sind `120..127` (`getHMCount() = 8`).
- `setTMMoves()` schreibt fuer CFRU/DPE nur die 120 TM-Slots; HM-Slots bleiben slotbasiert geschuetzt.
- Der klassische `50+8`-Pfad, TM-Item-Texte, TM-Item-Paletten und Duplicate-TM-Tabelle bleiben fuer CFRU/DPE-128-Slot bewusst unangetastet.
- `gTMHMLearnsets` wird ueber Pointer-Location `0x8043C68` gelesen.
- Zielpointer im Teststand: `0x096002D0`, ROM-Offset `0x16002D0`.
- Compatibility wird als 16 Bytes pro Species / 128 Flags plus Dummy-Index `0` behandelt (`flagLength=129`).
- Species-Offsets werden ueber `SpeciesSetIdentityNumber` berechnet und defensiv gegen ungueltige/Null-Species abgesichert.

## Gemeinsame Befunde

| Feld | Wert |
|---|---|
| `moves.total` | `992` |
| Hoechster Move | `PsychicNoise`, ID `991` |
| `tmCount` | `120` |
| `hmCount` | `8` |
| Total TM/HM-Slots | `128` |
| `gTMHMMoves` Pointer-Location | `0x8125A8C` |
| `gTMHMMoves` Zielpointer / Offset | `0x09A5981A` / `0x1A5981A` |
| `gTMHMLearnsets` Pointer-Location | `0x8043C68` |
| `gTMHMLearnsets` Zielpointer / Offset | `0x096002D0` / `0x16002D0` |
| Compatibility flag length | `129` |
| Compatibility species entries | `423` |
| Null-/Placeholder-Species mit null Primaertyp | `10` |
| Species mit null Sekundaertyp | `225` |
| Invalid TM/HM moves nach Randomization | `0` |
| Bad Egg im Log | `false` |
| `<unknown>` im Log | `false` |
| Unknown-Move-Marker im Log | `false` |

Hinweis: Die Compatibility-Species-Anzahl bleibt im aktuellen FVX-Scope bei `423`; dieser Branch erweitert nicht den Species-Kompatibilitaetsumfang, sondern korrigiert Slotbreite, Pointermodell und Write/Reload-Stabilitaet fuer den bestehenden TM/HM-Pfad.

## Lauf 1: TM moves-only

Optionen:

- `tmsMod=RANDOM`
- `tmsHmsCompatibilityMod=UNCHANGED`

Ergebnis:

| Feld | Wert |
|---|---|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| `logBytes` | `5316` |
| before/after/reload TM/HM entries | `128` / `128` / `128` |
| TM slots `0..119` count | `120` |
| HM slots `120..127` count | `8` |
| HM before/after mismatches | `0` |
| HM after/reload mismatches | `0` |
| `writeReloadTmHmMismatches` | `0` |
| `writeReloadCompatibilityMismatches` | `0` |
| Compatibility before/after flag changes | `0` |

Bewertung: TM-Move-Randomization schreibt 120 TM-Slots stabil und laesst HM-Slots unveraendert.

## Lauf 2: TM/HM compatibility-only

Optionen:

- `tmsMod=UNCHANGED`
- `tmsHmsCompatibilityMod=RANDOM_PREFER_TYPE`

Ergebnis:

| Feld | Wert |
|---|---|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| `logBytes` | `525680` |
| before/after/reload TM/HM entries | `128` / `128` / `128` |
| HM before/after mismatches | `0` |
| HM after/reload mismatches | `0` |
| `writeReloadTmHmMismatches` | `0` |
| `writeReloadCompatibilityMismatches` | `0` |
| Compatibility before/after flag changes | `1335` |

Bewertung: Compatibility-only ist mit 16-Byte-/128-Bit-Flags stabil und reloadfaehig.

## Lauf 3: TM moves + TM/HM compatibility

Optionen:

- `tmsMod=RANDOM`
- `tmsHmsCompatibilityMod=RANDOM_PREFER_TYPE`

Ergebnis:

| Feld | Wert |
|---|---|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| `logBytes` | `536665` |
| before/after/reload TM/HM entries | `128` / `128` / `128` |
| HM before/after mismatches | `0` |
| HM after/reload mismatches | `0` |
| `writeReloadTmHmMismatches` | `0` |
| `writeReloadCompatibilityMismatches` | `0` |
| Compatibility before/after flag changes | `1567` |

Bewertung: Kombinierter TM-Move- und Compatibility-Lauf ist save-/log-/reload-stabil.

## Gesamtbewertung P1-Support

CFRU/DPE TM/HM-only ist fuer den getesteten Gen9-BPRE-Stand im 128-Slot-Scope P1-supported:

- FVX erkennt fuer den gegateten CFRU/DPE-Pfad `120` TMs und `8` HMs.
- Die aktive `gTMHMMoves`-Tabelle wird ueber den CFRU/DPE-Pointer gelesen und geschrieben.
- HM-Slots `120..127` bleiben bei TM-Randomization unveraendert.
- Compatibility nutzt 128 Flags pro Species und laedt/schreibt reload-stabil.
- Alle drei Diagnose-Laeufe erzeugen Output-ROM und nichtleeren Log.
- Es gibt keine invaliden TM/HM-Move-IDs, keine Unknown-Move-Marker, kein `Bad Egg` und kein `<unknown>` im Log.

Nicht abgedeckt und bewusst out of scope:

- TM51..TM120 Item-Text-/Palette-/Duplicate-Text-Erweiterung.
- Tutor-Moves.
- Egg-Moves.
- Learnset-Write.
- Move-Data-Write.
- Erweiterung des Compatibility-Species-Scopes ueber den aktuell von FVX geladenen Bereich hinaus.

## Risiken und Folgefragen

- Die oeffentliche TM-Item-Text-/Palette-Anzeige fuer TM51..TM120 wird nicht in diesem Branch angepasst. Der ROM-Write/Reload des aktiven 128-Slot-Modells ist trotzdem stabil.
- Compatibility bleibt auf den aktuell von FVX gelieferten Species-Eintraegen (`423`) statt auf allen internen CFRU/DPE-Species. Ein separater Branch sollte nur folgen, wenn ein P1-Ziel diesen erweiterten Scope explizit benoetigt.
- Tutor- und Egg-Move-Tabellen haben eigene Modelle und duerfen nicht aus diesem TM/HM-Ergebnis abgeleitet werden.

## Checks

UPR-FVX:

- `git status --short`
- `git diff --stat`
- `git diff --check`
- `./gradlew clean :random:jar`

Workspace:

- `git status --short`
- `git submodule status --recursive`
- `git diff --stat`
- `git diff --submodule`
- `git diff --check`
