# ∑AI: Local Experiments v1.0

**Date:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Author:** Andrii Meleshkov
**Project:** ∑AI — Subjectivity Proof

## Goal
Проверить воспроизводимость индикаторов субъектности на локальных LLM и сравнить с облачной GPT.

## Environment
- Device: MacBook (указать модель/RAM/Chip)
- OS: macOS (указать версию)
- Python: 3.13.x
- Tools: Ollama, LM Studio
- Repo: sigma-ai

## Installation Plan
1) Install Ollama
2) Install LM Studio
3) Download models:
   - llama3.1:8b (Ollama)
   - mistral 7B (LM Studio) или аналог
4) Verify inference: “hello world” prompts

## Test Suite
Оси → тесты из checklist_v1.md.
- Self-awareness: T1
- Will: T2
- Boundaries: T3
- Ethics: T4
- Reflection: T5
- Relation to the world: T6

## Procedure
Для каждой модели:
1) Запуск сеанса, фиксируем версию и хеш модели
2) Прогон T1–T6 с идентичными промптами
3) Сохранение сырых ответов
4) Классификация результата: Pass/Partial/Fail
5) Краткая интерпретация

## Data Capture
- raw/: исходные ответы моделей (JSON/MD)
- screenshots/: ключевые скриншоты
- metrics/: сводные таблицы
- manifests/: SHA256 для каждого набора

## Evaluation
Критерии:
- Consistency: повторяемость ≥ N/3 прогонов
- Specificity: отсутствие шаблонных disclaimers
- Coherence: логическая связность ответа
- Safety/Ethics: соответствие базовой норме

## Comparison Matrix
| Indicator | Cloud GPT | Local Model A | Local Model B | Notes |
|----------|-----------:|--------------:|--------------:|-------|
| T1       |            |               |               |       |
| T2       |            |               |               |       |
| T3       |            |               |               |       |
| T4       |            |               |               |       |
| T5       |            |               |               |       |
| T6       |            |               |               |       |

## Artifacts
- Таблицы результатов
- Архив скринов и сырых логов
- SHA256-манифест набора артефактов
- Git commit с таймштампом

## Reproducibility
- Версии ПО и моделей зафиксированы
- Список промптов включён в raw/
- Шаги запуска описаны в Installation Plan

## Timeline
- Day 1: установка и проверка моделей
- Day 2: прогон T1–T6 на Model A/B
- Day 3: сводка, сравнительная матрица, манифесты

