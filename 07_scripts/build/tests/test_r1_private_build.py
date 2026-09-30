#!/usr/bin/env python3
"""ROM-free runner regression matrix; bytes are trivial NON-ROM fixtures."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import re
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


def init_storage_checkout(root, *, ignore_input=True, ignore_output=True):
    root.mkdir(parents=True)
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    ignored = []
    if ignore_input:
        ignored.append('04_private_roms/')
    if ignore_output:
        ignored.append('05_builds/')
    (root / '.gitignore').write_text('\n'.join(ignored) + ('\n' if ignored else ''))
    source = root / '02_external' / 'CFRU-expansion' / 'tracked-source.txt'
    source.parent.mkdir(parents=True)
    source.write_text('tracked synthetic source')
    subprocess.run(['git', '-C', str(root), 'add', '.gitignore', '02_external'], check=True)
    subprocess.run(['git', '-C', str(root), '-c', 'user.name=Synthetic',
                    '-c', 'user.email=synthetic@example.invalid', 'commit', '-qm',
                    'NON-ROM synthetic storage checkout'], check=True)
    (root / '04_private_roms').mkdir()
    (root / '05_builds').mkdir()
    (root / '07_scripts').mkdir()
    (root / 'docs').mkdir()
    (root / 'arbitrary' / 'subdir').mkdir(parents=True)
    return root


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='r1-synthetic-tests-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / 'workspace'
        init_storage_checkout(self.workspace)
        self.base = self.workspace / '04_private_roms' / 'PRIVATE INPUT MARKER.gba'
        self.base.write_bytes(FIXTURE)
        self.output = self.workspace / '05_builds' / 'PRIVATE OUTPUT MARKER.gba'
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


class CanonicalPathPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='r1-path-policy-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.runner_workspace = init_storage_checkout(self.root / 'runner-workspace')
        self.storage = init_storage_checkout(self.root / 'storage-workspace')
        self.input = self.storage / '04_private_roms' / 'base with spaces.gba'
        self.input.write_bytes(FIXTURE)
        self.output = self.storage / '05_builds' / 'test.gba'

    def test_allowed_canonical_private_input_with_spaces(self):
        self.assertEqual(r.validate_input(self.runner_workspace, self.input),
                         self.input.resolve())

    def test_allowed_canonical_output_and_directory_shorthand(self):
        self.assertEqual(r.validate_output(self.runner_workspace, self.output),
                         self.output.resolve())
        self.assertEqual(r.validate_output(self.runner_workspace,
                                           self.storage / '05_builds'), self.output.resolve())

        outside_alias = self.root / 'outside-build-alias'
        outside_alias.symlink_to(self.storage / '05_builds', target_is_directory=True)
        self.assertEqual(r.validate_output(self.runner_workspace, outside_alias / 'alias.gba'),
                         (self.storage / '05_builds' / 'alias.gba').resolve())
        self.assertEqual(r.validate_output(self.runner_workspace, outside_alias),
                         self.output.resolve())
        with self.assertRaises(r.BuildFailure):
            r.validate_output(self.runner_workspace, self.storage / 'arbitrary')

    def test_existing_final_output_fails_without_overwrite(self):
        original = b'existing NON-ROM output bytes'
        self.output.write_bytes(original)
        with self.assertRaises(r.BuildFailure):
            r.validate_output(self.runner_workspace, self.output)

        calls = []
        with patch.object(r, 'validate_profile'), patch.object(r, 'validate_tools'), \
             patch.object(r, 'export_source', side_effect=lambda *args: calls.append('export')), \
             patch.object(r, 'run_child', side_effect=lambda *args, **kwargs: calls.append('child')), \
             contextlib.redirect_stdout(io.StringIO()):
            result = r.execute(self.runner_workspace, self.input, self.output)
        self.assertEqual(result, 1)
        self.assertEqual(self.output.read_bytes(), original)
        self.assertEqual(calls, [])

    def test_dirty_old_storage_checkout_zones_are_accepted_and_untouched(self):
        source = self.storage / '02_external' / 'CFRU-expansion' / 'tracked-source.txt'
        source.write_text('unrelated dirty tracked source')
        before_status = r.git(self.storage, 'status', '--porcelain')
        before_source = source.read_bytes()

        self.assertEqual(r.validate_input(self.runner_workspace, self.input), self.input.resolve())
        self.assertEqual(r.validate_output(self.runner_workspace, self.output), self.output.resolve())
        self.assertEqual(r.git(self.storage, 'status', '--porcelain'), before_status)
        self.assertEqual(source.read_bytes(), before_source)

    def test_ignore_contract_requires_the_zone_itself_to_be_ignored(self):
        no_private_ignore = init_storage_checkout(self.root / 'no-private-ignore',
                                                  ignore_input=False)
        private_input = no_private_ignore / '04_private_roms' / 'base.gba'
        private_input.write_bytes(FIXTURE)
        with self.assertRaises(r.BuildFailure):
            r.validate_input(self.runner_workspace, private_input)

        no_build_ignore = init_storage_checkout(self.root / 'no-build-ignore',
                                                 ignore_output=False)
        with self.assertRaises(r.BuildFailure):
            r.validate_output(self.runner_workspace,
                              no_build_ignore / '05_builds' / 'test.gba')

    def test_source_and_noncanonical_destinations_are_rejected(self):
        candidates = (
            self.storage / '02_external' / 'CFRU-expansion' / 'test.gba',
            self.storage / '07_scripts' / 'foo.gba',
            self.storage / 'docs' / 'foo.gba',
            self.storage / 'arbitrary' / 'subdir' / 'foo.gba',
        )
        for candidate in candidates:
            with self.subTest(candidate=candidate.relative_to(self.storage)):
                with self.assertRaises(r.BuildFailure):
                    r.validate_output(self.runner_workspace, candidate)

    def test_symlinks_that_do_not_resolve_to_the_canonical_zone_fail_closed(self):
        source = self.storage / '02_external' / 'CFRU-expansion' / 'tracked-source.txt'
        input_link = self.storage / '04_private_roms' / 'linked.gba'
        input_link.symlink_to(source)
        with self.assertRaises(r.BuildFailure):
            r.validate_input(self.runner_workspace, input_link)

        private_alias = self.storage / '04_private_roms' / 'source-alias'
        private_alias.symlink_to(source.parent, target_is_directory=True)
        with self.assertRaises(r.BuildFailure):
            r.validate_input(self.runner_workspace, private_alias / source.name)

        escaped_parent = self.storage / '05_builds' / 'source-alias'
        escaped_parent.symlink_to(source.parent, target_is_directory=True)
        with self.assertRaises(r.BuildFailure):
            r.validate_output(self.runner_workspace, escaped_parent / 'test.gba')

        linked_output = self.storage / '05_builds' / 'existing-link.gba'
        linked_output.symlink_to(source)
        with self.assertRaises(r.BuildFailure):
            r.validate_output(self.runner_workspace, linked_output)

        linked_zone_root = init_storage_checkout(self.root / 'linked-zone-root')
        (linked_zone_root / '05_builds').rmdir()
        (linked_zone_root / '05_builds').symlink_to(
            linked_zone_root / '02_external' / 'CFRU-expansion', target_is_directory=True)
        with self.assertRaises(r.BuildFailure):
            r.validate_output(self.runner_workspace,
                              linked_zone_root / '05_builds' / 'test.gba')

        private_zone_root = init_storage_checkout(self.root / 'linked-private-root')
        (private_zone_root / '04_private_roms').rmdir()
        (private_zone_root / '04_private_roms').symlink_to(
            private_zone_root / '02_external' / 'CFRU-expansion', target_is_directory=True)
        with self.assertRaises(r.BuildFailure):
            r.validate_input(self.runner_workspace,
                             private_zone_root / '04_private_roms' / source.name)


class SourceExportTests(unittest.TestCase):
    @staticmethod
    def excluded(name):
        path = Path(name)
        return (path.parts[0] in ('deps', 'build', '.git')
                or path.suffix.lower() in
                ('.gba', '.gb', '.gbc', '.sav', '.state', '.exe', '.dll', '.jar', '.zip', '.7z', '.srm')
                or re.fullmatch(r'\.ss[0-9].*', path.suffix, re.IGNORECASE) is not None
                or any(part.startswith('.env') for part in path.parts))

    def assert_export(self, component, pin, exported):
        with patch.object(r.subprocess, 'Popen', wraps=subprocess.Popen) as invocation:
            r.export_source(component, pin, exported)
        invocation.assert_called_once()
        command = invocation.call_args.args[0]
        self.assertEqual(command, ['git', '-C', str(component), 'archive', pin,
                                   '--', '.', *r.EXPORT_EXCLUDES])
        self.assertLessEqual(len(command), 32)
        self.assertLess(sum(len(os.fsencode(arg)) + 1 for arg in command), 2048)
        return command

    def test_thousands_of_committed_paths_keep_archive_argv_bounded(self):
        with tempfile.TemporaryDirectory(prefix='r1-large-synthetic-') as directory:
            root = Path(directory)
            repo = root / 'component'
            repo.mkdir()
            subprocess.run(['git', 'init', '-q', str(repo)], check=True)
            def commit():
                subprocess.run(['git', '-C', str(repo), 'add', '.'], check=True)
                subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Synthetic',
                                '-c', 'user.email=synthetic@example.invalid', 'commit',
                                '-qm', 'NON-ROM synthetic source export fixture'], check=True)
                return r.git(repo, 'rev-parse', 'HEAD')
            (repo / 'source.py').write_text('committed synthetic source')
            small_pin = commit()
            small_command = self.assert_export(repo, small_pin, root / 'small-export')
            sources = {'source.py'}
            for index in range(6000):
                name = f'src/group_{index // 100}/source_{index:04d}_{"x" * 64}.c'
                sources.add(name)
                target = repo / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('/* NON-ROM synthetic source fixture */')
            # All exclusions at root and nested depth, including mixed case.
            blocked = {'deps/not_a_binary.txt', 'build/not_a_build.txt',
                       '.env', '.env.local', 'nested/.env', 'nested/.environment',
                       'nested/.envdir/fixture.txt'}
            for suffix in ('.gba', '.gb', '.gbc', '.sav', '.state', '.exe', '.dll',
                           '.jar', '.zip', '.7z', '.srm', '.ss4', '.ss5'):
                blocked.update({f'fixture{suffix}', f'nested/deep/fixture{suffix.upper()}'})
            for name in blocked:
                target = repo / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('EXCLUDED NON-ROM NON-BINARY synthetic fixture only')
            # Nested directories with these names remain legitimate source.
            for name in ('src/deps/keep.c', 'src/build/keep.c', 'src/env_config.c'):
                sources.add(name)
                target = repo / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('/* legitimate synthetic source */')
            large_pin = commit()
            # Committed-tree guarantee despite dirty and untracked files.
            (repo / 'source.py').write_text('dirty source must remain untouched')
            (repo / 'untracked.c').write_text('untracked synthetic source')
            before = r.git(repo, 'status', '--porcelain')
            exported = root / 'large-export'
            large_command = self.assert_export(repo, large_pin, exported)
            self.assertEqual(small_command[:4] + small_command[5:],
                             large_command[:4] + large_command[5:])
            self.assertGreater(sum(len(name) + 1 for name in sources), 248276)
            files = {str(path.relative_to(exported)) for path in exported.rglob('*') if path.is_file()}
            self.assertEqual(files, sources)
            self.assertTrue(files.isdisjoint(blocked))
            self.assertEqual((exported / 'source.py').read_text(), 'committed synthetic source')
            self.assertEqual(r.git(repo, 'status', '--porcelain'), before)
            # Inspect the actual Git archive listing before extraction: excluded
            # fixtures must never have entered the stream, not merely be skipped.
            result = subprocess.run(large_command, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)
            with r.tarfile.open(fileobj=io.BytesIO(result.stdout)) as archive:
                archived_files = {member.name for member in archive if member.isfile()}
            self.assertEqual(archived_files, sources)
            self.assertNotIn(b'EXCLUDED NON-ROM NON-BINARY', result.stdout)
            print(f'Bounded export: {len(sources)} sources, {len(large_command)} argv entries; '
                  'small/large command shape identical; stream exclusions PASS')

    def smoke_exact_pin(self, name):
        workspace = RUNNER.parents[2]
        relative, pin = r.PINS[name]
        component = workspace / relative
        def identity():
            return (r.git(component, 'rev-parse', 'HEAD'),
                    r.git(component, 'status', '--porcelain', '--untracked-files=all'),
                    r.git(component, 'ls-files', '--stage', '-z'))
        before = identity()
        self.assertEqual(before[0], pin)
        self.assertEqual(before[1], '')
        names = set(filter(None, r.git(component, 'ls-tree', '-r', '--name-only', '-z', pin).split('\0')))
        expected = {name for name in names if not self.excluded(name)}
        with tempfile.TemporaryDirectory(prefix='r1-exact-source-smoke-') as directory:
            exported = Path(directory) / name
            command = self.assert_export(component, pin, exported)
            for required in ('scripts/build.py', 'scripts/make.py', 'scripts/insert.py',
                             'BPRE.ld', 'linker.ld', 'special_inserts.asm',
                             'hooks', 'repoints', 'functionrewrites'):
                self.assertTrue((exported / required).is_file(), required)
            for required in ('src', 'include', 'assembly', 'graphics', 'strings'):
                self.assertTrue((exported / required).is_dir(), required)
                self.assertTrue(any((exported / required).rglob('*')), required)
            for excluded in ('deps', 'build', '.git'):
                self.assertFalse((exported / excluded).exists(), excluded)
            files = {str(path.relative_to(exported)) for path in exported.rglob('*') if path.is_file()}
            self.assertEqual(files, expected, 'legitimate committed source set changed')
            self.assertFalse(any(self.excluded(path) for path in files))
            self.assertEqual(identity(), before, 'registered component changed during export')
            print(f'{name} exact-pin export: PASS; {len(files)} committed files; '
                  f'{len(command)} argv entries; required structure/exclusions/unchanged PASS')
        self.assertFalse(exported.exists())
        self.assertEqual(identity(), before)

    def test_cfru_exact_pin_export_smoke(self):
        self.smoke_exact_pin('CFRU')

    def test_dpe_exact_pin_export_smoke(self):
        self.smoke_exact_pin('DPE')


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
            init_storage_checkout(workspace)
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
            input_path = workspace / '04_private_roms' / 'PRIVATE_INPUT_MARKER.gba'
            input_path.write_bytes(FIXTURE)
            output_path = workspace / '05_builds' / 'PRIVATE_OUTPUT_MARKER.gba'
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
            self.assertEqual(set(workspace.rglob('*.gba')), {input_path, output_path})

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
