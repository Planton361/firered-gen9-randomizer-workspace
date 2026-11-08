"""#743/#748/#750 tests: synthetic settings/ROM files and a mocked UPR process only.

Never launches UPR, Gradle or a real JAR and never opens a real ROM or .rnqs.
The Java adapter test compiles against synthetic Settings stand-ins.
"""
import contextlib
import hashlib
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


# CliRandomizer's real failure output: completeRandomization, then usageError and its usage text.
USAGE = ("Usage: java [-Xmx4096M] -jar UPR-FVX.jar cli -i <path to source ROM> -o <path for output ROM>\n"
         "Optional flags: \n-z <seed>          : Use the given seed.\n")


def rejection(guard):
    return m.GUARD_LINE + guard + "\nERROR: Randomization failed\n" + USAGE


GUARD_TEXT = rejection(m.LEARNSET_GUARD)


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
        self.effects = m.OVERLAY_EFFECT  # overlay -> Settings change settings-profile applies
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
                state = m.apply(state, self.effects.get(args[i + 1], {}))
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

    def suite(self, plan):
        return m.run_suite(self.rom, self.baseline, self.jar, self.out, self.temp, plan)


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

        def guard_plus_error(args, output):
            return done(args, 1, GUARD_TEXT + "ERROR: Could not save ROM\n")

        def guard_plus_trace(args, output):
            return done(args, 1, GUARD_TEXT, "java.lang.NullPointerException\n\tat com.uprfvx.X.y(X.java:1)\n")

        for name, fake in (("other", other_error), ("accepted", accepted), ("output", guard_with_output),
                           ("stray", guard_with_stray_file), ("plus error", guard_plus_error),
                           ("plus trace", guard_plus_trace)):
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
        overlays.put("MODE-WILD-GAME", s -> setWildZoneMode(s, Settings.WildPokemonZoneMod.GAME));
        overlays.put("MODE-TYPE-INVERSE", s -> s.setTypeEffectivenessMod(Settings.TypeEffectivenessMod.INVERSE));
        overlays.put("FVX-GEN-003", s -> s.setRandomizeIntroMon(false));
        overlays.put("FVX-TRAIT-001", s -> s.setBaseStatisticsMod(Settings.BaseStatisticsMod.RANDOM));
        overlays.put("FVX-TRAIT-002", s -> s.setBaseStatsFollowEvolutions(true));
        overlays.put("FVX-TRAIT-007", s -> s.setDualTypeOnly(true));
        overlays.put("FVX-TRAIT-017", s -> s.setEvolutionsMod(Settings.EvolutionsMod.RANDOM_EVERY_LEVEL));
        overlays.put("FVX-TRAIT-025", s -> s.setMakeEvolutionsEasier(true));
        overlays.put("FVX-TRAIT-026", s -> s.setEstimateLevelForEvolutionImprovements(true));
        overlays.put("FVX-SST-001", unsupported("FVX-SST-001", "Custom starters need IDs."));
        overlays.put("FVX-MOVE-007", s -> s.setMovesetsMod(Settings.MovesetsMod.COMPLETELY_RANDOM));
        overlays.put("FVX-MOVE-008", s -> s.setStartWithGuaranteedMoves(true));
        overlays.put("FVX-FOE-011", s -> s.setBattleStyle(new BattleStyle(BattleStyle.Modification.RANDOM, BattleStyle.Style.SINGLE_BATTLE)));
        overlays.put("FVX-WILD-001", s -> s.setRandomizeWildPokemon(true));
        overlays.put("FVX-WILD-002", s -> s.setWildPokemonZoneMod(Settings.WildPokemonZoneMod.GAME));
        overlays.put("FVX-TM-001", s -> s.setTmsMod(Settings.TMsMod.RANDOM));
        overlays.put("FVX-TYPE-001", s -> s.setTypeEffectivenessMod(Settings.TypeEffectivenessMod.RANDOM_BALANCED));
        overlays.put("FVX-TYPE-002", s -> s.setInverseTypesRandomImmunities(true));
        overlays.put("FVX-GFX-001", SettingsProfileGenerator::enablePokemonPaletteRandomization);
        overlays.put("FVX-MISC-001", s -> enableMiscTweak(s, MiscTweak.FASTEST_TEXT));
        overlays.put("FVX-MISC-003", s -> enableMiscTweak(s, MiscTweak.RANDOMIZE_PC_POTION));
        overlays.put("FVX-X-HELPER", s -> helper(s, X.Y));
        overlays.put("FVX-X-CONFLICT", s -> {
            s.setTmsMod(Settings.TMsMod.RANDOM);
            s.setTmsMod(Settings.TMsMod.UNCHANGED);
        });
        return Collections.unmodifiableMap(overlays);
    }
'''
SYNTHETIC_SETTINGS = "\n".join("    public %s %s() { return null; }" % pair for pair in (
    ("WildPokemonZoneMod", "getWildPokemonZoneMod"), ("boolean", "isRandomizeWildPokemon"),
    ("TypeEffectivenessMod", "getTypeEffectivenessMod"), ("boolean", "isRandomizeIntroMon"),
    ("BaseStatisticsMod", "getBaseStatisticsMod"), ("boolean", "isBaseStatsFollowEvolutions"),
    ("boolean", "isDualTypeOnly"), ("EvolutionsMod", "getEvolutionsMod"), ("boolean", "isMakeEvolutionsEasier"),
    ("boolean", "useEstimatedLevelsForEvolutionImprovements"), ("MovesetsMod", "getMovesetsMod"),
    ("boolean", "isStartWithGuaranteedMoves"), ("BattleStyle", "getBattleStyle"), ("TMsMod", "getTmsMod"),
    ("boolean", "isInverseTypesRandomImmunities"), ("PokemonPalettesMod", "getPokemonPalettesMod"),
    ("int", "getCurrentMiscTweaks"))) + '''
    public TweakForROMFeedback tweakForRom(RomHandler rh) {
        TweakForROMFeedback feedback = new TweakForROMFeedback();
        if (x) {
            this.setTmsMod(TMsMod.UNCHANGED);
            trainersMod = TrainersMod.RANDOM;
        }
        return feedback;
    }

    // getters and setters
'''
SYNTHETIC_MISC = '''    public static final MiscTweak FASTEST_TEXT = new MiscTweak(1 << 3, "fastestText", 0);
    public static final MiscTweak RANDOMIZE_PC_POTION = new MiscTweak(1 << 5, "pcPotion", 0);
