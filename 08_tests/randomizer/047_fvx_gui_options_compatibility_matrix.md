# 047 - FVX GUI Options Compatibility Matrix for CFRU/DPE Gen9-BPRE

## Scope

This protocol summarizes the current Universal Pokemon Randomizer FVX GUI option compatibility for the tested CFRU/DPE Gen9-BPRE baseline, using the existing workspace diagnostics only. No ROMs, saves, builds, tool binaries, private paths, secrets, or `02_external/**` files were changed.

Current baseline assumed from prior diagnostics:

| Field | Value |
|---|---|
| Tested ROM family | FireRed BPRE CFRU/DPE Gen9 |
| Species scope | internal CFRU/DPE species IDs through `NUM_SPECIES=1440` / highest documented `SPECIES_PECHARUNT=0x59F` |
| Move scope | `moves.total=992`, highest loaded move `991:PsychicNoise` |
| Latest UPR-FVX compatibility baseline in docs | bounded learnset-write baseline from diagnostic 044 / UPR-FVX `dd9d80c1` |
| Matrix source | existing protocols in `08_tests/randomizer/**` |

## Status Legend

| Status | Meaning |
|---|---|
| P1-supported | Save/log/reload diagnostics exist for the tested CFRU/DPE scope, with no known blocking mismatch in that option area. |
| Partially supported | A meaningful sub-scope works, but full GUI behavior still has known limits or unimplemented writer paths. |
| Open / not diagnosed | No dedicated CFRU/DPE Gen9 diagnostic exists yet, or only model-level analysis exists. |
| Blocked | Existing diagnostics show a blocker that still requires a fix branch. |
| Out of scope | Deliberately excluded from current P1 support scope. |

## Compatibility Matrix

