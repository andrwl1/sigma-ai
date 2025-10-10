#!/usr/bin/env bash
set -euo pipefail
python3 -m src.metrics.evaluate --tsv "$1" --outdir "$2" --history "$3" --run-id "nightly-$(date +%s)"