'''
SYNTHETIC_BUNDLES = {family: () for family in m.gm.FAMILIES + ("EVOLUTIONS",)}
SYNTHETIC_BUNDLES.update({"TRAITS": ("FVX-TRAIT-001", "FVX-TRAIT-002", "FVX-TRAIT-025"),
                          "WILD": ("FVX-WILD-001", "FVX-WILD-002"), "TM_TUTOR": ("FVX-TM-001",),
                          "TYPE_EFFECTIVENESS": ("FVX-TYPE-001", "FVX-TYPE-002"),
                          "MISC": ("FVX-MISC-001", "FVX-MISC-003"), "MOVES_MOVESETS": ("FVX-MOVE-007",)})
SYNTHETIC_PROFILES = {name: () for name in m.gm.FULL}
SYNTHETIC_PROFILES["01_TRAITS_SAFE"] = ("FVX-TRAIT-001", "FVX-TRAIT-002")


class SyntheticSource:
    """A temporary Workspace with synthetic, correctly pinned UPR-FVX source text."""

    def __init__(self, testcase, catalog=SYNTHETIC_CATALOG, bundles=SYNTHETIC_BUNDLES, settings=SYNTHETIC_SETTINGS,
                 profiles=SYNTHETIC_PROFILES, misc=SYNTHETIC_MISC, handler=None):
        self.root = Path(tempfile.mkdtemp(prefix="pilot-catalog-"))
        testcase.addCleanup(shutil.rmtree, self.root, True)
        ledger = self.root / m.LEDGER
        ledger.parent.mkdir(parents=True)
        ledger.write_text("feature_id\tfeature_name\nFVX-TRAIT-001\tx\nFVX-OLD-001\told\n")
        texts = {m.CATALOG_SOURCE: catalog, m.SETTINGS_SOURCE: settings, m.MISC_SOURCE: misc}
        if handler is not None:
            texts[m.HANDLER_SOURCE] = handler
        for rel, text in texts.items():
            path = self.root / m.UPR_SOURCE / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        pins = {rel: hashlib.sha256(text.encode()).hexdigest() for rel, text in texts.items()}
        for patcher in (patch.object(m, "SOURCE_PINS", pins),
                        patch.object(m, "family_bundles", return_value=(bundles, profiles))):
            patcher.start()
            testcase.addCleanup(patcher.stop)

    def inventory(self):
        return m.inventory(self.root)

    def plan(self):
        return m.plan_cases(self.inventory())


def by_id(plan):
    return {c.id: c for c in plan}


class InventoryTests(unittest.TestCase):
    def test_every_catalog_and_ledger_id_has_one_visible_disposition(self):
        inv = SyntheticSource(self).inventory()
        self.assertEqual(inv.notes, [])
        self.assertEqual((inv.catalog_ids, inv.ledger_ids, inv.ledger_only), (23, 2, 1))
        states = {k: f.state for k, f in inv.features.items()}
        self.assertEqual(states, {
            "MODE-WILD-GAME": "RUNNABLE", "MODE-TYPE-INVERSE": "RUNNABLE", "FVX-GEN-003": "NOT_RUN",
            "FVX-TRAIT-001": "RUNNABLE", "FVX-TRAIT-002": "RUNNABLE", "FVX-TRAIT-007": "NEEDS_REVIEW",
            "FVX-TRAIT-017": "GUARDED", "FVX-TRAIT-025": "NEEDS_REVIEW", "FVX-TRAIT-026": "NEEDS_REVIEW",
            "FVX-SST-001": "UNSUPPORTED", "FVX-MOVE-007": "GUARDED", "FVX-MOVE-008": "GUARDED",
            "FVX-FOE-011": "NEEDS_REVIEW", "FVX-WILD-001": "RUNNABLE", "FVX-WILD-002": "RUNNABLE",
            "FVX-TM-001": "RUNNABLE", "FVX-TYPE-001": "RUNNABLE", "FVX-TYPE-002": "RUNNABLE",
            "FVX-GFX-001": "NEEDS_REVIEW", "FVX-MISC-001": "RUNNABLE", "FVX-MISC-003": "RUNNABLE",
            "FVX-X-HELPER": "NEEDS_REVIEW", "FVX-X-CONFLICT": "NEEDS_REVIEW", "FVX-OLD-001": "NEEDS_REVIEW"})
        reasons = {k: f.reason for k, f in inv.features.items()}
        self.assertIn("parent FVX-TRAIT-006 has no current overlay", reasons["FVX-TRAIT-007"])
        self.assertIn("parent FVX-MOVE-007 is GUARDED", reasons["FVX-MOVE-008"])
        self.assertIn("parent FVX-FOE-001 has no current overlay", reasons["FVX-FOE-011"])
        self.assertIn("OWNERSHIP_WITNESS_V1", reasons["FVX-TRAIT-025"])
        self.assertIn("not readable", reasons["FVX-TRAIT-026"])     # setter/getter names differ
        self.assertIn("Custom starters need IDs.", reasons["FVX-SST-001"])
        self.assertIn("OFF value", reasons["FVX-GEN-003"])
        self.assertIn("without current overlay", reasons["FVX-OLD-001"])
        self.assertIn("tweakForRom may normalize setTmsMod", reasons["FVX-TM-001"])
        self.assertIn("with FVX-TRAIT-001", reasons["FVX-TRAIT-002"])

    def test_source_derived_deltas(self):
        f = SyntheticSource(self).inventory().features
        self.assertEqual(f["MODE-WILD-GAME"].delta, {"isRandomizeWildPokemon": "true", "getWildPokemonZoneMod": "GAME"})
        self.assertEqual(f["FVX-GFX-001"].delta, {"getPokemonPalettesMod": "RANDOM"})
        self.assertEqual(f["FVX-MISC-003"].delta, {"getCurrentMiscTweaks": "32"})
        self.assertEqual(m.merge([f["FVX-MISC-001"].delta, f["FVX-MISC-003"].delta]), ({"getCurrentMiscTweaks": "40"}, ""))
        self.assertEqual(m.merge([{"a": "1"}, {"a": "2"}]), (None, "a"))
        self.assertIsNone(m.overlay_delta("s -> s.setTmsMod(someVariable)", {"getTmsMod"}, {}))
        self.assertIsNone(m.overlay_delta("s -> s.setTmsMod(Settings.TMsMod.RANDOM)", set(), {}))
        self.assertEqual(m.overlay_delta("s -> s.setBattleStyle(new BattleStyle(BattleStyle.Modification.RANDOM, "
                                         "BattleStyle.Style.SINGLE_BATTLE))", {"getBattleStyle"}, {}),
                         {"getBattleStyle": "RANDOM"})

    def test_missing_or_changed_source_fails_closed(self):
        src = SyntheticSource(self)
        (src.root / m.UPR_SOURCE / m.CATALOG_SOURCE).write_text(SYNTHETIC_CATALOG + "// changed\n")
        inv = src.inventory()
        self.assertIn("differs from the pinned revision", inv.notes[0])
        self.assertEqual({f.state for f in inv.features.values()}, {"NEEDS_REVIEW"})
        self.assertFalse([c for c in m.plan_cases(inv) if c.status in m.RUNNABLE_CASES and c.overlays])
        shutil.rmtree(src.root / m.UPR_SOURCE)
        inv = src.inventory()
        self.assertIn("unavailable", inv.notes[0])
        self.assertEqual(list(inv.features), ["FVX-TRAIT-001", "FVX-OLD-001"])

    def test_tweak_setters_include_direct_field_writes(self):
        self.assertEqual(m.tweak_setters(SYNTHETIC_SETTINGS), {"setTmsMod", "setTrainersMod"})


class CasePlanTests(unittest.TestCase):
    def test_singles_cover_every_feature_once_with_parents_and_reasons(self):
        plan = SyntheticSource(self).plan()
        singles = [c for c in plan if c.kind == "SINGLE"]
        self.assertEqual(len(singles), 24)
        cases = by_id(plan)
        self.assertEqual(cases["SGL-FVX-TRAIT-002"].overlays, ("FVX-TRAIT-001", "FVX-TRAIT-002"))
        self.assertEqual(cases["SGL-FVX-TRAIT-002"].own, (("isBaseStatsFollowEvolutions", "true"),))
        self.assertEqual(cases["SGL-FVX-TYPE-002"].overlays, ("MODE-TYPE-INVERSE", "FVX-TYPE-002"))
        self.assertEqual(cases["SGL-FVX-MOVE-007"].status, "EXPECTED_REJECTION")
        self.assertEqual(cases["SGL-FVX-MOVE-007"].guard, m.LEARNSET_GUARD)
        self.assertIn("RANDOM_EVERY_LEVEL", cases["SGL-FVX-TRAIT-017"].guard)
        self.assertEqual(cases["SGL-FVX-MOVE-008"].status, "GUARDED")
        self.assertEqual(cases["SGL-FVX-SST-001"].status, "UNSUPPORTED")
        self.assertEqual(cases["SGL-FVX-GEN-003"].status, "NOT_RUN")
        self.assertEqual((cases["SGL-FVX-WILD-002"].status, cases["SGL-FVX-WILD-002"].reason),
                         ("DUPLICATE", "same effective settings as SGL-MODE-WILD-GAME"))
        self.assertEqual(cases["SGL-FVX-TM-001"].risk, "high")
        self.assertEqual(cases["SGL-FVX-TRAIT-001"].risk, "normal")
        for c in plan:
            if c.status not in m.RUNNABLE_CASES:
                self.assertTrue(c.reason, c.id)
                self.assertEqual(c.overlays, (), c.id)

    def test_pairs_triples_and_profiles_reuse_legacy_definitions_with_filters(self):
        plan = SyntheticSource(self).plan()
        kinds = [c.kind for c in plan]
        self.assertEqual(kinds.count("PAIR"), 66)
        self.assertEqual(kinds.count("TRIPLE"), 12)
        self.assertEqual(kinds.count("PROFILE"), 1 + len(m.gm.FULL) + len(m.gm.MAXIMUM) + 2)
        cases = by_id(plan)
        pair = cases["PAIR-TRAITS+WILD"]
        self.assertEqual(pair.status, "RUNNABLE")
        self.assertEqual(pair.overlays, ("FVX-TRAIT-001", "FVX-TRAIT-002", "FVX-WILD-001", "FVX-WILD-002"))
        self.assertEqual(set(pair.families), {"TRAIT", "WILD"})
        types = cases["PAIR-TM_TUTOR+TYPE_EFFECTIVENESS"]
        self.assertEqual(types.overlays, ("FVX-TM-001", "FVX-TYPE-001"))
        self.assertIn("left out (contradicts earlier members): FVX-TYPE-002", types.reason)
        self.assertEqual(dict(cases["PAIR-TM_TUTOR+MISC"].delta)["getCurrentMiscTweaks"], "40")
        self.assertEqual(cases["PAIR-GEN_SAFE+TRAITS"].reason, "no runnable overlay in GEN_SAFE")
        self.assertEqual(cases["PAIR-TRAITS+MOVES_MOVESETS"].status, "NEEDS_REVIEW")   # guarded only
        self.assertEqual(cases["FAM-01_TRAITS_SAFE"].status, "DUPLICATE")
        self.assertEqual(cases["PRO-CONTROL"].status, "RUNNABLE")
        self.assertEqual(cases["PRO-CASUAL_NATDEX"].status, "NEEDS_REVIEW")
        for c in plan:
            if c.kind != "SINGLE" and c.status in m.RUNNABLE_CASES:
                self.assertFalse(set(c.overlays) & set(m.gm.RISK_SINGLES), c.id)

    def test_runnable_cases_have_unique_effective_settings_and_stable_seeds(self):
        plan = SyntheticSource(self).plan()
        runnable = [c for c in plan if c.status in m.RUNNABLE_CASES]
        self.assertEqual(len({(c.delta, c.status) for c in runnable}), len(runnable))
        self.assertEqual(len({c.seed for c in plan}), len(plan))
        self.assertEqual([c.seed for c in plan], [c.seed for c in SyntheticSource(self).plan()])
        self.assertTrue(all(re.fullmatch(r"[A-Za-z0-9_+-]{1,80}", c.id) for c in plan))

    def test_plan_prints_inventory_and_case_counts_without_rom_jar_or_process(self):
        src = SyntheticSource(self)
        with patch.object(m, "ROOT", src.root), patch.object(m, "command", side_effect=AssertionError("no")), \
                patch.object(m.gm, "input_digest", side_effect=AssertionError("no ROM")):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(m.main(["--plan"]), 0)
        text = out.getvalue()
        lines = text.splitlines()
        self.assertEqual(sum(line[:1] == "M" for line in lines), 11)
        self.assertEqual(sum(line.startswith("S0") for line in lines), len(m.SINGLE_OPTIONS))
        self.assertIn("Features: 24 IDs (23 current overlays, 2 ledger IDs, 1 ledger-only); RUNNABLE=11, "
                      "GUARDED=3, UNSUPPORTED=1, NEEDS_REVIEW=8, NOT_RUN=1", text)
        self.assertIn("Revision: CFRU 196058edbc2b DPE d887185de1f6 UPR-FVX 1a9b59db3f49", text)
        self.assertRegex(text, r"PAIR\s+66\s+")
        self.assertRegex(text, r"TRIPLE\s+12\s+")
        self.assertIn("  FVX-OLD-001", text)


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.plan = SyntheticSource(self).plan()

    def test_no_implicit_full_run_and_unknown_values_stop(self):
        with self.assertRaisesRegex(m.MatrixError, "no implicit full run"):
            m.select_cases(self.plan)
        for kwargs, message in (({"kinds": ("QUAD",)}, "QUAD"), ({"families": ("NOPE",)}, "NOPE"),
                                ({"risk": "medium"}, "medium"), ({"ids": ("/private/x",)}, "<invalid>"),
                                ({"ids": ("SGL-FVX-SST-001",)}, "UNSUPPORTED: settings-profile refuses"),
                                ({"ids": ("SGL-FVX-WILD-002",)}, "DUPLICATE")):
            with self.assertRaisesRegex(m.MatrixError, message, msg=kwargs):
                m.select_cases(self.plan, **kwargs)

    def test_filters_select_only_runnable_cases(self):
        chosen = m.select_cases(self.plan, kinds=("SINGLE",), families=("TRAIT",))
        self.assertEqual([c.id for c in chosen], ["SGL-FVX-TRAIT-001", "SGL-FVX-TRAIT-002", "SGL-FVX-TRAIT-017"])
        self.assertTrue(all(c.risk == "high" for c in m.select_cases(self.plan, risk="high")))
        self.assertEqual([c.id for c in m.select_cases(self.plan, ids=("PRO-CONTROL",))], ["PRO-CONTROL"])

    def test_large_selection_needs_an_explicit_chunk(self):
        with patch.object(m, "MAX_BATCH", 4):
            with self.assertRaisesRegex(m.MatrixError, r"pass --chunk 1\.\.\d"):
                m.select_cases(self.plan, kinds=("PAIR",))
            first = m.select_cases(self.plan, kinds=("PAIR",), chunk=1)
            second = m.select_cases(self.plan, kinds=("PAIR",), chunk=2)
            self.assertEqual((len(first), len(set(first) & set(second))), (4, 0))
            with self.assertRaisesRegex(m.MatrixError, "--chunk must be"):
                m.select_cases(self.plan, kinds=("PAIR",), chunk=99)


class SuiteRunTests(unittest.TestCase):
    """--suite reuses settings-profile, both observations, generate, reopen and replay."""

    def setUp(self):
        self.src = SyntheticSource(self)
        self.inv = self.src.inventory()
        self.plan = m.plan_cases(self.inv)

    def fixture(self, baseline=None):
        f = Fixture(self, baseline)
        f.upr.effects = {k: v.delta for k, v in self.inv.features.items() if v.delta}
        return f

    def batch(self, *ids):
        return m.select_cases(self.plan, ids=ids)

    def test_batch_passes_with_exact_rejections_and_replay(self):
        f = self.fixture()
        before = f.rom.read_bytes()
        batch = self.batch("PRO-CONTROL", "SGL-FVX-TRAIT-002", "SGL-FVX-MOVE-007", "PAIR-TM_TUTOR+MISC")
        results = f.suite(batch)
        self.assertEqual([(r.settings, r.target, r.status) for r in results.values()], [
            ("PASS", "PASS", "PASS"), ("PASS", "PASS", "PASS"), ("PASS", "PASS", "EXPECTED_REJECTION"),
            ("PASS", "PASS", "PASS")])
        self.assertEqual([r.replay for r in results.values()], ["PASS", "PASS", "-", "PASS"])
        lines, overall = m.suite_report_lines(results, batch)
        self.assertEqual(overall, "PASS")
        text = "\n".join(lines)
        self.assertIn("PASS_GENERATION_REOPEN_REPLAY=3, EXPECTED_REJECTION=1", text)
        self.assertNotIn("FEATURE_VERIFIED", text.replace("no FEATURE_VERIFIED claim", ""))
        self.assertEqual(f.rom.read_bytes(), before)
        self.assertEqual(sorted(p.name for p in f.out.iterdir()), sorted(
            ["settings", "PRO-CONTROL", "PRO-CONTROL-replay", "SGL-FVX-TRAIT-002", "SGL-FVX-TRAIT-002-replay",
             "SGL-FVX-MOVE-007", "PAIR-TM_TUTOR+MISC", "PAIR-TM_TUTOR+MISC-replay"]))
        profiles = [a for k, a in f.upr.calls if k == "profile"]
        self.assertEqual(profiles[0][-2:], ["--profile", "00_BASELINE"])
        self.assertEqual([a for a in profiles[1] if a.startswith("FVX-")], ["FVX-TRAIT-001", "FVX-TRAIT-002"])
        kinds = [k for k, _ in f.upr.calls]
        self.assertEqual(kinds[:7], ["observe"] + ["profile"] * 4 + ["observe", "observe"])

    def test_exact_non_learnset_guard_is_expected_rejection(self):
        f = self.fixture()
        case, = self.batch("SGL-FVX-TRAIT-017")
        f.upr.cli_override[case.seed] = lambda args, output: done(args, 1, rejection(case.guard))
        self.assertEqual(f.suite([case])[case.id].detail, "exact guard, no output")

    def test_wrong_rejection_fails_and_later_cases_are_not_run(self):
        f = self.fixture()
        batch = self.batch("SGL-FVX-TRAIT-017", "SGL-FVX-TYPE-001")
        self.assertEqual(batch[0].id, "SGL-FVX-TRAIT-017")
        f.upr.cli_override[batch[0].seed] = lambda args, output: done(args, 1, "", "java.lang.NullPointerException")
        results = f.suite(batch)
        self.assertEqual([r.status for r in results.values()], ["FAIL", "NOT_RUN"])
        self.assertEqual(results["SGL-FVX-TRAIT-017"].detail, "different or additional failure (see local cli.log)")

    def test_settings_drift_or_noop_is_needs_review_and_never_generated(self):
        state = neutral()
        state["isBaseStatsFollowEvolutions"] = "true"      # baseline already holds TRAIT-002's change
        f = self.fixture(state)
        f.upr.extra_effect["FVX-TM-001"] = {"isRaceMode": "true"}
        batch = self.batch("SGL-FVX-TRAIT-002", "SGL-FVX-TM-001", "SGL-FVX-TRAIT-001")
        results = f.suite(batch)
        self.assertEqual({k: (r.settings, r.status) for k, r in results.items()}, {
            "SGL-FVX-TRAIT-002": ("NO-OP", "NEEDS_REVIEW"), "SGL-FVX-TM-001": ("DRIFT", "NEEDS_REVIEW"),
            "SGL-FVX-TRAIT-001": ("PASS", "PASS")})
        self.assertIn("isRaceMode", results["SGL-FVX-TM-001"].detail)
        self.assertFalse((f.out / "SGL-FVX-TRAIT-002").exists())
        self.assertEqual(m.suite_report_lines(results, batch)[1], "INCOMPLETE")

    def test_target_normalization_is_needs_review(self):
        f = self.fixture()
        f.upr.tweak = {"getTmsMod": "UNCHANGED"}
        results = f.suite(self.batch("SGL-FVX-TM-001", "SGL-MODE-TYPE-INVERSE"))
        self.assertEqual({k: (r.target, r.status) for k, r in results.items()}, {
            "SGL-FVX-TM-001": ("NEEDS_REVIEW", "NEEDS_REVIEW"), "SGL-MODE-TYPE-INVERSE": ("PASS", "PASS")})

    def test_generation_reopen_and_replay_failures_fail_fast(self):
        for failure in ("cli", "reopen", "replay"):
            f = self.fixture()
            batch = self.batch("SGL-FVX-TRAIT-001", "SGL-MODE-TYPE-INVERSE")
            seed = batch[0].seed
            if failure == "cli":
                f.upr.cli_fail.add(seed)
            elif failure == "reopen":
                f.upr.reopen_fail.add(seed)
            else:
                f.upr.nondeterministic = True
            results = f.suite(batch)
            self.assertEqual([r.status for r in results.values()], ["FAIL", "NOT_RUN"], failure)

    def test_source_rom_change_stops(self):
        f = self.fixture()
        real = f.upr.cli

        def tamper(args):
            f.rom.write_text("changed")
            return real(args)
        f.upr.cli = tamper
        with self.assertRaisesRegex(m.MatrixError, "Source ROM changed"):
            f.suite(self.batch("SGL-FVX-TRAIT-001"))

    def test_main_suite_is_explicit_bounded_and_sanitized(self):
        f = self.fixture()
        seed = by_id(self.plan)["SGL-FVX-TYPE-001"].seed
        f.upr.cli_fail.add(seed)
        out_dir = f.dir / "05_builds" / "run"
        out_dir.parent.mkdir()
        common = ["--confirm", m.CONFIRM_TOKEN, "--rom", str(f.rom), "--baseline", str(f.baseline),
                  "--out", str(out_dir), "--jar", str(f.jar)]
        with patch.object(m, "ROOT", self.src.root), \
                patch.object(m, "revision_lines", return_value=["UPR-FVX: 1a9b59db3f49 MATCH"]):
            for extra, message in (([], "no implicit full run"), (["--case", "SGL-FVX-SST-001"], "UNSUPPORTED")):
                err = io.StringIO()
                with contextlib.redirect_stderr(err):
                    self.assertEqual(m.main(["--suite"] + common + extra), 2)
                self.assertIn(message, err.getvalue())
            self.assertEqual(f.upr.calls, [])
            self.assertFalse(out_dir.exists())
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                rc = m.main(["--suite", "--kind", "SINGLE", "--family", "TRAIT,TYPE"] + common)
        text = stdout.getvalue() + stderr.getvalue()
        self.assertEqual(rc, 1)
        self.assertIn("#750 comprehensive matrix batch (6 cases)", text)
        self.assertIn("Revision: CFRU 196058edbc2b", text)
        self.assertIn("SUITE=FAIL", text)
        for leak in (str(f.dir), "/private/secret", "IllegalStateException", "boom", ".gba", ".rnqs"):
            self.assertNotIn(leak, text)

    def test_changed_source_stops_suite(self):
        f = self.fixture()
        (self.src.root / m.UPR_SOURCE / m.MISC_SOURCE).write_text("changed")
        err = io.StringIO()
        with patch.object(m, "ROOT", self.src.root), contextlib.redirect_stderr(err):
            rc = m.main(["--suite", "--kind", "SINGLE", "--confirm", m.CONFIRM_TOKEN, "--rom", str(f.rom),
                         "--baseline", str(f.baseline), "--out", str(f.dir / "05_builds" / "x"), "--jar", str(f.jar)])
        self.assertEqual(rc, 2)
        self.assertIn("differs from the pinned revision", err.getvalue())
        self.assertEqual(f.upr.calls, [])


class RepairTests(unittest.TestCase):
    """#751 repairs: release prerequisites, exact rejections, family representation."""

    def test_high_risk_options_without_accepted_prerequisites_are_needs_review(self):
        catalog = SYNTHETIC_CATALOG.replace("        return Collections", "".join(
            f'        overlays.put("{fid}", s -> s.setTmsMod(Settings.TMsMod.RANDOM));\n'
            for fid in ("FVX-TRAIT-027", "FVX-ITEM-010", "FVX-GFX-002", "FVX-GFX-004")) + "        return Collections")
        inv = SyntheticSource(self, catalog).inventory()
        for fid in ("FVX-TRAIT-027", "FVX-ITEM-010", "FVX-GFX-002", "FVX-GFX-004", "FVX-GFX-001"):
            f = inv.features[fid]
            self.assertEqual(f.state, "NEEDS_REVIEW", fid)
            self.assertIn("high risk, prerequisite not accepted", f.reason)
            self.assertRegex(f.reason, r"#7[0-9]{2}")
            self.assertIsNotNone(f.delta)      # technically readable, but not released
        plan = by_id(m.plan_cases(inv))
        self.assertEqual(plan["SGL-FVX-ITEM-010"].status, "NEEDS_REVIEW")
        self.assertTrue(set(m.PREREQUISITES) >= set(m.gm.RISK_SINGLES))

    def test_exact_rejection_requires_the_guard_alone(self):
        guard = m.LEARNSET_GUARD
        self.assertTrue(m.exact_rejection(rejection(guard), guard))
        self.assertTrue(m.exact_rejection("WARNING: Settings file older\n" + rejection(guard), guard))
        for name, text in (
                ("other exception", rejection(guard).replace("exceptions.Randomization", "exceptions.RomIO")),
                ("guard inside another error", m.GUARD_LINE + "RomIOException: x " + guard + "\nERROR: Randomization failed\n"),
                ("additional error", rejection(guard) + "ERROR: Could not save ROM\n"),
                ("stack trace", rejection(guard) + "\tat com.uprfvx.random.GameRandomizer.randomize(G.java:1)\n"),
                ("cause", rejection(guard) + "Caused by: java.lang.IllegalStateException\n"),
                ("guard twice", m.GUARD_LINE + guard + "\n" + rejection(guard)),
                ("no CLI failure line", m.GUARD_LINE + guard + "\n"),
                ("old substring format", "Randomization failed: com.uprfvx.random." + guard + "\nRandomization failed\n")):
            self.assertFalse(m.exact_rejection(text, guard), name)

    def test_expected_guard_plus_independent_error_is_fail(self):
        src = SyntheticSource(self)
        inv = src.inventory()
        plan = m.plan_cases(inv)
        case, = m.select_cases(plan, ids=("SGL-FVX-TRAIT-017",))
        f = Fixture(self)
        f.upr.effects = {k: v.delta for k, v in inv.features.items() if v.delta}
        f.upr.cli_override[case.seed] = lambda args, output: done(
            args, 1, rejection(case.guard), "Exception in thread \"main\" java.lang.OutOfMemoryError\n")
        r = f.suite([case])[case.id]
        self.assertEqual((r.status, r.detail), ("FAIL", "different or additional failure (see local cli.log)"))

    def test_family_filtered_away_by_conflicts_is_never_runnable(self):
        bundles = dict(SYNTHETIC_BUNDLES, TYPE_EFFECTIVENESS=("FVX-TYPE-001",), FOE=("MODE-TYPE-INVERSE",))
        plan = by_id(SyntheticSource(self, bundles=bundles).plan())
        lost = plan["PAIR-FOE+TYPE_EFFECTIVENESS"]
        self.assertEqual(lost.status, "NEEDS_REVIEW")
        self.assertIn("no effective change left for TYPE_EFFECTIVENESS", lost.reason)
        self.assertIn("FVX-TYPE-001", lost.reason)
        kept = plan["PAIR-TRAITS+TYPE_EFFECTIVENESS"]
        self.assertEqual(kept.status, "RUNNABLE")
        self.assertEqual([f for f, change in kept.groups if change], ["TRAITS", "TYPE_EFFECTIVENESS"])

    def test_every_runnable_composite_keeps_each_named_family(self):
        for c in SyntheticSource(self).plan():
            if c.kind in ("PAIR", "TRIPLE") and c.status in m.RUNNABLE_CASES:
                self.assertEqual(len(c.groups), len(c.id.split("-", 1)[1].split("+")), c.id)
                self.assertTrue(all(change for _, change in c.groups), c.id)

    def test_family_made_ineffective_by_normalization_is_needs_review(self):
        src = SyntheticSource(self)
        inv = src.inventory()
        plan = m.plan_cases(inv)
        batch = m.select_cases(plan, ids=("PAIR-TRAITS+TM_TUTOR", "PAIR-WILD+TM_TUTOR"))
        f = Fixture(self)
        f.upr.effects = {k: v.delta for k, v in inv.features.items() if v.delta}
        # tweakForRom forces the TRAITS change onto every file: the case still matches, but TRAITS adds nothing.
        f.upr.tweak = {"getBaseStatisticsMod": "RANDOM", "isBaseStatsFollowEvolutions": "true"}
        results = f.suite(batch)
        r = results["PAIR-TRAITS+TM_TUTOR"]
        self.assertEqual((r.settings, r.target, r.status), ("PASS", "NEEDS_REVIEW", "NEEDS_REVIEW"))
        self.assertIn("change of TRAIT", r.detail)
        self.assertFalse((f.out / "PAIR-TRAITS+TM_TUTOR").exists())
        self.assertEqual(results["PAIR-WILD+TM_TUTOR"].status, "PASS")

    def test_single_made_ineffective_by_normalization_is_needs_review(self):
        inv = SyntheticSource(self).inventory()
        case, = m.select_cases(m.plan_cases(inv), ids=("SGL-FVX-TRAIT-002",))
        f = Fixture(self)
        f.upr.effects = {k: v.delta for k, v in inv.features.items() if v.delta}
        f.upr.tweak = {"isBaseStatsFollowEvolutions": "true"}
        r = f.suite([case])[case.id]
        self.assertEqual((r.target, r.status), ("NEEDS_REVIEW", "NEEDS_REVIEW"))


class SerializationDefectTests(unittest.TestCase):
    """#752: FVX-WILD-007 sets level 45; the .rnqs keeps 3 bits and reads back 5."""

    def source(self):
        catalog = SYNTHETIC_CATALOG.replace("        return Collections", (
            '        overlays.put("FVX-WILD-007", s -> {\n            s.setUseMinimumCatchRate(true);\n'
            '            s.setMinimumCatchRateLevel(45);\n        });\n        return Collections'))
        settings = SYNTHETIC_SETTINGS.replace("    public TweakForROMFeedback", (
            "    public boolean isUseMinimumCatchRate() { return false; }\n"
            "    public int getMinimumCatchRateLevel() { return 1; }\n    public TweakForROMFeedback"))
        bundles = dict(SYNTHETIC_BUNDLES, WILD=("FVX-WILD-001", "FVX-WILD-007", "FVX-WILD-002"))
        profiles = dict(SYNTHETIC_PROFILES, **{"05_WILD_FULL": ("FVX-WILD-001", "FVX-WILD-007")})
        return SyntheticSource(self, catalog, bundles, settings, profiles)

    def test_round_trip_defect_is_needs_review_with_the_source_delta_kept(self):
        f = self.source().inventory().features["FVX-WILD-007"]
        self.assertEqual(f.state, "NEEDS_REVIEW")
        self.assertIn("serialization defect", f.reason)
        self.assertIn("#752", f.reason)
        # The declared value stays the source's 45; nothing is rewritten to 5.
        self.assertEqual(f.delta, {"isUseMinimumCatchRate": "true", "getMinimumCatchRateLevel": "45"})

    def test_never_part_of_a_runnable_single_or_composite(self):
        plan = self.source().plan()
        cases = by_id(plan)
        self.assertEqual(cases["SGL-FVX-WILD-007"].status, "NEEDS_REVIEW")
        with self.assertRaisesRegex(m.MatrixError, "#752"):
            m.select_cases(plan, ids=("SGL-FVX-WILD-007",))
        for c in plan:
            if c.status in m.RUNNABLE_CASES:
                self.assertNotIn("FVX-WILD-007", c.overlays, c.id)
                self.assertNotIn("getMinimumCatchRateLevel", dict(c.delta), c.id)
        pair = cases["PAIR-WILD+TM_TUTOR"]
        self.assertEqual((pair.status, pair.overlays), ("RUNNABLE", ("FVX-WILD-001", "FVX-WILD-002", "FVX-TM-001")))
        self.assertEqual(cases["FAM-05_WILD_FULL"].status, "DUPLICATE")       # only WILD-001 remains
        self.assertNotIn("FVX-WILD-007", m.select_cases(plan, families=("WILD",))[0].overlays)

    def test_drift_check_still_catches_the_round_trip(self):
        src = self.source()
        inv = src.inventory()
        case, = m.select_cases(m.plan_cases(inv), ids=("SGL-FVX-WILD-001",))
        f = Fixture(self)
        f.upr.effects = {k: v.delta for k, v in inv.features.items() if v.delta}
        f.upr.extra_effect["FVX-WILD-001"] = {"getMinimumCatchRateLevel": "5"}    # what the round trip does
        r = f.suite([case])[case.id]
        self.assertEqual((r.settings, r.status), ("DRIFT", "NEEDS_REVIEW"))
        self.assertIn("getMinimumCatchRateLevel", r.detail)
        self.assertEqual(f.upr.count("cli"), 0)


class TargetNormalizationTests(unittest.TestCase):
    """tweakForRom resets limitPokemon and useTimeBasedEncounters for every CFRU/DPE pilot ROM."""

    def source(self, branches=True):
        catalog = SYNTHETIC_CATALOG.replace("        return Collections", (
            '        overlays.put("FVX-GEN-001", s -> s.setLimitPokemon(true));\n'
            '        overlays.put("MODE-GEN-LIMIT-1-9", s -> setGenLimit(s, true));\n'
            '        overlays.put("MODE-ALLOW-REGIONAL-FORMS", s -> s.setAllowRegionalFormsAcrossGenLimit(true));\n'
            '        overlays.put("FVX-SPECIAL-WILD-001", s -> s.setUseTimeBasedEncounters(true));\n'
            '        return Collections')) + (
            "\n    private static void setGenLimit(Settings settings, boolean allowEvolutionaryRelatives) {\n"
            "        GenRestrictions restrictions = new GenRestrictions();\n"
            "        restrictions.setAllowEvolutionaryRelatives(allowEvolutionaryRelatives);\n"
            "        settings.setLimitPokemon(true);\n"
            "        settings.setCurrentRestrictions(restrictions);\n    }\n")
        tweaks = ("        if (rh instanceof Gen3RomHandler && !rh.isRomValid(null)) {\n"
                  "            this.currentRestrictions = null;\n            this.setLimitPokemon(false);\n        }\n"
                  "        if (!rh.hasTimeBasedEncounters()) {\n"
                  "            this.setUseTimeBasedEncounters(false);\n        }\n") if branches else ""
        settings = SYNTHETIC_SETTINGS.replace("    public TweakForROMFeedback", (
            "    public boolean isLimitPokemon() { return false; }\n"
            "    public boolean isAllowRegionalFormsAcrossGenLimit() { return false; }\n"
            "    public boolean isUseTimeBasedEncounters() { return false; }\n"
            "    public GenRestrictions getCurrentRestrictions() { return null; }\n"
            "    public TweakForROMFeedback")).replace("        return feedback;", tweaks + "        return feedback;")
        bundles = dict(SYNTHETIC_BUNDLES, GEN_SAFE=("MODE-GEN-LIMIT-1-9", "MODE-ALLOW-REGIONAL-FORMS"),
                       SPECIAL_WILD=("FVX-SPECIAL-WILD-001",))
        profiles = dict(SYNTHETIC_PROFILES, **{"11_SPECIAL_WILD": ("FVX-SPECIAL-WILD-001",)})
        return SyntheticSource(self, catalog, bundles, settings, profiles)

    def test_both_normalizations_are_needs_review_from_the_source(self):
        features = self.source().inventory().features
        gen, limit, regional, timed = (features[i] for i in ("FVX-GEN-001", "MODE-GEN-LIMIT-1-9",
                                                             "MODE-ALLOW-REGIONAL-FORMS", "FVX-SPECIAL-WILD-001"))
        self.assertEqual({gen.state, limit.state, regional.state, timed.state}, {"NEEDS_REVIEW"})
        self.assertIn("ineffective on the pilot target: setLimitPokemon", gen.reason)
        self.assertIn("Gen3RomHandler && !isRomValid(null)", gen.reason)
        self.assertEqual(gen.delta, {"isLimitPokemon": "true"})          # declared change kept as is
        self.assertIn("(via setGenLimit): setLimitPokemon", limit.reason)  # helper resolved from its source
        self.assertEqual(regional.reason, "parent FVX-GEN-001 is NEEDS_REVIEW")
        self.assertIn("setUseTimeBasedEncounters", timed.reason)
        self.assertIn("hasTimeBasedEncounters()", timed.reason)

    def test_only_a_setter_tweakForRom_resets_is_target_ineffective(self):
        src = self.source(branches=False)
        features = src.inventory().features
        self.assertEqual(features["FVX-GEN-001"].state, "RUNNABLE")
        self.assertEqual(features["MODE-ALLOW-REGIONAL-FORMS"].state, "RUNNABLE")
        self.assertEqual(features["FVX-SPECIAL-WILD-001"].state, "RUNNABLE")
        # setGenLimit's restrictions object is no plain constant: still unreadable, never runnable.
        self.assertEqual(features["MODE-GEN-LIMIT-1-9"].reason, "overlay source not readable as exact Settings changes")
        catalog = (src.root / m.UPR_SOURCE / m.CATALOG_SOURCE).read_text()
        self.assertEqual(m.helper_setters("s -> setGenLimit(s, true)", catalog),
                         {"setLimitPokemon", "setCurrentRestrictions"})
        self.assertEqual(m.helper_setters("s -> missing(s, true)", "no helper here"), set())

    def test_families_without_an_effective_member_are_not_offered(self):
        plan = self.source().plan()
        cases = by_id(plan)
        for cid in ("SGL-FVX-GEN-001", "SGL-MODE-ALLOW-REGIONAL-FORMS", "SGL-FVX-SPECIAL-WILD-001"):
            self.assertEqual(cases[cid].status, "NEEDS_REVIEW", cid)
        self.assertEqual((cases["PAIR-GEN_SAFE+TRAITS"].status, cases["PAIR-GEN_SAFE+TRAITS"].reason),
                         ("NEEDS_REVIEW", "no runnable overlay in GEN_SAFE"))
        self.assertEqual(cases["PAIR-TRAITS+SPECIAL_WILD"].reason, "no runnable overlay in SPECIAL_WILD")
        self.assertEqual(cases["PAIR-GEN_SAFE+SPECIAL_WILD"].reason, "no runnable overlay in GEN_SAFE,SPECIAL_WILD")
        self.assertEqual(cases["FAM-11_SPECIAL_WILD"].status, "NEEDS_REVIEW")
        self.assertEqual(cases["PAIR-TRAITS+WILD"].status, "RUNNABLE")       # unaffected families keep running
        normalized = {"FVX-GEN-001", "MODE-GEN-LIMIT-1-9", "MODE-ALLOW-REGIONAL-FORMS", "FVX-SPECIAL-WILD-001"}
        for c in plan:
            if c.status in m.RUNNABLE_CASES:
                self.assertFalse(set(c.overlays) & normalized, c.id)
                self.assertFalse({"isLimitPokemon", "isUseTimeBasedEncounters"} & dict(c.delta).keys(), c.id)
            if "GEN_SAFE" in c.id or "SPECIAL_WILD" in c.id:
                self.assertNotIn(c.status, m.RUNNABLE_CASES, c.id)
        with self.assertRaisesRegex(m.MatrixError, "no runnable overlay in GEN_SAFE"):
            m.select_cases(plan, ids=("PAIR-GEN_SAFE+TRAITS",))

    def test_drift_check_still_catches_both_normalizations(self):
        with patch.object(m, "TARGET_NORMALIZED", {}):     # without the static classification
            inv = self.source().inventory()
        plan = m.plan_cases(inv)
        cases = m.select_cases(plan, ids=("SGL-FVX-GEN-001", "PAIR-TRAITS+SPECIAL_WILD"))
        self.assertEqual([c.status for c in cases], ["RUNNABLE", "RUNNABLE"])
        f = Fixture(self)
        f.upr.effects = {k: v.delta for k, v in inv.features.items() if v.delta}
        f.upr.tweak = {"isLimitPokemon": "false", "isUseTimeBasedEncounters": "false"}
        results = f.suite(cases)
        self.assertEqual([results[c.id].status for c in cases], ["NEEDS_REVIEW", "NEEDS_REVIEW"])
        self.assertIn("tweakForRom changed isLimitPokemon", results["SGL-FVX-GEN-001"].detail)
        self.assertIn("tweakForRom changed isUseTimeBasedEncounters", results["PAIR-TRAITS+SPECIAL_WILD"].detail)
        self.assertEqual(f.upr.count("cli"), 0)


class TargetValueNormalizationTests(unittest.TestCase):
    """tweakForRom turns TrainersMod MAINPLAYTHROUGH into RANDOM outside Gen 5; other modes stay."""

    MODES = {"MODE-FOE-RANDOM": "RANDOM", "MODE-FOE-EVEN-DISTRIBUTION": "DISTRIBUTED",
             "MODE-FOE-MAIN-PLAYTHROUGH": "MAINPLAYTHROUGH", "MODE-FOE-TYPE-THEMED": "TYPE_THEMED",
             "MODE-FOE-KEEP-THEMED": "KEEP_THEMED"}

    def source(self, branch=True):
        catalog = SYNTHETIC_CATALOG.replace("        return Collections", "".join(
            f'        overlays.put("{fid}", s -> s.setTrainersMod(Settings.TrainersMod.{value}));\n'
            for fid, value in self.MODES.items()) + "        return Collections")
        gen5 = ("        if (rh.generationOfPokemon() != 5) {\n"
                "            if (trainersMod == TrainersMod.MAINPLAYTHROUGH) {\n"
                "                trainersMod = TrainersMod.RANDOM;\n            }\n        }\n") if branch else (
                "        if (rh.generationOfPokemon() != 5) {\n            if (y) {\n"
                "                trainersMod = TrainersMod.RANDOM;\n            }\n        }\n")
        settings = SYNTHETIC_SETTINGS.replace("    public TweakForROMFeedback", (
            "    public TrainersMod getTrainersMod() { return null; }\n    public TweakForROMFeedback")).replace(
            "        return feedback;", gen5 + "        return feedback;")
        bundles = dict(SYNTHETIC_BUNDLES, FOE=("MODE-FOE-MAIN-PLAYTHROUGH",),
                       TM_TUTOR=("MODE-FOE-MAIN-PLAYTHROUGH", "FVX-TM-001"))
        profiles = dict(SYNTHETIC_PROFILES, **{"04_FOE_BASE": ("MODE-FOE-MAIN-PLAYTHROUGH", "MODE-FOE-RANDOM")})
        return SyntheticSource(self, catalog, bundles, settings, profiles)

    def test_only_the_reset_value_is_needs_review(self):
        features = self.source().inventory().features
        main = features["MODE-FOE-MAIN-PLAYTHROUGH"]
        self.assertEqual(main.state, "NEEDS_REVIEW")
        self.assertEqual(main.reason, "value not kept on the pilot target: getTrainersMod=MAINPLAYTHROUGH: "
                                      + m.TARGET_NORMALIZED_VALUES[("getTrainersMod", "MAINPLAYTHROUGH")][1])
        self.assertEqual(main.delta, {"getTrainersMod": "MAINPLAYTHROUGH"})   # nothing rewritten to RANDOM
        for fid, value in self.MODES.items():
            if value != "MAINPLAYTHROUGH":
                self.assertEqual((features[fid].state, features[fid].delta), ("RUNNABLE", {"getTrainersMod": value}))

    def test_needs_the_exact_source_condition(self):
        self.assertEqual(self.source(branch=False).inventory().features["MODE-FOE-MAIN-PLAYTHROUGH"].state,
                         "RUNNABLE")

    def test_never_part_of_a_runnable_single_or_composite(self):
        plan = self.source().plan()
        cases = by_id(plan)
        self.assertEqual(cases["SGL-MODE-FOE-MAIN-PLAYTHROUGH"].status, "NEEDS_REVIEW")
        with self.assertRaisesRegex(m.MatrixError, "value not kept on the pilot target"):
            m.select_cases(plan, ids=("SGL-MODE-FOE-MAIN-PLAYTHROUGH",))
        for c in plan:
            if c.status in m.RUNNABLE_CASES:
                self.assertNotIn("MODE-FOE-MAIN-PLAYTHROUGH", c.overlays, c.id)
                self.assertNotEqual(dict(c.delta).get("getTrainersMod"), "MAINPLAYTHROUGH", c.id)
        self.assertEqual(cases["PAIR-TRAITS+FOE"].reason, "no runnable overlay in FOE")
        self.assertEqual(cases["PAIR-WILD+TM_TUTOR"].overlays, ("FVX-WILD-001", "FVX-WILD-002", "FVX-TM-001"))
        fam = cases["FAM-04_FOE_BASE"]                               # only MODE-FOE-RANDOM is left
        self.assertEqual((fam.status, fam.reason), ("DUPLICATE", "same effective settings as SGL-MODE-FOE-RANDOM"))

    def test_drift_check_still_catches_the_reset(self):
        with patch.object(m, "TARGET_NORMALIZED_VALUES", {}):      # without the static classification
            inv = self.source().inventory()
        case, = m.select_cases(m.plan_cases(inv), ids=("SGL-MODE-FOE-MAIN-PLAYTHROUGH",))
        f = Fixture(self)
        f.upr.effects = {k: v.delta for k, v in inv.features.items() if v.delta}
        f.upr.tweak = {"getTrainersMod": "RANDOM"}
        r = f.suite([case])[case.id]
        self.assertEqual((r.target, r.status), ("NEEDS_REVIEW", "NEEDS_REVIEW"))
        self.assertIn("tweakForRom changed getTrainersMod", r.detail)
        self.assertEqual(f.upr.count("cli"), 0)


SYNTHETIC_HANDLER = '''    public int miscTweaksAvailable() {
        int available = MiscTweak.LOWER_CASE_POKEMON_NAMES.getValue();
        if (!isCfruDpeGen9BpreProfile() && romEntry.getIntValue("NationalDexTweakPossible") != 0) {
            available |= MiscTweak.NATIONAL_DEX_AT_START.getValue();
        }
        if (usesCfruDpeBpreRunningLogic()
                ? cfruDpeRunningLogicAlreadyAllowsIndoorRunningForDiagnostics(rom)
                : romEntry.getIntValue("RunIndoorsTweakOffset") > 0) {
            available |= MiscTweak.RUNNING_SHOES_INDOORS.getValue();
        }
        if (!usesCfruDpeBpreRunningLogic() || findCfruDpeRunningFlagBranchOffsetForDiagnostics(rom) >= 0) {
            available |= MiscTweak.RUN_WITHOUT_RUNNING_SHOES.getValue();
        }
        return available;
    }
