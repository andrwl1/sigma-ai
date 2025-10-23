#!/usr/bin/env bash
set -e
input_dir="$1"
history="$2"

python -m sigma_ai.eval.rollup \
  --metrics "$input_dir/metrics.json" \
  --history "$history" \
  --label "t2500_nightly"
