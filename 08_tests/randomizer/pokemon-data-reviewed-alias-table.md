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
- Alias table reported 28 reviewed entries.
- Category summary included Species form-name, GMax/Giga and local-shortform aliases; Move split aliases, Hidden Power ignore pattern and spelling alias; Ability name-mismatch and behavior-risk entries.
- Existing CFRU/DPE local drift remained visible: Ogerpon form-name differences, Ability `0x4D` naming drift, and Ability alias rows.

External Showdown-data audit:

- Script completed successfully against an external Pokemon Showdown data directory.
- Species Showdown-without-local: 12 classified, 307 still uncategorized.
- Species local-without-Showdown: 16 classified, 205 still uncategorized.
- Moves Showdown-without-local: 24 classified, 80 still uncategorized.
- Moves local-without-Showdown: 15 classified, 128 still uncategorized.
- Abilities Showdown-without-local: 1 classified, 35 still uncategorized.
- Abilities local-without-Showdown: 1 classified, 7 still uncategorized.

Syntax check:

- `python3 -m py_compile 07_scripts/data_audit/showdown_mapping_audit.py` passed.

## Caveats

This is a targeted read-only smoke. The table is intentionally small and does not resolve the full Showdown-to-local mapping space.

Ability `behavior-risk` entries remain behavior risks even if the local normalized ability name exists. They require separate CFRU ability behavior review before any Gen9 data update should treat them as solved.
