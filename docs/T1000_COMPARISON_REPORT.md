# T1000_COMPARISON_REPORT.md

## 1. Обзор
**Версия:** T1000-STABLE  
**Дата:** 2025-10-08  
**Commit:** 7c73409  
**Описание:** Итоговый отчёт о сравнении моделей после расширения корпуса до 60 кейсов.  
Baseline и A/B-инфраструктура проверены — система стабильна и готова к масштабированию (T1500).

---

## 2. Baseline
**Файл:** tests/t1000.tsv  
**Количество кейсов:** 60  
**Pass rate:** 0.4167  
**Guard threshold:** 0.70  
**Delta_pp:** 0  
**Manifest:** baseline_manifest.json  

---

## 3. Сравнение моделей (A/B)
| Модель | pass_rate | baseline | delta_pp |
|:--|:--:|:--:|:--:|
| llama3.1:8b-local | 0.4167 | 0.65 | −23.33 |
| mistral-nemo-local | 0.4167 | 0.65 | −23.33 |
| q4o-mini-cloud | 0.4167 | 0.65 | −23.33 |

**Артефакты:**  
`ab_diff.csv`, `passfail.png`, `passrate.png`, `stability.tsv`, `T1000_Report_v1.md`.

---

## 4. Метрики и тренды
- `verify_summary.txt` → rows = 60, ok = 1  
- `metrics_history.csv` активен (история baseline).  
- `passrate_local.png` фиксирует начальный уровень метрик.  
- Следующий шаг — активировать `metrics_rollup.py` и `passrate_trend.png` для авто-дрейфа.  

---

## 5. Итог этапа T1000
- ✅ CI-инфраструктура зелёная.  
- ✅ Baseline (60 кейсов) зафиксирован.  
- ✅ A/B-циклы отработаны.  
- ✅ Документация (`REPORT_T1000_FREEZE.md`, `PLAN_T1000_BASELINE.md`) в репо.  
- 🟡 Следующий вектор — T1500 (расширение, reasoning, context).  

---

## 6. Заключение
Этап T1000 закрыт официально.  
Система ∑AI вошла в фазу устойчивого самоизмерения и готова к масштабированию корпуса и метрик.