| GUI option / area | FVX component | CFRU/DPE ROM data model | Current status | Evidence / diagnostics | Read support needed | Write support needed | Risk | Next recommended branch |
|---|---|---|---|---|---|---|---|---|
| Species count / Gen restrictions | `RestrictedSpeciesService`, Gen3 ROM species loading | Internal SpeciesSet identity, CFRU/DPE count reaches `PokemonCount=1439` in diagnostics | P1-supported | Species identity, Gen restriction and Gen9 count diagnostics; Wild post-merge smoke | Yes, implemented for current scope | Pool selection only | Low for existing pools; Alt/Form edge cases remain possible | none unless new species tables are added |
| Wild Pokemon - standard / fallback encounters | `WildEncounterRandomizer` | Vanilla/Fallback wild encounter tables written by internal species identity | P1-supported | Wild internal species write, Gen9 wild post-merge smoke, Bad Egg special-species ban | Yes | Yes | Low for standard/fallback areas | none for P1 standard wild |
| Wild Pokemon - CFRU Day/Night/custom encounter tables | `WildEncounterRandomizer` plus CFRU custom encounter model | Custom Day/Night tables are separate from the FVX fallback wild path | Open / not diagnosed | Encounter-system model marks Day/Night custom wild as separate P2 scope | Yes | Yes | High: separate table model and time-specific encounter semantics | `analysis/upr-fvx-cfru-dpe-p2-day-night-wild-model` |
| Starters | `StarterRandomizer` | Starter species pointers/slots must preserve internal SpeciesSet identity | P1-supported | Starter write diagnostics and internal species write fix | Yes | Yes | Low | none |
| Static / Gift Pokemon | `StaticPokemonRandomizer` | Static/Gift scope includes nullable placeholder entries; writes use internal SpeciesSet identity | P1-supported | Diagnostics 021 and 022 | Yes | Yes | Low for current Static/Gift scope; Roamer/hardcoded special cases should stay explicitly scoped | none for P1 Static/Gift |
| Trainer Pokemon - species | `TrainerPokemonRandomizer` | Trainer parties with CFRU/DPE internal species and placeholder/special-species filtering | P1-supported | Diagnostics 023 and 024 | Yes | Yes | Low for species-only; trainer ability/item/moveset subfeatures have separate risks | none for species-only |
| Trainer Movesets | `TrainerMovesetRandomizer`, `Gen3RomHandler.getMovesLearnt()` | Trainer movesets use loaded move table and CFRU/DPE level-up learnset reader | P1-supported | Diagnostics 029, 031, 032 | Yes | Yes for trainer movesets | Medium: depends on move data and learnset read pool, but current combinations are stable | none for trainer movesets |
| Trainer Held Items - normal | `TrainerPokemonRandomizer`, held-item pool logic | Trainer held item entries in trainer party data | P1-supported | Diagnostics 027 and 028 | Yes | Yes | Low for normal held items | none |
| Trainer Held Items - sensible / move-based | `TrainerPokemonRandomizer`, move-sensitive held item logic | Requires trainer movesets and move data to be available without eager legacy learnset failure | P1-supported in tested combinations | Diagnostic 032 | Yes | Yes | Medium: still sensitive to future move-data/model changes | none for current tested scope |
| Pokemon Evolutions | `EvolutionRandomizer` | CFRU/DPE evolution entries with species targets written by internal identity | P1-supported | Diagnostics 025 and 026 | Yes | Yes | Medium: evolution method-specific edge cases can exist outside species-target randomization | none for P1 species evolution scope |
| Pokemon Movesets / Level-up Learnsets - read pool | `SpeciesMovesetRandomizer`, `TrainerMovesetRandomizer`, `Gen3RomHandler.getMovesLearnt()` | `gLevelUpLearnsets[]` pointer table; entries are `u16 move + u8 level`; sentinel `{0, 0xFF}` | P1-supported for read | Diagnostics 030 and 031 | Yes | No for read pool | Low for reads after CFRU/DPE gated reader | none for read-only use |
| Pokemon Movesets / Level-up Learnsets - bounded write | `SpeciesMovesetRandomizer`, `Gen3RomHandler.setMovesLearnt()` | In-place write only when new entry count fits original entry count and pointer is conflict-free | Partially supported | Diagnostics 043 and 044 | Yes | Bounded same-size / no-growth only | High if GUI settings produce growth; skipped growth requires repointing | `compat/upr-fvx-cfru-dpe-learnset-write-repointing` after FreeSpace proof |
| Pokemon Movesets / Level-up Learnsets - full randomization with growth | `SpeciesMovesetRandomizer`, `Gen3RomHandler.setMovesLearnt()` | Requires new learnset blob, pointertable update, dedupe/shared-pointer policy and reload proof | Blocked | Diagnostic 045; no proven static append region yet | Yes | Yes, with repointing | Very high: FreeSpace, pointertable, dedupe, growth and reload risks | `compat/upr-fvx-cfru-dpe-learnset-write-repointing` only if Phase 2 FreeSpace proof succeeds |
| Move Data - read | `MoveDataRandomizer`, `Gen3RomHandler.loadMoves()` | CFRU/DPE `MOVES_COUNT=992`; `BattleMove` remains 12 bytes and uses `split` for category | P1-supported for read | Diagnostics 033 and 034 | Yes | No | Low for consumers after move reader fix | none for read-only move consumers |
| Move Data - write / update moves | `MoveDataRandomizer` | Same 992-move table, with Gen4+ physical/special split and additional CFRU/DPE fields | Open / not diagnosed | Diagnostic 033 explicitly leaves Move-Data-Write open | Yes | Yes | High: field bounds, split/category semantics and extra fields must be preserved | `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model` |
| Pokemon Base Stats | `SpeciesBaseStatRandomizer`, Gen3 ROM base-stat writer | CFRU/DPE expanded species count with additional ability/type/item/stat fields in species data | Open / not diagnosed | No dedicated base-stat protocol exists in current diagnostics | Yes | Yes | High: array length, placeholder species, ability slots and Gen9 species scope need validation | `analysis/upr-fvx-cfru-dpe-p1-base-stats-model` |
| Pokemon Types | `SpeciesTypeRandomizer`, base-stat data access | Types are normally embedded in base stats; CFRU/DPE may add modern type/mapping assumptions | Open / not diagnosed | No dedicated type-randomization protocol exists | Yes | Yes | High: depends on base-stat model and valid type enum range | `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` |
| Pokemon Abilities / Hidden Abilities | `SpeciesAbilityRandomizer`, trainer ability consumers | Ability slots in species data; trainer randomization previously exposed zero-ability special-species risk | Open / not diagnosed | Trainer diagnostics fixed zero-ability pool handling, but ability randomization itself is untested | Yes | Yes | High: ability count, hidden ability fields, null/placeholder species and ability names need model proof | `analysis/upr-fvx-cfru-dpe-p1-abilities-model` |
| TM/HM Moves | `TMTutorMoveRandomizer`, `TMHMTutorCompatibilityRandomizer`, Gen3 ROM TM/HM handlers | CFRU/DPE `gTMHMMoves` via `0x8125A8C`, `u16[128]`, TMs slots `0..119`, HMs slots `120..127` | P1-supported | Diagnostics 035, 036, 037, 038 | Yes | Yes | Low for 128-slot moves; TM51-TM120 item text/menu rewrite remains out of scope | none for 128-slot TM/HM data |
| TM/HM Compatibility | `TMHMTutorCompatibilityRandomizer` | `gTMHMLearnsets` via `0x8043C68`, 16 bytes / 128 bits per species in loaded species scope | P1-supported | Diagnostics 037 and 038 | Yes | Yes | Medium: currently validated in FVX loaded species scope; broader all-1440 species write policy should stay explicit | none for tested compatibility scope |
| Move Tutors - normal tutor moves | `TMTutorMoveRandomizer` | `gMoveTutorMoves` via `0x8120BE4`, `u16[152]` | P1-supported | Diagnostics 039 and 040 | Yes | Yes | Low for normal tutor table | none |
| Move Tutors - normal tutor compatibility | `TMHMTutorCompatibilityRandomizer` | `gTutorLearnsets` via `0x8120C30`, active 19-byte stride / 152 bits per species | P1-supported | Diagnostic 040 | Yes | Yes | Medium: species-scope and placeholder handling remain important | none for normal tutor compatibility |
| Special Tutors | Special CFRU/DPE tutor logic outside normal tutor table | Separate from `gMoveTutorMoves` normal table | Out of scope | Diagnostics 039 and 040 explicitly exclude Special Tutors | Yes | Yes | High: separate UI/menu/text and compatibility semantics | `analysis/upr-fvx-cfru-dpe-p2-special-tutor-model` |
| Tutor text / menu rewrites | Text/menu writer paths | Text/menu data not part of normal 152-slot support | Out of scope | Diagnostics 040 and task scopes explicitly excluded Tutor text/menu rewrites | Yes | Yes | High: text tables and UI resources can be fragile | `analysis/upr-fvx-cfru-dpe-p2-tutor-text-menu-model` |
| Egg Moves | `SpeciesMovesetRandomizer`, Gen3 ROM egg move reader/writer | `gEggMoves` via pointer location `0x45C50`, classic `u16` stream, species marker `species + 20000`, end sentinel `0xFFFF` | P1-supported for direct scope | Diagnostics 041 and 042 | Yes | Yes | Medium: coupled full moveset randomization still depends on learnset-write scope | none for direct Egg Moves |
| Field Items | `ItemRandomizer` | Overworld item data and banned-item filtering; CFRU/DPE item count/model not yet proven | Open / not diagnosed | No dedicated Field Items protocol exists | Yes | Yes | High: item ID range, key items, HMs/TMs and script-linked items need model proof | `analysis/upr-fvx-cfru-dpe-p1-field-items-model` |
| Shops | `ItemRandomizer` / shop randomization paths | Shop inventories and item blacklist/guarantee rules | Open / not diagnosed | No dedicated Shops protocol exists | Yes | Yes | High: item IDs, special marts, evolution/X item guarantees and CFRU/DPE expanded items need validation | `analysis/upr-fvx-cfru-dpe-p1-shops-model` |
| Pickup Items | `ItemRandomizer` | Pickup item table(s) and bad-item filtering | Open / not diagnosed | No dedicated Pickup protocol exists | Yes | Yes | Medium-high: item table size and bad-item list scope unknown | `analysis/upr-fvx-cfru-dpe-p1-pickup-items-model` |
| Encounter held items | `EncounterHeldItemRandomizer` | Wild held-item fields in species/base-stat data | Open / not diagnosed | No dedicated Encounter Held Items protocol exists | Yes | Yes | High: depends on base-stat/species data model and expanded item IDs | `analysis/upr-fvx-cfru-dpe-p1-encounter-held-items-model` |
| Type Effectiveness | `TypeEffectivenessRandomizer` | Type chart / effectiveness table; modern type scope unknown | Open / not diagnosed | No dedicated Type Effectiveness protocol exists | Yes | Yes | High: type enum range and Fairy/modern type support must be established | `analysis/upr-fvx-cfru-dpe-p1-type-effectiveness-model` |
| Misc Tweaks | `MiscTweakRandomizer` | Mixed code/data patches depending on selected tweak | Open / not diagnosed | No Misc Tweaks protocol exists | Varies | Varies | Very high: each tweak can touch independent code/data paths | `analysis/upr-fvx-cfru-dpe-p1-misc-tweaks-inventory` |
| Pokemon Palettes - unchanged load/save safety | `PaletteRandomizer`, Gen3 palette handlers | CFRU/DPE palette table has missing/shared/unchanged entries; unchanged palettes are skipped on save | P1-supported for unchanged/safety path | Palette loader/save blocker diagnostics and fixes | Yes | Skip unchanged writes only | Low for non-palette-randomizing flows | none for safety path |
| Pokemon Palettes - palette randomization / type-following palettes | `Gen3to5PaletteRandomizer`, `PaletteRandomizer` | Expanded species palette table with shared/missing compressed palette pointers | Open / not diagnosed | Defensive palette diagnostics only covered loading and skipping unchanged saves | Yes | Yes | High: compressed palette write/repointing and shared palette identity risks | `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model` |
| Sprites / Graphics | Palette and ROM graphics handlers if exposed by FVX options | Compressed graphics/palette resources with CFRU/DPE expanded species | Open / not diagnosed | No sprite/graphics randomization protocol exists; only palette safety was diagnosed | Yes | Yes | Very high: compressed graphics, repointing and shared resources | `analysis/upr-fvx-cfru-dpe-p2-graphics-model` |
| Intro Pokemon | `IntroPokemonRandomizer` | Intro species reference(s), likely hardcoded or small table | Open / not diagnosed | No Intro Pokemon protocol exists | Yes | Yes | Medium: small scope but hardcoded pointers may differ in CFRU/DPE | `analysis/upr-fvx-cfru-dpe-p1-intro-pokemon-diagnostics` |
| In-game Trades | `TradeRandomizer` | Trade species/item/nickname/trainer text data | Open / not diagnosed | No Trade protocol exists | Yes | Yes | High: species identity plus text/item/write paths | `analysis/upr-fvx-cfru-dpe-p1-trades-model` |
| Trainer names / class names | `TrainerNameRandomizer` | Text data and trainer metadata | Open / not diagnosed | No Trainer Name protocol exists | Yes | Yes | Medium-high: text encoding and table bounds | `analysis/upr-fvx-cfru-dpe-p1-trainer-text-model` |

