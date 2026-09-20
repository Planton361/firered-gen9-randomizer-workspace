"""Canonical sanitized JSONL serialization."""

from __future__ import annotations

import json
import re


FORBIDDEN_KEY_PARTS = ("path", "pointer", "timestamp", "rom", "emulator", "temp")
HEX_POINTER = re.compile(r"0x[0-9a-fA-F]{8,}")
PROTECTED_SUFFIX = re.compile(r"\.(gba|gbc?|rom|sav|srm|state)(?:$|\s)", re.IGNORECASE)


def _audit(value: object, key: str = "") -> None:
    lowered = key.lower()
    if any(part in lowered for part in FORBIDDEN_KEY_PARTS):
        raise ValueError(f"forbidden trace key: {key}")
    if isinstance(value, dict):
        for child_key, child in value.items():
            _audit(child, str(child_key))
    elif isinstance(value, list):
        for child in value:
            _audit(child, key)
    elif isinstance(value, str):
        if (HEX_POINTER.search(value) or PROTECTED_SUFFIX.search(value)
                or value.startswith(("/", "file://"))):
            raise ValueError("forbidden host/path/pointer-like trace value")


def canonical_trace_line(trace: dict) -> bytes:
    _audit(trace)
    return (json.dumps(trace, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("utf-8")
