#!/usr/bin/env bash
set -euxo pipefail
input_dir="${1}"
history="${2}"
trend_png="${3:-artifacts/trend_drift_t3000.png}"

python -m sigma.eval.rollup \
  --metrics "${input_dir}/metrics.json" \
  --history "${history}" \
  --label "t3000_nightly"

[ -f "${history}" ]
[ -f "${trend_png}" ] || : 
