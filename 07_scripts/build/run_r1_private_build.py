#!/usr/bin/env python3
"""User-owned POSIX R1 build. No ROM inspection, hashes, or persistent logs."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile

BASE = '5a14e200c926646886990d0a802ffe878dcaf9f5'
PINS = {
    'CFRU': ('02_external/CFRU-expansion', 'c9a7f19f1e8aaebd33213503f32fa7bba59ce81c'),
    'DPE': ('02_external/Dynamic-Pokemon-Expansion-Gen-9', '22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc'),
    'UPR-FVX': ('02_external/upr-fvx', '7bf79ee1e7c46c972f7a9c84942970a950be0723'),
}
TOOLS = ('python3', 'arm-none-eabi-as', 'arm-none-eabi-gcc',
         'arm-none-eabi-ld', 'arm-none-eabi-objcopy', 'arm-none-eabi-objdump',
         'arm-none-eabi-nm', 'grit', 'wav2agb', 'mid2agb')
# Fixed Git-side exclusions: argv never grows with committed file count.
# Glob **/ covers root and nested names; icase preserves suffix.lower() behavior.
EXPORT_EXCLUDES = (
    ':(top,exclude)deps', ':(top,exclude)build', ':(top,exclude).git',
    *(f':(glob,icase,exclude)**/*{suffix}' for suffix in
      ('.gba', '.gb', '.gbc', '.sav', '.state', '.exe', '.dll', '.jar', '.zip', '.7z')),
    ':(glob,icase,exclude)**/*.srm', ':(glob,icase,exclude)**/*.ss[0-9]*',
    ':(glob,exclude)**/.env*', ':(glob,exclude)**/.env*/**',
)
PROFILE_FILES = {'07_scripts/build/run_r1_private_build.py',
                 '07_scripts/build/tests/test_r1_private_build.py',
                 'docs/build/r1-private-build.md'}
# DPE's committed make.py ignores os.system insert status. Adapt execution,
# without editing its source, so a failed nested build/insert always fails.
DPE_MAKE = """import os, runpy, subprocess, sys
sys.path.insert(0, 'scripts')
def checked_system(command):
    subprocess.run(command, shell=True, check=True)
    return 0
