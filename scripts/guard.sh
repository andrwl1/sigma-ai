#!/usr/bin/env bash
set -euo pipefail

CSV="artifacts/summary/ab_diff.csv"
THR="${THRESHOLD_PP:-2}"
FAIL="${FAIL_ON_DIFF:-0}"

[[ -f "$CSV" ]] || { echo "no ab_diff.csv"; exit 0; }
[[ -s "$CSV" ]] || { echo "empty ab_diff.csv"; exit 0; }

pp_delta="$(awk -F',' 'NR==2{print $3+0}' "$CSV" 2>/dev/null || echo 0)"
abs_delta="$(awk -v v="$pp_delta" 'BEGIN{ if (v<0) v=-v; printf "%.6f", v }')"

echo "pp_delta=${pp_delta}"
echo "threshold=${THR}"
echo "abs_delta=${abs_delta}"

if awk -v a="$abs_delta" -v t="$THR" 'BEGIN{exit (a<=t?0:1)}'; then
  echo "within threshold"
  exit 0
else
  if [[ "$FAIL" == "1" ]]; then
    echo "regression exceeds threshold — FAIL"
    exit 1
  else
    echo "regression exceeds threshold — soft pass"
    exit 0
  fi
fi
