#!/usr/bin/env bash
set -euo pipefail
TS="$(date +%s)"
DST="artifacts/pack/${TS}"
mkdir -p "$DST"
find . -type f -name 'ab_diff.csv' -print -quit | xargs -I{} cp "{}" "$DST/ab_diff.csv"
find . -type f -name 'ab_plot.png' -print -quit | xargs -I{} cp "{}" "$DST/ab_plot.png" || true
find . -type f -name '*pass*.png' -print -quit | xargs -I{} cp "{}" "$DST/passrate.png" || true
find . -type f -name 'manifest.json' -print -quit | xargs -I{} cp "{}" "$DST/manifest.json"
test -s "$DST/ab_diff.csv" || exit 1
test -s "$DST/manifest.json" || exit 1
[ -f "$DST/ab_plot.png" ] || echo "warn: ab_plot.png missing"
[ -f "$DST/passrate.png" ] || echo "warn: passrate.png missing"
jq -e '.rows and .pass_rate and .delta_pp' "$DST/manifest.json" >/dev/null || true
echo "$DST"
