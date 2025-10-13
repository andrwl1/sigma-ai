# REPRO_T2000_VALIDATION

Дата проверки: 2025-10-12  
Фаза: **T2000 Reproducibility Validation**

---

## I. Цель
Проверить воспроизводимость baseline T2000 в независимом окружении и подтвердить совпадение метрик.

---

## II. Процедура
1. Инициализация окружения:
python -m venv .venv
source .venv/bin/activate
2. Установка пакета:
python -m pip install -e .
3. Запуск:
bash scripts/run_t2000.sh tests/t2000.tsv artifacts/repro_t2000 artifacts/repro_metrics_history.csv
4. Rollup и график:
bash scripts/run_t2000_rollup.sh artifacts/repro_t2000 artifacts/repro_metrics_history.csv artifacts/repro_trend_t2000.png

---

## III. Критерии совпадения
| Метрика         | Ожидаемое | Допуск | Статус |
|-----------------|-----------|--------|--------|
| pass_rate       | 1.00      | ±0.02  | ✅     |
| semantic_score  | 1.00      | ±0.02  | ✅     |

---

## IV. Итог
Репликация завершена: метрики совпадают с baseline T2000, расхождений не обнаружено.  
Система подтверждена как **воспроизводимая**.

**Validation OK.**

---
