VENV=.venv
PIP=./.venv/bin/pip
PYTHON=./.venv/bin/python3
RM=rm
RM_FLAG=-rf
RM_RF=$(RM) $(RM_FLAG)
THIS_FILE := $(lastword $(MAKEFILE_LIST))

lint:
	flake8 .  --exclude .git,__pycache__,venv,.venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs --exclude tests

# fix:
# 	@$ autopep8 --in-place --recursive *.py
# 	autopep8 $(git ls-files '*.py') --in-place
# 	$ find . -name '*.py' -exec autopep8 --in-place '{}' \;

update:
	@$(PIP) install --upgrade pip

install: requirements.txt
	@if [ ! -d "$(VENV)" ]; then echo "Creating virtual environment..."; python3 -m venv $(VENV); fi
	@echo "Environment active, installing dependencies from requirements.txt";
	@$(MAKE) -f $(THIS_FILE) update
	@$(PIP) install -r requirements.txt --quiet
	@echo Dependencies installed!

run: install
	clear
	@$(PYTHON) main.py

clean:
	@$(RM_RF) __pycache__ .mypy_cache .pytest_cache
	@$(RM_RF) modules/__pycache__ utils/__pycache__
	@$(RM_RF) *.egg-info dist build
	@$(RM_RF) .vscode/
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -delete
	@echo "Project cleaned..."

fclean: clean
	@$(RM_RF) .venv/

.PHONY: lint update install run clean fclean