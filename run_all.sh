#!/usr/bin/env bash
set -euo pipefail

# всегда запускаем из корня проекта
cd "$(dirname "$0")"

# активируем venv (если не активирован)
source .venv/bin/activate

# основной конвейер проекта
./scripts/daily.sh
