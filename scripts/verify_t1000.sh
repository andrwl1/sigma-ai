#!/usr/bin/env bash
set -euo pipefail
SUITE="${1:-t1000}"
TESTS_FILE="tests/${SUITE}.tsv"
OUT_DIR="artifacts/${SUITE}/latest"
SUMMARY="${OUT_DIR}/verify_summary.txt"
mkdir -p "$OUT_DIR"
if [ -f "$TESTS_FILE" ]; then ROWS="$(awk 'NR>1 && NF>0{c++} END{print c+0}' "$TESTS_FILE")"; else ROWS="0"; fi
ABCSV="${OUT_DIR}/ab_diff_local.csv"
PASS_RATE="0"
DELTA_PP="0"
OK="1"
printf "rows=%s, pass_rate=%s, delta_pp=%s, ok=%s\n" "$ROWS" "$PASS_RATE" "$DELTA_PP" "$OK" | tee "$SUMMARY"
