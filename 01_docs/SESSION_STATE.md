# Session State

## 2026-05-14 - CFRU/DPE Evolution Same Typing Code Diagnosis

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-evolution-same-typing-blocker-diagnostics`

Aktueller Stand:

- Neues read-only Codeanalyse-Protokoll `08_tests/randomizer/079_p1_evolution_same_typing_code_diagnosis.md` erstellt.
- 079 untersucht konkret den 070-Blocker `FVX-TRAIT-019` Evolutions Same Typing im Carrier `FVX-TRAIT-016` Evolution-Species-Writer.
- Relevante Codepfade sind `GameRandomizer.maybeRandomizeEvolutions()`, `EvolutionRandomizer.randomizeEvolutions()`, `findPossibleReplacements(...)`, `SpeciesSet.filter(...)`, `Species.hasSharedType(...)` und der Gen3 Base-Stats-Type-Read-Scope.
- Wahrscheinlich konkrete Ursache: Der Same-Typing-Filter ruft `to.hasSharedType(...)` auf. Wenn ein Kandidat aus dem Evolution-Replacement-Pool `primaryType == null` hat, dereferenziert `Species.hasSharedType(...)` diesen Null-Type und wirft eine `NullPointerException`.
- Der allgemeine Evolution-Species-Carrier bleibt abgegrenzt: `FVX-TRAIT-016` ist belegt, aber Same Typing nutzt einen zusaetzlichen Species-Type-Filter vor der Zielauswahl.
- `FVX-TRAIT-018` Evolutions Similar Strength bleibt getrennt, weil es nicht denselben `hasSharedType(...)`-Pfad nutzt und in 070 stattdessen Save/Reload mit `writeReloadEvolutionMismatches=24` und `Bad Egg=true` erreichte.
- Ein lokaler Diagnose-Lauf ist fuer die Fixplanung nicht zwingend noetig; ein spaeterer Fix-Smoke fuer `FVX-TRAIT-019` bleibt erforderlich.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Eng gegateten UPR-FVX-Fixbranch fuer `EvolutionRandomizer` Same-Typing-/Null-Primary-Type-Scope vorbereiten. `FVX-TRAIT-018` separat halten und nicht durch denselben Fix als supported hochstufen.

## 2026-05-14 - CFRU/DPE Trainer Type Diversity Null-Type Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`

Aktueller Stand:

- UPR-FVX-Fix `d89fc64e3b0223b03a65466422847dc7df30d03c` erstellt.
- Der Fix bleibt auf `TrainerPokemonRandomizer` begrenzt und behandelt Species mit `primaryType == null` defensiv im Force-Diverse-Types-/`usedTypes`-Pfad.
- Null-Primary-Type-Species werden im erweiterten BPRE-Hack nicht mehr als valide Type-Diversity-/Type-Themes-Replacements genutzt; `EnumSet<Type>` erhaelt keine `null`-Eintraege.
- Bestehende BST-zero-, all-zero-Ability- und Placeholder-/Special-Species-Grenzen bleiben unveraendert.
- `FVX-FOE-009` Trainer Type Diversity / Type Themes wurde lokal sanitisiert ausgefuehrt: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTrainerPokemonMismatches=0`, `filterViolations=0`, `Bad Egg=false`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- Trainer Similar Strength unter `FVX-FOE-001` wurde als Regression lokal sanitisiert ausgefuehrt und bleibt mit Save/Log/Output/Reload true sowie `writeReloadTrainerPokemonMismatches=0` stabil.
- Neues Diagnoseprotokoll `08_tests/randomizer/078_trainer_type_diversity_nulltype_fix_diagnostics.md` erstellt.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit und aktualisiert README, Session, Next Steps, Roadmap, Feature-Coverage und Tool-Manifest.
- Keine Wild-, Evolution-, TypeChart-, MoveData-, Palette-, Item-, Text/Menu-, Graphics-, Trainer-Level-, Additional-Pokemon-, Better-Movesets-, Battle-Style- oder Trainer-Names/Class-Names-Aenderung.

Naechster sinnvoller Schritt:

- UPR-FVX-PR und Workspace-PR reviewen und mergen. Danach die verbleibenden 070-Evolution-Blocker `FVX-TRAIT-018` und `FVX-TRAIT-019` getrennt fortsetzen.

## 2026-05-14 - CFRU/DPE Trainer Type Diversity Code Diagnosis

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-trainer-type-diversity-code-diagnosis`

Aktueller Stand:

- Neues read-only Codeanalyse-Protokoll `08_tests/randomizer/077_p1_trainer_type_diversity_code_diagnosis.md` erstellt.
- 077 untersucht konkret den 070/076-Blocker `FVX-FOE-009` Trainer Type Diversity / Type Themes im Carrier `FVX-FOE-001` Trainer Pokemon.
- Relevante Codepfade sind `GameRandomizer.maybeRandomizeTrainerPokemon()`, `TrainerPokemonRandomizer.randomizeTrainerPokes()`, `pickTrainerPokeReplacement(...)` und `updateUsedTypes(...)`.
- Wahrscheinlich konkrete Ursache: Der Force-Diverse-Types-Pfad schreibt `sp.getPrimaryType(false)` in ein `EnumSet<Type>`. Wenn eine Replacement-Species `primaryType == null` hat, wirft `EnumSet.add(null)` eine `NullPointerException`.
- Der Trainer-Species-Pool filtert im erweiterten BPRE-Hack bereits `BST == 0` und all-zero Ability Species, aber keinen Null-Primary-Type-/unsupported-Type-Scope.
- Trainer Similar Strength ist abgegrenzt: Der stabile 070-Slice nutzt `getRandomSimilarStrengthSpecies(...)`, aktiviert aber nicht den Force-Diverse-Types-/`usedTypes`-Pfad.
- Ein lokaler Diagnose-Lauf ist fuer die Fixplanung nicht zwingend noetig; optional waere er nur fuer sanitisierten Stacktrace-/Null-Primary-Type-Zaehler-Beleg.
- Empfohlen ist ein eng gegateter UPR-FVX-Fixbranch fuer Trainer-Type-Diversity-Null-Type-Scope in `TrainerPokemonRandomizer`, ohne Wild, Evolution, TypeChart, MoveData, Palette, Items, Text/Menu, Graphics oder Level-Modifier.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Fixbranch fuer defensiven Trainer-Type-Diversity-Null-Type-Scope vorbereiten. Danach nur `FVX-FOE-009` und optional Trainer Similar Strength als Regression lokal sanitisiert pruefen.

## 2026-05-14 - CFRU/DPE Trainer Type Diversity Blocker Diagnostics Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-trainer-type-diversity-blocker-diagnostics`

Aktueller Stand:

- Neues read-only Diagnoseplan-Protokoll `08_tests/randomizer/076_p1_trainer_type_diversity_blocker_diagnostics_plan.md` erstellt.
- 076 fokussiert nur den verbliebenen 070-Blocker `FVX-FOE-009` Trainer Type Diversity / Type Themes im Carrier `FVX-FOE-001` Trainer Pokemon.
- Der Befund aus 070 bleibt als echter Save-Blocker klassifiziert: `saveSuccessful=false`, kein Output/Reload, `NullPointerException` und `filterViolations=112` nur bis Abbruch.
- Trainer Similar Strength unter `FVX-FOE-001` bleibt bewusst getrennt, weil dieser Slice in 070 mit Save/Log/Output/Reload true und `writeReloadTrainerPokemonMismatches=0` stabil war.
- Pruefspuren sind Trainer-Type-Diversity-Auswahl gegen Null-Type-, Placeholder-, BST-zero- oder unsupported-Type-Species, Trainer-Pool-Scope, Team-Type-Constraints und fehlende Skip-/Scope-Regeln im Type-Diversity-/Type-Themes-Pfad.
- Spaetere Diagnosemetriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater read-only Code-/Protokollanalysebranch fuer `FVX-FOE-009`, der Trainer-Randomizer- und Type-Diversity-Codepfade identifiziert und den Unterschied zum stabilen Trainer Similar Strength Slice klaert. Kein Fixbranch ohne klare Ursache.

## 2026-05-14 - CFRU/DPE Wild Filter Carrier Nullslot Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`

Aktueller Stand:

- UPR-FVX-Fix `acaada514d04b1d306581ce872d2d77fe1b4c5b3` erstellt.
- Der Fix bleibt auf `WildEncounterRandomizer` begrenzt und behandelt `Encounter`-Slots mit `species == null` defensiv vor der Mapping-/InfoMap-Auswahl.
- Null/unaufloesbare Wild-Encounter-Slots werden nicht als `zoneMap`-/InfoMap-Anker genutzt; sie erhalten ein Replacement aus bestehenden `remaining`-/`allowed`-Pools, mit vorhandener Theme-Grenze und Area-Bans.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary wurden einzeln lokal sanitisiert ausgefuehrt.
- Beide Slices melden `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadWildPokemonMismatches=0`, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`.
- `FVX-WILD-004` meldet `filterViolations=0`; fuer `FVX-WILD-011` wurde kein eigener Filterverletzungszaehler behauptet.
- Die lokalen Fix-Smokes beobachteten `nullSlotsBefore=0` und `nullSlotsAfter=0`; der Fix bleibt trotzdem auf den in 074 identifizierten defensiven Null-/unaufloesbar-Scope begrenzt.
- Neues Diagnoseprotokoll `08_tests/randomizer/075_wild_filter_carrier_nullslot_fix_diagnostics.md` erstellt.
- Workspace pinnt `02_external/upr-fvx` auf den neuen UPR-FVX-Fix-Commit und aktualisiert README, Session, Next Steps, Roadmap, Feature-Coverage und Tool-Manifest.
- Keine TypeChart-, MoveData-, Palette-, Item-, Encounter-Held-Item-, custom-Day/Night-Wild-, Catch-Em-All-, Minimum-Catch-Rate-, Level-Modifier-, Text/Menu- oder Graphics-Aenderung.

Naechster sinnvoller Schritt:

- UPR-FVX-PR und Workspace-PR reviewen und mergen. Danach die restlichen 070-Blocker getrennt fortsetzen: `FVX-FOE-009` Trainer Type Diversity sowie `FVX-TRAIT-018/019` Evolution-Slices.

## 2026-05-14 - CFRU/DPE Wild Filter Carrier Code Diagnosis

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-code-diagnosis`

Aktueller Stand:

- Neues read-only Codeanalyse-Protokoll `08_tests/randomizer/074_p1_wild_filter_carrier_code_diagnosis.md` erstellt.
- 074 untersucht konkret die 070-Wild-Blocker `FVX-WILD-011` und `FVX-WILD-004` im gemeinsamen `FVX-WILD-001` Standard/Fallback-Wild-Carrier.
- Beide Slices nutzen `wildPokemonZoneMod=GAME` und laufen daher durch `WildEncounterRandomizer.InnerRandomizer.game1to1Encounters()` mit `useMapping=true`.
- Wahrscheinlich konkrete Ursache: `setupAreaInfoMap()` baut seine Infos aus `EncounterArea.getSpeciesInArea()`, dieses nutzt `SpeciesSet`, und `SpeciesSet.add(...)` ignoriert `null`; ein nicht aufloesbarer/null Encounter-Slot bleibt aber in `randomizeArea()` erhalten und trifft danach `setupAllowedForReplacementUsingInfoMap()`, das `IllegalStateException("Info was null for encounter's species!")` wirft.
- Damit treffen `FVX-WILD-011` und `FVX-WILD-004` wahrscheinlich denselben InfoMap-/Nullslot-Pfad, bevor Similar-Strength-BST- oder Keep-Primary-Type-Filter fachlich greifen.
- Ein lokaler Diagnose-Lauf ist fuer die Fixplanung nicht zwingend noetig; optional waere er nur fuer sanitisierten Area-/Slot- oder Exception-Message-Beleg.
- Empfohlen ist ein eng gegateter Fixbranch fuer Wild-Mapping-/Nullslot-Scope, ohne TypeChart, MoveData, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level Modifier, Text/Menu oder Graphics.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- PR fuer 074 reviewen und mergen; danach Fixbranch fuer defensiven Wild-Filter-Carrier-/Nullslot-Scope vorbereiten oder optional einen separat freigegebenen lokalen Diagnosebranch fuer sanitisierten Exception-/Area-Beleg starten.

## 2026-05-14 - CFRU/DPE Wild Filter Carrier Diagnostics Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-filter-carrier-diagnostics`

Aktueller Stand:

- Neues read-only Diagnose-/Harness-Planprotokoll `08_tests/randomizer/073_p1_wild_filter_carrier_diagnostics_plan.md` erstellt.
- 073 fokussiert nur `FVX-WILD-011` Wild Similar Strength, `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary und den gemeinsamen `FVX-WILD-001` Standard/Fallback-Wild-Carrier.
- Ausgangsbefunde aus 070 bleiben: beide Wild-Slices sind echte Save-Blocker mit `saveSuccessful=false`, keinem Output/Reload und `IllegalStateException`; `FVX-WILD-004` hatte `filterViolations=0` nur bis Abbruch.
- 073 plant zuerst read-only Code-/Protokollanalyse, um Carrier-Scope von Similar-Strength- und Type-Restriction-Filter-Scope zu trennen.
- Falls vorhandene Dokumente und Codepfade nicht ausreichen, soll eine spaetere lokale Diagnose nur als separater Freigabeschritt erfolgen.
- Hypothesen zu Wild-Nullslot-/Placeholder-Eintraegen, Area-/Encounter-Slot-Scope, leeren oder ungueltigen BST-/Species-Pools, Species-Type-Filtern und strengeren Suboption-Grenzen sind dokumentiert.
- Spaetere Metriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- Keine Codeaenderung, kein Fix, keine Randomizer-Laeufe, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- PR fuer 073 reviewen und mergen; danach read-only Code-/Protokollanalyse fuer den Wild-Filter-Carrier oder, falls nicht ausreichend, ein separat freigegebener lokaler Diagnosebranch.

## 2026-05-14 - CFRU/DPE Wild 070 Blockers Diagnostics Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-wild-070-blockers-diagnostics`

Aktueller Stand:

- Neues read-only Diagnoseplan-Protokoll `08_tests/randomizer/072_p1_wild_070_blockers_diagnostics_plan.md` erstellt.
- 072 plant die gemeinsame Folge-Diagnose fuer `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary.
- Beide Slices bleiben echte Save-Blocker im `FVX-WILD-001` Standard/Fallback-Wild-Carrier: kein Output/Reload und `IllegalStateException`.
- `FVX-WILD-011` wird als BST-/Species-Pool-Filter-Scope plus Wild-Nullslot-/Placeholder-Scope eingeordnet.
- `FVX-WILD-004` wird als Species-Type-Filter-Scope plus Wild-Nullslot-/Placeholder-Scope eingeordnet; `filterViolations=0` aus 070 bleibt nur ein Vor-Abbruch-Befund.
- Gemeinsame Hypothesen sind dokumentiert: Nullslot-/Placeholder-Wild-Entries, Area-/Encounter-Slot-Scope, leere/ungueltige Pools, Placeholder-/Special-/unsupported-Type-Species und strengere Suboption-Vorauswahl trotz P1-supported `FVX-WILD-001` Carrier.
- Spaetere Diagnosemetriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- TypeChart/TypeEffectiveness, MoveData Write, Palette, Items/Field/Shops/Pickup, Encounter Held Items, custom Day/Night-Wild, Catch Em All / Minimum Catch Rate, Level Modifier und Text/Menu/Graphics bleiben ausgeschlossen.
- Keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater read-only Diagnose-/Harness-Plan oder freigegebene read-only Diagnose fuer den Wild-Filter-Carrier; kein Fixbranch ohne klare Ursache.

## 2026-05-14 - CFRU/DPE 070 Blocked Slices Follow-up Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-070-blocked-slices-followup-plan`

Aktueller Stand:

- Neues read-only Planprotokoll `08_tests/randomizer/071_p1_070_blocked_slices_followup_plan.md` erstellt.
- 071 plant die Folgeanalyse fuer die in 070 blockierten Similar Strength / Same Type / Type Themes Slices, ohne Codeaenderung, Fix oder Randomizer-Laeufe.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary werden gemeinsam als Wild-Carrier-/Placeholder-Scope modelliert, weil beide `FVX-WILD-001` Carrier und `IllegalStateException` teilen.
- `FVX-FOE-009` Trainer Type Diversity / Type Themes bleibt ein eigener Trainer-Type-Diversity-/Null-Type-Scope.
- `FVX-TRAIT-018` Evolutions Similar Strength bleibt ein eigener Evolution-Reload-/Bad-Egg-Scope; `Bad Egg` kann dort nicht als reine 055-Log-Hygiene freigegeben werden, solange `writeReloadEvolutionMismatches` ungleich `0` ist.
- `FVX-TRAIT-019` Evolutions Same Typing bleibt ein eigener Evolution-Same-Typing-/Null-Scope.
- Spaetere Diagnosemetriken, Sanitizing-Regeln und Stop-Regeln sind dokumentiert; keine Diagnosewerte wurden erfunden.
- TypeChart/TypeEffectiveness, MoveData Write, Palette, Items/Field/Shops/Pickup, Graphics/Sprites, Text/Menu, Level Modifier und Evolution-Methoden-Writer bleiben ausgeschlossen.
- Keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Separater read-only Diagnoseplan oder Diagnosebranch fuer Wild Similar Strength + Wild Type Restrictions, ohne offene Writer und ohne Fixarbeit.

