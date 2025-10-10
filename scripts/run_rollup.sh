#!/usr/bin/env bash
set -euo pipefail
python3 -m src.metrics.rollup --history metrics_history.csv --outdir artifacts
