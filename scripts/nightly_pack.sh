#!/usr/bin/env bash
set -euo pipefail

DATE=$(date +%F)
RUN_ID=${RUN_ID:-$(gh run list --workflow="nightly.yml" --limit 1 --json databaseId --jq '.[0].databaseId' 2>/dev/null || echo local)}
DST="artifacts/nightly/${DATE}"
mkdir -p "$DST"

AB_SRC=$(find . -type f -name 'ab_diff.csv' -print -quit)
PLOT_SRC=$(find . -type f -name 'ab_plot.png' -print -quit || true)
PASS_SRC=$(find . -type f -name '*pass*.png' -print -quit || true)

cp "$AB_SRC" "$DST/ab_diff_${RUN_ID}.csv"
[ -n "${PLOT_SRC:-}" ] && cp "$PLOT_SRC" "$DST/ab_plot_${RUN_ID}.png" || echo "warn: ab_plot.png missing" >&2
[ -n "${PASS_SRC:-}" ] && cp "$PASS_SRC" "$DST/passrate_${RUN_ID}.png" || echo "warn: passrate.png missing" >&2

bash scripts/manifest_enrich.sh . "$DST/manifest_${RUN_ID}.json"
echo "manifest_enrich.sh -> $DST/manifest_${RUN_ID}.json" >&2

test -s "$DST/ab_diff_${RUN_ID}.csv"
test -s "$DST/manifest_${RUN_ID}.json"

jq -e 'has("rows") and has("pass_rate") and has("delta_pp")
       and (.rows|type=="number")
       and (.pass_rate|type=="number")
       and (.delta_pp|type=="number")' "$DST/manifest_${RUN_ID}.json" >/dev/null

echo "$DST"
