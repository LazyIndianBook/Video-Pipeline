#!/usr/bin/env bash
# reference_analysis.sh - turn a reference video into measurable pacing numbers (report section 7 rule 10).
#
# Steps: ffprobe (fps, duration, size) -> FFmpeg scene-change detection
#        select='gt(scene,THRESHOLD)',showinfo -> cut timestamps -> one still per shot (at the shot midpoint)
#        -> shot-length statistics (median, mean, min, max) with sort + awk.
#
# Standard FFmpeg/ffprobe usage, NOT run on a real file by the author (ffmpeg is not installed on the build
# machine): verify on your build. The showinfo line format can differ between FFmpeg versions; --selftest
# checks the parser against an embedded sample only.
#
# Usage:  reference_analysis.sh VIDEO OUT_DIR [--threshold 0.3] [--min-shot 0.1] [--no-stills]
#         reference_analysis.sh --selftest
# Writes: OUT_DIR/probe.txt showinfo.log cuts.txt shots.tsv analysis.json stills/shot_001.png ...
# Notes:  - threshold 0.3 is the common starting point; tune per reference (fast cuts: lower; fades: higher).
#         - cuts closer together than --min-shot seconds are merged (flash frames, dissolves).
#         - r_frame_rate != avg_frame_rate suggests variable fps: re-encode to constant fps before measuring.
#         - references are analysed for rhythm and layout only; never reuse their assets.
# Exit:   0 ok | 1 selftest failed | 2 usage error | 3 ffmpeg/ffprobe missing   (contract.md section 12)
set -u

THRESHOLD="0.3"; MIN_SHOT="0.1"; STILLS=1

