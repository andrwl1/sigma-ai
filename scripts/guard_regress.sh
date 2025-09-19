#!/usr/bin/env bash
set -euo pipefail

CSV_PATH="${CSV_PATH:-artifacts/summary/ab_diff.csv}"
PNG_PATH="${PNG_PATH:-artifacts/plots/ab_plot.png}"
FAIL_ON_DIFF="${FAIL_ON_DIFF:-0}"

if [ ! -f "$CSV_PATH" ]; then echo "ERR: CSV not found: $CSV_PATH" >&2; exit 1; fi
if [ ! -f "$PNG_PATH" ]; then echo "ERR: PNG not found: $PNG_PATH" >&2; exit 1; fi

CSV_LINES=$(wc -l < "$CSV_PATH" | tr -d ' ')
if [ "$CSV_LINES" -lt 2 ]; then echo "ERR: CSV empty or header-only: $CSV_PATH (lines=$CSV_LINES)" >&2; exit 1; fi
if [ ! -s "$PNG_PATH" ]; then echo "ERR: PNG is zero bytes: $PNG_PATH" >&2; exit 1; fi

if [ "$FAIL_ON_DIFF" = "1" ]; then
  if awk -F, 'NR>1 { for(i=1;i<=NF;i++) if ($i ~ /^-?[0-9]+(\.[0-9]+)?$/ && $i+0 != 0) exit 1 }' "$CSV_PATH"; then
    echo "DIFF: all numeric deltas are zero"
  else
    echo "DIFF: non-zero deltas detected"; exit 1
  fi
else
  echo "SOFT: diff check skipped (FAIL_ON_DIFF=0)"
fi

echo "OK: artifacts validated"
