#!/bin/sh
# Professor Diki regression suite: QA A11–A21 regressions, render audio extras, brand and motif selftests.
# Usage: sh tests/run_all.sh        (PY = the project venv python; it needs imageio_ffmpeg and playwright)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PY:-$HOME/Movies/DikiStudio/.venv/bin/python}
[ -x "$PY" ] || PY=python3
"$PY" "$HERE/test_regressions.py"
"$PY" "$HERE/../brand/brand_check.py" --selftest >/dev/null && echo "PASS  brand_check.py --selftest"
if [ -f "$HERE/../brand/motif/make_motif.py" ]; then
  "$PY" "$HERE/../brand/motif/make_motif.py" --selftest >/dev/null && echo "PASS  make_motif.py --selftest"
fi
echo "run_all: OK"
