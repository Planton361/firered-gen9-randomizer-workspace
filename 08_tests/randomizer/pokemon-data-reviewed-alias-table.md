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
- Alias table reported 107 reviewed entries.
- Category summary included 4 Species form-name aliases, 32 GMax/Giga Species aliases, 55 local-shortform Species aliases, 7 Move split aliases, 1 Hidden Power ignore pattern, 1 spelling alias, 1 Ability name-mismatch alias, and 6 Ability behavior-risk entries.
- Existing CFRU/DPE local drift remained visible: Ogerpon form-name differences, Ability `0x4D` naming drift, and Ability alias rows.

External Showdown-data audit:

- Script completed successfully against an external Pokemon Showdown data directory.
- Species Showdown-without-local: 91 classified, 228 still uncategorized.
- Species local-without-Showdown: 95 classified, 126 still uncategorized.
- Moves Showdown-without-local: 24 classified, 80 still uncategorized.
- Moves local-without-Showdown: 15 classified, 128 still uncategorized.
- Abilities Showdown-without-local: 1 classified, 35 still uncategorized.
- Abilities local-without-Showdown: 1 classified, 7 still uncategorized.

Syntax check:

- `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py` passed.

## Caveats

This is a targeted read-only smoke. The Batch 2 table resolves reviewed regional Species shortforms and GMax/Giga Species aliases, but does not resolve the full Showdown-to-local mapping space.

Ability `behavior-risk` entries remain behavior risks even if the local normalized ability name exists. They require separate CFRU ability behavior review before any Gen9 data update should treat them as solved.
