#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts/local artifacts/reports artifacts/summary artifacts/plots
bash scripts/run_local_suite.sh
LIMIT=${LIMIT:-30} python3 scripts/judge_basics.py --reports-dir artifacts/reports --out artifacts/local/judgement.tsv
LIMIT=${LIMIT:-30} bash scripts/build_report.sh
