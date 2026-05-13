# 055 - Type Log / Placeholder Hygiene Classification

## Ziel

Dieses read-only Protokoll klassifiziert sichtbare `Bad Egg`, `<unknown>`, Unknown-Type-/Unknown-Ability-/Unknown-Item-Marker sowie Placeholder-/Null-Species im Randomizer-Log fuer den getesteten CFRU/DPE Gen9-BPRE-Stand.

Scope:

- Nur bestehende Protokolle und read-only `rg`-Befunde.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine neuen Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, ROM-Namen, Hashes, Secrets oder `.env`-Inhalte gelesen oder dokumentiert.

Dieses Protokoll ist Log-Hygiene. Es erweitert nicht:

- Type-Chart- oder Type-Effectiveness-Support.
- Ability-Namen-/Description-Support.
- Item-Namen-/Description-Support.
- Species-Scope, Forme-Scope oder Placeholder-Filter.
- Randomizer-Writer oder Reload-Verhalten.

## Genutzte Belege

Primaere Belege:

- `047_fvx_gui_options_compatibility_matrix.md`
- `051_base_stats_types_scope_write_diagnostics.md`
- `052_abilities_hidden_ability_scope_write_diagnostics.md`
- `053_p1_item_data_and_bad_item_model.md`
- `054_encounter_held_items_scope_write_diagnostics.md`

Ergaenzende Einordnung aus vorhandenen Protokollen:

- `021_p1_static_gift_species_only.md`
- `023_p1_trainer_species_only.md`
- `024_trainer_scope_write_diagnostics.md`
- `026_evolutions_scope_write_diagnostics.md`
- `031_trainer_movesets_learnsets_fix_diagnostics.md`
- `upr-fvx-cfru-dpe-wild-bad-egg-diagnostics.md`
- `upr-fvx-cfru-dpe-wild-banned-special-species-diagnostics.md`

Read-only `rg`-Befunde bestaetigen Marker in Dokumentation und bestehenden UPR-FVX-Codepfaden:

- `Bad Egg`
- `<unknown>`
- `Unknown-Type`
- `unknown ability`
- `unknown item`
- `Placeholder`
- `Null-Species`
- `BST == 0`
- `unsupportedPrimaryType`
- `skippedPlaceholder`
- `ability #`
- `item #`

## Klassifikation