## P1-supported Areas

The following FVX GUI areas are currently P1-supported for the tested CFRU/DPE Gen9-BPRE scope:

| Area | Supported scope | Primary evidence |
|---|---|---|
| Species pools / Gen restrictions | Gen1-Gen9 species pools in current loaded scope | Count, Gen restriction and Wild diagnostics |
| Wild Pokemon | Standard / fallback wild encounters, including special-species ban | Wild write and Bad Egg diagnostics |
| Starters | Starter species write/reload by internal SpeciesSet identity | Starter diagnostics |
| Static/Gift Pokemon | Static/Gift species write/reload with null-scope handling | 021, 022 |
| Trainer Pokemon | Trainer species write/reload | 023, 024 |
| Trainer Movesets | Movesets-only and tested combinations | 029, 031, 032 |
| Trainer Held Items | Normal and sensible/move-based combinations in tested scope | 027, 028, 032 |
| Evolutions | Species-target evolution randomization | 025, 026 |
| Move Data read | Full 992-move load with split/category support | 033, 034 |
| TM/HM | 128-slot TM/HM moves and compatibility | 035-038 |
| Move Tutors | Normal 152-slot tutor moves and compatibility | 039, 040 |
| Egg Moves | Direct Egg Move stream write/reload | 041, 042 |
| Palette safety | Defensive load and skip-unchanged save | Palette loader/save diagnostics |