## 2026-05-14 - CFRU/DPE Similar Strength / Same Type Regression-Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/070_p1_similar_strength_same_type_regression_smoke_results.md` erstellt.
- Die in 069 geplanten Similar-Strength-/Same-Type-/Type-Theme-/Type-Restriction-Slices wurden einzeln lokal ausgefuehrt und sanitisiert dokumentiert.
- Trainer Similar Strength unter `FVX-FOE-001` ist im Trainer-Species-Carrier-Smoke stabil: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTrainerPokemonMismatches=0`, `Bad Egg=false`, `<unknown>=false`, `stacktrace=none`.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary blockieren beim Save mit `IllegalStateException`; kein Output/Reload.
- `FVX-FOE-009` Trainer Type Diversity / Type Themes blockiert beim Save mit `NullPointerException`; kein Output/Reload.
- `FVX-TRAIT-018` Evolutions Similar Strength speichert und reloadet, meldet aber `writeReloadEvolutionMismatches=24` und `Bad Egg=true`; der Marker wird wegen der Mismatches nicht als unkritischer 055-Marker freigegeben.
- `FVX-TRAIT-019` Evolutions Same Typing blockiert beim Save mit `NullPointerException`; kein Output/Reload.
- TypeChart/TypeEffectiveness, MoveData Write, Field Items/Shops/Pickup, Encounter Held Items, Palette/Graphics, Text/Menu, Level-Modifier, Evolution-Methoden-Writer, Starter Held Items, Race Mode / Intro Mon, Better Movesets, Trainer Additional Pokemon, Battle Style, Trainer Names/Class Names, Catch Em All, Minimum Catch Rate, Wild held items und custom Day/Night-Wild blieben ausgeschlossen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.
- Lokale ROM-, Log-, Output-ROM-, Build- und Diagnoseartefakte blieben ignored und werden nicht committed oder dokumentiert.

Naechster sinnvoller Schritt:

- Read-only Diagnoseplan fuer die blockierten 070-Slices: Wild Similar Strength/Type Restrictions gegen Wild-Nullslot-/Placeholder-Scope, `FVX-FOE-009` gegen Trainer-Type-Diversity-/Null-Type-Scope und `FVX-TRAIT-018/019` gegen Evolution-Reload-Mismatches, `Bad Egg` und Null-Evolution-Scope.

## 2026-05-14 - CFRU/DPE Similar Strength / Same Type Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/069_p1_similar_strength_same_type_regression_smoke.md` erstellt.
- 069 plant spaetere Regression-Smokes fuer BST-/Type-basierte Poolfilter: Similar Strength, Same Type / Same Typing, Type Themes und Type Restrictions.
- Geplante Slices: `FVX-WILD-011` Wild Similar Strength, `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary, Trainer Similar Strength konservativ als Suboption unter `FVX-FOE-001`, `FVX-FOE-009` Trainer Type Diversity / Type Themes, `FVX-TRAIT-018` Evolutions Similar Strength und `FVX-TRAIT-019` Evolutions Same Typing.
- Geeignete Carrier sind `FVX-WILD-001` Standard/Fallback Wild, `FVX-FOE-001` Trainer Pokemon und `FVX-TRAIT-016` Evolution Randomization.
- 069 nutzt Species-Pools, BaseStats/BST und Species-Type-Felder aus belegten Datenpfaden; Same Type / Type Themes beweisen keinen TypeChart- oder TypeEffectiveness-Support.
- Starter-Type/BST aus 065 und `FVX-SST-012` Static Similar Strength bleiben nur Referenz-/Vergleichsbelege, nicht primaerer Scope.
- TypeChart/TypeEffectiveness, MoveData Write, Field Items/Shops/Pickup, Encounter Held Items, Palette/Graphics, Text/Menu, Level-Modifier, Evolution-Methoden-Writer, Starter Held Items, Race Mode / Intro Mon, Better Movesets, Trainer Additional Pokemon, Battle Style, Trainer Names/Class Names, Catch Em All, Minimum Catch Rate, Wild held items und custom Day/Night-Wild bleiben ausgeschlossen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`: die in 069 geplanten Wild-, Trainer- und Evolution-Slices einzeln lokal ausfuehren und sanitisiert dokumentieren, weiter ohne offene Writer.

## 2026-05-14 - CFRU/DPE TypeEffectiveness Follow-up Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/068_type_effectiveness_followup_smoke_results.md` erstellt.
- Die in 067 geplanten TypeEffectiveness-Folgesmokes wurden einzeln lokal ausgefuehrt und sanitisiert dokumentiert: `FVX-TYPE-001` Balanced, Keep Type Identities und Inverse, `FVX-TYPE-002` Add Random Immunities sowie `FVX-TYPE-003` Update Type Effectiveness.
- Alle fuenf Slices melden `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTypeChartMismatches=0` und `stacktrace=none`.
- Foresight- und Endtable-Terminatoren blieben in allen Slices erhalten.
- Unsupported/Stellar wurde in keinem Slice eingefuehrt oder still normalisiert.
- `Bad Egg=false` und `<unknown>=false` in allen Slice-Logs.
- Balanced erzeugte Fairy-Rohtriplets und reloadete sie als raw `0x17`; Keep Type Identities, Inverse, Add Random Immunities und Update Type Effectiveness erzeugten keine Fairy-Rohtriplets und kein Fehlmapping.
- `FVX-TYPE-002` Add Random Immunities wurde getrennt als eigener Risikopunkt getestet.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein Tool-Manifest-Update.
- Lokale ROM-, Log-, Output-ROM-, Build- und Diagnoseartefakte blieben ignored und werden nicht committed.

Naechster sinnvoller Schritt:

- PR fuer `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes` reviewen und mergen; danach zu `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke` zurueckkehren oder einen offenen Writer separat freigeben.

