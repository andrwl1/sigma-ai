#!/usr/bin/env bash
set -euo pipefail
MODEL="${1:-llama3:8b}"
MAP="artifacts/reports/test_prompts.json"
echo "Model: $MODEL"
for t in $(jq -r 'keys[]' "$MAP" | sort -V); do
  p="$(jq -r --arg t "$t" '.[$t]' "$MAP")"
  ./scripts/run_local_test.sh "$t" "$p" "$MODEL"
done
