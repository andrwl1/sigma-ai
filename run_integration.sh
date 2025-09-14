#!/usr/bin/env bash
set -euo pipefail

echo "[Integration] Running T400 tests..."
pytest -q tests/integration --disable-warnings --maxfail=1
