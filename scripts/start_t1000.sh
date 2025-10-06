#!/usr/bin/env bash
set -euo pipefail
MODEL_A="${MODEL_A:-llama3.1:8b}"
MODEL_B="${MODEL_B:-llama3.1:8b}"
export MODE=t1000
export LIMIT=1000
if [ -x scripts/ab_benchmark.sh ]; then
  bash scripts/ab_benchmark.sh "$MODEL_A" "$MODEL_B" || true
fi
ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
sha="$(git rev-parse --short HEAD || echo na)"
cat > manifest.json <<EOF
{"run_id":"${GITHUB_RUN_ID:-local}","git_sha":"$sha","started_at":"$ts","duration_s":0,"suite":"t1000","models":["$MODEL_A","$MODEL_B"],"rows":0,"pass_rate":0,"delta_pp":0,"guard_ok":false}
EOF
touch ab_diff.csv ab_plot.png passfail.png
