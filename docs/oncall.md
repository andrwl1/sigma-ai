# Oncall Guide

## When CI fails
1. Check guard_regress.log
2. If header or NaN error → fix dataset
3. If min rows failed → rerun with larger corpus

## When Nightly fails
1. Check artifacts/cloud_runs/<ts>/
2. Verify ab_diff.csv ≥ 500
3. Check manifest.json for delta_pp_mean and delta_pp_p95

## Common issues
- Missing script → check git add/commit/push
- Disk space → retention.sh
- API errors → rerun workflow with ref
