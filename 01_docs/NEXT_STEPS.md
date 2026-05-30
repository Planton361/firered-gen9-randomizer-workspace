# Next steps update - Pokemon Showdown data local build/boot smoke

- Treat `08_tests/randomizer/showdown-pokemon-data-gen1-9.md` as updated with the sanitized local build/boot smoke.
- Current data pins for follow-up review: DPE `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`; CFRU `8c2d69b48aee8923098912ee06c188d3db93d231`.
- Status: DPE build pass, CFRU build on the new DPE ROM pass, mGBA boot pass, and no crash before first gameplay pass.
- Keep next validation focused on targeted data spot checks: representative Base Stats/type/gender/egg group/Ability display checks and level-up learnset spot checks.
- Keep Ability behavior-risk entries, Move open-risk entries, and Species open-risk form families blocked from stronger gameplay claims.
- Do not claim full-playthrough, BizHawk, Ironmon Tracker, or P1 support from this smoke.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens, and `.env` data from commits.

# Next steps update - Pokemon Showdown Pokemon Data Gen1-9 sync

- Treat DPE commit `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` and CFRU commit `8c2d69b48aee8923098912ee06c188d3db93d231` on branch `data/showdown-pokemon-data-gen1-9` as the current data-sync candidates.
- Treat `08_tests/randomizer/showdown-pokemon-data-gen1-9.md` as the current sanitized handoff.
- Run a local DPE/CFRU rebuild from the pinned commits before merging or promoting support.
- Run targeted local ROM boot/data smokes only after rebuild: representative Base Stats/type/gender/egg group/Ability display checks, plus level-up learnset spot checks in both DPE and CFRU.
- Keep Ability behavior-risk entries blocked for gameplay-behavior claims until source-backed CFRU behavior fixes or targeted smokes exist.
- Keep open-risk form families out of automated data writes unless a future source-backed policy resolves them.
- Do not claim full-playthrough, BizHawk, Ironmon Tracker, or P1 support from this data sync.
- Continue excluding Pokemon Showdown data copies, raw reports, ROMs, saves, emulator states, builds, tool binaries, screenshots, hashes, private paths, tokens, secrets, `.env`, and local-only paths from commits.

# Next steps update - DPE Base Stats full source sync audit

- Treat `01_docs/analysis/dpe-base-stats-full-source-sync.md` as the current decision record for whole-file DPE `Base_Stats.c` replacement.
- Do not full-replace DPE `src/Base_Stats.c` from Shiny-Miner, Skeli, pokeemerald-expansion, or Pokemon Showdown.
- Continue with small reviewed field-family tranches driven by the alias table and dry-diff helper.
- Keep Ability assignment updates blocked until Ability behavior/alias risk is explicitly accepted, fixed, or excluded.
- For a later real data PR, generate a review table with Species key, local DPE ID, source key, exact fields, blocker status, and canonical-vs-local-balance classification before writing any DPE table.
- Continue excluding submodule repins, external data copies, raw reports, ROMs, saves, builds, tool binaries, screenshots, hashes, private paths, tokens, secrets and `.env` data unless a later task explicitly allows them.

# Next steps update - DPE Base Stats tranche 1

- Treat DPE commit `1c8d53870e38d7019c681a68a17c9425a3490611` on branch `data/dpe-base-stats-tranche-1` as the current tranche 1 candidate.
- Run a local DPE/CFRU rebuild smoke from this DPE pin.
- Keep the smoke sanitized: document build pass/fail and any table-load symptoms only, without ROM paths, hashes, screenshots, raw logs, saves, states, private paths, tool binaries, tokens, secrets or `.env` data.
- If the build passes, optionally run a targeted ROM boot/menu smoke, but do not claim full-playthrough, BizHawk, Ironmon Tracker or P1 support from this tranche.
- Do not expand tranche 1 with Ability fields, Catch Rate, EXP Yield, EV Yield, Growth Rate, held items, base stats, moves, learnsets, TM/Tutor compatibility, CFRU code, UPR-FVX code, or extra DPE Species without a separate reviewed plan.

# Next steps update - DPE Base Stats Gen9 tranche 1 plan

- Treat `01_docs/analysis/dpe-base-stats-gen9-tranche-1-plan.md` as the current handoff for the first narrow DPE `Base_Stats.c` data PR.
- Recommended tranche 1 is limited to 10 Species: Sneasel-Hisui, Sneasler, Ursaluna, Toedscool, Toedscruel, Primarina, Brionne, Sylveon, Magnezone, and Crobat.
- Later implementation should edit only the listed non-Ability fields in DPE `Base_Stats.c`; do not include Ability fields, stats, Catch Rate, EXP Yield, EV Yield, Growth Rate, moves, learnsets, TM/Tutor compatibility, CFRU, UPR-FVX, or submodule pins.
- Keep excluded categories out of tranche 1: Species open-risk, reviewed ignores, cosmetic Pikachu forms, representation-only gender diffs, egg-group order-only churn, obvious local balance buffs, and local custom type additions without separate policy.
- Suggested later DPE commit: `data: update dpe base stats tranche 1`; suggested later workspace docs/pin commit if needed: `docs: pin dpe base stats tranche 1`.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits outside the later dedicated data PR, UPR-FVX changes, submodule repins, ROMs, saves, builds, tool binaries, screenshots, hashes, private paths, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - DPE Base Stats Gen9 safe dry diff

- Treat `07_scripts/data_audit/dpe_base_stats_dry_diff.py` as the current read-only helper for DPE Base Stats dry-diff review against external Pokemon Showdown `pokedex.ts`.
- Current dry-diff result is `PASS_READ_ONLY_WITH_BLOCKERS`: `1317` tested Species, `29` Species `open-risk` skipped, `167` reviewed Species ignores skipped, `65` Species blocked from safe candidate promotion by Ability blockers, `4` missing local entries after alias/ignore handling, and `225` safe candidate Species with non-Ability field diffs.
- Keep Ability assignments analysis-only until Ability behavior/open-risk blockers are accepted, fixed, or explicitly excluded.
- Do not generate Catch Rate, EXP Yield, EV Yield, or Growth Rate updates from Showdown `pokedex.ts`; choose a secondary trusted source before touching those fields.
- First useful implementation follow-up: a narrow DPE Base Stats non-Ability tranche for reviewed non-open-risk Species, with raw diff output kept outside the repo and DPE table writes limited to a separate reviewed PR.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits, UPR-FVX changes, submodule repins, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Pokemon data generator dry-run plan

- Treat `07_scripts/data_audit/pokemon_data_dry_run.py` as the current read-only gate before any Pokemon Showdown-to-CFRU/DPE data generator work.
- Current dry-run result is `BLOCKED_BY_REVIEWED_POLICY`: no uncategorized Species/Move/Ability keys remain, but Species `open-risk`, Move `open-risk`, and Ability `behavior-risk` / `open-risk` entries block all six data blocks.
- Keep Base Stats blocked by Species open-risk until form semantics are accepted or excluded.
- Keep Ability Assignments blocked by Species open-risk and Ability behavior/open risks until CFRU Ability behavior is accepted, fixed, or explicitly excluded.
- Keep Level-up Learnsets, Egg Moves, TM Compatibility, and Tutor Compatibility blocked by Species open-risk and Move open-risk until form semantics and missing/unsupported move behavior are resolved or excluded.
- First useful implementation path: generate a sanitized base-stats-only dry diff for a non-blocked species subset, still with no table writes until review.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits, UPR-FVX changes, submodule repins, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Pokemon data species alias table final

- Treat `07_scripts/data_audit/showdown_aliases.json` as updated through the final Species unresolved-key classification batch.
- Species unresolved audit buckets now have 0 still-uncategorized Showdown-only Species keys and 0 still-uncategorized local-only Species keys.
- Keep Species `open-risk` entries blocked for generator/data updates until source-backed form semantics or an explicit non-support policy exists.
- Blocking Species follow-up should focus on Alcremie cream/sweet forms, Basculin/Basculegion form semantics, Battle Bond Greninja, Pumpkaboo/Gourgeist size naming, Ogerpon mask-vs-form naming, Sinistea/Polteageist antique/chipped naming, Rockruff Dusk, and Tatsugiri form color/name semantics.
- Next useful data work can plan a dry-run generator/audit path against the reviewed alias table, still failing closed on any uncategorized key and treating `open-risk` / `behavior-risk` as unresolved.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits, UPR-FVX changes, submodule repins, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Pokemon data ability risk table final

- Treat `07_scripts/data_audit/showdown_aliases.json` as updated through the final Ability unresolved-key classification batch.
- Ability unresolved audit buckets now have 0 still-uncategorized Showdown-only Ability keys and 0 still-uncategorized local-only Ability keys.
- Keep Ability `behavior-risk`, `alias-plus-hook`, `name-mismatch` with blocked policy, and `open-risk` entries blocked for generator/data updates until source-backed behavior acceptance or an explicit non-support policy exists.
- Non-blocking Ability entries are limited to explicit legacy `intentionally-merged` name/effect merges, local-only ignores, non-project Future/CAP ignores, and sentinel-only `noability` / `ABILITY_NONE` handling.
- Next useful mapping work should continue remaining Species form/name policy; Ability follow-up should focus on targeted battle smokes or source fixes for blocked entries such as As One, Chilling Neigh, Full Metal Body, Libero, Zero to Hero, Terapagos Tera behavior, Commander, Hospitality, and Embody Aspect.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits, UPR-FVX changes, submodule repins, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Pokemon data ability risk table

- Treat `07_scripts/data_audit/showdown_aliases.json` as updated through the Ability behavior-risk table batch.
- Ability behavior risk is now machine-readable but still blocking by default: `alias-plus-hook`, `behavior-risk`, `name-mismatch`, and `missing-local` entries do not authorize generator-safe Ability updates.
- Only explicit `intentionally-merged` legacy Ability entries and `local-only` ignores are non-blocking classifications.
- Next Ability work should either add targeted battle smokes for selected `alias-plus-hook` entries or source-fix/document non-support for high-risk entries such as Zero to Hero and Terapagos Tera behavior.
- Remaining uncategorized Ability names should stay visible until reviewed in small batches; do not add broad regex rules.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits, UPR-FVX changes, submodule repins, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Pokemon ability behavior risk audit

- Treat `01_docs/analysis/pokemon-ability-behavior-risk-audit.md` as the current source-backed Ability behavior-risk handoff.
- Keep Ability aliases separate from solved mappings: a local Gen9 Ability name can still compile to an older CFRU Ability ID.
- Next policy batch should extend the reviewed alias/ignore table with Ability categories such as `implemented-alias-hooked`, `partial-alias-hooked`, `alias-only-risk`, `display-or-definition-risk`, and `missing-local`.
- Block Commander, Hospitality, Embody Aspect, and Terapagos Tera Shift / Tera Shell from generator-safe behavior assumptions until source-backed behavior or explicit non-support policy exists.
- Treat Zero to Hero as unresolved for true form-change behavior until a targeted source fix or sanitized battle smoke confirms it.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits, UPR-FVX changes, submodule repins, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Pokemon data alias table move final

- Treat `07_scripts/data_audit/showdown_aliases.json` as updated through the reviewed remaining-Move classification batch.
- Move audit buckets now have 0 still-uncategorized Showdown-only Move keys and 0 still-uncategorized local-only Move keys.
- Keep `open-risk` Move entries blocked: `allyswitch` and Let's Go partner moves are classified as known unresolved behavior gaps, not safe aliases.
- Keep CAP/Future Showdown moves and local helper/project constants as explicit non-actionable ignores unless the project later opts into those data domains.
- Next alias-table batch should focus on Ability behavior-risk expansion or remaining Species form/name policy; do not broaden Move regex rules.
- Audit/generator work must continue to fail closed on uncategorized Species or Ability mappings and must treat `open-risk` as unresolved.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits, UPR-FVX changes, submodule repins, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Pokemon data alias table move splits

- Treat `07_scripts/data_audit/showdown_aliases.json` as updated through the reviewed Z/Max/GMax physical-special Move split batch.
- Move split alias coverage is now 69 explicit entries; do not add broad regex rules for these names.
- Next alias-table batch should review narrow spelling/name aliases separately from real missing Move behavior.
- Keep Ally Switch, Let's Go-style moves, CAP/fan moves, and local extra moves visible as unresolved behavior/content risks until source-backed review exists.
- Keep expanding Ability entries only as `behavior-risk` when local names alias to older effects; do not mark them solved until CFRU ability behavior is audited.
- Audit/generator work must continue to fail closed on uncategorized Species, Move, or Ability mappings.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits, UPR-FVX changes, submodule repins, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Pokemon data alias table batch 2

- Treat `07_scripts/data_audit/showdown_aliases.json` as updated through Batch 2 for reviewed regional Species shortforms and GMax/Giga Species aliases.
- Next alias-table batch should focus on the remaining explicit Z/Max/GMax physical-special Move split pairs; keep them explicit and avoid broad regex rules.
- After Move split coverage, review narrow spelling/name aliases separately from real missing Move behavior.
- Keep expanding Ability entries only as `behavior-risk` when local names alias to older effects; do not mark them solved until CFRU ability behavior is audited.
- Audit/generator work must continue to fail closed on uncategorized Species, Move, or Ability mappings.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits, UPR-FVX changes, submodule repins, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Pokemon data reviewed alias table

- Treat `01_docs/analysis/pokemon-data-reviewed-alias-table.md` and `07_scripts/data_audit/showdown_aliases.json` as the current reviewed alias/ignore handoff.
- Expand the alias table only in small review batches: remaining regional form aliases, remaining GMax/Giga species names, remaining Z/Max/GMax physical-special split moves, then explicit Ability behavior-risk entries.
- Keep `ignore` entries limited to deliberate Showdown-only forms such as Hidden Power typed variants; do not use ignores to hide uncertain mappings.
- Keep Ability behavior-risk entries separate from name aliases. A local normalized ability name is not evidence of true Gen9 behavior.
- Before any CFRU/DPE data-table update, require the generator/audit path to fail closed on uncategorized Species, Move, or Ability mappings.
- Continue excluding Pokemon Showdown data copies, raw reports, CFRU/DPE table edits, UPR-FVX changes, submodule repins, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Pokemon data Showdown mapping audit

- Treat `01_docs/analysis/pokemon-data-showdown-mapping-audit.md` as the current handoff for the Pokemon Showdown-to-CFRU/DPE mapping audit.
- Use `07_scripts/data_audit/showdown_mapping_audit.py` against an external Pokemon Showdown `data/` checkout only; do not vendor Showdown data into this repository.
- First review target: explicit alias map for Ogerpon Terastal form names between Showdown, CFRU `GREEN/BLUE/RED/GREY`, and DPE `*_TERASTAL` names.
- Second review target: Ability aliases. Treat local alias defines as unresolved behavior risk even when the normalized ability name exists locally.
- If preserving output, commit only a sanitized summary, not raw bulk comparison output, private paths, downloaded data, ROMs, saves, states, builds, screenshots, hashes, secrets, tokens or `.env` data.

# Next steps update - Pokemon data Gen9 inventory

- Treat `01_docs/analysis/pokemon-data-gen9-inventory.md` as the current source-backed handoff for Gen9 Pokemon data table planning.
- Next useful step is a read-only name/ID/form mapping audit from Pokemon Showdown data to local CFRU/DPE constants before any table edits.
- Keep ability work separate: current source shows Gen9 ability aliases can map to older CFRU effects, so true Gen9 ability behavior needs a dedicated CFRU engine audit before changing IDs or assignments broadly.
- Update order should stay conservative: constants/form mapping, DPE base stats and ability assignments, CFRU move data, CFRU/DPE learnset sync, egg moves, TM compatibility, then tutor compatibility last.
- Do not change CFRU/DPE data tables, UPR-FVX code, submodule pins, ROMs, saves, emulator states, builds, tool binaries, screenshots, raw logs, hashes, private paths, `.local.json`, secrets, tokens or `.env` data without a separate implementation task.

# Next steps update - CFRU Randomizer baseline config local smoke

- Treat `08_tests/randomizer/cfru-randomizer-baseline-config.md` as the current sanitized local smoke record for CFRU Randomizer Baseline Config.
- Status: `PASS_TARGETED_LOCAL_BUILD_BOOT_SETTINGS_SMOKE_WITH_CAVEATS`.
- Keep the current result limited to local clean rebuild, mGBA boot, and targeted in-game settings behavior.
- Follow-up evidence, if needed, should separately verify the currently inconclusive rows: Oak tutorial removed, poison overworld faint, SwSh catch-level malus off, old/flat EXP behavior, and intro controls guide skipped.
- Keep Nuzlocke and Wild Prebattle toggle claims scoped to the reported targeted settings smoke unless a later sanitized gameplay matrix broadens them.
- Do not promote this to full-playthrough, BizHawk, Ironmon Tracker or P1 support.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU Randomizer baseline config

- Treat CFRU commit `53273184bab06f91cdc3ad6e0e5af4a8ba41591a` on branch `feature/cfru-randomizer-baseline-config` as the current Randomizer-/Ironmon-near baseline config candidate.
- Treat `08_tests/randomizer/cfru-randomizer-baseline-config.md` as the source-backed implementation handoff.
- Run a local clean CFRU rebuild from this commit.
- Run a targeted sanitized menu smoke: Page 3 should show `Level Scaling`, `Trainer AI`, `Hard Cap`, `Nuzlocke`, `Wild Prebattle`, and `Cancel`.
- Verify opening and closing the menu without changing `Nuzlocke` or `Wild Prebattle` leaves the existing flags unchanged.
- Verify explicit `Nuzlocke Off/On` only clears/sets `FLAG_NUZLOCKE`.
- Verify explicit `Wild Prebattle Off/On` only clears/sets `FLAG_ENABLE_WILD_PMN_PREBATTLE_SCREEN`.
- Run a small sanitized gameplay smoke for the compile-time baseline: Oak tutorial removed, poison can faint in overworld, no SwSh higher-level catch malus, old/flat EXP behavior, and skipped intro controls guide.
- Keep `FLAG_WILD_POKEMON_PREBATTLE_SCREEN` treated as transient encounter/window state, not menu-owned configuration.
- Do not promote this to full-playthrough, BizHawk, Ironmon Tracker or P1 support without separate evidence.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Trainer AI Policy v3 local smoke

- Treat `08_tests/randomizer/trainer-ai-policy-v3.md` as the current sanitized local smoke record for Trainer-AI-Policy v3.
- Status: `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`.
- Keep the current result limited to local build/boot/menu and targeted mGBA move-choice behavior.
- If Trainer-AI work continues, use fresh source-backed analysis before changing scoring logic; do not infer a global AI-quality result from this smoke.
- Optional follow-up: broaden only with sanitized A/B tables for additional trainer classes or separate Protect/Fake-Out micro-smokes, still without ROMs, saves, states, screenshots, raw logs, hashes or private paths.
- Do not promote this to full-playthrough, BizHawk, Ironmon Tracker or P1 support.

# Next steps update - Trainer AI Policy v3 experiment

- Treat CFRU commit `74310deeb62c7f73ba6c7b11f921418617a9a740` on branch `experiment/trainer-ai-policy-v3` as the current Trainer-AI Policy v3 experiment.
- Treat `08_tests/randomizer/trainer-ai-policy-v3.md` as the smoke handoff.
- Run a local mGBA A/B smoke from the same pre-Rival battle state across Trainer AI `Vanilla`, `Normal`, `Smart`, `Hard`, `Expert`, and `Auto`.
- Keep Game Difficulty, Level Scaling, Hard Cap, player actions, party, and items fixed except where the row explicitly tests `Auto` derivation.
- Record only sanitized turn summaries: AI option, Game Difficulty for `Auto`, turn number, enemy move selected, player Accuracy stage bucket, whether Tackle looked meaningful or KO-relevant, and result category.
- Add a separate small doubles micro-smoke only if validating the Hard/Expert Protect-Fake-Out retarget gate; do not mix that with the Rival Smokescreen result.
- Watch especially for `Smart`: it should show full smart move AI but no Expert extras such as shift-switching, player-switch prediction or type-resist berry hidden knowledge.
- Do not claim full-playthrough, BizHawk, Tracker or P1 support from this experiment.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Trainer AI Smokescreen behavior analysis

- Treat `01_docs/analysis/trainer-ai-smokescreen-behavior.md` as the current source-backed handoff for the Rival `Tackle` + `Smokescreen` behavior.
- Run a local mGBA A/B smoke from the same pre-Rival battle state, comparing Trainer AI `Auto`, `Vanilla`, `Normal`, `Hard`, `Expert`, and `Smart`; add `Easy` only if a weaker-AI comparison is useful.
- Record only sanitized turn summaries: AI option, turn number, enemy move selected, player Accuracy stage bucket, whether Tackle looked meaningful or KO-relevant, and result category.
- Classify results as plausible, suspicious, clear bug, or design mismatch before proposing any CFRU scoring change.
- Do not change CFRU or UPR-FVX code from the single observation. If `Smart` v2 still overuses Smokescreen in a simple damage-vs-Accuracy-drop setup, design a narrow v3 proposal around repeated Accuracy-down dampening or damage-over-neutral-utility tie-breaks.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - MacBook rebuild success status sync

- Treat `01_docs/setup/macbook-rebuild-success.md` as the current sanitized local MacBook rebuild status.
- Treat UPR-FVX compat commit `1a597a667129b50284dd88afb231372b5bd01d7f` as the current locally confirmed workspace pin.
- Current local baseline: UPR-FVX builds with `./gradlew clean :random:jar`, UPR-FVX GUI starts with Java 25, devkitPro/devkitARM and required GBA build tools are present, local Wine wrappers for `wav2agb.exe` / `mid2agb.exe` are present, DPE and CFRU rebuild locally, and the final local CFRU+DPE Gen9 ROM candidate loads in UPR-FVX and boots in mGBA.
- Next major compatibility block remains BizHawk plus Ironmon Tracker validation.
- Do not promote this rebuild sync to full-playthrough, BizHawk, Tracker or P1 support; keep it as a local environment and mGBA boot baseline.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, ROM hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU settings split final smoke

- Treat `08_tests/randomizer/cfru-settings-split-final-smoke.md` as the current sanitized final local smoke record for the CFRU settings-split UI.
- Status: `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`.
- If a later regression appears, isolate it by setting owner first: Game Difficulty, Trainer Level Scaling, Trainer AI, Hard Cap, Wild Level Scaling, or UPR-FVX Randomizer-only trainer settings.
- Optional future coverage can add a broader route/trainer matrix, a hard-cap boundary matrix, or a Trainer-AI quality evaluation, but this smoke should not be upgraded into a full-playthrough claim.
- Keep Better Movesets and Trainer Rows treated as UPR-FVX Randomizer-only baseline unless a separate source-backed task reopens them.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU hard level cap option row

- Treat CFRU `feature/cfru-settings-hard-level-cap-option` as the implementation branch for exposing Hard Level Cap on option-menu Page 3.
- Verify in a later local menu smoke that Page 3 shows `Level Scaling / Trainer AI / Hard Cap / Cancel`.
- Verify raw `VAR_HARD_LEVEL_CAP_MODE == 0` displays `Auto` and opening/closing the menu without changing the row leaves raw `0` and `FLAG_HARD_LEVEL_CAP` untouched.
- Verify explicit `Off` writes raw `1` and clears `FLAG_HARD_LEVEL_CAP`; explicit `On` writes raw `2` and sets `FLAG_HARD_LEVEL_CAP`.
- Confirm `FLAG_KEPT_LEVEL_CAP_ON` remains untouched by menu interactions and continues to be only challenge-tracking state.
- Do not mix any follow-up with EXP, Rare Candy, Daycare, DexNav, Wild, or Trainer Level Scaling enforcement changes unless a separate source-backed implementation branch is requested.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU hard level cap menu option analysis

- Treat `01_docs/analysis/cfru-hard-level-cap-menu-option.md` as the implementation handoff for adding Hard Level Cap to CFRU option-menu Page 3.
- Recommended later UI row: `Hard Cap = Auto / Off / On`, after `Level Scaling` and `Trainer AI` and before `Cancel`.
- Before implementation, confirm `0x515C` is still free; if so, use `VAR_HARD_LEVEL_CAP_MODE = 0x515C` with raw `0=Auto`, `1=Off`, `2=On`.
- Keep `FLAG_HARD_LEVEL_CAP` as the enforcement flag and preserve script-owned behavior while mode raw is `0=Auto`.
- Do not set `FLAG_KEPT_LEVEL_CAP_ON` from the option menu; source only proves a clear path for challenge tracking, not a safe menu-owned set path.
- Regression scope for implementation: raw Auto unchanged menu close, explicit Off clears hard cap, explicit On sets hard cap, Page 3 layout remains `Level Scaling / Trainer AI / Hard Cap / Cancel`, and no Trainer Level Scaling behavior changes.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU game difficulty vanilla option analysis

- Treat `01_docs/analysis/cfru-game-difficulty-vanilla-option.md` as the current handoff for deciding whether CFRU `Game Difficulty` needs an explicit `Vanilla` value.
- If the project only needs "CFRU Normal without Hard/Expert rules", keep Variant A and do not add a value.
- If the project needs FireRed-/Ironmon-near no-Difficulty power/rules while keeping Trainer Level Scaling and Trainer AI separate, implement Variant B later: add `Difficulty = Vanilla` with a new raw value, keep raw `0 = Normal`, and avoid raw-order comparisons.
- Before implementation, decide how Vanilla should handle trainer EV spreads, runtime randomized-trainer evolution, raid item punishment, fog behavior, wild boss scaling, and wild/raid AI hardening.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU trainer level scaling gate

- Treat CFRU `feature/cfru-enable-trainer-level-scaling-gate` as the implementation branch that makes the existing split `Trainer Level Scaling` setting reachable at runtime.
- Re-run the sanitized local runtime smoke with one Lv17 party mon and an early generic Viridian Forest-style Bug Catcher.
- Expected result with `Level Scaling = Expert`: the trainer should scale visibly above the original Lv9/Lv10 range, roughly around Lv15 for a flat early generic team.
- Regression check with `Level Scaling = Off`: the same trainer should remain at source levels even if Game Difficulty is Expert.
- Regression check with `Level Scaling = Auto`: raw `VAR_TRAINER_LEVEL_SCALING_MODE == 0` should continue to derive from `VAR_GAME_DIFFICULTY`.
- Do not treat the newly defined optional `FLAG_SCALE_WILD_BOSS_LEVEL` as a Wild Level Scaling feature rollout; it is present only because the compiled trainer-scaling code already references it and should remain unset unless a separate wild-boss plan uses it.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU trainer AI profile option row

