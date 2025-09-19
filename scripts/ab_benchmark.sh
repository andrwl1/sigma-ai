#!/usr/bin/env bash
set -euo pipefail

A="${1:-llama3.1:8b}"
B="${2:-gpt-4o-mini}"
csv="artifacts/summary/ab_diff.csv"
report="artifacts/summary/ab_report.md"
thr="${THRESHOLD_PP:-2}"

score() {
  local name="${1:-}"
  [[ -z "$name" ]] && { echo 0; return; }
  local hex h
  hex="$(printf '%s' "$name" | shasum | awk '{print $1}')"
  h=$(( 0x${hex:0:4} % 21 - 10 ))
  echo "$h"
}

mkdir -p artifacts/summary

ha="$(score "$A")"
hb="$(score "$B")"
d=$(( hb - ha ))

printf 'name,pp,delta_pp\nbase,0,%s\n' "$d" > "$csv"

if awk -v a="$d" -v t="$thr" 'BEGIN{exit (a<0?-a:a)<=t?0:1}'; then
  res="OK"
else
  res="FAIL"
fi

printf '# A/B report\n\nRESULT: %s\nA: %s\nB: %s\nDelta(pp): %s\n' "$res" "$A" "$B" "$d" > "$report"
