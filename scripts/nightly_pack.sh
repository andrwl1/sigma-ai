#!/usr/bin/env bash
set -euo pipefail

TS="$(date +%s)"
DST="artifacts/pack/${TS}"
mkdir -p "$DST"

find . -type f -name 'ab_diff.csv' -print -quit | xargs -I{} cp "{}" "$DST/ab_diff.csv"
find . -type f -name 'ab_plot.png' -print -quit | xargs -I{} cp "{}" "$DST/ab_plot.png"
find . -type f -name '*pass*.png' -print -quit | xargs -I{} cp "{}" "$DST/pass.png"
find . -type f -name 'manifest.json' -print -quit | xargs -I{} cp "{}" "$DST/manifest.json"

test -s "$DST/ab_diff.csv"
test -f "$DST/ab_plot.png"
test -f "$DST/pass.png"
jq -e '.rows and .pass_rate and .delta_pp' "$DST/manifest.json" >/dev/null

echo "$DST"
