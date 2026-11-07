"""#743 tests: synthetic settings/ROM files and a mocked UPR process only.

Never launches UPR, Gradle or a real JAR and never opens a real ROM or .rnqs.
The Java adapter test compiles against synthetic Settings stand-ins.
"""
import contextlib
import io
import json
from pathlib import Path
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
        out = []
        for path in paths:
            out.append("BEGIN")
            out += [f"{k}={v}" for k, v in sorted(json.loads(Path(path).read_text()).items())]
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
}''',
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
                    "getUnknown": "UNSUPPORTED", "isRandomizeIntroMon": "false",
                    "useEstimatedLevelsForEvolutionImprovements": "true"})
                with self.assertRaisesRegex(m.MatrixError, "cannot be inspected"):
                    m.observe(d / "jar", d, [good, bad])


if __name__ == "__main__":
    unittest.main()
