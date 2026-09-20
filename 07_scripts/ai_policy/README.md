# Trainer AI host contract harness

This standard-library Python package is a deterministic executable specification
for Workspace Issue #508. It operates only on the committed synthetic JSON
fixtures. It is not a Trainer AI implementation, CFRU adapter, battle simulator,
or tournament runner.

Run from the Workspace root:

```sh
python3 07_scripts/ai_policy/cli.py validate
python3 07_scripts/ai_policy/cli.py run --policy uniform_legal --replicate 0
python3 07_scripts/ai_policy/cli.py replay --fixture-id equal_four --replicate 37
python3 07_scripts/ai_policy/cli.py summarize --policy uniform_legal --replicate 0
python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'
```

All commands are offline and require no ROM, save, emulator, component build,
network service, or third-party Python package. `run` writes canonical JSONL to
standard output; redirect it only to an untracked location when a retained local
copy is needed.

The fixture document and every fixture use schema `ai-policy-fixture-v1`.
Validation requires the complete logical contract and rejects unknown fields,
schemas, policy configuration, malformed action rows, contradictory truth and
expectations, duplicate IDs, inconsistent reveal history, and seed values that
do not match the required SHA-256 derivation.

Actions use this fixed compact row order in the JSON corpus:

```text
id, kind, legal, productive, known_no_effect, pure_status,
robust_safe_ko, redundant_status, stat_stage_before, stat_stage_after,
effect_family, positive_marginal_exception, expected_damage,
switch_legal, entry_survives, forced, fallback_cost, switch_from, switch_to
```

The loader expands each validated row into a named mapping before projection or
policy execution. Changing this order requires a new schema version.

Fair observations contain only declared public state and explicitly revealed
opponent facts. Challenge observations may contain the authorized full opposing
team, moves/PP, items, abilities and stats. Neither mode projects the submitted
player action or future RNG. Candidate action facts are synthetic referee
declarations; hidden-state twins verify that fair results do not change when
private truth changes.

The baselines are `uniform_legal`, `ko_first_no_switch`, and `first_legal`.
Their names are literal: none represents current CFRU, Standard, Ironmon Smart,
Expert, or production battle behavior.
