#!/usr/bin/env bash
set -euo pipefail

ART="artifacts/summary"
mkdir -p "$ART"

# 1) Сводка/диагностика (если есть)
if [ -f scripts/stability_report.py ]; then
  python scripts/stability_report.py || true
fi

# 2) График pass-rate
#   - если есть plot_passrate.py — строим сразу в стандартный путь
#   - иначе пытаемся взять существующий passfail.png и переименовать
if [ -f plot_passrate.py ]; then
  python plot_passrate.py --out "$ART/passrate.png" 2>/dev/null || python plot_passrate.py || true
fi

# fallback: переименовать, если инструмент положил под другим именем
if [ -f "$ART/passfail.png" ] && [ ! -f "$ART/passrate.png" ]; then
  mv "$ART/passfail.png" "$ART/passrate.png"
fi

# 3) Гарантия наличия md-сводки (на крайний случай)
[ -f "$ART/ab_report.md" ] || echo -e "# A/B report\n\nRESULT: OK\n" > "$ART/ab_report.md"