## 2026-05-14 - CFRU/DPE TypeEffectiveness Follow-up Smoke Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/067_type_effectiveness_followup_smoke_plan.md` erstellt.
- Der gemergte TypeChart-Fix aus Diagnose 066 bleibt Referenz: TypeEffectiveness-only Random war Save/Log/Output/Reload-stabil, `writeReloadTypeChartMismatches=0`, Fairy reloadete als raw `0x17`, unsupported/Stellar wurde nicht eingefuehrt oder still normalisiert und Terminatoren blieben erhalten.
- 067 stellt klar, dass der Random-Smoke aus 066 die Einzelpruefung weiterer TypeEffectiveness-GUI-Modi nicht ersetzt.
- Geplante spaetere Slices: `FVX-TYPE-001` Balanced, `FVX-TYPE-001` Keep Type Identities, `FVX-TYPE-001` Inverse, `FVX-TYPE-002` Add Random Immunities und `FVX-TYPE-003` Update Type Effectiveness.
- `FVX-TYPE-002` Add Random Immunities bleibt als eigener Risikopunkt getrennt geplant.
- Gemeinsame spaetere Erfolgskriterien dokumentiert: Save/Log/Output/Reload true, `writeReloadTypeChartMismatches=0`, Fairy raw `0x17`, unsupported/Stellar nicht eingefuehrt oder normalisiert, Foresight-/Endtable-Terminatoren erhalten, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`.
- MoveData, Palette-Randomization, Items/Field Items/Shops/Pickup, Graphics/Sprites, Text/Menu und Species-Type-Write bleiben ausgeschlossen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- Spaeterer Test-/Diagnosebranch fuer die geplanten TypeEffectiveness-Folgesmokes, der die Slices einzeln ausfuehrt und sanitisiert dokumentiert, oder Rueckkehr zu `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`.

## 2026-05-14 - CFRU/DPE TypeChart Preserve Effectiveness Fix

Workspace-Branch: `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness`

Aktueller Stand:

- UPR-FVX-Fix `36707e0190d3d9fa587550dfc5631fcaa9abd6b1` erstellt.
- Der Fix trennt TypeChart-raw-Type-Mapping von `gBaseStats`-Type-Mapping: Fairy `0x17` wird im CFRU/DPE-TypeChart gelesen und geschrieben, waehrend Stellar/raw `0x18` unsupported bleibt.
- Unsupported raw TypeChart-Triplets werden preserve-/skip-only behandelt und nicht still auf Normal, Fairy oder null normalisiert.
- Foresight-Block und Endtable-Terminator bleiben erhalten; die CFRU/DPE-Kapazitaetspruefung nutzt den vorhandenen TypeChart-Bereich.
- Neues Diagnoseprotokoll `08_tests/randomizer/066_type_chart_preserve_effectiveness_fix_diagnostics.md` erstellt.
- TypeEffectiveness-only Smoke: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, Reload erfolgreich, `writeReloadTypeChartMismatches=0`, `fairyNonNeutralReload=13`, `rawFairyEntriesReload=13`, `unsupportedRawEntriesPreserved=true`, Terminatoren erhalten und `stacktrace=none`.
- `Bad Egg=false` und `<unknown>=false` im TypeEffectiveness-only Log.
- Keine Species-Type-Write-Aenderung aus 051, kein STELLAR-Enum, keine MoveData-, Palette-, Item-, Graphics- oder Text/Menu-Aenderung.
- Workspace dokumentiert den neuen UPR-FVX-Submodule-Pin; lokale Diagnoseartefakte bleiben ignored und werden nicht committed.

Naechster sinnvoller Schritt:

- PRs fuer UPR-FVX-Fix und Workspace-Submodule-/Diagnoseupdate pruefen; danach optional einzelne TypeEffectiveness-Folgesmokes fuer Balanced, Keep Identities, Inverse/Add Immunities und Update Type Effectiveness planen.

## 2026-05-14 - CFRU/DPE Starters Suboptions Regression-Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/065_p1_starters_suboptions_regression_smoke_results.md` erstellt.
- Die lokal ausgefuehrten 063-Slices wurden sanitisiert dokumentiert: Baseline `FVX-SST-002`, `FVX-SST-003` basic with 2 evolutions, `FVX-SST-004` any basic, `FVX-SST-005` type restrictions, `FVX-SST-006` no legendaries und `FVX-SST-009` BST min/max.
- Alle sechs Slices melden Save/Log/Reload true, `Starter-Mismatches=0`, `Filterverletzungen=0` und `stacktrace=none`.
- `Bad Egg=false` und `<unknown>=false` in allen Slice-Logs.
- Starter Held Items `FVX-SST-007`/`FVX-SST-008`, MoveData Write, Field Items/Shops/Pickup, Palette-Randomization, TypeChart und Text/Menu/Graphics blieben aus.
- `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` wurden konservativ als getestet im Starter-Species-Writer-Smoke dokumentiert, nicht als globale Vollabdeckung fuer Wild-/Trainer-/Evolution-Kombinationen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe im Dokumentationsblock, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`: BST-/Type-basierte Pooling-Suboptionen pruefen, ohne TypeChart oder MoveData-Write zu aktivieren.

## 2026-05-14 - CFRU/DPE Global Species Pool Regression-Smoke Results

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke`

Aktueller Stand:

- Neues Ergebnisprotokoll `08_tests/randomizer/064_p1_global_species_pool_regression_smoke_results.md` erstellt.
- Die lokal ausgefuehrten 062-Slices wurden sanitisiert dokumentiert: Baseline Carrier, `FVX-GEN-001` Generation Limits, `FVX-GEN-001` related Pokemon und `FVX-GEN-002` No Premature Evolutions.
- Alle vier Slices melden Save/Log/Reload true, `Starter-Mismatches=0` und `stacktrace=none`.
- `Bad Egg` und `<unknown>` traten in den Slice-Logs nicht auf.
- Aktiv war nur `FVX-SST-002` als Starter-Species-Carrier plus jeweiliger Poolfilter.
- Held Items, MoveData-Write, Palette-Randomization, TypeChart, Evolution-Methoden-Fixes und Intro/Race Mode blieben aus.
- `FVX-GEN-001` und `FVX-GEN-002` wurden konservativ als getestet im Starter-Carrier-Smoke dokumentiert, nicht als globale Vollabdeckung fuer Wild-/Trainer-/Evolution-Kombinationen.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe im Dokumentationsblock, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`: die in 063 geplanten Starter-Suboptions-Slices lokal ausfuehren, weiter ohne Starter Held Items und ohne offene Writer.

## 2026-05-14 - CFRU/DPE Starters Suboptions Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/063_p1_starters_suboptions_regression_smoke.md` erstellt.
- Starter-Suboptionen aus Diagnose 061/062 ueber den belegten Starter-Species-Writer geplant.
- `FVX-SST-002` bleibt nur belegter Basis-/Carrier-Pfad.
- Geplante Slices dokumentiert: `FVX-SST-003`/`FVX-SST-004` Basic-/Evolution-Filter, `FVX-SST-005` Type Restrictions, `FVX-SST-006` Legendary Filter und `FVX-SST-009` BST-Min/Max separat.
- Starter Held Items `FVX-SST-007`/`FVX-SST-008`, Field Items/Shops/Pickup, Encounter Held Items, MoveData Write, Palette/Graphics, TypeChart, Text/Menu, Level Modifier und Evolution-Methoden-Writer bleiben ausgeschlossen.
- Erwartete spaetere Metriken, Artefaktregeln und Stop-Regeln dokumentiert; keine Hochstufung der Starter-Suboptionen auf P1-supported ohne separaten spaeteren Lauf.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`: BST-/Type-basierte Pooling-Suboptionen planen, ohne TypeChart oder MoveData-Write zu aktivieren.

## 2026-05-14 - CFRU/DPE Global Species Pool Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/062_p1_global_species_pool_regression_smoke.md` erstellt.
- Erster konkreter Regression-Smoke aus Diagnose 061 fuer Global Species Pools / Generation Limits geplant.
- Primaere Feature-IDs festgelegt: `FVX-GEN-001` Limit Pokemon und `FVX-GEN-002` No Premature Evolutions.
- Generation Limits und related-Pokemon-Scope werden unter `FVX-GEN-001` gefuehrt, weil keine separaten Feature-IDs existieren.
- `FVX-GEN-003` No Random Intro Mon und `FVX-GEN-004` Race Mode sind ausdruecklich nicht Teil dieses Smokes.
- Minimaler Carrier fuer spaetere Laeufe ist ein einzelner P1-stabiler Species-Writer, bevorzugt `FVX-SST-002`; optionaler Wild-Vergleich gegen `FVX-WILD-001` bleibt separat.
- Spaetere Smoke-Slices, erlaubte Settings, ausgeschlossene offene Writer, erwartete Metriken, Artefaktregeln und Stop-Regeln dokumentiert.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke`: Starter-Poolfilter wie random basic/two evolutions, Type Restrictions, No Legendaries und BST-Min/Max getrennt von Starter-Held-Items planen.

## 2026-05-13 - CFRU/DPE P1 Regression-Smoke-Plan

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/061_p1_regression_smoke_plan.md` erstellt.
- Priorisierte Smoke-Gruppen aus Diagnose 060 und der FVX Feature-Coverage-Matrix abgeleitet.
- Feature-Coverage mit `130` Feature-/Suboption-Zeilen eingebunden; spaetere Smokes sollen Feature-IDs referenzieren.
- Smoke-Gruppen festgelegt: Global Species Pools / Generation Limits, Similar Strength / Same Type Pooling, Evolutions-Suboptionen ohne offene Method-/Item-/Move-Writer, Starters, Movesets/TM/Tutor/Egg, Trainer Level Modifier separat und Wild Level Modifier separat.
- Offene Writer explizit als Nicht-Smoke-Fixbereiche markiert: MoveData Write, Field Items/Shops/Pickup, Palette Randomization, TypeChart, Graphics/Sprites und Text/Menu.
- Allgemeine spaetere Metriken definiert: Save/Log/Output/Reload, relevanter Mismatch-Zaehler `0`, `stacktrace=none`, keine verbotenen Artefakte und Marker nur nach 055 klassifizieren.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke`: erster spaeterer Regression-Smoke fuer `Limit Pokemon`, Generation Limits und related Pokemon, strikt ohne offene Writer.

## 2026-05-13 - CFRU/DPE GUI-Suboptions-Regressionsmatrix

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-gui-suboptions-regression-matrix`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md` erstellt.
- Konkrete FVX-GUI-Hauptoptionen und Suboptionen wurden gegen den aktuellen CFRU/DPE-P1-Supportstand eingeordnet.
- Statusklassen festgelegt: `P1-supported`, `wahrscheinlich supported, aber nicht einzeln getestet`, `modelliert, Fix offen`, `open-not-diagnosed` und `out of scope`.
- Direkt belegte Datenpfade wurden von nur wahrscheinlich stabilen Suboptionen, modellierten offenen Writern und ungetesteten GUI-Kombinationen getrennt.
- Similar Strength, Same Type / Prefer Same Type, Follow Evolutions, Level Modifier, Force Change, Change Impossible Evolutions und Make Evolutions Easier wurden konservativ nach Datenpfad- und Writer-Risiko eingeordnet.
- Diagnose 055 bleibt Log-Hygiene-Grenze, 056 MoveData-Grenze, 057 Field-/Shop-/Pickup-Grenze, 058 Palette-/Graphics-Grenze und 059 TypeChart-Grenze.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan`: read-only Smoke-/Regression-Plan fuer priorisierte Suboptionen erstellen, bevor mehrere offene Writer in einem Fixbranch vermischt werden.

