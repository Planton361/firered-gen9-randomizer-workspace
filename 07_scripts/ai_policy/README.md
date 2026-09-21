# Trainer AI deterministic host harness

This standard-library Python package is the synthetic host contract from
Workspace Issue #508 plus the executable `standard` host policy from Issue
#510 and the separate `ironmon_smart` host policy from Issue #515. It does not
consume ROM, save, emulator, state, build, or component data.
Candidate facts are source-authored referee declarations; they are not claimed
to be derived from CFRU mechanics.

Run from the Workspace root:

```sh
python3 07_scripts/ai_policy/cli.py validate
python3 07_scripts/ai_policy/cli.py run --policy standard --replicate 0
python3 07_scripts/ai_policy/cli.py replay --fixture-id standard_equal_four --policy standard --replicate 37
python3 07_scripts/ai_policy/cli.py summarize --policy standard --replicate 0
python3 07_scripts/ai_policy/cli.py run --policy ironmon_smart --replicate 0
python3 07_scripts/ai_policy/cli.py replay --fixture-id ironmon_equal_four --policy ironmon_smart --replicate 37
python3 07_scripts/ai_policy/cli.py summarize --policy ironmon_smart --replicate 0
python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'
```

`validate` checks all three committed fixture documents by default. The
`standard` policy automatically selects `fixtures/standard_fixtures.json`,
`ironmon_smart` selects `fixtures/ironmon_fixtures.json`, and the three baseline
policies automatically select the unchanged #508 corpus. An explicit document
can be selected before the subcommand, for example:

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

`ai-policy-fixture-v3` is a separate strict Ironmon schema and does not
reinterpret v1 or v2. It retains the common action floor and Standard utility
facts for baseline comparison, then adds supported tactical class, switch and
loop facts plus at most eight response branches per action. The document
materializes deterministic team/battle/policy seeds from the accepted SHA-256
derivation; every policy value is integer-only.

The fair response model contains only revealed move IDs and public use counts.
Add-one smoothed revealed moves receive 75% aggregate weight while any slot is
unknown, with the remaining 25% assigned to one `UNKNOWN` branch. With no
revealed move, `UNKNOWN` receives 100%; with all slots revealed it receives no
weight. Ironmon v1 rejects every nonzero speculative opponent-switch weight.

Each response branch supplies net faints, 1/256 HP deltas, one bounded
undiscounted future term, and entry cost. The future term is divided by two
with toward-zero rounding and capped at 40. The policy subtracts the computed
repeat cost, any A->B->A loop cost, and one quarter of the branch-utility range
(maximum 25), then saturates the final signed result to int32. There is no
move-class bonus and no recursive search.

Ironmon compares each admissible voluntary switch with the best defensible stay
and excludes every candidate whose own advantage is below 12. The best
remaining advantage from 12 through 19 consumes exactly one 50/50 policy-stream
admission draw; 20 or more admits deterministically. Emergency candidates must
each strictly dominate a defensible stay; forced replacement remains separate.
Selection then samples stable action IDs within epsilon 4 of the best member of
the admitted stay or individually eligible replacement class. Canonical traces
record the public response weights, branch utilities, uncertainty/repeat/loop
costs, best stay, each switch score/advantage and eligibility, the admitted
replacement pool, threshold, admission RNG, near-best set, total RNG state, and
action.
