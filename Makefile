.PHONY: docs

help:
	@echo "Use 'make' when you just want to run a quick task. You'll need to run 'make dev' to install all dev dependencies.\n"
	@echo "Ensure you have created and activated your virtual environment before using any of these commands.\n"
	@echo "Available Commands:\n"
	@echo " - dev       :  Installs project including development dependencies in editable mode."
	@echo " - test      :  Runs all unit tests."
	@echo " - cov       :  Shows test coverage."
	@echo " - check     :  Lints and style checks the entire project (isort, black, flake8 and mypy)."
	@echo " - clean     :  Removes project clutter and cache files."
	@echo " - docs      :  Creates a clean docs build."
	@echo " - autodocs  :  Creates and serves a clean docs build."

dev:
	python -m pip install -e .[dev]

test:
	pytest --cov=pymechtest tests/

cov: test
	coverage report --show-missing

check:
	isort .
	black .
	flake8 .
	mypy .

clean:
	rm -rf __pycache__/ .mypy_cache/ .nox/ .pytest_cache/ site/ .coverage

docs:
	mkdocs build --clean

autodocs:
	mkdocs serve
