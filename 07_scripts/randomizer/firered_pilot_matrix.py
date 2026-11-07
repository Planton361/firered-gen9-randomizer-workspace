#!/usr/bin/env python3
"""#743: USER-ONLY CFRU/DPE Gen 9 pilot settings matrix (starter/wild/trainer).

Composes UPR-FVX's existing settings-profile, cli and loaded-manifest commands
for the eleven pilot cases. The user supplies one neutral .rnqs saved once from
the GUI; its effective state is read through the public Settings API (a
temporary read-only Java adapter, because UPR has no settings-dump command)
before any overlay is applied. No settings bytes are written or patched here.

Modes: --plan (prints cases, reads nothing), --self-test (synthetic mocks only)
and --matrix (real local run; requires --confirm USER_LOCAL_RUN). Output stays
on the user's machine; the printed table contains categories only.
"""

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import upr_generation_matrix as gm
from upr_generation_matrix import MatrixError, command


ROOT = gm.ROOT
DEFAULT_JAR = ROOT / gm.LOCAL_JAR
CONFIRM_TOKEN = "USER_LOCAL_RUN"
# Public pilot candidate; the ROM's CFRU/DPE build cannot be verified from here.
PILOT = {
    "CFRU": ("02_external/CFRU-expansion", "196058edbc2b8b7d8c725b715b1f967ba60f5c83"),
    "DPE": ("02_external/Dynamic-Pokemon-Expansion-Gen-9", "d887185de1f6ae6a78e85c4311bbadde17041d00"),
    "UPR-FVX": ("02_external/upr-fvx", "1a9b59db3f49b6702b56cf76409de911cce9806e"),
}
# Outputs are ROMs: never inside the tracked tree, only in ignored local folders.
ALLOWED_OUTPUT_ROOTS = ("04_private_roms", "05_builds")

STARTER, WILD, TRAINER = "FVX-SST-002", "FVX-WILD-001", "FVX-FOE-001"
MOVESETS, REORDER = "FVX-MOVE-007", "FVX-MOVE-009"
# Exact Settings getter changes each settings-profile overlay must produce.
OVERLAY_EFFECT = {
    STARTER: {"getStartersMod": "COMPLETELY_RANDOM"},
    WILD: {"isRandomizeWildPokemon": "true"},
    TRAINER: {"getTrainersMod": "RANDOM"},
    MOVESETS: {"getMovesetsMod": "COMPLETELY_RANDOM"},
    REORDER: {"isReorderDamagingMoves": "true"},
}
LEARNSET_GUARD = ("RandomizationException: CFRU/DPE level-up learnset changes are unavailable: "
                  "select Unchanged, disable Reorder Damaging Moves, and do not use Metronome Only.")


@dataclass(frozen=True)
class Case:
    id: str
    title: str
    overlays: tuple
    seed: int
    expect: str = "PASS"          # PASS or EXPECTED_REJECTION
    replay_of: str = ""


CASES = (
    Case("M00", "Starter/Wild/Trainer OFF", (), 743000),
    Case("M01", "Starter", (STARTER,), 743001),
    Case("M02", "Wild", (WILD,), 743002),
    Case("M03", "Trainer", (TRAINER,), 743003),
    Case("M04", "Starter + Wild", (STARTER, WILD), 743004),
    Case("M05", "Starter + Trainer", (STARTER, TRAINER), 743005),
    Case("M06", "Wild + Trainer", (WILD, TRAINER), 743006),
    Case("M07", "Starter + Wild + Trainer", (STARTER, WILD, TRAINER), 743007),
    Case("M08", "Movesets Randomized", (MOVESETS,), 743008, "EXPECTED_REJECTION"),
    Case("M09", "Reorder Damaging Moves", (REORDER,), 743009, "EXPECTED_REJECTION"),
    Case("M10", "Replay of M07", (STARTER, WILD, TRAINER), 743007, replay_of="M07"),
)

