# UPR-FVX CFRU/DPE Compatibility Implementation Report

Stand: 2026-05-21

Scope: technischer Bericht zum bisherigen UPR-FVX-Kompatibilitaetsstand auf
`compat/firered-gen9-cfru-dpe`, workspace-gepinnt bei `8349daf5ce005f0defc5674cbc3a3468f009218c`
bis PR #152. Dieser Bericht dokumentiert keine neue ROM-Ausfuehrung, keinen Build und keine neue
P1-Promotion.

## 1. Executive Summary

### Ursprungliches Problem

UPR-FVX ist fuer offizielle Core-ROMs modelliert. Der lokale Zielscope ist aber FireRed BPRE mit
CFRU/DPE-Gen9-Erweiterungen. Dadurch liegen mehrere Datenquellen nicht mehr dort oder nicht mehr in
der Form, die ein normaler Gen3-Handler erwartet:

- Species koennen ueber interne CFRU/DPE-IDs 1-9 statt nur ueber National-Dex-Nummern laufen.
- Trainerkaempfe koennen `trainerbattle`-Scriptquellen verwenden, deren `TrainerData`-Rows nicht in
  der normalen geladenen Trainerliste liegen.
- Intro-Mon-Visuals, Catching Tutorial, Wild, Paletten, Items und Trainer-Held-Items nutzen teils
  separate Pointer-/Runtime-/Filterpfade.
- Mega-/GMax-/Regional-/Irregular-Formen und Mechanic-Items sind in CFRU/DPE sichtbar, aber nicht
  automatisch in den generischen FVX-Alt-Form-/Mega-Metadaten enthalten.

### Insgesamt erreicht

Der bisherige Fix-Stack hat aus einem "normale Logs sehen sauber aus, aber Ingame-Pfade koennen
abweichen"-Stand einen gezielter abgesicherten Kompatibilitaetsstand gemacht:

- Gen3/CFRU/DPE Species-Identitaet wird in wichtigen Write-Pfaden ueber interne SpeciesSet-Identity
  behandelt.
- FRLG runtime Trainer-Quellen werden diagnostiziert, gueltige nicht geladene Rows strikt geladen,
  randomizer-eligible gemacht und wieder gespeichert.
- Intro Mon, Oak-Lab-Rival, Trainer-Class-Sprite-Sync, Palette Writes, Catching Tutorial, Running
  Shoes, Fast Egg, Gen Limit 1-9, Special-Form-Filter, Mechanic-Item-Filter und Trainer-Held-Item
  NPE-Faelle wurden gezielt gefixt oder auditierbar gemacht.
- Evidence-Dateien `202` bis `212` dokumentieren die lokalen sanitized Smokes/Audits. Die staerksten
  aktuellen Status sind targeted smoke/audit pass with caveats, nicht Full-Playthrough oder P1.

### Bewusst noch nicht P1-supported

Nicht P1-promoted sind insbesondere:

- Full Playthrough.
- Special Wild / Day-Night / Swarms / andere CFRU runtime Wild-Quellen.
- Static Script/Gift/NPC item sources ausserhalb normaler Item-Replacement-Pools.
- custom/future form encodings ausserhalb der dokumentierten CFRU/DPE identity blocks.
- loaded-mismatch, invalid-pointer, empty-party und out-of-range runtime Trainer rows.
- Shiny-Palette-Breitabdeckung.
- vollstaendige Type-Matchup-Matrix.
- vollstaendige Trainer-Held-Item-Distribution-Audit.

## 2. Architekturueberblick

### Wie UPR-FVX Gen3/CFRU/DPE-Daten liest und schreibt

Der zentrale Codepfad ist `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`.
Der Handler laedt fuer Gen3 statische ROM-Tabellen ueber `romEntry`-Offsets und schreibt geaenderte
Daten zurueck. Im CFRU/DPE-BPRE-Scope wurden mehrere Pfade erweitert:

- `loadSpeciesStats()` baut `pokes` und `pokesInternal`. Fuer Extended BPRE setzt der Handler
  `Species.speciesSetIdentityNumber` auf die interne Species-ID und bestimmt die Generation ueber
  `generationOf()` / `generationOfSpeciesId()`.
- Wild: `getEncounters(false)` / `setEncounters(...)` lesen und schreiben den modellierten
  Gen3-`WildPokemon`-Headerpfad. `getWildEncounterInternalSpeciesId()` schreibt im Extended-BPRE-Fall
  die SpeciesSet-Identity.
- Trainer: `loadTrainers()` liest normale `TrainerData`-Rows und FRLG-zusaetzlich validierte
  runtime-source Rows; `saveTrainers()` schreibt normale Rows und bei FRLG runtime-source Rows zurueck.
- Paletten: `loadPokemonPalettes()` laedt fuer CFRU/DPE defensiv; `savePokemonPalettes()` schreibt
  bei geaenderten CFRU/DPE-Paletten neue komprimierte Palette-Copies und aktualisiert die Pointer.
- Intro/Catching Tutorial/Misc: `setIntroPokemon()`, `setCatchingTutorial()` und `applyMiscTweak()`
  kapseln die konkreten Patch-/Write-Pfade.

