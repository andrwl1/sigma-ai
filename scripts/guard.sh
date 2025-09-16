#!/usr/bin/env bash
set -euo pipefail
[[ -f artifacts/summary/ab_diff.csv ]] || { echo "no ab_diff.csv"; exit 0; }
[[ -s artifacts/summary/ab_diff.csv ]] || { echo "empty ab_diff.csv"; exit 0; }
pp_delta="$(awk -F, 'NR==2{print $3+0}' artifacts/summary/ab_diff.csv)"
thr="${THRESHOLD_PP:-2}"
fail="${FAIL_ON_DIFF:-0}"
abs_delta="$(python3 - <<'PY'
import sys
v=float(sys.argv[1])
print(abs(v))
PY
"$pp_delta")"
echo "pp_delta=${pp_delta}"
echo "threshold=${thr}"
if python3 - <<'PY'
import sys
d=float(sys.argv[1]); t=float(sys.argv[2])
sys.exit(0 if d<=t else 1)
PY
"$abs_delta" "$thr"
then
  echo "within threshold"
  exit 0
else
  if [[ "$fail" == "1" ]]; then
    echo "regression exceeds threshold"
    exit 1
  else
    echo "regression exceeds threshold (soft)"
    exit 0
  fi
fi