os.system = checked_system
runpy.run_path('scripts/make.py', run_name='__main__')
"""


class BuildFailure(Exception):
    """Only constant, non-sensitive reasons may be reported."""


def git(root: Path, *args: str) -> str:
    result = subprocess.run(['git', '-C', str(root), *args],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if result.returncode:
        raise BuildFailure('source metadata unavailable or unsupported')
    return result.stdout.decode('utf-8').strip()


def validate_profile(workspace: Path) -> None:
    git(workspace, 'merge-base', '--is-ancestor', BASE, 'HEAD')
    changed = git(workspace, 'diff', '--name-only', BASE, 'HEAD').splitlines()
    if set(changed) - PROFILE_FILES:
        raise BuildFailure('unsupported Workspace profile')
    for name, (relative, pin) in PINS.items():
        if git(workspace, 'rev-parse', f'HEAD:{relative}') != pin:
            raise BuildFailure(f'{name} pin mismatch')
        index = git(workspace, 'ls-files', '--stage', '--', relative).split()
        if len(index) < 3 or index[:3] != ['160000', pin, '0']:
            raise BuildFailure(f'{name} index pin mismatch')
        component = workspace / relative
        if git(component, 'rev-parse', '--show-toplevel') != str(component.resolve()):
            raise BuildFailure(f'{name} checkout unavailable')
        if git(component, 'rev-parse', 'HEAD') != pin:
            raise BuildFailure(f'{name} checkout pin mismatch')
        git(component, 'cat-file', '-e', f'{pin}^{{commit}}')


def validate_tools() -> None:
    missing = [tool for tool in TOOLS if shutil.which(tool) is None]
    if missing:
        raise BuildFailure('missing tools: ' + ', '.join(missing))
    if os.name != 'posix':
        raise BuildFailure('unsupported host; POSIX required')


def validate_output(workspace: Path, output: Path) -> None:
    resolved = output.resolve()
    if resolved == workspace.resolve() or workspace.resolve() in resolved.parents:
        raise BuildFailure('output inside Workspace is prohibited')
    if os.path.lexists(output):
        raise BuildFailure('output already exists')
    if not output.parent.is_dir():
        raise BuildFailure('output parent must be an existing directory')
    # Also reject tracked/source destinations in other Git checkouts.
    result = subprocess.run(['git', '-C', str(output.parent), 'rev-parse',
                             '--is-inside-work-tree'], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)
    if result.returncode == 0 and result.stdout.strip() == b'true':
        raise BuildFailure('output inside a Git checkout is prohibited')


def export_source(component: Path, pin: str, destination: Path) -> None:
    destination.mkdir()
    # Git excludes protected entries before producing the archive stream.
    exported_files = 0
    with subprocess.Popen(['git', '-C', str(component), 'archive', pin, '--',
                           '.', *EXPORT_EXCLUDES],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as child:
        try:
            with tarfile.open(fileobj=child.stdout, mode='r|') as archive:
                for member in archive:
                    target = destination / member.name
                    if (destination.resolve() not in target.resolve().parents
                            or not (member.isdir() or member.isfile())):
                        raise BuildFailure('unsupported source archive entry')
                    if member.isdir():
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        with archive.extractfile(member) as source, target.open('xb') as sink:
                            shutil.copyfileobj(source, sink)
                        target.chmod(member.mode & 0o777)
                        exported_files += 1
        except BaseException:
            child.kill()
            child.wait()
            raise
        if child.wait() != 0:
            raise BuildFailure('source export returned non-zero')
    if not exported_files:
        raise BuildFailure('empty source export')


def run_child(tree: Path, script: str, *, dpe_make: bool = False) -> None:
    command = ['python3', '-c', DPE_MAKE] if dpe_make else ['python3', script]
    # Never persist or relay compiler/insert output: it can contain private paths.
    with subprocess.Popen(command, cwd=tree, stdin=subprocess.DEVNULL,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          start_new_session=True) as child:
        try:
            returncode = child.wait()
        except BaseException:
            # Stop nested make/build/insert children before removing their tree.
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait()
            raise
    if returncode != 0:
        raise BuildFailure('child process returned non-zero')


def require_absent(output: Path) -> None:
    if os.path.lexists(output):
        raise BuildFailure('pre-existing component output')


def require_fresh(output: Path) -> None:
    if output.is_symlink() or not output.is_file():
        raise BuildFailure('fresh component output missing or not regular')


def execute(workspace: Path, base_rom: Path, output: Path) -> int:
    stage = 'Profile'
    temporary = None
    staged_output = None
    failure = None
    print('R1 private build')
    try:
        validate_profile(workspace)
        print('Profile: OK')
        stage = 'Toolchain'
        validate_tools()
        print('Toolchain: OK')
        stage = 'Final output preflight'
        validate_output(workspace, output)
        stage = 'Source export'
        temporary = tempfile.TemporaryDirectory(prefix='r1-private-build-')
        area = Path(temporary.name)
        # Refuse a TMPDIR configured inside any source checkout.
        validate_output(workspace, area / 'unused-output')
        for name in ('DPE', 'CFRU'):
            relative, pin = PINS[name]
            export_source(workspace / relative, pin, area / name)
        dpe, cfru = area / 'DPE', area / 'CFRU'
        require_absent(dpe / 'test.gba')
        require_absent(cfru / 'test.gba')
        stage = 'DPE source build'
        run_child(dpe, 'scripts/build.py')
        print(stage + ': PASS')
        stage = 'Private input'
        if base_rom.is_symlink() or not base_rom.is_file():
            raise BuildFailure('input must be an existing regular file')
        # Input within the Workspace is prohibited too; no source-file copying.
        if workspace.resolve() in base_rom.resolve().parents:
            raise BuildFailure('input inside Workspace is prohibited')
        shutil.copyfile(base_rom, dpe / 'BPRE0.gba')
        stage = 'DPE insertion'
        require_absent(dpe / 'test.gba')
        run_child(dpe, 'scripts/make.py', dpe_make=True)
        require_fresh(dpe / 'test.gba')
        print(stage + ': PASS')
        stage = 'DPE to CFRU handoff'
        shutil.copyfile(dpe / 'test.gba', cfru / 'BPRE0.gba')
        stage = 'CFRU source build'
        run_child(cfru, 'scripts/build.py')
        print(stage + ': PASS')
        # The pinned insert.py already enforces M-009/source and linked AI gates.
        stage = 'CFRU insertion'
        require_absent(cfru / 'test.gba')
        run_child(cfru, 'scripts/make.py')
        require_fresh(cfru / 'test.gba')
        print(stage + ': PASS')
        stage = 'Final output'
        validate_output(workspace, output)
        descriptor, name = tempfile.mkstemp(prefix='.r1-publish-', dir=output.parent)
        staged_output = Path(name)
        with os.fdopen(descriptor, 'wb') as sink, (cfru / 'test.gba').open('rb') as source:
            shutil.copyfileobj(source, sink)
        # Cleanup must succeed before an output is published as READY.
    except KeyboardInterrupt:
        failure = (stage, 'interrupted')
    except BuildFailure as error:
        failure = (stage, str(error))
    except Exception:
        failure = (stage, 'operation failed')
    finally:
        if temporary is not None:
            try:
                temporary.cleanup()
                print('Temporary build area: CLEANED')
            except KeyboardInterrupt:
                failure = ('Cleanup', 'interrupted')
                try:
                    temporary.cleanup()
                    print('Temporary build area: CLEANED')
                except (Exception, KeyboardInterrupt):
                    failure = ('Cleanup', 'temporary build cleanup failed')
            except Exception:
                failure = ('Cleanup', 'temporary build cleanup failed')
    if staged_output is not None:
        try:
            if failure is None:
                # Atomic no-clobber publication, including a racing destination.
                os.link(staged_output, output)
        except KeyboardInterrupt:
            failure = ('Final output', 'interrupted')
        except Exception:
            failure = ('Final output', 'output publication failed')
        finally:
            try:
                staged_output.unlink()
            except KeyboardInterrupt:
                failure = ('Cleanup', 'interrupted')
                try:
                    staged_output.unlink(missing_ok=True)
                except (Exception, KeyboardInterrupt):
                    failure = ('Cleanup', 'output staging cleanup failed')
            except Exception:
                failure = ('Cleanup', 'output staging cleanup failed')
    if failure:
        print('R1_PRIVATE_BUILD_FAILED')
        print('Stage: ' + failure[0])
        print('Reason: ' + failure[1])
        return 1
    print('Final output: READY')
    return 0


class SanitizedParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse otherwise echoes unknown arguments (possibly private paths).
        self.exit(2, 'R1_PRIVATE_BUILD_FAILED\nStage: CLI\nReason: invalid arguments\n')


def main(argv=None) -> int:
    parser = SanitizedParser(description=__doc__)
    parser.add_argument('--base-rom', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    return execute(Path(__file__).resolve().parents[2], args.base_rom, args.output)


if __name__ == '__main__':
    sys.exit(main())
