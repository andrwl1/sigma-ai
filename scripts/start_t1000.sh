#!/usr/bin/env bash
set -euo pipefail
: > ab_diff.csv
: > ab_plot.png
: > passfail.png
ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
sha="$(git rev-parse --short HEAD || echo na)"
printf '{"run_id":"%s","git_sha":"%s","started_at":"%s","duration_s":0,"suite":"t1000","models":["llama3.1:8b","llama3.1:8b"],"rows":0,"pass_rate":0,"delta_pp":0,"guard_ok":false}\n' "${GITHUB_RUN_ID:-local}" "$sha" "$ts" > manifest.json
