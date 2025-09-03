#!/usr/bin/env bash
set -euo pipefail

TEST="${1:?usage: run_cloud_test.sh <TEST> <PROMPT> [MODEL]}"
PROMPT="${2:?usage: run_cloud_test.sh <TEST> <PROMPT> [MODEL]}"
MODEL="${3:-gpt-4o-mini}"

: "${OPENAI_API_KEY:?OPENAI_API_KEY is required}"

ts="$(date +%Y%m%d_%H%M%S)"
safe_model="${MODEL//[:\/ ]/_}"
out_raw="artifacts/cloud_runs/raw/${ts}_${safe_model}_${TEST}.txt"
out_meta="artifacts/cloud_runs/raw/${ts}_${safe_model}_${TEST}.meta"

# запуск и замер (Responses: chat.completions — стабильно совместим)
start_ns=$(date +%s%N)
resp="$(curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --arg m "$MODEL" --arg p "$PROMPT" \
        '{model:$m, temperature:0, messages:[{role:"user", content:$p}] }')" )"
end_ns=$(date +%s%N)

# извлечь ответ (первую строку) и метрики
answer="$(printf "%s" "$resp" | jq -r '.choices[0].message.content' | head -n1 | tr -d '\r')"
elapsed="$(awk -v s="$start_ns" -v e="$end_ns" 'BEGIN{printf "%.3f",(e-s)/1e9}')"

# сохранить raw
printf "%s\n" "$answer" | tee "$out_raw" >/dev/null
printf "elapsed=%s\n" "$elapsed" > "$out_meta"

# базовые счётчики
chars="$(wc -m < "$out_raw" | tr -d ' ')"
words="$(wc -w < "$out_raw" | tr -d ' ')"

# сводка
summary_file="summary/cloud_vs_local.md"
if [ ! -s "$summary_file" ]; then
  printf '| ts | side | model | test | elapsed(s) | answer | chars | words |\n|---|---|---|---:|---:|---|---:|---:|\n' > "$summary_file"
fi
printf '| %s | cloud | %s | %s | %s | %s | %s | %s |\n' "$ts" "$MODEL" "$TEST" "$elapsed" "$answer" "$chars" "$words" >> "$summary_file"

echo "OK: $out_raw"
echo "OK: $out_meta"
echo "OK: summary -> $summary_file"