## 2026-05-13 - CFRU/DPE Type-Chart-Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/059_p1_type_chart_model.md` erstellt.
- Pokemon-Type-Read/Write aus Diagnose 051 wurde strikt von Type-Chart-/Effectiveness-Randomization getrennt.
- Klar dokumentiert: 051 beweist `gBaseStats`-Type-Read/Write inklusive Fairy `0x17` und `typeIdMismatches=0`, aber keinen Type-Chart-Support.
- Fairy `0x17` in Species-Daten wurde von Fairy-Effectiveness-Eintraegen in der TypeTable getrennt.
- Stellar `0x18` bleibt unsupported/preserve-only und darf nicht stillschweigend in Random-Pools oder TypeChart-Writes eingefuehrt werden.
- `TypeEffectivenessRandomizer`, `getTypeTable()`/`setTypeTable()`, `TypeEffectivenessOffset`, Foresight-/End-Table-Terminatoren und `nonNeutralEffectivenessCount` wurden als eigener Hochrisiko-Writer klassifiziert.
- Preserve-/Skip-Policy und Reload-/Diagnosekriterien fuer spaetere TypeChart-Fixbranches festgelegt.
- Diagnose 058 bleibt Palette-Grenze, 057 Item-/Field-/Shop-/Pickup-Grenze, 056 MoveData-Grenze und 055 Log-Hygiene-Grenze.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-gui-suboptions-regression-matrix`: GUI-Suboptionen nach den read-only Modellen 055-059 regressionsorientiert konsolidieren.

## 2026-05-13 - CFRU/DPE Palette-Randomization-Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/058_p1_palette_randomization_model.md` erstellt.
- Bestehende Palette-Safety wurde strikt von echter geaenderter Palette-Randomization getrennt.
- Safety-Stand eingeordnet: defensiver `loadPokemonPalettes()` fuer missing/invalid Slots und Skip-Unchanged-`savePokemonPalettes()` fuer unveraenderte CFRU/DPE-Pokemon-Paletten.
- Klar dokumentiert: `PokemonPalettesMod.RANDOM` und `Gen3to5PaletteRandomizer` sind echte Writer-Pfade und nicht durch die Safety-Diagnosen als P1-supported belegt.
- `savePokemonPalettes()`, `rewriteCompressedPalette()` und der komprimierte `DataRewriter`-Repointing-Pfad wurden als offene Hochrisiko-Writer klassifiziert.
- Shared/missing Palette-Pointer-Risiken dokumentiert, inklusive `SPECIES_CUBONE_A`-/`gMonPaletteTable[1038]`-Nullslot, DPE-Gap-Slots `[252]..[276]` und `gFrontSprite252Pal`/`gBackShinySprite252Pal`.
- Preserve-/Skip-Policy und Reload-/Diagnosekriterien fuer spaetere Palette-Fixbranches festgelegt.
- Graphics/Sprites bleiben ein eigenes P2-Modell; keine Vermischung mit Pokemon-Palette-Randomization.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`: Type-Chart- und moderne Type-Interaktion getrennt von Pokemon-Type-Read/Write modellieren.

## 2026-05-13 - CFRU/DPE Field Items / Shops / Pickup Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-field-items-shops-pickup-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md` erstellt.
- Field Items, Shops, Pickup und allgemeine Item-Randomization wurden strikt von Encounter Held Items aus Diagnose 054 getrennt.
- Item-Scope-Stand aus 053/054 eingeordnet: klassischer FVX-FRLG-`ItemCount=374`, CFRU-naher Scope bis `778`/`779`, DPE-Header-Scope bis ca. `799`, getesteter 054-Scope `item.count=778`.
- Field-Item-Risiken dokumentiert: Map-/Script-Kontext, required field TMs, moderne TM/HM-Items, Key-/System-/Placeholder-Items und eigener Reload-Nachweis.
- Shop-Randomization-Risiken dokumentiert: `ShopPointerOffsets`, Special-/Main-Game-Shop-Scope, Shopgroessen, Preise, Guaranteed Items und Text/Menu-Grenze.
- Pickup-Risiken dokumentiert: klassischer `PickupTableStartLocator`/`PickupItemCount`, CFRU `sPickupCommonItems`/`sPickupRareItems`, Probability-Slots und moderne Item-Pools.
- Preserve-/Skip-Policy und Reload-/Diagnosekriterien fuer spaetere Fixbranches festgelegt.
- Diagnose 055 bleibt Log-Hygiene-Grenze; Diagnose 056 bleibt Move-Data-Write-Grenze.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`: Vorhandene Palette-Safety von echter Palette-/Graphics-Randomization trennen und Write-/Repointing-Risiken modellieren.

## 2026-05-13 - CFRU/DPE Move-Data-Write-Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/056_p1_move_data_write_model.md` erstellt.
- Der aktuelle Move-Data-Read-Stand wurde aus vorhandenen Diagnosen eingeordnet: `moves.total=992`, hoechster geladener Move `991:PsychicNoise`, Category-Verteilung aus Diagnose 034.
- Das CFRU/DPE-`BattleMove`-Layout wurde als 12-Byte-Entry mit `split` bei Byte `+10` dokumentiert.
- Der aktuelle Gen3-`saveMoves()`-Pfad wurde read-only klassifiziert: Move-Namen und die ersten fuenf MoveData-Bytes werden geschrieben; `secondaryEffectChance`, `target`, `priority`, `flags`, `z_move_power`, `split` und `z_move_effect` bleiben nicht als Writer modelliert.
- Preserve-Policy und Reload-Kriterien fuer einen spaeteren Move-Data-Write-Fix wurden festgelegt.
- Diagnose 055 bleibt die Grenze: Log-Hygiene/Fallback-Marker sind getrennt von echten MoveData-Writer-/Scope-Risiken.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe, kein Tool-Manifest-Update.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-field-items-shops-pickup-model`: Field Items, Shops, Pickup und allgemeine Item-Randomization getrennt von Encounter Held Items modellieren.

## 2026-05-13 - CFRU/DPE Type Log / Placeholder Hygiene

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-type-log-placeholder-hygiene`

Aktueller Stand:

- Neues read-only Analyseprotokoll `08_tests/randomizer/055_type_log_placeholder_hygiene.md` erstellt.
- `Bad Egg`, `<unknown>`, Unknown-Type-/Unknown-Ability-/Unknown-Item-Marker und Placeholder-/Null-Species wurden strikt aus bestehenden Protokollen und read-only `rg`-Befunden klassifiziert.
- Die Marker aus 051/052/054 blockieren den dokumentierten P1-Support nicht, solange Save/Log/Output/Reload stabil bleiben und die jeweiligen Mismatch-Zaehler `0` sind.
- Echte Blocker bleiben getrennt: Null-Species-/BST-zero-/all-zero-Ability-Species sind nur dann Blocker, wenn ein konkreter Randomizer-Pfad abbricht, falsch schreibt oder falsch reloadet.
- Log-Hygiene wurde getrennt von Type-Chart-, Ability-Name-, Item-Name-, Species-Scope- und Fix-Themen dokumentiert.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, keine neuen Randomizer-Laeufe.

Naechster sinnvoller Schritt:

- `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model`: Move-Data-Write fuer `moves.total=992`, `BattleMove.split` und CFRU/DPE-Felder read-only modellieren.

## 2026-05-13 - CFRU/DPE Encounter Held Items Scope-and-Write Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`

