#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN="${VIRTUAL_ENV:+$VIRTUAL_ENV/bin/python}"
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3)}"
export PYTHONPATH="$(pwd):${PYTHONPATH:-}"
TESTS_FILE="${1:-tests/t2500.tsv}"
OUT_DIR="${2:-artifacts/t2500}"
HIST_FILE="${3:-artifacts/metrics_history.csv}"
mkdir -p "$OUT_DIR"
"$PYTHON_BIN" -m sigma_ai.cli --tests "$TESTS_FILE" --out "$OUT_DIR/results.jsonl"
had_err=$?
if [ $had_err -ne 0 ]; then exit $had_err; fi
"$PYTHON_BIN" -m sigma.eval.metrics --pred "$OUT_DIR/results.jsonl" --out "$OUT_DIR/metrics.json"
"$PYTHON_BIN" -m sigma.eval.rollup --metrics "$OUT_DIR/metrics.json" --history "$HIST_FILE" --label "t2500_local"
