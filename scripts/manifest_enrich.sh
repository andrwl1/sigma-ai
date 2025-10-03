#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
OUT="${2:-artifacts/manifest.json}"

json_in="{}"
[ -f "$OUT" ] && json_in="$(cat "$OUT")"

rows=""
if [ -f tests/prompts.tsv ]; then
  rows=$(awk 'NR>1{c++}END{print c+0}' tests/prompts.tsv)
elif [ -f artifacts/summary/stability.tsv ]; then
  rows=$(awk 'NR>1{c++}END{print c+0}' artifacts/summary/stability.tsv)
fi

pass_rate=""
if [ -f artifacts/summary/stability.tsv ]; then
  read -r p f <<<"$(awk 'BEGIN{IGNORECASE=1}NR>1{if($0~/(^|[,\t ])pass([,\t ]|$)/)p++; else if($0~/(^|[,\t ])fail([,\t ]|$)/)f++}END{print p+0" "f+0}' artifacts/summary/stability.tsv)"
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
      for(i=1;i<=NF;i++){gsub(/[[:space:]]/,"",$i);h[$i]=i}
    }
    NR==2{
      if("delta_pp" in h) print $h["delta_pp"];
      else if("delta" in h) print $h["delta"];
    }' artifacts/summary/ab_diff.csv)
fi

jq \
  --argjson base "$json_in" \
  --argjson rows    "$( [ -n "$rows" ] && echo "$rows" || echo null )" \
  --argjson pass    "$( [ -n "$pass_rate" ] && echo "$pass_rate" || echo null )" \
  --argjson dpp     "$( [ -n "$delta_pp" ] && echo "$delta_pp" || echo null )" \
  '
  ($base // {}) as $b
  | $b + {
      rows:    (if $rows==null then ($b.rows    // $b.summary.rows    // $b.stats.rows    // null) else $rows end),
      pass_rate:(if $pass==null then ($b.pass_rate// $b.summary.pass_rate// $b.metrics.pass_rate// null) else $pass end),
      delta_pp:(if $dpp==null then ($b.delta_pp // $b.summary.delta_pp // $b.metrics.delta_pp // null) else $dpp end)
    }
  ' <<< '{}' > "$OUT.tmp"

mv "$OUT.tmp" "$OUT"
echo "$OUT"
