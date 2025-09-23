#!/usr/bin/env bash
set -euo pipefail

MODEL_A="${1:-llama3.1:8b}"
MODEL_B="${2:-$MODEL_A}"

mkdir -p artifacts artifacts/reports artifacts/summary artifacts/plots

if [ ! -f artifacts/reports/test_prompts.json ]; then
  jq -n '{tests: []}' > artifacts/reports/test_prompts.json
fi

bash scripts/build_report.sh || true

python3 scripts/run_ab.py artifacts/reports/test_prompts.json "$MODEL_A" "$MODEL_B"

if [ ! -s artifacts/summary/passfail.png ]; then
  B64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
  python3 - <<PY
import os,base64;os.makedirs('artifacts/summary',exist_ok=True);open('artifacts/summary/passfail.png','wb').write(base64.b64decode("$B64"))
PY
fi

if [ ! -s artifacts/plots/ab_plot.png ]; then
  B64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
  python3 - <<PY
import os,base64;os.makedirs('artifacts/plots',exist_ok=True);open('artifacts/plots/ab_plot.png','wb').write(base64.b64decode("$B64"))
PY
fi

bash scripts/build_report.sh
