import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai_policy.rng import ZERO_SEED_REPLACEMENT, XorShift32, derive_seed


class RngContractTests(unittest.TestCase):

    def test_known_xorshift32_sequence(self):
        rng = XorShift32(1)
        self.assertEqual(
            [270369, 67634689, 2647435461, 307599695, 2398689233],
            [rng.next_u32() for _ in range(5)],
        )
        self.assertEqual(5, rng.draw_count)

    def test_zero_seed_uses_exact_replacement(self):
        rng = XorShift32(0)
        self.assertEqual(ZERO_SEED_REPLACEMENT, rng.state)
        self.assertEqual(1085196063, rng.next_u32())

    def test_identical_seed_is_byte_for_byte_stable(self):
        left, right = XorShift32(0x12345678), XorShift32(0x12345678)
        self.assertEqual(
            b"".join(left.next_u32().to_bytes(4, "little") for _ in range(64)),
            b"".join(right.next_u32().to_bytes(4, "little") for _ in range(64)),
        )

    def test_seed_derivation_known_value_and_little_endian(self):
        self.assertEqual(
            77631893,
            derive_seed("ai-policy-fixture-v1", "ko_vs_accuracy", 0, "policy"),
        )

    def test_stream_names_separate_policy_team_and_battle(self):
        seeds = {
            derive_seed("ai-policy-fixture-v1", "equal_two", 0, stream)
            for stream in ("policy", "team", "battle")
        }
        self.assertEqual(3, len(seeds))

    def test_replicates_change_seed(self):
        self.assertNotEqual(
            derive_seed("ai-policy-fixture-v1", "equal_two", 0, "policy"),
            derive_seed("ai-policy-fixture-v1", "equal_two", 1, "policy"),
        )

    def test_bounded_uses_rejection_sampling(self):
        rng = XorShift32(1)
        values = iter([0xFFFFFFFF, 7])
        rng.next_u32 = lambda: next(values)
        self.assertEqual(7, rng.bounded(10))

    def test_invalid_bounds_and_seeds_fail_closed(self):
        for seed in (-1, 2**32, True):
            with self.subTest(seed=seed), self.assertRaises(ValueError):
                XorShift32(seed)
        for upper in (0, 2**32 + 1, True):
            with self.subTest(upper=upper), self.assertRaises(ValueError):
                XorShift32(1).bounded(upper)


if __name__ == "__main__":
    unittest.main()
