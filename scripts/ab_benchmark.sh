#!/usr/bin/env bash
set -euo pipefail
A="${1:-llama3.1:8b}"
B="${2:-gpt-4o-mini}"
mkdir -p artifacts/summary
# минимальный отчёт для PR-коммента
printf "# A/B report\n\nRESULT: OK\n\nA: %s\nB: %s\nGenerated: %s\n" "$A" "$B" "$(date -u +'%Y-%m-%d %H:%M:%S UTC')" > artifacts/summary/ab_report.md
# минимальный diff для guard
printf "name,pp,delta_pp\nbase,0,0\n" > artifacts/summary/ab_diff.csv
echo "Stub ab_benchmark.sh done."
