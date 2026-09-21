# Trainer AI deterministic host harness

This standard-library Python package is the synthetic host contract from
Workspace Issue #508 plus the executable `standard` host policy from Issue
#510. It does not consume ROM, save, emulator, state, build, or component data.
Candidate facts are source-authored referee declarations; they are not claimed
to be derived from CFRU mechanics.

Run from the Workspace root:

```sh
python3 07_scripts/ai_policy/cli.py validate
python3 07_scripts/ai_policy/cli.py run --policy standard --replicate 0
python3 07_scripts/ai_policy/cli.py replay --fixture-id standard_equal_four --policy standard --replicate 37
python3 07_scripts/ai_policy/cli.py summarize --policy standard --replicate 0
python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'
```

`validate` checks both committed fixture documents by default. The `standard`
policy automatically selects `fixtures/standard_fixtures.json`; the three
baseline policies automatically select the unchanged #508 corpus. An explicit
document can be selected before the subcommand, for example:

```sh
python3 07_scripts/ai_policy/cli.py \
  --fixtures 07_scripts/ai_policy/fixtures/standard_fixtures.json \
  summarize --policy ko_first_no_switch --replicate 0
```

`run` writes canonical JSONL to standard output. Retained local output belongs
only in an untracked location.

## Fixture versions

`ai-policy-fixture-v1` remains byte-for-byte unchanged. Its compact action row
order is:

```text
id, kind, legal, productive, known_no_effect, pure_status,
robust_safe_ko, redundant_status, stat_stage_before, stat_stage_after,
effect_family, positive_marginal_exception, expected_damage,
switch_legal, entry_survives, forced, fallback_cost, switch_from, switch_to
```

`ai-policy-fixture-v2` is a separate, strict Standard schema. It appends only
the synthetic facts required by the accepted policy:

```text
net_faints, opponent_hp_fraction_lost, own_hp_fraction_lost,
immediate_future_gain, entry_cost, repeat_cost, uncertainty_cost,
standard_switch_emergency
```

HP fractions use an exact 1/256 scale. `own_hp_fraction_lost` may be negative
to represent certified net recovery. `net_faints` is bounded to `[-1, 1]`, HP
terms to their documented fixed-point ranges, future gain to `[-40, 40]`, and
costs to non-negative signed-int32 values. Non-integers and out-of-range inputs
fail closed. The exact utility expression is evaluated within signed-int64
bounds and its final result is clamped once to signed int32; the trace records
whether saturation occurred. Division rounds toward zero.

The Standard utility is:

```text
U = 200 * net_faints
  + trunc_toward_zero(100 * (opponent_HP_fraction_lost
                              - own_HP_fraction_lost) / 256)
  + immediate_future_gain
  - entry_cost
  - repeat_cost
  - uncertainty_cost
```

The policy performs no recursive search. It applies the #508 hard floor and
robust-KO dominance first, admits only forced replacements or referee-certified
emergency/dominance voluntary switches, applies the A->B->A loop guard, then
scores. It uniformly samples the stable-ID set `score >= best_score - 8` with
the existing rejection-sampled xorshift32 policy stream. A singleton consumes
zero draws; a multi-action set performs one bounded selection, whose raw draw
count (including any rejection) is recorded.

Canonical Standard traces add total utility, every utility term, saturation,
admission/exclusion reasons, eligibility, near-best membership, selection, and
policy RNG pre/post/draw state. Private truth, submitted actions, and future RNG
are never projected into the fair observation.

The baselines remain `uniform_legal`, `ko_first_no_switch`, and `first_legal`.
Their definitions and v1 canonical trace bytes are unchanged. None represents
current CFRU, Standard gameplay strength, Ironmon Smart, Expert, or a gameplay
tournament result.
