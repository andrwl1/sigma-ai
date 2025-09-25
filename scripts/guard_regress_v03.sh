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
if [ ! -f "$DIFF" ]; then exit 2; fi
if [ ! -s "$DIFF" ]; then exit 3; fi
H="$(head -n1 "$DIFF")"
if [ "$H" != "prompt_id,model_a,model_b,equal,delta_pp" ]; then exit 4; fi
ROWS="$(wc -l < "$DIFF" | tr -d ' ')"
if [ "$ROWS" -lt "$MIN_ROWS" ]; then exit 5; fi
if [ ! -f "$MAN" ]; then exit 6; fi
if [ ! -s "$MAN" ]; then exit 7; fi
if [ ! -f "$PLOT" ]; then exit 8; fi
if [ ! -s "$PLOT" ]; then exit 9; fi
if [ "$(wc -c < "$PLOT" | tr -d ' ')" -lt 1000 ]; then exit 10; fi
if [ -f "$PASSFAIL" ]; then
  if [ ! -s "$PASSFAIL" ]; then exit 11; fi
fi
if [ "$FAIL_ON_DIFF" = "1" ]; then
  BAD="$(awk -F, 'NR>1 && $5 != 0 {c++} END{print c+0}' "$DIFF")"
  if [ "$BAD" -gt 0 ]; then exit 12; fi
else
  awk -F, 'NR>1 && $5 != 0 {f=1} END{if(f) print "warn: nonzero deltas"}' "$DIFF" >/dev/stderr || true
fi
echo "Guard: OK"
exit 0
