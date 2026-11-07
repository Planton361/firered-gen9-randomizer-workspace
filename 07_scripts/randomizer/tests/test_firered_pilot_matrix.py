"""#743/#748 tests: synthetic settings/ROM files and a mocked UPR process only.

Never launches UPR, Gradle or a real JAR and never opens a real ROM or .rnqs.
The Java adapter test compiles against synthetic Settings stand-ins.
"""
import contextlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import firered_pilot_matrix as m  # noqa: E402


GUARD_TEXT = "Randomization failed: com.uprfvx.random." + m.LEARNSET_GUARD + "\nRandomization failed\n"


def neutral():
    state = dict(m.NEUTRAL)
    # Free sub-options a GUI save may carry; they must survive unchanged.
    state.update({"getWildPokemonZoneMod": "GAME", "isBlockWildLegendaries": "true",
                  "isTrainersBlockLegendaries": "true", "getGuaranteedMoveCount": "2"})
    return state


def done(args, rc=0, out="", err=""):
    return subprocess.CompletedProcess(args, rc, out, err)


class FakeUPR:
    """Models settings-profile, cli, the reopen identity check and loaded-manifest.

    Synthetic .rnqs files are JSON states; synthetic ROMs are text.
    """

    def __init__(self):
        self.calls = []
        self.extra_effect = {}       # overlay -> hidden extra Settings change
        self.cli_fail = set()        # case seeds whose generation fails
        self.cli_override = {}       # seed -> callable(args, output) -> CompletedProcess
        self.reopen_fail = set()
        self.manifest_fail = set()
        self.observe_rc = 0
        self.target_rc = 0
        self.tweak = {}              # tweakForRom stand-in: getter -> value after normalization
        self.profile_rc = 0
        self.nondeterministic = False

    def kind(self, args):
        if "settings-profile" in args:
            return "profile"
        if "cli" in args:
            return "cli"
        if "loaded-manifest" in args:
            return "manifest"
        if any(str(a).endswith("PilotSettingsObserve.java") for a in args):
            return "observe"
        if any(str(a).endswith("MatrixReopen.java") for a in args):
            return "reopen"
        if args[:2] == ["git", "-C"]:
            return "git"
        raise AssertionError("unexpected command")

    def __call__(self, args, cwd, timeout=600):
        args = [str(a) for a in args]
        kind = self.kind(args)
        self.calls.append((kind, args))
        return getattr(self, kind)(args)

    def observe(self, args):
        if self.observe_rc:
            return done(args, self.observe_rc)
        paths = args[args.index(next(a for a in args if a.endswith(".java"))) + 1:]
        target = paths[:1] == ["--rom"]
        if target:
            if self.target_rc:
                return done(args, self.target_rc)
            paths = paths[2:]
        out = []
        for path in paths:
            state = json.loads(Path(path).read_text())
            if target:
                state.update(self.tweak)
            out.append("BEGIN")
            out += [f"{k}={v}" for k, v in sorted(state.items())]
            out.append("END")
        return done(args, 0, "\n".join(out) + "\n")

    def profile(self, args):
        if self.profile_rc:
            return done(args, self.profile_rc, "", "Unknown settings feature overlay")
        if "--enable" not in args and "--profile" not in args:
            return done(args, 1, "", "No --enable or --profile overlays were provided.")
        state = json.loads(Path(args[args.index("--base-settings") + 1]).read_text())
        for i, a in enumerate(args):
            if a == "--profile" and args[i + 1] != "00_BASELINE":
                return done(args, 1, "", "Unknown settings profile")
            if a in ("--enable", "--profile"):
                state.update(m.OVERLAY_EFFECT.get(args[i + 1], {}))
                state.update(self.extra_effect.get(args[i + 1], {}))
        Path(args[args.index("--output-settings") + 1]).write_text(json.dumps(state))
        return done(args, 0, "Settings profile written successfully.\n")

    def cli(self, args):
        state = json.loads(Path(args[args.index("-s") + 1]).read_text())
        seed, output = int(args[args.index("-z") + 1]), Path(args[args.index("-o") + 1])
        if seed in self.cli_override:
            return self.cli_override[seed](args, output)
        if state["getMovesetsMod"] != "UNCHANGED" or state["isReorderDamagingMoves"] == "true":
            return done(args, 1, "", GUARD_TEXT)
        if seed in self.cli_fail:
            return done(args, 1, "", "java.lang.IllegalStateException: boom at /private/secret/path\n")
        nonce = len(self.calls) if self.nondeterministic else 0
        output.write_text(json.dumps([seed, state["getStartersMod"], state["isRandomizeWildPokemon"],
                                      state["getTrainersMod"], nonce]))
        return done(args, 0, "Randomized successfully!\n")

    def reopen(self, args):
        if json.loads(Path(args[-1]).read_text())[0] in self.reopen_fail:
            return done(args, 1)
        return done(args, 0, "Supported CFRU/DPE output identity verified.\n")

    def manifest(self, args):
        if json.loads(Path(args[args.index("-i") + 1]).read_text())[0] in self.manifest_fail:
            return done(args, 1, "ERROR: Could not write sanitized loaded manifests.\n")
        Path(args[args.index("-o") + 1]).mkdir()
        return done(args, 0, "Wrote sanitized loaded manifests.\n")

    def count(self, kind):
        return sum(k == kind for k, _ in self.calls)


