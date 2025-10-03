#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-artifacts/nightly}"
KEEP="${2:-14}"
[ -d "$ROOT" ] || exit 0

# Оставляем последние KEEP директорий по mtime, остальное удаляем
mapfile -t DIRS < <(find "$ROOT" -mindepth 1 -maxdepth 1 -type d -printf '%T@ %p\n' \
  | sort -nr | awk '{print $2}')
COUNT=${#DIRS[@]}
if (( COUNT > KEEP )); then
  for d in "${DIRS[@]:KEEP}"; do rm -rf "$d"; done
fi
