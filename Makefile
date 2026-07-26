VENV=.venv

lint:
	flake8 .  --exclude .git,__pycache__,venv,.venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs --exclude tests

# fix:
# 	@$ autopep8 --in-place --recursive *.py
# 	autopep8 $(git ls-files '*.py') --in-place
# 	$ find . -name '*.py' -exec autopep8 --in-place '{}' \;

install: requirements.txt
	@if [ ! -d "$(VENV)" ]; then echo "Creating virtual environment..."; python3 -m venv $(VENV); fi
	@echo "Environment active, installing dependencies from requirements.txt";
	@./.venv/bin/pip install -r requirements.txt --quiet
	@echo Dependencies installed!

run: install
	@./.venv/bin/python3 main.py

clean:
	@rm -rf __pycache__ .mypy_cache .pytest_cache
	@rm -rf modules/__pycache__ utils/__pycache__
	@rm -rf *.egg-info dist build
	@rm -rf .vscode/
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -delete
	@echo "Project cleaned..."

fclean: clean
	@rm -rf .venv/

.PHONY: lint create activate install run clean fclean