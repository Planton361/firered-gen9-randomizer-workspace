"""Small evaluation baselines; none represents CFRU or Ironmon Smart."""

from __future__ import annotations

from .floor import FloorResult
from .rng import XorShift32


POLICY_IDS = frozenset({"uniform_legal", "ko_first_no_switch", "first_legal"})


def choose_action(policy_id: str, observation: dict, floor: FloorResult, rng: XorShift32) -> str:
    if policy_id not in POLICY_IDS:
        raise ValueError(f"unknown baseline policy: {policy_id}")
    by_id = {action["id"]: action for action in observation["candidates"]}
    eligible = [by_id[action_id] for action_id in floor.eligible_ids]
    if policy_id == "uniform_legal":
        ordered = sorted(action["id"] for action in eligible)
        return ordered[0] if len(ordered) == 1 else ordered[rng.bounded(len(ordered))]
    if policy_id == "first_legal":
        return min(action["id"] for action in eligible)

    forced = [action for action in eligible if action["forced"]]
    if forced:
        return min(action["id"] for action in forced)
    kos = [action for action in eligible if action["robust_safe_ko"] and action["kind"] == "move"]
    pool = kos or [action for action in eligible if action["kind"] == "move"]
    if not pool:
        # This baseline has no voluntary switching strategy; the deterministic
        # floor fallback keeps the harness total in switch-only synthetic states.
        return min(action["id"] for action in eligible)
    return min(pool, key=lambda action: (-action["expected_damage"], action["id"]))["id"]
