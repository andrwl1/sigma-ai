#!/usr/bin/env bash
set -euo pipefail

.venv/bin/python src/ingest_logs.py || true
.venv/bin/python src/plot_logs.py
.venv/bin/python src/metrics.py
.venv/bin/python src/report.py
.venv/bin/python src/export_bundle.py
.venv/bin/python src/mark_day.py

today=$(date +"%Y-%m-%d")
mkdir -p archive/proofs/$today
cp reports/metrics.json archive/proofs/$today/ 2>/dev/null || true
cp reports/README.md  archive/proofs/$today/ 2>/dev/null || true
cp reports/plots/loss.png archive/proofs/$today/ 2>/dev/null || true
lb=$(ls -t bundle/bundle_*.zip 2>/dev/null | head -n 1 || true)
bn=""
if [ -n "${lb:-}" ]; then cp "$lb" archive/proofs/$today/ || true; bn=$(basename "$lb"); fi
cat > archive/proofs/$today/log.txt <<EOF
DATE: $today
STEP: Auto archival
DETAILS:
- metrics.json
- README.md
- loss.png
- $bn
STATUS: COMPLETE
EOF

.venv/bin/python src/log_history.py
echo "✅ daily: done"

tl_status=$(tail -n 1 archive/TIMELINE.md | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/,"",$2); print $2}')
hist_status=$(tail -n 1 reports/history.csv | awk -F',' '{print $2}')
if [ "$tl_status" != "$hist_status" ]; then
  echo "✗ Status mismatch: timeline=$tl_status history=$hist_status"
  exit 2
else
  echo "✓ Status synced ($tl_status)"
fi
