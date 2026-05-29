# Pokemon Data Showdown Mapping Audit Plan

Date: 2026-05-29

Branch: `analysis/pokemon-data-showdown-mapping-audit`

Scope: read-only mapping audit planning plus a small local audit helper. No CFRU/DPE Pokemon data table, UPR-FVX code, submodule pin, ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, hash, private path, token, secret or `.env` data is changed.

## Inputs

Local constant sources:

- CFRU species: `02_external/CFRU-expansion/include/constants/species.h`
- DPE species: `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`
- CFRU moves: `02_external/CFRU-expansion/include/constants/moves.h`
- DPE moves: `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/moves.h`
- CFRU abilities: `02_external/CFRU-expansion/include/constants/abilities.h`
- DPE abilities: `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/abilities.h`

External reference input, not vendored:

- Pokemon Showdown data directory: <https://github.com/smogon/pokemon-showdown/tree/master/data>
- Expected files from an external checkout: `pokedex.ts`, `moves.ts`, and `abilities.ts`

## Audit Helper

Added `07_scripts/data_audit/showdown_mapping_audit.py`.

The helper is intentionally read-only:

- It parses local CFRU/DPE `#define` constants for Species, Moves and Abilities.
- It detects CFRU-vs-DPE constant-name drift and same-value/different-name rows.
- It detects alias defines such as `ABILITY_HADRONENGINE ABILITY_ELECTRICSURGE`.
- If `--showdown-data-dir` is supplied, it reads an external Pokemon Showdown `data/` directory and reports normalized keys that do not map cleanly.
- It writes nothing unless the caller redirects stdout outside the repo or into an ignored local path.
- It does not download Pokemon Showdown data and does not copy Showdown data into the repository.

Example local-only smoke:

```sh
python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20
```

Example full audit against an external checkout:

```sh
python3 07_scripts/data_audit/showdown_mapping_audit.py --showdown-data-dir /path/to/pokemon-showdown/data --limit 100
```

## Local-Only Findings

The local-only helper run produced these source-backed findings:

| Area | Local finding | Current unresolved mapping risk |
| --- | --- | --- |
| Species | CFRU has 1415 Species constants; DPE has 1415 Species constants. | Four same-ID Ogerpon Terastal form names differ between CFRU and DPE. |
| Moves | CFRU has 993 Move constants; DPE has 993 Move constants. | No CFRU-vs-DPE local constant-name drift found in the local-only run. Showdown comparison is still needed for normalized move keys. |
| Abilities | CFRU has 289 Ability constants; DPE has 288 Ability constants. | CFRU-only `EVAPORATE` and `LINGERINGAROMA`, DPE-only `UNUSED`, same value `0x4D` named differently, and 67 total local alias define rows across the two headers. |

Important local unresolved mappings:

- `0x592`: CFRU `SPECIES_OGERPON_GREEN`; DPE `SPECIES_OGERPON_TERASTAL`
- `0x593`: CFRU `SPECIES_OGERPON_BLUE`; DPE `SPECIES_OGERPON_WELLSPRING_TERASTAL`
- `0x594`: CFRU `SPECIES_OGERPON_RED`; DPE `SPECIES_OGERPON_HEARTHFLAME_TERASTAL`
- `0x595`: CFRU `SPECIES_OGERPON_GREY`; DPE `SPECIES_OGERPON_CORNERSTONE_TERASTAL`
- `0x4D`: CFRU `ABILITY_LINGERINGAROMA`; DPE `ABILITY_UNUSED`

Ability aliases need a separate risk class. A normalized name match between Pokemon Showdown and CFRU/DPE is not sufficient when the local constant is an alias to an older effect. Examples from the local headers include:

- `ABILITY_HADRONENGINE -> ABILITY_ELECTRICSURGE`
- `ABILITY_ORICHALCUMPULSE -> ABILITY_DROUGHT`
- `ABILITY_POISONPUPPETEER -> ABILITY_PLUS`
- `ABILITY_PROTOSYNTHESIS -> ABILITY_QUARKDRIVE`
- `ABILITY_SUPERSWEETSYRUP -> ABILITY_INTIMIDATE`
- `ABILITY_TOXICCHAIN -> ABILITY_POISONTOUCH`

## Full Showdown Mapping Report Shape

When an external Pokemon Showdown checkout is available, generate a report with these sections:

1. `Showdown species keys without local normalized constant`
2. `Local species constants without Showdown normalized key`
3. `Showdown move keys without local normalized constant`
4. `Local move constants without Showdown normalized key`
5. `Showdown ability keys without local normalized constant`
6. `Local ability constants without Showdown normalized key`
7. `Ability aliases`, always reviewed separately from name coverage
8. `CFRU/DPE same value with different names`

Interpretation rules:

- Unresolved does not automatically mean missing data. It means the name normalization could not prove a safe one-to-one mapping.
- Species/form mismatches should be resolved with an explicit alias map before any data update.
- Local-only move extras such as Z-Moves, Max Moves or G-Max Moves may be intentional engine constants rather than Showdown mismatches.
- Ability aliases should remain unresolved for behavior purposes until the CFRU effect implementation is audited.

## Recommended Next Step

Run the helper against a clean external Pokemon Showdown checkout outside the repository and capture only sanitized summary counts and unresolved-name lists. Do not commit Showdown source files or generated bulk reports. If a report is worth preserving, commit a small sanitized summary under `08_tests/randomizer/` and keep raw comparison output in ignored local storage.

## Handoff Prompt

Continue from `analysis/pokemon-data-showdown-mapping-audit`. Run `07_scripts/data_audit/showdown_mapping_audit.py` against an external Pokemon Showdown `data/` directory, review unresolved species/forms/moves/abilities, and draft a small alias map proposal. Treat Ability aliases as behavior-risk findings, not solved mappings. Do not edit CFRU/DPE Pokemon data tables.