## Partially Supported Areas

| Area | Supported part | Missing part |
|---|---|---|
| Learnset writes | Bounded same-size in-place writes with reload match | Full growth/repointing writer |
| Move Data | Reader reaches `moves.total=992` | Move data write/update randomization |
| Palettes | Non-randomized safety path | Actual palette randomization/repointing |
| Egg Moves | Direct Egg Move scope | Coupled full moveset randomization still depends on full learnset write |
| TM/Tutor | Data tables and compatibility | Text/menu/item-name rewrites and Special Tutors |

## Open High-Risk Writers

| Priority group | Writer | Why high risk |
|---|---|---|
| 1 | Full Learnset Write / Repointing | Needs FreeSpace proof, central blob strategy, pointertable update, dedupe/shared-pointer policy and reload mismatch diagnostics. |
| 2 | Base Stats / Types / Abilities | Most per-species GUI options depend on a correct CFRU/DPE species data model and placeholder handling. |
| 3 | Move Data Write | Must preserve 992-move table, split/category fields and CFRU/DPE extra semantics. |
| 4 | Items / Shops / Field Items / Pickup | Expanded item ranges and script-/key-item safety are not yet modeled. |
| 5 | Palette / Graphics Randomization | Compressed/shared resources and repointing risk remain unmodeled beyond unchanged-save safety. |

