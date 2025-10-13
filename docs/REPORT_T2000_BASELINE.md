# REPORT_T2000_BASELINE

Дата: 2025-10-12  
Фаза: **T2000 Baseline Results**

---

## I. Итог
Baseline T2000 сформирован и подтверждён. Метрики стабильны, дрейф не наблюдается.

| Метрика         | Значение | Порог/допуск | Статус |
|-----------------|----------|--------------|--------|
| pass_rate       | 1.00     | ≥ 0.70       | ✅     |
| semantic_score  | 1.00     | ±0.02        | ✅     |

---

## II. Артефакты
- `artifacts/t2000/results.jsonl`
- `artifacts/t2000/metrics.json`
- `artifacts/metrics_history.csv`
- `artifacts/trend_drift_t2000.png`

---

## III. Ссылки
- Nightly T2000: `.github/workflows/nightly_t2000.yml`
- Nightly T2000 Rollup: `.github/workflows/nightly_t2000_rollup.yml`
- Freeze: `docs/REPORT_T2000_FREEZE.md`
- Validation: `docs/REPRO_T2000_VALIDATION.md`
