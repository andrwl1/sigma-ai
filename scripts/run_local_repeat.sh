#!/usr/bin/env bash
set -euo pipefail
TEST_ID="${1:?TEST_ID required}"
MODEL="${2:-llama3:8b}"
N="${3:-5}"
MAP="artifacts/reports/test_prompts.json"
PROMPT="$(jq -r --arg t "$TEST_ID" '.[$t]' "$MAP")"
for i in $(seq 1 "$N"); do
  ./scripts/run_local_test.sh "${TEST_ID}_r${i}" "$PROMPT" "$MODEL"
done
