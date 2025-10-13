#!/usr/bin/env bash
set -e
input_dir="$1"
history="$2"
trend="$3"
python -m sigma.eval.rollup \
  --metrics "$input_dir/metrics.json" \
  --history "$history" \
  --label "t2500_nightly" \
  --trend "$trend"