Aktueller Stand:

- Workspace PR #91 als gemerged geprueft.
- UPR-FVX-Fix `5c7170b654b09e1fc27ced6857dd50a8e4711f08` erstellt.
- CFRU/DPE-gegateter Item-Scope implementiert: DPE-Oberregion bis `798` wird nur bei plausiblen Itemnamen genutzt, sonst konservativer Scope bis `778`.
- Itemnamen-Fallbacks bleiben sichtbar als `item #<id>` und werden nicht als Random-Pick zugelassen.
- Moderne Bad-/Banned-Filter fuer Encounter Held Items ergaenzt: TMs/HMs, Mail, Balls, Free-/Placeholder-/Shiny-Space, Booster Energy, Tera Orb, Portable PC und modellierte Form-/Mega-/Z-/Plate-/Mask-/Utility-Items.
- Encounter Held Items in `gBaseStats` bei `item1/item2` (`0x0C`/`0x0E`) werden read/write/reload-stabil behandelt; moderne bestehende IDs werden preserved statt zu `0` zu kollabieren.
- Neues Diagnoseprotokoll `08_tests/randomizer/054_encounter_held_items_scope_write_diagnostics.md` erstellt.
- Encounter Held Items-only, Encounter Held Items + Base Stats, + Abilities und + Types liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true` und `writeReloadEncounterHeldItemMismatches=0`.
- Keine Field-Items-, Shops-, Pickup-, Move-Data-, Tutor-, Egg-Move-, Palette/Graphics-, Type-Chart- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs einen der offenen Matrixbereiche modellieren: Move-Data-Write, Field Items/Shops/Pickup, Palette/Graphics, Type-Chart oder Placeholder-/Bad-Egg-Log-Hygiene.

## 2026-05-13 - CFRU/DPE Item-/Bad-Item-/Encounter-Held-Item Modell

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-item-data-and-bad-item-model`

Aktueller Stand:

- Workspace PR #90 und UPR-FVX PR #27 als gemerged geprueft.
- Neues read-only Analyseprotokoll `08_tests/randomizer/053_p1_item_data_and_bad_item_model.md` erstellt.
- CFRU/DPE Itemgrenzen eingeordnet: CFRU-naher Scope bis `ITEM_FREE_SPACE3=778` / `ITEMS_COUNT=779`, DPE-Header-Scope bis `ITEM_SHINY_SPACE20 + 1` / ca. `799`.
- FVX-Risiko dokumentiert: klassischer FireRed `ItemCount=374`, `itemIDToStandard(...)`-Fallback ueber `UNIQUE_OFFSET` und unvollstaendige moderne Itemnamen-/Bad-Item-Abdeckung.
- Encounter Held Items liegen in `gBaseStats` als `u16 item1/item2` bei Offsets `0x0C/0x0E`; Felder sind eng fixbar, aber nicht sicher ohne erweiterten Item-Scope und moderne Bad-/Key-Item-Filter.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.

Naechster sinnvoller Schritt:

- Fixbranch `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`: CFRU/DPE-gated ItemCount-/Itemnamen-Scope, moderne Bad-/Banned-Item-Filter und Encounter-Held-Item-Read/Write/Reload diagnostisch absichern.

## 2026-05-13 - CFRU/DPE Abilities + Hidden Ability Scope-and-Write Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-abilities-hidden-ability-scope-and-write`

Aktueller Stand:

- Workspace PR #89 und UPR-FVX PR #26 als gemerged geprueft.
- UPR-FVX-Fix `639c7e61adbeffea2e29b1d0dafdba8a02a83f89` erstellt.
- CFRU/DPE-gegatetes Ability-Modell implementiert: Ability1/2 bleiben bei BaseStats-Offsets `0x16/0x17`, Hidden Ability wird bei Offset `0x1A` gelesen/geschrieben.
- CFRU/DPE meldet `abilitiesPerSpecies=3` und `highestAbilityIndex=254` / `0xFE`.
- Ability-Namen werden bis `0xFE` geladen; fehlende moderne Namen fallen sichtbar auf `ability #<id>` zurueck.
- `SpeciesAbilityRandomizer` skippt Placeholder-/Null-Species, `BST == 0`, all-zero-Ability-Species und invalid Ability-IDs defensiv.
- Neues Diagnoseprotokoll `08_tests/randomizer/052_abilities_hidden_ability_scope_write_diagnostics.md` erstellt.
- Ability1/2-only, Hidden Ability-only, Ability1/2 + Hidden Ability und Base Stats + Types + Abilities liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `writeReloadAbilityMismatches=0` und `writeReloadHiddenAbilityMismatches=0`.
- Keine Encounter-Held-Item-, Move-Data-Write-, Tutor-, Egg-Move-, Palette/Graphics-, Type-Chart- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Item-/Bad-Item-Modell fuer Encounter Held Items starten oder vorher Placeholder-/Unknown-Type-/Bad-Egg-Log-Hygiene separat einordnen.

## 2026-05-13 - CFRU/DPE Base Stats + Types Scope-and-Write Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write`

Aktueller Stand:

- Workspace PR #88 als gemerged geprueft.
- UPR-FVX-Fix `20f16d07ab4ea62e5cd3f27ef09a6d5b036d2392` erstellt.
- CFRU/DPE-gegatetes BaseStats-Type-Mapping implementiert: raw `0x17` wird als `Type.FAIRY` gelesen und `Type.FAIRY` als `0x17` geschrieben.
- CFRU/DPE-TypeTable-Pool enthaelt Fairy, aber kein Stellar; Stellar-/unsupported Primary-Type-Species werden im Type-Randomizer defensiv uebersprungen.
- Neues Diagnoseprotokoll `08_tests/randomizer/051_base_stats_types_scope_write_diagnostics.md` erstellt.
- Base Stats-only, Types-only und Base Stats + Types liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `writeReloadBaseStatsMismatches=0` und `typeIdMismatches=0`.
- Keine Hidden-Ability-, Encounter-Held-Item-, Move-Data-Write-, Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Hidden Abilities separat fixen oder vorher Item-/Bad-Item-Modell fuer Encounter Held Items starten.

## 2026-05-13 - CFRU/DPE Base Stats, Types, Abilities Model

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model`

Aktueller Stand:

- UPR-FVX PR #25 und Workspace PR #87 als gemerged geprueft.
- Neues read-only Protokoll `08_tests/randomizer/050_p1_base_stats_types_abilities_model.md` erstellt.
- `gBaseStats` fuer den getesteten CFRU/DPE Gen9-BPRE-Stand modelliert: Pointer-Ort `0x080001BC`, Entry-Size `0x1C`, internes Species-Indexing bis `SPECIES_PECHARUNT=0x59F` / `NUM_SPECIES=1440`.
- CFRU BaseStats-Felder eingeordnet: Stats, `type1/type2`, `item1/item2`, `ability1/ability2` und `hiddenAbility` bei Offset `0x1A`.
- FVX-Risiken dokumentiert: Gen3-Type-Mapping liest/schreibt Fairy aktuell nicht korrekt, Stellar ist nicht im FVX-Type-Enum, Hidden Ability wird nicht gelesen/geschrieben, Ability-Count ist `77` statt CFRU `255`, Encounter Held Items haengen am erweiterten Itemmodell.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein ROM-/Build-/Log-Artefakt.

Naechster sinnvoller Schritt:

- `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write` als kleinen ersten Fixbranch planen.
- Hidden Abilities und Encounter Held Items getrennt behandeln; Encounter Held Items erst nach Item-/Bad-Item-Modell.

## 2026-05-13 - CFRU/DPE Learnset GUI Flow Safety Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`

Aktueller Stand:

- UPR-FVX-Fix `086d2a9177df7624a0e7ca1876b210a200d7aa98` erstellt.
- Logger-Nullsafety, Learnset-Repointing-Multiwrite-Safety, Trainer-Movesets-Key-Fallbacks sowie TM/HM-/Tutor-Level-Up-Sanity defensiv stabilisiert.
- Neues Protokoll `08_tests/randomizer/049_p1_learnset_gui_flow_safety_fix_diagnostics.md` erstellt.
- Sieben GameRandomizer-nahe Movesets/Learnsets-Laeufe diagnostiziert: Movesets-only, Trainer-Movesets, Reorder-Damaging, TM/HM-Sanity, Tutor-Sanity, gekoppelte Egg Moves und TM/HM+Tutor-Sanity.
- Alle Laeufe liefern `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true` und `writeReloadLearnsetMismatches=0`.
- Reorder-Damaging nutzt zwei freie Learnset-Blob-Bloecke innerhalb `0x1219A48-0x1600000`; der zweite Write blockiert nicht mehr an einem statischen FreeSpace-Start.
- Keine Move-Data-Write-, Tutor-Text/Menu-, Special-Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.
- Danach Move-Data-Write, Items/Shops/Field, Palette/Graphics und Special-Tutor/Text/Menu separat modellieren.

