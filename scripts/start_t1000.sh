#!/usr/bin/env bash
set -euo pipefail
SUITE="${1:-t1000}"
OUT_DIR="artifacts/${SUITE}/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT_DIR"
python3 scripts/run_ab.py "$SUITE"
cp artifacts/summary/ab_diff.csv "$OUT_DIR/ab_diff_local.csv"
cp artifacts/summary/passfail.png "$OUT_DIR/passfail_local.png"
cp artifacts/plots/ab_plot.png "$OUT_DIR/ab_plot_local.png"
cp artifacts/manifest.json "$OUT_DIR/manifest.json"
ln -sfn "$OUT_DIR" "artifacts/${SUITE}/latest"
