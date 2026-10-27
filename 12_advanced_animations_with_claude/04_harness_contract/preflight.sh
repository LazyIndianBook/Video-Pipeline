#!/usr/bin/env bash
# preflight.sh - is this machine ready to render ExamLeaf scenes? (edge cases 21, 22, 55)
#
# Checks: node >= 22 [N8], npx, ffmpeg, ffprobe, python3 >= 3.11, Chrome/Chromium or $CHROME [N17],
#         Devanagari + Bengali-Assamese font coverage (fc-list), free disk space, skills symlink [N66][N67];
#         with --workspace: secret scan (sk-ant-, AKIA, PRIVATE KEY blocks, api_key=) and effort/model greps
#         (ultracode effort in flags/env/settings; unversioned claude-opus/sonnet/haiku or bare aliases) (#3, #6, #40).
#         Added 15 Oct 2026 (audit M11). Matched text is never printed, only file names.
# Prints a PASS/WARN/FAIL table. Works on bash 3.2 (macOS default) and newer. No network, no installs.
#
# Usage:  preflight.sh [--dir PATH] [--workspace JOB_DIR] [--help]
#                                                  PATH is where frames will be written (default: current dir);
#                                                  JOB_DIR is the job folder to scan (scans are skipped without it)
#         preflight.sh --selftest                  list the checks and test the helpers; never fails on the environment
# Env:    CHROME=/path/to/chrome                   pin the browser binary [N17]
#         PREFLIGHT_MIN_FREE_GB (default 20)       WARN below this
#         PREFLIGHT_MIN_FREE_FAIL_GB (default 5)   FAIL below this
#         PREFLIGHT_FONTS_BUNDLED=1                fonts ship as local @font-face files: missing system fonts is only a WARN
# Exit:   0 no FAIL (WARN allowed) | 1 at least one FAIL (or selftest failed) | 2 usage error   (contract.md section 12)
set -u

MIN_NODE_MAJOR=22          # [N8] HyperFrames requires Node.js 22+
MIN_PY="3.11"              # engine pyproject requires-python >= 3.11
WARN_GB="${PREFLIGHT_MIN_FREE_GB:-20}"
FAIL_GB="${PREFLIGHT_MIN_FREE_FAIL_GB:-5}"
DIR="$PWD"
WS=""
ROWS=""; NPASS=0; NWARN=0; NFAIL=0
# Scan patterns (extended regex). Written so this file never matches its own patterns.
SECRET_RE='sk-ant-[A-Za-z0-9_-]{8,}|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|api_key[[:space:]]*[=:][[:space:]]*["'"'"']?[A-Za-z0-9_./+-]{8,}'
ULTRA_RE='(--effort[[:space:]=]+|EFFORT_LEVEL=["'"'"']?|"effortLevel"[[:space:]]*:[[:space:]]*")ultracode'
ALIAS_RE='claude-(opus|sonnet|haiku)(-latest|[^-0-9]|$)|"model"[[:space:]]*:[[:space:]]*"(opus|sonnet|haiku)"|--model[[:space:]=]+(opus|sonnet|haiku)([^-0-9a-z]|$)'


# ---- helpers ---------------------------------------------------------------------------
add() {  # add STATUS CHECK DETAIL
  case "$1" in PASS) NPASS=$((NPASS+1));; WARN) NWARN=$((NWARN+1));; FAIL) NFAIL=$((NFAIL+1));; esac
  ROWS="${ROWS}$(printf '%-6s %-26s %s' "$1" "$2" "$3")
"
}
major_of() { local v="${1#v}"; echo "${v%%.*}"; }
minor_of() { local v="${1#v}"; case "$v" in *.*) v="${v#*.}"; echo "${v%%.*}";; *) echo 0;; esac; }
ver_ge() {  # ver_ge FOUND WANTED (major.minor compare) -> exit 0 if FOUND >= WANTED
  local fa fb wa wb
  fa=$(major_of "$1"); fb=$(minor_of "$1"); wa=$(major_of "$2"); wb=$(minor_of "$2")
  [ "$fa" -gt "$wa" ] || { [ "$fa" -eq "$wa" ] && [ "$fb" -ge "$wb" ]; }
}
find_chrome() {  # echo the first usable Chrome/Chromium path, or nothing
  local c p
  for c in google-chrome google-chrome-stable chromium chromium-browser chrome; do
    p=$(command -v "$c" 2>/dev/null) && { echo "$p"; return; }
  done
  for p in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
    [ -x "$p" ] && { echo "$p"; return; }
  done
}
font_faces() {  # font_faces HEXCODEPOINT -> number of installed faces covering it (ignores .LastResort)
  fc-list ":charset=$1" family 2>/dev/null | grep -v '^\.LastResort' | grep -c . || true
}
free_gb() { df -Pk "$1" 2>/dev/null | awk 'NR==2{printf "%d", $4/1048576}'; }
scan() {  # scan DIR REGEX [-i] -> matching text files, one per line (never the matched text)
  grep -rIlE $3 --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=renders -e "$2" "$1" 2>/dev/null || true
}
scan_row() {  # scan_row CHECK REGEX FLAGS WHY
  local hits n; hits=$(scan "$WS" "$2" "$3"); n=$(printf '%s' "$hits" | grep -c . || true)
  if [ "$n" -eq 0 ]; then add PASS "$1" "no match in $WS"
  else add FAIL "$1" "$n file(s): $(printf '%s' "$hits" | head -5 | tr '\n' ' ')- $4"; fi
}

