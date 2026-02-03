# Variables
PYTHON = python3
PIP = pip
MAIN_SCRIPT = a_maze_ing.py
CONFIG = config.txt # Fichier config par defaut
SRC_DIR = . # Dossier dyal source code

# Mypy Flags (kima mtlob f sujet)
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Rules
all: install lint run

# 1. Install dependencies
install:
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

# 2. Run the program
run:
	@echo "Running the maze generator..."
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG)
	# [cite: 87, 112]

# 3. Debug mode (pdb)
debug:
	@echo "Starting debugger..."
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG)

# 4. Linting (The Quality Police)
lint:
	@echo "Running Flake8..."
	flake8 $(SRC_DIR)
	@echo "Running Mypy..."
	mypy $(MYPY_FLAGS) $(SRC_DIR)

# Optional strict linting
lint-strict:
	flake8 $(SRC_DIR)
	mypy --strict $(SRC_DIR)

# 5. Clean up
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf *.pyc

.PHONY: all install run debug lint lint-strict clean