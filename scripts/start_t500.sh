#!/usr/bin/env bash
set -euo pipefail
RUNS=${1:-3}
DATE=$(date +%F)
mkdir -p "artifacts/nightly/$DATE"

latest_id() {
  gh run list --workflow="nightly.yml" --limit 1 --json databaseId --jq '.[0].databaseId' 2>/dev/null || true
}

trigger_and_wait() {
  local before after
  before=$(latest_id || true)
  gh workflow run nightly.yml --ref master >/dev/null
  for _ in $(seq 1 120); do
    after=$(latest_id || true)
    if [ -n "${after:-}" ] && [ "$after" != "${before:-}" ]; then
      gh run watch "$after" --exit-status
      echo "$after"
      return 0
    fi
    sleep 2
  done
  echo "timeout" >&2
  exit 1
}

i=1
while [ $i -le $RUNS ]; do
  RUN_ID=$(trigger_and_wait)
  RUN_DIR="artifacts/nightly/$DATE/run_$RUN_ID"
  mkdir -p "$RUN_DIR"
  gh run download "$RUN_ID" --dir "$RUN_DIR"

  AB=$(find "$RUN_DIR" -type f -name 'ab_diff.csv' -print -quit)
  PLOT=$(find "$RUN_DIR" -type f -name 'ab_plot.png' -print -quit)
  PASS=$(find "$RUN_DIR" -type f -name '*pass*.png' -print -quit)
  JSON=$(find "$RUN_DIR" -type f -name 'manifest.json' -print -quit)

  test -s "$AB"
  test -f "$PLOT"
  test -f "$PASS"
  jq -e '.rows and .pass_rate and .delta_pp' "$JSON" >/dev/null

  cp "$AB"   "artifacts/nightly/$DATE/ab_diff_${RUN_ID}.csv"
  cp "$PLOT" "artifacts/nightly/$DATE/ab_plot_${RUN_ID}.png"
  cp "$PASS" "artifacts/nightly/$DATE/pass_${RUN_ID}.png"
  cp "$JSON" "artifacts/nightly/$DATE/manifest_${RUN_ID}.json"

  i=$((i+1))
done

tar -C "artifacts/nightly/$DATE" -czf "artifacts/nightly/summary_snapshot_$DATE.tar.gz" .
bash scripts/retention.sh
gh run list --workflow="nightly.yml" --limit 3 --json status,conclusion,displayTitle --jq '.[]|.status+" "+.conclusion+" "+.displayTitle'