Randomizer-Entscheidungen liegen hauptsaechlich unter
`02_external/upr-fvx/random/src/main/java/com/uprfvx/random/`:

- `GameRandomizer.java` orchestriert Reihenfolge und Reapply-Schritte.
- `RestrictedSpeciesService.java` liefert die gefilterten Species-Pools.
- `TrainerPokemonRandomizer.java`, `IntroPokemonRandomizer.java`, `ItemRandomizer.java`,
  `MiscTweakRandomizer.java` und `TrainerClassSpriteSyncRandomizer.java` nutzen diese Handler- und
  Service-Pfade.
- `RandomizationLogger.java` erzeugt Logs und wurde robuster gegen expanded/null Daten gemacht.

### Daten aus statischen Tabellen

Statische Tabellen sind der klassische FVX-Kern:

- Species-/BaseStats-/Learnset-/Evolution-/Palette-/Item-/Trainer-Tabellen aus `romEntry`-Offsets.
- Standard-Wild ueber `WildPokemon`-Header.
- normale `TrainerData`-Rows bis `TrainerCount`.
- Trainer class names und display names ueber Trainer-Class-Name-Tabelle, im CFRU/DPE-Fall mit
  Runtime-Pointer-Fallback via `chooseCfruDpeTrainerClassNamesOffset()`.
- GUI-/Settings-Daten ueber `Settings.java`, `RandomizerGUI.java`, `GenerationLimitDialog.java` und
  `SettingsProfileGenerator.java`.

### Daten aus Runtime-/Script-Quellen

Runtime-/Script-Quellen sind der eigentliche Kompatibilitaetsbruch gegen Vanilla-FireRed:

- FRLG `trainerbattle` script commands werden ueber
  `findFrlgTrainerBattleCommands()` / `findFrlgTrainerBattleRuntimeSources()` erkannt.
- Die dazugehoerigen raw `TrainerData` rows koennen ausserhalb der normalen geladenen Liste liegen.
  `buildFrlgTrainerRuntimeSourceAuditRows()` klassifiziert sie als `VALID_RUNTIME_NOT_LOADED`,
  `LOADED_AND_RUNTIME_MATCH`, `LOADED_AND_RUNTIME_MISMATCH`, `INVALID_POINTER`, `EMPTY_PARTY`,
  `OUT_OF_RANGE` oder false positive.
- Oak-Lab-Rival nutzt Script-/TrainerData-Quellen, deren Starterzuordnung nicht der naiven Reihenfolge
  entspricht. `findFrlgOakLabRivalTrainerIdsByPlayerStarterSlot()` bildet die FRLG-Scriptreihenfolge
  auf die Player-Starter-Slots ab.
- Wild-CFRU-Runtime-Systeme wie Day/Night, Swarms, DexNav, Raids oder andere Spezialquellen liegen
  bewusst ausserhalb des aktuellen Standard/Fallback-`WildPokemon`-Pfads.

### Hauptkompatibilitaetsrisiken

- Falsche ID-Ebene: National-Dex-Nummer statt interner CFRU/DPE SpeciesSet-Identity.
- Statische Modellannahme fuer Daten, die Ingame aus Scripts oder Runtime-Pointern kommen.
- Null-/Placeholder-/invalid Rows in expanded Tables.
- Form- und Mechanic-Metadaten fehlen im generischen FVX-Modell und muessen source-backed klassifiziert
  werden.
- Logs koennen sauber sein, obwohl der Ingame-Pfad eine andere Quelle benutzt.
- Targeted Smoke ist kein Ersatz fuer Full Playthrough, breite Distribution-Audits oder komplette
  Matchup-/Palette-Matrizen.

## 3. Feature-/Fix-Erklaerung nach Themen

### Intro Mon Visual Source / Species-0 Guard

**Problem vor dem Fix:** FRLG-Intro-Offsets wurden zwar geaendert, aber CFRU/DPE BPRE zeigte weiter die
alte sichtbare Nidoran-female-Quelle. Zusaetzlich konnte der expanded Pool eine ungueltige Species `0`
in den Intro-Pfad bringen.

**Codebereiche:** `Gen3RomHandler.setIntroPokemon()`,
`getIntroPokemonInternalSpeciesId()`, `writeCfruDpeIntroVisualTables()`,
`syncCfruDpeIntroVisualSourcePointerTableEntries()`, `IntroPokemonRandomizer.randomizeIntroPokemon()`;
Tests `Gen3IntroMonVisualSourceDiagnosticsTest`, `Gen3IntroMonVisualSourceRomTest`,
`IntroPokemonDecisionTest`.

**Konkrete Aenderung:** PR #107/#108 fuehrte Intro-Mon Visual-Source-Diagnostik und Settings-Overlay-
Semantik ein. PR #109 synchronisierte fuer CFRU/DPE die Nidoran-female
`PokemonFrontImages`- und `PokemonNormalPalettes`-Eintraege auf die Ziel-Species-Asset-Pointer. PR #117
gab `setIntroPokemon()` einen Species-0-Guard. PR #131 erweiterte Gen7/8/9 Intro-Kandidaten auf
gueltige visual-table candidates.

