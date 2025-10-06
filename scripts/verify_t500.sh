#!/usr/bin/env bash
set -euo pipefail
DATE="${1:-$(date +%F)}"
ROOT="artifacts/nightly/$DATE"

err(){ echo "❌ $*" >&2; exit 1; }
ok(){ echo "✅ $*"; }

[ -d "$ROOT" ] || err "нет каталога $ROOT"

CSV=$(ls -1t "$ROOT"/ab_diff_*.csv 2>/dev/null | head -n1 || true)
PLOT=$(ls -1t "$ROOT"/ab_plot_*.png 2>/dev/null | head -n1 || true)
PASS=$(ls -1t "$ROOT"/pass_*.png "$ROOT"/passrate_*.png 2>/dev/null | head -n1 || true)
JSON=$(ls -1t "$ROOT"/manifest_*.json 2>/dev/null | head -n1 || true)

[ -n "${CSV:-}" ]  || err "не найден ab_diff_*.csv"
[ -f "$CSV" ]      || err "CSV отсутствует: $CSV"
rows=$(awk 'NR>1 {c++} END{print c+0}' "$CSV")
[ "$rows" -ge 1 ]  || err "CSV пустой: $CSV"
ok "CSV ок: $CSV (rows=$rows)"

check_png(){ local f="$1"; [ -f "$f" ] || return 1
  if command -v sips >/dev/null 2>&1; then sips -g pixelWidth -g pixelHeight "$f" >/dev/null 2>&1 || return 1
  else file "$f" | grep -qi 'PNG image data' || return 1; fi; }

if [ -n "${PLOT:-}" ] && check_png "$PLOT"; then ok "PNG ок: $PLOT"; else echo "⚠️  нет/битый ab_plot PNG: ${PLOT:-<none>}"; fi
if [ -n "${PASS:-}" ] && check_png "$PASS"; then ok "PNG ок: $PASS"; else echo "⚠️  нет/битый pass PNG: ${PASS:-<none>}"; fi

r_val=""; p_val=""; d_val=""
if [ -n "${JSON:-}" ] && [ -f "$JSON" ]; then
  r_val=$(jq -r '(.rows // .summary.rows // .stats.rows // .metrics.rows // empty)' "$JSON")
  p_val=$(jq -r '(.pass_rate // .summary.pass_rate // .metrics.pass_rate // (.passes/((.passes//0)+(.fails//0)+1e-9)) // empty)' "$JSON")
  d_val=$(jq -r '(.delta_pp // .summary.delta_pp // .metrics.delta_pp // empty)' "$JSON")
  if [ -n "$r_val" ] && [ -n "$p_val" ] && [ -n "$d_val" ] && \
     jq -e '((.rows // .summary.rows // .stats.rows // .metrics.rows | type=="number") and
             (.pass_rate // .summary.pass_rate // .metrics.pass_rate | type=="number") and
             (.delta_pp // .summary.delta_pp // .metrics.delta_pp | type=="number"))' "$JSON" >/dev/null 2>&1; then
    ok "JSON ок: $JSON (rows=$r_val, pass_rate=$p_val, delta_pp=$d_val)"
  else
    echo "⚠️  метрики в $JSON не найдены/нечисловые; продолжаю без них"
  fi
else
  echo "⚠️  manifest не найден"
fi

{
  echo "date=$DATE"
  echo "csv=$CSV (rows=$rows)"
  echo "plot=${PLOT:-<none>}"
  echo "pass=${PASS:-<none>}"
  if [ -n "${JSON:-}" ]; then
    echo "manifest=$JSON (rows=${r_val:-na}, pass_rate=${p_val:-na}, delta_pp=${d_val:-na})"
  else
    echo "manifest=<none>"
  fi
} > "$ROOT/verify_summary.txt"

ok "Сводка → $ROOT/verify_summary.txt"
