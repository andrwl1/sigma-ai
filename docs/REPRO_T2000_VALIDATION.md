# REPRO_T2000_VALIDATION
Шаги воспроизведения:
1. pip install -e .
2. bash scripts/run_t2000.sh tests/t2000.tsv artifacts/t2000 artifacts/metrics_history.csv
3. bash scripts/run_t2000_rollup.sh artifacts/t2000 artifacts/metrics_history.csv artifacts/trend_drift_t2000.png
Ожидаемо: pass_rate ≥0.70, расхождение с nightly ≤5% по pass_rate и ≤2% по semantic_score.