**Warum kompatibler:** Der sichtbare Oak-Intro-Pfad nutzt jetzt dieselbe visual source wie die
randomisierte Ziel-Species, statt nur einen nicht sichtbaren Literal-/Cry-Pfad zu aendern. Ungueltige
Species werden uebersprungen statt geschrieben.

**Evidence:** `205_intro_mon_visual_source_fix_smoke.md`, `207_rival_counter_starter_and_combined_visual_smoke.md`,
`208_combined_trainer_visual_runtime_smoke.md`, `212_gen_limit_special_form_item_smoke.md`; UPR-FVX PR
#107, #109, #117, #131.

**Caveats:** targeted visual smoke, kein Full-Playthrough, keine globale Visual-Source-Proof fuer alle
custom hacks.

### Trainer Runtime Source Sync

**Problem vor dem Fix:** Bestimmte FRLG-Battles verwendeten raw `TrainerData`-Rows, die nicht in der
normalen FVX-Trainerliste lagen. Randomizer-Logs konnten daher sauber aussehen, waehrend Ingame ein
vanilla wirkender Runtime-Trainer kaempfte.

**Codebereiche:** `Gen3RomHandler.findFrlgTrainerBattleRuntimeSources()`,
`buildFrlgTrainerRuntimeSourceAuditRows()`, `findFrlgRuntimeTrainerDataRowsToLoad()`,
`loadFrlgRuntimeTrainerSourceRows()`, `saveFrlgRuntimeTrainerSourceRows()`.

**Konkrete Aenderung:** PR #100 brachte Diagnose fuer `trainerbattle` Runtime-Quellen. PR #102 fixte
zunaechst Rival 2 `329/330/331` und Brock `414`. PR #103/#106 ergaenzten globale und Pre/Post-Audits.
PR #104 ersetzte die reine Known-ID-Loesung durch strict auto-sync fuer gueltige
`VALID_RUNTIME_NOT_LOADED` Rows.

**Warum kompatibler:** Gueltige Script-referenzierte Trainer werden ins FVX-Modell geladen, randomisiert
und wieder an ihre raw Runtime-Quelle geschrieben. Damit stimmen geloggte/geladene Parteien eher mit
dem tatsaechlichen Ingame-Battle-Pfad ueberein.

**Evidence:** `202_trainer_runtime_source_diagnostics_sync.md`,
`203_runtime_source_trainer_randomization_smoke.md`, `204_runtime_source_trainer_randomization_smoke.md`;
UPR-FVX PR #100, #102, #103, #104, #106.

**Caveats:** `loaded-mismatch`, invalid pointer, empty party und out-of-range Rows bleiben Diagnose- und
Follow-up-Scope. Kein Full-Playthrough.

### Trainer Runtime Source Randomization

**Problem vor dem Fix:** Selbst wenn Runtime-Rows geladen wurden, konnten generische `RUNTIME-SOURCE`
Trainer fuer die Foe-Pokemon-Randomization nicht wie regulaere Trainer behandelt werden.

**Codebereiche:** `Gen3RomHandler.loadFrlgRuntimeTrainerSourceRows()` setzt Tags ueber
`frlgRuntimeTrainerSourceTag()`, `TrainerPokemonRandomizer` arbeitet anschliessend auf
`romHandler.getTrainers()`.

**Konkrete Aenderung:** PR #105 machte generische `RUNTIME-SOURCE`-Trainer randomizer-eligible, ohne
bekannte Rival-/Brock-Spezialtags zu verlieren.

**Warum kompatibler:** Runtime-Source-Trainer werden nicht nur gelesen/geschrieben, sondern nehmen auch
an den normalen Trainer-Pokemon-Randomizer-Entscheidungen teil.

**Evidence:** `203_runtime_source_trainer_randomization_smoke.md` und `204_runtime_source_trainer_randomization_smoke.md`
mit Viridian-Forest IDs `531/532`, randomized output audit `unloaded-valid-parties total=0`, sowie
sanitized Rival 2/Brock Beispiele.

**Caveats:** nur targeted Trainer/Foe evidence; weitere suspected runtime-source Battles brauchen
eigene sanitized Evidence.

### Rival Counter-Starter / Oak-Lab Rival Counter

**Problem vor dem Fix:** Der Oak-Lab-Rival braucht die korrekte Counter-Starter-Logik, auch wenn Starter
und Trainer-Pokemon randomisiert wurden. Eine naive Scriptreihenfolge gab falsche Rival-Zuordnung.

**Codebereiche:** `Gen3RomHandler.findFrlgOakLabRivalTrainerIdsByPlayerStarterSlot()`,
`GameRandomizer.maybeRandomizeTrainerPokemon()` mit `makeFirstRivalCarryStarter()` Reapply,
`TrainerPokemonRandomizer`.

**Konkrete Aenderung:** PR #97 korrigierte die Oak-Lab-Slotzuordnung. PR #117 bewahrte den
Counter-Starter nach Foe-Pokemon-Randomization. PR #144/#152 dokumentieren/erhalten, dass Oak-Lab
Counter-Starter unabhaengig von "Rival Carries Starter Through Game" erhalten bleibt.

**Warum kompatibler:** Starter- und Trainer-Randomization koennen kombiniert werden, ohne dass der erste
Rival denselben oder falschen Starter bekommt.

