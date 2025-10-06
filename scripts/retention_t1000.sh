#!/usr/bin/env bash
set -euo pipefail
find artifacts/t1000 2>/dev/null | head -n 1 >/dev/null || exit 0
find artifacts/t1000 -type f -mtime +14 -delete || true