# Neutral baseline: every other randomizer/updater/tweak owner off. Sub-options
# without an owner are free but must stay identical in every generated case.
UNCHANGED_MODS = (
    "getAbilitiesMod", "getAllyPokemonMod", "getAuraMod", "getBaseStatisticsMod", "getEvolutionsMod",
    "getFieldItemsMod", "getInGameTradesMod", "getMoveTutorMovesMod", "getMoveTutorsCompatibilityMod",
    "getMovesetsMod", "getPickupItemsMod", "getPokemonPalettesMod", "getShopItemsMod",
    "getSpeciesTypesMod", "getStartersMod", "getStaticPokemonMod", "getTmsHmsCompatibilityMod",
    "getTmsMod", "getTotemPokemonMod", "getTrainersMod", "getTypeEffectivenessMod",
)
FALSE_FLAGS = (
    "isAllowGigantamaxForms", "isAllowMegaForms", "isBetterBossTrainerMovesets",
    "isBetterImportantTrainerMovesets", "isBetterRegularTrainerMovesets", "isChangeImpossibleEvolutions",
    "isEvolutionMovesForAll", "isFullHMCompat", "isIncludeDynamaxGmaxItems", "isIncludeMegaItems",
    "isIncludeZCrystalItems", "isLimitPokemon", "isMakeEvolutionsEasier", "isPokemonPalettesFollowEvolutions",
    "isPokemonPalettesFollowTypes", "isPokemonPalettesShinyFromNormal", "isRaceMode",
    "isRandomizeHeldItemsForBossTrainerPokemon", "isRandomizeHeldItemsForImportantTrainerPokemon",
    "isRandomizeHeldItemsForRegularTrainerPokemon", "isRandomizeInGameTradesIVs",
    "isRandomizeInGameTradesItems", "isRandomizeInGameTradesNicknames", "isRandomizeInGameTradesOTs",
    "isRandomizeIntroMon", "isRandomizeMoveAccuracies", "isRandomizeMoveCategory", "isRandomizeMoveNames",
    "isRandomizeMovePPs", "isRandomizeMovePowers", "isRandomizeMoveTypes", "isRandomizeStartersHeldItems",
    "isRandomizeTotemHeldItems", "isRandomizeTrainerClassNames", "isRandomizeTrainerClassSprites",
    "isRandomizeTrainerNames", "isRandomizeWildPokemon", "isRandomizeWildPokemonHeldItems",
    "isRemoveTimeBasedEvolutions", "isReorderDamagingMoves", "isRivalCarriesStarterThroughout",
    "isShinyChance", "isStandardizeEXPCurves", "isStaticLevelModified", "isTotemLevelsModified",
    "isTrainersEvolveTheirPokemon", "isTrainersLevelModified", "isUpdateBaseStats", "isUpdateMoves",
    "isUpdateMovesLegacy", "isUpdateTypeEffectiveness", "isUpdatedFromOldVersion", "isUseMinimumCatchRate",
    "isWildLevelsModified",
)
ZERO_VALUES = (
    "getAdditionalBossTrainerPokemon", "getAdditionalImportantTrainerPokemon",
    "getAdditionalRegularTrainerPokemon", "getCurrentMiscTweaks", "getEliteFourUniquePokemonNumber",
)
NEUTRAL = {**{k: "UNCHANGED" for k in UNCHANGED_MODS}, **{k: "false" for k in FALSE_FLAGS},
           **{k: "0" for k in ZERO_VALUES}, "getBattleStyle": "UNCHANGED"}

# Read-only: every public Settings getter of a checkable type, in name order.
# Unknown types print UNSUPPORTED so the runner fails closed instead of guessing.
OBSERVE_JAVA = r'''import com.uprfvx.random.Settings;
import com.uprfvx.romio.gamedata.BattleStyle;
import com.uprfvx.romio.gamedata.GenRestrictions;
import java.io.FileInputStream;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.*;
class PilotSettingsObserve {
  static final Set<String> SKIP = Set.of("getRomName", "getCustomNames", "getCustomStarters");
  public static void main(String[] args) {
    try {
      List<Method> methods = new ArrayList<>(Arrays.asList(Settings.class.getMethods()));
      methods.sort(Comparator.comparing(Method::getName));
      for (String path : args) {
        Settings s;
        try (FileInputStream in = new FileInputStream(path)) { s = Settings.readFromFileFormat(in); }
        System.out.println("BEGIN");
        for (Method m : methods) {
          String n = m.getName();
          if (m.getParameterCount() != 0 || m.getDeclaringClass() != Settings.class
              || Modifier.isStatic(m.getModifiers()) || SKIP.contains(n)
              || !(n.startsWith("is") || n.startsWith("get") || n.startsWith("use"))) continue;
          Object v = m.invoke(s);
          String text;
          if (v == null) text = "null";
          else if (v instanceof Boolean || v instanceof Integer) text = v.toString();
          else if (v instanceof Enum<?> e) text = e.name();
          else if (v instanceof GenRestrictions g) text = Integer.toString(g.toInt());
          else if (v instanceof BattleStyle b) text = b.getModification().name();
          else text = "UNSUPPORTED";
          System.out.println(n + "=" + text);
        }
        System.out.println("END");
      }
    } catch (Exception ignored) {
      System.exit(3);  // Never expose a private path or exception text.
    }
  }
}
'''
VALUE = re.compile(r"true|false|null|-?[0-9]{1,10}|[A-Z][A-Z0-9_]{0,63}")


