# REPORT_T1000_FREEZE.md

## 1. Состояние системы
**Версия:** T1000-STABLE  
**Дата:** 2025-10-08  
**Commit:** 834bce5  
**Статус:** CI полностью зелёный (pre-ci, guard, nightly_t1000).  
**Guard threshold:** 0.70  
**Freeze-метка:** baseline зафиксирован, пайплайн стабилен.

---

## 2. Baseline
**Файл:** `tests/t1000.tsv`  
**Количество кейсов:** 12  
**Pass rate:** 0.4167  
**Delta_pp:** 0  
**Manifest:** `baseline_manifest.json`  
**Комментарий:** мини-корпус успешно прогнан, baseline-артефакты зафиксированы.

---

## 3. A/B-прогоны
| Модель | pass_rate | delta_pp |
|--------|------------|-----------|
| llama3.1:8b-local | 0.4167 | −23.33 |
| mistral-nemo-local | 0.4167 | −23.33 |
| q4o-mini-cloud | 0.4167 | −23.33 |

**Артефакты:**  
`artifacts/summary/ab_diff.csv`  
`artifacts/summary/passfail.png`  
`artifacts/summary/passrate.png`  
`artifacts/summary/T1000_Report_v1.md`

---

## 4. Метрики и история
- `verify_summary.txt` — `rows=12`, `ok=1`  
- `metrics_history.csv` — готов к накоплению истории  
- `passrate_local.png` — визуальный baseline  
- Следующий шаг — активировать `metrics_rollup.py` и тренд-чарт `passrate_trend.png`.

---

## 5. Вывод
T1000-этап завершён.  
CI-контур устойчив, baseline сформирован, отчёт зафиксирован.  
Проект переходит в фазу T1500 (расширение корпуса и тренд-мониторинг).
