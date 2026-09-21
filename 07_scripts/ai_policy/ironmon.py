"""Deterministic Ironmon Smart policy over fair synthetic referee facts."""

from __future__ import annotations

from dataclasses import dataclass

from .floor import FloorResult
from .memory import consecutive_successes, normalize_effect_family, trim_decisions
from .rng import XorShift32
from .standard import INT32_MAX, INT32_MIN, HP_FRACTION_SCALE


IRONMON_EPSILON = 4
SWITCH_RANDOM_MIN = 12
SWITCH_RANDOM_MAX = 19
SWITCH_DETERMINISTIC_MIN = 20
SWITCH_LOOP_COST = 16
PROGRESS_EXCEPTION_MIN = 8
REPEAT_EXCEPTION_MARGIN = 8
UNKNOWN_RESPONSE_ID = "UNKNOWN"
REPEAT_EXCEPTION_REASONS = frozenset({
    "certified_order_threshold",
    "ko_or_2hko_threshold",
    "survival_threshold",
    "net_positive_recovery",
    "residual_win_line",
})


@dataclass(frozen=True)
class IronmonUtility:
    total: int
    expected_before_uncertainty: int
    uncertainty_cost: int
    branch_range: int
    repeat_count: int
    repeat_cost: int
    loop_cost: int
    saturated: bool
    branches: tuple[dict, ...]


@dataclass(frozen=True)
class IronmonDecision:
    selected_action_id: str
    best_score: int
    near_best_ids: tuple[str, ...]
    diagnostics: tuple[dict, ...]
    response_weights: tuple[dict, ...]
    switch_arbitration: dict


def _toward_zero(numerator: int, denominator: int) -> int:
    magnitude = abs(numerator) // denominator
    return -magnitude if numerator < 0 else magnitude


def response_distribution(observation: dict) -> tuple[dict, ...]:
    """Build exact integer weights from revealed moves and public counts only."""
    model = observation["response_model"]
    moves = sorted(model["revealed_moves"])
    if not moves:
        return ({"response_id": UNKNOWN_RESPONSE_ID, "weight": 1},)
    smoothed = {move: model["move_counts"][move] + 1 for move in moves}
    total = sum(smoothed.values())
    if model["unknown_move_slots"]:
        # Known responses own 75% and the aggregate UNKNOWN response owns 25%:
        # 3*total known units + total unknown units, without rounding.
        rows = [
            {"response_id": move, "weight": 3 * smoothed[move]}
            for move in moves
        ]
        rows.append({"response_id": UNKNOWN_RESPONSE_ID, "weight": total})
        return tuple(rows)
    return tuple(
        {"response_id": move, "weight": smoothed[move]}
        for move in moves
    )


def _aba_within_three(memory: dict, action: dict) -> bool:
    if action["kind"] != "switch" or action["forced"]:
        return False
    start, end = action["switch_from"], action["switch_to"]
    for decision in trim_decisions(memory.get("decisions", []))[-3:]:
        if decision.get("kind") != "switch" or decision.get("forced"):
            continue
        if (decision.get("switch_from"), decision.get("switch_to")) == (end, start):
            return True
    return False


def _consecutive_voluntary_switches(memory: dict) -> int:
    count = 0
    for decision in reversed(trim_decisions(memory.get("decisions", []))):
        if decision.get("kind") == "switch" and decision.get("forced"):
            continue
        if decision.get("kind") != "switch":
            break
        count += 1
    return count


def _repeat_count(action: dict, memory: dict) -> int:
    if not action["pure_status"]:
        return 0
    return consecutive_successes(memory.get("decisions", []), action["effect_family"])