'''


class TargetMiscTweakTests(unittest.TestCase):
    """tweakForRom masks the misc tweaks with Gen3RomHandler.miscTweaksAvailable()."""

    AFFECTED = {"FVX-MISC-002": "RUNNING_SHOES_INDOORS", "FVX-MISC-004": "NATIONAL_DEX_AT_START",
                "FVX-MISC-010": "RUN_WITHOUT_RUNNING_SHOES"}

    def source(self, handler=SYNTHETIC_HANDLER, filtered=True):
        catalog = SYNTHETIC_CATALOG.replace("        return Collections", "".join(
            f'        overlays.put("{fid}", s -> enableMiscTweak(s, MiscTweak.{name}));\n'
            for fid, name in self.AFFECTED.items()) + "        return Collections")
        misc = SYNTHETIC_MISC + (
            '    public static final MiscTweak RUNNING_SHOES_INDOORS = new MiscTweak(1 << 4, "runningShoes", 0);\n'
            '    public static final MiscTweak NATIONAL_DEX_AT_START = new MiscTweak(1 << 7, "nationalDex", 0);\n'
            '    public static final MiscTweak RUN_WITHOUT_RUNNING_SHOES = new MiscTweak(1 << 18, "runWithout", 0);\n')
        settings = SYNTHETIC_SETTINGS.replace("        return feedback;", (
            "        int oldMiscTweaks = this.currentMiscTweaks;\n"
            "        this.currentMiscTweaks &= rh.miscTweaksAvailable();\n" if filtered else "")
            + "        return feedback;")
        bundles = dict(SYNTHETIC_BUNDLES, MISC=("FVX-MISC-001", "FVX-MISC-002", "FVX-MISC-004", "FVX-MISC-003",
                                                "FVX-MISC-010"))
        profiles = dict(SYNTHETIC_PROFILES, **{"10_MISC_SAFE": ("FVX-MISC-001", "FVX-MISC-010", "FVX-MISC-003")})
        return SyntheticSource(self, catalog, bundles, settings, profiles, misc=misc, handler=handler)

    def test_each_unavailable_bit_has_its_own_reason_and_keeps_its_delta(self):
        features = self.source().inventory().features
        national, indoors, without = (features[i] for i in ("FVX-MISC-004", "FVX-MISC-002", "FVX-MISC-010"))
        self.assertEqual({national.state, indoors.state, without.state}, {"NEEDS_REVIEW"})
        self.assertIn("MiscTweak.NATIONAL_DEX_AT_START (1 << 7): profile exclusion", national.reason)
        self.assertIn("!isCfruDpeGen9BpreProfile()", national.reason)
        self.assertNotIn("ROM-signature", national.reason)
        self.assertIn("MiscTweak.RUNNING_SHOES_INDOORS (1 << 4): ROM-signature dependent", indoors.reason)
        self.assertIn("cfruDpeRunningLogicAlreadyAllowsIndoorRunningForDiagnostics(rom)", indoors.reason)
        self.assertIn("MiscTweak.RUN_WITHOUT_RUNNING_SHOES (1 << 18): ROM-signature dependent", without.reason)
        self.assertIn("findCfruDpeRunningFlagBranchOffsetForDiagnostics(rom) >= 0", without.reason)
        for f in (indoors, without):
            self.assertIn("not a claim about every CFRU/DPE ROM", f.reason)
        self.assertEqual([f.delta for f in (indoors, national, without)],
                         [{m.MISC_KEY: "16"}, {m.MISC_KEY: "128"}, {m.MISC_KEY: "262144"}])
        self.assertEqual((features["FVX-MISC-001"].state, features["FVX-MISC-003"].state), ("RUNNABLE", "RUNNABLE"))

    def test_needs_the_handler_condition_and_the_settings_filter(self):
        no_profile_exclusion = SYNTHETIC_HANDLER.replace("!isCfruDpeGen9BpreProfile() && ", "")
        for kwargs, review in (({"handler": None}, set()), ({"filtered": False}, set()),
                               ({"handler": no_profile_exclusion}, {"FVX-MISC-002", "FVX-MISC-010"})):
            features = self.source(**kwargs).inventory().features
            self.assertEqual({k for k in self.AFFECTED if features[k].state == "NEEDS_REVIEW"}, review, kwargs)
            self.assertEqual({features[k].state for k in self.AFFECTED if k not in review}, {"RUNNABLE"}, kwargs)

    def test_never_part_of_a_runnable_single_or_composite(self):
        plan = self.source().plan()
        cases = by_id(plan)
        for fid in self.AFFECTED:
            self.assertEqual(cases["SGL-" + fid].status, "NEEDS_REVIEW", fid)
            with self.assertRaisesRegex(m.MatrixError, "misc tweak not kept on the pilot target"):
                m.select_cases(plan, ids=("SGL-" + fid,))
        for c in plan:
            if c.status in m.RUNNABLE_CASES:
                self.assertFalse(set(c.overlays) & set(self.AFFECTED), c.id)
                self.assertFalse(int(dict(c.delta).get(m.MISC_KEY, "0")) & (16 | 128 | 262144), c.id)
        self.assertEqual(cases["PAIR-WILD+MISC"].overlays, ("FVX-WILD-001", "FVX-WILD-002", "FVX-MISC-001",
                                                            "FVX-MISC-003"))
        self.assertEqual((cases["FAM-10_MISC_SAFE"].status, cases["FAM-10_MISC_SAFE"].overlays),
                         ("RUNNABLE", ("FVX-MISC-001", "FVX-MISC-003")))

    def test_drift_check_still_catches_all_three_missing_bits(self):
        with patch.object(m, "TARGET_MISC_UNAVAILABLE", {}):      # without the static classification
            inv = self.source().inventory()
        cases = m.select_cases(m.plan_cases(inv), ids=tuple("SGL-" + fid for fid in self.AFFECTED))
        self.assertEqual([c.status for c in cases], ["RUNNABLE"] * 3)
        f = Fixture(self)
        f.upr.effects = {k: v.delta for k, v in inv.features.items() if v.delta}
        f.upr.tweak = {m.MISC_KEY: "0"}                            # miscTweaksAvailable() drops the bit
        results = f.suite(cases)
        for c in cases:
            self.assertEqual((results[c.id].target, results[c.id].status), ("NEEDS_REVIEW", "NEEDS_REVIEW"), c.id)
            self.assertIn("tweakForRom changed getCurrentMiscTweaks", results[c.id].detail)
        self.assertEqual(f.upr.count("cli"), 0)


UPR = m.ROOT / m.UPR_SOURCE


@unittest.skipUnless((UPR / m.CATALOG_SOURCE).is_file(), "UPR-FVX source not checked out")
class SourceBackingTests(unittest.TestCase):
    """The declarative cases and pins match the checked-out UPR-FVX source (read as text only)."""

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

    def test_pins_guards_and_full_inventory(self):
        for rel, pin in m.SOURCE_PINS.items():
            self.assertEqual(hashlib.sha256((UPR / rel).read_text().encode()).hexdigest(), pin, rel)
        for rel, text in m.GUARD_SOURCES.items():
            self.assertIn(text, (UPR / rel).read_text())
        joined = re.sub(r'"\s*\+\s*"', "", (UPR / "random/src/main/java/com/uprfvx/random/randomizers/"
                                             "EvolutionRandomizer.java").read_text())
        self.assertIn(m.EXPECTED_GUARDS["FVX-TRAIT-017"].removeprefix("RandomizationException: "), joined)
        inv = m.inventory(m.ROOT)
        self.assertEqual(inv.notes, [])
        ledger = [line.split("\t", 1)[0] for line in (m.ROOT / m.LEDGER).read_text().splitlines()[1:] if line]
        self.assertEqual((inv.catalog_ids, inv.ledger_ids, len(ledger)), (159, 132, 132))
        self.assertTrue(set(ledger) <= set(inv.features))
        self.assertEqual(len(inv.features), 159 + inv.ledger_only)
        for o in m.SINGLE_OPTIONS:
            self.assertEqual((inv.features[o.feature].state, inv.features[o.feature].delta), ("RUNNABLE", o.effect))
        self.assertTrue(set(m.PARENTS) | {p for ps in m.PARENTS.values() for p in ps} <= set(inv.features))

    def test_real_plan_is_filtered_and_complete(self):
        inv = m.inventory(m.ROOT)
        plan = m.plan_cases(inv)
        kinds = [c.kind for c in plan]
        self.assertEqual((kinds.count("SINGLE"), kinds.count("PAIR"), kinds.count("TRIPLE")), (159, 66, 12))
        ok = {k for k, f in inv.features.items() if f.state == "RUNNABLE"}
        for c in plan:
            if c.status == "RUNNABLE":
                self.assertTrue(set(c.overlays) <= ok, c.id)
            if c.status == "EXPECTED_REJECTION":
                self.assertIn(c.overlays[-1], m.EXPECTED_GUARDS)
        self.assertGreater(sum(c.status in m.RUNNABLE_CASES for c in plan), 170)
        for c in plan:
            if c.status in m.RUNNABLE_CASES:
                self.assertFalse(set(c.overlays) & set(m.PREREQUISITES), c.id)
            if c.kind in ("PAIR", "TRIPLE") and c.status in m.RUNNABLE_CASES:
                self.assertEqual([f for f, change in c.groups if change], c.id.split("-", 1)[1].split("+"), c.id)
        for fid in m.gm.RISK_SINGLES:
            self.assertEqual(inv.features[fid].state, "NEEDS_REVIEW", fid)
        for c in plan:
            if c.status in m.RUNNABLE_CASES:
                self.assertFalse(set(c.overlays) & set(m.SERIALIZATION_DEFECTS), c.id)

    def test_target_normalizations_are_in_the_pinned_source(self):
        settings = (UPR / m.SETTINGS_SOURCE).read_text()
        handlers = UPR / "romio/src/main/java/com/uprfvx/romio/romhandlers"
        gen3, gb, base = ((handlers / f"{n}.java").read_text()
                          for n in ("Gen3RomHandler", "AbstractGBRomHandler", "AbstractRomHandler"))
        self.assertIn("if (rh instanceof Gen1RomHandler || (rh instanceof Gen3RomHandler && !rh.isRomValid(null))) {\n"
                      "            this.currentRestrictions = null;\n            this.setLimitPokemon(false);", settings)
        self.assertIn("if (!rh.hasTimeBasedEncounters()) {\n            this.setUseTimeBasedEncounters(false);", settings)
        self.assertIn("public class Gen3RomHandler extends AbstractGBRomHandler {", gen3)
        self.assertNotRegex(gen3, r"boolean (isRomValid|hasTimeBasedEncounters)\(")
        self.assertIn("public abstract class AbstractGBRomHandler extends AbstractRomHandler {", gb)
        self.assertIn("return getRomEntry().getExpectedCRC32() == actualCRC32;", gb)
        self.assertNotIn("hasTimeBasedEncounters", gb)
        self.assertRegex(base, r"public boolean hasTimeBasedEncounters\(\) \{\n\s*// DEFAULT: no\n\s*return false;")
        inv = m.inventory(m.ROOT)
        lost = {k for k, f in inv.features.items() if f.reason.startswith("ineffective on the pilot target")}
        self.assertEqual(lost, {"FVX-GEN-001", "MODE-GEN-LIMIT-1-9", "MODE-GEN-LIMIT-1-9-NO-RELATIVES",
                                "FVX-SPECIAL-WILD-001"})
        self.assertEqual(inv.features["MODE-ALLOW-REGIONAL-FORMS"].state, "NEEDS_REVIEW")
        for c in m.plan_cases(inv):
            if "GEN_SAFE" in c.id or "SPECIAL_WILD" in c.id:
                self.assertNotIn(c.status, m.RUNNABLE_CASES, c.id)
            if c.status in m.RUNNABLE_CASES:
                self.assertFalse(set(c.overlays) & (lost | {"MODE-ALLOW-REGIONAL-FORMS"}), c.id)
                self.assertFalse({"isLimitPokemon", "isUseTimeBasedEncounters"} & dict(c.delta).keys(), c.id)

    def test_main_playthrough_reset_is_in_the_pinned_source(self):
        settings = (UPR / m.SETTINGS_SOURCE).read_text()
        catalog = m.overlay_catalog((UPR / m.CATALOG_SOURCE).read_text())
        gen3 = (UPR / "romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java").read_text()
        self.assertEqual(catalog["MODE-FOE-MAIN-PLAYTHROUGH"], "s -> s.setTrainersMod(Settings.TrainersMod.MAINPLAYTHROUGH)")
        self.assertIn("        if (rh.generationOfPokemon() != 5) {\n            "
                      + m.TARGET_NORMALIZED_VALUES[("getTrainersMod", "MAINPLAYTHROUGH")][0], settings)
        self.assertIn("    public int generationOfPokemon() {\n        return 3;\n    }", gen3)
        features = m.inventory(m.ROOT).features
        self.assertEqual(features["MODE-FOE-MAIN-PLAYTHROUGH"].state, "NEEDS_REVIEW")
        for fid in ("MODE-FOE-RANDOM", "MODE-FOE-EVEN-DISTRIBUTION", "MODE-FOE-TYPE-THEMED", "MODE-FOE-KEEP-THEMED",
                    "FVX-FOE-001"):
            self.assertEqual(features[fid].state, "RUNNABLE", fid)
        for c in m.plan_cases(m.inventory(m.ROOT)):
            if c.status in m.RUNNABLE_CASES:
                self.assertNotIn("MODE-FOE-MAIN-PLAYTHROUGH", c.overlays, c.id)

    def test_misc_tweak_availability_is_in_the_pinned_source(self):
        settings = (UPR / m.SETTINGS_SOURCE).read_text()
        handler = (UPR / m.HANDLER_SOURCE).read_text()
        misc = (UPR / m.MISC_SOURCE).read_text()
        catalog = m.overlay_catalog((UPR / m.CATALOG_SOURCE).read_text())
        self.assertIn("        // misc tweaks\n        int oldMiscTweaks = this.currentMiscTweaks;\n        " + m.MISC_FILTER,
                      settings)
        for fid, name, bit in (("FVX-MISC-002", "RUNNING_SHOES_INDOORS", 4), ("FVX-MISC-004", "NATIONAL_DEX_AT_START", 7),
                               ("FVX-MISC-010", "RUN_WITHOUT_RUNNING_SHOES", 18)):
            self.assertEqual(catalog[fid], f"s -> enableMiscTweak(s, MiscTweak.{name})")
            self.assertIn(f"public static final MiscTweak {name} = new MiscTweak(1 << {bit},", misc)
            self.assertIn(m.TARGET_MISC_UNAVAILABLE[name][0], handler)
        self.assertIn("private boolean usesCfruDpeBpreRunningLogic() {\n        return isCfruDpeGen9BpreProfile();", handler)
        inv = m.inventory(m.ROOT)
        lost = {k for k, f in inv.features.items() if f.reason.startswith("misc tweak not kept on the pilot target")}
        self.assertEqual(lost, {"FVX-MISC-002", "FVX-MISC-004", "FVX-MISC-010"})
        for fid in ("FVX-MISC-001", "FVX-MISC-003", "FVX-MISC-005", "FVX-MISC-006", "FVX-MISC-007", "FVX-MISC-008",
                    "FVX-MISC-009", "FVX-MISC-012"):
            self.assertEqual(inv.features[fid].state, "RUNNABLE", fid)
        cases = by_id(m.plan_cases(inv))
        self.assertEqual(cases["FAM-10_MISC_SAFE"].overlays, ("FVX-MISC-001", "FVX-MISC-003", "FVX-MISC-005",
                                                              "FVX-MISC-006", "FVX-MISC-007", "FVX-MISC-008",
                                                              "FVX-MISC-009"))
        self.assertEqual(cases["MAX-MAX_SAFE_WORLD"].status, "RUNNABLE")
        for c in cases.values():
            if c.status in m.RUNNABLE_CASES:
                self.assertFalse(set(c.overlays) & lost, c.id)

    def test_wild_007_round_trip_defect_is_in_the_pinned_source(self):
        catalog = m.overlay_catalog((UPR / m.CATALOG_SOURCE).read_text())
        settings = (UPR / m.SETTINGS_SOURCE).read_text()
        self.assertTrue(set(m.SERIALIZATION_DEFECTS) <= set(catalog))
        self.assertIn("s.setMinimumCatchRateLevel(45);", catalog["FVX-WILD-007"])
        self.assertIn("out.write(eliteFourUniquePokemonNumber | ((minimumCatchRateLevel - 1) << 3));", settings)
        self.assertIn("settings.setMinimumCatchRateLevel(((data[52] & 0x38) >> 3) + 1);", settings)
        written = (0 | ((45 - 1) << 3)) & 0xFF           # OutputStream.write keeps the low byte
        self.assertEqual(((written & 0x38) >> 3) + 1, 5)
        feature = m.inventory(m.ROOT).features["FVX-WILD-007"]
        self.assertEqual((feature.state, feature.delta["getMinimumCatchRateLevel"]), ("NEEDS_REVIEW", "45"))


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