**Evidence:** `207_rival_counter_starter_and_combined_visual_smoke.md`, `208_combined_trainer_visual_runtime_smoke.md`,
`212_gen_limit_special_form_item_smoke.md`; UPR-FVX PR #97, #117, #144.

**Caveats:** sampled path, kein all-starter-choice matrix und kein Full-Playthrough.

### Trainer Class Sprite Sync inklusive GUI-Control

**Problem vor dem Fix:** `Randomize Trainer Class Names` aenderte nur Textlabels. Sichtbare Trainer-Sprites
und `trainerClass`/`trainerPic` blieben semantisch getrennt, was im CFRU/DPE-Scope besonders auffiel.

**Codebereiche:** `TrainerNameRandomizer.randomizeTrainerClassNames()`,
`TrainerClassSpriteSyncRandomizer.randomizeTrainerClassSprites()`,
`Gen3RomHandler.writeTrainerClassSpriteFields()`,
`saveFrlgRuntimeTrainerSourceRows()`, `RandomizerGUI.java`, `RandomizerGUI.form`,
`Bundle.properties`, `Settings.java`, `SettingsProfileGenerator.java`.

**Konkrete Aenderung:** PR #111 fuehrte `MODE-TRAINER-CLASS-SPRITE-SYNC` ein. PR #112 bis #116
korrigierten Persistenz auf Runtime-Rows, Semantik, identity mappings, per-trainer Assignment und
Rival/Friend-Gruppierung. PR #143 machte die Option in der GUI sichtbar.

**Warum kompatibler:** Wenn Sync aktiv ist, folgen Class-Label, `trainerClass` und sichtbarer
`trainerPic` derselben Trainer-Class-Assignment. Runtime-source Rows koennen dabei mitgeschrieben
werden.

**Evidence:** `206_trainer_class_sprite_sync.md`, `208_combined_trainer_visual_runtime_smoke.md`,
`212_gen_limit_special_form_item_smoke.md`; Tests `TrainerClassSpriteSyncRandomizerTest`,
`Gen3TrainerTextDisplayNameSyncTest`; UPR-FVX PR #111-#116, #143.

**Caveats:** targeted visual smoke; keine breite Route-/Kategorie-Abdeckung.

### Trainer Class Names vs Sprite Sync Semantik

**Problem vor dem Fix:** Der Projektstatus konnte leicht "Class Names randomisieren" mit "Class IDs und
Sprites randomisieren" vermischen.

**Codebereiche:** `TrainerNameRandomizer` speichert textuelle Class-Name-Mappings und per-trainer
Assignments; `TrainerClassSpriteSyncRandomizer` setzt erst bei aktivem Sync `trainerClass` und
`trainerPic`; `Gen3RomHandler.setTrainerClassNames()` refreshed Display Names.

**Konkrete Aenderung:** Die Semantik wurde getrennt: `Randomize Trainer Names` aendert persoenliche
Namen; `Randomize Trainer Class Names` bleibt ohne Sync legacy/textlabel-only; `Sync Trainer Class
Sprites` ist der opt-in ID/Sprite-Pfad.

**Warum kompatibler:** Der Nutzer kann bewusst zwischen Textchaos und sichtbarer Class/Sprite-Konsistenz
waehlen. Der Bericht vermeidet dadurch falsche Supportclaims.

**Evidence:** `206_trainer_class_sprite_sync.md`, Dashboard `FVX-FOE-013`, UPR-FVX PR #116/#143.

**Caveats:** Ohne Sync bleibt das alte Textlabel-Verhalten absichtlich erhalten.

### Wild Pokemon Base-vs-Output Audit

**Problem vor dem Fix:** Wild-Logs konnten nicht leicht gegen tatsaechliche Base-vs-Output-Slots
verglichen werden. Gleichzeitig deckt der Gen3-Handler bewusst nur modeled Standard/Fallback-Wild ab.

**Codebereiche:** `Gen3RomHandler.getEncounters(false)`, `setEncounters(...)`,
`getFrlgWildEncounterOutputAuditForDiagnostics()`, `buildFrlgWildEncounterOutputAudit()`.

**Konkrete Aenderung:** PR #118 fuehrte einen opt-in Base-vs-Output-Audit fuer den modeled Gen3
`WildPokemon`-Tabellenpfad ein.

**Warum kompatibler:** Bei Abweichungen zwischen Log und Ingame kann lokal geprueft werden, ob FVX den
modellierten Standardpfad wirklich geaendert hat. Das trennt "Writer hat nicht geschrieben" von
"Ingame benutzt eine andere CFRU/DPE-Runtime-Quelle".

**Evidence:** `fvx-progress-dashboard.md`, `NEXT_STEPS.md`, UPR-FVX PR #118.

**Caveats:** diagnostic-only; keine Writer-Aenderung; Special Wild / Day-Night / Swarms bleiben separat.

### Graphics/Palettes Output Writes + Logging-Fallback

**Problem vor dem Fix:** CFRU/DPE-Palettentabellen enthalten expanded/null/forme-nahe Faelle, bei denen
klassisches Rewrite-Verhalten nicht robust ist. Zusaetzlich konnte Logging auf expanded/null Daten
abbrechen.

