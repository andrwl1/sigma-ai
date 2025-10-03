#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-artifacts/nightly}"
KEEP="${2:-14}"
[ -d "$ROOT" ] || exit 0

# Самые новые сначала
DIRS=$(LC_ALL=C ls -1dt "$ROOT"/*/ 2>/dev/null || true)
[ -n "$DIRS" ] || exit 0

i=1
# shellcheck disable=SC2086
for d in $DIRS; do
  if [ $i -gt "$KEEP" ]; then
    rm -rf "$d"
  fi
  i=$((i+1))
done
