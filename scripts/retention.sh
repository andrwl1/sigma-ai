#!/usr/bin/env bash
set -euo pipefail
DIR=${1:-artifacts/nightly}
KEEP=${2:-14}
runs=( $(ls -1dt "$DIR"/run-* 2>/dev/null || true) )
total=${#runs[@]}
if [ "$total" -le "$KEEP" ]; then exit 0; fi
for ((i=KEEP; i<total; i++)); do rm -rf "${runs[$i]}"; done
