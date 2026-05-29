# Pokemon data reviewed alias table smoke

Date: 2026-05-29
Branch: `analysis/pokemon-data-reviewed-alias-table`
Result: `PASS_ALIAS_TABLE_CLASSIFICATION_SMOKE_WITH_CAVEATS`

## Scope

This smoke covers the reviewed Pokemon Showdown-to-CFRU/DPE alias/ignore table and its read-only integration in `07_scripts/data_audit/showdown_mapping_audit.py`.

No CFRU/DPE Pokemon data tables, UPR-FVX code, submodule pins, Pokemon Showdown data copies, ROMs, saves, emulator states, builds, tool binaries, screenshots, raw logs, hashes, private paths, tokens, secrets, or `.env` data are included.

## Commands

- `python3 07_scripts/data_audit/showdown_mapping_audit.py --limit 20`
- `python3 07_scripts/data_audit/showdown_mapping_audit.py --showdown-data-dir <external-pokemon-showdown-data-dir> --limit 50`
- `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py`

## Observed results

Local-only audit:

- Script completed successfully.
- Alias table loaded from the repo-local default path.
- Alias table reported 471 reviewed entries.
- Category summary included Species aliases/ignores/open-risks: 4 form-name aliases, 34 GMax/Giga aliases, 76 local-shortform aliases, 11 cosmetic-form aliases, 7 cosmetic-form ignores, 161 fan-ignore entries, 1 local-extra ignore entry, and 29 Species open-risk entries.
- Category summary also retained 69 Move split aliases, 1 Hidden Power ignore pattern, 1 spelling alias, 3 CAP/Fan Move ignores, 1 Future/Fan Move ignore, 2 local helper-constant ignores, 2 local project-move ignores, 13 LGPE partner Move open-risks, 1 missing-engine Move open-risk, 13 Ability alias-plus-hook behavior-risk entries, 5 Ability behavior-risk entries, 3 Ability name-mismatch behavior-risk entries, 8 Ability missing-local open-risk entries, 13 Ability intentionally-merged aliases, 7 Ability missing-local ignores, 1 Ability sentinel/name-mismatch ignore, and 5 Ability local-only ignores.
- Existing CFRU/DPE local drift remained visible: Ogerpon form-name differences, Ability `0x4D` naming drift, and Ability alias rows.

External Showdown-data audit:

- Script completed successfully against an external Pokemon Showdown data directory.
- Species Showdown-without-local: 319 classified, 0 still uncategorized.
- Species local-without-Showdown: 221 classified, 0 still uncategorized.
- Moves Showdown-without-local: 104 classified, 0 still uncategorized.
- Moves local-without-Showdown: 143 classified, 0 still uncategorized.
- Abilities Showdown-without-local: 36 classified, 0 still uncategorized.
- Abilities local-without-Showdown: 8 classified, 0 still uncategorized.

Syntax check:

- `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py` passed.

## Caveats

This is a targeted read-only smoke. The table now classifies all current Species, Move, and Ability Showdown/local unresolved-name buckets from the external audit, but open-risk and behavior-risk entries remain blocked.

Species `open-risk` entries are not solved aliases. Alcremie cream/sweet forms, Basculin/Basculegion form semantics, Battle Bond Greninja, Pumpkaboo/Gourgeist size naming, Ogerpon mask-vs-form naming, Sinistea/Polteageist antique/chipped naming, Rockruff Dusk, and Tatsugiri form color/name semantics require source-backed policy before generated data may treat them as safe.

Move keys now have no still-uncategorized bucket in the external audit, but `open-risk` Move entries are not solved aliases. `allyswitch` and Let's Go partner moves still require source-backed local behavior or an explicit non-support policy before generator/data work can treat them as resolved.

Ability `alias-plus-hook`, `behavior-risk`, and `open-risk` entries remain blocking classifications even if the local normalized ability name exists. They require source-backed acceptance and, where appropriate, targeted battle smoke before any Gen9 data update should treat them as solved.

The Ability final batch classifies the remaining uncategorized Ability names, but does not mark blocked behavior as generator-safe. Blocking keys include As One name mismatches, Chilling Neigh, Full Metal Body, Libero, Terapagos/Ogerpon missing-local entries, Commander, Hospitality, and the existing Ruin/Tera behavior-risk entries.
