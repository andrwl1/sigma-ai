#!/usr/bin/env bash
set -euo pipefail
# Порядок аргументов: ID, PROMPT, MODEL
ID="${1:-}"; PROMPT="${2:-}"; MODEL="${3:-llama3.1:8b}"
[ -z "$ID" ] && { echo "usage: run_local_answer.sh <ID> <PROMPT> [MODEL]"; exit 2; }

# Запускаем исходный скрипт
bash scripts/run_local_test.sh "$ID" "$PROMPT" "$MODEL" || true

# Печатаем самый свежий текстовый артефакт
CANDIDATES=$(ls -t artifacts/**/* 2>/dev/null | head -n 20 || true)
printed=0
for f in $CANDIDATES; do
  # только текстовые/markdown/csv
  if file "$f" | grep -Eqi 'text|utf-8|csv|markdown'; then
    echo "---- $(basename "$f") ----"
    tail -n 200 "$f"
    printed=1
    break
  fi
done

# Если ничего не нашли — скажем явно
if [ "$printed" -eq 0 ]; then
  echo "no textual artifacts found under artifacts/"
  exit 3
fi
