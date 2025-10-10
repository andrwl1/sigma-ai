# 🧭 PLAN T1500 BASELINE → Transition to T2000 Expansion

## 1. Цель
Закрепить лабораторно-чистую фазу T1500 и подготовить систему ∑AI к расширению корпуса и дрейф-анализу.
Основная задача — перейти от верифицированного baseline к исследовательскому ядру (T2000), сохранив полную воспроизводимость и контроль метрик.

---

## 2. Исходная точка
**Тег:** `t1500-freeze`  
**Состояние:** baseline стабилен, pass_rate = 1.0  
**Метрики активны:** BLEU, ROUGE-L, cosine similarity  
**Пайплайн:** `run_metrics.sh` + `rollup.sh`  
**Документы:**  
- `REPORT_T1500_FREEZE.md`  
- `REPRO_T1500_VALIDATION.md`

---

## 3. Цели перехода
1. Расширить корпус (T2000) до 300–400 кейсов.  
2. Увеличить вариативность данных (multi-category sampling).  
3. Подключить baseline сравнение между моделями (LLaMA, Mistral, Q4, OpenAI).  
4. Ввести drift-анализ (semantic & stylistic drift).  
5. Проверить стабильность pass_rate при росте корпуса.  

---

## 4. Базовая структура корпуса
Файл: `tests/t2000.tsv`  
Структура:
| Категория | Примеров | Примечание |
|------------|-----------|-------------|
| reasoning | 60 | логические задачи |
| translation | 60 | двунаправленные пары (RU↔EN) |
| math | 60 | числовые и алгебраические примеры |
| coding | 60 | генерация кода и вывод |
| context | 60 | многошаговые сценарии |

---

## 5. Контрольные метрики
| Метрика | Цель | Допуск |
|----------|------|--------|
| pass_rate | ≥ 0.70 | Δ ≤ 5% |
| BLEU | ≥ 0.40 | Δ ≤ 0.05 |
| ROUGE-L | ≥ 0.45 | Δ ≤ 0.05 |
| cosine | ≥ 0.70 | Δ ≤ 0.05 |
| semantic drift | ≤ 2% | — |

---

## 6. Технический стек
- Python 3.12  
- sacrebleu / evaluate / sentence-transformers  
- matplotlib / csv / json  
- scripts:  
  - `run_metrics.sh` — основной pipeline  
  - `run_rollup.sh` — автоагрегация истории  
  - `run_check.sh` — проверка порогов  
- Ветка: `master`  
- Тег freeze: `t1500-freeze`

---

## 7. Этапы перехода
| Этап | Задача | Цель |
|------|---------|------|
| I | Подготовить корпус `t2000.tsv` | 300+ кейсов |
| II | Прогнать baseline на mock и sigma | сверка pass_rate |
| III | Активировать drift-анализ | semantic drift tracking |
| IV | Freeze `t2000-freeze` | завершить фазу расширения |

---

## 8. Критерии завершения перехода
✅ pass_rate ≥ 0.70  
✅ стабильные BLEU/ROUGE/cosine  
✅ корректный rollup-график  
✅ freeze-документы оформлены  
✅ archive snapshot сохранён (`archive_2025-10-10`)

---

## 9. Коммит и тег
```bash
git add docs/PLAN_T1500_BASELINE.md
git commit -m "Docs: PLAN_T1500_BASELINE.md — baseline → T2000 transition"
git tag t1500-baseline