# ---- parsing and statistics (pure functions on stdin/args; these are what --selftest exercises) --------
showinfo_times() {        # stdin: ffmpeg stderr. stdout: one pts_time per showinfo frame line
  grep 'showinfo' | sed -n 's/.*[[:space:]]pts_time:\([-0-9.]*\).*/\1/p'
}
dedupe_cuts() {           # $1 = min gap (s). stdin: times. stdout: sorted times; t<=0 and near-duplicates dropped
  sort -n | awk -v gap="$1" '$1 > 0 && (last == "" || $1 - last >= gap) { print $1; last = $1 }'
}
shots_table() {           # $1 = duration. stdin: cut times. stdout: idx start end length
  awk -v dur="$1" 'BEGIN { prev = 0; i = 0 }
    $1 < dur { i++; printf "%d\t%.4f\t%.4f\t%.4f\n", i, prev, $1, $1 - prev; prev = $1 }
    END { i++; printf "%d\t%.4f\t%.4f\t%.4f\n", i, prev, dur, dur - prev }'
}
shot_stats() {            # stdin: shots table. stdout: "n median mean min max"
  cut -f4 | sort -n | awk '{ a[NR] = $1; s += $1 }
    END { n = NR; if (n == 0) { print "0 0 0 0 0"; exit }
          med = (n % 2) ? a[(n + 1) / 2] : (a[n / 2] + a[n / 2 + 1]) / 2
          printf "%d %.4f %.4f %.4f %.4f\n", n, med, s / n, a[1], a[n] }'
}
frac_to_fps() {           # "30000/1001" -> 29.9700 ; "0/0" -> 0
  awk -v f="$1" 'BEGIN { n = split(f, p, "/"); if (n == 2 && p[2] + 0 != 0) printf "%.4f", p[1] / p[2]; else if (n == 1) printf "%.4f", f + 0; else printf "0.0000" }'
}
json_escape() { printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'; }
json_array() {            # stdin: one number per line -> [a, b, c]
  awk 'BEGIN { printf "[" } { printf "%s%s", (NR > 1 ? ", " : ""), $1 } END { printf "]" }'
}

# ---- selftest ----------------------------------------------------------------------------------------
SAMPLE_SHOWINFO='[Parsed_showinfo_1 @ 0x6000012d0000] config in time_base: 1/30000, frame_rate: 30000/1001
[Parsed_showinfo_1 @ 0x6000012d0000] n:   0 pts:  72072 pts_time:2.4024  duration:   1001 duration_time:0.0333667 fmt:yuv420p cl:left sar:1/1 s:1080x1920 i:P iskey:1 type:I checksum:5A1C2D3E plane_checksum:[5A1C2D3E 11111111 22222222] mean:[120 128 127] stdev:[40.1 3.2 3.0]
frame=  150 fps=0.0 q=-0.0 size=N/A time=00:00:05.00 bitrate=N/A speed=12x
[Parsed_showinfo_1 @ 0x6000012d0000] n:   1 pts: 156156 pts_time:5.205   duration:   1001 duration_time:0.0333667 fmt:yuv420p cl:left sar:1/1 s:1080x1920 i:P iskey:0 type:P checksum:AABBCCDD plane_checksum:[AABBCCDD 33333333 44444444] mean:[100 128 128] stdev:[30.0 2.0 2.0]
[Parsed_showinfo_1 @ 0x6000012d0000] n:   2 pts: 157157 pts_time:5.2385  duration:   1001 duration_time:0.0333667 fmt:yuv420p cl:left sar:1/1 s:1080x1920 i:P iskey:0 type:P checksum:AABBCCDE plane_checksum:[AABBCCDE 33333333 44444444] mean:[101 128 128] stdev:[30.0 2.0 2.0]
[Parsed_showinfo_1 @ 0x6000012d0000] n:   3 pts: 294294 pts_time:9.8098  duration:   1001 duration_time:0.0333667 fmt:yuv420p cl:left sar:1/1 s:1080x1920 i:P iskey:1 type:I checksum:01020304 plane_checksum:[01020304 55555555 66666666] mean:[90 128 128] stdev:[20.0 1.0 1.0]
[Parsed_showinfo_1 @ 0x6000012d0000] n:   4 pts: 420420 pts_time:14.014  duration:   1001 duration_time:0.0333667 fmt:yuv420p cl:left sar:1/1 s:1080x1920 i:P iskey:0 type:P checksum:0A0B0C0D plane_checksum:[0A0B0C0D 77777777 88888888] mean:[80 128 128] stdev:[10.0 1.0 1.0]
video:0kB audio:0kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: unknown'

selftest() {
  local f=0 got
  t() { if [ "$2" = "$3" ]; then echo "  PASS $1"; else echo "  FAIL $1 (got '$2', want '$3')"; f=$((f+1)); fi; }
  echo "reference_analysis.sh --selftest (embedded showinfo sample; ffmpeg is not run)"
  got=$(printf '%s\n' "$SAMPLE_SHOWINFO" | showinfo_times | tr '\n' ' ')
  t "showinfo parser finds 5 frame timestamps, ignores config/progress/summary lines" "$got" "2.4024 5.205 5.2385 9.8098 14.014 "
  got=$(printf '%s\n' "$SAMPLE_SHOWINFO" | showinfo_times | dedupe_cuts "$MIN_SHOT" | tr '\n' ' ')
  t "dedupe merges the 5.2385 flash cut (min-shot 0.1)" "$got" "2.4024 5.205 9.8098 14.014 "
  local cuts; cuts=$(printf '%s\n' "$SAMPLE_SHOWINFO" | showinfo_times | dedupe_cuts "$MIN_SHOT")
  got=$(printf '%s\n' "$cuts" | shots_table 20.02 | cut -f4 | tr '\n' ' ')
  t "shot lengths for duration 20.02" "$got" "2.4024 2.8026 4.6048 4.2042 6.0060 "
  got=$(printf '%s\n' "$cuts" | shots_table 20.02 | shot_stats)
  t "stats: n median mean min max" "$got" "5 4.2042 4.0040 2.4024 6.0060"
  got=$(printf '' | shots_table 12.5 | shot_stats)
  t "no cuts: one shot, median = duration" "$got" "1 12.5000 12.5000 12.5000 12.5000"
  got=$(printf '1\n3\n' | shots_table 4 | shot_stats)
  t "odd shot count (1,2,1): median is the middle value" "$got" "3 1.0000 1.3333 1.0000 2.0000"
  got=$(printf '1\n3\n6\n' | shots_table 10 | shot_stats)
  t "even shot count (1,2,3,4): median is the mean of the middle two = 2.5" "$got" "4 2.5000 2.5000 1.0000 4.0000"
  got=$(printf -- '-0.04\n0\n3\n' | dedupe_cuts 0.1 | tr '\n' ' ')
  t "dedupe drops t<=0" "$got" "3 "
  t "frac_to_fps 30000/1001" "$(frac_to_fps 30000/1001)" "29.9700"
  t "frac_to_fps 30/1" "$(frac_to_fps 30/1)" "30.0000"
  t "frac_to_fps 0/0 (no divide by zero)" "$(frac_to_fps 0/0)" "0.0000"
  t "json_array" "$(printf '1.5\n2\n' | json_array)" "[1.5, 2]"
  t "json_escape" "$(json_escape 'a"b\c')" 'a\"b\\c'
  echo "selftest: $([ $f -eq 0 ] && echo OK || echo FAILED) ($f failed)"
  [ "$f" -eq 0 ]
}

# ---- main --------------------------------------------------------------------------------------------
VIDEO=""; OUT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --selftest) selftest; exit $? ;;
    --threshold) [ $# -ge 2 ] || { echo "error: --threshold needs a value" >&2; exit 2; }; THRESHOLD="$2"; shift 2 ;;
    --min-shot) [ $# -ge 2 ] || { echo "error: --min-shot needs a value" >&2; exit 2; }; MIN_SHOT="$2"; shift 2 ;;
    --no-stills) STILLS=0; shift ;;
    --help|-h) sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "error: unknown option '$1' (try --help)" >&2; exit 2 ;;
    *) if [ -z "$VIDEO" ]; then VIDEO="$1"; elif [ -z "$OUT" ]; then OUT="$1"; else echo "error: too many arguments" >&2; exit 2; fi; shift ;;
  esac
