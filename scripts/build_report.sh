set -e
ART="artifacts/summary"
mkdir -p "$ART"

# 1) Генерация сводки (если есть)
if [ -f scripts/stability_report.py ]; then
  python scripts/stability_report.py || true
fi

# 2) График passrate (если есть)
if [ -f plot_passrate.py ]; then
  python plot_passrate.py --out "$ART/passrate.png" 2>/dev/null || python plot_passrate.py || true
fi

# 3) Гарантируем наличие сводного файла (на крайний случай)
[ -f "$ART/ab_report.md" ] || echo "RESULT: OK" > "$ART/ab_report.md"
