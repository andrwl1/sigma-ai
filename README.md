# Pre-CI guard

Guard проверяет регрессию по `artifacts/summary/judgement.tsv` и валит билд при падении >2pp.
Порог настраивается переменной окружения `THRESHOLD_PP_2` (дефолт: `2`).

Артефакты:
- `artifacts/summary/judgement.tsv` — итог кейсов (OK/FAIL).
- `artifacts/summary/ab_diff.csv` — расхождения (id/ожидание/факт).
- `artifacts/summary/passfail.png` — тренд pass-rate.

Статус: ![Pre-CI](https://img.shields.io/badge/preci-guard-green)
## 📦 Артефакты

| Файл                              | Содержимое                    | Где появляется               |
|-----------------------------------|-------------------------------|------------------------------|
| `artifacts/summary/ab_report.md`  | Основной отчёт mini-bench     | CI, автокоммент в PR         |
| `artifacts/summary/ab_diff.csv`   | Дифф метрик (CSV)            | Guard RESULT (regression)    |
| `artifacts/summary/passrate.png`  | График passrate по тестам     | Mini-bench / CI              |

### 🔽 Скачивание артефактов из CI

Через UI:
1. **Actions** → выбрать нужный workflow run.
2. Внизу блока ранa — секция **Artifacts** → скачать zip.

Через CLI (пример для артефакта `preci-report`):
```bash
gh run list -L 5
gh run download <RUN_ID> --name "preci-report" --dir artifacts/summary
ls -lh artifacts/summary