**Codebereiche:** `Gen3RomHandler.loadPokemonPalettesDefensively()`,
`saveCfruDpePokemonPaletteCopies()`, `writeCompressedPaletteCopy()`,
`getGen3PaletteOutputAuditForDiagnostics()`, `buildGen3PaletteOutputAudit()`,
`RandomizationLogger.logMovesets()` und Wild-Logger-Fallback fuer `<unknown>`.

**Konkrete Aenderung:** PR #119-#123 machten Palette-Settings effektiv, schuetzten expanded palette
descriptions, auditiereten Output-Daten und schrieben fuer CFRU/DPE geaenderte Paletten als neue
komprimierte Copies. PR #124 ergaenzte Logging-Fallbacks/Bounds fuer expanded Trainer-/Moveset-Daten.

**Warum kompatibler:** Palette-Randomization endet nicht nur im Log, sondern aendert den Output-Pointer-
Pfad. Logging soll bei Null-/Out-of-range-Daten diagnostisch weiterlaufen.

**Evidence:** `209_graphics_palettes_visual_smoke.md`: `normalPaletteWriteAttempts=841`,
`sampledCount=21`, `normalChangedCount=21`, `shinyChangedCount=0`; UPR-FVX PR #123/#124.

**Caveats:** targeted visual/audit smoke; shiny coverage bleibt offen.

### Misc Tweaks: Fast Text, PC Potion, Running Shoes, Catching Tutorial, Fast Egg

**Problem vor dem Fix:** Einige Misc-Tweaks benutzten Vanilla-Patches oder Species-Mapping-Annahmen, die
im CFRU/DPE-BPRE-Scope nicht zuverlaessig waren. Fast Egg konnte auf Species ohne `BreedingInfo`
crashen.

**Codebereiche:** `MiscTweakRandomizer.applyMiscTweaks()`,
`Gen3RomHandler.applyMiscTweak()`, `applyRunningShoesIndoorsPatch()`,
`applyRunWithoutRunningShoesPatch()`, `applyCfruDpeRunWithoutRunningShoesPatch()`,
`setCatchingTutorial()`, `getCatchingTutorialInternalSpeciesId()`,
`applyFastEggHatchingPatch()`.

**Konkrete Aenderung:** PR #125 fixte Running-Shoes-Tweaks fuer CFRU/DPE BPRE. PR #126 mappte
Catching-Tutorial-Species auf gueltige interne Species-Identity. PR #127 ueberspringt Species ohne
`BreedingInfo` bei Fast Egg Hatching.

**Warum kompatibler:** Misc-Patches schreiben nicht mehr blind auf Vanilla-Annahmen und crashen nicht
auf expanded Species ohne Breeding-Daten.

**Evidence:** `210_misc_tweaks_behavior_smoke.md`; UPR-FVX PR #125, #126, #127.

**Caveats:** targeted behavior smoke; kein Full-Hatch-Cycle-Proof; Ban Lucky Egg nur likely pass/no
issue observed; Reusable TMs und Forgettable HMs bleiben CFRU-provided stable-profile caveats.

### Type Effectiveness Battle Smoke

**Problem vor dem Fix:** TypeEffectiveness hatte CLI-/Settings-Abdeckung, aber keine dokumentierte lokale
Battle-Evidence.

**Codebereiche:** `TypeEffectivenessRandomizer.java`, `TypeEffectivenessUpdater.java`,
`SettingsProfileGenerator.java` fuer `MODE-TYPE-*` Overlays.

**Konkrete Aenderung:** Kein neuer Code in diesem Workspace-Bericht; vorhandene TypeEffectiveness-Pfade
wurden lokal sanitized im Battle-Smoke dokumentiert.

**Warum kompatibler:** Der Status wechselt von reiner CLI/Settings-Sicherheit zu targeted Ingame-
Verhalten ohne Battle-Crash.

**Evidence:** `211_type_effectiveness_battle_smoke.md`, Dashboard `FVX-TYPE-001` bis `003`.

**Caveats:** keine vollstaendige Type-Matchup-Matrix, kein Full-Playthrough, keine P1-Promotion.

### Gen Limit 1-9

**Problem vor dem Fix:** FVX-Settings und GenRestrictions waren historisch an die ROM-Generation
gekoppelt. CFRU/DPE FireRed enthaelt aber Gen1-9-Pokemon.

**Codebereiche:** `Gen3RomHandler.generationOf()`, `generationOfSpeciesId()`, `GenRestrictions.java`,
`Settings.java`, `SettingsProfileGenerator.java`, `GenerationLimitDialog.java`,
`RestrictedSpeciesService.setRestrictions()`.

**Konkrete Aenderung:** PR #129 fuehrte CFRU/DPE Gen1-9-Limit-Support ein. PR #130 wendete Gen-Limits
auf Randomizer-Pools an. Settings-/GUI-/profile Overlays wurden um Gen1-9-faehige Flags erweitert.

**Warum kompatibler:** Gen-Limit ist nicht mehr "FireRed == Gen3". Randomizer-Pools koennen fuer den
expanded Species-Raum sinnvoll auf Gen1-9 begrenzt werden.

**Evidence:** `212_gen_limit_special_form_item_smoke.md`, `SettingsProfileGeneratorTest`, `GenRestrictionsTest`,
`Gen3CfruDpeSpeciesGenerationTest`; UPR-FVX PR #129/#130.

