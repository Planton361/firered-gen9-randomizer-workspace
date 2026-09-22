"""Executable common-floor reference contract."""

from __future__ import annotations

from dataclasses import dataclass

from .memory import consecutive_successes, normalize_effect_family


STAT_CHANGE_FAMILIES = frozenset({
    "accuracy_down", "speed_down", "attack_up", "defense_up", "speed_up",
    "special_attack_up", "special_defense_up", "evasion_up", "attack_down",
    "defense_down", "special_attack_down", "special_defense_down", "evasion_down",
})

@dataclass(frozen=True)
class FloorResult:
    legal_ids: tuple[str, ...]
    eligible_ids: tuple[str, ...]
    excluded: dict[str, tuple[str, ...]]
    reasons: tuple[str, ...]
    no_productive_action: bool


def _action_reasons(action: dict, memory: dict) -> list[str]:
    reasons: list[str] = []
    if not action["legal"]:
        return ["ILLEGAL_ACTION"]
    if action["kind"] == "switch":
        if not action["switch_legal"]:
            reasons.append("ILLEGAL_SWITCH")
        if not action["entry_survives"]:
            reasons.append("ENTRY_KO")
    if action["known_no_effect"]:
        reasons.append("KNOWN_NO_EFFECT")
    if action["redundant_status"]:
        reasons.append("REDUNDANT_STATUS")
    if (action["pure_status"]
            and normalize_effect_family(action["effect_family"]) in STAT_CHANGE_FAMILIES
            and action["stat_stage_before"] == action["stat_stage_after"]):
        reasons.append("CAPPED_STAT_CHANGE")
    repeats = consecutive_successes(memory.get("decisions", []), action["effect_family"])
    if (action["pure_status"] and repeats >= 2
            and not action["positive_marginal_exception"]):
        reasons.append("HARMFUL_REPEAT")
    if not action["productive"] and not reasons:
        reasons.append("NO_MARGINAL_VALUE")
    return reasons


def apply_common_floor(observation: dict, memory: dict) -> FloorResult:
    actions = observation["candidates"]
    legal = tuple(sorted(action["id"] for action in actions if action["legal"]))
    if not legal:
        raise ValueError("fixture has no legal action")
    forced = sorted(action["id"] for action in actions if action["legal"] and action["forced"])
    excluded: dict[str, tuple[str, ...]] = {}
    if forced:
        for action in actions:
            if action["id"] not in forced:
                excluded[action["id"]] = ("FORCED_ACTION_PRESENT",)
        return FloorResult(legal, tuple(forced), excluded, ("FORCED_ACTION",), False)

    safe: list[dict] = []
    for action in actions:
        reasons = _action_reasons(action, memory)
        if reasons:
            excluded[action["id"]] = tuple(sorted(set(reasons)))
        else:
            safe.append(action)

    if not safe:
        legal_actions = [action for action in actions if action["legal"]]
        fallback = min(legal_actions, key=lambda action: (action["fallback_cost"], action["id"]))
        excluded.pop(fallback["id"], None)
        return FloorResult(legal, (fallback["id"],), excluded,
                           ("NO_PRODUCTIVE_ACTION",), True)

    kos = sorted(action["id"] for action in safe if action["robust_safe_ko"])
    if kos:
        for action in safe:
            if action["id"] not in kos:
                excluded[action["id"]] = ("ROBUST_KO_DOMINATES",)
        safe_ids = tuple(kos)
        reasons = ("ROBUST_SAFE_KO",)
    else:
        safe_ids = tuple(sorted(action["id"] for action in safe))
        reasons = ()
    return FloorResult(legal, safe_ids, excluded, reasons, False)


def candidate_contract(observation: dict, memory: dict) -> list[dict]:
    result = apply_common_floor(observation, memory)
    excluded = result.excluded
    rows = []
    for action in sorted(observation["candidates"], key=lambda item: item["id"]):
        rows.append({
            "id": action["id"],
            "eligible": action["id"] in result.eligible_ids,
            "expected_damage": action["expected_damage"],
            "forced": action["forced"],
            "kind": action["kind"],
            "productive": action["productive"],
            "reasons": list(excluded.get(action["id"], ())),
            "robust_safe_ko": action["robust_safe_ko"],
        })
    return rows
