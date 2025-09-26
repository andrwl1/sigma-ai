#!/usr/bin/env bash
set -euo pipefail
ROOT="artifacts/cloud_runs"
KEEP="${KEEP_N:-14}"
mkdir -p "$ROOT"
mapfile -t runs < <(ls -1 "$ROOT" 2>/dev/null | sort)
cnt=${#runs[@]}
if [ "$cnt" -le "$KEEP" ]; then exit 0; fi
for r in "${runs[@]:0:cnt-KEEP}"; do
  tar -I 'zstd -19' -cf "$ROOT/${r}.tar.zst" -C "$ROOT" "$r"
  rm -rf "$ROOT/$r"
done
