#!/usr/bin/env bash
set -e
input_dir="$1"
history="$2"

python -m sigma.eval.rollup \
  --metrics "$input_dir/metrics.json" \
  --history "$history" \
  --label "t3000_nightly"
