#!/usr/bin/env bash
set -euo pipefail
ts="$(date +%Y%m%d_%H%M%S)"
out="artifacts/reports/env_${ts}.md"
{
  echo "# Env snapshot $ts"
  echo "## System"; uname -a
  echo "## macOS";  sw_vers || true
  echo "## CPU";    sysctl -n machdep.cpu.brand_string || true
  echo "## Ollama"; ollama --version || true
  echo "## Models"; curl -s http://127.0.0.1:11434/api/tags || ollama list || true
} > "$out"
echo "OK -> $out"