**Caveats:** targeted log/visual smoke; custom/future encodings bleiben audit-required.

### Mega/GMax/Regional/Irregular/Special Form Filtering

**Problem vor dem Fix:** CFRU/DPE-Formen erschienen nicht zwingend in generischen FVX-Alt-Form-/Mega-
Metadaten. Ohne source-backed Filter konnten Mega/GMax/Regional/Irregular-Formen in Pools auftauchen,
obwohl der Nutzer sie nicht wollte.

**Codebereiche:** `Species.java` Form-Predicates, `SpecialFormPredicates.java`,
`SpecialFormExclusionOptions.java`, `RestrictedSpeciesService.java`, `GenerationLimitDialog.java`,
`Settings.java`.

**Konkrete Aenderung:** PR #133-#138 fuehrten Optionen, Predicates, Settings und GUI-Kontrollen ein.
PR #140/#146/#147 erweiterten GMax-, Regional- und Mega-Detection. Irregular special forms werden
standardmaessig ausgeschlossen.

**Warum kompatibler:** Starter, Wild, Trainer, Static, Trade, Intro und Tutorial ziehen aus gemeinsamen
restricted pools, die ungewollte Special-Formen herausfiltern.

**Evidence:** `SpecialFormPredicatesTest`, `RestrictedSpeciesServiceGenLimitExclusionsTest`,
`212_gen_limit_special_form_item_smoke.md`; UPR-FVX PR #133-#140, #146, #147.

**Caveats:** source-backed bekannte Identity-Ranges; custom/future encodings ausserhalb dieser Ranges
bleiben offen.

### Evolutionary Relatives vs Regional override

**Problem vor dem Fix:** `Allow Evolutionary Relatives` konnte Regionalformen oder regionale
Branch-Evolutions indirekt in einen Gen-Limit-Pool ziehen.

**Codebereiche:** `SpecialFormPredicates.isAllowedAfterEvolutionaryRelativeExpansion()`,
`effectiveGenerationForDirectLimit()`, `RestrictedSpeciesService.allInclAltFormesFromRestrictions()`.

**Konkrete Aenderung:** PR #139 trennte Evolutionary-Relative-Expansion von Regional-Override. Regional
forms nutzen ohne Override ihre eigene Form-Generation; mit `Allow Regional Forms across Gen Limit` duerfen
sie ueber die Base-Family-Generation in den Pool.

**Warum kompatibler:** Ein Gen1-only Pool mit Evolutionsverwandten bleibt Gen-limit-konform, solange der
Nutzer Regionalformen nicht explizit quer erlaubt.

**Evidence:** `RestrictedSpeciesServiceGenLimitExclusionsTest` Faelle
`evolutionaryRelativesDoNotAllowRegionalFormsWithoutRegionalOverride()` und
`regionalOverrideAllowsRegionalFormsAfterEvolutionaryRelativeExpansion()`; Evidence 212; UPR-FVX PR #139.

**Caveats:** Haengt an source-backed Regionalklassifikation.

### Mechanic Item Filtering fuer Mega/Z/Dynamax-GMax Items

**Problem vor dem Fix:** Wenn Mega/GMax/Z/Dynamax-Mechaniken nicht erwuenscht sind, durften dazugehoerige
Items nicht aus Field-/Shop-/Pickup-/Held-Item-Pools leaken. CFRU/DPE-Item-IDs koennen aber in FVX-
Standard-Item-Namespace kollidieren.

**Codebereiche:** `ItemMechanicPredicates.java`, `ItemMechanicExclusionOptions.java`,
`CfruDpeItemCategories.java`, `ItemRandomizer.filterAllowedMechanicItems()`,
`TrainerPokemonRandomizer.filterAllowedMechanicItems()`, `Settings.java`.

**Konkrete Aenderung:** PR #136 wendete Special-Mechanic-Item-Filter an. PR #141 deckte Z-Crystal-
Exclusions ab. PR #148/#150 fuegten source-backed CFRU/DPE-Item-Kategorien und Mega-Item-Leak-Coverage
hinzu. Mega Stones, Mega accessories, Z-Crystals/accessories und Dynamax/GMax Items werden bei
Default-Off gefiltert.

**Warum kompatibler:** Item-Randomizer erzeugt keine mechanic-inkonsistenten Items, wenn die
entsprechende Mechanik/Forms ausgeschlossen sind.

**Evidence:** `ItemMechanicPredicatesTest`, `212_gen_limit_special_form_item_smoke.md`; UPR-FVX PR #136,
#141, #148, #150.

**Caveats:** Plates/Drives/Memories/Nectars sind kategorisiert, aber ohne separate user-facing Policy.
Static Script/Gift/NPC item sources bleiben caveated, wenn sie Replacement-Pools umgehen.

### Trainer Held Items / Sensible Items NPE-Fixes

**Problem vor dem Fix:** Trainer Held Items, speziell `Sensible Items`, konnten auf null/fehlende Pools
oder fehlende Movepools im expanded CFRU/DPE-Scope laufen.

**Codebereiche:** `TrainerPokemonRandomizer.randomizeTrainerHeldItems()`,
`getMovesetForTrainerHeldItem()`, `randomizeHeldItem()`, `Gen3SensibleHeldItemsTest`.

