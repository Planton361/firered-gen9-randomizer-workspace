# Next Steps

## Aktueller Fokus

CFRU/DPE MoveData Fairy-Type-Byte Fix ist dokumentiert. Diagnose: `08_tests/randomizer/087_move_data_fairy_type_byte_fix_diagnostics.md`.

`FVX-MOVE-004` Randomize Move Types ist nach dem engen CFRU/DPE-MoveData-Fairy-Type-Byte-Fix reload-stabil.

Naechster aktiver Arbeitsblock: UPR-FVX PR #34 und Workspace-PR reviewen und mergen; danach Post-Merge-Doku-Sync.

## Priorisierte naechste Arbeitsbloecke

1. MoveData Fairy-Type-Byte-Fix reviewen
   - Empfohlener UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`.
   - Workspace-Branch: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`.
   - UPR-FVX PR: https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/34
   - Ziel: Review/Merge des engen `Gen3RomHandler`-Fixes fuer raw `0x17` Fairy im MoveData-Byte `+2`.
   - Ergebnis aus 087: Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`, `moves.total=992`, `991:PsychicNoise`, Preserve-Bytes `0` Mismatches.
   - Grenzen: `FVX-MOVE-005` Move Names/Descriptions bleibt out of scope; TypeChart, TypeEffectiveness und Species-Type-Write nicht vermischen; Vanilla/Jambo/andere Gen3-Pfade unveraendert lassen.

2. Post-Merge-Doku-Sync nach MoveData Fairy-Type-Byte-Fix
   - Empfohlener Branch nach Merge: `docs/post-merge-move-data-fairy-type-byte-sync`.
   - Ziel: PR-Status fuer UPR-FVX PR #34 und Workspace-PR markieren, `FVX-MOVE-004` als GUI-kompatibel halten und naechsten Scope konservativ bestimmen.
   - `FVX-MOVE-005` Move Names/Descriptions nicht implizit starten; nur separat planen, wenn explizit freigegeben.

3. MoveData Types Reload-Smoke reviewen
   - Branch: `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke`.
   - Diagnose 086 dokumentiert den Blocker fuer `FVX-MOVE-004`.
   - Save/Log/Output/Reload sind true; `moves.total=992` und `991:PsychicNoise` bleiben stabil.
   - Preserve-Bytes bleiben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
   - Der Blocker ist durch Diagnose 087 behoben.

4. MoveData Power/Accuracy/PP Reload-Smoke reviewen
   - Branch: `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke`.
   - Diagnose 085 bestaetigt `FVX-MOVE-001`, `FVX-MOVE-002` und `FVX-MOVE-003` mit Save/Log/Output/Reload true und `writeReloadMoveDataMismatches=0`.
   - `powerReloadMismatches=0`, `accuracyReloadMismatches=0`, `ppReloadMismatches=0`.
   - Preserve-Bytes bleiben bytegleich.

5. PRs fuer Wild-Filter-Carrier-Nullslot-Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Diagnose 075 und Submodule-Pin reviewen und mergen.

6. PRs fuer Trainer Type Diversity Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Diagnose 078 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `TrainerPokemonRandomizer` und den Force-Diverse-Types-/`usedTypes`-Pfad begrenzt.

7. PRs fuer Evolution Same Typing Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Diagnose 080 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `EvolutionRandomizer` und den Same-Typing-/Null-Primary-Type-Scope begrenzt.

8. PR fuer `FVX-TRAIT-018` Similar Strength Normalized Reload reviewen
   - Diagnose 082 bestaetigt den einzelnen Similar-Strength-Smoke mit Save/Log/Output/Reload true und `normalizedWriteReloadEvolutionMismatches=0`.
   - Der Reload-Vergleich nutzt nur persistierte Gen3-Evolution-Felder und Ziel-Species per interner `SpeciesSet`-Identitaet; `Evolution.forme` ist kein Mismatch-Kriterium.
   - `Bad Egg=true` ist nach 055 klassifiziert; `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
   - Fuer diesen engen `FVX-TRAIT-018`-Scope ist kein Fixbranch erforderlich. Evolution-Methoden-Writer und weitere Evolution-Suboptionen bleiben getrennt.

9. Wild-Suboptionen konservativ halten
   - `FVX-WILD-011` und `FVX-WILD-004` sind im `FVX-WILD-001` Carrier-Fix-Smoke stabil.
   - Evolution Restrictions, Catch Em All, Minimum Catch Rate und Level-Balance bleiben getrennte Wild-Scope-Themen.

10. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

11. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

12. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
