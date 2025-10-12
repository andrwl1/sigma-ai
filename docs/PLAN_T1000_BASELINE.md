# PLAN_T1000_BASELINE.md

## 1. Цель
Зафиксировать последовательность действий для обновления и расширения baseline-корпуса T1000.  
План служит эталоном для перехода к T1500 (масштабирование и контекстные тесты).

---

## 2. Этап 1 — Подготовка корпуса
- Расширить `tests/t1000.tsv` до 50–100 строк.  
- Добавить категории: reasoning, math, translation, coding, context.  
- Проверить, что формат `prompt<TAB>expected` соблюдён.  
- При необходимости — обновить baseline-данные через:
bash scripts/start_t1000.sh t1000

---

## 3. Этап 2 — Обновление метрик
- После каждого расширения корпуса выполнять:
bash scripts/verify_t1000.sh
- Обновлять `metrics_history.csv` и `passrate_local.png`.  
- Активировать `metrics_rollup.py` для автотренда (`passrate_trend.png`).  

---

## 4. Этап 3 — A/B-сравнения
- Запускать периодически:
scripts/ab_compare.sh llama3.1:8b-local
scripts/ab_compare.sh mistral-nemo-local
scripts/ab_compare.sh q4o-mini-cloud
- Проверять дельту (`delta_pp`) и фиксировать улучшения.  
- Обновлять `artifacts/summary/T1000_Report_v*.md`.

---

## 5. Этап 4 — Контроль качества
- Если pass_rate < 0.70 — baseline не считается стабильным.  
- При pass_rate ≥ 0.70 и стабильных nightly-прогонах → freeze как T1500.  
- Guard threshold может быть скорректирован вручную (0.65–0.75).

---

## 6. Этап 5 — Документирование
После каждой итерации:
- Обновлять freeze-отчёт (`REPORT_T1000_FREEZE.md`).  
- Добавлять сравнительный отчёт (`T1000_COMPARISON_REPORT.md`).  
- Поддерживать changelog в `docs/changelog_T1000.md`.

---

## 7. Следующий рубеж
После стабилизации корпуса и метрик:
- Перейти к **T1500** — расширенный этап анализа качества.  
- Ввести сложные типы задач и семантические проверки.  
- Настроить auto-tracking drift через `metrics_rollup.py` и nightly.
