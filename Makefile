# ================================
# Makefile for Sigma-AI Pre-CI
# ================================

# Запуск всех тестов (pytest)
test:
	pytest -q --disable-warnings -q

# Локальный прогон регрессионного гуарда
guard:
	./scripts/guard_regress.sh

# Построение графика pass-rate
report:
	python3 scripts/plot_passrate.py

# Диагностика и наблюдаемость (PNG + CSV)
diagnostics:
	python3 scripts/stability_report.py

# Локальный прогон CI (тесты + отчёт)
ci-local:
	pytest -q --junitxml=report.xml || true
	python3 scripts/plot_passrate.py
	python3 scripts/stability_report.py

# Чистка временных файлов и артефактов
clean:
	rm -rf __pycache__ .pytest_cache artifacts/summary/*.png artifacts/summary/*.csv report.xml
