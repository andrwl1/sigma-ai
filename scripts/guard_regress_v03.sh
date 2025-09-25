#!/usr/bin/env bash
set -euo pipefail
SUM="artifacts/summary"
PLOTS="artifacts/plots"
ART="artifacts"
DIFF="$SUM/ab_diff.csv"
PASSFAIL="$SUM/passfail.png"
PLOT="$PLOTS/ab_plot.png"
MAN="$ART/manifest.json"
MIN_ROWS="${MIN_ROWS:-30}"
FAIL_ON_DIFF="${FAIL_ON_DIFF:-1}"

[ -f "$DIFF" ] || exit 2
[ -s "$DIFF" ] || exit 3

DELTA_COL="$(awk -F, 'NR==1{for(i=1;i<=NF;i++) if($i ~ /^delta(_pp)?$/){print i; exit}}' "$DIFF")"
[ -n "${DELTA_COL:-}" ] || exit 4

ROWS="$(wc -l < "$DIFF" | tr -d ' ')"
[ "$ROWS" -ge "$MIN_ROWS" ] || exit 5

[ -f "$MAN" ] || exit 6
[ -s "$MAN" ] || exit 7

[ -f "$PLOT" ] || exit 8
[ -s "$PLOT" ] || exit 9
[ "$(wc -c < "$PLOT" | tr -d ' ')" -ge 1000 ] || exit 10

if [ -f "$PASSFAIL" ]; then
  [ -s "$PASSFAIL" ] || exit 11
fi

if [ "$FAIL_ON_DIFF" = "1" ]; then
  BAD="$(awk -F, -v C="$DELTA_COL" 'NR>1 && $C != 0 {c++} END{print c+0}' "$DIFF")"
  [ "$BAD" -eq 0 ] || exit 12
else
  awk -F, -v C="$DELTA_COL" 'NR>1 && $C != 0 {f=1} END{if(f) print "warn: nonzero deltas"}' "$DIFF" >/dev/stderr || true
fi

echo "Guard: OK"
exit 0
