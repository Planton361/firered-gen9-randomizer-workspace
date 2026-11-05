#!/bin/sh
# Local DPE -> CFRU build into a separate, git-ignored 05_builds folder.
#
# Usage:  07_scripts/build/dev_build.sh [--release] <clean FireRed BPRE rev0 ROM>
#
#   FAST (default): builds the component checkouts as they are. Actual commits,
#                   Gitlink deviations and local changes are recorded, not enforced.
#   --release:      additionally requires a clean Workspace, DPE/CFRU HEAD equal
#                   to the Workspace Gitlinks, and clean DPE/CFRU worktrees.
#
# Existing in-place artifacts (BPRE0.gba, test.gba, offsets.ini, build/) of DPE
# and CFRU are MOVED (never deleted) into $OUT/pre-build-archive/ first. Results
# are COPIED to $OUT. The base ROM is only read. Never commit any output.
set -eu

MODE=FAST
if [ "${1:-}" = "--release" ]; then MODE=RELEASE; shift; fi

WS=$(cd "$(dirname "$0")/../.." && pwd -P)
DPE_REL=02_external/Dynamic-Pokemon-Expansion-Gen-9
CFRU_REL=02_external/CFRU-expansion
DPE="$WS/$DPE_REL"
CFRU="$WS/$CFRU_REL"

BASE_ROM=${1:?"usage: dev_build.sh [--release] <clean BPRE rev0 base ROM>"}
TS=$(date +%Y%m%d-%H%M%S)
if [ "$MODE" = RELEASE ]; then NAME="release-$TS"; else NAME="dev-$TS"; fi
OUT="$WS/05_builds/$NAME"
ARCH="$OUT/pre-build-archive"

