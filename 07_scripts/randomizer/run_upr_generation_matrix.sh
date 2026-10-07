#!/bin/sh
# User-owned execution only. Codex tests this entry point with mocks/no ROM.
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$script_dir/upr_generation_matrix.py" "$@"