class Fixture:
    def __init__(self, testcase, baseline=None):
        self.dir = Path(tempfile.mkdtemp(prefix="pilot-test-"))
        testcase.addCleanup(shutil.rmtree, self.dir, True)
        self.rom = self.dir / "source.gba"
        self.rom.write_text("synthetic source rom")
        self.baseline = self.dir / "neutral.rnqs"
        self.baseline.write_text(json.dumps(neutral() if baseline is None else baseline))
        self.jar = self.dir / "UPR-FVX.jar"
        self.jar.write_text("synthetic")
        self.out = self.dir / "out"
        self.out.mkdir()
        self.temp = self.dir / "temp"
        self.temp.mkdir()
        self.upr = FakeUPR()
        patcher = patch.object(m, "command", self.upr)
        patcher.start()
        testcase.addCleanup(patcher.stop)

    def run(self):
        return m.run_matrix(self.rom, self.baseline, self.jar, self.out, self.temp)

    def single(self, options=m.SINGLE_OPTIONS):
        return m.run_single(self.rom, self.baseline, self.jar, self.out, self.temp, options)


def statuses(results):
    return [results[c.id].status for c in m.CASES]


class PlanTests(unittest.TestCase):
    def test_exact_case_order_and_expectations(self):
        self.assertEqual([c.id for c in m.CASES], [f"M{i:02}" for i in range(11)])
        self.assertEqual([c.expect for c in m.CASES], ["PASS"] * 8 + ["EXPECTED_REJECTION"] * 2 + ["PASS"])
        positives = {c.overlays for c in m.CASES[:8]}
        self.assertEqual(len(positives), 8)
        self.assertTrue(all(set(o) <= {m.STARTER, m.WILD, m.TRAINER} for o in positives))
        m10, m07 = m.CASES[10], m.CASES[7]
        self.assertEqual((m10.overlays, m10.seed, m10.replay_of), (m07.overlays, m07.seed, "M07"))
        self.assertEqual(len({c.seed for c in m.CASES}), 10)

    def test_plan_reads_and_runs_nothing(self):
        with patch.object(m, "command", side_effect=AssertionError("no process")), \
                patch.object(m.gm, "input_digest", side_effect=AssertionError("no ROM")):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(m.main(["--plan"]), 0)
        self.assertEqual(sum(line[:1] == "M" for line in out.getvalue().splitlines()), 11)

    def test_matrix_requires_explicit_local_confirmation(self):
        for extra in ([], ["--confirm", "yes"], ["--confirm", "user_local_run"]):
            with patch.object(m, "command", side_effect=AssertionError("no process")):
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    rc = m.main(["--matrix", "--rom", "r", "--baseline", "b", "--out", "o"] + extra)
            self.assertEqual(rc, 2)
            self.assertIn("--confirm " + m.CONFIRM_TOKEN, err.getvalue())

    def test_one_mode_is_required(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            m.main([])


class MatrixTests(unittest.TestCase):
    def test_full_matrix_pass_with_expected_rejections_and_replay(self):
        f = Fixture(self)
        before = f.rom.read_bytes()
        results = f.run()
        self.assertEqual(statuses(results), ["PASS"] * 8 + ["EXPECTED_REJECTION"] * 2 + ["PASS"])
        self.assertEqual(results["M10"].replay, "PASS")
        self.assertEqual(m.report_lines(results)[1], "PASS")
        self.assertEqual(f.rom.read_bytes(), before)
        for case in m.CASES:
            produced = (f.out / case.id / "output.gba").exists()
            self.assertEqual(produced, case.expect == "PASS", case.id)
            self.assertEqual((f.out / case.id / "loaded-manifest").is_dir(), produced, case.id)
        # Every successful output was reopened, both ways, once each.
        self.assertEqual(f.upr.count("reopen"), 9)
        self.assertEqual(f.upr.count("manifest"), 9)
        self.assertEqual(f.upr.count("cli"), 11)

    def test_all_settings_checked_before_any_rom_generation(self):
        f = Fixture(self)
        f.run()
        kinds = [k for k, _ in f.upr.calls]
        self.assertEqual(kinds[:13], ["observe"] + ["profile"] * 11 + ["observe"])
        self.assertNotIn("cli", kinds[:13])

    def test_each_case_has_its_own_settings_and_seed(self):
        f = Fixture(self)
        f.run()
        cli = [a for k, a in f.upr.calls if k == "cli"]
        self.assertEqual([a[a.index("-z") + 1] for a in cli], [str(c.seed) for c in m.CASES])
        self.assertEqual(len({a[a.index("-o") + 1] for a in cli}), 11)
        for case, args in zip(m.CASES, cli):
            self.assertTrue(args[args.index("-s") + 1].endswith(case.id + ".rnqs"))

    def test_settings_come_only_from_settings_profile(self):
        f = Fixture(self)
        f.run()
        profiles = [a for k, a in f.upr.calls if k == "profile"]
        for case, args in zip(m.CASES, profiles):
            enabled = [args[i + 1] for i, a in enumerate(args) if a == "--enable"]
            self.assertEqual(tuple(enabled), case.overlays)
            self.assertEqual(args[args.index("--base-settings") + 1], str(f.baseline))
        self.assertNotIn("writeToFileFormat", m.OBSERVE_JAVA)
        self.assertNotIn("fromString", m.OBSERVE_JAVA)

    def test_case_without_overlays_uses_the_baseline_profile(self):
        f = Fixture(self)
        f.run()
        profiles = [a for k, a in f.upr.calls if k == "profile"]
        m00 = profiles[0][profiles[0].index("settings-profile") + 1:]
        self.assertEqual(m00, ["--base-settings", str(f.baseline), "--output-settings",
                               str(f.out / "settings" / "M00.rnqs"), "--profile", "00_BASELINE"])
        for args in profiles[1:]:
            self.assertNotIn("--profile", args)
        # The former call without --enable/--profile is rejected by settings-profile.
        rejected = f.upr.profile([a for a in profiles[0] if a not in ("--profile", "00_BASELINE")])
        self.assertEqual(rejected.returncode, 1)

    def test_baseline_profile_drift_stops_before_generation(self):
        f = Fixture(self)
        f.upr.extra_effect["00_BASELINE"] = {"getStartersMod": "RANDOM"}
        with self.assertRaisesRegex(m.MatrixError, "M00: settings-profile output differs"):
            f.run()
        self.assertFalse(any(k == "cli" for k, _ in f.upr.calls))

    def test_non_neutral_baseline_stops_before_overlays(self):
        for key, value in (("isRandomizeIntroMon", "true"), ("getMovesetsMod", "COMPLETELY_RANDOM"),
                           ("getEvolutionsMod", "RANDOM"), ("isMakeEvolutionsEasier", "true"),
                           ("getStartersMod", "COMPLETELY_RANDOM"), ("getCurrentMiscTweaks", "8"),
                           ("isUpdatedFromOldVersion", "true"), ("getBattleStyle", "RANDOM")):
            baseline = neutral()
            baseline[key] = value
            f = Fixture(self, baseline)
            with self.assertRaisesRegex(m.MatrixError, "not neutral: " + key):
                f.run()
            self.assertEqual(f.upr.count("profile"), 0, key)
            self.assertEqual(f.upr.count("cli"), 0, key)

    def test_uninspectable_baseline_is_never_treated_as_valid(self):
        f = Fixture(self)
        f.upr.observe_rc = 3
        with self.assertRaisesRegex(m.MatrixError, "cannot be inspected"):
            f.run()
        incomplete = neutral()
        del incomplete["isRandomizeIntroMon"]
        f = Fixture(self, incomplete)
        with self.assertRaisesRegex(m.MatrixError, "lacks 1 required"):
            f.run()
        opaque = neutral()
        opaque["getSomethingNew"] = "UNSUPPORTED"
        f = Fixture(self, opaque)
        with self.assertRaisesRegex(m.MatrixError, "cannot inspect"):
            f.run()
        self.assertEqual(f.upr.count("cli"), 0)

    def test_hidden_overlay_drift_stops_before_generation(self):
        f = Fixture(self)
        f.upr.extra_effect[m.WILD] = {"isRandomizeIntroMon": "true"}
        with self.assertRaisesRegex(m.MatrixError, "M02: settings-profile output differs"):
            f.run()
        self.assertEqual(f.upr.count("cli"), 0)

    def test_settings_profile_failure_stops(self):
        f = Fixture(self)
        f.upr.profile_rc = 1
        with self.assertRaisesRegex(m.MatrixError, "M00: settings-profile failed"):
            f.run()

    def test_unexpected_failure_stops_remaining_cases(self):
        f = Fixture(self)
        f.upr.cli_fail.add(m.CASES[2].seed)
        results = f.run()
        self.assertEqual(statuses(results), ["PASS", "PASS", "FAIL"] + ["NOT_RUN"] * 8)
        self.assertEqual(f.upr.count("cli"), 3)
        self.assertFalse((f.out / "M03").exists())

    def test_reopen_and_manifest_failures_are_failures(self):
        for attr in ("reopen_fail", "manifest_fail"):
            f = Fixture(self)
            getattr(f.upr, attr).add(m.CASES[1].seed)
            results = f.run()
            self.assertEqual(results["M01"].status, "FAIL", attr)
            self.assertEqual(results["M01"].reopen, "FAIL", attr)
            self.assertEqual(statuses(results)[2:], ["NOT_RUN"] * 9, attr)

    def test_only_the_exact_learnset_guard_counts_as_expected_rejection(self):
        def other_error(args, output):
            return done(args, 1, "", "Randomization failed: RomIOException: Oak #78 intro layout\n")

        def accepted(args, output):
            output.write_text(json.dumps([743008]))
            return done(args, 0, "Randomized successfully!\n")

        def guard_with_output(args, output):
            output.write_text("partial")
            return done(args, 1, "", GUARD_TEXT)

        def guard_with_stray_file(args, output):
            (output.parent / "output.gba.log").write_text("log")
            return done(args, 1, "", GUARD_TEXT)

        for name, fake in (("other", other_error), ("accepted", accepted),
                           ("output", guard_with_output), ("stray", guard_with_stray_file)):
            f = Fixture(self)
            f.upr.cli_override[743008] = fake
            results = f.run()
            self.assertEqual(results["M08"].status, "FAIL", name)
            self.assertEqual(statuses(results)[9:], ["NOT_RUN"] * 2, name)

    def test_replay_mismatch_fails(self):
        f = Fixture(self)
        f.upr.nondeterministic = True
        results = f.run()
        self.assertEqual((results["M10"].status, results["M10"].replay), ("FAIL", "FAIL"))
        self.assertEqual(m.report_lines(results)[1], "FAIL")

    def test_source_rom_change_stops(self):
        f = Fixture(self)
        real = f.upr.cli

        def tamper(args):
            f.rom.write_text("changed")
            return real(args)
        f.upr.cli = tamper
        with self.assertRaisesRegex(m.MatrixError, "Source ROM changed during M00"):
            f.run()


class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="pilot-root-"))
        self.addCleanup(shutil.rmtree, self.root, True)

    def test_output_folder_is_new_and_outside_tracked_tree(self):
        existing = self.root / "05_builds" / "run"
        existing.mkdir(parents=True)
        (existing / "keep.gba").write_text("user rom")
        with self.assertRaisesRegex(m.MatrixError, "already exists"):
            m.output_root(str(existing), self.root)
        self.assertEqual((existing / "keep.gba").read_text(), "user rom")
        with self.assertRaisesRegex(m.MatrixError, "must be under"):
            m.output_root(str(self.root / "07_scripts" / "run"), self.root)
        with self.assertRaisesRegex(m.MatrixError, "parent folder"):
            m.output_root(str(self.root / "05_builds" / "missing" / "run"), self.root)
        self.assertTrue(m.output_root(str(self.root / "05_builds" / "new"), self.root).is_dir())
        outside = Path(tempfile.mkdtemp(prefix="pilot-outside-"))
        self.addCleanup(shutil.rmtree, outside, True)
        self.assertTrue(m.output_root(str(outside / "run"), self.root).is_dir())

    def test_revision_gate(self):
        heads = {name: rev for name, (_, rev) in m.PILOT.items()}

        def git(path, *args):
            name = next(n for n, (rel, _) in m.PILOT.items() if str(path).endswith(rel))
            return heads[name] if args[0] == "rev-parse" else ""

        with patch.object(m.gm, "git", git), patch.object(m.gm, "jar_freshness",
                                                         return_value="NOT_OLDER_THAN_LOCAL_SOURCE"):
            lines = m.revision_lines(self.root, self.root / "jar", False)
            self.assertTrue(all("MATCH" in line for line in lines[:3]))
            heads["CFRU"] = "0" * 40
            self.assertIn("DIFFERS", m.revision_lines(self.root, self.root / "jar", False)[0])
            heads["UPR-FVX"] = "f" * 40
            with self.assertRaisesRegex(m.MatrixError, "not the pilot candidate"):
                m.revision_lines(self.root, self.root / "jar", False)
            self.assertIn("DIFFERS", m.revision_lines(self.root, self.root / "jar", True)[2])
        heads["UPR-FVX"] = m.PILOT["UPR-FVX"][1]
        for freshness in ("OLDER_THAN_LOCAL_SOURCE; rebuild recommended", "UNKNOWN"):
            with patch.object(m.gm, "git", git), patch.object(m.gm, "jar_freshness", return_value=freshness):
                with self.assertRaisesRegex(m.MatrixError, "rebuild"):
                    m.revision_lines(self.root, self.root / "jar", False)

    def test_report_has_no_paths_hashes_or_raw_logs(self):
        f = Fixture(self)
        f.upr.cli_fail.add(m.CASES[3].seed)
        out_dir = f.dir / "05_builds" / "run"
        out_dir.parent.mkdir()
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(m, "ROOT", f.dir), \
                patch.object(m, "revision_lines", return_value=["UPR-FVX: 1a9b59db3f49 MATCH"]), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            rc = m.main(["--matrix", "--confirm", m.CONFIRM_TOKEN, "--rom", str(f.rom),
                         "--baseline", str(f.baseline), "--out", str(out_dir), "--jar", str(f.jar)])
        text = stdout.getvalue() + stderr.getvalue()
        self.assertEqual(rc, 1)
        self.assertIn("M03  Trainer", text)
        self.assertIn("NOT_RUN=7", text)
        for leak in (str(f.dir), "/private/secret", "IllegalStateException", "boom", ".gba", ".rnqs"):
            self.assertNotIn(leak, text)
        self.assertIn("/private/secret", (out_dir / "M03" / "cli.log").read_text())

    def test_parse_observations_fails_closed(self):
        good = "BEGIN\nisA=true\nEND\n"
        self.assertEqual(m.parse_observations(good, 1), [{"isA": "true"}])
        for bad in ("BEGIN\nisA=true\n", "isA=true\n", "BEGIN\nisA=/tmp/x\nEND\n",
                    "BEGIN\nisA=true\nisA=false\nEND\n", "BEGIN\nfoo=true\nEND\n", good + good):
            with self.assertRaises(m.MatrixError):
                m.parse_observations(bad, 1)