def parse_observations(text, count):
    blocks, current = [], None
    for line in text.splitlines():
        if line == "BEGIN" and current is None:
            current = {}
        elif line == "END" and current is not None:
            blocks.append(current)
            current = None
        else:
            key, sep, value = line.partition("=")
            if (current is None or not sep or not re.fullmatch(r"(is|get|use)[A-Za-z0-9]+", key)
                    or key in current or not VALUE.fullmatch(value)):
                raise MatrixError("Settings observation schema mismatch; details discarded.")
            current[key] = value
    if current is not None or len(blocks) != count:
        raise MatrixError("Settings observation incomplete; STOP.")
    return blocks


def observe(jar, temp, paths):
    adapter = temp / "PilotSettingsObserve.java"
    adapter.write_text(OBSERVE_JAVA)
    result = command(["java", "--class-path", str(jar), str(adapter), *map(str, paths)], temp)
    if result.returncode:
        raise MatrixError("Effective settings cannot be inspected through the Settings API; STOP.")
    return parse_observations(result.stdout, len(paths))


def check_baseline(state):
    """The baseline must be inspectable and neutral before any overlay is applied."""
    if any(value == "UNSUPPORTED" for value in state.values()):
        raise MatrixError("Baseline contains settings this runner cannot inspect; STOP.")
    missing = [key for key in NEUTRAL if key not in state]
    if missing:
        raise MatrixError(f"Baseline inspection lacks {len(missing)} required settings; STOP.")
    drift = sorted(key for key, value in NEUTRAL.items() if state[key] != value)
    if drift:
        raise MatrixError("Baseline is not neutral: " + ", ".join(drift) + "; save a neutral .rnqs.")


def expected_state(baseline, case):
    state = dict(baseline)
    for overlay in case.overlays:
        state.update(OVERLAY_EFFECT[overlay])
    return state


def check_case_settings(baseline, case, state):
    if state != expected_state(baseline, case):
        raise MatrixError(case.id + ": settings-profile output differs from baseline + overlays; STOP.")


def plan_lines():
    lines = ["#743 pilot settings matrix (USER-ONLY; --plan reads no ROM, JAR or settings)", ""]
    lines.append(f"{'ID':<4} {'Case':<26} {'Overlays':<38} {'Seed':<7} Expected")
    for case in CASES:
        overlays = ",".join(case.overlays) or "-"
        expected = case.expect + (" (bytes == " + case.replay_of + ")" if case.replay_of else "")
        lines.append(f"{case.id:<4} {case.title:<26} {overlays:<38} {case.seed:<7} {expected}")
    lines += ["", "Prerequisites: java, an existing UPR-FVX JAR built from the pilot candidate (never built here),",
              "the source ROM, a neutral .rnqs saved once in the GUI, and a new --out folder outside the",
              "tracked tree (" + " or ".join(ALLOWED_OUTPUT_ROOTS) + "/ inside the Workspace).",
              "Pilot candidate: " + "; ".join(f"{k} {v[1][:12]}" for k, v in PILOT.items())]
    return lines


def revision_lines(root, jar, allow_drift):
    """UPR must be the candidate the JAR was built from; CFRU/DPE are informational."""
    lines = []
    for name, (relative, expected) in PILOT.items():
        actual = gm.git(root / relative, "rev-parse", "HEAD")
        dirty = gm.git(root / relative, "status", "--porcelain", "--untracked-files=no")
        state = ("MATCH" if actual == expected else "DIFFERS") + ("; local changes" if dirty else "")
        lines.append(f"{name}: {actual[:12]} {state}")
        if name == "UPR-FVX" and state != "MATCH" and not allow_drift:
            raise MatrixError("UPR-FVX checkout is not the pilot candidate; STOP (or --allow-revision-drift).")
    freshness = gm.jar_freshness(root, jar)
    lines.append("JAR: " + freshness)
    if freshness != "NOT_OLDER_THAN_LOCAL_SOURCE" and not allow_drift:
        raise MatrixError("JAR is older than the UPR-FVX source or unverifiable; rebuild it first.")
    return lines


