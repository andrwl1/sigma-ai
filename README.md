## 📦 Артефакты

| Файл                           | Содержимое                  | Где появляется             |
|--------------------------------|-----------------------------|----------------------------|
| `artifacts/summary/ab_report.md` | Основной отчёт mini-bench   | CI, автокоммент в PR       |
| `artifacts/summary/ab_diff.csv`  | Дифф метрик (CSV)           | Guard RESULT (regression)  |
| `artifacts/summary/passrate.png` | График passrate по тестам   | Mini-bench / CI            |

## ⬇️ Скачивание артефактов из CI

Через UI:
1. Зайти во вкладку **Actions** → выбрать нужный workflow run.
2. Внизу страницы есть блок **Artifacts** → скачать zip.

Через CLI (пример для артефакта `preci-report`):
```bash
gh run list -L 5
gh run download <RUN_ID> --name "preci-report" --dir artifacts/summary
ls -lh artifacts/summary
