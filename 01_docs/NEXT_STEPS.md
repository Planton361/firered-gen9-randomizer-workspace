# Next Steps

## Aktueller Fokus

CFRU/DPE MoveData Write Preserve Reload-Smoke ist dokumentiert. Diagnose: `08_tests/randomizer/084_move_data_write_preserve_reload_smoke.md`.

## Priorisierte naechste Arbeitsbloecke

1. PR fuer MoveData Write Preserve Reload-Smoke reviewen
   - Workspace: `test/upr-fvx-cfru-dpe-move-data-write-preserve-reload-smoke`.
   - Diagnose 084 bestaetigt `Update Moves` im MoveData-Writer-Preserve-Scope mit Save/Log/Output/Reload true.
   - Reload-Kriterien: `writeReloadMoveDataMismatches=0`, `moves.total=992`, `991:PsychicNoise`, `categorySplitMismatches=0`, `categoryReloadMismatches=0` und `preserveByteMismatchesUnchangedMoves=0`.
   - Kein Submodule-Pin-Wechsel; UPR-FVX bleibt auf `bb5ee11978e38839979e654ff1c14ba60a0cde93`.

2. PRs fuer MoveData Write Preserve reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-move-data-write-preserve`.
   - Workspace: `compat/upr-fvx-cfru-dpe-move-data-write-preserve`.
   - UPR-FVX PR #33 pruefen; Workspace pinnt `02_external/upr-fvx` auf `bb5ee11978e38839979e654ff1c14ba60a0cde93`.
   - Der Fix bleibt auf `Gen3RomHandler.saveMoves()` begrenzt: klassische MoveData-Bytes `+0..+4`, CFRU/DPE `BattleMove.split` bei `+10`, Preserve fuer `+5/+6/+7/+8/+9/+11`.
   - Reload-Sanity ist in Diagnose 084 separat bestaetigt; einzelne Power/Accuracy/PP/Types-Suboptionen bleiben konservativ bis zu eigenen GUI-nahen Smokes.

3. PRs fuer Wild-Filter-Carrier-Nullslot-Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Diagnose 075 und Submodule-Pin reviewen und mergen.

4. PRs fuer Trainer Type Diversity Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Diagnose 078 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `TrainerPokemonRandomizer` und den Force-Diverse-Types-/`usedTypes`-Pfad begrenzt.

5. PRs fuer Evolution Same Typing Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Diagnose 080 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `EvolutionRandomizer` und den Same-Typing-/Null-Primary-Type-Scope begrenzt.

6. PR fuer `FVX-TRAIT-018` Similar Strength Normalized Reload reviewen
   - Diagnose 082 bestaetigt den einzelnen Similar-Strength-Smoke mit Save/Log/Output/Reload true und `normalizedWriteReloadEvolutionMismatches=0`.
   - Der Reload-Vergleich nutzt nur persistierte Gen3-Evolution-Felder und Ziel-Species per interner `SpeciesSet`-Identitaet; `Evolution.forme` ist kein Mismatch-Kriterium.
   - `Bad Egg=true` ist nach 055 klassifiziert; `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
   - Fuer diesen engen `FVX-TRAIT-018`-Scope ist kein Fixbranch erforderlich. Evolution-Methoden-Writer und weitere Evolution-Suboptionen bleiben getrennt.

7. Wild-Suboptionen konservativ halten
   - `FVX-WILD-011` und `FVX-WILD-004` sind im `FVX-WILD-001` Carrier-Fix-Smoke stabil.
   - Evolution Restrictions, Catch Em All, Minimum Catch Rate und Level-Balance bleiben getrennte Wild-Scope-Themen.

8. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

9. `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint`
   - Nur nach separater Freigabe: echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern.

10. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
