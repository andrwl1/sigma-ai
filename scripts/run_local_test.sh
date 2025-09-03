#!/usr/bin/env bash
set -euo pipefail

TEST="${1:?usage: run_local_test.sh <TEST> <PROMPT> [MODEL]}"
PROMPT="${2:?usage: run_local_test.sh <TEST> <PROMPT> [MODEL]}"
MODEL="${3:-llama3:8b}"

ts="$(date +%Y%m%d_%H%M%S)"
safe_model="${MODEL//[:\/ ]/_}"
out_raw="artifacts/local_runs/raw/${ts}_${safe_model}_${TEST}.txt"
out_meta="artifacts/local_runs/raw/${ts}_${safe_model}_${TEST}.meta"

# запуск и замер
{ time -p bash -lc "printf %s \"$PROMPT\" | ollama run \"$MODEL\"" | tee "$out_raw"; } 2>"$out_meta"

# простые метрики
answer="$(head -n1 "$out_raw" | tr -d '\r')"
elapsed="$(awk '/^real/ {print $2}' "$out_meta")"
chars="$(wc -m < "$out_raw" | tr -d ' ')"
words="$(wc -w < "$out_raw" | tr -d ' ')"

# сводка
summary_file="summary/cloud_vs_local.md"
if [ ! -s "$summary_file" ]; then
  printf '| ts | side | model | test | elapsed(s) | answer | chars | words |\n|---|---|---|---:|---:|---|---:|---:|\n' > "$summary_file"
fi
printf '| %s | local | %s | %s | %s | %s | %s | %s |\n' "$ts" "$MODEL" "$TEST" "${elapsed:-NA}" "$answer" "$chars" "$words" >> "$summary_file"

echo "OK: $out_raw"
echo "OK: $out_meta"
echo "OK: summary -> $summary_file"
