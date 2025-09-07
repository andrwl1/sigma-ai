![Pre-CI](https://github.com/andrwl1/sigma-ai/actions/workflows/pre-ci.yml/badge.svg)
# ∑AI — Cloud vs Local Proof (T1–T24)

## Цель
Минимально-достаточное доказательство сопоставимости ответов **Cloud GPT** ↔ **Local LLaMA (ollama)** на наборе детерминированных тестов **T1–T24** с фиксацией артефактов и отчёта.

## Структура

## Структура
src/        — код инструментов
tests/      — сценарии и карта expected
scripts/    — раннеры (local, cloud, report)
artifacts/  — raw/ (cloud/local), reports/ (отчёты)
summary/    — сводка cloud_vs_local.md
docs/       — документация

## Быстрый старт
0. Подготовка: установить `ollama`, экспортировать `OPENAI_API_KEY`.
1. Локальный тест:
   ./scripts/run_local_test.sh T1 "Сумма 123+456=? Ответ только числом." llama3:8b
2. Облачный тест:
   ./scripts/run_cloud_test.sh T1 "Сумма 123+456=? Ответ только числом." gpt-4o-mini
3. Собрать отчёт:
   python3 scripts/build_report.py
4. Зафиксировать изменения:
   git add artifacts summary README.md
   git commit -m "docs: minimal README + repo skeleton"

## Статус
- T1–T24 локально и в облаке закрыты.
- Артефакты сохранены в artifacts/.
- Сводка в summary/cloud_vs_local.md.
- Отчёт: artifacts/reports/cloud_vs_local_report.md.