- Treat CFRU `feature/cfru-settings-trainer-ai-profile-option` as the implementation branch for the second split-setting UI row.
- Verify in a later local gameplay/menu smoke that `Auto` displays for raw `VAR_TRAINER_AI_PROFILE == 0`, and that opening/closing the menu without changing the row keeps raw `0`.
- Verify explicit `Vanilla`, `Easy`, `Normal`, `Hard`, `Expert`, and `Smart` selections write raw `1..6` without changing `FLAG_SMART_TRAINER_AI`.
- Keep the existing `Game Difficulty` row unchanged until a separate branch explicitly handles display ordering or labeling.
- Do not change Trainer Level Scaling behavior from this branch; the only Level Scaling touch should remain page-array accommodation for the additional row.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU level scaling option row

- Treat CFRU `feature/cfru-settings-level-scaling-option` as the implementation branch for the first split-setting UI row.
- Verify in a later local gameplay/menu smoke that `Auto` displays for raw `VAR_TRAINER_LEVEL_SCALING_MODE == 0`, and that opening/closing the menu without changing the row keeps raw `0`.
- Next UI branch can add `Trainer AI` using the same original-raw plus dirty-tracking pattern for `VAR_TRAINER_AI_PROFILE`.
- Keep the existing `Game Difficulty` row unchanged until a separate branch explicitly handles display ordering or labeling.
- Do not add Better Movesets or Trainer Evolution to CFRU; those remain UPR-FVX Randomizer settings.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU settings UI split implementation plan

- Treat `01_docs/analysis/cfru-settings-ui-tab-implementation-plan.md` as the current handoff for implementing the CFRU in-ROM split settings UI.
- First implementation branch should extend option-menu page 2 with `Level Scaling` and preserve raw `VAR_TRAINER_LEVEL_SCALING_MODE == 0` unless the user changes that row.
- Second implementation branch should add `Trainer AI` with the same raw `0 = legacy/unset` preservation and explicit raw `1..6` writes only after user changes the setting.
- Add dirty/original-raw tracking before converting helper-derived display values back to saved vars; otherwise opening and closing the menu would accidentally migrate old saves.
- Keep Better Movesets and Trainer Evolution out of CFRU; they remain UPR-FVX Randomizer settings.
- Defer a third option-menu page, Wild/Raid AI profile, CFRU runtime randomized-trainer evolution toggle, and schema/debug UI until separate source-backed plans exist.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU difficulty power/rules mode split

- Treat CFRU `feature/cfru-difficulty-power-rules-mode` as the implementation branch for making `GetGameDifficultyMode()` the single internal read path for Difficulty-owned power and rules behavior.
- Review the semantic caveats before UI work: option-menu storage still writes `VAR_GAME_DIFFICULTY` directly by design, and `src/util.c` remains the compatibility bridge for existing saves/scripts.
- Do not merge Trainer Level Scaling, Trainer AI Profile, or Smart Trainer AI behavior back into Difficulty; those paths should continue using their split helpers.
- Decide later whether CFRU runtime randomized-trainer evolution deserves a separate randomizer/runtime setting instead of continuing to derive from DifficultyMode.
- Decide later whether Wild/Raid AI should stay Difficulty-owned or receive a separate Wild/Raid AI profile; this branch only routes the existing fallback through `GetGameDifficultyMode()` without changing behavior.
- Before UI work, add explicit settings-write plumbing for Difficulty, Trainer Level Scaling, and Trainer AI Profile while preserving `0 = legacy/unset` for the split vars.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU trainer AI profile mode split

- Treat CFRU `feature/cfru-trainer-ai-profile-mode` as the implementation branch for separating Trainer AI Profile from the base Difficulty bundle.
- Next CFRU AI branch should leave Wild/Raid AI on the old Difficulty gates unless a separate Wild/Raid AI profile is explicitly designed.
- Before UI work, add profile-write plumbing that can set `VAR_TRAINER_AI_PROFILE` explicitly while leaving unset/`0` saves on legacy `VAR_GAME_DIFFICULTY` plus `FLAG_SMART_TRAINER_AI` behavior.
- Keep explicit `TRAINER_AI_PROFILE_VANILLA` as "trainer data AI flags only", with no Difficulty AI uplifts.
- Continue keeping Trainer Level Scaling, Trainer Power, bag/move restrictions, Wild/Raid behavior, and battle rules out of Trainer AI Profile migrations.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU trainer level scaling mode split

- Treat CFRU `feature/cfru-trainer-level-scaling-mode` as the implementation branch for separating Trainer Level Scaling from the base Difficulty bundle.
- Next CFRU migration branch should either move a clearly bounded Difficulty category, such as Hall of Fame display or trainer-power reads, or continue with a separate design for Wild/Raid scaling before touching `GetScaledWildBossLevel()`.
- Keep `GetScaledWildBossLevel()` on the old difficulty path until a separate Wild/Raid scaling setting is explicitly designed.
- Keep CFRU runtime scaling-linked evolution separate from UPR-FVX Trainer Evolution; do not route UPR-FVX write-time evolution settings through CFRU runtime scaling vars.
- Before UI work, add profile-write plumbing that can set `VAR_TRAINER_LEVEL_SCALING_MODE` explicitly while leaving unset/`0` saves on legacy behavior.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU difficulty split mode helpers

- Treat the CFRU helper branch as the current implementation baseline for split difficulty storage.
- Next CFRU branch should migrate existing `VAR_GAME_DIFFICULTY` reads gradually through the new helpers, starting with low-risk display or isolated trainer-level-scaling call sites.
- Preserve the rule that unset split vars (`0`) keep legacy behavior through `VAR_GAME_DIFFICULTY`; do not default invalid explicit values to weaker modes.
- Use `IsSmartTrainerAIEnabled()` for the legacy `FLAG_SMART_TRAINER_AI` override instead of treating the flag as a full profile-wide Smart AI upgrade.
- Do not move wild or raid AI behavior into `TrainerAIProfile` until a separate Wild/Raid AI setting is designed.
- Keep UPR-FVX Better Movesets and Trainer Evolution separate from CFRU runtime level scaling and AI profile settings.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU difficulty split var/mode plan

- Treat `01_docs/analysis/cfru-difficulty-split-var-mode-plan.md` as the current implementation handoff for CFRU split-setting storage.
- First implementation branch should add helpers around existing behavior before moving call sites: `GetGameDifficultyMode()`, `GetTrainerLevelScalingMode()`, `GetTrainerAIProfile()`, and `IsSmartTrainerAIEnabled()`.
- Use `VAR_GAME_DIFFICULTY` for `DifficultyMode`; add `VAR_TRAINER_LEVEL_SCALING_MODE` at `0x515A` and `VAR_TRAINER_AI_PROFILE` at `0x515B`; keep raw `0 = legacy/unset` for both new vars.
- Keep `FLAG_SMART_TRAINER_AI` as a trainer-only legacy/script compatibility override while the new AI profile var is unset.
- Do not move wild/raid AI gates into `TrainerAIProfile` in the first implementation; leave them on difficulty behavior until an explicit Wild/Raid AI setting is designed.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU difficulty settings UI split design

- Treat `01_docs/analysis/cfru-difficulty-settings-ui-split-design.md` as the current source-backed map before implementing any CFRU difficulty split.
- Next implementation should first introduce separate internal settings for `DifficultyMode`, `TrainerLevelScalingMode`, and `TrainerAIProfile`, then move each existing `VAR_GAME_DIFFICULTY` read according to the mapping table.
- Keep Better Movesets and Trainer Evolution in UPR-FVX Randomizer-only settings; do not wire them into CFRU runtime difficulty vars.
- Before assigning new CFRU var IDs, audit the CFRU var range and decide whether `VAR_GAME_DIFFICULTY` remains a compatibility alias for `DifficultyMode`.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - Final Trainer Better Movesets smoke

- Treat `08_tests/randomizer/trainer-better-movesets-randomized-species-smoke.md` as the current targeted local evidence that the Trainer / Better Movesets / Route 22 regression cluster is clean for the tested profile.
- Do not reopen Better-Movesets stale-move or Route-22 weak Rival carryover work from slot `0` observations alone; weak Route 22 protected starter carryover is slot `1`, while slot `0` remains randomizable.
- For future suspicious low-level moves, first run or inspect the Better-Movesets source audit. `TUTOR` or `TM_HM` with `fallback=yes` is expected behavior for Better Movesets, not a stale-original-moves proof.
- With the Trainer baseline clean, continue Smart-Trainer-AI A/B smoke separately so AI move-choice findings are not conflated with Trainer write/reload or Better-Movesets issues.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - UPR-FVX Better Movesets source audit

- For the sanitized Graveler Lv7 / Hurricane-style cases, run the private local randomizer workflow with `uprfvx.trainerBetterMovesetsSourceAudit=true` and narrow it with `uprfvx.trainerBetterMovesetsSourceAuditTrainerId` plus `uprfvx.trainerBetterMovesetsSourceAuditSlot`.
- Expected diagnostic line shape: `trainer=<id> slot=<slot> species=<name> level=<level> chosenMove=<name>(<id>) sources=[...] fallback=<yes|no>`.
- Interpret `TM_HM` / `TUTOR` with `fallback=yes` as the low-probability fallback branch from Better Movesets, not as proof of stale original trainer moves.
- If a chosen move reports `[not-in-recorded-pool]`, inspect whether it was written by a later non-Better-Movesets path before changing trainer move selection.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - UPR-FVX Better Movesets pool rules

- Treat `01_docs/analysis/upr-fvx-better-movesets-pool-rules.md` as the current source-backed explanation for Trainer Better Movesets pool construction.
- For future suspicious low-level trainer moves, do not classify them as stale/original moves until the final randomized level-up, TM/HM, tutor, egg, and compatibility sources have been checked for the final trainer species.
- If more precision is needed, add a diagnostic-only pool audit for one sanitized trainer id/slot that reports source categories and move-name categories without private paths, ROMs, raw logs, seeds, hashes, screenshots, saves, builds, or local addresses.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - UPR-FVX runtime trainer source overlap-free save

- Treat the merged old-range runtime trainer source save as the current implementation candidate for the saveRom crash after the CFRU/DPE `partyFlags=3` 32-byte layout fix.
- Re-run the local private randomizer save that previously failed with `Can't free a space that is already freed`. Expected result: save completes without weakening `FreedSpace`.
- Then rerun the private trainer write/reload audit and the sanitized gBattleMons smoke for held-item custom-move trainers. Expected result: no raw output mismatch warnings and no leading empty move slot caused by the old classic layout.
- If save still fails, capture only sanitized trainer id, partyFlags category, old range length class, and overlap yes/no; do not document raw addresses, paths, logs, ROMs, saves, builds, hashes, screenshots, local addresses, secrets, tokens or `.env` data.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - UPR-FVX CFRU held-item custom-move rows

- Treat the CFRU/DPE `partyFlags=3` expanded writer/reloader as the current implementation candidate for held-item custom-move rows.
- Re-run the local sanitized Trainer Better Movesets smoke with a freshly built UPR-FVX jar and fresh output ROM. Focus on enemy rows that have both held items and custom moves; expected result is no leading empty move slot caused by the old classic 16-byte decode/write.
- Re-run the private trainer write/reload audit. Expected row context for CFRU/DPE held-item custom moves is `layout=cfru-held-item-custom-moves`, `bytesPerSlot=32`, item offset `20`, move offset `22`, and no raw output mismatch warnings.
- If `gBattleMons` still shows `[-/Move/Move/Move]` after the audit stays clean, re-check whether `FLAG_POKEMON_RANDOMIZER` causes CFRU to skip custom trainer moves and generate/default moves at runtime.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU runtime custom move construction

- Treat `01_docs/analysis/cfru-runtime-custom-move-construction.md` as the current source-backed split between UPR-FVX raw trainer audit, CFRU runtime trainer construction, and Tracker `gBattleMons` reads.
- Next minimal diagnostic branch should report the affected trainer id/slot plus sanitized `partyFlags`, has-item/custom-move state, writer row size, writer move offset, and whether the row is decoded as classic Gen3 or CFRU expanded layout.
- Prioritize the CFRU/DPE held-item custom-move layout mismatch: UPR-FVX no-item custom rows match CFRU, but held-item custom rows likely need a CFRU/DPE-specific 32-byte writer/reloader.
- Also verify whether `FLAG_POKEMON_RANDOMIZER` is active in the local smoke, because CFRU can skip applying custom trainer moves under that flag; if so, inspect generated move assignment separately from Better Movesets.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data.

# Next steps update - CFRU runtime trainer vs Tracker slot

- Install the updated `CFRUDPEExtension.lua` and rerun the sanitized local Route-22 Rival smoke with local ignored keys for `gBattleMons`, `gBattlerPartyIndexes`, `gBattleTypeFlags`, and `gTrainerBattleOpponent_A`.
- Expected diagnostic improvement: `partySlot[...]` now reflects CFRU's 16-bit `gBattlerPartyIndexes` slots and shows `-` when absent/out of range; snapshot context shows raw battle flags and trainer IDs when local keys are present.
- Interpret weak Route-22 slot-aware evidence as follows: slot `0` may be randomizable, while protected starter carryover is slot `1`.
- If a stable `partySlot[1]` observation still contradicts the clean UPR-FVX write/reload audit, investigate CFRU runtime trainer construction next, especially `setCustomMoves`, randomizer flags, and battle transition timing.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU/DPE Tracker party-index snapshot

- Install the updated `CFRUDPEExtension.lua` plus committed `source-data.json` into the local Tracker extension folder.
- Add `Addresses.gBattlerPartyIndexes` to the local ignored `game-addresses.local.json` when a safe local symbol source provides it. Do not commit the address or local JSON.
- Re-run a sanitized Route-22 Rival battle smoke and use `partySlot[...]` to distinguish the randomizable opponent slot `0` from the protected weak Route-22 starter slot `1`.
- If snapshots show `partySlot[-]`, treat that as missing local address metadata, not as a `gBattleMons` reader failure.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - UPR-FVX CFRU/DPE output ROM reload detection

- Re-run the private-ROM trainer write/reload audit with both `-D` paths from the current UPR-FVX branch.
- Expected result after the reload-detection fix: randomized output-ROM trainer load should keep `cfruDpeMode=true` and no longer classify expanded trainer raw IDs such as `rawSpecies=1375` or `rawMove=643` as out-of-bounds due to small reload bounds.
- If the audit still fails with `cfruDpeMode=false`, inspect which table-profile condition failed: Gen9 BaseStats anchors, `gLevelUpLearnsets`, `gTMHMLearnsets`, `gTMHMMoves`, `gMoveNames`, or `gBattleMoves`.
- If reload succeeds, continue the raw trainer write/reload audit before making any further Rival or Better-Movesets changes.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX output ROM expanded bounds reload

- Re-run the private-ROM trainer write/reload audit with both `-D` paths from the current UPR-FVX branch.
- Expected trainer-load failure context now includes `cfruDpeMode`, `loadedSpeciesCount`, and `loadedMoveCount`.
- If `cfruDpeMode=false` or counts are below CFRU/DPE Gen9 expectations (`loadedSpeciesCount=1440`, `loadedMoveCount=992`), inspect why randomized output-ROM reload did not activate expanded CFRU/DPE detection before trainer rows were decoded.
- If counts are correct but `rawSpecies=1375` or `rawMove=643` still report out-of-bounds, inspect array population/null slots rather than Rival or Better-Movesets logic.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX trainer-load raw slot diagnostics

- Re-run the private-ROM trainer write/reload audit with both `-D` paths from the current UPR-FVX branch.
- Expected trainer-load failure context now distinguishes whether trainer `1` slot `0` fails because `rawSpecies`, `rawItem`, or one of the `rawMoves` is out-of-bounds.
- If `speciesStatus=out-of-bounds`, inspect trainer species write/reload identity for that row. If move statuses are out-of-bounds while species is valid, inspect custom-move write/layout handling for `partyFlags=1`.
- If all raw values are in-bounds but the crash remains, inspect whether the read layout inferred from `partyFlags` matches the actual CFRU/DPE TrainerMon bytes.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX trainer-load bounds diagnostics

- Re-run the private-ROM trainer write/reload audit with both `-D` paths from the current UPR-FVX branch.
- Expected trainer-load failure shape now includes sanitized row context: `trainer=<id>`, `slot=<slot-or-header>`, `layout=<layout>`, `partyFlags=<flags>`, `partyCount=<count>`, and offset/pointer classes.
- If `partyPointer` or `slotOffset` is `out-of-rom`, inspect trainer-party pointer writing/repointing for that trainer ID before changing Rival or Better-Movesets logic.
- If offsets are `in-rom` but the exception remains, inspect species/item/move raw value bounds for that trainer layout and slot.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX randomized output ROM reload diagnostics

- Re-run the private-ROM trainer write/reload audit with both `-D` paths from the current UPR-FVX branch.
- Expected failure shape now includes a sanitized load phase: `Configured randomized ROM could not be loaded during <phase>: <ExceptionClass>`.
- If the phase is `trainer load`, focus next on raw trainer pointer/species/item/move bounds during reload of the output ROM. If it is an earlier data-table phase, audit that table's repointed offset/count assumptions first.
- Once the randomized output ROM loads, continue with the raw output trainer audit before changing Randomizer behavior or CFRU runtime code.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX trainer audit ROM loading hardening

- Re-run the private-ROM audit with both `-D` paths.
- If ROM loading still fails, use the role in the sanitized failure message to decide whether the base ROM or randomized ROM is the failing input.
- Expected failure shape is `Configured base ROM could not be loaded: <ExceptionClass>` or `Configured randomized ROM could not be loaded: <ExceptionClass>`, with no private path printed.
- Once both ROMs load, continue with the audit report classification before any further UPR-FVX or CFRU runtime changes.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX trainer audit property forwarding

- Re-run the private-ROM audit with regular `-D` properties from `02_external/upr-fvx`; the `romio:test` task now forwards the two audit ROM properties into the forked test JVM.
- Expected local result with valid private paths: the post-randomization audit should no longer be `SKIPPED`, and test output should print the sanitized `reportPath=build/reports/diagnostics/...` line plus summary/warnings.
- If it still skips, inspect the local Gradle test XML/HTML to verify property delivery before changing audit logic.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX trainer audit report output

- Re-run the opt-in private-ROM post-randomization audit from `02_external/upr-fvx`.
- If the report is hard to locate, use the printed sanitized `reportPath=build/reports/diagnostics/trainer-runtime-source-post-randomization-audit-report.txt` line from test output.
- Use the printed summary and warning lines only to classify the layer; inspect the full local report privately for row details.
- If the test fails on report writing, treat that as an infrastructure problem before interpreting any Route-22/Rival/Better-Movesets evidence.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX trainer write/reload audit

- Use the new post-randomization runtime-source audit before any further Route-22/Rival/Better-Movesets fixes.
- First prove the local smoke uses a freshly generated output ROM from the current UPR-FVX branch. Then run the opt-in private-ROM audit and inspect only sanitized local findings.
- If `outputRawParty` shows `moves=[0, ...]`, classify the failure as output-ROM trainer data or stale generation context, not CFRU runtime.
- If the audit warns that the Route-22 protected starter differs from the Oak-Lab opening Rival starter, continue in UPR-FVX route/source-row handling.
- If raw output trainer data is compact and protected starter slots match, investigate CFRU runtime trainer construction or the local smoke context before changing UPR-FVX again.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX actual Route-22 Rival starter slot

- Treat the FRLG Route-22 post-opening sync as the current implementation candidate for the confirmed Oak Lab `Magcargo Lv5` -> Route-22 `Arctozolt Lv9` mismatch.
- Re-run the local sanitized Route-22 Rival smoke with a freshly built UPR-FVX jar and freshly generated output ROM. Expected result: the weak Route-22 protected starter slot carries the final Oak Lab Rival starter Species; nonstarter Route-22 slots may still randomize.
- Validate both early Route 22 and, if reachable, late Route 22: early protected slot is `1`, late protected slot is `5`.
- Keep this separate from Move-Slot/Better-Movesets validation, which is not changed in this block.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX Route-22 Rival starter carryover

- Treat the explicit FRLG Rival force-slot metadata as the current implementation candidate for the remaining Route-22 starter-carryover failure.
- Re-run the local sanitized Route-22 Rival smoke with a freshly built UPR-FVX jar and freshly generated output ROM. Expected result: the weak Route-22 protected starter slot carries the lab Rival counter-starter; nonstarter Route-22 slots may still randomize.
- Keep Better Movesets validation separate: move slots should remain compact from the previous final normalization fix, and Better Movesets should compute moves for the final Route-22 starter Species after carryover.
- If the Route-22 starter still mismatches, capture only sanitized trainer context, starter choice, party slot, Species, Level, and move names. Do not copy raw logs, screenshots, hashes, paths, local addresses, ROMs, saves, emulator states, builds, tool binaries, secrets, tokens, or `.env` data.

# Next steps update - UPR-FVX final trainer move normalization

- Treat the new final pre-write normalization as the current implementation candidate for lingering `[-/Move/Move/Move]` trainer rows after Better Movesets.
- Re-run the local sanitized Route-22/Rival smoke with a freshly built UPR-FVX jar and freshly generated output ROM; expected result is that a randomizable Pidgey-slot replacement cannot enter battle with `moves[-/Tackle/Growl/Sandattack]`.
- If a leading empty slot still appears after confirming a fresh jar/output/save context, investigate CFRU runtime trainer construction or another non-UPR writer path separately.
- Keep Rival starter interpretation slot-aware: Route-22 nonstarter slots may randomize, while only the protected starter slot must match the starterbattle carryover.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX Route-22 Rival final moveslot normalization

- Treat the final writer/fallback normalization as the current implementation candidate for remaining `[-/Move/Move/Move]` trainer rows.
- Re-run the local sanitized Route-22/Rival smoke that produced `Decidueye Lv47` with `moves[-/Blizzard/Crunch/Psychocut]`; expected result is that any real moves are compacted into slot 0 onward.
- Continue recording Route-22 Rival observations with trainer context, party slot, level and whether the observed Pokemon is the protected starter slot or a randomizable nonstarter.
- If a Level-47 Rival still appears in the Route-22 context after this fix, investigate script/trainerbattle source selection separately from move-slot normalization.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX Rival starter / trainer move-slot regression

- Treat the UPR-FVX move-slot follow-up as the current implementation candidate: Better Movesets must compact away `MOVE_NONE` before writing trainer custom moves and clearing `resetMoves`.
- Re-run the local sanitized Trainer Species plus Better Movesets smoke with `gBattleMons`, focusing on formerly observed `[-/Lick/Tackle/Ember]`-style rows. Slot 0 should not be empty when later slots are populated from a valid move pool.
- For Route-22 Rival observations, record whether the visible enemy is the protected starter slot or a randomizable nonstarter slot before labeling it a carryover failure.
- Keep `TrainerSpecialRulesTest` as the ROM-free guardrail for Route-22-style equal-level Rival teams; broaden local smoke across all starter choices only if sanitized evidence still contradicts the guarded behavior.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX Trainer Better Movesets empty-pool fix

- Treat the UPR-FVX empty-pool fix as the current implementation candidate: Better Movesets only clears `resetMoves` after writing at least one move.
- Run the local sanitized smoke from `08_tests/randomizer/trainer-better-movesets-randomized-species-smoke.md` on a private output ROM: Trainer Species randomization plus Better Movesets, with `gBattleMons` validation for enemy Species/Level/Moves.
- Specifically re-check the prior `Incineroar Lv6`-style failure mode: a random Trainer Species must not carry old/original custom moves when the Better-Movesets pool is empty.
- Keep Rival-starter interpretation separate from ordinary Trainer/Nichtstarter findings until trainer ID and party slot are known.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - UPR-FVX Trainer Better Movesets with randomized species

- Treat `01_docs/analysis/upr-fvx-trainer-better-movesets-randomized-species.md` as the current source-backed diagnosis for stale/original trainer moves after Species randomization plus Better Movesets.
- Preferred implementation next step: in `TrainerMovesetRandomizer`, keep `resetMoves=true` until a non-empty Better-Movesets pool has actually written new move slots. Add a focused regression for the empty-pool path.
- Also audit the Gen3/CFRU-DPE fallback path around `getMovesAtLevel(tp.getSpecies().getNumber(), ...)` to confirm expanded Species identity handling is correct for random Trainer Species.
- Run the smoke plan in `08_tests/randomizer/trainer-better-movesets-randomized-species-smoke.md`: separate regular trainer, Rival forced-starter slot, and Rival/Trainer nonstarter findings, using only sanitized `gBattleMons` observations.
- Do not classify the current `Incineroar Lv6` observation as a Rival-starter failure until the trainer ID and party slot are identified.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, local addresses, secrets, tokens and `.env` data.

# Next steps update - CFRU/DPE tracker extension readers

- Treat the updated `CFRUDPEExtension.lua` snapshot as the current active-battle debug surface for sampled live `BattlePokemon` fields.
- Local smoke should now look for change-based `active-battle=snapshot P:... | E:...` lines with species, level, HP/max HP, type pair, ability, held item, primary status, and move/PP slots.
- Validate sanitized field plausibility in both wild and trainer battle states. Specifically compare type pair, ability name, held item name, and status changes against in-game-visible behavior without copying raw logs, screenshots, private paths, real addresses, or local JSON values.
- `type3` and raw `status2` are available in extension state but remain caveated until a later smoke decides how to display temporary extra-type and volatile status state.
- Stock Tracker UI still is not updated. Next options remain broader sanitized field validation, a safer battle-state gate, or an extension-owned visual/status panel.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, `offsets.ini`, generated `.local.json`, real local addresses, secrets, tokens and `.env` data.

# Next steps update - CFRU/DPE battle reader debug view

- Treat the updated `CFRUDPEExtension.lua` snapshot logging as the current local debug surface for `gBattleMons` active-battle reads.
- Local smoke should now look for `active-battle=loaded rows=...` followed by `active-battle=snapshot P:... | E:...` with species, level, HP/max HP, and move/PP slots.
- `active-battle=idle/no valid rows` is acceptable outside battle or during state transitions and should not be treated as a failure by itself.
- The reader still does not update stock Tracker UI. Next options are broader sanitized field validation, a safer battle-state gate, or an extension-owned visual/status panel.
- Continue excluding real local addresses, local JSON values, `offsets.ini`, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, secrets, tokens and `.env` data.

# Next steps update - CFRU/DPE gBattleMons reader smoke results

- Treat `08_tests/randomizer/cfru-dpe-gbattlemons-reader-smoke-results.md` as the current sanitized local evidence for the v1 extension-owned `gBattleMons` reader.
- Current result is `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`: source data and local ignored manifests load, and active-battle rows can plausibly report player-left/opponent-left species.
- Do not interpret this as stock Tracker UI support. v1 still stores data only in `extension.state.activeBattleMons`.
- Next useful follow-up is either a safer battle-state gate, an extension-owned debug/status display, or a broader sanitized smoke for HP, PP, move names, ability, and held item fields.
- Continue excluding real local addresses, local JSON values, `offsets.ini`, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, secrets, tokens and `.env` data.

