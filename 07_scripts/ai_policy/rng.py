"""Stable policy RNG and seed derivation for synthetic fixtures."""

from __future__ import annotations

import hashlib


MASK32 = 0xFFFFFFFF
ZERO_SEED_REPLACEMENT = 0x6D2B79F5


def derive_seed(schema: str, fixture_id: str, replicate: int, stream: str) -> int:
    """Derive the contract seed from four UTF-8 fields."""
    if not all(isinstance(value, str) and value for value in (schema, fixture_id, stream)):
        raise ValueError("schema, fixture_id, and stream must be non-empty strings")
    if not isinstance(replicate, int) or isinstance(replicate, bool) or replicate < 0:
        raise ValueError("replicate must be a non-negative integer")
    material = f"{schema}|{fixture_id}|{replicate}|{stream}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(material).digest()[:4], "little")


class XorShift32:
    """xorshift32 with explicit uint32 wrapping and observable draw state."""

    def __init__(self, seed: int):
        if not isinstance(seed, int) or isinstance(seed, bool) or not 0 <= seed <= MASK32:
            raise ValueError("seed must be a uint32")
        self.state = seed or ZERO_SEED_REPLACEMENT
        self.draw_count = 0

    def next_u32(self) -> int:
        value = self.state
        value ^= (value << 13) & MASK32
        value ^= value >> 17
        value ^= (value << 5) & MASK32
        self.state = value & MASK32
        self.draw_count += 1
        return self.state

    def bounded(self, upper: int) -> int:
        """Return an unbiased value in [0, upper) using rejection sampling."""
        if not isinstance(upper, int) or isinstance(upper, bool) or not 1 <= upper <= 2**32:
            raise ValueError("upper must be in [1, 2**32]")
        limit = (2**32 // upper) * upper
        while True:
            value = self.next_u32()
            if value < limit:
                return value % upper
