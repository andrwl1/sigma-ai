#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
OUT="${2:-artifacts/manifest.json}"
mkdir -p "$(dirname "$OUT")"
[ -f "$OUT" ] || echo '{}' > "$OUT"

num_or_null() {
  awk 'BEGIN{v='"$1"'; if(v==v+0) print v; else print "null"}'
}

rows=""
if [ -f tests/prompts.tsv ]; then rows=$(awk 'NR>1{c++}END{print c+0}' tests/prompts.tsv); fi
if [ -z "${rows:-}" ] && [ -f artifacts/summary/stability.tsv ]; then rows=$(awk 'NR>1{c++}END{print c+0}' artifacts/summary/stability.tsv); fi

pass_rate=""
if [ -f artifacts/summary/stability.tsv ]; then
  read -r p f <<<"$(awk 'BEGIN{IGNORECASE=1}NR>1{if($0~/(^|[,\t ;])pass([,\t ;]|$)/)p++; else if($0~/(^|[,\t ;])fail([,\t ;]|$)/)f++}END{print p+0" "f+0}' artifacts/summary/stability.tsv)"
  tot=$((p+f))
  if [ "$tot" -gt 0 ]; then
    pass_rate=$(python - <<PY
p=$p; f=$f
print(round(p/float(p+f), 6))
PY
)
  fi
fi

delta_pp=""
if [ -f artifacts/summary/ab_diff.csv ]; then
  delta_pp=$(awk -F, 'NR==1{
    for(i=1;i<=NF;i++){gsub(/[[:space:]]/,"",$i);h[tolower($i)]=i}
  }
  NR==2{
    for(c in h) if(c ~ /^(delta_pp|delta|delta_pp_pct|delta_percent)$/){print $h[c]; exit}
  }' artifacts/summary/ab_diff.csv)
fi

jq \
  --argjson rows    "$( [ -n "${rows:-}" ] && printf '%s' "$rows" | num_or_null || echo null )" \
  --argjson pass    "$( [ -n "${pass_rate:-}" ] && printf '%s' "$pass_rate" | num_or_null || echo null )" \
  --argjson dpp     "$( [ -n "${delta_pp:-}" ] && printf '%s' "$delta_pp" | num_or_null || echo null )" \
  '
  . as $b
  | .rows       = (if $rows == null then (.rows       // .summary.rows       // .stats.rows       // null) else $rows end)
  | .pass_rate  = (if $pass == null then (.pass_rate  // .summary.pass_rate  // .metrics.pass_rate // null) else $pass end)
  | .delta_pp   = (if $dpp  == null then (.delta_pp   // .summary.delta_pp   // .metrics.delta_pp  // null) else $dpp  end)
  ' "$OUT" > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
echo "$OUT"