## Prioritized Next Five Work Blocks

| Rank | Branch | Goal | Rationale |
|---|---|---|---|
| 1 | `compat/upr-fvx-cfru-dpe-learnset-write-repointing` | Continue only if Phase 2 proves enough reservable FreeSpace for actual learnset blob needs. | Full learnset write is the most direct remaining blocker for full moveset/learnset GUI support. |
| 2 | `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model` | Model base stats, type fields, ability slots and hidden ability semantics. | Base Stats, Types, Abilities and Encounter Held Items depend on the same species-data foundation. |
| 3 | `analysis/upr-fvx-cfru-dpe-p1-move-data-write-model` | Model safe write/update of the 992-entry CFRU/DPE move table. | Move read is fixed, but GUI move-update/write options remain open. |
| 4 | `analysis/upr-fvx-cfru-dpe-p1-items-shops-field-model` | Inventory Field Items, Shops, Pickup, item IDs, bad-item lists and script/key-item constraints. | Item-family GUI options are broad and currently undocumented for CFRU/DPE. |
| 5 | `analysis/upr-fvx-cfru-dpe-p1-palette-randomization-model` | Separate unchanged palette safety from actual palette randomization/repointing support. | Existing palette fixes unblock saves, but do not prove palette randomization. |

## Assumptions and Risks

- This matrix intentionally uses only existing diagnostics and repository documentation; it is not a new ROM or harness run.
- GUI option naming is grouped by FVX functional area, because exact checkbox labels can map to shared randomizer components.
- P1-supported means supported for the tested CFRU/DPE Gen9-BPRE scope, not for every possible CFRU/DPE fork or every GUI sub-option.
- Current Move Data read support does not imply Move Data write support.
- Current bounded learnset-write support does not imply safe full learnset randomization with growth.
- Special Tutors, Tutor text/menu rewrites, Move-Data-Write, full Learnset Repointing, CFRU Day/Night wild tables and graphics repointing remain deliberately outside the proven P1 surface.

## Conclusion

The tested CFRU/DPE Gen9-BPRE baseline has strong P1 support for encounter/species-facing randomization, trainer data, evolutions, TM/HM, normal tutors and direct egg moves. The remaining high-risk work is concentrated in writer-heavy GUI areas: full learnset repointing, species base-stat/type/ability data, move-data writes, item/shop tables and palette/graphics randomization.
