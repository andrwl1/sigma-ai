#!/usr/bin/env bash
set -euo pipefail

IN_DIR="${1:-artifacts/t2000}"
HIST_FILE="${2:-artifacts/metrics_history.csv}"
OUT_PNG="${3:-artifacts/trend_drift_t2000.png}"

python3 -m sigma_ai.eval.rollup --metrics "$IN_DIR/metrics.json" --history "$HIST_FILE" --label "t2000_local"
python3 -m sigma.eval.trend --history "$HIST_FILE" --out "$OUT_PNG"
