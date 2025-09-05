#!/usr/bin/env bash
set -euo pipefail

python scripts/ab_report.py
python scripts/ab_diff.py