| Marker / Kategorie | Bestehender Befund | Klassifikation | Blockiert P1-Support in 051/052/054? |
|---|---|---|---|
| `Bad Egg` in 051 | Base Stats-only, Types-only und Base Stats + Types melden `Bad Egg im Log=true`; gleichzeitig `saveSuccessful=true`, `logSuccessful=true`, Output vorhanden, `writeReloadBaseStatsMismatches=0`, `typeIdMismatches=0`. | Erwartetes Placeholder-/Special-Species-Logartefakt im Traits-/BaseStats-/Type-Log. | Nein. |
| Unknown-Type-/`null`-Marker in 051 | `Unknown-Type-Marker=true`, `unsupportedPrimaryTypeBytesBefore=9`, `unsupportedPrimaryTypeBytesReload=9`, `stellarSkippedCount=9`; Type-Write/Reload bleibt mismatch-frei. | Unsupported-Type-/Placeholder-Logmarker, getrennt von Type-Chart und Type-Enum-Erweiterung. | Nein. |
| `Bad Egg` in 052 | Ability1/2 + Hidden Ability und Base Stats + Types + Abilities melden `Bad Egg im Log=true`; Ability-only Direktlaeufe melden `false`. Alle Laeufe reloaden Ability1/2 und Hidden Ability mit `0` Mismatches. | Placeholder-/Special-Species-Logartefakt, sichtbar im kombinierten Trait-/Species-Logging. | Nein. |
| Unknown-Ability-Marker in 052 | Kombinierte Ability-Randomizer-Laeufe melden `unknown ability marker=true`; `unknownAbilityFallbackCount` ist dokumentiert. | Sichtbarer Ability-Namen-Fallback fuer moderne IDs ohne geladenen Namen. Kein Ability-Datenfehler. | Nein. |
| `ability #<id>` | `abilityName()`-Fallbacks sind dokumentiert; 052 haelt fest, dass fehlende Ability-Namen als `ability #<id>` sichtbar bleiben und nicht crashen. | Unknown-Ability-Fallback / Namensabdeckungsthema. | Nein. |
| `Bad Egg` in 054 | Alle vier Encounter-Held-Item-Laeufe melden `Bad Egg=true`; gleichzeitig Save/Log/Output erfolgreich, `writeReloadEncounterHeldItemMismatches=0`, `invalid/missing item IDs=0`. | Bestehendes Placeholder-/Special-Species-Logartefakt, kein Encounter-Held-Item-Write/Reload-Fehler. | Nein. |
| `<unknown>` in 054 | Alle vier Encounter-Held-Item-Laeufe melden `<unknown>=false`. | Kein aktueller Marker in 054. Historische `<unknown>`-Befunde bleiben Nullslot-/Species-Aufloesungsthemen. | Nein. |
| Unknown-Item-Marker in 054 | Alle vier Encounter-Held-Item-Laeufe melden `unknown item marker=false`; Itemname-Fallback-Zaehler ist `0`. | Kein aktueller Encounter-Held-Item-Logmarker in 054. | Nein. |
| `item #<id>` | 053 und 054 beschreiben `item #<id>` als sichtbaren Fallback fuer fehlende/implausible Itemnamen. 054 nutzt Fallback-Items nicht als Random-Picks. | Item-Namen-/Preserve-Fallback, getrennt von Field Items/Shops/Pickup und Item-Text-Support. | Nein, sofern keine Mismatches oder invalid/missing IDs auftreten. |
| `unknown item #<id>` | 026 dokumentiert Evolution-Logger-Fallbacks wie `unknown item #1732`; diese blockierten den Evolution-Fix nicht. | Logger-Fallback fuer unbekannte Item-ExtraInfos, kein Encounter-Held-Item-Modellbeweis. | Nicht relevant fuer 051/052/054. |
| Null-Species / Placeholder-Species | 021 dokumentierte echte Null-Static-Eintraege als frueheren Blocker; 022 fixte diesen Scope. 052/054 dokumentieren defensive Skip-Policy. | Kann echter Blocker sein, wenn ein Randomizer-Pfad dereferenziert oder schreibt; sonst Log-/Scope-Hygiene. | In 051/052/054 nein. |
| `BST == 0` | 052 skippt Species mit `BST == 0`; 023 dokumentierte Zero-Ability-/Zero-BST-Sonder-Species als frueheren Trainer-Blocker. | Potentieller Randomizer-Pool-Blocker, wenn nicht defensiv gefiltert. | In 052/054 nein, weil defensiv behandelt. |
| All-zero Ability Species | 052 meldet `skippedAllZeroAbilitySpecies=2` und `skippedPlaceholderNullSpecies=2`. | Defensive Ability-Randomizer-Scope-Hygiene. | Nein. |

## Echte Save-/Reload-Blocker

Als echte Blocker zaehlen nur dokumentierte Faelle mit fehlendem Save/Log/Output, Stacktrace, direktem Abbruch oder Write/Reload-Mismatch.

Beispiele aus bestehenden Protokollen:

- 021: Static/Gift Species-only blockierte an Null-Species-Eintraegen, bevor stabiler Save/Log/Reload moeglich war.
- 023: Trainer-Species-only blockierte auf Zero-Ability-/Zero-BST-Sonder-Species im Ability-Slot-Auswahlpfad.
- 025/026: Evolution-Species-only hatte vor dem Scope/Write-Fix Logger-/Reload-Probleme; 026 bestaetigte spaeter `writeReloadMismatches=0`.

Nicht als echte Blocker zaehlen die Marker aus 051, 052 und 054, solange gleichzeitig gilt:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- relevanter Write/Reload-Mismatch-Zaehler ist `0`
- `stacktrace=none` oder kein Stacktrace dokumentiert

## Placeholder-/Special-Species-Logartefakte

`Bad Egg` ist im aktuellen Log-Hygiene-Kontext ein sichtbarer Sonder-Species-Name, nicht automatisch ein Save-/Reload-Fehler.

Bekannte Einordnung:

- Wild-Diagnosen zeigten frueher `Bad Egg` als Wild-Replacement-Symptom; der Wild-Special-Species-Ban hat diesen Standard-/Fallback-Wild-Befund beseitigt.
- 051, 052 und 054 zeigen `Bad Egg` weiterhin in Trait-/Species-nahen Logs, ohne die jeweiligen P1-Support-Kriterien zu verletzen.
- 024 dokumentierte `Bad Egg#identity=412#number=252#gen=3#bst=0#abilities=0/0/0` als Pool-Sonderfall, waehrend der Trainer-Log selbst kein `Bad Egg` zeigte.

Fazit: `Bad Egg` muss pro Logbereich klassifiziert werden. Ein sichtbarer Name ist erst dann ein Blocker, wenn er in einem konkreten Randomizer-Pfad zu Abbruch, falschem Write, falschem Reload oder unzulessiger Pool-Auswahl fuehrt.

## Unknown-Type / Unsupported-Type

051 ist der zentrale Beleg:

- `unsupportedPrimaryTypeBytesBefore=9`
- `unsupportedPrimaryTypeBytesReload=9`
- `stellarSkippedCount=9`
- `Unknown-Type-Marker=true`
- `typeIdMismatches=0`

Klassifikation:

- Fairy `0x17` ist im getesteten Scope gelesen und geschrieben.
- Stellar `0x18` bleibt fuer P1 bewusst nicht randomisierbar.
- Species mit nicht representierbarem oder `null` Primary Type werden defensiv uebersprungen.
- Unknown-Type-/`null`-Marker sind deshalb Log-Hygiene oder unsupported-Type-Scope, nicht Type-Chart-Support.

Nicht abgedeckt:

- Type-Chart-Randomization.
- Stellar als FVX-Type-Enum.
- Type-Effectiveness fuer moderne Typen.
- Vollstaendige Placeholder-/Forme-Typisierung.

## Unknown-Ability-Fallbacks

052 ist der zentrale Beleg:

- `abilitiesPerSpecies=3`
- `highestAbilityIndex=254`
- `writeReloadAbilityMismatches=0`
- `writeReloadHiddenAbilityMismatches=0`
- `unknownAbilityFallbackCount` ist in allen Ability-Laeufen sichtbar.
- Kombinierte Ability-Laeufe melden `unknown ability marker=true`, blockieren aber nicht.

Klassifikation:

- `ability #<id>` bedeutet fehlender oder nicht geladener Ability-Name.
- Der Marker ist ein sichtbarer Logger-Fallback, kein Beleg fuer falsche Ability-Bytes.
- Ability1/2 und Hidden Ability bleiben im getesteten Scope P1-supported.

Nicht abgedeckt:

- Vollstaendige moderne Ability-Namen.
- Ability-Descriptions.
- Text/Menu-Support.
- Fachliche Bewertung aller Gen9-Ability-Aliase.

## Unknown-Item / Item-Fallbacks

053 und 054 trennen Itemmodell und Encounter-Held-Item-Fix:

- 053 beschreibt `item #<internalId>` / `item #<standardId>` als noetigen Fallback bei fehlender Itemnamenabdeckung.
- 054 meldet `Itemname-Fallback-Zaehler=0` und `unknown item marker=false` in allen vier Encounter-Held-Item-Laeufen.
- 054 bannt Items mit Fallback- oder implausiblem Namen aus Random-Picks.
- 026 dokumentiert `unknown item #1732` als Evolution-Logger-Fallback fuer unbekannte Item-ExtraInfos.

Klassifikation:

- `item #<id>` ist ein Itemnamen-/Preserve-Fallback.
- `unknown item #<id>` ist ein Logger-Fallback fuer Item-ExtraInfo oder unmodellierte Itemnamen.
- Beide sind von Field Items, Shops, Pickup und Item-Text/Description getrennt zu behandeln.

Nicht abgedeckt:

- Field Items.
- Shops.
- Pickup.
- Allgemeine Item-Randomization.
- Item-Text- oder Description-Rewrites.

## Null-Species / BST-zero / All-zero Ability Species

Diese Kategorie ist die wichtigste Grenze zwischen Log-Hygiene und echten Blockern.

Vorhandene Belege:

- 021: Null-Species im Static/Gift-Scope waren ein echter Blocker.
- 022: Null-Species wurden im Static/Gift-Schreibpfad defensiv behandelt.
- 023: Zero-Ability-/Zero-BST-Sonder-Species blockierten Trainer-Species-only vor Save.
- 052: `skippedPlaceholderNullSpecies=2`, `skippedAllZeroAbilitySpecies=2`, `skippedInvalidAbilityIds=0`.
- 054: `skipped Placeholder-/Null-Species=0` in Encounter Held Items-only; Placeholder-/Null-/BST-zero-Species werden defensiv uebersprungen.
- Fruehere Wild-`<unknown>`-Befunde waren mit `rawInternalSpeciesId=0` als Nullslot-Thema klassifiziert.

Klassifikation:

- Null-Species kann ein echter Blocker sein, wenn ein Pfad sie dereferenziert oder schreibt.
- `BST == 0` und all-zero Ability Species koennen echte Pool-/Randomizer-Blocker sein, wenn sie als normale Species behandelt werden.
- Defensive Skip-Zaehler sind kein Fehler, sondern ein Stabilitaetskriterium.
- `<unknown>` muss getrennt nach Kontext klassifiziert werden: Wild-Nullslot, Logger-Fallback oder fehlende Species-Aufloesung.

## P1-Support-Bewertung fuer 051/052/054

Die Marker aus 051, 052 und 054 blockieren den dokumentierten P1-Support nicht.

| Protokoll | P1-Scope | Marker | Stabilitaetskriterien |
|---|---|---|---|
| 051 | Base Stats + Types | `Bad Egg`, Unknown-Type-/`null`, unsupported Primary Types | Save/Log/Output true; `writeReloadBaseStatsMismatches=0`; `typeIdMismatches=0`; Stacktrace none |
| 052 | Ability1/2 + Hidden Ability | `Bad Egg`, unknown ability marker, `ability #<id>`-Fallbacks | Save/Log/Output true; `writeReloadAbilityMismatches=0`; `writeReloadHiddenAbilityMismatches=0`; no stacktrace |
| 054 | Encounter Held Items | `Bad Egg`; `<unknown>=false`; unknown item marker false | Save/Log/Output true; `writeReloadEncounterHeldItemMismatches=0`; invalid/missing item IDs `0`; stacktrace none |

Damit ist die richtige Folgearbeit nicht ein sofortiger Fix, sondern saubere Trennung:

- Log-Hygiene / sichtbare Namen.
- Placeholder-/Special-Species-Scope.
- Type-Chart-/Type-Enum-Arbeit.
- Ability-Namen-/Textarbeit.
- Item-Namen-/Textarbeit.
- Separate Writer-Modelle fuer noch offene GUI-Bereiche.

## Risiken und Annahmen

- Die Klassifikation nutzt nur vorhandene Markdown-Protokolle und read-only `rg`-Befunde; sie beweist keine neuen ROM-Daten.
- Keine neuen Diagnosewerte wurden erhoben.
- `Bad Egg` kann je nach Pfad harmloses Logartefakt oder echter Pool-Fehler sein; diese Einordnung gilt nur fuer die dokumentierten Befunde.
- `<unknown>` ist historisch meistens ein Nullslot-/Species-Aufloesungsthema, aber der genaue Kontext muss pro Logbereich erhalten bleiben.
- Unknown-Ability- und Unknown-Item-Fallbacks sind sichtbar und absichtlich diagnostisch, ersetzen aber keine vollstaendige moderne Namen-/Textunterstuetzung.

## Ergebnis

Die bestehenden Marker aus Base Stats/Types, Abilities/Hidden Ability und Encounter Held Items sind fuer den getesteten CFRU/DPE Gen9-BPRE-Stand klassifiziert. Sie blockieren den aktuellen P1-Support nicht, solange Save/Log/Output/Reload stabil bleiben und die jeweiligen Mismatch-Zaehler `0` sind.

Naechste sinnvolle Analysebloecke bleiben getrennt:

1. `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`
2. `analysis/upr-fvx-cfru-dpe-p1-field-items-shops-pickup-model`
3. `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`
4. `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`