# ---- the checks ------------------------------------------------------------------------
check_node() {
  if ! command -v node >/dev/null 2>&1; then add FAIL "node >= $MIN_NODE_MAJOR" "node not found [N8]"; return; fi
  local v; v=$(node --version 2>/dev/null)
  if [ "$(major_of "$v")" -ge "$MIN_NODE_MAJOR" ] 2>/dev/null; then add PASS "node >= $MIN_NODE_MAJOR" "found $v [N8]"
  else add FAIL "node >= $MIN_NODE_MAJOR" "found $v; HyperFrames needs Node.js 22+ [N8] (edge case 22)"; fi
}
check_npx() {
  if command -v npx >/dev/null 2>&1; then add PASS "npx" "found $(command -v npx)"
  else add WARN "npx" "not found; needed for 'npx hyperframes init' [N9] and 'npx skills add' [N1] (verify)"; fi
}
check_ffmpeg() {
  local t
  for t in ffmpeg ffprobe; do
    if command -v "$t" >/dev/null 2>&1; then add PASS "$t" "$($t -version 2>/dev/null | head -1)"
    else add FAIL "$t" "not found in PATH [N8] (edge case 22)"; fi
  done
}
check_python() {
  if ! command -v python3 >/dev/null 2>&1; then add FAIL "python3 >= $MIN_PY" "python3 not found"; return; fi
  local v; v=$(python3 -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])' 2>/dev/null)
  if ver_ge "$v" "$MIN_PY"; then add PASS "python3 >= $MIN_PY" "found $v"
  else add FAIL "python3 >= $MIN_PY" "found $v; the engine requires >= $MIN_PY"; fi
}
check_chrome() {
  if [ -n "${CHROME:-}" ]; then
    if [ -x "$CHROME" ]; then add PASS "Chrome / \$CHROME" "CHROME=$CHROME [N17]"
    else add FAIL "Chrome / \$CHROME" "CHROME is set to '$CHROME' but it is not executable [N17] (edge case 21)"; fi
    return
  fi
  local p; p=$(find_chrome)
  if [ -n "$p" ]; then add PASS "Chrome / \$CHROME" "autodetected '$p'; export CHROME to pin it [N17]"
  else add FAIL "Chrome / \$CHROME" "no Chrome/Chromium found and CHROME unset: set CHROME=/path [N17] (edge case 21)"; fi
}
check_fonts() {
  if ! command -v fc-list >/dev/null 2>&1; then
    add WARN "fonts (Devanagari/Bengali)" "fc-list not available; cannot check coverage. Verify by rendering a shaping test card (edge case 55)"; return
  fi
  local dev ben asm bad=0 miss=""
  dev=$(font_faces 0915); ben=$(font_faces 0995); asm=$(font_faces 09f0)
  [ "$dev" -gt 0 ] || { bad=1; miss="$miss Devanagari(U+0915)"; }
  [ "$ben" -gt 0 ] || { bad=1; miss="$miss Bengali(U+0995)"; }
  [ "$asm" -gt 0 ] || { bad=1; miss="$miss Assamese-RA(U+09F0)"; }
  if [ "$bad" -eq 0 ]; then
    add PASS "fonts (Devanagari/Bengali)" "faces covering Devanagari=$dev Bengali=$ben Assamese-RA U+09F0=$asm (coverage is not shaping quality; still run the test card)"
  elif [ "${PREFLIGHT_FONTS_BUNDLED:-0}" = "1" ]; then
    add WARN "fonts (Devanagari/Bengali)" "no system font for:$miss; PREFLIGHT_FONTS_BUNDLED=1 so bundled @font-face fonts are assumed"
  else
    add FAIL "fonts (Devanagari/Bengali)" "no system font for:$miss -> tofu boxes (edge case 55). Install Noto-class fonts or bundle them and set PREFLIGHT_FONTS_BUNDLED=1"
  fi
}
check_disk() {
  local g; g=$(free_gb "$DIR")
  if [ -z "$g" ]; then add WARN "disk space" "could not read free space for $DIR"; return; fi
  local note="PNG frames at 1080x1920: a 10 min lesson at 30 fps is 18,000 frames; at an assumed ~1 MB each, two renders for the hash test need ~36 GB [Hypothesis; measure]"
  if [ "$g" -lt "$FAIL_GB" ]; then add FAIL "disk space" "${g} GB free at $DIR (< ${FAIL_GB} GB). $note"
  elif [ "$g" -lt "$WARN_GB" ]; then add WARN "disk space" "${g} GB free at $DIR (< ${WARN_GB} GB). $note"
  else add PASS "disk space" "${g} GB free at $DIR"; fi
}

