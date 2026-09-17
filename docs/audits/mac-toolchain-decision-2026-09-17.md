# macOS Toolchain Decision — wav2agb / mid2agb

**Evidence classification:** CONFIRMED CURRENT STATE. The repository-authorized
`pret/pokefirered` source route is now verified; the unrelated `midi2agb`
reimplementation remains a CONFLICT / LEGACY candidate.

## Exact CFRU revision

The intended integrated CFRU revision was inspected read-only:

`8bc8c38210ddba0b05c933dbda06cb4539254c7a`

Its `scripts/build.py` recursively processes existing `audio/**/*.wav` and
`audio/**/*.mid` inputs. The exact tree contains two WAV inputs:

- `audio/sounds/Wav_grass_footstep_sample.wav`
- `audio/sounds/Wav_sand_footstep_sample.wav`

and two MIDI inputs:

- `audio/sounds/grass_footstep.mid`
- `audio/sounds/sand_footstep.mid`

No corresponding generated `.s` files are tracked. `ProcessAudio` and
`ProcessMusic` invoke their converter when the generated object is absent or
older than the source/flag file; a clean checkout therefore requires both
conversion paths. Existing newer objects may skip regeneration.

## wav2agb

- Upstream: <https://github.com/ipatix/wav2agb>
- Tag: `v1.0.0`
- Exact source SHA: `7279d3cf899e53154482bcdcd66a483f6a4572ba`
- License: MIT
- Build: upstream `make` with Apple Clang C++17
- Result: native macOS arm64 executable; synthetic WAV conversion and
  `arm-none-eabi-as` syntax validation passed
- Activation: user-local tool directory under `$HOME/.local/firered-gen9-tools/bin`
- No binary redistribution or repository copy

**Classification:** SOURCE-BACKED NATIVE CANDIDATE — VERIFIED.

## mid2agb / midi2agb

The original Nintendo `mid2agb` source remains unavailable. The separately
tested `ipatix/midi2agb` reimplementation built natively and accepts basic
positional input and output arguments, but the exact CFRU flag line is not
drop-in compatible:

`-V 127 -G 0x848ED74`

The spaced form fails in that reimplementation; an attached form changes the
generated voicegroup symbol semantics. No alias, wrapper, symlink, rename, or
build.py change is authorized.

**Classification:** LEGACY / OBSOLETE candidate for this project. It is not the
authoritative tool route used by the repository.

### Follow-up flag semantics audit (public pret implementation)

The public `pret/pokefirered` `mid2agb` source documents `-V???` as master
volume and `-G???` as a numeric voicegroup number. Its parser accepts attached
or separate arguments, and its output formats the group as `voicegroup%03u`
and emits an `_mvl` header value. This is `CONFIRMED CURRENT STATE` for that
public implementation; the meaning of CFRU's historical hexadecimal literal
in any other proprietary tool variant remains UNKNOWN.

The exact CFRU MIDI files were tested with the unmodified public
`pret/pokefirered/tools/mid2agb` source at commit
`c75f352304d529f6ba92d4f74b9cf8b5c3810788` (2026-08-03, merge PR #770).
The tool built with the repository Makefile using Apple Clang 21 on macOS
arm64 and produced a Mach-O arm64 executable. For both
`grass_footstep.mid` and `sand_footstep.mid`:

- no flags, `-V127`, and `-V 127` produce `_mvl = 127` and the same output;
- `-G0`, `-G 0`, `-G848`, `-G 848`, `-G1`, `-G 1`, `-G127`, and `-G 127`
  produce `voicegroup000`, `voicegroup848`, `voicegroup001`, and
  `voicegroup127` respectively;
- both `-G0x848ED74` and `-G 0x848ED74` are accepted but, because the parser
  uses decimal `std::stoi`, produce `voicegroup000` (the hexadecimal suffix is
  not interpreted as an address);
- the exact CFRU form `-V 127 -G 0x848ED74` succeeds and produces
  `voicegroup000` with `_mvl = 127`;
- representative outputs assemble with the exact public CFRU `MPlayDef.s`,
  leaving an unresolved `voicegroup000`/`voicegroup848` symbol for the later
  linker step, and exact-command reruns are byte-for-byte deterministic.

The CFRU `scripts/build.py` then explicitly rewrites the generated music
`_grp` line to the `-G` flag value before assembling. Therefore the
hexadecimal `0x848ED74` is repository-authorized post-processing data, not a
`mid2agb` voicegroup-number argument. This is CONFIRMED CURRENT STATE for the
public source/toolchain path; the proprietary historical origin of that
address literal is UNKNOWN. The rewrite looks for a separate `-G` token, which
the exact CFRU flags provide; attached `-G0x848ED74` is therefore only a
converter-parser test, not an equivalent `build.py` flag-file form.

No exact generated `.s` output for either footstep MIDI was found in the
public CFRU history. The MIDI/WAV inputs were introduced by CFRU commit
`581114c`; no generated footstep `.s` counterpart is present in its history.

**Compatibility decision:** A. OFFICIAL / REPOSITORY-AUTHORIZED for the public
`pret/pokefirered` source route. The separate `ipatix/midi2agb` result above is
CONFLICT / LEGACY and must not be substituted.

## Decision

- `wav2agb`: ACTIVE REQUIRED for this revision's clean build path and now
  satisfied by the approved user-local source-built tool.
- `mid2agb`: ACTIVE REQUIRED for this revision's clean build path; the public
  pret source is source-backed and natively buildable on this macOS arm64 host,
  and is now activated user-locally at
  `$HOME/.local/firered-gen9-tools/bin/mid2agb`.
- Installed `mid2agb` SHA-256:
  `cab683f693c7081e1673e265167b36c92990e15ebf8805d06e04333eae08d06b`.
- The exact CFRU converter smoke passed for both public footstep WAV files and
  both public footstep MIDI files using `-V 127 -G 0x848ED74`; outputs were
  deterministic, assembled with devkitARM, and had no unresolved voicegroup
  symbol after the documented CFRU rewrite.
- Full `python3 scripts/build.py` passed on a separate exact CFRU checkout at
  `8bc8c38210ddba0b05c933dbda06cb4539254c7a`, producing the source/link
  outputs without protected inputs (exit code 0; the existing linker emitted
  only its RWX LOAD-segment warning). The Workspace Gitlink was not changed.
- Re-run source gates: Premier Ball callback PASS; coherent learnset source
  contract, sanitizer host (144,000 cases), and negative mutations PASS;
  M-009 ownership/scanner, map census, sanitizer host, and eight rejection
  cases PASS. The documented Showdown replay command is BLOCKED on this host's
  Python 3.9 because the current helper uses `zip(..., strict=True)`; no
  source workaround was applied.
