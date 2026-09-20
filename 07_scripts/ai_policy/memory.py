"""Battle-local, four-decision memory used by the host contract."""

from __future__ import annotations

from collections.abc import Iterable


MEMORY_LIMIT = 4
ACCURACY_FAMILY = frozenset({"accuracy_down", "sand_attack", "smokescreen"})
SPEED_FAMILY = frozenset({"speed_down", "string_shot"})


def normalize_effect_family(family: str | None) -> str | None:
    if family in ACCURACY_FAMILY:
        return "accuracy_down"
    if family in SPEED_FAMILY:
        return "speed_down"
    return family


def trim_decisions(decisions: Iterable[dict]) -> list[dict]:
    return [dict(item) for item in decisions][-MEMORY_LIMIT:]


def consecutive_successes(decisions: Iterable[dict], family: str | None) -> int:
    normalized = normalize_effect_family(family)
    if not normalized:
        return 0
    count = 0
    for decision in reversed(trim_decisions(decisions)):
        if decision.get("forced") or not decision.get("success"):
            break
        if normalize_effect_family(decision.get("effect_family")) != normalized:
            break
        count += 1
    return count


def voluntary_switch_edges(decisions: Iterable[dict]) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for decision in trim_decisions(decisions):
        if decision.get("kind") != "switch" or decision.get("forced"):
            continue
        start, end = decision.get("switch_from"), decision.get("switch_to")
        if isinstance(start, str) and isinstance(end, str) and start and end:
            edges.append((start, end))
    return edges


def detects_aba_switch_loop(decisions: Iterable[dict]) -> bool:
    """Detect A->B followed later by B->A among voluntary edges only."""
    edges = voluntary_switch_edges(decisions)
    for first, second in zip(edges, edges[1:]):
        if first[0] == second[1] and first[1] == second[0]:
            return True
    return False