## 2026-05-13 - CFRU/DPE Learnset GUI Combination Diagnostics

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-learnset-gui-combinations`

Aktueller Stand:

- UPR-FVX PR #24 und Workspace PR #85 als gemerged geprueft.
- Neues Protokoll `08_tests/randomizer/048_p1_learnset_gui_combinations.md` erstellt.
- GameRandomizer-nahe Movesets/Learnsets-Laeufe diagnostiziert; keine Codeaenderung und keine `02_external/**`-Aenderung.
- Erster Learnset-Repointing-Write bleibt stabil: `plannedBlobBytes=30099`, `writtenBlobBytes=31771`, `pointertableEntriesUpdated=1413`, `writeReloadLearnsetMismatches=0`.
- Movesets-only, Movesets+TM/HM ohne Level-Up-Sanity, Movesets+Tutor ohne Level-Up-Sanity und gekoppelte Egg Moves speichern/reloaden stabil.
- Voller GUI-P1-Support bleibt blockiert durch Logger-Fehler, Trainer-Movesets-Kombinationen, Reorder-Damaging-Moves sowie TM/HM-/Tutor-Level-Up-Sanity.

Naechster sinnvoller Schritt:

- Fixbranch `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety` starten.
- Ziele: multi-write-sicheren Learnset-Repointing-Pfad, interne Species-ID-Key-Fallbacks fuer Sanity/Trainer-Movesets und Logger-Nullpfad beheben.


## 2026-05-13 - CFRU/DPE Learnset-Write Repointing Fix

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`

Aktueller Stand:

- UPR-FVX-Fix `77de517da880bebb6ed690ca6e170e5bd10b9cad` erstellt.
- `setMovesLearnt()` schreibt fuer den eng gegateten CFRU/DPE Gen9-BPRE-Pfad neue Level-Up-Learnset-Blobs in die validierte FreeSpace-Region `0x1219A48-0x1600000`.
- Die bestehende `gLevelUpLearnsets`-Pointertable bei `0x25D7B4` bleibt erhalten und wird pro interner Species-ID aktualisiert.
- Diagnose 046 bestaetigt `plannedBlobBytes=17418`, `writtenBlobBytes=11547`, `uniqueBlobCount=416`, `pointertableEntriesUpdated=1413` und `writeReloadLearnsetMismatches=0`.
- Save, Reload, Output-ROM und nichtleerer Log waren im lokalen Diagnoseharness erfolgreich; lokale Artefakte blieben ignored unter `05_builds/**`.
- Keine Move-Data-Write-, Tutor-Text-, Special-Tutor-, Egg-Move-, Palette/Graphics- oder Text/Menu-Ausweitung.

Naechster sinnvoller Schritt:

- Nach Merge der PRs einen GUI-/Settings-Kombinationssmoke fuer Pokemon Movesets/Learnsets planen.
- Danach `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.


## 2026-05-13 - FVX GUI Options Compatibility Matrix

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-fvx-gui-options-matrix`

Aktueller Stand:

- Matrixprotokoll `08_tests/randomizer/047_fvx_gui_options_compatibility_matrix.md` erstellt.
- P1-supported Bereiche aus vorhandenen Diagnosen zusammengefuehrt: Standard/Fallback-Wild, Starters, Static/Gift, Trainer Species, Trainer Movesets, Trainer Held Items, Evolutions, Move-Data-Read, TM/HM 128-Slot, normale Tutor-Tabellen und direkte Egg Moves.
- Teilunterstuetzte Bereiche markiert: bounded Learnset-Write, Palette-Safety und Move-Data-Read ohne Write.
- Offene Hochrisiko-Writer priorisiert: Full Learnset Repointing, Base Stats/Types/Abilities, Move-Data-Write, Items/Shops/Field/Pickup und Palette/Graphics-Randomization.
- Keine Codeaenderung, keine `02_external/**`-Aenderung und keine ROM-/Build-/Tool-Artefakte.

Naechster sinnvoller Schritt:

- Wenn Phase 2 FreeSpace-Nachweis positiv ist, `compat/upr-fvx-cfru-dpe-learnset-write-repointing` fortsetzen.
- Andernfalls zuerst `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` starten.

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #80 ist gemerged.
- UPR-FVX PR #23 und Workspace PR #81 sind gemerged.
- UPR-FVX-Stand im Workspace: `5c7170b654b09e1fc27ced6857dd50a8e4711f08`.
- TM/HM-only ist im getesteten CFRU/DPE-128-Slot-Scope P1-supported.
- Tutor-only ist im getesteten CFRU/DPE-152-Slot-Scope P1-supported.
- Egg-Move direct scope ist P1-supported.
- Learnset-Write bounded in-place ist implementiert und diagnostisch stabil fuer strikt validierte same-size Writes.
- Full Learnset-Write-Repointing ist im direkten `setMovesLearnt()`-Scope implementiert und diagnostisch stabil.
- Pokemon Movesets/Learnsets sind im getesteten GUI-/Settings-nahen Flow P1-supported.
- Encounter Held Items sind im getesteten CFRU/DPE-`gBaseStats`-Scope P1-supported.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model`

## Aktueller Arbeitsblock

CFRU/DPE Palette-Randomization-Modell.

## Ziel

Read-only modellieren, wie bestehende Palette-Safety von echter geaenderter Palette-/Graphics-Randomization zu trennen ist.

## In diesem Arbeitsblock geprueft / geaendert

- Workspace-Branch `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model` genutzt; nicht auf `main` gearbeitet.
- Pflichtdokumente und Diagnosen 047/055/056/057 sowie vorhandene Palette-Safety-Protokolle gelesen.
- Read-only `rg`-Suche nach Palette-, `PokemonPalettesMod.RANDOM`-, `Gen3to5PaletteRandomizer`-, `savePokemonPalettes()`-, `rewriteCompressedPalette()`-, compressed-, repoint-, sprite- und graphics-Markern ausgefuehrt.
- Neues Protokoll erstellt: `08_tests/randomizer/058_p1_palette_randomization_model.md`.
- `08_tests/randomizer/README.md`, `SESSION_STATE.md`, `NEXT_STEPS.md` und Roadmap aktualisiert.
- Tool-Manifest nicht geaendert, weil kein Tool-/Repo-/Commit-/Submodule-Stand geaendert wurde.

## Ergebnis

- Palette-Safety ist nur fuer defensive Loads, missing/invalid Slots und unveraenderte Palette-Saves belegt.
- Echte geaenderte Palette-Randomization ueber `PokemonPalettesMod.RANDOM` / `Gen3to5PaletteRandomizer` bleibt open / not diagnosed.
- `savePokemonPalettes()` faellt bei geaenderten Paletten in compressed Write-/Repointing-Semantik.
- Shared/missing Palette-Pointer, Dex-/Pokedex-Mapping und FreeSpace/Repointing bleiben eigene Risiken.
- Graphics/Sprites bleiben ein separates P2-Modell.

## Noch nicht gestartet

- Special-Tutor-Modell/Fix
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Vollstaendige Nullslot-`<unknown>`-Analyse ausserhalb der bereits dokumentierten Klassifikation
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen.

Lokale Diagnose-Artefakte blieben ignored unter `05_builds/**` und wurden nicht committed.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

UPR-FVX und andere `02_external/**`-Repos blieben in diesem Analyseblock unangetastet.

Keine Type-Chart-, Ability-Name-, Item-Name-, Move-Data-Write-, Tutor-Text/Menu-, Special-Tutor-, Egg-Move-, Graphics/Sprite- oder Text/Menu-Ausweitung.

Keine MCP-Configs mit Secrets angelegt.

## Naechste Pruefung

Lokal im Workspace nach den Dokumentationsaenderungen pruefen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

## Naechster empfohlener Branch

Nach Merge dieses Analyseblocks: `analysis/upr-fvx-cfru-dpe-p1-type-chart-model`. Graphics/Sprites, Special Tutors, Tutor-Text/Menu-Rewrites und spaetere Palette- oder Field-Items-/Shops-/Pickup-Fixes bleiben eigene Folgebranches.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-learnset-repointing-model

- UPR-FVX PR #23 und Workspace PR #81 als gemerged geprueft.
- CFRU/DPE Learnset-Repointing-Modell read-only dokumentiert.
- `gLevelUpLearnsets` Pointer-Ort `0x03EA7C` zeigt auf die aktive Pointertable bei `0x25D7B4`.
- Quellenanalyse: `1408` Pointertable-Zuweisungen, `1104` eindeutige Learnset-Ziele, `148` Shared-Zielgruppen.
- Kein statisch freier Append-Bereich belastbar belegt; spaeterer Fix muss FreeSpace im konkreten ROM nachweisen.
- Kein Fix, keine Aenderung an `02_external/**`, kein Repointing.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-learnset-write-bounded

- Workspace PR #80 als gemerged geprueft.
- UPR-FVX-Fix `dd9d80c16936a99bac1d7ef777b43baa7c2f029d` erstellt.
- `setMovesLearnt()` erhaelt einen eng gegateten CFRU/DPE bounded in-place Write-Pfad fuer `gLevelUpLearnsets`.
- Kein Repointing: Growth wird diagnostiziert und uebersprungen.
- Diagnose 044 bestaetigt Save/Log/Output/Reload und `writeReloadLearnsetMismatches=0`.
- Writer akzeptiert im Test `boundedWrites=1` und skippt `1412` unsafe Pointer; voller Learnset-Write braucht ein separates Repointing-Modell.
- Keine Move-Data-Write-, Tutor-Text-, Special-Tutor- oder Egg-Move-Ausweitung.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-egg-move-model

- UPR-FVX PR #21 und Workspace PR #77 als gemerged geprueft.
- CFRU/DPE Egg-Move-Modell read-only dokumentiert.
- `gEggMoves` als `u16`-Stream mit Species-Marker `species + 20000` und Terminator `0xFFFF` eingeordnet.
- DPE `repointall` zeigt `gEggMoves 08045C50`; FVX nutzt aktuell noch `EggMoves=0x25EF0C` aus dem FireRed-RomEntry.
- DPE-Egg-Move-Stream enthaelt Gen8-/PLA-/Paldea-Species und Move-IDs bis `MOVE_TIDYUP` ID `967`.
- Aktuelle FVX-Risiken: Pokédex-ID-Mapping statt interner Species-ID, globale Move-Ban-Arrays mit Laenge `827`, Egg-Move-Randomization an Learnset-Write gekoppelt.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility

- Workspace PR #76 als gemerged geprueft.
- UPR-FVX-Fix `4ce93754de390e9177efd2541c02edba0afbb0c4` erstellt.
- CFRU/DPE-Tutor-Pfad eng ueber `useCfruDpeGen9SpeciesCount` gegatet.
- `gMoveTutorMoves` als `u16[152]` ueber `0x8120BE4` gelesen/geschrieben.
- `gTutorLearnsets` als 19-Byte-/152-Bit-Compatibility pro Species ueber `0x8120C30` gelesen/geschrieben.
- Diagnose 040 bestaetigt Tutor moves-only, Compatibility-only und Tutor moves + Compatibility mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Special-Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder Tutor-Text-Rewrite-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tutor-model

- UPR-FVX PR #20 und Workspace PR #75 als gemerged geprueft.
- CFRU/DPE Tutor-/Special-Tutor-Modell read-only dokumentiert.
- `gMoveTutorMoves` als `u16[152]` ueber Pointer-Location `0x8120BE4` eingeordnet.
- `gTutorLearnsets` als 152-Bit-/19-Byte-Compatibility pro Species ueber Pointer-Location `0x8120C30` eingeordnet.
- Special Tutors als Sonderlogik ausserhalb der normalen Tabelle dokumentiert.
- FVX nutzt aktuell weiterhin klassischen FireRed-Tutor-Scope `15`; Tutor-only bleibt nicht P1-supported.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tm-hm-128-slot

- Workspace PR #74 als gemerged geprueft.
- UPR-FVX-Fix `58379ffd3146fcd6bb0eb416647cdf9b752cfc0e` erstellt.
- CFRU/DPE-128-Slot-TM/HM-Pfad eng ueber `useCfruDpeGen9SpeciesCount` gegatet.
- `gTMHMMoves` als `u16[128]` ueber `0x8125A8C` gelesen/geschrieben; TMs `0..119`, HMs `120..127`.
- `gTMHMLearnsets` als 16-Byte-/128-Bit-Compatibility pro Species ueber `0x8043C68` gelesen/geschrieben.
- Diagnose 038 bestaetigt TM moves-only, Compatibility-only und TM moves + Compatibility mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder TM51..TM120-Item-Text-/Palette-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model

- UPR-FVX PR #19 und Workspace PR #73 als gemerged geprueft.
- CFRU/DPE-128-Slot-TM/HM-Modell read-only dokumentiert.
- `gTMHMMoves` ist `u16[128]` ueber Pointer `0x8125A8C`; TMs `1..120`, HMs `121..128`.
- `gTMHMLearnsets` ist 128-Bit-/16-Byte-Compatibility pro Species ueber Pointer `0x8043C68`.
- FVX-`50+8`-Pfad bleibt P1-supported, bildet aber das 128-Slot-Modell nicht ab.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety

- Workspace PR #72 als gemerged geprueft.
- UPR-FVX-Fix `32e43ac03a5762542773213a13be4e0389f1deae` erstellt.
- TM-Move-Randomization fuer CFRU/DPE gegen Move-IDs oberhalb der alten FVX-Sicherheitslisten abgesichert.
- TM/HM-Compatibility fuer CFRU/DPE gegen Placeholder-Species und `null`-Typen abgesichert.
- Diagnose 036 bestaetigt TM moves + Compatibility, Compatibility-only und TM moves-only mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder 128-Slot-TM/HM-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-only

- UPR-FVX PR #18 und Workspace PR #71 als gemerged geprueft.
- TM/HM-only Diagnose auf UPR-FVX `c71fd75e67f5a839560bbf5de7c6f17317a64bd1` ausgefuehrt.
- FVX erkennt nur klassisches `50+8`-TM/HM-Modell.
- TM-Move-Randomization blockiert an altem Move-Ban-Array-Limit.
- TM/HM-Compatibility-only blockiert separat an Null-Type-Species.
- Neues Protokoll erstellt: `08_tests/randomizer/035_p1_tm_hm_only.md`.
- Kein Fix, keine Randomizer-Codeaenderung, keine committed ROM-/Build-Artefakte.

## 2026-05-13 - CFRU/DPE Egg-Move scope/write fix

- Active branch: `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write`.
- UPR-FVX fix commit: `18168b78b973a4c39f34053ac58f21279a26d8d2`.
- Implemented a gated CFRU/DPE `gEggMoves` reader/writer through pointer location `0x45C50` while preserving the classic `u16` stream, `species + 20000` markers, and `0xFFFF` sentinel.
- Preserved internal `SpeciesSet` identity for Egg-Move keys and guarded high move-ID flag-array access in `SpeciesMovesetRandomizer`.
- Added diagnosis `08_tests/randomizer/042_egg_moves_scope_and_write_fix_diagnostics.md`.
- Direct Egg-Move harness result: `moves.total=992`, highest loaded move `991:PsychicNoise`, target pointer `0x09A0E94C`, species entries `436 -> 436 -> 436`, highest species `1412`, highest move after/reload `991`, `writeReloadEggMoveMismatches=0`, `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`.
- No Learnset-Write, Move-Data-Write, Tutor-Text, Special-Tutor, or `setMovesLearnt()` expansion was included.

## 2026-05-13 - CFRU/DPE Learnset-Write-Modell

- Active branch: `analysis/upr-fvx-cfru-dpe-p1-learnset-write-model`.
- UPR-FVX PR #22 und Workspace PR #79 als gemerged geprueft.
- `gLevelUpLearnsets` Write-Modell read-only dokumentiert; keine Aenderung an `02_external/**`.
- Neues Protokoll: `08_tests/randomizer/043_p1_learnset_write_model.md`.
- Befund: Pointer-Ort `0x03EA7C` / `0x0803EA7C`, interne Species-ID-Pointertabelle, Eintraege `u16 move + u8 level`, Sentinel `{0, 0xFF}`, `MAX_LEARNABLE_MOVES=50`, Species bis `SPECIES_PECHARUNT=0x59F`, Moves bis `MOVE_PSYCHICNOISE=0x3DF`.
- Empfehlung: Folgefix nur eng gegatet und zunaechst bounded in-place; Repointing separat modellieren.