def single_by(feature):
    return next(o for o in m.SINGLE_OPTIONS if o.feature == feature)


class SingleOptionTests(unittest.TestCase):
    """#748: explicit single-option cases reuse the pilot pipeline."""

    def test_options_are_new_families_with_fixed_unique_ids_and_seeds(self):
        options = m.SINGLE_OPTIONS
        self.assertGreaterEqual(len(options), 4)
        pilot_families = {o.split("-")[1] for c in m.CASES for o in c.overlays}
        new = {o.feature.split("-")[1] for o in options}
        self.assertGreaterEqual(len(new), 3)
        self.assertFalse(new & pilot_families)
        self.assertEqual(len({o.id for o in options}), len(options))
        seeds = [o.seed for o in options] + [c.seed for c in m.CASES]
        self.assertEqual(len(set(seeds)), len(options) + 10)
        for o in options:
            self.assertEqual(m.OVERLAY_EFFECT[o.feature], o.effect)
            self.assertTrue(set(o.effect) <= set(m.NEUTRAL), o.feature)   # baseline-checked owner

    def test_pilot_cases_are_unchanged(self):
        self.assertEqual([(c.id, c.overlays, c.seed, c.expect, c.replay_of) for c in m.CASES], [
            ("M00", (), 743000, "PASS", ""), ("M01", (m.STARTER,), 743001, "PASS", ""),
            ("M02", (m.WILD,), 743002, "PASS", ""), ("M03", (m.TRAINER,), 743003, "PASS", ""),
            ("M04", (m.STARTER, m.WILD), 743004, "PASS", ""), ("M05", (m.STARTER, m.TRAINER), 743005, "PASS", ""),
            ("M06", (m.WILD, m.TRAINER), 743006, "PASS", ""),
            ("M07", (m.STARTER, m.WILD, m.TRAINER), 743007, "PASS", ""),
            ("M08", (m.MOVESETS,), 743008, "EXPECTED_REJECTION", ""),
            ("M09", (m.REORDER,), 743009, "EXPECTED_REJECTION", ""),
            ("M10", (m.STARTER, m.WILD, m.TRAINER), 743007, "PASS", "M07")])
        f = Fixture(self)
        f.run()
        self.assertFalse(any(k == "observe" and "--rom" in a for k, a in f.upr.calls))
        self.assertFalse(any(k == "profile" and "FVX-TM-001" in a for k, a in f.upr.calls))

    def test_selection_is_explicit(self):
        self.assertEqual(m.select_options("all"), m.SINGLE_OPTIONS)
        self.assertEqual([o.id for o in m.select_options("FVX-TYPE-001,FVX-TM-001")], ["S02", "S05"])
        for value, message in ((None, "<empty>"), ("", "<empty>"), ("FVX-NOPE-001", "FVX-NOPE-001"),
                               ("FVX-MOVE-007", "FVX-MOVE-007"), ("FVX-SST-002", "FVX-SST-002"),
                               ("/private/x.gba", "<invalid>"), ("FVX-TM-001,FVX-TM-001", "repeated")):
            with self.assertRaisesRegex(m.MatrixError, message, msg=value):
                m.select_options(value)

    def test_bad_selection_stops_before_anything_runs(self):
        f = Fixture(self)
        out = f.dir / "05_builds" / "run"
        out.parent.mkdir()
        err = io.StringIO()
        with patch.object(m, "ROOT", f.dir), contextlib.redirect_stderr(err):
            rc = m.main(["--single", "--confirm", m.CONFIRM_TOKEN, "--select", "FVX-MOVE-007",
                         "--rom", str(f.rom), "--baseline", str(f.baseline), "--out", str(out), "--jar", str(f.jar)])
        self.assertEqual(rc, 2)
        self.assertIn("non-executable", err.getvalue())
        self.assertEqual(f.upr.calls, [])
        self.assertFalse(out.exists())

    def test_single_requires_explicit_local_confirmation(self):
        with patch.object(m, "command", side_effect=AssertionError("no process")):
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                rc = m.main(["--single", "--select", "all", "--rom", "r", "--baseline", "b", "--out", "o"])
        self.assertEqual(rc, 2)
        self.assertIn("--single runs real ROM generation", err.getvalue())

    def test_all_single_options_pass_generation_reopen_and_replay(self):
        f = Fixture(self)
        before = f.rom.read_bytes()
        results = f.single()
        self.assertEqual([(r.target, r.generate, r.reopen, r.replay, r.status) for r in results.values()],
                         [("PASS", "PASS", "PASS", "PASS", "PASS")] * 5)
        lines, overall = m.single_report_lines(results, m.SINGLE_OPTIONS)
        self.assertEqual(overall, "PASS")
        self.assertIn("GENERATION/REOPEN PASS", lines[1])
        self.assertNotIn("FEATURE_VERIFIED", "\n".join(lines).replace("no FEATURE_VERIFIED claim", ""))
        self.assertEqual(f.rom.read_bytes(), before)
        cli = [a for k, a in f.upr.calls if k == "cli"]
        self.assertEqual(len(cli), 10)
        self.assertEqual(len({a[a.index("-o") + 1] for a in cli}), 10)       # collision-free
        self.assertEqual(sorted(p.name for p in f.out.iterdir()),
                         sorted(["settings"] + [o.id for o in m.SINGLE_OPTIONS]
                                + [o.id + "-replay" for o in m.SINGLE_OPTIONS]))
        for o in m.SINGLE_OPTIONS:
            profile = next(a for k, a in f.upr.calls if k == "profile" and a[-1] == o.feature)
            self.assertEqual(profile[-2:], ["--enable", o.feature])
            self.assertTrue((f.out / o.id / "loaded-manifest").is_dir())

    def test_settings_and_target_checked_before_any_rom_generation(self):
        f = Fixture(self)
        f.single(m.select_options("FVX-TM-001,FVX-ITEM-002"))
        kinds = [k for k, _ in f.upr.calls]
        self.assertEqual(kinds[:5], ["observe", "profile", "profile", "observe", "observe"])
        target = f.upr.calls[4][1]
        self.assertEqual(target[target.index("--rom") + 1], str(f.rom))
        self.assertEqual(len(target) - target.index("--rom"), 5)   # flag, ROM, baseline, two cases

    def test_non_neutral_baseline_stops_single_run(self):
        state = neutral()
        state["getFieldItemsMod"] = "RANDOM"
        f = Fixture(self, baseline=state)
        with self.assertRaisesRegex(m.MatrixError, "Baseline is not neutral: getFieldItemsMod"):
            f.single()
        self.assertEqual([k for k, _ in f.upr.calls], ["observe"])

    def test_case_side_effect_stops_before_generation(self):
        f = Fixture(self)
        f.upr.extra_effect["FVX-TM-001"] = {"isFullHMCompat": "true"}
        with self.assertRaisesRegex(m.MatrixError, "S02: settings-profile output differs"):
            f.single()
        self.assertEqual(f.upr.count("cli"), 0)

    def test_silent_noop_overlay_stops(self):
        f = Fixture(self)
        f.upr.extra_effect["FVX-TYPE-001"] = {"getTypeEffectivenessMod": "UNCHANGED"}
        with self.assertRaisesRegex(m.MatrixError, "S05: settings-profile output differs"):
            f.single()
        self.assertEqual(f.upr.count("cli"), 0)

    def test_target_normalization_is_needs_review_never_pass(self):
        f = Fixture(self)
        f.upr.tweak = {"getTmsMod": "UNCHANGED"}       # tweakForRom silently disables S02
        results = f.single()
        self.assertEqual(results["S02"].status, "NEEDS_REVIEW")
        self.assertEqual((results["S02"].target, results["S02"].generate), ("NEEDS_REVIEW", "NOT_RUN"))
        self.assertIn("getTmsMod", results["S02"].detail)
        self.assertFalse((f.out / "S02").exists())
        self.assertEqual([r.status for k, r in results.items() if k != "S02"], ["PASS"] * 4)
        lines, overall = m.single_report_lines(results, m.SINGLE_OPTIONS)
        self.assertEqual(overall, "INCOMPLETE")
        self.assertIn("NEEDS_REVIEW=1", "\n".join(lines))

    def test_equal_normalization_of_baseline_and_case_is_accepted(self):
        f = Fixture(self)
        f.upr.tweak = {"isLimitPokemon": "false", "getCurrentRestrictions": "null"}
        self.assertEqual({r.status for r in f.single().values()}, {"PASS"})

    def test_target_rom_refusal_stops(self):
        f = Fixture(self)
        f.upr.target_rc = 4
        with self.assertRaisesRegex(m.MatrixError, "cannot be opened as CFRU/DPE"):
            f.single()
        self.assertEqual(f.upr.count("cli"), 0)

    def test_guard_or_other_failure_is_fail_and_stops_remaining_cases(self):
        for failure in ("guard", "error"):
            f = Fixture(self)
            seed = single_by("FVX-TM-001").seed
            if failure == "guard":
                f.upr.cli_override[seed] = lambda args, output: done(args, 1, "", GUARD_TEXT)
            else:
                f.upr.cli_fail.add(seed)
            results = f.single()
            self.assertEqual([r.status for r in results.values()], ["PASS", "FAIL", "NOT_RUN", "NOT_RUN", "NOT_RUN"])
            self.assertFalse((f.out / "S02" / "output.gba").exists())
            self.assertEqual(m.single_report_lines(results, m.SINGLE_OPTIONS)[1], "FAIL")

    def test_reopen_failure_and_replay_mismatch_fail(self):
        f = Fixture(self)
        f.upr.reopen_fail.add(single_by("FVX-TRAIT-001").seed)
        self.assertEqual(f.single()["S01"].reopen, "FAIL")
        f = Fixture(self)
        f.upr.nondeterministic = True
        results = f.single()
        self.assertEqual((results["S01"].status, results["S01"].replay), ("FAIL", "FAIL"))
        self.assertEqual(results["S02"].status, "NOT_RUN")

    def test_source_rom_change_stops(self):
        f = Fixture(self)
        real = f.upr.observe

        def tamper(args):
            if "--rom" in args:
                f.rom.write_text("changed")
            return real(args)
        f.upr.observe = tamper
        with self.assertRaisesRegex(m.MatrixError, "Source ROM changed during target normalization"):
            f.single()
        self.assertEqual(f.upr.count("cli"), 0)

    def test_single_report_has_no_paths_hashes_or_raw_logs(self):
        f = Fixture(self)
        f.upr.cli_fail.add(single_by("FVX-ITEM-002").seed)
        out_dir = f.dir / "05_builds" / "run"
        out_dir.parent.mkdir()
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(m, "ROOT", f.dir), \
                patch.object(m, "revision_lines", return_value=["UPR-FVX: 1a9b59db3f49 MATCH"]), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            rc = m.main(["--single", "--confirm", m.CONFIRM_TOKEN, "--select", "all", "--rom", str(f.rom),
                         "--baseline", str(f.baseline), "--out", str(out_dir), "--jar", str(f.jar)])
        text = stdout.getvalue() + stderr.getvalue()
        self.assertEqual(rc, 1)
        self.assertIn("#748 single-option matrix", text)
        self.assertIn("S04  FVX-ITEM-002", text)
        self.assertIn("SINGLE=FAIL", text)
        for leak in (str(f.dir), "/private/secret", "IllegalStateException", "boom", ".gba", ".rnqs"):
            self.assertNotIn(leak, text)
        self.assertIn("/private/secret", (out_dir / "S04" / "cli.log").read_text())

    def test_existing_output_folder_is_refused_for_single(self):
        f = Fixture(self)
        existing = f.dir / "05_builds" / "run"
        existing.mkdir(parents=True)
        (existing / "keep.gba").write_text("user rom")
        err = io.StringIO()
        with patch.object(m, "ROOT", f.dir), \
                patch.object(m, "revision_lines", return_value=[]), contextlib.redirect_stderr(err):
            rc = m.main(["--single", "--confirm", m.CONFIRM_TOKEN, "--select", "all", "--rom", str(f.rom),
                         "--baseline", str(f.baseline), "--out", str(existing), "--jar", str(f.jar)])
        self.assertEqual(rc, 2)
        self.assertIn("already exists", err.getvalue())
        self.assertEqual(f.upr.calls, [])
        self.assertEqual(sorted(p.name for p in existing.iterdir()), ["keep.gba"])


