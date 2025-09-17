#!/usr/bin/env bash
set -euo pipefail

CSV="artifacts/summary/ab_diff.csv"
PNG="artifacts/summary/passrate.png"

THRESHOLD_PP="${THRESHOLD_PP:-2}"
FAIL_ON_DIFF="${FAIL_ON_DIFF:-0}"

echo "THRESHOLD_PP=${THRESHOLD_PP} FAIL_ON_DIFF=${FAIL_ON_DIFF}"

test -s "$CSV" || { echo "CSV missing or empty: $CSV"; exit 2; }
if [[ -f "$PNG" ]]; then
  test -s "$PNG" || { echo "PNG is empty: $PNG"; exit 2; }
fi

max_delta=$(tail -n +2 "$CSV" | awk -F',' 'NF>=3 {d=$3+0; if(d<0)d=-d; if(d>m)m=d} END{if(m=="")m=0; print m}')
echo "max|delta_pp|=${max_delta}"

if [[ "$FAIL_ON_DIFF" == "1" ]] && awk -v a="$max_delta" -v t="$THRESHOLD_PP" 'BEGIN{exit !(a>t)}'
then
  echo "Threshold exceeded: ${max_delta} > ${THRESHOLD_PP}"
  exit 1
fi

echo "Guard OK"
exit 0
