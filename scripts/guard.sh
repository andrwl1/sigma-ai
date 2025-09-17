#!/usr/bin/env bash
set -euo pipefail

# Пути можно переопределить переменными окружения
CSV_PATH="${CSV_PATH:-artifacts/summary/ab_diff.csv}"
PNG_PATH="${PNG_PATH:-}"                     # если пусто — авто-детект ниже
FAIL_ON_DIFF="${FAIL_ON_DIFF:-0}"

# Автодетект PNG (приоритет: passfail.png → любые в summary → любые в plots)
if [[ -z "$PNG_PATH" ]]; then
  for p in artifacts/summary/passfail.png artifacts/summary/*.png artifacts/plots/*.png; do
    [[ -f "$p" ]] && { PNG_PATH="$p"; break; }
  done
fi

### 1) Базовая проверка наличия
[[ -f "$CSV_PATH" ]] || { echo "ERR: CSV not found: $CSV_PATH" >&2; exit 1; }
[[ -n "$PNG_PATH" && -f "$PNG_PATH" ]] || { echo "ERR: PNG not found (searched summary/ and plots/). Set PNG_PATH explicitly." >&2; exit 1; }

### 2) CSV: не пустой и есть содержательные строки (не только заголовок)
CSV_LINES="$(wc -l < "$CSV_PATH" | tr -d ' ')"
if [[ "$CSV_LINES" -lt 2 ]]; then
  echo "ERR: CSV empty or header-only: $CSV_PATH (lines=$CSV_LINES)" >&2
  exit 1
fi
# Ищем любую непустую ячейку после заголовка; корректно возвращаем 0/1 в END
if ! awk -F',' '
  NR==1 { next }                    # пропускаем заголовок
  {
    for (i=1; i<=NF; i++) {
      gsub(/[[:space:]]+/, "", $i)
      if (length($i) > 0) { ok=1; break }
    }
    if (ok) { exit 0 }              # нашли данные → успех
  }
  END { exit (ok ? 0 : 1) }         # 0 если нашли, иначе 1
' "$CSV_PATH"; then
  echo "ERR: CSV has no data rows beyond header (all empty cells)." >&2
  exit 1
fi

### 3) PNG: размер >0 и корректная PNG-сигнатура
[[ -s "$PNG_PATH" ]] || { echo "ERR: PNG is zero bytes: $PNG_PATH" >&2; exit 1; }
# Проверка сигнатуры: 89 50 4E 47 0D 0A 1A 0A
if command -v hexdump >/dev/null 2>&1; then
  sig="$(hexdump -n 8 -v -e '8/1 "%02X"' "$PNG_PATH" 2>/dev/null || true)"
  if [[ "$sig" != "89504E470D0A1A0A" ]]; then
    echo "ERR: PNG signature invalid (got $sig) for $PNG_PATH" >&2
    exit 1
  fi
fi

### 4) Строгий режим по дельтам (если включён)
if [[ "$FAIL_ON_DIFF" == "1" ]]; then
  if awk -F',' '
    NR==1 { next }
    {
      for (i=1; i<=NF; i++)
        if ($i ~ /^-?[0-9]+(\.[0-9]+)?$/ && ($i+0)!=0) { exit 0 }
    }
    END { exit 1 }
  ' "$CSV_PATH"
  then
    echo "DIFF: non-zero deltas detected -> fail"
    exit 1
  else
    echo "DIFF: all numeric deltas are zero"
  fi
else
  echo "SOFT: diff check skipped (FAIL_ON_DIFF=0)"
fi

echo "OK: artifacts validated (CSV=$CSV_PATH, PNG=$PNG_PATH)"