SYNTHETIC_CATALOG = '''    private static Map<String, Consumer<Settings>> buildFeatureOverlays() {
        overlays.put("FVX-A-001", s -> s.setPlain(true));
        overlays.put("FVX-A-002", s -> {
            s.setTouched(true);
            s.setPlain(false);
        });
        overlays.put("FVX-A-003", s -> helper(s, X.Y));
        overlays.put("FVX-A-004", unsupported("FVX-A-004", "No."));
        overlays.put("FVX-A-005", Gen::enable);
        overlays.put("FVX-TRAIT-001", s -> s.setBaseStatisticsMod(Settings.BaseStatisticsMod.RANDOM));
        overlays.put("FVX-MOVE-007", s -> s.setMovesetsMod(Settings.MovesetsMod.COMPLETELY_RANDOM));
        overlays.put("FVX-WILD-001", s -> s.setRandomizeWildPokemon(true));
        return Collections.unmodifiableMap(overlays);
    }
'''
SYNTHETIC_SETTINGS = '''    public TweakForROMFeedback tweakForRom(RomHandler rh) {
        TweakForROMFeedback feedback = new TweakForROMFeedback();
        if (x) {
            this.setTouched(false);
            trainersMod = TrainersMod.RANDOM;
        }
        return feedback;
    }

    // getters and setters
'''


class DispositionTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="pilot-catalog-"))
        self.addCleanup(shutil.rmtree, self.root, True)
        ledger = self.root / m.LEDGER
        ledger.parent.mkdir(parents=True)
        ledger.write_text("feature_id\tfeature_name\nFVX-A-001\tx\nFVX-OLD-001\told\n")

    def write_upr(self):
        for rel, text in ((m.CATALOG_SOURCE, SYNTHETIC_CATALOG), (m.SETTINGS_SOURCE, SYNTHETIC_SETTINGS)):
            path = self.root / m.UPR_SOURCE / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)

    def test_every_catalog_and_ledger_id_gets_a_visible_disposition(self):
        self.write_upr()
        rows, note = m.disposition(self.root)
        self.assertEqual(note, "")
        self.assertEqual({k: v[0] for k, v in rows.items()}, {
            "FVX-A-001": "NOT_RUN", "FVX-A-002": "NEEDS_REVIEW", "FVX-A-003": "NEEDS_REVIEW",
            "FVX-A-004": "UNSUPPORTED", "FVX-A-005": "NEEDS_REVIEW", "FVX-TRAIT-001": "EXECUTABLE",
            "FVX-MOVE-007": "GUARDED", "FVX-WILD-001": "EXECUTABLE", "FVX-OLD-001": "NEEDS_REVIEW"})
        self.assertIn("setTouched", rows["FVX-A-002"][1])
        self.assertIn("without current overlay", rows["FVX-OLD-001"][1])
        self.assertIn("--single S01", rows["FVX-TRAIT-001"][1])

    def test_missing_upr_source_is_never_executable(self):
        rows, note = m.disposition(self.root)
        self.assertIn("unavailable", note)
        self.assertEqual({v[0] for v in rows.values()}, {"NEEDS_REVIEW"})
        self.assertEqual(list(rows), ["FVX-A-001", "FVX-OLD-001"])

    def test_tweak_setters_include_direct_field_writes(self):
        self.assertEqual(m.tweak_setters(SYNTHETIC_SETTINGS), {"setTouched", "setTrainersMod"})

    def test_plan_prints_disposition_without_rom_jar_or_process(self):
        self.write_upr()
        with patch.object(m, "ROOT", self.root), patch.object(m, "command", side_effect=AssertionError("no")), \
                patch.object(m.gm, "input_digest", side_effect=AssertionError("no ROM")):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(m.main(["--plan"]), 0)
        text = out.getvalue()
        self.assertIn("  FVX-OLD-001", text)
        self.assertIn("Disposition: 9 IDs; EXECUTABLE=2, GUARDED=1, UNSUPPORTED=1, NEEDS_REVIEW=4, NOT_RUN=1", text)
        self.assertEqual(sum(line.startswith("S0") for line in text.splitlines()), len(m.SINGLE_OPTIONS))


