.PHONY: test guard report ci-local
test:
	pytest -q --junitxml=report.xml

guard:
	bash scripts/guard_regress.sh

report:
	python3 scripts/plot_passrate.py

ci-local: test guard report

integration:
	bash run_integration.sh

dev:
	python3 -m venv .venv && . .venv/bin/activate && python -m pip install -U pip && python -m pip install -r requirements-dev.txt
