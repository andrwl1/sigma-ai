#!/usr/bin/env bash
set -euo pipefail
[ -f scripts/set_openai_env.sh ] && source scripts/set_openai_env.sh
bash scripts/ab_benchmark.sh llama3.1:8b gpt-4o-mini
[ -f artifacts/summary/ab_report.md ] && { echo; echo "====== A/B REPORT ======"; cat artifacts/summary/ab_report.md; }