def output_root(value, root):
    out = Path(os.path.abspath(value))
    if out.is_relative_to(root) and not any(out.is_relative_to(root / p) for p in ALLOWED_OUTPUT_ROOTS):
        raise MatrixError("--out inside the Workspace must be under " + " or ".join(ALLOWED_OUTPUT_ROOTS) + "/.")
    if not out.parent.is_dir():
        raise MatrixError("--out parent folder does not exist.")
    try:
        out.mkdir()   # Atomic reservation; an existing folder is never reused.
    except FileExistsError:
        raise MatrixError("--out already exists; nothing is overwritten. Choose a new folder.") from None
    return out


@dataclass
class Result:
    status: str = "NOT_RUN"
    generate: str = "NOT_RUN"
    reopen: str = "NOT_RUN"
    replay: str = "-"
    detail: str = ""


def save_log(directory, name, result):
    # Raw UPR text stays in the local case folder only; it is never printed.
    (directory / name).write_text(result.stdout + "\n--- stderr ---\n" + result.stderr)


def generate(case, rom, jar, settings, directory, digest):
    """One case in its own fresh folder; returns (Result, output path or None)."""
    res = Result()
    output = directory / "output.gba"
    run = command(["java", "-jar", str(jar), "cli", "-i", str(rom), "-o", str(output),
                   "-s", str(settings), "-z", str(case.seed)], directory)
    save_log(directory, "cli.log", run)
    text = run.stdout + run.stderr
    if gm.input_digest(rom) != digest:
        raise MatrixError("Source ROM changed during " + case.id + "; STOP.")
    produced = output.exists()
    if case.expect == "EXPECTED_REJECTION":
        res.generate = "REJECTED" if run.returncode else "PASS"
        untouched = not produced and [p.name for p in directory.iterdir()] == ["cli.log"]
        if run.returncode and LEARNSET_GUARD in text and untouched:
            res.status, res.detail = "EXPECTED_REJECTION", "learnset guard, no output"
        else:
            res.status = "FAIL"
            res.detail = ("output written" if not untouched else "accepted" if not run.returncode
                          else "different failure (see local cli.log)")
        return res, None
    if (run.returncode or "Randomized successfully!" not in text or gm.ERROR_MARKERS.search(text)
            or not produced or output.stat().st_size == 0):
        res.status, res.generate, res.detail = "FAIL", "FAIL", "generation failed (see local cli.log)"
        return res, None
    res.generate = "PASS"
    identity = directory / "MatrixReopen.java"
    identity.write_text(gm.REOPEN_IDENTITY)
    run = command(["java", "--class-path", str(jar), str(identity), str(output)], directory)
    identity.unlink()
    save_log(directory, "reopen.log", run)
    if run.returncode or "Supported CFRU/DPE output identity verified." not in run.stdout:
        res.status, res.reopen, res.detail = "FAIL", "FAIL", "output not reopened as CFRU/DPE"
        return res, None
    run = command(["java", "-jar", str(jar), "loaded-manifest", "-i", str(output),
                   "-o", str(directory / "loaded-manifest")], directory)
    save_log(directory, "loaded-manifest.log", run)
    text = run.stdout + run.stderr
    if run.returncode or "Wrote sanitized loaded manifests." not in text or gm.ERROR_MARKERS.search(text):
        res.status, res.reopen, res.detail = "FAIL", "FAIL", "loaded-manifest failed"
        return res, None
    res.status, res.reopen = "PASS", "PASS"
    return res, output


def run_matrix(rom, baseline, jar, out, temp):
    """All settings are generated and checked before the first ROM is touched."""
    settings_dir = out / "settings"
    settings_dir.mkdir()
    base_state, = observe(jar, temp, [baseline])
    check_baseline(base_state)
    paths = []
    for case in CASES:
        target = settings_dir / (case.id + ".rnqs")
        args = ["java", "-jar", str(jar), "settings-profile", "--base-settings", str(baseline),
                "--output-settings", str(target)]
        for overlay in case.overlays:
            args += ["--enable", overlay]
        if not case.overlays:
            # settings-profile rejects a call without overlays; 00_BASELINE is its no-op profile.
            args += ["--profile", "00_BASELINE"]
        run = command(args, temp)
        if run.returncode or "Settings profile written successfully." not in run.stdout or not target.is_file():
            raise MatrixError(case.id + ": settings-profile failed; STOP.")
        paths.append(target)
    for case, state in zip(CASES, observe(jar, temp, paths)):
        check_case_settings(base_state, case, state)

    results = {case.id: Result() for case in CASES}
    outputs = {}
    digest = gm.input_digest(rom)
    for case, settings in zip(CASES, paths):
        directory = out / case.id
        directory.mkdir()
        res, output = generate(case, rom, jar, settings, directory, digest)
        if case.replay_of and res.status == "PASS":
            same = case.replay_of in outputs and gm.same_bytes(outputs[case.replay_of], output)
            res.replay = "PASS" if same else "FAIL"
            if not same:
                res.status, res.detail = "FAIL", "output differs from " + case.replay_of
        results[case.id] = res
        if res.status == "FAIL":
            break   # Fail fast: later cases stay NOT_RUN.
        if output:
            outputs[case.id] = output
    return results


