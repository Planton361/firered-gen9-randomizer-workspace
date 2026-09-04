# M-001 UPR-FVX Field Items matrix harness

**Status:** Harness available; the six-row M-001 acceptance gate remains open.

This workspace-side harness runs the six required Field Items save/reload rows
against a user-supplied private candidate ROM. It does not modify UPR-FVX,
CFRU, DPE, any Gitlink, or the input ROM.

## Contract

The wrapper compiles its committed Java runner into the selected ignored output
directory. Every row launches a separate JVM, loads the same input ROM, and
writes to its own fresh output location. Outputs are never used as later row
inputs.

The runner uses UPR-FVX's Gen3 loader, settings, Field Items API, randomizer,
and save/reload path. A read-only scan of the loaded Gen3 map structures also
compares the raw Field Items slot view with the API view and confirms
low-byte-92 visible-item discovery. It emits no private path, name, hash, raw
ROM content, diagnostic, or randomizer log.

Each row emits exactly these sanitized fields:

```text
mode=<mode>
banBad=<off/on>
candidateLoaded=true/false
saveSuccessful=true/false
reloadSuccessful=true/false
rawApiTmSlotAlignmentMismatches=<n>
tmFieldItemSlotMismatches=<n>
nonTmFieldItemSlotMismatches=<n>
requiredFieldTMMissingAfter=<n>
fieldItemReloadMismatches=<n>
lowByte92Discovery=true/false
```

PASS for an individual row requires all three success booleans, all five
mismatch counters equal to zero, and `lowByte92Discovery=true`. A failed or
unavailable row uses false success values and negative counters; it cannot be
mistaken for a pass.

## Use

Run the no-ROM dry-run first. It validates the runner, Java tools, explicit
UPR-FVX JAR, and safe output destination without opening the ROM or creating
outputs:

```sh
python3 07_scripts/randomizer/m001_field_items_matrix.py \
  --rom <private-input-rom> \
  --upr-jar <pinned-upr-fvx-jar> \
  --output-dir <ignored-output-dir> \
  --dry-run
```

For the actual six-row run, omit `--dry-run` and keep the output directory
under `05_builds/` or use an existing external ignored directory. Keep the
private artifacts local and record only the sanitized result fields in any
subsequent evidence task.

```sh
python3 07_scripts/randomizer/m001_field_items_matrix.py \
  --rom <private-input-rom> \
  --upr-jar <pinned-upr-fvx-jar> \
  --output-dir <ignored-output-dir>
```

The supported matrix is fixed at Unchanged/off, Shuffle/off, Random/off,
Random/on, Random Even/off, and Random Even/on. This document does not claim
that any row has been run or that M-001 is complete.
