#!/usr/bin/env python3
"""ROM-free runner regression matrix; bytes are trivial NON-ROM fixtures."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
RUNNER = Path(__file__).resolve().parents[1] / 'run_r1_private_build.py'
spec = importlib.util.spec_from_file_location('r1_runner', RUNNER)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
FIXTURE = b'NON-ROM synthetic fixture for orchestration only\n'


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='r1-synthetic-tests-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / 'workspace'
        self.workspace.mkdir()
        self.base = self.root / 'PRIVATE_INPUT_MARKER.gba'
        self.base.write_bytes(FIXTURE)
        self.output = self.root / 'PRIVATE_OUTPUT_MARKER.gba'
        self.calls = []
        self.areas = []
        self.mode = {}
        self.registered = self.workspace / 'registered-source.txt'
        self.registered.write_text('unchanged registered source')

    def export(self, component, pin, tree):
        self.areas.append(tree.parent)
        tree.mkdir()
        (tree / 'scripts').mkdir()
        if self.mode.get('export-stale') == tree.name:
            (tree / 'test.gba').write_bytes(FIXTURE)

    def child(self, tree, script, **kwargs):
        label = tree.name + ' ' + script
        self.calls.append(label)
        action = self.mode.get(label)
        if action == 'fail':
            raise r.BuildFailure('child process returned non-zero')
        if action == 'exception':
            raise OSError(str(self.base))
        if action == 'interrupt':
            raise KeyboardInterrupt()
        if script.endswith('build.py') and action == 'stale':
            (tree / 'test.gba').write_bytes(FIXTURE)
        if script.endswith('make.py') and action != 'missing':
            self.assertEqual((tree / 'BPRE0.gba').read_bytes(), FIXTURE)
            (tree / 'test.gba').write_bytes(FIXTURE)

    def run_pipeline(self, profile=None, tools=None):
        stream = io.StringIO()
        with patch.object(r, 'validate_profile', side_effect=profile), \
             patch.object(r, 'validate_tools', side_effect=tools), \
             patch.object(r, 'export_source', side_effect=self.export), \
             patch.object(r, 'run_child', side_effect=self.child), \
             contextlib.redirect_stdout(stream):
            result = r.execute(self.workspace, self.base, self.output)
        text = stream.getvalue()
        for value in (str(self.base), str(self.output), 'PRIVATE_INPUT_MARKER',
                      'PRIVATE_OUTPUT_MARKER'):
            self.assertNotIn(value, text)
        for area in self.areas:
            self.assertFalse(area.exists(), 'temporary source/private data persisted')
        self.assertEqual(self.registered.read_text(), 'unchanged registered source')
        self.assertEqual(self.base.read_bytes(), FIXTURE)
        self.assertFalse(list(self.root.glob('.r1-publish-*')))
        return result, text

    def test_success_order_single_publication_cleanup(self):
        with patch.object(r.os, 'link', wraps=os.link) as publish, \
             patch.object(r.shutil, 'copyfileobj', wraps=r.shutil.copyfileobj) as final_copy:
            result, text = self.run_pipeline()
        self.assertEqual(result, 0)
        self.assertIn('Final output: READY', text)
        publish.assert_called_once()
        final_copy.assert_called_once()
        self.assertEqual(self.output.read_bytes(), FIXTURE)
        self.assertEqual(self.calls, ['DPE scripts/build.py', 'DPE scripts/make.py',
                                     'CFRU scripts/build.py', 'CFRU scripts/make.py'])

    def test_all_child_failures_stop_and_clean(self):
        order = ['DPE scripts/build.py', 'DPE scripts/make.py',
                 'CFRU scripts/build.py', 'CFRU scripts/make.py']
        for index, label in enumerate(order):
            for action in ('fail', 'exception', 'interrupt'):
                with self.subTest(label=label, action=action):
                    self.calls.clear()
                    self.mode = {label: action}
                    result, text = self.run_pipeline()
                    self.assertEqual(result, 1)
                    self.assertEqual(self.calls, order[:index + 1])
                    self.assertFalse(self.output.exists())
                    self.assertIn('R1_PRIVATE_BUILD_FAILED', text)

    def test_exit_zero_missing_output_fails(self):
        for component, length in (('DPE', 2), ('CFRU', 4)):
            with self.subTest(component=component):
                self.calls.clear()
                self.mode = {component + ' scripts/make.py': 'missing'}
                self.assertEqual(self.run_pipeline()[0], 1)
                self.assertEqual(len(self.calls), length)
                self.assertFalse(self.output.exists())

    def test_build_created_stale_output_rejected_before_make(self):
        for component, length in (('DPE', 1), ('CFRU', 3)):
            with self.subTest(component=component):
                self.calls.clear()
                self.mode = {component + ' scripts/build.py': 'stale'}
                self.assertEqual(self.run_pipeline()[0], 1)
                self.assertEqual(len(self.calls), length)
                self.assertFalse(self.output.exists())

    def test_export_preexisting_output_rejected(self):
        for component in ('DPE', 'CFRU'):
            self.mode = {'export-stale': component}
            self.assertEqual(self.run_pipeline()[0], 1)
            self.assertEqual(self.calls, [])

    def test_preflights_before_private_use(self):
        for check in ('profile', 'tools'):
            with self.subTest(check=check), patch.object(r.shutil, 'copyfile') as copy:
                self.assertEqual(self.run_pipeline(**{check: r.BuildFailure('rejected')})[0], 1)
                copy.assert_not_called()
                self.assertEqual(self.calls, [])

    def test_copy_failures_stop_and_cleanup(self):
        original = r.shutil.copyfile
        for failed_copy, expected_calls in ((1, 1), (2, 2)):
            counter = [0]
            def copying(source, target):
                counter[0] += 1
                if counter[0] == failed_copy:
                    raise OSError(str(self.base))
                return original(source, target)
            with self.subTest(copy=failed_copy), patch.object(r.shutil, 'copyfile', side_effect=copying):
                self.calls.clear()
                self.assertEqual(self.run_pipeline()[0], 1)
                self.assertEqual(len(self.calls), expected_calls)
                self.assertFalse(self.output.exists())

    def test_export_failure_cleanup(self):
        original = self.export
        def broken_export(component, pin, tree):
            original(component, pin, tree)
            raise OSError(str(self.base))
        with patch.object(self, 'export', side_effect=broken_export):
            self.assertEqual(self.run_pipeline()[0], 1)
        self.assertEqual(self.calls, [])
        self.assertFalse(self.output.exists())

    def test_private_input_not_statted_before_preflights(self):
        class UnreadableInput:
            touched = False
            def is_symlink(self):
                self.touched = True
                return False
            def is_file(self):
                self.touched = True
                return False
        for stage in ('validate_profile', 'validate_tools'):
            private_input = UnreadableInput()
            with patch.object(r, 'validate_profile'), patch.object(r, 'validate_tools'), \
                 patch.object(r, stage, side_effect=r.BuildFailure('preflight failed')), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(r.execute(self.workspace, private_input, self.output), 1)
            self.assertFalse(private_input.touched)

    def test_existing_output_preserved(self):
        self.output.write_bytes(b'existing NON-ROM')
        self.assertEqual(self.run_pipeline()[0], 1)
        self.assertEqual(self.output.read_bytes(), b'existing NON-ROM')
        self.assertEqual(self.calls, [])

    def test_output_copy_failure_cleanup(self):
        with patch.object(r.shutil, 'copyfileobj', side_effect=OSError(str(self.output))):
            self.assertEqual(self.run_pipeline()[0], 1)
        self.assertFalse(self.output.exists())

    def test_publication_race_no_overwrite(self):
        def race(source, target):
            target.write_bytes(b'concurrent NON-ROM')
            raise FileExistsError(str(target))
        with patch.object(r.os, 'link', side_effect=race):
            self.assertEqual(self.run_pipeline()[0], 1)
        self.assertEqual(self.output.read_bytes(), b'concurrent NON-ROM')

    def test_cleanup_failure_prevents_publication(self):
        cleanup = r.tempfile.TemporaryDirectory.cleanup
        def clean_then_fail(obj):
            cleanup(obj)
            raise OSError(str(self.base))
        with patch.object(r.tempfile.TemporaryDirectory, 'cleanup', clean_then_fail):
            self.assertEqual(self.run_pipeline()[0], 1)
        self.assertFalse(self.output.exists())

    def test_interrupt_during_cleanup_retries_and_fails_safely(self):
        cleanup = r.tempfile.TemporaryDirectory.cleanup
        calls = [0]
        def interrupted(obj):
            calls[0] += 1
            if calls[0] == 1:
                raise KeyboardInterrupt()
            return cleanup(obj)
        with patch.object(r.tempfile.TemporaryDirectory, 'cleanup', interrupted):
            result, text = self.run_pipeline()
        self.assertEqual(result, 1)
        self.assertGreaterEqual(calls[0], 2)
        self.assertFalse(self.output.exists())
        self.assertIn('Temporary build area: CLEANED', text)

    def test_missing_or_directory_input(self):
        saved = self.base
        for candidate in (self.root / 'missing-private.gba', self.root):
            self.base = candidate
            with patch.object(r, 'validate_profile'), patch.object(r, 'validate_tools'), \
                 patch.object(r, 'export_source', side_effect=self.export), \
                 patch.object(r, 'run_child', side_effect=self.child), \
                 contextlib.redirect_stdout(io.StringIO()) as stream:
                self.assertEqual(r.execute(self.workspace, candidate, self.output), 1)
            self.assertNotIn(str(candidate), stream.getvalue())
            self.assertFalse(self.output.exists())
            self.assertTrue(all(not area.exists() for area in self.areas))
        self.base = saved


class PreflightTests(unittest.TestCase):
    def test_each_and_multiple_missing_tools(self):
        for missing in [(tool,) for tool in r.TOOLS] + [r.TOOLS]:
            with self.subTest(missing=missing), \
                 patch.object(r.shutil, 'which', side_effect=lambda tool: None if tool in missing else '/hidden/tool'):
                with self.assertRaises(r.BuildFailure) as error:
                    r.validate_tools()
                self.assertEqual(str(error.exception), 'missing tools: ' + ', '.join(missing))
                self.assertNotIn('/hidden', str(error.exception))
        with patch.object(r.shutil, 'which', return_value='/hidden/tool'):
            r.validate_tools()

    def test_profile_exact_and_pin_rejections(self):
        workspace = Path('/synthetic-workspace')
        def metadata(root, *args):
            if args[0] == 'merge-base':
                return ''
            if args[0] == 'diff':
                return '07_scripts/build/run_r1_private_build.py'
            for relative, pin in r.PINS.values():
                if args == ('rev-parse', 'HEAD:' + relative):
                    return pin
                if args == ('ls-files', '--stage', '--', relative):
                    return '160000 ' + pin + ' 0\t' + relative
                if root == workspace / relative:
                    if args == ('rev-parse', '--show-toplevel'):
                        return str(root.resolve())
                    if args == ('rev-parse', 'HEAD'):
                        return pin
                    return ''
            self.fail((root, args))
        with patch.object(r, 'git', side_effect=metadata):
            r.validate_profile(workspace)
        for name in r.PINS:
            relative, pin = r.PINS[name]
            def mismatch(root, *args):
                if args == ('rev-parse', 'HEAD:' + relative):
                    return '0' * 40
                return metadata(root, *args)
            with self.subTest(name=name), patch.object(r, 'git', side_effect=mismatch):
                with self.assertRaisesRegex(r.BuildFailure, name + ' pin mismatch'):
                    r.validate_profile(workspace)
        def unsupported(root, *args):
            return 'src/gameplay.c' if args[0] == 'diff' else metadata(root, *args)
        with patch.object(r, 'git', side_effect=unsupported):
            with self.assertRaisesRegex(r.BuildFailure, 'unsupported Workspace'):
                r.validate_profile(workspace)
        with patch.object(r, 'git', side_effect=r.BuildFailure('unsupported ancestry')):
            with self.assertRaises(r.BuildFailure):
                r.validate_profile(workspace)

    def test_prohibited_source_destinations_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / 'workspace'
            workspace.mkdir()
            source = workspace / 'tracked.py'
            source.write_text('source')
            for output in (source, workspace / 'new.gba'):
                with self.assertRaises(r.BuildFailure):
                    r.validate_output(workspace, output)
            alias = root / 'alias'
            alias.symlink_to(workspace, target_is_directory=True)
            with self.assertRaises(r.BuildFailure):
                r.validate_output(workspace, alias / 'new.gba')
            with self.assertRaises(r.BuildFailure):
                r.validate_output(workspace, root / 'missing-parent' / 'output.gba')
            other = root / 'other-checkout'
            other.mkdir()
            subprocess.run(['git', 'init', '-q', str(other)], check=True)
            with self.assertRaises(r.BuildFailure):
                r.validate_output(workspace, other / 'output.gba')

    def test_cli_redaction(self):
        with contextlib.redirect_stderr(io.StringIO()) as stream:
            with self.assertRaises(SystemExit) as error:
                r.main(['--PRIVATE_PATH_MARKER'])
        self.assertEqual(error.exception.code, 2)
        self.assertNotIn('PRIVATE_PATH_MARKER', stream.getvalue())


class RealChildTests(unittest.TestCase):
    def test_child_status_signal_and_redaction(self):
        with tempfile.TemporaryDirectory() as directory:
            tree = Path(directory)
            script = tree / 'child.py'
            for body, fails in [
                ("print('PRIVATE_CHILD_PATH_MARKER')", False),
                ("raise SystemExit(7)", True),
                ("import os, signal; os.kill(os.getpid(), signal.SIGTERM)", True),
            ]:
                script.write_text(body)
                with contextlib.redirect_stdout(io.StringIO()) as stream:
                    if fails:
                        with self.assertRaises(r.BuildFailure):
                            r.run_child(tree, 'child.py')
                    else:
                        r.run_child(tree, 'child.py')
                self.assertNotIn('PRIVATE_CHILD_PATH_MARKER', stream.getvalue())

    def test_child_redaction_at_os_capture_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            tree = Path(directory)
            (tree / 'child.py').write_text(
                "import sys\nprint('PRIVATE_CHILD_STDOUT_MARKER')\n"
                "print('PRIVATE_CHILD_STDERR_MARKER', file=sys.stderr)\n")
            code = ("import sys, importlib.util; sys.dont_write_bytecode=True; "
                    f"spec=importlib.util.spec_from_file_location('runner', {str(RUNNER)!r}); "
                    "r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r); "
                    f"r.run_child(r.Path({str(tree)!r}), 'child.py')")
            result = subprocess.run([sys.executable, '-c', code], capture_output=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, b'')
            self.assertEqual(result.stderr, b'')

    def test_dpe_nested_insert_failure_even_with_fresh_output(self):
        with tempfile.TemporaryDirectory() as directory:
            tree = Path(directory)
            (tree / 'scripts').mkdir()
            script = tree / 'scripts/make.py'
            for status in (0, 7):
                script.write_text("import os\nfrom pathlib import Path\n"
                                  "Path('test.gba').write_bytes(b'NON-ROM partial fixture')\n"
                                  f"os.system('python3 -c \"raise SystemExit({status})\"')\n")
                if status:
                    with self.assertRaises(r.BuildFailure):
                        r.run_child(tree, 'scripts/make.py', dpe_make=True)
                else:
                    r.run_child(tree, 'scripts/make.py', dpe_make=True)

    def test_git_export_uses_committed_tree_and_excludes_binaries(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / 'component'
            repo.mkdir()
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            (repo / 'source.py').write_text('committed source')
            (repo / 'deps').mkdir()
            # Clearly synthetic tool fixture, never a real binary.
            (repo / 'deps/tool.exe').write_text('NON-BINARY synthetic excluded fixture')
            for args in [('add', 'source.py', 'deps/tool.exe'),
                         ('-c', 'user.name=Synthetic', '-c', 'user.email=synthetic@example.invalid',
                          'commit', '-qm', 'synthetic source')]:
                subprocess.run(['git', '-C', str(repo), *args], check=True)
            pin = r.git(repo, 'rev-parse', 'HEAD')
            (repo / 'source.py').write_text('dirty source remains untouched')
            before = r.git(repo, 'status', '--porcelain')
            exported = root / 'exported'
            r.export_source(repo, pin, exported)
            self.assertEqual((exported / 'source.py').read_text(), 'committed source')
            self.assertFalse((exported / 'deps').exists())
            self.assertEqual(r.git(repo, 'status', '--porcelain'), before)
            self.assertEqual((repo / 'source.py').read_text(), 'dirty source remains untouched')

    def test_full_synthetic_export_build_insert_pipeline(self):
        with tempfile.TemporaryDirectory(prefix='r1-full-synthetic-') as directory:
            root = Path(directory)
            workspace = root / 'workspace'
            workspace.mkdir()
            pins = {}
            for name in ('DPE', 'CFRU'):
                repo = workspace / name
                (repo / 'scripts').mkdir(parents=True)
                subprocess.run(['git', 'init', '-q', str(repo)], check=True)
                (repo / 'scripts/build.py').write_text("print('PRIVATE_CHILD_PATH_MARKER')\n")
                (repo / 'scripts/make.py').write_text(
                    "from pathlib import Path\n"
                    "Path('test.gba').write_bytes(Path('BPRE0.gba').read_bytes())\n")
                subprocess.run(['git', '-C', str(repo), 'add', 'scripts'], check=True)
                subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Synthetic',
                                '-c', 'user.email=synthetic@example.invalid', 'commit',
                                '-qm', 'NON-ROM synthetic sources'], check=True)
                pins[name] = (name, r.git(repo, 'rev-parse', 'HEAD'))
            input_path = root / 'PRIVATE_INPUT_MARKER.gba'
            input_path.write_bytes(FIXTURE)
            output_path = root / 'PRIVATE_OUTPUT_MARKER.gba'
            calls, areas = [], []
            original_child, original_export = r.run_child, r.export_source
            def child(tree, script, **kwargs):
                calls.append((tree.name, script))
                return original_child(tree, script, **kwargs)
            def exporting(component, pin, tree):
                areas.append(tree.parent)
                return original_export(component, pin, tree)
            before = {name: r.git(workspace / name, 'status', '--porcelain') for name in pins}
            with patch.object(r, 'PINS', pins), patch.object(r, 'validate_profile'), \
                 patch.object(r, 'validate_tools'), patch.object(r, 'run_child', side_effect=child), \
                 patch.object(r, 'export_source', side_effect=exporting), \
                 contextlib.redirect_stdout(io.StringIO()) as stream:
                self.assertEqual(r.execute(workspace, input_path, output_path), 0)
            self.assertEqual(output_path.read_bytes(), FIXTURE)
            self.assertEqual(calls, [('DPE', 'scripts/build.py'), ('DPE', 'scripts/make.py'),
                                    ('CFRU', 'scripts/build.py'), ('CFRU', 'scripts/make.py')])
            self.assertTrue(all(not area.exists() for area in areas))
            self.assertFalse(list(root.glob('.r1-publish-*')))
            for marker in ('PRIVATE_INPUT_MARKER', 'PRIVATE_OUTPUT_MARKER', 'PRIVATE_CHILD_PATH_MARKER'):
                self.assertNotIn(marker, stream.getvalue())
            self.assertEqual(before, {name: r.git(workspace / name, 'status', '--porcelain') for name in pins})
            self.assertFalse(list(workspace.rglob('*.gba')))

    def test_interrupt_stops_child_process_group(self):
        class FakeChild:
            pid = 12345678
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def wait(self):
                if not getattr(self, 'interrupted', False):
                    self.interrupted = True
                    raise KeyboardInterrupt()
                return -9
        with patch.object(r.subprocess, 'Popen', return_value=FakeChild()), \
             patch.object(r.os, 'killpg') as kill:
            with self.assertRaises(KeyboardInterrupt):
                r.run_child(Path('/synthetic-tree'), 'scripts/make.py')
        kill.assert_called_once_with(12345678, r.signal.SIGKILL)

    def test_live_profile_validation_is_read_only(self):
        workspace = RUNNER.parents[2]
        before = {name: r.git(workspace / relative, 'status', '--porcelain')
                  for name, (relative, pin) in r.PINS.items()}
        r.validate_profile(workspace)
        after = {name: r.git(workspace / relative, 'status', '--porcelain')
                 for name, (relative, pin) in r.PINS.items()}
        self.assertEqual(before, after)
        self.assertTrue(all(value == '' for value in after.values()))


if __name__ == '__main__':
    unittest.main(verbosity=2)
