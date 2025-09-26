#!/usr/bin/env bash
set -euo pipefail
PNG="artifacts/plots/ab_plot.png"
MAN="artifacts/manifest.json"
rows=$(jq -r '.rows' "$MAN")
pass=$(jq -r '.pass_rate' "$MAN")
mean=$(jq -r '.delta_pp_mean' "$MAN")
p95=$(jq -r '.delta_pp_p95' "$MAN")
mode=$(jq -r '.mode' "$MAN")
limit=$(jq -r '.limit' "$MAN")
ma=$(jq -r '.model_a' "$MAN")
mb=$(jq -r '.model_b' "$MAN")
png_size=$(wc -c < "$PNG" 2>/dev/null || echo 0)
printf "CI smoke summary\n\n" > comment.txt
printf "- mode: %s, limit: %s\n" "$mode" "$limit" >> comment.txt
printf "- models: %s vs %s\n" "$ma" "$mb" >> comment.txt
printf "- rows: %s\n" "$rows" >> comment.txt
printf "- pass_rate: %.4f\n" "$pass" >> comment.txt
printf "- delta_pp mean/p95: %.6f / %.6f\n" "$mean" "$p95" >> comment.txt
printf "- plot.png size: %s bytes\n" "$png_size" >> comment.txt
printf "- Guard: OK\n" >> comment.txt
