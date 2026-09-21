"""Deterministic Standard policy over synthetic referee candidate facts."""

from __future__ import annotations

from dataclasses import dataclass

from .floor import FloorResult
from .memory import would_form_aba_switch_loop
from .rng import XorShift32


INT32_MIN = -(2**31)
INT32_MAX = 2**31 - 1
HP_FRACTION_SCALE = 256
STANDARD_EPSILON = 8
STANDARD_UTILITY_FIELDS = (
    "net_faints", "opponent_hp_fraction_lost", "own_hp_fraction_lost",
    "immediate_future_gain", "entry_cost", "repeat_cost", "uncertainty_cost",
)


@dataclass(frozen=True)
class UtilityResult:
    total: int
    terms: dict[str, int | bool]


@dataclass(frozen=True)
class StandardDecision:
    selected_action_id: str
    best_score: int
    near_best_ids: tuple[str, ...]
    diagnostics: tuple[dict, ...]


def _toward_zero(numerator: int, denominator: int) -> int:
    magnitude = abs(numerator) // denominator
    return -magnitude if numerator < 0 else magnitude


def utility(action: dict) -> UtilityResult:
    """Evaluate the accepted signed utility formula and saturate to int32.

    Inputs are schema-bounded.  The exact expression fits signed int64, then the
    final result is clamped once to the signed int32 policy range.
    """
    missing = [field for field in STANDARD_UTILITY_FIELDS if field not in action]
    if missing:
        raise ValueError(f"standard candidate lacks utility fields: {missing}")
    for field in STANDARD_UTILITY_FIELDS:
        if not isinstance(action[field], int) or isinstance(action[field], bool):
            raise ValueError(f"standard utility field {field} must be an integer")
    if not -1 <= action["net_faints"] <= 1:
        raise ValueError("net_faints must be in [-1, 1]")
    if not 0 <= action["opponent_hp_fraction_lost"] <= HP_FRACTION_SCALE:
        raise ValueError("opponent HP fraction lost must be in [0, 256]")
    if not -HP_FRACTION_SCALE <= action["own_hp_fraction_lost"] <= HP_FRACTION_SCALE:
        raise ValueError("own HP fraction lost must be in [-256, 256]")
    if not -40 <= action["immediate_future_gain"] <= 40:
        raise ValueError("immediate future gain must be in [-40, 40]")
    for field in ("entry_cost", "repeat_cost", "uncertainty_cost"):
        if not 0 <= action[field] <= INT32_MAX:
            raise ValueError(f"{field} must be a non-negative int32")
    net_faints_term = 200 * action["net_faints"]
    hp_delta = action["opponent_hp_fraction_lost"] - action["own_hp_fraction_lost"]
    hp_delta_term = _toward_zero(100 * hp_delta, HP_FRACTION_SCALE)
    raw_total = (
        net_faints_term
        + hp_delta_term
        + action["immediate_future_gain"]
        - action["entry_cost"]
        - action["repeat_cost"]
        - action["uncertainty_cost"]
    )
    total = min(INT32_MAX, max(INT32_MIN, raw_total))
    return UtilityResult(total, {
        "entry_cost": action["entry_cost"],
        "hp_delta_term": hp_delta_term,
        "immediate_future_gain": action["immediate_future_gain"],
        "net_faints": action["net_faints"],
        "net_faints_term": net_faints_term,
        "opponent_hp_fraction_lost": action["opponent_hp_fraction_lost"],
        "own_hp_fraction_lost": action["own_hp_fraction_lost"],
        "repeat_cost": action["repeat_cost"],
        "saturated": total != raw_total,
        "uncertainty_cost": action["uncertainty_cost"],
    })


def _admission(action: dict, floor: FloorResult, memory: dict) -> tuple[bool, tuple[str, ...]]:
    action_id = action["id"]
    if action_id not in floor.eligible_ids:
        return False, floor.excluded.get(action_id, ("HARD_FLOOR_EXCLUDED",))
    if action["kind"] != "switch":
        return True, ("STANDARD_STAY_ADMITTED",)
    if action["forced"]:
        return True, ("STANDARD_FORCED_REPLACEMENT_ADMITTED",)
    if not action["standard_switch_emergency"]:
        return False, ("STANDARD_NON_EMERGENCY_SWITCH",)
    if (would_form_aba_switch_loop(
            memory.get("decisions", []), action["switch_from"], action["switch_to"])
            and not action["positive_marginal_exception"]):
        return False, ("STANDARD_SWITCH_LOOP_GUARD",)
    return True, ("STANDARD_EMERGENCY_SWITCH_ADMITTED",)


def standard_admitted_ids(
        observation: dict, floor: FloorResult, memory: dict) -> tuple[str, ...]:
    return tuple(sorted(
        action["id"] for action in observation["candidates"]
        if _admission(action, floor, memory)[0]
    ))


def choose_standard(
        observation: dict, floor: FloorResult, memory: dict, rng: XorShift32) -> StandardDecision:
    scored: dict[str, UtilityResult] = {}
    admissions: dict[str, tuple[bool, tuple[str, ...]]] = {}
    for action in observation["candidates"]:
        scored[action["id"]] = utility(action)
        admissions[action["id"]] = _admission(action, floor, memory)
    admitted = sorted(action_id for action_id, result in admissions.items() if result[0])
    if not admitted:
        raise ValueError("standard policy has no admitted action after hard-floor filtering")
    best_score = max(scored[action_id].total for action_id in admitted)
    near_best = tuple(
        action_id for action_id in admitted
        if scored[action_id].total >= best_score - STANDARD_EPSILON
    )
    selected = near_best[0] if len(near_best) == 1 else near_best[rng.bounded(len(near_best))]
    diagnostics = []
    for action in sorted(observation["candidates"], key=lambda item: item["id"]):
        action_id = action["id"]
        admitted_action, reasons = admissions[action_id]
        score = scored[action_id]
        diagnostics.append({
            "action_id": action_id,
            "admission_reasons": list(reasons),
            "near_best": action_id in near_best,
            "selected": action_id == selected,
            "standard_eligible": admitted_action,
            "utility_terms": score.terms,
            "utility_total": score.total,
        })
    return StandardDecision(selected, best_score, near_best, tuple(diagnostics))