check_skills_link() {  # edge case 26: 'skills add' installs into .agents/skills; Claude Code needs .claude/skills [N66][N67]
  [ -d ".agents/skills" ] || return 0   # only relevant if skills were installed in the current directory
  if [ -L ".claude/skills" ]; then add PASS ".claude/skills link" "symlink present; confirm it points at .agents/skills [N67]"
  elif [ -d ".claude/skills" ]; then add WARN ".claude/skills link" "real directory (not a symlink): skills in .agents/skills may be invisible to Claude Code [N67] (edge case 26)"
  else add WARN ".claude/skills link" ".agents/skills exists but .claude/skills does not: Claude Code will not load them [N66][N67] (edge case 26)"; fi
}

check_workspace_scans() {  # #40 secrets, #3/#4 ultracode, #6 unpinned aliases (doc 01 sections 6.5 and 9)
  if [ -z "$WS" ]; then
    add WARN "secret + effort scans" "skipped: pass --workspace <job folder> (scanning a repo root would match the docs)"; return
  fi
  scan_row "secret scan" "$SECRET_RE" "-i" "key-like strings: stop, rotate at the provider, purge, record (#40)"
  scan_row "ultracode scan" "$ULTRA_RE" "" "ultracode is refused for every run (AD-02, #3)"
  scan_row "model alias scan" "$ALIAS_RE" "" "pin full model IDs, never aliases (#6 [N28])"
}

