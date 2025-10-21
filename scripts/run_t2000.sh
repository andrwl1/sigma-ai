#!/usr/bin/env bash
set -euo pipefail
TESTS_FILE="${1:-tests/t2000.tsv}"
OUT_DIR="${2:-artifacts/t2000}"
HIST_FILE="${3:-artifacts/metrics_history.csv}"
mkdir -p "$OUT_DIR"
python3 -m sigma_ai.eval.run --tests "$TESTS_FILE" --out "$OUT_DIR/results.jsonl"
python3 -m sigma.eval.metrics --pred "$OUT_DIR/results.jsonl" --out "$OUT_DIR/metrics.json"
python3 -m sigma.eval.rollup --metrics "$OUT_DIR/metrics.json" --history "$HIST_FILE" --label "t2000_local"
