# Pre-CI guard
Guard проверяет регрессию по `artifacts/summary/judgement.tsv` и валит билд при падении >2pp.
Порог настраивается переменной окружения `THRESHOLD_PP_2` (дефолт `2`).
Артефакты: `artifacts/summary/judgement.tsv`, `artifacts/summary/ab_diff.csv`, `artifacts/summary/passfail.png`.
Статус: ![Pre-CI](https://img.shields.io/badge/preci-guard-green)