**Konkrete Aenderung:** PR #151 guardete null sensible held item pools. PR #152 guardete fehlende
Trainer-Held-Item-Movepools und faellt auf allgemeine Held-Item-Pools zurueck, wenn sensible Kandidaten
leer sind.

**Warum kompatibler:** Held-Item-Randomization bricht nicht mehr auf fehlenden expanded Daten ab und kann
weiterhin mechanic item filters anwenden.

**Evidence:** `212_gen_limit_special_form_item_smoke.md`, `Gen3SensibleHeldItemsTest`; UPR-FVX PR #151/#152.

**Caveats:** targeted NPE-free GUI smoke; keine vollstaendige Held-Item-Distribution-Audit.

## 4. Bewertung des bisherigen Ansatzes

### Strukturiert und sinnvoll

- Zuerst wurden Diagnose- und Auditpfade gebaut, bevor riskante Writer erweitert wurden: Trainer
  runtime source audit, Intro visual source diagnostics, Wild Base-vs-Output Audit, Palette Output Audit.
- Fixes sind meist klein und feature-spezifisch geblieben.
- Gemeinsame Services (`RestrictedSpeciesService`, `SpecialFormPredicates`, `ItemMechanicPredicates`)
  reduzieren Pool-Divergenz zwischen Intro, Trainer, Wild, Static, Trade, Tutorial und Items.
- Evidence-Dateien trennen Code-Fix, sanitized local smoke und Caveat.

### Eher reaktiv

- Viele Fixes folgten beobachteten Ingame-Abweichungen: Rival/Brock runtime trainers, Intro visual
  mismatch, Palette writes, Running Shoes, Catching Tutorial, Fast Egg, Held Item NPEs.
- Teilweise wurden erst Known-ID-Fixes umgesetzt und danach zu generischeren Strict-Sync/Audit-Modellen
  erweitert.
- GUI-/Settings-Semantik fuer Trainer Class Sprite Sync und Special Forms wurde ueber mehrere PRs
  nachgeschaerft.

### Technisch stabil wirkende Teile

- Interne SpeciesSet-Identity fuer Extended BPRE in Species-, Wild-, Trainer-, Intro- und Tutorial-
  Write-Pfaden.
- Strict runtime trainer source sync fuer `VALID_RUNTIME_NOT_LOADED` Rows mit plausiblen Parties.
- Gemeinsame Special-Form- und Mechanic-Item-Predicates.
- Palette Copy Writes mit Changed-Check statt blindem Rewriting.
- Settings/Profile-Overlays fuer exakte CLI/GUI-Modi.

### Nur smoke-/audit-gestuetzte Teile

- Intro Mon visible source.
- Trainer Class Sprite Sync.
- Rival Carry/Counter-Starter.
- Palette visual output und Shiny-Status.
- Misc Tweaks behavior.
- Type Effectiveness battle behavior.
- Trainer Held Items/Sensible Items distribution.
- Wild Base-vs-Output Audit als Diagnose, nicht Ingame-Beweis fuer CFRU runtime Wild.

### Refactor sinnvoll ohne Verhalten zu aendern

- `Gen3RomHandler` ist stark gewachsen. Sinnvolle No-behavior Refactors waeren RuntimeTrainerSource,
  IntroMonVisualSource, PaletteOutputAudit und WildOutputAudit in eigene helper/service Klassen zu
  verschieben.
- Settings/GUI/Profile-Overlay-IDs koennten in einer zentraleren Feature-ID/Mode-Registry liegen.
- Repeated "internal species identity for Extended BPRE" Helpers koennten vereinheitlicht werden.
- Logging-Fallbacks koennten als kleine Format-/SafeAccess-Helper gebuendelt werden.

## 5. Datenqualitaet vs Kompatibilitaet

Falsche BaseStats, Learnsets, Abilities oder sonstige Pokemon-Daten sind eine andere Problemklasse als
Randomizer-Kompatibilitaet.

Dieser Bericht bewertet, ob UPR-FVX im CFRU/DPE-Gen9-BPRE-Scope die richtigen Quellen findet,
gueltige IDs schreibt, ungueltige Rows schuetzt, Randomizer-Pools korrekt filtert und Output/Log/Audit
koharent bleiben. Er bewertet nicht, ob die zugrunde liegenden CFRU/DPE-Daten inhaltlich perfekt sind.

Beispiel: Wenn eine Gen9-Species einen falschen Learnset-Eintrag in der CFRU/DPE-Basis hat, kann UPR-FVX
trotzdem kompatibel arbeiten, solange es den Learnset korrekt laedt, randomisiert oder konservativ
ueberspringt. Eine spaetere Datenkorrektur waere ein getrennter Scope und sollte nicht mit FVX-
Kompatibilitaetsfixes vermischt werden.

## 6. Empfohlene naechste Bewertungsmatrix

