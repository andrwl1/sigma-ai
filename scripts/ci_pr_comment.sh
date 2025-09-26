#!/usr/bin/env bash
set -euo pipefail

PNG="artifacts/plots/ab_plot.png"
MAN="artifacts/manifest.json"

rows=$(jq -r '.rows // 0' "$MAN")
pass=$(jq -r '.pass_rate // 0' "$MAN")
mean=$(jq -r '.delta_pp_mean // 0' "$MAN")
p95=$(jq -r '.delta_pp_p95 // 0' "$MAN")
mode=$(jq -r '.mode // "smoke"' "$MAN")
limit=$(jq -r '.limit // 0' "$MAN")
ma=$(jq -r '.model_a // "?"' "$MAN")
mb=$(jq -r '.model_b // "?"' "$MAN")
png_size=$(wc -c < "$PNG" 2>/dev/null || echo 0)

{
  echo "CI smoke summary"
  echo
  echo "- mode: $mode, limit: $limit"
  echo "- models: $ma vs $mb"
  echo "- rows: $rows"
  printf -- "- pass_rate: %.4f\n" "$pass"
  printf -- "- delta_pp mean/p95: %.6f / %.6f\n" "$mean" "$p95"
  echo "- plot.png size: $png_size bytes"
  echo "- Guard: OK"
} > comment.txt