UPR = m.ROOT / m.UPR_SOURCE


@unittest.skipUnless((UPR / m.CATALOG_SOURCE).is_file(), "UPR-FVX source not checked out")
class SourceBackingTests(unittest.TestCase):
    """The declarative cases match the checked-out UPR-FVX source (read as text only)."""

    def test_single_options_match_current_overlays_and_are_not_normalized(self):
        catalog = m.overlay_catalog((UPR / m.CATALOG_SOURCE).read_text())
        touched = m.tweak_setters((UPR / m.SETTINGS_SOURCE).read_text())
        for o in m.SINGLE_OPTIONS:
            self.assertEqual(catalog[o.feature], o.source, o.feature)
            setter, = re.findall(r"s\.(set\w+)\(", o.source)
            getter, = o.effect
            self.assertEqual(getter, "get" + setter[3:])
            self.assertTrue(o.source.endswith("." + o.effect[getter] + ")"), o.feature)
            self.assertNotIn(setter, touched, o.feature)

    def test_guards_are_source_cited_and_ledger_is_fully_covered(self):
        for rel, text in m.GUARD_SOURCES.items():
            self.assertIn(text, (UPR / rel).read_text())
        rows, note = m.disposition(m.ROOT)
        self.assertEqual(note, "")
        ledger = [line.split("\t", 1)[0] for line in (m.ROOT / m.LEDGER).read_text().splitlines()[1:] if line]
        self.assertEqual(len(ledger), 132)
        self.assertTrue(set(ledger) <= set(rows))
        executable = {k for k, v in rows.items() if v[0] == "EXECUTABLE"}
        self.assertEqual(executable, {o.feature for o in m.SINGLE_OPTIONS} | {m.STARTER, m.WILD, m.TRAINER})