def ironmon_utility(
        action: dict, response_weights: tuple[dict, ...], memory: dict) -> IronmonUtility:
    repeat_count = _repeat_count(action, memory)
    repeat_cost = 8 * min(3, repeat_count)
    loop_cost = SWITCH_LOOP_COST if _aba_within_three(memory, action) else 0
    weights = {row["response_id"]: row["weight"] for row in response_weights}
    branch_by_response = {row["response_id"]: row for row in action["responses"]}
    branch_rows: list[dict] = []
    weighted_total = 0
    total_weight = 0
    totals: list[int] = []
    for response_id in [row["response_id"] for row in response_weights]:
        branch = branch_by_response[response_id]
        discounted_future = _toward_zero(branch["future_gain_undiscounted"], 2)
        discounted_future = max(-40, min(40, discounted_future))
        hp_delta = branch["opponent_hp_fraction_lost"] - branch["own_hp_fraction_lost"]
        hp_delta_term = _toward_zero(100 * hp_delta, HP_FRACTION_SCALE)
        net_faints_term = 200 * branch["net_faints"]
        branch_total = (
            net_faints_term
            + hp_delta_term
            + discounted_future
            - branch["entry_cost"]
            - repeat_cost
            - loop_cost
        )
        weight = weights[response_id]
        weighted_total += weight * branch_total
        total_weight += weight
        totals.append(branch_total)
        branch_rows.append({
            "discounted_future_gain": discounted_future,
            "entry_cost": branch["entry_cost"],
            "future_gain_undiscounted": branch["future_gain_undiscounted"],
            "hp_delta_term": hp_delta_term,
            "net_faints": branch["net_faints"],
            "net_faints_term": net_faints_term,
            "opponent_hp_fraction_lost": branch["opponent_hp_fraction_lost"],
            "own_hp_fraction_lost": branch["own_hp_fraction_lost"],
            "response_id": response_id,
            "utility_before_uncertainty": branch_total,
            "weight": weight,
        })
    expected = _toward_zero(weighted_total, total_weight)
    branch_range = max(totals) - min(totals)
    uncertainty_cost = min(25, branch_range // 4)
    raw_total = expected - uncertainty_cost
    total = min(INT32_MAX, max(INT32_MIN, raw_total))
    return IronmonUtility(
        total=total,
        expected_before_uncertainty=expected,
        uncertainty_cost=uncertainty_cost,
        branch_range=branch_range,
        repeat_count=repeat_count,
        repeat_cost=repeat_cost,
        loop_cost=loop_cost,
        saturated=total != raw_total,
        branches=tuple(branch_rows),
    )


def _select_near_best(
        action_ids: list[str], scores: dict[str, IronmonUtility], rng: XorShift32,
) -> tuple[str, int, tuple[str, ...]]:
    ordered = sorted(action_ids)
    best_score = max(scores[action_id].total for action_id in ordered)
    near_best = tuple(
        action_id for action_id in ordered
        if scores[action_id].total >= best_score - IRONMON_EPSILON
    )
    selected = near_best[0] if len(near_best) == 1 else near_best[rng.bounded(len(near_best))]
    return selected, best_score, near_best


def choose_ironmon(
        observation: dict, floor: FloorResult, memory: dict, rng: XorShift32) -> IronmonDecision:
    response_weights = response_distribution(observation)
    by_id = {action["id"]: action for action in observation["candidates"]}
    scores = {
        action_id: ironmon_utility(action, response_weights, memory)
        for action_id, action in by_id.items()
    }
    excluded: dict[str, list[str]] = {
        action_id: list(floor.excluded.get(action_id, ()))
        for action_id in by_id
        if action_id not in floor.eligible_ids
    }
    admitted = set(floor.eligible_ids)
    repeat_evidence = {
        action_id: {
            "best_productive_alternative": None,
            "exception_admitted": False,
            "exception_margin": None,
        }
        for action_id in by_id
    }

    # The common floor allows only an explicitly flagged repeat exception.  The
    # Ironmon layer then proves its named reason and post-cost margin.
    for action_id in sorted(tuple(admitted)):
        action = by_id[action_id]
        score = scores[action_id]
        if score.repeat_count < 2 or not action["pure_status"]:
            continue
        alternatives = [
            other_id for other_id in admitted
            if other_id != action_id and by_id[other_id]["productive"]
            and normalize_effect_family(by_id[other_id]["effect_family"])
            != normalize_effect_family(action["effect_family"])
        ]
        best_alternative_id = (
            min(alternatives, key=lambda item: (-scores[item].total, item))
            if alternatives else None
        )
        best_alternative = (
            scores[best_alternative_id].total if best_alternative_id else None)
        reason_ok = action["repeat_exception_reason"] in REPEAT_EXCEPTION_REASONS
        margin_ok = (
            best_alternative is not None
            and score.total >= best_alternative + REPEAT_EXCEPTION_MARGIN
        )
        repeat_evidence[action_id] = {
            "best_productive_alternative": (
                None if best_alternative_id is None else {
                    "action_id": best_alternative_id,
                    "score": best_alternative,
                }
            ),
            "exception_admitted": bool(
                action["positive_marginal_exception"] and reason_ok and margin_ok),
            "exception_margin": (
                None if best_alternative is None else score.total - best_alternative),
        }
        if not action["positive_marginal_exception"] or not reason_ok or not margin_ok:
            admitted.remove(action_id)
            excluded.setdefault(action_id, []).append("IRONMON_REPEAT_EXCEPTION_REJECTED")

    consecutive_switches = _consecutive_voluntary_switches(memory)
    for action_id in sorted(tuple(admitted)):
        action = by_id[action_id]
        if action["kind"] != "switch" or action["forced"]:
            continue
        independent_progress = (
            action["progress_after_loop_cost"] >= PROGRESS_EXCEPTION_MIN
            and not action["regenerator_only"]
        )
        if (_aba_within_three(memory, action)
                and not action["public_threat_changed"]
                and not independent_progress):
            admitted.remove(action_id)
            excluded.setdefault(action_id, []).append("IRONMON_ABA_LOOP_GUARD")
            continue
        if (consecutive_switches >= 2
                and not action["ironmon_switch_emergency"]
                and not independent_progress):
            admitted.remove(action_id)
            excluded.setdefault(action_id, []).append(
                "IRONMON_CONSECUTIVE_SWITCH_GUARD")

    if not admitted:
        raise ValueError("ironmon policy has no admitted action after floor and loop guards")

    forced = sorted(action_id for action_id in admitted if by_id[action_id]["forced"])
    emergencies = sorted(
        action_id for action_id in admitted
        if by_id[action_id]["kind"] == "switch"
        and by_id[action_id]["ironmon_switch_emergency"]
    )
    stays = sorted(
        action_id for action_id in admitted if by_id[action_id]["kind"] != "switch")
    defensible_stays = sorted(
        action_id for action_id in stays if by_id[action_id]["stay_defensible"])
    voluntary_switches = sorted(
        action_id for action_id in admitted
        if by_id[action_id]["kind"] == "switch" and not by_id[action_id]["forced"]
        and not by_id[action_id]["ironmon_switch_emergency"]
    )

    best_stay_id = (
        min(defensible_stays, key=lambda item: (-scores[item].total, item))
        if defensible_stays else None
    )
    best_switch_ids = emergencies or voluntary_switches
    best_switch_id = (
        min(best_switch_ids, key=lambda item: (-scores[item].total, item))
        if best_switch_ids else None
    )
    best_stay_score = scores[best_stay_id].total if best_stay_id else None
    best_switch_score = scores[best_switch_id].total if best_switch_id else None
    advantage = (
        best_switch_score - best_stay_score
        if best_switch_score is not None and best_stay_score is not None else None
    )
    admission_pre = rng.state
    admission_draws_before = rng.draw_count
    admission_result: bool | None = None

    if forced:
        pool = forced
        threshold_class = "forced_replacement"
        admitted_class = "forced_replacement"
        admission_result = True
    elif emergencies:
        if best_stay_score is not None and best_switch_score <= best_stay_score:
            raise ValueError("emergency switch must strictly dominate defensible staying")
        pool = emergencies
        threshold_class = "emergency"
        admitted_class = "emergency_switch"
        admission_result = True
    elif not voluntary_switches:
        pool = stays
        threshold_class = "no_eligible_switch"
        admitted_class = "stay"
        admission_result = False
    elif not defensible_stays:
        raise ValueError("non-emergency switch comparison requires a defensible stay")
    elif advantage < SWITCH_RANDOM_MIN:
        pool = defensible_stays
        threshold_class = "below_12"
        admitted_class = "stay"
        admission_result = False
    elif advantage <= SWITCH_RANDOM_MAX:
        admission_result = bool(rng.bounded(2))
        threshold_class = "random_12_19"
        admitted_class = "voluntary_switch" if admission_result else "stay"
        pool = voluntary_switches if admission_result else defensible_stays
    elif advantage >= SWITCH_DETERMINISTIC_MIN:
        pool = voluntary_switches
        threshold_class = "at_least_20"
        admitted_class = "voluntary_switch"
        admission_result = True
    else:  # The integer thresholds above are exhaustive.
        raise AssertionError("unreachable switch threshold")

    admission_post = rng.state
    admission_draw_count = rng.draw_count - admission_draws_before
    selected, best_score, near_best = _select_near_best(pool, scores, rng)
    diagnostics = []
    for action_id in sorted(by_id):
        action = by_id[action_id]
        score = scores[action_id]
        repeat_reason = action["repeat_exception_reason"]
        diagnostics.append({
            "action_id": action_id,
            "admission_reasons": sorted(excluded.get(action_id, [])),
            "branch_range": score.branch_range,
            "branch_utilities": list(score.branches),
            "expected_before_uncertainty": score.expected_before_uncertainty,
            "ironmon_eligible": action_id in pool,
            "loop_cost": score.loop_cost,
            "near_best": action_id in near_best,
            "progress_after_loop_cost": action["progress_after_loop_cost"],
            "public_threat_changed": action["public_threat_changed"],
            "regenerator_only": action["regenerator_only"],
            "repeat_best_productive_alternative": repeat_evidence[action_id][
                "best_productive_alternative"],
            "repeat_cost": score.repeat_cost,
            "repeat_count": score.repeat_count,
            "repeat_exception_admitted": repeat_evidence[action_id]["exception_admitted"],
            "repeat_exception_margin": repeat_evidence[action_id]["exception_margin"],
            "repeat_exception_reason": repeat_reason,
            "selected": action_id == selected,
            "tactical_class": action["tactical_class"],
            "uncertainty_cost": score.uncertainty_cost,
            "utility_total": score.total,
            "utility_saturated": score.saturated,
        })
    switch_arbitration = {
        "admission_rng": {
            "admitted": admission_result,
            "draw_count": admission_draw_count,
            "post_state": admission_post,
            "pre_state": admission_pre,
        },
        "admitted_tactical_class": admitted_class,
        "advantage": advantage,
        "best_stay": None if best_stay_id is None else {
            "action_id": best_stay_id, "score": best_stay_score},
        "best_switch": None if best_switch_id is None else {
            "action_id": best_switch_id, "score": best_switch_score},
        "threshold_class": threshold_class,
    }
    return IronmonDecision(
        selected_action_id=selected,
        best_score=best_score,
        near_best_ids=near_best,
        diagnostics=tuple(diagnostics),
        response_weights=response_weights,
        switch_arbitration=switch_arbitration,
    )
