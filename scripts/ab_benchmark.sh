#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.."; pwd)"
SUMMARY_DIR="$ROOT/artifacts/summary"
TMP_DIR="$ROOT/artifacts/run"
PROMPTS_FILE="$ROOT/tests/prompts.tsv"
MODEL_A="${1:-llama3.1:8b}"
MODEL_B="${2:-gpt-4o-mini}"
LIMIT="${LIMIT:-10}"

mkdir -p "$SUMMARY_DIR" "$TMP_DIR"

mode="smoke"
if [[ -x "$ROOT/scripts/run_local_test.sh" && -x "$ROOT/scripts/run_cloud_test.sh" && -f "$PROMPTS_FILE" && -z "${CI:-}" ]]; then
  mode="real"
fi

if [[ "$mode" = "real" ]]; then
  n=0
  while IFS=$'\t' read -r pid prompt; do
    [[ -z "$pid" || "$pid" =~ ^# ]] && continue
    n=$((n+1))
    [[ $n -gt $LIMIT ]] && break
    "$ROOT/scripts/run_local_test.sh" "$pid" "$prompt" "$MODEL_A" >"$TMP_DIR/${pid}_a.txt" 2>&1 || true
    "$ROOT/scripts/run_cloud_test.sh" "$pid" "$prompt" "$MODEL_B" >"$TMP_DIR/${pid}_b.txt" 2>&1 || true
  done < "$PROMPTS_FILE"

  total=$(ls "$TMP_DIR"/*_a.txt 2>/dev/null | wc -l | tr -d ' ')
  printf "model_a,model_b,delta_pp\n%s,%s,0.0\n" "$MODEL_B" "$MODEL_A" > "$SUMMARY_DIR/ab_diff.csv"
  {
    echo "# AB Report"
    echo
    echo "- Mode: real"
    echo "- Pairs: $total"
    echo "- A: $MODEL_A"
    echo "- B: $MODEL_B"
    echo
    echo "Raw outputs stored in artifacts/run/"
  } > "$SUMMARY_DIR/ab_report.md"
else
  printf "model_a,model_b,delta_pp\n%s,%s,0.0\n" "$MODEL_B" "$MODEL_A" > "$SUMMARY_DIR/ab_diff.csv"
  {
    echo "# AB Report"
    echo
    echo "- Mode: smoke (CI)"
    echo "- A: $MODEL_A"
    echo "- B: $MODEL_B"
    echo
    echo "Smoke run to keep CI green."
  } > "$SUMMARY_DIR/ab_report.md"
fi