| Feature | Codepfad | Datenquelle | FVX-Touchpoint | Teststatus | Ingame-Test noetig | Caveat | Empfehlung |
|---|---|---|---|---|---|---|---|
| Intro Mon | `Gen3RomHandler.setIntroPokemon()` | Intro literals + visual pointer tables | `IntroPokemonRandomizer` | `PASS_TARGETED_INGAME_SMOKE` | Ja, breiter | targeted | Regression-only, sonst breiter visueller Smoke |
| Trainer Runtime Source | `find/load/saveFrlgRuntimeTrainerSourceRows()` | FRLG `trainerbattle` Scripts + raw `TrainerData` | `TrainerPokemonRandomizer` | `PASS_INGAME_SMOKE` fuer 531/532 | Ja, Full/weitere Rows | loaded-mismatch/invalid offen | Nur neue Rows mit sanitized Audit aufnehmen |
| Rival Counter-Starter | `makeFirstRivalCarryStarter()` + Oak-Lab mapping | Starter script + Rival TrainerData | `GameRandomizer` | targeted pass | Ja, all starters | kein Full-Playthrough | Bei Regression oder all-starter matrix |
| Trainer Class Sprite Sync | `TrainerClassSpriteSyncRandomizer` + `writeTrainerClassSpriteFields()` | Trainer class names, trainerClass, trainerPic | GUI `Sync Trainer Class Sprites` | targeted visual pass | Ja, breiter | ohne Sync textlabel-only | Beibehalten, breiter nur bei Bedarf |
| Wild Standard/Fallback | `getEncounters()` / `setEncounters()` | modeled `WildPokemon` table | `WildEncounterRandomizer` | log pass + audit available | Ja | runtime wild offen | Bei Divergenz Base-vs-Output Audit nutzen |
| Graphics/Palettes | `saveCfruDpePokemonPaletteCopies()` | Pokemon palette pointer tables | `Gen3to5PaletteRandomizer` | targeted visual/audit pass | Ja | Shiny offen | Shiny/breite form samples separat |
| Misc Tweaks | `applyMiscTweak()` | patch offsets + species/breeding data | `MiscTweakRandomizer` | targeted behavior pass | Ja | kein full hatch/drop proof | Regression-only oder Detailsmoke |
| Type Effectiveness | `TypeEffectivenessRandomizer` / updater | type chart | Type settings overlays | battle smoke pass | Ja | keine komplette Matrix | Full matrix nur eigener Scope |
| Gen Limit 1-9 | `generationOf()` + `RestrictedSpeciesService` | internal Species IDs | Settings/Profile/GUI | targeted log/visual pass | Ja | custom encodings offen | Beibehalten, neue encodings auditieren |
| Special Form Filtering | `SpecialFormPredicates` | Species identity ranges | Restricted pools | unit + smoke pass | Ja | source-backed range only | Audit bei neuen Form-Ranges |
| Regional override | `isAllowedAfterEvolutionaryRelativeExpansion()` | regional form metadata/fallbacks | Restricted pools | unit + smoke pass | Ja | classification-bound | Semantik beibehalten |
| Mechanic Item Filtering | `ItemMechanicPredicates` | item IDs + decoded names | Item/Trainer item pools | unit + smoke pass | Ja | static item sources offen | Source-backed Kategorien pflegen |
| Trainer Held Items | `randomizeTrainerHeldItems()` | held item pools + movesets | Trainer item randomizer | NPE-free targeted smoke | Ja | keine Distribution-Audit | Distribution-Audit nur separat |

## 7. Offene Risiken

- Full Playthrough fehlt.
- Static Script/Gift/NPC item sources koennen Items ausserhalb normaler Replacement-Pools setzen.
- Special Wild / Day-Night / Swarms sind nicht durch den modeled Standard-Wild-Pfad abgedeckt.
- custom/future form encodings ausserhalb dokumentierter CFRU/DPE identity blocks bleiben audit-required.
- Trainer loaded-mismatch / invalid / out-of-range rows sind bewusst nicht automatisch gesynct.
- Shiny palette coverage ist offen; Evidence 209 hatte `shinyChangedCount=0`.
- Vollstaendige Type-Matchup-Matrix fehlt.
- Vollstaendige Held-Item-Distribution-Audit fehlt.

## 8. Fazit

Der bisherige Weg war effektiv, weil er beobachtete CFRU/DPE-Brueche nicht mit grossen Refactors,
sondern mit Diagnose, kleinen Writer-/Pool-Fixes und sanitized Evidence bearbeitet hat. Besonders stark
ist die Trennung zwischen harten Fakten, Interpretation und Caveats im Workspace-Status.

Beibehalten werden sollte:

- erst Audit/Diagnose, dann enger Fix;
- source-backed Klassifikation fuer Forms und Items;
- interne SpeciesSet-Identity statt National-Dex-Annahmen im Extended-BPRE-Scope;
- keine P1-Promotion aus targeted smoke;
- sanitized Evidence ohne ROM-Pfade, Hashes, Full Logs, Screenshots, Saves oder Output-ROMs.

Kuenftig strukturierter werden sollte:

- wiederkehrende Runtime-/Audit-Helper aus `Gen3RomHandler` herausziehen;
- Bewertungsmatrizen vor neuen Smokes explizit definieren;
- Full-Playthrough-, Distribution-, Shiny- und Type-Matrix-Fragen als eigene Scopes behandeln;
- neue CFRU/DPE data-quality Fragen strikt von Randomizer-Kompatibilitaet trennen.
