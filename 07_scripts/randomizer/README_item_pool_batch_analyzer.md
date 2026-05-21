# Item Pool Batch Analyzer

`item_pool_batch_analyzer.py` summarizes UPR-FVX Randomizer logs for Shop Items and Pickup Items.
It is intended for local CFRU/DPE item-policy review only.

The script writes sanitized summaries under `.local/item-pool-analysis/` by default. Raw logs,
output ROMs, saves, screenshots and full private paths must stay local and must not be committed.

## Parse-only Mode

Use this when Anton already has local Randomizer logs:

```sh
python 07_scripts/randomizer/item_pool_batch_analyzer.py parse-only \
  --logs-dir .local/item-pool-analysis/raw-logs \
  --output-dir .local/item-pool-analysis \
  --delete-raw-logs
```

`--delete-raw-logs` is optional. When set, the script deletes only parsed `.log` or `.txt` files
after summaries were written successfully, and only if the log directory is inside the workspace.

Generated files:

- `shop_items_summary.tsv`
- `pickup_items_summary.tsv`
- `combined_item_summary.tsv`
- `suspicious_items.tsv`
- `run_summary.md`

## Batch-run Mode

UPR-FVX has a local CLI entry point:

```text
java -jar UPR-FVX.jar cli -i <input-rom> -o <output-rom> -s <settings-file> -z <seed> -l
```

The analyzer can wrap that CLI for local use:

```sh
python 07_scripts/randomizer/item_pool_batch_analyzer.py batch-run \
  --jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar \
  --input-rom <private-input.gba> \
  --settings-file <settings.rnqs> \
  --output-dir .local/item-pool-analysis \
  --runs 20 \
  --seed-strategy sequential \
  --seed-base 1000
```

Codex must not run this mode with a ROM. By default, successful batch-run analysis deletes raw
logs and output ROMs after parsing. Use `--keep-raw-logs` only for local debugging under `.local/`.

## Policy Heuristic

The `policy_guess` column is intentionally heuristic. It flags likely leaks such as TMs/HMs,
Fossils, Shards, Relics/high-value valuables, Apricorns, Memories, Plates, Drives, Nectars, Mega
Stones, Z-Crystals, Dynamax/GMax items, Light/Dark Stone, Gracidea, Rusted Sword/Shield, Odd
Keystone, Bottle Caps, Sun/Moon Flute and other system/form-looking names.

Allowed examples such as healing items, normal utility items, Balls including Master Ball, Rare
Candy/PP Up/Vitamins, X Items, Gems, Eviolite and modern held/battle items are not marked
suspicious by default.

## Tests

Run the ROM-free parser tests with stdlib `unittest`:

```sh
python -m unittest 07_scripts/randomizer/tests/test_item_pool_batch_analyzer.py
```
