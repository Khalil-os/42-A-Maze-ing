PYTHON = python3
MAIN_SCRIPT = a_maze_ing.py
CONFIG_FILE = config.txt

.PHONY: install run debug clean lint lint-strict

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)

debug:
	@echo "Running in debug mode..."
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

clean:
	@echo "Cleaning up caches and temporary files..."
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf mazegen/__pycache__
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

lint:
	@echo "Running linters..."
	flake8 --exclude=venv_test
	mypy --exclude venv_test --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	@echo "Running strict linters..."
	flake8 --exclude=venv_test
	mypy --strict .