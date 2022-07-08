# TODO: add mypy

.PHONY: fmt fmt-check lint test

.venv:
	@python -m venv .venv
	@poetry install

fmt:
	@poetry run isort .
	@poetry run black . --exclude .venv

fmt-check:
	@poetry run isort . --check
	@poetry run black . --exclude .venv --check

lint:
	@poetry run flake8 . --exclude .venv

test: fmt-check lint
	@poetry run pytest
