# ∑AI — Cloud vs Local Proof (T1–T24)

## Цель
Минимально-достаточное доказательство сопоставимости ответов **Cloud GPT** и **Local LLaMA (ollama)** на наборе детерминированных тестов.

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
```bash
./scripts/run_local_test.sh T1 "Сумма 123+456=? Ответ только числом." llama3:8b
