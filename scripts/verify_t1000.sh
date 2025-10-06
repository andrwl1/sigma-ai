#!/usr/bin/env bash
set -euo pipefail
ok=1
for f in manifest.json ab_diff.csv ab_plot.png passfail.png; do
  [ -f "$f" ] || ok=0
done
rows=$(python - <<'PY'
import json,sys
try:
  d=json.load(open("manifest.json"))
  print(d.get("rows",0))
except Exception:
  print(0)
PY
)
pass_rate=$(python - <<'PY'
import json,sys
try:
  d=json.load(open("manifest.json"))
  print(d.get("pass_rate",0))
except Exception:
  print(0)
PY
)
delta_pp=$(python - <<'PY'
import json,sys
try:
  d=json.load(open("manifest.json"))
  print(d.get("delta_pp",0))
except Exception:
  print(0)
PY
)
echo "rows=${rows}, pass_rate=${pass_rate}, delta_pp=${delta_pp}, ok=${ok}" > verify_summary.txt
[ "$ok" = "1" ] && echo "OK" || { echo "FAIL"; exit 1; }
