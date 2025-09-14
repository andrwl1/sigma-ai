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