@unittest.skipUnless(shutil.which("javac") and shutil.which("java"), "JDK not available")
class ObserveAdapterTests(unittest.TestCase):
    """Compile and run the real adapter text against synthetic API stand-ins."""

    STUBS = {
        "com/uprfvx/random/Settings.java": '''package com.uprfvx.random;
import com.uprfvx.romio.gamedata.*;
import java.io.FileInputStream;
public class Settings {
  public enum StartersMod { UNCHANGED, COMPLETELY_RANDOM }
  public enum Odd { A { public String toString() { return "lower/case"; } } }
  public static Settings readFromFileFormat(FileInputStream in) throws java.io.IOException {
    if (in.read() != 'S') throw new java.io.IOException("x"); return new Settings(); }
  public StartersMod getStartersMod() { return StartersMod.UNCHANGED; }
  public boolean isRandomizeIntroMon() { return false; }
  public int getCurrentMiscTweaks() { return 0; }
  public boolean useEstimatedLevelsForEvolutionImprovements() { return true; }
  public Odd getOdd() { return Odd.A; }
  public GenRestrictions getCurrentRestrictions() { return new GenRestrictions(); }
  public BattleStyle getBattleStyle() { return new BattleStyle(); }
  public String getRomName() { return "private"; }
  public int[] getCustomStarters() { return new int[0]; }
  public Object getCustomNames() { return null; }
  public StringBuilder getUnknown() { return new StringBuilder(); }
  public boolean isFlag(int x) { return true; }
  public static boolean isStatic() { return true; }
  public void setStartersMod(StartersMod m) { }
  boolean tweaked;
  public boolean isTweaked() { return tweaked; }
  public Object tweakForRom(com.uprfvx.romio.romhandlers.RomHandler rh) { tweaked = true; return null; }
}''',
        "com/uprfvx/romio/RootPath.java": '''package com.uprfvx.romio;
public class RootPath { public static String path; }''',
        "com/uprfvx/romio/romhandlers/RomHandler.java": '''package com.uprfvx.romio.romhandlers;
public interface RomHandler { }''',
        "com/uprfvx/romio/romhandlers/Gen3RomHandler.java": '''package com.uprfvx.romio.romhandlers;
public class Gen3RomHandler implements RomHandler {
  public boolean usesCfruDpeRandomPoolPolicy() { return true; } }''',
        "com/uprfvx/romio/romio/RomOpener.java": '''package com.uprfvx.romio.romio;
import com.uprfvx.romio.romhandlers.*;
public class RomOpener {
  public static class Results { boolean ok; RomHandler h;
    public boolean wasOpeningSuccessful() { return ok; } public RomHandler getRomHandler() { return h; } }
  public Results openRomFile(java.io.File f) throws java.io.IOException {
    Results r = new Results();
    try (java.io.FileInputStream in = new java.io.FileInputStream(f)) { r.ok = in.read() == 'C'; }
    r.h = new Gen3RomHandler(); return r; } }''',
        "com/uprfvx/romio/gamedata/GenRestrictions.java": '''package com.uprfvx.romio.gamedata;
public class GenRestrictions { public int toInt() { return 1022; } }''',
        "com/uprfvx/romio/gamedata/BattleStyle.java": '''package com.uprfvx.romio.gamedata;
public class BattleStyle { public enum Modification { UNCHANGED }
  public Modification getModification() { return Modification.UNCHANGED; } }''',
    }

    def test_adapter_prints_getters_in_order_and_flags_unknown_types(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            for rel, text in self.STUBS.items():
                (d / "src" / rel).parent.mkdir(parents=True, exist_ok=True)
                (d / "src" / rel).write_text(text)
            classes = d / "classes"
            subprocess.run(["javac", "-d", str(classes), *map(str, (d / "src").rglob("*.java"))],
                           check=True, capture_output=True)
            good, bad = d / "a.rnqs", d / "b.rnqs"
            good.write_text("S")
            bad.write_text("X")
            original = m.command
            with patch.object(m, "command", lambda args, cwd, timeout=600: original(
                    [a.replace(str(d / "jar"), str(classes)) for a in map(str, args)], cwd)):
                state, = m.observe(d / "jar", d, [good])
                self.assertEqual(list(state), sorted(state))
                self.assertEqual(state, {
                    "getBattleStyle": "UNCHANGED", "getCurrentMiscTweaks": "0",
                    "getCurrentRestrictions": "1022", "getOdd": "A", "getStartersMod": "UNCHANGED",
                    "getUnknown": "UNSUPPORTED", "isRandomizeIntroMon": "false", "isTweaked": "false",
                    "useEstimatedLevelsForEvolutionImprovements": "true"})
                with self.assertRaisesRegex(m.MatrixError, "cannot be inspected"):
                    m.observe(d / "jar", d, [good, bad])
                # #748: with a ROM, every file is normalized through tweakForRom first.
                rom, other = d / "rom.gba", d / "other.gba"
                rom.write_text("C")
                other.write_text("X")
                first, second = m.observe(d / "jar", d, [good, good], rom=rom)
                self.assertEqual((first["isTweaked"], second["isTweaked"]), ("true", "true"))
                with self.assertRaisesRegex(m.MatrixError, "cannot be opened as CFRU/DPE"):
                    m.observe(d / "jar", d, [good], rom=other)


if __name__ == "__main__":
    unittest.main()
