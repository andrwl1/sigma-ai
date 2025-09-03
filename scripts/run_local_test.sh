#!/usr/bin/env bash
set -euo pipefail
TEST_ID="$1"
PROMPT="$2"
MODEL="${3:-llama3:8b}"
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
out_dir="artifacts/reports/${TEST_ID}"
mkdir -p "$out_dir"
req_file="$out_dir/request.txt"
res_file="$out_dir/response.txt"
meta_file="$out_dir/meta.json"

printf "%s\n" "$PROMPT" > "$req_file"

# Вызов локальной модели через ollama
resp="$(OLLAMA_NUM_CTX=2048 ollama run "$MODEL" <<<"$PROMPT" 2>&1 || true)"

printf "%s\n" "$resp" > "$res_file"

cat > "$meta_file" <<JSON
{
  "test": "$TEST_ID",
  "model": "$MODEL",
  "timestamp_utc": "$ts",
  "prompt_chars": ${#PROMPT},
  "response_chars": ${#resp}
}
JSON
echo "OK $TEST_ID -> $out_dir"
