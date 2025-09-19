#!/usr/bin/env bash
set -euo pipefail
MODEL_A="${1:-llama3.1:8b}"
MODEL_B="${2:-llama3.1:8b}"
LIMIT_VAL="${3:-30}"
TIMEOUT_S="${4:-90}"
mkdir -p logs artifacts/summary artifacts/plots
pkill -f "ab_benchmark.sh|run_cloud_test.sh|openai" || true
source scripts/set_openai_env.sh || true
export LIMIT="$LIMIT_VAL"
LOG="logs/ab_$(date +%Y%m%d_%H%M%S).log"
if ! gtimeout "${TIMEOUT_S}s" bash scripts/ab_benchmark.sh "$MODEL_A" "$MODEL_B" 2>&1 | tee "$LOG"; then
  echo "ab_benchmark: timeout/fail" | tee -a "$LOG"
  pkill -f "ab_benchmark.sh|run_cloud_test.sh|openai" || true
fi
bash scripts/guard.sh | tee -a "$LOG"