die() { echo "STOP: $*" >&2; exit 1; }
# On any failure or Ctrl-C, point to the preserved previous artifacts.
trap 'rc=$?; if [ $rc -ne 0 ] && [ -d "$ARCH" ]; then echo "NOTE: previous in-place artifacts are preserved in $ARCH" >&2; fi' EXIT
trap 'exit 130' INT TERM
# Canonical path with every symlink resolved, including the last element.
canon() { python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$1"; }
# Fingerprint of tracked/untracked state, used to detect build-time source edits.
tree_state() { { git -C "$1" status --porcelain; git -C "$1" diff HEAD; } | shasum | cut -c1-40; }
gitlink() { git -C "$WS" ls-tree HEAD "$1" | awk '{print $3}'; }
dirty_count() { git -C "$1" status --porcelain | wc -l | tr -d ' '; }

# --- Preconditions -----------------------------------------------------------
[ -f "$BASE_ROM" ] || die "base ROM not found"
# 05_builds must be a real directory inside the Workspace, not a symlink.
if [ -L "$WS/05_builds" ] || [ ! -d "$WS/05_builds" ] || [ "$(canon "$WS/05_builds")" != "$WS/05_builds" ]; then
    die "05_builds must be an existing real directory inside the Workspace (no symlink)"
fi
ROM_REAL=$(canon "$BASE_ROM")
case "$ROM_REAL" in
    "$(canon "$DPE")"/*|"$(canon "$CFRU")"/*|"$WS/05_builds"/*)
        die "base ROM (after resolving symlinks) must not live inside DPE, CFRU or 05_builds" ;;
esac
{ [ ! -e "$OUT" ] && [ ! -L "$OUT" ]; } || die "$OUT already exists"
git -C "$WS" check-ignore -q "05_builds/$NAME" || die "05_builds is not git-ignored"
for t in arm-none-eabi-gcc grit wav2agb mid2agb python3; do
    command -v "$t" >/dev/null || die "$t not in PATH (open a login shell / source ~/.zprofile)"
done
# ROM header: game code at 0xAC must be BPRE, version byte at 0xBC must be 0.
code=$(dd if="$BASE_ROM" bs=1 skip=172 count=4 2>/dev/null)
ver=$(dd if="$BASE_ROM" bs=1 skip=188 count=1 2>/dev/null | od -An -tu1 | tr -d ' ')
[ "$code" = "BPRE" ] && [ "$ver" = "0" ] || die "base ROM is not BPRE rev0 (code=$code ver=$ver)"

DPE_HEAD=$(git -C "$DPE" rev-parse HEAD)
CFRU_HEAD=$(git -C "$CFRU" rev-parse HEAD)
if [ "$MODE" = RELEASE ]; then
    [ -z "$(git -C "$WS" status --porcelain)" ] || die "RELEASE: Workspace not clean (incl. Gitlink deviations)"
    [ "$DPE_HEAD" = "$(gitlink "$DPE_REL")" ] || die "RELEASE: DPE HEAD differs from Workspace Gitlink"
    [ "$CFRU_HEAD" = "$(gitlink "$CFRU_REL")" ] || die "RELEASE: CFRU HEAD differs from Workspace Gitlink"
    [ "$(dirty_count "$DPE")" = 0 ] || die "RELEASE: DPE worktree not clean"
fi
# CFRU's own make.py (scripts/check_native_source_identity.py) refuses any
# tracked change or unignored untracked file. Fail before archiving/DPE work.
if git -C "$CFRU" status --porcelain --untracked-files=all | grep -v '^?? BPRE0\.gba$' | grep -q .; then
    die "CFRU worktree not clean; CFRU's native build requires committed source (commit WIP on a CFRU feature branch)"
fi

# --- Archive previous in-place artifacts (move, never delete) ----------------
mkdir -p "$ARCH/dpe" "$ARCH/cfru"
[ "$(canon "$ARCH")" = "$ARCH" ] || die "output path resolves outside $WS/05_builds"
for f in BPRE0.gba test.gba offsets.ini build; do
    # -L also catches dangling symlinks, which cp would otherwise follow.
    if [ -e "$DPE/$f" ] || [ -L "$DPE/$f" ]; then mv "$DPE/$f" "$ARCH/dpe/"; fi
    if [ -e "$CFRU/$f" ] || [ -L "$CFRU/$f" ]; then mv "$CFRU/$f" "$ARCH/cfru/"; fi
done
for f in BPRE0.gba test.gba offsets.ini build; do
    if [ -e "$DPE/$f" ] || [ -L "$DPE/$f" ] || [ -e "$CFRU/$f" ] || [ -L "$CFRU/$f" ]; then
        die "$f still present after archiving"
    fi
done

DPE_SHORT=$(git -C "$DPE" rev-parse --short=7 HEAD)
CFRU_SHORT=$(git -C "$CFRU" rev-parse --short=8 HEAD)
DPE_DIRTY=$(dirty_count "$DPE")
if [ "$DPE_DIRTY" != 0 ]; then DPE_SHORT="$DPE_SHORT-dirty"; fi
DPE_ROM="$OUT/dpe-$DPE_SHORT.gba"
CFRU_ROM="$OUT/cfru-$CFRU_SHORT-dpe-$DPE_SHORT.gba"

# --- DPE ------------------------------------------------------------------------
cp "$BASE_ROM" "$DPE/BPRE0.gba"
dpe_state=$(tree_state "$DPE")
( cd "$DPE" && python3 scripts/make.py ) > "$OUT/dpe-build.log" 2>&1 \
    || { tail -20 "$OUT/dpe-build.log"; die "DPE build failed (see dpe-build.log)"; }
tail -5 "$OUT/dpe-build.log"
[ -f "$DPE/test.gba" ] || die "DPE produced no test.gba"
# DPE make.py ignores insert.py's exit code; require its success marker.
grep -q '^Inserted in ' "$OUT/dpe-build.log" || die "DPE insert did not complete (see dpe-build.log)"
[ "$(tree_state "$DPE")" = "$dpe_state" ] || die "DPE build changed tracked files"
cp "$DPE/test.gba" "$DPE_ROM"
cp "$DPE/offsets.ini" "$OUT/dpe-offsets.ini"

# --- CFRU on top of the DPE output -------------------------------------------
cp "$DPE/test.gba" "$CFRU/BPRE0.gba"
cmp -s "$DPE_ROM" "$CFRU/BPRE0.gba" || die "CFRU input differs from fresh DPE output"
cfru_state=$(tree_state "$CFRU")
( cd "$CFRU" && python3 scripts/make.py ) > "$OUT/cfru-build.log" 2>&1 \
    || { tail -20 "$OUT/cfru-build.log"; die "CFRU build failed (see cfru-build.log)"; }
tail -5 "$OUT/cfru-build.log"
[ -f "$CFRU/test.gba" ] || die "CFRU produced no test.gba"
[ "$(tree_state "$CFRU")" = "$cfru_state" ] || die "CFRU build changed tracked files"
cp "$CFRU/test.gba" "$CFRU_ROM"
cp "$CFRU/offsets.ini" "$OUT/cfru-offsets.ini"

# --- Record what was actually built ------------------------------------------
link_note() { if [ "$2" = "$(gitlink "$1")" ]; then echo "matches Gitlink"; else echo "DEVIATES from Gitlink $(gitlink "$1")"; fi; }
{
    if [ "$MODE" = RELEASE ]; then
        echo "Build $NAME — RELEASE (Workspace-pinned, clean)"
    else
        echo "Build $NAME — FAST (local development candidate, not release evidence)"
    fi
    echo "Workspace: $(git -C "$WS" rev-parse HEAD) ($(git -C "$WS" rev-parse --abbrev-ref HEAD)); changed entries: $(dirty_count "$WS")"
    echo "DPE:  $DPE_HEAD; $(link_note "$DPE_REL" "$DPE_HEAD"); local changes: $DPE_DIRTY"
    echo "CFRU: $CFRU_HEAD; $(link_note "$CFRU_REL" "$CFRU_HEAD"); local changes: 0"
    echo "Toolchain: $(arm-none-eabi-gcc --version | head -1); $(python3 --version)"
    ( cd "$OUT" && shasum -a 256 ./*.gba )
} > "$OUT/BUILD_INFO.txt"
cat "$OUT/BUILD_INFO.txt"
echo "OK -> $OUT"