# Next steps update - CFRU/DPE gBattleMons reader

- Install the updated `CFRUDPEExtension.lua` and `data/source-data.json` into the local Tracker `Lua/extensions/` layout.
- Provide ignored local `data/game-addresses.local.json` with `Addresses.gBattleMons`; add `Addresses.gBattlersCount` if a safe local symbol source provides it.
- Run the local smoke in a wild or trainer battle and inspect only sanitized status: `source-data=loaded`, manifest load state, and `active-battle=loaded rows=...` with plausible player-left/opponent-left fields.
- Do not expect stock Tracker team screens to update yet. The v1 reader stores data in `extension.state.activeBattleMons` and intentionally does not patch `Program.readNewPokemon` or `TrackerAPI.getActiveBattlePokemon`.
- Keep real local addresses, `offsets.ini`, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, secrets, tokens and `.env` data out of commits and documentation.

# Next steps update - CFRU/DPE gBattleMons reader design

- Treat `01_docs/analysis/cfru-dpe-gbattlemons-reader-design.md` as the current design boundary for the first CFRU/DPE active-battle live-data reader.
- Next implementation should be extension-owned and read-only: load local `gBattleMons`, prefer `gBattlersCount`, read `BattlePokemon` rows with source-backed size `0x58`, and store/display only extension state.
- Do not inject into stock `Program.GameData.PlayerTeam` / `EnemyTeam` in v1. Stock `TrackerAPI.getActiveBattlePokemon` still depends on party objects populated by the vanilla `Program.readNewPokemon` path.
- Minimal v1 display should cover player-left and opponent-left species, level, HP/max HP, moves and PP; doubles, hidden ability provenance, Tera/Gigantamax, party sync, bag and SaveBlock remain later work.
- If local symbols do not provide `gBattleMons`, stop and require a safe local symbol source or future CFRU/DPE metadata table. Do not document real local addresses, ROM paths, hashes, raw logs, screenshots or private paths.

# Next steps update - CFRU/DPE Tracker live RAM anchors

- Treat `01_docs/analysis/cfru-dpe-tracker-live-ram-anchors.md` as the current source-backed diagnosis for the failed live-data smoke.
- Do not interpret `game-addresses.local=true` or `tracker-overrides.local=true` as proof that Player, Enemy, Wild, or Battle data can be read. They only prove loader return status.
- Next implementation should first validate sanitized presence of live symbols such as `gPlayerParty`, `gEnemyParty`, `gBattleMons`, `gBattlersCount`, `gBattleMainFunc`, and `gBattlerPartyIndexes` in ignored local metadata.
- Prefer a small CFRU/DPE active battle reader around `gBattleMons` as the first useful v1 data path. Full party display needs a CFRU-aware `struct Pokemon` reader because stock `Program.readNewPokemon` expects vanilla encrypted Gen III substructures.
- Keep ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, `offsets.ini`, generated `.local.json`, real local addresses, secrets, tokens, and `.env` data out of commits and documentation.

# Next steps update - CFRU/DPE local tracker overrides generator

