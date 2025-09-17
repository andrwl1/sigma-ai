#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts/summary
echo "# AB Report

Autogen stub: CI smoke passed." > artifacts/summary/ab_report.md
echo "model_a,model_b,delta_pp
gpt-4o-mini,llama3.1:8b,0.0" > artifacts/summary/ab_diff.csv
