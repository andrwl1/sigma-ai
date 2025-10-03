#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
OUT="${2:-artifacts/manifest.json}"
mkdir -p "$(dirname "$OUT")"

rows=0
if [ -f tests/prompts.tsv ]; then
  rows=$(awk 'END{print NR}' tests/prompts.tsv)
fi

pass_rate=0
if [ -f artifacts/summary/stability.tsv ]; then
  total=$(awk 'NR>1{t+=$2+$3}END{print t+0}' artifacts/summary/stability.tsv)
  passed=$(awk 'NR>1{p+=$2}END{print p+0}' artifacts/summary/stability.tsv)
  if [ "$total" -gt 0 ]; then
    pass_rate=$(python3 - <<PY
print(round($passed/float($total)*100, 2))
PY
)
  fi
fi

delta_pp=0
if [ -f artifacts/summary/ab_diff.csv ]; then
  delta_pp=$(awk -F, 'NR==1{for(i=1;i<=NF;i++){h[$i]=i}}NR==2{print $(h["delta_pp"])+0}' artifacts/summary/ab_diff.csv 2>/dev/null || echo 0)
fi

jq -n \
  --argjson r "$rows" \
  --argjson p "$pass_rate" \
  --argjson d "$delta_pp" \
  '{rows:$r, pass_rate:$p, delta_pp:$d}' > "$OUT"

echo "✅ manifest_enrich.sh → $OUT"