- Use `07_scripts/tracker/generate_cfru_dpe_tracker_overrides_local.py` to create a private ignored `tracker-overrides.local.json` for local Tracker layout smoke.
- Treat the generated file as local-only. Do not commit it or use it as proof of party, battle, trainer-party or bag correctness.
- Pair it with `source-data.json` and optional `game-addresses.local.json`, then verify locally whether `TrackerAPI.loadTrackerOverridesFromJson` updates the nested `Program.Addresses`, `PokemonData.Addresses`, and `MoveData.Addresses` fields actually consumed by read paths.
- Remaining blockers: CFRU party `struct Pokemon` decoding, live RAM addresses, SaveBlock/bag metadata, expanded TrainerMon support, hidden ability display, and move split/category behavior.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, `offsets.ini`, generated `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU/DPE local address generator

- Use `07_scripts/tracker/generate_cfru_dpe_game_addresses_local.py --offsets path/to/offsets.ini` to create a private ignored `game-addresses.local.json` for local Tracker smoke.
- Treat the generated file as local-only. Do not commit it, copy address values into docs, or use it as public truth.
- First smoke should confirm the extension loads `source-data.json` and optional `game-addresses.local.json`, then separately check warnings for missing `gPlayerParty`, `gEnemyParty`, `gBattleMons`, SaveBlock, and bag-pocket symbols.
- Live party, enemy, battle, and bag correctness remains blocked until those RAM/runtime symbols come from safe local metadata, a public symbol source, or a CFRU/DPE metadata table.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, `offsets.ini`, generated `.local.json`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU/DPE Tracker manifest path resolution

- For local Tracker smoke, install `CFRUDPEExtension.lua` directly in `Lua/extensions/` and copy committed source data to `Lua/extensions/data/source-data.json`.
- Optional private local manifests should live beside it as `Lua/extensions/data/game-addresses.local.json` and `Lua/extensions/data/tracker-overrides.local.json`.
- Re-test that `source-data.json` is found and logs counts. Missing `.local.json` files should still log as missing without failing startup.
- If source-data is still missing, inspect the extension console status and verify that the copied `data/` folder is directly below the folder containing `CFRUDPEExtension.lua`, not nested under `CFRUDPEExtension/data/`.
- Continue excluding local `.local.json` manifests, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, `offsets.ini`, secrets, tokens and `.env` data from commits.

# Next steps update - CFRU/DPE Tracker manifest loader smoke

- Treat `CFRUDPEExtension.lua` as the current loader-smoke implementation: it reads committed `source-data.json`, reports counts, and optionally loads ignored `game-addresses.local.json` / `tracker-overrides.local.json`.
- First local Tracker smoke should confirm the extension logs source-data counts and handles missing local manifests cleanly.
- Only after that, create private local `.local.json` manifests from safe metadata or sanitized local validation and verify TrackerAPI loader return status.
- Do not claim party, battle, trainer or bag correctness from loader smoke alone. Live-data correctness still requires safe addresses plus a CFRU-aware party/read strategy.
- Keep local `.local.json` manifests, ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, `offsets.ini`, secrets, tokens and `.env` data out of commits.

# Next steps update - CFRU/DPE Tracker layout overrides

- Treat `01_docs/analysis/cfru-dpe-tracker-layout-overrides.md` as the current source-backed boundary for Tracker layout/override candidates.
- Safe next generator work can emit layout candidates for `BattleMove`, `BattlePokemon`, `BaseStats`, `Trainer`, simple TrainerMon rows and bag `ItemSlot`/pocket counts, but must keep real ROM/RAM addresses local or metadata-derived.
- Do not treat `sizeofPokemonStruct` / `offsetPokemonSubstruct` as enough to fix CFRU party reads. CFRU `struct Pokemon` is expanded and direct, while stock Tracker `Program.readNewPokemon` expects vanilla encrypted substruct decoding.
- Before a local manifest smoke claims correctness, validate whether `TrackerAPI.loadTrackerOverridesFromJson` updates the nested `Program.Addresses`, `PokemonData.Addresses`, and `MoveData.Addresses` fields actually consumed by read paths. If not, use explicit extension-side nested assignment.
- Move category display needs specific validation because CFRU has a `BattleMove.split` byte while stock Tracker reads category bits from a flags byte.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, `offsets.ini`, secrets, tokens and `.env` data.

# Next steps update - CFRU/DPE Tracker source-data generator

- Treat `07_scripts/tracker/generate_cfru_dpe_source_data.py` as the current source-derived generator for `CFRUDPEExtension/data/source-data.json`.
- Regenerate with `python3 07_scripts/tracker/generate_cfru_dpe_source_data.py` after CFRU/DPE header updates.
- Generated data is counts, ID mappings, macro-derived fallback names and warnings only. It does not include real local addresses or values from `offsets.ini`.
- Next technical step is either layout generation/validation for Tracker overrides or a local ignored address smoke. Do not commit `game-addresses.json` / `tracker-overrides.json` with local values.
- Reconcile DPE item count `799` vs CFRU constants item count `779` before treating item mappings as final Tracker truth.

# Next steps update - Tracker Lua source inventory

- Treat `01_docs/analysis/tracker-lua-source-inventory.md` as the current checklist of inputs for the CFRU/DPE/Gen9 Tracker extension.
- Next implementation should start with a source-derived data generator for counts and ID mappings, not with Tracker-core edits.
- Use `TrackerAPI.lua`, `CustomCode.lua`, `GameSettings.lua`, `Program.lua`, NatDexExtension, CFRU/DPE headers and CFRU/DPE tables as source inputs.
- Keep local `offsets.ini` and `generatedrepoints` as diagnostic/local-override aids only. Do not commit them or copy full symbol dumps into documentation.
- First real manifest work should still avoid final local addresses; use ignored local `game-addresses.json` / `tracker-overrides.json` only for smoke until a public metadata/symbol path exists.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, secrets, tokens and `.env` data.

# Next steps update - CFRU/DPE Tracker manifest source map

- Treat `01_docs/analysis/cfru-dpe-tracker-manifest-source-map.md` as the current source-backed boundary for Tracker manifest generation.
- Commit-safe next data is source-derived only: counts, enum mappings, display-name mappings from source, layout candidates and pointer-slot metadata.
- Keep actual target addresses for party, battle, trainer, saveblock and repointed data tables in local ignored `game-addresses.json` / `tracker-overrides.json` until a public symbol source or CFRU/DPE metadata table exists.
- Reconcile DPE item count 799 vs. CFRU constants item count 779 before generating final item mappings.
- Preferred next implementation step: write a small generator for source-derived `source-data.json`, then separately design a CFRU metadata table or symbol-map reader for runtime addresses.
- Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, secrets, tokens and `.env` data.

# Next steps update - CFRU/DPE Tracker extension skeleton

- Treat `03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua` as the current external Tracker extension skeleton.
- The skeleton is load/unload and manifest-path plumbing only. It does not yet provide real CFRU/DPE species, move, ability, item, party, enemy, trainer or battle data.
- Next minimal implementation step: generate or manually curate local source-derived `game-addresses.json` and `tracker-overrides.json` from CFRU/DPE symbols, struct layouts and Tracker override fields.
- Keep committed files example-only until values are source-backed and sanitized. Do not commit ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, secrets, tokens or `.env` data.
- First local smoke should only claim extension load/unload and prepared manual profile. Data correctness requires filled non-example manifests and separate sanitized validation.

# Next steps update - CFRU/DPE Tracker extension design

- Treat `01_docs/analysis/cfru-dpe-tracker-extension-design.md` as the current implementation concept for a future public CFRU/DPE/Gen9 Ironmon Tracker extension.
- Do not fork Tracker core first. Prototype an external `CFRUDPEExtension.lua` that loads source-derived CFRU/DPE address/data manifests and restores any wrapped functions on unload.
- v1 should use manual profile activation unless a robust source-backed CFRU/DPE marker is identified. Do not reuse NatDexExtension's NatDex-specific mon-count detection without proof.
- First implementation smoke should prove species/move/ability/item mappings plus player party and live enemy battle data. Keep static trainer-party display caveated until runtime construction and randomizer behavior are validated.
- Keep BizHawk local only. Continue excluding ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds, tool binaries, secrets, tokens and `.env` data.

# Next steps update - Tracker memory API map

- Treat `01_docs/analysis/tracker-memory-api-map.md` as the current source-backed map for why stock Ironmon Tracker and NatDexExtension do not yet read CFRU/DPE/Gen9 correctly.
- Use `08_tests/randomizer/ironmon-tracker-cfru-dpe-compat-plan.md` for local sanitized Tracker smoke. Do not commit ROMs, saves, emulator states, screenshots, raw logs, hashes, private paths, builds or tool binaries.
- Preferred next technical step: generate or curate a small CFRU/DPE address/data manifest for Tracker consumption, then prototype a read-only CFRU/DPE Tracker extension.
- Do not force NatDexExtension on as a shortcut. Its detection marker, pointer metadata and ID maps are NatDex-specific unless proven otherwise for the local CFRU/DPE ROM.
- First extension smoke should prove player party, enemy party, active battle Pokemon, move names, ability names including hidden ability, and item names before claiming trainer-team fidelity.

# Next steps update - Tracker source references

- Treat `01_docs/analysis/tracker-source-reference-map.md` as the current source map for Ironmon Tracker, NatDexExtension `dev_new`, and BizHawk local-tool boundaries.
- Use `02_external/Ironmon-Tracker/ironmon_tracker/TrackerAPI.lua` first for Tracker API compatibility analysis, then inspect `Memory.lua`, `GameSettings.lua`, `Program.lua`, and `ironmon_tracker/data/PokemonData.lua`, `MoveData.lua`, `AbilityData.lua`, and `TrainerData.lua` as needed.
- Use `02_external/NatDexExtension/NatDexExtension.lua` as the `dev_new` extension entry point, but keep it as a CyanSMP64/NatDex reference rather than assuming it is a drop-in CFRU/DPE/Gen9 compatibility layer.
- Keep BizHawk local and ignored. Do not add a BizHawk source submodule or commit release zips, AppImages, builds, tool binaries, screenshots, raw logs, ROM paths, hashes, saves or emulator states.
- Recommended next analysis block: compare Tracker API and memory reads against CFRU/DPE/Gen9 species, moves, abilities, item IDs and battle/party memory assumptions.

# Next steps update - CFRU Expert AI isolation

- Treat `01_docs/analysis/cfru-expert-ai-isolation.md` as the current source-backed reference for Expert Difficulty vs. Smart Trainer AI v2.
- Do not use Expert Difficulty as a shortcut for Smart Trainer AI. Expert's ordinary trainer flag uplift is already represented by v2, while its broader effects include trainer strength, PP, level scaling, wild AI, player restrictions, battle rules and situational anti-cheese.
- For the next local smoke, compare Normal flag-off, Normal `FLAG_SMART_TRAINER_AI` v2 flag-on, and Expert only as a diagnostic reference. Record sanitized behavior only and note whether Expert changed levels, stats, evolutions or other non-AI context.
- If v2 still overuses Sand Attack/Accuracy-down, prefer a targeted utility-scoring or tie-break experiment, or a deeper Vanilla/NatDex `AI_CheckViability` / `AI_TryToFaint` port. Do not re-add `AI_SCRIPT_CHECK_GOOD_MOVE` globally without a focused scoring design.
- Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, builds, private paths, secrets, tokens and `.env` data.

# Next steps update - Smart AI patch source verification

- Treat `01_docs/analysis/smart-ai-patch-source-verification.md` as the current source-backed reference for original FireRed/LeafGreen Smart-AI patch behavior.
- Do not describe CFRU v1 as behavior-identical to Ironmon/NatDex `0x07`: tom-overton/NatDex use classic Gen3 `CHECK_BAD_MOVE | CHECK_VIABILITY | TRY_TO_FAINT`, while CFRU v1 used `CHECK_BAD_MOVE | SEMI_SMART | CHECK_GOOD_MOVE`.
- Keep CFRU v2 as the immediate smoke candidate: `FLAG_SMART_TRAINER_AI` should add `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART` while `VAR_GAME_DIFFICULTY` stays Normal.
- If v2 is too weak, decide explicitly between a source-port of Vanilla/NatDex `AI_CheckViability` / `AI_TryToFaint` semantics and a separate damage-/KO-oriented CFRU mode. Do not re-enable `CHECK_GOOD_MOVE` just for numeric `0x07` similarity without addressing utility/Accuracy-drop scoring.
- Continue excluding ROM paths, ROM hashes, full logs, screenshots, output ROMs, saves, emulator states, builds, patch assets, private paths, secrets, tokens and `.env` data.

# Next steps update - CFRU Smart Trainer AI v2 utility-spam reduction

- Treat Smart Trainer AI v2 as the current implementation candidate: `FLAG_SMART_TRAINER_AI` now adds `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`, not `AI_SCRIPT_CHECK_GOOD_MOVE`.
- Run the Pallet smoke path again on Normal Difficulty and compare flag off vs. flag on.
- Specific v2 regression focus: the earlier sanitized v1 observation was opposing Pidgey/Taubsi using Sand Attack/Sandwirbel four times despite Tackle being available. v2 should be checked for reduced Sand Attack/Accuracy-drop/utility spam while still avoiding clearly bad moves.
- Keep confirming that `VAR_GAME_DIFFICULTY`, trainer IVs, EVs, friendship, PP, levels, wild/raid AI, player bag access, player move restrictions, battle rules, Expert anti-cheese, Option Menu and Settings NPC behavior remain unchanged.
- If v2 is too weak, decide between a targeted scoring adjustment and a deeper NatDex/Ironmon `AI_CheckViability` / `AI_TryToFaint` source-port; do not re-enable Hard/Expert Difficulty as a shortcut.
- Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, builds, private paths, secrets, tokens and `.env` data.

# Next steps update - Smart AI move scoring comparison

- Treat `01_docs/analysis/smart-ai-scoring-comparison.md` as the current source-backed reference for why CFRU v1 Smart Trainer AI can prefer Sand Attack/status-style moves.
- Do not describe the current CFRU `FLAG_SMART_TRAINER_AI` v1 behavior as an exact Ironmon/NatDex Smart-AI port. It is numerically close to `0x07`, but CFRU `AI_SCRIPT_CHECK_GOOD_MOVE` uses broader positive utility scoring than NatDex `AI_CheckViability` / `AI_TryToFaint`.
- Next local smoke should explicitly record whether flag-on trainers prefer Accuracy-down/status/setup over direct damage, and separate "not bad move" from "damage-oriented smart move".
- If the project wants closer Ironmon/NatDex behavior, compare the current all-three-flags v1 against a conservative CFRU flag combination or design a deeper source-port of NatDex `AI_CheckViability` / `AI_TryToFaint` semantics.
- Continue keeping `VAR_GAME_DIFFICULTY` Normal and do not use Hard/Expert difficulty as a Smart-AI shortcut.
- Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, builds, private paths, secrets, tokens and `.env` data.

# Next steps update - CFRU Smart Trainer AI smoke confirmation

- In local flag-on smoke, trigger `EventScript_Pallet_FatGuy` and confirm the visible message `Smart Trainer AI enabled.` before entering sampled trainer battles.
- Keep the A/B split unchanged: baseline is Normal Difficulty without triggering the Pallet smoke script; test case is Normal Difficulty after the Pallet smoke script.
- Continue verifying that only trainer AI behavior changes and that `VAR_GAME_DIFFICULTY`, trainer stats, levels, wild/raid behavior, player restrictions, battle rules, Expert anti-cheese and shift-switch behavior remain Normal-equivalent.
- Do not treat this confirmation as final UX; Settings NPC, Option Menu, toggle and randomizer-profile wiring remain separate decisions after smoke evidence.

# Next steps update - CFRU Smart Trainer AI smoke activation

- Treat `EventScript_Pallet_FatGuy` in `02_external/CFRU-expansion/assembly/overworld_scripts/Pallet_town.s` as the current local-only smoke activation path for `FLAG_SMART_TRAINER_AI`.
- Run the local A/B smoke on Normal Difficulty: baseline with the Pallet test script not triggered, then flag-on after triggering the Pallet test script once.
- Confirm only trainer move-choice behavior changes; trainer IVs, EVs, friendship, PP, levels, wild/raid behavior, bag access, player move restrictions, battle rules, Expert anti-cheese and shift-switch behavior must remain unchanged.
- Do not treat the Pallet test script as final UX. If the smoke passes, decide separately between Settings NPC, Option Menu, or randomizer-profile wiring.
- Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, builds, private paths, secrets, tokens and `.env` data.

# Next steps update - CFRU Smart Trainer AI activation smoke plan

- Use `08_tests/randomizer/cfru-smart-trainer-ai-smoke-plan.md` as the current minimal test plan for `FLAG_SMART_TRAINER_AI`.
- Smallest next implementation step: add a tightly scoped early script-set activation for a local smoke profile, not a full Option Menu or Settings NPC UI yet.
- Run local A/B smoke with Normal Difficulty and flag off/on; share only sanitized pass/fail observations, not ROMs, saves, output logs, screenshots, hashes or private paths.
- If smoke passes, choose the durable activation surface: Settings NPC for controlled player-facing toggling, Option Menu for broad discoverability, or Randomizer-profile wiring for reproducible Ironmon-style profiles.
- Keep `VAR_GAME_DIFFICULTY` separate and continue testing that Smart Trainer AI does not affect trainer strength, level scaling, wild/raid behavior, player restrictions, battle rules or Expert anti-cheese paths.

# Next steps update - CFRU Smart Trainer AI runtime flag

- Review the CFRU v1 implementation of `FLAG_SMART_TRAINER_AI 0xA0E` on branch `feature/cfru-smart-trainer-ai-mode`.
- CFRU source commit: `eb1f3bff3fef83b46999e0513a7598b6bde601b8`.
- Next integration decision: how scripts, an NPC, option menu, or randomizer profile should set/clear the flag. No UI or NPC wiring exists yet.
- Test focus: compare Normal difficulty with and without `FLAG_SMART_TRAINER_AI`, confirming trainer AI improves while trainer IVs, EVs, friendship, PP, levels, wild/raid behavior, bag access, player move restrictions, battle rules, Expert anti-cheese and shift-switch behavior remain unchanged.
- Watch specifically for `AI_SCRIPT_CHECK_GOOD_MOVE` side effects, because v1 intentionally chooses NatDex/Ironmon `0x07` closeness over the weaker `AI_SCRIPT_SEMI_SMART`-only uplift.

# Next steps update - CFRU Smart AI flag mapping

- Treat `01_docs/analysis/cfru-smart-ai-source-port-map.md` as updated with the CFRU-side `0x07` mapping.
- If implementing an Ironmon/NatDex-close v1, keep `VAR_GAME_DIFFICULTY` Normal and add only trainer `GetAIFlags` behavior equivalent to `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`.
- Do not include `AI_SCRIPT_ROAMING`, `AI_SCRIPT_SAFARI`, `AI_SCRIPT_FIRST_BATTLE`, wild/raid smart paths, shift-switch prediction, Expert anti-cheese, trainer IV/EV/friendship/PP buffs, level scaling, player restrictions or battle-rule changes in v1.
- If choosing the more conservative CFRU-native path, document clearly that `AI_SCRIPT_SEMI_SMART` alone is intentionally weaker than the NatDex/Ironmon `0x07` model.
- Before implementation, confirm whether the branch should import or wait for the separate `ironmon-smart-ai-patch-map.md` documentation PR, because that file is not currently present on this feature branch.

# Next steps update - Ironmon / NatDex Smart AI patch map

- Treat `01_docs/analysis/ironmon-smart-ai-patch-map.md` as the current source-backed comparison reference for Ironmon/Super-Kaizo/NatDex Smart AI.
- Baseline conclusion: do not use CFRU `VAR_GAME_DIFFICULTY` as a Smart-AI proxy. The NatDex/Ironmon source-backed behavior is trainer-AI-flag focused, while CFRU Difficulty also changes trainer strength, level scaling, player restrictions, wild/raid behavior and battle rules.
- If implementing CFRU Smart Trainer AI, decide whether v1 is conservative (`AI_SCRIPT_SEMI_SMART` only) or closer to the NatDex/Ironmon `0x07` model by setting the nearest CFRU equivalents of Bad-Move, Semi-Smart/Viability and Good-Move/Try-to-Faint behavior.
- Keep wild AI, Expert anti-cheese, trainer build strength, bag restrictions, move restrictions and battle-rule changes out of the baseline Smart Trainer AI option unless separately requested.
- Do not download, apply or commit ROM patches or randomizer release zips. Continue excluding ROMs, output ROMs, saves, emulator states, builds, tool binaries, private paths, hashes, full logs, secrets, tokens and `.env` data.

# Next steps update - CFRU Smart AI source-port map

- Treat `01_docs/analysis/cfru-smart-ai-source-port-map.md` as the current source-backed map for a future Smart Trainer AI only source-port.
- Preferred design: keep `VAR_GAME_DIFFICULTY` Normal for the Randomizer/Ironmon baseline and introduce a separate trainer-AI option, preferably `VAR_TRAINER_AI_MODE` if future tiers are likely.
- Minimal future implementation should start in `GetAIFlags`: for trainer battles, add `AI_SCRIPT_SEMI_SMART` when the new trainer-AI option is enabled and `AI_SCRIPT_CHECK_GOOD_MOVE` is absent.
- Keep wild AI separate. Do not reuse CFRU `FLAG_SMART_WILD` as the global trainer toggle because it is an existing one-time wild state cleared after battle.
- Do not include Expert anti-cheese, switch prediction, shift-switch behavior, raid behavior or wild special cases in the baseline without a separate design decision and targeted tests.
- Future tests must prove trainer IVs, EVs, friendship, PP, levels, player bag access, player move access, battle rules, wild construction and raid behavior remain Normal-equivalent.
- Keep the known dirty CFRU `src/config.h` state out of commits. Do not stage or modify `02_external/**`.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - CFRU Smart AI only design

- Treat `01_docs/analysis/cfru-smart-ai-only-design.md` as the current source-backed policy note for Smart AI only vs CFRU runtime difficulty.
- Baseline recommendation: do not expose `VAR_GAME_DIFFICULTY` as a Smart-AI randomizer option. Keep runtime difficulty Normal unless a user explicitly chooses a Hard-mode profile.
- If Smart AI only becomes implementation work, keep trainer AI and wild AI separate. Start with `GetAIFlags` for trainer move-choice behavior, then decide separately on `ShouldDoAIShiftSwitch`, switch prediction, Expert anti-cheese, `WILD_ALWAYS_SMART`, and `FLAG_SMART_WILD`.
- Future code work must prove it does not change trainer IVs, EVs, friendship, PP, level scaling, bag restrictions, move restrictions, battle rules, wild encounter builds, or raid behavior unless those are explicitly requested.
- Keep the known dirty CFRU `src/config.h` state out of commits. Do not stage or modify `02_external/**`.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - CFRU game difficulty map

- Treat `01_docs/analysis/cfru-game-difficulty-map.md` as the current source-backed reference for CFRU `VAR_GAME_DIFFICULTY 0x5157`.
- Keep the distinction explicit: Hard/Expert overlap with Smart AI but are broader because they also change trainer-mon construction, level scaling, player restrictions, wild/raid behavior, and selected battle rules/calculations.
- Do not describe `VAR_GAME_DIFFICULTY` as a pure Smart-AI runtime switch.
- If a pure Smart-AI-only Ironmon-style mode is needed, analyze or implement it separately; the requested source search did not find a pure runtime switch for only Smart AI.
- Keep local dirty CFRU `src/config.h` edits out of commits. `FLAT_EXP_FORMULA` being locally enabled is balance-relevant but not directly `VAR_GAME_DIFFICULTY`-specific.
- Useful follow-up: fold `WILD_ALWAYS_SMART`, `FLAG_SMART_WILD`, `TRAINERS_WITH_EVS`, `SCALED_TRAINERS`, and local config overlays into the broader CFRU runtime/config option map without changing CFRU/DPE source.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - Rival starter consistency smoke plan

- Treat `08_tests/randomizer/rival_starter_consistency_smoke.md` as the current documentation-only plan for a focused local Rival starter consistency smoke.
- Existing evidence is enough to run the smoke without inventing a new evidence structure: Oak-Lab Rival counter-slot evidence comes from `192`, Rival carry/counter evidence from `207`, combined Oak-Lab plus Route 22 evidence from `208`, Oak-Lab independence from `212`, and runtime-source/Trainer Pokemon caveats from `202` through `204` plus the TSV and decision matrix.
- Recommended local settings: randomized Starter Pokemon, randomized Foe/Trainer Pokemon, `Rival Carries Starter Through Game` enabled, Trainer Class Sprite Sync enabled only when Trainer Class Names are randomized, Special-Wild/Day-Night/Swarms off, and unrelated Item/Palette/Misc/TypeEffectiveness variants excluded unless already part of a stable visual profile.
- PASS remains caveated: Oak-Lab Rival and Route 22 Rival starter must match the expected counter-starter for the sampled player starter, non-starter Rival Pokemon must be interpreted separately, and evidence must stay sanitized.
- Keep follow-up scope explicit: all-starter-choice matrix, later Rival appearances, broader runtime-source rows and full playthrough are separate optional local work.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No P1 promotion follows from this plan.

# Next steps update - FVX compatibility implementation report

- Treat `01_docs/randomizer/fvx-compat-implementation-report.md` as the current technical summary of how the UPR-FVX CFRU/DPE compatibility fix stack was implemented through compat commit `8349daf5ce005f0defc5674cbc3a3468f009218c` / PR #152.
- Use the report for future review/handoff before opening new FVX compatibility work, especially when deciding whether a topic is code-supported, audit-supported, targeted-smoke-supported or still caveated.
- Keep the report boundaries explicit: no new ROM run, no build, no output artifact, no full-playthrough claim, no broad Type-Matchup/Palette/Held-Item distribution proof and no P1 promotion.
- Recommended next work remains evidence-driven: only revisit Gen Limit / Special Forms / Mechanic Items / Trainer Held Items / Intro / Rival / Runtime Trainer / Palette / Misc / TypeEffectiveness when a regression, full-playthrough question or a separately scoped audit/smoke is requested.
- Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data from committed documentation.

# Next steps update - Gen Limit / Special Form / Mechanic Item final smoke

- Treat UPR-FVX compat commit `8349daf5ce005f0defc5674cbc3a3468f009218c` as the current workspace pin for the merged Gen-Limit, Special-Form, Trainer-Class-Sprite-Sync, Oak-Lab-Rival, Mechanic-Item and Trainer-Held-Item fix chain through PR #152.
- Treat `08_tests/randomizer/212_gen_limit_special_form_item_smoke.md` as the current sanitized evidence file for Gen Limit / Special Form / Mechanic Item Exclusions and Trainer Held Items / Sensible Items NPE-free final smoke.
- Status is `PASS_TARGETED_LOG_VISUAL_SMOKE_WITH_CAVEATS`.
- Confirmed locally in sanitized evidence: Gen-Limit 1-9 infrastructure works; Gen1-only and Gen1-6 log smokes looked correct; Gen7/8/9 Intro Mon no longer crashes and supports valid visual-table candidates; Mega/GMax/Regional/Irregular/Special-form filtering works in latest checks; Regional forms are not pulled in by Evolutionary Relatives unless Regional Forms across Gen Limit is enabled.
- Also confirmed locally: Trainer Class Sprite Sync is GUI-exposed and should be enabled when Trainer Class Names are randomized; Oak-Lab Rival counter-starter is preserved independently of Rival Carries Starter Through Game; mechanic item filtering uses source-backed CFRU/DPE categories for Mega/Z/Dynamax-GMax items; Trainer Held Items / Sensible Items run without the earlier missing-pool or missing-movepool NPEs; no current crash was observed in the latest GUI smoke.
- Keep caveats explicit: targeted local smoke only, no full playthrough; no full held-item distribution audit; Plates/Drives/Memories/Nectars have no separate user-facing policies yet; Static Script/Gift/NPC item sources remain caveated if outside randomizer item replacement pools; custom/future form encodings outside documented CFRU/DPE identity blocks remain audit-required.
- Do not promote this status to P1. Do not run ROMs through Codex. Continue excluding output ROMs, private paths, ROM hashes, full logs, screenshots, saves, emulator states, secrets, tokens and `.env` data.

# Next steps update - Misc Tweaks behavior smoke

- Treat UPR-FVX PR #125, PR #126 and PR #127 as synced into the workspace pin at `155fac0b33474f6ed5b3fbaed7dd9bf24b4e1315`.
- Treat `08_tests/randomizer/210_misc_tweaks_behavior_smoke.md` as the current sanitized evidence file for Misc Tweaks behavior smoke.
- Misc Tweaks status is `PASS_TARGETED_BEHAVIOR_SMOKE_WITH_CAVEATS`.
- Confirmed locally in sanitized evidence: Fastest Text pass, Randomize PC Potion pass, Run Without Running Shoes pass, Running Shoes Indoors pass, Randomize Catching Tutorial pass without question-mark sprite/name, Fast Egg Hatching crash-free randomization with output load, and no crash/freeze in tested paths.
- Keep caveats explicit: Fast Egg Hatching has no full hatch-cycle proof; Ban Lucky Egg is likely pass / no issue observed rather than dedicated proof; Reusable TMs and Forgettable HMs are CFRU-provided and should not be duplicated by the UPR-FVX stable profile.
- Do not promote Misc Tweaks to P1 from this targeted smoke.
- Do not run ROMs through Codex. Continue excluding output ROMs, private paths, ROM hashes, full logs, screenshots, saves, emulator states, secrets, tokens and `.env` data.

# Next steps update - Type Effectiveness battle smoke

- Treat `08_tests/randomizer/211_type_effectiveness_battle_smoke.md` as the current sanitized evidence file for Type Effectiveness battle smoke.
- Type Effectiveness status is `PASS_TARGETED_BATTLE_SMOKE_WITH_CAVEATS`.
- Confirmed locally in sanitized evidence: Type Effectiveness was tested in battle, effectiveness behavior looked appropriate and no battle crashes were reported.
- Keep caveats explicit: no full type-chart matchup matrix, targeted battle smoke only, no full playthrough and no P1 promotion.
- Do not run ROMs through Codex. Continue excluding output ROMs, private paths, ROM hashes, full logs, screenshots, saves, emulator states, secrets, tokens and `.env` data.

# Next steps update - Graphics/Palettes visual smoke

- Treat UPR-FVX PR #124 as synced into the workspace pin at `0eb815418470fa1ac000695b95d09cb084338dca`; this includes PR #123 palette output writes and PR #124 expanded trainer logging fallback.
- Treat `08_tests/randomizer/209_graphics_palettes_visual_smoke.md` as the current sanitized evidence file for Graphics/Palettes visual smoke.
- Graphics/Palettes visual/audit smoke is locally passed with caveats: `Pokemon Palettes: Randomized/Changed`, `normalPaletteWriteAttempts=841`, `sampledCount=21`, `normalChangedCount=21`, `shinyChangedCount=0`, `unchangedCount=0`, sampled normal palettes changed from base and changed palettes were visually observed.
- The final run had no `Error during logging`.
- Keep the caveat explicit: targeted visual/audit smoke only, not a full playthrough, broad species/form sweep, shiny behavior proof or P1 promotion.
- Useful follow-up, if needed, is a separate local shiny-focused palette audit/visual smoke and broader species sampling, still with sanitized evidence only.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - Graphics/Palettes smoke settings prep

- A local ignored manual smoke input is prepared at `05_builds/randomizer-smoke/settings/manual/graphics_palettes_smoke.rnqs`.
- The input is copied from the existing generated `risk_graphics_palettes_visual` settings profile and should be treated as Graphics/Palettes-only.
- Feature scope: `FVX-GFX-001` Pokemon Palettes Random, `FVX-GFX-002` Palettes Follow Types, `FVX-GFX-003` Palettes Follow Evolutions and `FVX-GFX-004` Palettes Shiny From Normal.
- Do not mix this smoke with Wild, Foe, Items, Misc, TypeEffectiveness/type chaos, Custom Player Graphics or Character-to-Replace.
- Next local work, if explicitly run outside Codex, is a targeted visual palette smoke with sanitized observations only.
- Do not update evidence or promote P1 until a local ingame smoke actually exists.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - Wild encounter output audit sync

- Treat UPR-FVX PR #118 as synced into the workspace pin at `ed692d07bfc81405706f2b94fda06639426e6a75`.
- Wild Encounter Base-vs-Output Audit is available as an opt-in diagnostic for Gen3/FRLG/CFRU-DPE.
- Keep the scope explicit: diagnostic-only, no writer/randomizer behavior change and no P1 promotion.
- The audit covers the modeled Gen3 base `WildPokemon` table path and reports per-slot base-vs-output species deltas plus total/changed/unchanged/changed percentage.
- If local ingame wild encounters still appear vanilla while the randomizer log says changed, use the private local audit output to compare modeled Base/Output slots and share only sanitized summaries.
- CFRU/DPE special/runtime wild sources remain the follow-up if the modeled-table audit and ingame behavior diverge.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - Combined trainer visual runtime smoke

- Treat `08_tests/randomizer/208_combined_trainer_visual_runtime_smoke.md` as the current sanitized evidence file for the combined trainer visual runtime smoke.
- Combined trainer visual runtime smoke is `PASS_WITH_CAVEATS`.
- Confirmed locally in sanitized evidence: Intro Mon visibly randomized; Player Charmander -> Oak-Lab Rival Squirtle and Route-22 Rival Squirtle; Route 22 Rival sprite consistent with the Oak-Lab Rival sprite; Viridian Forest trainer sprites randomized; no crash/freeze/garbled sprite observed.
- Route 22 Rival non-starter Pokemon observed: Silvally Lv9. Interpretation: Rival Carries Starter Through Game protects/corrects the Rival starter slot only; non-starter Rival Pokemon remain eligible for Foe Pokemon randomization.
- Useful follow-up, if needed, is broader local sampling across additional player-starter choices and later Rival appearances, still with sanitized evidence only.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No P1 promotion follows from this smoke.

# Next steps update - Rival counter starter and combined visual smoke

- Treat UPR-FVX PR #117 as synced into the workspace pin at `5983011752273e00c402e25cc1ae1a9baca110f1`.
- Treat `08_tests/randomizer/207_rival_counter_starter_and_combined_visual_smoke.md` as the current sanitized evidence file for Rival Carries Starter Through Game plus the combined visual smoke.
- Rival Carries Starter Through Game is locally smoke-confirmed for the sampled counter path: Player Charmander -> Rival Squirtle.
- Intro Mon Species `0` regression is fixed in the sampled combined profile; visible Intro Mon was Blissey.
- Trainer Class Sprite Sync remains visually okay from prior checks: Viridian Forest trainers get per-trainer randomized classes/sprites and Rival keeps a consistent class/sprite across appearances.
- Caveat: targeted visual smoke only, not a full playthrough, all-starter-choice matrix, global runtime-source proof or P1 promotion.
- Useful follow-up, if needed, is broader local sampling across all starter choices and later Rival appearances, still with sanitized evidence only.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No P1 promotion follows from this sync.

# Next steps update - Trainer Class Sprite Sync final smoke

- Treat UPR-FVX PR #116 as synced into the workspace pin at `36dd431d059bc69eb1bee3311200e28c872c6cc9`.
- Treat `08_tests/randomizer/206_trainer_class_sprite_sync.md` as the current sanitized evidence file for Trainer Class Sprite Sync.
- `MODE-TRAINER-CLASS-SPRITE-SYNC` is locally smoke-confirmed for targeted visual consistency.
- Keep the semantics explicit: `Randomize Trainer Names` only changes trainer personal names; `Randomize Trainer Class Names` remains legacy/textlabel-only unless Sprite Sync is also enabled; with Sprite Sync enabled, class label, `trainerClass` and visible `trainerPic` follow the class assignment.
- Regular trainers use per-trainer class/sprite assignments. Rival/Friend rows use grouped class/sprite consistency. Runtime-source rows are included where eligible.
- Caveat: targeted visual smoke only, not a full playthrough, route sweep or global visual-source proof.
- Recommended next work should not be another semantic correction unless new evidence contradicts the final model. Broader follow-up should sample more trainer categories, eligible runtime-source rows and longer playthrough paths, still with sanitized evidence only.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No P1 promotion follows from this sync.

# Next steps update - Trainer Class Sprite Sync

- Treat UPR-FVX PR #111 as synced into the workspace pin at `4805a5a930bc97203199816222465c76de2f2150`.
- Treat `08_tests/randomizer/206_trainer_class_sprite_sync.md` as the current sanitized handoff for Trainer Class Sprite Sync.
- `MODE-TRAINER-CLASS-SPRITE-SYNC` is available as an opt-in mode.
- Keep the semantics explicit: `Randomize Trainer Names` only changes trainer personal names; `Randomize Trainer Class Names` remains legacy/textlabel-only unless Sprite Sync is also enabled; with Sprite Sync enabled, `trainerClass` and visible `trainerPic` follow the Trainer Class Names target class mapping.
- Do not describe the feature as Regular-only. The target is class label / classId / pic consistency; special target classes are allowed when the class-name mapping selects them and a valid target pic is observed.
- Final local smoke is still needed on the merged pin. Sanitized evidence should include whether the battle started, the visible sprite label in words, the class/sprite sync marker values, and whether the displayed class label matches the visible sprite class.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No P1 promotion follows from this sync.

# Next steps update - Intro Mon visual source fix smoke

- Treat UPR-FVX PR #109 as synced into the workspace pin at `a9bb4a5f201c5078ec02fe1f2f8417695448afe9`.
- Treat `08_tests/randomizer/205_intro_mon_visual_source_fix_smoke.md` as the sanitized local evidence for the Intro Mon visual-source fix.
- `FVX-GEN-003` / Intro Mon visual mismatch is locally fixed for the targeted CFRU/DPE Gen9 BPRE smoke: the visible Oak intro sprite changed away from Nidoran female, with no crash, freeze or garbled sprite observed.
- Keep the caveat explicit: this was targeted ingame smoke, not a full playthrough and not a global visual-source proof.
- Do not promote P1 unless explicitly approved later.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - Intro Mon visual source diagnostics sync

- Treat UPR-FVX PR #107 as synced into the workspace pin at `a7e098a5158d824b1ddec62a286f2a6ffafce8e4`.
- Intro Mon Visual-Source-Diagnose is now available for local opt-in checks of known FRLG Intro Mon literals/pointers and optional Base-ROM vs randomized Output-ROM comparison.
- Keep the semantics explicit: `No Random Intro Mon` is a negative GUI option; `randomizeIntroMon=true` is the active Randomize Intro Mon path; `MODE-INTRO-RANDOM` sets true; `MODE-NO-RANDOM-INTRO` and `FVX-GEN-003` set false.
- This is diagnosis-only. It does not fix the visible Intro Mon mismatch, does not prove ingame visuals and does not promote P1.
- Next local evidence should compare private Base/Output ROMs with the opt-in report and share only sanitized source names, hex offsets, raw/decoded species, `changedFromBase=yes/no` and observed visible Intro Mon label.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - Runtime source trainer randomization smoke evidence refresh

- Treat UPR-FVX PR #105 runtime-source randomization evidence as documented while the workspace remains pinned to PR #106 commit `5bb1d853f132095922be2aceef55af2878192b85` or later.
- Treat `08_tests/randomizer/204_runtime_source_trainer_randomization_smoke.md` as the latest sanitized local evidence for strict runtime-source sync plus `RUNTIME-SOURCE` Trainer Pokemon randomization.
- Viridian Forest trainer IDs `531/532` are audit-confirmed and ingame-confirmed in the targeted local smoke: loaded/raw parties match, and the formerly vanilla Viridian Forest trainer now shows Eiscue.
- The randomized output audit reported `trainer runtime source audit mode=unloaded-valid-parties` with `total=0`, equivalent to no remaining valid runtime-not-loaded rows in that focused audit view.
- Rival 2 trainer IDs `329/330/331` and Brock trainer ID `414` also have sanitized local randomized-party observations.
- Keep broader Trainer/Foe caveats: loaded-mismatch, invalid-pointer, empty-party, out-of-range rows and full playthrough coverage remain follow-up scope.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No P1 promotion follows from this smoke.

# Next steps update - Runtime trainer post-randomization audit sync

- Treat UPR-FVX PR #106 as synced into the workspace pin at `5bb1d853f132095922be2aceef55af2878192b85`.
- Pre/Post Runtime-Trainer-Audit is now available as an opt-in local diagnostic for comparing a private Base-ROM with a private randomized Output-ROM.
- Use the audit to review valid script-referenced runtime trainer rows, changed-from-base status, loaded/raw output comparison and warning markers.
- Keep this as audit-only: PR #106 adds no new writer, auto-sync or randomizer behavior.
- Local users should run the two-ROM comparison themselves and share only sanitized trainer IDs, party summaries, classifications, warning markers and pass/fail observations.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No P1 promotion follows from this sync.

# Next steps update - Runtime source trainer randomization smoke

- Treat UPR-FVX PR #105 as synced into the workspace pin at `c0d8e33f3547020c6fd2fe5baffbc80ec93f9197`.
- Treat `08_tests/randomizer/203_runtime_source_trainer_randomization_smoke.md` as sanitized local evidence for Viridian Forest runtime-source trainer IDs `531/532`.
- Trainer/Foe runtime-source strict sync plus randomizer eligibility is locally confirmed for this targeted case: audit loaded/raw parties match and the observed Viridian Forest battle now shows randomized Eiscue instead of vanilla Metapod/Caterpie.
- Keep broader Trainer/Foe caveats: loaded-mismatch, invalid-pointer, empty-party and out-of-range rows remain follow-up scope, and additional suspected runtime-source battles need separate sanitized evidence.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No P1 promotion follows from this smoke.

# Next steps update - Strict runtime trainer source sync

- Treat UPR-FVX PR #104 as synced into the workspace pin at `6dcda7e499cd3e22319c447c7d7df9ddbd67de60`.
- Strict Runtime Trainer Source Sync is now available for audit candidates classified as `VALID_RUNTIME_NOT_LOADED`.
- Keep Trainer/Foe as CLI-log-clean but not P1-promoted: local private-ROM audit plus ingame smoke is still required.
- For Viridian Forest trainer IDs `531/532`, confirm locally that they still appear as `VALID_RUNTIME_NOT_LOADED`; if so, they should be covered by strict sync.
- Keep `loaded-mismatch`, `invalid`, empty-party and out-of-range audit rows as diagnosis/follow-up scope, not synced coverage.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No P1 promotion follows from this sync.

# Next steps update - Runtime trainer source audit sync

- Treat UPR-FVX PR #103 as synced into the workspace pin at `14c1c8c0c6960f1b4a0cf0246a1117628ca1f3cc`.
- Runtime Trainer Source Audit is now available through `uprfvx.trainerRuntimeSourceAudit` / `UPRFVX_TRAINER_RUNTIME_SOURCE_AUDIT`.
- Use `unloaded-valid-parties` first when looking for likely in-game trainer rows that are script-referenced, have valid raw parties and are not present in the normal loaded trainer model.
- Use `loaded-mismatch` for loaded trainer rows whose raw runtime party differs from the loaded model, and `invalid` to inspect out-of-range, invalid-pointer, empty-party or likely false-positive candidates.
- Keep this as diagnosis only: no auto-sync, no SaveTrainers expansion and no broader writer change follows from PR #103.
- Additional runtime-source fixes for trainer battles beyond the already synced Rival 2/Brock fix require sanitized local audit evidence first.
- Do not run ROMs through Codex. Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No P1 promotion follows from this sync.

# Next steps update - Runtime trainer party fix sync

- Treat UPR-FVX PR #102 as synced into the workspace pin at `eabbcd7eccb1703f98000f85669d969f516e1247`.
- Rival 2 trainer IDs `329/330/331` and Brock trainer ID `414` now have a merged UPR-FVX fix that loads and saves validated raw FRLG `trainerbattle` runtime-source `TrainerData` rows outside the normal loaded trainer count.
- Keep Foe Trainer as CLI-log-clean but not P1-promoted: local ingame smoke is still needed to confirm Rival 2, Brock and broader trainer play use randomized runtime parties as expected.
- For any additional vanilla-looking trainer, first collect targeted redacted runtime-source evidence before expanding the sync target list.
- Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data. No ROM runs by Codex and no P1 promotion follow from this sync.

# Next steps update - Trainer runtime source diagnostics sync

- Treat UPR-FVX PR #100 as synced into the workspace pin at `87bba797620dd2043f02c11c67f7b752a7238a00`.
- Use `08_tests/randomizer/202_trainer_runtime_source_diagnostics_sync.md` as the workspace handoff for the Trainer runtime-source diagnosis.
- Keep Foe Trainer as CLI-log-clean but ingame partial/caveated until local sanitized evidence proves the affected battles use the same `TrainerData` rows and party pointers that UPR-FVX logs and writes.
- Prioritize local opt-in evidence for second Rival, Brock and selected normal trainers: affected battle label, trainer ID if visible, observed party summary if known, and redacted runtime-source diagnostic rows.
- If runtime-source rows differ from the logged trainer IDs, plan a focused UPR-FVX follow-up for script-ID mapping or raw/source sync before any stronger Foe Trainer support claim.
- No ROM runs by Codex, output ROMs, private paths, hashes, full logs, screenshots, saves, emulator states, secrets, tokens, `.env` data or P1 promotion follow from this sync.

# Next steps update - Settings profile variant overlays sync

- Treat UPR-FVX PR #99 as synced into the workspace pin at `4c8e7394a230e6e8471977036be268c80883ac0b`.
- Use `08_tests/randomizer/cli_profile_matrix.coverage.example.tsv` to enable exact Foe mode, Wild location, TypeEffectiveness and Intro random/no-random rows for local generated settings runs when needed.
- `feature_overlays` may now contain Feature IDs or exact `MODE-*` overlay IDs; keep generated `.rnqs` files and real matrix outputs under ignored local directories.
- Keep `MODE-GEN-LIMIT-1-9*` rows disabled/unsupported until Settings can encode Gen 8/9 restrictions and GMax exclusion.
- No ROM runs, output ROMs, private paths, hashes, full logs, screenshots, saves, emulator states, secrets, tokens, `.env` data or P1 promotion follow from this sync.

# Next steps update - Exact coverage batches 03-18

- Treat `08_tests/randomizer/201_exact_coverage_batches_03_18.md` as sanitized CLI log/helper evidence for exact-coverage Batches 03 through 18 only.
- Batch 03 through 17 processed 165 generator-capable exact/cumulative/mode profiles with dry-run disabled, 0 bad markers and 0 warnings for all PASS profiles; Batch 18 confirmed 4 Gen-Limit `MODE-*` overlays fail as expected because they are unsupported by current Settings format.
- Covered rows now have Batch 03-18 log-pass evidence but still need local boot/play, visual smoke, behavior-specific ingame/manual smoke or feature-specific ingame smoke before any stronger support claim.
- Keep caveats visible: Graphics/Palettes need visual smoke, sensible Trainer Held Items remains caveated due previous NPE history, Intro Mon needs visual confirmation, Special-Wild remains separate, Gen-Limit-1-9 `MODE-*` overlays remain unsupported by Settings format, static null placeholders remain null, Custom Starters and Custom Player Graphics remain manual/unsupported, and Update Moves remains out-of-scope for CFRU/DPE Gen9.
- No P1 promotion follows from these batches.
- Continue excluding ROM paths, hashes, full logs, output paths, screenshots, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - Exact coverage batch 02 items

- Treat `08_tests/randomizer/200_exact_coverage_batch_02_items.md` as sanitized CLI log evidence for exact-coverage Batch 02 Items only.
- Batch 02 processed 13 exact Item single/variant profiles with dry-run disabled, 0 bad markers and 0 warnings.
- `FVX-ITEM-001` through `FVX-ITEM-010` now have Batch 02 log-pass evidence but still need local boot/play or item-specific ingame smoke before any stronger support claim.
- Keep the Required-TM forcing and supported/special shop caveats visible; this batch does not change item writer/reload or gameplay evidence.
- No P1 promotion follows from this batch.
- Continue excluding ROM paths, hashes, full logs, output paths, screenshots, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - Exact coverage batch 01

- Treat `08_tests/randomizer/199_exact_coverage_batch_01.md` as sanitized CLI log evidence for exact-coverage Batch 01 only.
- Batch 01 processed 19 exact single/variant profiles with dry-run disabled, 0 bad markers and 0 warnings.
- The updated Feature IDs now have log-pass evidence from Batch 01 but still need local boot/play or feature-specific ingame smoke before any stronger support claim.
- Keep `FVX-SST-010` and `FVX-SST-012` static null-placeholder caveats visible; this batch does not change static placeholder semantics.
- No P1 promotion follows from this batch.
- Continue excluding ROM paths, hashes, full logs, output paths, screenshots, saves, emulator states, private paths, secrets, tokens and `.env` data.

# Next steps update - Coverage CLI profile matrix pass

- Treat `08_tests/randomizer/198_cli_profile_matrix_coverage_run.md` as sanitized CLI log evidence for the coverage-generated profile matrix only.
- The coverage `.rnqs` matrix processed 14 profiles with 0 bad markers and 0 warnings.
- Keep all updated TSV rows below P1: log-pass evidence is not ingame evidence, writer/reload proof or full-playthrough evidence.
- Only rows exactly enabled by the executed coverage profile overlays should cite the 198 evidence.
- Unexpected-pass profiles still need focused follow-up before de-caveating: `04_foe_held_items_sensible_expected_fail`, `09_graphics_palettes`, `10_misc_tweaks` and `11_special_wild`.
- Continue using `fvx_profile_coverage_plan.md` to identify variants that were not actually covered by the 14-profile run.
- No ROM paths, hashes, full logs, output paths, screenshots, saves, emulator states, private paths, secrets, tokens or `.env` data should be documented. No P1 promotion follows from this matrix run.

# Next steps update - FVX profile coverage audit

- Use `08_tests/randomizer/fvx_profile_coverage_plan.md` as the profile coverage source of truth for mapping all 130 Feature IDs to single, variant, tab, cumulative and risk-interaction profile IDs.
- Use `08_tests/randomizer/cli_profile_matrix.coverage.example.tsv` for opt-in fine-grained profile generation. The broad rows remain enabled; single/variant/risk rows are disabled until the user chooses a focused run.
- When generating targeted profiles, pass the coverage manifest through `generate_settings_profiles_from_matrix.sh`; rows with `feature_overlays` call UPR-FVX `settings-profile --enable` directly.
- Do not count related broad profiles as exact feature coverage when the coverage plan says `current_14_profile_includes_feature=no`.
- Priority follow-ups: `FVX-TRAIT-017`, Starter/Static variants, Foe Additional/Type/Battle/Rival-Carry variants, Field/Shop item variants, exact TypeEffectiveness modes, Graphics/Palettes visual smoke and Misc behavior smokes.
- Superseded by UPR-FVX PR #99: TypeEffectiveness Random, Random-Balanced, Keep-Identities and Inverse can now be auto-generated from this workspace manifest through `MODE-TYPE-*` overlays.
- No ROM runs, output ROMs, private paths, hashes, full logs or P1 promotion follow from this audit.

# Next steps update - Generated CLI profile matrix results

- Treat `08_tests/randomizer/197_cli_profile_matrix_generated_run.md` as sanitized CLI log evidence for the generated profile matrix only.
- The generated `.rnqs` matrix processed 14 profiles with 0 bad markers and 0 warnings.
- Keep all updated TSV rows below P1: log-pass evidence is not ingame evidence, writer/reload proof or full-playthrough evidence.
- Unexpected-pass profiles need focused follow-up before de-caveating: `04_foe_held_items_sensible_expected_fail`, `09_graphics_palettes`, `10_misc_tweaks` and `11_special_wild`.
- Recommended next block: isolate one unexpected-pass profile at a time, starting with Trainer Held Items Sensible or Graphics/Palettes visual smoke.
- Special-Wild/Day-Night/Swarms remain a separate scope despite the clean CLI profile log smoke.
- Continue excluding ROM paths, hashes, full logs, output paths, screenshots, saves, emulator states, private paths, secrets, tokens and `.env` data.
- No P1 promotion follows from this matrix run.

# Next steps update - Settings profile generator sync

- Treat UPR-FVX PR #98 as synced into the workspace pin at `81fa4cf35af48bce19996e4581f1e4a688ebfa3b`.
- Use `07_scripts/randomizer/generate_settings_profiles_from_matrix.sh` to derive `.rnqs` profile settings from one local base `.rnqs` and `08_tests/randomizer/cli_profile_matrix.example.tsv`.
- Build the pinned UPR-FVX jar first, then run the generator with `--upr-dir 02_external/upr-fvx --base-settings <local-base-settings.rnqs> --profile-manifest <profiles.tsv> --output-settings-dir <ignored-local-settings-dir>`.
- Keep generated settings, real CLI smoke outputs and raw logs under ignored local directories.
- Continue using `run_cli_profile_matrix.sh` for actual local private-ROM matrix runs after settings are generated.
- Codex may use only help/dry-run/artificial fixtures. Real ROM smokes remain user-local.
- Do not document ROM paths, hashes, full logs, screenshots, output ROM paths, saves, emulator states, private paths, secrets, tokens or `.env` data.
- No P1 promotion follows from this tooling sync.

# Next steps update - FVX feature test status matrix

- Use `08_tests/randomizer/fvx_feature_test_status_matrix.tsv` as the machine-readable worklist for future CLI profile matrix runs.
- Keep `01_docs/randomizer/fvx-progress-dashboard.md` as the human overview and do not shorten its full feature list.
- When a local CLI matrix run reports sanitized results, update only the affected TSV rows: `log_status`, `ingame_status`, `known_caveat`, `blocker`, `evidence` and `next_step`.
- Move a row to `PASS_INGAME_SMOKE` only after sanitized local ingame evidence exists for that feature path.
- Keep Special-Wild out-of-scope, Trainer Class Names textlabel-only and trainer held Sensible Items expected-fail; Graphics/Palettes and Misc Tweaks have since moved to targeted smoke statuses with caveats, and future row changes should stay evidence-scoped.
- Continue excluding ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data.
- No P1 promotion follows from the matrix alone.

# Next steps update - CLI profile matrix pipeline

- Use `08_tests/randomizer/194_cli_profile_matrix_pipeline.md` for multi-profile CLI smoke orchestration.
- Keep the current implementation on saved local `.rnqs` profiles listed in a TSV manifest. Do not byte-patch settings files from shell/Python.
- To scaffold a local manifest, run `07_scripts/randomizer/generate_cli_smoke_profiles.sh --output 05_builds/randomizer-smoke/cli-profile-matrix/profiles.tsv`.
- To validate wiring without ROM access, run `07_scripts/randomizer/run_cli_profile_matrix.sh --profile-manifest 08_tests/randomizer/cli_profile_matrix.example.tsv --output-dir /tmp/upr-fvx-cli-profile-matrix --summary-report /tmp/upr-fvx-cli-profile-matrix/summary.md --dry-run`.
- Target state: add a future UPR-FVX CLI/helper subcommand or Java helper that derives profile settings through FVX `Settings` APIs, then let the manifest activate feature blocks automatically.
- Real matrix runs remain local-only with private ROM/settings/output/log paths under ignored directories. Report back only sanitized aggregate evidence.
- Keep Trainer Class Names, Special-Wild and `Rival Carries Starter Through Game` caveated/separate unless a profile explicitly tests them. Do not promote P1 from this pipeline.

# Next steps update - CLI log smoke pipeline

- Use `08_tests/randomizer/193_cli_log_smoke_pipeline.md` for the local-only CLI counterpart to the GUI smoke.
- Build the pinned UPR-FVX jar locally if needed, then run `07_scripts/randomizer/cli_log_smoke_pipeline.sh` with a private ROM, local settings file and ignored `05_builds/randomizer-smoke/` output/report paths.
- Prefer a settings file over `--settings-string` for local runs so shell history does not capture the settings string.
- Treat the generated sanitized report as smoke evidence only: CLI exit code, success marker, output/log creation and marker counts.
- Keep Trainer Class Names disabled for stable visual sampling unless textlabel-only remapping is intentionally being tested.
- Keep Special-Wild/Day-Night/Swarms out-of-scope and keep `Rival Carries Starter Through Game` separate until explicitly smoked.
- Do not promote any new P1 status from the CLI pipeline; continue reporting sanitized yes/no evidence only, without ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens or `.env` data.

# Next steps update - Starter/Rival sync pass

- Treat UPR-FVX PR #97 as synced into the workspace pin at `51d52a03235664154549105003dadfb45c76d0d0`.
- Treat Starter Pokemon as locally smoke-passed for the Oak-Lab first Rival counter-slot path.
- Root cause: the Oak-Lab Rival runtime source is raw `TrainerData` party rows outside the normal loaded trainer model. The corrected candidate mapping is `[328, 326, 327]`.
- Sanitized local evidence: starter slots Groudon, Fearow and Mudbray; player chose Groudon; expected Rival Fearow; observed Rival Fearow.
- Stable Visual Profile can now optionally include Starter Pokemon in local sampling.
- Keep `Rival Carries Starter Through Game` separate until the full-rival-through-game path has its own evidence.
- Keep Trainer Class Names off for visual consistency unless textlabel-only remapping is intentional.
- Keep Special-Wild/Day-Night/Swarms out-of-scope for the stable profile.
- Recommended next block: run a Stable Visual Profile + Starter Pokemon local smoke with Trainer Class Names and Special-Wild still disabled, or isolate `Rival Carries Starter Through Game` as a separate path.
- Do not promote any new P1 status from this sync; continue reporting sanitized yes/no evidence only, without ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens or `.env` data.

# Next steps update - Stable Visual Profile smoke

- Treat the Stable Visual Profile as locally smoke-passed on sanitized evidence after the merged GUI Working Settings Matrix baseline.
- Keep Stable Visual Profile ON: Wild Standard/Fallback, Trainer Pokemon core, Pokemon Movesets -> Random completely, Trainer Movesets, Trainer Names, Field Items basic, Pokemon Abilities, TM/HM Compatibility, TM Moves, Move Tutor Moves, Move Tutor Compatibility, Shop Items, Pickup Items, In-Game Trades, Static Pokemon, Type Effectiveness, Pokemon Base Statistics and Move Data Power/Accuracy/PP/Type/Names.
- Keep Stable Visual Profile OFF: Starter Pokemon, Trainer Class Names, Evolution Randomization and Special-Wild/Day-Night/Swarms.
- This is still a short smoke and does not promote any new P1 status.
- Known exclusions remain separate: Starter/Rival sync, Trainer Class Names visual mismatch and Special-Wild scope.
- Recommended next block: isolate Starter Pokemon/rival first-battle sync if starters should enter the stable profile; otherwise continue with longer local playthrough sampling on the same Stable Visual Profile.
- Continue reporting sanitized yes/no evidence only, without ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens or `.env` data.

# Next steps update - GUI working settings matrix

- Treat UPR-FVX PR #88 and PR #89 as synced into the workspace pin at `f3a6d04ff6db8d48468800194e0baffbafb7505c`.
- Treat the current GUI Working Settings Matrix as locally passed for the sanitized normal walkthrough scope after fixes through PR #89.
- Keep the stable visual profile conservative: Wild Standard/Fallback, Trainer Pokemon core, Pokemon Movesets -> Random completely, Trainer Movesets, Trainer Names, Field Items basic, Pokemon Abilities, TM/HM/Tutor options, supported Shop Items, Pickup Items, In-Game Trades, Static Pokemon, Type Effectiveness, Pokemon Base Statistics and Move Data slices are recorded as passed with the documented caveats.
- Keep Trainer Class Names off for visual consistency unless class-text-only remapping is intentionally desired; class id and trainer sprite remain unchanged by that option.
- Keep Starter Pokemon off the stable profile until rival first-battle sync is diagnosed.
- Keep Special-Wild out-of-scope and swarms disabled by CFRU `SWARM_CHANCE=0`.
- Recommended next option block: isolate Starter Pokemon/rival starter sync, or run one stable-profile local smoke with Trainer Class Names, Starters and Special-Wild still disabled before expanding further.
- Do not promote any new P1 status from this sync; continue reporting sanitized yes/no evidence only, without ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens or `.env` data.

# Next steps update - Trainer Names/Class Names GUI smoke

- Treat UPR-FVX PR #83, PR #85 and PR #86 as synced into the workspace pin at `f86315e7528ba3257df03b80c0c75ccc69ef574b`.
- Treat Trainer Names as locally GUI-smoke passed for the current normal walkthrough path; changed names are visible in the Trainer Pokemon log.
- Treat Trainer Class Names as locally GUI-smoke passed for global class-label remapping. The option remaps class labels, so the same original class receives the same new class label.
- The previous `Director` and `[PKMN] BREEDER` collapse symptoms are resolved in sanitized local evidence.
- Per-trainer class assignment is not supported by this option and remains a separate possible future feature.
- Keep Evolutions, Wild Standard/Fallback, Trainer Pokemon core and Pokemon Movesets -> Random completely as stable in the tested path. Squirtle -> Wartortle Lv16 remains correct.
- Keep swarms disabled and Special-Wild systems out-of-scope.
- Recommended next isolated option block: a first Items/Moves/Abilities slice, still with Special-Wild systems disabled and without P1 promotion.
- Continue reporting sanitized yes/no evidence only, without ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens or `.env` data.

# Next steps update - CFRU/DPE evolution row stride fix

- Treat UPR-FVX PR #82 as synced into the workspace pin at `485f0b899c84470f3fab82317331a671ec023ac1`.
- Evolution row stride is fixed for the CFRU/DPE Gen9 path: `EVOS_PER_MON=16`, `evolutionSlotsPerSpecies=16` and `evolutionRowSize=0x80`.
- Sanitized local Evolution Report evidence after PR #82 shows the private input ROM starter chains correct and a newly generated output preserving the same starter chains.
- Correct starter chain baseline: Bulbasaur -> Ivysaur Lv16, Ivysaur -> Venusaur Lv32, Charmander -> Charmeleon Lv16, Charmeleon -> Charizard Lv36, Squirtle -> Wartortle Lv16 and Wartortle -> Blastoise Lv36.
- Sanitized ingame smoke evidence after PR #82 shows Squirtle evolved into Wartortle at Lv16 in a new FVX output.
- Discard previous bad/Test13-style outputs; they are stale because they were produced before the evolution row-stride fix.
- Next recommended local option block: keep Special-Wild off and choose one separate narrow scope, preferably Trainer Names/Class Names or a first Items/Moves/Abilities slice, rather than full randomization.
- Do not promote any new P1 status from this sync; continue reporting sanitized yes/no evidence without ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens or `.env` data.

# Next steps update - GUI-4B no-swarms pass

- Treat GUI-4B as passed for Wild Standard/Fallback plus Trainer Pokemon core plus Pokemon Movesets -> Random completely in sanitized local GUI E2E evidence.
- The empty-learnset `SpeciesMovesetRandomizer` crash is resolved for this scope; the prior `IndexOutOfBoundsException` was not reproduced.
- Treat Swarm-Frigibax as neutralized for normal randomized walkthroughs by the synced CFRU `SWARM_CHANCE=0` config. Route 1 no-swarm rebuild evidence did not observe Swarm-Frigibax, and an example Route 1 encounter was Urshifu Lv3 displayed correctly.
- Ogerpon remains valid and pool-eligible after the Learnset/Sprite/Palette fixes.
- Remaining guarded invalid palette candidates are known warnings and not blockers.
- CFRU Day/Night Wild and other Special-Wild systems remain out-of-scope and are not promoted.
- Recommended next local option block: keep Special-Wild off and choose one separate narrow scope, preferably Trainer Names/Class Names or a first Items/Moves/Abilities slice, rather than full randomization.
- Do not promote any new P1 status from this sync; continue reporting sanitized yes/no evidence without ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens or `.env` data.

# Next steps update - GUI-4A Ogerpon Wild/Trainer pass

- Treat GUI-4A as passed for Wild Standard/Fallback plus Trainer Pokemon core in sanitized local GUI E2E evidence.
- Ogerpon's Learnset/Sprite/Palette blocker is resolved for the current randomizer pool; Ogerpon appears in Trainer output/log and is pool-eligible.
- Keep remaining invalid candidates guarded: Bad Egg for no usable learnset, plus Warrior, Exeggcute, Cubone, Koffing and Mime Jr. for invalid/missing front battle sprite/palette.
- CFRU Day/Night Wild, Swarms and other Special-Wild systems remain out-of-scope for the current normal walkthrough goal.
- Recommended next local option block: GUI-4B Learnsets only, layered on top of the now-passed Wild Standard/Fallback plus Trainer Pokemon core path. Keep Trainer Names/Class Names and Items/Moves/Abilities separate unless explicitly selected next.
- Do not promote any new P1 status from this sync; continue reporting only sanitized yes/no evidence without ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens or `.env` data.

# Next steps update - Ogerpon asset fix sync

- Treat the Ogerpon front-sprite/palette asset blocker as resolved in the sanitized Pool Asset Report baseline after syncing DPE PR #2 and UPR-FVX PR #77.
- Current sanitized report baseline: 1186 accepted after guard, 6 excluded total, 1 no-usable-learnset exclusion, 5 invalid/missing front battle sprite pointer exclusions and 5 invalid/missing normal palette pointer exclusions.
- Ogerpon internal slots 1422..1429 now have valid learnsets, front sprite pointers and normal palette pointers in the report.
- Ogerpon status is accepted.
- Remaining invalid candidates are Bad Egg for no usable learnset, plus Warrior, Exeggcute, Cubone, Koffing and Mime Jr. for invalid/missing front battle sprite pointers.
- Next local GUI step: rerun the local GUI E2E path with the updated DPE/UPR-FVX pins before broadening option groups; keep reporting sanitized yes/no evidence only.
- Do not promote any new P1 status from this sync; keep ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens and `.env` data out of documentation.

# Next steps update - CFRU/DPE learnset runtime fixes sync

- Treat the learnset-runtime-pointer blocker as resolved in the sanitized Pool Asset Report baseline after syncing UPR-FVX PR #76, CFRU PR #3, CFRU PR #2 and DPE PR #1.
- Current sanitized report baseline: 1185 accepted after guard, 7 excluded total, 1 no-usable-learnset exclusion, 6 invalid/missing front battle sprite pointer exclusions and 6 invalid/missing normal palette pointer exclusions.
- Ogerpon now has a valid learnset and moves in the report: movesLearntCount 20 and learnsetPointerValid true.
- Ogerpon remains excluded because of invalid/missing front battle sprite pointer.
- Next technical block: diagnose Ogerpon/front battle sprite pointer before expanding GUI E2E options further around Ogerpon-eligible pools.
- Do not promote any new P1 status from this sync; keep reporting sanitized evidence only, without ROM paths, hashes, full logs, screenshots, output ROMs, saves, emulator states, private paths, secrets, tokens or `.env` data.

# Next steps update - GUI E2E Wild smoke pass

- Treat GUI-0 through GUI-3 as passed for the minimal Wild Standard/Fallback route: GUI load, Wild-only randomization, local output creation, BizHawk boot and first wild encounter all succeeded in sanitized local evidence.
- Keep the evidence boundary narrow: this is GUI workflow evidence for Wild Standard/Fallback only and does not promote any new P1 scope.
- Next local step is GUI-4: add one option group at a time.
- Start GUI-4 with either a Trainer-Core slice or a Learnsets slice.
- Do not jump directly to full randomization; keep Trainer Names/Class Names, Items/Moves/Abilities and Special Wild systems separate unless explicitly selected as the next isolated smoke.
- Continue reporting only sanitized yes/no evidence without ROM paths, hashes, CRCs, full logs, screenshots, saves, emulator states, private paths, secrets, tokens or `.env` data.

# Next steps update - GUI load null species fix sync

- Treat GUI-0 as passed after UPR-FVX PR #68: the private custom ROM loads in the local UPR-FVX GUI with null Species filtered from dropdown Species lists.
- Continue with GUI-1 locally: start a fresh/minimal GUI session, enable only Wild Standard/Fallback randomization and attempt to create one local output ROM.
- Keep Trainer Names/Class Names, Learnsets, Items/Moves/Abilities, Special Wild systems, Day/Night Wild, Swarms, Roamers, DexNav, Raids and Wild Double Battles disabled for GUI-1.
- Report GUI-1 only with sanitized yes/no fields; do not include ROM paths, output paths, hashes, full logs, screenshots with private paths, saves, emulator states, build artifacts, secrets, tokens or `.env` data.
- Do not promote any new P1 support from the GUI-0 load pass.

# Next steps update - GUI E2E smoke pipeline

- Run the GUI E2E smoke locally, not through Codex: GUI-0 load the private custom ROM in UPR-FVX GUI without randomization, GUI-1 enable only Wild Standard/Fallback and create one local output ROM, GUI-2 boot that output ROM locally, GUI-3 reach the first wild encounter.
- Report back only with the sanitized yes/no structure from `08_tests/randomizer/gui_e2e_smoke_pipeline.md`.
- Keep Trainer Names/Class Names, Learnsets, Items/Moves/Abilities, Special Wild systems, Day/Night Wild, Swarms, Roamers, DexNav, Raids and Wild Double Battles disabled until GUI-0 through GUI-3 are clean.
- Do not include ROM paths, output paths, hashes, full logs, screenshots with private paths, saves, emulator states, build artifacts, secrets, tokens or `.env` data.
- Do not promote any new P1 support from this documentation-only block.

# Next steps update - Trainer text ROM smoke harness sync

- Treat UPR-FVX PR #67 as harness-prepared only: a ROM-facing Gen3 Trainer Names/Class Names smoke can now be run locally with explicit private-ROM opt-in.
- The harness default path skips without ROM, so normal tests do not require or expose private ROM material.
- Keep Trainer Names/Class Names below P1-supported; the real local ROM smoke has not been documented.
- Byte-exact Terminator/Padding inspection is still not directly proven and remains a later evidence gap.
- Next Trainer Names/Class Names work, if explicitly authorized, should run the harness locally with private ROM and summarize only sanitized pass/fail evidence. Do not document ROM paths, hashes, full logs or output ROMs.
- Do not promote P1 from PR #67 alone.

# Next steps update - Wild encounters P1 decision

- Treat Standard/Fallback Wild Encounters as `P1-supported` for the documented writer/reload scope in the tested private target context.
- Keep special Wild systems separate: CFRU Day/Night Wild, Swarms, Roamers, DexNav, Raids, Wild Double Battles and other non-standard systems are not promoted by this decision.
- Next Randomizer work should move to the next explicitly scoped area; do not rerun or expand Wild ROM evidence unless a new Wild sub-scope is opened.

# Next steps update - Wild encounters ROM smoke evidence sync

- Treat UPR-FVX PR #66 plus the sanitized local `Gen3WildEncounterRomSmokeTest` pass as ROM-facing Writer/Reload smoke evidence for Wild Encounters.
- Wild Encounters is now a P1 candidate, not automatically P1-promoted.
- Next Wild work should be a short separate P1 decision/evaluation that reviews this evidence and any remaining P1 criteria.
- Keep private ROM paths, hashes, full logs and output ROMs out of documentation.

# Next steps update - Wild encounters ROM smoke harness sync

- Treat UPR-FVX PR #65 as harness-prepared only: a ROM-facing Wild Encounter writer/reload smoke can now be run locally with explicit private-ROM opt-in.
- The harness default path skips without ROM, so normal tests do not require or expose private ROM material.
- Keep Wild Encounters below P1-supported; the real local ROM smoke has not been executed or reviewed.
- Next Wild work, if explicitly authorized, should run the harness locally with private ROM and summarize only non-private pass/fail evidence. Do not document ROM paths, hashes, logs or output ROMs.
- Do not promote P1 from PR #65 alone.

# Next steps update - Wild encounters reload equality evidence sync

- Treat UPR-FVX PR #64 as the first ROM-free Writer/Reload Equality evidence for Wild Encounters only.
- The pinned `WildCatchLevelDecisionTest` now includes a synthetic reloadable `RomHandler` path that proves written Wild Encounter slot data reloads equal for area metadata, slot counts, level ranges, allowed Species and high Species IDs above `1000`.
- Keep Wild Encounters below P1-supported; real Gen3 byte writer/reload proof, output ROM evidence and a Randomizer run remain missing.
- Next Wild P1 work, if explicitly authorized, should target the smallest ROM-facing or equivalent Gen3 writer/reload proof. Do not promote P1 from PR #64 alone.

# Next steps update - Items first test slice sync

- Treat the UPR-FVX PR #63 sync as a narrow ROM-free Items/Moves/Abilities evidence update only.
- The pinned `ItemDecisionTest` now includes a first synthetic Items slice: `ItemRandomizer.randomizeFieldItems()` for Non-TM Field Items keeps choices inside the non-bad allowed Item pool, excludes bad/key-style Items, keeps output non-empty, preserves Field-Item count and allows high Item IDs `1001..1003`.
- Keep Items/Moves/Abilities below P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or reload equality was produced in this sync.
- Next Items/Moves/Abilities work, if explicitly authorized, should choose another narrow ROM-free Move/Ability/Item behavior slice or a later ROM-facing/equivalent Writer/Reload evidence plan.
- Do not run ROM evidence, perform Writer-/Reload smokes or promote P1 from this sync.

# Next steps update - Moves first test slice sync

- Treat the UPR-FVX PR #62 sync as a narrow ROM-free Items/Moves/Abilities evidence update only.
- The pinned `TMTutorMoveDecisionTest` now includes a first synthetic Moves slice: `TMTutorMoveRandomizer.randomizeTMMoves()` keeps choices inside the allowed Move pool, excludes HM/game-breaking/levelup-banned/illegal Moves, preserves the Field-Move-TM slot, keeps output count stable and allows high Move IDs `1001..1003`.
- Keep Items/Moves/Abilities below P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or reload equality was produced in this sync.
- Next Items/Moves/Abilities work, if explicitly authorized, should choose another narrow ROM-free Move/Ability/Item behavior slice or a later ROM-facing/equivalent Writer/Reload evidence plan.
- Do not run ROM evidence, perform Writer-/Reload smokes or promote P1 from this sync.

# Next steps update - Items/Moves/Abilities first test slice sync

- Treat the UPR-FVX PR #61 sync as a narrow ROM-free Items/Moves/Abilities evidence update only.
- The pinned `SpeciesAbilityDecisionTest` now includes a first synthetic Ability slice: `SpeciesAbilityRandomizer` keeps choices inside the allowed Ability pool, rejects banned Ability candidates, produces non-empty two-Ability output and keeps Species ID `1025` in the path.
- Keep Items/Moves/Abilities below P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or reload equality was produced in this sync.
- Next Items/Moves/Abilities work, if explicitly authorized, should choose another narrow ROM-free Move/Ability/Item behavior slice or a later ROM-facing/equivalent Writer/Reload evidence plan.
- Do not run ROM evidence, perform Writer-/Reload smokes or promote P1 from this sync.

# Next steps update - Learnsets evolution moves test slice sync

- Treat the UPR-FVX PR #60 sync as a narrow ROM-free Learnsets option-test evidence update only.
- The pinned `LearnsetDecisionTest` now includes a fourth synthetic Evolution Moves for All slice: exactly one Level-0 Evolution-Move slot is added while existing Level-1/later level slots, Move pool and high Species ID `1025` path stay stable.
- Keep Learnsets below P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or reload equality was produced in this sync.
- Learnsets now has four small ROM-free slices; next Learnsets work should be a separately authorized ROM-facing/equivalent Writer/Reload evidence plan or a different Randomizer area.
- Do not run ROM evidence, perform Writer-/Reload smokes or promote P1 from this sync.

# Next steps update - Learnsets starting moves test slice sync

- Treat the UPR-FVX PR #59 sync as a narrow ROM-free Learnsets option-test evidence update only.
- The pinned `LearnsetDecisionTest` now includes a third synthetic Guaranteed Starting Moves slice: expected Level-1 slots are added, the later level slot is preserved, Move pool stays stable and high Species ID `1025` remains in the path.
- Keep Learnsets below P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or reload equality was produced in this sync.
- Next Learnsets work, if explicitly authorized, should choose another narrow ROM-free behavior slice or a later ROM-facing/equivalent Writer/Reload evidence plan.
- Do not run ROM evidence, perform Writer-/Reload smokes or promote P1 from this sync.

# Next steps update - Learnsets option test slice sync

- Treat the UPR-FVX PR #58 sync as a narrow ROM-free Learnsets option-test evidence update only.
- The pinned `LearnsetDecisionTest` now includes a second synthetic `orderDamagingMovesByDamage()` slice: damaging Moves are sorted by damage while Evolution-/Non-Damaging-Slots remain unchanged, Level-/Slot-Anzahl and Move pool stay stable and high Species ID `1025` remains in the path.
- Keep Learnsets below P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or reload equality was produced in this sync.
- Next Learnsets work, if explicitly authorized, should choose another narrow ROM-free behavior slice or a later ROM-facing/equivalent Writer/Reload evidence plan.
- Do not run ROM evidence, perform Writer-/Reload smokes or promote P1 from this sync.

# Next steps update - Learnsets first test slice sync

- Treat the UPR-FVX PR #57 sync as a narrow ROM-free Learnsets unit-test evidence update only.
- The pinned `LearnsetDecisionTest` now includes a first synthetic `randomizeMovesLearnt()` slice: Learnsets stay non-empty, Level-/Slot-Anzahl remains stable, selected Moves stay in the allowed pool and high Species ID `1025` is processed.
- Keep Learnsets below P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or reload equality was produced in this sync.
- Next Learnsets work, if explicitly authorized, should choose another narrow ROM-free option/behavior slice or a later ROM-facing/equivalent Writer/Reload evidence plan.
- Do not run ROM evidence, perform Writer-/Reload smokes or promote P1 from this sync.

# Next steps update - Wild encounters option test slice sync

- Treat the UPR-FVX PR #56 sync as a narrow ROM-free Wild Encounter option-test evidence update only.
- The pinned `WildCatchLevelDecisionTest` now includes a third synthetic option slice for `BlockWildLegendaries`, proving the option keeps legendary Species out of the replacement pool under ROM-free test data.
- Keep Wild Encounters below P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or reload equality was produced in this sync.
- Next Wild work, if explicitly authorized, should choose another narrow ROM-free option slice or a later ROM-facing/equivalent Writer/Reload evidence plan.
- Do not run ROM evidence, perform Writer-/Reload smokes or promote P1 from this sync.

# Next steps update - Wild encounters multi-area test slice sync

- Treat the UPR-FVX PR #55 sync as a narrow ROM-free Wild Encounter unit-test evidence update only.
- The pinned `WildCatchLevelDecisionTest` now includes a second synthetic Multi-Area-/Multi-Slot Wild Encounter slice: unterschiedliche Areas, Slot-Anzahlen, Levelbereiche, encounter types, rates and map/location metadata remain structurally stable.
- Keep Wild Encounters below P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or reload equality was produced in this sync.
- Next Wild work, if explicitly authorized, should choose a separate narrow scope: either more ROM-free option coverage or a later ROM-facing/equivalent Writer/Reload evidence plan.
- Do not run ROM evidence, perform Writer-/Reload smokes or promote P1 from this sync.

# Next steps update - Wild encounters first test slice sync

- Treat the UPR-FVX PR #54 sync as a narrow ROM-free Wild Encounter unit-test evidence update only.
- The pinned `WildCatchLevelDecisionTest` now includes a first synthetic Wild Encounter slice for preserved Slot-/Level-/Area structure, non-empty encounter areas, allowed Species selection and high-numbered Species IDs above `1000`.
- Keep Wild Encounters below P1-supported; no ROM-facing Writer/Reload evidence, output ROM, Randomizer run or reload equality was produced in this sync.
- Next Wild work, if explicitly authorized, should choose a separate narrow scope: either more ROM-free option coverage or a later ROM-facing/equivalent Writer/Reload evidence plan.
- Do not run ROM evidence, perform Writer-/Reload smokes or promote P1 from this sync.

# Next steps update - Trainer Class Names encoded length fix sync

- Treat the UPR-FVX PR #53 sync as a narrow fix/evidence update only.
- The Trainer Class Names `changeTo.length()` selection-guard risk is fixed in the pinned UPR-FVX logic by using encoded/internal length.
- Keep `FVX-FOE-013` Trainer Names/Class Names at `tested-non-rom`, not P1-supported.
- Any later P1 discussion still needs separately authorized ROM-facing or equivalent Writer/Reload evidence for fixed-field byte length, byte-truncation absence, Terminator/Padding validity and decoded reload equality.
- Do not run ROM evidence, perform Writer-/Reload smokes, make Text-Encoding support claims or promote P1 from this sync.

# Next steps update - Trainer Names text length unit evidence

- Treat `08_tests/randomizer/031_trainer_names_text_length_unit_evidence.md` as ROM-free unit-test evidence only.
- Keep `FVX-FOE-013` Trainer Names/Class Names at `tested-non-rom`, not P1-supported.
- The next possible step, only if explicitly authorized, is a separate ROM-facing or equivalent writer/reload evidence plan for fixed-field byte length, truncation absence, Terminator/Padding validity and decoded reload equality.
- Keep the Class-Names `changeTo.length()` risk open unless a later fix/evidence scope explicitly addresses encoded/internal class-name limits.
- Do not run ROM evidence, implement Writer-/Reload fixes, make Text-Encoding support claims or promote P1 from this unit evidence.

# Next steps update - Trainer Names text harness design

- Treat `08_tests/randomizer/030_trainer_names_text_harness_design.md` as a design only.
- Keep `FVX-FOE-013` Trainer Names/Class Names at `tested-non-rom`, not P1-supported.
- Next minimal implementation, if explicitly authorized, should be a focused UPR-FVX unit-test branch extending the existing Trainer-name test style with a fake `RomHandler` encoded/internal length model that differs from Java length.
- Include a class-name risk test that exposes `changeTo.length()` without fixing it; keep any fixed-field byte-model helper test-only and ROM-free.
- Do not run ROM evidence, implement Writer-/Reload fixes, make Text-Encoding support claims or promote P1 from this design.

# Next steps update - Trainer Names text evidence harness plan

- Treat `08_tests/randomizer/029_trainer_names_text_evidence_harness_plan.md` as a plan only.
- Keep `FVX-FOE-013` Trainer Names/Class Names at `tested-non-rom`, not P1-supported.
- Next minimal implementation, if explicitly authorized, should start with a ROM-free harness that proves selection behavior using encoded/internal length and exposes the `changeTo.length()` class-name risk with synthetic strings.
- Any later ROM-facing evidence must separately prove fixed-field byte length, byte-truncation absence, terminator/padding validity and decoded reload equality before P1 can be discussed.
- Do not run ROM evidence, implement Writer-/Reload fixes, make Text-Encoding support claims or promote P1 from this plan.

# Next steps update - Trainer writer/reload/text field review

- Treat `08_tests/randomizer/028_trainer_writer_reload_text_field_review.md` as read-only preparation only.
- Current Trainer follow-up suboptions remain `tested-non-rom`, not P1-supported.
- If continued, open a separate narrow evidence plan or harness design for exactly one Trainer scope.
- For Trainer Names/Class Names, require encoded/internal byte length, fixed-field write/reload, terminator/padding validity and decoded reload equality; do not rely on Java `String.length()` / `changeTo.length()` as the proof metric.
- Do not run ROM evidence, implement Writer-/Reload fixes, make Text-Encoding support claims or promote P1 from this review.

# Next steps update - Trainer ROM/Reload/Text evidence plan

- Treat the new Trainer ROM-/Reload-/Text-Encoding evidence document as a plan only.
- Keep current Trainer follow-up suboptions at `tested-non-rom`, not P1-supported, until a separately authorized evidence scope exists.
- Next minimal step, if continued, should be a read-only design/review block that identifies exact Trainer writer/reload fields and exact Trainer text encoder/decoder length checks.
- Do not run ROM evidence, implement Writer-/Reload fixes, make Text-Encoding claims, rely on `changeTo.length()` alone, or promote P1 from this plan.

# Next steps update - Diagnose 181

- Treat `FVX-FOE-013` Trainer Names/Class Names as `tested-non-rom`, not P1-supported.
- The merged UPR-FVX PR #51 harness covers ROM-free `TrainerNameRandomizerTest` decisions with synthetic data: `canChangeTrainerText=false`, singles-/doubles-pools, repeated-name translation, `MAX_LENGTH`, `MAX_LENGTH_WITH_CLASS`, Class-Name pools and fixed class-name length.
- Keep Gen3 Writer-/Reload-ROM evidence, ROM-Smoke, text-encoding proof, output-ROM generation, Randomizer runs, `changeTo.length()` fixes and P1-promotion out of scope unless separately authorized.
- Next minimal Trainer block, if continued, should be another still-open Trainer scope or an explicit ROM-/Reload/Text-Encoding evidence plan. Do not start implementation from this follow-up.

# Next steps update - Diagnose 180B

- Treat `FVX-FOE-011` Battle Style as `tested-non-rom`, not P1-supported.
- The merged UPR-FVX PR #50 harness covers ROM-free Battle Style decisions with synthetic Trainer data: `UNCHANGED`, `SINGLE_STYLE`, deterministic `RANDOM` and too-few-Pokemon skips.
- Keep Writer-/Reload-ROM evidence, ROM-Smoke, output-ROM generation, Randomizer runs and P1-promotion out of scope unless separately authorized.
- Keep `FVX-FOE-013` Trainer Names/Class Names/Text separate and unstarted.
- Next minimal Trainer block, if continued, should be a read-only plan for `FVX-FOE-013` Trainer Names/Class Names/Text or another still-open Trainer suboption, without implementing text changes.

# Next steps update - Diagnose 179B

- Treat `FVX-FOE-010`, `FVX-FOE-012` and `FVX-FOE-014` Trainer Special Rules as `tested-non-rom`, not P1-supported.
- The merged UPR-FVX PR #49 harness covers ROM-free League Unique, Rival Carries Starter and Trainers Evolve Their Pokemon + Level Modifier behavior with synthetic Trainer, Party, Species and Evolution data.
- Keep `FVX-FOE-011` Battle Style and `FVX-FOE-013` Trainer Names/Class Names/Text as separate scopes.
- Do not run ROM-Smoke, Trainer Writer-/Reload-ROM tests, Trainer Names/Class Names/Text work, Battle Style work, output-ROM generation, Randomizer runs or P1-promotion work without a separate explicit scope.

# Next steps update - Diagnose 178B

- Treat `FVX-FOE-005`, `FVX-FOE-006` and `FVX-FOE-007` Additional Pokemon for Boss, Important and Regular Trainers as `tested-non-rom`, not P1-supported.
- The merged UPR-FVX PR #48 harness covers ROM-free Trainer Additional Pokemon mutation/guard behavior with synthetic Trainer, Party and Species data.
- Do not run ROM-Smoke, Trainer Writer-/Reload-ROM tests, Trainer Names/Class Names/Text work, output-ROM generation, Randomizer runs or P1-promotion work without a separate explicit scope.

# Next steps update - Diagnose 177B

- Treat `FVX-FOE-009` Force Diverse Types / Type Themes as `tested-non-rom`, not P1-supported.
- The merged UPR-FVX PR #47 harness covers ROM-free Trainer Type Diversity null Primary/Secondary Type guard behavior with synthetic Trainer and Species data.
- Do not run ROM-Smoke, Writer-/Reload-ROM tests, Trainer Names/Class Names/Text work, output-ROM generation, Randomizer runs or P1-promotion work without a separate explicit scope.

# Next steps update - Diagnose 176B

- Treat `FVX-WILD-007`, `FVX-WILD-010` and `FVX-WILD-012` as `tested-non-rom`, not P1-supported.
- The merged UPR-FVX PR #46 harness covers ROM-free Wild minimum Catch Rate, Catch Em All and Level Modifier / Balance Low Level decisions with synthetic data.
- Do not run ROM-Smoke, Writer-/Reload-ROM tests, output-ROM generation, Randomizer runs or P1-promotion work without a separate explicit scope.

# Next steps update - Diagnose 175B

- Treat `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` and `FVX-MOVE-006` as `tested-non-rom`, not P1-supported.
- The merged UPR-FVX PR #45 harnesses cover ROM-free Gen3 MoveData writer decisions and MoveUpdater apply decisions with synthetic data.
- Keep `FVX-MOVE-005` Move Names/Text separate and out of scope.
- Do not run ROM-Smoke, Writer-/Reload-ROM tests, output-ROM generation, Randomizer runs or Move Names/Text work without a separate explicit scope.

# Next steps update - Diagnose 174B

- Treat `FVX-TRAIT-025A` as `tested-non-rom`, not P1-supported.
- The merged UPR-FVX PR #44 harness covers only ROM-free Make Evolutions Easier Condense-/Level-/Decision logic through synthetic Species/Evolution chains.
- Keep `FVX-TRAIT-025B` separate: Gen3 Happiness-byte patch / writer-like scope still needs its own read-only plan or explicit implementation scope.
- Keep `FVX-TRAIT-026` attached to `024/025`; do not promote it standalone.
- Do not run ROM-Smoke, Writer/Reload tests, output-ROM generation, Randomizer runs or Gen3 Happiness-byte patch work without a separate explicit scope.

# Next steps update - Diagnose 173

- Treat `FVX-TRAIT-025` as `make-easier-plan-ready`, not tested and not P1-supported.
- Split future work into `025A` ROM-free Condense-/Level-/Decision harness and `025B` Gen3 Happiness-byte patch / writer-like scope.
- Next minimal implementation, if continued, should be a small UPR-FVX Non-ROM `:romio:test` for `025A` only: synthetic Species/Evolution chains, intermediate/final level caps, non-level `estimatedEvoLvl` capping and `highestEvoLvl` behavior.
- Keep `025B` out of that first harness; any byte-patch, writer/reload, ROM-Smoke, Save, Output-ROM or Randomizer run needs separate explicit scope.
- Keep `FVX-TRAIT-026` attached to `024/025`; do not promote it standalone.

# Next steps update - Diagnose 172B

- Treat `FVX-TRAIT-024` and `FVX-TRAIT-027` as `tested-non-rom`, not P1-supported.
- The merged UPR-FVX PR #43 harness covers only ROM-free method decisions with synthetic `Species` / `Evolution` objects.
- Writer-/Reload-Evidenz, ROM-Smoke, output-ROM generation and Randomizer runs remain separate and unauthorized.
- Next minimal Evolution work, if continued, should be a read-only plan for `FVX-TRAIT-025`: split ROM-free condense-level logic from the Gen3 happiness-byte patch risk.
- Keep `FVX-TRAIT-026` attached to `024/025`; do not promote it standalone.

# Next steps update - Diagnose 171

- Treat `FVX-TRAIT-024` and `FVX-TRAIT-027` as `decision-review-ready`, not tested or P1-supported.
- Next minimal Evolution work, if continued, should be a small UPR-FVX ROM-free `:romio:test` decision harness for Change Impossible Evolutions and Remove Time-Based Evolutions.
- Test only synthetic `Species` / `Evolution` mapping decisions: Trade/Trade-Item/FRLG happiness/beauty for `024`, and timeless/paired Day-Night/Dusk mappings for `027`.
- Keep `FVX-TRAIT-025` split and keep `FVX-TRAIT-026` attached to `024/025`; do not promote either as standalone.
- Do not run ROM-Smoke, Randomizer runs, builds, Gen3 writer/reload tests or output-ROM generation without a separate explicit scope.

# Next steps update - Diagnose 170

- Treat `FVX-TRAIT-024` through `FVX-TRAIT-027` as `methods-plan-ready`, not tested or P1-supported.
- Next minimal Evolution work, if continued, should be a read-only UPR-FVX code-review / Non-ROM test-plan for `FVX-TRAIT-024` and `FVX-TRAIT-027` method-mapping decisions.
- Split `FVX-TRAIT-025` into ROM-free `condenseLevelEvolutions(...)` evidence and separate Gen3 happiness-byte writer/reload risk.
- Keep `FVX-TRAIT-026` attached to `024/025`; do not promote it as standalone.
- Do not run ROM-Smoke, Randomizer runs, builds, Gen3 writer/reload tests or output-ROM generation without a separate explicit scope.

# Next steps update - Diagnose 169B

- Treat `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023` as `tested-non-rom` after merged UPR-FVX PR #42.
- Keep these slices below P1-supported until a separately authorized ROM-Smoke / reload path exists.
- Do not run ROM-Smoke, Gen3 writer tests, output-ROM generation, Randomizer runs or builds for this follow-up status.
- Keep `FVX-TRAIT-024` through `FVX-TRAIT-027` separate; the next minimal Evolution work is a read-only plan for Evolution-improvement/method slices.

# Next steps update - Diagnose 168

- Treat the Evolution filter harness scope as ready: `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023` can be covered by a small UPR-FVX Non-ROM `:random:test`.
- Preferred later implementation: synthetic `Species` / `Evolution` graph plus `RomHandler` proxy/fake, scoped to `EvolutionRandomizerTest` or a new `EvolutionFilterRandomizerTest`.
- Keep `FVX-TRAIT-024` through `FVX-TRAIT-027` out of this harness; they remain separate Evolution-improvement/method slices.
- Do not run ROM-Smoke, Randomizer runs, Gen3 writer tests, output-ROM generation or builds unless separately authorized.

# Next steps update - Diagnose 167

- Treat the Evolution-Species-Carrier matrix as consolidated for `FVX-TRAIT-016` through `FVX-TRAIT-027`.
- Keep `FVX-TRAIT-016` as P1-supported and `FVX-TRAIT-018` / `FVX-TRAIT-019` as `diagnosis-ready`; do not open a fixbranch for these without new crash, unsafe Species or normalized reload mismatch evidence.
- If Evolution suboptions remain the next priority, plan a small read-only Non-ROM harness block for `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023`.
- Keep `FVX-TRAIT-024` through `FVX-TRAIT-027` separate from the Species-Carrier; they need their own Evolution-improvement/methods plan before any smoke or code work.

# Next steps update - Diagnose 166

- Treat `FVX-TRAIT-019` Evolution Same Typing as reclassified out of the active blocker lane for the narrow `FVX-TRAIT-016` Evolution-Species-Carrier scope.
- Do not open a UPR-FVX fix branch for Same Typing unless new evidence shows a null-type crash, normalized reload mismatches, unsafe target Species, or a Save/Log/Reload failure.
- If more confidence is required, the next minimal block should be read-only code review or a Non-ROM harness plan for the Same-Typing guard, not a ROM-Smoke.
- Keep Evolution-Methoden-Writer, Change Impossible Evolutions, Make Evolutions Easier, Text/Menu, Items, MoveData, TypeChart and Graphics as separate scopes.

# Next steps update - Diagnose 165

- Treat `FVX-TRAIT-018` Evolution Similar Strength as reclassified out of the active blocker lane for the narrow `FVX-TRAIT-016` Evolution-Species-Carrier scope.
- Do not open a UPR-FVX fix branch for Similar Strength unless new normalized reload evidence shows mismatches, unsafe target Species, or a Save/Log/Reload failure.
- If more confidence is required, the next minimal block should be read-only code review or a Non-ROM harness plan for Similar-Strength selection/normalization, not a ROM-Smoke.
- Keep Evolution-Methoden-Writer, Change Impossible Evolutions, Make Evolutions Easier, Text/Menu, Items, MoveData, TypeChart and Graphics as separate scopes.

# Next steps update - Diagnose 164

- Treat In-Game Trades as closed for the current tested scope: `guarded/preserve-only, not supported`.
- Do not spend the next block on In-Game Trades unless there is explicit new read-only active-row evidence, corrected locator/row-shape evidence, hard unsupported/dummy proof, or a separately authorized ROM-facing smoke scope.
- Do not run ROM-Smoke, Species-Write-Smoke, Randomizer runs, Text/Nickname/OT, IV or Trade Held Item randomization for In-Game Trades.
- Move to the next non-In-Game-Trades Randomizer roadmap item unless the user explicitly reopens one of the documented criteria.

# Next steps update - FVX dashboard XLSX export script

- Markdown remains the source of truth for `01_docs/randomizer/fvx-progress-dashboard.md`.
- Use `python 07_scripts/randomizer/export_fvx_progress_dashboard_xlsx.py --input 01_docs/randomizer/fvx-progress-dashboard.md --output /tmp/fvx-progress-dashboard.xlsx` when a local filterable workbook is needed.
- Do not commit generated `.xlsx` output unless a later review explicitly decides to version that visual dashboard artifact.

# Next steps update - Diagnose 163B

- Keep In-Game Trades closed as `blocked-pending-evidence`.
- The ROM-free Gen3 writer-preserve test is merged and pinned, so unsafe-row mutation and writer-preserve decisions now have non-ROM test coverage.
- Next allowed step, if explicitly requested, is a guarded/preserve-only closure decision or further read-only evidence for valid active trade rows.
- Do not run ROM-Smoke, Species-Write-Smoke, Randomizer runs, Text/Nickname/OT, IV or Trade Held Item randomization.

# Next steps update - Diagnose 162

- Keep In-Game Trades closed as `blocked-pending-evidence`.
- Next allowed implementation step, if explicitly requested, is a small UPR-FVX `:romio:test` writer-preserve unit test with a narrow Gen3 In-Game-Trade row-write decision seam.
- The later test should prove unsafe/null-request rows skip before byte writes and leave synthetic bytes unchanged; it should not test or promote valid active row writes.
- Do not run ROM-Smoke, Species-Write-Smoke, Randomizer runs, Text/Nickname/OT, IV or Trade Held Item randomization.

# Next steps update - Diagnose 161B

- Keep In-Game Trades closed as `blocked-pending-evidence`.
- The non-ROM `TradeRandomizer` harness is merged and pinned, so the immediate mutation-guard test gap is reduced.
- Next allowed step, if explicitly requested, is a read-only Gen3 writer-preserve-test plan or continued guarded/preserve-only tracking.
- Do not run ROM-Smoke, Species-Write-Smoke, Randomizer runs, Text/Nickname/OT, IV or Trade Held Item randomization.

# Next steps update - Diagnose 160

- Keep In-Game Trades closed as `blocked-pending-evidence`.
- Next allowed implementation step, if explicitly requested, is a small UPR-FVX non-ROM `TradeRandomizer` harness/unit-test for synthetic unsafe `InGameTrade` rows.
- First test scope should prove skipped null-request rows, skipped unsafe/placeholder Species rows, all-skipped `setInGameTrades(...)` avoidance, `changesMade=false`, and skip counter visibility.
- Defer Gen3 writer preserve testing unless it can be done without ROM bytes, generated artifacts, broad refactor or private fixtures.
- Do not run Species-Write-Smoke, ROM smoke, Randomizer runs, Text/Nickname/OT, IV or Trade Held Item randomization.

# Next steps update - Diagnose 159

- Keep In-Game Trades closed as `blocked-pending-evidence`.
- Recommended next step: a small explicitly scoped non-ROM harness for unsafe-row skip/preserve behavior, especially skip counters, no writer call when all rows skip, and `changesMade=false`.
- Do not run Species-Write-Smoke, ROM smoke, Text/Nickname/OT, IV or Trade Held Item randomization until valid active rows are separately proven and authorized.

# Next steps update - Diagnose 158B

- Keep In-Game Trades closed as `blocked-pending-evidence` even after the merged UPR-FVX PR #39 guard.
- Next allowed step is a targeted read-only/code-review of the guard behavior or an explicitly allowed non-ROM test/harness for skip/preserve behavior.
- Do not run Species-Write-Smoke and do not add Text, Nickname/OT, IV or Trade Held Item randomization until valid active rows are separately proven and authorized.

# Next steps update - Diagnose 157

- Keep In-Game Trades closed as `blocked-pending-evidence`.
- Optional later implementation branch: defensive null-request guard only, likely scoped to `TradeRandomizer.java` and `Gen3RomHandler.java`, with optional logger/status strings if needed.
- Do not run Species-Write-Smoke or include Nickname/OT, IV or Trade Held Item writes until skipped/preserved rows and valid active rows are separately proven.

# Next steps update - Diagnose 156

- Keep In-Game Trades closed as `blocked-pending-evidence`.
- Preserve/Skip policy: write no trade rows, leave dummy/placeholder/null-request structures unchanged, and do not prepare Species-Write-Smoke, Nickname/OT randomization, IV randomization or Trade Held Item randomization.
- Reopen only with explicit valid active-row evidence, corrected locator/row-shape evidence, an unsupported/dummy proof, or a separate defensive null-requested-species skip/guard plan.

# Next steps update - Diagnose 155

- Keep In-Game Trades Species-Write-Smoke blocked.
- Next minimal step: decide read-only between corrected locator evidence, explicit active-row evidence, content-based dummy-row skip policy, defensive null-requested-species handling, or unsupported/dummy scope.
- Do not prepare Species writes, Nickname/OT randomization, Trade Held Item randomization, IV randomization or other feature-scope work until valid active rows are confirmed.

# Next steps update - Diagnose 154

- Keep In-Game Trades Species-Write-Smoke blocked.
- Next minimal step remains a read-only locator/table-model candidate diagnostic with valid-active-row confirmation or an unsupported/dummy-row decision.
- Do not include Nickname/OT text, Trade Held Items or IV extras in the first write path.

# Next steps update - Diagnose 153

- Next minimal step: run a read-only In-Game Trades locator/table-model diagnostic.
- Do not run species-only write/reload smoke until valid active trade rows are confirmed and requestedSpecies-null handling is resolved.
- Keep Nickname/OT text, Trade Held Items and IV extras out of the locator diagnostic except for read-only field classification.

# Next steps update - Diagnose 152

- Next minimal step: plan a narrow In-Game Trades locator/table-model blocker diagnostic before any write/reload smoke.
- Do not run the Given/Requested species-only smoke until active trade rows classify with valid Species fields and requestedSpecies-null risk is resolved.
- Keep Nickname/OT fixed-length text randomization separate and blocked until locator and species safety are proven.

# Next steps update - Diagnose 151

- Next minimal Randomizer step: run an In-Game Trades read-only candidate diagnostic.
- First diagnostic should record sanitized trade count, requested/given species safety, held-item field safety, fixed-length nickname/OT readability, IV readability and foreign-scope isolation.
- Do not start with text randomization; nickname/OT fixed-length fields should remain a separate follow-up after species and item paths are proven reload-stable.

# 2026-05-15 - Next: move past Special Wild unless requirements change

Special Wild triggerability is documented in Diagnose 150 and does not require immediate UPR-FVX writer work in the tracked state.

Recommended next step: choose the next major Randomizer feature scope outside already closed Standard Wild, Items, Shops and Held Items.

Only reopen Special Wild if non-empty Day/Night headers, Swarm runtime requirements, Raid support or DexNav/Wild-Double gameplay tests become explicit product goals.

# 2026-05-15 - Next: special Wild Encounter systems

Recommended next branch: `analysis/upr-fvx-cfru-dpe-special-wild-encounter-systems-scope-plan`.

Goal: plan read-only diagnostics for CFRU Day/Night Wild, Swarms, Roamers, DexNav, Raids and special encounter tables without retesting already covered Standard Wild P0.

Keep out of scope: Held Items, Trainer Pokemon, Starters, Static/Gift, Field Items, Pickup, Shops, code changes, builds, Randomizer runs and ROM writes.

# 2026-05-15 - Next: Wild Encounters read-only candidate diagnostic

Recommended next branch: `test/upr-fvx-cfru-dpe-wild-encounters-scope-diagnostics`.

Goal: scan Wild Encounter areas and slots read-only, classify encounter types and validate SpeciesSet identity mapping without writes, builds or Randomizer runs.

Keep out of scope: Wild Held Items, Trainer Pokemon, Starters, Static/Gift Pokemon, Field Items, Pickup, Shops and all non-Wild-Encounter features.

# 2026-05-15 - Next: next major Randomizer feature scope

Held Items scope is closed in the tested CFRU/DPE Gen9-BPRE scope after Diagnose 147.

Recommended next branch: create a new analysis branch for the next major Randomizer feature scope.

Keep out of scope unless explicitly reopened: Wild Held Items, Trainer Held Items, Starter Held Items, Field Items, Pickup, Shops and prior completed item scopes.

# 2026-05-15 - Next: Starter Held Items + Ban Bad

Recommended next branch: `test/upr-fvx-cfru-dpe-starter-held-items-ban-bad-reload-smoke`.

Goal: test Starter Held Items with `banBadRandomStarterHeldItems=true` after Diagnose 146 confirmed Starter Held Items reload stability without Ban Bad.

Keep out of scope: Wild Held Items, Trainer Held Items, Field Items, Pickup, Shops and non-Held-Item randomizer work.

# 2026-05-15 - Next: Starter Held Items or optional Trainer filter combinations

Recommended next branch: `test/upr-fvx-cfru-dpe-starter-held-items-reload-smoke` if Boss/Important filter combinations are not required.

Optional alternative: plan Boss/Important Trainer Held Item filter combinations only if product coverage requires them.

Keep out of scope for Starter: Wild Held Items, Trainer Held Items, Field Items, Pickup, Shops and non-Held-Item randomizer work.

# 2026-05-15 - Next: Trainer Held Item filter smoke

Recommended next branch: `test/upr-fvx-cfru-dpe-trainer-held-items-regular-filters-reload-smoke`.

Goal: test Regular Trainer Held Items with `Consumable Only`, `Sensible Items` and `Highest Level Only` enabled, while preserving Boss, Important, `shouldNotGetBuffs`, Wild, Starter, Field, Pickup and Shop scopes.

Fallback: if the combined filter smoke is too broad, split into Consumable-only, Sensible-only and Highest-Level-only smokes.

# 2026-05-15 - Next: Trainer Held Item filters or Starter Held Items

Recommended next branch: `analysis/upr-fvx-cfru-dpe-trainer-held-items-filters-scope-plan` if filter coverage is required, or `test/upr-fvx-cfru-dpe-starter-held-items-reload-smoke` to move to Starter Held Items.

Goal: decide whether Consumable/Sensible/Highest-Level Trainer Held Item filter options need separate coverage before moving to Starter Held Items.

Keep out of scope: Wild Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer work.

Required checks for any next smoke: save/log/output/reload success, class/preserve counters `0`, no invalid/unloaded/fallback/placeholder writes, and cross-scope isolation.

# 2026-05-15 - Next: Regular Trainer Held Items smoke

Recommended next branch: `test/upr-fvx-cfru-dpe-trainer-held-items-regular-reload-smoke`.

Goal: test Regular Trainer Held Items only, after Diagnose 142 confirmed Important Trainer Held Items reload stability.

Keep out of scope: Boss/Important expansion beyond the selected class, Consumable/Sensible/Highest-Level filters, Starter Held Items, Wild Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer work.

Required checks: save/log/output/reload success, Regular Trainer held item reload mismatches 0, Boss/Important/shouldNotGetBuffs preserve counters 0, no invalid/unloaded/fallback/placeholder writes, and Wild/Starter/Field/Pickup/Shop isolation.

# 2026-05-15 - Next: Important Trainer Held Items smoke

Recommended next branch: `test/upr-fvx-cfru-dpe-trainer-held-items-important-reload-smoke`.

Goal: test Important Trainer Held Items only, after Diagnose 141 confirmed Boss Trainer Held Items reload stability.

Keep out of scope: Boss/Regular expansion beyond the selected class, Consumable/Sensible/Highest-Level filters, Starter Held Items, Wild Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer work.

Required checks: save/log/output/reload success, Important Trainer held item reload mismatches 0, Boss/Regular/shouldNotGetBuffs preserve counters 0, no invalid/unloaded/fallback/placeholder writes, and Wild/Starter/Field/Pickup/Shop isolation.

# 2026-05-15 - Next: Trainer Held Items scope

Recommended next branch: `analysis/upr-fvx-cfru-dpe-trainer-held-items-scope-plan` or, if no extra planning block is needed, `test/upr-fvx-cfru-dpe-trainer-held-items-boss-reload-smoke`.

Goal: move from completed Wild/Encounter Held Items coverage to Trainer Held Items, starting with a narrow Boss Trainers-only scope without Consumable/Sensible/Highest-Level filters.

Keep out of scope: Starter Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer work.

Required checks for a smoke: save/log/output/reload success, trainer held item reload mismatches 0, preserve `shouldNotGetBuffs`, no invalid/unloaded/fallback/placeholder writes, and Wild/Starter/Field/Pickup/Shop isolation.

# 2026-05-15 - Next: Wild Held Items Ban Bad smoke

Recommended next branch: `test/upr-fvx-cfru-dpe-wild-held-items-ban-bad-reload-smoke`.

Goal: test Wild/Encounter Held Items with `banBadRandomWildPokemonHeldItems=true` only, after Diagnose 139 confirmed the no-Ban-Bad Wild/Encounter writer reloads with `wildHeldItemReloadMismatches=0`.

Keep out of scope: Trainer Held Items, Starter Held Items, Field Items, Pickup, Shops and all non-Held-Item randomizer work.

Required checks remain: save/log/output/reload success, no invalid/unloaded/fallback/placeholder writes, `badWildHeldItemWrites=0`, and scope isolation for Trainer/Starter/Field/Pickup/Shop.

# Next Steps Update - 2026-05-15 - Wild/Encounter Held Items smoke next

Aktueller Fokus:

- Diagnose 138 confirms read-only Held Items candidate structure for Wild/Encounter, Trainer and Starter paths.
- Wild/Encounter Held Items are the first recommended write/reload smoke because the Species/BaseStats structure is readable and should be tested before Trainer or Starter Held Items.
- Fallback/placeholder held items exist in the current read-only inventory and must be measured as write-safety counters.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-wild-encounter-held-items-reload-smoke`

Ziel des Folgeblocks:

- Test only Wild/Encounter Held Items without Ban Bad.
- Keep Trainer Held Items, Starter Held Items, Field Items, Pickup, Shops and all other randomizer scopes disabled.

# Next Steps Update - 2026-05-15 - Held Items diagnostics next

Aktueller Fokus:

- Diagnose 137 plans Held Items as a separate scope after the tested Shop Items scope was closed by Diagnose 136.
- Held Items are split into Wild/Encounter, Trainer and Starter subscopes.
- No Held-Item feature is promoted by the plan; a read-only candidate diagnostic is required before any Held-Items write smoke.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-held-items-scope-diagnostics`

Ziel des Folgeblocks:

- Read-only Held-Items candidate diagnostic for Species/BaseStats held items, TrainerPokemon held items and Starter held items.
- No Field Items, Pickup, Shops, Trainer Randomization, Wild Randomization, Evolution, Learnset, TM/HM/Tutor, Move, Ability, TypeChart, Palette, Graphics or Text/Menu work.

# Next Steps Update - 2026-05-15 - Shop Items scope closed

Aktueller Fokus:

- Diagnose 136 closes the tested Shop Items scope after the Balance Prices + Cheap Rare Candies combination passed reload.
- FVX-ITEM-005, FVX-ITEM-006, the individually tested FVX-ITEM-007 Ban flags, the individually tested FVX-ITEM-008 Guarantee flags, and FVX-ITEM-009 individual plus combination price/Rare-Candy paths are GUI-compatible in the tested Shop-only CFRU/DPE Gen9-BPRE scope.
- Ban combinations and Evolution+X combination remain optional regression follow-ups, not blockers for closing the tested Shop scope.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-held-items-scope-diagnostics-plan`

Ziel des Folgeblocks:

- Held Items als naechsten separaten Item-writer Scope read-only planen.
- Keine Shops, Field Items, Pickup, Encounter/Trainer/Starter Held Items-Ausweitung ohne eigene Scope-Trennung, keine TM/HM/Tutor/Learnset-, Wild-, Trainer-, Evolution-, Text/Menu-, Palette/Graphics-, MoveData/MoveNames- oder TypeChart-Arbeit.

# Next step - 2026-05-15

- Minimal decision: either run a narrow Balance Prices + Cheap Rare Candies combination smoke or close the current Shop Items scope.
- Do not treat the two individual FVX-ITEM-009 passes as automatic combination coverage.
- Keep Ban combinations, Evolution+X combination, Field Items, Pickup and Held Items separate unless explicitly scoped.

# Next step - 2026-05-15

- Minimal next branch: `test/upr-fvx-cfru-dpe-shop-cheap-rare-candies-reload-smoke`.
- Scope: Shop-only Cheap Rare Candies with `ShopItemsMod.UNCHANGED`, `balanceShopPrices=false`, `addCheapRareCandiesToShops=true`; no Bans, no Guarantees, no Field/Pickup/Held Items.
- Measure Shop-list growth, Rare Candy price reload, terminators, skipped-Shop policy, and foreign-scope stability.

# Next step - 2026-05-15

- Recommended next branch: `test/upr-fvx-cfru-dpe-shop-balance-prices-reload-smoke`.
- Scope: Shop-only Balance Shop Prices with `ShopItemsMod.UNCHANGED`, no Cheap Rare Candies, no Ban combinations, no Guarantee combination, no Field/Pickup/Held Items.
- Measure price table read/write/reload stability before any Rare-Candy Shop-list growth smoke.

# Next step - 2026-05-15

- Minimal decision: either run a narrow Evolution+X combination smoke for FVX-ITEM-008 or move to the FVX-ITEM-009 prices/Cheap Rare Candies scope plan.
- Do not treat the individual Guarantee Evolution and Guarantee X passes as automatic combination coverage.
- Keep Ban combinations and price/Rare-Candy logic separate unless explicitly scoped.

# Next step - 2026-05-15

- Minimal next step: run a Shop-only Guarantee X Items Write/Reload-Smoke for FVX-ITEM-008 if the same candidate source and safety constraints are explicitly released.
- Do not combine Guarantee Evolution + X until both single-feature smokes are reload-stable.
- Keep FVX-ITEM-009 Balance Shop Prices/Cheap Rare Candies separate.

# 2026-05-15 - Naechster Schritt nach Diagnose 130

- Empfohlen: `test/upr-fvx-cfru-dpe-shop-guarantee-evolution-items-reload-smoke`.
- Scope: nur `ShopItemsMod.RANDOM + guaranteeEvolutionItems=true`; keine Guarantee X Items, keine Ban-Kombinationen, keine Preis- oder Cheap-Rare-Candy-Optionen.
- Pflicht: MainGame-Special-Placement, SkipShop-Preserve, Laengen/Terminatoren, Reload und Preis/Field/Pickup/Held-Fremdscopes messen.

# 2026-05-15 - Naechster Schritt nach Diagnose 129

- Entscheiden, ob `FVX-ITEM-007` Ban-Kombinationsdeckung braucht oder ob direkt `FVX-ITEM-008 Guarantee Evolution/X Items` geplant wird.
- Wenn Kombinationen getestet werden: nur nach separater Scope-Entscheidung und ohne Preis/Rare-Candy-Optionen.
- Nicht ausweiten auf `FVX-ITEM-009`, Field Items, Pickup oder Held Items.

# 2026-05-15 - Naechster Schritt nach Diagnose 128

- Empfohlen: Shop Random + Ban OP als separaten Subscope planen oder smoken.
- Voraussetzung: OP-Shop-Item-Pool bleibt klar klassifizierbar und getrennt von Ban Bad/Regular.
- Nicht ausweiten auf Ban-Kombinationen, Guarantee Evolution/X Items, Preise, Cheap Rare Candies, Field Items, Pickup oder Held Items.

# 2026-05-15 - Naechster Schritt nach Diagnose 127

- Empfohlen: Shop Random + Ban Regular als separaten Subscope planen oder smoken.
- Voraussetzung: Regular-Shop-Item-Pool bleibt klar getrennt von Ban Bad und OP-Ban.
- Nicht ausweiten auf OP-Ban-Kombinationen, Guarantee Evolution/X Items, Preise, Cheap Rare Candies, Field Items, Pickup oder Held Items.

# Next Steps Update - 2026-05-15 - Shop Random Ban Bad smoke next

Aktueller Fokus:

- Diagnose 126 plans `FVX-ITEM-007 Shop Item Bans` as a Shop-only sub-scope.
- Ban flags act only in `ShopItemsMod.RANDOM` through `ItemRandomizer.randomizeShopItems()` / `setupPossible()`.
- First recommended Ban test is Ban Bad only because Diagnose 125 already provides `allowedShopItemPoolSize=536` and `nonBadShopItemPoolSize=485`.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-shop-items-random-ban-bad-reload-smoke`

Ziel des Folgeblocks:

- Run only Shop Random + `banBadRandomShopItems=true`.
- Keep `banRegularShopItems=false`, `banOPShopItems=false`, Guarantee Evolution/X Items, Balance Prices, Cheap Rare Candies, Field Items, Pickup and Held Items out of scope.
- Required focus metrics: save/log/output/reload, `shopItemReloadMismatches=0`, skipped-shop preservation, `badShopItemWrites=0`, `banBadShopItemPoolCandidates=51`, price unchanged and foreign scopes unchanged.

# Next Steps Update - 2026-05-15 - Shop Item Bans next

Aktueller Fokus:

- Diagnose 125 confirms `FVX-ITEM-006 Shop Items Random` as reload-stable in the Shop-only CFRU/DPE Gen9-BPRE scope.
- Stable criteria: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `shopItemReloadMismatches=0`, skipped-shop mismatches `0`, price reload mismatches `0`, and Field/Pickup/Held scope changes `false`.
- `FVX-ITEM-007..009` remain separate and are not upgraded by the Random smoke.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-shop-item-bans-scope-plan`

Ziel des Folgeblocks:

- Plan `FVX-ITEM-007 Shop Item Bans` as the next Shop-only sub-scope.
- Keep Guarantee Evolution/X Items, Balance Prices, Cheap Rare Candies, Field Items, Pickup and Held Items out of scope.
- Decide whether the next executable smoke should test Ban Bad first, or split Bad/Regular/OP ban policies into separate smokes.

# Next Steps Update - 2026-05-15 - Shop Random smoke next

Aktueller Fokus:

- Diagnose 124 confirms `FVX-ITEM-005 Shop Items Shuffle` as reload-stable in the Shop-only CFRU/DPE Gen9-BPRE scope.
- Stable criteria: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `reloadSuccessful=true`, `shopItemReloadMismatches=0`, skipped-shop mismatches `0`, price reload mismatches `0`, and Field/Pickup/Held scope changes `false`.
- `FVX-ITEM-006..009` remain separate and are not upgraded by the Shuffle smoke.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-shop-items-random-reload-smoke`

Ziel des Folgeblocks:

- Run only `FVX-ITEM-006 Shop Items Random` as a Shop-only Write/Reload-Smoke.
- Keep Shop Bans, Guarantee Evolution/X Items, Balance Prices, Cheap Rare Candies, Field Items, Pickup and Held Items out of scope.
- Reuse the Diagnose-123/124 structure criteria: counts, lengths, terminators, skipped shops, special policy, prices and foreign scopes must stay stable.

# Next Steps Update - 2026-05-15 - Shop Shuffle smoke next

Aktueller Fokus:

- Diagnose 123 confirms a stable read-only Shop structure for the approved CFRU/DPE Gen9-BPRE candidate.
- Shop metrics are stable enough for the next minimal write/reload test: `shopScanSuccessful=true`, `shopCount=23`, `shopItemsTotal=157`, `terminatorModelStable=true`, `shopLengthMismatch=0`, invalid/unloaded/fallback/placeholder Shop items all `0`.
- `dataRewriterOrRepointingRisk=true` remains a required Smoke criterion because `Gen3RomHandler.setShops(...)` uses `DataRewriter<Shop>`.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-shop-items-shuffle-reload-smoke`

Ziel des Folgeblocks:

- Run only `FVX-ITEM-005 Shop Items Shuffle` as a Shop-only Write/Reload-Smoke.
- Prove stable Shop count, item total, min/max length, terminators, preserved skipped shops, Special/MainGame policy and no price, Field, Pickup or Held scope changes.
- Do not include Shop Random, Shop Bans, Guarantee Evolution/X Items, Balance Prices, Cheap Rare Candies, Field Items, Pickup, Held Items, TM/HM/Tutor/Learnset, Trainer, Wild, Evolution, Text/Menu, Palette/Graphics, MoveData/MoveNames or TypeChart.

# Next Steps Update - 2026-05-15 - Shop Items candidate needed

Aktueller Fokus:

- Diagnose 122 is blocked/preflight because no explicitly approved local CFRU/DPE Gen9-BPRE candidate source was provided for the Shop read-only scan.
- The codepath model remains valid: Shops are pointer-list, terminator, length, `DataRewriter`/repointing and price-adjacent scope, separate from Field Items, Pickup and Held Items.
- Do not run Shop Shuffle, Random, Ban, Guarantee or Price smokes before a successful read-only Shop candidate diagnostic.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-candidate`

Ziel des Folgeblocks:

- Use an explicitly approved local CFRU/DPE Gen9-BPRE candidate source.
- Read-only scan only Shops and report aggregated `candidateLoaded`, `shopScanSuccessful`, `shopCount`, `mainGameShopCount`, `skippedShopCount`, `specialShopCount`, `emptyShopCount`, `shopItemsTotal`, min/max length, terminator stability, item-safety counters and price-table untouched status.
- Keep Field Items, Pickup, Held Items, prices, Shop writes, builds, Randomizer writes/saves and private artefact documentation out of scope.

# Next Steps Update - 2026-05-15 - Shop Items scope diagnostics next

Aktueller Fokus:

- Diagnose 121 confirms Shops as the next separate CFRU/DPE Gen9-BPRE Item writer scope after Field Items and Pickup.
- `FVX-ITEM-005..009` remain Shop-only and are not upgraded by Field Items, Pickup or Held Item results.
- `Gen3RomHandler.setShops(...)` uses `DataRewriter<Shop>`, so Shop writes must treat terminators, lengths, pointers, skipped/special/main-game policy and price fields as explicit reload criteria.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics`

Ziel des Folgeblocks:

- Run a sanitized read-only Shop candidate diagnostic.
- Report only aggregated counters: `candidateLoaded`, `shopScanSuccessful`, `shopCount`, `mainGameShopCount`, `skippedShopCount`, `specialShopCount`, item counts, terminator/length mismatches, invalid/unloaded/fallback/placeholder/bad items, skipped-shop preservation expectations and price-table readability.
- Do not run a Shop write smoke yet and keep Field Items, Pickup, Held Items, TM/HM/Tutor/Learnset, Trainer, Wild, Evolution, Text/Menu, Palette/Graphics, MoveData/MoveNames and TypeChart out of scope.

# Next Steps Update - 2026-05-15 - Shops-only scope next

Current recommended branch:

- `analysis/upr-fvx-cfru-dpe-shop-items-scope-diagnostics-plan`

Goal:

- Plan Shops as the next separate Item writer scope after Field Items and Pickup.
- Keep Field Items, Pickup, Encounter Held Items, Trainer Held Items and Starter Held Items out of the Shop plan.
- Start read-only: identify Shop item lists, terminators, lengths, special shops, price handling, bad-item policy and CFRU/DPE Gen9-BPRE risks before any writer smoke.

Current Pickup status:

- `FVX-ITEM-010 Pickup Items Random / Ban Bad Items` is `GUI-kompatibel` for the tested Pickup-only Random scope with `banBadRandomPickupItems=false` and `true`.
- UPR-FVX remains pinned to `a2373888ad17145f270ebf6ff17303af41aa86eb`.

# Next Steps Update - 2026-05-15 - Pickup Items Ban Bad smoke next

Current recommended branch:

- `test/upr-fvx-cfru-dpe-pickup-items-random-ban-bad-reload-smoke`

Goal:

- Run a sanitized Pickup-only Write/Reload-Smoke for `FVX-ITEM-010 Pickup Items Random` with `Settings.PickupItemsMod.RANDOM` and `banBadRandomPickupItems=true`.
- Reuse UPR-FVX `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- Keep scope limited to Pickup Items; no Field Items, Shops, Held Items, TM/HM/Tutor/Learnset, Scriptparser, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution or Text/Menu work.

Expected focus metrics:

- Preserve Diagnose 118 reload baseline: `pickupItemsTotalReload=16`, `pickupItemReloadMismatches=0`, `pickupProbabilityMismatches=0`, `pickupReloadLocatorRegression=false`.
- Add Ban-Bad assertions: `badPickupItemWrites=0`, `pickupBadItemPoolCandidates=51`, `pickupBadItemPoolExcluded=51`, `pickupPoolNonBadSize=485`.
- Confirm `fieldItemScopeChanged=false`, `shopItemScopeChanged=false`, and `heldItemScopeChanged=false`.

# Next Steps Update - 2026-05-15 - Pickup Ban Bad next

Aktueller Fokus:

- Diagnose 118 fixes and verifies the Pickup reload locator for `FVX-ITEM-010 Pickup Items Random` with `banBadRandomPickupItems=false`.
- `FVX-ITEM-010 Pickup Items Random` is now GUI-compatible only in that narrow no-Ban-Bad Pickup-only scope.
- Pickup Ban Bad remains untested and separate.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-pickup-items-ban-bad-scope-plan`

Ziel des Folgeblocks:

- Read-only planen, wie Pickup Ban Bad fuer `FVX-ITEM-010` getestet werden soll.
- Danach erst einen Pickup-only Random smoke mit `banBadRandomPickupItems=true` vorbereiten.
- Keine Field Items, Shops, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu oder Scriptparser-Arbeit.

# Next Steps Update - 2026-05-15 - Pickup reload locator fix next

Aktueller Fokus:

- Diagnose 116 blocks `FVX-ITEM-010 Pickup Items Random` after successful save/log/output/reopen because fresh reload cannot locate the Pickup table.
- Diagnose 117 narrows the likely cause to the content-based `PickupTableStartLocator`: the current handler keeps a cached table offset after write, but a fresh handler searches for the old item-ID pattern, which Pickup Random has changed.
- `FVX-ITEM-010` remains `Write modelliert` / reload-blocked.
- Pickup Ban Bad remains blocked until Random without Ban Bad reloads stably.

Naechster empfohlener Minimalblock:

- `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`

Ziel des Folgeblocks:

- Minimalen UPR-FVX-Fix fuer eine reloadstabile Pickup-Table-Lokalisierung vorbereiten.
- Bevorzugt eine stabile ROM-Entry-Adresse oder nicht item-inhaltsabhaengige Referenz im sicheren CFRU/DPE-/FRLG-Gate nutzen.
- Den bestehenden `PickupTableStartLocator` nur als klassischen Fallback erhalten.
- Danach Pickup-only Random-Smoke mit `banBadRandomPickupItems=false` wiederholen.
- Keine Pickup Ban Bad, Field Items, Shops, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu oder Scriptparser-Arbeit.

# Next Steps Update - 2026-05-15 - Pickup Items reload locator blocker

Aktueller Fokus:

- Diagnose 116 blockiert `FVX-ITEM-010 Pickup Items Random` nach erfolgreichem Save/Log/Output beim Reload-Locator.
- Der frische Reload findet die Pickup-Tabelle nicht mehr: `pickupLocatorSuccessful=false`, `pickupItemsTotalReload=0`.
- Vor und direkt nach Write bleibt der aktive Handler stabil: `pickupItemsTotalBefore=16`, `pickupItemsTotalAfter=16`.
- Field Items, Shops und Held Items blieben unveraendert.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-pickup-items-reload-locator-blocker-plan`

Ziel des Folgeblocks:

- Read-only klaeren, warum `PickupTableStartLocator` nach `PickupItemsMod.RANDOM` nicht mehr greift.
- Einen engen spaeteren Fix-Scope fuer `Gen3RomHandler.getPickupItems()` / `setPickupItems(...)` oder einen privaten Pickup-Table-Helper planen.
- Keine Ban-Bad-Pickup-Arbeit, keine Field Items, keine Shops, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Arbeit.

# Next Steps Update - 2026-05-15 - Pickup Items random smoke next

Aktueller Fokus:

- Diagnose 115 hat Pickup Items read-only klassifiziert.
- Locator, Count, Entry-Size und Probability-Modell sind fuer den Kandidaten stabil: `pickupLocatorSuccessful=true`, `pickupItemsTotal=16`, `pickupExpectedCount=16`, `pickupEntrySize=4`, `pickupProbabilityModelStable=true`.
- Item-ID-Sicherheit ist fuer den aktuellen Pickup-Scope stabil: `pickupInvalidItemIds=0`, `pickupUnloadedItemIds=0`, `pickupFallbackItems=0`, `pickupPlaceholderItems=0`.
- Ban Bad bleibt separat, weil `pickupBadItemPoolCandidates=51` und `pickupBadItemPoolExcluded=51` eine eigene Poolfilter-Wirkung zeigen.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-pickup-items-random-reload-smoke`

Ziel des Folgeblocks:

- Nur `FVX-ITEM-010 Pickup Items Random` mit `banBadRandomPickupItems=false` als Write-/Reload-Smoke testen.
- Erwartet: Save/Log/Output/Reload true, `pickupItemsTotalBefore/After/Reload=16`, `pickupItemReloadMismatches=0`, Tabellenlaenge und Probability-Modell stabil, keine invalid/unloaded/fallback/placeholder Writes.
- Keine Field-Items-Arbeit, keine Shops, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Arbeit.

# Next Steps Update - 2026-05-15 - Pickup Items diagnostics next

Aktueller Fokus:

- Field Items `FVX-ITEM-001..004` sind im getesteten engen Field-Items-only Scope abgeschlossen.
- Pickup Items sind als naechster getrennter Item-Writer-Scope geplant.
- Diagnose 114 empfiehlt zuerst eine read-only Pickup-Kandidatendiagnose, bevor ein Write-/Reload-Smoke gestartet wird.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics`

Ziel des Folgeblocks:

- Nur Pickup Items read-only klassifizieren: Locator, Tabellenlaenge, Entry-Size, Probability-Modell, Common/Rare-Hinweise, valide/geladene Item-IDs, Bad-/Fallback-/Placeholder-/TM-Pool-Sicherheit.
- Keine Pickup-Write-/Randomizer-Ausfuehrung, kein Build, keine Codeaenderung.
- Keine Field-Items-Arbeit, keine Shops, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Arbeit.

# Next Steps Update - 2026-05-15 - Field Items complete in tested scope

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` ist im engen allowed-slot Scope `GUI-kompatibel`.
- `FVX-ITEM-002 Field Items Random` ist im engen Field-Items-only Scope `GUI-kompatibel`, inklusive `banBadRandomFieldItems=true` fuer `FieldItemsMod.RANDOM`.
- `FVX-ITEM-003 Field Items Random even distribution` ist im engen Field-Items-only Scope `GUI-kompatibel`, inklusive `banBadRandomFieldItems=true` fuer `FieldItemsMod.RANDOM_EVEN`.
- `FVX-ITEM-004 Field Items Ban Bad Items` ist fuer Field Items Random und Random Even `GUI-kompatibel`.
- Shops, Pickup und Held Items bleiben nicht hochgestuft und muessen getrennt geplant werden.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics-plan`

Ziel des Folgeblocks:

- Pickup als separaten Item-Writer-Scope read-only planen.
- Keine Field-Items-Nacharbeit, keine Shops, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Arbeit.

# Next Steps Update - 2026-05-15 - Field Items Random Even Ban Bad smoke next

Aktueller Fokus:

- Diagnose 112 confirms a Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=true`.
- Save/log/output/reload succeeded, `fieldItemReloadMismatches=0`, Required Field TMs stayed complete, and `badFieldItemWrites=0`.
- `FVX-ITEM-004` is tested for `FieldItemsMod.RANDOM`, but not fully GUI-compatible because Random Even + Ban Bad remains unsmoked and the 75er Ban-Bad baseline from Diagnose 111 was not reproduced in this run.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke`: sanitized Field-Items-only smoke for `FVX-ITEM-003 Field Items Random even distribution` with `banBadRandomFieldItems=true`.


Aktueller Fokus:

- Diagnose 111 plans `FVX-ITEM-004 Field Items Ban Bad Items` read-only.
- `banBadRandomFieldItems` affects the Non-TM Field-Items random pool only; TM slots and Required Field TMs stay in the separate TM path.
- Baseline Ban-Bad count from Diagnose 100: `badFieldItems=75` / `badItemBanCandidates=75`.
- `FVX-ITEM-004` remains `Write modelliert` until at least the first Ban-Bad reload smoke passes.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `test/upr-fvx-cfru-dpe-field-items-random-ban-bad-reload-smoke`: sanitized Field-Items-only smoke for `FVX-ITEM-002 Field Items Random` with `banBadRandomFieldItems=true`; keep Random Even + Ban Bad separate afterward.

# Next Steps Update - 2026-05-15 - Field Items Ban Bad scope plan next

Aktueller Fokus:

- Diagnose 110 confirms `FVX-ITEM-003 Field Items Random even distribution` as `GUI-kompatibel` in the narrow Field-Items-only scope with `banBadRandomFieldItems=false`.
- Confirmed counters include `fieldItemReloadMismatches=0`, `apiTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`, `randomTmPoolDeficit=0`, and `requiredFieldTMMissingAfter=0`.
- `FVX-ITEM-004 Field Items Ban Bad Items` remains `Write modelliert` and should be planned separately before activation.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `analysis/upr-fvx-cfru-dpe-field-items-ban-bad-scope-plan`: read-only plan for `FVX-ITEM-004 Field Items Ban Bad Items`, preserving the same allowed-slot, TM/Non-TM, Required-TM and API-TM-slot criteria.

# Next Steps Update - 2026-05-15 - Field Items Random Even smoke next

Aktueller Fokus:

- Diagnose 109 confirms `FVX-ITEM-002 Field Items Random` as `GUI-kompatibel` in the narrow Field-Items-only scope with `banBadRandomFieldItems=false`.
- Confirmed counters include `fieldItemReloadMismatches=0`, `apiTmFieldItemSlots=28`, `rawApiTmSlotAlignmentMismatches=0`, `randomTmPoolDeficit=0`, and `requiredFieldTMMissingAfter=0`.
- `FVX-ITEM-003 Field Items Random even distribution` remains `Write modelliert` and should be tested separately next.
- `FVX-ITEM-004 Ban Bad Items` remains separate and inactive.

Nicht ausweiten:

- No Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu or Scriptparser work.

Naechster Block:

- `test/upr-fvx-cfru-dpe-field-items-random-even-reload-smoke`: sanitized Field-Items-only smoke for `FVX-ITEM-003` without Ban Bad Items, preserving the same allowed-slot, TM/Non-TM, Required-TM and API-TM-slot criteria.

# Next Steps Update - 2026-05-15 - Field Items API TM-slot reload smoke next

Aktueller Fokus:

- UPR-FVX PR #37 prepares the narrow CFRU/DPE Field-Items API TM-slot scope fix.
- Workspace pins `02_external/upr-fvx` to `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- `FVX-ITEM-002` remains below GUI-compatible until a separate Field-Items-only reload smoke confirms `randomTmNeededSlots=28`, `apiTmFieldItemSlots=28`, and `fieldItemReloadMismatches=0`.

Empfohlener naechster Branch:

- `test/upr-fvx-cfru-dpe-field-items-api-tm-slot-reload-smoke`

Ziel:

- Run a sanitized Field-Items-only `FVX-ITEM-002 Field Items Random` Write-/Reload-Smoke with `banBadRandomFieldItems=false` on UPR-FVX `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Keep Random Even, Ban Bad Items, Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Scriptparser, Palette, MoveData, Trainer, Wild, Evolution and Text/Menu out of scope.

# Next Steps Update - 2026-05-15 - Field Items API TM-slot scope fix next

Aktueller Fokus:

- Diagnose 107 narrows the `FVX-ITEM-002 Field Items Random` blocker to the Field-Items API TM-slot scope.
- Raw diagnostics show `tmFieldItemSlots=28` and `requiredFieldTMsTotal=24`; `getFieldItems()` currently exposes `0` TM slots because it filters on `Item::isAllowed`.
- Do not proceed to `FVX-ITEM-003` or `FVX-ITEM-004` until `FVX-ITEM-002` reloads successfully.

Empfohlener naechster Branch:

- `compat/upr-fvx-cfru-dpe-field-items-api-tm-slot-scope-fix`

Ziel:

- Prepare a minimal CFRU/DPE-gated Field-Items API TM-slot scope fix for `FVX-ITEM-002` with `banBadRandomFieldItems=false`.
- Do not make TMs globally allowed and do not expand Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even, Ban Bad Items, Scriptparser, Palette, MoveData, Trainer, Wild, Evolution or Text/Menu.

# Next Steps Update - 2026-05-15 - Field Items Random API TM-slot scope plan next

Aktueller Fokus:

- Diagnose 106 blocks `FVX-ITEM-002 Field Items Random` after PR #36.
- The Unique-TM-Filler pool is sufficient: `randomTmUniquePoolSize=50`, `randomTmFillerAvailable=26`, `randomTmPoolDeficit=0`.
- Active blocker is now the `getFieldItems()` API TM-slot scope: raw diagnostics show `tmFieldItemSlots=28`, but Randomizer API metrics show `randomTmNeededSlots=0` / `randomTmCurrentSlots=0`.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-field-items-random-api-tm-slot-scope-plan`

Ziel des Folgeblocks:

- Read-only klaeren, warum der Gen3/CFRU-DPE Field-Items-API-Scope keine TM-Field-Item-Slots an `ItemRandomizer.randomizeTMFieldItems(...)` uebergibt.
- Weiterhin keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Random Even Distribution und keine Ban-Bad-Items-Umsetzung.

# Next Steps Update - 2026-05-15 - Field Items Random TM-pool reload smoke next

Aktueller Fokus:

- UPR-FVX PR #36 contains the narrow `FVX-ITEM-002 Field Items Random` TM-pool fix.
- Workspace pins `02_external/upr-fvx` to `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd` in this branch.
- `FVX-ITEM-002` remains pending until a Field-Items-only Write-/Reload-Smoke confirms the fix.

Naechster empfohlener Minimalblock nach Merge:

- `test/upr-fvx-cfru-dpe-field-items-random-tm-pool-reload-smoke`

Ziel des Folgeblocks:

- `FVX-ITEM-002 Field Items Random` mit `banBadRandomFieldItems=false` fachlich erneut testen.
- Erwartete TM-Pool-Metriken: `randomTmNeededSlots=28`, `randomTmRequiredTotal=24`, `randomTmFillerNeeded=4`, `randomTmPoolDeficit=0`, `randomTmResultSize=28`, `randomTmResultUniqueSize=28`.
- Erwartete Reload-Metriken: `saveSuccessful=true`, `reloadSuccessful=true`, `fieldItemReloadMismatches=0`, `requiredFieldTMMissingAfter=0`, `disallowedFieldItemWrites=0`, `scriptPatternExpansion=0`.
- Weiterhin keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Random Even Distribution und keine Ban-Bad-Items-Umsetzung.

# Next Steps Update - 2026-05-15 - Field Items Random TM-pool fix next

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` bleibt `GUI-kompatibel` im engen allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random` bleibt blockiert durch den TM-Field-Items-Random-Pool.
- Diagnose 104 empfiehlt einen engen Fix nur fuer `ItemRandomizer.randomizeTMFieldItems(...)` bzw. einen kleinen privaten Helper.

Naechster empfohlener Minimalblock:

- `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix`

Ziel des Folgeblocks:

- Minimalen UPR-FVX-Fix fuer `FVX-ITEM-002` vorbereiten.
- Sanitisiert pruefen: `randomTmNeededSlots=28`, `randomTmRequiredTotal=24`, `randomTmCandidatePoolSize >= 28`, `randomTmPoolDeficit=0`.
- Danach Field-Items-Random Write-/Reload-Smoke wiederholen.
- Keine Shops, kein Pickup, keine Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Random Even Distribution, keine Ban-Bad-Items-Umsetzung.

# Next Steps Update - 2026-05-15 - Field Items Random TM-pool blocker next

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` bleibt durch Diagnose 102 `GUI-kompatibel` im engen allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random` ist durch Diagnose 103 blockiert: Save bricht mit `RandomizationException` ab, kein Output-ROM, kein Reload.
- `FVX-ITEM-003 Field Items Random even distribution` und `FVX-ITEM-004 Ban Bad Items` bleiben `Write modelliert`.

Naechster empfohlener Minimalblock:

- `analysis/upr-fvx-cfru-dpe-field-items-random-tm-pool-blocker-plan`

Ziel des Folgeblocks:

- Read-only den Random-TM-Field-Items-Pool und Required-TM-Policy untersuchen.
- Klaeren, ob ein spaeterer Fix eng auf `FVX-ITEM-002` Field Items Random begrenzt werden kann.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution und Text/Menu bleiben ausserhalb.

# Next Steps Update - 2026-05-15 - Field Items Random smoke next

Aktueller Fokus:

- `FVX-ITEM-001 Field Items Shuffle` ist durch Diagnose 102 im engen allowed-slot Scope `GUI-kompatibel`.
- `FVX-ITEM-002 Field Items Random`, `FVX-ITEM-003 Field Items Random even distribution` und `FVX-ITEM-004 Ban Bad Items` bleiben `Write modelliert`.
- Shops, Pickup und Held Items bleiben getrennte Writer-Scope-Bloecke.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-field-items-random-reload-smoke`

Ziel des Folgeblocks:

- Nur `FVX-ITEM-002 Field Items Random` testen.
- `banBadRandomFieldItems=false` lassen; `FVX-ITEM-004` separat spaeter testen.
- Dieselben allowed-slot-, TM-/Non-TM-, Required-TM- und preserve-only-Metriken wie Diagnose 102 pruefen.

# Next Steps Update - 2026-05-14 - Field Items allowed-slot smoke next

Aktueller Fokus:

- `FVX-ITEM-001..004` Field Items bleiben `Write modelliert`.
- Diagnose 101 bestaetigt read-only, dass der bestehende Gen3 Field-Items-Writer bereits nur allowed Slots schreibt.
- Ein fachlicher Write-/Reload-Smoke wurde nicht ausgefuehrt, weil fuer diesen Block keine explizite lokale Kandidatenfreigabe fuer einen ROM-Write vorlag.

Naechster empfohlener Minimalblock:

- `test/upr-fvx-cfru-dpe-field-items-allowed-slot-reload-smoke`

Ziel des Folgeblocks:

- Explizit freigegebenen CFRU/DPE Gen9-BPRE-Kandidaten verwenden.
- Nur `FVX-ITEM-001 Field Items Shuffle` als ersten Field-Items-Carrier pruefen.
- Erwartet: `fieldItemsTotalBefore=339`, `fieldItemsTotalAfter=339`, `fieldItemsTotalReload=339`, `fieldItemReloadMismatches=0`, TM-/Non-TM-Mismatches `0`, `requiredFieldTMMissingAfter=0`, `disallowedFieldItemWrites=0`, `scriptPatternExpansion=0`.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer, Wild, Evolution und Text/Menu bleiben ausserhalb.

# Next Steps Update - 2026-05-14 - Field Items guarded write/smoke

Recommended next block:

`compat/upr-fvx-cfru-dpe-field-items-allowed-slot-write-guard`

Goal: implement and smoke a narrow Field-Items-only guard for allowed slots, preserving disallowed/progression-sensitive/key-system slots, keeping TM slots as TMs and Non-TM slots as Non-TMs, and maintaining `requiredFieldTMMissingAfter=0`. Keep Shops, Pickup, held items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution and Text/Menu out of scope.

# Next Steps Update - 2026-05-14 - Field Items diagnostics candidate needed

Recommended next block only after an explicitly approved local CFRU/DPE Gen9-BPRE candidate is available:

`test/upr-fvx-cfru-dpe-field-items-scope-diagnostics-candidate`

Goal: run the sanitized Field-Items-only read-only diagnostic from protocol 098/099 and report only aggregated counters for visible Itemballs, Hidden Items/Signposts, TM/Non-TM slots, Required Field TMs, progression-sensitive items, bad items, modern item IDs and invalid/unloaded item IDs. Keep Shops, Pickup, held items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution and Text/Menu out of scope.

# Next Steps Update - 2026-05-14 - Field Items diagnostics scope

Recommended next block:

`test/upr-fvx-cfru-dpe-field-items-scope-diagnostics`

Goal: run a sanitized Field-Items-only diagnostic that reports aggregated visible Itemball, Hidden Item/Signpost, TM-slot, Non-TM-slot, Required Field TM, bad-item, modern-item and invalid-item counters. Keep Shops, Pickup, held items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution and Text/Menu out of scope.

# Next Steps - 2026-05-14 Field Items / Shops / Pickup Plan

Aktiver Anschlussblock:

- `analysis/upr-fvx-cfru-dpe-field-items-scope-diagnostics-plan`

Ziel: Field Items als ersten getrennten Item-Writer read-only planen/diagnostizieren. Fokus auf sichtbare Itemballs, Hidden Items, TM-Slots, Required Field TMs, Progression-/Key-/System-Item-Preserve, invalid/fallback Items und Reload-Kriterien.

Entscheidung aus Diagnose 097:

- Field Items, Shops und Pickup nicht gemeinsam fixen.
- Field Items: Map-/Script-/Signpost-Offset-Writer, naechster engster Block.
- Pickup: separater Table-/Locator-/Probability-Scope.
- Shops: separater Shoplisten-/Terminator-/DataRewriter-/Repointing-/Preis-Scope.
- Gemeinsame Item-Pool-Bans sind noetig, aber kein gemeinsamer Writer-Fix.

Grenzen: keine Shops, kein Pickup, keine Encounter Held Items, keine Trainer/Starter Held Items, keine TM/HM/Tutor/Learnset-Ausweitung, keine Palette/Graphics, kein MoveData/MoveNames, kein TypeChart/TypeEffectiveness, keine Trainer/Wild/Evolution/Text/Menu-Umsetzung.

# Next Steps - 2026-05-14 Post-Merge Palette Sync

Aktiver Anschlussblock:

- `analysis/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-plan`

Ziel: Field Items, Shops und Pickup read-only als eigenen P1-Scope planen. Keine Umsetzung, kein Randomizer-Lauf, kein Build und keine Vermischung mit Palette, Graphics, TypeChart, Trainer, Wild, Evolution, Text/Menu, MoveData oder MoveNames.

Post-Merge-Status aus Diagnose 096:

- Workspace PR #140 ist gemerged.
- `FVX-GFX-001` hat den UPR-FVX Guard-Fix aus PR #35/#139, aber der Reload-Smoke ist blockiert.
- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- `candidateSpeciesTotal=0`
- kein fachlicher Palette-Write-/Reload-Smoke
- keine Hochstufung fuer `FVX-GFX-001`
- `FVX-GFX-001`, `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`.

`FVX-GFX-001` wartet auf einen explizit freigegebenen UPR-FVX-ladbaren CFRU/DPE Gen9-BPRE-Kandidaten mit `candidateSpeciesTotal=1439`, bevor ein gleicher Normal-only Single-owner Reload-Smoke erneut sinnvoll ist.

# Next Steps - 2026-05-14 Update

Aktiver Anschlussblock nach Diagnose 096:

- `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke-retry`

Ziel: Den engen `FVX-GFX-001` Normal-only Single-owner Reload-Smoke erst wiederholen, wenn ein explizit freigegebener UPR-FVX-ladbarer CFRU/DPE-Gen9-BPRE-Kandidat verfügbar ist und `candidateSpeciesTotal=1439` erfüllt.

Status aus Diagnose 096:

- `candidateFilesChecked=94`
- `candidateLoaded=false`
- `candidateOpenFailures=2`
- `candidateSpeciesTotalMismatches=92`
- kein fachlicher Palette-Write-/Reload-Smoke
- keine Hochstufung für `FVX-GFX-001`
- `FVX-GFX-002/003/004` bleiben `Write modelliert`

Nicht ausweiten auf Shiny, Shared-Paletten, Graphics/Sprites, TypeChart/TypeEffectiveness, Species-Type-Write, Evolution-Writer, Items, Trainer/Wild, Text/Menu, MoveData oder MoveNames.

# Next Steps

## Aktueller Fokus

CFRU/DPE Palette Normal Single-owner Write Guard Fix ist dokumentiert. Aktuelle Diagnose: `08_tests/randomizer/095_palette_normal_single_owner_write_guard_fix_diagnostics.md`.

`FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel. `FVX-MOVE-005` bleibt getrennt vom MoveData-Byte-Writer-Scope.

Ergebnis aus 090: Der erneute Candidate-Preflight ist blockiert. `candidateFilesChecked=94`, `candidatePreflightSuccessful=false`, `candidateMovesTotal=not available`, `candidateHighestMove=not available`. Es gab keinen fachlichen Name-only fixed-length Reload-Smoke.

Planergebnis aus 091: echte `PokemonPalettesMod.RANDOM`-Randomization ist wegen compressed-data-, shared-pointer-, missing/invalid-pointer-, FreeSpace-/Repointing- und Forme-/Mapping-Risiken noch nicht direkt fixbar.

Diagnoseergebnis aus 093: der sanitisierten read-only Lauf findet `candidateWritablePalettes=385`, aber nur `candidateWritableNormalPalettes=385` und `candidateWritableShinyPalettes=0`. Shared/invalid/missing/decode-failed Paletten bleiben preserve-only.

Planergebnis aus 094: ein spaeterer Fix-/Smoke-Scope ist reviewbar, aber nur fuer Normal-Paletten, die single-owner, dekomprimierbar, gueltig, nicht shared, nicht missing, nicht invalid, nicht decode-failed und nicht cross-kind shared sind. Repointing muss bewusst abgesichert werden.

Fixstand aus 095: UPR-FVX `2697511da9a97df4c29c00dfda8b40e556020489` implementiert den Normal-only-Single-owner-Guard. Kein ROM-/Reload-Smoke wurde in diesem Block ausgefuehrt; `FVX-GFX-001` bleibt bis zum separaten Reload-Smoke `Write modelliert`.

Naechster aktiver Arbeitsblock: `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`.

## Priorisierte naechste Arbeitsbloecke

1. Palette Normal Single-owner Reload-Smoke ausfuehren
   - Empfohlener Branch: `test/upr-fvx-cfru-dpe-palette-normal-single-owner-reload-smoke`.
   - Ziel: den UPR-FVX-Guard-Fix aus 095 fachlich mit einem sanitisierten Reload-Smoke bestaetigen.
   - Erwartet: `normalPaletteWriteCandidates=385`, `normalPaletteWriteAttempts <= 385`, `normalPaletteReloadMismatches=0`, `shinyPaletteWriteAttempts=0`, `sharedPaletteWriteAttempts=0`, `invalidPaletteWriteAttempts=0`, `missingPaletteWriteAttempts=0`, `decodeFailedPaletteWriteAttempts=0`, `crossKindSharedWriteAttempts=0`, `exceptionClass=none`, `stacktrace=none`.
   - Grenzen: keine Shiny-/Shared-/Graphics-/Sprite-, TypeChart-, Species-Type-, Evolution-, Items-, Trainer-, Wild-, Text/Menu- oder MoveData-Arbeit.

2. Palette Randomization Preserve/Repoint Plan halten
   - Diagnose 091 dokumentiert: direkter Fix noch nicht eng genug.
   - `FVX-GFX-001..004` bleiben `Write modelliert`.
   - Spaeterer Fix darf nur single-owner/dekomprimierbare Paletten schreiben oder muss eine vollstaendige Secondary-Pointer-/Shared-Pointer-Policy liefern.

3. Move Names fixed-length Reload-Smoke erst mit eindeutigem Kandidaten wiederholen
   - Empfohlener Branch: `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke-candidate`.
   - Voraussetzung: freigegebener lokaler CFRU/DPE Gen9-BPRE-Kandidat muss mit `moves.total=992` und `991:PsychicNoise` erkennbar sein.
   - Ziel: `FVX-MOVE-005` Name-only im bestehenden Gen3 fixed-length Move-Namen-Pfad pruefen.
   - Kriterien: Save/Log/Output/Reload true, `moves.total=992`, `991:PsychicNoise`, `moveNameReloadMismatches=0`, `moveNameLengthViolations=0`, `moveNameTerminatorPaddingMismatches=0`, keine Description-/Pointer-Aenderung, `exceptionClass=none`, `stacktrace=none`.
   - Grenzen: keine Move Descriptions, keine Pointer-/Repointing- oder Text/Menu-Umsetzung, keine MoveData-Byte-Writer-Aenderung, keine TypeChart/TypeEffectiveness, keine Species-Type-, TM/HM-, Tutor-, Egg-, Learnset-, Palette-, Items-, Trainer-, Wild-, Evolution- oder Graphics-Arbeit.

4. Move Names fixed-length Reload-Smoke Retry-Ergebnis halten
   - Diagnose 089 dokumentiert den blockierten Versuch.
   - Diagnose 090 dokumentiert den blockierten Retry-Preflight mit 94 geprueften lokalen Kandidatendateien und ohne fachliche Smoke-Auswertung.
   - `FVX-MOVE-005` bleibt `Write modelliert`.
   - Keine Feature-Hochstufung ohne stabilen Name-only Reload.

5. Move Names / Descriptions Text/Menu-Scope Plan halten
   - Diagnose 088 dokumentiert `FVX-MOVE-005` als getrennten Text/Menu-Scope.
   - Name-only fixed-length Smoke ist realistisch.
   - Move Descriptions / Text/Menu-Repointing bleibt vorerst zurueckgestellt.

6. MoveData Fairy-Type-Byte-Fix post-merge halten
   - UPR-FVX PR #34 ist gemerged.
   - Workspace PR #129 ist gemerged.
   - Diagnose 087 bestaetigt `FVX-MOVE-004` mit Save/Log/Output/Reload true, `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`, `moves.total=992`, `991:PsychicNoise` und Preserve-Bytes `0` Mismatches.
   - `FVX-MOVE-001/002/003/004/006` sind GUI-kompatibel; `FVX-MOVE-005` bleibt getrennt.

7. MoveData Types Reload-Smoke historisch einordnen
   - Branch: `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke`.
   - Diagnose 086 dokumentiert den Blocker fuer `FVX-MOVE-004`.
   - Save/Log/Output/Reload sind true; `moves.total=992` und `991:PsychicNoise` bleiben stabil.
   - Preserve-Bytes bleiben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
   - Der Blocker ist durch Diagnose 087 behoben.

8. MoveData Power/Accuracy/PP Reload-Smoke halten
   - Branch: `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke`.
   - Diagnose 085 bestaetigt `FVX-MOVE-001`, `FVX-MOVE-002` und `FVX-MOVE-003` mit Save/Log/Output/Reload true und `writeReloadMoveDataMismatches=0`.
   - `powerReloadMismatches=0`, `accuracyReloadMismatches=0`, `ppReloadMismatches=0`.
   - Preserve-Bytes bleiben bytegleich.

9. PRs fuer Wild-Filter-Carrier-Nullslot-Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`.
   - Diagnose 075 und Submodule-Pin reviewen und mergen.

10. PRs fuer Trainer Type Diversity Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`.
   - Diagnose 078 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `TrainerPokemonRandomizer` und den Force-Diverse-Types-/`usedTypes`-Pfad begrenzt.

11. PRs fuer Evolution Same Typing Null-Type Fix reviewen
   - UPR-FVX: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Workspace: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.
   - Diagnose 080 und Submodule-Pin reviewen und mergen.
   - Der Fix bleibt auf `EvolutionRandomizer` und den Same-Typing-/Null-Primary-Type-Scope begrenzt.

12. PR fuer `FVX-TRAIT-018` Similar Strength Normalized Reload reviewen
   - Diagnose 082 bestaetigt den einzelnen Similar-Strength-Smoke mit Save/Log/Output/Reload true und `normalizedWriteReloadEvolutionMismatches=0`.
   - Der Reload-Vergleich nutzt nur persistierte Gen3-Evolution-Felder und Ziel-Species per interner `SpeciesSet`-Identitaet; `Evolution.forme` ist kein Mismatch-Kriterium.
   - `Bad Egg=true` ist nach 055 klassifiziert; `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
   - Fuer diesen engen `FVX-TRAIT-018`-Scope ist kein Fixbranch erforderlich. Evolution-Methoden-Writer und weitere Evolution-Suboptionen bleiben getrennt.

13. Wild-Suboptionen konservativ halten
   - `FVX-WILD-011` und `FVX-WILD-004` sind im `FVX-WILD-001` Carrier-Fix-Smoke stabil.
   - Evolution Restrictions, Catch Em All, Minimum Catch Rate und Level-Balance bleiben getrennte Wild-Scope-Themen.

14. Spaetere TypeEffectiveness-Kombinationen nur bei Bedarf
   - Nicht mit MoveData, Palette, Items, Graphics, Text/Menu oder Species-Type-Write vermischen.

15. `analysis/upr-fvx-cfru-dpe-palette-single-owner-normal-only-fix-scope-plan`
   - Abgeschlossen: Diagnose 094 plant den normal-palette-only, single-owner/decompressible Fix-/Smoke-Scope; kein Shiny-Write, kein shared-pointer Write, kein Repointing ohne eigene Policy.

16. `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write`
   - Nur nach separater Freigabe: Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Pfade, Secrets oder `.env` dokumentieren oder committen.
- Keine Aenderungen direkt auf `main`.
- Keine Original-Upstreams kontaktieren.
- `02_external/**` nur in expliziten Fixbranches und nur nach Freigabe aendern.
