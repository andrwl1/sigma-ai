#!/usr/bin/env bash
set -euo pipefail
TS="$(date +%s)"
DST="artifacts/cloud_runs/${TS}"
mkdir -p "$DST"
rsync -a artifacts/ "$DST"/
echo "$DST"