# ---- selftest --------------------------------------------------------------------------
selftest() {
  local f=0
  t() { if [ "$2" = "ok" ]; then echo "  PASS $1"; else echo "  FAIL $1"; f=$((f+1)); fi; }
  echo "preflight.sh --selftest (no environment check is evaluated)"
  echo "Checks this script would run:"
  printf '  %-3s %-44s %-12s %s\n' 1 "node >= $MIN_NODE_MAJOR" "[N8]" "FAIL if missing or older"
  printf '  %-3s %-44s %-12s %s\n' 2 "npx" "[N9][N1]" "WARN if missing"
  printf '  %-3s %-44s %-12s %s\n' 3 "ffmpeg and ffprobe in PATH" "[N8]" "FAIL if missing"
  printf '  %-3s %-44s %-12s %s\n' 4 "python3 >= $MIN_PY" "engine" "FAIL if missing or older"
  printf '  %-3s %-44s %-12s %s\n' 5 "Chrome/Chromium or executable \$CHROME" "[N17]" "FAIL if neither"
  printf '  %-3s %-44s %-12s %s\n' 6 "fonts: U+0915 U+0995 U+09F0 via fc-list" "edge case 55" "FAIL if absent; WARN if no fc-list"
  printf '  %-3s %-44s %-12s %s\n' 7 "free disk space at --dir" "[Hypothesis]" "WARN < ${WARN_GB} GB, FAIL < ${FAIL_GB} GB"
  printf '  %-3s %-44s %-12s %s\n' 8 "./.claude/skills if ./.agents/skills exists" "[N66][N67]" "WARN if missing"
  printf '  %-3s %-44s %-12s %s\n' 9 "secret scan of --workspace" "#40 [N19]" "FAIL on a match; WARN if no --workspace"
  printf '  %-3s %-44s %-12s %s\n' 10 "ultracode effort scan of --workspace" "#3 [N24]" "FAIL on a match"
  printf '  %-3s %-44s %-12s %s\n' 11 "unversioned model alias scan of --workspace" "#6 [N28]" "FAIL on a match"
  echo "Helper tests:"
  [ "$(major_of v22.11.0)" = "22" ] && t "major_of v22.11.0 = 22" ok || t "major_of v22.11.0 = 22" no
  [ "$(major_of 3.14.2)" = "3" ] && t "major_of 3.14.2 = 3" ok || t "major_of 3.14.2 = 3" no
  [ "$(minor_of 3.14.2)" = "14" ] && t "minor_of 3.14.2 = 14" ok || t "minor_of 3.14.2 = 14" no
  ver_ge 3.14.2 3.11 && t "3.14.2 >= 3.11" ok || t "3.14.2 >= 3.11" no
  ver_ge 3.11.0 3.11 && t "3.11.0 >= 3.11 (boundary)" ok || t "3.11.0 >= 3.11 (boundary)" no
  ver_ge 3.9.18 3.11 && t "3.9.18 < 3.11 rejected" no || t "3.9.18 < 3.11 rejected" ok
  ver_ge 4 3.11 && t "4 >= 3.11 (no minor part)" ok || t "4 >= 3.11 (no minor part)" no
  ver_ge 3 3.11 && t "3 < 3.11 rejected" no || t "3 < 3.11 rejected" ok
  add PASS "table-format-probe" "row formatting works"; add WARN "table-format-probe" "row formatting works"; add FAIL "table-format-probe" "row formatting works"
  [ "$NPASS" = 1 ] && [ "$NWARN" = 1 ] && [ "$NFAIL" = 1 ] && t "status counters" ok || t "status counters" no
  local d; d=$(mktemp -d 2>/dev/null || mktemp -d -t preflight)   # scanner tests on synthetic files (15 Oct 2026)
  printf 'brief: ultracode is never used; model claude-opus-5-5\n' > "$d/clean.md"
  printf 'export K=%s\n' "sk-""ant-api03-ABCDEFGH1234" > "$d/k1.sh"
  printf 'aws=%s\n' "AK""IAABCDEFGHIJKLMNOP" > "$d/k2.txt"
  printf -- '-----%s-----\n' "BEGIN RSA PRIV""ATE KEY" > "$d/k3.pem"
  printf 'API_KEY = "%s"\n' "abcd1234efgh" > "$d/k4.py"
  printf 'claude --effort %s -p x\n' "ultra""code" > "$d/run1.sh"
  printf '{"effortLevel": "%s"}\n' "ultra""code" > "$d/s.json"
  printf 'claude --model claude-%s -p x\n' "opus" > "$d/run2.sh"
  printf '{"model": "%s"}\n' "sonnet" > "$d/s2.json"
  [ "$(scan "$d" "$SECRET_RE" -i | grep -c .)" = 4 ] && t "secret scan finds 4 key files, not the clean one" ok || t "secret scan finds 4 key files, not the clean one" no
  [ "$(scan "$d" "$ULTRA_RE" "" | grep -c .)" = 2 ] && t "ultracode scan finds flag and settings forms only" ok || t "ultracode scan finds flag and settings forms only" no
  [ "$(scan "$d" "$ALIAS_RE" "" | grep -c .)" = 2 ] && t "alias scan finds unversioned claude-opus and bare alias" ok || t "alias scan finds unversioned claude-opus and bare alias" no
  [ -z "$(scan "$0" "$SECRET_RE" -i)$(scan "$0" "$ULTRA_RE" "")" ] && t "this script does not match its own patterns" ok || t "this script does not match its own patterns" no
  rm -rf "$d"
  printf '%s' "$ROWS" | head -3 | sed 's/^/    /'
  echo "selftest: $([ $f -eq 0 ] && echo OK || echo FAILED) ($f failed)"
  [ "$f" -eq 0 ]
}

# ---- main ------------------------------------------------------------------------------
while [ $# -gt 0 ]; do
  case "$1" in
    --selftest) selftest; exit $? ;;
    --dir) [ $# -ge 2 ] || { echo "error: --dir needs a path" >&2; exit 2; }; DIR="$2"; shift 2 ;;
    --workspace) [ $# -ge 2 ] && [ -d "$2" ] || { echo "error: --workspace needs a directory" >&2; exit 2; }; WS="$2"; shift 2 ;;
    --help|-h) sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "error: unknown argument '$1' (try --help)" >&2; exit 2 ;;
  esac
done
[ -d "$DIR" ] || { echo "error: --dir '$DIR' is not a directory" >&2; exit 2; }

check_node; check_npx; check_ffmpeg; check_python; check_chrome; check_fonts; check_disk; check_skills_link
check_workspace_scans
printf '%-6s %-26s %s\n' STATUS CHECK DETAIL
printf '%-6s %-26s %s\n' ------ -------------------------- ------
printf '%s' "$ROWS"
echo "Summary: $NPASS PASS, $NWARN WARN, $NFAIL FAIL"
[ "$NFAIL" -eq 0 ]