def report_lines(results):
    lines = [f"{'ID':<4} {'Case':<26} {'Generate':<9} {'Reopen':<8} {'Replay':<7} Result"]
    for case in CASES:
        r = results[case.id]
        detail = " (" + r.detail + ")" if r.detail else ""
        lines.append(f"{case.id:<4} {case.title:<26} {r.generate:<9} {r.reopen:<8} {r.replay:<7} {r.status}{detail}")
    counts = {k: sum(r.status == k for r in results.values())
              for k in ("PASS", "EXPECTED_REJECTION", "FAIL", "NOT_RUN")}
    overall = "PASS" if counts["FAIL"] == counts["NOT_RUN"] == 0 else "FAIL"
    lines += ["", "Summary: " + ", ".join(f"{k}={v}" for k, v in counts.items()) + "; MATRIX=" + overall,
              "Scope: generation/reopen/replay only; no boot, gameplay or learnset-preservation claim."]
    return lines, overall


def self_test():
    import unittest
    tests = Path(__file__).resolve().parent / "tests"
    suite = unittest.defaultTestLoader.discover(str(tests), pattern="test_firered_pilot_matrix.py",
                                                top_level_dir=str(tests))
    return 0 if unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful() else 1


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        # Never echo supplied values; they may be private paths.
        self.exit(2, "Invalid arguments; see --help.\n")


def main(argv=None):
    parser = SafeParser(description="#743 USER-ONLY pilot settings matrix.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--plan", action="store_true", help="list cases; reads nothing")
    action.add_argument("--self-test", action="store_true", help="synthetic mock tests only")
    action.add_argument("--matrix", action="store_true", help="real local run (needs --confirm)")
    parser.add_argument("--confirm", help="must be " + CONFIRM_TOKEN + " for --matrix")
    parser.add_argument("--rom", help="source CFRU/DPE ROM")
    parser.add_argument("--baseline", help="neutral .rnqs saved once from the UPR GUI")
    parser.add_argument("--out", help="new output folder (must not exist)")
    parser.add_argument("--jar", help="existing UPR-FVX JAR (default: local build output)")
    parser.add_argument("--allow-revision-drift", action="store_true",
                        help="run although UPR-FVX/JAR are not the pilot candidate (development only)")
    args = parser.parse_args(argv)
    if args.plan:
        print("\n".join(plan_lines()))
        return 0
    if args.self_test:
        return self_test()
    try:
        if args.confirm != CONFIRM_TOKEN:
            raise MatrixError("--matrix runs real ROM generation; pass --confirm " + CONFIRM_TOKEN + ".")
        if not (args.rom and args.baseline and args.out):
            raise MatrixError("--matrix requires --rom, --baseline and --out.")
        rom, baseline = Path(args.rom).resolve(), Path(args.baseline).resolve()
        jar = Path(args.jar).resolve() if args.jar else DEFAULT_JAR
        if not rom.is_file() or not baseline.is_file() or not jar.is_file():
            raise MatrixError("ROM, baseline or JAR not found; the JAR is never built here.")
        header = ["#743 pilot settings matrix" + (" (REVISION DRIFT ALLOWED)" if args.allow_revision_drift else "")]
        header += revision_lines(ROOT, jar, args.allow_revision_drift)
        out = output_root(args.out, ROOT)
        print("\n".join(header), flush=True)
        with tempfile.TemporaryDirectory(prefix="pilot-matrix-") as temp:
            results = run_matrix(rom, baseline, jar, out, Path(temp))
        lines, overall = report_lines(results)
        print("\n".join(lines))
        return 0 if overall == "PASS" else 1
    except MatrixError as error:
        print("STOP: " + str(error), file=sys.stderr)
        return 2
    except (OSError, subprocess.SubprocessError):
        print("STOP: local file or subprocess operation failed; details discarded.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
