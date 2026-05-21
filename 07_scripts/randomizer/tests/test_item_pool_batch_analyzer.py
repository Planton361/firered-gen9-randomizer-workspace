import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "item_pool_batch_analyzer.py"
SPEC = importlib.util.spec_from_file_location("item_pool_batch_analyzer", SCRIPT_PATH)
analyzer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = analyzer
SPEC.loader.exec_module(analyzer)


SAMPLE_LOG = """
( Shop Items {SHMS} )

Added cheap Rare Candies to most shops.

--Special Shops:--

Celadon Department 4F
- Yellow Shard
- TwistedSpoon
- Pink Nectar
- Spell Tag
- Wacan Berry
- Reins Unity
- Rare Candy

==========================================================

( Pickup Items {PUMS} )

Level 1-10
15%: Float Stone
10%: Sun Stone, Max Ether, Payapa Berry, Revival Herb, Luxury Ball, Expert Belt
5%: Icy Rock, Berry Juice, Energy Root, Miracle Seed
1%: Oran Berry, Leaf Stone, Electric Gem, Icy Rock, Clear Amulet
"""


class ItemPoolBatchAnalyzerTest(unittest.TestCase):

    def test_shop_items_are_extracted(self):
        parsed = analyzer.parse_log_text(SAMPLE_LOG, "run_a")

        self.assertEqual(7, len(parsed.shop_items))
        self.assertEqual("Yellow Shard", parsed.shop_items[0].item)
        self.assertEqual("Celadon Department 4F", parsed.shop_items[0].shop)
        self.assertNotIn("Added cheap Rare Candies to most shops.",
                         [occ.item for occ in parsed.shop_items])

    def test_pickup_items_are_extracted(self):
        parsed = analyzer.parse_log_text(SAMPLE_LOG, "run_a")

        by_item = {occ.item: occ for occ in parsed.pickup_items}
        self.assertEqual("Level 1-10", by_item["Float Stone"].level_range)
        self.assertEqual("15%", by_item["Float Stone"].percentage)
        self.assertEqual("10%", by_item["Sun Stone"].percentage)
        self.assertEqual(16, len(parsed.pickup_items))

    def test_multiple_runs_are_aggregated(self):
        parsed_a = analyzer.parse_log_text(SAMPLE_LOG, "run_a")
        parsed_b = analyzer.parse_log_text(SAMPLE_LOG.replace("- Yellow Shard", "- Light Stone"), "run_b")

        summary = analyzer.aggregate([parsed_a, parsed_b])
        combined_by_item = {row["item"]: row for row in summary["combined_item_summary.tsv"]}

        self.assertEqual("2", combined_by_item["Rare Candy"]["shop_count"])
        self.assertEqual("4", combined_by_item["Icy Rock"]["pickup_count"])
        self.assertEqual("yes", combined_by_item["Light Stone"]["suspicious"])

    def test_suspicious_items_are_marked(self):
        self.assertTrue(analyzer.classify_item("Yellow Shard").suspicious)
        self.assertTrue(analyzer.classify_item("Pink Nectar").suspicious)
        self.assertTrue(analyzer.classify_item("Reins Unity").suspicious)
        self.assertTrue(analyzer.classify_item("Alorichium Z").suspicious)
        self.assertFalse(analyzer.classify_item("Rare Candy").suspicious)
        self.assertFalse(analyzer.classify_item("Clear Amulet").suspicious)
        self.assertFalse(analyzer.classify_item("Electric Gem").suspicious)

    def test_parse_only_writes_sanitized_outputs_and_can_cleanup_raw_logs(self):
        local_root = Path(".local/test-item-pool-batch-analyzer")
        local_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=local_root) as temp_name:
            temp_dir = Path(temp_name)
            logs_dir = temp_dir / "logs"
            output_dir = temp_dir / "out"
            logs_dir.mkdir()
            raw_log = logs_dir / "run_001.log"
            raw_log.write_text(SAMPLE_LOG, encoding="utf-8")

            exit_code = analyzer.main([
                "parse-only",
                "--logs-dir", str(logs_dir),
                "--output-dir", str(output_dir),
                "--delete-raw-logs",
            ])

            self.assertEqual(0, exit_code)
            self.assertFalse(raw_log.exists())
            self.assertTrue((output_dir / "shop_items_summary.tsv").exists())
            self.assertTrue((output_dir / "pickup_items_summary.tsv").exists())
            self.assertTrue((output_dir / "combined_item_summary.tsv").exists())
            self.assertTrue((output_dir / "suspicious_items.tsv").exists())
            self.assertTrue((output_dir / "run_summary.md").exists())

            rows = read_tsv(output_dir / "suspicious_items.tsv")
            self.assertIn("Yellow Shard", {row["item"] for row in rows})
            summary = (output_dir / "run_summary.md").read_text(encoding="utf-8")
            self.assertIn("ROM paths documented: no", summary)
            self.assertNotIn(str(logs_dir), summary)

    def test_raw_cleanup_is_not_run_when_parse_fails(self):
        local_root = Path(".local/test-item-pool-batch-analyzer")
        local_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=local_root) as temp_name:
            temp_dir = Path(temp_name)
            logs_dir = temp_dir / "logs"
            output_dir = temp_dir / "out"
            logs_dir.mkdir()
            raw_log = logs_dir / "not-a-log.md"
            raw_log.write_text(SAMPLE_LOG, encoding="utf-8")

            with self.assertRaises(ValueError):
                analyzer.main([
                    "parse-only",
                    "--logs-dir", str(logs_dir),
                    "--output-dir", str(output_dir),
                    "--delete-raw-logs",
                ])

            self.assertTrue(raw_log.exists())

    def test_cleanup_refuses_paths_outside_workspace(self):
        with tempfile.TemporaryDirectory() as temp_name:
            outside_dir = Path(temp_name)
            outside_log = outside_dir / "run.log"
            outside_log.write_text(SAMPLE_LOG, encoding="utf-8")

            with self.assertRaises(ValueError):
                analyzer.cleanup_raw_logs([outside_log], outside_dir, Path.cwd())

            self.assertTrue(outside_log.exists())


def read_tsv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


if __name__ == "__main__":
    unittest.main()
