#!/usr/bin/env bash
set -euo pipefail
J=${1:-manifest.json}
RID=${GITHUB_RUN_ID:-}
REPO=${GITHUB_REPOSITORY:-}
RUN_URL="https://github.com/${REPO}/actions/runs/${RID}"
rows=$(jq -r '.rows' "$J")
pass_rate=$(jq -r '.pass_rate' "$J")
delta=$(jq -r '.delta_pp // .delta_pp_mean // .delta_pp_p95' "$J")
model_a=$(jq -r '.model_a' "$J")
model_b=$(jq -r '.model_b' "$J")
limit=$(jq -r '.limit' "$J")
branch=$(jq -r '.branch' "$J")
printf "Nightly T500 ✅\nbranch: %s\nmodels: %s vs %s\nlimit: %s\nrows: %s\npass_rate: %s\ndelta_pp: %s\nrun: %s\n" "$branch" "$model_a" "$model_b" "$limit" "$rows" "$pass_rate" "$delta" "$RUN_URL"
