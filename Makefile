# Task runner for carla-distributed-causal-forensics.
# Override the interpreter if you are not using the documented conda env:
#   make test PYTHON=/path/to/python
PYTHON ?= python
ARTIFACTS ?= artifacts_v2
SEEDS ?= 0 1 2

.PHONY: help install env-check test test-fast test-carla lint leakage verify \
        s1 suite counterfactuals evaluate report viewer clean

help:
	@echo "install          - editable install of the cdf package"
	@echo "env-check        - inspect Python/CARLA environment"
	@echo "test             - full pytest run (CARLA tests skipped if no server)"
	@echo "test-fast        - pytest excluding CARLA and slow-marked tests"
	@echo "test-carla       - only CARLA-marked integration tests"
	@echo "lint             - pyflakes over src, scripts and tests"
	@echo "leakage          - run the anti-leakage test suite only"
	@echo "verify           - re-hash recorded runs against their evidence manifests"
	@echo "s1               - run scenario S01 with seed 0"
	@echo "suite            - run all scenarios for SEEDS='$(SEEDS)'"
	@echo "counterfactuals  - counterfactual replays for RUN=<run_dir>"
	@echo "evaluate         - evaluate RUN=<run_dir>"
	@echo "report           - aggregate all runs under $(ARTIFACTS)"
	@echo "viewer           - serve the forensic viewer for RUN=<run_dir>"

install:
	$(PYTHON) -m pip install -e .

env-check:
	$(PYTHON) scripts/check_environment.py

test:
	$(PYTHON) -m pytest -q

test-fast:
	$(PYTHON) -m pytest -q -m "not carla and not slow"

test-carla:
	$(PYTHON) -m pytest -q -m carla

lint:
	$(PYTHON) -m pyflakes src scripts tests

leakage:
	$(PYTHON) -m pytest -q tests/test_no_privileged_leakage.py

verify:
	$(PYTHON) scripts/verify_evidence.py --artifacts $(ARTIFACTS)

s1:
	$(PYTHON) scripts/run_scenario.py --scenario S01 --seed 0

suite:
	$(PYTHON) scripts/run_suite.py --all --seeds $(SEEDS)

counterfactuals:
	$(PYTHON) scripts/run_counterfactuals.py --run $(RUN)

evaluate:
	$(PYTHON) scripts/evaluate.py --run $(RUN)

report:
	$(PYTHON) scripts/generate_report.py --artifacts $(ARTIFACTS)

viewer:
	$(PYTHON) scripts/serve_viewer.py --run $(RUN)

clean:
	rm -rf .pytest_cache **/__pycache__ src/*.egg-info