done
[ -n "$VIDEO" ] && [ -n "$OUT" ] || { echo "usage: reference_analysis.sh VIDEO OUT_DIR [--threshold 0.3] [--min-shot 0.1] [--no-stills] | --selftest" >&2; exit 2; }
for v in "$THRESHOLD" "$MIN_SHOT"; do
  awk -v x="$v" 'BEGIN { exit !(x ~ /^[0-9]*\.?[0-9]+$/) }' || { echo "error: '$v' is not a non-negative number" >&2; exit 2; }
done
[ -f "$VIDEO" ] || { echo "error: no such file: $VIDEO" >&2; exit 2; }
command -v ffprobe >/dev/null 2>&1 && command -v ffmpeg >/dev/null 2>&1 || { echo "error: ffmpeg/ffprobe not found in PATH (run preflight.sh)" >&2; exit 2; }
mkdir -p "$OUT/stills" || { echo "error: cannot create $OUT" >&2; exit 2; }

# 1. probe: size and frame rates of the first video stream, container duration
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,avg_frame_rate -of default=noprint_wrappers=1 "$VIDEO" > "$OUT/probe.txt" || { echo "error: ffprobe failed" >&2; exit 2; }
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO" | head -1)
WIDTH=$(sed -n 's/^width=//p' "$OUT/probe.txt"); HEIGHT=$(sed -n 's/^height=//p' "$OUT/probe.txt")
RFR=$(sed -n 's/^r_frame_rate=//p' "$OUT/probe.txt"); AFR=$(sed -n 's/^avg_frame_rate=//p' "$OUT/probe.txt")
FPS_R=$(frac_to_fps "$RFR"); FPS_A=$(frac_to_fps "$AFR")
VFR=$(awk -v a="$FPS_R" -v b="$FPS_A" 'BEGIN { d = a - b; if (d < 0) d = -d; print (d > 0.01 ? "true" : "false") }')

# 2. scene-change detection. The filter graph is the standard select+showinfo idiom; showinfo logs go to stderr.
ffmpeg -hide_banner -nostats -i "$VIDEO" -an -vf "select='gt(scene,${THRESHOLD})',showinfo" -f null - 2> "$OUT/showinfo.log"
showinfo_times < "$OUT/showinfo.log" | dedupe_cuts "$MIN_SHOT" > "$OUT/cuts.txt"

# 3. shots, statistics
shots_table "$DURATION" < "$OUT/cuts.txt" > "$OUT/shots.tsv"
read -r NSHOTS MEDIAN MEAN MINL MAXL <<EOF_STATS
$(shot_stats < "$OUT/shots.tsv")
EOF_STATS

# 4. one still per shot, at the shot midpoint (the first frame after a cut is often mid-transition)
if [ "$STILLS" -eq 1 ]; then
  while IFS="$(printf '\t')" read -r idx start end len; do
    mid=$(awk -v s="$start" -v l="$len" 'BEGIN { printf "%.3f", s + l / 2 }')
    ffmpeg -hide_banner -loglevel error -ss "$mid" -i "$VIDEO" -frames:v 1 -y "$(printf '%s/stills/shot_%03d.png' "$OUT" "$idx")" || echo "warning: still $idx failed" >&2
  done < "$OUT/shots.tsv"
fi

# 5. report
{
  printf '{\n  "video": "%s",\n  "note": "standard FFmpeg usage; verify on your build",\n' "$(json_escape "$VIDEO")"
  printf '  "width": %s, "height": %s,\n' "${WIDTH:-null}" "${HEIGHT:-null}"
  printf '  "r_frame_rate": "%s", "avg_frame_rate": "%s", "fps": %s, "variable_fps_suspected": %s,\n' "$RFR" "$AFR" "$FPS_A" "$VFR"
  printf '  "duration_s": %s,\n  "scene_threshold": %s, "merge_cuts_closer_than_s": %s,\n' "$DURATION" "$THRESHOLD" "$MIN_SHOT"
  printf '  "cut_times_s": %s,\n' "$(json_array < "$OUT/cuts.txt")"
  printf '  "shot_lengths_s": %s,\n' "$(cut -f4 "$OUT/shots.tsv" | json_array)"
  printf '  "n_shots": %s, "median_shot_s": %s, "mean_shot_s": %s, "min_shot_s": %s, "max_shot_s": %s\n}\n' "$NSHOTS" "$MEDIAN" "$MEAN" "$MINL" "$MAXL"
} > "$OUT/analysis.json"
echo "fps=$FPS_A duration=${DURATION}s size=${WIDTH}x${HEIGHT} variable_fps_suspected=$VFR"
echo "shots=$NSHOTS median=${MEDIAN}s mean=${MEAN}s min=${MINL}s max=${MAXL}s   (threshold $THRESHOLD, min-shot ${MIN_SHOT}s)"
echo "wrote $OUT/analysis.json, cuts.txt, shots.tsv$([ "$STILLS" -eq 1 ] && echo ", stills/")"
