#!/usr/bin/env python3
"""Generate source-only CFRU review evidence after exact pinned replay succeeds."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import showdown_pokemon_data_sync as sync
import showdown_pinned_closure as closure
import showdown_coherent_forms as coherent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--showdown-data-dir", type=Path, required=True)
    args = parser.parse_args()
    reference = json.loads(closure.REFERENCE.read_text())
    closure.verify_reference(args.showdown_data_dir, reference)
    closure.verify_component_inputs(reference)
    closure.verify_candidate(args.showdown_data_dir, reference)
    inventory, _ = closure.build_inventory(args.showdown_data_dir, reference)
    closure.require(not inventory["inventories"]["SAFE_DATA_DIFF"], "Unapplied data diff")
    before = subprocess.check_output(["git", "-C", str(sync.CFRU_ROOT), "show",
        reference["canonical_pins"]["CFRU"] + ":src/Tables/level_up_learnsets.c"], text=True)
    after = sync.CFRU_LEARNSETS.read_text()
    block = re.compile(r"static const struct LevelUpMove (s\w+)\[\] = \{.*?\};", re.S)
    old = {m[1]: m[0] for m in block.finditer(before)}
    new = {m[1]: m[0] for m in block.finditer(after)}
    sha = lambda text: hashlib.sha256(text.encode()).hexdigest()
    record = {"schema_version": 1, "canonical_cfru_pin": reference["canonical_pins"]["CFRU"],
        "showdown_revision": reference["revision"], "historical_showdown_revision": "UNKNOWN",
        "baseline_sha256": sha(before), "candidate_sha256": sha(after),
        "reference_lock": reference, "helper_sha256": inventory["helper_sha256"],
        "approved_table_sha256": {name: sha(text) for name, text in sorted(new.items()) if old.get(name) != text},
        "pointer_plan": inventory["layout_plan"], "inventory_counts": inventory["summary"]["counts"]}
    output = sync.CFRU_ROOT / "docs/coherent-learnsets-provenance.json"
    output.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n")
    consumers = sync.CFRU_ROOT / "docs/coherent-learnset-consumers.jsonl"
    consumers.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in inventory["consumer_provenance"]))
    print("Exported exact source provenance and every consumer's selected generation/profile disposition")


if __name__ == "__main__":
    main()
